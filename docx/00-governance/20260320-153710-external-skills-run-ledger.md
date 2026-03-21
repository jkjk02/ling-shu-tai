# 外部Skill发现运行台账

- 阶段：00-governance
- 提交时间：20260320-153710
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md

## 目标

1. 为新一轮“Codex 外部 Skill 发现”切片建立独立台账。
2. 沿用已批准的需求、架构与最新交付基线，不重复制造需求与架构分叉。
3. 把本轮负责 agent、阶段状态、验证门槛和关键决策固化到 `docx/`。

## 核心内容

1. 已确认本轮唯一上游交付基线：
   - `docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md`
2. 已确认继续沿用的批准基线：
   - 需求基线：`docx/01-requirements/20260320-142228-requirements-baseline-import.md`
   - 架构基线：`docx/02-architecture/20260320-142228-architecture-baseline-import.md`
3. 本轮目标锁定为：
   - 从真实外部目录发现 Codex Skills
   - 解析 `SKILL.md` 元数据与正文
   - 在平台中以只读资源方式展示 discovered Skills
   - 让 Dashboard / Discovery / Skills 列表反映真实外部发现结果
4. 当前已确认的真实外部源：
   - `/root/.codex/skills/agents-team/SKILL.md`
   - `/root/.codex/skills/docx-multi-agent-delivery/SKILL.md`
5. 运行台账：

| 名称 | 类型 | agent id | 当前状态 | 负责范围 | 最近产出 |
| --- | --- | --- | --- | --- | --- |
| 主代理 | orchestrator | main | in_progress | `docx/`、前端可见性补充、集成验证、交付 | 已创建新一轮阶段文档并补充 `SkillsPage` 来源标识 |
| Euler | solution_architect | 019d0a2c-6307-7961-90f4-5d5ac19f482c | running | 本轮实施计划文档 | 生成中 |
| Hubble | worker | 019d0a2c-f5ce-7931-b369-d2c0ad41e07e | running | 后端 discovery / skills / dashboard | 生成中 |

6. 并行约束：
   - 主代理仅修改前端 `Skills` 页面与 `docx/` 文档。
   - worker `Hubble` 仅修改后端 discovery / skills / dashboard 相关文件。
   - 本轮写集已明确分离，避免前后端抢文件。

## 风险与待确认项

1. 当前真实外部源已确认存在，但 `SKILL.md` 格式是 Markdown 元数据文件，不是原先 discovery 统计的 JSON，需要新增解析逻辑。
2. 外部 discovered skills 必须保持只读，不能误接入现有 managed 写路径。
3. 当前目录仍不是 Git 仓库，本轮继续按用户要求直接交付，不执行提交与推送。

## 交接输出

1. 允许计划阶段以本台账和最新已批准交付文档作为唯一上游输入继续推进。
2. 要求实现阶段重点验证：
   - `GET /api/skills`
   - `GET /api/skills/{id}`
   - `GET /api/dashboard`
   - `GET /api/discovery`
   - discovered skill 的只读语义

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-153710
- 备注：本轮沿用既有批准基线，仅新增“外部 Skill 发现”增强切片。
