# Shots for "Sea View". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=105.4
SEQ=[('OPEN', 0.0), ('MISSION', 1.21), ('ROMANCE', 5.71), ('FAMILYT', 7.14), ('BORED', 8.49), ('SEAVIEW', 12.74), ('MEET', 14.73), ('FINALLY', 18.24), ('PEACE', 22.26), ('UTRAY', 24.57), ('CHAI', 26.3), ('COUPLE', 28.66), ('SPECIAL', 31.03), ('AWW', 33.3), ('PARKING', 34.49), ('INSULT', 36.24), ('FAMILY', 39.1), ('SAB', 44.71), ('ITNA', 46.11), ('GHAR', 47.48), ('SAMANDAR', 49.43), ('PLATE', 51.11), ('HUNGER', 52.87), ('ORDER', 55.07), ('DINNER', 57.97), ('TOH', 59.88), ('TABHI', 63.21), ('BOYCOMES', 63.96), ('LOST', 67.58), ('STOPJOKE', 70.32), ('SHOULDERS', 72.25), ('MOTHER', 77.96), ('THANKS', 81.24), ('KOIBAAT', 82.66), ('REASONS', 85.37), ('STORYL', 87.81), ('NARR', 92.31), ('SHOR', 94.15), ('GHARQ', 99.67), ('HAAN', 100.53), ('PEHLE', 101.04), ('BRO', 102.55)]
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
def fit_cam(o,w,h,k,ymin=-.12,ymax=.86,xm=.93):
    # keep a camera-facing card fully inside the frame: shrink if too wide, then slide it in
    if k<=0: return
    c=Vector(CAM.location); f=(Vector(TGT.location)-c).normalized(); r=f.cross(Vector((0,0,1))).normalized(); u=r.cross(f)
    th=10.125/CAM.data.lens; tv=18.0/CAM.data.lens
    par=o.parent.matrix_world if o.parent else None
    p=o.matrix_world.translation if par else Vector(o.location); v=p-c; z=v.dot(f)
    if z<=.2: return
    hw=w*k/(z*th); s=1.0
    if hw>xm: s=xm/hw; hw=xm
    hh=h*k*s/(z*tv); x=v.dot(r)/(z*th); y=v.dot(u)/(z*tv)
    nx=max(-xm+hw,min(xm-hw,x)); ny=max(ymin+hh,min(ymax-hh,y))
    o.scale=(k*s,k*s,k*s)
    if par is None: o.location=Vector(o.location)+r*((nx-x)*z*th)+u*((ny-y)*z*tv)
def bubble(body,loc,t0,size=.2,col='#16171C',bg='#FFFFFF',w=None,dur=99):
    e=empty(loc); w=w or (len(body)*size*.34+min(.2,size*1.1)); obox((0,.03,0),(w,.02,size*.9),M(bg,.5,emit=.5),size*.5,e); text(body,(0,0,0),(0,-1,0),size,M(col,.5,emit=.2),ex=.005,parent=e); e.scale=(0,0,0)
    def fn(o,t):
        k=pop(t-t0) if t0<=t<t0+dur else 0; o.scale=(k,k,k); o.location=loc; face_cam(o); fit_cam(o,w,size*.9,k)
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
ALLH=[]; _abd0=avatar_bd
def avatar_bd(*a,**k):
    H=_abd0(*a,**k); ALLH.append(H); return H
def walkers(n,seed,x0,x1,ys,z=0.0):
    # one direction and one speed per lane, evenly spaced: nobody walks through anybody
    r=random.Random(seed); P=[]; per=max(1,-(-n//len(ys))); L_=x1-x0
    for li,y in enumerate(ys):
        d=1 if li%2==0 else -1
        for i in range(per):
            if len(P)>=n: break
            H=avatar_bd((0,y,z),90*d,person(seed*100+li*20+i),name='w%d_%d_%d'%(seed,li,i)); P.append(dict(H=H,x0=x0+L_*(i+r.uniform(.15,.55))/per,y=y,d=d,v=1.0,a=x0,b=x1))
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
        k=pop(t-t0) if t>=t0 else 0; o.scale=(k,k,k); o.location=loc; face_cam(o); fit_cam(o,len(body)*size*.32+.4,size*.75,k)
    fx.add(e,fn); return e



# ================================================================ set + helpers
def _st():
    st=[0]+[i+1 for i,w in enumerate(W_[:-1]) if w['w'][-1] in '.!?"…']; return st
def sg(a,b=None):
    st=_st(); b=a if b is None else b; e=(st[b+1]-1) if b+1<len(st) else len(W_)-1; return (W_[st[a]]['s'],W_[e]['e'])
FR0={'da':(-1.1,-5.4),'sh':(0,-4.8),'bi':(1.1,-5.4)}
def beach(crowd=10,seed=3,extras=True,hero=False,lanes=(-2.45,6.3)):
    sea,lamps=surf_set(); hc=hero_car() if hero else None; pc=parked_cars(hero=hc)
    stall(-4,-6.8,'corn','#2B8A5A','BHUTTA'); stall(-1.2,-6.8,'chaat','#C8372D','CHAAT'); stall(1.8,-6.8,'chai','#7448C2','CHAI'); stall(4.8,-6.8,'ice','#2B5AA8','ICE CREAM')
    for (x,y,c,rz) in ((-14,2,'#C8372D',10),(-18,4,'#2B8A5A',-15),(16,3,'#F2C14E',5)): mat((x,y,.01),c,rz)
    mat((10,1,.01),'#7448C2',0)
    cm=camel((-7,3.4,0),-60); hs=horse((13.2,4.0,0),30); bl=balloons((-9.5,-.6,0))
    sun=empty((-8,90,9)); oico((0,0,0),5.5,M('#FFC870',.3,emit=7),sun,sub=2)
    B.done('beach'); setup_world('golden',shadow=50)
    P=dict(da=mk(DANI,*FR0['da'],180,'dani'),sh=mk(SHERRY,*FR0['sh'],180,'sherry'),bi=mk(BILAL,*FR0['bi'],180,'bilal'))
    W=walkers(crowd,seed,-26,26,lanes) if crowd else []
    vend=mk(VENDOR,-9.5,-.2,180,'vendor')
    return dict(sea=sea,cm=cm,hs=hs,P=P,W=W,vend=vend,hc=hc)
def bidle(S,t,skip=()):
    for i,e in enumerate(S['sea']): e.location[1]=12+i*1.6-.9*math.sin(t*1.2+i*.9); e.scale[0]=1
    upd_walkers(S['W'],t+3); S['cm'].rotation_euler[2]=R(-60+3*math.sin(t*.7)); S['hs'].location[2]=.03*abs(math.sin(t*3))
    stand(S['vend'],t); blink(S['vend'],t)
    for k,H in S['P'].items():
        if k not in skip: stand(H,t); blink(H,t)
def fpos(S,face=None):
    for k,(x,y) in FR0.items():
        H=S['P'][k]; H['root'].location=(x,y,0)
        if face: facep(H,face)
def add(S,key,C,x,y,rz):
    S['P'][key]=mk(C,x,y,rz,key); return S['P'][key]
def tk(S,key,a,b=None,cam=None,lens=36,tgt=-.05,**kw):
    H=S['P'][key]; return H
# ================================================================ HOOK
def OPEN_():
    S=beach(crowd=16); fpos(S)
    def upd(t):
        bidle(S,t); q=ease(t/DUR); camset(LV((-24,-6,9),(-16,-4,6),q),(4,10,1.0),22,22)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def MISSION_():
    S=beach(crowd=28); fpos(S); title_card('EVERYONE HAS A MISSION',.3,(0,2,3.4),.26)
    a=add(S,'bf',BOYF,-12.4,8,180); b=add(S,'gf',GIRLF,-11.15,8.5,180); am=add(S,'am',AMMI,9.3,1.6,0); ab=add(S,'ab',ABBU,11.3,1.4,0); kd=add(S,'kd',KID,10.3,.4,0)
    def upd(t):
        bidle(S,t); sit(ab,1,.05,legs=90); q=ease(t/DUR); camset(LV((0,-6,4.5),(0,-4,3.6),q),(0,4,1.2),20,22)
    return dict(upd=upd)
SHOTS['MISSION']=MISSION_
def ROMANCE_():
    S=beach(crowd=4); fpos(S); a=add(S,'bf',BOYF,-12.4,8,180); b=add(S,'gf',GIRLF,-11.15,8.5,180); hearts(lambda t:(-12,8,2.6),.2,DUR,n=6)
    def upd(t):
        bidle(S,t); arm_to(a,-1,hp(b,-.7),.8,base=(-30,0,0)); arm_to(b,1,hp(a,-.7),.8,base=(-30,0,0))
        q=ease(t/DUR); camset(LV((-14.5,4.2,1.4),(-13.8,4.6,1.5),q),(-12,8.5,1.5),26,8)
    return dict(upd=upd)
SHOTS['ROMANCE']=ROMANCE_
def FAMILYT_():
    S=beach(crowd=4); fpos(S); am=add(S,'am',AMMI,9.3,1.6,0); ab=add(S,'ab',ABBU,11.3,1.4,0); kd=add(S,'kd',KID,10.3,.4,0)
    for k in range(4): e=empty((9.98+.2*k,1.25,.02)); plate_food(e,1.3)
    def upd(t):
        bidle(S,t); sit(ab,1,.05,legs=90); sit(am,1,.05,legs=90); face(am,mouth='grin'); face(ab,mouth='smile'); kd['root'].location[2]=.1*abs(math.sin(t*5)); face(kd,mouth='grin')
        q=ease(t/DUR); camset(LV((10.5,-2.9,1.6),(10.3,-2.5,1.6),q),(10.3,1.0,.75),21,8)
    return dict(upd=upd)
SHOTS['FAMILYT']=FAMILYT_
def BORED_():
    S=beach(crowd=4); fpos(S); g=add(S,'bg',dict(person(77),h=1.0),-14.0,-8.3,180); ph=phone(g,1,1.4); label('GHAR MEIN BORE HO RAHE THAY',(-14.0,-8.3,2.6),.3,size=.14)
    def upd(t):
        bidle(S,t); sit(g,1,1.2,legs=85); g['root'].location=(-14.0,-8.85,0); hold_phone(g,1,1); g['head'].rotation_euler[0]=R(18); face(g,mouth='O' if (t%2)<.6 else 'flat',eyes=.4)
        q=ease(t/DUR); camset(LV((-13.2,-5.6,1.7),(-13.4,-6.0,1.7),q),hp(g,-.3),30,4)
    return dict(upd=upd)
SHOTS['BORED']=BORED_
def SEAVIEW_():
    S=beach(crowd=18); fpos(S); title_card('SEA VIEW',.2,(0,6,4.5),.8); sparkles((0,6,4),5,.2,DUR,n=40,size=.08)
    def upd(t):
        bidle(S,t); q=ease(t/DUR); camset(LV((10,-8,2.4),(4,-6,4.0),q),(-2,8,2.6),18,22)
    return dict(upd=upd)
SHOTS['SEAVIEW']=SEAVIEW_
# ================================================================ SCENE 1 — friends
SEATS={'da':(0,-.9,.8),'sh':(0,.9,.8),'bi':(-1.9,0,.95)}
def incar(S,t,lean=0.0):
    """seat the three friends in the hero car: nothing clips - legs under the dash, arms beside the seats, driver's hands on the wheel"""
    for k,(x,y,sh_) in SEATS.items():
        H=S['P'][k]; px=x+(lean if k=='bi' else 0); w=cw((px,y,0)); H['root'].location=(w[0],w[1],0); facep(H,cw((px+30,y,0))); sit(H,1,sh_,legs=90); blink(H,t)
        H['head'].rotation_euler=(0,0,0)
        for q in (1,-1): H['arm'][q].rotation_euler=(R(-14),0,0)
    D=S['P']['da']; b=.012*math.sin(t*1.7)
    arm_to(D,1,cw((.66,-.7,1.6+b)),1); arm_to(D,-1,cw((.66,-1.1,1.6-b)),1)
def cidle(S,t): bidle(S,t,skip=('da','sh','bi'))
def MEET_():
    S=beach(crowd=6,hero=True)
    for i,(k,nm,c,z) in enumerate((('da','DANI','#1F3A6A',3.4),('sh','SHERRY','#7A1F1F',3.4),('bi','BILAL','#1F4D3A',3.95))): x,y,_=SEATS[k]; label(nm,cw((x,y,z)),.3+.5*i,size=.24,col=c)
    def upd(t):
        cidle(S,t); incar(S,t); face(S['P']['da'],mouth='grin'); face(S['P']['sh'],mouth='flat',brow=-.03); face(S['P']['bi'],mouth='smile')
        q=ease(t/DUR); camset(LV(cw((5.6,.3,2.55)),cw((4.7,.1,2.5)),q),cw((0,0,2.45)),24,8)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def ctalk(key,a,b,cam,lens=36,extra=None,turn=None,lean=0.0,tz=-.05):
    def S_():
        S=beach(crowd=4,hero=True)
        def upd(t):
            cidle(S,t); incar(S,t,lean); H=S['P'][key]; talk(H,t,*sg(a,b)); face(H,brow=.05)
            for k,o in S['P'].items():
                if k!=key: look_at(o,hp(H),.5,maxyaw=50)
            if turn: look_at(H,hp(S['P'][turn]),.45,maxyaw=40)
            if extra: extra(S,t)
            q=ease(t/DUR); c0=cw(cam); c1=(c0[0]+(hp(H)[0]-c0[0])*.06,c0[1]+(hp(H)[1]-c0[1])*.06,c0[2]); camset(LV(c0,c1,q),hp(H,tz),lens,2.8)
        return dict(upd=upd)
    return S_
def _fin(S,t):
    H=S['P']['da']; k=tl(t,.1,.5); g=math.sin(t*9)*6*k; H['arm'][1].rotation_euler=(R(-14-92*k+g),0,R(-8*k)); H['head'].rotation_euler[0]=R(-8*k); face(H,mouth='grin',brow=.06)
def _peace(S,t): H=S['P']['sh']; gest(H,t,-1,1.2,8,-78); face(H,brow=-.05,brow_r=-16)
def _utr(S,t): H=S['P']['bi']; face(H,mouth='flat',brow=-.02,brow_r=-6); H['head'].rotation_euler[0]=R(6)
SHOTS['FINALLY']=ctalk('da',7,8,(3.0,-.45,2.1),extra=_fin)
SHOTS['PEACE']=ctalk('sh',9,10,(3.0,.5,2.1),extra=_peace,turn='da')
SHOTS['UTRAY']=ctalk('bi',11,11,(.4,0,2.4),lens=21,extra=_utr,lean=.45,tz=0)
def CHAI_():
    S=beach(crowd=4,hero=True); b=bubble('CHAI ONLY',cw((.7,-.7,2.66)),.3,size=.12,col='#6A2A6A',bg='#F3E6FF')
    def upd(t):
        cidle(S,t); incar(S,t); H=S['P']['sh']; talk(H,t,*sg(12)); face(H,brow=.02,eyes=.7)
        for k in ('da','bi'): look_at(S['P'][k],hp(H),.6,maxyaw=50); face(S['P'][k],mouth='flat',brow=-.04,brow_r=-14)
        q=ease(t/DUR); camset(LV(cw((3.6,.25,2.15)),cw((3.4,.3,2.15)),q),cw((0,.45,2.1)),30,4)
    return dict(upd=upd)
SHOTS['CHAI']=CHAI_
# ================================================================ SCENE 2 — couple
def cset():
    S=beach(crowd=4); fpos(S); a=add(S,'bf',BOYF,-12.4,8,180); b=add(S,'gf',GIRLF,-11.15,8.5,180); return S,a,b
def COUPLE_():
    S,a,b=cset(); label('THE COUPLE',(-12,8,2.7),.3,size=.2,col='#7A1F4A',bg='#FFE0F0')
    def upd(t):
        bidle(S,t); arm_to(a,-1,(b['root'].location[0]-.5,b['root'].location[1]-.3,1.8),.8,base=(-30,0,0)); face(a,mouth='smile'); face(b,mouth='smile')
        q=ease(t/DUR); camset(LV((-12,2.4,1.5),(-12,3.6,1.5),q),(-12,8.5,1.6),24,8)
    return dict(upd=upd)
SHOTS['COUPLE']=COUPLE_
def ctalk(who,a_,b_=None,mood='smile',extra=None):
    def S_():
        S,a,b=cset()
        def upd(t):
            bidle(S,t); facep(a,(-11.6,8)); facep(b,(-12.4,8)); H=a if who=='a' else b; O=b if who=='a' else a
            cam=(-11.75,6.4,1.95) if who=='b' else (-12.25,6.4,1.95)
            facep(H,(-11.6,8) if who=='a' else (-12.4,8),.55,cam=cam[:2]); talk(H,t,*sg(a_,b_)); face(O,mouth=mood); look_at(O,hp(H),.8)
            if extra: extra(a,b,t)
            q=ease(t/DUR); camset(LV(cam,(cam[0],cam[1]+.15,cam[2]),q),hp(H,-.05),36,2.8)
        return dict(upd=upd)
    return S_
def _ins(a,b,t): face(b,brow=-.06,brow_r=-22); b['arm'][1].rotation_euler=(R(-30),0,R(-45)); b['arm'][-1].rotation_euler=(R(-30),0,R(45))
def _pk(a,b,t): face(a,brow=.05); a['arm'][1].rotation_euler=(R(-120),0,R(-20))
SHOTS['SPECIAL']=ctalk('a',14)
SHOTS['AWW']=ctalk('b',15,mood='smile')
SHOTS['PARKING']=ctalk('a',16,mood='O',extra=_pk)
def INSULT_():
    S,a,b=cset(); 
    def upd(t):
        bidle(S,t); facep(a,(-11.6,8)); facep(b,(-12.4,8),.5,cam=(-10.9,5.8)); talk(b,t,*sg(17)); face(b,brow=-.07,brow_r=-24); b['arm'][1].rotation_euler=(R(-30),0,R(-45)); b['arm'][-1].rotation_euler=(R(-30),0,R(45))
        face(a,mouth='O',brow=.06); a['root'].rotation_euler[0]=R(6*tl(t,.4,.8))
        q=ease(t/DUR); camset(LV((-10.9,5.5,1.85),(-10.9,5.8,1.85),q),hp(b,-.1),32,5.6)
    return dict(upd=upd)
SHOTS['INSULT']=INSULT_
# ================================================================ SCENE 3 — family
def famset():
    S=beach(crowd=4,lanes=(6.3,)); fpos(S); am=add(S,'am',AMMI,9.3,1.7,0); ab=add(S,'ab',ABBU,11.3,1.5,0); kd=add(S,'kd',KID,10.3,.2,0)
    pl=[]
    for k in range(5): e=empty((9.3+.35*k,1.0+.15*(k%2),.02)); plate_food(e,1.4); e.scale=(0,0,0); pl.append(e)
    return S,am,ab,kd,pl
def FAMILY_():
    S,am,ab,kd,pl=famset(); bags=[in_hand(am,s,lambda e: foodbag2(e,1.8,c)) for s,c in ((1,'#F4F1EA'),(-1,'#C8372D'))]+[in_hand(ab,s,lambda e: foodbag2(e,1.8,c)) for s,c in ((1,'#2B5AA8'),(-1,'#F2C14E'))]
    label('SO MUCH FOOD',(10,0,2.6),2.0,size=.2,col='#7A3A10')
    def upd(t):
        bidle(S,t)
        for H,p0,p1 in ((am,(8.9,-5),(9.3,1.7)),(ab,(10.9,-5.4),(11.3,1.5)),(kd,(9.9,-6.6),(10.3,.2))): walk_path(H,[p0,p1],t,0,DUR-.5,step=.5); blink(H,t); face(H,mouth='grin')
        for H in (am,ab):
            for s in (1,-1): H['arm'][s].rotation_euler=(R(-15),0,R(s*-12))
        q=ease(t/DUR); m_=((am['root'].location[0]+ab['root'].location[0])/2,(am['root'].location[1]+ab['root'].location[1])/2,1.25); camset(LV((14.8,-1.6,1.8),(14.4,-.6,1.8),q),m_,24,8)
    return dict(upd=upd)
SHOTS['FAMILY']=FAMILY_
def fidle(S,am,ab,kd,pl,t,plates=True):
    bidle(S,t); am['root'].location=(9.3,1.7,0); ab['root'].location=(11.3,1.5,0); kd['root'].location=(10.3,.2,0)
    facep(am,(10.1,.6)); facep(ab,(9.6,1.2)); facep(kd,(9.3,1.6))
    for e in pl: k=1 if plates else 0; e.scale=(k,k,k)
def SAB_():
    S,am,ab,kd,pl=famset()
    def upd(t):
        fidle(S,am,ab,kd,pl,t,plates=False)
        for i,e in enumerate(pl): k=pop(t-.4-.18*i) if t>.4+.18*i else 0; e.scale=(k,k,k)
        facep(am,(9.4,-1.2)); talk(am,t,*sg(19,20)); face(am,brow=-.03,brow_r=-10); g=math.sin(t*6); am['arm'][1].rotation_euler=(R(-150+20*g),0,R(-20)); am['arm'][-1].rotation_euler=(R(-60),0,R(30))
        q=ease(t/DUR); camset(LV((9.3,-.9,1.9),(9.32,-.75,1.9),q),hp(am,-.08),34,2.8)
    return dict(upd=upd)
SHOTS['SAB']=SAB_
def ITNA_():
    S,am,ab,kd,pl=famset()
    def upd(t):
        fidle(S,am,ab,kd,pl,t); facep(ab,(9.3,1.7),.6,cam=(11.4,-.2)); talk(ab,t,*sg(21)); face(ab,brow=.06,brow_r=16); ab['arm'][1].rotation_euler=(R(-60),0,R(-60)); ab['arm'][-1].rotation_euler=(R(-60),0,R(60))
        q=ease(t/DUR); camset(LV((11.4,-.3,1.95),(11.38,-.15,1.95),q),hp(ab,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['ITNA']=ITNA_
def GHAR_():
    S,am,ab,kd,pl=famset()
    def upd(t):
        fidle(S,am,ab,kd,pl,t); facep(am,(11.3,1.5),.6,cam=(8.6,-.1)); talk(am,t,*sg(22),rest='grin'); face(am,brow=.02); am['arm'][1].rotation_euler=(R(-40),0,R(-60))
        q=ease(t/DUR); camset(LV((8.6,-.2,1.9),(8.62,-.05,1.9),q),hp(am,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['GHAR']=GHAR_
def SAMANDAR_():
    S,am,ab,kd,pl=famset()
    def upd(t):
        fidle(S,am,ab,kd,pl,t); facep(kd,(9.3,1.7),.85,cam=(10.1,-1.8)); talk(kd,t,*sg(23)); face(kd,brow=.06,brow_r=14); arm_to(kd,1,(10.5,12,1.5),tl(t,.2,.5),base=(-30,0,0)); kd['root'].location[2]=.06*abs(math.sin(t*7))
        q=ease(t/DUR); camset(LV((10.1,-1.4,1.2),(10.1,-1.25,1.2),q),hp(kd,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['SAMANDAR']=SAMANDAR_
def PLATE_():
    S,am,ab,kd,pl=famset()
    def upd(t):
        fidle(S,am,ab,kd,pl,t); facep(am,(10.3,.2)); talk(am,t,*sg(24),shapes=('O','o','O','flat')); face(am,brow=-.06,brow_r=-22); arm_to(am,1,hp(kd,-.3),tl(t,.1,.35),base=(-30,0,0))
        face(kd,mouth='frown',brow=.05); kd['head'].rotation_euler[0]=R(15)
        q=ease(t/DUR); camset(LV((8.0,-.8,1.6),(8.2,-.6,1.6),q),(9.8,.9,1.3),28,5.6)
    return dict(upd=upd)
SHOTS['PLATE']=PLATE_
# ================================================================ SCENE 4 — food
SP={'da':(-.9,-5.2),'sh':(1.0,-5.9),'bi':(-2.6,-4.0)}
def spos(S):
    for k,(x,y) in SP.items(): S['P'][k]['root'].location=(x,y,0)
def stallset(lanes=(6.3,)):
    S=beach(crowd=6,lanes=lanes); spos(S); v=[mk(VENDOR,x,-7.3,180,'v%d'%i) for i,x in enumerate((-4,-1.2,1.8,4.8))]; return S,v
def sidle(S,v,t):
    bidle(S,t)
    for H in v: stand(H,t); blink(H,t); H['root'].rotation_euler[2]=R(180)
def HUNGER_():
    S,v=stallset()
    def upd(t):
        sidle(S,v,t); spos(S); sh=S['P']['sh']; walk_path(sh,[(1.0,-4.2),(1.0,-5.9)],t,0,1.2,step=.45); face(sh,mouth='grin',brow=.06,eyes=.6)
        if t>1.2: facep(sh,(1.8,-7.3))
        q=ease(t/DUR); camset(LV((1.9,-1.6,1.5),(1.7,-2.2,1.5),q),(1.2,-6.4,1.85),26,8)
    return dict(upd=upd)
SHOTS['HUNGER']=HUNGER_
def ORDER_():
    S,v=stallset(); items=[]
    for i,txt in enumerate(('CORN','FRIES','CHANA CHAAT','ICE CREAM')): items.append(label(txt,(.25,-5.9,2.3-.18*i),.4+.65*i,size=.05,col='#7A3A10'))
    def upd(t):
        sidle(S,v,t); spos(S); sh=S['P']['sh']; sh['root'].location=(1.0,-5.9,0); facep(sh,(1.8,-7.3),.55,cam=(.3,-7.3)); talk(sh,t,*sg(26),rate=10); face(sh,brow=.05); gest(sh,t,1,1.4,9,-90)
        q=ease(t/DUR); h_=hp(sh); camset(LV((.3,-7.3,1.95),(.32,-7.22,1.95),q),(h_[0]-.27,h_[1]+.135,h_[2]+.02),20,4)
    return dict(upd=upd)
SHOTS['ORDER']=ORDER_
def DINNER_():
    S,v=stallset()
    def upd(t):
        sidle(S,v,t); spos(S); sh=S['P']['sh']; sh['root'].location=(1.0,-5.9,0); da=S['P']['da']; facep(da,(1.0,-5.9),.6,cam=(-.3,-3.0)); talk(da,t,*sg(27)); face(da,brow=.07,brow_r=18)
        da['arm'][1].rotation_euler=(R(-70),0,R(-50)); da['arm'][-1].rotation_euler=(R(-70),0,R(50))
        q=ease(t/DUR); camset(LV((-.3,-3.0,1.95),(-.3,-3.15,1.95),q),hp(da,.0),34,2.8)
    return dict(upd=upd)
SHOTS['DINNER']=DINNER_
def TOH_():
    S,v=stallset(); cn=in_hand(S['P']['sh'],1,lambda e: corn_cob(e,1.8))
    def upd(t):
        sidle(S,v,t); spos(S); sh=S['P']['sh']; sh['root'].location=(1.0,-5.9,0); facep(sh,(-.9,-5.2),.6,cam=(1.5,-3.0)); talk(sh,t,*sg(28,29),rest='grin'); face(sh,brow=.02,eyes=.8)
        arm_to(sh,1,hp(sh,-.3),.5+.5*abs(math.sin(t*2)),base=(-30,0,0))
        q=ease(t/DUR); camset(LV((1.5,-2.5,1.9),(1.48,-2.7,1.9),q),hp(sh,.1),26,4)
    return dict(upd=upd)
SHOTS['TOH']=TOH_
# ================================================================ SCENE 5 — the lost boy
def lset():
    S,v=stallset(lanes=(6.3,)); lb=add(S,'lb',LOST,.3,-3.8,0); return S,v,lb
def TABHI_():
    S,v,lb=lset(); lb['root'].location=(30,30,0)
    def upd(t):
        sidle(S,v,0); spos(S); S['P']['sh']['root'].location=(1.0,-5.9,0)
        for k in ('da','sh','bi'): face(S['P'][k],mouth='flat',brow=.03)
        q=ease(t/DUR); camset(LV((-1.6,1.2,1.8),(-1.6,.8,1.8),q),(-1.6,-5.2,1.8),18,8)
    return dict(upd=upd)
SHOTS['TABHI']=TABHI_
def BOYCOMES_():
    S,v,lb=lset()
    def upd(t):
        sidle(S,v,t); spos(S); S['P']['sh']['root'].location=(1.0,-5.9,0); walk_path(lb,[(5.5,.5),(.3,-3.8)],t,0,DUR-.6,step=.35); blink(lb,t); face(lb,mouth='frown',brow=.07,brow_r=24,eyes=.7)
        lb['head'].rotation_euler[2]=R(25*math.sin(t*2))
        for k in ('da','sh','bi'): look_at(S['P'][k],hp(lb),tl(t,1.5,2.5)); face(S['P'][k],mouth='O' if t>2.5 else 'flat',brow=.05)
        q=ease(t/DUR); camset(LV((4.0,-2.6,1.2),(3.0,-2.4,1.2),q),(hp(lb)[0],hp(lb)[1],.9),26,8)
    return dict(upd=upd)
SHOTS['BOYCOMES']=BOYCOMES_
def LOST_():
    S,v,lb=lset()
    for i in range(10):
        for s in (-1,1): puff((.3+s*.06,-3.88,1.3),.2+i*.3,.025,1,M('#7FC8F0',.2,emit=.6,alpha=.8),.0,.4,drift=(s*.2,-.3,-1.0),seed=i)
    def upd(t):
        sidle(S,v,t); spos(S); S['P']['sh']['root'].location=(1.0,-5.9,0); lb['root'].location=(.3,-3.8,0); facep(lb,(.55,-5.6)); talk(lb,t,*sg(32),shapes=('o','frown','o','frown'),rest='frown'); face(lb,brow=.08,brow_r=26,eyes=.6)
        lb['head'].rotation_euler[0]=R(-12); arm_to(lb,1,hp(lb,-.15),.7,base=(-30,0,0))
        q=ease(t/DUR); camset(LV((.55,-5.6,1.35),(.53,-5.5,1.33),q),hp(lb,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['LOST']=LOST_
def STOPJOKE_():
    S,v,lb=lset()
    def upd(t):
        sidle(S,v,t); spos(S); S['P']['sh']['root'].location=(1.0,-5.9,0); lb['root'].location=(.3,-3.8,0); facep(lb,(0,-5.2)); face(lb,mouth='frown',eyes=.6)
        for k in ('da','sh','bi'): H=S['P'][k]; facep(H,(.3,-3.8)); face(H,mouth='flat',brow=.04,brow_r=14)
        S['P']['bi']['root'].rotation_euler[0]=R(12*tl(t,.3,.9)); S['P']['da']['root'].rotation_euler[0]=R(10*tl(t,.3,.9))
        q=ease(t/DUR); camset(LV((.0,-1.7,1.9),(.05,-2.0,1.85),q),(.15,-4.6,1.5),20,8)
    return dict(upd=upd)
SHOTS['STOPJOKE']=STOPJOKE_
def SHOULDERS_():
    S,v,lb=lset(); C=[]
    def upd(t):
        sidle(S,v,t); bi=S['P']['bi']; da=S['P']['da']; sh=S['P']['sh']
        k=tl(t,0,.8)
        if t<.8: stand(bi,t); bi['root'].location=(-2.6,-4.0,0)
        else: walk_path(bi,[(-2.6,-4.0),(-2.9,-.3)],t,.8,DUR,step=.5)
        sit(lb,k,0,legs=80); bp=bi['root'].location; kz=min(1,k/.6); kx=max(0,(k-.6)/.4); lb['root'].location=(bp[0],L(-3.1,bp[1],kx),L(0,4.3*bi['u'],kz)); lb['root'].rotation_euler[2]=bi['root'].rotation_euler[2]
        face(lb,mouth='frown',eyes=.8); face(bi,mouth='flat',brow=.03)
        for H in (bi,): H['arm'][1].rotation_euler=(R(-160),0,R(-10)); H['arm'][-1].rotation_euler=(R(-160),0,R(10))
        walk_path(da,[(-.9,-5.2),(1.8,-2.2)],t,.4,DUR,step=.5); walk_path(sh,[(1.0,-5.9),(5.6,-3.6)],t,.6,DUR,step=.5)
        for H,o in ((da,0),(sh,1)): arm_to(H,1,hp(H,.05),1,base=(-30,0,0)) if int(t*1.5+o)%2==0 else None; mouth_talk(H,t,.6,DUR,rate=5,shapes=('O','O')); face(H,brow=.05)
        q=ease(t/DUR); camset(LV((-1.0,1.4,2.4),(.0,2.2,2.5),q),(hp(bi)[0],hp(bi)[1],2.2),26,8)
    return dict(upd=upd)
SHOTS['SHOULDERS']=SHOULDERS_
def mset():
    S=beach(crowd=8,lanes=(-2.45,)); fpos(S); mo=add(S,'mo',MOTHER2,7.5,4.0,180); lb=add(S,'lb',LOST,6.2,3.2,0); return S,mo,lb
def mpos(S,mo,lb):
    for k,(x,y) in (('da',(5.0,2.6)),('sh',(4.1,4.16)),('bi',(6.08,.73))): S['P'][k]['root'].location=(x,y,0); facep(S['P'][k],(7.5,4.0))
def MOTHER_():
    S,mo,lb=mset(); label('AMMI!',(6.2,2.6,1.9),1.4,size=.2,col='#7A1F1F',bg='#FFE0E6')
    def upd(t):
        bidle(S,t); mpos(S,mo,lb); walk_path(mo,[(11,7),(7.0,3.8)],t,0,DUR-.8,step=.55,run_=True); blink(mo,t); face(mo,mouth='O',brow=.08,brow_r=24)
        k=tl(t,1.4,DUR); lb['root'].location=(L(6.1,6.3,k),L(2.2,2.9,k),0); facep(lb,mo['root'].location[:2]); face(lb,mouth='grin' if k>.3 else 'O',brow=.06)
        q=ease(t/DUR); camset(LV((9.9,-.9,1.7),(9.5,-.5,1.7),q),(6.4,3.4,1.25),26,8)
    return dict(upd=upd)
SHOTS['MOTHER']=MOTHER_
def THANKS_():
    S,mo,lb=mset(); hearts(lambda t:(6.9,3.7,2.4),.2,DUR,n=5)
    def upd(t):
        bidle(S,t); mpos(S,mo,lb); mo['root'].location=(7.0,3.8,0); lb['root'].location=(6.3,2.9,0); facep(mo,(5.0,2.6),.6,cam=(6.8,2.0)); talk(mo,t,*sg(36)); face(mo,brow=.06,brow_r=18,eyes=.8)
        arm_to(mo,-1,hp(lb,-.4),1,base=(-30,0,0)); arm_to(lb,1,hp(mo,-1.2),1,base=(-30,0,0)); face(lb,mouth='grin')
        q=ease(t/DUR); camset(LV((6.8,2.0,1.9),(6.82,2.15,1.9),q),hp(mo,-.15),30,4)
    return dict(upd=upd)
SHOTS['THANKS']=THANKS_
def KOIBAAT_():
    S,mo,lb=mset()
    def upd(t):
        bidle(S,t); mpos(S,mo,lb); mo['root'].location=(7.0,3.8,0); lb['root'].location=(6.3,2.9,0); facep(mo,(5.0,2.6)); da=S['P']['da']; facep(da,(7.0,3.8),.6,cam=(6.0,3.9)); talk(da,t,*sg(37,38),rest='smile'); face(da,brow=.02)
        g=math.sin(t*3); da['arm'][1].rotation_euler=(R(-50-15*g),0,R(-20))
        q=ease(t/DUR); camset(LV((6.1,3.95,1.95),(6.05,3.9,1.95),q),hp(da,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['KOIBAAT']=KOIBAAT_
# ================================================================ ENDING
def eset():
    S=beach(crowd=10,lanes=(6.3,)); 
    for k,(x,y) in (('da',(-21.75,-8.55)),('sh',(-19.95,-8.55)),('bi',(-17.7,-8.55))): S['P'][k]['root'].location=(x,y,0)
    return S
def eidle(S,t,talker=None):
    bidle(S,t)
    for k,(x,y) in (('da',(-21.75,-8.55)),('sh',(-19.95,-8.55)),('bi',(-17.7,-8.55))):
        H=S['P'][k]; sit(H,1,1.2,legs=90); H['root'].location=(x,y-.62,H['root'].location[2]); H['root'].rotation_euler[2]=R(180); H['arm'][1].rotation_euler=(R(-6),0,R(4)); H['arm'][-1].rotation_euler=(R(-6),0,R(-4))
        if talker and k!=talker: look_at(H,hp(S['P'][talker]),.6)
def etalk(key,a,b=None,cam=None,rest='smile',extra=None):
    def S_():
        S=eset()
        def upd(t):
            eidle(S,t,key); H=S['P'][key]; c=cam or (H['root'].location[0]+.3,-6.6,1.9); talk(H,t,*sg(a,b),rest=rest); face(H,brow=.03)
            if extra: extra(S,t)
            q=ease(t/DUR); camset(LV(c,(c[0],c[1]-.15,c[2]),q),hp(H,.2),36,2.8)
        return dict(upd=upd)
    return S_
SHOTS['REASONS']=etalk('bi',39)
SHOTS['STORYL']=etalk('da',40)
def NARR_():
    S=eset()
    def upd(t):
        eidle(S,t); q=ease(t/DUR); camset(LV((-19.6,-1.6,2.1),(-19.6,-2.4,2.1),q),(-19.6,-8.6,2.0),22,8)
    return dict(upd=upd)
SHOTS['NARR']=NARR_
def SHOR_():
    S=beach(crowd=22,seed=9); fpos(S); a=add(S,'bf',BOYF,-12.4,8,180); b=add(S,'gf',GIRLF,-11.15,8.5,180); am=add(S,'am',AMMI,9.3,1.7,0); ab=add(S,'ab',ABBU,11.3,1.5,0); kd=add(S,'kd',KID,10.3,.2,0)
    for i_,k in enumerate(('da','sh','bi')): S['P'][k]['root'].location=(40+6*i_,-40,0)
    title_card('THOUSANDS OF LITTLE STORIES',1.0,(-2,4,5.2),.5)
    def upd(t):
        bidle(S,t); sit(ab,1,.05,legs=90); kd['root'].location[2]=.08*abs(math.sin(t*5)); arm_to(a,-1,(b['root'].location[0]-.5,b['root'].location[1]-.3,1.8),.8,base=(-30,0,0))
        q=ease(t/DUR); camset(LV((-20,-7,6),(16,-7,6),q),LV((-12,6,1.2),(10,6,1.2),q),22,22)
    return dict(upd=upd)
SHOTS['SHOR']=SHOR_
def _stand_up(S,t):
    for k in ('da','sh','bi'): pass
SHOTS['GHARQ']=etalk('sh',43,cam=(-19.6,-6.6,1.9))
SHOTS['HAAN']=etalk('da',44,cam=(-21.4,-6.6,1.9),rest='grin')
def PEHLE_():
    S=eset(); cp=in_hand(S['P']['sh'],1,lambda e: tea_cup(e,1.8))
    def upd(t):
        eidle(S,t,'sh'); H=S['P']['sh']; talk(H,t,*sg(45),rest='grin'); face(H,brow=-.02,brow_r=-10,eyes=.7); arm_to(H,1,hp(H,-.35),tl(t,.1,.5),base=(-30,0,0))
        q=ease(t/DUR); camset(LV((-19.65,-6.6,1.9),(-19.67,-6.75,1.9),q),hp(H,.18),34,2.8)
    return dict(upd=upd)
SHOTS['PEHLE']=PEHLE_
def BRO_():
    S=eset(); cp=in_hand(S['P']['sh'],1,lambda e: tea_cup(e,1.8)); title_card('BRO, TUMHARI CHAI KHATAM HI NAHI HOTI!',1.2,(-18.5,-8.2,3.3),.13)
    def upd(t):
        eidle(S,t,'bi'); H=S['P']['bi']; talk(H,t,*sg(46),shapes=('O','O','o','O'),rest='O'); face(H,brow=.08,brow_r=24); k=tl(t,0,.3)
        H['arm'][1].rotation_euler=(R(-25),0,R(-25)); H['arm'][-1].rotation_euler=(R(-25-40*k),0,R(25+120*k)); sh=S['P']['sh']; arm_to(sh,1,hp(sh,-.35),1,base=(-30,0,0)); face(sh,mouth='grin',eyes=.6)
        q=ease(t/DUR); camset(LV((-18.8,-3.9,2.0),(-18.8,-4.3,2.0),q),(-18.8,-8.9,2.15),20,8)
    return dict(upd=upd)
SHOTS['BRO']=BRO_
W_=json.load(open(LH+'/audio/words.json'))
