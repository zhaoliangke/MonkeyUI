from django.db import models


class KbElement(models.Model):
    STATUS_CHOICES = (
        ('valid', '有效'),
        ('invalid', '失效'),
    )

    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    page_name = models.CharField(max_length=200, verbose_name='页面名称')
    element_name = models.CharField(max_length=200, verbose_name='元素名称')
    element_type = models.CharField(max_length=50, verbose_name='元素类型')
    locator_type = models.CharField(max_length=50, verbose_name='定位器类型')
    locator_value = models.CharField(max_length=500, verbose_name='定位器值')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='valid', verbose_name='状态')
    last_refresh_time = models.DateTimeField(null=True, blank=True, verbose_name='最后刷新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'kb_element'
        verbose_name = '公共元素'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.page_name} - {self.element_name}'
