# Agents纵向切片实现

- 阶段：04-implementation
- 提交时间：20260320-144522
- 责任角色：systems_implementer
- 当前状态：done
- 评审状态：pending
- 输入依据：
  - docx/03-plan/20260320-144522-agents-vertical-slice-plan.md

## 目标

1. 补通 `Agents` 的列表、详情、新建、编辑、删除闭环。
2. 打通 Skill 分配、MCP 关联、`tool_scope` 多选和 `System Prompt` 编辑。
3. 让前端在真实联调下可直接消费 `Skills`、`MCPs`、`Agents` 三类资源。

## 核心内容

1. 当前实现拆分：
   - 主代理：前端页面、类型契约、联调、文档归档
   - worker `Nash`：`backend/app/routers/agents.py`
2. 当前已完成进展：
   - `Agent` 类型与 DTO 已补充 `description`、`cliTool`、`createdAt`
   - `agentsApi` 已补充 `get/create/update/remove`
   - `AgentsPage.vue` 已重写为列表 + 详情 + 表单对话框模式
   - 后端 `agents.py` 已补充 `agent_conflict`
   - `npm run build` 已通过
   - 真实 HTTP `Agents CRUD` 已通过前端代理验证并清理测试数据

## 代码归属

| 责任方 | 文件 |
| --- | --- |
| 主代理 | `src/pages/AgentsPage.vue` |
| 主代理 | `src/api/contracts.ts` |
| 主代理 | `src/api/resources.ts` |
| 主代理 | `src/types/resources.ts` |
| 主代理 | `src/data/mock.ts` |
| worker `Nash` | `backend/app/routers/agents.py` |

## 预期验证

1. `npm run build`
2. 真实 HTTP 通过 `5173/api/agents` 进行 CRUD 验证
3. 测试后恢复 `backend/data/agents/agents.json`

## 实际验证结果

1. `npm run build`：通过
2. 真实 HTTP `Agents CRUD`：
   - `agent create -> 201, id=http-agent-smoke`
   - `agent update -> 200`
   - `agent get -> 200`
   - `agent duplicate -> 409, code=agent_conflict`
   - `agent delete -> 200`
3. 验证路径：
   - `http://127.0.0.1:5173/api/agents`
4. 临时测试记录已在验证结束后删除，没有污染 `backend/data/agents/agents.json`

## 风险与待确认项

1. 本轮暂不扩展后端引用一致性校验，只保证联调闭环。
2. `Agents` 完成后，剩余重点将集中到 `Workflows` 与外部资源回写。

## 交接输出

1. 交给评审阶段：
   - `Agents` 是否真正达到需求基线中的复合表单能力
   - `agent_conflict` 是否已落地
2. 交给测试阶段：
   - 构建结果
   - 真实 HTTP CRUD 结果
   - 测试数据恢复情况
3. 本阶段唯一上游输入文件：
   - `docx/03-plan/20260320-144522-agents-vertical-slice-plan.md`

## 批准记录

- 评审人：
- 评审结论：
- 批准时间：
- 备注：
