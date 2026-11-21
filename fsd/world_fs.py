# sets for "Everyone in Faisalabad is a businessman": Ghanta Ghar plaza + bazaar, borrowed-clothes stall, textile mill, chai dhaba
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=False):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot; a.data.use_shadow=shadow; return a
LEAF=[M('#3E8E4A',.7,kind='leaves'),M('#5FA84A',.7,kind='leaves'),M('#2F7A45',.7,kind='leaves'),M('#74B85A',.7,kind='leaves'),M('#4C9A50',.7,kind='leaves')]
SAND='#D9B98A'; SAND2='#C9A26E'; BRICK='#B5643E'; CHAR='#26262C'; WOOD='#7A4E2E'
FAB=['#C6453A','#2F4E8C','#E8C25A','#3B8E8C','#D98AA8','#F2EBDD','#6C5FB0','#8BB85A','#E07A2E','#1F3A5A','#B8683A','#9E3B4E']
def tree(x,y,s=1.0,seed=1):
    r=random.Random(seed); B.cyl((x,y,1.5*s),.18*s,3.0*s,M('#6B4A30',.85,kind='wood'),seg=8,r2=.13*s)
    for k in range(6): B.ico((x+r.uniform(-.9,.9)*s,y+r.uniform(-.9,.9)*s,(3.2+r.uniform(0,1.2))*s),r.uniform(.8,1.2)*s,LEAF[k%5],sc=(1,1,.85),sub=1)
def palm(x,y,s=1.0,seed=1):
    r=random.Random(seed); B.cyl((x,y,2.6*s),.16*s,5.2*s,M('#8A6A48',.8,kind='wood'),seg=8,r2=.11*s)
    for i in range(8):
        a=2*pi*i/8+r.uniform(-.2,.2); B.box((x+math.cos(a)*1.0*s,y+math.sin(a)*1.0*s,5.05*s),(1.1*s,.22*s,.03),LEAF[i%5],0,rot=(0,R(24),a))
def wire(a,b,sag=.6,n=10,mat=None):
    mat=mat or M('#18181C',.6); pts=[Vector(a).lerp(Vector(b),i/n)-Vector((0,0,sag*math.sin(pi*i/n))) for i in range(n+1)]
    for i in range(n):
        p,q=pts[i],pts[i+1]; d=q-p; B.cyl(tuple((p+q)/2),.012,d.length,mat,rot=tuple(d.to_track_quat('Z','Y').to_euler()),seg=4)
# ---------------------------------------------------------------- vehicles
def rickshaw(x,y,rz=0,col='#2E8B5A'):
    r=empty((x,y,0),rot=(0,0,R(rz))); C_=M(col,.35,metal=.3); BK=M('#1B1B20',.6)
    obox((0,0,.62),(1.0,.62,.28),C_,.06,r); obox((-.15,0,1.35),(.9,.66,.48),M('#1B1B20',.7,kind='fabric'),.12,r); obox((.75,0,1.1),(.28,.5,.4),C_,.06,r)
    obox((.95,0,1.2),(.03,.42,.24),M('#22303E',.05,spec=1.0),.01,r); obox((-.2,0,.92),(.5,.55,.12),M('#7A1E2E',.8,kind='fabric'),.04,r)
    obox((-.98,0,.9),(.03,.58,.24),M('#E8C25A',.4),.02,r)
    for k in range(6): obox((-.99,-.45+k*.18,.9),(.012,.06,.18),M(FAB[k],.5),0,r)
    W=[ocyl((sx,sy,.24),.24,.14,M('#111216',.8),r,rot=(R(90),0,0),seg=14) for sx,sy in ((.95,0),(-.6,.58),(-.6,-.58))]
    return r
def bike(x,y,rz=0,col='#C9302C'):
    r=empty((x,y,0),rot=(0,0,R(rz))); C_=M(col,.3,metal=.4)
    for sx in (-.62,.62): ocyl((sx,0,.32),.32,.09,M('#111216',.8),r,rot=(R(90),0,0),seg=16); ocyl((sx,0,.32),.16,.1,M('#C9CDD6',.3,metal=.9),r,rot=(R(90),0,0),seg=10)
    obox((0,0,.62),(.42,.12,.16),C_,.05,r); obox((-.25,0,.8),(.35,.13,.05),M('#1B1B20',.7),.03,r); obox((.55,0,.95),(.04,.38,.03),M(CHAR,.4,metal=.6),.01,r); obox((.6,0,.78),(.06,.08,.12),M('#FFF2C8',.3,emit=2),.02,r)
    return r
def truck_load(x,y,rz=0):
    r=empty((x,y,0),rot=(0,0,R(rz))); obox((1.7,0,1.2),(.7,.95,.9),M('#2E6FB0',.4,metal=.2),.08,r); obox((1.9,0,1.55),(.4,.9,.4),M('#22303E',.05,spec=1.0),.04,r)
    obox((-.6,0,.9),(1.6,1.0,.12),M(WOOD,.7,kind='wood'),.02,r)
    for i in range(3):
        for j in range(2): ocyl((-1.6+i*.95,-.45+j*.9,1.3),.32,.92,M(FAB[(i*2+j)%12],.8,kind='fabric'),r,rot=(0,R(90),0),seg=14)
    for sx,sy in ((1.8,.95),(1.8,-.95),(-1.3,.95),(-1.3,-.95)): ocyl((sx,sy,.42),.42,.26,M('#111216',.8),r,rot=(R(90),0,0),seg=16)
    obox((2.42,0,.8),(.03,.9,.25),M('#E8C25A',.5),.02,r)
    return r
# ---------------------------------------------------------------- Ghanta Ghar (clock tower)
CT=(0,0)   # clock tower centre
def clock_face(cx,cy,z,n,r_=.95):
    a=math.atan2(n[0],-n[1]); e=empty((cx,cy,z),rot=(R(90),0,a))
    ocyl((0,0,0),r_+.12,.08,M('#3A2E22',.5),e,rot=(0,0,0),seg=40); ocyl((0,0,.03),r_,.08,M('#F4EEDD',.35,emit=.35),e,rot=(0,0,0),seg=40)
    for k in range(12):
        an=2*pi*k/12; obox((math.sin(an)*r_*.82,math.cos(an)*r_*.82,.08),(.03 if k%3 else .05,.1 if k%3 else .14,.01),M(CHAR,.5),0,e,rot=(0,0,-an))
    h=empty((0,0,.09),e,rot=(0,0,R(-130))); obox((0,.25,0),(.04,.27,.012),M(CHAR,.4),0,h)
    m=empty((0,0,.1),e,rot=(0,0,R(-20))); obox((0,.38,0),(.025,.4,.012),M(CHAR,.4),0,m)
    ocyl((0,0,.11),.05,.02,M('#C9A24A',.3,metal=.8),e,rot=(0,0,0),seg=10)
    return m
def ghanta_ghar():
    S_=M(SAND,.8,kind='concrete',sc=.35); S2=M(SAND2,.8,kind='concrete',sc=.35); RD=M('#A4553A',.8,kind='concrete',sc=.35); WH=M('#F2EDE2',.6)
    # octagonal plinth with steps
    for k,(rr,h) in enumerate(((6.4,.18),(6.0,.36),(5.6,.54))): B.cyl((0,0,h/2),rr,h,M('#BFAE94',.85,kind='concrete',sc=.4),seg=8,rot=(0,0,R(22.5)))
    B.cyl((0,0,1.6),3.2,2.1,S_,seg=8,rot=(0,0,R(22.5)))
    for a in range(8):
        an=2*pi*a/8; x=3.25*math.cos(an); y=3.25*math.sin(an)
        B.box((x*.98,y*.98,1.45),(.06,1.0,.9),RD,.02,rot=(0,0,an)); B.cyl((x*1.0,y*1.0,2.0),.5,.12,RD,rot=(0,R(90),an),seg=16)
    # main shaft (square with chamfers) in layers
    for k,(z0,z1,w,mat) in enumerate(((2.65,9.5,2.3,S_),(9.5,10.0,2.6,S2),(10.0,13.8,2.1,S_),(13.8,14.3,2.5,S2),(14.3,17.6,1.85,S_))):
        B.box((0,0,(z0+z1)/2),(w,w,(z1-z0)/2),mat,.05); B.box((0,0,(z0+z1)/2),(w*1.04,w*1.04,(z1-z0)/2*.98),mat,.05,rot=(0,0,R(45))) if False else None
        for s in (-1,1):
            for t_ in (-1,1): B.box((s*w,t_*w,(z0+z1)/2),(.18,.18,(z1-z0)/2),S2,.03)
    for z in (4.0,6.8):        # arched windows on the shaft
        for a in range(4):
            an=pi/2*a; n=(math.sin(an),-math.cos(an)); x=n[0]*2.31; y=n[1]*2.31
            B.box((x,y,z),(.5 if a%2==0 else .02,.02 if a%2==0 else .5,.85),M('#5A3A22',.6),0); B.cyl((x,y,z+.85),.5,.04,RD,rot=(R(90),0,an),seg=16)
            B.box((x+n[0]*.02,y+n[1]*.02,z-.9),(.65 if a%2==0 else .04,.04 if a%2==0 else .65,.06),RD,.01)
    for a in range(4):
        an=pi/2*a; n=(math.sin(an),-math.cos(an)); clock_face(n[0]*2.13,n[1]*2.13,12.0,n,1.15)
        for k in range(5): B.box((n[0]*2.55+(k-2)*.5*abs(n[1]),n[1]*2.55+(k-2)*.5*abs(n[0]),14.5),(.12,.12,.25),S2,.02)
    # chhatri (domed kiosk) top
    for s in (-1,1):
        for t_ in (-1,1): B.cyl((s*1.3,t_*1.3,18.5),.14,1.8,WH,seg=10)
    B.box((0,0,19.45),(1.65,1.65,.15),S2,.03); B.ico((0,0,20.2),1.55,M('#F2EDE2',.5),sc=(1,1,.9),sub=3); B.cyl((0,0,21.7),.08,.8,M('#C9A24A',.3,metal=.8),seg=8); B.ico((0,0,22.1),.15,M('#C9A24A',.3,metal=.8),sub=2)
    for a in range(4):
        an=pi/2*a+pi/4; B.ico((math.cos(an)*1.85,math.sin(an)*1.85,17.95),.35,WH,sc=(1,1,.9),sub=2)
    # garden ring + railing + lamps around the plinth
    B.cyl((0,0,.04),9.5,.08,M('#5F9A48',.9,kind='leaves'),seg=48); B.cyl((0,0,.06),6.8,.1,M('#BFAE94',.85,kind='concrete',sc=.4),seg=8,rot=(0,0,R(22.5)))
    for k in range(48):
        an=2*pi*k/48; B.cyl((9.45*math.cos(an),9.45*math.sin(an),.45),.035,.9,M(CHAR,.4,metal=.5),seg=6)
    for k in range(4):
        an=2*pi*k/4+pi/4; B.cyl((9.45*math.cos(an),9.45*math.sin(an),2.0),.08,4.0,M(CHAR,.4,metal=.5),seg=8); B.ico((9.45*math.cos(an),9.45*math.sin(an),4.1),.22,M('#FFE2A8',.3,emit=5),sub=2)
    r=random.Random(3)
    for k in range(22):
        an=2*pi*k/22+.07; rr=r.uniform(7.3,8.9); B.ico((rr*math.cos(an),rr*math.sin(an),.35),r.uniform(.3,.55),LEAF[k%5],sc=(1,1,.7),sub=1)
        if k%3==0: B.ico((rr*math.cos(an),rr*math.sin(an),.75),.1,M(r.choice(['#E8483A','#F2C12E','#F4F1EA','#D98AA8']),.6),sub=1)
    tree(6.2,6.2,1.1,1); tree(-6.4,5.8,1.0,2); tree(-6.0,-6.3,1.05,3); tree(6.4,-6.0,1.0,4)
    B.box((0,-6.3,.62),(1.0,.3,.06),M(WOOD,.6,kind='wood'),.02)
    for s in (-1,1): B.box((s*.85,-6.3,.3),(.08,.25,.3),M(CHAR,.4,metal=.5),.01)
SHOPC=['#E8DCC8','#D8C2A0','#F0E8DC','#C9A888','#E4CDB0','#D9C8B8','#CFB89A','#E8D2B4']
def shop_row(x0,x1,y,face,seed,depth=7.0,h=(7,12),rz=0):
    """bazaar facade line along x from x0 to x1 at y; face=+1/-1 (direction the fronts look, in y)"""
    r=random.Random(seed); x=x0
    while x<x1-1:
        w=r.uniform(3.2,5.0); h_=r.uniform(*h); col=r.choice(SHOPC); cx=x+w/2; cy=y-face*depth/2
        B.box((cx,cy,h_/2),(w/2-.03,depth/2,h_/2),M(col,.85,kind='wall'),.02)
        fy=y+face*.01
        # shutter/opening with merchandise
        B.box((cx,fy-face*.25,1.45),(w/2-.35,.02,1.45),M('#2A221C',.9),0)
        for k in range(int(w/0.55)):
            c=r.choice(FAB); xx=cx-w/2+.5+k*.5
            if xx>cx+w/2-.45: break
            B.box((xx,fy-face*.5,1.6+r.uniform(-.2,.2)),(.2,.25,r.uniform(.55,1.05)),M(c,.85,kind='fabric'),.03)
        for k in range(r.randint(2,4)): B.box((cx-w/2+.6+k*.9,fy+face*.25,.45),(.35,.3,.45),M(r.choice(FAB),.85,kind='fabric'),.05)
        B.box((cx,fy+face*.05,3.25),(w/2-.15,.06,.42),M(r.choice(['#1F3A5A','#7A1E2E','#2E6E3A','#F2C12E','#C6453A','#22242B']),.5,emit=.25),.02)
        for j in range(int(w*1.2)): B.box((cx-w/2+.4+j*.75,fy+face*.07,3.25+r.uniform(-.1,.1)),(.24,.01,.07),M('#F4F1EA',.5,emit=.4),0)
        B.box((cx,fy+face*.55,2.85),(w/2,.55,.04),M(r.choice(['#2E6E3A','#C6453A','#E8C25A','#3B8E8C','#7A1E2E']),.8,kind='fabric'),.01,rot=(R(-12*face),0,0))
        for fl in range(1,int(h_/3.1)):
            z=fl*3.1+1.5
            if z>h_-.8: break
            for k in range(max(1,int(w/1.6))):
                xx=cx-w/2+w*(k+.5)/max(1,int(w/1.6))
                B.box((xx,fy,z),(.42,.02,.62),M('#3A4E5E',.2,spec=.8) if r.random()<.7 else M('#FFD9A0',.4,emit=1.2),0); B.box((xx,fy+face*.05,z-.66),(.5,.06,.04),M(shade(col,.75),.7),.01)
            if r.random()<.4: B.box((cx,fy+face*.35,z-.8),(w/2-.3,.35,.05),M(shade(col,.8),.7),.01); B.box((cx,fy+face*.68,z-.45),(w/2-.3,.02,.35),M(CHAR,.4,metal=.5),0)
        if r.random()<.5: B.box((cx,fy+face*.1,h_-.9),(w/2-.4,.04,.45),M(r.choice(['#F2C12E','#2E8B5A','#C6453A','#2F4E8C']),.4,emit=.8),.02)
        if r.random()<.6: B.cyl((cx+r.uniform(-1,1),cy,h_+.5),.45,1.0,M(r.choice(['#2B2C33','#E8E4D8','#3E6FB0']),.5),seg=10)
        x+=w
def bazaar_lane(L=40,seed=5,clutter=True):
    """lane along x, ground y[-4,4]; shop fronts at y=+4 (facing -y) and y=-4 (facing +y)"""
    B.box((0,0,-.05),(L,4.05,.05),M('#8E8478',.9,kind='concrete',sc=.4),0)
    shop_row(-L,L,4.0,-1,seed); shop_row(-L,L,-4.0,1,seed+50)
    r=random.Random(seed)
    if clutter:
        for i in range(int(L/3)):
            x=r.uniform(-L+3,L-3); wire((x,4.0,r.uniform(5.5,7.5)),(x+r.uniform(-3,3),-4.0,r.uniform(5.5,7.5)),r.uniform(.4,1.0))
        for i in range(int(L/7)):
            x=-L+5+i*7+r.uniform(-1,1); B.cyl((x,3.6,3.4),.09,6.8,M('#9A9A96',.7,kind='concrete'),seg=8); B.box((x,3.6,6.6),(.04,.5,.04),M('#6A6A66',.7),.01)
            for k in range(3): wire((x,3.6,6.4-k*.15),(x+7,3.6,6.4-k*.15),.35)
def city_backdrop(seed=1,R0=40,R1=120,n=180):
    r=random.Random(seed)
    for i in range(n):
        an=r.uniform(0,2*pi); rr=r.uniform(R0,R1); x=rr*math.cos(an); y=rr*math.sin(an); w=r.uniform(6,12); h=r.uniform(6,16)
        if y<-25 and -110<x<25: continue
        B.box((x,y,h/2),(w/2,w/2,h/2),M(r.choice(SHOPC+['#B5643E','#A86848']),.9,kind='wall'),0)
        if r.random()<.35: B.box((x,y,h+.6),(.6,.6,.6),M('#2B2C33',.5),.02)
        if r.random()<.15: B.ico((x+w/2+1,y,3.4),1.6,LEAF[i%5],sc=(1,1,.9),sub=1)
def plaza(night=False,with_dhaba=True):
    """Ghanta Ghar at origin, 8 bazaar roads radiating; the friends' bench is at (0,-6.3); chai dhaba at (8.5,-11.5)"""
    ghanta_ghar()
    B.box((0,0,-.06),(60,60,.05),M('#4A4A50',.85,kind='asphalt'),0)
    B.cyl((0,0,-.02),13.0,.04,M('#5A5A60',.85,kind='asphalt'),seg=48)
    for k in range(8):
        an=2*pi*k/8+pi/8;
        for j in range(14): B.box(((13.5+j*1.5)*math.cos(an),(13.5+j*1.5)*math.sin(an),-.003),(.5,.06,.005),M('#E8E4D8',.6),0,rot=(0,0,an))
    # ring of bazaar buildings around the roundabout (8 blocks between 8 roads)
    r=random.Random(11)
    for k in range(8):
        an=2*pi*k/8; e_=empty((0,0,0),rot=(0,0,an));
        for j in range(3):
            w=r.uniform(5,6.5); h=r.uniform(8,13); col=r.choice(SHOPC); d=8; rr=18.5+d/2
            bx=(rr*math.cos(an)+(j-1)*5.6*-math.sin(an),rr*math.sin(an)+(j-1)*5.6*math.cos(an))
            B.box((bx[0],bx[1],h/2),(w/2,d/2,h/2),M(col,.85,kind='wall'),.02,rot=(0,0,an+pi/2))
            fx_=bx[0]-math.cos(an)*(d/2+.02); fy_=bx[1]-math.sin(an)*(d/2+.02)
            B.box((fx_,fy_,1.45),(w/2-.4,.02,1.45),M('#2A221C',.9),0,rot=(0,0,an+pi/2))
            for q in range(7): B.box((fx_+math.cos(an)*.4+(q-3)*.62*-math.sin(an),fy_+math.sin(an)*.4+(q-3)*.62*math.cos(an),1.6+r.uniform(-.2,.2)),(.22,.22,r.uniform(.55,1.0)),M(r.choice(FAB),.85,kind='fabric'),.03,rot=(0,0,an+pi/2))
            B.box((fx_-math.cos(an)*.06,fy_-math.sin(an)*.06,3.25),(w/2-.2,.06,.42),M(r.choice(['#1F3A5A','#7A1E2E','#2E6E3A','#F2C12E','#C6453A']),.5,emit=.3),.02,rot=(0,0,an+pi/2))
            B.box((fx_-math.cos(an)*.6,fy_-math.sin(an)*.6,2.85),(w/2,.55,.04),M(r.choice(['#2E6E3A','#C6453A','#E8C25A','#3B8E8C']),.8,kind='fabric'),.01,rot=(R(12),0,an+pi/2))
            for fl in range(1,int(h/3.1)):
                z=fl*3.1+1.5
                if z>h-.8: break
                for q in range(3): B.box((fx_+(q-1)*1.6*-math.sin(an),fy_+(q-1)*1.6*math.cos(an),z),(.42,.02,.62),M('#3A4E5E',.2,spec=.8) if r.random()<.7 else M('#FFD9A0',.4,emit=1.2),0,rot=(0,0,an+pi/2))
            if r.random()<.6: B.box((fx_,fy_,h-1),(w/2-.5,.04,.45),M(r.choice(['#F2C12E','#2E8B5A','#C6453A','#2F4E8C']),.4,emit=.8),.02,rot=(0,0,an+pi/2))
        for q in range(4):
            a2=an+r.uniform(-.25,.25); rr=r.uniform(14.5,16); wire((rr*math.cos(a2),rr*math.sin(a2),7),(rr*math.cos(a2+.4),rr*math.sin(a2+.4),7),.5)
    city_backdrop(2,40,140,220)
    if with_dhaba: dhaba(8.5,-11.5,135)
def dhaba(x,y,rz):
    """roadside chai stall: tin roof on poles, counter with stove + big kettle, glass jars, benches + plastic chairs"""
    e=empty((x,y,0),rot=(0,0,R(rz)))
    for sx in (-1.6,1.6):
        for sy in (-1.4,1.4): ocyl((sx,sy,1.35),.05,2.7,M('#6A6A66',.6,metal=.4),e,rot=(0,0,0),seg=8)
    obox((0,0,2.76),(1.9,1.7,.04),M('#8A9AA8',.5,metal=.5),.01,e,rot=(R(-6),0,0)); obox((0,-1.72,2.6),(1.9,.02,.2),M('#C6453A',.6,emit=.3),.01,e)
    text('CHAI',(0,-1.75,2.6),(0,-1,0),.26,M('#FFFFFF',.3,emit=1.5),ex=.01,parent=e) if False else None
    obox((0,.9,.5),(1.5,.4,.5),M('#5A3A22',.7,kind='wood'),.02,e); obox((0,.9,1.02),(1.55,.45,.03),M('#C9CDD6',.3,metal=.7),.01,e)
    ocyl((-.8,.9,1.15),.22,.2,M('#2B2C33',.5,metal=.4),e,rot=(0,0,0),seg=14); oico((-.8,.9,1.25),.13,M('#3A7AFF',.3,emit=3),e,sc=(1,1,.3),sub=1)
    k=ocyl((-.8,.9,1.43),.2,.32,M('#C9CDD6',.25,metal=.9),e,rot=(0,0,0),seg=16,r2=.15); ocyl((-.6,.9,1.5),.03,.22,M('#C9CDD6',.25,metal=.9),e,rot=(0,R(55),0),seg=8)
    for q in range(5): ocyl((.0+q*.18,.85,1.1),.05,.12,M('#E8DCC0',.4),e,rot=(0,0,0),seg=10,r2=.06)
    for q in range(3): ocyl((.9+q*.22,1.0,1.22),.09,.36,M('#DDEEF6',.05,spec=1.0,alpha=.35),e,rot=(0,0,0),seg=12); oico((.9+q*.22,1.0,1.18),.08,M(['#E8C25A','#D9963E','#C6453A'][q],.6),e,sc=(1,1,1.4),sub=1)
    for sy in (-.6,):
        obox((0,sy,.42),(1.3,.22,.05),M(WOOD,.7,kind='wood'),.02,e)
        for sx in (-1.1,1.1): obox((sx,sy,.2),(.06,.18,.2),M(WOOD,.7,kind='wood'),.01,e)
    steam((x,y,1.7),0,200,n=10,size=.06)
    return e
# ---------------------------------------------------------------- the stall (borrowed clothes) in a bazaar lane
STALL=(0,0)
def stall_set():
    bazaar_lane(40,seed=21)
    T=M(WOOD,.7,kind='wood')
    B.box((0,.4,.82),(1.3,.6,.04),T,.02);
    for sx in (-1.2,1.2):
        for sy in (-.1,.9): B.box((sx,sy,.4),(.05,.05,.4),T,.01)
    B.box((0,.4,.85),(1.25,.58,.01),M('#F2EBDD',.85,kind='fabric'),0)
    r=random.Random(4)
    for i in range(6):
        c=FAB[(i*5)%12];
        for k in range(3): B.box((-.95+i*.38,.35+(i%2)*.18,.89+k*.045),(.17,.22,.022),M(c,.8,kind='fabric'),.01)
    # hanging rack with shirts
    B.box((0,1.25,2.05),(1.3,.03,.03),M('#C9CDD6',.3,metal=.8),.01)
    for sx in (-1.3,1.3): B.box((sx,1.25,1.05),(.03,.03,1.0),M('#C9CDD6',.3,metal=.8),.01)
    for i in range(7):
        x=-1.05+i*.35; c=FAB[(i*3+2)%12]; B.box((x,1.25,1.65),(.15,.03,.34),M(c,.8,kind='fabric'),.01); B.box((x,1.25,1.88),(.18,.03,.06),M(c,.8,kind='fabric'),.01)
        B.box((x,1.25,2.0),(.07,.01,.05),M('#C9CDD6',.3,metal=.8),0)
    # banner
    B.box((0,1.3,2.55),(1.45,.03,.35),M('#1F3A5A',.6,emit=.15),.02)
    text('SHAHZAIB INTERNATIONAL',(0,1.26,2.66),(0,-1,0),.16,M('#F2C12E',.3,emit=1.2),ex=.008); text('CEO GARMENTS',(0,1.26,2.42),(0,-1,0),.14,M('#FFFFFF',.3,emit=1.0),ex=.008)
    # umbrella
    B.cyl((1.45,.6,1.4),.03,2.8,M('#C9CDD6',.3,metal=.8),seg=8)
    for k in range(8): B.box((1.45+.0,.6,2.8),(1.15,.55,.02),M(['#C6453A','#F4F1EA'][k%2],.8,kind='fabric'),.01,rot=(R(10),0,R(22.5*k)))
    # stool + price card + mirror
    B.cyl((-1.75,.9,.25),.22,.5,M('#2E6FB0',.6),seg=12); B.box((.85,.05,.98),(.14,.02,.09),M('#FFFFFF',.5),.005,rot=(R(-20),0,0)); text('2500',(.85,.03,.98),(0,-1,0),.07,M('#C6453A',.4),ex=.004,rot=(R(-20),0,0)) if False else None
def stall_light(mood='golden'):
    S_,w,rp,bg=setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=60); return S_,w
# ---------------------------------------------------------------- textile mill
def loom(x,y,rz=0,seed=1,col=None):
    r=random.Random(seed); e=empty((x,y,0),rot=(0,0,R(rz))); G=M('#4E6A5C',.45,metal=.35); D=M('#2B2C33',.5,metal=.5)
    for sx in (-1.0,1.0): obox((sx,0,.7),(.08,.6,.7),G,.02,e)
    obox((0,-.55,1.32),(1.05,.06,.06),D,.01,e); obox((0,.55,.92),(1.05,.08,.08),D,.01,e)
    ocyl((0,.62,.62),.14,2.0,D,e,rot=(0,R(90),0),seg=14); ocyl((0,-.62,.5),.2,1.95,M(col or r.choice(FAB),.85,kind='fabric'),e,rot=(0,R(90),0),seg=16)
    obox((0,0,1.05),(.95,.55,.01),M(col or r.choice(FAB),.8,kind='fabric'),0,e,rot=(R(18),0,0))
    for k in range(18): obox((-.9+k*.106,.3,1.18),(.004,.3,.004),M('#F4F1EA',.5),0,e,rot=(R(18),0,0))
    beater=obox((0,-.1,1.2),(1.0,.04,.12),D,.01,e); shuttle=obox((0,-.1,1.12),(.12,.035,.035),M('#C9A24A',.4,metal=.6),.01,e)
    obox((1.12,0,.9),(.14,.25,.25),M('#C6453A',.5),.02,e); ocyl((1.25,0,.9),.2,.04,D,e,rot=(0,R(90),0),seg=14)
    return dict(root=e,beater=beater,shuttle=shuttle,ph=r.uniform(0,6))
def mill(light=True):
    """mill hall x[-14,14] y[-10,10], sawtooth roof; Chacha's desk area at (0,-6.5); looms in rows for y>-3"""
    FL=M('#7E7A74',.8,kind='concrete',sc=.5); WL=M('#E4DCCB',.85,kind='wall'); BR=M(BRICK,.85,kind='concrete',sc=.3)
    B.box((0,0,-.05),(14.2,10.2,.05),FL,0); B.box((0,10.05,3.5),(14.2,.05,3.5),WL,0); B.box((14.05,0,3.5),(.05,10.2,3.5),WL,0); B.box((-14.05,0,3.5),(.05,10.2,3.5),WL,0)
    B.box((0,-10.05,1.2),(14.2,.05,1.2),WL,0); B.box((0,-10.05,6.0),(14.2,.05,1.0),WL,0)
    for xx in range(-12,13,4): B.box((xx,-10.05,3.6),(1.5,.03,1.3),M('#FFE7BE',.3,emit=2.0),0); B.box((xx,-10.02,3.6),(1.55,.05,.04),M(CHAR,.5),.01); B.box((xx,-10.02,3.6),(.04,.05,1.35),M(CHAR,.5),.01)
    B.box((0,10,.9),(14.1,.06,.9),BR,.01); B.box((14,0,.9),(.06,10.1,.9),BR,.01); B.box((-14,0,.9),(.06,10.1,.9),BR,.01)
    for k in range(7):
        y0=-10+k*3.0; B.box((0,y0+1.5,7.0),(14.2,1.55,.06),M('#9AA6AE',.5,metal=.4),.01,rot=(R(-22),0,0)); B.box((0,y0+2.85,7.4),(14.2,.05,.55),M('#FFF2D8',.3,emit=2.4),0)
    for xx in range(-12,13,6):
        for yy in (-6,0,6): B.cyl((xx,yy,3.5),.14,7.0,M('#3E6FB0',.5,metal=.4),seg=8)
    for xx in range(-12,13,6): B.box((xx,0,6.6),(.15,10,.2),M('#3E6FB0',.5,metal=.4),.01)
    for xx in range(-9,10,6):
        for yy in (-4,3):
            B.cyl((xx,yy,6.2),.03,.8,M(CHAR,.5),seg=6); fn=empty((xx,yy,5.8)); fn['fan']=1
            for k in range(3): obox((.45*math.cos(k*2.094),.45*math.sin(k*2.094),0),(.45,.07,.01),M('#7A7E86',.5,metal=.3),.01,fn,rot=(0,0,k*2.094))
            ocyl((0,0,0),.1,.1,M('#5A5E66',.5,metal=.4),fn,rot=(0,0,0),seg=10)
            def spin(o,t): o.rotation_euler[2]=t*9.0
            fx.add(fn,spin)
    for xx in range(-11,12,4):
        for yy in (-7.5,-1.5,4.5): B.box((xx,yy,5.4),(1.0,.08,.03),M('#F4FAFF',.3,emit=6),.01); B.box((xx,yy,5.48),(1.05,.12,.04),M('#C9CDD6',.4,metal=.4),.01)
    L=[]
    for i,yy in enumerate((-1.2,2.0,5.2,8.2)):
        for j,xx in enumerate((-10.5,-6.8,-3.1,3.1,6.8,10.5)): L.append(loom(xx,yy,0,i*7+j,FAB[(i*3+j)%12]))
    # fabric roll stacks + bales + cart
    r=random.Random(9)
    for (sx,sy,n_) in ((-12.4,-8.2,4),(12.4,-8.2,4),(-12.6,-4.4,3),(12.6,-4.4,3)):
        for a in range(n_):
            for b in range(3-a%2): B.cyl((sx,sy+b*.85-.85+(a%2)*.42,.4+a*.74),.38,1.8,M(r.choice(FAB),.85,kind='fabric'),rot=(0,R(90),0),seg=16); B.cyl((sx,sy+b*.85-.85+(a%2)*.42,.4+a*.74),.12,1.84,M('#C9A880',.7),rot=(0,R(90),0),seg=10)
    for k in range(5): B.box((-8.8+k*1.1,-8.8,.45),(.5,.5,.45),M('#D8C8A8',.9,kind='fabric'),.08); B.box((-8.8+k*1.1,-8.8,.45),(.51,.04,.46),M('#8A6A48',.7),.0)
    B.box((8.6,-8.4,.55),(.9,.6,.04),M('#3E6FB0',.5,metal=.4),.01)
    for k in range(3): B.cyl((8.6,-8.75+k*.36,.78),.17,1.6,M(FAB[k*4],.85,kind='fabric'),rot=(0,R(90),0),seg=14)
    # Chacha's desk: steel desk, ledger, phone, calculator, chair, wall calendar + framed "JAMEEL TEXTILE MILLS"
    D=M('#6A4A32',.55,kind='wood',sc=2.5); B.box((0,-6.2,.78),(1.25,.62,.04),D,.02); B.box((0,-5.7,.4),(1.2,.1,.38),D,.01)
    for s in (-1,1): B.box((s*1.15,-6.2,.4),(.08,.58,.38),D,.01)
    B.box((-.35,-6.35,.84),(.3,.22,.02),M('#F4F1EA',.6),.01,rot=(0,0,.1)); B.box((-.35,-6.35,.86),(.29,.005,.012),M('#7A1E2E',.6),0,rot=(0,0,.1))
    B.box((.5,-6.3,.84),(.11,.15,.02),M(CHAR,.4),.01); B.box((.5,-6.4,.86),(.08,.04,.005),M('#9ACD9A',.5,emit=.4),0)
    B.cyl((.85,-6.15,.9),.05,.1,M('#E8DCC0',.4),seg=10,r2=.06)
    B.box((0,-4.95,1.0),(.42,.38,.06),M('#2B2C33',.6,kind='fabric'),.04); B.box((0,-4.6,1.55),(.42,.06,.5),M('#2B2C33',.6,kind='fabric'),.06)
    for s in (-1,1): B.box((s*.35,-4.95,.5),(.04,.3,.48),M('#5A5E66',.4,metal=.5),.01)
    B.box((-3.6,-9.96,2.6),(1.6,.03,.42),M('#1F3A5A',.5,emit=.2),.02); text('JAMEEL TEXTILE MILLS',(-3.6,-9.92,2.6),(0,1,0),.24,M('#F2C12E',.3,emit=1.2),ex=.01)
    B.box((3.6,-9.96,2.5),(.42,.03,.55),M('#FFFFFF',.6),.01); B.box((3.6,-9.94,2.86),(.42,.01,.12),M('#C6453A',.5),0)
    for k in range(6): B.box((3.4+(k%3)*.2,-9.93,2.6-(k//3)*.2),(.07,.004,.07),M('#3A3D47',.6),0)
    if light:
        S,A,w,bg=setup_interior('day',room=(0,0,6.5),res=PCT,samples=SAMPLES); A.data.size=24; A.data.energy=900; A.data.color=(1,.98,.94)
        point((0,-6,4),300,(1,.95,.86),.6); point((-7,2,4.5),260,(1,.98,.92),.6,shadow=False); point((7,2,4.5),260,(1,.98,.92),.6,shadow=False)
        area((0,-9.6,3.4),900,(22,2.2),(1,.92,.78),rot=(R(-90),0,0))
    return L
def loom_run(L,t,on=1.0):
    for l in L:
        p=t*7.0+l['ph']; l['beater'].location[1]=-.1+.13*math.sin(p)*on; l['shuttle'].location[0]=.82*math.sin(p*.5)*on
def mill_sound_spots(): return None
# ---------------------------------------------------------------- small props
def kurta_shirt(loc,col,rz=0,parent=None):
    e=empty(loc,parent,rot=(0,0,R(rz))); m=M(col,.8,kind='fabric'); obox((0,0,0),(.2,.012,.28),m,.01,e); obox((-.26,0,.17),(.1,.012,.12),m,.01,e,rot=(0,R(35),0)); obox((.26,0,.17),(.1,.012,.12),m,.01,e,rot=(0,R(-35),0))
    obox((0,-.014,.22),(.06,.004,.06),M(shade(col,.7),.7),0,e); return e
def cup(loc,parent=None):
    e=empty(loc,parent); ocyl((0,0,.05),.045,.1,M('#E8DCC0',.4),e,rot=(0,0,0),seg=12,r2=.052); ocyl((0,0,.092),.047,.012,M('#B5784A',.4),e,rot=(0,0,0),seg=12); return e
