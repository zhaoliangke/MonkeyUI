from rest_framework.decorators import api_view
from apps.reflux.models import KbRefluxRecord
from apps.reflux.serializers import KbRefluxRecordSerializer
from apps.reflux.service import RefluxService
from core.response import ApiResponse
from core.middleware import get_current_project_id
from core.exception import NotFoundException


@api_view(['POST'])
def reflux_list(request):
    project_id = get_current_project_id()
    status = request.data.get('status', '')
    qs = KbRefluxRecord.objects.all()
    if project_id:
        qs = qs.filter(project_id=project_id)
    if status:
        qs = qs.filter(status=status)
    qs = qs.order_by('-create_time')
    serializer = KbRefluxRecordSerializer(qs, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def reflux_detail(request):
    record_id = request.data.get('id')
    if not record_id:
        return ApiResponse.error(message='请提供记录ID')
    record = KbRefluxRecord.objects.filter(id=record_id).first()
    if not record:
        raise NotFoundException('回流记录不存在')
    data = KbRefluxRecordSerializer(record).data
    data['diff_content'] = RefluxService.compute_diff(record.asset_id)
    return ApiResponse.success(data=data)


@api_view(['POST'])
def reflux_audit(request):
    record_id = request.data.get('id')
    action = request.data.get('action', 'merge')
    audit_user = request.data.get('audit_user', 'admin')
    if not record_id:
        return ApiResponse.error(message='请提供记录ID')
    try:
        record = RefluxService.apply_reflux(record_id, action, audit_user)
        return ApiResponse.success(data=KbRefluxRecordSerializer(record).data, message='审核操作成功')
    except ValueError as e:
        return ApiResponse.error(message=str(e))


@api_view(['POST'])
def reflux_rollback(request):
    record_id = request.data.get('id')
    if not record_id:
        return ApiResponse.error(message='请提供回流记录ID')
    record = KbRefluxRecord.objects.filter(id=record_id).first()
    if not record:
        raise NotFoundException('回流记录不存在')
    record.status = 'ignored'
    record.audit_time = __import__('datetime').datetime.now()
    record.save()
    return ApiResponse.success(message='版本已回滚')
