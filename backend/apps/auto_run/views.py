from rest_framework.decorators import api_view
from apps.auto_run.models import KbRunRecord
from apps.auto_run.serializers import KbRunRecordSerializer
from apps.auto_run.service import RunEngineService
from core.response import ApiResponse
from core.middleware import get_current_project_id
from core.exception import NotFoundException


@api_view(['POST'])
def run_execute(request):
    asset_id = request.data.get('asset_id')
    if not asset_id:
        return ApiResponse.error(message='请提供资产ID')
    try:
        record_id = RunEngineService.execute_asset(asset_id, 'single')
        return ApiResponse.success(data={'record_id': record_id}, message='执行任务已提交')
    except ValueError as e:
        return ApiResponse.error(message=str(e))


@api_view(['POST'])
def run_batch(request):
    asset_ids = request.data.get('asset_ids', [])
    if not asset_ids:
        return ApiResponse.error(message='请选择要执行的资产')
    record_ids = RunEngineService.execute_batch(asset_ids, 'batch')
    return ApiResponse.success(data={'record_ids': record_ids, 'count': len(record_ids)}, message=f'已提交{len(record_ids)}个执行任务')


@api_view(['POST'])
def record_list(request):
    project_id = get_current_project_id()
    asset_id = request.data.get('asset_id')
    result = request.data.get('result', '')
    qs = KbRunRecord.objects.all()
    if project_id:
        qs = qs.filter(project_id=project_id)
    if asset_id:
        qs = qs.filter(asset_id=asset_id)
    if result:
        qs = qs.filter(result=result)
    qs = qs.order_by('-run_time')
    serializer = KbRunRecordSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def record_detail(request):
    record_id = request.data.get('id')
    if not record_id:
        return ApiResponse.error(message='请提供记录ID')
    record = KbRunRecord.objects.filter(id=record_id).first()
    if not record:
        raise NotFoundException('执行记录不存在')
    return ApiResponse.success(data=KbRunRecordSerializer(record).data)
