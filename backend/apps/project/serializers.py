from rest_framework import serializers
from apps.project.models import SysProject, ProjectMember
from core.middleware import get_current_project_id


class SysProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysProject
        fields = '__all__'
        read_only_fields = ('create_time', 'update_time')

    def validate_project_code(self, value):
        instance = self.instance
        qs = SysProject.objects.filter(project_code=value)
        if instance:
            qs = qs.exclude(id=instance.id)
        if qs.exists():
            raise serializers.ValidationError('项目编码已存在')
        return value


class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = '__all__'
        read_only_fields = ('create_time',)
