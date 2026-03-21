# 统一验证命令与 CI 接入实现记录

- 阶段：04-implementation
- 提交时间：20260321-085239
- 责任角色：systems_implementer
- 当前状态：done
- 评审状态：pending
- 输入依据：
  - docx/03-plan/20260321-085058-unified-verification-and-ci-plan.md

## 目标

1. 为现有验证链补统一命令入口。
2. 为仓库补 GitHub Actions CI 骨架。
3. 同步 README，说明本地与 CI 的使用方式。

## 核心内容

1. 统一验证命令
   - 在 `package.json` 新增：
     - `check:backend`
     - `test:backend`
     - `verify`
   - `verify` 串联后端语法校验、后端自动化回归和前端构建，作为本轮主验收入口。
2. CI 骨架
   - 新增 `.github/workflows/ci.yml`
   - 工作流覆盖：
     - checkout
     - Node 22
     - Python 3.12
     - `npm ci`
     - 创建 `backend/.venv`
     - 安装 `backend/requirements.txt`
     - 执行 `npm run check:backend`
     - 执行 `npm run test:backend`
     - 执行 `npm run build`
3. 文档更新
   - README 新增统一验证入口与 CI 骨架说明。

## 代码归属

1. worker-1
   - `package.json`
   - `.github/workflows/ci.yml`
2. 主代理
   - `README.md`
   - `docx/` 阶段文档与交付集成

## 验证方式

1. `npm run check:backend`
2. `npm run verify`

## 风险与待确认项

1. GitHub Actions 工作流在当前本地目录无法真实触发，只能作为仓库内交付骨架。
2. 统一脚本依赖项目内 `backend/.venv`，开发者若未完成后端初始化会直接失败。
3. 当前 CI 仍未覆盖浏览器交互自动化。

## 交接输出

1. 允许进入实现评审阶段。
2. 评审阶段需重点检查脚本是否清晰、CI 是否复用本地脚本、README 是否说明前置条件。

## 批准记录

- 评审人：待评审
- 评审结论：pending
- 批准时间：
- 备注：实现已完成，等待 Stage 5 评审。
