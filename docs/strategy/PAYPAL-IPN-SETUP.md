# PayPal 后台开启 IPN 操作指南（OracleMind）

> 目的：让 PayPal 在每笔付款完成后，自动向我们服务器 `https://oraclemind.cc/api/payment/paypal/ipn` 发一条回执（IPN），由系统校验后**自动开通用户权限**。
> 收款账号：`463102527@qq.com`（已配入 `PAYPAL_RECEIVER_EMAIL` 生产环境变量）

---

## 关键事实（先读）

- 我们的结账链接**每笔都自带 `notify_url`**（代码已写死 `https://oraclemind.cc/api/payment/paypal/ipn`）。所以即使后台不单独开，PayPal 也会按这笔付款的 notify_url 发回执。
- 但官方要求：**IPN 功能整体必须处于"开启接收"状态**，否则可能不发。所以后台这一步必须做，作为兜底 + 保证手动/历史付款也能回调。
- 后台填的通知 URL 与 checkout 里的 `notify_url` 用**同一个**：`https://oraclemind.cc/api/payment/paypal/ipn`

---

## 方式一：直接点链接（最快）

1. 登录 PayPal：https://www.paypal.com/signin （用 `463102527@qq.com`）
2. 点这个直达链接（经典版 IPN 设置页）：
   https://www.paypal.com/cgi-bin/webscr?cmd=_profile-ipn-notify
3. 若上一条打不开/空白，用新版商家后台：
   https://www.paypal.com/businessmanage/preferences/instant-payment-notifications

---

## 方式二：从界面一步步导航（中文界面）

1. 用 `463102527@qq.com` 登录 https://www.paypal.com
2. 右上角点 **齿轮 ⚙ 设置（Settings）** 或 **账户设置**
3. 在设置页左侧菜单找 **"通知"（Notifications）** —— 没有就找 **"网站付款" / "销售工具" / "网站偏好设置"**
4. 找到 **"即时付款通知（Instant Payment Notification，简称 IPN）"** → 点右侧 **"更新（Update）"**
5. 选择 **"接收 IPN 消息（推荐）" / Receive IPN messages (Recommended)**
6. 在 **"通知 URL（Notification URL）"** 框里填：
   ```
   https://oraclemind.cc/api/payment/paypal/ipn
   ```
7. 点 **"保存（Save）"**

> 若你的界面是老版（个人账号常见），路径为：
> 设置 → **网站付款销售工具** → **即时付款通知** → 点击"更新" → 勾选"接收 IPN 消息" → 填上面的 URL → 保存。

---

## 开启后如何验证（确认真的通了）

**方式 A — 真实测试支付（推荐，零代码）**
1. 在 OracleMind 定价页点 "Pay with PayPal"，买一笔 **Deep Analysis（$4.99）** 或 **Credits ×30（$4.99）**。
2. 用另一个 PayPal 账号（或同一账号付给自己也行，真实付款即可）完成支付。
3. PayPal 自动发 IPN 回执 → 系统校验 VERIFIED → 自动 `grantCredits` / 升级订阅层级。
4. 在你自己的账号查：订阅层级变化、积分到账；或在 `/api/command-center`（公开可读）看支付统计。

**方式 B — 后台发测试 IPN（可选）**
部分账号在 IPN 设置页有 "IPN 历史记录 / 重新发送" 功能，可手动选一笔历史交易重发，观察我们服务器是否收到（需服务器日志确认，普通用户不易看，故优先用方式 A）。

---

## 完成状态自检

- [ ] 后台 IPN 状态 = "已开启 / Receiving"
- [ ] 通知 URL = `https://oraclemind.cc/api/payment/paypal/ipn`
- [ ] 用一笔 $4.99 测试支付走完，权限自动开通

---

## 注意事项

- **个人账号也能用 IPN**（PayPal Payments Standard + IPN 是个人号支持的，不强制商业号）。若界面死活找不到 IPN 入口，可把账号升级为"商业账号（Business）"——个人号收外币有时也建议升商业号以免风控。
- IPN 回执是 **POST 明文 HTTP 表单**，我们服务器会回 PayPal 做 `cmd=_notify-validate` 二次校验，伪造回执会被拒绝（已 3/3 验证），所以安全。
- 通知 URL 必须是 **公网可达的 https**，我们的 `oraclemind.cc` 已满足。
- 不要在这里填任何带端口、localhost、或带 query 参数的地址。
