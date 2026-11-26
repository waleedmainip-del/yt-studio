# India vs Pakistan (project ipk) - shots part 1
SEQ=[('HOOK', 0.0), ('VSI', 4.067), ('VSP', 4.733), ('STOPS', 6.167), ('ROADS', 9.0), ('SHOPS', 10.233), ('WEDDING', 11.5), ('DULHA', 12.967), ('LASTOVER', 14.1), ('LAHORE', 16.133), ('RULEP', 18.867), ('DELHI', 21.067), ('RULEI', 23.867), ('ONEDAD', 26.067), ('SAMESOFA', 27.933), ('SAMECHAI', 28.933), ('SAMOSA', 29.9), ('NEIGHBOR', 31.1), ('HATES', 34.367), ('SATDOWN', 35.933), ('FOURHRS', 38.133), ('WASHROOM', 39.967), ('BAITHO', 41.6), ('CUP', 44.167), ('CANT', 46.733), ('THANDI', 49.233), ('PLEASE', 51.367), ('JABTAK', 53.067), ('SECRET', 55.7), ('FRIENDS', 57.933), ('GAYE', 60.1), ('SAPNE', 61.633), ('KISSE', 62.867), ('KOINAHI', 64.233), ('LASTOV', 65.567), ('ONEBALL', 67.267), ('BREATH', 69.933), ('BOWLER', 72.2), ('LIGHT', 73.733), ('BUFFERTV', 75.933), ('BUFFER', 76.9), ('PROBLEM', 79.0), ('TERE', 83.767), ('NAHI', 85.167), ('NAHI2', 86.6), ('HEARD', 87.567), ('STREETP', 89.067), ('STREETI', 90.2), ('SOMETHING', 91.267), ('KYAP', 93.767), ('KYAI', 94.633), ('BACK', 95.633), ('STREAM', 96.867), ('SCREEN', 98.2), ('TIED', 99.433), ('FAINTP', 101.633), ('FAINTI', 102.633), ('SAMETIME', 103.7), ('PHIRSE', 105.1), ('PHIRSE2', 106.8), ('SATBACK', 107.767), ('SEATS', 109.433), ('NOBODY', 111.433), ('BOWLER2', 112.633), ('LIGHT2', 114.133), ('CTA', 115.0)]
END=120.3
WI={'HOOK': 0, 'VSI': 10, 'VSP': 11, 'STOPS': 13, 'ROADS': 20, 'SHOPS': 23, 'WEDDING': 26, 'DULHA': 29, 'LASTOVER': 32, 'LAHORE': 38, 'RULEP': 45, 'DELHI': 51, 'RULEI': 59, 'ONEDAD': 65, 'SAMESOFA': 69, 'SAMECHAI': 71, 'SAMOSA': 73, 'NEIGHBOR': 75, 'HATES': 84, 'SATDOWN': 87, 'FOURHRS': 94, 'WASHROOM': 99, 'BAITHO': 101, 'CUP': 109, 'CANT': 118, 'THANDI': 127, 'PLEASE': 132, 'JABTAK': 134, 'SECRET': 144, 'FRIENDS': 151, 'GAYE': 155, 'SAPNE': 160, 'KISSE': 163, 'KOINAHI': 169, 'LASTOV': 172, 'ONEBALL': 176, 'BREATH': 183, 'BOWLER': 188, 'LIGHT': 192, 'BUFFERTV': 198, 'BUFFER': 201, 'PROBLEM': 206, 'TERE': 220, 'NAHI': 225, 'NAHI2': 228, 'HEARD': 229, 'STREETP': 233, 'STREETI': 235, 'SOMETHING': 236, 'KYAP': 242, 'KYAI': 244, 'BACK': 246, 'STREAM': 250, 'SCREEN': 254, 'TIED': 258, 'FAINTP': 262, 'FAINTI': 264, 'SAMETIME': 266, 'PHIRSE': 270, 'PHIRSE2': 273, 'SATBACK': 275, 'SEATS': 279, 'NOBODY': 283, 'BOWLER2': 285, 'LIGHT2': 289, 'CTA': 290}
SHOTS={}
# ---------------------------------------------------------------- shared staging
def room_set(side,who='dbmg',tvwall=False):
    Hm=home(side,0.0,tvwall=tvwall); home_world(); F=family(side,0.0,who); FILLE[0]=16; return Hm,F
def dh_set(who='db'):
    P,I=dollhouse(); FP=family('P',0.0,who); FI=family('I',UPZ,who); FILLE[0]=0; return P,I,FP,FI
def cam_wide(k=0.0): camset(LV((-4.05,-5.3,3.1),(-3.9,-5.0,3.05),k),(.55,.8,1.1),22,8)
def cam_two(k=0.0,dx=0.0,tx=0.0): camset(LV((dx,-4.9,2.1),(dx,-4.5,2.05),k),(tx,1.55,1.75),27,8)
def cam_one(H,k=0.0,side=.25,dist=3.5,lens=34,dz=.1,tz=-.25):
    h=hp(H); camset((h[0]+side,h[1]-dist+.3*k,h[2]+dz),(h[0],h[1],h[2]+tz),lens,8)
def finger(H,t,s=1,k=1.0,wag=1.0):
    """index-finger-up warning arm (raised forward-up, wagging)"""
    H['arm'][s].rotation_euler=(R((-138+7*math.sin(t*11)*wag)*k),R(s*24*k),0)
# ---------------------------------------------------------------- 1  HOOK: normal ... except for one day
def HOOK():
    P,I,FP,FI=dh_set(); ph=[phone_of(FP['b'],1),phone_of(FI['b'],1)]; t1=ws(6)-.08
    def upd(t):
        on=1 if t>=t1 else 0
        for Hm,F,d in ((P,FP,0.0),(I,FI,.07)):
            home_lights(Hm,t,power=1.0,tv=.12+.88*on,flick=on); fam_idle(F,t,'calm'); dad,boy=F['d'],F['b']
            if not on:
                crossed(dad); phone_up(boy,1,1.0,h=3.3,fw=1.3); look_at(boy,handw(boy,1),1.0,maxpitch=20)
            else:
                cheer(dad,t,t1+d); cheer(boy,t,t1+.1+d,ph=1.3)
        dh_cam(ease(t/DUR)*.6)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
def VS(side):
    def f():
        Hm,F=room_set(side,'db'); dad,boy=F['d'],F['b']; x=DADP[0]
        def upd(t):
            home_lights(Hm,t); fam_idle(F,t,'happy'); cheer(dad,t,-1.0); cheer(boy,t,-1.0,ph=1.6)
            for s in (1,-1): dad['arm'][s].rotation_euler=(R(-38+16*math.sin(t*14+s)),R(-s*52),0)
            q=ease(t/DUR); camset(LV((x-.1,-2.75,2.2),(x,-2.45,2.2),q),(x+.45,1.5,1.72),30,8)
        return dict(upd=upd)
    return f
SHOTS['VSI']=VS('I'); SHOTS['VSP']=VS('P')
# ---------------------------------------------------------------- the rule
def RULE_WIDE(side,w0):
    def f():
        Hm,F=room_set(side); dad=F['d']
        def upd(t):
            home_lights(Hm,t); fam_idle(F,t,'watch'); k=ease(tl(t,ws(w0)-.25,ws(w0)+.25))
            if k>0:
                sitp(dad,t,up=k,rz=L(0,-28,k)); mood(dad,'glare'); finger(dad,t,-1,k); dad['arm'][1].rotation_euler=(0,0,0); look_at(dad,hp(F['b']),k)
                for q in 'bmg': look_at(F[q],hp(dad),k,maxyaw=80); mood(F[q],'tense' if k>.5 else 'watch')
            cam_wide(ease(t/DUR))
        return dict(upd=upd)
    return f
SHOTS['LAHORE']=RULE_WIDE('P',41); SHOTS['DELHI']=RULE_WIDE('I',54)
def RULE(side,a,b):
    def f():
        Hm,F=room_set(side,'dbm'); dad=F['d']
        def upd(t):
            home_lights(Hm,t); fam_idle(F,t,'tense'); sw=math.sin(t*2.6)
            sitp(dad,t,up=1.0,rz=-28+10*sw); mood(dad,'glare'); finger(dad,t,-1,1.0); dad['arm'][1].rotation_euler=(R(-8),0,0)
            look_at(dad,hp(F['b']) if sw<.3 else hp(F['m']),1.0); speak(dad,t,a,b,gesture=False)
            for q in 'bm': look_at(F[q],hp(dad),1.0,maxyaw=80); F[q]['root'].rotation_euler[0]=R(-5)
            h=hp(dad); q=ease(t/DUR); camset(LV((h[0]+.22,h[1]-4.4,2.2),(h[0]+.2,h[1]-4.1,2.18),q),(h[0]-.3,h[1],1.72),32,8)
        return dict(upd=upd)
    return f
SHOTS['RULEP']=RULE('P',45,50); SHOTS['RULEI']=RULE('I',59,64)
def ONEDAD():
    P,I,FP,FI=dh_set(); t1=ws(67)-.05
    def upd(t):
        for Hm,F in ((P,FP),(I,FI)):
            home_lights(Hm,t); fam_idle(F,t,'tense'); dad=F['d']; k=1-ease(tl(t,t1,t1+.4))
            sitp(dad,t,up=k,rz=-28*k); mood(dad,'glare'); finger(dad,t,-1,k,wag=.5); look_at(F['b'],hp(dad),k,maxyaw=80)
            if k<=0: crossed(dad); look_at(dad,TVP(F['z0']),1.0)
        dh_cam(.3+.3*ease(t/DUR))
    return dict(upd=upd)
SHOTS['ONEDAD']=ONEDAD
def SAMESOFA():
    P,I,FP,FI=dh_set()
    def upd(t):
        for Hm,F in ((P,FP),(I,FI)):
            home_lights(Hm,t); fam_idle(F,t,'watch'); crossed(F['d']); k=math.sin(min(1,t/DUR)*pi)
            for q in 'db': F[q]['root'].location[2]+=.05*abs(math.sin(t*9))*(t<.45)       # both families bounce on the same sofa once
        dh_cam(.6+.25*ease(t/DUR))
    return dict(upd=upd)
SHOTS['SAMESOFA']=SAMESOFA
def TABLE(side,tx):
    def f():
        Hm,F=room_set(side,'db'); FILLE[0]=30
        for dx,dy in ((-.6,.1),(-.42,-.1),(-.24,.1)): steam((dx,-.75+dy,.66),-1.0,9.0,n=5,seed=int(dx*50)+9,size=.035)
        def upd(t):
            home_lights(Hm,t); fam_idle(F,t,'watch'); q=ease(t/DUR)
            camset(LV((tx*1.15,-2.6,2.2),(tx*1.08,-2.35,2.05),q),(tx,-.78,.5),58,8)
        return dict(upd=upd)
    return f
SHOTS['SAMECHAI']=TABLE('P',-.42); SHOTS['SAMOSA']=TABLE('I',.4)
# ---------------------------------------------------------------- the neighbour
def NEIGHBOR():
    Hm,F=room_set('P','dbm'); t1=ws(79)-.1; t2=ws(82); V=int(os.environ.get('IPKV','0'))
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); k=ease(tl(t,t1,t1+.15)); b=ease(tl(t,t2,t2+.25))
        for q in 'dbm':
            H=F[q]
            if k>0 and b<1: look_at(H,(5.5,-.2,H['z0']+2.3),k*(1-b),maxyaw=66); mood(H,'shock')
            if b>=1: mood(H,'sad')
        q=ease(t/DUR)
        if V==0: camset(LV((3.3,-1.7,2.25),(3.15,-1.5,2.22),q),(-.1,1.4,1.95),28,8)
        else: camset(LV((3.9,-2.6,2.3),(3.7,-2.35,2.25),q),(0,1.4,1.9),30,8)
    return dict(upd=upd)
SHOTS['NEIGHBOR']=NEIGHBOR
def HATES():
    Hm,F=room_set('P','dbm'); dad=F['d']; ch=empty((0,0,-5)); obox((0,0,0),(.13,.3,.03),M('#5A3A22',.6),.02,ch); obox((0,-.1,.05),(.12,.03,.05),M('#3A2A1E',.6),.02,ch)
    t0=.5; V=int(os.environ.get('IPKV','0'))
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'glare')
        for q in 'dbm': look_at(F[q],(5.5,-.2,2.3),1.0,maxyaw=66)
        w=tl(t,.12,t0); th=tl(t,t0,t0+.14)
        dad['arm'][1].rotation_euler=(R(L(-40,-150,w)+95*th),R(20*w),0); bpy.context.view_layer.update()
        if t<t0: ch.location=handw(dad,1); ch.rotation_euler=(0,0,R(90))
        else:
            q=t-t0; p0=Vector((DADP[0]+.9,1.3,2.75)); ch.location=(p0.x+7.5*q,p0.y+.4*q,p0.z+1.2*q-4.9*q*q); ch.rotation_euler=(q*14,q*6,R(90))
        q=ease(t/DUR)
        if V==0: camset(LV((3.5,-2.9,2.3),(3.35,-2.65,2.27),q),(-.35,1.4,2.0),30,8)
        else: camset(LV((2.6,-3.4,2.25),(2.5,-3.1,2.22),q),(-.2,1.4,2.0),30,8)
    return dict(upd=upd)
SHOTS['HATES']=HATES
# ---------------------------------------------------------------- Waleed has not moved for four hours
def squeeze(H,t,k=1.0):
    """needs the washroom: knees together, bouncing, hands pressed on the knees"""
    for q in (1,-1): H['leg'][q].rotation_euler[1]=R(-q*7*k); H['leg'][q].rotation_euler[0]+=R(3*math.sin(t*22+q)*k)
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-62*k),R(s*8*k),0)
    H['root'].location[0]+=.012*math.sin(t*26)*k
def SATDOWN():
    Hm,F=room_set('P','dbm'); wa=F['b']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'watch'); sitp(wa,t,lean=0); look_at(wa,TVP(),1.0); face(wa,mouth='flat',brow=.05,brow_r=8,eyes=1.15); squeeze(wa,t,.5)
        cam_one(wa,ease(t/DUR),side=.5,dist=4.3,lens=30)
    return dict(upd=upd)
SHOTS['SATDOWN']=SATDOWN
def FOURHRS():
    Hm,F=room_set('P','dbm'); wa=F['b']; web=M('#F4F4F0',.6,emit=.5)
    hx,hy=BOYP; pts=[((hx+.95,hy+.25,1.15),(hx+2.2,hy+.3,.95)),((hx+.95,hy+.25,1.15),(hx+2.25,hy+.2,1.5)),((hx+1.55,hy+.28,1.05),(hx+1.75,hy+.26,1.33)),((hx+1.25,hy+.27,1.1),(hx+1.4,hy+.26,1.25))]
    for p_,q_ in pts: bseg(p_,q_,.006,web,seg=4)
    B.done('web'); dr=[oico((0,0,-5),.035,M('#9FD8FF',.2,emit=.8),None,sub=1) for k in range(3)]
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'watch'); sitp(wa,t,lean=0); look_at(wa,TVP(),1.0); face(wa,mouth='strain',brow=.06,brow_r=14,eyes=1.2); squeeze(wa,t,1.0)
        bpy.context.view_layer.update(); h=Vector(hp(wa))
        for k,o in enumerate(dr):
            q=((t*1.1+k*.37)%1.0); o.location=(h.x+(-.36,.38,-.3)[k],h.y-.3,h.z+.22-.5*q); o.scale=tuple(3*[1-q*.5])
        cam_one(wa,ease(t/DUR),side=.25,dist=3.0,lens=34,tz=-.1)
    return dict(upd=upd)
SHOTS['FOURHRS']=FOURHRS
def wash_set():
    Hm,F=room_set('P','dbm'); return Hm,F
def WASHROOM():
    Hm,F=wash_set(); wa,dad=F['b'],F['d']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'watch'); k=ease(tl(t,ws(99)-.2,ws(99)+.2))
        sitp(wa,t,up=.3*k,lean=0); squeeze(wa,t,1-k*.5); wa['arm'][-1].rotation_euler=(R(-120*k-40*(1-k)),R(6*k),0); look_at(wa,hp(dad),k,maxyaw=42)
        face(wa,mouth='flat',brow=.05,brow_r=12,eyes=1.1); speak(wa,t,99,100,gesture=False)
        cam_two(ease(t/DUR))
    return dict(upd=upd)
SHOTS['WASHROOM']=WASHROOM
def BAITHO():
    Hm,F=wash_set(); wa,dad=F['b'],F['d']; t1=ws(108)-.08
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'watch'); k=1-ease(tl(t,t1,t1+.16))
        sitp(wa,t,up=.3*k,lean=0); squeeze(wa,t,.6); wa['arm'][-1].rotation_euler=(R(-120*k-40*(1-k)),R(6*k),0); look_at(wa,hp(dad),1.0,maxyaw=42)
        face(wa,mouth='o' if k>.5 else 'flat',brow=.06,brow_r=12,eyes=1.15 if k>.5 else 1.25)
        a=ease(tl(t,0,.22)); look_at(dad,hp(wa),a,maxyaw=54); mood(dad,'glare'); speak(dad,t,101,108,gesture=False)
        bpy.context.view_layer.update(); arm_to(dad,1,(BOYP[0]-.25,BOYP[1]-.35,.75+.12*math.sin(t*12)*(t>t1-.5)),a,base=(R(-40),R(-4),0))
        q=ease(t/DUR); camset(LV((-.4,-3.85,2.2),(-.33,-3.55,2.15),q),(.05,1.45,1.86),26,8)
    return dict(upd=upd)
SHOTS['BAITHO']=BAITHO
# ---------------------------------------------------------------- Rohan and the cup
def cup_set(who='dbm'):
    Hm,F=room_set('I',who); ro=F['b']; cp=cup_of(ro,1); return Hm,F,ro,cp
def cup_hold(ro,cp,t,sip=0.0,out=0.0,a=-66):
    hold_chai(ro,cp,1,a=a,sip=sip,out=out); upright(cp,ro,1); ro['arm'][-1].rotation_euler=(R(-40),R(4),0)
def CUP():
    Hm,F,ro,cp=cup_set()
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); sitp(ro,t,lean=0); look_at(ro,TVP(),1.0); face(ro,mouth='flat',brow=.05,eyes=1.15); cup_hold(ro,cp,t)
        q=ease(t/DUR); camset(LV((.3,-4.8,2.1),(.75,-3.3,1.95),q),LV((0,1.55,1.75),(BOYP[0],1.4,1.7),q),27,8)
    return dict(upd=upd)
SHOTS['CUP']=CUP
def CANT():
    Hm,F,ro,cp=cup_set(); dad=F['d']; h=DUR/2
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); sitp(ro,t,lean=0)
        s1=math.sin(min(1,max(0,t/(h-.1)))*pi); s2=math.sin(min(1,max(0,(t-h)/(h-.1)))*pi)
        cup_hold(ro,cp,t,sip=.8*s1,out=0,a=-66+34*s2); gl=max(tl(t,.35,.55)*(1-tl(t,h-.25,h-.05)),tl(t,h+.35,h+.55))
        look_at(dad,hp(ro),gl,maxyaw=75); mood(dad,'glare' if gl>.3 else 'tense')
        look_at(ro,hp(dad) if gl>.5 else TVP(),1.0,maxyaw=70); face(ro,mouth='o' if gl>.5 else 'flat',brow=.06,eyes=1.2 if gl>.5 else 1.1)
        cam_two(ease(t/DUR),dx=.35,tx=.2)
    return dict(upd=upd)
SHOTS['CANT']=CANT
def THANDI():
    Hm,F,ro,cp=cup_set(); mom=F['m']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); sitp(ro,t,lean=0); look_at(ro,TVP(),1.0); face(ro,mouth='flat',brow=.05,eyes=1.15); cup_hold(ro,cp,t)
        sitp(mom,t,lean=6); look_at(mom,hp(ro),1.0,maxyaw=70); face(mom,mouth='flat',brow=.03,brow_r=6,eyes=1.0); speak(mom,t,127,131,gesture=False)
        bpy.context.view_layer.update(); arm_to(mom,-1,handw(ro,1),ease(tl(t,.15,.5))*.8,base=(R(-40),R(4),0))
        q=ease(t/DUR); camset(LV((.2,-3.5,2.1),(.35,-3.2,2.05),q),(2.25,1.2,1.8),29,8)
    return dict(upd=upd)
SHOTS['THANDI']=THANDI
def PLEASE():
    Hm,F,ro,cp=cup_set(); mom=F['m']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); sitp(ro,t,lean=0); cup_hold(ro,cp,t); k=ease(tl(t,0,.25))
        look_at(ro,hp(mom),k,maxyaw=70); face(ro,mouth='flat',brow=-.02,brow_r=-6,eyes=.9); speak(ro,t,132,133,gesture=False)
        q=ease(t/DUR); camset(LV((BOYP[0]+1.35,-2.1,2.05),(BOYP[0]+1.25,-1.85,2.05),q),(BOYP[0],1.5,1.85),33,8)
    return dict(upd=upd)
SHOTS['PLEASE']=PLEASE
def JABTAK():
    Hm,F,ro,cp=cup_set(); dad=F['d']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); sitp(ro,t,lean=0); k=ease(tl(t,0,.5))
        cup_hold(ro,cp,t,sip=.38*k); look_at(ro,(BOYP[0],-4,1.9),1.0); face(ro,mouth='flat',brow=-.03,brow_r=-10,eyes=1.0); speak(ro,t,134,143,gesture=False)
        n=tl(t,ws(140)-.1,ws(140)+.2); look_at(dad,hp(ro),n,maxyaw=75); mood(dad,'happy' if n>.5 else 'tense'); dad['head'].rotation_euler[0]+=R(9*math.sin(t*9))*n
        cam_one(ro,ease(t/DUR),side=-.35,dist=3.4,lens=33,tz=-.3)
    return dict(upd=upd)
SHOTS['JABTAK']=JABTAK
