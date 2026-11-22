# Shots for "The Sindhi Family". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=51.4
SEQ=[('OPEN', 0.0), ('VISIT', 1.14), ('EVENT', 4.0), ('MEET', 5.75), ('VISITS', 6.83), ('BAS', 9.6), ('CHAI', 12.74), ('TEA', 14.04), ('FOOD', 15.25), ('FRUIT', 16.61), ('ANOTHER', 17.75), ('BASHO', 19.68), ('MEHMAAN', 21.39), ('LATER', 25.32), ('AUNT', 28.04), ('LEJAO', 29.97), ('KHALA', 31.03), ('TOH', 33.73), ('CAR', 35.4), ('FOLLOW', 37.4), ('RUKO', 38.89), ('FREEZE', 39.97), ('BAG', 41.28), ('BIRYANI', 43.18), ('CAMERA', 46.04), ('GROCERY', 47.61)]
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
TY=1.6
LEVELS={1:[('tea',0,TY)],2:[('biryani',-.85,TY),('karahi',.55,TY+.05)],3:[('fruit',1.45,TY-.05)],4:[('kebab',-1.5,TY+.05),('naan',-.2,TY-.12),('halwa',.9,TY-.18)]}
def table_food(upto=4,pop_at=None):
    E={}
    for lv in range(1,upto+1):
        for (k,x,y) in LEVELS[lv]:
            e=dish(x,y,k); E[(lv,k)]=e
            if pop_at and lv in pop_at:
                t0=pop_at[lv]+.12*LEVELS[lv].index((k,x,y)); e.scale=(0,0,0)
                def fn(o,t,t0=t0): k_=pop(t-t0) if t>=t0 else 0; o.scale=(k_,k_,k_)
                fx.add(e,fn)
    return E
def room_set(kind='day'):
    baithak(); B.done('baithak'); setup_interior(kind,room=(0,0,3.6),res=PCT,samples=SAMPLES,shadow_dist=18)
    point((0,0,2.6),180 if kind=='day' else 260,(1,.86,.6),.4,False); point((0,-1.5,2.2),90,(1,.95,.88),1.0,False)
DZ=.5
def seated(H,t): sit(H,1,DZ,legs=60); blink(H,t)
def family(room=True,ali_seat=True):
    Al=mk(ALI,0,3.05,0,'ali'); Ch=mk(CHACHA,-1.55,3.05,15,'chacha'); Da=mk(DADI,1.6,3.05,-12,'dadi'); Kh=mk(KHALA,2.6,1.2,40,'khala'); Co=mk(COUSIN,-2.9,1.4,-30,'cousin')
    return Al,Ch,Da,Kh,Co
def fam_idle(F,t,ali=True):
    Al,Ch,Da,Kh,Co=F
    if ali: seated(Al,t)
    seated(Ch,t); Ch['root'].rotation_euler[2]=R(15); seated(Da,t); Da['root'].rotation_euler[2]=R(-12); stand(Kh,t); blink(Kh,t); stand(Co,t); blink(Co,t)
def lane_set(dusk=False):
    lane(dusk); B.done('lane'); setup_world('dusk' if dusk else 'morning_s',shadow=50)
    if dusk: point((1.6,2.6,2.6),220,(1,.82,.55),.5,False); point((-1,-1.5,2.8),200,(1,.85,.65),1.0,False)
    car=sedan((-5.2,-1.7,0),0); return car
DOOR=(0,3.35)

# ================================================================ HOOK
def OPEN_():
    room_set(); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4)
    def upd(t):
        fam_idle(F,t); face(Al,mouth='flat',brow=.05,brow_r=10); Al['head'].rotation_euler[2]=R(10*math.sin(t*2))
        for H in (Ch,Da,Kh,Co): face(H,mouth='grin'); look_at(H,hp(Al),.7)
        Kh['arm'][1].rotation_euler=(R(-80),0,R(10)); Co['arm'][1].rotation_euler=(R(-80),0,R(-10))
        q=ease(t/DUR); camset(LV((0,-2.9,2.6),(0,-1.4,1.7),q),LV((0,2.2,.8),(0,2.6,1.3),q),22,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def VISIT_():
    car=lane_set(); Al=mk(ALI,-1.2,1.0,180,'ali'); cc=clock_card((-1.6,1.4,3.6),.4,'10 MIN',spin=.2,col='#1F5A3A')
    def upd(t):
        walk_path(Al,[(-3.4,.2),(-.6,2.2),(0,2.55)],t,-.4,2.4,step=.5); blink(Al,t); face(Al,mouth='smile')
        if t>2.4: stand(Al,t); Al['root'].rotation_euler[2]=R(180)
        q=ease(t/DUR); camset(LV((2.6,-2.6,1.8),(2.2,-2.2,1.8),q),(-.8,1.6,1.9),22,16)
    return dict(upd=upd)
SHOTS['VISIT']=VISIT_
def EVENT_():
    room_set(); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4); e=title_card('3-DAY EVENT',.2,(0,2.6,3.05),.3)
    def upd(t):
        fam_idle(F,t); face(Al,mouth='O',brow=.06,eyes=1.3); Al['root'].location[2]+=0
        for H in (Ch,Da,Kh,Co): face(H,mouth='grin',brow=.04); laugh(H,t+H['seed'],.5)
        q=ease(t/DUR); camset(LV((0,-.9,1.6),(0,-.5,1.65),q),(0,2.9,1.9),26,8)
    return dict(upd=upd)
SHOTS['EVENT']=EVENT_

# ================================================================ SCENE 1 — the doorstep
def MEET_():
    car=lane_set(); Al=mk(ALI,0,2.55,180,'ali'); label('ALI',(0,2.55,3.0),.15,col='#1F3A6A',bg='#DFEBFF')
    def upd(t):
        stand(Al,t); blink(Al,t); Al['root'].rotation_euler[2]=R(lerp_angle(180,-20,tl(t,.0,.4)))
        k=tl(t,.4,.7); Al['arm'][1].rotation_euler=(R(-150*k),0,R(20*k)); face(Al,mouth='grin')
        q=ease(t/DUR); camset(LV((.8,-.6,1.75),(.6,-.2,1.78),q),(0,2.55,1.75),30,8)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def door_scene(t,Al,Ch,d):
    stand(Al,t); blink(Al,t); stand(Ch,t); blink(Ch,t); Al['root'].location=(-.45,2.45,0); Ch['root'].location=(.55,3.0,0)
def VISITS_():
    car=lane_set(); Al=mk(ALI,-.45,2.45,180,'ali'); Ch=mk(CHACHA,.55,3.0,-140,'chacha')
    def upd(t):
        door_scene(t,Al,Ch,None); k=tl(t,.6,1.1); Al['root'].rotation_euler[2]=R(119); Ch['root'].rotation_euler[2]=R(-61)
        arm_to(Ch,1,hp(Al,-.9),k,base=(-40,0,0)); arm_to(Ch,-1,hp(Al,-.8),k,base=(-40,0,0)); face(Ch,mouth='grin',brow=.05); face(Al,mouth='smile')
        Ch['root'].location=(L(.55,.15,k),L(3.0,2.75,k),0); Al['arm'][1].rotation_euler=(R(-60*k),0,R(-20)); Al['arm'][-1].rotation_euler=(R(-60*k),0,R(20))
        q=ease(t/DUR); camset(LV((2.4,-.6,1.8),(2.1,-.2,1.8),q),(.1,2.7,1.75),28,8)
    return dict(upd=upd)
SHOTS['VISITS']=VISITS_
def BAS_():
    car=lane_set(); Al=mk(ALI,-.45,2.45,117,'ali'); Ch=mk(CHACHA,.35,2.85,-50,'chacha')
    def upd(t):
        door_scene(t,Al,Ch,None); Ch['root'].location=(.35,2.85,0); Al['root'].rotation_euler[2]=R(117); Ch['root'].rotation_euler[2]=R(-50); talk(Al,t,9.6,12.5); face(Al,brow=.04)
        g=math.sin(t*5); Al['arm'][1].rotation_euler=(R(-60-15*g),0,R(-15)); k=tl(t,1.6,1.9); Al['arm'][-1].rotation_euler=(R(-80*k),0,R(30*k)); face(Ch,mouth='smile')
        q=ease(t/DUR); camset(LV((1.25,2.05,1.85),(1.1,2.1,1.86),q),hp(Al,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['BAS']=BAS_
def CHAI_():
    car=lane_set(); Al=mk(ALI,-.45,2.45,117,'ali'); Ch=mk(CHACHA,.35,2.85,-50,'chacha')
    def upd(t):
        door_scene(t,Al,Ch,None); Ch['root'].location=(.35,2.85,0); Al['root'].rotation_euler[2]=R(117); Ch['root'].rotation_euler[2]=R(lerp_angle(-61,-25,tl(t,.2,.6)))
        talk(Ch,t,12.74,13.8); face(Ch,brow=-.02,brow_r=-6); k=tl(t,.3,.6); arm_to(Ch,1,(.5,6,1.2),k,base=(-30,0,0)); arm_to(Ch,-1,hp(Al,-.7),k,base=(-30,0,0))
        q=ease(t/DUR); camset(LV((.05,.9,1.95),(.08,1.1,1.96),q),hp(Ch,-.05),42,2.8)
    return dict(upd=upd)
SHOTS['CHAI']=CHAI_

# ================================================================ SCENE 2 — the food keeps coming
def sip(Al,t,k=1.0): Al['arm'][1].rotation_euler=(R(-110*k),0,R(-28*k)); Al['head'].rotation_euler[0]=R(-8*k)
def TEA_():
    room_set(); F=family(); Al,Ch,Da,Kh,Co=F; table_food(1); cp=in_hand(Al,1,lambda e: ocyl((0,-.06,.08),.05,.1,M('#F4F1EA',.4),e,rot=(0,0,0),seg=12))
    def upd(t):
        fam_idle(F,t); k=math.sin(pi*tl(t,.2,1.1)); sip(Al,t,k); face(Al,mouth='smile' if k<.5 else 'o')
        for H in (Ch,Da): face(H,mouth='grin'); look_at(H,hp(Al),.6)
        q=ease(t/DUR); camset(LV((.9,-.4,1.3),(.7,-.1,1.32),q),(0,2.4,1.3),28,8)
    return dict(upd=upd)
SHOTS['TEA']=TEA_
def serve(Kh,t,t0,dur=.7,x=-.85):
    k=math.sin(pi*tl(t,t0-.3,t0+dur)); Kh['root'].location=(L(2.6,x+.2,k),L(1.2,1.0,k),0); arm_to(Kh,1,(x,TY,.6),k,base=(-60,0,0)); arm_to(Kh,-1,(x,TY,.6),k,base=(-60,0,0)); face(Kh,mouth='grin')
def FOOD_():
    room_set(); F=family(); Al,Ch,Da,Kh,Co=F; table_food(2,{2:.45})
    def upd(t):
        fam_idle(F,t); serve(Kh,t,.45,.8,-.3); face(Al,mouth='o',brow=.04); look_at(Al,(-.3,TY,.5),.6); face(Ch,mouth='grin')
        q=ease(t/DUR); camset(LV((0,-.8,1.9),(0,-.5,1.85),q),(0,1.9,.9),28,8)
    return dict(upd=upd)
SHOTS['FOOD']=FOOD_
def FRUIT_():
    room_set(); F=family(); Al,Ch,Da,Kh,Co=F; table_food(3,{3:.25}); sparkles((1.45,TY,.8),.3,.3,1.4,12,.03,13,.3)
    def upd(t):
        fam_idle(F,t); serve(Kh,t,.25,.7,1.45); face(Al,mouth='O',brow=.05,eyes=1.15); look_at(Al,(1.45,TY,.5),.7)
        q=ease(t/DUR); camset(LV((-.4,-.4,1.5),(-.3,-.1,1.5),q),(.9,2.2,.9),30,8)
    return dict(upd=upd)
SHOTS['FRUIT']=FRUIT_
def ANOTHER_():
    room_set(); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4,{4:.35})
    def upd(t):
        fam_idle(F,t); serve(Kh,t,.35,1.1,-.2); k=tl(t,.6,1.1); face(Al,mouth='O',brow=.07,eyes=1.35); Al['root'].rotation_euler[0]=R(10*k)
        Co['arm'][1].rotation_euler=(R(-150),0,R(20)); face(Co,mouth='grin'); Ch['arm'][1].rotation_euler=(R(-90),0,R(-20)); face(Ch,mouth='grin',brow=.05)
        q=ease(t/DUR); camset(LV((0,-1.6,1.4),(0,-.8,1.3),q),(0,2.4,1.0),24,16)
    return dict(upd=upd)
SHOTS['ANOTHER']=ANOTHER_
def BASHO_():
    room_set(); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4)
    def upd(t):
        fam_idle(F,t); talk(Al,t,19.68,21.15); face(Al,brow=.06,brow_r=14,eyes=1.1); k=tl(t,.1,.35); Al['arm'][1].rotation_euler=(R(-120*k),0,R(-12)); Al['arm'][-1].rotation_euler=(R(-40*k),0,R(-40*k))
        Al['head'].rotation_euler[2]=R(-15)
        q=ease(t/DUR); camset(LV((-.3,1.0,1.55),(-.25,1.25,1.56),q),hp(Al,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['BASHO']=BASHO_
def MEHMAAN_():
    room_set(); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4)
    def upd(t):
        fam_idle(F,t); Ch['root'].rotation_euler[2]=R(40); talk(Ch,t,21.39,25.1); face(Ch,brow=.0); g=math.sin(t*4); arm_to(Ch,1,hp(Al,-.6),tl(t,.2,.5),base=(-30,0,0)); Ch['arm'][-1].rotation_euler=(R(-70-15*g),0,R(-30))
        look_at(Al,hp(Ch),.6); face(Al,mouth='flat',brow=.04)
        q=ease(t/DUR); camset(LV((-.5,1.0,1.55),(-.6,1.2,1.56),q),hp(Ch,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['MEHMAAN']=MEHMAAN_

# ================================================================ SCENE 3 — three hours later
def LATER_():
    room_set('evening'); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4); title_card('3 HOURS LATER...',.15,(0,2.8,2.6),.3)
    def upd(t):
        fam_idle(F,t,ali=False); k=ease(tl(t,.7,1.8)); sit(Al,1-.55*k,DZ,legs=60); Al['root'].location[2]+=.0; blink(Al,t); Al['root'].rotation_euler[0]=R(-8*k)
        Al['arm'][1].rotation_euler=(R(-30),0,R(-40)); Al['arm'][-1].rotation_euler=(R(-60*k),0,R(40)); face(Al,mouth='flat',brow=.05,eyes=.85)
        Da['head'].rotation_euler[0]=R(16); face(Da,mouth='flat',eyes=.4)
        q=ease(t/DUR); camset(LV((0,-2.2,1.6),(0,-1.6,1.5),q),(0,2.6,1.3),24,16)
    return dict(upd=upd)
SHOTS['LATER']=LATER_
def stood(Al,t): stand(Al,t); blink(Al,t); Al['root'].location=(0,2.65,0); Al['root'].rotation_euler[2]=0
def AUNT_():
    room_set('evening'); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4); tf=in_hand(Kh,1,lambda e: tiffin(e,1.5))
    def upd(t):
        fam_idle(F,t,ali=False); stood(Al,t); face(Al,mouth='o',brow=.05)
        walk_path(Kh,[(3.6,-2.6),(2.4,-.6),(1.1,1.0)],t,-.1,1.6,step=.45); Kh['arm'][1].rotation_euler=(R(-85),0,R(10)); face(Kh,mouth='grin',brow=.04)
        if t>1.6: stand(Kh,t); Kh['root'].location=(1.1,1.0,0); facep(Kh,(0,2.65))
        look_at(Al,hp(Kh),.7)
        q=ease(t/DUR); camset(LV((-1.6,-1.8,1.7),(-1.3,-1.4,1.7),q),(.8,1.6,1.5),26,8)
    return dict(upd=upd)
SHOTS['AUNT']=AUNT_
def kh_pose(Kh,Al,t):
    stand(Kh,t); blink(Kh,t); Kh['root'].location=(.75,1.55,0); facep(Kh,(0,2.65))
def LEJAO_():
    room_set('evening'); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4); tf=in_hand(Kh,1,lambda e: tiffin(e,1.5))
    def upd(t):
        fam_idle(F,t,ali=False); stood(Al,t); kh_pose(Kh,Al,t); talk(Kh,t,29.97,30.95); face(Kh,brow=.04); arm_to(Kh,1,hp(Al,-1.0),tl(t,.1,.4),base=(-70,0,0))
        q=ease(t/DUR); camset(LV((-.7,1.85,1.75),(-.6,1.95,1.76),q),hp(Kh,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['LEJAO']=LEJAO_
def KHALA_():
    room_set('evening'); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4); tf=in_hand(Kh,1,lambda e: tiffin(e,1.5))
    def upd(t):
        fam_idle(F,t,ali=False); stood(Al,t); kh_pose(Kh,Al,t); arm_to(Kh,1,hp(Al,-1.0),1,base=(-70,0,0)); talk(Al,t,31.03,33.5); face(Al,brow=.06,brow_r=16,eyes=1.15)
        g=math.sin(t*7); Al['arm'][1].rotation_euler=(R(-90-20*g),0,R(-25)); Al['arm'][-1].rotation_euler=(R(-90+20*g),0,R(25))
        q=ease(t/DUR); camset(LV((.5,.55,1.85),(.45,.8,1.86),q),hp(Al,-.03),42,2.8)
    return dict(upd=upd)
SHOTS['KHALA']=KHALA_
def TOH_():
    room_set('evening'); F=family(); Al,Ch,Da,Kh,Co=F; table_food(4); tf=in_hand(Kh,1,lambda e: tiffin(e,1.5)); ta=in_hand(Al,1,lambda e: tiffin(e,1.5)); tg=.9
    def upd(t):
        fam_idle(F,t,ali=False); stood(Al,t); kh_pose(Kh,Al,t); talk(Kh,t,33.73,35.3,rest='grin'); face(Kh,brow=.05)
        k=tl(t,.3,tg); arm_to(Kh,1,hp(Al,-1.05),k*(1-tl(t,tg+.1,tg+.4))+(1-k)*.6,base=(-70,0,0)); tf.scale=(1,1,1) if t<tg else (0,0,0); ta.scale=(0,0,0) if t<tg else (1,1,1)
        Al['arm'][1].rotation_euler=(R(-75*(t>tg)),0,R(-10)); face(Al,mouth='frown' if t>tg else 'o',brow=.05)
        for H in (Ch,Da,Co): face(H,mouth='grin')
        q=ease(t/DUR); camset(LV((-1.4,-.2,1.6),(-1.2,.1,1.6),q),(.4,2.1,1.5),28,8)
    return dict(upd=upd)
SHOTS['TOH']=TOH_

# ================================================================ SCENE 4 — the car
def ali_full(Al):
    a=in_hand(Al,1,lambda e: tiffin(e,1.5)); b=in_hand(Al,-1,lambda e: pot_bag(e,1.4)); return a,b
def CAR_():
    car=lane_set(True); Al=mk(ALI,0,2.4,180,'ali'); a,b=ali_full(Al)
    def upd(t):
        walk_path(Al,[(0,2.4),(-1.6,.6),(-3.2,-.6)],t,0,DUR+.3,step=.4,mood=-1); blink(Al,t); Al['arm'][1].rotation_euler=(R(-65),0,R(10)); Al['arm'][-1].rotation_euler=(R(-65),0,R(-10)); face(Al,mouth='flat',brow=.03)
        q=ease(t/DUR); camset(LV((1.8,-2.6,1.8),(1.5,-2.3,1.8),q),(-1.6,1.0,1.3),24,16)
    return dict(upd=upd)
SHOTS['CAR']=CAR_
AP=(-3.2,-.6)
def car_scene(dusk=True):
    car=lane_set(True); Al=mk(ALI,AP[0],AP[1],-61,'ali'); a,b=ali_full(Al); Ch=mk(CHACHA,0,2.6,180,'chacha'); return car,Al,a,b,Ch
def ali_hold(Al,t):
    stand(Al,t); blink(Al,t); Al['root'].location=(AP[0],AP[1],0); Al['arm'][1].rotation_euler=(R(-65),0,R(10)); Al['arm'][-1].rotation_euler=(R(-65),0,R(-10))
def FOLLOW_():
    car,Al,a,b,Ch=car_scene(); bg=in_hand(Ch,1,lambda e: shopper(e,1.6,'#F2C14E','BIRYANI'))
    def upd(t):
        ali_hold(Al,t); Al['root'].rotation_euler[2]=R(-61); face(Al,mouth='flat')
        walk_path(Ch,[(0,2.6),(-.9,1.2)],t,-.1,1.3,step=.45); blink(Ch,t); Ch['arm'][1].rotation_euler=(R(-40),0,R(10)); face(Ch,mouth='grin')
        if t>1.3: stand(Ch,t); Ch['root'].location=(-.9,1.2,0)
        q=ease(t/DUR); camset(LV((1.6,-2.6,1.6),(1.3,-2.2,1.6),q),(-1.4,1.0,1.5),26,16)
    return dict(upd=upd)
SHOTS['FOLLOW']=FOLLOW_
def ch_near(Ch,t):
    stand(Ch,t); blink(Ch,t); Ch['root'].location=(-1.9,.2,0); facep(Ch,AP)
def RUKO_():
    car,Al,a,b,Ch=car_scene(); bg=in_hand(Ch,1,lambda e: shopper(e,1.6,'#F2C14E','BIRYANI'))
    def upd(t):
        ali_hold(Al,t); ch_near(Ch,t); talk(Ch,t,38.89,39.9); face(Ch,brow=.05); arm_to(Ch,-1,hp(Al),tl(t,.0,.25),base=(-30,0,0)); Ch['arm'][1].rotation_euler=(R(-40),0,R(10))
        q=ease(t/DUR); camset(LV((-3.0,-2.0,1.9),(-2.9,-1.8,1.9),q),hp(Ch,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['RUKO']=RUKO_
def FREEZE_():
    car,Al,a,b,Ch=car_scene()
    def upd(t):
        ali_hold(Al,0); Al['root'].rotation_euler[2]=R(-61); blink(Al,0); face(Al,mouth='O',brow=.07,eyes=1.4); k=tl(t,.0,.2); Al['leg'][1].rotation_euler[0]=R(-30); Al['root'].location[2]=.0
        q=t/DUR; camset(LV((-4.6,-2.6,1.9),(-4.3,-2.2,1.9),q),hp(Al,-.1),40,4)
    return dict(upd=upd)
SHOTS['FREEZE']=FREEZE_
def BAG_():
    car,Al,a,b,Ch=car_scene(); bg=in_hand(Ch,1,lambda e: shopper(e,1.6,'#F2C14E','BIRYANI')); bga=in_hand(Al,1,lambda e: shopper(e,1.6,'#F2C14E','BIRYANI')); tg=1.0
    def upd(t):
        ali_hold(Al,t); Al['root'].rotation_euler[2]=R(lerp_angle(-61,60,tl(t,0,.5))); ch_near(Ch,t); Ch['root'].location=(-2.5,-.2,0); facep(Ch,AP)
        k=tl(t,.3,tg); arm_to(Ch,1,(AP[0]+.45,AP[1]+.2,1.2),k*(1-tl(t,tg+.1,tg+.4)),base=(-40,0,0)); bg.scale=(1,1,1) if t<tg else (0,0,0); bga.scale=(0,0,0) if t<tg else (1,1,1); a.scale=(0,0,0) if t>tg else (1,1,1)
        face(Ch,mouth='grin',brow=.05); face(Al,mouth='flat' if t<tg else 'frown',brow=.05)
        q=ease(t/DUR); camset(LV((-1.0,-3.0,1.7),(-1.2,-2.7,1.7),q),(-2.9,-.4,1.45),30,8)
    return dict(upd=upd)
SHOTS['BAG']=BAG_
def BIRYANI_():
    car,Al,a,b,Ch=car_scene(); bga=in_hand(Al,1,lambda e: shopper(e,1.6,'#F2C14E','BIRYANI')); a.scale=(0,0,0)
    def upd(t):
        ali_hold(Al,t); Al['root'].rotation_euler[2]=R(60); a.scale=(0,0,0); ch_near(Ch,t); Ch['root'].location=(-2.5,-.2,0); facep(Ch,AP,.45,cam=(-1.0,-1.6)); talk(Ch,t,43.18,45.9); face(Ch,brow=.05)
        g=math.sin(t*4); Ch['arm'][1].rotation_euler=(R(-35-10*g),0,R(25)); Ch['arm'][-1].rotation_euler=(R(-30),0,R(-20))
        q=ease(t/DUR); camset(LV((-1.0,-1.6,1.85),(-1.1,-1.4,1.86),q),hp(Ch,-.05),42,2.8)
    return dict(upd=upd)
SHOTS['BIRYANI']=BIRYANI_
def CAMERA_():
    car,Al,a,b,Ch=car_scene(); bga=in_hand(Al,1,lambda e: shopper(e,1.6,'#F2C14E','BIRYANI')); a.scale=(0,0,0); cam=(AP[0]-.2,AP[1]-2.6,1.95)
    def upd(t):
        ali_hold(Al,t); a.scale=(0,0,0); ch_near(Ch,t); Ch['root'].location=(-2.5,-.2,0); face(Ch,mouth='grin')
        Al['root'].rotation_euler[2]=R(lerp_angle(60,0,ease(tl(t,.2,.9)))); Al['head'].rotation_euler[0]=R(4); face(Al,mouth='flat',brow=.02,eyes=.85)
        q=ease(t/DUR); camset(LV(cam,(cam[0],cam[1]+.6,cam[2]),q),hp(Al,-.05),35,2.8)
    return dict(upd=upd)
SHOTS['CAMERA']=CAMERA_
def GROCERY_():
    car,Al,a,b,Ch=car_scene(); bga=in_hand(Al,1,lambda e: shopper(e,1.6,'#F2C14E','BIRYANI')); a.scale=(0,0,0); cam=(AP[0]-.2,AP[1]-2.0,1.95)
    def upd(t):
        ali_hold(Al,t); a.scale=(0,0,0); ch_near(Ch,t); Ch['root'].location=(-2.5,-.2,0); face(Ch,mouth='grin')
        Al['root'].rotation_euler[2]=0; talk(Al,t,47.61,50.6); face(Al,brow=.03,eyes=.85); Al['head'].rotation_euler=(R(4),R(6*math.sin(t*1.5)),0)
        q=ease(t/DUR); camset(LV(cam,(cam[0],cam[1]+.5,cam[2]),q),hp(Al,-.1),38,2.8)
    return dict(upd=upd)
SHOTS['GROCERY']=GROCERY_
W_=json.load(open(LH+'/audio/words.json'))
