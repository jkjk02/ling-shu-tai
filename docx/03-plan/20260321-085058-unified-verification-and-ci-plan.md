# 统一验证命令与 CI 接入实施计划

- 阶段：03-plan
- 提交时间：20260321-085058
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/02-architecture/20260321-085058-unified-verification-and-ci-architecture.md

## 目标

1. 把 CI 接入切片拆成小而明确的写集。
2. 保证脚本、CI 文件和文档边界清晰，避免冲突。

## 核心内容

## 实施拆分

1. 工作包 A：统一验证脚本与 CI 骨架
   - 改动文件：`package.json`、`.github/workflows/ci.yml`
   - 目标：落地本地统一命令和 GitHub Actions 工作流
2. 工作包 B：文档更新与交付集成
   - 改动文件：`README.md`、`docx/`
   - 目标：补充本地执行方式、CI 说明和阶段文档链

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| worker-1 | 脚本与 CI 文件 | `package.json`, `.github/workflows/` | 已批准架构方案 | 统一验证命令与 CI 骨架 |

说明：
- README 与 `docx` 由主代理集成，避免与 worker-1 冲突。
- 本轮任务较小，不再拆分更多代码 worker。

## 实施顺序

1. 先补 `package.json` 脚本。
2. 再补 `.github/workflows/ci.yml` 并复用脚本。
3. 最后更新 README 和交付文档。

## 验证计划

1. `npm run check:backend`
2. `npm run test:backend`
3. `npm run verify`

## 完成定义

1. 本地统一命令可执行通过。
2. README 能说明命令和 CI 骨架用途。
3. CI YAML 逻辑自洽，覆盖 checkout、依赖安装和验证步骤。

## 风险与待确认项

1. `npm run verify` 若直接调用 `npm run build`，会重复 Node 启动开销，但复杂度最低，当前可接受。
2. 当前没有 GitHub Actions 本地执行器，CI 文件只能做静态交付。

## 交接输出

1. 允许实施阶段按单 worker 代码实现 + 主代理文档集成推进。
2. 评审阶段重点核查脚本命名是否清晰、CI 是否复用本地脚本、README 是否说明前置条件。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-085220
- 备注：写入边界清晰，允许进入实施阶段。
