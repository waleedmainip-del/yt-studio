SHOTS={}
WJ=json.load(open('/home/claude/match/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('X_hook', 0), ('X_final', 13), ('X_chacha', 32), ('X_abbu', 41), ('X_bilal', 52), ('X_abbu92', 61), ('X_dada', 73), ('X_pak', 88), ('X_lastover', 104), ('X_yorker', 112), ('X_four', 129), ('X_hug', 132), ('X_dot', 147), ('X_cut', 163), ('X_ups', 182), ('X_stream', 186), ('X_buffer', 190), ('X_window', 199), ('X_radio', 209), ('X_six', 223), ('G_party', 228), ('X_replay', 239), ('G_back', 250), ('G_stubborn', 259), ('X_upscheck', 269), ('X_ammi', 281), ('X_cta', 299)]
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

# ============================================================ helpers for "Match Day — Light Gayi"
OWNER=[None]
def body_vis(H,on):
    if '_body' not in H: H['_body']=[o for o in [H['root']]+list(H['root'].children_recursive) if o.type=='MESH']
    for o in H['_body']: o.hide_render=not on
def insert_cam(ph,lens=26,dist=.18):
    H=OWNER[0]
    if H: body_vis(H,False)
    bpy.context.view_layer.update(); m=ph.matrix_world; c=m@Vector((.0,-dist,.012)); tg=m@Vector((0,0,0)); _camset(tuple(c),tuple(tg),lens,22,focus=tuple(tg))
def phone_in_hand(H,ph,up=2.0,face_dist=.55,raise_=0.0):
    h=Vector(headpos(H)); M3=root_mat(H).to_3x3(); f=M3@Vector((0,-1,0)); rt=M3@Vector((1,0,0)); p=h+f*face_dist+Vector((0,0,-.25*up+raise_))
    bpy.context.view_layer.update()
    for a in (1,-1):
        sh=H['arm'][a].matrix_world.translation; side=1 if (sh-p).dot(rt)>0 else -1
        arm_reach(H,a,tuple(p+rt*side*.075+Vector((0,0,-.05))))
    ph.location=(p.x,p.y,p.z); ph.rotation_euler=(R(-28),0,H['root'].rotation_euler[2]+R(180)); return p
def cam_close(H,side=1,dist=2.1,lens=28,ang=28,dz=.38,tz=-.25):
    h=headpos(H); rz=H['root'].rotation_euler[2]+R(side*ang); f=(math.sin(rz),-math.cos(rz))
    camset((h[0]+f[0]*dist,h[1]+f[1]*dist,h[2]+dz),(h[0],h[1],h[2]+tz),lens,2.8,focus=h)
def celebrate(H,t,k=1.0,ph=0.0):
    a=-150+18*math.sin(t*9+ph); arms(H,a*k,0,-20*k+8*math.sin(t*9+ph),a*k,0,20*k-8*math.sin(t*9+1+ph))
def point_at(H,s,target,k=1.0):
    h=Vector(headpos(H)); d=(Vector(target)-h); d.normalize(); arm_reach(H,s,tuple(h+d*.75+Vector((0,0,-.3))),k)
def bhangra(H,t,ph=0.0):
    b=abs(math.sin(t*5.5+ph)); H['root'].location[2]+=.1*b; arms(H,-160+20*math.sin(t*5.5+ph),0,-25,-160+20*math.sin(t*5.5+ph+1),0,25); H['root'].rotation_euler[2]+=R(12*math.sin(t*2.7+ph))
TVP=(TVC[0],TVC[1]-.1,TVC[2])
ALLP=[]; KEEP=[None]; NEAR=[1.5]
def front_cam(H,dist=1.7,lens=26,ang=25,dz=.3,tz=-.2):
    h=headpos(H); rz=H['root'].rotation_euler[2]+R(ang); f=(math.sin(rz),-math.cos(rz))
    _camset((h[0]+f[0]*dist,h[1]+f[1]*dist,h[2]+dz),(h[0],h[1],h[2]+tz),lens,2.8,focus=h)
def hide_block():
    cam=bpy.context.scene.camera; bpy.context.view_layer.update(); Mi=cam.matrix_world.inverted()
    fd=cam.data.dof.focus_distance if cam.data.dof.focus_distance>.1 else 3.0; lens=cam.data.lens; hx=10.125/lens; hy=18.0/lens
    for H in ALLP:
        if H is OWNER[0]: continue
        if H['root'].location.z<-5: continue
        h=Vector(headpos(H)); blk=False; K=KEEP[0]
        if K is not None and H in K: body_vis(H,True); continue
        lim=fd+.3 if K is not None else min(fd-.55,NEAR[0])
        for p in (h,h-Vector((0,0,.45)),h-Vector((0,0,.85))):
            v=Mi@p; d=-v.z
            if .05<d<lim and abs(v.x)<hx*d+.35 and abs(v.y)<hy*d+.35: blk=True;break
        body_vis(H,not blk)
def dark_fill(on):
    L_=DF[0]
    if L_ is None:
        bpy.ops.object.light_add(type='AREA',location=(0,0,RH-.2)); L_=bpy.context.object; L_.data.size=6; L_.data.color=(.55,.65,1.0); DF[0]=L_
    L_.data.energy=260 if on else 0
DF=[None]
NAMED=['abbu','chacha','phupha','dada']
CROWD_SEATS=['sofa_l','l1','l2','l3','f1','f4','c1','c2','c3','c4','c5']
def lounge_scene(mode='on',street=False):
    D=lounge(); B.done('lounge'); setup_interior('night',(0,0,RH),res=PCT,samples=SAMPLES,shadow_dist=14); bpy.context.scene.view_settings.exposure=-.2
    P={}
    P['waleed']=person((0,0,0),180,WALEED,'smile',name='waleed'); P['bilal']=person((0,0,0),180,BILAL,'grin',name='bilal')
    P['abbu']=person((0,0,0),180,ABBU,'smile',name='abbu'); P['chacha']=person((0,0,0),180,CHACHA,'grin',name='chacha'); P['phupha']=person((0,0,0),180,PHUPHA,'flat',name='phupha')
    P['dada']=person((0,0,0),180,DADA,'smile',name='dada'); P['ammi']=person((0,-9,0),0,AMMI,'smile',name='ammi')
    CR=[]; DF[0]=None
    for i,nm in enumerate(CROWD_SEATS): CR.append((nm,person((0,0,0),180,local(200+i*7,i%5==4),'grin',name='cr%d'%i)))
    for i,(x,y,hd) in enumerate(STAND): CR.append((('st',x,y,hd),person((x,y,0),hd,local(300+i*9,i==3),'grin',name='sd%d'%i)))
    ALLP[:]=list(P.values())+[h for _,h in CR]
    return D,P,CR
def seat(H,nm,t,extra=0.0):
    x,y,hd,sh=SEATS[nm]; seatH(H,x,y,hd+extra,sh=sh); blink(H,t+hash(nm)%7)
def crowd_pose(CR,t,mood='watch',k=1.0):
    for i,(nm,H) in enumerate(CR):
        if isinstance(nm,tuple): standH(H,nm[1],nm[2],nm[3],t); blink(H,t+i)
        else: seat(H,nm,t)
        if mood=='watch': arms(H,-30,0,-8,-30,0,8); look_at(H,TVP,.7); face(H,mouth='flat' if i%3 else 'O',eyes=1.0+.15*(i%2))
        elif mood=='cheer': celebrate(H,t,k,ph=i*.7); face(H,mouth='grin',eyes=1.25); H['root'].location[2]+=.06*abs(math.sin(t*9+i)) if isinstance(nm,tuple) else 0
        elif mood=='shock': arms(H,-80,0,-60,-80,0,60); face(H,mouth='O',eyes=1.35,brow=.1); look_at(H,TVP,.7)
        elif mood=='shout': celebrate(H,t,.35,ph=i); face(H,mouth='shout',eyes=1.3,brow=-.06); look_at(H,(UPS[0],UPS[1],.4),.8)
        elif mood=='dark': arms(H,-30,0,-8,-30,0,8); face(H,mouth='O',eyes=1.3); look_at(H,(0,0,3.2),.5)
        elif mood=='lean': arms(H,-45,0,-8,-45,0,8); H['root'].rotation_euler[0]=R(-10); look_at(H,TVP,.8); face(H,mouth='flat',eyes=1.2)
def family(P,t,stand_w=False):
    for nm in NAMED: seat(P[nm],nm,t)
    seat(P['bilal'],'f2',t)
    if not stand_w: seat(P['waleed'],'f3',t)
    for nm in NAMED+['bilal']: arms(P[nm],-30,0,-8,-30,0,8); look_at(P[nm],TVP,.6)
def tv(D,name,emit=1.0): set_screen(D['tv'],name,emit)
def tv_cam(q,lens=20):
    _camset((L(-.2,0,q),L(.3,.6,q),L(1.55,1.6,q)),(0,TVC[1],TVC[2]),lens,6,focus=(0,TVC[1],TVC[2]))
# ============================================================ LOUNGE shots
def SH_X(view):
    KEY='X_'+view; D,P,CR=lounge_scene(); w,bl,ab,ch,pu,dd,am=P['waleed'],P['bilal'],P['abbu'],P['chacha'],P['phupha'],P['dada'],P['ammi']
    OWNER[0]=bl if view=='buffer' else None
    tray=empty((0,0,0)); obox((0,0,0),(.32,.32,.015),M('#C9CDD6',.3,metal=.7),.01,tray)
    for k in range(10): oico((.2*math.cos(k*.63),.2*math.sin(k*.63),.03),.045,M('#C98A2A',.7,kind='fabric'),tray,sc=(1.1,1,.7))
    pk=oico((0,0,0),.045,M('#C98A2A',.7,kind='fabric'),sc=(1.1,1,.7)); tb,beads=tasbeeh_obj(); rd=radio_obj(); ph,scr=phone_obj('ph_buffer')
    lit=view not in ('cut','ups','stream','buffer','window','radio','six')
    def upd(t):
        KEEP[0]=None; NEAR[0]=1.5
        q=ease(t/DUR); D['fan'].rotation_euler[2]=t*7 if lit else t*7*max(0,1-t)
        room_lights(D,lit,tv=lit); dark_fill(not lit); bpy.context.scene.view_settings.exposure=-.2 if lit else .5; tv(D,'tv_score',1.0 if lit else 0.0); set_screen(D['ups'],'ups_dead',.6)
        for o in (tray,pk,rd,ph,tb): o.location=(9,9,-9)
        am['root'].location=(0,-9,0); family(P,t); crowd_pose(CR,t,'watch')
        for b_ in D['pak']: b_.scale=(1,1,1)
        if view=='hook':      # the packed lounge, the giant TV, everyone yelling at it
            crowd_pose(CR,t,'cheer',.6+.4*math.sin(t*2));
            for nm in NAMED: celebrate(P[nm],t,.5,ph=hash(nm)%5); face(P[nm],mouth='shout',eyes=1.2)
            _camset((L(-3.3,-3.0,q),L(-3.0,-2.6,q),L(2.9,2.7,q)),(.4,1.6,1.1),L(16,18,q),6,focus=(0,0,1))
        elif view=='final':   # reverse from the TV: everyone, then Ammi arrives with the pakoray
            k=ease((t-wl(28,KEY)+.6)/1.4); walk_path(am,[(-2.4,-4.4),(-2.4,-3.0),(-1.6,-1.3),(-1.05,-.05)],t,wl(28,KEY)-.8,wl(28,KEY)+1.2,step=.44,arm=10) if t>wl(28,KEY)-.8 else None
            if t>wl(28,KEY)-.8:
                p=Vector(headpos(am))+root_mat(am).to_3x3()@Vector((0,-.45,-.5)); tray.location=tuple(p); arm_reach(am,1,tuple(p+Vector((.2,0,-.02)))); arm_reach(am,-1,tuple(p+Vector((-.2,0,-.02))))
                for nm in NAMED: look_at(P[nm],tuple(p),.8); face(P[nm],mouth='grin',eyes=1.2)
            face(am,mouth='smile')
            _camset((L(.3,.2,q),L(2.6,2.3,q),L(2.1,1.9,q)),(L(0,-.5,q),-1.0,1.2),L(17,18,q),6,focus=headpos(ab))
        elif view=='chacha':  # "Main captain hota na…"
            talk(ch,t,32,40,KEY,rest='smirk',shapes=('o','grin','O','smirk')); face(ch,eyes=1.05,brow=.06); look_at(ch,headpos(ab),.6); arms(ch,-30,0,-8,-110+15*math.sin(t*5),0,25)
            look_at(ab,headpos(ch),.6); KEEP[0]=[ch,ab]; cam_close(ch,1,1.6,26,ang=25)
        elif view=='abbu':    # "Yeh bowler? …gali mein bhi na khilaun."
            talk(ab,t,41,51,KEY,rest='flat',shapes=('o','frown','O','flat')); face(ab,eyes=.85,brow=-.06); arms(ab,-30,0,-8,-45+10*math.sin(t*4),0,30); look_at(ab,TVP,.6)
            KEEP[0]=[ab]; cam_close(ab,-1,1.6,26,ang=20)
        elif view=='bilal':   # Bilal on the floor, turning round: "Uncle, aap ne aakhri dafa bat kab pakra tha?"
            seat(bl,'f2',t,extra=150); talk(bl,t,52,60,KEY,rest='smirk',shapes=('o','grin','O','smirk')); face(bl,eyes=1.05,brow=.07); look_at(bl,headpos(ab),.9)
            look_at(ab,headpos(bl),.8); face(ab,mouth='frown',brow=-.05)
            KEEP[0]=[bl]; front_cam(bl,1.5,L(24,26,q),ang=-30,dz=.2)
        elif view=='abbu92':  # "Unniis sau baanve mein." — chest out, finger up
            talk(ab,t,61,72,KEY,rest='smirk',shapes=('o','grin','O','smirk')); face(ab,eyes=1.0,brow=.08); arms(ab,-30,0,-8,-170,0,15); ab['root'].rotation_euler[0]=R(6); look_at(ab,headpos(bl),.6)
            KEEP[0]=[ab]; cam_close(ab,-1,1.7,26,ang=25,dz=.1)
        elif view=='dada':    # tasbeeh faster and faster… and it snaps
            k=max(0,t-wl(82,KEY)); hp=Vector(headpos(dd))+root_mat(dd).to_3x3()@Vector((.15,-.42,-.55)); tb.location=tuple(hp); tb.rotation_euler=(0,0,dd['root'].rotation_euler[2])
            arm_reach(dd,1,tuple(hp+Vector((0,0,.05)))); face(dd,mouth='frown' if k<=0 else 'O',eyes=1.0 if k<=0 else 1.4,brow=.05); look_at(dd,TVP,.8)
            for i,b_ in enumerate(beads):
                a=2*pi*i/len(beads)+(t*(2+t*1.5) if k<=0 else 0); base=Vector((.06*math.cos(a),0,-.08+.06*math.sin(a)))
                if k>0: v=Vector((math.cos(i*1.9),math.sin(i*2.7),.8+.5*math.sin(i)))*1.6; base=base+v*k+Vector((0,0,-4.9*k*k)); base.z=max(base.z,-hp.z+.02)
                b_.location=tuple(base)
            KEEP[0]=[dd]; front_cam(dd,1.6,L(26,28,q),ang=-25)
        elif view=='pak':     # top-down on the tray: hands grab, pakoray vanish, the fight continues
            n=len(D['pak']); gone=int(min(n,(t/DUR)*n*1.35))
            for i,b_ in enumerate(D['pak']): b_.scale=(0,0,0) if i<gone else (1,1,1)
            for i,H in enumerate((ab,ch,pu,bl)):
                k=(t*1.3+i*.37)%1; tgt=Vector((math.cos(i*1.6)*.15,.45+math.sin(i*1.6)*.15,.52)); arm_reach(H,1 if i%2 else -1,tuple(Vector(headpos(H)).lerp(tgt,.3+.7*math.sin(pi*k)) if k<1 else tgt))
                face(H,mouth='shout' if gone>=n else 'grin',eyes=1.2)
            _camset((.05,.2,L(2.9,2.6,q)),(0,.45,.45),L(22,26,q),6,focus=(0,.45,.45))
        elif view=='lastover':# over the crowd's shoulders: LAST OVER
            tv(D,'tv_lastover',1.0); crowd_pose(CR,t,'lean')
            for nm in NAMED+['bilal','waleed']: P[nm]['root'].rotation_euler[0]=R(-8); face(P[nm],mouth='flat',eyes=1.3)
            _camset((L(.1,.05,q),L(-1.6,-1.0,q),2.05),(0,TVC[1],TVC[2]),L(20,24,q),6,focus=(0,TVC[1],TVC[2]))
        elif view=='yorker':  # Chacha on his feet: "Ab sirf yorker!" — Waleed: "Chacha, hum batting kar rahe hain." — "To? Yorker ka josh to rakho!"
            standH(ch,.55,-.15,heading_to(ch,TVP) if t<wl(117,KEY) else heading_to(ch,headpos(w)),t); blink(ch,t)
            standH(w,1.55,.95,heading_to(w,headpos(ch)),t); blink(w,t)
            if t<wl(117,KEY): talk(ch,t,112,116,KEY,rest='shout',shapes=('shout','O','shout','O')); celebrate(ch,t,.7); face(ch,eyes=1.3,brow=-.08)
            elif t<wl(123,KEY): talk(w,t,117,122,KEY,rest='flat',shapes=('o','flat','O','flat')); face(w,eyes=.9,brow=.06); face(ch,mouth='O'); arms(ch,-90,0,-40,-90,0,40)
            else: talk(ch,t,123,128,KEY,rest='shout',shapes=('shout','O','shout','O')); point_at(ch,1,headpos(w)); face(ch,eyes=1.3,brow=-.1); face(w,mouth='flat',eyes=.8)
            KEEP[0]=[ch,w]; _camset((L(-.7,-.5,q),L(1.8,1.6,q),1.65),((.55+1.55)/2,.4,1.4),L(19,21,q),4,focus=headpos(ch))
        elif view=='four':    # FOUR! the room explodes
            tv(D,'tv_four',1.1); crowd_pose(CR,t,'cheer')
            for nm in NAMED+['bilal','waleed']: celebrate(P[nm],t,1.0,ph=hash(nm)%5); face(P[nm],mouth='grin',eyes=1.3)
            NEAR[0]=2.3; _camset((L(-.3,.3,q),2.95,2.05),(0,-1.0,1.05),L(16,17,q),6,focus=(0,-.6,1.1))
        elif view=='hug':     # Chacha hugs Abbu… Abbu's pakora drops… silence
            tv(D,'tv_four',1.0)
            standH(ch,.25,.35,heading_to(ch,headpos(ab)),t); standH(ab,-.35,.3,heading_to(ab,headpos(ch)),t); blink(ch,t); blink(ab,t)
            hp=Vector(headpos(ab)); arm_reach(ch,1,tuple(hp+Vector((.0,.35,-.55)))); arm_reach(ch,-1,tuple(hp+Vector((0,-.35,-.55)))); face(ch,mouth='grin',eyes=1.25)
            tf=wl(140,KEY); p0=Vector(hand_w(ab,1)); arms(ab,-40,0,-10,-60,0,20)
            if t<tf: pk.location=tuple(p0+Vector((0,0,.04))); face(ab,mouth='grin')
            else: k=t-tf; pk.location=(p0.x,p0.y,max(.05,p0.z-4.9*k*k*.5)); pk.rotation_euler=(k*6,k*4,0); face(ab,mouth='O',eyes=1.35)
            if t>wl(145,KEY): crowd_pose(CR,t,'shock');
            for nm in ('phupha','dada'): look_at(P[nm],tuple(pk.location),.8) if t>tf else None
            _camset((L(-.2,0,q),L(2.4,2.2,q),L(1.6,1.4,q)),(-.05,.3,L(1.4,.7,ease((t-tf)/1.2) if t>tf else 0)),L(22,26,q),3,focus=tuple(pk.location) if t>tf else headpos(ch))
        elif view=='dot':     # DOT. Phupha ji slaps the TV; the TV wobbles back
            tv(D,'tv_dot',1.0); k=ease((t-.2)/1.0); walk_path(pu,[(1.4,-.3),(1.0,1.6),(.75,2.85)],t,.1,1.3,step=.45,arm=16) if t<1.3 else standH(pu,.75,2.85,180,t); blink(pu,t)
            sl=wl(155,KEY); s_=max(0,t-sl)
            if s_>0: arm_reach(pu,-1,(.55,TVC[1]-.12,TVC[2]+.1*math.cos(min(1,s_*6)*pi))); face(pu,mouth='strain',eyes=1.1,brow=-.08)
            wob=R(4)*math.exp(-3*max(0,t-sl-.1))*math.sin(18*max(0,t-sl-.1)) if t>sl+.1 else 0; D['tv'].rotation_euler=(0,wob,0)
            for nm in ('abbu','chacha'): face(P[nm],mouth='frown',eyes=1.0)
            _camset((L(-1.3,-1.1,q),L(1.3,1.5,q),1.8),(.3,TVC[1],1.6),L(19,21,q),4,focus=headpos(pu))
        elif view in ('cut','ups'):
            tv(D,'tv_score',0.0)
            if view=='cut':   # the light goes: a second of silence, then everyone: "UPS! UPS! UPS!"
                sh_=t>wl(179,KEY)-.1; crowd_pose(CR,t,'shout' if sh_ else 'dark')
                for nm in NAMED+['bilal','waleed']: face(P[nm],mouth='shout' if sh_ else 'O',eyes=1.35); look_at(P[nm],(UPS[0],UPS[1],.4),.8) if sh_ else None
                _camset((L(-.3,-.2,q),L(2.5,2.3,q),2.0),(0,-.8,1.1),L(17,18,q),6,focus=headpos(ab))
            else:             # UPS insert: battery 0%
                set_screen(D['ups'],'ups_dead',1.2); _camset((UPS[0]+.05,UPS[1]-1.05,.5),(UPS[0],UPS[1]-.3,.32),L(26,32,q),22,focus=(UPS[0],UPS[1]-.3,.32))
        elif view in ('stream','buffer','window'):
            tv(D,'tv_score',0.0); standH(bl,.2,.9,0,t); blink(bl,t); phone_in_hand(bl,ph,up=1.4,face_dist=.6)
            for i,H in enumerate((w,ch,ab)): standH(H,[-.5,.85,.3][i],[1.4,1.45,1.75][i],heading_to(H,tuple(ph.location)),t); look_at(H,tuple(ph.location),.8); blink(H,t)
            glow=ph.location
            if view=='stream':   # "Mobile pe stream lagao!" — everyone crowds the phone
                talk(bl,t,186,189,KEY,rest='O',shapes=('shout','O','shout','O')); face(bl,eyes=1.3)
                for H in (w,ch,ab): face(H,mouth='O',eyes=1.3)
                _camset((L(.2,.25,q),L(-1.4,-1.1,q),1.65),(.25,1.2,1.45),L(20,23,q),3,focus=headpos(bl))
            elif view=='buffer': insert_cam(ph,L(24,30,q),.2)
            else:                # noise from the next mohalla: every head turns to the window
                set_screen(scr,'ph_buffer',1.0)
                for H in (bl,w,ch,ab): look_at(H,(RMx[1],1.5,1.7),.9*ease(t/.4)); face(H,mouth='O',eyes=1.35,brow=.08)
                crowd_pose(CR,t,'dark')
                for nm,H in CR: look_at(H,(RMx[1],1.5,1.7),.9)
                _camset((L(-1.6,-1.4,q),L(-1.0,-.8,q),1.7),(1.5,1.4,1.4),L(20,22,q),4,focus=headpos(ch))
        elif view=='radio':   # Dada fetches the old radio from the almari: "Asli cricket radio pe hi hoti thi."
            tv(D,'tv_score',0.0); ax,ay=ALMARI
            if t<1.4: walk_path(dd,[(3.15,.3),(3.5,-1.0),(ax-.95,ay)],t,0,1.4,step=.38,arm=10);
            else: standH(dd,ax-.95,ay,L(90,-60,ease((t-1.4)/.6)),t)
            blink(dd,t); k=ease((t-1.2)/.5); p=Vector(headpos(dd))+root_mat(dd).to_3x3()@Vector((0,-.45,-.5)); rd.location=tuple(Vector((ax-.45,ay,1.1)).lerp(p,k)); rd.rotation_euler=(0,0,dd['root'].rotation_euler[2])
            if k>0: arm_reach(dd,1,tuple(Vector(rd.location)+Vector((.2,0,-.02)))); arm_reach(dd,-1,tuple(Vector(rd.location)+Vector((-.2,0,-.02))))
            talk(dd,t,216,222,KEY,rest='smile',shapes=('o','smile','O','smile')); face(dd,eyes=.9,brow=.05)
            crowd_pose(CR,t,'dark')
            for nm,H in CR:
                if H['root'].location.x>2.4: H['root'].location=(9,9,-9)
            KEEP[0]=[dd]; front_cam(dd,2.0,L(22,24,q),ang=-20,dz=.25)
        elif view=='six':     # the radio: "SIX!" — everyone leaps
            tv(D,'tv_score',0.0); standH(dd,.0,.7,180,t); blink(dd,t); p=Vector(headpos(dd))+root_mat(dd).to_3x3()@Vector((0,-.45,-.5)); rd.location=tuple(p); rd.rotation_euler=(0,0,dd['root'].rotation_euler[2])
            arm_reach(dd,1,tuple(p+Vector((.2,0,-.02)))); arm_reach(dd,-1,tuple(p+Vector((-.2,0,-.02))))
            jump=t>wl(227,KEY)-.05
            for i,H in enumerate((ch,ab,bl,w)):
                standH(H,[-.75,.75,-1.2,1.2][i],[.35,.35,.95,.95][i],heading_to(H,tuple(rd.location)),t); blink(H,t)
                if jump: celebrate(H,t,1.0,ph=i); H['root'].location[2]+=.15*abs(math.sin(t*8+i)); face(H,mouth='grin',eyes=1.35)
                else: look_at(H,tuple(rd.location),.8); face(H,mouth='O',eyes=1.3); arms(H,-45,0,-20,-45,0,20)
            face(dd,mouth='grin' if jump else 'O',eyes=1.2)
            KEEP[0]=[dd,ch,ab,bl,w]; _camset((L(.1,0,q),L(3.0,2.8,q),2.2),(0,.6,1.05),L(19,21,q),3,focus=tuple(rd.location))
        elif view=='replay':  # light back: the replay — CAUGHT
            tv(D,'tv_caught',1.1); crowd_pose(CR,t,'shock')
            for nm in NAMED+['bilal','waleed']: face(P[nm],mouth='O',eyes=1.35,brow=.1)
            if t<.35: room_lights(D,False); tv(D,'tv_caught',0.0)
            _camset((L(.15,.05,q),L(-1.6,-.9,q),1.75),(0,TVC[1],TVC[2]-.15),L(19,24,q),6,focus=(0,TVC[1],TVC[2]))
        elif view=='upscheck':# late night: Waleed checks the UPS — battery full, plug out
            for nm,H in CR: H['root'].location=(9,9,-9)
            for nm in NAMED+['bilal']: P[nm]['root'].location=(9,9,-9)
            room_lights(D,True,tv=False); tv(D,'tv_score',0.0); set_screen(D['ups'],'ups_full',1.0)
            k=ease(t/1.0); standH(w,UPS[0]-.65,UPS[1]-.75,L(150,120,k),t); w['root'].location[2]-=.35*ease((t-.6)/.5); blink(w,t)
            look_at(w,(UPS[0]+.5,RMy[1]-.16,.45) if t>wl(278,KEY) else (UPS[0]-.18,UPS[1],.3),.9); arm_reach(w,1,(UPS[0]+.42,RMy[1]-.2,.45)) if t>wl(278,KEY) else arms(w,-30,0,-8,-30,0,8)
            D['plug'].location=(UPS[0]+.5,RMy[1]-.32,.06); D['plug'].rotation_euler=(R(80),0,0)
            face(w,mouth='O' if t>wl(278,KEY) else 'flat',eyes=1.3 if t>wl(278,KEY) else 1.0)
            _camset((L(3.9,3.8,q),L(.9,1.1,q),1.5),(1.95,2.7,.7),L(20,26,q),3,focus=(UPS[0],UPS[1],.4))
        else:                 # 'ammi' / 'cta': Ammi on the sofa with the remote, her 9 o'clock drama on
            for nm,H in CR: H['root'].location=(9,9,-9)
            for nm in NAMED+['bilal']: P[nm]['root'].location=(9,9,-9)
            room_lights(D,True); tv(D,'tv_drama',1.0); D['plug'].location=(UPS[0]+.5,RMy[1]-.32,.06); D['plug'].rotation_euler=(R(80),0,0)
            seat(am,'abbu',t); arms(am,-40,0,-10,-60,0,20); look_at(am,TVP,.6); standH(w,1.4,.6,heading_to(w,headpos(am)),t); blink(w,t)
            if view=='ammi':
                if t<wl(288,KEY): talk(w,t,281,287,KEY,rest='shout',shapes=('shout','O','shout','O')); celebrate(w,t,.45); face(w,eyes=1.35,brow=-.08); face(am,mouth='flat')
                else: talk(am,t,288,298,KEY,rest='smile',shapes=('o','smile','o','flat')); face(am,eyes=.85,brow=.03); arms(w,-80,0,-60,-80,0,60); face(w,mouth='O',eyes=1.3)
                camset((L(-1.2,-1.0,q),L(1.9,1.7,q),1.6),((headpos(am)[0]+headpos(w)[0])/2,-.1,1.2),L(19,21,q),4,focus=headpos(am))
            else:
                hw=Vector(headpos(w)); arm_reach(w,1,tuple(hw+root_mat(w).to_3x3()@Vector((.05,-.2,-.02)))); w['head'].rotation_euler[0]=R(15); face(w,mouth='frown',eyes=.6)
                face(am,mouth='smile',eyes=.95); seat(dd,'dada',t); dd['head'].rotation_euler=(R(25),0,R(15)); face(dd,mouth='o',eyes=.1)
                _camset((L(-.2,-.3,q),L(2.6,2.4,q),1.9),(.4,-.3,1.1),L(17,18,q),6,focus=headpos(am))
    def upd2(t): upd(t); hide_block()
    return dict(upd=upd2)
for v in ('hook','final','chacha','abbu','bilal','abbu92','dada','pak','lastover','yorker','four','hug','dot','cut','ups','stream','buffer','window','radio','six','replay','upscheck','ammi','cta'): SHOTS['X_'+v]=(lambda v=v: SH_X(v))
# ============================================================ THE GALI: dhol, bhangra, mithai — then the mithai goes back
def SH_G(view):
    KEY='G_'+view; gali(); B.done('gali'); setup_interior('night',(GX,0,7),res=PCT,samples=SAMPLES,shadow_dist=25); bpy.context.scene.view_settings.exposure=.2
    ch=person((GX+.6,-.4,0),0,CHACHA,'grin',name='chacha'); dh=person((GX-1.6,.6,0),0,DHOLI,'grin',name='dholi'); bl=person((GX-.4,1.4,0),0,BILAL,'grin',name='bilal'); w=person((GX+1.6,1.2,0),0,WALEED,'grin',name='waleed')
    rnd=random.Random(12); specs=[(GX+rnd.uniform(-6,6),rnd.uniform(-2.8,3.0),rnd.uniform(-30,30)) for _ in range(16)]
    cr=crowd(specs,seed0=77); kid=person((GX+1.5,-1.1,0),180,local(91,True),'grin',name='kid')
    ALLP[:]=cr+[kid,bl,w,dh,ch]; OWNER[0]=None
    dhol=dhol_obj(); st1=stick_obj(); st2=stick_obj(); box=mithai_obj(); sw=mithai_obj(); sw.scale=(.35,.35,.6)
    def upd(t):
        q=ease(t/DUR); stop=view!='party'
        for i,H in enumerate(cr):
            standH(H,specs[i][0],specs[i][1],specs[i][2],t); blink(H,t+i)
            if not stop: bhangra(H,t,i*.9); face(H,mouth='grin',eyes=1.2)
            else: arms(H,-25,0,-8,-25,0,8); face(H,mouth='flat',eyes=.9); look_at(H,headpos(ch),.5)
        standH(dh,GX-1.6,.6,10,t); blink(dh,t); hp=Vector(headpos(dh)); M3=root_mat(dh).to_3x3(); dhol.location=tuple(hp+M3@Vector((0,-.38,-1.05))); dhol.rotation_euler=(0,0,dh['root'].rotation_euler[2])
        beat=0 if stop else abs(math.sin(t*9))
        for s,st in ((1,st1),(-1,st2)): p=Vector(dhol.location)+M3@Vector((s*.3,-.1,.12+.15*beat)); arm_reach(dh,s,tuple(p)); st.location=tuple(p); st.rotation_euler=(R(70),0,dh['root'].rotation_euler[2])
        face(dh,mouth='grin' if not stop else 'flat',eyes=1.1); dh['root'].location[2]+=.03*beat
        standH(bl,GX-.4,1.4,0,t); standH(w,GX+1.6,1.2,-10,t); blink(bl,t); blink(w,t)
        standH(kid,GX+1.4,-1.15,heading_to(kid,headpos(ch)),t); blink(kid,t)
        if view=='party':     # dhol, bhangra, Chacha hands out mithai
            bhangra(bl,t,.4); bhangra(w,t,1.3); face(bl,mouth='grin'); face(w,mouth='grin')
            standH(ch,GX+.6,-.4,heading_to(ch,headpos(kid)),t); blink(ch,t); p=Vector(headpos(ch))+root_mat(ch).to_3x3()@Vector((0,-.45,-.5)); box.location=tuple(p); arm_reach(ch,-1,tuple(p+Vector((-.12,0,-.02))))
            k=(t*.8)%1; hand=Vector(p).lerp(Vector(headpos(kid))+Vector((0,0,-.5)),math.sin(pi*k)); arm_reach(ch,1,tuple(hand)); sw.location=tuple(hand+Vector((0,0,.03))); face(ch,mouth='grin',eyes=1.2)
            arm_reach(kid,1,tuple(Vector(headpos(kid))+root_mat(kid).to_3x3()@Vector((0,-.4,-.45)))); face(kid,mouth='grin',eyes=1.2)
            _camset((L(GX-3.6,GX-3.0,q),L(-3.6,-3.2,q),1.9),(GX,.3,1.3),L(17,19,q),6,focus=headpos(ch))
        elif view=='back':    # the dhol stops; Chacha takes the mithai back from the kid
            standH(ch,GX+.6,-.4,heading_to(ch,headpos(kid)),t); blink(ch,t); p=Vector(headpos(ch))+root_mat(ch).to_3x3()@Vector((0,-.45,-.5)); box.location=tuple(p); arm_reach(ch,-1,tuple(p+Vector((-.12,0,-.02))))
            k=ease((t-.6)/1.2); kh=Vector(headpos(kid))+Vector((0,0,-.5)); hand=kh.lerp(p,k); arm_reach(ch,1,tuple(hand)); sw.location=tuple(hand+Vector((0,0,.03))); arm_reach(kid,1,tuple(kh if k<.3 else kh+Vector((0,.1,0))))
            face(ch,mouth='flat',eyes=.9,brow=-.05); face(kid,mouth='frown' if k>.5 else 'O',eyes=1.2); face(bl,mouth='flat'); face(w,mouth='flat')
            cam_close(ch,1,2.2,24,ang=35,dz=.0)
        else:                 # 'stubborn': "Main ne pehle hi kaha tha. Yorker daalna chahiye tha."
            box.location=(9,9,-9); sw.location=(9,9,-9); standH(ch,GX+.6,-.4,-15,t); blink(ch,t); arms(ch,-55,0,-55,-55,0,55)
            talk(ch,t,259,268,KEY,rest='smirk',shapes=('o','frown','O','smirk')); face(ch,eyes=.85,brow=-.08); ch['head'].rotation_euler[1]=R(-8)
            cam_close(ch,-1,1.7,26,ang=15)
    def upd2(t): upd(t); hide_block()
    return dict(upd=upd2)
for v in ('party','back','stubborn'): SHOTS['G_'+v]=(lambda v=v: SH_G(v))
