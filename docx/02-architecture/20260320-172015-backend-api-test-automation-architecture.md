# 后端 API 自动化回归测试架构方案

- 阶段：02-architecture
- 提交时间：20260320-172015
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/01-requirements/20260320-171731-backend-api-test-automation-requirements.md

## 目标

1. 在不默认新增外部依赖的约束下，为 FastAPI 后端建立可维护、可隔离、可重复执行的 API 自动化回归架构。
2. 明确测试入口、隔离策略、目录结构和必要的代码改动点。

## 核心内容

### 需求基线摘要

1. 需求要求覆盖 `health`、`skills`、`mcps`、`agents`、`workflows`、`dashboard`、`discovery` 的核心 API 场景。
2. 测试必须使用隔离数据目录和隔离 discovery 样本目录。
3. 当前 `fastapi.testclient` 不可用，因为 venv 缺少 `httpx`。

### 候选方案对比

| 方案 | 描述 | 依赖成本 | 真实 HTTP 程度 | 隔离性 | 维护成本 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| 方案 A | 安装 `httpx` / `pytest`，使用 `TestClient` 做进程内接口测试 | 高，需要新增依赖并解决安装来源 | 中，经过 ASGI 栈但不经过真实端口与服务进程 | 高，可配合临时目录 | 中，写测试较舒适 | 本轮不推荐，受限于无外网依赖前提 |
| 方案 B | 使用 `unittest + subprocess + urllib.request`，启动真实 `uvicorn` 进程并通过本地端口访问 | 低，只依赖标准库和现有 venv | 高，覆盖真实 HTTP、真实服务启动和路由链路 | 高，可通过环境变量切换临时数据目录与发现目录 | 中，需要自行封装服务启动和请求辅助 | 推荐 |
| 方案 C | 编写 shell/curl 回归脚本，通过命令行断言 JSON | 低 | 高 | 中，隔离逻辑易分散在脚本中 | 高，断言脆弱且复用差 | 不推荐，长期可维护性差 |

### 推荐方案

1. 采用方案 B：`unittest + subprocess + urllib.request + uvicorn`。
2. 推荐理由：
   - 不依赖 `httpx`、`pytest` 或浏览器工具链，符合当前环境约束。
   - 能覆盖真实服务启动、异常处理、HTTP 状态码和 JSON 响应包装。
   - 可通过环境变量把 `Settings` 指向临时数据目录和临时 discovery 样本目录，满足“测试不污染正式数据”的核心要求。
   - 后续若未来引入 `pytest`，当前测试样本与隔离逻辑仍可复用，不会形成完全一次性资产。

### 模块边界

1. 配置层
   - 文件：`backend/app/config.py`
   - 责任：增加测试可用的 `LINGSHU_DATA_DIR` 覆盖能力，确保 repository 初始化可指向临时数据根
2. 测试层
   - 建议目录：`backend/tests/`
   - 责任：封装测试环境、服务生命周期、HTTP 请求辅助、断言场景
3. 文档层
   - 文件：`README.md`
   - 责任：公开测试命令、覆盖范围与已知边界

### 技术栈与入口建议

1. 测试框架：Python 标准库 `unittest`
2. HTTP 客户端：Python 标准库 `urllib.request`
3. 服务启动：`backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port <port>`
4. 命令入口建议：
   - 首选：`backend/.venv/bin/python -m unittest discover -s backend/tests`
   - 可选：后续再包装为脚本，但不是本轮必需

### 需要的代码改动点

1. `backend/app/config.py`
   - 新增 `LINGSHU_DATA_DIR` 支持
   - 确保 `collection_files`、managed 目录、agent/workflow 目录都从覆盖后的 `data_dir` 派生
2. `backend/tests/test_api_regression.py`
   - 建立临时目录
   - 写入最小 discovered skill / mcp 样本
   - 启动和关闭 `uvicorn`
   - 封装 JSON 请求与响应断言
3. `README.md`
   - 增加自动化测试命令
   - 说明当前覆盖后端 API，不覆盖浏览器交互

### 风险与权衡

1. 使用真实 `uvicorn` 进程比进程内 `TestClient` 更慢，但本轮规模小，代价可接受。
2. 端口监听需要处理启动等待和释放，测试文件应封装重试与清理，避免脆弱性。
3. 通过环境变量切换数据目录会引入新的配置路径，测试必须验证该路径确实生效。
4. 当前方案优先覆盖 API 稳定性，不解决前端状态流与拖拽画布回归。

## 风险与待确认项

1. 若本地已有占用端口，需要测试层自行选择空闲端口。
2. 若未来引入 CI，需额外确认 CI 机器上 `backend/.venv` 的准备方式。
3. 如果后续希望更细粒度断言内部异常，可能仍需补充更轻量的进程内单元测试。

## 交接输出

1. 允许计划阶段按“配置隔离 + API 回归测试文件 + 文档更新”拆分实现。
2. 要求实施阶段优先落地 `LINGSHU_DATA_DIR` 覆盖，再编写自动化测试。
3. 要求测试阶段用新增自动化入口自行验证，而非回退到纯手工 HTTP。

## 批准记录

- 评审人：implementation_reviewer / 主代理
- 评审结论：approved
- 批准时间：20260320-172120
- 备注：确认采用标准库真实 HTTP 路线，暂不引入新的测试依赖。
