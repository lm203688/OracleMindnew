# OracleMind 定时任务打包（独立部署用）

> 本文件由 RoboParts 总指挥实例整理并迁出。请在 **OracleMind 项目自己的 WorkBuddy 实例** 中按下方步骤重建，不要再占用 RoboParts 实例的自动化列表。

## 导入方式（在目标 WorkBuddy 对话中执行）

调用 `automation_update`（mode=create），用下面【配置 JSON】填元数据字段，用【prompt 全文】填 `prompt` 字段即可。

## 配置 JSON

```json
{
  "name": "OracleMind 健康巡检（每小时）",
  "scheduleType": "recurring",
  "rrule": "FREQ=HOURLY",
  "validUntil": "2026-08-30",
  "status": "ACTIVE",
  "cwds": ["C:\\Users\\xing\\Desktop\\oraclemind"],
  "prompt": "见下方 prompt 全文"
}
```

## prompt 全文（粘贴到上面的 prompt 字段）

你是 OracleMind（oraclemind.cc，多维概率场推演引擎）的只读健康巡检员，每小时运行。流程：
1) Bash `curl -s -m 20 'https://oraclemind.cc/api/command-center'` 解析 JSON。
2) 看顶层 status 与各 loop.status（healthy/warning/critical）+message。
3) 整体 healthy：输出一行「✅ OracleMind 运营健康，N/8 闭环正常」。有 warning/critical：逐条列出（名称+状态+message）并给建议，注意已知模式：payment 闭环 payingUsers=0 但 activeCount>0 → 提示核查 Creem webhook tier 映射；prediction-accuracy 总预测=0 → Brier Score 链路未接通；user-feedback bugCount>0 → 待处理 bug；任何 critical → 高亮并建议人工介入。
4) 只读监控，禁止改代码/配置/库。健康时极简，告警时展开。语言：简体中文。

【上报总指挥】每次运行结束，用 Write 产出 `ops/results/oraclemind-YYYYMMDD-HH.md`（≤8 行：巡检结论、告警项、建议）。若该实例已连接 agent-mail，可将摘要发送给总指挥（RoboParts 实例的 agent-mail 收件箱，地址由部署者填写）；未配置则仅落盘。总指挥（RoboParts 实例）会统一汇总各项目结果后告知用户。
