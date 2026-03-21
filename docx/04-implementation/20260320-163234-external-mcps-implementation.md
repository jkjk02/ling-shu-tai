# 外部MCP发现实现记录

- 阶段：04-implementation
- 提交时间：20260320-163234
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/03-plan/20260320-163234-external-mcps-plan.md
  - docx/00-governance/20260320-162533-external-mcps-run-ledger.md

## 目标

1. 按计划补齐 `cludea` / `opencode` 的外部 MCP 发现与详情读取能力。
2. 不破坏既有 managed MCP 行为和其它资源 CRUD。

## 核心内容

1. 实现文件：
   - `backend/app/services/discovery.py`
   - `backend/app/routers/mcps.py`
   - `backend/app/routers/dashboard.py`
   - `src/pages/McpsPage.vue`
   - `README.md`
2. 主要实现点：
   - 在 `discovery.py` 中新增 discovered MCP 聚合、详情查询、计数与 JSON 最佳努力解析。
   - 将外部 MCP 统一映射为 `source_kind=discovered`、`is_writable=false`。
   - 在 `mcps.py` 中复用 Skills 的模式，补齐 discovered MCP 列表、详情、创建冲突检查和只读拒绝。
   - 在 `dashboard.py` 中将 MCP 统计从 managed-only 调整为 managed + discovered 聚合。
   - 在 `McpsPage.vue` 中补充来源列与页面描述，使 discovered MCP 与 managed MCP 可区分。
   - 在 `README.md` 中同步当前实现范围。
3. 本轮未修改内容：
   - 未实现外部 MCP 回写。
   - 未改动 `Skills` / `Agents` / `Workflows` 的交互结构。
   - 未建立自动化测试框架。
4. 自检结果：
   - `backend/.venv/bin/python -m py_compile ...` 通过。
   - `npm run build` 通过。

## 风险与待确认项

1. JSON 最佳努力解析对真实第三方 MCP 方言的兼容性仍需更多样本验证。
2. discovered MCP 进入 MCP 列表后，Agent 表单也会读取到这些 MCP；当前未做额外过滤，默认允许引用只读 MCP。
3. 当前目录不是 Git 仓库，无法提供提交哈希作为实现锚点。

## 交接输出

1. 评审阶段应重点检查：
   - MCP 路由是否已聚合 discovered MCP
   - Dashboard MCP 统计是否计入 discovered MCP
   - discovered MCP 的只读语义是否未回归
2. 测试阶段应使用临时目录覆盖：
   - `LINGSHU_CLUDEA_ROOT`
   - `LINGSHU_OPENCODE_ROOT`

## 批准记录

- 评审人：implementation_reviewer / 主代理
- 评审结论：approved
- 批准时间：20260320-163234
- 备注：`05-review` 已确认实现边界符合计划，允许进入测试并交付。
