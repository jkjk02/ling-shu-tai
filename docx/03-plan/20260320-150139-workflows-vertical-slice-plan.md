# Workflows纵向切片实施计划

- 阶段：03-plan
- 提交时间：20260320-150139
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/02-architecture/20260320-142228-architecture-baseline-import.md
  - docx/07-delivery/20260320-145551-agents-vertical-slice-delivery.md

## 目标

1. 为 `Workflows` 纵向切片提供唯一实施输入。
2. 在当前不引入 Vue Flow 的前提下，落地最小可用的工作流画布编辑能力。

## 核心内容

1. 本轮范围：
   - `Workflows` 列表、详情、新建、编辑、删除
   - 节点新增、删除、拖拽定位
   - 边新增、删除、标签编辑
   - 保存、加载、删除与重复创建冲突保护
2. 实现策略：
   - 前端使用原生绝对定位画布 + SVG 连线完成最小可用编排能力
   - 后端沿用现有 `WorkflowUpsert` 模型和 JSON 仓储
   - 先满足“可拖拽、可连线、可保存、可加载”，不在本轮接入 Vue Flow

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| worker-frontend | `src/pages/WorkflowsPage.vue`、`src/api/*`、`src/types/resources.ts`、`src/data/mock.ts` | 仅前端页面与契约 | 本文档 | 最小可用工作流编辑器 |
| worker-backend | `backend/app/routers/workflows.py` | 仅后端路由 | 本文档 | `workflow_conflict` 与写接口保护 |

## 完成定义

1. `Workflows` 页面具备真实 CRUD 闭环。
2. 页面支持新增节点、拖拽节点、编辑节点绑定 Agent。
3. 页面支持新增和删除边，并能保存与重新加载。
4. 创建重复 `Workflow` 时返回 `409 workflow_conflict`。
5. `npm run build` 通过。
6. 真实 HTTP 通过 `5173/api/workflows` 验证 CRUD 成功并清理测试数据。

## 风险与待确认项

1. 当前未接入 Vue Flow，画布交互为最小实现，复杂连线体验有限。
2. 浏览器级拖拽细节仍需手工验证补充。

## 交接输出

1. 开发阶段以本文件为唯一实施拆分依据。
2. 评审阶段重点核对“拖拽、连线、保存、加载”是否已形成最小可用闭环。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-150139
- 备注：批准进入 `Workflows` 纵向切片开发。
