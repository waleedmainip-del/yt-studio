SHOTS={}
WJ=json.load(open('/home/claude/fsd/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('H_aerial',0),('H_cloth',14),('H_mill',17),('H_shops',20),('H_ceo',23),('H_welcome',35),
    ('I_jump',38),('I_boys',41),('I_paise',47),('I_nahi',49),('I_exp',50),('I_toh',52),('I_vision',56),('I_ceo',57),
    ('C_sit',59),('C_listen',68),('C_kapray',81),('C_kiski',87),('C_future',90),('C_investor',99),('C_doctor',108),
    ('S_borrow',120),('S_stall',128),('S_cust',133),('S_kitne',137),('S_price',141),('S_market',145),('S_bclass',152),('S_plane',161),
    ('S_laugh',166),('S_respect',170),('S_away',175),('S_bhaag',179),('S_comp',184),
    ('F_wide',189),('F_looms',197),('F_haan',203),('F_brand',208),('F_invest',217),('F_ideas',221),('F_stare',229),('F_beta',233),('F_partner',242),('F_bill',246),
    ('P_ring',255),('P_what',259),('P_jump',262),('P_500',266),('P_kisne',267),('P_adv',276),('P_kahan',281),('P_phone',285),('P_intl',295),
    ('R_back',302),('R_kahan',310),('R_prod',315),('R_noorder',321),('R_fake',332),('R_pre',341),('R_startup',348),('R_asli',354),
    ('Z_sit',372),('Z_ab',380),('Z_band',383),('Z_paise',387),('Z_partner',390),('Z_point',397),('Z_chai',403),('Z_over',405),('Z_paise2',410),('Z_look',418),
    ('Z_city',428),('Z_plans',437),('Z_kal',446),('Z_meet',451),('Z_kaam',453)]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.1,3)) for k,i in _K]
SEQ=[(k,(round(WE[417]+.08,3) if k=='Z_look' else t)) for k,t in SEQ]
END=round(WE[-1]+2.6,3)
def TK(key): return [t for k,t in SEQ if k==key][0]
def wl(i,key): return WS[i]-TK(key)
def we(i,key): return WE[i]-TK(key)
def talk(H,t,a,b,key,rest='smile',rate=8.0,shapes=('O','flat','o','grin','flat')):
    t0=wl(a,key); t1=we(b,key)
    if t0<=t<t1: face(H,mouth=shapes[int((t-t0)*rate+H['seed']*3)%len(shapes)])
    else: face(H,mouth=rest)
    return t0<=t<t1
def hand_w(H,s=1):
    u=H['u']; P=H['arm'][s]; return root_mat(H)@(Vector(P.location)+Euler(P.rotation_euler).to_matrix()@Vector((s*.5*u,0,-1.95*u)))
def carry(o,H,s=1,off=(0,0,0)):
    p=hand_w(H,s); o.location=(p.x+off[0],p.y+off[1],p.z+off[2])
def seatH(H,x,y,rz,sh=.62,k=1.0):
    H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler=(0,0,R(rz)); H['z0']=0; sit(H,k,sh,90); H['head'].rotation_euler=(0,0,0)
def standH(H,x,y,rz,t):
    H['root'].location[0]=x; H['root'].location[1]=y; stand(H,t); H['root'].rotation_euler[2]=R(rz)
def rest(H,t=0,a=-12):
    s=H['seed']; b=1.5*math.sin(t*1.3+s); arms(H,a+b,0,5,a-b,0,-5)
def breathe(H,t): H['root'].location[2]+=.006*math.sin(t*2.1+H['seed'])
def nod(H,t,amp=5,rate=5): H['head'].rotation_euler[0]=R(amp)*math.sin(t*rate)
def headpos(H): u=H['u']; return tuple(root_mat(H)@Vector((0,0,4.75*u)))
PEOPLE=[]; _pers=person
def person(*a,**k):
    H=_pers(*a,**k); PEOPLE.append(H); return H
CAMLOCK={}; PROBE=[False]
def _root_of(o):
    while o.parent is not None: o=o.parent
    return o
def _is_person(o,ignore=None):
    r=_root_of(o)
    for H in PEOPLE:
        if H['root'] is r: return (ignore is None) or (H is not ignore)
    return False
def ray_clear(a,b,skip_people=False,ignore=None):
    """returns hit distance from a toward b, or None"""
    sc=bpy.context.scene; dg=bpy.context.evaluated_depsgraph_get(); a=Vector(a); b=Vector(b); d=b-a; n=d.length
    if n<1e-4: return None
    d.normalize(); o=a.copy(); travelled=0.0
    for _ in range(12):
        hit,loc,nrm,idx,ob,mx=sc.ray_cast(dg,o,d,distance=n-travelled)
        if not hit: return None
        ob=ob.original if hasattr(ob,'original') else ob
        step=(loc-o).length
        if (skip_people and _is_person(ob)) or (ignore is not None and _root_of(ob) is ignore['root'] and False):
            travelled+=step+.01; o=loc+d*.01; continue
        return travelled+step
    return None
_camset=camset
def camset(loc,tg,lens,fs=5.6,focus=None,roll=0):
    f=Vector(focus or tg); L_=Vector(loc); dv=L_-f; n=dv.length
    if n>.9:
        bpy.context.view_layer.update(); dn=dv.normalized(); h=ray_clear(f+dn*.4,L_,skip_people=True)
        if h is not None: L_=f+dn*max(.7,.4+h-.3)
    _camset(tuple(L_),tg,lens,fs,focus=focus,roll=roll)
def _clear_view(H,c):
    h=Vector(headpos(H)); c=Vector(c); d=(c-h).normalized(); side=d.cross(Vector((0,0,1))).normalized()
    for p in (h, h+side*.34, h-side*.34, h+Vector((0,0,.24)), h-Vector((0,0,.55)), h-Vector((0,0,.55))+side*.3, h-Vector((0,0,.55))-side*.3):
        if ray_clear(p+d*.36,c) is not None: return False
    return True
def cam_head(H,off,lens=40,fs=2.8,dz=0.0,lead=(0,0,0),q=None,ang=26,dist=3.0):
    h=headpos(H); rz=H['root'].rotation_euler[2]; key=H['root'].name+'%.0f%.0f'%(off[0],off[1])
    if key not in CAMLOCK:
        bpy.context.view_layer.update(); best=None
        sides=[]
        for sg in (1,-1):
            f=(math.sin(rz+sg*R(ang)),-math.cos(rz+sg*R(ang))); sides.append((f[0]*off[0]+f[1]*off[1],sg))
        sides.sort(reverse=True); order=[]
        for a in (ang,ang+14,max(0,ang-14),ang+28,ang+42,0):
            for _,sg in sides: order.append(sg*a)
        for dzz in (0.0,.35,.7):
            for a in order:
                for ds in (dist,dist*.8):
                    f=(math.sin(rz+R(a)),-math.cos(rz+R(a))); c=(h[0]+f[0]*ds,h[1]+f[1]*ds,h[2]+H.get('camdz',.08)+dz+dzz)
                    if _clear_view(H,c): best=(a,ds,dzz); break
                if best: break
            if best: break
        CAMLOCK[key]=best or (ang*sides[0][1],dist*.75,.3)
    a,ds,dzz=CAMLOCK[key]; f=(math.sin(rz+R(a)),-math.cos(rz+R(a)))
    _camset((h[0]+f[0]*ds,h[1]+f[1]*ds,h[2]+H.get('camdz',.08)+dz+dzz),(h[0]+lead[0]*.3,h[1]+lead[1]*.3,h[2]-.22),lens*.95*ds/3.0,fs,focus=h)
def pick(H,t,a,b,key):
    """quick reaction gesture while speaking"""
    pass
CROSS=lambda H: arms(H,-62,0,-58,-62,0,58)
HIPS=lambda H: arms(H,-8,0,-38,-8,0,38)
SHRUG=lambda H,k=1: arms(H,-25*k,0,-55*k,-25*k,0,55*k)
# ------------------------------------------------------------ crowd helpers
def strollers(specs,seed=0):
    out=[]
    for i,(pts,t0,t1) in enumerate(specs):
        C=design(900+seed*13+i*7) if i%2 else local(700+seed*11+i*5,female=(i%3==0)); H=person((pts[0][0],pts[0][1],0),0,C,'smile',name='w%d_%d'%(seed,i)); H['pts']=pts; H['tt']=(t0,t1); out.append(H)
    return out
def strollers_upd(G,t):
    for H in G: blink(H,t); walk_path(H,H['pts'],t,H['tt'][0],H['tt'][1],step=.52,arm=22,ease_in=.0,ease_out_=.0)
def idlers(specs,seed=0):
    out=[]
    for i,(x,y,rz,act) in enumerate(specs):
        C=local(500+seed*17+i*5,female=(i%4==1)) if i%2==0 else design(600+seed*7+i*3); H=person((x,y,0),rz,C,'smile',name='i%d_%d'%(seed,i)); H['act']=act; H['xy']=(x,y,rz); out.append(H)
    return out
def idlers_upd(G,t):
    for H in G:
        x,y,rz=H['xy']; standH(H,x,y,rz,t); blink(H,t); ph=H['seed']
        if H['act']=='talk': face(H,mouth=('o','flat','O','smile')[int(t*7+ph)%4]); arms(H,-30-15*math.sin(t*4+ph),0,10,-14,0,-5)
        elif H['act']=='phone': arms(H,-14,0,5,-140,0,-38); face(H,mouth='flat'); H['head'].rotation_euler=(R(14),0,0)
        elif H['act']=='sell': arms(H,-60-10*math.sin(t*3+ph),0,-20,-60,0,20); face(H,mouth=('grin','O','grin','o')[int(t*5+ph)%4])
        else: rest(H,t); face(H,mouth='smile'); H['head'].rotation_euler[2]=R(15)*math.sin(t*.7+ph)
def movers(paths,seed=0):
    """vehicles driving along polylines: [(kind,col,pts,speed,t0)]"""
    V=[]
    for kind,col,pts,sp,t0 in paths:
        o=rickshaw(0,0,0,col) if kind=='r' else (bike(0,0,0,col) if kind=='b' else truck_load(0,0,0)); V.append((o,pts,sp,t0))
    return V
def movers_upd(V,t):
    for o,pts,sp,t0 in V:
        Lp=path_len(pts); d=((t-t0)*sp)%Lp if Lp>0 else 0; p,hdg=path_pos(pts,d); o.location=(p[0],p[1],0); o.rotation_euler[2]=R(hdg-90)
def ring_path(r,n=24,a0=0): return [(r*math.cos(a0+2*pi*k/n),r*math.sin(a0+2*pi*k/n)) for k in range(n+1)]
# ============================================================ HOOK
def SH_aerial():
    plaza(); B.done('pl'); S_,w,rp,bg=setup_render('golden',res=PCT,samples=SAMPLES,shadow_dist=200); w.mist_settings.start=60; w.mist_settings.depth=260
    V=movers([('r','#2E8B5A',ring_path(11.0),4.0,0),('r','#E8C25A',ring_path(11.6,a0=2),4.2,0),('b','#C9302C',ring_path(12.2,a0=4),6,0),('t','',ring_path(10.6,a0=1),3.5,0),('b','#2F4E8C',ring_path(11.3,a0=3.2),5.5,0)])
    G=strollers([([(-14,-15),(-12,-12)],0,9),([(15,14),(13,12)],0,9),([(14,-16),(12,-13.5)],0,9),([(-15,13),(-13,11)],0,9)],1)
    def upd(t):
        movers_upd(V,t); strollers_upd(G,t); q=t/DUR; e=ease_out(q)
        a=R(L(-40,-8,ease(q))); rr=L(120,26,e); camset((rr*math.sin(a),-rr*math.cos(a),L(95,14,e)),(0,0,L(0,11,ease(q))),L(24,26,q),8.0)
    return dict(upd=upd)
SHOTS['H_aerial']=SH_aerial
def lane_scene(seed=21,stall=True,n_idle=6,mood='golden',walkers=True):
    if stall: stall_set()
    else: bazaar_lane(40,seed=seed)
    B.done('lane'); S_,w,rp,bg=setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=60)
    r=random.Random(seed)
    I=idlers([(r.uniform(-30,30),r.choice((-3.2,3.2)),r.choice((0,180,90,-90)),r.choice(('talk','phone','idle','sell'))) for i in range(n_idle)],seed)
    I=[H for H in I if abs(H['xy'][0])>4]
    G=strollers([([(-30+i*8,(-3.4,2.9)[i%2]),(-30+i*8+14,(-3.4,2.9)[i%2])],-2,20) for i in range(6)],seed) if walkers else []
    V=movers([('b','#C9302C',[(-40,.6),(40,.6)],4.5,0),('r','#2E8B5A',[(40,-.6),(-40,-.6)],3.2,-3)])
    def base(t): idlers_upd(I,t); strollers_upd(G,t); movers_upd(V,t)
    return base
def SH_cloth():
    base=lane_scene(31,stall=False,n_idle=0,walkers=False)
    sel=person((4.0,2.6,0),0,local(51),'grin',name='sel'); buy=person((4.0,1.2,0),180,local(52,female=True),'smile',name='buy'); bolt=obox((0,0,0),(.05,.5,.35),M(FAB[2],.8,kind='fabric'),.02)
    def upd(t):
        base(t); standH(sel,4.0,2.6,0,t); standH(buy,4.0,1.2,180,t); blink(sel,t); blink(buy,t)
        k=ease(t/.5); arms(sel,-80*k,0,-20,-80*k,0,20); p1=hand_w(sel,1); p2=hand_w(sel,-1); bolt.location=((p1.x+p2.x)/2,(p1.y+p2.y)/2-.05,(p1.z+p2.z)/2+.1); bolt.rotation_euler=(0,0,R(90))
        face(sel,mouth=('grin','O','grin','o')[int(t*6)%4]); arms(buy,-20,0,6,-40,0,-10); face(buy,mouth='smile'); nod(buy,t,4,4)
        q=ease(t/DUR); camset((L(1.6,2.0,q),L(-1.8,-1.4,q),1.7),(4.0,1.9,1.75),30,3.5,focus=(4.0,1.9,1.8))
    return dict(upd=upd)
SHOTS['H_cloth']=SH_cloth
def SH_mill():
    L_=mill(); B.done('mill'); W_=idlers([(-8.6,-.5,0,'idle'),(5.0,-.5,0,'idle'),(-5.0,2.7,0,'idle'),(8.7,5.9,0,'idle')],3)
    def upd(t):
        loom_run(L_,t); idlers_upd(W_,t); q=t/DUR; camset((L(-12,-9,q),-8.5,3.2),(L(-4,0,q),3,1.2),22,6.0)
    return dict(upd=upd)
SHOTS['H_mill']=SH_mill
def SH_shops():
    base=lane_scene(41,stall=False,n_idle=0,walkers=False)
    sk=person((-2.5,3.1,0),0,local(61),'grin',name='sk'); sk2=person((1.8,-3.1,0),180,local(62),'grin',name='sk2'); cu=person((-1.5,1.9,0),160,design(64),'smile',name='cu')
    def upd(t):
        base(t)
        for H,(x,y,rz) in ((sk,(-2.5,3.1,0)),(sk2,(1.8,-3.1,180)),(cu,(-1.5,1.9,160))): standH(H,x,y,rz,t); blink(H,t)
        arms(sk,-70,0,-25+10*math.sin(t*5),-30,0,8); face(sk,mouth=('grin','O','o','grin')[int(t*6)%4]); arms(sk2,-150,0,-30,-10,0,5); face(sk2,mouth='O'); arms(cu,-15,0,5,-15,0,-5); look_at(cu,(-2.5,3.1,2.0))
        q=ease(t/DUR); camset((L(-3.4,-3.0,q),L(-1.9,-1.6,q),1.95),(-2.1,2.4,1.75),28,4.0,focus=(-2.1,2.5,1.85))
    return dict(upd=upd)
SHOTS['H_shops']=SH_shops
def SH_ceo():
    base=lane_scene(51,stall=False,n_idle=4); Sz=person((0,-12,0),180,SHAHZAIB,'smirk',name='shahzaib'); gl=sunglasses(Sz)
    def upd(t):
        base(t); blink(Sz,t); walk_path(Sz,[(-9.5,-.6),(-1.0,-.4)],t,-.2,DUR+.2,step=.6,arm=28,ease_in=.0,ease_out_=.0); Sz['root'].rotation_euler[2]=R(-90)
        face(Sz,mouth='smirk',brow=.02,brow_r=-8); Sz['head'].rotation_euler[2]=R(-22)
        a=wl(28,'H_ceo')
        if t>a: k=ease((t-a)/.35); Sz['arm'][1].rotation_euler=(R(-25*k),R(0),R(-58*k)); Sz['arm'][-1].rotation_euler=(R(-25*k),0,R(58*k))
        x=Sz['root'].location[0]; q=ease(t/DUR); camset((x+L(4.2,3.4,q),-2.3,1.75),(x,-.4,1.75),28,4.0,focus=(x,-.4,1.8))
    return dict(upd=upd)
SHOTS['H_ceo']=SH_ceo
def SH_welcome():
    plaza(); B.done('pl'); setup_render('golden',res=PCT,samples=SAMPLES,shadow_dist=120)
    V=movers([('r','#2E8B5A',ring_path(11.0),4.0,0),('b','#C9302C',ring_path(12.2,a0=4),6,0),('r','#C6453A',ring_path(11.6,a0=2.6),4.4,0)])
    G=strollers([([(-8,-11),(8,-11.5)],-2,12),([(9,-10),(-6,-12)],-2,12)],2)
    sparkles((0,-2.5,12),3,0,3,n=20,size=.08,seed=4,rise=.5)
    def upd(t):
        movers_upd(V,t); strollers_upd(G,t); q=ease(t/DUR); _camset((L(-2.6,-2.0,q),L(-17.5,-16.0,q),1.4),(0,0,L(9,11.5,q)),L(20,22,q),8.0)
    return dict(upd=upd)
SHOTS['H_welcome']=SH_welcome
# ============================================================ PLAZA (scene 1, 2, 7)
BX=(0,-6.3)
def plaza_scene(dusk=False,sz_stand=True,dhaba_on=False,n_idle=6):
    plaza(night=dusk,with_dhaba=True); B.done('pl')
    S_,w,rp,bg=setup_render('sunset' if dusk else 'golden',res=PCT,samples=SAMPLES,shadow_dist=60)
    if dusk:
        for k in range(4): an=2*pi*k/4+pi/4; point((9.45*math.cos(an),9.45*math.sin(an),4.0),220,(1,.72,.42),.3,shadow=False)
        point((8.5,-11.5,2.4),60,(1,.7,.42),.3,shadow=False)
    S={}
    S['sz']=person((0,-7.6,0),180,SHAHZAIB,'smile',name='shahzaib'); S['pp']=person((.75,-6.3,0),0,PAPPU,'smile',name='pappu'); S['nm']=person((-.75,-6.3,0),0,NOMI,'smile',name='nomi')
    S['ch']=person((8.9,-10.9,0),-45,CHAIWALA,'smile',name='chaiwala')
    S['I']=idlers([(-6.5,-10.5,40,'talk'),(-5.8,-11.3,-140,'talk'),(5.2,-12.6,200,'phone'),(-9.5,-6.2,90,'idle'),(10.4,-9.9,-50,'idle')][:n_idle],4)
    S['V']=movers([('r','#2E8B5A',ring_path(11.0),4.0,0),('r','#E8C25A',ring_path(11.6,a0=2),4.2,0),('b','#C9302C',ring_path(12.2,a0=4),6,0),('b','#2F4E8C',ring_path(11.3,a0=3.2),5.5,0)])
    S['G']=strollers([([(-14,-12.5),(14,-13.0)],-4,20),([(13,-14),(-13,-13.6)],-8,20),([(-12,-9.4),(-3,-9.6)],-2,14)],3)
    return S
def plaza_base(S,t,sz='stand',sit_all=False):
    idlers_upd(S['I'],t); movers_upd(S['V'],t); strollers_upd(S['G'],t)
    for k,x in (('nm',-.75),('pp',.75)): seatH(S[k],x,-6.3,0); blink(S[k],t); rest(S[k],t); breathe(S[k],t)
    if sit_all: seatH(S['sz'],0,-6.3,0); blink(S['sz'],t); rest(S['sz'],t); breathe(S['sz'],t)
    elif sz=='stand': standH(S['sz'],0,-7.6,180,t); blink(S['sz'],t)
    ch=S['ch']; standH(ch,8.9,-10.9,-45,t); blink(ch,t); arms(ch,-55,0,-10,-30,0,8); face(ch,mouth='flat')
# camera helpers for plaza: friends sit facing -y at y=-6.3; Shahzaib stands at y=-7.6 facing +y
def cam_sz(t,q,lens=40,dx=0.0): h=headpos(S_['sz']) if False else None
def SH_plaza(view):
    KEY='I_'+view; sit_all=False
    S=plaza_scene(); sz,pp,nm=S['sz'],S['pp'],S['nm']; sz['camdz']=.32
    def upd(t):
        plaza_base(S,t,sz='walk' if view=='jump' else 'stand')
        hz=headpos(sz); hn=headpos(nm); hp=headpos(pp); q=ease(t/DUR)
        if view=='jump':
            a=wl(39,KEY); k=ease((t-a+.2)/.45); seatH(sz,0,-6.3,0,k=1-k) if k<1 else None
            if k<1: sz['root'].location[2]+=.0
            if k>=1:
                k2=ease((t-a-.25)/.5); sz['root'].location[0]=0; sz['root'].location[1]=L(-6.3,-7.6,k2); legs0(sz); stand(sz,t); sz['root'].rotation_euler[2]=R(L(0,180,ease((t-a-.35)/.4)))
                sz['root'].location[2]+=.35*math.sin(pi*min(1,max(0,(t-a)/.35)))*(1 if t-a<.35 else 0)
            seatH(sz,0,-6.3,0,k=1-k) if k<1 else None; blink(sz,t); arms(sz,-30*k,0,10,-30*k,0,-10); face(sz,mouth='grin',brow=.05,eyes=1.15)
            look_at(nm,(sz['root'].location[0],sz['root'].location[1],1.9),ease((t-a)/.3)); look_at(pp,(sz['root'].location[0],sz['root'].location[1],1.9),ease((t-a)/.3))
            camset((L(2.6,2.2,q),L(-10.6,-10.3,q),1.8),(0,-6.8,1.55),30,4.0,focus=(0,-6.9,1.6))
            return
        look_at(nm,hz); look_at(pp,hz)
        if view=='boys':
            talk(sz,t,41,46,KEY,rest='grin'); k=ease(t/.3); arms(sz,-150*k-8*math.sin(t*8)*k,0,-30*k,-80*k,0,25*k); face(sz,brow=.05,eyes=1.15); nod(sz,t,4,5)
            face(nm,mouth='flat',brow=-.01); face(pp,mouth='grin')
            cam_head(sz,(L(.9,.7,q),L(2.6,2.0,q),-.15),lens=40)
        elif view=='paise':
            talk(nm,t,47,48,KEY,rest='flat'); face(nm,brow=.02,brow_r=8); arms(nm,-30,0,8,-30,0,-8); face(sz,mouth='smile'); face(pp,mouth='smile')
            cam_head(nm,(L(-.9,-.7,q),L(-2.3,-1.8,q),.12),lens=42)
        elif view=='nahi':
            talk(sz,t,49,49,KEY,rest='grin',shapes=('o','grin')); SHRUG(sz,ease(t/.3)); face(sz,brow=.03); nod(sz,t,6,6)
            cam_head(sz,(L(.8,.6,q),L(2.4,1.9,q),-.15),lens=42)
        elif view=='exp':
            talk(pp,t,50,50,KEY,rest='o'); talk(sz,t,51,51,KEY,rest='grin',shapes=('o','grin')); face(pp,brow=.03,brow_r=8); arms(pp,-50,0,-20,-30,0,8)
            if t>wl(51,KEY): SHRUG(sz,ease((t-wl(51,KEY))/.25))
            cam_head(pp,(1,-1,0),lens=40)
        elif view=='toh':
            talk(nm,t,52,55,KEY,rest='flat'); arms(nm,-55,0,-40,-55,0,40); face(nm,brow=.03,brow_r=10,eyes=.85); nod(nm,t,-4,3)
            cam_head(nm,(L(-.8,-.6,q),L(-2.3,-1.8,q),.12),lens=44)
        elif view=='vision':
            k=ease(t/.25); talk(sz,t,56,56,KEY,rest='grin',shapes=('shout','O','shout')); arms(sz,-168*k,0,-22*k,-168*k,0,22*k); face(sz,brow=.07,eyes=1.25); sz['head'].rotation_euler[0]=R(-14*k)
            sparkles((0,-7.6,2.6),.9,.05,1.0,n=18,size=.04,seed=7,rise=.4) if False else None
            face(nm,mouth='flat',eyes=.7); face(pp,mouth='O',eyes=1.2)
            cam_head(sz,(1,1,0),lens=L(30,36,q),ang=40)
        else:
            talk(pp,t,57,58,KEY,rest='grin'); k=ease(t/.3); arms(pp,-30*k,0,-120*k,-14,0,-5); face(pp,brow=.04,eyes=1.15); nod(pp,t,5,6)
            look_at(sz,hp); face(sz,mouth='grin'); face(nm,mouth='flat',brow=-.02)
            cam_head(pp,(L(.9,.7,q),L(-2.3,-1.9,q),.1),lens=42)
    return dict(upd=upd)
for v in ('jump','boys','paise','nahi','exp','toh','vision','ceo'): SHOTS['I_'+v]=(lambda v=v: SH_plaza(v))
def SH_clock(view):
    KEY='C_'+view; S=plaza_scene(); sz,pp,nm=S['sz'],S['pp'],S['nm']
    def upd(t):
        plaza_base(S,t,sit_all=True); hz=headpos(sz); hn=headpos(nm); hp=headpos(pp); q=ease(t/DUR)
        if view=='sit':
            for H in (sz,pp,nm): face(H,mouth='smile')
            look_at(nm,hz,.6); look_at(pp,hz,.6); sz['head'].rotation_euler[2]=R(20)*math.sin(t*.8)
            camset((L(-2.0,-1.0,q),L(-16,-14,q),L(1.3,1.5,q)),(0,-3,L(5.5,4.0,q)),L(22,24,q),8.0)
        elif view=='listen':
            look_at(nm,hz); look_at(pp,hz); talk(sz,t,68,80,KEY,rest='smirk'); k=ease(t/.3); b=math.sin(t*4)
            arms(sz,-60*k-12*b,0,-30,-40*k,0,14); face(sz,brow=.03,brow_r=-6); sz['head'].rotation_euler[2]=R(25*math.sin(t*1.3))
            if t>wl(73,KEY): arms(sz,-45,0,-125,-40,0,14); sz['head'].rotation_euler=(R(-10),0,R(-35))
            face(nm,mouth='flat'); face(pp,mouth='grin'); nod(pp,t,5,5)
            camset((L(-.2,0,q),L(-9.2,-8.6,q),1.6),(0,-6.3,1.55),30,4.5,focus=(0,-6.4,1.6))
        elif view=='kapray':
            look_at(sz,hn,.8); look_at(pp,hn,.6); talk(nm,t,81,84,KEY,rest='flat'); talk(sz,t,85,86,KEY,rest='smirk'); look_at(nm,hz)
            if t>wl(85,KEY): sz['arm'][1].rotation_euler=(R(-90),0,R(-30))
            cam_head(nm,(L(-.4,-.3,q),L(-2.1,-1.8,q),.1),lens=40,lead=(.4,0,0))
        elif view=='kiski':
            look_at(nm,hz); look_at(sz,hn); talk(nm,t,87,89,KEY,rest='flat'); face(nm,brow=.03,brow_r=10); arms(nm,-40,0,-10,-40,0,10)
            cam_head(nm,(L(-.6,-.4,q),L(-2.0,-1.7,q),.1),lens=42)
        elif view=='future':
            talk(sz,t,90,98,KEY,rest='smile'); k=ease((t-wl(94,KEY))/.5); sz['head'].rotation_euler=(R(-22*k),0,R(-10*k)); arms(sz,-150*k,0,-35*k,-14,0,5); face(sz,eyes=L(1,.7,k),brow=.04)
            look_at(nm,hz); look_at(pp,hz); face(nm,mouth='flat',eyes=.75)
            sparkles((-1.2,-6.6,3.0),.9,wl(94,KEY),DUR,n=16,size=.03,seed=3,rise=.3) if False else None
            cam_head(sz,(L(.3,.2,q),L(-2.0,-1.6,q),-.05),lens=40)
        elif view=='investor':
            talk(pp,t,99,107,KEY,rest='grin'); pp['head'].rotation_euler=(R(-14),0,R(15)); k=ease(t/.4); arms(pp,-20*k,0,-100*k,-20*k,0,100*k); face(pp,eyes=.55,brow=.05)
            look_at(nm,hp); face(nm,mouth='flat',brow=-.02,brow_r=8); face(sz,mouth='grin'); look_at(sz,hp)
            cam_head(pp,(L(.5,.4,q),L(-2.0,-1.7,q),.0),lens=40)
        else:
            talk(nm,t,108,119,KEY,rest='flat'); k=ease((t-wl(113,KEY))/.3); arm_reach(nm,1,(hn[0]-.04,hn[1]-.25,hn[2]+.05)) if k>0 else arms(nm,-30,0,8,-30,0,-8)
            nm['head'].rotation_euler=(R(10*k),0,R(-30*(1-k))); face(nm,eyes=.6,brow=-.02,brow_r=12)
            look_at(sz,hn); look_at(pp,hn); face(sz,mouth='o'); face(pp,mouth='o')
            cam_head(nm,(-1,-1,0),lens=40)
    return dict(upd=upd)
for v in ('sit','listen','kapray','kiski','future','investor','doctor'): SHOTS['C_'+v]=(lambda v=v: SH_clock(v))
# ============================================================ STALL (scene 3, 6)
SZP=(0,1.05,0); PPS=(-1.75,.9); NMP=(2.0,.55,-70); CUP=(0,-1.05,180)
def stall_scene(n_idle=6,cust=True,chacha=False):
    base=lane_scene(21,stall=True,n_idle=n_idle); S={'base':base}
    S['sz']=person((0,1.05,0),0,SHAHZAIB,'smile',name='shahzaib'); S['pp']=person((-1.75,.9,0),0,PAPPU,'smile',name='pappu'); S['nm']=person((2.0,.55,0),-70,NOMI,'smile',name='nomi')
    if cust: S['cu']=person((0,-1.05,0),180,CUST,'smile',name='cust')
    if chacha: S['jm']=person((0,-1.1,0),180,CHACHA,'flat',name='chacha')
    S['sh']=kurta_shirt((0,0,0),'#2F4E8C')
    S['sh'].scale=(0,0,0)
    return S
def stall_base(S,t):
    S['base'](t); sz,pp,nm=S['sz'],S['pp'],S['nm']
    standH(sz,0,1.05,0,t); blink(sz,t); seatH(pp,-1.75,.9,0,sh=.5); blink(pp,t); rest(pp,t); standH(nm,2.0,.55,-70,t); blink(nm,t); arms(nm,-62,0,-58,-62,0,58)
    if 'cu' in S: standH(S['cu'],0,-1.05,180,t); blink(S['cu'],t); rest(S['cu'],t)
def SH_stall(view):
    KEY='S_'+view
    if view=='borrow':
        base=lane_scene(21,stall=True,n_idle=4); sz=person((0,0,0),0,SHAHZAIB,'grin',name='shahzaib'); pile=[kurta_shirt((0,0,0),FAB[(i*5+1)%12]) for i in range(5)]
        ow=person((-7.2,3.05,0),0,local(88),'flat',name='owner')
        def upd(t):
            base(t); blink(sz,t); walk_path(sz,[(-7.2,2.0),(-4,1.3),(-.4,1.05)],t,.1,DUR-.3,step=.5,arm=0,ease_in=.15,ease_out_=.3); arms(sz,-80,0,-12,-80,0,12)
            p=(hand_w(sz,1)+hand_w(sz,-1))/2
            for i,s in enumerate(pile): s.location=(p.x,p.y-.08,p.z+.06+i*.045); s.rotation_euler=(R(90),0,sz['root'].rotation_euler[2]+R(4*i))
            face(sz,mouth='grin',brow=.03); standH(ow,-7.2,3.05,0,t); blink(ow,t); look_at(ow,headpos(sz)); arms(ow,-60,0,-55,-60,0,55); face(ow,mouth='flat',brow=-.02,brow_r=10)
            x=sz['root'].location[0]; q=ease(t/DUR); camset((x+2.6,-3.6,1.9),(x-.6,1.2,1.4),26,4.5,focus=(x,1.3,1.5))
        return dict(upd=upd)
    S=stall_scene(cust=view not in ('stall',)); sz,pp,nm=S['sz'],S['pp'],S['nm']; cu=S.get('cu')
    def upd(t):
        stall_base(S,t); hz=headpos(sz); q=ease(t/DUR)
        hc=headpos(cu) if cu else (0,-1,1.9)
        look_at(pp,hc if cu else hz,.8); look_at(nm,hc if cu else hz,.6)
        if view=='stall':
            arms(sz,-60,0,-40,-60,0,40); face(sz,mouth='grin',brow=.03); face(pp,mouth='grin'); sz['head'].rotation_euler[2]=R(20*math.sin(t))
            camset((L(-1.5,-.5,q),L(-6.2,-5.4,q),L(2.4,2.1,q)),(0,.6,1.45),26,5.0,focus=(0,.6,1.5))
        elif view=='cust':
            walk_path(cu,[(6.5,-1.9),(2.4,-1.4),(0,-1.05)],t,-.3,DUR-.1,step=.52,arm=20,ease_in=.0,ease_out_=.3); blink(cu,t); face(cu,mouth='smile')
            look_at(sz,headpos(cu)); face(sz,mouth='grin',brow=.04); arms(sz,-55,0,-35,-55,0,35)
            camset((L(-2.6,-2.3,q),L(-3.2,-3.6,q),1.85),(L(1.6,.3,q),-.3,1.6),28,4.0,focus=(cu['root'].location[0],cu['root'].location[1],1.7))
        elif view=='kitne':
            talk(cu,t,137,140,KEY,rest='flat'); arm_reach(cu,1,(.3,.35,1.0)); look_at(cu,(.3,.35,.95),.6); look_at(sz,hc)
            cam_head(cu,(1,1,0),lens=40)
        elif view=='price':
            talk(sz,t,141,144,KEY,rest='grin'); k=ease(t/.3); arms(sz,-150*k,0,-24,-150*k,0,24); look_at(sz,hc,.6); face(sz,brow=.05,eyes=1.15)
            p1=hand_w(sz,1); p2=hand_w(sz,-1); S['sh'].scale=(1.2,1.2,1.2); S['sh'].location=((p1.x+p2.x)/2,(p1.y+p2.y)/2-.08,(p1.z+p2.z)/2-.25); S['sh'].rotation_euler=(0,0,0)
            cam_head(sz,(1,-1,0),lens=40)
        elif view=='market':
            talk(cu,t,145,151,KEY,rest='smirk'); arms(cu,-62,0,-58,-62,0,58); face(cu,brow=-.01,brow_r=8); look_at(sz,hc)
            cam_head(cu,(-1,1,0),lens=40)
        elif view=='bclass':
            talk(sz,t,152,160,KEY,rest='smirk'); k=ease(t/.3); sz['arm'][1].rotation_euler=(R(-95),0,R(-35+10*math.sin(t*5))); sz['arm'][-1].rotation_euler=(R(-20),0,R(5)); face(sz,brow=.03,brow_r=-10,eyes=.85); nod(sz,t,4,4)
            cam_head(sz,(1,-1,0),lens=40)
        elif view=='plane':
            talk(cu,t,161,165,KEY,rest='smirk',shapes=('O','o','grin','flat')); arms(cu,-20,0,-40,-115,0,-45+20*math.sin(t*3)); cu['head'].rotation_euler=(0,0,R(14*math.sin(t*2)))
            face(cu,brow=.04,brow_r=-6); look_at(sz,hc); face(sz,mouth='o')
            cam_head(cu,(-1,1,0),lens=40)
        elif view=='laugh':
            pp['root'].rotation_euler[0]=R(18+6*math.sin(t*14)); face(pp,mouth='grin',eyes=.1,brow=.05); arms(pp,-50,0,-10+10*math.sin(t*14),-60,0,10); pp['root'].location[2]+=.03*abs(math.sin(t*14))
            look_at(sz,headpos(pp),.8); face(sz,mouth='flat',brow=-.03,brow_r=14)
            camset((L(-3.4,-3.0,q),L(-1.8,-1.5,q),1.6),(-1.75,.9,1.25),32,3.0,focus=(-1.75,.9,1.3))
        elif view=='respect':
            talk(sz,t,170,174,KEY,rest='flat',shapes=('shout','O','shout','o')); look_at(sz,headpos(pp)); arm_to(sz,1,headpos(pp)); face(sz,brow=-.04,brow_r=18,eyes=1.2)
            pp['root'].rotation_euler[0]=R(4); face(pp,mouth='o',brow=.04); look_at(pp,hz)
            cam_head(sz,(-1,-1,0),lens=38)
        elif view=='away':
            walk_path(cu,[(0,-1.05),(.5,-2.2),(9,-2.6)],t,.1,DUR+1.5,step=.52,arm=18,ease_in=.25,ease_out_=0); blink(cu,t); face(cu,mouth='smirk')
            look_at(sz,headpos(cu)); arms(sz,-40,0,-30,-150,0,-30); face(sz,mouth='o',brow=.04); look_at(nm,headpos(cu))
            camset((L(-2.0,-2.2,q),L(-3.6,-3.8,q),1.9),(L(.6,2.2,q),-1.0,1.5),26,5.0,focus=(cu['root'].location[0],-1.5,1.6))
        elif view=='bhaag':
            talk(nm,t,179,183,KEY,rest='flat'); look_at(nm,hz); face(nm,brow=-.02,brow_r=10,eyes=.75); nod(nm,t,-3,2)
            cam_head(nm,(L(-.6,-.5,q),L(-2.1,-1.8,q),.05),lens=40)
        else:
            talk(sz,t,184,188,KEY,rest='smirk'); look_at(sz,headpos(nm)); arms(sz,-62,0,-58,-62,0,58); face(sz,brow=.03,brow_r=-12,eyes=.8); sz['head'].rotation_euler[0]=R(-6)
            cam_head(sz,(1,-1,0),lens=40)
    return dict(upd=upd)
for v in ('borrow','stall','cust','kitne','price','market','bclass','plane','laugh','respect','away','bhaag','comp'): SHOTS['S_'+v]=(lambda v=v: SH_stall(v))
# ============================================================ MILL (scene 4)
JM=(0,-5.3); BOYS={'sz':(0,-7.6,180),'pp':(-1.05,-7.75,168),'nm':(1.05,-7.8,192)}
def SH_factory(view):
    KEY='F_'+view; L_=mill(); B.done('mill'); W_=idlers([(-8.6,-.5,0,'idle'),(5.0,-.5,0,'idle'),(-5.0,2.7,0,'idle'),(8.7,5.9,0,'idle'),(-1.8,4.0,0,'idle')],3)
    jm=person((0,-5.3,0),0,CHACHA,'flat',name='chacha'); sz=person((0,-7.6,0),180,SHAHZAIB,'smile',name='shahzaib'); pp=person((-1.05,-7.75,0),168,PAPPU,'smile',name='pappu'); nm=person((1.05,-7.8,0),192,NOMI,'smile',name='nomi')
    cart=obox((0,0,0),(.4,.3,.05),M('#3E6FB0',.5,metal=.4),.01)
    wk=person((-11,-2,0),0,local(97),'smile',name='wk')
    def base(t):
        loom_run(L_,t); idlers_upd(W_,t); standH(jm,0,-5.3,0,t); blink(jm,t)
        for k,H in (('sz',sz),('pp',pp),('nm',nm)): x,y,rz=BOYS[k]; standH(H,x,y,rz,t); blink(H,t); rest(H,t)
        walk_path(wk,[(-11,-2.5),(11,-2.5)],t,-3,10,step=.5,arm=0); arms(wk,-80,0,-10,-80,0,10); blink(wk,t); carry(cart,wk,1,(0,0,.05))
    def upd(t):
        base(t); hj=headpos(jm); hz=headpos(sz); q=ease(t/DUR)
        if view=='wide':
            for k,H in (('sz',sz),('pp',pp),('nm',nm)):
                x,y,rz=BOYS[k]; walk_path(H,[(x-9.8,y-.4),(x-3,y-.2),(x,y)],t,-.5,DUR-.3,step=.52,arm=22,ease_in=0,ease_out_=.3); look_at(H,(0,2,2.0),.6)
            arms(jm,-40,0,-20,-40,0,20); jm['head'].rotation_euler=(R(18),0,0)
            camset((L(-7,-5,q),L(-9.4,-9.5,q),3.4),(L(-3,-.5,q),-5.0,1.3),22,6.0)
        elif view=='looms':
            l=L_[2]; x=l['root'].location[0]; y=l['root'].location[1]; camset((x+L(1.5,1.0,q),y-2.0,1.65),(x,y,1.1),34,2.2,focus=(x,y-.1,1.15))
        elif view=='haan':
            talk(jm,t,203,207,KEY,rest='flat',rate=6); jm['head'].rotation_euler=(R(L(18,0,ease(t/.4))),0,0); arms(jm,-40,0,-20,-30,0,10); face(jm,brow=-.01,brow_r=6)
            for H in (sz,pp,nm): look_at(H,hj)
            cam_head(jm,(1,-1,0),lens=40)
        elif view=='brand':
            talk(sz,t,208,216,KEY,rest='grin'); k=ease(t/.3); arms(sz,-150*k,0,-25,-60*k,0,30); look_at(sz,hj); face(sz,brow=.05,eyes=1.15); look_at(jm,hz)
            look_at(pp,hz); look_at(nm,hz); face(pp,mouth='grin')
            cam_head(sz,(-1,1,0),lens=40)
        elif view=='invest':
            talk(jm,t,217,220,KEY,rest='flat',rate=6); look_at(jm,hz); arms(jm,-62,0,-58,-62,0,58); face(jm,brow=.02,brow_r=-6)
            for H in (sz,pp,nm): look_at(H,hj)
            cam_head(jm,(1,-1,0),lens=42)
        elif view=='ideas':
            talk(sz,t,221,228,KEY,rest='grin'); arms(sz,-45,0,-125,-14,0,5); look_at(sz,hj); face(sz,brow=.03,brow_r=-8,eyes=.9); nod(sz,t,4,4); look_at(jm,hz)
            cam_head(sz,(-1,1,0),lens=40)
        elif view=='stare':
            look_at(jm,hz); arms(jm,-62,0,-58,-62,0,58); face(jm,mouth='flat',brow=-.04,brow_r=18,eyes=.6); jm['head'].rotation_euler[0]=R(-4)
            cam_head(jm,(1,-1,0),lens=L(40,56,q))
        elif view=='beta':
            talk(jm,t,233,241,KEY,rest='flat',rate=6); look_at(jm,hz); k=math.sin(t*4); arms(jm,-90,0,-20+12*k,-30,0,8); face(jm,brow=-.02,brow_r=12); nod(jm,t,3,3)
            look_at(sz,hj); face(sz,mouth='flat',eyes=.8)
            cam_head(jm,(1,-1,0),lens=40)
        elif view=='partner':
            hp=headpos(pp); talk(pp,t,242,245,KEY,rest='grin'); k=ease(t/.3); arms(pp,-90*k,0,-10,-20,0,5); look_at(pp,hj); face(pp,brow=.04,eyes=1.1)
            look_at(jm,hp); look_at(sz,hp); look_at(nm,hp); face(nm,mouth='flat',brow=-.02,brow_r=10)
            cam_head(pp,(-1,1,0),lens=40)
        else:
            hp=headpos(pp); talk(jm,t,246,254,KEY,rest='flat',rate=6); look_at(jm,hp); arm_to(jm,1,hp); face(jm,brow=-.03,brow_r=14); nod(jm,t,3,3)
            look_at(pp,hj); face(pp,mouth='o',brow=.04); face(nm,mouth='grin'); face(sz,mouth='o')
            camset((L(1.5,1.3,q),L(-4.2,-4.4,q),2.45),(-.4,-7.7,1.55),26,4.5,focus=(-.6,-7.7,1.7))
    return dict(upd=upd)
for v in ('wide','looms','haan','brand','invest','ideas','stare','beta','partner','bill'): SHOTS['F_'+v]=(lambda v=v: SH_factory(v))
# ============================================================ PHONE (scene 5, bazaar lane away from the stall)
PZ={'sz':(-14,-.2,0),'pp':(-14.95,-1.0,0),'nm':(-13.05,-1.0,0)}
def SH_phone(view):
    KEY='P_'+view; base=lane_scene(61,stall=True,n_idle=5)
    sz=person((-14,-.2,0),0,SHAHZAIB,'smile',name='shahzaib'); pp=person((-14.95,-1.0,0),0,PAPPU,'smile',name='pappu'); nm=person((-13.05,-1.0,0),0,NOMI,'smile',name='nomi')
    ph=phone(sz,1,'#7FD3FF'); scr=obox((0,0,0),(.06,.002,.11),M('#F4F7FA',.4,emit=1.3),0); scr.scale=(0,0,0)
    bub=[obox((0,0,0),(w_,.001,.012),M(c,.4,emit=1.0),0) for w_,c in ((.045,'#2E8B5A'),(.035,'#2E8B5A'),(.05,'#9AA0A8'))]
    for b in bub: b.scale=(0,0,0)
    def base2(t):
        base(t)
        for k,H in (('sz',sz),('pp',pp),('nm',nm)): x,y,rz=PZ[k]; standH(H,x,y,rz,t); blink(H,t); rest(H,t)
        sz['root'].rotation_euler[2]=R(0); pp['root'].rotation_euler[2]=R(-60); nm['root'].rotation_euler[2]=R(60)
    def phone_ear(k=1.0): arm_reach(sz,1,(L(-13.75,-13.75,k),L(-.55,-.2,k),L(1.3,1.95,k))); ph.rotation_euler=(R(L(-80,0,k)),0,R(90*k))
    def upd(t):
        base2(t); hz=headpos(sz); q=ease(t/DUR); hp=headpos(pp); hn=headpos(nm)
        look_at(pp,hz); look_at(nm,hz)
        if view=='ring':
            k=ease((t-.6)/.4); phone_ear(k); sz['root'].location[2]+=.0; face(sz,mouth='o' if t<.6 else 'smile',brow=.03)
            vib=.006*math.sin(t*90)*(1 if t<.6 else 0); ph.location[0]+=vib
            camset((L(-14.3,-14.1,q),L(-2.2,-1.9,q),L(1.6,1.85,q)),(-13.8,-.4,L(1.4,1.85,q)),30,2.6,focus=(-13.8,-.4,1.6))
        elif view=='what':
            phone_ear(1); talk(sz,t,259,261,KEY,rest='O',shapes=('shout','O','shout','O')); face(sz,brow=.07,eyes=1.35); sz['root'].rotation_euler[0]=R(-6); sz['arm'][-1].rotation_euler=(R(-60),0,R(30))
            cam_head(sz,(L(.4,.3,q),L(-1.6,-1.2,q),-.05),lens=42)
        elif view=='jump':
            a=wl(262,KEY); hop=abs(math.sin(min(t,2.4)*6))*.35; sz['root'].location[2]+=hop; arms(sz,-170+10*math.sin(t*12),0,-22,-170+10*math.sin(t*12),0,22); carry(ph,sz,1,(0,0,.05)); ph.rotation_euler=(0,0,0)
            talk(sz,t,262,265,KEY,rest='grin',shapes=('shout','O','grin','shout')); face(sz,brow=.07,eyes=1.25)
            face(pp,mouth='O',eyes=1.2); face(nm,mouth='o',eyes=1.15)
            camset((L(-14.2,-14.1,q),L(-4.6,-4.9,q),L(1.5,1.6,q)),(-14,-.4,1.75),28,4.0,focus=(-14,-.5,1.8))
        elif view=='500':
            talk(pp,t,266,266,KEY,rest='O',shapes=('shout','O','shout')); k=ease(t/.2); arms(pp,-35*k,0,-140*k,-35*k,0,140*k); face(pp,brow=.07,eyes=1.35); pp['root'].location[2]+=.15*abs(math.sin(t*9))*k
            cam_head(pp,(L(-.9,-.7,q),L(-1.7,-1.4,q),.0),lens=40,lead=(.3,0,0))
        elif view=='kisne':
            talk(nm,t,267,268,KEY,rest='flat'); talk(sz,t,269,275,KEY,rest='grin'); look_at(sz,hn); carry(ph,sz,1,(0,0,.05)); ph.rotation_euler=(R(-70),0,0); arms(sz,-75,0,-20,-60,0,40)
            face(nm,brow=.02,brow_r=8); face(sz,brow=.04,eyes=1.1)
            cam_head(sz,(-1,-1,0),lens=38)
        elif view=='adv':
            for a,b,H,rest_ in ((276,277,nm,'flat'),(278,278,sz,'flat'),(279,279,nm,'flat'),(280,280,sz,'flat')): talk(H,t,a,b,KEY,rest=rest_) if wl(a,KEY)-.05<=t<we(b,KEY)+.3 else None
            look_at(sz,hn); look_at(nm,hz); k=ease((t-wl(278,KEY))/.2); arms(nm,-62,0,-58,-62,0,58); face(nm,brow=.02,brow_r=12,eyes=.85)
            arms(sz,-40,0,-50*k,-40,0,50*k); face(sz,eyes=L(1.1,.9,k),brow=.03)
            if t>wl(280,KEY): sz['head'].rotation_euler[0]=R(10)
            cam_head(nm,(1,-1,0),lens=38)
        elif view=='kahan':
            talk(nm,t,281,284,KEY,rest='flat'); arms(nm,-55,0,-40,-55,0,40); face(nm,brow=.03,brow_r=12); look_at(nm,hz)
            cam_head(nm,(L(.9,.7,q),L(-1.8,-1.5,q),.05),lens=40,lead=(-.3,0,0))
        elif view=='phone':
            a=wl(290,KEY); arm_reach(sz,1,(-13.85,-.75,1.65)); ph.rotation_euler=(R(-68),0,R(0)); look_at(sz,(-13.85,-.75,1.55)); face(sz,mouth='flat' if t<a else 'o',eyes=.9,brow=.02)
            insert=a-.6<t<we(294,KEY)+.9
            if insert:
                p=Vector(ph.location); scr.scale=(1,1,1); scr.location=(p.x,p.y-.022,p.z+.0); scr.rotation_euler=ph.rotation_euler
                for i,b in enumerate(bub): b.scale=(1,1,1); b.location=(p.x+(.02 if i<2 else -.015),p.y-.026,p.z+.07-i*.045+.0); b.rotation_euler=ph.rotation_euler
                _camset((p.x,p.y-L(.34,.3,q),p.z+.16),(p.x,p.y,p.z),40,1.6,focus=(p.x,p.y,p.z))
            else:
                scr.scale=(0,0,0)
                for b in bub: b.scale=(0,0,0)
                cam_head(sz,(-1,-1,0),lens=34)
            if t>we(294,KEY)+.2:
                for H in (sz,pp,nm): face(H,mouth='flat',eyes=.75,brow=-.01)
                look_at(nm,hz); look_at(pp,hz)
        else:
            talk(pp,t,295,301,KEY,rest='grin'); look_at(pp,hz); pp['arm'][1].rotation_euler=(R(-60),0,R(-70)); face(pp,brow=.04,brow_r=-8,eyes=.9); nod(pp,t,4,3)
            face(sz,mouth='flat',eyes=.8); face(nm,mouth='flat',eyes=.6,brow=-.02,brow_r=14); look_at(nm,hp)
            cam_head(pp,(L(-.9,-.7,q),L(-1.8,-1.5,q),.0),lens=40,lead=(.3,0,0))
    return dict(upd=upd)
for v in ('ring','what','jump','500','kisne','adv','kahan','phone','intl'): SHOTS['P_'+v]=(lambda v=v: SH_phone(v))
# ============================================================ REVEAL at the stall (scene 6)
def SH_reveal(view):
    KEY='R_'+view; S=stall_scene(cust=False,chacha=True); sz,pp,nm,jm=S['sz'],S['pp'],S['nm'],S['jm']
    def upd(t):
        stall_base(S,t); standH(jm,0,-1.1,180,t); blink(jm,t); CROSS(jm); hz=headpos(sz); hj=headpos(jm); hn=headpos(nm); hp=headpos(pp); q=ease(t/DUR)
        look_at(jm,hz); look_at(sz,hj); look_at(pp,hj,.7); look_at(nm,hj,.7); face(jm,mouth='flat',brow=-.02,brow_r=12)
        if view=='back':
            for k,H,(x,y,rz),pts in (('sz',sz,(0,1.05,0),[(6.5,2.0),(2.5,1.6),(0,1.05)]),('pp',pp,(0,0,0),[(7.6,2.6),(3.2,2.4),(-1.75,.9)]),('nm',nm,(2.0,.55,-70),[(8.6,1.4),(4.0,.9),(2.0,.55)])):
                walk_path(H,pts,t,.35,DUR+.4,step=.52,arm=22,ease_in=.1,ease_out_=.1)
            face(sz,mouth='o',brow=.04); face(pp,mouth='o'); face(nm,mouth='flat')
            camset((L(-3.2,-2.8,q),L(-4.4,-4.6,q),2.2),(L(.2,.8,q),-.2,1.45),26,5.0,focus=(0,-1.1,1.7))
        elif view=='kahan':
            talk(jm,t,310,314,KEY,rest='flat',rate=6,shapes=('shout','O','o','flat')); face(jm,brow=-.04,brow_r=16); arms(jm,-90,0,-20+10*math.sin(t*5),-62,0,58)
            cam_head(jm,(1,1,0),lens=40)
        elif view=='prod':
            talk(sz,t,315,320,KEY,rest='strain'); face(sz,brow=.05,brow_r=10,eyes=1.05); arms(sz,-55,0,-35+8*math.sin(t*6),-55,0,35); nod(sz,t,4,4)
            cam_head(sz,(L(.7,.6,q),L(-2.1,-1.8,q),-.05),lens=38)
        elif view=='noorder':
            talk(jm,t,321,331,KEY,rest='flat',rate=6,shapes=('shout','O','o','flat')); arm_to(jm,1,hz); jm['arm'][-1].rotation_euler=(R(-60),0,R(55)); face(jm,brow=-.05,brow_r=18,eyes=1.1); nod(jm,t,3,4)
            face(sz,mouth='strain',brow=.05,eyes=1.2)
            cam_head(jm,(-1,1,0),lens=40)
        elif view=='fake':
            k=ease(t/.4); nm['root'].rotation_euler[2]=R(L(-70,-100,k)); look_at(nm,hz); talk(nm,t,336,340,KEY,rest='flat'); face(nm,brow=.06,eyes=1.25); arms(nm,-40,0,-45,-40,0,45)
            cam_head(nm,(L(-1.3,-1.1,q),L(-1.6,-1.4,q),.05),lens=38,lead=(-.3,0,0))
        elif view=='pre':
            look_at(sz,hn); talk(sz,t,341,347,KEY,rest='strain'); sz['arm'][1].rotation_euler=(R(-80),0,R(-30)); face(sz,brow=.04,brow_r=-8,eyes=.95); look_at(nm,hz); face(nm,mouth='flat',brow=-.03,brow_r=14)
            cam_head(sz,(L(-.5,-.4,q),L(-2.0,-1.8,q),-.05),lens=40)
        elif view=='startup':
            talk(pp,t,351,353,KEY,rest='smirk'); a=wl(348,KEY); nod(pp,t,9 if t<wl(351,KEY) else 4,5); arms(pp,-62,0,-58,-62,0,58); face(pp,brow=.02,brow_r=-10,eyes=.8); look_at(pp,hj,.7)
            cam_head(pp,(L(.8,.6,q),L(-1.8,-1.5,q),.12),lens=38)
        else:
            talk(jm,t,354,371,KEY,rest='flat',rate=6); face(jm,brow=-.01,brow_r=8,eyes=.9); k=math.sin(t*2.5); arms(jm,-95,0,-25+10*k,-62,0,58); jm['head'].rotation_euler[2]=R(-20+35*math.sin(t*.6))
            for H in (sz,pp,nm): face(H,mouth='flat',eyes=.75); H['head'].rotation_euler[0]=R(12)
            cam_head(jm,(1,1,0),lens=34,ang=40)
    return dict(upd=upd)
for v in ('back','kahan','prod','noorder','fake','pre','startup','asli'): SHOTS['R_'+v]=(lambda v=v: SH_reveal(v))
# ============================================================ DUSK at the clock tower (scene 7 + ending)
def SH_dusk(view):
    KEY='Z_'+view; S=plaza_scene(dusk=True); sz,pp,nm,ch=S['sz'],S['pp'],S['nm'],S['ch']
    cups=[cup((0,0,0)) for i in range(3)]
    for c_ in cups: c_.scale=(0,0,0)
    plan=obox((0,0,0),(.18,.003,.24),M('#F4F1EA',.6),.005); plan.scale=(0,0,0)
    for j in range(6): obox((0,-.004,.18-j*.07),(.13 if j%2 else .1,.001,.008),M('#2F4E8C',.6),0,plan)
    obox((.06,-.004,-.17),(.05,.001,.03),M('#C6453A',.5),0,plan)
    def upd(t):
        plaza_base(S,t,sit_all=True); hz=headpos(sz); hn=headpos(nm); hp=headpos(pp); hc=headpos(ch); q=ease(t/DUR)
        for H in (sz,pp,nm): face(H,mouth='flat',eyes=.8)
        if view in ('sit','ab','band','paise','partner'):
            for i,H in enumerate((nm,sz,pp)):
                c_=cups[i]; c_.scale=(1,1,1); p=hand_w(H,-1 if i==0 else 1); c_.location=(p.x,p.y-.04,p.z+.02)
        if view=='sit':
            for H in (sz,pp,nm): H['root'].rotation_euler[0]=R(10); H['head'].rotation_euler[0]=R(16)
            arms(sz,-40,0,-10,-40,0,10); arms(pp,-50,0,-10,-50,0,10); arms(nm,-45,0,-10,-45,0,10)
            camset((L(1.6,.6,q),L(-15.5,-13.5,q),L(1.6,1.5,q)),(0,-5,L(4,2.8,q)),L(22,26,q),6.0)
        elif view=='ab':
            talk(pp,t,380,382,KEY,rest='flat'); look_at(pp,hz); face(pp,brow=.03,brow_r=10,eyes=.9); arms(pp,-50,0,-10,-50,0,10)
            cam_head(pp,(L(.6,.5,q),L(-1.9,-1.6,q),.05),lens=40)
        elif view=='band':
            talk(sz,t,383,386,KEY,rest='flat',shapes=('shout','O','o','flat')); k=ease(t/.25); arms(sz,-40,0,-10,-120*k,0,-20); face(sz,brow=-.02,brow_r=-8,eyes=1.1); look_at(sz,hp)
            cam_head(sz,(L(.4,.3,q),L(-1.9,-1.6,q),-.05),lens=40)
        elif view=='paise':
            talk(nm,t,387,389,KEY,rest='flat',shapes=('shout','O','o')); look_at(nm,hz); face(nm,brow=-.03,brow_r=16,eyes=1.15); arms(nm,-40,0,-10,-100,0,40)
            cam_head(nm,(L(-.5,-.4,q),L(-1.9,-1.6,q),.05),lens=40)
        elif view=='partner':
            talk(sz,t,390,393,KEY,rest='smirk'); talk(pp,t,394,396,KEY,rest='o'); look_at(sz,hp); look_at(pp,hz); look_at(nm,hz); face(sz,brow=.02,brow_r=-12,eyes=.8)
            camset((L(-.3,-.1,q),L(-9.0,-8.7,q),1.55),(.3,-6.3,1.55),30,4.5,focus=(.3,-6.3,1.6))
        elif view=='point':
            k=ease(t/.4); arm_to(sz,1,hc); sz['root'].rotation_euler[2]=R(-20*k); look_at(sz,hc); face(sz,mouth='grin',brow=.05,eyes=1.15)
            look_at(pp,hc,ease((t-.3)/.4)); look_at(nm,hc,ease((t-.4)/.4))
            camset((L(-2.3,-2.0,q),L(-4.7,-4.5,q),2.5),(5.5,-10.5,1.4),24,5.0,focus=(0,-6.4,1.6))
        elif view=='chai':
            talk(sz,t,403,404,KEY,rest='grin',shapes=('shout','O','grin')); arm_to(sz,1,hc); look_at(sz,hc); face(sz,brow=.06,eyes=1.25); sz['root'].location[2]+=.06*abs(math.sin(t*8))
            look_at(pp,hc); look_at(nm,hz); face(pp,mouth='grin'); face(nm,mouth='flat',eyes=.6)
            cam_head(sz,(L(-.7,-.5,q),L(-1.9,-1.6,q),0),lens=36,lead=(.4,0,0))
        elif view=='over':
            k=ease((t-.3)/.4); ch['head'].rotation_euler=(0,0,R(0)); look_at(ch,hz,k); arms(ch,-55*(1-k),0,-10,-30,0,8); ch['root'].rotation_euler[2]=R(L(-45,-60,k)); face(ch,mouth='flat',brow=-.02,brow_r=12)
            cam_head(ch,(-1,1,0),lens=40,ang=34)
        elif view=='paise2':
            ch['root'].rotation_euler[2]=R(-60); look_at(ch,hz); talk(ch,t,410,417,KEY,rest='flat',rate=6); arms(ch,-30,0,8,-95,0,40-15*math.sin(t*4)); face(ch,brow=-.02,brow_r=14)
            for H in (sz,pp,nm): look_at(H,hc); face(H,mouth='o',eyes=1.1)
            cam_head(ch,(-1,1,0),lens=40,ang=40)
        elif view=='look':
            a=0.0; b=wl(418,KEY)
            for i,H in enumerate((sz,pp,nm)):
                tg=(hn if H is not nm else hz) if (t+i*.25)%1.4<.7 else (hp if H is not pp else hz)
                look_at(H,tg,ease((t-i*.1)/.25)); face(H,mouth='flat',eyes=1.15)
            talk(nm,t,418,427,KEY,rest='flat',rate=6);
            if t>b: face(nm,eyes=.6,brow=-.02,brow_r=12); look_at(nm,hz)
            camset((L(-.4,-.2,q),L(-9.0,-8.7,q),1.55),(0,-6.3,1.5),30,4.5,focus=(0,-6.35,1.55))
        elif view=='city':
            q2=t/DUR; a=R(L(-30,25,ease(q2))); rr=L(60,48,q2); camset((rr*math.sin(a),-rr*math.cos(a),L(30,22,q2)),(0,0,L(6,9,q2)),L(26,24,q2),8.0)
        elif view=='plans':
            plan.scale=(1,1,1); arm_reach(sz,1,(0,-6.75,1.45)); arm_reach(sz,-1,(0,-6.75,1.45)); p=(hand_w(sz,1)+hand_w(sz,-1))/2; plan.location=(p.x,p.y-.03,p.z+.12); plan.rotation_euler=(R(-20),0,0)
            look_at(sz,(p.x,p.y,p.z+.1)); face(sz,mouth='smirk',brow=.03); look_at(pp,(p.x,p.y,p.z+.1)); look_at(nm,(p.x,p.y,p.z+.1)); face(pp,mouth='grin'); face(nm,mouth='flat',brow=-.02)
            camset((L(.8,.5,q),L(-8.6,-8.2,q),1.75),(0,-6.4,1.45),30,4.0,focus=(0,-6.5,1.5))
        elif view=='kal':
            talk(sz,t,446,450,KEY,rest='grin'); k=ease(t/.3); arms(sz,-150*k,0,-25*k,-150*k,0,25*k); face(sz,brow=.05,eyes=1.15); look_at(sz,hp,.6)
            sz['root'].location[2]+=.0; look_at(pp,hz); look_at(nm,hz); face(pp,mouth='grin'); face(nm,mouth='flat',eyes=.7)
            cam_head(sz,(L(.4,.3,q),L(-1.9,-1.6,q),-.05),lens=38)
        elif view=='meet':
            talk(pp,t,451,452,KEY,rest='grin'); k=ease(t/.3); arms(pp,-62,0,-58,-62,0,58); pp['arm'][1].rotation_euler[2]=R(-58+30*k); face(pp,brow=.04,brow_r=-8); look_at(pp,hz)
            cam_head(pp,(L(.5,.4,q),L(-1.9,-1.6,q),.05),lens=38)
        else:
            talk(nm,t,453,458,KEY,rest='flat'); look_at(nm,(0,-9,1.6),ease((t-wl(457,KEY))/.3)*.0+.0); look_at(nm,hz); face(nm,brow=-.02,brow_r=10,eyes=.75)
            k=ease((t-we(458,KEY)-.1)/.4);
            if k>0: look_at(nm,(0,-12,1.6),k); face(nm,mouth='smirk',eyes=.8)
            face(sz,mouth='o',eyes=1.1); face(pp,mouth='o',eyes=1.1); look_at(sz,hn); look_at(pp,hn)
            camset((L(-.2,0,q),L(-8.9,-9.6,q),L(1.55,1.65,q)),(0,-6.3,L(1.5,1.7,q)),L(30,26,q),4.5,focus=(0,-6.35,1.55))
    return dict(upd=upd)
for v in ('sit','ab','band','paise','partner','point','chai','over','paise2','look','city','plans','kal','meet','kaam'): SHOTS['Z_'+v]=(lambda v=v: SH_dusk(v))
