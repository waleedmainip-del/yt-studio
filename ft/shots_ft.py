# Shots for "Faisalabad: The Textile Kingdom". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=127.4
SEQ=[('OPEN', 0.0), ('EMPIRE', 3.92), ('MEET', 6.1), ('SHOP', 7.04), ('FATHER', 10.89), ('DREAMS', 14.53), ('BILLION', 16.76), ('ABU', 19.95), ('PEHLE', 22.53), ('TWELVE', 24.76), ('NINE', 26.93), ('BRAND', 28.61), ('NAMES', 30.97), ('IFG', 32.12), ('THREE', 33.9), ('BILAL', 36.86), ('BIRYANI', 40.22), ('ROOF', 42.57), ('BG', 43.9), ('OYE', 46.67), ('INSTA', 48.81), ('PIN', 50.23), ('ACROSS', 51.61), ('BIGSIGN', 54.82), ('COPY', 60.25), ('PUTTAR', 62.44), ('BUYER', 65.82), ('TENK', 70.11), ('CELEB', 73.54), ('DANCE', 75.32), ('MOTHER', 76.7), ('CAR', 77.75), ('ORDER', 79.82), ('CALM', 81.75), ('KAPRA', 84.39), ('SILENCE', 86.36), ('MILLRUN', 89.47), ('LOOMS', 91.47), ('OWNER', 92.99), ('DAS', 94.79), ('POCKET', 96.9), ('RUPEES', 98.4), ('BACK', 101.47), ('ADVANCE', 103.82), ('SMILE', 106.72), ('PUTTARF', 110.16), ('DISCOUNT', 113.25), ('REPLY', 115.33), ('CHARGES', 117.21), ('PAYS', 122.36), ('FAINT', 124.57)]
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
def bz_set(mood='afternoon',crowd=10,seed=3):
    hands=bazaar_ft(); B.done('bazaar'); setup_world(mood,shadow=45); set_clock(hands,4,10)
    W=walkers(crowd,seed,-24,24,(-1.6,1.6)); return hands,W
def shop_set():
    shop_int(); B.done('shop'); setup_interior('day',room=(0,0,3.3),res=PCT,samples=SAMPLES,shadow_dist=14); point((0,-.5,2.8),130,(1,.95,.86),1.2,False); point((0,-4,2.5),300,(1,.92,.8),1.5,False)
    fan=fan_ft((-.6,.2,3.0)); Ra=mk(RASHID,0,1.95,0,'rashid'); Ju=mk(JUNAID,1.3,.35,200,'junaid'); return fan,Ra,Ju
def sidle(Ra,Ju,t,fan=None,fs=1.0):
    stand(Ra,t); blink(Ra,t); stand(Ju,t); blink(Ju,t)
    if fan is not None: fan.rotation_euler[2]=t*9*fs
def measure(Ra,t):
    g=math.sin(t*4); Ra['arm'][1].rotation_euler=(R(-35-8*g),0,R(-15+15*g)); Ra['arm'][-1].rotation_euler=(R(-35+8*g),0,R(15+15*g)); Ra['head'].rotation_euler[0]=R(18)
def dance(H,t,amp=1.0):
    g=math.sin(t*10); H['root'].location[2]+=.08*abs(g)*amp; H['root'].rotation_euler[2]+=R(15*g*amp); H['arm'][1].rotation_euler=(R(-160+25*g),0,R(15)); H['arm'][-1].rotation_euler=(R(-160-25*g),0,R(-15))
# ================================================================ HOOK
def OPEN_():
    hands,W=bz_set(crowd=14)
    def upd(t):
        upd_walkers(W,t+2); q=ease(t/DUR); camset(LV((-14,0,7.5),(-10,0,2.4),q),LV((10,0,6),(14,0,6.5),q),22,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def EMPIRE_():
    fan,Ra,Ju=shop_set(); Ju['root'].location=(0,.3,0); Ju['root'].rotation_euler[2]=0; title_card('INTERNATIONAL EMPIRE?',.6,(0,1.4,2.75),.24); sparkles((0,.3,1.6),1.2,.2,DUR,n=26,size=.03)
    def upd(t):
        sidle(Ra,Ju,t,fan); Ju['root'].location=(0,.3,0); Ju['root'].rotation_euler[2]=0; face(Ju,mouth='grin',brow=.06); k=tl(t,.1,.5)
        Ju['arm'][1].rotation_euler=(R(-165*k),0,R(10)); Ju['arm'][-1].rotation_euler=(R(-30*k),0,R(-40*k)); measure(Ra,t); face(Ra,mouth='flat',brow=-.03)
        q=ease(t/DUR); camset(LV((0,-2.6,1.4),(0,-2.2,1.5),q),(0,.6,1.75),24,8)
    return dict(upd=upd)
SHOTS['EMPIRE']=EMPIRE_
# ================================================================ SCENE 1
def MEET_():
    fan,Ra,Ju=shop_set(); label('JUNAID',(1.3,.35,2.65),.1,col='#1B1F33',bg='#FFF3B0')
    def upd(t):
        sidle(Ra,Ju,t,fan); Ju['root'].rotation_euler[2]=R(lerp_angle(200,345,tl(t,0,.4))); face(Ju,mouth='grin',brow=.05); shk(Ju,1-tl(t,.2,.6)) if False else None
        q=ease(t/DUR); camset(LV((.9,-1.0,1.9),(.95,-.85,1.9),q),hp(Ju,-.15),36,4)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def SHOP_():
    hands,W=bz_set(crowd=5,seed=5); label('SINCE 1994',(0,3.2,4.35),.8,size=.22)
    def upd(t):
        upd_walkers(W,t+4); q=ease(t/DUR); camset(LV((-4.5,-2.9,2.7),(-3.6,-2.8,2.9),q),(0,3.6,2.8),22,12)
    return dict(upd=upd)
SHOTS['SHOP']=SHOP_
def FATHER_():
    fan,Ra,Ju=shop_set(); Ju['root'].location=(9,9,0); label('30 YEARS. SAME LAWN.',(0,1.95,2.75),.6,size=.2)
    def upd(t):
        sidle(Ra,Ju,t,fan); measure(Ra,t); face(Ra,mouth='flat',brow=-.02,eyes=.7)
        q=ease(t/DUR); camset(LV((-1.3,.1,2.1),(-1.2,.25,2.1),q),hp(Ra,-.3),30,5.6)
    return dict(upd=upd)
SHOTS['FATHER']=FATHER_
def DREAMS_():
    fan,Ra,Ju=shop_set(); b=bubble('BILLIONAIRE',(1.0,.4,2.75),.4,size=.2,col='#7A5A10',bg='#FFF3B0'); sparkles((1.3,.35,2.4),.6,.3,DUR,n=24,size=.03)
    def upd(t):
        sidle(Ra,Ju,t,fan); Ju['root'].rotation_euler[2]=R(330); face(Ju,mouth='smile',brow=.06,eyes=.55); Ju['head'].rotation_euler=(R(-14),0,R(8*math.sin(t*1.5)))
        Ju['arm'][1].rotation_euler=(R(-40),0,R(-60)); Ju['arm'][-1].rotation_euler=(R(-40),0,R(60))
        q=ease(t/DUR); camset(LV((.5,-1.4,1.7),(.55,-1.15,1.75),q),hp(Ju,-.05),32,4)
    return dict(upd=upd)
SHOTS['DREAMS']=DREAMS_
def BILLION_():
    fan,Ra,Ju=shop_set(); title_card('BILLIONAIRE BEFORE 25',.15,(1.0,.6,2.75),.22); coins=[]
    for k in range(14):
        e=empty((0,0,-50)); ocyl((0,0,0),.08,.02,M('#F2C14E',.25,metal=.9,emit=.3),e,rot=(R(90),0,0),seg=14); coins.append((e,random.Random(k).uniform(-1,1),random.Random(k+50).uniform(0,1.5)))
    def upd(t):
        sidle(Ra,Ju,t,fan); Ju['root'].rotation_euler[2]=R(330); face(Ju,mouth='grin',brow=.06); dance(Ju,t,.5)
        for e,dx,t0 in coins: q=((t+t0)%1.5)/1.5; e.location=(1.3+dx*.8,.0+dx*.2,2.6-2.6*q); e.rotation_euler=(R(90),0,t*6+dx)
        q=ease(t/DUR); camset(LV((.4,-2.4,1.6),(.45,-2.0,1.65),q),(1.1,.5,1.6),28,8)
    return dict(upd=upd)
SHOTS['BILLION']=BILLION_
def ABU_():
    fan,Ra,Ju=shop_set()
    def upd(t):
        sidle(Ra,Ju,t,fan); facep(Ju,(0,1.95)); talk(Ju,t,*ln(55,62)); face(Ju,brow=.06,brow_r=8); gest(Ju,t,1,1.2,8,-80); gest(Ju,t+1,-1,1.0,8,-70)
        measure(Ra,t)
        q=ease(t/DUR); camset(LV((-.3,1.2,1.95),(-.25,1.05,1.95),q),hp(Ju,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['ABU']=ABU_
def PEHLE_():
    fan,Ra,Ju=shop_set()
    def upd(t):
        sidle(Ra,Ju,t,fan); facep(Ju,(0,1.95)); facep(Ra,(1.3,.35),.6,cam=(.9,-.3)); talk(Ra,t,*ln(63,70)); face(Ra,brow=-.05,brow_r=-16); arm_to(Ra,1,hp(Ju,-.1),tl(t,.2,.5),base=(-30,0,0)); Ra['arm'][-1].rotation_euler=(R(-50),0,R(20))
        q=ease(t/DUR); camset(LV((.95,-.25,1.95),(.9,-.05,1.95),q),hp(Ra,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['PEHLE']=PEHLE_
def TWELVE_():
    hands,W=bz_set(crowd=4,seed=7); set_clock(hands,12,0); Ju=mk(JUNAID,-8,0,-90,'junaid'); cc=clock_card((-1.4,0,3.0),.4,'12:00 PM')
    def upd(t):
        upd_walkers(W,t+6); walk_path(Ju,[(-7,.6),(-1.2,1.8)],t,0,DUR,step=.5); face(Ju,mouth='smile',eyes=.6); blink(Ju,t)
        Ju['arm'][1].rotation_euler[0]+=0
        q=ease(t/DUR); camset(LV((-2.5,-2.8,1.6),(-1.8,-2.6,1.6),q),(hp(Ju)[0],hp(Ju)[1],1.7),26,8)
    return dict(upd=upd)
SHOTS['TWELVE']=TWELVE_
def NINE_():
    fan,Ra,Ju=shop_set(); Ju['root'].location=(9,9,0); cc=clock_card((-1.3,2.4,2.55),.35,'OPEN: 9:00 AM',spin=0)
    def upd(t):
        sidle(Ra,Ju,t,fan); face(Ra,mouth='frown',brow=-.05,brow_r=-16); k=tl(t,.1,.4); Ra['arm'][1].rotation_euler=(R(-40*k),0,R(-45*k)); Ra['arm'][-1].rotation_euler=(R(-40*k),0,R(45*k)); Ra['root'].rotation_euler[2]=R(15)
        q=ease(t/DUR); camset(LV((.9,-.4,1.85),(.85,-.25,1.87),q),(-.25,1.9,2.0),28,4)
    return dict(upd=upd)
SHOTS['NINE']=NINE_
# ================================================================ SCENE 2 — the brand
def BRAND_():
    fan,Ra,Ju=shop_set(); Ju['root'].location=(1.8,.6,0); ph=phone(Ju,1,1.4); sparkles((1.8,.4,2.1),.5,.3,DUR,n=20,size=.025)
    b=bubble('CREATING BRAND...',(1.8,.6,2.7),.4,size=.16,col='#1B1F33',bg='#DFEBFF')
    def upd(t):
        sidle(Ra,Ju,t,fan); Ju['root'].location=(1.8,.6,0); facep(Ju,(2.9,-.3)); hold_phone(Ju,1,1); Ju['head'].rotation_euler[0]=R(14); face(Ju,mouth='grin',brow=.05)
        g=math.sin(t*14); Ju['arm'][-1].rotation_euler=(R(-75+6*g),0,R(30)); Ra['head'].rotation_euler[2]=R(25); face(Ra,mouth='flat',brow=-.03)
        q=ease(t/DUR); camset(LV((2.9,-.3,1.9),(2.8,-.15,1.9),q),hp(Ju,-.2),32,4)
    return dict(upd=upd)
SHOTS['BRAND']=BRAND_
def NAMES_():
    fan,Ra,Ju=shop_set(); Ju['root'].location=(1.0,.2,0)
    def upd(t):
        sidle(Ra,Ju,t,fan); Ju['root'].location=(1.0,.2,0); Ju['root'].rotation_euler[2]=R(-15); face(Ju,mouth='smile',brow=.06,eyes=.7); k=tl(t,0,.4)
        Ju['arm'][1].rotation_euler=(R(-160*k),0,R(-45*k)); Ju['arm'][-1].rotation_euler=(R(-160*k),0,R(45*k))
        q=ease(t/DUR); camset(LV((.9,-1.7,1.6),(.9,-1.4,1.6),q),hp(Ju,-.2),26,4)
    return dict(upd=upd)
SHOTS['NAMES']=NAMES_
def IFG_():
    hands,W=bz_set(crowd=0,seed=9); bn=ifg_banner(); Ju=mk(JUNAID,1.6,1.8,200,'junaid'); sparkles((0,3.0,4.6),2.6,.4,1.6,n=40,size=.04)
    def upd(t):
        upd_walkers(W,t+8); k=pop(t-.1) if t>.1 else 0; bn.scale=(k,k,k); stand(Ju,t); blink(Ju,t); facep(Ju,(0,3.5),.5,cam=(0,-3)); face(Ju,mouth='grin',brow=.06)
        Ju['arm'][1].rotation_euler=(R(-150),0,R(-20)); Ju['arm'][-1].rotation_euler=(R(-40),0,R(30))
        q=ease(t/DUR); camset(LV((-.3,-3.0,1.4),(-.2,-2.6,1.5),q),(.1,3,3.1),20,12)
    return dict(upd=upd)
SHOTS['IFG']=IFG_
def THREE_():
    fan,Ra,Ju=shop_set(); Ju['root'].location=(-1.9,.1,0); rack=empty((-.6,.2,0)); sh=three_shirts(rack,1.0); label('FULL COLLECTION: 3 SHIRTS',(-.6,.2,2.35),.5,size=.18)
    def upd(t):
        sidle(Ra,Ju,t,fan); Ju['root'].location=(-1.9,.1,0); facep(Ju,(-.6,.2),.5,cam=(-.6,-2.5)); face(Ju,mouth='grin',brow=.05); arm_to(Ju,1,(-.6,.2,1.4),tl(t,.2,.5),base=(-30,0,0))
        for i,h in enumerate(sh): h.rotation_euler[2]=R(10*math.sin(t*2+i))
        q=ease(t/DUR); camset(LV((-.9,-2.6,1.5),(-.8,-2.2,1.5),q),(-.9,.2,1.3),26,8)
    return dict(upd=upd)
SHOTS['THREE']=THREE_
# ================================================================ roof shoot
def rf_set():
    kites=roof_set(); B.done('roof'); setup_world('day',shadow=30)
    Bi=mk(BILAL,0,2.0,0,'bilal'); Ju=mk(JUNAID,-.3,-1.2,180,'junaid'); ph=phone(Ju,1,1.4); rl=empty((.9,-.9,0)); ring_light(rl); return kites,Bi,Ju,ph
def ridle(K,Bi,Ju,t):
    stand(Bi,t); blink(Bi,t); stand(Ju,t); blink(Ju,t)
    for i,k in enumerate(K): k.location[2]+=.0; k.rotation_euler[1]=R(45+10*math.sin(t*2+i))
def pose(Bi,t,n):
    P=[((-170,0,10),(-170,0,-10),15),((-60,0,-80),(-20,0,40),-20),((-110,0,-10),(0,0,0),0),((-20,0,-90),(-20,0,90),25)]
    a,b,rz=P[n%len(P)]; Bi['arm'][1].rotation_euler=tuple(R(x) for x in a); Bi['arm'][-1].rotation_euler=tuple(R(x) for x in b); Bi['root'].rotation_euler[2]=R(rz)
def BILAL_():
    K,Bi,Ju,ph=rf_set(); label('COUSIN BILAL (MODEL)',(0,2.0,2.75),.3,size=.2,col='#7A3A10')
    def upd(t):
        ridle(K,Bi,Ju,t); pose(Bi,t,int(t/.9)); face(Bi,mouth='smile',brow=.04,eyes=.7); hold_phone(Ju,1,1)
        q=ease(t/DUR); camset(LV((2.5,-1.7,1.9),(2.3,-1.5,1.9),q),(0,2.0,1.5),26,8)
    return dict(upd=upd)
SHOTS['BILAL']=BILAL_
def BIRYANI_():
    K,Bi,Ju,ph=rf_set(); pl=in_hand(Bi,1,lambda e: biryani_plate(e,1.8)); label('PAYMENT: 1 PLATE BIRYANI',(0,2.0,2.7),.3,size=.18)
    def upd(t):
        ridle(K,Bi,Ju,t); Bi['arm'][1].rotation_euler=(R(-35),0,R(-10)); face(Bi,mouth='grin' if t%1<.5 else 'O',brow=.05); Bi['head'].rotation_euler[0]=R(10)
        g=abs(math.sin(t*5)); Bi['arm'][-1].rotation_euler=(R(-60-50*g),0,R(30))
        q=ease(t/DUR); camset(LV((1.0,.3,2.2),(.95,.45,2.2),q),hp(Bi,-.45),30,4)
    return dict(upd=upd)
SHOTS['BIRYANI']=BIRYANI_
def ROOF_():
    K,Bi,Ju,ph=rf_set()
    def upd(t):
        ridle(K,Bi,Ju,t); pose(Bi,t,1); face(Bi,mouth='smile',eyes=.7); hold_phone(Ju,1,1); Ju['root'].location[2]=-.15*tl(t,.2,.6); Ju['root'].rotation_euler[0]=R(10*tl(t,.2,.6))
        q=ease(t/DUR); camset(LV((-6,-5,5.5),(-5,-4.4,4.6),q),(0,1.0,1.0),24,16)
    return dict(upd=upd)
SHOTS['ROOF']=ROOF_
def BG_():
    K,Bi,Ju,ph=rf_set(); label('WATER TANK',(2.6,3.6,3.0),.4,size=.18); label('LAUNDRY',(-1.5,2.2,2.6),.9,size=.18)
    def upd(t):
        ridle(K,Bi,Ju,t); pose(Bi,t,3); face(Bi,mouth='grin',eyes=.8); hold_phone(Ju,1,1)
        q=ease(t/DUR); camset(LV((.7,-2.3,2.0),(.6,-1.9,1.95),q),(.6,2.4,1.7),26,8)
    return dict(upd=upd)
SHOTS['BG']=BG_
def OYE_():
    K,Bi,Ju,ph=rf_set(); Da=mk(DANISH,-2.2,-.4,90,'danish'); label('DANISH',(-2.2,-.4,2.55),.1,size=.18,col='#1F4D3A',bg='#DFF5E1')
    def upd(t):
        ridle(K,Bi,Ju,t); pose(Bi,t,2); stand(Da,t); blink(Da,t); facep(Da,(-.3,-1.2),.4,cam=(-1.2,-3)); talk(Da,t,*ln(133,137)); laugh(Da,t,.6); face(Da,brow=.06,brow_r=12); arm_to(Da,1,hp(Ju,-.5),tl(t,.1,.4),base=(-30,0,0))
        q=ease(t/DUR); camset(LV((-2.0,-2.4,1.85),(-2.0,-2.1,1.85),q),hp(Da,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['OYE']=OYE_
def INSTA_():
    K,Bi,Ju,ph=rf_set()
    def upd(t):
        ridle(K,Bi,Ju,t); pose(Bi,t,0); facep(Ju,(-2.2,-.4),.6,cam=(-.8,-3)); talk(Ju,t,*ln(138,144)); face(Ju,brow=.05,brow_r=-6,eyes=.8); hold_phone(Ju,1,.6); Ju['arm'][-1].rotation_euler=(R(-40),0,R(30))
        q=ease(t/DUR); camset(LV((-.7,-2.6,1.9),(-.65,-2.35,1.9),q),hp(Ju,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['INSTA']=INSTA_
def PIN_():
    D=insta_ui(); ui_world()
    def upd(t):
        k=1+.06*math.sin(t*8); D['pin'].scale=(k,k,k); camset((0,-L(7.4,6.6,ease(t/DUR)),-200),(0,0,-200),50,22)
    return dict(upd=upd)
SHOTS['PIN']=PIN_
# ================================================================ SCENE 3 — the rival
def street(seed=11,crowd=8):
    hands,W=bz_set(crowd=crowd,seed=seed); Sa=mk(SALEEM,.4,-2.9,0,'saleem'); Ju=mk(JUNAID,-.6,2.9,180,'junaid'); bn=ifg_banner(); return hands,W,Sa,Ju,bn
def ACROSS_():
    hands,W,Sa,Ju,bn=street(); label('UNCLE SALEEM',(.4,-2.9,2.8),.3,size=.2,col='#7A1F1F')
    def upd(t):
        upd_walkers(W,t+10); stand(Sa,t); blink(Sa,t); stand(Ju,t); blink(Ju,t); facep(Sa,(-.6,2.9),.5,cam=(2,2)); face(Sa,mouth='smile',brow=-.03,brow_r=-10,eyes=.6)
        Sa['arm'][1].rotation_euler=(R(-25),0,R(-35)); Sa['arm'][-1].rotation_euler=(R(-25),0,R(35))
        q=ease(t/DUR); camset(LV((1.6,1.6,1.9),(1.4,1.3,1.9),q),hp(Sa,-.3),32,5.6)
    return dict(upd=upd)
SHOTS['ACROSS']=ACROSS_
def BIGSIGN_():
    hands,W,Sa,Ju,bn=street(); gb=global_banner(); sparkles((0,-3.3,5.0),3.4,1.3,2.6,n=40,size=.04)
    def upd(t):
        upd_walkers(W,t+14); stand(Sa,t); blink(Sa,t); stand(Ju,t); blink(Ju,t); k=pop(t-1.1) if t>1.1 else 0; gb.scale=(k,k,k); gb.location[2]=5.0+3*(1-tl(t,1.0,1.6))
        facep(Sa,(0,0),.5,cam=(.5,4)); face(Sa,mouth='grin',brow=.04); Sa['arm'][1].rotation_euler=(R(-150*tl(t,1.3,1.8)),0,R(-25)); Sa['arm'][-1].rotation_euler=(R(-25),0,R(35))
        face(Ju,mouth='O' if t>2.0 else 'flat',brow=.07,brow_r=20)
        q=ease(t/DUR); camset(LV((.4,2.6,1.6),(.3,2.0,1.65),q),(0,-3.4,3.7),20,12)
    return dict(upd=upd)
SHOTS['BIGSIGN']=BIGSIGN_
def COPY_():
    hands,W,Sa,Ju,bn=street(); gb=global_banner()
    def upd(t):
        upd_walkers(W,t+20); stand(Sa,t); blink(Sa,t); stand(Ju,t); blink(Ju,t); Ju['root'].location=(-.3,1.2,0); facep(Ju,(.4,-2.9)); talk(Ju,t,*ln(170,175)); face(Ju,brow=-.06,brow_r=-22)
        arm_to(Ju,1,(.4,-3.6,3.2),tl(t,.1,.35),base=(-30,0,0)); g=math.sin(t*9); Ju['arm'][-1].rotation_euler=(R(-60-20*g),0,R(30)); Ju['root'].location[2]=.04*abs(g)
        q=ease(t/DUR); camset(LV((-.9,-.5,1.9),(-.85,-.3,1.9),q),hp(Ju,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['COPY']=COPY_
def PUTTAR_():
    hands,W,Sa,Ju,bn=street(crowd=0); gb=global_banner()
    def upd(t):
        upd_walkers(W,t+24); stand(Sa,t); blink(Sa,t); stand(Ju,t); blink(Ju,t); facep(Sa,(-.6,2.9)); talk(Sa,t,*ln(176,183),rest='grin'); laugh(Sa,t,.7)
        g=math.sin(t*5); Sa['arm'][1].rotation_euler=(R(-70-20*g),0,R(-30)); Sa['arm'][-1].rotation_euler=(R(-20),0,R(40)); Sa['root'].rotation_euler[1]=R(3*g)
        q=ease(t/DUR); camset(LV((.75,-.7,1.95),(.7,-.95,1.95),q),hp(Sa,-.08),36,2.8)
    return dict(upd=upd)
SHOTS['PUTTAR']=PUTTAR_
# ================================================================ SCENE 4 — the buyer
def BUYER_():
    hands,W=bz_set(crowd=12,seed=13); Bu=mk(BUYER,-9,-.6,-90,'buyer'); label('FOREIGN BUYER',(0,0,0),99)
    lb=label('ACTUAL FOREIGN BUYER',(-3,-.6,2.9),1.0,size=.2,col='#1B1F33',bg='#DFEBFF')
    lookers=[mk(c,x,y,rz,'lk%d'%i) for i,(c,x,y,rz) in enumerate(zip(crowd_cast(3,4),(-1.5,1.2,2.8),(2.6,-2.6,2.4),(200,330,190)))]
    def upd(t):
        upd_walkers(W,t+30); walk_path(Bu,[(-8.5,-.6),(-1.2,-.2),(.2,2.2)],t,0,DUR-.2,step=.55); blink(Bu,t); face(Bu,mouth='smile')
        lb.location=(Bu['root'].location[0],Bu['root'].location[1],2.95)
        for H in lookers: stand(H,t); blink(H,t); look_at(H,hp(Bu),.9); face(H,mouth='O',brow=.06)
        q=ease(t/DUR); camset(LV((-5,-2.9,1.5),(-1.5,-2.9,1.6),q),hp(Bu,-.25),26,8)
    return dict(upd=upd)
SHOTS['BUYER']=BUYER_
def shop2():
    fan,Ra,Ju=shop_set(); Bu=mk(BUYER,-1.2,.5,160,'buyer'); rack=empty((-2.2,.6,0)); sh=three_shirts(rack,1.0); return fan,Ra,Ju,Bu,sh
def TENK_():
    fan,Ra,Ju,Bu,sh=shop2(); b=bubble('10,000 PIECES, PLEASE',(-1.2,.5,2.95),1.0,size=.2,col='#1B1F33',bg='#DFEBFF')
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Bu,(-2.2,.6),1-tl(t,.8,1.2),cam=(0,1.9)); face(Bu,mouth='smile' if t<1.0 else 'o',brow=.03); arm_to(Bu,-1,(-2.0,.6,1.3),tl(t,.1,.4)*(1-tl(t,1.0,1.3)),base=(-30,0,0))
        mouth_talk(Bu,t,1.0,3.4); facep(Ju,(-1.2,.5)); face(Ju,mouth='O',brow=.07,brow_r=18)
        q=ease(t/DUR); camset(LV((-2.9,-1.3,1.85),(-2.7,-1.1,1.85),q),(-1.4,.6,1.7),26,8)
    return dict(upd=upd)
SHOTS['TENK']=TENK_
def CELEB_():
    fan,Ra,Ju,Bu,sh=shop2(); sparkles((1.3,.35,2.2),.8,.1,DUR,n=24,size=.03)
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); face(Ju,mouth='grin',brow=.07,eyes=.5); k=tl(t,0,.3); Ju['arm'][1].rotation_euler=(R(-170*k),0,R(-10)); Ju['arm'][-1].rotation_euler=(R(-170*k),0,R(10))
        Ju['root'].location[2]=.25*abs(math.sin(t*7)); Ju['root'].rotation_euler[2]=R(330)
        q=ease(t/DUR); camset(LV((1.0,-1.6,1.6),(.95,-1.35,1.6),q),hp(Ju,-.35),30,4)
    return dict(upd=upd)
SHOTS['CELEB']=CELEB_
def DANCE_():
    fan,Ra,Ju,Bu,sh=shop2()
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); Ju['root'].location=(.4,1.25,.97); Ju['root'].rotation_euler[2]=R(0); dance(Ju,t); face(Ju,mouth='grin',brow=.07,eyes=.5)
        Ra['root'].location=(1.6,2.0,0); facep(Ra,(.4,1.25)); face(Ra,mouth='flat',brow=-.05,brow_r=-15); facep(Bu,(.4,1.25)); face(Bu,mouth='O',brow=.06)
        q=ease(t/DUR); camset(LV((.2,-2.4,1.7),(.25,-2.0,1.8),q),(.4,1.3,2.2),26,8)
    return dict(upd=upd)
SHOTS['DANCE']=DANCE_
def MOTHER_():
    fan,Ra,Ju,Bu,sh=shop2(); ph=phone(Ju,-1,1.4); b=bubble('AMMI! AMMI!',(1.3,.35,2.5),.2,size=.17,col='#7A1F1F',bg='#FFE0E6')
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); Ju['root'].rotation_euler[2]=R(340); ear(Ju,-1,1); face(Ju,mouth='O' if (t*5)%2<1 else 'grin',brow=.07); Ju['root'].location[2]=.06*abs(math.sin(t*8))
        q=ease(t/DUR); camset(LV((1.05,-1.6,2.05),(1.05,-1.4,2.05),q),hp(Ju,-.1),34,2.8)
    return dict(upd=upd)
SHOTS['MOTHER']=MOTHER_
def CAR_():
    fan,Ra,Ju,Bu,sh=shop2(); ph=phone(Ju,1,1.4); b=bubble('NEW CAR: ORDERED',(1.3,.35,2.75),.5,size=.18,col='#1F4D3A',bg='#DFF5E1'); sparkles((1.3,.2,2.0),.4,.5,DUR,n=14,size=.025)
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); Ju['root'].rotation_euler[2]=R(340); hold_phone(Ju,1,1); Ju['head'].rotation_euler[0]=R(14); face(Ju,mouth='grin',brow=.06)
        g=math.sin(t*14); Ju['arm'][-1].rotation_euler=(R(-75+6*g),0,R(30))
        q=ease(t/DUR); camset(LV((.85,-1.0,1.8),(.9,-.85,1.82),q),hp(Ju,-.25),34,4)
    return dict(upd=upd)
SHOTS['CAR']=CAR_
def ORDER_():
    fan,Ra,Ju,Bu,sh=shop2()
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Ju,(0,1.95)); talk(Ju,t,*ln(227,230),shapes=('O','O','o','O')); face(Ju,brow=.08,brow_r=10); k=tl(t,0,.3)
        Ju['arm'][1].rotation_euler=(R(-170*k),0,R(-20)); Ju['arm'][-1].rotation_euler=(R(-170*k),0,R(20)); Ju['root'].location[2]=.1*abs(math.sin(t*7))
        q=ease(t/DUR); camset(LV((-.25,1.2,1.95),(-.2,1.0,1.95),q),hp(Ju,-.1),32,2.8)
    return dict(upd=upd)
SHOTS['ORDER']=ORDER_
def CALM_():
    fan,Ra,Ju,Bu,sh=shop2()
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Ra,(1.3,.35),.5,cam=(.5,-1)); face(Ra,mouth='flat',brow=-.01,eyes=.6); k=tl(t,.3,1.2); Ra['arm'][1].rotation_euler=(R(-40*k),0,R(-40*k)); Ra['arm'][-1].rotation_euler=(R(-40*k),0,R(40*k))
        q=ease(t/DUR); camset(LV((.5,-.6,1.95),(.45,-.3,1.95),q),hp(Ra,-.1),36,2.8)
    return dict(upd=upd)
SHOTS['CALM']=CALM_
def KAPRA_():
    fan,Ra,Ju,Bu,sh=shop2()
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Ra,(1.3,.35),.5,cam=(.5,-1)); talk(Ra,t,*ln(237,239)); face(Ra,brow=-.02,brow_r=-6,eyes=.7); Ra['arm'][1].rotation_euler=(R(-40),0,R(-40)); Ra['arm'][-1].rotation_euler=(R(-40),0,R(40))
        camset((.45,-.1,1.95),hp(Ra,-.03),46,2.8)
    return dict(upd=upd)
SHOTS['KAPRA']=KAPRA_
def SILENCE_():
    fan,Ra,Ju,Bu,sh=shop2(); fan_st=[0]
    def upd(t):
        sidle(Ra,Ju,t,None); stand(Bu,t); blink(Bu,t); fan.rotation_euler[2]=R(400)*(1-math.exp(-t*1.4))/1.4+R(60)
        face(Ju,mouth='flat',brow=.03,eyes=1.0); Ju['arm'][1].rotation_euler=(R(-170),0,R(-20)); Ju['arm'][-1].rotation_euler=(R(-170),0,R(20)); facep(Ju,(0,1.95))
        facep(Bu,(1.3,.35)); face(Bu,mouth='flat',brow=.04); face(Ra,mouth='flat',eyes=.6)
        q=ease(t/DUR); camset(LV((-.2,-2.6,2.0),(-.2,-2.75,2.05),q),(.2,1.0,1.8),24,8)
    return dict(upd=upd)
SHOTS['SILENCE']=SILENCE_
# ================================================================ SCENE 5 — the mill
def ml_set():
    beaters=mill_set(); B.done('mill'); setup_interior('day',room=(0,0,6.0),res=PCT,samples=SAMPLES,shadow_dist=22); point((0,-8,4.5),350,(1,.97,.9),3.0,False); point((0,2,4.5),350,(1,.97,.9),3.0,False)
    Mu=mk(MUKHTAR,5.6,-9.2,200,'mukhtar'); Ju=mk(JUNAID,3.7,-11.3,20,'junaid'); return beaters,Mu,Ju
def bt(beaters,t):
    for i,b in enumerate(beaters): b.location[1]=.05+.25*abs(math.sin(t*9+i*.7))
def MILLRUN_():
    beaters,Mu,Ju=ml_set()
    def upd(t):
        bt(beaters,t); stand(Mu,t); blink(Mu,t); walk_path(Ju,[(1.0,-16),(3.6,-11.2)],t,0,DUR-.2,step=.7,run_=True); blink(Ju,t); face(Ju,mouth='O',brow=.07,brow_r=18)
        q=ease(t/DUR); camset(LV((1.6,-8.2,2.0),(2.0,-8.8,1.9),q),hp(Ju,-.4),26,8)
    return dict(upd=upd)
SHOTS['MILLRUN']=MILLRUN_
def LOOMS_():
    beaters,Mu,Ju=ml_set(); label('LOUD.',(0,0,3.6),.5,size=.4,col='#7A1F1F')
    def upd(t):
        bt(beaters,t); stand(Mu,t); blink(Mu,t); stand(Ju,t); blink(Ju,t)
        q=ease(t/DUR); camset(LV((-8.5,-10,3.4),(-7.5,-9,3.0),q),(2,4,.8),22,16)
    return dict(upd=upd)
SHOTS['LOOMS']=LOOMS_
def OWNER_():
    beaters,Mu,Ju=ml_set(); label('LOUDER.',(5.6,-9.2,3.05),.4,size=.3,col='#7A1F1F'); label('MUKHTAR SAHAB',(5.6,-9.2,2.65),.15,size=.16,col='#1B1F33',bg='#DFEBFF')
    def upd(t):
        bt(beaters,t); stand(Mu,t); blink(Mu,t); stand(Ju,t); blink(Ju,t); Ju['root'].location=(3.7,-11.3,0); facep(Mu,(3.7,-11.3),.6,cam=(4.6,-13)); face(Mu,mouth='frown',brow=-.06,brow_r=-20)
        Mu['arm'][1].rotation_euler=(R(-30),0,R(-45)); Mu['arm'][-1].rotation_euler=(R(-30),0,R(45))
        q=ease(t/DUR); camset(LV((4.9,-12.6,1.4),(5.0,-12.2,1.5),q),hp(Mu,-.15),28,5.6)
    return dict(upd=upd)
SHOTS['OWNER']=OWNER_
def DAS_():
    beaters,Mu,Ju=ml_set()
    def upd(t):
        bt(beaters,t); stand(Mu,t); blink(Mu,t); stand(Ju,t); blink(Ju,t); Ju['root'].location=(3.7,-11.3,0); facep(Mu,(3.7,-11.3)); talk(Mu,t,*ln(261,265),shapes=('O','o','O','flat')); face(Mu,brow=-.06,brow_r=-20)
        arm_to(Mu,1,hp(Ju,-.6),tl(t,1.0,1.3),base=(-30,0,0)); Mu['root'].location[2]=0
        q=ease(t/DUR); camset(LV((4.4,-10.7,2.05),(4.45,-10.55,2.05),q),hp(Mu,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['DAS']=DAS_
def POCKET_():
    beaters,Mu,Ju=ml_set(); pk=in_hand(Ju,1,lambda e: pocket_stuff(e,1.6))
    def upd(t):
        bt(beaters,t); stand(Mu,t); blink(Mu,t); stand(Ju,t); blink(Ju,t); Ju['root'].location=(3.7,-11.3,0); facep(Ju,(3.3,-13.3)); k=tl(t,.3,.9)
        Ju['arm'][1].rotation_euler=(R(-15-55*k),0,R(-10)); Ju['head'].rotation_euler[0]=R(25*k); face(Ju,mouth='frown',brow=.06,brow_r=20); pk.scale=(k,k,k)
        q=ease(t/DUR); camset(LV((3.2,-13.4,1.8),(3.25,-13.2,1.8),q),hp(Ju,-.35),30,4)
    return dict(upd=upd)
SHOTS['POCKET']=POCKET_
def RUPEES_():
    beaters,Mu,Ju=ml_set(); pk=in_hand(Ju,1,lambda e: pocket_stuff(e,1.6)); label('RS. 40',(3.7,-11.3,2.75),.1,size=.2,col='#7A3A10'); label('+ BIRYANI RECEIPT',(3.7,-11.3,2.45),1.7,size=.15)
    def upd(t):
        bt(beaters,t); stand(Mu,t); blink(Mu,t); stand(Ju,t); blink(Ju,t); Ju['root'].location=(3.7,-11.3,0); facep(Ju,(3.3,-13.3)); Ju['arm'][1].rotation_euler=(R(-70),0,R(-10)); Ju['head'].rotation_euler[0]=R(25)
        face(Ju,mouth='frown',brow=.06,brow_r=22)
        q=ease(t/DUR); camset(LV((3.45,-12.9,1.95),(3.5,-12.75,1.95),q),(3.7,-11.4,1.55),28,2.8)
    return dict(upd=upd)
SHOTS['RUPEES']=RUPEES_
# ================================================================ FINAL
def BACK_():
    hands,W=bz_set(crowd=8,seed=15); bn=ifg_banner(); Ju=mk(JUNAID,-6,.8,-90,'junaid')
    def upd(t):
        upd_walkers(W,t+40); walk_path(Ju,[(-6,.8),(-.3,1.6),(0,3.2)],t,0,DUR-.3,step=.45); blink(Ju,t); face(Ju,mouth='frown',brow=.04,eyes=.6); Ju['head'].rotation_euler[0]=R(12)
        q=ease(t/DUR); camset(LV((-4.5,-2.2,1.6),(-1.6,-2.0,1.7),q),(hp(Ju)[0],hp(Ju)[1],1.6),26,8)
    return dict(upd=upd)
SHOTS['BACK']=BACK_
def ADVANCE_():
    fan,Ra,Ju,Bu,sh=shop2()
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Ju,(0,1.95)); talk(Ju,t,*ln(289,294)); face(Ju,brow=.03,brow_r=-8,eyes=.8); Ju['head'].rotation_euler[0]=R(6)
        q=ease(t/DUR); camset(LV((-.25,1.15,1.95),(-.2,1.0,1.95),q),hp(Ju,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['ADVANCE']=ADVANCE_
def SMILE_():
    fan,Ra,Ju,Bu,sh=shop2(); sparkles(hp(Ra,0),.5,.8,DUR,n=16,size=.025); label('FIRST SMILE IN 30 YEARS',(0,1.95,2.7),.9,size=.17)
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Ra,(1.3,.35),.5,cam=(.5,-1)); k=tl(t,.4,1.4); face(Ra,mouth='smile' if k>.5 else 'flat',brow=.03*k,eyes=.6+.3*k)
        q=ease(t/DUR); camset(LV((.5,-.5,1.95),(.47,-.2,1.95),q),hp(Ra,-.05),42,2.8)
    return dict(upd=upd)
SHOTS['SMILE']=SMILE_
def PUTTARF_():
    fan,Ra,Ju,Bu,sh=shop2()
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); Ra['root'].location=(1.1,1.6,0); facep(Ra,(1.3,.35)); talk(Ra,t,*ln(305,312),rest='smile'); face(Ra,brow=.03)
        arm_to(Ra,-1,(1.25,.45,1.75),tl(t,.3,.8),base=(-30,0,0)); facep(Ju,(1.1,1.6)); face(Ju,mouth='smile',brow=.04)
        q=ease(t/DUR); camset(LV((2.6,.2,1.9),(2.4,.3,1.9),q),(1.2,1.0,1.8),30,4)
    return dict(upd=upd)
SHOTS['PUTTARF']=PUTTARF_
def DISCOUNT_():
    fan,Ra,Ju,Bu,sh=shop2(); b=bubble('DISCOUNT?',(-1.2,.5,2.85),.3,size=.24,col='#1B1F33',bg='#DFEBFF')
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Bu,(1.3,.35),.6,cam=(-1.5,-1.0)); mouth_talk(Bu,t,.2,1.6); face(Bu,brow=.05,brow_r=8); Bu['arm'][1].rotation_euler=(R(-60),0,R(-30))
        q=ease(t/DUR); camset(LV((-1.8,-1.5,2.0),(-1.75,-1.3,2.0),q),hp(Bu,-.15),32,2.8)
    return dict(upd=upd)
SHOTS['DISCOUNT']=DISCOUNT_
def REPLY_():
    fan,Ra,Ju,Bu,sh=shop2()
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Ju,(-1.2,.5),.5,cam=(1.6,-1.5)); face(Ju,mouth='smile',brow=-.02,brow_r=-10,eyes=.75); k=tl(t,.4,1.2); shk(Ju,k)
        q=ease(t/DUR); camset(LV((1.6,-1.1,1.9),(1.55,-.9,1.92),q),hp(Ju,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['REPLY']=REPLY_
def CHARGES_():
    fan,Ra,Ju,Bu,sh=shop2(); cards=[]
    for i,(txt,t0) in enumerate((('DISCOUNT: ALAG',.1),('DELIVERY: ALAG',1.55),('PACKING: ALAG',2.65),('BREATHING: ALAG',4.0))):
        cards.append(label(txt,(.25,-.2,2.75-.33*i),t0,size=.16,col='#7A1F1F',bg='#FFF3B0'))
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); shk(Ju,1); facep(Ju,(-1.2,.5),.4,cam=(.6,-2.6)); talk(Ju,t,*ln(323,337),rate=10); face(Ju,brow=.03,brow_r=-6); gest(Ju,t,1,1.3,11,-80); gest(Ju,t+.5,-1,1.0,11,-60)
        facep(Bu,(1.3,.35)); face(Bu,mouth='O',brow=.07,brow_r=16)
        q=ease(t/DUR); camset(LV((.4,-2.8,1.85),(.4,-2.4,1.85),q),(.4,.3,1.85),28,8)
    return dict(upd=upd)
SHOTS['CHARGES']=CHARGES_
def PAYS_():
    fan,Ra,Ju,Bu,sh=shop2(); stacks=[]
    for k in range(5):
        e=empty((-.6+.3*k,1.25,1.0)); cash(e,2.0,4); e.scale=(0,0,0); stacks.append((e,.3+.3*k))
    def upd(t):
        sidle(Ra,Ju,t,fan); stand(Bu,t); blink(Bu,t); facep(Bu,(0,1.25)); arm_to(Bu,1,(0,1.2,1.1),.6+.4*abs(math.sin(t*4)),base=(-30,0,0)); face(Bu,mouth='smile')
        for e,t0 in stacks: k=pop(t-t0) if t>t0 else 0; e.scale=(k,k,k)
        face(Ra,mouth='grin',brow=.04); face(Ju,mouth='grin',brow=.07); Ju['root'].location[2]=.1*abs(math.sin(t*6))
        q=ease(t/DUR); camset(LV((.2,-1.7,2.4),(.15,-1.4,2.3),q),(0,1.0,1.2),28,8)
    return dict(upd=upd)
SHOTS['PAYS']=PAYS_
def FAINT_():
    hands,W,Sa,Ju,bn=street(seed=17); gb=global_banner(); Sa['root'].location=(.4,-2.9,0)
    def upd(t):
        upd_walkers(W,t+50); blink(Sa,t); stand(Ju,t); blink(Ju,t); k=ease_in(tl(t,.5,1.1)) if t<1.1 else 1; stand(Sa,t) if k<.05 else None
        Sa['root'].rotation_euler=(R(-86*k),0,R(180)); Sa['root'].location[2]=.12*k; face(Sa,mouth='O',brow=.07,eyes=1-k*.9); Sa['arm'][1].rotation_euler=(R(-150*k),0,R(-30)); Sa['arm'][-1].rotation_euler=(R(-150*k),0,R(30))
        q=ease(t/DUR); camset(LV((1.8,-.2,1.6),(1.6,-.5,1.5),q),(.4,-3.6,1.1),26,8)
    return dict(upd=upd)
SHOTS['FAINT']=FAINT_
W_=json.load(open(LH+'/audio/words.json'))
