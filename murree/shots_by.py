SHOTS={}
WJ=json.load(open('/home/claude/murree/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('M_hook', 0), ('M_plan', 12), ('M_six', 23), ('M_bilal', 30), ('M_kis', 38), ('M_toll', 43), ('M_donkey', 52), ('M_overtake', 66), ('M_hour', 71), ('M_chai', 78), ('M_family', 89), ('M_biryani', 104), ('N_bhutta1', 117), ('N_bhutta2', 129), ('N_snow', 136), ('N_fridge', 147), ('N_stuck', 153), ('N_push', 161), ('N_chain', 175), ('O_rates', 187), ('O_fog', 205), ('O_premium', 212), ('L_selfie', 218), ('L_call', 234), ('L_proud', 242), ('R_ammi', 249), ('Q_photo', 257), ('R_snowman', 268), ('L_shock', 281), ('L_dhund', 290), ('Z_cta', 300)]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.1,3)) for k,i in _K]
END=round(WE[-1]+2.0,3)
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
def cam_head(H,off,lens=40,fs=2.8,dz=0.0,lead=(0,0,0),q=None,ang=26,dist=3.3):
    h=headpos(H); rz=H['root'].rotation_euler[2]; key=H['root'].name+'%.0f%.0f'%(off[0],off[1])
    if key not in CAMLOCK:
        bpy.context.view_layer.update(); best=None
        sides=[]
        for sg in (1,-1):
            f=(math.sin(rz+sg*R(ang)),-math.cos(rz+sg*R(ang))); sides.append((f[0]*off[0]+f[1]*off[1],sg))
        sides.sort(reverse=True); order=[]
        for a in (ang,ang+14,max(0,ang-14),ang+28,ang+42,0):
            for _,sg in sides: order.append(sg*a)
        order+=[sg*a for a in (60,75,90) for _,sg in sides]
        for dzz in (0.0,.35,.7,1.05):
            for a in order:
                for ds in (dist,dist*.8):
                    f=(math.sin(rz+R(a)),-math.cos(rz+R(a))); c=(h[0]+f[0]*ds,h[1]+f[1]*ds,h[2]+H.get('camdz',.08)+dz+dzz)
                    if _clear_view(H,c): best=(a,ds,dzz); break
                if best: break
            if best: break
        CAMLOCK[key]=best or (ang*sides[0][1],dist*.75,.3)
    a,ds,dzz=CAMLOCK[key]; f=(math.sin(rz+R(a)),-math.cos(rz+R(a)))
    _camset((h[0]+f[0]*ds,h[1]+f[1]*ds,h[2]+H.get('camdz',.08)+dz+dzz),(h[0]+lead[0]*.3,h[1]+lead[1]*.3,h[2]-.22),lens*.82*ds/3.0,fs,focus=h)
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

# ============================================================ helpers for "Murree — Sab Ek Hi Din"
OWNER=[None]
def body_vis(H,on):
    if '_body' not in H: H['_body']=[o for o in [H['root']]+list(H['root'].children_recursive) if o.type=='MESH']
    for o in H['_body']: o.hide_render=not on
def phone_in_hand(H,ph,up=2.0,face_dist=.55,raise_=0.0):
    h=Vector(headpos(H)); M3=root_mat(H).to_3x3(); f=M3@Vector((0,-1,0)); rt=M3@Vector((1,0,0)); p=h+f*face_dist+Vector((0,0,-.25*up+raise_))
    bpy.context.view_layer.update()
    for a in (1,-1):
        sh=H['arm'][a].matrix_world.translation; side=1 if (sh-p).dot(rt)>0 else -1
        arm_reach(H,a,tuple(p+rt*side*.075+Vector((0,0,-.05))))
    ph.location=(p.x,p.y,p.z); ph.rotation_euler=(R(-28),0,H['root'].rotation_euler[2]+R(180)); return p
def phone_ear(H,ph,s=1):
    h=Vector(headpos(H)); M3=root_mat(H).to_3x3(); p=h+M3@Vector((s*.34,-.02,-.08)); arm_reach(H,s,tuple(p+Vector((0,0,-.05)))); ph.location=tuple(p); ph.rotation_euler=(0,0,H['root'].rotation_euler[2]+R(s*90)); return p
def insert_cam(ph,lens=26,dist=.18):
    H=OWNER[0]
    if H: body_vis(H,False)
    bpy.context.view_layer.update(); m=ph.matrix_world; c=m@Vector((.0,-dist,.012)); tg=m@Vector((0,0,0)); _camset(tuple(c),tuple(tg),lens,22,focus=tuple(tg))
def cam_close(H,side=1,dist=2.1,lens=28,ang=28,dz=.38,tz=-.25):
    h=headpos(H); rz=H['root'].rotation_euler[2]+R(side*ang); f=(math.sin(rz),-math.cos(rz))
    camset((h[0]+f[0]*dist,h[1]+f[1]*dist,h[2]+dz),(h[0],h[1],h[2]+tz),lens,2.8,focus=h)
def celebrate(H,t,k=1.0):
    a=-150+18*math.sin(t*9); arms(H,a*k,0,-20*k+8*math.sin(t*9),a*k,0,20*k-8*math.sin(t*9+1))
def point_at(H,s,target,k=1.0):
    h=Vector(headpos(H)); d=(Vector(target)-h); d.normalize(); arm_reach(H,s,tuple(h+d*.75+Vector((0,0,-.3))),k)
def cv(C,lx,ly,lz):
    """car-local point -> world"""
    bpy.context.view_layer.update(); return tuple(C['root'].matrix_world@Vector((lx,ly,lz)))
def sit_in(C,H,key,t,rz_extra=0.0):
    p=seat_world(C,key); rz=math.degrees(C['root'].rotation_euler[2])+180+rz_extra
    seatH(H,p.x,p.y,rz,sh=C['seat_h']); H['root'].location[2]+=C['root'].location[2]; blink(H,t)
def drive_hands(C,H,t):
    st=C['steer']; bpy.context.view_layer.update(); m=st.matrix_world
    arm_reach(H,1,tuple(m@Vector((.17,0,.02+.01*math.sin(t*3))))); arm_reach(H,-1,tuple(m@Vector((-.17,0,.02))))
def wheels_spin(C,t,rate):
    pass   # plain round tyres: spin would be invisible
CAR_IN=[None]
def trio_in_car(C,w,bl,sh,t,look=None):
    sit_in(C,w,'drv',t); sit_in(C,bl,'pas',t); sit_in(C,sh,'back',t); drive_hands(C,w,t)
    arms(bl,-55,0,-8,-55,0,8); arms(sh,-50,0,-10,-50,0,10)
def cam_car_front(C,q,lz=1.75,dist=2.9,lens=19,tx=0.0):
    c=cv(C,tx,1.2+dist,lz); tg=cv(C,tx*.3,-.6,1.5); _camset(c,tg,lens,6,focus=tg)
def cam_in(C,lx,ly,lz,tx,ty,tz,lens=20,fs=2.8): _camset(cv(C,lx,ly,lz),cv(C,tx,ty,tz),lens,fs,focus=cv(C,tx,ty,tz))
# ============================================================ 1. THE PLAN + TOLL PLAZA JAM (morning)
def mw_scene(phupho=True,donkey=True):
    cars=motorway(); dhaba(); C=hero_car(HERO_LANE,HERO_Y,0); B.done('mw'); setup_render('morning',res=PCT,samples=SAMPLES,shadow_dist=50)
    w=person((0,0,0),180,WALEED,'smile',name='waleed'); bl=person((0,0,0),180,BILAL,'smile',name='bilal'); sh=person((0,0,0),180,SHERRY,'smile',name='sherry')
    P=None; ph_=None; kids=[]
    if phupho:
        P=hero_car(-1.8,HERO_Y,0,col='#E8A33A',open_side=1)
        r=P['root']; ocyl((0,-.2,2.62),.44,.42,M('#B9C2CC',.25,metal=.85),r,rot=(0,0,0),seg=20); ocyl((0,-.2,2.84),.46,.04,M('#9AA2AC',.25,metal=.85),r,rot=(0,0,0),seg=20)
        obox((0,.7,2.5),(.5,.3,.16),M('#C8102E',.7,kind='fabric'),.05,r)
        ph_=person((0,0,0),180,PHUPHO,'smile',name='phupho'); kids=[person((0,0,0),180,local(31,True),'grin',name='kid1'),person((0,0,0),180,local(37,True),'grin',name='kid2')]
    D=donkey_cart(LANES[3],HERO_Y-14,90) if donkey else None; dm=person((0,0,0),0,GADHAWALA,'smile',name='gadhawala') if donkey else None
    return dict(C=C,w=w,bl=bl,sh=sh,P=P,ph=ph_,kids=kids,D=D,dm=dm)
def mw_people(S,t):
    C=S['C']; trio_in_car(C,S['w'],S['bl'],S['sh'],t)
    if S['P']:
        sit_in(S['P'],S['ph'],'drv',t); sit_in(S['P'],S['kids'][0],'back',t,-12); S['kids'][1]['root'].location=(9,9,-9)
        arms(S['ph'],-50,0,-10,-50,0,10); arms(S['kids'][0],-60,0,-10,-60,0,10)
def donkey_at(S,y,t):
    D=S['D']; D['root'].location=(LANES[3],y,0); donkey_walk(D,t); dm=S['dm']
    p=Vector(D['root'].location)+Vector((-.2,0,0)); seatH(dm,p.x,p.y,-90,sh=1.0); blink(dm,t); arms(dm,-60,0,-10,-60,0,10)
def SH_M(view):
    KEY='M_'+view; S=mw_scene(phupho=view not in ('hook',),donkey=True); C=S['C']; w,bl,sh=S['w'],S['bl'],S['sh']
    cup=cup_obj(); plate=plate_obj()
    def upd(t):
        q=ease(t/DUR); mw_people(S,t); cup.location=(9,9,-9); plate.location=(9,9,-9)
        hw=headpos(w); hb=headpos(bl); hs=headpos(sh)
        donkey_at(S,HERO_Y-14,t)
        if view=='hook':      # crane up over the endless jam towards the toll plaza and the snowy mountains
            donkey_at(S,HERO_Y+1.0+t*.4,t); face(w,mouth='smile')
            _camset((L(3.2,4.0,q),L(-22,-26,q),L(2.0,9.0,q)),(L(2.0,1.0,q),L(-10,10,q),L(1.4,2.0,q)),L(20,17,q),8,focus=hw)
        elif view=='plan':    # front through the windscreen: all three happy, Waleed driving with sunglasses vibe
            face(w,mouth='grin',eyes=1.1); face(bl,mouth='smile'); face(sh,mouth='grin'); look_at(bl,hw,.3*math.sin(t)); cam_car_front(C,q,dist=L(3.3,2.9,q))
        elif view=='six':     # "Subah chhe baje niklenge…" Waleed close, confident
            talk(w,t,23,29,KEY,rest='smirk'); face(w,brow=.06,eyes=1.1); look_at(w,hb,.5); cam_in(C,.45,1.22,1.72,.58,-.1,1.62,16)
        elif view=='bilal':   # Bilal deadpan
            talk(bl,t,30,37,KEY,rest='flat',shapes=('flat','o','flat','O')); face(bl,eyes=.8,brow=-.04); look_at(bl,hw,.7); bl['head'].rotation_euler[1]=R(6)
            cam_in(C,-.45,1.22,1.72,-.58,-.1,1.62,16)
        elif view=='kis':     # "Pakistan ko kis ne bataya?" — honestly confused
            talk(w,t,38,42,KEY,rest='O',shapes=('O','o','O','flat')); face(w,eyes=1.3,brow=.1); look_at(w,hb,.8); w['head'].rotation_euler[1]=R(-10)
            cam_in(C,.4,1.22,1.72,.58,-.1,1.62,18)
        elif view=='toll':    # high wide: the line never ends
            _camset((L(-6,-6.5,q),L(-34,-30,q),L(8,11,q)),(1.5,L(5,15,q),1.0),L(18,20,q),8,focus=(1.8,HERO_Y,1))
        elif view=='donkey':  # the donkey cart strolls past them in the empty lane
            donkey_at(S,L(HERO_Y-4.5,HERO_Y+5,t/DUR),t); face(w,mouth='O',eyes=1.2); look_at(w,headpos(S['dm']),.8); look_at(sh,headpos(S['dm']),.8)
            _camset((3.7,L(HERO_Y-7.5,HERO_Y-6.8,q),1.35),(L(4.6,5.0,q),HERO_Y+2,1.15),L(18,20,q),5,focus=headpos(S['dm']))
        elif view=='overtake':# Sherry in the back seat, pointing out of the window
            donkey_at(S,HERO_Y+5+t*.6,t); talk(sh,t,66,70,KEY,rest='O',shapes=('O','shout','O','grin')); face(sh,eyes=1.35,brow=.1)
            point_at(sh,1,cv(C,3.0,4,1.3)); look_at(sh,cv(C,3.0,4,1.3),.8); cam_in(C,-.1,.55,1.85,0,-1.55,1.62,18)
        elif view=='hour':    # an hour later: the car crawls two metres
            C['root'].location[1]=HERO_Y+.6*ease(t/DUR); wheels_spin(C,t,1.2); mw_people(S,t); face(w,mouth='flat',eyes=.7); face(bl,mouth='flat',eyes=.6)
            _camset((L(3.4,3.2,q),L(HERO_Y-6.5,HERO_Y-6.0,q),2.9),(1.8,HERO_Y+2,1.3),L(22,24,q),6,focus=cv(C,0,0,1.4))
        elif view=='chai':    # Sherry walks back with his chai; the car has not moved an inch
            sh['root'].location=(9,9,-9) if False else sh['root'].location
            pts=[(DHABA[0]-1.6,DHABA[1]+.6),(6.2,HERO_Y+2.6),(3.6,HERO_Y-.4)]; walk_path(sh,pts,t,0,DUR-.8,step=.5,arm=12); blink(sh,t)
            p=Vector(hand_w(sh,1)); arm_reach(sh,1,tuple(Vector(headpos(sh))+root_mat(sh).to_3x3()@Vector((.18,-.3,-.45)))); cup.location=tuple(Vector(hand_w(sh,1))+Vector((0,0,.05)))
            face(sh,mouth='smile' if t<DUR-.9 else 'flat',eyes=1.0)
            _camset((L(7.8,7.4,q),L(HERO_Y-6.5,HERO_Y-6.0,q),1.75),(L(6.5,3.6,q),L(HERO_Y-1,HERO_Y,q),1.2),L(18,20,q),6,focus=headpos(sh))
        elif view in ('family','biryani'):
            P=S['P']; hp=headpos(S['ph'])
            if view=='family':   # Phupho's car: a pateela strapped on the roof
                _camset((L(.1,0.0,q),L(HERO_Y+3.6,HERO_Y+3.2,q),L(3.6,3.3,q)),(-1.8,HERO_Y-.3,1.9),L(20,22,q),6,focus=hp)
                k=ease((t-wl(99,KEY))/.6); look_at(S['ph'],hb,.8*k); face(S['ph'],mouth='smile')
            else:                # "Beta, biryani khaoge?" — plate out of the window
                k=ease(t/.5); p=Vector(cv(P,1.35+.25*k,.15,1.45)); arm_reach(S['ph'],1,tuple(p)); plate.location=tuple(p+Vector((0,0,.04)))
                talk(S['ph'],t,104,116,KEY,rest='smile',shapes=('o','smile','O','grin')); face(S['ph'],eyes=1.05,brow=.04); look_at(S['ph'],hb,.8)
                look_at(bl,tuple(plate.location),.8); face(bl,mouth='O',eyes=1.25)
                _camset((L(.0,-.05,q),HERO_Y+1.9,1.75),(hp[0]+.15,hp[1]-.1,hp[2]-.25),22,2.8,focus=hp)
    return dict(upd=upd)
for v in ('hook','plan','six','bilal','kis','toll','donkey','overtake','hour','chai','family','biryani'): SHOTS['M_'+v]=(lambda v=v: SH_M(v))
# ============================================================ 2. MOUNTAIN ROAD: bhutta, snow, stuck, dhakka (snowy)
CARY=6.0
def SH_N(view):
    KEY='N_'+view; BH=mountain_road(); C=hero_car(MX+2.2,CARY,0); B.done('mt'); setup_render('snowy',res=PCT,samples=SAMPLES,shadow_dist=40)
    w=person((0,0,0),180,WALEED,'smile',name='waleed'); bl=person((0,0,0),180,BILAL,'smile',name='bilal'); sh=person((0,0,0),180,SHERRY,'smile',name='sherry')
    bw=person((BH['x']-.7,BH['y']+.2,0),-90,BHUTTA,'smirk',name='bhutta'); corn=bhutta_obj(); snowball=oico((0,0,0),.07,SNOW)
    strangers=[person((0,0,0),0,local(60+i*7,False),'grin',name='st%d'%i) for i in range(5)] if view in ('push','chain') else []
    extra=[]
    if view=='chain':
        for k in range(10): extra.append(person((0,0,0),0,local(120+k*5,k%4==3),'grin',name='ex%d'%k))
    def upd(t):
        q=ease(t/DUR); bw_h=headpos(bw); standH(bw,BH['x']-.75,BH['y']+.2,-90+8*math.sin(t*.8),t); blink(bw,t); corn.location=(9,9,-9); snowball.location=(9,9,-9)
        for H in strangers+extra: H['root'].location=(9,9,-9)
        if view=='bhutta1':     # driving up past the 50 and 100 boards
            C['root'].location[1]=L(-30,-6,t/DUR); wheels_spin(C,t,-9); trio_in_car(C,w,bl,sh,t); face(w,mouth='smile'); face(sh,mouth='O',eyes=1.2); look_at(sh,(MX-6,C['root'].location[1]+2,1.8),.8)
            cy=C['root'].location[1]; _camset((MX-2.6,cy-5.2,2.1),(MX-1.0,cy+3.0,1.3),18,6,focus=cv(C,0,0,1.2))
        elif view=='bhutta2':   # "Teen sau. Barf ka view free hai."
            C['root'].location[1]=BH['y']-1.0; trio_in_car(C,w,bl,sh,t); look_at(w,bw_h,.7)
            talk(bw,t,129,135,KEY,rest='smirk',shapes=('o','smirk','O','grin')); face(bw,eyes=.85,brow=.05)
            arm_reach(bw,1,tuple(Vector(bw_h)+root_mat(bw).to_3x3()@Vector((.2,-.45,-.35)))); corn.location=tuple(Vector(hand_w(bw,1))+Vector((0,0,.12)))
            look_at(bw,cv(C,0,0,1.4),.6); cam_close(bw,-1,1.9,26,ang=25)
        elif view in ('snow','fridge'):
            C['root'].location[1]=CARY; sit_in(C,bl,'pas',t); sit_in(C,sh,'back',t); arms(bl,-55,0,-8,-55,0,8); arms(sh,-50,0,-10,-50,0,10)
            px,py=MX+4.3,CARY+.8
            if view=='snow':    # gets out, kneels, touches his first snow
                k=ease((t-.4)/1.0); standH(w,L(MX+3.8,px,k),py,L(-90,-60,k),t); blink(w,t)
                if t>1.4: kk=ease((t-1.4)/.6); w['root'].location[2]-=.35*kk; arm_reach(w,1,(px+.3,py-.35,L(.6,.2,kk))); face(w,mouth='grin',eyes=1.3,brow=.06)
                else: face(w,mouth='grin',eyes=1.2)
                _camset((L(MX+6.6,MX+6.2,q),L(CARY-2.8,CARY-2.4,q),1.25),(px,py,.9),L(20,24,q),4,focus=headpos(w))
            else:               # "Yeh to fridge wali barf hai!" — holds a snowball, disappointed
                standH(w,px+.3,py,70,t); blink(w,t); talk(w,t,147,152,KEY,rest='frown',shapes=('O','frown','o','flat')); face(w,eyes=.95,brow=-.06)
                hw=Vector(headpos(w)); p=hw+root_mat(w).to_3x3()@Vector((.3,-.42,-.62)); arm_reach(w,1,tuple(p)); snowball.location=tuple(p+Vector((0,0,.06)))
                h=headpos(w); rz=w['root'].rotation_euler[2]+R(-22); _camset((h[0]+math.sin(rz)*1.9,h[1]-math.cos(rz)*1.9,h[2]+.25),(h[0],h[1],h[2]-.25),28,2.8,focus=h)
        elif view=='stuck':     # wheels spin, snow sprays; Bilal jumps out: "Dhakka lagao!"
            C['root'].location=(MX+2.2+.02*math.sin(t*40),CARY,0); wheels_spin(C,t,-30); sit_in(C,w,'drv',t); drive_hands(C,w,t); face(w,mouth='strain',eyes=1.2)
            sit_in(C,sh,'back',t); arms(sh,-50,0,-10,-50,0,10); face(sh,mouth='O')
            standH(bl,MX+.4,CARY-1.0,heading_to(bl,headpos(w)),t); blink(bl,t); talk(bl,t,159,160,KEY,rest='O',shapes=('shout','O','shout','O')); face(bl,eyes=1.3,brow=.1); celebrate(bl,t,.6)
            for i in range(8):
                f_=t*3+i*.37; ph_=f_%1.0; snowball.location=(9,9,-9)
            _camset((L(MX-1.6,MX-1.2,q),L(CARY-5.0,CARY-4.6,q),1.3),(MX+1.6,CARY,1.0),L(19,21,q),5,focus=headpos(bl))
        elif view=='push':      # five strangers push the car out; then: "Ab hamari bhi nikalwao"
            k=ease((t-.6)/1.6); C['root'].location[1]=CARY+1.8*k; wheels_spin(C,t,-6*k); sit_in(C,w,'drv',t); drive_hands(C,w,t); face(w,mouth='grin' if k>.5 else 'strain')
            sit_in(C,sh,'back',t); arms(sh,-50,0,-10,-50,0,10)
            standH(bl,MX+.4,CARY-1.0,heading_to(bl,cv(C,0,-2.4,1)),t); celebrate(bl,t,.5*k); blink(bl,t)
            rear=Vector(cv(C,0,-2.48,0))
            for i,H in enumerate(strangers):
                if t<wl(169,KEY):
                    x_=rear.x-1.0+i*.5; y_=rear.y-.62-(.2 if i%2 else 0); standH(H,x_,y_,180,t); H['root'].rotation_euler[0]=R(-14)
                    arm_reach(H,1,(x_+.15,rear.y+.05,.95)); arm_reach(H,-1,(x_-.15,rear.y+.05,.95)); face(H,mouth='strain')
                else:
                    standH(H,MX+1.0-i*.55,CARY-2.6-(i%2)*.4,heading_to(H,headpos(w)),t); face(H,mouth='grin'); blink(H,t)
            if t>=wl(169,KEY):
                talk(strangers[0],t,171,174,KEY,rest='grin',shapes=('o','grin','O','grin')); point_at(strangers[0],1,(MX-2.2,CARY+6,1),1.0)
            _camset((L(MX-3.0,MX-2.6,q),L(CARY-7.0,CARY-6.4,q),1.7),(MX+1.4,CARY-1.0,1.0),L(18,20,q),6,focus=cv(C,0,-2.4,1.2))
        elif view=='chain':     # two hours later the whole of Murree is pushing everyone's car
            C['root'].location[1]=CARY+1.8; sit_in(C,w,'drv',t); drive_hands(C,w,t); sit_in(C,sh,'back',t); arms(sh,-50,0,-10,-50,0,10); bl['root'].location=(9,9,-9)
            crew=strangers+extra; slots=[(MX-2.2,30),(MX+2.2,36),(MX-2.2,42)]
            for i,H in enumerate(crew):
                cx,cy=slots[i%3]; x_=cx-1.0+(i//3)*.5; y_=cy-2.9; standH(H,x_,y_,0,t); H['root'].rotation_euler[0]=R(14)
                arm_reach(H,1,(x_+.15,cy-2.2,.95)); arm_reach(H,-1,(x_-.15,cy-2.2,.95)); face(H,mouth='strain'); H['root'].location[1]+=.04*math.sin(t*5+i)
            _camset((L(MX+8,MX+7,q),L(14,18,q),L(5.5,6.5,q)),(MX,L(34,36,q),1.0),L(20,18,q),8,focus=(MX,36,1))
    return dict(upd=upd)
for v in ('bhutta1','bhutta2','snow','fridge','stuck','push','chain'): SHOTS['N_'+v]=(lambda v=v: SH_N(v))
# ============================================================ 3. HOTEL (day, fog)
def SH_O(view):
    KEY='O_'+view; hotel(); B.done('hotel'); setup_interior('day',(HX,0,3.6),res=PCT,samples=SAMPLES); bpy.context.scene.view_settings.exposure=-.5
    rc=person((HX,2.35,0),0,RECEP,'smile',name='recep'); w=person((HX+.5,.4,0),180,WALEED,'smile',name='waleed'); bl=person((HX-.5,.3,0),180,BILAL,'flat',name='bilal'); sh=person((HX-2.6,-.4,0),90,SHERRY,'frown',name='sherry')
    def upd(t):
        q=ease(t/DUR); hr=headpos(rc); hw=headpos(w)
        standH(rc,HX,2.35,0,t); blink(rc,t); standH(w,HX+.5,.4,180,t); standH(bl,HX-.5,.3,180,t); blink(w,t); blink(bl,t); look_at(w,hr,.6); look_at(bl,hr,.6)
        standH(sh,HX-3.9,-.5,90,t); blink(sh,t)
        if view=='rates':     # points at the rate board, line by line
            talk(rc,t,188,204,KEY,rest='smile',shapes=('o','smile','O','flat')); face(rc,eyes=.95,brow=.03); look_at(rc,hw,.6)
            k=(t*.5)%1; arm_reach(rc,1,tuple(Vector(hr)+Vector((.45,.5,.15-.5*k)))); face(w,mouth='O' if t>2 else 'flat',eyes=1.1+.25*min(1,t/4)); face(bl,mouth='flat',eyes=.8)
            _camset((L(HX+2.6,HX+2.4,q),L(-1.3,-1.0,q),1.75),(HX-.2,1.9,L(1.55,1.7,q)),L(18,20,q),4,focus=hr)
        elif view=='fog':     # Sherry at the window: outside is only fog
            talk(sh,t,205,211,KEY,rest='frown',shapes=('O','shout','O','frown')); face(sh,eyes=1.25,brow=-.06); point_at(sh,1,(HX-5,-.5,1.8)); look_at(sh,hr,.5)
            _camset((L(HX-1.6,HX-1.9,q),L(-2.6,-2.3,q),1.6),(HX-4.2,-.5,1.55),L(20,24,q),3,focus=headpos(sh))
        else:                 # 'premium': "Sir, dhund bhi premium snow hai." — smug
            talk(rc,t,212,217,KEY,rest='smirk',shapes=('o','smirk','O','smirk')); face(rc,eyes=.8,brow=.07); look_at(rc,headpos(sh),.7); HIPS(rc) if False else arms(rc,-55,0,-55,-55,0,55)
            cam_close(rc,1,1.7,28,ang=15)
    return dict(upd=upd)
for v in ('rates','fog','premium'): SHOTS['O_'+v]=(lambda v=v: SH_O(v))
# ============================================================ 4. MALL ROAD at night: selfie, call, reveal reaction
FR=[(LX-.6,-1.0),(LX+.2,-1.15),(LX+1.0,-1.0)]     # Bilal, Waleed, Sherry
def SH_L(view):
    KEY='L_'+view; mk=mall_road(); B.done('mall'); setup_interior('night',(LX,0,8),res=PCT,samples=SAMPLES,shadow_dist=30); bpy.context.scene.view_settings.exposure=.25
    bl=person((FR[0][0],FR[0][1],0),0,BILAL,'grin',name='bilal'); w=person((FR[1][0],FR[1][1],0),0,WALEED,'grin',name='waleed'); sh=person((FR[2][0],FR[2][1],0),0,SHERRY,'grin',name='sherry'); OWNER[0]=w
    ph,scr=phone_obj('ph_ammi'); rnd=random.Random(7)
    specs=[(LX+rnd.uniform(-9,9),rnd.uniform(.5,4.2),rnd.uniform(-180,180)) for _ in range(26)]+[(LX+rnd.uniform(-9,9),rnd.uniform(-4.2,-2.2),rnd.uniform(-180,180)) for _ in range(8)]
    cr=crowd(specs,seed0=40); D=donkey_cart(LX+3.0,1.6,180)
    def upd(t):
        q=ease(t/DUR); hw=headpos(w); hb=headpos(bl); body_vis(w,True)
        for i,H in enumerate(cr): standH(H,specs[i][0],specs[i][1],specs[i][2]+10*math.sin(t*.5+i),t); blink(H,t+i)
        donkey_walk(D,t,.0);
        for i,m in enumerate(mk): m.rotation_euler[2]=R(170+25*math.sin(t*1.5+i))
        for H,(x,y) in zip((bl,w,sh),FR): standH(H,x,y,0,t); blink(H,t)
        if view=='selfie':    # selfie: two thousand people, three monkeys and the same donkey behind them
            h=Vector(hw); p=h+Vector((.05,-.75,.35)); arm_reach(w,1,tuple(p)); ph.location=tuple(p); ph.rotation_euler=(R(-10),0,0)
            set_screen(scr,'ph_ammi',0.0); face(w,mouth='grin',eyes=1.1); face(bl,mouth='grin'); face(sh,mouth='grin'); celebrate(sh,t,.5); arms(bl,-40,0,-60,-160,0,25)
            look_at(w,tuple(p),.6); look_at(bl,tuple(p),.6); look_at(sh,tuple(p),.6)
            D['root'].location=(L(LX+3.0,LX+1.0,t/DUR),1.6,0); donkey_walk(D,t,1)
            _camset((L(LX+.1,LX+.15,q),L(-4.1,-3.8,q),2.05),(LX+.2,1.5,1.6),L(17,18,q),8,focus=hw)
        elif view=='call':    # insert: Ammi calling
            phone_in_hand(w,ph,up=1.6); set_screen(scr,'ph_ammi',1.3); ph.location=(ph.location[0]+.002*math.sin(t*40),ph.location[1],ph.location[2]); insert_cam(ph,L(24,28,q),.2)
        elif view=='proud':   # "Ammi, Murree mein barf dekh raha hoon." — proud, on the phone
            phone_ear(w,ph,1); talk(w,t,242,248,KEY,rest='grin',shapes=('grin','o','O','smile')); face(w,eyes=1.1,brow=.05); w['root'].rotation_euler[2]=R(15)
            arms(w,w['arm'][1].rotation_euler[0]*180/pi,0,w['arm'][1].rotation_euler[2]*180/pi,-55,0,55) if False else None
            look_at(bl,hw,.6); look_at(sh,hw,.6); cam_close(w,-1,1.8,26,ang=12)
        elif view=='shock':   # "Bhai... Murree khud chal ke hamare ghar aa gaya."
            h=Vector(hw); p=h+Vector((0,-.42,-.55)); arm_reach(w,1,tuple(p+Vector((.07,0,-.05)))); arm_reach(w,-1,tuple(p+Vector((-.07,0,-.05)))); ph.location=tuple(p); ph.rotation_euler=(R(-60),0,R(180))
            set_screen(scr,'ph_roof',1.0); talk(w,t,281,289,KEY,rest='O',shapes=('O','o','O','shout')); face(w,eyes=1.4,brow=.1)
            for H in (bl,sh): look_at(H,tuple(p),.8); face(H,mouth='O',eyes=1.35,brow=.1)
            _camset((L(LX+.15,LX+.15,q),L(-3.4,-3.0,q),1.65),(LX+.2,-1.0,1.6),L(22,26,q),3,focus=hw)
        else:                 # 'dhund': Bilal defeated, fog creeping in
            ph.location=(9,9,-9); talk(bl,t,290,299,KEY,rest='frown',shapes=('o','frown','o','flat')); face(bl,eyes=.6,brow=.12); bl['head'].rotation_euler[0]=R(12)
            arms(bl,-8,0,-6,-8,0,6); face(w,mouth='frown',eyes=.7); face(sh,mouth='frown',eyes=.7)
            cam_close(bl,1,1.8,26,ang=18)
    return dict(upd=upd)
for v in ('selfie','call','proud','shock','dhund'): SHOTS['L_'+v]=(lambda v=v: SH_L(v))
# ============================================================ 5. AMMI ON THE ROOF (snow at home)
def SH_R(view):
    KEY='R_'+view; Rf=home_roof(); B.done('roof'); setup_render('snowy',res=PCT,samples=SAMPLES,shadow_dist=30)
    am=person((RX-.8,-.6,0),20,AMMI,'smile',name='ammi'); ph,scr=phone_obj('ph_ammi'); set_screen(scr,'ph_ammi',0.4)
    def upd(t):
        q=ease(t/DUR); snowfall(Rf['flakes'],t); ha=headpos(am); standH(am,RX-.8,-.6,20,t); blink(am,t)
        if view=='ammi':      # tight on Ammi: "Achha? Zara ghar ki chhat ki photo dekho." (snowflakes give it away)
            phone_ear(am,ph,1); talk(am,t,249,256,KEY,rest='smirk',shapes=('o','smirk','O','smile')); face(am,eyes=.95,brow=.05)
            cam_close(am,-1,1.35,32,ang=20,dz=.15)
        else:                 # 'snowman': slow push across the snowman — Waleed's beanie, Abbu's muffler, the halwa carrot
            ph.location=(9,9,-9); arms(am,-62,0,-58,-62,0,58); face(am,mouth='grin',eyes=1.0)
            sx,sy=Rf['snowman']
            if t<wl(271,KEY)-.05: tg=(sx,sy,1.95)
            elif t<wl(274,KEY)-.05: tg=(sx,sy,1.4)
            else: tg=(sx,sy-.3,1.66)
            k=ease(t/DUR); _camset((L(sx-1.6,sx-.2,k),L(sy-3.4,sy-1.6,k),L(1.6,1.75,k)),tg,L(24,34,k),3,focus=tg)
    return dict(upd=upd)
for v in ('ammi','snowman'): SHOTS['R_'+v]=(lambda v=v: SH_R(v))
# ============================================================ 6. PHOTO INSERT (the roof picture on Waleed's phone)
def SH_Q(view):
    mall_road(); B.done('mall'); setup_interior('night',(LX,0,8),res=PCT,samples=SAMPLES,shadow_dist=30); bpy.context.scene.view_settings.exposure=.25
    w=person((FR[1][0],FR[1][1],0),0,WALEED,'O',name='waleed'); OWNER[0]=w; ph,scr=phone_obj('ph_roof')
    def upd(t):
        q=ease(t/DUR); standH(w,FR[1][0],FR[1][1],0,t); phone_in_hand(w,ph,up=1.6); set_screen(scr,'ph_roof',1.1); insert_cam(ph,L(22,32,q),.2)
    return dict(upd=upd)
SHOTS['Q_photo']=lambda: SH_Q('photo')
# ============================================================ 7. CTA: going home, the same jam at night, the donkey overtakes again
def SH_Z(view):
    S=mw_scene(phupho=False,donkey=True); C=S['C']; sc=bpy.context.scene
    for o in sc.objects:
        if o.type=='LIGHT' and o.data.type=='SUN': o.data.energy=.25; o.data.color=(.55,.65,1.0)
    sc.view_settings.exposure=.6
    for k in range(-6,7): point((LANES[k%4],HERO_Y-30+k*6,1.0),35,(1,.25,.2),.3,shadow=False)
    def upd(t):
        q=ease(t/DUR); C['root'].rotation_euler[2]=R(180); C['root'].location=(HERO_LANE,HERO_Y,0); mw_people(S,t)
        face(S['w'],mouth='flat',eyes=.6); face(S['bl'],mouth='frown',eyes=.5); face(S['sh'],mouth='frown',eyes=.5); S['sh']['head'].rotation_euler[1]=R(18)
        D=S['D']; D['root'].rotation_euler[2]=R(-90); D['root'].location=(LANES[3],L(HERO_Y+6,HERO_Y-6,t/DUR),0); donkey_walk(D,t); dm=S['dm']
        p=Vector(D['root'].location); seatH(dm,p.x,p.y+.2,90,sh=1.0); arms(dm,-60,0,-10,-60,0,10); face(dm,mouth='grin')
        _camset((L(3.75,3.6,q),L(HERO_Y-8.5,HERO_Y-8.0,q),1.4),(L(3.4,2.8,q),HERO_Y+1,1.3),L(19,21,q),5,focus=cv(C,0,0,1.3))
    return dict(upd=upd)
SHOTS['Z_cta']=lambda: SH_Z('cta')
