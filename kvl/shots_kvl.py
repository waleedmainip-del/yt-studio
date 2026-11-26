# Shots for "Karachi vs Lahore". SEQ/END/WI filled by gen_seq.py.
SHOTS={}
END=117.5
SEQ=[('HOOK', 0.0), ('KHI', 1.7), ('LHR', 2.667), ('SIDE', 3.833), ('BABY', 5.967), ('INTERVIEW', 7.867), ('ALOO', 10.267), ('WRONG', 13.733), ('MEET', 17.033), ('LINE', 18.733), ('SETTLE', 20.967), ('ROUND1', 22.433), ('NASHTA', 24.333), ('BIRYANI', 28.333), ('ALOO2', 30.867), ('PULAO', 32.533), ('ENDED', 35.367), ('NOBODY', 37.633), ('DIFFERENT', 40.067), ('ONEBOY', 41.767), ('WALEED', 44.933), ('WON', 45.767), ('BHOOK', 48.267), ('ROUND2', 50.067), ('BADSHAHI', 52.033), ('SAMANDAR', 54.233), ('TANKER', 56.067), ('CELEB', 58.833), ('SMOG1', 61.667), ('SMOG2', 64.167), ('FAINT', 66.767), ('TIED', 68.3), ('DOWN', 70.567), ('LASSI', 72.567), ('BUN', 75.267), ('TASTE', 77.867), ('BREATH', 79.133), ('DONO', 81.133), ('DONO2', 82.867), ('TURNED', 83.767), ('VOICE', 85.333), ('ISB', 87.3), ('SILENCE', 91.833), ('NAU', 96.4), ('PAHAAD', 98.333), ('HIGHFIVE', 100.833), ('OVER', 104.7), ('MORNING', 107.333), ('ATE', 109.733), ('KHA', 112.333), ('CTA', 113.833)]
WI={'HOOK': 0, 'KHI': 6, 'LHR': 8, 'SIDE': 11, 'BABY': 18, 'INTERVIEW': 24, 'ALOO': 30, 'WRONG': 39, 'MEET': 51, 'LINE': 57, 'SETTLE': 67, 'ROUND1': 71, 'NASHTA': 74, 'BIRYANI': 83, 'ALOO2': 90, 'PULAO': 93, 'ENDED': 99, 'NOBODY': 105, 'DIFFERENT': 109, 'ONEBOY': 114, 'WALEED': 125, 'WON': 126, 'BHOOK': 133, 'ROUND2': 139, 'BADSHAHI': 143, 'SAMANDAR': 148, 'TANKER': 152, 'CELEB': 160, 'SMOG1': 165, 'SMOG2': 173, 'FAINT': 181, 'TIED': 184, 'DOWN': 189, 'LASSI': 196, 'BUN': 206, 'TASTE': 214, 'BREATH': 217, 'DONO': 221, 'DONO2': 224, 'TURNED': 225, 'VOICE': 230, 'ISB': 236, 'SILENCE': 245, 'NAU': 253, 'PAHAAD': 260, 'HIGHFIVE': 267, 'OVER': 278, 'MORNING': 285, 'ATE': 292, 'KHA': 298, 'CTA': 303}
FOC=(0.0,-1.5)
LROWS=[(-4.5,1.4),(-6.4,2.6),(-4.5,6.2),(-4.5,8.6),(-6.4,.2),(-4.5,3.8),(-6.4,5.0),(-6.4,7.4),(-6.4,9.8)]
def rows(team): return [(x if team=='L' else -x,y) for x,y in LROWS]
def team_flag(H,col,col2,s=1):
    def b(e):
        ocyl((0,-.06,-.72),.022,1.7,M('#D8D2C4',.5),e,rot=(0,0,0),seg=6); obox((.37,-.06,-1.28),(.37,.008,.25),M(col,.7,kind='fabric'),.0,e)
        obox((.37,-.07,-1.28),(.22,.006,.07),M(col2,.7),0,e); obox((.37,-.05,-1.28),(.22,.006,.07),M(col2,.7),0,e)
    return in_hand(H,s,b)
def mkfans(team,skip=(),only=None,focus=FOC,shift=(0,0),flags=(0,7)):
    C=LFANS if team=='L' else KFANS; out=[]
    for i,(x,y) in enumerate(rows(team)):
        if i in skip or (only is not None and i not in only): continue
        x+=shift[0]*(1 if team=='L' else -1); y+=shift[1]
        rz=face_dir(focus[0]-x,focus[1]-y); H=mk(C[i],x,y,rz,'%s%d'%(team,i)); H['home']=(x,y,rz); H['ph']=i*1.37+(0 if team=='L' else .7); H['team']=team; H['i']=i
        H['flag']=team_flag(H,LG if team=='L' else KB,LGOLD if team=='L' else KW) if i in flags else None; out.append(H)
    return out
def fan(H,t,mode='idle',look=None,k=1.0,talky=False):
    x,y,rz=H['home']; ph=H['ph']; r=H['root']; r.location[0]=x; r.location[1]=y; r.location[2]=H['z0']; r.rotation_euler=(0,0,R(rz)); stand(H,t); blink(H,t)
    for s in (1,-1): H['arm'][s].rotation_euler=(R(2*math.sin(t*1.3+ph+s)),0,0)
    H['head'].rotation_euler=(0,0,0); face(H,brow=0,brow_r=0,eyes=1)
    if look is not None: look_at(H,look,1.0,maxyaw=70)
    alt=lambda a,b,f=5: a if (int(t*f+ph)%2 or not talky) else b
    if mode=='cheer':
        b=abs(math.sin(t*5.2+ph)); r.location[2]=H['z0']+.008+.16*b*k
        for s in (1,-1): H['arm'][s].rotation_euler=(R((-158+14*math.sin(t*10.4+ph+s))*k),R(-s*12*k),0)
        face(H,mouth=alt('grin','O'),brow=.04)
    elif mode=='fist':
        H['arm'][1].rotation_euler=(R(-150+18*math.sin(t*9+ph)),R(-8),0); face(H,mouth=alt('shout','O'),brow=-.02,brow_r=-10); r.rotation_euler[0]=R(5)
    elif mode=='shout':
        H['arm'][1].rotation_euler=(R(-92+12*math.sin(t*11+ph)),R(-6),0); H['arm'][-1].rotation_euler=(R(-30+8*math.sin(t*7+ph)),R(10),0)
        face(H,mouth=alt('shout','O',6),brow=-.03,brow_r=-12); r.rotation_euler[0]=R(7)
    elif mode=='gasp':
        shock(H,k); face(H,mouth='O',brow=.06,eyes=1.15); H['head'].rotation_euler[0]=R(-6)
    elif mode=='laugh':
        laugh(H,t); H['arm'][1].rotation_euler=(R(-40+10*math.sin(t*12+ph)),0,R(20))
    elif mode=='freeze':
        r.rotation_euler[0]=R(8*k); face(H,mouth='o',brow=.05,eyes=1.15)
        for s in (1,-1): H['arm'][s].rotation_euler=(R(-18*k),0,0)
    elif mode=='glare':
        face(H,mouth='frown',brow=-.03,brow_r=-14*k)
        for s in (1,-1): H['arm'][s].rotation_euler=(R(-6),R(-s*8),0)
    elif mode=='dance':
        b=math.sin(t*7+ph); r.location[2]=H['z0']+.008+.1*abs(b)
        for s in (1,-1): H['arm'][s].rotation_euler=(R(-140+20*b*s),R(s*20),0)
        H['leg'][1].rotation_euler[0]=R(-28*max(0,b)); H['leg'][-1].rotation_euler[0]=R(-28*max(0,-b)); face(H,mouth='grin',brow=.04)
    elif mode=='smile': face(H,mouth='smile')
    else: face(H,mouth='flat')
    if H.get('flag') is not None and mode not in ('cheer','fist','dance','gasp'): H['arm'][1].rotation_euler=(R(-128+6*math.sin(t*3+ph)),R(-10),0)
def fans(F,t,mode='idle',look=None,k=1.0,talky=False):
    for H in F: fan(H,t,mode,look,k,talky)
def place(H,x,y,rz):
    H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(rz)
SX=1.9; CY=.8; SRZ=62
def captains():
    sh=mk(SHEEDA,-SX,CY,SRZ,'sheeda'); gu=mk(GUDDU,SX,CY,-SRZ,'guddu'); return sh,gu
def cap_idle(H,t,x,y,rz,other=None,mouth='flat'):
    place(H,x,y,rz); H['root'].rotation_euler[0]=0; hstand(H,t); H['head'].rotation_euler=(0,0,0); face(H,mouth=mouth,brow=0,brow_r=0,eyes=1)
    if other is not None: look_at(H,other,1.0,maxyaw=70)
def crossed(H,k=1.0):
    H['arm'][1].rotation_euler=(R(-58*k),R(34*k),0); H['arm'][-1].rotation_euler=(R(-50*k),R(-34*k),0)
def handw(H,s): return H['arm'][s].matrix_world@Vector(hand_loc(H,s))
def speak(H,t,a,b,s=1,amp=1.0,base=-55,rate=7.0,gesture=True):
    g0,g1=wt(a,b); talk(H,t,g0,g1,rate=rate)
    if gesture and g0-T0-.1<=t<=g1-T0+.25: gest(H,t,s,amp,6.5,base)
def single(H,yaw=30,dist=3.0,dz=.12,tz=-.2,lens=32):
    h=Vector(hp(H)); a=H['root'].rotation_euler[2]+R(yaw); f=Vector((math.sin(a),-math.cos(a),0)); c=h+f*dist+Vector((0,0,dz))
    return (c.x,c.y,c.z),(h.x,h.y,h.z+tz),lens
def hands_head(H,k=1.0,dx=.95,dz=5.55,dy=-.05,only=None):
    m=root_mat(H); u=H['u']
    for s in ((1,-1) if only is None else (only,)): arm_to(H,s,m@Vector((s*dx*u,dy*u,dz*u)),k,base=(0,0,0))
def what_pose(H,k=1.0,t=0.0,amp=1.0):
    """palms-up 'WHAT?!': both arms out wide & low (rigid arms never come near the face)"""
    b=math.sin(t*9)*amp
    for s in (1,-1): H['arm'][s].rotation_euler=(R((-30+4*b)*k),R(-s*(60+5*b)*k),0)
def arms_up(H,k=1.0,t=0.0,spread=18,jig=0.0,only=None):
    """arms raised in a V (outward tilt keeps them clear of the head)"""
    for s in ((1,-1) if only is None else (only,)): H['arm'][s].rotation_euler=(R((-165+jig*math.sin(t*12+s))*k),R(s*spread*k),0)
def pointw(H,s,p,k=1.0): arm_to(H,s,p,k,base=tuple(H['arm'][s].rotation_euler))
REFP=(0.0,-.7)
def ref_mk(x=REFP[0],y=REFP[1],rz=0): return mk(REF,x,y,rz,'ref')
def placard(H,l1,l2,col='#C8372D'):
    u=H['u']; e=empty((0,-.3*u,7.05*u),H['root'])
    obox((0,0,0),(.98,.03,.5),M('#F4F1EA',.6),.02,e); obox((0,.012,0),(1.04,.02,.56),M(col,.5),.01,e)
    text(l1,(0,-.04,.17),(0,-1,0),.34,M('#16171C',.5),ex=.01,parent=e); text(l2,(0,-.04,-.21),(0,-1,0),.3,M(col,.5),ex=.01,parent=e); return e
def hold_board(H,e,k=1.0):
    m=e.matrix_world
    for s in (1,-1): arm_to(H,s,m@Vector((s*.8,-.05,-.42)),k,base=(0,0,0))
def whistle(H):
    u=H['u']; ocyl((0,-.6*u,3.32*u),.04,.11,M('#C9CED8',.25,metal=.9),H['root'],rot=(R(90),0,0),seg=10)
    for s in (1,-1): obox((s*.13*u,-.545*u,3.72*u),(.012,.008,.36*u),M('#C8372D',.6),0,H['root'],rot=(0,R(s*14),0))
# ---------------------------------------------------------------- 1-4 hook
def HOOK():
    arena('kv_day'); LF=mkfans('L'); KF=mkfans('K'); sh,gu=captains(); FILLE[0]=0
    def upd(t):
        fans(LF,t,'cheer',look=(0,CY,1.8)); fans(KF,t,'cheer',look=(0,CY,1.8))
        cap_idle(sh,t,-SX,CY,SRZ,hp(gu),'smirk'); cap_idle(gu,t,SX,CY,-SRZ,hp(sh),'smirk'); crossed(sh); crossed(gu)
        q=ease(t/DUR); camset(LV((0,-12.2,5.6),(0,-10.4,4.5),q),LV((0,3.0,2.2),(0,2.6,2.3),q),20,8)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
def side_shot(team):
    s=-1 if team=='L' else 1
    def f():
        arena('kv_day',gtext=False); F=mkfans(team); sh,gu=captains(); me=sh if team=='L' else gu; ot=gu if team=='L' else sh; FILLE[0]=25
        def upd(t):
            fans(F,t,'cheer',look=(-s*2,-4,2.0))
            cap_idle(ot,t,-s*SX,CY,s*SRZ,hp(me)); crossed(ot)
            place(me,s*SX,CY,-s*48); hstand(me,t); b=abs(math.sin(t*6)); me['root'].location[2]=me['z0']+.008+.1*b
            me['arm'][1].rotation_euler=(R(-160+10*math.sin(t*12)),R(-10),0); me['arm'][-1].rotation_euler=(R(-20),R(12),0); face(me,mouth='grin',brow=.03)
            me['head'].rotation_euler=(R(-4),0,0)
            q=ease(t/DUR); camset(LV((-s*2.9,-5.0,2.25),(-s*2.6,-4.5,2.25),q),(s*4.2,3.2,2.5),23,8)
        return dict(upd=upd)
    return f
SHOTS['KHI']=side_shot('K'); SHOTS['LHR']=side_shot('L')
def SIDE():
    arena('kv_day',gtext=False); C=(0,-4.8,2.05); LF=mkfans('L',focus=(0,-5)); KF=mkfans('K',focus=(0,-5)); sh,gu=captains(); FILLE[0]=30
    def upd(t):
        k=tl(t,.15,.55)
        for H in LF+KF:
            fan(H,t,'idle',look=C); ps=-1 if H.get('flag') is not None else 1; arm_to(H,ps,C,k,base=(R(2),0,0)); face(H,mouth='O' if k>.5 else 'flat',brow=-.02,brow_r=-8*k)
        for H,x in ((sh,-SX),(gu,SX)):
            cap_idle(H,t,x,CY,face_dir(-x*.4,-5-CY),C); arm_to(H,1,C,k,base=(R(2),0,0)); face(H,mouth='O' if k>.5 else 'flat',brow=-.02,brow_r=-10*k)
        q=ease(t/DUR); camset(LV(C,(0,-4.3,2.05),q),(0,3.0,2.1),20,8)
    return dict(upd=upd)
SHOTS['SIDE']=SIDE
# ---------------------------------------------------------------- 5 babies
def BABYS():
    P=nursery(); bb=mk(BABY,0,.25,0,'baby'); dad=mk(DAD,-1.85,2.3,face_dir(1.85,-2.05),'dad'); mom=mk(MOM,1.85,2.3,face_dir(-1.85,-2.05),'mom'); FILLE[0]=30
    LF=(-.7,.22,1.2); KFp=(.7,.22,1.2); kp=P['KARACHI']
    def upd(t):
        place(bb,0,.25,0); sit(bb,1,0.0,legs=90); blink(bb,t); bb['root'].rotation_euler[0]=0
        a=tl(t,.15,.4)*(1-tl(t,.7,.95)); b=tl(t,.8,1.05); pk=tl(t,1.05,1.35)
        look_at(bb,LV(LV((0,-3,1),LF,a),KFp,b) if pk<.5 else LV(KFp,(0,-3,1.0),tl(t,1.45,1.7)),1.0,maxyaw=75,maxpitch=40)
        for s in (1,-1): bb['arm'][s].rotation_euler=(R(-20),0,0)
        bb['root'].rotation_euler[1]=R(14*pk); kp.rotation_euler[1]=R(-7*pk)
        if pk>0:
            bpy.context.view_layer.update(); arm_to(bb,1,(.7,.22,.42),pk,base=(R(-20),0,0)); arms_up(bb,pk,t,spread=22,jig=10,only=-1)
        face(bb,mouth='grin' if pk>.3 else ('o' if b>.5 else 'smile'),brow=.03)
        for H,me in ((dad,'L'),(mom,'K')):
            stand(H,t); blink(H,t); place(H,H['root'].location[0],H['root'].location[1],face_dir(-H['root'].location[0],.25-H['root'].location[1])); look_at(H,hp(bb),1.0,maxpitch=40)
            H['root'].rotation_euler[0]=R(10*(1-pk))
            for s in (1,-1): H['arm'][s].rotation_euler=(R(-35*(1-pk)),0,0)
        face(dad,mouth='smile' if pk<.3 else 'O',brow=.05 if pk>.3 else .02,eyes=1.15 if pk>.3 else 1); face(mom,mouth='grin' if pk>.3 else 'smile',brow=.04)
        if pk>0:
            what_pose(dad,pk,t,amp=.6); dad['head'].rotation_euler[0]+=R(-6*pk)
            arms_up(mom,pk,t,spread=16,jig=8); mom['root'].location[2]=mom['z0']+.008+.1*abs(math.sin(t*9))*pk
        q=ease(t/DUR); camset(LV((0,-2.75,1.14),(0,-2.5,1.1),q),(0,1.0,1.02),21,8)
    return dict(upd=upd)
SHOTS['BABY']=BABYS
# ---------------------------------------------------------------- 6-8 interview
BOSSP=(0,2.38); CANDP=(.55,-.95)
def boss_sit(bs,t,lean=0.0):
    place(bs,BOSSP[0],BOSSP[1],0); seat(bs,t,.36); bs['root'].rotation_euler[0]=R(lean)
    for s in (1,-1): arm_to(bs,s,(s*.42,1.62,.95),1.0,base=(0,0,0))
def cand_sit(cd,t,x=CANDP[0],y=CANDP[1],rz=180):
    place(cd,x,y,rz); seat(cd,t,.58)
    for s in (1,-1): cd['arm'][s].rotation_euler=(R(-42),R(-s*4),0)
def INTERVIEW():
    O=office(); bs=mk(BOSS,BOSSP[0],BOSSP[1],0,'boss'); ch=roll_chair(CANDP[0],CANDP[1],180); cd=mk(CAND,CANDP[0],CANDP[1],180,'cand'); FILLE[0]=40
    def upd(t):
        boss_sit(bs,t); look_at(bs,hp(cd),1.0); face(bs,mouth='flat',brow=-.02,brow_r=-6)
        cand_sit(cd,t); look_at(cd,hp(bs),1.0); face(cd,mouth='smile')
        q=ease(t/DUR); camset(LV((3.05,-3.25,1.95),(2.8,-2.9,1.9),q),(.05,2.3,1.5),30,8)
    return dict(upd=upd)
SHOTS['INTERVIEW']=INTERVIEW
def ALOO():
    O=office(); bs=mk(BOSS,BOSSP[0],BOSSP[1],0,'boss'); ch=roll_chair(CANDP[0],CANDP[1],180); cd=mk(CAND,CANDP[0],CANDP[1],180,'cand'); FILLE[0]=60
    pl=in_hand(bs,1,lambda e: biryani_plate(e,(0,-.08,.02))); pp=O['paper']; p0=Vector(pp.location)
    def upd(t):
        boss_sit(bs,t); cand_sit(cd,t)
        a=tl(t,ws(30)-.1,ws(31)+.15); fl=tl(t,ws(31)-.05,ws(31)+.45)
        bs['arm'][-1].rotation_euler=(R(-60+40*a*(1-fl)),R(30*a*(1-fl)),R(0)) if a<1 or fl<1 else (R(-50),0,0)
        pp.location=p0+Vector((-1.6*fl,-.3*fl,.6*math.sin(pi*fl))); pp.rotation_euler=(R(40*fl),0,R(220*fl))
        up=tl(t,ws(32)-.2,ws(32)+.25); lean=tl(t,ws(36)-.1,ws(37))
        bs['arm'][1].rotation_euler=(R(-25),0,0); arm_to(bs,1,(.16,1.6,1.46),up,base=(R(-25),0,0)); upright(pl,bs,1,tilt=-34*up)
        bs['root'].rotation_euler[0]=R(9*lean); look_at(bs,(.5,-.3,1.62),1.0)
        face(bs,mouth='flat',brow=-.03*lean,brow_r=-12*lean); speak(bs,t,30,38,s=-1,gesture=False)
        q=ease(t/DUR); camset(LV((.5,-.25,1.62),(.42,.05,1.6),q),(0,2.32,1.42),33,8)
    return dict(upd=upd)
SHOTS['ALOO']=ALOO
def WRONG():
    O=office(); bs=mk(BOSS,BOSSP[0],BOSSP[1],0,'boss'); ch=roll_chair(CANDP[0],CANDP[1],180); cd=mk(CAND,CANDP[0],CANDP[1],180,'cand'); gd=mk(GUARD,-.95,-.95,90,'guard'); FILLE[0]=40
    DY,DX=O['door']; X1=DX+2.0
    def upd(t):
        boss_sit(bs,t)
        sp=tl(t,.85,1.25); gq=min(1,max(0,(t-1.2)/(DUR-1.25))); go=gq*gq*(3-2*gq)
        x=L(CANDP[0],X1,go); y=L(CANDP[1],DY,min(1,go*3)); rz=L(180,90,sp)
        ch.location=(x,y,0); ch.rotation_euler=(0,0,R(rz)); cand_sit(cd,t,x,y,rz)
        face(cd,mouth='o' if t<.8 and int(t*7)%2 else ('O' if t>1.0 else 'smile'),brow=.05 if t>1.0 else 0,eyes=1.15 if t>1.0 else 1)
        if t<.8: speak(cd,t,39,41,gesture=False); look_at(cd,hp(bs),1.0)
        if t>1.0:
            for s in (1,-1): cd['arm'][s].rotation_euler=(R(-120+25*math.sin(t*13+s)),R(-s*25),0)
            for s in (1,-1): cd['leg'][s].rotation_euler[0]=-R(90)+R(14*math.sin(t*15+s*1.6))
        look_at(bs,hp(cd),1.0); face(bs,mouth='frown',brow=-.03,brow_r=-14)
        pt=tl(t,.55,.85); arm_to(bs,1,(DX,DY,1.6),pt,base=(0,0,0)) if pt>0 else None
        f=Vector((math.sin(R(rz)),-math.cos(R(rz)),0))
        g0=Vector((-.95,-.95,0)); g=g0.lerp(Vector((x,y,0))-f*1.28,sp) if go<=0 else Vector((min(x-1.28,DX-2.2),y,0))
        place(gd,g.x,g.y,90); walk(gd,(g-g0).length,step=.5,arm=0); blink(gd,t)
        rel=1.0 if x-1.28<DX-2.2 else max(0,1-(x-1.28-(DX-2.2))/.8)
        for s in (1,-1): gd['arm'][s].rotation_euler=(R(-72*max(sp,go>0)*rel),0,0)
        face(gd,mouth='flat',brow=-.03,brow_r=-10)
        q=ease(min(1,max(0,(t-1.0)/(DUR-1.0)))); camset((1.2,-4.05,2.3),LV((.25,.35,1.3),(4.9,-.7,1.2),q),20,8)
    return dict(upd=upd)
SHOTS['WRONG']=WRONG
# ---------------------------------------------------------------- 9-12 the line
def MEET():
    arena('kv_gold'); LF=mkfans('L'); KF=mkfans('K'); FILLE[0]=0
    b1=w11((-40,-9.6,0),0,seed=12,col='#1F7A44',accent='#E6B53A'); b2=w11((40,-6.2,0),180,seed=13,col='#2466C9',accent='#F4F6FA')
    def upd(t):
        fans(LF,t,'cheer',look=(-12,-9,2)); fans(KF,t,'cheer',look=(12,-6,2))
        d=ease_out(min(1,t/(DUR*.92)))*33.8
        roll(b1,-40+d,-9.6,0,d); roll(b2,40-d,-6.2,180,d)
        q=ease(t/DUR); camset(LV((0,-21.0,6.6),(0,-19.8,6.2),q),(0,-2.0,2.3),16,8)
    return dict(upd=upd)
SHOTS['MEET']=MEET
def LINE():
    arena('kv_gold',gtext=False); LF=mkfans('L',focus=(0,-2)); KF=mkfans('K',focus=(0,-2)); rf=ref_mk(0,-1.2,0); whistle(rf); FILLE[0]=30
    def upd(t):
        fans(LF,t,'idle',look=hp(rf)); fans(KF,t,'idle',look=hp(rf))
        d=1.3*t; place(rf,0,-1.2-d,0); walk(rf,d,step=.48,arm=18); blink(rf,t); face(rf,mouth='flat',brow=-.02,brow_r=-6)
        q=ease(t/DUR); camset(LV((0,-9.2,.45),(0,-8.4,1.5),q),LV((0,4.0,1.2),(0,3.0,2.0),q),21,8)
    return dict(upd=upd)
SHOTS['LINE']=LINE
def SETTLE():
    arena('kv_gold',gtext=False); LF=mkfans('L',focus=(0,BACKY)); KF=mkfans('K',focus=(0,BACKY)); FILLE[0]=0
    def upd(t):
        fans(LF,t,'idle',look=(0,BACKY,6)); fans(KF,t,'idle',look=(0,BACKY,6))
        q=ease(t/DUR); camset(LV((0,BACKY-12.6,6.0),(0,BACKY-11.2,6.25),q),(0,BACKY,6.45),25,8)
    return dict(upd=upd)
SHOTS['SETTLE']=SETTLE
def round_card(l1,l2,col,cam0,cam1,mood='kv_gold'):
    def f():
        arena(mood,gtext=False); LF=mkfans('L',focus=REFP); KF=mkfans('K',focus=REFP); rf=ref_mk(); whistle(rf); bd=placard(rf,l1,l2,col); FILLE[0]=40
        def upd(t):
            fans(LF,t,'fist' if t>.5 else 'idle',look=hp(rf)); fans(KF,t,'fist' if t>.5 else 'idle',look=hp(rf))
            place(rf,REFP[0],REFP[1],0); hstand(rf,t); k=tl(t,0,.3); s_=.6+.4*k; bd.scale=(s_,s_,s_); bd.location=(0,-.3*rf['u'],L(5.6,7.05,k)*rf['u'])
            bpy.context.view_layer.update(); hold_board(rf,bd,1.0); face(rf,mouth='O' if t<.5 else 'flat',brow=.03)
            q=ease(t/DUR); camset(LV(cam0,cam1,q),(0,-.7,2.55),25,8)
        return dict(upd=upd)
    return f
SHOTS['ROUND1']=round_card('ROUND 1','FOOD','#C8372D',(.4,-6.4,2.2),(.3,-5.6,2.3))
# ---------------------------------------------------------------- 13-17 food round
LT=(-2.5,-.55); KT=(2.5,-.25); SHF=(-2.5,.9,18); GUF=(2.5,.95,-18)
def food_set(mood='kv_gold',skipL=(0,),skipK=(0,)):
    arena(mood); nt=nashta_table(LT[0],LT[1],0); dg=degh(KT[0],KT[1],0)
    LF=mkfans('L',skip=skipL,focus=(-2.5,.0)); KF=mkfans('K',skip=skipK,focus=(2.5,.0)); sh,gu=captains(); return LF,KF,sh,gu,nt,dg
def food_idle(sh,gu,t):
    cap_idle(sh,t,*SHF,other=(-1.0,-5,2.3)); cap_idle(gu,t,*GUF,other=(1.0,-5,2.3))
def NASHTA():
    LF,KF,sh,gu,nt,dg=food_set(); FILLE[0]=40
    items=[(LT[0]-.8,LT[1]+.05,1.2),(LT[0]-.2,LT[1]+.12,1.2),(LT[0]+.42,LT[1]+.1,1.35),(LT[0]+.92,LT[1]-.3,1.4)]
    def upd(t):
        food_idle(sh,gu,t); crossed(gu)
        times=[ws(74),ws(75),ws(76),ws(77)]
        ix=max([i for i,x in enumerate(times) if t>=x-.1] or [0]); swp=tl(t,ws(78)-.1,ws(80))
        tgt=Vector(items[ix]); look_at(sh,tgt if (swp<.5 and t>times[0]-.1) else (-1.5,-5,2.3),1.0,maxpitch=14)
        kk=tl(t,times[0]-.3,times[0]); sd=1 if tgt.x>sh['root'].location[0] else -1
        for s in (1,-1): sh['arm'][s].rotation_euler=(R(-8),R(-s*6),0)
        if swp<.5: arm_to(sh,sd,tgt,kk*(1-2*swp),base=(R(-8),R(-sd*6),0))
        if swp>0:
            for s in (1,-1): arm_to(sh,s,root_mat(sh)@Vector((s*4.2*sh['u'],-1.9*sh['u'],2.6*sh['u'])),ease(min(1,swp*1.6)),base=tuple(sh['arm'][s].rotation_euler))
        face(sh,mouth='smile',brow=.02); speak(sh,t,74,82,gesture=False)
        fans(LF,t,'cheer' if t>ws(80) else 'smile',look=hp(sh)); fans(KF,t,'glare',look=hp(sh))
        q=ease(t/DUR); camset(LV((-1.45,-4.6,2.5),(-1.6,-4.0,2.45),q),LV((-2.5,.25,1.6),(-2.5,.3,1.7),q),26,8)
    return dict(upd=upd)
SHOTS['NASHTA']=NASHTA
def BIRYANI():
    LF,KF,sh,gu,nt,dg=food_set(); FILLE[0]=40; lid=dg['lid']; st=steam((KT[0],KT[1],1.15),ws(84),DUR+1,n=12,size=.06)
    al=in_hand(gu,1,lambda e: oico((0,-.1,.12),.14,M('#E0B45A',.6),e,sc=(1.2,1,.85),sub=2)); al.scale=(0,0,0)
    def upd(t):
        food_idle(sh,gu,t); crossed(sh)
        up=tl(t,ws(84)-.15,ws(86)); lid.location=(-1.25*up,1.74*up,1.42+1.0*up); lid.rotation_euler=(R(-18*up),R(-72*up),0)
        bpy.context.view_layer.update(); lp=lid.matrix_world@Vector((-.55,0,.12))
        arm_to(gu,-1,lp,tl(t,ws(84)-.35,ws(84)),base=(0,0,0))
        sh_=tl(t,ws(87)-.25,ws(87)+.1); al.scale=(sh_,sh_,sh_)
        gu['arm'][1].rotation_euler=(R(-82*sh_),0,R(42*sh_)); upright(al,gu,1) if sh_>0 else None
        look_at(gu,(1.5,-5,2.3),1.0,maxpitch=20); face(gu,mouth='smirk',brow=.02); speak(gu,t,83,89,gesture=False)
        fans(KF,t,'cheer' if t>ws(87) else 'smile',look=hp(gu)); fans(LF,t,'glare',look=hp(gu))
        q=ease(t/DUR); camset(LV((1.45,-4.6,2.5),(1.6,-4.0,2.45),q),LV((2.5,.25,1.55),(2.5,.3,1.7),q),26,8)
    return dict(upd=upd)
SHOTS['BIRYANI']=BIRYANI
def ALOO2():
    BOARD[0]=False
    LF,KF,sh,gu,nt,dg=food_set(); FILLE[0]=50
    def upd(t):
        food_idle(sh,gu,t); crossed(gu)
        k=tl(t,0,.22); sh['root'].rotation_euler[0]=R(-5*k); what_pose(sh,k,t)
        look_at(sh,(-2.0,-3,2.6),1.0); face(sh,mouth='O',brow=.06,eyes=1.18); speak(sh,t,90,92,gesture=False)
        fans(LF,t,'gasp',look=(KT[0],KT[1],1.2)); fans(KF,t,'smile',look=hp(sh))
        q=ease(t/DUR); camset(LV((-2.05,-2.2,2.62),(-2.15,-1.9,2.6),q),(-2.5,.9,2.33),30,8)
    return dict(upd=upd)
SHOTS['ALOO2']=ALOO2
def PULAO():
    BOARD[0]=False
    LF,KF,sh,gu,nt,dg=food_set(); FILLE[0]=50
    def upd(t):
        food_idle(sh,gu,t); what_pose(sh,1,t,amp=.5); face(sh,mouth='O',brow=.06,eyes=1.15)
        p=tl(t,ws(95)-.2,ws(95)+.1); arm_to(gu,-1,hp(sh),p,base=(0,0,0)); gu['arm'][1].rotation_euler=(R(-10),R(-8),0)
        look_at(gu,(2.0,-3,2.5),1.0); face(gu,mouth='smirk',brow=.03,brow_r=6); speak(gu,t,93,98,gesture=False)
        fans(KF,t,'laugh' if t>ws(96) else 'smile',look=hp(sh)); fans(LF,t,'gasp',look=hp(gu))
        q=ease(t/DUR); camset(LV((2.05,-2.2,2.6),(2.15,-1.9,2.58),q),(2.5,.95,2.3),30,8)
    return dict(upd=upd)
SHOTS['PULAO']=PULAO
def ENDED():
    LF,KF,sh,gu,nt,dg=food_set(); rf=ref_mk(0,-.9,0); whistle(rf); FILLE[0]=20
    def upd(t):
        cap_idle(sh,t,-1.35,1.25,90,hp(gu)); cap_idle(gu,t,1.35,1.25,-90,hp(sh))
        for H in (sh,gu):
            H['arm'][1].rotation_euler=(R(-95+14*math.sin(t*11+H['seed'])),R(-6),0); face(H,mouth='shout' if int(t*6+H['seed'])%2 else 'O',brow=-.03,brow_r=-14); H['root'].rotation_euler[0]=R(6)
        place(rf,0,-.9,0); hstand(rf,t); spread(rf,1,ang=70,fw=-30); face(rf,mouth='O',brow=.05); rf['head'].rotation_euler=(0,0,R(30*math.sin(t*5)))
        fans(LF,t,'fist',look=hp(gu)); fans(KF,t,'fist',look=hp(sh))
        q=ease(t/DUR); camset(LV((0,-8.6,3.4),(0,-7.6,3.0),q),(0,.6,1.75),24,8)
    return dict(upd=upd)
SHOTS['ENDED']=ENDED
