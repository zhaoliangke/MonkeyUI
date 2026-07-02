from django.db import models


class KbCrawlerTask(models.Model):
    STATUS_CHOICES = (
        ('pending', '待执行'),
        ('running', '采集中'),
        ('completed', '已完成'),
        ('failed', '失败'),
        ('stopped', '已停止'),
    )

    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    task_name = models.CharField(max_length=200, verbose_name='任务名称')
    url = models.CharField(max_length=500, verbose_name='爬取URL')
    env_id = models.IntegerField(null=True, blank=True, verbose_name='环境ID')
    credential_id = models.IntegerField(null=True, blank=True, verbose_name='凭据ID')
    crawler_scope = models.TextField(blank=True, default='', verbose_name='爬取范围')
    filter_rule = models.TextField(blank=True, default='', verbose_name='过滤规则')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    result_msg = models.TextField(blank=True, default='', verbose_name='结果信息')
    element_count = models.IntegerField(default=0, verbose_name='采集元素数')
    step_count = models.IntegerField(default=0, verbose_name='生成步骤数')
    auto_asset_id = models.IntegerField(null=True, blank=True, verbose_name='自动生成资产ID')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    create_user = models.CharField(max_length=100, blank=True, default='', verbose_name='创建人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kb_crawler_task'
        verbose_name = '爬取任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.task_name
