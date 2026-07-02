from django.db import transaction
from apps.project.models import SysProject, ProjectMember
from core.exception import BusinessException, NotFoundException


class ProjectService:

    @staticmethod
    @transaction.atomic
    def set_default(project_id: int):
        project = SysProject.objects.filter(id=project_id).first()
        if not project:
            raise NotFoundException('项目不存在')
        SysProject.objects.update(is_default=False)
        project.status = 1
        project.save()
        return project

    @staticmethod
    def get_default_project_id():
        project = SysProject.objects.filter(status=1).first()
        return project.id if project else None

    @staticmethod
    def save_members(project_id: int, members_data: list):
        project = SysProject.objects.filter(id=project_id).first()
        if not project:
            raise NotFoundException('项目不存在')
        ProjectMember.objects.filter(project=project).delete()
        for member in members_data:
            ProjectMember.objects.create(
                project=project,
                user_id=member.get('user_id'),
                role=member.get('role', 'member'),
            )

    @staticmethod
    def get_members(project_id: int):
        return ProjectMember.objects.filter(project_id=project_id)
