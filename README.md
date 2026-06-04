# huoshan-jimeng-guide
# 🎨 即梦 AI 4.6 官方 API 小白教程

> 从拿到 AK/SK 到跑出第一张图，5 分钟。
> 踩坑实录：SDK 安装 / 签名报错 / base64 解码 / 50200 服务故障，全收录。

## 前置准备

| 你需要 | 在哪拿 |
|---|---|
| 🔑 Access Key | 火山引擎控制台 → 密钥管理 |
| 🔐 Secret Key | 同上 |
| 📦 免费额度 | 即梦 4.6 开通免费试用（200 张） |

## 第一步：安装 SDK ⚠️

```bash
# ✅ 正确姿势 — 两个都要装
pip install volcengine
pip install volcengine-python-sdk

# ❌ 网上的 [all] 后缀不要用，会缺模块
```

> 💡 安装卡住 = 没管理员权限。把命令发给有权限的人帮你跑。

## 第二步：跑起来

```python
from volcengine.visual.VisualService import VisualService
import time, base64

svc = VisualService()
svc.set_ak("YOUR_AK")
svc.set_sk("YOUR_SK")

# 提交
resp = svc.cv_sync2async_submit_task({
    "req_key": "jimeng_seedream46_cvtob",
    "prompt": "一只可爱的柴犬在樱花树下微笑，动漫风格",
    "width": 1728, "height": 2304,
})
task_id = resp["data"]["task_id"]

# 轮询
for _ in range(30):
    time.sleep(3)
    r = svc.cv_sync2async_get_result({
        "req_key": "jimeng_seedream46_cvtob",
        "task_id": task_id,
    })
    if r["data"]["status"] == "done":
        for i, b64 in enumerate(r["data"]["binary_data_base64"]):
            with open(f"output_{i+1}.png", "wb") as f:
                f.write(base64.b64decode(b64))
        break
```

## ⚠️ 踩坑速查

| 错误 | 原因 | 解法 |
|---|---|---|
| `ModuleNotFoundError: volcengine` | 基类没装 | `pip install volcengine` |
| `SignatureDoesNotMatch` | 手写签名 | 用 SDK，别手写 |
| `image_urls` 是空的 | 图片在 base64 里 | `binary_data_base64[]` |
| 每次只出一张 | `force_single` 默认 true | 多调几次 |
| Prompt 太长 → 50500 | 超 800 字符 | 精简到 500 以内 |
| 提交成功(10000)查报 50200 | **服务端挂了** | 换时间重试，非代码问题 |
| 积分不足 (1006) | SessionID 额度用完 | 等明天或切官方 API |

> 📖 完整错误表见 `troubleshooting/errors.txt`

## 三种调用方式

| 方式 | 难度 | 免费额度 |
|---|---|---|
| 🍪 SessionID Cookie | ⭐⭐⭐ | 每天 ~8 次 |
| 📄 AK/SK（本教程） | ⭐⭐ | 200 张 |
| 🔑 ARK Key | ⭐ | 200 次 |

## 心路历程

```
09:00  AK/SK 到手 → 以为像 OpenAI → ❌
10:00  手写 HMAC 签名 → 三种格式全跪 → 😤
10:30  SDK 分包黑洞 → 基类模块没装 → 🤯
11:00  alpha 手动 pip install volcengine → ✅
11:20  首张公主克洛伊 → 忘写 anime style → 真人大片 😂
11:40  梵高克洛伊 → 全链路绿灯 → 🎉
16:20  长 prompt → 50500 → prompt 精简后秒过
17:00  提交成功 → 查询 50200 → 火山引擎服务宕了
```

整整一上午跑通一个 API。你不需要重走这些路。

---

*写于 2026-06-04 | alpha（AK/SK + 手动安装） & sola（签名 + 文档）*
