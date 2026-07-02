# Requirements Document

## Introduction

UI自动化智能知识库平台是一个企业级低代码UI自动化自愈测试平台，基于Python Django + Vue3前后端分离架构，实现站点资产自动爬取、零代码自然语言用例、LLM智能生成自动化脚本、在线引擎执行、执行数据回流迭代资产的完整闭环。

## Glossary

- **System/平台**: UI自动化智能知识库平台
- **项目**: 最高数据隔离维度，所有业务数据绑定项目ID
- **资产**: 知识库中的测试用例单元，包含步骤、脚本、元素等信息
- **回流**: 根据自动化执行结果反向更新资产步骤、脚本、元素的流程
- **LLM**: 大语言模型，用于AI生成自动化脚本
- **爬取**: 通过无头浏览器自动采集站点页面元素和结构信息
- **凭据**: 测试环境登录所需的账号、密码、Cookie、Token等认证信息

---

## Requirements

### Requirement 1: 多项目管理与数据隔离

**User Story:** AS 平台管理员, I want 创建和管理多个项目, so that 不同业务线、不同团队的数据完全隔离，互不干扰。

#### Acceptance Criteria

1. The system SHALL provide project CRUD operations including project name, unique code, description, and status management.
2. WHEN a project is set as default, the system SHALL ensure only one default project exists globally.
3. The system SHALL assign a unique project_id to every business data record across all modules.
4. WHEN a user switches projects via the global navigation, the system SHALL filter all data queries by the current project_id.
5. The system SHALL provide project member permission management with admin and member roles.
6. The system SHALL bind a default test environment and default LLM model to each project.
7. IF a request lacks a valid project_id in the context, the system SHALL reject the request with an authorization error.

---

### Requirement 2: LLM大模型配置与AI能力管理

**User Story:** AS 项目管理员, I want 配置和管理大模型参数与Prompt模板, so that AI能够根据不同的Prompt模板生成准确的自动化脚本。

#### Acceptance Criteria

1. The system SHALL support multiple LLM model types including public cloud and private deployment.
2. The system SHALL encrypt API keys using AES before storing them in the database.
3. WHEN a user saves an LLM configuration, the system SHALL provide a connectivity test endpoint that returns model availability status.
4. The system SHALL support configurable model parameters including API base URL, temperature, max tokens, and timeout.
5. The system SHALL provide rich text editing for Prompt templates supporting variable placeholders.
6. The system SHALL support four template types: natural language to script conversion, step correction, element failure repair, and assertion auto-generation.
7. The system SHALL log every AI call with input content, output script, duration, status, and error messages.
8. The system SHALL provide an online AI test panel where users input natural language steps and preview generated Python scripts in real time.

---

### Requirement 3: 站点爬取与资产采集

**User Story:** AS 测试工程师, I want 通过无头浏览器自动爬取站点页面元素, so that 能够快速生成初始测试资产，减少手工录入。

#### Acceptance Criteria

1. The system SHALL use Python Playwright headless browser for page loading and DOM parsing.
2. WHEN a crawl task is started, the system SHALL validate environment connectivity and credential validity before proceeding.
3. IF the target environment is production, the system SHALL reject the crawl request.
4. The system SHALL automatically filter advertisements, hidden elements, and redundant DOM nodes, retaining only interactive elements.
5. WHEN crawling completes, the system SHALL automatically create draft knowledge base assets with initial natural language steps.
6. The system SHALL provide real-time crawl progress, log streaming, and task pause/stop/resume controls.
7. The system SHALL support incremental crawling that identifies new, deprecated, and changed elements by comparing with historical data.
8. The system SHALL automatically store collected elements into the shared element library.

---

### Requirement 4: 知识库资产管理

**User Story:** AS 测试工程师, I want 管理知识库测试资产的生命周期, so that 所有测试用例有统一的标准化的存储和维护方式。

#### Acceptance Criteria

1. The system SHALL provide a three-level category tree navigation for asset organization.
2. The system SHALL support asset status management with states: draft, published, pending update, pending reflux review, and invalidated.
3. The system SHALL provide asset editing with six fixed panels: crawl configuration, basic info, natural language steps, automation parameters, script preview, and version comparison.
4. The system SHALL support batch operations on assets including archive, enable/disable, execute, migrate category, and re-crawl.
5. WHEN an asset step references an element, the system SHALL validate the element exists and is valid.
6. The system SHALL track asset versions with full change history for every modification.
7. The system SHALL associate each asset with a specific project, environment type, and execution engine.

---

### Requirement 5: NLP+LLM双引擎脚本生成

**User Story:** AS 测试工程师, I want 将自然语言步骤自动转化为Python自动化脚本, so that 不需要手写代码即可获得可执行的自动化测试脚本。

#### Acceptance Criteria

1. The system SHALL parse natural language steps using regex-based NLP to extract element names, action types, parameters, and assertion conditions.
2. WHEN NLP parsing succeeds for basic scenarios, the system SHALL generate a baseline script without calling LLM.
3. WHEN NLP parsing is incomplete or uncertain, the system SHALL invoke LLM for error correction, completion, and formatting.
4. The system SHALL generate standard executable Python scripts for Playwright, Selenium, and Appium engines.
5. The system SHALL render Prompt templates by replacing step, element, and parameter placeholders before LLM invocation.
6. The system SHALL save generated scripts with versioning, marking the latest as the active script.
7. The system SHALL allow manual editing of generated scripts before execution.

---

### Requirement 6: 多引擎自动化执行

**User Story:** AS 测试工程师, I want 在不同场景下执行自动化测试脚本, so that 可以灵活进行单条调试、批量回归和CI/CD集成测试。

#### Acceptance Criteria

1. The system SHALL support single execution, batch regression, scheduled tasks, and CI/CD pipeline triggers.
2. WHEN an execution is requested, the system SHALL validate asset status, script validity, environment, and credential availability.
3. The system SHALL dispatch execution tasks via multi-threaded asynchronous scheduling.
4. The system SHALL automatically match the execution engine (Playwright/Selenium/Appium) based on asset configuration.
5. The system SHALL capture execution logs, screenshots, failure recordings, exception stack traces, duration, and results.
6. WHEN execution completes, the system SHALL generate an execution report and trigger the reflux mechanism.
7. The system SHALL provide real-time execution progress, logs, and final results to the frontend.

---

### Requirement 7: 资产回流自愈引擎

**User Story:** AS 测试工程师, I want 执行结果自动反向迭代更新资产, so that 测试用例能够自动适应页面变更，减少人工维护成本。

#### Acceptance Criteria

1. WHEN an execution completes, the system SHALL automatically trigger the reflux mechanism.
2. The system SHALL perform text-based semantic comparison for natural language steps, element info, and assertion parameters.
3. The system SHALL perform AST-based comparison for Python scripts to identify logical changes ignoring whitespace differences.
4. The system SHALL auto-approve lightweight data reflux including execution pass rate, duration, and running status.
5. The system SHALL generate pending review records for structural data reflux including step changes, element failures, and script logic changes.
6. The system SHALL provide visual diff comparison in the reflux review center for step, element, script, and parameter differences.
7. The system SHALL support one-click merge, partial merge, ignore, and version rollback operations.
8. WHEN a reflux is approved, the system SHALL generate a new asset version and archive the old version.

---

### Requirement 8: 环境与凭据管理

**User Story:** AS 项目成员, I want 管理测试环境和认证凭据, so that 自动化脚本能够在正确的环境中以正确的身份执行。

#### Acceptance Criteria

1. The system SHALL support multiple environment types: test, staging, and production.
2. The system SHALL encrypt credential fields (password, cookie, token) using AES before storage.
3. WHEN credentials are displayed on the frontend, the system SHALL show masked values only.
4. The system SHALL authorize credentials for reuse across projects based on permission settings.
5. The system SHALL support credential types including account/password, cookie, and token.

---

### Requirement 9: 公共元素库管理

**User Story:** AS 测试工程师, I want 统一管理和维护页面元素定位信息, so that 元素的定位变更能自动同步到所有关联的测试脚本。

#### Acceptance Criteria

1. The system SHALL store elements with page name, element name, type, locator type, and locator value.
2. WHEN an element is marked as invalid, the system SHALL show all associated test cases that reference it.
3. The system SHALL support AI-based element locator repair for invalid elements.
4. The system SHALL batch update all scripts referencing a repaired element.

---

### Requirement 10: 系统权限与全局配置

**User Story:** AS 系统管理员, I want 管理系统用户、角色和全局配置, so that 平台安全和运营参数得到统一管控。

#### Acceptance Criteria

1. The system SHALL provide user management with role-based access control.
2. The system SHALL provide global configuration for execution engines, file storage paths, screenshot rules, and data masking.
3. The system SHALL log all user operations for audit trail purposes.
4. The system SHALL provide a data dashboard showing project asset statistics, crawl success rates, execution pass rates, and pending reflux counts.

---

## 原始需求文档

用户提供的完整架构设计文档已保存在 `.monkeycode/specs/ui-automation-knowledge-platform/original-requirements.md`。
