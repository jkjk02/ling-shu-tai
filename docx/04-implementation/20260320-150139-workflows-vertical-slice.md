# Workflows纵向切片实现

- 阶段：04-implementation
- 提交时间：20260320-150139
- 责任角色：systems_implementer
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/03-plan/20260320-150139-workflows-vertical-slice-plan.md

## 目标

1. 补通 `Workflows` 的列表、详情、新建、编辑、删除闭环。
2. 提供最小可用的节点拖拽、连线编辑、保存与加载能力。
3. 让前端可在真实联调下通过 `5173/api/workflows` 完成完整工作流 CRUD。

## 核心内容

1. 当前实现拆分：
   - 主代理：前端页面、类型契约、联调、文档归档
   - worker `Kant`：`backend/app/routers/workflows.py`
2. 当前已完成进展：
   - `Workflow` 类型与 DTO 已补充 `viewport`、`createdAt`
   - `workflowsApi` 已补充 `get/create/update/remove`
   - `WorkflowsPage.vue` 已重写为列表 + 元数据 + 画布 + 节点/连线编辑模式
   - 后端 `workflows.py` 已补充 `workflow_conflict`
   - `npm run build` 已通过
   - 真实 HTTP `Workflows CRUD` 已通过前端代理验证并清理测试数据

## 代码归属

| 责任方 | 文件 |
| --- | --- |
| 主代理 | `src/pages/WorkflowsPage.vue` |
| 主代理 | `src/api/contracts.ts` |
| 主代理 | `src/api/resources.ts` |
| 主代理 | `src/types/resources.ts` |
| 主代理 | `src/data/mock.ts` |
| 主代理 | `src/styles/main.css` |
| worker `Kant` | `backend/app/routers/workflows.py` |

## 预期验证

1. `npm run build`
2. 真实 HTTP 通过 `5173/api/workflows` 进行 CRUD 验证
3. 测试后恢复 `backend/data/workflows/workflows.json`

## 实际验证结果

1. `npm run build`：通过
2. 真实 HTTP `Workflows CRUD`：
   - `workflow create -> 201, id=http-workflow-smoke`
   - `workflow update -> 200`
   - `workflow get -> 200, nodes=2`
   - `workflow duplicate -> 409, code=workflow_conflict`
   - `workflow delete -> 200`
3. 验证路径：
   - `http://127.0.0.1:5173/api/workflows`
4. 临时测试记录已在验证结束后删除，没有污染 `backend/data/workflows/workflows.json`

## 风险与待确认项

1. 当前画布为最小可用实现，不等同于完整 Vue Flow 级体验。
2. 浏览器级拖拽与交互细节还需要手工补测记录。
3. 剩余主要缺口将集中到外部资源解析回写与 Monaco 编辑器。

## 交接输出

1. 交给评审阶段：
   - `Workflows` 是否已形成最小可用编排闭环
   - `workflow_conflict` 是否已落地
2. 交给测试阶段：
   - 构建结果
   - 真实 HTTP CRUD 结果
   - 测试数据恢复情况
3. 本阶段唯一上游输入文件：
   - `docx/03-plan/20260320-150139-workflows-vertical-slice-plan.md`

## 批准记录

- 评审人：implementation_reviewer
- 评审结论：approved
- 批准时间：20260320-152728
- 备注：实现范围、代码与文档一致，允许进入测试阶段。
