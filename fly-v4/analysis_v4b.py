"""Registered analysis of stage 0b (PREREG_v4_stage0b.md). Three-tier verdict, s = 0.03; strict flag = CI lower bound also >= s."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(71); S=0.03; L=[]
TASKS=["teacher_pert","teacher_shuf","teacher_real","teacher_random","linear_teacher","door_class","door_teacher_real"]; KINDS=["real","shuffled","random","real_binary","real_wshuf","linear"]
HEAD=[("teacher_pert","real","shuffled"),("teacher_pert","real","random"),("teacher_shuf","shuffled","random"),("teacher_shuf","shuffled","real"),("door_class","real","random"),("door_class","real","shuffled")]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def ci(d,lev,n=10000):
    d=np.asarray(d,float); m=d[rng.integers(0,len(d),(n,len(d)))].mean(1); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(m,[a,100-a])]
def tier(m,lo,hi):
    if lo>0 or hi<0:
        if abs(m)<S: return "small-real"
        return "meaningful-strict" if min(abs(lo),abs(hi))>=S else "meaningful (边缘)"
    return "equivalent" if (lo>-S and hi<S) else "uncertain"
def load(t,k,metric): return np.array([json.load(open(os.path.join(HERE,"results_b",f"{t}__{k}__{s}.json")))[metric] for s in range(5000,5100)])
def head(t,a,b): d=load(t,a,"auc")-load(t,b,"auc"); m,lo,hi=ci(d,99.2); return m,lo,hi,tier(m,lo,hi)
P("# 结果（第四阶段 0b，自动生成）\n\n三档判定，s = 0.03；主结论族（★，6 个）99.2% 区间，其余 95%；100 个测试世界（种子 5000–5099）。\n")
for t in TASKS:
    P(f"\n## {t}\n| 学习器 | auc | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |\n|---|---|---|---|---|---|---|")
    for k in KINDS:
        A={m:load(t,k,m) for m in ("auc","acc50","final","noisy","silenced")}; f=lambda m:"—" if np.isnan(A[m]).any() else f"{A[m].mean():.3f}"
        P(f"| {k} | "+" | ".join(f(m) for m in ("auc","acc50","final","noisy","silenced"))+f" | {A['auc'].std():.3f} |")
    P("\n配对差（auc；A − B）：")
    for a,b in [("real","shuffled"),("real","random"),("shuffled","random"),("real","real_binary"),("real","real_wshuf"),("real","linear"),("linear","random")]:
        d=load(t,a,"auc")-load(t,b,"auc"); h=(t,a,b) in HEAD or ((t,b,a) in HEAD and False); m,lo,hi=ci(d,99.2 if (t,a,b) in HEAD else 95); P(f"- {'★' if (t,a,b) in HEAD else ''}{a} − {b}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**")
    for met in ("acc50","noisy","silenced"):
        try: d=load(t,"real",met)-load(t,"random",met)
        except Exception: continue
        m,lo,hi=ci(d,95); P(f"- （{met}）real − random: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → {tier(m,lo,hi)}")
g1=head("teacher_pert","real","shuffled"); g2=head("teacher_pert","real","random"); g3=head("teacher_shuf","shuffled","random"); g4=head("teacher_shuf","shuffled","real")
m=lambda g:g[3].startswith("meaningful") and g[0]>0
A=m(g1) and m(g2); B=m(g3) or m(g4)
P("\n## 门槛（非循环阳性对照）")
P(f"- 对比 1 teacher_pert real − shuffled: {g1[0]:+.3f} [{g1[1]:+.3f}, {g1[2]:+.3f}] → {g1[3]}")
P(f"- 对比 2 teacher_pert real − random: {g2[0]:+.3f} [{g2[1]:+.3f}, {g2[2]:+.3f}] → {g2[3]}")
P(f"- 对比 3 teacher_shuf shuffled − random: {g3[0]:+.3f} [{g3[1]:+.3f}, {g3[2]:+.3f}] → {g3[3]}")
P(f"- 对比 4 teacher_shuf shuffled − real: {g4[0]:+.3f} [{g4[1]:+.3f}, {g4[2]:+.3f}] → {g4[3]}")
P(f"- **门槛 A（连线实例检出）：{'通过' if A else '未通过'}；门槛 B（统计类别检出）：{'通过' if B else '未通过'}**")
P("- door_class 解读规则见 PREREG：A、B 都通过→等价可解读为无优势；A 通过 B 不通过→只说无实例层面优势；A 不通过→不解读。")
open(os.path.join(HERE,"RESULTS_v4_stage0b.md"),"w").write("\n".join(L)+"\n")
