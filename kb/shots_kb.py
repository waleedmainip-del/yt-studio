# Shots for "Karachi - People Can Never Say No To Biryani". Cuts sit on narration words (audio/words.json); SEQ is written by gen_seq.py.
SHOTS={}
END=143.5
SEQ=[('OPEN', 0.0), ('INTRO', 3.833), ('W1', 8.733), ('A1', 14.9), ('Z1', 17.0), ('AY1', 21.133), ('W2', 23.867), ('A2', 27.5), ('W3', 29.767), ('STREET', 33.133), ('W4', 36.4), ('A3', 39.6), ('BOX', 42.333), ('SMELL', 45.133), ('W5', 48.133), ('Z2', 49.233), ('W6', 50.0), ('AY2', 51.833), ('W7', 53.733), ('A4', 57.367), ('W8', 60.0), ('LAWN', 62.667), ('AY3', 65.833), ('A5', 68.633), ('GRAB', 69.4), ('W9', 72.3), ('Z3', 74.233), ('W10', 75.267), ('A6', 77.833), ('NOTICE', 80.867), ('W11', 84.567), ('AY4', 86.633), ('W12', 89.9), ('Z4', 93.1), ('W13', 95.4), ('FULL', 98.633), ('A7', 102.767), ('AY5', 104.767), ('Z5', 107.267), ('RIDER', 109.567), ('W14', 114.867), ('A8', 115.933), ('W15', 116.767), ('AY6', 118.267), ('Z6', 120.033), ('TURN', 121.867), ('W16', 123.7), ('A9', 126.133), ('PHONE', 127.8), ('MORAL', 133.567), ('FINAL', 139.0)]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0
def we(i): return W_[i]['e']-T0
def rest(H,a=6): H['arm'][1].rotation_euler=(R(-5),0,R(a)); H['arm'][-1].rotation_euler=(R(-5),0,R(-a))
def fwd(rz): return (math.sin(R(rz)),-math.cos(R(rz)))
def cwalk(H,x0,y,d,v,t,step=.55,arm=24):
    H['root'].location[0]=x0+d*v*t; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(90*d); walk(H,v*t+H['seed'],step=step,arm=arm)
def closecam(H,rz,side=.3,dist=3.0,dz=.05,tz=-.3,lens=36):
    h=hp(H); f=fwd(rz); f=(f[0],f[1]-1.2); n_=math.hypot(*f); f=(f[0]/n_,f[1]/n_); rt=(-f[1],f[0])
    return (h[0]+f[0]*dist+rt[0]*side,h[1]+f[1]*dist+rt[1]*side,h[2]+dz),(h[0],h[1],h[2]+tz),lens
NAMES={'wa':'WALEED','al':'ALI','zo':'ZOHAIB','ay':'AYESHA'}
CASTS={'wa':WALEED,'al':ALI,'zo':ZOHAIB,'ay':AYESHA}
NCOL={'wa':'#0E5C56','al':'#3A4558','zo':'#2F5A3A','ay':'#C0563A'}
def lap(H):                                                  # hands resting on thighs while seated
    m=root_mat(H)
    for s in (1,-1): arm_to(H,s,m@Vector((s*.3,-.55,.95)),1)
def tarms(H,dz=0.0):
    m=root_mat(H)
    for s in (1,-1): arm_to(H,s,m@Vector((s*.34,-.62,1.2+dz)),1)
# ================================================================ SET A: chai dhaba
def aset():
    S=dhaba_k(); P={}
    for k,p in SEATS_A.items(): P[k]=mk(CASTS[k],p[0],p[1],seat_rz(p),k)
    D=[mk(person(61+i*5),x,y,rz,'d%d'%i) for i,(x,y,rz) in enumerate(S['bg'])]
    cw=mk(CHAIWALA,2.6,6.0,0,'chaiwala'); steam((2.4,6.8,1.6),0,99,n=12,seed=4,size=.09)
    return dict(P=P,D=D,cw=cw,bg=S['bg'])
def aidle(S,t,free=()):
    for k,H in S['P'].items():
        p=SEATS_A[k]; seat(H,t+dseed(k),.58); H['root'].location[0]=p[0]; H['root'].location[1]=p[1]; H['root'].rotation_euler[2]=R(seat_rz(p)); H['head'].rotation_euler=(0,0,0)
        if k not in free: tarms(H)
    for i,H in enumerate(S['D']):
        x,y,rz=S['bg'][i]; seat(H,t+i*1.7,.58); H['root'].rotation_euler[2]=R(rz); tarms(H,.04*math.sin(t*2.4+i)); H['head'].rotation_euler=(R(4+4*math.sin(t*1.5+i*2)),0,R(12*math.sin(t*.6+i)))
        face(H,mouth='smile' if int(t*1.3+i)%3 else 'o')
    c=S['cw']; stand(c,t); blink(c,t); c['arm'][1].rotation_euler=(R(-60+12*math.sin(t*3)),0,R(10)); c['arm'][-1].rotation_euler=(R(-45),0,R(-10)); c['head'].rotation_euler=(R(14),0,0)
def atalk(key,a,b,extra=None,init=None,rest_='flat',side=.3,dist=3.0,lens=36,cam=None):
    def S_():
        S=aset(); P=S['P']
        if init: init(S)
        H=P[key]; rz=seat_rz(SEATS_A[key])
        def upd(t):
            aidle(S,t); talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k!=key: look_at(o,hp(H),.55,maxyaw=60)
            if extra: extra(S,t)
            c0,tg,ln=cam if cam else closecam(H,rz,side,dist,lens=lens); q=ease(t/DUR); c1=(L(c0[0],tg[0],.06),L(c0[1],tg[1],.06),c0[2]); camset(LV(c0,c1,q),tg,ln,2.8)
        return dict(upd=upd)
    return S_
AW=((0,-4.3,2.15),(0,.7,1.55),22)
def INTRO_():
    S=aset(); P=S['P']; T=dict(SEQ)['INTRO']
    for k,wi in (('wa',11),('al',12),('zo',13),('ay',15)):
        p=SEATS_A[k]; label(NAMES[k],(p[0]*1.05,p[1],3.0),W_[wi]['s']-T,size=.2,col='#FFFFFF',bg=NCOL[k])
    def upd(t):
        aidle(S,t,free=('wa','zo'))
        for k,H in P.items(): face(H,mouth='smile' if k!='zo' else 'grin')
        P['wa']['arm'][1].rotation_euler=(R(-80),R(-10),0); arm_to(P['wa'],-1,root_mat(P['wa'])@Vector((-.34,-.62,1.2)),1)
        P['zo']['arm'][1].rotation_euler=(R(-95+8*math.sin(t*4)),R(-8),0); arm_to(P['zo'],-1,root_mat(P['zo'])@Vector((-.34,-.62,1.2)),1)
        look_at(P['al'],hp(P['ay']),.5); look_at(P['ay'],hp(P['al']),.5)
        q=ease(t/DUR); camset(LV((1.5,-5.6,3.0),(.2,-3.7,2.2),q),LV((0,2.5,1.9),(0,.8,1.55),q),L(20,23,q),8)
    return dict(upd=upd)
SHOTS['INTRO']=INTRO_
def _w1i(S): S['b1']=bubble('Rs 10,00,000   OR   BIRYANI?',(-.92,1.0,3.05),W_[37]['s']-dict(SEQ)['W1'],size=.16,col='#FFFFFF',bg='#1E6A3A')
def _w1(S,t): H=S['P']['wa']; gest(H,t,1,.9,6,-70); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1)
def _a1(S,t): H=S['P']['al']; k=tl(t,ws(45),ws(45)+.3); H['arm'][1].rotation_euler=(R(-100*k-10),R(-15),0); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); face(H,brow=.05)
def _z1i(S): bubble('365 DAYS OF BIRYANI',(.92,1.1,3.05),W_[55]['s']-dict(SEQ)['Z1'],size=.17,col='#FFFFFF',bg='#D9811A')
def _z1(S,t): H=S['P']['zo']; gest(H,t,1,.7,5,-60); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); face(H,brow=.05,eyes=.9)
def _ay1(S,t): H=S['P']['ay']; arm_to(H,1,hp(S['P']['zo'],-.4),tl(t,ws(59),ws(59)+.3)*.9); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); face(H,brow=.03,brow_r=-6)
def _w2(S,t):
    H=S['P']['wa']; k=tl(t,ws(66),ws(66)+.18); slam=tl(t,ws(70),ws(70)+.12)
    arm_to(H,1,root_mat(H)@Vector((.3,-.6,L(1.6,1.08,slam))),1); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); face(H,brow=.06,brow_r=8)
    for k_ in ('al','zo','ay'): face(S['P'][k_],mouth='o' if t>ws(70)+.1 else 'flat',brow=.05*slam)
def _a2(S,t): H=S['P']['al']; face(H,brow=.02,brow_r=-10,eyes=.8); arm_to(H,1,H['head'].matrix_world@Vector((.4,-.3,.1)),tl(t,0,.3)*.8)
def _w3(S,t):
    H=S['P']['wa']; k=tl(t,0,.3)
    for s in (1,-1): arm_to(H,s,H['root'].matrix_world@Vector((s*.15,-.38,1.75)),k)
    H['head'].rotation_euler[0]+=R(-8*k); face(H,brow=.06)
SHOTS['W1']=atalk('wa',24,42,extra=_w1,init=_w1i)
SHOTS['A1']=atalk('al',43,46,extra=_a1,rest_='grin')
SHOTS['Z1']=atalk('zo',47,58,extra=_z1,init=_z1i,rest_='smirk')
SHOTS['AY1']=atalk('ay',59,65,extra=_ay1,rest_='smirk')
SHOTS['W2']=atalk('wa',66,71,extra=_w2,cam=((-.55,-2.2,2.05),(-.75,1.0,1.75),28))
SHOTS['A2']=atalk('al',72,77,extra=_a2)
SHOTS['W3']=atalk('wa',78,86,extra=_w3,rest_='grin')
# ================================================================ SET B: street
SPX=0.0
SP={'wa':(SPX-.3,.2),'zo':(SPX+1.6,1.0),'al':(SPX-2.1,1.7),'ay':(SPX+2.6,-.4)}
def bset(fx_=0.0,walkers_=True):
    S=street_k(fx_); P={k:mk(CASTS[k],0,0,0,k) for k in ('wa','al','zo','ay')}; S['P']=P
    S['W']=walkers(9,7,-60,60,(-2.6,2.9),z=.0) if walkers_ else []
    return S
def bstop(S,t,look_c=None):
    upd_walkers(S['W'],T0+t)
    for k,H in S['P'].items():
        x,y=SP[k]; c=look_c or (SPX,.4); H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(face_dir(c[0]-x,c[1]-y))); stand(H,t+dseed(k)); blink(H,t); rest(H); H['head'].rotation_euler=(0,0,0)
def BOXK(S):
    bx=biryani_box((0,0,0),1.0); S['bx']=bx; bx['setk']('full'); return bx
def box_in_hands(S,t,lidk=1.0):
    z=S['P']['zo']; m=root_mat(z); S['bx']['root'].matrix_world=m@Matrix.Translation(Vector((0,-.72,1.32))); S['bx']['lid'](lidk)
    for s in (1,-1): arm_to(z,s,m@Vector((s*.38,-.68,1.38)),1)
def btalk(key,a,b,extra=None,init=None,rest_='flat',side=.3,dist=2.7,lens=34,box=True,plate=False):
    def S_():
        S=bset(); P=S['P']
        if box: BOXK(S); steam((SP['zo'][0],SP['zo'][1]-.72,1.6),0,99,n=12,seed=11,size=.08)
        if plate: S['pl']=in_hand(P['wa'],1,lambda e: plate_spoon(e,1.2))
        if init: init(S)
        def upd(t):
            bstop(S,t)
            if box: box_in_hands(S,t)
            H=P[key]; talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k!=key: look_at(o,hp(H),.6,maxyaw=70)
            if plate: P['wa']['arm'][1].rotation_euler=(R(-70),R(-10),0); P['wa']['arm'][-1].rotation_euler=(R(-60),R(25),0)
            if extra: extra(S,t)
            rz=math.degrees(H['root'].rotation_euler[2]); c0,tg,ln=closecam(H,rz,side,dist,lens=lens); q=ease(t/DUR); c1=(L(c0[0],tg[0],.06),L(c0[1],tg[1],.06),c0[2]); camset(LV(c0,c1,q),tg,ln,2.8)
        return dict(upd=upd)
    return S_
def OPEN_():
    DX=7.5; S=street_k(DX); deg(DX,.15,1.25,lid=False,fire=True); B.done('hookdeg'); steam((DX,.15,1.9),0,99,n=22,seed=9,size=.14)
    P={}; HP={'al':(-2.7,1.9),'wa':(-.9,2.35),'zo':(.9,2.35),'ay':(2.7,1.9)}
    for k,(x,y) in HP.items(): P[k]=mk(CASTS[k],x+DX,y,face_dir(-x*.5,-1),k)
    W=walkers(9,7,-60,60,(2.95,))
    def upd(t):
        upd_walkers(W,T0+t)
        for k,H in P.items():
            stand(H,t+dseed(k)); blink(H,t); lean=tl(t,.6,1.6); H['root'].rotation_euler[0]=R(9*lean); look_at(H,(DX,.15,1.6),.8,maxpitch=40); face(H,mouth='o' if k in ('wa','zo') else 'grin',brow=.05,eyes=1.15)
            H['arm'][1].rotation_euler=(R(-40*lean),0,R(10)); H['arm'][-1].rotation_euler=(R(-40*lean),0,R(-10))
        q=ease(t/DUR); camset(LV((DX,-2.9,3.5),(DX,-2.3,3.1),q),LV((DX,1.3,1.5),(DX,1.3,1.55),q),24,5.6)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
WK={'wa':(0.0,.3),'ay':(.95,1.85),'al':(1.1,-1.2),'zo':(2.05,.45)}           # walking formation (x offset, lane y)
def STREET_():
    S=bset(); P=S['P']; X0=9.0
    def upd(t):
        upd_walkers(S['W'],T0+t); v=1.05
        for k,H in P.items(): dx,y=WK[k]; cwalk(H,X0+dx,y,-1,v,t+.4); blink(H,t); face(H,mouth='smile' if k!='wa' else 'smirk')
        x=P['wa']['root'].location[0]; q=ease(t/DUR); camset((x-L(5.2,4.4,q),.6,L(2.0,2.1,q)),(x+.9,.4,1.65),22,5.6)
    return dict(upd=upd)
SHOTS['STREET']=STREET_
def wtalk(key,a,b,extra=None,init=None,rest_='flat',cam2=False):
    def S_():
        S=bset(); P=S['P']; X0=4.2
        if init: init(S)
        def upd(t):
            upd_walkers(S['W'],T0+t); v=.9
            for k,H in P.items(): dx,y=WK[k]; cwalk(H,X0+dx,y,-1,v,t,step=.5); blink(H,t)
            H=P[key]; talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k!=key: look_at(o,hp(H),.45,maxyaw=60)
            if extra: extra(S,t)
            h=hp(H); camset((h[0]-2.6,h[1]-.9,h[2]+.05),(h[0]+.2,h[1]+.15,h[2]-.35),30,2.8)
        return dict(upd=upd)
    return S_
def _w4(S,t):
    H=S['P']['wa']; k=tl(t,ws(101),ws(101)+.3); H['arm'][1].rotation_euler=(R(-95*k),R(-30*k),R(20*k)); face(H,brow=.06)
def _a3(S,t): face(S['P']['al'],brow=.03,brow_r=-8,eyes=.85); S['P']['al']['head'].rotation_euler[2]+=R(6*math.sin(t*2))
SHOTS['W4']=wtalk('wa',96,106,extra=_w4,rest_='smirk')
SHOTS['A3']=wtalk('al',107,113,extra=_a3,rest_='smirk')
def BOX_():
    S=bset(); P=S['P']; BOXK(S); st=steam((SP['zo'][0],SP['zo'][1]-.72,1.6),ws(116)+.4,99,n=18,seed=11,size=.1)
    def upd(t):
        bstop(S,t); k=tl(t,ws(116),ws(116)+.5); box_in_hands(S,t,k)
        z=P['zo']; face(z,mouth='grin',brow=.04); look_at(z,(SP['zo'][0],SP['zo'][1]-.7,1.3),.8,maxpitch=40)
        for k_ in ('al','ay'): look_at(P[k_],(SP['zo'][0],SP['zo'][1]-.7,1.4),.6); face(P[k_],mouth='smile')
        q=ease(t/DUR); camset(LV((SP['zo'][0]-1.3,SP['zo'][1]-2.5,1.9),(SP['zo'][0]-1.1,SP['zo'][1]-2.1,1.85),q),(SP['zo'][0],SP['zo'][1]-.6,1.5),32,4)
    return dict(upd=upd)
SHOTS['BOX']=BOX_
def SMELL_():
    S=bset(); P=S['P']; BOXK(S); X0=-.3+.9*1.6
    puff_t=ws(121)
    for i in range(5): puff((SP['zo'][0]-.2-i*.35,SP['zo'][1]-.75-i*.12,1.7+i*.12),puff_t+i*.12,size=.1,n=4,col=M('#F4F1EA',.6,alpha=.6),rise=.15,life=1.2,seed=20+i)
    def upd(t):
        bstop(S,t); box_in_hands(S,t,1.0); wa=P['wa']
        k=tl(t,0,ws(124)); stopk=ease(k)
        x=L(SP['wa'][0]-1.7,SP['wa'][0],stopk); wa['root'].location[0]=x; wa['root'].rotation_euler[2]=R(lerp_angle(90,face_dir(SP['zo'][0]-x,SP['zo'][1]-.2),tl(t,ws(124),ws(125))))
        if t<ws(124): walk(wa,1.7*stopk+wa['seed'],step=.5,arm=20)
        sn=tl(t,ws(121),ws(122)+.3); wa['head'].rotation_euler=(R(-14*sn),0,R(-25*sn)); face(wa,mouth='o' if sn>.5 else 'flat',brow=.06*sn,eyes=L(1,.7,sn))
        q=ease(t/DUR); h=hp(wa); camset((h[0]+2.3,h[1]-1.9,h[2]+.05),(h[0]+.2,h[1],h[2]-.35),30,2.8)
    return dict(upd=upd)
SHOTS['SMELL']=SMELL_
def _w5(S,t): H=S['P']['wa']; H['arm'][1].rotation_euler=(R(-80),0,R(40)); face(H,brow=.06,eyes=1.2)
def _w6(S,t): H=S['P']['wa']; look_at(H,(SP['zo'][0],SP['zo'][1]-.7,1.35),.9,maxpitch=40); face(H,brow=.06,eyes=1.25); H['root'].rotation_euler[0]=R(8)
def _ay2(S,t): H=S['P']['ay']; arm_to(H,1,hp(S['P']['wa'],-.5),tl(t,ws(133),ws(133)+.25)); face(H,brow=.05,brow_r=-8)
def _w7(S,t): face(S['P']['wa'],brow=.05,brow_r=6)
def _a4(S,t): H=S['P']['al']; arm_to(H,1,hp(S['P']['wa'],-.7),tl(t,ws(155),ws(155)+.25)*.9); face(H,brow=.03,brow_r=-10,eyes=.85)
def _w8(S,t): H=S['P']['wa']; H['root'].rotation_euler[0]=R(-5); H['head'].rotation_euler[0]+=R(-10); face(H,brow=.06,brow_r=10)
SHOTS['W5']=btalk('wa',126,126,extra=_w5,rest_='o',dist=2.5)
SHOTS['Z2']=btalk('zo',127,128,rest_='flat')
SHOTS['W6']=btalk('wa',129,132,extra=_w6,rest_='o',dist=2.5)
SHOTS['AY2']=btalk('ay',133,140,extra=_ay2)
SHOTS['W7']=btalk('wa',141,154,extra=_w7,rest_='smile',plate=True)
SHOTS['A4']=btalk('al',155,161,extra=_a4,rest_='smirk',plate=True)
SHOTS['W8']=btalk('wa',162,168,extra=_w8,rest_='flat',plate=True)
# ================================================================ SET C: night lawn
def cpos(k):
    x,y,rz=SEATS_C[k]
    return x,y,(rz if rz is not None else face_dir(BX[0]-x,BX[1]-1.0-y))
def cset(stage='full',fx_=0.0):
    lawn_k(fx_); P={}
    for k in SEATS_C: x,y,rz=cpos(k); P[k]=mk(CASTS[k],x,y,rz,k)
    bx=biryani_box((BX[0],BX[1],.76),.85); bx['setk'](stage); bx['lid'](1.45)
    G=[]
    for i,(gx,gy) in enumerate(((-11,9.95),(5.5,9.95),(11,9.95))): G.append((mk(person(80+i*7),gx,gy,180,'g%d'%i),gx,gy))
    W=walkers(6,11,-40,40,(8.9,),z=.02)
    return dict(P=P,bx=bx,G=G,W=W)
def cidle(S,t,free=()):
    upd_walkers(S['W'],T0+t)
    for k,H in S['P'].items():
        x,y,rz=cpos(k); seat(H,t+dseed(k),.6); H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(rz); H['head'].rotation_euler=(0,0,0)
        if k not in free: lap(H)
    for i,(H,gx,gy) in enumerate(S['G']):
        seat(H,t+i,.62); H['root'].location=(gx,gy+.05,H['root'].location[2]); lap(H); H['head'].rotation_euler=(0,0,R(14*math.sin(t*.7+i))); face(H,mouth='smile')
def eat(H,t,ph=0.0,box_=BX):
    m=root_mat(H); c=math.sin(t*6+ph); tgt=Vector((box_[0],box_[1],1.0)) if c>0 else m@Vector((.08,-.25,2.05))
    arm_to(H,1,Vector(tgt).lerp(m@Vector((.08,-.25,2.05)),.5+.5*math.cos(t*6+ph)),1); arm_to(H,-1,m@Vector((-.3,-.55,.95)),1)
def ctalk(stage,key,a,b,extra=None,init=None,rest_='flat',side=.3,dist=3.0,lens=36,cam=None,free=()):
    def S_():
        S=cset(stage); P=S['P']
        if init: init(S)
        H=P[key]; rz=cpos(key)[2]
        def upd(t):
            cidle(S,t,free=free); talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k!=key: look_at(o,hp(H),.55,maxyaw=70)
            if extra: extra(S,t)
            c0,tg,ln=cam if cam else closecam(H,rz,side,dist,lens=lens); q=ease(t/DUR); c1=(L(c0[0],tg[0],.06),L(c0[1],tg[1],.06),c0[2]); camset(LV(c0,c1,q),tg,ln,2.8)
        return dict(upd=upd)
    return S_
CW=((0,-4.6,2.2),(0,.9,1.45),23)
def LAWN_():
    S=cset('full'); P=S['P']; steam((BX[0],BX[1],.95),0,99,n=14,seed=12,size=.08)
    def upd(t):
        cidle(S,t)
        for k,H in P.items(): look_at(H,(BX[0],BX[1],.9),.7,maxpitch=40); face(H,mouth='grin',brow=.04)
        q=ease(t/DUR); camset(LV((5.5,-7.5,4.6),(1.2,-4.6,2.4),q),LV((0,6,4),(0,.9,1.45),q),L(19,22,q),8)
    return dict(upd=upd)
SHOTS['LAWN']=LAWN_
def _ay3(S,t): H=S['P']['ay']; gest(H,t,-1,.5,5,-45); face(H,brow=.04)
def _a5(S,t): H=S['P']['al']; H['arm'][1].rotation_euler=(R(-95),R(-20),R(10)); face(H,mouth='smile')
SHOTS['AY3']=ctalk('full','ay',177,184,extra=_ay3,free=('ay',))
SHOTS['A5']=ctalk('full','al',185,185,extra=_a5,free=('al',),rest_='smile')
def GRAB_():
    S=cset('full'); P=S['P']; bx=S['bx']; z=P['zo']; mw=bx['big'].matrix_world.copy()
    def upd(t):
        cidle(S,t,free=('zo',)); k=tl(t,.5,1.2); back=tl(t,1.3,2.0)
        bp=Vector(bx['root'].matrix_world@Vector((-.18,.06,.19)))
        hand=bp.lerp(root_mat(z)@Vector((.2,-.45,1.35)),back); arm_to(z,1,bp if k<1 else hand,k); arm_to(z,-1,root_mat(z)@Vector((-.3,-.55,.95)),1)
        if back>0: bx['big'].matrix_world=Matrix.Translation(hand+Vector((0,0,.05)))
        look_at(z,hp(P['wa']),.4*(1-back)); face(z,mouth='smirk',brow=.03); look_at(z,(BX[0],BX[1],.9),.8*back)
        for k_ in ('wa','al','ay'): look_at(P[k_],(BX[0],BX[1],.9),.5); face(P[k_],mouth='smile')
        q=ease(t/DUR); camset(LV((1.3,-1.4,1.8),(1.15,-1.15,1.75),q),(.15,.6,1.05),34,2.8)
    return dict(upd=upd)
SHOTS['GRAB']=GRAB_
def _hold_big(S):
    z=S['P']['zo']; S['bx']['setk']('grab'); S['chk']=in_hand(z,1,lambda e: (oico((0,-.1,.05),.11,M('#9A4A1E',.55),e,sc=(1.3,1,.8),sub=2),ocyl((.14,-.1,.05),.02,.16,M('#F4EEE0',.5),e,rot=(0,R(90),0),seg=6)))
def _zh(S,t): z=S['P']['zo']; arm_to(z,1,root_mat(z)@Vector((.2,-.5,1.45)),1); arm_to(z,-1,root_mat(z)@Vector((-.3,-.55,.95)),1)
def _w9(S,t): H=S['P']['wa']; arm_to(H,1,hp(S['P']['zo'],-.6),tl(t,ws(194),ws(194)+.15)); face(H,brow=.06,brow_r=12,eyes=1.15); _zh(S,t)
def _z3(S,t): _zh(S,t); face(S['P']['zo'],brow=.02)
def _w10(S,t): H=S['P']['wa']; gest(H,t,-1,1.0,8,-80); arm_to(H,1,hp(S['P']['zo'],-.6),1); face(H,brow=.06,brow_r=12); _zh(S,t)
def _a6(S,t): H=S['P']['al']; k=tl(t,0,.3)
SHOTS['W9']=ctalk('grab','wa',194,200,extra=_w9,init=_hold_big,free=('wa','zo'),rest_='O')
SHOTS['Z3']=ctalk('grab','zo',201,202,extra=_z3,init=_hold_big,free=('zo',),rest_='smirk')
SHOTS['W10']=ctalk('grab','wa',203,209,extra=_w10,init=_hold_big,free=('wa','zo'),rest_='O')
def _a6(S,t):
    H=S['P']['al']; k=tl(t,0,.3)
    for s in (1,-1): arm_to(H,s,root_mat(H)@Vector((s*.45,-.7,1.25+.08*math.sin(t*5))),k)
    _zh(S,t)
SHOTS['A6']=ctalk('grab','al',210,216,extra=_a6,init=_hold_big,free=('al','zo'))
def NOTICE_():
    S=cset('noaaloo'); P=S['P']; wa=P['wa']
    def upd(t):
        cidle(S,t); look_at(wa,(BX[0],BX[1],.9),.9,maxpitch=40); k=tl(t,ws(219),ws(219)+.5); face(wa,mouth='flat' if k<.6 else 'o',brow=.06*k,eyes=L(1,1.25,k))
        if t<ws(220)-.1: camset(LV((-.3,-.9,2.05),(-.3,-.75,1.95),ease(t/max(.1,ws(220)))),(BX[0],BX[1]+.1,.85),40,2.8)
        else:
            q=tl(t,ws(220),DUR); h=hp(wa); camset(LV((h[0]+.1,h[1]-1.9,h[2]),(h[0]+.05,h[1]-1.3,h[2]),q),(h[0],h[1],h[2]-.32),36,2.8)
    return dict(upd=upd)
SHOTS['NOTICE']=NOTICE_
def _noal(S): S['bx']['setk']('noaaloo')
def _w11(S,t):
    H=S['P']['wa']; k=tl(t,0,.2)
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-8*k),0,R(s*150*k))
    H['head'].rotation_euler[0]+=R(-12*k); face(H,brow=.06,brow_r=14,eyes=1.3)
    for k_ in ('al','zo','ay'): face(S['P'][k_],mouth='o',eyes=1.2,brow=.06)
def _ay4(S,t): H=S['P']['ay']; gest(H,t,-1,.6,6,-50); face(H,brow=.04,brow_r=-10)
def _w12(S,t):
    H=S['P']['wa']; k=tl(t,0,.3)
    for s in (1,-1): arm_to(H,s,H['root'].matrix_world@Vector((s*.12,-.38,1.72)),k)
    face(H,brow=.06,brow_r=14,eyes=.8)
def _z4(S,t): laugh(S['P']['zo'],t,.8); face(S['P']['zo'],mouth='grin')
def _w13(S,t): H=S['P']['wa']; H['arm'][1].rotation_euler=(R(-80),0,R(-10)); H['root'].rotation_euler[0]=R(6); face(H,brow=-.03,brow_r=-6,eyes=.85)
SHOTS['W11']=ctalk('noaaloo','wa',224,228,extra=_w11,init=_noal,free=('wa',),rest_='O',cam=((-.6,-1.4,2.05),(-.92,1.55,1.95),30))
SHOTS['AY4']=ctalk('noaaloo','ay',229,240,extra=_ay4,free=('ay',))
SHOTS['W12']=ctalk('noaaloo','wa',241,250,extra=_w12,free=('wa',))
SHOTS['Z4']=ctalk('noaaloo','zo',251,257,extra=_z4,free=('zo',),rest_='grin')
SHOTS['W13']=ctalk('noaaloo','wa',258,265,extra=_w13,free=('wa',),dist=2.5)
def FULL_():
    S=cset('empty'); P=S['P']
    def upd(t):
        cidle(S,t)
        for i,(k,H) in enumerate(P.items()):
            H['root'].rotation_euler[0]=R(-9*tl(t,.2,1.0)); face(H,mouth='smile',brow=0,eyes=.75); H['head'].rotation_euler=(R(-8),0,R(5*math.sin(t+i)))
            for s in (1,-1): arm_to(H,s,root_mat(H)@Vector((s*.15,-.42,1.28)),1)
        q=ease(t/DUR); camset(LV(CW[0],(0,-3.9,2.1),q),CW[1],CW[2],5.6)
    return dict(upd=upd)
SHOTS['FULL']=FULL_
def _full(S,t):
    for k,H in S['P'].items(): H['root'].rotation_euler[0]=R(-9); face(H,eyes=.8)
def _a7(S,t): _full(S,t); H=S['P']['al']; arm_to(H,1,root_mat(H)@Vector((.15,-.42,1.28)),1)
def _ay5(S,t): _full(S,t); H=S['P']['ay']; gest(H,t,1,.6,4,-60)
def _z5(S,t): _full(S,t); H=S['P']['zo']; H['root'].rotation_euler[0]=R(-14); face(H,mouth='strain',eyes=.6)
SHOTS['A7']=ctalk('empty','al',276,279,extra=_a7,free=('al',),rest_='smile')
SHOTS['AY5']=ctalk('empty','ay',280,284,extra=_ay5,free=('ay',))
SHOTS['Z5']=ctalk('empty','zo',285,292,extra=_z5,rest_='strain')
def RIDER_():
    S=cset('empty'); P=S['P']; mb,R_=rider_bike(RIDER); T=DUR
    def upd(t):
        cidle(S,t); x=L(9.5,-9.5,t/T); mb['root'].location=(x,RIDER_Y,0)
        for w_ in mb['wheels']: w_.rotation_euler[1]=-(9.5-x)/(.32*1.4)
        seat(R_,t,1.05); R_['root'].location=(x+.15,RIDER_Y,R_['root'].location[2]); R_['root'].rotation_euler=(0,0,R(-90)); arm_to(R_,1,(x-.95,RIDER_Y-.45,1.7),1); arm_to(R_,-1,(x-.95,RIDER_Y+.45,1.7),1)
        for k,H in P.items(): look_at(H,(x,RIDER_Y,1.4),tl(t,.3,1.0)*.95,maxyaw=85); face(H,mouth='o',eyes=1.15,brow=.05)
        q=ease(t/DUR); tx=max(-2.2,min(2.2,x*.4)); camset((tx*.3,-3.4,1.95),(tx,4.0,1.55),22,5.6)
    return dict(upd=upd)
SHOTS['RIDER']=RIDER_
def _lookR(S,t):
    for k,H in S['P'].items():
        if k!='wa': pass
def _w14(S,t): H=S['P']['wa']; H['arm'][1].rotation_euler=(R(-85),R(-30),R(-25)); look_at(H,(-8,RIDER_Y,1.4),.6,maxyaw=85); face(H,eyes=1.15)
def _a8(S,t): H=S['P']['al']; H['arm'][1].rotation_euler=(R(-90),0,R(30)); face(H,brow=.05,brow_r=-12)
def _w15(S,t): H=S['P']['wa']; gest(H,t,1,.7,5,-75); face(H,brow=.06,brow_r=10)
def _ay6(S,t): H=S['P']['ay']; H['arm'][-1].rotation_euler=(R(-70*tl(t,ws(311),ws(311)+.2)),0,R(-25)); face(H,brow=.05,brow_r=-12,eyes=.8)
def _z6(S,t): H=S['P']['zo']; H['arm'][1].rotation_euler=(R(-60),0,R(10)); face(H,brow=.06,eyes=1.1); H['head'].rotation_euler[1]+=R(6)
SHOTS['W14']=ctalk('empty','wa',304,304,extra=_w14,free=('wa',),rest_='flat',dist=2.5)
SHOTS['A8']=ctalk('empty','al',305,305,extra=_a8,free=('al',))
SHOTS['W15']=ctalk('empty','wa',306,310,extra=_w15,free=('wa',))
SHOTS['AY6']=ctalk('empty','ay',311,314,extra=_ay6,free=('ay',))
SHOTS['Z6']=ctalk('empty','zo',315,319,extra=_z6,free=('zo',),rest_='smile')
def TURN_():
    S=cset('empty'); P=S['P']
    def upd(t):
        cidle(S,t); k=tl(t,.1,.35)
        for k_ in ('wa','al','ay'): look_at(P[k_],hp(P['zo']),k,maxyaw=85); face(P[k_],mouth='o',eyes=1.2,brow=.05)
        face(P['zo'],mouth='smile',brow=.03); look_at(P['zo'],(0,-4,2.0),.5)
        q=ease(t/DUR); camset(LV((1.2,-2.2,2.0),(1.1,-1.6,1.98),q),(.92,1.55,1.95),30,4)
    return dict(upd=upd)
SHOTS['TURN']=TURN_
def _w16(S,t):
    H=S['P']['wa']; arm_to(H,1,hp(S['P']['zo'],-.6),tl(t,0,.3)*.8); face(H,brow=.06)
def _a9(S,t):
    H=S['P']['al']
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-10),0,R(s*120*tl(t,0,.25)))
    face(H,brow=.05,brow_r=14)
SHOTS['W16']=ctalk('empty','wa',324,329,extra=_w16,free=('wa',),rest_='grin')
SHOTS['A9']=ctalk('empty','al',330,333,extra=_a9,free=('al',),rest_='O')
def PHONE_():
    S=cset('empty'); P=S['P']; al=P['al']; ph=phone(al,1); T=dict(SEQ)['PHONE']
    bubble('EXTRA LARGE BIRYANI  x1   ORDERED!',(-1.5,.2,2.95),W_[343]['s']-T,size=.13,col='#FFFFFF',bg='#D9811A')
    def upd(t):
        cidle(S,t,free=('al',)); k=tl(t,.2,.7); ph.scale=(k,k,k); hold_phone(al,1,k); arm_to(al,-1,root_mat(al)@Vector((-.3,-.55,.95)),1)
        if t>ws(339): talk(al,t,*wt(339,348),rest='flat')
        look_at(al,al['arm'][1].matrix_world@Vector(hand_loc(al,1)),.8*k,maxpitch=30); face(al,brow=.04,brow_r=10)
        for k_ in ('wa','zo','ay'): look_at(P[k_],hp(al),.7); face(P[k_],mouth='grin' if k_!='ay' else 'smile',brow=.04)
        c0,tg,ln=closecam(al,cpos('al')[2],.2,2.7,lens=34); q=ease(t/DUR); camset(LV(c0,(L(c0[0],tg[0],.06),L(c0[1],tg[1],.06),c0[2]),q),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['PHONE']=PHONE_
def MORAL_():
    S=cset('empty'); P=S['P']
    def upd(t):
        cidle(S,t)
        for k,H in P.items(): face(H,mouth='smile'); look_at(H,(0,.4,1.6),.3)
        q=ease(t/DUR); camset(LV((0,-4.0,2.1),(0,-11.5,9.5),q),LV((0,.9,1.5),(0,16,9),q),L(23,21,q),8)
    return dict(upd=upd)
SHOTS['MORAL']=MORAL_
def FINAL_():
    S=cset('empty'); P=S['P']; T=dict(SEQ)['FINAL']; tb=ws(370)
    sparkles((0,1.0,2.6),1.8,tb,tb+3,n=46,size=.05,seed=13,rise=.8,mat=M('#F2C45A',.4,emit=1.5))
    def upd(t):
        cidle(S,t,free=('wa','al','zo','ay') if t>tb-.1 else ('wa',)); wa=P['wa']
        if t<tb-.1:
            talk(wa,t,*wt(363,369),rest='grin'); gest(wa,t,1,.8,6,-90); look_at(wa,(0,-4,2.0),.6); face(wa,brow=.05)
            for k_ in ('al','zo','ay'): look_at(P[k_],hp(wa),.6); face(P[k_],mouth='grin')
            q=ease(t/max(.1,tb)); h=hp(wa); camset(LV((h[0]+.25,h[1]-1.9,h[2]),(h[0]+.2,h[1]-1.6,h[2]),q),(h[0],h[1],h[2]-.3),34,2.8)
        else:
            k=tl(t,tb-.1,tb+.15)
            for i,(k_,H) in enumerate(P.items()):
                for s in (1,-1): H['arm'][s].rotation_euler=(R(-10*k),0,R(s*(150+8*math.sin(t*9+i))*k))
                H['head'].rotation_euler[0]=R(-10*k); face(H,mouth='shout',brow=.06,eyes=1.15); look_at(H,(0,-4,2.2),.5)
            if t>ws(370): talk(P['wa'],t,*wt(370,370),rest='grin')
            q=ease(tl(t,tb,DUR)); camset(LV(CW[0],(0,-5.6,2.4),q),CW[1],CW[2],5.6)
    return dict(upd=upd)
SHOTS['FINAL']=FINAL_
