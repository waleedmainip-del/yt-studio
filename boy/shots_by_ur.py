SHOTS={}
WJ=json.load(open('/home/claude/boy/audio_ur/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('A_open', 0), ('A_two', 11), ('A_today', 21), ('A_clock', 30), ('A_ammi', 40), ('A_five', 47), ('A_ramzan', 51), ('A_pull', 60), ('B_wake', 67), ('B_insta', 82), ('B_later', 86), ('B_kamre', 89), ('B_imp', 95), ('B_kya', 103), ('B_research', 104), ('B_cat', 105), ('C_enter', 116), ('C_bottles', 127), ('C_charger', 131), ('C_godaam', 138), ('C_please', 145), ('C_shirt', 160), ('C_teen', 165), ('C_decor', 173), ('D_lie', 180), ('D_dream', 191), ('D_calls', 204), ('D_bro', 209), ('D_unavail', 220), ('D_kal', 226), ('D_ups', 235), ('E_arrive', 242), ('E_fix', 247), ('E_beta', 263), ('E_career', 270), ('E_mash', 288), ('E_sus', 292), ('E_blanket', 300), ('F_night', 311), ('F_promise', 331), ('F_alarm', 345), ('G_morning', 353), ('G_eye', 361), ('G_monday', 375), ('G_life', 378), ('G_legend', 391), ('G_five', 395)]
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
# ============================================================ helpers for this film
HIP=(-1.35,1.25); SITB=(-2.05,.62); DOORP=(2.0,-2.3); NIGHT_PH=(-2.62,0.0,.62)
def room(night=False,clock=(11,47)):
    D=bedroom(night=night); gaming_chair(CHAIR[0],CHAIR[1],0); B.done('room')
    setup_interior('night' if night else 'day',(0,0,3.4),res=PCT,samples=SAMPLES,shadow_dist=12); bpy.context.scene.view_settings.exposure=(-.2 if night else -.7)
    set_clock(D,*clock); return D
def fan_spin(D,t): D['fan'].rotation_euler[2]=t*7.5
def door_set(D,k): D['door'].rotation_euler[2]=R(92*ease(k))
def ammi_walk_in(H,t,t0,t1,to=(2.0,-1.7)):
    walk_path(H,[(2.0,-3.5),(2.0,-2.6),to],t,t0,t1,step=.46,arm=16,ease_in=.1,ease_out_=.2)
def hold_chappal(H,o,s=1): p=hand_w(H,s); o.location=(p.x,p.y,p.z+.02); o.rotation_euler=(R(80),0,H['root'].rotation_euler[2])
def mumble(H,t,a,b,key): talk(H,t,a,b,key,rest='flat',rate=5,shapes=('o','flat','o'))
def phone_in_hand(H,ph,s=1,up=1.0,face_dist=.5):
    """hold the phone in front of the face, screen toward the eyes"""
    body_vis(H,True); h=Vector(headpos(H)); f=root_mat(H).to_3x3()@Vector((0,-1,0)); p=h+f*face_dist+Vector((0,0,-.25*up))
    arm_reach(H,s,(p.x,p.y,p.z-.06)); arm_reach(H,-s,(p.x,p.y,p.z-.08)); ph.location=(p.x,p.y,p.z); ph.rotation_euler=(R(-12),0,H['root'].rotation_euler[2]+R(180)); return p
def phone_lying(H,ph,t):
    """lying on the back holding the phone up over the face"""
    h=Vector(headpos(H)); p=h+Vector((.08,0,.42)); arm_reach(H,1,(p.x+.05,p.y-.05,p.z-.05)); arm_reach(H,-1,(p.x+.05,p.y+.05,p.z-.05)); ph.location=(p.x,p.y,p.z); ph.rotation_euler=(R(90),0,R(90)); return p
OWNER=[None]
def body_vis(H,on):
    if '_body' not in H:
        H['_body']=[o for o in [H['root']]+list(H['root'].children_recursive) if o.type=='MESH']
    for o in H['_body']: o.hide_render=not on
def insert_cam(ph,dist=.22,lens=26,side=0.08):
    """over-the-shoulder look at the phone screen"""
    H=OWNER[0]; body_vis(H,False); bpy.context.view_layer.update(); m=ph.matrix_world; c=m@Vector((.0,-.18,.015)); tg=m@Vector((0,0,0)); _camset(tuple(c),tuple(tg),lens,1.4,focus=tuple(tg))
def lie_insert(ph,hw):
    p=Vector(ph.location); c=Vector(hw)+Vector((.42,-.22,.05)); _camset(tuple(c),tuple(p),26,1.4,focus=tuple(p))
def cycle_screen(sc,names,t,fps=2.0): set_screen(sc,names[int(t*fps)%len(names)])
def cam_close(H,side=1,dist=2.1,lens=28,ang=28,dz=.38,tz=-.25):
    """camera in front of the character (by body heading), slightly to one side; walls handled by safe camset"""
    h=headpos(H); rz=H['root'].rotation_euler[2]+R(side*ang); f=(math.sin(rz),-math.cos(rz))
    camset((h[0]+f[0]*dist,h[1]+f[1]*dist,h[2]+dz),(h[0],h[1],h[2]+tz),lens,2.8,focus=h)
def cam_lying(hw,dist=1.0,lens=28,side=.55):
    """from the foot side, above: face reads upright"""
    _camset((hw[0]+.95*dist,hw[1]-.18,hw[2]+1.05*dist),(hw[0]+.12,hw[1],hw[2]-.05),lens,2.8,focus=hw)
# ============================================================ 1. THE MORNING LIE
def SH_A(view):
    KEY='A_'+view; D=room(); w=person((0,0,0),0,WALEED,'flat',name='waleed'); dr=Drape(-2.9,-.1,.15,2.65,bed=BED)
    am=person((2.0,-3.5,0),180,AMMI,'frown',name='ammi'); ch=chappal(); ph,scr=phone_obj('scr_lock'); ph.location=(NIGHT_PH[0],NIGHT_PH[1],NIGHT_PH[2]+.008); ph.rotation_euler=(R(-90),0,R(180))
    def upd(t):
        fan_spin(D,t); lie(w,HIP[0],HIP[1],BED['top']); blink(w,t); face(w,mouth='flat',eyes=.0); q=ease(t/DUR)
        edge=-1.85
        ammi_in=view in ('ammi','five','ramzan','pull')
        if ammi_in:
            if view=='ammi': ammi_walk_in(am,t,.05,1.0); door_set(D,(t)/.5)
            else: standH(am,2.0,-1.7,180,t); door_set(D,1)
            am['root'].rotation_euler[2]=R(heading_to(am,(HIP[0]-.9,HIP[1],0))) if view!='ammi' or t>1.0 else am['root'].rotation_euler[2]
            blink(am,t); look_at(am,headpos(w)); HIPS(am); hold_chappal(am,ch,1)
        else: am['root'].location=(9,-9,0); ch.location=(9,-9,0); door_set(D,0)
        hw=headpos(w); ha=headpos(am)
        if view=='open':
            dr.update(edge); _camset((L(2.3,1.6,q),L(-2.1,-1.5,q),L(2.3,2.0,q)),(-1.0,.9,L(1.2,1.0,q)),20,6)
        elif view=='two':
            dr.update(edge); _camset((L(-1.0,-1.3,q),L(.6,1.0,q),1.95),(-1.7,2.5,2.15),L(30,38,q),4,focus=(-1.7,2.49,2.15))
        elif view=='today':
            dr.update(edge); face(w,mouth='o' if int(t*1.5)%2 else 'flat',eyes=0); w['head'].rotation_euler[2]=R(8)*math.sin(t*1.2)
            cam_lying(hw,L(1.1,.95,q))
        elif view=='clock':
            dr.update(edge); k=t*1.4; ph.location=(NIGHT_PH[0]+.004*math.sin(t*60),NIGHT_PH[1],NIGHT_PH[2]+.008)
            c=Vector(ph.location)+Vector((.3,-.2,.28)); _camset(tuple(c),tuple(ph.location),30,1.5,focus=tuple(ph.location))
        elif view=='ammi':
            dr.update(edge); talk(am,t,40,46,KEY,rest='shout',shapes=('shout','O','shout','O')); face(am,brow=-.06,brow_r=22,eyes=1.25)
            _camset((L(-.3,-.1,q),L(.7,.5,q),2.05),(2.0,-1.9,1.6),22,4,focus=ha)
        elif view=='five':
            dr.update(edge); mumble(w,t,47,50,KEY); face(w,eyes=.0,brow=.02); w['head'].rotation_euler[2]=R(-15)
            cam_lying(hw,1.0)
        elif view=='ramzan':
            dr.update(edge); talk(am,t,51,59,KEY,rest='frown',shapes=('shout','O','o','shout')); face(am,brow=-.05,brow_r=20,eyes=1.15)
            p=hand_w(am,1); am['arm'][1].rotation_euler=(R(-110+25*math.sin(t*7)),0,R(-20)); hold_chappal(am,ch,1)
            camset((L(.7,.8,q),L(-.4,-.6,q),1.75),(2.0,-1.75,1.8),26,3,focus=ha)
        else:   # pull the blanket over the head
            k=ease((t-.3)/1.0); e=L(-1.85,-2.95,k); hh=Vector(hw); pull=Vector((L(-1.7,-2.4,k),HIP[1],BED['top']+.32))
            arm_reach(w,1,(pull.x,pull.y-.18,pull.z)); arm_reach(w,-1,(pull.x,pull.y+.18,pull.z)); face(w,mouth='frown',eyes=0)
            dr.update(e); look_at(am,hw); face(am,mouth='O',eyes=1.2)
            _camset((-.6,-.9,2.1),(-1.9,1.2,.9),26,4,focus=(-1.9,1.25,.95))
    return dict(upd=upd)
for v in ('open','two','today','clock','ammi','five','ramzan','pull'): SHOTS['A_'+v]=(lambda v=v: SH_A(v))
# ============================================================ 2. THE PHONE ADDICTION
def SH_B(view):
    KEY='B_'+view; D=room(clock=(11,49) if view in ('wake','insta') else (13,52))
    w=person((0,0,0),0,WALEED,'flat',name='waleed'); OWNER[0]=w; dr=Drape(-2.9,-.1,1.05,2.65,bed=BED); am=person((2.0,-3.5,0),180,AMMI,'frown',name='ammi'); ch=chappal()
    ph,scr=phone_obj('scr_feed0')
    for k,(xx,yy) in enumerate(((-.2,-.55),(.1,-.75),(-.45,-.8))): can(xx,yy,0) if view not in ('wake','insta') else None
    def upd(t):
        fan_spin(D,t); q=ease(t/DUR); dr.update(-2.95) if t==t else None
        seatH(w,SITB[0],SITB[1],0,sh=BED['top']); blink(w,t); breathe(w,t)
        if view=='later': set_clock(D,11+((49+t*40)//60),(49+t*40)%60)
        ammi_on=view in ('kamre','imp','kya','research','cat')
        if ammi_on:
            standH(am,2.0,-1.7,heading_to(am,(SITB[0],SITB[1],0)),t); door_set(D,1); blink(am,t); HIPS(am); hold_chappal(am,ch,1)
        else: am['root'].location=(9,-9,0); ch.location=(9,-9,0); door_set(D,0)
        hw=headpos(w); ha=headpos(am)
        if ammi_on: look_at(am,hw)
        if view=='wake':
            k=ease((t-.6)/.9); src=Vector((NIGHT_PH[0],NIGHT_PH[1],NIGHT_PH[2]+.01))
            if k<1:
                g=Vector(hand_w(w,-1)); arm_reach(w,-1,tuple(src.lerp(Vector((hw[0]-.1,hw[1]-.35,hw[2]-.3)),max(0,(t-1.0)/.5)))) ; arms(w,-20,0,8,w['arm'][-1].rotation_euler[0]*57.3,0,w['arm'][-1].rotation_euler[2]*57.3) if False else None
                look_at(w,tuple(src),.7)
                if t>1.0: carry(ph,w,-1,(0,0,.04))
                else: ph.location=tuple(src); ph.rotation_euler=(R(90),0,0)
            else: phone_in_hand(w,ph)
            face(w,mouth='flat',eyes=L(.3,.9,ease(t/1.2)))
            camset((L(-.5,-.7,q),L(-1.6,-1.8,q),1.75),(hw[0],hw[1],hw[2]-.4),26,3.5,focus=hw)
        elif view=='insta':
            phone_in_hand(w,ph); cycle_screen(scr,['scr_feed0','scr_feed1','scr_feed2','scr_feed3'],t,1.6); mumble(w,t,82,85,KEY); look_at(w,tuple(ph.location))
            if t<wl(83,KEY)+.2: cam_close(w,1,2.0,28)
            else: insert_cam(ph)
        elif view=='later':
            phone_in_hand(w,ph); cycle_screen(scr,['scr_feed2','scr_feed0','scr_feed3','scr_feed1'],t,4); face(w,mouth='flat',eyes=.65); look_at(w,tuple(ph.location))
            _camset((L(1.6,1.2,q),L(-1.4,-1.0,q),2.6),(-.5,.8,1.5),22,6)
        elif view=='kamre':
            phone_in_hand(w,ph); talk(am,t,89,94,KEY,rest='frown',shapes=('shout','O','shout')); face(am,brow=-.05,brow_r=20,eyes=1.2); am['arm'][1].rotation_euler=(R(-120+20*math.sin(t*7)),0,R(-20)); hold_chappal(am,ch,1)
            camset((.4,.3,1.95),(2.0,-1.75,1.8),30,3,focus=ha)
        elif view=='imp':
            phone_in_hand(w,ph,up=1.7); talk(w,t,95,102,KEY,rest='flat'); face(w,brow=-.02,eyes=.8); look_at(w,tuple(ph.location))
            cam_close(w,1,2.0,28)
        elif view=='kya':
            phone_in_hand(w,ph); talk(am,t,103,103,KEY,rest='frown',shapes=('shout','O')); face(am,brow=.02,brow_r=-14,eyes=.75)
            camset((.4,.3,1.95),(2.0,-1.75,1.8),36,3,focus=ha)
        elif view=='research':
            phone_in_hand(w,ph,up=1.7); talk(w,t,104,104,KEY,rest='smirk'); face(w,brow=.04,brow_r=-12,eyes=.85); look_at(w,ha,.6)
            cam_close(w,1,2.0,28)
        else:
            phone_in_hand(w,ph); k=t/DUR; set_screen(scr,'scr_cat%d'%min(5,int(k*8))); look_at(w,tuple(ph.location))
            if t<DUR*.55: insert_cam(ph)
            else: face(w,mouth='grin',eyes=.1,brow=.05); w['root'].rotation_euler[0]=R(6*math.sin(t*14)); cam_close(w,1,2.0,28)
    return dict(upd=upd)
for v in ('wake','insta','later','kamre','imp','kya','research','cat'): SHOTS['B_'+v]=(lambda v=v: SH_B(v))
# ============================================================ 3. THE ROOM
SHIRT_ON_CHAIR=(1.43,.15,1.32)
def SH_C(view):
    KEY='C_'+view; D=room(clock=(13,55)); w=person((0,0,0),0,WALEED,'flat',name='waleed'); OWNER[0]=w; dr=Drape(-2.9,-.1,1.05,2.65,bed=BED); am=person((2.0,-3.5,0),180,AMMI,'frown',name='ammi')
    ph,scr=phone_obj('scr_cat5'); sh=shirt_obj('#E8C25A')
    for k,(xx,yy) in enumerate(((-.2,-.55),(.1,-.75),(-.45,-.8))): can(xx,yy,0)
    AP=(.95,.15)
    def upd(t):
        fan_spin(D,t); q=ease(t/DUR); dr.update(-2.95); door_set(D,1)
        seatH(w,SITB[0],SITB[1],0,sh=BED['top']); blink(w,t); breathe(w,t); phone_in_hand(w,ph) if view in ('enter','bottles','charger','godaam') else rest(w,t,-30);
        if view not in ('enter','bottles','charger','godaam'): ph.location=(SITB[0]+.35,SITB[1]+.3,BED['top']+.012); ph.rotation_euler=(R(-90),0,R(190))
        hw=headpos(w)
        if view=='enter': walk_path(am,[(2.0,-2.0),(1.4,-1.1),AP],t,.2,DUR-.3,step=.46,arm=16); am['head'].rotation_euler[2]=R(35*math.sin(t*1.6))
        else: standH(am,AP[0],AP[1],heading_to(am,(SITB[0],SITB[1],0)) if view not in ('shirt','teen') else (90 if view=='shirt' else heading_to(am,(SITB[0],SITB[1],0))),t)
        blink(am,t); ha=headpos(am)
        held=view in ('shirt','teen','decor')
        if view=='shirt':
            k=ease((t-.4)/.6); src=Vector(SHIRT_ON_CHAIR); arm_reach(am,1,tuple(src+Vector((0,-.1,.2)))) if k<1 else None
            if t>1.0: am['root'].rotation_euler[2]=R(L(90,heading_to(am,(SITB[0],SITB[1],0)),ease((t-1.0)/.5))); arms(am,-80,0,-10,-80,0,10); p=(hand_w(am,1)+hand_w(am,-1))/2; sh.location=(p.x,p.y,p.z-.3); sh.rotation_euler=(0,0,am['root'].rotation_euler[2]+R(180))
            else: sh.location=SHIRT_ON_CHAIR; sh.rotation_euler=(0,R(-10),R(90))
            look_at(am,tuple(src),.8); face(am,mouth='flat',brow=.02,brow_r=12)
        elif held:
            arms(am,-80,0,-10,-80,0,10); p=(hand_w(am,1)+hand_w(am,-1))/2; sh.location=(p.x,p.y,p.z-.3); sh.rotation_euler=(0,0,am['root'].rotation_euler[2]+R(180))
        else: sh.location=SHIRT_ON_CHAIR; sh.rotation_euler=(0,R(-10),R(90))
        if view=='enter':
            face(am,mouth='O',eyes=1.25,brow=.05); look_at(w,ha,.6); face(w,mouth='flat')
            camset((L(-.4,-.9,q),L(-1.8,-2.0,q),2.3),(L(1.6,.6,q),L(-1.2,0,q),1.2),22,5,focus=ha)
        elif view=='bottles':
            _camset((L(1.75,1.85,q),L(-.75,-.55,q),1.3),(DESK['x']-.2,0,DESK['top']+.1),30,2.2,focus=(DESK['x']-.2,0,DESK['top']+.1))
        elif view=='charger':
            _camset((L(1.0,1.1,q),-1.05,L(.95,.85,q)),(CHAIR[0],CHAIR[1],.35),26,2.2,focus=(CHAIR[0],CHAIR[1],.3))
        elif view=='godaam':
            talk(am,t,138,144,KEY,rest='shout',shapes=('shout','O','shout','O')); face(am,brow=-.06,brow_r=22,eyes=1.3); arms(am,-40,0,-120+15*math.sin(t*6),-40,0,120-15*math.sin(t*6)); look_at(am,hw)
            cam_close(am,-1,2.0,28)
        elif view=='please':
            talk(w,t,145,159,KEY,rest='O'); face(w,brow=.07,brow_r=16,eyes=1.25); arms(w,-80,0,-30+10*math.sin(t*8),-80,0,30-10*math.sin(t*8)); look_at(w,ha); look_at(am,hw)
            cam_close(w,1,2.0,28)
        elif view=='shirt':
            camset((L(2.35,2.25,q),L(-.95,-.85,q),1.95),(1.0,.15,1.55),24,3,focus=ha)
        elif view=='teen':
            talk(am,t,165,172,KEY,rest='frown',shapes=('o','O','flat','o')); face(am,brow=-.03,brow_r=18,eyes=.85); look_at(am,hw)
            cam_close(am,-1,2.1,26,tz=-.4)
        else:
            talk(w,t,173,179,KEY,rest='flat'); face(w,brow=-.02,eyes=.85); look_at(w,ha); face(am,mouth='O',eyes=1.2); look_at(am,hw)
            cam_close(w,1,2.0,30)
    return dict(upd=upd)
for v in ('enter','bottles','charger','godaam','please','shirt','teen','decor'): SHOTS['C_'+v]=(lambda v=v: SH_C(v))
# ============================================================ 4. THE DREAM LIFE (+ Bilal's video call)
def SH_D(view):
    KEY='D_'+view
    if view in ('bro','kal'):
        street_corner(); B.done('street'); setup_interior('day',(SX,0,4),res=PCT,samples=SAMPLES,shadow_dist=20); bpy.context.scene.view_settings.exposure=-.6
        bl=person((SX+.1,1.3,0),0,BILAL,'grin',name='bilal'); ph,scr=phone_obj('scr_call')
        S_=walkers([([(SX-6,.0),(SX+6,-.4)],-1,12),([(SX+6,2.0),(SX-6,2.2)],-2,12)],5) if 'walkers' in globals() else []
        def upd(t):
            standH(bl,SX+.1,1.3,0,t); blink(bl,t); h=Vector(headpos(bl)); p=h+Vector((.28,-.62,-.45)); arm_reach(bl,1,(p.x,p.y+.04,p.z-.05)); ph.location=(p.x,p.y,p.z); ph.rotation_euler=(R(-10),0,R(180))
            if view=='bro': talk(bl,t,209,219,KEY,rest='grin'); face(bl,brow=.04,eyes=1.05); bl['arm'][-1].rotation_euler=(R(-40+15*math.sin(t*4)),0,R(15))
            else: talk(bl,t,226,234,KEY,rest='grin',shapes=('grin','O','grin','shout')); face(bl,eyes=.25,brow=.05); bl['root'].rotation_euler[0]=R(5*math.sin(t*12))
            for H in S_: walk_path(H,H['pts'],t,H['tt'][0],H['tt'][1],step=.5,arm=20)
            c=h+Vector((.06,-1.0,.05))+Vector((.012*math.sin(t*3.1),.0,.01*math.sin(t*4.7))); _camset(tuple(c),tuple(h+Vector((0,0,-.2))),20,4,focus=tuple(h))
        return dict(upd=upd)
    D=room(clock=(15,20)); w=person((0,0,0),0,WALEED,'flat',name='waleed'); OWNER[0]=w; dr=Drape(-2.9,-.1,.15,2.65,bed=BED); ph,scr=phone_obj('scr_car0')
    for k,(xx,yy) in enumerate(((-.2,-.55),(.1,-.75),(-.45,-.8))): can(xx,yy,0)
    PROP=(-2.3,1.3)
    def upd(t):
        fan_spin(D,t); q=ease(t/DUR); dr.update(-1.55)
        seatH(w,PROP[0],PROP[1],90,sh=BED['top']); w['root'].rotation_euler[1]=0; w['root'].rotation_euler[0]=0; blink(w,t)
        p=phone_in_hand(w,ph,up=1.7); hw=headpos(w); look_at(w,tuple(ph.location))
        if view=='lie':
            cycle_screen(scr,['scr_car0','scr_car1','scr_car2','scr_car3'],t,2.5); face(w,mouth='smile',eyes=.9)
            if t<DUR*.45: _camset((L(.3,0,q),L(-.5,-.2,q),2.2),(-1.6,1.2,1.0),22,4)
            else: insert_cam(ph)
        elif view=='dream':
            cycle_screen(scr,['scr_car1','scr_car2','scr_car3','scr_car0'],t,2.5); talk(w,t,191,203,KEY,rest='grin'); face(w,eyes=.55,brow=.05); look_at(w,(0,1.3,2.6),.7)
            cam_close(w,-1,2.0,28)
        elif view=='calls':
            set_screen(scr,'scr_call'); ph.location=(ph.location[0]+.004*math.sin(t*70),ph.location[1],ph.location[2]); face(w,mouth='o',eyes=1.15)
            insert_cam(ph) if t>.6 else cam_close(w,-1,2.0,28)
        elif view=='unavail':
            set_screen(scr,'scr_call'); talk(w,t,220,225,KEY,rest='flat'); face(w,brow=-.02,eyes=.8); cam_close(w,-1,2.0,28)
        else:
            set_screen(scr,'scr_call'); talk(w,t,235,241,KEY,rest='smirk'); face(w,brow=.03,brow_r=-10,eyes=.75); nod(w,t,6,3); cam_close(w,-1,2.0,30)
    return dict(upd=upd)
for v in ('lie','dream','calls','bro','unavail','kal','ups'): SHOTS['D_'+v]=(lambda v=v: SH_D(v))
# ============================================================ 5. THE GUESTS (drawing room)
UNP=(LX-.9,2.55); AUP=(LX+.15,2.55); WLP=(LX+2.55,.3); AMP=(LX+1.2,-1.5)
def SH_E(view):
    KEY='E_'+view; drawing_room(); B.done('dr'); setup_interior('day',(LX,0,3.4),res=PCT,samples=SAMPLES,shadow_dist=12); bpy.context.scene.view_settings.exposure=-.6
    w=person((WLP[0],WLP[1],0),-90,WALEED,'flat',name='waleed'); un=person((LX-5,-1.8,0),90,UNCLE,'smile',name='uncle'); au=person((LX-5,-1.8,0),90,AUNTY2,'smile',name='aunty'); am=person((AMP[0],AMP[1],0),0,AMMI,'smile',name='ammi')
    ph,scr=phone_obj('scr_feed1')
    def upd(t):
        q=ease(t/DUR); DRDOOR[0].rotation_euler[2]=R(-85*ease(min(1,(t+(0 if view=='arrive' else 9))/.6)))
        # Waleed on the east single sofa (seat .54) facing -x
        seatH(w,WLP[0],WLP[1],-90,sh=.54); blink(w,t)
        if view=='arrive':
            slouch=1.0; w['root'].rotation_euler[0]=R(-14); w['root'].location[2]-=.06; phone_in_hand(w,ph,face_dist=.38); look_at(w,tuple(ph.location)); face(w,mouth='flat',eyes=.7)
            for H,pts,t0 in ((un,[(LX-5,-1.8),(LX-3.0,-1.6),(LX-1.6,1.0),(UNP[0],1.9)],.2),(au,[(LX-5,-1.8),(LX-3.2,-1.7),(LX-.6,1.0),(AUP[0],1.9)],.9)): walk_path(H,pts,t,t0,t0+2.4,step=.46,arm=16)
            standH(am,AMP[0],AMP[1],heading_to(am,(LX-2,-1.8,0)),t); arms(am,-60,0,-20,-60,0,20)
            _camset((L(LX+3.2,LX+3.0,q),L(-2.8,-2.6,q),2.3),(LX-.8,.2,1.0),20,6)
            for H in (un,au,am): blink(H,t); face(H,mouth='grin')
            return
        seatH(un,UNP[0],UNP[1],0,sh=.56); seatH(au,AUP[0],AUP[1],0,sh=.56); standH(am,AMP[0],AMP[1],heading_to(am,(LX,1.5,0)),t)
        for H in (un,au,am): blink(H,t)
        rest(un,t,-30); rest(au,t,-30); arms(am,-62,0,-58,-62,0,58)
        hw=headpos(w); hu=headpos(un); ha=headpos(au); hm=headpos(am)
        if view=='fix':
            k1=ease((t-.1)/.35); k2=ease((t-.7)/.4); k3=ease((t-1.3)/.4)
            w['root'].rotation_euler[0]=R(L(-14,0,k3)); w['root'].location[2]-=.06*(1-k3)
            if k1<1: phone_in_hand(w,ph,face_dist=L(.38,.2,k1)); ph.location=(ph.location[0],ph.location[1],ph.location[2]-.5*k1)
            else: ph.location=(WLP[0]+.05,WLP[1]+.45,.56); ph.rotation_euler=(R(-90),0,R(180))
            if k1>=1 and k2<1: arm_reach(w,1,(hw[0]+.05,hw[1],hw[2]+.35)); w['head'].rotation_euler[1]=R(8*math.sin(t*12))
            elif k2>=1: arms(w,-40,0,8,-40,0,-8)
            face(w,mouth='grin' if k3>0 else 'O',eyes=1.15); look_at(w,hu,k3)
            camset((LX+.55,-1.25,1.75),(hw[0],hw[1],hw[2]-.3),28,3,focus=hw)
            return
        ph.location=(WLP[0]+.05,WLP[1]+.45,.56); ph.rotation_euler=(R(-90),0,R(180)); arms(w,-40,0,8,-40,0,-8); look_at(w,hu)
        if view=='beta':
            talk(un,t,263,269,KEY,rest='smile'); look_at(un,hw); arms(un,-30,0,8,-70,0,-30); face(un,brow=.03); look_at(au,hw,.6); face(w,mouth='smile')
            camset((LX+.6,.6,1.7),hu,32,3,focus=hu)
        elif view=='career':
            talk(w,t,270,287,KEY,rest='grin'); face(w,brow=.04,eyes=1.05); arms(w,-40,0,8,-75,0,-30+12*math.sin(t*4)); nod(w,t,3,3); look_at(un,hw); look_at(au,hw)
            camset((LX+.4,-.9,1.7),hw,32,3,focus=hw)
        elif view=='mash':
            talk(un,t,288,291,KEY,rest='grin'); look_at(un,hw); face(un,brow=.05,eyes=1.15); arms(un,-30,0,8,-110,0,-40); look_at(au,hw); face(au,mouth='grin')
            camset((LX+.6,.6,1.7),hu,30,3,focus=hu)
        elif view=='sus':
            look_at(am,hw); face(am,mouth='flat',brow=-.03,brow_r=-14,eyes=.55); am['head'].rotation_euler[1]=R(8)
            camset((LX+.45,.35,2.05),hm,30,3,focus=hm)
        else:
            look_at(am,hu); talk(am,t,300,310,KEY,rest='smirk'); face(am,brow=.03,brow_r=-12,eyes=.65); arms(am,-62,0,-58,-90,0,-30)
            look_at(un,hw); look_at(au,hw); face(un,mouth='O',eyes=1.2); face(au,mouth='o')
            if t>we(310,KEY)-.4: face(w,mouth='strain',eyes=1.25,brow=.06)
            camset((LX+.1,-.6,1.75),hm,30,3,focus=hm) if t<we(307,KEY) else camset((LX+.4,-.9,1.7),hw,32,3,focus=hw)
    return dict(upd=upd)
for v in ('arrive','fix','beta','career','mash','sus','blanket'): SHOTS['E_'+v]=(lambda v=v: SH_E(v))
# ============================================================ 6. THE MIDNIGHT PROMISE
def SH_F(view):
    KEY='F_'+view; D=room(night=True,clock=(2,30)); w=person((0,0,0),90,WALEED,'flat',name='waleed'); dr=Drape(-2.9,-.1,.15,2.65,bed=BED); cp=chips(); ph,scr=phone_obj('scr_alarm')
    for k,(xx,yy) in enumerate(((-.2,-.55),(.1,-.75),(-.45,-.8),(1.1,-.9),(1.3,.9))): can(xx,yy,0)
    kb=(DESK['x']-.15,(DESK['y0']+DESK['y1'])/2+.1,DESK['top']+.04)
    def upd(t):
        dr.update(-2.95); q=ease(t/DUR); seatH(w,CHAIR[0]+.02,CHAIR[1],90,sh=.56); blink(w,t); hw=headpos(w)
        ph.location=(kb[0]+.02,kb[1]-.55,DESK['top']+.01); ph.rotation_euler=(R(-90),0,R(-90))
        cp.location=(kb[0]+.05,kb[1]+.48,DESK['top']+.11)
        if view=='night':
            k=(t%2.2)/2.2
            arm_reach(w,1,(kb[0],kb[1]-.12,kb[2]+.01*math.sin(t*20)));
            if k<.45: arm_reach(w,-1,(kb[0],kb[1]+.12,kb[2]+.01*math.sin(t*23)))
            else:
                kk=math.sin(pi*(k-.45)/.55); src=Vector(cp.location); mouth=Vector((hw[0]+.18,hw[1],hw[2]-.2)); arm_reach(w,-1,tuple(src.lerp(mouth,kk))); face(w,mouth='O' if kk>.7 else 'flat')
            look_at(w,(DESK['x']+.1,kb[1],DESK['top']+.6)); face(w,eyes=1.15)
            _camset((L(-.6,-.2,q),L(-1.6,-1.3,q),L(2.2,1.9,q)),(1.9,.2,1.2),22,5)
        elif view=='promise':
            talk(w,t,331,344,KEY,rest='grin'); face(w,brow=.06,eyes=1.2); k=ease((t-wl(343,KEY))/.3); arms(w,-60,0,-10,-60-100*k,0,10); look_at(w,(0,.1,1.9),.6)
            w['root'].rotation_euler[2]=R(90-30*ease(t/.6))
            cam_close(w,-1,1.9,28)
        else:
            arm_reach(w,1,(ph.location[0],ph.location[1],ph.location[2]+.03)); look_at(w,tuple(ph.location)); face(w,mouth='smile',eyes=.8)
            _camset((ph.location[0]-.12,ph.location[1],ph.location[2]+.32),tuple(ph.location),34,1.5,focus=tuple(ph.location)) if t>.5 else _camset((hw[0]-1.0,hw[1]-1.1,hw[2]+.2),(kb[0],kb[1]-.4,DESK['top']+.2),30,3)
    return dict(upd=upd)
for v in ('night','promise','alarm'): SHOTS['F_'+v]=(lambda v=v: SH_F(v))
# ============================================================ ENDING
ALRM=(-2.15,.62,BED['top']+.012)
def SH_G(view):
    KEY='G_'+view; D=room(clock=(7,0)); w=person((0,0,0),0,WALEED,'flat',name='waleed'); dr=Drape(-2.9,-.1,.15,2.65,bed=BED); ph,scr=phone_obj('scr_alarm')
    for k,(xx,yy) in enumerate(((-.2,-.55),(.1,-.75),(-.45,-.8),(1.1,-.9),(1.3,.9))): can(xx,yy,0)
    def upd(t):
        fan_spin(D,t); q=ease(t/DUR); lie(w,HIP[0],HIP[1],BED['top']); blink(w,t); face(w,mouth='flat',eyes=0); hw=headpos(w)
        ph.location=ALRM; ph.rotation_euler=(R(-90),0,R(190)); ring=view in ('morning','eye')
        if view=='five': edge=-2.95
        else: edge=-1.85
        if view=='eye':
            a=wl(361,KEY); b=wl(366,KEY); c=wl(370,KEY)
            face(w,eyes=0);
            if t>a: w['lids'][0].scale[2]=0 if 'lids' in w and False else 1
            ey=.45 if a<t<c else 0; face(w,mouth='flat',eyes=ey)
            if b<t<c+.4: k=math.sin(pi*min(1,(t-b)/(c-b+.4))); arm_reach(w,1,tuple(Vector(hand_w(w,1)).lerp(Vector((ALRM[0],ALRM[1],ALRM[2]+.03)),k)))
            if t>c: ring=False; set_screen(scr,'scr_lock')
        if ring: ph.location=(ALRM[0]+.006*math.sin(t*80),ALRM[1],ALRM[2]); ph.rotation_euler=(R(-90),0,R(190+4*math.sin(t*50)))
        dr.update(edge)
        if view=='morning':
            _camset((L(-.2,-.6,q),L(-1.4,-1.0,q),1.7),(-2.0,.8,.8),26,3,focus=ALRM)
        elif view=='eye':
            _camset((hw[0]+1.0,hw[1]-1.7,hw[2]+1.0),(hw[0]+.15,hw[1]-.4,hw[2]-.1),26,3,focus=hw)
        elif view=='monday':
            mumble(w,t,375,377,KEY); face(w,eyes=0); w['head'].rotation_euler[2]=R(-12)
            cam_lying(hw,1.0,30)
        elif view=='life':
            face(w,mouth='o' if int(t*1.5)%2 else 'flat',eyes=0); _camset((L(.2,2.4,q),L(-.6,-2.2,q),L(1.6,2.6,q)),(-1.2,.9,L(1.0,1.2,q)),L(26,18,q),6)
        elif view=='legend':
            _camset((L(.6,-.6,q),L(-1.6,-.9,q),L(2.1,1.8,q)),(-1.9,1.25,.9),L(22,32,q),4)
        else:
            # under the blanket: the blanket bulges and shakes as he shouts
            dr.update(-2.95); hh=Vector(hw); w['root'].location[2]+=.04*abs(math.sin(t*9))*(1 if t<1.6 else 0)
            _camset((L(-.7,-.8,q),L(-.5,-.3,q),L(1.9,1.8,q)),(-1.9,1.25,.9),L(28,34,q),4)
    return dict(upd=upd)
for v in ('morning','eye','monday','life','legend','five'): SHOTS['G_'+v]=(lambda v=v: SH_G(v))
