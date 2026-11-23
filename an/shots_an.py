# Shots for the "every city" announcement (Instagram story). Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=23.9
SEQ=[('HOOK',0.0),('COMMENTS',3.95),('KAB',6.5),('FIKAR',8.92),('MAP',10.1),('HAR',14.85),('FARMAISH',16.5),('LIKHO',18.8),('DM',20.8)]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0          # word start, local to the shot
ALLC=list(CITY.keys())
def room(lit=None):
    """lit: None = all pins on; or dict city->local time it switches on"""
    pins=map_room(); H=mk(HOST,0,-.1,0,'host'); ph=phone(H,1); ph.scale=(0,0,0)
    def idle(t,stand_=True):
        if stand_: stand(H,t)
        blink(H,t)
        for k in ALLC:
            on=1.0 if lit is None else (pop(t-lit[k]) if k in lit else 0.0); pin_set(pins,k,on,t)
    return dict(H=H,pins=pins,ph=ph,idle=idle)
def HOOK_():
    S=room(); H=S['H']
    def upd(t):
        S['idle'](t); talk(H,t,*wt(0,10)); face(H,mouth=None,brow=.07)
        w=math.sin(t*9); H['arm'][1].rotation_euler=(R(-158),R(-12+16*w),0); H['arm'][-1].rotation_euler=(R(-10),0,R(10))
        q=ease(t/DUR); camset(LV((0,-10.0,3.5),(0,-8.2,3.0),q),(0,2.5,3.4),24,8)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK_
def COMMENTS_():
    S=room(); H=S['H']; b=bubble('99+ COMMENTS',(-.95,-.7,2.95),.5,size=.15,col='#FFFFFF',bg='#E8301A')
    def upd(t):
        S['idle'](t); S['ph'].scale=(1,1,1); hold_phone(H,1,1); look_at(H,hand_w(H,1),.8); face(H,mouth='O',brow=.08,eyes=1.1)
        q=ease(t/DUR); camset(LV((1.5,-3.6,2.25),(1.2,-3.2,2.25),q),hp(H,-.25),32,4)
    return dict(upd=upd)
SHOTS['COMMENTS']=COMMENTS_
def hand_w(H,s): return H['arm'][s].matrix_world@Vector(hand_loc(H,s))
def KAB_():
    S=room(); H=S['H']; P=((-1.0,-.6,3.1),(1.0,-.6,2.85),(-1.0,-.6,2.5))
    for i,(txt,wi) in enumerate((('KARACHI KAB?',20),('QUETTA KAB?',22),('SIALKOT KAB?',24))): bubble(txt,P[i],W_[wi]['s']-SEQ[2][1],size=.15,col='#16171C',bg='#FFFFFF')
    def upd(t):
        S['idle'](t); k=0 if t<ws(22) else (1 if t<ws(24) else 2); look_at(H,P[k],.75,maxyaw=55); face(H,mouth='O' if k<2 else 'flat',brow=.09 if k<2 else -.03,brow_r=0 if k<2 else -10)
        g=tl(t,ws(24),ws(24)+.35); H['arm'][1].rotation_euler=(R(-10-60*g),0,R(-12-20*g)); H['arm'][-1].rotation_euler=(R(-10-60*g),0,R(12+20*g))
        q=ease(t/DUR); camset(LV((.2,-5.3,2.3),(.1,-5.0,2.3),q),hp(H,.2),28,5.6)
    return dict(upd=upd)
SHOTS['KAB']=KAB_
def FIKAR_():
    S=room(); H=S['H']
    def upd(t):
        S['idle'](t); talk(H,t,*wt(26,28),rest='grin'); face(H,brow=.05); k=tl(t,0,.3)
        arm_to(H,1,(.85,-1.0,1.5+.04*math.sin(t*10)),k); H['arm'][-1].rotation_euler=(R(-8),0,R(8)); H['head'].rotation_euler[2]=R(7*math.sin(t*7))
        q=ease(t/DUR); camset(LV((-.7,-3.3,2.15),(-.6,-3.0,2.15),q),hp(H,-.05),38,2.8)
    return dict(upd=upd)
SHOTS['FIKAR']=FIKAR_
MAPL=(('LAHORE',29,(2.05,4.5)),('KARACHI',31,(-1.7,2.78)),('PESHAWAR',33,(-1.0,5.3)),('QUETTA',34,(-1.75,4.2)),('MULTAN',35,(2.0,3.88)),('SMALL',36,(1.0,2.8)))
def MAP_():
    lit={k:W_[wi]['s']-SEQ[4][1] for k,wi,_ in MAPL}; S=room(lit); H=S['H']
    for k,wi,(lx,lz) in MAPL:
        nm='AAP KA SHEHAR' if k=='SMALL' else k; bubble(nm,(lx,WALLY-.5,lz),lit[k]+.1,size=.26 if k!='SMALL' else .22,col='#16171C' if k!='SMALL' else '#FFFFFF',bg='#FFD23F' if k!='SMALL' else '#FF4F8B')
    sparkles(mp(*CITY['SMALL']),.5,lit['SMALL'],lit['SMALL']+1.4,n=22,size=.05,seed=4)
    def upd(t):
        S['idle'](t,False); H['root'].location=(1.35,.2,0); facep(H,(.3,3.0),.3,cam=(.1,-6)); blink(H,t); legs0(H)
        cur=[k for k,_,_ in MAPL if t>=lit[k]]; k=cur[-1] if cur else 'LAHORE'; tg=Vector(mp(*CITY[k])); pr=Vector(mp(*CITY[cur[-2]])) if len(cur)>1 else tg
        p=pr.lerp(tg,ease((t-lit[k])/.3)) if cur else tg; arm_to(H,-1,p,1); H['arm'][1].rotation_euler=(R(-6),0,R(-6)); (arm_to(H,1,p,1), H['arm'][-1].__setattr__('rotation_euler',(R(-6),0,R(6)))); look_at(H,p,.7,maxyaw=50); talk(H,t,*wt(29,41)); face(H,brow=.05)
        q=ease(t/DUR); camset(LV((.1,-6.0,3.3),(.1,-5.4,3.4),q),(.1,3,3.7),26,8)
    return dict(upd=upd)
SHOTS['MAP']=MAP_
def HAR_():
    S=room({k:.04*i for i,k in enumerate(ALLC)}); H=S['H']; sparkles((0,WALLY-.5,4.0),2.2,.1,1.7,n=60,size=.06,seed=9)
    def upd(t):
        S['idle'](t); talk(H,t,*wt(42,46),rest='grin'); face(H,brow=.07); k=tl(t,0,.3); w=math.sin(t*10)*8
        arm_to(H,1,(1.25,-.25,3.35+.01*w),k); arm_to(H,-1,(-1.25,-.25,3.35-.01*w),k); H['root'].location[2]=.12*abs(math.sin(t*6.5))*k
        q=ease(t/DUR); camset(LV((-1.9,-6.6,1.5),(-1.5,-6.0,1.6),q),(0,2.2,3.5),22,8)
    return dict(upd=upd)
SHOTS['HAR']=HAR_
def FARMAISH_():
    S=room(); H=S['H']; hearts(lambda t: hp(H,.75),.3,2.2,n=9,seed=3,size=1.1,rise=1.2)
    def upd(t):
        S['idle'](t); talk(H,t,*wt(47,52),rest='smile'); face(H,brow=.04,eyes=.85); arm_to(H,1,H['root'].matrix_world@Vector((.05,-.3,3.05*H['u'])),tl(t,0,.35),base=(0,0,0)); H['arm'][-1].rotation_euler=(R(-8),0,R(8))
        H['head'].rotation_euler[0]=R(4*math.sin(t*3))
        q=ease(t/DUR); camset(LV((.75,-3.1,2.2),(.6,-2.8,2.2),q),hp(H,0),40,2.8)
    return dict(upd=upd)
SHOTS['FARMAISH']=FARMAISH_
def LIKHO_():
    S=room(); H=S['H']; label('COMMENT KAREIN',(0,-.7,3.5),.3,size=.24,col='#16171C',bg='#FFD23F'); label('APNE SHEHAR KA NAAM',(0,-.7,2.98),.75,size=.2,col='#16171C',bg='#FFFFFF')
    def upd(t):
        S['idle'](t); talk(H,t,*wt(53,61)); face(H,brow=.05); b=.05*math.sin(t*9)
        arm_to(H,1,(.55,-1.0,1.25+b),tl(t,.1,.4)); arm_to(H,-1,(-.55,-1.0,1.25-b),tl(t,.1,.4))
        q=ease(t/DUR); camset(LV((.3,-5.3,2.35),(.2,-4.9,2.35),q),hp(H,.45),28,5.6)
    return dict(upd=upd)
SHOTS['LIKHO']=LIKHO_
def DM_():
    S=room(); H=S['H']; title_card('PAID PROMOTION?',.35,(0,-.7,3.55),.3); label('DM @INRBLXWORLD',(0,-.7,2.98),ws(67),size=.2,col='#FFFFFF',bg='#FF4F8B')
    def upd(t):
        S['idle'](t); talk(H,t,*wt(62,68),rest='grin'); face(H,brow=.06); S['ph'].scale=(1,1,1); k=tl(t,.1,.45)
        arm_to(H,1,(.85,-.75,1.7+.03*math.sin(t*6)),k,base=(0,0,0)); H['arm'][-1].rotation_euler=(R(-8),0,R(8)); H['head'].rotation_euler[2]=R(-6*k)
        q=ease(t/DUR); camset(LV((-.5,-5.4,2.4),(-.25,-4.5,2.45),q),hp(H,.45),28,5.6)
    return dict(upd=upd)
SHOTS['DM']=DM_
