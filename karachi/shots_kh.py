SHOTS={}
WJ=json.load(open('/home/claude/karachi/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('I_space',0),('I_coast',16),('I_roads',43),('I_people',64),('I_title',83),
    ('D_horn',86),('D_ammi',92),('D_paanch',98),('D_utho',102),('D_air',114),
    ('S_sherry',122),('S_road',128),('S_constr',141),('S_driver',149),('S_jaga',153),('S_bump',156),
    ('W_queue',167),('W_ceremony',182),('W_neigh',195),('W_chotu',204),('W_perm',209),('W_hose',218),
    ('P_fan',243),('P_resign',250),('P_ammi',257),('P_sched',269),('P_allah',276),
    ('M_market',286),('M_shop',297),('M_rider',312),('M_labour',323),('M_student',332),('M_family',343),
    ('U_enter',362),('U_fridge',370),('U_money',382),('U_guzara',388),
    ('R_baarish',407),('R_cool',409),('R_bike',416),('R_road',423),('R_car',426),('R_chotu',432),('R_ammi',438),
    ('N_roof',443),('N_socha',453),('N_kyun',457),('N_ghar',464),('N_comp',478),
    ('F_rise',491),('F_coast',526),('F_final',552)]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.1,3)) for k,i in _K]
END=round(WE[-1]+.5,3)
def TK(key): return [t for k,t in SEQ if k==key][0]
def wl(i,key): return WS[i]-TK(key)
def we(i,key): return WE[i]-TK(key)
def talk(H,t,a,b,key,rest='smile',rate=8.0,shapes=('O','flat','o','grin','flat')):
    t0=wl(a,key); t1=we(b,key)
    if t0<=t<t1: face(H,mouth=shapes[int((t-t0)*rate+H['seed']*3)%len(shapes)])
    else: face(H,mouth=rest)
    return t0<=t<t1
def handsdown(H): H['arm'][1].rotation_euler=(0,0,0); H['arm'][-1].rotation_euler=(0,0,0)
def hips(H,k=1.0): H['arm'][1].rotation_euler=(R(-15*k),R(-35*k),R(70*k)); H['arm'][-1].rotation_euler=(R(-15*k),R(35*k),R(-70*k))
def street_day(mood='haze',seed=3,x0=-30,x1=30):
    ph=street(x0,x1,seed); B.done('street'); setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=70); return ph
def traffic(seed=1,n=6,y=(-3.2,-1.0,1.0,3.2),speed=(5,9),x0=-30,x1=30,bus=True):
    r=random.Random(seed); out=[]
    for i in range(n):
        yy=r.choice(y); d=1 if yy<0 else -1; sp=r.uniform(*speed)*d; xs=r.uniform(x0,x1)
        kind=r.random()
        if bus and i==0: o=kbus(xs,yy,0 if d>0 else 180,seed+i)
        elif kind<.45: o=car(xs,yy,r.choice(['#F4F1EA','#C0392B','#2B2C33','#8A9098','#1F6FB8','#D8D8D4']),0 if d>0 else 180)
        elif kind<.8: o=bike(xs,yy,0 if d>0 else 180,r.choice(['#C0392B','#1E1E22','#1F6FB8']))
        else: o=rickshaw(xs,yy,0 if d>0 else 180,r.choice(['#2E8B57','#1E1E22','#F4F1EA']))
        def fn(o,t,xs=xs,sp=sp): x=xs+sp*t; L_=x1-x0; o.location[0]=x0+((x-x0)%L_)
        fx.add(o,fn); out.append(o)
    return out
def riders(H1,H2,bk,t):
    """H1 driver (Sherry) and H2 pillion (Daniyal) on bike empty bk"""
    for i,(H,dx) in enumerate(((H1,.15),(H2,-.55))):
        H['root'].location=bk.matrix_world@Vector((dx,0,.0)); H['root'].location[2]=.02; H['root'].rotation_euler[2]=bk.rotation_euler[2]+R(90)
        H['z0']=0; sit(H,1,.86,80); H['legs'][1].rotation_euler[0]=R(-70); H['legs'][-1].rotation_euler[0]=R(-70)
    H1['arm'][1].rotation_euler=(R(-75),0,R(-12)); H1['arm'][-1].rotation_euler=(R(-75),0,R(12))
def mbike(x,y,rz=0,col='#C0392B'):
    b=bike(x,y,rz,col); return b


# ============================================================ INTRO
def SH_I(view):
    KEY='I_'+view
    if view=='space':
        space(); B.done('space'); setup_render('nightc',res=PCT,samples=SAMPLES,shadow_dist=300,mist=False)
        w_=bpy.context.scene.world; w_.use_nodes=False; w_.color=(0,0,0)
        bpy.ops.object.light_add(type='SUN'); sn=bpy.context.object; sn.rotation_euler=(R(60),0,R(-30)); sn.data.energy=4.0
        def upd(t):
            q=ease_in(min(1,t/DUR)); d=L(420,74,q); n=Vector((0,-1,.3)).normalized()
            camset(tuple(n*d+Vector((L(60,0,q),0,0))),tuple(n*L(0,60,q)),L(30,40,q),16.0)
        return dict(upd=upd)
    if view in ('coast','title'):
        city(3,False,R_=180,ss=-1); B.done('city'); setup_render('haze',res=PCT,samples=SAMPLES,shadow_dist=200)
        def upd(t):
            q=ease(t/DUR)
            if view=='coast': camset((L(-40,10,q),L(-210,-150,q),L(60,45,q)),(L(-10,10,q),L(-120,-40,q),0),24,8.0)
            else: camset((L(30,10,q),L(-60,-90,q),L(70,95,q)),(0,-10,0),22,8.0)
        return dict(upd=upd)
    street_day('haze',seed=5,x0=-40,x1=40); traffic(2,12,x0=-40,x1=40)
    peds=crowd([(-12,-5.4,90),(-4,-5.6,-90),(8,5.5,90),(15,5.4,-90),(20,-5.5,90),(-2,-5.2,90),(1,5.6,-90),(-8,5.3,90)],30)
    def upd(t):
        for i,c in enumerate(peds): blink(c,t); walker(c,(c['x'],c['y'],.18),c['rz'],1.0+.1*(i%3),t,arm=18)
        q=ease(t/DUR)
        if view=='roads': camset((L(-16,-8,q),-1.8,L(16,11,q)),(L(6,12,q),.5,0),24,8.0)
        else: camset((L(9,7,q),-6.2,1.5),(-4,-5.3,1.4),30,8.0)
    return dict(upd=upd)
for v in ('space','coast','roads','people','title'): SHOTS['I_'+v]=(lambda v=v: SH_I(v))

# ============================================================ FLAT MORNING
def flat_set(kind='morning'):
    fans=flat(); setup_interior(kind,room=(0,0,3.1),res=PCT,samples=SAMPLES); point((-2.6,2.2,1.9),55,(1,.93,.8),.4); point((3.0,2.2,1.9),45,(1,.93,.8),.4); return fans
def SH_D(view):
    KEY='D_'+view; fans=flat_set('morning'); D=person((-5.2,1.6,0),180,DAN,'flat',name='dan'); A=person((-3.0,-1.2,0),-30,AMMI,'frown',name='ammi')
    for f in fans: fx.add(f,lambda o,t: setattr(o,'rotation_euler',(0,0,t*9.0)))
    def lie(t,k):
        D['root'].location=(-5.1,1.25,.008); D['root'].rotation_euler=(0,0,0); D['z0']=0; sit(D,1,.62,90); D['root'].rotation_euler[0]=R(-75*(1-k))
    if view=='horn':
        hideH(A)
        def upd(t):
            k=ease((t-.25)/.25); lie(t,k); blink(D,t,0 if t<.25 else None); SHAKE[0]=.03 if t<.5 else 0
            talk(D,t,86,91,KEY,rest='shout',shapes=('shout','O','shout','frown')); arms(D,-120*k,0,30,-120*k,0,-30); face(D,brow=-.05,brow_r=20,eyes=1.15)
            q=ease(t/DUR); camset((-3.4,-.6,1.4),(-5.0,1.3,.95),26,4.0,focus=(-5.0,1.3,1.0))
        return dict(upd=upd)
    if view in ('ammi','paanch','utho'):
        def upd(t):
            blink(D,t); blink(A,t)
            if view=='ammi':
                walk_path(A,[(-1.0,-1.8),(-3.4,.2)],t,0,1.0,step=.45); talk(A,t,92,97,KEY,rest='frown',rate=7); lie(t,.4)
                if t>1.0: A['root'].rotation_euler[2]=R(heading_to(A,(-5.1,1.25))); stand(A,t); hips(A,ease((t-1.0)/.3))
                face(D,mouth='flat',eyes=.4); q=ease(t/DUR); camset((-5.7,-.6,1.8),(-3.6,-.2,1.5),24,5.0)
            elif view=='paanch':
                A['root'].location=(-3.4,.2,.008); A['root'].rotation_euler[2]=R(heading_to(A,(-5.1,1.25))); stand(A,t); hips(A)
                lie(t,1); D['head'].rotation_euler=(R(28),0,R(8*math.sin(t*2))); D['root'].rotation_euler[1]=R(-8)
                talk(D,t,98,101,KEY,rest='flat',rate=5); face(D,eyes=.25,brow=.03); D['arm'][1].rotation_euler=(R(-20),0,0)
                q=ease(t/DUR); camset((-3.9,-.4,1.3),(-5.1,1.25,1.0),26,4.0,focus=(-5.1,1.25,1.1))
            else:
                A['root'].location=(-3.4,.2,.008); A['root'].rotation_euler[2]=R(heading_to(A,(-5.1,1.25))); stand(A,t)
                talk(A,t,102,113,KEY,rest='frown',rate=7); hips(A); face(A,brow=-.04,brow_r=18)
                if t>wl(113,KEY): A['arm'][1].rotation_euler=(R(-150),0,R(20)); lie(t,ease((t-wl(113,KEY))/.4))
                else: lie(t,0)
                q=ease(t/DUR); camset((-4.6,1.0,1.75),(-3.4,.2,1.75),24,4.0,focus=(-3.4,.2,1.75))
        return dict(upd=upd)
    # air: window + dust puff + coughing
    hideH(A); dust=[]
    for k in range(26):
        o=oico((0,0,0),.12,M('#C9B48A',.95,alpha=.45),sub=1); ph=k/26.0
        def fn(o,t,ph=ph,k=k):
            u=max(0,t-1.0-ph*.6); s_=.3+u*1.5; o.location=(-2.6+.25*math.sin(k*1.7)*u*2,2.8-u*1.6,1.85+.25*math.cos(k*2.3)*u*2); o.scale=(s_,s_,s_) if 0<u<2.5 else (0,0,0)
        fx.add(o,fn)
    def upd(t):
        blink(D,t); stand(D,t); D['root'].location=(-2.6,1.3,.008); D['root'].rotation_euler[2]=R(180)
        k=ease(t/.6); D['arm'][1].rotation_euler=(R(-130*k),0,R(-20)) if t<1.2 else (R(-40),0,0)
        talk(D,t,114,115,KEY,rest='grin'); cough=t>wl(115,KEY)+.5 and t<wl(116,KEY)
        if cough: D['root'].rotation_euler[0]=R(12*abs(math.sin(t*14))); face(D,mouth='O',eyes=.4); D['arm'][-1].rotation_euler=(R(-110),0,R(-30))
        else: D['root'].rotation_euler[0]=0; talk(D,t,116,121,KEY,rest='smirk')
        face(D,brow=.02)
        q=ease(t/DUR); camset((L(-1.9,-2.1,q),2.55,1.8),(-2.6,1.3,1.85),22,4.0,focus=(-2.6,1.3,1.9))
    return dict(upd=upd)
for v in ('horn','ammi','paanch','utho','air'): SHOTS['D_'+v]=(lambda v=v: SH_D(v))

# ============================================================ ROADS
def SH_S(view):
    KEY='S_'+view; ph=street_day('haze',seed=3); tr=traffic(4,9,y=(-1.0,1.0,3.2),speed=(4,7))
    D=person((-1,-5.4,.18),180,DAN,'smile',name='dan'); S=person((0,-3.4,0),90,SHER,'grin',name='sher'); bk=mbike(-.2,-3.6,0,'#C0392B')
    for H in (D,S): H['z0']=.18
    peds=crowd([(-14,5.5,90),(10,5.6,-90),(16,-5.6,-90)],40)
    def bg(t):
        for i,c in enumerate(peds): blink(c,t); walker(c,(c['x'],c['y'],.18),c['rz'],.9,t,arm=18)
    def onbike(t):
        S['root'].location=bk.matrix_world@Vector((.1,0,0)); S['root'].location[2]=.02; S['root'].rotation_euler[2]=bk.rotation_euler[2]+R(90); S['z0']=0; sit(S,1,.86,80)
        S['arm'][1].rotation_euler=(R(-75),0,R(-12)); S['arm'][-1].rotation_euler=(R(-75),0,R(12))
    if view in ('sherry','road','constr'):
        D['root'].location=(-1.0,-5.4,.19)
        def upd(t):
            bg(t); blink(D,t); blink(S,t); stand(D,t); onbike(t)
            if view=='sherry':
                walk_path(D,[(-5,-5.4),(-1.2,-5.2)],t,0,DUR,step=.55); D['root'].location[2]=.19; talk(S,t,122,127,KEY,rest='grin')
                S['arm'][-1].rotation_euler=(R(-130),0,R(-25*math.sin(t*7))); look_at(S,D['root'].location+Vector((0,0,1.9)),.8)
                q=ease(t/DUR); camset((L(2.8,2.4,q),-3.9,1.4),(-1.4,-5.0,1.5),24,6.0)
            elif view=='road':
                D['root'].rotation_euler[2]=R(150); talk(D,t,128,136,KEY,rest='o'); talk(S,t,137,140,KEY,rest='flat') if t>wl(137,KEY)-.05 else None
                D['arm'][1].rotation_euler=(R(-60),0,R(-20)); look_at(D,(4,-1,0),.6 if t<wl(137,KEY) else .2); S['arm'][-1].rotation_euler=(R(-100),0,R(30))
                q=ease(t/DUR); camset((L(-3.0,-6.0,q),L(-3.4,-2.6,q),L(1.6,3.2,q)),(L(-1.0,4,q),L(-4.8,-1,q),L(1.6,.3,q)),L(30,22,q),6.0)
            else:
                D['root'].rotation_euler[2]=R(200); talk(D,t,141,148,KEY,rest='O',shapes=('O','shout','o')); shock(D,ease(t/.3)*.6); face(D,brow=.1,eyes=1.15)
                q=ease(t/DUR); camset((-2.7,-3.4,1.8),(-1.0,-5.4,1.95),30,3.5,focus=(-1.0,-5.4,1.95))
        return dict(upd=upd)
    if view=='driver':
        cr=car(0,-1.0,'#F4F1EA',0); dv=person((0,-1.0,0),0,DRIVER,'shout',name='driver')
        def upd(t):
            bg(t); hideH(D); hideH(S); cr.location[0]=-.5+1.0*t
            dv['root'].location=(cr.location[0]+.2,-1.85,.25); dv['root'].rotation_euler=(0,R(-12),R(-10)); dv['z0']=.25; sit(dv,1,.9,80)
            talk(dv,t,149,152,KEY,rest='shout',shapes=('shout','O','shout','frown')); dv['arm'][-1].rotation_euler=(R(-150),0,R(-30+25*math.sin(t*9))); face(dv,brow=-.05,brow_r=22)
            bk.location=(cr.location[0]-3.0+2.0*t,-3.6,0)
            camset((cr.location[0]+1.6,-4.6,1.5),(cr.location[0]+.2,-1.9,1.7),28,4.0,focus=(cr.location[0]+.2,-1.85,1.8))
        return dict(upd=upd)
    def upd(t):
        bg(t); blink(D,t); blink(S,t); x=-8+6.0*t; bump=0
        if view=='bump':
            tb=wl(157,KEY)-.4; u=t-tb
            if 0<u<.7: bump=math.sin(pi*u/.7)
        bk.location=(x,-2.6,.0); bk.rotation_euler=(R(-6*bump),0,R(0))
        for H,dx in ((S,.15),(D,-.6)):
            H['root'].location=(x+dx,-2.6,.02+(.6*bump if H is D else .12*bump)); H['root'].rotation_euler=(0,0,R(90)); H['z0']=0; sit(H,1,.86,80)
        S['arm'][1].rotation_euler=(R(-75),0,R(-12)); S['arm'][-1].rotation_euler=(R(-75),0,R(12))
        if view=='jaga':
            talk(S,t,153,155,KEY,rest='O',shapes=('shout','O')); face(D,mouth='O'); D['arm'][1].rotation_euler=(R(-30),0,R(-20)); face(S,brow=.06)
            camset((x+.6,-5.6,1.45),(x-.2,-2.6,1.55),26,5.0,focus=(x,-2.6,1.6))
        else:
            talk(D,t,156,166,KEY,rest='O',shapes=('shout','O','shout','o')); D['arm'][1].rotation_euler=(R(-160*bump-40),0,R(-30)); D['arm'][-1].rotation_euler=(R(-150*bump-30),0,R(30))
            face(D,brow=.1,eyes=1+.3*bump); face(S,mouth='grin' if t>wl(158,KEY) else 'O')
            SHAKE[0]=.05*bump; camset((x+.4,-5.6,1.0),(x-.2,-2.6,1.6),24,5.0,focus=(x,-2.6,1.6))
    return dict(upd=upd)
for v in ('sherry','road','constr','driver','jaga','bump'): SHOTS['S_'+v]=(lambda v=v: SH_S(v))

# ============================================================ WATER TANKER
def SH_W(view):
    KEY='W_'+view; street_day('hotday',seed=9,x0=-24,x1=24); tk=tanker(2,3.0,180)
    A=person((-1.2,1.0,0),-90,AMMI,'flat',name='ammi'); C=person((.4,.2,0),-90,CHOTU,'smile',name='chotu'); D=person((-2.6,-.4,0),60,DAN,'smile',name='dan')
    q_=crowd([(-2.4,1.1,-90),(-3.4,1.0,-90),(-4.5,1.2,-90),(-5.6,1.1,-90),(-6.6,1.0,-90),(6.0,-2.0,-120),(6.5,.2,90)],50)
    NB=q_[1]
    B2=Batch(); r=random.Random(2)
    for i,(x,y) in enumerate([(-1.6,.6),(-2.8,.55),(-3.9,.6),(-5.0,.6),(-6.0,.55),(-7.0,.6),(-1.1,.5),(-2.4,.4)]):
        c=r.choice(['#2E86C1','#C0392B','#27AE60','#E67E22','#8E44AD']); s_=r.uniform(.8,1.1); B2.cyl((x,y,.2*s_),.2*s_,.4*s_,M(c,.4),seg=14,r2=.15*s_)
    B2.done('buckets')
    cb=ocyl((0,0,0),.1,.18,M('#E84393',.4),r2=.08,rot=(0,0,0),seg=12)
    def upd(t):
        for c_ in q_: blink(c_,t); stand(c_,t); gaze_idle(c_,t)
        for H in (A,C,D): blink(H,t); stand(H,t)
        cb.location=C['arm'][1].matrix_world@Vector((0,-.05,-.95*C['u']))
        A['root'].location=(-1.2,1.0,.008); A['root'].rotation_euler[2]=R(-110); D['root'].rotation_euler[2]=R(heading_to(D,(-1.2,1.0)))
        if view=='queue':
            walk_path(D,[(-6,-2.6),(-2.6,-.4)],t,0,1.4,step=.55); p=D['root'].location
            if t>1.4: D['root'].rotation_euler[2]=R(heading_to(D,(-1.2,1.0)))
            talk(D,t,167,172,KEY,rest='o'); talk(A,t,173,181,KEY,rest='frown',rate=7) if t>wl(173,KEY)-.05 else None
            look_at(A,(p.x,p.y,1.9),.8); A['arm'][1].rotation_euler=(R(-70),0,R(-40)) if t>wl(178,KEY) else (0,0,0)
            q=ease(t/DUR); camset((L(.8,.5,q),-2.8,1.6),(-1.8,.5,1.6),24,6.0)
        elif view=='ceremony':
            talk(D,t,182,194,KEY,rest='smirk'); D['arm'][1].rotation_euler=(R(-70),0,R(-45+20*math.sin(t*3))); look_at(D,(2,3,2.0),.6); face(D,brow=.03,brow_r=-12)
            q=ease(t/DUR); camset((-1.0,-2.6,1.6),(-2.6,-.4,1.9),30,3.5,focus=(-2.6,-.4,1.9))
        elif view=='neigh':
            NB['root'].location=(-3.2,.6,.008); NB['root'].rotation_euler[2]=R(heading_to(NB,(-2.6,-.4))); talk(NB,t,195,203,KEY,rest='frown',rate=7)
            NB['arm'][1].rotation_euler=(R(-95),0,R(10*math.sin(t*8))); face(NB,brow=-.04,brow_r=18); look_at(D,(-3.2,.6,1.9)); face(D,mouth='o')
            q=ease(t/DUR); camset((-4.4,-1.0,1.7),(-3.2,.6,1.85),28,3.5,focus=(-3.2,.6,1.85))
        elif view=='chotu':
            walk_path(C,[(1.8,-.6),(-1.8,-.6)],t,0,1.1,step=.35)
            if t>1.1: C['root'].rotation_euler[2]=R(heading_to(C,(-2.6,-.4))); stand(C,t)
            C['arm'][1].rotation_euler=(R(-70),0,R(10)); talk(C,t,204,208,KEY,rest='grin'); face(C,brow=.08,eyes=1.15)
            look_at(D,C['root'].location+Vector((0,0,1.3)),.9)
            q=ease(t/DUR); camset((L(-.6,-1.0,q),-2.8,1.0),(-1.6,-.6,1.0),26,4.0,focus=C['root'].location+Vector((0,0,1.2)))
        elif view=='perm':
            C['root'].location=(-1.8,-.6,.008); C['root'].rotation_euler[2]=R(heading_to(C,(-2.6,-.4)))
            D['root'].location=(-2.7,-.4,.008); D['root'].rotation_euler[2]=R(heading_to(D,(-1.8,-.6)))
            talk(D,t,209,217,KEY,rest='grin'); D['arm'][1].rotation_euler=(R(-80),0,R(-20+15*math.sin(t*4))); look_at(D,(-1.8,-.6,1.2)); face(C,mouth='grin' if t>DUR*.75 else 'o',brow=.06)
            C['arm'][1].rotation_euler=(R(-70),0,R(10))
            if t>DUR*.75:
                for i,c_ in enumerate(q_+[A,D]): face(c_,mouth='grin'); c_['root'].rotation_euler[1]=R(4*math.sin(t*12+i))
            q=ease(t/DUR); camset((-2.0,-2.9,1.25),(-2.2,-.5,1.25),26,4.0,focus=(-2.3,-.5,1.3))
        elif view=='hose':
            for H,(x,y) in ((D,(-3.2,-.8)),(C,(-2.4,-1.0))): H['root'].location=(x,y,.008); H['root'].rotation_euler[2]=R(heading_to(H,(.2,2.0)))
            A['root'].location=(.3,.9,.008); A['root'].rotation_euler[2]=R(150); A['arm'][1].rotation_euler=(R(-60),0,0); A['arm'][-1].rotation_euler=(R(-60),0,0)
            for i,c_ in enumerate(q_[:4]): c_['root'].location[0]=-1.2-1.0*i+.3*ease(t/DUR)
            q=ease(t/DUR); camset((L(3.6,2.6,q),-3.4,L(1.0,2.6,q)),(.4,1.0,1.0),L(24,20,q),5.0)
    if view=='hose':
        nz=empty((.4,2.0,1.4)); ocyl((0,0,0),.05,2.0,M('#1E1E22',.6),nz,rot=(R(60),0,0),seg=8)
        for k in range(30):
            d_=obox((0,0,0),(.02,.02,.06),M('#BFE6FF',.1,alpha=.6,emit=.3),0); ph_=k/30
            def fn(o,t,ph_=ph_):
                u=(t*2.2+ph_)%1.0; o.location=(.35+.02*math.sin(ph_*30),1.3-.15*u,1.3-1.0*u*u)
            fx.add(d_,fn)
        ocyl((.35,1.25,.35),.3,.7,M('#2E86C1',.4),seg=16,rot=(0,0,0)); wl_=ocyl((.35,1.25,.0),.27,.01,M('#BFE6FF',.1,alpha=.7,emit=.2),seg=16,rot=(0,0,0))
        fx.add(wl_,lambda o,t: setattr(o,'location',(.35,1.25,.05+.6*min(1,t/8.0))))
    return dict(upd=upd)
for v in ('queue','ceremony','neigh','chotu','perm','hose'): SHOTS['W_'+v]=(lambda v=v: SH_W(v))

# ============================================================ LIGHTS OUT
def SH_P(view):
    KEY='P_'+view; fans=flat_set('day')
    D=person((2.4,1.2,0),0,DAN,'flat',name='dan'); S=person((3.6,1.2,0),0,SHER,'flat',name='sher'); A=person((4.8,1.2,0),0,AMMI,'flat',name='ammi')
    for H in (D,S,A): H['z0']=0
    T_STOP=wl(243,'P_fan')-.6
    def fanrot(o,t):
        tg=TK(KEY)+t-TK('P_fan'); spin=9.0 if tg<T_STOP else max(0,9.0-6*(tg-T_STOP))
        o['ang']=o.get('ang',0)+spin/24.0; o.rotation_euler=(0,0,o['ang'])
    for f in fans: fx.add(f,fanrot)
    hf=empty((0,0,0)); obox((0,0,.12),(.15,.012,.12),M('#E8C25A',.8,kind='fabric'),.02,hf); obox((0,0,-.1),(.015,.015,.12),M('#6B4026',.6),.005,hf)
    ph=phone(S,1)
    def upd(t):
        for H,x in ((D,2.4),(S,3.6),(A,4.8)): blink(H,t); H['root'].location=(x,1.2,.008); H['root'].rotation_euler[2]=0; sit(H,1,.46,90)
        for H in (D,S,A): face(H,mouth='flat',brow=-.02)
        hf.scale=(0,0,0); ph.scale=(0,0,0)
        if view=='fan':
            up=ease((t-.6)/.4)
            for H in (D,S,A): H['head'].rotation_euler[0]=R(30*up)
            talk(D,t,243,248,KEY,rest='flat'); talk(S,t,249,249,KEY,rest='flat')
            q=ease(t/DUR); camset((3.6,-2.6,1.2),(3.6,1.0,L(1.3,1.8,q)),24,6.0)
        elif view=='resign':
            talk(D,t,250,256,KEY,rest='smirk'); D['arm'][1].rotation_euler=(R(-45),0,R(10)); D['head'].rotation_euler[2]=R(-15); face(S,mouth='o')
            q=ease(t/DUR); camset((1.2,-.8,1.35),(2.4,1.2,1.45),30,3.5,focus=(2.4,1.2,1.45))
        elif view=='ammi':
            hf.scale=(1,1,1); a=math.sin(t*10); A['arm'][-1].rotation_euler=(R(-55),0,R(25+15*a)); hf.location=hand_pos(A,-1); hf.rotation_euler=(R(20*a),0,R(30))
            talk(A,t,257,268,KEY,rest='frown',rate=7); face(A,brow=-.04,brow_r=16); look_at(A,(3.0,1.2,1.4),.6)
            q=ease(t/DUR); camset((5.9,-.7,1.35),(4.8,1.2,1.45),30,3.5,focus=(4.8,1.2,1.45))
        elif view=='sched':
            ph.scale=(1,1,1); S['arm'][1].rotation_euler=(R(-80),0,R(-20)); S['head'].rotation_euler[0]=R(12); talk(S,t,269,275,KEY,rest='frown'); face(D,mouth='O',brow=.05)
            q=ease(t/DUR); camset((3.4,-.9,1.25),(3.6,1.2,1.35),30,3.5,focus=(3.6,1.2,1.4))
        elif view=='allah':
            talk(D,t,276,285,KEY,rest='flat'); D['arm'][1].rotation_euler=(R(-45+10*math.sin(t*3)),0,R(10)); D['head'].rotation_euler[0]=R(-15); face(D,brow=.05,eyes=.85)
            q=ease(t/DUR); camset((L(1.2,1.6,q),L(-.8,-1.6,q),1.4),(2.4,1.2,1.45),L(30,24,q),3.5,focus=(2.4,1.2,1.45))
    if view=='allah':
        # generator smoke outside the window
        for k in range(14):
            o=oico((0,0,0),.1,M('#8A8A8A',.95,alpha=.4),sub=1); ph_=k/14
            def fn(o,t,ph_=ph_):
                u=(t*.45+ph_)%1.0; o.location=(3.0+.3*math.sin(ph_*20),3.6+u*.4,1.2+u*2.0); s_=.3+u*1.2; o.scale=(s_,s_,s_)
            fx.add(o,fn)
    return dict(upd=upd)
for v in ('fan','resign','ammi','sched','allah'): SHOTS['P_'+v]=(lambda v=v: SH_P(v))

# ============================================================ MARKET MONTAGE
def SH_M(view):
    KEY='M_'+view
    if view=='family':
        flat(); setup_interior('evening',room=(0,0,3.1),res=PCT,samples=SAMPLES)
        fam=[person((3.0+dx,.5+dy,0),rz,c,'smile',name='fam%d'%i) for i,(dx,dy,rz,c) in enumerate([(-.9,0,-90,local(81)),(.9,0,90,local(82,female=True)),(0,-.8,0,local(83,kid=True)),(0,.8,180,local(84,kid=True))])]
        B2=Batch(); B2.box((3.0,.5,.2),(.7,.6,.03),M('#C9302C',.9,kind='fabric'),0)
        for k,c in enumerate(['#F4F1EA','#E8C25A','#C9302C']): B2.cyl((2.75+k*.25,.5,.25),.12,.05,M(c,.5),seg=12)
        B2.done('dastarkhwan')
        bk_=empty((0,0,0)); obox((0,0,0),(.12,.09,.015),M('#2E86C1',.6),.01,bk_)
        def upd(t):
            for i,H in enumerate(fam): blink(H,t); H['z0']=0; sit(H,1,.25,90); face(H,mouth='grin' if (t+i)%1.6<.8 else 'smile'); H['arm'][1].rotation_euler=(R(-60-15*math.sin(t*3+i)),0,0)
            bk_.location=hand_pos(fam[2],1)+Vector((0,0,.05))
            q=ease(t/DUR); camset((3.0,L(-2.4,-1.8,q),L(2.2,1.8,q)),(3.0,.5,.6),24,5.0,focus=(3.0,.5,.7))
        return dict(upd=upd)
    mood={'market':'dusk','shop':'haze','rider':'hotday','labour':'hotday','student':'dusk'}[view]
    street_day(mood,seed={'market':31,'shop':32,'rider':33,'labour':34,'student':35}[view],x0=-22,x1=22)
    if view=='market':
        D=person((0,0,0),90,DAN,'smile',name='dan'); ppl=crowd([(-3,-4.4,90),(2,-4.6,-90),(5,-3.8,-90),(-6,-4.2,90),(8,-4.5,-90),(1,-3.6,90)],110)
        B2=Batch(); r=random.Random(5)
        for k in range(6):
            x=-8+k*3.4; B2.box((x,-3.2,.85),(.8,.45,.05),M('#7A5A3A',.7,kind='wood'),.02)
            for j in range(10): B2.ico((x-.6+j*.13,-3.2+r.uniform(-.25,.25),.98),.08,M(r.choice(['#E2562E','#F2C12E','#5FA84A','#C9302C']),.5),sub=1)
            for sx in (-.7,.7): B2.cyl((x+sx,-3.2,.4),.03,.8,M('#5A5F66',.5,metal=.5),seg=6)
            B2.box((x,-3.2,2.1),(.9,.6,.02),M(r.choice(['#C0392B','#2E86C1','#E67E22','#16A0A0']),.8,kind='fabric'),.01)
            B2.ico((x,-3.2,1.95),.08,M('#FFE6B0',.3,emit=12),sub=1)
        B2.done('stalls')
        def upd(t):
            for c_ in ppl: blink(c_,t); walker(c_,(c_['x'],c_['y'],.0),c_['rz'],.8,t,arm=16)
            x=-6+1.1*t; D['root'].location=(x,-4.0,.008); D['root'].rotation_euler[2]=R(90); walk(D,x,step=.55,arm=16); blink(D,t)
            look_at(D,(x+1,-3.2,1.0),.5); face(D,mouth='smile')
            camset((x+3.2,-1.4,1.7),(x+.3,-3.8,1.4),24,5.0)
        return dict(upd=upd)
    if view=='shop':
        K=person((0,-5.6,.18),180,local(97),'smile',name='k'); sh=obox((0,-6.75,1.3),(2.2,.04,1.2),M('#8A9098',.4,metal=.6),0)
        def upd(t):
            blink(K,t); stand(K,t); k=ease(t/(DUR*.8)); sh.location=(0,-6.72,1.3+2.2*k); sh.scale=(1,1,1)
            K['root'].location=(0,-5.9,.19); K['root'].rotation_euler[2]=R(180); arms(K,-170+40*(1-k),0,15,-170+40*(1-k),0,-15)
            if k>.95: K['root'].rotation_euler[2]=R(L(180,0,ease((t-DUR*.8)/.5))); face(K,mouth='grin')
            camset((1.6,-2.8,1.5),(0,-6.2,1.6),24,5.0)
        return dict(upd=upd)
    if view=='rider':
        R_=person((0,0,0),90,dict(SHER,pack='#E2562E',jacket='#2E86C1',cap='#2E86C1'),'flat',name='rider'); bk=mbike(0,-2,0,'#1E1E22'); traffic(8,6,y=(1.2,3.2),speed=(3,5),bus=True)
        haze_=[]
        def upd(t):
            x=-4+4.5*t; bk.location=(x,-2.0,.0); R_['root'].location=(x+.15,-2.0,.02); R_['root'].rotation_euler[2]=R(90); R_['z0']=0; sit(R_,1,.86,80); blink(R_,t)
            R_['arm'][1].rotation_euler=(R(-75),0,R(-12)); R_['arm'][-1].rotation_euler=(R(-75),0,R(12)); face(R_,mouth='flat',brow=-.03,eyes=.8)
            camset((x+3.2,-4.0,1.1),(x,-2.0,1.4),26,5.0,focus=(x,-2,1.4))
        return dict(upd=upd)
    if view=='labour':
        Ls=[person((0,0,0),90,dict(local(100+i),top='#D8C8A0',pants='#7A6A5A'),'flat',name='lab%d'%i) for i in range(3)]
        brick=M('#A8513A',.85,kind='concrete',sc=.5); loads=[]
        for i in range(3):
            e=empty((0,0,0))
            for k in range(3): obox((0,0,.09*k),(.22,.11,.045),brick,.005,e)
            loads.append(e)
        B2=Batch()
        for k in range(30): B2.box((5+(k%6)*.46,-5.6+(k//6%2)*.25,.26+.1*(k//12)),(.22,.11,.045),brick,.005)
        B2.box((-4,-5.6,.6),(1.2,.6,.6),M('#B8B0A0',.9,kind='concrete'),.02); B2.done('site')
        def upd(t):
            for i,(H,e) in enumerate(zip(Ls,loads)):
                x=-3+1.0*t+i*2.2; H['root'].location=(x,-5.3+.3*i,.19); H['root'].rotation_euler[2]=R(90); walk(H,x,step=.45,arm=0); blink(H,t)
                arms(H,-170,0,10,-170,0,-10); e.location=H['head'].matrix_world@Vector((0,0,1.25*H['u'])); face(H,mouth='flat',brow=-.04,eyes=.75)
            camset((2.6,-2.4,1.2),(0.0,-5.2,1.6),24,5.0)
        return dict(upd=upd)
    # student on the bus stop / walking with books
    ST=person((0,0,0),90,dict(local(120,kid=True),pack='#C0392B',h=.86),'smile',name='st'); bs=kbus(14,-2.0,180,5)
    def upd(t):
        x=-4+1.0*t; ST['root'].location=(x,-5.4,.19); ST['root'].rotation_euler[2]=R(90); walk(ST,x,step=.45,arm=14); blink(ST,t); face(ST,mouth='smile')
        bs.location[0]=14-3.0*t
        camset((x+2.6,-3.2,1.1),(x,-5.4,1.2),26,5.0)
    return dict(upd=upd)
for v in ('market','shop','rider','labour','student','family'): SHOTS['M_'+v]=(lambda v=v: SH_M(v))

# ============================================================ UNCLE RASHID
def SH_U(view):
    KEY='U_'+view; tube=shopset(); setup_interior('evening',room=(0,0,3.0),res=PCT,samples=SAMPLES); point((0,1.6,2.8),45,(.92,.97,1.0),.6); point((-1,-1.5,2.6),30,(1,.8,.6),.6)
    tube.scale=(0,0,0)   # no electricity
    U=person((.4,1.35,0),0,RASH,'smile',name='rashid'); D=person((-.3,-.55,0),180,DAN,'smile',name='dan')
    def upd(t):
        blink(U,t); blink(D,t); stand(U,t); stand(D,t)
        if view=='enter':
            walk_path(D,[(-1.0,-2.8),(-.3,-.55)],t,0,1.2,step=.55)
            if t>1.2: D['root'].rotation_euler[2]=R(180)
            talk(U,t,362,365,KEY,rest='smile',rate=6); talk(D,t,366,369,KEY,rest='smile') if t>wl(366,KEY)-.05 else None
            U['arm'][1].rotation_euler=(R(-120),0,R(-15+15*math.sin(t*5))) if t<wl(366,KEY) else (0,0,0); face(U,brow=.03)
            q=ease(t/DUR); camset((1.6,-1.9,1.55),(.2,1.2,1.75),26,4.0,focus=(.4,1.35,1.8))
        elif view=='fridge':
            talk(U,t,370,381,KEY,rest='smile',rate=6); U['root'].rotation_euler[2]=R(-25); U['arm'][-1].rotation_euler=(R(-60),R(0),R(-40)) if t<DUR*.7 else (0,0,0)
            if t>DUR*.75: face(D,mouth='grin'); D['root'].rotation_euler[1]=R(4*math.sin(t*14)); face(U,mouth='grin')
            q=ease(t/DUR); camset((L(-.9,-.6,q),-.2,1.95),(.4,1.35,1.85),L(28,34,q),3.0,focus=(.4,1.35,1.8))
        elif view=='money':
            talk(D,t,382,387,KEY,rest='o'); k=ease(t/.4); U['arm'][1].rotation_euler=(R(-70*k),0,R(-10)); U['arm'][-1].rotation_euler=(R(-70*k),0,R(10)); U['head'].rotation_euler[0]=R(22*k)
            face(U,mouth='flat',eyes=.75)
            q=ease(t/DUR); camset((1.3,-.3,1.75),(.4,1.2,1.4),28,3.5,focus=(.4,1.2,1.4))
        else:
            talk(U,t,388,406,KEY,rest='smile',rate=5); U['head'].rotation_euler=(R(6),0,R(10*math.sin(t*.6))); face(U,eyes=.8,brow=.02)
            if t>DUR*.85: D['head'].rotation_euler[0]=R(12*math.sin((t-DUR*.85)*8))
            q=ease(t/DUR); camset((L(-1.8,-1.4,q),-.4,1.7),(.2,1.0,1.8),L(26,32,q),4.0,focus=(.4,1.35,1.8))
    return dict(upd=upd)
for v in ('enter','fridge','money','guzara'): SHOTS['U_'+v]=(lambda v=v: SH_U(v))

# ============================================================ RAIN
def SH_R(view):
    KEY='R_'+view; street_day('rainy',seed=13,x0=-24,x1=24); rain((0,-3,0),9,420,5)
    fw=floodwater(-40,40,-4.6,4.6); fw2=floodwater(-40,40,-6.8,6.8)
    D=person((-1.0,-5.5,.18),180,DAN,'smile',name='dan'); S=person((0,-2,0),90,SHER,'flat',name='sher'); C=person((-3,-3,0),90,CHOTU,'grin',name='chotu')
    A=person((-6,-3,0),90,AMMI,'frown',name='ammi'); MN=person((0,0,0),90,DRIVER,'frown',name='man')
    bk=mbike(2.0,-2.0,0,'#C0392B'); kids=crowd([(-5,-2.4,90),(-6.2,-1.6,90)],70,'grin')
    for kk in kids: kk['root'].scale=(.75,.75,.75)
    cr=car(-4,1.6,'#8A9098',0)
    tg0=TK('R_baarish')
    def level(t): g=TK(KEY)+t-tg0; return max(0,min(.45,(g-2.0)*.07))
    def upd(t):
        lv=level(t); fw.location[2]=lv-.005; fw2.location[2]=max(0,lv-.18)
        for H in (D,S,C,A,MN): blink(H,t)
        hideH(A); hideH(MN)
        if view=='baarish':
            hideH(S); hideH(D); bk.location=(40,0,0)
            for i,kk in enumerate([C]+kids):
                x=-6+3.0*t-i*.8; kk['root'].location=(x,-2.4+.6*i,.008); kk['root'].rotation_euler[2]=R(90); run(kk,x)
                arms(kk,-160,0,25,-160,0,-25); face(kk,mouth='shout',brow=.08)
            talk(C,t,407,408,KEY,rest='shout',shapes=('shout','O'))
            q=ease(t/DUR); camset((L(.2,.8,q),-4.4,1.0),(L(-3,-1,q),-2.4,1.2),22,6.0)
        elif view=='cool':
            for kk in [C]+kids: kk['root'].location=(4+kk['seed']%3,-1,0)
            hideH(S); stand(D,t); D['root'].location=(-1.0,-5.4,.19); D['root'].rotation_euler[2]=R(180); k=ease(t/.5)
            D['arm'][1].rotation_euler=(R(-20),0,R(-80*k)); D['arm'][-1].rotation_euler=(R(-20),0,R(80*k))
            D['head'].rotation_euler[0]=R(-20*k); talk(D,t,409,415,KEY,rest='grin'); face(D,eyes=.6)
            q=ease(t/DUR); camset((-1.0,-2.6,1.2),(-1.0,-5.4,2.0),26,4.0,focus=(-1.0,-5.4,2.0))
        elif view in ('bike','road'):
            hideH(C); stand(D,t); x0=2.0
            bk.location=(x0,-2.0,lv*.15); S['root'].location=(x0+.15,-2.0,.02); S['root'].rotation_euler[2]=R(90); S['z0']=0; sit(S,1,.86,80)
            D['root'].location=(-.4,-3.6,.01); D['root'].rotation_euler[2]=R(heading_to(D,(x0,-2.0)))
            if view=='bike':
                S['arm'][1].rotation_euler=(R(-75),0,R(-12)); S['arm'][-1].rotation_euler=(R(-75+15*math.sin(t*14)),0,R(12)); talk(S,t,416,420,KEY,rest='O',shapes=('shout','O','o'))
                talk(D,t,421,422,KEY,rest='o') if t>wl(421,KEY)-.05 else None; look_at(S,(-.4,-3.6,1.9),ease((t-.6)/.3)); face(S,brow=.08)
                q=ease(t/DUR); camset((L(4.2,3.8,q),-4.4,1.3),(1.0,-2.6,1.4),24,5.0)
            else:
                talk(S,t,423,425,KEY,rest='frown',shapes=('shout','O')); face(D,mouth='flat',brow=-.02); look_at(S,(-.4,-3.6,1.9)); S['arm'][-1].rotation_euler=(R(-150),0,R(30))
                q=ease(t/DUR); camset((L(4.0,4.3,q),-4.6,1.5),(1.0,-2.8,1.4),24,5.0)
        elif view=='car':
            hideH(D); hideH(S); hideH(C); MN['root'].scale=(1,1,1)
            cr.location=(-3+.25*t,1.2,0); MN['root'].location=(cr.location[0]-2.6,1.2,.02); MN['root'].rotation_euler=(R(18),0,R(90)); walk(MN,t*.3,step=.4,arm=0)
            arms(MN,-90,0,10,-90,0,-10); talk(MN,t,426,431,KEY,rest='frown',shapes=('shout','O','frown')); face(MN,brow=-.05,brow_r=20)
            q=ease(t/DUR); camset((-3.8,-2.2,1.4),(-4.6,1.2,1.4),24,5.0,focus=(-5.4,1.2,1.6))
        elif view=='chotu':
            hideH(D); hideH(S); C['root'].location=(-1.5,-2.6,.008-.0); C['root'].rotation_euler=(0,0,R(30*math.sin(t*3)))
            arms(C,-150+40*math.sin(t*8),0,40,-150-40*math.sin(t*8),0,-40); C['root'].location[2]=.05*abs(math.sin(t*6)); talk(C,t,432,437,KEY,rest='grin')
            face(C,brow=.08); q=ease(t/DUR); camset((-.4,-4.4,.9),(-1.5,-2.6,1.0),26,4.0,focus=(-1.5,-2.6,1.0))
        else:
            hideH(D); hideH(S); A['root'].scale=(1,1,1); k=ease(t/.5)
            A['root'].location=(L(-4.0,-2.3,k),-2.6,.02); A['root'].rotation_euler[2]=R(90); walk(A,A['root'].location.x,step=.45,arm=20) if t<.5 else stand(A,t)
            C['root'].location=(-1.5+.0,-2.6,.008); C['root'].rotation_euler[2]=R(-90)
            arm_to(A,1,C['head'].matrix_world.translation+Vector((0,0,-.1)),k); talk(A,t,438,442,KEY,rest='frown',shapes=('shout','O','shout')); face(A,brow=-.06,brow_r=22)
            face(C,mouth='O',brow=.1); shock(C,.5)
            if t>1.0: C['root'].location[0]=-1.5-.8*(t-1.0); A['root'].location[0]=-2.3-.8*(t-1.0)
            q=ease(t/DUR); camset((-.6,-4.6,1.3),(-2.0,-2.6,1.4),24,4.0)
    return dict(upd=upd)
for v in ('baarish','cool','bike','road','car','chotu','ammi'): SHOTS['R_'+v]=(lambda v=v: SH_R(v))

# ============================================================ ROOFTOP NIGHT
def night_city():
    city(7,True,R_=150,ss=-1); objs=B.done('city')
    for o in objs: o.location[2]=-26
def SH_N(view):
    KEY='N_'+view; night_city(); roof(); B.done('roof'); setup_render('nightc',res=PCT,samples=SAMPLES,shadow_dist=30)
    for x,y,e in ((-3,2,120),(3,0,80)): point((x,y,2.6),e,(1,.8,.6),.5)
    area((0,-8.5,2.4),900,(5,3),(.7,.8,1.0),rot=(R(-90),0,0),shadow=False); area((2.5,-1.0,3.2),260,(2,2),(1,.78,.55),rot=(R(35),0,R(160)),shadow=False)
    D=person((-.6,-4.0,0),0,DAN,'flat',name='dan'); S=person((.6,-4.0,0),0,SHER,'flat',name='sher')
    def upd(t):
        for H,x in ((D,-.5),(S,.5)):
            blink(H,t); stand(H,t); H['root'].location=(x,-4.55,.008)
            H['arm'][1].rotation_euler=(R(-50),0,0); H['arm'][-1].rotation_euler=(R(-50),0,0)
        D['root'].rotation_euler[2]=R(-8); S['root'].rotation_euler[2]=R(8)
        if view=='roof':
            talk(S,t,443,452,KEY,rest='flat',rate=6); look_at(S,(-.5,-4.55,1.9),.5); face(D,mouth='flat',eyes=.85)
            q=ease(t/DUR); camset((L(.2,0,q),L(1.4,.6,q),L(2.4,2.1,q)),(0,-6,L(1.4,1.2,q)),24,5.0,focus=(0,-4.6,1.8))
        elif view=='socha':
            talk(D,t,453,456,KEY,rest='flat',rate=5); face(D,eyes=.8,brow=.02); look_at(D,(-2,-40,8),.6)
            camset((-1.4,-5.4,1.85),(-.5,-4.55,1.95),34,2.8,focus=(-.5,-4.55,1.95))
        elif view=='kyun':
            talk(S,t,457,463,KEY,rest='flat',rate=6); look_at(S,(-.5,-4.55,1.9),.9)
            camset((-.3,-5.7,1.85),(.5,-4.55,1.95),32,2.8,focus=(.5,-4.55,1.95))
        elif view=='ghar':
            talk(D,t,464,477,KEY,rest='smile',rate=6); look_at(D,(.5,-4.55,1.9),ease(t/1.0)*.8); face(D,brow=.02,eyes=.9)
            q=ease(t/DUR); camset((L(.5,.3,q),-5.9,1.85),(-.5,-4.55,1.95),L(30,36,q),2.8,focus=(-.5,-4.55,1.95))
        else:
            talk(D,t,478,490,KEY,rest='flat',rate=6); D['head'].rotation_euler[0]=R(18); look_at(D,(0,-40,-20),.5); face(D,brow=-.02,brow_r=10)
            q=ease(t/DUR); camset((.4,L(-6.6,-7.0,q),L(.8,.6,q)),(-.4,-4.55,1.9),28,4.0,focus=(-.5,-4.55,1.9))
    return dict(upd=upd)
for v in ('roof','socha','kyun','ghar','comp'): SHOTS['N_'+v]=(lambda v=v: SH_N(v))

# ============================================================ FINAL CITY
def SH_F(view):
    KEY='F_'+view; night_city(); roof(); B.done('roof'); setup_render('nightc',res=PCT,samples=SAMPLES,shadow_dist=60)
    area((0,-8.5,2.4),900,(5,3),(.7,.8,1.0),rot=(R(-90),0,0),shadow=False)
    D=person((-.5,-4.55,0),-8,DAN,'flat',name='dan'); S=person((.5,-4.55,0),8,SHER,'flat',name='sher')
    def upd(t):
        for H in (D,S): blink(H,t); stand(H,t); H['arm'][1].rotation_euler=(R(-50),0,0); H['arm'][-1].rotation_euler=(R(-50),0,0)
        q=ease(t/DUR)
        if view=='rise': camset((0,L(1.0,10,q),L(2.6,40,q)),(0,L(-8,-110,q),L(1.0,-8,q)),24,8.0)
        elif view=='coast': camset((L(-30,30,q),L(20,0,q),55),(L(-20,20,q),-150,-20),24,8.0)
        else: camset((0,L(10,30,q),L(45,70,q)),(0,-130,L(-15,-10,q)),L(24,20,q),8.0)
    return dict(upd=upd)
for v in ('rise','coast','final'): SHOTS['F_'+v]=(lambda v=v: SH_F(v))
