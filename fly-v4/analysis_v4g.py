"""Registered analysis of stage 5b (PREREG_v4_stage5b.md)."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(77); S=0.03; L=[]
TASKS=["door_class","door_teacher_real"]; KINDS=["real","shuffled","random"]; DOSES=(3,7,13)
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
R={(t,k):[json.load(open(os.path.join(HERE,"results_g",f"{t}__{k}__{s}.json"))) for s in range(5000,5100)] for t in TASKS for k in KINDS}
def col(t,k,m): return np.array([r[m] for r in R[(t,k)]])
def drop(t,k,when,name,m): return col(t,k,"intact")-col(t,k,f"{when}_{name}_{m}")
def ex(t,k,when,name,m): return drop(t,k,when,name,m)-drop(t,k,when,"random",m)
def ci(d,lev,n=10000):
    d=np.asarray(d,float); b=d[rng.integers(0,len(d),(n,len(d)))].mean(1); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(b,[a,100-a])]
def tier(m,lo,hi):
    if lo>0 or hi<0: return "small-real" if abs(m)<S else ("meaningful-strict" if min(abs(lo),abs(hi))>=S else "meaningful (边缘)")
    return "equivalent" if (lo>-S and hi<S) else "uncertain"
H=[("1","door_class real：post，hub 13 个通道的超额损失",lambda:ex("door_class","real","post","hub",13)),
   ("2","door_class real：post，bridger 13 个通道的超额损失",lambda:ex("door_class","real","post","bridger",13)),
   ("3","door_class real：pre，hub 13 个通道的超额损失",lambda:ex("door_class","real","pre","hub",13)),
   ("4","door_teacher_real real：pre，hub 13 个通道的超额损失（教师用同一连线，循环，见登记）",lambda:ex("door_teacher_real","real","pre","hub",13)),
   ("5","door_teacher_real real：pre，bridger 13 个通道的超额损失",lambda:ex("door_teacher_real","real","pre","bridger",13)),
   ("6","door_teacher_real：post，hub 13 的超额损失，real − shuffled",lambda:ex("door_teacher_real","real","post","hub",13)-ex("door_teacher_real","shuffled","post","hub",13)),
   ("7","door_class：post，hub 13 的超额损失，real − shuffled",lambda:ex("door_class","real","post","hub",13)-ex("door_class","shuffled","post","hub",13))]
P("# 结果（第四阶段 5b：嗅小球通道的定向病变，自动生成）\n\n学习率 0.05；剂量 = 沉默的嗅小球通道数（3 / 7 / 13，约 5% / 10% / 20%）；超额 = 排序病变的损失 − 同样数量随机通道的损失。三档判定，s = 0.03；主结论族（★，7 个）99.3% 区间，其余 95%；100 个测试世界。\n")
P("## 主结论族\n")
for i,lab,f in H: m,lo,hi=ci(f(),99.3); P(f"- ★{i}. {lab}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**")
for t in TASKS:
    P(f"\n## {t}\n\n完整准确率：" + "，".join(f"{k} {col(t,k,'intact').mean():.3f}" for k in KINDS)+"；hub 与 bridger 前 7 名的重叠个数："+"，".join(f"{k} {col(t,k,'overlap_hub_bridger_7').mean():.1f}" for k in KINDS))
    P("\n超额损失（95% 区间）：")
    for k in KINDS:
        for when in("post","pre"):
            for name in("hub","bridger"):
                for m in DOSES:
                    mm,lo,hi=ci(ex(t,k,when,name,m),95); P(f"- {k} / {when} / {name} / {m}: {mm:+.3f} [{lo:+.3f}, {hi:+.3f}] → {tier(mm,lo,hi)}")
open(os.path.join(HERE,"RESULTS_v4_stage5b.md"),"w").write("\n".join(L)+"\n")
