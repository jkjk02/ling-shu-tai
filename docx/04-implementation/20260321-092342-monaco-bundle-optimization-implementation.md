# Monaco 包体优化实现记录

- 阶段：04-implementation
- 提交时间：20260321-092342
- 责任角色：systems_implementer
- 当前状态：done
- 评审状态：pending
- 输入依据：
  - docx/03-plan/20260321-092125-monaco-bundle-optimization-plan.md

## 目标

1. 收缩 Monaco 到当前真实用到的 worker 集合。
2. 在不改页面接入和编辑体验的前提下减少构建负担。

## 核心内容

1. 组件裁剪
   - 修改 `src/components/MonacoCodeEditor.vue`
   - 删除未使用的：
     - `css.worker`
     - `html.worker`
     - `ts.worker`
   - 保留：
     - `editor.worker`
     - `json.worker`
     - `markdown/python/shell` 基础语言贡献
2. 构建结果对比
   - 优化前：
     - `css.worker`、`html.worker`、`ts.worker` 均进入产物
     - 构建时间约 `31.82s`
   - 优化后：
     - 上述 3 个 worker 从产物中消失
     - 构建时间降至约 `18.50s`
3. 体验边界
   - 当前三处 Monaco 接入点均不依赖被删除的 worker，因此功能不回归

## 代码归属

1. 主代理
   - `src/components/MonacoCodeEditor.vue`
   - `README.md`
   - `docx/`

## 验证方式

1. `npm run build`

## 风险与待确认项

1. `MonacoCodeEditor` 主 chunk 仍然很大，本轮只消除了确定无效的 worker。
2. 若未来新增 HTML/CSS/TS 编辑位，需要重新引入对应 worker。

## 交接输出

1. 允许进入实现评审阶段。
2. 评审阶段重点确认未使用 worker 已移除且构建通过。

## 批准记录

- 评审人：待评审
- 评审结论：pending
- 批准时间：
- 备注：实现已完成，等待 Stage 5 评审。
