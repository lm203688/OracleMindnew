# -*- coding: utf-8 -*-
"""回填续跑：只处理 predictedProbability 仍为 None 的事件，并对空响应/解析失败重试。

背景：backfill_pilot.py 只在「网络异常」时重试；LLM 代理返回空字符串（''）时
parse_prob 返回 None，但脚本不重试，导致 76 条事件漏填。
本脚本：跳过已填 + 对空/解析失败最多重试 3 次 + 每 5 条 checkpoint 写回。

用法: python backfill_resume.py
"""
import json, sys, time, re, urllib.request, os, random

PROXY = "http://127.0.0.1:8788/v1/chat/completions"
MODEL = "deepseek-v4-flash"
SEED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "backfill-events.seed.json")

SYSTEM = (
    "You are a probabilistic forecaster. Given a question about a future event, "
    "estimate the probability (0.0-1.0) that the event will occur as stated. "
    "Reply with ONLY a single number between 0.00 and 1.00. Do not explain."
)


def call_llm(question, timeout=45, retries=2):
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
            content = j["choices"][0]["message"]["content"].strip()
            # 空响应视为可重试的失败（不抛异常但返回 None 标记）
            if not content:
                last_err = Exception("empty content")
                if attempt < retries:
                    time.sleep(2 + random.random() * 3)
                    continue
                return "", dt
            return content, dt
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(2 + random.random() * 3)
    raise last_err


def parse_prob(text):
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
    print(f"总事件 {len(events)}，已回填 {len(events)-len(todo)}，本次续跑 {len(todo)} 条", flush=True)
    ok = 0
    fail = 0
    for i, ev in enumerate(todo):
        q = ev["question"]
        try:
            text, dt = call_llm(q)
            p = parse_prob(text)
            if p is None:
                print(f"[{ev['id']}] 重试后仍失败: {text!r} ({dt:.1f}s)", flush=True)
                fail += 1
                continue
            ev["predictedProbability"] = round(p, 4)
            print(f"[{ev['id']}] p={p:.2f} 来自 {text!r} ({dt:.1f}s)", flush=True)
            ok += 1
        except Exception as e:
            print(f"[{ev['id']}] ERR: {e}", flush=True)
            fail += 1
        # 每 5 条 checkpoint
        if (i + 1) % 5 == 0:
            with open(SEED, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            done_now = sum(1 for x in events if x.get("predictedProbability") is not None)
            print(f"[checkpoint] 累计 {done_now}/{len(events)}", flush=True)
        time.sleep(1)

    with open(SEED, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    done_now = sum(1 for x in events if x.get("predictedProbability") is not None)
    print(f"\n续跑完成：新增成功 {ok}，失败 {fail}，累计 {done_now}/{len(events)}", flush=True)
    if fail:
        print(f"⚠️ 仍有 {fail} 条未填（可能需要检查代理稳定性或换模型）", flush=True)


if __name__ == "__main__":
    main()
