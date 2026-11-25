# ============================================================ helpers for "Everyone Is a Desi Aunty"
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
def sit_rk(K,H,key,t,extra=0.0):
    lx,ly,lz=K['seats'][key]; p=rk_world(K,lx,ly,0); rz=math.degrees(K['root'].rotation_euler[2])+180+extra
    seatH(H,p.x,p.y,rz,sh=lz); blink(H,t)
def drive_rk(K,H,t):
    bpy.context.view_layer.update(); m=K['hb'].matrix_world
    arm_reach(H,1,tuple(m@Vector((.34,0,.0+.01*math.sin(t*3))))); arm_reach(H,-1,tuple(m@Vector((-.34,0,0))))
def cam_rk(K,lx,ly,lz,tx,ty,tz,lens=20,fs=3.5): _camset(tuple(rk_world(K,lx,ly,lz)),tuple(rk_world(K,tx,ty,tz)),lens,fs,focus=tuple(rk_world(K,tx,ty,tz)))
RKX=-2.0
def road_crowd(seed=0,n=14,y0=-6,y1=30):
    rnd=random.Random(seed); G=[]
    for i in range(n):
        s=-1 if i%3 else 1; x=s*rnd.uniform(4.6,5.8); y=rnd.uniform(y0,y1)
        if abs(x+5.3)<.9 and abs(y-22)<1.6: y+=3.0
        H=person((x,y,0),0,aunty(300+seed*31+i*7),'smile',name='rc%d'%i); H['xy']=(x,y,rnd.uniform(0,360)); H['ph']=rnd.uniform(0,6); G.append(H)
    # pair them up: each faces the nearest neighbour
    for H in G:
        best=min((o for o in G if o is not H),key=lambda o:(Vector(o['xy'][:2])-Vector(H['xy'][:2])).length)
        if (Vector(best['xy'][:2])-Vector(H['xy'][:2])).length<2.2: H['xy']=(H['xy'][0],H['xy'][1],face_dir(best['xy'][0]-H['xy'][0],best['xy'][1]-H['xy'][1]))
    reg(*G); return G
def road_crowd_upd(G,t,stare=None):
    for i,H in enumerate(G):
        x,y,rz=H['xy']; standH(H,x,y,rz,t); blink(H,t+i)
        if stare is not None: look_at(H,stare,.8); gossip(H,t,H['ph'],talking=(i%2==0))
        else: gossip(H,t,H['ph'],talking=(int(t*.6+i)%2==0))
def traffic_cars(seed=0):
    out=[]
    for i,(x,col,sp,y0) in enumerate(((2.0,'#F4F5FA',-7,60),(2.0,'#C8102E',-6,30),(-2.0,'#2B2C33',6,-30),(2.0,'#2F6FE0',-8,5))):
        out.append((car(x,y0,col,rz=90 if sp>0 else -90),x,sp,y0))
    return out
def traffic_upd(V,t):
    for o,x,sp,y0 in V: o.location=(x,((y0+sp*t)+40)%130-40,0)
# ============================================================ A. THE ROAD + RICKSHAW
def SH_A(view):
    KEY='A_'+view; road(); B.done('road'); setup_render('morning_s',res=PCT,samples=SAMPLES,shadow_dist=40)
    w=WAL(); dr=person((0,0,0),0,RICK,'smile',name='rick'); reg(w,dr); K=rickshaw(RKX,0,0)
    G=road_crowd(1 if view in ('hook','job') else 2)
    HK=[]
    if view in ('hook','job'):
        rnd=random.Random(9)
        for i in range(11):
            a=-1.35+i*.27; rr=rnd.uniform(1.3,1.9); x=-4.75-abs(math.cos(a))*rr*.6; y=8.0+math.sin(a)*rr*1.4
            H=person((x,y,0),0,aunty(1300+i*11),'smile',name='hk%d'%i); H['xy']=(x,y,0); H['ph']=rnd.uniform(0,6); HK.append(H)
        reg(*HK)
    of=person((0,0,0),0,OFFICER,'flat',name='officer'); reg(of); V=traffic_cars()
    ph,scr=phone_obj('gps1'); tk=paper_obj('ticket',.14,.2); gl=glass_obj(); wh=whistle_obj()
    def upd(t):
        q=ease(t/DUR); traffic_upd(V,t)
        for o in (ph,tk,gl,wh): o.location=(0,0,-9)
        of['root'].location=(0,0,-9); KEEP[0]=None; NEAR[0]=1.5; OWNER[0]=None
        if view in ('hook','job'):
            K['root'].location=(RKX,-30,0); dr['root'].location=(0,0,-9)
            road_crowd_upd(G,t,stare=headpos(w) if view=='hook' else None)
            for i,H in enumerate(HK):
                x,y,_=H['xy']; standH(H,x,y,heading_to(H,headpos(w)),t); blink(H,t+i); gossip(H,t,H['ph'],talking=(i%3!=0)); look_at(H,headpos(w),.8)
            if view=='hook':      # every adult on this road is an aunty — and they are all looking at Waleed
                standH(w,-4.5,8.0,90,t); blink(w,t); face(w,mouth='flat',eyes=1.1); arms(w,-12,0,6,-12,0,-6)
                for i,H in enumerate(G): look_at(H,headpos(w),.8)
                _camset((L(-.9,-1.4,q),L(8.4,8.1,q),L(1.9,2.2,q)),(-4.9,8.0,1.3),L(19,17,q),6,focus=headpos(w))
            else:                  # one job: reach the interview by ten — checks the watch, then waves for a rickshaw
                standH(w,-4.6,8.0,L(200,90,ease((t-wl(18,KEY))/.6)),t); blink(w,t)
                if t<wl(18,KEY): arm_reach(w,-1,hand_front(w,-1,.35,-.45,.05)); arm_reach(w,1,hand_front(w,-1,.3,-.42,.02)); w['head'].rotation_euler=(R(25),0,0); face(w,mouth='O' if t>wl(13,KEY) else 'flat',eyes=1.2)
                else: arms(w,-30,0,8,-165+15*math.sin(t*10),0,-10); face(w,mouth='O',eyes=1.25,brow=.06)
                _camset((-2.5,L(9.6,10.2,q),1.7),(-4.5,8.0,1.45),L(26,22,q),4,focus=headpos(w))
        else:
            # rickshaw position for each view (moving at ~4 m/s where it drives)
            pos={'stop':(L(-16,1.5,ease_out(min(1,t/1.6))),0),'mirror':(4+3.5*t,0),'drv1':(16+3.5*t,0),'wal':(30+3.5*t,0),'drv2':(-12+3.5*t,0),'gps':(-28+3.5*t,0),
                 'cop':(L(10,22.6,ease_out(min(1,t/(wl(75,KEY)+.4)))),0),'scold':(22.6,0),'ticket':(22.6,0),'lassi':(22.6,0)}[view]
            y=pos[0]; K['root'].location=(RKX,y,0); K['root'].rotation_euler=(0,0,0)
            road_crowd_upd(G,t)
            sit_rk(K,dr,'drv',t); drive_rk(K,dr,t)
            if view=='stop':
                standH(w,-4.6,1.0,L(90,120,q),t); blink(w,t); arms(w,-30,0,8,-150+20*math.sin(t*8),0,-10) if t<1.4 else arms(w,-20,0,8,-20,0,-8); face(w,mouth='grin' if t>1.4 else 'O')
                look_at(dr,headpos(w),.7*ease((t-1.2)/.5)); face(dr,mouth='smile')
                _camset((L(.35,.3,q),L(-2.4,-2.0,q),1.65),(-4.3,1.0,1.25),L(20,22,q),5,focus=headpos(w))
            else:
                sit_rk(K,w,'back',t); arms(w,-55,0,-8,-55,0,8)
            if view=='mirror':    # the driver adjusts the mirror... to look at Waleed, not the road
                k=ease((t-.3)/.8); m=K['mir']; m.rotation_euler=(0,0,R(-28*k)); bpy.context.view_layer.update()
                if t<1.4: arm_reach(dr,1,tuple(m.matrix_world@Vector((.1,0,0))))
                dr['head'].rotation_euler=(R(-14*k),0,R(-8*k)); face(dr,mouth='smirk',eyes=1.1,brow=.08); look_at(w,headpos(dr),.5); face(w,mouth='flat')
                cam_rk(K,.3,2.6,1.95,0,.6,1.9,L(24,28,q),4)
            elif view in ('drv1','drv2'):   # she turns right round in her seat to interrogate him
                a,b=(37,44) if view=='drv1' else (49,55)
                dr['root'].rotation_euler[2]+=R(-38); dr['head'].rotation_euler=(0,0,R(-30)); arm_reach(dr,1,tuple(K['hb'].matrix_world@Vector((.34,0,0))))
                talk(dr,t,a,b,KEY,rest='smile',shapes=('o','grin','O','smirk')); face(dr,eyes=1.1,brow=.07); arms(dr,-30,0,8,-50-20*math.sin(t*5),0,-20) if view=='drv2' else None
                look_at(w,headpos(dr),.6); face(w,mouth='flat',eyes=.95)
                cam_rk(K,2.7,L(.2,-.1,q),1.6,0,-.15,1.4,L(25,27,q),5) if view=='drv1' else cam_rk(K,L(1.0,1.2,q),2.5,1.75,-.1,-.25,1.45,L(22,24,q),5)
            elif view=='wal':      # "Bhai, bas jaldi chalein."
                talk(w,t,45,48,KEY,rest='flat',shapes=('o','flat','O','flat')); face(w,eyes=1.0,brow=-.05)
                arms(w,-15,0,-8,-35,0,20); OWNER[0]=dr; body_vis(dr,False); hw=headpos(w); _camset(tuple(rk_world(K,.05,.95,2.0)),(hw[0],hw[1],hw[2]-.2),L(17,19,q),3,focus=hw)
            elif view=='gps':      # even the GPS has opinions — phone on the dash
                set_screen(scr,'gps2' if t>wl(64,KEY) else 'gps1',1.3)
                ph.location=tuple(rk_world(K,.22,1.0,1.35)); ph.rotation_euler=(R(-20),0,R(180)); ph.scale=(1,1,1)
                OWNER[0]=None; bpy.context.view_layer.update(); m=ph.matrix_world; c=m@Vector((.0,-.26,.02)); tg=m@Vector((0,0,0)); _camset(tuple(c),tuple(tg),L(26,30,q),16,focus=tuple(tg))
                face(dr,mouth='smile')
            elif view=='cop':      # traffic police aunty steps out, whistle — stops them. Not for the licence.
                k=ease((t-.2)/1.2); standH(of,L(-3.2,-3.0,k),L(25.2,24.2,k),L(200,180,k),t); blink(of,t)
                p=hand_front(of,1,.18,-.18,.0); wh.location=p; arm_reach(of,1,p) if t<wl(75,KEY) else arms(of,-30,0,8,-100,0,20)
                face(of,mouth='O' if t<wl(75,KEY) else 'flat',eyes=1.15,brow=-.07); look_at(of,headpos(w),.7); look_at(w,headpos(of),.6*k); face(w,mouth='O')
                _camset((L(-.2,-.4,q),L(30.5,30.0,q),L(1.7,1.6,q)),(L(-2.4,-2.6,q),23.2,1.3),L(22,26,q),5,focus=headpos(of))
            elif view in ('scold','ticket'):
                standH(of,-3.1,23.0,heading_to(of,headpos(w)),t); blink(of,t)
                if view=='scold':  # "Inni dhup vich bina topi de? Ammi nu pata ae?"
                    talk(of,t,81,90,KEY,rest='frown',shapes=('o','frown','O','frown')); face(of,eyes=1.05,brow=-.09); arms(of,-8,0,-38,-120+30*math.sin(t*6),0,10)
                    look_at(w,headpos(of),.7); face(w,mouth='flat',eyes=.9,brow=.05)
                    KEEP[0]=[]; front_cam(of,1.9,L(24,26,q),ang=-35,dz=.15)
                else:              # she writes the ticket: one glass of lassi
                    p=hand_front(of,-1,.36,-.45,-.05); tk.location=p; tk.rotation_euler=(R(-60),0,of['root'].rotation_euler[2]); arm_reach(of,-1,p); arm_reach(of,1,tuple(Vector(p)+Vector((.06,0,.04+.02*math.sin(t*14)))))
                    of['head'].rotation_euler=(R(25),0,0); face(of,mouth='flat',eyes=.8,brow=-.05); look_at(w,p,.7); face(w,mouth='O')
                    KEEP[0]=[of,w]; two_cam(of,w,side=-1,dist=2.4,lens=L(22,25,q),dz=.2)
            elif view=='lassi':    # Waleed at the stall, gulping a whole glass while she watches
                w['root'].location=(9,9,-9); standH(w,-4.1,19.7,heading_to(w,(-3.0,21.0,1.5)),t); blink(w,t)
                p=Vector(headpos(w))+root_mat(w).to_3x3()@Vector((0,-.2,-.12)); gl.location=tuple(p); gl.rotation_euler=(R(-40-20*q),0,w['root'].rotation_euler[2]); arm_reach(w,1,tuple(p+Vector((0,0,-.05))))
                w['head'].rotation_euler=(R(-20),0,0); face(w,mouth='O',eyes=.6)
                standH(of,-3.0,21.0,heading_to(of,headpos(w)),t); blink(of,t); arms(of,-62,0,-58,-62,0,58); face(of,mouth='smirk',eyes=1.0,brow=-.04)
                look_at(dr,headpos(w),.6); face(dr,mouth='grin')
                KEEP[0]=[w,of]; two_cam(w,of,side=-1,dist=3.0,lens=L(21,23,q),dz=.2)
        if view not in ('gps',): hide_block()
    return dict(upd=upd)
for v in ('hook','job','stop','mirror','drv1','wal','drv2','gps','cop','scold','ticket','lassi'): SHOTS['A_'+v]=(lambda v=v: SH_A(v))
# ============================================================ B. THE OFFICE
def SH_B(view):
    KEY='B_'+view; w=WAL(); reg(w)
    if view in ('gate','guard'):
        office_ext(); B.done('ox'); setup_render('day',res=PCT,samples=SAMPLES,shadow_dist=40)
        gd=person((OX+2.3,2.0,0),0,GUARDA,'flat',name='guard'); reg(gd)
        P=[person((0,0,0),0,aunty(800+i*9),'smile',name='px%d'%i) for i in range(4)]; reg(*P)
        spots=[(OX-6,-1.6,90),(OX-5.2,-1.4,270),(OX+6.5,-1.2,80),(OX+7.3,-1.5,260)]
        def upd(t):
            q=ease(t/DUR)
            for i,H in enumerate(P): standH(H,*spots[i],t); blink(H,t+i); gossip(H,t,i,talking=(i%2==0)); look_at(H,headpos(w),.5)
            standH(gd,OX+.9,1.9,heading_to(gd,headpos(w)) if t>.5 else 0,t); blink(gd,t)
            if view=='gate':      # twenty minutes late — the guard aunty stops him and looks him up and down
                tg=wl(115,KEY)
                if t<tg: walk_path(w,[(OX-.3,-5),(OX-.2,-1.5),(OX-.1,.6)],t,0,tg,step=.62,arm=30,run_=True)
                else: standH(w,OX-.1,.6,180,t); blink(w,t); arms(w,-25,0,-10,-25,0,10); face(w,mouth='O',eyes=1.1)
                sw=0 if t<tg+.3 else math.sin((t-tg-.3)*2.4); gd['head'].rotation_euler=(R(-25*sw),0,0); face(gd,mouth='flat',eyes=1.0,brow=-.06); arms(gd,-8,0,-38,-8,0,38)
                _camset((L(OX-3.6,OX-3.2,q),L(-5.0,-4.2,q),1.6),(OX,L(-.5,1.0,q),1.4),L(18,22,q),6,focus=headpos(w))
            else:                 # "Bohat kamzor ho gaye ho. Khana nahi khaande?"
                standH(w,OX-.1,.6,heading_to(w,headpos(gd)),t); blink(w,t); face(w,mouth='flat',eyes=.95); arms(w,-20,0,-8,-20,0,8)
                talk(gd,t,122,129,KEY,rest='frown',shapes=('o','frown','O','frown')); face(gd,eyes=1.1,brow=.08)
                hp=Vector(headpos(w)); arm_reach(gd,1,tuple(hp+Vector((0,0,-.55))+(Vector(headpos(gd))-hp).normalized()*.3)) if t>.8 else arms(gd,-8,0,-38,-8,0,38)
                KEEP[0]=[]; front_cam(gd,1.9,L(24,26,q),ang=-30,dz=.15)
            hide_block()
        return dict(upd=upd)
    if view in ('wait','anda'):
        D=waiting_room(); B.done('wr'); setup_interior('day',(OX,WY,3.2),res=PCT,samples=SAMPLES,shadow_dist=12)
        C=[person((0,0,0),0,c,'smile',name='cand%d'%i) for i,c in enumerate((CAND1,CAND2,CAND3))]; reg(*C)
        rc=person((OX+2.6,WY-1.6,0),0,aunty(77),'smile',name='recep'); reg(rc)
        tf=tiffin_obj(); lid=empty((0,0,0)); ocyl((0,0,0),.092,.02,M('#C9CDD6',.25,metal=.85),lid,rot=(0,0,0),seg=16); eg=egg_obj(); pl=plate_obj()
        def upd(t):
            q=ease(t/DUR); S=D['seats']
            for i,H in enumerate(C): seatH(H,S[i][0],S[i][1],S[i][2],sh=S[i][3]); blink(H,t+i)
            seatH(w,S[3][0],S[3][1],S[3][2],sh=S[3][3]); blink(w,t)
            standH(rc,OX+2.6,WY-1.55,180,t); blink(rc,t); look_at(rc,headpos(w),.5); face(rc,mouth='smile')
            lap=Vector(headpos(w))+root_mat(w).to_3x3()@Vector((0,-.42,-.95)); a,b_,c_=C
            if view=='wait':      # they open his bag... and check his lunch
                k=ease((t-wl(137,KEY))/.8); tf.location=tuple(lap); lid.location=tuple(Vector(lap)+Vector((0,0,.22+.0*k))+Vector((-.25*k,0,.25*k)))
                arm_reach(w,1,tuple(lap+Vector((.1,0,.05)))); arm_reach(w,-1,tuple(lap+Vector((-.1,0,.05)))); face(w,mouth='O' if k>.2 else 'flat',eyes=1.2)
                for i,H in enumerate((a,b_,c_)): H['root'].rotation_euler[2]+=R(-45 if i<2 else -30); look_at(H,tuple(lap),.9); face(H,mouth='O' if k>.4 else 'smile',eyes=1.2)
                arm_reach(c_,1,tuple(Vector(lid.location)+Vector((.05,0,.02)))) if k>0 else None
                _camset((L(OX-.4,OX-.2,q),L(WY-.9,WY-.6,q),1.45),(OX-.9,WY+1.9,.9),L(20,24,q),4,focus=tuple(lap))
            else:                 # "Sirf ek anda? Beta, interview vaaste taaqat chahidi ae!" — and a paratha appears
                tf.location=tuple(lap); lid.location=(0,0,-9)
                p=Vector(headpos(c_))+root_mat(c_).to_3x3()@Vector((-.25,-.35,.05)); eg.location=tuple(p); arm_reach(c_,1,tuple(p+Vector((0,0,-.04))))
                talk(c_,t,144,152,KEY,rest='O',shapes=('O','o','frown','O')); face(c_,eyes=1.35,brow=.12)
                k=ease((t-wl(147,KEY))/.6); pp=Vector(headpos(b_))+root_mat(b_).to_3x3()@Vector((-.2,-.5,-.35)); pl.location=tuple(pp.lerp(lap+Vector((0,0,.25)),k)); arm_reach(b_,1,tuple(Vector(pl.location)+Vector((0,0,-.02))))
                face(b_,mouth='grin',eyes=1.1); face(a,mouth='O',eyes=1.3); look_at(a,tuple(p),.8); look_at(w,tuple(p),.6); face(w,mouth='flat',eyes=.9,brow=.06)
                _camset((OX-.9,WY-.5,1.75),(OX-.6,WY+1.9,1.05),L(22,24,q),4,focus=headpos(c_))
            hide_block()
        return dict(upd=upd)
    # manager's office
    D=manager_office(); B.done('mo'); setup_interior('day',(MX,WY,3.2),res=PCT,samples=SAMPLES,shadow_dist=12)
    mg=person((0,0,0),0,MANAGER,'flat',name='manager'); reg(mg)
    cv=paper_obj('cv',.21,.3); pl=plate_obj()
    def upd(t):
        q=ease(t/DUR); bx,by,brz,bsh=D['boss']; gx,gy,grz,gsh=D['guest']
        seatH(mg,bx,by,brz,sh=bsh); blink(mg,t); seatH(w,gx,gy,grz,sh=gsh); blink(w,t)
        look_at(w,headpos(mg),.6); look_at(mg,headpos(w),.6); cv.rotation_euler=(R(90),0,0); pl.location=(0,0,-9)
        cvp=(MX+.1,WY+.7,D['desk_z']+.005)
        if view=='cv':        # the manager pushes his CV aside: "CV chhoro. Kis de puttar ho?"
            k=ease((t-.3)/.7); cv.location=(cvp[0]-1.0*k,cvp[1]+.1*k,cvp[2]); cv.rotation_euler=(R(90),0,R(40*k))
            if t<1.1: arm_reach(mg,1,(cv.location[0]+.1,cv.location[1]+.1,cv.location[2]+.06))
            talk(mg,t,162,167,KEY,rest='flat',shapes=('o','flat','O','smirk')); face(mg,eyes=.95,brow=-.04); arms(w,-55,0,-8,-55,0,8)
            if t>1.2: arms(mg,-60,0,-20,-60,0,20)
            _camset((L(MX-1.6,MX-1.3,q),L(WY-1.4,WY-1.1,q),1.55),(MX-.1,WY+1.1,1.0),L(20,22,q),4,focus=headpos(mg))
        elif view=='shazia':  # "Sir... Shazia ka beta hoon."
            cv.location=(cvp[0]-1.0,cvp[1]+.1,cvp[2]); cv.rotation_euler=(R(90),0,R(40))
            talk(w,t,168,172,KEY,rest='flat',shapes=('o','flat','o','flat')); face(w,eyes=.95,brow=.08); arms(w,-55,0,-8,-70,0,25)
            KEEP[0]=[]; front_cam(w,1.5,L(26,30,q),ang=25,dz=.2)
        elif view=='pakki':   # "Shazia? Oh te meri cousin di nand ae! Naukri pakki."
            cv.location=(cvp[0]-1.0,cvp[1]+.1,cvp[2]); cv.rotation_euler=(R(90),0,R(40))
            k=ease((t-wl(174,KEY))/.5); mg['root'].location[2]+=.0;
            if k>0: standH(mg,bx,by-.35,brz,t); blink(mg,t); celebrate(mg,t,.6*k)
            talk(mg,t,173,182,KEY,rest='grin',shapes=('O','grin','o','grin')); face(mg,eyes=1.3,brow=.12)
            face(w,mouth='O' if t<wl(181,KEY) else 'grin',eyes=1.2)
            _camset((L(MX+1.7,MX+1.5,q),L(WY-1.3,WY-1.0,q),1.6),(MX,WY+.9,1.2),L(19,21,q),4,focus=headpos(mg))
        else:                 # "Aur salary, sir?" — "Salary baad vich. Pehlan roti kha." (pushes a plate of roti over)
            cv.location=(cvp[0]-1.0,cvp[1]+.1,cvp[2]); cv.rotation_euler=(R(90),0,R(40))
            if t<wl(186,KEY): talk(w,t,183,185,KEY,rest='flat',shapes=('o','flat','O','flat')); face(w,eyes=1.0,brow=.06); face(mg,mouth='smile')
            else:
                talk(mg,t,186,191,KEY,rest='smile',shapes=('o','smile','O','smile')); face(mg,eyes=1.0,brow=.04); face(w,mouth='flat',eyes=.85)
                k=ease((t-wl(188,KEY))/.8); pl.location=(MX+L(.0,.45,k),WY+L(1.1,.35,k),D['desk_z']+.02); arm_reach(mg,1,(pl.location[0],pl.location[1]+.08,pl.location[2]+.05)) if k<1 else None
            two_cam(w,mg,side=1,dist=2.4,lens=L(20,22,q),dz=.35)
        hide_block()
    return dict(upd=upd)
for v in ('gate','guard','wait','anda','cv','shazia','pakki','roti'): SHOTS['B_'+v]=(lambda v=v: SH_B(v))
# ============================================================ C. THE WALK HOME — every window opens
def SH_C(view):
    KEY='C_'+view; WIN=home_street(); B.done('st'); setup_render('golden',res=PCT,samples=SAMPLES,shadow_dist=40)
    w=WAL(); reg(w); SH=[]; AU=[]
    for i,wn in enumerate(WIN[:16]):
        SH.append(shutters(wn)); H=person((0,0,-9),0,aunty(500+i*13),'smile',name='nw%d'%i); AU.append(H)
    reg(*AU)
    kids=[person((SX+.3,30,0),0,local(61+i,True),'grin',name='kd%d'%i) for i in range(2)]; reg(*kids)
    def upd(t):
        q=ease(t/DUR)
        for i,k_ in enumerate(kids): standH(k_,SX+[-.8,.9][i],34+i*.7,[150,210][i],t); blink(k_,t); arms(k_,-40,0,10,-110+30*math.sin(t*6+i),0,-10); face(k_,mouth='grin')
        if view=='walk':      # walking home smiling. He hasn't told anyone yet.
            wy=L(-6,2,t/DUR); walk_path(w,[(SX-.2,-6),(SX-.2,2.5)],t,0,DUR,step=.55,arm=24); face(w,mouth='grin',eyes=1.0); blink(w,t)
            opened=[]
        else:
            if view=='win': wy=L(2,12,t/DUR); walk_path(w,[(SX-.2,2),(SX-.2,12)],t,0,DUR,step=.55,arm=24)
            else: wy=12.4; standH(w,SX-.2,12.4,heading_to(w,headpos(AU[6])),t)
            blink(w,t); face(w,mouth='O' if view=='win' else 'grin',eyes=1.25)
        for i,wn in enumerate(WIN[:16]):
            if view=='walk': k=0
            elif view=='win': k=ease((t-(wn['y']-2)/10*DUR*.85)/.35) if wn['y']>1 else ease((t-.1*i)/.35)
            else: k=1
            shutters_set(SH[i],wn['s'],k); H=AU[i]
            if k>0:
                zf=0.0 if wn['fl']==0 else 3.0; xx=wn['x']+wn['s']*.33; H['root'].rotation_euler=(0,0,R(-90 if wn['s']>0 else 90))
                stand(H,t); H['root'].location=(xx,wn['y'],zf-.35*(1-k)); blink(H,t+i); look_at(H,headpos(w),.8)
                face(H,mouth=('grin','O','smile','grin')[i%4],eyes=1.15); arms(H,-60,0,-10,-120+20*math.sin(t*5+i),0,10) if i%3==0 else arms(H,-40,0,-10,-40,0,10)
            else: H['root'].location=(0,0,-9)
        if view=='walk': front_cam(w,L(3.2,2.6,q),L(24,24,q),ang=10,dz=-.1)
        elif view=='win': _camset((SX+.4,wy+4.5,2.2),(SX-.2,wy,1.6),L(16,17,q),6,focus=headpos(w))
        else:                 # one aunty, right at the window: "Mubarak ho! Tankhwah thori ae, par chalo."
            H=AU[6]; talk(H,t,211,217,KEY,rest='smirk',shapes=('o','grin','O','smirk')); face(H,eyes=1.05,brow=.06); arms(H,-40,0,-10,-90-20*math.sin(t*5),0,20)
            KEEP[0]=[H]; _camset((SX+1.6,L(13.0,13.3,q),1.8),(WIN[6]['x'],WIN[6]['y'],1.6),L(22,24,q),4,focus=headpos(H))
        hide_block()
    return dict(upd=upd)
for v in ('walk','win','mub'): SHOTS['C_'+v]=(lambda v=v: SH_C(v))
# ============================================================ D. HOME: phone, TV, the call
def SH_D(view):
    KEY='D_'+view; D=living(); B.done('lv'); setup_interior('evening',(LX,0,3.0),res=PCT,samples=SAMPLES,shadow_dist=10)
    w=WAL(); reg(w); OWNER[0]=None
    ph,scr=phone_obj('fam'); rm=empty((0,0,0)); obox((0,0,0),(.025,.08,.012),M('#16171C',.4),.006,rm)
    def upd(t):
        q=ease(t/DUR); D['fan'].rotation_euler[2]=t*6; set_screen(D['tv'],'tv_off',.2); rm.location=(LX-1.05,-.15,.37); ph.location=(0,0,-9); OWNER[0]=None
        sx,sy,srz,ssh=D['sofa'][1]
        if view=='tv': sx,sy,srz,ssh=D['sofa'][0]
        if view=='phone':     # four hundred messages in the family group
            set_screen(scr,'fam',1.3); standH(w,LX-.2,-.9,60,t); blink(w,t)
            phone_in_hand(w,ph,up=1.6,face_dist=.5,raise_=.02*math.sin(t*40) if t<.8 else 0); face(w,mouth='O',eyes=1.3)
            if t<1.3: front_cam(w,1.6,24,ang=-25,dz=.1)
            else: OWNER[0]=w; insert_cam(ph,L(24,28,q),.24)
        elif view=='tv':      # he turns on the TV
            seatH(w,sx,sy,srz,sh=ssh); blink(w,t); on=t>wl(231,KEY)
            p=hand_front(w,1,.45,-.35,.1); rm.location=p; rm.rotation_euler=(0,0,w['root'].rotation_euler[2]); arm_reach(w,1,p); set_screen(D['tv'],'tv_news' if on else 'tv_off',1.1 if on else .2)
            face(w,mouth='flat' if not on else 'O',eyes=1.0 if not on else 1.3); look_at(w,(LX+2.8,.1,1.45),.6)
            _camset((L(LX-2.7,LX-2.6,q),L(.3,.2,q),1.92),(LX+2.8,-.1,1.15),L(17,19,q),5,focus=(LX+2.8,.1,1.4))
        elif view=='sit':     # Waleed sits down. His phone rings.
            set_screen(D['tv'],'tv_news',1.0); k=ease(t/.9)
            if t<.9: standH(w,L(LX-1.6,sx+.3,k),sy,270,t); w['root'].location[2]-=0
            else: seatH(w,sx,sy,srz,sh=ssh)
            blink(w,t); rg=t>wl(253,KEY)
            set_screen(scr,'pm',1.2); ph.location=(LX-.85+(.004*math.sin(t*90) if rg else 0),.35,.35); ph.rotation_euler=(R(90),0,R(90))
            if t>wl(253,KEY)+.5: p=phone_ear(w,ph,1)
            face(w,mouth='O' if rg else 'smile',eyes=1.2 if rg else .9); look_at(w,tuple(ph.location),.6*rg)
            _camset((L(LX-.2,LX-.4,q),L(1.9,1.7,q),1.5),(sx,sy,.9),L(20,22,q),4,focus=headpos(w))
        elif view=='pm':      # caller ID: PRIME MINISTER
            seatH(w,sx,sy,srz,sh=ssh); set_screen(scr,'pm',1.3); phone_in_hand(w,ph,up=1.6,face_dist=.5,two=False); OWNER[0]=w; insert_cam(ph,L(24,28,q),.24)
        else:                 # 'cta': on the phone with the PM — jaw on the floor, then the facepalm
            seatH(w,sx,sy,srz,sh=ssh); blink(w,t); set_screen(D['tv'],'tv_news',1.0); set_screen(scr,'pm',1.0)
            if t<1.6: phone_ear(w,ph,1); face(w,mouth='O',eyes=1.4,brow=.12)
            else: ph.location=tuple(Vector(hand_front(w,1,.3,-.75,.2))); arm_reach(w,-1,tuple(Vector(headpos(w))+root_mat(w).to_3x3()@Vector((-.04,-.2,-.02)))); w['head'].rotation_euler=(R(14),0,0); face(w,mouth='frown',eyes=.5)
            front_cam(w,L(2.1,1.8,q),L(24,26,q),ang=20,dz=.2)
    return dict(upd=upd)
for v in ('phone','tv','sit','pm','cta'): SHOTS['D_'+v]=(lambda v=v: SH_D(v))
# ============================================================ E. NEWS STUDIO + F. PM OFFICE
def SH_E(view):
    KEY='E_'+view; D=studio(); B.done('ns'); setup_interior('night',(NX,0,4),res=PCT,samples=SAMPLES,shadow_dist=10); bpy.context.scene.view_settings.exposure=.25
    an=person((0,0,0),0,ANCHOR,'smile',name='anchor'); reg(an)
    def upd(t):
        q=ease(t/DUR); x,y,rz,sh=D['seat']; seatH(an,x,y,rz,sh=sh); blink(an,t); arms(an,-55,0,-10,-55+10*math.sin(t*3),0,10)
        talk(an,t,233,248,KEY,rest='smile',shapes=('o','smile','O','flat')); face(an,eyes=1.05,brow=.05)
        if t>wl(241,KEY): an['head'].rotation_euler=(R(5),0,R(-12)); face(an,brow=.12)
        _camset((NX+L(.6,.1,q),L(-3.8,-3.0,q),1.45),(NX,.7,1.15),L(20,24,q),4,focus=headpos(an))
    return dict(upd=upd)
SHOTS['E_news']=lambda: SH_E('news')
def SH_F(view):
    KEY='F_'+view; D=pm_office(); B.done('pm'); setup_interior('day',(PX,0,3.8),res=PCT,samples=SAMPLES,shadow_dist=12)
    pm=person((0,0,0),0,PMA,'smile',name='pm'); reg(pm); ph,scr=phone_obj('pm')
    def upd(t):
        q=ease(t/DUR); x,y,rz,sh=D['seat']; seatH(pm,x,y,rz,sh=sh); blink(pm,t); phone_ear(pm,ph,1); arms(pm,-60,0,-20,None or -60,0,20) if False else None
        arm_reach(pm,-1,(x-.25,y-.75,.9)); talk(pm,t,260,264,KEY,rest='smile',shapes=('o','smile','O','smile')); face(pm,eyes=.95,brow=.06)
        pm['head'].rotation_euler=(0,R(6),0)
        _camset((L(PX+.7,PX+.3,q),L(-2.2,-1.5,q),1.6),(PX,1.8,1.25),L(22,28,q),4,focus=headpos(pm))
    return dict(upd=upd)
SHOTS['F_pm']=lambda: SH_F('pm')
