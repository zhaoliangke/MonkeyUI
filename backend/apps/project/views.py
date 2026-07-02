from rest_framework.decorators import api_view
from django.db.models import Q
from apps.project.models import SysProject, ProjectMember
from apps.project.serializers import SysProjectSerializer, ProjectMemberSerializer
from apps.project.service import ProjectService
from core.response import ApiResponse
from core.exception import NotFoundException


@api_view(['POST'])
def project_list(request):
    keyword = request.data.get('keyword', '')
    status = request.data.get('status')
    qs = SysProject.objects.all()
    if keyword:
        qs = qs.filter(Q(project_name__icontains=keyword) | Q(project_code__icontains=keyword))
    if status is not None:
        qs = qs.filter(status=status)
    qs = qs.order_by('-create_time')
    projects = qs.all()
    serializer = SysProjectSerializer(projects, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def project_save(request):
    instance_id = request.data.get('id')
    instance = SysProject.objects.filter(id=instance_id).first() if instance_id else None
    serializer = SysProjectSerializer(instance=instance, data=request.data, partial=bool(instance))
    if not serializer.is_valid():
        return ApiResponse.error(message=str(serializer.errors), code=400)
    project = serializer.save()
    return ApiResponse.success(data=SysProjectSerializer(project).data, message='保存成功')


@api_view(['POST'])
def project_set_default(request):
    project_id = request.data.get('id')
    if not project_id:
        return ApiResponse.error(message='请提供项目ID')
    project = ProjectService.set_default(project_id)
    return ApiResponse.success(data=SysProjectSerializer(project).data, message='已设为默认项目')


@api_view(['POST'])
def project_permission_save(request):
    project_id = request.data.get('project_id')
    members_data = request.data.get('members', [])
    if not project_id:
        return ApiResponse.error(message='请提供项目ID')
    ProjectService.save_members(project_id, members_data)
    return ApiResponse.success(message='权限配置保存成功')


@api_view(['GET'])
def project_members(request, project_id):
    members = ProjectService.get_members(project_id)
    serializer = ProjectMemberSerializer(members, many=True)
    return ApiResponse.success(data=serializer.data)


@api_view(['POST'])
def project_delete(request):
    project_id = request.data.get('id')
    if not project_id:
        return ApiResponse.error(message='请提供项目ID')
    project = SysProject.objects.filter(id=project_id).first()
    if not project:
        raise NotFoundException('项目不存在')
    project.delete()
    return ApiResponse.success(message='删除成功')
