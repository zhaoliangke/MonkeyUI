from django.db import models


class SysProject(models.Model):
    STATUS_CHOICES = (
        (1, '启用'),
        (0, '禁用'),
    )

    project_name = models.CharField(max_length=100, verbose_name='项目名称')
    project_code = models.CharField(max_length=50, unique=True, verbose_name='项目唯一编码')
    description = models.TextField(blank=True, default='', verbose_name='项目描述')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    default_env_id = models.IntegerField(null=True, blank=True, verbose_name='默认关联环境ID')
    default_llm_config_id = models.IntegerField(null=True, blank=True, verbose_name='默认LLM模型ID')
    global_timeout = models.IntegerField(default=60, verbose_name='全局执行超时(秒)')
    global_retry = models.IntegerField(default=0, verbose_name='全局重试次数')
    default_priority = models.CharField(max_length=20, default='P2', verbose_name='资产默认优先级')
    create_user = models.CharField(max_length=100, blank=True, default='', verbose_name='创建人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'sys_project'
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_name


class ProjectMember(models.Model):
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('member', '普通成员'),
    )

    project = models.ForeignKey(SysProject, on_delete=models.CASCADE, related_name='members', verbose_name='项目')
    user_id = models.IntegerField(verbose_name='用户ID')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member', verbose_name='角色')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'sys_project_member'
        verbose_name = '项目成员'
        verbose_name_plural = verbose_name
        unique_together = ('project', 'user_id')
