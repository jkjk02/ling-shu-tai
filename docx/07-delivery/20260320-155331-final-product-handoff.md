# 灵枢台当前成品接管说明

- 阶段：07-delivery
- 提交时间：20260320-155331
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/07-delivery/20260320-153601-codex-external-skills-delivery.md
  - docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md

## 目标

1. 给出一份可脱离当前长上下文的最终接管说明。
2. 让新会话或新窗口能基于单一文档快速恢复项目状态并继续推进。

## 核心内容

# 成品状态

- 当前状态：阶段性交付可用
- 真实性质：不是最终完整版，但已具备可直接演示和继续开发的当前成品
- 最新交付基线：
  - `docx/07-delivery/20260320-153601-codex-external-skills-delivery.md`

## 当前已完成能力

1. `Skills`：
   - managed skills 的列表、详情、新建、编辑、删除闭环
   - 真实 Codex `SKILL.md` 外部发现
   - discovered skills 的只读展示与只读保护
2. `MCPs`：
   - 列表、详情、新建、编辑、删除闭环
3. `Agents`：
   - 列表、详情、新建、编辑、删除闭环
   - Skill 多选分配、MCP 关联、Tool Scope 配置
4. `Workflows`：
   - 列表、详情、新建、编辑、删除闭环
   - 最小可用画布：节点新增、拖拽、Agent 绑定、连线编辑、保存、加载
5. `Dashboard` / `Discovery`：
   - 总览统计
   - 发现状态展示
   - Codex discovered skills 统计已纳入总览

## 已验证结果

1. `npm run build` 通过
2. 真实 HTTP 已验证：
   - `Skills` CRUD
   - `MCPs` CRUD
   - `Agents` CRUD
   - `Workflows` CRUD
   - Codex discovered skills 列表、详情、只读保护
   - `Dashboard` / `Discovery` 统计
3. 回归验证已确认：
   - 外部 discovered skills 接入后，没有破坏 managed skill 的写路径

## 启动方式

1. 前端：
   - `cd /home/lst/ling-shu-tai`
   - `npm run dev`
2. 后端：
   - `cd /home/lst/ling-shu-tai`
   - `backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000`

## 关键路径

1. 前端通过 `/api` 访问后端
2. 后端数据文件：
   - `backend/data/skills.json`
   - `backend/data/mcps.json`
   - `backend/data/agents/agents.json`
   - `backend/data/workflows/workflows.json`
3. Codex 外部 Skill 候选根目录：
   - `$LINGSHU_CODEX_ROOT`
   - `~/.codex`
   - `~/.config/codex`

## 主要文件入口

1. 前端页面：
   - `src/pages/SkillsPage.vue`
   - `src/pages/McpsPage.vue`
   - `src/pages/AgentsPage.vue`
   - `src/pages/WorkflowsPage.vue`
   - `src/pages/DashboardPage.vue`
2. 后端路由：
   - `backend/app/routers/skills.py`
   - `backend/app/routers/mcps.py`
   - `backend/app/routers/agents.py`
   - `backend/app/routers/workflows.py`
   - `backend/app/routers/dashboard.py`
   - `backend/app/routers/discovery.py`
3. 后端发现逻辑：
   - `backend/app/services/discovery.py`

## 明确未完成项

1. `Monaco Editor` 尚未接入
2. 工作流画布仍是最小实现，不是完整 `Vue Flow` 级体验
3. 其他 CLI 工具的外部 Skill / MCP 真实解析尚未补齐
4. 外部 MCP 解析与回写尚未完成
5. 自动化测试体系尚未建立
6. 当前目录仍不是 Git 仓库，未执行提交和推送

## 建议下一步优先级

1. 其他工具外部解析：
   - `cludea`
   - `opencode`
   - 外部 MCP
2. `Monaco Editor` 接入到脚本编辑体验
3. 自动化测试：
   - API 回归
   - 前端关键页面冒烟
4. 视需要再升级 `Workflows` 画布体验

## 新窗口接手提示

1. 若开 `/new`，优先读取本文件。
2. 再读取以下两份最新交付基线：
   - `docx/07-delivery/20260320-153601-codex-external-skills-delivery.md`
   - `docx/07-delivery/20260320-151548-workflows-vertical-slice-delivery.md`
3. 若继续沿用 `docx` 工作流，新一轮应从 `00-governance` 新建时间戳台账开始。

## 风险与待确认项

1. 当前成品适合交接和继续开发，但不能宣称“最终完整版已完成”。
2. 若新窗口继续推进，应保持“真实验证先行、文档同步批准”的工作流，不要只改代码不补 `docx`。

## 交接输出

1. 本文件可作为压缩上下文后的单一接管入口。
2. 允许基于本文件在新窗口继续推进。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-155331
- 备注：本文件用于最终交接与上下文压缩，不改变现有阶段性交付结论。
