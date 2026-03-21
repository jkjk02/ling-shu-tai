# Agents纵向切片实施计划

- 阶段：03-plan
- 提交时间：20260320-144522
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/02-architecture/20260320-142228-architecture-baseline-import.md
  - docx/07-delivery/20260320-142911-mcps-vertical-slice-delivery.md

## 目标

1. 为 `Agents` 纵向切片提供唯一实施输入。
2. 在不改变整体架构的前提下，把 `Agents` 从展示卡片页推进为真实 CRUD 闭环。

## 核心内容

1. 本轮范围：
   - `Agents` 列表、详情、新建、编辑、删除
   - `System Prompt` 编辑
   - Skill 多选分配
   - MCP 关联选择
   - `tool_scope` 多选
   - 后端创建冲突保护
2. 沿用策略：
   - 复用 `Skills` / `MCPs` 已验证的“列表 + 详情 + 对话框表单”页面模式
   - 复用 `docx/` 阶段化交付流程

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| worker-frontend | `src/pages/AgentsPage.vue`、`src/api/*`、`src/types/resources.ts`、`src/data/mock.ts` | 仅前端页面与契约 | 本文档 | `Agents` 可用页面与 DTO |
| worker-backend | `backend/app/routers/agents.py` | 仅后端路由 | 本文档 | `Agent` 冲突保护与结构化错误码 |

## 完成定义

1. `Agents` 页面具备真实 CRUD 闭环。
2. 页面可加载 `Skills` 和 `MCPs` 作为关联选项。
3. 创建重复 `Agent` 时返回 `409 agent_conflict`。
4. `npm run build` 通过。
5. 真实 HTTP 联调下 `Agents` CRUD 可用并清理测试数据。

## 风险与待确认项

1. 当前后端仍未对 `skill_ids` 和 `mcp_id` 做引用一致性校验，本轮先保证闭环可用。
2. 浏览器黑盒验证依赖当前已启动的本地前后端服务。

## 交接输出

1. 开发阶段以本文件为唯一实施拆分依据。
2. 评审阶段重点核对 `Agents` 是否真正补齐了需求基线中的复合表单能力。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-144522
- 备注：批准进入 `Agents` 纵向切片开发。
