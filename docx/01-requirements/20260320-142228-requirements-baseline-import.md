# 需求基线导入

- 阶段：01-requirements
- 提交时间：20260320-142228
- 责任角色：requirements_analyst
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/00-governance/20260320-142228-run-ledger.md
  - doc/01-需求基线.md

## 目标

1. 将历史已确认的需求基线正式纳入 `docx/` 流程。
2. 明确本轮继续推进时唯一有效的需求输入。

## 核心内容

1. 继承的需求基线版本：`doc/01-需求基线.md` v0.2，状态为“已确认”。
2. 本轮继续有效的关键需求：
   - 平台需覆盖 `Skills`、`MCPs`、`Agents`、`Workflows` 四类资源管理。
   - `MCPs` 至少支持列表、新建、编辑、删除、查看详情。
   - 编辑页至少支持 `name`、`cli_tool`、`model_name`、`temperature`、`max_tokens` 和结构化扩展参数。
   - 前后端通过 RESTful JSON 通信，错误响应需要统一结构。
3. 本轮范围收缩说明：
   - 本轮只实现 `MCPs` 纵向切片，不等于缩减需求基线。
   - 其余资源继续保留在后续阶段交付范围中。

## 风险与待确认项

1. 需求文档仍含早期 `apps/ling-shu-tai` 表述，但当前实际项目根目录以 `/home/lst/ling-shu-tai` 为准。
2. `Monaco` 与 `Workflow` 画布仍不在本轮实施范围内。

## 交接输出

1. 架构阶段继续沿用已确认的资源模型与前后端分层方案。
2. 本文档作为后续架构和计划阶段的唯一需求输入。

## 批准记录

- 评审人：implementation_reviewer
- 评审结论：approved
- 批准时间：20260320-142228
- 备注：批准基于历史已确认需求基线导入，不新增需求分歧。
