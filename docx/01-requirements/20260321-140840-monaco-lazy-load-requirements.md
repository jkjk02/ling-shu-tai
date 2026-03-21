# Monaco 懒加载优化需求基线

- 阶段：01-requirements
- 提交时间：20260321-140840
- 责任角色：requirements_analyst
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/00-governance/20260321-140840-monaco-lazy-load-run-ledger.md

## 目标

1. 让页面只在需要编辑时才加载 Monaco 组件。
2. 保持当前三处编辑位的功能、字段与保存链路不变。

## 核心内容

## 功能模型

1. `Skills`、`MCPs`、`Agents` 页面应通过异步组件方式接入 Monaco。
2. 只有打开新建/编辑弹窗时才需要真正请求 `MonacoCodeEditor` 相关代码。

## 行为模型

1. 页面列表和详情展示阶段不需要立即拉取 Monaco 组件。
2. 打开弹窗时再异步解析 Monaco 组件。

## 数据模型

1. 表单字段保持不变。
2. 共享组件接口保持不变。

## 约束

1. 不改 `MonacoCodeEditor` 对外 props / emits。
2. 不改后端和保存 payload。

## 验收标准

1. 三页都改为异步组件接入。
2. `npm run build` 通过。

## 风险与待确认项

1. 构建结果可能不会明显缩小，但运行时加载路径应更合理。

## 交接输出

1. 允许架构阶段采用最小异步组件方案。

## 批准记录

- 评审人：主代理
- 评审结论：approved
- 批准时间：20260321-140915
- 备注：需求锁定为页面按需异步引入 Monaco。
