SHOTS={}
WJ=json.load(open('/home/claude/abbu/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('M_hook', 0), ('M_ac', 7), ('M_guard', 17), ('M_shirt', 22), ('M_cash', 31), ('M_atm', 58), ('M_atmscr', 65), ('M_food', 75), ('M_waiter', 87), ('M_snatch', 99), ('M_stranger', 112), ('B_cut', 123), ('B_out', 130), ('B_fauji', 135), ('C_cinema', 145), ('C_advice', 154), ('N_cab', 165), ('N_tez', 175), ('N_switch', 184), ('H_home', 202), ('H_abbu', 214), ('H_pizza', 224), ('H_stare', 234), ('H_switch', 251), ('H_bill', 261), ('H_end', 265), ('H_cta', 279)]
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
    H=_pers(*a,**k); PEOPLE.append(H); C=a[2] if len(a)>2 else {}
    sl=C.get('slim') if isinstance(C,dict) else None
    if sl:
        for o in H['root'].children:
            if o is H['head']: continue
            o.location.x*=sl[0]; o.location.y*=sl[1]; o.scale.x*=sl[0]; o.scale.y*=sl[1]
    return H
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

# ============================================================ helpers for "Everyone Is Abbu"
OWNER=[None]; ALLP=[]; KEEP=[None]; NEAR=[1.5]
def body_vis(H,on):
    if '_body' not in H: H['_body']=[o for o in [H['root']]+list(H['root'].children_recursive) if o.type=='MESH']
    for o in H['_body']: o.hide_render=not on
def hide_block():
    cam=bpy.context.scene.camera; bpy.context.view_layer.update(); Mi=cam.matrix_world.inverted()
    fd=cam.data.dof.focus_distance if cam.data.dof.focus_distance>.1 else 3.0; lens=cam.data.lens; hx=10.125/lens; hy=18.0/lens
    for H in ALLP:
        if H is OWNER[0]: continue
        if H['root'].location.z<-5: continue
        K=KEEP[0]
        if K is not None and H in K: body_vis(H,True); continue
        lim=fd+.3 if K is not None else min(fd-.55,NEAR[0]); h=Vector(headpos(H)); blk=False
        for p in (h,h-Vector((0,0,.45)),h-Vector((0,0,.85))):
            v=Mi@p; d=-v.z
            if .05<d<lim and abs(v.x)<hx*d+.35 and abs(v.y)<hy*d+.35: blk=True;break
        body_vis(H,not blk)
def reg(*Hs):
    for H in Hs: ALLP.append(H)
def insert_cam(ph,lens=26,dist=.18):
    H=OWNER[0]
    if H: body_vis(H,False)
    bpy.context.view_layer.update(); m=ph.matrix_world; c=m@Vector((.0,-dist,.012)); tg=m@Vector((0,0,0)); _camset(tuple(c),tuple(tg),lens,22,focus=tuple(tg))
def phone_in_hand(H,ph,up=2.0,face_dist=.55,raise_=0.0,two=True):
    h=Vector(headpos(H)); M3=root_mat(H).to_3x3(); f=M3@Vector((0,-1,0)); rt=M3@Vector((1,0,0)); p=h+f*face_dist+Vector((0,0,-.25*up+raise_))
    bpy.context.view_layer.update()
    for a in ((1,-1) if two else (1,)):
        sh=H['arm'][a].matrix_world.translation; side=1 if (sh-p).dot(rt)>0 else -1
        arm_reach(H,a,tuple(p+rt*side*.075+Vector((0,0,-.05))))
    ph.location=(p.x,p.y,p.z); ph.rotation_euler=(R(-28),0,H['root'].rotation_euler[2]+R(180)); return p
def phone_ear(H,ph,s=1):
    h=Vector(headpos(H)); M3=root_mat(H).to_3x3(); p=h+M3@Vector((s*.34,-.02,-.08)); arm_reach(H,s,tuple(p+Vector((0,0,-.05)))); ph.location=tuple(p); ph.rotation_euler=(0,0,H['root'].rotation_euler[2]+R(s*90)); return p
def front_cam(H,dist=1.7,lens=26,ang=25,dz=.3,tz=-.2,fs=2.8):
    h=headpos(H); rz=H['root'].rotation_euler[2]+R(ang); f=(math.sin(rz),-math.cos(rz))
    _camset((h[0]+f[0]*dist,h[1]+f[1]*dist,h[2]+dz),(h[0],h[1],h[2]+tz),lens,fs,focus=h)
def two_cam(A,Bh,side=1,dist=2.6,lens=22,dz=.25,fs=4):
    a=Vector(headpos(A)); b=Vector(headpos(Bh)); m=(a+b)/2; d=(b-a); d.z=0; d.normalize(); n=Vector((-d.y,d.x,0))*side
    c=m+n*dist+Vector((0,0,dz)); _camset(tuple(c),tuple(m+Vector((0,0,-.25))),lens,fs,focus=tuple(m))
def celebrate(H,t,k=1.0,ph=0.0):
    a=-150+18*math.sin(t*9+ph); arms(H,a*k,0,-20*k+8*math.sin(t*9+ph),a*k,0,20*k-8*math.sin(t*9+1+ph))
def point_at(H,s,target,k=1.0):
    h=Vector(headpos(H)); d=(Vector(target)-h); d.normalize(); arm_reach(H,s,tuple(h+d*.75+Vector((0,0,-.3))),k)
def hand_front(H,s,fwd=.42,dz=-.5,side=.15):
    return tuple(Vector(headpos(H))+root_mat(H).to_3x3()@Vector((s*side,-fwd,dz)))
def gossip(H,t,ph=0.0,talking=True):
    if talking: face(H,mouth=('o','smile','O','grin','flat')[int(t*7+ph*3)%5]); arms(H,-35-18*math.sin(t*4+ph),0,10,-20,0,-8)
    else: face(H,mouth='smile'); arms(H,-14,0,6,-14,0,-6)
def WAL(): return person((0,0,0),0,WALEED,'smile',name='waleed')
WALEED_CUT=dict(WALEED,hairstyle='short')
def fan_self(H,t,ph=0.0,obj=None):
    p=Vector(headpos(H))+root_mat(H).to_3x3()@Vector((.22,-.3,-.15+.06*math.sin(t*11+ph))); arm_reach(H,1,tuple(p))
    if obj: obj.location=tuple(p+Vector((0,0,.1))); obj.rotation_euler=(R(20*math.sin(t*11+ph)),0,H['root'].rotation_euler[2])
def sweat_wipe(H,t):
    arm_reach(H,-1,tuple(Vector(headpos(H))+root_mat(H).to_3x3()@Vector((.05,-.2,.12+.03*math.sin(t*6)))))
def wag(H,t,s=1):
    arms(H,-20,0,-10,-120,0,10+10*math.sin(t*10)) if s==1 else arms(H,-120,0,-10-10*math.sin(t*10),-20,0,10)
def stern(H,t): face(H,mouth='frown',eyes=.95,brow=-.08)
def dads(specs,seed=0):
    G=[]
    for i,(x,y,rz,act) in enumerate(specs):
        H=person((x,y,0),rz,dad(400+seed*37+i*11),'flat',name='dd%d_%d'%(seed,i)); H['xy']=(x,y,rz); H['act']=act; H['ph']=i*1.3
        if act=='fan': H['np']=empty((0,0,0)); obox((0,0,0),(.12,.008,.16),M('#E8E2D6',.6),.005,H['np'])
        G.append(H)
    reg(*G); return G
def dads_upd(G,t,look=None,walkers=None):
    for i,H in enumerate(G):
        x,y,rz=H['xy']; a=H['act']
        if a=='walk':
            Lp=6.0; d=((t*.9+i*1.7)%Lp); yy=y+(d if (int((t*.9+i*1.7)/Lp)%2==0) else Lp-d); standH(H,x,yy,180 if int((t*.9+i*1.7)/Lp)%2==0 else 0,t); walk(H,yy,step=.5,arm=18,t=t)
        else: standH(H,x,y,rz,t)
        blink(H,t+i)
        if a=='fan': fan_self(H,t,H['ph'],H['np']); face(H,mouth='frown',eyes=.9)
        elif a=='talk':
            if int((t+H['ph'])/2.6)%2==0: face(H,mouth=('o','frown','O','flat')[int(t*6+i)%4]); arms(H,-30-12*math.sin(t*4+i),0,10,-14,0,-6)
            else: face(H,mouth='flat'); arms(H,-12,0,6,-12,0,-6)
        elif a=='read': arms(H,-70,0,-25,-70,0,25); H['head'].rotation_euler=(R(18),0,0); face(H,mouth='flat')
        elif a=='walk': face(H,mouth='flat')
        else: arms(H,-8,0,-38,-8,0,38); stern(H,t)
        if look is not None and a!='walk': look_at(H,look,.7)
# ============================================================ M. THE MALL
def SH_M(view):
    KEY='M_'+view; D=mall(); B.done('mall'); setup_interior('day',(0,12,8),res=PCT,samples=SAMPLES,shadow_dist=30); bpy.context.scene.view_settings.exposure=-.7
    w=WAL(); reg(w)
    specs=[(-3.6,0,30,'fan'),(-2.6,1.3,210,'talk'),(3.4,1.5,160,'read'),(-4.4,5.0,90,'fan'),(4.6,10.5,250,'stand'),(-3.8,14,120,'talk'),(-2.6,15.0,300,'fan'),
           (3.8,15.5,200,'fan'),(-1.5,9,0,'walk'),(3.0,6,0,'walk'),(-4.6,22,80,'read'),(4.8,27,240,'fan'),(.5,27.5,180,'talk'),(1.6,28.6,0,'fan')]
    if view in ('food','waiter','snatch','stranger'): specs=[s for s in specs if not (15<s[1]<20)]
    if view=='hook': specs=specs+[(2.3,-.6,270,'fan'),(-2.3,-1.6,90,'stand'),(1.2,3.6,180,'stand'),(2.6,3.2,200,'read'),(-2.6,-3.4,60,'stand'),(2.7,-2.8,300,'stand')]
    G=dads(specs,1)
    gd=person((0,0,0),0,GUARDB,'flat',name='guard'); cs=person((0,0,0),0,CASHIER,'flat',name='cashier'); wt=person((0,0,0),0,WAITER,'flat',name='waiter'); st=person((0,0,0),0,STRANGER,'flat',name='stranger'); reg(gd,cs,wt,st)
    sh=shirt_obj(); tr=tray_obj(); ph,scr=phone_obj('ph_chat')
    def upd(t):
        q=ease(t/DUR); OWNER[0]=None; KEEP[0]=None
        for o in (sh,tr,ph): o.location=(0,0,-9)
        for H in (gd,cs,wt,st): H['root'].location=(0,0,-9)
        set_screen(D['atm'],'atm1',1.0)
        standH(gd,-1.0,3.6,heading_to(gd,headpos(w)),t); blink(gd,t); arms(gd,-8,0,-38,-8,0,38); stern(gd,t)
        standH(cs,5.95,7.0,270,t); blink(cs,t); stern(cs,t); arms(cs,-30,0,-8,-30,0,8)
        dads_upd(G,t,look=headpos(w) if view in ('hook','guard','cash','stranger') else None)
        if view=='hook':      # every man in the mall is someone's Abbu — and they all turn to the boy who walked in
            walk_path(w,[(0,-5),(0,-1.2)],t,0,DUR*.8,step=.55,arm=22); blink(w,t); face(w,mouth='smile' if t<1.5 else 'O',eyes=1.15)
            _camset((L(.4,.2,q),L(4.6,4.0,q),L(2.5,2.3,q)),(0,-1.8,1.3),L(17,18,q),6,focus=headpos(w))
        elif view=='ac':      # the AC is off. All of it.
            standH(w,-1.0,1.6,heading_to(w,(-1.8,4.0,4.9)),t); blink(w,t); sweat_wipe(w,t); look_at(w,(-1.8,4.0,4.9),.9,maxpitch=45); face(w,mouth='O',eyes=1.2)
            _camset((L(.3,.1,q),L(-.8,-.6,q),1.35),(-1.5,4.0,L(2.8,3.6,q)),L(17,19,q),6,focus=(-1.8,4.0,4.9))
        elif view=='guard':   # "AC? Bill tera peo dega?"
            standH(w,-1.0,1.6,heading_to(w,headpos(gd)),t); blink(w,t); face(w,mouth='flat',eyes=1.0); arms(w,-20,0,-8,-20,0,8)
            talk(gd,t,17,21,KEY,rest='frown',shapes=('o','frown','O','frown')); wag(gd,t)
            KEEP[0]=[gd]; front_cam(gd,1.8,L(24,26,q),ang=30,dz=.2)
        elif view=='shirt':   # three thousand rupees
            standH(w,2.5,4.6,300,t); blink(w,t); p=Vector(headpos(w))+root_mat(w).to_3x3()@Vector((.38,-.4,-.35)); sh.location=tuple(p); sh.rotation_euler=(0,0,w['root'].rotation_euler[2]+R(180))
            arm_reach(w,1,tuple(p+root_mat(w).to_3x3()@Vector((0,0,.3)))); arms(w,-20,0,-8,None or 0,0,0) if False else None; face(w,mouth='grin' if t<wl(28,KEY) else 'O',eyes=1.2)
            _camset((L(-.1,.1,q),L(6.3,6.1,q),1.6),(2.7,4.6,1.3),L(21,23,q),4,focus=headpos(w))
        elif view=='cash':    # "Tin hazaar? Saade zamane vich pooray saal de kapray aa jaande si."
            standH(w,4.25,7.0,90,t); blink(w,t); sh.location=(5.1,6.9,1.17); sh.rotation_euler=(R(90),0,R(90+30*ease((t-wl(47,KEY))/.6)))
            talk(cs,t,45,57,KEY,rest='frown',shapes=('o','frown','O','frown')); face(cs,eyes=1.1,brow=.1); wag(cs,t) if t>wl(47,KEY) else arms(cs,-60,0,-20,-60,0,20)
            if t<wl(45,KEY): look_at(cs,(5.1,6.9,1.17) if (t<wl(37,KEY) or t>wl(40,KEY)) else headpos(w),.9); face(cs,mouth='flat',eyes=1.2,brow=.1)
            face(w,mouth='smile' if t<wl(45,KEY) else 'flat',eyes=1.1); arms(w,-14,0,-6,-14,0,6)
            KEEP[0]=[cs,w]; two_cam(w,cs,side=-1,dist=2.4,lens=L(22,24,q),dz=.2)
        elif view=='atm':     # the ATM had questions
            standH(w,-5.55,7.5,270,t); blink(w,t); arm_reach(w,1,(-6.12,7.65+.03*math.sin(t*12),1.0)); look_at(w,(-6.13,7.5,1.38),.8); face(w,mouth='flat')
            _camset((L(-5.55,-5.6,q),L(9.0,8.9,q),1.65),(-5.9,7.5,1.3),L(19,21,q),4,focus=headpos(w))
        elif view=='atmscr':  # "Paise kis kam layi? Pichle mahine wale kithe gaye?"
            standH(w,-5.55,7.5,270,t); set_screen(D['atm'],'atm2' if t>.25 else 'atm1',1.0); OWNER[0]=w; body_vis(w,False)
            _camset((-5.3,7.5,1.42),(-6.13,7.5,1.38),L(28,31,q),16,focus=(-6.13,7.5,1.38))
        elif view in ('food','waiter','snatch','stranger'):
            tx,ty=TABLE; seatH(w,tx,ty-.85,180,sh=.48); blink(w,t)
            if view=='food':  # he orders a burger. The waiter brings roti and daal.
                tg=min(1,t/(DUR*.7)); walk_path(wt,[(4.6,20.5),(3.0,18.8),(2.3,17.4)],t,0,DUR*.7,step=.5,arm=8) if t<DUR*.7 else standH(wt,2.3,17.4,heading_to(wt,headpos(w)),t); blink(wt,t)
                p=Vector(headpos(wt))+root_mat(wt).to_3x3()@Vector((0,-.42,-.5)); 
                if t<DUR*.75: tr.location=tuple(p)
                else: tr.location=(tx,ty-.2,.78)
                arm_reach(wt,1,tuple(Vector(tr.location)+Vector((.18,0,.0)))); arm_reach(wt,-1,tuple(Vector(tr.location)+Vector((-.18,0,0)))); face(wt,mouth='smirk')
                look_at(w,headpos(wt),.6); face(w,mouth='grin' if t<DUR*.75 else 'O',eyes=1.2)
                _camset((L(-.2,0,q),L(19.4,19.0,q),1.75),(1.4,16.6,1.05),L(21,24,q),4,focus=headpos(w))
            elif view=='waiter':  # "Bahar da khana sehat layi changa nahi. Eh kha."
                standH(wt,2.3,17.4,heading_to(wt,headpos(w)),t); blink(wt,t); tr.location=(tx,ty-.2,.78)
                talk(wt,t,87,98,KEY,rest='frown',shapes=('o','frown','O','flat')); wag(wt,t,-1) if t<wl(92,KEY) else point_at(wt,-1,tuple(tr.location))
                face(wt,eyes=1.0,brow=-.06); face(w,mouth='flat',eyes=.85); look_at(w,headpos(wt),.6)
                KEEP[0]=[wt,w]; front_cam(wt,1.9,L(24,26,q),ang=-25,dz=.15)
            else:
                tr.location=(tx,ty-.2,.78); standH(wt,9,9,0,t)
                if view=='snatch':  # out comes the phone... and a stranger takes it out of his hand
                    tg=wl(108,KEY); walk_path(st,[(-1.0,14.5),(.9,15.2),(2.45,16.1)],t,0,tg,step=.5,arm=12) if t<tg else standH(st,2.45,16.1,heading_to(st,headpos(w)),t); blink(st,t)
                    k=ease((t-wl(110,KEY))/.5); hp=Vector(hand_front(w,1,.45,-.4,.1)); sp=Vector(headpos(st))+root_mat(st).to_3x3()@Vector((.2,-.25,.1))
                    pp=hp.lerp(sp,k); ph.location=tuple(pp); ph.rotation_euler=(R(-30),0,w['root'].rotation_euler[2]+R(180)); arm_reach(w,1,tuple(hp)) if k<.2 else arms(w,-40,0,-8,-60,0,10)
                    if t>wl(109,KEY): arm_reach(st,1,tuple(pp))
                    face(w,mouth='grin' if k<.2 else 'O',eyes=1.0 if k<.2 else 1.35); look_at(w,tuple(pp),.6); stern(st,t)
                    _camset((L(-.3,-.1,q),L(19.0,18.7,q),1.65),(1.5,16.4,1.1),L(21,23,q),4,focus=headpos(w))
                else:               # "Saara din phone. Akhaan kharab ho jaan giyan."
                    standH(st,2.45,16.1,heading_to(st,headpos(w)),t); blink(st,t); sp=Vector(headpos(st))+root_mat(st).to_3x3()@Vector((.5,-.15,.05)); ph.location=tuple(sp); arm_reach(st,1,tuple(sp))
                    talk(st,t,112,122,KEY,rest='frown',shapes=('o','frown','O','frown')); face(st,eyes=1.0,brow=-.08); point_at(st,-1,headpos(w)) if t>wl(115,KEY) else None
                    face(w,mouth='O',eyes=1.2); look_at(w,tuple(sp),.7)
                    KEEP[0]=[st]; front_cam(st,1.9,L(24,26,q),ang=30,dz=.2)
        hide_block()
    return dict(upd=upd)
for v in ('hook','ac','guard','shirt','cash','atm','atmscr','food','waiter','snatch','stranger'): SHOTS['M_'+v]=(lambda v=v: SH_M(v))
# ============================================================ B. THE BARBER — exact haircut Abbu had in 1985
def SH_B(view):
    KEY='B_'+view; D=barber(); B.done('bb'); setup_interior('day',(BX,0,3.0),res=PCT,samples=SAMPLES,shadow_dist=10)
    w=person((0,0,0),0,WALEED if view=='cut' else WALEED_CUT,'smile',name='waleed'); bb=person((0,0,0),0,BARBER,'flat',name='barber'); reg(w,bb)
    cust=person((0,0,0),0,dad(91),'flat',name='cust'); wt1=person((0,0,0),0,dad(93),'flat',name='wt1'); reg(cust,wt1)
    sc=scissors_obj(); hair=[oico((0,0,0),.02,M('#16100C',.8),sc=(1.4,.4,.4)) for _ in range(10)]
    def upd(t):
        q=ease(t/DUR); x1,y1,_,s1=D['chairs'][0]; x2,y2,_,s2=D['chairs'][1]
        seatH(cust,x2,y2,180,sh=s2); blink(cust,t); arms(cust,-50,0,-8,-50,0,8); stern(cust,t)
        seatH(wt1,BX-2.4,-1.4,90,sh=.47); blink(wt1,t); arms(wt1,-70,0,-25,-70,0,25); wt1['head'].rotation_euler=(R(15),0,0)
        for i,hb in enumerate(hair): hb.location=(0,0,-9)
        if view=='cut':      # in for a fresh cut...
            seatH(w,x1,y1,180,sh=s1); blink(w,t); arms(w,-15,0,-8,-15,0,8); face(w,mouth='smile',eyes=.9)
            standH(bb,x1+.1,y1-.75,heading_to(bb,headpos(w)),t); blink(bb,t); hp=Vector(headpos(w)); p=hp+Vector((.12*math.sin(t*3),-.05,.2+.05*math.sin(t*5))); sc.location=tuple(p); sc.rotation_euler=(0,R(20*math.sin(t*30)),0)
            arm_reach(bb,1,tuple(p)); arm_reach(bb,-1,tuple(hp+Vector((-.15,0,.25)))); face(bb,mouth='smirk',eyes=1.0,brow=-.03)
            for i,hb in enumerate(hair):
                k=((t*1.3+i*.37)%1.0); hb.location=(hp.x+.15*math.cos(i*2.1),hp.y+.1*math.sin(i*1.7),hp.z+.15-k*1.0)
            _camset((L(BX-2.7,BX-2.6,q),2.35,1.8),(BX-.85,.95,1.4),L(16,17,q),4,focus=headpos(w))
        elif view=='out':    # ...out with the exact haircut Abbu had in 1985
            standH(w,BX-1.7,.1,L(200,47,ease((t-.4)/.6)),t); blink(w,t); face(w,mouth='O',eyes=1.35,brow=.1); arms(w,-25,0,-30,-25,0,30)
            standH(bb,BX-.3,.8,heading_to(bb,headpos(w)),t); blink(bb,t); arms(bb,-8,0,-38,-8,0,38); face(bb,mouth='grin',eyes=1.0)
            KEEP[0]=[w,bb]; _camset((L(BX-.1,BX-.3,q),L(-1.4,-1.2,q),1.6),(BX-2.2,.3,1.5),L(20,23,q),4,focus=headpos(w))
        else:                # "Fauji cut. Hun lagda ae shareef banda."
            standH(w,BX-1.9,-.1,heading_to(w,(BX-.6,-1.5,1.5)),t); blink(w,t); face(w,mouth='flat',eyes=.9)
            standH(bb,BX-.5,.5,heading_to(bb,(BX-.6,-1.5,1.5)),t); blink(bb,t); talk(bb,t,135,144,KEY,rest='grin',shapes=('o','grin','O','grin')); face(bb,eyes=1.0,brow=.06)
            arms(bb,-8,0,-38,-150+12*math.sin(t*5),0,10)
            KEEP[0]=[bb,w]; _camset((L(BX-.9,BX-1.0,q),L(-2.0,-1.9,q),1.75),(BX-1.2,.2,1.45),L(20,22,q),4,focus=headpos(bb))
        hide_block()
    return dict(upd=upd)
for v in ('cut','out','fauji'): SHOTS['B_'+v]=(lambda v=v: SH_B(v))
# ============================================================ C. THE CINEMA — the movie pauses for advice
def SH_C(view):
    KEY='C_'+view; D=cinema(); B.done('cn'); setup_interior('night',(CX,0,6),res=PCT,samples=SAMPLES,shadow_dist=14); bpy.context.scene.view_settings.exposure=1.5
    w=person((0,0,0),0,WALEED_CUT,'smile',name='waleed'); us=person((0,0,0),0,USHER,'flat',name='usher'); reg(w,us)
    aud=[]
    for i,(r_,c) in enumerate(((0,-3),(0,2),(1,-1),(1,3),(2,-4),(2,-2),(2,2),(3,-1),(3,1),(3,4),(4,-3),(4,2),(5,0),(5,-2))):
        H=person((0,0,0),0,dad(700+i*5),'flat',name='au%d'%i); H['rc']=(r_,c); aud.append(H)
    reg(*aud); torch=empty((0,0,0)); ocyl((0,0,0),.03,.16,M('#2B2C33',.4),torch,rot=(R(90),0,0),seg=10)
    def upd(t):
        q=ease(t/DUR); x,y,_,sh=D['seat'](2,1); seatH(w,x,y,180,sh=sh); blink(w,t); arms(w,-50,0,-8,-50,0,8)
        for i,H in enumerate(aud):
            ax,ay,_,ash=D['seat'](*H['rc']); seatH(H,ax,ay,180,sh=ash); blink(H,t+i); arms(H,-50,0,-8,-50,0,8)
            look_at(H,headpos(us),.5); face(H,mouth=('flat','smirk','flat')[i%3])
        bpy.context.scene.view_settings.exposure=.45 if view=='cinema' else 1.5
        if view=='cinema':   # the hero freezes mid-punch: NASEEHAT BREAK. An usher steps in front of the screen.
            tg=DUR*.6; walk_path(us,[(CX+4.5,6.6),(CX+1.2,6.0)],t,.2,tg,step=.5,arm=12) if t<tg else standH(us,CX+1.2,6.0,heading_to(us,headpos(w)),t); blink(us,t)
            p=hand_front(us,1,.4,-.35,.15); torch.location=p; arm_reach(us,1,p); stern(us,t); face(w,mouth='O',eyes=1.3)
            _camset((L(CX-.6,CX-.2,q),L(-5.2,-4.6,q),L(4.3,4.0,q)),(CX,5.5,2.5),L(17,19,q),6,focus=(CX,7.8,3.2))
        else:                # "Eh hero vekh. Padhai poori kar ke aaya ae. Tu kad karenga?"
            standH(us,CX,y+.15,heading_to(us,headpos(w)),t); us['root'].location[2]=.44; blink(us,t)
            talk(us,t,154,164,KEY,rest='frown',shapes=('o','frown','O','frown')); face(us,eyes=1.0,brow=-.07)
            point_at(us,-1,(CX,7.85,3.4)) if t<wl(157,KEY) else point_at(us,1,headpos(w)); torch.location=hand_front(us,1,.3,-.5,.15)
            look_at(w,headpos(us),.6); face(w,mouth='flat',eyes=.85,brow=.05)
            KEEP[0]=[us,w]; _camset((CX+2.2,L(2.7,2.5,q),2.4),(CX+.3,.85,1.4),L(19,21,q),4,focus=headpos(us))
        hide_block()
    return dict(upd=upd)
for v in ('cinema','advice'): SHOTS['C_'+v]=(lambda v=v: SH_C(v))
# ============================================================ N. THE TAXI at 20 km/h, and the light switches
TXL=RX-1.8
def SH_N(view):
    KEY='N_'+view; LIT=night_road(); B.done('nr'); setup_interior('night',(RX,10,7),res=PCT,samples=SAMPLES,shadow_dist=25); bpy.context.scene.view_settings.exposure=.3
    C=taxi(TXL,0,0); w=person((0,0,0),0,WALEED_CUT,'smile',name='waleed'); dr=person((0,0,0),0,DRIVER,'flat',name='driver'); reg(w,dr)
    walker=person((0,0,0),0,dad(55),'flat',name='walker'); cyc=person((0,0,0),0,dad(57),'flat',name='cyclist'); bk=bike(0,0,'#16171C'); reg(walker,cyc)
    def sit_in(H,key,t):
        p=seat_world(C,key); seatH(H,p.x,p.y,math.degrees(C['root'].rotation_euler[2])+180,sh=C['seat_h']); blink(H,t)
    def upd(t):
        q=ease(t/DUR); OWNER[0]=None; KEEP[0]=None
        for e in LIT: lit_set(e,True)
        if view=='cab':      # twenty km/h: an old man on foot overtakes the taxi; so does a cyclist
            cy=5.5*t; C['root'].location=(TXL,cy,0)
            walk_path(walker,[(RX-4.4,cy-3.0),(RX-4.4,cy+12)],t,0,DUR*1.5,step=.6,arm=20); blink(walker,t); face(walker,mouth='smirk')
            by=cy-6+9.5*t; bk.location=(RX-.4,by,0); bk.rotation_euler=(0,0,0); seatH(cyc,RX-.4,by-.2,180,sh=.85); arms(cyc,-70,0,-10,-70,0,10); blink(cyc,t); face(cyc,mouth='grin'); look_at(cyc,headpos(w),.6)
            sit_in(dr,'drv',t); sit_in(w,'back',t); arms(dr,-60,0,-8,-60,0,8); face(w,mouth='O',eyes=1.2); look_at(w,headpos(walker),.6); arms(w,-50,0,-8,-50,0,8)
            _camset((RX+1.6,cy+L(-3.0,1.0,q),1.4),(TXL,cy+1.5,1.2),L(18,20,q),5,focus=(TXL,cy,1.4))
        elif view=='tez':    # "Bhai, thora tez?" — "Tez? Petrol muft aunda ae?"
            cy=40+5.5*t; C['root'].location=(TXL,cy,0); bk.location=(0,0,-9); walker['root'].location=(0,0,-9); cyc['root'].location=(0,0,-9)
            sit_in(dr,'drv',t); sit_in(w,'back',t); arms(w,-50,0,-8,-50,0,8); arms(dr,-60,0,-8,-60,0,8)
            if t<wl(178,KEY): talk(w,t,175,177,KEY,rest='flat',shapes=('o','flat','O','flat')); face(w,eyes=1.1,brow=.08); arms(w,-50,0,-8,-90,0,30); face(dr,mouth='flat')
            else: talk(dr,t,178,183,KEY,rest='frown',shapes=('O','frown','o','frown')); dr['head'].rotation_euler=(0,0,R(150*ease((t-wl(178,KEY))/.4)/2)); face(dr,eyes=1.1,brow=-.1); face(w,mouth='O')
            hw=Vector(headpos(w)); _camset(tuple(Vector(C['root'].location)+Vector((.35,.95,1.85))),(hw.x+.25,hw.y,hw.z-.15),L(16,18,q),3,focus=tuple(hw))
        else:                # the cab stops at every light switch. The driver gets out... and turns each one off.
            C['root'].location=(TXL,30,0); bk.location=(0,0,-9); walker['root'].location=(0,0,-9); cyc['root'].location=(0,0,-9)
            sit_in(w,'back',t); arms(w,-50,0,-8,-50,0,8); look_at(w,(RX-4.1,34,1.4),.6); face(w,mouth='O',eyes=1.3)
            poles=sorted([e for e in LIT if 'lamp' in e and e['s']<0 and e['y']>=33],key=lambda e:e['y'])
            per=DUR/ max(1,len(poles[:4])+.6)
            # driver walks pole to pole on the left kerb flipping switches; shop lights on that stretch die with them
            k_=min(len(poles[:4])-1,int(t/per)); e=poles[k_]; tt=t-k_*per
            px,py=e['pole']; prev=(TXL-1.0,31.5) if k_==0 else poles[k_-1]['pole']; prev=(prev[0]+.45,prev[1]+.2) if k_ else prev
            if tt<per*.55: walk_path(dr,[prev,(px+.45,py+.2)],tt,0,per*.55,step=.55,arm=16)
            else: standH(dr,px+.45,py+.2,270,t); arm_reach(dr,1,(px+.24,py,1.38))
            blink(dr,t); face(dr,mouth='flat',eyes=.9)
            for j,ee in enumerate(poles[:4]):
                off=(j<k_) or (j==k_ and tt>per*.75)
                lit_set(ee,not off)
                for sh_ in LIT:
                    if 'win' in sh_ and sh_['s']<0 and abs(sh_['y']-ee['y'])<3.0: lit_set(sh_,not off)
            hd_=headpos(dr); _camset((RX-1.9,hd_[1]-4.6,1.9),(RX-3.5,hd_[1]+1.5,1.5),L(19,20,q),5,focus=hd_)
        hide_block()
    return dict(upd=upd)
for v in ('cab','tez','switch'): SHOTS['N_'+v]=(lambda v=v: SH_N(v))
# ============================================================ H. HOME — the real Abbu
def SH_H(view):
    KEY='H_'+view; D=home(); B.done('hm'); setup_interior('evening',(HX,0,3.0),res=PCT,samples=SAMPLES,shadow_dist=10); bpy.context.scene.view_settings.exposure=-.35
    w=person((0,0,0),0,WALEED_CUT,'smile',name='waleed'); ab=person((0,0,0),0,ABBUR,'smile',name='abbu'); reg(w,ab)
    ph,scr=phone_obj('ph_pizza'); sp=specs_obj(); pz=pizza_obj()
    def upd(t):
        q=ease(t/DUR); OWNER[0]=None; KEEP[0]=None; sp.location=(0,0,-9); pz.location=(0,0,-9)
        sx,sy,srz,ssh=D['sofa']; seatH(ab,sx-.2,sy,srz,sh=ssh); blink(ab,t)
        mask=[True]*4
        if view in ('home','abbu','pizza','stare'):
            phone_in_hand(ab,ph,up=1.7,face_dist=.45,two=False); arms(ab,-40,0,-10,None or -40,0,10) if False else None
            if view=='home':   # exhausted, he walks in — and there's his real Abbu
                walk_path(w,[(HX+.2,-3.8),(HX+.2,-1.3)],t,0,DUR*.7,step=.42,arm=8,mood=-1) if t<DUR*.7 else standH(w,HX+.2,-1.3,180,t); blink(w,t)
                w['head'].rotation_euler=(R(12),0,0) if t<DUR*.7 else (0,0,0); face(w,mouth='frown' if t<DUR*.7 else 'O',eyes=.6 if t<DUR*.7 else 1.3)
                face(ab,mouth='smile')
                _camset((L(HX-1.4,HX-1.1,q),L(2.0,1.7,q),1.75),(HX+.2,L(-3.2,-1.6,q),1.35),L(20,22,q),4,focus=headpos(w))
            elif view=='abbu': # AC on. Four lights on. Phone in hand... ordering pizza.
                standH(w,HX+.2,-1.3,180,t); blink(w,t); face(ab,mouth='grin',eyes=1.0)
                a=0 if t<wl(217,KEY) else (1 if t<wl(220,KEY) else 2)
                if a==0: _camset((HX+.9,.6,1.9),(HX,2.65,2.42),L(26,28,q),5,focus=(HX,2.65,2.42))
                elif a==1: _camset((HX+.6,-1.9,1.6),(HX-.1,1.8,1.5),L(17,18,q),6,focus=headpos(ab))
                else: OWNER[0]=ab; insert_cam(ph,L(24,28,q),.24)
            elif view=='pizza':# "Aa ja puttar. Pizza mangwaya ae. Kade kade chalda ae."
                standH(w,HX+.2,-1.3,180,t); blink(w,t); face(w,mouth='flat',eyes=.9)
                talk(ab,t,224,233,KEY,rest='grin',shapes=('o','grin','O','smile')); face(ab,eyes=1.0,brow=.05); arms(ab,-20,0,-8,-110+25*math.sin(t*6),0,-10) if t<wl(227,KEY) else None
                KEEP[0]=[ab]; front_cam(ab,2.0,L(24,26,q),ang=-15,dz=.2)
            else:              # Waleed stares. Something inside him moves.
                standH(w,HX+.2,-1.3,180,t); blink(w,t); face(w,mouth='flat',eyes=L(1.0,.55,ease((t-wl(245,KEY))/1.0)),brow=-.1*ease((t-wl(245,KEY))/1.0))
                tg_=(HX-1.6,1.4,3.0) if t<wl(239,KEY) else ((HX,2.65,2.45) if t<wl(242,KEY) else headpos(ab)); look_at(w,tg_,.9,maxpitch=40)
                KEEP[0]=[w]; front_cam(w,L(1.8,1.2,q),L(28,32,q),ang=10,dz=.05)
        elif view=='switch':   # he walks to the wall... and switches off three lights
            ph.location=tuple(hand_front(ab,1,.3,-.7,.2)); bx,by,bz=D['board']
            tg=DUR*.45
            if t<tg: walk_path(w,[(HX+.2,-1.3),(HX+1.6,-1.0),(bx-.6,by)],t,0,tg,step=.5,arm=18)
            else: standH(w,bx-.6,by,90,t)
            blink(w,t); face(w,mouth='flat',eyes=.8,brow=-.08)
            for i in range(3):
                ti=tg+.35+i*.45
                if t>tg: arm_reach(w,1,(bx,-1.0+i*.13,bz)) if t<ti+.3 else None
                if t>ti: mask[i]=False; D['sw'][i].rotation_euler=(0,R(18),0)
                else: D['sw'][i].rotation_euler=(0,R(-18),0)
            look_at(ab,headpos(w),.7); face(ab,mouth='O' if not mask[0] else 'smile',eyes=1.25)
            _camset((L(HX-1.6,HX-1.2,q),L(-2.2,-2.0,q),1.8),(HX+2.4,-.4,1.3),L(18,20,q),4,focus=headpos(w))
        elif view=='bill':     # "Abbu... bill kaun dega?"
            mask=[False,False,False,True]; ph.location=tuple(hand_front(ab,1,.3,-.7,.2))
            standH(w,HX+1.5,.2,heading_to(w,headpos(ab)),t); blink(w,t); arms(w,-8,0,-38,-8,0,38)
            talk(w,t,261,264,KEY,rest='frown',shapes=('o','frown','O','frown')); face(w,eyes=.95,brow=-.1)
            face(ab,mouth='O',eyes=1.3,brow=.1); look_at(ab,headpos(w),.7)
            KEEP[0]=[w]; front_cam(w,1.9,L(24,26,q),ang=-25,dz=.15)
        else:                  # 'end' / 'cta': specs on, hands on hips — he has become Abbu. Abbu wipes a proud tear.
            mask=[False,False,False,True]
            standH(w,HX+1.5,.2,heading_to(w,(HX+.6,-2.2,1.5)) if view=='cta' else heading_to(w,headpos(ab)),t); blink(w,t); arms(w,-8,0,-38,-8,0,38); face(w,mouth='frown',eyes=.9,brow=-.08)
            hp=Vector(headpos(w)); sp.location=tuple(hp+root_mat(w).to_3x3()@Vector((0,-.43,.05))); sp.rotation_euler=(0,0,w['root'].rotation_euler[2])
            pz.location=(HX,.9,.39); arm_reach(ab,-1,tuple(Vector(headpos(ab))+root_mat(ab).to_3x3()@Vector((-.1,-.22,.05)))) if view=='end' and t>wl(275,KEY) else None
            face(ab,mouth='grin',eyes=.8 if view=='end' else 1.0); look_at(ab,headpos(w),.6)
            if view=='end': KEEP[0]=[w,ab]; _camset((HX-2.7,L(-.6,-.4,q),1.65),(HX+.7,1.2,1.25),L(19,21,q),4,focus=headpos(w))
            else: KEEP[0]=[w,ab]; _camset((HX+.6,L(-2.4,-2.2,q),1.65),(HX+.7,1.0,1.2),L(17,18,q),4,focus=headpos(w))
        lights_set(D,mask)
        hide_block()
    return dict(upd=upd)
for v in ('home','abbu','pizza','stare','switch','bill','end','cta'): SHOTS['H_'+v]=(lambda v=v: SH_H(v))
