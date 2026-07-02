from rest_framework.decorators import api_view
from django.db.models import Q
from apps.knowledge.models import KbCategory, KbAsset, KbAssetStep, KbAssetScript, KbAssetVersion
from apps.knowledge.serializers import (
    KbCategorySerializer, KbAssetSerializer, KbAssetStepSerializer,
    KbAssetScriptSerializer, KbAssetVersionSerializer,
)
from apps.knowledge.service import KnowledgeService
from core.response import ApiResponse
from core.middleware import get_current_project_id
from core.exception import NotFoundException


@api_view(['POST'])
def dashboard_stats(request):
    project_id = get_current_project_id()
    stats = KnowledgeService.get_dashboard_stats(project_id)
    return ApiResponse.success(data=stats)


@api_view(['POST'])
def category_list(request):
    project_id = get_current_project_id()
    qs = KnowledgeService.get_category_tree(project_id) if project_id else KbCategory.objects.filter(parent_id__isnull=True)
    serializer = KbCategorySerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def category_save(request):
    instance_id = request.data.get('id')
    instance = KbCategory.objects.filter(id=instance_id).first() if instance_id else None
    serializer = KbCategorySerializer(instance=instance, data=request.data, partial=bool(instance))
    if not serializer.is_valid():
        return ApiResponse.error(message=str(serializer.errors))
    serializer.save()
    return ApiResponse.success(data=serializer.data, message='保存成功')


@api_view(['POST'])
def asset_list(request):
    project_id = get_current_project_id()
    keyword = request.data.get('keyword', '')
    status = request.data.get('status', '')
    category_id = request.data.get('category_id')
    qs = KbAsset.objects.all()
    if project_id:
        qs = qs.filter(project_id=project_id)
    if keyword:
        qs = qs.filter(Q(asset_name__icontains=keyword) | Q(pre_condition__icontains=keyword))
    if status:
        qs = qs.filter(status=status)
    if category_id:
        qs = qs.filter(category_id=category_id)
    qs = qs.order_by('-update_time')
    serializer = KbAssetSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def asset_save(request):
    data = request.data.copy()
    data['version'] = data.get('version', 1)
    asset = KnowledgeService.save_asset_with_steps(data)
    return ApiResponse.success(data=KbAssetSerializer(asset).data, message='保存成功')


@api_view(['GET'])
def asset_detail(request, asset_id):
    asset = KbAsset.objects.filter(id=asset_id).first()
    if not asset:
        raise NotFoundException('资产不存在')
    serializer = KbAssetSerializer(asset)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def asset_batch(request):
    action = request.data.get('action', '')
    ids = request.data.get('ids', [])
    if not ids:
        return ApiResponse.error(message='请选择资产')

    assets = KbAsset.objects.filter(id__in=ids)
    if action == 'archive':
        assets.update(status='invalidated')
    elif action == 'enable':
        assets.update(status='published')
    elif action == 'disable':
        assets.update(status='draft')
    elif action == 're-crawl':
        assets.update(status='pending_update')
    elif action == 'migrate':
        category_id = request.data.get('category_id')
        if category_id:
            assets.update(category_id=category_id)
        else:
            return ApiResponse.error(message='请选择目标分类')
    else:
        return ApiResponse.error(message='未知操作类型')
    return ApiResponse.success(message=f'批量{action}操作成功')


@api_view(['POST'])
def script_save(request):
    asset_id = request.data.get('asset_id')
    engine_type = request.data.get('engine_type', 'playwright')
    script_content = request.data.get('script_content', '')
    if not asset_id:
        return ApiResponse.error(message='请提供资产ID')
    script = KnowledgeService.save_script(asset_id, engine_type, script_content)
    return ApiResponse.success(data=KbAssetScriptSerializer(script).data, message='脚本保存成功')


@api_view(['POST'])
def version_diff(request):
    asset_id = request.data.get('asset_id')
    version_a = request.data.get('version_a')
    version_b = request.data.get('version_b')
    if not all([asset_id, version_a, version_b]):
        return ApiResponse.error(message='参数不完整')
    result = KnowledgeService.get_version_diff(asset_id, version_a, version_b)
    return ApiResponse.success(data=result)
