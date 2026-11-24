# Shots for Karachi ep 2 "Biryani ke mamle mein compromise nahi". Cuts sit on narration words (audio/words.json); SEQ is written by gen_seq.py.
SHOTS={}
END=116.5667
SEQ=[('OPEN', 0.0), ('A1', 4.833), ('W1', 7.433), ('Z1', 10.233), ('W2', 14.3), ('AY1', 16.967), ('W3', 20.4), ('A2', 23.167), ('Z2', 26.467), ('ARRIVE', 30.5), ('Z3', 33.633), ('A3', 36.233), ('Z4', 38.367), ('W4', 43.367), ('Z5', 46.733), ('SERVE', 50.1), ('BITE', 52.033), ('W5', 53.3), ('Z6', 55.4), ('A4', 58.633), ('W6', 60.733), ('Z7', 64.067), ('AY2', 67.333), ('A5', 71.3), ('W7', 74.433), ('Z8', 75.9), ('W8', 78.867), ('AY3', 82.4), ('W9', 85.4), ('FIN', 89.167), ('W10', 91.933), ('Z9', 93.333), ('W11', 94.767), ('Z10', 97.233), ('W12', 99.6), ('A6', 101.967), ('MORAL', 106.067), ('FINAL', 112.467)]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0
def we(i): return W_[i]['e']-T0
def fwd(rz): return (math.sin(R(rz)),-math.cos(R(rz)))
CASTS={'wa':WALEED,'al':ALI,'zo':ZOHAIB,'ay':AYESHA}
def lap(H):
    m=root_mat(H)
    for s in (1,-1): arm_to(H,s,m@Vector((s*.3,-.55,.95)),1)
def tarms(H,dz=0.0):
    m=root_mat(H)
    for s in (1,-1): arm_to(H,s,m@Vector((s*.32,-.6,1.2+dz)),1)
def closecam(H,rz,side=.3,dist=3.0,dz=.05,tz=-.3,lens=36,bias=1.2):
    h=hp(H); f=fwd(rz); f=(f[0],f[1]-bias); n_=math.hypot(*f); f=(f[0]/n_,f[1]/n_); rt=(-f[1],f[0])
    return (h[0]+f[0]*dist+rt[0]*side,h[1]+f[1]*dist+rt[1]*side,h[2]+dz),(h[0],h[1],h[2]+tz),lens
def drift(c0,tg,t,a=.06): q=ease(t/DUR); return LV(c0,(L(c0[0],tg[0],a),L(c0[1],tg[1],a),c0[2]),q)
# ================================================================ SCENE 1: in the SUV
def dset():
    S=drive_k(); P={}
    for k,(x,y) in CAR_SEATS.items(): P[k]=mk(CASTS[k],x,y,0,k)
    belts(P); S['P']=P; return S
def didle(S,t,free=()):
    scroll(S['bg'],T0+t); bump=.012*math.sin((T0+t)*7.3)+.008*math.sin((T0+t)*11.1)
    S['car']['root'].location[2]=bump
    for w_ in S['car']['wheels']: w_.rotation_euler[1]=-(T0+t)*9.0/.55
    for k,H in S['P'].items():
        x,y=CAR_SEATS[k]; seat(H,t+dseed(k),.55); H['root'].location[0]=x; H['root'].location[1]=y; H['root'].location[2]+=bump; H['root'].rotation_euler[2]=0; H['head'].rotation_euler=(0,0,0)
        if k in free: continue
        if k=='al':                                              # hands on the steering wheel
            for s in (1,-1): arm_to(H,s,(x+s*.2,-1.22,1.25+bump),1)
        else: lap(H)
FRONT=((0,-3.25,1.9),(0,.4,1.55),26)                            # through the windshield
def dtalk(key,a,b,extra=None,rest_='flat',cam=None,look=None):
    def S_():
        S=dset(); P=S['P']; H=P[key]
        def upd(t):
            didle(S,t,free=(key,) if key!='al' else ()); talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k==key: continue
                if k=='al': look_at(o,hp(H),.25*(.5+.5*math.sin(t*.7)),maxyaw=40)      # driver glances, eyes mostly on the road
                else: look_at(o,hp(H),.55,maxyaw=70)
            if key!='al': lap(H) if not extra else None
            if extra: extra(S,t)
            c0,tg,ln=cam(H) if callable(cam) else (cam or FRONT); camset(drift(c0,tg,t),tg,ln,4.0)
        return dict(upd=upd)
    return S_
def cam_front(H):                                                # close-up through the windshield on one occupant
    h=hp(H); return (h[0]*.6,-3.1,h[2]+.05),(h[0],h[1],h[2]-.3),40 if h[1]<0 else 46
def cam_side(H):                                                 # from outside the side window
    h=hp(H); s=1 if h[0]>0 else -1; return (h[0]+s*2.8,h[1]-1.6,h[2]+.1),(h[0],h[1],h[2]-.3),34
def _a1(S,t): pass
def _w1(S,t): H=S['P']['wa']; gest(H,t,1,.7,5,-60); arm_to(H,-1,root_mat(H)@Vector((-.3,-.55,.95)),1); face(H,brow=.05)
def _z1(S,t): H=S['P']['zo']; gest(H,t,-1,.8,6,-70); arm_to(H,1,root_mat(H)@Vector((.3,-.55,.95)),1); face(H,brow=.04,brow_r=-8)
def _w2(S,t): H=S['P']['wa']; H['arm'][1].rotation_euler=(R(-60),0,R(-10)); arm_to(H,-1,root_mat(H)@Vector((-.3,-.55,.95)),1); look_at(H,hp(S['P']['zo']),.5,maxyaw=100); face(H,mouth='smirk' if t>we(46) else 'flat')
def _ay1(S,t): H=S['P']['ay']; gest(H,t,1,.7,5,-65); arm_to(H,-1,root_mat(H)@Vector((-.3,-.55,.95)),1); face(H,brow=.04,brow_r=-6)
def _w3(S,t): H=S['P']['wa']; arm_to(H,1,root_mat(H)@Vector((.05,-.4,1.7)),tl(t,0,.3)); arm_to(H,-1,root_mat(H)@Vector((-.3,-.55,.95)),1); face(H,brow=.06)
def _a2(S,t): H=S['P']['al']; look_at(H,(0,-1.3,2.25),.8*tl(t,0,.3)*(1-tl(t,we(74)-.3,we(74))),maxyaw=40); face(H,brow=.04)
def _z2(S,t): H=S['P']['zo']; arm_to(H,1,root_mat(H)@Vector((.1,-.45,1.55)),tl(t,0,.3)); arm_to(H,-1,root_mat(H)@Vector((-.3,-.55,.95)),1); face(H,brow=.06)
SHOTS['A1']=dtalk('al',12,17,cam=cam_front,rest_='smile')
SHOTS['W1']=dtalk('wa',18,24,extra=_w1,cam=cam_front,rest_='smirk')
SHOTS['Z1']=dtalk('zo',25,38,extra=_z1,cam=cam_side)
SHOTS['W2']=dtalk('wa',39,46,extra=_w2,cam=cam_front,rest_='smirk')
SHOTS['AY1']=dtalk('ay',47,59,extra=_ay1,cam=cam_side,rest_='smirk')
SHOTS['W3']=dtalk('wa',60,64,extra=_w3,cam=cam_front,rest_='grin')
SHOTS['A2']=dtalk('al',65,74,extra=_a2,cam=FRONT)
SHOTS['Z2']=dtalk('zo',75,82,extra=_z2,cam=cam_side,rest_='grin')
# ================================================================ SCENE 2: outside the restaurant / at the counter
OUT={'wa':(-1.1,-3.0),'zo':(.85,-2.5),'al':(2.6,-3.2),'ay':(-2.9,-3.4)}       # standing on the footpath facing the counter
def rset(stage=None,car_=True,tablek=None):
    S=rest_k(car_); P={k:mk(CASTS[k],0,0,0,k) for k in ('wa','al','zo','ay')}; S['P']=P
    S['cook']=mk(COOK,-2.1,1.25,180,'cook'); S['wt']=mk(WAITER,2.4,9.3,180,'waiter')
    S['D']=[mk(person(91+i*5),x,y,rz,'d%d'%i) for i,(x,y,rz) in enumerate(S['bg'])]
    steam((-1.6,COUNTER_Y+.05,2.05),0,999,n=14,seed=21,size=.1); steam((1.6,COUNTER_Y+.05,2.05),0,999,n=14,seed=22,size=.1)
    S['W']=walkers(6,9,-25,25,(-6.4,),z=.0)
    return S
def ridle(S,t):
    fans_spin(S,T0+t); upd_walkers(S['W'],T0+t)
    c=S['cook']; stand(c,t); blink(c,t); c['root'].location=(-2.1,1.25,0); c['root'].rotation_euler=(0,0,R(180)); c['arm'][1].rotation_euler=(R(-75+14*math.sin(t*3.2)),0,R(10)); c['arm'][-1].rotation_euler=(R(-45),0,R(-10))
    for i,H in enumerate(S['D']):
        x,y,rz=S['bg'][i]; seat(H,t+i*1.3,.58); H['root'].rotation_euler[2]=R(rz); m=root_mat(H); c_=math.sin(t*5+i*1.7)
        arm_to(H,1,m@Vector((.2,-.6,L(1.2,1.75,max(0,c_)))),1); arm_to(H,-1,m@Vector((-.3,-.6,1.2)),1); face(H,mouth='o' if c_>.3 else 'smile')
def ostand(S,t,look=(0,1.2,2.3)):
    for k,H in S['P'].items():
        x,y=OUT[k]; H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(180+.0)); stand(H,t+dseed(k)); blink(H,t)
        H['arm'][1].rotation_euler=(R(-5),0,R(6)); H['arm'][-1].rotation_euler=(R(-5),0,R(-6)); H['head'].rotation_euler=(0,0,0)
def ocam(H,side=0.0):                                            # from behind the counter, over the degs, looking out at the speaker
    h=hp(H); return (h[0]*.7+side,-.2,h[2]+.2),(h[0],h[1],h[2]-.35),23
def otalk(key,a,b,extra=None,rest_='flat',cam=None):
    def S_():
        S=rset(); P=S['P']; H=P[key]
        def upd(t):
            ridle(S,t); ostand(S,t); talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k!=key: look_at(o,hp(H),.6,maxyaw=80)
            if extra: extra(S,t)
            c0,tg,ln=cam(H) if callable(cam) else (cam or ocam(H)); camset(drift(c0,tg,t),tg,ln,4.0)
        return dict(upd=upd)
    return S_
def OPEN_():
    S=rset(car_=True); P=S['P']
    for i,H in enumerate(P.values()): H['root'].location=(i*4,-60,0)
    def upd(t):
        ridle(S,t)
        q=ease(t/DUR); camset(LV((-2.5,-8.5,6.5),(-.4,-4.6,3.1),q),LV((0,.5,3.6),(0,.6,2.0),q),L(20,22,q),8)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def _wsign(S,t):
    H=S['P']['wa']; k=tl(t,0,.4); look_at(H,(0,-.3,5.4),.9*k,maxpitch=40); H['arm'][1].rotation_euler=(R(-140*k),R(-10),R(10)); face(H,brow=.06,brow_r=12,eyes=1.15)
    for k_ in ('al','ay'): look_at(S['P'][k_],(0,-.3,5.4),.8,maxpitch=40); face(S['P'][k_],mouth='flat',brow=.05)
    look_at(S['P']['zo'],hp(H),.6); face(S['P']['zo'],mouth='grin')
def ARRIVE_():
    S=rset(); P=S['P']; T=dict(SEQ)['ARRIVE']
    def upd(t):
        ridle(S,t); ostand(S,t); H=P['wa']; talk(H,t,*wt(83,86),rest='o'); _wsign(S,t)
        q=ease(t/DUR); camset(LV((-.6,-7.4,1.9),(-.5,-6.6,2.1),q),LV((0,-1.4,2.6),(0,-1.2,3.2),q),22,6)
    return dict(upd=upd)
SHOTS['ARRIVE']=ARRIVE_
def _z3(S,t): H=S['P']['zo']; H['arm'][1].rotation_euler=(R(-80),R(-10),R(20)); face(H,brow=.04)
def _a3(S,t):
    H=S['P']['al']; k=tl(t,0,.3); H['arm'][1].rotation_euler=(R(-95*k),0,R(5)); face(H,brow=.03)
    c=S['cook']; c['root'].rotation_euler[0]=R(10*tl(t,we(99)-.2,we(99)+.2)*(1-tl(t,we(99)+.4,we(99)+.8))); face(c,mouth='smile')
def _z4(S,t):
    H=S['P']['zo']; arm_to(H,1,(OUT['zo'][0]+.1,COUNTER_Y-.2,1.5),tl(t,0,.3)); face(H,brow=.06,brow_r=-6)
    c=S['cook']; look_at(c,hp(H),.8); face(c,mouth='flat',brow=-.02)
def _w4(S,t): H=S['P']['wa']; gest(H,t,1,.8,6,-70); face(H,brow=.05,brow_r=8); look_at(H,hp(S['P']['zo']),.9,maxyaw=85)
def _z5(S,t): H=S['P']['zo']; H['arm'][1].rotation_euler=(R(-75),0,R(-15)); H['root'].rotation_euler[0]=R(-4); face(H,brow=-.02,brow_r=-8,eyes=.85)
SHOTS['Z3']=otalk('zo',87,93,extra=_z3,rest_='smile')
SHOTS['A3']=otalk('al',94,99,extra=_a3,rest_='smile')
SHOTS['Z4']=otalk('zo',100,114,extra=_z4)
SHOTS['W4']=otalk('wa',115,124,extra=_w4,rest_='smirk')
SHOTS['Z5']=otalk('zo',125,132,extra=_z5)
# ================================================================ SCENES 3-5: at the table
def tset(stage='full',plates=True):
    S=rset(car_=False); P=S['P']
    S['wt']['root'].location=(0,-60,0)
    S['plates']={}
    for k,(x,y) in TSEATS.items():
        px=x*.38; e=empty((px,y,1.03)); S['plates'][k]=e
        ocyl((0,0,.02),.26,.03,M('#F4F1EA',.25,spec=.8),e,rot=(0,0,0),seg=20)
        mound=oico((0,0,.04),1.0,M('#F2C45A',.65),e,sc=(.2,.2,.08),sub=2); pc=oico((.08,.05,.11),.07,M('#9A4A1E',.55),e,sc=(1.3,1,.8),sub=2)
        S['plates'][k+'_food']=(mound,pc)
        ocyl((-.2,-.24,.04),.09,.08,M('#F4F1EA',.3),e,rot=(0,0,0),seg=12); ocyl((-.2,-.24,.09),.075,.02,M('#E6EEDF',.5),e,rot=(0,0,0),seg=12)   # raita bowl
        obox((.25,0,.02),(.012,.12,.006),M('#C9CED8',.25,metal=.9),.004,e)
        if not plates: e.scale=(0,0,0)
    if stage=='empty':
        for k in TSEATS: m_,p_=S['plates'][k+'_food']; m_.scale=(.2*.35,.2*.35,.08*.5); p_.scale=(0,0,0)
    return S
def tidle(S,t,free=()):
    ridle(S,t)
    for k,H in S['P'].items():
        x,y=TSEATS[k]; seat(H,t+dseed(k),.6); H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(tseat_rz(k)); H['head'].rotation_euler=(0,0,0)
        if k not in free: tarms(H)
def ttalk(key,a,b,extra=None,init=None,rest_='flat',stage='full',free=(),cam=None,dist=3.0,side=.3,lens=36):
    def S_():
        S=tset(stage); P=S['P']; H=P[key]
        if init: init(S)
        def upd(t):
            tidle(S,t,free=free); talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k!=key: look_at(o,hp(H),.55,maxyaw=75)
            if extra: extra(S,t)
            c0,tg,ln=cam if cam else closecam(H,tseat_rz(key),side,dist,lens=lens); camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
TW=((0,1.9,2.75),(0,5.0,1.45),24)                                  # down the length of the table
def SERVE_():
    S=tset('full'); P=S['P']; w=S['wt']; T=dict(SEQ)['SERVE']; tb=ws(133)
    for k in TSEATS: S['plates'][k].scale=(0,0,0)
    tray=obox((0,0,0),(.45,.3,.02),M('#C9CED8',.25,metal=.85),.01)
    def upd(t):
        tidle(S,t); k=tl(t,0,1.0)
        wx,wy=L(2.0,0,ease(k)),L(9.1,7.2,ease(k)); w['root'].location=(wx,wy,0); w['root'].rotation_euler=(0,0,R(lerp_angle(face_dir(-2,-1.9),0,k)))
        if k<1: walk(w,k*2.6,step=.45,arm=0)
        else: stand(w,t)
        blink(w,t); m=root_mat(w); tp=m@Vector((0,-.6,1.4)); tray.location=tp
        for s in (1,-1): arm_to(w,s,tp+Vector((s*.2,0,-.02)),1)
        for i,kk in enumerate(TSEATS): S['plates'][kk].scale=(1,1,1) if t>.9+i*.12 else (0,0,0)
        if t>.9: tray.scale=(1,1,1)
        face(w,mouth='smile')
        for kk,H in P.items(): look_at(H,(0,4.9,1.1),.6,maxpitch=40); face(H,mouth='grin',brow=.04)
        if t>tb: talk(P['al'],t,*wt(133,133),rest='smile'); P['al']['arm'][1].rotation_euler=(R(-60),R(10),R(-10))
        q=ease(t/DUR); camset(LV((.3,1.7,2.9),(.2,2.2,2.7),q),LV((0,4.9,1.4),(0,5.2,1.3),q),24,4)
    return dict(upd=upd)
SHOTS['SERVE']=SERVE_
def eat(H,t,ph=0.0,k=1.0):
    m=root_mat(H); c=.5+.5*math.sin(t*5.5+ph); arm_to(H,1,(m@Vector((.18,-.62,1.12))).lerp(m@Vector((.1,-.28,1.9)),c),k)
def BITE_():
    S=tset('full'); P=S['P']
    def upd(t):
        tidle(S,t,free=('wa','zo','al'))
        for i,k in enumerate(('wa','zo','al')): eat(P[k],t,i*1.4); face(P[k],mouth='o' if math.sin(t*5.5+i*1.4)>.4 else 'flat',brow=.04); arm_to(P[k],-1,root_mat(P[k])@Vector((-.32,-.6,1.2)),1)
        ay=P['ay']; talk(ay,t,*wt(134,135),rest='smile'); look_at(ay,hp(P['wa']),.7,maxyaw=80)
        q=ease(t/DUR); camset(LV(TW[0],(0,-.1,2.5),q),TW[1],TW[2],4)
    return dict(upd=upd)
SHOTS['BITE']=BITE_
def _chew(S,t,k='wa'): H=S['P'][k]; H['head'].rotation_euler[0]+=R(2*math.sin(t*12))
def _w5(S,t): _chew(S,t); H=S['P']['wa']; H['arm'][1].rotation_euler=(R(-70),0,R(-20)); H['head'].rotation_euler[2]+=R(8*math.sin(t*2.5)); face(H,brow=.02,brow_r=-6,eyes=.85)
def _z6(S,t):
    H=S['P']['zo']; k=tl(t,0,.2)
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-10),0,R(s*120*k))
    face(H,brow=.06,brow_r=12,eyes=1.15)
def _a4(S,t): _chew(S,t,'al'); eat(S['P']['al'],t,.5); face(S['P']['al'],brow=.03)
def _w6(S,t): H=S['P']['wa']; gest(H,t,1,.7,5,-60); face(H,brow=.04,brow_r=8)
def _z7(S,t): H=S['P']['zo']; arm_to(H,1,hp(S['P']['wa'],-.5),tl(t,0,.2)*.85); face(H,brow=.06,brow_r=-12)
def _ay2(S,t):
    H=S['P']['ay']; tarms(H); H['head'].rotation_euler[2]+=R(8*math.sin(t*2)); face(H,brow=.05,brow_r=-10)
    for k_ in ('wa','zo'): face(S['P'][k_],mouth='flat',brow=.03)
SHOTS['W5']=ttalk('wa',136,138,extra=_w5,free=('wa',),rest_='flat')
SHOTS['Z6']=ttalk('zo',139,144,extra=_z6,free=('zo',),rest_='O')
SHOTS['A4']=ttalk('al',145,149,extra=_a4,free=('al',),rest_='smile')
SHOTS['W6']=ttalk('wa',150,158,extra=_w6,free=('wa',),rest_='flat')
SHOTS['Z7']=ttalk('zo',159,167,extra=_z7,free=('zo',))
SHOTS['AY2']=ttalk('ay',168,180,extra=_ay2,free=('ay',),rest_='smirk')
def _a5(S,t): H=S['P']['al']; gest(H,t,1,.6,5,-60); face(H,brow=.04)
def _w7(S,t): H=S['P']['wa']; arm_to(H,1,H['root'].matrix_world@Vector((.1,-.4,1.75)),tl(t,0,.25)); face(H,brow=.06)
def _z8(S,t): H=S['P']['zo']; gest(H,t,1,.9,7,-80); face(H,brow=.05,brow_r=10)
def _w8(S,t): H=S['P']['wa']; arm_to(H,1,hp(S['P']['zo'],-.5),tl(t,0,.2)*.85); face(H,brow=.06,brow_r=12)
def _ay3(S,t):
    H=S['P']['ay']; k=tl(t,0,.25)
    tarms(H,.04*math.sin(t*6))
    face(H,brow=.05,brow_r=-12,eyes=.85)
def _w9(S,t): H=S['P']['wa']; H['arm'][1].rotation_euler=(R(-95),R(-10),R(-5)); face(H,brow=-.02,brow_r=-6,eyes=.85); H['root'].rotation_euler[0]=R(5)
SHOTS['A5']=ttalk('al',181,188,extra=_a5,free=('al',))
SHOTS['W7']=ttalk('wa',189,190,extra=_w7,free=('wa',),rest_='grin')
SHOTS['Z8']=ttalk('zo',191,198,extra=_z8,free=('zo',),rest_='grin')
SHOTS['W8']=ttalk('wa',199,210,extra=_w8,free=('wa',))
SHOTS['AY3']=ttalk('ay',211,219,extra=_ay3,free=('ay',))
SHOTS['W9']=ttalk('wa',220,229,extra=_w9,free=('wa',))
def _full(S,t):
    for k,H in S['P'].items(): H['root'].rotation_euler[0]=R(-6)
def _z9(S,t): _full(S,t); H=S['P']['zo']; H['root'].rotation_euler[0]=R(0); H['arm'][1].rotation_euler=(R(-70),0,R(-15)); face(H,brow=.04)
def _w10(S,t): _full(S,t); H=S['P']['wa']; H['head'].rotation_euler[2]+=R(-10); face(H,brow=0,eyes=.9)
def _zshout(S,t):
    H=S['P']['zo']; k=tl(t,0,.15)
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-8*k),0,R(s*150*k))
    H['root'].rotation_euler[0]=R(-8*k); face(H,brow=.06,brow_r=14,eyes=1.3)
    for k_ in ('al','ay'): face(S['P'][k_],mouth='o',eyes=1.15,brow=.05)
def _w11i(S):
    S['wt']['root'].location=(-2.75,2.35,0)
    for i,(x,y,rz) in enumerate(S['bg']):
        if abs(x+2.9)<.2 and abs(y-3.6)<.2: S['bg'][i]=(x,-80,rz); S['D'][i]['root'].location=(x,-80,0)
def _w11(S,t):
    _full(S,t); H=S['P']['wa']; k=tl(t,0,.3); H['arm'][1].rotation_euler=(R(-70*k),R(20*k),R(40*k)); look_at(H,(-2.75,2.35,2.0),.8,maxyaw=100); face(H,brow=.02)
    w=S['wt']; stand(w,t); blink(w,t); w['root'].rotation_euler=(0,0,R(face_dir(1.55,1.65))); w['root'].rotation_euler[0]=R(8*tl(t,we(245)-.2,we(245)+.2)); face(w,mouth='smile')
def _z10(S,t):
    H=S['P']['zo']; arm_to(H,1,hp(S['P']['wa'],-.5),tl(t,0,.2)); face(H,brow=.06,brow_r=12,eyes=1.15)
def _w12(S,t): H=S['P']['wa']; H['arm'][1].rotation_euler=(R(-60),0,R(30)); H['arm'][-1].rotation_euler=(R(-60),0,R(-30)); face(H,brow=.05,eyes=1.1)
def _a6(S,t):
    for i,(k,H) in enumerate(S['P'].items()): laugh(H,t+i*.3,.9); face(H,mouth='grin',eyes=.7)
    H=S['P']['al']; arm_to(H,1,hp(S['P']['wa'],-.6),tl(t,0,.25)*.8)
SHOTS['FIN']=ttalk('zo',230,235,extra=_z9,stage='empty',free=('zo',),rest_='smirk')
SHOTS['W10']=ttalk('wa',236,237,extra=_w10,stage='empty',rest_='flat',dist=2.6)
SHOTS['Z9']=ttalk('zo',238,239,extra=_zshout,stage='empty',free=('zo',),rest_='shout',dist=2.4)
SHOTS['W11']=ttalk('wa',240,245,extra=_w11,init=_w11i,stage='empty',free=('wa',),cam=((1.2,.9,2.45),(-1.9,3.0,1.85),22))
SHOTS['Z10']=ttalk('zo',246,254,extra=_z10,stage='empty',free=('zo',),rest_='O')
SHOTS['W12']=ttalk('wa',255,262,extra=_w12,stage='empty',free=('wa',),rest_='grin')
SHOTS['A6']=ttalk('al',263,269,extra=_a6,stage='empty',free=('al',),rest_='grin',cam=TW)
def MORAL_():
    S=tset('empty'); P=S['P']; bag=None
    def upd(t):
        tidle(S,t)
        for k,H in P.items(): face(H,mouth='smile'); look_at(H,(0,4.9,1.8),.3)
        q=ease(t/DUR); camset(LV((0,1.6,2.6),(0,-9.5,4.2),q),LV((0,4.9,1.5),(0,2.5,3.4),q),L(24,20,q),8)
    return dict(upd=upd)
SHOTS['MORAL']=MORAL_
def FINAL_():
    S=tset('empty'); P=S['P']; wa=P['wa']
    bag=in_hand(wa,1,lambda e: (obox((0,-.1,-.05),(.2,.14,.22),M('#F4F1EA',.7),.03,e),stext('AL-NOOR',(0,-.25,-.02),.07,'#C8372D',parent=e)))
    sparkles((-1.2,4.0,2.6),1.2,ws(296),ws(296)+2.5,n=30,size=.04,seed=31,rise=.6,mat=M('#F2C45A',.4,emit=1.5))
    def upd(t):
        tidle(S,t,free=('wa',)); talk(wa,t,*wt(290,298),rest='grin'); wa['arm'][1].rotation_euler=(R(-95),R(-10),R(-10)); wa['arm'][-1].rotation_euler=(R(-140*tl(t,ws(296),ws(296)+.3)),0,R(-10)); face(wa,brow=.05)
        for k_ in ('al','zo','ay'): look_at(P[k_],hp(wa),.6); face(P[k_],mouth='grin')
        c0,tg,ln=closecam(wa,tseat_rz('wa'),.3,2.6,lens=34); camset(drift(c0,tg,t,.1),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['FINAL']=FINAL_
