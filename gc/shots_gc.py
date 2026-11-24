# Shots for "Gali Cricket Ke Qanoon". Cuts sit on narration words (audio/words.json); SEQ is written by gen_seq.py.
SHOTS={}
END=61.4
SEQ=[('OPEN', 0.0), ('MOIZ', 5.3), ('B1', 8.833), ('M1', 11.2), ('B2', 12.433), ('M2', 14.7), ('B3', 17.067), ('M3', 19.2), ('CH', 21.033), ('BOOM', 23.9), ('M4', 25.967), ('PLEAD', 29.467), ('SIX', 33.5), ('GATE', 38.433), ('M5', 43.067), ('KNOCK', 46.967), ('R1', 49.067), ('BAT', 50.133), ('ENDW', 53.967), ('CTA', 58.2)]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0
def we(i): return W_[i]['e']-T0
def fwd(rz): return (math.sin(R(rz)),-math.cos(R(rz)))
def drift(c0,tg,t,a=.06): q=ease(t/DUR); return LV(c0,(L(c0[0],tg[0],a),L(c0[1],tg[1],a),c0[2]),q)
def closecam(H,rz,side=.3,dist=3.0,dz=.05,tz=-.3,lens=36,bias=0.0,bx=0.0):
    h=hp(H); f=fwd(rz); f=(f[0]+bx,f[1]-bias); n_=math.hypot(*f); f=(f[0]/n_,f[1]/n_); rt=(-f[1],f[0])
    return (h[0]+f[0]*dist+rt[0]*side,h[1]+f[1]*dist+rt[1]*side,h[2]+dz),(h[0],h[1],h[2]+tz),lens
def arc(p0,p1,f,h): return Vector((L(p0[0],p1[0],f),L(p0[1],p1[1],f),L(p0[2],p1[2],f)+4*h*f*(1-f)))
# ---------------------------------------------------------------- positions
CREASE=(.62,-.36); KEEP=(-1.7,.1)
FIELD={'b1':(4.6,2.15),'b2':(2.9,-2.35),'b3':(12.0,2.5),'b4':KEEP}
RUN0=13.6; REL_X=9.3; LANE=.35
CAST={'b1':BOY1,'b2':BOY2,'b3':BOY3,'b4':BOY4}
def pset(bat_on=True):
    G=gali_k(); S={}
    S['leaves']=G['leaves']
    S['wk']=wicket()
    S['mo']=mk(MOIZ,CREASE[0],CREASE[1],90,'mo'); S['wa']=mk(WALEED,RUN0,LANE,-90,'wa')
    S['F']={k:mk(CAST[k],x,y,face_dir(CREASE[0]-x,CREASE[1]-y),k) for k,(x,y) in FIELD.items()}
    S['ball']=ball_obj()
    S['batp']=empty((0,0,0),S['mo']['root']); S['bat']=bat_obj(S['batp']); S['batp'].location=(.22,-.42,1.28)
    if not bat_on: S['batp'].scale=(0,0,0)
    return S
def bat_angle(S,a,yaw=0.0):
    S['batp'].rotation_euler=(R(a),0,R(yaw))
def bat_hands(S,k=1.0):
    mo=S['mo']; p=S['batp'].matrix_world.translation
    for s in (1,-1): arm_to(mo,s,p+Vector((0,0,.02*s)),k)
def bat_tip(S,frac=.75):
    return S['batp'].matrix_world@Vector((0,0,-.36-.95*frac))*1.0
def fidle(S,t,look=None):
    for k,H in S['F'].items():
        x,y=FIELD[k]; H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(face_dir(CREASE[0]-x,CREASE[1]-y)))
        stand(H,t+dseed(k)); blink(H,t); H['head'].rotation_euler=(0,0,0)
        if k=='b4': H['root'].rotation_euler[0]=R(16); H['arm'][1].rotation_euler=(R(-60),0,R(20)); H['arm'][-1].rotation_euler=(R(-60),0,R(-20))
        else: H['arm'][1].rotation_euler=(R(-25),0,R(12)); H['arm'][-1].rotation_euler=(R(-25),0,R(-12))
        if look is not None: look_at(H,look,.7,maxyaw=85,maxpitch=45)
def mstance(S,t,a=28):
    mo=S['mo']; mo['root'].location=(CREASE[0],CREASE[1],0); mo['root'].rotation_euler=(R(8),0,R(90)); stand(mo,t); blink(mo,t); bat_angle(S,a); bat_hands(S)
def bowl(S,t,t_rel,v=4.2,label=True):
    """Waleed's run-up and windmill action; returns ball world pos while held (None after release)"""
    wa=S['wa']; t_run=(RUN0-REL_X)/v; t0=t_rel-t_run
    if t<t_rel:
        x=RUN0-max(0,t-t0)*v; wa['root'].location=(x,LANE,0); wa['root'].rotation_euler=(R(12 if t>t0 else 0),0,R(-90))
        if t>t0: walk(wa,(t-t0)*v*.6+wa['seed'],step=.9,arm=40)
        else: stand(wa,t)
        k=tl(t,t_rel-.35,t_rel); wa['arm'][1].rotation_euler=(R(-10-330*k),0,R(4))
        if k>0: wa['arm'][-1].rotation_euler=(R(-80*k),0,R(-20))
    else:
        f=tl(t,t_rel,t_rel+.5); x=REL_X-1.2*ease_out(f); wa['root'].location=(x,LANE,0); wa['root'].rotation_euler=(R(18*(1-f)+4),0,R(-90)); stand(wa,t)
        wa['arm'][1].rotation_euler=(R(-340-60*f),0,R(4)); wa['arm'][-1].rotation_euler=(R(-50*(1-f)),0,R(-20))
    blink(wa,t); face(wa,mouth='strain' if abs(t-t_rel)<.4 else 'flat',brow=.05)
    if t<t_rel: return wa['arm'][1].matrix_world@Vector(hand_loc(wa,1))
    return None
def ball_to_wicket(S,t,t_rel,dur=.55):
    """release -> bounce -> wicket; returns impact time"""
    p0=Vector((REL_X-.25,LANE+.1,2.55)); pb=Vector((2.6,.15,.07)); pw=Vector((.02,0,.5))
    d1=dur*.62; d2=dur*.38
    if t<t_rel+d1: f=(t-t_rel)/d1; p=p0.lerp(pb,f); p.z=L(p0.z,pb.z,f)+.4*f*(1-f)
    else: f=min(1,(t-t_rel-d1)/d2); p=arc(pb,pw,f,.28)
    return p,t_rel+dur
SHOW_LABEL=True
# ================================================================ shots
def OPEN_():
    S=pset(); b=S['ball']
    def upd(t):
        fidle(S,t); mstance(S,t); face(S['mo'],mouth='smirk',brow=.03)
        wa=S['wa']; x=L(10.5,RUN0,ease(tl(t,.3,2.2))); wa['root'].location=(x,LANE,0); wa['root'].rotation_euler=(0,0,R(90 if t<2.3 else -90))
        if .3<t<2.2: walk(wa,(x-10.5)+wa['seed'],step=.5,arm=20)
        else: stand(wa,t)
        blink(wa,t); b.location=wa['arm'][1].matrix_world@Vector(hand_loc(wa,1))
        q=ease(t/DUR); camset(LV((8.5,-1.2,8.5),(6.4,-1.5,2.7),q),LV((3.5,0,1.0),(1.6,0,1.25),q),L(19,22,q),8)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def MOIZ_():
    S=pset(); b=S['ball']; mo=S['mo']; T=dict(SEQ)['MOIZ']
    bubble('MOIZ',(CREASE[0]+.25,CREASE[1]-.45,3.15),W_[16]['s']-T,size=.2,col='#FFFFFF',bg='#1E8A4A',dur=W_[21]['s']-W_[16]['s'])
    bubble('QANOON: MOIZ KE',(CREASE[0]+.25,CREASE[1]-.45,3.15),W_[21]['s']-T,size=.13,col='#FFFFFF',bg='#C8372D')
    def upd(t):
        fidle(S,t,look=hp(mo)); mo['root'].location=(CREASE[0],CREASE[1],0); mo['root'].rotation_euler=(0,0,R(30)); stand(mo,t); blink(mo,t)
        face(mo,mouth='smirk',brow=.04)
        hand=mo['arm'][1].matrix_world@Vector(hand_loc(mo,1)); toss=abs(math.sin(t*3.0))*.55
        mo['arm'][1].rotation_euler=(R(-95),R(-10),R(10)); b.location=Vector(hand)+Vector((0,0,.08+toss))
        bat_angle(S,0,0); S['batp'].location=(-.35,-.15,1.1); arm_to(mo,-1,S['batp'].matrix_world.translation,1); S['batp'].rotation_euler=(R(-10),R(-20),0)
        c0,tg,ln=closecam(mo,30,.2,3.0,lens=34); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['MOIZ']=MOIZ_
SIDE=((4.6,-6.4,2.2),(4.6,0,1.2),22)
def BALLW(power=1.0,cam='side',seed=1,slow=1.0,t_rel=None):
    def S_():
        S=pset(); b=S['ball']; tr=t_rel if t_rel is not None else .95
        def upd(t):
            fidle(S,t); mstance(S,t); tt=t*slow
            p=bowl(S,tt,tr)
            if p is not None: b.location=p
            else:
                bp,t_hit=ball_to_wicket(S,tt,tr)
                if tt<t_hit: b.location=bp
                else: f=tt-t_hit; b.location=(-.4-1.5*f,.1,max(.07,.5+1.0*f-4.9*f*f))
                bricks_fall(S['wk'],tt,t_hit,power,seed)
                mo=S['mo']
                if tt>t_hit-.25: bat_angle(S,L(28,-40,tl(tt,t_hit-.25,t_hit))); bat_hands(S)
                if tt>t_hit: face(mo,mouth='o',brow=.06,eyes=1.2); look_at(mo,(0,0,.3),.8*tl(tt,t_hit,t_hit+.2),maxyaw=100,maxpitch=45)
                for k,H in S['F'].items():
                    if tt>t_hit+.1 and k!='b4': H['arm'][1].rotation_euler=(R(-10),0,R(150)); H['arm'][-1].rotation_euler=(R(-10),0,R(-150)); face(H,mouth='shout')
            if cam=='side': q=ease(t/DUR); camset(LV((15.6,-1.6,3.7),(15.0,-1.4,3.5),q),(1.5,.1,.8),30,8)
            elif cam=='front': q=ease(t/DUR); camset(LV((-3.2,2.5,1.3),(-2.9,2.4,1.3),q),(2.6,-.3,.9),22,4)
            elif cam=='slowwa':
                wa=S['wa']; h=hp(wa); camset((h[0]-3.0,h[1]-1.6,h[2]-.2),(h[0],h[1],h[2]-.5),30,4)
            elif cam=='boom': camset((-2.8,-2.6,.8),(0,0,.5),24,4)
        return dict(upd=upd)
    return S_
SHOTS['B1']=BALLW(1.0,'side',1)
def mtalk(a,b_,extra=None,rest_='flat',fallen=None,cam=None,rz=60):
    def S_():
        S=pset(); mo=S['mo']; b=S['ball']; b.location=(0,0,-5)
        def upd(t):
            fidle(S,t,look=hp(mo)); mo['root'].location=(CREASE[0],CREASE[1],0); mo['root'].rotation_euler=(0,0,R(rz)); stand(mo,t); blink(mo,t)
            bat_angle(S,15,0); S['batp'].location=(.32,-.25,1.12); arm_to(mo,1,S['batp'].matrix_world.translation,1); mo['arm'][-1].rotation_euler=(R(-5),0,R(-8))
            talk(mo,t,*wt(a,b_),rest=rest_); face(mo,brow=.04)
            if fallen: bricks_fall(S['wk'],10,0,*fallen)
            if extra: extra(S,t)
            c0,tg,ln=cam if cam else closecam(mo,rz,.25,3.1,lens=34); camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
def _m1(S,t):
    mo=S['mo']; k=tl(t,0,.3)
    for s in (1,-1): mo['arm'][s].rotation_euler=(R(-40*k),0,R(s*70*k))
    S['batp'].location=(.5,-.6,0.0); S['batp'].rotation_euler=(R(80),0,R(20))
def _m2(S,t):
    mo=S['mo']; k=tl(t,0,.25); mo['arm'][-1].rotation_euler=(R(-170*k),0,R(-10)); look_at(mo,(WIRE_X,0,WIRE_Z),.5*k,maxpitch=40)
    face(mo,brow=.05)
def _m3(S,t):
    mo=S['mo']; k=tl(t,0,.25)
    for s in (1,-1): mo['arm'][s].rotation_euler=(R(-75*k),0,R(s*25*k))
    S['batp'].location=(.5,-.6,0.0); S['batp'].rotation_euler=(R(80),0,R(20)); face(mo,brow=.03,brow_r=10)
SHOTS['M1']=mtalk(26,28,_m1,rest_='smirk',fallen=(1.0,1))
def B2_():
    S=pset(); b=S['ball']; tr=.95; b1=S['F']['b1']
    def upd(t):
        fidle(S,t); mstance(S,t); mo=S['mo']
        p=bowl(S,t,tr)
        t_hit=tr+.5; catch=t_hit+1.15; hand=Vector(hp(b1))+Vector((0,0,.45))
        if p is not None: b.location=p
        elif t<t_hit:
            f=(t-tr)/.5; p0=Vector((REL_X-.25,LANE+.1,2.55)); pb=Vector((3.0,.1,.07)); pc=Vector((1.25,-.3,.95))
            b.location=p0.lerp(pb,min(1,f/.65)) if f<.65 else arc(pb,pc,(f-.65)/.35,.2)
        elif t<catch: b.location=arc(Vector((1.25,-.3,.95)),hand,(t-t_hit)/(catch-t_hit),4.6)
        else: b.location=hand
        if t>t_hit-.3: bat_angle(S,L(28,-115,ease_out(tl(t,t_hit-.3,t_hit+.15)))); bat_hands(S)
        if t>t_hit: look_at(mo,b.location,.8,maxpitch=60,maxyaw=100)
        k=tl(t,catch-.6,catch); b1['arm'][1].rotation_euler=(R(-160*k),0,R(10)); b1['arm'][-1].rotation_euler=(R(-160*k),0,R(-10)); look_at(b1,b.location,.8*tl(t,t_hit,t_hit+.3),maxpitch=70)
        if t>catch:
            j=max(0,math.sin((t-catch)*9))*.25; b1['root'].location[2]=j; face(b1,mouth='shout',eyes=1.15)
            for k_ in ('b2','b3','b4'): H=S['F'][k_]; H['arm'][1].rotation_euler=(R(-10),0,R(150)); H['arm'][-1].rotation_euler=(R(-10),0,R(-150)); face(H,mouth='shout')
            face(mo,mouth='O',brow=.06,eyes=1.2)
        q=ease(t/DUR); camset(LV((8.0,-1.8,1.6),(7.6,-1.7,1.8),q),LV((2.0,0,1.2),(3.8,1.4,2.2),q),18,5.6)
    return dict(upd=upd)
SHOTS['B2']=B2_
SHOTS['M2']=mtalk(29,35,_m2,rest_='smirk',cam=((1.8,-3.0,1.1),(.6,-.36,2.2),26))
SHOTS['B3']=BALLW(1.1,'front',3)
SHOTS['M3']=mtalk(36,39,_m3,fallen=(1.1,3))
SHOTS['CH']=BALLW(0,'slowwa',5,slow=.42,t_rel=1.0)
def BOOM_():
    S=pset(); b=S['ball']; mo=S['mo']; t_hit=.45
    for i in range(6): puff((0,0,.3),t_hit,size=.12,n=6,col=M('#B88A6A',.8,alpha=.7),rise=.4,life=1.6,seed=40+i)
    def upd(t):
        fidle(S,t); mstance(S,t); tt=t_hit+(t-t_hit)*(.45 if t>t_hit else 1)
        if t<t_hit: b.location=arc(Vector((2.2,.12,.12)),Vector((.02,0,.5)),t/t_hit,.15)
        else: f=tt-t_hit; b.location=(-.5-4*f,.2,max(.07,.6+2*f-4.9*f*f))
        bricks_fall(S['wk'],tt,t_hit,2.4,7)
        if t>t_hit:
            face(mo,mouth='O',brow=.06,eyes=1.3); mo['root'].rotation_euler[0]=R(-10)
            k4=S['F']['b4']; k4['root'].rotation_euler[0]=R(30); k4['arm'][1].rotation_euler=(R(-150),0,R(30)); k4['arm'][-1].rotation_euler=(R(-150),0,R(-30)); face(k4,mouth='O')
        k4=S['F']['b4']; k4['root'].location=(-2.0,1.1,0)
        q=ease(t/DUR); camset(LV((-1.2,-2.4,.7),(-1.5,-2.6,.9),q),(-.2,0,.55),22,4)
    return dict(upd=upd)
SHOTS['BOOM']=BOOM_
def M4_():
    S=pset(); mo=S['mo']; b=S['ball']
    def upd(t):
        fidle(S,t,look=hp(mo)); bricks_fall(S['wk'],10,0,2.4,7)
        k=tl(t,.15,.7); x=CREASE[0]-1.1*ease(tl(t,1.3,DUR)); mo['root'].location=(x if t>1.3 else CREASE[0],CREASE[1]-.4*ease(tl(t,1.3,DUR)),0)
        mo['root'].rotation_euler=(0,0,R(lerp_angle(60,-120,tl(t,1.1,1.6))))
        if t>1.3: walk(mo,(t-1.3)*1.1+mo['seed'],step=.5,arm=10)
        else: stand(mo,t)
        blink(mo,t); talk(mo,t,*wt(52,61),rest='flat'); face(mo,brow=-.03,brow_r=-10,eyes=.85)
        hand=mo['arm'][1].matrix_world@Vector(hand_loc(mo,1)); mo['arm'][1].rotation_euler=(R(-70),0,R(10)); b.location=hand
        S['batp'].location=(-.3,.05,1.9); S['batp'].rotation_euler=(R(-60),R(10),R(90)); mo['arm'][-1].rotation_euler=(R(-150),0,R(-20))
        for H in S['F'].values(): face(H,mouth='o',brow=.05)
        S['F']['b4']['root'].location=(-2.6,2.3,0)
        h=hp(mo); camset((-4.2,-2.2,1.9),(h[0],h[1],h[2]-.4),30,2.8)
    return dict(upd=upd)
SHOTS['M4']=M4_
PLEAD_POS={'wa':(-1.2,-1.9),'b1':(-.4,.9),'b2':(-2.6,1.3),'b3':(-2.4,-1.7)}
def PLEAD_():
    S=pset(); mo=S['mo']; b=S['ball']; bricks=S['wk']; mx,my=(-1.8,-.2)
    P=dict(S['F']); P['wa']=S['wa']
    def upd(t):
        bricks_fall(bricks,10,0,2.4,7)
        mo['root'].location=(mx-1.6,my,0); mo['root'].rotation_euler=(0,0,R(90)); stand(mo,t); blink(mo,t)
        nod=tl(t,ws(67),ws(67)+.4)
        for s in (1,-1): arm_to(mo,s,root_mat(mo)@Vector((s*.05,-.42,1.5)),1-nod)
        mo['head'].rotation_euler=(R(10*math.sin((t-ws(67))*9)*nod*(1-tl(t,ws(67)+.9,ws(67)+1.2))),R(-14*(1-nod)),0); face(mo,mouth='smirk' if nod>.5 else 'flat',brow=.04*nod)
        hand=mo['arm'][1].matrix_world@Vector(hand_loc(mo,1)); b.location=hand
        S['batp'].location=(-.3,.05,1.9); S['batp'].rotation_euler=(R(-60),R(10),R(90))
        for i,(k,(x,y)) in enumerate(PLEAD_POS.items()):
            H=P[k]; H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(face_dir(mo['root'].location[0]-x,my-y))); stand(H,t+i); blink(H,t)
            m=root_mat(H)
            for s in (1,-1): arm_to(H,s,m@Vector((s*.03,-.5,1.55+.05*math.sin(t*6+i))),1)
            H['head'].rotation_euler=(R(8),0,R(6*math.sin(t*3+i))); face(H,mouth='o' if nod<.5 else 'grin',brow=.06 if nod<.5 else .02,brow_r=-10 if nod<.5 else 0)
        k4=S['F']['b4']; stand(k4,t); blink(k4,t); k4['root'].location=(-4.4,1.2,0); k4['root'].rotation_euler=(0,0,R(face_dir(1.0,-1.4)))
        for s in (1,-1): arm_to(k4,s,root_mat(k4)@Vector((s*.03,-.5,1.55)),1)
        face(k4,mouth='o',brow=.06)
        q=ease(t/DUR); camset(LV((1.4,-1.7,2.0),(.9,-1.5,1.9),q),(-2.5,0,1.35),24,5.6)
    return dict(upd=upd)
SHOTS['PLEAD']=PLEAD_
def SIX_():
    S=pset(); b=S['ball']; tr=1.05; t_hit=tr+.5; land=we(85)-.15
    def upd(t):
        fidle(S,t); mstance(S,t); mo=S['mo']
        p=bowl(S,t,tr)
        pc=Vector((1.35,-.36,1.1)); pl=Vector((RX+.2,GY+2.2,.07))
        if p is not None: b.location=p
        elif t<t_hit:
            f=(t-tr)/.5; p0=Vector((REL_X-.25,LANE+.1,2.55)); pb=Vector((3.0,.1,.07))
            b.location=p0.lerp(pb,min(1,f/.65)) if f<.65 else arc(pb,pc,(f-.65)/.35,.2)
        elif t<land: b.location=arc(pc,pl,(t-t_hit)/(land-t_hit),7.0)
        else: b.location=pl
        if t>t_hit-.35: bat_angle(S,L(40,-150,ease_out(tl(t,t_hit-.35,t_hit+.2))),-25*tl(t,t_hit-.1,t_hit+.3)); bat_hands(S)
        if t>t_hit:
            look_at(mo,b.location,.7,maxpitch=70,maxyaw=110); face(mo,mouth='grin',brow=.05)
            for k_,H in S['F'].items(): look_at(H,b.location,.8,maxpitch=70,maxyaw=110); face(H,mouth='O',eyes=1.2)
            wa=S['wa']; look_at(wa,b.location,.8,maxpitch=70,maxyaw=120); face(wa,mouth='O',eyes=1.2)
        if t<t_hit+.25: camset((7.2,-1.6,2.1),(1.8,0,1.2),24,5.6)
        else:
            bl=Vector(b.location); f=tl(t,t_hit+.25,land+.3); cpos=Vector((L(5.5,RX-4.5,ease(f)),L(-1.6,-1.2,f),L(2.0,2.6,math.sin(pi*f)*.6+f*.4)))
            camset(tuple(cpos),tuple(bl.lerp(Vector((RX,GY,1.8)),.4+.6*tl(t,land-.4,land+.3))),22,8)
    return dict(upd=upd)
SHOTS['SIX']=SIX_
def gset():
    S=pset(bat_on=False)
    return S
def gate_open(S,k):
    for h in S['leaves']: s_=1 if h.location.x>RX else -1; h.rotation_euler[2]=R(-s_*95*k)
def GATE_():
    S=gset(); b=S['ball']; b.location=(0,0,-5)
    for H in list(S['F'].values())+[S['mo'],S['wa']]: H['root'].location=(H['root'].location[0],-30,0)
    def upd(t):
        q=ease(t/DUR); camset(LV((RX-.4,-2.6,1.2),(RX-.2,-.6,1.5),q),LV((RX,GY,2.4),(RX,GY,2.2),q),L(22,26,q),5.6)
    return dict(upd=upd)
SHOTS['GATE']=GATE_
GW=(RX+.95,GY-1.05)
def M5_():
    S=pset(); mo=S['mo']; wa=S['wa']; b=S['ball']; b.location=(0,0,-5); bricks_fall(S['wk'],10,0,2.4,7)
    MP=(RX-1.4,GY-2.3); WP=(RX+.6,GY-2.0)
    for i,(k,H) in enumerate(S['F'].items()): H['root'].location=[(RX-3.4,.9),(RX-4.7,.2),(RX-3.2,-.7),(RX-4.9,-1.4)][i]+(0,)
    def upd(t):
        mo['root'].location=(MP[0],MP[1],0); mo['root'].rotation_euler=(0,0,R(face_dir(WP[0]-MP[0],WP[1]-MP[1]))); stand(mo,t); blink(mo,t)
        k=tl(t,ws(101)-.1,ws(101)+.2); arm_to(mo,1,Vector((WP[0],WP[1],1.6)),k) if k>0 else None; look_at(mo,(RX-.4,-1.6,1.9),.5*(1-k)); talk(mo,t,*wt(97,106),rest='smirk'); face(mo,brow=.04)
        S['batp'].location=(-.3,.05,1.9); S['batp'].rotation_euler=(R(-60),R(10),R(90)); mo['arm'][-1].rotation_euler=(R(-150),0,R(-20))
        wa['root'].location=(WP[0],WP[1],0); wa['root'].rotation_euler=(0,0,R(face_dir(MP[0]-WP[0],MP[1]-WP[1]))); stand(wa,t); blink(wa,t)
        kk=tl(t,ws(102),ws(102)+.3); face(wa,mouth='O' if kk>.5 else 'flat',brow=.06*kk,eyes=1+.25*kk); wa['arm'][1].rotation_euler=(R(-60*kk),R(20*kk),R(30*kk))
        for i,H in enumerate(S['F'].values()): stand(H,t+i); blink(H,t); H['root'].rotation_euler=(0,0,R(face_dir(MP[0]-H['root'].location[0],MP[1]-H['root'].location[1]))); look_at(H,hp(mo),.6); face(H,mouth='smile')
        c0=(RX-.4,-2.4,1.95); tg=(RX-.4,1.15,1.55); camset(drift(c0,tg,t),tg,20,2.8)
    return dict(upd=upd)
SHOTS['M5']=M5_
def razia_mk(S):
    R_=mk(RAZIA,RX,GY+.95,0,'razia'); return R_
def KNOCK_():
    S=gset(); wa=S['wa']; b=S['ball']; b.location=(0,0,-5); R_=razia_mk(S); bk=bucket_obj(R_['root']); bk.location=(0,-.62,.85)
    for H in list(S['F'].values())+[S['mo']]: H['root'].location=(H['root'].location[0],-30,0)
    def upd(t):
        wa['root'].location=(GW[0],GW[1],0); wa['root'].rotation_euler=(0,0,R(180)); stand(wa,t); blink(wa,t)
        kn=[.35,.65,.95]; a=max([max(0,1-abs(t-x)/.13) for x in kn]); arm_to(wa,1,(GW[0]-.1,GY+.05,1.85),.6+.4*a); face(wa,mouth='flat',brow=.03)
        go=tl(t,1.3,2.0); gate_open(S,ease(go))
        stand(R_,t); blink(R_,t); R_['root'].location=(RX,GY+.95,0); m=root_mat(R_)
        for s in (1,-1): arm_to(R_,s,m@Vector((s*.28,-.6,1.42)),1)
        face(R_,mouth='flat',brow=-.02,brow_r=-8,eyes=.85)
        if go>.6: wa['root'].rotation_euler[0]=R(-6*tl(t,2.0,2.3)); face(wa,mouth='O',eyes=1.25,brow=.06)
        q=ease(t/DUR); camset(LV((RX-1.9,GY-4.0,1.9),(RX-1.6,GY-3.6,1.9),q),(RX+.1,GY+.4,1.6),24,5.6)
    return dict(upd=upd)
SHOTS['KNOCK']=KNOCK_
def R1_():
    S=gset(); wa=S['wa']; b=S['ball']; b.location=(0,0,-5); R_=razia_mk(S); bk=bucket_obj(R_['root']); bk.location=(0,-.62,.85); gate_open(S,1)
    for H in list(S['F'].values())+[S['mo']]: H['root'].location=(H['root'].location[0],-30,0)
    def upd(t):
        wa['root'].location=(GW[0]+1.1,GW[1]-.3,0); wa['root'].rotation_euler=(R(-5),0,R(200)); stand(wa,t); blink(wa,t); face(wa,mouth='O',eyes=1.2,brow=.06)
        stand(R_,t); blink(R_,t); m=root_mat(R_)
        for s in (1,-1): arm_to(R_,s,m@Vector((s*.28,-.6,1.42)),1)
        talk(R_,t,*wt(107,109),rest='flat'); face(R_,brow=-.02,brow_r=-8,eyes=.85); R_['head'].rotation_euler[1]=R(-8)
        c0,tg,ln=closecam(R_,0,-.5,3.0,lens=32,tz=-.45); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['R1']=R1_
def BAT_():
    S=gset(); wa=S['wa']; b=S['ball']; b.location=(0,0,-5); R_=razia_mk(S); gate_open(S,1)
    bk=bucket_obj(); bk.location=(RX+1.0,GY+.55,0)
    rb=empty((0,0,0),R_['root']); bat_obj(rb); rb.location=(.3,-.15,2.0); rb.rotation_euler=(R(150),0,R(-15))
    for H in list(S['F'].values())+[S['mo']]: H['root'].location=(H['root'].location[0],-30,0)
    def upd(t):
        k=ease(tl(t,.1,1.1)); R_['root'].location=(RX,L(GY+.95,GY-.45,k),0); R_['root'].rotation_euler=(0,0,0)
        if 0.1<t<1.1: walk(R_,k*1.4+R_['seed'],step=.4,arm=0)
        else: stand(R_,t)
        blink(R_,t); arm_to(R_,1,rb.matrix_world.translation,1); R_['arm'][-1].rotation_euler=(R(-30),0,R(-40))
        talk(R_,t,*wt(110,116),rest='smirk'); face(R_,brow=-.03,brow_r=-6,eyes=.9)
        wy=L(GW[1],GW[1]-1.0,ease(tl(t,.2,1.1))); wa['root'].location=(GW[0]+1.4,wy,0); wa['root'].rotation_euler=(R(-6),0,R(160)); stand(wa,t); blink(wa,t); face(wa,mouth='O',eyes=1.2,brow=.06)
        q=ease(t/DUR); camset(LV((RX-.7,GY-4.6,1.6),(RX-.6,GY-4.2,1.7),q),(RX+.3,GY-.8,1.8),24,4)
    return dict(upd=upd)
SHOTS['BAT']=BAT_
def ENDW_():
    S=pset(bat_on=False); b=S['ball']; mo=S['mo']; wa=S['wa']; bricks=S['wk']
    R_=mk(RAZIA,CREASE[0],CREASE[1],90,'razia'); rp=empty((0,0,0),R_['root']); bat_obj(rp); rp.location=(.22,-.42,1.22)
    bk=bucket_obj(wa['root']); bk.location=(0,-.55,.9)
    tr=1.35; t_hit=tr+.5; land=t_hit+1.8
    def upd(t):
        fidle(S,t)
        R_['root'].location=(CREASE[0],CREASE[1],0); R_['root'].rotation_euler=(R(6),0,R(90)); stand(R_,t); blink(R_,t)
        a=L(30,-150,ease_out(tl(t,t_hit-.35,t_hit+.2))) if t>t_hit-.35 else 30; rp.rotation_euler=(R(a),0,0)
        for s in (1,-1): arm_to(R_,s,rp.matrix_world.translation+Vector((0,0,.02*s)),1)
        face(R_,mouth='smirk',brow=-.02)
        # Moiz bowls, sad
        v=3.2; t_run=(RUN0-REL_X)/v; t0=tr-t_run
        if t<tr:
            x=RUN0-max(0,t-t0)*v; mo['root'].location=(x,LANE,0); mo['root'].rotation_euler=(0,0,R(-90))
            if t>t0: walk(mo,(t-t0)*v*.6+mo['seed'],step=.7,arm=20)
            else: stand(mo,t)
            k=tl(t,tr-.35,tr); mo['arm'][1].rotation_euler=(R(-10-330*k),0,R(4)); b.location=mo['arm'][1].matrix_world@Vector(hand_loc(mo,1))
        else:
            mo['root'].location=(REL_X-.6,LANE,0); stand(mo,t); mo['arm'][1].rotation_euler=(R(-20),0,R(4))
            pc=Vector((1.35,-.36,1.1)); pl=Vector((-14,1.2,9))
            if t<t_hit: f=(t-tr)/.5; p0=Vector((REL_X-.25,LANE+.1,2.4)); pb=Vector((3.0,.1,.07)); b.location=p0.lerp(pb,min(1,f/.65)) if f<.65 else arc(pb,pc,(f-.65)/.35,.2)
            else: b.location=arc(pc,Vector((14,1.0,.5)),min(1.2,(t-t_hit)/land),9)
        blink(mo,t); face(mo,mouth='flat',brow=-.04,brow_r=-12,eyes=.8); mo['head'].rotation_euler[0]=R(10)
        wa['root'].location=(3.6,2.1,0); wa['root'].rotation_euler=(0,0,R(face_dir(-3.0,-2.4))); stand(wa,t); blink(wa,t)
        for s in (1,-1): arm_to(wa,s,root_mat(wa)@Vector((s*.3,-.6,1.45)),1)
        face(wa,mouth='smile' if t<t_hit else 'O')
        bricks_fall(bricks,0,99); S['F']['b2']['root'].location=(8.2,-2.4,0)
        q=ease(t/DUR); camset(LV((6.6,-2.0,1.8),(6.2,-1.9,1.7),q),LV((.6,-.3,1.3),(.8,-.3,1.3),q),24,8)
    return dict(upd=upd)
SHOTS['ENDW']=ENDW_
def CTA_():
    S=pset(bat_on=False); mo=S['mo']; b=S['ball']; b.location=(0,0,-5)
    R_=mk(RAZIA,CREASE[0],CREASE[1],90,'razia'); rp=empty((0,0,0),R_['root']); bat_obj(rp); rp.location=(.22,-.42,1.22); rp.rotation_euler=(R(30),0,0)
    def upd(t):
        fidle(S,t); R_['root'].location=(CREASE[0],CREASE[1],0); R_['root'].rotation_euler=(R(6),0,R(90)); stand(R_,t); blink(R_,t)
        for s in (1,-1): arm_to(R_,s,rp.matrix_world.translation+Vector((0,0,.02*s)),1)
        face(R_,mouth='smirk')
        mo['root'].location=(REL_X-1.0,LANE,0); mo['root'].rotation_euler=(0,0,R(-60)); stand(mo,t); blink(mo,t)
        mo['arm'][1].rotation_euler=(R(-5),0,R(6)); mo['arm'][-1].rotation_euler=(R(-5),0,R(-6)); look_at(mo,(REL_X-3.5,-4,2.0),.8); face(mo,mouth='flat',brow=-.04,brow_r=-14,eyes=.8)
        c0,tg,ln=closecam(mo,-60,.0,2.9,lens=32,bias=.6); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['CTA']=CTA_
