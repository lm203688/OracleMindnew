# -*- coding: utf-8 -*-
"""真实 LLM 回填试点：取 seed 前 N 条，用 deepseek-v4-flash 预测概率，走 extractor+calibrator 链路。
用法: python backfill_pilot.py [N]  默认 5
"""
import json, sys, time, re, urllib.request, os

PROXY = "http://127.0.0.1:8788/v1/chat/completions"
MODEL = "deepseek-v4-flash"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
SEED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "backfill-events.seed.json")

SYSTEM = (
    "You are a probabilistic forecaster. Given a question about a future event, "
    "estimate the probability (0.0-1.0) that the event will occur as stated. "
    "Reply with ONLY a single number between 0.00 and 1.00. Do not explain."
)

def call_llm(question, timeout=60, retries=1):
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": question},
        ],
        "max_tokens": 20,
        "temperature": 0.7,
        "reasoning_effort": "none",
    }
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(PROXY, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json", "Authorization": "Bearer dummy"})
            t0 = time.time()
            r = urllib.request.urlopen(req, timeout=timeout)
            dt = time.time() - t0
            j = json.loads(r.read())
            return j["choices"][0]["message"]["content"].strip(), dt
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(3)
    raise last_err

def parse_prob(text):
    # 提取 0.00-1.00（独立小数 token，加数字边界防 "1.00" 匹配出 ".00"）或 0-100%
    m = re.search(r"(?<!\d)(1\.0+|0?\.\d{1,4})(?!\d)", text)
    if m:
        p = float(m.group(1))
        if 0 <= p <= 1:
            return p
    m = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", text)
    if m:
        p = float(m.group(1)) / 100.0
        if 0 <= p <= 1:
            return p
    return None

def main():
    d = json.load(open(SEED, encoding="utf-8"))
    events = d["events"]
    todo = [ev for ev in events if ev.get("predictedProbability") is None]
    print(f"总事件 {len(events)}，已回填 {len(events)-len(todo)}，待回填 {len(todo)}，本次处理前 {N} 条", flush=True)
    results = []
    ok = 0
    processed = 0
    for ev in todo[:N]:
        q = ev["question"]
        try:
            text, dt = call_llm(q)
            p = parse_prob(text)
            if p is None:
                print(f"[{ev['id']}] 解析失败: {text!r} ({dt:.1f}s)", flush=True)
                results.append({"id": ev["id"], "raw": text, "p": None, "latency": dt})
                continue
            print(f"[{ev['id']}] p={p:.2f} 来自 {text!r} ({dt:.1f}s)", flush=True)
            ev["predictedProbability"] = round(p, 4)
            results.append({"id": ev["id"], "raw": text, "p": p, "latency": dt})
            ok += 1
        except Exception as e:
            print(f"[{ev['id']}] ERR: {e}", flush=True)
            results.append({"id": ev["id"], "raw": None, "p": None, "latency": None})
        time.sleep(1)  # 轻微节流

        # 增量 checkpoint：每 10 条写回一次 seed，崩溃/中断不丢进度
        processed += 1
        if processed % 10 == 0:
            with open(SEED, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            done_now = sum(1 for x in d["events"] if x.get("predictedProbability") is not None)
            print(f"[checkpoint] 已写回 seed，累计 {done_now}/{len(d['events'])}", flush=True)

    # 最终写回 seed
    with open(SEED, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    avg_lat = [r["latency"] for r in results if r.get("latency")]
    print(f"\n完成：{ok}/{N} 成功，平均延迟 {sum(avg_lat)/len(avg_lat):.1f}s" if avg_lat else f"\n完成：{ok}/{N} 成功")
    print("已写回 seed 文件")

if __name__ == "__main__":
    main()
