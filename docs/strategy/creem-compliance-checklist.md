# Creem 收尾清单（OracleMind 独立新店 + 恢复 SwarmLabs）

> 状态：我侧全部代码 + 商品 + 商店分离已完成（commit `39e82f1` 已 push）。**仅剩你一步：在 Vercel Dashboard 更新环境变量 + 重部署**。

---

## ✅ 已完成（我侧，API + 代码）
- [x] **恢复 SwarmLabs×2**（FrontierKB 活跃商品）：
  - SwarmLabs Standard Pack — 500 Credits → `prod_1ocNX0SaHRp3BWJMmGsHZf`
  - SwarmLabs Starter Pack — 100 Credits → `prod_60dCG1Pjbs3yc0RGS7LzXQ`
- [x] 你已在 Dashboard 建好 OracleMind 新店 + 配 webhook，并发来 Key/Secret
- [x] **新店建 3 个 OracleMind 商品**（key=`creem_7b9D0NEZhsuy3JC6wrMyrN`，已复核 active）：
  - Deep Analysis $4.99 onetime → `prod_7YycAgL3PP058KroOmZKYa`
  - Premium Monthly $9.99/mo → `prod_gq5tn9v0RzkKZbBOyhEPE`
  - Premium Yearly $99/yr → `prod_3YeioVJhK3rTsT24Ao1MzK`
- [x] 代码 7 文件 26 处商品 ID 全部改新 → `tsc` 通过 → commit `39e82f1` push master（Vercel 自动构建）
- [x] **归档 FrontierKB 旧 3 个 OracleMind 商品** → 商店分离彻底完成：
  - 新 OracleMind 店：仅 3 个 OracleMind 商品（active）
  - FrontierKB 店：仅 SwarmLabs×2 + 其他项目商品

## 🔲 仅剩你一步：Vercel 环境变量更新 + 重部署（约 2 分钟）
打开 **https://vercel.com/team_dbopiTcCVu7hCeA2t4MKRA69/oraclemind** → **Settings → Environment Variables**

1. `CREEM_API_KEY` → 改为 `creem_7b9D0NEZhsuy3JC6wrMyrN`
2. `CREEM_WEBHOOK_SECRET` → 改为 `whsec_6c7iJuTYovGu4e3HScYpyQ`
3. 进 **Deployments** → 最新一条 → ⋮ → **Redeploy**（让新代码新商品ID + 新凭证同时生效）

## 🔍 你做完喊我，我立刻复验
- [ ] `command-center` 状态（预期 system-health 仍 healthy；付费闭环通后整体转 healthy）
- [ ] 测试支付后账户 tier 是否升级（`/api/payment/verify` 登录态）
- [ ] Vercel Functions `[Webhook]` 日志出现成功行

## ⚠️ 仍属 Creem 账户层的（可选，不影响 OracleMind 结账）
- 账户级 "Account Rejected / 支持邮箱 mismatch" 需你在 Creem Dashboard 把账户支持邮箱对齐 + 提交 re-review：
  https://docs.creem.io/merchant-of-record/account-reviews/account-reviews
- 随 OracleMind 移入正确注册(oraclemind.cc)的独立新店，「unregistered traffic」根因已解。

---
### 备注
- 新店 3 商品 ID 已与代码硬编码值一致；Vercel env 更新 + Redeploy 后，结账事件将由新店签名、webhook 用新 secret 校验通过。
- 0 付费不会因这步凭空消失——它让"付费→自动升级"闭环跑通；一旦有人付费，tier 自动升级，`command-center` 转 healthy。
