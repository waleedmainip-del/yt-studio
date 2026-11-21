SHOTS={}
WJ=json.load(open('/home/claude/train/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('T_intro',0),('T_bags',15),('T_unfort',27),('P_dani',35),('P_bilal',40),('P_snacks',47),('P_sherry',53),('P_faizan',63),
    ('D_wave',75),('D_chaar',81),('D_emotion',89),('D_chips',93),('D_pass',105),('D_charger',114),
    ('C_uncle',119),('C_changa',126),('C_door',131),('C_google',139),('C_bolde',148),('C_bilal',152),
    ('F_vendor',160),('F_idhar',163),('F_kitna',166),('F_dani',176),('F_bharosa',183),('F_paratha',188),('F_ekaur',194),('F_sherry',198),('F_research',209),
    ('N_voice',214),('N_bilal',227),('N_snore',233),('N_engine',236),('N_wake',243),('N_khana',249),
    ('L_arrive',253),('L_made',258),('L_bag',262),('L_dosti',269),('L_owner',278),('L_welcome',282),
    ('O_driver',286),('O_best',299),('O_conf',306),('O_car',320),
    ('Z_food',333),('Z_bilal',339),('Z_dil',343),('Z_rishta',354),('Z_call',362),('Z_settle',371),('Z_final',381)]
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

def lift(H,z): H['root'].location[2]=z; H['z0']=z
def stand_at(H,t,x,y,z,rz):
    H['root'].location=(x,y,z); H['z0']=z; stand(H,t); H['root'].location[2]=z; H['root'].rotation_euler[2]=R(rz)
def suitcase(x,y,z,col,s=1.0):
    e=empty((x,y,z)); obox((0,0,.55*s),(.42*s,.22*s,.55*s),M(col,.4),.05*s,e); obox((0,0,1.18*s),(.12*s,.03,.08*s),M('#22242B',.5),.01,e)
    for dx in (-.3,.3): ocyl((dx*s,0,.05),.05,.05,M('#1E1E22',.6),e,rot=(R(90),0,0),seg=8)
    return e
def gang(z=1.0,y=-4.6,x0=-1.5):
    D=person((x0,y,z),0,DANI,'grin',name='dani'); S=person((x0+1.0,y,z),0,SHERY,'smile',name='sherry')
    F=person((x0+2.0,y,z),0,FAIZ,'smile',name='faizan'); Bl=person((x0+3.0,y,z),0,BILAL,'flat',name='bilal')
    for H in (D,S,F,Bl): H['z0']=z
    return D,S,F,Bl

# ============================================================ PLATFORM (Karachi Cantt, morning)
def SH_T(view):
    KEY=view; key=KEY
    platform('KARACHI CANTT',seed=1); tr=train(30,0,4); B.done('platform'); setup_render('morning',res=PCT,samples=SAMPLES,shadow_dist=60)
    D,S,F,Bl=gang(); bags=[suitcase(0,0,0,c,1.35) for c in ('#C0392B','#8E44AD','#2E86C1','#27AE60')]
    peds=crowd([(-14,-6,90),(10,-7,-90),(16,-5.5,-90),(-8,-8.5,0),(4,-8.8,0)],60)
    for c in peds: lift(c,1.0)
    fb=empty((0,0,0))
    for k in range(9): oico((-.25+.12*(k%5),-.1+.1*(k//5),.32+.05*(k%3)),.09,M(random.choice(['#E2562E','#F2C12E','#C0392B','#27AE60','#F4F1EA']),.5),fb,sub=1)
    obox((0,0,0),(.4,.25,.3),M('#2E86C1',.6,kind='fabric'),.05,fb); fb.scale=(0,0,0)
    def bg(t):
        for i,c in enumerate(peds):
            blink(c,t)
            if i<3: walker(c,(c['x'],c['y'],1.0),c['rz'],.9,t,arm=18); c['root'].location[2]=1.0
            else: stand(c,t); c['root'].location[2]=1.0; gaze_idle(c,t)
    def gangpose(t,walkk=None):
        for i,(H,b) in enumerate(zip((D,S,F,Bl),bags)):
            blink(H,t)
            if walkk is None: stand_at(H,t,-1.5+1.3*i,-4.6,1.0,0)
            b.location=H['root'].location+Vector((.55,.15,0)); H['arm'][1].rotation_euler=(R(-8),0,R(8))
    if view=='T_intro':
        def upd(t):
            bg(t); gangpose(t); tr.location[0]=30
            q=ease(t/DUR); camset((L(-16,-10,q),L(-9.5,-8.6,q),L(4.0,2.8,q)),(L(-4,0,q),-2,2.2),22,8.0)
        return dict(upd=upd)
    if view=='T_bags':
        def upd(t):
            bg(t)
            for i,(H,b) in enumerate(zip((D,S,F,Bl),bags)):
                blink(H,t); x=-9+1.1*t+i*.2; y=-4.2-1.0*i*.0-.0+(-1.0 if i%2 else 0)
                H['root'].location=(x-i*1.4,-4.6+(.9 if i%2 else 0),1.0); H['z0']=1.0; H['root'].rotation_euler[2]=R(90); walk(H,x+i,step=.5,arm=14); H['root'].location[2]=1.0
                b.location=H['root'].location+Vector((-.55,.55,0)); H['arm'][1].rotation_euler=(R(10),0,R(-20)); face(H,mouth='grin')
            q=ease(t/DUR); camset((L(-3.5,-1.5,q),-8.2,1.9),(L(-8,-5,q),-4.4,1.8),24,6.0)
        return dict(upd=upd)
    if view=='T_unfort':
        def upd(t):
            bg(t); gangpose(t)
            for i,H in enumerate((D,S,F,Bl)):
                hips(H,ease((t-.2*i)/.4)); face(H,mouth='smirk',brow=-.02,brow_r=-10); H['head'].rotation_euler[0]=R(-6)
            q=ease(t/DUR); camset((0,L(-9.4,-8.2,q),L(1.6,1.4,q)),(0,-4.6,2.0),L(22,26,q),5.0)
        return dict(upd=upd)
    def upd(t):
        bg(t); gangpose(t)
        if view=='P_dani':
            k=ease(t/.3); arms(D,-170*k,0,25,-170*k,0,-25); D['root'].location[2]=1.0+.15*abs(math.sin(t*5))*k; talk(D,t,35,39,KEY,rest='grin'); face(D,brow=.1)
            for H in (S,F,Bl): look_at(H,D['root'].location+Vector((0,0,1.9)),.6)
            q=ease(t/DUR); camset((-1.5,-7.2,1.5),(-1.5,-4.6,2.4),24,4.0,focus=(-1.5,-4.6,2.0))
        elif view=='P_bilal':
            talk(Bl,t,40,46,KEY,rest='flat'); Bl['arm'][1].rotation_euler=(R(-80),0,R(-60)); face(Bl,brow=-.03,brow_r=14); look_at(Bl,(-1.5,-4.6,2.0),.7)
            q=ease(t/DUR); camset((2.6,-7.0,1.75),(2.4,-4.6,2.05),30,3.5,focus=(2.4,-4.6,2.05))
        elif view=='P_snacks':
            fb.scale=(1,1,1); fb.location=(1.1,-5.3,1.0); talk(F,t,47,52,KEY,rest='grin'); F['head'].rotation_euler[0]=R(25); F['arm'][1].rotation_euler=(R(-50),0,R(-20)); F['arm'][-1].rotation_euler=(R(-50),0,R(20))
            for H in (D,S,Bl): look_at(H,(1.1,-5.3,1.2),.8); face(H,mouth='O')
            q=ease(t/DUR); camset((1.7,L(-7.6,-7.2,q),1.9),(1.1,-4.9,1.7),22,4.0,focus=(1.1,-5.0,1.6))
        elif view=='P_sherry':
            fb.scale=(1,1,1); fb.location=(1.1,-5.3,1.0); talk(S,t,53,62,KEY,rest='O'); shock(S,.6); face(S,brow=.12,eyes=1.15); look_at(S,(1.1,-5.3,1.2),.6)
            q=ease(t/DUR); camset((-.6,-7.0,1.8),(-.2,-4.6,2.05),30,3.5,focus=(-.2,-4.6,2.05))
        else:
            fb.scale=(1,1,1); fb.location=F['root'].location+Vector((0,-.45,.9)); talk(F,t,63,74,KEY,rest='smile'); F['arm'][1].rotation_euler=(R(-70),0,R(30)); F['arm'][-1].rotation_euler=(R(-70),0,R(-30))
            face(F,brow=-.02,brow_r=-8)
            q=ease(t/DUR); camset((1.2,-7.2,1.7),(1.1,-4.6,2.0),28,3.5,focus=(1.1,-4.6,2.0))
    return dict(upd=upd)
for v in ('T_intro','T_bags','T_unfort','P_dani','P_bilal','P_snacks','P_sherry','P_faizan'): SHOTS[v]=(lambda v=v: SH_T(v))

# ============================================================ TRAIN (compartment)
def inside(night=False,move=True):
    compartment(night); clutter(3); B.done('comp')
    if night: setup_interior('night',room=(0,0,2.6),res=PCT,samples=SAMPLES); point((0,0,2.5),35,(.95,.95,1.0),.5); point((2.6,0,2.5),18,(.95,.95,1.0),.5)
    else: setup_interior('evening',room=(0,0,2.6),res=PCT,samples=SAMPLES); point((0,0,2.5),25,(1,.97,.9),.5); point((-2.6,0,2.5),15,(1,.97,.9),.5); point((2.6,0,2.5),15,(1,.97,.9),.5)
    ov=outside_view(night)
    if move:
        for e,x0,d in ov:
            def fn(o,t,x0=x0,d=d): sp=14.0/max(1,d/4); o.location=(((x0-sp*t)+40)%80-40,1.6+d,0)
            fx.add(e,fn)
    return ov
def cam_on(H,lens=20,fs=4.0):
    bpy.context.view_layer.update(); hp_=H['head'].matrix_world.translation.copy(); sy=1 if H['root'].location.y>0 else -1
    pos=(hp_.x+.3,-sy*.45,1.72); camset(pos,(hp_.x,hp_.y,hp_.z-.12),lens,fs,focus=tuple(hp_))
def SH_D(view):
    KEY=view; night=view.startswith('N_')
    inside(night)
    D=person((-1.0,1.1,0),0,DANI,'smile',name='dani'); S=person((-.35,1.1,0),0,SHERY,'smile',name='sherry')
    U=person((-.6,-1.1,0),180,UNC,'smile',name='uncle'); Bl=person((.05,-1.1,0),180,BILAL,'flat',name='bilal')
    F=person((.3,1.1,0),0,FAIZ,'smile',name='faizan'); P=person((2.2,-1.1,0),180,PASS,'flat',name='pass')
    chips=empty((0,0,0)); obox((0,0,0),(.08,.03,.12),M('#E2562E',.4),.01,chips); chips.scale=(0,0,0)
    ph=phone(D,1); ph2=phone(S,1,'#FFB86A'); ph.scale=(0,0,0); ph2.scale=(0,0,0)
    par=empty((0,0,0)); ocyl((0,0,0),.16,.02,M('#D8A050',.7),par,rot=(0,0,0),seg=16); par.scale=(0,0,0)
    if view in ('D_chaar','D_emotion','D_chips','D_pass','D_charger'): hideH(U)
    vend=person((-6,-.9,0),90,VEND,'shout',name='vend') if view in ('F_vendor','F_idhar','F_kitna') else None
    tray=None
    if vend:
        tray=empty((0,0,0)); obox((0,0,0),(.35,.22,.02),M('#C9CDD6',.3,metal=.7),.01,tray)
        for k in range(5): ocyl((-.24+k*.12,0,.06),.04,.09,M('#F4F1EA',.4),tray,rot=(0,0,0),seg=8)
    def seat(H,x,y,rz,t):
        blink(H,t); H['root'].location=(x,y,.008); H['root'].rotation_euler=(0,0,R(rz)); H['z0']=0; sit(H,1,.48,90)
    def base(t):
        SHAKE[0]=.004
        seat(D,-1.0,1.1,0,t); seat(S,-.35,1.1,0,t); seat(U,-.6,-1.1,180,t); seat(Bl,.05,-1.1,180,t); seat(F,.3,1.1,0,t); seat(P,2.2,-1.1,180,t)
        if view not in ('D_pass','D_charger','N_snore'): hideH(P)
    def upd(t):
        base(t)
        if night:
            for H in (U,P): face(H,mouth='flat',eyes=.0)
        if view=='D_chaar':
            talk(Bl,t,81,88,KEY,rest='flat'); look_at(Bl,(-1.0,1.1,1.4),.8); face(Bl,brow=-.02,brow_r=12); hideH(U)
            q=ease(t/DUR); cam_on(Bl)
        elif view=='D_emotion':
            talk(D,t,89,92,KEY,rest='smile'); D['arm'][1].rotation_euler=(R(-60),0,R(-60)); face(D,brow=.06,eyes=.8); D['head'].rotation_euler[0]=R(-12)
            q=ease(t/DUR); cam_on(D)
        elif view=='D_chips':
            chips.scale=(1,1,1); chips.location=hand_pos(F,1); F['arm'][1].rotation_euler=(R(-70),0,R(10)); F['arm'][-1].rotation_euler=(R(-70+20*math.sin(t*6)),0,R(-10))
            talk(S,t,93,97,KEY,rest='flat'); talk(F,t,98,104,KEY,rest='grin') if t>wl(98,KEY)-.05 else None; look_at(S,(.3,1.1,1.3),.7)
            q=ease(t/DUR); cam_on(S)
        elif view=='D_pass':
            talk(P,t,105,111,KEY,rest='frown'); look_at(P,(-1.0,1.1,1.4),.8); face(P,brow=-.03,brow_r=14); talk(D,t,112,113,KEY,rest='grin') if t>wl(112,KEY)-.05 else None
            if t>wl(112,KEY): D['arm'][1].rotation_euler=(R(-100),0,R(-20))
            q=ease(t/DUR); cam_on(P)
        elif view=='D_charger':
            D['root'].location=(-.6,.2,.008); stand(D,t); D['root'].rotation_euler[2]=R(-20); arms(D,-150,0,25,-30,0,-20)
            talk(D,t,114,118,KEY,rest='shout',shapes=('shout','O','shout')); face(D,brow=.08); look_at(P,(-.2,.2,2.0),.8); face(P,mouth='O',brow=.1)
            for H in (S,Bl,F): face(H,mouth='o')
            q=ease(t/DUR); cam_on(D)
        elif view=='C_uncle':
            talk(U,t,119,122,KEY,rest='smile',rate=6); talk(D,t,123,125,KEY,rest='grin') if t>wl(123,KEY)-.05 else None; look_at(U,(-1.0,1.1,1.4),.8)
            q=ease(t/DUR); cam_on(U)
        elif view=='C_changa':
            talk(U,t,126,130,KEY,rest='grin',rate=6); U['arm'][-1].rotation_euler=(R(-110),0,R(30)); U['root'].rotation_euler[1]=R(3*math.sin(t*8)); face(U,brow=.06)
            q=ease(t/DUR); cam_on(U)
        elif view=='C_door':
            talk(S,t,131,135,KEY,rest='o'); talk(U,t,136,138,KEY,rest='smile',rate=5) if t>wl(136,KEY)-.05 else None; look_at(S,(-.6,-1.1,1.4),.8)
            q=ease(t/DUR); cam_on(S)
        elif view=='C_google':
            talk(S,t,139,147,KEY,rest='smirk'); S['arm'][1].rotation_euler=(R(-80),0,R(-30+20*math.sin(t*5))); face(S,brow=.04,brow_r=-10); look_at(S,(-.6,-1.1,1.4),.8)
            q=ease(t/DUR); cam_on(S)
        elif view=='C_bolde':
            talk(U,t,148,151,KEY,rest='grin',rate=6); U['root'].rotation_euler[1]=R(5*math.sin(t*12)); face(U,brow=.04,eyes=.6)
            for H in (D,S): face(H,mouth='grin')
            q=ease(t/DUR); cam_on(U)
        elif view=='C_bilal':
            talk(Bl,t,152,159,KEY,rest='flat'); Bl['head'].rotation_euler=(R(10),0,R(-20)); Bl['arm'][-1].rotation_euler=(R(-130),0,R(-20)); face(Bl,eyes=.7,brow=-.03)
            q=ease(t/DUR); cam_on(Bl)
        elif view in ('F_vendor','F_idhar','F_kitna'):
            vx=L(-6,-.9,ease(min(1,t/2.0))) if view=='F_vendor' else -.9
            stand_at(vend,t,vx,-.2,.008,90); walk(vend,vx,step=.5,arm=0) if view=='F_vendor' and t<2.0 else None
            vend['arm'][1].rotation_euler=(R(-80),0,R(-20)); tray.location=hand_pos(vend,1)+Vector((.1,.2,.02)); blink(vend,t)
            if view=='F_vendor': talk(vend,t,160,162,KEY,rest='shout',shapes=('shout','O')); q=ease(t/DUR); camset((2.2,-1.4,1.5),(-2.0,-.9,1.7),24,5.0)
            elif view=='F_idhar':
                k=ease(t/.3); F['root'].location=(.3,.6,.008); stand(F,t); F['root'].rotation_euler[2]=R(0); F['arm'][1].rotation_euler=(R(-160*k),0,R(20+20*math.sin(t*10)))
                talk(F,t,163,165,KEY,rest='shout',shapes=('shout','O')); face(F,brow=.1); q=ease(t/DUR); cam_on(F)
            else:
                F['root'].location=(.3,.6,.008); stand(F,t); F['root'].rotation_euler[2]=R(-20); F['arm'][1].rotation_euler=(R(-80),0,R(20))
                talk(Bl,t,166,167,KEY,rest='flat'); talk(F,t,168,175,KEY,rest='grin') if t>wl(168,KEY)-.05 else None; look_at(Bl,(.3,1.1,1.3),.7)
                q=ease(t/DUR); cam_on(F)
        elif view=='F_dani':
            talk(D,t,176,182,KEY,rest='smirk'); D['arm'][1].rotation_euler=(R(-70),0,R(-30)); look_at(D,(.3,1.1,1.3),.7)
            q=ease(t/DUR); cam_on(D)
        elif view=='F_bharosa':
            talk(F,t,183,187,KEY,rest='flat'); F['arm'][1].rotation_euler=(R(-60),0,R(-20)); face(F,brow=-.03,brow_r=12); look_at(F,(-1.0,1.1,1.3),.6)
            q=ease(t/DUR); cam_on(F)
        elif view=='F_paratha':
            par.scale=(1,1,1); U['arm'][1].rotation_euler=(R(-90*ease(t/.5)),0,R(-50)); par.location=hand_pos(U,1)+Vector((0,0,.05)); talk(U,t,188,193,KEY,rest='smile',rate=6); look_at(U,(.3,1.1,1.3))
            q=ease(t/DUR); cam_on(U)
        elif view=='F_ekaur':
            par.scale=(1,1,1); par.location=hand_pos(F,1)+Vector((0,0,.05)); F['arm'][1].rotation_euler=(R(-110),0,R(10)); k=ease((t-.3)/.3)
            talk(F,t,194,197,KEY,rest='O',shapes=('O','shout','O','grin')); face(F,eyes=1+.4*k,brow=.12*k); F['root'].location[2]=.008+.05*k
            q=ease(t/DUR); cam_on(F)
        elif view=='F_sherry':
            talk(S,t,198,208,KEY,rest='O'); S['arm'][1].rotation_euler=(R(-95),0,R(-55)); face(S,brow=.1,eyes=1.1); look_at(S,(.3,1.1,1.3),.8)
            q=ease(t/DUR); cam_on(S)
        elif view=='F_research':
            par.scale=(1,1,1); par.location=hand_pos(F,1); F['arm'][1].rotation_euler=(R(-100+15*math.sin(t*6)),0,R(10)); talk(F,t,209,213,KEY,rest='flat',rate=6); face(F,brow=-.02,brow_r=-6)
            q=ease(t/DUR); cam_on(F)
        elif view=='N_voice':
            ph.scale=(1,1,1); ph2.scale=(1,1,1); D['arm'][1].rotation_euler=(R(-110),0,R(10)); talk(D,t,214,226,KEY,rest='grin')
            S['arm'][1].rotation_euler=(R(-150),0,R(-20)); face(S,mouth=('grin','smirk','O')[int(t*1.5)%3]); hideH(Bl) if False else None
            q=ease(t/DUR); cam_on(D)
        elif view=='N_bilal':
            Bl['root'].location=(.05,-1.1,.55); Bl['root'].rotation_euler=(R(-75),0,R(180)); talk(Bl,t,227,232,KEY,rest='frown'); face(Bl,brow=-.05,brow_r=18)
            q=ease(t/DUR); cam_on(Bl)
        elif view in ('N_snore','N_engine'):
            F['root'].rotation_euler=(R(-60),0,R(0)); F['root'].location=(.3,1.1,.3); face(F,mouth='O' if (t*2.2)%1<.5 else 'o',eyes=0.0)
            SHAKE[0]=.02*abs(math.sin(t*14))
            if view=='N_snore':
                P['root'].location=(-.9,-.62,.008); talk(P,t,233,235,KEY,rest='O',shapes=('shout','O')); face(P,brow=.1,eyes=1.2); shock(P,.5)
                q=ease(t/DUR); cam_on(P if view=='N_snore' else S)
            else:
                talk(S,t,236,242,KEY,rest='smirk'); S['arm'][1].rotation_euler=(R(-80),0,R(-60)); look_at(S,(.3,1.1,.9),.6)
                q=ease(t/DUR); cam_on(P if view=='N_snore' else S)
        elif view=='N_wake':
            F['root'].rotation_euler=(R(-60),0,R(0)); F['root'].location=(.3,1.1,.3); face(F,eyes=0.0,mouth='O')
            D['root'].location=(.3,.3,.008); stand(D,t); D['root'].rotation_euler[2]=R(0); arm_reach(D,1,F['root'].location+Vector((0,0,1.2)),1.0); D['arm'][1].rotation_euler[0]+=R(10*math.sin(t*16))
            talk(D,t,243,248,KEY,rest='shout',shapes=('shout','O','shout')); face(D,brow=.08)
            q=ease(t/DUR); cam_on(F)
        elif view=='N_khana':
            k=ease(t/.15); F['root'].location=(.3,1.1,.008); F['root'].rotation_euler=(R(-60*(1-k)),0,R(0)); F['z0']=0; sit(F,1,.48,90)
            talk(F,t,249,252,KEY,rest='O',shapes=('shout','O','shout')); face(F,eyes=1.3,brow=.14); arms(F,-140*k,0,25,-140*k,0,-25); SHAKE[0]=.02
            q=ease(t/DUR); cam_on(F)
    return dict(upd=upd)
for v in ('D_chaar','D_emotion','D_chips','D_pass','D_charger','C_uncle','C_changa','C_door','C_google','C_bolde','C_bilal',
          'F_vendor','F_idhar','F_kitna','F_dani','F_bharosa','F_paratha','F_ekaur','F_sherry','F_research',
          'N_voice','N_bilal','N_snore','N_engine','N_wake','N_khana'): SHOTS[v]=(lambda v=v: SH_D(v))

# ============================================================ DEPARTURE (exterior)
def SH_wave():
    platform('KARACHI CANTT',seed=1); tr=train(30,0,4); B.done('platform'); setup_render('morning',res=PCT,samples=SAMPLES,shadow_dist=60)
    D=person((0,-1.28,1.25),0,DANI,'shout',name='dani'); peds=crowd([(-6,-5,0),(-2,-6,0),(3,-5.5,0),(6,-6.2,0)],61)
    for c in peds: lift(c,1.0)
    def upd(t):
        x=30+.3*t*t; tr.location[0]=x; D['root'].location=(x-30-30.7,-1.55,1.64); D['root'].rotation_euler=(0,0,0); D['z0']=1.64; blink(D,t)
        for s_ in (-1,1): D['leg'][s_].scale=(0,0,0)
        D['arm'][1].rotation_euler=(R(-165),0,R(20+30*math.sin(t*9))); D['arm'][-1].rotation_euler=(R(-165),0,R(-20-30*math.sin(t*9+1)))
        talk(D,'D_wave' and t,75,80,'D_wave',rest='shout',shapes=('shout','O','shout','grin')); face(D,brow=.1)
        for i,c in enumerate(peds): blink(c,t); stand(c,t); c['root'].location[2]=1.0; look_at(c,D['root'].location+Vector((0,0,2)),.6); face(c,mouth='o')
        dx=D['root'].location.x; camset((dx-2.5,-4.6,1.7),(dx,-1.3,2.6),24,4.5,focus=(dx,-1.3,2.6))
    return dict(upd=upd)
SHOTS['D_wave']=SH_wave

# ============================================================ LAHORE ARRIVAL
def SH_L(view):
    KEY=view
    platform('LAHORE JUNCTION',roof='#7A1E2E',col='#C9705A',seed=7,lahore=True); tr=train(30,0,4); B.done('platform'); setup_render('dawn',res=PCT,samples=SAMPLES,shadow_dist=60)
    D,S,F,Bl=gang(); bags=[suitcase(0,0,0,c,1.35) for c in ('#C0392B','#8E44AD','#2E86C1','#27AE60')]
    ow_bag=suitcase(0,0,0,'#1E1E22',1.35); OW=person((6,-5,1.0),-90,OWNR,'shout',name='owner'); lift(OW,1.0)
    peds=crowd([(-12,-6.5,90),(9,-7,-90),(-6,-8.5,0),(12,-5.5,-90)],62)
    for c in peds: lift(c,1.0)
    def bg(t):
        for i,c in enumerate(peds):
            blink(c,t)
            if i<2: walker(c,(c['x'],c['y'],1.0),c['rz'],.9,t,arm=18); c['root'].location[2]=1.0
            else: stand(c,t); c['root'].location[2]=1.0
    def upd(t):
        bg(t)
        if view=='L_arrive':
            for H in (D,S,F,Bl,OW): hideH(H)
            for b in bags+[ow_bag]: b.scale=(0,0,0)
            x=L(-40,30,ease_out(min(1,t/DUR))); tr.location[0]=x
            q=ease(t/DUR); camset((L(18,14,q),-8.8,L(3.6,2.6,q)),(L(0,8,q),0,2.2),22,8.0)
            return
        tr.location[0]=30
        for i,(H,b) in enumerate(zip((D,S,F,Bl),bags)):
            blink(H,t); stand_at(H,t,-1.5+1.3*i,-4.6,1.0,0); b.location=H['root'].location+Vector((.55,.15,0))
        OW['root'].scale=(1,1,1) if view in ('L_owner','L_welcome') else (0,0,0)
        if view=='L_made':
            for i,H in enumerate((D,S,F,Bl)): k=ease((t-.1*i)/.3); arms(H,-165*k,0,25,-165*k,0,-25); H['root'].location[2]=1.0+.25*abs(math.sin(t*6+i))*k; face(H,mouth='shout' if i==0 else 'grin',brow=.08)
            talk(D,t,258,261,KEY,rest='shout',shapes=('shout','O'))
            q=ease(t/DUR); camset((0,-8.6,1.3),(0,-4.6,2.4),22,5.0)
            ow_bag.scale=(0,0,0)
        else:
            ow_bag.location=S['root'].location+Vector((-.5,-.3,0)); bags[1].location=(-1.0,-3.6,1.0)
            S['arm'][-1].rotation_euler=(R(-20),0,R(20))
            if view=='L_bag':
                talk(Bl,t,262,268,KEY,rest='O'); Bl['arm'][1].rotation_euler=(R(-95),0,R(60)); look_at(Bl,S['root'].location+Vector((0,0,1.5)),.8); face(Bl,brow=.1)
                q=ease(t/DUR); camset((1.0,-7.6,1.8),(0.4,-4.8,1.8),26,4.0)
            elif view=='L_dosti':
                talk(S,t,269,277,KEY,rest='smirk'); S['arm'][1].rotation_euler=(R(-70),0,R(-40)); face(S,brow=.02,brow_r=-10)
                q=ease(t/DUR); camset((-.4,-7.0,1.75),(-.2,-4.6,2.05),30,3.5,focus=(-.2,-4.6,2.05))
            elif view=='L_owner':
                ox=L(6,1.2,ease(min(1,t/1.0))); OW['root'].location=(ox,-5.6,1.0); OW['z0']=1.0; OW['root'].rotation_euler[2]=R(-90); walk(OW,ox,step=.6,arm=30) if t<1.0 else stand(OW,t); OW['root'].location[2]=1.0
                OW['arm'][1].rotation_euler=(R(-150),0,R(20+25*math.sin(t*9))); talk(OW,t,278,281,KEY,rest='shout',shapes=('shout','O','shout')); face(OW,brow=-.06,brow_r=24)
                look_at(S,OW['root'].location+Vector((0,0,2)),.8); face(S,mouth='O',eyes=1.2,brow=.1)
                q=ease(t/DUR); camset((-1.6,-8.2,1.9),(1.2,-5.0,2.0),24,5.0)
            else:
                OW['root'].location=(1.2,-5.6,1.0); OW['root'].rotation_euler[2]=R(-90); stand(OW,t); OW['root'].location[2]=1.0; hips(OW); face(OW,mouth='frown',brow=-.05,brow_r=20)
                ow_bag.location=S['root'].location+Vector((-.5,-.3,-.15*ease(t/.3))); talk(S,t,282,285,KEY,rest='grin'); S['arm'][1].rotation_euler=(R(-100),0,R(-20)); face(S,brow=.06)
                q=ease(t/DUR); camset((-.3,-7.6,1.7),(.4,-5.0,2.0),26,4.0)
    return dict(upd=upd)
for v in ('L_arrive','L_made','L_bag','L_dosti','L_owner','L_welcome'): SHOTS[v]=(lambda v=v: SH_L(v))

# ============================================================ OUTSIDE LAHORE JUNCTION
def SH_O(view):
    KEY=view; lahore_junction(); B.done('ljn'); setup_render('morning_s',res=PCT,samples=SAMPLES,shadow_dist=80)
    cr=car(4,-6,'#F4F1EA',180); DV=person((2.2,-4.6,0),180,DRV,'grin',name='driver')
    D=person((0,-3.0,0),0,DANI,'smile',name='dani'); S=person((1.0,-3.1,0),0,SHERY,'smile',name='sherry'); F=person((-1.0,-3.1,0),0,FAIZ,'smile',name='faizan'); Bl=person((-2.0,-3.0,0),0,BILAL,'flat',name='bilal')
    rk=rickshaw(-12,-9,90,'#2E8B57'); peds=crowd([(-8,-2.2,90),(8,-2.4,-90),(-14,-3,90)],63)
    def upd(t):
        for c in peds: blink(c,t); walker(c,(c['x'],c['y'],0),c['rz'],1.0,t,arm=18)
        rk.location[0]=-12+4*t
        for H,x in ((D,0),(S,1.0),(F,-1.0),(Bl,-2.0)): blink(H,t); stand_at(H,t,x,-3.0,.008,0) if view!='O_car' else None
        blink(DV,t)
        if view=='O_driver':
            dx=L(4,1.4,ease(min(1,t/1.2))); DV['root'].location=(dx,-4.6,.008); DV['root'].rotation_euler[2]=R(90 if t<1.2 else 160); walk(DV,dx,step=.55) if t<1.2 else stand(DV,t)
            talk(DV,t,286,289,KEY,rest='grin',rate=6); talk(D,t,290,298,KEY,rest='smile') if t>wl(290,KEY)-.05 else None
            look_at(D,DV['root'].location+Vector((0,0,1.9)),.7)
            q=ease(t/DUR); camset((L(3.8,3.2,q),-7.8,1.7),(.4,-3.6,1.8),24,5.0)
        elif view=='O_best':
            DV['root'].location=(1.4,-4.6,.008); DV['root'].rotation_euler[2]=R(160); stand(DV,t); k=ease(t/.4); arms(DV,-90-60*k,0,40*k,-90-60*k,0,-40*k)
            talk(DV,t,299,305,KEY,rest='grin',rate=6); face(DV,brow=.08)
            q=ease(t/DUR); camset((L(.6,.9,q),-3.45,1.55),(1.4,-4.6,2.05),24,3.5,focus=(1.4,-4.6,2.0))
        elif view=='O_conf':
            DV['root'].location=(1.4,-4.6,.008); DV['root'].rotation_euler[2]=R(160); stand(DV,t); face(DV,mouth='grin')
            talk(D,t,306,309,KEY,rest='grin'); talk(S,t,310,319,KEY,rest='smirk') if t>wl(310,KEY)-.05 else None
            D['arm'][1].rotation_euler=(R(-80),0,R(-60)) if t<wl(310,KEY) else (0,0,0); look_at(D,(1.4,-4.6,1.9),.6)
            q=ease(t/DUR); camset((-.6,-6.4,1.75),(.5,-3.0,1.9),26,4.5)
        else:
            x=L(4,-14,ease_in(min(1,t/DUR))); cr.location=(x,-6.0,0)
            for H,(dx,dy,zz) in ((DV,(.4,-.45,.25)),(D,(.4,.45,.25)),(S,(-.8,-.45,.25)),(F,(-.8,.45,.25))):
                H['root'].location=(x+dx*-1,-6.0+dy,zz); H['root'].rotation_euler=(0,0,R(-90)); H['z0']=zz; sit(H,1,.5,80); blink(H,t)
            hideH(Bl); talk(DV,t,320,324,KEY,rest='grin',rate=6); talk(D,t,325,326,KEY,rest='grin') if t>wl(325,KEY)-.05 else None; talk(DV,t,327,332,KEY,rest='grin',rate=6) if t>wl(327,KEY)-.05 else None
            DV['arm'][1].rotation_euler=(R(-75),0,R(-12)); DV['arm'][-1].rotation_euler=(R(-75),0,R(12))
            camset((x-3.6,-9.6,2.2),(x-.2,-6.0,1.2),26,5.0)
    return dict(upd=upd)
for v in ('O_driver','O_best','O_conf','O_car'): SHOTS[v]=(lambda v=v: SH_O(v))

# ============================================================ FOOD STREET (night)
def SH_Z(view):
    KEY=view; foodstreet(); B.done('food'); setup_render('dusk',res=PCT,samples=SAMPLES,shadow_dist=40)
    for x in (-12,-4,4,12): point((x,0,4.2),220,(1,.78,.5),1.2)
    area((0,-9,2.5),500,(6,3),(1,.85,.7),rot=(R(-90),0,0),shadow=False)
    D=person((-1.5,-1.2,0),0,DANI,'smile',name='dani'); S=person((-.5,-1.3,0),0,SHERY,'smile',name='sherry'); F=person((.6,-1.2,0),0,FAIZ,'O',name='faizan'); Bl=person((1.6,-1.25,0),0,BILAL,'flat',name='bilal')
    diners=crowd([(-10,-2.0,0),(-8,2.0,180),(6,-2.0,0),(9,2.0,180),(13,-2.0,0),(-13,2,180)],70)
    walkers=crowd([(-16,-4.4,90),(15,-4.0,-90),(-6,4.5,90)],71)
    ph=phone(F,1,'#7FD3FF'); ph.scale=(0,0,0)
    plate=empty((0,0,0)); ocyl((0,0,0),.16,.02,M('#F4F1EA',.4),plate,rot=(0,0,0),seg=16); ocyl((0,0,.02),.12,.03,M('#C0392B',.6),plate,rot=(0,0,0),seg=14); plate.scale=(0,0,0)
    def bg(t):
        for i,c in enumerate(diners): blink(c,t); c['z0']=0; sit(c,1,.42,90); c['arm'][1].rotation_euler=(R(-70-15*math.sin(t*3+i)),0,0); face(c,mouth='grin' if (t+i)%2<1 else 'smile')
        for c in walkers: blink(c,t); walker(c,(c['x'],c['y'],0),c['rz'],.9,t,arm=18)
    def upd(t):
        bg(t)
        for H,x in ((D,-1.5),(S,-.5),(F,.6),(Bl,1.6)): blink(H,t); stand_at(H,t,x,-1.25,.008,0)
        if view=='Z_food':
            k=ease(t/1.0); F['root'].location=(L(.6,.9,k),L(-1.2,-.4,k),.008); F['root'].rotation_euler[2]=R(L(0,200,ease((t-.6)/.8))); talk(F,t,333,338,KEY,rest='O',rate=5)
            face(F,eyes=1.25,brow=.1); F['arm'][1].rotation_euler=(R(-40),0,R(-30)); F['arm'][-1].rotation_euler=(R(-40),0,R(30))
            q=ease(t/DUR); camset((L(1.0,.8,q),-4.6,1.6),(.6,0,1.9),24,5.0)
        elif view=='Z_bilal':
            talk(Bl,t,339,342,KEY,rest='O'); Bl['arm'][1].rotation_euler=(R(-90),0,R(40)); look_at(Bl,(.6,-1.2,1.9),.8); face(Bl,brow=.1)
            q=ease(t/DUR); camset((2.2,-3.8,1.75),(1.6,-1.25,2.0),30,3.5,focus=(1.6,-1.25,2.0))
        elif view=='Z_dil':
            talk(F,t,343,353,KEY,rest='smile',rate=6); F['arm'][1].rotation_euler=(R(-60),R(-20),R(-50)); F['head'].rotation_euler=(R(-10),0,R(10*math.sin(t*1.2))); face(F,eyes=.75,brow=.05)
            q=ease(t/DUR); camset((L(.9,.6,q),-3.4,1.8),(.6,-1.2,1.95),L(28,34,q),3.0,focus=(.6,-1.2,1.95))
        elif view=='Z_rishta':
            talk(D,t,354,361,KEY,rest='smirk'); D['arm'][1].rotation_euler=(R(-80),0,R(-50)); look_at(D,(.6,-1.2,1.9),.7); face(D,brow=.03,brow_r=-12)
            q=ease(t/DUR); camset((-2.2,-3.6,1.75),(-1.5,-1.2,2.0),28,3.5,focus=(-1.5,-1.2,2.0))
        elif view=='Z_call':
            ph.scale=(1,1,1); arm_reach(F,1,F['head'].matrix_world@Vector((.75*F['u'],-.1*F['u'],0)),1.0); talk(F,t,366,367,KEY,rest='smile') if t>wl(366,KEY)-.05 else face(F,mouth='o')
            F['head'].rotation_euler[2]=R(-10); face(F,brow=.03)
            q=ease(t/DUR); camset((.0,-3.4,1.8),(.6,-1.2,1.95),30,3.5,focus=(.6,-1.2,1.95))
        elif view=='Z_settle':
            ph.scale=(1,1,1); arm_reach(F,1,F['head'].matrix_world@Vector((.75*F['u'],-.1*F['u'],0)),1.0); talk(F,t,371,380,KEY,rest='grin',rate=6); face(F,eyes=.8)
            if t>wl(380,KEY):
                for i,H in enumerate((D,S,Bl)): face(H,mouth='grin'); H['root'].rotation_euler[1]=R(6*math.sin(t*14+i)); H['root'].rotation_euler[0]=R(-8)
            q=ease(t/DUR); camset((L(.6,0,q),L(-3.6,-5.0,q),L(1.8,2.2,q)),(.1,-1.2,1.7),24,4.0)
        else:
            for H,x in ((D,-1.0),(S,-.3),(Bl,.4)):
                H['root'].location=(x,-2.4,.008); arms(H,-20,0,60,-20,0,-60); face(H,mouth='grin',brow=.05)
            D['arm'][1].rotation_euler=(R(-165),0,R(20)); S['arm'][-1].rotation_euler=(R(-100),0,R(-40))
            F['root'].location=(1.1,1.4,.008); F['z0']=0; sit(F,1,.42,90); F['root'].rotation_euler[2]=R(200); plate.scale=(1,1,1); plate.location=(.95,.8,.8)
            F['arm'][1].rotation_euler=(R(-90-30*abs(math.sin(t*5))),0,0); face(F,mouth='O' if (t*5)%1<.5 else 'grin')
            q=ease(t/DUR); camset((L(-.3,-.2,q),L(-4.0,-4.8,q),L(1.6,2.3,q)),(-.2,-.6,L(1.9,2.0,q)),L(22,16,q),6.0)
    return dict(upd=upd)
for v in ('Z_food','Z_bilal','Z_dil','Z_rishta','Z_call','Z_settle','Z_final'): SHOTS[v]=(lambda v=v: SH_Z(v))
