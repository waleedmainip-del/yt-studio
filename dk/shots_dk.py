# Shots for "The Guy Who Couldn't Be Killed". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=98.6
SEQ=[('OPEN',0.0),('IDIOT',3.25),('NAME',6.15),('PLANE',7.8),('VOLC',9.45),('TRUCK',10.65),('STRONG',12.3),('LUCKY',13.88),('MISTAKE',16.15),
     ('WALK',18.95),('FALL',21.8),('BOOM',23.72),('SILENT',25.2),('CRAWL',27.72),('LOOK',30.3),('SONG',32.55),('AFTN',34.45),('BLACK',38.9),
     ('CARS',40.58),('CLOCK',42.08),('APPEAR',43.86),('RAISE',46.72),('TIMEUP',48.5),('DLOOK',50.62),('HUNGRY',51.9),('DISRESP',54.38),('DECIDE',57.05),
     ('SNAP',59.33),('METEOR',60.84),('UP',63.37),('ATDEATH',64.52),('PHONE',65.69),('CALL',67.86),('HIT',69.94),('EXPLO',71.08),('SILENCE',74.42),
     ('SMOKE',75.5),('RUBBLE',76.42),('SMILE',77.5),('FINALLY',78.86),('RING',81.08),('DOWN',82.72),('MOMID',83.93),('ANSWER',85.22),('MOMYELL',86.2),
     ('FROZE',87.93),('BEHIND',89.15),('FRIEND',91.98),('WHISPER',93.78),('OUT',97.6)]
DK=(0.0,5.0)        # Derek's mark on the north sidewalk in front of the deli / mover building
def hide(o): o.scale=(0,0,0)
def hideH(H): H['root'].scale=(0,0,0)
def tl(t,a,b): return ease((t-a)/max(1e-3,b-a))
def hand_loc(H,s=1): u=H['u']; return (s*.5*u,-.05*u,-2.08*u)
def in_hand(H,s,builder):
    e=empty(hand_loc(H,s),H['arm'][s]); builder(e); return e
def talk(H,t,t0,t1): mouth_talk(H,t,t0,t1)
def birds(n,seed,p0,p1,t0,dur,freeze=None):
    r=random.Random(seed); out=[]
    for i in range(n):
        e=empty((0,0,-80)); bm=M('#6E6E78',.6); wl=empty((0,0,0),e); wr=empty((0,0,0),e)
        obox((-.14,0,0),(.14,.05,.012),bm,0,wl); obox((.14,0,0),(.14,.05,.012),bm,0,wr); oico((0,0,0),.07,bm,e,sc=(.8,1.5,.8),sub=1)
        off=Vector((r.uniform(-3,3),r.uniform(-2,2),r.uniform(-1.5,1.5))); ph=r.uniform(0,6); dl=r.uniform(0,.4)
        def fn(o,t,wl=wl,wr=wr,off=off,ph=ph,dl=dl):
            tt=t if freeze is None else min(t,freeze); q=(tt-t0-dl)/dur
            o.location=Vector(p0).lerp(Vector(p1),max(0,min(1.5,q)))+off+Vector((0,0,1.5*max(0,q))); d=Vector(p1)-Vector(p0); o.rotation_euler=(0,0,math.atan2(-d.x,d.y))
            f=math.sin(tt*22+ph)*.9; wl.rotation_euler[1]=f; wr.rotation_euler[1]=-f
        fx.add(e,fn); out.append(e)
    return out

# ---------------------------------------------------------------- lighting mood blend
WORLD={}
def setup_world(mood,shadow=60):
    S,w,rp,bg=setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=shadow); WORLD.update(S=S,w=w,rp=rp,bg=bg,mood=mood)
    sc=bpy.context.scene; WORLD['mist']=None
    if sc.use_nodes:
        for n in sc.node_tree.nodes:
            if n.type=='MIX_RGB': WORLD['mist']=n
    return S
def blend_mood(a,b,k):
    A=MOODS[a]; Bm=MOODS[b]; S=WORLD['S']; rp=WORLD['rp']; bg=WORLD['bg']
    lc=lambda x,y: tuple(L(p,q,k) for p,q in zip(hexc(x),hexc(y)))
    S.data.energy=L(A['e'],Bm['e'],k); S.data.color=tuple(L(p,q,k) for p,q in zip(A['col'],Bm['col']))
    rp.color_ramp.elements[0].color=lc(A['bot'],Bm['bot']); rp.color_ramp.elements[1].color=lc(A['top'],Bm['top']); bg.inputs[1].default_value=L(A['sky'],Bm['sky'],k)
    nt=WORLD['w'].node_tree; mx=nt.nodes.get(WORLD['w']['cloudmix'])
    if mx: mx.inputs[7].default_value=lc(A.get('cloud','#FFFFFF'),Bm.get('cloud','#FFFFFF'))
    if WORLD['mist'] is not None: WORLD['mist'].inputs[2].default_value=lc(A['mist'],Bm['mist'])

# ---------------------------------------------------------------- hearts (extra lives)
HEARTG=M('#3FE07A',.3,emit=2.5); HEARTR=M('#8A8E96',.5); REDT=M('#FF3B2F',.3,emit=3.0)
def heart(parent,loc,mat,s=1.0):
    e=empty(loc,parent)
    for dx in (-.07,.07): oico((dx*s,0,.04*s),.085*s,mat,e,sc=(1,.45,1),sub=2)
    obox((0,0,-.05*s),(.085*s,.035*s,.085*s),mat,.03*s,e,rot=(0,R(45),0)); return e
def face_cam(e):
    cam=bpy.context.scene.camera; p=e.matrix_world.translation; d=cam.location-p; yaw=math.atan2(-d.x,d.y)+pi
    pr=e.parent.matrix_world.to_euler()[2] if e.parent else 0; e.rotation_euler=(0,0,yaw-pr)
def give_heart(H,mat=HEARTG,s=1.3):
    u=H['u']; e=heart(H['root'],(0,0,5.9*u),mat,s); H['heart']=e; return e
def derek_counter(H,n=47):
    u=H['u']; e=empty((0,0,6.1*u),H['root']); hb=heart(e,(-.2,0,0),HEARTR,1.4)
    crack=obox((-.2,-.05,.0),(.01,.01,.12),M('#1B1B22',.5),0,e,rot=(0,R(20),0))
    obox((.2,.03,0),(.3,.02,.16),M('#16171C',.5),.06,e); tx=text('x%d'%n,(.2,-.01,0),(0,-1,0),.25,M('#FF4A3A',.3,emit=2.5),ex=.01,parent=e); H['counter']=e; H['ctext']=tx; return e
def set_counter(H,n):
    H['ctext'].data.body='x%d'%n

# ---------------------------------------------------------------- crowd + traffic
CITY_TOPS=['#2F5EA8','#C8372D','#3A8A5A','#E8C24E','#F4F1EA','#22242B','#7448C2','#E07A3A','#5A8AB8','#B8D86A','#D45A8A','#8A6A4A']
def city_design(seed):
    c=design(seed); r=random.Random(seed*7+1)
    if r.random()<.35 and 'jacket' not in c: c['hoodie']=True; c['trim']=shade(c['top'],.8)
    if r.random()<.3: c['top']=r.choice(CITY_TOPS)
    return c
class Crowd:
    def __init__(s): s.p=[]
    def add(s,H,mode,**kw): d=dict(H=H,mode=mode); d.update(kw); s.p.append(d); return d
def make_crowd(n,seed,zones=((-30,30,4.9,7.0),(-30,30,-7.0,-4.9)),walk_frac=.6,avoid=(),hearts=False):
    r=random.Random(seed); C=Crowd()
    for i in range(n):
        for _ in range(30):
            z=r.choice(zones); x=r.uniform(z[0],z[1]); y=r.uniform(z[2],z[3])
            if not any(a[0]<x<a[1] and a[2]<y<a[3] for a in avoid): break
        D=city_design(seed*1000+i); w=r.random()<walk_frac; zz=.14 if abs(y)>4.5 else 0
        if w:
            dr=r.choice([-1,1]); H=avatar_dk((x,y,zz),90*dr,D,name='c%d_%d'%(seed,i)); C.add(H,'walk',x0=x,y=y,dir=dr,v=r.uniform(.9,1.25),xa=z[0],xb=z[1])
        else:
            rz=r.choice([0,180,90,-90,r.uniform(-180,180)]); H=avatar_dk((x,y,zz),rz,D,name='c%d_%d'%(seed,i)); C.add(H,'stand',rz=rz)
        if hearts: give_heart(H)
    return C
def upd_crowd(C,tg,freeze=None,look=None,react=0.0):
    for i,d in enumerate(C.p):
        H=d['H']
        if freeze is None or tg<freeze: blink(H,tg)
        if d['mode']=='walk':
            te=tg if freeze is None else min(tg,freeze); L_=d['xb']-d['xa']; x=d['xa']+((d['x0']-d['xa'])+d['dir']*d['v']*te)%L_
            H['root'].location[0]=x; H['root'].location[1]=d['y']; H['root'].rotation_euler[2]=R(90*d['dir'])
            walk(H,abs(d['v']*te),step=.55)
        else: stand(H,tg+i if freeze is None else min(tg,freeze)+i)
        if look is not None:
            look_at(H,look,1.0,maxyaw=80)
            if react>0:
                k=react*(.6+.4*((i*37)%10)/10); H['arm'][1].rotation_euler=(R(-25*k),0,R(10*k)); H['arm'][-1].rotation_euler=(R(-25*k),0,R(-10*k)); face(H,mouth='O',brow=.06*k,eyes=1+.25*k)
        elif d['mode']=='stand' and (freeze is None or tg<freeze): gaze_idle(H,tg+i*1.3)
        if 'heart' in H: face_cam(H['heart']); H['heart'].location[2]=5.9*H['u']+.05*math.sin(tg*3+i)
VCOL=['#F4F5FA','#C8372D','#2B58C9','#1A1A1E','#C9CED8','#35975A','#8A8E96']
def make_traffic(n,seed,lanes=((2.1,1),(-2.1,-1)),xr=(-70,70),kinds=('taxi','taxi','car','car','bus')):
    r=random.Random(seed); T=[]
    for i in range(n):
        y,dr=r.choice(lanes); k=r.choice(kinds); x=r.uniform(*xr)
        V=taxi((x,y,0),0,seed*50+i) if k=='taxi' else (bus((x,y,0),0) if k=='bus' else car((x,y,0),0,r.choice(VCOL),seed*50+i))
        if k!='bus': V['root'].scale=(1.15,1.15,1.15); V['r']*=1.15
        V['x0']=x; V['y']=y; V['dir']=dr; V['v']=r.uniform(6,9) if k!='bus' else 5.0; V['xr']=xr; V['kind']=k; T.append(V)
    return T
def upd_traffic(T,tg,freeze=None,brake=.6):
    for V in T:
        L_=V['xr'][1]-V['xr'][0]
        if freeze is None or tg<freeze: d=V['v']*tg
        else: d=V['v']*(freeze+brake*.5*(1-math.exp(-(tg-freeze)/max(.05,brake*.3))))
        x=V['xr'][0]+((V['x0']-V['xr'][0])+V['dir']*d)%L_
        drive(V,x,V['y'],0 if V['dir']>0 else 180,d)
def street(mood='city',crowd_n=24,traffic_n=10,seed=1,avoid=(),hearts=False,walk_frac=.6,zones=None,lanes=((2.1,1),(-2.1,-1))):
    city(1); B.done('city'); setup_world(mood)
    C=make_crowd(crowd_n,seed,zones=zones or ((-35,35,4.9,7.0),(-35,35,-7.0,-4.9)),walk_frac=walk_frac,avoid=tuple(avoid),hearts=hearts)
    T=make_traffic(traffic_n,seed,lanes=lanes) if traffic_n else []
    return C,T

# ---------------------------------------------------------------- FX helpers
SMOKE=M('#9A9496',.95,spec=.05); SMOKED=M('#5A5458',.95,spec=.05); DUST=M('#C9B89E',.95,spec=.05); EMBER=M('#FF8A3A',.3,emit=8.0)
def smoke_column(loc,t0,t1,n=14,size=.6,rise=2.5,mat=None,seed=4,life=2.4,spread=.6):
    r=random.Random(seed)
    for i in range(n):
        st=t0+(t1-t0)*i/n; puff((loc[0]+r.uniform(-spread,spread),loc[1]+r.uniform(-spread,spread),loc[2]),st,size=size,n=3,col=mat or SMOKE,rise=rise,life=life,seed=seed*31+i)
def embers(center,radius,t0,t1,n=30,seed=5):
    sparkles(center,radius,t0,t1,n,.04,seed,1.2,mat=EMBER)
def debris(center,t0,n=24,seed=3,spd=6.0,mats=None,size=(.08,.25)):
    r=random.Random(seed); spec=[]
    for i in range(n):
        s_=r.uniform(*size); o=obox((0,0,-50),(s_,s_*r.uniform(.5,1),s_*r.uniform(.4,.9)),(mats or [M('#7A6A5E',.9),M('#9C4A36',.85)])[i%2],.02)
        a=r.uniform(0,6.28); v=r.uniform(.4,1)*spd
        spec.append((o,Vector(center),Vector((math.cos(a)*v*.5,math.sin(a)*v*.5,r.uniform(.6,1.3)*v)),Vector((r.uniform(-9,9),r.uniform(-9,9),r.uniform(-9,9)))))
    ballistic(spec,t0)
def ring_wave(center,t0,dur=.8,r1=30,mat=None):
    o=ocyl(center,1.0,.4,mat or M('#FFD9A0',.4,emit=4.0,alpha=.6),None,rot=(0,0,0),seg=40,r2=1.0); o.scale=(0,0,0)
    def fn(o,t):
        q=(t-t0)/dur
        if q<0 or q>1: o.scale=(0,0,0); return
        s=r1*ease_out(q); o.scale=(s,s,1-q)
    fx.add(o,fn); return o

# ---------------------------------------------------------------- Derek helpers
def derek(loc,rz,counter=True,n=47):
    H=avatar_dk(loc,rz,DEREK,name='derek')
    if counter: derek_counter(H,n)
    return H
def upd_counter(H):
    if 'counter' in H: face_cam(H['counter']); H['counter'].location[2]=6.1*H['u']+.04*math.sin(TNOW[0]*3)
def lie(H,k,face_down=True,base_z=None):
    # rotate whole body to lying (pivot at feet), k 0..1
    u=H['u']; a=R(90*k)*(1 if face_down else -1); H['root'].rotation_euler[0]=a
    H['root'].location[2]=(H['z0'] if base_z is None else base_z)+.008+.25*u*math.sin(abs(a))
def crawl(H,t,k):
    lie(H,k*.78)
    for s in (1,-1):
        ph=math.sin(t*6+(0 if s>0 else pi)); H['arm'][s].rotation_euler=(R(-150-25*ph*k),0,R(s*8)); H['leg'][s].rotation_euler[0]=R(20*ph*k)
    H['head'].rotation_euler[0]=R(-40*k)
def piano_hang(x=0.0,y=5.35,z=9.2):
    rope=mover_rig(x,1,7.5,z+2.6); P=piano((x,y,z),180); return P,rope
def movers_window(x=0.0,z=11.0):
    out=[]
    for i,dx in enumerate((-.7,.7)):
        H=avatar_dk((x+dx,7.25,z-1.8),0,MOVER,name='mover%d'%i); out.append(H)
    return out

def OPEN_():
    C,T=street(crowd_n=36,traffic_n=14,seed=1,hearts=True)
    BI=birds(6,2,(-40,-6,16),(30,20,22),0.0,6.0)
    def upd(t):
        upd_crowd(C,t+2); upd_traffic(T,t+2); q=ease(t/DUR)
        camset(LV((-34,-1.8,17),(-15,-2.6,3.4),q),LV((0,3,3),(-6,4.6,2.6),q),24,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_

def IDIOT_():
    C,T=street(crowd_n=22,traffic_n=8,seed=2,hearts=True,avoid=((-12,-2,4.6,7.2),),lanes=((-2.1,-1),))
    Dk=derek((-9.4,5.0,.14),90,n=45); peel=obox((-7.9,5.0,.16),(.08,.14,.012),M('#F2D14A',.5),.01)
    sp=sparkles((-7.6,5.0,2.4),.4,.9,1.4,16,.05,7,.4)
    def upd(t):
        upd_crowd(C,t+5); upd_traffic(T,t+5); blink(Dk,t); upd_counter(Dk)
        tf=.55; tu=1.35
        if t<tf: walk_path(Dk,[(-9.4,5.0),(-7.9,5.0)],t,0,tf+.05,step=.5,ease_out_=.01); set_counter(Dk,45 if t<.3 else 46)
        else:
            k=tl(t,tf,tf+.18)*(1-tl(t,tu,tu+.35)); Dk['root'].location[0]=-7.9+.3*k; legs0(Dk)
            lie(Dk,k,face_down=False); arms(Dk,-150*k,0,30*k,-150*k,0,-30*k); face(Dk,mouth='O' if k>.2 and t<tu else 'grin',eyes=1+.2*k)
            set_counter(Dk,46 if t<tu else 47)
            if t>tu+.35: idle(Dk,t); Dk['arm'][1].rotation_euler=(R(-60*tl(t,tu+.4,tu+.6)),0,R(10)); Dk['root'].rotation_euler[2]=R(90-60*tl(t,tu+.3,tu+.6))
        camset((-4.4,2.4,1.7),(-7.5,5.0,1.7),30,4.0)
    return dict(upd=upd)
SHOTS['IDIOT']=IDIOT_

def NAME_():
    C,T=street(crowd_n=16,traffic_n=6,seed=3,hearts=True,avoid=((-8,-2,4.6,7.2),),lanes=((-2.1,-1),))
    Dk=derek((-5.0,5.1,.14),-20)
    def upd(t):
        upd_crowd(C,t+8); upd_traffic(T,t+8); stand(Dk,t); blink(Dk,t); upd_counter(Dk); face(Dk,mouth='grin',brow=.04)
        w=math.sin(t*12)*tl(t,.15,.4); Dk['arm'][1].rotation_euler=(R(-165),0,R(20+18*w)); look_at(Dk,(-3.6,2.6,1.7),.8)
        camset((-3.7,1.6,1.8),(-5.0,5.1,1.8),32,4.0)
    return dict(upd=upd)
SHOTS['NAME']=NAME_

def PLANE_():
    crash_field(); B.done('field'); setup_world('field')
    Dk=derek((1.5,3.5,0),-10,counter=False); r=random.Random(3)
    smoke_column((-1,9,2),-2.5,DUR,16,2.2,4.5,SMOKED,2,3.2,1.2); smoke_column((5,10,1.5),-2.5,DUR,14,1.8,4.0,SMOKE,3,3.0,.8); embers((0,7.5,1.0),2.0,0,DUR,30,4)
    puff((1.5,3.2,.6),0,size=.5,n=6,col=SMOKE,rise=.8,life=1.0,seed=5)
    def upd(t):
        walk_path(Dk,[(1.5,3.5),(1.2,1.2)],t,0,DUR,step=.45,mood=6); blink(Dk,t)
        face(Dk,mouth='grin' if t>.8 else 'strain',eyes=.85); k=math.sin(t*14)*tl(t,.9,1.1)
        Dk['arm'][-1].rotation_euler=(R(-40+20*k),0,R(-20)); Dk['arm'][1].rotation_euler=(R(-30),0,R(15))
        camset((2.8,-3.4,1.5),(1.3,2.2,1.6),30,5.0)
    return dict(upd=upd)
SHOTS['PLANE']=PLANE_

def VOLC_():
    pool=volcano_set(); B.done('volc'); setup_world('lava'); point((0,4,1.5),220,(1,.5,.25),r=2.0)
    Dk=derek((0,4,-2.2),0,counter=False)
    flame(lambda t: Vector((0,4,Dk['root'].location[2]+2.25)),0,DUR,.14,3,(0,0,1)); smoke_column((0,4,2.6),0,DUR,8,.25,1.5,SMOKED,6,1.2,.15)
    embers((0,4,.6),4.5,0,DUR,40,8)
    def upd(t):
        k=ease_out(tl(t,0,.55)); Dk['root'].location[2]=L(-2.2,.008,k); stand(Dk,t); Dk['root'].location[2]=L(-2.2,.008,k); blink(Dk,t)
        th=tl(t,.6,.8); Dk['arm'][1].rotation_euler=(R(-95*th),0,R(10*th)); face(Dk,mouth='grin',eyes=1.0,brow=.04)
        camset((0,-.6,1.5),(0,4,1.4),32,5.0)
    return dict(upd=upd)
SHOTS['VOLC']=VOLC_

def TRUCK_():
    C,T=street(crowd_n=14,traffic_n=0,seed=4,avoid=((8,18,4.4,7.2),))
    Tk=truck((-30,-2.1,0),0); Dk=derek((10.0,-.9,0),180,counter=False); hit=.5; vx=24.0
    def upd(t):
        upd_crowd(C,t+12,look=(10,-1,1) if t>hit else None,react=.5*tl(t,hit,hit+.3))
        x=10-3.95-(hit-t)*vx if t<hit else 10-3.95+(t-hit)*vx*math.exp(-(t-hit)*1.6); drive(Tk,x,-2.1,0,x+30)
        blink(Dk,t)
        if t<hit: walk_path(Dk,[(10.0,.6),(10.0,-.9)],t,-.6,hit,step=.5); face(Dk,mouth='smile')
        else:
            tt=t-hit; z=max(0,6.0*tt-4.9*tt*tt); Dk['root'].location=(10+6.0*min(tt,1.05),-.9+1.5*min(tt,1.05),z+.008); legs0(Dk)
            sp=min(1,tt/1.05); Dk['root'].rotation_euler=(R(-360*sp*1.0),R(30*sp),R(180)); arms(Dk,-160,0,40,-150,0,-40); face(Dk,mouth='O',eyes=1.3)
            if tt>1.1:
                q=tl(tt,1.15,1.5); Dk['root'].rotation_euler=(R(-90*(1-q)),0,R(180)); Dk['root'].location[2]=.008+.2*(1-q); arms(Dk,-90*(1-q),0,10,-20,0,-10); face(Dk,mouth='grin')
        SHAKE[0]=.06*math.exp(-max(0,t-hit)*6) if t>hit else 0
        camset((18.5,3.6,2.0),(12.0,-.6,1.9),22,16)
    return dict(upd=upd)
SHOTS['TRUCK']=TRUCK_

def STRONG_():
    C,T=street(crowd_n=10,traffic_n=6,seed=5,avoid=((-10,-4,4.6,7.2),),lanes=((-2.1,-1),))
    Dk=derek((-7.0,5.1,.14),-15,counter=False); jar=in_hand(Dk,1,lambda e: (ocyl((0,0,0),.07,.16,M('#9ACB6A',.15,spec=.8,alpha=.7),e,rot=(0,0,0),seg=16),ocyl((0,0,.09),.072,.04,M('#C8372D',.4),e,rot=(0,0,0),seg=16)))
    def upd(t):
        upd_crowd(C,t+15); upd_traffic(T,t+15); stand(Dk,t); blink(Dk,t)
        hp=root_mat(Dk)@Vector((0,-1.1*Dk['u'],3.6*Dk['u'])); w=math.sin(t*40)*.02
        arm_to(Dk,1,(hp.x+.05,hp.y,hp.z+w),1.0,base=(0,0,0)); arm_to(Dk,-1,(hp.x-.02,hp.y,hp.z+.18+w),1.0,base=(0,0,0))
        st=tl(t,.2,.6); face(Dk,mouth='strain' if t<1.15 else 'frown',brow=.04 if t<1.15 else .05,brow_r=14,eyes=.75 if t<1.15 else 1.0)
        Dk['head'].rotation_euler=(R(10),0,R(4*math.sin(t*30)*st*(t<1.15)))
        camset((-6.0,2.2,1.8),(-7.0,5.1,1.75),32,4.0)
    return dict(upd=upd)
SHOTS['STRONG']=STRONG_

def LUCKY_():
    C,T=street(crowd_n=10,traffic_n=6,seed=6,avoid=((-10,-4,4.6,7.2),),lanes=((-2.1,-1),))
    Dk=derek((-6.4,5.0,.14),-10,counter=False)
    cone=in_hand(Dk,1,lambda e: ocyl((0,0,.0),.06,.22,M('#D9A066',.7),e,rot=(R(180),0,0),seg=10,r2=.005))
    sc=oico((0,0,0),.1,M('#F4A6C0',.6),None,sub=2); spl=ocyl((-6.6,4.8,.15),.18,.01,M('#F4A6C0',.6),None,rot=(0,0,0),seg=16); spl.scale=(0,0,0)
    tf=.75
    def upd(t):
        upd_crowd(C,t+18); upd_traffic(T,t+18); stand(Dk,t); blink(Dk,t)
        Dk['arm'][1].rotation_euler=(R(-100),0,R(18)); cp=cone.matrix_world.translation
        if t<tf: sc.location=cp+Vector((0,0,.17)); sc.scale=(1,1,1); face(Dk,mouth='grin',brow=.04); look_at(Dk,cp,.7)
        else:
            tt=t-tf; z=max(.18,cp.z+.17-4.9*tt*tt); sc.location=(cp.x-.2*tt,cp.y-.3*tt,z); sc.scale=(1,1,1) if z>.18 else (0,0,0)
            if z<=.18: spl.scale=(1,1,1)
            look_at(Dk,(-6.6,4.8,.2),.9*tl(t,tf+.2,tf+.6)); face(Dk,mouth='frown' if t>tf+.5 else 'O',brow=.05,brow_r=16,eyes=1.0)
        camset((-7.6,2.3,1.7),(-6.4,5.0,1.65),32,4.0)
    return dict(upd=upd)
SHOTS['LUCKY']=LUCKY_

def MISTAKE_():
    C,T=street('city',crowd_n=8,traffic_n=6,seed=7,avoid=((-12,2,4.4,7.4),),lanes=((-2.1,-1),),walk_frac=0)
    Dk=derek((-4.5,5.0,.14),90,counter=False); De=avatar_dk((-6.6,6.2,.14),90,DEATH,name='death'); sc_=De['props']['scythe']
    bend=(.35,1.6); sw=(.55,.95)
    def upd(t):
        upd_crowd(C,t+21); upd_traffic(T,t+21); blink(Dk,t); stand(Dk,t)
        k=tl(t,bend[0],bend[0]+.2)*(1-tl(t,bend[1],bend[1]+.25))
        Dk['root'].rotation_euler[0]=R(55*k); Dk['root'].location[2]=.148-.25*k; Dk['head'].rotation_euler[0]=R(30*k); arms(Dk,-60*k,0,0,-60*k,0,0); face(Dk,mouth='smile')
        stand(De,t); s=tl(t,sw[0],sw[1]); De['arm'][-1].rotation_euler=(R(-60-60*math.sin(pi*s)),0,R(-90*s+20)); De['root'].rotation_euler[2]=R(90-30*s)
        face(De,mouth='frown' if t>1.3 else 'flat',brow=-.03,brow_r=-20 if t<1.3 else 12)
        if t>1.5: De['arm'][1].rotation_euler=(R(-150*tl(t,1.5,1.8)),0,R(-30)); De['head'].rotation_euler[0]=R(25*tl(t,1.5,1.8))
        camset((-4.6,.4,1.7),(-5.4,5.4,1.6),24,5.0)
    return dict(upd=upd)
SHOTS['MISTAKE']=MISTAKE_

# ---------------------------------------------------------------- piano sequence
def WALK_():
    C,T=street(crowd_n=18,traffic_n=0,seed=8,avoid=((-12,3,4.6,7.2),(-12,8,-7.4,-4.4))); P,rope=piano_hang(); Mv=movers_window()
    Dk=derek((-9,5.0,.14),90,counter=False)
    def upd(t):
        upd_crowd(C,t+24); blink(Dk,t); walk_path(Dk,[(-9,5.0),(-2.2,5.0)],t,0,DUR+.6,step=.55,ease_out_=.05); face(Dk,mouth='smile',brow=.03)
        P['root'].rotation_euler[2]=R(180+4*math.sin(t*1.3)); P['root'].location[2]=9.2+.05*math.sin(t*2)
        for i,H in enumerate(Mv): stand(H,t+i); face(H,mouth='strain'); arms(H,-80,0,10,-80,0,-10)
        x=Dk['root'].location[0]; camset((x+1.2,-2.6,1.3),(x+2.4,5.0,4.4),20,16)
    return dict(upd=upd)
SHOTS['WALK']=WALK_
def FALL_():
    C,T=street(crowd_n=12,traffic_n=6,seed=9,avoid=((-6,3,4.6,7.2),),lanes=((-2.1,-1),)); P,rope=piano_hang(); Mv=movers_window()
    Dk=derek((-.1,5.0,.14),90,counter=False); ph=in_hand(Dk,1,lambda e: phone_obj(e,(0,-.06,.05),1.0)); snap=.35; T_imp=23.8-T0
    def upd(t):
        upd_crowd(C,t+27); upd_traffic(T,t+27); blink(Dk,t); stand(Dk,t); Dk['arm'][1].rotation_euler=(R(-75),0,R(10)); look_at(Dk,ph.matrix_world.translation,.8); face(Dk,mouth='smile')
        if t<snap: z=9.2
        else: tt=(t-snap)/(T_imp-snap); z=L(9.2,.0,tt*tt)
        P['root'].location=(0,4.85,max(0,z)); P['root'].rotation_euler=(R(6*tl(t,snap,T_imp)),0,R(180+8*tl(t,snap,T_imp)))
        rope.scale=(1,1,1 if t<snap else .4)
        for i,H in enumerate(Mv):
            stand(H,t+i); k=tl(t,snap,snap+.25); arms(H,-80-60*k,0,10+25*k,-80-60*k,0,-10-25*k); face(H,mouth='O' if t>snap else 'strain',eyes=1+.3*k,brow=.06*k)
        camset((1.6,2.5,.45),(0,4.9,6.2),18,16)
    return dict(upd=upd)
SHOTS['FALL']=FALL_
def BOOM_():
    C,T=street(crowd_n=18,traffic_n=6,seed=10,avoid=((-5,5,4.6,7.2),)); Pb=piano((0,4.9,.15),190,broken=True)
    imp=23.8-T0; puff((0,4.9,.6),imp,size=1.6,n=14,col=DUST,rise=1.4,life=2.2,seed=3); puff((0,4.9,.3),imp,size=1.0,n=10,col=DUST,rise=.4,life=1.6,drift=(2,-2,0),seed=4)
    debris((0,4.9,.8),imp,30,5,5.0,[M('#141218',.2,spec=.9),M('#F4F1EA',.3)],(.03,.12))
    def upd(t):
        upd_crowd(C,t+30,look=(0,4.9,.5) if t>imp else None,react=.6*tl(t,imp,imp+.25)); upd_traffic(T,t+30,freeze=imp+30)
        Pb['root'].scale=(1,1,1) if t>imp else (0,0,0); SHAKE[0]=.09*math.exp(-max(0,t-imp)*5) if t>imp else 0
        camset((-4.6,.2,2.0),(0,4.9,1.2),24,16)
    return dict(upd=upd)
SHOTS['BOOM']=BOOM_
def SILENT_():
    C,T=street(crowd_n=26,traffic_n=0,seed=11,avoid=((-3,3,4.6,7.2),),walk_frac=0); Pb=piano((0,4.9,.15),190,broken=True)
    tx=taxi((3.5,2.1,0),180); smoke_column((0,4.9,.3),-2,DUR,10,.6,1.0,DUST,9,2.0,.6)
    def upd(t):
        upd_crowd(C,40,look=(0,4.9,.5),react=.55)
        q=ease(t/DUR); camset(LV((-9.5,-2.6,3.4),(-8.2,-2.0,3.0),q),(0,5.0,1.0),26,16)
    return dict(upd=upd)
SHOTS['SILENT']=SILENT_
def CRAWL_():
    C,T=street(crowd_n=12,traffic_n=0,seed=12,avoid=((-4,4,4.6,7.2),),walk_frac=0); Pb=piano((0,4.9,.15),190,broken=True)
    Dk=derek((.2,4.95,.14),-90,counter=False); smoke_column((0,4.9,.3),-2,DUR,8,.5,.8,DUST,9,2.0,.5)
    def upd(t):
        upd_crowd(C,40,look=(1,4.7,.5),react=.6); blink(Dk,t)
        if t<1.9:
            q=tl(t,.1,1.9); Dk['root'].location[0]=L(-.2,1.5,q); Dk['root'].rotation_euler[2]=R(-90); crawl(Dk,t,1.0); face(Dk,mouth='strain',eyes=.8)
        else:
            q=tl(t,1.9,2.5); Dk['root'].location[0]=1.5; legs0(Dk); lie(Dk,.78*(1-q)); arms(Dk,-150*(1-q),0,0,-150*(1-q),0,0); Dk['head'].rotation_euler[0]=R(-40*(1-q)); face(Dk,mouth='flat',eyes=.9)
        camset((3.0,2.5,.55),(.6,4.95,.5),28,5.0)
    return dict(upd=upd)
SHOTS['CRAWL']=CRAWL_
def LOOK_():
    C,T=street(crowd_n=12,traffic_n=0,seed=12,avoid=((-4,4,4.6,7.2),),walk_frac=0); Pb=piano((0,4.9,.15),190,broken=True)
    Dk=derek((1.5,4.95,.14),-90,counter=False); smoke_column((0,4.9,.3),-2,DUR,8,.5,.8,DUST,9,2.0,.5)
    for k in range(6): obox((1.5+random.Random(k).uniform(-.3,.3),5.5+random.Random(k+9).uniform(-.2,.2),2.0+random.Random(k).uniform(0,.6)),(.04,.04,.04),DUST,.01,None)
    def upd(t):
        upd_crowd(C,40,look=(1.5,4.95,1.5),react=.6); stand(Dk,t); blink(Dk,t)
        look_at(Dk,(0,4.9,.2),.9*tl(t,.1,.6)); Dk['head'].rotation_euler[1]=R(8*tl(t,1.0,1.4)); face(Dk,mouth='flat',eyes=.85,brow=.0)
        camset((3.6,2.3,1.65),(.7,4.95,1.0),26,5.0)
    return dict(upd=upd)
SHOTS['LOOK']=LOOK_
def SONG_():
    C,T=street(crowd_n=10,traffic_n=0,seed=12,avoid=((-4,4,4.6,7.2),),walk_frac=0); Pb=piano((0,4.9,.15),190,broken=True)
    Dk=derek((1.5,4.95,.14),-110,counter=False); key=obox((0,0,-50),(.015,.07,.015),M('#F4F1EA',.3),0)
    def upd(t):
        stand(Dk,t); blink(Dk,t); look_at(Dk,(-.2,2.5,1.8),.5); face(Dk,brow=-.01,brow_r=-4,eyes=.72); talk(Dk,t,32.63-T0,33.79-T0)
        camset((.4,2.7,1.8),(1.45,4.95,1.95),45,2.8)
    return dict(upd=upd)
SHOTS['SONG']=SONG_

# ---------------------------------------------------------------- Death's office
def office():
    st=M('#2A2630',.9,kind='concrete',sc=.8); wd=M('#3A2418',.5,kind='wood',sc=.6); pap=M('#E8DFC8',.7); red=M('#A8202A',.6)
    B.box((0,0,-.05),(8,8,.05),M('#1E1A22',.85,kind='tile',h2='#16131A',sc=1.2),0); B.box((0,4,3),(8,.2,3),st,0); B.box((-4.5,0,3),(.2,8,3),st,0); B.box((4.5,0,3),(.2,8,3),st,0)
    B.box((0,1.0,.82),(1.6,.75,.06),wd,.02)
    for dx in (-1.45,1.45):
        for dy in (.35,1.65): B.box((dx,dy,.4),(.08,.08,.4),wd,.01)
    for k in range(6): B.box((-3.6+k*.7,3.6,1.2),(.32,.3,1.2),M('#3A3640',.6,metal=.3),.02); B.box((-3.6+k*.7,3.28,1.8),(.12,.02,.03),M('#8A8E96',.3,metal=.8),0)
    for k in range(40): B.box((random.Random(k).uniform(-3.8,3.8),3.4,random.Random(k+5).uniform(2.6,5.2)),(.22,.25,.03),pap,.0,rot=(0,random.Random(k).uniform(-.3,.3),0))
    for x in (-.95,1.2):
        B.cyl((x,1.3,.95),.05,.22,M('#F4F1EA',.6),seg=10); B.ico((x,1.3,1.1),.04,M('#FFB23A',.3,emit=12.0),sub=1)
    B.box((-1.4,.9,.92),(.18,.12,.04),M('#1B1B22',.4),.01); B.cyl((-1.4,.9,1.0),.03,.12,M('#1B1B22',.4),seg=8)
    fold=empty((.1,.7,.89)); obox((0,0,0),(.42,.3,.02),red,.01,fold); obox((0,0,.022),(.38,.27,.005),pap,0,fold)
    text('DEREK',(0,-.05,.03),(0,0,1),.12,M('#1B1B22',.5),ex=.003,parent=fold).rotation_euler=(0,0,0)
    for k in range(9): obox((-.28+k*.05,.12,.028),(.006,.05,.002),M('#1B1B22',.5),0,fold,rot=(0,0,R(10 if k%5==4 else 0)))
    text('OVERDUE',(.1,-.17,.03),(0,0,1),.07,M('#C8372D',.4),ex=.003,parent=fold).rotation_euler=(0,0,R(-12))
    point((0,1.0,1.6),260,(1,.65,.35),r=.3); point((0,-2,3.5),220,(.6,.5,1.0),r=1.5); point((-2.5,3,4),150,(1,.3,.3),r=1.0)
    return fold
def AFTN_():
    fold=office(); B.done('office'); setup_world('doom',shadow=15); WORLD['S'].data.energy=.15
    De=avatar_dk((.1,2.05,0),0,DEATH,name='death'); stamp=in_hand(De,1,lambda e: (obox((0,0,0),(.07,.07,.05),M('#3A2418',.5),.02,e),obox((0,0,-.08),(.09,.09,.03),M('#A8202A',.5),.01,e)))
    for o in bpy.data.objects:
        if o.type=='LIGHT' and o.data.type=='POINT': o.data.shadow_soft_size=.3
    def upd(t):
        stand(De,t); De['root'].location[2]=.008; blink(De,t)
        sl=tl(t,.6,.75)*(1-tl(t,.85,1.1)); De['arm'][1].rotation_euler=(R(-60-50*(1-sl)*tl(t,.2,.6)),0,R(14))
        look_at(De,(.1,.7,.9),.8*(1-tl(t,2.6,3.2))); face(De,mouth='flat' if t<2.6 else 'smirk',brow=-.04,brow_r=-24)
        if t>2.6: De['root'].location[2]=.008+.0; De['arm'][-1].rotation_euler=(R(-40*tl(t,2.6,3.0)),0,R(-10))
        SHAKE[0]=.02 if .74<t<.9 else 0
        q=ease(t/DUR); camset(LV((.2,-2.6,1.55),(.15,-1.2,1.75),q),LV((.1,1.2,1.3),(.1,2.0,2.4),q),30,4.0)
    return dict(upd=upd)
SHOTS['AFTN']=AFTN_

# ---------------------------------------------------------------- the day turns to night
def doom_street(seed,crowd_n=18,traffic_n=8,freeze=None,avoid=(),mood='doom',lanes=((-2.1,-1),)):
    C,T=street(mood,crowd_n=crowd_n,traffic_n=traffic_n,seed=seed,avoid=((-6,6,4.4,7.4),)+tuple(avoid),lanes=lanes); return C,T
def lamps_on(k):
    for o in bpy.data.objects:
        if o.get('lamp'): o.data.energy=160*k
def add_lamp_lights():
    for x in range(-64,65,11):
        for s in (-1,1):
            xx=x+(2 if s>0 else -3)
            if s>0 and -15<xx<11: continue
            l=point((xx,s*3.7,4.35),0,(1,.82,.55),r=.2,shadow=False); l['lamp']=1
def BLACK_():
    C,T=doom_street(31,22,0,mood='city'); add_lamp_lights()
    Dk=derek(( .5,5.0,.14),0,counter=False); cl=street_clock(-3.2,4.9)
    def upd(t):
        k=tl(t,.15,1.3); blend_mood('city','doom',k); lamps_on(tl(t,.9,1.2))
        upd_crowd(C,t+40,look=(0,0,30) if t>.6 else None,react=.4*tl(t,.6,1.0)); upd_traffic(T,t+40)
        stand(Dk,t); blink(Dk,t); look_at(Dk,(-6,-10,25),.8*tl(t,.5,1.0)); face(Dk,mouth='o',eyes=1.1); clock_set(cl,15*3600+t)
        q=ease(t/DUR); camset(LV((-9,-3.4,1.4),(-9.6,-3.6,1.6),q),(-1,4.5,6.5),20,16)
    return dict(upd=upd)
SHOTS['BLACK']=BLACK_
def CARS_():
    C,T=doom_street(32,24,0); add_lamp_lights(); lamps_on(1)
    tx=taxi((-30,-2.1,0),0); fr=.55; BI=birds(5,7,(-6,-1,6),(10,4,9),-1,4.0,freeze=fr)
    def upd(t):
        upd_crowd(C,t+44,freeze=44+fr)
        x=-14+11.0*min(t,fr)+(11.0*.25*(1-math.exp(-(t-fr)/.25)) if t>fr else 0); drive(tx,x,-2.1,0,x+14)
        tx['root'].rotation_euler[1]=R(-3*math.exp(-max(0,t-fr)*6)*(t>fr))
        camset((-1.5,-5.4,1.3),(-6.5,-.5,1.4),22,16)
    return dict(upd=upd)
SHOTS['CARS']=CARS_
def CLOCK_():
    C,T=doom_street(33,10,0); add_lamp_lights(); lamps_on(1); cl=street_clock(-3.2,4.9); fr=.55
    def upd(t):
        upd_crowd(C,40); ct=15*3600+50+(min(t,fr) if t<fr else fr)*60
        clock_set(cl,ct); s=math.exp(-max(0,t-fr)*12)*(t>fr); cl['head'].rotation_euler=(0,R(1.5*s*math.sin(t*60)),0)
        q=ease(t/DUR); camset(LV((-2.6,2.0,4.3),(-2.7,2.4,4.4),q),(-3.2,4.9,4.6),32,5.6)
    return dict(upd=upd)
SHOTS['CLOCK']=CLOCK_
DE=(0.0,2.4)    # where Death appears, facing Derek
def APPEAR_():
    C,T=doom_street(34,14,0); add_lamp_lights(); lamps_on(1)
    Dk=derek((0,5.0,.14),0,counter=False); De=avatar_dk((DE[0],DE[1],-3.0),180,DEATH,name='death')
    smoke_column((0,2.4,.1),0,1.8,22,.9,2.2,SMOKED,11,2.2,.9); embers((0,2.4,.4),1.2,.2,2.4,24,3); glo=point((0,2.0,.4),0,(1,.25,.2),r=.5)
    def upd(t):
        upd_crowd(C,40); blink(Dk,t); stand(Dk,t); look_at(Dk,(0,2.4,2.6),.6); face(Dk,mouth='flat',eyes=1.0)
        glo.data.energy=400*tl(t,.1,.6); k=ease(tl(t,.3,2.0)); De['root'].location[2]=L(-3.0,.008,k); stand(De,t); De['root'].location[2]=L(-3.0,.008,k)
        e=tl(t,1.8,2.2); [setattr(o,'scale',(e,e,e)) for o in De['xeyes']]; face(De,mouth='flat',brow=-.04,brow_r=-26)
        camset((2.7,4.5,1.9),(0,2.4,2.1),22,5.6,focus=(0,2.4,2.6))
    return dict(upd=upd)
SHOTS['APPEAR']=APPEAR_
def death_pair(seed=35,crowd_n=12):
    C,T=doom_street(seed,crowd_n,0); add_lamp_lights(); lamps_on(1)
    Dk=derek((0,5.0,.14),0,counter=False); De=avatar_dk((DE[0],DE[1],0),180,DEATH,name='death')
    point((-2.2,3.7,3.2),140,(1,.75,.6),r=1.0,shadow=False); point((2.4,3.0,2.6),90,(.7,.6,1.0),r=1.0,shadow=False)
    return C,Dk,De
def RAISE_():
    C,Dk,De=death_pair(35)
    def upd(t):
        upd_crowd(C,40); stand(De,t); blink(De,t,force=False); k=ease(tl(t,.1,.7))
        arm_to(De,1,(-1.2,2.6,5.0),k,base=(0,0,0)); face(De,mouth='flat',brow=-.04,brow_r=-28); stand(Dk,t)
        for o in De['xeyes']: o.scale=(1+.4*k,1+.4*k,1)
        camset((.9,3.9,.6),(0,2.4,2.6),20,16)
    return dict(upd=upd)
SHOTS['RAISE']=RAISE_
def TIMEUP_():
    C,Dk,De=death_pair(35,8)
    def upd(t):
        stand(De,t); talk(De,t,48.58-T0,50.65-T0); face(De,brow=-.05,brow_r=-30)
        f=1.4+.3*math.sin(t*20)*(48.58-T0<t<50.65-T0)
        for o in De['xeyes']: o.scale=(f,f,1)
        q=ease(t/DUR); camset(LV((0.05,4.1,2.7),(0.05,3.85,2.75),q),(0,2.4,2.85),38,2.8)
    return dict(upd=upd)
SHOTS['TIMEUP']=TIMEUP_
def DLOOK_():
    C,Dk,De=death_pair(35,8)
    def upd(t):
        stand(Dk,t); blink(Dk,t,force=(.55<t<.68)); face(Dk,mouth='flat',eyes=.95,brow=.0); look_at(Dk,(0,2.4,2.8),.7)
        camset((.5,3.7,2.1),(0,5.0,1.95),36,2.8)
    return dict(upd=upd)
SHOTS['DLOOK']=DLOOK_
def HUNGRY_():
    C,Dk,De=death_pair(36,10)
    def upd(t):
        stand(Dk,t); stand(De,t); blink(Dk,t); talk(Dk,t,51.98-T0,54.36-T0); face(Dk,brow=.05,brow_r=12,eyes=1.1)
        k=tl(t,.1,.4); Dk['arm'][1].rotation_euler=(R(-60*k),0,R(-35*k)); r_=math.sin(t*9)*.3
        Dk['arm'][-1].rotation_euler=(R(-40-20*r_),0,R(-30)) if t<1.4 else (R(-120),0,R(-60*tl(t,1.4,1.7)))
        face(De,mouth='flat',brow=.04,brow_r=10); look_at(De,(0,5,2),.6); De['head'].rotation_euler[1]=R(8*tl(t,1.0,1.6))
        camset((-4.4,3.6,1.9),(0,3.7,2.0),24,5.6)
    return dict(upd=upd)
SHOTS['HUNGRY']=HUNGRY_
def DISRESP_():
    C,Dk,De=death_pair(36,8)
    puff((0,2.5,3.5),.8,size=.25,n=6,col=SMOKE,rise=.8,life=1.2,seed=3); puff((0,2.5,3.5),1.6,size=.25,n=6,col=SMOKE,rise=.8,life=1.2,seed=4)
    def upd(t):
        stand(De,t); k=tl(t,.2,.8); face(De,mouth='strain' if t<1.6 else 'shout',brow=-.05,brow_r=-30*k,eyes=1.0)
        tw=math.sin(t*50)*.03*k; De['head'].rotation_euler=(R(4),R(2*math.sin(t*40)*k),0); De['props']['scythe'].rotation_euler=(R(3*math.sin(t*45)*k),0,0)
        for o in De['xeyes']: o.scale=(1+.8*k+tw,1+.8*k+tw,1)
        q=ease(t/DUR); camset(LV((0.25,4.2,2.85),(0.2,3.85,2.9),q),(0,2.4,2.85),38,2.8)
    return dict(upd=upd)
SHOTS['DISRESP']=DISRESP_
def DECIDE_():
    C,Dk,De=death_pair(37,10)
    sc=De['props']['scythe']
    def upd(t):
        stand(De,t); stand(Dk,t); face(De,mouth='frown',brow=-.05,brow_r=-26); look_at(De,(0,5,2.4),.8)
        th=tl(t,.3,.6); De['arm'][-1].rotation_euler=(R(-90*th*(1-tl(t,.6,.9))),0,R(-30*th))
        if t>.55:
            if sc.parent: mw=sc.matrix_world.copy(); sc.parent=None; sc.matrix_world=mw; sc['p0']=tuple(sc.location); sc['r0']=tuple(sc.rotation_euler)
            tt=t-.55; p0=Vector(sc['p0']); sc.location=(p0.x-2.2*min(tt,.6),p0.y-.6*min(tt,.6),max(.1,p0.z-4.9*tt*tt)); sc.rotation_euler=(sc['r0'][0],sc['r0'][1]+R(-80*min(1,tt/.5)),sc['r0'][2])
        k=tl(t,1.1,1.6); De['arm'][1].rotation_euler=(R(-100*k),0,R(40*k)); De['arm'][-1].rotation_euler=(R(-100*k),0,R(-40*k)) if t>1.1 else De['arm'][-1].rotation_euler
        camset((-3.0,4.4,1.2),(0,2.4,2.3),24,16)
    return dict(upd=upd)
SHOTS['DECIDE']=DECIDE_
def SNAP_():
    C,Dk,De=death_pair(37,6); hide(De['props']['scythe'])
    snap=59.85-T0; sparkles((0,0,0),.01,0,0,1)
    sp=[]
    def upd(t):
        stand(De,t); arm_to(De,1,(-.55,3.6,4.0),1.0,base=(0,0,0)); face(De,mouth='smirk',brow=-.04,brow_r=-24)
        hp=hand_pos(De,1) if 'hand_pos' in globals() else None
        if t>snap and not sp:
            p=De['arm'][1].matrix_world@Vector((.5*De['u'],-.05*De['u'],-2.1*De['u'])); sp.append(1)
            puff(p,snap,size=.25,n=6,col=M('#FF3B2F',.3,emit=6.0),rise=.3,life=.5,seed=2)
        SHAKE[0]=.025*math.exp(-max(0,t-snap)*8) if t>snap else 0
        camset((-1.6,4.6,2.6),(-.5,3.2,3.6),32,4.0)
    return dict(upd=upd)
SHOTS['SNAP']=SNAP_

# ---------------------------------------------------------------- meteor
MET_T0=61.25; MET_IMP=70.5; MET_P0=Vector((75,6,92)); MET_P1=Vector((0,2.2,0))
def meteor(scale=1.0):
    root=empty((0,0,-500)); rk=M('#3A2A26',.9,kind='concrete',sc=.4); lav=M('#FF6A1A',.4,emit=7.0)
    oico((0,0,0),7.0*scale,rk,root,sc=(1,.9,1.05),sub=2,smooth=False)
    r=random.Random(3)
    for k in range(18):
        a=r.uniform(0,6.28); b=r.uniform(-1.2,1.2); d=6.8*scale
        oico((d*math.cos(a)*math.cos(b),d*math.sin(a)*math.cos(b),d*math.sin(b)),r.uniform(.6,1.6)*scale,lav if k%3==0 else rk,root,sub=1,smooth=False)
    glow_=oico((0,0,0),9.5*scale,M('#FF7A2A',.4,emit=3.0,alpha=.35),root,sub=3)
    trail=[ocyl((0,0,0),(7.5-k*1.1)*scale,14*scale,M(['#FFD27A','#FF9A3A','#FF6A1A','#C83A1A'][k%4],.4,emit=6.0-k,alpha=.55-k*.08),root,rot=(0,0,0),seg=20,r2=.5*scale) for k in range(4)]
    for k,o in enumerate(trail): o.location=(0,0,9*scale+k*9*scale)
    L_=point((0,0,0),0,(1,.55,.25),r=6.0); L_.parent=root
    return dict(root=root,trail=trail,light=L_)
def met_pos(tg):
    f=max(0,min(1,(tg-MET_T0)/(MET_IMP-MET_T0))); g=f**2.6
    return MET_P0.lerp(MET_P1,g), f
def met_upd(Mt,tg,show=True,light=4e5):
    p,f=met_pos(tg); app=tl(tg,MET_T0,MET_T0+.6)
    if not show or tg<MET_T0 or tg>MET_IMP+.02: Mt['root'].location=(0,0,-500); Mt['light'].data.energy=0; return p,f
    Mt['root'].location=p; d=(MET_P0-MET_P1).normalized(); Mt['root'].rotation_euler=d.to_track_quat('Z','Y').to_euler()
    Mt['root'].scale=(app,app,app); Mt['root'].rotation_euler.rotate_axis('Z',tg*.6)
    Mt['light'].data.energy=light*app*(.5+f)
    for k,o in enumerate(Mt['trail']): o.scale=(1+.08*math.sin(tg*20+k),1+.08*math.sin(tg*20+k),1+.15*math.sin(tg*13+k))
    return p,f
def METEOR_():
    C,Dk,De=death_pair(38,16); hide(De['props']['scythe']); Mt=meteor(1.8)
    puff((26,46,150),MET_T0-T0,size=14,n=10,col=M('#3A1A1A',.95),rise=0,life=1.6,seed=4)
    def upd(t):
        tg=T0+t; met_upd(Mt,tg); stand(Dk,t); stand(De,t); upd_crowd(C,40)
        camset((-3.0,-1.4,.4),(26,4,32),16,16)
    return dict(upd=upd)
SHOTS['METEOR']=METEOR_
def sky_glow(k):
    WORLD['S'].data.energy=MOODS['doom']['e']+2.0*k; WORLD['S'].data.color=(1,.5,.25)
def UP_():
    C,Dk,De=death_pair(38,6); hide(De['props']['scythe']); Mt=meteor()
    def upd(t):
        tg=T0+t; p,f=met_upd(Mt,tg); sky_glow(f); stand(Dk,t); blink(Dk,t); Dk['root'].rotation_euler[2]=R(45); look_at(Dk,(40,5,60),1.0,maxyaw=80,maxpitch=45); face(Dk,mouth='o',eyes=1.15,brow=.05)
        camset((2.3,3.4,1.45),(0,5.0,2.05),34,4.0)
    return dict(upd=upd)
SHOTS['UP']=UP_
def ATDEATH_():
    C,Dk,De=death_pair(38,6); hide(De['props']['scythe']); Mt=meteor()
    def upd(t):
        tg=T0+t; p,f=met_upd(Mt,tg); sky_glow(f); stand(Dk,t); stand(De,t); blink(Dk,t)
        k=ease(tl(t,.15,.55)); look_at(Dk,(1-k)*Vector((40,5,60))+k*Vector((0,2.4,2.9)),1.0,maxyaw=80,maxpitch=45); face(Dk,mouth='flat',eyes=1.0)
        face(De,mouth='smirk',brow=-.03,brow_r=-20)
        camset((-3.4,3.9,1.9),(0,3.7,2.3),26,5.0)
    return dict(upd=upd)
SHOTS['ATDEATH']=ATDEATH_
def PHONE_():
    C,Dk,De=death_pair(38,6); hide(De['props']['scythe']); Mt=meteor(); ph=in_hand(Dk,1,lambda e: phone_obj(e,(0,-.06,.05),1.2))
    def upd(t):
        tg=T0+t; p,f=met_upd(Mt,tg); sky_glow(f); stand(Dk,t); blink(Dk,t); k=ease(tl(t,.2,1.8))
        pk=root_mat(Dk)@Vector((.25*Dk['u'],-.7*Dk['u'],2.5*Dk['u'])); hp=root_mat(Dk)@Vector((.3*Dk['u'],-1.2*Dk['u'],3.7*Dk['u']))
        arm_to(Dk,1,pk.lerp(hp,k),1.0,base=(0,0,0)); ph.scale=(1,1,1) if k>.02 else (0,0,0); face(Dk,mouth='flat',eyes=.9); look_at(Dk,ph.matrix_world.translation,.7*k)
        camset((1.5,3.4,1.65),(0,4.9,1.7),32,4.0)
    return dict(upd=upd)
SHOTS['PHONE']=PHONE_
def CALL_():
    C,Dk,De=death_pair(38,6); hide(De['props']['scythe']); Mt=meteor(); ph=in_hand(Dk,1,lambda e: phone_obj(e,(0,-.06,.05),1.2))
    def upd(t):
        tg=T0+t; p,f=met_upd(Mt,tg); sky_glow(f); stand(Dk,t); stand(De,t); blink(Dk,t)
        ear=root_mat(Dk)@Vector((1.0*Dk['u'],-2.0*Dk['u'],4.2*Dk['u'])); arm_to(Dk,1,ear,1.0,base=(0,0,0))
        k=tl(t,.1,.35); Dk['arm'][-1].rotation_euler=(R(-110*k),0,R(-20*k)); talk(Dk,t,67.92-T0,69.5-T0); face(Dk,brow=.03,eyes=.95)
        look_at(Dk,(0,2.4,2.8),.6); face(De,mouth='O' if t>.8 else 'flat',brow=.05,brow_r=14,eyes=1.1); look_at(De,(0,5,2.1),.6)
        camset((-3.4,3.0,1.0),(3,3.8,4.6),18,16)
    return dict(upd=upd)
SHOTS['CALL']=CALL_
def HIT_():
    C,T=doom_street(39,10,0); add_lamp_lights(); lamps_on(1); Mt=meteor()
    Dk=derek((0,5.0,.14),0,counter=False); De=avatar_dk((DE[0],DE[1],0),180,DEATH,name='death'); hide(De['props']['scythe'])
    imp=MET_IMP-T0; fb=oico((0,2.2,0),1.0,M('#FFF2C8',.3,emit=30.0),None,sub=3); fb.scale=(0,0,0)
    def upd(t):
        tg=T0+t; p,f=met_upd(Mt,tg); sky_glow(f); stand(Dk,t); stand(De,t); upd_crowd(C,40)
        if t>imp: s=30*ease_out(tl(t,imp,imp+.5)); fb.scale=(s,s,s*.8)
        bpy.context.scene.view_settings.exposure=4.0*tl(t,imp,imp+.35)
        SHAKE[0]=.25*tl(t,imp-.3,imp)
        camset((-34,-3.2,3.0),(0,3,9),20,16)
    return dict(upd=upd)
SHOTS['HIT']=HIT_
def EXPLO_():
    C,T=doom_street(40,0,0); fb=oico((0,2.2,0),1.0,M('#FFB23A',.4,emit=14.0),None,sub=3); core=oico((0,2.2,0),1.0,M('#FFF2C8',.3,emit=30.0),None,sub=3)
    ring_wave((0,2.2,.3),.25,1.4,60,M('#FFD9A0',.4,emit=5.0,alpha=.5))
    debris((0,2.2,1.0),.2,40,8,14.0,[M('#5A4A40',.9),M('#9C4A36',.85)],(.2,.6))
    for k in range(10): puff((random.Random(k).uniform(-12,12),random.Random(k+3).uniform(-4,6),2),.6+k*.12,size=random.Random(k).uniform(5,8),n=4,col=M('#4A4044',.95),rise=6,life=3.5,seed=k)
    def upd(t):
        e=1-tl(t,.35,1.6); bpy.context.scene.view_settings.exposure=4.0*e+.0
        s=L(30,48,ease_out(tl(t,0,2.0))); fb.scale=(s,s,s*.7); fb.location=(0,2.2,4+6*tl(t,0,3))
        c=s*.55*(1-tl(t,1.0,2.6)); core.scale=(c,c,c*.7)
        blend_mood('doom','ash',tl(t,1.2,3.2)); SHAKE[0]=.35*math.exp(-t*1.2)
        camset((-40,-1.5,4.0),(0,3,10),22,16)
    return dict(upd=upd)
SHOTS['EXPLO']=EXPLO_

# ---------------------------------------------------------------- aftermath
def aftermath(seed=50):
    C,T=street('ash',crowd_n=0,traffic_n=0,seed=seed)
    r=random.Random(seed); rub=[M('#5E5450',.9,kind='concrete',sc=.5),M('#8A5A44',.9,kind='wall'),M('#3A3438',.9)]
    B.cyl((0,2.2,.01),7.5,.04,M('#1E1A1A',.95),seg=40); B.cyl((0,2.2,.03),4.5,.05,M('#2A1A16',.9),seg=40)
    for k in range(70):
        a=r.uniform(0,6.28); d=r.uniform(4.5,9.5); B.box((math.cos(a)*d,2.2+math.sin(a)*d*.8,.15),(r.uniform(.15,.7),r.uniform(.15,.5),r.uniform(.08,.35)),r.choice(rub),.03,rot=(r.uniform(-.4,.4),r.uniform(-.4,.4),r.uniform(0,6)))
    for k in range(40):
        B.box((r.uniform(-25,25),r.uniform(-4.2,7),.1),(r.uniform(.1,.4),r.uniform(.1,.3),r.uniform(.05,.2)),r.choice(rub),.02,rot=(0,0,r.uniform(0,6)))
    for x in (-6,5,9): B.box((x,2.2+r.uniform(-3,3),.6),(1.2,.8,.6),r.choice(rub),.1,rot=(r.uniform(-.3,.3),r.uniform(-.3,.3),r.uniform(0,6)))
    tx=taxi((-8,-1.0,.0),130); tx['root'].rotation_euler=(R(180),R(8),R(130)); tx['root'].location[2]=1.75
    Pb=piano((7,-1.5,.15),40,broken=True); B.done('rubble')
    for k,(x,y) in enumerate(((-4,4.5),(5,6),(8,-2),(-9,1),(12,5))): smoke_column((x,y,.3),-3,12,12,1.0,3.5,SMOKE if k%2 else SMOKED,20+k,3.0,.5); flame(lambda t,x=x,y=y: Vector((x,y,.3)),-1,30,.35,k,(0,0,1))
    embers((0,2.2,1.5),9.0,-1,12,60,9)
    return C
def SILENCE_():
    aftermath()
    def upd(t): q=ease(t/DUR); camset(LV((-14,-3.6,2.6),(-13.6,-3.5,2.65),q),(0,3,1.5),22,16)
    return dict(upd=upd)
SHOTS['SILENCE']=SILENCE_
def SMOKE_():
    aftermath(); smoke_column((-2,-1,.2),-3,3,10,1.4,2.0,SMOKE,30,3.0,1.5)
    def upd(t): q=ease(t/DUR); camset(LV((-4.5,-3.4,1.2),(-4.0,-3.2,1.4),q),(0,1.5,1.4),30,5.6)
    return dict(upd=upd)
SHOTS['SMOKE']=SMOKE_
def RUBBLE_():
    aftermath()
    def upd(t): q=ease(t/DUR); camset(LV((5.5,-3.6,.9),(3.0,-3.6,.9),q),LV((7,-1.5,.3),(4.5,0,.4),q),26,5.6)
    return dict(upd=upd)
SHOTS['RUBBLE']=RUBBLE_
DA=(0.0,1.6)    # Death in the aftermath, facing the camera (-y)
def death_after(phone=False,lit=False):
    aftermath(); De=avatar_dk((DA[0],DA[1],0),0,DEATH,name='death'); hide(De['props']['scythe'])
    ph=phone_obj(None,(.9,.7,.16),1.6,lit=lit); ph.rotation_euler=(R(-90),0,R(20)) if not phone else ph.rotation_euler
    return De,ph
def SMILE_():
    De,ph=death_after(); puff((0,1.6,1.0),-1,size=1.4,n=8,col=SMOKE,rise=1.0,life=2.2,seed=2)
    def upd(t):
        stand(De,t); blink(De,t); k=tl(t,.3,.8); face(De,mouth='smirk' if k<.5 else 'grin',brow=.03*k,brow_r=-10+8*k,eyes=1.0-.15*k)
        q=ease(t/DUR); camset(LV((.4,-2.6,2.4),(.3,-2.0,2.55),q),(0,1.6,2.75),34,4.0)
    return dict(upd=upd)
SHOTS['SMILE']=SMILE_
def FINALLY_():
    De,ph=death_after()
    def upd(t):
        blink(De,t); face(De,mouth='smile',brow=.04,brow_r=6,eyes=.8)
        if t<1.0:
            stand(De,t); k=math.sin(t*16)*tl(t,.1,.25)*(1-tl(t,.8,1.0)); hp=root_mat(De)@Vector((0,-1.2*De['u'],3.0*De['u']))
            arm_to(De,1,(hp.x+.1+.08*k,hp.y,hp.z),1.0,base=(0,0,0)); arm_to(De,-1,(hp.x-.1-.08*k,hp.y,hp.z),1.0,base=(0,0,0))
        else: walk_path(De,[(DA[0],DA[1]),(DA[0]-3.5,DA[1]+.6)],t,1.0,DUR+.8,step=.5,ease_out_=.05)
        camset((1.4,-3.6,1.9),(-.5,1.8,2.3),28,5.6)
    return dict(upd=upd)
SHOTS['FINALLY']=FINALLY_
def RING_():
    De,ph=death_after(lit=True); De['root'].location=(-2.2,2.1,0)
    def upd(t):
        walk_path(De,[(-1.4,1.9),(-2.6,2.2)],t,-.5,.6,step=.5,ease_out_=.4); stand(De,t) if t>.6 else None; blink(De,t)
        if t>.9: look_at(De,ph.matrix_world.translation,.8*tl(t,.9,1.3)); De['root'].rotation_euler[2]=R(lerp_angle(-104,150,tl(t,.7,1.3)))
        v=.02*math.sin(t*70)*(int(t*3)%2==0); ph.location=(.9+v,.7,.16); ph.rotation_euler=(R(-90),0,R(20+4*math.sin(t*70)))
        camset((1.9,-.9,.4),(-.4,1.9,1.1),22,2.8,focus=(.9,.7,.2))
    return dict(upd=upd)
SHOTS['RING']=RING_
def DOWN_():
    De,ph=death_after(lit=True); De['root'].location=(.3,1.3,0); De['root'].rotation_euler[2]=R(45)
    point((1.6,-.4,1.2),120,(1,.8,.7),r=.5,shadow=False)
    def upd(t):
        stand(De,t); blink(De,t); look_at(De,(.9,.7,.16),1.0,maxpitch=45); face(De,mouth='flat',brow=.03,brow_r=8)
        v=.02*math.sin(t*70)*(int(t*3)%2==0); ph.location=(.9+v,.7,.16)
        camset((1.45,.35,.3),(.3,1.3,2.9),22,16)
    return dict(upd=upd)
SHOTS['DOWN']=DOWN_
def MOMID_():
    De,ph=death_after(lit=True)
    sc_=bpy.data.objects[ph['scr']]; tx=text('MOM',(0,-.012*1.6,.05*1.6),(0,-1,0),.035*1.6,M('#16171C',.4),ex=.0,parent=ph)
    hb=heart(ph,(0,-.013*1.6,-.02*1.6),M('#FF3B5A',.3,emit=2.5),.25); hb.rotation_euler=(0,0,0)
    tx2=text('calling...',(0,-.012*1.6,-.07*1.6),(0,-1,0),.016*1.6,M('#16171C',.4),ex=.0,parent=ph)
    ph.rotation_euler=(R(-90),0,0); ph.location=(.9,.7,.16)
    def upd(t):
        v=.006*math.sin(t*70)*(int(t*3)%2==0); ph.location=(.9+v,.7,.16)
        camset((.9,.68,.55),(.9,.7,.16),40,2.0)
    return dict(upd=upd)
SHOTS['MOMID']=MOMID_
def ANSWER_():
    De,ph=death_after(lit=True); De['root'].location=(.3,1.3,0); De['root'].rotation_euler[2]=R(25)
    def upd(t):
        stand(De,t); blink(De,t); k=ease(tl(t,.05,.5)); g=ease(tl(t,.5,.9))
        hp=Vector((.9,.7,.16)); ear=root_mat(De)@Vector((1.15*De['u'],-2.1*De['u'],3.9*De['u']))
        if t<.5: arm_to(De,1,hp,k,base=(0,0,0)); De['root'].rotation_euler[0]=R(25*k); look_at(De,hp,1.0,maxpitch=45)
        else:
            De['root'].rotation_euler[0]=R(25*(1-g)); arm_to(De,1,ear,1.0,base=(0,0,0)); look_at(De,(0,-4,2.5),.5*g)
            if ph.parent is None: ph.parent=De['arm'][1]; ph.matrix_parent_inverse.identity(); ph.location=hand_loc(De,1); ph.rotation_euler=(0,0,R(90))
        face(De,mouth='flat',brow=.04,brow_r=8)
        camset((1.6,-2.4,1.8),(.4,1.3,2.6),28,4.0)
    return dict(upd=upd)
SHOTS['ANSWER']=ANSWER_
def MOMYELL_():
    kitchen(); B.done('kitchen'); setup_world('day',shadow=15); point((0,0,2.9),250,(1,.95,.85),r=1.0); point((-2.5,0,1.9),120,(.8,.9,1),r=.8)
    Mo=avatar_dk((.9,.6,0),-20,MOM,name='mom'); ph=in_hand(Mo,-1,lambda e: phone_obj(e,(0,-.06,.05),1.2))
    lid=ocyl((1.0,-.2,.97),.23,.02,M('#C9CED8',.3,metal=.8),None,rot=(0,0,0),seg=16)
    def upd(t):
        stand(Mo,t); blink(Mo,t,force=False); ear=root_mat(Mo)@Vector((-.85*Mo['u'],-2.0*Mo['u'],4.1*Mo['u'])); arm_to(Mo,-1,ear,1.0,base=(0,0,0))
        talk(Mo,t,86.28-T0,87.65-T0); face(Mo,brow=-.04,brow_r=-26,eyes=1.15); k=tl(t,.05,.2)
        Mo['arm'][1].rotation_euler=(R(-60-30*math.sin(t*14)*k),0,R(25)); Mo['head'].rotation_euler=(R(-8*k),R(3*math.sin(t*30)*k),0)
        lid.location[2]=.97+.02*abs(math.sin(t*40))*k; SHAKE[0]=.02*k*(t<1.5)
        camset((.55,-1.75,1.55),(.9,.6,1.7),30,4.0)
    return dict(upd=upd)
SHOTS['MOMYELL']=MOMYELL_
def death_phone(De):
    ph=in_hand(De,1,lambda e: phone_obj(e,(0,-.06,.05),1.6)); ear=root_mat(De)@Vector((1.15*De['u'],-2.1*De['u'],3.9*De['u'])); return ph
def FROZE_():
    De,ph0=death_after(); hide(ph0); ph=death_phone(De); drop=obox((0,0,-50),(.03,.01,.05),M('#9FD8FF',.1,spec=1.0,alpha=.8),.02)
    def upd(t):
        legs0(De); idle(De,0); ear=root_mat(De)@Vector((1.15*De['u'],-2.1*De['u'],3.9*De['u'])); arm_to(De,1,ear,1.0,base=(0,0,0))
        face(De,mouth='strain',brow=.06,brow_r=14,eyes=.6)
        for o in De['xeyes']: o.scale=(.55,.55,1)
        hp=De['head'].matrix_world@Vector((.45*De['u'],-.66*De['u'],(1.0-.5*tl(t,.3,1.2))*De['u'])); drop.location=hp
        camset((.15,-1.0,2.75),(0,1.6,2.75),38,2.8)
    return dict(upd=upd)
SHOTS['FROZE']=FROZE_
def BEHIND_():
    De,ph0=death_after(); hide(ph0); ph=death_phone(De)
    Dk=derek((-1.6,3.2,0),150,counter=True,n=47); sw=in_hand(Dk,1,lambda e: sandwich(e,(0,-.08,.05),1.4))
    for o in bpy.data.objects:
        if o.name.startswith('derek') or (o.parent and o.parent.name.startswith('derek')): pass
    def upd(t):
        legs0(De); idle(De,0); ear=root_mat(De)@Vector((1.15*De['u'],-2.1*De['u'],3.9*De['u'])); arm_to(De,1,ear,1.0,base=(0,0,0)); face(De,mouth='strain',brow=.06,brow_r=14)
        for o in De['xeyes']: o.scale=(.55,.55,1)
        walk_path(Dk,[(-2.8,4.2),(-1.35,2.7)],t,0,1.3,step=.5); stand(Dk,t) if t>1.3 else None; blink(Dk,t); upd_counter(Dk)
        if t>1.0: Dk['root'].rotation_euler[2]=R(lerp_angle(math.degrees(Dk['root'].rotation_euler[2]),20,tl(t,1.0,1.4)))
        bite=(int(t*1.6)%2==0) and t>1.4; Dk['arm'][1].rotation_euler=(R(-110 if bite else -70),0,R(20)); face(Dk,mouth='grin' if not bite else 'o',brow=.03)
        set_counter(Dk,47 if t<2.0 else 48)
        camset((-.9,-2.3,2.1),(-.85,2.4,2.15),26,4.0,focus=(-1.3,2.7,2.0) if t>1.0 else (0,1.6,2.7))
    return dict(upd=upd)
SHOTS['BEHIND']=BEHIND_
def FRIEND_():
    De,ph0=death_after(); hide(ph0); ph=death_phone(De)
    Dk=derek((-1.05,1.9,0),30,counter=True,n=48); sw=in_hand(Dk,-1,lambda e: sandwich(e,(0,-.08,.05),1.4))
    def upd(t):
        legs0(De); idle(De,0); ear=root_mat(De)@Vector((1.15*De['u'],-2.1*De['u'],3.9*De['u'])); arm_to(De,1,ear,1.0,base=(0,0,0)); face(De,mouth='flat',brow=.05,brow_r=16,eyes=.8)
        stand(Dk,t); blink(Dk,t); upd_counter(Dk); talk(Dk,t,92.06-T0,93.36-T0); face(Dk,brow=.04)
        sh=root_mat(De)@Vector((-.9*De['u'],0,4.0*De['u'])); arm_to(Dk,1,sh,1.0,base=(0,0,0)); look_at(Dk,ph.matrix_world.translation,.7)
        Dk['root'].rotation_euler[1]=R(6)
        camset((-.9,-2.9,2.15),(-.7,1.7,2.15),27,4.0)
    return dict(upd=upd)
SHOTS['FRIEND']=FRIEND_
def WHISPER_():
    De,ph0=death_after(); hide(ph0); ph=death_phone(De)
    Dk=derek((-1.05,1.9,0),30,counter=False); sw=in_hand(Dk,-1,lambda e: sandwich(e,(0,-.08,.05),1.4))
    def upd(t):
        legs0(De); idle(De,0); ear=root_mat(De)@Vector((1.15*De['u'],-2.1*De['u'],3.9*De['u'])); arm_to(De,1,ear,1.0,base=(0,0,0))
        k=tl(t,.2,1.5); face(De,brow=.05,brow_r=18*k,eyes=1.0-.35*k); talk(De,t,95.57-T0,97.43-T0)
        for o in De['xeyes']: o.scale=(1-.5*k,1-.5*k,1)
        De['head'].rotation_euler=(R(10*k),R(-6*k),0); stand(Dk,t); blink(Dk,t); face(Dk,mouth='grin')
        sh=root_mat(De)@Vector((-.9*De['u'],0,4.0*De['u'])); arm_to(Dk,1,sh,1.0,base=(0,0,0))
        q=ease(t/DUR); camset(LV((-.3,-1.8,2.7),(-.2,-1.1,2.75),q),(-.15,1.6,2.7),34,2.8)
    return dict(upd=upd)
SHOTS['WHISPER']=WHISPER_
def OUT_():
    setup_world('doom'); WORLD['bg'].inputs[1].default_value=0; WORLD['S'].data.energy=0
    if WORLD['mist'] is not None: WORLD['mist'].inputs[2].default_value=(0,0,0,1)
    def upd(t): camset((0,0,1),(0,10,1),30,16)
    return dict(upd=upd)
SHOTS['OUT']=OUT_
