import json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":["Hiragino Sans GB","Heiti SC","Arial Unicode MS"],"axes.unicode_minus":False,"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#8a8985","axes.labelcolor":"#52514e","xtick.color":"#52514e","ytick.color":"#52514e","axes.grid":True,"grid.color":"#e4e3df","grid.linewidth":.6,"axes.axisbelow":True})
BLUE,ORANGE,GRAY,INK="#2a78d6","#eb6834","#8a8985","#0b0b0b"; rng=np.random.default_rng(3)
# fig1: corrected dose-response
fig,axs=plt.subplots(1,2,figsize=(9.2,3.9),sharey=True)
for ax,(circ,nm) in zip(axs,[("MR","男性 MaleCNS 右半球"),("FR","女性 FlyWire 右半球")]):
    d=json.load(open(f"round2_A_{circ}.json")); P=d["parts"]; x=np.array([p["overlap"] for p in P]); y=np.array([np.mean(p["forg"]) for p in P]); b=np.polyfit(x,y,1); xs=np.linspace(x.min(),x.max(),50)
    bs=np.array([np.polyval(np.polyfit(x[i],y[i],1),xs) for i in (rng.integers(0,len(x),len(x)) for _ in range(1500))])
    ax.fill_between(xs,*np.percentile(bs,[2.5,97.5],axis=0),color=BLUE,alpha=.15,lw=0); ax.plot(xs,np.polyval(b,xs),color=BLUE,lw=2); ax.scatter(x,y,s=22,color=BLUE,edgecolor="#fcfcfb",linewidth=1,zorder=3)
    ax.set_title(f"{nm}：简单斜率 {b[0]:+.3f}",fontsize=10,loc="left",color=INK); ax.set_xlabel("同隔间 MBON 的 KC 输入重叠度（入度分层划分）")
axs[0].set_ylabel("遗忘量（准确率，T=24）")
axs[0].text(.02,.04,"控制入度同质性与学习量后，\n重叠度的偏回归系数：−0.005 [−0.020, 0.008]",transform=axs[0].transAxes,fontsize=8.5,color="#52514e")
axs[1].text(.02,.04,"偏回归系数：+0.007 [−0.006, 0.020]",transform=axs[1].transAxes,fontsize=8.5,color="#52514e")
fig.suptitle("修正后的剂量反应（直线为未校正的简单斜率）：只在男性数据里为正，控制混杂后两边都不显著",x=0.01,ha="left",fontsize=11.5,color=INK); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig("../figures/fig1_dose_response.png",dpi=170); plt.close()
# fig3: corrected baselines (similar T=48, mean over MR/FR, test seeds)
pts={"fly-real":[],"delta":[],"EWC(λ=10)":[],"多头（用任务标识）":[]}
for circ in ["MR","FR"]:
    r=json.load(open(f"round2_B_{circ}.json"))["similar_T48"]; g=lambda k,f:np.mean([x[f] for x in r[k][10:]])
    for lab,k in [("fly-real","fly_real_0.3"),("delta","delta_0.5"),("EWC(λ=10)","ewc_10"),("多头（用任务标识）","mh")]: pts[lab].append((g(k,"forg_acc"),g(k,"final_acc")))
fig,ax=plt.subplots(figsize=(6.8,4.3))
for lab,v in pts.items():
    m=np.mean(v,axis=0); col=BLUE if lab=="fly-real" else GRAY; ax.scatter(m[0],m[1],s=75 if lab=="fly-real" else 48,color=col,zorder=3,edgecolor="#fcfcfb")
    dx,dy={"fly-real":(-8,-14),"delta":(8,-14),"EWC(λ=10)":(8,6),"多头（用任务标识）":(8,-14)}[lab]; ax.annotate(lab,m,xytext=(dx,dy),textcoords="offset points",fontsize=9.5,color=INK if lab=="fly-real" else "#52514e",ha="left" if dx>0 else "right")
ax.set_xlabel("遗忘量（越小越好；横轴已反向，越靠右越好）"); ax.set_ylabel("最终准确率（越大越好）"); ax.invert_xaxis(); ax.set_ylim(0.55,1.03)
ax.set_title("仅展示 8 个设定中的一个（相似气味，T=48，男女电路均值）：回路落后于 EWC",loc="left",fontsize=10.2,color=INK); ax.text(.02,.93,"多头基线读出时使用任务标识，回路不使用，\n二者不是同一设定",transform=ax.transAxes,fontsize=8.3,color="#52514e",va="top")
fig.tight_layout(); fig.savefig("../figures/fig3_baselines.png",dpi=170); plt.close()
# fig4: matched-learning curves from preregistered runs (T=48 random), two circuits
fig,axs=plt.subplots(1,2,figsize=(9.4,4.1),sharey=True)
def cv(circ,rule,cond,task="random",T=48):
    D=json.load(open(f"matched_{circ}_{task}_{T}.json")); ks=sorted([k for k in D if k.startswith(f"{rule}|{cond}|")],key=lambda k:float(k.split("|")[2]))
    a=np.array([(np.mean([x["learn_acc"] for x in D[k]]),np.mean([x["forg_acc"] for x in D[k]])) for k in ks]); return a[np.argsort(a[:,0])]
for ax,(circ,nm) in zip(axs,[("MR","男性 MaleCNS 右"),("FR","女性 FlyWire 右")]):
    r=cv(circ,"bounded","real"); n=cv(circ,"bounded","none"); a=cv(circ,"additive0","real")
    lo=max(r[:,0].min(),n[:,0].min()); hi=min(r[:,0].max(),n[:,0].max()); ax.axvspan(lo,hi,color=GRAY,alpha=.13,lw=0)
    ax.plot(r[:,0],r[:,1],"-",color=BLUE,lw=2,marker="o",ms=4,label="有界规则 · 分隔间"); ax.plot(n[:,0],n[:,1],"--",color=BLUE,lw=2,marker="o",ms=4,label="有界规则 · 不分隔间")
    ax.plot(a[:,0],a[:,1],"-",color=ORANGE,lw=2,marker="o",ms=4,label="无界加法规则 · 分隔间"); ax.set_title(nm,loc="left",fontsize=10,color=INK); ax.set_xlabel("学习时准确率（学得多少）")
    ax.text(.5*(lo+hi),0.97,"灰带：两条曲线都覆盖的可比范围",fontsize=8,color="#52514e",ha="center",va="top",transform=ax.get_xaxis_transform())
axs[0].set_ylabel("遗忘量（T=48，随机气味，40 个种子的均值）"); axs[0].legend(frameon=False,fontsize=8.5,loc="lower right")
fig.suptitle("匹配学习量下：有界规则的分隔间与不分隔间曲线重合；无界加法规则遗忘更少（仅在可比范围内成立）",x=0.01,ha="left",fontsize=10.5,color=INK); fig.tight_layout(rect=[0,0,1,.93]); fig.savefig("../figures/fig4_ablation_matched_learning.png",dpi=170); plt.close(); print("ok")
