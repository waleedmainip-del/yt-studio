SHOTS={}
WJ=json.load(open('/home/claude/wed/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('A_ext', 0), ('A_clothes', 14), ('A_money', 21), ('A_dance', 26), ('A_judge', 29), ('A_groom', 34), ('A_biryani', 46), ('A_welcome', 58), ('B_mirror', 63), ('B_bro', 75), ('B_relax', 82), ('B_bill', 87), ('B_abbu', 100), ('B_hamza', 106), ('B_ji', 107), ('B_adv', 109), ('B_hall', 114), ('B_acct', 118), ('B_dono', 124), ('C_full', 127), ('C_aunty', 139), ('C_salam', 145), ('C_bas', 149), ('C_height', 154), ('C_khana', 161), ('C_details', 167), ('C_spots', 176), ('C_beti', 180), ('C_freeze', 191), ('C_kal', 194), ('D_walk', 202), ('D_smile', 208), ('D_smiles', 211), ('D_natural', 213), ('D_again', 216), ('D_emo', 219), ('D_conf', 222), ('D_cand', 237), ('D_turn', 240), ('D_perfect', 243), ('D_lean', 250), ('D_400', 253), ('E_music', 267), ('E_grab', 278), ('E_chal', 281), ('E_nahi', 284), ('E_kya', 288), ('E_wild', 298), ('E_uncle', 302), ('E_karte', 312), ('E_beta', 317), ('E_move', 329), ('E_watch', 335), ('E_pro', 341), ('F_dinner', 347), ('F_reach', 355), ('F_kidhar', 361), ('F_yahan', 365), ('F_lid', 367), ('F_yeh', 376), ('F_khatam', 379), ('F_shaadi', 384), ('F_around', 388), ('F_20saal', 392), ('F_hears', 406), ('F_bro', 413), ('F_kya', 422), ('F_biryani', 423), ('F_turns', 424), ('F_mubarak', 429), ('F_camera', 439), ('F_caterer', 444), ('G_about', 449), ('G_problem', 462), ('G_abkya', 464), ('G_wallet', 466), ('G_rush', 472), ('G_kahan', 477), ('G_diya', 481), ('G_mujhe', 486), ('G_haan', 487), ('G_pockets', 493), ('G_photo', 503), ('G_last', 507), ('G_gum', 511), ('G_tension', 516), ('H_over', 524), ('H_plate', 533), ('H_finally', 540), ('H_bite', 545), ('H_beta', 553), ('H_ji', 555), ('H_shopping', 557), ('H_freeze', 564), ('H_abhi', 566), ('H_abbu', 572), ('H_payment', 576), ('H_aunty', 582), ('H_cousin', 587), ('H_down', 596), ('H_gaari', 602), ('H_kahan', 605), ('H_dubai', 606), ('Z_wedding', 607), ('Z_montage', 616), ('Z_disaster', 629), ('Z_groom', 634), ('Z_escape', 637)]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.1,3)) for k,i in _K]
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
# ============================================================ wedding helpers
def guest(seed,female=None):
    C=local(seed,female=female)
    if not C.get('waistcoat') and C.get('hairstyle')!='dupatta' and seed%3==0: C['waistcoat']=['#2B2C33','#7A1E2E','#1F3A5A','#C99A2E'][seed%4]; C['wc_trim']='#C9A24A'
    if C.get('hairstyle')=='dupatta': C['bangles']=['#E8C25A','#F4F1EA','#C21E3A'][seed%3]
    return C
TABLES=[(s*tx,ty) for s in (-1,1) for (tx,ty) in ((10.0,-6.5),(13.5,-3.0),(10.0,.5),(13.5,4.0),(10.0,-10.5),(13.5,-11.5))]
def seated_guests(n=20,seed=0,skip=()):
    r=random.Random(seed); out=[]; spots=[]
    for ti,(tx,ty) in enumerate(TABLES):
        if ti in skip: continue
        for k in range(6): a=2*pi*k/6; spots.append((tx+1.35*math.cos(a),ty+1.35*math.sin(a),tx,ty))
    r.shuffle(spots)
    for i,(x,y,tx,ty) in enumerate(spots[:n]):
        H=person((x,y,0),0,guest(300+seed*37+i*7,female=(i%2==0)),'smile',name='sg%d_%d'%(seed,i)); H['spot']=(x,y,tx,ty); H['act']=r.choice(('talk','eat','look','talk','phone')); out.append(H)
    return out
def seated_upd(G,t):
    for H in G:
        x,y,tx,ty=H['spot']; H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(heading_to(H,(tx,ty,0)))); H['z0']=0; sit(H,1.0,.56,90); blink(H,t); ph=H['seed']
        if H['act']=='talk': face(H,mouth=('o','flat','O','smile','grin')[int(t*6+ph)%5]); arms(H,-45-12*math.sin(t*4+ph),0,10,-35,0,-8); H['head'].rotation_euler[2]=R(25)*math.sin(t*.6+ph)
        elif H['act']=='eat': arms(H,-62+14*max(0,math.sin(t*2.2+ph)),0,-6,-40,0,6); face(H,mouth=('flat','o')[int(t*3+ph)%2])
        elif H['act']=='phone': arms(H,-14,0,5,-120,0,-30); face(H,mouth='smile'); H['head'].rotation_euler=(R(14),0,0)
        else: arms(H,-38,0,6,-38,0,-6); face(H,mouth='smile'); H['head'].rotation_euler[2]=R(35)*math.sin(t*.5+ph)
def standers(specs,seed=0):
    out=[]
    for i,(x,y,rz,act) in enumerate(specs):
        H=person((x,y,0),rz,guest(500+seed*17+i*5,female=(i%2==1)),'smile',name='st%d_%d'%(seed,i)); H['act']=act; H['xy']=(x,y,rz); out.append(H)
    return out
def standers_upd(G,t):
    for H in G:
        x,y,rz=H['xy']; H['z0']=0; standH(H,x,y,rz,t); blink(H,t); ph=H['seed']
        if H['act']=='talk': face(H,mouth=('o','flat','O','smile','grin')[int(t*6+ph)%5]); arms(H,-35-15*math.sin(t*4+ph),0,10,-14,0,-5)
        elif H['act']=='selfie': arms(H,-150,0,-25,-14,0,-5); face(H,mouth='grin'); H['head'].rotation_euler=(R(-8),R(8),0)
        elif H['act']=='clap': c=abs(math.sin(t*7+ph)); arms(H,-70,0,-25+25*c,-70,0,25-25*c); face(H,mouth='grin')
        elif H['act']=='dance': bhangra(H,t,ph,.7)
        elif H['act']=='stare': arms(H,-62,0,-58,-62,0,58); face(H,mouth='O',eyes=1.2)
        else: rest(H,t); face(H,mouth='smile'); H['head'].rotation_euler[2]=R(20)*math.sin(t*.6+ph)
def walkers(specs,seed=0):
    out=[]
    for i,(pts,t0,t1) in enumerate(specs):
        H=person((pts[0][0],pts[0][1],0),0,guest(800+seed*13+i*7,female=(i%2==0)),'smile',name='wk%d_%d'%(seed,i)); H['pts']=pts; H['tt']=(t0,t1); out.append(H)
    return out
def walkers_upd(G,t):
    for H in G: H['z0']=0; blink(H,t); walk_path(H,H['pts'],t,H['tt'][0],H['tt'][1],step=.52,arm=22,ease_in=.05,ease_out_=.15); face(H,mouth='smile')
def bhangra(H,t,ph=0,amp=1.0):
    w=t*6.2+ph; b=abs(math.sin(w)); H['root'].location[2]+=.07*b*amp
    arms(H,-150+22*math.sin(w),0,-38,-150+22*math.sin(w+pi),0,38); H['root'].rotation_euler[2]+=R(14*amp)*math.sin(w/2)
    H['leg'][1].rotation_euler[0]=-R(28*amp)*max(0,math.sin(w)); H['leg'][-1].rotation_euler[0]=-R(28*amp)*max(0,-math.sin(w))
    face(H,mouth='grin')
FLASH=[None]
def flash_light(loc):
    p=point(loc,0,(1,1,1),.05,shadow=False); FLASH[0]=p; return p
def flash(t,times,dur=.12,e=2500):
    v=0
    for tt in times:
        if 0<=t-tt<dur: v=max(v,1-(t-tt)/dur)
    if FLASH[0]: FLASH[0].data.energy=e*v
def hall_scene(n_seat=22,seed=0,stand=(),walk=(),dance=False,skip=()):
    D=hall(); B.done('hall'); setup_interior('night',(0,0,6.5),res=PCT,samples=SAMPLES,shadow_dist=40)
    G=seated_guests(n_seat,seed,skip); S_=standers(list(stand),seed); W_=walkers(list(walk),seed); DL=dance_lights() if dance else None
    def base(t):
        seated_upd(G,t); standers_upd(S_,t); walkers_upd(W_,t)
        if DL: DL(t)
    return base,D
def room_scene():
    fan=dressing_room(); B.done('room'); setup_interior('night',(GX,GY,3.5),res=PCT,samples=SAMPLES,shadow_dist=12)
    def base(t): fan.rotation_euler[2]=t*7.0
    return base
def on_stage(H,x,y,rz,t): H['z0']=.6; standH(H,x,y,rz,t)
def dslr_hands(H,cam_o,up=1.0):
    arms(H,-95*up,0,-28*up,-95*up,0,28*up); p=(hand_w(H,1)+hand_w(H,-1))/2; cam_o.location=(p.x,p.y,p.z+.06); cam_o.rotation_euler=(0,0,H['root'].rotation_euler[2])
# ============================================================ 1. INTRO
def SH_A(view):
    KEY='A_'+view
    if view=='ext':
        exterior(); B.done('ext'); setup_interior('night',(0,-16,7),res=PCT,samples=SAMPLES,shadow_dist=50)
        W_=walkers([([(-1.0,-29),(-.4,-15.0)],-1,9),([(1.0,-31),(.5,-15.2)],0,10),([(-5,-25),(-1.2,-18),(-.6,-15)],-.5,8),([(5.5,-26),(1.4,-18.5),(.7,-15.2)],1.0,10),([(.2,-34),(0,-16)],1.5,12)],1)
        S_=standers([(-3.2,-16.5,140,'talk'),(-2.6,-17.3,-40,'talk'),(3.0,-16.2,200,'selfie'),(4.2,-19.5,0,'talk')],1)
        def upd(t):
            walkers_upd(W_,t); standers_upd(S_,t); q=ease(t/DUR); _camset((L(.8,0,q),L(-30,-22.5,q),L(2.8,1.7,q)),(0,-14,L(4.0,2.8,q)),24,10)
        return dict(upd=upd)
    if view=='clothes':
        base,D=hall_scene(16,2,stand=[(-2.3,-9.5,90,'talk'),(-1.6,-9.5,-90,'talk')],walk=[([(-.5,-13.6),(-.4,-6)],-.5,6),([(.5,-13.8),(.6,-6.5)],.0,6.5),([(-.1,-14.2),(0,-7.5)],.6,7)])
        def upd(t):
            base(t); q=ease(t/DUR); camset((L(2.2,1.6,q),L(-5.2,-5.8,q),1.5),(0,L(-11,-9,q),1.4),28,5)
        return dict(upd=upd)
    if view=='money':
        room=room_scene(); ab=person((GX-1.4,GY-2.3,0),180,ABBU,'flat',name='abbu'); nb=notebook(ab); cash=[obox((0,0,0),(.07,.035,.004),M('#4E8C5A',.6),.002) for i in range(6)]
        def upd(t):
            room(t); ab['root'].location=(GX-1.4,GY-2.2,0); ab['root'].rotation_euler=(0,0,R(180)); ab['z0']=0; sit(ab,1.0,.64,90); blink(ab,t)
            arms(ab,-70,0,-14,-75+10*math.sin(t*9),0,14); p=hand_w(ab,-1); nb.location=(p.x,p.y-.05,p.z+.03); nb.rotation_euler=(R(-55),0,0)
            p2=hand_w(ab,1)
            for i,c_ in enumerate(cash): k=((t*2.6+i/6)%1.0); c_.location=(p2.x+.1*math.sin(i)+.0,p2.y-.1,p2.z+.05+k*.5); c_.rotation_euler=(k*6+i,k*4,i)
            ab['head'].rotation_euler=(R(18),0,R(-8)); face(ab,mouth=('o','flat')[int(t*5)%2],brow=-.03,brow_r=14,eyes=1.15)
            q=ease(t/DUR); camset((GX-1.0+L(.3,0,q),GY+L(.4,.1,q),1.7),(GX-1.4,GY-2.2,1.4),30,3.0,focus=headpos(ab))
        return dict(upd=upd)
    if view=='dance':
        base,D=hall_scene(14,3,stand=[(x,y,rz,'dance') for (x,y,rz) in ((-1.6,.2,10),(1.2,.4,-20),(-.2,2.4,180),(1.9,2.6,200),(-2.4,2.0,150),(0.3,-.8,0),(2.6,-.6,30))]+[(-4.8,-1.8,60,'clap'),(4.9,-1.2,-60,'clap'),(-4.6,3.4,100,'clap')],dance=True)
        def upd(t):
            base(t); q=ease(t/DUR); camset((L(-4.6,-3.2,q),L(-5.8,-5.0,q),L(3.2,2.4,q)),(0,1,.9),24,6)
        return dict(upd=upd)
    if view=='judge':
        base,D=hall_scene(16,4,stand=[(1.6,-6.0,-90,'talk'),(4.0,-5.2,0,'idle')])
        au=person((-1.0,-6.4,0),70,AUNTY,'smirk',name='aunty'); rl=person((-1.55,-5.7,0),110,RELATIVE,'smirk',name='rel')
        def upd(t):
            base(t)
            for H,(x,y,rz) in ((au,(-1.0,-6.4,70)),(rl,(-1.55,-5.7,110))): H['z0']=0; standH(H,x,y,rz,t); blink(H,t)
            tg=(1.6,-6.0,1.9); look_at(au,tg); look_at(rl,tg,.7); arms(au,-62,0,-58,-62,0,58); face(au,mouth='smirk',brow=.02,brow_r=-14,eyes=.75)
            arm_to(rl,1,headpos(au)); face(rl,mouth=('o','smirk')[int(t*5)%2],brow=.03,eyes=.85); rl['head'].rotation_euler[1]=R(10)
            q=ease(t/DUR); camset((L(1.0,.8,q),L(-7.9,-7.7,q),1.85),(-1.3,-6.0,1.7),30,3.2,focus=headpos(au))
        return dict(upd=upd)
    if view=='groom':
        base,D=hall_scene(14,5); hz_=person((0,11.6,0),0,HAMZA,'flat',name='hamza'); am=person((-.9,10.6,0),40,AMMI,'smile',name='ammi'); ph=person((.6,8.3,0),180,PHOTO,'grin',name='photo')
        cam_o=dslr(); flash_light((.6,8.0,2.2)); bl=person((1.0,10.5,0),-40,BILAL,'grin',name='bilal')
        def upd(t):
            base(t); seatH(hz_,0,11.6,0,sh=1.12); blink(hz_,t); face(hz_,mouth='flat',eyes=1.15,brow=.03,brow_r=10)
            hz_['head'].rotation_euler[2]=R(25)*math.sin(t*3.2); arms(hz_,-30,0,8,-30,0,-8)
            on_stage(am,-.9,10.6,40,t); blink(am,t); arm_reach(am,1,(-.12,11.45,2.15)); arms(am,am['arm'][1].rotation_euler[0]*57.3,0,am['arm'][1].rotation_euler[2]*57.3,-20,0,-5) if False else None; face(am,mouth=('o','flat','O')[int(t*6)%3])
            on_stage(bl,1.0,10.5,-40,t); blink(bl,t); arm_reach(bl,-1,(.25,11.5,1.6)); face(bl,mouth='grin')
            ph['z0']=0; standH(ph,.6,8.3,180,t); blink(ph,t); dslr_hands(ph,cam_o); face(ph,mouth='grin')
            flash(t,[.3,1.0,1.6,2.1])
            q=ease(t/DUR); camset((L(-1.6,-1.2,q),L(7.4,7.9,q),1.8),(0,11.4,1.6),30,4,focus=(0,11.6,1.9))
        return dict(upd=upd)
    if view=='biryani':
        base,D=hall_scene(10,6); y=D['dish'][3]; lid=tray_lid(); ub=person((-13.2,y,0),-90,UNCLEB,'flat',name='uncleb')
        rice=[oico((-14.4+random.Random(i).uniform(-.25,.25),y+random.Random(i+9).uniform(-.35,.35),1.03),.04,M(['#E8A040','#F4E8C8'][i%2],.7),sub=1) for i in range(5)]
        def upd(t):
            base(t); ub['z0']=0; standH(ub,-13.2,y,-90,t); blink(ub,t); look_at(ub,(-14.4,y,1.0)); face(ub,mouth='O',eyes=1.3,brow=.06)
            k=ease((t-.4)/.6); lid.location=(-14.4,y,1.08+.35*k); lid.rotation_euler=(0,R(-40*k),0)
            q=ease(t/DUR); camset((-13.1,y-1.6,1.75),(-14.4,y,1.0),34,2.6,focus=(-14.4,y,1.0))
        return dict(upd=upd)
    # welcome: wide hero of the hall
    base,D=hall_scene(28,7,stand=[(x,y,rz,'dance') for (x,y,rz) in ((-1.6,.2,10),(1.2,.4,-20),(-.2,2.4,180),(1.9,2.6,200),(0.3,-.8,0))]+[(-1.5,-9.5,90,'talk'),(-.9,-9.5,-90,'talk'),(2.0,-4.0,0,'selfie')],dance=True)
    def upd(t):
        base(t); q=ease_out(t/DUR); _camset((L(0,0,q),L(-13.2,-11.5,q),L(5.6,3.2,q)),(0,L(4,6,q),L(1.0,1.6,q)),L(20,22,q),8)
    return dict(upd=upd)
for v in ('ext','clothes','money','dance','judge','groom','biryani','welcome'): SHOTS['A_'+v]=(lambda v=v: SH_A(v))
# ============================================================ 2. DRESSING ROOM
HZR=(GX,GY+1.1); BLR=(GX+.62,GY+.6); HZ2=(GX,GY+.72); BL2=(GX-.7,GY+1.6); AB2=(GX+1.3,GY-.95)
def SH_B(view):
    KEY='B_'+view; room=room_scene()
    hz=person((GX,GY+1.1,0),180,HAMZA,'flat',name='hamza'); bl=person((GX+.62,GY+.6,0),200,BILAL,'grin',name='bilal'); ab=person((GX+2.8,GY-1.2,0),-90,ABBU,'flat',name='abbu'); nb=notebook(ab)
    comb=obox((0,0,0),(.08,.012,.025),M('#1A1B22',.4),.004)
    pre=view in ('mirror','bro','relax','bill')
    def upd(t):
        room(t); q=ease(t/DUR)
        for H in (hz,bl,ab): H['z0']=0
        if pre or view=='abbu':
            ab_in=view=='abbu'
            if ab_in: walk_path(ab,[(GX+2.8,GY-1.2),(GX+2.1,GY-1.05),AB2],t,.15,1.9,step=.48,arm=0)
            else: ab['root'].location=(GX+40,GY,0)
            k=ease((t-1.4)/.7) if ab_in else 0
            if k<=0: seatH(hz,HZR[0],HZR[1],180,sh=.56); rest(hz,t,-30); breathe(hz,t)
            else:
                legs0(hz); hz['root'].location=(GX,L(HZR[1],HZ2[1],k),L(.56-1.5*hz['u'],0,k)); hz['z0']=0
                if k>=1: stand(hz,t)
                hz['root'].rotation_euler=(0,0,R(L(180,heading_to(hz,(AB2[0],AB2[1],0))+360 if heading_to(hz,(AB2[0],AB2[1],0))<0 else heading_to(hz,(AB2[0],AB2[1],0)),k))); rest(hz,t)
            if ab_in and t>1.0: walk_path(bl,[BLR,(GX-.2,GY+.35),BL2],t,1.0,2.4,step=.45,arm=14)
            else: standH(bl,BLR[0],BLR[1],200,t)
        else:
            standH(hz,HZ2[0],HZ2[1],heading_to(hz,(AB2[0],AB2[1],0)),t); standH(bl,BL2[0],BL2[1],heading_to(bl,(GX+.6,GY-.3,0)),t); standH(ab,AB2[0],AB2[1],heading_to(ab,(HZ2[0],HZ2[1],0)),t); rest(hz,t)
        for H in (hz,bl,ab): blink(H,t)
        hh=headpos(hz); hb=headpos(bl)
        if pre:
            arm_reach(bl,-1,(hh[0]+.12*math.sin(t*5),hh[1]-.05,hh[2]+.32)); bl['arm'][1].rotation_euler=(R(-40),0,R(10)); carry(comb,bl,-1,(0,0,.05)); look_at(bl,(hh[0],hh[1],hh[2]+.3))
        else: rest(bl,t); comb.location=(GX+.7,GY+2.2,.9)
        ab['arm'][-1].rotation_euler=(R(-70),0,R(10)); ab['arm'][1].rotation_euler=(R(-10),0,R(5)); p=hand_w(ab,-1); nb.location=(p.x,p.y,p.z+.05); nb.rotation_euler=(R(-60),0,ab['root'].rotation_euler[2])
        ha=headpos(ab)
        if not pre: look_at(bl,ha,.7)
        if view=='mirror':
            face(hz,mouth='flat',eyes=1.1,brow=.03,brow_r=10); face(bl,mouth='grin')
            camset((GX-L(1.9,1.7,q),GY+2.0,1.9),(GX+.3,GY+.9,1.5),24,4,focus=hh)
        elif view=='bro':
            talk(hz,t,75,81,KEY,rest='flat'); face(hz,eyes=1.1,brow=.04,brow_r=12); look_at(hz,(GX,GY+2.6,1.8))
            camset((GX-1.05,GY+2.35,1.85),hh,24,2.8,focus=hh)
        elif view=='relax':
            talk(bl,t,82,86,KEY,rest='grin'); face(bl,brow=.04); face(hz,mouth='flat')
            camset((GX+1.95,GY+1.7,2.1),hb,28,2.8,focus=hb)
        elif view=='bill':
            talk(hz,t,87,99,KEY,rest='flat'); face(hz,eyes=1.15,brow=.05,brow_r=16); look_at(hz,(GX,GY+2.6,1.8)); nod(hz,t,-3,3)
            camset((GX-1.0,GY+2.35,1.85),hh,28,2.8,focus=hh)
        elif view=='abbu':
            face(ab,mouth='flat',brow=-.03,brow_r=10); look_at(ab,hh); face(hz,mouth='o'); look_at(hz,ha,ease((t-.9)/.5)); face(bl,mouth='o'); look_at(bl,ha,ease((t-.9)/.5))
            camset((GX-2.6,GY-.4,2.0),(GX+1.4,GY-.3,1.5),24,5,focus=ha)
        elif view=='hamza':
            talk(ab,t,106,106,KEY,rest='flat',shapes=('shout','O')); look_at(ab,hh); face(ab,brow=-.04,brow_r=16); look_at(hz,ha); face(hz,mouth='o')
            camset((GX-1.4,GY+.2,1.95),ha,30,2.8,focus=ha)
        elif view=='ji':
            talk(hz,t,107,108,KEY,rest='flat'); look_at(hz,ha); face(hz,eyes=1.1,brow=.03)
            camset((GX+.6,GY-2.1,1.95),hh,30,2.8,focus=hh)
        elif view=='adv':
            look_at(ab,(p.x,p.y,p.z)); talk(ab,t,109,112,KEY,rest='flat',rate=6); talk(hz,t,113,113,KEY,rest='flat'); face(ab,brow=-.02,eyes=.85); look_at(hz,ha)
            camset((GX-1.5,GY+.3,2.0),ha,26,2.8,focus=ha)
        elif view=='hall':
            look_at(ab,(p.x,p.y,p.z)); talk(ab,t,114,117,KEY,rest='flat',rate=6); face(ab,brow=-.02,eyes=.85); look_at(hz,ha)
            camset((GX-1.4,GY+.2,1.95),ha,32,2.8,focus=ha)
        elif view=='acct':
            talk(hz,t,118,123,KEY,rest='flat',shapes=('O','o','flat','O')); look_at(hz,ha); face(hz,brow=-.02,brow_r=14,eyes=1.1); arms(hz,-30,0,8,-75,0,-45+10*math.sin(t*5))
            camset((GX+.6,GY-2.1,1.95),hh,30,2.8,focus=hh)
        else:
            look_at(ab,hh); talk(ab,t,124,126,KEY,rest='flat',rate=5); face(ab,brow=-.01,eyes=.7); look_at(hz,ha)
            if t>we(126,KEY)+.2: face(hz,mouth='O',eyes=1.3)
            camset((GX-1.4,GY+.2,1.95),ha,L(30,40,q),2.8,focus=ha)
    return dict(upd=upd)
for v in ('mirror','bro','relax','bill','abbu','hamza','ji','adv','hall','acct','dono'): SHOTS['B_'+v]=(lambda v=v: SH_B(v))
# ============================================================ 3. RELATIVES ARRIVE (aisle)
AMP=(-1.7,-8.0); AUP=(.6,-8.0); RLP=(2.0,-6.2)
def SH_C(view):
    KEY='C_'+view
    stand=[(-2.6,-10.6,60,'selfie'),(-3.2,-10.0,-120,'talk'),(2.8,-10.8,-60,'talk'),(3.4,-10.2,120,'talk'),(2.6,-4.6,180,'clap'),(-2.6,-4.8,0,'talk'),(-3.2,-4.2,180,'talk')]
    base,D=hall_scene(24,8,stand=stand,walk=[([(-.4,-14.2),(-.5,-11.0),(-2.0,-9.2)],0,4.5),([(.6,-14.4),(1.4,-11)],.8,5)] if view=='full' else [])
    am=person((AMP[0],AMP[1],0),90,AMMI,'smile',name='ammi'); au=person((0,-13.5,0),180,AUNTY,'smile',name='aunty'); rl=person((RLP[0],RLP[1],0),210,RELATIVE,'smile',name='rel')
    ph=person((-3.6,-7.2,0),-120,PHOTO,'grin',name='photo'); cam_o=dslr(); flash_light((-3.4,-7.5,2.2))
    def upd(t):
        base(t); am['z0']=0; au['z0']=0; rl['z0']=0; ph['z0']=0
        standH(am,AMP[0],AMP[1],90,t); blink(am,t); rest(am,t); standH(rl,RLP[0],RLP[1],210,t); blink(rl,t); rest(rl,t)
        standH(ph,-3.6,-7.2,-120,t); blink(ph,t); dslr_hands(ph,cam_o); flash(t,[.5,1.7,3.1])
        if view in ('full','aunty'):
            if view=='full': au['root'].location=(0,-30,0)
            else: walk_path(au,[(0,-13.6),(.1,-10.0),AUP],t,.1,DUR-.15,step=.48,arm=18); face(au,mouth='smile')
        else:
            standH(au,AUP[0],AUP[1],-90 if view not in ('spots','beti','freeze','kal') else -90,t)
        blink(au,t); ha=headpos(au); hm=headpos(am); hr=headpos(rl); q=ease(t/DUR)
        if view not in ('full','aunty'): rest(au,t); arms(au,-14,0,5,-35,0,-5)
        if view=='full':
            face(am,mouth='grin'); look_at(am,(0,-12,1.8),.5); _camset((L(-5.5,-4.0,q),L(-13.0,-12.2,q),L(3.4,2.6,q)),(L(1,0,q),-3,1.2),22,8)
        elif view=='aunty':
            look_at(am,ha); face(am,mouth='smile'); x=au['root'].location[1]
            camset((.9,L(-4.4,-4.7,q),2.1),(au['root'].location[0],x,1.7),30,4,focus=ha)
        elif view=='salam':
            talk(au,t,145,148,KEY,rest='smile',shapes=('grin','O','o','grin')); look_at(au,hm); arms(au,-14,0,5,-100,0,-20); face(au,brow=.04,eyes=1.1); look_at(am,ha)
            cam_head(au,(1,-1,0),lens=40)
        elif view=='bas':
            talk(am,t,149,153,KEY,rest='smile'); look_at(am,ha); look_at(au,hm); face(am,brow=.01)
            cam_head(am,(-1,-1,0),lens=40)
        elif view=='height':
            talk(au,t,154,160,KEY,rest='smirk'); look_at(au,hm); face(au,brow=.05,brow_r=-10,eyes=.9); au['head'].rotation_euler[1]=R(10); look_at(am,ha); face(am,mouth='flat',eyes=1.2)
            cam_head(au,(1,-1,0),lens=40)
        elif view=='khana':
            talk(am,t,161,166,KEY,rest='grin',shapes=('grin','o','grin')); look_at(am,ha); face(am,brow=.03,eyes=.75); arms(am,-14,0,5,-60,0,-60); look_at(au,hm)
            cam_head(am,(-1,-1,0),lens=40)
        elif view=='details':
            talk(au,t,167,175,KEY,rest='smirk'); look_at(au,hm); arms(au,-14,0,5,-95+12*math.sin(t*5),0,-25); face(au,brow=.03,brow_r=-12,eyes=.85); look_at(am,ha); face(am,mouth='flat',eyes=1.1)
            cam_head(au,(1,-1,0),lens=40)
        elif view=='spots':
            k=ease((t-.2)/.5); au['root'].rotation_euler[2]=R(L(-90,heading_to(au,(RLP[0],RLP[1],0)),k)); look_at(au,hr,k); face(au,mouth='smirk',brow=.06,eyes=1.15); look_at(am,ha)
            camset((L(-1.6,-1.4,q),L(-10.6,-10.3,q),1.85),(.8,-7.2,1.65),28,4,focus=ha)
        elif view=='beti':
            au['root'].rotation_euler[2]=R(heading_to(au,(RLP[0],RLP[1],0))); look_at(au,hr); talk(au,t,180,190,KEY,rest='smirk'); face(au,brow=.04,brow_r=-12,eyes=.85); arms(au,-14,0,5,-80,0,-30)
            look_at(rl,ha); face(rl,mouth='smile')
            cam_head(au,(1,1,0),lens=40)
        elif view=='freeze':
            look_at(rl,ha); face(rl,mouth='flat',eyes=1.3,brow=.06); rl['root'].location[2]+=0
            if t<.05: pass
            arms(rl,-25,0,6,-25,0,-6)
            cam_head(rl,(-1,-1,0),lens=L(40,54,q))
        else:
            look_at(rl,ha); talk(rl,t,194,201,KEY,rest='flat'); face(rl,brow=-.02,brow_r=10,eyes=.75); arms(rl,-62,0,-58,-62,0,58)
            cam_head(rl,(-1,-1,0),lens=40)
    return dict(upd=upd)
for v in ('full','aunty','salam','bas','height','khana','details','spots','beti','freeze','kal'): SHOTS['C_'+v]=(lambda v=v: SH_C(v))
# ============================================================ 4. PHOTOGRAPHER (in front of the stage)
HZP=(0,7.55); PHP=(.25,5.1); BLP=(1.45,7.3)
def SH_D(view):
    KEY='D_'+view
    base,D=hall_scene(22,9,stand=[(-3.0,6.4,120,'talk'),(-3.6,5.8,-60,'talk'),(3.6,5.6,-120,'clap'),(-1.8,3.6,180,'selfie')])
    hz=person((HZP[0],HZP[1],0),0,HAMZA,'smile',name='hamza'); ph=person((PHP[0],PHP[1],0),180,PHOTO,'grin',name='photo'); bl=person((BLP[0],BLP[1],0),-20,BILAL,'grin',name='bilal')
    cam_o=dslr(); fl=flash_light((PHP[0],PHP[1]+.3,2.1))
    def upd(t):
        base(t)
        for H in (hz,ph,bl): H['z0']=0
        if view=='walk': walk_path(ph,[(3.4,2.6),(1.4,4.2),PHP],t,.0,DUR-.2,step=.5,arm=0); ph['arm'][1].rotation_euler=(R(-40),0,R(-10))
        else: standH(ph,PHP[0],PHP[1],180,t)
        standH(hz,HZP[0],HZP[1],0,t); standH(bl,BLP[0],BLP[1],-20,t)
        for H in (hz,ph,bl): blink(H,t)
        rest(hz,t); rest(bl,t); hz_h=headpos(hz); hp=headpos(ph); hb=headpos(bl); q=ease(t/DUR)
        look_at(bl,hz_h,.5); face(bl,mouth='smirk')
        if view!='walk': dslr_hands(ph,cam_o,.6 if view in ('smile','natural','emo','cand','perfect') else 1.0)
        else: carry(cam_o,ph,1,(0,0,.05))
        look_at(ph,hz_h); look_at(hz,hp)
        if view=='walk':
            face(ph,mouth='grin'); face(hz,mouth='smile',eyes=1.1)
            camset((L(-2.4,-2.0,q),L(9.6,9.2,q),2.4),(.8,5.6,1.5),24,5,focus=hp)
        elif view=='smile':
            talk(ph,t,208,210,KEY,rest='grin',shapes=('grin','O','o')); face(ph,brow=.05)
            cam_head(ph,(1,1,0),lens=40)
        elif view=='smiles':
            k=ease((t-.15)/.3); face(hz,mouth='grin' if k>.5 else 'smile',eyes=L(1,1.25,k),brow=.05*k); flash(t,[.6])
            cam_head(hz,(1,-1,0),lens=46)
        elif view=='natural':
            talk(ph,t,213,215,KEY,rest='flat',shapes=('o','flat','o')); face(ph,brow=-.02,brow_r=8); face(hz,mouth='grin')
            cam_head(ph,(1,1,0),lens=40)
        elif view=='again':
            face(hz,mouth='smile',eyes=.7,brow=-.01); hz['head'].rotation_euler[1]=R(8); flash(t,[.5,.65])
            cam_head(hz,(1,-1,0),lens=46)
        elif view=='emo':
            talk(ph,t,219,221,KEY,rest='o',shapes=('o','O','o')); arms(ph,-40,0,-20,-130,0,-40+10*math.sin(t*4)); hide(cam_o); face(ph,brow=.06,brow_r=-12,eyes=.6)
            cam_head(ph,(1,1,0),lens=40)
        elif view=='conf':
            face(hz,mouth='flat',brow=.03,brow_r=16,eyes=.95); hz['head'].rotation_euler[1]=R(12)
            talk(hz,t,225,236,KEY,rest='flat',shapes=('O','o','flat','grin')); arms(hz,-30,0,8,-80,0,-55+10*math.sin(t*4))
            cam_head(hz,(1,-1,0),lens=40)
        elif view=='cand':
            talk(ph,t,237,239,KEY,rest='grin',shapes=('O','grin','O')); face(ph,brow=.06,eyes=1.15)
            cam_head(ph,(1,1,0),lens=40)
        elif view=='turn':
            k=ease((t-.1)/.5); hz['root'].rotation_euler[2]=R(L(0,-75,k)); look_at(hz,(4,7.2,1.9),k); face(hz,mouth='flat',eyes=.8,brow=-.02,brow_r=10); flash(t,[.8,.95,1.1])
            camset((L(-.9,-.7,q),L(4.0,4.3,q),1.85),(0,7.3,1.6),32,3.5,focus=hz_h)
        elif view=='perfect':
            hz['root'].rotation_euler[2]=R(-75); look_at(hz,(4,7.2,1.9)); face(hz,mouth='flat',eyes=.8)
            talk(ph,t,243,249,KEY,rest='grin',shapes=('shout','O','grin','O')); k=ease(t/.25); ph['root'].location[2]+=.12*abs(math.sin(t*9))*(1 if t<.6 else 0); face(ph,brow=.07,eyes=1.3); flash(t,[.1,.3,.5,.7,.9,1.1,1.3])
            cam_head(ph,(1,1,0),lens=36)
        elif view=='lean':
            hz['root'].rotation_euler[2]=R(-75); k=ease(t/.6); bl['root'].rotation_euler[2]=R(L(-20,-60,k)); bl['root'].rotation_euler[0]=R(12*k); look_at(bl,hz_h); face(bl,mouth='smirk',eyes=.85)
            face(hz,mouth='flat',eyes=.85)
            camset((L(3.4,3.2,q),L(5.6,5.9,q),1.95),(.7,7.4,1.7),30,3.5,focus=hb)
        else:
            hz['root'].rotation_euler[2]=R(-75); bl['root'].rotation_euler[2]=R(-60); bl['root'].rotation_euler[0]=R(12); look_at(bl,hz_h); talk(bl,t,253,266,KEY,rest='smirk'); face(bl,brow=.04,brow_r=-10)
            look_at(hz,hb,.8); face(hz,mouth='flat',eyes=.7); flash(t,[.8,2.2,3.0])
            cam_head(bl,(1,-1,0),lens=40)
    return dict(upd=upd)
for v in ('walk','smile','smiles','natural','again','emo','conf','cand','turn','perfect','lean','400'): SHOTS['D_'+v]=(lambda v=v: SH_D(v))
# ============================================================ 5. DANCE FLOOR
HZD=(-.9,.9); BLD=(.9,.9); UDP=(1.5,2.9)
def SH_E(view):
    KEY='E_'+view
    fr=[(x,y,rz,'dance') for (x,y,rz) in ((-2.4,2.6,150),(2.6,2.9,200),(-2.8,-.6,40),(2.9,-.4,-40),(-.6,3.6,180),(-3.4,1.2,90))]
    base,D=hall_scene(18,10,stand=fr+[(-5.2,-2.0,60,'clap'),(5.2,-1.6,-60,'clap'),(-5.0,4.0,110,'clap'),(5.1,3.8,-110,'selfie')],dance=True)
    hz=person((HZD[0],HZD[1],0),0,HAMZA,'flat',name='hamza'); bl=person((BLD[0],BLD[1],0),0,BILAL,'grin',name='bilal'); ud=person((5.5,-2.0,0),0,UNCLED,'grin',name='uncled')
    def upd(t):
        base(t)
        for H in (hz,bl,ud): H['z0']=0
        q=ease(t/DUR)
        if view=='music':
            walk_path(hz,[(-1.2,-3.6),(-.8,-1.4),HZD],t,-1,DUR+1.5,step=.5,arm=10) if False else standH(hz,-2.2,-2.6,0,t)
            walk_path(bl,[(2.5,-4.2),(1.2,-1.6),BLD],t,.1,DUR,step=.6,arm=30,run_=False); face(bl,mouth='grin')
            rest(hz,t); face(hz,mouth='flat',eyes=1.1); ud['root'].location=(30,30,0)
            _camset((L(4.2,3.0,q),L(-6.4,-5.6,q),L(3.0,2.2,q)),(0,L(.5,1.0,q),1.0),22,6); blink(hz,t); blink(bl,t); return
        standH(hz,*HZD,0,t) if view!='grab' else None
        if view=='grab':
            k=ease((t-.3)/1.0); hz['root'].location[0]=L(-2.2,HZD[0],k); hz['root'].location[1]=L(-2.6,HZD[1],k); hz['root'].rotation_euler=(0,0,R(L(0,-35,k))); idle(hz,t)
            hz['leg'][1].rotation_euler[0]=R(15)*math.sin(t*9)*(1 if 0<k<1 else 0); hz['leg'][-1].rotation_euler[0]=-hz['leg'][1].rotation_euler[0]
            bl['root'].location=(hz['root'].location[0]+1.5,hz['root'].location[1]+.15,0); bl['root'].rotation_euler=(0,0,R(-60)); idle(bl,t); arm_reach(bl,-1,hand_w(hz,1)); arm_reach(hz,1,hand_w(bl,-1))
            face(hz,mouth='O',eyes=1.2); face(bl,mouth='grin')
            camset((L(-1.4,-1.0,q),L(-6.4,-5.8,q),1.9),(L(-1.6,-.2,q),L(-2.0,.6,q),1.4),26,4,focus=headpos(hz)); blink(hz,t); blink(bl,t); ud['root'].location=(30,30,0); return
        standH(bl,*BLD,0,t); blink(hz,t); blink(bl,t); hh=headpos(hz); hb=headpos(bl)
        hz['root'].rotation_euler[2]=R(-35); bl['root'].rotation_euler[2]=R(35)
        if view in ('chal','nahi','kya'): ud['root'].location=(30,30,0)
        else:
            if view=='uncle': walk_path(ud,[(4.6,-2.6),(3.0,.4),UDP],t,.2,1.8,step=.5,arm=22);
            else: standH(ud,*UDP,heading_to(ud,(0,.6,0)),t)
            blink(ud,t)
        hu=headpos(ud)
        if view=='chal':
            talk(bl,t,281,283,KEY,rest='grin',shapes=('shout','O','shout')); bhangra(bl,t,0,.8); face(bl,brow=.07,eyes=1.3); rest(hz,t); face(hz,mouth='O',eyes=1.2); look_at(hz,hb)
            cam_head(bl,(1,-1,0),lens=36)
        elif view=='nahi':
            talk(hz,t,284,287,KEY,rest='O',shapes=('O','o','O')); arms(hz,-60,0,-40+10*math.sin(t*9),-60,0,40-10*math.sin(t*9)); face(hz,brow=.07,brow_r=18,eyes=1.3); look_at(hz,hb)
            cam_head(hz,(-1,-1,0),lens=38)
        elif view=='kya':
            talk(bl,t,288,297,KEY,rest='grin'); look_at(bl,hh); arms(bl,-30,0,-60,-30,0,60); face(bl,brow=.05,brow_r=-10); rest(hz,t); face(hz,mouth='flat',eyes=1.1); look_at(hz,hb)
            cam_head(bl,(1,-1,0),lens=38)
        elif view=='wild':
            w=t*9; bl['root'].location[2]+=.15*abs(math.sin(w)); arms(bl,-170+40*math.sin(w),R(0),-60*math.sin(w*.5),-170+40*math.sin(w+pi),0,60*math.sin(w*.5)); bl['root'].rotation_euler[2]+=R(40)*math.sin(w*.5)
            bl['leg'][1].rotation_euler[0]=-R(45)*max(0,math.sin(w)); bl['leg'][-1].rotation_euler[0]=-R(45)*max(0,-math.sin(w)); face(bl,mouth=('grin','shout')[int(t*4)%2],eyes=.3)
            rest(hz,t); face(hz,mouth='flat',eyes=1.15); look_at(hz,hb); ud['root'].location=(30,30,0)
            camset((L(-.5,.2,q),L(-4.2,-3.8,q),1.6),(0,1.0,1.3),28,4,focus=hb)
        elif view in ('uncle','move'):
            b=max(0,t-1.8) if view=='uncle' else t;
            if view=='move' or t>1.8:
                spin=(b*2.4)%1.0 if view=='move' else 0; ud['root'].rotation_euler[2]=R(heading_to(ud,(0,.6,0))+360*ease(min(1,b*1.4)) ) if view=='move' else R(heading_to(ud,(0,.6,0)))
                w=b*7; arms(ud,-160,0,-10+30*math.sin(w),-160,0,10-30*math.sin(w)); ud['root'].location[2]+=.1*abs(math.sin(w)); ud['root'].rotation_euler[1]=R(14)*math.sin(w/2)
                if view=='move' and b>1.0: c=ease((b-1.0)/.4)*(1-ease((b-2.2)/.4)); ud['root'].location[2]-=.5*c; ud['leg'][1].rotation_euler[0]=-R(80)*c; ud['leg'][-1].rotation_euler[0]=R(30)*c
                face(ud,mouth='grin',eyes=.5,brow=.05)
            bhangra(bl,t,0,.5); face(hz,mouth='O',eyes=1.25); look_at(hz,hu); look_at(bl,hu,.6)
            camset((L(-1.4,-1.0,q),L(-3.6,-3.2,q),1.75),(.8,1.6,1.3),26,4,focus=hu)
        elif view=='karte':
            talk(hz,t,312,316,KEY,rest='o'); look_at(hz,hu); face(hz,brow=.05,eyes=1.15); look_at(ud,hh); face(ud,mouth='grin'); arms(ud,-14,0,5,-14,0,-5); bhangra(bl,t,0,.4)
            cam_head(hz,(1,-1,0),lens=40)
        elif view=='beta':
            talk(ud,t,317,328,KEY,rest='smirk'); look_at(ud,hh); arms(ud,-62,0,-58,-120,0,-30+15*math.sin(t*3)); face(ud,brow=.04,brow_r=-10,eyes=.85); face(hz,mouth='o'); look_at(hz,hu)
            cam_head(ud,(-1,-1,0),lens=40)
        elif view=='watch':
            k=ease(t/.6); bhangra(bl,t,0,1-k) if k<1 else arms(bl,-62,0,-58,-62,0,58); look_at(bl,hu); face(bl,mouth='O',eyes=L(1,1.3,k))
            w=t*8; arms(ud,-160,0,-20*math.sin(w),-160,0,20*math.sin(w)); ud['root'].rotation_euler[2]=R(heading_to(ud,(0,.6,0))+40*math.sin(w/2)); ud['root'].location[2]+=.08*abs(math.sin(w)); face(ud,mouth='grin',eyes=.4)
            look_at(hz,hu); face(hz,mouth='O')
            cam_head(bl,(-1,-1,0),lens=36)
        else:
            look_at(bl,hh); arms(bl,-62,0,-58,-62,0,58); talk(bl,t,341,346,KEY,rest='o'); face(bl,brow=.06,eyes=1.1); look_at(hz,hb); face(hz,mouth='flat')
            w=t*8; arms(ud,-160,0,-20*math.sin(w),-160,0,20*math.sin(w)); ud['root'].location[2]+=.08*abs(math.sin(w)); face(ud,mouth='grin',eyes=.4)
            cam_head(bl,(1,-1,0),lens=40)
    return dict(upd=upd)
for v in ('music','grab','chal','nahi','kya','wild','uncle','karte','beta','move','watch','pro'): SHOTS['E_'+v]=(lambda v=v: SH_E(v))
# ============================================================ 6. BIRYANI WAR (buffet)
def SH_F(view):
    KEY='F_'+view
    base,D=hall_scene(16,11,skip=(0,4),stand=[(-12.2,-9.0,-90,'idle'),(-12.0,-10.0,-90,'talk'),(-11.4,-7.4,-100,'idle'),(-12.3,-2.6,-90,'idle')],
        walk=[([(-4,-6),(-11.6,-8.4)],-.5,4.5),([(-3,-4),(-11.6,-6.6)],0,5),([(-5,-2),(-12.0,-3.8)],.3,5.5)] if view in ('dinner','reach') else [])
    y=D['dish'][3]; UBP=(-13.05,y); WTP=(-15.3,y); HZF=(-11.2,y+1.7); BLF=(-11.0,y+.7)
    ub=person((UBP[0],UBP[1],0),-90,UNCLEB,'flat',name='uncleb'); wt=person((WTP[0],WTP[1],0),90,WAITER,'smile',name='waiter'); lid=tray_lid()
    hz=person((HZF[0],HZF[1],0),-120,HAMZA,'flat',name='hamza'); bl=person((BLF[0],BLF[1],0),-100,BILAL,'flat',name='bilal')
    rice=[oico((-14.4+random.Random(i).uniform(-.25,.25),y+random.Random(i+9).uniform(-.35,.35),1.03),.035,M(['#E8A040','#F4E8C8'][i%2],.7),sub=1) for i in range(5)]
    def upd(t):
        base(t)
        for H in (ub,wt,hz,bl): H['z0']=0
        q=ease(t/DUR); lid_open=view not in ('dinner','reach','kidhar','yahan','lid')
        if view=='lid': k=ease((t-wl(368,KEY))/.5); lid_open=None
        if view in ('dinner','reach'):
            walk_path(ub,[(-3.5,-1.4),(-9,y+.3),UBP],t,-.2 if view=='reach' else -3,DUR-.2,step=.55,arm=26)
        else: standH(ub,UBP[0],UBP[1],-90,t)
        standH(wt,WTP[0],WTP[1],90,t)
        hz_on=view in ('hears','bro','kya','biryani','turns','mubarak','camera','caterer')
        if hz_on:
            if view=='hears': walk_path(hz,[(-7.5,y+3.2),HZF],t,.0,DUR-.3,step=.5,arm=20); walk_path(bl,[(-7.2,y+2.2),BLF],t,.1,DUR-.2,step=.5,arm=20)
            else: standH(hz,HZF[0],HZF[1],-120,t); standH(bl,BLF[0],BLF[1],-100,t)
        else: hz['root'].location=(40,40,0); bl['root'].location=(41,40,0)
        for H in (ub,wt,hz,bl): blink(H,t)
        rest(wt,t); rest(hz,t); rest(bl,t)
        hu=headpos(ub); hw=headpos(wt); hh=headpos(hz); hb=headpos(bl)
        if lid_open is None: lid.location=(-14.4,y,1.08+.35*k); lid.rotation_euler=(0,R(-30*k),0)
        elif lid_open: lid.location=(-14.0,y-.4,1.0); lid.rotation_euler=(R(10),R(-70),0)
        else: lid.location=(-14.4,y,1.08); lid.rotation_euler=(0,0,0)
        if lid_open or lid_open is None:
            if lid_open: arm_reach(ub,-1,(-13.95,y-.4,1.25)) if view in ('yeh','khatam') else None
        look_at(wt,hu)
        if view=='dinner':
            face(ub,mouth='grin',eyes=1.15); _camset((L(-6.5,-7.0,q),L(-13.5,-13.0,q),2.6),(-10,-4.5,1.2),22,6)
        elif view=='reach':
            face(ub,mouth='grin',eyes=1.15); look_at(ub,(-14.4,y,1.0),.6); camset((L(-12.3,-12.1,q),y-2.8,1.85),(-13.4,y,1.5),26,4,focus=hu)
        elif view=='kidhar':
            talk(ub,t,361,364,KEY,rest='smile'); look_at(ub,hw); arms(ub,-14,0,5,-80,0,-40); face(ub,brow=.04); cam_head(ub,(1,-1,0),lens=40)
        elif view=='yahan':
            talk(wt,t,365,366,KEY,rest='smile'); arm_reach(wt,1,(-14.4,y,1.15)); look_at(ub,(-14.4,y,1.0)); cam_head(wt,(1,-1,0),lens=40)
        elif view=='lid':
            arm_reach(ub,1,(lid.location[0]+.05,lid.location[1]+.35,lid.location[2]+.12)); look_at(ub,(-14.4,y,1.0)); face(ub,mouth='smile' if t<wl(371,KEY) else 'O',eyes=1.0 if t<wl(371,KEY) else 1.35,brow=.02 if t<wl(371,KEY) else .07)
            if t<wl(371,KEY): camset((-13.0,y-1.4,1.75),(-14.0,y,1.2),30,3,focus=hu)
            else: _camset((-13.55,y-.95,1.95),(-14.4,y,1.0),30,2.4,focus=(-14.4,y,1.02))
        elif view=='yeh':
            talk(ub,t,376,378,KEY,rest='O',shapes=('shout','O','shout')); face(ub,brow=.07,brow_r=-16,eyes=1.35); arms(ub,-40,0,-140,-40,0,140); cam_head(ub,(1,-1,0),lens=36)
        elif view=='khatam':
            talk(wt,t,379,383,KEY,rest='flat'); face(wt,brow=.04,brow_r=12,eyes=.9); arms(wt,-30,0,-55,-30,0,55); face(ub,mouth='O'); cam_head(wt,(1,-1,0),lens=40)
        elif view=='shaadi':
            talk(ub,t,384,387,KEY,rest='O',shapes=('shout','O','shout','frown')); arms(ub,-30,0,-150,-30,0,150); ub['root'].location[2]+=.05*abs(math.sin(t*9)); face(ub,brow=-.05,brow_r=20,eyes=1.3)
            cam_head(ub,(1,-1,0),lens=34)
        elif view=='around':
            k=t/DUR; ub['root'].rotation_euler[2]=R(-90+170*ease(k)); look_at(ub,(-8,y+2*math.sin(t*3),1.9),.8); face(ub,mouth='frown',brow=-.05,brow_r=20,eyes=1.2); arms(ub,-62,0,-58,-62,0,58)
            camset((L(-10.2,-10.6,q),y+.4,1.75),(-13.0,y,1.65),30,4,focus=hu)
        elif view=='20saal':
            ub['root'].rotation_euler[2]=R(80); talk(ub,t,392,405,KEY,rest='frown',shapes=('shout','O','frown','shout')); arms(ub,-110+20*math.sin(t*5),0,-30,-40,0,20); ub['arm'][1].rotation_euler[2]=R(-30+20*math.sin(t*3))
            face(ub,brow=-.05,brow_r=22,eyes=1.25); cam_head(ub,(1,1,0),lens=36)
        elif view=='hears':
            ub['root'].rotation_euler[2]=R(80); face(ub,mouth='frown',brow=-.05,brow_r=20); talk(hz,t,410,412,KEY,rest='flat'); look_at(hz,hu); face(hz,brow=.04,eyes=1.15)
            camset((L(-8.2,-8.6,q),L(y+4.6,y+4.2,q),2.0),(-11.6,y+.8,1.6),26,4,focus=hh)
        elif view=='bro':
            ub['root'].rotation_euler[2]=R(80); look_at(bl,(-14.4,y,1.0)); talk(bl,t,413,421,KEY,rest='flat'); face(bl,brow=.03,eyes=.85); look_at(hz,hb); cam_head(bl,(1,1,0),lens=40)
        elif view=='kya':
            ub['root'].rotation_euler[2]=R(80); talk(hz,t,422,422,KEY,rest='o'); look_at(hz,hb); face(hz,brow=.05,eyes=1.2); cam_head(hz,(1,1,0),lens=42)
        elif view=='biryani':
            ub['root'].rotation_euler[2]=R(80); look_at(bl,hh); talk(bl,t,423,423,KEY,rest='flat'); face(bl,brow=-.02,eyes=.7); cam_head(bl,(1,1,0),lens=L(44,58,q))
        elif view=='turns':
            k=ease(t/.8); ub['root'].rotation_euler[2]=R(L(80,heading_to(ub,(HZF[0],HZF[1],0)),k)); look_at(ub,hh,k); face(ub,mouth='frown',brow=-.03,brow_r=14); look_at(hz,hu); face(hz,mouth='o',eyes=1.15)
            camset((L(-10.2,-10.5,q),y-2.2,1.8),(-12.2,y+.6,1.6),28,4,focus=hu)
        elif view=='mubarak':
            ub['root'].rotation_euler[2]=R(heading_to(ub,(HZF[0],HZF[1],0))); look_at(ub,hh); talk(ub,t,429,438,KEY,rest='frown',rate=6); arms(ub,-14,0,5,-90,0,-20); face(ub,brow=-.02,brow_r=14,eyes=.8)
            look_at(hz,hu); face(hz,mouth='flat'); cam_head(ub,(1,1,0),lens=40)
        elif view=='camera':
            ub['root'].rotation_euler[2]=R(heading_to(ub,(HZF[0],HZF[1],0))); k=ease(t/.5); hz['root'].rotation_euler[2]=R(L(-120,60,k)); look_at(hz,(-8,y+3.4,1.9),k); face(hz,mouth='flat',eyes=.7,brow=-.02)
            _camset((HZF[0]+1.55,HZF[1]+.9,1.95),(HZF[0],HZF[1],1.85),40,2.8,focus=hh)
        else:
            ub['root'].rotation_euler[2]=R(heading_to(ub,(HZF[0],HZF[1],0))); hz['root'].rotation_euler[2]=R(60); look_at(hz,(-8,y+3.4,1.9)); talk(hz,t,444,448,KEY,rest='flat',shapes=('O','o','shout','O'))
            arms(hz,-30,0,8,-80,0,-55+8*math.sin(t*6)); face(hz,brow=-.03,brow_r=16,eyes=1.15); _camset((HZF[0]+1.5,HZF[1]+.88,1.95),(HZF[0],HZF[1],1.85),L(40,48,q),2.8,focus=hh)
    return dict(upd=upd)
for v in ('dinner','reach','kidhar','yahan','lid','yeh','khatam','shaadi','around','20saal','hears','bro','kya','biryani','turns','mubarak','camera','caterer'): SHOTS['F_'+v]=(lambda v=v: SH_F(v))
# ============================================================ 7. WALLET (front of stage)
HZG=(-1.9,7.0); ABG=(-3.95,6.95); BLG=(-.1,6.2); PHG=(-1.7,4.9)
def SH_G(view):
    KEY='G_'+view
    base,D=hall_scene(22,12,stand=[(3.0,6.4,-120,'talk'),(3.6,5.8,60,'talk'),(-5.2,4.0,40,'clap'),(2.0,3.2,180,'selfie')])
    hz=person((0,7.6,0),0,HAMZA,'flat',name='hamza'); bl=person((4,2,0),0,BILAL,'flat',name='bilal'); ab=person((ABG[0],ABG[1],0),90,ABBU,'flat',name='abbu'); ph=person((5,3,0),0,PHOTO,'grin',name='photo')
    nb=notebook(ab); cam_o=dslr(); fl=flash_light((0,0,0));
    def upd(t):
        base(t)
        for H in (hz,bl,ab,ph): H['z0']=0; blink(H,t)
        q=ease(t/DUR)
        stage_part=view in ('about','problem','abkya','wallet')
        if view=='about':
            walk_path(hz,[(0,6.6),(0,7.9)],t,.0,1.6,step=.45,arm=16);
            if t>1.6: standH(hz,0,7.9,180,t); hz['root'].rotation_euler[2]=R(L(0,180,ease((t-1.6)/.4))) if t<2.0 else R(180)
            walk_path(bl,[(4.5,1.5),(1.6,5.5),(.7,6.9)],t,wl(459,KEY)-.3,DUR,step=.7,arm=34,run_=True)
            face(hz,mouth='smile',eyes=.8); face(bl,mouth='O',eyes=1.2)
            camset((L(2.6,2.2,q),L(3.2,3.6,q),1.9),(.4,6.6,1.4),24,5,focus=headpos(hz))
        elif stage_part:
            standH(hz,0,7.9,0,t); standH(bl,.7,6.9,heading_to(bl,(0,7.9,0)),t); hh=headpos(hz); hb=headpos(bl); look_at(hz,hb); look_at(bl,hh); rest(hz,t)
            if view=='problem': talk(bl,t,462,463,KEY,rest='O',shapes=('shout','O','shout')); arms(bl,-140,0,-30+15*math.sin(t*9),-60,0,30); face(bl,brow=.07,eyes=1.3); cam_head(bl,(1,-1,0),lens=36)
            elif view=='abkya': talk(hz,t,464,465,KEY,rest='frown',shapes=('O','shout')); arms(hz,-40,0,-50,-40,0,50); face(hz,brow=-.04,brow_r=16,eyes=1.1); cam_head(hz,(-1,-1,0),lens=38)
            else: talk(bl,t,466,471,KEY,rest='O'); arms(bl,-60,0,-30,-60,0,30); face(bl,brow=.06,eyes=1.25); face(hz,mouth='O',eyes=1.3); cam_head(bl,(1,-1,0),lens=36)
        else:
            if view=='rush': walk_path(hz,[(0,7.9),(-.8,7.4),HZG],t,.1,DUR-.2,step=.62,arm=30)
            else: standH(hz,HZG[0],HZG[1],-90,t)
            standH(bl,BLG[0],BLG[1],heading_to(bl,(HZG[0],HZG[1],0)),t); standH(ab,ABG[0],ABG[1],90,t)
            hh=headpos(hz); hb=headpos(bl); ha=headpos(ab); look_at(ab,hh); look_at(bl,hh,.6); rest(bl,t)
            ab['arm'][-1].rotation_euler=(R(-70),0,R(10)); ab['arm'][1].rotation_euler=(R(-10),0,R(5)); p=hand_w(ab,-1); nb.location=(p.x,p.y,p.z+.05); nb.rotation_euler=(R(-60),0,ab['root'].rotation_euler[2])
            phon=view in ('photo','last','gum','tension')
            if phon:
                if view=='photo': walk_path(ph,[(3.0,3.2),(.4,4.4),PHG],t,wl(503,KEY)-.2,DUR-.1,step=.5,arm=0); carry(cam_o,ph,1,(0,0,.05))
                else: standH(ph,PHG[0],PHG[1],heading_to(ph,(HZG[0],HZG[1],0)),t); dslr_hands(ph,cam_o)
                fl.location=(cam_o.location[0],cam_o.location[1]+.1,cam_o.location[2]+.15)
            else: ph['root'].location=(40,40,0)
            hp=headpos(ph)
            if view=='rush': look_at(hz,ha,.6); face(hz,mouth='O',eyes=1.2); face(ab,mouth='flat'); camset((L(-.2,-.6,q),L(3.4,3.6,q),2.0),(-2.2,7.0,1.5),26,5,focus=hh)
            elif view=='kahan': look_at(hz,ha); talk(hz,t,477,480,KEY,rest='o'); arms(hz,-60,0,-30,-60,0,30); face(hz,brow=.05,eyes=1.2); cam_head(hz,(1,-1,0),lens=40)
            elif view=='diya': talk(ab,t,481,485,KEY,rest='flat',shapes=('O','o','flat')); arm_to(ab,1,hh); face(ab,brow=-.03,brow_r=12); look_at(hz,ha); cam_head(ab,(1,-1,0),lens=40)
            elif view=='mujhe':
                talk(hz,t,486,486,KEY,rest='O',shapes=('shout','O')); look_at(hz,ha); arm_reach(hz,1,(hh[0]+.1,hh[1]-.35,hh[2]-.55)); hz['arm'][-1].rotation_euler=(R(-30),0,R(40)); face(hz,brow=.08,eyes=1.4)
                hz['root'].location[2]+=.1*ease(t/.15)*(1-ease((t-.3)/.2)); cam_head(hz,(1,-1,0),lens=L(38,48,q))
            elif view=='haan': talk(ab,t,487,492,KEY,rest='flat',rate=6); arm_to(ab,1,hh); face(ab,brow=-.04,brow_r=16); nod(ab,t,4,4); look_at(hz,ha); face(hz,mouth='O'); cam_head(ab,(1,-1,0),lens=40)
            elif view=='pockets':
                w=t*5; arm_reach(hz,1,(hh[0]+.32,hh[1]-.1,hh[2]-1.15+.08*math.sin(w))); arm_reach(hz,-1,(hh[0]-.32,hh[1]-.1,hh[2]-1.15+.08*math.sin(w+1))); look_at(hz,(hh[0],hh[1]-.4,hh[2]-1.4)); face(hz,mouth='strain',eyes=1.2,brow=.06)
                b=wl(497,KEY)
                if t>b: hz['head'].rotation_euler[0]=R(0); look_at(hz,ha); face(hz,mouth='O',eyes=1.3); arms(hz,-30,0,-60,-30,0,60)
                camset((L(-1.0,-.9,q),L(4.2,4.4,q),1.85),(-1.9,7.0,1.5),28,4,focus=hh) if t<wl(498,KEY) else None
                if t>=wl(498,KEY):
                    arm_reach(bl,1,(hb[0]+.3,hb[1],hb[2]-1.15+.08*math.sin(w))); arm_reach(bl,-1,(hb[0]-.3,hb[1],hb[2]-1.15)); look_at(bl,(hb[0],hb[1]-.3,hb[2]-1.4)); face(bl,mouth='strain',eyes=1.15)
                    camset((L(.4,.6,q),L(4.0,4.2,q),1.85),(-1.1,6.8,1.5),28,4,focus=hb)
            elif view=='photo': face(ph,mouth='grin'); look_at(ph,hh); face(hz,mouth='flat',eyes=1.1); look_at(hz,hp,ease((t-wl(505,KEY))/.4)); camset((L(1.4,1.0,q),L(3.0,3.3,q),1.95),(-1.4,5.8,1.5),26,4,focus=hp)
            elif view=='last': talk(ph,t,507,510,KEY,rest='grin',shapes=('grin','O','o')); look_at(ph,hh); face(ph,brow=.05,eyes=1.15); flash(t,[1.1],e=2200); look_at(hz,hp); cam_head(ph,(1,-1,0),lens=40)
            elif view=='gum': talk(hz,t,511,515,KEY,rest='frown',shapes=('shout','O','shout','frown')); look_at(hz,hp); arms(hz,-150,0,-30+15*math.sin(t*8),-60,0,40); face(hz,brow=-.06,brow_r=22,eyes=1.3); flash(t,[.6,1.2],e=2200); cam_head(hz,(1,-1,0),lens=36)
            else: talk(ph,t,516,523,KEY,rest='grin',rate=6); look_at(ph,hh); face(ph,brow=.02,eyes=.8,mouth=None); flash(t,[2.4,2.55,2.7],e=2400); face(hz,mouth='frown',brow=-.06,brow_r=22); cam_head(ph,(1,-1,0),lens=40)
    return dict(upd=upd)
for v in ('about','problem','abkya','wallet','rush','kahan','diya','mujhe','haan','pockets','photo','last','gum','tension'): SHOTS['G_'+v]=(lambda v=v: SH_G(v))
# ============================================================ 8. FINAL TWIST (on the stage sofa)
AMS=(-1.6,9.95); ABS=(-2.7,10.7); AUS=(1.7,9.95); BLS=(2.0,10.95)
def SH_H(view):
    KEY='H_'+view
    base,D=hall_scene(10,13,stand=[(3.0,4.4,-140,'talk'),(-4.0,3.0,30,'idle')])
    hz=person((0,11.6,0),0,HAMZA,'flat',name='hamza'); bl=person((BLS[0],BLS[1],0),-60,BILAL,'grin',name='bilal'); am=person((AMS[0],AMS[1],0),0,AMMI,'smile',name='ammi')
    ab=person((ABS[0],ABS[1],0),0,ABBU,'flat',name='abbu'); au=person((AUS[0],AUS[1],0),0,AUNTY,'smile',name='aunty'); pl=plate(); nb=notebook(ab); spoon=obox((0,0,0),(.012,.06,.006),M('#C9CDD6',.2,metal=.9),.002)
    def upd(t):
        base(t); seatH(hz,0,11.6,0,sh=1.12); blink(hz,t); hh=headpos(hz); q=ease(t/DUR)
        has_plate=view not in ('over',)
        # Bilal
        if view=='plate': walk_path(bl,[(3.4,9.6),(2.0,10.2),BLS],t,.0,DUR-.4,step=.5,arm=0,z=.6)
        else: on_stage(bl,BLS[0],BLS[1],heading_to(bl,(0,11.6,0)),t)
        blink(bl,t); hb=headpos(bl)
        if view in ('over','plate'):
            arms(hz,-30,0,8,-30,0,-8); face(hz,mouth='flat',eyes=.75)
            if view=='plate': arms(bl,-70,0,-8,-70,0,8); p=(hand_w(bl,1)+hand_w(bl,-1))/2; pl.location=(p.x,p.y-.05,p.z+.06); face(bl,mouth='grin'); look_at(hz,hb,ease(t/.8)); face(hz,mouth='smile')
            else: pl.location=(0,0,-5); rest(bl,t); bl['root'].location=(30,30,0)
        else:
            arms(hz,-45,0,-12,-45,0,12); p=(hand_w(hz,1)+hand_w(hz,-1))/2; pl.location=(p.x,p.y-.05,p.z+.05); rest(bl,t); look_at(bl,hh)
        # family arrives
        fam_am=view in ('bite','beta','ji','shopping','freeze','abhi','abbu','payment','aunty','cousin','down','gaari','kahan','dubai')
        fam_ab=view in ('abbu','payment','aunty','cousin','down','gaari','kahan','dubai'); fam_au=view in ('aunty','cousin','down','gaari','kahan','dubai')
        if fam_am:
            if view=='bite' : walk_path(am,[(-3.2,9.6),(-2.2,10.0),AMS],t,wl(549,KEY),DUR-.1,step=.48,arm=16,z=.6)
            else: on_stage(am,AMS[0],AMS[1],heading_to(am,(0,11.6,0)),t)
        else: am['root'].location=(30,31,0)
        if fam_ab:
            if view=='abbu': walk_path(ab,[(-3.6,10.8),ABS],t,.1,DUR-.2,step=.48,arm=0,z=.6)
            else: on_stage(ab,ABS[0],ABS[1],heading_to(ab,(0,11.6,0)),t)
            ab['arm'][-1].rotation_euler=(R(-70),0,R(10)); pn=hand_w(ab,-1); nb.location=(pn.x,pn.y,pn.z+.05); nb.rotation_euler=(R(-60),0,ab['root'].rotation_euler[2])
        else: ab['root'].location=(30,32,0)
        if fam_au:
            if view=='aunty': walk_path(au,[(3.4,9.7),(2.2,9.9),AUS],t,.1,DUR-.2,step=.46,arm=16,z=.6)
            else: on_stage(au,AUS[0],AUS[1],heading_to(au,(0,11.6,0)),t)
        else: au['root'].location=(30,33,0)
        for H in (am,ab,au): blink(H,t); rest(H,t)
        hm=headpos(am); ha=headpos(ab); hu=headpos(au)
        for H in (am,ab,au): look_at(H,hh)
        if view=='over':
            _camset((L(0,0,q),L(-2.0,1.0,q),L(3.6,2.6,q)),(0,11,1.5),L(24,30,q),6)
        elif view=='plate':
            camset((L(2.2,1.9,q),L(8.4,8.8,q),2.2),(.6,11.0,1.5),28,4,focus=hh)
        elif view=='finally':
            talk(hz,t,540,544,KEY,rest='grin'); face(hz,eyes=.4,brow=.03); hz['head'].rotation_euler[0]=R(-8); cam_head(hz,(1,-1,0),lens=40)
        elif view=='bite':
            k=(t%1.6)/1.6; arm_reach(hz,1,(hh[0],hh[1]-.22,hh[2]-.25+.25*math.sin(pi*min(1,k*2)))); carry(spoon,hz,1,(0,0,.04)); face(hz,mouth='O' if .2<k<.45 else ('o' if k<.2 else 'grin'),eyes=.5)
            if t>wl(549,KEY): look_at(hz,hm,ease((t-wl(551,KEY))/.4)); face(am,mouth='smile')
            camset((L(1.4,1.1,q),L(8.6,8.9,q),2.0),(-.4,11.0,1.6),26,4,focus=hh)
        elif view=='beta':
            talk(am,t,553,554,KEY,rest='smile',shapes=('grin','O','grin')); arms(am,-14,0,5,-100,0,-30); look_at(hz,hm); face(hz,mouth='o'); cam_head(am,(-1,-1,0),lens=40)
        elif view=='ji':
            talk(hz,t,555,556,KEY,rest='flat'); look_at(hz,hm); face(hz,eyes=1.05); cam_head(hz,(-1,-1,0),lens=40)
        elif view=='shopping':
            talk(am,t,557,563,KEY,rest='smile'); face(am,brow=.03,eyes=.9); arms(am,-14,0,5,-80,0,-20+10*math.sin(t*4)); look_at(hz,hm); face(hz,mouth='flat',eyes=1.1); cam_head(am,(-1,-1,0),lens=40)
        elif view=='freeze':
            look_at(hz,hm); face(hz,mouth='flat',eyes=1.35,brow=.07); cam_head(hz,(1,-1,0),lens=L(40,58,q))
        elif view=='abhi':
            look_at(hz,hm); talk(hz,t,566,571,KEY,rest='O',shapes=('shout','O','shout','frown')); face(hz,brow=-.05,brow_r=22,eyes=1.35); arms(hz,-62,0,-12,-150,0,-25+15*math.sin(t*8)); cam_head(hz,(1,-1,0),lens=36)
        elif view=='abbu':
            look_at(hz,ha); face(hz,mouth='O'); face(ab,mouth='flat',brow=-.02); cam_head(ab,(1,-1,0),lens=36)
        elif view=='payment':
            talk(ab,t,576,581,KEY,rest='flat',rate=6); look_at(ab,hh); face(ab,brow=-.02,eyes=.85); look_at(hz,ha); face(hz,mouth='O',eyes=1.2); cam_head(ab,(-1,-1,0),lens=40)
        elif view=='aunty':
            look_at(hz,hu,ease((t-1.0)/.5)); face(hz,mouth='flat',eyes=1.2); face(au,mouth='smirk'); cam_head(au,(-1,-1,0),lens=36)
        elif view=='cousin':
            talk(au,t,587,595,KEY,rest='smirk'); look_at(au,hh); arms(au,-14,0,5,-90,0,-25); face(au,brow=.04,brow_r=-10,eyes=.85); look_at(hz,hu); face(hz,mouth='flat',eyes=1.25); cam_head(au,(1,-1,0),lens=40)
        elif view=='down':
            k=ease((t-.3)/1.6); arms(hz,L(-45,-30,k),0,-12,L(-45,-30,k),0,12); p=(hand_w(hz,1)+hand_w(hz,-1))/2; pl.location=(p.x,p.y-.08,p.z+.05) if k<.98 else (.95,11.5,1.18)
            face(hz,mouth='flat',eyes=.6,brow=-.02); hz['head'].rotation_euler[0]=R(12*k)
            camset((L(.1,0,q),L(8.4,8.9,q),2.4),(0,11.5,2.05),L(34,44,q),3,focus=hh)
        elif view=='gaari':
            pl.location=(.95,11.5,1.18); arms(hz,-30,0,8,-30,0,-8); look_at(hz,hb); talk(hz,t,602,604,KEY,rest='flat',rate=5); face(hz,eyes=.6,brow=-.02); cam_head(hz,(1,-1,0),lens=42)
        elif view=='kahan':
            pl.location=(.95,11.5,1.18); arms(hz,-30,0,8,-30,0,-8); look_at(hz,hb); talk(bl,t,605,605,KEY,rest='o'); look_at(bl,hh); face(bl,brow=.05,eyes=1.15); cam_head(bl,(1,-1,0),lens=40)
        else:
            pl.location=(.95,11.5,1.18); arms(hz,-30,0,8,-30,0,-8); look_at(hz,hb); talk(hz,t,606,606,KEY,rest='flat'); face(hz,eyes=.55,brow=-.02)
            if t>we(606,KEY)+.2:
                for H in (am,ab,au): face(H,mouth='O',eyes=1.3)
            cam_head(hz,(1,-1,0),lens=L(42,52,q))
    return dict(upd=upd)
for v in ('over','plate','finally','bite','beta','ji','shopping','freeze','abhi','abbu','payment','aunty','cousin','down','gaari','kahan','dubai'): SHOTS['H_'+v]=(lambda v=v: SH_H(v))
# ============================================================ FINAL NARRATION
def SH_Z(view):
    KEY='Z_'+view
    if view=='escape':
        exterior(); B.done('ext'); setup_interior('night',(0,-16,7),res=PCT,samples=SAMPLES,shadow_dist=50)
        hz=person((0,-15,0),0,HAMZA,'grin',name='hamza'); bl=person((.8,-15,0),0,BILAL,'grin',name='bilal')
        def upd(t):
            hz['z0']=0; bl['z0']=0; walk_path(hz,[(0,-15.2),(-1.5,-19),(-7.6,-22.6)],t,.2,DUR-.3,step=.7,arm=34,run_=True); walk_path(bl,[(.8,-15.2),(-.6,-19.4),(-7.0,-23.6)],t,.0,DUR-.5,step=.7,arm=34,run_=True)
            blink(hz,t); blink(bl,t); face(hz,mouth='grin',eyes=1.1); face(bl,mouth='grin')
            q=ease(t/DUR); _camset((L(4.5,2.5,q),L(-27,-29,q),L(2.4,3.4,q)),(L(-.5,-5,q),L(-16,-21,q),1.2),24,8)
        return dict(upd=upd)
    stand=[(x,y,rz,'dance') for (x,y,rz) in ((-1.6,.2,10),(1.2,.4,-20),(-.2,2.4,180),(1.9,2.6,200),(0.3,-.8,0))]+[(-1.5,-9.5,90,'talk'),(-.9,-9.5,-90,'talk'),(2.0,-4.0,0,'selfie'),(-12.2,-6.5,-90,'idle'),(-12.0,-5.0,-90,'talk')]
    base,D=hall_scene(28,14,stand=stand,dance=True)
    if view=='wedding':
        hz=person((0,11.6,0),0,HAMZA,'flat',name='hamza'); am=person((AMS[0],AMS[1],0),0,AMMI,'smile',name='ammi'); ab=person((ABS[0],ABS[1],0),0,ABBU,'flat',name='abbu'); au=person((AUS[0],AUS[1],0),0,AUNTY,'smile',name='aunty'); bl=person((BLS[0],BLS[1],0),0,BILAL,'grin',name='bilal')
        def upd(t):
            base(t); seatH(hz,0,11.6,0,sh=1.12); arms(hz,-30,0,8,-30,0,-8); face(hz,mouth='flat',eyes=.6); blink(hz,t); hh=headpos(hz)
            for H,(x,y) in ((am,AMS),(ab,ABS),(au,AUS),(bl,BLS)): on_stage(H,x,y,heading_to(H,(0,11.6,0)),t); blink(H,t); rest(H,t); look_at(H,hh); face(H,mouth=('o','flat','O','smile')[int(t*6+H['seed'])%4])
            q=ease(t/DUR); _camset((L(.3,0,q),L(4.5,1.0,q),L(2.0,3.0,q)),(0,11.2,1.6),L(30,24,q),5)
        return dict(upd=upd)
    if view=='montage':
        def upd(t):
            base(t); q=t/DUR; a=R(L(-60,60,ease(q))); _camset((7.5*math.sin(a),1-7.5*math.cos(a),L(2.2,3.2,q)),(0,1,1.0),22,6)
        return dict(upd=upd)
    if view=='disaster':
        ab=person((-4.2,-2.0,0),0,ABBU,'flat',name='abbu'); nb=notebook(ab)
        def upd(t):
            base(t); ab['z0']=0; standH(ab,-4.2,-2.0,30,t); blink(ab,t); ab['arm'][-1].rotation_euler=(R(-75),0,R(10)); pn=hand_w(ab,-1); nb.location=(pn.x,pn.y,pn.z+.05); nb.rotation_euler=(R(-60),0,ab['root'].rotation_euler[2])
            hh=headpos(ab); arm_reach(ab,1,(hh[0]+.05,hh[1]-.2,hh[2]+.15)); look_at(ab,(pn.x,pn.y,pn.z)); face(ab,mouth='frown',eyes=.5,brow=-.03,brow_r=18)
            cam_head(ab,(-1,-1,0),lens=L(40,48,ease(t/DUR)))
        return dict(upd=upd)
    # groom: Hamza alone on the sofa, the hall emptying, slow push-in
    hz=person((0,11.6,0),0,HAMZA,'flat',name='hamza')
    def upd(t):
        base(t); seatH(hz,0,11.6,0,sh=1.12); arms(hz,-30,0,8,-30,0,-8); blink(hz,t); face(hz,mouth='smile' if t>wl(637,KEY) else 'flat',eyes=.7); hz['head'].rotation_euler[2]=R(10)*math.sin(t*.8)
        q=ease(t/DUR); camset((0,L(5.5,8.6,q),L(1.9,1.85,q)),(0,11.6,1.75),L(28,40,q),4,focus=headpos(hz))
    return dict(upd=upd)
for v in ('wedding','montage','disaster','groom','escape'): SHOTS['Z_'+v]=(lambda v=v: SH_Z(v))
