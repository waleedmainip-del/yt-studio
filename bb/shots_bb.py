# Shots for "The Islamabadi Burger Bachha". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=137.2
SEQ=[('OPEN', 0.0), ('IDENT', 3.42), ('TITLE', 6.11), ('MEET', 7.12), ('THREE', 9.54), ('COFFEE', 13.9), ('SNEAK', 16.08), ('SAMOSA', 17.6), ('CALL', 20.47), ('OYEB', 22.55), ('READY', 25.02), ('NASA', 26.69), ('ARRIVE', 30.19), ('STEPOUT', 31.94), ('STARE', 35.97), ('VIP', 37.53), ('PLEASE', 41.64), ('NAAM', 44.32), ('ANNOY', 47.69), ('NORMAL', 49.16), ('PINDI', 51.6), ('RIDE', 54.55), ('STALL', 58.15), ('MENU', 60.62), ('OAT', 62.24), ('KEEPER', 63.9), ('FALL', 65.69), ('WIFI', 67.95), ('ORDER', 71.76), ('FLOOK', 73.33), ('WAH', 74.69), ('STRANGERS', 77.83), ('GETUP', 81.3), ('BETWEEN', 83.05), ('RELAX', 85.27), ('SLAUGH', 87.83), ('PHONE', 89.33), ('DAD', 91.56), ('FREEZE', 94.47), ('CONN', 95.96), ('SMILE', 98.62), ('ISB', 99.87), ('HOUSE', 101.97), ('BOYSARR', 105.05), ('FEAST', 106.58), ('BITE', 109.19), ('KAMAAL', 111.68), ('PROUD', 115.62), ('MOMIN', 119.62), ('MOM', 120.97), ('TRAIL', 122.9), ('LOOKO', 124.65), ('NIKLA', 126.25), ('LAUGH', 129.62), ('CARD', 131.69)]
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

# ================================================================ sets
def view_set(mood='afternoon'):
    viewpoint(); B.done('view'); setup_world(mood,shadow=70)
    Bi=mk(BILAL,-2.5,3.5,12,'bilal'); Sh=mk(SHERRY,-1.2,3.9,4,'sherry'); Fa=mk(FAIZAN,.1,3.5,-14,'faizan'); Ah=mk(AHMED,2.4,3.6,-8,'ahmed'); cp=cup(Ah,1)
    return Bi,Sh,Fa,Ah
def sector_set(mood='morning',skip=None,door=False):
    SKIPX[0]=skip; sector(skip); kiosk(-13.5,6.9); samosa_cart(13.5,5.3)
    if door: cx,w,gx=house_pick(); villa_door(gx)
    B.done('sector'); setup_world(mood,shadow=70)
def adda_set(mood='afternoon',truck=True,bikes=True,n=4,seed=3):
    adda(); B.done('adda'); setup_world(mood,shadow=70)
    if truck: truck_art(-9.5,8.2,8)
    charpai(1.5,8.6,-6)
    if bikes: motorbike((6.9,7.9,0),-70,'#C8372D'); motorbike((-3.6,7.3,0),-110,'#1F3A5A')
    return walkers(n,seed,-30,30,(15.3,16.0))
def boys3(p=((3.2,6.2),(4.4,6.6),(5.6,6.2)),rz=(0,0,0)):
    return mk(BILAL,p[0][0],p[0][1],rz[0],'bilal'),mk(SHERRY,p[1][0],p[1][1],rz[1],'sherry'),mk(FAIZAN,p[2][0],p[2][1],rz[2],'faizan')
JX,JY=-1.0,2.4
def arrive_set(seed=4):
    W=adda_set(seed=seed); J=jeep((JX,JY,0),0); Bi,Sh,Fa=boys3(); Ah=mk(AHMED,-1.55,0.0,0,'ahmed'); cp=cup(Ah,1); return W,J,Bi,Sh,Fa,Ah
SP=dict(bi=(-4.0,3.7,60),sh=(-3.1,4.6,15),ah=(-2.0,4.6,-15),fa=(-1.2,3.7,-60))
def stall_set(ah_seated=False,thugs=False):
    stall(); B.done('stall'); setup_world('dusk',shadow=50)
    point((0,6.4,2.7),700,(1,.74,.42),.3,False); point((-2.6,2.6,3.3),650,(1,.82,.6),.5,False); point((2.6,5.5,3.4),350,(1,.8,.55),.4,False)
    S={}; S['ch']={k:plastic_chair(v[0],v[1],v[2],'#C8372D') for k,v in SP.items()}
    S['kp']=mk(KEEPER,0,8.6,0,'keeper'); S['spat']=in_hand(S['kp'],1,lambda e:(obox((0,-.05,.2),(.012,.012,.2),M('#C9CED8',.3,metal=.9),0,e),obox((0,-.05,.44),(.06,.01,.07),M('#C9CED8',.3,metal=.9),.01,e)))
    S['bi']=mk(BILAL,SP['bi'][0],SP['bi'][1],SP['bi'][2],'bilal'); S['sh']=mk(SHERRY,SP['sh'][0],SP['sh'][1],SP['sh'][2],'sherry'); S['fa']=mk(FAIZAN,SP['fa'][0],SP['fa'][1],SP['fa'][2],'faizan')
    S['ah']=mk(AHMED,SP['ah'][0],SP['ah'][1],SP['ah'][2],'ahmed') if ah_seated else mk(AHMED,2.45,7.9,-10,'ahmed')
    if thugs: S['th']=[mk(THUG1,1.3,3.2,-90,'thug1'),mk(THUG2,.7,4.1,-90,'thug2'),mk(THUG3,2.1,4.3,-90,'thug3')]
    return S
def stall_idle(S,t,seated=('bi','sh','fa'),kp=True):
    for k in seated: seat(S[k],t+dseed(k),.6); S[k]['root'].rotation_euler[2]=R(SP[k][2])
    if kp:
        K=S['kp']; stand(K,t); blink(K,t); K['arm'][1].rotation_euler=(R(-58-10*math.sin(t*5)),0,R(8)); face(K,mouth='flat',brow=-.02)
def dining_set(prints=False):
    dining(); B.done('dining'); setup_interior('day',room=(0,0,3.6),res=PCT,samples=SAMPLES,shadow_dist=20); point((0,-1.2,2.6),260,(1,.92,.8),.4,False)
    for x in (-1.6,0,1.6): dining_chair(x,1.32,0)
    dining_chair(3.2,0,-90); dining_chair(-3.2,0,90)
    S=dict(bi=mk(BILAL,-1.6,1.32,0,'bilal'),fa=mk(FAIZAN,0,1.32,0,'faizan'),sh=mk(SHERRY,1.6,1.32,0,'sherry'),ah=mk(AHMED2,3.2,0,-90,'ahmed'),mo=mk(MOTHER,-3.5,.3,90,'mother'))
    if prints:
        r=random.Random(8); pts=[(5.2,-.3),(4.2,.6),(3.4,1.9),(2.4,2.3),(1.2,2.3),(0,2.3),(-1.2,2.3),(-1.9,2.0)]
        for i in range(len(pts)-1):
            a=Vector((pts[i][0],pts[i][1],0)); b=Vector((pts[i+1][0],pts[i+1][1],0)); ang=math.atan2(b.y-a.y,b.x-a.x)
            for j in range(3):
                p=a.lerp(b,(j+.3)/3); s_=1 if (i*3+j)%2 else -1; q=p+Vector((-math.sin(ang),math.cos(ang),0))*.14*s_
                obox((q.x,q.y,.004),(.13,.055,.004),M(r.choice(['#5A3E24','#6B4A2E','#4A3220']),.95),.02,rot=(0,0,ang+r.uniform(-.2,.2))); obox((q.x+r.uniform(-.2,.2),q.y+r.uniform(-.2,.2),.003),(.04,.03,.003),M('#6B4A2E',.95),.01)
    return S
def dine_idle(S,t,who=('bi','fa','sh','ah')):
    for k in who:
        seat(S[k],t+dseed(k),.62); S[k]['root'].rotation_euler[2]=R(-90 if k=='ah' else 0)
    if 'mo' in S: stand(S['mo'],t); blink(S['mo'],t)

# ================================================================ HOOK — the viewpoint
def OPEN_():
    Bi,Sh,Fa,Ah=view_set(); label('PINDI',(-1.2,3.7,3.15),1.2,size=.3); label('ISLAMABAD',(2.4,3.6,2.95),2.2,col='#1F5A3A',bg='#E2F4E0',size=.25)
    def upd(t):
        idle_all((Bi,Sh,Fa,Ah),t); shk(Ah,0); hold(Ah,1); Ah['head'].rotation_euler[2]=R(-14)
        gest(Bi,t,1); gest(Sh,t,-1,f=6); gest(Fa,t,1,f=8); mouth_talk(Bi,t,0,1.2,rest='grin'); mouth_talk(Sh,t,1.0,2.2,rest='smile'); mouth_talk(Fa,t,2.0,3.4,rest='grin')
        look_at(Bi,hp(Sh),.7); look_at(Fa,hp(Sh),.7); look_at(Sh,hp(Fa if t>1.4 else Bi),.6); face(Ah,mouth='smile')
        q=ease(t/DUR); camset(LV((-2.4,-1.4,1.6),(.6,-1.6,1.6),q),(0,3.6,1.55),26,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def IDENT_():
    Bi,Sh,Fa,Ah=view_set()
    def upd(t):
        idle_all((Bi,Sh,Fa,Ah),t); shk(Ah,0); k=math.sin(pi*tl(t,.45,1.9)); Ah['arm'][1].rotation_euler=(R(-70-48*k),0,R(18*k)); Ah['head'].rotation_euler=(R(-10*k),0,0); face(Ah,mouth='o' if k>.6 else 'smirk',brow=.02)
        Ah['arm'][-1].rotation_euler=(R(-25),0,R(-30)); q=ease(t/DUR); camset(LV((3.2,.3,1.95),(2.9,.9,2.0),q),hp(Ah,.05),50,2.8)
    return dict(upd=upd)
SHOTS['IDENT']=IDENT_
def TITLE_():
    Bi,Sh,Fa,Ah=view_set(); bg=burger_obj(None,(2.4,3.6,6),3.4)
    def upd(t):
        idle_all((Bi,Sh,Fa,Ah),t); shk(Ah,0); hold(Ah,1); z=fall(t,5.2,2.52); bg.location=(2.4,3.6,z); bg.rotation_euler[2]=t*1.5; landed=t>.42
        for i,H in enumerate((Bi,Sh,Fa)): arm_to(H,1 if i<2 else -1,hp(Ah,.2),1.0,base=(0,0,0)); look_at(H,hp(Ah),.9); laugh(H,t+i)
        Ah['head'].rotation_euler=(R(-14 if landed else 0),0,0); face(Ah,mouth='flat' if landed else 'smile',brow=-.03 if landed else 0,brow_r=-10 if landed else 0)
        camset((.3,-3.4,1.7),(.2,3.6,1.95),26,16)
    return dict(upd=upd)
SHOTS['TITLE']=TITLE_

# ================================================================ SCENE 1 — the friend group
def MEET_():
    sector_set(); Ah=mk(AHMED,-5,4.9,90,'ahmed',z=.14); cp=cup(Ah,1)
    def upd(t):
        walk_path(Ah,[(-5.2,4.9),(-1.2,4.9)],t,-.4,DUR+.5,z=.14,step=.5); blink(Ah,t); shk(Ah,0); hold(Ah,1); face(Ah,mouth='smile'); x=Ah['root'].location[0]; Ah['head'].rotation_euler[2]=R(-22)
        camset((x+3.6,.4,1.45),(x+.3,4.9,1.6),30,8)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def THREE_():
    W=adda_set(seed=5); Bi,Sh,Fa=boys3(((-1.6,6.4),(0,6.8),(1.6,6.4)),(8,0,-8)); tn=(11.58-T0,12.33-T0,12.97-T0)
    label('BILAL',(-1.6,6.4,3.2),tn[0]); label('SHERRY',(0,6.8,3.3),tn[1],col='#0E6E7A',bg='#E0F6F8'); label('FAIZAN',(1.6,6.4,2.75),tn[2],col='#7A4A0E',bg='#FFF0C8')
    def upd(t):
        upd_walkers(W,t+4); idle_all((Bi,Sh,Fa),t)
        k=tl(t,tn[0],tn[0]+.25); headtouch(Bi,1,k,dx=.3,dy=-.75,dz=-.25); Bi['arm'][-1].rotation_euler=(R(-20*k),0,R(55*k)); face(Bi,mouth='smirk',brow=-.02,brow_r=-8)
        k=tl(t,tn[1],tn[1]+.25); Sh['arm'][1].rotation_euler=(R(-150*k),0,R(22*k)); Sh['head'].rotation_euler[1]=R(8*k); face(Sh,mouth='grin' if k>.5 else 'smile')
        k=tl(t,tn[2],tn[2]+.25); g=math.sin(t*11); Fa['arm'][1].rotation_euler=(R(-160*k),0,R((20+14*g)*k)); Fa['arm'][-1].rotation_euler=(R(-160*k),0,R(-(20+14*g)*k)); face(Fa,mouth='grin' if k>.5 else 'smile',brow=.04*k)
        q=ease(t/DUR); camset(LV((.6,-1.6,1.6),(.1,-.2,1.65),q),(0,6.6,1.65),26,16)
    return dict(upd=upd)
SHOTS['THREE']=THREE_
def COFFEE_():
    sector_set(); Ah=mk(AHMED,-13.2,5.4,18,'ahmed',z=.14); cp=cup(Ah,1,1.6)
    tg=empty((.16,-.06,.1),cp); obox((0,0,-.12),(.13,.006,.07),M('#F4F1EA',.6),.01,tg); text('Rs 1,250',(0,-.012,-.12),(0,-1,0),.05,M('#C8372D',.5),ex=.002,parent=tg); obox((0,0,-.03),(.004,.004,.04),M('#16171C',.5),0,tg)
    sparkles((-13.0,5.0,2.2),.5,.5,2.0,16,.05,4,.4)
    def upd(t):
        stand(Ah,t); blink(Ah,t); shk(Ah,0); k=ease(tl(t,.15,.7)); Ah['arm'][1].rotation_euler=(R(-70-50*k),0,R(14*k)); Ah['head'].rotation_euler=(R(-8*k),0,R(14*k)); face(Ah,mouth='grin' if k>.5 else 'smile',brow=.04)
        Ah['arm'][-1].rotation_euler=(R(-20),0,R(-40)); tg.rotation_euler=(0,R(8*math.sin(t*5)),0)
        q=ease(t/DUR); camset(LV((-11.5,2.0,1.8),(-11.8,2.5,1.85),q),(-13.15,5.4,1.95),35,4.0)
    return dict(upd=upd)
SHOTS['COFFEE']=COFFEE_
def SNEAK_():
    sector_set(); Ah=mk(AHMED,-6,4.9,90,'ahmed',z=.14); sparkles((-5.0,4.6,.3),.7,.1,1.5,22,.04,6,.3)
    B.cyl((-4.3,4.9,.145),.42,.012,M('#5A4630',.3,spec=.9),seg=14); B.done('puddle')
    def upd(t):
        walk_path(Ah,[(-6.0,4.9),(-4.9,4.75),(-4.3,4.25),(-3.6,4.5)],t,-.3,DUR+.4,z=.14,step=.42); x=Ah['root'].location[0]
        camset((x+1.6,3.95,.5),(x+.15,Ah['root'].location[1],.12),30,4.0)
    return dict(upd=upd)
SHOTS['SNEAK']=SNEAK_
def SAMOSA_():
    sector_set(); Ah=mk(AHMED,11.5,5.0,62,'ahmed',z=.14); Vn=mk(VENDOR,15.25,5.4,-78,'vendor',z=.14)
    bubble('One samosa, please.',(11.6,4.9,2.95),.35,size=.15,col='#1F3A2A',bg='#E2F4E0'); bubble('Extra crispy?',(11.6,4.9,2.6),1.15,size=.15,col='#1F3A2A',bg='#E2F4E0'); bubble('???',(15.2,5.3,2.75),1.7,size=.3,col='#7A1F1F',bg='#FFF3B0')
    def upd(t):
        idle_all((Ah,Vn),t); shk(Ah,0); k=tl(t,.2,.5); Ah['arm'][1].rotation_euler=(R(-115*k),0,R(10)); mouth_talk(Ah,t,.3,2.2,rest='smile'); look_at(Ah,hp(Vn),.8); face(Ah,brow=.03)
        k2=tl(t,1.5,1.9); headtouch(Vn,1,k2,dx=.4,dy=.1,dz=.7); look_at(Vn,hp(Ah),.8); face(Vn,mouth='flat',brow=.05,brow_r=12); Vn['head'].rotation_euler[1]=R(10*k2)
        q=ease(t/DUR); camset(LV((13.2,-.6,1.6),(13.1,0,1.62),q),(13.35,5.2,1.6),24,16)
    return dict(upd=upd)
SHOTS['SAMOSA']=SAMOSA_
def call_set(seed=6):
    W=adda_set(seed=seed); Bi=mk(BILAL,1.2,8.2,0,'bilal'); Fa=mk(FAIZAN,2.25,8.2,-12,'faizan'); Sh=mk(SHERRY,.25,9.55,18,'sherry'); ph=phone(Bi,1); return W,Bi,Sh,Fa,ph
def call_idle(Bi,Sh,Fa,t):
    seat(Bi,t,.6); seat(Fa,t+1,.6); Fa['root'].rotation_euler[2]=R(-12); stand(Sh,t); blink(Sh,t); Sh['root'].rotation_euler[0]=R(10)
def CALL_():
    W,Bi,Sh,Fa,ph=call_set()
    def upd(t):
        upd_walkers(W,t+7); call_idle(Bi,Sh,Fa,t); k=tl(t,.9,1.4); hold_phone(Bi,1,1-k);
        if k>0: ear(Bi,1,k)
        Bi['head'].rotation_euler[0]=R(16*(1-k)); face(Bi,mouth='smirk'); look_at(Sh,hp(Bi),.8); look_at(Fa,hp(Bi),.8); face(Sh,mouth='grin'); face(Fa,mouth='smile')
        q=ease(t/DUR); camset(LV((1.6,3.4,1.6),(1.5,4.0,1.6),q),(1.3,8.3,1.6),30,8)
    return dict(upd=upd)
SHOTS['CALL']=CALL_
def OYEB_():
    W,Bi,Sh,Fa,ph=call_set(7)
    def upd(t):
        upd_walkers(W,t+9); call_idle(Bi,Sh,Fa,t); ear(Bi,1,1); talk(Bi,t,22.55,24.7); face(Bi,brow=.05,eyes=1.15); g=math.sin(t*9); Bi['arm'][-1].rotation_euler=(R(-75-20*g),0,R(-20)); Bi['head'].rotation_euler=(R(-6),R(5*g),0)
        laugh(Fa,t,.6); look_at(Sh,hp(Bi),.8); face(Sh,mouth='grin')
        q=ease(t/DUR); camset(LV((1.9,5.6,1.9),(1.7,5.9,1.95),q),hp(Bi,.02),45,2.8)
    return dict(upd=upd)
SHOTS['OYEB']=OYEB_
def READY_():
    closet(); B.done('closet'); setup_interior('day',room=(0,0,3.3),res=PCT,samples=SAMPLES); Ah=mk(AHMED,0,-.1,6,'ahmed'); ph=phone(Ah,-1)
    def upd(t):
        stand(Ah,t); blink(Ah,t); shk(Ah,0); ear(Ah,-1,1); g=math.sin(t*6); headtouch(Ah,1,1,dx=.35,dy=-.35+.15*g,dz=.8); talk(Ah,t,25.02,26.44); Ah['head'].rotation_euler=(0,R(6),R(10)); face(Ah,brow=.02)
        q=ease(t/DUR); camset(LV((.7,-2.4,1.75),(.5,-2.2,1.78),q),(0,-.1,1.72),26,5.6)
    return dict(upd=upd)
SHOTS['READY']=READY_
def NASA_():
    W=adda_set(seed=8); Bi=mk(BILAL,1.2,8.2,0,'bilal'); Sh=mk(SHERRY,.5,6.9,6,'sherry'); Fa=mk(FAIZAN,1.75,7.2,-22,'faizan'); ph=phone(Sh,1); tn=28.55-T0
    rk=empty((-.7,7.4,2.0)); ocyl((0,0,0),.11,.5,M('#F4F1EA',.4),rk,rot=(0,0,0),seg=12); ocyl((0,0,.36),.11,.24,M('#C8372D',.4),rk,rot=(0,0,0),seg=12,r2=.01); oico((0,-.1,.08),.05,M('#2B9BE8',.3,emit=1),rk,sub=1)
    for a in range(3): obox((math.cos(a*2.1)*.13,math.sin(a*2.1)*.13,-.2),(.05,.012,.09),M('#C8372D',.4),.01,rk,rot=(0,0,a*2.1))
    for i in range(6): puff((-.7,7.4,2.0),tn+i*.07,.14,4,M('#F2A64A',.8),-.3,.5,seed=i)
    def upd(t):
        upd_walkers(W,t+12); seat(Bi,t,.6); stand(Sh,t); stand(Fa,t); blink(Sh,t); blink(Fa,t); hold_phone(Sh,1,1); Sh['arm'][1].rotation_euler[0]-=R(18); talk(Sh,t,26.69,30.1); face(Sh,brow=.05,brow_r=8)
        g=math.sin(t*8); Sh['arm'][-1].rotation_euler=(R(-80-25*g),0,R(-28)); Sh['head'].rotation_euler=(0,R(6*g),R(-6))
        laugh(Fa,t); headtouch(Bi,-1,tl(t,.4,.8),dx=.2,dy=-.75,dz=.25); laugh(Bi,t+1,.7)
        k=tl(t,tn,tn+.9); rk.scale=(1,1,1) if t>=tn-.15 else (0,0,0); rk.location=(-.7+.3*k,7.4,2.0+5.5*k*k); rk.rotation_euler[1]=R(8*k)
        q=ease(t/DUR); camset(LV((.9,3.7,1.95),(.8,4.1,2.0),q),(.75,7.0,2.15),35,4.0)
    return dict(upd=upd)
SHOTS['NASA']=NASA_

# ================================================================ SCENE 2 — the meetup
def ARRIVE_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(); hide(Ah['root'])
    def upd(t):
        upd_walkers(W,t+15); idle_all((Bi,Sh,Fa),t); x=JX-14*(1-ease_out(min(1,t/1.35))); drive(J,x,JY,0,x); J['root'].rotation_euler[1]=R(-2.5*math.sin(pi*min(1,max(0,(t-1.2)/.5))))
        for H in (Bi,Sh,Fa): facep(H,(x,JY)); look_at(H,(x,JY,1.6),.5)
        face(Bi,mouth='flat',brow=.04); face(Sh,mouth='o',brow=.05); face(Fa,mouth='O',brow=.05)
        camset((8.6,-2.6,1.5),(1.6,3.9,1.35),24,16)
    return dict(upd=upd)
SHOTS['ARRIVE']=ARRIVE_
def STEPOUT_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(5); sparkles((-1.5,.3,1.9),.8,1.9,3.9,26,.05,7,.5)
    def upd(t):
        upd_walkers(W,t+17); idle_all((Bi,Sh,Fa),t); drive(J,JX,JY,0,0); k=ease(tl(t,.2,.75)); J['hinge'].rotation_euler[2]=R(72*k)
        if t<.8: Ah['root'].scale=(0,0,0)
        else:
            Ah['root'].scale=(1,1,1); walk_path(Ah,[(-1.3,1.35),(-1.55,0.0)],t,.8,2.1,step=.5); blink(Ah,t); shk(Ah,1)
            if t>=2.1: stand(Ah,t); Ah['root'].rotation_euler[2]=R(lerp_angle(8,20,tl(t,2.1,2.5)))
            k2=tl(t,2.1,2.6); Ah['arm'][1].rotation_euler=(R(-70-35*k2),0,R(16*k2)); headtouch(Ah,-1,math.sin(pi*tl(t,2.5,3.6)),dx=.62,dy=-.7,dz=.1); face(Ah,mouth='smirk',brow=-.02)
        for H in (Bi,Sh,Fa): facep(H,(-1.5,.5))
        q=ease(tl(t,.6,DUR)); camset(LV((-3.3,-3.6,.55),(-2.9,-3.0,.7),q),(-1.45,.7,1.5),28,8)
    return dict(upd=upd)
SHOTS['STEPOUT']=STEPOUT_
def boys_face(Bi,Sh,Fa,p=(-1.5,.3)):
    for H in (Bi,Sh,Fa): facep(H,p)
def STARE_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(6)
    def upd(t):
        upd_walkers(W,t+21); idle_all((Bi,Sh,Fa),t); boys_face(Bi,Sh,Fa); k=tl(t,.15,.9)
        for i,H in enumerate((Bi,Sh,Fa)): H['head'].rotation_euler=(R(4),R((10+3*i)*k*(1 if i!=1 else -1)),0); face(H,mouth='O' if i else 'o',brow=.06,eyes=1.2)
        q=ease(t/DUR); camset(LV((.4,2.0,1.75),(.9,2.5,1.78),q),(4.35,6.4,1.85),38,5.6)
    return dict(upd=upd)
SHOTS['STARE']=STARE_
def VIP_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(7); Fa['root'].location=(3.0,4.7,0)
    def upd(t):
        upd_walkers(W,t+23); idle_all((Bi,Sh,Fa),t); boys_face(Bi,Sh,Fa); Fa['root'].location=(3.0,4.7,0); Fa['root'].rotation_euler[2]=R(-150+20*math.sin(t*1.5)) ; facep(Fa,(-1.5,.3),.55,cam=(.2,2.2))
        talk(Fa,t,37.53,41.4); face(Fa,brow=.06,eyes=1.1); g=math.sin(t*5); k=tl(t,1.2,1.6)
        Fa['arm'][1].rotation_euler=(R(-95-20*g),R(-40*k),R(20)); Fa['arm'][-1].rotation_euler=(R(-95+20*g),R(40*k),R(-20)); Fa['root'].location[2]=.06*abs(math.sin(t*6))
        s=tl(t,1.6,2.0); headtouch(Sh,1,s,dx=.55,dy=-.6,dz=.35); laugh(Sh,t,.6); Bi['root'].rotation_euler[0]=R(18*math.sin(pi*tl(t,1.8,3.2))); laugh(Bi,t+1,.5)
        q=ease(t/DUR); camset(LV((1.6,.3,1.45),(1.9,.7,1.5),q),(3.2,5.0,1.45),30,8)
    return dict(upd=upd)
SHOTS['VIP']=VIP_
def ahm_cu(Ah,t,cam,lens=50):
    stand(Ah,t); blink(Ah,t); facep(Ah,(4.4,6.4),.35,cam=cam); camset(cam,hp(Ah,.02),lens,2.8)
def PLEASE_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(8)
    def upd(t):
        upd_walkers(W,t+27); q=ease(t/DUR); ahm_cu(Ah,t,LV((1.3,.9,1.9),(1.1,.75,1.92),q)); shk(Ah,1); hold(Ah,1); talk(Ah,t,41.64,43.9); face(Ah,brow=.06,brow_r=14)
        g=math.sin(t*6); Ah['arm'][-1].rotation_euler=(R(-85-8*g),0,R(-12)); Ah['head'].rotation_euler=(R(4),0,R(6*math.sin(t*4)))
    return dict(upd=upd)
SHOTS['PLEASE']=PLEASE_
def NAAM_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(9)
    def upd(t):
        upd_walkers(W,t+30); idle_all((Bi,Sh,Fa),t); boys_face(Bi,Sh,Fa); facep(Bi,(-1.5,.3),.3,cam=(1.4,3.2)); talk(Bi,t,44.32,47.5,); face(Bi,brow=.05); arm_to(Bi,1,(-1.5,.3,1.7),tl(t,.9,1.2),base=(0,0,0))
        Bi['head'].rotation_euler[0]=R(-6+5*math.sin(t*12)); Bi['arm'][-1].rotation_euler=(R(-30),0,R(40)); laugh(Sh,t); laugh(Fa,t+2); Sh['root'].rotation_euler[0]=R(10*abs(math.sin(t*3)))
        q=ease(t/DUR); camset(LV((1.2,3.0,1.8),(1.5,3.4,1.85),q),hp(Bi,-.05),40,4.0)
    return dict(upd=upd)
SHOTS['NAAM']=NAAM_
def ANNOY_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(10)
    def upd(t):
        upd_walkers(W,t+33); ahm_cu(Ah,t,(.9,.55,1.85),55); k=tl(t,.1,.45); shk(Ah,1-k); hold(Ah,1); headtouch(Ah,-1,tl(t,.5,.9),dx=.05,dy=-.8,dz=.2); Ah['head'].rotation_euler=(R(14*tl(t,.5,.9)),0,0); face(Ah,mouth='frown',brow=-.03,brow_r=-14)
    return dict(upd=upd)
SHOTS['ANNOY']=ANNOY_
def NORMAL_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(11); cam=(6.4,.6,1.5)
    def upd(t):
        upd_walkers(W,t+35); idle_all((Bi,Sh,Fa,Ah),t); Ah['root'].location=(1.5,4.3,0); facep(Ah,(4.4,6.4),.35,cam=cam); shk(Ah,0); hold(Ah,1); talk(Ah,t,49.16,51.4); face(Ah,brow=-.02,brow_r=-10)
        g=math.sin(t*7); Ah['arm'][-1].rotation_euler=(R(-70-14*g),0,R(-30))
        for i,H in enumerate((Bi,Sh,Fa)): facep(H,(1.5,4.3),.4,cam=cam); look_at(H,hp(Ah),.6); face(H,mouth='grin',brow=.03)
        Sh['arm'][1].rotation_euler=(R(-25),0,R(-50)); Sh['arm'][-1].rotation_euler=(R(-25),0,R(50))
        q=ease(t/DUR); camset(LV(cam,(6.0,1.0,1.5),q),(3.3,5.4,1.5),26,16)
    return dict(upd=upd)
SHOTS['NORMAL']=NORMAL_
def PINDI_():
    W,J,Bi,Sh,Fa,Ah=arrive_set(12); hide(Ah['root']); hide(J['root']); tn=53.35-T0
    for i,x in enumerate((3.0,4.4,5.8)): puff((x,6.0,.1),tn+.05*i,.22,6,M('#C8B898',.9),.5,.9,seed=i)
    def upd(t):
        upd_walkers(W,t+38); idle_all((Bi,Sh,Fa),t); Sh['root'].location=(4.4,6.0,0)
        for H in (Bi,Sh,Fa): H['root'].rotation_euler[2]=0
        talk(Sh,t,51.6,54.3); face(Sh,brow=-.03,brow_r=-10); k=tl(t,tn,tn+.2); g=math.sin(t*6)
        Sh['arm'][1].rotation_euler=(R(-60-100*k),0,R(18+10*g*(1-k))); Sh['arm'][-1].rotation_euler=(R(-60-10*g),0,R(-18))
        Bi['arm'][1].rotation_euler=(R(-35-125*k),0,R(-48*(1-k)+14*k)); Bi['arm'][-1].rotation_euler=(R(-35),0,R(48)); face(Bi,mouth='grin' if k else 'smirk',brow=-.03,brow_r=-10)
        Fa['arm'][1].rotation_euler=(R(-160*k),0,R(16)); Fa['arm'][-1].rotation_euler=(R(-160*k),0,R(-16)); face(Fa,mouth='grin',brow=.03); Fa['root'].location[2]=.12*abs(math.sin((t-tn)*9))*k
        q=ease(t/DUR); camset(LV((4.6,1.9,.85),(4.45,2.5,.95),q),(4.4,6.2,1.95),26,16)
    return dict(upd=upd)
SHOTS['PINDI']=PINDI_

# ================================================================ SCENE 3 — the real test
def RIDE_():
    W=adda_set(seed=13,bikes=False); B1=motorbike((0,1.3,0),0,'#C8372D'); B2=motorbike((0,-1.1,0),0,'#1F3A5A'); R_=[]
    for Bk,(C1,n1),(C2,n2) in ((B1,(BILAL,'bilal'),(AHMED,'ahmed')),(B2,(SHERRY,'sherry'),(FAIZAN,'faizan'))):
        Bk['root'].scale=(1.25,1.25,1.25); Bk['r']*=1.25
        for C,n,lx in ((C1,n1,-.02),(C2,n2,-.58)):
            H=mk(C,0,0,0,n); H['root'].parent=Bk['root']; H['root'].location=(lx,0,.42); H['root'].rotation_euler=(0,0,R(90)); sit(H,1,.55,legs=70); H['z0']=0; R_.append(H)
    Bi,Ah,Sh,Fa=R_
    def upd(t):
        upd_walkers(W,t+40); x=-16+7.0*t; drive(B1,x,1.3,0,x); drive(B2,x-2.7,-1.1+.25*math.sin(t*2),0,x)
        for H in R_: blink(H,t); H['root'].rotation_euler=(0,R(2*math.sin(t*9+H['seed'])),R(90))
        arms(Bi,-66,0,6,-66,0,-6); arms(Sh,-66,0,6,-66,0,-6); face(Bi,mouth='grin',brow=-.02); face(Sh,mouth='grin'); shk(Ah,0)
        arms(Ah,-80,0,-14,-80,0,14); face(Ah,mouth='O',brow=.06,eyes=1.3); Ah['head'].rotation_euler=(R(6),0,R(8*math.sin(t*7)))
        g=math.sin(t*8); Fa['arm'][1].rotation_euler=(R(-165),0,R(20+12*g)); Fa['arm'][-1].rotation_euler=(R(-70),0,R(-10)); face(Fa,mouth='grin',brow=.04)
        camset((x+6.8,-3.6,1.3),(x-.9,.3,1.5),30,8)
    return dict(upd=upd)
SHOTS['RIDE']=RIDE_
def STALL_():
    S=stall_set()
    def upd(t):
        stall_idle(S,t); Ah=S['ah']; stand(Ah,t); blink(Ah,t); shk(Ah,0); look_at(Ah,(3.6,7.9,1.9),.8); headtouch(Ah,1,1,dx=.2,dy=-.8,dz=-.35)
        gest(S['bi'],t,1); mouth_talk(S['bi'],t,.3,1.6,rest='grin'); laugh(S['fa'],t,.5); face(S['sh'],mouth='smile'); look_at(S['sh'],hp(S['bi']),.6)
        q=ease(t/DUR); camset(LV((-1.2,-4.6,3.9),(-1.0,-3.9,1.8),q),LV((-.6,6.5,2.6),(-.6,5.6,1.5),q),24,16)
    return dict(upd=upd)
SHOTS['STALL']=STALL_
def MENU_():
    S=stall_set()
    def upd(t):
        stall_idle(S,t); Ah=S['ah']; stand(Ah,t); blink(Ah,t); shk(Ah,0); k=tl(t,.1,.5); look_at(Ah,(3.7,7.8,1.7+.3*math.sin(t*2.5)),.9*k); headtouch(Ah,1,1,dx=.2,dy=-.8,dz=-.35); face(Ah,mouth='flat',brow=.03,brow_r=8)
        q=ease(t/DUR); camset(LV((2.2,4.3,1.7),(2.4,4.8,1.72),q),(3.0,7.8,1.75),35,5.6)
    return dict(upd=upd)
SHOTS['MENU']=MENU_
def OAT_():
    S=stall_set()
    def upd(t):
        stall_idle(S,t); Ah=S['ah']; stand(Ah,t); blink(Ah,t); shk(Ah,0); cam=(.55,7.15,1.85); facep(Ah,(0,8.6),.5,cam=cam); talk(Ah,t,62.24,63.6); face(Ah,brow=.05)
        k=tl(t,.1,.4); Ah['arm'][1].rotation_euler=(R(-110*k),0,R(8)); Ah['head'].rotation_euler=(0,R(-6),0)
        camset(cam,hp(Ah,.02),50,2.8)
    return dict(upd=upd)
SHOTS['OAT']=OAT_
def KEEPER_():
    S=stall_set()
    def upd(t):
        stall_idle(S,t,kp=False); K=S['kp']; legs0(K); blink(K,t,force=(1.0<t<1.15)); K['arm'][1].rotation_euler=(R(-58),0,R(8)); K['head'].rotation_euler=(0,0,R(-8)); face(K,mouth='flat',brow=-.04,brow_r=-6,eyes=.8)
        q=ease(t/DUR); camset(LV((.5,5.0,1.8),(.35,5.9,1.82),q),hp(K,-.05),50,2.8)
    return dict(upd=upd)
SHOTS['KEEPER']=KEEPER_
def FALL_():
    S=stall_set(); Bi=S['bi']; ch=S['ch']['bi']
    def upd(t):
        stall_idle(S,t); q=tl(t,.25,.9); r_=tl(t,1.5,1.9); a=-34*(ease_out(q)-ease(r_))+(-4*math.sin(t*22) if .9<t<1.5 else 0)
        Bi['root'].rotation_euler[0]=R(a); ch.rotation_euler[0]=R(a); g=math.sin(t*20); w=1 if .3<t<1.6 else 0
        Bi['arm'][1].rotation_euler=(R(-120-40*g*w),0,R(30)); Bi['arm'][-1].rotation_euler=(R(-120+40*g*w),0,R(-30)); laugh(Bi,t); face(Bi,mouth='grin',brow=.06)
        for q_ in (1,-1): Bi['leg'][q_].rotation_euler[0]=-R(90+ (-a)*.9)
        laugh(S['fa'],t+1); laugh(S['sh'],t+2,.7)
        camset((-1.9,.3,1.25),(-3.7,3.8,1.35),32,5.6)
    return dict(upd=upd)
SHOTS['FALL']=FALL_
def WIFI_():
    S=stall_set(); Bi=S['bi']; tn=70.35-T0; wifi_icon((-3.3,3.9,2.95),tn)
    def upd(t):
        stall_idle(S,t); talk(Bi,t,67.95,71.3); face(Bi,brow=.05); headtouch(Bi,-1,1,dx=.55,dy=-.75,dz=-.3); k=tl(t,1.2,1.5); arm_to(Bi,1,(2.45,7.9,1.8),k,base=(-60,0,10)); look_at(Bi,(0,8.6,1.9),.7)
        laugh(S['fa'],t+1); laugh(S['sh'],t+2); S['sh']['arm'][1].rotation_euler=(R(-100+30*math.sin(t*14)),0,R(10))
        q=ease(t/DUR); camset(LV((-2.2,-.9,1.5),(-2.4,-.4,1.5),q),(-2.7,4.1,1.6),28,8)
    return dict(upd=upd)
SHOTS['WIFI']=WIFI_
def ORDER_():
    S=stall_set(True); Ah=S['ah']; bz=1.035; pl=empty((-2.25,4.05,bz)); ocyl((0,0,.01),.2,.02,M('#F8F6F0',.3,spec=.8),pl,rot=(0,0,0),seg=16); burger_obj(pl,(0,0,.02),1.5); sparkles((-2.25,4.05,1.3),.35,.45,1.4,14,.04,9,.3)
    def upd(t):
        stall_idle(S,t,('bi','sh','fa','ah')); shk(Ah,0); k=pop(t-.35); pl.scale=(k,k,k); c=tl(t,.6,.9); g=abs(math.sin(t*10))*c
        Ah['arm'][1].rotation_euler=(R(-75*c),0,R(-25*c-10*g)); Ah['arm'][-1].rotation_euler=(R(-75*c),0,R(25*c+10*g)); Ah['head'].rotation_euler[0]=R(12*c); face(Ah,mouth='grin' if c>.3 else 'smile',brow=.05,eyes=1.15)
        look_at(S['fa'],hp(Ah),.5); look_at(S['sh'],hp(Ah),.5); face(S['sh'],mouth='smirk'); face(S['fa'],mouth='flat'); face(S['bi'],mouth='grin')
        q=ease(t/DUR); camset(LV((-2.3,.9,1.6),(-2.25,1.3,1.6),q),(-2.1,4.4,1.5),38,4.0)
    return dict(upd=upd)
SHOTS['ORDER']=ORDER_
def eat_pose(Ah,t,bite=1.0):
    arms(Ah,-108*bite,0,-26,-108*bite,0,26); shk(Ah,0)
def FLOOK_():
    S=stall_set(True); Ah=S['ah']; Fa=S['fa']; bg=in_hand(Ah,1,lambda e: burger_obj(e,(-.12,-.1,.06),1.3))
    def upd(t):
        stall_idle(S,t,('bi','sh','fa','ah')); eat_pose(Ah,t); face(Ah,mouth='O'); k=ease(tl(t,.15,.9)); look_at(Fa,hp(Ah),k,maxyaw=75); face(Fa,mouth='flat',brow=-.03,brow_r=-8,eyes=.75)
        q=ease(t/DUR); camset(LV((-2.6,1.4,1.5),(-2.4,1.7,1.5),q),hp(Fa,-.02),50,2.8)
    return dict(upd=upd)
SHOTS['FLOOK']=FLOOK_
def WAH_():
    S=stall_set(True); Ah=S['ah']; Fa=S['fa']; bg=in_hand(Ah,1,lambda e: burger_obj(e,(-.12,-.1,.06),1.3))
    def upd(t):
        stall_idle(S,t,('bi','sh','fa','ah')); eat_pose(Ah,t); face(Ah,mouth='O',brow=.05,eyes=1.15); look_at(Ah,hp(Fa),.6); look_at(Fa,hp(Ah),.8,maxyaw=75); talk(Fa,t,74.69,77.2); face(Fa,brow=.04)
        c=tl(t,1.7,2.0); g=abs(math.sin(t*5))*c; Fa['arm'][1].rotation_euler=(R(-80*c),0,R(-22*c-12*g)); Fa['arm'][-1].rotation_euler=(R(-80*c),0,R(22*c+12*g)); laugh(S['bi'],t,.6); laugh(S['sh'],t+1,.6)
        q=ease(t/DUR); camset(LV((-3.3,1.6,1.6),(-3.2,1.9,1.6),q),(-1.7,4.1,1.45),32,5.6)
    return dict(upd=upd)
SHOTS['WAH']=WAH_

# ================================================================ SCENE 4 — the tables turn
TP=((.9,3.9),(1.7,3.0),(2.3,4.5))
def thug_idle(S,t,mood='angry'):
    for i,H in enumerate(S['th']):
        stand(H,t+i); blink(H,t+i); H['root'].location=(TP[i][0],TP[i][1],0); H['root'].rotation_euler[2]=R(-78+8*i)
        if mood=='angry': face(H,mouth='frown',brow=-.04,brow_r=-16)
WIDE=((-.8,-1.3,1.6),(-.8,3.6,1.45))
def STRANGERS_():
    S=stall_set(True,True); Ah=S['ah']; bg=in_hand(Ah,1,lambda e: burger_obj(e,(-.12,-.1,.06),1.3))
    def upd(t):
        stall_idle(S,t,('bi','sh','fa','ah')); eat_pose(Ah,t,.7); face(Ah,mouth='o',brow=.05)
        for i,H in enumerate(S['th']):
            if t<1.5+.1*i: walk_path(H,[(7.5+i*.8,TP[i][1]+.4),TP[i]],t,-.2,1.5+.1*i,step=.6); blink(H,t); face(H,mouth='frown',brow=-.04,brow_r=-16)
            else:
                stand(H,t+i); H['root'].rotation_euler[2]=R(-78+8*i); face(H,brow=-.04,brow_r=-16); mouth_talk(H,t,1.6+i*.5,3.4,rest='frown',rate=8)
                if i==0: arm_to(H,1,hp(S['bi']),tl(t,1.7,2.0),base=(0,0,0))
                else: gest(H,t,1 if i==1 else -1,1.3,9)
        for k in ('bi','sh','fa','ah'): look_at(S[k],hp(S['th'][0]),.8*tl(t,.6,1.2),maxyaw=75)
        face(S['bi'],mouth='frown',brow=-.03,brow_r=-12); face(S['sh'],mouth='flat',brow=-.03,brow_r=-10); face(S['fa'],mouth='o',brow=.05)
        q=ease(t/DUR); camset(LV((-.6,-2.0,1.65),WIDE[0],q),WIDE[1],26,16)
    return dict(upd=upd)
SHOTS['STRANGERS']=STRANGERS_
def up_pose(S,t,k1=1.0,k2=1.0):
    Bi=S['bi']; Sh=S['sh']
    for H,k,(x,y),rz0 in ((Bi,k1,(-3.4,3.3),60),(Sh,k2,(-2.9,4.9),15)):
        sit(H,1-k,.6); H['root'].location[0]=L(SP['bi' if H is Bi else 'sh'][0],x,k); H['root'].location[1]=L(SP['bi' if H is Bi else 'sh'][1],y,k); H['root'].rotation_euler=(R(8*k),0,R(lerp_angle(rz0,82,k)))
        if k>=1: H['root'].location[2]=0
        blink(H,t); H['arm'][1].rotation_euler=(R(-28*k),0,R(22*k)); H['arm'][-1].rotation_euler=(R(-28*k),0,R(-22*k)); face(H,mouth='frown',brow=-.04,brow_r=-16)
def GETUP_():
    S=stall_set(True,True); Ah=S['ah']
    def upd(t):
        stall_idle(S,t,('fa','ah')); thug_idle(S,t); shk(Ah,0); face(Ah,mouth='o',brow=.05); face(S['fa'],mouth='o',brow=.05); up_pose(S,t,ease(tl(t,.15,.6)),ease(tl(t,.45,.9)))
        q=ease(t/DUR); camset(LV((-1.6,.2,.95),(-1.8,.6,1.0),q),(-3.3,4.0,1.65),28,8)
    return dict(upd=upd)
SHOTS['GETUP']=GETUP_
AB=(-1.0,2.5)
def BETWEEN_():
    S=stall_set(True,True); Ah=S['ah']
    def upd(t):
        stall_idle(S,t,('fa',)); thug_idle(S,t); up_pose(S,t); shk(Ah,0); face(S['fa'],mouth='o',brow=.05)
        if t<1.3: walk_path(Ah,[(-2.0,4.6),(-1.6,5.3),(-.9,4.6),AB],t,-.1,1.3,step=.5); blink(Ah,t)
        else: stand(Ah,t); blink(Ah,t); Ah['root'].location=(AB[0],AB[1],0); Ah['root'].rotation_euler[2]=0
        k=tl(t,1.1,1.5); Ah['arm'][1].rotation_euler=(R(-10*k),R(-78*k),0); Ah['arm'][-1].rotation_euler=(R(-10*k),R(78*k),0); face(Ah,mouth='flat',brow=.03)
        q=ease(t/DUR); camset(LV(WIDE[0],(-.9,-.8,1.6),q),(-.8,3.4,1.5),26,16)
    return dict(upd=upd)
SHOTS['BETWEEN']=BETWEEN_
def mid_set():
    S=stall_set(True,True); Ah=S['ah']; Ah['root'].location=(AB[0],AB[1],0); return S,Ah
def mid_idle(S,Ah,t,freeze=False):
    tt=0 if freeze else t
    stall_idle(S,tt,('fa',)); thug_idle(S,tt); up_pose(S,tt); stand(Ah,tt); Ah['root'].location=(AB[0],AB[1],0)
    if not freeze: blink(Ah,t)
def RELAX_():
    S,Ah=mid_set()
    def upd(t):
        mid_idle(S,Ah,t); Ah['root'].rotation_euler[2]=R(8); shk(Ah,0); talk(Ah,t,85.27,87.6); face(Ah,brow=.04); g=math.sin(t*5)
        Ah['arm'][1].rotation_euler=(R(-55+8*g),R(-25),0); Ah['arm'][-1].rotation_euler=(R(-55+8*g),R(25),0); Ah['head'].rotation_euler=(0,0,R(22*math.sin(t*1.8)))
        q=ease(t/DUR); camset(LV((-.6,-.4,1.85),(-.7,-.1,1.88),q),hp(Ah,.0),45,2.8)
    return dict(upd=upd)
SHOTS['RELAX']=RELAX_
def SLAUGH_():
    S,Ah=mid_set()
    def upd(t):
        mid_idle(S,Ah,t)
        for i,H in enumerate(S['th']): laugh(H,t+i*1.3,1.2); H['root'].rotation_euler[0]=R(-8*abs(math.sin(t*5+i))); arms(H,-22,0,18,-22,0,-18)
        q=ease(t/DUR); camset(LV((0.0,1.4,1.9),(.15,1.7,1.92),q),(1.5,3.9,2.05),35,5.6)
    return dict(upd=upd)
SHOTS['SLAUGH']=SLAUGH_
def PHONE_():
    S,Ah=mid_set(); ph=phone(Ah,-1,1.4)
    def upd(t):
        mid_idle(S,Ah,t); Ah['root'].rotation_euler[2]=R(-6); shk(Ah,0); k=ease(tl(t,.5,1.1)); ph.scale=(1,1,1) if t>.45 else (0,0,0); hold_phone(Ah,-1,k); Ah['head'].rotation_euler[0]=R(14*k); face(Ah,mouth='smirk',brow=-.02)
        q=ease(t/DUR); camset(LV((-2.2,-.1,1.6),(-2.0,.2,1.6),q),(-1.0,2.5,1.65),40,4.0)
    return dict(upd=upd)
SHOTS['PHONE']=PHONE_
def DAD_():
    S,Ah=mid_set(); ph=phone(Ah,-1,1.4); bubble('ABBU   calling...',(-.75,3.6,2.95),.5,size=.17,col='#1F3A2A',bg='#DFF5E1'); cam=(1.0,1.9,1.85)
    def upd(t):
        mid_idle(S,Ah,t); facep(Ah,(1.5,3.8),.55,cam=cam); shk(Ah,0); ear(Ah,-1,1); talk(Ah,t,91.56,94.3); face(Ah,brow=-.03,brow_r=-6); g=math.sin(t*5); Ah['arm'][1].rotation_euler=(R(-60-10*g),0,R(16))
        q=ease(t/DUR); camset(LV(cam,(.8,2.1,1.87),q),hp(Ah,.1),45,2.8)
    return dict(upd=upd)
SHOTS['DAD']=DAD_
def FREEZE_():
    S,Ah=mid_set(); ph=phone(Ah,-1,1.4)
    def upd(t):
        mid_idle(S,Ah,t,True); Ah['root'].rotation_euler[2]=R(20); shk(Ah,0); ear(Ah,-1,1); face(Ah,mouth='smirk')
        for H in S['th']: face(H,mouth='O',brow=.06,brow_r=10,eyes=1.3)
        for k in ('bi','sh','fa'): face(S[k],mouth='O',brow=.06,eyes=1.25); look_at(S[k],hp(Ah),.9,maxyaw=75)
        q=t/DUR; camset(LV((-.8,-1.2,1.65),(-.8,-.9,1.65),q),(-.8,3.5,1.5),26,16)
    return dict(upd=upd)
SHOTS['FREEZE']=FREEZE_
def CONN_():
    S,Ah=mid_set(); Fa=S['fa']
    def upd(t):
        mid_idle(S,Ah,t); k=tl(t,.05,.3); headtouch(Fa,1,k,dx=.55,dy=-.1,dz=.5); headtouch(Fa,-1,k,dx=.55,dy=-.1,dz=.5); talk(Fa,t,95.96,98.4,shapes=('O','o','O','flat')); face(Fa,brow=.06,eyes=1.3)
        Fa['head'].rotation_euler=(R(-6),0,R(-18+10*math.sin(t*6)))
        q=ease(t/DUR); camset(LV((-2.1,1.3,1.5),(-1.9,1.7,1.5),q),hp(Fa,.02),48,2.8)
    return dict(upd=upd)
SHOTS['CONN']=CONN_
def SMILE_():
    S,Ah=mid_set()
    def upd(t):
        mid_idle(S,Ah,t); Ah['root'].rotation_euler[2]=R(10); k=ease(tl(t,.3,.75)); shk(Ah,k); headtouch(Ah,1,math.sin(pi*tl(t,.15,.95)),dx=.6,dy=-.7,dz=.5); face(Ah,mouth='smirk',brow=-.02)
        q=ease(t/DUR); camset(LV((-.8,-.2,1.88),(-.85,.1,1.9),q),hp(Ah,.03),55,2.8)
    return dict(upd=upd)
SHOTS['SMILE']=SMILE_
def ISB_():
    S,Ah=mid_set()
    def upd(t):
        mid_idle(S,Ah,t); Ah['root'].rotation_euler[2]=R(6); shk(Ah,1); talk(Ah,t,99.87,101.8,rest='smirk'); Ah['arm'][1].rotation_euler=(R(-30),0,R(-55)); Ah['arm'][-1].rotation_euler=(R(-30),0,R(55)); face(Ah,brow=-.02)
        b=ease(tl(t,.5,2.0))
        for i,H in enumerate(S['th']): H['root'].location=(TP[i][0]+4.5*b,TP[i][1]+.6*b,0); walk(H,-4.5*b,step=.4); face(H,mouth='o',brow=.06,brow_r=12)
        for k in ('bi','sh'): face(S[k],mouth='O',brow=.06); look_at(S[k],hp(Ah),.9,maxyaw=75)
        q=ease(t/DUR); camset(LV((-.2,.3,.8),(-.3,.6,.85),q),(-1.0,2.5,1.85),28,8)
    return dict(upd=upd)
SHOTS['ISB']=ISB_

# ================================================================ FINAL — the house
def house_pick():
    if not HOUSES:
        r=random.Random(21); x=-66
        while x<66:
            w=r.choice([11,12,13]); r.choice([6.0,6.8,7.4]); HOUSES.append((x+w/2,w)); x+=w
        HOUSES.append(None)
    c=min([h for h in HOUSES if h],key=lambda h: abs(h[0]-28)); return c[0],c[1],c[0]+c[1]*.2
def HOUSE_():
    cx,w,gx=house_pick(); sector_set('morning_s',gx,True); Bi,Sh,Fa=boys3(((0,5.2),(0,5.2),(0,5.2)))
    def upd(t):
        for i,H in enumerate((Bi,Sh,Fa)):
            walk_path(H,[(gx-7.5-i*1.1,5.0+.3*(i%2)),(gx-1.2-i*1.1+1.1,5.0+.3*(i%2))],t,-.6,DUR+.2,z=.14,step=.55); blink(H,t); look_at(H,(cx,12,4.5),.7*tl(t,.8,1.6)); face(H,mouth='o',brow=.05)
        q=ease(t/DUR); camset(LV((cx-4.5,-2.8,1.1),(cx-2.0,-2.4,2.0),q),LV((cx-1.5,9,2.6),(cx,10,3.0),q),24,16)
    return dict(upd=upd)
SHOTS['HOUSE']=HOUSE_
def BOYSARR_():
    cx,w,gx=house_pick(); sector_set('morning_s',gx,True); Bi,Sh,Fa=boys3(((gx-1.15,5.5),(gx,5.9),(gx+1.15,5.5)),(180,180,180))
    for H in (Bi,Sh,Fa): H['z0']=.14
    def upd(t):
        idle_all((Bi,Sh,Fa),t)
        for i,H in enumerate((Bi,Sh,Fa)): H['root'].location[2]=.14; H['head'].rotation_euler=(R(-18),0,R(12*math.sin(t*1.6+i*2))); face(H,mouth='O' if i!=0 else 'o',brow=.06,eyes=1.2)
        k=tl(t,.5,.9); headtouch(Bi,1,k,dx=.3,dy=-.75,dz=-.25); Fa['arm'][1].rotation_euler=(R(-70*k),0,R(-25)); Fa['arm'][-1].rotation_euler=(R(-70*k),0,R(25))
        q=ease(t/DUR); camset(LV((gx+.3,8.4,2.7),(gx+.2,8.2,2.6),q),(gx,5.7,1.75),28,8)
    return dict(upd=upd)
SHOTS['BOYSARR']=BOYSARR_
def FEAST_():
    S=dining_set(); Mo=S['mo']; dish=in_hand(Mo,1,lambda e: karahi_obj((0,-.25,.0),.9,parent=e)); sparkles((0,0,1.5),1.8,.3,2.4,30,.04,11,.3)
    def upd(t):
        dine_idle(S,t); Mo['root'].location=(-3.45,.25,0); Mo['arm'][1].rotation_euler=(R(-62),0,R(-8)); Mo['arm'][-1].rotation_euler=(R(-62),0,R(8)); face(Mo,mouth='smile'); Mo['root'].rotation_euler[2]=R(90)
        for i,k in enumerate(('bi','fa','sh')): H=S[k]; H['head'].rotation_euler=(R(14),0,R(14*math.sin(t*1.4+i*2))); face(H,mouth='O',brow=.06,eyes=1.25)
        g=abs(math.sin(t*9)); S['fa']['arm'][1].rotation_euler=(R(-70),0,R(-24-8*g)); S['fa']['arm'][-1].rotation_euler=(R(-70),0,R(24+8*g)); face(S['ah'],mouth='smile'); look_at(S['ah'],hp(S['fa']),.5)
        q=ease(t/DUR); camset(LV((-2.6,-3.5,2.3),(1.0,-3.6,2.0),q),LV((-.6,.5,1.2),(.2,.5,1.25),q),24,8)
    return dict(upd=upd)
SHOTS['FEAST']=FEAST_
def BITE_():
    S=dining_set(); Bi=S['bi']; dr=in_hand(Bi,1,lambda e: drumstick(e,1.5)); sparkles((-1.6,1.1,2.3),.5,1.35,2.4,18,.04,12,.3)
    def upd(t):
        dine_idle(S,t); k=math.sin(pi*tl(t,.3,1.3)); Bi['arm'][1].rotation_euler=(R(-75-48*k),0,R(-18*k)); wow=t>1.35
        face(Bi,mouth=('O' if k>.7 else 'flat') if not wow else 'O',brow=.06 if wow else 0,eyes=1.3 if wow else 1.0); Bi['head'].rotation_euler=(R(6*k),0,0)
        if .9<t<1.35: face(Bi,mouth=('o','flat')[int(t*10)%2])
        q=ease(t/DUR); camset(LV((-1.3,-1.5,1.85),(-1.4,-1.1,1.88),q),hp(Bi,-.02),45,2.8)
    return dict(upd=upd)
SHOTS['BITE']=BITE_
def KAMAAL_():
    S=dining_set(); Bi=S['bi']; dr=in_hand(Bi,1,lambda e: drumstick(e,1.5))
    def upd(t):
        dine_idle(S,t); talk(Bi,t,111.68,115.4); face(Bi,brow=.05); g=math.sin(t*6); Bi['arm'][1].rotation_euler=(R(-85-12*g),0,R(10)); Bi['head'].rotation_euler=(0,R(4*g),R(-28*tl(t,.2,.6)))
        Bi['arm'][-1].rotation_euler=(R(-60*tl(t,1.6,1.9)),0,R(-30)); face(S['fa'],mouth=('o','flat')[int(t*5)%2]); S['fa']['head'].rotation_euler[0]=R(8+6*math.sin(t*7)); face(S['sh'],mouth='grin')
        q=ease(t/DUR); camset(LV((-2.2,-1.5,2.1),(-2.1,-1.2,2.1),q),(-1.6,1.32,1.85),40,4.0)
    return dict(upd=upd)
SHOTS['KAMAAL']=KAMAAL_
def PROUD_():
    S=dining_set(); Ah=S['ah']; ts=117.39-T0
    def upd(t):
        dine_idle(S,t); shk(Ah,0); talk(Ah,t,117.39,119.4,rest='smirk'); face(Ah,mouth='smirk' if t<ts else None,brow=-.02); k=tl(t,ts,ts+.3); Ah['arm'][1].rotation_euler=(R(-70*k),0,R(-40*k)); Ah['head'].rotation_euler=(R(-6),0,R(-26))
        Ah['arm'][-1].rotation_euler=(R(-20),0,0)
        q=ease(t/DUR); camset(LV((1.2,-1.9,1.75),(1.5,-1.5,1.78),q),hp(Ah,.02),48,2.8)
    return dict(upd=upd)
SHOTS['PROUD']=PROUD_
def MOMIN_():
    S=dining_set(); Mo=S['mo']
    def upd(t):
        dine_idle(S,t); walk_path(Mo,[(-5.2,-1.9),(-3.9,-1.6),(-3.2,-1.25)],t,-.2,1.15,step=.5); blink(Mo,t)
        if t>=1.15: stand(Mo,t); Mo['root'].rotation_euler[2]=R(55)
        face(Mo,mouth='flat',brow=-.03,brow_r=-10); Mo['arm'][-1].rotation_euler=(R(-20),0,R(48))
        q=ease(t/DUR); camset(LV((-1.2,-3.6,1.6),(-1.4,-3.4,1.62),q),(-3.5,-1.4,1.6),32,5.6)
    return dict(upd=upd)
SHOTS['MOMIN']=MOMIN_
def MOM_():
    S=dining_set(); Mo=S['mo']; cam=(-1.9,-2.9,1.75)
    def upd(t):
        dine_idle(S,t); Mo['root'].location=(-3.2,-1.25,0); Mo['root'].rotation_euler[2]=R(50); talk(Mo,t,120.97,124.6); face(Mo,brow=-.04,brow_r=-14)
        k=tl(t,.7,1.0); arm_to(Mo,1,(2.0,2.2,0),k,base=(-60,0,0)); Mo['arm'][-1].rotation_euler=(R(-20),0,R(48)); Mo['head'].rotation_euler=(0,0,R(8*math.sin(t*5)))
        q=ease(t/DUR); camset(LV(cam,(-2.1,-2.7,1.77),q),hp(Mo,.0),48,2.8)
    return dict(upd=upd)
SHOTS['MOM']=MOM_
def TRAIL_():
    S=dining_set(True)
    def upd(t):
        dine_idle(S,t); q=ease(t/DUR); camset(LV((4.0,-3.4,2.6),(1.6,-2.8,2.4),q),LV((4.6,-.3,0),(1.0,2.0,0),q),28,8)
    return dict(upd=upd)
SHOTS['TRAIL']=TRAIL_
def LOOKO_():
    S=dining_set(True); Bi=S['bi']
    def upd(t):
        dine_idle(S,t); Bi['head'].rotation_euler=(0,0,R(-38*math.sin(pi*tl(t,.1,.7))+38*math.sin(pi*tl(t,.7,1.4)))); face(Bi,mouth='flat',brow=.05)
        face(S['fa'],mouth='o',brow=.05); face(S['sh'],mouth='flat',brow=.05); S['sh']['arm'][1].rotation_euler=(R(-40),0,R(40)); S['sh']['arm'][-1].rotation_euler=(R(-40),0,R(-40))
        look_at(S['fa'],(0,-1,.2),.6)
        q=ease(t/DUR); camset(LV((-.7,-2.9,2.35),(-.8,-2.5,2.35),q),(-.9,1.3,1.65),32,5.6)
    return dict(upd=upd)
SHOTS['LOOKO']=LOOKO_
def NIKLA_():
    S=dining_set(True); Bi=S['bi']
    def upd(t):
        dine_idle(S,t); k=ease(tl(t,.05,.4)); sit(Bi,1-k,.62);
        if k>=1: Bi['root'].location[2]=0
        talk(Bi,t,126.25,129.4,shapes=('O','flat','o','grin')); face(Bi,brow=.06); arm_to(Bi,-1,hp(S['ah']),tl(t,.7,1.0),base=(0,0,0)); g=math.sin(t*10); Bi['arm'][1].rotation_euler=(R(-150*k),0,R(18+10*g))
        Bi['head'].rotation_euler=(R(-6+4*g),0,R(-20)); laugh(S['fa'],t); laugh(S['sh'],t+1)
        q=ease(t/DUR); camset(LV((-.6,-2.6,2.35),(-.7,-2.2,2.35),q),(-1.3,1.3,1.85),30,5.6)
    return dict(upd=upd)
SHOTS['NIKLA']=NIKLA_
def LAUGH_():
    S=dining_set(True); Ah=S['ah']; Mo=S['mo']
    def upd(t):
        dine_idle(S,t); Mo['root'].location=(-3.4,-.9,0); Mo['root'].rotation_euler[2]=R(60); Mo['head'].rotation_euler=(0,0,R(14*math.sin(t*5))); face(Mo,mouth='smile'); Mo['arm'][-1].rotation_euler=(R(-20),0,R(48))
        for i,k in enumerate(('bi','fa','sh')): H=S[k]; laugh(H,t+i*1.7,1.2); H['root'].rotation_euler[0]=R(-10*abs(math.sin(t*4+i))); H['arm'][1].rotation_euler=(R(-60-30*math.sin(t*12+i)),0,R(10))
        shk(Ah,0); headtouch(Ah,1,tl(t,.2,.5),dx=.05,dy=-.8,dz=.2); Ah['head'].rotation_euler[0]=R(14); face(Ah,mouth='smile')
        q=ease(t/DUR); camset(LV((0,-3.9,2.2),(0,-3.5,2.3),q),(0,.5,1.45),22,16)
    return dict(upd=upd)
SHOTS['LAUGH']=LAUGH_
def CARD_():
    Bi,Sh,Fa,Ah=view_set('sunset'); Ah['root'].location=(-.3,3.6,0); Bi['root'].location=(-1.5,3.7,0); Sh['root'].location=(1.0,3.9,0); Fa['root'].location=(2.2,3.6,0)
    point((0,-1.5,2.6),1400,(1,.85,.7),1.0,False)
    tm=M('#FFF3B0',.4,emit=2.2); bk=M('#1B1F33',.6); L_=[]
    for i,(s_,tt) in enumerate((('ONE ISLAMABADI.',131.69),('THREE PINDI BOYS.',133.26),('ZERO PEACE.',134.79))):
        e=empty((.2,3.2,4.75-i*.62)); obox((0,.06,0),(len(s_)*.125+.25,.03,.25),bk,.08,e); text(s_,(0,0,0),(0,-1,0),.36,tm,ex=.02,parent=e); e.scale=(0,0,0); L_.append((e,tt-T0))
    def upd(t):
        idle_all((Bi,Sh,Fa,Ah),t); shk(Ah,0); hold(Ah,1); Ah['root'].rotation_euler[2]=R(-4); Bi['root'].rotation_euler[2]=R(30); arm_to(Bi,1,hp(Ah,.3),1,base=(0,0,0)); laugh(Bi,t); Ah['root'].rotation_euler[1]=R(-6); Ah['head'].rotation_euler[1]=R(-8)
        face(Ah,mouth='flat',brow=-.03,brow_r=-10); laugh(Sh,t+1); laugh(Fa,t+2); g=math.sin(t*8); Fa['arm'][1].rotation_euler=(R(-160),0,R(18+10*g)); Sh['arm'][-1].rotation_euler=(R(-150),0,R(-18-10*g)); look_at(Sh,hp(Ah),.6); look_at(Fa,hp(Ah),.6)
        for e,tt in L_:
            k=pop(t-tt) if t>=tt else 0; e.scale=(k,k,k)
        q=ease(t/DUR); camset(LV((.2,-4.9,1.8),(.2,-4.5,1.85),q),(.2,3.6,2.75),26,16)
    return dict(upd=upd)
SHOTS['CARD']=CARD_
