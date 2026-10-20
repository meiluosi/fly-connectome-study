"""Registered analysis of stage 4 (PREREG_v4_stage4.md)."""
import json, os, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); rng=np.random.default_rng(75); S=0.03; L=[]
TASKS=["door_class","door_teacher_real","linear_teacher","teacher_real"]; ARMS=["global","comp_real","comp_shuf","comp_shufbal","unsigned"]; GRID=(0.005,0.01,0.02,0.05,0.15,0.4,1.0)
HEAD=[("door_class","comp_real","comp_shufbal",0.03),("door_class","comp_real","global",0.03),("linear_teacher","comp_real","comp_shufbal",0.03),("linear_teacher","comp_real","global",0.03),
      ("cl","comp_real","global",0.03),("cl","comp_real","global_matched",0.03),("cl","comp_real","comp_shufbal",0.03)]
def P(*a): s=" ".join(str(x) for x in a); print(s); L.append(s)
def load(t,tag,m): return np.array([json.load(open(os.path.join(HERE,"results_e",f"{t}__{tag}__{s}.json")))[m] for s in range(5000,5100)])
def ci(d,lev,n=10000):
    d=np.asarray(d,float); m=d[rng.integers(0,len(d),(n,len(d)))].mean(1); a=(100-lev)/2; return float(d.mean()),*[float(x) for x in np.percentile(m,[a,100-a])]
def tier(m,lo,hi,s=S):
    if lo>0 or hi<0: return "small-real" if abs(m)<s else ("meaningful-strict" if min(abs(lo),abs(hi))>=s else "meaningful (边缘)")
    return "equivalent" if (lo>-s and hi<s) else "uncertain"
P("# 结果（第四阶段 4：效价专门化隔间 + 多巴胺时序规则，自动生成）\n\n三档判定，s = 0.03（准确率点）；主结论族（★，7 个）99.3% 区间，其余 95%；100 个测试世界（种子 5000–5099）。\n")
P("## A. 时序现象（单个气味，3 次配对，学习率 0.3）\n")
ISIS=(-8.0,-6.0,-3.0,-1.5,-0.5,0.5,1.5,3.0,4.0,8.0)
def ph(arm,var,R,isi): return np.array([json.load(open(os.path.join(HERE,"results_e","phen",f"{arm}__{var}__{s}.json")))[f"{R}|{isi}"] for s in range(5000,5100)])
P("| 学习器 | 变体 | 奖励 ISI −0.5 | 奖励 +0.5 | 惩罚 −0.5 | 惩罚 +0.5 | 奖励 +8 | 奖励 −8 | P1 符号 | P2 衰减 | P3 隔间特异 |\n|---|---|---|---|---|---|---|---|---|---|---|")
for arm in ("comp_real","comp_shuf","comp_shufbal"):
    I={v:{(R,i):ph(arm,v,R,i) for R in (1.0,-1.0) for i in ISIS} for v in("intact","PAM","PPL","notiming")}
    mu=lambda v,R,i:I[v][(R,i)].mean()
    def sg(v,R,i,pos): m,lo,hi=ci(I[v][(R,i)],95); return (lo>0) if pos else (hi<0)
    p1=sg("intact",1.0,0.5,True) and sg("intact",1.0,-0.5,False) and sg("intact",-1.0,0.5,False) and sg("intact",-1.0,-0.5,True)
    p2=all(abs(mu("intact",R,sgn*8.0 if sgn>0 else -8.0))<=0.25*abs(mu("intact",R,sgn*0.5)) for R in (1.0,-1.0) for sgn in (1,-1))
    p3=(abs(mu("PAM",1.0,0.5))<=0.1*abs(mu("intact",1.0,0.5)) and abs(mu("PAM",-1.0,0.5))>=0.8*abs(mu("intact",-1.0,0.5)) and abs(mu("PPL",-1.0,0.5))<=0.1*abs(mu("intact",-1.0,0.5)) and abs(mu("PPL",1.0,0.5))>=0.8*abs(mu("intact",1.0,0.5)))
    for v in ("intact","notiming"):
        r=lambda R,i:f"{mu(v,R,i):+.3f}"
        P(f"| {arm} | {v} | {r(1.0,-0.5)} | {r(1.0,0.5)} | {r(-1.0,-0.5)} | {r(-1.0,0.5)} | {r(1.0,8.0)} | {r(1.0,-8.0)} | "+(" | ".join(["是" if x else "否" for x in (p1,p2,p3)]) if v=="intact" else "— | — | —")+" |")
P("\n## B. 样本效率任务（auc；每个（任务，学习器）调参后的学习率）\n")
T=json.load(open(os.path.join(HERE,"tuning_v4e.json")))
for t in TASKS:
    P(f"\n### {t}\n| 学习器 | 学习率 | auc | 50 次后 | 最终 |\n|---|---|---|---|---|")
    for k in ARMS: P(f"| {k} | {T[f'{t}|{k}']['eta']} | {load(t,k,'auc').mean():.3f} | {load(t,k,'acc50').mean():.3f} | {load(t,k,'final').mean():.3f} |")
    P("\n配对差（auc）：")
    for a,b in (("comp_real","global"),("comp_real","comp_shufbal"),("comp_real","comp_shuf"),("comp_real","unsigned"),("global","comp_shufbal")):
        h=any(x[:3]==(t,a,b) for x in HEAD); m,lo,hi=ci(load(t,a,"auc")-load(t,b,"auc"),99.3 if h else 95); P(f"- {'★' if h else ''}{a} − {b}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**")
P("\n## C. 持续学习（4 个任务各 10 个气味，随机 ±1 标签，依次学习，最后测全部 40 个）\n")
P("| 学习器 | 学习率 | 刚学完时 | 最终 | 遗忘（归一化） |\n|---|---|---|---|---|")
for k,tag in (("global","global"),("global (匹配学习量)","global_matched"),("comp_real","comp_real"),("comp_shuf","comp_shuf"),("comp_shufbal","comp_shufbal"),("unsigned","unsigned")):
    eta=T["cl|global_matched"]["eta"] if tag=="global_matched" else T[f"cl|{tag}"]["eta"]
    P(f"| {k} | {eta} | {load('cl',tag,'after').mean():.3f} | {load('cl',tag,'final').mean():.3f} | {load('cl',tag,'forgetting').mean():.3f} |")
P("\n配对差（最终准确率）：")
for a,b in (("comp_real","global"),("comp_real","global_matched"),("comp_real","comp_shufbal"),("comp_real","comp_shuf"),("comp_real","unsigned")):
    h=("cl",a,b,0.03) in HEAD; m,lo,hi=ci(load("cl",a,"final")-load("cl",b,"final"),99.3 if h else 95); P(f"- {'★' if h else ''}{a} − {b}: {m:+.3f} [{lo:+.3f}, {hi:+.3f}] → **{tier(m,lo,hi)}**")
P("\n学习量—最终准确率的前沿（全部学习率，描述性）：\n\n| 学习率 | global 刚学完 / 最终 | comp_real 刚学完 / 最终 |\n|---|---|---|")
for e in GRID: P(f"| {e} | {load('cl',f'front_global_{e}','after').mean():.3f} / {load('cl',f'front_global_{e}','final').mean():.3f} | {load('cl',f'front_comp_real_{e}','after').mean():.3f} / {load('cl',f'front_comp_real_{e}','final').mean():.3f} |")
open(os.path.join(HERE,"RESULTS_v4_stage4.md"),"w").write("\n".join(L)+"\n")
