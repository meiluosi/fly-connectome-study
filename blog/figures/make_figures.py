"""Generates the two explanatory SVG figures for blog post 01 (toy-sized schematics; numbers in captions come from the real circuit file)."""
import random
INK="#1b2329"; MUTED="#5d6a73"; LINE="#c9ced3"; BLUE="#1f6fd0"; ORANGE="#c9501b"; TEAL="#0b8a84"; GREY="#8d98a1"; SOFT="#eef2f6"
FONT="font-family=\"Noto Sans SC,PingFang SC,Hiragino Sans GB,Microsoft YaHei,system-ui,sans-serif\""
def T(x,y,s,size=13,fill=INK,anchor="start",weight="normal"): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {FONT}>{s}</text>'
def svg(w,h,body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"><rect width="{w}" height="{h}" fill="#ffffff"/>{body}</svg>'
# ---------------------------------------------------------------- figure 1: the circuit
def fig1():
    W,H=980,490; b=[]
    cols=[(70,"气味"),(250,"嗅觉小球"),(500,"Kenyon 细胞 (KC)"),(760,"输出神经元 (MBON)"),(915,"行为")]
    for x,l in cols: b.append(T(x,34,l,14,INK,"middle","bold"))
    # odour -> glomeruli
    random.seed(3)
    b.append(f'<rect x="30" y="150" width="80" height="150" rx="8" fill="{SOFT}" stroke="{LINE}"/>'+T(70,215,"一种",13,INK,"middle")+T(70,235,"气味",13,INK,"middle")+T(70,262,"= 激活",12,MUTED,"middle")+T(70,280,"若干小球",12,MUTED,"middle"))
    gy=[70+i*40 for i in range(9)]; lit={1,4,6}
    for i,y in enumerate(gy):
        c=BLUE if i in lit else LINE
        b.append(f'<circle cx="250" cy="{y}" r="11" fill="{c}" opacity="{1 if i in lit else .6}"/>')
        if i in lit: b.append(f'<line x1="110" y1="225" x2="239" y2="{y}" stroke="{BLUE}" stroke-width="1.6" opacity=".7"/>')
    b.append(T(250,440,"65 种小球（图中只画 9 个）",12,MUTED,"middle"))
    # KC layer
    ky=[62+i*22 for i in range(17)]; klit={2,7,11,14}
    for j,y in enumerate(ky):
        for i in random.sample(range(9),2):
            if i in lit and j in klit: b.append(f'<line x1="261" y1="{gy[i]}" x2="490" y2="{y}" stroke="{BLUE}" stroke-width="1.4" opacity=".75"/>')
            else: b.append(f'<line x1="261" y1="{gy[i]}" x2="490" y2="{y}" stroke="{LINE}" stroke-width=".8" opacity=".5"/>')
    for j,y in enumerate(ky): b.append(f'<circle cx="500" cy="{y}" r="7" fill="{BLUE if j in klit else "#dde2e7"}"/>')
    b.append(T(500,440,"约 2000 个（图中画 17 个）· 只有最强的 5% 亮",12,MUTED,"middle"))
    # MBON
    my=[100+i*52 for i in range(6)]; sg=[1,-1,1,-1,1,-1]
    for j,y in enumerate(my):
        col=TEAL if sg[j]>0 else ORANGE
        b.append(f'<circle cx="760" cy="{y}" r="15" fill="{col}" opacity=".9"/>'+T(760,y+5,"+" if sg[j]>0 else "−",16,"#ffffff","middle","bold"))
    for j in klit:
        for m in (0,1,2,3,4,5):
            if (j+m)%3==0: b.append(f'<line x1="507" y1="{ky[j]}" x2="745" y2="{my[m]}" stroke="{GREY}" stroke-width="1.2" opacity=".55"/>')
    b.append(T(760,440,"49 个：+ 兴奋(25) / − 抑制(24)",12,MUTED,"middle"))
    # DAN
    b.append(f'<rect x="590" y="372" width="120" height="30" rx="6" fill="{SOFT}" stroke="{ORANGE}"/>'+T(650,392,"多巴胺 = 预测误差",12,ORANGE,"middle"))
    b.append(f'<line x1="650" y1="372" x2="650" y2="290" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="4 3"/><polygon points="645,296 655,296 650,284" fill="{ORANGE}"/>')
    b.append(T(660,330,"改写这一层",12,ORANGE)+T(660,346,"突触强度 q",12,ORANGE))
    # behaviour
    b.append(f'<rect x="880" y="190" width="70" height="70" rx="8" fill="{SOFT}" stroke="{LINE}"/>'+T(915,220,"趋近",13,TEAL,"middle","bold")+T(915,242,"回避",13,ORANGE,"middle","bold"))
    b.append(f'<line x1="776" y1="225" x2="878" y2="225" stroke="{GREY}" stroke-width="1.6"/><polygon points="872,220 872,230 882,225" fill="{GREY}"/>')
    # brackets
    b.append(f'<rect x="206" y="52" width="388" height="372" rx="10" fill="none" stroke="{BLUE}" stroke-dasharray="5 4" opacity=".6"/>'+T(400,466,"编码层：真实连线 P（65 × 2045）",12.5,BLUE,"middle","bold"))
    b.append(T(700,466,"学习层：真实连线 N（2045 × 49）+ 递质符号",12.5,ORANGE,"middle","bold"))
    return svg(W,H,"".join(b))
# ---------------------------------------------------------------- figure 2: the controls
KC={0:{0:3,1:1},1:{0:1,2:2,3:1},2:{1:2,2:1},3:{3:3,4:1},4:{2:1,4:2,5:1},5:{0:1,5:2},6:{1:1,3:1,4:1},7:{2:2,5:1}}
def panel(x0,title,sub,edges,note,show_kc=True,hub=None,color=BLUE):
    b=[]; gx,kx=x0+30,x0+140; gy=[70+i*34 for i in range(6)]; ky=[70+i*26 for i in range(8)]
    b.append(T(x0+85,34,title,14,INK,"middle","bold")+T(x0+85,52,sub,11.5,MUTED,"middle"))
    for (g,k,w) in edges: b.append(f'<line x1="{gx+8}" y1="{gy[g]}" x2="{kx-6}" y2="{ky[k]}" stroke="{color}" stroke-width="{0.6+0.9*w}" opacity=".7"/>')
    for i,y in enumerate(gy): b.append(f'<circle cx="{gx}" cy="{y}" r="7" fill="{BLUE if (hub is not None and i==hub) else "#9fb4cb"}"/>')
    if show_kc:
        for y in ky: b.append(f'<circle cx="{kx}" cy="{y}" r="6" fill="#dde2e7" stroke="{GREY}"/>')
    b.append(T(gx,282,"小球",11,MUTED,"middle")+T(kx,282,"KC",11,MUTED,"middle"))
    for n,line in enumerate(note): b.append(T(x0+85,312+n*17,line,11.5,MUTED if n else INK,"middle","bold" if n==0 else "normal"))
    return "".join(b)
def fig2():
    W,H=1040,380; rnd=random.Random(11); b=[]
    real=[(g,k,w) for k,d in KC.items() for g,w in d.items()]
    shuf=[]
    for k,d in KC.items():
        gl=rnd.sample(range(6),len(d)); shuf+= [(g,k,w) for g,(_,w) in zip(gl,d.items())]
    rand=[(g,k,1) for k in KC for g in rnd.sample(range(6),3)]
    rb=[(g,k,1) for g,k,w in real]
    b.append(panel(10,"真实","原始连线",real,["接线与粗细都保留","小球3 连得最多（枢纽）"],hub=2))
    b.append(panel(215,"打乱","保度数，换掉连哪个小球",shuf,["每个 KC 输入数、粗细不变","改变：具体连哪个小球"]))
    b.append(panel(420,"随机稀疏","每个 KC 随机选固定个数，粗细为 1",rand,["去掉：真实拓扑与强度差异","保留：稀疏扩展本身"]))
    b.append(panel(625,"真实二值","真实拓扑，所有粗细置 1",rb,["保留：谁连谁","去掉：输入强度的差异"]))
    # linear
    x0=830; gx=x0+30; gy=[70+i*34 for i in range(6)]
    b.append(T(x0+90,34,"线性学习器",14,INK,"middle","bold")+T(x0+90,52,"没有稀疏扩展",11.5,MUTED,"middle"))
    for y in gy: b.append(f'<line x1="{gx+8}" y1="{y}" x2="{x0+140}" y2="{ 70+2.5*34}" stroke="{TEAL}" stroke-width="1.4" opacity=".7"/>'+f'<circle cx="{gx}" cy="{y}" r="7" fill="#9fb4cb"/>')
    b.append(f'<rect x="{x0+134}" y="{70+2.5*34-14}" width="52" height="28" rx="6" fill="{SOFT}" stroke="{TEAL}"/>'+T(x0+160,70+2.5*34+5,"价值",12,TEAL,"middle"))
    b.append(T(gx,282,"小球",11,MUTED,"middle")+T(x0+160,282,"直接线性读出",11,MUTED,"middle"))
    b.append(T(x0+90,312,"检验稀疏扩展有没有用",11.5,INK,"middle","bold")+T(x0+90,329,"（还有“不学习”作健全性检查）",11.5,MUTED,"middle"))
    b.append(T(520,368,"五种对照：学习规则、任务、预算、调参方式都一样，只换这一层连线。图为 6 个小球、8 个 KC 的示意；粗线 = 突触数多。",12,MUTED,"middle"))
    return svg(W,H,"".join(b))

# ---------------------------------------------------------------- figure 3: protocol flow ; figure 4: what the reviews changed
def box(x,y,w,h,title,sub,color=BLUE):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{SOFT}" stroke="{color}"/>'+T(x+w/2,y+26,title,14,INK,"middle","bold")+"".join(T(x+w/2,y+48+i*17,l,11.5,MUTED,"middle") for i,l in enumerate(sub))
def arrow(x1,y1,x2,y2,color=GREY): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.8"/><polygon points="{x2},{y2} {x2-8},{y2-5} {x2-8},{y2+5}" fill="{color}"/>'
def fig3():
    W,H=1040,300; b=[]; steps=[("写预先登记",["假设、对比、","判定标准、等价边界"]),("锁哈希",["代码和登记文件","记下 sha256"]),("调参 / 测试分开",["调参用一段种子","测试用全新种子"]),("测试只跑一次",["不回头再调参"]),("脚本出结果",["登记好的分析脚本","自动生成"]),("独立审查",["没有上下文的","子 agent 挑错"]),("更正并记录",["改结论、写进","偏离日志"])]
    bw,gap=124,22
    for i,(t,sub) in enumerate(steps):
        x=14+i*(bw+gap); col=ORANGE if i==5 else BLUE; b.append(box(x,70,bw,90,t,sub,col))
        if i<6: b.append(arrow(x+bw+2,115,x+bw+gap-2,115))
    b.append(T(520,38,"每个实验都走同一条线",15,INK,"middle","bold"))
    xs=14+5*(bw+gap)+bw/2; xe=14+6*(bw+gap)+bw/2
    b.append(f'<path d="M {xe} 162 L {xe} 215 L 70 215 L 70 168" fill="none" stroke="{ORANGE}" stroke-width="1.8" stroke-dasharray="5 4"/><polygon points="70,160 64,171 76,171" fill="{ORANGE}"/>')
    b.append(T(520,238,"审查发现问题 → 回到起点：改登记、加对照、重跑（原结果保留，不删）",12.5,ORANGE,"middle"))
    b.append(T(520,282,"共 9 份审查报告：隔间 4 份、持续学习审计 2 份、旅行商 3 份",12,MUTED,"middle"))
    return svg(W,H,"".join(b))
def fig4():
    rows=[("隔间与遗忘","隔间让遗忘变少，是“因果”","主要是学得少；重叠度和入度混在一起"),
          ("持续学习审计","FlyModel 与简单基线“等价”","被 SLDA 超过（差 0.05 到 0.13）"),
          ("觅食","20、60 个世界里隐约有优势","200 个新世界里：真实 ≈ 打乱，随机稀疏更好"),
          ("旅行商 v1","没有特征映射超过 0.5pp","只能说“不确定”"),
          ("旅行商 v2","真实连线无关","特征与距离相关 0.85，设计测不出"),
          ("旅行商 v3","转角上下文没有用","学习器根本没学到转角信息")]
    W=1040; H=70+len(rows)*54+20; b=[T(520,34,"审查之后，我说法的变化",15,INK,"middle","bold")]
    b.append(T(190,62,"项目",12,MUTED,"middle")+T(470,62,"起初的说法",12,ORANGE,"middle","bold")+T(830,62,"审查之后",12,TEAL,"middle","bold"))
    for i,(p,a,c) in enumerate(rows):
        y=76+i*54; b.append(f'<line x1="20" x2="{W-20}" y1="{y-6}" y2="{y-6}" stroke="{LINE}"/>')
        b.append(T(190,y+24,p,13.5,INK,"middle","bold")+T(470,y+24,a,13,INK,"middle")+arrow(640,y+19,690,y+19,GREY)+T(830,y+24,c,13,INK,"middle"))
    return svg(W,H,"".join(b))
open("fig3_protocol.svg","w").write(fig3()); open("fig4_downgrades.svg","w").write(fig4())

# ---------------------------------------------------------------- figures 5-7: foraging post
VIOLET="#7048c9"
def fig5():
    W,H=1040,400; b=[T(260,30,"一个觅食世界（俯视）",15,INK,"middle","bold"),T(790,30,"奖励怎么变",15,INK,"middle","bold")]
    ax,ay,asz=40,50,440; b.append(f'<rect x="{ax}" y="{ay}" width="{asz}" height="{asz-100}" rx="6" fill="#f7f9fb" stroke="{LINE}"/>')
    src=[(110,120,"A",TEAL),(200,200,"A\u2032",TEAL),(120,280,"A\u2033",TEAL),(400,110,"B",VIOLET),(360,210,"B\u2032",VIOLET),(420,290,"B\u2033",VIOLET)]
    for x,y,l,c in src:
        b.append(f'<circle cx="{x}" cy="{y}" r="34" fill="{c}" opacity=".12"/><circle cx="{x}" cy="{y}" r="16" fill="{c}" opacity=".25"/><circle cx="{x}" cy="{y}" r="7" fill="{c}"/>'+T(x+12,y-10,l,13,c,"start","bold"))
    b.append(f'<polygon points="262,215 244,205 244,225" fill="{BLUE}"/><circle cx="262" cy="215" r="3" fill="{BLUE}"/>'+T(262,246,"果蝇：左右触角比较气味",12,BLUE,"middle"))
    b.append(T(260,462,"6 个食物源，分两个气味家族；变体（A′、A″）与原型共享 6 个小球里的 4 个",12,MUTED,"middle"))
    # timeline
    x0,w=600,380; b.append(T(x0,70,"家族 A",13,TEAL,"start","bold")+T(x0,130,"家族 B",13,VIOLET,"start","bold"))
    for row,(y,c) in enumerate(((78,TEAL),(138,VIOLET))):
        good=(row==0)
        for half in (0,1):
            gd=(good if half==0 else not good); fill=("#bfe3d1" if gd else "#f1c9c0")
            b.append(f'<rect x="{x0+half*w/2}" y="{y}" width="{w/2-3}" height="34" rx="4" fill="{fill}"/>'+T(x0+half*w/2+w/4,y+22,"+1 好吃" if gd else "−1 有害",13,INK,"middle"))
    b.append(T(x0,184,"0",11,MUTED)+T(x0+w/2,184,"第 3000 步：奖励整体反转",11,ORANGE,"middle")+T(x0+w,184,"6000",11,MUTED,"end"))
    b.append(f'<line x1="{x0+w/2-1}" x2="{x0+w/2-1}" y1="68" y2="176" stroke="{ORANGE}" stroke-dasharray="4 3"/>')
    # consistent / conflict
    b.append(T(x0,236,"两种世界",13,INK,"start","bold"))
    b.append(T(x0,264,"相似气味同奖励",12.5,INK,"start","bold")+T(x0,282,"A、A′、A″ 同一个符号，B 家族相反",12,MUTED))
    for i,c in enumerate([TEAL,TEAL,TEAL,VIOLET,VIOLET,VIOLET]): b.append(f'<circle cx="{x0+300+i*14}" cy="270" r="5" fill="{c}"/>')
    b.append(T(x0,318,"相似气味奖励相反",12.5,INK,"start","bold")+T(x0,336,"A 与 A′ 符号相反：只靠“长得像”会学错",12,MUTED))
    for i,c in enumerate([TEAL,VIOLET,TEAL,VIOLET,TEAL,VIOLET]): b.append(f'<circle cx="{x0+300+i*14}" cy="324" r="5" fill="{c}"/>')
    b.append(T(x0,372,"吃到 +1 或 −1，吃过的源 30 步内不再给奖励",11.5,MUTED))
    return svg(W,H+80,"".join(b))
def hbars(title,rows,series,colors,maxv,x0=210,w=330,y0=60,fmt=lambda v:f"+{v:.1f}",bh=15):
    b=[T(x0+w/2,y0-26,title,14,INK,"middle","bold")]; yy=y0
    for lab,vals in rows:
        b.append(T(x0-10,yy+bh+2,lab,13,INK,"end"))
        for j,v in enumerate(vals):
            ww=max(0,v/maxv*w); b.append(f'<rect x="{x0}" y="{yy+j*(bh+3)}" width="{ww}" height="{bh}" rx="2" fill="{colors[j]}"/>'+T(x0+ww+6,yy+j*(bh+3)+bh-3,fmt(v),11.5,MUTED))
        yy+=len(vals)*(bh+3)+14
    return "".join(b),yy
def fig6():
    rows=[("真实连线",[44.0,35.9]),("打乱连线",[44.4,32.4]),("随机稀疏连线",[50.9,44.1]),("线性学习器",[46.2,31.5]),("不学习",[0.5,0.9])]
    body,yy=hbars("单只果蝇：6000 步的平均净奖励（200 个新世界）",rows,2,[BLUE,ORANGE],60,x0=170,w=520)
    body+=f'<rect x="750" y="48" width="12" height="12" fill="{BLUE}"/>'+T(768,59,"相似气味同奖励",12,MUTED)+f'<rect x="750" y="68" width="12" height="12" fill="{ORANGE}"/>'+T(768,79,"相似气味奖励相反",12,MUTED)
    body+=T(520,yy+10,"真实 − 打乱：−0.4 [−3.6, +2.8] / +3.5 [0.0, +6.9]　　真实 − 随机稀疏：−6.9 / −8.3（区间都在 0 的一侧）",12,MUTED,"middle")
    return svg(1040,yy+36,body)
def fig7():
    rows=[("独立（无通信）",[274.2]),("手写：聚在一起",[211.0]),("观察学习",[353.5]),("广播（非生物）",[411.6]),("蚁群",[187.9]),("单只果蝇",[42.9])]
    b1,yy=hbars("20 只个体的总净奖励（相似气味同奖励，100 个新世界）",rows,1,[BLUE],450,x0=160,w=300)
    # crowding curve
    xs=[1,5,10,20,40]; per=[41.7,32.9,22.5,13.8,6.7]; tot=[41.7,164.4,224.7,275.6,267.6]
    cx,cy,cw,ch=620,70,360,220; b2=[T(cx+cw/2,cy-34,"拥挤：独立果蝇群的规模曲线",14,INK,"middle","bold"),f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="none" stroke="{LINE}"/>']
    X=lambda n:cx+ (xs.index(n))*cw/4; Yt=lambda v:cy+ch-v/300*ch
    for g in (0,100,200,300): b2.append(f'<line x1="{cx}" x2="{cx+cw}" y1="{Yt(g)}" y2="{Yt(g)}" stroke="{LINE}" stroke-dasharray="2 3"/>'+T(cx-6,Yt(g)+4,str(g),11,MUTED,"end"))
    pt=lambda arr:" ".join(f"{X(n)},{Yt(v)}" for n,v in zip(xs,arr))
    b2.append(f'<polyline points="{pt(tot)}" fill="none" stroke="{BLUE}" stroke-width="2.5"/><polyline points="{pt(per)}" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')
    for n,v in zip(xs,tot): b2.append(f'<circle cx="{X(n)}" cy="{Yt(v)}" r="4" fill="{BLUE}"/>')
    for n,v in zip(xs,per): b2.append(f'<circle cx="{X(n)}" cy="{Yt(v)}" r="4" fill="{ORANGE}"/>')
    for n in xs: b2.append(T(X(n),cy+ch+18,str(n),12,MUTED,"middle"))
    b2.append(T(cx+cw/2,cy+ch+38,"群体大小（只）",12,MUTED,"middle")+T(cx+cw-6,Yt(tot[-1])-10,"总量",12,BLUE,"end","bold")+T(cx+cw-6,Yt(per[-1])-8,"每只",12,ORANGE,"end","bold"))
    return svg(1040,max(yy,cy+ch+60)+30,b1+"".join(b2))
open("fig5_world.svg","w").write(fig5()); open("fig6_single_fly.svg","w").write(fig6()); open("fig7_swarm.svg","w").write(fig7())

# ---------------------------------------------------------------- figures 8-10: continual-learning audit post
def fig8():
    W,H=1040,230; b=[T(520,30,"FlyModel 做了什么",15,INK,"middle","bold")]
    steps=[("冻结的特征","84 维（MNIST）/ 512 维（CIFAR）","由别的网络提前训练好"),("随机稀疏投影","3200 / 20000 个单元","每个单元随机连几个输入"),("只留最强 5%","k-WTA（类似 KC 稀疏编码）","其余置 0"),("按类累加","每个类一个权重向量","= 该类稀疏特征之和")]
    bw,gap=215,36
    for i,(t,a,c) in enumerate(steps):
        x=20+i*(bw+gap); b.append(f'<rect x="{x}" y="60" width="{bw}" height="100" rx="8" fill="{SOFT}" stroke="{BLUE}"/>'+T(x+bw/2,90,t,14.5,INK,"middle","bold")+T(x+bw/2,114,a,12,MUTED,"middle")+T(x+bw/2,134,c,12,MUTED,"middle"))
        if i<3: b.append(arrow(x+bw+3,110,x+bw+gap-3,110))
    b.append(T(520,196,"预测：哪个类的权重向量与输入的稀疏特征点积最大。每个类的权重互不相干，所以“旧类不被覆盖”几乎是构造出来的。",12.5,ORANGE,"middle"))
    return svg(W,H,"".join(b))
def vbars(title,groups,series,colors,maxv,fmt,W=1040,H=380,note=None):
    b=[T(W/2,30,title,15,INK,"middle","bold")]; x0,y0,pw,ph=70,60,W-110,H-130
    for g in range(0,int(maxv*100)+1,20):
        v=g/100; y=y0+ph-v/maxv*ph; b.append(f'<line x1="{x0}" x2="{x0+pw}" y1="{y}" y2="{y}" stroke="{LINE}" stroke-dasharray="2 3"/>'+T(x0-8,y+4,f"{g}%",11,MUTED,"end"))
    gw=pw/len(groups); bw=min(34,(gw-30)/len(series))
    for i,(lab,vals) in enumerate(groups):
        gx=x0+i*gw+(gw-bw*len(series))/2
        for j,v in enumerate(vals):
            h=v/maxv*ph; b.append(f'<rect x="{gx+j*bw}" y="{y0+ph-h}" width="{bw-3}" height="{h}" rx="2" fill="{colors[j]}"/>'+T(gx+j*bw+(bw-3)/2,y0+ph-h-5,fmt(v),10.5,MUTED,"middle"))
        b.append(T(x0+i*gw+gw/2,y0+ph+22,lab,13,INK,"middle"))
    lx=x0
    for j,sn in enumerate(series): b.append(f'<rect x="{lx}" y="{H-34}" width="12" height="12" fill="{colors[j]}"/>'+T(lx+18,H-24,sn,12,MUTED)); lx+=24+len(sn)*13
    return svg(W,H,"".join(b))
def fig9():
    g=[("MNIST-20",[.707,.760,.601,.622,.872]),("CIFAR-100 简单特征",[.340,.400,.273,.069,.437]),("CIFAR-100 强特征",[.508,.639,.533,.162,.677])]
    return vbars("学完全部类别后的最终准确率（5 个种子）",g,["FlyModel（论文设定）","SLDA（免回放）","最近类均值","最佳反向传播基线*","离线上界"],[BLUE,TEAL,GREY,ORANGE,"#6b7a86"],0.95,lambda v:f"{100*v:.0f}",H=400)
def fig10():
    g=[("MNIST-20",[.562,.033]),("CIFAR 简单特征",[.127,.02]),("CIFAR 强特征",[.067,-0.01])]
    W,H=760,380; b=[T(W/2,30,"FlyModel 比稠密对照好多少？（准确率差）",15,INK,"middle","bold")]; x0,y0,pw,ph=70,60,W-110,H-130; mx=0.6
    zero=y0+ph*0.97/1.0
    for gv in (0,0.2,0.4,0.6):
        y=y0+ph-(gv+0.03)/(mx+0.03)*ph; b.append(f'<line x1="{x0}" x2="{x0+pw}" y1="{y}" y2="{y}" stroke="{LINE}" stroke-dasharray="2 3"/>'+T(x0-8,y+4,f"{gv:+.1f}" if gv else "0",11,MUTED,"end"))
    Y=lambda v:y0+ph-(v+0.03)/(mx+0.03)*ph; gw=pw/3
    for i,(lab,vals) in enumerate(g):
        gx=x0+i*gw+gw/2-45
        for j,(v,c) in enumerate(zip(vals,[ORANGE,TEAL])):
            y1,y2=sorted([Y(0),Y(v)]); b.append(f'<rect x="{gx+j*48}" y="{y1}" width="42" height="{max(y2-y1,1.5)}" rx="2" fill="{c}"/>'+T(gx+j*48+21,(Y(v)-6 if v>=0 else Y(v)+16),f"{v:+.2f}",11,MUTED,"middle"))
        b.append(T(x0+i*gw+gw/2,y0+ph+24,lab,13,INK,"middle"))
    b.append(f'<rect x="{x0}" y="{H-34}" width="12" height="12" fill="{ORANGE}"/>'+T(x0+18,H-24,"论文式对照：稠密 + 类和点积",12,MUTED)+f'<rect x="{x0+250}" y="{H-34}" width="12" height="12" fill="{TEAL}"/>'+T(x0+268,H-24,"同一个最近类均值分类器下的稀疏 − 稠密（探索性）",12,MUTED))
    return svg(W,H,"".join(b))
open("fig8_flymodel.svg","w").write(fig8()); open("fig9_audit_accuracy.svg","w").write(fig9()); open("fig10_sparse_vs_dense.svg","w").write(fig10())

# ---------------------------------------------------------------- figures 11-13: meta-learning post
def fig11():
    W,H=1040,300; b=[T(520,30,"两层循环：外层进化，内层觅食",15,INK,"middle","bold")]
    b.append(f'<rect x="30" y="56" width="980" height="200" rx="10" fill="none" stroke="{ORANGE}" stroke-dasharray="5 4"/>'+T(60,80,"外层：进化策略（25 代）",13,ORANGE,"start","bold"))
    items=[("5 个参数的中心点 θ","正/负误差学习率、遗忘速率、","KC 稀疏度、价值的转向权重"),("加噪声，得到 16 个候选","8 对对偶（+ε 和 −ε）",""),("每个候选去觅食","12 个训练世界，反转周期","取自 1000 / 2000 / 3000（内层）"),("按平均净奖励排名","只用排名，不用数值","")]
    bw,gap=215,36
    for i,(t,a,c) in enumerate(items):
        x=55+i*(bw+gap); col=TEAL if i==2 else BLUE
        b.append(f'<rect x="{x}" y="100" width="{bw}" height="100" rx="8" fill="{SOFT}" stroke="{col}"/>'+T(x+bw/2,128,t,14,INK,"middle","bold")+T(x+bw/2,152,a,12,MUTED,"middle")+T(x+bw/2,170,c,12,MUTED,"middle"))
        if i<3: b.append(arrow(x+bw+3,150,x+bw+gap-3,150))
    b.append(f'<path d="M {55+3*(bw+gap)+bw/2} 202 L {55+3*(bw+gap)+bw/2} 232 L {55+bw/2} 232 L {55+bw/2} 206" fill="none" stroke="{ORANGE}" stroke-width="1.8"/><polygon points="{55+bw/2},202 {55+bw/2-5},212 {55+bw/2+5},212" fill="{ORANGE}"/>')
    b.append(T(520,250,"沿排名高的方向移动 θ，进入下一代",12.5,ORANGE,"middle"))
    b.append(T(520,284,"评估：最后一代的中心点，在 100 个从未用过的世界上与手调默认值配对比较",12,MUTED,"middle"))
    return svg(W,H,"".join(b))
def fig12():
    rows=[("真实连线",[(+6.0,1.1,11.0),(+2.6,-1.9,7.2),(+4.2,-0.2,8.7)]),("打乱连线",[(+4.8,0.9,8.6),(+5.2,1.2,9.6),(+4.9,0.7,9.2)]),("随机稀疏连线",[(+3.6,-0.9,8.1),(+8.9,3.7,13.9),(+8.0,2.8,13.2)])]
    W,H=1040,470; x0,w=190,780; mx=16.0; X=lambda v:x0+(v+2)/(mx+2)*w
    b=[T(520,30,"进化后 − 手调默认值：净奖励的提升（in-dist，100 个留出世界）",15,INK,"middle","bold")]
    for g in (0,6,12): b.append(f'<line x1="{X(g)}" x2="{X(g)}" y1="56" y2="390" stroke="{LINE if g!=6 else ORANGE}" stroke-dasharray="{"2 3" if g!=6 else "5 3"}"/>'+T(X(g),408,("+%d"%g) if g else "0",11.5,ORANGE if g==6 else MUTED,"middle"))
    b.append(T(X(6)+4,52,"预设门槛 +6",11.5,ORANGE,"start"))
    y=76
    for lab,vals in rows:
        b.append(T(x0-14,y+44,lab,13.5,INK,"end","bold"))
        for k,(m,lo,hi) in enumerate(vals):
            yy=y+k*30; b.append(f'<line x1="{X(lo)}" x2="{X(hi)}" y1="{yy+10}" y2="{yy+10}" stroke="{BLUE}" stroke-width="3" opacity=".75"/><circle cx="{X(m)}" cy="{yy+10}" r="5" fill="{BLUE}"/>'+T(X(hi)+8,yy+14,f"{m:+.1f}",11.5,MUTED))
        y+=100
    b.append(T(520,444,"每行三个点是三次独立进化；线是 95% 区间（只对世界做了自助法，不含进化本身的方差）",12,MUTED,"middle"))
    return svg(W,H,"".join(b))
def fig13():
    data={"real":{"c":BLUE,"v":[[.47,.54,.63],[.64,.67,.73],[.020,.024,.020],[1.32,1.72,1.88]]},"shuffled":{"c":ORANGE,"v":[[.45,.34,.48],[.56,.66,.71],[.024,.022,.021],[2.17,1.28,1.57]]},"random":{"c":TEAL,"v":[[.68,.44,.71],[.60,.72,.62],[.019,.018,.017],[1.71,1.79,1.73]]}}
    labs=[("正误差学习率",0.4,0.0,1.0),("负误差学习率",0.4,0.0,1.0),("KC 稀疏度",0.05,0.0,0.06),("价值的转向权重",2.0,0.0,2.5)]
    W,H=1040,330; b=[T(520,28,"9 次进化的最终参数（点）与手调默认值（虚线）",15,INK,"middle","bold")]
    pw=210
    for i,(lab,dflt,lo,hi) in enumerate(labs):
        x0=40+i*(pw+22); b.append(f'<rect x="{x0}" y="56" width="{pw}" height="210" fill="none" stroke="{LINE}"/>'+T(x0+pw/2,46,lab,13,INK,"middle","bold"))
        Y=lambda v:56+210-(v-lo)/(hi-lo)*210
        b.append(f'<line x1="{x0}" x2="{x0+pw}" y1="{Y(dflt)}" y2="{Y(dflt)}" stroke="{INK}" stroke-dasharray="5 3"/>'+T(x0+4,Y(dflt)-5,f"默认 {dflt:g}",11,MUTED,"start"))
        for j,(k,d) in enumerate(data.items()):
            for m,v in enumerate(d["v"][i]): b.append(f'<circle cx="{x0+40+j*65+(m-1)*12}" cy="{Y(v)}" r="5.5" fill="{d["c"]}"/>')
        for j,k in enumerate(data): b.append(T(x0+40+j*65,284,{"real":"真实","shuffled":"打乱","random":"随机"}[k],11.5,MUTED,"middle"))
    b.append(T(520,316,"遗忘速率：9 次全部停在搜索范围的下界（1e-5），没有一次选择遗忘",12.5,ORANGE,"middle"))
    return svg(W,H,"".join(b))
open("fig11_evolution_loop.svg","w").write(fig11()); open("fig12_evolved_gain.svg","w").write(fig12()); open("fig13_evolved_params.svg","w").write(fig13())

# ---------------------------------------------------------------- figures 14-16: TSP post
def fig14():
    import random as _r; r=_r.Random(5); W,H=1040,330; pts=[(60+r.random()*300,70+r.random()*190) for _ in range(9)]
    import math as _m; cx_=sum(p[0] for p in pts)/9; cy_=sum(p[1] for p in pts)/9; tour=sorted(range(9),key=lambda i:_m.atan2(pts[i][1]-cy_,pts[i][0]-cx_)); b=[T(210,30,"旅行商问题：走一圈，经过每个城市，越短越好",14,INK,"middle","bold")]
    b.append(f'<rect x="30" y="46" width="360" height="240" rx="8" fill="#f7f9fb" stroke="{LINE}"/>')
    for i in range(len(tour)):
        a=pts[tour[i]]; c=pts[tour[(i+1)%len(tour)]]; b.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{c[0]}" y2="{c[1]}" stroke="{BLUE}" stroke-width="2.2" opacity=".8"/>')
    for x,y in pts: b.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{INK}"/>')
    b.append(T(210,308,"一条路线 = 一只蚂蚁走完一圈",12,MUTED,"middle"))
    b.append(T(720,30,"蚂蚁在每个城市怎么选下一站",14,INK,"middle","bold"))
    b.append(T(720,76,"权重 =  τ^α  ×  η^β  ×  exp(κ · v)",21,INK,"middle","bold"))
    items=[("τ 信息素",ORANGE,"这一次搜索里，别的蚂蚁留下的痕迹","（实例内学，每条边一个数）"),("η = 1 / 距离",GREY,"越近越想去","（固定的先验）"),("v 学到的边价值",BLUE,"跨实例训练的蘑菇体给出","（v = 0 就是普通蚁群）")]
    for i,(t,c,a,d) in enumerate(items):
        y=110+i*62; b.append(f'<rect x="460" y="{y}" width="12" height="44" fill="{c}"/>'+T(484,y+16,t,14,INK,"start","bold")+T(484,y+34,a+" "+d,11.5,MUTED))
    b.append(T(720,310,"我们只换最后一项 v 的来源，其余不动",12.5,BLUE,"middle","bold"))
    return svg(W,H,"".join(b))
def fig15():
    g=[("R1 均匀 50 城",[1.81,1.75,1.73,1.80,1.78,2.41,7.23]),("R2 均匀 100 城",[2.31,2.27,2.20,2.32,2.28,4.05,11.81]),("R3 聚类 50 城",[3.64,3.38,3.39,3.53,3.44,4.31,9.11])]
    names=["普通蚁群","在线学习·真实","在线学习·随机稀疏","在线学习·线性","4 个异质回路","4 个子蚁群不交换","去掉信息素"]
    cols=[GREY,BLUE,TEAL,"#7a9fd1","#4a64b8",ORANGE,"#8a3d2a"]
    W,H=1040,400; b=[T(520,30,"路线比参考解长多少 %（越低越好；300 个测试实例）",15,INK,"middle","bold")]; x0,y0,pw,ph=70,56,W-110,H-140; mx=12.5
    for v in (0,3,6,9,12): y=y0+ph-v/mx*ph; b.append(f'<line x1="{x0}" x2="{x0+pw}" y1="{y}" y2="{y}" stroke="{LINE}" stroke-dasharray="2 3"/>'+T(x0-8,y+4,f"{v}%",11,MUTED,"end"))
    gw=pw/3; bw=30
    for i,(lab,vals) in enumerate(g):
        gx=x0+i*gw+(gw-bw*7)/2
        for j,v in enumerate(vals):
            h=v/mx*ph; b.append(f'<rect x="{gx+j*bw}" y="{y0+ph-h}" width="{bw-3}" height="{h}" rx="2" fill="{cols[j]}"/>'+T(gx+j*bw+(bw-3)/2,y0+ph-h-5,f"{v:.1f}",10,MUTED,"middle"))
        b.append(T(x0+i*gw+gw/2,y0+ph+20,lab,13,INK,"middle"))
    lx,ly=x0,H-52
    for j,n in enumerate(names):
        cx=lx+(j%4)*245; cy=ly+(j//4)*20; b.append(f'<rect x="{cx}" y="{cy}" width="12" height="12" fill="{cols[j]}"/>'+T(cx+18,cy+11,n,12,MUTED))
    return svg(W,H,"".join(b))
def fig16():
    rows=[("v1","MB-真实 − 蚁群 · R1",-0.21,-0.59,0.14),("v1","MB-真实 − 蚁群 · R2",-0.33,-0.72,0.05),
          ("v2","在线真实 − 蚁群 · R1",-0.05,-0.21,0.11),("v2","在线真实 − 蚁群 · R2",-0.04,-0.24,0.15),("v2","在线真实 − 蚁群 · R3",-0.26,-0.44,-0.07),("v2","在线真实 − 蚁群 · R4(2-opt)",-0.01,-0.09,0.07),
          ("v2","异质 − 同质 · R1",0.05,-0.09,0.19),("v2","异质 − 同质 · R2",0.00,-0.19,0.19),("v2","异质 − 同质 · R3",0.07,-0.09,0.25),("v2","异质 − 同质 · R4",0.02,-0.03,0.09),
          ("v3","转角学习 − 蚁群 · R1",-0.01,-0.15,0.14),("v3","转角学习 − 蚁群 · R2",0.03,-0.15,0.22),("v3","转角学习 − 蚁群 · R3",-0.18,-0.37,0.00)]
    W=1040; H=80+len(rows)*26+70; x0,w=420,560; R=0.8; X=lambda v:x0+(v+R)/(2*R)*w
    b=[T(520,30,"主要对比：学习器 − 对照（百分点；负 = 学习器路线更短）",15,INK,"middle","bold")]
    b.append(f'<rect x="{X(-0.5)}" y="52" width="{X(0.5)-X(-0.5)}" height="{len(rows)*26+6}" fill="{SOFT}"/>'+T(X(0),48,"等价区（±0.5；R4 为 ±0.25）",11,MUTED,"middle"))
    b.append(f'<line x1="{X(0)}" x2="{X(0)}" y1="52" y2="{58+len(rows)*26}" stroke="{MUTED}" stroke-dasharray="3 3"/>')
    cmap={"v1":GREY,"v2":BLUE,"v3":TEAL}
    for i,(v,lab,m,lo,hi) in enumerate(rows):
        y=64+i*26; c=cmap[v]
        b.append(T(x0-14,y+5,lab,12.5,INK,"end")+f'<line x1="{X(lo)}" x2="{X(hi)}" y1="{y}" y2="{y}" stroke="{c}" stroke-width="3"/><circle cx="{X(m)}" cy="{y}" r="4.5" fill="{c}"/>')
    yy=64+len(rows)*26+10
    for v,lab,xx in (("v1","第一轮（100 个实例）",x0),("v2","第二轮（300 个实例）",x0+190),("v3","第三轮（300 个实例）",x0+390)): b.append(f'<circle cx="{xx}" cy="{yy+14}" r="5" fill="{cmap[v]}"/>'+T(xx+10,yy+18,lab,12,MUTED))
    for t in (-0.5,0,0.5): b.append(T(X(t),yy-2,f"{t:+.1f}" if t else "0",11,MUTED,"middle"))
    return svg(W,H,"".join(b))
open("fig14_tsp_aco.svg","w").write(fig14()); open("fig15_tsp_results.svg","w").write(fig15()); open("fig16_tsp_forest.svg","w").write(fig16())

# ---------------------------------------------------------------- figures 17-18: wrap-up post
def fig17():
    rows=[("觅食（单只果蝇）",["eq:等价 / 不确定","worse:随机更好","eq:等价 / 真实略好（不稳）"]),
          ("元学习（进化后）",["eq:等价 / 不确定","worse:随机更好（3 次里 2 次）","na:未比较"]),
          ("旅行商 第一轮",["eq:等价","eq:等价","eq:等价"]),
          ("旅行商 第二轮",["blind:等价（设计测不出）","blind:等价（设计测不出）","blind:等价（设计测不出）"]),
          ("旅行商 第三轮",["blind:等价（未学到转角）","blind:等价（未学到转角）","blind:等价（未学到转角）"]),
          ("隔间与遗忘",["na:真实 vs 打乱隔间：未确认","na:—","na:—"])]
    cols=["真实 vs 打乱连线","真实 vs 随机稀疏连线","真实 vs 线性学习器"]
    fills={"eq":("#e3ebf3",INK),"worse":("#f6d9cc",ORANGE),"blind":("#fff4cc","#8a6d00"),"na":("#f3f3f3",MUTED)}
    W=1040; H=120+len(rows)*58+90; x0=230; cw=270; b=[T(520,32,"证据地图：真实连线对各种对照",15,INK,"middle","bold")]
    for j,c in enumerate(cols): b.append(T(x0+j*cw+cw/2-6,78,c,13,INK,"middle","bold"))
    for i,(lab,cells) in enumerate(rows):
        y=92+i*58; b.append(T(x0-14,y+30,lab,13.5,INK,"end","bold"))
        for j,cell in enumerate(cells):
            k,t=cell.split(":"); f,c=fills[k]; b.append(f'<rect x="{x0+j*cw}" y="{y}" width="{cw-12}" height="46" rx="6" fill="{f}"/>'+T(x0+j*cw+(cw-12)/2,y+28,t,12.5,c,"middle"))
    ly=92+len(rows)*58+16
    for n,(k,t) in enumerate((("eq","区间落在等价界内"),("worse","对照明显更好"),("blind","等价，但设计测不出效应"),("na","没做这个比较"))):
        f,c=fills[k]; x=x0+n*210; b.append(f'<rect x="{x}" y="{ly}" width="14" height="14" rx="3" fill="{f}" stroke="{LINE}"/>'+T(x+20,ly+12,t,12,MUTED))
    b.append(T(520,ly+54,"没有一格是“真实连线明显更好”。",14,INK,"middle","bold"))
    return svg(W,H,"".join(b))
def fig18():
    W,H=1040,260; b=[T(520,32,"下一步：先做阳性对照，再谈连线",15,INK,"middle","bold")]
    steps=[("① 植入已知规律","在任务里放一个“只有气味组合","才有奖励”的结构"),("② 看学习器能不能检出","能检出：设置可信","检不出：先修设置"),("③ 再比较连线","真实 / 打乱 / 随机稀疏 / 线性","这时的“没差别”才有分量")]
    bw,gap=290,50
    for i,(t,a,c) in enumerate(steps):
        x=40+i*(bw+gap); col=TEAL if i==1 else BLUE; b.append(f'<rect x="{x}" y="70" width="{bw}" height="110" rx="8" fill="{SOFT}" stroke="{col}"/>'+T(x+bw/2,102,t,15,INK,"middle","bold")+T(x+bw/2,132,a,12.5,MUTED,"middle")+T(x+bw/2,152,c,12.5,MUTED,"middle"))
        if i<2: b.append(arrow(x+bw+4,125,x+bw+gap-4,125))
    b.append(T(520,222,"另外两个补充：用真实的个体差异（不同果蝇的连线）；用多巴胺时序规则和效价专门化的隔间重做。",12.5,MUTED,"middle"))
    return svg(W,H,"".join(b))
open("fig17_evidence_map.svg","w").write(fig17()); open("fig18_next_step.svg","w").write(fig18())

# ---------------------------------------------------------------- figure 19: forgetting sweep (follow-up to post 5)
def fig19():
    xs=["0","1e-4","1e-3","3e-3","1e-2","3e-2"]
    ser=[("fast（反转周期 500）",[5.2,4.9,8.8,17.4,17.7,8.5],ORANGE),("in-dist（1000/2000/3000）",[28.0,25.6,38.2,37.4,25.9,10.8],BLUE),("stationary（不反转）",[68.6,64.7,55.7,44.6,27.9,13.8],TEAL)]
    W,H=1040,430; x0,y0,pw,ph=90,60,W-150,260; mx=80
    b=[T(520,30,"给学习器加上“遗忘”，在不同世界里净奖励怎么变",15,INK,"middle","bold")]
    for v in range(0,81,20): y=y0+ph-v/mx*ph; b.append(f'<line x1="{x0}" x2="{x0+pw}" y1="{y}" y2="{y}" stroke="{LINE}" stroke-dasharray="2 3"/>'+T(x0-8,y+4,str(v),11,MUTED,"end"))
    X=lambda i:x0+40+i*(pw-80)/5
    b.append(f'<rect x="{X(0)-30}" y="{y0}" width="76" height="{ph}" fill="#fbe9e1" opacity=".7"/>'+T(X(0)+8,y0+16,"进化停在这里",11.5,ORANGE,"middle"))
    for name,vals,c in ser:
        pts=" ".join(f"{X(i)},{y0+ph-v/mx*ph}" for i,v in enumerate(vals)); b.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2.6"/>')
        for i,v in enumerate(vals): b.append(f'<circle cx="{X(i)}" cy="{y0+ph-v/mx*ph}" r="4.5" fill="{c}"/>'+T(X(i),y0+ph-v/mx*ph-9,f"{v:.0f}",10.5,MUTED,"middle"))
    for i,lab in enumerate(xs): b.append(T(X(i),y0+ph+20,lab,12,INK,"middle"))
    b.append(T(x0+pw/2,y0+ph+44,"遗忘速率（每步向初值回落的比例；0 = 不遗忘）",12.5,MUTED,"middle"))
    lx=x0
    for name,vals,c in ser: b.append(f'<rect x="{lx}" y="{H-34}" width="12" height="12" fill="{c}"/>'+T(lx+18,H-24,name,12.5,MUTED)); lx+=250
    return svg(W,H,"".join(b))
open("fig19_forgetting_sweep.svg","w").write(fig19())

def fig20():
    W,H=900,380; groups=[("原分布（in-dist）",6.6,18.1),("更波动（fast）",1.7,8.3),("不反转（stationary）",7.7,-10.6)]
    x0,y0,pw,ph=80,60,W-120,220; lo,hi=-15,25; Y=lambda v:y0+ph-(v-lo)/(hi-lo)*ph
    b=[T(W/2,30,"进化相对手调默认值的提升（三种连线的平均净奖励差）",15,INK,"middle","bold")]
    for v in (-10,0,10,20): b.append(f'<line x1="{x0}" x2="{x0+pw}" y1="{Y(v)}" y2="{Y(v)}" stroke="{LINE if v else MUTED}" stroke-dasharray="{"2 3" if v else "0"}"/>'+T(x0-8,Y(v)+4,f"{v:+d}" if v else "0",11,MUTED,"end"))
    gw=pw/3
    for i,(lab,a,c) in enumerate(groups):
        gx=x0+i*gw+gw/2-52
        for j,(v,col) in enumerate(((a,GREY),(c,BLUE))):
            y1,y2=sorted([Y(0),Y(v)]); b.append(f'<rect x="{gx+j*56}" y="{y1}" width="48" height="{y2-y1}" rx="2" fill="{col}"/>'+T(gx+j*56+24,(Y(v)-6 if v>=0 else Y(v)+16),f"{v:+.1f}",11.5,MUTED,"middle"))
        b.append(T(x0+i*gw+gw/2,y0+ph+34,lab,13,INK,"middle"))
    b.append(f'<rect x="{x0}" y="{H-30}" width="12" height="12" fill="{GREY}"/>'+T(x0+18,H-20,"第一次进化（遗忘被卡在 1e-5）",12,MUTED)+f'<rect x="{x0+300}" y="{H-30}" width="12" height="12" fill="{BLUE}"/>'+T(x0+318,H-20,"重跑（遗忘起点在中段）",12,MUTED))
    return svg(W,H,"".join(b))
open("fig20_meta_rerun.svg","w").write(fig20())

open("fig1_circuit.svg","w").write(fig1()); open("fig2_controls.svg","w").write(fig2()); print("ok")
