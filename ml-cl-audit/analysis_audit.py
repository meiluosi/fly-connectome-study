"""Applies the decision rules of PREREG_audit.md, with the corrections listed in DEVIATIONS.md (2026-10-08):
 - comparators (best prototype baseline, best backprop baseline) are chosen on VALIDATION finals, not test means;
 - H1 wording: 'dominated by' vs 'comparable' vs 'exceeds' (equivalence is never tested);
 - H2 pairs seeds by seed id; exploratory representation x classifier contrasts are reported separately;
 - H3 is reported per stream (class-ordered = registered; interleaved = pre-declared extension) and marked INCOMPLETE if any benchmark or baseline is missing.
Reads results/<bench>/*.json (one file per key); writes RESULTS_audit_auto.md."""
import json, glob, os, numpy as np
rng = np.random.default_rng(2026); L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)
BENCH = ["mnist20", "cifar100", "cifar100_224"]
LABEL = {"mnist20": "MNIST-20", "cifar100": "CIFAR-100-A (32x32 特征)", "cifar100_224": "CIFAR-100-B (224x224 特征)"}
def load(b):
    out = {}
    for f in glob.glob(f"results/{b}/*.json"):
        d = json.load(open(f)); out[d["key"]] = d["value"]
    return out
def collect(c):
    """name -> {seed: value}; key format test|<name>[|tag...]|<hp json>|s<seed>"""
    out = {}
    for k, v in c.items():
        if not k.startswith("test|"): continue
        parts = k.split("|"); seed = int(parts[-1][1:]) if parts[-1][1:].isdigit() else 0; name = "|".join(parts[1:-2])
        out.setdefault(name, {})[seed] = v
    return out
def val_final(c, name):
    hp = c.get(f"best|{name}")
    if hp is None: return None
    v = c.get(f"val|{name}|{json.dumps(hp)}|s0"); return None if v is None else v["final"]
def mf(m): return float(np.mean([v["final"] for v in m.values()]))
def boot_ci(d, n=4000):
    d = np.asarray(d); m = np.array([d[rng.integers(0, len(d), len(d))].mean() for _ in range(n)]); return float(d.mean()), float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))
def paired(a, b): ks = sorted(set(a) & set(b)); return [a[k]["final"] - b[k]["final"] for k in ks]
V = {"H1": [], "H3": {"": [], "|inter": []}}
ALL = {b: (load(b)) for b in BENCH}
for b in BENCH:
    c = ALL[b]; R = collect(c)
    if not R: P(f"\n## {LABEL[b]}\n(无结果)"); continue
    P(f"\n## {LABEL[b]}")
    P("| 方法 | 种子数 | 最终准确率 | 学习时准确率 A_jj | memory loss |\n|---|---|---|---|---|")
    order = ["Fly_F0", "Fly_F1", "Fly_dense_l2", "Fly_dense_minmax", "NCM_euclid", "NCM_cos", "ClassSumDot", "SLDA", "B1_vanilla", "B2_ewc", "B3_er200", "B3_er1000",
             "B1_vanilla|inter", "B2_ewc|inter", "B3_er200|inter", "B3_er1000|inter", "B4_offline", "Fly_dense_l2_noclip", "Fly_wta_noclip", "ExpNCM_wta_euc", "ExpNCM_wta_cos", "ExpNCM_dense_euc", "ExpNCM_dense_cos"]
    for n in order + [k for k in R if k not in order]:
        if n not in R: continue
        m = R[n]; fin = [v["final"] for v in m.values()]; la = [v.get("learn", float("nan")) for v in m.values()]; ml = [v.get("memloss", float("nan")) for v in m.values()]
        tag = "（探索性）" if (n.endswith("noclip") or n.startswith("ExpNCM")) else ("（交错流，预先声明的扩展）" if n.endswith("|inter") else "")
        P(f"| {n}{tag} | {len(m)} | {np.mean(fin):.4f} ± {np.std(fin):.4f} | {np.nanmean(la):.4f} | {np.nanmean(ml):.4f} |")
    # H1: comparator chosen on validation
    protos = {n: val_final(c, n) for n in ["NCM_euclid", "NCM_cos", "ClassSumDot", "SLDA"]}; protos = {n: v for n, v in protos.items() if v is not None and n in R}
    if "Fly_F0" in R and protos:
        bestP = max(protos, key=protos.get); tb = mf(R[bestP]); f0 = [v["final"] for v in R["Fly_F0"].values()]; delta = float(np.mean(f0)) - tb
        v1 = "被免回放原型基线超过" if delta <= -0.02 else ("与原型基线相当(±0.02)" if delta < 0.02 else ("超过原型基线" if np.median(f0) > tb else "混合"))
        V["H1"].append(v1); extra = ""
        if "Fly_F1" in R: extra = f"；F1(验证集调参) − best_P = {mf(R['Fly_F1'])-tb:+.4f}"
        P(f"\nH1 [{b}]: best_P(按验证集)={bestP}，测试 {tb:.4f}；F0 − best_P = {delta:+.4f} → **{v1}**{extra}")
    # H2 (registered) and exploratory
    if "Fly_F0" in R and "Fly_dense_l2" in R:
        d = paired(R["Fly_F0"], R["Fly_dense_l2"]); mm, lo, hi = boot_ci(d)
        v2 = "WTA 稀疏有价值(登记的对照下)" if (mm >= 0.02 and lo > 0) else ("无实质价值" if (lo > -0.02 and hi < 0.02) else "不确定")
        f2b = np.mean(paired(R["Fly_F0"], R["Fly_dense_minmax"])) if "Fly_dense_minmax" in R else float("nan")
        P(f"H2 [{b}]（登记）: F0 − F2(稠密+L2，类和点积) = {mm:+.4f} [{lo:+.4f},{hi:+.4f}] → **{v2}**；F0 − F2b = {f2b:+.4f}（F2b 是随机水平，见审查：饱和使全部权重为 1）")
    for a_, b_, lab in [("ExpNCM_wta_euc", "ExpNCM_dense_euc", "欧氏"), ("ExpNCM_wta_cos", "ExpNCM_dense_cos", "余弦")]:
        if a_ in R and b_ in R:
            d = paired(R[a_], R[b_]); mm, lo, hi = boot_ci(d); P(f"   探索性：同一最近类均值分类器下，稀疏(WTA) − 稠密（{lab}）= {mm:+.4f} [{lo:+.4f},{hi:+.4f}]")
    # H3 per stream
    for tag, lab in [("", "类内顺序流（登记）"), ("|inter", "任务内交错流（预先声明的扩展）")]:
        names = [f"B1_vanilla{tag}", f"B2_ewc{tag}", f"B3_er200{tag}"]; have = [n for n in names if n in R and len(R[n]) >= 5]
        if "Fly_F0" in R and len(have) == 3:
            bps = {n: val_final(c, n) for n in names}
            if all(v is not None for v in bps.values()):
                bb = max(bps, key=bps.get); delta = mf(R["Fly_F0"]) - mf(R[bb]); ok = delta >= 0.05; V["H3"][tag].append(ok)
                P(f"H3 [{b}] {lab}: best_BP(按验证集)={bb}，测试 {mf(R[bb]):.4f}；F0 − best_BP = {delta:+.4f} → **{'成立' if ok else '不成立'}**（门槛 0.05；ER(1000)：{mf(R['B3_er1000'+tag]) if 'B3_er1000'+tag in R else float('nan'):.4f}）")
                continue
        V["H3"][tag].append(None); P(f"H3 [{b}] {lab}: **未完成**（缺少 {[n for n in names if n not in R or len(R[n])<5]}）")
    if "B4_offline" in R: P(f"   （另报）离线上界 = {mf(R['B4_offline']):.4f}")
P("\n## 总判定")
if len(V["H1"]) == 3:
    v = V["H1"]; P("H1:", v, "→", "FlyModel 被免回放原型基线超过（三个基准一致）" if all(x.startswith("被") for x in v) else "超过原型基线（三个基准一致）" if all(x == "超过原型基线" for x in v) else "混合")
else: P("H1: 基准结果不全", V["H1"])
for tag, lab in [("", "类内顺序流"), ("|inter", "任务内交错流")]:
    h = V["H3"][tag]; P(f"H3 [{lab}]:", h, "→", "未完成（有基准缺失）" if (len(h) < 3 or any(x is None for x in h)) else ("公平调参下仍成立" if all(h) else "不全成立"))
open("RESULTS_audit_auto.md", "w").write("\n".join(L)); print("written")
