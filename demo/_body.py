# ============================================================ helpers for "Demo Ka Millionaire"
SEATW=(CHAIR[0]+.02,CHAIR[1])          # Waleed on the gaming chair facing the laptop (+x)
BILB=(-1.3,1.05)                        # Bilal sits on the bed edge
AMMI_P=(2.15,-1.85)                     # Ammi just inside the door
KB=(LAPTOP[0]-.08,LAPTOP[1],DESK['top']+.035)
def room(mode='day'):
    D=trading_room(mode); gaming_chair(CHAIR[0],CHAIR[1],0); B.done('room')
    setup_interior('day' if mode=='day' else 'night',(0,0,3.3),res=PCT,samples=SAMPLES,shadow_dist=12)
    bpy.context.scene.view_settings.exposure=(-.6 if mode=='day' else (.35 if mode=='night' else .5)); return D
def fan_spin(D,t,on=True): D['fan'].rotation_euler[2]=t*7.5 if on else 0
def lapscr(D,name,emit=1.0): set_screen(D['lap'],name,emit)
def sit_desk(w,t,type_=True,look=True):
    seatH(w,SEATW[0],SEATW[1],90,sh=.56); blink(w,t)
    if type_:
        arm_reach(w,1,(KB[0],KB[1]-.1,KB[2]+.012*math.sin(t*19))); arm_reach(w,-1,(KB[0],KB[1]+.1,KB[2]+.012*math.sin(t*23+1)))
    if look: look_at(w,(LAPTOP[0]+.15,LAPTOP[1],DESK['top']+.2),.8,maxpitch=10)
SCR=(2.60,LAPTOP[1],.965)
def lap_cam(q,push=.06,lens=23,w=None):
    """insert on the laptop screen from the chair, gentle push-in (Waleed hidden so the camera can sit where his eyes are)"""
    if w is not None: body_vis(w,False)
    _camset((L(2.0,2.0+push,q),SCR[1]-.01,L(1.1,1.08,q)),SCR,lens,22,focus=SCR)
def mon_cam(q):
    _camset((L(1.9,2.0,q),.62,1.3),(2.73,.82,1.33),L(19,20,q),22,focus=(2.73,.82,1.33))
def cam_close(H,side=1,dist=2.1,lens=28,ang=28,dz=.38,tz=-.25):
    h=headpos(H); rz=H['root'].rotation_euler[2]+R(side*ang); f=(math.sin(rz),-math.cos(rz))
    camset((h[0]+f[0]*dist,h[1]+f[1]*dist,h[2]+dz),(h[0],h[1],h[2]+tz),lens,2.8,focus=h)
OWNER=[None]
def body_vis(H,on):
    if '_body' not in H:
        H['_body']=[o for o in [H['root']]+list(H['root'].children_recursive) if o.type=='MESH']
    for o in H['_body']: o.hide_render=not on
def phone_in_hand(H,ph,up=2.0,face_dist=.55,raise_=0.0):
    body_vis(H,True); h=Vector(headpos(H)); M3=root_mat(H).to_3x3(); f=M3@Vector((0,-1,0)); rt=M3@Vector((1,0,0)); p=h+f*face_dist+Vector((0,0,-.25*up+raise_))
    bpy.context.view_layer.update()
    for a in (1,-1):
        sh=H['arm'][a].matrix_world.translation; side=1 if (sh-p).dot(rt)>0 else -1
        arm_reach(H,a,tuple(p+rt*side*.075+Vector((0,0,-.05))))
    ph.location=(p.x,p.y,p.z); ph.rotation_euler=(R(-28),0,H['root'].rotation_euler[2]+R(180)); return p
def phone_one(H,ph,s=1,dz=0.0,fwd=.42,side=.12):
    """phone in one hand in front of the chest"""
    h=Vector(headpos(H)); M3=root_mat(H).to_3x3(); f=M3@Vector((0,-1,0)); rt=M3@Vector((1,0,0)); p=h+f*fwd+rt*side*s+Vector((0,0,-.42+dz))
    arm_reach(H,s,tuple(p+Vector((0,0,-.06)))); ph.location=tuple(p); ph.rotation_euler=(R(-25),0,H['root'].rotation_euler[2]+R(180)); return p
def insert_cam(ph,lens=26,dist=.18):
    H=OWNER[0]
    if H: body_vis(H,False)
    bpy.context.view_layer.update(); m=ph.matrix_world; c=m@Vector((.0,-dist,.012)); tg=m@Vector((0,0,0)); _camset(tuple(c),tuple(tg),lens,22,focus=tuple(tg))
def flat_insert(ph,q,lens=26,d0=.2,d1=.17):
    """phone lying on a surface, camera straight above it"""
    p=Vector(ph.location); _camset((p.x+.001,p.y-.002,p.z+L(d0,d1,q)),tuple(p),lens,22,focus=tuple(p))
def desk_face(w,q,lens=24,push=.08):
    """3/4 front close-up from beside the laptop, looking back at Waleed at the desk"""
    hw=headpos(w); c=(L(2.55,2.5,q),L(-1.15,-1.0,q),hw[2]-.05); _camset(c,(hw[0]+.1,hw[1],hw[2]-.2),L(lens,lens+4,q),2.8,focus=hw)
def celebrate(H,t,k=1.0):
    a=-150+18*math.sin(t*9); arms(H,a*k,0,-20*k+8*math.sin(t*9),a*k,0,20*k-8*math.sin(t*9+1))
def beg(H,t):
    """palms together in front of the face, shaking"""
    h=Vector(headpos(H)); M3=root_mat(H).to_3x3(); f=M3@Vector((0,-1,0)); rt=M3@Vector((1,0,0)); p=h+f*.36+Vector((0,0,-.5+.015*math.sin(t*16)))
    arm_reach(H,1,tuple(p+rt*.03)); arm_reach(H,-1,tuple(p-rt*.03))
def helmet_on(hm,H):
    bpy.context.view_layer.update(); mw=H['head'].matrix_world; u=H['u']; hm.matrix_world=mw@Matrix.Translation((0,.02*u,.95*u))
def stomp(H,pts,t,t0,t1): return walk_path(H,pts,t,t0,t1,step=.62,arm=34,ease_in=.12,ease_out_=.2)
CLOCK=[]
# ============================================================ 1. DEMO MILLIONAIRE (day)
def SH_A(view):
    KEY='A_'+view; D=room('day'); w=person((0,0,0),90,WALEED,'grin',name='waleed'); OWNER[0]=None
    bl=person((BILB[0],BILB[1],0),70,BILAL,'smirk',name='bilal'); lapscr(D,'lap_demo',1.0)
    chips=empty((0,0,0)); obox((0,0,0),(.07,.04,.1),M('#F2C12E',.4,spec=.7),.02,chips)
    def upd(t):
        fan_spin(D,t); q=ease(t/DUR); hw=headpos(w); hb=headpos(bl)
        seatH(bl,BILB[0],BILB[1],62,sh=BEDR['top']); blink(bl,t); arms(bl,-50,0,-5,-20,0,10); carry(chips,bl,1,(0,0,-.05)); look_at(bl,hw,.7)
        if view=='hook':     # over the shoulder: $1,000,000 on screen, he throws his arms up
            sit_desk(w,t,type_=t<.9); face(w,mouth='grin' if t>.9 else 'smile',eyes=1.15)
            if t>.9: celebrate(w,t,ease((t-.9)/.35)); w['root'].location[2]+=.03*abs(math.sin(t*9))
            _camset((L(2.6,2.55,q),L(-1.7,-1.55,q),1.55),(1.9,.3,1.35),L(19,21,q),4,focus=headpos(w))
        elif view=='demo':   # insert: DEMO ACCOUNT badge
            sit_desk(w,t); lap_cam(q,.1,22,w)
        elif view=='ten':    # his face lit by the screen, grinning, spinning a little in the chair
            sit_desk(w,t,type_=True); w['root'].rotation_euler[2]=R(90+6*math.sin(t*1.6)); face(w,mouth='grin',eyes=1.1,brow=.05)
            desk_face(w,q)
        elif view=='born':   # stands up, hands on hips, low hero angle, TRADER MINDSET poster
            k=ease(t/.6); seatH(w,SEATW[0]-.25*k,SEATW[1]-.1*k,L(90,-25,k),sh=.56,k=1-k) if k<1 else standH(w,SEATW[0]-.25,SEATW[1]-.1,-25,t)
            blink(w,t); HIPS(w) if k>.6 else None; talk(w,t,27,34,KEY,rest='smirk'); face(w,brow=.06,eyes=1.05); w['head'].rotation_euler[0]=R(-6)
            camset((L(.2,.35,q),L(-1.6,-1.45,q),L(.75,.85,q)),(hw[0]-.1,hw[1],hw[2]-.2),L(20,22,q),3,focus=hw)
        elif view=='bilal':  # Bilal, deadpan, chips in hand
            standH(w,SEATW[0]-.25,SEATW[1]-.1,-75,t); HIPS(w); look_at(w,hb,.5)
            talk(bl,t,35,40,KEY,rest='flat',shapes=('flat','o','flat','O')); face(bl,brow=-.03,eyes=.85); bl['head'].rotation_euler[1]=R(8)
            arms(bl,-50,0,-5,-60+15*math.sin(t*5),0,25); carry(chips,bl,1,(0,0,-.05))
            camset((L(.4,.25,q),L(-.15,-.05,q),1.25),(hb[0],hb[1],hb[2]-.18),L(28,32,q),2.8,focus=hb)
        elif view=='skill':  # taps his temple, confident
            standH(w,SEATW[0]-.25,SEATW[1]-.1,-75,t); look_at(w,hb,.6); talk(w,t,41,46,KEY,rest='smirk'); face(w,brow=.07,eyes=1.1)
            hp=Vector(hw); M3=root_mat(w).to_3x3(); k=math.sin(pi*min(1,max(0,(t-wl(44,KEY))/1.0)))
            arm_reach(w,1,tuple(hp+M3@Vector((.3,-.06,-.02))*k+Vector(hand_w(w,1))*0)) if k>0 else arms(w,-10,0,-38,-10,0,38)
            arms(w,-10,0,38,w['arm'][1].rotation_euler[0]*180/pi,0,w['arm'][1].rotation_euler[2]*180/pi) if False else None
            cam_close(w,-1,1.8,30)
    return dict(upd=upd)
for v in ('hook','demo','ten','born','bilal','skill'): SHOTS['A_'+v]=(lambda v=v: SH_A(v))
# ============================================================ 2. THE USTAAD (day)
def SH_B(view):
    KEY='B_'+view; D=room('day'); w=person((0,0,0),90,WALEED,'smile',name='waleed'); OWNER[0]=w
    ph,scr=phone_obj('ph_profile'); en=empty((0,0,0)); notes=[note_obj('note5000') for _ in range(4)]
    def upd(t):
        fan_spin(D,t); q=ease(t/DUR); hw=headpos(w); body_vis(w,True)
        for n in notes: n.location=(9,9,-9)
        if view=='scroll':   # leaning back in the chair, scrolling, eyebrows up
            seatH(w,SEATW[0],SEATW[1],-30,sh=.56); blink(w,t); phone_in_hand(w,ph,up=1.6); face(w,mouth='o' if t>1.2 else 'smile',eyes=1.2,brow=.05)
            w['head'].rotation_euler[0]=R(16)
            cam_close(w,1,1.6,28,ang=20)
        elif view=='prof':   # insert: Sir Zain's profile, slow push
            seatH(w,SEATW[0],SEATW[1],-30,sh=.56); phone_in_hand(w,ph,up=1.6); insert_cam(ph,L(24,30,q),L(.2,.17,q))
        elif view=='fees':   # payment sent
            seatH(w,SEATW[0],SEATW[1],-30,sh=.56); phone_in_hand(w,ph,up=1.6); set_screen(scr,'ph_paid'); insert_cam(ph,26,.19)
        elif view=='eidi':   # empties the Eidi envelope and the bike jar onto the desk
            sit_desk(w,t,type_=False,look=False); look_at(w,(DESK['x']-.1,DESK['y']-.65,DESK['top']),.9); face(w,mouth='strain' if t%1.4<.7 else 'smile',eyes=1.0)
            jar=Vector((DESK['x']-.05,DESK['y']-.82,DESK['top']+.22)); env=Vector((DESK['x']-.12,DESK['y']-.55,DESK['top']+.02))
            for i,n in enumerate(notes):
                ti=.3+i*.42; k=max(0,min(1,(t-ti)/.4)); src=env if i%2==0 else jar; dst=Vector((KB[0]-.18+i*.03,KB[1]-.32+i*.06,DESK['top']+.004+i*.002))
                p=src.lerp(dst,ease(k))+Vector((0,0,.12*math.sin(pi*k))); n.location=tuple(p); n.rotation_euler=(0,0,R(20*i+60*k))
                if 0<k<1: arm_reach(w,1 if i%2 else -1,tuple(p)) if False else None
            kk=(t*1.4)%1; arm_reach(w,-1,tuple(env.lerp(Vector((KB[0]-.15,KB[1]-.25,DESK['top']+.05)),math.sin(pi*kk)))); arm_reach(w,1,tuple(jar+Vector((0,.05,-.05))))
            _camset((L(2.0,2.08,q),L(-1.55,-1.45,q),L(1.35,1.3,q)),(2.38,-.5,.84),L(26,30,q),4,focus=(2.4,-.55,.82))
        elif view=='kul':    # REAL ACCOUNT Rs 20,000
            sit_desk(w,t); lapscr(D,'lap_real',1.0)
            for i,n in enumerate(notes): n.location=(KB[0]-.18+i*.03,KB[1]-.32+i*.06,DESK['top']+.004+i*.002); n.rotation_euler=(0,0,R(20*i+60))
            lap_cam(q,.1,22,w)
    return dict(upd=upd)
for v in ('scroll','prof','fees','eidi','kul'): SHOTS['B_'+v]=(lambda v=v: SH_B(v))
# ============================================================ 3. FIRST TRADE + PIZZA (day)
def SH_C(view):
    KEY='C_'+view; D=room('day'); w=person((0,0,0),90,WALEED,'smile',name='waleed'); bl=person((BILB[0],BILB[1],0),70,BILAL,'smile',name='bilal'); ph,scr=phone_obj('ph_signal')
    lapscr(D,'lap_real' if view=='first' else 'lap_green',1.0)
    def upd(t):
        fan_spin(D,t); q=ease(t/DUR); hw=headpos(w); hb=headpos(bl)
        seatH(bl,BILB[0],BILB[1],62,sh=BEDR['top']); blink(bl,t); arms(bl,-25,0,5,-25,0,-5); look_at(bl,hw,.6); ph.location=(9,9,-9)
        if view=='first':    # finger hovering, then click; tense close
            sit_desk(w,t,type_=False); face(w,mouth='strain',eyes=1.25,brow=-.03)
            k=ease((t-.3)/.9); arm_reach(w,1,(KB[0]-.02,KB[1]-.05,KB[2]+L(.12,.0,k)+(.0 if t<1.3 else .01*math.sin(t*30)))); arms(w,-30,0,10,w['arm'][1].rotation_euler[0]*180/pi,0,w['arm'][1].rotation_euler[2]*180/pi) if False else arm_reach(w,-1,(KB[0]+.02,KB[1]+.2,KB[2]))
            desk_face(w,q)
        elif view=='green':  # insert green candle +Rs 200
            sit_desk(w,t); lap_cam(q,.12,22,w)
        elif view=='jump':   # jumps up from the chair, both arms up
            k=ease(t/.4);
            if k<1: seatH(w,SEATW[0]-.2*k,SEATW[1],90,sh=.56,k=1-k)
            else: standH(w,SEATW[0]-.2,SEATW[1],L(90,-30,ease((t-.4)/.6)),t); w['root'].location[2]+=max(0,.12*math.sin((t-.4)*7)) if t<1.3 else 0
            celebrate(w,t,k); face(w,mouth='grin',eyes=1.25,brow=.06); blink(w,t)
            look_at(bl,hw,.8); face(bl,mouth='smile')
            _camset((L(.2,.35,q),L(-1.55,-1.45,q),1.35),(hw[0]-.2,hw[1],hw[2]-.3),L(19,21,q),3.5,focus=hw)
        else:                # 'call': "Bilal! Pizza mangwa" — points at Bilal; Bilal grabs his phone
            standH(w,SEATW[0]-.2,SEATW[1],heading_to(w,hb),t); blink(w,t); talk(w,t,83,90,KEY,rest='grin',shapes=('shout','O','grin','O')); face(w,eyes=1.2,brow=.05)
            hp=Vector(hb); arm_reach(w,1,tuple(Vector(hw).lerp(hp,.35)+Vector((0,0,-.25)))) ; arms(w,0,0,0,-15,0,-30) if False else None
            look_at(w,hb,.8); k=ease((t-wl(84,KEY))/.5); face(bl,mouth='grin' if k>0 else 'O',eyes=1.15)
            if k>0: phone_one(bl,ph,1,dz=.1*k); set_screen(scr,'ph_map')
            d_=(Vector(hb)-Vector(hw)); d_.z=0; d_.normalize(); sd=Vector((-d_.y,d_.x,0)); c=Vector(hb)+d_*.75+sd*.45+Vector((0,0,.15)); _camset(tuple(c+Vector((0,0,0))*q),(hw[0],hw[1],hw[2]-.25),L(24,27,q),3,focus=hw)
    return dict(upd=upd)
for v in ('first','green','jump','call'): SHOTS['C_'+v]=(lambda v=v: SH_C(v))
# ============================================================ 4. PIZZA AT THE GATE (evening)
GW=(GX+.25,-.55); GB=(GX-.75,-.5); RB=(GX+1.25,-1.95); BIKEP=(GX+2.6,-2.2)
def SH_D(view):
    KEY='D_'+view; gate_street(); B.done('gate'); setup_render('golden',res=PCT,samples=SAMPLES,shadow_dist=30)
    w=person((GW[0],GW[1],0),0,WALEED,'grin',name='waleed'); bl=person((GB[0],GB[1],0),0,BILAL,'grin',name='bilal'); rd=person((RB[0],RB[1],0),150,ZAIN_RIDER,'flat',name='rider')
    hm=helmet_obj(); bk=bike(BIKEP[0],BIKEP[1],0,'#C8102E'); bx=pizza_box()
    def upd(t):
        q=ease(t/DUR); hw=headpos(w); hr=headpos(rd); hb=headpos(bl)
        standH(rd,RB[0],RB[1],145,t); blink(rd,t); helmet_on(hm,rd); face(rd,mouth='flat')
        standH(w,GW[0],GW[1],-20,t); standH(bl,GB[0],GB[1],-10,t); blink(w,t); blink(bl,t); look_at(bl,hr,.7)
        if view=='give':     # rider hands over the box, Waleed takes it, rider walks to the bike
            k=ease((t-.2)/.7); mid=Vector(((hw[0]+hr[0])/2,(hw[1]+hr[1])/2,1.05))
            if t<1.2:
                bx.location=tuple(Vector(hand_w(rd,1)).lerp(mid,k)); arm_reach(rd,1,tuple(bx.location+Vector((.12,0,-.02)))); arm_reach(rd,-1,tuple(bx.location+Vector((-.12,.05,-.02))))
                arm_reach(w,1,tuple(bx.location+Vector((.1,.12,-.03))) ) if k>.6 else rest(w,t)
            else:
                bx.location=tuple(mid); arm_reach(w,1,tuple(mid+Vector((.13,.05,-.03)))); arm_reach(w,-1,tuple(mid+Vector((-.13,.05,-.03))))
                walk_path(rd,[RB,(RB[0]+.6,RB[1]-.6),(BIKEP[0]-.3,BIKEP[1]-.75)],t,1.3,DUR+.4,step=.5,arm=20); helmet_on(hm,rd)
            bx.rotation_euler=(0,0,R(-15)); look_at(w,tuple(bx.location),.6); face(w,mouth='grin',eyes=1.15)
            camset((L(GX-2.4,GX-2.0,q),L(-5.6,-5.2,q),1.6),(GX+.6,-1.1,1.2),L(22,24,q),4,focus=hr)
        else:                # 'lid': the box lid reads TOTAL Rs 3,000; Bilal leans in
            mid=Vector((hw[0]+.05,hw[1]-.42,.95)); bx.location=tuple(mid); bx.rotation_euler=(R(70),0,R(-20)); body_vis(w,False); arm_reach(w,1,tuple(mid+Vector((.13,.02,-.06)))); arm_reach(w,-1,tuple(mid+Vector((-.13,.02,-.06))))
            look_at(w,tuple(mid),.7); face(w,mouth='smile',eyes=1.0); look_at(bl,tuple(mid),.8); face(bl,mouth='O',eyes=1.2)
            walk_path(rd,[(BIKEP[0]-.3,BIKEP[1]-.75),(BIKEP[0]+3,BIKEP[1]-.9)],t,0,DUR,step=.5,arm=20); helmet_on(hm,rd)
            n=Euler(bx.rotation_euler).to_matrix()@Vector((0,0,1)); bpy.context.view_layer.update(); c=mid+n*L(.7,.6,q); _camset(tuple(c),tuple(mid),24,8,focus=tuple(mid))
    return dict(upd=upd)
for v in ('give','lid'): SHOTS['D_'+v]=(lambda v=v: SH_D(v))
# ============================================================ 5. PIZZA PARTY (evening, room)
def SH_E(view):
    KEY='E_'+view; D=room('day'); w=person((0,0,0),0,WALEED,'grin',name='waleed'); bl=person((0,0,0),0,BILAL,'grin',name='bilal')
    bx=pizza_box(); sl=[empty((0,0,0)) for _ in range(2)]
    for e in sl: omesh([(0,0,0),(.16,-.05,0),(.16,.05,0)],[(0,1,2)],M('#F2B84A',.6),e,thick=.012); obox((.15,0,.008),(.02,.055,.01),M('#C9843A',.6),.005,e)
    lapscr(D,'lap_green',1.0)
    def upd(t):
        fan_spin(D,t); q=ease(t/DUR)
        seatH(w,-1.3,.75,90,sh=BEDR['top']); seatH(bl,-1.3,1.75,90,sh=BEDR['top']); blink(w,t); blink(bl,t)
        bx.location=(-1.45,1.25,BEDR['top']+.05); bx.rotation_euler=(0,0,R(10))
        for i,(H,e) in enumerate(((w,sl[0]),(bl,sl[1]))):
            hp=Vector(headpos(H)); ph_=(t*.9+i*.5)%1; k=math.sin(pi*ph_); src=Vector((-1.45,1.25+(-.12 if i==0 else .12),BEDR['top']+.1)); mouth=hp+Vector((.18,0,-.2))
            p=src.lerp(mouth,k); arm_reach(H,1 if i==0 else -1,tuple(p)); e.location=tuple(p+Vector((.02,0,.02))); e.rotation_euler=(0,R(-20),R(180))
            face(H,mouth='O' if k>.8 else 'grin',eyes=1.1); look_at(H,headpos(bl if i==0 else w),.2)
        _camset((L(1.4,1.2,q),L(-1.2,-.9,q),L(1.6,1.5,q)),(-1.35,1.25,.95),L(22,25,q),4,focus=(-1.3,1.25,1.1))
    return dict(upd=upd)
SHOTS['E_party']=lambda: SH_E('party')
# ============================================================ 6. THE SIGNAL (night)
def SH_F(view):
    KEY='F_'+view; mode='dark' if view in ('cut','wifi','open') else 'night'
    D=room('night'); w=person((0,0,0),90,WALEED,'flat',name='waleed'); OWNER[0]=w; ph,scr=phone_obj('ph_signal')
    am=person((AMMI_P[0],-3.4,0),180,AMMI,'frown',name='ammi'); lapscr(D,'lap_real',.8); set_screen(D['mon'],'lap_real',.8)
    def lights(on):
        for k_,a in D['L'].items(): a.data.energy=a['e0'] if on else (a['e0']*(.35 if k_=='scr' else .04))
        for m_,e0 in ((D['panel'],.6),(D['strip'],5)):
            m=m_.data.materials[0]; m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=e0 if on else 0
        for l in D['leds']: l.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=6 if on else 0
        set_screen(D['mon'],'lap_red2' if on else 'lap_noint',1.2 if on else 0.0)
    for a in D['L'].values(): a['e0']=a.data.energy
    def upd(t):
        q=ease(t/DUR); hw=headpos(w); body_vis(w,True)
        am['root'].location=(9,-9,0); door_set(D,0); lights(True); fan_spin(D,t)
        ph.location=(KB[0]-.25,KB[1]-.45,DESK['top']+.008); ph.rotation_euler=(0,0,R(-90))
        if view=='night':    # dark room, phone on the desk lights up and buzzes
            sit_desk(w,t,type_=False,look=False); look_at(w,tuple(ph.location),.9*ease((t-.8)/.4)); face(w,mouth='flat' if t<1 else 'O',eyes=1.1)
            lapscr(D,'lap_real',.8); buzz=.004*math.sin(t*90) if (t%1.0)<.5 else 0; ph.location=(ph.location[0]+buzz,ph.location[1],ph.location[2])
            set_screen(scr,'ph_signal',1.6)
            _camset((L(.3,.6,q),L(-1.3,-1.0,q),L(2.0,1.8,q)),(2.4,-.2,.95),L(20,24,q),4,focus=(2.3,-.25,.85))
        elif view=='sig':    # insert: the signal message
            sit_desk(w,t,type_=False); phone_in_hand(w,ph,up=1.7); set_screen(scr,'ph_signal',1.4); insert_cam(ph,L(24,28,q),.19)
        elif view=='allin':  # slams PLACE ORDER, determined
            sit_desk(w,t,type_=False); lapscr(D,'lap_buy',.8); face(w,mouth='strain' if t<.8 else 'smirk',eyes=1.15,brow=-.04)
            k=ease((t-.4)/.3); arm_reach(w,1,(KB[0]-.02,KB[1]-.06,KB[2]+L(.16,.0,k))); arm_reach(w,-1,(KB[0]+.02,KB[1]+.2,KB[2]))
            desk_face(w,q)
        elif view=='nosl':   # insert: stop loss field is empty (push toward the right of the screen)
            sit_desk(w,t); lapscr(D,'lap_buy',.75); body_vis(w,False); D['L']['scr'].data.energy=0; tg=(SCR[0],L(.2,.1,q),L(.965,.955,q))
            _camset((L(2.0,2.25,q),L(.19,.1,q),L(1.08,1.0,q)),tg,L(20,24,q),22,focus=tg)
        elif view=='red':    # candles turn red, more red
            sit_desk(w,t,type_=False); n=min(3,int(t/DUR*4)); lapscr(D,'lap_red%d'%n,.8); D['L']['scr'].data.energy=0; lap_cam(q,.1,22,w)
        elif view=='beg':    # begs the screen, red light on his face
            sit_desk(w,t,type_=False); lapscr(D,'lap_red3',.9); beg(w,t); talk(w,t,139,147,KEY,rest='frown',shapes=('O','frown','o','strain')); face(w,eyes=1.3,brow=.08)
            w['root'].location[0]+=.08*ease(t/1.2)
            desk_face(w,q)
        elif view in ('ammi','sale'):
            sit_desk(w,t,type_=False); lapscr(D,'lap_red3',.9); standH(am,AMMI_P[0],AMMI_P[1],heading_to(am,hw),t); door_set(D,1); blink(am,t)
            if view=='ammi':
                k=ease(t/.6); walk_path(am,[(2.0,-3.4),(2.05,-2.6),AMMI_P],t,0,.9,step=.42,arm=14); door_set(D,k); look_at(am,(2.6,.2,1.0),.6)
                talk(am,t,148,152,KEY,rest='frown'); face(am,brow=-.05,eyes=1.1); arms(am,-20,0,-30,-20,0,30)
                w['root'].rotation_euler[2]=R(90+25*ease((t-.8)/.5)); face(w,mouth='O',eyes=1.3)
                camset((L(.2,.35,q),L(-.4,-.55,q),1.6),((AMMI_P[0]+hw[0])/2,(AMMI_P[1]+hw[1])/2,1.25),L(18,20,q),4,focus=headpos(am))
            else:
                w['root'].rotation_euler[2]=R(heading_to(w,headpos(am))); look_at(w,headpos(am),.8); talk(w,t,153,157,KEY,rest='smile',shapes=('grin','o','grin','flat')); face(w,eyes=1.25,brow=.08)
                arms(w,-40,0,-10,-60,0,30*math.sin(t*4)); look_at(am,hw,.8); face(am,mouth='frown',eyes=.9,brow=-.06); arms(am,-62,0,-58,-62,0,58)
                cam_close(w,1,1.7,30,ang=20)
        elif view=='cut':    # the power goes: everything off, only the laptop on battery
            sit_desk(w,t,type_=False); lapscr(D,'lap_red3',.9); on=t<.55; lights(on); fan_spin(D,t,on)
            face(w,mouth='O' if not on else 'frown',eyes=1.35); look_at(w,(0,0,3.2),.6*(0 if on else ease((t-.6)/.4)))
            _camset((L(.2,.3,q),L(-1.4,-1.3,q),1.9),(1.9,.2,1.1),20,4,focus=hw)
        elif view=='wifi':   # router lights go out
            sit_desk(w,t,type_=False); lights(t<.35)
            c=(RM['x1']-.95,DESK['y']-.6,1.82); _camset(c,(RM['x1']-.25,DESK['y']-.75,1.78),L(30,34,q),5,focus=(RM['x1']-.22,DESK['y']-.75,1.78))
        else:                # 'open': laptop on battery: no internet, trade still open
            sit_desk(w,t,type_=False); lights(False); lapscr(D,'lap_noint',.8); lap_cam(q,.1,22,w)
    return dict(upd=upd)
for v in ('night','sig','allin','nosl','red','beg','ammi','sale','cut','wifi','open'): SHOTS['F_'+v]=(lambda v=v: SH_F(v))
# ============================================================ 7. ROOFTOP, no signal (night)
DOORR=(RX-3.6,RY+2.1)
def SH_G(view):
    KEY='G_'+view; rooftop(); B.done('roof'); setup_interior('night',(RX,RY,6),res=PCT,samples=SAMPLES,shadow_dist=20); bpy.context.scene.view_settings.exposure=.25
    w=person((DOORR[0],DOORR[1],0),0,WALEED,'O',name='waleed'); OWNER[0]=w; ph,scr=phone_obj('ph_nosignal')
    glow=point((0,0,0),2.5,(.7,.85,1.0),.05,shadow=False)
    def upd(t):
        q=ease(t/DUR); hw=headpos(w); body_vis(w,True)
        if view=='run':      # bursts out of the stair door and runs to the middle, phone up
            walk_path(w,[DOORR,(RX-2.6,RY+.8),(RX-.6,RY-.6),(RX+.4,RY-1.0)],t,0,DUR-.2,run_=True,arm=40,ease_in=.15,ease_out_=.3); blink(w,t)
            p=hand_w(w,1); ph.location=(p.x,p.y,p.z); ph.rotation_euler=(R(-60),0,w['root'].rotation_euler[2]+R(180)); face(w,mouth='O',eyes=1.25)
            camset((L(RX+1.8,RX+2.2,q),L(RY-4.2,RY-3.6,q),L(1.5,1.6,q)),(hw[0],hw[1],hw[2]-.3),L(18,22,q),4,focus=hw)
        elif view=='up':     # phone held high, turning around searching for a signal
            standH(w,RX+.4,RY-1.0,L(-20,60,ease(t/DUR))+15*math.sin(t*2.2),t); blink(w,t)
            k=.5+.5*math.sin(t*3); h=Vector(hw); M3=root_mat(w).to_3x3(); p=h+M3@Vector((.18,-.25,.55+.12*k))
            arm_reach(w,1,tuple(p)); arms(w,-10,0,10,w['arm'][1].rotation_euler[0]*180/pi,0,w['arm'][1].rotation_euler[2]*180/pi) if False else None
            ph.location=tuple(p+Vector((0,0,.06))); ph.rotation_euler=(R(-75),0,w['root'].rotation_euler[2]+R(180)); look_at(w,tuple(ph.location),.9); face(w,mouth='frown',eyes=1.2,brow=.06)
            glow.location=tuple(Vector(hw)+M3@Vector((0,-.4,.1)))
            cam_close(w,-1,2.3,22,ang=15,dz=-.35,tz=.25)
        else:                # 'nosig' / 'nodata' inserts on the phone, hand shaking
            standH(w,RX+.4,RY-1.0,10,t); phone_in_hand(w,ph,up=1.4); set_screen(scr,'ph_nosignal' if view=='nosig' else 'ph_nodata',1.4)
            ph.location=(ph.location[0]+.003*math.sin(t*11),ph.location[1],ph.location[2]); insert_cam(ph,L(24,28,q),.2)
    return dict(upd=upd)
for v in ('run','up','nosig','nodata'): SHOTS['G_'+v]=(lambda v=v: SH_G(v))
# ============================================================ 8. MOBILE SHOP, Rs 100 package (night)
WS_=(SX+.15,SHOP['y']-1.62); KS_=(SX-.1,SHOP['y']-.3)
def SH_H(view):
    KEY='H_'+view; S=shop_street(); B.done('shop'); setup_interior('night',(SX,0,6),res=PCT,samples=SAMPLES,shadow_dist=20); bpy.context.scene.view_settings.exposure=.05
    w=person((WS_[0],WS_[1],0),180,WALEED,'frown',name='waleed'); OWNER[0]=w; point((SX-3.4,-.6,2.4),60 if view in ('ask','reply') else 0,(.75,.8,1.0),.4,shadow=False); sk=person((KS_[0],KS_[1],0),0,SHOPK,'flat',name='shopk')
    nt=note_obj('note100'); ph,scr=phone_obj('ph_pkg'); kph,_=phone_obj('ph_pkg')
    def upd(t):
        q=ease(t/DUR); hw=headpos(w); hs=headpos(sk); body_vis(w,True)
        standH(sk,KS_[0],KS_[1],0,t); blink(sk,t); standH(w,WS_[0],WS_[1],180,t); blink(w,t)
        if view=='pay':      # hands his last Rs 100 over the counter; shopkeeper types the package
            k=ease((t-.2)/.7); cnt=Vector((SX+.05,SHOP['y']-.75,1.06))
            p=Vector(hand_w(w,1)) if k<=0 else Vector(((hw[0]+.05),hw[1]+.35,1.12)).lerp(cnt+Vector((0,0,.1)),k)
            if t<1.6: arm_reach(w,1,tuple(p)); nt.location=tuple(p+Vector((0,0,.03))); nt.rotation_euler=(R(-80),0,0)
            else: nt.location=tuple(Vector(hand_w(sk,-1))+Vector((0,0,.02))); rest(w,t,-15)
            if t>1.4: kk=ease((t-1.4)/.4); phone_one(sk,kph,1,dz=.05*kk,fwd=.4); arm_reach(sk,-1,tuple(Vector(kph.location)+Vector((-.06,0,-.04)))) ; look_at(sk,tuple(kph.location),.9)
            else: look_at(sk,tuple(p),.7); arms(sk,-35,0,-10,-35,0,10); kph.location=(9,9,-9)
            face(sk,mouth='flat'); face(w,mouth='frown',eyes=1.1,brow=.05); look_at(w,hs,.6); ph.location=(9,9,-9)
            camset((L(SX+2.0,SX+1.85,q),L(.0,.15,q),1.7),((hw[0]+hs[0])/2,(hw[1]+hs[1])/2,1.35),L(19,21,q),4,focus=hs)
        elif view=='app':    # steps back from the counter, opens the app, hopeful
            phone_in_hand(w,ph,up=1.6); set_screen(scr,'ph_pkg',1.3); face(w,mouth='smile',eyes=1.2,brow=.06); look_at(sk,hw,.6); arms(sk,-35,0,-10,-35,0,10)
            w['root'].rotation_euler[2]=R(L(180,10,ease(t/.6)))
            camset((L(SX+.1,SX+.15,q),L(SHOP['y']-3.4,SHOP['y']-3.1,q),L(1.5,1.45,q)),(hw[0],hw[1],hw[2]-.25),L(26,32,q),2.8,focus=hw)
        elif view=='zero':   # insert: balance Rs 0
            phone_in_hand(w,ph,up=1.6); set_screen(scr,'ph_zero',1.4); insert_cam(ph,L(22,30,q),.2)
        elif view=='ask':    # sits on the shop step, types to Sir Zain
            seatH(w,SX-3.6,SHOP['y']-.95,10,sh=.13); blink(w,t); phone_in_hand(w,ph,up=1.4,face_dist=.5); set_screen(scr,'ph_chat1',1.3)
            talk(w,t,189,192,KEY,rest='frown',shapes=('o','frown','o')); face(w,eyes=.8,brow=.1); w['head'].rotation_euler[0]=R(18)
            for s in (1,-1): w['leg'][s].rotation_euler[0]=-R(70)
            _camset((L(SX-4.5,SX-4.35,q),L(-.7,-.55,q),L(1.1,1.05,q)),(hw[0],hw[1],hw[2]-.3),L(24,28,q),2.8,focus=hw)
        else:                # 'reply': insert, the reply comes in
            seatH(w,SX-3.6,SHOP['y']-.95,10,sh=.13); phone_in_hand(w,ph,up=1.4,face_dist=.5); set_screen(scr,'ph_chat1' if t<.5 else 'ph_chat2',1.3)
            for s in (1,-1): w['leg'][s].rotation_euler[0]=-R(70)
            insert_cam(ph,L(24,27,q),.2)
    return dict(upd=upd)
for v in ('pay','app','zero','ask','reply'): SHOTS['H_'+v]=(lambda v=v: SH_H(v))
# ============================================================ 9. THE "OFFICE" (afternoon, main road)
BKP=(PX+2.6,-1.75); RDR=(PX+2.2,-1.0); WLK=[(PX-9,-.45),(PX-4,-.5),(PX+.6,-.55),(PX+1.05,-.65)]
def SH_I(view):
    KEY='I_'+view; R_=main_road(); B.done('road'); setup_render('afternoon',res=PCT,samples=SAMPLES,shadow_dist=40)
    w=person((WLK[0][0],WLK[0][1],0),-90,WALEED,'frown',name='waleed'); OWNER[0]=w; zr=person((RDR[0],RDR[1],0),90,ZAIN_RIDER,'flat',name='zain')
    hm=helmet_obj(); bk=bike(BKP[0],BKP[1],0,'#C8102E'); ph,scr=phone_obj('ph_map')
    def upd(t):
        q=ease(t/DUR); hw=headpos(w); hz=headpos(zr); body_vis(w,True)
        standH(zr,RDR[0],RDR[1],100,t); blink(zr,t); helmet_on(hm,zr); arms(zr,-20,0,-10,-20,0,10); face(zr,mouth='flat')
        if view=='walk':     # storms along the footpath, phone with the map
            stomp(w,WLK[:3],t,0,DUR+1.2); blink(w,t); phone_one(w,ph,1,dz=.05); face(w,mouth='frown',brow=-.07,eyes=1.0)
            camset((hw[0]+L(2.6,2.2,q),hw[1]-2.4,1.55),(hw[0],hw[1],hw[2]-.3),L(22,24,q),3.5,focus=hw)
        elif view=='map':    # insert: "Sir Zain Trading Office"
            standH(w,WLK[2][0],WLK[2][1],-90,t); phone_in_hand(w,ph,up=1.6); insert_cam(ph,L(24,28,q),.2)
        elif view=='reveal': # he stops, looks up: PIZZA POINT. The rider in the red jacket by the door
            standH(w,WLK[2][0],WLK[2][1],L(-90,-160,ease(t/.8)),t); blink(w,t); look_at(w,(PX,1.0,3.0),.8*ease(t/.8)); face(w,mouth='O',eyes=1.25,brow=.06)
            p=hand_w(w,1); ph.location=(p.x,p.y,p.z); rest(w,t,-15)
            camset((L(PX-2.8,PX-2.4,q),L(-4.6,-4.2,q),L(1.2,1.35,q)),(PX+.6,.4,L(1.6,2.4,q)),L(17,19,q),5,focus=hw)
        elif view=='helmet': # rider takes off the helmet: it's Sir Zain. "Aap? Aur Lamborghini?"
            standH(w,WLK[3][0],WLK[3][1],-75,t); blink(w,t); look_at(w,hz,.9); ph.location=(9,9,-9); rest(w,t,-12)
            standH(zr,RDR[0],RDR[1],100,t); k=ease((t-.15)/.8); u=zr['u']
            if k<=0: helmet_on(hm,zr)
            else:
                bpy.context.view_layer.update(); top=Matrix(zr['head'].matrix_world)@Vector((0,.02*u,.95*u)); hand=Vector(hand_w(zr,1))
                hp=top.lerp(Vector((hz[0]+.25,hz[1]-.25,hz[2]-.55)),k)+Vector((0,0,.18*math.sin(pi*min(1,k*1.2)))); hm.location=tuple(hp); hm.rotation_euler=(R(-40*k),0,R(100))
                arm_reach(zr,1,tuple(hp+Vector((.12,0,-.05)))); arm_reach(zr,-1,tuple(hp+Vector((-.12,0,-.05)))) if k<.7 else arms(zr,-15,0,-10,-15,0,10)
            face(zr,mouth='smile' if k>.9 else 'flat',eyes=1.0); look_at(zr,hw,.7*k)
            talk(w,t,216,218,KEY,rest='O',shapes=('O','shout','O','o')); face(w,eyes=1.35,brow=.08)
            camset((L(PX+1.0,PX+1.15,q),L(-4.3,-4.0,q),1.65),((hw[0]+hz[0])/2,(hw[1]+hz[1])/2,1.4),L(24,26,q),3,focus=hz)
        elif view=='show':   # Sir Zain points at the car showroom next door: the Lamborghini is behind the glass
            standH(w,WLK[3][0],WLK[3][1],-60,t); look_at(w,(SHW['x'],2.0,1.0),.8*ease((t-.6)/.5)); blink(w,t); ph.location=(9,9,-9)
            hm.location=(BKP[0]-.55,BKP[1],1.38); hm.rotation_euler=(0,0,R(30))
            standH(zr,RDR[0],RDR[1],L(100,60,ease(t/.5)),t); talk(zr,t,219,223,KEY,rest='smile',shapes=('o','flat','O','smile')); face(zr,brow=.05,eyes=.9)
            k=ease(t/.5); arm_reach(zr,1,tuple(Vector(hz)+Vector((.55*k,.15,-.25)))); arms(zr,-15,0,-10,-15,0,10) if False else None
            c=(L(PX+3.0,PX+5.2,q),L(-3.6,-4.4,q),1.5); camset(c,(L(PX+2.4,SHW['x'],q),L(-1.0,2.2,q),L(1.5,1.2,q)),L(22,18,q),5,focus=(L(PX+2.4,SHW['x'],q),L(-1,2.5,q),1.3))
        else:                # 'loss': "Bhai, main bhi loss mein hoon" — sheepish; Waleed deadpan
            standH(w,WLK[3][0],WLK[3][1],-75,t); look_at(w,hz,.9); face(w,mouth='flat',eyes=.75,brow=-.04); ph.location=(9,9,-9); rest(w,t,-12)
            hm.location=(BKP[0]-.55,BKP[1],1.38); hm.rotation_euler=(0,0,R(30)); standH(zr,RDR[0],RDR[1],100,t); look_at(zr,hw,.6)
            talk(zr,t,224,229,KEY,rest='frown',shapes=('o','frown','o','flat')); face(zr,eyes=.9,brow=.1); arms(zr,-25,0,-50,-25,0,50); zr['head'].rotation_euler[1]=R(-6)
            cam_close(zr,1,1.9,28,ang=24)
    return dict(upd=upd)
for v in ('walk','map','reveal','helmet','show','loss'): SHOTS['I_'+v]=(lambda v=v: SH_I(v))
# ============================================================ 10. BACK TO DEMO (night, room)
def SH_J(view):
    KEY='J_'+view; D=room('night'); w=person((0,0,0),90,WALEED,'smile',name='waleed'); am=person((AMMI_P[0],-3.4,0),180,AMMI,'smirk',name='ammi')
    nt=note_obj('note100'); lapscr(D,'lap_demo',.85); set_screen(D['mon'],'lap_demo',.8)
    def upd(t):
        q=ease(t/DUR); hw=headpos(w); fan_spin(D,t); am['root'].location=(9,-9,0); door_set(D,0); nt.location=(9,9,-9)
        if view=='home':     # walks in tired, drops into the chair, opens the demo account
            if t<1.6:
                walk_path(w,[(2.0,-2.3),(1.6,-1.0),(SEATW[0]-.05,SEATW[1]-.55)],t,0,1.6,step=.44,arm=12,mood=1); face(w,mouth='frown',eyes=.7); door_set(D,1-ease((t-1.0)/.6))
            else:
                k=ease((t-1.6)/.6); seatH(w,SEATW[0],SEATW[1]-.55*(1-k),L(30,90,k),sh=.56,k=k); face(w,mouth='flat',eyes=.8)
                if t>2.2: arm_reach(w,1,(KB[0],KB[1]-.1,KB[2]+.01*math.sin(t*19))); arm_reach(w,-1,(KB[0],KB[1]+.1,KB[2]))
            blink(w,t); _camset((L(-.4,-.1,q),L(-1.7,-1.4,q),L(2.0,1.85,q)),(L(1.8,2.1,q),L(-1.2,.1,q),1.0),L(19,22,q),5,focus=hw)
        elif view=='happy':  # "Yahan main ab bhi millionaire hoon" — content smile, glow on the face
            sit_desk(w,t,type_=False); arms(w,-60,0,-5,-60,0,5); talk(w,t,241,246,KEY,rest='smile',shapes=('smile','o','grin','o')); face(w,eyes=1.05,brow=.04)
            w['root'].rotation_euler[2]=R(90+8*math.sin(t*1.2))
            desk_face(w,q)
        else:                # 'milk' + 'cta': Ammi at the door with Rs 100
            door_set(D,1); standH(am,AMMI_P[0],AMMI_P[1],heading_to(am,hw),t); blink(am,t); look_at(am,hw,.8)
            if view=='milk':
                sit_desk(w,t,type_=False); w['root'].rotation_euler[2]=R(L(90,heading_to(w,headpos(am)),ease(t/.6))); look_at(w,headpos(am),.7); face(w,mouth='flat',eyes=.9)
                talk(am,t,247,255,KEY,rest='smirk',shapes=('o','smirk','O','flat')); face(am,eyes=.95,brow=.04)
                hp=Vector(hand_w(am,1)); arm_reach(am,1,tuple(Vector(headpos(am))+Vector((-.25,.35,-.45)))); nt.location=tuple(Vector(hand_w(am,1))+Vector((0,0,.03))); nt.rotation_euler=(0,0,R(30))
                camset((L(.2,.35,q),L(-.4,-.55,q),1.6),((AMMI_P[0]+hw[0])/2,(AMMI_P[1]+hw[1])/2,1.25),L(18,20,q),4,focus=headpos(am))
            else:            # takes the note, stands, looks at us and shrugs
                k=ease(t/.6); seatH(w,SEATW[0]-.1*k,SEATW[1]-.2*k,L(90,20,k),sh=.56,k=1-k) if k<1 else standH(w,SEATW[0]-.1,SEATW[1]-.2,L(20,-20,ease((t-.6)/.8)),t); blink(w,t)
                nt.location=tuple(Vector(hand_w(w,1))+Vector((0,0,.02))); nt.rotation_euler=(0,0,R(10))
                if t>1.4: SHRUG(w,ease((t-1.4)/.4)); face(w,mouth='smirk',eyes=1.05,brow=.07)
                else: face(w,mouth='flat')
                arms(am,-62,0,-58,-62,0,58); face(am,mouth='smirk')
                cam_close(w,1,2.0,24,ang=8)
    return dict(upd=upd)
for v in ('home','happy','milk','cta'): SHOTS['J_'+v]=(lambda v=v: SH_J(v))
# ============================================================ Sir Zain's profile photo (outside the showroom)
def SH_P(view):
    R_=main_road(); B.done('road'); setup_render('afternoon',res=PCT,samples=SAMPLES,shadow_dist=40)
    z=person((SHW['x']-2.0,-.1,0),-12,ZAIN_GURU,'smirk',name='zain')
    def upd(t):
        standH(z,SHW['x']-2.0,-.1,-14,t); face(z,mouth='smirk',eyes=1.0,brow=.04); HIPS(z); z['head'].rotation_euler=(R(-5),0,R(8))
        _camset((SHW['x']-1.2,-5.6,1.3),(SHW['x']-.9,1.0,1.6),22,8,focus=headpos(z))
    return dict(upd=upd)
SHOTS['P_photo']=lambda: SH_P('photo')
