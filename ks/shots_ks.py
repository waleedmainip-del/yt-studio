# Shots for "The Karachi Survivor". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=62.6
SEQ=[('OPEN', 0.0), ('COURSE', 1.07), ('TUESDAY', 3.79), ('MEET', 6.34), ('WAKE', 7.55), ('MSG', 11.02), ('LOOKOUT', 12.84), ('BAS', 15.69), ('LEAVES', 17.98), ('CALL', 19.27), ('OYE', 21.4), ('RASTE', 22.74), ('MAP', 24.12), ('NOTMOVED', 25.89), ('SHOP', 27.44), ('KYA', 29.25), ('COLD', 30.88), ('THANDI', 31.93), ('STARE', 33.05), ('MILTI', 35.37), ('POWER', 37.77), ('SHOUT', 40.05), ('GADGETS', 41.62), ('TAYYAR', 46.25), ('NASA', 48.35), ('RINGS', 50.62), ('LAHORE', 52.19), ('KAISA', 53.76), ('DARK', 55.41), ('ACHA', 57.33)]
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
def powerbank(e,s=1.0): obox((0,-.06,.08),(.05*s,.02*s,.09*s),M('#22242B',.4),.01,e); obox((0,-.083,.12),(.03*s,.003,.004),M('#35C85A',.3,emit=4),0,e)
def torch(e,s=1.0):
    ocyl((0,-.06,.12),.035*s,.24*s,M('#C9CED8',.3,metal=.8),e,rot=(0,0,0),seg=10); ocyl((0,-.06,.25*s),.05*s,.05*s,M('#C9CED8',.3,metal=.8),e,rot=(0,0,0),seg=12)
    lens=ocyl((0,-.06,.28*s),.045*s,.01,M('#FFF6D8',.2,emit=8),e,rot=(0,0,0),seg=12); return lens
def minifan(e,s=1.0):
    ocyl((0,-.06,.05),.02*s,.12*s,M('#F4F1EA',.5),e,rot=(0,0,0),seg=8); g=empty((0,-.06,.17*s),e); ocyl((0,0,0),.11*s,.02,M('#4DB0E8',.4,alpha=.6),g,rot=(R(90),0,0),seg=18)
    bl=empty((0,-.01,0),g)
    for a in range(4): obox((math.cos(a*pi/2)*.05*s,0,math.sin(a*pi/2)*.05*s),(.045*s,.004,.02*s),M('#F4F1EA',.5),.004,bl,rot=(0,-a*pi/2,0))
    return bl
def umbrella(e,s=1.0,col='#2B58C9'):
    ocyl((0,-.06,.6*s),.015,1.2*s,M('#3A3D44',.5,metal=.4),e,rot=(0,0,0),seg=6); c=empty((0,-.06,1.2*s),e)
    for a in range(8): obox((math.cos(a*pi/4)*.35*s,math.sin(a*pi/4)*.35*s,-.05*s),(.38*s,.16*s,.008),M(col if a%2 else '#F4F1EA',.6),.0,c,rot=(0,R(18),a*pi/4))
    return c

# ================================================================ sets
def street_set(dark=False,n_rain=260,rc=(0,0),seed=1):
    street(); cornershop(); B.done('street'); water()
    S,w,rp,bg=setup_render('storm',res=PCT,samples=SAMPLES,shadow_dist=50)
    glamp((SHOPX,6.6,2.9),380,(1,.95,.88),.6); glamp((-12,3.5,7.5),250,(1,.8,.55),.4); glamp((14,-3.5,7.5),250,(1,.8,.55),.4)
    if dark: grid(0); S.data.energy*=.35; bg.inputs[1].default_value*=.35
    rain((rc[0],rc[1],0),n_rain,(14,10),9,seed); ripples((rc[0],rc[1]),22,(12,7))
    return S,bg
def room_set():
    flat_room(); B.done('room'); setup_interior('day',room=(0,0,3.2),res=PCT,samples=SAMPLES,shadow_dist=15)
    bpy.context.scene.objects[0]; point((1.8,-.6,2.4),70,(.8,.85,1.0),1.0,False)
    rain((6,.8,0),120,(4,6),7,3); fan=ceiling_fan((0,0,2.8)); return fan
def phone_set(kind):
    ui_world(); D=phone_ui(kind); return D
def ui_cam(t,z=-200,d=7.2,dz=0.0,lens=50): camset((0,-d,z+dz),(0,0,z+dz),lens,22)
def wade(H,t,step=.5,lift=.12): walk(H,t*1.1,step=step,lift=lift,arm=18)
SY=4.3   # sidewalk line in front of the shop

# ================================================================ HOOK
def OPEN_():
    street_set(rc=(-2,0)); Dn=mk(DANIYAL,-2.5,-.6,90,'dan'); um=in_hand(Dn,1,lambda e: umbrella(e,1.3)); bus=minibus((-14,1.8,0),0)
    def upd(t):
        x=-3.4+.55*t; Dn['root'].location=(x,-.6,0); Dn['root'].rotation_euler[2]=R(90); wade(Dn,t); blink(Dn,t); Dn['arm'][1].rotation_euler=(R(-95),0,R(10)); face(Dn,mouth='flat',brow=-.02)
        bus.location=(-14+4.5*t,1.8,0); bus.rotation_euler[1]=R(1.2*math.sin(t*3))
        q=ease(t/DUR); camset(LV((3.0,-3.2,6.0),(1.5,-3.1,2.2),q),LV((-3,3,3.5),(-2.5,0,1.3),q),22,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def COURSE_():
    street_set(rc=(0,0),seed=2); Dn=mk(DANIYAL,-.2,-.6,90,'dan'); um=in_hand(Dn,1,lambda e: umbrella(e,1.3)); bus=minibus((-9,1.9,0),0); ts=1.0
    for i in range(14): puff((-1.0+.12*i,1.0,.4),ts+.03*i,.28,5,M('#8FA8B0',.4,alpha=.7),.8,1.0,drift=(0,-2.5,1.2),seed=i)
    def upd(t):
        bus.location=(-9+7.5*t,1.9,0); stand(Dn,t); blink(Dn,t); Dn['root'].location=(-.2,-.6,0); k=tl(t,ts,ts+.25)
        Dn['root'].rotation_euler=(R(-12*k),0,R(90-60*k)); Dn['arm'][1].rotation_euler=(R(-95-40*k),0,R(10+30*k)); face(Dn,mouth='O' if k>.3 else 'flat',brow=.05*k,eyes=1+.3*k)
        q=ease(t/DUR); camset(LV((3.2,-4.2,1.6),(3.0,-3.8,1.65),q),(-.5,0,1.4),26,16)
    return dict(upd=upd)
SHOTS['COURSE']=COURSE_
def TUESDAY_():
    street_set(rc=(0,0),seed=3); Dn=mk(DANIYAL,-.2,-.6,40,'dan'); um=in_hand(Dn,1,lambda e: umbrella(e,1.3)); tt=5.4-T0
    e=empty((-.2,-.6,3.6)); obox((0,.05,0),(.6,.04,.7),M('#FFFFFF',.5,emit=.6),.08,e); obox((0,0,.5),(.6,.05,.2),M('#C8372D',.5,emit=.6),.05,e); text('TUESDAY',(0,-.06,.48),(0,-1,0),.17,M('#FFFFFF',.4,emit=2),ex=.01,parent=e)
    text('NORMAL',(0,-.06,-.05),(0,-1,0),.2,M('#16171C',.5),ex=.01,parent=e); text('DAY',(0,-.06,-.35),(0,-1,0),.2,M('#16171C',.5),ex=.01,parent=e); e.scale=(0,0,0)
    def ce(o,t): k=pop(t-tt) if t>=tt else 0; o.scale=(k,k,k); face_cam(o); o.rotation_euler[1]=R(6*math.sin(t*3))
    fx.add(e,ce)
    def upd(t):
        stand(Dn,t); blink(Dn,t); Dn['arm'][1].rotation_euler=(R(-95),0,R(10)); face(Dn,mouth='flat',brow=.03); Dn['root'].location[2]=0; Dn['head'].rotation_euler[0]=R(-15*tl(t,tt,tt+.4))
        q=ease(t/DUR); camset(LV((.6,-4.4,1.7),(.5,-4.0,2.0),q),(-.2,-.6,2.3),28,8)
    return dict(upd=upd)
SHOTS['TUESDAY']=TUESDAY_

# ================================================================ SCENE 1 — the flat
def bed_dan(t,Dn,stretch=0.0):
    sit(Dn,1,.68,legs=85); blink(Dn,t); Dn['root'].rotation_euler=(0,0,R(0))
def MEET_():
    fan=room_set(); Dn=mk(DANI_HOME,-1.4,.7,0,'dan'); label('DANIYAL',(-1.4,.7,2.85),.5,col='#1F5A5A',bg='#DFF5F0')
    def upd(t):
        bed_dan(t,Dn); fan.rotation_euler[2]=t*9; k=math.sin(pi*tl(t,.1,1.1)); arms(Dn,-170*k,0,15*k,-170*k,0,-15*k); face(Dn,mouth='O' if k>.4 else 'flat',eyes=.6 if k>.4 else 1.0); Dn['head'].rotation_euler[0]=R(-12*k)
        q=ease(t/DUR); camset(LV((1.2,-2.4,1.5),(1.0,-2.0,1.55),q),(-1.2,.8,1.3),26,8)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def WAKE_():
    fan=room_set(); Dn=mk(DANI_HOME,-1.4,.7,0,'dan'); ph=phone(Dn,1,1.3)
    def upd(t):
        bed_dan(t,Dn); fan.rotation_euler[2]=t*9; k=tl(t,.3,.9); hold_phone(Dn,1,k); Dn['head'].rotation_euler[0]=R(18*k); face(Dn,mouth='flat',brow=.02,eyes=.85); Dn['arm'][-1].rotation_euler=(R(-20),0,R(25))
        ph.scale=(1,1,1) if t>.25 else (0,0,0)
        q=ease(t/DUR); camset(LV((-.2,-1.4,1.6),(-.4,-1.1,1.62),q),hp(Dn,-.25),35,4)
    return dict(upd=upd)
SHOTS['WAKE']=WAKE_
def MSG_():
    D=phone_set('rain'); nb=D['nb']
    def upd(t):
        k=pop(t-.15) if t>.15 else 0; nb.scale=(k,k,k); ui_cam(t,d=L(7.8,7.0,ease(t/DUR)))
    return dict(upd=upd)
SHOTS['MSG']=MSG_
def LOOKOUT_():
    fan=room_set(); Dn=mk(DANI_HOME,2.6,.8,-90,'dan')
    def upd(t):
        stand(Dn,t); blink(Dn,t); fan.rotation_euler[2]=t*9; Dn['root'].rotation_euler[2]=R(90); k=tl(t,.2,.6); Dn['arm'][1].rotation_euler=(R(-60*k),0,R(10)); Dn['arm'][-1].rotation_euler=(R(-60*k),0,R(-10)); face(Dn,mouth='flat',brow=.04)
        q=ease(t/DUR); camset(LV((.4,-.6,2.0),(.7,-.4,2.0),q),(3.4,.9,1.8),30,4)
    return dict(upd=upd)
SHOTS['LOOKOUT']=LOOKOUT_
def BAS_():
    fan=room_set(); Dn=mk(DANI_HOME,2.6,.8,-90,'dan')
    def upd(t):
        stand(Dn,t); blink(Dn,t); fan.rotation_euler[2]=t*9; Dn['root'].rotation_euler[2]=R(lerp_angle(90,-60,tl(t,.0,.6))); talk(Dn,t,15.69,17.6); face(Dn,brow=-.03,brow_r=-12)
        k=tl(t,.7,1.1); Dn['arm'][1].rotation_euler=(R(-25*k),0,R(-45*k)); Dn['arm'][-1].rotation_euler=(R(-25*k),0,R(45*k))
        q=ease(t/DUR); camset(LV((1.6,-.9,1.95),(1.7,-.6,1.97),q),hp(Dn,-.03),42,2.8)
    return dict(upd=upd)
SHOTS['BAS']=BAS_

# ================================================================ SCENE 2 — "raste vich"
def LEAVES_():
    street_set(rc=(-16,2),seed=4); Dn=mk(DANIYAL,-16,4.6,0,'dan',z=.2); um=in_hand(Dn,1,lambda e: umbrella(e,1.3)); ts=.9
    for i in range(10): puff((-16,3.2,.35),ts+.05*i,.25,5,M('#8FA8B0',.4,alpha=.7),.6,.8,seed=i)
    def upd(t):
        if t<ts: walk_path(Dn,[(-16,4.6),(-16,3.6)],t,0,ts,z=.2,step=.5)
        else:
            k=ease(tl(t,ts,ts+.3)); Dn['root'].location=(-16,3.6-.6*k,.2-.2*k); stand(Dn,t); face(Dn,mouth='O' if t<ts+.6 else 'frown',brow=.05)
        blink(Dn,t); Dn['arm'][1].rotation_euler=(R(-95),0,R(10))
        q=ease(t/DUR); camset(LV((-13.6,-1.8,1.4),(-13.9,-1.4,1.3),q),(-16,3.4,.9),28,8)
    return dict(upd=upd)
SHOTS['LEAVES']=LEAVES_
def ham_shop(t,Hm,phone_up=True):
    stand(Hm,t); blink(Hm,t); Hm['root'].location=(SHOPX-1.9,SY,.2)
def CALL_():
    street_set(rc=(SHOPX,2),seed=5); Hm=mk(HAMMAD,SHOPX-1.9,SY,-20,'ham',z=.2); ph=phone(Hm,1,1.3)
    def upd(t):
        ham_shop(t,Hm); k=tl(t,.6,1.1); hold_phone(Hm,1,1-k)
        if k>0: ear(Hm,1,k)
        Hm['arm'][-1].rotation_euler=(R(-40),0,R(-50)); face(Hm,mouth='frown',brow=-.03,brow_r=-10); Hm['head'].rotation_euler[0]=R(12*(1-k))
        q=ease(t/DUR); camset(LV((SHOPX-.2,-1.0,1.6),(SHOPX-.5,-.6,1.65),q),(SHOPX-1.9,SY+.3,1.65),30,8)
    return dict(upd=upd)
SHOTS['CALL']=CALL_
def OYE_():
    street_set(rc=(SHOPX,2),seed=6); Hm=mk(HAMMAD,SHOPX-1.9,SY,-20,'ham',z=.2); ph=phone(Hm,1,1.3)
    def upd(t):
        ham_shop(t,Hm); ear(Hm,1,1); talk(Hm,t,21.4,22.3,shapes=('O','o','O','flat')); face(Hm,brow=-.04,brow_r=-16); g=math.sin(t*9); Hm['arm'][-1].rotation_euler=(R(-80-25*g),0,R(-20))
        q=ease(t/DUR); camset(LV((SHOPX-1.3,SY-2.1,1.85),(SHOPX-1.4,SY-1.8,1.86),q),hp(Hm,-.05),45,2.8)
    return dict(upd=upd)
SHOTS['OYE']=OYE_
def RASTE_():
    street_set(rc=(-8,0),seed=7); Dn=mk(DANIYAL,-8,-.5,30,'dan'); ph=phone(Dn,-1,1.3); um=in_hand(Dn,1,lambda e: umbrella(e,1.3))
    def upd(t):
        stand(Dn,t); blink(Dn,t); Dn['root'].location=(-8,-.5,0); ear(Dn,-1,1); Dn['arm'][1].rotation_euler=(R(-95),0,R(10)); talk(Dn,t,22.74,23.95); face(Dn,brow=.02)
        q=ease(t/DUR); camset(LV((-6.6,-2.9,1.6),(-6.8,-2.5,1.65),q),hp(Dn,-.15),35,4)
    return dict(upd=upd)
SHOTS['RASTE']=RASTE_
def MAP_():
    D=phone_set('map'); pin=D['pin']
    def upd(t):
        k=1+.25*math.sin(t*6); pin.scale=(k,1,k); ui_cam(t,d=L(7.6,6.6,ease(t/DUR)),dz=.0)
    return dict(upd=upd)
SHOTS['MAP']=MAP_
def NOTMOVED_():
    street_set(rc=(-8,0),seed=8); Dn=mk(DANIYAL,-8,-.5,30,'dan'); ph=phone(Dn,-1,1.3); um=in_hand(Dn,1,lambda e: umbrella(e,1.3)); duck=empty((-6.8,-1.6,.32))
    obox((0,0,.08),(.14,.1,.08),M('#F2C14E',.5),.05,duck); obox((.13,0,.2),(.08,.07,.07),M('#F2C14E',.5),.04,duck); obox((.22,0,.19),(.04,.03,.02),M('#F28A1A',.5),.01,duck)
    def upd(t):
        stand(Dn,t); blink(Dn,t); Dn['root'].location=(-8,-.5,0); Dn['arm'][1].rotation_euler=(R(-95),0,R(10)); Dn['arm'][-1].rotation_euler=(R(-20),0,R(-20)); face(Dn,mouth='flat',brow=.02); Dn['head'].rotation_euler[2]=R(20*math.sin(t*.9))
        duck.location=(-6.8+.4*t,-1.6,.3+.02*math.sin(t*5))
        camset((-8,-3.3,3.7),(-8,.2,.9),24,16)
    return dict(upd=upd)
SHOTS['NOTMOVED']=NOTMOVED_

# ================================================================ SCENE 3 — the shop
def shop_cast(dark=False,rc=(SHOPX,2),seed=9):
    S,bg=street_set(dark,rc=rc,seed=seed); Kp=mk(KEEPER,SHOPX,6.25,0,'keeper',z=0); Dn=mk(DANIYAL,SHOPX+.2,SY,180,'dan',z=.2); Hm=mk(HAMMAD,SHOPX-1.9,SY,-40,'ham',z=.2)
    return S,bg,Kp,Dn,Hm
def keeper_idle(Kp,t,bored=True):
    stand(Kp,t); blink(Kp,t); Kp['arm'][-1].rotation_euler=(R(-75),0,R(-25)); Kp['arm'][1].rotation_euler=(R(-75),0,R(25)); Kp['root'].rotation_euler[0]=R(4)
    if bored: face(Kp,mouth='flat',brow=-.02,eyes=.75)
def SHOP_():
    S,bg,Kp,Dn,Hm=shop_cast(); um=in_hand(Dn,1,lambda e: umbrella(e,1.3)); drips=[]
    def upd(t):
        keeper_idle(Kp,t); ham_shop(t,Hm); Hm['root'].rotation_euler[2]=R(-40); face(Hm,mouth='smirk')
        if t<1.3: walk_path(Dn,[(SHOPX+4.5,SY-1.2),(SHOPX+.9,SY-.3),(SHOPX+.2,SY)],t,-.2,1.3,z=.2,step=.5)
        else: stand(Dn,t); Dn['root'].location=(SHOPX+.2,SY,.2); Dn['root'].rotation_euler[2]=R(180)
        blink(Dn,t); Dn['arm'][1].rotation_euler=(R(-95),0,R(10)); face(Dn,mouth='frown',brow=.04)
        q=ease(t/DUR); camset(LV((SHOPX+3.2,-1.6,1.7),(SHOPX+2.6,-1.2,1.75),q),(SHOPX,5.6,1.6),24,16)
    return dict(upd=upd)
SHOTS['SHOP']=SHOP_
def KYA_():
    S,bg,Kp,Dn,Hm=shop_cast(seed=10)
    def upd(t):
        keeper_idle(Kp,t,False); talk(Kp,t,29.25,30.6); face(Kp,brow=-.02,eyes=.75); Kp['head'].rotation_euler=(R(4),0,R(6*math.sin(t*1.5)))
        q=ease(t/DUR); camset(LV((SHOPX+.5,SY+.4,1.95),(SHOPX+.45,SY+.6,1.96),q),hp(Kp,-.05),42,2.8)
    return dict(upd=upd)
SHOTS['KYA']=KYA_
def dan_cu(Dn,t,cam):
    stand(Dn,t); blink(Dn,t); Dn['root'].location=(SHOPX+.2,SY,.2); Dn['root'].rotation_euler[2]=R(180)
def COLD_():
    S,bg,Kp,Dn,Hm=shop_cast(seed=11); um=in_hand(Dn,1,lambda e: umbrella(e,1.3))
    def upd(t):
        keeper_idle(Kp,t); dan_cu(Dn,t,None); Dn['arm'][1].rotation_euler=(R(-50),0,R(15)); talk(Dn,t,30.88,31.65); face(Dn,brow=.03,eyes=.85); Dn['head'].rotation_euler[0]=R(6)
        q=ease(t/DUR); camset(LV((SHOPX+.9,6.7,2.15),(SHOPX+.85,6.5,2.14),q),hp(Dn,-.05),45,2.8)
    return dict(upd=upd)
SHOTS['COLD']=COLD_
def THANDI_():
    S,bg,Kp,Dn,Hm=shop_cast(seed=12)
    def upd(t):
        keeper_idle(Kp,t,False); talk(Kp,t,31.93,32.8); face(Kp,brow=-.02,eyes=.75); k=tl(t,.1,.4); arm_to(Kp,1,(SHOPX+1.7,7.0,1.3),k,base=(-75,0,25)); Kp['head'].rotation_euler[2]=R(-25*k)
        q=ease(t/DUR); camset(LV((SHOPX-.9,SY+.1,1.95),(SHOPX-.8,SY+.35,1.96),q),(SHOPX+.6,6.5,1.7),30,4)
    return dict(upd=upd)
SHOTS['THANDI']=THANDI_
def STARE_():
    S,bg,Kp,Dn,Hm=shop_cast(seed=13); um=in_hand(Dn,1,lambda e: umbrella(e,1.3))
    def upd(t):
        keeper_idle(Kp,t); stand(Dn,t); Dn['root'].location=(SHOPX+.2,SY,.2); Dn['root'].rotation_euler[2]=R(lerp_angle(180,10,tl(t,.1,.6))); blink(Dn,t,force=False)
        Dn['arm'][1].rotation_euler=(R(-95),0,R(10)); face(Dn,mouth='frown',brow=.06,brow_r=16,eyes=1.1); Dn['head'].rotation_euler[0]=R(-4)
        q=ease(t/DUR); camset(LV((SHOPX+.2,SY-2.4,2.0),(SHOPX+.2,SY-1.3,1.98),q),hp(Dn,-.03),45,2.8)
    return dict(upd=upd)
SHOTS['STARE']=STARE_
def MILTI_():
    S,bg,Kp,Dn,Hm=shop_cast(seed=14); um=in_hand(Dn,1,lambda e: umbrella(e,1.3))
    def upd(t):
        keeper_idle(Kp,t); stand(Dn,t); Dn['root'].location=(SHOPX+.2,SY,.2); Dn['root'].rotation_euler=(0,0,R(10)); blink(Dn,t); talk(Dn,t,35.37,37.6)
        face(Dn,brow=.06,brow_r=18); k=tl(t,.4,.9); Dn['arm'][1].rotation_euler=(R(-95+10*k),0,R(10)); Dn['arm'][-1].rotation_euler=(R(-70*k),0,R(-30*k)); Dn['head'].rotation_euler[0]=R(-10*k)
        camset((SHOPX+2.2,-.6,.6),(SHOPX+.2,SY,2.3),24,16)
    return dict(upd=upd)
SHOTS['MILTI']=MILTI_

# ================================================================ SCENE 4 — load-shedding
def POWER_():
    S,bg,Kp,Dn,Hm=shop_cast(seed=15); e0=S.data.energy; b0=bg.inputs[1].default_value; to=.55
    def upd(t):
        keeper_idle(Kp,t); dan_cu(Dn,t,None); ham_shop(t,Hm)
        if t<to: k=1
        elif t<to+.35: k=1 if int((t-to)*20)%2 else .1
        else: k=0
        grid(k); S.data.energy=e0*(.35+.65*k); bg.inputs[1].default_value=b0*(.35+.65*k)
        o=t>to+.3; face(Kp,mouth='O' if o else 'flat',brow=.05 if o else 0); face(Hm,mouth='O' if o else 'smile',brow=.05 if o else 0); face(Dn,mouth='flat')
        for H in (Kp,Hm): H['head'].rotation_euler[0]=R(-20*tl(t,to+.2,to+.5))
        q=ease(t/DUR); camset(LV((SHOPX+3.5,-2.6,2.6),(SHOPX+3.0,-2.0,2.3),q),(SHOPX-.4,5.4,2.0),24,16)
    return dict(upd=upd)
SHOTS['POWER']=POWER_
def SHOUT_():
    S,bg,Kp,Dn,Hm=shop_cast(True,seed=16); N1=mk(NEIGH1,SHOPX-6.4,4.6,10,'n1',z=3.0); N2=mk(NEIGH2,SHOPX+5.6,4.6,-10,'n2',z=3.0)
    def upd(t):
        keeper_idle(Kp,t,False); dan_cu(Dn,t,None); ham_shop(t,Hm); face(Dn,mouth='flat')
        for i,H in enumerate((Kp,Hm,N1,N2)):
            if H in (N1,N2): stand(H,t); blink(H,t); H['root'].location[2]=3.0
            mouth_talk(H,t,0+.15*i,DUR,shapes=('O','o','O','flat'),rate=9); face(H,brow=-.04,brow_r=-16); g=math.sin(t*10+i)
            H['arm'][1].rotation_euler=(R(-140+30*g),0,R(20)); H['arm'][-1].rotation_euler=(R(-120-30*g),0,R(-20))
        q=ease(t/DUR); camset(LV((SHOPX,-3.4,2.4),(SHOPX,-3.0,2.5),q),(SHOPX,5.0,2.6),22,16)
    return dict(upd=upd)
SHOTS['SHOUT']=SHOUT_
TT=[W_i for W_i in ()]
def gadget_times(): return [W_[i]['s']-T0 for i in (108,111,114)]
def GADGETS_():
    S,bg,Kp,Dn,Hm=shop_cast(True,seed=17); tg=gadget_times()
    pb=in_hand(Dn,-1,lambda e: powerbank(e,1.8)); tc=in_hand(Dn,1,lambda e: torch(e,1.8)); fn_=minifan(empty((SHOPX+.9,5.55,1.15)),2.2)
    tl_=point((SHOPX+.6,SY-1.4,1.5),0,(1,.95,.85),.4,False)
    fan_root=fn_.parent.parent
    def upd(t):
        keeper_idle(Kp,t,False); face(Kp,mouth='O',brow=.05); ham_shop(t,Hm); face(Hm,mouth='O',brow=.05); look_at(Hm,hp(Dn),.7); look_at(Kp,hp(Dn),.7)
        dan_cu(Dn,t,None); Dn['root'].rotation_euler[2]=R(35); face(Dn,mouth='smirk',brow=-.02)
        k0=tl(t,tg[0]-.3,tg[0]); pb.scale=(1,1,1) if t>tg[0]-.35 else (0,0,0); Dn['arm'][-1].rotation_euler=(R(-75*k0),0,R(-10))
        k1=tl(t,tg[1]-.3,tg[1]); tc.scale=(1,1,1) if t>tg[1]-.35 else (0,0,0); Dn['arm'][1].rotation_euler=(R(-100*k1),0,R(-25*k1)); tl_.data.energy=45*k1
        k2=pop(t-tg[2]) if t>tg[2] else 0; fan_root.scale=(k2,k2,k2); fn_.rotation_euler[1]=t*25
        q=ease(t/DUR); camset(LV((SHOPX+2.4,1.6,1.9),(SHOPX+2.1,2.0,1.9),q),(SHOPX+.3,4.8,1.6),28,8)
    return dict(upd=upd)
SHOTS['GADGETS']=GADGETS_
def dark_gear(Dn):
    tc=in_hand(Dn,1,lambda e: torch(e,1.8)); point((SHOPX+.6,SY-1.4,1.5),45,(1,.95,.85),.4,False); point((SHOPX+.2,1.0,.6),120,(1,.95,.85),1.0,False); return tc
def TAYYAR_():
    S,bg,Kp,Dn,Hm=shop_cast(True,seed=18); tc=dark_gear(Dn); point((SHOPX-2.6,SY-1.6,2.2),30,(1,.95,.85),.6,False)
    def upd(t):
        keeper_idle(Kp,t); dan_cu(Dn,t,None); Dn['root'].rotation_euler[2]=R(60); Dn['arm'][1].rotation_euler=(R(-100),0,R(-25))
        ham_shop(t,Hm); Hm['root'].rotation_euler[2]=R(-20); talk(Hm,t,46.25,48.0); face(Hm,brow=.06,eyes=1.25); k=tl(t,.1,.4); arm_to(Hm,1,hp(Dn,-.5),k,base=(-20,0,0))
        q=ease(t/DUR); camset(LV((SHOPX-2.6,SY-2.2,2.1),(SHOPX-2.5,SY-1.9,2.1),q),hp(Hm,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['TAYYAR']=TAYYAR_
def NASA_():
    S,bg,Kp,Dn,Hm=shop_cast(True,seed=19); tc=dark_gear(Dn); fn_=minifan(in_hand(Dn,-1,lambda e: None),2.0)
    def upd(t):
        keeper_idle(Kp,t); ham_shop(t,Hm); dan_cu(Dn,t,None); Dn['root'].rotation_euler[2]=R(15); talk(Dn,t,48.35,50.1); face(Dn,brow=-.03,brow_r=-10)
        Dn['arm'][1].rotation_euler=(R(-100),0,R(-25)); Dn['arm'][-1].rotation_euler=(R(-115),0,R(-35)); fn_.rotation_euler[1]=t*25; Dn['head'].rotation_euler=(R(-6),0,R(6*math.sin(t*4)))
        q=ease(t/DUR); camset(LV((SHOPX+.5,SY-1.9,1.95),(SHOPX+.45,SY-1.6,1.96),q),hp(Dn,-.08),42,2.8)
    return dict(upd=upd)
SHOTS['NASA']=NASA_
# ================================================================ FINAL
def RINGS_():
    S,bg,Kp,Dn,Hm=shop_cast(True,seed=20); tc=dark_gear(Dn); ph=phone(Dn,-1,1.3)
    def upd(t):
        keeper_idle(Kp,t); ham_shop(t,Hm); dan_cu(Dn,t,None); Dn['root'].rotation_euler[2]=R(15); Dn['arm'][1].rotation_euler=(R(-55),0,R(-15))
        k=tl(t,.2,.6); hold_phone(Dn,-1,k); ph.location[0]=.012*math.sin(t*80); Dn['head'].rotation_euler[0]=R(15*k); face(Dn,mouth='o',brow=.04)
        q=ease(t/DUR); camset(LV((SHOPX+1.5,SY-1.9,2.0),(SHOPX+1.3,SY-1.6,2.0),q),hp(Dn,-.15),35,4)
    return dict(upd=upd)
SHOTS['RINGS']=RINGS_
def LAHORE_():
    D=phone_set('call')
    def upd(t):
        for i,r_ in enumerate(D['ring']): q=((t*1.2)+i*.5)%1; k=1+q*.8; r_.scale=(k,1,k)
        ui_cam(t,d=L(7.4,6.8,ease(t/DUR)))
    return dict(upd=upd)
SHOTS['LAHORE']=LAHORE_
def KAISA_():
    S,bg,Kp,Dn,Hm=shop_cast(True,seed=21); tc=dark_gear(Dn); ph=phone(Dn,-1,1.3); bubble('Bhai, Karachi kaisa hai?',(SHOPX+.9,SY-.3,2.6),.1,size=.16,col='#1F3A2A',bg='#DFF5E1')
    def upd(t):
        keeper_idle(Kp,t); ham_shop(t,Hm); dan_cu(Dn,t,None); Dn['root'].rotation_euler[2]=R(15); Dn['arm'][1].rotation_euler=(R(-100),0,R(-25)); ear(Dn,-1,1); face(Dn,mouth='flat',brow=.02)
        q=ease(t/DUR); camset(LV((SHOPX+1.9,SY-2.4,1.8),(SHOPX+1.7,SY-2.0,1.82),q),hp(Dn,-.1),35,4)
    return dict(upd=upd)
SHOTS['KAISA']=KAISA_
def DARK_():
    S,bg,Kp,Dn,Hm=shop_cast(True,seed=22,rc=(SHOPX,0)); tc=dark_gear(Dn); ph=phone(Dn,-1,1.3)
    def upd(t):
        keeper_idle(Kp,t); ham_shop(t,Hm); stand(Dn,t); blink(Dn,t); Dn['root'].location=(SHOPX+.2,SY,.2); Dn['root'].rotation_euler[2]=R(lerp_angle(15,0,tl(t,0,.5))); ear(Dn,-1,1); Dn['arm'][1].rotation_euler=(R(-100),0,R(-10))
        face(Dn,mouth='flat',brow=.03,eyes=.9)
        q=ease(t/DUR); camset(LV((SHOPX+1.1,SY+.9,2.8),(SHOPX+1.0,SY+.7,2.8),q),(SHOPX-1.5,-3,1.0),24,16)
    return dict(upd=upd)
SHOTS['DARK']=DARK_
def ACHA_():
    S,bg,Kp,Dn,Hm=shop_cast(True,seed=23); tc=dark_gear(Dn); ph=phone(Dn,-1,1.3)
    def upd(t):
        keeper_idle(Kp,t); ham_shop(t,Hm); dan_cu(Dn,t,None); Dn['root'].rotation_euler[2]=R(5); ear(Dn,-1,1); Dn['arm'][1].rotation_euler=(R(-100),0,R(-10)); talk(Dn,t,57.33,61.3); face(Dn,brow=.0,eyes=.85)
        Dn['head'].rotation_euler=(R(-4),0,R(4*math.sin(t*1.2)))
        q=ease(t/DUR); camset(LV((SHOPX+.25,SY-1.2,1.95),(SHOPX+.25,SY-2.6,2.2),q),hp(Dn,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['ACHA']=ACHA_
W_=json.load(open(LH+'/audio/words.json'))
