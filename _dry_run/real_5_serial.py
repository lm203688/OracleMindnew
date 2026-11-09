"""5-question serial run to validate LLM behavior is actually overconfident."""
import json, math, time, random, urllib.request

PROXY = "http://127.0.0.1:8788/v1/chat/completions"
MODEL = "deepseek-v4-flash"

PROMPT = """You are a probabilistic forecaster. Output the probability (0.0-1.0) that the event as literally described will occur. Reply with ONLY a single number, no explanation.

Question: {q}
Category: {cat}

Your probability:"""

def predict(q, cat):
    body = {"model": MODEL,
            "messages": [{"role": "user", "content": PROMPT.format(q=q, cat=cat)}],
            "max_tokens": 8, "temperature": 0.7, "reasoning_effort": "none"}
    req = urllib.request.Request(PROXY, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer dummy"})
    with urllib.request.urlopen(req, timeout=90) as r:
        j = json.loads(r.read())
    text = j["choices"][0]["message"]["content"]
    tok = ""
    for ch in text:
        if ch.isdigit() or ch == ".": tok += ch
        elif tok: break
    return float(tok) if tok else None

def main():
    with open("../data/backfill-events.seed.json", encoding="utf-8") as f:
        d = json.load(f)
    events = [e for e in d["events"] if e["outcome"] in ("positive", "negative")]
    random.seed(7)
    sample = random.sample(events, 5)

    print(f"Running {MODEL} on 5 questions serially...\n")
    rows = []
    for i, e in enumerate(sample):
        t0 = time.time()
        p = predict(e["question"], e["category"])
        dt = time.time() - t0
        y = 1 if e["outcome"] == "positive" else 0
        rows.append((p, y, e["category"], e["question"][:80], dt))
        print(f"[{i+1}/5] {dt:5.1f}s  p={p}  y={y}  cat={e['category']:10s}  {e['question'][:70]}...")

    ps = [r[0] for r in rows]
    ys = [r[1] for r in rows]
    print(f"\nmean_p={sum(ps)/len(ps):.3f}  true_rate={sum(ys)/len(ys):.3f}")
    print(f"brier={sum((p-y)**2 for p,y in zip(ps,ys))/len(ps):.4f}")

    # temp scale
    def bce(T):
        t = 0
        for p, y in zip(ps, ys):
            li = math.log(max(p,1e-6)/max(1-p,1e-6)) / T
            pc = 1/(1+math.exp(-li))
            pc = max(min(pc, 1-1e-6), 1e-6)
            t -= y*math.log(pc) + (1-y)*math.log(1-pc)
        return t/len(ps)
    best_T, best_l = 1.0, float('inf')
    T = 0.3
    while T <= 3.0:
        l = bce(T)
        if l < best_l: best_T, best_l = T, l
        T += 0.05
    print(f"\nOptimal T={best_T:.2f}  (raw bce={bce(1.0):.4f}  scaled bce={best_l:.4f})")

    with open("real_5.json", "w", encoding="utf-8") as f:
        json.dump([{"p": r[0], "y": r[1], "cat": r[2], "q": r[3]} for r in rows], f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
