# Monaco 包体优化架构方案

- 阶段：02-architecture
- 提交时间：20260321-092125
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/01-requirements/20260321-092125-monaco-bundle-optimization-requirements.md

## 目标

1. 选择 Monaco 包体优化的最低风险实现路径。
2. 在不回退现有三处编辑器功能的前提下减少无效 worker 开销。

## 核心内容

## 方案比较

### 方案 A：只裁掉未使用 worker 与语言导入

1. 做法
   - 在 `MonacoCodeEditor.vue` 里删除 `css/html/typescript` worker
   - 保留当前真实使用的 `json` 与 editor worker
2. 优点
   - 改动最小
   - 风险最低
3. 缺点
   - 不能解决所有 chunk 警告

### 方案 B：进一步把 Monaco 组件改为按需懒加载

1. 做法
   - 改页面接入方式或组件内部装载方式
2. 优点
   - 可能进一步降低首屏影响
3. 缺点
   - 生命周期与弹窗交互复杂度明显上升
   - 当前切片过大

## 推荐方案

1. 采用方案 A。
2. 理由：
   - 当前主要问题是无效 worker 明显过大，先移除最确定的浪费项。
   - 等这一步稳定后，再决定是否需要做更重的懒加载优化。

## 风险与待确认项

1. 该方案不能保证所有大 chunk 警告消失，但应显著减少无意义的 worker 体积。
2. 未来若新增 HTML/CSS/TS 编辑位，需要重新引入对应 worker。

## 交接输出

1. 允许计划阶段按“Monaco 组件调整 + 构建验证 + README/文档更新”组织实施。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-092230
- 备注：采用最小 worker 裁剪方案。
