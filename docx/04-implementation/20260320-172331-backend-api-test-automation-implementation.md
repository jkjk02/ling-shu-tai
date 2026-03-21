# 后端 API 自动化回归测试实现记录

- 阶段：04-implementation
- 提交时间：20260320-172331
- 责任角色：systems_implementer
- 当前状态：done
- 评审状态：pending
- 输入依据：
  - docx/03-plan/20260320-172208-backend-api-test-automation-plan.md

## 目标

1. 落地隔离数据目录能力，确保自动化测试不会污染正式示例数据。
2. 新增可重复执行的后端 API 自动化回归测试入口。
3. 补充 README 运行说明与覆盖边界。

## 核心内容

1. 配置隔离实现
   - 在 `backend/app/config.py` 增加 `LINGSHU_DATA_DIR` 环境变量覆盖逻辑。
   - 后端在该变量存在时改用临时数据目录生成集合文件与 managed 目录，避免写入正式 `backend/data`。
2. 测试基座实现
   - 新增 `backend/tests/support.py`，负责：
     - 复制正式 JSON 数据到临时测试目录
     - 选择本地临时端口
     - 启动和停止真实 `uvicorn`
     - 通过 `urllib` 发起 JSON 请求
     - 在测试结束时校验正式 `backend/data` 未被改写
   - 新增 `backend/tests/fixtures/`，提供最小 discovered skill / MCP 样本，覆盖只读发现链路。
3. 用例实现
   - 新增 `backend/tests/test_api_regression.py`，覆盖 6 个测试：
     - `health`
     - `dashboard` / `discovery`
     - `skills` managed CRUD 与 discovered 只读
     - `mcps` managed CRUD 与 discovered 只读
     - `agents` CRUD
     - `workflows` round-trip 与 `422 workflow_invalid`
   - 首轮真实执行暴露了 `unittest discover` 下的导入边界问题，已修正为同目录导入 `support`。
4. 文档更新
   - 更新 `README.md`，补充测试命令、隔离策略、覆盖边界与未覆盖项。

## 代码归属

1. worker-1
   - `backend/app/config.py`
   - `backend/tests/support.py`
   - `backend/tests/test_api_regression.py`
   - `backend/tests/fixtures/`
2. 主代理
   - `README.md`
   - `docx/` 阶段文档集成
   - 导入边界修复与最终验证

## 验证方式

1. `backend/.venv/bin/python -m py_compile backend/app/config.py backend/tests/support.py backend/tests/test_api_regression.py`
2. `backend/.venv/bin/python -m unittest discover -s backend/tests`
3. `npm run build`

## 风险与待确认项

1. 自动化测试依赖本地回环网络与 `uvicorn` 子进程；在极端受限环境中仍可能需要额外权限。
2. 当前回归未覆盖浏览器层面的交互、拖拽、缩放与画布渲染。
3. 当前测试样本是最小 discovered 夹具，未来若 discovery 规则扩展，需要同步补充更多样本。

## 交接输出

1. 允许进入实现评审阶段。
2. 评审阶段应重点检查：
   - 是否真实 HTTP 而非伪造 service 调用
   - 是否验证了 discovered 只读保护
   - 是否证明正式 `backend/data` 未被污染
3. 测试阶段应以新增 `unittest` 命令作为最终验收入口。

## 批准记录

- 评审人：待实现评审
- 评审结论：pending
- 批准时间：
- 备注：实现已完成，等待 Stage 5 审批。
