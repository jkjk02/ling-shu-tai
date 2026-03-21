# Codex外部Skill发现测试

- 阶段：06-test
- 提交时间：20260320-153601
- 责任角色：tester
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/05-review/20260320-153601-codex-external-skills-review.md
  - docx/04-implementation/20260320-153601-codex-external-skills-implementation.md

## 目标

1. 验证 Codex 外部 Skill 发现切片是否达到本轮最小可交付标准。
2. 记录构建、真实 HTTP 结果、回归结果、缺陷结论和是否允许进入交付。

## 核心内容

### 上游输入版本

1. 实施计划版本：`docx/03-plan/20260320-153601-codex-external-skills-plan.md`
2. 实现记录版本：`docx/04-implementation/20260320-153601-codex-external-skills-implementation.md`
3. 评审版本：`docx/05-review/20260320-153601-codex-external-skills-review.md`

### 测试范围

1. 前端正式构建
2. `Skills` 真实 HTTP discovered 列表与详情联调
3. `Dashboard` 与 `Discovery` 统计联调
4. discovered skill 的只读保护
5. managed skill CRUD 回归

## 测试结论

- 轮次：1
- 场景：Codex 外部 Skill 发现真实联调验证
- 结果：passed

### 执行结果

1. `npm run build` 通过。
2. 真实 HTTP 通过 `http://127.0.0.1:5173/api` 验证通过：
   - `/skills -> 200, total=6`
   - discovered Codex skills：5 个
   - 代表性 discovered id：`codex-discovered-system-openai-docs`
   - `/skills/{id} -> 200, source_kind=discovered, is_writable=false`
   - `/dashboard -> 200, total_skills=6, codex skills=6`
   - `/discovery -> 200, codex discovered_skill_files=5`
   - `PUT /skills/{discovered_id} -> 403, code=skill_read_only`
   - `DELETE /skills/{discovered_id} -> 403, code=skill_read_only`
3. managed skill 回归验证：
   - `create -> 201, id=http-managed-skill-smoke`
   - `update -> 200, description=managed smoke updated`
   - `delete -> 200, deleted=true`
4. 本轮回归后未污染 `backend/data/skills.json`。

### 缺陷列表

1. 本轮测试范围内未发现阻塞性代码缺陷。
2. 已发现并闭环的流程问题：
   - 初版 `04-implementation` 文档未补全，评审阶段无法正式放行
   - 处理方式：回填实现文档并清理 `03-plan` 重复模板尾段
   - 复核结果：通过，不需要代码返工

### 重试轮次

1. 重试轮次：1
2. 重试原因：阶段文档不完整导致评审未放行，不属于代码缺陷
3. 当前状态：已闭环，不需要继续重试

## 错误日志

~~~text
真实 HTTP 关键结果：
/skills -> 200, total=6
discovered codex skills -> 5
/skills/{id} -> 200, source_kind=discovered, is_writable=false
/dashboard -> 200, total_skills=6, codex skills=6
/discovery -> 200, codex discovered_skill_files=5
PUT /skills/{discovered_id} -> 403, code=skill_read_only
DELETE /skills/{discovered_id} -> 403, code=skill_read_only

managed skill 回归：
create -> 201, id=http-managed-skill-smoke
update -> 200
delete -> 200
~~~

## 风险与待确认项

1. 当前测试未覆盖复杂 front matter、异常 Markdown 或大规模外部 skill 目录。
2. 当前只验证了 Codex `SKILL.md`，未覆盖其他 CLI 工具或外部 MCP 解析。
3. 当前测试未覆盖浏览器级完整手工交互录屏或自动化端到端回归。

## 是否达到交付条件

1. 就本轮 Codex 外部 Skill 发现切片而言：达到进入交付阶段的条件。
2. 就整项目最终目标而言：外部资源发现只补齐了 Codex Skills，`Monaco`、其他工具外部解析、外部 MCP 解析与自动化测试仍未完成。

## 交接输出

1. 允许进入本轮阶段性交付。
2. 交付摘要需明确：
   - Codex discovered skills 已可真实读取并只读展示
   - managed skill 写路径回归通过
   - 整项目仍未达到最终完整版目标

## 批准记录

- 评审人：tester
- 评审结论：approved
- 批准时间：20260320-154652
- 备注：本轮测试范围内通过，建议进入 Codex 外部 Skill 发现阶段性交付。
