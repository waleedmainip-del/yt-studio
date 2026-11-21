# Shots for "The Pindi Boys". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=60.4
SEQ=[('OPEN', 0.0), ('FIVE', 1.07), ('TWELVE', 3.36), ('MEET', 5.36), ('MISSION', 7.86), ('GHOOM', 11.57), ('PETROLQ', 14.02), ('QUIET', 15.51), ('ARGUE', 17.79), ('DRIVE', 20.9), ('INSIDE', 22.15), ('CHIPS', 26.57), ('DE', 28.17), ('PAISE', 28.81), ('STATION', 30.22), ('FIVEHUND', 32.01), ('ENNA', 34.71), ('FERRARI', 37.41), ('LATER', 40.18), ('MOM', 42.84), ('BAS', 44.93), ('TEPETROL', 47.2), ('LOOKS', 48.06), ('POINT', 49.79), ('FAIZ', 51.92), ('KEYS', 54.26), ('PAIDAL', 56.0), ('WALK', 57.01)]
def hide(o): o.scale=(0,0,0)
def tl(t,a,b): return ease((t-a)/max(1e-3,b-a))
def hand_loc(H,s=1): u=H['u']; return (s*.5*u,-.05*u,-2.08*u)
def in_hand(H,s,builder):
    e=empty(hand_loc(H,s),H['arm'][s]); builder(e); return e
def talk(H,t,g0,g1,**kw): mouth_talk(H,t,g0-T0,g1-T0,**kw)
def seat(H,t,h=.58):
    sit(H,1,h,legs=90); blink(H,t); H['root'].rotation_euler[0]=0; H['root'].rotation_euler[1]=R(1.0)*math.sin(t*.8+H['seed'])
def setup_world(mood,shadow=55):
    S,w,rp,bg=setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=shadow); return S
def ui_world():
    setup_render('morning_s',res=PCT,samples=SAMPLES,mist=False); bpy.context.scene.world.node_tree.nodes['Background'].inputs[1].default_value=.0
HEARTM=M('#FF4F7A',.3,emit=2.2)
def heart(parent,loc,mat=HEARTM,s=1.0):
    e=empty(loc,parent)
    for dx in (-.07,.07): oico((dx*s,0,.04*s),.085*s,mat,e,sc=(1,.45,1),sub=2)
    obox((0,0,-.05*s),(.085*s,.035*s,.085*s),mat,.03*s,e,rot=(0,R(45),0)); return e
def face_cam(e):
    cam=bpy.context.scene.camera; p=e.matrix_world.translation; d=cam.location-p; e.rotation_euler=(0,0,math.atan2(-d.x,d.y)+pi-(e.parent.matrix_world.to_euler()[2] if e.parent else 0))
def hearts(src_fn,t0,t1,n=8,seed=1,size=1.0,rise=1.6):
    r=random.Random(seed)
    for i in range(n):
        h=heart(None,(0,0,-60),s=size*r.uniform(.7,1.2)); ts=t0+(t1-t0)*i/n+r.uniform(0,.1); dx=r.uniform(-.35,.35); ph=r.uniform(0,6)
        def fn(o,t,ts=ts,dx=dx,ph=ph):
            q=(t-ts)/1.3
            if q<=0 or q>=1: o.scale=(0,0,0); return
            p=Vector(src_fn(t)); o.location=(p.x+dx+.12*math.sin(q*6+ph),p.y,p.z+rise*q); k=min(1,q*5)*(1-q)**.5; o.scale=(k,k,k); face_cam(o)
        fx.add(h,fn)
def bubble(body,loc,t0,size=.2,col='#16171C',bg='#FFFFFF',w=None,dur=99):
    e=empty(loc); w=w or (len(body)*size*.34+.2); obox((0,.03,0),(w,.02,size*.9),M(bg,.5,emit=.5),size*.5,e); text(body,(0,0,0),(0,-1,0),size,M(col,.5,emit=.2),ex=.005,parent=e); e.scale=(0,0,0)
    def fn(o,t):
        k=pop(t-t0) if t0<=t<t0+dur else 0; o.scale=(k,k,k); face_cam(o)
    fx.add(e,fn); return e

# ---------------------------------------------------------------- people
SKL=['#C98F62','#B97A4E','#D9A074','#A86F47','#E0AE84','#C08A5C']; HRL=['#15120F','#1E1A18','#2A1B14','#3B2314']
MENC=['#F4F1EA','#BFD6E8','#2A2C34','#6B7A4A','#C9B48A','#8FB8D8','#A8C8B0','#D2473A','#27365A','#E6A31C']
WOMC=['#E8554D','#CF3F78','#F2C14E','#35975A','#7448C2','#16909E','#F28AA0','#2B58C9','#B8D86A']
def person(seed,young=False):
    r=random.Random(seed*13+7); c=dict(skin=r.choice(SKL),hair=r.choice(HRL),eye='#2A1A12')
    if r.random()<.4 and not young:
        top=r.choice(WOMC); c.update(top=top,trim=shade(top,.75),pants=r.choice([shade(top,.6),'#F4F1EA']),hairstyle=r.choice(['long','bun','ponytail']),kurta=True,dupatta=r.choice(WOMC),dupatta_trim='#E6B53A',
                 lashes=True,earrings=True,shoes='#C9A27A',accent='#E6B53A',sole='#3A2A1E',h=r.choice([.9,.93,.96]),button='#E6B53A')
    elif r.random()<.5:
        top=r.choice(MENC); c.update(top=top,trim=shade(top,.8),pants=top,kurta=True,shalwar=True,cuff=True,hairstyle=r.choice(['short','fringe','quiff']),sandals='#5E3A1E',h=r.choice([.96,1.0,1.04]),button=shade(top,.7))
        if r.random()<.4: c['stache']=c['hair']
    else:
        c.update(top=r.choice(MENC),pants=r.choice(['#27365A','#3A3D47','#4A3D32','#1E2A44']),hairstyle=r.choice(['short','fringe','quiff','cap','curly']),shoes=r.choice(['#F4F5FA','#22242B']),accent='#22242B',sole='#F0F1F5',
                 h=r.choice([.96,1.0,1.03]),short=r.random()<.5,cap=r.choice(MENC))
        if r.random()<.35: c['jacket']=r.choice(MENC)
        if r.random()<.2: c['glasses']=True
    return c
def walkers(n,seed,x0,x1,ys,z=0.0):
    r=random.Random(seed); P=[]
    for i in range(n):
        y=r.choice(ys)+r.uniform(-.3,.3); d=r.choice([-1,1]); H=avatar_bd((0,y,z),90*d,person(seed*100+i),name='w%d_%d'%(seed,i)); P.append(dict(H=H,x0=r.uniform(x0,x1),y=y,d=d,v=r.uniform(.9,1.2),a=x0,b=x1))
    return P
def upd_walkers(P,tg):
    for p in P:
        H=p['H']; L_=p['b']-p['a']; x=p['a']+((p['x0']-p['a'])+p['d']*p['v']*tg)%L_; H['root'].location[0]=x; H['root'].location[1]=p['y']; H['root'].rotation_euler[2]=R(90*p['d']); walk(H,p['v']*tg,step=.55); blink(H,tg)
def phone(H,s=1,sc=1.2):
    return in_hand(H,s,lambda e: phone_obj(e,(0,-.06,.05),sc))
def hold_phone(H,s=1,k=1.0):
    hp=root_mat(H)@Vector((s*.28*H['u'],-1.15*H['u'],3.5*H['u'])); arm_to(H,s,hp,k,base=(0,0,0))

# ================================================================ helpers for this film
def mk(C,x,y,rz,name,z=0.0): return avatar_bd((x,y,z),rz,C,name=name)
def hp(H,dz=0.0): r=H['root'].location; return (r[0],r[1],r[2]+4.75*H['u']+dz)
def facep(H,p,amt=1.0,cam=None):
    r=H['root']; a=face_dir(p[0]-r.location[0],p[1]-r.location[1])
    if cam is not None: a=lerp_angle(a,face_dir(cam[0]-r.location[0],cam[1]-r.location[1]),amt)
    r.rotation_euler[2]=R(a)
def shk(H,k):
    sh=H['props']['shades']; u=H['u']; sh.location=(0,.12*u*(1-k),.62*u*(1-k)); sh.rotation_euler=(R(-28*(1-k)),0,0)
def big_cup(e,s=1.0):
    ocyl((0,-.06,.08*s),.07*s,.2*s,M('#F4F1EA',.5),e,rot=(0,0,0),seg=14,r2=.055*s); ocyl((0,-.06,.07*s),.073*s,.08*s,M('#2F6A3E',.7),e,rot=(0,0,0),seg=14); ocyl((0,-.06,.19*s),.075*s,.02*s,M('#F4F1EA',.4),e,rot=(0,0,0),seg=14)
    obox((.02,-.06,.27*s),(.008,.008,.09*s),M('#35975A',.5),0,e,rot=(0,R(12),0))
def cup(H,s=1,sc=1.4): return in_hand(H,s,lambda e: big_cup(e,sc))
def hold(H,s=1,a=-70,z=10): H['arm'][s].rotation_euler=(R(a),0,R(s*z))
def gest(H,t,s=1,a=1.0,f=7.0,base=-62):
    g=math.sin(t*f+H['seed']); H['arm'][s].rotation_euler=(R(base-18*g*a),0,R(s*(12+9*g*a)))
def laugh(H,t,a=1.0):
    H['head'].rotation_euler[0]=R(-8*a+7*a*math.sin(t*15+H['seed'])); face(H,mouth='grin',brow=.04)
def ear(H,s=1,k=1.0):
    u=H['u']; arm_to(H,s,H['head'].matrix_world@Vector((s*.85*u,-.25*u,.0)),k,base=(0,0,0))
def headtouch(H,s=1,k=1.0,dx=.5,dy=-.5,dz=.55):
    u=H['u']; arm_to(H,s,H['head'].matrix_world@Vector((s*dx*u,dy*u,dz*u)),k,base=(0,0,0))
def idle_all(Hs,t):
    for H in Hs: stand(H,t); blink(H,t)
def label(body,loc,t0,col='#7A1F1F',bg='#FFF3B0',size=.26): return bubble(body,loc,t0,size=size,col=col,bg=bg)
def wifi_icon(loc,t0):
    e=empty(loc); m=M('#2B9BE8',.4,emit=2.5); obox((0,.03,.2),(.52,.02,.42),M('#FFFFFF',.5,emit=.5),.12,e); oico((0,0,-.02),.05,m,e,sub=1)
    for r_ in (.16,.28,.40):
        for k in range(9):
            a=R(48+k*10.5); obox((math.cos(a)*r_,0,math.sin(a)*r_-.02),(.03,.015,.022),m,0,e,rot=(0,-(a-pi/2),0))
    e.scale=(0,0,0)
    def fn(o,t):
        k=pop(t-t0) if t>=t0 else 0; o.scale=(k,k,k); face_cam(o)
    fx.add(e,fn); return e
def drumstick(e,s=1.0):
    ocyl((0,-.06,.1*s),.022*s,.2*s,M('#F4EEE0',.5),e,rot=(0,0,0),seg=6); oico((0,-.06,.24*s),.085*s,M('#B5642A',.5,spec=.7),e,sc=(1,1,1.35),sub=2)


# ================================================================ props
def chips(e,s=1.0):
    obox((0,-.06,.12*s),(.11*s,.035*s,.15*s),M('#F28A1A',.25,spec=.9),.02*s,e); obox((0,-.098*s,.14*s),(.07*s,.004,.05*s),M('#C8372D',.4),.0,e)
    text('CRUNCHO',(0,-.103*s,.2*s),(0,-1,0),.035*s,M('#FFF3B0',.4,emit=.4),ex=.002,parent=e)
def keys(e,s=1.0):
    ocyl((0,-.06,.03),.04*s,.01,M('#C9CED8',.3,metal=.9),e,rot=(R(90),0,0),seg=10); obox((0,-.06,.1*s),(.012*s,.005,.06*s),M('#C9CED8',.3,metal=.9),.0,e); obox((.03,-.06,-.04),(.03*s,.01,.04*s),M('#C8372D',.5),.01,e)
def note500(e,s=1.0):
    obox((0,-.08,.06),(.1*s,.004,.05*s),M('#4E8A4A',.6),.002,e); text('500',(0,-.086,.06),(0,-1,0),.035*s,M('#F4F1EA',.5),ex=.001,parent=e)
def clock_card(loc,t0,label,spin=1.0,col='#7A1F1F'):
    e=empty(loc); obox((0,.05,0),(.75,.03,.75),M('#FFFFFF',.5,emit=.4),.3,e); ocyl((0,.0,0),.55,.04,M('#FFF3B0',.5,emit=.5),e,rot=(R(90),0,0),seg=28)
    for k in range(12): a=k*pi/6; obox((math.sin(a)*.47,-.03,math.cos(a)*.47),(.02,.01,.05),M('#16171C',.5),0,e,rot=(0,a,0))
    h1=empty((0,-.04,0),e); obox((0,0,.15),(.025,.01,.17),M('#16171C',.5),0,h1); h2=empty((0,-.05,0),e); obox((0,0,.22),(.018,.01,.25),M(col,.5),0,h2)
    text(label,(0,-.05,-.98),(0,-1,0),.3,M(col,.5,emit=.3),ex=.02,parent=e); obox((0,.0,-.98),(len(label)*.11+.2,.03,.22),M('#FFF3B0',.5,emit=.5),.08,e)
    e.scale=(0,0,0)
    def fn(o,t):
        k=pop(t-t0) if t>=t0 else 0; o.scale=(k,k,k); face_cam(o); h2.rotation_euler[1]=(t-t0)*spin*6; h1.rotation_euler[1]=(t-t0)*spin*.5
    fx.add(e,fn); return e
def title_card(body,t0,loc,size=.5):
    e=empty(loc); obox((0,.06,0),(len(body)*size*.32+.4,.03,size*.75),M('#1B1F33',.6),.1,e); text(body,(0,0,0),(0,-1,0),size,M('#FFF3B0',.4,emit=2),ex=.02,parent=e); e.scale=(0,0,0)
    def fn(o,t):
        k=pop(t-t0) if t>=t0 else 0; o.scale=(k,k,k); face_cam(o)
    fx.add(e,fn); return e

# ================================================================ sets
CAR_P=(-4.6,1.25)
def gali_set(night=False,car=True,carx=None):
    gali(night); B.done('gali'); setup_world('night' if night else 'afternoon',shadow=60)
    if night:
        point((0,2.7,2.7),280,(1,.8,.55),.3,False); point((-6,0,4.5),350,(1,.85,.6),.6,False); point((5,-1,4.5),250,(.7,.8,1),.6,False); point((-.5,-1.2,2.6),420,(1,.88,.7),1.0,False); point((3.5,-1.5,3.0),260,(.75,.82,1),1.0,False)
    C=mehran((CAR_P[0] if carx is None else carx,CAR_P[1],0),0) if car else None
    return C
def boys_gali(p=((-.2,2.2,-10),(1.2,2.0,8),(2.5,2.3,-20))):
    Bi=mk(BILAL,*p[0],'bilal'); Sh=mk(SHERRY,*p[1],'sherry'); Fa=mk(FAIZAN,*p[2],'faizan'); return Bi,Sh,Fa
def in_car(C):
    Hs=[]
    for C_,n,(lx,ly) in ((BILAL,'bilal',(.12,-.5)),(SHERRY,'sherry',(.12,.5)),(FAIZAN,'faizan',(-1.0,.42))):
        H=mk(C_,0,0,0,n); H['root'].parent=C['root']; H['root'].location=(lx,ly,0); H['root'].rotation_euler=(0,0,R(90)); H['z0']=0; Hs.append(H)
    return Hs
def car_idle(Hs,t):
    for H in Hs: sit(H,1,.74,legs=88); blink(H,t); H['root'].rotation_euler=(0,0,R(90))
def drive_hands(Bi,t,k=1.0):
    g=math.sin(t*2.2); Bi['arm'][1].rotation_euler=(R(-70*k),0,R((6+8*g)*k)); Bi['arm'][-1].rotation_euler=(R(-70*k),0,R((-6+8*g)*k))
def road_set(mood='golden'):
    gt_road(); B.done('road'); setup_world(mood,shadow=60); C=mehran((0,-2.1,0),0); Hs=in_car(C); return C,Hs
def pump_set():
    D=pump(); B.done('pump'); setup_world('dusk',shadow=50); point((0,6,4.6),900,(1,.95,.88),2.0,False); point((-4,3,2.2),220,(1,.9,.8),.5,False)
    return D
CABIN=lambda C,x,y,z: C['root'].matrix_world@Vector((x,y,z))
SPD=11.0

# ================================================================ HOOK
def OPEN_():
    C=gali_set(); Bi,Sh,Fa=boys_gali()
    def upd(t):
        idle_all((Bi,Sh,Fa),t); gest(Bi,t,1); gest(Sh,t,-1,f=6); laugh(Fa,t,.5); look_at(Bi,hp(Sh),.6); look_at(Sh,hp(Bi),.6); mouth_talk(Bi,t,.1,1.0,rest='smile'); face(Sh,mouth='smile')
        q=ease(t/DUR); camset(LV((-.6,-3.3,4.0),(.0,-3.2,2.2),q),LV((-1,3,2.2),(.4,2.3,1.5),q),20,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def FIVE_():
    C=gali_set(); Bi,Sh,Fa=boys_gali(); clock_card((-.9,2.1,3.3),.35,'5 MIN',spin=.2,col='#1F5A3A')
    def upd(t):
        idle_all((Bi,Sh,Fa),t); k=tl(t,.15,.45); Bi['arm'][1].rotation_euler=(R(-150*k),0,R(22*k)); face(Bi,mouth='grin',brow=.04); Bi['root'].rotation_euler[2]=R(-10)
        look_at(Sh,hp(Bi),.7); look_at(Fa,hp(Bi),.7); face(Sh,mouth='smile'); face(Fa,mouth='smile')
        q=ease(t/DUR); camset(LV((.6,-1.2,1.9),(.4,-.9,1.95),q),(-.2,2.2,2.1),30,5.6)
    return dict(upd=upd)
SHOTS['FIVE']=FIVE_
def TWELVE_():
    C,Hs=road_set('golden'); Bi,Sh,Fa=Hs; X0=-20; cc=clock_card((0,0,0),.25,'12 HOURS',spin=3.0)
    def upd(t):
        x=X0+SPD*1.4*t; drive(C,x,-2.1,0,x); C['root'].location[2]=.03*math.sin(t*17); car_idle(Hs,t); drive_hands(Bi,t)
        for H in Hs: face(H,mouth='grin',brow=.04)
        Sh['arm'][-1].rotation_euler=(R(-160),0,R(-20)); Fa['arm'][1].rotation_euler=(R(-150),0,R(20+10*math.sin(t*9)))
        cc.location=(x+1.0,-2.1,4.3); camset((x+9.0,-9.5,1.4),(x+.6,-2.1,1.7),30,16)
    return dict(upd=upd)
SHOTS['TWELVE']=TWELVE_

# ================================================================ SCENE 1
def MEET_():
    C=gali_set(); Bi,Sh,Fa=boys_gali(); tn=[W_[i]['s']-T0 for i in (16,17,19)]
    label('BILAL',(-.2,2.2,3.15),tn[0]); label('SHERRY',(1.2,2.0,3.3),tn[1],col='#7A1F1F'); label('FAIZAN',(2.5,2.3,2.75),tn[2],col='#1F4A7A',bg='#DFEFFF')
    def upd(t):
        idle_all((Bi,Sh,Fa),t)
        k=tl(t,tn[0],tn[0]+.25); Bi['arm'][1].rotation_euler=(R(-25*k),0,R(-45*k)); Bi['arm'][-1].rotation_euler=(R(-25*k),0,R(45*k)); face(Bi,mouth='smirk',brow=-.02,brow_r=-8)
        k=tl(t,tn[1],tn[1]+.25); Sh['arm'][1].rotation_euler=(R(-140*k),0,R(18*k)); face(Sh,mouth='grin' if k>.5 else 'smile'); Sh['head'].rotation_euler[1]=R(-8*k)
        k=tl(t,tn[2],tn[2]+.25); Fa['arm'][1].rotation_euler=(R(-70*k),0,R(-30*k)); Fa['root'].location[2]=.1*abs(math.sin((t-tn[2])*8))*k*(t<tn[2]+1.2); face(Fa,mouth='grin' if k>.5 else 'smile')
        q=ease(t/DUR); camset(LV((1.3,-2.6,1.6),(1.0,-2.0,1.65),q),(1.1,2.2,1.6),26,16)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def MISSION_():
    C=gali_set(); Bi,Sh,Fa=boys_gali(); ky=in_hand(Bi,1,lambda e: keys(e,1.6)); sparkles((-4.6,1.25,1.4),2.0,1.6,3.4,30,.05,4,.6)
    def upd(t):
        idle_all((Bi,Sh,Fa),t); g=t*14; Bi['arm'][1].rotation_euler=(R(-115),0,R(14)); ky.rotation_euler=(0,g,0); face(Bi,mouth='grin',brow=.05); Bi['root'].rotation_euler[2]=R(-50)
        for H,d in ((Sh,1),(Fa,-1)): H['arm'][1].rotation_euler=(R(-150-15*math.sin(t*8+d)),0,R(18)); H['arm'][-1].rotation_euler=(R(-150+15*math.sin(t*8+d)),0,R(-18)); face(H,mouth='grin',brow=.05)
        Fa['root'].location[2]=.12*abs(math.sin(t*6)); Sh['root'].location[2]=.1*abs(math.sin(t*6+1))
        q=ease(t/DUR); camset(LV((-1.0,-2.9,1.5),(-.6,-2.7,1.55),q),(-.6,1.9,1.4),22,16)
    return dict(upd=upd)
SHOTS['MISSION']=MISSION_
def GHOOM_():
    C=gali_set(); Bi,Sh,Fa=boys_gali(); ky=in_hand(Bi,1,lambda e: keys(e,1.6))
    def upd(t):
        idle_all((Bi,Sh,Fa),t); talk(Bi,t,11.57,13.6); face(Bi,brow=-.02,brow_r=-6); g=math.sin(t*5); Bi['arm'][1].rotation_euler=(R(-70-10*g),0,R(12)); ky.rotation_euler=(0,R(30*g),0)
        Bi['arm'][-1].rotation_euler=(R(-40-30*abs(math.sin(t*3))),0,R(-25)); Bi['head'].rotation_euler=(0,R(4*g),R(8))
        q=ease(t/DUR); camset(LV((.4,-.6,1.9),(.3,-.3,1.92),q),hp(Bi,-.02),45,2.8)
    return dict(upd=upd)
SHOTS['GHOOM']=GHOOM_
def PETROLQ_():
    C=gali_set(); Bi,Sh,Fa=boys_gali()
    def upd(t):
        idle_all((Bi,Sh,Fa),t); talk(Sh,t,14.02,15.15); face(Sh,brow=-.03,brow_r=-14); Sh['head'].rotation_euler=(R(6),R(-8),R(-14)); k=tl(t,.2,.5); Sh['arm'][1].rotation_euler=(R(-60*k),0,R(10)); Sh['arm'][-1].rotation_euler=(R(-25),0,R(-35))
        q=ease(t/DUR); camset(LV((1.6,-.7,2.1),(1.5,-.4,2.12),q),hp(Sh,-.03),45,2.8)
    return dict(upd=upd)
SHOTS['PETROLQ']=PETROLQ_
def QUIET_():
    C=gali_set(); Bi,Sh,Fa=boys_gali(); ph=phone(Bi,1)
    globals()['LEAF']=[M(c,.8) for c in ('#B8862E','#9A7A2A','#C9A24A','#7A8A3A','#A8662E')]; falling_leaves(-1,3,1.2,2.6,4.0,6,seed=2)
    def upd(t):
        idle_all((Bi,Sh,Fa),t); hold_phone(Bi,1,tl(t,.1,.5)); Bi['head'].rotation_euler[0]=R(18*tl(t,.1,.5)); face(Bi,mouth='flat',brow=.02)
        Sh['head'].rotation_euler=(R(-20*tl(t,.2,.6)),0,R(25)); face(Sh,mouth='flat'); Sh['arm'][1].rotation_euler=(R(-10),0,R(-6))
        Fa['head'].rotation_euler=(0,0,R(-50*tl(t,.3,.7)+10*math.sin(t*2))); face(Fa,mouth='o' if int(t*3)%2 else 'flat',brow=.03); Fa['arm'][-1].rotation_euler=(R(-20),0,R(30)); Fa['arm'][1].rotation_euler=(R(-20),0,R(-30))
        for H in (Bi,Sh,Fa): blink(H,t)
        q=t/DUR; camset(LV((1.0,-3.4,1.6),(1.0,-3.1,1.6),q),(1.0,2.2,1.6),26,16)
    return dict(upd=upd)
SHOTS['QUIET']=QUIET_
def ARGUE_():
    C=gali_set(); Bi,Sh,Fa=boys_gali(((-.2,2.0,30),(1.2,2.5,180),(2.3,1.9,-40))); cc=clock_card((1.1,2.6,3.6),.15,'20 MIN',spin=4.0,col='#7A1F1F')
    def upd(t):
        idle_all((Bi,Sh,Fa),t)
        for i,(H,tgt) in enumerate(((Bi,Sh),(Sh,Fa),(Fa,Bi))):
            facep(H,hp(tgt)[:2],.0); H['root'].rotation_euler[2]=R(face_dir(1.1-H['root'].location[0],2.1-H['root'].location[1])); gest(H,t+i,1,1.6,10); gest(H,t+i+.7,-1,1.4,9)
            mouth_talk(H,t,0,DUR,rate=9,rest='frown'); face(H,brow=-.04,brow_r=-14); H['root'].location[2]=.05*abs(math.sin(t*7+i))
        q=ease(t/DUR); camset(LV((1.1,-1.6,3.4),(1.1,-1.2,3.0),q),(1.1,2.1,1.5),24,16)
    return dict(upd=upd)
SHOTS['ARGUE']=ARGUE_

# ================================================================ SCENE 2 — the drive
def DRIVE_():
    C,Hs=road_set(); Bi,Sh,Fa=Hs; X0=0
    def upd(t):
        x=X0+SPD*t; drive(C,x,-2.1,0,x); C['root'].location[2]=.03*math.sin(t*17); car_idle(Hs,t); drive_hands(Bi,t); face(Bi,mouth='smirk')
        g=math.sin(t*4); Sh['arm'][-1].rotation_euler=(R(-95),0,R(-40+20*g)); face(Sh,mouth=('o','flat')[int(t*6)%2],brow=.03); Fa['arm'][1].rotation_euler=(R(-110+30*abs(math.sin(t*7))),0,R(10)); face(Fa,mouth='O' if int(t*7)%2 else 'flat')
        camset((x-2.0,-8.6,1.8),(x+.2,-2.1,1.6),30,16)
    return dict(upd=upd)
SHOTS['DRIVE']=DRIVE_
def inside_cam(C,t,dx=3.2,dy=0,dz=2.0,tx=-.3,ty=0,tz=1.85,lens=28):
    camset(CABIN(C,dx,dy,dz),CABIN(C,tx,ty,tz),lens,8)
def INSIDE_():
    C,Hs=road_set(); Bi,Sh,Fa=Hs; ch=in_hand(Fa,1,lambda e: chips(e,1.6)); tf=W_[64]['s']-T0
    def upd(t):
        x=SPD*(t+3); drive(C,x,-2.1,0,x); C['root'].location[2]=.03*math.sin(t*17); car_idle(Hs,t); drive_hands(Bi,t); face(Bi,mouth='flat',brow=-.02)
        g=math.sin(t*5); Sh['arm'][-1].rotation_euler=(R(-100),0,R(30+25*g)); Sh['head'].rotation_euler[2]=R(-14*g); mouth_talk(Sh,t,0,tf,rate=8); 
        k=abs(math.sin(t*5))*(t>tf-.3); Fa['arm'][1].rotation_euler=(R(-75-50*k),0,R(14)); face(Fa,mouth=('O','flat')[int(t*6)%2] if t>tf else 'smile')
        q=ease(t/DUR); inside_cam(C,t,LV((3.6,.8,2.3),(3.3,.3,2.1),q)[0],LV((3.6,.8,2.3),(3.3,.3,2.1),q)[1],LV((3.6,.8,2.3),(3.3,.3,2.1),q)[2])
    return dict(upd=upd)
SHOTS['INSIDE']=INSIDE_
def CHIPS_():
    C,Hs=road_set(); Bi,Sh,Fa=Hs; ch=in_hand(Fa,1,lambda e: chips(e,1.6))
    def upd(t):
        x=SPD*(t+8); drive(C,x,-2.1,0,x); C['root'].location[2]=.03*math.sin(t*17); car_idle(Hs,t); drive_hands(Bi,t)
        k=tl(t,.1,.5); arm_to(Fa,1,CABIN(C,.4,.2,1.6),k,base=(-75,0,14)); talk(Fa,t,26.57,27.8); face(Fa,brow=.04); Fa['head'].rotation_euler=(0,0,R(-12))
        look_at(Sh,hp(Fa),.6*tl(t,.6,1.0),maxyaw=80); face(Sh,mouth='o',brow=.05,eyes=1.15)
        inside_cam(C,t,.45,2.7,2.05,-.9,.25,1.75,26)
    return dict(upd=upd)
SHOTS['CHIPS']=CHIPS_
def DE_():
    C,Hs=road_set(); Bi,Sh,Fa=Hs; ch=in_hand(Fa,1,lambda e: chips(e,1.6))
    def upd(t):
        x=SPD*(t+10); drive(C,x,-2.1,0,x); car_idle(Hs,t); drive_hands(Bi,t); arm_to(Fa,1,CABIN(C,.4,.2,1.6),1,base=(-75,0,14)); face(Fa,mouth='smile')
        Sh['head'].rotation_euler=(0,0,R(-60)); k=ease(tl(t,.0,.25)); arm_to(Sh,1,CABIN(C,.3,.25,1.65),k,base=(-60,0,0)); talk(Sh,t,28.17,28.62,shapes=('O','O'),rest='grin'); face(Sh,brow=.06,eyes=1.2)
        inside_cam(C,t,.45,2.7,2.05,-.9,.25,1.75,26)
    return dict(upd=upd)
SHOTS['DE']=DE_
def PAISE_():
    C,Hs=road_set(); Bi,Sh,Fa=Hs; ch=in_hand(Fa,1,lambda e: chips(e,1.6))
    def upd(t):
        x=SPD*(t+11); drive(C,x,-2.1,0,x); car_idle(Hs,t); drive_hands(Bi,t)
        k=ease(tl(t,.0,.35)); arm_to(Fa,1,CABIN(C,.4,.2,1.6),1-k,base=(-105,0,10)); talk(Fa,t,28.81,30.1,rest='smirk'); face(Fa,brow=-.02,brow_r=-8); Fa['head'].rotation_euler=(R(-6),0,R(10))
        Sh['head'].rotation_euler=(0,0,R(-60)); arm_to(Sh,1,CABIN(C,.3,.25,1.65),1-tl(t,.6,1.0),base=(-30,0,0)); face(Sh,mouth='frown',brow=-.04,brow_r=-14)
        face(Bi,mouth='grin'); inside_cam(C,t,.45,2.7,2.05,-.9,.25,1.75,26)
    return dict(upd=upd)
SHOTS['PAISE']=PAISE_

# ================================================================ SCENE 3 — petrol pump
PY=6.0
def STATION_():
    D=pump_set(); C=mehran((-16,PY,0),0); Hs=in_car(C); At=mk(ATTEND,-.9,4.6,180,'attend')
    def upd(t):
        q=ease_out(min(1,t/1.3)); x=-16+16*q; drive(C,x,PY,0,x); C['root'].rotation_euler[1]=R(-2*math.sin(pi*tl(t,1.1,1.5))); car_idle(Hs,t); drive_hands(Hs[0],t)
        stand(At,t); blink(At,t); look_at(At,(x,PY,1.5),.7); face(At,mouth='smile')
        camset((6.5,-3.2,1.9),(-1.0,5.6,1.6),24,16)
    return dict(upd=upd)
SHOTS['STATION']=STATION_
def FIVEHUND_():
    D=pump_set(); C=mehran((0,PY,0),0); Hs=in_car(C); Bi=Hs[0]; At=mk(ATTEND,-.6,4.55,0,'attend'); nt=in_hand(Bi,-1,lambda e: note500(e,1.8)); nz=in_hand(At,1,lambda e: ocyl((0,-.06,.1),.035,.3,M('#16171C',.6),e,rot=(0,0,0),seg=6))
    disp=text('000',(-2.0,3.68,1.25),(0,-1,0),.18,M('#FF5A3A',.4,emit=3),ex=.002); hand=tl(32.47-T0,0,1)
    tr=32.6-T0
    def upd(t):
        drive(C,0,PY,0,0); car_idle(Hs,t); k=tl(t,.15,.6)*(1-tl(t,tr+.1,tr+.4)); arm_to(Bi,-1,(-.25,4.55,1.75),k,base=(-60,0,0)); nt.scale=(1,1,1) if t<tr+.15 else (0,0,0); face(Bi,mouth='smirk',brow=-.02)
        stand(At,t); blink(At,t); At['root'].rotation_euler[2]=R(-20); kk=tl(t,tr-.2,tr+.1); arm_to(At,-1,(-.3,4.7,1.75),kk*(1-tl(t,tr+.4,tr+.7)),base=(-10,0,0)); arm_to(At,1,(-1.6,4.2,1.0),tl(t,tr+.6,tr+1.0),base=(-50,0,0))
        v=int(500*ease(tl(t,tr+1.0,DUR-.3))); disp.data.body='%03d'%v; face(At,mouth='smile')
        q=ease(t/DUR); camset(LV((-3.2,1.2,1.9),(-3.0,1.6,1.95),q),(-.6,4.7,1.65),26,8)
    return dict(upd=upd)
SHOTS['FIVEHUND']=FIVEHUND_
def ENNA_():
    D=pump_set(); C=mehran((0,PY,0),0); Hs=in_car(C); Bi,Sh,Fa=Hs; At=mk(ATTEND,-.6,4.55,0,'attend'); b=bubble('Rs 500 only?!',(1.6,PY+.6,3.25),.3,size=.2,col='#7A1F1F',bg='#FFF3B0')
    def upd(t):
        drive(C,0,PY,0,0); car_idle(Hs,t); stand(At,t); blink(At,t)
        Sh['head'].rotation_euler=(0,0,R(60)); talk(Sh,t,34.71,37.3); face(Sh,brow=.05,brow_r=12); g=math.sin(t*6); Sh['arm'][1].rotation_euler=(R(-90-15*g),0,R(25)); Sh['arm'][-1].rotation_euler=(R(-20),0,R(-40))
        face(Bi,mouth='flat',brow=-.02); laugh(Fa,t,.5)
        inside_cam(C,t,3.1,1.2,2.2,0,.0,1.9,30)
    return dict(upd=upd)
SHOTS['ENNA']=ENNA_
def FERRARI_():
    D=pump_set(); C=mehran((0,PY,0),0); Hs=in_car(C); Bi,Sh,Fa=Hs; sparkles((0,PY,2.0),1.6,1.3,2.6,30,.05,8,.5); tz=39.3-T0
    def upd(t):
        x=0+ (14*ease_in(tl(t,tz,DUR)) if t>tz else 0); drive(C,x,PY,0,x); car_idle(Hs,t)
        talk(Bi,t,37.41,40.0); face(Bi,brow=-.03,brow_r=-10); Bi['head'].rotation_euler=(0,0,R(-50*(1-tl(t,tz-.3,tz)))); k=tl(t,.2,.4); Bi['arm'][-1].rotation_euler=(R(-80-20*abs(math.sin(t*9))*(t<1.2)),0,R(-10)); Bi['arm'][1].rotation_euler=(R(-70),0,R(8))
        face(Sh,mouth='frown',brow=-.03,brow_r=-12); face(Fa,mouth='O',brow=.05)
        if t<tz: inside_cam(C,t,2.6,-.4,2.1,.1,-.5,1.95,32)
        else: camset((6,1.0,1.4),(x,PY,1.2),26,16)
    for i in range(6): puff((-2.4,PY+.4,.5),tz+i*.06,.18,4,M('#B8B0A8',.9),.4,.8,seed=i)
    return dict(upd=upd)
SHOTS['FERRARI']=FERRARI_

# ================================================================ SCENE 4 — back home
def gali_night(car_in=True):
    C=gali_set(True); Bi,Sh,Fa=boys_gali(((.9,1.7,-40),(2.1,1.45,-35),(3.25,1.75,-30))); Mo=mk(AMMI,-.4,3.0,35,'ammi'); return C,Bi,Sh,Fa,Mo
def LATER_():
    C=gali_set(True); Hs=in_car(C); title_card('3 HOURS LATER...',.15,(-5.4,.3,3.2),.3)
    def upd(t):
        q=ease_out(min(1,t/1.6)); x=-18+(CAR_P[0]+18)*q; drive(C,x,CAR_P[1],0,x); C['root'].rotation_euler[1]=R(3*math.sin(t*30)*(t>1.6)*(t<2.0)); car_idle(Hs,t); drive_hands(Hs[0],t)
        for H in Hs: face(H,mouth='flat',brow=-.02)
        camset((-3.0,-3.0,2.4),(-6.5,1.3,1.6),24,16)
    for i in range(6): puff((CAR_P[0]-2.4,CAR_P[1]+.3,.5),1.6+i*.1,.2,4,M('#6A6460',.9),.4,.9,seed=i)
    return dict(upd=upd)
SHOTS['LATER']=LATER_
def MOM_():
    C,Bi,Sh,Fa,Mo=gali_night()
    def upd(t):
        idle_all((Bi,Sh,Fa,Mo),t); Mo['arm'][1].rotation_euler=(R(-40),0,R(-55)); Mo['arm'][-1].rotation_euler=(R(-40),0,R(55)); face(Mo,mouth='flat',brow=-.04,brow_r=-14); Mo['head'].rotation_euler[2]=R(8*math.sin(t*1.5))
        for H in (Bi,Sh,Fa): H['head'].rotation_euler[0]=R(10); face(H,mouth='flat',brow=.03)
        q=ease(t/DUR); camset(LV((-1.4,-2.4,1.6),(-1.1,-2.0,1.62),q),(.7,2.4,1.5),24,16)
    return dict(upd=upd)
SHOTS['MOM']=MOM_
def BAS_():
    C,Bi,Sh,Fa,Mo=gali_night(); ky=in_hand(Bi,1,lambda e: keys(e,1.6))
    def upd(t):
        idle_all((Bi,Sh,Fa,Mo),t); talk(Bi,t,44.93,47.1); face(Bi,brow=.05,brow_r=12,eyes=1.15); Bi['arm'][1].rotation_euler=(R(-15),0,R(8)); Bi['arm'][-1].rotation_euler=(R(-30),0,R(-35)); Bi['head'].rotation_euler=(0,R(-6),R(-12))
        q=ease(t/DUR); camset(LV((.2,-.1,1.95),(.25,.15,1.97),q),hp(Bi,-.02),45,2.8)
    return dict(upd=upd)
SHOTS['BAS']=BAS_
def TEPETROL_():
    C,Bi,Sh,Fa,Mo=gali_night()
    def upd(t):
        idle_all((Bi,Sh,Fa,Mo),t); talk(Mo,t,47.2,48.0); face(Mo,brow=-.05,brow_r=-18,eyes=.85); Mo['arm'][1].rotation_euler=(R(-40),0,R(-55)); Mo['arm'][-1].rotation_euler=(R(-40),0,R(55)); Mo['head'].rotation_euler=(R(6),0,R(-8))
        q=ease(t/DUR); camset(LV((-.9,1.2,1.75),(-.85,1.45,1.76),q),hp(Mo,-.03),50,2.8)
    return dict(upd=upd)
SHOTS['TEPETROL']=TEPETROL_
def LOOKS_():
    C,Bi,Sh,Fa,Mo=gali_night()
    def upd(t):
        idle_all((Bi,Sh,Fa,Mo),t); Bi['head'].rotation_euler=(0,0,R(50*math.sin(pi*tl(t,.1,.9)))); face(Bi,mouth='flat',brow=.05,brow_r=10); face(Sh,mouth='flat',brow=.03); face(Fa,mouth='flat',brow=.03)
        look_at(Sh,hp(Bi),.5); look_at(Fa,hp(Bi),.5)
        q=ease(t/DUR); camset(LV((1.6,-2.1,1.9),(1.6,-1.8,1.9),q),(1.9,1.7,1.75),28,8)
    return dict(upd=upd)
SHOTS['LOOKS']=LOOKS_
def POINT_():
    C,Bi,Sh,Fa,Mo=gali_night(); ch=in_hand(Fa,1,lambda e: chips(e,1.6))
    def upd(t):
        idle_all((Bi,Sh,Fa,Mo),t); k=ease(tl(t,.2,1.6)); arm_to(Sh,1,hp(Fa,-.85),k,base=(-10,0,0)); Sh['head'].rotation_euler=(0,0,R(-30*k)); face(Sh,mouth='flat',brow=-.02)
        Fa['arm'][1].rotation_euler=(R(-60),0,R(10)); face(Fa,mouth='o' if t>1.4 else 'smile',brow=.05*tl(t,1.3,1.6)); look_at(Fa,hp(Sh),.8*tl(t,1.2,1.6))
        look_at(Mo,hp(Fa),.6*tl(t,1.0,1.6)); face(Mo,mouth='flat',brow=-.04,brow_r=-14)
        q=ease(t/DUR); camset(LV((3.6,-1.7,1.75),(3.5,-1.4,1.78),q),(2.6,1.6,1.7),30,8)
    return dict(upd=upd)
SHOTS['POINT']=POINT_
def FAIZ_():
    C,Bi,Sh,Fa,Mo=gali_night(); ch=in_hand(Fa,1,lambda e: chips(e,1.6))
    def upd(t):
        idle_all((Bi,Sh,Fa,Mo),t); talk(Fa,t,51.92,54.1,shapes=('O','o','O','flat')); face(Fa,brow=.06,eyes=1.3); g=math.sin(t*12)
        Fa['arm'][1].rotation_euler=(R(-130+20*g),0,R(20)); Fa['arm'][-1].rotation_euler=(R(-130-20*g),0,R(-20)); Fa['root'].location[2]=.08*abs(math.sin(t*9)); Fa['head'].rotation_euler=(0,0,R(14*math.sin(t*6)))
        q=ease(t/DUR); camset(LV((3.0,-.1,1.65),(3.0,.15,1.66),q),hp(Fa,-.05),45,2.8)
    return dict(upd=upd)
SHOTS['FAIZ']=FAIZ_
def KEYS_():
    C,Bi,Sh,Fa,Mo=gali_night(); kb=in_hand(Bi,1,lambda e: keys(e,1.6)); km=in_hand(Mo,1,lambda e: keys(e,1.6)); tg=.9
    def upd(t):
        idle_all((Bi,Sh,Fa,Mo),t); Mo['root'].location=(-.05,2.55,0); Mo['root'].rotation_euler[2]=R(15)
        k=tl(t,.2,tg); arm_to(Mo,1,(.5,1.95,1.45),k*(1-tl(t,tg+.1,tg+.5)),base=(-20,0,0)); arm_to(Bi,1,(.5,1.95,1.4),.8,base=(0,0,0))
        kb.scale=(1,1,1) if t<tg else (0,0,0); km.scale=(0,0,0) if t<tg else (1,1,1)
        if t>tg+.5: Mo['arm'][1].rotation_euler=(R(-100),0,R(-10)); km.rotation_euler[1]=R(25*math.sin(t*6))
        face(Mo,mouth='flat',brow=-.05,brow_r=-16); face(Bi,mouth='O' if t>tg else 'flat',brow=.06 if t>tg else .02,eyes=1.2 if t>tg else 1.0)
        for H in (Sh,Fa): look_at(H,hp(Mo),.6); face(H,mouth='o',brow=.05)
        q=ease(t/DUR); camset(LV((-.9,-1.4,1.8),(-.8,-1.1,1.8),q),(.35,2.2,1.6),28,8)
    return dict(upd=upd)
SHOTS['KEYS']=KEYS_
def PAIDAL_():
    C,Bi,Sh,Fa,Mo=gali_night(); km=in_hand(Mo,1,lambda e: keys(e,1.6))
    def upd(t):
        idle_all((Bi,Sh,Fa,Mo),t); talk(Mo,t,56.0,56.9); face(Mo,brow=-.05,brow_r=-16); k=tl(t,.05,.35); arm_to(Mo,-1,(8,-1,1.2),k,base=(0,0,0)); Mo['arm'][1].rotation_euler=(R(-95),0,R(-10)); km.rotation_euler[1]=R(25*math.sin(t*6))
        q=ease(t/DUR); camset(LV((-.9,1.2,1.75),(-.85,1.4,1.76),q),hp(Mo,-.03),45,2.8)
    return dict(upd=upd)
SHOTS['PAIDAL']=PAIDAL_
def WALK_():
    C,Bi,Sh,Fa,Mo=gali_night(); km=in_hand(Mo,1,lambda e: keys(e,1.6))
    def upd(t):
        stand(Mo,t); blink(Mo,t); talk(Mo,t,57.01,59.0); face(Mo,brow=-.05,brow_r=-16); Mo['arm'][1].rotation_euler=(R(-95),0,R(-10)); km.rotation_euler[1]=R(25*math.sin(t*6)); g=math.sin(t*5); Mo['arm'][-1].rotation_euler=(R(-70-20*g),0,R(20))
        for i,H in enumerate((Bi,Sh,Fa)):
            x0=H['root'].location[0] if t==0 else None
            walk_path(H,[((.9,2.1,3.25)[i],(1.7,1.45,1.75)[i]),((.9,2.1,3.25)[i]+1.0,.3),(((.9,2.1,3.25)[i]+9.0),-.2+.35*i)],t,.2+.15*i,DUR+2.5,step=.45,mood=-1); blink(H,t); face(H,mouth='frown',brow=.04,brow_r=12); H['head'].rotation_euler[0]=R(14)
        q=ease(t/DUR); camset(LV((9.5,-2.6,2.2),(9.0,-2.4,2.0),q),(2.0,1.4,1.4),24,16)
    return dict(upd=upd)
SHOTS['WALK']=WALK_
W_=json.load(open(LH+'/audio/words.json'))
