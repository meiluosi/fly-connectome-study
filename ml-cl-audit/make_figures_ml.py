import json, glob, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":["Hiragino Sans GB","Heiti SC","Arial Unicode MS"],"axes.unicode_minus":False,"font.size":10,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#8a8985","axes.labelcolor":"#52514e","xtick.color":"#52514e","ytick.color":"#52514e","axes.grid":True,"grid.color":"#e4e3df","grid.linewidth":.6,"axes.axisbelow":True})
BLUE,ORANGE,GRAY,INK="#2a78d6","#eb6834","#8a8985","#0b0b0b"
def load(b):
    c={}
    for f in glob.glob(f"results/{b}/*.json"): d=json.load(open(f)); c[d["key"]]=d["value"]
    out={}
    for k,v in c.items():
        if k.startswith("test|"): p=k.split("|"); out.setdefault("|".join(p[1:-2]),[]).append(v["final"])
    return {n:float(np.mean(v)) for n,v in out.items()}, {n:float(np.std(v)) for n,v in out.items()}
B={b:load(b) for b in ["mnist20","cifar100","cifar100_224"]}; TT={"mnist20":"MNIST-20","cifar100":"CIFAR-100-A（弱特征）","cifar100_224":"CIFAR-100-B（强特征）"}
# Fig 1: final accuracy by method, three benchmarks
rows=[("FlyModel（论文设定）","Fly_F0",BLUE),("FlyModel（验证集调参）","Fly_F1",BLUE),("SLDA（免回放）","SLDA",ORANGE),("最近类均值（余弦）","NCM_cos",GRAY),("回放 ER-200","B3_er200|inter",GRAY),("回放 ER-1000","B3_er1000|inter",GRAY),("EWC","B2_ewc|inter",GRAY),("微调","B1_vanilla|inter",GRAY),("离线上界","B4_offline","#52514e")]
fig,axs=plt.subplots(1,3,figsize=(11.5,4.3),sharey=True)
for ax,b in zip(axs,B):
    m,s=B[b]; ys=[]; 
    for i,(lab,key,col) in enumerate(rows):
        if key in m: ax.errorbar(m[key],i,xerr=s[key],fmt="o",color=col,ms=6,capsize=2,lw=1.4); ax.text(m[key]+0.012,i,f"{m[key]:.2f}",va="center",fontsize=8.3,color="#52514e")
        else: ax.text(0.02,i,"未完成",va="center",fontsize=8,color="#a8a7a2")
    ax.set_title(TT[b],fontsize=10,loc="left",color=INK); ax.set_xlim(0,1.0); ax.set_xlabel("最终准确率（测试集，类增量）")
axs[0].set_yticks(range(len(rows)),[r[0] for r in rows]); axs[0].invert_yaxis(); axs[0].grid(axis="y",visible=False)
fig.suptitle("FlyModel 在三个基准上都被免回放的 SLDA 超过（EWC/微调/回放为任务内交错流的结果；SLDA 与最近类均值为单次确定性运行，无误差线）",x=0.01,ha="left",fontsize=11,color=INK); fig.tight_layout(rect=[0,0,1,.94]); fig.savefig("figures/fig1_final_accuracy.png",dpi=170); plt.close()
# Fig 2: sparse - dense under two classifier rules
reg=[];same=[]
for b in B:
    m,_=B[b]; reg.append(m["Fly_F0"]-m["Fly_dense_l2"]); same.append(m["ExpNCM_wta_euc"]-m["ExpNCM_dense_euc"])
fig,ax=plt.subplots(figsize=(7.2,3.9)); x=np.arange(3)
ax.scatter(x,reg,s=70,color=GRAY,zorder=3,label="我登记的稠密对照 F2：L2 归一化 + Hebbian 类和点积（未调 β）"); ax.scatter(x,same,s=70,color=BLUE,zorder=3,label="探索性：同一个最近类均值分类器（欧氏）下")
for xi,a,b_ in zip(x,reg,same): ax.plot([xi,xi],[a,b_],color="#c9c8c3",lw=1.2,zorder=2); ax.text(xi+0.06,a,f"{a:+.2f}",va="center",fontsize=8.5,color="#52514e"); ax.text(xi+0.06,b_,f"{b_:+.2f}",va="center",fontsize=8.5,color=BLUE)
ax.axhline(0,color=INK,lw=0.8); ax.set_xticks(x,[TT[b] for b in B],fontsize=9); ax.set_ylabel("稀疏扩展相对稠密扩展的最终准确率优势"); ax.legend(frameon=False,fontsize=8.5,loc="upper right")
ax.set_title("（探索性，看到结果后加入）换成同一个分类器后，稀疏相对稠密的优势缩到 ±0.03 以内",loc="left",fontsize=10,color=INK); fig.tight_layout(); fig.savefig("figures/fig2_sparse_vs_dense.png",dpi=170); plt.close(); print("ok",np.round(reg,3),np.round(same,3))
