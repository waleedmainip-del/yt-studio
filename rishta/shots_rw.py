SHOTS={}
WJ=json.load(open('/home/claude/rishta/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('A_world',0),('A_fear',13),('A_not',31),('A_title',40),
    ('B_sleep',46),('B_ammi',50),('B_kya',52),('B_aa',55),('B_again',61),('B_umar',62),('B_expiry',68),
    ('D_abbu',76),('D_abbu2',80),
    ('G_bell',97),('G_walk',101),('G_salam',112),('G_yeh',116),
    ('Q_height',120),('Q_salary',123),('Q_abhi',124),('Q_matlab',130),('Q_future',132),('Q_gaari',135),('Q_ghar',139),('Q_biz',142),('Q_close',145),('Q_apna',150),('Q_dua',155),
    ('R_ruko',158),('R_photo',165),('R_kaun',170),('R_doc',173),('R_pata',181),('R_bilkul',188),('R_ammi',195),('R_conf',196),
    ('C_call',202),('C_bhai',208),('C_congrats',214),('C_ready',215),('C_simple',219),('C_pagal',225),('C_dubai',227),('C_karachi',235),('C_bro',240),
    ('V_came',250),('V_salam',264),('V_wa',265),('V_what',268),('V_froze',273),('V_same',280),('V_really',285),('V_yes',286),('V_ammi',303),
    ('T_ring',310),('T_beta',320),('T_abkya',326),('T_larki',328),('T_serious',338),('T_haan',339),('T_kya',344),('T_unko',345),('T_silent',352),('T_remote',355),('T_main',361),
    ('E_out',368),('E_aunty',379),('E_noesc',387)]
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

# ============================================================ sets
def set_room():
    R_=drawing_room(); setup_interior('day',room=(0,0,3.2),res=PCT,samples=SAMPLES)
    bpy.context.scene.view_settings.exposure=-0.35
    area((-1.1,4.2,1.8),260,(1.4,1.4),(1,.95,.85),rot=(R(90),0,0),shadow=True)
    point((0,.5,3.0),45,(1,.93,.82),.4); point((-3.6,2.6,1.45),18,(1,.8,.55),.2,shadow=False); point((3.5,-.4,1.5),10,(.5,1,.6),.2,shadow=False)
    return R_
def set_bed():
    R_=bedroom(); setup_interior('morning',room=(0,0,3.0),res=PCT,samples=SAMPLES)
    bpy.context.scene.view_settings.exposure=-0.3
    area((4.2,.4,1.8),300,(1.2,1.2),(1,.9,.72),rot=(0,R(-90),0),shadow=True); point((0,0,2.9),30,(1,.93,.82),.4)
    return R_
def set_colony(mood='morning_s',cars=True):
    colony(5,cars=cars); setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=60)
def set_roof():
    rooftop(); setup_render('dusk',res=PCT,samples=SAMPLES,shadow_dist=30); point((0,-1.5,2.6),60,(1,.85,.6),.4)
def set_clinic():
    clinic(); setup_interior('day',room=(0,0,3.0),res=PCT,samples=SAMPLES); bpy.context.scene.view_settings.exposure=-0.4
    point((0,-.6,2.6),60,(1,.97,.94),.4)
    B.box((0,1.55,.25),(.3,.3,.25),M('#2B2C33',.5),.04); B.box((0,1.85,.75),(.3,.05,.4),M('#2B2C33',.5),.04); B.done('chair')

def tv_anim(R_,t):
    m=R_['tv'].active_material
    try: m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=1.1+.15*math.sin(t*3)
    except Exception: pass

# ============================================================ INTRO (colony)
def SH_A(view):
    KEY=view; set_colony('morning_s',cars=False)
    AU=person((0,0,0),90,AUNTY,'smirk',name='aunty'); nb=notebook(AU,-1); hb=handbag(AU,1)
    nb_specs=[(-8,3.7,0),(-3.5,3.75,10),(3.2,3.7,-10),(7.5,3.7,0),(11,-3.7,180),(-6,-3.75,180)]
    NB=[person((x,y,0),rz,local(700+i*7),'smile',name='nb%d'%i) for i,(x,y,rz) in enumerate(nb_specs)]
    def neighbours(t,ax):
        for i,(H,(x,y,rz)) in enumerate(zip(NB,nb_specs)):
            put_at(H,t,x,y,rz); d=abs(ax-x); k=cl((5.5-d)/1.2) if view!='A_world' else 0
            if k>0:
                H['root'].rotation_euler[2]=R(rz+180*min(1,k*1.5)); kneel(H,k); face(H,mouth='O',brow=.12,eyes=1.2)
            else: gaze_idle(H,t); face(H,mouth='smile')
    def aunty_walk(t,x0,v):
        x=x0+v*t; AU['root'].location=(x,0.0,.008); AU['root'].rotation_euler[2]=R(90); AU['z0']=0; walk(AU,x,step=.45,arm=14); blink(AU,t)
        AU['arm'][-1].rotation_euler=(R(-70),0,R(25)); face(AU,mouth='smirk',brow=-.02,brow_r=-10); return x
    def upd(t):
        if view=='A_world':
            x=aunty_walk(t,-14,.8); neighbours(t,x); q=ease(t/DUR)
            camset((L(-34,-24,q),L(-2.5,-1.5,q),L(20,9,q)),(L(-8,-10,q),.5,0),26,8.0)
        elif view=='A_fear':
            x=aunty_walk(t,-11,1.0); neighbours(t,x); AU['head'].rotation_euler[2]=R(25*math.sin(t*1.3))
            camset((x+4.0,-.3,2.6),(x+.3,1.0,1.3),24,6.0)
        elif view=='A_not':
            x=aunty_walk(t,-1.0,.55); neighbours(t,x); AU['arm'][1].rotation_euler=(R(-75),0,R(-30)); AU['head'].rotation_euler[0]=R(15)
            cf(AU,d=2.0,lat=-.45,dz=.05,lens=30)
        else:
            k=cl(t/.6); x=7.0+.4*k; AU['root'].location=(x,0.0,.008); stand(AU,t); AU['root'].rotation_euler[2]=R(L(90,0,ease(k))); blink(AU,t)
            neighbours(t,100); AU['arm'][-1].rotation_euler=(R(-70),0,R(25)); hips(AU,.0)
            AU['arm'][1].rotation_euler=(R(-15),R(-35),R(70)); face(AU,mouth='smirk' if t<1.2 else 'grin',brow=-.03,brow_r=-14)
            q=ease(t/DUR); camset((x+L(.3,.15,q),L(-3.0,-2.2,q),L(.9,1.2,q)),(x,0.0,L(1.7,1.85,q)),L(24,30,q),3.0)
    return dict(upd=upd)
for v in ('A_world','A_fear','A_not','A_title'): SHOTS[v]=(lambda v=v: SH_A(v))

# ============================================================ BEDROOM
def SH_B(view):
    KEY=view; Rb=set_bed(); HM=person((0,0,0),0,HAMZA,'smile',name='hamza'); AM=person((0,0,0),0,AMMI,'frown',name='ammi'); bl=Rb['blanket']; dr=Rb['door']
    def lying(t):
        HM['root'].location=(.2,-.05,.62); HM['root'].rotation_euler=(R(-90),0,0); HM['z0']=0; handsdown(HM)
        for q in (1,-1): HM['leg'][q].rotation_euler=(0,0,0)
        bl.location=(.2,.75,.86); bl.rotation_euler=(0,0,0); HM['root'].scale=(1,1,1+.01*math.sin(t*1.6))
    def door(k): dr.location=(L(2.5,3.0-.04,k),L(-2.28,-1.7-.55,k),1.1); dr.rotation_euler=(0,0,R(L(0,90,k)) if False else 0)
    def upd(t):
        if view=='B_sleep':
            lying(t); hideH(AM); face(HM,mouth='smile',eyes=.0) if False else None; blink(HM,t,force=1) if False else None
            face(HM,mouth='smile'); HM['lid'] if False else None
            try: blink(HM,t,force=1.0)
            except TypeError: pass
            q=ease(t/DUR); camset((L(2.6,1.8,q),L(-1.6,-.6,q),L(2.2,1.9,q)),(.2,1.6,.8),26,4.0)
        elif view=='B_ammi':
            lying(t); k=cl(t/.45); ax=L(3.4,1.9,ease(cl(t/1.1))); AM['root'].location=(ax,L(-1.7,-.6,ease(cl(t/1.1))),.008); AM['z0']=0
            AM['root'].rotation_euler[2]=R(-110); walk(AM,ax,step=.6,arm=20) if t<1.1 else stand(AM,t); blink(AM,t)
            talk(AM,t,50,51,KEY,rest='frown',shapes=('shout','O','shout')); AM['arm'][1].rotation_euler=(R(-140),0,R(-10)); AM['arm'][-1].rotation_euler=(R(-140),0,R(10))
            face(AM,brow=-.05,brow_r=20)
            try: blink(HM,t,force=1.0 if t<wl(51,KEY) else 0.0)
            except TypeError: pass
            if t>wl(51,KEY): HM['root'].location[2]=.62+.25*math.exp(-((t-wl(51,KEY)-.15)/.12)**2); face(HM,mouth='O',eyes=1.3,brow=.14)
            camset((-1.6,-2.2,1.9),(.9,.2,1.1),22,5.0)
        else:
            bl.location=(.2,1.5,.6); bl.scale=(1,.5,1)
            seat(HM,t,.2,-.1,0,sh=.6); put_at(AM,t,1.6,-1.2,-128); look_at(HM,headpos(AM),.6); look_at(AM,headpos(HM),.6)
            for q in (1,-1): HM['leg'][q].rotation_euler[0]=-R(30)
            HM['root'].location[2]=.6-1.5*HM['u']+.02
            if view=='B_kya': talk(HM,t,52,54,KEY,rest='O',shapes=('O','shout','O')); face(HM,brow=.13,eyes=1.25); HM['arm'][1].rotation_euler=(R(-60),0,R(-30)); cf(HM,d=1.7,lat=-.45,lens=30)
            elif view=='B_aa': talk(AM,t,55,60,KEY,rest='grin'); gesture(AM,t,1); face(AM,brow=.06); ots(HM,AM)
            elif view=='B_again': talk(HM,t,61,61,KEY,rest='O',shapes=('shout','O')); face(HM,brow=.16,eyes=1.4); arms(HM,-160,0,20,-160,0,-20); q=ease(t/.4); cf(HM,d=L(1.8,1.2,q),lat=-.2,lens=32)
            elif view=='B_umar': talk(AM,t,62,67,KEY,rest='frown'); face(AM,brow=.08,brow_r=-12); AM['arm'][1].rotation_euler=(R(-70),0,R(-20)); ots(HM,AM,back=1.0,side=-.4)
            else: talk(HM,t,68,75,KEY,rest='frown',shapes=('shout','O','flat')); face(HM,brow=-.04,brow_r=18); gesture(HM,t,1,1.3); gesture(HM,t+1,-1,1.0); cf(HM,d=1.8,lat=.45,lens=30)
            door(1)
        if view in ('B_sleep',): door(0)
        elif view=='B_ammi': door(cl(t/.35))
    return dict(upd=upd)
for v in ('B_sleep','B_ammi','B_kya','B_aa','B_again','B_umar','B_expiry'): SHOTS[v]=(lambda v=v: SH_B(v))

# ============================================================ DRAWING ROOM (all indoor house scenes)
POS=dict(abbu=(2.12,-.4,90), au_sofa=(-3.3,.2,90), am_sofa=(-3.3,1.2,90), hm_stand=(-.45,.85,-90), hm_seat=(.25,2.45,0), am_seat=(1.0,2.45,0))
def SH_D(view):
    KEY=view; Rr=set_room()
    AB=person((0,0,0),0,ABBU,'smile',name='abbu'); rm=remote(AB,1)
    AU=person((0,0,0),0,AUNTY,'smirk',name='aunty'); AM=person((0,0,0),0,AMMI,'smile',name='ammi'); HM=person((0,0,0),0,HAMZA,'smile',name='hamza')
    nb=notebook(AU,-1); hb=handbag(AU,1); ph=photo(AU,1); ph.scale=(0,0,0); hph=phone(HM,1,'#9FD8FF'); hph.scale=(0,0,0); aph=phone(AU,1,'#7FD3FF'); aph.scale=(0,0,0)
    bag_on_sofa=obox((-3.35,1.85,.6),(.16,.07,.13),M('#3A2A1E',.45),.03)
    ph_='QRVT'
    def abbu(t,watch=True):
        x,y,rz=POS['abbu']; seat(AB,t,x,y,rz); AB['arm'][1].rotation_euler=(R(-55),0,R(-10)); AB['arm'][-1].rotation_euler=(R(-20),0,R(20)); tv_anim(Rr,t)
        if watch: look_at(AB,(3.9,-.4,1.55),.8); face(AB,mouth='grin' if math.sin(t*.9)>.6 else 'smile')
    def sofa_ladies(t):
        x,y,rz=POS['au_sofa']; seat(AU,t,x,y,rz); x,y,rz=POS['am_sofa']; seat(AM,t,x,y,rz); hb.scale=(0,0,0)
        AU['arm'][-1].rotation_euler=(R(-65),0,R(20)); AU['arm'][1].rotation_euler=(R(-60),0,R(-25+6*math.sin(t*7)))
    g=view[0]
    def upd(t):
        if g=='D':
            abbu(t); hideH(AU); hideH(AM); hideH(HM); bag_on_sofa.scale=(0,0,0)
            if view=='D_abbu':
                q=ease(t/DUR); camset((L(-1.5,-.8,q),L(-3.2,-2.9,q),L(2.4,2.0,q)),(2.4,-.4,1.1),24,5.0)
            else:
                talk(AB,t,80,96,KEY,rest='smile',rate=6); look_at(AB,(3.9,-.4,1.55),.8); AB['head'].rotation_euler[2]=R(-35) if wl(80,KEY)<t<wl(83,KEY)+.3 else AB['head'].rotation_euler[2]
                gesture(AB,t,-1,.6); cf(AB,d=1.6,lat=-.5,lens=30)
            return
        abbu(t)
        if g=='G':
            bag_on_sofa.scale=(0,0,0); put_at(AM,t,-1.9,2.0,170); put_at(HM,t,-.45,.85,-60)
            if view=='G_walk':
                k=ease(cl(t/2.6)); AU['root'].location=(-2.6,L(3.9,1.95,k),.008); AU['z0']=0; AU['root'].rotation_euler[2]=R(0); walk(AU,L(3.9,1.95,k),step=.45,arm=12) if k<1 else stand(AU,t); blink(AU,t)
                AU['arm'][-1].rotation_euler=(R(-65),0,R(20)); face(AU,mouth='smirk',brow=-.02); look_at(AM,headpos(AU),.7); look_at(HM,headpos(AU),.6); face(HM,mouth='flat',brow=.06)
                Rr['door'].rotation_euler=(0,0,0); q=ease(t/DUR); camset((L(-1.2,-1.5,q),-1.2,1.75),(-2.6,L(3.2,2.2,q),1.6),26,4.0)
            else:
                put_at(AU,t,-2.6,1.95,-20); AU['arm'][-1].rotation_euler=(R(-65),0,R(20))
                if view=='G_salam':
                    talk(AU,t,112,115,KEY,rest='grin',rate=6); AU['arm'][1].rotation_euler=(R(-110),0,R(-20)) if t<wl(113,KEY) else (R(-20),0,0); look_at(AU,headpos(HM),.5)
                    cf(AU,d=2.1,lat=-.4,lens=30)
                else:
                    talk(AM,t,116,119,KEY,rest='grin'); AM['root'].rotation_euler[2]=R(130); AM['arm'][1].rotation_euler=(R(-75),0,R(-55)); look_at(AU,headpos(HM),.7); look_at(HM,headpos(AU),.5)
                    face(HM,mouth='smile',brow=.05); q=ease(t/DUR); camset((L(-1.1,-.9,q),-1.6,1.7),(-1.5,1.3,1.6),L(22,26,q),5.0)
            return
        # Q / R / V / T: ladies on sofa, bag on sofa
        sofa_ladies(t)
        if g in 'QR':
            x,y,rz=POS['hm_stand']
            if g=='R' and view!='R_ruko': x,y,rz=-1.05,-.3,-90
            put_at(HM,t,x,y,rz); look_at(HM,headpos(AU),.7); look_at(AU,headpos(HM),.7); look_at(AM,headpos(HM),.5)
        if g=='Q':
            nb.scale=(1,1,1)
            if view=='Q_height':
                talk(AU,t,120,120,KEY,rest='smirk'); talk(HM,t,121,122,KEY,rest='smile') if t>wl(121,KEY)-.05 else face(HM,mouth='smile'); HM['root'].scale=(1,1,1.0)
                camset((-1.7,-3.2,1.7),(-1.85,1.0,1.2),20,5.0)
            elif view=='Q_salary': talk(AU,t,123,123,KEY,rest='smirk'); face(AU,brow=-.03,brow_r=-16); cf(AU,d=1.5,lat=.35,lens=30)
            elif view=='Q_abhi': talk(HM,t,124,129,KEY,rest='flat'); face(HM,brow=.05,brow_r=-10); HM['arm'][1].rotation_euler=(R(-25),R(20),R(60)); cf(HM,d=1.7,lat=.4,lens=30)
            elif view=='Q_matlab':
                AU['arm'][1].rotation_euler=(R(-60),0,R(-25)); talk(AU,t,130,131,KEY,rest='flat'); face(AU,brow=-.05,brow_r=-20,eyes=.9); AU['head'].rotation_euler[0]=R(12)
                q=ease(t/DUR); cf(AU,d=L(1.6,1.1,q),lat=.25,lens=32)
            elif view=='Q_future': talk(HM,t,132,134,KEY,rest='grin'); face(HM,brow=.05); hips(HM); cf(HM,d=1.9,lat=-.3,lens=30)
            elif view in ('Q_gaari','Q_ghar'):
                a,b=(135,136) if view=='Q_gaari' else (139,139); c,d=(137,138) if view=='Q_gaari' else (140,141)
                if t<wl(c,KEY)-.05: talk(AU,t,a,b,KEY,rest='smirk')
                else: talk(HM,t,c,d,KEY,rest='smile'); face(AU,mouth='flat')
                if view=='Q_gaari': ots(HM,AU,back=1.0,side=-.4)
                else: cf(HM,d=1.8,lat=.4,lens=30)
            elif view=='Q_biz':
                if t<wl(143,KEY)-.05: talk(AU,t,142,142,KEY,rest='smirk')
                else: talk(HM,t,143,144,KEY,rest='smile')
                AB['head'].rotation_euler[2]=R(-70) if t>wl(143,KEY) else 0; face(AB,mouth='smirk' if t>wl(143,KEY) else 'smile',brow=.04)
                camset((-1.6,-2.9,1.8),(-1.2,.6,1.3),20,6.0)
            elif view=='Q_close':
                k=ease(cl((t-.3)/1.4)); AU['arm'][1].rotation_euler=(R(L(-60,-75,k)),0,R(L(-25,-5,k))); face(AU,mouth='flat',brow=-.04,eyes=.85)
                nb.scale=(1,1,1); nb.rotation_euler=(0,0,R(-40*k)); q=ease(t/DUR)
                cf(AU,d=1.35,lat=-.5,dz=-.25,tgt_dz=-.4,lens=32)
            elif view=='Q_apna': talk(AU,t,150,154,KEY,rest='flat',rate=5); face(AU,brow=.05,brow_r=8); AU['head'].rotation_euler[1]=R(8); cf(AU,d=1.4,lat=.3,lens=32)
            else:
                talk(HM,t,155,157,KEY,rest='grin'); face(HM,eyes=.8,brow=.06); HM['arm'][1].rotation_euler=(R(-40),0,R(-20)); HM['arm'][-1].rotation_euler=(R(-40),0,R(20))
                face(AM,mouth='grin',eyes=.8); q=ease(t/DUR); cf(HM,d=L(2.0,1.6,q),lat=-.3,lens=30)
            return
        if g=='R':
            nb.scale=(0,0,0) if view!='R_ruko' else (1,1,1)
            if view=='R_ruko':
                k=ease(cl((t-.2)/.5)); AU['root'].location[2]=L(AU['root'].location[2],0.008,k)
                for q in (1,-1): AU['leg'][q].rotation_euler[0]=-R(90)*(1-k)
                if k>=1: put_at(AU,t,-3.3+.9*ease(cl((t-.7)/.8)),.2-.5*ease(cl((t-.7)/.8)),90)
                talk(AU,t,158,164,KEY,rest='grin',rate=7); AU['arm'][1].rotation_euler=(R(-150),0,R(-15)); face(AU,brow=.1,eyes=1.15); look_at(AU,headpos(HM),.5)
                face(HM,mouth='o',brow=.08); camset((-.6,-2.3,1.7),(-2.6,.6,1.45),22,5.0)
                return
            put_at(AU,t,-2.4,-.3,90); ph.scale=(1,1,1); AU['arm'][1].rotation_euler=(R(-90),0,R(-10)); look_at(AU,headpos(HM),.6); look_at(HM,ph.matrix_world.translation if view=='R_photo' else headpos(AU),.7)
            if view=='R_photo':
                k=ease(cl(t/.6)); AU['arm'][1].rotation_euler=(R(-90*k),0,R(-10*k)); face(AU,mouth='grin',brow=.06)
                q=ease(t/DUR); camset((-1.7,L(-2.6,-2.1,q),1.65),(-1.7,-.3,1.55),28,3.0)
            elif view=='R_kaun': talk(HM,t,170,172,KEY,rest='flat'); face(HM,brow=.05,brow_r=-12); ots(AU,HM,side=.8)
            elif view=='R_doc': talk(AU,t,173,180,KEY,rest='grin',rate=7); face(AU,brow=.08); AU['arm'][-1].rotation_euler=(R(-50),0,R(30)); ots(HM,AU,back=1.0,side=-.4)
            elif view=='R_pata': talk(HM,t,181,187,KEY,rest='flat'); face(HM,brow=.04); ots(AU,HM,side=-.8)
            elif view=='R_bilkul': talk(AU,t,188,194,KEY,rest='grin',rate=7); face(AU,brow=.1,eyes=1.1); AU['arm'][-1].rotation_euler=(R(-120),0,R(10)); ots(HM,AU,side=.8)
            elif view=='R_ammi':
                k=ease(cl(t/.25)); HM['root'].rotation_euler[2]=R(L(-90,-150,k)); look_at(HM,headpos(AM),.8); talk(HM,t,195,195,KEY,rest='O',shapes=('shout','O'))
                face(HM,brow=.15,eyes=1.3); arms(HM,-60,0,30,-60,0,-30); cf(HM,d=1.4,lat=0,lens=30)
            else: talk(AM,t,196,201,KEY,rest='smile',rate=6); face(AM,brow=.03,brow_r=-8); AM['arm'][1].rotation_euler=(R(-50),0,R(-20)); look_at(AM,headpos(HM),.6); cf(AM,d=1.6,lat=.35,lens=30)
            return
        # V / T: Hamza + Ammi on two-seater, phone call
        nb.scale=(0,0,0)
        x,y,rz=POS['hm_seat']; seat(HM,t,x,y,rz); x,y,rz=POS['am_seat']; seat(AM,t,x,y,rz)
        if g=='V':
            hph.scale=(1,1,1); phone_front(HM,1); look_at(AM,headpos(HM),.4); look_at(AU,headpos(HM),.5)
            hp=headpos(HM)
            if view=='V_came':
                k=cl((t-1.0)/1.0); HM['arm'][-1].rotation_euler=(R(-165*math.sin(math.pi*k)),0,R(15)); face(HM,mouth='grin' if t>2.2 else 'flat',brow=.05,eyes=1.05)
                HM['root'].rotation_euler[0]=R(-3); q=ease(t/DUR); camset((L(1.6,.9,q),L(-1.4,-.2,q),1.55),(hp.x,hp.y,hp.z-.15),26,3.5)
            elif view=='V_wa': talk(HM,t,265,267,KEY,rest='grin'); face(HM,brow=.06); camset((hp.x+.15,hp.y-1.45,hp.z-.1),(hp.x,hp.y,hp.z-.2),28,2.5)
            elif view=='V_froze':
                face(HM,mouth='flat',eyes=1.35,brow=.14) if t<wl(275,KEY) else None; talk(HM,t,275,279,KEY,rest='flat',rate=6) if t>=wl(275,KEY)-.05 else None
                HM['arm'][-1].rotation_euler=(R(-40),0,R(10)) if t>wl(276,KEY) else (0,0,0); q=ease(t/DUR); camset((hp.x+.1,hp.y-L(1.7,1.3,q),hp.z-.1),(hp.x,hp.y,hp.z-.2),28,2.5)
            elif view=='V_really': talk(HM,t,285,285,KEY,rest='grin'); face(HM,brow=.12,eyes=1.15); camset((hp.x+.15,hp.y-1.45,hp.z-.1),(hp.x,hp.y,hp.z-.2),28,2.5)
            else:
                k=ease(cl(t/.6)); HM['head'].rotation_euler[2]=R(-50*k); talk(HM,t,303,309,KEY,rest='flat',rate=5); face(HM,brow=.03,brow_r=-15,eyes=.9)
                look_at(AM,headpos(HM),.6); face(AM,mouth='flat',brow=.05); camset((.65,.6,1.65),(.65,2.45,1.5),26,4.0)
            return
        # T
        if view in ('T_ring','T_beta','T_larki','T_haan','T_unko'):
            aph.scale=(1,1,1) if view=='T_ring' else (0,0,0)
        if view=='T_ring':
            k=cl((t-.6)/.4); AU['arm'][1].rotation_euler=(R(L(-60,-150,k)),0,R(L(-25,-28,k))); talk(AU,t,314,319,KEY,rest='o',rate=6) if t>wl(314,KEY)-.05 else face(AU,mouth='o')
            face(AU,brow=.08); camset((-1.4,-1.2,1.45),(-3.2,.2,1.35),26,4.0)
        elif view=='T_beta': talk(AU,t,320,325,KEY,rest='grin',rate=7); face(AU,brow=.1,eyes=1.15); AU['arm'][1].rotation_euler=(R(-40),0,R(-70)); look_at(AU,headpos(HM),.7); cf(AU,d=1.8,lat=.35,lens=28)
        elif view=='T_abkya': talk(HM,t,326,327,KEY,rest='O',shapes=('shout','O')); face(HM,brow=-.05,brow_r=20,eyes=1.2); arms(HM,-100,0,40,-100,0,-40); look_at(HM,headpos(AU),.6); cf(HM,d=1.5,lat=-.2,lens=30)
        elif view=='T_larki': talk(AU,t,328,337,KEY,rest='grin',rate=7); face(AU,brow=.06); gesture(AU,t,1); look_at(AU,headpos(HM),.6); cf(AU,d=1.7,lat=-.35,lens=30)
        elif view=='T_serious': talk(HM,t,338,338,KEY,rest='grin'); face(HM,eyes=1.1,brow=.1); arms(HM,-150,0,30,-150,0,-30); look_at(HM,headpos(AU),.5); cf(HM,d=1.4,lat=-.2,lens=30)
        elif view=='T_haan': talk(AU,t,339,343,KEY,rest='flat',rate=5); face(AU,brow=.0,brow_r=-15); AU['arm'][1].rotation_euler=(R(-100),0,R(-10)); look_at(AU,headpos(HM),.6); cf(AU,d=1.5,lat=.3,lens=30)
        elif view=='T_kya': talk(HM,t,344,344,KEY,rest='o'); face(HM,brow=.08,eyes=1.1); look_at(HM,headpos(AU),.6); camset((headpos(HM).x+.1,headpos(HM).y-1.5,headpos(HM).z-.1),tuple(headpos(HM)-Vector((0,0,.2))),28,2.5)
        elif view=='T_unko':
            talk(AU,t,345,351,KEY,rest='grin',rate=5); face(AU,brow=.06); look_at(AU,headpos(AB),.8); AU['arm'][1].rotation_euler=(R(-90),0,R(-60)) if t>wl(347,KEY) else (R(-40),0,0)
            q=ease(t/DUR); cf(AU,d=L(1.8,1.3,q),lat=.3,lens=30)
        elif view=='T_silent':
            for H in (HM,AM,AU): look_at(H,headpos(AB),.8); face(H,mouth='o',brow=.1,eyes=1.2)
            q=ease(t/DUR); camset((L(-.6,-.3,q),-3.3,L(2.4,2.6,q)),(0,1.0,.9),20,8.0)
        elif view=='T_remote':
            k=ease(cl((t-.3)/1.6)); AB['arm'][1].rotation_euler=(R(L(-55,-5,k)),0,R(-10)); AB['root'].rotation_euler[2]=R(L(90,210,ease(cl((t-1.3)/.7)))); face(AB,mouth='flat',eyes=1.25,brow=.1)
            hp=headpos(AB); camset((1.2,.9,hp.z-.05),(hp.x,hp.y,hp.z-.3),30,3.0)
        else:
            AB['arm'][1].rotation_euler=(R(-5),0,R(-10)); AB['root'].rotation_euler[2]=R(210); talk(AB,t,361,367,KEY,rest='O',rate=7,shapes=('shout','O','o')); face(AB,brow=.13,eyes=1.3)
            AB['arm'][-1].rotation_euler=(R(-50),0,R(60)); cf(AB,d=1.7,lat=.3,lens=30)
            for H in (HM,AM,AU): look_at(H,headpos(AB),.8)
    return dict(upd=upd)
for v in ('D_abbu','D_abbu2','G_walk','G_salam','G_yeh','Q_height','Q_salary','Q_abhi','Q_matlab','Q_future','Q_gaari','Q_ghar','Q_biz','Q_close','Q_apna','Q_dua',
          'R_ruko','R_photo','R_kaun','R_doc','R_pata','R_bilkul','R_ammi','R_conf','V_came','V_wa','V_froze','V_really','V_ammi',
          'T_ring','T_beta','T_abkya','T_larki','T_serious','T_haan','T_kya','T_unko','T_silent','T_remote','T_main'): SHOTS[v]=(lambda v=v: SH_D(v))

# ============================================================ GATE (doorbell)
def SH_G(view):
    KEY=view; set_colony('morning_s'); AU=person((0,0,0),180,AUNTY,'smirk',name='aunty'); nb=notebook(AU,-1); hb=handbag(AU,1)
    def upd(t):
        k=ease(cl(t/1.2)); AU['root'].location=(L(-2.5,1.45,k),L(2.6,3.75,k),.008); AU['z0']=0; AU['root'].rotation_euler[2]=R(L(110,180,cl((t-.9)/.3)))
        walk(AU,k*4,step=.45,arm=12) if k<1 else stand(AU,t); blink(AU,t); AU['arm'][-1].rotation_euler=(R(-65),0,R(20))
        p=ease(cl((t-1.3)/.3))-ease(cl((t-1.9)/.3)); AU['arm'][1].rotation_euler=(R(-95*p),0,R(-10*p)); face(AU,mouth='smirk',brow=-.02)
        camset((3.8,1.2,1.55),(.6,4.1,1.5),24,5.0)
    return dict(upd=upd)
SHOTS['G_bell']=lambda: SH_G('G_bell')

# ============================================================ PHONE CALL: Hamza (bedroom) / Bilal (rooftop)
def SH_C(view):
    KEY=view; hamza_side=view in ('C_call','C_bhai','C_ready','C_pagal','C_karachi')
    if hamza_side:
        Rb=set_bed(); HM=person((0,0,0),0,HAMZA,'frown',name='hamza'); ph=phone(HM,1,'#7FD3FF'); Rb['blanket'].location=(.2,1.2,.58); Rb['blanket'].scale=(1,1.6,.5)
        Rb['door'].location=(2.5,-2.28,1.1)
        def upd(t):
            if view=='C_call':
                k=cl((t-.3)/1.0); x=L(-1.6,.6,ease(cl(t/2.2))); HM['root'].location=(x,-.9,.008); HM['z0']=0; HM['root'].rotation_euler[2]=R(90); walk(HM,x,step=.5,arm=10) if t<2.2 else stand(HM,t)
                blink(HM,t); HM['arm'][1].rotation_euler=(R(L(-20,-150,k)),0,R(L(0,-28,k))); face(HM,mouth='frown',brow=.06,brow_r=-12)
                camset((x+1.5,-2.0,1.7),(x,-.9,1.6),24,4.0)
            else:
                ph_=(view=='C_bhai'); x=.6+.25*math.sin(t*.9); HM['root'].location=(x,-.9,.008); HM['z0']=0; HM['root'].rotation_euler[2]=R(-15+20*math.sin(t*.7)); stand(HM,t); HM['root'].location[2]=.008; blink(HM,t)
                phone_ear(HM,1); a,b={'C_bhai':(208,213),'C_ready':(215,218),'C_pagal':(225,226),'C_karachi':(235,239)}[view]
                talk(HM,t,a,b,KEY,rest='frown',shapes=('shout','O','flat')); face(HM,brow=.1 if view!='C_pagal' else -.05,brow_r=-14 if view!='C_pagal' else 18)
                gesture(HM,t,-1,1.2); cf(HM,d=1.7,lat=-.45,lens=30)
        return dict(upd=upd)
    set_roof(); BL=person((0,0,0),0,BILAL,'grin',name='bilal'); ph=phone(BL,1,'#7FD3FF')
    chips=empty((0,0,0)); obox((0,0,0),(.09,.04,.13),M('#E8B92E',.4),.02,chips); obox((0,-.042,.02),(.06,.002,.05),M('#C9302C',.4),0,chips)
    def upd(t):
        a,b={'C_congrats':(214,214),'C_simple':(219,224),'C_dubai':(227,234),'C_bro':(240,249)}[view]
        if view!='C_bro':
            seat(BL,t,0,.55,0,sh=.46); phone_ear(BL,1); BL['arm'][-1].rotation_euler=(R(-55),0,R(10)); bpy.context.view_layer.update(); chips.location=hand_pos(BL,-1)+Vector((0,-.04,.05))
        else:
            k=ease(cl(t/.5)); seat(BL,t,0,.55,0,sh=.46); BL['root'].location[2]=L(BL['root'].location[2],.008,k)
            for q in (1,-1): BL['leg'][q].rotation_euler[0]=-R(90)*(1-k)
            phone_ear(BL,1); BL['arm'][-1].rotation_euler=(R(-40),0,R(70+10*math.sin(t*5))); bpy.context.view_layer.update(); chips.location=(-.5,.6,.47)
        talk(BL,t,a,b,KEY,rest='grin',rate=7); face(BL,brow=.06 if view!='C_bro' else .1,eyes=1.0)
        q=ease(t/DUR)
        if view=='C_congrats': camset((L(-1.6,-1.2,q),-2.6,1.7),(0,.55,1.3),24,5.0)
        elif view=='C_bro': cf(BL,d=L(2.4,1.9,q),lat=.2,dz=-.3,lens=28,tgt_dz=-.1)
        else: cf(BL,d=1.6,lat=.35 if view=='C_simple' else -.35,dz=-.05,lens=30)
    return dict(upd=upd)
for v in ('C_call','C_bhai','C_congrats','C_ready','C_simple','C_pagal','C_dubai','C_karachi','C_bro'): SHOTS[v]=(lambda v=v: SH_C(v))

# ============================================================ VIDEO CALL: doctor
def SH_V(view):
    KEY=view; set_clinic(); DC=person((0,0,0),0,DOC,'smile',name='doc')
    def upd(t):
        seat(DC,t,0,1.45,0,sh=.52); DC['arm'][1].rotation_euler=(R(-60),0,R(-15)); DC['arm'][-1].rotation_euler=(R(-60),0,R(15))
        a,b={'V_salam':(264,264),'V_what':(268,272),'V_same':(280,284),'V_yes':(286,302)}[view]
        talk(DC,t,a,b,KEY,rest='smile',rate=6); face(DC,brow=.03)
        if view=='V_yes': DC['arm'][1].rotation_euler=(R(-70+10*math.sin(t*3)),0,R(-30)); face(DC,brow=.06)
        if view=='V_same': DC['head'].rotation_euler[1]=R(8*math.sin(t*1.5))
        hp=headpos(DC); camset((hp.x,hp.y-1.55,hp.z-.05),(hp.x,hp.y,hp.z-.25),26,4.0)
    return dict(upd=upd)
for v in ('V_salam','V_what','V_same','V_yes'): SHOTS[v]=(lambda v=v: SH_V(v))

# ============================================================ ENDING: no escape
def SH_E(view):
    KEY=view; set_colony('golden'); HM=person((0,0,0),0,HAMZA,'grin',name='hamza'); AU=person((0,0,0),0,AUNTY,'smirk',name='aunty'); nb=notebook(AU,-1)
    def upd(t):
        if view=='E_out':
            hideH(AU); y=L(3.7,1.6,ease(cl(t/2.6))); HM['root'].location=(.3,y,.008); HM['z0']=0; HM['root'].rotation_euler[2]=0; walk(HM,y,step=.5,arm=22) if t<2.6 else stand(HM,t); blink(HM,t)
            if t>2.7: arms(HM,-170,0,30,-170,0,-30)
            face(HM,mouth='grin',eyes=.85,brow=.05); q=ease(t/DUR); camset((L(1.6,1.0,q),L(-1.6,-1.0,q),1.6),(.3,y,1.6),26,5.0)
        elif view=='E_aunty':
            put_at(HM,t,.3,1.6,-90); look_at(HM,(-5,1.6,1.5),.6); face(HM,mouth='smile' if t<1.0 else 'O',brow=.12 if t>1.0 else 0)
            k=ease(cl(t/.8)); put_at(AU,t,-4.6,L(4.2,3.4,k),-90); AU['arm'][-1].rotation_euler=(R(-70),0,R(25)); face(AU,mouth='grin',brow=-.02,brow_r=-14)
            AU['arm'][1].rotation_euler=(R(-140),0,R(-10)) if t>.9 else (0,0,0)
            camset((1.8,-.6,1.55),(-2.0,2.4,1.45),24,6.0)
        else:
            put_at(HM,t,.3,1.6,-90); shock(HM,1.0); face(HM,mouth='O',eyes=1.4,brow=.16); arms(HM,-160,0,40,-160,0,-40)
            put_at(AU,t,-1.0,1.6,90); AU['arm'][-1].rotation_euler=(R(-75),0,R(25)); AU['arm'][1].rotation_euler=(R(-60),0,R(-25)); face(AU,mouth='grin',brow=-.03,brow_r=-16)
            look_at(AU,headpos(HM),.6); ots(AU,HM,side=-.8,back=L(1.8,1.3,ease(t/DUR)))
    return dict(upd=upd)
for v in ('E_out','E_aunty','E_noesc'): SHOTS[v]=(lambda v=v: SH_E(v))
