# Set for the "every city" announcement: a creator's map room. Back wall (y=3) carries a pixel map of Pakistan
# with city pins that light up; shelves with mini landmarks, editing desk, ring light, tripod, rug, string lights.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
PK=[(71.2,36.4),(72.5,36.9),(74.8,37.0),(76.8,35.7),(77.6,34.8),(76.6,34.0),(74.4,33.0),(75.3,32.4),(74.6,31.1),(73.9,29.9),(72.9,29.0),(71.9,27.9),
    (70.6,27.9),(70.0,26.6),(71.0,24.6),(70.0,24.2),(68.9,24.3),(68.2,23.7),(67.4,24.0),(67.0,24.8),(66.4,25.5),(64.6,25.2),(63.5,25.2),(61.6,25.1),
    (61.8,26.2),(63.2,26.7),(63.2,27.2),(62.8,28.3),(60.9,29.8),(62.5,29.4),(64.1,29.4),(66.2,29.8),(66.4,30.9),(67.3,31.2),(68.2,31.8),(69.3,31.9),
    (69.5,33.1),(70.0,33.3),(70.0,34.0),(71.1,34.1),(71.6,35.0),(71.6,35.9)]
MAPZ=3.9; WALLY=3.0
def mp(lon,lat,y=WALLY-.16): return ((lon-69.3)*.225,y,MAPZ+(lat-30.3)*.26)
CITY=dict(LAHORE=(74.35,31.52),KARACHI=(67.0,24.9),PESHAWAR=(71.5,34.0),QUETTA=(67.0,30.2),MULTAN=(71.5,30.2),ISLAMABAD=(73.05,33.7),FAISALABAD=(73.0,31.2),
          HYDERABAD=(68.4,25.5),SIALKOT=(74.5,32.5),GWADAR=(62.4,25.3),GILGIT=(74.3,35.9),SUKKUR=(68.9,27.7),BAHAWALPUR=(71.7,29.2),SMALL=(69.6,29.0))
def _inside(x,y,P):
    c=False; n=len(P)
    for i in range(n):
        (x1,y1),(x2,y2)=P[i],P[(i+1)%n]
        if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: c=not c
    return c
def pk_map():
    """pixel map on the back wall + one pin per city. returns {city:(off_dot,glow,ring)}"""
    r=random.Random(11); G=[M(c,.55,emit=.25) for c in ('#1F8A5A','#23976A','#1B7C52')]; c=.14
    lon=60.6
    while lon<78:
        lat=23.6
        while lat<37.2:
            if _inside(lon,lat,PK): x,y,z=mp(lon,lat,WALLY-.07); B.box((x,y,z),(c*.46,.035,c*.46),r.choice(G),.012)
            lat+=c/.26
        lon+=c/.225
    B.box((0,WALLY-.02,MAPZ+.05),(2.55,.03,2.15),M('#0E2A33',.7),.03)                      # board
    for sx in (-1,1): B.box((sx*2.6,WALLY-.03,MAPZ+.05),(.07,.06,2.25),M('#8A5A32',.6,kind='wood'),.02)
    for sz in (-1,1): B.box((0,WALLY-.03,MAPZ+.05+sz*2.2),(2.67,.06,.07),M('#8A5A32',.6,kind='wood'),.02)
    pins={}
    for k,(lo,la) in CITY.items():
        x,y,z=mp(lo,la); off=oico((x,y,z),.045,M('#D8DCE2',.5),sub=1)
        g=oico((x,y-.02,z),.085,M('#FFD23F',.3,emit=6.0),sub=2); g.scale=(0,0,0)
        rg=ocyl((x,y+.03,z),.17,.02,M('#FF4F8B',.3,emit=3.0),rot=(R(90),0,0),seg=20); rg.scale=(0,0,0)
        pins[k]=(off,g,rg)
    return pins
def pin_set(pins,k,on,t=0.0):
    """on: 0..1 (use pop()); lit pins breathe a little"""
    off,g,rg=pins[k]; b=1+.12*math.sin(t*5+hash(k)%7); g.scale=(on*b,)*3; rg.scale=(on,on,on)
def mini_minar(e,s=1.0):
    w=M('#F4F1EA',.5); ocyl((0,0,.05*s),.2*s,.1*s,w,e,rot=(0,0,0),seg=12); ocyl((0,0,.15*s),.14*s,.1*s,w,e,rot=(0,0,0),seg=12)
    ocyl((0,0,.55*s),.06*s,.7*s,w,e,rot=(0,0,0),seg=10,r2=.035*s); ocyl((0,0,.93*s),.06*s,.06*s,w,e,rot=(0,0,0),seg=10); oico((0,0,1.0*s),.04*s,M('#D9B24A',.3,metal=.8),e,sub=1)
def mini_mosque(e,s=1.0):
    w=M('#F4F1EA',.5); obox((0,0,.04*s),(.3*s,.22*s,.04*s),M('#C9CED8',.6),.01,e)
    for a in range(4): obox((0,0,.2*s),(.2*s,.012*s,.2*s),w,.005,e,rot=(R(38),0,a*pi/2))
    for sx in (-1,1):
        for sy in (-1,1): ocyl((sx*.27*s,sy*.19*s,.3*s),.018*s,.5*s,w,e,rot=(0,0,0),seg=6,r2=.006*s)
def mini_clock(e,s=1.0):
    st=M('#C9A27A',.7); obox((0,0,.22*s),(.09*s,.09*s,.22*s),st,.01,e); obox((0,0,.5*s),(.11*s,.11*s,.07*s),M('#F4F1EA',.5),.01,e)
    for a in range(4): ocyl((math.sin(a*pi/2)*.115*s,-math.cos(a*pi/2)*.115*s,.5*s),.05*s,.01,M('#16171C',.4),e,rot=(R(90),0,a*pi/2),seg=12)
    ocyl((0,0,.62*s),.1*s,.14*s,M('#8A3A2A',.6),e,rot=(0,0,0),seg=4,r2=.0)
def mini_truck(e,s=1.0):
    obox((0,0,.12*s),(.3*s,.12*s,.08*s),M('#E8552D',.4),.01,e); obox((.2*s,0,.24*s),(.1*s,.12*s,.09*s),M('#2B5AA8',.4),.01,e); obox((-.08*s,0,.27*s),(.2*s,.125*s,.1*s),M('#F2C14E',.5),.01,e)
    obox((.2*s,0,.38*s),(.13*s,.13*s,.05*s),M('#35975A',.5),.01,e)
    for sx in (-.18,.18):
        for sy in (-1,1): ocyl((sx*s,sy*.12*s,.05*s),.05*s,.03*s,M('#16171C',.7),e,seg=10)
def plant(x,y,z=0,s=1.0,col='#3F8A4A'):
    B.cyl((x,y,z+.18*s),.16*s,.36*s,M('#C96A3A',.7),seg=12,r2=.2*s)
    r=random.Random(int(x*31+y*17))
    for k in range(7): a=k*.9; B.box((x+math.cos(a)*.1*s,y+math.sin(a)*.1*s,z+(.6+r.uniform(0,.35))*s),(.035*s,.1*s,.3*s),M(shade(col,r.uniform(.8,1.15)),.7),.02,rot=(R(r.uniform(-22,22)),R(r.uniform(-22,22)),a))
def shelf(x,y,rz=0):
    wd=M('#7A5230',.6,kind='wood'); root=empty((x,y,0),rot=(0,0,R(rz)))
    for sx in (-1,1): obox((sx*.95,0,1.5),(.05,.3,1.5),wd,.02,root)
    for k in range(5): obox((0,0,.1+k*.72),(.95,.3,.04),wd,.02,root)
    obox((0,.28,1.5),(.95,.02,1.5),M('#5A3A22',.7),.01,root)
    items=[(mini_truck,-.45,0,1.0),(mini_clock,.45,0,1.0),(mini_minar,-.5,1,.62),(mini_mosque,.42,1,.9),(mini_clock,-.5,2,.9),(mini_truck,.4,2,.9),(mini_mosque,-.45,3,.85),(mini_minar,.5,3,.6)]
    for fn,dx,k,s in items: e=empty((dx,-.02,.14+k*.72),root); fn(e,s)
    r=random.Random(5)
    for k in range(4):                                             # books between the models
        for j in range(4): obox((-.1+j*.075,.05,.14+k*.72+.17),(.03,.16,.17+r.uniform(-.03,.03)),M(r.choice(['#2B5AA8','#C8372D','#F2C14E','#35975A','#7448C2','#F4F1EA']),.6),.008,root)
    return root
def desk(x,y):
    wd=M('#8A5A32',.5,kind='wood'); dk=M('#16171C',.4); B.box((x,y,1.05),(1.25,.6,.05),wd,.02)
    for sx in (-1.1,1.1):
        for sy in (-.45,.45): B.box((x+sx,y+sy,.5),(.05,.05,.5),dk,.01)
    B.box((x,y+.3,1.72),(.75,.03,.44),dk,.02); B.box((x,y+.265,1.72),(.7,.005,.39),M('#2A3A5A',.3,emit=.6),0)                 # monitor: edit timeline
    for k,(c,w) in enumerate((('#FFCF2E',.5),('#FF4F8B',.32),('#3FA7E8',.42),('#35975A',.25))): B.box((x-.62+w+.02+k*.04,y+.258,1.45+k*.06),(w,.004,.022),M(c,.4,emit=1.5),0)
    B.box((x,y+.255,1.86),(.3,.004,.19),M('#F2B27A',.4,emit=1.0),0); B.box((x,y+.25,1.8),(.08,.004,.1),M('#D8432E',.4,emit=1.0),0)
    B.box((x,y+.3,1.2),(.05,.04,.12),dk,.01); B.box((x,y+.3,1.11),(.25,.15,.012),dk,.01)
    B.box((x-.1,y-.2,1.115),(.42,.14,.015),M('#2A2C34',.5),.01); B.box((x+.55,y-.2,1.115),(.07,.1,.018),M('#F4F1EA',.4),.02)        # keyboard, mouse
    B.cyl((x-.9,y-.1,1.2),.07,.18,M('#F4F1EA',.4),seg=12); B.box((x+.95,y+.1,1.45),(.02,.02,.35),dk,.005,rot=(0,R(-20),0)); B.box((x+.82,y+.1,1.78),(.06,.06,.1),M('#3A3D47',.4),.03)  # mug, mic arm
    # chair
    B.box((x,y-1.15,.75),(.42,.4,.07),M('#D8432E',.6,kind='fabric'),.05); B.box((x,y-1.5,1.4),(.42,.07,.62),M('#16171C',.6,kind='fabric'),.06); B.cyl((x,y-1.15,.38),.05,.66,dk,seg=8)
    for a in range(5): B.box((x+math.cos(a*1.257)*.25,y-1.15+math.sin(a*1.257)*.25,.06),(.27,.04,.03),dk,.01,rot=(0,0,a*1.257))
def ring_light(x,y,h=2.6):
    dk=M('#16171C',.4); B.cyl((x,y,h/2),.03,h,dk,seg=8)
    for a in range(3): B.box((x+math.cos(a*2.094)*.3,y+math.sin(a*2.094)*.3,.12),(.34,.025,.02),dk,.005,rot=(0,R(-20),a*2.094))
    e=empty((x,y,h+.45),rot=(0,0,R(-25)))
    for k in range(28): a=k*pi/14; obox((math.cos(a)*.45,0,math.sin(a)*.45),(.06,.035,.045),M('#FFF6E0',.3,emit=5.0),.01,e,rot=(0,-a,0))
def tripod_cam(x,y,rz=0):
    dk=M('#16171C',.4); root=empty((x,y,0),rot=(0,0,R(rz)))
    for a in range(3): obox((math.cos(a*2.094)*.33,math.sin(a*2.094)*.33,.85),(.025,.025,.9),dk,.005,root,rot=(R(-math.sin(a*2.094)*21),R(math.cos(a*2.094)*21),0))
    obox((0,0,1.78),(.06,.06,.08),dk,.01,root); obox((0,0,1.98),(.2,.14,.13),M('#22242B',.4),.03,root); ocyl((0,.2,1.98),.09,.16,dk,root,seg=14); ocyl((0,.285,1.98),.075,.01,M('#3FA7E8',.1,spec=1.0),root,seg=14)
    obox((.12,-.02,2.14),(.03,.03,.03),M('#E8301A',.3,emit=3.0),.01,root)
def flag(x,z,y=WALLY-.03,s=1.0):
    B.box((x+.36*s,y,z),(.5*s,.012,.4*s),M('#0F5A36',.7,kind='fabric'),.01); B.box((x-.3*s,y,z),(.16*s,.012,.4*s),M('#F4F1EA',.7,kind='fabric'),.01)
    B.cyl((x+.36*s,y-.016,z),.19*s,.008,M('#F4F1EA',.6),rot=(R(90),0,0),seg=20); B.cyl((x+.43*s,y-.022,z+.05*s),.165*s,.008,M('#0F5A36',.7),rot=(R(90),0,0),seg=20)
    B.ico((x+.52*s,y-.03,z+.1*s),.05*s,M('#F4F1EA',.6),sc=(1,.2,1),sub=1)
def frame_pic(x,z,cols,w=.42,h=.55,y=WALLY-.03):
    B.box((x,y,z),(w,.02,h),M('#F4F1EA',.6),.015); B.box((x,y-.012,z),(w-.05,.012,h-.05),M(cols[0],.6),0)
    B.box((x,y-.02,z-h*.45),(w-.05,.012,h*.25),M(cols[1],.7),0); B.box((x-w*.3,y-.024,z-.05),(w*.16,.012,h*.4),M(cols[2],.6),0); B.box((x+w*.25,y-.024,z-.12),(w*.2,.012,h*.3),M(cols[3],.6),0)
def map_room():
    wall=M('#1D4750',.85); fl=M('#B98A5A',.5,kind='wood',h2='#A87848',sc=3)
    B.box((0,0,-.05),(7,8,.05),fl,0); B.box((0,WALLY+.1,3.6),(7,.1,3.7),wall,0)
    for sx in (-1,1): B.box((sx*5.6,-1,3.6),(.1,5,3.7),M('#234F58',.85),0)
    B.box((0,-1,7.3),(7,5,.1),M('#16353C',.9),0)
    B.box((0,WALLY-.03,.25),(5.5,.04,.25),M('#F4F1EA',.6),.01)                                  # skirting
    pins=pk_map()
    stext('@INRBLXWORLD',(0,WALLY-.06,6.55),.42,'#FF4F8B',e=4.0); B.box((0,WALLY-.02,6.55),(2.3,.02,.36),M('#12303A',.8),.05)   # neon sign above the map
    r=random.Random(3)
    for k in range(23):                                                                          # string lights
        x=-5.2+k*.47; z=7.0-.22*math.sin(k/22*pi*3)**2; B.ico((x,WALLY-.25,z),.06,M(r.choice(['#FFD23F','#FF4F8B','#3FA7E8','#7CFC9A']),.3,emit=4.0),sub=1)
    B.box((0,WALLY-.25,7.08),(5.3,.008,.008),M('#16171C',.5),0)
    for (x,y,c) in ((-2.6,-.8,'#FFD23F'),(2.6,-.8,'#FF4F8B'),(0,-3.6,'#3FA7E8'),(-3.6,-4.2,'#7CFC9A'),(3.6,-4.4,'#FFD23F')):   # pendant lamps
        B.box((x,y,6.85),(.012,.012,.45),M('#16171C',.5),0); B.cyl((x,y,6.3),.34,.3,M(c,.5),seg=14,r2=.12); B.ico((x,y,6.14),.13,M('#FFF6E0',.3,emit=6.0),sub=1)
    for y in (-4.5,-2.0,.5): B.box((0,y,7.12),(5.5,.12,.1),M('#6A4628',.6,kind='wood'),.02)                                     # ceiling beams
    shelf(-4.2,2.62); desk(3.9,1.9)
    flag(-4.55,3.85,s=.9); frame_pic(3.55,3.5,('#FFB878','#C8A070','#E8708A','#7FB8E0')); frame_pic(4.55,3.3,('#8FD0FF','#3F8A4A','#F2C14E','#C8372D'),w=.36,h=.46); frame_pic(4.1,4.5,('#2A3A6A','#16171C','#FFD23F','#FF4F8B'),w=.5,h=.36)
    plant(-2.95,2.5,s=1.3); plant(2.35,2.55,s=1.1,col='#2F7A5A'); plant(5.0,.2,s=1.5,col='#4F9A4A')
    B.cyl((0,-.1,.012),1.9,.024,M('#C8372D',.9,kind='fabric'),seg=40); B.cyl((0,-.1,.02),1.5,.024,M('#F2C14E',.9,kind='fabric'),seg=40); B.cyl((0,-.1,.028),1.1,.024,M('#1F8A5A',.9,kind='fabric'),seg=40)  # rug
    ring_light(-3.2,-2.6); tripod_cam(3.1,-2.9,rz=25)
    B.box((-4.6,-1.2,.35),(.5,.5,.35),M('#7448C2',.8,kind='fabric'),.12); B.box((-4.4,.4,.3),(.4,.4,.3),M('#16909E',.8,kind='fabric'),.1)     # bean bags
    B.done('room')
    S,A,w,bg=setup_interior('day',room=(0,-1,7.1),res=PCT,samples=SAMPLES,shadow_dist=22); A.data.energy=520; A.data.size=7.0
    point((0,-4.5,4.2),900,(1,.93,.82),r=1.2); point((-4.2,1.2,3.6),260,(1,.45,.7),r=.6,shadow=False); point((4.3,1.0,3.6),260,(.4,.75,1.0),r=.6,shadow=False); point((0,2.2,6.2),160,(1,.5,.75),r=.5,shadow=False)
    return pins
