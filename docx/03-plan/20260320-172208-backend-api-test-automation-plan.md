# 后端 API 自动化回归测试实施计划

- 阶段：03-plan
- 提交时间：20260320-172208
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/02-architecture/20260320-172037-backend-api-test-automation-architecture.md

## 目标

1. 把架构方案拆成最小可交付实现包，确保本轮改动可独立验证。
2. 明确写入边界，避免 README、配置和测试实现互相抢文件。
3. 固定实施完成定义和验证顺序，降低返工概率。

## 核心内容

## 实施拆分

1. 工作包 A：后端配置隔离能力
   - 改动文件：`backend/app/config.py`
   - 目标：支持通过环境变量覆盖数据目录
   - 验收点：测试可把集合文件写入临时目录而非 `backend/data`
2. 工作包 B：自动化回归测试基座与用例
   - 改动文件：`backend/tests/test_api_regression.py`
   - 目标：落地真实 HTTP 测试、样本准备、服务生命周期控制和断言
   - 验收点：`backend/.venv/bin/python -m unittest discover -s backend/tests` 通过
3. 工作包 C：使用说明更新
   - 改动文件：`README.md`
   - 目标：记录测试命令、覆盖边界和隔离说明
   - 验收点：README 可独立指导执行本轮自动化测试

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| worker-1 | 后端配置与测试实现 | `backend/app/config.py`, `backend/tests/` | 已批准架构方案 | 可执行回归测试与隔离配置 |

说明：
- `README.md` 由主代理在集成阶段更新，避免与 `worker-1` 冲突。
- 本轮任务规模较小，不再额外拆分第二个代码 worker。

## 实施顺序

1. 先实现 `LINGSHU_DATA_DIR` 一类的数据目录覆盖能力。
2. 再实现测试基座：
   - 创建临时目录
   - 生成 discovered skill / MCP 样本
   - 选取可用端口
   - 启动 `uvicorn`
   - 发起 HTTP 断言
3. 最后补充 README 与实现文档，并执行验证。

## 验证计划

1. `backend/.venv/bin/python -m unittest discover -s backend/tests`
2. `backend/.venv/bin/python -m py_compile backend/app/config.py`
3. `npm run build`

## 完成定义

1. 自动化测试可稳定通过，且失败时能定位到具体接口或断言。
2. 仓库内正式 JSON 示例数据未被测试污染。
3. README 已同步本轮入口与边界。
4. 实现文档记录代码归属、验证方式和未覆盖项。

## 风险与待确认项

1. 若子进程启动超时，测试需要显式打印 stderr 或超时原因。
2. 若固定 discover 样本与真实扫描规则不一致，可能导致测试误报；实现时必须直接复用现有 discovery 规则。
3. `unittest` 发现规则默认较宽，测试文件命名应保持 `test_*.py`，避免执行混乱。

## 交接输出

1. 允许实施阶段按单 worker 代码实现 + 主代理文档集成的方式推进。
2. 评审阶段重点检查：是否真实 HTTP、是否隔离数据、是否覆盖关键失败链路。
3. 测试阶段重点检查：新测试命令本身是否成为最终验证手段。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-172230
- 备注：任务拆分边界清晰，本轮仅使用一个代码 worker 即可完成。
