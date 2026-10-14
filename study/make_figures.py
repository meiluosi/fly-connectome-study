import json, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, core, core_fw
plt.rcParams.update({"font.family":["Hiragino Sans GB","Heiti SC","Arial Unicode MS"],"axes.unicode_minus":False,"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#8a8985","axes.labelcolor":"#52514e","xtick.color":"#52514e","ytick.color":"#52514e","axes.grid":True,"grid.color":"#e4e3df","grid.linewidth":.6,"axes.axisbelow":True})
BLUE,ORANGE,GRAY,INK="#2a78d6","#eb6834","#8a8985","#0b0b0b"; rng=np.random.default_rng(3)
# ---- Fig 1: dose-response, confirmatory
fig,axs=plt.subplots(1,2,figsize=(9.2,3.9),sharey=True)
shuf_ov={"MR":0.203,"FR":0.169}
for ax,(circ,nm) in zip(axs,[("MR","男性 MaleCNS 右半球"),("FR","女性 FlyWire 右半球")]):
    d=json.load(open(f"confirm_p1_{circ}.json")); ok=[p for p in d["parts"] if not(np.isnan(p["forg"]).any() or np.isnan(p["learned"]).any())]
    x=np.array([p["overlap"] for p in ok]); y=np.array([np.mean(p["forg"]) for p in ok]); b=np.polyfit(x,y,1); xs=np.linspace(x.min(),x.max(),50)
    bs=np.array([np.polyval(np.polyfit(x[i],y[i],1),xs) for i in (rng.integers(0,len(x),len(x)) for _ in range(1500))])
    ax.fill_between(xs,*np.percentile(bs,[2.5,97.5],axis=0),color=BLUE,alpha=.15,lw=0); ax.plot(xs,np.polyval(b,xs),color=BLUE,lw=2)
    ax.scatter(x,y,s=22,color=BLUE,edgecolor="#fcfcfb",linewidth=1,zorder=3)
    ref=d["ref"]; ax.scatter([d["real_overlap"]],[np.nanmean(np.array(ref["real"])[:,1])],marker="D",s=58,color=INK,zorder=4,edgecolor="#fcfcfb")
    ax.scatter([shuf_ov[circ]],[np.nanmean(np.array(ref["shuffled"])[:,1])],marker="D",s=58,color=ORANGE,zorder=4,edgecolor="#fcfcfb")
    ax.annotate("真实隔间",(d["real_overlap"],np.nanmean(np.array(ref["real"])[:,1])),xytext=(6,8),textcoords="offset points",fontsize=9,color=INK)
    ax.annotate("打乱隔间",(shuf_ov[circ],np.nanmean(np.array(ref["shuffled"])[:,1])),xytext=(-4,-17),textcoords="offset points",fontsize=9,color="#a8431a")
    ax.set_title(f"{nm}：斜率 {b[0]:.3f}",fontsize=10,loc="left",color=INK); ax.set_xlabel("同隔间 MBON 的 KC 输入重叠度（余弦）")
axs[0].set_ylabel("遗忘量（T=24）")
fig.suptitle("人为改变重叠度，遗忘随之上升（确认性实验，新种子与新划分）",x=0.01,ha="left",fontsize=11.5,color=INK); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig("../figures/fig1_dose_response.png",dpi=170); plt.close()
# ---- Fig 2: real - shuffled forest
def boot(d,n=4000):
    m=np.array([d[rng.integers(0,len(d),len(d))].mean() for _ in range(n)]); return d.mean(),*np.percentile(m,[2.5,97.5])
fig,ax=plt.subplots(figsize=(7.4,4.1)); labs=[];i=0
for circ,nm,col in [("MR","男 右",BLUE),("ML","男 左",BLUE),("FR","女 右",ORANGE),("FL","女 左",ORANGE)]:
    dd=json.load(open(f"confirm_p24_{circ}.json"))
    for T in [12,48]:
        r=dd[f"random_T{T}"]; d=np.array([x["forg_acc"] for x in r["real"]])-np.array([x["forg_acc"] for x in r["shuffled"]]); m,lo,hi=boot(d)
        ax.plot([lo,hi],[i,i],color=col,lw=2,solid_capstyle="round"); ax.scatter([m],[i],s=36,color=col,zorder=3,edgecolor="#fcfcfb"); labs.append(f"{nm}  T={T}"); i+=1
ax.axvline(0,color=INK,lw=1); ax.axvspan(-.01,.01,color=GRAY,alpha=.15,lw=0); ax.set_yticks(range(len(labs)),labs); ax.set_ylim(7.9,-.6); ax.grid(axis="y",visible=False)
ax.set_xlabel("遗忘量之差：真实隔间 − 打乱隔间（正值 = 真实隔间忘得更多）"); ax.text(.0105,7.62,"灰带：±0.01 等价边界",fontsize=8.5,color="#52514e",va="center")
ax.set_title("行为读出下的差异：男性数据方向一致，女性数据不稳（未达预先登记判据）",loc="left",fontsize=10.5,color=INK,pad=10); fig.tight_layout(); fig.savefig("../figures/fig2_real_vs_shuffled.png",dpi=170); plt.close()
# ---- Fig 3: baselines, similar T=48, mean over 4 circuits
M={"fly-real":"real","fly-none":"none","delta":"delta","EWC(最优λ)":"ewc","多头无约束":"mh"}; acc={k:[] for k in M}; frg={k:[] for k in M}
for circ in ["MR","ML","FR","FL"]:
    r=json.load(open(f"confirm_p24_{circ}.json"))["similar_T48"]
    best=max(["ewc10","ewc100","ewc1000"],key=lambda m:np.mean([x["final_acc"] for x in r[m]]))
    for k,m in M.items():
        mm=best if m=="ewc" else m; acc[k].append(np.mean([x["final_acc"] for x in r[mm]])); frg[k].append(np.mean([x["forg_acc"] for x in r[mm]]))
fig,ax=plt.subplots(figsize=(6.6,4.2))
for k in M:
    col=BLUE if k=="fly-real" else GRAY; ax.scatter(np.mean(frg[k]),np.mean(acc[k]),s=70 if k=="fly-real" else 46,color=col,zorder=3,edgecolor="#fcfcfb")
    dx,dy={"fly-real":(8,-14),"fly-none":(8,4),"delta":(-6,9),"EWC(最优λ)":(8,-14),"多头无约束":(8,6)}[k]; ax.annotate(k,(np.mean(frg[k]),np.mean(acc[k])),xytext=(dx,dy),textcoords="offset points",fontsize=9.5,color=INK if k=="fly-real" else "#52514e",ha="left" if dx>0 else "right")
ax.set_xlabel("遗忘量（越小越好）"); ax.set_ylabel("最终准确率（越大越好）"); ax.invert_xaxis()
ax.set_title("相似气味任务，T=48：回路忘得少，但最终准确率不如常规基线",loc="left",fontsize=10.5,color=INK); fig.tight_layout(); fig.savefig("../figures/fig3_baselines.png",dpi=170); plt.close(); print("figures ok")
