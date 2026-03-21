# 架构方案导入

- 阶段：02-architecture
- 提交时间：20260320-142228
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/01-requirements/20260320-142228-requirements-baseline-import.md
  - doc/02-架构方案.md

## 目标

1. 将历史架构方案纳入 `docx/` 流程。
2. 明确本轮 `MCPs` 纵向切片实现时必须遵守的架构边界。

## 核心内容

1. 继承架构方案：`doc/02-架构方案.md` v0.1。
2. 本轮必须遵守的关键架构约束：
   - 前端负责页面、表单、列表和 API 接入，不承担持久化逻辑。
   - 后端负责 REST API、资源模型和文件系统持久化。
   - 统一资源基类字段继续沿用 `id/name/description/cli_tool/source_kind/source_path/is_writable/updated_at/created_at`。
   - `MCP` 资源字段继续沿用 `model_name/temperature/max_tokens/top_p/presence_penalty/frequency_penalty/extra_params`。
3. 本轮方案比较结论：
   - 方案 A：完全复用 `Skills` 页交互模式
   - 方案 B：为 `MCPs` 单独设计一套新页面模式
   - 推荐：方案 A
   - 原因：成本最低、用户学习成本最低、最符合当前“逐类资源补闭环”的交付策略。

## 风险与待确认项

1. `extra_params` 需要以结构化 JSON 方式编辑，前端必须防止非法 JSON 直接提交。
2. `top_p/presence_penalty/frequency_penalty` 作为 MCP 专属字段，不能在编辑时被静默丢失。

## 交接输出

1. 计划阶段按“页面交互 / API 契约 / 后端路由保护 / 验证”组织 `MCPs` 开发。
2. 实施阶段默认复用 `Skills` 的 UI 模式、错误提示模式和读写保护模式。

## 批准记录

- 评审人：implementation_reviewer
- 评审结论：approved
- 批准时间：20260320-142228
- 备注：批准基于历史架构方案导入，允许本轮在不改变架构边界的前提下推进 `MCPs`。
