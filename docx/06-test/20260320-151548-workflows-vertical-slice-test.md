# Workflows纵向切片测试

- 阶段：06-test
- 提交时间：20260320-151548
- 责任角色：tester
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/05-review/20260320-151548-workflows-vertical-slice-review.md
  - docx/04-implementation/20260320-150139-workflows-vertical-slice.md

## 目标

1. 验证 `Workflows` 纵向切片是否达到本轮最小可交付标准。
2. 记录测试范围、执行结果、缺陷结论、剩余风险和是否允许进入交付。

## 核心内容

### 上游输入版本

1. 实施计划版本：`docx/03-plan/20260320-150139-workflows-vertical-slice-plan.md`
2. 实现记录版本：`docx/04-implementation/20260320-150139-workflows-vertical-slice.md`
3. 评审版本：`docx/05-review/20260320-151548-workflows-vertical-slice-review.md`

### 测试范围

1. 前端正式构建
2. `Workflows` 真实 HTTP CRUD 联调
3. `workflow_conflict` 冲突保护
4. 测试数据清理结果

### 测试结论

- 轮次：1
- 场景：`Workflows` 纵向切片真实联调验证
- 结果：passed

### 执行结果

1. `npm run build` 通过。
2. 真实 HTTP 通过 `http://127.0.0.1:5173/api/workflows` 验证通过：
   - `before list -> 200, total=1, baseline=draft-delivery-workflow`
   - `create -> 201, id=http-workflow-smoke`
   - `update -> 200, nodes=3`
   - `get -> 200, nodes=3`
   - `duplicate -> 409, code=workflow_conflict`
   - `delete -> 200, deleted=true`
   - `after list -> 200, total=1, baseline=draft-delivery-workflow`
3. `backend/data/workflows/workflows.json` 已回到基线状态，没有保留临时 `Workflow` 数据。

### 缺陷列表

1. 本轮测试范围内未发现阻塞性代码缺陷。
2. 已发现并完成闭环的问题：
   - 初次联调时，提权启动的 Vite dev server 无法访问沙箱内启动的后端，先后出现 `EPERM` 与 `ECONNREFUSED`
   - 处理方式：将前端与后端进程放到同一权限层后重新执行联调
   - 复测结果：通过，`/api/workflows` CRUD 与 `workflow_conflict` 均生效

### 重试轮次

1. 重试轮次：1
2. 重试原因：测试环境权限隔离导致代理联调失败，不属于代码缺陷
3. 当前状态：已闭环，不需要继续重试

## 错误日志

~~~text
初次启动 Vite dev server 失败：
Error: listen EPERM: operation not permitted 127.0.0.1:5173

初次联调代理失败：
Error: connect ECONNREFUSED 127.0.0.1:8000

修正权限层并复测后结果：
create -> 201, id=http-workflow-smoke
update -> 200, nodes=3
get -> 200, nodes=3
duplicate -> 409, code=workflow_conflict
delete -> 200, deleted=true
~~~

## 风险与待确认项

1. 当前测试未覆盖浏览器级手工拖拽与复杂交互细节。
2. 当前画布能力为最小实现，不等同于完整 Vue Flow 体验。
3. 当前测试未覆盖后端对 `agent_id` 的引用一致性校验。
4. 当前测试仅覆盖构建与真实 HTTP 联调，尚未覆盖更完整的端到端自动化回归。

## 是否达到交付条件

1. 就本轮 `Workflows` 纵向切片而言：达到进入交付阶段的条件。
2. 就整项目最终目标而言：四类核心资源已具备可视化 CRUD 与最小工作流编排能力，但 `Monaco`、真实外部文件格式解析与自动化测试仍未补齐。

## 交接输出

1. 允许进入本轮 `Workflows` 阶段性交付。
2. 交付摘要需明确：
   - `Workflows` 已形成真实 CRUD 与最小编排闭环
   - 本轮环境问题已闭环
   - 整项目仍存在增强项与非阻塞限制

## 批准记录

- 评审人：tester
- 评审结论：approved
- 批准时间：20260320-152728
- 备注：本轮测试范围内通过，建议进入 `Workflows` 阶段性交付。
