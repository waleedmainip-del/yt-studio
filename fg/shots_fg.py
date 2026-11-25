# Shots for "Family Group". SEQ/END are filled by gen_seq.py.
SHOTS={}
END=94.6667
SEQ=[('HOOK', 0.0), ('MEME', 5.633), ('UI_MEME', 9.433), ('SEND', 13.433), ('UI_GROUP', 14.8), ('PANIC', 18.6), ('UI_DELETE', 20.033), ('UI_SEEN0', 23.6), ('ABBU', 29.2), ('STEAL', 33.5), ('CHACHA', 36.1), ('MIT1', 41.733), ('RIDE', 46.367), ('PH_DOOR', 50.667), ('GRAB', 55.8), ('CHAI', 61.067), ('RELIEF', 63.733), ('UI_SEEN1', 67.233), ('DADI', 71.2), ('DADI1', 74.5), ('WQ', 78.2), ('DADI2', 79.933), ('UI_CALL', 84.2), ('UI_LEFT', 85.7), ('CTA', 91.033)]
import os as _os
FILLE=[45.0]; _FL=[]
_camset0=camset
def camset(loc,tg,lens,*a,**k):
    _camset0(loc,tg,lens,*a,**k)
    if not _FL: _FL.append(point((0,0,0),FILLE[0],(1,.93,.85),r=.4,shadow=False))
    v=Vector(tg)-Vector(loc); _FL[0].location=Vector(loc)+v.normalized()*min(1.0,v.length*.3)+Vector((0,0,.35)); _FL[0].data.energy=FILLE[0]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0
def we(i): return W_[i]['e']-T0
def mk(C,x,y,rz,name,z=0.0): return avatar_bg((x,y,z),rz,C,name=name)
def fwd(rz): return (math.sin(R(rz)),-math.cos(R(rz)))
def drift(c0,tg,t,a=.06): q=ease(t/DUR); return LV(c0,(L(c0[0],tg[0],a),L(c0[1],tg[1],a),c0[2]),q)
def closecam(H,rz,side=.3,dist=3.0,dz=.05,tz=-.3,lens=36,bias=0.0):
    h=hp(H); f=fwd(rz); f=(f[0],f[1]-bias); n_=math.hypot(*f); f=(f[0]/n_,f[1]/n_); rt=(-f[1],f[0])
    return (h[0]+f[0]*dist+rt[0]*side,h[1]+f[1]*dist+rt[1]*side,h[2]+dz),(h[0],h[1],h[2]+tz),lens
def hidep(H):
    for o in [H['root']]: o.location=(o.location[0],o.location[1],-40)
def home_set(mood='night'):
    home_fg(); _S,_A,_w,_bg=setup_interior(mood,room=(1.5,0,3.6),res=PCT,samples=SAMPLES,shadow_dist=18); _A.data.energy*=.4 if mood=='night' else .6
def phone_glow(ph,P=18):
    l=point((0,0,0),P,(.75,.85,1.0),r=.05); l.parent=ph; l.location=(0,-.25,0); return l
def lie(H,x,yf,z=.86):
    H['root'].location=(x,yf,z); H['root'].rotation_euler=(R(-90),0,0)
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-8),0,R(s*8)); H['leg'][s].rotation_euler=(0,0,0)
# ================================================================ Waleed's room
WBED=(-9.2,1.75)
def bedsit(H,t):
    """Waleed sitting up in bed against the headboard (bed runs along x, headboard at x=-10.4)"""
    seat(H,t,.72); H['root'].location=(-9.6,1.55,0); H['root'].rotation_euler=(0,0,R(0))
def ROOM_SHOT(cam,mood_face='smirk',talk_=None,react=None,pk=None):
    def S_():
        home_set(); wa=mk(WALEED,-9.6,1.55,0,'wa'); ph=phone_in_hand(wa,1,'#DFF6E8',em=1.1); phone_glow(ph,4)
        def upd(t):
            bedsit(wa,t); blink(wa,t); u=wa['u']
            arm_to(wa,1,root_mat(wa)@Vector((.25*u,-1.35*u,3.55*u)),1); arm_to(wa,-1,root_mat(wa)@Vector((-.1*u,-1.35*u,3.4*u)),1)
            look_at(wa,ph.matrix_world.translation,.75,maxpitch=40)
            if talk_: talk(wa,t,*wt(*talk_),rest='O')
            face(wa,mouth=mood_face if not talk_ else None,brow=.04)
            if react: react(wa,t,ph)
            cam(wa,t)
        return dict(upd=upd)
    return S_
def _hook_cam(wa,t): q=ease(t/DUR); camset(LV((-6.4,-2.2,2.6),(-7.4,-1.0,2.2),q),LV((-9.3,1.4,1.4),(-9.5,1.5,1.55),q),L(24,30,q),4)
def _hook_react(wa,t,ph):
    k=math.sin(t*2.0); face(wa,mouth='smile' if k>0 else 'grin',brow=.03)
SHOTS['HOOK']=ROOM_SHOT(_hook_cam,react=_hook_react)
for _i,(_x,_z,_c) in enumerate(((-9.2,2.8,'#25D366'),(-8.8,3.1,'#25D366'),(-9.6,3.3,'#25D366'))): pass
def _meme_cam(wa,t): c0,tg,ln=closecam(wa,0,.35,2.6,dz=.15,lens=34,tz=-.3); camset(drift(c0,tg,t,.1),tg,ln,2.8)
def _meme_react(wa,t,ph):
    face(wa,mouth='grin' if t>DUR*.3 else 'smirk',brow=.05); wa['head'].rotation_euler[1]+=R(4*math.sin(t*9)*tl(t,DUR*.5,DUR*.55)*(1-tl(t,DUR*.8,DUR*.85)))
SHOTS['MEME']=ROOM_SHOT(_meme_cam,react=_meme_react)
def _send_cam(wa,t): q=ease(t/DUR); c0,tg,ln=closecam(wa,0,-.25,2.2,dz=-.15,lens=36,tz=-.5); camset(LV(c0,(c0[0],c0[1]+.25,c0[2]),q),tg,ln,2.8)
def _send_react(wa,t,ph):
    k=tl(t,ws(45)-.1,ws(45)+.2); face(wa,mouth='grin' if k<.5 else 'flat',eyes=1+.3*k,brow=.04+.04*k)
    if t<ws(42)+.3: wa['arm'][-1].rotation_euler[0]+=R(-6*max(0,math.sin((t-ws(41))*14))) if t>ws(41) else 0
SHOTS['SEND']=ROOM_SHOT(_send_cam,react=_send_react)
def PANIC():
    home_set(); wa=mk(WALEED,-9.6,1.55,0,'wa'); ph=phone_in_hand(wa,1,'#DFF6E8',em=1.1); phone_glow(ph,4)
    def upd(t):
        bedsit(wa,t); u=wa['u']; k=ease(tl(t,0,.25))
        wa['root'].location[2]=.06*k; arm_to(wa,1,root_mat(wa)@Vector((.2*u,-1.6*u,L(3.55,4.1,k)*u)),1); arm_to(wa,-1,root_mat(wa)@Vector((-.7*u,.1*u,6.1*u)),k)
        talk(wa,t,*wt(51,54),rest='O'); face(wa,brow=.07,eyes=1.35); wa['head'].rotation_euler[2]=R(14*math.sin(t*18)*k)
        c0,tg,ln=closecam(wa,0,0,2.3,dz=0,lens=32,tz=-.4); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['PANIC']=PANIC
# ================================================================ Abbu's room
def ABBU_S():
    home_set(); ab=mk(ABBU,0,0,0,'abbu'); wa=mk(WALEED,-2.8,-1.6,0,'wa'); u=ab['u']
    ph=empty((0,0,0)); obox((0,0,0),(.13,.22,.012),M('#16171C',.3,spec=.8),.01,ph); obox((0,0,.013),(.12,.2,.002),M('#2A3A5A',.3,emit=.4),0,ph)
    def upd(t):
        lie(ab,ABBU_BED[0],ABBU_BED[1]-1.15); blink(ab,t)
        br=1+.03*math.sin(t*2.2); ab['root'].scale=(1,1,1); face(ab,mouth='O' if math.sin(t*2.2)>0 else 'flat',eyes=0.05)
        bp=root_mat(ab)@Vector((0,-.6*u,3.05*u)); ph.location=bp+Vector((0,0,.02+.015*math.sin(t*2.2))); ph.rotation_euler=(0,0,R(8))
        k=ease(tl(t,.3,DUR-.3)); x=L(-2.8,-.15,k); y=L(-1.6,.9,k); wa['root'].location=(x,y,0); wa['root'].rotation_euler=(0,0,R(face_dir(1.0,1.0)*(1-k)+face_dir(1.4,.4)*k))
        if 0<k<1: walk(wa,k*5.0+wa['seed'],step=.38,arm=10); wa['root'].rotation_euler[0]=R(6)
        else: stand(wa,t)
        blink(wa,t); face(wa,mouth='flat',brow=.06,eyes=1.15); wa['arm'][1].rotation_euler=(R(-60),0,R(10)); wa['arm'][-1].rotation_euler=(R(-40),0,R(-30))
        q=ease(t/DUR); camset(LV((3.6,-2.6,2.7),(3.2,-2.2,2.6),q),LV((.6,.6,1.0),(.6,.8,1.1),q),22,4)
    return dict(upd=upd)
SHOTS['ABBU']=ABBU_S
def STEAL():
    home_set(); ab=mk(ABBU,0,0,0,'abbu'); wa=mk(WALEED,-.05,.95,0,'wa'); u=ab['u']
    ph=empty((0,0,0)); obox((0,0,0),(.13,.22,.012),M('#16171C',.3,spec=.8),.01,ph); scr=obox((0,0,.013),(.12,.2,.002),M('#DFF6E8',.3,emit=1.6),0,ph); phone_glow(ph,3)
    def upd(t):
        lie(ab,ABBU_BED[0],ABBU_BED[1]-1.15); face(ab,mouth='O' if math.sin(t*2.2)>0 else 'flat',eyes=0.05)
        bp=root_mat(ab)@Vector((0,-.6*ab['u'],3.05*ab['u']))+Vector((0,0,.02))
        k=ease(tl(t,.2,.9)); kb=ease(tl(t,DUR-.7,DUR-.2))
        wa['root'].location=(-.05,.95,0); wa['root'].rotation_euler=(R(18*k),0,R(face_dir(1.25,.0))); stand(wa,t); blink(wa,t)
        hand=wa['arm'][1].matrix_world@Vector(hand_loc(wa,1))
        tgt=bp.lerp(Vector((bp.x-.3,bp.y,bp.z+.5)),ease(tl(t,1.0,1.5))*(1-kb)); arm_to(wa,1,tgt,max(k,1-kb) if t<DUR-.2 else 0)
        ph.location=tgt if 1.0<t<DUR-.5 else bp; ph.rotation_euler=(R(-60*ease(tl(t,1.0,1.5))*(1-kb)),0,R(8))
        wa['cheek_puff']=1; face(wa,mouth='flat',brow=.06,eyes=1.1); look_at(wa,ph.location,.85,maxpitch=60)
        camset((3.6,-.1,2.3),(.5,.85,1.05),24,4)
    return dict(upd=upd)
SHOTS['STEAL']=STEAL
# ================================================================ lane / Chacha / Phuppo gate
def lane_set():
    lane_fg(); setup_world('night',shadow=40)
def CHACHA_():
    lane_set(); ch=mk(CHACHA,CHACHA_DOOR[0],CHACHA_DOOR[1]-.35,0,'ch'); wa=mk(WALEED,CHACHA_DOOR[0]+.7,CHACHA_DOOR[1]-1.5,0,'wa'); ph=phone_in_hand(ch,1,'#2A3A5A',em=.6)
    def upd(t):
        stand(ch,t); blink(ch,t); face(ch,mouth='O' if t<1.4 else 'flat',eyes=.7,brow=-.03); ch['arm'][-1].rotation_euler=(R(-150*(1-tl(t,.0,1.2))),0,R(-20))
        k=ease(tl(t,ws(110)+.1,ws(110)+.6)); arm_to(ch,1,Vector((CHACHA_DOOR[0]+.35,CHACHA_DOOR[1]-.95,1.3)),k)
        wa['root'].location=(CHACHA_DOOR[0]+.7,CHACHA_DOOR[1]-1.5,0); wa['root'].rotation_euler=(0,0,R(face_dir(-.7,1.15))); stand(wa,t); blink(wa,t)
        talk(wa,t,*wt(103,110),rest='smile'); face(wa,brow=.05,brow_r=8); wa['arm'][1].rotation_euler=(R(-45),0,R(15))
        q=ease(t/DUR); camset(LV((CHACHA_DOOR[0]-2.6,CHACHA_DOOR[1]-4.6,1.9),(CHACHA_DOOR[0]-2.3,CHACHA_DOOR[1]-4.2,1.85),q),(CHACHA_DOOR[0]+.3,CHACHA_DOOR[1]-.9,1.55),24,4)
    return dict(upd=upd)
SHOTS['CHACHA']=CHACHA_
def MIT1():
    lane_set(); ch=mk(CHACHA,CHACHA_DOOR[0],CHACHA_DOOR[1]-.35,0,'ch'); wa=mk(WALEED,CHACHA_DOOR[0]+.7,CHACHA_DOOR[1]-1.5,0,'wa'); ph=phone_in_hand(wa,1,'#DFF6E8',em=1.1); phone_glow(ph,3)
    def upd(t):
        stand(ch,t); blink(ch,t); ch['arm'][-1].rotation_euler=(R(-150),0,R(-20)) if int(t*.7)%2 else (R(-5),0,R(-6)); face(ch,mouth='O' if int(t*.7)%2 else 'flat',eyes=.5)
        wa['root'].location=(CHACHA_DOOR[0]+.7,CHACHA_DOOR[1]-1.5,0); wa['root'].rotation_euler=(0,0,R(20)); stand(wa,t); blink(wa,t); u=wa['u']
        arm_to(wa,1,root_mat(wa)@Vector((.25*u,-1.3*u,3.6*u)),1); look_at(wa,ph.matrix_world.translation,.7*(1-tl(t,ws(113)-.2,ws(113)+.2)),maxpitch=40)
        k=tl(t,ws(113)-.2,ws(113)+.3); face(wa,mouth='smile' if k<.5 else 'flat',brow=.03 if k<.5 else -.06,brow_r=0 if k<.5 else -14)
        c0,tg,ln=closecam(wa,20,.3,L(3.2,2.0,ease(tl(t,ws(113),DUR))),lens=32,tz=-.45); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['MIT1']=MIT1
def RIDE():
    lane_set(); mb=motorbike((0,0,0),180,'#2A2C34'); mb['root'].scale=(1.4,)*3
    rid=mk(WALEED,0,0,0,'rider'); rid['root'].parent=mb['root']; rid['root'].location=(-.05,0,.35); rid['root'].rotation_euler=(0,0,R(90)); rid['root'].scale=(1/1.4,)*3
    def upd(t):
        k=tl(t,0,ws(130)); x=L(4,PHUPPO_GATE[0]-1.8,ease_out(k)); mb['root'].location=(x,PHUPPO_GATE[1]-2.7,0); mb['root'].rotation_euler=(0,0,0)
        for w_ in mb['wheels']: w_.rotation_euler[1]=x/.45
        sit(rid,1,.85,legs=80); blink(rid,t); face(rid,mouth='flat',brow=-.05,brow_r=-10)
        for s in (1,-1): rid['arm'][s].rotation_euler=(R(-75),0,R(s*8))
        if t<ws(128)-.3: camset((x+3.6,PHUPPO_GATE[1]-6.2,1.7),(x-.2,PHUPPO_GATE[1]-2.5,1.3),26,4)
        else: camset((PHUPPO_GATE[0]-5.2,PHUPPO_GATE[1]-6.2,1.7),(PHUPPO_GATE[0]-.6,PHUPPO_GATE[1]-1.2,1.5),22,4)
    return dict(upd=upd)
SHOTS['RIDE']=RIDE
def PH_DOOR():
    lane_set(); P=PHUPPO_GATE; pp=mk(PHUPPO,P[0],P[1]-.3,0,'pp'); wa=mk(WALEED,P[0]+.55,P[1]-1.6,0,'wa')
    def upd(t):
        stand(pp,t); blink(pp,t); talk(pp,t,*wt(134,136),rest='flat'); face(pp,brow=-.05,brow_r=-12,eyes=.9)
        pp['arm'][1].rotation_euler=(R(-25),0,R(30)); pp['arm'][-1].rotation_euler=(R(-25),0,R(-30))
        wa['root'].location=(P[0]+.55,P[1]-1.6,0); wa['root'].rotation_euler=(0,0,R(face_dir(-.55,1.3))); stand(wa,t); blink(wa,t)
        talk(wa,t,*wt(137,150),rest='grin'); face(wa,brow=.05,brow_r=8); kk=tl(t,ws(146)-.1,ws(146)+.2); wa['arm'][1].rotation_euler=(R(-40-30*kk),0,R(20))
        if t<ws(137)-.1: camset((P[0]-1.3,P[1]-3.8,1.8),(P[0]+.15,P[1]-.5,1.6),30,2.8)
        else: camset((P[0]-1.6,P[1]-4.2,1.9),(P[0]+.3,P[1]-.9,1.6),26,4)
    return dict(upd=upd)
SHOTS['PH_DOOR']=PH_DOOR
# ================================================================ Phuppo's drawing room
def ph_set():
    phuppo_in(); _S,_A,_w,_bg=setup_interior('night',room=(PH_X,0,3.6),res=PCT,samples=SAMPLES,shadow_dist=14); _A.data.energy*=.45
    phn=empty((PH_X+.25,.65,.47)); obox((0,0,0),(.13,.22,.012),M('#16171C',.3,spec=.8),.01,phn); obox((0,0,.013),(.12,.2,.002),M('#DFF6E8',.3,emit=1.4),0,phn); return phn
def GRAB():
    phn=ph_set(); pp=mk(PHUPPO,PH_X-.75,.0,90,'pp'); wa=mk(WALEED,PH_X+1.25,.1,-90,'wa')
    def upd(t):
        stand(pp,t); blink(pp,t); stand(wa,t); blink(wa,t)
        kp=ease(tl(t,ws(153)-.2,ws(158))); arm_to(pp,1,Vector((PH_X+.25-.35*(1-kp),.65,.6+.4*(1-kp))),kp*.9); pp['root'].rotation_euler=(R(14*kp),0,R(90))
        kw=ease(tl(t,ws(161)-.15,ws(163))); hand=phn.location
        if t<ws(163): arm_to(wa,1,Vector((PH_X+.25,.65,.55)),kw); wa['root'].rotation_euler=(R(18*kw),0,R(-90))
        else:
            kk=ease(tl(t,ws(163),ws(163)+.4)); p_=Vector((PH_X+.25,.65,.5)).lerp(Vector((PH_X+.95,.0,1.55)),kk); arm_to(wa,1,p_,1); phn.location=p_; phn.rotation_euler=(R(-70*kk),0,0)
            wa['root'].rotation_euler=(R(18*(1-kk)),0,R(-90)); look_at(wa,p_,.8*kk,maxpitch=50)
        face(pp,mouth='flat',brow=0); face(wa,mouth='grin' if t>ws(165) else 'flat',brow=.05,eyes=1.15)
        slow=1.0
        if t<ws(160): camset((PH_X+.25,-3.0,1.6),(PH_X+.25,.55,.6),22,4)
        else: camset((PH_X+.25,-3.6,2.4),(PH_X+.25,.3,1.15),24,4)
    return dict(upd=upd)
SHOTS['GRAB']=GRAB
def CHAI():
    phn=ph_set(); phn.location=(0,0,-20); pp=mk(PHUPPO,PH_X-.55,-.2,40,'pp'); wa=mk(WALEED,PH_X+.75,-.35,-50,'wa')
    cup=empty((0,0,0),pp['arm'][1]); cup.location=(.5*pp['u'],-.3*pp['u'],-2.1*pp['u']); ocyl((0,0,0),.07,.11,M('#F4F1EA',.25),cup,rot=(0,0,0)); ocyl((0,0,.045),.06,.02,M('#B07A4A',.4),cup,rot=(0,0,0))
    def upd(t):
        stand(pp,t); blink(pp,t); talk(pp,t,*wt(168,175),rest='smile'); face(pp,brow=.05)
        arm_to(pp,1,root_mat(pp)@Vector((.35*pp['u'],-1.4*pp['u'],3.4*pp['u'])),ease(tl(t,ws(172)-.3,ws(172)+.2)))
        k=tl(t,ws(168),ws(168)+.3)*(1-tl(t,ws(171),ws(171)+.3)); arm_to(pp,-1,Vector(hp(wa))+Vector((0,0,.35)),k)
        stand(wa,t); blink(wa,t); face(wa,mouth='grin',brow=.03); wa['head'].rotation_euler[0]=R(-6*k)
        c0,tg,ln=closecam(pp,40,-.4,3.2,lens=30,tz=-.5); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['CHAI']=CHAI
def RELIEF():
    phn=ph_set(); phn.location=(0,0,-20); wa=mk(WALEED,PH_X-.3,1.75,0,'wa'); ph=phone_in_hand(wa,1,'#DFF6E8',em=1.1); phone_glow(ph,3)
    cup=empty((0,0,0),wa['arm'][-1]); cup.location=(-.5*wa['u'],-.3*wa['u'],-2.1*wa['u']); ocyl((0,0,0),.07,.11,M('#F4F1EA',.25),cup,rot=(0,0,0))
    def upd(t):
        seat(wa,t,.62); wa['root'].location=(PH_X-.3,1.75,0); blink(wa,t); u=wa['u']
        k=ease(tl(t,ws(182)-.2,ws(183)+.2))
        arm_to(wa,-1,root_mat(wa)@Vector((-.3*u,-1.2*u,L(4.3,3.2,k)*u)),1); arm_to(wa,1,root_mat(wa)@Vector((.3*u,-1.2*u,L(2.6,3.6,k)*u)),1)
        kd=tl(t,ws(184),ws(184)+.25); face(wa,mouth='smile' if kd<.5 else 'O',eyes=.6 if t<ws(180) else 1+.35*kd,brow=-.02+.08*kd)
        look_at(wa,ph.matrix_world.translation,.8*k,maxpitch=45); wa['head'].rotation_euler[0]+=R(-8*(1-k)*(1-tl(t,0,.2)))
        c0,tg,ln=closecam(wa,0,.2,2.6,lens=32,tz=-.5); camset(LV(c0,(c0[0],c0[1]+.5,c0[2]),ease(tl(t,ws(184),DUR))),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['RELIEF']=RELIEF
# ================================================================ lounge (Dadi)
def dadi_set(): home_set(); da=mk(DADI,*DADI_SEAT,0,'dadi'); ph=phone_in_hand(da,1,'#F4E2B0',em=1.4); phone_glow(ph,3); return da,ph
def dseat(da,t): seat(da,t,.8); da['root'].location=(DADI_SEAT[0],DADI_SEAT[1],0)
def DADI_S():
    da,ph=dadi_set(); wa=mk(WALEED,7.0,-1.5,0,'wa')
    def upd(t):
        dseat(da,t); blink(da,t); u=da['u']; arm_to(da,1,root_mat(da)@Vector((.3*u,-1.3*u,3.0*u)),1); look_at(da,ph.matrix_world.translation,.6,maxpitch=40); face(da,mouth='smile',brow=.03)
        k=ease(tl(t,.1,DUR-.5)); wa['root'].location=(L(7.0,9.6,k),L(-1.5,-.2,k),0); wa['root'].rotation_euler=(0,0,R(face_dir(1,.5)))
        if 0<k<1: walk(wa,k*3.5+wa['seed'],step=.4,arm=16)
        else: stand(wa,t)
        blink(wa,t); face(wa,mouth='flat',brow=-.02,eyes=.85)
        q=ease(t/DUR); camset(LV((12.9,-3.6,2.1),(12.6,-3.2,2.0),q),LV((9.6,.4,1.2),(10.2,.8,1.25),q),22,4)
    return dict(upd=upd)
SHOTS['DADI']=DADI_S
def DTALK(a,b,react=None,cam='dadi'):
    def S_():
        da,ph=dadi_set(); wa=mk(WALEED,9.8,-.1,0,'wa')
        def upd(t):
            dseat(da,t); blink(da,t); u=da['u']; arm_to(da,1,root_mat(da)@Vector((.4*u,-1.4*u,3.4*u)),1)
            talk(da,t,*wt(a,b),rest='smile'); face(da,brow=.04); look_at(da,hp(wa),.6)
            wa['root'].location=(9.8,-.1,0); wa['root'].rotation_euler=(0,0,R(face_dir(1.2,2.1))); stand(wa,t); blink(wa,t)
            if react: react(wa,t)
            if cam=='dadi': c0,tg,ln=closecam(da,0,.3,3.0,dz=-.2,lens=30,tz=-.45); camset(drift(c0,tg,t),tg,ln,2.8)
            else: c0,tg,ln=closecam(wa,face_dir(1.2,2.1),-.35,2.4,lens=32,tz=-.4,bias=.0); camset(c0,tg,ln,2.8)
        return dict(upd=upd)
    return S_
def _wq(wa,t): talk(wa,t,*wt(210,212),rest='O'); face(wa,brow=.06,eyes=1.2); wa['arm'][1].rotation_euler=(R(-50),0,R(25))
def _wd(wa,t): face(wa,mouth='O',eyes=1.3,brow=.07); wa['root'].rotation_euler[0]=R(-4)
SHOTS['DADI1']=DTALK(200,209,react=lambda wa,t: face(wa,mouth='flat',eyes=1.1,brow=.04))
SHOTS['WQ']=DTALK(200,209,react=_wq,cam='wa')
SHOTS['DADI2']=DTALK(213,224,react=_wd)
def CTA():
    home_set(); wa=mk(WALEED,-9.6,1.55,0,'wa'); ph=phone_in_hand(wa,1,'#DFF6E8',em=1.1); phone_glow(ph,4)
    def upd(t):
        bedsit(wa,t); blink(wa,t); u=wa['u']; arm_to(wa,1,root_mat(wa)@Vector((.35*u,-1.2*u,3.0*u)),1)
        face(wa,mouth='flat',brow=-.06,brow_r=-14,eyes=.85); wa['head'].rotation_euler[0]=R(4)
        c0,tg,ln=closecam(wa,0,0,2.4,dz=0,lens=30,tz=-.45); q=ease(t/DUR); camset(LV(c0,(c0[0],c0[1]+.4,c0[2]),q),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['CTA']=CTA
for _k in ('UI_MEME','UI_GROUP','UI_DELETE','UI_SEEN0','UI_SEEN1','UI_CALL','UI_LEFT'): SHOTS[_k]=None
SEQ=[('HOOK', 0.0), ('MEME', 5.633), ('UI_MEME', 9.433), ('SEND', 13.433), ('UI_GROUP', 14.8), ('PANIC', 18.6), ('UI_DELETE', 20.033), ('UI_SEEN0', 23.6), ('ABBU', 29.2), ('STEAL', 33.5), ('CHACHA', 36.1), ('MIT1', 41.733), ('RIDE', 46.367), ('PH_DOOR', 50.667), ('GRAB', 55.8), ('CHAI', 61.067), ('RELIEF', 63.733), ('UI_SEEN1', 67.233), ('DADI', 71.2), ('DADI1', 74.5), ('WQ', 78.2), ('DADI2', 79.933), ('UI_CALL', 84.2), ('UI_LEFT', 85.7), ('CTA', 91.033)]
END=94.6667
