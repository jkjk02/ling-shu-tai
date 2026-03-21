# 其他CLI外部Skill发现运行台账

- 阶段：00-governance
- 提交时间：20260320-155940
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/07-delivery/20260320-155331-final-product-handoff.md
  - docx/07-delivery/20260320-153601-codex-external-skills-delivery.md
  - docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md

## 目标

1. 为新一轮“其他 CLI 外部 Skill 发现”切片建立独立台账。
2. 根据最新 handoff 判断下一优先级，沿用既有批准基线，不重复已完成 CRUD。
3. 在实施前固定本轮范围、验证门槛、代理分工和风险边界。

## 核心内容

1. 已确认当前项目状态：
   - 项目当前为阶段性交付可用，不是最终完整版。
   - `Skills`、`MCPs`、`Agents`、`Workflows` 的 managed CRUD 已完成，不应重复实施。
   - 已完成真实 Codex `SKILL.md` 发现、只读保护与前端展示闭环。
2. 已确认本轮优先级：
   - `final-product-handoff` 建议优先项包含“其他工具外部解析”“外部 MCP”“Monaco”“自动化测试”。
   - 代码检查结果显示 `backend/app/config.py` 已为 `cludea` 与 `opencode` 预置候选根目录，但 `backend/app/services/discovery.py` 当前只对 `codex` 真实解析 `SKILL.md`。
   - 基于现有架构与最小增量原则，本轮优先推进“其他 CLI 外部 Skill 发现”，暂不进入外部 MCP 回写与 Monaco 编辑器接入。
3. 已确认继续沿用的批准基线：
   - 需求基线：`docx/01-requirements/20260320-142228-requirements-baseline-import.md`
   - 架构基线：`docx/02-architecture/20260320-142228-architecture-baseline-import.md`
   - 最新交付接管基线：`docx/07-delivery/20260320-155331-final-product-handoff.md`
4. 本轮范围锁定：
   - 扩展后端 discovery，让 `cludea` / `opencode` 也能发现外部 Skill 文件。
   - 复用现有 `Skills` 只读聚合链路，在列表、详情、Dashboard/Discovery 统计中体现新增发现结果。
   - 使用受控 fixture 或环境变量覆盖目录进行验证，因为当前环境不存在真实 `~/.cludea` / `~/.opencode` 目录。
5. 本轮明确非范围：
   - 不重复实现 `Skills` / `MCPs` / `Agents` / `Workflows` 已完成的 CRUD。
   - 不在本轮实现外部 MCP 详情读取、只读聚合和回写。
   - 不在本轮接入 Monaco Editor 或重做 Workflows 画布。
   - 不宣称项目已最终完成。
6. 当前环境检查结论：
   - `/home/lst/ling-shu-tai` 当前不是 Git 仓库，无法记录提交哈希。
   - 真实外部 Skill 样本目前仅确认存在 `/root/.codex/skills/*/SKILL.md`。
   - 未发现 `~/.cludea`、`~/.claude`、`~/.opencode` 目录，因此测试需自建临时样本。
7. 运行台账：

| 名称 | 类型 | agent id | 当前状态 | 负责范围 | 最近产出 |
| --- | --- | --- | --- | --- | --- |
| 主代理 | orchestrator | main | in_progress | `docx/`、代码集成、验证、交付 | 已完成优先级判断并创建本轮治理台账 |
| Harvey | solution_architect | 019d0a41-d783-7d11-b09c-e7164db7812d | completed | 本轮 Stage 3 计划建议 | 已确认需要新建 `03-plan`，范围仅限 `cludea` / `opencode` 外部 Skill 发现，不建议并行 worker |
| Planck | requirements_tracker | 019d0a41-d7a3-7631-aa28-60cafdc62813 | completed | 需求/架构基线沿用核对 | 已确认无需新增 `01/02` 文档，继续沿用既有批准基线 |

## 风险与待确认项

1. `cludea` / `opencode` 的真实外部 Skill 文件格式可能与 Codex `SKILL.md` 不同，需要采用“候选文件模式 + 最佳努力解析 + 回退正文”的兼容策略。
2. 新发现的外部 Skill 必须继续保持只读，不能误穿透现有 managed 写路径。
3. 当前环境缺少真实 `cludea` / `opencode` 外部目录，若 fixture 设计过窄，可能高估解析兼容性。
4. 当前目录不是 Git 仓库，本轮只能通过阶段文档固化状态，不能提供提交记录。

## 交接输出

1. 允许计划阶段以本台账、既有批准需求/架构基线和最新 handoff 作为唯一上游输入继续推进。
2. 要求实现阶段至少验证：
   - `GET /api/skills`
   - `GET /api/skills/{id}`
   - `PUT /api/skills/{id}` 对 discovered skill 的只读拒绝
   - `DELETE /api/skills/{id}` 对 discovered skill 的只读拒绝
   - `GET /api/dashboard`
   - `GET /api/discovery`
3. 要求交付阶段明确说明：本轮只补“其他 CLI 外部 Skill 发现”，整项目仍是阶段性交付。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-155940
- 备注：本轮沿用既有批准基线，仅新增“其他 CLI 外部 Skill 发现”增强切片。
