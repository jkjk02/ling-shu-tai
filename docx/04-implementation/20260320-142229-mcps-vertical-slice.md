# MCPs纵向切片实现

- 阶段：04-implementation
- 提交时间：20260320-142229
- 责任角色：systems_implementer
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/03-plan/20260320-142228-plan-baseline-import.md

## 目标

1. 补通 `MCPs` 的列表、详情、新建、编辑、删除闭环。
2. 保证 `MCP` 的专属参数不会在编辑时被丢失。
3. 让后端 `MCP` 路由具备与 `Skills` 一致的冲突保护和只读保护。

## 核心内容

1. 前端改动：
   - 新增 [McpsPage.vue](/home/lst/ling-shu-tai/src/pages/McpsPage.vue)，实现列表、筛选、详情、弹窗表单和删除确认。
   - 复用 `Skills` 页交互模式，新增 `extraParamsText` 的 JSON 校验。
   - 支持 `modelName`、`temperature`、`maxTokens`、`topP`、`presencePenalty`、`frequencyPenalty` 和 `extraParams` 编辑。
2. 契约与类型改动：
   - 在 [types/resources.ts](/home/lst/ling-shu-tai/src/types/resources.ts) 中补充 `McpDraft` 与 MCP 专属参数。
   - 在 [contracts.ts](/home/lst/ling-shu-tai/src/api/contracts.ts) 中补充 `ApiMcpUpsert`、`mapMcpPayload()`。
   - 在 [resources.ts](/home/lst/ling-shu-tai/src/api/resources.ts) 中补充 `mcpsApi.get/create/update/remove`。
3. 后端改动：
   - 在 [mcps.py](/home/lst/ling-shu-tai/backend/app/routers/mcps.py) 中接入 `create_unique()`、`update_writable()`、`delete_writable()`。
   - 新增结构化错误码：`mcp_conflict`、`mcp_read_only`。
4. 协作说明：
   - 前端与文档由主代理完成。
   - 后端 `mcps.py` 的写保护逻辑由 worker `Singer` 负责并已回写到工作区。
5. 实际验证：
   - `npm run build` 通过。
   - 进程内 `MCP CRUD` 冒烟通过，覆盖列表、新建、详情、更新、删除、重复创建冲突、只读更新拒绝、只读删除拒绝。
   - 验证结束后 `backend/data/mcps.json` 已恢复原始内容。

## 风险与待确认项

1. `extra_params` 当前使用文本域编辑 JSON，体验可用但不够友好。
2. `MCPs` 闭环完成后，`Agents` 关联 `MCP` 的复合表单仍未补齐。
3. 本轮没有引入 HTTP 层自动测试和浏览器黑盒验证。

## 交接输出

1. 交付给评审阶段的结果：
   - 前端 `MCPs` 已达到与 `Skills` 类似的 CRUD 闭环水平
   - 后端写保护已收敛到统一资源服务能力之上
2. 交付给测试阶段的重点：
   - 构建是否通过
   - `extra_params` JSON 校验是否有效
   - `409/403/404` 行为是否符合预期

## 批准记录

- 评审人：implementation_reviewer
- 评审结论：approved
- 批准时间：20260320-142911
- 备注：本轮范围内通过，允许进入测试与阶段性交付。
