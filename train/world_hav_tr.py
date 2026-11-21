BRICK=['#9C4A32','#A85A3E','#8E4430','#B86A4A']; PLAST=['#E8D2A8','#D9B88A','#C9D8C8','#E8C8B0','#B8C8D8','#F0E2C4','#D8A890']
SHUT=['#1F7A8C','#2B58C9','#2E8B6E','#C9452E','#E6A31C','#6C5FB0']; AWN=['#C9452E','#2E8B6E','#E6A31C','#2B58C9','#9E3B4E','#E07A2E','#16909E']
def haveli(x,yface,side,w,h,seed,shop=True,goods=True):
    """old-city house facing the lane. side=+1 north of lane (facade looking -y)"""
    r=random.Random(seed); brick=r.random()<.55; col=r.choice(BRICK) if brick else r.choice(PLAST)
    wall=M(col,.8,kind='concrete',sc=.28) if brick else M(col,.85,kind='wall'); d=6.0; yc=yface+side*d/2; fy=yface-side*.01
    B.box((x,yc,h/2),(w/2,d/2,h/2),wall,.02)
    trim=M(shade(col,.72) if brick else '#F2EDE2',.7); WOOD=M('#6B4026',.6,kind='wood',sc=2); DARK=M('#1E1A18',.9); GLASS=M('#3A4A5A',.2,spec=.8)
    B.box((x,fy-side*.06,h+.15),(w/2+.12,.18,.15),trim,.02)
    for i in range(int(w/1.1)):
        if r.random()<.5: B.box((x-w/2+.55+i*1.1,fy-side*.05,h+.42),(.3,.1,.12),trim,.02)
    # roof clutter
    if r.random()<.6: B.cyl((x+r.uniform(-w/3,w/3),yc+side*r.uniform(0,2),h+.6),.45,1.0,M(r.choice(['#2B2C33','#E8E4D8','#3E6FB0']),.5),seg=12)
    if r.random()<.4: seg((x-w/3,yc,h),(x-w/3,yc,h+2.4),.03,M('#5A5F66',.4,metal=.7))
    sh=r.choice(SHUT); SH=M(sh,.6,kind='wood',sc=2)
    for fl in range(1,int(h/3.1)):
        z=fl*3.1+1.4
        if z>h-.8: break
        n=max(1,int(w/2.4))
        for i in range(n):
            xx=x-w/2+w*(i+.5)/n
            if r.random()<.35:   # jharokha: carved wooden balcony
                B.box((xx,fy-side*.45,z-.75),(.85,.45,.1),WOOD,.03); B.box((xx,fy-side*.45,z+.95),(.9,.5,.08),WOOD,.04)
                for k in range(5): B.box((xx-.7+k*.35,fy-side*.88,z-.2),(.04,.04,.45),WOOD,.01)
                B.box((xx,fy-side*.88,z-.6),(.85,.04,.06),WOOD,.01); B.box((xx,fy-side*.02,z+.1),(.6,.02,.75),DARK,0)
                B.box((xx,fy-side*.45,z+1.12),(.6,.3,.12),WOOD,.06)
            else:
                B.box((xx,fy,z),(.45,.02,.65),GLASS if r.random()<.5 else DARK,0)
                B.box((xx,fy-side*.03,z+.75),(.55,.06,.08),trim,.01); B.box((xx,fy-side*.03,z-.72),(.55,.08,.05),trim,.01)
                for s in (-1,1): B.box((xx+s*.7,fy-side*.12,z),(.24,.03,.66),SH,.01,rot=(0,0,R(s*side*25)))
            if r.random()<.25: B.box((xx,fy-side*.2,z-.95),(.55,.2,.35),M('#C9CDD6',.4,metal=.5),.02)   # AC unit
    # ground floor
    if shop:
        aw=r.choice(AWN); B.box((x,fy-side*.02,1.35),(w/2-.35,.02,1.25),M('#2A2420',.9),0)
        B.box((x,fy-side*.7,2.75),(w/2-.2,.7,.04),M(aw,.7,kind='fabric'),.02,rot=(R(-14*side),0,0))
        for k in range(int(w/.8)): B.box((x-w/2+.4+k*.8,fy-side*1.38,2.6),(.18,.02,.16),M(aw if k%2 else '#F4F1EA',.7),.01)
        B.box((x,fy-side*.05,3.25),(w/2-.5,.04,.3),M(r.choice(['#F4F1EA','#F2C12E','#2E8B6E','#C9452E']),.5,emit=.15),.02)
        for k in range(r.randint(2,4)): B.box((x-w/2+.8+k*1.1,fy-side*.04,3.25),(.35,.01,.16),M(r.choice(['#C9452E','#1E1A18','#2B58C9']),.5),0)
        if goods: stall(x,fy-side*.9,side,w-1.0,r)
    else:
        B.box((x,fy-side*.02,1.25),(.75,.04,1.25),M(r.choice(SHUT),.6,kind='wood',sc=2),.02); B.box((x,fy-side*.06,2.6),(.95,.08,.14),trim,.02)
        for s in (-1,1): B.cyl((x+s*.95,fy-side*.12,1.3),.08,2.6,trim,seg=8)
        B.cyl((x,fy-side*.04,2.5),.75,.06,trim,rot=(R(90),0,0),seg=24)
        if r.random()<.6:
            for s in (-1,1): B.cyl((x+s*1.4,fy-side*.35,.3),.25,.6,M('#B8683A',.8),seg=10,r2=.32); B.ico((x+s*1.4,fy-side*.35,.85),.35,LEAF2,sub=1)
FRUIT=['#E2562E','#F2C12E','#5FA84A','#C9302C','#F28A2E','#7A3E9E']
def stall(x,y,side,w,r):
    T=M('#8A5A3A',.7,kind='wood',sc=3); B.box((x,y,.45),(w/2,.55,.45),T,.03)
    kind=r.choice(['fruit','spice','cloth','pots','sweets'])
    if kind=='fruit':
        for i in range(int(w/.55)):
            c=r.choice(FRUIT)
            for j in range(5): B.ico((x-w/2+.3+i*.55+r.uniform(-.1,.1),y+r.uniform(-.35,.35),.98+r.uniform(0,.12)),.09,M(c,.5),sub=1)
    elif kind=='spice':
        for i in range(int(w/.45)): B.cyl((x-w/2+.25+i*.45,y,1.05),.18,.3,M(r.choice(['#C9452E','#E6A31C','#8A5A2A','#F2C12E','#5A7A2E']),.9),seg=10,r2=.02)
    elif kind=='cloth':
        for i in range(int(w/.4)): B.box((x-w/2+.2+i*.4,y,1.0),(.17,.45,.1),M(r.choice(KUR),.85,kind='fabric'),.03)
        for i in range(int(w/.6)): B.box((x-w/2+.3+i*.6,y-side*.4,2.0),(.22,.02,.6),M(r.choice(KUR),.85,kind='fabric'),.01)
    elif kind=='pots':
        for i in range(int(w/.5)): B.cyl((x-w/2+.25+i*.5,y,1.06),.17,.22,M(r.choice(['#C9CDD6','#B8683A','#C9A24A']),.3,metal=.7),seg=12,r2=.12)
    else:
        for i in range(int(w/.5)): B.box((x-w/2+.25+i*.5,y,.98),(.2,.3,.06),M(r.choice(['#F2C12E','#F4F1EA','#E2562E','#D98AA8']),.6),.02)
