"""
Real LLM prediction dry-run on 30 sampled questions.
Uses SenseNova proxy at 127.0.0.1:8788 (deepseek-v4-flash, non-thinking).
"""
import json
import math
import random
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

PROXY = "http://127.0.0.1:8788/v1/chat/completions"
MODEL = "deepseek-v4-flash"

PROMPT_TMPL = """You are a probabilistic forecaster. For each question below, output the probability (0.0-1.0) that the event as literally described will occur. Output ONLY a single number between 0.0 and 1.0, no explanation, no other text.

Question: {q}
Resolution date: {rd}
Category: {cat}

Your probability:"""

def predict(q, rd, cat, retries=3):
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT_TMPL.format(q=q, rd=rd, cat=cat)}],
        "max_tokens": 8,
        "temperature": 0.7,
        "reasoning_effort": "none",
    }
    data = json.dumps(body).encode()
    for i in range(retries):
        try:
            req = urllib.request.Request(
                PROXY, data=data,
                headers={"Content-Type": "application/json", "Authorization": "Bearer dummy"}
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                j = json.loads(r.read())
            text = j["choices"][0]["message"]["content"]
            # extract first number
            tok = ""
            for ch in text:
                if ch.isdigit() or ch == ".":
                    tok += ch
                elif tok:
                    break
            if not tok:
                continue
            p = float(tok)
            return max(0.01, min(0.99, p))
        except Exception as e:
            if i == retries - 1:
                return None
            time.sleep(1)
    return None

def main():
    with open("../data/backfill-events.seed.json", encoding="utf-8") as f:
        d = json.load(f)
    events = [e for e in d["events"] if e["outcome"] in ("positive", "negative")]
    random.seed(42)
    sample = random.sample(events, 30)

    print(f"Sampled {len(sample)} questions. Running {MODEL} predictions...")
    preds = [None] * len(sample)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {}
        for i, e in enumerate(sample):
            f = ex.submit(predict, e["question"], e["resolutionDate"], e["category"])
            futs[f] = i
        for f in as_completed(futs):
            i = futs[f]
            preds[i] = f.result()

    dt = time.time() - t0
    valid = [(p, 1 if sample[i]["outcome"] == "positive" else 0)
             for i, p in enumerate(preds) if p is not None]
    print(f"Predicted in {dt:.1f}s. Valid: {len(valid)}/{len(sample)}")

    # save raw
    with open("real_predictions.json", "w", encoding="utf-8") as f:
        json.dump([{"question": sample[i]["question"],
                    "outcome": sample[i]["outcome"],
                    "category": sample[i]["category"],
                    "horizonDays": sample[i]["horizonDays"],
                    "predicted": preds[i]}
                   for i in range(len(sample))], f, ensure_ascii=False, indent=2)

    if len(valid) < 10:
        print("Not enough valid predictions")
        return

    ys = [y for _, y in valid]
    ps = [p for p, _ in valid]
    print(f"\nPredictions: {['%.2f'%p for p in ps]}")
    print(f"Truths:      {ys}")
    print(f"Mean predicted: {sum(ps)/len(ps):.3f}, True rate: {sum(ys)/len(ys):.3f}")

    # ---- metrics ----
    def brier(): return sum((p-y)**2 for p, y in zip(ps, ys)) / len(ps)
    def logloss():
        return -sum((y*math.log(max(p,1e-6)) + (1-y)*math.log(max(1-p,1e-6))) for p, y in zip(ps, ys)) / len(ps)
    def ece(bins=10):
        tot, N = 0.0, len(ps)
        for i in range(bins):
            lo, hi = i/bins, (i+1)/bins
            idx = [j for j, p in enumerate(ps) if lo <= p < hi]
            if not idx: continue
            n = len(idx)
            tot += (n/N) * abs(sum(ps[j] for j in idx)/n - sum(ys[j] for j in idx)/n)
        return tot
    def acc(): return sum(1 for p, y in zip(ps, ys) if (p>=0.5) == (y==1)) / len(ps)

    # ---- temperature scaling ----
    def find_T():
        def bce(T):
            t = 0
            for p, y in zip(ps, ys):
                logit = math.log(max(p,1e-6)/max(1-p,1e-6))
                logit_t = logit / T
                pc = 1/(1+math.exp(-logit_t))
                pc = max(min(pc, 1-1e-6), 1e-6)
                t -= (y*math.log(pc) + (1-y)*math.log(1-pc))
            return t / len(ps)
        best_T, best_l = 1.0, float('inf')
        T = 0.3
        while T <= 3.0:
            l = bce(T)
            if l < best_l: best_T, best_l = T, l
            T += 0.05
        return best_T
    T = find_T()
    ps_cal = []
    for p in ps:
        logit = math.log(max(p,1e-6)/max(1-p,1e-6)) / T
        ps_cal.append(1/(1+math.exp(-logit)))

    print(f"\n{'Model':40s} | Brier | LogLoss | ECE | Acc")
    print("-"*70)
    print(f"{'Raw LLM predictions':40s} | {brier():.4f} | {logloss():.4f} | {ece():.4f} | {acc():.3f}")
    print(f"{'Temperature scaled (T='+f'{T:.2f})':40s} | {sum((p-y)**2 for p,y in zip(ps_cal,ys))/len(ps_cal):.4f} | {logloss() if False else sum(-(y*math.log(max(p,1e-6))+(1-y)*math.log(max(1-p,1e-6))) for p,y in zip(ps_cal,ys))/len(ps_cal):.4f} | {ece(ps=ps_cal):.4f} | {acc() if False else sum(1 for p,y in zip(ps_cal,ys) if (p>=0.5)==(y==1))/len(ps_cal):.3f}")

    def ece2(ps2):
        tot, N = 0.0, len(ps2)
        for i in range(10):
            lo, hi = i/10, (i+1)/10
            idx = [j for j, p in enumerate(ps2) if lo <= p < hi]
            if not idx: continue
            n = len(idx)
            tot += (n/N)*abs(sum(ps2[j] for j in idx)/n - sum(ys[j] for j in idx)/n)
        return tot
    print(f"\n校准前后 ECE: {ece():.4f} → {ece2(ps_cal):.4f}  (T={T:.2f})")

if __name__ == "__main__":
    main()
