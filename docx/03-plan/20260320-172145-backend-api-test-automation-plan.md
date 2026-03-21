# 后端 API 自动化回归测试实施计划

- 阶段：03-plan
- 提交时间：20260320-172145
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/02-architecture/20260320-171954-backend-api-test-automation-architecture.md

## 目标

1. 将后端 API 自动化回归测试切片拆分为可执行的实现工作包。
2. 明确写入边界、输入文档、交付物和验收点，确保开发阶段可并行而不抢文件。

## 核心内容

### 实施顺序

1. 先补齐测试隔离与服务拉起基础设施。
2. 再补齐 API 回归用例，覆盖核心成功链路和关键失败链路。
3. 最后补充 README 运行说明，并用自动化测试入口完成自验证。

### 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| worker-1 | 测试基础设施与隔离配置 | `backend/app/config.py`、`backend/tests/support.py`、`backend/tests/__init__.py` | 已批准架构方案 | 环境变量隔离能力、服务启动辅助模块 |
| worker-2 | API 回归用例与样本数据 | `backend/tests/test_api_regression.py`、`backend/tests/fixtures/**` | 已批准架构方案 | 资源 CRUD、只读保护、workflow 校验、dashboard/discovery 回归用例 |
| 主代理 | 文档与集成验证 | `README.md`、`docx/04-implementation/*`、后续评审/测试/交付文档 | 已批准架构方案 + worker 输出 | 运行说明、阶段文档、集成验证记录 |

### 工作包约束

1. `worker-1` 只负责基础设施，不编写业务接口断言。
2. `worker-2` 不修改 `backend/app/**` 业务代码；若发现无法在当前接口上落地测试，只能把缺口反馈给主代理。
3. 主代理负责整合两个 worker 输出，并处理 README 与阶段文档，不进入 worker 写集。
4. 并行数为 2，低于技能要求的 4 个上限。

### 约定接口

1. `worker-1` 需提供可复用测试辅助接口，至少包括：
   - 启动/停止临时后端服务
   - 构造隔离数据目录
   - 发送 JSON HTTP 请求并返回状态码与 JSON 结果
2. `worker-2` 基于上述辅助接口编写断言，不自行实现第二套服务管理逻辑。

### 验收点

1. 存在统一测试命令，可直接执行全部后端 API 回归测试。
2. 测试覆盖 requirements 中列出的最小资源范围。
3. 自动化测试执行后，默认 `backend/data` 内容不发生变化。
4. README 明确说明运行方法、覆盖边界和未覆盖范围。

## 风险与待确认项

1. 若 `worker-2` 在并行开发中需要额外测试辅助接口，主代理统一收敛到 `backend/tests/support.py`，禁止直接改 `worker-1` 写集之外的基础设施文件。
2. 如果配置隔离实现必须新增环境变量，需要确保 README 同步更新，避免后续误用默认数据目录。

## 交接输出

1. 开发阶段按本计划进入实现，默认启用 2 个 worker 并行。
2. `docx/04-implementation/` 需记录每个工作包的代码归属、集成方式和验证结果。
3. 若实现过程中发现写集耦合超预期，必须在实现记录中解释原因，不能静默打破边界。

## 完成定义

1. 拆分边界清晰。
2. 并行数不超过 4。
3. 每个 worker 都有独立写集。
4. 每个工作包都有可验证结果。

## 批准记录

- 评审人：solution_architect / 主代理
- 评审结论：approved
- 批准时间：20260320-172145
- 备注：按 2 个 worker 并行实施，主代理负责集成与文档闭环。
