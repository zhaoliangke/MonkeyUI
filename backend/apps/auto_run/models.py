from django.db import models


class KbRunRecord(models.Model):
    RUN_TYPE_CHOICES = (
        ('single', '单条执行'),
        ('batch', '批量回归'),
        ('schedule', '定时任务'),
        ('cicd', 'CI/CD触发'),
    )
    RESULT_CHOICES = (
        ('pass', '通过'),
        ('fail', '失败'),
        ('blocked', '阻塞'),
        ('running', '运行中'),
    )

    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    asset_id = models.IntegerField(verbose_name='资产ID')
    script_version = models.IntegerField(default=1, verbose_name='脚本版本号')
    run_type = models.CharField(max_length=20, choices=RUN_TYPE_CHOICES, default='single', verbose_name='执行类型')
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='running', verbose_name='执行结果')
    cost_time = models.FloatField(default=0, verbose_name='执行耗时(秒)')
    screenshot_path = models.TextField(blank=True, default='', verbose_name='截图路径')
    video_path = models.TextField(blank=True, default='', verbose_name='录屏路径')
    log_content = models.TextField(blank=True, default='', verbose_name='执行日志')
    fail_reason = models.TextField(blank=True, default='', verbose_name='失败原因')
    llm_model_used = models.CharField(max_length=100, blank=True, default='', verbose_name='使用的LLM模型')
    run_time = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')

    class Meta:
        db_table = 'kb_run_record'
        verbose_name = '执行记录'
        verbose_name_plural = verbose_name
        ordering = ['-run_time']
