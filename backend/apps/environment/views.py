from rest_framework.decorators import api_view
from apps.environment.models import KbEnv, KbCredential
from apps.environment.serializers import KbEnvSerializer, KbCredentialSerializer, KbCredentialListSerializer
from core.response import ApiResponse
from core.middleware import get_current_project_id
from core.security import aes_encrypt


@api_view(['POST'])
def env_list(request):
    project_id = get_current_project_id()
    qs = KbEnv.objects.all()
    if project_id:
        qs = qs.filter(project_id=project_id)
    qs = qs.order_by('-create_time')
    serializer = KbEnvSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def env_save(request):
    instance_id = request.data.get('id')
    instance = KbEnv.objects.filter(id=instance_id).first() if instance_id else None
    serializer = KbEnvSerializer(instance=instance, data=request.data, partial=bool(instance))
    if not serializer.is_valid():
        return ApiResponse.error(message=str(serializer.errors))
    serializer.save()
    return ApiResponse.success(data=serializer.data, message='保存成功')


@api_view(['POST'])
def credential_list(request):
    env_id = request.data.get('env_id')
    qs = KbCredential.objects.all()
    if env_id:
        qs = qs.filter(env_id=env_id)
    serializer = KbCredentialListSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def credential_save(request):
    data = request.data.copy()
    for field in ('password', 'cookie', 'token'):
        if data.get(field) and not data[field].startswith('AES:'):
            data[field] = aes_encrypt(data[field])
    instance_id = data.get('id')
    instance = KbCredential.objects.filter(id=instance_id).first() if instance_id else None
    serializer = KbCredentialSerializer(instance=instance, data=data, partial=bool(instance))
    if not serializer.is_valid():
        return ApiResponse.error(message=str(serializer.errors))
    serializer.save()
    return ApiResponse.success(data={'id': serializer.instance.id}, message='保存成功')
