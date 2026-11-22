# Sets for "Sea View": Clifton beach at sunset (sand, animated surf, promenade wall with lamp posts, parked cars,
# bhutta/chaat/chai stalls, camel + horse rides, balloon seller, kite, beach mats), car interior strip for the parking gag.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
SAND=M('#D8B98A',.95,kind='asphalt',h2='#C8A878',sc=2.5); WET=M('#9A8668',.35,spec=.9)
def surf_set():
    """sea toward +y; beach y in [-6, 9]; wet strip ~9..11; water beyond. Promenade at y=-9 (road behind at y<-11)."""
    B.box((0,0,-.05),(60,30,.05),SAND,0)
    B.box((0,10.2,-.03),(60,1.4,.03),WET,0)
    sea=[]
    B.box((0,40,-.08),(80,28,.05),M('#2E7A9A',.08,spec=1.0),0)
    for k in range(5):
        e=empty((0,12+k*1.6,0)); obox((0,0,0),(60,.25,.04),M('#F4FAFF',.3,emit=.25,alpha=.9),.02,e); sea.append(e)
    # promenade wall + railings + lamps
    B.box((0,-9.2,.6),(60,.5,.6),M('#C8C0B0',.8,kind='wall'),.03)
    for x in range(-58,59,2): B.box((x,-9.2,1.45),(.05,.05,.25),M('#5A5E66',.3,metal=.7),0)
    B.box((0,-9.2,1.72),(60,.04,.04),M('#5A5E66',.3,metal=.7),0)
    lamps=[]
    for x in range(-48,49,8):
        B.cyl((x,-9.2,3.0),.08,4.8,M('#3A3D44',.3,metal=.7),seg=8); B.box((x,-8.6,5.3),(.6,.08,.06),M('#3A3D44',.3,metal=.7),0); lamps.append(B.ico((x,-8.1,5.2),.22,M('#FFE0A0',.3,emit=5),sub=1))
    B.box((0,-14,-.05),(60,4.5,.05),M('#4A4C54',.85,kind='asphalt'),0)
    for x in range(-50,51,5): B.box((x,-14,.0),(1.2,.06,.01),M('#F4F1EA',.6),0)
    # buildings / skyline behind road
    r=random.Random(3)
    for k in range(16):
        x=-56+k*7.3; h=r.uniform(8,26); B.box((x,-24,h/2),(3.2,3,h/2),M(r.choice(['#E8D8B0','#C9CED8','#D8C8A8','#F0E6CC','#A8B8C8']),.7,kind='wall'),0)
        for j in range(int(h/2.2)): B.box((x,-20.95,1.5+j*2.2),(2.6,.03,.35),M('#FFE8B0',.2,emit=r.choice([0,0,.9,1.4])),0)
    return sea,lamps
CARS=1.7  # cars are scaled to the chunky characters (2.3 tall): 7.0 long, 2.9 wide, 2.5 tall
def parked_cars(seed=4,hero=None):
    r=random.Random(seed); C=[]; cols=['#C8372D','#16171C','#2B5AA8','#9A9AA2','#D9B24A','#2F6E4A','#7A1F2E']
    for k in range(9):   # parked row along the kerb, parallel to the road
        x=-36+k*9+r.uniform(-.5,.5); c=car((x,-11.45,0),180 if k%3 else 0,r.choice(cols),seed=k); c['root'].scale=(CARS,)*3; C.append(c)
    for k in range(-4,5):  # the jam in the driving lane (hero car takes slot 0)
        if hero is not None and k in (0,-1): continue
        c=car((hero_x+k*8.6+r.uniform(-.3,.3),-15.7,0),180,r.choice(cols),seed=20+k); c['root'].scale=(CARS,)*3; C.append(c)
    return C
hero_x=2.0
def hero_car(loc=(hero_x,-15.7,0),rotz=180,col='#E8E4DA'):
    """open-window car with a full interior. local +x = front. seats: driver (0,-.9), passenger (0,.9), rear bench x=-1.9"""
    root=empty(loc,rot=(0,0,R(rotz))); bd=M(col,.3,metal=.3,spec=.6); dk=M('#1E2026',.7); st=M('#4A3A30',.85,kind='fabric'); ch=M('#C9CED8',.3,metal=.8); W=[]; HW=1.95
    obox((.1,0,.45),(3.5,HW,.1),dk,.03,root)                                   # floor
    for sy in (-1,1):
        obox((-.5,sy*(HW-.06),1.02),(2.1,.06,.48),bd,.03,root)                 # doors
        obox((-.2,sy*(HW+.01),1.25),(.14,.02,.03),ch,.01,root); obox((-1.9,sy*(HW+.01),1.25),(.14,.02,.03),ch,.01,root)
        for px in (1.55,-.55,-2.6): obox((px,sy*(HW-.08),2.18),(.07,.07,.7),bd,.02,root)   # pillars
        obox((1.75,sy*(HW+.16),1.62),(.07,.14,.1),bd,.03,root)                 # side mirrors
        obox((3.6,sy*1.35,1.05),(.04,.34,.14),M('#FFF6D8',.2,emit=2.5),.03,root); obox((-3.45,sy*1.4,1.1),(.04,.3,.12),M('#E8301A',.3,emit=2.0),.03,root)
    obox((2.6,0,1.02),(1.0,HW,.48),bd,.12,root)                                # hood
    obox((1.38,0,1.0),(.22,HW-.1,.5),dk,.04,root)                              # dashboard
    obox((1.3,.9,1.42),(.12,.4,.07),M('#2A2C34',.5),.02,root)                  # glovebox lip
    obox((1.26,0,1.3),(.1,.3,.14),M('#101216',.4),.02,root); obox((1.2,0,1.32),(.02,.22,.09),M('#3FA7E8',.3,emit=1.2),.01,root)  # screen
    obox((-2.95,0,1.02),(.5,HW,.48),bd,.12,root)                               # boot
    obox((-.55,0,2.95),(2.12,HW,.08),bd,.06,root)                              # roof
    obox((-2.62,0,2.18),(.03,HW-.15,.66),M('#1A2433',.06,spec=1.0),.01,root)   # rear glass
    obox((3.62,0,.62),(.05,HW,.12),ch,.03,root); obox((-3.47,0,.62),(.05,HW,.12),ch,.03,root); obox((3.66,0,.95),(.02,.5,.14),M('#F4F1EA',.5),.01,root)
    for sy in (-1,1):                                                          # front seats
        obox((.1,sy*.9,.68),(.45,.48,.12),st,.05,root); obox((-.38,sy*.9,1.45),(.09,.48,.75),st,.06,root); obox((-.38,sy*.9,2.36),(.08,.26,.13),st,.05,root)
    obox((.0,0,.72),(.4,.06,.14),dk,.03,root); obox((.45,0,.98),(.03,.03,.14),ch,.01,root); oico((.45,0,1.14),.06,dk,root,sub=1)   # console + gear stick
    obox((-1.8,0,.8),(.5,1.75,.15),st,.06,root); obox((-2.32,0,1.6),(.1,1.75,.7),st,.06,root)   # rear bench
    obox((1.0,-.9,1.36),(.26,.05,.05),dk,.02,root,rot=(0,R(-25),0))             # steering column
    sw=empty((.78,-.9,1.47),root,rot=(0,R(65),0))
    for k in range(24): a=k*pi/12; obox((math.cos(a)*.24,math.sin(a)*.24,0),(.036,.022,.022),dk,.012,sw,rot=(0,0,a+pi/2))
    obox((0,0,0),(.03,.22,.02),dk,.01,sw); obox((0,0,0),(.07,.07,.03),dk,.02,sw)
    for sx in (-2.3,2.3):
        for sy in (-1,1): W.append(wheel((sx,sy*(HW-.05),.55),.55,.34,root))
    return dict(root=root,wheels=W,r=.55,sw=sw)
def cw(p,loc=(hero_x,-15.7,0),rotz=180):
    a=R(rotz); return (loc[0]+p[0]*math.cos(a)-p[1]*math.sin(a),loc[1]+p[0]*math.sin(a)+p[1]*math.cos(a),loc[2]+(p[2] if len(p)>2 else 0))
def stall(x,y,kind,col,label_):
    wd=M('#7A5236',.6,kind='wood'); B.box((x,y,.45),(.9,.5,.45),wd,.03); B.box((x,y,.92),(.95,.55,.03),M('#E8E4DA',.6),.01)
    for dx in (-.85,.85): B.cyl((x+dx,y-.45,1.4),.03,2.0,M('#8A8E96',.3,metal=.6),seg=6)
    B.box((x,y+.1,2.4),(1.1,.75,.05),M(col,.85,kind='fabric',h2='#F4F1EA',sc=4),.02,rot=(R(12),0,0))
    B.box((x,y+.62,2.86),(len(label_)*.2*.46+.14,.04,.2),M('#16171C',.5),.03); stext(label_,(x,y+.67,2.86),.2,'#FFF3B0',n=(0,1,0),e=1.6)
    for dx in (-.9,.9): B.cyl((x+dx,y+.6,2.6),.025,.5,M('#8A8E96',.3,metal=.6),seg=6)
    if kind=='corn':
        B.box((x-.3,y,1.0),(.3,.25,.06),M('#2A2C34',.5),0);
        for k in range(5): B.cyl((x-.45+.08*k,y,1.08),.04,.3,M('#F2C14E',.6),rot=(0,R(90),0),seg=8)
        for k in range(4): B.ico((x-.3+.15*k,y-.05,1.1),.04,M('#FF6A1A',.3,emit=3),sub=1)
    elif kind=='chaat':
        for k in range(4): B.cyl((x-.5+.33*k,y,1.0),.14,.1,M('#C9CED8',.3,metal=.8),seg=12)
        B.box((x+.5,y,1.1),(.2,.2,.15),M('#F4F1EA',.5),.02)
    elif kind=='chai':
        B.cyl((x-.3,y,1.15),.2,.4,M('#C8703F',.3,metal=.8),seg=14,r2=.15); B.ico((x-.3,y,1.4),.08,M('#C8703F',.3,metal=.8),sub=1)
        for k in range(6): B.cyl((x+.1+.12*k,y,.98),.04,.08,M('#F4F1EA',.4),seg=8)
    elif kind=='ice':
        B.box((x,y,1.05),(.6,.35,.12),M('#9FC8E8',.3),.02)
        for k in range(4): B.cyl((x-.35+.23*k,y,1.15),.08,.06,M(['#E8709A','#F2E6A8','#8A4A2A','#7FD8A8'][k],.5),seg=10)
def camel(loc,rz=0,col='#C8A06A'):
    e=empty(loc,rot=(0,0,R(rz))); m=M(col,.85,kind='fabric',h2=shade(col,.85),sc=6); dec=M('#C8372D',.8,kind='fabric')
    obox((0,0,1.45),(.35,.85,.35),m,.12,e); oico((0,.05,1.95),.32,m,e,sc=(1,1.2,1),sub=2)
    obox((0,-.95,1.85),(.12,.12,.45),m,.05,e,rot=(R(-25),0,0)); obox((0,-1.2,2.28),(.12,.3,.12),m,.05,e)
    for dx in (-.22,.22):
        for dy in (-.6,.6): obox((dx,dy,.55),(.08,.08,.55),m,.03,e)
    obox((0,0,1.82),(.38,.5,.05),dec,.03,e);
    for k in range(6): oico((-.35+.14*k,-.5,1.75),.04,M('#F2C14E',.4),e,sub=1)
    return e
def horse(loc,rz=0,col='#F4F1EA'):
    e=empty(loc,rot=(0,0,R(rz))); m=M(col,.7); obox((0,0,1.25),(.25,.75,.28),m,.1,e); obox((0,-.85,1.65),(.12,.25,.3),m,.06,e,rot=(R(-30),0,0)); obox((0,-1.05,1.95),(.12,.3,.12),m,.05,e)
    for dx in (-.15,.15):
        for dy in (-.55,.55): obox((dx,dy,.5),(.06,.06,.5),m,.02,e)
    obox((0,-.6,1.95),(.04,.25,.18),M('#3A2414',.6),.02,e); obox((0,.1,1.56),(.28,.35,.04),M('#2B5AA8',.7,kind='fabric'),.02,e)
    return e
def balloons(loc,n=9,seed=2):
    r=random.Random(seed); e=empty(loc)
    for k in range(n):
        x,y,z=r.uniform(-.35,.35),r.uniform(-.2,.2),2.3+r.uniform(0,.8); oico((x,y,z),.16,M(r.choice(['#E8423A','#F2C14E','#2B8AE8','#7CD86A','#E8709A']),.3,spec=.9),e,sc=(1,1,1.2),sub=2)
        ocyl(((x)/2,(y)/2,z/2+.6),.004,z-1.2,M('#F4F1EA',.5),e,rot=(0,0,0),seg=4)
    return e
def mat(loc,col='#C8372D',rz=0):
    B.box(loc,(1.3,1.0,.01),M(col,.9,kind='fabric',h2='#F2C14E',sc=5),0,rot=(0,0,R(rz)))
def foodbag2(e,s=1.0,col='#F4F1EA'):
    obox((0,-.1,.14*s),(.14*s,.09*s,.15*s),M(col,.9,kind='fabric'),.03,e); obox((0,-.1,.32*s),(.02,.08*s,.05*s),M(col,.9),0,e)
def corn_cob(e,s=1.0): ocyl((0,-.08,.1*s),.035*s,.22*s,M('#E8B030',.6),e,rot=(0,0,0),seg=8); ocyl((0,-.08,-.03),.02*s,.08*s,M('#6A8A3A',.6),e,rot=(0,0,0),seg=6)
def tea_cup(e,s=1.0): ocyl((0,-.08,.05*s),.045*s,.09*s,M('#F4F1EA',.4),e,rot=(0,0,0),seg=10,r2=.035*s); ocyl((0,-.08,.095*s),.04*s,.005,M('#B8743A',.5),e,rot=(0,0,0),seg=10)
def plate_food(e,s=1.0):
    ocyl((0,-.08,.02),.18*s,.02,M('#F4F1EA',.4),e,rot=(0,0,0),seg=16); oico((0,-.08,.05),.12*s,M('#E8B84A',.8),e,sc=(1,1,.35),sub=2)
