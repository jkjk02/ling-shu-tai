# Monaco 懒加载优化架构方案

- 阶段：02-architecture
- 提交时间：20260321-140840
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/01-requirements/20260321-140840-monaco-lazy-load-requirements.md

## 目标

1. 选择 Monaco 懒加载优化的最低风险实现路径。

## 核心内容

## 方案比较

### 方案 A：继续静态 import Monaco 组件

1. 优点：简单
2. 缺点：页面模块仍直接依赖 Monaco 组件

### 方案 B：页面使用 `defineAsyncComponent` 按需引入 Monaco 组件

1. 优点：
   - 页面首段代码不再静态绑定 Monaco 组件
   - 改动小，不破坏共享组件
2. 缺点：
   - 需要处理首次打开弹窗的异步加载

## 推荐方案

1. 采用方案 B。
2. 理由：
   - 改动小、风险低、与当前架构兼容。

## 风险与待确认项

1. 该方案不等于彻底解决主 chunk 体积问题。

## 交接输出

1. 允许计划阶段按“三页 import 方式调整 + 构建验证 + 文档更新”组织实施。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-140930
- 备注：采用 `defineAsyncComponent` 最小方案。
