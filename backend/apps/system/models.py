from django.db import models


class SystemConfig(models.Model):
    config_key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    config_value = models.TextField(verbose_name='配置值')
    description = models.CharField(max_length=200, blank=True, default='', verbose_name='配置说明')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'sys_config'
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.config_key


class AuditLog(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='操作用户')
    action = models.CharField(max_length=100, verbose_name='操作类型')
    resource = models.CharField(max_length=200, blank=True, default='', verbose_name='资源路径')
    detail = models.TextField(blank=True, default='', verbose_name='操作详情')
    ip_address = models.CharField(max_length=50, blank=True, default='', verbose_name='IP地址')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    class Meta:
        db_table = 'sys_audit_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
