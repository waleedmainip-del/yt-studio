# Shots for "The Punjabi Family". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=62.9
SEQ=[('OPEN', 0.0), ('ONEP', 1.07), ('MEETING', 5.21), ('MEET', 7.1), ('TELLS', 8.39), ('CANADA', 10.82), ('PAPER', 12.68), ('KYUN', 15.59), ('CAREER', 16.5), ('SAAF', 17.73), ('PACK', 20.18), ('CRY', 22.28), ('UNCLE', 24.28), ('ZAMEEN', 27.45), ('JOB', 29.3), ('AIRPORT', 31.75), ('ADVICE', 34.75), ('HATH', 36.61), ('BAGS', 38.39), ('IPHONE', 40.92), ('MEREY', 43.02), ('BOARD', 44.82), ('CALL', 47.1), ('BEDROOM', 49.64), ('FANQ', 51.74), ('CLOSES', 54.6), ('ABBA', 56.52), ('GRUMBLE', 59.66)]
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



# ================================================================ props + sets
def newspaper(e,s=1.0): obox((.05,-.15,.1),(.25*s,.01,.18*s),M('#E8E4DA',.8),.0,e,rot=(0,0,R(10))); text('DAWN?',(0,0,0),(0,-1,0),.001,M('#E8E4DA',.8),ex=0,parent=e) if False else None; [obox((.05,-.162,.18-.05*k),(.2*s,.002,.008),M('#5A5E66',.6),0,e,rot=(0,0,R(10))) for k in range(6)]
def foodbag(e,s=1.0,col='#C8372D'):
    obox((0,-.1,.1*s),(.14*s,.09*s,.15*s),M(col,.85,kind='fabric'),.03,e); obox((0,-.1,.28*s),(.06*s,.01,.04*s),M('#16171C',.6),0,e)
def lounge_set():
    lounge(); B.done('lounge'); setup_interior('day',room=(0,0,3.4),res=PCT,samples=SAMPLES,shadow_dist=18); point((0,-1.5,2.4),150,(1,.95,.88),1.0,False)
    F=dict(ab=mk(ABBA,-3.4,1.0,90,'abba'),da=mk(DADI,-.8,2.7,0,'dadi'),ch=mk(CHACHA,.85,2.7,0,'chacha'),am=mk(AMMI,3.2,-.1,180,'ammi'),ar=mk(ARSLAN,.3,.2,160,'arslan'))
    return F
def lidle(F,t,seated=('ab','da','ch')):
    for k in seated: sit(F[k],1,.46,legs=80); blink(F[k],t)
    F['ab']['root'].rotation_euler[2]=R(90); F['da']['root'].rotation_euler[2]=0; F['ch']['root'].rotation_euler[2]=0
    for k in ('am','ar'):
        if k not in seated: stand(F[k],t); blink(F[k],t)
# ================================================================ HOOK
def OPEN_():
    F=lounge_set(); F['am']['root'].location=(1.9,1.6,0)
    def upd(t):
        lidle(F,t)
        for i,k in enumerate(('ab','da','ch','am')):
            H=F[k]; mouth_talk(H,t,.0+.1*i,DUR,rate=9,rest='O'); gest(H,t+i,1,1.4,9); face(H,brow=.05)
        face(F['ar'],mouth='flat',brow=.05); F['ar']['head'].rotation_euler[2]=R(25*math.sin(t*3))
        q=ease(t/DUR); camset(LV((2.6,-2.4,2.8),(2.0,-1.8,2.2),q),(-.7,1.8,1.0),22,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def ONEP_():
    F=lounge_set(); Ch=F['ch']
    def upd(t):
        lidle(F,t,('ab','da')); stand(Ch,t); blink(Ch,t); Ch['root'].location=(.85,2.0,0); Ch['root'].rotation_euler[2]=R(-10); mouth_talk(Ch,t,0,DUR,rate=8,rest='grin'); face(Ch,brow=.05)
        g=math.sin(t*6); Ch['arm'][1].rotation_euler=(R(-140-20*g),0,R(20)); Ch['arm'][-1].rotation_euler=(R(-100+30*g),0,R(-30)); Ch['root'].location[2]=.05*abs(math.sin(t*5))
        for k in ('ab','da','ar'): look_at(F[k],hp(Ch),.6); face(F[k],mouth='flat',brow=.03)
        q=ease(t/DUR); camset(LV((1.8,-.6,1.9),(1.6,-.2,1.9),q),hp(Ch,-.3),32,5.6)
    return dict(upd=upd)
SHOTS['ONEP']=ONEP_
def MEETING_():
    F=lounge_set(); F['am']['root'].location=(1.9,1.6,0); title_card('FULL FAMILY MEETING',.15,(-.3,1.8,2.9),.24)
    def upd(t):
        lidle(F,t)
        for i,k in enumerate(('ab','da','ch','am')): H=F[k]; look_at(H,hp(F['ar']),.7); face(H,mouth='flat',brow=-.03,brow_r=-10); H['arm'][1].rotation_euler=(R(-30),0,R(-40))
        face(F['ar'],mouth='o',brow=.05)
        q=ease(t/DUR); camset(LV((2.4,-2.0,2.3),(2.1,-1.7,2.2),q),(-.6,1.6,1.3),24,16)
    return dict(upd=upd)
SHOTS['MEETING']=MEETING_
# ================================================================ SCENE 1
def MEET_():
    F=lounge_set(); Ar=F['ar']; label('ARSLAN',(.3,.2,3.0),.3,col='#1F3A6A',bg='#DFEBFF')
    def upd(t):
        lidle(F,t); Ar['root'].rotation_euler[2]=R(lerp_angle(160,10,tl(t,.1,.5))); face(Ar,mouth='grin'); Ar['arm'][1].rotation_euler=(R(-130*tl(t,.4,.7)),0,R(20))
        q=ease(t/DUR); camset(LV((.6,-2.2,1.85),(.5,-1.8,1.87),q),hp(Ar,-.2),35,4)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def TELLS_():
    F=lounge_set(); Ar=F['ar']
    def upd(t):
        lidle(F,t); Ar['root'].rotation_euler[2]=R(150); face(Ar,mouth='smile'); k=tl(t,.3,.6); Ar['arm'][1].rotation_euler=(R(-25*k),0,R(-40*k)); Ar['arm'][-1].rotation_euler=(R(-25*k),0,R(40*k))
        for k_ in ('ab','da','ch','am'): look_at(F[k_],hp(Ar),.7)
        q=ease(t/DUR); camset(LV((2.4,-1.6,1.9),(2.1,-1.3,1.9),q),(-.3,1.6,1.3),24,16)
    return dict(upd=upd)
SHOTS['TELLS']=TELLS_
def CANADA_():
    F=lounge_set(); Ar=F['ar']
    def upd(t):
        lidle(F,t); Ar['root'].rotation_euler[2]=R(205); talk(Ar,t,10.82,12.5); face(Ar,brow=.04); Ar['arm'][1].rotation_euler=(R(-40),0,R(-50)); Ar['arm'][-1].rotation_euler=(R(-40),0,R(50))
        q=ease(t/DUR); camset(LV((-.6,1.3,1.8),(-.5,1.1,1.82),q),hp(Ar,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['CANADA']=CANADA_
def abba_chair(F,t):
    Ab=F['ab']; sit(Ab,1,.46,legs=80); blink(Ab,t); Ab['root'].rotation_euler[2]=R(90); return Ab
def PAPER_():
    F=lounge_set(); np_=in_hand(F['ab'],1,lambda e: newspaper(e,2.4))
    def upd(t):
        lidle(F,t); Ab=abba_chair(F,t); k=ease(tl(t,.4,2.2)); Ab['arm'][1].rotation_euler=(R(-95+55*k),0,R(-25)); Ab['arm'][-1].rotation_euler=(R(-95+55*k),0,R(25))
        face(Ab,mouth='flat',brow=-.03*k,brow_r=-12*k,eyes=.85); Ab['head'].rotation_euler[2]=R(-15)
        q=ease(t/DUR); camset(LV((-1.6,1.1,1.6),(-1.8,1.0,1.6),q),hp(Ab,-.15),38,4)
    return dict(upd=upd)
SHOTS['PAPER']=PAPER_
def KYUN_():
    F=lounge_set(); np_=in_hand(F['ab'],1,lambda e: newspaper(e,2.4))
    def upd(t):
        lidle(F,t); Ab=abba_chair(F,t); Ab['arm'][1].rotation_euler=(R(-40),0,R(-25)); talk(Ab,t,15.59,16.1); face(Ab,brow=-.04,brow_r=-14,eyes=.8); Ab['head'].rotation_euler=(R(6),0,R(-20))
        camset((-1.7,.4,1.75),hp(Ab,-.03),45,2.8)
    return dict(upd=upd)
SHOTS['KYUN']=KYUN_
def CAREER_():
    F=lounge_set(); Ar=F['ar']
    def upd(t):
        lidle(F,t); Ar['root'].rotation_euler[2]=R(-110); talk(Ar,t,16.5,17.2); face(Ar,brow=.05,brow_r=10); Ar['arm'][1].rotation_euler=(R(-60),0,R(-20))
        q=ease(t/DUR); camset(LV((-1.6,-.6,1.85),(-1.5,-.5,1.86),q),hp(Ar,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['CAREER']=CAREER_
def SAAF_():
    F=lounge_set(); np_=in_hand(F['ab'],-1,lambda e: newspaper(e,2.4))
    def upd(t):
        lidle(F,t,('da','ch')); Ab=F['ab']; k=ease(tl(t,0,.35)); sit(Ab,1-k,.46,legs=80); blink(Ab,t); Ab['root'].rotation_euler[2]=R(90)
        talk(Ab,t,17.73,20.0,shapes=('O','o','O','flat')); face(Ab,brow=-.05,brow_r=-18); arm_to(Ab,1,hp(F['ar']),tl(t,.4,.7),base=(-40,0,0)); Ab['arm'][-1].rotation_euler=(R(-30),0,R(-20)); Ab['head'].rotation_euler[2]=R(-10)
        face(F['ar'],mouth='O',brow=.06)
        q=ease(t/DUR); camset(LV((-1.4,-.8,1.6),(-1.6,-.4,1.65),q),(-3.0,1.0,1.7),32,5.6)
    return dict(upd=upd)
SHOTS['SAAF']=SAAF_
# ================================================================ SCENE 2
def PACK_():
    F=lounge_set(); Am=F['am']; bags=[]
    for k in range(5):
        e=empty((3.0+.3*k-.6,.55+.15*(k%2),.82)); foodbag(e,1.6,['#C8372D','#2B5AA8','#F2C14E','#2B8A5A','#7448C2'][k]); e.scale=(0,0,0); bags.append((e,.2+.35*k))
    def upd(t):
        lidle(F,t); stand(Am,t); blink(Am,t); Am['root'].location=(3.4,-.25,0); Am['root'].rotation_euler[2]=0
        g=math.sin(t*9); Am['arm'][1].rotation_euler=(R(-55-15*g),0,R(-10)); Am['arm'][-1].rotation_euler=(R(-55+15*g),0,R(10)); face(Am,mouth='flat',brow=.04)
        for e,t0 in bags: k=pop(t-t0) if t>t0 else 0; e.scale=(k,k,k)
        q=ease(t/DUR); camset(LV((2.2,-2.4,1.9),(2.4,-2.0,1.9),q),(3.4,.4,1.0),30,8)
    return dict(upd=upd)
SHOTS['PACK']=PACK_
def CRY_():
    F=lounge_set(); Da=F['da']
    for i in range(10):
        for s in (-1,1): puff((-.8+s*.1,2.55,1.75),.1+i*.18,.04,1,M('#7FC8F0',.2,emit=.6,alpha=.8),.0,.4,drift=(s*.4,-.6,-1.6),seed=i)
    def upd(t):
        lidle(F,t); face(Da,mouth='frown',brow=.06,brow_r=20,eyes=.6); Da['head'].rotation_euler=(R(10),0,R(8*math.sin(t*12)))
        k=math.sin(pi*tl(t,.4,1.4)); Da['arm'][1].rotation_euler=(R(-110*k-20),0,R(-20)); Da['root'].location[2]+=.0
        q=ease(t/DUR); camset(LV((-.8,1.1,1.55),(-.8,1.3,1.55),q),hp(Da,-.03),45,2.8)
    return dict(upd=upd)
SHOTS['CRY']=CRY_
def UNCLE_():
    F=lounge_set(); Ch=F['ch']; ph=phone(Ch,1,1.4); b=bubble('Toronto plot?',(.85,2.7,2.55),.4,size=.16,col='#1F3A2A',bg='#DFF5E1')
    def upd(t):
        lidle(F,t); hold_phone(Ch,1,1); Ch['head'].rotation_euler[0]=R(14); face(Ch,mouth='grin',brow=.05); g=math.sin(t*3); Ch['arm'][-1].rotation_euler=(R(-60-10*g),0,R(20))
        q=ease(t/DUR); camset(LV((.4,1.0,1.6),(.5,1.2,1.6),q),hp(Ch,-.15),38,4)
    return dict(upd=upd)
SHOTS['UNCLE']=UNCLE_
def ZAMEEN_():
    F=lounge_set(); Ch=F['ch']; ph=phone(Ch,1,1.4)
    def upd(t):
        lidle(F,t); hold_phone(Ch,1,.5); talk(Ch,t,27.45,29.2); face(Ch,brow=.05,brow_r=8); Ch['head'].rotation_euler=(R(0),0,R(-25)); Ch['arm'][-1].rotation_euler=(R(-45),0,R(25))
        q=ease(t/DUR); camset(LV((.2,1.3,1.6),(.25,1.5,1.6),q),hp(Ch,-.03),42,2.8)
    return dict(upd=upd)
SHOTS['ZAMEEN']=ZAMEEN_
def JOB_():
    F=lounge_set(); Ar=F['ar']
    def upd(t):
        lidle(F,t); Ar['root'].rotation_euler[2]=R(170); talk(Ar,t,29.3,31.3); face(Ar,brow=.06,brow_r=16); g=math.sin(t*8)
        Ar['arm'][1].rotation_euler=(R(-65-15*g),0,R(-25)); Ar['arm'][-1].rotation_euler=(R(-65+15*g),0,R(25))
        q=ease(t/DUR); camset(LV((.55,1.75,1.85),(.5,1.6,1.86),q),hp(Ar,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['JOB']=JOB_
# ================================================================ SCENE 3 — airport
def ap_set():
    airport(); B.done('airport'); setup_world('morning_s',shadow=50); point((0,0,6),800,(1,.97,.9),3.0,False); point((2,-3,4),500,(1,.97,.9),2.0,False)
    F=dict(ar=mk(ARSLAN,0,2.0,0,'arslan'),ab=mk(ABBA,-1.3,1.3,-50,'abba'),am=mk(AMMI,1.2,1.2,40,'ammi'),da=mk(DADI,-2.3,1.6,-40,'dadi'),ch=mk(CHACHA,2.4,1.9,60,'chacha'))
    tr=empty((-.9,3.0,0)); trolley(tr,1.0); W=walkers(6,9,-12,12,(5.5,7.0)); return F,W
def apidle(F,W,t,skip=()):
    upd_walkers(W,t+3)
    for k,H in F.items():
        if k not in skip: stand(H,t); blink(H,t)
def AIRPORT_():
    F,W=ap_set()
    def upd(t):
        upd_walkers(W,t+3)
        for i,(k,H) in enumerate(F.items()):
            p=H['root'].location.copy() if t==0 else None
            x0={'ar':0,'ab':-1.3,'am':1.2,'da':-2.3,'ch':2.4}[k]; y0={'ar':2.0,'ab':1.3,'am':1.2,'da':1.6,'ch':1.9}[k]
            walk_path(H,[(x0,y0+5.5),(x0,y0)],t,-.1*i,DUR-.4,step=.5); blink(H,t)
            face(H,mouth='grin')
        q=ease(t/DUR); camset(LV((0,-5,2.2),(0,-4,2.0),q),(0,3,1.5),24,16)
    return dict(upd=upd)
SHOTS['AIRPORT']=AIRPORT_
def ADVICE_():
    F,W=ap_set()
    def upd(t):
        apidle(F,W,t); Ab=F['ab']; Ar=F['ar']; Ab['root'].location=(-.8,1.4,0); facep(Ab,(0,2.0)); Ar['root'].rotation_euler[2]=R(-130); arm_to(Ab,-1,hp(Ar,-.7),tl(t,.2,.6),base=(-30,0,0)); face(Ab,mouth='flat',brow=-.02); face(Ar,mouth='smile')
        q=ease(t/DUR); camset(LV((-1.6,3.9,1.8),(-1.4,3.6,1.8),q),(-.4,1.6,1.6),28,8)
    return dict(upd=upd)
SHOTS['ADVICE']=ADVICE_
def HATH_():
    F,W=ap_set()
    def upd(t):
        apidle(F,W,t); Ab=F['ab']; Ar=F['ar']; Ab['root'].location=(-.8,1.4,0); Ab['root'].rotation_euler[2]=math.atan2(-1.0-(-.8),-(-.6-1.4)); Ar['root'].rotation_euler[2]=R(-130); arm_to(Ab,-1,hp(Ar,-.7),1,base=(-30,0,0))
        talk(Ab,t,36.61,38.3); face(Ab,brow=-.02); g=math.sin(t*3); Ab['arm'][1].rotation_euler=(R(-60-15*g),0,R(20))
        q=ease(t/DUR); camset(LV((-1.0,-.6,1.85),(-.98,-.4,1.86),q),hp(Ab,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['HATH']=HATH_
def BAGS_():
    F,W=ap_set(); Ar=F['ar']; Am=F['am']; bs=[]
    for k in range(5):
        e=empty((0,0,0)); foodbag(e,1.5,['#C8372D','#2B5AA8','#F2C14E','#2B8A5A','#7448C2'][k]); e.parent=Ar['root']; e.location=(-.35+.18*k,-.35,1.2+.2*(k%2)); e.scale=(0,0,0); bs.append((e,.3+.3*k))
    def upd(t):
        apidle(F,W,t); Ar['root'].rotation_euler[2]=0; Am['root'].location=(.9,1.2,0); facep(Am,(0,2.0)); g=abs(math.sin(t*4)); arm_to(Am,-1,hp(Ar,-1.0),.5+.5*g,base=(-30,0,0)); face(Am,mouth='grin')
        for e,t0 in bs: k=pop(t-t0) if t>t0 else 0; e.scale=(k,k,k)
        Ar['arm'][1].rotation_euler=(R(-70),0,R(15)); Ar['arm'][-1].rotation_euler=(R(-70),0,R(-15)); face(Ar,mouth='O' if t>1.0 else 'flat',brow=.05); Ar['root'].rotation_euler[0]=R(6*tl(t,1.0,2.0))
        q=ease(t/DUR); camset(LV((.4,-2.4,1.7),(.4,-2.0,1.7),q),(.3,1.8,1.4),28,8)
    return dict(upd=upd)
SHOTS['BAGS']=BAGS_
def IPHONE_():
    F,W=ap_set(); Ch=F['ch']; b=bubble('iPhone!',(1.5,2.1,2.75),.5,size=.18,col='#7A1F1F',bg='#FFF3B0')
    def upd(t):
        apidle(F,W,t); Ch['root'].location=(1.5,2.1,0); facep(Ch,(0,2.0),.5,cam=(1.3,-1.4)); F['am']['root'].location=(.5,.9,0); face(Ch,mouth='grin',brow=.05); k=tl(t,.2,.5); Ch['arm'][1].rotation_euler=(R(-20*k),0,R(150*k)); Ch['arm'][-1].rotation_euler=(R(-20*k),0,R(-150*k))
        Ch['root'].location[2]=.05*abs(math.sin(t*4))
        q=ease(t/DUR); camset(LV((3.3,-1.3,1.9),(3.1,-1.0,1.9),q),hp(Ch,-.1),30,4)
    return dict(upd=upd)
SHOTS['IPHONE']=IPHONE_
def MEREY_():
    F,W=ap_set(); Ch=F['ch']
    def upd(t):
        apidle(F,W,t); F['am']['root'].location=(.5,.9,0); Ch['root'].location=(1.5,2.1,0); facep(Ch,(0,2.0),.5,cam=(1.3,-.2)); talk(Ch,t,43.02,44.7,rest='grin'); face(Ch,brow=.05); g=math.sin(t*6); Ch['arm'][1].rotation_euler=(R(-45-15*g),0,R(-25)); Ch['root'].rotation_euler[1]=R(4*g)
        q=ease(t/DUR); camset(LV((1.3,.3,1.75),(1.3,.5,1.76),q),hp(Ch,-.03),42,2.8)
    return dict(upd=upd)
SHOTS['MEREY']=MEREY_
# ================================================================ SCENE 4 — plane + call
SY_=0.0
def plane_set():
    cabin(); B.done('cabin'); setup_interior('day',room=(0,0,2.8),res=PCT,samples=SAMPLES,shadow_dist=12); point((0,-1.5,2.3),50,(1,.95,.88),1.0,False)
    Ar=mk(ARSLAN,-.55,SY_,0,'arslan'); r=random.Random(4)
    for k,(x,y) in enumerate(((-1.45,SY_),(.55,SY_-1.6),(1.0,SY_),(-1.0,SY_-1.6),(.55,SY_+1.6))): H=mk(dict(ABBA,top=r.choice(['#2B5AA8','#C8372D','#7448C2']),vest=None,glasses=False,hairstyle=r.choice(['short','fringe','curly'])),x,y,0,'pax%d'%k); PX.append(H)
    return Ar
PX=[]
def pidle(Ar,t):
    sit(Ar,1,.51,legs=80); blink(Ar,t); Ar['root'].location[0]=-.55; Ar['root'].location[1]=SY_
    for H in PX: sit(H,1,.51,legs=80); blink(H,t); H['head'].rotation_euler[0]=R(10); face(H,mouth='flat',eyes=.5)
def BOARD_():
    Ar=plane_set()
    def upd(t):
        pidle(Ar,t); face(Ar,mouth='smile'); k=tl(t,.3,1.0); Ar['root'].rotation_euler[0]=R(-8*k); Ar['arm'][1].rotation_euler=(R(-20),0,R(-40)); Ar['arm'][-1].rotation_euler=(R(-20),0,R(40))
        q=ease(t/DUR); camset(LV((.1,-3.6,1.9),(-.1,-2.4,1.75),q),hp(Ar,-.1),28,8)
    return dict(upd=upd)
SHOTS['BOARD']=BOARD_
def CALL_():
    D=phone_call()
    ui_world()
    def upd(t):
        for i,r_ in enumerate(D['ring']): q=((t*1.2)+i*.5)%1; k=1+q*.8; r_.scale=(k,1,k)
        camset((0,-L(7.6,6.8,ease(t/DUR)),-200),(0,0,-200),50,22)
    return dict(upd=upd)
SHOTS['CALL']=CALL_
def bed_set():
    bedroom(); B.done('bedroom'); setup_interior('evening',room=(0,0,3.2),res=PCT,samples=SAMPLES,shadow_dist=12); point((0,-1.0,2.6),70,(1,.9,.75),1.0,False)
    fan=ceiling_fan_w((0,.4,2.9)); Ab=mk(ABBA,.3,-.2,0,'abba'); ph=phone(Ab,1,1.4); return fan,Ab,ph
def selfie(Ab,t): stand(Ab,t); blink(Ab,t); Ab['root'].location=(.3,-.2,0); arm_to(Ab,1,(1.3,-.9,2.0),1,base=(0,0,0))
def BEDROOM_():
    fan,Ab,ph=bed_set(); b=bubble('VIDEO CALL',(.0,.2,2.75),.1,size=.13,col='#1F5A3A',bg='#DFF5E1')
    def upd(t):
        selfie(Ab,t); fan.rotation_euler[2]=t*10; face(Ab,mouth='flat',brow=-.03,brow_r=-10); Ab['head'].rotation_euler=(R(-8),0,R(10*math.sin(t*1.5)))
        q=ease(t/DUR); camset(LV((-.4,-2.0,2.1),(-.35,-1.7,2.05),q),(.2,.4,1.8),24,8)
    return dict(upd=upd)
SHOTS['BEDROOM']=BEDROOM_
def FANQ_():
    fan,Ab,ph=bed_set()
    def upd(t):
        selfie(Ab,t); fan.rotation_euler[2]=t*10; talk(Ab,t,51.74,54.4); face(Ab,brow=-.04,brow_r=-14); k=tl(t,1.0,1.3); arm_to(Ab,-1,(0,.4,2.9),k,base=(-30,0,0)); Ab['head'].rotation_euler[0]=R(-25*k*(1-tl(t,2.2,2.5)))
        q=ease(t/DUR); camset(LV((-.3,-1.5,1.95),(-.25,-1.3,1.96),q),hp(Ab,.0),30,4)
    return dict(upd=upd)
SHOTS['FANQ']=FANQ_
def CLOSES_():
    Ar=plane_set(); ph=phone(Ar,1,1.3)
    def upd(t):
        pidle(Ar,t); hold_phone(Ar,1,1); Ar['head'].rotation_euler[0]=R(8); blink(Ar,t,force=t>.4); face(Ar,mouth='flat',brow=.05,brow_r=14,eyes=.0 if t>.4 else 1.0)
        q=ease(t/DUR); camset(LV((-.4,-1.4,1.85),(-.45,-1.2,1.86),q),hp(Ar,-.1),32,2.8)
    return dict(upd=upd)
SHOTS['CLOSES']=CLOSES_
def ABBA_():
    Ar=plane_set(); ph=phone(Ar,1,1.3)
    def upd(t):
        pidle(Ar,t); hold_phone(Ar,1,1); Ar['head'].rotation_euler[0]=R(8); talk(Ar,t,56.52,59.5); face(Ar,brow=.04,brow_r=10,eyes=.75); headtouch(Ar,-1,tl(t,.1,.4)*(1-tl(t,1.2,1.5)),dx=.1,dy=-.8,dz=.35)
        q=ease(t/DUR); camset(LV((-.45,-1.3,1.85),(-.5,-1.15,1.86),q),hp(Ar,-.1),32,2.8)
    return dict(upd=upd)
SHOTS['ABBA']=ABBA_
def GRUMBLE_():
    fan,Ab,ph=bed_set()
    def upd(t):
        stand(Ab,t); blink(Ab,t); Ab['root'].location=(.3,-.2,0); hold_phone(Ab,1,1); Ab['head'].rotation_euler[0]=R(12); talk(Ab,t,59.66,62.3,rest='frown'); face(Ab,brow=-.04,brow_r=-14); fan.rotation_euler[2]=t*10*(1-tl(t,1.6,2.6))
        Ab['arm'][-1].rotation_euler=(R(-30),0,R(40)); Ab['head'].rotation_euler[2]=R(-12*math.sin(t*2))
        q=ease(t/DUR); camset(LV((.6,-1.6,1.75),(.55,-1.35,1.76),q),hp(Ab,-.05),40,2.8)
    return dict(upd=upd)
SHOTS['GRUMBLE']=GRUMBLE_
W_=json.load(open(LH+'/audio/words.json'))
