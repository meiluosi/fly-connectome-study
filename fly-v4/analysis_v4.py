"""Registered analysis of stage 0 (PREREG_v4_stage0.md). Three-tier verdict, s = 0.03 accuracy points."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(71); S=0.03; L=[]
TASKS=["teacher_real","teacher_random","linear_teacher","family","door_class","door_teacher_real"]; KINDS=["real","shuffled","random","real_binary","real_wshuf","linear","real+ad","shuffled+ad","random+ad"]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def ci(d,lev=95,n=4000):
    d=np.asarray(d,float); m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(m,[a,100-a])]
def tier(m,lo,hi): 
    if lo>0 or hi<0: return "meaningful" if abs(m)>=S else "small-real"
    return "equivalent" if (lo>-S and hi<S) else "uncertain"
def load(task,kind,metric):
    return np.array([json.load(open(os.path.join(HERE,"results",f"{task}__{kind}__{s}.json")))[metric] for s in range(5000,5100)])
HEAD=[("teacher_real","real","shuffled"),("teacher_real","real","random"),("linear_teacher","linear","real"),("door_class","real","random"),("door_teacher_real","real","random"),("door_class","real+ad","random+ad"),("door_teacher_real","real+ad","random+ad")]
P("# 结果（第四阶段 0，自动生成）\n\n三档判定，s = 0.03（准确率点）；主结论族（★）99.3% 区间，其余 95%。每个任务 100 个测试世界（种子 5000–5099）。\n")
for t in TASKS:
    P(f"\n## {t}\n| 学习器 | auc（样本效率） | 50 次后 | 最终 | 输入噪声下 | 沉默 20% KC 下 | auc 的世界间 SD |\n|---|---|---|---|---|---|---|")
    for k in KINDS:
        try: A={m:load(t,k,m) for m in ("auc","acc50","final","noisy","silenced")}
        except Exception: continue
        P(f"| {k} | "+" | ".join(f"{A[m].mean():.3f}" for m in ("auc","acc50","final","noisy","silenced"))+f" | {A['auc'].std():.3f} |")
    P("\n配对差（auc；A − B）：")
    pairs=[("real","shuffled"),("real","random"),("real","real_binary"),("real","real_wshuf"),("real","linear"),("linear","random"),("real+ad","random+ad"),("real+ad","shuffled+ad"),("real+ad","real"),("random+ad","random"),("shuffled+ad","shuffled")]
    for a,b in pairs:
        try: d=load(t,a,"auc")-load(t,b,"auc")
        except Exception: continue
        head=(t,a,b) in HEAD; m,lo,hi=ci(d,99.3 if head else 95); P(f"- {'★' if head else ''}{a} − {b}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**")
    for met in ("acc50","noisy","silenced"):
        try: d=load(t,"real",met)-load(t,"random",met)
        except Exception: continue
        m,lo,hi=ci(d); P(f"- （{met}）real − random: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → {tier(m,lo,hi)}")
# gate
def v(t,a,b,lev=99.3): d=load(t,a,"auc")-load(t,b,"auc"); m,lo,hi=ci(d,lev); return m,lo,hi,tier(m,lo,hi)
g1=v("teacher_real","real","shuffled"); g2=v("teacher_real","real","random"); g3=v("linear_teacher","linear","real"); n1=v("teacher_random","real","random")
ok=lambda g:(g[3]=="meaningful" and g[0]>0)
P("\n## 门槛（阳性对照）")
P(f"- teacher_real: real − shuffled → {g1[3]}（{g1[0]:+.3f}）；real − random → {g2[3]}（{g2[0]:+.3f}）")
P(f"- linear_teacher: linear − real → {g3[3]}（{g3[0]:+.3f}）")
P(f"- teacher_random（阴性）: real − random → {n1[3]}（{n1[0]:+.3f}）；不应为 real 更好 meaningful")
P("- **门槛："+("通过" if (ok(g1) and ok(g2) and ok(g3) and not (n1[3]=="meaningful" and n1[0]>0)) else "未通过")+"**")
open(os.path.join(HERE,"RESULTS_v4_stage0.md"),"w").write("\n".join(L)+"\n")
