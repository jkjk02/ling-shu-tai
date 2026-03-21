# 外部MCP发现运行台账

- 阶段：00-governance
- 提交时间：20260320-162533
- 责任角色：主代理
- 当前状态：done
- 评审状态：approved
- 输入依据：
  - docx/07-delivery/20260320-161543-other-cli-external-skills-delivery.md
  - docx/07-delivery/20260320-155331-final-product-handoff.md

## 目标

1. 为新一轮“外部 MCP 发现”切片建立独立台账。
2. 基于最新交付判断下一优先级，并继续沿用既有批准需求与架构基线。
3. 在实施前锁定本轮范围、非范围、验证门槛和文档链路。

## 核心内容

1. 当前项目状态：
   - 项目仍是阶段性交付成品，不是最终完整版。
   - managed `Skills` / `MCPs` / `Agents` / `Workflows` CRUD 已完成，不应重复实施。
   - 外部 Skill 发现已补齐到 `codex` / `cludea` / `opencode`。
2. 本轮优先级判断：
   - 最新交付文档明确未完成项仍包括“外部 MCP 详情与回写”。
   - 当前 `backend/app/services/discovery.py` 只统计 `discovered_mcp_files`，但 `backend/app/routers/mcps.py` 仍只读 managed MCP 数据。
   - 因此本轮优先级锁定为“外部 MCP 发现与只读展示”，暂不进入 MCP 回写。
3. 继续沿用的批准基线：
   - 需求基线：`docx/01-requirements/20260320-142228-requirements-baseline-import.md`
   - 架构基线：`docx/02-architecture/20260320-142228-architecture-baseline-import.md`
   - 最新增强交付基线：`docx/07-delivery/20260320-161543-other-cli-external-skills-delivery.md`
4. 本轮范围：
   - 扩展后端 discovery，解析外部 MCP JSON 文件为只读 MCP 资源。
   - 让 `/api/mcps` 与 `/api/mcps/{id}` 支持 discovered MCP 列表和详情读取。
   - 对 discovered MCP 复用现有只读拒绝语义。
   - 让 Dashboard 中 MCP 统计包含 discovered MCP。
   - 对 MCP 页面做最小可见性补充，便于区分 managed 与 discovered。
5. 本轮非范围：
   - 不重复实现已完成的 managed CRUD。
   - 不实现外部 MCP 回写。
   - 不在本轮接入 Monaco、工作流画布增强或自动化测试体系。
   - 不宣称项目已最终完成。
6. 环境与验证约束：
   - 当前环境不存在真实 `~/.cludea` / `~/.opencode` MCP 目录样本，需要用临时 fixture + 环境变量覆盖验证。
   - 当前目录不是 Git 仓库，本轮继续只以 `docx` 文档固化状态。

## 风险与待确认项

1. 第三方 MCP JSON 格式差异可能比 skill 更大，本轮只能做最佳努力解析。
2. 若 discovered MCP 的 ID 生成与 managed MCP 冲突，需要在创建路径做只读冲突保护。
3. 若 Dashboard 和 Agents 页开始消费 discovered MCP，需要确保既有 managed 交互未回归。

## 交接输出

1. 允许计划阶段按“发现解析 / 路由聚合 / 只读保护 / Dashboard 统计 / MCP 页面可见性 / HTTP 验证”组织实施。
2. 要求测试阶段至少覆盖：
   - `GET /api/mcps`
   - `GET /api/mcps/{id}`
   - `PUT /api/mcps/{discovered_id}`
   - `DELETE /api/mcps/{discovered_id}`
   - `GET /api/dashboard`
   - `GET /api/discovery`
3. 交付阶段必须明确：本轮只补“外部 MCP 发现与只读展示”，外部 MCP 回写仍未完成。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260320-162533
- 备注：本轮沿用既有批准基线，仅新增“外部 MCP 发现”增强切片。
