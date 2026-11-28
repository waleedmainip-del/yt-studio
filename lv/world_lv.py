# Worlds for the Lahore vampire-prince film. All new sets:
#   gali()     old-city Lahore lane at night: brick havelis, jharokas, fairy lights, chai stall, domes + minarets at the east end, hero house door at (0,3.2), hero roof at z 10.7
#   baithak()  Khala's drawing room      qila() castle hall (Transylvania)      qila_ext() castle gate in the snow      plaza() old European square (hook)
MOODS['lv_night']=dict(sun=(55,-30),e=.9,col=(.62,.70,1.0),top='#070620',bot='#3A2760',sky=.95,mist='#22183E',cloud='#35275E',cov=.36,cstr=.5)
MOODS['lv_storm']=dict(MOODS['lv_night'],top='#14061E',bot='#5A2A7A',cloud='#7A4A9A',cov=.12,cstr=.9)
MOODS['lv_in']=dict(sun=(60,-160),e=.25,col=(1,.9,.8),top='#17120F',bot='#1E1814',sky=.5,mist='#1A1410',cloud='#1E1814',cov=.3,cstr=.5)
MOODS['lv_snow']=dict(sun=(50,-35),e=1.0,col=(.66,.76,1.0),top='#060A22',bot='#2A3A6E',sky=.95,mist='#1A2248',cloud='#2A3468',cov=.3,cstr=.5)
BRK=['#9A4A32','#B0603C','#8A3E2A','#C9A27A','#D9C9A8','#7C93A8','#C86A4A','#A8553A']; DOORC=['#1F7A7A','#2E6B3A','#2B58C9','#7A2A1A','#C9A24A']; JH=[]; RZ=10.7
BULB=['#FF5A5A','#FFD23A','#5AFF8A','#5AB8FF','#FF7AD8']
def haveli(cx,side,w,seed,hero=False):
    """old-city house front. side=+1: north of the lane, front at y=3.2 facing -y. w = half width"""
    r=random.Random(seed); s=side; fy=s*3.2; bc=M(BRK[seed%8],.9,kind='wall'); wd=M(r.choice(['#5A3A22','#6B4A2E','#4A2E1A']),.6,kind='wood',sc=.5); h=10.2 if hero else r.choice([9.0,10.2,11.4]); cr=M('#E8DCC0',.8)
    cy=fy+s*4.0
    if hero:      # real doorway: a hall recess x -1.04..1.04, 2.4 m deep, 2.9 m high
        for e_ in (-1,1): B.box((cx+e_*(w+1.04)/2,cy,h/2),((w-1.04)/2,4.0,h/2),bc,0)
        B.box((cx,cy,(h+2.9)/2),(1.04,4.0,(h-2.9)/2),bc,0); B.box((cx,fy+s*5.2,1.45),(1.04,2.8,1.45),bc,0)
    else: B.box((cx,cy,h/2),(w,4.0,h/2),bc,0)
    B.box((cx,cy,h+.25),(w+.12,4.12,.25),cr,0)
    for k in range(int(w*2/.8)): B.box((cx-w+.4+k*.8,fy+s*.15,h+.75),(.22,.15,.25),cr,0)
    B.box((cx,fy-s*.45,.16),(w-.15,.45,.16),M('#8A7A68',.9,kind='concrete',sc=.4),.02)
    dc=M(DOORC[seed%5],.6,kind='wood',sc=.5)
    if not hero:
        dx=cx-w*.35; B.box((dx,fy-s*.02,1.5),(.72,.06,1.2),dc,.02); B.cyl((dx,fy-s*.02,2.7),.72,.12,dc,rot=(R(90),0,0),seg=14); B.box((dx,fy-s*.09,1.5),(.02,.01,1.15),M('#16171C',.5),0)
        sx=cx+w*.45; B.box((sx,fy-s*.03,1.55),(w*.36,.04,1.2),M(r.choice(['#7A8A9A','#8A9A7A','#9A8A7A','#6A7A8A']),.5,metal=.5),0)
        for q in range(7): B.box((sx,fy-s*.08,.55+q*.33),(w*.36,.012,.02),M('#4A5560',.5,metal=.5),0)
        if r.random()<.5: B.box((sx,fy-s*.55,2.95),(w*.42,.55,.04),M(r.choice(['#B8232E','#1F7A7A','#E6B93A','#2E6B3A']),.8,kind='fabric'),0,rot=(R(-s*14),0,0))
    jx=cx+(0 if hero else r.uniform(-.6,.6)); jz=4.7; jw=min(1.9,w*.55); on=hero or r.random()<.6; gl=lit('#FFC36A',3.2 if on else .12)
    B.box((jx,fy-s*.45,jz),(jw,.45,1.05),wd,.03); B.box((jx,fy-s*.5,jz+1.2),(jw+.2,.6,.09),wd,.02,rot=(R(-s*10),0,0)); B.box((jx,fy-s*.45,jz-1.15),(jw+.08,.5,.1),wd,.02)
    for q in (-1,0,1):
        B.box((jx+q*jw*.62,fy-s*.91,jz+.05),(jw*.24,.012,.6),gl,0); B.cyl((jx+q*jw*.62,fy-s*.905,jz+.65),jw*.24,.03,gl,rot=(R(90),0,0),seg=10)
        for z_ in (-.25,.15): B.box((jx+q*jw*.62,fy-s*.925,jz+z_),(jw*.24,.01,.02),wd,0)
    JH.append((jx,fy-s*.93,jz+.1,jw*.9,side,on))
    for q in (-1,1):
        wx=cx+q*w*.5; on2=r.random()<.45
        B.box((wx,fy-s*.02,7.7),(.5,.03,.75),lit('#FFD890',2.4) if on2 else M('#1A1E2A',.3),0); B.box((wx,fy-s*.12,6.87),(.8,.14,.05),cr,0)
        for e_ in (-1,1): B.box((wx+e_*.7,fy-s*.05,7.7),(.19,.03,.77),M(DOORC[(seed+q)%5],.6),0)
    if r.random()<.6: B.cyl((cx+r.uniform(-w*.4,w*.4),cy+s*1.5,h+1.25),.7,1.3,M(r.choice(['#2B58C9','#16171C','#E8E2D0']),.6),seg=10)
    return h
def mbike(x,y,rz=0,col='#B8232E'):
    c=math.cos(R(rz)); s_=math.sin(R(rz)); bk=M('#16171C',.5); P=lambda dx,dz:(x+dx*c,y+dx*s_,dz)
    for dx in (-.62,.62): B.cyl(P(dx,.32),.32,.1,bk,rot=(R(90),0,R(rz)),seg=12)
    B.box(P(0,.62),(.5,.13,.14),M(col,.4),.05,rot=(0,0,R(rz))); B.box(P(-.22,.84),(.34,.15,.07),bk,.03,rot=(0,0,R(rz))); B.box(P(.5,.95),(.04,.3,.03),M('#C9CED8',.3,metal=.8),0,rot=(0,0,R(rz))); B.box(P(.6,.74),(.06,.07,.09),lit('#FFF0C0',1.0),0,rot=(0,0,R(rz)))
def gali(mood='lv_night',posters=False,night=1.0,stall=True):
    """lane along x, y -3.2..3.2. hero house north at x -4.2..4.2, carved double door at (0,3.2) (returns its leaves dl, dr: rotate z +/-100 to open inward). hero roof top at z RZ, y 3.2..11.2"""
    NIGHT[0]=night; S=setup_world(mood,shadow=60); r=random.Random(21); JH.clear()
    B.box((0,0,-.1),(260,260,.1),M('#2E2824',.95),0); B.box((0,0,-.02),(95,3.25,.05),M('#6A5648',.92,kind='tile',sc=.35),0); B.box((0,0,.031),(95,.16,.006),M('#3A322C',.9),0)
    def row(side,x0,x1,seed):
        x=x0; i=0
        while x<x1-1.5:
            w=r.choice([2.6,3.0,3.4,3.9])
            if x+2*w>x1-1.5: w=(x1-x)/2
            haveli(x+w,side,w,seed+i); x+=2*w; i+=1
    row(1,-64,-4.2,100); row(1,4.2,64,200); row(-1,-64,64,300); haveli(0,1,4.2,7,hero=True)
    # hero door: carved frame, two leaves on hinges, warm hall behind
    wd=M('#5A3A22',.55,kind='wood',sc=.4); gd=M('#C9A24A',.3,metal=.8); fr=M('#E8DCC0',.8)
    for sx in (-1,1): B.box((sx*1.2,3.12,1.5),(.16,.1,1.5),fr,.02)
    B.box((0,3.12,3.0),(1.36,.1,.2),fr,.02); hw_=M('#C4A476',.85,kind='wall')
    B.box((0,4.4,.16),(1.04,1.2,.16),M('#8A7A68',.9,kind='concrete',sc=.4),0); B.box((0,4.3,.33),(.7,1.0,.01),M('#7A2A1A',.8,kind='fabric'),0)
    for sx in (-1,1): B.box((sx*1.035,4.4,1.6),(.006,1.2,1.3),hw_,0)
    B.box((0,5.595,1.6),(1.04,.006,1.3),hw_,0); B.box((0,4.4,2.895),(1.04,1.2,.006),M('#A89C84',.9),0)
    B.box((0,5.57,1.95),(.36,.02,.46),gd,.01); B.box((0,5.55,1.95),(.3,.01,.4),M('#8FB8D8',.7),0); B.ico((0,5.54,1.98),.15,M('#D8A277',.7),sc=(1,.08,1),sub=1)
    B.box((.78,5.5,2.25),(.08,.08,.14),lit('#FFD9A0',1.6,always=True),.02); point((0,4.5,2.5),26*night,(1,.8,.55),r=.4,shadow=False)
    L=[]
    for sx in (-1,1):
        e=empty((sx*1.04,3.2,0)); obox((-sx*.52,0,1.4),(.52,.05,1.4),wd,.02,e)
        for q in range(4):
            for q2 in range(2): oico((-sx*(.26+q2*.5),-.06,.5+q*.6),.045,gd,e,sub=1)
        obox((-sx*.95,-.07,1.4),(.03,.03,.14),gd,.01,e); L.append(e)
    sign('NASREEN MANZIL',(2.35,3.13,2.0),.11,'#3A2A1E','#E8DCC0',n=(0,-1,0),pad=.08,th=.03,frame='#6B4A2E')
    for sx in (-1,1): B.box((sx*1.7,3.02,2.75),(.11,.11,.18),lit('#FFC36A',2.2),.03); B.box((sx*1.7,3.02,2.98),(.14,.14,.04),M('#2A2C34',.5,metal=.5),0)
    point((0,1.6,2.9),150*night,(1,.78,.5),r=.5,shadow=False)
    for k in range(-5,6):
        if k==0: continue
        x=k*11.0+3; s=1 if k%2 else -1; B.box((x,s*3.02,3.4),(.11,.11,.18),lit('#FFC36A',2.4),.03); point((x,s*1.8,3.3),190*night,(1,.78,.5),r=.5,shadow=False)
    # fairy lights zig-zag + wires
    wr=M('#1A1A1E',.6)
    for i,x in enumerate(range(-44,45,4)):
        a=(x,-3.15,6.3+.4*(i%3)); b=(x+2.2,3.15,6.9-.3*(i%2))
        for q in range(10):
            f=q/9.; sag=.55*math.sin(f*math.pi); B.ico((a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f,a[2]+(b[2]-a[2])*f-sag),.075,M(BULB[(q+i)%5],.3,emit=6.0),sub=1)
    for z_ in (5.9,6.05): B.box((0,3.02,z_),(64,.012,.012),wr,0); B.box((0,-3.02,z_+.5),(64,.012,.012),wr,0)
    # chai stall (north side, x -14): counter, awning, kettle, cups, stools
    if stall:
        cw=M('#2E6B3A',.6,kind='wood',sc=.5); B.box((-14,2.3,.5),(1.3,.4,.5),cw,.02); B.box((-14,2.3,1.03),(1.4,.48,.04),M('#C9CED8',.4,metal=.6),.01); B.box((-14,1.9,2.6),(1.6,.9,.04),M('#B8232E',.8,kind='fabric'),0,rot=(R(-12),0,0))
        B.cyl((-14.5,2.3,1.22),.17,.3,M('#C9CED8',.3,metal=.8),seg=10); B.cyl((-14.5,2.3,1.42),.06,.1,M('#16171C',.5),seg=8); B.box((-13.4,2.3,1.1),(.3,.2,.03),M('#F4F1EA',.5),0)
        for q in range(4): B.cyl((-13.6+q*.14,2.25,1.17),.04,.09,M('#F4F1EA',.4),seg=8)
        point((-14,1.4,2.2),150*night,(1,.8,.5),r=.4,shadow=False); steam((-14.5,2.3,1.5),0,400,n=5,seed=3,size=.07)
        for q in (-1,1): B.cyl((-14+q*2.2,.9,.24),.2,.48,M('#7A5A3A',.7,kind='wood'),seg=8)
    mbike(11.5,-2.5,8); mbike(-22,-2.45,-6,'#2B58C9'); mbike(27,2.4,188,'#16171C')
    for k in range(18):
        x=r.uniform(-58,58); s=r.choice((-1,1))
        if abs(x)<5.2 and s>0: continue
        if s<0 and abs(x)<36: continue
        if stall and -17<x<-11 and s>0: continue
        B.cyl((x,s*2.75,.52),.2,.4,M('#B8674A',.8),seg=8,r2=.26); B.ico((x,s*2.75,.95),.32,M(r.choice(['#2F6A3A','#3A7A3A','#D83A8A']),.85,kind='leaves'),sub=1)
    if posters:
        k=0
        for x in [q*1.45 for q in range(-12,13)]:
            if abs(x)<2.9: continue
            poster(x,3.19,1.95+.12*(k%2),n=(0,-1,0),s=.95,seed=k,txt=False); k+=1
        for x in [q*1.45+.7 for q in range(-12,12)]: poster(x,-3.19,2.0+.12*(k%2),n=(0,1,0),s=.95,seed=k,txt=False); k+=1
    # hero roof: stair tower with a poster wall, water tank, charpai, clothes line, kite
    wl=M(BRK[7],.9,kind='wall'); B.box((2.7,9.2,RZ+1.25),(1.3,1.3,1.25),wl,0); B.box((2.7,9.2,RZ+2.58),(1.45,1.45,.08),M('#E8DCC0',.8),0); B.box((1.38,9.2,RZ+1.0),(.03,.5,1.0),M('#1F7A7A',.6,kind='wood'),0)
    B.cyl((-2.8,9.6,RZ+.75),.75,1.5,M('#2B58C9',.6),seg=12); B.cyl((-2.8,9.6,RZ+1.53),.78,.08,M('#1F3F9A',.6),seg=12)
    for sy in (4.0,8.2): B.cyl((-3.7,sy,RZ+1.1),.04,2.2,M('#3A3D44',.5),seg=6)
    B.box((-3.7,6.1,RZ+2.1),(.008,2.1,.008),M('#F4F1EA',.6),0)
    for q,c in enumerate(('#D83A8A','#F2C14E','#0F8A64')): B.box((-3.7,4.7+q*1.3,RZ+1.7),(.01,.4,.4),M(c,.85,kind='fabric'),0)
    poster(2.0,7.89,RZ+1.55,n=(0,-1,0),s=1.0,seed=1)
    for s_ in (-1,1): B.box((0,3.75+4.0+s_*3.9,RZ+.45),(4.2,.1,.45),wl,0) if s_>0 else None
    for sx in (-1,1): B.box((sx*4.12,7.2,RZ+.45),(.1,4.0,.45),wl,0)
    # skyline at the east end of the lane: domes + minarets, big moon; city gate at the west end
    ms=M('#8A3E2A',.9,kind='wall'); mw=M('#E8E2D0',.6,emit=.22)
    B.box((92,0,7),(8,26,7),ms,0); B.ico((92,0,19),7.5,mw,sc=(1,1,1.18),sub=3)
    for sy in (-1,1): B.ico((92,sy*13,16.5),4.6,mw,sc=(1,1,1.18),sub=3); B.cyl((90,sy*24,16),1.5,32,ms,seg=10,r2=1.1); B.ico((90,sy*24,33.2),1.9,mw,sub=2)
    point((80,0,14),4500*night,(.8,.85,1.0),r=4,shadow=False)
    B.box((-67,-4.6,5),(1.6,1.4,5),ms,0); B.box((-67,4.6,5),(1.6,1.4,5),ms,0); B.box((-67,0,8.6),(1.6,3.3,1.4),ms,0); B.cyl((-67,0,7.2),3.2,3.2,M('#2E2824',.95),rot=(0,R(90),0),seg=18)
    for k in range(40):
        x=r.uniform(-90,80); y=r.choice((-1,1))*r.uniform(13,60); w=r.uniform(3,5.5); h=r.uniform(8,14); B.box((x,y,h/2),(w,w,h/2),M(BRK[k%8],.9,kind='wall'),0)
        if r.random()<.5: B.box((x,y-(1 if y>0 else -1)*(w+.02),h*.7),(.6,.02,.6),lit('#FFD890',2.4),0)
    for k in range(150): a=r.uniform(0,6.283); el=r.uniform(.12,1.25); d=430; B.ico((d*math.cos(a)*math.cos(el),d*math.sin(a)*math.cos(el),d*math.sin(el)),r.uniform(.5,1.2),M('#FFFFFF',.3,emit=6.0),sub=1)
    B.ico((400,150,170),26,M('#FFF6D8',.3,emit=2.6),sub=3)
    B.done('gali'); return dict(dl=L[0],dr=L[1],S=S)
def door_open(G,k):
    G['dl'].rotation_euler[2]=R(88*k); G['dr'].rotation_euler[2]=R(-88*k)
# ---------------------------------------------------------------- drawing room
SOFA=(1.0,3.5,0); MD=(1.2,.9,0); CHA=(-1.7,1.1,80); CHW=(4.0,1.0,-62)      # sofa centre seat, aunty's armchair, Waleed's armchair (x,y,rz)
def armchair(x,y,rz,col,wd):
    e=empty((x,y,0),rot=(0,0,R(rz))); f=M(col,.85,kind='fabric')
    obox((0,-.12,.3),(.86,.5,.2),f,.06,e); obox((0,.5,.8),(.86,.12,.52),f,.08,e)
    for sx in (-1,1): obox((sx*1.0,-.1,.5),(.12,.56,.26),f,.06,e); obox((sx*1.0,-.12,.78),(.13,.58,.03),wd,.02,e)
    for sx in (-.8,.8):
        for sy in (-.5,.4): obox((sx,sy,.06),(.05,.05,.06),wd,.01,e)
    return e
W4=[False]
def baithak(night=True):
    """room x -5.2..5.2, back wall y 4.6, open to -y. 3-seat sofa on the back wall (centre seat SOFA), armchairs CHA (left) and CHW (right), tea table at (0.6,1.5), door in the right wall"""
    NIGHT[0]=1.0; S=setup_world('lv_in',shadow=30); r=random.Random(5); wl=M('#E8D8B8',.9,kind='wall'); wd=M('#5A3A22',.5,kind='wood',sc=.5); wd2=M('#7A5230',.5,kind='wood',sc=.5); gd=M('#C9A24A',.3,metal=.8)
    B.box((0,-3,-.1),(8,10,.1),M('#B8A890',.9,kind='tile',sc=.8),0); B.box((0,4.7,2.2),(5.4,.1,2.2),wl,0); B.box((0,4.58,.45),(5.3,.03,.45),M('#C9B48A',.85),0); B.box((0,4.56,.92),(5.3,.04,.03),wd,0)
    for sx in (-1,1): B.box((sx*5.3,-3,2.2),(.1,8,2.2),wl,0)
    B.box((0,-3,4.5),(5.5,8,.1),M('#B9AE98',.9),0)
    if W4[0]:      # fourth wall, only built for reverse angles
        B.box((0,-4.7,2.2),(5.4,.1,2.2),wl,0); B.box((0,-4.58,.45),(5.3,.03,.45),M('#C9B48A',.85),0); B.box((0,-4.56,.92),(5.3,.04,.03),wd,0)
        B.box((-1.6,-4.59,2.3),(1.1,.02,1.0),lit('#27306A',.9,always=True),0); B.box((-1.6,-4.5,3.75),(1.7,.1,.14),gd,.03)
        for q in (-1,1): B.box((-1.6+q*1.25,-4.5,2.2),(.3,.08,1.5),M('#8A1F3A',.85,kind='fabric'),.05)
        B.box((2.6,-4.3,.55),(1.2,.3,.55),wd,.02); B.cyl((2.2,-4.3,1.3),.14,.4,M('#1F7A7A',.4),seg=10); B.cyl((3.1,-4.3,1.2),.1,.2,gd,seg=8)
        for i,(x,z,c) in enumerate(((1.6,2.9,'#F2D0C0'),(2.8,3.0,'#C8E0B8'),(3.9,2.85,'#8FB8D8'))): B.box((x,-4.6,z),(.4,.03,.32),gd if i%2 else wd,.01); B.box((x,-4.57,z),(.34,.01,.26),M(c,.7),0)
    B.box((.6,1.6,.012),(3.4,2.4,.012),M('#8A1F2A',.9,kind='fabric'),0); B.box((.6,1.6,.02),(3.0,2.0,.012),M('#B8443A',.9,kind='fabric'),0); B.box((.6,1.6,.028),(1.6,1.0,.012),M('#E6C87A',.9,kind='fabric'),0)
    # sofa (3 seats) maroon velvet, carved wooden frame
    sf=M('#7A1F2E',.85,kind='fabric'); sx0=SOFA[0]
    B.box((sx0,3.6,.3),(1.75,.5,.2),sf,.06); B.box((sx0,4.12,.85),(1.75,.14,.6),sf,.08); B.box((sx0,4.2,1.5),(1.85,.06,.1),wd,.03); B.ico((sx0,4.2,1.66),.14,gd,sub=1)
    for e_ in (-1,1): B.box((sx0+e_*1.86,3.62,.52),(.12,.52,.3),sf,.06); B.box((sx0+e_*1.86,3.6,.84),(.13,.54,.03),wd,.02)
    for q in (-1,0,1): B.box((sx0+q*1.15,3.6,.51),(.54,.46,.035),M('#8A2A38',.85,kind='fabric'),.03)
    for e_ in (-1.6,1.6): B.box((sx0+e_,3.2,.06),(.06,.06,.06),wd,.01)
    for e_ in (-1,1): B.box((sx0+e_*1.3,3.85,.78),(.26,.1,.22),M('#E6B93A',.85,kind='fabric'),.08,rot=(R(-14),0,R(e_*10)))
    armchair(CHA[0],CHA[1],CHA[2],'#0F6A5A',wd); armchair(CHW[0],CHW[1],CHW[2],'#0F6A5A',wd)
    # tea table + tea set (in front of the sofa); the mooda (cane stool) in the middle of the room is the hot seat
    TX,TY=1.0,2.5
    B.box((TX,TY,.42),(.75,.42,.03),M('#BFD0D8',.15,spec=1.0,alpha=.55),.01); B.box((TX,TY,.2),(.7,.38,.02),wd2,.01)
    for sx in (-.65,.65):
        for sy in (-.34,.34): B.box((TX+sx,TY+sy,.21),(.035,.035,.21),wd,.01)
    B.cyl((TX-.25,TY+.05,.56),.1,.16,M('#F4F1EA',.3),seg=10); B.cyl((TX-.25,TY+.05,.66),.04,.05,gd,seg=8); B.box((TX+.32,TY-.05,.47),(.2,.14,.015),M('#F4F1EA',.4),.01)
    for q in range(5): B.box((TX+.2+q*.06,TY-.05,.5),(.022,.05,.012),M('#C98A4A',.8),.004)
    for q in range(3): B.cyl((TX-.5+q*.14,TY-.2,.5),.04,.07,M('#F4F1EA',.4),seg=8)
    B.cyl((MD[0],MD[1],.24),.42,.48,M('#C9A24A',.7,kind='wood',sc=.3),seg=14,r2=.36); B.cyl((MD[0],MD[1],.505),.4,.05,M('#D83A8A',.85,kind='fabric'),seg=14)
    # showcase with crockery (back wall, left)
    B.box((-3.3,4.35,1.15),(1.3,.25,1.15),wd,.02); B.box((-3.3,4.08,1.45),(1.15,.012,.7),M('#BFD0D8',.12,spec=1.0,alpha=.35),0)
    for z_ in (1.0,1.55,2.1): B.box((-3.3,4.3,z_-.3),(1.2,.2,.02),wd2,0)
    for q in range(6): B.cyl((-4.2+q*.36,4.3,1.86),.13,.02,M('#F4F1EA',.3),rot=(R(78),0,0),seg=12); B.cyl((-4.2+q*.36,4.28,1.3),.06,.1,M(r.choice(['#F4F1EA','#8FB8D8','#E6B93A']),.3),seg=8)
    B.box((-3.3,4.35,2.36),(1.36,.28,.06),wd,.02)
    # frames, clock, curtain window (left wall), floor lamp, fan, door (right wall)
    for i,(x,z,w,h,c) in enumerate(((0.0,2.9,.42,.3,'#8FB8D8'),(1.1,3.05,.3,.4,'#E8C9A0'),(2.2,2.9,.42,.3,'#C8E0B8'),(-1.2,2.95,.3,.38,'#F2D0C0'))): B.box((x,4.6,z),(w+.05,.03,h+.05),gd if i%2 else wd,.01); B.box((x,4.57,z),(w,.01,h),M(c,.7),0); B.ico((x,4.555,z+.03),min(w,h)*.38,M('#D8A277',.7),sc=(1,.08,1),sub=1)
    B.cyl((3.9,4.58,3.2),.34,.05,M('#F4F1EA',.5),rot=(R(90),0,0),seg=20); B.box((3.9,4.54,3.3),(.014,.01,.14),M('#16171C',.5),0); B.box((4.0,4.54,3.2),(.11,.01,.014),M('#16171C',.5),0)
    B.box((-5.18,.2,2.4),(.03,1.1,1.1),lit('#3A3A7A',.8,always=True),0)
    for q in (-1,1): B.box((-5.08,.2+q*1.0,2.2),(.08,.45,1.9),M('#8A1F3A',.85,kind='fabric'),.05)
    B.box((-5.08,.2,3.9),(.1,1.6,.16),gd,.03)
    B.cyl((-4.3,3.9,.03),.22,.06,gd,seg=10); B.cyl((-4.3,3.9,.9),.025,1.8,gd,seg=6); B.cyl((-4.3,3.9,1.9),.3,.42,M('#F2D8A0',.5,emit=2.2),seg=12,r2=.18); point((-4.3,3.6,1.9),90,(1,.82,.55),r=.3,shadow=False)
    B.cyl((0,1.2,4.3),.08,.3,M('#F4F1EA',.5),seg=8)
    for q in range(3): B.box((.62*math.cos(q*2.094),1.2+.62*math.sin(q*2.094),4.18),(.6,.09,.012),M('#F4F1EA',.5),0,rot=(0,0,q*2.094))
    B.box((5.2,1.9,1.3),(.05,.75,1.3),wd,.02); B.box((5.14,1.9,1.3),(.012,.6,1.15),wd2,0); B.cyl((5.1,1.35,1.25),.045,.08,gd,rot=(0,R(90),0),seg=8)
    B.box((-4.4,-1.2,.5),(.5,.32,.02),M('#C9CED8',.3,metal=.7),.01); B.box((-4.4,-1.2,.2),(.5,.32,.02),M('#C9CED8',.3,metal=.7),.01)
    for sx in (-.45,.45):
        for sy in (-.28,.28): B.cyl((-4.4+sx,-1.2+sy,.3),.018,.6,M('#C9CED8',.3,metal=.7),seg=6)
    B.cyl((-4.55,-1.2,.62),.11,.2,M('#D83A8A',.4),seg=10); B.cyl((-4.2,-1.15,.56),.045,.08,M('#F4F1EA',.4),seg=8)
    B.box((0,1,4.38),(1.0,.08,.04),lit('#FFF2DC',1.4,always=True),0)
    for (x_,y_) in ((-2.8,-2.0),(2.8,-2.0),(-2.8,2.4),(2.8,2.4)): point((x_,y_,3.3),185,(1,.9,.74),r=1.2,shadow=False)
    B.done('baithak'); return S
# ---------------------------------------------------------------- castle
def torch(x,y,z,e=320):
    B.box((x,y,z),(.05,.05,.3),M('#3A2A1E',.6),0); B.ico((x,y,z+.42),.14,M('#FFB03A',.3,emit=9.0),sc=(1,1,1.5),sub=1); point((x,y-.4 if y>0 else y+.4,z+.4),e,(1,.62,.3),r=.4,shadow=False)
def qila(table=False,locks=False):
    """castle hall: x -7..7, y -7..9, 9 m high. big double door in the back wall at (0,9). red carpet along y. coffin on a plinth at (-3.6,4). optional council table at (0,1.5) with the map"""
    NIGHT[0]=1.0; S=setup_world('lv_in',shadow=30); r=random.Random(31); st=M('#4A4E5E',.92,kind='wall',sc=1.6); st2=M('#3A3E4C',.92,kind='wall',sc=1.6); wd=M('#3A2618',.6,kind='wood',sc=.5); gd=M('#C9A24A',.3,metal=.8)
    B.box((0,0,-.1),(9,12,.1),M('#30323C',.9,kind='tile',sc=1.4),0); B.box((0,9.2,7.5),(1.8,.2,1.5),st,0); B.box((0,1,9.1),(7.4,9,.1),st2,0)
    for sx in (-1,1): B.box((sx*4.6,9.2,4.5),(2.8,.2,4.5),st,0); B.box((sx*2.6,13.4,.45),(.3,4.0,.45),st2,.03)
    B.box((0,14,-.06),(7,5,.06),M('#E6ECF6',.85),0); B.box((0,19.5,7),(14,.1,8),lit('#16224A',.55,always=True),0); point((0,12.5,4.2),320,(.66,.76,1.0),r=1.0,shadow=False)
    for sx in (-1,1):
        B.box((sx*7.2,1,4.5),(.2,9,4.5),st,0)
        for k in range(4): y=-4+k*4.0; B.box((sx*6.3,y,4.5),(.45,.45,4.5),st2,.04); B.box((sx*6.3,y,.4),(.6,.6,.4),st2,.04); B.box((sx*6.3,y,8.6),(.6,.6,.3),st2,.04)
        for k in range(3): y=-2+k*4.0; B.box((sx*6.98,y,5.0),(.03,.9,2.2),lit('#6A8AE0',1.6,always=True),0); B.cyl((sx*6.98,y,7.2),.9,.06,lit('#6A8AE0',1.6,always=True),rot=(0,R(90),0),seg=14); B.box((sx*6.95,y,5.4),(.03,.04,2.6),st2,0); B.box((sx*6.95,y,5.6),(.03,.9,.04),st2,0)
        for k in range(2): y=0+k*4.0; B.box((sx*6.9,y,6.0),(.03,.55,1.5),M('#3D1050',.85,kind='fabric'),0); B.ico((sx*6.86,y,6.3),.22,gd,sc=(.1,1.6,.7),sub=1)
    B.box((0,1,.012),(1.25,8.6,.012),M('#7A1420',.9,kind='fabric'),0); B.box((0,1,.02),(1.0,8.6,.012),M('#9A1C2A',.9,kind='fabric'),0)
    # door: stone arch, two heavy leaves (objects), iron bands
    B.box((0,9.02,6.6),(2.3,.1,.5),st2,.03); 
    for sx in (-1,1): B.box((sx*2.1,9.02,3.1),(.28,.12,3.1),st2,.03)
    L=[]
    for sx in (-1,1):
        e=empty((sx*1.8,8.98,0)); obox((-sx*.9,0,3.0),(.9,.09,3.0),wd,.02,e)
        for z_ in (1.0,3.0,5.0): obox((-sx*.9,-.1,z_),(.9,.02,.09),M('#2A2C34',.4,metal=.7),0,e)
        oico((-sx*1.55,-.14,2.9),.11,gd,e,sub=1); L.append(e)
    torch(-3.0,8.9,3.6); torch(3.0,8.9,3.6)
    for (x,y) in ((-5.2,-1.0),(5.2,-1.0),(-5.2,5.5),(5.2,5.5)):
        B.cyl((x,y,.05),.3,.1,gd,seg=10); B.cyl((x,y,1.1),.04,2.1,gd,seg=6)
        for q in range(3): a=q*2.094; B.cyl((x+.25*math.cos(a),y+.25*math.sin(a),2.15),.03,.26,M('#F4F1EA',.5),seg=6); B.ico((x+.25*math.cos(a),y+.25*math.sin(a),2.36),.06,M('#FFB03A',.3,emit=9.0),sc=(1,1,1.6),sub=1)
        point((x,y,2.5),200,(1,.66,.34),r=.4,shadow=False)
    B.box((-3.6,4.0,.25),(1.1,1.8,.25),st2,.04); C=coffin((-3.6,4.0,.5),0,0)
    if table:
        B.cyl((0,1.5,.98),1.9,.1,wd,seg=20); B.cyl((0,1.5,.5),.3,1.0,wd,seg=10); B.cyl((0,1.5,.05),.9,.1,wd,seg=14)
        B.box((0,1.5,1.04),(1.25,.85,.012),M('#E8D8B0',.85),0); B.box((0,1.5,1.05),(1.2,.8,.008),M('#D9C9A0',.85),0)
        for (px,py,pw,ph,c) in ((-.6,1.75,.4,.3,'#B8C8A0'),(.45,1.2,.5,.25,'#B8C8A0'),(.2,1.95,.3,.2,'#C8D0A8'),(-.75,1.1,.25,.22,'#B8C8A0')): B.box((px,py,1.058),(pw,ph,.004),M(c,.85),.0)
        o_=text('LAHORE',(.12,1.52,1.066),(0,-1,0),.2,M('#16171C',.5),ex=.003); o_.rotation_euler=(0,0,0)
        for a in (45,-45): B.box((.12,1.52,1.085),(.62,.05,.008),M('#D8202A',.4,emit=1.5),0,rot=(0,0,R(a)))
        B.box((0,.92,1.064),(.56,.1,.006),M('#B8232E',.5),.004); o_=text('NO FLY ZONE',(0,.92,1.072),(0,-1,0),.11,M('#F4F1EA',.5),ex=.003); o_.rotation_euler=(0,0,0)
        point((0,.9,3.0),150,(1,.85,.6),r=.6,shadow=False)
    LK=None
    if locks:
        LK=empty((0,8.84,0)); im=M('#2A2C34',.4,metal=.8)
        for i,(z_,a) in enumerate(((1.2,12),(2.3,-9),(3.4,8),(4.5,-12))): obox((0,0,z_),(1.75,.03,.07),im,.01,LK,rot=(0,R(a),0)); obox((0,-.06,z_),(.2,.06,.24),gd,.04,LK); ocyl((0,-.06,z_+.28),.13,.05,im,LK,rot=(R(90),0,0),seg=10)
        for z_ in (1.8,4.0): obox((0,-.02,z_),(1.9,.05,.16),M('#5A3A22',.6,kind='wood'),.02,LK,rot=(0,R(5 if z_<3 else -6),0))
    point((0,-3.5,4.5),700,(.66,.74,1.0),r=1.5,shadow=False); point((0,4,6.5),260,(.7,.6,1.0),r=1.5,shadow=False)
    B.done('qila'); return dict(S=S,dl=L[0],dr=L[1],coffin=C,locks=LK)
def qila_ext():
    """castle gate at night in the snow. gate door at (0,6) facing -y; stone bridge along y from -14 to 6; towers either side; pines; moon"""
    NIGHT[0]=1.0; S=setup_world('lv_snow',shadow=70); r=random.Random(41); st=M('#555A6C',.92,kind='wall',sc=1.6); st2=M('#434858',.92,kind='wall',sc=1.6); sn=M('#E6ECF6',.85); wd=M('#3A2618',.6,kind='wood',sc=.5); gd=M('#C9A24A',.3,metal=.8)
    B.box((0,0,-6),(200,200,.2),M('#1A2038',.95),0); B.box((0,-4,-.3),(3.6,10.2,.3),st2,0); B.box((0,-4,.02),(3.4,10.2,.02),sn,0)
    for sx in (-1,1):
        B.box((sx*3.5,-4,.45),(.22,10.2,.45),st,0); B.box((sx*3.5,-4,.93),(.26,10.2,.04),sn,0)
        for k in range(6): B.box((sx*3.5,-13+k*3.6,1.15),(.3,.3,.22),st,0); B.box((sx*3.5,-13+k*3.6,1.4),(.33,.33,.04),sn,0)
        B.cyl((sx*5.6,7.4,9),2.6,18,st,seg=14); B.cyl((sx*5.6,7.4,20.5),3.0,5.2,M('#2A2E48',.8),seg=14,r2=.1); B.cyl((sx*5.6,7.4,18.2),2.95,.5,st2,seg=14)
        for k in range(3): B.box((sx*5.6,4.78,6+k*4.0),(.35,.05,.7),lit('#FFB45A',2.8),0)
        torch(sx*2.6,5.86,3.2,420)
    B.box((0,8.5,7),(16,2.5,7),st,0); B.box((0,6.0,10.5),(3.2,.4,3.5),st,0); B.box((0,5.9,14.2),(3.4,.5,.3),st2,0)
    for k in range(9): B.box((-3.2+k*.8,5.9,14.75),(.25,.5,.3),st2,0)
    for k in range(20): B.box((-15.5+k*1.6,6.1,14.3),(.5,.3,.35),st2,0)
    B.cyl((0,5.84,6.9),2.1,.3,st2,rot=(R(90),0,0),seg=18); L=[]
    for sx in (-1,1):
        B.box((sx*2.35,5.82,3.5),(.3,.25,3.5),st2,.03)
        e=empty((sx*2.05,5.86,0)); obox((-sx*1.02,0,3.3),(1.02,.1,3.3),wd,.02,e)
        for z_ in (1.1,3.3,5.5): obox((-sx*1.02,-.11,z_),(1.02,.02,.1),M('#2A2C34',.4,metal=.7),0,e)
        oico((-sx*1.75,-.16,3.1),.13,gd,e,sub=1); L.append(e)
    B.box((0,6.6,3.3),(2.05,.02,3.3),lit('#FFB45A',2.2,always=True),0)
    for k in range(60):
        a=r.uniform(0,6.283); d=r.uniform(16,70); x=d*math.cos(a); y=d*math.sin(a)-4
        if abs(x)<6 and -16<y<10: continue
        z=-5.8+r.uniform(0,4.5); h=r.uniform(4,8); B.cyl((x,y,z+h*.2),.2,h*.4,M('#3A2A1E',.8),seg=6); B.cyl((x,y,z+h*.62),h*.28,h*.75,M('#1F4A3A',.9,kind='leaves'),seg=7,r2=.02); B.cyl((x,y,z+h*.9),h*.14,h*.3,sn,seg=7,r2=.02)
    for k in range(9): a=-1.2+k*.3; B.cyl((60*math.sin(a),90,-6+r.uniform(8,20)),r.uniform(14,22),r.uniform(30,46),M('#2A3050',.95),seg=6,r2=.5)
    for k in range(150): a=r.uniform(0,6.283); el=r.uniform(.12,1.25); d=430; B.ico((d*math.cos(a)*math.cos(el),d*math.sin(a)*math.cos(el),d*math.sin(el)),r.uniform(.5,1.2),M('#FFFFFF',.3,emit=6.0),sub=1)
    B.ico((-120,400,190),26,M('#FFF6D8',.3,emit=3.2),sub=3)
    point((0,-2,5),900,(.62,.72,1.0),r=2,shadow=False)
    B.done('qila_ext'); return dict(S=S,dl=L[0],dr=L[1])
def plaza():
    """old European square at night (hook): cobbles, fountain at (0,2), half-timbered houses on three sides, clock tower, lamps"""
    NIGHT[0]=1.0; S=setup_world('lv_snow',shadow=60); r=random.Random(51); B.box((0,0,-.1),(120,120,.1),M('#3A3C46',.92,kind='tile',sc=.5),0)
    B.cyl((0,2,.25),1.9,.5,M('#8A8E9A',.8,kind='concrete'),seg=16); B.cyl((0,2,.52),1.7,.04,M('#3A6A9A',.2,spec=1.0),seg=16); B.cyl((0,2,.9),.45,1.3,M('#8A8E9A',.8),seg=10); B.cyl((0,2,1.6),.9,.14,M('#8A8E9A',.8),seg=12)
    def hh(x,y,w,rz,seed):
        q=random.Random(seed); c=q.choice(['#E8DCC0','#D9C9A8','#C9B48A','#E2D2B8']); h=q.uniform(6,8); cs=math.cos(R(rz)); sn_=math.sin(R(rz))
        B.box((x,y,h/2),(w,3,h/2),M(c,.9,kind='wall'),0,rot=(0,0,R(rz))); B.box((x,y,h+1.1),(w+.2,3.2,1.2),M(q.choice(['#7A3A2A','#5A3A3A','#3A4A5A']),.85),0,rot=(0,R(0),R(rz)))
        for k in range(-2,3): B.box((x+k*w*.4*cs-3.02*(-sn_),y+k*w*.4*sn_-3.02*cs,h/2),(.06,.03,h/2),M('#3A2618',.7),0,rot=(0,0,R(rz)))
        for z_ in (2.9,5.4): B.box((x+3.02*sn_,y-3.02*cs,z_),(w,.03,.07),M('#3A2618',.7),0,rot=(0,0,R(rz)))
        for k in (-1,1):
            for z_ in (1.7,4.2): B.box((x+k*w*.5*cs+3.03*sn_,y+k*w*.5*sn_-3.03*cs,z_),(.45,.03,.6),lit('#FFD890',2.2) if q.random()<.6 else M('#1A1E2A',.3),0,rot=(0,0,R(rz)))
    for i,x in enumerate((-11,-4.6,4.6,11)): hh(x,10.5,3.2,0,60+i)
    for i,y in enumerate((-3,3.5)): hh(-10.5,y,3.2,-90,70+i); hh(10.5,y,3.2,90,80+i)
    for i,y in enumerate((-9.6,-16.1,-22.6,-29.1)): hh(-8.0,y,3.2,-90,90+i); hh(8.0,y,3.2,90,100+i)      # the street they flee down
    for (x,y) in ((-4.4,-8),(4.4,-13),(-4.4,-18),(4.4,-23)): B.cyl((x,y,2),.07,4,M('#2A2C34',.5,metal=.5),seg=8); B.box((x,y,4.2),(.18,.18,.25),lit('#FFC36A',6.0),.04); point((x,y,3.9),380,(1,.8,.52),r=.5,shadow=False)
    B.box((0,15.5,8),(2.2,2.2,8),M('#8A8274',.9,kind='wall'),0); B.cyl((0,15.5,18.5),3.0,5,M('#3A4A5A',.8),seg=4,r2=.1); B.cyl((0,13.25,12.5),1.3,.1,lit('#FFF0C0',1.8),rot=(R(90),0,0),seg=20)
    for (x,y) in ((-5,-1),(5,-1),(-6,7),(6,7)): B.cyl((x,y,2),.07,4,M('#2A2C34',.5,metal=.5),seg=8); B.box((x,y,4.2),(.18,.18,.25),lit('#FFC36A',6.0),.04); point((x,y,3.9),380,(1,.8,.52),r=.5,shadow=False)
    for k in range(120): a=r.uniform(0,6.283); el=r.uniform(.12,1.25); d=430; B.ico((d*math.cos(a)*math.cos(el),d*math.sin(a)*math.cos(el),d*math.sin(el)),r.uniform(.5,1.2),M('#FFFFFF',.3,emit=6.0),sub=1)
    B.ico((60,400,200),24,M('#FFF6D8',.3,emit=3.2),sub=3); point((0,-4,5),700,(.62,.72,1.0),r=2,shadow=False)
    B.done('plaza'); return S
