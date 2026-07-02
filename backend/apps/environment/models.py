from django.db import models


class KbEnv(models.Model):
    ENV_TYPE_CHOICES = (
        ('test', '测试'),
        ('staging', '预发'),
        ('production', '生产'),
    )

    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    env_name = models.CharField(max_length=100, verbose_name='环境名称')
    env_type = models.CharField(max_length=20, choices=ENV_TYPE_CHOICES, default='test', verbose_name='环境类型')
    base_url = models.CharField(max_length=500, verbose_name='基础URL')
    headers = models.TextField(blank=True, default='{}', verbose_name='请求头(JSON)')
    status = models.IntegerField(default=1, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'kb_env'
        verbose_name = '环境'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.env_name}({self.get_env_type_display()})'


class KbCredential(models.Model):
    env = models.ForeignKey(KbEnv, on_delete=models.CASCADE, related_name='credentials', verbose_name='环境')
    title = models.CharField(max_length=100, verbose_name='凭据标题')
    account = models.CharField(max_length=200, blank=True, default='', verbose_name='账号')
    password = models.TextField(blank=True, default='', verbose_name='密码(加密)')
    cookie = models.TextField(blank=True, default='', verbose_name='Cookie(加密)')
    token = models.TextField(blank=True, default='', verbose_name='Token(加密)')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kb_credential'
        verbose_name = '凭据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
