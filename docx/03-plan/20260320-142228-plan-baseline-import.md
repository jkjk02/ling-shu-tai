# 实施计划导入

- 阶段：03-plan
- 提交时间：20260320-142228
- 责任角色：solution_architect
- 当前状态：approved
- 评审状态：approved
- 输入依据：
  - docx/02-architecture/20260320-142228-architecture-baseline-import.md
  - doc/03-实施计划.md

## 目标

1. 将历史实施计划纳入 `docx/`。
2. 为本轮 `MCPs` 纵向切片给出明确工作包、写入边界和验收点。

## 核心内容

1. 继承计划结论：按“骨架 -> 模型/API -> 前端功能页 -> 联调测试”顺序推进。
2. 本轮实施范围：
   - `MCPs` 列表、详情、新建、编辑、删除
   - 前端 JSON 参数编辑与校验
   - 后端重复创建冲突保护、只读资源写保护
   - 构建验证与进程内冒烟

## 并行拆分

| worker | 负责范围 | 写入边界 | 输入文档 | 交付物 |
| --- | --- | --- | --- | --- |
| worker-frontend | `src/pages/McpsPage.vue`、`src/api/*`、`src/types/*` | 仅前端页面与契约 | 本文档 | `MCPs` 可用页面与 DTO |
| worker-backend | `backend/app/routers/mcps.py` | 仅后端路由 | 本文档 | `MCP` 写保护与错误码 |

## 完成定义

- `MCPs` 页面具备真实 CRUD 闭环
- 后端 `MCP` 重复创建返回 `409`
- 后端只读 `MCP` 更新/删除返回 `403`
- `npm run build` 通过
- 进程内 `MCP` 冒烟验证通过并恢复测试数据

## 风险与待确认项

1. 当前环境未提供稳定的独立 worker 调度闭环，必要时允许主代理本地按相同边界完成。
2. 本轮不引入新依赖，不接入 Monaco。

## 交接输出

1. 开发阶段以本文件为唯一实施拆分依据。
2. 评审阶段重点核对 `MCPs` 是否真正达到与 `Skills` 同等级的闭环水平。

## 批准记录

- 评审人：implementation_reviewer
- 评审结论：approved
- 批准时间：20260320-142228
- 备注：批准后进入 `MCPs` 纵向切片开发。
