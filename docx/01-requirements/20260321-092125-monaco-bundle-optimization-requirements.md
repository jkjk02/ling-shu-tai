# Monaco 包体优化需求基线

- 阶段：01-requirements
- 提交时间：20260321-092125
- 责任角色：requirements_analyst
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/00-governance/20260321-092125-monaco-bundle-optimization-run-ledger.md

## 目标

1. 减少 Monaco 相关前端产物体积。
2. 保持当前 `Skills`、`MCPs`、`Agents` 的编辑体验与保存链路不变。
3. 明确只保留当前真实需要的 Monaco 语言与 worker。

## 核心内容

## 功能模型

1. 当前保留能力
   - `Skills` 需要 `markdown`、`python`、`shell`、`plaintext`
   - `MCPs` 需要 `json`
   - `Agents` 需要 `markdown`
2. 当前可裁剪能力
   - 未接入页面不需要 `css`、`html`、`typescript/javascript` worker
3. 交付要求
   - Monaco 组件接口保持不变
   - 页面接入点无需回退

## 行为模型

1. 优化前后，三处编辑位使用方式不变
2. 构建后，Monaco 相关 worker/chunk 应明显减少或变小

## 数据模型

1. 不修改任何业务表单字段
2. 不修改后端接口或 payload

## 约束

1. 只做最小裁剪，不重做整个加载策略
2. 不为了优化而牺牲当前已接入语言能力

## 验收标准

1. `npm run build` 通过
2. 构建结果中不再产出未使用的 `css/html/ts` worker
3. README 与交付文档记录优化结果与限制

## 风险与待确认项

1. 如果后续又需要在 Monaco 中编辑 TS/HTML/CSS，需要重新补回对应 worker。

## 交接输出

1. 允许架构阶段采用最小 worker/语言裁剪方案。
2. 要求计划阶段把改动边界限制在 Monaco 组件与文档。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-092210
- 备注：需求锁定为 Monaco 真实使用集合优化。
