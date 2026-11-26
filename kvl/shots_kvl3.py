# Shots 35-51
def bun_kabab(e,s=1.0):
    bn=M('#D9963A',.6); pt=M('#6A3A1E',.7)
    oico((0,-.12,.05*s),.13*s,bn,e,sc=(1,1,.42),sub=2); ocyl((0,-.12,.1*s),.125*s,.04*s,pt,e,rot=(0,0,0),seg=14)
    ocyl((0,-.12,.128*s),.128*s,.012*s,M('#F2E2B0',.6),e,rot=(0,0,0),seg=14); oico((0,-.12,.17*s),.13*s,bn,e,sc=(1,1,.5),sub=2)
def stache(wa):
    u=wa['u']; return obox((0,-.632*u,.2*u),(.3*u,.008,.05*u),M('#FFFDF4',.5),.01,wa['head'])
BUNP=(.78,-.62,1.32)
def wal_hold(wa,l2,b2):
    for s,e in ((1,l2),(-1,b2)):
        if e is None: continue
        wa['arm'][s].rotation_euler=(R(-50),R(-s*6),R(s*8)); upright(e,wa,s)
def BUN():
    LF,KF,sh,gu,wa=decide_set(); FILLE[0]=45
    l2=in_hand(wa,1,lassi_big); b1=in_hand(gu,-1,bun_kabab); b2=in_hand(wa,-1,bun_kabab); b2.scale=(0,0,0); ch=chai(gu,1)
    def upd(t):
        wal_idle(wa,t); cap_idle(sh,t,SDP[0],SDP[1],90,hp(wa)); cap_idle(gu,t,GDP[0],GDP[1],-90,hp(wa)); crossed(sh); face(sh,mouth='frown',brow=-.02)
        wal_hold(wa,l2,None)
        tg=ws(211)+.15; a=tl(t,.15,.7); b=tl(t,tg-.25,tg); c=tl(t,tg,tg+.45); up=tl(t,ws(212)-.2,ws(213))
        hold_chai(gu,ch,s=1,a=-60-70*up,out=10)
        if t<tg:
            arm_to(gu,-1,BUNP,a,base=(R(-20),0,0)); upright(b1,gu,-1); b1.scale=(1,1,1); b2.scale=(0,0,0)
            arm_to(wa,-1,(BUNP[0]-.22,BUNP[1],BUNP[2]-.05),b,base=(0,0,0)); look_at(wa,BUNP,b)
        else:
            b1.scale=(0,0,0); b2.scale=(1,1,1); gu['arm'][-1].rotation_euler=(R(-20*(1-c)),0,0)
            arm_to(wa,-1,LV((BUNP[0]-.22,BUNP[1],BUNP[2]-.05),(.2,-.75,1.25),c),1.0,base=(0,0,0)); upright(b2,wa,-1); look_at(wa,LV(BUNP,hp(gu),c),1.0)
            face(wa,mouth='grin',brow=.04)
        face(gu,mouth='grin',brow=.03)
        fans(KF,t,'cheer' if t>tg else 'idle',look=hp(wa)); fans(LF,t,'glare',look=hp(gu))
        q=ease(t/DUR); camset(LV((1.6,-4.6,2.0),(1.25,-4.2,2.0),q),(.7,-.2,1.6),27,8)
    return dict(upd=upd)
SHOTS['BUN']=BUN
def TASTE():
    BOARD[0]=False
    LF,KF,sh,gu,wa=decide_set(skipL=(1,4,6,7,8),skipK=(1,4,6,7,8)); FILLE[0]=60
    l2=in_hand(wa,1,lassi_big); b2=in_hand(wa,-1,bun_kabab); mu=stache(wa); mu.scale=(0,0,0)
    def upd(t):
        wal_idle(wa,t); cap_idle(sh,t,SDP[0],SDP[1],90,hp(wa)); cap_idle(gu,t,GDP[0],GDP[1],-90,hp(wa))
        for H in (sh,gu): H['root'].rotation_euler[0]=R(8); face(H,mouth='o',brow=.04,eyes=1.12)
        s1=math.sin(pi*min(1,max(0,(t-.05)/.55))); s2=math.sin(pi*min(1,max(0,(t-.62)/.55)))
        wal_hold(wa,l2,b2); m=root_mat(wa); hh=1.0
        if s1>0: arm_to(wa,1,m@Vector((.14,-.62,1.9)),s1,base=tuple(wa['arm'][1].rotation_euler)); upright(l2,wa,1,tilt=-25*s1)
        if s2>0: arm_to(wa,-1,m@Vector((-.12,-.6,1.95)),s2,base=tuple(wa['arm'][-1].rotation_euler)); upright(b2,wa,-1)
        mu.scale=(1,1,1) if t>.45 else (0,0,0)
        blink(wa,t,force=1 if s1>.6 else None); face(wa,mouth='o' if s1>.3 or s2>.3 else 'smile',brow=.02)
        fans(LF,t,'freeze',look=hp(wa)); fans(KF,t,'freeze',look=hp(wa))
        q=ease(t/DUR); camset(LV((.25,-2.5,2.2),(.2,-2.2,2.2),q),(0,WP[1],2.05),34,8)
    return dict(upd=upd)
SHOTS['TASTE']=TASTE
def BREATH():
    LF,KF,sh,gu,wa=decide_set(); FILLE[0]=30
    l2=in_hand(wa,1,lassi_big); b2=in_hand(wa,-1,bun_kabab); mu=stache(wa)
    def upd(t):
        wal_idle(wa,t); wal_hold(wa,l2,b2); face(wa,mouth='flat',brow=.02); look_at(wa,(0,-5,2.3),1.0); wa['head'].rotation_euler[2]+=R(10*math.sin(t*1.6))
        k=tl(t,0,1.2)
        for H,x in ((sh,SDP[0]),(gu,GDP[0])):
            cap_idle(H,t,x,SDP[1],90 if x<0 else -90,hp(wa)); H['root'].rotation_euler[0]=R(12*k); face(H,mouth='flat',brow=.05,eyes=1.15)
            for s in (1,-1): H['arm'][s].rotation_euler=(R(-25*k),R(-s*6),0)
        fans(LF,t,'freeze',look=hp(wa),k=k); fans(KF,t,'freeze',look=hp(wa),k=k)
        q=ease(t/DUR); camset(LV((0,-9.0,5.4),(0,-7.3,4.4),q),(0,.4,1.9),24,8)
    return dict(upd=upd)
SHOTS['BREATH']=BREATH
def DONO():
    BOARD[0]=False
    LF,KF,sh,gu,wa=decide_set(skipL=(1,4,6,7,8),skipK=(1,4,6,7,8)); FILLE[0]=60
    l2=in_hand(wa,1,lassi_big); b2=in_hand(wa,-1,bun_kabab); mu=stache(wa)
    def upd(t):
        wal_idle(wa,t); up=tl(t,ws(222)-.2,ws(222)+.15)
        for s,e in ((1,l2),(-1,b2)): wa['arm'][s].rotation_euler=(R(-50-60*up),R(-s*(6+22*up)),R(s*8)); upright(e,wa,s)
        look_at(wa,(.3,-4,2.4),1.0); face(wa,mouth='grin' if t>ws(222) else 'smile',brow=.04); speak(wa,t,221,223,gesture=False)
        for H,x in ((sh,SDP[0]),(gu,GDP[0])): cap_idle(H,t,x,SDP[1],90 if x<0 else -90,hp(wa)); H['root'].rotation_euler[0]=R(10); face(H,mouth='flat',brow=.05,eyes=1.15)
        fans(LF,t,'freeze',look=hp(wa)); fans(KF,t,'freeze',look=hp(wa))
        q=ease(t/DUR); camset(LV((.3,-2.75,2.25),(.25,-2.45,2.25),q),(0,WP[1],2.05),33,8)
    return dict(upd=upd)
SHOTS['DONO']=DONO
def DONO2():
    LF,KF,sh,gu,wa=decide_set(); FILLE[0]=20
    l2=in_hand(wa,1,lassi_big); b2=in_hand(wa,-1,bun_kabab); mu=stache(wa)
    def upd(t):
        wal_idle(wa,t); wal_hold(wa,l2,b2); face(wa,mouth='o',brow=.05,eyes=1.1); wa['root'].rotation_euler[0]=R(-4)
        k=tl(t,0,.18)
        for H,x in ((sh,SDP[0]),(gu,GDP[0])):
            cap_idle(H,t,x,SDP[1],90 if x<0 else -90,hp(wa)); shock(H,k); face(H,mouth='shout',brow=.06,eyes=1.2); H['root'].rotation_euler[0]=R(-6*k)
        fans(LF,t,'gasp',look=hp(wa),k=k); fans(KF,t,'gasp',look=hp(wa),k=k)
        for H in LF+KF: face(H,mouth='shout',brow=.06,eyes=1.2)
        q=ease(t/DUR); camset(LV((0,-10.8,4.6),(0,-10.0,4.3),q),(0,1.4,2.0),21,8)
    return dict(upd=upd)
SHOTS['DONO2']=DONO2
def TURNED():
    LF,KF,sh,gu,wa=decide_set(); FILLE[0]=40
    l2=in_hand(wa,1,lassi_big); b2=in_hand(wa,-1,bun_kabab); mu=stache(wa)
    def upd(t):
        wal_idle(wa,t); wal_hold(wa,l2,b2); k=tl(t,.05,.5)
        wa['root'].location[2]=wa['z0']+.008-.05*k; face(wa,mouth='o',brow=.06,eyes=1.15); look_at(wa,LV((0,-4,2.3),hp(sh),tl(t,.6,.9)*(1-tl(t,1.0,1.3)))if t<1.0 else hp(gu),1.0)
        for H,x in ((sh,SDP[0]),(gu,GDP[0])):
            cap_idle(H,t,x,SDP[1],90 if x<0 else -90,hp(wa)); H['root'].rotation_euler[0]=R(10*k)
            H['arm'][1].rotation_euler=(R(-150*k+10*math.sin(t*9+H['seed'])),R(-10*k),0); H['arm'][-1].rotation_euler=(R(-70*k),R(12*k),0)
            face(H,mouth='shout' if k>.5 else 'frown',brow=-.04,brow_r=-16*k)
        fans(LF,t,'fist',look=hp(wa),k=k); fans(KF,t,'fist',look=hp(wa),k=k)
        q=ease(t/DUR); camset(LV((0,-3.9,1.2),(0,-3.6,1.15),q),(0,.0,2.25),21,8)
    return dict(upd=upd)
SHOTS['TURNED']=TURNED
# ---------------------------------------------------------------- Islamabad
ISBP=(0.0,-5.3)
def isb_set(skipL=(),skipK=()):
    LF,KF,sh,gu,wa=decide_set(skipL=skipL,skipK=skipK); l2=in_hand(wa,1,lassi_big); b2=in_hand(wa,-1,bun_kabab); mu=stache(wa)
    ib=mk(ISB,ISBP[0],ISBP[1],180,'isb'); cf=in_hand(ib,1,lambda e: big_cup(e,1.5)); return LF,KF,sh,gu,wa,l2,b2,ib,cf
def isb_pose(ib,cf,t,sip=0.0,x=ISBP[0],y=ISBP[1]):
    place(ib,x,y,180); hstand(ib,t); hold_chai(ib,cf,s=1,a=-48,sip=sip); face(ib,mouth='smile',brow=.0)
def VOICE():
    LF,KF,sh,gu,wa,l2,b2,ib,cf=isb_set(); FILLE[0]=30
    def upd(t):
        wal_idle(wa,t); wal_hold(wa,l2,b2); k=tl(t,.25,.8)
        d=min(1,t/(DUR*.95)); y=L(-10.8,ISBP[1],ease_out(d)); isb_pose(ib,cf,t,x=0,y=y); walk(ib,(y+10.8),step=.42,arm=0); hold_chai(ib,cf,s=1,a=-48)
        ib['arm'][-1].rotation_euler=(R(10*math.sin(t*3)),R(6),0)
        for H in (sh,gu,wa):
            if H is not wa: cap_idle(H,t,H['root'].location[0],SDP[1],90 if H is sh else -90)
            look_at(H,LV(hp(wa) if H is not wa else (0,-5,2.3),hp(ib),k),1.0,maxyaw=95); face(H,mouth='o' if k>.5 else 'shout',brow=.04)
        fans(LF,t,'freeze',look=hp(ib),k=k); fans(KF,t,'freeze',look=hp(ib),k=k)
        q=ease(t/DUR); camset(LV((0,4.6,3.1),(0,4.0,3.0),q),(0,-6.0,1.7),26,8)
    return dict(upd=upd)
SHOTS['VOICE']=VOICE
def ISBS():
    LF,KF,sh,gu,wa,l2,b2,ib,cf=isb_set(); FILLE[0]=55
    def upd(t):
        wal_idle(wa,t); wal_hold(wa,l2,b2); look_at(wa,hp(ib),1.0)
        for H in (sh,gu): cap_idle(H,t,H['root'].location[0],SDP[1],90 if H is sh else -90,hp(ib)); face(H,mouth='o',brow=.04)
        sp=math.sin(pi*min(1,max(0,(t-ws(240)+.2)/.9))) if t>ws(240)-.2 else 0
        isb_pose(ib,cf,t,sip=sp*.9); g=tl(t,ws(236)-.1,ws(237))*(1-tl(t,ws(238),ws(238)+.3))
        ib['arm'][-1].rotation_euler=(R(-58*g),R(14*g),R(-10*g*math.sin(t*5))) if g>0 else (R(-8),R(6),0)
        look_at(ib,(1.0,-2.5,2.35),1.0); face(ib,mouth='smile',brow=.02); speak(ib,t,236,244,gesture=False)
        fans(LF,t,'freeze',look=hp(ib)); fans(KF,t,'freeze',look=hp(ib))
        q=ease(t/DUR); camset(LV((.95,-2.75,2.3),(.85,-3.05,2.3),q),(0,ISBP[1],2.2),30,8)
    return dict(upd=upd)
SHOTS['ISB']=ISBS
def SILENCE():
    LF,KF,sh,gu,wa,l2,b2,ib,cf=isb_set(); FILLE[0]=30
    for H in LF+KF: H['rz0']=H['home'][2]; H['rz1']=face_dir(ISBP[0]-H['home'][0],ISBP[1]-H['home'][1])
    def upd(t):
        wal_idle(wa,t); wal_hold(wa,l2,b2); look_at(wa,hp(ib),1.0); face(wa,mouth='flat')
        isb_pose(ib,cf,t,sip=0); k=ease(min(1,max(0,(t-ws(246)+.1)/2.0)))
        for H,x in ((sh,SDP[0]),(gu,GDP[0])):
            rz=L(90 if x<0 else -90,face_dir(ISBP[0]-x,ISBP[1]-SDP[1]),k); cap_idle(H,t,x,SDP[1],rz,hp(ib)); face(H,mouth='frown',brow=-.03*k,brow_r=-15*k)
        for H in LF+KF:
            fan(H,t,'glare',look=hp(ib),k=k); H['root'].rotation_euler[2]=R(L(H['rz0'],H['rz1'],k)); look_at(H,hp(ib),1.0)
        q=ease(t/DUR); camset(LV((1.0,-8.2,2.6),(.85,-7.3,2.5),q),(0,-.6,2.0),24,8)
    return dict(upd=upd)
SHOTS['SILENCE']=SILENCE
def roast_isb(who,a,b,cam_yaw):
    def f():
        BOARD[0]=False
        LF,KF,sh,gu,wa,l2,b2,ib,cf=isb_set(); FILLE[0]=55; me=gu if who=='K' else sh; ot=sh if who=='K' else gu
        def upd(t):
            wal_idle(wa,t); wal_hold(wa,l2,b2); look_at(wa,hp(me),1.0); face(wa,mouth='smile')
            isb_pose(ib,cf,t); look_at(ib,hp(me),1.0); face(ib,mouth='o' if t>ws(b)-.3 else 'smile',brow=.04)
            for H in (sh,gu):
                x=H['root'].location[0]; cap_idle(H,t,x,SDP[1],face_dir(ISBP[0]-x,ISBP[1]-SDP[1]),hp(ib)); face(H,mouth='smirk',brow=-.01)
            p=tl(t,ws(a)-.15,ws(a)+.15); arm_to(me,1,hp(ib),p,base=(0,0,0)); speak(me,t,a,b,gesture=False); face(me,mouth='smirk',brow=.03,brow_r=6) if not (ws(a)<=t<we(b)) else None
            lg=t>ws(b)-.25
            fans(LF,t,'laugh' if lg else 'glare',look=hp(ib)); fans(KF,t,'laugh' if lg else 'glare',look=hp(ib))
            if lg: laugh(ot,t)
            c,tg,ln=single(me,yaw=cam_yaw,dist=3.1,lens=30); q=ease(t/DUR); camset(LV(c,(c[0],c[1]+.25,c[2]),q),tg,ln,8)
        return dict(upd=upd)
    return f
SHOTS['NAU']=roast_isb('K',253,259,24); SHOTS['PAHAAD']=roast_isb('L',260,266,-24)
def confetti(center,t0,n=110,seed=4,area=(4.5,3.2),top=6.5):
    r=random.Random(seed); P=[]; cols=['#1F7A44','#E6B53A','#2466C9','#F4F6FA','#6FC3EA','#E8554D','#F2C14E']
    for i in range(n):
        o=obox((0,0,-90),(.06,.01,.04),M(r.choice(cols),.5),0); P.append((o,r.uniform(-area[0],area[0]),r.uniform(-area[1],area[1]),r.uniform(0,.5),r.uniform(.6,1.1),r.uniform(0,6.28),r.uniform(0,2.5)))
    def upd(t):
        d=t-t0
        for o,x,y,dt,v,ph,z0 in P:
            if d<dt: o.location=(0,0,-90); continue
            q=d-dt; z=max(.03,top+z0-q*v*1.7)
            o.location=(center[0]+x+.25*math.sin(q*2.3+ph),center[1]+y,z); o.rotation_euler=(q*5+ph,q*3.6,ph)
    return upd
HFP=(-.72,.72,-.55); WBK=(0,1.45)
def HIGHFIVE():
    LF,KF,sh,gu,wa,l2,b2,ib,cf=isb_set(); FILLE[0]=40; th=ws(277)-.05; cu=confetti((0,1.0),th)
    def upd(t):
        k=ease(min(1,max(0,t/.9)))
        place(wa,0,L(WP[1],WBK[1],k),0); walk(wa,k*1.65,step=.36,arm=0) if 0<k<1 else hstand(wa,t); blink(wa,t); wal_hold(wa,l2,b2); face(wa,mouth='grin' if t>th else 'o',brow=.04)
        look_at(wa,(0,HFP[2],2.6),1.0)
        isb_pose(ib,cf,t); face(ib,mouth='frown' if t>th else 'o',brow=.03); look_at(ib,(0,HFP[2],2.6),1.0)
        m=tl(t,.35,1.3)
        for H,x0,x1,r1,s_ in ((sh,SDP[0],HFP[0],70,-1),(gu,GDP[0],HFP[1],-70,1)):
            x=L(x0,x1,m); y=L(SDP[1],HFP[2],m); cap_idle(H,t,x,y,L(face_dir(ISBP[0]-x0,ISBP[1]-SDP[1]),r1,tl(t,.2,1.0))); walk(H,abs(x-x0)+abs(y-SDP[1]),step=.4,arm=10) if 0<m<1 else None
            up=tl(t,th-.55,th-.05)
            arm_to(H,1 if H is gu else -1,(0,HFP[2]-.02,2.62+(.04 if t>th else 0)),up,base=(0,0,0))
            face(H,mouth='grin',brow=.04); look_at(H,(0,HFP[2],2.6),1.0)
        cu(t)
        fans(LF,t,'cheer' if t>th else 'smile',look=(0,HFP[2],2.6)); fans(KF,t,'cheer' if t>th else 'smile',look=(0,HFP[2],2.6))
        q=ease(t/DUR); camset(LV((-.9,-4.4,1.55),(-.7,-3.9,1.6),q),(0,HFP[2]+.3,2.4),23,8)
    return dict(upd=upd)
SHOTS['HIGHFIVE']=HIGHFIVE
def OVER():
    arena('kv_night',night=1.0); LF=mkfans('L'); KF=mkfans('K'); sh,gu=captains(); wa=mk(WALEED,0,1.2,0,'wa'); l2=in_hand(wa,1,lassi_big); FILLE[0]=60
    FW=[firework((-6,4,15),.1,'#3FC77A',seed=1),firework((5,6,16.5),.55,'#6FC3EA',seed=2),firework((0,9,18),1.1,'#FFE08A',seed=3),firework((-3,12,15.5),1.6,'#F4F6FA',seed=4),firework((7,10,15),2.05,'#3FC77A',seed=5)]
    def upd(t):
        fans(LF,t,'dance'); fans(KF,t,'dance')
        for H,x,r in ((sh,-1.4,70),(gu,1.4,-70)):
            place(H,x,-.4,r); b=math.sin(t*7+H['seed']); H['root'].location[2]=H['z0']+.008+.1*abs(b); blink(H,t)
            for s in (1,-1): H['arm'][s].rotation_euler=(R(-150+22*b*s),R(-s*32),0)
            H['leg'][1].rotation_euler[0]=R(-26*max(0,b)); H['leg'][-1].rotation_euler[0]=R(-26*max(0,-b)); face(H,mouth='grin',brow=.05)
        place(wa,0,1.2,0); hstand(wa,t); hold_chai(wa,l2,s=1,a=-55,sip=.5+.5*math.sin(t*2)); face(wa,mouth='smile')
        for f in FW: f(t)
        q=ease(t/DUR); camset(LV((0,-11.5,4.6),(0,-10.4,4.3),q),(0,1.5,3.2),21,8)
    return dict(upd=upd)
SHOTS['OVER']=OVER
# ---------------------------------------------------------------- morning
CC=(0.0,.7)
def morning_set(tables=True):
    arena('kv_morn',tokens=False,stand=True); r=random.Random(9)
    for i in range(26):
        x=r.uniform(-9,9); y=r.uniform(-3,10)
        if abs(x)<2.6 and -2.5<y<3: continue
        B.box((x,y,.02),(.09,.13,.02),M(r.choice(['#F4F1EA','#E8554D','#F2C14E','#6FC3EA']),.7),0,rot=(0,0,r.uniform(0,3)))
    for i in range(7): x=r.uniform(-8,8); B.cyl((x,r.uniform(4,9),.06),.06,.12,M('#F4F1EA',.5),seg=8)
    B.done('litter')
    chai_counter(CC[0],CC[1],0); cw=mk(CHAIWALA,CC[0],CC[1]+1.05,0,'chaiwala')
    return cw
def MORNING():
    cw=morning_set(); sh=mk(SHEEDA,-1.6,-.5,60,'sheeda'); gu=mk(GUDDU,1.6,-.5,-60,'guddu'); c1=chai(sh,1); c2=chai(gu,-1); FILLE[0]=40
    def upd(t):
        place(cw,CC[0],CC[1]+1.05,0); hstand(cw,t); face(cw,mouth='flat',brow=.03); look_at(cw,LV(hp(sh),hp(gu),.5+.5*math.sin(t*3)),1.0)
        for H,x,r,s,cp in ((sh,-1.6,60,1,c1),(gu,1.6,-60,-1,c2)):
            cap_idle(H,t,x,-.5,r,hp(gu if H is sh else sh)); hold_chai(H,cp,s=s,a=-62+8*math.sin(t*6+H['seed']))
            ot=gu if H is sh else sh; g=math.sin(t*9+H['seed']); arm_to(H,-s,LV(hp(ot,-.6),hp(ot,-.3),.5+.5*g),1.0,base=(0,0,0))
            face(H,mouth='shout' if int(t*5+H['seed'])%2 else 'O',brow=-.03,brow_r=-12); H['root'].rotation_euler[0]=R(5)
        q=ease(t/DUR); camset(LV((0,-5.6,2.25),(0,-5.0,2.2),q),(0,.2,1.95),24,8)
    return dict(upd=upd)
SHOTS['MORNING']=MORNING
WT=(-.55,-1.55); WAP=(-.55,-.05)
def eat_set():
    cw=morning_set(); nt=nashta_table(WT[0],WT[1],0); dg=degh(1.95,-1.4,0); wa=mk(WALEED,WAP[0],WAP[1],0,'wa')
    sh=mk(SHEEDA,-1.6,6.0,60,'sheeda'); gu=mk(GUDDU,1.6,6.0,-60,'guddu'); c1=chai(sh,1); c2=chai(gu,-1)
    pu=in_hand(wa,-1,lambda e: [ocyl((0,-.12,.06),.17,.02,M('#E8B85A',.6),e,rot=(R(70),0,0),seg=14)]); bp=in_hand(wa,1,lambda e: biryani_plate(e,(0,-.08,.02)))
    return cw,nt,dg,wa,sh,gu,c1,c2,pu,bp
def eat_bg(cw,sh,gu,c1,c2,t):
    place(cw,CC[0],CC[1]+1.05,0); hstand(cw,t)
    for H,x,r,s,cp in ((sh,-1.6,60,1,c1),(gu,1.6,-60,-1,c2)):
        cap_idle(H,t,x,6.0,r,hp(gu if H is sh else sh)); hold_chai(H,cp,s=s,a=-62); H['arm'][-s].rotation_euler=(R(-95+12*math.sin(t*9+H['seed'])),0,0)
        face(H,mouth='shout' if int(t*5+H['seed'])%2 else 'O',brow=-.03,brow_r=-12)
def ATE():
    cw,nt,dg,wa,sh,gu,c1,c2,pu,bp=eat_set(); mu=stache(wa); FILLE[0]=45
    def upd(t):
        eat_bg(cw,sh,gu,c1,c2,t)
        wal_idle(wa,t,WAP[0],WAP[1],0); m=root_mat(wa)
        e1=math.sin(pi*min(1,max(0,(t-.2)/.7))); e2=math.sin(pi*min(1,max(0,(t-1.15)/.7)))
        for s,e,ee in ((-1,pu,e1),(1,bp,e2)):
            wa['arm'][s].rotation_euler=(R(-55),R(-s*8),R(s*6)); arm_to(wa,s,m@Vector((s*-.13,-.6,1.92)),ee,base=(R(-55),R(-s*8),R(s*6))) if ee>0 else None; upright(e,wa,s)
        face(wa,mouth='o' if (e1>.5 or e2>.5) else 'smile',brow=.02); blink(wa,t,force=1 if (e1>.7 or e2>.7) else None); look_at(wa,(0,-4,2),1.0)
        q=ease(t/DUR); camset(LV((-.15,-4.9,2.35),(-.25,-4.4,2.3),q),(-.4,.4,1.75),24,8)
    return dict(upd=upd)
SHOTS['ATE']=ATE
def KHA():
    BOARD[0]=False
    cw,nt,dg,wa,sh,gu,c1,c2,pu,bp=eat_set(); mu=stache(wa); FILLE[0]=60
    def upd(t):
        eat_bg(cw,sh,gu,c1,c2,t)
        wal_idle(wa,t,WAP[0],WAP[1],0); up=tl(t,.1,.4)
        for s,e in ((-1,pu),(1,bp)): wa['arm'][s].rotation_euler=(R(-55-35*up),R(-s*(8+16*up)),R(s*6)); upright(e,wa,s)
        look_at(wa,(-.2,-3,2.4),1.0); face(wa,mouth='grin',brow=.04); speak(wa,t,298,302,gesture=False)
        wk=tl(t,we(302)-.25,we(302)-.1)*(1-tl(t,we(302)+.25,we(302)+.4))
        if wk>0: wa['lids'][0].scale=(wk,wk,wk); face(wa,mouth='smirk')
        q=ease(t/DUR); camset(LV((-.25,-2.6,2.45),(-.3,-2.3,2.42),q),(-.55,WAP[1],2.2),33,8)
    return dict(upd=upd)
SHOTS['KHA']=KHA
def CTA():
    arena('kv_day'); LF=mkfans('L',focus=(0,-1.6)); KF=mkfans('K',focus=(0,-1.6)); sh,gu=captains(); wa=mk(WALEED,0,-1.6,0,'wa'); FILLE[0]=40
    def upd(t):
        wal_idle(wa,t,0,-1.6,0); look_at(wa,(0,-8,2.3),1.0); face(wa,mouth='grin',brow=.03)
        a=tl(t,ws(304)-.15,ws(304)+.1)*(1-tl(t,ws(305),ws(305)+.2)); b=tl(t,ws(306)-.15,ws(306)+.1)*(1-tl(t,ws(307),ws(307)+.2)); c=tl(t,ws(307)-.1,ws(307)+.2)
        arm_to(wa,-1,(5,-1.6,2.3),a,base=(0,0,0)) if a>0 else None; arm_to(wa,1,(-5,-1.6,2.3),b,base=(0,0,0)) if b>0 else None
        if c>0: arm_to(wa,1,(0,-9,2.3),c,base=(0,0,0))
        look_at(wa,(5,-3,2.3) if a>.5 else ((-5,-3,2.3) if b>.5 else (0,-8,2.3)),1.0)
        fans(LF,t,'cheer' if b>.3 or c>0 else 'smile',look=hp(wa)); fans(KF,t,'cheer' if a>.3 or c>0 else 'smile',look=hp(wa))
        cap_idle(sh,t,-SX,CY,SRZ,hp(wa)); cap_idle(gu,t,SX,CY,-SRZ,hp(wa)); crossed(sh); crossed(gu); face(sh,mouth='smirk'); face(gu,mouth='smirk')
        if b>.3: sh['arm'][1].rotation_euler=(R(-160),R(-10),0); face(sh,mouth='grin')
        if a>.3: gu['arm'][1].rotation_euler=(R(-160),R(-10),0); face(gu,mouth='grin')
        q=ease(min(1,t/(DUR-.3))); camset(LV((0,-6.2,2.2),(0,-13.5,6.4),q),LV((0,-1.2,2.0),(0,2.0,2.4),q),22,8)
    return dict(upd=upd)
SHOTS['CTA']=CTA
