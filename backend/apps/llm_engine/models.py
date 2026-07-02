from django.db import models


class LlmGlobalConfig(models.Model):
    MODEL_TYPE_CHOICES = (
        ('public', '公有云'),
        ('private', '私有化本地'),
    )

    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    model_type = models.CharField(max_length=20, choices=MODEL_TYPE_CHOICES, default='public', verbose_name='模型类型')
    model_name = models.CharField(max_length=100, verbose_name='模型名称')
    api_base = models.CharField(max_length=500, verbose_name='模型地址')
    api_key = models.TextField(verbose_name='加密密钥')
    timeout = models.IntegerField(default=60, verbose_name='超时时间(秒)')
    temperature = models.FloatField(default=0.7, verbose_name='温度')
    max_tokens = models.IntegerField(default=4096, verbose_name='最大Token')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'llm_global_config'
        verbose_name = 'LLM模型配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.model_name}({self.get_model_type_display()})'


class LlmPromptTemplate(models.Model):
    TEMPLATE_TYPE_CHOICES = (
        ('script_gen', '自然语言转脚本'),
        ('step_correct', '步骤纠错'),
        ('element_fix', '元素失效修复'),
        ('assert_gen', '断言自动生成'),
    )

    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    template_name = models.CharField(max_length=100, verbose_name='模板名称')
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES, verbose_name='模板类型')
    template_content = models.TextField(verbose_name='模板文本')
    is_default = models.BooleanField(default=False, verbose_name='默认模板')
    is_enable = models.BooleanField(default=True, verbose_name='是否启用')
    sort = models.IntegerField(default=0, verbose_name='排序')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'llm_prompt_template'
        verbose_name = 'Prompt模板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.template_name


class LlmGenerateLog(models.Model):
    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    asset_id = models.IntegerField(null=True, blank=True, verbose_name='资产ID')
    template_type = models.CharField(max_length=50, verbose_name='模板类型')
    input_content = models.TextField(verbose_name='入参文本')
    output_script = models.TextField(blank=True, default='', verbose_name='生成脚本')
    cost_time = models.FloatField(default=0, verbose_name='耗时(秒)')
    status = models.CharField(max_length=20, default='success', verbose_name='状态')
    error_msg = models.TextField(blank=True, default='', verbose_name='错误信息')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'llm_generate_log'
        verbose_name = 'AI调用日志'
        verbose_name_plural = verbose_name
