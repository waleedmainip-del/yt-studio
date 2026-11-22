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
def parked_cars(seed=4):
    r=random.Random(seed); C=[]
    for k in range(9):
        x=-36+k*8+r.uniform(-1,1); C.append(car((x,-12.6,0),90 if k%2 else -90,r.choice(['#C8372D','#F4F1EA','#16171C','#2B5AA8','#9A9AA2','#D9B24A']),seed=k))
    return C
def stall(x,y,kind,col,label_):
    wd=M('#7A5236',.6,kind='wood'); B.box((x,y,.45),(.9,.5,.45),wd,.03); B.box((x,y,.92),(.95,.55,.03),M('#E8E4DA',.6),.01)
    for dx in (-.85,.85): B.cyl((x+dx,y-.45,1.4),.03,2.0,M('#8A8E96',.3,metal=.6),seg=6)
    B.box((x,y+.1,2.4),(1.1,.75,.05),M(col,.85,kind='fabric',h2='#F4F1EA',sc=4),.02,rot=(R(12),0,0))
    B.box((x,y+.52,1.6),(.8,.03,.18),M('#16171C',.5),0); stext(label_,(x,y+.56,1.6),.16,'#FFF3B0',n=(0,1,0),e=1.2)
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
