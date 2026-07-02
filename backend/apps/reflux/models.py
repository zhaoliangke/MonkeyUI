from django.db import models


class KbRefluxRecord(models.Model):
    REFLUX_TYPE_CHOICES = (
        ('light', '轻量数据(自动回流)'),
        ('structural', '结构性数据(需审核)'),
    )
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('ignored', '已忽略'),
        ('failed', '回流失败'),
    )

    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    asset_id = models.IntegerField(verbose_name='资产ID')
    run_record_id = models.IntegerField(null=True, blank=True, verbose_name='关联执行记录ID')
    reflux_type = models.CharField(max_length=20, choices=REFLUX_TYPE_CHOICES, default='light', verbose_name='回流类型')
    diff_content = models.TextField(blank=True, default='{}', verbose_name='差异内容(JSON)')
    new_script = models.TextField(blank=True, default='', verbose_name='新脚本')
    new_element_data = models.TextField(blank=True, default='{}', verbose_name='新元素数据(JSON)')
    new_step_data = models.TextField(blank=True, default='[]', verbose_name='新步骤数据(JSON)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='审核状态')
    audit_user = models.CharField(max_length=100, blank=True, default='', verbose_name='审核人')
    audit_time = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kb_reflux_record'
        verbose_name = '回流记录'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
