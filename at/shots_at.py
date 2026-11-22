# Shots for "Ashraf Tawa Takes Over" (invented legend). Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=61.0
SEQ=[('OPEN', 0.0), ('STOP', 1.07), ('NAME', 4.29), ('MEET', 5.67), ('SHOW', 8.95), ('VADDA', 10.87), ('LAUGH', 13.67), ('NAAM', 15.01), ('STOPS', 17.58), ('EVERY', 19.24), ('GYM', 21.45), ('BARBER', 22.38), ('GRAN', 23.6), ('WARGA', 25.48), ('DECIDES', 28.02), ('ARRIVES', 31.02), ('CROWD', 32.81), ('MUSIC', 33.95), ('WALKS', 35.17), ('FAISLA', 37.36), ('KAUN', 39.09), ('PAWA', 40.95), ('SMILES', 42.67), ('TAWA', 44.05), ('PREP', 45.81), ('PHONE', 47.67), ('SELFIE', 49.48), ('RUSH', 52.67), ('PUSHED', 55.5), ('FINAL', 57.7)]
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
RING=(0,4)
def chowk_set(mood='afternoon',crowd=0,seed=1,ring=False):
    chowk(); B.done('chowk'); setup_world(mood,shadow=60); C=[]
    cc=crowd_cast(max(crowd,1),seed)
    for i in range(crowd):
        if ring:
            a=pi*(.08+.84*i/max(1,crowd-1)); r_=4.3+.5*(i%2); x=math.cos(a)*r_; y=RING[1]+math.sin(a)*r_*.9
            if i%3==2: a2=pi+pi*(.15+.7*((i//3)/(max(1,crowd//3)))); x=math.cos(a2)*4.4*1.0; y=RING[1]+math.sin(a2)*1.4-1.2
        else:
            r=random.Random(seed*31+i); x=r.uniform(-9,9); y=r.uniform(-3,8)
        H=mk(cc[i],x,y,face_dir(RING[0]-x,RING[1]-y),'cr%d'%i); C.append(H)
    return C
def crowd_idle(C,t,cheer=0.0,look=None):
    for i,H in enumerate(C):
        stand(H,t+i*.7); blink(H,t+i)
        if look: look_at(H,look,.7)
        if cheer>0:
            g=math.sin(t*9+i); H['arm'][1].rotation_euler=(R(-150-20*g*cheer),0,R(15)); H['arm'][-1].rotation_euler=(R(-60-90*cheer*(i%2)),0,R(-15)); face(H,mouth='grin' if i%2 else 'O',brow=.05)
            H['root'].location[2]=.08*abs(math.sin(t*7+i))*cheer
def shop_cam(): pass

# ================================================================ HOOK
def OPEN_():
    C=chowk_set(crowd=10,seed=2); As=mk(ASHRAF,0,8.0,0,'ashraf'); Pw=None
    def upd(t):
        crowd_idle(C,0 if t>.5 else t,look=hp(As)); stand(As,t); blink(As,t); face(As,mouth='flat',brow=-.03,brow_r=-10)
        for i,H in enumerate(C):
            k=tl(t,.3+.05*i,.6+.05*i); face(H,mouth='O',brow=.06*k,eyes=1+.3*k)
        q=ease(t/DUR); camset(LV((0,-6,7),(0,-5,3.6),q),(0,5,1.4),22,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def STOP_():
    C=chowk_set(crowd=8,seed=3); cart=None
    def upd(t):
        for i,H in enumerate(C):
            if t<1.0: walk(H,t*1.1+i,step=.45)
            else: stand(H,0); H['root'].rotation_euler[2]=R(0); face(H,mouth='O',brow=.06,eyes=1.3)
            blink(H,t); H['root'].location[0]+=(.012 if t<1.0 else 0)
        q=ease(t/DUR); camset(LV((-6,-4.4,3.4),(-4.5,-4.0,3.0),q),(0,3,1.2),24,16)
    return dict(upd=upd)
SHOTS['STOP']=STOP_
def NAME_():
    C=chowk_set('dusk',crowd=0); As=mk(ASHRAF,0,6.5,0,'ashraf'); title_card('ASHRAF TAWA!',.05,(0,4.2,4.6),.5)
    point((0,9.5,2.5),900,(1,.8,.5),.6,False)
    for i in range(10): puff((random.Random(i).uniform(-2,2),6.0+random.Random(i+5).uniform(-.5,.5),.1),.1+i*.04,.35,6,M('#C8A878',.9),.6,1.2,seed=i)
    def upd(t):
        stand(As,t); blink(As,t); k=tl(t,.1,.5); As['arm'][1].rotation_euler=(R(-25*k),0,R(-50*k)); As['arm'][-1].rotation_euler=(R(-25*k),0,R(50*k)); face(As,mouth='smirk',brow=-.03,brow_r=-12)
        q=ease(t/DUR); camset(LV((0,1.0,.4),(0,1.6,.5),q),(0,6.5,2.2),24,16)
    return dict(upd=upd)
SHOTS['NAME']=NAME_

# ================================================================ SCENE 1
PX=-1.0
def MEET_():
    C=chowk_set(crowd=6,seed=4); Pw=mk(PAWA,-6,-1.2,90,'pawa')
    lb=label('PAWA',(-1.0,-1.2,3.2),.4,col='#7A1F1F')
    def upd(t):
        crowd_idle(C,t); walk_path(Pw,[(-6,-1.2),(PX,-1.2)],t,-.2,DUR,step=.55); blink(Pw,t); face(Pw,mouth='smirk',brow=-.02); x=Pw['root'].location[0]
        Pw['arm'][1].rotation_euler[2]+=R(10); Pw['root'].rotation_euler[1]=R(5*math.sin(t*6))
        camset((x+2.6,-4.6,1.4),(x+.2,-1.2,1.6),30,8)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def pw_stand(Pw,t,x=PX):
    stand(Pw,t); blink(Pw,t); Pw['root'].location=(x,-1.2,0)
def SHOW_():
    C=chowk_set(crowd=6,seed=5); Pw=mk(PAWA,PX,-1.2,0,'pawa'); sparkles((PX,-1.2,2.2),.6,.6,2.4,20,.04,3,.4)
    def upd(t):
        crowd_idle(C,t); pw_stand(Pw,t); k=tl(t,.1,.4); g=math.sin(t*4)
        Pw['arm'][1].rotation_euler=(R(-90*k),R(-60*k),R(80*k+10*g)); Pw['arm'][-1].rotation_euler=(R(-90*k),R(60*k),R(-80*k-10*g)); face(Pw,mouth='grin',brow=-.03,brow_r=-10)
        Pw['root'].rotation_euler[2]=R(20*math.sin(t*2))
        q=ease(t/DUR); camset(LV((PX+.4,-3.6,1.1),(PX+.2,-3.2,1.2),q),(PX,-1.2,1.8),28,8)
    return dict(upd=upd)
SHOTS['SHOW']=SHOW_
def VADDA_():
    C=chowk_set(crowd=6,seed=6); Pw=mk(PAWA,PX,-1.2,0,'pawa')
    def upd(t):
        crowd_idle(C,t); pw_stand(Pw,t); talk(Pw,t,10.87,13.3); face(Pw,brow=-.03,brow_r=-10); g=math.sin(t*5); Pw['arm'][1].rotation_euler=(R(-45),0,R(-55+6*g)); Pw['arm'][-1].rotation_euler=(R(-30),0,R(-40))
        Pw['head'].rotation_euler=(R(-8),0,R(8*g))
        q=ease(t/DUR); camset(LV((PX+.3,-2.7,1.75),(PX+.25,-2.4,1.78),q),hp(Pw,-.03),42,2.8)
    return dict(upd=upd)
SHOTS['VADDA']=VADDA_
def duo(seed):
    C=chowk_set(crowd=6,seed=seed); Pw=mk(PAWA,PX,-1.2,30,'pawa'); Jo=mk(JOJO,PX+1.3,-1.6,-50,'jojo'); return C,Pw,Jo
def LAUGH_():
    C,Pw,Jo=duo(7)
    def upd(t):
        crowd_idle(C,t); pw_stand(Pw,t); Pw['root'].rotation_euler[2]=R(lerp_angle(0,50,tl(t,.2,.6))); face(Pw,mouth='flat',brow=.03)
        stand(Jo,t); blink(Jo,t); laugh(Jo,t,1.2); Jo['root'].rotation_euler[0]=R(-10*abs(math.sin(t*5))); Jo['arm'][-1].rotation_euler=(R(-60),0,R(30)); Jo['arm'][1].rotation_euler=(R(-40-30*abs(math.sin(t*8))),0,R(10))
        q=ease(t/DUR); camset(LV((PX+.6,-4.6,1.6),(PX+.6,-4.2,1.6),q),(PX+.65,-1.4,1.5),28,8)
    return dict(upd=upd)
SHOTS['LAUGH']=LAUGH_
def NAAM_():
    C,Pw,Jo=duo(8)
    def upd(t):
        crowd_idle(C,t); pw_stand(Pw,t); Pw['root'].rotation_euler[2]=R(50); stand(Jo,t); blink(Jo,t); talk(Jo,t,15.01,17.1); face(Jo,brow=.05,brow_r=8); Jo['root'].rotation_euler[2]=R(-30)
        arm_to(Jo,1,(0,10.4,2.3),tl(t,.6,.9),base=(-30,0,0))
        q=ease(t/DUR); camset(LV((PX+2.4,-3.4,1.55),(PX+2.2,-3.1,1.56),q),hp(Jo,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['NAAM']=NAAM_
def STOPS_():
    C,Pw,Jo=duo(9)
    def upd(t):
        crowd_idle(C,t); pw_stand(Pw,t); Pw['root'].rotation_euler[2]=R(15); k=tl(t,.2,.9)
        face(Pw,mouth='smirk' if k<.4 else ('flat' if k<.8 else 'frown'),brow=.06*k,eyes=1+.25*k); Pw['head'].rotation_euler[0]=R(4)
        q=ease(t/DUR); camset(LV((PX+.3,-3.6,1.95),(PX+.3,-2.6,1.95),q),hp(Pw,-.03),45,2.8)
    return dict(upd=upd)
SHOTS['STOPS']=STOPS_

# ================================================================ SCENE 2 — the name everywhere
def EVERY_():
    C=chowk_set(crowd=0,seed=10); Pw=mk(PAWA,-8,8.6,90,'pawa')
    for (x,z) in ((-6.5,1.5),(-3.5,2.5),(-1.5,1.4),(2.5,1.8),(4.5,2.6)): poster((x,10.45,z),s=1.0)
    def upd(t):
        walk_path(Pw,[(-8,8.6),(-2,8.6)],t,-.2,DUR,step=.45); blink(Pw,t); x=Pw['root'].location[0]; Pw['head'].rotation_euler[2]=R(70*math.sin(t*1.5)); face(Pw,mouth='frown',brow=.05)
        camset((x+1.0,4.6,1.8),(x-.1,9.2,1.7),26,8)
    return dict(upd=upd)
SHOTS['EVERY']=EVERY_
def GYM_():
    gym(); B.done('gym'); setup_interior('day',room=(0,0,3.2),res=PCT,samples=SAMPLES); Gb=mk(GYMBRO,-.4,1.8,20,'gb'); Pw=mk(PAWA,1.8,.6,-60,'pawa')
    def upd(t):
        stand(Gb,t); blink(Gb,t); stand(Pw,t); blink(Pw,t); arm_to(Gb,1,(-1.0,2.9,2.1),tl(t,.1,.35),base=(-30,0,0)); face(Gb,mouth='grin',brow=.04); mouth_talk(Gb,t,.2,.8)
        look_at(Pw,(-1.0,2.9,2.1),.8); face(Pw,mouth='frown',brow=.05)
        camset((2.6,-1.4,2.5),(-.4,1.8,1.6),26,8)
    return dict(upd=upd)
SHOTS['GYM']=GYM_
def BARBER_():
    barber(); B.done('barber'); setup_interior('day',room=(0,0,3.2),res=PCT,samples=SAMPLES); Bb=mk(BARBER,-.9,1.4,30,'barber'); Pw=mk(PAWA,-1.5,2.0,180,'pawa')
    sc=in_hand(Bb,1,lambda e:(obox((0,-.06,.12),(.01,.03,.1),M('#C9CED8',.3,metal=.9),0,e),obox((.02,-.06,.12),(.01,.03,.1),M('#C9CED8',.3,metal=.9),0,e,rot=(0,R(20),0))))
    def upd(t):
        sit(Pw,1,.66,legs=80); blink(Pw,t); Pw['root'].location=(-1.5,2.0,Pw['root'].location[2]); Pw['root'].rotation_euler[2]=R(180)
        stand(Bb,t); blink(Bb,t); arm_to(Bb,-1,(2.9,2.9,2.3),tl(t,.1,.35),base=(-30,0,0)); Bb['arm'][1].rotation_euler=(R(-90),0,R(10)); sc.rotation_euler[1]=R(20*math.sin(t*20)); face(Bb,mouth='grin'); mouth_talk(Bb,t,.2,.9)
        face(Pw,mouth='frown',brow=.05)
        camset((1.4,-2.2,1.8),(-.6,2.0,1.6),26,8)
    return dict(upd=upd)
SHOTS['BARBER']=BARBER_
def gran_set():
    courtyard(); B.done('court'); setup_world('morning_s',shadow=40); Da=mk(DADI,-.3,2.2,0,'dadi'); Pw=mk(PAWA,1.9,1.0,-130,'pawa'); return Da,Pw
def GRAN_():
    Da,Pw=gran_set()
    def upd(t):
        sit(Da,1,.56,legs=70); blink(Da,t); Da['root'].rotation_euler[2]=R(-15); stand(Pw,t); blink(Pw,t); face(Pw,mouth='smile'); face(Da,mouth='smile')
        q=ease(t/DUR); camset(LV((1.5,-2.8,1.6),(1.2,-2.4,1.6),q),(.3,1.8,1.2),26,8)
    return dict(upd=upd)
SHOTS['GRAN']=GRAN_
def WARGA_():
    Da,Pw=gran_set()
    def upd(t):
        sit(Da,1,.56,legs=70); blink(Da,t); Da['root'].rotation_euler[2]=R(-25); talk(Da,t,25.48,27.6); face(Da,brow=.03); Da['arm'][1].rotation_euler=(R(-50-10*math.sin(t*4)),0,R(15))
        stand(Pw,t); blink(Pw,t); face(Pw,mouth='frown',brow=.06,eyes=1.2)
        q=ease(t/DUR); camset(LV((.0,.6,1.35),(.05,.85,1.36),q),hp(Da,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['WARGA']=WARGA_

# ================================================================ SCENE 3 — the showdown
def DECIDES_():
    C=chowk_set('golden',crowd=0,seed=11); Pw=mk(PAWA,PX,-1.2,0,'pawa'); hb=None
    def upd(t):
        pw_stand(Pw,t); k=tl(t,.3,.8); g=math.sin(t*14)
        Pw['arm'][1].rotation_euler=(R(-80*k),R(-40*k),R(40*k)); Pw['arm'][-1].rotation_euler=(R(-80*k),R(40*k),R(-40*k)); face(Pw,mouth='frown',brow=-.05,brow_r=-18)
        if 1.0<t<1.6: Pw['root'].location[2]=.03*abs(g)
        q=ease(t/DUR); camset(LV((PX,-2.9,1.4),(PX,-2.4,1.55),q),hp(Pw,-.15),35,4)
    return dict(upd=upd)
SHOTS['DECIDES']=DECIDES_
def ARRIVES_():
    C=chowk_set('golden',crowd=0,seed=12); Pw=mk(PAWA,0,-4,180,'pawa')
    for i in range(16): puff((random.Random(i).uniform(-1.5,1.5),-2+i*.25,.05),.1+i*.08,.3,5,M('#C8A878',.9),.5,1.0,drift=(1.2,0,.3),seed=i)
    def upd(t):
        walk_path(Pw,[(0,-4),(0,1.8)],t*.55,0,DUR*.55,step=.6); blink(Pw,t); face(Pw,mouth='frown',brow=-.05,brow_r=-16); Pw['root'].rotation_euler[2]=R(180)
        q=ease(t/DUR); camset(LV((.6,4.5,.4),(.5,4.0,.5),q),hp(Pw,-.3),28,16)
    return dict(upd=upd)
SHOTS['ARRIVES']=ARRIVES_
def arena(seed=13,mood='golden',n=14):
    C=chowk_set(mood,crowd=n,seed=seed,ring=True); Pw=mk(PAWA,0,2.0,180,'pawa'); As=mk(ASHRAF,0,6.0,0,'ashraf'); Dh=mk(DHOLI,3.6,1.2,40,'dholi'); dh=empty((0,0,0)); dhol_obj(dh,1.0)
    return C,Pw,As,Dh,dh
def dhol_play(Dh,dh,t,on=True):
    stand(Dh,t); blink(Dh,t); dh.parent=None; p=Dh['root'].location; dh.location=(p[0]+.0,p[1]-.0,1.15); dh.rotation_euler=(0,0,Dh['root'].rotation_euler[2])
    g=abs(math.sin(t*12)) if on else 0; Dh['arm'][1].rotation_euler=(R(-60-30*g),0,R(20)); Dh['arm'][-1].rotation_euler=(R(-60-30*abs(math.sin(t*12+1.5))*on),0,R(-20)); face(Dh,mouth='grin' if on else 'flat')
def CROWD_():
    C,Pw,As,Dh,dh=arena(14); As['root'].scale=(0,0,0)
    def upd(t):
        for i,H in enumerate(C):
            k=ease(tl(t,.05*i,.05*i+.8)); stand(H,t); blink(H,t); H['root'].location[2]=0; H['root'].scale=(1,1,1) if k>0 else (0,0,0)
            face(H,mouth='O',brow=.05)
        stand(Pw,t); blink(Pw,t); face(Pw,mouth='frown',brow=-.04,brow_r=-14); dhol_play(Dh,dh,t,False)
        q=ease(t/DUR); camset(LV((0,-6.5,7.5),(0,-5.8,6.0),q),(0,3.5,.6),24,16)
    return dict(upd=upd)
SHOTS['CROWD']=CROWD_
def MUSIC_():
    C,Pw,As,Dh,dh=arena(15); As['root'].scale=(0,0,0)
    def upd(t):
        crowd_idle(C,t,cheer=.5); dhol_play(Dh,dh,t,True); stand(Pw,t); blink(Pw,t)
        q=ease(t/DUR); camset(LV((5.6,-1.6,1.7),(5.3,-1.3,1.7),q),(3.6,1.2,1.4),30,8)
    return dict(upd=upd)
SHOTS['MUSIC']=MUSIC_
def WALKS_():
    C,Pw,As,Dh,dh=arena(16)
    for i in range(8): puff((random.Random(i).uniform(-1,1),7.0,.05),.2+i*.15,.3,5,M('#C8A878',.9),.5,1.0,seed=i)
    def upd(t):
        crowd_idle(C,t,look=hp(As)); dhol_play(Dh,dh,t,True); stand(Pw,t); blink(Pw,t)
        walk_path(As,[(0,8.2),(0,5.2)],t*.6,0,DUR*.6,step=.55); blink(As,t); As['root'].rotation_euler[2]=0; face(As,mouth='flat',brow=-.04,brow_r=-12)
        As['arm'][1].rotation_euler=(R(-15),0,R(-35)); As['arm'][-1].rotation_euler=(R(-15),0,R(35))
        q=ease(t/DUR); camset(LV((2.6,1.0,3.4),(2.3,1.5,3.1),q),hp(As,-.2),26,16)
    return dict(upd=upd)
SHOTS['WALKS']=WALKS_
def faceoff(seed):
    C,Pw,As,Dh,dh=arena(seed); As['root'].location=(0,5.2,0); Pw['root'].location=(0,2.9,0); return C,Pw,As,Dh,dh
def fo_idle(C,Pw,As,Dh,dh,t):
    crowd_idle(C,t,look=(0,4,1.8)); dhol_play(Dh,dh,t,False); stand(Pw,t); blink(Pw,t); stand(As,t); blink(As,t); As['root'].location=(0,5.2,0); Pw['root'].location=(0,2.9,0); As['root'].rotation_euler[2]=0; Pw['root'].rotation_euler[2]=R(180)
def FAISLA_():
    C,Pw,As,Dh,dh=faceoff(17)
    def upd(t):
        fo_idle(C,Pw,As,Dh,dh,t); Pw['root'].rotation_euler[2]=R(150); talk(Pw,t,37.36,38.9,shapes=('O','o','O','flat')); face(Pw,brow=-.05,brow_r=-18); g=math.sin(t*6)
        arm_to(Pw,1,hp(As),tl(t,.2,.45),base=(0,0,0)); Pw['arm'][-1].rotation_euler=(R(-80),R(40),R(-40))
        q=ease(t/DUR); camset(LV((1.0,4.2,1.95),(.95,4.0,1.96),q),hp(Pw,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['FAISLA']=FAISLA_
def KAUN_():
    C,Pw,As,Dh,dh=faceoff(18)
    def upd(t):
        fo_idle(C,Pw,As,Dh,dh,t); As['root'].rotation_euler[2]=R(-25); talk(As,t,39.09,40.8); face(As,brow=-.02,brow_r=-8); As['arm'][1].rotation_euler=(R(-15),0,R(-35)); As['arm'][-1].rotation_euler=(R(-15),0,R(35))
        As['head'].rotation_euler=(R(4),0,R(6*math.sin(t*1.5)))
        q=ease(t/DUR); camset(LV((-1.0,2.9,2.15),(-.95,3.1,2.16),q),hp(As,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['KAUN']=KAUN_
def PAWA_():
    C,Pw,As,Dh,dh=faceoff(19)
    def upd(t):
        fo_idle(C,Pw,As,Dh,dh,t); Pw['root'].rotation_euler[2]=R(150); talk(Pw,t,40.95,42.4); face(Pw,brow=-.04,brow_r=-12); k=tl(t,.1,.4)
        Pw['arm'][1].rotation_euler=(R(-45*k),0,R(-55*k)); Pw['arm'][-1].rotation_euler=(R(-25),0,R(-40)); Pw['root'].location[2]=0
        q=ease(t/DUR); camset(LV((1.2,4.6,1.6),(1.0,4.4,1.7),q),hp(Pw,-.08),36,2.8)
    return dict(upd=upd)
SHOTS['PAWA']=PAWA_
def SMILES_():
    C,Pw,As,Dh,dh=faceoff(20)
    def upd(t):
        fo_idle(C,Pw,As,Dh,dh,t); As['root'].rotation_euler[2]=R(-20); k=tl(t,.3,1.0); face(As,mouth='flat' if k<.5 else 'smirk',brow=-.02); As['head'].rotation_euler[0]=R(-6*k)
        q=ease(t/DUR); camset(LV((-.8,3.1,2.2),(-.7,3.3,2.2),q),hp(As,-.03),50,2.8)
    return dict(upd=upd)
SHOTS['SMILES']=SMILES_
def TAWA_():
    C,Pw,As,Dh,dh=faceoff(21)
    for i in range(6): sparkles((random.Random(i).uniform(-3,3),random.Random(i+9).uniform(1,7),2.5),.5,.5,1.5,6,.05,i,.4)
    def upd(t):
        crowd_idle(C,t,cheer=tl(t,.6,1.0)); dhol_play(Dh,dh,t,t>.6); stand(Pw,t); blink(Pw,t); stand(As,t); blink(As,t); As['root'].location=(0,5.2,0); Pw['root'].location=(0,2.9,0); Pw['root'].rotation_euler[2]=R(180)
        As['root'].rotation_euler[2]=R(-15); talk(As,t,44.05,45.5,rest='grin'); face(As,brow=-.02); k=tl(t,.2,.5); As['arm'][1].rotation_euler=(R(-25*k),0,R(-50*k)); As['arm'][-1].rotation_euler=(R(-160*k),0,R(-10))
        face(Pw,mouth='O',brow=.06,eyes=1.3)
        q=ease(t/DUR); camset(LV((1.7,.8,2.5),(1.5,1.1,2.45),q),(0,5.2,2.1),28,16)
    return dict(upd=upd)
SHOTS['TAWA']=TAWA_

# ================================================================ SCENE 4 — selfie first
def PREP_():
    C,Pw,As,Dh,dh=faceoff(22)
    def upd(t):
        fo_idle(C,Pw,As,Dh,dh,t); k=tl(t,.1,.5); g=math.sin(t*10)
        Pw['arm'][1].rotation_euler=(R(-95*k),R(-30*k),R(-15*k+5*g)); Pw['arm'][-1].rotation_euler=(R(-95*k),R(30*k),R(15*k-5*g)); Pw['root'].location[2]=.06*abs(math.sin(t*8))*k; face(Pw,mouth='frown',brow=-.05,brow_r=-18)
        for q_ in (1,-1): Pw['leg'][q_].rotation_euler[0]=R(15*q_*k)
        face(As,mouth='smirk')
        q=ease(t/DUR); camset(LV((4.2,4.0,1.6),(3.8,4.0,1.65),q),(0,4.0,1.5),26,8)
    return dict(upd=upd)
SHOTS['PREP']=PREP_
def PHONE_():
    C,Pw,As,Dh,dh=faceoff(23); ph=phone(As,1,1.6)
    def upd(t):
        fo_idle(C,Pw,As,Dh,dh,t); k=ease(tl(t,.2,.8)); ph.scale=(1,1,1) if t>.15 else (0,0,0); As['arm'][1].rotation_euler=(R(-100*k),0,R(-10*k)); face(As,mouth='grin'); As['root'].rotation_euler[2]=R(-15)
        Pw['arm'][1].rotation_euler=(R(-95),R(-30),R(-15)); Pw['arm'][-1].rotation_euler=(R(-95),R(30),R(15)); face(Pw,mouth='o',brow=.05)
        q=ease(t/DUR); camset(LV((-1.6,3.4,1.5),(-1.4,3.6,1.55),q),(0,5.1,2.0),30,4)
    return dict(upd=upd)
SHOTS['PHONE']=PHONE_
def SELFIE_():
    C,Pw,As,Dh,dh=faceoff(24); ph=phone(As,1,1.6)
    def upd(t):
        fo_idle(C,Pw,As,Dh,dh,t); As['root'].rotation_euler[2]=R(150); talk(As,t,49.48,52.4,rest='grin'); face(As,brow=.02); arm_to(As,1,(.5,3.6,2.6),1,base=(0,0,0)); As['arm'][-1].rotation_euler=(R(-60),0,R(-20))
        As['root'].rotation_euler[2]=R(-20); face(Pw,mouth='O',brow=.06,eyes=1.25); Pw['arm'][1].rotation_euler=(R(-40),0,R(-10))
        q=ease(t/DUR); camset(LV((.7,3.2,2.3),(.65,3.4,2.3),q),hp(As,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['SELFIE']=SELFIE_
def RUSH_():
    C,Pw,As,Dh,dh=faceoff(25); ph=phone(As,1,1.6); targets=[(-1.3+.65*(i%5),6.0+.55*(i//5)) for i in range(len(C))]
    def upd(t):
        stand(As,t); blink(As,t); As['root'].location=(0,5.2,0); As['root'].rotation_euler[2]=0; As['arm'][1].rotation_euler=(R(-165),0,R(-8)); face(As,mouth='grin',brow=.03)
        stand(Pw,t); blink(Pw,t); Pw['root'].location=(L(0,1.4,ease(tl(t,.5,1.2))),2.9,0); Pw['root'].rotation_euler=(0,R(-14*tl(t,.5,.9)),R(180)); face(Pw,mouth='O',brow=.06)
        dhol_play(Dh,dh,t,True)
        for i,H in enumerate(C):
            if not hasattr(H,'p0'): pass
            p0=C_P0[i]; k=ease(tl(t,.05*(i%6),.9+.05*(i%6))); x=L(p0[0],targets[i][0],k); y=L(p0[1],targets[i][1],k)
            H['root'].location=(x,y,0); walk(H,t*1.2+i,step=.55*(1-k)+.0) if k<1 else stand(H,t); H['root'].rotation_euler[2]=R(face_dir(0-x,8-y)) if k<.9 else 0
            blink(H,t); face(H,mouth='grin',brow=.05); H['arm'][1].rotation_euler=(R(-150*k),0,R(15))
        q=ease(t/DUR); camset(LV((0,-1.8,2.6),(0,-1.4,2.5),q),(0,5.0,1.6),24,16)
    C_P0=[tuple(H['root'].location[:2]) for H in C]
    return dict(upd=upd)
SHOTS['RUSH']=RUSH_
def PUSHED_():
    C,Pw,As,Dh,dh=faceoff(26); ph=phone(As,1,1.6); targets=[(-1.3+.65*(i%5),5.6+.5*(i//5)) for i in range(len(C))]
    def upd(t):
        stand(As,t); blink(As,t); As['root'].location=(0,5.2,0); As['arm'][1].rotation_euler=(R(-165),0,R(-8)); face(As,mouth='grin')
        for i,H in enumerate(C): stand(H,t+i); blink(H,t); H['root'].location=(targets[i][0],targets[i][1],0); H['root'].rotation_euler[2]=0; face(H,mouth='grin'); H['arm'][1].rotation_euler=(R(-150),0,R(15))
        k=ease(tl(t,.2,1.4)); stand(Pw,t); blink(Pw,t); Pw['root'].location=(L(.4,3.2,k),L(4.4,4.0,k),0); Pw['root'].rotation_euler=(0,R(-22*math.sin(pi*tl(t,.2,1.4))),R(-90)); face(Pw,mouth='O',brow=.06,eyes=1.3)
        Pw['arm'][1].rotation_euler=(R(-120),0,R(30)); Pw['arm'][-1].rotation_euler=(R(-140),0,R(-30))
        camset((0,-.4,2.2),(0,5.4,2.0),30,16)
    return dict(upd=upd)
SHOTS['PUSHED']=PUSHED_
def FINAL_():
    C,Pw,As,Dh,dh=faceoff(27); ph=phone(As,1,1.6); targets=[(-1.3+.65*(i%5),5.6+.5*(i//5)) for i in range(len(C))]
    L_=[]
    for i,(s_,tt) in enumerate((('LAHORE DA PAWA.',.15),('ASHRAF TAWA.',.75),('NO COMPETITION.',1.35))):
        e=empty((0,3.2,4.0-i*.55)); obox((0,.06,0),(len(s_)*.085+.2,.03,.17),M('#1B1F33',.6),.08,e); text(s_,(0,0,0),(0,-1,0),.23,M('#FFF3B0',.4,emit=2.2),ex=.02,parent=e); e.scale=(0,0,0); L_.append((e,tt))
    def upd(t):
        stand(As,t); blink(As,t); As['root'].location=(0,5.2,0); As['arm'][1].rotation_euler=(R(-165),0,R(-8)); face(As,mouth='grin')
        for i,H in enumerate(C): stand(H,t+i); blink(H,t); H['root'].location=(targets[i][0],targets[i][1],0); H['root'].rotation_euler[2]=0; face(H,mouth='grin'); H['arm'][1].rotation_euler=(R(-150),0,R(15))
        stand(Pw,t); blink(Pw,t); Pw['root'].location=(3.4,3.9,0); Pw['root'].rotation_euler=(0,0,R(-40)); face(Pw,mouth='frown',brow=.06,brow_r=14); Pw['arm'][1].rotation_euler=(R(-20),0,R(-30))
        for e,tt in L_: k=pop(t-tt) if t>=tt else 0; e.scale=(k,k,k)
        q=ease(t/DUR); camset(LV((0,-1.0,2.3),(0,-.6,2.3),q),(.3,5.0,2.3),26,16)
    return dict(upd=upd)
SHOTS['FINAL']=FINAL_
W_=json.load(open(LH+'/audio/words.json'))
