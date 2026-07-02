from rest_framework.decorators import api_view
from apps.llm_engine.models import LlmGlobalConfig, LlmPromptTemplate, LlmGenerateLog
from apps.llm_engine.serializers import LlmGlobalConfigSerializer, LlmPromptTemplateSerializer, LlmGenerateLogSerializer
from apps.llm_engine.service import LLMService
from apps.llm_engine.client import LLMClient
from core.response import ApiResponse
from core.middleware import get_current_project_id
from core.security import aes_encrypt, aes_decrypt
from core.logger import log_error


@api_view(['POST'])
def config_save(request):
    data = request.data.copy()
    if data.get('api_key') and not data['api_key'].startswith('AES:'):
        data['api_key'] = aes_encrypt(data['api_key'])

    instance_id = data.get('id')
    instance = LlmGlobalConfig.objects.filter(id=instance_id).first() if instance_id else None
    serializer = LlmGlobalConfigSerializer(instance=instance, data=data, partial=bool(instance))
    if not serializer.is_valid():
        return ApiResponse.error(message=str(serializer.errors))
    config = serializer.save()
    result_data = LlmGlobalConfigSerializer(config).data
    result_data['api_key'] = '******'
    return ApiResponse.success(data=result_data, message='保存成功')


@api_view(['POST'])
def config_test(request):
    data = request.data
    api_key = data.get('api_key', '')
    if api_key and not api_key.startswith('AES:'):
        pass
    elif api_key:
        api_key = aes_decrypt(api_key)
    else:
        config_id = data.get('id')
        config = LlmGlobalConfig.objects.filter(id=config_id).first()
        if not config:
            return ApiResponse.error(message='未找到LLM配置')
        api_key = aes_decrypt(config.api_key)

    client = LLMClient(
        api_base=data.get('api_base', ''),
        api_key=api_key,
        timeout=30,
    )
    result = client.test_connectivity()
    return ApiResponse.success(data=result)


@api_view(['POST'])
def template_list(request):
    project_id = get_current_project_id()
    template_type = request.data.get('template_type', '')
    qs = LlmPromptTemplate.objects.filter(is_enable=True)
    if project_id:
        qs = qs.filter(project_id=project_id)
    if template_type:
        qs = qs.filter(template_type=template_type)
    qs = qs.order_by('sort', '-create_time')
    serializer = LlmPromptTemplateSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def template_save(request):
    instance_id = request.data.get('id')
    instance = LlmPromptTemplate.objects.filter(id=instance_id).first() if instance_id else None
    serializer = LlmPromptTemplateSerializer(instance=instance, data=request.data, partial=bool(instance))
    if not serializer.is_valid():
        return ApiResponse.error(message=str(serializer.errors))
    serializer.save()
    return ApiResponse.success(data=serializer.data, message='保存成功')


@api_view(['POST'])
def generate_script(request):
    project_id = get_current_project_id()
    asset_id = request.data.get('asset_id')
    steps_text = request.data.get('steps_text', '')
    elements_text = request.data.get('elements_text', '')
    template_type = request.data.get('template_type', 'script_gen')
    extra_vars = request.data.get('extra_vars', {})

    if not steps_text:
        return ApiResponse.error(message='请输入自然语言步骤')

    result = LLMService.generate_script(
        project_id=project_id,
        asset_id=asset_id,
        steps_text=steps_text,
        elements_text=elements_text,
        template_type=template_type,
        extra_vars=extra_vars,
    )
    if result.get('success'):
        return ApiResponse.success(data={
            'script_content': result.get('content'),
            'cost_time': result.get('cost_time'),
            'log_id': result.get('log_id'),
        }, message='脚本生成成功')
    else:
        return ApiResponse.error(message=result.get('error', '脚本生成失败'))


@api_view(['POST'])
def log_list(request):
    project_id = get_current_project_id()
    asset_id = request.data.get('asset_id')
    status = request.data.get('status')
    keyword = request.data.get('keyword', '')
    qs = LlmGenerateLog.objects.all()
    if project_id:
        qs = qs.filter(project_id=project_id)
    if asset_id:
        qs = qs.filter(asset_id=asset_id)
    if status:
        qs = qs.filter(status=status)
    if keyword:
        qs = qs.filter(input_content__icontains=keyword)
    qs = qs.order_by('-create_time')
    serializer = LlmGenerateLogSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)
