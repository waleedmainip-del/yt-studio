# Shots for "Everyone Wants a Lahori Baddie". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=140.0
SEQ=[('OPEN',0.0),('SELL',3.35),('MEET',8.1),('DREAM',9.35),('WARN',13.45),('LOVE',14.85),('INSTA',17.35),('BIO',20.15),('CHECK',23.2),('BAL',25.5),('INVEST',28.4),
     ('CHANGE',30.85),('SHADES',34.0),('CAR',36.08),('COFFEE',37.72),('LIT',39.85),('FRIEND',43.35),('AMAZING',46.12),('UDHAAR',49.1),('PAST',51.35),
     ('AGREED',53.42),('EARLY',55.68),('LATE',57.78),('STOOD',59.93),('HEY',61.55),('THANKS',64.05),('CUTE',66.88),('POINT',68.42),('MENU',71.0),('HERE',72.58),
     ('NICE',74.48),('BABE',76.28),('SOUL',78.8),('ASKCAR',80.78),('BMW',84.2),('LENT',87.2),('RANG',91.05),('CALLER',92.65),('OYE',93.7),('LOOKG',97.2),('LOOKH',99.27),
     ('YOURCAR',100.33),('SILENCE',102.7),('CONFESS',103.7),('STARE',110.05),('LAUGH',112.12),('PAGAL',114.0),('CONF2',117.43),('ACHA',118.88),('HSMILE',121.38),
     ('ADDED',122.6),('BILL',123.72),('CHECK2',126.15),('BAL2',127.68),('WAITER',129.75),('TOTAL',130.97),('WHISPER',133.53),('BLACK',137.45)]
def hide(o): o.scale=(0,0,0)
def tl(t,a,b): return ease((t-a)/max(1e-3,b-a))
def hand_loc(H,s=1): u=H['u']; return (s*.5*u,-.05*u,-2.08*u)
def in_hand(H,s,builder):
    e=empty(hand_loc(H,s),H['arm'][s]); builder(e); return e
def talk(H,t,g0,g1): mouth_talk(H,t,g0-T0,g1-T0)
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

# ---------------------------------------------------------------- hook: the park
def park_set(seed=1,n=5):
    park(); B.done('park'); setup_world('morning_s'); Bs=[]; r=random.Random(seed)
    for i,x in enumerate((-8,-4,0,4,8)[:n]):
        park_bench(x,2.7)
        for j,dx in enumerate((-.55,.55)):
            H=avatar_bd((x+dx,2.55,0),0,person(seed*50+i*2+j,young=True),name='boy%d%d'%(i,j)); ph=phone(H); Bs.append((H,ph))
    return Bs
def boys_upd(Bs,t,look=None):
    for i,(H,ph) in enumerate(Bs):
        seat(H,t+i); hold_phone(H,1); H['head'].rotation_euler[0]=R(16); face(H,mouth='smile' if i%3 else 'grin',brow=.04,eyes=1.1)
def OPEN_():
    Bs=park_set(); W=walkers(3,3,-30,30,(5.2,))
    for i,(H,ph) in enumerate(Bs): hearts(lambda t,ph=ph: ph.matrix_world.translation,.2+i*.17,3.6,5,seed=i,size=.9,rise=1.3)
    def upd(t):
        boys_upd(Bs,t); upd_walkers(W,t+3); q=ease(t/DUR); camset(LV((-9.5,-3.4,1.5),(-1.5,-3.0,1.6),q),LV((-6,2.5,1.5),(1.5,2.5,1.5),q),28,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def SELL_():
    Bs=park_set(2,3); H0,p0=Bs[2]; H1,p1=Bs[3]; rep=6.57-T0
    sg=empty((.0,-.2*H1['u'],6.1*H1['u']),H1['root']); obox((0,0,0),(.62,.02,.3),M('#F4F1EA',.6),.02,sg); text('FUTURE',(0,-.03,.1),(0,-1,0),.2,M('#C8372D',.5),ex=.005,parent=sg); text('FOR SALE',(0,-.03,-.13),(0,-1,0),.17,M('#16171C',.5),ex=.005,parent=sg)
    bubble('hey',(-.9,2.2,2.75),rep,size=.24,bg='#DFF5E1')
    def upd(t):
        boys_upd(Bs,t); k=tl(t,rep,rep+.2)
        for i,(H,ph) in enumerate(Bs[2:4]):
            if i==1: arms(H,-165,0,12,-165,0,-12)
        for H,ph in Bs[1:5]:
            if H is not H0: look_at(H,(-.9,2.2,2.6),k,maxyaw=80); face(H,mouth='O' if k>.5 else 'smile',eyes=1+.3*k,brow=.06*k)
        face(H0,mouth='grin',eyes=1+.2*k); q=ease(t/DUR); camset(LV((.6,-3.4,1.6),(.3,-2.9,1.65),q),(-.1,2.5,1.85),30,16)
    return dict(upd=upd)
SHOTS['SELL']=SELL_

# ---------------------------------------------------------------- the rooftop
def roof_set():
    rooftop(); B.done('roof'); setup_world('afternoon',shadow=40)
    Hm=avatar_bd((-1.2,.28,0),0,HAMZA_A,name='hamza'); Al=avatar_bd((.7,.9,0),-90,ALI,name='ali'); Sd=avatar_bd((.9,-.4,0),-110,SAAD,name='saad'); return Hm,Al,Sd
def friends_idle(Al,Sd,t,look=(-1.2,.28,1.7)):
    for i,H in enumerate((Al,Sd)): stand(H,t+i); blink(H,t+i); look_at(H,look,.8)
def MEET_():
    Hm,Al,Sd=roof_set()
    def upd(t):
        seat(Hm,t); friends_idle(Al,Sd,t); k=tl(t,.1,.4); Hm['arm'][1].rotation_euler=(R(-150*k),0,R(18+14*math.sin(t*11)*k)); face(Hm,mouth='grin',brow=.04)
        q=ease(t/DUR); camset(LV((-1.6,-3.3,1.55),(-1.5,-2.9,1.6),q),(-1.2,.28,1.5),34,5.6)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def DREAM_():
    Hm,Al,Sd=roof_set(); hide(Al['root']); hide(Sd['root'])
    hearts(lambda t: (-1.2,.1,2.4),.8,4.0,9,seed=4,size=1.3,rise=1.8)
    def upd(t):
        seat(Hm,t); Hm['head'].rotation_euler=(R(-22),R(5*math.sin(t*1.2)),R(-10)); face(Hm,mouth='smile',brow=.05,eyes=1.15)
        Hm['arm'][1].rotation_euler=(R(-40),0,R(-40)); Hm['arm'][-1].rotation_euler=(R(-40),0,R(40))
        q=ease(t/DUR); camset(LV((-.2,-2.2,1.0),(-.5,-2.0,1.1),q),(-1.2,.2,2.0),30,5.6)
    return dict(upd=upd)
SHOTS['DREAM']=DREAM_
def WARN_():
    Hm,Al,Sd=roof_set()
    def upd(t):
        seat(Hm,t); Hm['head'].rotation_euler=(R(-18),0,R(-10)); face(Hm,mouth='smile',eyes=1.1)
        for i,H in enumerate((Al,Sd)):
            stand(H,t+i); blink(H,t+i); H['head'].rotation_euler=(R(4),0,R(22*math.sin(t*9+i)));
            face(H,mouth='frown',brow=-.02,brow_r=-14)
        arms(Al,-50,0,-60,-50,0,60); Sd['arm'][1].rotation_euler=(R(-95),0,R(10+20*math.sin(t*9)))
        camset((-3.6,-1.9,1.75),(.5,.4,1.75),32,5.6)
    return dict(upd=upd)
SHOTS['WARN']=WARN_
def LOVE_():
    Hm,Al,Sd=roof_set(); hide(Al['root']); hide(Sd['root']); ph=phone(Hm)
    hearts(lambda t: (-1.2,-.1,2.3),.2,2.4,7,seed=6,size=1.0,rise=1.2)
    def upd(t):
        seat(Hm,t); hold_phone(Hm,1); look_at(Hm,ph.matrix_world.translation,.6); face(Hm,mouth='grin',brow=.06,eyes=1.3)
        q=ease(t/DUR); camset(LV((-.7,-1.7,1.8),(-.8,-1.4,1.85),q),(-1.2,.28,1.86),45,2.8)
    return dict(upd=upd)
SHOTS['LOVE']=LOVE_
def profile_ui(bio):
    ui_world()
    P=ui_panel(bg='#FFFFFF'); ui_text(P,'zoya.dha',-.95,1.9,.2,al='LEFT'); ui_box(P,0,1.68,2.2,.008,'#DDDDDD')
    ring=ocyl((-.62,-.03,1.15),.36,.01,ui_mat('#E0457B'),P,seg=28); ocyl((-.62,-.04,1.15),.32,.01,ui_mat('#F6DCC6'),P,seg=28)
    for (x_,z_,w_,h_) in ((-.62,1.34,.5,.18),(-.83,1.14,.1,.36),(-.41,1.14,.1,.36)): obox((x_,-.06,z_),(w_/2,.005,h_/2),ui_mat('#3A2418'),.03,P)
    for s in (-1,1): ocyl((-.62+s*.11,-.07,1.14),.035,.01,ui_mat('#2A1A12'),P,seg=12)
    obox((-.62,-.07,1.0),(.07,.005,.015),ui_mat('#C8455A'),.01,P)
    for i,(n_,l_) in enumerate((('248','posts'),('58.4K','followers'),('112','following'))): ui_text(P,n_,-.02+i*.48,1.24,.14); ui_text(P,l_,-.02+i*.48,1.06,.075,'#777777')
    ui_text(P,'Zoya',-.95,.62,.15,al='LEFT'); ui_text(P,'DHA, Lahore',-.95,.42,.11,'#555555','LEFT')
    b1=ui_text(P,"Don't text me",-.95,.16,.14,'#16171C','LEFT'); b2=ui_text(P,"if you're broke.",-.95,-.06,.14,'#C8372D','LEFT')
    ui_box(P,-.5,-.42,.95,.26,'#3897F0',.06); ui_text(P,'Follow',-.5,-.42,.11,'#FFFFFF'); ui_box(P,.55,-.42,.95,.26,'#EFEFEF',.06); ui_text(P,'Message',.55,-.42,.11)
    r=random.Random(5)
    for i in range(6): ui_box(P,-.73+(i%3)*.73,-1.05-(i//3)*.73,.7,.7,r.choice(['#F2C6D0','#C6DCF2','#F2E2C6','#D6C6F2','#C6F2DC','#F2D0A8']),.02)
    return P,b1,b2
def INSTA_():
    P,b1,b2=profile_ui(False); hide(b1); hide(b2)
    def upd(t): q=ease(t/DUR); ui_cam(.2,7.6-.9*q)
    return dict(upd=upd)
SHOTS['INSTA']=INSTA_
def BIO_():
    P,b1,b2=profile_ui(True)
    def upd(t):
        k1=pop(t-.25); k2=pop(t-1.0); b1.scale=(k1,k1,k1); b2.scale=(k2,k2,k2); q=ease(t/DUR); ui_cam(.45-.25*q,6.6-.9*q)
    return dict(upd=upd)
SHOTS['BIO']=BIO_
def CHECK_():
    Hm,Al,Sd=roof_set(); ph=phone(Hm)
    def upd(t):
        seat(Hm,t); friends_idle(Al,Sd,t); hold_phone(Hm,1); look_at(Hm,ph.matrix_world.translation,.8); k=tl(t,.5,.9)
        Hm['arm'][-1].rotation_euler=(R(-95),0,R(40)); face(Hm,mouth='flat' if t<1.4 else 'frown',brow=.03,brow_r=10*k,eyes=1.0)
        camset((-2.9,-1.7,1.9),(-1.2,.2,1.55),38,4.0)
    return dict(upd=upd)
SHOTS['CHECK']=CHECK_
def bank_ui(still=False):
    ui_world()
    P=ui_panel(bg='#0E2A4A'); ui_text(P,'MERA BANK',0,1.85,.17,'#FFFFFF'); ui_box(P,0,.55,1.9,1.5,'#16406E',.1); ui_text(P,'Available balance',0,1.0,.11,'#A8C4E6')
    amt=ui_text(P,'Rs 847',0,.52,.42,'#FF5A4A'); ui_text(P,'Savings account',0,.05,.09,'#A8C4E6')
    for i,l_ in enumerate(('Send','Pay bills','Top up')): ui_box(P,-.66+i*.66,-.75,.52,.52,'#1D5A9A',.08); ui_text(P,l_,-.66+i*.66,-1.15,.075,'#FFFFFF')
    note=ui_text(P,'Low balance!',0,-1.65,.13,'#FFC83A')
    return P,amt,note
def BAL_():
    P,amt,note=bank_ui()
    def upd(t):
        k=pop(t-.25); amt.scale=(k,k,k); n=1 if (t>1.3 and int(t*4)%2==0) else (1 if t>2.2 else 0); note.scale=(n,n,n); q=ease(t/DUR); ui_cam(.2,7.2-1.3*q)
    return dict(upd=upd)
SHOTS['BAL']=BAL_
def INVEST_():
    Hm,Al,Sd=roof_set(); Hm['root'].location=(-1.0,-.5,0)
    def upd(t):
        stand(Hm,t); blink(Hm,t); talk(Hm,t,28.48,30.75); face(Hm,brow=-.03,brow_r=-16,eyes=.95); k=tl(t,.1,.4); Hm['arm'][1].rotation_euler=(R(-150*k),0,R(10)); Hm['root'].rotation_euler[2]=R(40)
        friends_idle(Al,Sd,t,look=(-1.0,-.5,1.8)); Al['arm'][1].rotation_euler=(R(-150*tl(t,1.2,1.6)),0,R(-50)); Al['head'].rotation_euler[0]=R(20*tl(t,1.2,1.6)); face(Sd,mouth='O',brow=.05)
        camset((-.2,-3.6,1.6),(-.1,.1,1.75),30,5.6)
    return dict(upd=upd)
SHOTS['INVEST']=INVEST_

# ---------------------------------------------------------------- the boulevard
def strip_set(seed=1,n=8):
    strip(); B.done('strip'); setup_world('morning_s'); W=walkers(n,seed,10,50,(-6.0,-6.6),z=.16); r=random.Random(seed); Vs=[]
    for i,(x,y,rz) in enumerate(((18,3.7,0),(44,3.7,0),(24,-3.7,180),(40,-3.7,180))):
        V=car((x,y,0),rz,['#C9CED8','#8A1F2A','#1F3A5A','#3A3D47'][i],seed*9+i); V['root'].scale=(1.15,1.15,1.15); Vs.append(V)
    return W
def CHANGE_():
    W=strip_set(2,6); A=avatar_bd((26,5.9,.16),90,HAMZA_A,name='hamzaA'); Bv=avatar_bd((29.7,6.7,.16),180,HAMZA_B,name='hamzaB'); sw=1.25
    sparkles((29.7,6.6,1.6),.7,sw-.1,sw+.5,26,.06,5,.5)
    def upd(t):
        upd_walkers(W,t+10)
        if t<sw: walk_path(A,[(26.6,5.9),(29.0,6.0),(29.7,6.75)],t,-.2,sw,step=.5,ease_out_=.05); Bv['root'].scale=(0,0,0); blink(A,t)
        else:
            A['root'].scale=(0,0,0); Bv['root'].scale=(1,1,1)
            if t<sw+1.0: walk_path(Bv,[(29.7,6.75),(30.3,5.75)],t,sw,sw+1.0,step=.5)
            else: stand(Bv,t); Bv['root'].rotation_euler[2]=R(lerp_angle(150,10,tl(t,sw+1.0,sw+1.3))); k=tl(t,sw+1.2,sw+1.5); arms(Bv,-20*k,0,-55*k,-20*k,0,55*k); face(Bv,mouth='smirk',brow=-.02)
        q=ease(t/DUR); camset(LV((30.6,1.2,1.5),(30.5,2.2,1.6),q),(29.6,6.3,1.7),28,16)
    return dict(upd=upd)
SHOTS['CHANGE']=CHANGE_
def SHADES_():
    W=strip_set(2,4); Hm=avatar_bd((30.3,5.75,.16),8,HAMZA_B,name='hamza'); sh=Hm['props']['shades']; u=Hm['u']
    tg=empty((.75*u,-.66*u,.5*u),sh); obox((0,0,-.12),(.11,.006,.075),M('#F4F1EA',.6),.01,tg); text('Rs 25,000',(0,-.012,-.12),(0,-1,0),.045,M('#C8372D',.5),ex=.002,parent=tg); obox((0,0,-.02),(.004,.004,.05),M('#16171C',.5),0,tg)
    def upd(t):
        upd_walkers(W,t+14); stand(Hm,t); k=ease(tl(t,.35,.9)); sh.location=(0,.12*u*(1-k),.62*u*(1-k)-.0); sh.rotation_euler=(R(-28*(1-k)),0,0)
        arm_to(Hm,1,Hm['head'].matrix_world@Vector((.6*u,-.7*u,.7*u)),1-tl(t,1.0,1.4),base=(0,0,0)); face(Hm,mouth='smirk',brow=-.02); tg.rotation_euler=(0,R(8*math.sin(t*5)),0)
        q=ease(t/DUR); camset(LV((30.5,3.9,1.95),(30.5,4.3,1.98),q),(30.3,5.75,2.02),50,2.8)
    return dict(upd=upd)
SHOTS['SHADES']=SHADES_
def CAR_():
    W=strip_set(3,4); V=car((31.0,3.75,0),0,'#F4F5FA',77); V['root'].scale=(1.15,1.15,1.15)
    Hm=avatar_bd((29.2,2.6,0),-20,HAMZA_B,name='hamza'); Cz=avatar_bd((32.3,1.7,0),75,COUSIN,name='cousin'); ky=in_hand(Hm,1,lambda e: obox((0,-.05,.03),(.03,.01,.07),M('#C9CED8',.3,metal=.9),.01,e))
    def upd(t):
        upd_walkers(W,t+17); stand(Hm,t); blink(Hm,t); face(Hm,mouth='grin'); Hm['arm'][1].rotation_euler=(R(-110),0,R(20+25*math.sin(t*10))); Hm['arm'][-1].rotation_euler=(R(-10),0,R(-35))
        stand(Cz,t); blink(Cz,t); face(Cz,mouth='frown',brow=-.03,brow_r=-20); Cz['arm'][1].rotation_euler=(R(-75),0,R(-10)); look_at(Cz,(29.2,2.6,1.9),.8)
        camset((29.6,-2.6,1.5),(30.6,3.0,1.5),28,16)
    return dict(upd=upd)
SHOTS['CAR']=CAR_
def big_cup(e,s=1.0):
    ocyl((0,-.06,.08*s),.07*s,.2*s,M('#F4F1EA',.5),e,rot=(0,0,0),seg=14,r2=.055*s); ocyl((0,-.06,.07*s),.073*s,.08*s,M('#6B4A2E',.7),e,rot=(0,0,0),seg=14); ocyl((0,-.06,.19*s),.075*s,.02*s,M('#2A2C34',.4),e,rot=(0,0,0),seg=14)
def coffee_set(seed=4):
    W=strip_set(seed,5); Hm=avatar_bd((35.0,5.7,.16),0,HAMZA_B,name='hamza'); cp=in_hand(Hm,1,lambda e: big_cup(e,1.5)); return W,Hm,cp
def COFFEE_():
    W,Hm,cp=coffee_set()
    def upd(t):
        upd_walkers(W,t+20); stand(Hm,t); blink(Hm,t); k=math.sin(pi*tl(t,.5,1.7)); Hm['arm'][1].rotation_euler=(R(-70-45*k),0,R(18*k)); Hm['head'].rotation_euler[0]=R(-10*k); face(Hm,mouth='o' if k>.6 else 'smirk')
        q=ease(t/DUR); camset(LV((35.6,3.2,1.75),(35.5,3.6,1.8),q),(35.0,5.7,1.8),40,4.0)
    return dict(upd=upd)
SHOTS['COFFEE']=COFFEE_
def LIT_():
    W,Hm,cp=coffee_set(5); lt=[42.55-T0-.9,42.55-T0-.45,42.55-T0]
    for i,(x,z,a) in enumerate(((34.1,2.75,10),(35.9,2.6,-8),(35.0,3.1,0))): b=bubble('literally',(x,5.6,z),lt[i],size=.16,bg='#FFF3B0'); b.rotation_euler[1]=R(a)
    def upd(t):
        upd_walkers(W,t+23); stand(Hm,t); blink(Hm,t); Hm['arm'][1].rotation_euler=(R(-70),0,R(10)); g=math.sin(t*7); Hm['arm'][-1].rotation_euler=(R(-70-20*g),0,R(-25-10*g)); talk(Hm,t,39.92,43.3); face(Hm,brow=.03)
        Hm['head'].rotation_euler=(0,R(4*g),R(8*math.sin(t*3)))
        camset((35.0,2.4,1.9),(35.0,5.7,2.15),30,5.6)
    return dict(upd=upd)
SHOTS['LIT']=LIT_
def bike_set(seed=6):
    W=strip_set(seed,5); Hm=avatar_bd((35.0,5.6,.16),25,HAMZA_B,name='hamza'); cp=in_hand(Hm,1,lambda e: big_cup(e,1.5))
    Bk=motorbike((36.8,3.9,0),180,'#C8372D'); Bk['root'].scale=(1.25,1.25,1.25); Bk['r']*=1.25
    Al=avatar_bd((0,0,0),-90,ALI,name='ali'); Al['root'].parent=Bk['root']; Al['root'].location=(-.15,0,.42); Al['root'].rotation_euler=(0,0,R(-90)); sit(Al,1,.55,legs=70); Al['z0']=0
    return W,Hm,Bk,Al
def bike_idle(Hm,Al,t):
    stand(Hm,t); blink(Hm,t); blink(Al,t); Hm['arm'][1].rotation_euler=(R(-70),0,R(10)); arms(Al,-70,0,6,-70,0,-6)
def FRIEND_():
    W,Hm,Bk,Al=bike_set(); stp=1.0
    def upd(t):
        upd_walkers(W,t+26); bike_idle(Hm,Al,t); x=36.8+9.0*(1-ease_out(min(1,t/stp)))**1.0*(1 if t<stp else 0); drive(Bk,x,3.9,180,44-x)
        Al['head'].rotation_euler[2]=R(70*tl(t,stp-.2,stp+.2)); talk(Al,t,44.35,46.05); k=tl(t,stp,stp+.3); Al['arm'][1].rotation_euler=(R(-70-60*k),0,R(6+20*k)); face(Al,brow=.04)
        look_at(Hm,(36.8,3.9,1.8),.8*tl(t,.3,.8)); face(Hm,mouth='smirk')
        camset((35.6,-.6,1.5),(36.0,4.8,1.6),26,16)
    return dict(upd=upd)
SHOTS['FRIEND']=FRIEND_
def AMAZING_():
    W,Hm,Bk,Al=bike_set(7)
    def upd(t):
        upd_walkers(W,t+29); bike_idle(Hm,Al,t); talk(Hm,t,46.2,49.0); face(Hm,brow=-.02,brow_r=-6); Hm['head'].rotation_euler=(R(-8),0,R(10)); k=tl(t,1.2,1.5); Hm['arm'][-1].rotation_euler=(R(-30*k),0,R(-45*k))
        q=ease(t/DUR); camset(LV((35.9,3.6,1.9),(35.8,3.8,1.92),q),(35.0,5.6,2.05),45,2.8)
    return dict(upd=upd)
SHOTS['AMAZING']=AMAZING_
def UDHAAR_():
    W,Hm,Bk,Al=bike_set(8)
    def upd(t):
        upd_walkers(W,t+32); bike_idle(Hm,Al,t); Al['head'].rotation_euler[2]=R(70); talk(Al,t,49.17,51.3); face(Al,brow=.06,eyes=1.25); p=root_mat(Hm)@Vector((0,0,3.6*Hm['u']))
        arm_to(Al,1,p,1.0,base=(0,0,0)); Al['root'].rotation_euler[1]=R(3*math.sin(t*14))
        camset((35.9,6.4,1.8),(36.75,3.9,1.75),36,4.0)
    return dict(upd=upd)
SHOTS['UDHAAR']=UDHAAR_
def PAST_():
    W,Hm,Bk,Al=bike_set(9); Hm['root'].location=(35.9,4.9,0.16)
    def upd(t):
        upd_walkers(W,t+35); bike_idle(Hm,Al,t); Al['head'].rotation_euler[2]=R(70); face(Al,mouth='grin'); Hm['root'].location=(35.9,4.9,.16); Hm['root'].rotation_euler[2]=R(45); Hm['root'].rotation_euler[0]=R(12)
        talk(Hm,t,51.42,53.3); face(Hm,brow=.05,brow_r=14); hp=Hm['head'].matrix_world@Vector((-.5*Hm['u'],-.9*Hm['u'],.4*Hm['u'])); arm_to(Hm,-1,hp,1.0,base=(0,0,0))
        Hm['head'].rotation_euler[2]=R(20*math.sin(t*5))
        camset((36.9,.4,1.6),(36.2,4.5,1.75),30,4.0)
    return dict(upd=upd)
SHOTS['PAST']=PAST_

# ---------------------------------------------------------------- the cafe date
def chat_ui():
    ui_world()
    P=ui_panel(bg='#F4F4F6'); ui_box(P,0,1.9,2.2,.6,'#FFFFFF',0); ui_text(P,'zoya.dha',0,1.9,.16)
    rows=[('hey',1,.9,.5),('coffee sometime?',1,.45,1.5),('seen',0,.12,.5)]
    for b_,me,z,w in rows[:2]: ui_box(P,1.0-w/2,z,w,.32,'#3897F0',.1); ui_text(P,b_,1.0-w/2,z,.11,'#FFFFFF')
    ui_text(P,'Seen',.8,.14,.07,'#888888')
    a=empty((0,0,0),P); ui_box(a,-.35,-.45,1.3,.34,'#E4E6EB',.1); ui_text(a,'fine. saturday 7.',-.35,-.45,.11)
    b=empty((0,0,0),P); ui_box(b,-.6,-.9,.8,.34,'#E4E6EB',.1); ui_text(b,"don't be late",-.6,-.9,.1)
    return P,a,b
def AGREED_():
    P,a,b=chat_ui()
    def upd(t):
        k=pop(t-.4); a.scale=(k,k,k); k2=pop(t-1.2); b.scale=(k2,k2,k2); q=ease(t/DUR); ui_cam(.4-.5*q,6.8-1.0*q)
    return dict(upd=upd)
SHOTS['AGREED']=AGREED_
HX,ZX,TY=-.95,.95,-.6
def cafe_set(seed=1,hamza=HAMZA_C,zoya=True,guests=True,stand_h=False):
    tabs=cafe(); B.done('cafe'); setup_world('dusk',shadow=40); cafe_lights(); G=[]; r=random.Random(seed)
    ch=cafe_chair(HX,TY,90); cz=cafe_chair(ZX,TY,-90)
    Hm=avatar_bd((HX,TY,0),90,hamza,name='hamza'); Zy=avatar_bd((ZX,TY,0),-90,ZOYA,name='zoya') if zoya else None
    if guests:
        for i,(x,y) in enumerate(tabs):
            for j,(dx,rz) in enumerate(((-.95,90),(.95,-90))):
                if r.random()<.75: g=avatar_bd((x+dx,y,0),rz,person(seed*40+i*2+j),name='g%d%d'%(i,j)); G.append(g)
    Wt=avatar_bd((-7.6,3.2,0),-60,WAITER,name='waiter')
    V=car((2.5,-8.2,-.15),0,'#101218',55); V['root'].scale=(1.2,1.2,1.2)
    return dict(Hm=Hm,Zy=Zy,G=G,Wt=Wt,ch=ch,cz=cz)
def cafe_idle(S,t,hs=True,zs=True,freeze=False):
    tt=0 if freeze else t
    for i,g in enumerate(S['G']): seat(g,tt+i); g['head'].rotation_euler[2]=R(8*math.sin(tt*.7+i)); arms(g,-35,0,0,-35,0,0)
    stand(S['Wt'],tt); blink(S['Wt'],tt)
    if hs: seat(S['Hm'],t); arms(S['Hm'],-38,0,-6,-38,0,6)
    if zs and S['Zy']: seat(S['Zy'],t); arms(S['Zy'],-38,0,-6,-38,0,6)
def stamp(body):
    e=empty((0,-1.2,3.25)); obox((0,.03,0),(.75,.02,.2),M('#16171C',.5,alpha=.85),.08,e); text(body,(0,0,0),(0,-1,0),.2,M('#FFE7B8',.4,emit=2.5),ex=.005,parent=e); fx.add(e,lambda o,t: face_cam(o)); return e
def _hp(H): r=H['root'].location; return Vector((r.x,r.y,r.z+4.75*H['u']))
ZH=lambda S: _hp(S['Zy'])
HH=lambda S: _hp(S['Hm'])
def cu_z(S,t,lens=45,d=0.0): p=ZH(S); camset((-.75-.1*d,TY-1.0+.08*d,p.z+.02),(p.x,p.y,p.z+.1),lens,2.8)
def cu_h(S,t,lens=45,d=0.0): p=HH(S); camset((.75+.1*d,TY-1.0+.08*d,p.z+.02),(p.x,p.y,p.z+.1),lens,2.8)
def two(S,t,q=0): camset((0,-3.9+.25*q,1.6),(0,TY,1.5),22,5.6)
def EARLY_():
    S=cafe_set(1,zoya=False); stamp('6:20 PM'); Hm=S['Hm']
    def upd(t):
        cafe_idle(S,t); k=math.sin(pi*tl(t,.5,1.8)); Hm['arm'][1].rotation_euler=(R(-38-50*k),0,R(-30*k)); Hm['head'].rotation_euler[0]=R(18*k); face(Hm,mouth='smile',brow=.03)
        Hm['leg'][1].rotation_euler[0]=R(-90+6*math.sin(t*16)); two(S,t,ease(t/DUR))
    return dict(upd=upd)
SHOTS['EARLY']=EARLY_
def LATE_():
    S=cafe_set(1); stamp('7:25 PM'); Hm,Zy=S['Hm'],S['Zy']
    def upd(t):
        cafe_idle(S,t,zs=False); walk_path(Zy,[(7.6,-3.3),(2.6,-3.3),(1.9,-1.4)],t,-2.6,DUR+.4,step=.5); blink(Zy,t); face(Zy,mouth='smirk'); Zy['arm'][-1].rotation_euler=(R(-25),0,R(-8))
        Hm['head'].rotation_euler[0]=R(25); face(Hm,mouth='frown',brow=.04,brow_r=12)
        camset((-3.2,-3.5,1.6),(1.6,-1.6,1.55),30,5.6)
    return dict(upd=upd)
SHOTS['LATE']=LATE_
def stand_pair(S,t,h_up=1.0):
    Hm,Zy=S['Hm'],S['Zy']; Zy['root'].location=(1.9,-1.4,.008); Zy['root'].rotation_euler=(0,0,R(-75)); stand(Zy,t); blink(Zy,t); Zy['arm'][-1].rotation_euler=(R(-25),0,R(-8))
    if h_up>=1: Hm['root'].location=(HX+.1,TY-.75,.008); stand(Hm,t); blink(Hm,t); Hm['root'].rotation_euler[2]=R(75)
def STOOD_():
    S=cafe_set(1); Hm,Zy=S['Hm'],S['Zy']
    def upd(t):
        cafe_idle(S,t,zs=False); stand_pair(S,t,0); k=tl(t,.15,.45)
        if k<1: sit(Hm,1-k,.58,legs=90); Hm['root'].location[1]=TY-.75*k
        else: Hm['root'].location=(HX+.1,TY-.75,.008); stand(Hm,t); Hm['root'].rotation_euler[2]=R(75)
        S['ch'].rotation_euler[0]=R(-80*tl(t,.2,.55)); S['ch'].location=(HX-.5*tl(t,.2,.55),TY,.25*tl(t,.2,.55))
        face(Hm,mouth='grin',brow=.06,eyes=1.2); Hm['arm'][1].rotation_euler=(R(-120*k),0,R(20+15*math.sin(t*12))); face(Zy,mouth='smirk'); two(S,t)
    return dict(upd=upd)
SHOTS['STOOD']=STOOD_
def zstand_cam(S,q=0): p=ZH(S); camset((.2,-2.9+.2*q,p.z),(p.x,p.y,p.z+.1),45,2.8)
def hstand_cam(S,q=0): p=HH(S); camset((1.0,-2.3+.2*q,p.z),(p.x,p.y,p.z+.1),45,2.8)
def HEY_():
    S=cafe_set(1); Zy=S['Zy']; sh=Zy['props']['shades']
    def upd(t):
        cafe_idle(S,t,False,False); stand_pair(S,t); talk(Zy,t,61.63,64.0); face(Zy,brow=.04,brow_r=-6); Zy['head'].rotation_euler=(R(4),R(-6),R(32+6*math.sin(t*2))); zstand_cam(S,ease(t/DUR))
    return dict(upd=upd)
SHOTS['HEY']=HEY_
def THANKS_():
    S=cafe_set(1); Hm=S['Hm']
    def upd(t):
        cafe_idle(S,t,False,False); stand_pair(S,t); talk(Hm,t,64.11,66.8); face(Hm,brow=.06,brow_r=10,eyes=1.15); Hm['arm'][-1].rotation_euler=(R(-140),0,R(-40)); Hm['head'].rotation_euler=(0,0,R(25+4*math.sin(t*9))); hstand_cam(S,ease(t/DUR))
    return dict(upd=upd)
SHOTS['THANKS']=THANKS_
def CUTE_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t,False,False); stand_pair(S,t); talk(Zy,t,66.95,68.35); face(Zy,brow=.0); Zy['head'].rotation_euler=(0,R(8),R(32)); zstand_cam(S,ease(t/DUR))
    return dict(upd=upd)
SHOTS['CUTE']=CUTE_
def POINT_():
    S=cafe_set(1); Hm,Zy=S['Hm'],S['Zy']
    def upd(t):
        cafe_idle(S,t,False,False); stand_pair(S,t); Hm['root'].rotation_euler[2]=R(lerp_angle(75,170,tl(t,.1,.5))); arm_to(Hm,1,(0,3.6,4.6),tl(t,.3,.7),base=(0,0,0)); face(Hm,mouth='grin',brow=.05)
        look_at(Zy,(0,3.6,4.5),tl(t,.6,1.0),maxyaw=80); face(Zy,mouth='flat')
        camset((1.0,-4.6,1.0),(0,1.6,3.6),19,16)
    return dict(upd=upd)
SHOTS['POINT']=POINT_
def menu(H):
    e=empty((0,-.75*H['u'],2.75*H['u']),H['root'],rot=(R(-25),0,0)); obox((0,0,0),(.2,.012,.28),M('#7A1F2E',.6),.01,e); text('MENU',(0,-.016,.14),(0,-1,0),.07,M('#E6C25A',.4,metal=.6),ex=.002,parent=e); return e
def MENU_():
    S=cafe_set(1); Zy=S['Zy']; mn=menu(Zy)
    def upd(t):
        cafe_idle(S,t); arms(Zy,-62,0,-14,-62,0,14); Zy['head'].rotation_euler=(R(24),0,R(10*math.sin(t*3))); face(Zy,mouth='flat',brow=.03,brow_r=-8); cu_z(S,t,38,ease(t/DUR))
    return dict(upd=upd)
SHOTS['MENU']=MENU_
def HERE_():
    S=cafe_set(1); Zy=S['Zy']; mn=menu(Zy)
    def upd(t):
        cafe_idle(S,t); arms(Zy,-50,0,-14,-50,0,14); k=tl(t,0,.25); Zy['head'].rotation_euler=(R(24*(1-k)),0,R(32*k)); talk(Zy,t,72.64,74.4); face(Zy,brow=.05,brow_r=-14,eyes=.85); cu_z(S,t,48)
    return dict(upd=upd)
SHOTS['HERE']=HERE_
def NICE_():
    S=cafe_set(1); Hm=S['Hm']
    def upd(t):
        cafe_idle(S,t); talk(Hm,t,74.55,76.2); face(Hm,brow=.06,brow_r=12,eyes=1.15); Hm['arm'][1].rotation_euler=(R(-80),0,R(30+10*math.sin(t*8))); Hm['head'].rotation_euler[2]=R(25); cu_h(S,t,45)
    return dict(upd=upd)
SHOTS['NICE']=NICE_
def BABE_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); talk(Zy,t,76.34,78.75); face(Zy,brow=.04,brow_r=10,eyes=.9); Zy['head'].rotation_euler=(0,R(-10),R(32)); Zy['arm'][1].rotation_euler=(R(-75),0,R(-25+8*math.sin(t*6))); cu_z(S,t,45,ease(t/DUR))
    return dict(upd=upd)
SHOTS['BABE']=BABE_
def ghost(H):
    u=H['u']; gm=M('#DFF1FF',.4,emit=1.4,alpha=.4); e=empty((0,0,0),H['root'])
    obox((0,0,3.0*u),(1.0*u,.5*u,1.0*u),gm,.07*u,e); obox((0,0,4.75*u),(.62*u,.62*u,.6*u),gm,.13*u,e)
    for s in (-1,1): obox((s*1.5*u,0,3.6*u),(.48*u,.48*u,.5*u),gm,.05*u,e,rot=(0,R(s*-70),0)); obox((s*.5*u,0,1.3*u),(.45*u,.45*u,.8*u),gm,.2*u,e)
    for s in (-1,1): ocyl((s*.25*u,-.63*u,4.85*u),.1*u,.01,M('#16171C',.5),e)
    ocyl((0,-.63*u,4.5*u),.1*u,.01,M('#16171C',.5),e,(1,1.4,1)); return e
def SOUL_():
    S=cafe_set(1); Hm=S['Hm']; g=ghost(Hm)
    def upd(t):
        cafe_idle(S,t); sit(Hm,1,.58); arms(Hm,-38,0,-6,-38,0,6); Hm['head'].rotation_euler=(R(-6),0,R(-22)); face(Hm,mouth='o',brow=.06,eyes=1.3); blink(Hm,t,force=False)
        k=ease(tl(t,.2,1.8)); g.location=(.1*math.sin(t*3),0,1.9*k); g.scale=(k**.3,k**.3,k**.3) if k>0 else (0,0,0); g.rotation_euler=(0,R(6*math.sin(t*2.4)),0)
        camset((.9,-3.1,1.9),(HX+.1,TY,2.5),28,5.6)
    return dict(upd=upd)
SHOTS['SOUL']=SOUL_
def ASKCAR_():
    S=cafe_set(1); Zy=S['Zy']; cp=in_hand(Zy,-1,lambda e: big_cup(e,1.0))
    def upd(t):
        cafe_idle(S,t); talk(Zy,t,82.48,84.1); face(Zy,brow=.03); k=math.sin(pi*tl(t,.1,1.4)); Zy['arm'][-1].rotation_euler=(R(-60-45*k),0,R(-14*k)); Zy['head'].rotation_euler=(R(-6*k),0,R(32))
        if t<1.6: two(S,t)
        else: cu_z(S,t,45)
    return dict(upd=upd)
SHOTS['ASKCAR']=ASKCAR_
def BMW_():
    S=cafe_set(1); Hm=S['Hm']; ky=in_hand(Hm,1,lambda e: (obox((0,-.05,.05),(.035,.012,.08),M('#16171C',.3,spec=.9),.01,e),ocyl((0,-.05,.16),.04,.008,M('#C9CED8',.3,metal=.9),e)))
    def upd(t):
        cafe_idle(S,t); talk(Hm,t,85.82,87.1); face(Hm,mouth='smirk' if t<85.82-T0 else None,brow=-.02,brow_r=-8); k=tl(t,.5,.9); Hm['arm'][1].rotation_euler=(R(-38-70*k),0,R(20*k)); ky.rotation_euler=(0,R(40*math.sin(t*9)*k),0); Hm['head'].rotation_euler=(R(-6),0,R(-32)); cu_h(S,t,42,ease(t/DUR))
    return dict(upd=upd)
SHOTS['BMW']=BMW_
def gate_set(car_=True):
    gate_street(); B.done('gate'); setup_world('day'); Al=avatar_bd((-.6,3.3,.12),-60,ALI,name='ali')
    V=None
    if car_: V=car((4.4,1.5,0),0,'#101218',55); V['root'].scale=(1.2,1.2,1.2)
    return Al,V
def LENT_():
    Al,V=gate_set(True); Hm=avatar_bd((.9,3.3,.12),110,HAMZA_B,name='hamza'); b=bubble('2 HOURS ONLY',(.25,3.2,2.95),1.3,size=.22,col='#C8372D',bg='#FFF3B0')
    ky=in_hand(Al,1,lambda e: obox((0,-.05,.05),(.035,.012,.08),M('#16171C',.3,spec=.9),.01,e))
    def upd(t):
        stand(Al,t); stand(Hm,t); blink(Al,t); blink(Hm,t); k=tl(t,.2,.6); Al['arm'][1].rotation_euler=(R(-75*k),0,R(-20*k)); Al['arm'][-1].rotation_euler=(R(-150*tl(t,1.1,1.4)),0,R(-10)); face(Al,mouth='flat',brow=-.03,brow_r=-18)
        Hm['arm'][1].rotation_euler=(R(-70*k),0,R(20*k)); face(Hm,mouth='grin',brow=.05); look_at(Al,(.9,3.3,1.9),.8); look_at(Hm,(-.6,3.3,1.7),.8)
        q=ease(t/DUR); camset(LV((.5,-1.3,1.6),(.4,-.9,1.65),q),(.15,3.3,1.9),28,16)
    return dict(upd=upd)
SHOTS['LENT']=LENT_
def RANG_():
    S=cafe_set(1); Hm=S['Hm']; ph=phone_obj(None,(-.25,TY-.1,1.02),1.5); ph.rotation_euler=(R(-90),0,R(30))
    def upd(t):
        cafe_idle(S,t); v=.012*math.sin(t*80)*(int(t*3)%2==0); ph.location=(-.25+v,TY-.1,1.02); ph.rotation_euler=(R(-90),0,R(30+3*math.sin(t*80)))
        look_at(Hm,(-.25,TY-.1,1.0),tl(t,.3,.6)); face(Hm,mouth='o',brow=.06,eyes=1.2); face(S['Zy'],mouth='flat'); look_at(S['Zy'],(-.25,TY-.1,1.0),tl(t,.5,.9))
        camset((.3,-2.3,1.75),(-.25,TY,1.15),32,4.0,focus=(-.25,TY-.1,1.0))
    return dict(upd=upd)
SHOTS['RANG']=RANG_
def CALLER_():
    ui_world()
    P=ui_panel(bg='#16171C'); ocyl((0,-.03,.9),.45,.01,ui_mat('#9AA4B0'),P,seg=28); ui_text(P,'A',0,.9,.42,'#FFFFFF'); ui_text(P,'ALI (BMW wala)',0,.1,.19,'#FFFFFF'); c=ui_text(P,'calling...',0,-.2,.12,'#A8A8B0')
    ocyl((-.55,-.03,-1.4),.26,.01,ui_mat('#E5484D'),P,seg=24); ocyl((.55,-.03,-1.4),.26,.01,ui_mat('#3FBF6A'),P,seg=24)
    def upd(t): P.rotation_euler=(0,R(1.2*math.sin(t*70)),0); ui_cam(0,6.4)
    return dict(upd=upd)
SHOTS['CALLER']=CALLER_
def OYE_():
    Al,V=gate_set(False); Am=avatar_bd((-1.8,3.6,.12),20,AMMI,name='ammi'); ph=phone(Al); Al['root'].rotation_euler[2]=R(0)
    def upd(t):
        stand(Al,t); stand(Am,t); blink(Am,t); talk(Al,t,93.76,97.15); face(Al,brow=-.04,brow_r=-24,eyes=1.2)
        ear=root_mat(Al)@Vector((1.15*Al['u'],-2.1*Al['u'],3.9*Al['u'])); arm_to(Al,1,ear,1.0,base=(0,0,0)); g=math.sin(t*11); Al['arm'][-1].rotation_euler=(R(-110-25*g),0,R(-40)); Al['root'].rotation_euler[1]=R(3*g)
        look_at(Am,(-.6,3.3,1.9),.8); face(Am,mouth='frown',brow=.04,brow_r=12); Am['arm'][1].rotation_euler=(R(-60),0,R(-30)); Am['leg'][1].rotation_euler[0]=R(8*abs(math.sin(t*7)))
        SHAKE[0]=.012; q=ease(t/DUR); camset(LV((-.4,-.6,1.7),(-.5,0,1.75),q),(-.9,3.4,1.75),32,5.6)
    return dict(upd=upd)
SHOTS['OYE']=OYE_
def phone_ear(H,s=1):
    ear=root_mat(H)@Vector((s*1.0*H['u'],-1.6*H['u'],4.1*H['u'])); arm_to(H,s,ear,1.0,base=(0,0,0))
def LOOKG_():
    S=cafe_set(1); Hm=S['Hm']; ph=phone(Hm,-1)
    def upd(t):
        cafe_idle(S,t); phone_ear(Hm,-1); k=ease(tl(t,.3,1.6)); Hm['head'].rotation_euler=(0,0,R(-42+42*k)); face(Hm,mouth='strain',brow=.06,brow_r=14,eyes=1.15); cu_h(S,t,45)
    return dict(upd=upd)
SHOTS['LOOKG']=LOOKG_
def LOOKH_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); arms(Zy,-50,0,-60,-50,0,60); face(Zy,mouth='flat',brow=.05,brow_r=-16,eyes=.8); Zy['head'].rotation_euler=(R(4),0,R(32)); cu_z(S,t,50,ease(t/DUR))
    return dict(upd=upd)
SHOTS['LOOKH']=LOOKH_
def YOURCAR_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); arms(Zy,-50,0,-60,-50,0,60); talk(Zy,t,100.39,102.6); face(Zy,brow=.05,brow_r=-16,eyes=.85); Zy['head'].rotation_euler=(R(4),R(-6),R(32)); Zy['root'].rotation_euler[0]=R(6*tl(t,.3,.8)); cu_z(S,t,50)
    return dict(upd=upd)
SHOTS['YOURCAR']=YOURCAR_
def SILENCE_():
    S=cafe_set(1); Hm,Zy=S['Hm'],S['Zy']; ph=phone(Hm,-1)
    def upd(t):
        cafe_idle(S,t,freeze=True); arms(Zy,-50,0,-60,-50,0,60); arms(Hm,-38,0,-6,-38,0,6); face(Hm,mouth='strain',brow=.06,brow_r=14,eyes=1.2); face(Zy,mouth='flat',brow=.05,brow_r=-16,eyes=.8)
        for g in S['G']: look_at(g,(0,TY,1.8),.9,maxyaw=85)
        q=ease(t/DUR); camset(LV((0,-3.1,2.7),(0,-2.9,2.5),q),(0,TY+.6,1.5),22,16)
    return dict(upd=upd)
SHOTS['SILENCE']=SILENCE_
def CONFESS_():
    S=cafe_set(1,hamza=HAMZA_B); Hm=S['Hm']; sh=Hm['props']['shades']; u=Hm['u']; t1,t2,t3=106.26-T0,107.35-T0,108.47-T0
    ky=obox((-.3,TY-.18,1.03),(.035,.08,.012),M('#16171C',.3,spec=.9),.01); cp=empty((-.15,TY+.22,1.0)); big_cup(cp,1.3); sh2=empty((-.38,TY+.05,1.03));
    for s in (-1,1): obox((s*.09,0,0),(.08,.055,.008),M('#0E0F14',.08,spec=1.0),.02,sh2)
    def upd(t):
        cafe_idle(S,t); talk(Hm,t,103.76,109.9); face(Hm,brow=.06,brow_r=16,eyes=.9); Hm['head'].rotation_euler=(R(18),0,R(-15+6*math.sin(t*2)))
        for o,ts in ((ky,t1),(sh2,t2),(cp,t3)):
            k=pop(t-ts); o.scale=(k,k,k)
        sh.scale=(0,0,0) if t>t2 else (1,1,1)
        r_=max([tl(t,ts-.2,ts)*(1-tl(t,ts,ts+.3)) for ts in (t1,t2,t3)]); Hm['arm'][1].rotation_euler=(R(-38-45*r_),0,R(15*r_))
        face(S['Zy'],mouth='flat',brow=.03,brow_r=-10)
        q=ease(t/DUR); camset(LV((.2,-2.9,2.2),(.1,-2.5,2.1),q),(-.25,TY,1.25),32,4.0)
    return dict(upd=upd)
SHOTS['CONFESS']=CONFESS_
def STARE_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); blink(Zy,t,force=False); face(Zy,mouth='flat',brow=.0,brow_r=-4,eyes=.95); Zy['head'].rotation_euler=(0,0,R(32)); cu_z(S,t,48+10*ease(t/DUR))
    return dict(upd=upd)
SHOTS['STARE']=STARE_
def laugh(Zy,t,k=1.0):
    b=abs(math.sin(t*13))*k; Zy['head'].rotation_euler=(R(-14*k+4*b),0,R(32)); Zy['root'].rotation_euler[0]=R(-4*k+3*b); face(Zy,mouth='grin',brow=.06,eyes=.7); Zy['arm'][1].rotation_euler=(R(-95),0,R(32))
def LAUGH_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); laugh(Zy,t,tl(t,.1,.4)); face(S['Hm'],mouth='o',brow=.06,brow_r=14)
        if t<.9: cu_z(S,t,48)
        else: two(S,t)
    return dict(upd=upd)
SHOTS['LAUGH']=LAUGH_
def PAGAL_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); talk(Zy,t,114.07,117.35); face(Zy,brow=.06,eyes=.9); g=math.sin(t*6); Zy['arm'][1].rotation_euler=(R(-80-10*g),0,R(-30+15*g)); Zy['head'].rotation_euler=(R(-4),R(5*g),R(32)); cu_z(S,t,44,ease(t/DUR))
    return dict(upd=upd)
SHOTS['PAGAL']=PAGAL_
def CONF2_():
    S=cafe_set(1); Hm=S['Hm']
    def upd(t):
        cafe_idle(S,t); face(Hm,mouth='o',brow=.06,brow_r=14,eyes=1.1); Hm['head'].rotation_euler=(0,R(12*tl(t,.2,.6)),R(-32)); cu_h(S,t,45)
    return dict(upd=upd)
SHOTS['CONF2']=CONF2_
def ACHA_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); talk(Zy,t,118.94,121.3); face(Zy,brow=.04,brow_r=6,eyes=1.0); Zy['head'].rotation_euler=(R(4),R(-8),R(32)); cu_z(S,t,50,ease(t/DUR))
    return dict(upd=upd)
SHOTS['ACHA']=ACHA_
def HSMILE_():
    S=cafe_set(1); Hm=S['Hm']; hearts(lambda t: HH(S)+Vector((0,-.2,.4)),.1,1.0,5,seed=9,size=.8,rise=.9)
    def upd(t):
        cafe_idle(S,t); face(Hm,mouth='grin',brow=.06,eyes=1.2); Hm['head'].rotation_euler=(0,0,R(-32)); cu_h(S,t,45)
    return dict(upd=upd)
SHOTS['HSMILE']=HSMILE_
def ADDED_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); k=tl(t,.1,.6); Zy['root'].rotation_euler[0]=R(8*k); face(Zy,mouth='smirk',brow=.03,brow_r=-10); Zy['head'].rotation_euler=(0,R(-8*k),R(32)); face(S['Hm'],mouth='grin'); two(S,t,ease(t/DUR))
    return dict(upd=upd)
SHOTS['ADDED']=ADDED_
def BILL_():
    S=cafe_set(1); Zy=S['Zy']
    def upd(t):
        cafe_idle(S,t); talk(Zy,t,123.79,126.1); face(Zy,brow=.05,brow_r=-10,eyes=.9); Zy['root'].rotation_euler[0]=R(8); p=HH(S); arm_to(Zy,1,(p.x,p.y,p.z-.5),tl(t,.9,1.2),base=(R(-38),0,R(-6))); Zy['head'].rotation_euler=(0,R(-8),R(32)); cu_z(S,t,46)
    return dict(upd=upd)
SHOTS['BILL']=BILL_
def CHECK2_():
    S=cafe_set(1); Hm=S['Hm']; ph=phone(Hm)
    def upd(t):
        cafe_idle(S,t); hp=root_mat(Hm)@Vector((.3*Hm['u'],-1.0*Hm['u'],2.6*Hm['u'])); arm_to(Hm,1,hp,1.0,base=(0,0,0)); Hm['head'].rotation_euler=(R(30),0,R(8)); face(Hm,mouth='strain',brow=.06,brow_r=16,eyes=1.1)
        p=HH(S); camset((.5,-2.0,1.5),(p.x+.1,p.y,p.z-.2),40,2.8)
    return dict(upd=upd)
SHOTS['CHECK2']=CHECK2_
def BAL2_():
    P,amt,note=bank_ui(); note.data.body='Still Rs 847.'
    def upd(t):
        s=1+.06*math.sin(t*14); amt.scale=(s,s,s); q=ease(t/DUR); ui_cam(.3,6.4-.7*q)
    return dict(upd=upd)
SHOTS['BAL2']=BAL2_
def folder(H):
    return in_hand(H,1,lambda e: (obox((0,-.1,.08),(.12,.02,.17),M('#16171C',.4),.01,e),obox((0,-.125,.08),(.09,.004,.13),M('#F4F1EA',.5),0,e)))
def WAITER_():
    S=cafe_set(1); Wt=S['Wt']; fd=folder(Wt)
    def upd(t):
        cafe_idle(S,t); walk_path(Wt,[(-6.5,-3.1),(-3.6,-2.6),(-2.2,-1.5)],t,-1.8,DUR,step=.5); blink(Wt,t); Wt['arm'][1].rotation_euler=(R(-75),0,R(8)); face(Wt,mouth='smile')
        face(S['Hm'],mouth='strain',brow=.06,brow_r=16); S['Hm']['head'].rotation_euler=(0,0,R(-60*tl(t,.4,.9))); face(S['Zy'],mouth='smirk'); two(S,t)
    return dict(upd=upd)
SHOTS['WAITER']=WAITER_
def TOTAL_():
    ui_world()
    P=ui_panel(w=2.0,h=3.6,bg='#FFFDF6'); ui_text(P,'CAFE LUMIERE',0,1.5,.17); ui_text(P,'DHA Phase 6, Lahore',0,1.28,.08,'#777777'); ui_box(P,0,1.12,1.8,.006,'#999999')
    items=[('Truffle pasta','4,200'),('Wagyu slider x2','6,400'),('Rose latte','1,450'),('Gold-leaf cake','3,900'),('Sparkling water','950'),('Service 10%','1,600')]
    for i,(a,b) in enumerate(items): ui_text(P,a,-.85,.88-i*.24,.09,'#333333','LEFT'); ui_text(P,b,.85,.88-i*.24,.09,'#333333','RIGHT')
    ui_box(P,0,-.62,1.8,.006,'#999999'); ui_text(P,'TOTAL',-.85,-.95,.17,'#16171C','LEFT'); tt=ui_text(P,'Rs 18,500',.85,-.95,.2,'#C8372D','RIGHT'); ui_text(P,'Thank you! Come again.',0,-1.45,.075,'#777777')
    def upd(t):
        s=1+.25*max(0,1-abs(t-2.0)*3) if t>1.6 else 1; tt.scale=(s,s,s); q=ease(t/DUR); ui_cam(L(.2,-.5,q),L(6.2,5.2,q))
    return dict(upd=upd)
SHOTS['TOTAL']=TOTAL_
def WHISPER_():
    S=cafe_set(1); Hm,Wt,Zy=S['Hm'],S['Wt'],S['Zy']; fd=folder(Wt)
    def upd(t):
        cafe_idle(S,t); Wt['root'].location=(-2.2,-1.5,.008); Wt['root'].rotation_euler=(R(8*tl(t,.5,1.2)),0,R(65)); Wt['arm'][1].rotation_euler=(R(-75),0,R(8)); look_at(Wt,HH(S),.8); face(Wt,mouth='o' if t>3.2 else 'smile',brow=.05)
        k=tl(t,.3,1.0); Hm['root'].rotation_euler[2]=R(90-105*k); Hm['head'].rotation_euler=(R(-18*k),0,R(-20*k)); talk(Hm,t,135.37,137.3); face(Hm,brow=.06,brow_r=18,eyes=.9)
        hp=Hm['head'].matrix_world@Vector((.55*Hm['u'],-.8*Hm['u'],.35*Hm['u'])); arm_to(Hm,1,hp,k,base=(R(-38),0,R(-6)))
        face(Zy,mouth='smirk'); Zy['head'].rotation_euler=(R(10),0,R(20))
        q=ease(t/DUR); camset(LV((.3,-3.5,1.75),(.1,-3.2,1.78),q),(-1.55,-1.1,1.8),34,4.0)
    return dict(upd=upd)
SHOTS['WHISPER']=WHISPER_
def BLACK_():
    ui_world()
    for o in bpy.data.objects:
        if o.type=='LIGHT': o.data.energy=0
    R_=empty((0,0,UIZ)); a=ui_text(R_,'THE LAHORI BADDIE',0,.45,.3,'#FFFFFF'); b=ui_text(R_,'EXPERIENCE',0,-.02,.42,'#FF4F7A')
    sk=empty((0,0,-.95),R_); ui_box(sk,0,.08,.6,.52,'#F4F1EA',.2); ui_box(sk,0,-.24,.34,.2,'#F4F1EA',.04)
    for s in (-1,1): ocyl((s*.14,-.04,.1),.09,.01,ui_mat('#000000'),sk,seg=16)
    for k in range(3): ui_box(sk,-.1+k*.1,-.25,.02,.16,'#000000',0)
    for o in (a,b,sk): o.scale=(0,0,0)
    def upd(t):
        for o,ts in ((a,.5),(b,.9),(sk,1.3)): k=pop(t-ts); o.scale=(k,k,k)
        ui_cam(-.1,7.5)
    return dict(upd=upd)
SHOTS['BLACK']=BLACK_
