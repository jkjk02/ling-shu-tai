# 工作流编排体验增强测试报告

- 阶段：06-test
- 提交时间：20260320-170248
- 责任角色：tester
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/05-review/20260320-170248-workflow-orchestration-ux-review.md
  - docx/04-implementation/20260320-170248-workflow-orchestration-ux-implementation.md

## 目标

1. 验证 richer workflow payload 是否可以被真实后端保存并回读。
2. 验证后端新加的 workflow 结构校验是否生效。

## 核心内容

1. 测试范围：
   - 构建验证：`npm run build`
   - Python 语法校验：`backend/.venv/bin/python -m py_compile backend/app/routers/workflows.py backend/app/schemas/resources.py backend/app/main.py`
   - 真实 HTTP 验证：`POST /api/workflows`、`GET /api/workflows/{id}`、`DELETE /api/workflows/{id}`、非法 workflow `POST /api/workflows`
2. 测试环境：
   - 真实服务：`uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8014`
3. 测试结论：
   - 轮次：1
   - 场景：工作流编排体验增强与后端结构校验
   - 结果：passed
4. 关键结果：
   - `POST /api/workflows` 成功创建 `orchestration-ux-verification`
   - `GET /api/workflows/{id}` 能回读：
     - `viewport = { x: 120.0, y: 48.0, zoom: 0.9 }`
     - `nodes[1].config = { kind: "task", stage: "implementation", status: "running", notes: "Execute plan" }`
     - `edges[0].condition = "requirements approved"`
   - 非法 payload 中使用不存在的 `agent_id=missing-agent`，`POST /api/workflows` 返回：
     - `422 workflow_invalid`
   - `DELETE /api/workflows/{id}` 成功，说明 round-trip 清理正常
5. 缺陷列表：
   - 本轮未发现阻断缺陷。

## 错误日志

~~~text
422 workflow_invalid
message: Workflow 中存在引用不存在 Agent 的节点。
details.invalid_node_agent_ids = ["bad-node"]
~~~

## 回流动作

- 回流给：无
- 修复负责人：无
- 下一轮计划：进入交付文档整理，并额外输出新的 handoff 文档

## 风险与待确认项

1. 当前测试未覆盖浏览器层面的手工拖拽与缩放回归。
2. 当前测试主要验证结构正确性与持久化回读，不等于验证所有 UX 细节。
3. 自动化浏览器测试体系仍未建立。

## 交接输出

1. 本轮达到交付条件，可进入 `07-delivery`。
2. 交付文档必须明确：当前编排体验显著增强，但项目仍不是最终完整版。

## 批准记录

- 评审人：tester / 主代理
- 评审结论：approved
- 批准时间：20260320-170248
- 备注：第 1 轮测试通过，无需进入缺陷重试回路。
