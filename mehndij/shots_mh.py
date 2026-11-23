SHOTS={}
WJ=json.load(open('/home/claude/mehndij/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('I_venue',0),('I_aunty',18),('I_uncle',25),('I_mehndi',34),('I_mistake',39),
    ('P_yaaro',57),('P_bhai',71),('P_bilkul',77),('P_tut',84),('P_haters',91),('P_move',96),('P_chair',109),
    ('S_dj',116),('S_ladies',121),('S_walk',130),('S_forget',137),('S_change',146),('S_which',149),('S_save',151),('S_rush',157),('S_fight',166),('S_street',178),
    ('A_watch',186),('A_ye',195),('A_pata',203),('A_kaisi',208),('A_beta',212),
    ('U_jump',219),('U_side',227),('U_dance',234),('U_who',247),('U_knees',252),('D_dadi',260),
    ('W_dj',271),('W_dadi',278),('W_crowd',279),('W_seven',283),('W_seventy',289),
    ('N_narr',297),('N_morning',310),('N_ammi',313),('N_tabiyat',322),('N_dadi',327),('N_bahar',337)]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.12,3)) for k,i in _K]
END=round(WE[-1]+1.2,3)
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
def L(a,b,q): return a+(b-a)*q
def cl(x): return max(0.0,min(1.0,x))
def headpos(H):
    bpy.context.view_layer.update(); return H['head'].matrix_world.translation.copy()
def cf(H,d=2.2,lat=.35,dz=0.0,lens=30,fs=3.5,tgt_dz=-.05):
    hp_=headpos(H); a=H['root'].rotation_euler[2]; fwd=Vector((math.sin(a),-math.cos(a),0)); rt=Vector((math.cos(a),math.sin(a),0))
    pos=hp_+fwd*d+rt*lat+Vector((0,0,dz)); tg=hp_+Vector((0,0,tgt_dz)); camset(tuple(pos),tuple(tg),lens,fs,focus=tuple(hp_))
def ots(A,Bh,back=1.1,side=.45,up=.1,lens=32,fs=3.0):
    """over A's shoulder looking at Bh's face"""
    side=math.copysign(max(abs(side),.8),side); back=max(back,1.3); lens=max(lens,36)
    a_=headpos(A); b_=headpos(Bh); d=(b_-a_); d.z=0; d.normalize(); rt=Vector((d.y,-d.x,0))
    pos=a_-d*back+rt*side+Vector((0,0,up)); camset(tuple(pos),tuple(b_+Vector((0,0,-.1))),lens,fs,focus=tuple(b_))
def put_at(H,t,x,y,rz,z=.0):
    H['root'].location=(x,y,z+.008); H['z0']=z; stand(H,t); H['root'].location[2]=z+.008; H['root'].rotation_euler[2]=R(rz); blink(H,t)
def seat(H,t,x,y,rz,sh=.47,z=0.0):
    blink(H,t); H['root'].location=(x,y,z+.008); H['root'].rotation_euler=(0,0,R(rz)); H['z0']=z; sit(H,1,sh+z,90)
def breathe(H,t): H['root'].scale=(1,1,1+.006*math.sin(t*2.2+H['seed']))
def phone_ear(H,s=1): H['arm'][s].rotation_euler=(R(-150),0,R(-28*s))
def phone_front(H,s=1,k=1.0): H['arm'][s].rotation_euler=(R(-85*k),0,R(-18*s*k))
def gesture(H,t,s=1,amp=1.0): H['arm'][s].rotation_euler=(R(-45*amp+10*math.sin(t*4)),0,R(-25*s*amp))


# ---------------------------------------------------------------- registry for collision QC
PEOPLE=[]
_person0=person
def person(loc,rz,C,mouth='smile',name=None):
    H=_person0(loc,rz,C,mouth,name); H['nm']=name or 'p%d'%len(PEOPLE); PEOPLE.append(H); return H

# ---------------------------------------------------------------- arm poses (arm[1] is at +x; outward = -Y roll for arm[1], +Y for arm[-1])
def ARMV(H,a=150,sw=0.0): H['arm'][1].rotation_euler=(0,R(-a-sw),0); H['arm'][-1].rotation_euler=(0,R(a-sw),0)
def GEST(H,s,up=50,out=15): H['arm'][s].rotation_euler=(R(-up),0,R(out*s))
def side(H,s,a=85): H['arm'][s].rotation_euler=(0,R(-a*s),0)
# ---------------------------------------------------------------- dance moves
def dance(H,t,style,amp=1.0,ph=0.0):
    s=t*2*math.pi*(1.9 if style!='dadi' else 1.3)+ph; b=abs(math.sin(s))
    z0=H.get('z0',0.0)
    for q in (1,-1): H['leg'][q].rotation_euler=(0,0,0)
    if style=='bhangra':
        H['arm'][1].rotation_euler=(0,R(-150-15*math.sin(s)),0); H['arm'][-1].rotation_euler=(0,R(150-15*math.sin(s)),0)
        k=1 if math.sin(s*.5)>0 else -1; H['leg'][k].rotation_euler=(R(-35*amp*b),0,0)
        H['root'].location[2]=z0+.008+.07*amp*b; H['root'].rotation_euler[1]=R(5*math.sin(s))
    elif style=='fight':
        p=math.sin(s*1.5); H['arm'][1].rotation_euler=(R(-90 if p>0 else -40),0,R(6)); H['arm'][-1].rotation_euler=(R(-40 if p>0 else -90),0,R(-6))
        H['leg'][1].rotation_euler=(R(-25*amp*max(0,math.sin(s*.75))),0,0); H['root'].rotation_euler[1]=R(6*p); H['root'].location[2]=z0+.008+.03*b
    elif style=='dadi':
        H['arm'][1].rotation_euler=(R(-12),R(-118+18*math.sin(s)),0); H['arm'][-1].rotation_euler=(R(-12),R(118+18*math.sin(s)),0)
        H['root'].rotation_euler[1]=R(8*math.sin(s)); H['root'].location[2]=z0+.008+.03*b
    elif style=='clap':
        k=.5+.5*math.sin(s*2); H['arm'][1].rotation_euler=(R(-80),0,R(-6-15*k)); H['arm'][-1].rotation_euler=(R(-80),0,R(6+15*k))
    elif style=='stiff':
        j=1 if (t%1.3)<.12 else 0; H['arm'][1].rotation_euler=(R(-30-60*j),0,R(8)); H['arm'][-1].rotation_euler=(R(-10),0,R(-8))
    elif style=='cheer':
        ARMV(H,152,10*math.sin(s)); H['root'].location[2]=z0+.008+.08*b
def flat_legs(H):
    for q in (1,-1): H['leg'][q].rotation_euler=(0,0,0)

# ---------------------------------------------------------------- sets
STG=.6
def set_venue():
    mehndi_venue(); setup_render('nightc',res=PCT,samples=SAMPLES,shadow_dist=40)
    bpy.context.scene.view_settings.exposure=0.15
    for x in (-3,0,3): point((x,1.0,4.6),260,(1,.82,.55),.6)
    point((0,4.0,4.4),420,(1,.86,.62),.8); area((0,-4,4.0),900,(10,6),(1,.85,.65),rot=(R(25),0,0),shadow=False)
    for x in (-8,8): point((x,-3,3.5),180,(1,.8,.5),.6)
    point((8.6,1.6,2.6),160,(1,.85,.7),.5); point((-4.2,.6,2.4),120,(1,.85,.7),.5)
STAGE_X=dict(wal=0.0,bil=-2.4,sher=2.4,uncle=-.2,dadi=1.3)
def venue_crowd(seed=900,n=26,stand=True):
    r=random.Random(seed); out=[]
    rows=[(-3.3,(-7,-5,-3,3,5,7)),(-5.5,(-7,-5,-3,3,5,7)),(-7.7,(-7,-3,5))]
    i=0
    for y,xs in rows:
        for x in xs:
            H=person((x,y,0),180,local(seed+i*5,female=(i%2==0)),'smile',name='g%d'%i); H['_seat']=(x,y); out.append(H); i+=1
    if stand:
        for (x,y,rz) in ((-9.6,-1.0,-120),(-9.8,1.2,-100),(9.8,-1.2,120),(-10.2,-5.0,-150),(10.2,-5.2,150),(-12.0,-2.8,-90),(12.2,-0.4,100)):
            H=person((x,y,0),rz,local(seed+i*5,female=(i%3==0)),'smile',name='g%d'%i); H['_stand']=(x,y,rz); out.append(H); i+=1
    def upd(t,mode='watch'):
        for k,H in enumerate(out):
            if '_seat' in H:
                x,y=H['_seat']; seat(H,t,x,y,180,sh=.47)
                if mode=='cheer' and k%2==0: dance(H,t,'clap',ph=k)
                elif mode=='wild': ARMV(H,150,12*math.sin(t*9+k))
                face(H,mouth='grin' if mode!='watch' else ('smile' if k%3 else 'o'))
            else:
                x,y,rz=H['_stand']; put_at(H,t,x,y,rz)
                if mode in ('cheer','wild'): dance(H,t,'cheer' if mode=='wild' else 'clap',ph=k)
                else: gaze_idle(H,t)
                face(H,mouth='grin' if mode!='watch' else 'smile')
    return out,upd

# ============================================================ INTRO
def SH_I(view):
    KEY=view; set_venue()
    cs,crowd_upd=venue_crowd()
    A1=person((0,0,0),180,AUN1,'flat',name='aun1'); A2=person((0,0,0),180,AUN2,'smirk',name='aun2'); CH=person((0,0,0),180,CHA,'grin',name='chacha')
    G=[person((0,0,0),180,local(950+i*3),'smile',name='fr%d'%i) for i in range(2)]
    def front(t):
        seat(A1,t,-3.2,-.95,180,sh=.44); seat(A2,t,-5.2,-.95,180,sh=.44)
        for H,x in zip(G,(3.2,5.2)): seat(H,t,x,-.95,180,sh=.44)
    def upd(t):
        front(t)
        if view=='I_venue':
            crowd_upd(t,'cheer'); hideH(CH); q=ease(t/DUR)
            camset((0,L(-16,-11,q),L(9,4.2,q)),(0,L(2,3,q),L(0,1.4,q)),24,8.0)
        elif view=='I_aunty':
            crowd_upd(t); hideH(CH); GEST(A1,1,50,15); face(A1,mouth='flat',brow=-.04,brow_r=-16,eyes=.9); face(A2,mouth='smirk',brow=-.02,brow_r=14)
            look_at(A1,(0,4,1.6),.4); look_at(A2,headpos(A1),.6); q=ease(t/DUR)
            camset((L(-2.2,-2.8,q),L(1.6,1.2,q),1.4),(-4.2,-.95,1.3),26,4.0)
        elif view=='I_uncle':
            crowd_upd(t,'cheer'); put_at(CH,t,8.0,-1.2,150); dance(CH,t,'cheer'); CH['arm'][-1].rotation_euler=(0,R(12),0); face(CH,mouth='grin',brow=.06)
            CH['head'].rotation_euler[2]=R(15*math.sin(t*2)); cf(CH,d=2.2,lat=-.3,lens=28)
        elif view=='I_mehndi':
            crowd_upd(t,'cheer'); hideH(CH); q=ease(t/DUR); camset((L(-3,3,q),-1.9,2.6),(0,4,1.7),22,8.0)
    return dict(upd=upd)
for v in ('I_venue','I_aunty','I_uncle','I_mehndi'): SHOTS[v]=(lambda v=v: SH_I(v))

# ============================================================ BACKSTAGE (prep)
def SH_P(view):
    KEY=view; chairs=backstage(); setup_interior('night',room=(0,0,3.0),res=PCT,samples=SAMPLES); bpy.context.scene.view_settings.exposure=-0.2
    point((0,0,2.6),90,(1,.88,.7),.5); point((-1,2.0,2.2),30,(.9,.95,1),.4); point((0,-2.4,2.2),160,(1,.9,.78),.6); point((-2.5,-1.5,2.0),70,(1,.9,.8),.5); point((2.5,-1.5,2.0),70,(1,.9,.8),.5); area((5,-1,2.2),300,(2,2),(1,.8,.5),rot=(0,R(-90),0),shadow=False)
    W=person((0,0,0),0,WAL,'grin',name='waleed'); BL=person((0,0,0),0,BIL2,'smirk',name='bilal'); SH=person((0,0,0),0,SHR,'smirk',name='sherry')
    def upd(t):
        put_at(W,t,0,.45,0); put_at(BL,t,-2.0,-.7,40); put_at(SH,t,2.0,-.9,-40)
        look_at(BL,headpos(W),.7); look_at(SH,headpos(W),.7)
        if view=='I_mistake':
            hideH(BL); hideH(SH); put_at(W,t,-1.6,.6,10); face(W,mouth='flat' if t<wl(50,KEY) else 'O',brow=.08,brow_r=-12,eyes=1.0 if t<wl(50,KEY) else 1.3)
            GEST(W,1,35,10); q=ease(t/DUR); cf(W,d=L(2.3,1.6,q),lat=.3,lens=30)
            return
        if view=='P_yaaro': talk(W,t,57,70,KEY,rest='grin',rate=7); side(W,1,78); side(W,-1,62); face(W,brow=.08); q=ease(t/DUR); camset((L(.4,.2,q),L(-2.6,-2.3,q),1.7),(0,-.2,1.4),22,5.0)
        elif view=='P_bhai': talk(BL,t,71,76,KEY,rest='smirk'); face(BL,brow=-.03,brow_r=14); BL['arm'][1].rotation_euler=(R(-15),R(-35),R(70)); cf(BL,d=1.6,lat=.35,lens=30)
        elif view=='P_bilkul': talk(W,t,77,83,KEY,rest='grin'); face(W,brow=.08,eyes=.9); W['arm'][1].rotation_euler=(R(-15),R(-35),R(70)); W['arm'][-1].rotation_euler=(R(-15),R(35),R(-70)); cf(W,d=1.8,lat=-.3,lens=30)
        elif view=='P_tut': talk(SH,t,84,90,KEY,rest='smirk'); face(SH,brow=-.02,brow_r=-14); GEST(SH,1,48,20); cf(SH,d=1.8,lat=-.35,lens=30)
        elif view=='P_haters': talk(W,t,91,95,KEY,rest='smirk'); face(W,brow=-.03,brow_r=12); GEST(W,1,52,25); cf(W,d=1.8,lat=.3,lens=30)
        elif view=='P_move':
            k=cl((t-1.0)/.35)-cl((t-1.55)/.35); W['leg'][1].rotation_euler=(R(-75*k),0,0); W['arm'][1].rotation_euler=(R(-20),R(-100),0); W['arm'][-1].rotation_euler=(R(-20),R(82),0)
            W['root'].rotation_euler[1]=R(-6*k); face(W,mouth='O' if k>.5 else 'grin',brow=.1 if k>.5 else .05,eyes=1.2 if k>.5 else 1)
            hit=cl((t-1.3)/.15)*math.exp(-max(0,t-1.3)*4); chairs[1].rotation_euler=(R(10*hit*math.sin(t*30)),0,R(30)); face(BL,mouth='O'); face(SH,mouth='O')
            camset((-.6,-2.7,1.6),(.6,-.1,.9),24,4.0)
        else: talk(BL,t,109,115,KEY,rest='grin',rate=7); face(BL,eyes=.8,brow=.05); BL['arm'][-1].rotation_euler=(R(-15),R(35),R(-70)); GEST(BL,1,52,20); cf(BL,d=1.8,lat=.4,lens=30)
    return dict(upd=upd)
for v in ('I_mistake','P_yaaro','P_bhai','P_bilkul','P_tut','P_haters','P_move','P_chair'): SHOTS[v]=(lambda v=v: SH_P(v))

# ============================================================ STAGE (everything at the venue after the prep)
def SH_S(view):
    KEY=view; set_venue(); cs,crowd_upd=venue_crowd()
    W=person((0,0,0),0,WAL,'grin',name='waleed'); BL=person((0,0,0),0,BIL2,'grin',name='bilal'); SH=person((0,0,0),0,SHR,'grin',name='sherry')
    DJm=person((0,0,0),0,DJ,'grin',name='dj'); CH=person((0,0,0),0,CHA,'grin',name='chacha'); DA=person((0,0,0),0,DADI,'smile',name='dadi')
    A1=person((0,0,0),180,AUN1,'flat',name='aun1'); A2=person((0,0,0),180,AUN2,'smirk',name='aun2')
    G=[person((0,0,0),180,local(950+i*3),'smile',name='fr%d'%i) for i in range(2)]
    mic=empty((0,0,0)); ocyl((0,0,0),.03,.22,M('#1E1E22',.3,metal=.5),mic,rot=(R(-20),0,0)); ocyl((0,-.04,.12),.05,.07,M('#8A8F99',.3,metal=.8),mic,rot=(0,0,0))
    def front(t):
        seat(A1,t,-3.2,-.95,180,sh=.44); seat(A2,t,-5.2,-.95,180,sh=.44)
        for H,x in zip(G,(3.2,5.2)): seat(H,t,x,-.95,180,sh=.44)
    def dj(t,grab=False):
        put_at(DJm,t,8.6,3.45,-10); DJm['arm'][-1].rotation_euler=(R(-70),0,R(10+8*math.sin(t*6)))
        DJm['arm'][1].rotation_euler=(R(-70),0,R(-10+8*math.sin(t*5+1))); bpy.context.view_layer.update(); hp_=headpos(DJm); mic.location=(hp_.x-.05,hp_.y-.55,hp_.z-.32) if grab else (8.95,2.75,1.15)
    def onstage(H,t,x,y=3.4,rz=0): put_at(H,t,x,y,rz,STG)
    g=view[0]
    def upd(t):
        front(t)
        if view in ('S_dj','S_ladies'):
            crowd_upd(t); dj(t,grab=(view=='S_ladies' or t>.5)); hideH(W); hideH(BL); hideH(SH); hideH(CH); hideH(DA)
            if view=='S_dj': face(DJm,mouth='grin',brow=.08); q=ease(t/DUR); camset((L(6.0,6.6,q),L(-.2,.4,q),2.0),(8.6,3.4,1.8),26,4.0)
            else:
                talk(DJm,t,121,129,KEY,rest='grin',rate=7,shapes=('shout','O','grin')); face(DJm,brow=.1); (side(DJm,-1,95) if t>wl(129,KEY) else None)
                cf(DJm,d=2.3,lat=.5,dz=.25,lens=30)
            return
        dj(t,grab=view in ('S_which','W_dj','W_dadi'))
        # who is on stage
        hideH(CH) if g in 'S' or view in ('A_watch','A_ye','A_pata','A_kaisi','A_beta') else None
        hideH(DA) if g in 'SAU' else None
        if view=='S_walk':
            crowd_upd(t,'cheer'); hideH(BL); hideH(SH)
            k=cl(t/1.5); k=k*k*(3-2*k); x=L(4.2,0,k); W['root'].location=(x,3.4,STG+.008); W['z0']=STG; W['root'].rotation_euler[2]=R(L(-90,0,ease(cl((t-1.35)/.35))))
            walk(W,x,step=.5,arm=22) if k<.98 else stand(W,t); W['root'].location[2]=STG+.008; blink(W,t)
            if t>1.75: ARMV(W,150*ease(cl((t-1.75)/.25)))
            face(W,mouth='grin',brow=.06); camset((L(1.6,.2,k),.6,1.9),(x,3.4,1.85),24,6.0)
            return
        if view=='S_forget':
            crowd_upd(t); hideH(BL); hideH(SH); onstage(W,t,0); dance(W,t,'stiff'); face(W,mouth='flat',eyes=1.3,brow=.13); W['head'].rotation_euler[2]=R(8*math.sin(t*1.7))
            q=ease(t/DUR); cf(W,d=L(3.6,2.2,q),lat=0,dz=-.2,lens=30)
            return
        if view in ('S_change','S_save'):
            crowd_upd(t); hideH(BL); hideH(SH); onstage(W,t,0,rz=45); a,b=(129,131) if view=='S_change' else (134,139)
            talk(W,t,a,b,KEY,rest='O',shapes=('shout','O')); face(W,brow=.14,eyes=1.3); (ARMV(W,142,6*math.sin(t*14)) if view=='S_save' else (GEST(W,1,75,30),GEST(W,-1,75,30)))
            cf(W,d=2.2,lat=.3,lens=30)
            return
        if view=='S_which':
            crowd_upd(t); hideH(BL); hideH(SH); onstage(W,t,0,rz=45); talk(DJm,t,149,150,KEY,rest='o'); face(DJm,brow=.1,brow_r=-12); look_at(DJm,headpos(W),.6); cf(DJm,d=2.3,lat=.5,dz=.25,lens=30)
            return
        if view=='S_rush':
            crowd_upd(t); onstage(W,t,0,rz=0); face(W,mouth='O',brow=.12); k=ease(cl(t/1.6))
            BL['root'].location=(L(-6.2,STAGE_X['bil'],k),3.5,STG+.008); BL['z0']=STG; BL['root'].rotation_euler[2]=R(90 if k<.95 else 0); run(BL,BL['root'].location.x) if k<.95 else stand(BL,t); BL['root'].location[2]=STG+.008; blink(BL,t)
            SH['root'].location=(L(6.2,STAGE_X['sher'],k),3.5,STG+.008); SH['z0']=STG; SH['root'].rotation_euler[2]=R(-90 if k<.95 else 0); run(SH,SH['root'].location.x) if k<.95 else stand(SH,t); SH['root'].location[2]=STG+.008; blink(SH,t)
            camset((0,-2.6,2.5),(0,3.5,1.5),20,6.0)
            return
        # from here on Waleed, Bilal, Sherry on stage
        onstage(W,t,0 if g not in 'UDWN' else (-2.4 if g=='U' else -4.8)); onstage(BL,t,STAGE_X['bil'] if g not in 'UDWN' else (-4.6 if g=='U' else -2.6),3.6); onstage(SH,t,STAGE_X['sher'] if g not in 'UDWN' else (2.6 if g=='U' else 4.1),3.6)
        if view=='S_fight':
            crowd_upd(t); dance(BL,t,'fight'); face(BL,mouth='frown',brow=-.06,brow_r=22); BL['root'].rotation_euler[2]=R(25*math.sin(t*2.2)); face(W,mouth='O',brow=.1); look_at(W,headpos(BL),.6); look_at(SH,headpos(BL),.6); face(SH,mouth='O',brow=.12)
            q=ease(t/DUR); camset((L(-1.2,-1.8,q),.4,2.0),(-1.6,3.5,1.8),24,5.0)
        elif view=='S_street':
            crowd_upd(t); dance(BL,t,'fight'); look_at(SH,headpos(BL),.7); SH['root'].rotation_euler[2]=R(-30); talk(SH,t,178,185,KEY,rest='O',shapes=('shout','O')); face(SH,brow=-.05,brow_r=22)
            side(SH,1,80); side(SH,-1,80); cf(SH,d=2.3,lat=.3,lens=30)
        elif g=='A':
            crowd_upd(t); dance(BL,t,'fight' if view!='A_kaisi' else 'clap'); dance(SH,t,'clap')
            if view=='A_watch':
                look_at(A1,headpos(W),.4); look_at(A2,headpos(W),.4); face(A1,mouth='flat',brow=-.04,brow_r=-15,eyes=.9); face(A2,mouth='smirk'); dance(W,t,'stiff')
                camset((-2.0,1.3,1.6),(-4.2,-.95,1.35),26,4.0)
            elif view=='A_ye': dance(W,t,'stiff'); talk(A1,t,195,202,KEY,rest='flat'); look_at(A1,headpos(A2),.6); look_at(A2,headpos(A1),.6); GEST(A1,1,42,15); face(A1,brow=-.03,brow_r=-15); cf(A1,d=1.9,lat=.4,lens=30)
            elif view=='A_pata': dance(W,t,'stiff'); talk(A2,t,203,207,KEY,rest='grin'); look_at(A2,headpos(A1),.6); look_at(A1,headpos(A2),.5); GEST(A2,-1,42,15); face(A2,brow=.06); cf(A2,d=1.9,lat=-.4,lens=30)
            elif view=='A_kaisi':
                W['root'].rotation_euler[0]=R(12); W['root'].rotation_euler[2]=R(-25); talk(W,t,208,211,KEY,rest='grin'); face(W,brow=.08); GEST(W,1,40,20); look_at(W,headpos(A1),.6)
                cf(W,d=2.2,lat=.5,lens=30)
            else: talk(A1,t,212,218,KEY,rest='flat',rate=6); face(A1,brow=.02,eyes=.85); look_at(A1,headpos(W),.5); face(A2,mouth='grin'); cf(A1,d=1.9,lat=.4,lens=30)
        elif g=='U':
            crowd_upd(t,'cheer' if view in ('U_dance','U_who','U_knees') else 'watch')
            if view=='U_jump':
                k=cl(t/1.3); P0=Vector((-2.4,-.1)); P1=Vector((-.2,3.3)); TK_=.62
                if k<TK_: p=P0.lerp(Vector((-1.75,.9)),k/TK_); z=0.0
                else:
                    a_=(k-TK_)/(1-TK_); p=Vector((-1.75,.9)).lerp(P1,a_); z=STG*min(1,a_*1.6)+.55*math.sin(math.pi*a_)
                hd=math.degrees(math.atan2(P1.x-P0.x,-(P1.y-P0.y)))
                CH['root'].location=(p.x,p.y,z+.008); CH['z0']=z; CH['root'].rotation_euler=(0,0,R(hd if k<1 else L(hd,0,ease(cl((t-1.3)/.3))) if t<1.6 else 0))
                if k<TK_: walk(CH,k*5,step=.8,lift=.16,arm=42,lean=5)
                elif k<1: flat_legs(CH); CH['leg'][1].rotation_euler=(R(-55),0,0); CH['leg'][-1].rotation_euler=(R(25),0,0); ARMV(CH,140)
                else: stand(CH,t); dance(CH,t,'cheer')
                CH['root'].location[0]=p.x; CH['root'].location[1]=p.y
                if k<1: CH['root'].location[2]=z+.008
                blink(CH,t); face(CH,mouth='grin',brow=.1); [look_at(H,headpos(CH),.6) for H in (W,BL,SH)]; [face(H,mouth='O') for H in (W,BL,SH)]
                camset((2.3,.3,1.8),(-1.1,2.3,1.4),22,6.0)
            elif view=='U_side':
                onstage(CH,t,-.2,3.3); talk(CH,t,227,233,KEY,rest='grin',shapes=('shout','O','grin')); side(CH,1,85); side(CH,-1,160); face(CH,brow=.08); CH['_cflat']=-.6
                k=ease(cl(t/.8)); [look_at(H,headpos(CH),.6) for H in (W,BL,SH)]; cf(CH,d=2.3,lat=-.6,lens=28)
            elif view=='U_dance':
                onstage(CH,t,-.2,3.3); CH['z0']=STG; dance(CH,t,'bhangra',1.2); face(CH,mouth='grin',eyes=.8,brow=.06); [look_at(H,headpos(CH),.5) for H in (W,BL,SH)]; face(W,mouth='O'); face(BL,mouth='grin'); face(SH,mouth='grin')
                q=ease(t/DUR); camset((L(1.6,-1.6,q),.0,1.7),(-.2,3.3,2.1),22,5.0)
            else:
                onstage(CH,t,-.2,3.3); CH['z0']=STG; dance(CH,t,'bhangra',1.2); face(CH,mouth='grin')
                W['root'].rotation_euler[2]=R(-45); BL['root'].rotation_euler[2]=R(45)
                if view=='U_who': talk(W,t,247,251,KEY,rest='flat'); face(W,brow=.06,brow_r=-14); look_at(W,headpos(BL),.5); cf(W,d=2.2,lat=.6,lens=30)
                else: talk(BL,t,252,259,KEY,rest='smirk'); face(BL,brow=-.02,brow_r=12); look_at(BL,headpos(W),.5); cf(BL,d=2.2,lat=-.6,lens=30)
        elif g in 'DWN':
            onstage(CH,t,-.4,3.3); onstage(DA,t,1.8,3.4); CH['z0']=STG; DA['z0']=STG
            if view=='D_dadi':
                crowd_upd(t,'wild'); k=ease(cl(t/1.0)); DA['root'].location=(L(6.2,1.8,k),3.4,STG+.008); walk(DA,DA['root'].location.x,step=.35,arm=8) if k<1 else dance(DA,t,'dadi')
                DA['root'].rotation_euler[2]=R(-90 if k<1 else 0); dance(CH,t,'bhangra',1.2); dance(BL,t,'fight',ph=1); dance(SH,t,'bhangra',.8,ph=2); dance(W,t,'stiff')
                face(DA,mouth='grin',eyes=.85,brow=.06); face(W,mouth='O',brow=.12); q=ease(t/DUR); camset((L(-.5,.5,q),L(-.6,.2,q),L(2.8,2.4,q)),(-.4,3.4,1.6),18,7.0)
            elif view=='W_dj':
                crowd_upd(t); [dance(H,t,'stiff') for H in (W,)]; talk(DJm,t,271,277,KEY,rest='grin',rate=6); side(DJm,-1,95); face(DJm,brow=.1)
                cf(DJm,d=2.2,lat=-.6,dz=.15,lens=30)
            elif view=='W_dadi':
                crowd_upd(t,'wild'); dance(DA,t,'dadi'); face(DA,mouth='grin',eyes=.8,brow=.08); face(W,mouth='O',brow=.14,eyes=1.3)
                [look_at(H,headpos(DA),.6) for H in (W,BL,SH,CH)]; q=ease(t/DUR); cf(DA,d=L(3.0,2.4,q),lat=.6,dz=.35,lens=30)
            elif view=='W_crowd':
                crowd_upd(t,'wild'); dance(DA,t,'dadi'); dance(CH,t,'cheer'); face(W,mouth='flat',eyes=.8,brow=-.02); q=ease(t/DUR); camset((L(.6,1.2,q),1.6,3.8),(4.6,-4.6,.9),24,8.0)
            elif view=='W_seven':
                crowd_upd(t); dance(DA,t,'dadi'); W['root'].rotation_euler[2]=R(25); talk(W,t,283,288,KEY,rest='frown',rate=5); face(W,brow=.06,brow_r=-18,eyes=.8); W['head'].rotation_euler[0]=R(14)
                handsdown(W); cf(W,d=2.0,lat=-.7,lens=30)
            elif view=='W_seventy':
                crowd_upd(t); dance(DA,t,'dadi'); SH['root'].rotation_euler[2]=R(-30); talk(SH,t,289,296,KEY,rest='smirk',rate=6); face(SH,brow=-.02,brow_r=12); look_at(SH,headpos(W),.6); cf(SH,d=2.0,lat=.7,lens=30)
            else:
                crowd_upd(t,'cheer'); dance(DA,t,'dadi'); dance(CH,t,'bhangra'); dance(BL,t,'fight'); hideH(SH)
                W['root'].rotation_euler[2]=R(20); face(W,mouth='frown',eyes=.75,brow=.05); W['head'].rotation_euler[0]=R(18); handsdown(W)
                q=ease(t/DUR); cf(W,d=L(2.8,2.2,q),lat=-.7,dz=.1,lens=30)
    return dict(upd=upd)
for v in ('S_dj','S_ladies','S_walk','S_forget','S_change','S_which','S_save','S_rush','S_fight','S_street','A_watch','A_ye','A_pata','A_kaisi','A_beta',
          'U_jump','U_side','U_dance','U_who','U_knees','D_dadi','W_dj','W_dadi','W_crowd','W_seven','W_seventy','N_narr'): SHOTS[v]=(lambda v=v: SH_S(v))

# ============================================================ NEXT MORNING (courtyard)
def SH_N(view):
    KEY=view; courtyard(); setup_render('morning_s',res=PCT,samples=SAMPLES,shadow_dist=30)
    W=person((0,0,0),0,WAL,'flat',name='waleed'); AM=person((0,0,0),0,AMMI2,'grin',name='ammi'); DA=person((0,0,0),0,DADI,'grin',name='dadi')
    shawl=obox((0,0,0),(.75,.42,.08),M('#5A6B8A',.9,kind='fabric'),.05); cup=empty((0,0,0)); ocyl((0,0,0),.04,.08,M('#F4F1EA',.3),cup,rot=(0,0,0),seg=10)
    def lying(t,sit_up=0.0):
        W['root'].location=(-.95,.8,.80); W['root'].rotation_euler=(R(-90),0,R(-90)); W['z0']=0; handsdown(W); flat_legs(W)
        shawl.scale=(0,0,0); W['root'].scale=(1,1,1+.01*math.sin(t*1.5))
    def sitting(t):
        W['root'].scale=(1,1,1); seat(W,t,0,.55,0,sh=.47); handsdown(W)
    def upd(t):
        if view=='N_morning':
            lying(t); hideH(AM); hideH(DA); face(W,mouth='flat')
            try: blink(W,t,force=1.0)
            except TypeError: pass
            q=ease(t/DUR); camset((L(-3.5,-2.5,q),L(-3.6,-2.8,q),L(2.8,2.2,q)),(0,1.2,.9),24,5.0)
            return
        sitting(t)
        put_at(AM,t,2.6,-1.6,-125); AM['arm'][1].rotation_euler=(R(-75),0,R(-10)); bpy.context.view_layer.update(); cup.location=hand_pos(AM,1)+Vector((0,-.03,.06))
        look_at(W,headpos(AM),.6)
        if view=='N_ammi': hideH(DA); talk(AM,t,313,321,KEY,rest='grin',rate=6); face(AM,brow=.05); look_at(AM,headpos(W),.6); face(W,mouth='flat',eyes=.8); cf(AM,d=2.0,lat=.45,lens=30)
        elif view=='N_tabiyat':
            hideH(DA); talk(W,t,322,326,KEY,rest='frown',shapes=('shout','O','frown')); face(W,brow=.1,brow_r=-15); W['head'].rotation_euler[1]=R(8)
            cf(W,d=2.3,lat=-.35,dz=.05,lens=30)
        elif view=='N_dadi':
            k=ease(cl(t/.5)); put_at(DA,t,1.3,2.2,10,0); dance(DA,t,'dadi'); DA['root'].location[2]=L(-1.4,0,k)+.008+.02
            talk(DA,t,327,336,KEY,rest='grin',rate=7,shapes=('shout','grin','O')); face(DA,brow=.08,eyes=.9)
            W['head'].rotation_euler[2]=R(-55*ease(cl((t-.5)/.3))); face(W,mouth='O',eyes=1.3,brow=.14)
            camset((-1.9,-1.0,1.7),(.8,1.5,1.3),26,4.0)
        else:
            put_at(DA,t,1.3,2.2,10); dance(DA,t,'dadi'); face(DA,mouth='grin')
            W['head'].rotation_euler[2]=0; talk(W,t,337,343,KEY,rest='O',shapes=('shout','O')); face(W,brow=.16,eyes=1.4); ARMV(W,150,6*math.sin(t*14))
            q=ease(t/DUR); cf(W,d=L(2.6,1.9,q),lat=-.3,lens=30)
    return dict(upd=upd)
for v in ('N_morning','N_ammi','N_tabiyat','N_dadi','N_bahar'): SHOTS[v]=(lambda v=v: SH_N(v))
