# Train trip sets: Karachi Cantt platform, train coaches, compartment interior, Lahore Junction, food street
GRN='#1F6B4A'; CRM='#E8DCB8'
def coach(x,y,L_=22.0,parent=None,seed=0,body=GRN):
    r=empty((x,y,0)) if parent is None else parent
    B_=M(body,.45,metal=.25); C_=M(CRM,.5); RF=M('#5A5F66',.5,metal=.4); GL=M('#2A3644',.12,spec=.9); TI=M('#1E1E22',.7)
    obox((0,0,2.35),(L_/2,1.45,1.35),B_,.08,r); obox((0,0,3.72),(L_/2-.1,1.42,.08),RF,.06,r)
    ocyl((0,0,3.6),1.42,L_-.2,RF,r,rot=(0,R(90),0),seg=20,sc=(1,1,.18)) if False else None
    for s in (-1,1):
        obox((0,s*1.46,2.0),(L_/2,.01,.12),C_,0,r)
        for k in range(int(L_/1.6)):
            xx=-L_/2+1.0+k*1.6
            obox((xx,s*1.465,2.85),(.55,.01,.38),GL,0,r); obox((xx,s*1.47,2.85),(.6,.008,.42),M('#C9CDD6',.3,metal=.7),0,r)
            for b in range(4): obox((xx-.45+b*.3,s*1.48,2.85),(.01,.01,.4),M('#3A3E44',.4,metal=.6),0,r)
        for xx in (-L_/2+.5,L_/2-.5): obox((xx,s*1.465,2.3),(.45,.01,1.0),M(shade(body,.8),.5),0,r)
    obox((0,0,.95),(L_/2-.8,1.2,.2),M('#2B2C33',.6),.02,r)
    for xx in (-L_/2+2.4,L_/2-2.4):
        obox((xx,0,.55),(1.2,1.1,.25),M('#2B2C33',.6,metal=.3),.02,r)
        for dx in (-.7,.7):
            for s in (-1,1): ocyl((xx+dx,s*.75,.48),.45,.12,TI,r,rot=(R(90),0,0),seg=16)
    t_=text('PAKISTAN RAILWAYS',(0,-1.47,2.0),(0,-1,0),.22,M('#E8DCB8',.5),ex=.004); t_.parent=r
    return r
def engine_car(x,y,parent=None):
    r=empty((x,y,0)) if parent is None else parent; B_=M('#2E6FB8',.4,metal=.3); Y_=M('#F2C12E',.5)
    obox((0,0,2.3),(9,1.45,1.4),B_,.1,r); obox((9.0,0,2.3),(.2,1.45,1.4),Y_,.05,r); obox((9.15,0,3.0),(.04,1.0,.4),M('#2A3644',.12,spec=.9),0,r)
    for s in (-1,1): obox((0,s*1.46,1.5),(9,.01,.12),Y_,0,r)
    obox((9.2,0,1.2),(.06,.3,.15),M('#FFF2C8',.3,emit=6),.01,r)
    for dx in (-6,-4.6,4.6,6):
        for s in (-1,1): ocyl((dx,s*.75,.48),.48,.12,M('#1E1E22',.7),r,rot=(R(90),0,0),seg=16)
    return r
def train(x0,y,n=4,parent_list=None):
    out=[]; e=empty((x0,y,0)); engine_car(0,0,parent=empty((0,0,0))).parent=e
    for i in range(n): c=coach(-10.5-11.1*i-11,0,L_=22.0); c.location=(-21.5-22.3*i,0,0); c.parent=e
    return e
def platform(name='KARACHI CANTT',x0=-40,x1=40,roof='#2E6FB8',col='#E2D6C0',seed=1,lahore=False):
    """platform along x, track at y=0, platform edge at y=-1.9 (platform y<-1.9), passengers side"""
    r=random.Random(seed); PL=M('#B8B0A0',.85,kind='concrete',sc=.6); EDGE=M('#F2C12E',.5)
    B.box(((x0+x1)/2,-6.0,.5),((x1-x0)/2,4.1,.5),PL,.02); B.box(((x0+x1)/2,-2.05,1.0),((x1-x0)/2,.18,.005),EDGE,0)
    B.box(((x0+x1)/2,0,-.05),((x1-x0)/2+30,14,.05),M('#6A6258',.95,kind='concrete',sc=.3),0)
    for yy in (-.72,.72,4.28,5.72):
        B.box(((x0+x1)/2,yy,.12),((x1-x0)/2+30,.05,.06),M('#8A8E96',.3,metal=.8),0)
    for k in range(int((x1-x0)/.7)): B.box((x0+k*.7,0,.04),(.12,1.2,.04),M('#5A4A3A',.85,kind='wood'),0); B.box((x0+k*.7,5,.04),(.12,1.2,.04),M('#5A4A3A',.85,kind='wood'),0)
    # canopy
    RM=M(roof,.5,metal=.3); CO=M('#C9CDD6',.4,metal=.5)
    for k in range(int((x1-x0)/6)+1):
        xx=x0+k*6; B.cyl((xx,-4.2,2.6),.12,4.2,CO,seg=10); B.box((xx,-4.2,5.0),(.1,3.3,.08),CO,0)
        if lahore: B.box((xx,-4.2,2.6),(.18,.18,2.6),M('#9C3A26',.8,kind='concrete',sc=.3),.02)
    B.box(((x0+x1)/2,-4.6,5.25),((x1-x0)/2,3.4,.12),RM,.02)
    for k in range(int((x1-x0)/4)): B.box((x0+2+k*4,-4.2,5.0),(.6,.05,.04),M('#F4FAFF',.3,emit=4),0)
    # back wall with doors/booths, benches, signs, stalls
    WL=M(col,.9,kind='wall'); B.box(((x0+x1)/2,-10.1,2.6),((x1-x0)/2,.1,2.6),WL,0)
    for k in range(int((x1-x0)/5)):
        xx=x0+2.5+k*5
        if k%3==0: B.box((xx,-10.0,1.2),(.9,.02,1.2),M('#5A3A22',.7,kind='wood'),0)
        elif k%3==1: B.box((xx,-10.0,1.6),(.8,.02,.6),M('#2A3644',.2,spec=.7),0)
        B.box((xx,-7.6,.95),(1.0,.25,.05),M('#2E6FB8' if not lahore else '#7A1E2E',.5),.02); B.box((xx,-7.8,1.25),(1.0,.04,.3),M('#2E6FB8' if not lahore else '#7A1E2E',.5),.02)
        for dx in (-.8,.8): B.box((xx+dx,-7.6,.72),(.05,.2,.22),M('#5A5F66',.5),0)
    for k in range(3):
        xx=x0+10+k*((x1-x0-20)/2)
        B.box((xx,-3.8,4.3),(1.6,.06,.38),M('#1F6B4A' if not lahore else '#F4F1EA',.5),.02); text(name,(xx,-3.86,4.3),(0,-1,0),.26,M('#F4F1EA' if not lahore else '#7A1E2E',.4),ex=.004)
        for dx in (-1.4,1.4): B.cyl((xx+dx,-3.8,4.8),.02,.6,M('#5A5F66',.5),seg=4)
    # tea stall + crates + water cooler
    B.box((x0+16,-8.6,1.1),(1.4,.8,1.1),M('#C0392B',.6),.03); B.box((x0+16,-7.75,1.6),(1.3,.04,.5),M('#2A2420',.9),0)
    for k in range(6): B.cyl((x0+15+k*.4,-7.85,1.2),.1,.25,M(r.choice(['#F2C12E','#E2562E','#2E86C1','#F4F1EA']),.5),seg=8)
    for k in range(5): B.box((x0+24+k*.7,-8.8,.25+.0),(.3,.3,.25),M(r.choice(['#7A5A3A','#5A6B7A','#8E44AD']),.7,kind='wood'),.02)
    B.box((x0+30,-9.6,.8),(.4,.3,.8),M('#C9CDD6',.3,metal=.6),.03)
    # far side: other track, wall, buildings
    for i in range(30):
        xx=r.uniform(x0-20,x1+20); h=r.uniform(6,16); B.box((xx,r.uniform(14,40),h/2),(r.uniform(3,7),r.uniform(3,6),h/2),M(r.choice(['#D8CDB8','#C9B9A0','#B8C4B0','#9C4A32','#E8D2A8']),.95,kind='wall'),0)
    B.box(((x0+x1)/2,9.0,1.0),((x1-x0)/2+30,.2,1.0),M('#B8A890',.9,kind='concrete'),0)
    for k in range(10): tree(r.uniform(x0,x1),r.uniform(11,13),0,r.uniform(1.0,1.5),k+seed,palm=r.random()<.3)
def lahore_junction():
    """red-brick fortress-style station building facade at y=8 facing -y, forecourt road y<8"""
    RB=M('#A0402A',.85,kind='concrete',sc=.35); WT=M('#E8DCC0',.6); DK=M('#2A1E18',.9)
    B.box((0,0,-.05),(60,30,.05),M('#5A5A5C',.9,kind='concrete',sc=.6),0)
    B.box((0,-2.0,.08),(40,1.2,.08),M('#B8B0A0',.85,kind='concrete'),0)
    B.box((0,12,6),(34,4,6),RB,.04)
    for s in (-1,1):
        for xx in (s*10,s*22):
            B.cyl((xx,8.3,8),2.0,16,RB,seg=8); B.cyl((xx,8.3,16.3),2.3,.6,WT,seg=8)
            for k in range(8): a=2*pi*k/8; B.box((xx+2.2*math.cos(a),8.3+2.2*math.sin(a),17.0),(.35,.35,.45),RB,.02)
            for z in (5,9,13): B.box((xx,6.25,z),(.3,.05,.7),DK,0)
    for k in range(-30,32,2): B.box((k,7.95,12.3),(.4,.4,.45),RB,.02)
    B.box((0,7.9,12.0),(34,.15,.15),WT,0)
    for k in range(-7,8):
        xx=k*2.6
        if abs(xx)<8: continue
        B.box((xx,7.95,3.0),(.9,.05,2.0),DK,0); B.cyl((xx,7.95,5.0),.9,.06,DK,rot=(R(90),0,0),seg=16); B.box((xx,7.9,6.3),(1.1,.05,.08),WT,0)
    B.box((0,7.4,4.5),(6,.6,4.5),RB,.04); B.box((0,6.75,3.0),(3.2,.05,3.0),DK,0); B.cyl((0,6.75,6.0),3.2,.06,DK,rot=(R(90),0,0),seg=24)
    B.box((0,6.7,7.6),(4.5,.08,.6),WT,.02); text('LAHORE JUNCTION',(0,6.6,7.6),(0,-1,0),.55,M('#7A1E2E',.4),ex=.01)
    B.cyl((0,6.7,9.6),.8,.08,M('#F4F1EA',.4),rot=(R(90),0,0),seg=24); B.cyl((0,6.6,9.6),.7,.04,M('#1E1E22',.4),rot=(R(90),0,0),seg=24)
    for k in range(8): tree(-28+k*8,-4.2,0,1.2,k+40,palm=k%2==0)
    for i in range(20):
        xx=random.uniform(-60,60); h=random.uniform(6,14); B.box((xx,random.uniform(-40,-14),h/2),(4,4,h/2),M(random.choice(['#D8CDB8','#9C4A32','#E8D2A8','#C9B9A0']),.95,kind='wall'),0)
def compartment(night=False):
    """coach interior: long berths along both walls facing the aisle (y=0). walls at y=+-1.5"""
    WL=M('#D8DCC8',.85,kind='wall'); FL=M('#5A5F66',.8,kind='concrete',sc=.4); SEAT=M('#2E7D5A',.7,kind='fabric'); MT=M('#C9CDD6',.3,metal=.7)
    B.box((0,0,-.02),(12,1.5,.02),FL,0); B.box((0,1.5,1.4),(12,.03,1.4),WL,0); B.box((0,-1.5,1.4),(12,.03,1.4),WL,0); B.box((0,0,2.75),(12,1.5,.05),M('#E8E4D8',.9),0)
    for s_ in (-1,1):
        B.box((0,s_*1.12,.42),(11,.3,.06),SEAT,.03); B.box((0,s_*1.38,.85),(11,.08,.38),SEAT,.03); B.box((0,s_*1.1,.2),(11,.25,.2),M('#3A3E44',.6),.01)
        B.box((0,s_*1.25,2.15),(11,.25,.03),MT,0)
        for k in range(-5,6):
            xx=k*1.8
            B.box((xx,s_*1.48,1.55),(.6,.02,.38),M('#9FC7E8' if not night else '#10182A',.1,emit=.7 if not night else .2),0)
            for b in range(5): B.box((xx-.48+b*.24,s_*1.46,1.55),(.012,.012,.39),MT,0)
            B.box((xx+.9,s_*1.3,.85),(.04,.2,.4),MT,0)
    for k in range(-5,6): B.box((k*1.8,0,2.68),(.6,.08,.04),M('#F4FAFF',.3,emit=6 if not night else 1.5),0)
    return []
def clutter(seed=3,n=30):
    r=random.Random(seed)
    for i in range(n):
        x=r.uniform(-4,4); kind=r.random(); s_=r.choice((-1,1))
        if kind<.3: B.box((x,s_*1.12,.5),(.18,.12,.04),M(r.choice(['#E2562E','#F2C12E','#2E86C1','#C0392B']),.6),.01)
        elif kind<.5: B.box((x,s_*r.uniform(.4,.7),.06),(.12,.25,.05),M(r.choice(['#22242B','#F4F1EA','#8E5B3A']),.6),.02)
        elif kind<.75: B.box((x,s_*1.25,2.36),(.35,.22,.18),M(r.choice(['#2E86C1','#8E44AD','#27AE60','#C0392B']),.7,kind='fabric'),.05)
        else: B.cyl((x,s_*1.12,.56),.04,.18,M(r.choice(['#2E86C1','#F4F1EA']),.3,alpha=.8),seg=8)
def outside_view(night=False):
    """scrolling landscape strip outside window (y>1.6) — returns empties to move"""
    objs=[]; r=random.Random(5)
    for i in range(40):
        e=empty((0,0,0)); x0=r.uniform(-30,30); d=r.uniform(4,18); kind=r.random()
        if kind<.55: ocyl((0,0,1.6),.15,3.2,M('#6B4A30',.8),e,rot=(0,0,0),seg=6); oico((0,0,3.6),1.2,M('#3E8E4A' if not night else '#0E1A14',.8),e,sub=1)
        elif kind<.8: obox((0,0,1.0),(r.uniform(1,3),1,r.uniform(.8,2)),M(r.choice(['#C9B9A0','#E2D6C0','#9C4A32']) if not night else '#141820',.9),.02,e)
        else: obox((0,0,4),(.08,.08,4),M('#5A5F66',.5),0,e)
        objs.append((e,x0,d))
    B.box((0,30,-1.5),(200,28,.05),M('#8AA05A' if not night else '#0A0E14',.95,kind='concrete',sc=.2),0)
    return objs
def foodstreet(night=True):
    """Lahore food street at night: lane along x with havelis (y=+-6.5), dining tables in middle, string lights"""
    GROUND=M('#8A6A52',.85,kind='concrete',sc=.32); B.box((0,0,-.05),(40,30,.05),GROUND,0)
    r=random.Random(21); k=0
    for side in (-1,1):
        x=-26
        while x<26:
            w=r.uniform(4.5,7.0); h=r.uniform(9,14); haveli(x+w/2,side*6.5,side,w,h,500+k,shop=True,goods=False); x+=w+.05; k+=1
    LT=[M(c,.3,emit=12) for c in ('#FFD27A','#FF9C5A','#FFE6B0','#7FD3FF','#FF7AB0')]
    for j in range(16):
        x0=-24+j*3.2; pts=[(x0,-6.0,6.0),(x0+1.5,0,4.6),(x0+3.0,6.0,6.0)]
        for a_,b_ in zip(pts,pts[1:]):
            seg(a_,b_,.01,M('#1A1A1E',.6),sides=4)
            for q in range(6):
                f=q/6; B.ico((L(a_[0],b_[0],f),L(a_[1],b_[1],f),L(a_[2],b_[2],f)-.05),.06,LT[(j+q)%5],sub=1)
    for i in range(10):
        x=-14+i*3.2
        for yy in (-2.6,2.6):
            B.box((x,yy,.72),(.7,.45,.03),M('#F4F1EA',.6,kind='fabric'),.01); B.cyl((x,yy,.36),.05,.72,M('#5A5F66',.5),seg=6)
            for dx in (-.5,.5): B.box((x+dx,yy+(.7 if yy>0 else -.7),.4),(.2,.2,.03),M('#C0392B',.5),.01); B.box((x+dx,yy+(.88 if yy>0 else -.88),.62),(.2,.02,.22),M('#C0392B',.5),.01)
            for q in range(3): B.cyl((x-.35+q*.35,yy,.79),.14,.08,M(r.choice(['#C9A24A','#8A5A2A','#C9CDD6']),.3,metal=.6),seg=14); B.cyl((x-.35+q*.35,yy,.84),.12,.03,M(r.choice(['#C0392B','#E07A2E','#E8C25A','#7A3A1E']),.6),seg=14)
    for x in (-18,-6,8,20):
        B.box((x,-5.2,.9),(1.2,.6,.9),M('#3A3A36',.6,metal=.3),.03); B.cyl((x,-5.2,1.9),.55,.15,M('#2B2C33',.4,metal=.6),seg=18,r2=.3)
        B.ico((x,-5.2,2.05),.3,M('#C0392B',.5),sc=(1,1,.3),sub=1)
