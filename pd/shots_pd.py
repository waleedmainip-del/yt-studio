# "Pindi vs the Dinosaur": shots. Rig note: brow_r POSITIVE = angry slant, NEGATIVE = worried slant. Dino faces -y at rz=0.
SEQ=[('HOOK', 0.0), ('EXCEPT', 2.933), ('ISB', 5.567), ('CLEAN', 8.567), ('VISIT', 11.933), ('BRO', 14.367), ('WOKE', 17.0), ('FORTY', 19.767), ('WALKING', 22.267), ('DOES', 24.367), ('CHILL', 26.933), ('CALLED', 29.267), ('EVERYONE', 30.633), ('SAHAB', 32.267), ('COMMITTEE', 33.767), ('GUARD', 35.2), ('ENTRY', 36.867), ('ATE', 37.867), ('CHALLAN', 39.6), ('NOTHING', 41.633), ('QUESTION', 42.7), ('PLANB', 44.433), ('HAI', 45.767), ('TWELVE', 48.2), ('BURGER', 50.633), ('DINOAA', 52.133), ('KINNA', 54.5), ('CHAALIS', 55.567), ('BAS', 56.633), ('ALONE', 58.333), ('BIKES', 59.933), ('SILENCER', 61.367), ('ROARED', 63.067), ('LOOKED', 64.933), ('ROARBACK', 66.767), ('FIRST', 68.5), ('SCARED', 71.5), ('INSPECT', 73.267), ('SILNAHI', 76.067), ('WHEELIE', 78.567), ('AVERAGE', 80.767), ('CHAKKAR', 82.067), ('NOBODY', 83.933), ('SELFIE', 86.267), ('SUNGLASS', 88.0), ('ROUND', 89.933), ('THREEH', 91.933), ('NEVER', 94.0), ('NEXTFRI', 96.567), ('PINDINOT', 99.367), ('NAMED', 100.7), ('SHERU', 102.267), ('MAMUQ', 104.933), ('MAMU', 107.767), ('MONSTER', 110.5), ('RIDE', 112.633), ('CTA', 114.133)]
END=118.1333
WI={'HOOK': 0, 'EXCEPT': 8, 'ISB': 12, 'CLEAN': 18, 'VISIT': 24, 'BRO': 30, 'WOKE': 36, 'FORTY': 44, 'WALKING': 49, 'DOES': 55, 'CHILL': 60, 'CALLED': 66, 'EVERYONE': 70, 'SAHAB': 74, 'COMMITTEE': 78, 'GUARD': 82, 'ENTRY': 87, 'ATE': 90, 'CHALLAN': 94, 'NOTHING': 100, 'QUESTION': 102, 'PLANB': 106, 'HAI': 110, 'TWELVE': 117, 'BURGER': 123, 'DINOAA': 126, 'KINNA': 132, 'CHAALIS': 135, 'BAS': 137, 'ALONE': 140, 'BIKES': 145, 'SILENCER': 148, 'ROARED': 151, 'LOOKED': 154, 'ROARBACK': 161, 'FIRST': 165, 'SCARED': 173, 'INSPECT': 177, 'SILNAHI': 184, 'WHEELIE': 192, 'AVERAGE': 199, 'CHAKKAR': 203, 'NOBODY': 208, 'SELFIE': 215, 'SUNGLASS': 219, 'ROUND': 224, 'THREEH': 231, 'NEVER': 236, 'NEXTFRI': 244, 'PINDINOT': 250, 'NAMED': 253, 'SHERU': 257, 'MAMUQ': 265, 'MAMU': 272, 'MONSTER': 279, 'RIDE': 283, 'CTA': 287}
SHOTS={}
# portrait frame: 36 mm is the VERTICAL sensor size, so half-width/distance = 10.125/lens
def cam2(t,p0,p1,tg,lens,tg1=None,fs=8):
    q=ease(t/DUR); camset(LV(p0,p1,q),tg if tg1 is None else LV(tg,tg1,q),lens,fs)
def headw(H): return H['root'].matrix_world@Vector((0,0,4.75*H['u']))
def c1(t,H,yaw=12,dist=2.8,lens=36,dz=0.0,tz=-.22,push=.08,ref=None,q=None,sx=0.0):
    """single: camera in front of H (yaw degrees round from its facing), slow push-in"""
    h=headw(H); a=(H['root'].rotation_euler[2] if ref is None else R(ref))+R(yaw); f=Vector((math.sin(a),-math.cos(a),0)); d=dist*(1-push*(ease(t/DUR) if q is None else q)); h=h+Vector((-f.y,f.x,0))*sx
    camset(tuple(h+f*d+Vector((0,0,dz))),(h.x,h.y,h.z+tz),lens,8)
def c2(t,Ha,Hb,frm=(0,-1),lens=30,fit=1.0,dz=.1,tz=-.6,push=.07,sh=0.0,pad=1.5,cx=0.0):
    """two-shot square on to the pair, from the side that frm points to; distance set so both fit"""
    a=headw(Ha); b=headw(Hb); m=(a+b)/2; d=b-a; d.z=0; n=Vector((-d.y,d.x,0)).normalized(); m=m+d.normalized()*cx
    if n.x*frm[0]+n.y*frm[1]<0: n=-n
    dist=(d.length+pad)/(2*10.125/lens)*fit*(1-push*ease(t/DUR))
    camset(tuple(m+n*dist+d.normalized()*sh+Vector((0,0,dz))),(m.x,m.y,m.z+tz),lens,8)
def fc(H,m):
    F=dict(calm=dict(mouth='smile',brow=0,brow_r=0,eyes=1.0),flat=dict(mouth='flat',brow=.01,brow_r=0,eyes=.9),bored=dict(mouth='flat',brow=.02,brow_r=-3,eyes=.78),happy=dict(mouth='grin',brow=.04,brow_r=0,eyes=1.05),
           shock=dict(mouth='O',brow=.07,brow_r=-6,eyes=1.3),worry=dict(mouth='o',brow=.05,brow_r=-12,eyes=1.15),sad=dict(mouth='frown',brow=.03,brow_r=-12,eyes=1.0),firm=dict(mouth='flat',brow=-.02,brow_r=8,eyes=.95),
           smug=dict(mouth='smile',brow=.03,brow_r=6,eyes=.82),dead=dict(mouth='flat',brow=.01,brow_r=0,eyes=.8),wow=dict(mouth='o',brow=.06,brow_r=0,eyes=1.25),laugh=dict(mouth='grin',brow=.05,brow_r=-4,eyes=.6),
           shout=dict(mouth='shout',brow=.05,brow_r=6,eyes=1.15),scream=dict(mouth='shout',brow=.07,brow_r=-10,eyes=1.3))
    face(H,**F[m])
def runp(H,t,x0,y0,rz,v=6.0,ph=0.0):
    """run in a straight line from (x0,y0) heading rz"""
    f=fwd(rz); d=v*t; H['root'].location[0]=x0+f[0]*d; H['root'].location[1]=y0+f[1]*d; H['root'].rotation_euler[2]=R(rz); run(H,d+ph,arm=50); blink(H,t)
def lamp(loc,e,col=(1,.86,.62),r=.6,shadow=False): return point(loc,e,col,r=r,shadow=shadow)
# ================================================================ Islamabad avenue
def ebox(parts,loc=(0,0,0),parent=None):
    e=empty(loc,parent)
    for (c,s_,m,bv) in parts: obox(c,s_,m,bv,e)
    return e
def HOOK():
    isb('pd_dusk',.4); D=dino((5.75,24,0),0); FILLE[0]=70
    X=[(3.2,13.0,5),(8.2,15.5,-5),(5.6,18.5,2),(-4.2,14.0,-7),(-7.2,17.0,8),(1.0,20.0,3)]
    P=[mk(ISBP[k] if k<5 else COMM[2],x,y,rz,'p%d'%k) for k,(x,y,rz) in enumerate(X)]; C=kcar((-5.75,34,0),-90,'#C9CED8',3)
    def upd(t):
        d=1.7*t; D['root'].location[1]=27-d; rr=dino_roar(t,.35,2.5); dino_pose(D,t,dist=d,pitch=12+6*rr,neck=30,head=4+12*rr,jaw=rr); dino_face(D,'angry')
        for k,H in enumerate(P):
            x,y,rz=X[k]; runp(H,t,x,y,rz,v=3.7,ph=k*.37); fc(H,'scream')
            if k%2==0: arms_up(H,1,t,spread=22,jig=14)
        roll(C,-5.75,34-8*t,-90,8*t)
        cam2(t,(4.4,-1.2,1.2),(4.7,-.4,1.25),(5.6,12,5.4),24,(5.6,12,6.0))
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
def EXCEPT():
    isb('pd_dusk',.4,arm=False); D=dino((5.75,15.5,0),0); FILLE[0]=110; XY=((5.75,2.2),(3.7,3.9),(7.8,3.9))
    V=[pbike((x,y,0),-90,BKC[k],rider=c,name='b%d'%k) for k,((x,y),c) in enumerate(zip(XY,(SHANI,BILLA,GOGA)))]
    cu=cup_of(V[0]['rider'],1); ph=phone_of(V[1]['rider'],1)
    def upd(t):
        rr=dino_roar(t,.15,2.3); dino_pose(D,t,pitch=2,neck=10,head=-24,jaw=rr,hz=-.3); dino_face(D,'angry')
        for k,v in enumerate(V): bike_roll(v,XY[k][0],XY[k][1],-90,0); bike_sit(v,t)
        S=V[0]['rider']; hold_chai(S,cu,1,sip=ease((t-.8)/.45)*(1-ease((t-1.8)/.4))); fc(S,'bored'); S['arm'][-1].rotation_euler=(R(-20),0,0)
        Bi=V[1]['rider']; phone_up(Bi,1,h=3.3); Bi['head'].rotation_euler[0]=R(14); fc(Bi,'flat'); Bi['arm'][-1].rotation_euler=(R(-20),0,0)
        G=V[2]['rider']; crossed(G); face(G,mouth='O' if .9<t<1.9 else 'flat',brow=.03,brow_r=-4,eyes=.5 if .9<t<1.9 else .8)
        cam2(t,(5.75,-5.8,1.9),(5.75,-5.0,1.95),(5.75,3.5,4.3),24)
    return dict(upd=upd)
SHOTS['EXCEPT']=EXCEPT
def ISB():
    isb('pd_gold',0.0); FILLE[0]=0
    C=[kcar((5.75,-20,0),90,'#F4F1EA',1),kcar((-5.75,40,0),-90,'#2B58C9',2),kcar((5.75,30,0),90,'#C8372D',3)]; J=mk(ISBP[1],11.8,-20,180,'jog')
    def upd(t):
        roll(C[0],5.75,-24+9*t,90,9*t); roll(C[1],-5.75,46-9*t,-90,9*t); roll(C[2],5.75,34+9*t,90,9*t); runp(J,t,11.6,-18,180,v=2.8); fc(J,'calm')
        cam2(t,(0,-40,13.5),(0,-36.5,11.8),(0,30,8.5),32,(0,30,9.3))
    return dict(upd=upd)
SHOTS['ISB']=ISB
def CLEAN():
    isb('pd_gold',0.0); FILLE[0]=40; J=mk(ISBP[1],-11.6,36,0,'jog'); Aw=mk(ISBP[0],-10.3,45,0,'wk'); St=mk(ISBP[3],-13.7,27.4,90,'st'); ph=phone_of(St,1)
    def upd(t):
        runp(J,t,-11.6,36,0,v=2.6); fc(J,'calm'); Aw['root'].location[1]=45-1.2*t; walk(Aw,1.2*t,step=.5); blink(Aw,t); fc(Aw,'calm')
        standp(St,t,-13.7,27.4,90); phone_up(St,1); St['head'].rotation_euler[0]=R(12); fc(St,'calm')
        cam2(t,(-9.9,21.0,1.35),(-10.2,22.4,1.5),(-11.3,31,2.4),28,(-11.4,31,2.3))
    return dict(upd=upd)
SHOTS['CLEAN']=CLEAN
WP=(-11.6,-4.0,135); RP=(-11.6,-1.2,45)
def cafe2(mood='pd_gold',night=0.0):
    isb(mood,night); wa=mk(WALEED,WP[0],WP[1],WP[2],'waleed'); ra=mk(RAYYAN,RP[0],RP[1],RP[2],'rayyan'); return wa,ra
def VISIT():
    wa,ra=cafe2(); FILLE[0]=60; cu=cup(ra,1); cw=cup_of(wa,-1)
    def upd(t):
        standp(wa,t,*WP); standp(ra,t,*RP); hold_chai(wa,cw,-1); hold(ra,1,-64); fc(wa,'calm'); fc(ra,'smug'); look_at(wa,headw(ra),.7); look_at(ra,headw(wa),.6)
        c2(t,wa,ra,frm=(1,0),lens=30,pad=1.9,tz=-.75)
    return dict(upd=upd)
SHOTS['VISIT']=VISIT
def BRO():
    wa,ra=cafe2(); FILLE[0]=70; cu=cup(ra,1)
    def upd(t):
        standp(wa,t,*WP); standp(ra,t,*RP); fc(wa,'calm'); fc(ra,'smug'); speak(ra,t,30,35,s=-1); look_at(ra,headw(wa),.45)
        k=ease((t-we(35)-.05)/.35); hold_chai(ra,cu,1,a=-64,sip=k*.9)
        c1(t,ra,yaw=24,dist=3.4,lens=36,tz=-.4)
    return dict(upd=upd)
SHOTS['BRO']=BRO
def WOKE():
    isb('pd_dusk',.3); D=dino((22,184,7.5),0); FILLE[0]=0; r=random.Random(4); BR=[]
    for k in range(9):
        e=empty((0,0,-50)); dm=M('#1A1A22',.6)
        for s in (1,-1): obox((s*.28,0,.08),(.3,.09,.03),dm,0,e,rot=(0,R(-s*22),0))
        BR.append((e,r.uniform(12,34),r.uniform(170,176),r.uniform(12,15),r.uniform(-3,3),r.uniform(0,.5)))
    def upd(t):
        k=ease((t-.35)/1.7); D['root'].location[2]=7.5-9.5*(1-k); dino_pose(D,t,pitch=-14+22*k,neck=6+30*k,head=-8+10*k,jaw=.55*ease((t-1.9)/.5)); dino_face(D,'shut' if k<.45 else 'angry')
        for i,(e,x,y,z,vx,dl) in enumerate(BR):
            q=max(0,t-.3-dl); e.location=(x+vx*q,y-2*q,z+4.5*q+.3*math.sin(q*9+i)) if q>0 else (0,0,-50); e.rotation_euler=(0,R(18*math.sin(q*16+i)),R(i*40))
        cam2(t,(20,138,7.5),(20.4,141.5,8.0),(22,176,14.5),58,(22,176,16.0))
    return dict(upd=upd)
SHOTS['WOKE']=WOKE
def FORTY():
    isb('pd_dusk',.4); D=dino((5.75,62,0),0); FILLE[0]=40; C=kcar((8.6,49,0),90,'#F4F1EA',5)
    def upd(t):
        d=2.2*t; D['root'].location[1]=62-d; dino_pose(D,t,dist=d+1.0,pitch=8,neck=26,head=-8,jaw=.4+.12*math.sin(t*4)); dino_face(D,'angry'); roll(C,8.6,49,90,0)
        q=ease(t/DUR); camset((3.3,43.6,.9+.5*q),(5.6,51.5-1.2*q,2.2+5.2*q),20,8)
    return dict(upd=upd)
SHOTS['FORTY']=FORTY
def WALKING():
    isb('pd_dusk',.4); D=dino((5.75,60,0),0); FILLE[0]=0; X=[(3.2,24.5,4),(6.6,28,-3),(8.7,31,2),(-4.2,26.5,-5),(-7.0,30,6),(4.9,33.5,1)]
    P=[mk(ISBP[k] if k<5 else COMM[2],x,y,rz,'p%d'%k) for k,(x,y,rz) in enumerate(X)]; C=[kcar((-5.75,30,0),-90,'#C8372D',7),kcar((-5.75,14,0),-90,'#F4F1EA',8)]
    def upd(t):
        d=1.9*t; y=54-d; D['root'].location[1]=y; dino_pose(D,t,dist=d+2.0,pitch=9,neck=28,head=-6,jaw=.3); dino_face(D,'angry')
        for k,H in enumerate(P):
            x,yy,rz=X[k]; runp(H,t,x,yy,rz,v=4.0,ph=k*.4); fc(H,'scream')
            if k%2==1: arms_up(H,1,t,spread=22,jig=14)
        roll(C[0],-5.75,30-11*t,-90,11*t); roll(C[1],-5.75,14-11*t,-90,11*t)
        camset((10.2,y+15.5,12.2-.3*ease(t/DUR)),(4.8,y-22,1.5),24,8)
    return dict(upd=upd)
SHOTS['WALKING']=WALKING
RD=(-10.6,10.8,90)
def DOES():
    isb('pd_dusk',.4); FILLE[0]=90; ra=mk(RAYYAN,*RD,'rayyan'); a=mk(ISBP[0],-10.6,12.75,90,'ia'); b=mk(ISBP[3],-10.6,8.85,90,'ib'); G=[ra,a,b]; PH=[phone_of(H,1) for H in G]; dn=(5.75,46,7)
    def upd(t):
        for i,H in enumerate(G):
            standp(H,t,-10.6,(10.8,12.75,8.85)[i],90); look_at(H,dn,.9,maxyaw=70); fc(H,'flat'); k=ease((t-.75)/.4); phone_up(H,1,k,h=4.3,fw=1.2,sx=.45)
        cam2(t,(-2.6,11.4,2.0),(-3.4,11.2,2.05),(-10.6,10.8,2.2),28)
    return dict(upd=upd)
SHOTS['DOES']=DOES
def CHILL():
    isb('pd_dusk',.4); FILLE[0]=90; ra=mk(RAYYAN,*RD,'rayyan'); ph=phone_of(ra,1)
    def upd(t):
        standp(ra,t,*RD); fc(ra,'smug'); speak(ra,t,60,65,gesture=False); k=1-ease((t-we(60)-.25)/.4); ra['arm'][-1].rotation_euler=(R(-78*k-6),R(10*k),0); phone_up(ra,1,1,h=3.5,fw=1.1,sx=.5)
        c1(t,ra,yaw=-22,dist=2.9,lens=38)
    return dict(upd=upd)
SHOTS['CHILL']=CHILL
def CALLED():
    isb('pd_dusk',.4); FILLE[0]=90; ra=mk(RAYYAN,*RD,'rayyan'); ph=phone_of(ra,1)
    def upd(t):
        standp(ra,t,*RD); fc(ra,'calm'); ear(ra,1,1); ra['head'].rotation_euler[1]=R(5)
        c1(t,ra,yaw=20,dist=2.7,lens=42,push=.1)
    return dict(upd=upd)
SHOTS['CALLED']=CALLED
def EVERYONE():
    isb('pd_dusk',.4); FILLE[0]=90; G=[mk(RAYYAN if k==0 else ISBP[k-1],-10.8,6.0+2.3*k,90,'e%d'%k) for k in range(5)]; PH=[phone_of(H,1) for H in G]
    def upd(t):
        for k,H in enumerate(G): standp(H,t,-10.8,6.0+2.3*k,90); fc(H,'calm' if k%2==0 else 'flat'); ear(H,1,1); H['head'].rotation_euler[2]=R(-18)
        cam2(t,(-6.2,-2.0,2.0),(-6.4,-1.3,2.0),(-11.0,11,2.1),35)
    return dict(upd=upd)
SHOTS['EVERYONE']=EVERYONE
def SAHAB():
    office(True); FILLE[0]=30; pa=mk(PA,2.0,2.6,0,'pa'); ph=phone_of(pa,1)
    def upd(t):
        standp(pa,t,2.0,2.6,0); fc(pa,'bored'); ear(pa,1,1); speak(pa,t,74,77,gesture=False); pa['arm'][-1].rotation_euler=(R(-6),0,0)
        cam2(t,(2.5,-2.6,2.3),(2.4,-2.0,2.3),(2.0,2.6,2.55),34)
    return dict(upd=upd)
SHOTS['SAHAB']=SAHAB
def ctable(x=-5.75,y=8.0,banner=True):
    wd=M('#F4F1EA',.8,kind='fabric'); B.box((x,y,1.0),(2.3,.55,.04),wd,.02); B.box((x,y-.56,.55),(2.3,.02,.5),M('#1E6A3A',.8,kind='fabric'),0)
    for k in range(3):
        B.cyl((x-1.4+k*1.4,y-.1,1.1),.07,.1,M('#F6F4EE',.4),seg=10,r2=.09)
        for j in range(4): B.box((x-1.9+k*1.4,y+.1,1.06+.035*j),(.26,.2,.015),M(('#F2C14E','#8FB8D8','#E8554D','#F4F1EA')[(j+k)%4],.7),.004)
    if banner:
        for s in (-1,1): B.cyl((x+s*2.6,y+2.3,2.3),.05,4.6,M('#C9CED8',.4,metal=.5),seg=6)
        sign('DINOSAUR COMMITTEE',(x,y+2.3,3.9),.32,'#FFFFFF','#1E6A3A',n=(0,-1,0),pad=.22,th=.05,frame='#F2C14E')
    B.done('ctable')
def COMMITTEE():
    isb('pd_dusk',.4); ctable(); FILLE[0]=90; G=[mk(COMM[k],-7.75+2*k,9.1,0,'c%d'%k) for k in range(3)]; CU=[cup_of(G[1],1)]
    Rn=[mk(ISBP[2],-9.0,16,0,'r0'),mk(ISBP[4],-2.6,19,0,'r1')]
    def upd(t):
        for k,H in enumerate(G): standp(H,t,-7.75+2*k,9.1,0); fc(H,'firm' if k!=1 else 'calm')
        hold_chai(G[1],CU[0],1,sip=ease((t-.3)/.4)); crossed(G[0]); G[2]['arm'][1].rotation_euler=(R(-95+8*math.sin(t*9)),0,R(10)); look_at(G[0],headw(G[1]),.5); look_at(G[2],headw(G[1]),.5)
        runp(Rn[0],t,-9.0,17,-4,v=4.2); runp(Rn[1],t,-2.4,21,5,v=4.2,ph=.5); fc(Rn[0],'scream'); fc(Rn[1],'scream'); arms_up(Rn[1],1,t,spread=22,jig=14)
        cam2(t,(-5.75,.2,2.5),(-5.75,.9,2.5),(-5.75,8,2.45),30)
    return dict(upd=upd)
SHOTS['COMMITTEE']=COMMITTEE
GP=(5.75,13.2,180)
def gstage(dy=28.0,arm=True):
    isb('pd_dusk',.45,arm=arm); D=dino((5.75,dy,0),0); g=mk(GUARD,*GP,'guard'); FILLE[0]=90; return D,g
def GUARD_():
    D,g=gstage()
    def upd(t):
        d=min(2.0,1.6*t); k=ease(t/1.2); D['root'].location[1]=30-d; dino_pose(D,t,dist=d if t<1.25 else None,pitch=8-10*k,neck=24-16*k,head=-6-22*k,jaw=.25); dino_face(D,'angry',mix=('curious',k))
        standp(g,t,*GP); fc(g,'firm'); g['arm'][1].rotation_euler=(R(-150*ease(t/.35)),R(26*ease(t/.35)),0); look_at(g,dino_headw(D),.9,maxpitch=40)
        cam2(t,(4.2,7.6,1.2),(4.3,8.2,1.25),(5.75,20,5.0),24)
    return dict(upd=upd)
SHOTS['GUARD']=GUARD_
def ENTRY():
    D,g=gstage()
    def upd(t):
        D['root'].location[1]=28; dino_pose(D,t,pitch=-2,neck=8,head=-28,jaw=.25); standp(g,t,*GP); fc(g,'firm'); speak(g,t,87,89,gesture=False); g['arm'][1].rotation_euler=(R(-62),R(-8),0); g['head'].rotation_euler[0]=R(-14)
        c1(t,g,yaw=-18,dist=3.0,lens=40,dz=-.15,tz=-.2)
    return dict(upd=upd)
SHOTS['ENTRY']=ENTRY
def ATE():
    D,g=gstage(); A=BARR['arm']; rest=Vector((9.85,17.3,1.3))
    def upd(t):
        D['root'].location[1]=27.2; a=ease(t/.5); b=ease((t-.62)/.55); bite=1 if t>.56 else 0
        dino_pose(D,t,pitch=-16*a+18*b,neck=4-34*a+44*b,head=-30-22*a+40*b,jaw=(.95*a if not bite else .22+.2*abs(math.sin((t-.56)*9))*(t>1.1)),hz=-1.5*a+1.2*b); dino_face(D,'angry' if t<1.0 else 'happy')
        if bite: m=dino_mouthw(D); A.location=(m.x+3.9,m.y-.25,m.z+.05); A.rotation_euler=(0,R(-10*b),R(6*b))
        else: A.location=rest; A.rotation_euler=(0,0,0)
        standp(g,t,*GP); fc(g,'shock' if t>.6 else 'firm'); look_at(g,dino_headw(D),.9,maxpitch=40)
        cam2(t,(.9,10.2,1.9),(1.2,10.6,2.0),(6.0,17.3,2.3),28,(6.0,17.6,4.2))
    return dict(upd=upd)
SHOTS['ATE']=ATE
def pad_in(H,s=-1):
    return in_hand(H,s,lambda e:(obox((0,-.16,.1),(.13,.02,.19),M('#F4F1EA',.6),.01,e,rot=(R(-58),0,0)),obox((0,-.17,.27),(.135,.022,.03),M('#C8372D',.6),.005,e,rot=(R(-58),0,0))))
def CHALLAN():
    D,g=gstage(arm=False); pd_=pad_in(g,-1); pen=in_hand(g,1,lambda e: obox((0,-.1,.08),(.016,.016,.11),M('#16171C',.4),.004,e,rot=(R(-30),0,0)))
    def upd(t):
        D['root'].location[1]=27.2; dino_pose(D,t,pitch=4,neck=22,head=-16,jaw=.3+.2*abs(math.sin(t*7))); standp(g,t,*GP); fc(g,'dead'); speak(g,t,94,99,gesture=False)
        phone_up(g,-1,1,h=3.15,fw=1.15,sx=.4); phone_up(g,1,1,h=3.3+.05*math.sin(t*22),fw=1.2,sx=.12+.07*math.sin(t*17)); k=ease((t-we(97))/.3); g['head'].rotation_euler[0]=R(16-34*k)
        c1(t,g,yaw=16,dist=3.5,lens=38,dz=-.1,tz=-.55)
    return dict(upd=upd)
SHOTS['CHALLAN']=CHALLAN
def NOTHING():
    isb('pd_dusk',.45,arm=False); D=dino((5.75,25,0),0); FILLE[0]=90; g=mk(GUARD,5.75,13.2,0,'guard')
    def upd(t):
        rr=dino_roar(t,.0,.95); dino_pose(D,t,pitch=14+6*rr,neck=30,head=2+10*rr,jaw=max(.3,rr)); dino_face(D,'angry')
        runp(g,t,6.3,13.6,-3,v=4.4); fc(g,'scream'); arms_up(g,1,t,spread=22,jig=14)
        cam2(t,(4.3,4.2,1.05),(4.4,4.7,1.1),(5.75,15,5.2),20)
    return dict(upd=upd)
SHOTS['NOTHING']=NOTHING
W2=(-10.9,-1.9,80); R2=(-10.9,-4.4,100)
def hide2(mood='pd_dusk',night=.45):
    isb(mood,night,arm=False); wa=mk(WALEED,*W2,'waleed'); ra=mk(RAYYAN,*R2,'rayyan'); FILLE[0]=90; return wa,ra
def QUESTION():
    wa,ra=hide2(); ph=phone_of(ra,1)
    def upd(t):
        standp(wa,t,*W2); standp(ra,t,*R2); k=ease((t-.75)/.4); fc(wa,'worry'); look_at(wa,LV((5.75,22,7),tuple(headw(ra)),k),1.0,maxyaw=80)
        what_pose(wa,1-k,t,.5); ear(ra,1,1); fc(ra,'worry')
        c1(t,wa,yaw=-12,dist=3.1,lens=40,ref=90)
    return dict(upd=upd)
SHOTS['QUESTION']=QUESTION
def PLANB():
    wa,ra=hide2(); ph=phone_of(ra,1)
    def upd(t):
        standp(wa,t,W2[0],W2[1],50); standp(ra,t,R2[0],R2[1],140); fc(wa,'worry'); speak(wa,t,106,109,gesture=False); what_pose(wa,1,t,.6); look_at(wa,headw(ra),.6); look_at(ra,headw(wa),.6); fc(ra,'worry')
        k=ease((t-.2)/.4); ear(ra,1,1-k); 
        c2(t,wa,ra,frm=(1,0),lens=32,pad=1.7,sh=.5)
    return dict(upd=upd)
SHOTS['PLANB']=PLANB
def HAI():
    wa,ra=hide2(); ph=phone_of(ra,1)
    def upd(t):
        standp(wa,t,W2[0],W2[1],50); standp(ra,t,R2[0],R2[1],140); fc(ra,'worry'); speak(ra,t,110,116,gesture=False); k=ease((t-we(110)-.1)/.4); ra['head'].rotation_euler[2]=R(14*k); ra['head'].rotation_euler[0]=R(8*k)
        ra['arm'][1].rotation_euler=(R(-30),0,R(6)); face(ra,brow_r=-12)
        c1(t,ra,yaw=-12,dist=3.5,lens=40)
    return dict(upd=upd)
SHOTS['HAI']=HAI
# ================================================================ Rawalpindi: the dhaba
def gang(**kw):
    pindi(**kw); FILLE[0]=110; A={}
    A['sv']=pbike((.6,7.4,0),0,BKC[0],rider=SHANI,name='shani'); A['sh']=A['sv']['rider']; A['bv']=pbike((-3.4,5.4,0),14,BKC[1],rider=BILLA,name='billa'); A['bi']=A['bv']['rider']
    A['go']=mk(GOGA,4.0,8.4,-90,'goga'); A['mi']=mk(MITHU,4.9,10.4,-50,'mithu'); A['ka']=mk(KAKA,-3.6,10.3,35,'kaka'); A['ch']=mk(DHABA,-1.6,13.75,0,'chacha'); A['cu']=cup_of(A['sh'],1); A['mc']=cup_of(A['mi'],1)
    return A
def gang_idle(A,t):
    bike_roll(A['sv'],.6,7.4,0,0); bike_sit(A['sv'],t); bike_roll(A['bv'],-3.4,5.4,14,0); bike_sit(A['bv'],t)
    standp(A['go'],t,4.0,8.4,-90); crossed(A['go']); standp(A['mi'],t,4.9,10.4,-50); hold_chai(A['mi'],A['mc'],1,sip=.5+.5*math.sin(t*1.3)); standp(A['ka'],t,-3.6,10.3,35); standp(A['ch'],t,-1.6,13.75,0)
    for k in ('bi','go','mi','ka'): fc(A[k],'happy'); look_at(A[k],headw(A['sh']),.6,maxyaw=50)
    fc(A['ch'],'calm'); A['bi']['arm'][-1].rotation_euler=(R(-20),0,0)
def TWELVE():
    A=gang(); sh=A['sh']; ph=phone_of(sh,-1)
    def upd(t):
        gang_idle(A,t); k=ease((t-1.25)/.4); hold_chai(sh,A['cu'],1,sip=.9*(1-ease((t-.9)/.4))); phone_up(sh,-1,k,h=3.5,fw=1.2,sx=.4); sh['head'].rotation_euler[0]=R(14*k); fc(sh,'bored')
        ph.scale=(1,1,1) if (t<1.2 or int(t*14)%2==0) else (1.12,1.12,1.12)
        cam2(t,(12.8,4.6,5.0),(7.6,5.5,2.3),(.4,8.0,2.5),26,(.4,7.5,2.2))
    return dict(upd=upd)
SHOTS['TWELVE']=TWELVE
def shani_call(a,b,yaw=-24,dist=3.0,lens=38,sip=None,shades=None,dz=0.0):
    A=gang(); sh=A['sh']; ph=phone_of(sh,-1)
    def upd(t):
        gang_idle(A,t); hold_chai(sh,A['cu'],1,sip=(0 if sip is None else ease((t-we(b)-sip)/.3))); ear(sh,-1,1); fc(sh,'bored'); speak(sh,t,a,b,gesture=False)
        if shades is not None:
            k=ease((t-we(b)-shades)/.22); shk(sh,k); fc(sh,'smug') if k>.5 else None
            if k>0: A['cu'].scale=(1-k,)*3; sh['arm'][1].rotation_euler=(R(-72),0,R(7)); bike_idle(A['sv'],t,k)
        c1(t,sh,yaw=yaw,dist=dist,lens=lens,ref=90,dz=dz)
    return dict(upd=upd)
SHOTS['BURGER']=lambda: shani_call(123,125,dist=3.9,lens=36)
SHOTS['KINNA']=lambda: shani_call(132,134,yaw=-10,dist=3.3,lens=42,sip=.02)
SHOTS['BAS']=lambda: shani_call(137,139,yaw=-36,dist=4.2,lens=34,shades=.05,dz=-.6)
def nite(dy,**kw):
    isb('pd_night',1.0,arm=False,stars=True,**kw); D=dino((5.75,dy,0),0); FILLE[0]=120; lamp((5.75,dy-11,6.5),2200,(1,.84,.62)); lamp((1.0,dy-2,9),1400,(.55,.68,1.0)); return D
RN=(-11.0,-4.6,-100)
def DINOAA():
    D=nite(14); ra=mk(RAYYAN,*RN,'rayyan'); ph=phone_of(ra,1)
    def upd(t):
        d=1.5*t; D['root'].location[1]=3.5-d; dino_pose(D,t,dist=d,pitch=9,neck=28,head=-4,jaw=.3); dino_face(D,'angry')
        standp(ra,t,*RN); ear(ra,1,1); fc(ra,'worry'); speak(ra,t,126,131,gesture=False); ra['root'].location[2]=.012*math.sin(t*31)
        c1(t,ra,yaw=6,dist=3.1,lens=32,tz=-.1,sx=-.45)
    return dict(upd=upd)
SHOTS['DINOAA']=DINOAA
def CHAALIS():
    D=nite(14); D['root'].location=(6.5,-4.6,0); D['root'].rotation_euler[2]=R(-90); lamp((-1,-4.6,4.5),1800,(1,.84,.62)); ra=mk(RAYYAN,*RN,'rayyan'); ph=phone_of(ra,1)
    def upd(t):
        dino_pose(D,t,pitch=12,neck=32,head=-24,jaw=.3); dino_face(D,'curious'); dino_eyes(D,dz=-.6); standp(ra,t,*RN); ear(ra,1,1); fc(ra,'shock'); speak(ra,t,135,136,gesture=False)
        k=ease(t/.25)*(1-ease((t-.55)/.3)); ra['head'].rotation_euler[2]=R(-70*k)
        c1(t,ra,yaw=-10,dist=3.0,lens=26,dz=-.9,tz=.75,sx=-.45)
    return dict(upd=upd)
SHOTS['CHAALIS']=CHAALIS
# ================================================================ the road: two hundred bikes
SF=[(0,0),(-3.0,-5),(3.0,-5.5),(-5.8,-10.5),(.2,-11),(5.9,-11.5),(-3.1,-16.5),(3.0,-17),(-6.2,-22),(0,-22.5),(6.0,-23)]
def swarm(n=9,y0=0.0,far=130):
    hiway(); FILLE[0]=90; RD_=[SHANI,BILLA,GOGA,MITHU,KAKA,NOMI]+[prider(k) for k in range(6)]; r=random.Random(77); FB=[]
    V=[pbike((SF[k][0],y0+SF[k][1],0),90,BKC[k%8],rider=RD_[k],name='s%d'%k,light=(260 if k==0 else False)) for k in range(n)]
    for k in range(far):
        x=r.uniform(-7.2,7.2); y=y0-27-k*1.15-r.uniform(0,1); e=empty((x,y,0)); obox((0,0,1.25),(.3,.45,.75),M('#15161C',.8),.1,e); oico((0,.5,1.35),.11,M('#FFF2CC',.3,emit=14.0),e,sub=1); oico((0,-.55,.95),.07,M('#FF2A1A',.3,emit=8.0),e,sub=1); FB.append((e,x,y))
    shk(V[0]['rider'],1); return V,FB
def swarm_upd(V,FB,t,y0,v=9.0,wh=None):
    for k,vv in enumerate(V):
        w=0.0 if wh is None else wh(k,t); bike_roll(vv,SF[k][0]+.12*math.sin(t*1.7+k),y0+SF[k][1]+v*t,90,v*t,wheelie=w); bike_sit(vv,t,lean=-6); fc(vv['rider'],'smug' if k%2==0 else 'happy')
    for k,(e,x,y) in enumerate(FB): e.location=(x+.15*math.sin(t*2+k),y+v*t,0)
def ALONE():
    V,FB=swarm(9,22)
    def upd(t):
        swarm_upd(V,FB,t,22); cam2(t,(1.3,44,.8),(1.3,46,.85),(0,26,1.8),40,(0,33,1.8))
    return dict(upd=upd)
SHOTS['ALONE']=ALONE
def BIKES():
    V,FB=swarm(11,0,far=170)
    def upd(t):
        swarm_upd(V,FB,t,0); y=9*t; cam2(t,(0,y+30,19),(0,y+28,17.5),(0,y-42,0),30)
    return dict(upd=upd)
SHOTS['BIKES']=BIKES
def SILENCER():
    V,FB=swarm(9,0,far=40)
    for k in (2,5,1): bike_smoke(V[k],.05+.05*k,n=11,every=.15,seed=k)
    def upd(t):
        swarm_upd(V,FB,t,0,wh=lambda k,t: (26*abs(math.sin(t*3.2)) if k==0 else 0)); y=-5.5+9*t
        for k in (2,5,1): bike_idle(V[k],t,2.0)
        cam2(t,(8.3,y+3.6,1.0),(8.2,y+2.9,1.05),(3.0,y-.7,1.55),28)
    return dict(upd=upd)
SHOTS['SILENCER']=SILENCER
# ================================================================ Islamabad night: Pindi boys vs the dinosaur
BM=[(5.75,6.5),(3.7,5.2),(7.8,5.2),(2.4,2.2),(5.75,2.0),(9.0,2.4)]; RD6=[SHANI,BILLA,GOGA,MITHU,KAKA,NOMI]
def conf(dy=24.0,nb=6):
    D=nite(dy); V=[pbike((x,y,0),90,BKC[k],rider=RD6[k],name='b%d'%k,light=(300 if k==0 else False)) for k,(x,y) in enumerate(BM[:nb])]
    if V: shk(V[0]['rider'],1)
    return D,V
def conf_idle(V,t,shake=1.0,dy=0.0):
    for k,v in enumerate(V): bike_roll(v,BM[k][0],BM[k][1]+dy,90,dy); bike_sit(v,t); bike_idle(v,t,shake)
def ROARED():
    D,V=conf(24,0)
    def upd(t):
        rr=dino_roar(t,.1,1.55); dino_pose(D,t,pitch=14+7*rr,neck=30-8*rr,head=-2-10*rr,jaw=max(.2,rr),hz=-.4*rr); dino_face(D,'angry')
        cam2(t,(4.9,9.4,1.0),(5.0,10.0,1.05),(5.75,16.5,5.6),22)
    return dict(upd=upd)
SHOTS['ROARED']=ROARED
def LOOKED():
    D,V=conf(24,3); S,Bi,G=[v['rider'] for v in V]
    def upd(t):
        conf_idle(V,t); a=ease((t-.35)/.3); b=ease((t-1.05)/.3)
        S['head'].rotation_euler=(R(-12*(1-a)),0,R(-38*a+76*b)); fc(S,'flat' if b<.9 else 'smug')
        for H in (Bi,G): look_at(H,LV((5.75,16,7),tuple(headw(S)),a),1.0,maxyaw=70); fc(H,'flat')
        cam2(t,(5.75,13.4,1.75),(5.75,12.8,1.8),(5.75,5.8,2.05),24)
    return dict(upd=upd)
SHOTS['LOOKED']=LOOKED
def ROARBACK():
    D,V=conf(24,6)
    for k,v in enumerate(V): bike_smoke(v,.1+.07*k,n=9,every=.17,seed=k)
    def upd(t):
        conf_idle(V,t,2.5)
        for k,v in enumerate(V):
            if k in (1,2,5): bike_roll(v,BM[k][0],BM[k][1],90,0,wheelie=24*abs(math.sin(t*5.5+k)))
            H=v['rider']; fc(H,'shout'); H['head'].rotation_euler[0]=R(-16)
            if k%2==1: arms_up(H,1,t,spread=16,jig=12,only=1)
        cam2(t,(3.3,14.2,.9),(3.5,13.6,.95),(5.75,5.2,2.2),22)
    return dict(upd=upd)
SHOTS['ROARBACK']=ROARBACK
def FIRST():
    D,V=conf(24,0); sw=oico((0,0,-9),.16,M('#8FD8FF',.2,emit=.6,alpha=.85),D['head'],sc=(1,.7,1.5),sub=2)
    def upd(t):
        k=ease((t-.75)/.45); k2=ease((t-1.5)/.9); dino_pose(D,t,pitch=14-4*k2,neck=30+12*k2,head=-10+8*k2,jaw=.9*(1-k)+.1*k+.04*math.sin(t*26)*k2,roll=.5*math.sin(t*33)*k2)
        dino_face(D,'angry',mix=('scared',k)); dino_eyes(D,dz=-.5*k)
        q=max(0,t-1.7); sw.location=(1.34,-1.0,1.0-.55*q) if q>0 else (0,0,-9)
        h=dino_headw(D); cam2(t,(.6,13.4,5.0),(1.1,14.2,5.4),(h.x,h.y-.9,h.z),30)
    return dict(upd=upd)
SHOTS['FIRST']=FIRST
def SCARED():
    D,V=conf(24,6)
    def upd(t):
        dd=2.6*ease(t/DUR*1.05); D['root'].location[1]=24+dd; dino_pose(D,t,dist=-dd,pitch=20,neck=34,head=-14,jaw=.25+.05*math.sin(t*30),arms=1.0,tail=.5); dino_face(D,'scared'); dino_eyes(D,dz=-.5)
        conf_idle(V,t,2.0,dy=1.1*t)
        for v in V: fc(v['rider'],'smug')
        cam2(t,(4.6,-3.4,2.7),(4.7,-2.6,2.8),(5.75,19,5.0),35)
    return dict(upd=upd)
SHOTS['SCARED']=SCARED
def insp(dy=27.0,who='sbgm'):
    D=nite(dy); V=[pbike((x,y,0),90,BKC[k],name='b%d'%k) for k,(x,y) in enumerate(BM)]; A=dict(D=D,V=V)
    for key,C_ in (('sh',SHANI),('bi',BILLA),('go',GOGA),('mi',MITHU)):
        if key[0] in who: A[key]=mk(C_,0,0,0,key)
    if 'sh' in A: shk(A['sh'],1)
    return A
def park(A):
    for k,v in enumerate(A['V']): bike_roll(v,BM[k][0],BM[k][1],90,0)
def frozen(D,t,pitch=10,neck=30,head=-8,**kw):
    dino_pose(D,t,pitch=pitch,neck=neck,head=head,jaw=.12,roll=.4*math.sin(t*31),tail=.25,**kw); dino_face(D,'scared'); dino_eyes(D,dx=.9*math.sin(t*2.6),dz=-.4)
def INSPECT():
    A=insp(); D=A['D']; sh,bi,go,mi=A['sh'],A['bi'],A['go'],A['mi']
    def upd(t):
        park(A); frozen(D,t); walk_path(sh,[(2.3,17.0),(2.3,22.2)],t,-.4,DUR+.6,step=.5,arm=0); blink(sh,t); fc(sh,'smug')
        for s in (1,-1): sh['arm'][s].rotation_euler=(R(30),R(s*16),0)
        sh['head'].rotation_euler[2]=R(-35); sh['head'].rotation_euler[0]=R(-18)
        standp(bi,t,2.6,25.9,90); bi['head'].rotation_euler[0]=R(22); headtouch(bi,1,1,dx=.3,dy=-.75,dz=-.35); fc(bi,'flat')
        standp(go,t,9.2,21.4,-90); look_at(go,(5.75,23,4.2),1.0,maxpitch=40); crossed(go); fc(go,'wow')
        standp(mi,t,5.75,15.2,180); look_at(mi,dino_headw(D),1.0,maxpitch=45); fc(mi,'wow'); mi['arm'][1].rotation_euler=(R(-130),R(14),0)
        cam2(t,(-2.8,9.8,2.0),(-1.4,8.6,2.3),(5.0,20,4.0),22)
    return dict(upd=upd)
SHOTS['INSPECT']=INSPECT
def SILNAHI():
    A=insp(who='b'); D=A['D']; bi=A['bi']
    def upd(t):
        park(A); frozen(D,t,hyaw=0); standp(bi,t,2.9,32.0,-22); fc(bi,'happy'); speak(bi,t,184,191,gesture=False)
        k=ease((t-.1)/.3)*(1-ease((t-we(187)-.1)/.3)); pointw(bi,1,(5.75,31,4.6),k) if k>0 else None; bi['head'].rotation_euler[2]=R(55*k); bi['head'].rotation_euler[0]=R(-20*k)
        if t>we(187)+.1: what_pose(bi,ease((t-we(187)-.1)/.3),t,.5)
        c1(t,bi,yaw=-14,dist=3.6,lens=28,dz=-.8,tz=.55)
    return dict(upd=upd)
SHOTS['SILNAHI']=SILNAHI
def WHEELIE():
    A=insp(who='g'); D=A['D']; go=A['go']
    def upd(t):
        park(A); k=ease(t/.5); dino_pose(D,t,pitch=10+26*k,neck=30+8*k,head=-10,jaw=.2,arms=k,roll=.4*math.sin(t*31),tail=.25); dino_face(D,'scared'); dino_eyes(D,dx=-.6,dz=-.6)
        standp(go,t,2.6,14.6,-28); fc(go,'laugh'); speak(go,t,192,198,gesture=False); pointw(go,-1,(5.75,26,9.0),1.0); go['head'].rotation_euler[2]=R(-30*(1-ease((t-we(193))/.3)))
        c1(t,go,yaw=-4,dist=3.9,lens=26,dz=-1.0,tz=.6,sx=.5)
    return dict(upd=upd)
SHOTS['WHEELIE']=WHEELIE
def AVERAGE():
    A=insp(who='m'); D=A['D']; mi=A['mi']
    def upd(t):
        park(A); k=ease(t/.45); dino_pose(D,t,pitch=-2,neck=6,head=-34,hroll=12*k,jaw=.1,tail=.25,hz=-.8); dino_face(D,'curious'); dino_eyes(D,dz=-.6)
        standp(mi,t,5.75,15.2,180); look_at(mi,dino_headw(D),1.0,maxpitch=45); fc(mi,'calm'); speak(mi,t,199,202,gesture=False); mi['arm'][1].rotation_euler=(R(-95+8*math.sin(t*9)),R(12),0)
        cam2(t,(8.4,19.6,6.0),(8.2,19.3,5.9),(5.75,15.4,2.2),42)
    return dict(upd=upd)
SHOTS['AVERAGE']=AVERAGE
def CHAKKAR():
    A=insp(who='s'); D=A['D']; sh=A['sh']
    def upd(t):
        park(A); dino_pose(D,t,pitch=4,neck=14,head=-30,hyaw=-30,jaw=.1,tail=.25); dino_face(D,'curious'); dino_eyes(D,dx=-.8,dz=-.6)
        standp(sh,t,2.9,26.6,90); fc(sh,'smug'); speak(sh,t,203,207,gesture=False); sh['arm'][-1].rotation_euler=(R(-82+7*math.sin(t*11)),0,0); sh['head'].rotation_euler[0]=R(-24); sh['head'].rotation_euler[2]=R(-25)
        c1(t,sh,yaw=-62,dist=3.3,lens=34,ref=90,dz=-.2)
    return dict(upd=upd)
SHOTS['CHAKKAR']=CHAKKAR
def NOBODY():
    A=insp(); D=A['D']; sh,bi,go,mi=A['sh'],A['bi'],A['go'],A['mi']
    def upd(t):
        park(A); k=ease((t-.45)/1.2); dino_pose(D,t,pitch=8-16*k,neck=28-30*k,head=-6-6*k,jaw=.08,tail=.4,hz=-1.9*k); dino_face(D,'scared',mix=('bored',k)); dino_eyes(D,dz=-.4)
        standp(sh,t,3.5,17.2,150); standp(bi,t,8.1,16.6,-160); standp(go,t,1.5,20.4,110); standp(mi,t,6.3,14.4,180)
        for H in (sh,bi,go,mi): look_at(H,dino_headw(D),.9,maxpitch=40); fc(H,'happy')
        sh['arm'][1].rotation_euler=(R(-150*ease((t-1.3)/.3)),R(14),0); arms_up(bi,ease((t-1.5)/.3),t,spread=18,jig=8)
        cam2(t,(-2.6,11,2.0),(-1.7,11.5,2.1),(5.0,19,3.3),24)
    return dict(upd=upd)
SHOTS['NOBODY']=NOBODY
def SELFIE():
    A=insp(27.6,who='sbg'); D=A['D']; sh,bi,go=A['sh'],A['bi'],A['go']; ph=phone_of(sh,1); fl=lamp((5.8,12.6,3.0),0,(1,1,1))
    def upd(t):
        park(A); dino_pose(D,t,pitch=-12,neck=-6,head=-4,jaw=.3,tail=.4,hz=-1.9); dino_face(D,'happy'); dino_eyes(D,dz=-.2)
        standp(sh,t,5.4,14.8,0); standp(bi,t,4.0,16.3,0); standp(go,t,7.0,16.4,0)
        phone_up(sh,1,1,h=4.5,fw=1.7,sx=.9); fc(sh,'happy'); fc(bi,'laugh'); fc(go,'happy'); arms_up(bi,1,t,spread=20,only=-1); go['arm'][1].rotation_euler=(R(-160),R(18),0)
        fl.data.energy=60000 if 1.12<t<1.2 else 0
        cam2(t,(5.95,12.2,2.9),(5.9,12.35,2.9),(5.5,17,3.2),18)
    return dict(upd=upd)
SHOTS['SELFIE']=SELFIE
def SUNGLASS():
    A=insp(who=''); D=A['D']
    def upd(t):
        park(A)
        dino_pose(D,t,pitch=12,neck=30,head=-2,hyaw=-24,jaw=.14,tail=.6); dino_face(D,'smug'); dino_shades(D,pop(t-.12))
        h=dino_headw(D); cam2(t,(.6,11.6,7.0),(1.2,12.4,7.2),(h.x,h.y-.6,h.z+.1),44)
    return dict(upd=upd)
SHOTS['SUNGLASS']=SUNGLASS
def mount(D,H,y,legs=64):
    H['root'].parent=D['hip']; H['dy']=y
def mount_head(D,H):
    H['root'].parent=D['head']; H['dy']=None
def mounted(D,H,t):
    if H['dy'] is None:
        sit(H,1,0,legs=64); H['root'].location=(0,.35,.82); H['root'].rotation_euler=(0,0,0); blink(H,t); H['head'].rotation_euler=(0,0,0); return
    sit(H,1,0,legs=64); H['root'].location=(0,H['dy'],1.3); H['root'].rotation_euler=(0,0,0); blink(H,t); H['head'].rotation_euler=(0,0,0)
def convoy(rz,moon=True):
    hiway(moon=moon); FILLE[0]=60; D=dino((0,0,0),rz); dino_shades(D,1); sh=mk(SHANI,0,0,0,'shani'); bi=mk(BILLA,0,0,0,'billa'); mount(D,sh,-2.3); mount(D,bi,-.2); shk(sh,1)
    V=[pbike((0,0,0),90,BKC[k+2],rider=c,name='e%d'%k) for k,c in enumerate((GOGA,MITHU,KAKA,NOMI))]; return D,sh,bi,V
EO=[(4.6,9.0),(5.8,1.5),(-5.2,-7.5),(5.8,-9.0)]
def convoy_upd(D,sh,bi,V,t,y,d,sgn=1):
    D['root'].location=(0,y,0); dino_pose(D,t,dist=d,S=5.4,pitch=13,neck=26,head=2,jaw=.55,tail=.7); dino_face(D,'happy'); mounted(D,sh,t); mounted(D,bi,t); arms_up(sh,1,t,spread=22,jig=8); arms_up(bi,1,t,spread=20,jig=10,only=1); bi['arm'][-1].rotation_euler=(R(-60),0,0)
    fc(sh,'laugh'); fc(bi,'shout')
    for k,v in enumerate(V): bike_roll(v,EO[k][0],y+sgn*EO[k][1],90 if sgn>0 else -90,d,wheelie=(24*abs(math.sin(t*3+k)) if k%2==0 else 0)); bike_sit(v,t,lean=-6); fc(v['rider'],'happy')
def ROUND():
    D,sh,bi,V=convoy(180)
    def upd(t):
        d=8.5*t; y=20+d; convoy_upd(D,sh,bi,V,t,y,d); camset((-7.9,y+15.5-1.5*ease(t/DUR),6.0),(-.2,y+1.0,5.6),24,8)
    return dict(upd=upd)
SHOTS['ROUND']=ROUND
def THREEH():
    D,sh,bi,V=convoy(0,moon=False); mo=oico((0,420,150),17,M('#FFF6D8',.3,emit=3.5),None,sub=3)
    def upd(t):
        d=8.5*t; y=98-d; convoy_upd(D,sh,bi,V,t,y,d,sgn=-1); q=t/DUR; mo.location=(-95+190*q,420,120+62*math.sin(pi*q))
        cam2(t,(.4,32.5,1.4),(.4,33.4,1.45),(0,70,8.0),50)
    return dict(upd=upd)
SHOTS['THREEH']=THREEH
# ================================================================ Pindi keeps him
def nameplate(D):
    e=empty((0,-4.66,.3),D['hip']); obox((0,0,0),(1.2,.05,.5),M('#F2C14E',.4),.04,e); obox((0,-.02,0),(1.1,.05,.4),M('#FFF8E6',.4),.02,e); text('SHERU',(0,-.08,0),(0,-1,0),.56,M('#16171C',.5),ex=.01,parent=e)
    for s in (-1,1): obox((s*1.0,.1,.9),(.03,.03,.5),M('#C9CED8',.3,metal=.8),0,e)
    D['plate']=e; return e
def pdino(x=9.0,plate=True,**kw):
    pindi(**kw); FILLE[0]=90; D=dino((x,5.8,0),-90); dino_shades(D,1); lamp((x-9,8.6,8.5),1000,(1,.84,.62)); lamp((x-3,3.6,9.5),600,(.55,.68,1.0))
    if plate: nameplate(D)
    return D
def ppose(D,t,pitch=8,neck=28,**kw):
    dino_pose(D,t,pitch=pitch,neck=neck,**kw)
    if 'plate' in D: D['plate'].rotation_euler[0]=R(pitch)
def NEVER():
    D=pdino(9,plate=False); V=[pbike((0,0,0),180,BKC[0],rider=SHANI,name='shani'),pbike((0,0,0),180,BKC[1],rider=BILLA,name='billa')]; shk(V[0]['rider'],1)
    G=[mk(ISBP[3],-6.4,10.3,60,'g0'),mk(DHABA,1.6,10.4,90,'chacha'),mk(KAKA,-9.6,10.2,70,'kaka')]
    def upd(t):
        d=2.4*t; x=9.5-d; D['root'].location[0]=x; ppose(D,t,dist=d,pitch=9,neck=28,head=-4,jaw=.25,tail=.6); dino_face(D,'happy')
        bike_roll(V[0],x-10.0,5.4,180,d); bike_roll(V[1],x-7.4,7.6,180,d)
        for v in V: bike_sit(v,t); fc(v['rider'],'smug')
        for k,H in enumerate(G): standp(H,t,(-6.4,1.6,-9.6)[k],(10.3,10.4,10.2)[k],(60,90,70)[k]); look_at(H,dino_headw(D),1.0,maxpitch=40,maxyaw=80); fc(H,'wow')
        cam2(t,(-13.2,8.3,1.5),(-12.4,8.2,1.6),(0,5.8,5.6),28)
    return dict(upd=upd)
SHOTS['NEVER']=NEVER
def fprint(x,y,rz=0):
    dk=M('#1C1D21',.95); c=math.cos(R(rz)); s=math.sin(R(rz))
    def P(dx,dy,hx,hy): B.box((x+dx*c-dy*s,y+dx*s+dy*c,.048),(hx,hy,.008),dk,.0,rot=(0,0,R(rz)))
    P(0,.3,.8,1.0)
    for dx in (-.55,0,.55): P(dx,-1.25,.2,.5)
def NEXTFRI():
    isb('pd_gold',0.0); fprint(-6.6,-3.4,8); fprint(-4.6,3.2,-6); fprint(-6.9,9.6,5)
    for k,(x,y) in enumerate(((-8.3,-4.6),(-5.2,-5.4),(-8.2,-1.6))): B.cyl((x,y,.38),.2,.76,M('#FF8A1E',.5),seg=8,r2=.07)
    B.done('fp'); FILLE[0]=60; ra=mk(RAYYAN,RP[0],RP[1],70,'rayyan'); cu=cup(ra,1)
    def upd(t):
        standp(ra,t,RP[0],RP[1],70); fc(ra,'bored'); k=ease((t-.5)/.5)*(1-ease((t-1.7)/.5)); hold_chai(ra,cu,1,a=-64,sip=.9*k); ra['head'].rotation_euler[2]=R(-30*ease((t-2.0)/.5))
        cam2(t,(-3.4,-7.6,1.55),(-4.8,-6.6,1.65),(-11.2,-1.5,2.2),40)
    return dict(upd=upd)
SHOTS['NEXTFRI']=NEXTFRI
PW=[(-3.0,7.6,200),(1.0,4.4,170),(-6.5,4.6,150)]
def PINDINOT():
    D=pdino(10); V=[pbike((x,y,0),rz,BKC[k],rider=RD6[k],name='b%d'%k) for k,(x,y,rz) in enumerate(PW)]; shk(V[0]['rider'],1)
    for k,v in enumerate(V): bike_smoke(v,.02+.06*k,n=8,every=.15,seed=k)
    def upd(t):
        rr=dino_roar(t,.0,1.2); ppose(D,t,pitch=16+6*rr,neck=30,head=6+8*rr,jaw=max(.3,rr),tail=1.0,arms=.6); dino_face(D,'happy')
        for k,v in enumerate(V): x,y,rz=PW[k]; bike_roll(v,x,y,rz,0,wheelie=26*abs(math.sin(t*5+k*1.3))); bike_sit(v,t); fc(v['rider'],'shout'); arms_up(v['rider'],1,t,spread=16,jig=12,only=1)
        cam2(t,(-12.5,5.6,1.1),(-11.9,5.6,1.15),(1.5,5.8,5.6),20)
    return dict(upd=upd)
SHOTS['PINDINOT']=PINDINOT
def NAMED():
    D=pdino(10)
    def upd(t):
        ppose(D,t,pitch=8,neck=28,head=-16,jaw=.12,tail=.6); dino_face(D,'smug'); p=D['plate'].matrix_world.translation
        cam2(t,(-8.2,5.0,5.0),(-7.0,5.1,5.2),(p.x,p.y,p.z+.75),40,(p.x,p.y,p.z+.55))
    return dict(upd=upd)
SHOTS['NAMED']=NAMED
def SHERU():
    D=pdino(7.3); ch=mk(DHABA,-3.0,9.8,-38,'chacha'); u=ch['u']; gc=empty((0,-.45*u,6.6*u),ch['root']); st=M('#C9CED8',.22,metal=.9)
    ocyl((0,0,0),.5,.62,st,gc,rot=(0,0,0),seg=16,r2=.6); ocyl((0,0,.3),.56,.03,M('#B5713A',.5),gc,rot=(0,0,0),seg=16); obox((.7,0,.05),(.14,.05,.2),st,.03,gc); steam((-3.0,9.5,3.6),0,3,n=8,seed=4,size=.12)
    def upd(t):
        k=ease((t-.9)/1.0); ppose(D,t,pitch=6-12*k,neck=24-36*k,head=-10-22*k,hyaw=-44*k,jaw=.15+.3*k,tail=.8,hz=-1.6*k); dino_face(D,'happy'); dino_eyes(D,dx=-.5,dz=-.5)
        standp(ch,t,-3.0,9.8,-38); arms_up(ch,.9,t,spread=8); fc(ch,'shout' if t<we(257)+.25 else 'happy'); speak(ch,t,257,264,gesture=False); ch['head'].rotation_euler[0]=R(-20); ch['head'].rotation_euler[2]=R(-30)
        cam2(t,(-7.6,6.0,1.5),(-7.0,6.5,1.6),(-2.6,9.2,3.6),26)
    return dict(upd=upd)
SHOTS['SHERU']=SHERU
RAY2=dict(RAYYAN,shades='up',shade_c='#0E0F14',scarf='#C8372D')
def MAMUQ():
    pindi(); FILLE[0]=110; ra=mk(RAY2,1.2,10.2,-25,'rayyan'); cu=cup_of(ra,1); ph=phone_of(ra,-1); mi=mk(MITHU,4.9,12.6,-60,'mithu'); ka=mk(KAKA,-2.4,12.3,40,'kaka')
    def upd(t):
        standp(ra,t,1.2,10.2,-25); k=ease((t-1.25)/.4); hold_chai(ra,cu,1,sip=.9*(1-ease((t-.9)/.35))); phone_up(ra,-1,k,h=3.7,fw=1.2,sx=.4); ra['head'].rotation_euler[0]=R(16*k); fc(ra,'happy' if k<.5 else 'wow')
        ph.scale=(1,1,1) if (t<1.2 or int(t*14)%2==0) else (1.12,1.12,1.12)
        standp(mi,t,4.9,12.6,-60); standp(ka,t,-2.4,12.3,40); fc(mi,'laugh'); fc(ka,'happy'); look_at(mi,headw(ka),.6); look_at(ka,headw(mi),.6)
        c1(t,ra,yaw=8,dist=3.4,lens=36,tz=-.35)
    return dict(upd=upd)
SHOTS['MAMUQ']=MAMUQ
def MAMU_():
    office(False); FILLE[0]=30; m=mk(MAMU,0,2.35,0,'mamu'); m['home']=(0,2.35,0); ph=phone_of(m,1); cu=cup_of(m,-1)
    def upd(t):
        sitp(m,t,seat=.68); ear(m,1,1); fc(m,'calm'); speak(m,t,272,278,gesture=False); hold_chai(m,cu,-1,sip=.95*ease((t-we(278)-.05)/.3))
        cam2(t,(.6,-3.8,2.05),(.45,-3.0,2.0),(0,2.3,1.85),36)
    return dict(upd=upd)
SHOTS['MAMU']=MAMU_
def MONSTER():
    isb('pd_dusk',.45,arm=False); D=dino((4.8,22,0),-18); FILLE[0]=60; P=[mk(RAYYAN,8.2,11.2,160,'rayyan'),mk(ISBP[0],6.2,9.4,170,'ia')]
    def upd(t):
        rr=dino_roar(t,.15,1.8); dino_pose(D,t,pitch=14+7*rr,neck=30,head=4+10*rr,jaw=max(.25,rr)); dino_face(D,'angry')
        for k,H in enumerate(P): standp(H,t,(8.2,6.2)[k],(11.2,9.4)[k],(160,170)[k]); hands_head(H,1); H['root'].location[2]=.015*math.sin(t*30+k); fc(H,'scream')
        cam2(t,(10.4,4.6,1.0),(10.1,5.2,1.05),(5.6,15.5,5.6),22)
    return dict(upd=upd)
SHOTS['MONSTER']=MONSTER
def RIDE():
    D=pdino(8); sh=mk(SHANI,0,0,0,'shani'); mount_head(D,sh); shk(sh,1); V=[pbike((0,0,0),180,BKC[k+1],rider=RD6[k+1],name='b%d'%k) for k in range(2)]
    def upd(t):
        d=5.0*t; x=8-d; D['root'].location[0]=x; ppose(D,t,dist=d,pitch=30,neck=34,head=4,jaw=.7,tail=.7,arms=1.0); dino_face(D,'happy'); mounted(D,sh,t); arms_up(sh,1,t,spread=22,jig=8); fc(sh,'laugh')
        bike_roll(V[0],x-9.5,8.0,180,d,wheelie=30); bike_roll(V[1],x-6.5,3.9,180,d,wheelie=26+4*math.sin(t*6))
        for v in V: bike_sit(v,t); fc(v['rider'],'shout')
        cam2(t,(-11.2,8.4,1.0),(-12.2,8.4,1.05),(x-6,5.8,6.4),22,(x-6.5,5.8,7.0))
    return dict(upd=upd)
SHOTS['RIDE']=RIDE
def CTA():
    D=pdino(11.5); wa=mk(WALEED,-.6,5.8,-90,'waleed'); ra=mk(RAY2,.9,7.3,-90,'rayyan'); cu=cup(ra,1); V=pbike((1.2,4.2,0),180,BKC[0],rider=SHANI,name='shani'); shk(V['rider'],1)
    def upd(t):
        ppose(D,t,pitch=-2,neck=6,head=-16,jaw=.14,tail=.8,hz=-.9); dino_face(D,'happy'); dino_eyes(D,dz=-.4)
        standp(wa,t,-.6,5.8,-90); fc(wa,'happy'); speak(wa,t,287,293,gesture=False); k=ease((t-ws(291))/.3); wa['arm'][1].rotation_euler=(R(-88*k),R(-6*k),0)
        a=ease((t-ws(288))/.25)*(1-ease((t-ws(289)-.1)/.25)); b=ease((t-ws(290))/.25)*(1-ease((t-we(290)-.25)/.25)); wa['arm'][-1].rotation_euler=(R(-40*a),R(50*a),0) if a>0 else (0,0,0)
        if b>0 and k<=0: wa['arm'][1].rotation_euler=(R(-30*b),R(-42*b),0)
        standp(ra,t,.9,7.3,-90); hold(ra,1,-64); fc(ra,'calm'); bike_roll(V,1.2,4.2,180,0); bike_sit(V,t); fc(V['rider'],'smug'); crossed(V['rider'])
        cam2(t,(-6.9,5.8,1.9),(-6.3,5.8,1.95),(0,5.8,2.9),26)
    return dict(upd=upd)
SHOTS['CTA']=CTA
def LOOK():
    isb('pd_gold',0.0); D=dino((5.6,30,0),0); FILLE[0]=60; W=mk(WALEED,2.6,24.5,180,'waleed'); V=pbike((8.6,22.5,0),90,BKC[0],rider=SHANI,name='shani',pillion=BILLA)
    def upd(t):
        k=int(t/DUR*4.999); dino_pose(D,t,dist=(None,3.0,None,None,None)[k],pitch=(8,8,8,40,8)[k],neck=(28,28,28,40,28)[k],head=(0,0,-10,10,-30)[k],jaw=(0,.3,1,.2,0)[k],hyaw=(0,0,0,0,30)[k]); dino_face(D,('calm','angry','angry','scared','happy')[k]); dino_shades(D,1 if k==4 else 0)
        standp(W,t,2.6,24.5,180); bike_roll(V,8.6,22.5,90,0,wheelie=(0,0,0,35,0)[k]); bike_sit(V,t)
        C=[((-8.5,27,4.5),(5.6,27,4.6),20),((16,12,3),(5.6,25,5),28),((5.6,9,2.0),(5.6,24,6.5),30),((-8,13,3),(5.6,27,6),22),((-1,13,4.5),(5.6,23.5,7.2),34)][k]
        camset(C[0],C[1],C[2],8)
    return dict(upd=upd)
if os.environ.get('LOOK'): SHOTS['HOOK']=LOOK
