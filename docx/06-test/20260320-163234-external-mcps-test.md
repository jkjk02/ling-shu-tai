# 外部MCP发现测试报告

- 阶段：06-test
- 提交时间：20260320-163234
- 责任角色：tester
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/05-review/20260320-163234-external-mcps-review.md
  - docx/04-implementation/20260320-163234-external-mcps-implementation.md

## 目标

1. 验证 discovered MCP 是否进入现有 `MCPs` / `Dashboard` / `Discovery` 链路。
2. 验证 discovered MCP 的只读保护是否未回归。

## 核心内容

1. 测试范围：
   - 构建验证：`npm run build`
   - Python 语法校验：`backend/.venv/bin/python -m py_compile ...`
   - 真实 HTTP 验证：`GET /api/mcps`、`GET /api/mcps/{id}`、`PUT /api/mcps/{id}`、`DELETE /api/mcps/{id}`、`GET /api/dashboard`、`GET /api/discovery`
2. 测试环境：
   - 临时 fixture 根目录：`/tmp/ling-shu-tai-mcp-discovery-8wx58vjt`
   - 覆盖变量：
     - `LINGSHU_CLUDEA_ROOT=/tmp/ling-shu-tai-mcp-discovery-8wx58vjt/cludea-root`
     - `LINGSHU_OPENCODE_ROOT=/tmp/ling-shu-tai-mcp-discovery-8wx58vjt/opencode-root`
   - 真实服务：`uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8013`
3. 测试结论：
   - 轮次：1
   - 场景：外部 MCP 发现与只读保护回归
   - 结果：passed
4. 关键结果：
   - `GET /api/mcps` 返回：
     - `cludea-discovered-mcps-sonnet`
     - `opencode-discovered-models-reasoning`
   - `GET /api/mcps/{id}` 返回 `source_kind=discovered`、`is_writable=false`，并能读取 `model_name` 与 `extra_params`。
   - `PUT /api/mcps/cludea-discovered-mcps-sonnet` 返回 `403 mcp_read_only`。
   - `DELETE /api/mcps/opencode-discovered-models-reasoning` 返回 `403 mcp_read_only`。
   - `GET /api/dashboard` 中：
     - `cludea.mcps=1`
     - `opencode.mcps=2`
   - `GET /api/discovery` 中：
     - `cludea.discovered_mcp_files=1`
     - `opencode.discovered_mcp_files=1`
5. 缺陷列表：
   - 本轮未发现阻断缺陷。

## 错误日志

~~~text
无。本轮真实 HTTP 复测通过，未触发缺陷回流。
~~~

## 回流动作

- 回流给：无
- 修复负责人：无
- 下一轮计划：进入交付文档整理，明确残余风险与非完成项

## 风险与待确认项

1. 测试覆盖的是临时 fixture，不是用户真实 MCP 目录。
2. 未覆盖浏览器端手工点击回归；前端本轮仅通过构建验证回归。
3. 仍未建立自动化测试体系。

## 交接输出

1. 本轮达到交付条件，可进入 `07-delivery`。
2. 交付文档必须明确：当前项目仍是阶段性成品，外部 MCP 回写仍未完成。

## 批准记录

- 评审人：tester / 主代理
- 评审结论：approved
- 批准时间：20260320-163234
- 备注：第 1 轮测试通过，无需进入缺陷重试回路。
