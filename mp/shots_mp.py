# Shots for "The Multani Prince". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=105.2
SEQ=[('OPEN', 0.0), ('KINGDOM', 3.47), ('MEET', 5.22), ('TRAVEL', 6.11), ('STEPS', 9.54), ('HOT', 14.31), ('NOTIMP', 15.8), ('GARMI', 17.71), ('MOMENT', 20.53), ('OYE', 22.77), ('PYAR', 24.9), ('BAG', 26.45), ('FULL', 27.71), ('TWELVE', 30.09), ('BITE', 31.35), ('EYES', 32.71), ('VIOLIN', 34.04), ('KAMAAL', 36.3), ('ADJUST', 38.4), ('QUALITY', 40.44), ('SNEAK1', 43.81), ('MALL', 46.07), ('GIFTWANT', 47.85), ('WATCH', 50.79), ('PRICE', 51.92), ('LAUGHS', 54.57), ('GIFT', 56.0), ('SNEAK2', 59.71), ('TOURIST', 61.89), ('MISTAKE', 65.97), ('SHRINES', 67.31), ('TILES', 69.24), ('MANGOES', 70.34), ('HEAT', 71.27), ('SAINTS', 72.06), ('CROWD', 73.36), ('NOTES', 75.68), ('GUIDE', 77.23), ('AMBASSADOR', 79.3), ('CLAPS', 82.33), ('ASKHALWA', 83.68), ('OPENS', 86.56), ('EMPTY', 88.85), ('TURNS', 92.09), ('FACE', 94.1), ('SAARA', 95.94), ('BHAI', 97.98), ('STARES', 100.24), ('IZZAT', 102.19)]
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
def mul_set(mood='golden'):
    multan_set(); B.done('multan'); setup_world(mood,shadow=80)
def tm_set(crowd=8,seed=3):
    bs=terminal_set(); B.done('terminal'); setup_world('afternoon',shadow=45)
    Sh=mk(SHAHZAIB,0,-1.6,0,'shah'); Ha=mk(HAMZA,1.4,.2,200,'hamza'); W=walkers(crowd,seed,-20,20,(1.5,3.0,6.0)); return bs,Sh,Ha,W
def tidle(Sh,Ha,W,t,skip=()):
    upd_walkers(W,t+5)
    for k,H in (('sh',Sh),('ha',Ha)):
        if k not in skip: stand(H,t); blink(H,t)
def ml_set(crowd=10,seed=4,tourist=False):
    mall_set(); B.done('mall'); setup_interior('day',room=(0,0,13),res=PCT,samples=SAMPLES,shadow_dist=25); point((0,0,11),1500,(1,.97,.92),5.0,False); point((6,4,3.5),200,(1,.95,.85),1.5,False)
    Sh=mk(SHAHZAIB,6.6,3.0,90,'shah'); Ha=mk(HAMZA,8.8,4.0,90,'hamza'); W=walkers(crowd,seed,-10,10,(-7,-1,10)); Tr=mk(TOURIST,4.6,2.0,-60,'tourist') if tourist else None
    return Sh,Ha,W,Tr
def bag_on(H,s=1): return in_hand(H,s,lambda e: duffel(e,1.3))
def crumbs(H):
    u=H['u']; m=M('#8A4A1E',.6)
    for (x,z) in ((-.25,-.35),(.2,-.42),(.05,-.3),(.32,-.2)): oico((x*u*1.5,-.72*u,z*u*1.5),.035,m,H['head'],sub=1)
# ================================================================ HOOK — Multan
def OPEN_():
    mul_set(); sparkles((0,20,23),2,.3,DUR,n=30,size=.08)
    def upd(t):
        q=ease(t/DUR); camset(LV((-14,-26,3),(-9,-22,6),q),(0,20,12),24,22)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def KINGDOM_():
    mul_set(); Sh=mk(SHAHZAIB,0,8.5,0,'shah',z=3.6); title_card('MULTAN: ROYAL KINGDOM',.2,(0,8.5,7.2),.4); sparkles((0,8.5,5.5),1.2,.2,DUR,n=26,size=.05)
    def upd(t):
        stand(Sh,t); blink(Sh,t); Sh['root'].location[2]=3.6; face(Sh,mouth='smile',brow=.04); k=tl(t,0,.5); Sh['arm'][1].rotation_euler=(R(-20*k),0,R(-110*k)); Sh['arm'][-1].rotation_euler=(R(-20*k),0,R(110*k))
        q=ease(t/DUR); camset(LV((0,1.5,4.6),(0,2.2,4.8),q),(0,8.5,6.2),26,16)
    return dict(upd=upd)
SHOTS['KINGDOM']=KINGDOM_
# ================================================================ SCENE 1 — terminal
def MEET_():
    bs,Sh,Ha,W=tm_set(); Ha['root'].location=(30,30,0); label('SHAHZAIB',(0,-1.6,2.75),.1,col='#1E3A6A',bg='#DFEBFF')
    def upd(t):
        tidle(Sh,Ha,W,t); face(Sh,mouth='smile',brow=.03); Sh['arm'][1].rotation_euler=(R(-20),0,R(-30)); Sh['arm'][-1].rotation_euler=(R(-20),0,R(30))
        q=ease(t/DUR); camset(LV((.3,-3.4,1.8),(.25,-3.1,1.8),q),hp(Sh,-.15),36,4)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def TRAVEL_():
    bs,Sh,Ha,W=tm_set(); Sh['root'].location=(30,30,0); Ha['root'].location=(30,31,0); title_card('MULTAN  >  LAHORE',.3,(-2,-6.5,5.2),.4)
    def upd(t):
        tidle(Sh,Ha,W,t); k=ease_out(tl(t,0,DUR-.6)); bs.location=(L(-30,-6,k),-6.5,0)
        q=ease(t/DUR); camset(LV((8,-14,2.2),(6,-13,2.0),q),(bs.location[0]+2,-6.5,2.0),24,16)
    return dict(upd=upd)
SHOTS['TRAVEL']=TRAVEL_
def STEPS_():
    bs,Sh,Ha,W=tm_set(); bg=bag_on(Sh,1); Ha['root'].location=(30,30,0)
    def upd(t):
        tidle(Sh,Ha,W,t,skip=('sh',)); walk_path(Sh,[(-1.2,-5.0),(-.6,-3.2),(0,-1.6)],t*.75,0,DUR*.75,step=.5); blink(Sh,t); face(Sh,mouth='smile',brow=.03)
        Sh['arm'][1].rotation_euler=(R(-15),0,R(-15)); Sh['scarf'] if False else None
        q=ease(t/DUR); camset(LV((1.2,1.6,.6),(1.0,1.2,.7),q),hp(Sh,-.5),24,8)
    return dict(upd=upd)
SHOTS['STEPS']=STEPS_
def HOT_():
    bs,Sh,Ha,W=tm_set(crowd=10); bg=bag_on(Sh,1); cc=clock_card((.4,4.0,3.6),.2,'45°C',spin=0,col='#C8372D')
    sun=empty((0,0,0))
    def upd(t):
        tidle(Sh,Ha,W,t); g=math.sin(t*12); Ha['arm'][1].rotation_euler=(R(-130),0,R(-40+25*g)); face(Ha,mouth='O',brow=.06,brow_r=18,eyes=.6); Ha['head'].rotation_euler[0]=R(-10)
        for p in W: p['H']['arm'][1].rotation_euler=(R(-130),0,R(-40+25*math.sin(t*12+p['y'])))
        q=ease(t/DUR); camset(LV((3.6,-2.6,1.9),(3.3,-2.4,1.9),q),(1.0,.6,1.6),26,8)
    return dict(upd=upd)
SHOTS['HOT']=HOT_
def NOTIMP_():
    bs,Sh,Ha,W=tm_set(); bg=bag_on(Sh,1)
    def upd(t):
        tidle(Sh,Ha,W,t); face(Sh,mouth='flat',brow=-.03,brow_r=-8); Sh['head'].rotation_euler=(R(-6),0,R(15*math.sin(t*1.2)))
        q=ease(t/DUR); camset(LV((.25,-3.0,1.95),(.22,-2.8,1.95),q),hp(Sh,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['NOTIMP']=NOTIMP_
def GARMI_():
    bs,Sh,Ha,W=tm_set(); bg=bag_on(Sh,1)
    def upd(t):
        tidle(Sh,Ha,W,t); talk(Sh,t,*ln(47,55),rest='smile'); face(Sh,brow=.03); g=math.sin(t*3); Sh['arm'][-1].rotation_euler=(R(-60-15*g),0,R(25)); Sh['head'].rotation_euler[2]=R(-8)
        q=ease(t/DUR); camset(LV((-.35,-2.95,1.95),(-.3,-2.75,1.95),q),hp(Sh,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['GARMI']=GARMI_
def MOMENT_():
    bs,Sh,Ha,W=tm_set(); bg=bag_on(Sh,1)
    def upd(t):
        tidle(Sh,Ha,W,t,skip=('ha',)); walk_path(Ha,[(5.5,2.5),(1.4,.2)],t,0,DUR-.4,step=.6,run_=True); blink(Ha,t); face(Ha,mouth='grin',brow=.06)
        facep(Sh,(1.4,.2),tl(t,1.2,1.8))
        q=ease(t/DUR); camset(LV((4.6,-3.4,1.8),(4.3,-3.1,1.8),q),(1.0,-.4,1.5),26,8)
    return dict(upd=upd)
SHOTS['MOMENT']=MOMENT_
def two(Sh,Ha):
    Sh['root'].location=(0,-1.6,0); Ha['root'].location=(1.2,-.4,0); facep(Sh,(1.2,-.4)); facep(Ha,(0,-1.6))
def OYE_():
    bs,Sh,Ha,W=tm_set(); bg=bag_on(Sh,1)
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); talk(Ha,t,*ln(62,68)); face(Ha,brow=.06,brow_r=10); gest(Ha,t,1,1.2,8,-80); arm_to(Ha,-1,(.2,-1.6,1.2),tl(t,.6,1.0),base=(-30,0,0))
        q=ease(t/DUR); camset(LV((-.35,-1.25,2.0),(-.3,-1.1,2.0),q),hp(Ha,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['OYE']=OYE_
def PYAR_():
    bs,Sh,Ha,W=tm_set(); bg=bag_on(Sh,1)
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); facep(Sh,(1.2,-.4),.7,cam=(.9,-3.2)); talk(Sh,t,*ln(69,74),rest='smile'); face(Sh,brow=.03); headtouch(Sh,-1,tl(t,.1,.4),dx=.1,dy=-1.2,dz=-1.3)
        q=ease(t/DUR); camset(LV((.9,-3.3,1.95),(.88,-3.1,1.95),q),hp(Sh,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['PYAR']=PYAR_
def bench_scene(open_k):
    bs,Sh,Ha,W=tm_set(crowd=6); bag=empty((.6,-1.0,.0)); lid=duffel(bag,1.4); return bs,Sh,Ha,W,bag,lid
def BAG_():
    bs,Sh,Ha,W,bag,lid=bench_scene(0)
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); k=tl(t,.3,1.0); lid.rotation_euler[0]=R(-110*k); arm_to(Sh,1,(.6,-1.2,.8),tl(t,0,.3),base=(-30,0,0)); Sh['root'].rotation_euler[0]=R(10)
        face(Sh,mouth='smile'); face(Ha,mouth='O',brow=.06); look_at(Ha,(.6,-1.0,.5),.8)
        q=ease(t/DUR); camset(LV((2.4,-2.7,2.4),(2.2,-2.5,2.3),q),(.5,-.9,.6),28,5.6)
    return dict(upd=upd)
SHOTS['BAG']=BAG_
def boxes_rise(t0,n=12,c=(.6,-1.0,.6)):
    bx=[]
    for k in range(n):
        e=empty((0,0,-50)); halwa_box(e,1.4); bx.append((e,t0+.12*k,k))
    def place(t):
        for e,ts,k in bx:
            q=tl(t,ts,ts+.5)
            if t<ts: e.location=(0,0,-50); continue
            col=k%4; row=k//4; e.location=(c[0]-.95+col*.63,c[1]-.0,c[2]+L(0,.3+row*.26,q)); e.scale=(1,1,1)
    return place
def FULL_():
    bs,Sh,Ha,W,bag,lid=bench_scene(1); lid.rotation_euler[0]=R(-110); pl=boxes_rise(.2); label('MULTANI SOHAN HALWA',(.6,-1.0,2.0),.8,size=.2,col='#7A1F1F')
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); pl(t); face(Sh,mouth='grin'); face(Ha,mouth='O',brow=.07,brow_r=16); look_at(Ha,(.6,-1.0,1.0),.8)
        q=ease(t/DUR); camset(LV((2.5,-2.9,1.7),(2.3,-2.7,1.65),q),(.5,-1.0,1.2),30,5.6)
    return dict(upd=upd)
SHOTS['FULL']=FULL_
def TWELVE_():
    bs,Sh,Ha,W,bag,lid=bench_scene(1); lid.rotation_euler[0]=R(-110); pl=boxes_rise(-5); cc=label('x 12',(.6,-1.0,2.1),.2,size=.4,col='#7A1F1F')
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); pl(t); face(Sh,mouth='grin')
        q=ease(t/DUR); camset(LV((1.6,-3.0,2.2),(1.4,-2.8,2.1),q),(.6,-1.0,1.3),28,5.6)
    return dict(upd=upd)
SHOTS['TWELVE']=TWELVE_
def BITE_():
    bs,Sh,Ha,W=tm_set(); pc=in_hand(Ha,1,lambda e: halwa_piece(e,1.6))
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); k=tl(t,.2,.8); arm_to(Ha,1,hp(Ha,-.25),k,base=(-30,0,0)); face(Ha,mouth='O' if k<.9 else 'flat',brow=.05)
        q=ease(t/DUR); camset(LV((.35,-1.3,1.9),(.38,-1.15,1.9),q),hp(Ha,-.1),36,2.8)
    return dict(upd=upd)
SHOTS['BITE']=BITE_
def EYES_():
    bs,Sh,Ha,W=tm_set(); sparkles(hp(Ha,0),.5,.3,DUR,n=18,size=.025)
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); blink(Ha,t,force=True); face(Ha,mouth='smile',brow=.06,brow_r=14,eyes=0); Ha['head'].rotation_euler=(R(-14),0,R(6*math.sin(t*1.4)))
        Ha['arm'][1].rotation_euler=(R(-50),0,R(-60)); Ha['arm'][-1].rotation_euler=(R(-50),0,R(60))
        q=ease(t/DUR); camset(LV((.25,-1.2,1.85),(.3,-1.05,1.87),q),hp(Ha,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['EYES']=EYES_
def VIOLIN_():
    bs,Sh,Ha,W=tm_set(); Vi=mk(VIOLINIST,2.6,.9,200,'vio'); vn=in_hand(Vi,-1,lambda e: violin(e,1.5)); label('*VIOLIN*',(2.6,.9,2.7),.4,size=.2,col='#6A2A6A',bg='#F3E6FF')
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); stand(Vi,t); blink(Vi,t); facep(Vi,(4.0,-1.4)); face(Vi,mouth='flat',eyes=0,brow=.04); blink(Vi,t,force=True)
        Vi['arm'][-1].rotation_euler=(R(-100),0,R(40)); Vi['arm'][1].rotation_euler=(R(-80),0,R(-30+25*math.sin(t*5))); Vi['head'].rotation_euler[2]=R(-15)
        face(Ha,mouth='smile',eyes=0,brow=.06,brow_r=14); blink(Ha,t,force=True)
        q=ease(t/DUR); camset(LV((4.2,-1.6,1.9),(4.0,-1.4,1.9),q),(1.9,.5,1.7),28,8)
    return dict(upd=upd)
SHOTS['VIOLIN']=VIOLIN_
def KAMAAL_():
    bs,Sh,Ha,W=tm_set()
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); talk(Ha,t,*ln(99,103),shapes=('O','o','O','grin')); face(Ha,brow=.07,brow_r=18); k=tl(t,0,.3); Ha['arm'][1].rotation_euler=(R(-30*k),0,R(-120*k)); Ha['arm'][-1].rotation_euler=(R(-30*k),0,R(120*k))
        q=ease(t/DUR); camset(LV((-.35,-1.25,2.0),(-.3,-1.1,2.0),q),hp(Ha,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['KAMAAL']=KAMAAL_
def ADJUST_():
    bs,Sh,Ha,W=tm_set()
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); facep(Sh,(1.2,-.4),.85,cam=(.4,-3.0)); headtouch(Sh,1,tl(t,.2,.5)*(1-tl(t,1.4,1.8)),dx=.45,dy=-.75,dz=.25); face(Sh,mouth='smile',brow=.03)
        q=ease(t/DUR); camset(LV((.4,-2.8,1.95),(.38,-2.65,1.95),q),hp(Sh,-.03),44,2.8)
    return dict(upd=upd)
SHOTS['ADJUST']=ADJUST_
def QUALITY_():
    bs,Sh,Ha,W=tm_set()
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); facep(Sh,(1.2,-.4),.5,cam=(.4,-3.0)); talk(Sh,t,*ln(108,116),rest='smile'); face(Sh,brow=.02); gest(Sh,t,1,1.0,5,-70); Sh['arm'][-1].rotation_euler=(R(-25),0,R(30))
        q=ease(t/DUR); camset(LV((.6,-3.1,1.9),(.55,-2.9,1.9),q),hp(Sh,-.08),36,2.8)
    return dict(upd=upd)
SHOTS['QUALITY']=QUALITY_
def SNEAK1_():
    bs,Sh,Ha,W,bag,lid=bench_scene(1); lid.rotation_euler[0]=R(-110); pc=in_hand(Ha,1,lambda e: halwa_piece(e,1.6))
    def upd(t):
        tidle(Sh,Ha,W,t); two(Sh,Ha); facep(Sh,(-1,-4)); face(Sh,mouth='smile',brow=.03); Ha['root'].location=(1.0,-.7,0); k=math.sin(pi*tl(t,.2,1.4))
        facep(Ha,(2.2,-1.6),.6,cam=(2.2,-1.6)); arm_to(Ha,1,(.6,-1.0,.7),k,base=(-30,0,0)); Ha['head'].rotation_euler[2]=R(-30); face(Ha,mouth='flat',brow=.03,eyes=.5); look_at(Ha,hp(Sh),.5)
        if t>1.4: arm_to(Ha,1,hp(Ha,-.25),tl(t,1.4,1.9),base=(-30,0,0))
        q=ease(t/DUR); camset(LV((2.5,-1.9,2.4),(2.4,-1.8,2.35),q),(.9,-.8,1.3),28,5.6)
    return dict(upd=upd)
SHOTS['SNEAK1']=SNEAK1_
# ================================================================ SCENE 2 — mall
def MALL_():
    Sh,Ha,W,Tr=ml_set(crowd=16)
    def upd(t):
        upd_walkers(W,t+2); walk_path(Sh,[(0,-8),(1.5,-3)],t,0,DUR,step=.5); walk_path(Ha,[(1,-8.5),(2.5,-3.5)],t,0,DUR,step=.5); blink(Sh,t); blink(Ha,t)
        q=ease(t/DUR); camset(LV((-3,-15,8),(-2,-14,6),q),(1,-2,2.5),20,22)
    return dict(upd=upd)
SHOTS['MALL']=MALL_
def mall2(tourist=False,crowd=8):
    Sh,Ha,W,Tr=ml_set(crowd=crowd,tourist=tourist); Cl=mk(CLERK,11.0,4.0,90,'clerk'); return Sh,Ha,W,Tr,Cl
def midle(Sh,Ha,W,Cl,t):
    upd_walkers(W,t+5)
    for H in (Sh,Ha,Cl): stand(H,t); blink(H,t)
    Cl['root'].rotation_euler[2]=R(-90)
def GIFTWANT_():
    Sh,Ha,W,Tr,Cl=mall2(); b=bubble('GIFT FOR MY FIANCEE',(8.8,4.0,2.7),.4,size=.17,col='#6A2A6A',bg='#FFE0F0')
    def upd(t):
        midle(Sh,Ha,W,Cl,t); Ha['root'].location=(8.8,4.0,0); facep(Ha,(9.8,4.0)); arm_to(Ha,1,(9.8,4.0,1.1),tl(t,.3,.7),base=(-30,0,0)); face(Ha,mouth='grin',brow=.05)
        Sh['root'].rotation_euler[2]=R(-60); face(Sh,mouth='flat',brow=-.02)
        q=ease(t/DUR); camset(LV((7.0,1.0,2.2),(7.2,1.3,2.1),q),(9.2,4.0,1.5),26,8)
    return dict(upd=upd)
SHOTS['GIFTWANT']=GIFTWANT_
def WATCH_():
    Sh,Ha,W,Tr,Cl=mall2(); wt=in_hand(Ha,1,lambda e: wristwatch(e,1.6))
    def upd(t):
        midle(Sh,Ha,W,Cl,t); Ha['root'].location=(8.8,4.0,0); facep(Ha,(8.0,3.0)); arm_to(Ha,1,hp(Ha,-.4),tl(t,.1,.6),base=(-30,0,0)); Ha['head'].rotation_euler[0]=R(15); face(Ha,mouth='smile',brow=.05)
        q=ease(t/DUR); camset(LV((8.0,3.0,1.95),(8.1,3.15,1.95),q),hp(Ha,-.3),34,2.8)
    return dict(upd=upd)
SHOTS['WATCH']=WATCH_
def PRICE_():
    Sh,Ha,W,Tr,Cl=mall2(); wt=in_hand(Ha,1,lambda e: wristwatch(e,1.6)); cc=label('Rs. 80,000',(8.8,4.0,2.75),.3,size=.3,col='#C8372D',bg='#FFF3B0')
    def upd(t):
        midle(Sh,Ha,W,Cl,t); Ha['root'].location=(8.8,4.0,0); facep(Ha,(7.7,2.7)); arm_to(Ha,1,hp(Ha,-.4),1,base=(-30,0,0)); face(Ha,mouth='O',brow=.08,brow_r=22,eyes=1.2); Ha['root'].location[2]=.12*pop(t-.4)*(t<1.0)
        q=ease(t/DUR); camset(LV((7.7,2.7,1.95),(7.85,2.95,1.95),q),hp(Ha,-.1),36,2.8)
    return dict(upd=upd)
SHOTS['PRICE']=PRICE_
def LAUGHS_():
    Sh,Ha,W,Tr,Cl=mall2()
    def upd(t):
        midle(Sh,Ha,W,Cl,t); facep(Sh,(8.8,4.0),.85,cam=(5.2,1.8)); laugh(Sh,t,1.0); Sh['arm'][1].rotation_euler=(R(-40),0,R(-30)); headtouch(Sh,-1,.6,dx=.3,dy=-1.3,dz=-1.9)
        q=ease(t/DUR); camset(LV((5.2,1.8,1.95),(5.35,2.0,1.95),q),hp(Sh,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['LAUGHS']=LAUGHS_
def GIFT_():
    Sh,Ha,W,Tr,Cl=mall2()
    def upd(t):
        midle(Sh,Ha,W,Cl,t); facep(Sh,(8.8,4.0),.8,cam=(5.3,1.9)); talk(Sh,t,*ln(152,163),rest='grin'); laugh(Sh,t,.4); gest(Sh,t,1,1.2,6,-75); Sh['arm'][-1].rotation_euler=(R(-30),0,R(30))
        q=ease(t/DUR); camset(LV((5.3,1.9,1.95),(5.4,2.05,1.95),q),hp(Sh,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['GIFT']=GIFT_
def SNEAK2_():
    Sh,Ha,W,Tr,Cl=mall2(); bx=in_hand(Ha,-1,lambda e: halwa_box(e,1.5,True)); pc=in_hand(Ha,1,lambda e: halwa_piece(e,1.6))
    def upd(t):
        midle(Sh,Ha,W,Cl,t); Ha['root'].location=(8.4,2.4,0); facep(Ha,(6,0)); Ha['arm'][-1].rotation_euler=(R(-60),0,R(10)); k=math.sin(pi*tl(t,.2,1.6)); arm_to(Ha,1,hp(Ha,-.25),k,base=(-30,0,0))
        face(Ha,mouth='O' if k>.8 else 'flat',eyes=.5,brow=.03); look_at(Ha,hp(Sh),.4); facep(Sh,(4,6)); face(Sh,mouth='smile')
        q=ease(t/DUR); camset(LV((7.2,.8,1.9),(7.3,1.0,1.9),q),hp(Ha,-.2),32,4)
    return dict(upd=upd)
SHOTS['SNEAK2']=SNEAK2_
# ================================================================ SCENE 3 — tourist
def TOURIST_():
    Sh,Ha,W,Tr,Cl=mall2(tourist=True); label('FOREIGN TOURIST',(4.6,2.0,2.95),.6,size=.18,col='#1F4D3A',bg='#DFF5E1')
    def upd(t):
        midle(Sh,Ha,W,Cl,t); walk_path(Tr,[(2.0,-1.5),(5.4,2.5)],t,0,2.2,step=.55); blink(Tr,t)
        if t>2.2: facep(Tr,(6.6,3.0)); mouth_talk(Tr,t,2.4,4.2); face(Tr,brow=.05,brow_r=10); gest(Tr,t,1,1.0,6,-70)
        facep(Sh,(5.4,2.5),tl(t,1.8,2.4)); face(Sh,mouth='smile')
        q=ease(t/DUR); camset(LV((5.6,-1.6,2.0),(5.8,-1.2,2.0),q),(6.0,2.8,1.7),28,8)
    return dict(upd=upd)
SHOTS['TOURIST']=TOURIST_
def tset():
    Sh,Ha,W,Tr,Cl=mall2(tourist=True); Tr['root'].location=(5.4,2.5,0); return Sh,Ha,W,Tr,Cl
def tidl(Sh,Ha,W,Tr,Cl,t):
    midle(Sh,Ha,W,Cl,t); stand(Tr,t); blink(Tr,t); Tr['root'].location=(5.4,2.5,0); facep(Tr,(6.6,3.0)); facep(Sh,(5.4,2.5))
def MISTAKE_():
    Sh,Ha,W,Tr,Cl=tset(); title_card('THAT WAS A MISTAKE.',.3,(6.6,3.0,2.9),.18)
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); facep(Sh,(5.4,2.5),.5,cam=(5.6,0)); k=tl(t,.2,.9); shk(Sh,1-k); face(Sh,mouth='grin',brow=.05,eyes=.8); Sh['arm'][1].rotation_euler=(R(-60*k),0,R(-30))
        q=ease(t/DUR); camset(LV((6.0,.6,1.95),(6.1,.95,1.97),q),hp(Sh,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['MISTAKE']=MISTAKE_
def SHRINES_():
    mul_set('morning'); label('THE SHRINES',(0,8,9),.3,size=.6,col='#1E3A6A',bg='#DFEBFF')
    def upd(t):
        q=ease(t/DUR); camset(LV((-17,-13,7.0),(-14,-11,8.0),q),(0,20,11),24,22)
    return dict(upd=upd)
SHOTS['SHRINES']=SHRINES_
def TILES_():
    mul_set('morning'); label('THE BLUE TILES',(4.6,15.2,8.9),.2,size=.35,col='#1E3A6A',bg='#DFEBFF')
    def upd(t):
        q=ease(t/DUR); camset(LV((7.3,12.7,7.4),(6.95,13.05,7.4),q),(4.12,15.88,7.6),26,8)
    return dict(upd=upd)
SHOTS['TILES']=TILES_
def MANGOES_():
    mul_set('morning'); e=empty((-6,-5.6,0)); mango_crate(e,1.4); label('THE MANGOES',(-6,-5.6,1.7),.15,size=.3,col='#7A3A10')
    def upd(t):
        q=ease(t/DUR); camset(LV((-4.6,-8.2,1.6),(-4.9,-7.8,1.6),q),(-6,-5.4,1.0),30,5.6)
    return dict(upd=upd)
SHOTS['MANGOES']=MANGOES_
def HEAT_():
    mul_set('afternoon'); cc=clock_card((0,4,6.5),.1,'50°C',spin=0,col='#C8372D')
    sun=empty((0,40,22)); oico((0,0,0),3.0,M('#FFE08A',.3,emit=6),sun,sub=2)
    def upd(t):
        s=1+.06*math.sin(t*6); sun.scale=(s,s,s); q=ease(t/DUR); camset(LV((0,-4,2.2),(0,-3.4,2.6),q),(0,20,12),24,22)
    return dict(upd=upd)
SHOTS['HEAT']=HEAT_
def SAINTS_():
    mul_set('golden'); title_card('THE CITY OF SAINTS',.2,(0,12,24),1.0); sparkles((0,20,20),6,.2,DUR,n=40,size=.1)
    def upd(t):
        q=ease(t/DUR); camset(LV((-20,-20,16),(-16,-16,14),q),(0,20,14),24,22)
    return dict(upd=upd)
SHOTS['SAINTS']=SAINTS_
def crowd_ring(n=9,seed=6):
    r=random.Random(seed); C=[]
    for i in range(n):
        a=R(-20+i*24); d=r.uniform(2.0,2.8); x=6.0+math.cos(a)*d*-1; y=2.8+math.sin(a)*d*-1
        H=mk(person(seed*30+i),x,y,0,'cr%d'%i); C.append(H)
    return C
def cidle(C,t,sh_pos=(6.6,3.0)):
    for H in C: stand(H,t); blink(H,t); facep(H,sh_pos); face(H,mouth='O',brow=.05)
def CROWD_():
    Sh,Ha,W,Tr,Cl=tset(); C=crowd_ring(); cc=clock_card((6.6,3.0,3.3),.2,'+20 MIN',spin=4)
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); cidle(C,t); facep(Sh,(4,2),.5,cam=(2,-2)); mouth_talk(Sh,t,0,DUR,rate=9,rest='grin'); gest(Sh,t,1,1.3,7,-90); gest(Sh,t+1,-1,1.3,7,-90)
        q=ease(t/DUR); camset(LV((2.0,-2.0,6.0),(2.4,-1.6,5.4),q),(6.4,2.8,1.3),24,8)
    return dict(upd=upd)
SHOTS['CROWD']=CROWD_
def NOTES_():
    Sh,Ha,W,Tr,Cl=tset(); C=crowd_ring(); N=C[3]; np_=in_hand(N,1,lambda e: notepad(e,1.6)); label('*TAKING NOTES*',(0,0,0),99)
    lb=label('TAKING NOTES',(N['root'].location[0],N['root'].location[1],2.6),.3,size=.17)
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); cidle(C,t); hold_phone(N,1,1); N['head'].rotation_euler[0]=R(20); g=math.sin(t*16); N['arm'][-1].rotation_euler=(R(-70+5*g),0,R(25)); face(N,mouth='flat',brow=.03)
        p=N['root'].location; q=ease(t/DUR); camset(LV((6.6,3.0,3.0),(6.55,3.0,2.95),q),hp(N,-.4),30,4)
    return dict(upd=upd)
SHOTS['NOTES']=NOTES_
def GUIDE_():
    Sh,Ha,W,Tr,Cl=tset(); C=crowd_ring()
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); cidle(C,t); talk(Tr,t,*ln(209,215)); face(Tr,brow=.05,brow_r=10); gest(Tr,t,1,1.0,6,-75)
        q=ease(t/DUR); camset(LV((6.35,2.95,2.05),(6.3,2.9,2.05),q),hp(Tr,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['GUIDE']=GUIDE_
def AMBASSADOR_():
    Sh,Ha,W,Tr,Cl=tset(); C=crowd_ring(); sparkles((6.6,3.0,2.2),1.0,.6,DUR,n=30,size=.04); title_card('MULTAN DA AMBASSADOR',1.5,(6.6,3.0,3.0),.18)
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); cidle(C,t); facep(Sh,(5.4,2.5),.6,cam=(7.6,1.6)); talk(Sh,t,*ln(216,222),rest='grin'); face(Sh,brow=.04); k=tl(t,1.2,1.7); Sh['arm'][1].rotation_euler=(R(-20*k),0,R(-115*k)); Sh['arm'][-1].rotation_euler=(R(-20*k),0,R(115*k))
        q=ease(t/DUR); camset(LV((7.7,1.4,1.9),(7.6,1.6,1.9),q),hp(Sh,-.2),32,4)
    return dict(upd=upd)
SHOTS['AMBASSADOR']=AMBASSADOR_
def CLAPS_():
    Sh,Ha,W,Tr,Cl=tset(); C=crowd_ring()
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); cidle(C,t)
        for i,H in enumerate(C+[Tr]): g=abs(math.sin(t*10+i)); H['arm'][1].rotation_euler=(R(-80),0,R(-20+18*g)); H['arm'][-1].rotation_euler=(R(-80),0,R(20-18*g)); face(H,mouth='grin',brow=.04)
        face(Sh,mouth='grin'); Sh['arm'][1].rotation_euler=(R(-150),0,R(-20))
        q=ease(t/DUR); camset(LV((2.4,-1.6,3.0),(2.8,-1.2,2.8),q),(6.4,2.8,1.4),24,8)
    return dict(upd=upd)
SHOTS['CLAPS']=CLAPS_
# ================================================================ FINAL
def ASKHALWA_():
    Sh,Ha,W,Tr,Cl=tset(); b=bubble('CAN I TAKE SOME HALWA HOME?',(5.4,2.5,2.9),.3,size=.16,col='#1F4D3A',bg='#DFF5E1')
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); mouth_talk(Tr,t,.2,2.6); face(Tr,brow=.05,brow_r=12); Tr['arm'][1].rotation_euler=(R(-60),0,R(-30)); Tr['arm'][-1].rotation_euler=(R(-60),0,R(30))
        q=ease(t/DUR); camset(LV((6.35,2.95,2.05),(6.3,2.9,2.05),q),hp(Tr,-.1),36,2.8)
    return dict(upd=upd)
SHOTS['ASKHALWA']=ASKHALWA_
def mbag():
    e=empty((6.9,2.2,0)); lid=duffel(e,1.4); return e,lid
def OPENS_():
    Sh,Ha,W,Tr,Cl=tset(); e,lid=mbag()
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); facep(Sh,(6.9,2.2)); Sh['root'].rotation_euler[0]=R(10); arm_to(Sh,1,(6.9,2.1,.8),tl(t,.2,.6),base=(-30,0,0)); lid.rotation_euler[0]=R(110*tl(t,.8,1.6)); face(Sh,mouth='grin',brow=.04)
        q=ease(t/DUR); camset(LV((7.9,.9,2.5),(7.8,1.1,2.45),q),(6.7,2.5,.9),28,5.6)
    return dict(upd=upd)
SHOTS['OPENS']=OPENS_
def EMPTY_():
    Sh,Ha,W,Tr,Cl=tset(); e,lid=mbag(); lid.rotation_euler[0]=R(110); l1=label('EMPTY.',(6.9,1.9,1.0),.1,size=.3,col='#C8372D'); l2=label('12 BOXES = 0 HALWA',(6.9,1.9,.75),1.3,size=.15)
    for k in range(4):
        b=empty((6.6+.2*k,1.9,.05),rot=(0,0,R(20*k))); halwa_box(b,1.0,True)
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t)
        q=ease(t/DUR); camset(LV((7.0,1.0,2.4),(7.0,1.15,2.3),q),(6.9,1.95,.3),30,4)
    return dict(upd=upd)
SHOTS['EMPTY']=EMPTY_
def TURNS_():
    Sh,Ha,W,Tr,Cl=tset(); Ha['root'].location=(8.0,4.2,0)
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); Ha['root'].location=(8.0,4.2,0); a0=face_dir(5.4-6.6,2.5-3.0); a1=face_dir(8.0-6.6,4.2-3.0); Sh['root'].rotation_euler[2]=R(lerp_angle(a0,a1,ease(tl(t,.2,1.8))))
        face(Sh,mouth='flat',brow=-.05,brow_r=-18,eyes=.7); Sh['head'].rotation_euler[2]=0
        q=ease(t/DUR); camset(LV((5.6,1.0,1.95),(5.7,1.3,1.95),q),hp(Sh,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['TURNS']=TURNS_
def FACE_():
    Sh,Ha,W,Tr,Cl=tset(); Ha['root'].location=(8.0,4.2,0); crumbs(Ha); bx=in_hand(Ha,-1,lambda e: halwa_box(e,1.5,True)); label('HALWA ON FACE',(8.0,4.2,2.6),.4,size=.17)
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); Ha['root'].location=(8.0,4.2,0); facep(Ha,(6.6,3.0),.5,cam=(7.0,2.2)); face(Ha,mouth='grin',brow=.04,eyes=.8); Ha['arm'][-1].rotation_euler=(R(-50),0,R(10))
        q=ease(t/DUR); camset(LV((7.3,2.7,1.9),(7.4,2.9,1.9),q),hp(Ha,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['FACE']=FACE_
def SAARA_():
    Sh,Ha,W,Tr,Cl=tset(); Ha['root'].location=(8.0,4.2,0)
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); Ha['root'].location=(8.0,4.2,0); facep(Sh,(8.0,4.2)); talk(Sh,t,*ln(259,264),shapes=('O','o','O','flat')); face(Sh,brow=-.06,brow_r=-22); arm_to(Sh,1,hp(Ha,-.3),tl(t,.2,.5),base=(-30,0,0))
        Sh['root'].location[2]=0
        q=ease(t/DUR); camset(LV((7.65,3.9,2.05),(7.6,3.85,2.05),q),hp(Sh,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['SAARA']=SAARA_
def BHAI_():
    Sh,Ha,W,Tr,Cl=tset(); Ha['root'].location=(8.0,4.2,0); crumbs(Ha); bx=in_hand(Ha,-1,lambda e: halwa_box(e,1.5,True))
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); Ha['root'].location=(8.0,4.2,0); facep(Ha,(6.6,3.0)); talk(Ha,t,*ln(265,269),shapes=('o','flat','o','grin'),rest='grin'); face(Ha,brow=.05,brow_r=12); Ha['arm'][-1].rotation_euler=(R(-50),0,R(10))
        gest(Ha,t,1,1.0,6,-60)
        q=ease(t/DUR); camset(LV((7.05,3.15,1.9),(7.15,3.3,1.9),q),hp(Ha,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['BHAI']=BHAI_
def STARES_():
    Sh,Ha,W,Tr,Cl=tset()
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); Tr['root'].location=(5.0,3.8,0); facep(Sh,(4.2,1.0)); face(Sh,mouth='flat',brow=-.02,brow_r=-6,eyes=.7); shk(Sh,0)
        q=ease(t/DUR); camset(LV((4.9,1.6,1.95),(5.25,2.0,1.95),q),hp(Sh,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['STARES']=STARES_
def IZZAT_():
    Sh,Ha,W,Tr,Cl=tset()
    def upd(t):
        tidl(Sh,Ha,W,Tr,Cl,t); Tr['root'].location=(5.0,3.8,0); facep(Sh,(4.2,1.0)); shk(Sh,0); talk(Sh,t,*ln(275,281),rest='frown'); face(Sh,brow=.04,brow_r=20,eyes=.85); headtouch(Sh,1,tl(t,.4,.8),dx=.2,dy=-1.0,dz=-1.5)
        q=ease(t/DUR); camset(LV((5.25,2.0,1.95),(5.35,2.12,1.95),q),hp(Sh,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['IZZAT']=IZZAT_
W_=json.load(open(LH+'/audio/words.json'))
