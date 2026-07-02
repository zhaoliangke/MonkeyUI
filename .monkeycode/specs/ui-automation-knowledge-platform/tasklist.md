# 需求实施计划

- [x] 1. 搭建 Django 后端项目结构
  - 创建 Django 项目和 config/settings 目录（base.py, dev.py, prod.py）
  - 创建 requirements.txt 包含 Django, djangorestframework, django-cors-headers, psycopg2-binary, cryptography, playwright 等依赖
  - 创建 core/ 公共模块包（response.py, exception.py, middleware.py, security.py, logger.py）
  - 创建 engine/, service/, utils/ 目录结构
  - 注册所有 apps 到 INSTALLED_APPS

- [ ] 2. 实现核心公共基础设施
  - [ ] 2.1 实现统一 API 返回结构体 (core/response.py)
    - 定义 ApiResponse 类封装 code, message, data 字段
    - 实现 success() 和 error() 静态工厂方法
    - 参考 Req 1.7: 所有接口使用统一返回格式

  - [ ] 2.2 实现全局异常捕获 (core/exception.py)
    - 定义自定义异常类 (BusinessException, AuthException, NotFoundException)
    - 实现 Django DRF exception_handler 自定义处理
    - 确保异常返回统一 ApiResponse 格式

  - [ ] 2.3 实现项目隔离与权限中间件 (core/middleware.py)
    - 实现 ProjectIsolationMiddleware 从请求头 X-Project-ID 提取当前项目
    - 使用 threading.local 存储当前请求的 project_id
    - 参考 Req 1.4: 切换项目后全站数据自动隔离
    - 参考 Req 1.7: 无 project_id 时返回 403

  - [ ] 2.4 实现 AES 加密与数据脱敏 (core/security.py)
    - 实现 AES-256-CBC 加密/解密函数
    - 实现敏感字段脱敏展示函数（mask_string）
    - 参考 Req 2.2: API密钥 AES 加密入库
    - 参考 Req 8.2: 凭据字段加密存储
    - 参考 Req 8.3: 前端脱敏展示

  - [ ] 2.5 实现全局日志配置 (core/logger.py)
    - 配置 Django logging 输出到 logs/ 目录
    - 实现操作审计日志记录函数
    - 参考 Req 10.3: 所有用户操作记录审计日志

- [ ] 3. 实现数据模型 (所有 apps 的 models.py)
  - [ ] 3.1 实现项目管理模型 (apps/project/models.py)
    - SysProject 模型: project_name, project_code, description, status, default_env_id, create_user
    - ProjectMember 模型: project, user, role
    - 参考 Req 1.1~1.6: 项目 CRUD、默认项目、成员权限

  - [ ] 3.2 实现 LLM 引擎模型 (apps/llm_engine/models.py)
    - LlmGlobalConfig 模型: project_id, model_type, model_name, api_base, api_key(加密), timeout, temperature, max_tokens, is_enable, is_default
    - LlmPromptTemplate 模型: project_id, template_name, template_type, template_content, is_default, is_enable, sort
    - LlmGenerateLog 模型: project_id, asset_id, template_type, input_content, output_script, cost_time, status, error_msg
    - 参考 Req 2.1~2.7: LLM 配置、模板、日志全字段

  - [ ] 3.3 实现知识库模型 (apps/knowledge/models.py)
    - KbCategory 模型: project_id, parent_id, name, level, sort
    - KbAsset 模型: project_id, category_id, asset_name, priority, terminal_type, status, pre_condition, post_condition, crawler_url, env_type, crawler_rule, engine_type, run_param, assert_config, version
    - KbAssetStep 模型: asset_id, sort_num, step_content, element_name, action_type, param, assert_text, is_valid
    - KbAssetScript 模型: asset_id, engine_type, script_content, script_version, is_last
    - KbAssetVersion 模型: asset_id, version_num, version_content(JSON), version_type
    - 参考 Req 4.1~4.7: 资产分类树、六大编辑板块、版本管理

  - [ ] 3.4 实现爬取模块模型 (apps/crawler/models.py)
    - KbCrawlerTask 模型: project_id, task_name, url, env_id, credential_id, crawler_scope, filter_rule, status, result_msg, element_count, step_count, auto_asset_id, start_time, end_time, create_user
    - 参考 Req 3.1~3.8: 爬取任务全生命周期

  - [ ] 3.5 实现环境与凭据模型 (apps/environment/models.py)
    - KbEnv 模型: project_id, env_name, env_type, base_url, status
    - KbCredential 模型: env_id, title, account, password(加密), cookie(加密), token(加密), is_enable
    - 参考 Req 8.1~8.5: 多环境、凭据加密

  - [ ] 3.6 实现元素库模型 (apps/element_lib/models.py)
    - KbElement 模型: project_id, page_name, element_name, element_type, locator_type, locator_value, status, last_refresh_time
    - 参考 Req 9.1~9.4: 元素定位、失效标记、关联查询

  - [ ] 3.7 实现执行记录模型 (apps/auto_run/models.py)
    - KbRunRecord 模型: project_id, asset_id, script_version, run_type, result, cost_time, screenshot_path, video_path, log_content, fail_reason, llm_model_used, run_time
    - 参考 Req 6.1~6.7: 执行记录全字段

  - [ ] 3.8 实现回流记录模型 (apps/reflux/models.py)
    - KbRefluxRecord 模型: project_id, asset_id, run_record_id, reflux_type, diff_content(JSON), new_script, new_element_data, new_step_data, status, audit_user, audit_time
    - 参考 Req 7.1~7.8: 回流分级、差异对比、审核

  - [ ] 3.9 创建数据库迁移文件并执行 migrate
    - 运行 python manage.py makemigrations 生成所有迁移
    - 运行 python manage.py migrate 创建所有表
    - 验证所有表结构符合设计文档

- [ ] 4. 检查点 - 确保数据库迁移成功且所有模型可正常导入

- [ ] 5. 实现全局 API 路由与跨域配置
  - [ ] 5.1 配置 config/urls.py 主路由
    - 注册所有 app 的 urlpatterns
    - 配置 /api/ 前缀统一路由
    - 添加 Swagger/DRF browsable API 支持
  - [ ] 5.2 配置 config/settings/base.py
    - 配置 DATABASES (PostgreSQL/MySQL)
    - 配置 REST_FRAMEWORK 分页、认证、渲染
    - 配置 CORS 跨域允许
    - 配置 AES_SECRET_KEY

- [ ] 6. 实现项目管理模块完整功能
  - [ ] 6.1 实现项目 CRUD API (apps/project/views.py)
    - POST /api/project/list - 分页获取项目列表
    - POST /api/project/save - 新增/编辑项目
    - POST /api/project/set-default - 设置默认项目（唯一约束）
    - 参考 Req 1.1~1.2: 项目 CRUD 和默认项目唯一性

  - [ ] 6.2 实现项目权限管理 API
    - POST /api/project/permission/save - 配置项目成员和角色
    - 实现项目级权限装饰器 @project_permission_required
    - 参考 Req 1.5: 管理员/普通成员权限区分

  - [ ] 6.3 实现项目 Serializer (apps/project/serializers.py)
    - SysProjectSerializer 包含字段验证
    - ProjectMemberSerializer 包含角色验证

  - [ ] 6.4 实现项目业务服务层 (apps/project/service.py)
    - 默认项目切换逻辑（原子操作取消旧默认、设置新默认）
    - 项目成员角色校验逻辑

  - [ ] 6.5 实现项目 URLs (apps/project/urls.py)
    - 注册所有项目相关路由

- [ ] 7. 实现 LLM 大模型引擎模块
  - [ ] 7.1 实现 LLM 通用客户端 (apps/llm_engine/client.py)
    - 封装 OpenAI 兼容接口调用（requests/httpx）
    - 支持超时、重试、温度、max_tokens 参数
    - 返回结构化的生成结果
    - 参考 Req 2.1: 支持公有云 + 私有化部署

  - [ ] 7.2 实现 LLM 配置 CRUD API (apps/llm_engine/views.py 配置部分)
    - POST /api/llm/config/save - 保存模型配置（api_key AES 加密入库）
    - POST /api/llm/config/test - 模型连通性测试
    - 参考 Req 2.2~2.4: 加密存储、连通性测试

  - [ ] 7.3 实现 Prompt 模板管理 API
    - GET /api/llm/template/list - 模板列表
    - POST /api/llm/template/save - 保存模板（支持四种类型）
    - 参考 Req 2.5~2.6: 富文本编辑、四类模板

  - [ ] 7.4 实现 AI 脚本生成核心服务 (apps/llm_engine/service.py)
    - 实现模板渲染: 替换 {steps}, {elements}, {params} 占位符
    - 实现 prompt_builder: 根据 template_type 组装完整 Prompt
    - 实现 generate_script: 调用 client + 模板渲染 + 日志留存
    - 参考 Req 2.7: 全量 AI 调用日志
    - 参考 Req 5.1~5.7: NLP+LLM 双引擎

  - [ ] 7.5 实现 AI 脚本生成 API 端点
    - POST /api/llm/generate/script - AI生成Python脚本
    - 接收 asset_id, template_type 参数
    - 返回生成的 script_content
    - 参考 Req 2.8: AI 测试面板实时预览

  - [ ] 7.6 实现 AI 调用日志 API
    - GET /api/llm/log/list - 分页查询调用日志
    - 支持按 asset_id, status, 时间范围筛选
    - 参考 Req 2.7: 日志查询、复盘

  - [ ] 7.7 实现 LLM Serializers 和 URLs
    - LlmConfigSerializer, LlmTemplateSerializer, LlmLogSerializer
    - 注册 llm_engine urls

- [ ] 8. 实现知识库资产管理模块
  - [ ] 8.1 实现资产分类树 API (apps/knowledge/views.py 分类部分)
    - GET 分类列表（递归构建树结构）
    - POST 新增/编辑分类
    - 参考 Req 4.1: 三级分类树导航

  - [ ] 8.2 实现资产 CRUD API
    - GET /api/knowledge/list - 分页 + 多维度筛选 + 关键词搜索
    - POST /api/knowledge/save - 保存资产（基础信息 + 步骤 + 脚本 + 自动化配置）
    - GET /api/knowledge/detail/:id - 资产详情（含步骤、脚本、版本列表）
    - 参考 Req 4.2~4.4: 资产状态管理、批量操作

  - [ ] 8.3 实现资产批量操作 API
    - POST /api/knowledge/batch - 支持批量归档、启用/禁用、迁移分类
    - 参考 Req 4.4: 批量操作

  - [ ] 8.4 实现资产版本管理
    - 保存资产时自动生成 kb_asset_version 记录
    - GET /api/knowledge/version/diff - 两个版本的差异对比
    - 参考 Req 4.6: 版本全链路追溯
    - 参考 Req 7.7: 旧版本归档可回滚

  - [ ] 8.5 实现资产步骤管理
    - 资产保存时批量 upsert 步骤（删除旧 + 插入新）
    - 步骤关联元素校验：验证 element_name 是否存在于 kb_element
    - 参考 Req 4.5: 元素关联校验

  - [ ] 8.6 实现资产脚本管理
    - 保存脚本时自动标记 is_last = True，旧脚本 is_last = False
    - 支持脚本版本切换查询
    - 参考 Req 5.6: 脚本版本管理

  - [ ] 8.7 实现 Knowledge Serializers 和 URLs
    - KbCategorySerializer, KbAssetSerializer, KbAssetStepSerializer, KbAssetScriptSerializer, KbAssetVersionSerializer

- [ ] 9. 实现站点爬取模块
  - [ ] 9.1 实现爬取核心服务 (apps/crawler/service.py)
    - 基于 Playwright 无头浏览器实现页面加载
    - 智能过滤：排除 display:none, visibility:hidden, aria-hidden 元素
    - 提取可交互元素（button, a, input, select, textarea）及其定位信息
    - 自动生成初始自然语言步骤（click, fill, assert 类型）
    - 参考 Req 3.1~3.5: 无头爬取、智能过滤、自动生成

  - [ ] 9.2 实现爬取任务 API (apps/crawler/views.py)
    - POST /api/crawler/test-connect - 测试站点连通性（先检查环境类型是否可爬取）
    - POST /api/crawler/start - 启动爬取任务（异步执行）
    - GET /api/crawler/progress - 获取实时进度（返回 status, element_count, step_count）
    - POST /api/crawler/result/save - 将爬取结果生成草稿资产
    - 参考 Req 3.2: 校验环境和凭据
    - 参考 Req 3.3: 生产环境禁止爬取

  - [ ] 9.3 实现增量爬取能力
    - 对比历史元素数据，标记新增/废弃/变更
    - 支持仅更新变更部分到已有资产
    - 参考 Req 3.7: 增量爬取

  - [ ] 9.4 实现 Crawler Serializers 和 URLs
    - KbCrawlerTaskSerializer
    - 注册 crawler urls

- [ ] 10. 实现环境与凭据管理模块
  - [ ] 10.1 实现环境管理 API (apps/environment/views.py)
    - GET /api/env/list + POST /api/env/save
    - 支持测试/预发/生产三类环境
    - 参考 Req 8.1: 多环境管理

  - [ ] 10.2 实现凭据管理 API
    - GET /api/credential/list + POST /api/credential/save
    - 保存时对 password/cookie/token 进行 AES 加密
    - 查询时脱敏展示（仅显示前2后2字符）
    - 参考 Req 8.2~8.5: 加密存储、脱敏展示

  - [ ] 10.3 实现 Environment Serializers 和 URLs
    - KbEnvSerializer, KbCredentialSerializer
    - 注册 environment urls

- [ ] 11. 检查点 - 确保项目管理、LLM、知识库、爬取、环境核心 API 可正常响应

- [ ] 12. 实现公共元素库模块
  - [ ] 12.1 实现元素 CRUD API (apps/element_lib/views.py)
    - GET /api/element/list - 分页列表（按页面名称、状态筛选）
    - POST /api/element/save - 新增/编辑元素
    - 参考 Req 9.1: 元素统一管理

  - [ ] 12.2 实现元素关联查询 API
    - GET /api/element/related-cases - 查询引用该元素的所有资产（通过 kb_asset_step.element_name JOIN）
    - 参考 Req 9.2: 失效元素关联用例展示

  - [ ] 12.3 实现 AI 元素修复 API
    - POST /api/element/repair - 调用 LLM 修复失效元素定位
    - 修复后自动标记元素为有效状态
    - 参考 Req 9.3: AI智能修复元素定位

  - [ ] 12.4 实现 ElementLib Serializers 和 URLs
    - KbElementSerializer
    - 注册 element_lib urls

- [ ] 13. 实现自动化执行引擎
  - [ ] 13.1 实现执行引擎抽象基类 (engine/engine_base.py)
    - 定义 BaseEngine 抽象类: execute(script, env_config, credential) 方法签名
    - 定义引擎生命周期: setup → execute → teardown → collect_results
    - 参考 Req 6.4: 引擎自动匹配

  - [ ] 13.2 实现 Playwright 引擎 (engine/playwright_engine.py)
    - 继承 BaseEngine，实现 execute 方法
    - 使用 Playwright sync API 执行脚本
    - 自动截图、录屏、日志收集
    - 参考 Req 6.5: 执行数据全量采集

  - [ ] 13.3 实现 Selenium 引擎 (engine/selenium_engine.py)
    - 继承 BaseEngine，实现 execute 方法
    - 使用 Selenium WebDriver 执行脚本
    - 参考 Req 6.4: 多引擎适配

  - [ ] 13.4 实现引擎工厂 (engine/engine_factory.py)
    - EngineFactory.get_engine(engine_type) 返回对应引擎实例
    - 支持 playwright, selenium, appium 三种类型

  - [ ] 13.5 实现任务调度器 (service/task_scheduler.py)
    - 基于 Python threading 实现异步任务调度
    - 支持单条执行、批量并发执行
    - 参考 Req 6.3: 多线程异步调度

  - [ ] 13.6 实现执行记录 API (apps/auto_run/views.py)
    - POST /api/run/execute - 单条手动执行
    - POST /api/run/batch - 批量回归执行
    - GET /api/run/record/list - 执行记录分页列表
    - GET /api/run/record/detail/:id - 执行详情（含截图、日志、堆栈）
    - 参考 Req 6.1~6.7: 多场景触发、执行记录

  - [ ] 13.7 实现 AutoRun Serializers 和 URLs
    - KbRunRecordSerializer
    - 注册 auto_run urls

- [ ] 14. 实现资产回流自愈模块
  - [ ] 14.1 实现差异比对服务 (service/diff_compare.py)
    - 实现文本差异比对: 使用 difflib.SequenceMatcher 比对步骤内容
    - 实现脚本 AST 差异比对: 使用 Python ast 模块比对脚本逻辑变更
    - 忽略空白、注释、格式差异
    - 参考 Req 7.2~7.3: 文本比对 + AST语法树比对

  - [ ] 14.2 实现 NLP 解析服务 (service/nlp_parse.py)
    - 实现正则解析自然语言步骤: 提取 element_name, action_type, param, assert_text
    - 支持 click, fill, select, navigate, assert_visible, assert_text 等动作类型
    - 参考 Req 5.1: NLP规则兜底解析

  - [ ] 14.3 实现脚本组装服务 (service/script_build.py)
    - 根据解析结果 + 引擎类型组装标准 Python 脚本
    - 生成 Playwright/Selenium 格式脚本代码
    - 参考 Req 5.3: 多引擎脚本生成

  - [ ] 14.4 实现回流记录 API (apps/reflux/views.py)
    - GET /api/reflux/list - 回流记录列表（按状态分类）
    - GET /api/reflux/detail/:id - 回流详情（含 diff_content 差异对比）
    - POST /api/reflux/audit - 审核操作（merge/pass/ignore）
    - POST /api/reflux/rollback/:id - 版本回滚
    - 参考 Req 7.4~7.8: 分级回流、人工审核、版本回滚

  - [ ] 14.5 实现回流核心服务 (apps/reflux/service.py)
    - 实现 auto_reflux: 执行完成后自动调用，轻量数据直接更新
    - 实现 structural_reflux: 结构性变更生成待审核记录
    - 实现 apply_reflux: 审核通过后应用变更（更新资产、生成新版本）
    - 参考 Req 7.4~7.5: 分级回流处理

  - [ ] 14.6 实现 Reflux Serializers 和 URLs
    - KbRefluxRecordSerializer
    - 注册 reflux urls

- [ ] 15. 实现系统权限模块
  - [ ] 15.1 实现用户管理 API (apps/system/views.py 用户部分)
    - GET /api/system/user/list + POST /api/system/user/save
    - 用户密码哈希存储
    - 参考 Req 10.1: 用户管理

  - [ ] 15.2 实现角色管理 API
    - GET /api/system/role/list + POST /api/system/role/save
    - 基于角色的权限控制（RBAC）
    - 参考 Req 10.1: 角色权限控制

  - [ ] 15.3 实现系统配置 API
    - GET /api/system/setting/get + POST /api/system/setting/save
    - 全局执行引擎配置、文件路径、截图录屏规则、数据脱敏开关
    - 参考 Req 10.2: 全局配置

  - [ ] 15.4 实现操作审计日志 API
    - GET /api/system/log/list - 分页查询操作日志
    - 中间件自动记录请求日志（参考 core/middleware.py）
    - 参考 Req 10.3: 操作日志全局追溯

  - [ ] 15.5 实现 System Serializers 和 URLs
    - UserSerializer, RoleSerializer, SystemConfigSerializer, AuditLogSerializer
    - 注册 system urls

- [ ] 16. 检查点 - 确保所有后端 API 可正常响应并返回统一格式

- [ ] 17. 搭建 Vue3 前端项目结构
  - [ ] 17.1 使用 Vite 创建 Vue3 项目
    - 初始化 package.json，安装 vue3, vue-router, pinia, axios, element-plus 依赖
    - 创建 src/ 目录结构（router, store, api, views, components, utils）
    - 配置 vite.config.js（含代理、allowedHosts）

  - [ ] 17.2 实现请求封装 (src/utils/request.js)
    - 封装 axios 实例，配置 baseURL, 超时, 拦截器
    - 请求拦截器自动注入 X-Project-ID 头
    - 响应拦截器统一错误处理

  - [ ] 17.3 实现全局路由 (src/router/index.js)
    - 配置所有页面路由（dashboard, project, llm, knowledge, crawler, env, elementLib, autoRun, reflux, system）
    - 实现路由守卫权限校验

  - [ ] 17.4 实现全局状态管理 (src/store/)
    - project.js: 当前项目ID、项目列表
    - llm.js: 当前项目LLM配置
    - user.js: 当前用户信息和权限

- [ ] 18. 实现前端 API 接口层
  - [ ] 18.1 实现所有 API 模块 (src/api/)
    - project.js: 项目列表、保存、设置默认、权限
    - llm.js: LLM配置、模板、脚本生成、调用日志
    - knowledge.js: 资产列表、详情、保存、批量操作、版本对比
    - crawler.js: 爬取任务、连通测试、进度、结果保存
    - env.js: 环境与凭据管理
    - element.js: 元素库 CRUD、关联查询、AI修复
    - run.js: 执行、批量、记录
    - reflux.js: 回流列表、审核、回滚
    - system.js: 用户、角色、配置、日志

- [ ] 19. 实现前端核心页面
  - [ ] 19.1 实现 Dashboard 页面 (src/views/dashboard/index.vue)
    - 数据看板：资产总数、有效/失效统计、爬取成功率、执行通过率、待审核回流数
    - 快捷操作入口
    - 参考 Req 1: 全局工作台

  - [ ] 19.2 实现项目管理页面 (src/views/project/)
    - list.vue: 项目列表（增删改查、默认设置、状态切换）
    - config.vue: 项目配置（绑定环境、LLM模型、超时、重试）
    - 参考 Req 1.1~1.6

  - [ ] 19.3 实现 LLM 配置页面 (src/views/llm/)
    - setting.vue: 模型配置表单 + 连通性测试
    - prompt.vue: Prompt模板富文本编辑 + 变量占位
    - test.vue: AI测试面板（输入步骤 → 选择模板 → 生成预览）
    - log.vue: AI调用日志分页展示
    - 参考 Req 2.1~2.8

  - [ ] 19.4 实现知识库资产页面 (src/views/knowledge/)
    - list.vue: 左侧分类树 + 资产筛选 + 批量操作
    - edit.vue: 六大板块编辑页（爬取配置、基础信息、步骤编辑、自动化配置、脚本预览、版本对比）
    - 参考 Req 4.1~4.7

  - [ ] 19.5 实现爬取管理页面 (src/views/crawler/)
    - taskList.vue: 爬取任务列表 + 新增爬取
    - taskDetail.vue: 实时进度 + 日志 + 结果预览
    - 参考 Req 3.1~3.8

  - [ ] 19.6 实现环境凭据页面 (src/views/env/)
    - envList.vue: 环境 CRUD
    - credential.vue: 凭据管理（加密字段脱敏展示）
    - 参考 Req 8.1~8.5

  - [ ] 19.7 实现元素库页面 (src/views/elementLib/list.vue)
    - 元素列表 + 筛选 + AI修复入口
    - 关联用例弹窗
    - 参考 Req 9.1~9.4

  - [ ] 19.8 实现执行记录页面 (src/views/autoRun/)
    - record.vue: 执行记录列表 + 详情弹窗（日志、截图、录屏）
    - batchTask.vue: 批量任务管理
    - 参考 Req 6.1~6.7

  - [ ] 19.9 实现回流中心页面 (src/views/reflux/center.vue)
    - 待审核/已完成/已忽略分类Tab
    - 差异对比可视化 + 审核操作按钮
    - 参考 Req 7.1~7.8

  - [ ] 19.10 实现系统管理页面 (src/views/system/)
    - user.vue, role.vue, setting.vue
    - 参考 Req 10.1~10.4

- [ ] 20. 实现前端全局复用组件
  - [ ] 20.1 实现项目切换组件 (components/projectConfig/)
    - 顶部导航常驻项目下拉切换
    - 切换后刷新全站数据
    - 参考 Req 1.4

  - [ ] 20.2 实现步骤编辑器组件 (components/stepEditor/)
    - 支持拖拽排序、增删改自然语言步骤
    - 步骤关联元素选择器
    - 参考 Req 4.3: 步骤精细化维护

  - [ ] 20.3 实现脚本预览组件 (components/scriptPreview/)
    - Python 代码高亮展示（使用 highlight.js）
    - 支持编辑和版本切换
    - 参考 Req 5.7: 手动修改脚本

  - [ ] 20.4 实现版本对比组件 (components/versionCompare/)
    - 左右分栏 diff 对比展示
    - 支持步骤、元素、脚本三类对比

- [ ] 21. 最终检查点 - 启动前后端验证完整流程
  - 启动 Django 后端服务
  - 启动 Vite 前端开发服务器
  - 验证项目创建 → LLM配置 → 资产编辑 → AI生成脚本 → 执行 → 回流 完整闭环
