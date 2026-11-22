# Shots for "Lahore Lahore Ayy!". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=122.3
SEQ=[('OPEN', 0.0), ('PROUD', 1.03), ('ACCORDING', 4.64), ('AYY', 6.07), ('MEET', 7.89), ('PROPER', 8.77), ('WAKES', 10.29), ('WAH', 13.4), ('SHOUTS', 17.23), ('DOODH', 19.16), ('BUSY', 20.69), ('BUSYQ', 22.5), ('KEYS', 25.33), ('FRIENDS', 27.51), ('CARGUY', 29.8), ('TRIP', 31.61), ('THIRD', 33.73), ('NAVI', 37.67), ('GAARI', 39.71), ('BAS', 42.64), ('HOR', 44.93), ('ARGUE', 47.25), ('TOURIST', 51.08), ('SEES', 53.86), ('APPROACH', 57.89), ('EXCUSE', 59.24), ('DUMBEST', 61.61), ('PUTTAR', 65.0), ('JINHA', 66.78), ('WHAT', 69.49), ('VEKH', 70.09), ('DECIDES', 72.57), ('OLDCITY', 74.83), ('ARCH', 76.58), ('FRNDS', 77.94), ('PUNJABI', 79.51), ('DAYS', 80.92), ('NEWLOOK', 83.98), ('MORNING', 88.73), ('OYEH', 92.35), ('POORA', 94.24), ('ADJUSTS', 96.73), ('LOOKS', 98.91), ('CONF', 99.81), ('PAWA', 101.18), ('FREEZES', 104.23), ('AGGE', 105.47), ('RAISES', 107.87), ('AYYY', 110.15), ('JOINS', 112.04), ('LOOKCAM', 113.91), ('EMOTION', 115.92), ('FINALTXT', 119.75)]
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
def ln(a,b): return (W_[a]['s'],W_[b]['e'])
def bd_set(mood='golden',crowd=0):
    badshahi(); B.done('badshahi'); setup_world(mood,shadow=60); return walkers(crowd,7,-18,18,(-6,-3,4)) if crowd else []
def crowd_at(n,cx,cy,r0,r1,seed=3,face=(0,-30)):
    r=random.Random(seed); C=[]
    for i,c in enumerate(crowd_cast(n,seed)):
        a=r.uniform(0,2*pi); d=r.uniform(r0,r1); H=mk(c,cx+math.cos(a)*d,cy+math.sin(a)*d,0,'cr%d_%d'%(seed,i)); C.append(H)
    return C
def cr_idle(C,t,face=None,mode='stand'):
    for i,H in enumerate(C):
        stand(H,t); blink(H,t)
        if face: facep(H,face)
        if mode=='proud': H['root'].rotation_euler[0]=R(-6); face_(H,'grin'); H['arm'][1].rotation_euler=(R(-30),0,R(-40)); H['arm'][-1].rotation_euler=(R(-30),0,R(40))
        elif mode=='cheer': g=math.sin(t*9+i); H['arm'][1].rotation_euler=(R(-165+15*g),0,R(-20)); H['arm'][-1].rotation_euler=(R(-165-15*g),0,R(20)); H['root'].location[2]=.12*abs(math.sin(t*6+i)); face_(H,'grin')
def face_(H,m): face(H,mouth=m,brow=.05)
def home_set():
    home_ll(); B.done('home'); setup_interior('morning',room=(0,0,3.2),res=PCT,samples=SAMPLES,shadow_dist=14); point((-3,0,2.8),150,(1,.95,.86),1.2,False); point((3.5,1,2.8),150,(1,.95,.86),1.2,False)
    Hz=mk(HAMZA,-2.0,1.6,180,'hamza'); Am=mk(AMMI,4.4,2.2,0,'ammi'); return Hz,Am
def ns_set(crowd=8):
    nc=night_street(); B.done('night'); setup_world('night',shadow=40)
    for x in range(-30,31,10): point((x,0,5.5),400,(1,.85,.6),3.0,False)
    Hz=mk(HAMZA,-.4,-3.4,0,'hamza'); F1=mk(CARGUY,1.2,-4.4,0,'f1'); F2=mk(TRAVELER,-1.6,-4.6,0,'f2'); F3=mk(LOREGUY,.4,-5.4,0,'f3'); W=walkers(crowd,5,-24,24,(-9.0,9.0)); point((0,-8,3.5),900,(1,.8,.6),2.5,False); point((0,-2,3.5),500,(1,.85,.7),2.0,False)
    return nc,Hz,F1,F2,F3,W
def nidle(P,W,t):
    upd_walkers(W,t+4)
    for H in P: stand(H,t); blink(H,t)
def wc_set(crowd=10,tour=TOURIST):
    walled_city(); B.done('walled'); setup_world('afternoon',shadow=40)
    Hz=mk(HAMZA,0,1.0,180,'hamza'); To=mk(tour,0,-.6,0,'tourist'); W=walkers(crowd,9,-28,26,(-2.2,2.4)); return Hz,To,W
def widle(Hz,To,W,t):
    upd_walkers(W,t+2); stand(Hz,t); blink(Hz,t); stand(To,t); blink(To,t)
# ================================================================ HOOK
def OPEN_():
    W=bd_set(crowd=12); sparkles((0,25,13),5,.2,DUR,n=30,size=.1)
    def upd(t):
        upd_walkers(W,t); q=ease(t/DUR); camset(LV((-5,-20,2.5),(-3.5,-16,5),q),(0,20,9),22,22)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def PROUD_():
    Hz,To,W=wc_set(crowd=4); To['root'].location=(60,60,0); C=crowd_at(9,0,0,1.0,2.6,seed=4); label('PROUD. FOR NO REASON.',(0,0,3.2),.5,size=.22)
    def upd(t):
        widle(Hz,To,W,t); cr_idle(C,t,face=(-6,0),mode='proud'); Hz['root'].rotation_euler=(R(-6),0,0); face(Hz,mouth='grin',brow=.05); Hz['arm'][1].rotation_euler=(R(-30),0,R(-40)); Hz['arm'][-1].rotation_euler=(R(-30),0,R(40))
        q=ease(t/DUR); camset(LV((-7,-1.2,2.6),(-6,-1.0,2.3),q),(0,.3,1.4),24,8)
    return dict(upd=upd)
SHOTS['PROUD']=PROUD_
def ACCORDING_():
    Hz,To,W=wc_set(crowd=4); To['root'].location=(60,60,0); C=crowd_at(9,0,0,1.0,2.6,seed=4)
    def upd(t):
        widle(Hz,To,W,t); facep(Hz,(-6,0)); face(Hz,mouth='smile',brow=.05,eyes=.7)
        for H in C: stand(H,t); blink(H,t); facep(H,(-6,0)); face(H,mouth='smile',brow=.05,eyes=.7)
        q=ease(t/DUR); camset(LV((-6.5,0,1.9),(-5.6,0,1.9),q),(0,.3,1.6),26,8)
    return dict(upd=upd)
SHOTS['ACCORDING']=ACCORDING_
def AYY_():
    Hz,To,W=wc_set(crowd=4); To['root'].location=(60,60,0); C=crowd_at(9,0,0,1.0,2.6,seed=4); title_card('LAHORE LAHORE AYY!',.1,(0,.3,3.4),.36); sparkles((0,.5,3),3,.1,DUR,n=50,size=.06)
    def upd(t):
        widle(Hz,To,W,t); cr_idle(C,t,face=(-6,0),mode='cheer'); facep(Hz,(-6,0)); g=math.sin(t*9); Hz['arm'][1].rotation_euler=(R(-165+15*g),0,R(-20)); Hz['arm'][-1].rotation_euler=(R(-165-15*g),0,R(20)); face(Hz,mouth='O',brow=.06)
        q=ease(t/DUR); camset(LV((-6.2,0,1.5),(-5.0,0,1.7),q),(0,.3,2.0),24,8)
    return dict(upd=upd)
SHOTS['AYY']=AYY_
# ================================================================ SCENE 2 — home
def MEET_():
    Hz,Am=home_set(); Am['root'].location=(30,30,0); label('HAMZA',(-2.0,1.6,2.65),.1,col='#1B1F33',bg='#FFF3B0')
    def upd(t):
        stand(Hz,t); blink(Hz,t); Hz['root'].rotation_euler[2]=R(lerp_angle(180,20,tl(t,0,.4))); face(Hz,mouth='grin',brow=.05)
        q=ease(t/DUR); camset(LV((-2.4,-.2,1.85),(-2.35,0,1.85),q),hp(Hz,-.12),34,4)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def PROPER_():
    Hz,Am=home_set(); Am['root'].location=(30,30,0); label('PROPER LAHORI',(-2.0,1.6,2.65),.2,size=.2,col='#7A1F1F'); sparkles((-2.0,1.6,1.8),.7,.2,DUR,n=18,size=.03)
    def upd(t):
        stand(Hz,t); blink(Hz,t); Hz['root'].rotation_euler[2]=R(20); face(Hz,mouth='grin',brow=.06); k=tl(t,0,.4); Hz['arm'][1].rotation_euler=(R(-30*k),0,R(-60*k)); Hz['arm'][-1].rotation_euler=(R(-150*k),0,R(10)); shk(Hz,1-k)
        q=ease(t/DUR); camset(LV((-2.6,-1.2,1.6),(-2.5,-1.0,1.6),q),hp(Hz,-.3),30,5.6)
    return dict(upd=upd)
SHOTS['PROPER']=PROPER_
def WAKES_():
    Hz,Am=home_set(); Am['root'].location=(30,30,0)
    def upd(t):
        blink(Hz,t,force=t<.5); k=tl(t,0,1.0)
        if t<1.0: sit(Hz,1,.75,legs=85); Hz['root'].location=(-4.6,2.0,0); Hz['root'].rotation_euler[2]=R(90); Hz['arm'][1].rotation_euler=(R(-160),0,R(-20)); Hz['arm'][-1].rotation_euler=(R(-160),0,R(20)); face(Hz,mouth='O',eyes=.3)
        else: walk_path(Hz,[(-4.2,1.8),(-2.0,1.6)],t,1.0,DUR-.2,step=.5); face(Hz,mouth='smile',eyes=.7)
        q=ease(t/DUR); camset(LV((-3.4,-1.8,2.2),(-3.0,-1.6,2.1),q),(-3.8,1.9,1.2),24,8)
    return dict(upd=upd)
SHOTS['WAKES']=WAKES_
def WAH_():
    Hz,Am=home_set(); Am['root'].location=(30,30,0)
    def upd(t):
        stand(Hz,t); blink(Hz,t); Hz['root'].location=(-2.0,1.3,0); Hz['root'].rotation_euler[2]=R(180); talk(Hz,t,*ln(39,47),rest='grin'); face(Hz,brow=.06); g=math.sin(t*4); Hz['arm'][1].rotation_euler=(R(-60-20*g),0,R(-20)); Hz['arm'][-1].rotation_euler=(R(-25),0,R(45))
        q=ease(t/DUR); camset(LV((-1.6,2.45,1.95),(-1.62,2.5,1.95),q),hp(Hz,-.08),30,2.8)
    return dict(upd=upd)
SHOTS['WAH']=WAH_
def SHOUTS_():
    Hz,Am=home_set(); Hz['root'].location=(30,30,0); b=bubble('HAMZA!!',(4.4,2.2,2.6),.3,size=.24,col='#7A1F1F',bg='#FFE0E6')
    def upd(t):
        stand(Am,t); blink(Am,t); Am['root'].location=(4.2,2.3,0); Am['root'].rotation_euler[2]=R(-60); mouth_talk(Am,t,.2,DUR,rate=6,shapes=('O','O','o','O')); face(Am,brow=-.05,brow_r=-14)
        arm_to(Am,1,(4.2,2.85,1.15),1,base=(-30,0,0)); Am['arm'][-1].rotation_euler=(R(-50),0,R(30))
        q=ease(t/DUR); camset(LV((2.4,-.6,2.0),(2.6,-.4,1.95),q),hp(Am,-.2),28,5.6)
    return dict(upd=upd)
SHOTS['SHOUTS']=SHOUTS_
def DOODH_():
    Hz,Am=home_set(); Hz['root'].location=(30,30,0)
    def upd(t):
        stand(Am,t); blink(Am,t); Am['root'].location=(4.2,2.3,0); Am['root'].rotation_euler[2]=R(-60); talk(Am,t,*ln(54,57),shapes=('O','o','O','flat')); face(Am,brow=-.05,brow_r=-16); gest(Am,t,-1,1.2,6,-60)
        q=ease(t/DUR); camset(LV((3.0,1.1,1.9),(3.1,1.25,1.9),q),hp(Am,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['DOODH']=DOODH_
def BUSY_():
    Hz,Am=home_set(); Am['root'].location=(30,30,0); ph=phone(Hz,1,1.4)
    def upd(t):
        stand(Hz,t); blink(Hz,t); Hz['root'].location=(-2.0,1.4,0); Hz['root'].rotation_euler[2]=R(20); hold_phone(Hz,1,1); Hz['head'].rotation_euler[0]=R(10); talk(Hz,t,*ln(58,61)); face(Hz,brow=.02,eyes=.7)
        q=ease(t/DUR); camset(LV((-2.4,-.1,1.85),(-2.38,.05,1.85),q),hp(Hz,-.1),34,2.8)
    return dict(upd=upd)
SHOTS['BUSY']=BUSY_
def BUSYQ_():
    Hz,Am=home_set(); ph=phone(Hz,1,1.4)
    def upd(t):
        stand(Hz,t); blink(Hz,t); Hz['root'].location=(-2.0,1.4,0); Hz['root'].rotation_euler[2]=R(20); hold_phone(Hz,1,1); Hz['head'].rotation_euler[0]=R(10); face(Hz,mouth='grin',eyes=.7)
        stand(Am,t); blink(Am,t); Am['root'].location=(.4,-.5,0); facep(Am,(-2.0,1.4)); talk(Am,t,*ln(62,72)); face(Am,brow=-.05,brow_r=-14); arm_to(Am,1,hp(Hz,-.5),tl(t,.4,.8),base=(-30,0,0)); Am['arm'][-1].rotation_euler=(R(-30),0,R(40))
        q=ease(t/DUR); camset(LV((-.9,-2.6,2.0),(-.8,-2.3,2.0),q),(-.8,.5,1.6),26,8)
    return dict(upd=upd)
SHOTS['BUSYQ']=BUSYQ_
def KEYS_():
    Hz,Am=home_set(); Am['root'].location=(.4,-.5,0); ky=in_hand(Hz,1,lambda e: keys(e,1.6))
    def upd(t):
        stand(Am,t); blink(Am,t); facep(Am,(-1.0,-1.0)); face(Am,mouth='frown',brow=-.05); walk_path(Hz,[(-2.0,1.4),(-1.4,-1.2),(-.6,-3.1)],t,0,DUR-.2,step=.55); blink(Hz,t); face(Hz,mouth='grin')
        Hz['arm'][1].rotation_euler=(R(-110),0,R(-20)); q=ease(t/DUR); camset(LV((-4.2,-2.6,2.0),(-4.0,-2.4,2.0),q),(hp(Hz)[0],hp(Hz)[1],1.5),26,8)
    return dict(upd=upd)
SHOTS['KEYS']=KEYS_
# ================================================================ SCENE 3 — friends at night
def FRIENDS_():
    nc,Hz,F1,F2,F3,W=ns_set(); label('THE LAHORI FRIENDS',(0,-4.5,3.0),.3,size=.22,col='#1B1F33',bg='#FFF3B0')
    def upd(t):
        nidle((Hz,F1,F2,F3),W,t); walk_path(Hz,[(-6,-4.6),(-.4,-3.4)],t,0,DUR-.3,step=.55)
        for H in (F1,F2,F3): facep(H,hp(Hz)); face(H,mouth='grin',brow=.04)
        q=ease(t/DUR); camset(LV((-4,-8.6,3.0),(-2.6,-8.2,2.6),q),(0,-4.4,1.4),24,8)
    return dict(upd=upd)
SHOTS['FRIENDS']=FRIENDS_
def fset():
    nc,Hz,F1,F2,F3,W=ns_set(); return nc,Hz,F1,F2,F3,W
def fidle(nc,Hz,F1,F2,F3,W,t):
    nidle((Hz,F1,F2,F3),W,t); facep(Hz,(.2,-4.8)); facep(F1,(-.4,-4.2)); facep(F2,(.2,-4.0)); facep(F3,(-.3,-4.0))
def CARGUY_():
    nc,Hz,F1,F2,F3,W=fset(); label('NEW CAR',(1.5,-2.6,1.9),.3,size=.2,col='#7A1F1F')
    def upd(t):
        fidle(nc,Hz,F1,F2,F3,W,t); facep(F1,(1.5,-2.6)); arm_to(F1,1,(1.5,-2.6,1.2),tl(t,.1,.4),base=(-30,0,0)); face(F1,mouth='grin',brow=.05)
        q=ease(t/DUR); camset(LV((4.6,-6.4,1.6),(4.2,-6.0,1.6),q),(1.4,-3.4,1.1),26,8)
    return dict(upd=upd)
SHOTS['CARGUY']=CARGUY_
def TRIP_():
    nc,Hz,F1,F2,F3,W=fset(); ph=phone(F2,1,1.6); b=bubble('MY TRIP PICS',(-1.6,-4.6,2.6),.3,size=.17,col='#1F4D3A',bg='#DFF5E1')
    def upd(t):
        fidle(nc,Hz,F1,F2,F3,W,t); facep(F2,(-.4,-6.6)); arm_to(F2,1,(-1.2,-5.4,1.7),tl(t,.1,.4),base=(-30,0,0)); face(F2,mouth='grin',brow=.05)
        q=ease(t/DUR); camset(LV((-1.0,-6.8,1.85),(-1.05,-6.55,1.85),q),hp(F2,-.2),32,4)
    return dict(upd=upd)
SHOTS['TRIP']=TRIP_
def THIRD_():
    nc,Hz,F1,F2,F3,W=fset(); b=bubble('NOBODY KNOWS LAHORE LIKE ME',(.4,-5.4,2.55),.5,size=.13,col='#4A2A6A',bg='#F3E6FF')
    def upd(t):
        fidle(nc,Hz,F1,F2,F3,W,t); facep(F3,(.4,-8)); mouth_talk(F3,t,.2,DUR,rate=8); gest(F3,t,1,1.3,7,-80); gest(F3,t+1,-1,1.3,7,-80); face(F3,brow=.05,brow_r=10)
        q=ease(t/DUR); camset(LV((.6,-7.3,1.8),(.55,-7.0,1.8),q),hp(F3,-.1),32,4)
    return dict(upd=upd)
SHOTS['THIRD']=THIRD_
def mk_talk(who,a,b,cam,lens=36,extra=None):
    def S_():
        nc,Hz,F1,F2,F3,W=fset(); P=dict(hz=Hz,f1=F1,f2=F2,f3=F3)
        def upd(t):
            fidle(nc,Hz,F1,F2,F3,W,t); H=P[who]; facep(H,cam[:2],.6,cam=cam[:2]); talk(H,t,*ln(a,b)); face(H,brow=.05,brow_r=10); gest(H,t,1,1.2,7,-75)
            if extra: extra(P,t)
            camset(LV(cam,(cam[0]*.98+hp(H)[0]*.02,cam[1]*.98+hp(H)[1]*.02,cam[2]),ease(t/DUR)),hp(H,-.05),lens,2.8)
        return dict(upd=upd)
    return S_
SHOTS['NAVI']=mk_talk('f1',112,116,(1.9,-5.9,1.95))
SHOTS['GAARI']=mk_talk('f2',117,124,(-2.2,-6.1,1.9))
SHOTS['BAS']=mk_talk('hz',125,131,(-.7,-2.0,1.95))
SHOTS['HOR']=mk_talk('f3',132,138,(.9,-6.9,1.85))
def ARGUE_():
    nc,Hz,F1,F2,F3,W=fset(); title_card('WHO IS THE BIGGEST LAHORI?',.4,(0,-4.5,3.1),.2)
    def upd(t):
        fidle(nc,Hz,F1,F2,F3,W,t)
        for i,H in enumerate((Hz,F1,F2,F3)): mouth_talk(H,t,.1*i,DUR,rate=9); gest(H,t+i,1,1.5,9,-90); face(H,brow=-.04,brow_r=-14); H['root'].location[2]=.05*abs(math.sin(t*8+i))
        q=ease(t/DUR); camset(LV((0,-9,2.4),(0,-8.2,2.2),q),(0,-4.4,1.5),26,8)
    return dict(upd=upd)
SHOTS['ARGUE']=ARGUE_
# ================================================================ SCENE 4 — tourist in the Walled City
def TOURIST_():
    Hz,To,W=wc_set(crowd=14); Hz['root'].location=(60,60,0); label('FOREIGN TOURIST',(0,0,0),99); lb=label('A FOREIGN TOURIST',(0,0,2.8),.5,size=.18,col='#1F3A6A',bg='#DFEBFF')
    def upd(t):
        upd_walkers(W,t); walk_path(To,[(26,0),(16,-.3)],t,0,DUR,step=.55); blink(To,t); face(To,mouth='O',brow=.05); p=To['root'].location; lb.location=(p[0],p[1],2.85)
        q=ease(t/DUR); camset(LV((10,-2.0,1.6),(11,-1.8,1.7),q),(26,0,3.0),24,8)
    return dict(upd=upd)
SHOTS['TOURIST']=TOURIST_
def SEES_():
    Hz,To,W=wc_set(crowd=14); Hz['root'].location=(60,60,0)
    def upd(t):
        upd_walkers(W,t+4); walk_path(To,[(16,-.3),(10,-.3)],t,0,DUR,step=.55); blink(To,t); face(To,mouth='O',brow=.06); To['head'].rotation_euler=(R(-15),0,R(25*math.sin(t*1.2)))
        q=ease(t/DUR); camset(LV((6,1.6,1.2),(6,1.6,1.4),q),LV((14,-3.5,7),(4,-3.5,6),q),20,16)
    return dict(upd=upd)
SHOTS['SEES']=SEES_
def wpos(Hz,To):
    Hz['root'].location=(0,.9,0); To['root'].location=(.2,-.6,0); facep(Hz,(.2,-.6)); facep(To,(0,.9))
def APPROACH_():
    Hz,To,W=wc_set()
    def upd(t):
        upd_walkers(W,t+8); stand(Hz,t); blink(Hz,t); Hz['root'].location=(0,.9,0); Hz['root'].rotation_euler[2]=R(120); face(Hz,mouth='smile'); walk_path(To,[(4.5,-1.2),(.2,-.6)],t,0,DUR-.2,step=.55); blink(To,t); face(To,mouth='smile')
        q=ease(t/DUR); camset(LV((-2.8,-2.6,1.8),(-2.6,-2.4,1.8),q),(1.0,.2,1.5),26,8)
    return dict(upd=upd)
SHOTS['APPROACH']=APPROACH_
def EXCUSE_():
    Hz,To,W=wc_set()
    def upd(t):
        widle(Hz,To,W,t); wpos(Hz,To); facep(To,(0,.9),.5,cam=(1.4,.8)); talk(To,t,*ln(170,176)); face(To,brow=.05,brow_r=10); gest(To,t,1,1.0,6,-70)
        q=ease(t/DUR); camset(LV((1.3,.8,2.0),(1.25,.95,2.0),q),hp(To,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['EXCUSE']=EXCUSE_
def DUMBEST_():
    Hz,To,W=wc_set(); label('DUMBEST QUESTION IN HISTORY',(0,.9,2.6),.6,size=.14,col='#7A1F1F')
    def upd(t):
        widle(Hz,To,W,t); wpos(Hz,To); facep(Hz,(.2,-.6),.6,cam=(-1.45,-.4)); face(Hz,mouth='flat',brow=-.05,brow_r=-20,eyes=.6); Hz['head'].rotation_euler[0]=R(-6)
        q=ease(t/DUR); camset(LV((-1.45,-.4,1.95),(-1.4,-.3,1.95),q),hp(Hz,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['DUMBEST']=DUMBEST_
def hz_line(a,b,lens=36,shout=False,card=None):
    def S_():
        Hz,To,W=wc_set()
        if card: title_card(card,.3,(0,.9,2.9),.15)
        def upd(t):
            widle(Hz,To,W,t); wpos(Hz,To); facep(Hz,(.2,-.6),.6,cam=(-1.45,-.4)); talk(Hz,t,*ln(a,b),shapes=('O','o','O','grin') if shout else ('o','flat','O','flat')); face(Hz,brow=.06 if shout else .02,brow_r=16 if shout else -6)
            if shout: k=tl(t,.2,.5); Hz['arm'][1].rotation_euler=(R(-160*k),0,R(-20)); Hz['arm'][-1].rotation_euler=(R(-40*k),0,R(40*k))
            else: arm_to(Hz,1,hp(To,-.4),tl(t,.2,.5),base=(-30,0,0))
            q=ease(t/DUR); camset(LV((-1.45,-.4,1.95),(-1.4,-.3,1.95),q),hp(Hz,-.1 if shout else -.05),lens if not shout else 30,2.8)
        return dict(upd=upd)
    return S_
SHOTS['PUTTAR']=hz_line(189,193)
SHOTS['JINHA']=hz_line(194,201,shout=True,card='JINHA LAHORE NI TAKKEYA, OH JAMMEYA HI NAI!')
def WHAT_():
    Hz,To,W=wc_set()
    def upd(t):
        widle(Hz,To,W,t); wpos(Hz,To); facep(To,(0,.9),.5,cam=(1.4,.8)); talk(To,t,*ln(202,202),shapes=('O','O')); face(To,brow=.09,brow_r=26,eyes=1.25); To['root'].rotation_euler[0]=R(-8)
        camset((1.2,.85,2.05),hp(To,-.05),44,2.8)
    return dict(upd=upd)
SHOTS['WHAT']=WHAT_
SHOTS['VEKH']=hz_line(203,209)
def DECIDES_():
    Hz,To,W=wc_set(); title_card('MISSION: EXPLORE LAHORE',.3,(.2,-.6,2.9),.16)
    def upd(t):
        widle(Hz,To,W,t); wpos(Hz,To); facep(To,(0,.9),.9,cam=(1.4,-2)); face(To,mouth='grin',brow=-.03,brow_r=-10); k=tl(t,.2,.5); To['arm'][1].rotation_euler=(R(-80*k),0,R(-60*k)); To['root'].rotation_euler[0]=R(-5*k)
        q=ease(t/DUR); camset(LV((1.4,-2.2,1.8),(1.3,-2.0,1.8),q),hp(To,-.2),30,4)
    return dict(upd=upd)
SHOTS['DECIDES']=DECIDES_
def OLDCITY_():
    Hz,To,W=wc_set(crowd=12); label('THE OLD CITY',(8,0,4.0),.2,size=.3,col='#7A1F1F')
    def upd(t):
        upd_walkers(W,t+12); walk_path(Hz,[(0,.4),(8,.4)],t,0,DUR,step=.55); walk_path(To,[(-.4,-.6),(7.6,-.6)],t,0,DUR,step=.55); blink(Hz,t); blink(To,t); face(Hz,mouth='grin'); face(To,mouth='O')
        arm_to(Hz,1,(12,3.5,5),.8,base=(-30,0,0))
        q=ease(t/DUR); camset(LV((11,-2.4,1.6),(12.5,-2.2,1.6),q),(hp(Hz)[0],0,1.8),24,8)
    return dict(upd=upd)
SHOTS['OLDCITY']=OLDCITY_
def ARCH_():
    Hz,To,W=wc_set(crowd=6); label('THE ARCHITECTURE',(26,0,9.0),.2,size=.45,col='#7A1F1F')
    def upd(t):
        upd_walkers(W,t+14); stand(Hz,t); blink(Hz,t); stand(To,t); blink(To,t); Hz['root'].location=(22,.6,0); To['root'].location=(22,-.6,0); Hz['root'].rotation_euler[2]=R(90); To['root'].rotation_euler[2]=R(90)
        arm_to(Hz,1,(29,0,8),1,base=(-30,0,0)); To['head'].rotation_euler[0]=R(-25)
        q=ease(t/DUR); camset(LV((17,-2.6,.8),(17.5,-2.4,.9),q),(29,0,7),22,16)
    return dict(upd=upd)
SHOTS['ARCH']=ARCH_
def FRNDS_():
    Hz,To,W=wc_set(crowd=4); f=[mk(c,x,y,rz,'fr%d'%i) for i,(c,x,y,rz) in enumerate(((CARGUY,1.2,1.4,200),(TRAVELER,2.2,.6,240),(LOREGUY,2.0,-.8,300)))]; label('MEET THE FRIENDS',(1.2,.3,2.9),.2,size=.2)
    def upd(t):
        widle(Hz,To,W,t); wpos(Hz,To)
        for i,H in enumerate(f): stand(H,t); blink(H,t); facep(H,(.2,-.6)); face(H,mouth='grin'); g=math.sin(t*6+i); H['arm'][1].rotation_euler=(R(-150+20*g),0,R(-20))
        face(To,mouth='grin'); To['arm'][1].rotation_euler=(R(-150),0,R(-20))
        q=ease(t/DUR); camset(LV((-2.6,-3.0,2.0),(-2.4,-2.8,2.0),q),(1.0,.2,1.5),26,8)
    return dict(upd=upd)
SHOTS['FRNDS']=FRNDS_
def PUNJABI_():
    Hz,To,W=wc_set(crowd=4); b=bubble('KI HAAL AE?',(0,.9,2.6),.1,size=.2,col='#7A1F1F'); b2=bubble('KEE HAAL AAY?',(.2,-.6,2.75),.8,size=.18,col='#1F3A6A',bg='#DFEBFF')
    def upd(t):
        widle(Hz,To,W,t); wpos(Hz,To); mouth_talk(Hz,t,0,.7); mouth_talk(To,t,.8,1.4); face(To,brow=.06,brow_r=14); gest(Hz,t,1,1.0,6,-70)
        q=ease(t/DUR); camset(LV((2.4,.2,1.9),(2.2,.2,1.9),q),(.1,.15,1.8),28,5.6)
    return dict(upd=upd)
SHOTS['PUNJABI']=PUNJABI_
def DAYS_():
    Hz,To,W=wc_set(crowd=6,tour=TOURIST_L); cc=clock_card((.2,-.6,3.0),.1,'DAY 1 ... DAY 7',spin=8)
    def upd(t):
        widle(Hz,To,W,t); wpos(Hz,To); facep(To,(1.4,-2.6)); k=min(1,(t*2.2)); To['root'].rotation_euler[2]+=R(360*ease(tl(t,.2,1.6))); face(To,mouth='grin',brow=.05); sparkles if False else None
        q=ease(t/DUR); camset(LV((1.6,-2.9,1.9),(1.4,-2.6,1.9),q),hp(To,-.4),28,5.6)
    return dict(upd=upd)
SHOTS['DAYS']=DAYS_
def NEWLOOK_():
    Hz,To,W=wc_set(crowd=10,tour=TOURIST_L); label('NEW LAHORI LOOK',(.2,-.6,2.85),.3,size=.18,col='#7A1F1F'); sparkles((.2,-.6,1.6),.8,.2,DUR,n=20,size=.03)
    def upd(t):
        upd_walkers(W,t+20); stand(Hz,t); blink(Hz,t); Hz['root'].location=(60,60,0); walk_path(To,[(-6,-.6),(2,-.6)],t,0,DUR,step=.55); blink(To,t); face(To,mouth='grin',brow=.05)
        g=math.sin(t*5); To['arm'][1].rotation_euler=(R(-150+20*g),0,R(-30)); To['head'].rotation_euler[2]=R(25*math.sin(t*2))
        q=ease(t/DUR); camset(LV((-3.4,-3.2,1.8),(-.2,-3.0,1.8),q),(hp(To)[0],hp(To)[1],1.9),28,8)
    return dict(upd=upd)
SHOTS['NEWLOOK']=NEWLOOK_
# ================================================================ SCENE 5/6 — Badshahi morning
def bm_set(crowd=0):
    W=bd_set('morning',crowd=crowd); To=mk(TOURIST_L,0,6,180,'tourist'); Hz=mk(HAMZA,0,1.5,180,'hamza'); return W,To,Hz
def bpos(To,Hz):
    To['root'].location=(0,6,0); Hz['root'].location=(.3,4.3,0); facep(To,(.3,4.3)); facep(Hz,(0,6))
def bidle(W,To,Hz,t):
    upd_walkers(W,t)
    for H in (To,Hz): stand(H,t); blink(H,t)
def MORNING_():
    W,To,Hz=bm_set(crowd=3)
    def upd(t):
        bidle(W,To,Hz,t); To['root'].location=(0,6,0); To['root'].rotation_euler[2]=0; face(To,mouth='smile'); walk_path(Hz,[(1.5,-1),(.3,4.3)],t,0,DUR,step=.55)
        q=ease(t/DUR); camset(LV((-3,-10,1.6),(-2,-7,1.8),q),(0,10,5),22,16)
    return dict(upd=upd)
SHOTS['MORNING']=MORNING_
def OYEH_():
    W,To,Hz=bm_set()
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); facep(To,(.3,4.3),.5,cam=(-1.0,4.6)); talk(To,t,*ln(265,269),shapes=('O','o','O','grin')); face(To,brow=.06); k=tl(t,0,.3); To['arm'][1].rotation_euler=(R(-30*k),0,R(-110*k)); To['arm'][-1].rotation_euler=(R(-30*k),0,R(110*k))
        q=ease(t/DUR); camset(LV((-1.0,4.4,2.05),(-.95,4.55,2.05),q),hp(To,-.15),32,4)
    return dict(upd=upd)
SHOTS['OYEH']=OYEH_
def POORA_():
    W,To,Hz=bm_set()
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); facep(Hz,(0,6),.5,cam=(1.4,5.6)); talk(Hz,t,*ln(270,276),shapes=('O','o','O','grin')); laugh(Hz,t,.4); arm_to(Hz,1,hp(To,-.4),tl(t,.1,.4),base=(-30,0,0))
        q=ease(t/DUR); camset(LV((1.3,5.6,2.0),(1.25,5.45,2.0),q),hp(Hz,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['POORA']=POORA_
def tclose(lens=40,dz=-.05,cam=(-1.0,4.6,2.05)):
    return cam,lens,dz
def ADJUSTS_():
    W,To,Hz=bm_set()
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); facep(To,(.3,4.3),.6,cam=(-.8,4.8)); headtouch(To,1,tl(t,.2,.5)*(1-tl(t,1.6,2.0)),dx=.45,dy=-.75,dz=.25); face(To,mouth='smile',brow=.02)
        q=ease(t/DUR); camset(LV((-.8,4.75,2.05),(-.75,4.85,2.05),q),hp(To,-.03),42,2.8)
    return dict(upd=upd)
SHOTS['ADJUSTS']=ADJUSTS_
def LOOKS_():
    W,To,Hz=bm_set()
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); face(To,mouth='flat',brow=-.02,brow_r=-8); look_at(To,hp(Hz),1)
        q=ease(t/DUR); camset(LV((1.4,5.0,1.95),(1.3,5.1,1.95),q),hp(To,-.1),34,4)
    return dict(upd=upd)
SHOTS['LOOKS']=LOOKS_
def CONF_():
    W,To,Hz=bm_set()
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); facep(To,(.3,4.3),.6,cam=(-.8,4.8)); face(To,mouth='smile',brow=-.03,brow_r=-12,eyes=.8); To['arm'][1].rotation_euler=(R(-25),0,R(-40)); To['arm'][-1].rotation_euler=(R(-25),0,R(40))
        q=ease(t/DUR); camset(LV((-.85,4.6,1.7),(-.8,4.7,1.8),q),hp(To,-.1),32,4)
    return dict(upd=upd)
SHOTS['CONF']=CONF_
def PAWA_():
    W,To,Hz=bm_set()
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); facep(To,(.3,4.3),.6,cam=(-.8,4.8)); talk(To,t,*ln(288,295),rest='smile'); face(To,brow=.0,brow_r=-8); arm_to(To,1,hp(To,-.9),tl(t,.8,1.2),base=(-30,0,0)); To['arm'][-1].rotation_euler=(R(-25),0,R(40))
        q=ease(t/DUR); camset(LV((-.8,4.75,2.05),(-.77,4.85,2.05),q),hp(To,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['PAWA']=PAWA_
def FREEZES_():
    W,To,Hz=bm_set()
    def upd(t):
        bidle(W,To,Hz,0); bpos(To,Hz); facep(Hz,(0,6),.5,cam=(1.4,5.6)); face(Hz,mouth='O',brow=.09,brow_r=26,eyes=1.25); Hz['root'].rotation_euler[0]=R(-6)
        camset((1.3,5.55,2.0),hp(Hz,-.05),44,2.8)
    return dict(upd=upd)
SHOTS['FREEZES']=FREEZES_
def AGGE_():
    W,To,Hz=bm_set()
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); facep(Hz,(0,6),.5,cam=(1.4,5.6)); talk(Hz,t,*ln(298,306),shapes=('O','o','O','flat')); face(Hz,brow=.08,brow_r=22); headtouch(Hz,-1,tl(t,.3,.6))
        q=ease(t/DUR); camset(LV((1.3,5.6,2.0),(1.25,5.5,2.0),q),hp(Hz,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['AGGE']=AGGE_
def RAISES_():
    W,To,Hz=bm_set(crowd=0)
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); Hz['root'].location=(1.5,4.8,0); To['root'].rotation_euler[2]=0; k=ease(tl(t,.3,1.4)); To['arm'][1].rotation_euler=(R(-170*k),0,R(-20)); To['arm'][-1].rotation_euler=(R(-170*k),0,R(20)); face(To,mouth='grin',brow=.06)
        q=ease(t/DUR); camset(LV((0,1.0,1.2),(0,1.6,1.3),q),(0,6,2.6),24,8)
    return dict(upd=upd)
SHOTS['RAISES']=RAISES_
def AYYY_():
    W,To,Hz=bm_set(crowd=6); title_card('LAHORE LAHORE AYYY!',.1,(0,6,3.3),.32); sparkles((0,6,3),2.5,.1,DUR,n=50,size=.06)
    def upd(t):
        bidle(W,To,Hz,t); bpos(To,Hz); Hz['root'].location=(1.5,4.8,0); To['root'].rotation_euler[2]=0; talk(To,t,*ln(314,316),shapes=('O','O','O','O')); face(To,brow=.07); g=math.sin(t*9); To['arm'][1].rotation_euler=(R(-165+15*g),0,R(-20)); To['arm'][-1].rotation_euler=(R(-165-15*g),0,R(20))
        To['root'].location[2]=.1*abs(math.sin(t*6))
        q=ease(t/DUR); camset(LV((0,2.0,1.7),(0,2.6,1.8),q),(0,6,2.4),26,8)
    return dict(upd=upd)
SHOTS['AYYY']=AYYY_
def JOINS_():
    W,To,Hz=bm_set(); C=crowd_at(14,0,6,1.6,4.5,seed=8); sparkles((0,6,3),4,.1,DUR,n=60,size=.07)
    def upd(t):
        upd_walkers(W,t); bpos(To,Hz); stand(To,t); stand(Hz,t)
        for H in [To,Hz]+C: pass
        cr_idle(C+[To,Hz],t,face=(0,-4),mode='cheer')
        q=ease(t/DUR); camset(LV((-2,-6,3.0),(-1,-4.5,2.6),q),(0,5.5,1.8),22,12)
    return dict(upd=upd)
SHOTS['JOINS']=JOINS_
def LOOKCAM_():
    W,To,Hz=bm_set(); C=crowd_at(10,0,6,1.6,4.5,seed=8)
    def upd(t):
        upd_walkers(W,t); bpos(To,Hz); stand(To,t); stand(Hz,t); cr_idle(C+[To],t,face=(0,-4),mode='cheer'); Hz['root'].rotation_euler[2]=R(lerp_angle(face_dir(-.3,1.7),0,ease(tl(t,.2,1.0)))); face(Hz,mouth='smile',brow=.03)
        q=ease(t/DUR); camset(LV((.3,2.4,1.95),(.3,2.6,1.95),q),hp(Hz,-.1),34,4)
    return dict(upd=upd)
SHOTS['LOOKCAM']=LOOKCAM_
def EMOTION_():
    W,To,Hz=bm_set(); C=crowd_at(10,0,6,1.6,4.5,seed=8); hearts(lambda t: hp(Hz,.35),1.6,DUR,n=8)
    def upd(t):
        upd_walkers(W,t); bpos(To,Hz); stand(To,t); stand(Hz,t); cr_idle(C+[To],t,face=(0,-4),mode='cheer'); Hz['root'].rotation_euler[2]=0; talk(Hz,t,*ln(327,335),rest='smile'); face(Hz,brow=.03); headtouch(Hz,-1,tl(t,1.6,2.0),dx=.1,dy=-1.2,dz=-1.4)
        q=ease(t/DUR); camset(LV((.3,2.6,1.95),(.3,2.75,1.95),q),hp(Hz,-.08),38,2.8)
    return dict(upd=upd)
SHOTS['EMOTION']=EMOTION_
def FINALTXT_():
    ui_world(); e=empty((0,0,-200)); text('JINHA LAHORE NI TAKKEYA,',(0,0,.3),(0,-1,0),.19,M('#FFF3B0',.4,emit=2.5),ex=0,parent=e); text('OH JAMMEYA HI NAI!',(0,0,-.15),(0,-1,0),.24,M('#FFF3B0',.4,emit=2.5),ex=0,parent=e)
    def upd(t):
        k=pop(t-.1) if t>.1 else 0; e.scale=(k,k,k); camset((0,-L(7.4,6.9,ease(t/DUR)),-200),(0,0,-200),50,22)
    return dict(upd=upd)
SHOTS['FINALTXT']=FINALTXT_
W_=json.load(open(LH+'/audio/words.json'))
