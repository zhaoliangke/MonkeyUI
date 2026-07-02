from django.db import models


class KbCategory(models.Model):
    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    parent_id = models.IntegerField(null=True, blank=True, verbose_name='父级ID')
    name = models.CharField(max_length=100, verbose_name='分类名称')
    level = models.IntegerField(default=1, verbose_name='层级')
    sort = models.IntegerField(default=0, verbose_name='排序')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kb_category'
        verbose_name = '资产分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class KbAsset(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
        ('pending_update', '待更新'),
        ('pending_reflux', '待回流审核'),
        ('invalidated', '已失效'),
    )
    PRIORITY_CHOICES = (
        ('P0', 'P0'),
        ('P1', 'P1'),
        ('P2', 'P2'),
        ('P3', 'P3'),
    )
    ENGINE_CHOICES = (
        ('playwright', 'Playwright'),
        ('selenium', 'Selenium'),
        ('appium', 'Appium'),
    )

    project_id = models.IntegerField(db_index=True, verbose_name='项目ID')
    category_id = models.IntegerField(null=True, blank=True, verbose_name='分类ID')
    asset_name = models.CharField(max_length=200, verbose_name='资产名称')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='P2', verbose_name='优先级')
    terminal_type = models.CharField(max_length=20, default='web', verbose_name='终端类型')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
    pre_condition = models.TextField(blank=True, default='', verbose_name='前置条件')
    post_condition = models.TextField(blank=True, default='', verbose_name='后置条件')
    crawler_url = models.CharField(max_length=500, blank=True, default='', verbose_name='爬取URL')
    env_type = models.CharField(max_length=20, blank=True, default='', verbose_name='环境类型')
    crawler_rule = models.TextField(blank=True, default='', verbose_name='爬取规则')
    engine_type = models.CharField(max_length=20, choices=ENGINE_CHOICES, default='playwright', verbose_name='执行引擎')
    run_param = models.TextField(blank=True, default='', verbose_name='执行参数(JSON)')
    assert_config = models.TextField(blank=True, default='', verbose_name='断言配置(JSON)')
    version = models.IntegerField(default=1, verbose_name='当前版本号')
    create_user = models.CharField(max_length=100, blank=True, default='', verbose_name='创建人')
    update_user = models.CharField(max_length=100, blank=True, default='', verbose_name='更新人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'kb_asset'
        verbose_name = '知识库资产'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.asset_name


class KbAssetStep(models.Model):
    asset = models.ForeignKey(KbAsset, on_delete=models.CASCADE, related_name='steps', verbose_name='资产')
    sort_num = models.IntegerField(default=0, verbose_name='排序号')
    step_content = models.TextField(verbose_name='步骤内容(自然语言)')
    element_name = models.CharField(max_length=200, blank=True, default='', verbose_name='元素名称')
    action_type = models.CharField(max_length=50, verbose_name='操作类型')
    param = models.TextField(blank=True, default='', verbose_name='操作参数')
    assert_text = models.TextField(blank=True, default='', verbose_name='断言文本')
    is_valid = models.BooleanField(default=True, verbose_name='是否有效')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kb_asset_step'
        verbose_name = '资产步骤'
        verbose_name_plural = verbose_name
        ordering = ['sort_num']


class KbAssetScript(models.Model):
    asset = models.ForeignKey(KbAsset, on_delete=models.CASCADE, related_name='scripts', verbose_name='资产')
    engine_type = models.CharField(max_length=20, verbose_name='引擎类型')
    script_content = models.TextField(verbose_name='脚本内容')
    script_version = models.IntegerField(default=1, verbose_name='脚本版本号')
    is_last = models.BooleanField(default=True, verbose_name='是否最新版本')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kb_asset_script'
        verbose_name = '资产脚本'
        verbose_name_plural = verbose_name


class KbAssetVersion(models.Model):
    VERSION_TYPE_CHOICES = (
        ('create', '创建'),
        ('edit', '编辑'),
        ('ai_generate', 'AI生成'),
        ('reflux', '回流更新'),
        ('rollback', '回滚'),
    )

    asset = models.ForeignKey(KbAsset, on_delete=models.CASCADE, related_name='versions', verbose_name='资产')
    version_num = models.IntegerField(verbose_name='版本号')
    version_content = models.TextField(verbose_name='版本内容(JSON快照)')
    version_type = models.CharField(max_length=20, choices=VERSION_TYPE_CHOICES, default='edit', verbose_name='版本类型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kb_asset_version'
        verbose_name = '资产版本'
        verbose_name_plural = verbose_name
        ordering = ['-version_num']
