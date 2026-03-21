# 后端 API 自动化回归测试实施计划

- 阶段：03-plan
- 提交时间：20260320-172015
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/02-architecture/20260320-172015-backend-api-test-automation-architecture.md

## 目标

1. 把已批准架构方案拆解为可执行的实现顺序、验证方式和工作包边界。
2. 在不超过 4 个 worker 的前提下，给出清晰且不重叠的写集。

## 核心内容

### 开发顺序

1. 先改配置层
   - 在 `backend/app/config.py` 增加数据目录覆盖能力
   - 确认 managed / agents / workflows 路径都从覆盖后的数据根派生
2. 再补测试层
   - 创建 `backend/tests/`
   - 编写真实 HTTP 回归测试，封装服务生命周期与请求辅助
3. 最后补文档层
   - 更新 `README.md`
   - 在实现文档中记录命令与覆盖范围

### 验证方式

1. Python 语法与导入校验
   - `backend/.venv/bin/python -m py_compile backend/app/config.py backend/app/main.py`
2. 自动化测试主验证
   - `backend/.venv/bin/python -m unittest discover -s backend/tests`
3. 前端回归门
   - `npm run build`

### 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| worker-1 | 配置隔离与测试基础设施 | `backend/app/config.py`, `backend/tests/` | 已批准架构方案 | 数据目录覆盖能力、测试用例、服务启动与请求辅助 |
| worker-2 | 文档与命令入口说明 | `README.md` | 已批准架构方案 | 自动化测试运行说明、覆盖边界说明 |

### 工作包说明

1. `worker-1`
   - 输入：`docx/02-architecture/20260320-172015-backend-api-test-automation-architecture.md`
   - 输出：
     - `LINGSHU_DATA_DIR` 覆盖能力
     - 隔离样本目录构建
     - 覆盖 `health` / `skills` / `mcps` / `agents` / `workflows` / `dashboard` / `discovery` 的回归测试
   - 不可修改范围：
     - `src/`
     - 现有业务路由协议
2. `worker-2`
   - 输入：`docx/02-architecture/20260320-172015-backend-api-test-automation-architecture.md`
   - 输出：
     - README 中的测试命令与说明
   - 不可修改范围：
     - `backend/app/`
     - `backend/tests/`

### 完成定义

1. 存在 `backend/tests/` 自动化测试文件，且命令可稳定执行。
2. 测试过程中不污染正式 `backend/data`。
3. 自动化测试至少断言：
   - 健康检查成功
   - discovered skill / mcp 能被发现
   - managed 资源创建与读取成功
   - workflow 非法提交返回 `422 workflow_invalid`
4. README 已说明如何运行测试与当前未覆盖项。

## 风险与待确认项

1. 当前切片规模中等偏小，若实际实施时发现 `README.md` 改动极少，可由主代理顺手完成，不强制真的并行。
2. 若 `unittest discover` 启动时端口竞争明显，需要在测试中加入空闲端口选择逻辑。
3. 若发现 discovery 样本构造过重，应优先缩减样本而不是缩减关键接口覆盖。

## 交接输出

1. 允许开发阶段按本计划执行。
2. 实现记录必须写明测试场景、命令和文件所有权。
3. 评审阶段需重点检查：是否真的走了隔离目录，是否真的通过自动化入口验证。

## 批准记录

- 评审人：implementation_reviewer / 主代理
- 评审结论：approved
- 批准时间：20260320-172200
- 备注：计划批准，可进入开发阶段。
