# Karachi sets: concrete apartment street, water tanker, flat interior, kiryana shop, rooftop, aerial city, rain/flood
CONC=['#D8CDB8','#C9B9A0','#B8C4B0','#D6B8A8','#C2C6CC','#E2D6C0','#B9A890','#CFC2D0','#A9B7BF']
SIGN=['#C0392B','#1F6FB8','#2E8B57','#E07A2E','#8E44AD','#16A0A0','#D4A017']
CLOTH=['#C0392B','#2E86C1','#F4F1EA','#27AE60','#E67E22','#8E44AD','#F1C40F','#E84393','#34495E']
def stains(x,fy,side,w,h,r,col):
    for k in range(int(w*1.2)):
        xx=x-w/2+r.uniform(.2,w-.2); hh=r.uniform(1.5,h*.6); B.box((xx,fy-side*.012,h-hh/2-.3),(r.uniform(.05,.25),.004,hh/2),M(shade(col,r.uniform(.72,.86)),.95),0)
def apt(x,yface,side,w,h,seed,shop=True):
    r=random.Random(seed); col=r.choice(CONC); d=8.0; yc=yface+side*d/2; fy=yface-side*.01
    W_=M(col,.92,kind='wall'); B.box((x,yc,h/2),(w/2,d/2,h/2),W_,.02); stains(x,fy,side,w,h,r,col)
    RL=M('#5A5F66',.5,metal=.5); DK=M('#1C1E22',.9); GL=M('#4A5866',.25,spec=.6)
    fl=3.0; nf=int((h-3.2)/fl)
    for f in range(nf):
        z=3.3+f*fl; n=max(1,int(w/3.2))
        for i in range(n):
            xx=x-w/2+w*(i+.5)/n
            if r.random()<.55:   # balcony
                B.box((xx,fy-side*.7,z),(1.2,.7,.08),M(shade(col,.85),.9),.02)
                B.box((xx,fy-side*1.38,z+.5),(1.2,.03,.45),RL if r.random()<.6 else M(shade(col,.9),.9),.01)
                B.box((xx,fy-side*.02,z+1.2),(.8,.02,1.1),DK,0)
                if r.random()<.6:   # laundry line
                    for c in range(r.randint(2,5)): B.box((xx-.9+c*.42,fy-side*1.0,z+1.6),(.17,.01,.3),M(r.choice(CLOTH),.85,kind='fabric'),.005)
                    B.box((xx,fy-side*1.0,z+1.92),(1.15,.006,.006),DK,0)
                if r.random()<.4: B.cyl((xx+.8,fy-side*.5,z+.45),.22,.7,M(r.choice(['#2E86C1','#C0392B','#F4F1EA']),.5),seg=10)   # water drum
            else:
                B.box((xx,fy,z+1.3),(.6,.02,.6),GL if r.random()<.6 else DK,0)
                for k in range(5): B.box((xx-.5+k*.25,fy-side*.05,z+1.3),(.015,.02,.62),RL,0)
                B.box((xx,fy-side*.05,z+.66),(.7,.06,.05),M(shade(col,.8),.9),0)
                if r.random()<.45: B.box((xx+.95,fy-side*.25,z+1.1),(.4,.22,.3),M('#D8DCE0',.4,metal=.3),.03)
    # roof: tanks, dishes, rods
    for k in range(r.randint(1,3)): B.cyl((x+r.uniform(-w/3,w/3),yc+side*r.uniform(0,3),h+.7),.6,1.3,M('#1E1E22',.6),seg=12)
    if r.random()<.6: dsh=B.cyl((x+r.uniform(-w/3,w/3),yc,h+.9),.45,.06,M('#E8E8E8',.4),rot=(R(60),0,R(r.uniform(0,360))),seg=14)
    for k in range(3): B.cyl((x-w/2+.4+k*.9,yface+side*.3,h+.6),.03,1.2,M('#6A5A4A',.6,metal=.5),seg=4)
    if shop:
        sc_=r.choice(SIGN); open_=r.random()<.6; sw=w/2-.3
        if open_:
            B.box((x,fy-side*.02,1.3),(sw,.02,1.2),M('#2A2622',.9),0)
            for k in range(int(w/.7)):
                B.box((x-sw+.3+k*.7,fy-side*.25,r.uniform(.6,1.9)),(.25,.18,.2),M(r.choice(CLOTH+SIGN),.6),.02)
            B.box((x,fy-side*.9,.42),(sw-.2,.5,.42),M('#7A5A3A',.7,kind='wood'),.02)
        else:
            B.box((x,fy-side*.03,1.3),(sw,.03,1.2),M('#8A9098',.4,metal=.6,kind='wood',sc=8),0)
            for k in range(12): B.box((x,fy-side*.05,.2+k*.2),(sw,.01,.012),M('#6A7078',.4,metal=.6),0)
        B.box((x,fy-side*.12,2.85),(sw+.1,.1,.42),M(sc_,.5,emit=.2),.02)
        for k in range(r.randint(2,4)): B.box((x-sw+.8+k*1.3,fy-side*.18,2.85),(.42,.01,.2),M(r.choice(['#F4F1EA','#F1C40F','#1E1E22']),.5),0)
def footpath(x0,x1,side,seed):
    r=random.Random(seed); FP=M('#9C968C',.9,kind='concrete',sc=.5); CURB=M('#C8C2B4',.85)
    yc=side*5.65; B.box(((x0+x1)/2,yc,.09),((x1-x0)/2,1.1,.09),FP,.01); B.box(((x0+x1)/2,side*4.52,.12),((x1-x0)/2,.07,.12),CURB,.01)
    B.box(((x0+x1)/2,side*4.75,.0),((x1-x0)/2,.16,.02),M('#2A2A20',.3,spec=.5),0)   # open drain channel
    for k in range(int((x1-x0)/2.2)):   # broken tiles
        if r.random()<.35: B.box((x0+k*2.2+r.uniform(0,1.5),yc+r.uniform(-.8,.8),.185),(r.uniform(.2,.5),r.uniform(.2,.4),.012),M('#7E786E',.95),0,rot=(0,0,r.uniform(0,1)))
    for k in range(int((x1-x0)/9)):   # electric poles with cable bundles
        px=x0+4+k*9+r.uniform(-1,1); B.cyl((px,side*4.95,4.6),.13,9.2,M('#8A8A84',.7,kind='concrete'),seg=8)
        B.box((px,side*4.95,8.6),(.8,.06,.06),M('#5A5A55',.6),0)
        for j in range(3): B.cyl((px+.25*j-.25,side*4.95-.15,7.2-.4*j),.18,.35,M('#3A3A36',.6),seg=8)
    if r.random()<.8:
        for k in range(int((x1-x0)/14)):
            gx=x0+6+k*14+r.uniform(-2,2)
            for j in range(9): B.ico((gx+r.uniform(-.7,.7),side*5.9+r.uniform(-.4,.4),.25),r.uniform(.15,.3),M(r.choice(['#3A3A36','#5A6B3A','#E8E4D8','#2E86C1','#6A4A3A']),.9),sub=1)
def road(x0,x1,seed=3,potholes=True):
    r=random.Random(seed); ASP=M('#4A4A4C',.92,kind='concrete',sc=.6)
    B.box(((x0+x1)/2,0,-.05),((x1-x0)/2+30,40,.05),M('#8A8070',.95,kind='concrete',sc=.4),0)
    B.box(((x0+x1)/2,0,.0),((x1-x0)/2,4.5,.02),ASP,0)
    for k in range(int((x1-x0)/4)):
        if r.random()<.6: B.box((x0+k*4+1,0,.025),(.9,.07,.004),M('#D8D4C8',.8),0)
    out=[]
    if potholes:
        for k in range(int((x1-x0)/5)):
            px=x0+2+k*5+r.uniform(-1.5,1.5); py=r.uniform(-3.8,3.8); s_=r.uniform(.35,.8)
            B.cyl((px,py,.024),s_,.008,M('#2E2C28',.95),seg=16); B.cyl((px,py,.03),s_*.7,.004,M('#5C6066',.05,spec=1.0),seg=14); out.append((px,py,s_))
    return out
def street(x0=-30,x1=30,seed=3,shops=.7):
    ph=road(x0,x1,seed)
    r=random.Random(seed+7); k=0
    for side in (-1,1):
        footpath(x0,x1,side,seed+side)
        x=x0
        while x<x1:
            w=r.uniform(7,11); h=r.uniform(14,24); apt(x+w/2,side*6.8,side,w,h,seed*100+k,shop=r.random()<shops); x+=w+.08; k+=1
    wires(x0,x1,-5.0,5.0,7.0,int((x1-x0)/2),seed+3)
    # big tangled cable bundles along poles
    for side in (-1,1):
        for k in range(3):
            pts=[(x0+i*3,side*4.85+.1*math.sin(i+k),7.2-.25*k-.35*math.sin(i*.7)**2) for i in range(int((x1-x0)/3)+1)]
            for a,b in zip(pts,pts[1:]): seg(a,b,.03,M('#1A1A1E',.6),sides=4)
    # far skyline blocks for depth/haze
    for i in range(60):
        xx=r.uniform(x0-40,x1+40); yy=r.choice((-1,1))*r.uniform(18,60); h=r.uniform(15,40)
        B.box((xx,yy,h/2),(r.uniform(4,9),r.uniform(4,9),h/2),M(r.choice(CONC),.95,kind='wall'),0)
    for i in range(4): B.box((r.uniform(x0,x1),r.choice((-1,1))*35,22),(5,3,22),M('#B8BCC4',.6),0)
    return ph
def kbus(x,y,rz=0,seed=1):
    r=empty((x,y,0),rot=(0,0,R(rz))); rr=random.Random(seed)
    BODY=M('#F4F1EA',.35,metal=.2); TI=M('#111216',.8); RIM=M('#C9CDD6',.25,metal=.9); GL=M('#22303E',.08,spec=1.0)
    obox((0,0,1.75),(5.2,1.25,1.35),BODY,.12,r); obox((0,0,1.05),(5.22,1.27,.18),M('#C0392B',.4),.02,r); obox((0,0,2.15),(5.22,1.27,.12),M('#1F6FB8',.4),.02,r)
    for k in range(12): obox((-4.8+k*.85,0,1.42),(.32,1.28,.22),M(rr.choice(CLOTH+SIGN),.4,emit=.1),.02,r)
    obox((0,0,2.45),(4.6,1.27,.4),GL,.05,r)
    for k in range(10): obox((-4.4+k*.95,0,2.45),(.04,1.29,.42),M('#C9CDD6',.3,metal=.9),0,r)
    obox((5.21,0,2.3),(.03,1.0,.55),GL,.02,r); obox((5.25,0,3.25),(.08,1.3,.18),M('#F1C40F',.4),.03,r)
    obox((0,0,3.15),(5.0,1.1,.06),M('#C9CDD6',.3,metal=.8),.02,r)
    for k in range(10): ocyl((-4.5+k*1.0,1.05,3.3),.08,.25,M('#C9CDD6',.3,metal=.9),r,seg=8)
    for sx in (-3.4,3.4):
        for sy in (-1,1): ocyl((sx,sy*1.15,.52),.52,.3,TI,r,rot=(R(90),0,0),seg=18); ocyl((sx,sy*1.31,.52),.3,.02,RIM,r,rot=(R(90),0,0),seg=12)
    for sy in (-.8,.8): obox((5.22,sy,1.25),(.03,.22,.12),M('#FFF2C8',.3,emit=4),.01,r)
    return r
def tanker(x,y,rz=0):
    r=empty((x,y,0),rot=(0,0,R(rz))); TK=M('#2E6FB8',.35,metal=.3); CAB=M('#F4F1EA',.4); TI=M('#111216',.8)
    obox((3.2,0,1.6),(1.1,1.15,1.1),CAB,.15,r); obox((3.95,0,1.95),(.35,1.1,.5),M('#22303E',.08,spec=1.0),.05,r); obox((3.2,0,.65),(1.15,1.2,.25),M('#C0392B',.5),.04,r)
    ocyl((-1.0,0,1.85),1.2,5.4,TK,r,rot=(0,R(90),0),seg=24); obox((-1.0,0,.65),(2.9,.9,.12),M('#2B2C33',.5),.02,r)
    for k in range(3): ocyl((-3.0+k*2.0,0,1.85),1.24,.12,M('#1F4F8A',.4,metal=.4),r,rot=(0,R(90),0),seg=24)
    ocyl((-1.0,0,3.1),.35,.25,M('#1F4F8A',.4,metal=.4),r,seg=12)
    t_=text('PAANI',(-1.0,-1.22,1.9),(0,-1,0),.5,M('#F4F1EA',.4),ex=.01); t_.parent=r
    for sx in (-2.6,-1.4,3.2):
        for sy in (-1,1): ocyl((sx,sy*1.05,.48),.48,.32,TI,r,rot=(R(90),0,0),seg=16)
    return r
def bucket(x,y,col,s=1.0,kind=0):
    if kind==0: B.cyl((x,y,.2*s),.2*s,.4*s,M(col,.4),seg=14,r2=.15*s); B.cyl((x,y,.41*s),.21*s,.02,M(shade(col,.8),.4),seg=14)
    else: B.box((x,y,.32*s),(.17*s,.13*s,.32*s),M(col,.35,alpha=.85),.04); B.cyl((x,y,.68*s),.05*s,.08*s,M('#2E86C1',.4),seg=8)
def flat():
    """Daniyal's flat: bedroom zone x<0, living x>1; window wall y=2.8 (faces -y)"""
    FL=M('#B9AE9C',.6,kind='tile',h2='#A89C88',sc=1.6); WL=M('#E8D2B0',.9,kind='wall'); WL2=M('#B8D4C8',.9,kind='wall')
    B.box((0,0,-.05),(7,3.6,.05),FL,0); B.box((-1.5,2.85,1.6),(5.5,.05,1.6),WL,0); B.box((-6.9,0,1.6),(.05,3.6,1.6),WL2,0); B.box((0,0,3.25),(7,3.6,.05),M('#F2EEE6',.9),0)
    B.box((4.2,2.85,1.6),(.3,.05,1.6),WL,0); B.box((1.0,1.9,1.6),(.06,.95,1.6),WL2,.01)
    # barred window showing street
    B.box((-2.6,2.86,1.85),(1.0,.02,.75),M('#E8EEF2',.3,emit=1.2),0)
    for k in range(7): B.box((-3.45+k*.28,2.8,1.85),(.018,.02,.76),M('#3A3E44',.4,metal=.6),0)
    for z in (1.4,2.3): B.box((-2.6,2.8,z),(1.0,.02,.018),M('#3A3E44',.4,metal=.6),0)
    B.box((-2.6,2.82,2.65),(1.05,.04,.06),M('#C9C2B0',.8),0)
    # bed, side table, cupboard, calendar, plastic chairs, cooler
    B.box((-5.2,1.7,.25),(1.0,1.0,.25),M('#6B4A30',.6,kind='wood'),.03); B.box((-5.2,1.7,.55),(.95,.95,.08),M('#E8E0D0',.9,kind='fabric'),.05)
    B.box((-5.2,1.9,.7),(.85,.7,.08),M('#C0392B',.9,kind='fabric'),.06); B.box((-5.2,2.55,.68),(.5,.15,.1),M('#F4F1EA',.9,kind='fabric'),.05)
    B.box((-3.8,2.4,.3),(.3,.3,.3),M('#8A6A4A',.6,kind='wood'),.02)
    B.box((-6.6,-.6,1.1),(.28,.9,1.1),M('#7A8A96',.4,metal=.4),.02); B.box((-6.31,-.6,1.1),(.005,.02,1.0),M('#2B2C33',.4),0)
    B.box((-1.2,2.82,1.9),(.32,.01,.42),M('#F4F1EA',.6),0); B.box((-1.2,2.81,2.2),(.32,.005,.1),M('#C0392B',.6),0)
    for x,c in ((2.4,'#2E86C1'),(3.6,'#C0392B'),(4.8,'#2E86C1')):
        B.box((x,1.2,.42),(.25,.25,.03),M(c,.35),.02); B.box((x,1.45,.75),(.25,.03,.33),M(c,.35),.02)
        for sx in (-.2,.2):
            for sy in (-.2,.2): B.cyl((x+sx,1.2+sy,.2),.025,.4,M(c,.35),seg=6)
    B.box((3.6,.2,.38),(.6,.4,.03),M('#8A6A4A',.6,kind='wood'),.02)
    for sx in (-.5,.5):
        for sy in (-.3,.3): B.cyl((3.6+sx,.2+sy,.18),.03,.36,M('#6B4A30',.6),seg=6)
    B.cyl((3.6,.2,.48),.06,.18,M('#F4F1EA',.4,alpha=.6),seg=10)
    B.box((6.0,2.3,.7),(.45,.35,.7),M('#5A6B7A',.5,metal=.3),.04)
    for k in range(5): B.box((6.0,1.94,.5+k*.15),(.35,.01,.03),M('#2B2C33',.5),0)
    # living-side window
    B.box((3.0,2.86,1.9),(.9,.02,.7),M('#F2E6CC',.3,emit=1.0),0)
    for k in range(6): B.box((2.2+k*.32,2.8,1.9),(.018,.02,.7),M('#3A3E44',.4,metal=.6),0)
    B.done('flat')
    fans=[]
    for fx_ in (-3.0,3.6):
        f=empty((fx_,.8,2.95)); obox((0,0,.15),(.05,.05,.15),M('#F2EEE6',.5),.01,f); ocyl((0,0,0),.16,.12,M('#F2EEE6',.5),f,seg=16)
        for k in range(3):
            a=2*pi*k/3; obox((math.cos(a)*.55,math.sin(a)*.55,-.02),(.45,.08,.01),M('#E8E2D6',.5),.01,f,rot=(0,0,a))
        fans.append(f)
    return fans
def shopset():
    """Uncle Rashid's kiryana: counter at y=0.6, shelves on back wall y=2.6, door to street at -y"""
    FL=M('#8A8478',.85,kind='concrete',sc=.6); WL=M('#C8D8C0',.9,kind='wall')
    B.box((0,0,-.05),(4,3.2,.05),FL,0); B.box((0,2.75,1.6),(4,.05,1.6),WL,0); B.box((-3.9,0,1.6),(.05,3.2,1.6),WL,0); B.box((3.9,0,1.6),(.05,3.2,1.6),WL,0); B.box((0,0,3.2),(4,3.2,.05),M('#E8E4D8',.9),0)
    r=random.Random(4)
    for k in range(4):
        z=.5+k*.65; B.box((0,2.45,z),(3.4,.3,.03),M('#7A5A3A',.7,kind='wood'),.01)
        x=-3.2
        while x<3.2:
            w=r.uniform(.12,.3); h=r.uniform(.2,.45); c=r.choice(SIGN+CLOTH)
            if r.random()<.3: B.cyl((x+w/2,2.45,z+h/2+.03),w/2,h,M(c,.4),seg=10)
            else: B.box((x+w/2,2.45,z+h/2+.03),(w/2-.01,.12,h/2),M(c,.45),.01)
            x+=w+.02
    B.box((0,.6,.55),(2.6,.35,.55),M('#9A7A54',.7,kind='wood'),.02); B.box((0,.6,1.12),(2.65,.4,.03),M('#C9CDD6',.25,metal=.4),.01)
    for k in range(6): B.cyl((-2.2+k*.45,.62,1.3),.15,.3,M('#F4F1EA',.15,alpha=.55),seg=12); B.cyl((-2.2+k*.45,.62,1.48),.16,.05,M(r.choice(SIGN),.4),seg=12)
    B.box((3.2,1.6,1.0),(.45,.45,1.0),M('#C0392B',.45),.04); B.box((3.2,1.14,1.05),(.38,.01,.85),M('#9FC7D8',.08,spec=1.0,alpha=.5),0)
    for k in range(4):
        for j in range(5): B.cyl((3.0+j*.1,1.4,.4+k*.42),.04,.26,M(r.choice(['#2E86C1','#27AE60','#E67E22','#8E44AD']),.3),seg=8)
    text('COLD DRINKS',(3.2,1.13,1.95),(0,-1,0),.11,M('#F4F1EA',.4),ex=.003)
    for k in range(3): B.cyl((-3.3+k*.55,-1.8,.4),.25,.8,M(r.choice(['#E8DCC0','#D8C8A0']),.9,kind='fabric'),seg=10)
    B.box((0,2.7,2.85),(1.0,.04,.22),M('#1F6FB8',.5),.02); text('RASHID GENERAL STORE',(0,2.66,2.85),(0,-1,0),.11,M('#F4F1EA',.4),ex=.003)
    B.box((-1.6,.6,1.25),(.25,.2,.1),M('#5A5F66',.4,metal=.4),.02)
    B.done('shop')
    tube=obox((0,1.6,3.1),(.7,.04,.03),M('#F4FAFF',.3,emit=6),.01)
    return tube
def city(seed=3,night=False,R_=180,sea=True,ss=1):
    r=random.Random(seed); win=M('#FFD9A0',.4,emit=9.0); win2=M('#BFE0FF',.4,emit=6.0)
    B.box((0,0,-.06),(R_*1.6,R_*1.6,.05),M('#6E665A',.95,kind='wall'),0)
    for i in range(520 if night else 900):
        x=r.uniform(-R_,R_); y=ss*r.uniform(-R_,R_*.75)
        if abs(x)<8 and abs(y)<8: continue
        w=r.uniform(5,12); d=r.uniform(5,12); h=r.uniform(8,30)*(1.8 if r.random()<.06 else 1); col=r.choice(CONC)
        B.box((x,y,h/2),(w/2,d/2,h/2),M(col if not night else shade(col,.35),.95,kind='wall'),0)
        if r.random()<.5: B.cyl((x+r.uniform(-w/3,w/3),y+r.uniform(-d/3,d/3),h+.6),.6,1.2,M('#1E1E22',.6),seg=8)
        if night:
            lit=r.random()
            if lit>.12:
                for k in range(int(4+lit*10)):
                    fz=2+int(r.uniform(0,(h-2)/2.6))*2.6+1; m_=win if r.random()<.75 else win2
                    B.box((x+r.uniform(-w/2+.6,w/2-.6),y+ss*(d/2+.02),fz),(.45,.02,.4),m_,0); sx=r.choice((-1,1)); B.box((x+sx*(w/2+.02),y+r.uniform(-d/2+.6,d/2-.6),fz),(.02,.45,.4),m_,0)
    # main roads with traffic lights at night
    for k in range(-2,3):
        B.box((0,k*55,.02),(R_,4,.02),M('#3A3A3C',.9),0)
        if night:
            for j in range(80): B.box((r.uniform(-R_,R_),k*55+r.choice((-2,2)),.4),(.3,.12,.08),M(r.choice(['#FFE6B0','#FF3B2E']),.3,emit=8),0)
    if sea:
        B.box((0,ss*(R_*.75+60),-.02),(R_*2,60,.02),M('#2E5A78' if not night else '#1C3050',.12,spec=1.0),0)
        B.box((0,ss*(R_*.75+2),.05),(R_*2,3,.05),M('#D8C8A0' if not night else '#3A3830',.9),0)
        for k in range(5): B.box((r.uniform(-R_,R_),ss*(R_*.75+8),8),(.4,.4,8),M('#C0392B',.5),0); B.box((r.uniform(-R_,R_),ss*(R_*.75+8),16),(6,.4,.3),M('#C0392B',.5),0)
        if night:
            for j in range(160): B.box((r.uniform(-R_*1.5,R_*1.5),ss*(R_*.75+4),r.uniform(.5,6)),(.25,.25,.25),M('#FFD9A0',.3,emit=14),0)
def rain(center,spread,n,seed,speed=14.0,zmax=9):
    r=random.Random(seed); out=[]; mat=M('#C8D8E8',.2,alpha=.35,emit=.4)
    for i in range(n):
        o=obox((0,0,0),(.006,.006,.22),mat,0); x=center[0]+r.uniform(-spread,spread); y=center[1]+r.uniform(-spread*.6,spread*.6); ph=r.uniform(0,zmax)
        def fn(o,t,x=x,y=y,ph=ph): o.location=(x+.15*((t*speed+ph)%zmax)/zmax,y,zmax-((t*speed+ph)%zmax))
        fx.add(o,fn); out.append(o)
    return out
def floodwater(x0,x1,y0,y1):
    return obox(((x0+x1)/2,(y0+y1)/2,0),((x1-x0)/2,(y1-y0)/2,.005),M('#6A6450',.08,spec=1.0),0)
def roof():
    """rooftop at z=0, parapet at y=-3.5 looking -y over the city"""
    FL=M('#8A867C',.9,kind='concrete',sc=.5); PW=M('#B8B0A0',.9,kind='wall')
    B.box((0,0,-.1),(6,5,.1),FL,0)
    for s in (-1,1): B.box((s*6,0,.5),(.12,5,.5),PW,.02)
    B.box((0,-5,.5),(6,.12,.5),PW,.02); B.box((0,5,.5),(6,.12,.5),PW,.02)
    for x in (-3.5,3.8): B.cyl((x,3.2,.75),.65,1.5,M('#1E1E22',.6),seg=14); B.cyl((x,3.2,1.55),.4,.1,M('#2B2C33',.6),seg=12)
    B.cyl((4.5,-1,.9),.5,.06,M('#D8D8D4',.4),rot=(R(55),0,R(160)),seg=14); B.cyl((4.5,-.8,.45),.04,.9,M('#5A5F66',.4,metal=.6),seg=6)
    B.box((0,2.0,1.7),(4,.006,.006),M('#2B2C33',.6),0)
    for k in range(6): B.box((-3+k*1.1,2.0,1.45),(.22,.01,.25),M(CLOTH[k],.85,kind='fabric'),.005)
    for x in (-1.2,1.2): B.box((x,-2.0,.45),(.3,.3,.45),M('#2E86C1' if x<0 else '#C0392B',.35),.03)

def space():
    r=random.Random(1); st=M('#FFFFFF',.3,emit=8)
    for i in range(700):
        a=r.uniform(0,2*pi); e=r.uniform(-1.2,1.2); d=900
        B.box((d*math.cos(a)*math.cos(e),d*math.sin(a)*math.cos(e),d*math.sin(e)),(.9,.9,.9),st,0)
    B.ico((0,0,0),60,M('#1E5AA8',.25,spec=.7),sub=5)
    lands=M('#5E8A3A',.8); des=M('#C2A26A',.85)
    for i in range(160):
        a=r.uniform(0,2*pi); e=r.uniform(-1.1,1.1); n=Vector((math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)))
        B.ico(tuple(n*59.2),r.uniform(4,11),des if r.random()<.4 else lands,sc=(1,1,.25),rot=tuple(n.to_track_quat('Z','Y').to_euler()),sub=2)
    # Pakistan-ish landmass facing camera direction (-y), Karachi dot
    n=Vector((0,-1,.35)).normalized()
    for i in range(14): B.ico(tuple((n+Vector((r.uniform(-.12,.12),0,r.uniform(-.1,.1)))).normalized()*59.4),r.uniform(5,8),des if i%2 else lands,sc=(1,1,.22),rot=tuple(n.to_track_quat('Z','Y').to_euler()),sub=2)
    B.ico(tuple(Vector((0,-1,.28)).normalized()*60.2),.9,M('#FFD27A',.3,emit=20),sub=2)
    B.ico((0,0,0),62.5,M('#7FB8FF',.0,alpha=.12,emit=.3),sub=4)
