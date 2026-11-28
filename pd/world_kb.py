# Sets for "Karachi - People Can Never Say No To Biryani" (Pakistan city series):
#   dhaba_k()        - Quetta-style chai hotel under a tin awning, golden hour (scene 1)
#   street_k(fx_)    - Burns Road style food street at dusk, biryani degs, string lights (hook + scene 2)
#   lawn_k()         - night lawn in front of a floodlit colonial hall, charpai picnic (scenes 3-4, ending)
# World scale: characters ~2.3 units tall, props ~1.3x real size. Vehicles scaled x VSC.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
VSC=1.7
def palm(x,y,s=1.0,seed=0):
    r=random.Random(seed); lean=r.uniform(-.25,.25); tr=M('#8A6A4A',.85)
    for k in range(7): B.cyl((x+lean*k*.25*s,y,(.45+k*.9)*s),(.2-.012*k)*s,.92*s,tr,seg=8)
    tx,tz=x+lean*1.75*s,6.7*s
    for k in range(9):
        a=k*2*pi/9+r.uniform(-.2,.2)
        for j in range(4):
            d=(.5+j*.55)*s; B.box((tx+math.cos(a)*d,y+math.sin(a)*d,tz-(j*j)*.12*s),(.32*s,.11*s,.02),M(shade('#3F7A3A',1+.1*j),.8,kind='leaves'),.01,rot=(0,R(18+j*12),a))
    for k in range(4): B.ico((tx+math.cos(k*1.6)*.25*s,y+math.sin(k*1.6)*.25*s,tz-.3*s),.14*s,M('#7A5A2A',.7),sub=1)
def bush(x,y,s=1.0,col='#3F7A3A'):
    for dx,dy,dz,r_ in ((0,0,.45,.6),(.45,.2,.35,.45),(-.4,-.1,.38,.48)): B.ico((x+dx*s,y+dy*s,dz*s),r_*s,M(shade(col,1+.1*math.sin(x+dz*5)),.85,kind='leaves'),sub=1)
def pchair(x,y,rz,col):
    """plastic chair (seat .56) facing rz"""
    cm=M(col,.45); e=empty((x,y,0),rot=(0,0,R(rz)))
    obox((0,0,.555),(.27,.26,.03),cm,.03,e)
    for sx in (-.22,.22):
        for sy in (-.21,.21): ocyl((sx,sy,.27),.025,.54,cm,e,rot=(0,0,0),seg=6)
    obox((0,.26,.86),(.27,.025,.3),cm,.03,e,rot=(R(-8),0,0))
    for k in range(3): obox((-.14+k*.14,.27,.9),(.04,.03,.16),M(shade(col,.7),.5),.01,e)
    return e
def stool(x,y,col):
    cm=M(col,.45); B.cyl((x,y,.56),.26,.05,cm,seg=16); B.cyl((x,y,.28),.22,.52,cm,seg=16,r2=.26); B.cyl((x,y,.3),.12,.5,M(shade(col,.6),.5),seg=12)
def charpai(x,y,rz=0,L_=2.6,W_=1.25):
    """rope bed: seat height .6, long axis along local x"""
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#7A4E2A',.6,kind='wood',sc=.6); rope=M('#D9C9A0',.85,kind='fabric')
    for sy in (-1,1): obox((0,sy*W_/2,.55),(L_/2,.06,.06),wd,.02,e)
    for sx in (-1,1): obox((sx*L_/2,0,.55),(.06,W_/2,.06),wd,.02,e)
    for sx in (-1,1):
        for sy in (-1,1): ocyl((sx*(L_/2-.02),sy*(W_/2-.02),.3),.07,.6,wd,e,rot=(0,0,0),seg=8)
    for k in range(14): obox((-L_/2+.1+k*(L_-.2)/13,0,.585),(.018,W_/2-.04,.012),rope,0,e)
    for k in range(7): obox((0,-W_/2+.1+k*(W_-.2)/6,.592),(L_/2-.04,.018,.012),rope,0,e)
    return e
def deg(x,y,s=1.0,lid=False,fire=True):
    """big copper biryani pot on a stand"""
    cu=M('#7A3E1A',.3,metal=.85); blk=M('#1A1A1E',.5,metal=.5)
    B.box((x,y,.28*s),(.62*s,.62*s,.28*s),M('#8A4A32',.9,kind='wall',sc=.5),.03); B.box((x,y-.63*s,.22*s),(.25*s,.02,.14*s),M('#16171C',.8),0)
    B.cyl((x,y,.96*s),.5*s,.8*s,cu,seg=24,r2=.7*s); B.cyl((x,y,1.36*s),.6*s,.06*s,M('#5A2E12',.3,metal=.85),seg=24); B.cyl((x,y,1.33*s),.5*s,.05*s,M('#D9A050',.3,metal=.8),seg=24)
    if lid: B.cyl((x,y,1.4*s),.5*s,.08*s,M('#8E5A2A',.4,metal=.6),seg=24)
    else:
        B.cyl((x,y,1.31*s),.47*s,.04*s,M('#F2C45A',.6),seg=24)
        r=random.Random(int(x*13+y))
        for k in range(14): B.ico((x+r.uniform(-.35,.35)*s,y+r.uniform(-.35,.35)*s,1.34*s),.04*s,M(r.choice(['#F4EEDC','#E8A23A','#C8622A','#F4EEDC']),.6),sub=1)
    if fire:
        for k in range(5): B.ico((x+math.cos(k*1.25)*.2*s,y+math.sin(k*1.25)*.2*s,.32*s),.12*s,M('#FF7A1A',.3,emit=6),sc=(1,1,1.6),sub=1)
def minibus(loc,rotz,seed=0):
    """Karachi W-11 style minibus with truck-art panels (static prop)"""
    r=random.Random(seed); e=empty(loc,rot=(0,0,R(rotz))); body=M('#1E8A4A',.4,metal=.2); gl=M('#1A2433',.06,spec=1.0)
    obox((0,0,1.45),(3.4,1.05,1.0),body,.2,e); obox((0,0,2.5),(3.3,1.0,.08),M('#F2C14E',.5),.05,e)
    for k in range(6): obox((-2.6+k*1.0,-1.06,1.75),(.4,.02,.35),gl,.03,e)
    obox((3.41,0,1.75),(.02,.85,.4),gl,.03,e)
    for k in range(9): obox((-3.0+k*.75,-1.07,.95),(.3,.02,.18),M(r.choice(['#E8554D','#F2C14E','#4D8FE8','#E87AB8','#F4F1EA','#35975A']),.5,emit=.15),.02,e)
    for k in range(18): oico((-3.3+k*.39,-1.08,2.32),.05,M(r.choice(['#FF4F7A','#FFD23F','#35C8FF']),.3,emit=1.2),e,sub=1)
    obox((0,-1.08,2.1),(3.2,.02,.06),M('#C8372D',.5),.01,e)
    for sx in (-2.2,2.2):
        for sy in (-1.0,1.0): ocyl((sx,sy,.45),.45,.28,M('#16171C',.7),e,seg=16)
    return e
def bulb_string(p0,p1,n,sag,cols,em,r_=.08):
    for k in range(n+1):
        f=k/n; x=L(p0[0],p1[0],f); y=L(p0[1],p1[1],f); z=L(p0[2],p1[2],f)-sag*math.sin(pi*f)
        B.ico((x,y,z),r_,M(cols[k%len(cols)],.3,emit=em),sub=1)
        if k<n:
            f2=(k+1)/n; x2=L(p0[0],p1[0],f2); y2=L(p0[1],p1[1],f2); z2=L(p0[2],p1[2],f2)-sag*math.sin(pi*f2)
            d=math.dist((x,y,z),(x2,y2,z2)); B.box(((x+x2)/2,(y+y2)/2,(z+z2)/2+.04),(d/2,.008,.008),M('#16171C',.5),0,rot=(0,-math.atan2(z2-z,math.hypot(x2-x,y2-y)),math.atan2(y2-y,x2-x)))
# ------------------------------------------------------------------ biryani box (dynamic)
def biryani_box(loc,s=1.0,rz=0):
    """takeaway biryani box. returns dict with setk(state) where state in full/grab/noaaloo/empty and lid(k)"""
    e=empty(loc,rot=(0,0,R(rz))); card=M('#F4EEE0',.75); prt=M('#C8372D',.5)
    W,D,H=.46*s,.32*s,.12*s
    obox((0,0,H/2),(W,D,H/2),card,.015,e); obox((0,0,H+.004),(W-.02,D-.02,.004),M('#E8DCC4',.8),0,e)
    for sx in (-1,1): obox((sx*W,0,H*.55),(.004,D*.8,H*.25),prt,0,e)
    hinge=empty((0,D,H),e); lid=obox((0,-D,.006),(W,D,.012),card,.012,hinge); obox((0,-D,.02),(W*.7,D*.5,.004),prt,0,hinge)
    stext('KARACHI BIRYANI',(0,-D,.03),.075*s,'#FFFFFF',n=(0,0,1),parent=hinge)
    rice=[]; r=random.Random(7)
    mound=oico((0,0,H+.01),1.0,M('#F2C45A',.65),e,sc=(W*.92,D*.9,.07*s),sub=2); rice.append(mound)
    for k in range(70):
        g=oico((r.uniform(-W*.85,W*.85),r.uniform(-D*.8,D*.8),H+.04*s+r.uniform(0,.03)*s),.02*s,M(r.choice(['#FFF6E0','#F4EEDC','#E89A2A','#D8641E','#FFF6E0']),.6),e,sc=(1.8,.8,.8),sub=1,rot=(0,0,r.uniform(0,3)))
        rice.append(g)
    def piece(x,y,big=1.0):
        p=empty((x,y,H+.07*s),e); oico((0,0,0),.085*s*big,M('#9A4A1E',.55),p,sc=(1.3,1,.8),sub=2); ocyl((.11*s*big,0,0),.018*s,.12*s*big,M('#F4EEE0',.5),p,rot=(0,R(90),0),seg=6); return p
    big=piece(-.18*s,.06*s,1.35); ch2=piece(.2*s,-.1*s,1.0); ch3=piece(.05*s,.14*s,.9)
    aaloo=oico((.15*s,.12*s,H+.07*s),.075*s,M('#E8B84A',.45),e,sc=(1,1,.85),sub=2)
    plums=[oico((r.uniform(-.3,.3)*s,r.uniform(-.2,.2)*s,H+.06*s),.025*s,M('#3A1A22',.4),e,sub=1) for k in range(4)]
    bones=[ocyl((r.uniform(-.25,.25)*s,r.uniform(-.15,.15)*s,H+.02*s),.016*s,.14*s,M('#F4EEE0',.5),e,rot=(0,R(90),r.uniform(0,3)),seg=6) for k in range(3)]
    for b in bones: b.scale=(0,0,0)
    def setk(st):
        vis={'full':(1,1,1,1,1,0),'grab':(1,0,1,1,1,0),'noaaloo':(1,0,1,1,0,0),'empty':(0,0,0,0,0,1)}[st]
        for o in rice: o.scale=o.scale if vis[0] else (0,0,0)
        if not vis[0]: mound.scale=(0,0,0)
        for o,v in ((big,vis[1]),(ch2,vis[2]),(ch3,vis[3]),(aaloo,vis[4])): o.scale=(1,1,1) if v else (0,0,0)
        for p in plums: p.scale=(1,1,1) if vis[0] else (0,0,0)
        for b in bones: b.scale=(1,1,1) if vis[5] else (0,0,0)
    def lidk(k): hinge.rotation_euler=(R(-118*k),0,0)
    return dict(root=e,setk=setk,lid=lidk,big=big,aaloo=aaloo,top=H)
def plate_spoon(e,s=1.0):
    ocyl((0,-.12,.05),.2*s,.025,M('#F8F6F0',.25,spec=.8),e,rot=(R(90),0,0),seg=20); ocyl((0,-.14,.05),.15*s,.01,M('#E6E2D8',.3),e,rot=(R(90),0,0),seg=20)
    obox((.16,-.1,.2),(.012,.012,.16),M('#C9CED8',.25,metal=.9),.005,e); oico((.16,-.1,.38),.035,M('#C9CED8',.25,metal=.9),e,sc=(1,.5,1.4),sub=1)
# ------------------------------------------------------------------ SET A: chai dhaba (golden hour)
TC=(0,.45)                                       # table centre
SEATS_A={'al':(-1.95,.45),'wa':(-.92,1.55),'zo':(.92,1.55),'ay':(1.95,.45)}
def seat_rz(p,c=TC): return face_dir(c[0]-p[0],c[1]-p[1])
def dhaba_k():
    r=random.Random(31); ch=M('#C9CED8',.3,metal=.85); wd=M('#6E4A2E',.6,kind='wood',sc=.6)
    B.box((0,0,-.05),(30,20,.05),M('#9A938A',.9,kind='concrete',sc=.5),0)
    B.box((0,-.5,.006),(8,4.5,.006),M('#C8B89A',.8,kind='tile',h2='#B8A888',sc=1.6),0)
    B.box((0,-8.5,-.03),(30,3.2,.03),M('#3A3C44',.85,kind='asphalt'),0)
    # shop building (open front) + neighbours
    facade(0,11,2,'#E8D8B8','',"#2B6A4A",11,side=1,Y=4.0,trim='#F4EBDA',shop=False)
    facade(-10.5,9,3,'#BFD3D6','KARACHI MOBILE ZONE','#2B58C9',12,side=1,Y=4.4)
    facade(10.5,9,2,'#E6C8B0','SAEED GENERAL STORE','#C8372D',13,side=1,Y=4.4)
    # interior back wall: shelves, kettles, stove, sign
    B.box((0,7.6,1.7),(5.2,.1,1.7),M('#3F6E5A',.8,kind='wall'),0)
    for z in (1.55,2.25):
        B.box((-2.6,7.35,z),(2.2,.22,.03),wd,.01)
        for k in range(10): B.cyl((-4.5+k*.42,7.35,z+.14),.08,.24,M(r.choice(['#F4E8C8','#E8D0A0','#D8B878']),.3,spec=.8,alpha=.85),seg=10)
    B.box((2.6,6.8,.5),(2.2,.6,.5),M('#5A5E66',.6,metal=.4),.02); B.box((2.6,6.8,1.02),(2.25,.65,.03),M('#C9CED8',.3,metal=.8),.01)
    for k,x in enumerate((1.3,2.4,3.5)):
        B.cyl((x,6.8,1.25),.3,.42,M('#B8732E',.3,metal=.8),seg=16,r2=.22); B.cyl((x,6.8,1.5),.08,.12,M('#B8732E',.3,metal=.8),seg=10)
        B.box((x+.32,6.8,1.3),(.18,.03,.03),M('#B8732E',.3,metal=.8),.01,rot=(0,R(-30),0))
        for j in range(4): B.ico((x+math.cos(j*1.6)*.15,6.8+math.sin(j*1.6)*.15,1.06),.07,M('#2A6AFF',.2,emit=5),sc=(1,1,1.5),sub=1)
    for k in range(8): B.cyl((1.0+k*.45,6.35,1.1),.06,.13,M('#F4F1EA',.4),seg=10)
    B.box((0,4.12,3.55),(4.6,.08,.5),M('#1E6A3A',.5),.04); B.box((0,4.04,3.55),(4.45,.02,.42),M('#F4F1EA',.6),0)
    stext('QUETTA CAFE',(0,3.98,3.72),.42,'#1E6A3A'); stext('CHAI  •  PARATHA  •  BUN KABAB',(0,3.98,3.32),.18,'#C8372D')
    # tin awning on poles
    for k in range(13):
        B.box((-6+k*1.0,1.2,3.75),(.5,2.9,.02),M('#2E7A4A' if k%2 else '#E8E4DA',.6,metal=.3),.0,rot=(R(-7),0,0))
    for x in (-5.9,-2,2,5.9): B.cyl((x,-1.6,1.8),.06,3.6,ch,seg=8)
    B.box((0,-1.65,3.45),(6.1,.08,.08),ch,.01)
    for x in (-3.5,0,3.5): B.cyl((x,1.0,3.35),.006,.5,M('#16171C',.5),seg=4); B.ico((x,1.0,3.08),.1,M('#FFD98A',.2,emit=10),sub=1)
    # hero table (steel top) with cups
    B.box((TC[0],TC[1],1.0),(1.05,.55,.03),M('#C9CED8',.25,metal=.8),.02)
    for sx in (-.8,.8):
        for sy in (-.42,.42): B.cyl((TC[0]+sx,TC[1]+sy,.5),.03,1.0,ch,seg=6)
    for dx,dy in ((-.55,.25),(-.2,.38),(.2,.38),(.55,.25)): B.cyl((TC[0]+dx,TC[1]+dy,1.1),.075,.15,M('#F4F1EA',.35),seg=12); B.cyl((TC[0]+dx,TC[1]+dy,1.16),.065,.02,M('#C58A4A',.4),seg=12)
    B.cyl((TC[0],TC[1]-.05,1.09),.22,.04,M('#E8C070',.6),seg=16); B.cyl((TC[0],TC[1]-.05,1.12),.18,.02,M('#B8732E',.5),seg=16)
    cols={'al':'#2B58C9','wa':'#C8372D','zo':'#C8372D','ay':'#2B58C9'}
    for k,p in SEATS_A.items(): pchair(p[0],p[1],seat_rz(p),cols[k])
    # other customers' tables + chairs
    BG=[]
    for tx,ty in ((-4.6,1.6),(4.6,1.9),(-4.4,-2.4)):
        B.box((tx,ty,1.0),(.7,.45,.03),M('#C9CED8',.25,metal=.8),.02)
        for sx in (-.55,.55):
            for sy in (-.33,.33): B.cyl((tx+sx,ty+sy,.5),.03,1.0,ch,seg=6)
        B.cyl((tx-.2,ty,1.09),.07,.14,M('#F4F1EA',.35),seg=10); B.cyl((tx+.25,ty+.1,1.09),.07,.14,M('#F4F1EA',.35),seg=10)
        for sx in (-1,1): pchair(tx+sx*1.15,ty,-90*sx,r.choice(['#C8372D','#2B58C9','#F2C14E'])); BG.append((tx+sx*1.15,ty,-90*sx))
    # street side: palms, minibus, bikes, wires
    palm(-9,-4.6,1.0,1); palm(8.5,-4.9,1.1,2); palm(14,-5,1.0,3)
    minibus((-14,-7.6,0),0,5)
    for x in (6.6,7.5): mb=motorbike((x,-2.9,0),90,r.choice(['#C8372D','#16171C'])); mb['root'].scale=(1.4,)*3
    wires(-16,16,3.9,3.9,6.2,4,7)
    for k in range(4): bush(-7.2+k*.8,3.7,.6,'#3F7A3A') if k%2 else None
    B.done('dhaba')
    setup_world('golden',60)
    point((0,-1.0,3.0),180,(1,.85,.6),r=1.2,shadow=False); point((0,5.5,2.8),160,(1,.8,.55),r=.8,shadow=False); point((0,-6,4),350,(1,.75,.5),r=3,shadow=False)
    return dict(bg=BG)
# ------------------------------------------------------------------ SET B: Burns Road style food street (dusk)
SIGNS=['KARACHI BIRYANI CENTRE','NIHARI HOUSE','RABRI & DOODH','BUN KABAB CORNER','HALEEM KING','FRY FISH','KHEER & FALOODA','SAJJI POINT','KULFI WALA','DESI GHEE PARATHA']
SCOL=['#C8372D','#1E6A3A','#2B58C9','#D9811A','#7A1F2E','#16171C','#B8456A','#35975A','#2B6A8A','#8A4A1E']
def street_k(fx_=0.0):
    r=random.Random(77); em=4.0
    B.box((0,0,-.05),(70,12,.05),M('#4A4C54',.85,kind='asphalt'),0)
    for s in (1,-1): B.box((0,s*3.9,.06),(70,.55,.06),M('#B8A890',.85,kind='tile'),0); B.box((0,s*3.33,.08),(70,.06,.08),M('#F2C14E',.6),0)
    i=0
    for s in (1,-1):
        x=-62
        while x<62:
            w=r.uniform(6.5,9); facade(x+w/2,w,r.randint(2,4),r.choice(['#E8D8B8','#D8C4A0','#C9D6D8','#E6C8B0','#D8B890','#E0D0C0']),SIGNS[i%len(SIGNS)],SCOL[i%len(SCOL)],100+i,side=s,Y=4.45,trim='#F4EBDA'); x+=w+.05; i+=1
    # degs, stalls and street tables in front of the shops (north side), facing the street
    for k,x in enumerate(range(-54,58,9)):
        deg(x+r.uniform(-1,1),3.8,1.0,lid=(k%3==1)); B.box((x+1.6,3.85,.5),(.6,.35,.5),M('#8A5A36',.6,kind='wood',sc=.6),.03); B.box((x+1.6,3.85,1.02),(.65,.4,.03),M('#C9CED8',.3,metal=.8),.01)
    for k,x in enumerate(range(-50,55,12)):
        stool(x+4,-3.8,r.choice(['#C8372D','#2B58C9'])); stool(x+5.2,-3.85,r.choice(['#C8372D','#F2C14E']))
    # overhead light strings + banner
    cols=['#FF4F7A','#FFD23F','#35C8FF','#7CFC9A','#FF8A3A','#FFF3D0']
    for x in range(-56,57,7): bulb_string((x,4.4,6.4),(x+3.5,-4.4,6.4),16,.9,cols,em*1.3)
    for x in (18,-26):
        for sy in (-1,1): B.cyl((x,sy*3.5,3.4),.08,6.8,M('#2A2C34',.4,metal=.5),seg=8)
        B.box((x,0,6.1),(.06,3.6,.55),M('#C8372D',.6),.03); B.box((x-.07,0,6.1),(.01,3.45,.45),M('#F2C14E',.6),0)
        stext('BURNS ROAD FOOD STREET',(x-.09,0,6.1),.36,'#7A1F1F',n=(-1,0,0)); stext('BURNS ROAD FOOD STREET',(x+.07,0,6.1),.36,'#7A1F1F',n=(1,0,0))
    for x in range(-60,61,15):
        for s in (1,-1): B.cyl((x,s*3.5,3.6),.08,7.2,M('#2A2C34',.4,metal=.5),seg=8); B.box((x,s*3.1,7.1),(.06,.45,.05),M('#2A2C34',.4),.01); B.ico((x,s*2.7,7.0),.18,M('#FFE0A0',.3,emit=em),sub=1)
    wires(-62,62,4.3,-4.3,7.6,6,9)
    B.done('street')
    setup_world('dusk',70)
    for dx in (-14,-5,4,13): point((fx_+dx,0,5.8),500,(1,.82,.6),r=.6,shadow=(dx in (-5,4)))
    point((fx_,2.8,2.0),260,(1,.6,.35),r=1.5,shadow=False)
    bikes=[]
    for x in (-37,-21,-8,3.5,15,31,46):
        mb=motorbike((x,-3.55,0),r.choice([82,98]),r.choice(['#C8372D','#16171C','#2B58C9'])); mb['root'].scale=(1.4,)*3
    rk=rickshaw((-15,-2.9,0),0,'#2E8A3A'); rk['root'].scale=(VSC,)*3; rk2=rickshaw((24,-2.9,0),180,'#2B58C9'); rk2['root'].scale=(VSC,)*3
    return {}
# ------------------------------------------------------------------ SET C: night lawn + colonial hall
SEATS_C={'wa':(-.92,1.55,0),'zo':(.92,1.55,0),'al':(-2.05,.35,None),'ay':(2.05,.35,None)}
BX=(0,.35)                                        # crate with the biryani box
RIDER_Y=6.3
def hall(y0=24):
    st=M('#D9B88A',.8,kind='wall',sc=.8); st2=M('#C9A273',.8,kind='wall'); rf=M('#7A4A3A',.7); dk=M('#2A2018',.4); gl=M('#FFD9A0',.3,emit=1.4)
    B.box((0,y0+4,4.5),(13,4,4.5),st,0); B.box((0,y0-.05,9.15),(13.2,.25,.25),st2,.02)
    for k in range(13):
        x=-12+k*2.0
        for z,h in ((2.3,1.3),(6.4,1.2)):
            B.box((x,y0-.02,z),(.45,.05,h),dk,0); B.box((x,y0-.06,z),(.32,.03,h-.12),gl,0)
            B.box((x,y0-.06,z+h+.05),(.32,.03,.32),gl,0,rot=(0,R(45),0)); B.box((x,y0-.09,z+h+.42),(.55,.06,.12),st2,.02)
        B.box((x+1.0,y0-.15,4.5),(.16,.15,4.5),st2,.02)
    B.box((0,y0-1.2,1.6),(3.2,1.2,1.6),st2,.02)
    for x in (-2.2,0,2.2): B.box((x,y0-2.42,1.2),(.6,.05,1.0),dk,0); B.box((x,y0-2.45,2.25),(.45,.03,.45),dk,0,rot=(0,R(45),0))
    B.box((0,y0+2,14),(2.4,2.4,5.0),st,0)
    for z in (11.5,14.5,17.2):
        for s in (-1,1): B.box((s*0,y0-.42,z),(.5,.05,.9),dk,0); B.box((0,y0-.45,z),(.38,.03,.78),gl,0)
    B.box((0,y0-.45,18.4),(1.0,.08,1.0),M('#F4F1EA',.3,emit=1.0),.05); B.box((0,y0-.53,18.4),(.03,.02,.6),dk,0); B.box((.2,y0-.53,18.55),(.03,.02,.35),dk,0,rot=(0,R(50),0))
    B.cyl((0,y0+2,21.0),2.6,4.0,rf,seg=4,r2=.05,rot=(0,0,R(45)))
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((sx*2.3,y0+2+sy*2.3,20.0),.25,2.0,st2,seg=8,r2=.05)
    for x in (-13,13): B.box((x,y0+4,10.0),(1.0,4.0,1.0),st2,0); B.cyl((x,y0+4,11.8),1.0,2.6,rf,seg=4,r2=.05,rot=(0,0,R(45)))
    for k in range(-12,13,2): B.box((k,y0-.1,9.6),(.35,.12,.3),st2,.02)
def lawn_k(fx_=0.0):
    r=random.Random(55); grass=M('#3F7A3A',.9,kind='leaves',h2='#356E34',sc=3)
    B.box((0,0,-.05),(80,60,.05),grass,0)
    B.box((0,RIDER_Y,.02),(80,1.2,.03),M('#A89880',.85,kind='tile',h2='#988870',sc=2.0),0)        # park path (rider)
    B.box((0,8.9,.02),(80,.9,.03),M('#A89880',.85,kind='tile'),0)                                   # footpath (walkers)
    B.box((0,22.5,.02),(9,1.5,.03),M('#C8B89A',.85,kind='tile'),0)
    hall(24)
    for x,s in ((-16,1.1),(-9,1.0),(9.5,1.05),(17,1.15),(-24,1.0),(25,1.0),(-32,1.1),(33,1.0)): palm(x,14+r.uniform(-1,1),s,int(x*3))
    for x in range(-30,31,5): bush(x+r.uniform(-1,1),11.2,r.uniform(.7,1.0),r.choice(['#3F7A3A','#356E38','#4F8A3A']))
    for x in range(-28,29,4):
        for k in range(5): B.ico((x+k*.3-.6,12.4+r.uniform(-.1,.1),.18),.12,M(r.choice(['#E8554D','#F2C14E','#F28AA0','#F4F1EA']),.6,emit=.15),sub=1)
    for x in range(-36,37,9):
        B.cyl((x,7.3,2.4),.07,4.8,M('#1E2A24',.4,metal=.5),seg=8); B.ico((x,7.3,4.95),.25,M('#FFE6B0',.3,emit=6),sub=1); B.cyl((x,7.3,5.2),.3,.1,M('#1E2A24',.4),seg=10)
    for x in (-11,-5.5,5.5,11):                                                                            # benches by the footpath
        B.box((x,9.95,.6),(1.1,.3,.05),M('#6A4628',.6,kind='wood'),.02); B.box((x,10.25,1.0),(1.1,.05,.3),M('#6A4628',.6,kind='wood'),.02)
        for sx in (-.9,.9): B.box((x+sx,9.95,.3),(.06,.28,.3),M('#2A2C34',.4),.01)
    # city behind the hall
    for k in range(22):
        x=-90+k*8.5+r.uniform(-1,1); h=r.uniform(10,26); B.box((x,62,h/2),(3.6,3,h/2),M(r.choice(['#5A6070','#6A6A78','#4A5060']),.8),0)
        for j in range(int(h/2.6)):
            for q in (-1.7,0,1.7):
                if r.random()<.6: B.box((x+q,58.95,2.2+j*2.5),(.45,.04,.55),M('#FFE0A0',.2,emit=r.choice([1.5,2.5,3.5])),0)
    # picnic: charpai, stools, crate; other groups on durries
    charpai(0,1.55,0); stool(-2.05,.35,'#2B58C9'); stool(2.05,.35,'#C8372D')
    B.box((BX[0],BX[1],.38),(.5,.36,.38),M('#9A6A3A',.7,kind='wood',sc=.5),.03)
    for k in range(4): B.box((BX[0],BX[1]-.37,.12+k*.2),(.5,.01,.05),M('#7A4E2A',.6),0)
    for gx,gy,c in ((-8.5,3.2,'#B8456A'),(8.0,3.6,'#2B58C9'),(-15,-1.5,'#D9811A')):
        B.box((gx,gy,.02),(1.6,1.1,.012),M(c,.85,kind='fabric'),0)
        for k in range(6): B.box((gx-1.5+k*.6,gy,.035),(.1,1.05,.004),M('#F4F1EA',.85),0)
        B.cyl((gx,gy,.12),.25,.22,M('#C9CED8',.3,metal=.8),seg=14)
    B.done('lawn')
    setup_world('night',70)
    point((0,14,9),3500,(1,.78,.5),r=2,shadow=False); point((-10,16,3),1200,(1,.75,.45),r=1,shadow=False); point((10,16,3),1200,(1,.75,.45),r=1,shadow=False)
    point((fx_-3,-2.5,4.2),700,(1,.85,.65),r=1.2,shadow=True); point((fx_+3.5,3.5,3.8),350,(.8,.85,1.0),r=1.5,shadow=False); point((0,-5,3),500,(1,.9,.75),r=2.5,shadow=False)
    return {}
# ------------------------------------------------------------------ delivery rider (moving)
def rider_bike(C):
    mb=motorbike((0,0,0),180,'#16171C'); mb['root'].scale=(1.4,)*3
    bx=obox((-.95,0,1.35),(.32,.3,.28),M('#E86A1A',.5),.04,mb['root']); obox((-.95,-.305,1.38),(.26,.005,.2),M('#F4F1EA',.6),0,mb['root'])
    stext('BIRYANI',(-.95,-.315,1.45),.075,'#C8372D',parent=mb['root']); stext('EXPRESS',(-.95,-.315,1.33),.065,'#C8372D',parent=mb['root'])
    H=mk(C,0,0,90,'rider')
    return mb,H
