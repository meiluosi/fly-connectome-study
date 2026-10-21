"""Registered analysis of stage 7 (PREREG_v4_stage7.md)."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(81); S=0.03; L=[]
KINDS=["real","shuffled","random","real_binary","real_wshuf","raw"]; MET=["acc_2shot","acc_5shot","retrieval"]
HEAD=[("acc_2shot","real","shuffled"),("acc_2shot","real","random"),("acc_5shot","real","shuffled"),("acc_5shot","real","random"),("retrieval","real","shuffled"),("retrieval","real","random")]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def load(k,m): return np.array([json.load(open(os.path.join(HERE,"results_i",f"{k}__{s}.json")))[m] for s in range(5000,5100)])
def ci(d,lev,n=10000):
    d=np.asarray(d,float); b=d[rng.integers(0,len(d),(n,len(d)))].mean(1); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(b,[a,100-a])]
def tier(m,lo,hi):
    if lo>0 or hi<0: return "small-real" if abs(m)<S else ("meaningful-strict" if min(abs(lo),abs(hi))>=S else "meaningful (边缘)")
    return "equivalent" if (lo>-S and hi<S) else "uncertain"
P("# 结果（第四阶段 7：自然气味统计上的表示层检验，自动生成）\n\nDoOR 2.0 的 301 个气味分子 × 65 个嗅小球响应；T1 = 9 个化学类别的少样本最近质心分类（平衡准确率），T2 = 150 个气味的 5 近邻在 KC 编码与 DoOR 空间之间的重合比例。三档判定 s = 0.03；主结论族（★，6 个）99.2% 区间，其余 95%；100 个世界（种子 5000–5099）。随机水平约 0.11（T1）。\n")
P("| 表示 | 2-shot 准确率 | 5-shot 准确率 | 近邻重合 |\n|---|---|---|---|")
for k in KINDS: P(f"| {k} | "+" | ".join(f"{load(k,m).mean():.3f}" for m in MET)+" |")
P("\n配对差：")
for m in MET:
    for a,b in (("real","shuffled"),("real","random"),("real","real_binary"),("real","real_wshuf"),("real","raw"),("random","shuffled")):
        h=(m,a,b) in HEAD; mm,lo,hi=ci(load(a,m)-load(b,m),99.2 if h else 95); P(f"- {'★' if h else ''}{m}: {a} − {b} = {mm:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(mm,lo,hi)}**")
open(os.path.join(HERE,"RESULTS_v4_stage7.md"),"w").write("\n".join(L)+"\n")
