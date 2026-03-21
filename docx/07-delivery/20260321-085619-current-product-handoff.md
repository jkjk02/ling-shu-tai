# 灵枢台当前成品接管说明（CI 骨架后）

- 阶段：07-delivery
- 提交时间：20260321-085619
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/07-delivery/20260321-085515-unified-verification-and-ci-delivery.md
  - docx/07-delivery/20260321-084504-current-product-handoff.md

## 目标

1. 为新会话提供 CI 骨架补齐后的最新单一接管入口。
2. 让后续继续开发时直接基于当前验证与交付状态选择下一轮切片。

## 核心内容

## 当前状态

- 当前状态：阶段性交付可用，已具备后端自动化回归、统一验证入口与 GitHub Actions 骨架
- 真实性质：仍不是最终完整版，但交付链已经从“手工验证”为主提升到“本地统一验证 + 预置 CI”
- 最新增强基线：
  - `docx/07-delivery/20260321-085515-unified-verification-and-ci-delivery.md`

## 当前已完成能力

1. `Skills`
   - managed CRUD
   - `codex` / `cludea` / `opencode` 外部 skill 发现
   - discovered skill 详情读取与只读保护
2. `MCPs`
   - managed CRUD
   - `cludea` / `opencode` 外部 MCP 发现
   - discovered MCP 详情读取与只读保护
3. `Agents`
   - managed CRUD
   - Skill 多选、MCP 关联、Tool Scope 配置
4. `Workflows`
   - CRUD
   - 节点模板
   - 缩放、平移、自动布局
   - 节点结构化配置
   - 连线标签与条件
   - 后端结构校验
5. `Dashboard / Discovery`
   - 汇总统计
   - 外部 skill / MCP 发现状态展示
6. 自动化与交付链
   - `backend/.venv/bin/python -m unittest discover -s backend/tests`
   - `npm run check:backend`
   - `npm run test:backend`
   - `npm run verify`
   - `.github/workflows/ci.yml` GitHub Actions 骨架

## 已验证结果

1. `npm run verify` 通过
2. `npm run check:backend` 通过
3. `backend/.venv/bin/python -m unittest discover -s backend/tests` 通过，执行 6 个测试
4. `npm run build` 通过
5. 历史真实 HTTP 与 richer workflow round-trip 验证记录仍保留在上轮交付链

## 主要文件入口

1. 前端：
   - `src/pages/SkillsPage.vue`
   - `src/pages/McpsPage.vue`
   - `src/pages/AgentsPage.vue`
   - `src/pages/WorkflowsPage.vue`
   - `src/pages/DashboardPage.vue`
2. 后端：
   - `backend/app/config.py`
   - `backend/app/services/discovery.py`
   - `backend/app/routers/skills.py`
   - `backend/app/routers/mcps.py`
   - `backend/app/routers/workflows.py`
   - `backend/app/routers/dashboard.py`
   - `backend/app/routers/discovery.py`
3. 测试与交付：
   - `backend/tests/support.py`
   - `backend/tests/test_api_regression.py`
   - `package.json`
   - `.github/workflows/ci.yml`

## 明确未完成项

1. 浏览器交互自动化与前端组件测试尚未建立
2. GitHub Actions 工作流尚未在真实远端仓库执行
3. `Monaco Editor` 尚未接入
4. 外部 MCP 回写尚未实现
5. 当前编排器体验仍不是完整第三方流程图引擎
6. 当前目录仍不是 Git 仓库

## 建议下一步优先级

1. 浏览器级冒烟自动化
   - Workflows 关键交互冒烟
   - Dashboard / Discovery 基础展示回归
2. 真实远端 CI 落地
   - 把现有 `.github/workflows/ci.yml` 接进 GitHub 仓库并实际触发
3. `Monaco Editor`
   - Skill / Prompt / JSON 编辑体验升级
4. 外部 MCP 回写
   - 在确认真实格式样本后再补

## 新窗口接手提示

1. 若开新会话，优先读取本文件。
2. 再读取：
   - `docx/07-delivery/20260321-085515-unified-verification-and-ci-delivery.md`
   - `docx/07-delivery/20260321-084426-backend-api-test-automation-delivery.md`
3. 若继续沿用 `docx` 工作流，新一轮应从 `00-governance` 新建时间戳台账开始。

## 风险与待确认项

1. 当前成品适合继续开发与演示，但不能宣称最终完整版已完成。
2. 统一验证入口和 CI 骨架已经补齐，但浏览器层自动化与真实远端 CI 仍未闭环。
3. 本地运行真实后端回归时，在受限环境中可能仍需要本地 socket 权限。

## 交接输出

1. 本文件可作为压缩上下文后的最新单一接管入口。
2. 允许基于本文件继续推进“浏览器冒烟自动化”或“真实远端 CI 落地”切片。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-085720
- 备注：本文件更新到统一验证命令与 CI 骨架切片交付后的最新状态。
