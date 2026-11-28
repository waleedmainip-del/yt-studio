# World for "India vs Pakistan" (match day): two mirrored living rooms (Lahore = P, Delhi = I), stackable as a dollhouse (Delhi upstairs),
# a mohalla street (day/night), a shaadi tent and a cricket ground for the TV shots.  Rooms are open toward -y (camera side); the TV sits on the camera side.
INT['ip_eve']=dict(sun=(66,205),e=.55,col=(.6,.7,1.0),top='#0C1430',bot='#26366A',sky=.42,fill=(1,.9,.76),fe=0,cloud='#2A3550',cov=.5)
HH=3.4; SLAB=.2; UPZ=HH+SLAB; HW=4.6; BACK=3.2
DADP=(-1.05,1.42); BOYP=(1.05,1.42); MOMP=(3.1,.8); GRANP=(-3.1,.8)
MOMRZ=face_dir(0-MOMP[0],-3.2-MOMP[1]); GRANRZ=face_dir(0-GRANP[0],-3.2-GRANP[1])
PAL=dict(P=dict(wall='#DCE8D2',floor='#B88A5A',kind='wood',rug='#B8553A',rug2='#F2E3C4',team=PKG,team2=PKW,curt='#2F6B4F',accent='#E6B53A',bunt=(PKG,PKW)),
         I=dict(wall='#D5E0F2',floor='#A8977C',kind='tile',rug='#D9A23A',rug2='#27365A',team=INB,team2=INO,curt='#C8662C',accent='#27365A',bunt=('#FF9933','#F8F8F4','#138808')))
def star5(loc,r,mat,par=None,rot=0.0):
    vs=[(0,0,0)]
    for k in range(10):
        a=R(rot)+k*pi/5; rr=r if k%2==0 else r*.4; vs.append((rr*math.sin(a),0,rr*math.cos(a)))
    return omesh(vs,[(0,1+k,1+(k+1)%10) for k in range(10)],mat,par,loc=loc)
def flag_pk(loc,w=1.5,par=None):
    """Pakistan flag, hoist on the left, facing -y"""
    h=w*2/3; x,y,z=loc; g=M('#01411C',.7,kind='fabric'); wh=M('#F8F8F4',.7)
    obox((x+w*.125,y,z),(w*.375,.012,h/2),g,0,par); obox((x-w*.375,y,z),(w*.125,.012,h/2),wh,0,par)
    cx=x+w*.125; r=h*.3
    ocyl((cx,y-.016,z),r,.006,wh,par,rot=(R(90),0,0),seg=32); ocyl((cx+r*.27,y-.021,z+r*.27),r*.85,.006,g,par,rot=(R(90),0,0),seg=32)
    star5((cx+r*.44,y-.026,z+r*.44),r*.36,wh,par,rot=45)
def flag_in(loc,w=1.5,par=None):
    """India flag, facing -y"""
    h=w*2/3; x,y,z=loc
    for k,c in enumerate(('#FF9933','#F8F8F4','#138808')): obox((x,y,z+h/3*(1-k)),(w/2,.012,h/6),M(c,.7,kind='fabric'),0,par)
    nv=M('#000080',.6); r=h/6*.86
    ocyl((x,y-.016,z),r,.006,nv,par,rot=(R(90),0,0),seg=32); ocyl((x,y-.021,z),r*.84,.006,M('#F8F8F4',.7),par,rot=(R(90),0,0),seg=32)
    for k in range(12): obox((x,y-.026,z),(r*.84,.004,.007),nv,0,par,rot=(0,k*pi/12,0))
    ocyl((x,y-.03,z),r*.17,.006,nv,par,rot=(R(90),0,0),seg=10)
def _rot(x,y,rz,lx,ly): a=R(rz); return (x+lx*math.cos(a)-ly*math.sin(a),y+lx*math.sin(a)+ly*math.cos(a))
def sofa2(x,y,z0,col='#7A1F2E',w=2.25):
    """the same 2-seater in both houses: maroon velvet with white lace covers. faces -y, seat top .58"""
    m=M(col,.85,kind='fabric'); d=M(shade(col,.78),.85,kind='fabric'); wood=M('#4A2E1C',.5,kind='wood'); lace=M('#F6F1E4',.8,kind='fabric')
    B.box((x,y+.05,z0+.28),(w,.55,.2),d,.05); B.box((x,y,z0+.5),(w-.02,.5,.08),m,.06); B.box((x,y+.62,z0+.85),(w,.14,.57),m,.08)
    for s in (-1,1):
        B.box((x+s*(w+.17),y+.08,z0+.52),(.19,.64,.42),m,.08); B.box((x+s*1.05,y+.6,z0+1.34),(.5,.16,.1),lace,.02); B.box((x+s*1.05,y+.45,z0+1.22),(.5,.012,.2),lace,.004)
        B.box((x+s*(w+.17),y-.2,z0+.955),(.2,.3,.012),lace,.004)
        for sy in (-1,1): B.cyl((x+s*(w+.2),y+sy*.5,z0+.045),.06,.09,wood,seg=8)
def armchair(x,y,rz,z0,col='#7A1F2E'):
    m=M(col,.85,kind='fabric'); d=M(shade(col,.78),.85,kind='fabric'); lace=M('#F6F1E4',.8,kind='fabric'); a=R(rz)
    def bx(lx,ly,z,sz,mat,bv=.05): p=_rot(x,y,rz,lx,ly); B.box((p[0],p[1],z0+z),sz,mat,bv,rot=(0,0,a))
    bx(0,.05,.28,(.95,.55,.2),d); bx(0,0,.5,(.93,.5,.08),m,.06); bx(0,.62,.85,(.95,.14,.57),m,.08); bx(0,.6,1.34,(.5,.16,.1),lace,.02)
    for s in (-1,1): bx(s*1.12,.08,.52,(.19,.64,.42),m,.08)
def ctable(x,y,z0,side):
    wood=M('#5A3A22',.45,kind='wood',sc=.6); B.box((x,y,z0+.47),(.95,.42,.035),wood,.02)
    for sx in (-1,1):
        for sy in (-1,1): B.box((x+sx*.82,y+sy*.32,z0+.22),(.045,.045,.22),wood,.01)
    B.box((x,y,z0+.2),(.8,.32,.02),wood,.01)
    st=M('#C9CED8',.25,metal=.9); B.box((x-.42,y,z0+.515),(.36,.26,.012),st,.01)                       # steel tray
    for k,(dx,dy) in enumerate(((-.6,.1),(-.42,-.1),(-.24,.1))):
        B.cyl((x+dx,y+dy,z0+.575),.06,.1,M('#F4F1EA',.4),seg=12,r2=.048); B.cyl((x+dx,y+dy,z0+.622),.05,.008,M('#B8763A',.5),seg=12)
    B.cyl((x+.4,y+.02,z0+.515),.26,.02,M('#F4F1EA',.35),seg=20)                                         # samosa plate
    sm=M('#D9A04A',.7)
    for k,(dx,dy,rr) in enumerate(((.3,.08,20),(.5,.1,-30),(.4,-.1,70),(.28,-.08,130),(.52,-.06,-80))):
        B.box((x+dx,y+dy,z0+.56),(.085,.065,.04),sm,.03,rot=(0,0,R(rr)))
    B.cyl((x+.78,y+.2,z0+.535),.07,.05,M('#F4F1EA',.4),seg=10); B.cyl((x+.78,y+.2,z0+.558),.058,.008,M('#3F8A3A' if side=='P' else '#B8323A',.5),seg=10)   # chutney
    B.box((x+.1,y-.28,z0+.52),(.07,.16,.015),M('#23252E',.5),.01)                                       # remote
def home(side,z0=0.0,tvwall=False,flags=True,front=-9.0):
    """one living room. returns dict of lights + props.  side 'P' = Lahore, 'I' = Delhi"""
    p=PAL[side]; w=HW; h=HH; wm=M(p['wall'],.85,kind='wall',sc=.5); wm2=M(shade(p['wall'],.93),.85,kind='wall',sc=.5)
    yc=(front+BACK+.1)/2; yh=(BACK+.1-front)/2
    B.box((0,yc,z0-.05),(w+.1,yh,.05),M(p['floor'],.6,kind=p['kind'],sc=.7),0); B.box((0,BACK,z0+h/2),(w,.1,h/2),wm,0)
    for s in (-1,1): B.box((s*w,yc,z0+h/2),(.1,yh,h/2),wm2,0)
    B.box((0,BACK-.11,z0+.09),(w,.02,.09),M('#F4F1EA',.6),0); B.box((0,yc,z0+h+SLAB/2),(w+.2,yh,SLAB/2),M('#EFEAE0',.9),0)
    B.box((0,BACK-.14,z0+h-.12),(w,.1,.12),M('#F4F1EA',.7),.02)
    for s in (-1,1): B.box((s*(w-.14),yc,z0+h-.12),(.1,yh,.12),M('#F4F1EA',.7),.02)
    B.done('room'+side)
    # rug, sofa set, table
    B.box((0,-.5,z0+.012),(3.7,2.55,.012),M(p['rug'],.9,kind='fabric'),.0); B.box((0,-.5,z0+.016),(3.35,2.2,.012),M(p['rug2'],.9,kind='fabric'),.0); B.box((0,-.5,z0+.02),(3.1,1.95,.012),M(p['rug'],.9,kind='fabric'),.0)
    for sx in (-1,1):
        for sy in (-1,1): B.box((sx*2.45,-.5+sy*1.4,z0+.024),(.3,.3,.01),M(p['rug2'],.9,kind='fabric'),0,rot=(0,0,R(45)))
    # lived-in floor: floor cushion, toy bat + ball, slippers
    B.cyl((-3.55,-2.7,z0+.14),.5,.24,M(p['team'],.85,kind='fabric'),seg=16); B.cyl((-3.55,-2.7,z0+.27),.34,.03,M(p['team2'],.85,kind='fabric'),seg=14)
    B.box((-2.5,-2.05,z0+.06),(.07,.42,.03),M('#D9B982',.6,kind='wood',sc=.5),.02,rot=(0,0,R(35))); B.box((-2.75,-2.4,z0+.06),(.03,.16,.03),M('#2A2C34',.5),.01,rot=(0,0,R(35))); B.ico((-2.05,-1.75,z0+.1),.085,M('#B8232E',.5),sub=2)
    for q,dy in ((-1,0),(1,.08)): B.box((1.9+q*.14,-.05+dy,z0+.04),(.1,.24,.03),M('#3A2A1E',.6),.02,rot=(0,0,R(8*q)))
    sofa2(0,1.6,z0); armchair(MOMP[0],MOMP[1]+.05,MOMRZ,z0); armchair(GRANP[0],GRANP[1]+.05,GRANRZ,z0); ctable(0,-.75,z0,side)
    # back wall: flag above the sofa, clock, photo, window with curtains, shelf
    if flags: (flag_pk if side=='P' else flag_in)((0,BACK-.12,z0+2.5),1.35)
    B.cyl((-1.75,BACK-.12,z0+2.75),.3,.05,M('#F4F1EA',.5),rot=(R(90),0,0),seg=24); B.cyl((-1.75,BACK-.15,z0+2.75),.26,.02,M(p['accent'],.5),rot=(R(90),0,0),seg=24)
    B.cyl((-1.75,BACK-.165,z0+2.75),.23,.02,M('#FBF8F0',.5),rot=(R(90),0,0),seg=24); B.box((-1.75,BACK-.18,z0+2.83),(.012,.006,.09),M('#16171C',.5),0); B.box((-1.68,BACK-.18,z0+2.75),(.07,.006,.012),M('#16171C',.5),0)
    frame(1.75,BACK-.12,z0+2.7,.3,.38,'#D9B24A','#C9B48A' if side=='P' else '#B8C6D8')
    B.box((1.75,BACK-.15,z0+2.6),(.2,.01,.16),M(p['team'],.6),0); B.ico((1.68,BACK-.16,z0+2.86),.07,M('#C58C5E',.6),sub=1); B.ico((1.84,BACK-.16,z0+2.84),.06,M('#D9A273',.6),sub=1)
    wx=3.25; B.box((wx,BACK-.06,z0+2.1),(.8,.04,.85),M('#14204A',.3,emit=.35),0)
    for dx in (-.8,0,.8): B.box((wx+dx,BACK-.1,z0+2.1),(.035,.03,.87),M('#F4F1EA',.5),0)
    for dz in (-.85,0,.85): B.box((wx,BACK-.1,z0+2.1+dz),(.83,.03,.035),M('#F4F1EA',.5),0)
    for s in (-1,1): B.box((wx+s*.95,BACK-.16,z0+2.05),(.2,.04,1.0),M(p['curt'],.85,kind='fabric'),.02)
    B.box((wx,BACK-.16,z0+3.08),(1.25,.05,.05),M('#6B4A2E',.5),.01)
    B.box((-3.3,BACK-.3,z0+1.9),(.75,.18,.03),M('#5A3A22',.5,kind='wood'),.01)
    if side=='P':
        B.cyl((-3.6,BACK-.3,z0+2.15),.1,.34,M('#E6B53A',.3,metal=.9),seg=10,r2=.05); B.box((-3.6,BACK-.3,z0+1.96),(.12,.12,.03),M('#3A2A1E',.5),.01)       # trophy
        B.box((-3.05,BACK-.3,z0+2.08),(.3,.12,.15),M('#8A5A36',.5),.02); B.cyl((-3.15,BACK-.43,z0+2.08),.07,.01,M('#23252E',.5),rot=(R(90),0,0),seg=10)      # radio
    else:
        for k,c in enumerate(('#B8323A','#2F6B8A','#E6B53A','#3F7A3A')): B.box((-3.75+k*.13,BACK-.3,z0+2.13),(.05,.13,.2),M(c,.6),.01)
        B.cyl((-2.9,BACK-.3,z0+2.03),.11,.2,M('#B8553A',.7),seg=10,r2=.09); B.ico((-2.9,BACK-.3,z0+2.33),.2,M('#3F7A3A',.85,kind='leaves'),sub=1)
    # floor lamp + side things
    B.cyl((4.15,2.65,z0+.03),.2,.06,M('#3A2A1E',.5),seg=12); B.cyl((4.15,2.65,z0+.9),.025,1.75,M('#C9A24A',.3,metal=.8),seg=8); B.cyl((4.15,2.65,z0+1.95),.3,.42,M('#FFE9B8',.5,emit=1.6),seg=14,r2=.2)
    B.cyl((-4.15,2.6,z0+.3),.3,.6,M('#B8553A' if side=='P' else '#3A5A8A',.7),seg=12,r2=.24); B.ico((-4.15,2.6,z0+1.25),.55,M('#3F7A3A',.85,kind='leaves'),sc=(1,1,1.35),sub=1)
    bunting((-HW+.15,BACK-.35,z0+3.27),(HW-.15,BACK-.35,z0+3.27),19,p['bunt'],sag=.1)
    B.done('home'+side)
    F=fan(0,-.3,z0+h-.5)
    # lights
    bpy.ops.object.light_add(type='AREA',location=(0,-.4,z0+h-.12)); A=bpy.context.object; A.data.size=5.0; A.data.color=(1,.9,.76); A.data.energy=170
    try: A.data.use_shadow=True
    except Exception: pass
    tvl=point((0,-3.0,z0+1.35),190,(.62,.78,1.0),r=.6,shadow=False); tvl.data.specular_factor=0; lamp=point((4.0,2.4,z0+2.0),45,(1,.82,.55),r=.3,shadow=False)
    A.data.energy=215
    bpy.ops.object.light_add(type='AREA',location=(0,-5.6,z0+2.3),rotation=(R(90),0,0)); moon=bpy.context.object; moon.data.size=4.5; moon.data.color=(.5,.62,1.0); moon.data.energy=0
    try: moon.data.use_shadow=False
    except Exception: pass
    Hm=dict(side=side,z0=z0,main=A,tvl=tvl,lamp=lamp,fan=F,E=215.0,TVE=190.0,tv=None,moon=moon,MOONE=210.0)
    if tvwall: Hm['tv']=tvset(side,z0)
    return Hm
def tvset(side,z0=0.0):
    """front (camera-side) wall with the TV, only built for reverse shots. screen faces +y at y=-3.36"""
    p=PAL[side]; wm=M(shade(p['wall'],.97),.85,kind='wall',sc=.5); wood=M('#5A3A22',.45,kind='wood',sc=.6); bk=M('#101116',.35)
    B.box((0,-3.6,z0+HH/2),(HW,.1,HH/2),wm,0); B.box((0,-3.2,z0+.4),(2.0,.3,.4),wood,.03); B.box((0,-2.89,z0+.4),(1.9,.012,.3),M(shade('#5A3A22',1.2),.5,kind='wood'),.0)
    B.box((0,-3.42,z0+1.85),(1.62,.06,.95),bk,.04); B.box((0,-3.3,z0+.84),(.5,.16,.04),bk,.02)
    B.box((-1.45,-3.2,z0+.86),(.22,.14,.05),M('#23252E',.5),.02); B.box((1.3,-3.2,z0+.92),(.12,.12,.12),M(p['team'],.6),.02)
    for s in (-1,1): B.box((s*2.6,-3.3,z0+.95),(.3,.26,.95),M('#23252E',.6),.04); B.cyl((s*2.6,-3.03,z0+1.35),.2,.02,M('#3A3D47',.5),rot=(R(90),0,0),seg=16); B.cyl((s*2.6,-3.03,z0+.65),.2,.02,M('#3A3D47',.5),rot=(R(90),0,0),seg=16)
    bunting((-HW+.2,-3.45,z0+3.25),(HW-.2,-3.45,z0+3.25),15,p['bunt'],sag=.35)
    B.done('tvwall'+side)
    scr=empty((0,-3.355,z0+1.85)); G={}
    def grp(name,objs): G[name]=objs
    fld=M('#0E5A2A',.5,emit=.9); wht=M('#FFFFFF',.4,emit=2.0); yel=M('#FFD23F',.4,emit=2.2); red=M('#E8362C',.4,emit=1.8)
    bg_f=obox((0,0,0),(1.52,.008,.86),fld,0,scr); pitch=obox((0,.012,-.1),(.2,.004,.66),M('#B89A60',.6,emit=.35),0,scr)
    stripes=[obox((s*k*.52,.011,0),(.13,.003,.86),M('#127034',.5,emit=.9),0,scr) for k in (1,2) for s in (-1,1)]
    dim=[obox((0,.016,0),(1.52,.003,.86),M('#07301A',.5,emit=.32),0,scr),obox((0,.019,-.1),(.2,.002,.66),M('#4A3E28',.6,emit=.25),0,scr)]+[obox((s*k*.52,.019,0),(.13,.002,.86),M('#0A3A1E',.5,emit=.32),0,scr) for k in (1,2) for s in (-1,1)]
    bg_k=obox((0,.022,0),(1.52,.003,.86),M('#020203',.3),0,scr)
    live=[obox((-1.2,.02,.7),(.2,.004,.085),red,0,scr), text('LIVE',(-1.2,.03,.7),(0,1,0),.1,wht,ex=.002,parent=scr)]
    grp('field',[bg_f,pitch]+stripes+live); grp('dark',dim); grp('off',[bg_k])
    def page(name,lines):
        grp(name,[text(b,(0,.03,z),(0,1,0),s,(yel if c else wht),ex=.004,parent=scr) for b,z,s,c in lines])
    page('lastover',[('LAST OVER',.05,.42,1)]); page('oneball',[('1 BALL LEFT',.28,.3,0)]); page('tworuns',[('2 RUNS TO WIN',-.2,.3,1)])
    page('tied',[('MATCH TIED',.05,.38,0)]); page('super',[('SUPER',.3,.5,1),('OVER',-.28,.5,1)])
    dots=[oico((.42*math.sin(k*pi/4),.04,.42*math.cos(k*pi/4)),.1,M('#FFFFFF',.4,emit=2.0),scr,sub=2) for k in range(8)]; grp('spin',dots)
    for g in G.values():
        for o in g: o['sc']=tuple(o.scale)
    return dict(scr=scr,G=G,dots=dots)
def tv_show(TV,names,t=0.0,pop=None):
    """show only the listed groups. pop=(name,t0) scales that group in"""
    for n,objs in TV['G'].items():
        k=1.0 if n in names else 0.0
        if pop and n==pop[0] and k: k=min(1.0,max(0.0,(t-pop[1])/.14)); k=k*(1.18-.18*k) if k<1 else 1.0
        for o in objs: o.scale=tuple(v*k for v in o['sc'])
    if 'spin' in names:
        for i,o in enumerate(TV['dots']):
            q=(i-int(t*9))%8; o.scale=tuple(v*(1.0 if q==0 else .75 if q==7 else .5) for v in o['sc'])
def home_lights(Hm,t,power=1.0,tv=1.0,flick=1.0):
    """power: room electricity 0..1; tv: screen brightness 0..1; flick: 1 = live picture flicker, 0 = frozen picture"""
    s=Hm['z0']*3.1+(0 if Hm['side']=='P' else 1.7)
    Hm['main'].data.energy=Hm['E']*power; Hm['lamp'].data.energy=45*power; Hm['moon'].data.energy=Hm['MOONE']*(1-power)
    f=1.0-flick*(.22+.2*math.sin(t*19+s)*math.sin(t*6.7+s*2)+.1*math.sin(t*41+s))
    Hm['tvl'].data.energy=Hm['TVE']*tv*f
    Hm['fan'].rotation_euler[2]=t*9*power+s if power>0 else Hm['fan'].rotation_euler[2]
def home_world(res=None,samples=None):
    S,A,w_,bg_=setup_interior('ip_eve',room=(0,-.5,3.3),res=PCT,samples=SAMPLES,shadow_dist=18); A.data.energy=0
    return S
def dollhouse():
    """Lahore downstairs, Delhi upstairs. camera: (0,-16,UPZ/2+1.75) looking +y with a long lens"""
    P=home('P',0.0,front=-4.3); I=home('I',UPZ,front=-4.3); home_world()
    B.box((0,-4.33,UPZ-SLAB/2-.05),(HW+.2,.04,SLAB/2+.06),M('#5A3A2A',.7,emit=.25),0); B.done('slabface')
    return P,I
