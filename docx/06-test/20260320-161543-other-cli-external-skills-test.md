# 其他CLI外部Skill发现测试报告

- 阶段：06-test
- 提交时间：20260320-161543
- 责任角色：tester
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/05-review/20260320-161543-other-cli-external-skills-review.md
  - docx/04-implementation/20260320-161543-other-cli-external-skills-implementation.md

## 目标

1. 验证 `cludea` / `opencode` discovered skill 是否进入现有 `Skills` / `Dashboard` / `Discovery` 链路。
2. 验证 discovered skill 的只读保护是否未回归。

## 核心内容

1. 测试范围：
   - 构建验证：`npm run build`
   - Python 语法校验：`backend/.venv/bin/python -m py_compile ...`
   - 真实 HTTP 验证：`GET /api/skills`、`GET /api/skills/{id}`、`PUT /api/skills/{id}`、`DELETE /api/skills/{id}`、`GET /api/dashboard`、`GET /api/discovery`
2. 测试环境：
   - 临时 fixture 根目录：`/tmp/ling-shu-tai-discovery-wia5gc3g`
   - 覆盖变量：
     - `LINGSHU_CLUDEA_ROOT=/tmp/ling-shu-tai-discovery-wia5gc3g/cludea-root`
     - `LINGSHU_OPENCODE_ROOT=/tmp/ling-shu-tai-discovery-wia5gc3g/opencode-root`
   - 真实服务：`uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8012`
3. 测试结论：
   - 轮次：1
   - 场景：其他 CLI 外部 skill 发现与只读保护回归
   - 结果：passed
4. 关键结果：
   - `GET /api/skills` 返回：
     - `cludea-discovered-skills-design`
     - `opencode-discovered-commands-triage-prompt`
   - `GET /api/skills/{id}` 返回 `source_kind=discovered`、`script_language=markdown`、触发命令与描述正确。
   - `PUT /api/skills/cludea-discovered-skills-design` 返回 `403 skill_read_only`。
   - `DELETE /api/skills/opencode-discovered-commands-triage-prompt` 返回 `403 skill_read_only`。
   - `GET /api/dashboard` 中：
     - `cludea.skills=1`
     - `opencode.skills=1`
   - `GET /api/discovery` 中：
     - `cludea.discovered_skill_files=1`
     - `opencode.discovered_skill_files=1`
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

1. 测试覆盖的是临时 fixture，不是用户真实目录。
2. 未覆盖浏览器端手工点击回归；前端可见性依赖现有页面对后端数据的消费。
3. 仍未建立自动化测试体系。

## 交接输出

1. 本轮达到交付条件，可进入 `07-delivery`。
2. 交付文档必须明确：当前项目仍是阶段性成品，不是最终完整版。

## 批准记录

- 评审人：tester / 主代理
- 评审结论：approved
- 批准时间：20260320-161543
- 备注：第 1 轮测试通过，无需进入缺陷重试回路。
