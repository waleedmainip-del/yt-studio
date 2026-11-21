SHOTS={}
WJ=json.load(open('/home/claude/lahore/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('H_sky',0),('H_roof',20),('B_meet',23),('B_wake',29),('B_mirror',39),('B_mother',50),('B_busy',60),('B_mom2',64),('B_leave',75),
    ('F_wide',81),('F_car',87),('F_phone',94),('F_third',102),('F_l1',114),('F_l2',119),('F_l3',127),('F_l4',134),('F_fight',141),
    ('T_arrive',152),('T_bazaar',159),('T_appr',169),('T_ask',172),('T_look',179),('T_puttar',191),('T_what',204),('T_vekh',205),
    ('X_explore',212),('X_arch',225),('X_friends',229),('X_teach',235),('X_change',238),('X_greet',245),('X_morning',258),('X_oye',267),('X_ban',272),
    ('Z_adjust',279),('Z_pawa',290),('Z_freeze',298),('Z_agge',300),('Z_shout',309),('Z_final',323)]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.1,3)) for k,i in _K]
END=round(WE[-1]+.45,3)
def TK(key): return [t for k,t in SEQ if k==key][0]
def wl(i,key): return WS[i]-TK(key)
def we(i,key): return WE[i]-TK(key)
def talk(H,t,a,b,key,rest='smile',rate=8.0,shapes=('O','flat','o','grin','flat')):
    t0=wl(a,key); t1=we(b,key)
    if t0<=t<t1: face(H,mouth=shapes[int((t-t0)*rate+H['seed']*3)%len(shapes)])
    else: face(H,mouth=rest)
    return t0<=t<t1
def sway(H,t,amp=1.0):
    s=H['seed']; H['root'].rotation_euler[1]=R(2*amp)*math.sin(t*1.7+s); H['head'].rotation_euler[1]=R(3*amp)*math.sin(t*2.1+s*2)
def lane_day(**kw):
    lane(**kw); B.done('lane'); setup_render('morning_s',res=PCT,samples=SAMPLES)
def bazaar_day():
    lane(-30,30,bazaar=True,seed=11); B.done('bazaar'); setup_render('afternoon',res=PCT,samples=SAMPLES)
def masjid_set(mood='morning'):
    badshahi(30); skyline(5,0,0,120); B.done('masjid'); setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=90)
def home_set():
    mir=home(); S,A,w,bg=setup_interior('day',room=(0,0,3.4),res=PCT,samples=SAMPLES)
    point((-1.9,2.0,1.9),40,(1,.92,.78),.3); point((4.6,1.6,2.9),60,(1,.95,.85),.4); return mir

# ============================================================ HOOK
def SH_hook(view):
    KEY='H_'+view
    if view=='sky':
        masjid_set('golden'); kites((0,-20,0),40,18,4,zr=(30,55))
        def upd(t):
            q=ease(t/DUR); a=R(-118+22*q); rr=L(92,74,q)
            camset((rr*math.cos(a)*.75,30+rr*math.sin(a)*.75,L(62,44,q)),(0,25,L(10,13,q)),26,8.0)
        return dict(upd=upd)
    lane_day(x0=-20,x1=20,seed=7)
    pts=[(-2.2,.4,20),(-.8,-.4,0),(.6,.2,-15),(2.0,-.3,-10),(-1.5,1.6,10),(1.2,1.5,-5),(3.1,1.0,-20),(-3.2,1.2,25),(0,1.9,0)]
    cs=crowd(pts,40,'shout')
    def upd(t):
        for i,c in enumerate(cs):
            blink(c,t); stand(c,t); k=ease((t-i*.04)/.25); b=.5+.5*math.sin(t*9+i)
            arms(c,-160*k-10*b,0,15,-160*k-10*b,0,-15); c['root'].location[2]=c['z0']+.008+.12*k*max(0,math.sin(t*8+i*1.3)); face(c,mouth='shout',brow=.07)
        q=ease(t/DUR); camset((0,-4.6+.4*q,.9),(0,.4,2.6+.4*q),20,8.0)
    return dict(upd=upd)
for v in ('sky','roof'): SHOTS['H_'+v]=(lambda v=v: SH_hook(v))

# ============================================================ HOME
def SH_home(view):
    KEY='B_'+view; mir=home_set()
    if view in ('meet','wake','mirror','busy','leave'):
        H=person((-.2,1.2,0),180,HAMZA,'smile',name='hamza')
    if view in ('mother','mom2'):
        Mo=person((4.2,1.6,0),180,MOTHER,'shout',name='mother'); ld=ladle(Mo,1)
    if view=='meet':
        H['root'].location=(-1.2,.6,.008); H['root'].rotation_euler[2]=R(0)
        def upd(t):
            blink(H,t); stand(H,t); sway(H,t,.6); face(H,mouth='grin' if t>.6 else 'smile',brow=.03,brow_r=-6)
            k=ease((t-.4)/.5); H['arm'][1].rotation_euler=(R(-15*k),R(-35*k),R(70*k)); H['arm'][-1].rotation_euler=(R(-15*k),R(35*k),R(-70*k)); H['head'].rotation_euler[0]=R(-6*k)
            q=ease(t/DUR); camset((L(.5,.1,q),-3.6+.8*q,1.4),(-1.2,.6,1.65),30,4.0,focus=(-1.2,.6,1.8))
        return dict(upd=upd)
    if view=='wake':
        def upd(t):
            blink(H,t)
            if t<1.0:
                H['root'].location=(-3.0,1.05,.008); H['root'].rotation_euler=(0,0,R(0)); H['z0']=0; sit(H,1,.52,90)
                k=ease(t/.6); arms(H,-150*k,0,20,-150*k,0,-20); face(H,mouth='O' if t<.6 else 'smile',eyes=.5+.5*k)
            else:
                H['root'].scale=(1,1,1)
                p=walk_path(H,[(-3.0,1.0),(-1.6,1.0),(-.2,1.25)],t,1.0,DUR-.2); legs_k=1
                if p>=1: H['root'].rotation_euler[2]=R(180); stand(H,t)
                face(H,mouth='smile',brow=.02)
            q=ease(t/DUR); camset((L(-2.2,-1.2,q),-1.9,1.5),(L(-3.0,-.8,q),1.3,1.2),26,5.0)
        return dict(upd=upd)
    if view=='mirror':
        H['root'].location=(-.2,1.25,.008); H['root'].rotation_euler[2]=R(180)
        def upd(t):
            blink(H,t); stand(H,t); H['root'].rotation_euler[2]=R(180)
            sp=talk(H,t,39,49,KEY,rest='grin')
            a=wl(42,KEY); b=wl(45,KEY)
            if t<a: k=ease(t/.3); arms(H,-60*k,0,40*k,-60*k,0,-40*k); H['head'].rotation_euler=(R(-4),R(6*math.sin(t*6)),0)
            elif t<b: k=ease((t-a)/.25); arms(H,-150*k,0,25,-25,0,-10); H['head'].rotation_euler=(R(-8),R(-5),R(8))
            else:
                k=ease((t-b)/.3); arms(H,-100,0,-60*k,-100,0,60*k); H['head'].rotation_euler=(R(-10*k),0,R(10*math.sin(t*3)))
                H['root'].rotation_euler[1]=R(4*math.sin(t*4))
            face(H,brow=.05,brow_r=-8)
            q=ease(t/DUR); camset((.55,2.45,1.95),(-.2,1.2,L(1.7,1.85,q)),L(20,24,q),3.2,focus=(-.2,1.2,1.95))
        return dict(upd=upd)
    if view=='mother':
        Mo['root'].location=(4.0,1.5,.008)
        def upd(t):
            blink(Mo,t); stand(Mo,t); sp=talk(Mo,t,56,59,KEY,rest='frown',rate=7,shapes=('shout','O','shout','o'))
            k=ease((t-wl(56,KEY)+.2)/.25) if t>wl(56,KEY)-.3 else 0
            if t<wl(56,KEY)-.2: Mo['root'].rotation_euler[2]=R(0); arms(Mo,-55,0,10,-55,0,-10)
            else: Mo['root'].rotation_euler[2]=R(L(0,-60,k)); arms(Mo,-150*k-12*math.sin(t*10),0,20,-30,0,-30)
            face(Mo,brow=-.03,brow_r=16)
            steam_on=1
            q=ease(t/DUR); camset((L(2.6,2.3,q),-1.6,1.55),(4.0,1.6,L(1.3,1.6,q)),28,4.5,focus=(4.0,1.5,1.6))
        steam((3.8,2.2,1.33),0,DUR,n=14,size=.06)
        return dict(upd=upd)
    if view=='busy':
        H['root'].location=(-3.0,1.05,.008); H['z0']=0; ph=phone(H,1)
        def upd(t):
            blink(H,t); sit(H,1,.52,90); H['root'].rotation_euler[2]=R(-20)
            arm_reach(H,1,H['head'].matrix_world@Vector((.42,-.62,-.05)),1.0); arms_k=0
            H['arm'][-1].rotation_euler=(R(-20),0,R(-10))
            talk(H,t,60,63,KEY,rest='grin'); look_at(H,hand_pos(H,1),1.0)
            face(H,brow=.04,brow_r=-10)
            q=ease(t/DUR); camset((-1.5,-1.3,1.3),(-3.0,1.0,1.15),26,4.0,focus=(-3.0,1.0,1.2))
        return dict(upd=upd)
    if view=='mom2':
        Mo['root'].location=(1.6,.4,.008); Mo['root'].rotation_euler[2]=R(-110)
        def upd(t):
            blink(Mo,t); stand(Mo,t); talk(Mo,t,64,74,KEY,rest='frown',rate=7,shapes=('O','flat','shout','o'))
            arms(Mo,-20,0,60,-20,0,-60); Mo['arm'][1].rotation_euler=(R(-15),R(-35),R(70)); Mo['arm'][-1].rotation_euler=(R(-15),R(35),R(-70))
            if t>wl(68,KEY): Mo['arm'][1].rotation_euler=(R(-90),0,R(30*math.sin(t*6)))
            face(Mo,brow=-.04,brow_r=20); Mo['head'].rotation_euler[1]=R(8*math.sin(t*5))
            q=ease(t/DUR); camset((L(-.6,-.3,q),-1.4,1.45),(1.6,.4,1.75),30,4.0,focus=(1.6,.4,1.7))
        return dict(upd=upd)
    if view=='leave':
        ky=keys(H,-1)
        def upd(t):
            blink(H,t); face(H,mouth='smirk',brow=.02)
            if t<.7:
                H['root'].location=(-3.4,1.0,.008); H['root'].rotation_euler[2]=R(90); stand(H,t); k=ease(t/.4); H['arm'][-1].rotation_euler=(R(-70*k),0,0); ky.scale=(1,1,1) if t>.35 else (0,0,0)
            else:
                walk_path(H,[(-3.4,1.0),(-3.8,-.3),(-4.6,-1.4)],t,.7,DUR); ky.scale=(1,1,1)
                H['arm'][-1].rotation_euler[0]=R(-60+20*math.sin(t*8))
            q=ease(t/DUR); camset((-1.2,-2.6,1.5),(L(-3.4,-4.2,q),.0,1.3),26,6.0)
        return dict(upd=upd)
for v in ('meet','wake','mirror','mother','busy','mom2','leave'): SHOTS['B_'+v]=(lambda v=v: SH_home(v))

# ============================================================ FRIENDS (lane)
FX0=4.0
def friends_cast():
    cr=car(FX0+1.0,1.6,'#C9302C',rz=0)
    f1=person((FX0-1.8,.3,0),40,F1,'grin',name='f1'); f2=person((FX0-.6,-.9,0),10,F2,'smile',name='f2'); f3=person((FX0+.9,-.8,0),-30,F3,'flat',name='f3')
    return cr,f1,f2,f3
def SH_fr(view):
    KEY='F_'+view; lane_day(x0=-22,x1=26,seed=5); cr,f1,f2,f3=friends_cast(); H=person((FX0-3.2,-1.6,0),-60,HAMZA,'smile',name='hamza')
    ph=phone(f2,1,'#FFB86A'); peds=crowd([(-9,2.2,90),(14,-2.4,-90),(17,2.0,180),(-14,-2.0,0)],60)
    def bg(t):
        for i,c in enumerate(peds):
            blink(c,t)
            if i<2: walker(c,(c['x'],c['y'],0),c['rz'],1.1,t,arm=20)
            else: stand(c,t); gaze_idle(c,t)
    def base(t,hold=True):
        for c in (f1,f2,f3,H): blink(c,t); stand(c,t)
        f2['arm'][1].rotation_euler=(R(-75),0,R(15)) if hold else (0,0,0)
        bg(t)
    if view=='wide':
        def upd(t):
            base(t); walk_path(H,[(FX0-9,-1.2),(FX0-3.2,-1.4)],t,0,DUR*.9); face(H,mouth='smile')
            for c in (f1,f2,f3): look_at(c,H['root'].location+Vector((0,0,1.9)),.8)
            if t>DUR*.8: k=ease((t-DUR*.8)/.3); arms(f1,-150*k,0,20,0,0,0); face(f1,mouth='grin')
            q=ease(t/DUR); camset((FX0-4.2+.6*q,-4.6,1.7),(FX0-1.6,.2,1.5),18,8.0)
    elif view=='car':
        def upd(t):
            base(t); f2['root'].location=(FX0+2.4,-.4,.008); f3['root'].location=(FX0+3.4,-.2,.008); H['root'].location=(FX0-3.2,-1.4,.008); H['root'].rotation_euler[2]=R(60)
            f1['root'].location=(FX0-.9,.75,.008); f1['root'].rotation_euler[2]=R(-20)
            k=ease(t/.3); f1['arm'][-1].rotation_euler=(R(-80*k),R(-30*k),R(-60*k)); f1['arm'][1].rotation_euler=(R(-40+15*math.sin(t*5)),0,R(30))
            face(f1,mouth='grin',brow=.06,brow_r=-10); f1['head'].rotation_euler=(R(-8),0,R(8*math.sin(t*2)))
            q=ease(t/DUR); camset((FX0-3.2+1.2*q,-3.2,1.1),(FX0+.4,1.3,1.1),24,5.0,focus=(FX0-.9,.75,1.5))
    elif view=='phone':
        def upd(t):
            base(t,False); f2['root'].location=(FX0-.6,-.9,.008); f2['root'].rotation_euler[2]=R(-30)
            arm_reach(f2,1,f2['root'].matrix_world@Vector((.38,-.6,1.45)),1.0); face(f2,mouth='grin',brow=.08); f2['head'].rotation_euler[2]=R(15*math.sin(t*2))
            ph.rotation_euler=(R(0),0,R(0))
            q=ease(t/DUR); camset((FX0-.1,-4.0+.4*q,1.5),(FX0-.6,-.9,1.55),26,3.5,focus=(FX0-.6,-1.0,1.6))
    elif view=='third':
        def upd(t):
            base(t); f3['root'].rotation_euler[2]=R(-20); f3['arm'][1].rotation_euler=(R(-100),0,R(10*math.sin(t*9)))
            f3['arm'][-1].rotation_euler=(R(-40),0,R(-30)); face(f3,mouth=('O','flat','shout')[int(t*6)%3],brow=-.04,brow_r=18); f3['head'].rotation_euler[1]=R(8*math.sin(t*5))
            look_at(f1,(FX0+.9,-.8,1.9)); look_at(f2,(FX0+.9,-.8,1.9))
            q=ease(t/DUR); camset((FX0+2.4,-3.3,1.2),(FX0+.6,-.6,1.75),28,4.0,focus=(FX0+.9,-.8,1.8))
    elif view=='l1':
        def upd(t):
            base(t); f1['root'].location=(FX0-.9,.75,.008); f1['root'].rotation_euler[2]=R(-10); f2['root'].location=(FX0+1.9,-.5,.008); f3['root'].location=(FX0+2.9,-.3,.008)
            talk(f1,t,114,118,KEY,rest='grin'); f1['arm'][-1].rotation_euler=(R(-95),R(-10),R(-70+10*math.sin(t*7))); f1['arm'][1].rotation_euler=(R(-160),0,R(15))
            face(f1,brow=.07); q=ease(t/DUR); camset((FX0-1.6,-1.6,.75),(FX0-.6,.9,1.9),22,4.0,focus=(FX0-.9,.75,1.9))
    elif view=='l2':
        def upd(t):
            base(t,False); f2['root'].rotation_euler[2]=R(-15); talk(f2,t,119,126,KEY,rest='grin')
            arm_reach(f2,1,f2['root'].matrix_world@Vector((.4,-.62,1.5)),1.0); f2['arm'][-1].rotation_euler=(R(-60),0,R(-40+20*math.sin(t*6)))
            face(f2,brow=.06,brow_r=-8); q=ease(t/DUR); camset((FX0-.4,-3.6,1.55),(FX0-.6,-.9,1.65),28,3.2,focus=(FX0-.6,-1.1,1.7))
    elif view=='l3':
        def upd(t):
            base(t); H['root'].location=(FX0-2.4,-1.2,.008); H['root'].rotation_euler[2]=R(30); talk(H,t,127,133,KEY,rest='smirk')
            a=wl(128,KEY); k=ease((t-a)/.2) if t>a else 0
            arms(H,-40-50*k,0,-45*k,-40-50*k,0,45*k) if t>a else arms(H,-60,0,30,-60,0,-30)
            H['root'].scale=(1+.04*k,1+.04*k,1); H['head'].rotation_euler[0]=R(-10*k)
            face(H,brow=.03,brow_r=-10); look_at(f1,(FX0-2.4,-1.2,1.9)); look_at(f3,(FX0-2.4,-1.2,1.9))
            q=ease(t/DUR); camset((FX0-1.6,-3.8,1.0),(FX0-2.4,-1.2,1.85),26,3.5,focus=(FX0-2.4,-1.2,1.9))
    elif view=='l4':
        def upd(t):
            base(t); talk(f3,t,134,140,KEY,rest='grin'); k=ease((t-wl(135,KEY))/.3)
            arms(f3,-90-60*k,0,40*k,-90-60*k,0,-40*k); f3['root'].rotation_euler[2]=R(-15)
            face(f3,brow=.08); q=ease(t/DUR); camset((FX0+1.8,-2.8,.9),(FX0+.9,-.8,1.95),24,4.0,focus=(FX0+.9,-.8,1.9))
    elif view=='fight':
        def upd(t):
            base(t,False)
            ring=[(f1,(FX0-.6,.3)),(f2,(FX0+.6,.2)),(f3,(FX0+.7,-1.0)),(H,(FX0-.7,-1.1))]
            for i,(c,p) in enumerate(ring):
                c['root'].location=(p[0],p[1],.008); c['root'].rotation_euler[2]=R(heading_to(c,(FX0,-.4))); c['root'].location[2]=.008+.05*abs(math.sin(t*7+i))
                c['arm'][1].rotation_euler=(R(-100+30*math.sin(t*8+i)),0,R(20)); c['arm'][-1].rotation_euler=(R(-60+30*math.sin(t*7+i*2)),0,R(-30))
                face(c,mouth=('shout','O','flat')[int(t*7+i)%3],brow=-.04,brow_r=18); c['head'].rotation_euler[1]=R(9*math.sin(t*6+i))
            a=R(-90+70*t/DUR); camset((FX0+4.2*math.cos(a),-.4+4.2*math.sin(a),2.1),(FX0,-.4,1.6),24,6.0)
    return dict(upd=upd)
for v in ('wide','car','phone','third','l1','l2','l3','l4','fight'): SHOTS['F_'+v]=(lambda v=v: SH_fr(v))

# ============================================================ TOURIST (bazaar)
def bz_people(seed=70):
    sp=[]; r=random.Random(seed)
    for i in range(16): sp.append((r.uniform(-22,22),r.uniform(1.8,3.8) if i%4 else -r.uniform(3.4,3.9),r.choice((90,-90))))
    return crowd(sp,seed)
def bz_bg(cs,t):
    for i,c in enumerate(cs):
        blink(c,t)
        if i%3!=2: walker(c,(c['x'],c['y'],0),c['rz'],.9+.1*(i%3),t,arm=18)
        else: stand(c,t); gaze_idle(c,t)
def SH_tour(view):
    KEY='T_'+view; bazaar_day(); cs=bz_people(); T=person((-6,0,0),90,TOUR,'smile',name='tour'); HX=3.0
    H=person((HX,.4,0),-90,HAMZA,'flat',name='hamza')
    if view=='arrive':
        rk=rickshaw(-14,2.6,90); bk=bike(10,1.2,-90)
        def upd(t):
            bz_bg(cs,t); blink(H,t); hideH(H)
            walk_path(T,[(-11,-.3),(-6.5,0)],t,0,DUR,step=.5); look_at(T,(-4,2,4.5),.7); face(T,mouth='O' if t>1.2 else 'smile',brow=.08,eyes=1.15)
            rk.location[0]=-14+7*t; bk.location[0]=10-6*t
            q=ease(t/DUR); camset((-3.0,-2.6,.55),(-8.5,0,2.1),20,8.0)
    elif view=='bazaar':
        def upd(t):
            bz_bg(cs,t); hideH(H); x0=-6.5
            walk_path(T,[(x0,0),(x0+4.5,.1)],t,0,DUR,step=.5)
            look_at(T,(T['root'].location.x+2*math.sin(t*.8),3.0*math.sin(t*.9),3.0+1.5*math.sin(t*.6)),.9)
            face(T,mouth='O' if (t%1.6)<.8 else 'grin',brow=.08,eyes=1.1); T['arm'][1].rotation_euler[0]+=R(-25)
            x=T['root'].location.x; camset((x+3.2,-2.4,1.7),(x,0,1.9),24,5.0,focus=(x,0,1.9))
    elif view=='appr':
        def upd(t):
            bz_bg(cs,t); blink(H,t); stand(H,t); face(H,mouth='flat')
            walk_path(T,[(-1.5,.1),(HX-1.1,.25)],t,0,DUR*.95,step=.5); face(T,mouth='smile',brow=.06); look_at(T,(HX,.4,1.9))
            H['root'].rotation_euler[2]=R(-90+30*ease(t/DUR)); look_at(H,T['root'].location+Vector((0,0,2)),.6*ease(t/DUR))
            q=ease(t/DUR); camset((HX+.6,-3.6,1.6),(HX-1.0,.3,1.7),26,6.0)
    elif view=='ask':
        def upd(t):
            bz_bg(cs,t); blink(H,t); blink(T,t); stand(H,t); stand(T,t)
            T['root'].location=(HX-1.15,.25,.008); T['root'].rotation_euler[2]=R(80); H['root'].rotation_euler[2]=R(-80)
            talk(T,t,172,178,KEY,rest='smile'); T['arm'][1].rotation_euler=(R(-70),0,R(25+15*math.sin(t*4))); T['arm'][-1].rotation_euler=(R(-20),0,0)
            face(T,brow=.07,brow_r=-6); face(H,mouth='flat',brow=0)
            q=ease(t/DUR); camset((HX+.1,-1.8,1.8),(HX-1.15,.3,1.95),30,3.8,focus=(HX-1.15,.3,1.95))
    elif view=='look':
        def upd(t):
            bz_bg(cs,t); blink(H,t,0 if t<1.2 else None); blink(T,t); stand(H,t); stand(T,t)
            T['root'].location=(HX-1.15,.25,.008); T['root'].rotation_euler[2]=R(80); H['root'].rotation_euler[2]=R(-80)
            k=ease(t/1.0); H['head'].rotation_euler=(R(-5*k),R(-10*k),R(-12*k)); face(H,mouth='flat',brow=.06*k,brow_r=-22*k)
            for o_ in H['brows']: pass
            q=ease(t/DUR); camset((HX-.9,-1.4,1.95),(HX,.4,2.05),L(34,46,q),2.8,focus=(HX,.4,2.05))
    elif view=='puttar':
        def upd(t):
            bz_bg(cs,t); blink(H,t); blink(T,t); stand(H,t); stand(T,t)
            T['root'].location=(HX-1.0,.25,.008); T['root'].rotation_euler[2]=R(80); H['root'].rotation_euler[2]=R(-80)
            arm_reach(H,-1,T['root'].matrix_world@Vector((.45*T['u'],0,3.9*T['u'])),ease(t/.4))
            talk(H,t,191,203,KEY,rest='flat',rate=6.5); big=t>wl(196,KEY)
            if big: k=ease((t-wl(196,KEY))/.25); H['arm'][1].rotation_euler=(R(-150*k),0,R(15)); H['head'].rotation_euler[0]=R(-8*k)
            face(H,brow=-.03 if big else .03,brow_r=18 if big else -6); face(T,mouth='o',brow=.06)
            q=ease(t/DUR); camset((L(HX-1.4,HX-1.0,q),-2.4+.8*q,L(1.0,1.3,q)),(HX-.5,.3,1.95),L(26,32,q),4.0,focus=(HX,.4,2.0))
            SHAKE[0]=.012 if big else 0
    elif view=='what':
        def upd(t):
            bz_bg(cs,t); blink(T,t,0); stand(T,t); T['root'].location=(HX-1.0,.25,.008); T['root'].rotation_euler[2]=R(80); hideH(H)
            k=ease(t/.15); face(T,mouth='O',brow=.14*k,eyes=1+.35*k); shock(T,.7*k); T['root'].rotation_euler[0]=R(6*k)
            camset((HX+.4,-1.7,1.95),(HX-1.0,.25,2.1),34,3.0,focus=(HX-1.0,.25,2.05))
    elif view=='vekh':
        def upd(t):
            bz_bg(cs,t); blink(H,t); blink(T,t); stand(H,t); stand(T,t)
            T['root'].location=(HX-1.0,.25,.008); T['root'].rotation_euler[2]=R(80); H['root'].rotation_euler[2]=R(-60)
            talk(H,t,205,211,KEY,rest='grin'); k=ease(t/.4); H['arm'][1].rotation_euler=(R(-95*k),R(0),R(-55*k)); H['arm'][-1].rotation_euler=(R(-20),0,0)
            look_at(T,(HX-4,0,4),ease((t-.5)/.6)); face(T,mouth='o',brow=.08); face(H,brow=.04,brow_r=-8)
            q=ease(t/DUR); camset((HX-1.3,-2.8,1.4),(HX-.6,.4,2.0),24,6.0)
    return dict(upd=upd)
for v in ('arrive','bazaar','appr','ask','look','puttar','what','vekh'): SHOTS['T_'+v]=(lambda v=v: SH_tour(v))

# ============================================================ TRANSFORMATION
def SH_x(view):
    KEY='X_'+view
    if view in ('arch','morning','oye','ban'):
        masjid_set('morning_s' if view!='arch' else 'afternoon')
        pil=crowd([(-12,-18,30),(14,-22,-40),(-20,-8,90),(22,-12,-80),(12,-20,10),(-8,-26,0)],90)
        def pbg(t):
            for i,c in enumerate(pil):
                blink(c,t)
                if i<3: walker(c,(c['x'],c['y'],0),c['rz'],.8,t,arm=16)
                else: stand(c,t); gaze_idle(c,t)
        if view=='arch':
            T=person((-1.2,-18,0),180,TOUR,'O',name='tour'); H=person((1.0,-18.5,0),180,HAMZA,'grin',name='hamza')
            def upd(t):
                pbg(t)
                for c in (T,H): blink(c,t); stand(c,t)
                look_at(T,(0,30,18),1.0); face(T,mouth='O',brow=.12,eyes=1.2); shock(T,.35); H['arm'][1].rotation_euler=(R(-100),0,R(-30)); look_at(H,(-1.2,-18,2))
                q=ease(t/DUR); camset((L(-3,-1.5,q),-25,1.0),(0,-10,L(8,12,q)),20,8.0)
            return dict(upd=upd)
        T=person((0,-14,0),0,TOUR2,'grin',name='tour2'); H=person((2,-34,0),180,HAMZA,'smile',name='hamza')
        if view=='morning':
            def upd(t):
                pbg(t); blink(T,t); stand(T,t); T['arm'][1].rotation_euler=(R(-20),R(-35),R(70)); T['arm'][-1].rotation_euler=(R(-20),R(35),R(-70)); face(T,mouth='grin')
                walk_path(H,[(3,-29),(1.5,-20)],t,0,DUR,step=.55); face(H,mouth='flat',brow=.03); blink(H,t)
                q=ease(t/DUR); camset((L(7,5,q),-30+2*q,L(2.2,3.0,q)),(0,-12,L(6,4,q)),22,8.0)
        elif view=='oye':
            H['root'].location=(1.0,-19.0,.008); H['root'].rotation_euler[2]=R(180)
            def upd(t):
                pbg(t); blink(T,t); blink(H,t); stand(T,t); stand(H,t); H['root'].rotation_euler[2]=R(170)
                talk(T,t,267,271,KEY,rest='grin',shapes=('shout','O','shout','grin')); k=ease(t/.25)
                arms(T,-165*k,0,25+20*math.sin(t*10),-30,0,-20); T['root'].location[2]=.008+.08*max(0,math.sin(t*7))
                face(T,brow=.1); q=ease(t/DUR); camset((2.8,-19.8,1.45),(0,-14.2,1.95),L(28,34,q),4.0,focus=(0,-14,2.0))
        elif view=='ban':
            H['root'].location=(1.0,-19.0,.008)
            def upd(t):
                pbg(t); blink(H,t,0); blink(T,t); stand(T,t); stand(H,t); H['root'].rotation_euler[2]=R(170)
                talk(H,t,272,278,KEY,rest='O',shapes=('shout','O','shout','o')); k=ease(t/.2)
                arm_to(H,1,(0,-14,2.0),k); H['arm'][-1].rotation_euler=(R(-140*k),0,R(-20)); face(H,brow=.13,eyes=1+.3*k); H['root'].rotation_euler[0]=R(-5*k)
                face(T,mouth='grin'); T['arm'][1].rotation_euler=(R(-20),R(-35),R(70)); T['arm'][-1].rotation_euler=(R(-20),R(35),R(-70))
                q=ease(t/DUR); camset((-.2,-16.4,1.8),(1.0,-19,2.0),L(26,32,q),3.5,focus=(1.0,-19,2.0))
        return dict(upd=upd)
    lane_day(x0=-22,x1=26,seed=5 if view!='greet' else 13)
    if view=='explore':
        T=person((-8,0,0),90,TOUR,'grin',name='tour'); H=person((-8,1,0),90,HAMZA,'smile',name='hamza'); peds=crowd([(6,2.0,-90),(10,-2.0,-90),(-12,2.2,90)],95)
        def upd(t):
            for i,c in enumerate(peds): blink(c,t); walker(c,(c['x'],c['y'],0),c['rz'],1.0,t,arm=18)
            blink(T,t); blink(H,t); walk_path(T,[(-9,-.5),(-1,-.5)],t,0,DUR+.3,step=.55); walk_path(H,[(-8.6,.6),(-.6,.6)],t,0,DUR+.3,step=.55)
            look_at(T,(T['root'].location.x+3,3.5,4.5),.9); face(T,mouth='O' if (t%1.4)<.6 else 'grin',brow=.08)
            H['arm'][1].rotation_euler=(R(-95),0,R(-60)) if 1.2<t<2.8 else H['arm'][1].rotation_euler; face(H,mouth='grin')
            x=T['root'].location.x; camset((x+5.5,-3.0,1.4),(x+.5,0,1.9),26,7.0)
    elif view=='friends':
        cr,f1,f2,f3=friends_cast(); T=person((FX0-2.6,-1.2,0),60,TOUR,'grin',name='tour'); H=person((FX0-3.4,-.2,0),40,HAMZA,'smile',name='hamza')
        def upd(t):
            for c in (f1,f2,f3,T,H): blink(c,t); stand(c,t)
            f1['root'].location=(FX0-1.4,-.6,.008); f1['root'].rotation_euler[2]=R(-120); T['root'].rotation_euler[2]=R(70)
            sh=math.sin(t*9)*.5+.5; T['arm'][1].rotation_euler=(R(-75-14*sh),0,R(-20)); f1['arm'][1].rotation_euler=(R(-75-14*sh),0,R(20))
            for c in (f2,f3): look_at(c,(FX0-2.6,-1.2,2)); face(c,mouth='grin')
            face(T,mouth='grin',brow=.06); face(f1,mouth='grin',brow=.05); f3['arm'][1].rotation_euler=(R(-140),0,R(15+20*math.sin(t*6)))
            H['arm'][1].rotation_euler=(R(-90),0,R(-40)); face(H,mouth='smile')
            q=ease(t/DUR); camset((FX0-2.0,-4.3+.5*q,1.5),(FX0-1.9,-.9,1.7),26,5.0,focus=(FX0-2.0,-.9,1.7))
    elif view=='teach':
        T=person((-1.0,-1.6,0),90,TOUR,'o',name='tour'); H=person((.6,-1.6,0),-90,HAMZA,'smile',name='hamza')
        def upd(t):
            blink(T,t); blink(H,t)
            for c,x in ((T,-.9),(H,.5)): c['root'].location=(x,-1.6,.008); c['z0']=0; sit(c,1,.48,90)
            mouth_talk(H,t,0,DUR*.45,rate=7); mouth_talk(T,t,DUR*.5,DUR,rate=7,rest='grin')
            H['arm'][1].rotation_euler=(R(-80),0,R(-25*math.sin(t*5))) if t<DUR*.5 else (R(-40),0,0)
            T['arm'][1].rotation_euler=(R(-90),0,R(30)) if t>DUR*.5 else (R(-40),0,0); face(T,brow=.06); face(H,brow=.04)
            q=ease(t/DUR); camset((-.2,-4.7,1.3),(-.2,-1.6,1.3),22,4.0,focus=(-.2,-1.6,1.4))
        B2=Batch()
        for x in (-.9,.5): B2.box((x,-1.6,.22),(.4,.35,.22),M('#6B4026',.6,kind='wood'),.02); B2.box((x,-1.6,.46),(.42,.38,.03),M('#C9B48A',.8,kind='fabric'),.02)
        B2.box((-.2,-1.0,.35),(.3,.3,.35),M('#8A5A3A',.6,kind='wood'),.02); B2.cyl((-.2,-1.0,.78),.06,.1,M('#F4F1EA',.4),seg=12); B2.cyl((-.05,-.95,.78),.06,.1,M('#F4F1EA',.4),seg=12)
        B2.done('chairs'); steam((-.2,-1.0,.85),0,DUR,n=6,size=.03)
    elif view=='change':
        T=person((-6,0,0),90,TOUR2,'smirk',name='tour2')
        def upd(t):
            blink(T,t); p=walk_path(T,[(-1.0,-4.0),(-1.0,-.6)],t,0,DUR*1.2,step=.48)
            T['root'].rotation_euler[2]=R(0+180)
            face(T,mouth='smirk',brow=.02,brow_r=-6); T['arm'][-1].rotation_euler[0]*=.4
            q=ease(t/DUR); camset((-1.0,L(-7.8,-6.8,q),.45),(-1.0,-1.5,1.75),30,3.5,focus=T['root'].location+Vector((0,0,1.8)))
        T['root'].location=(-1.0,-.6,0)
        def upd2(t):
            blink(T,t); d=.4+.95*t; T['root'].location=(4.0-d,-.4,.008); T['root'].rotation_euler[2]=R(-90); walk(T,d,step=.5,arm=14)
            face(T,mouth='smirk',brow=.02,brow_r=-6)
            q=ease(t/DUR); camset((-3.4+.5*q,-.4,.45),(4.0-d*.6,-.4,1.75),30,3.5,focus=T['root'].location+Vector((0,0,1.8)))
        return dict(upd=upd2)
    elif view=='greet':
        T=person((-3,0,0),90,TOUR2,'grin',name='tour2'); loc=crowd([(-.8,1.3,-10),(.6,1.7,10),(1.8,1.2,-15),(3.6,1.5,20)],120,'grin')
        def upd(t):
            blink(T,t); walk_path(T,[(-4.5,0),(2.4,0)],t,0,DUR,step=.5); x=T['root'].location.x
            T['arm'][1].rotation_euler=(R(-160),0,R(20+25*math.sin(t*8))); face(T,mouth='grin' if (t%1.2)>.4 else 'O',brow=.07)
            look_at(T,(x+1.5,1.5*math.sin(t*1.3),1.9),.8)
            for i,c in enumerate(loc):
                blink(c,t); stand(c,t); d=abs(c['x']-x); k=ease((1.8-d)/.8); look_at(c,(x,0,1.9)); c['arm'][1].rotation_euler=(R(-150*k),0,R(20+25*math.sin(t*8+i)*k)); face(c,mouth='grin' if k>.3 else 'smile')
            camset((x+1.6,-4.4,1.6),(x+.2,0,1.6),20,6.0)
    return dict(upd=upd)
for v in ('explore','arch','friends','teach','change','greet','morning','oye','ban'): SHOTS['X_'+v]=(lambda v=v: SH_x(v))

# ============================================================ FINAL TWIST (masjid courtyard)
def SH_z(view):
    KEY='Z_'+view; masjid_set('golden' if view in ('shout','final') else 'morning_s')
    T=person((0,-14,0),15,TOUR2,'smirk',name='tour2'); H=person((1.0,-16.0,0),195,HAMZA,'O',name='hamza')
    big=None
    if view=='shout':
        sp=[]; r=random.Random(9)
        for ring_,n in ((3.2,8),(4.8,12),(6.6,14)):
            for i in range(n): a=pi*.15+pi*1.7*i/n+r.uniform(-.08,.08); sp.append((math.cos(a)*ring_,-14+math.sin(a)*ring_,0))
        big=crowd([(x,y,math.degrees(math.atan2(0-x,-(-14-y)))) for x,y,_ in sp],150,'smile')
    def upd(t):
        blink(T,t); blink(H,t); stand(T,t); stand(H,t); H['root'].location=(1.0,-16.0,.008); H['root'].rotation_euler[2]=R(195)
        if view=='adjust':
            k=ease((t-.4)/.5); arm_reach(T,1,T['head'].matrix_world@Vector((.25*T['u'],-.75*T['u'],.72*T['u'])),k)
            T['shades'].location=Vector(T['shades']['base'])+Vector((0,0,.03*math.sin(pi*min(1,max(0,(t-.6)/.6)))))
            face(T,mouth='smirk',brow=-.01,brow_r=-8); look_at(T,(1.0,-16,2.0),ease((t-1.6)/.6)); hideH(H) if t<0 else None
            q=ease(t/DUR); camset((L(-.9,-.6,q),-16.2,L(1.2,1.35,q)),(0,-14,2.0),L(30,40,q),2.8,focus=(0,-14,2.05))
        elif view=='pawa':
            talk(T,t,290,297,KEY,rest='smirk'); T['arm'][1].rotation_euler=(R(-15),R(-35),R(70)); T['arm'][-1].rotation_euler=(R(-15),R(35),R(-70))
            if t>wl(294,KEY): T['arm'][1].rotation_euler=(R(-60),0,R(-30)); T['root'].scale=(1.03,1.03,1)
            look_at(T,(1.0,-16,2.0)); face(T,brow=-.01,brow_r=-10); face(H,mouth='o',brow=.05)
            q=ease(t/DUR); camset((-.9,-17.0,1.05),(0,-14,2.0),28,3.2,focus=(0,-14,2.0))
        elif view=='freeze':
            blink(H,t,0); face(H,mouth='o',brow=.14,eyes=1.35); H['arm'][1].rotation_euler=(R(-8),0,0)
            q=ease_out(min(1,t/.35)); camset((1.7,L(-12.6,-14.0,q),1.95),(1.0,-16,2.05),L(30,52,q),2.5,focus=(1.0,-16,2.05))
        elif view=='agge':
            blink(H,t,0); talk(H,t,300,308,KEY,rest='O',shapes=('shout','O','shout','o')); k=ease(t/.25)
            arm_reach(H,1,H['head'].matrix_world@Vector((.7*H['u'],0,1.1*H['u'])),k); arm_reach(H,-1,H['head'].matrix_world@Vector((-.7*H['u'],0,1.1*H['u'])),k)
            H['root'].rotation_euler[0]=R(-6*k); H['head'].rotation_euler[1]=R(10*math.sin(t*6)); face(H,brow=.13,eyes=1.25)
            q=ease(t/DUR); camset((1.9,-14.0,1.6),(1.0,-16,2.0),30,3.5,focus=(1.0,-16,2.0))
        elif view=='shout':
            ts=wl(316,KEY); k=ease((t-wl(310,KEY))/.35); arms(T,-170*k,0,25,-170*k,0,-25); T['root'].location[2]=.008+(.15*max(0,math.sin((t-ts)*7)) if t>ts else 0)
            face(T,mouth='shout' if t>ts else 'grin',brow=.1); look_at(T,(0,-30,6),k*.6)
            face(H,mouth='O',brow=.1); H['root'].rotation_euler[2]=R(195)
            for i,c in enumerate(big):
                blink(c,t); stand(c,t); kk=ease((t-wl(319,KEY)-i*.02)/.3) if t>wl(319,KEY)-.1 else 0
                arms(c,-165*kk,0,20,-165*kk,0,-20); c['root'].location[2]=.008+.12*kk*max(0,math.sin(t*8+i)); face(c,mouth='shout' if kk>.2 else 'O')
            q=ease(t/DUR); camset((L(1.2,4.5,q),L(-19.5,-24,q),L(1.0,4.5,q)),(0,-14,L(2.4,2.0,q)),L(26,20,q),8.0)
        elif view=='final':
            T['root'].location=(-1.2,-13.0,.008); face(T,mouth='grin')
            H['root'].rotation_euler[2]=R(0); H['root'].location=(1.0,-16.0,.008)
            talk(H,t,323,331,KEY,rest='smirk'); k=ease((t-wl(326,KEY))/.3) if t>wl(326,KEY) else 0
            arm_to(H,1,(5,-13,4.5),k); H['arm'][-1].rotation_euler=(R(-15),R(35),R(-70)) if k>0 else (0,0,0)
            face(H,brow=.04,brow_r=-10); H['head'].rotation_euler[0]=R(-4)
            q=ease(t/DUR); camset((1.0,L(-19.2,-18.4,q),1.95),(1.0,-16,2.05),L(30,36,q),3.0,focus=(1.0,-16,2.05))
    return dict(upd=upd)
for v in ('adjust','pawa','freeze','agge','shout','final'): SHOTS['Z_'+v]=(lambda v=v: SH_z(v))
