"""Registered analysis of stage 5 (PREREG_v4_stage5.md)."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(76); S=0.03; L=[]
TASKS=["door_class","door_teacher_real"]; KINDS=["real","shuffled","random"]; DOSES=(102,409,818)
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
R={(t,k):[json.load(open(os.path.join(HERE,"results_f",f"{t}__{k}__{s}.json"))) for s in range(5000,5100)] for t in TASKS for k in KINDS}
def col(t,k,m): return np.array([r[m] for r in R[(t,k)]])
def drop(t,k,when,name,m): return col(t,k,"intact")-col(t,k,f"{when}_{name}_{m}")     # accuracy lost
def ci(d,lev,n=10000):
    d=np.asarray(d,float); b=d[rng.integers(0,len(d),(n,len(d)))].mean(1); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(b,[a,100-a])]
def tier(m,lo,hi):
    if lo>0 or hi<0: return "small-real" if abs(m)<S else ("meaningful-strict" if min(abs(lo),abs(hi))>=S else "meaningful (边缘)")
    return "equivalent" if (lo>-S and hi<S) else "uncertain"
# headline family: (id, label, function returning per-world differences)
def ex(t,k,when,name,m): return drop(t,k,when,name,m)-drop(t,k,when,"random",m)       # excess accuracy lost vs random lesion of the same size
H=[("1","door_teacher_real real：post-hoc，active 409 的超额损失",lambda:ex("door_teacher_real","real","post","active",409)),
   ("2","door_teacher_real real：post-hoc，active 818 的超额损失",lambda:ex("door_teacher_real","real","post","active",818)),
   ("3","door_teacher_real real：post-hoc，hub 818 的超额损失",lambda:ex("door_teacher_real","real","post","hub",818)),
   ("4","door_teacher_real：active 409 超额损失，real − shuffled",lambda:ex("door_teacher_real","real","post","active",409)-ex("door_teacher_real","shuffled","post","active",409)),
   ("5","door_teacher_real：active 409 超额损失，real − random 连线",lambda:ex("door_teacher_real","real","post","active",409)-ex("door_teacher_real","random","post","active",409)),
   ("6","door_class real：post-hoc，active 409 的超额损失",lambda:ex("door_class","real","post","active",409)),
   ("7","door_class real：post-hoc，active 818 的超额损失",lambda:ex("door_class","real","post","active",818)),
   ("8","door_teacher_real real：训练前移除，active 409 的超额损失",lambda:ex("door_teacher_real","real","pre","active",409))]
P("# 结果（第四阶段 5：KC 类别的定向病变，自动生成）\n\n学习率固定 0.05；剂量 = 沉默的 KC 数（102 / 409 / 818 ≈ 5% / 20% / 40%）；“损失”= 完整时准确率 − 病变后准确率；“超额”= 排序病变的损失 − 同样数量随机病变的损失。三档判定，s = 0.03；主结论族（★，8 个）99.4% 区间，其余 95%；100 个测试世界（种子 5000–5099）。\n")
P("## 主结论族\n")
for i,lab,f in H: m,lo,hi=ci(f(),99.4); P(f"- ★{i}. {lab}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**")
for t in TASKS:
    P(f"\n## {t}\n\n完整准确率：" + "，".join(f"{k} {col(t,k,'intact').mean():.3f}" for k in KINDS))
    P("\n| 连线 | 时机 | 排序 | 损失（102） | 损失（409） | 损失（818） |\n|---|---|---|---|---|---|")
    for k in KINDS:
        for when,wl in(("post","测试时沉默"),("pre","训练前移除")):
            for name in("hub","active","random"): P(f"| {k} | {wl} | {name} | "+" | ".join(f"{drop(t,k,when,name,m).mean():+.3f}" for m in DOSES)+" |")
    P("\n超额损失（排序 − 随机，95% 区间）：")
    for k in KINDS:
        for when in("post","pre"):
            for name in("hub","active"):
                for m in DOSES:
                    mm,lo,hi=ci(ex(t,k,when,name,m),95); P(f"- {k} / {when} / {name} / {m}: {mm:+.3f} [{lo:+.3f}, {hi:+.3f}] → {tier(mm,lo,hi)}")
open(os.path.join(HERE,"RESULTS_v4_stage5.md"),"w").write("\n".join(L)+"\n")
