# 统一验证命令与 CI 接入架构方案

- 阶段：02-architecture
- 提交时间：20260321-085058
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/01-requirements/20260321-085058-unified-verification-and-ci-requirements.md

## 目标

1. 选择最合适的统一验证与 CI 接入路径。
2. 在当前“无 Git 远端、无新增依赖”的约束下最大化复用已存在验证链。

## 核心内容

## 方案比较

### 方案 A：仅新增本地统一脚本，不提供 CI 工作流

1. 做法
   - 只在 `package.json` 增加 `check:*` / `verify` 脚本
2. 优点
   - 实现最小、维护成本低
3. 缺点
   - 无法把当前验证链固化为仓库级 CI 约定
   - 未来进入远端仓库后仍要重复补工作流文件

### 方案 B：新增本地统一脚本，同时补 GitHub Actions CI 骨架

1. 做法
   - 在 `package.json` 增加本地统一验证脚本
   - 在 `.github/workflows/ci.yml` 预置 Node/Python 双运行时验证链
2. 优点
   - 同时解决本地入口分散和远端接入缺位的问题
   - 未来推送到 GitHub 后可直接启用
3. 缺点
   - 需要额外维护一个 CI 文件
   - 当前本地无法真实执行 GitHub Actions，只能做静态审阅和逻辑校验

## 推荐方案

1. 采用方案 B。
2. 理由：
   - 新增文件少，但收益高。
   - 当前验证资产已经稳定，适合被提升为仓库规范。
   - 虽然本地不能真实触发远端 CI，但工作流文件仍能作为交付物固化下来。

## 目标架构

1. `package.json`
   - 新增细粒度脚本：
     - `check:backend`
     - `test:backend`
     - `verify`
2. `.github/workflows/ci.yml`
   - `on: [push, pull_request]`
   - 步骤：
     - checkout
     - setup-node
     - setup-python
     - `npm ci`
     - 创建 `backend/.venv`
     - 安装 `backend/requirements.txt`
     - 执行 backend check / test / build
3. `README.md`
   - 记录本地统一命令和 CI 骨架说明

## 质量属性与取舍

1. 一致性：本地统一命令与 CI 步骤尽量复用同一组子命令。
2. 可迁移性：CI 依赖系统 Python，而本地继续允许项目内 venv。
3. 低风险：不修改业务代码，不引入新依赖。

## 风险与待确认项

1. GitHub Actions YAML 本地无法真实执行，只能靠结构审阅与命令对齐降低风险。
2. 现有本地统一脚本若用 `backend/.venv` 绝对路径，要求开发者先完成 README 中的后端初始化。

## 交接输出

1. 允许计划阶段按“本地脚本 + CI 文件 + README”拆分实施。
2. 要求实现阶段把 CI 的执行命令尽量映射到 `package.json` 脚本，而不是在 YAML 里重复硬编码长命令。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-085200
- 备注：采用“本地统一脚本 + GitHub Actions CI 骨架”方案。
