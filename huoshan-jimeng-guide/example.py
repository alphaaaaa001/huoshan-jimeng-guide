"""即梦 4.6 API 开箱即用
改 PROMPT → 填 AK/SK → 跑！
"""
from volcengine.visual.VisualService import VisualService
import time, base64

AK = "YOUR_AK"
SK = "YOUR_SK"
PROMPT = "A cute shiba inu smiling under cherry blossoms, anime style"
WIDTH, HEIGHT = 1728, 2304

svc = VisualService()
svc.set_ak(AK)
svc.set_sk(SK)

print(f"[Submit] {PROMPT[:60]}...")
resp = svc.cv_sync2async_submit_task({
    "req_key": "jimeng_seedream46_cvtob",
    "prompt": PROMPT, "width": WIDTH, "height": HEIGHT,
})
tid = resp["data"]["task_id"]
print(f"[TaskID] {tid}")

for i in range(30):
    time.sleep(3)
    r = svc.cv_sync2async_get_result({
        "req_key": "jimeng_seedream46_cvtob", "task_id": tid,
    })
    if r["data"]["status"] == "done":
        for idx, b64 in enumerate(r["data"]["binary_data_base64"]):
            fname = f"output_{idx+1}.png"
            with open(fname, "wb") as f:
                f.write(base64.b64decode(b64))
            print(f"[Saved] {fname}")
        break
    if i % 10 == 0:
        print(f"  waiting... ({(i+1)*3}s)")
