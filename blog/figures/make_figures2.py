"""Figures 21-24 for blog posts 07-10 (numbers copied from fly-v4/RESULTS_v4_stage*.md and verification/replication/*)."""
src=open("make_figures.py").read().split("# ---------------------------------------------------------------- figure 1")[0]
exec(src)
def ciplot(title,rows,xmin,xmax,ticks,note,band=None,W=1040,rowh=34,x0=330,series=None,colors=None):
    """rows: (label, [(mean,lo,hi) per series]); band=(lo,hi) shaded equivalence band"""
    yend=84+sum(rowh*len(v)+10 for _,v in rows); H=yend+80; w=W-x0-70; X=lambda v:x0+(v-xmin)/(xmax-xmin)*w
    colors=colors or [BLUE,ORANGE,TEAL]; b=[T(W/2,28,title,15,INK,"middle","bold")]
    if band: b.append(f'<rect x="{X(band[0])}" y="52" width="{X(band[1])-X(band[0])}" height="{yend-52}" fill="{SOFT}"/>'+T(X(band[1])-4,66,"阴影：±0.03，最小有意义效应",11,MUTED,"end"))
    for t in ticks: b.append(f'<line x1="{X(t)}" x2="{X(t)}" y1="52" y2="{yend}" stroke="{LINE if t else MUTED}" stroke-dasharray="{"2 3" if t else "0"}"/>'+T(X(t),yend+16,f"{t:+.2f}" if t else "0",11,MUTED,"middle"))
    y=84
    for lab,vals in rows:
        b.append(T(x0-12,y+rowh*len(vals)/2+3,lab,12.5,INK,"end"))
        for k,(m,lo,hi) in enumerate(vals):
            yy=y+k*rowh+rowh/2
            b.append(f'<line x1="{X(lo)}" x2="{X(hi)}" y1="{yy}" y2="{yy}" stroke="{colors[k]}" stroke-width="3" opacity=".8"/><circle cx="{X(m)}" cy="{yy}" r="4.6" fill="{colors[k]}"/>'+T(X(hi)+8,yy+4,f"{m:+.3f}",11,MUTED))
        y+=rowh*len(vals)+10
    ly=yend+38
    if series:
        lx=x0-200
        for j,sn in enumerate(series): b.append(f'<rect x="{lx}" y="{ly-10}" width="12" height="12" fill="{colors[j]}"/>'+T(lx+18,ly,sn,12,MUTED)); lx+=40+len(sn)*13
    b.append(T(W/2,yend+62,note,11.5,MUTED,"middle"))
    return svg(W,H,"".join(b))
def fig21():
    rows=[("教师被重排 30%：真实 − 打乱",[(.064,.058,.071),(.065,.060,.070)]),("教师被重排 30%：真实 − 随机稀疏",[(.066,.059,.074),(.064,.058,.070)]),
          ("教师是打乱连线：打乱 − 随机稀疏",[(.001,-.002,.005),(-.002,-.006,.002)]),("教师是打乱连线：打乱 − 真实",[(.018,.013,.023),(.020,.015,.026)])]
    return ciplot("非循环阳性对照：能检出连线实例，检不出统计类别",rows,-.02,.10,[0,.03,.06],"点是均值，线是区间（原实现 99.2%，重新实现 95%）。学习器的学习率固定 0.05。",band=(-.03,.03),series=["原实现（100 个世界）","独立重新实现（60 个世界）"])
def fig22():
    rows=[("2-shot 类别分类：真实 − 打乱",[(.006,-.010,.021)]),("2-shot 类别分类：真实 − 随机稀疏",[(.010,-.006,.024)]),("5-shot 类别分类：真实 − 打乱",[(.017,-.001,.036)]),("5-shot 类别分类：真实 − 随机稀疏",[(.020,.002,.040)]),("近邻保留：真实 − 打乱",[(-.026,-.033,-.019)]),("近邻保留：真实 − 随机稀疏",[(-.001,-.008,.006)])]
    return ciplot("自然气味（DoOR）上，真实连线的 KC 编码没有表示优势",rows,-.05,.06,[-.03,0,.03],"99.2% 区间，100 个世界；类别分类用最近质心，近邻保留是 5 近邻与 DoOR 空间的重合比例。",band=(-.03,.03))
def fig23():
    rows=[("教师雄（M_R）：雌（F_R）− 随机稀疏",[(.036,.030,.043),(.010,.005,.015)]),("教师雌（F_R）：雄（M_R）− 随机稀疏",[(.027,.022,.032),(.019,.014,.024)]),("教师雌（H_R）：雄 − 随机稀疏",[(.022,.017,.027)]),("教师雌（H_R）：雌 − 随机稀疏",[(.024,.019,.029)]),
          ("教师雄（M_R）：雌（F_R）− 保留输入总量",[(.006,.002,.010),(-.009,-.012,-.005)]),("教师雌（F_R）：雄（M_R）− 保留输入总量",[(-.002,-.006,.001),(-.007,-.011,-.003)]),("教师 H_R：M_R − 保留输入总量",[(.002,-.002,.006)]),("教师 H_R：F_R − 保留输入总量",[(.000,-.004,.004)])]
    return ciplot("另一只果蝇的真实连线：比随机稀疏好一点，与“只保留嗅小球输入总量”相当",rows,-.02,.06,[0,.03],"蓝：阶段 3（K = 2018）与阶段 3b；橙：独立重新实现（K = 1800）。教师 H_R 是 hemibrain 的雌果蝇。",band=(-.03,.03),series=["阶段 3 / 3b","独立重新实现"],rowh=26)
def fig24():
    W,H=1040,420; x0,y0,pw,ph=90,60,W-150,H-140; xmin,xmax,ymin,ymax=.78,1.0,.70,.87
    X=lambda v:x0+(v-xmin)/(xmax-xmin)*pw; Y=lambda v:y0+ph-(v-ymin)/(ymax-ymin)*ph
    g=[(.875,.785),(.902,.798),(.940,.802),(.973,.776),(.988,.745),(.974,.723),(.799,.608)]; c=[(.838,.774),(.852,.789),(.874,.813),(.905,.846),(.923,.843),(.902,.818),(.900,.816)]
    b=[T(W/2,30,"持续学习：同样的“刚学完”准确率下，最终保留多少",15,INK,"middle","bold")]
    for v in (.70,.75,.80,.85): b.append(f'<line x1="{x0}" x2="{x0+pw}" y1="{Y(v)}" y2="{Y(v)}" stroke="{LINE}" stroke-dasharray="2 3"/>'+T(x0-8,Y(v)+4,f"{v:.2f}",11,MUTED,"end"))
    for v in (.80,.85,.90,.95,1.0): b.append(T(X(v),y0+ph+20,f"{v:.2f}",11,MUTED,"middle"))
    for pts,col,name in ((g,GREY,"原规则（双向、全局）"),(c,BLUE,"隔间规则（只抑制、分簇）")):
        pts=[p for p in pts if p[1]>.65]; b.append('<polyline fill="none" stroke="%s" stroke-width="2" points="%s"/>'%(col," ".join(f"{X(a)},{Y(f)}" for a,f in pts)))
        for a,f in pts: b.append(f'<circle cx="{X(a)}" cy="{Y(f)}" r="4.5" fill="{col}"/>')
    b.append(f'<rect x="{x0}" y="{H-30}" width="12" height="12" fill="{GREY}"/>'+T(x0+18,H-20,"原规则（双向、全局）",12,MUTED)+f'<rect x="{x0+240}" y="{H-30}" width="12" height="12" fill="{BLUE}"/>'+T(x0+258,H-20,"隔间规则（只抑制、分簇）",12,MUTED))
    b.append(T(W/2,y0+ph+44,"横轴：刚学完某个任务时的准确率；纵轴：学完 4 个任务后对全部 40 个气味的准确率。学习率 1.0 的原规则点（0.80/0.61）略去。",11.5,MUTED,"middle"))
    return svg(W,H,"".join(b))
open("fig21_positive_control.svg","w").write(fig21()); open("fig22_natural_odours.svg","w").write(fig22()); open("fig23_individuals.svg","w").write(fig23()); open("fig24_cl_frontier.svg","w").write(fig24()); print("ok")
