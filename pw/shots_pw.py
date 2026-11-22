# Shots for "The Peshawari Brother". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=95.9
SEQ=[('OPEN', 0.0), ('FAMILY', 3.13), ('MEET', 5.3), ('VISITS', 6.24), ('KNOCK', 9.64), ('KHUSH', 12.64), ('HUGS', 14.15), ('COUNTS', 16.05), ('SITS', 18.46), ('MOTHER', 20.07), ('KEBAB', 21.63), ('MORE', 22.74), ('KARAHI', 23.72), ('EVENMORE', 24.39), ('PULAO', 25.97), ('PLATE', 27.47), ('IMPOSSIBLE', 29.5), ('BAS', 31.35), ('DAKHABARA', 34.07), ('GREENTEA', 36.31), ('KAHWA1', 38.27), ('WALLET', 39.51), ('GRAB', 41.85), ('DOSTAN', 44.34), ('SMILES', 46.22), ('BAG', 47.32), ('YEH', 49.45), ('GHAR', 50.23), ('INSIDE', 52.08), ('KAHWA2', 56.11), ('BAZAAR', 57.78), ('SEES', 61.66), ('FINALP', 64.21), ('FINALQ', 65.8), ('TWENTY', 68.17), ('FIFTY', 70.28), ('DRINK', 71.64), ('HUG2', 73.91), ('WHOWON', 75.64), ('CAR', 76.79), ('OFFENDED', 79.53), ('YAAR', 81.05), ('LAUGHS', 83.22), ('FUEL', 84.25), ('WHISPER', 87.22), ('FREEZES', 89.77), ('FAMILYQ', 90.97), ('PETROL', 93.04)]
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
def st_set(crowd=6,seed=3):
    d,d2=house_street(); B.done('street'); setup_world('morning',shadow=40)
    Ha=mk(HAMID,0,3.0,0,'hamid'); Al=mk(ALI,0,1.5,180,'ali'); W=walkers(min(crowd,4),seed,-24,24,(-2.9,)); return d,d2,Ha,Al,W
def hug(A,Bh,k):
    for s in (1,-1):
        arm_to(A,s,hp(Bh,-.7),k,base=(-30,0,0)); arm_to(Bh,s,hp(A,-.7),k,base=(-30,0,0))
def hj_set():
    hujra(); B.done('hujra'); setup_interior('evening',room=(0,0,3.3),res=PCT,samples=SAMPLES,shadow_dist=12); point((0,0,2.8),160,(1,.9,.75),1.2,False); point((0,-2.5,2.0),160,(1,.92,.8),1.2,False)
    Al=mk(ALI,-.9,2.75,0,'ali'); Ha=mk(HAMID,.9,2.75,0,'hamid'); Mo=mk(MOTHER,3.4,-2.5,0,'mother'); return Al,Ha,Mo
def hidle(Al,Ha,Mo,t,mo_on=False):
    for H in (Al,Ha): sit(H,1,.26,legs=85); blink(H,t); H['root'].location[1]=2.75; H['root'].rotation_euler[2]=0
    stand(Mo,t); blink(Mo,t)
    if not mo_on: Mo['root'].location=(30,30,0)
FOODS={}
def spread(t0s):
    out=[]
    for kind,loc,s,t0 in t0s:
        e=food(kind,loc,s); e.scale=(0,0,0); out.append((e,t0))
    def upd(t):
        for e,t0 in out: k=pop(t-t0) if t>=t0 else 0; e.scale=(k,k,k)
    return upd
ALLF=[('kebab',(-.9,1.7,0),1.0),('naan',(.9,1.7,0),1.0),('karahi',(0,1.3,0),1.2),('kebab',(-.6,.8,0),1.0),('pulao',(.6,.9,0),1.5),('karahi',(-1.4,1.1,0),1.0),('pulao',(1.4,1.2,0),1.2)]
def foods(n_vis,new=None,t0=.3):
    L=[]
    for i,(k,l,s) in enumerate(ALLF[:n_vis]): L.append((k,l,s,-9))
    if new is not None:
        for j,i in enumerate(new): k,l,s=ALLF[i]; L.append((k,l,s,t0+.25*j))
    return spread(L)
# ================================================================ HOOK
def OPEN_():
    d,d2,Ha,Al,W=st_set(crowd=10); Al['root'].location=(30,30,0)
    def upd(t):
        upd_walkers(W,t); stand(Ha,t); blink(Ha,t); face(Ha,mouth='smile',brow=.04)
        q=ease(t/DUR); camset(LV((-9,-3.0,5.5),(-6,-2.6,2.4),q),LV((4,3,3.0),(0,3.0,1.8),q),22,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def FAMILY_():
    d,d2,Ha,Al,W=st_set(); Al['root'].location=(30,30,0); title_card('FRIEND = FAMILY',.3,(0,3.0,3.1),.3); hearts(lambda t: hp(Ha,.3),.4,DUR,n=8,size=1.0)
    def upd(t):
        upd_walkers(W,t+3); stand(Ha,t); blink(Ha,t); face(Ha,mouth='grin',brow=.05); k=tl(t,0,.5); Ha['arm'][1].rotation_euler=(R(-30*k),0,R(-100*k)); Ha['arm'][-1].rotation_euler=(R(-30*k),0,R(100*k))
        q=ease(t/DUR); camset(LV((0,-1.6,1.6),(0,-1.2,1.7),q),(0,3.0,1.9),26,8)
    return dict(upd=upd)
SHOTS['FAMILY']=FAMILY_
# ================================================================ SCENE 1
def MEET_():
    d,d2,Ha,Al,W=st_set(); Al['root'].location=(30,30,0); label('HAMID',(0,3.0,2.9),.1,col='#5A3418',bg='#FFF3B0')
    def upd(t):
        upd_walkers(W,t+5); stand(Ha,t); blink(Ha,t); face(Ha,mouth='smile',brow=.04); Ha['arm'][1].rotation_euler=(R(-20),0,R(-30)); Ha['arm'][-1].rotation_euler=(R(-20),0,R(30))
        q=ease(t/DUR); camset(LV((.3,1.0,1.95),(.25,1.2,1.95),q),hp(Ha,-.15),28,4)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def VISITS_():
    d,d2,Ha,Al,W=st_set(); Ha['root'].location=(30,30,0); label('ALI (FIRST VISIT)',(0,0,0),99); lb=label('ALI - FIRST VISIT',(0,0,2.6),.4,size=.18,col='#0E4A58',bg='#DFF5F8')
    def upd(t):
        upd_walkers(W,t+7); walk_path(Al,[(-7,-1.0),(-2,.6),(0,1.5)],t,0,DUR-.3,step=.5); blink(Al,t); face(Al,mouth='smile'); p=Al['root'].location; lb.location=(p[0],p[1],2.65)
        q=ease(t/DUR); camset(LV((-5,-2.0,1.7),(-1.5,-1.6,1.7),q),(hp(Al)[0],hp(Al)[1],1.6),26,8)
    return dict(upd=upd)
SHOTS['VISITS']=VISITS_
def KNOCK_():
    d,d2,Ha,Al,W=st_set(); Ha['root'].location=(0,3.9,0)
    def upd(t):
        upd_walkers(W,t+10); stand(Al,t); blink(Al,t); stand(Ha,t); blink(Ha,t); k=tl(t,.2,.6); arm_to(Al,1,(0,3.3,1.6),k*(1-tl(t,1.3,1.6)),base=(-30,0,0))
        o=ease(tl(t,1.2,1.7)); d.rotation_euler[2]=R(80*o); d2.rotation_euler[2]=R(-80*o); Ha['root'].location[1]=L(3.9,3.0,o); face(Ha,mouth='grin',brow=.05); face(Al,mouth='O' if t>1.4 else 'smile',brow=.05)
        q=ease(t/DUR); camset(LV((1.6,-.6,1.8),(1.4,-.3,1.8),q),(0,3.2,1.6),26,8)
    return dict(upd=upd)
SHOTS['KNOCK']=KNOCK_
def KHUSH_():
    d,d2,Ha,Al,W=st_set(); d.rotation_euler[2]=R(80); d2.rotation_euler[2]=R(-80)
    def upd(t):
        upd_walkers(W,t+13); stand(Al,t); blink(Al,t); stand(Ha,t); blink(Ha,t); talk(Ha,t,*ln(36,38),rest='grin'); face(Ha,brow=.05); k=tl(t,.2,.6)
        Ha['arm'][1].rotation_euler=(R(-40*k),0,R(-110*k)); Ha['arm'][-1].rotation_euler=(R(-40*k),0,R(110*k))
        q=ease(t/DUR); camset(LV((.95,1.55,2.0),(.9,1.7,2.0),q),hp(Ha,-.15),32,4)
    return dict(upd=upd)
SHOTS['KHUSH']=KHUSH_
def HUGS_():
    d,d2,Ha,Al,W=st_set(); d.rotation_euler[2]=R(80); d2.rotation_euler[2]=R(-80); cnt=[label(str(i+1),(-.8+.55*i,2.3,2.75),.3+.42*i,size=.3,col='#7A1F1F') for i in range(3)]
    def upd(t):
        upd_walkers(W,t+15); stand(Al,t); blink(Al,t); stand(Ha,t); blink(Ha,t); Al['root'].location=(0,2.15,0); hug(Ha,Al,1); face(Ha,mouth='grin',eyes=.4); face(Al,mouth='O',brow=.06)
        g=math.sin(t*5.5); Ha['root'].rotation_euler[2]=R(14*g); Al['root'].rotation_euler[2]=R(180+14*g)
        q=ease(t/DUR); camset(LV((2.3,.6,1.9),(2.0,.8,1.9),q),(0,2.5,1.7),28,5.6)
    return dict(upd=upd)
SHOTS['HUGS']=HUGS_
def COUNTS_():
    d,d2,Ha,Al,W=st_set(); d.rotation_euler[2]=R(80); d2.rotation_euler[2]=R(-80); c=label('ACTUALLY: 4',(0,2.15,2.75),1.0,size=.24,col='#7A1F1F')
    def upd(t):
        upd_walkers(W,t+17); stand(Al,t); blink(Al,t); stand(Ha,t); blink(Ha,t); Al['root'].location=(0,2.15,0); hug(Ha,Al,1); face(Ha,mouth='grin',eyes=.4)
        face(Al,mouth='flat',brow=.06,brow_r=14,eyes=.8)
        q=ease(t/DUR); camset(LV((-1.2,3.1,2.05),(-1.1,3.05,2.05),q),hp(Al,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['COUNTS']=COUNTS_
def SITS_():
    Al,Ha,Mo=hj_set(); fu=foods(0)
    def upd(t):
        hidle(Al,Ha,Mo,t); k=tl(t,.2,1.0); sit(Al,k,.26,legs=85); face(Al,mouth='smile'); face(Ha,mouth='grin'); fu(t)
        q=ease(t/DUR); camset(LV((0,-3.2,2.6),(0,-2.8,2.3),q),(0,1.8,.8),24,8)
    return dict(upd=upd)
SHOTS['SITS']=SITS_
def MOTHER_():
    Al,Ha,Mo=hj_set(); fu=foods(0)
    def upd(t):
        hidle(Al,Ha,Mo,t,True); walk_path(Mo,[(3.6,-2.6),(1.2,.9)],t,0,DUR-.2,step=.45); blink(Mo,t); face(Mo,mouth='smile'); Mo['arm'][1].rotation_euler=(R(-70),0,R(-10)); Mo['arm'][-1].rotation_euler=(R(-70),0,R(10))
        face(Al,mouth='smile'); fu(t)
        q=ease(t/DUR); camset(LV((-2.6,-2.6,2.0),(-2.3,-2.3,2.0),q),(1.2,.3,1.2),26,8)
    return dict(upd=upd)
SHOTS['MOTHER']=MOTHER_
def mo_place(Mo,t):
    Mo['root'].location=(2.2,1.6,0); facep(Mo,(0,1.4)); Mo['root'].rotation_euler[0]=R(15*abs(math.sin(t*2))); Mo['arm'][1].rotation_euler=(R(-60),0,R(-10)); Mo['arm'][-1].rotation_euler=(R(-60),0,R(10)); face(Mo,mouth='grin')
def foodshot(n_vis,new,lab=None,cam=((0,-1.2,1.9),(0,-1.0,1.8)),tgt=(0,1.4,.3),lens=26):
    def mk_():
        Al,Ha,Mo=hj_set(); fu=foods(n_vis,new)
        if lab: label(lab,(tgt[0],tgt[1],1.3),.5,size=.22,col='#7A3A10')
        def upd(t):
            hidle(Al,Ha,Mo,t,True); mo_place(Mo,t); fu(t); face(Al,mouth='O',brow=.06,brow_r=14)
            q=ease(t/DUR); camset(LV(cam[0],cam[1],q),tgt,lens,5.6)
        return dict(upd=upd)
    return mk_
SHOTS['KEBAB']=foodshot(0,[0,3],'CHAPLI KEBAB',((-.9,-.4,1.4),(-.9,-.2,1.3)),(-.8,1.3,.1),30)
SHOTS['MORE']=foodshot(2,[1],None)
SHOTS['KARAHI']=foodshot(3,[2,5],'KARAHI',((.6,-.5,1.4),(.5,-.3,1.3)),(-.2,1.2,.1),30)
SHOTS['EVENMORE']=foodshot(5,[],None,((0,-2.4,2.6),(0,-2.1,2.4)),(0,1.4,.4),24)
def PULAO_():
    Al,Ha,Mo=hj_set(); fu=foods(4,[4,6]); label('A MOUNTAIN OF PULAO',(.6,.9,1.4),.6,size=.2,col='#7A3A10')
    big=empty((.6,.9,0)); 
    def upd(t):
        hidle(Al,Ha,Mo,t,True); mo_place(Mo,t); fu(t); face(Al,mouth='O',brow=.07,brow_r=18)
        q=ease(t/DUR); camset(LV((1.2,-.6,.7),(1.1,-.4,.75),q),(.6,1.0,.4),28,4)
    return dict(upd=upd)
SHOTS['PULAO']=PULAO_
def PLATE_():
    Al,Ha,Mo=hj_set(); fu=foods(7); pl=empty((-.9,1.9,0)); ocyl((0,0,.03),.2,.02,M('#F4F1EA',.4),pl,rot=(0,0,0),seg=18); hp_=empty((-.9,1.9,.05)); oico((0,0,0),.15,M('#F2DCA0',.8),hp_,sc=(1,1,.6),sub=2)
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); k=(t*1.6)%1; s=.5+.8*(1-abs(1-2*k)) ; hp_.scale=(s,s,s); arm_to(Ha,1,(-.9,1.9,.3),.5+.5*abs(math.sin(t*3)),base=(-30,0,0)); face(Ha,mouth='grin'); face(Al,mouth='frown',brow=.06,brow_r=16)
        Al['head'].rotation_euler[0]=R(20)
        q=ease(t/DUR); camset(LV((-.3,.6,1.6),(-.35,.75,1.55),q),(-.9,2.0,.4),30,4)
    return dict(upd=upd)
SHOTS['PLATE']=PLATE_
def IMPOSSIBLE_():
    Al,Ha,Mo=hj_set(); fu=foods(7); title_card('PHYSICALLY IMPOSSIBLE',.2,(-.9,2.75,2.3),.16)
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); face(Al,mouth='frown',brow=.07,brow_r=20,eyes=.7); Al['root'].rotation_euler[0]=R(-8); Al['arm'][1].rotation_euler=(R(-20),0,R(-50)); Al['arm'][-1].rotation_euler=(R(-20),0,R(50))
        q=ease(t/DUR); camset(LV((-.9,.5,1.35),(-.9,.7,1.35),q),hp(Al,-.25),32,4)
    return dict(upd=upd)
SHOTS['IMPOSSIBLE']=IMPOSSIBLE_
def BAS_():
    Al,Ha,Mo=hj_set(); fu=foods(7)
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); Al['root'].rotation_euler[2]=R(-25); talk(Al,t,*ln(82,88)); face(Al,brow=.07,brow_r=20); k=tl(t,.1,.4); Al['arm'][1].rotation_euler=(R(-20*k),0,R(-80*k)); Al['arm'][-1].rotation_euler=(R(-20*k),0,R(80*k))
        q=ease(t/DUR); camset(LV((-.6,1.3,1.25),(-.62,1.45,1.25),q),hp(Al,-.03),38,2.8)
    return dict(upd=upd)
SHOTS['BAS']=BAS_
def DAKHABARA_():
    Al,Ha,Mo=hj_set(); fu=foods(7)
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); Ha['root'].rotation_euler[2]=R(30); talk(Ha,t,*ln(89,94),rest='grin'); face(Ha,brow=-.02,brow_r=-8); arm_to(Ha,1,(-.9,1.9,.3),tl(t,1.2,1.6),base=(-30,0,0)); Ha['arm'][-1].rotation_euler=(R(-60),0,R(30))
        q=ease(t/DUR); camset(LV((.55,1.3,1.3),(.57,1.45,1.3),q),hp(Ha,-.03),38,2.8)
    return dict(upd=upd)
SHOTS['DAKHABARA']=DAKHABARA_
def GREENTEA_():
    Al,Ha,Mo=hj_set(); fu=foods(7); kw=in_hand(Mo,1,lambda e: food('kahwa',(0,-.1,0),1.2) if False else None)
    pot=empty((0,0,0)); kk=food('kahwa',(0,0,0),1.4); kk.parent=Mo['arm'][1]; kk.location=hand_loc(Mo,1)
    def upd(t):
        hidle(Al,Ha,Mo,t,True); walk_path(Mo,[(3.0,-1.6),(1.2,.6)],t,0,DUR-.5,step=.45); blink(Mo,t); face(Mo,mouth='grin'); Mo['arm'][1].rotation_euler=(R(-70),0,R(-10)); fu(t)
        face(Al,mouth='O',brow=.06); face(Ha,mouth='grin')
        q=ease(t/DUR); camset(LV((-2.4,-2.0,1.9),(-2.2,-1.8,1.9),q),(1.4,.0,1.2),26,8)
    return dict(upd=upd)
SHOTS['GREENTEA']=GREENTEA_
def KAHWA1_():
    Al,Ha,Mo=hj_set(); fu=foods(7); kw=food('kahwa',(0,1.9,0),1.6); label('KAHWA #1',(0,1.9,1.0),.2,size=.3,col='#1F4D3A',bg='#DFF5E1')
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); face(Al,mouth='frown',brow=.06); face(Ha,mouth='grin')
        q=ease(t/DUR); camset(LV((0,-.6,1.5),(0,-.4,1.45),q),(0,2.0,.5),30,4)
    return dict(upd=upd)
SHOTS['KAHWA1']=KAHWA1_
# ================================================================ SCENE 2 — the bill
def WALLET_():
    Al,Ha,Mo=hj_set(); fu=foods(7); wl=in_hand(Al,-1,lambda e: wallet(e,1.6))
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); k=tl(t,.3,1.0); arm_to(Al,-1,(-.4,2.2,.7),k,base=(-30,0,0)); face(Al,mouth='smile'); Al['root'].rotation_euler[2]=R(-20)
        q=ease(t/DUR); camset(LV((-1.8,.8,1.4),(-1.7,.9,1.4),q),(-.6,2.4,.8),30,4)
    return dict(upd=upd)
SHOTS['WALLET']=WALLET_
def GRAB_():
    Al,Ha,Mo=hj_set(); fu=foods(7); wl=in_hand(Al,-1,lambda e: wallet(e,1.6)); label('EMERGENCY!',(0,2.75,1.9),.3,size=.24,col='#C8372D')
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); arm_to(Al,-1,(-.4,2.2,.7),1,base=(-30,0,0)); Al['root'].rotation_euler[2]=R(-20); k=ease(tl(t,.1,.35)); arm_to(Ha,1,(-.35,2.2,.75),k,base=(-30,0,0)); Ha['root'].rotation_euler[2]=R(30)
        face(Ha,mouth='O',brow=.08,brow_r=20,eyes=1.2); face(Al,mouth='O',brow=.06)
        q=ease(t/DUR); camset(LV((0,.2,1.5),(0,.45,1.45),q),(0,2.5,.9),26,5.6)
    return dict(upd=upd)
SHOTS['GRAB']=GRAB_
def DOSTAN_():
    Al,Ha,Mo=hj_set(); fu=foods(7)
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); Ha['root'].rotation_euler[2]=R(30); talk(Ha,t,*ln(122,126)); face(Ha,brow=.0,brow_r=-10); gest(Ha,t,-1,1.0,5,-60); arm_to(Ha,1,(-.35,2.2,.75),1,base=(-30,0,0))
        q=ease(t/DUR); camset(LV((.55,1.3,1.3),(.57,1.45,1.3),q),hp(Ha,-.03),38,2.8)
    return dict(upd=upd)
SHOTS['DOSTAN']=DOSTAN_
def SMILES_():
    Al,Ha,Mo=hj_set(); fu=foods(7)
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); Al['root'].rotation_euler[2]=R(-25); face(Al,mouth='smile',brow=.03,eyes=.7)
        q=ease(t/DUR); camset(LV((-.6,1.4,1.25),(-.62,1.5,1.25),q),hp(Al,-.03),40,2.8)
    return dict(upd=upd)
SHOTS['SMILES']=SMILES_
def gbag(H,s=-1): return in_hand(H,s,lambda e: gift_bag(e,1.6))
def BAG_():
    Al,Ha,Mo=hj_set(); fu=foods(7); gb=gbag(Ha,1)
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); Ha['root'].rotation_euler[2]=R(30); arm_to(Ha,1,hp(Al,-1.0),tl(t,.2,.8),base=(-30,0,0)); face(Ha,mouth='grin'); face(Al,mouth='O',brow=.05); Al['root'].rotation_euler[2]=R(-25)
        q=ease(t/DUR); camset(LV((0,.6,2.1),(0,.75,2.05),q),(0,2.6,1.1),28,5.6)
    return dict(upd=upd)
SHOTS['BAG']=BAG_
def YEH_():
    Al,Ha,Mo=hj_set(); fu=foods(7); gb=gbag(Al,1)
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); Al['root'].rotation_euler[2]=R(-25); Al['arm'][1].rotation_euler=(R(-70),0,R(-10)); talk(Al,t,*ln(136,138)); face(Al,brow=.06,brow_r=16)
        q=ease(t/DUR); camset(LV((-.6,1.3,1.25),(-.62,1.45,1.25),q),hp(Al,-.03),38,2.8)
    return dict(upd=upd)
SHOTS['YEH']=YEH_
def GHAR_():
    Al,Ha,Mo=hj_set(); fu=foods(7); gb=gbag(Al,1); g2=in_hand(Ha,-1,lambda e: gift_bag(e,1.3))
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t); Ha['root'].rotation_euler[2]=R(30); talk(Ha,t,*ln(139,146),rest='grin'); face(Ha,brow=.03); arm_to(Ha,-1,hp(Al,-1.0),tl(t,1.0,1.5),base=(-30,0,0)); Al['arm'][1].rotation_euler=(R(-70),0,R(-10))
        q=ease(t/DUR); camset(LV((.55,1.3,1.3),(.57,1.45,1.3),q),hp(Ha,-.03),38,2.8)
    return dict(upd=upd)
SHOTS['GHAR']=GHAR_
def INSIDE_():
    Al,Ha,Mo=hj_set(); fu=foods(7); items=[]
    for i,(txt,t0) in enumerate((('DRY FRUIT',.6),('SHAWL',1.9),('SWEETS',3.0))):
        e=empty((-1.2+1.2*i,.6,.0)); 
        if i==0: [oico((random.Random(k).uniform(-.25,.25),random.Random(k+9).uniform(-.2,.2),.08),.06,M(['#8A5A2A','#D9B24A','#C8372D'][k%3],.6),e,sub=1) for k in range(14)]
        elif i==1: obox((0,0,.12),(.35,.25,.1),M('#7448C2',.9,kind='fabric',h2='#D9B24A',sc=6),.06,e)
        else: obox((0,0,.1),(.3,.22,.1),M('#F2C14E',.4),.02,e); obox((0,-.225,.1),(.2,.003,.05),M('#C8372D',.4),0,e)
        e.scale=(0,0,0); items.append((e,t0)); label(txt,(-1.2+1.2*i,.6,.75),t0,size=.18,col='#7A3A10')
    def upd(t):
        hidle(Al,Ha,Mo,t); fu(t)
        for e,t0 in items: k=pop(t-t0) if t>=t0 else 0; e.scale=(k,k,k)
        face(Al,mouth='O',brow=.06); face(Ha,mouth='grin')
        q=ease(t/DUR); camset(LV((0,-1.6,1.7),(0,-1.4,1.6),q),(0,.8,.4),28,5.6)
    return dict(upd=upd)
SHOTS['INSIDE']=INSIDE_
def KAHWA2_():
    Al,Ha,Mo=hj_set(); fu=foods(7); k1=food('kahwa',(-.3,1.9,0),1.4); k2=food('kahwa',(.3,1.9,0),1.4); k2.scale=(0,0,0); label('KAHWA #2',(.3,1.9,1.0),.3,size=.3,col='#1F4D3A',bg='#DFF5E1')
    def upd(t):
        hidle(Al,Ha,Mo,t,True); mo_place(Mo,t); fu(t); k=pop(t-.2) if t>.2 else 0; k2.scale=(k,k,k); face(Al,mouth='frown',brow=.07,brow_r=18)
        q=ease(t/DUR); camset(LV((0,-.6,1.5),(0,-.4,1.45),q),(0,2.0,.6),28,4)
    return dict(upd=upd)
SHOTS['KAHWA2']=KAHWA2_
# ================================================================ SCENE 3 — Qissa Khwani
def qk_set(crowd=10,seed=5):
    qk_bazaar(); B.done('qk'); setup_world('afternoon',shadow=40)
    Ha=mk(HAMID,.6,2.3,-90,'hamid'); Al=mk(ALI,-1.9,1.0,160,'ali'); Sk=mk(SHOPKEEPER,-.6,2.3,90,'shop'); W=walkers(crowd,seed,-26,26,(-1.4,-.6)); return Ha,Al,Sk,W
def qidle(Ha,Al,Sk,W,t):
    upd_walkers(W,t+3)
    for H in (Ha,Al,Sk): stand(H,t); blink(H,t)
    facep(Ha,(-.6,2.3)); facep(Sk,(.6,2.3))
def BAZAAR_():
    Ha,Al,Sk,W=qk_set(crowd=16); title_card('QISSA KHWANI BAZAAR',.3,(0,0,5.6),.4)
    def upd(t):
        upd_walkers(W,t); walk_path(Ha,[(-10,.4),(.6,2.3)],t,0,DUR-.2,step=.55); walk_path(Al,[(-11,-.2),(-1.9,1.0)],t,0,DUR-.2,step=.55); blink(Ha,t); blink(Al,t); stand(Sk,t); blink(Sk,t)
        q=ease(t/DUR); camset(LV((-16,-2,4.5),(-12,-1.6,3.0),q),(4,1,2.2),22,16)
    return dict(upd=upd)
SHOTS['BAZAAR']=BAZAAR_
def SEES_():
    Ha,Al,Sk,W=qk_set(); label('NEGOTIATION',(0,2.3,2.8),.5,size=.2,col='#5A3418')
    ch=in_hand(Ha,1,lambda e: chappal(e,1.8))
    def upd(t):
        qidle(Ha,Al,Sk,W,t); facep(Al,(0,2.3)); face(Al,mouth='smile'); mouth_talk(Ha,t,0,DUR,rate=8,rest='flat'); mouth_talk(Sk,t,.4,DUR,rate=7); gest(Ha,t,-1,1.2,7,-70); Ha['arm'][1].rotation_euler=(R(-70),0,R(-10)); gest(Sk,t,1,1.0,6,-60)
        q=ease(t/DUR); camset(LV((2.6,-1.0,1.9),(2.4,-.8,1.9),q),(.2,2.0,1.6),26,8)
    return dict(upd=upd)
SHOTS['SEES']=SEES_
def FINALP_():
    Ha,Al,Sk,W=qk_set()
    def upd(t):
        qidle(Ha,Al,Sk,W,t); talk(Sk,t,*ln(180,182)); face(Sk,brow=-.04,brow_r=-12); Sk['arm'][1].rotation_euler=(R(-80),0,R(-30)); Sk['arm'][-1].rotation_euler=(R(-80),0,R(30))
        q=ease(t/DUR); camset(LV((.35,1.35,1.85),(.3,1.45,1.85),q),hp(Sk,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['FINALP']=FINALP_
def FINALQ_():
    Ha,Al,Sk,W=qk_set()
    def upd(t):
        qidle(Ha,Al,Sk,W,t); facep(Ha,(-.6,2.3),.5,cam=(-.35,1.35)); talk(Ha,t,*ln(183,189),rest='grin'); laugh(Ha,t,.5); gest(Ha,t,1,1.2,6,-75)
        q=ease(t/DUR); camset(LV((-.35,1.35,2.0),(-.3,1.45,2.0),q),hp(Ha,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['FINALQ']=FINALQ_
def TWENTY_():
    Ha,Al,Sk,W=qk_set(); cc=clock_card((0,2.6,3.2),.1,'20 MINUTES',spin=6)
    def upd(t):
        qidle(Ha,Al,Sk,W,t); mouth_talk(Ha,t,0,DUR,rate=9); mouth_talk(Sk,t,.2,DUR,rate=9); gest(Ha,t,1,1.4,9,-80); gest(Sk,t,1,1.4,9,-80); facep(Al,(0,2.3)); face(Al,mouth='flat',eyes=.4); Al['root'].location[2]=0
        q=ease(t/DUR); camset(LV((-1.0,-2.8,2.2),(-.8,-2.5,2.1),q),(.2,1.8,1.6),24,8)
    return dict(upd=upd)
SHOTS['TWENTY']=TWENTY_
def FIFTY_():
    Ha,Al,Sk,W=qk_set(); label('ALL THIS FOR Rs. 50',(0,2.3,2.8),.2,size=.22,col='#7A1F1F')
    def upd(t):
        qidle(Ha,Al,Sk,W,t); mouth_talk(Ha,t,0,DUR,rate=9); mouth_talk(Sk,t,.2,DUR,rate=9); gest(Ha,t,1,1.4,9,-80); gest(Sk,t,-1,1.4,9,-80)
        q=ease(t/DUR); camset(LV((0,-.6,1.9),(0,-.4,1.9),q),(0,2.3,1.6),28,5.6)
    return dict(upd=upd)
SHOTS['FIFTY']=FIFTY_
def DRINK_():
    Ha,Al,Sk,W=qk_set(); c1=in_hand(Ha,1,lambda e: ocyl((0,-.08,.06),.06,.1,M('#F4F1EA',.4),e,rot=(0,0,0),seg=10)); c2=in_hand(Sk,1,lambda e: ocyl((0,-.08,.06),.06,.1,M('#F4F1EA',.4),e,rot=(0,0,0),seg=10))
    def upd(t):
        qidle(Ha,Al,Sk,W,t)
        for i,H in enumerate((Ha,Sk)): k=math.sin(pi*((t*.7+i*.5)%1)); arm_to(H,1,hp(H,-.3),.4+.6*k,base=(-30,0,0)); face(H,mouth='flat' if k>.6 else 'o',eyes=.6)
        mouth_talk(Ha,t,0,DUR,rate=6)
        q=ease(t/DUR); camset(LV((0,-.6,1.9),(0,-.4,1.9),q),(0,2.3,1.6),28,5.6)
    return dict(upd=upd)
SHOTS['DRINK']=DRINK_
def HUG2_():
    Ha,Al,Sk,W=qk_set(); hearts(lambda t:(.25,2.1,2.4),.4,DUR,n=6)
    def upd(t):
        qidle(Ha,Al,Sk,W,t); Ha['root'].location=(-.05,2.3,0); hug(Ha,Sk,tl(t,.1,.5)); face(Ha,mouth='grin',eyes=.4); face(Sk,mouth='grin',eyes=.4)
        q=ease(t/DUR); camset(LV((0,-.6,1.9),(0,-.4,1.9),q),(-.3,2.3,1.6),28,5.6)
    return dict(upd=upd)
SHOTS['HUG2']=HUG2_
def WHOWON_():
    Ha,Al,Sk,W=qk_set(); title_card('WHO WON?',.1,(-1.9,1.0,2.7),.24)
    def upd(t):
        qidle(Ha,Al,Sk,W,t); Ha['root'].location=(-.05,2.3,0); hug(Ha,Sk,1); facep(Al,(0,2.3),.85,cam=(-1.75,-.9)); face(Al,mouth='flat',brow=.06,brow_r=16); headtouch(Al,1,.8)
        q=ease(t/DUR); camset(LV((-1.75,-.9,1.85),(-1.75,-.7,1.85),q),hp(Al,-.1),34,2.8)
    return dict(upd=upd)
SHOTS['WHOWON']=WHOWON_
# ================================================================ FINAL — the car
def car_set():
    needle,sw=car_int(); B.done('car'); setup_world('afternoon',shadow=20); point((0,-.8,2.4),40,(1,.9,.75),1.0,False)
    Al=mk(ALI,-.8,.1,0,'ali'); Ha=mk(HAMID,.8,.1,0,'hamid'); bg=in_hand(Al,1,lambda e: gift_bag(e,1.2)); return needle,sw,Al,Ha
def cidle(Al,Ha,needle,sw,t,fuel=.12):
    for H in (Al,Ha): sit(H,1,.6,legs=80); blink(H,t); H['root'].location[1]=.1; H['root'].rotation_euler[2]=0; H['root'].location[2]=.008*math.sin(t*23)
    arm_to(Ha,1,(.95,-1.6,1.55),1,base=(-30,0,0)); arm_to(Ha,-1,(.65,-1.6,1.55),1,base=(-30,0,0)); sw.rotation_euler[1]=R(5*math.sin(t*.8)); needle.rotation_euler[1]=R(-70+140*fuel)
    Al['arm'][1].rotation_euler=(R(-40),0,R(-10))
def CAR_():
    needle,sw,Al,Ha=car_set(); b=bubble('HOW MUCH DO I OWE YOU?',(-.8,.1,2.65),.6,size=.11,col='#0E4A58',bg='#DFF5F8')
    def upd(t):
        cidle(Al,Ha,needle,sw,t); look_at(Al,hp(Ha),.6); mouth_talk(Al,t,.6,2.4); face(Al,brow=.04); face(Ha,mouth='flat')
        q=ease(t/DUR); camset(LV((0,-2.3,2.15),(0,-2.15,2.1),q),(0,.1,1.9),24,8)
    return dict(upd=upd)
SHOTS['CAR']=CAR_
def OFFENDED_():
    needle,sw,Al,Ha=car_set()
    def upd(t):
        cidle(Al,Ha,needle,sw,t); look_at(Ha,hp(Al),.8*tl(t,.2,.6)); face(Ha,mouth='O',brow=.08,brow_r=24,eyes=1.15); Ha['head'].rotation_euler[0]=R(-6)
        q=ease(t/DUR); camset(LV((.5,-1.6,2.1),(.55,-1.45,2.1),q),hp(Ha,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['OFFENDED']=OFFENDED_
def YAAR_():
    needle,sw,Al,Ha=car_set()
    def upd(t):
        cidle(Al,Ha,needle,sw,t); look_at(Ha,hp(Al),.8); talk(Ha,t,*ln(228,234)); face(Ha,brow=.07,brow_r=22); arm_to(Ha,-1,hp(Ha,-.6),tl(t,.2,.5),base=(-30,0,0))
        q=ease(t/DUR); camset(LV((.5,-1.6,2.1),(.53,-1.5,2.1),q),hp(Ha,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['YAAR']=YAAR_
def LAUGHS_():
    needle,sw,Al,Ha=car_set()
    def upd(t):
        cidle(Al,Ha,needle,sw,t); laugh(Al,t,1.0); look_at(Al,hp(Ha),.5)
        q=ease(t/DUR); camset(LV((-.55,-1.6,2.1),(-.58,-1.5,2.1),q),hp(Al,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['LAUGHS']=LAUGHS_
def FUEL_():
    needle,sw,Al,Ha=car_set(); label('FUEL: ALMOST EMPTY',(.58,-1.9,1.98),.6,size=.05,col='#C8372D')
    def upd(t):
        cidle(Al,Ha,needle,sw,t,fuel=.12-.06*tl(t,.3,2.0)); look_at(Ha,(.58,-1.95,1.7),.8)
        camset((.58,-1.15,2.1),(.58,-1.95,1.71),30,1.4)
    return dict(upd=upd)
SHOTS['FUEL']=FUEL_
def WHISPER_():
    needle,sw,Al,Ha=car_set()
    def upd(t):
        cidle(Al,Ha,needle,sw,t); k=tl(t,0,.6); Ha['root'].location[0]=.8-.3*k; Ha['root'].rotation_euler[1]=R(-10*k); look_at(Ha,hp(Al),.8); talk(Ha,t,*ln(246,253),rate=5,shapes=('o','flat','o','flat')); face(Ha,brow=.02,brow_r=-6,eyes=.7)
        arm_to(Ha,-1,hp(Ha,-.05),k,base=(-30,0,0))
        q=ease(t/DUR); camset(LV((0,-2.0,2.1),(0,-1.9,2.1),q),(0,.1,2.0),26,4)
    return dict(upd=upd)
SHOTS['WHISPER']=WHISPER_
def FREEZES_():
    needle,sw,Al,Ha=car_set()
    def upd(t):
        cidle(Al,Ha,needle,sw,0); face(Al,mouth='O',brow=.08,brow_r=22,eyes=1.2); Al['head'].rotation_euler=(0,0,R(-25*tl(t,0,.25)))
        q=ease(t/DUR); camset(LV((-.55,-1.55,2.1),(-.6,-1.45,2.1),q),hp(Al,-.05),36,2.8)
    return dict(upd=upd)
SHOTS['FREEZES']=FREEZES_
def FAMILYQ_():
    needle,sw,Al,Ha=car_set()
    def upd(t):
        cidle(Al,Ha,needle,sw,t); look_at(Al,hp(Ha),.8); talk(Al,t,*ln(256,262)); face(Al,brow=.08,brow_r=22); Al['arm'][-1].rotation_euler=(R(-70),0,R(30))
        q=ease(t/DUR); camset(LV((-.55,-1.6,2.1),(-.58,-1.5,2.1),q),hp(Al,-.05),34,2.8)
    return dict(upd=upd)
SHOTS['FAMILYQ']=FAMILYQ_
def PETROL_():
    needle,sw,Al,Ha=car_set(); title_card('FAMILY HAI, PETROL FREE NAHI!',1.2,(0,-.3,2.7),.1)
    def upd(t):
        cidle(Al,Ha,needle,sw,t); look_at(Ha,(0,-2.3,2.1),.8); talk(Ha,t,*ln(263,267),rest='grin'); face(Ha,brow=.04); look_at(Al,hp(Ha),.7); face(Al,mouth='O',brow=.07)
        q=ease(t/DUR); camset(LV((-.3,-1.7,2.2),(-.28,-1.6,2.2),q),(.25,.1,1.95),26,8)
    return dict(upd=upd)
SHOTS['PETROL']=PETROL_
W_=json.load(open(LH+'/audio/words.json'))
