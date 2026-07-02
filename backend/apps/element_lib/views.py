from rest_framework.decorators import api_view
from django.db.models import Q
from apps.element_lib.models import KbElement
from apps.element_lib.serializers import KbElementSerializer
from apps.knowledge.models import KbAssetStep, KbAssetScript
from core.response import ApiResponse
from core.middleware import get_current_project_id


@api_view(['POST'])
def element_list(request):
    project_id = get_current_project_id()
    page_name = request.data.get('page_name', '')
    status = request.data.get('status', '')
    keyword = request.data.get('keyword', '')
    qs = KbElement.objects.all()
    if project_id:
        qs = qs.filter(project_id=project_id)
    if page_name:
        qs = qs.filter(page_name=page_name)
    if status:
        qs = qs.filter(status=status)
    if keyword:
        qs = qs.filter(Q(element_name__icontains=keyword) | Q(page_name__icontains=keyword))
    qs = qs.order_by('-update_time')
    serializer = KbElementSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def element_save(request):
    instance_id = request.data.get('id')
    instance = KbElement.objects.filter(id=instance_id).first() if instance_id else None
    old_locator = (instance.locator_type, instance.locator_value) if instance else (None, None)
    serializer = KbElementSerializer(instance=instance, data=request.data, partial=bool(instance))
    if not serializer.is_valid():
        return ApiResponse.error(message=str(serializer.errors))
    element = serializer.save()

    new_locator = (element.locator_type, element.locator_value)
    if instance and old_locator != new_locator:
        updated_count = KbAssetScript.objects.filter(
            asset__steps__element_name=element.element_name,
            is_last=True,
        ).count()
        if updated_count > 0:
            element.last_refresh_time = __import__('datetime').datetime.now()
            element.save()

    return ApiResponse.success(data=serializer.data, message='保存成功')


@api_view(['POST'])
def element_repair(request):
    element_id = request.data.get('id')
    new_locator_type = request.data.get('locator_type', '')
    new_locator_value = request.data.get('locator_value', '')

    element = KbElement.objects.filter(id=element_id).first()
    if not element:
        return ApiResponse.error(message='元素不存在')

    if new_locator_type and new_locator_value:
        element.locator_type = new_locator_type
        element.locator_value = new_locator_value

    element.status = 'valid'
    element.last_refresh_time = __import__('datetime').datetime.now()
    element.save()

    asset_ids = KbAssetStep.objects.filter(
        element_name__iexact=element.element_name
    ).values_list('asset_id', flat=True).distinct()

    updated_scripts = 0
    for asset_id in asset_ids:
        scripts = KbAssetScript.objects.filter(asset_id=asset_id, is_last=True)
        for script in scripts:
            old_content = script.script_content
            if element.locator_value in old_content:
                continue
            updated_scripts += 1

    return ApiResponse.success(data={
        'element': KbElementSerializer(element).data,
        'affected_assets': len(asset_ids),
        'affected_scripts': updated_scripts,
    }, message=f'元素修复成功，影响 {len(asset_ids)} 个资产，{updated_scripts} 个脚本')


@api_view(['POST'])
def element_related_cases(request):
    element_name = request.data.get('element_name', '')
    if not element_name:
        return ApiResponse.error(message='请提供元素名称')
    asset_ids = KbAssetStep.objects.filter(
        element_name__icontains=element_name
    ).values_list('asset_id', flat=True).distinct()
    from apps.knowledge.models import KbAsset
    assets = KbAsset.objects.filter(id__in=list(asset_ids)).values('id', 'asset_name', 'status')
    return ApiResponse.success(data={'assets': list(assets), 'count': len(asset_ids)})
