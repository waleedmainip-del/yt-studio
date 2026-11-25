# Shots part 3: rooftop stake-out, the city that never sleeps, zombies settle in, finale.
MIX=[]
for _i in range(max(len(CROWD),len(ZVAR)*2)):
    MIX.append(CROWD[_i%len(CROWD)])
    if _i%2==0: MIX.append(dict(ZVAR[(_i//2)%len(ZVAR)],scruffy=False))
RZ_POS=[(ZKING,1.2),(ZVAR[0],-1.7),(ZVAR[8],4.4),(ZVAR[2],-4.4)]; RZY=-BW-.62
def roof_z():
    return [mk(C,x,RZY,180,'rz%d'%i,z=ROOF_Z+.02) for i,(C,x) in enumerate(RZ_POS)]
def staff_prop(x,y,z,lean=10,h=3.5):
    e=empty((x,y,z),rot=(R(lean),0,0)); wd=M('#3A2A22',.6,kind='wood',sc=.6); gd=M('#E6B93A',.25,metal=.9)
    ocyl((0,0,h/2),.05,h,wd,e,rot=(0,0,0),seg=8); ocyl((0,0,h-.1),.12,.12,gd,e,rot=(0,0,0),seg=8); oico((0,0,h+.16),.2,M('#7CFF8A',.2,emit=6),e,sub=2); return e
def roof_watch(Z,t,sleepy=0.0):
    for i,H in enumerate(Z):
        stand(H,t); blink(H,t)
        if i==0: H['arm'][1].rotation_euler=(R(-12),0,0); H['arm'][-1].rotation_euler=(R(-12),0,0)
        else: zpose(H,t,1-sleepy*.85,base=-80)
        H['head'].rotation_euler=(R(16+12*sleepy+5*sleepy*math.sin(t*2.2+i*1.3)),0,R(6*sleepy*math.sin(t*1.1+i)))
        zeyes(H,1-.4*sleepy); face(H,mouth='flat' if sleepy<.5 else ('O' if (i+int(t*1.5))%4==0 else 'flat'),brow=-.02+.05*sleepy,brow_r=-10+16*sleepy)
def droopy(H,k=.5):
    u=H['u']
    for o in H['lids']: o.scale=(1,1,k); o.location[2]=(.66+.16*(1-k))*u
def night_street(clock,seed=1,walk=True,tabs=8,skip=(),pool=None,nost=(),mood='night',rsign='CHACHA MAGHAZ HOUSE',wx=(-30,26)):
    S=burns(mood,clock=clock,nost=nost,rest_sign=rsign); TB=street_tables(tabs,skip=skip); rooftop()
    D=diners(seed,TB,pool=pool); Wk=kwalkers(seed+3,((WLANE,1),(-WLANE,-1)),4,wx[0],wx[1],pool=pool) if walk else []
    def bg(t):
        upd_diners(D,t); upd_kwalkers(Wk,t); spin_fans(t)
    return dict(S=S,TB=TB,D=D,Wk=Wk,bg=bg)
# ---------------------------------------------------------------- PLAN
def PLAN():
    Q=night_street((0,50),seed=2,walk=False); Z=roof_z(); kg=Z[0]; FILLE[0]=60; staff_prop(2.75,RZY+.28,ROOF_Z+.3,lean=-7)
    point((1,RZY+3.5,ROOF_Z+1.0),900,(1,.8,.5),r=2,shadow=False); point((0,RZY-4,ROOF_Z+4),700,(.6,.75,1.0),r=2,shadow=False)
    def upd(t):
        Q['bg'](t); roof_watch(Z,t,0.0)
        k=tl(t,ws(203)-.1,ws(203)+.2); kg['arm'][-1].rotation_euler=(R(-78*k),R(18*k),0); kg['head'].rotation_euler=(R(12),0,R(20*math.sin(t*2.6)*k)); face(kg,mouth='smirk' if k>.5 else 'flat',brow=-.03,brow_r=-12)
        for i in (1,2,3):
            look_at(Z[i],hp(kg),.7*k,maxyaw=70); Z[i]['head'].rotation_euler[0]=R(8+8*math.sin(t*7+i)*tl(t,ws(206),ws(206)+.2))
        q=ease(t/DUR); camset(LV((-.6,RZY+10.5,ROOF_Z+1.2),(-.2,RZY+8.6,ROOF_Z+1.6),q),(.2,RZY,ROOF_Z+2.0),L(25,28,q),8)
    return dict(upd=upd)
SHOTS['PLAN']=PLAN
# ---------------------------------------------------------------- 1 AM / 2 AM / 3 AM vignettes (seen from the street, zombies peeking from the roof)
VL=[]
def vcam(t,x=0.0,lens=20,tz=3.05,y=5.6,z=1.5):
    if not VL: VL.append(point((x-1.5,4.6,3.4),1700,(1,.86,.66),r=1.5,shadow=False)); VL.append(point((x+2.5,3.8,2.2),700,(1,.9,.75),r=1.5,shadow=False))
    q=ease(t/DUR); camset((x+.25*q,y,z),(x,1.2,tz+.1*q),lens,8)
def stream(p0,p1,o):
    d=Vector(p1)-Vector(p0); o.location=tuple((Vector(p0)+Vector(p1))/2); o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); o.scale=(1,1,d.length)
def kettle(H,s=1):
    def b(e): ocyl((0,-.1,.1),.15,.24,M('#C9CED8',.25,metal=.9),e,rot=(0,0,0),seg=16,r2=.1); ocyl((0,-.1,.24),.07,.05,M('#2A2C34',.4),e,rot=(0,0,0),seg=10); obox((0,-.3,.12),(.025,.1,.025),M('#C9CED8',.25,metal=.9),.008,e,rot=(R(-32),0,0))
    return in_hand(H,s,b)
def ONEAM():
    Q=night_street((1,0),seed=3,skip=(0,1),walk=False); Z=roof_z(); FILLE[0]=30
    ce=chai_counter(0,1.7,180)
    cw=mk(CHAIWALA,0,.8,180,'chaiwala'); kt=kettle(cw,1); cu=[mk(CROWD[4],-2.0,2.0,128,'c1'),mk(CROWD[15],2.0,2.0,-128,'c2'),mk(CROWD[10],-4.2,.4,140,'c3')]; cups=[chai(cu[0],-1),chai(cu[1],1),chai(cu[2],1)]
    st=ocyl((0,0,0),.012,1.0,M('#B5713A',.4,emit=.3),rot=(0,0,0),seg=6); cc=chai(cw,-1)
    def upd(t):
        Q['bg'](t); roof_watch(Z,t,.0)
        hstand(cw,t); k=.5+.5*math.sin(t*3.2); cw['arm'][1].rotation_euler=(R(-150-12*k),0,R(10)); upright(kt,cw,1,tilt=-55); hold_chai(cw,cc,-1,a=-58); face(cw,mouth='grin')
        for i,H in enumerate(cu):
            hstand(H,t); hold_chai(H,cups[i],(-1,1,1)[i],a=-70,sip=(.5+.5*math.sin(t*3+i*2)) if i==2 else 0); face(H,mouth='grin' if i!=1 else 'smile')
        kp=kt.matrix_world@Vector((0,-.42,.2)); cp=ce.matrix_world@Vector((.35,.08,1.16)); stream(kp,cp,st)
        vcam(t)
    return dict(upd=upd)
SHOTS['ONEAM']=ONEAM
def bat(H,s=1):
    def b(e): obox((0,-.05,-.74),(.085,.03,.42),M('#D9B982',.6,kind='wood',sc=.5),.02,e); ocyl((0,-.05,-.17),.035,.32,M('#2A2C34',.5),e,rot=(0,0,0),seg=8)
    return in_hand(H,s,b)
def stumps(x,y,rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz))); S_=[ocyl((0,(k-1)*.16,.6),.03,1.2,M('#F2E2B0',.6),e,rot=(0,0,0),seg=8) for k in range(3)]; S_+=[obox((0,dy,1.22),(.02,.075,.02),M('#F2E2B0',.6),.005,e) for dy in (-.08,.08)]; return e,S_
def TWOAM():
    Q=night_street((2,0),seed=4,skip=(0,1),walk=False); Z=roof_z(); FILLE[0]=30
    bt=mk(FRIENDS[2],-.5,1.4,150,'batsman'); b_=bat(bt,1); stumps(1.15,.7,60)
    kids=[mk(CROWD[5],-2.6,2.3,150,'k1'),mk(CROWD[13],2.9,2.2,-150,'k2'),mk(FRIENDS[0],-4.4,.2,130,'k3')]
    ball=oico((0,0,-9),.11,M('#E8F23A',.4,emit=1.5),sub=2); TH=.72
    def upd(t):
        Q['bg'](t); roof_watch(Z,t,.3)
        hstand(bt,t); k=tl(t,TH-.18,TH+.06); bt['arm'][1].rotation_euler=(R(L(-35,-150,k)),R(L(-30,25,k)),0); bt['arm'][-1].rotation_euler=(R(L(-30,-120,k)),R(L(20,-20,k)),0); bt['root'].rotation_euler[2]=R(150+L(-20,30,k)); face(bt,mouth='strain' if k<1 else 'grin')
        if t<TH: ball.location=(L(-2.6,-.9,t/TH),L(7.5,2.0,t/TH),L(1.9,1.35,t/TH))
        else:
            d=t-TH; ball.location=(-.9-2.6*d*3.2,2.0-.4*d*3.2,1.35+12*d-4.9*d*d)
        for i,H in enumerate(kids):
            hstand(H,t); j=tl(t,TH+.05,TH+.3); look_at(H,ball.location,.8,maxpitch=50)
            if j>0: H['root'].location[2]=H['z0']+.008+.3*abs(math.sin((t-TH)*8))*(1 if i!=2 else .5); shock(H,j)
            face(H,mouth='grin' if j>.5 else 'smile')
        vcam(t,lens=20)
    return dict(upd=upd)
SHOTS['TWOAM']=TWOAM
def THREEAM2():
    Q=night_street((3,0),seed=5,skip=(0,1),walk=False); Z=roof_z(); FILLE[0]=30
    deg(-.9,1.6,1.0,lid=False); deg(1.1,1.55,1.0,lid=True); B.done('dg')
    ck=mk(dict(COOK,ladle=True),0.1,.35,180,'cook2'); steam((-.9,1.6,1.5),0,9,n=10,seed=4,size=.09)
    cu=[mk(CROWD[7],-2.2,2.3,128,'n1'),mk(CROWD[12],2.3,2.3,-128,'n2'),mk(CROWD[2],-4.4,.4,140,'n3')]
    P=[]
    for i,H in enumerate(cu):
        e=in_hand(H,1,lambda e_: (ocyl((0,-.2,.05),.2,.03,M('#F6F4EE',.4),e_,rot=(0,0,0),seg=16),ocyl((0,-.2,.07),.15,.02,M('#8A3A1A',.5),e_,rot=(0,0,0),seg=14))); P.append(e)
    def upd(t):
        Q['bg'](t); roof_watch(Z,t,.6)
        hstand(ck,t); c=math.sin(t*4.5); ck['arm'][-1].rotation_euler=(R(-70-22*c),R(18),0); ck['arm'][1].rotation_euler=(R(-40),0,0); ck['head'].rotation_euler[0]=R(12); face(ck,mouth='smile')
        for i,H in enumerate(cu):
            hstand(H,t); H['arm'][1].rotation_euler=(R(-78),0,R(8)); upright(P[i],H,1); H['arm'][-1].rotation_euler=(R(-8),0,0); look_at(H,(0,1.6,1.5),.6,maxpitch=20); face(H,mouth='grin' if i==0 else 'smile')
        vcam(t)
    return dict(upd=upd)
SHOTS['THREEAM2']=THREEAM2
# ---------------------------------------------------------------- 4 AM: a wedding
def dhol(H):
    u=H['u']; e=empty((0,-.95*u,2.55*u),H['root']); ocyl((0,0,0),.36,.78,M('#C8372D',.5),e,rot=(0,R(90),0),seg=18)
    for sx in (-1,1): ocyl((sx*.4,0,0),.37,.03,M('#F2E2B0',.6),e,rot=(0,R(90),0),seg=18); ocyl((sx*.3,0,0),.375,.05,M('#F2C14E',.5),e,rot=(0,R(90),0),seg=18)
    obox((0,.3,.42),(.5,.02,.05),M('#F2C14E',.7,kind='fabric'),.01,e,rot=(R(40),0,0)); return e
def firework(c,t0,col,n=26,seed=1,rad=4.5):
    r=random.Random(seed); m=M(col,.3,emit=12); P=[]
    for i in range(n):
        v=Vector((r.uniform(-1,1),r.uniform(-.4,.4),r.uniform(-1,1))).normalized()*r.uniform(.6,1.0); P.append((oico((0,0,-90),.1,m,sub=1),v))
    def upd(t):
        d=t-t0
        for o,v in P:
            if d<0 or d>1.3: o.location=(0,0,-90); continue
            q=1-math.exp(-d*3.2); o.location=(c[0]+v.x*rad*q,c[1]+v.y*rad*q,c[2]+v.z*rad*q-1.2*d*d); k=max(0,1-d/1.3); o.scale=(k,k,k)
    return upd
def FOURAM():
    Q=night_street((4,0),seed=6,walk=False,tabs=8,skip=(0,1,2,5,6)); Z=roof_z(); FILLE[0]=45; TC=ws(220)+.25
    dh=[mk(DHOLI,0,0,-90,'dh1'),mk(DHOLI2,0,0,-90,'dh2')]; [dhol(H) for H in dh]
    gr=mk(GROOM,0,0,-90,'groom'); dn=[mk(C,0,0,-90,'bd%d'%i) for i,C in enumerate((CROWD[8],CROWD[17],FRIENDS[3],CROWD[23],CROWD[11],AUNTY))]
    off=[(-1.6,1.2),(-1.2,-1.4)]; doff=[(-6.2,2.6),(-6.6,-2.5),(-8.8,1.3),(-9.2,-1.3),(-11.4,2.5),(-11.6,-2.4)]
    FW=[firework((-4,-9,24),.25,'#FF5A8A',seed=1),firework((6,10,27),.75,'#FFD23F',seed=2),firework((-12,8,22),1.15,'#5AD2FF',seed=3),firework((2,-11,26),1.5,'#9AFF7A',seed=4)]
    point((0,0,6),2200,(1,.8,.6),r=2,shadow=False)
    def upd(t):
        Q['bg'](t); s=1.1*t; X=-2.0+s
        for i,H in enumerate(dh):
            H['root'].location[0]=X+off[i][0]+4.2; H['root'].location[1]=off[i][1]; H['root'].rotation_euler[2]=R(90); walk(H,s,step=.45,arm=0); blink(H,t)
            b=math.sin(t*14+i*1.5); H['arm'][1].rotation_euler=(R(-58-22*max(0,b)),R(-12),0); H['arm'][-1].rotation_euler=(R(-58-22*max(0,-b)),R(12),0); H['root'].rotation_euler[1]=R(5*b); face(H,mouth='grin')
        gr['root'].location[0]=X-.6; gr['root'].location[1]=0; gr['root'].rotation_euler[2]=R(90); walk(gr,s,step=.45,arm=10); blink(gr,t); face(gr,mouth='smile',brow=.03)
        for i,H in enumerate(dn):
            H['root'].location[0]=X+doff[i][0]+4.2; H['root'].location[1]=doff[i][1]; H['root'].rotation_euler[2]=R(90+18*math.sin(t*5+i)); walk(H,s,step=.45,arm=0); blink(H,t)
            a=math.sin(t*9+i*1.3); H['arm'][1].rotation_euler=(R(-150+18*a),R(-14),0); H['arm'][-1].rotation_euler=(R(-150-18*a),R(14),0); H['root'].location[2]+=.1*abs(a); face(H,mouth='grin')
        for f in FW: f(t)
        if t<TC:
            roof_watch(Z,t,.85); q=ease(t/TC); camset(LV((9.5,.4,1.25),(9.0,.5,1.35),q),LV((1.5,0,3.6),(2.3,0,3.5),q),L(20,21,q),8)
        else:
            FILLE[0]=150; roof_watch(Z,t,.9); kg=Z[0]; k=tl(t,TC+.05,TC+.3); headtouch(kg,1,k,dx=.2,dy=-.7,dz=.75); kg['head'].rotation_euler=(R(26*k),0,0); face(kg,mouth='frown',brow=-.03,brow_r=6); zeyes(kg,.7)
            q=ease((t-TC)/(DUR-TC)); camset(LV((2.4,RZY+3.6,ROOF_Z+2.5),(2.2,RZY+3.2,ROOF_Z+2.55),q),(1.3,RZY,ROOF_Z+2.6),L(34,36,q),4.0)
    return dict(upd=upd)
SHOTS['FOURAM']=FOURAM
# ---------------------------------------------------------------- SUNRISE / ENOUGH / LEAVING on the roof
SLP=[(ZVAR[0],-4.6,-9.0,-90),(ZVAR[8],2.2,-9.5,-90),(ZVAR[2],-1.8,-12.0,-90),(ZVAR[5],5.9,-7.25,90)]
KSIT=(1.2,-BW-.66)
def lie(H,x,y,rz,t,ph=0.0):
    C=H['C']; d=.21*C.get('h',1.0)*(1+(C.get('wide',1.0)-1)*.45)
    for q in (1,-1): H['leg'][q].rotation_euler=(R(-4*q),0,0); H['leg'][q].location[2]=2.0*H['u']
    H['root'].location=(x,y,ROOF_Z+.05+d+.012*math.sin(t*1.6+ph)); H['root'].rotation_euler=(R(-90),0,R(rz))
    H['arm'][1].rotation_euler=(0,R(-34),0); H['arm'][-1].rotation_euler=(0,R(22),0); H['head'].rotation_euler=(0,0,R(28*math.sin(ph*3)))
    blink(H,t,force=1); zeyes(H,0); face(H,mouth='O' if math.sin(t*1.6+ph)>0 else 'o')
def zzz(fn,ph=0.0,n=3,size=.34):
    m=M('#F6F4EE',.4,emit=2.2); Zs=[]
    for i in range(n):
        o=text('Z',(0,0,-90),(0,-1,0),size*(.7+.3*i),m,ex=.01); Zs.append(o)
    def upd(t):
        for i,o in enumerate(Zs):
            q=((t*.55+ph+i/n)%1.0); p=Vector(fn()); o.location=(p.x+.25*q+.12*math.sin(q*9),p.y,p.z+.3+1.5*q); k=min(1,q*4)*(1-q); o.scale=(k,k,k); cam=CAM.location; d=cam-o.location; o.rotation_euler=(R(90),0,math.atan2(-d.x,d.y)+pi)
    return upd
def roof_morning(mood='khi_dawn',clock=(5,50),asleep=True):
    S=burns(mood,clock=clock,night=.25); TB=street_tables(8,skip=(2,5)); rooftop()
    D=diners(9,TB); Wk=kwalkers(11,((WLANE,1),(-WLANE,-1)),4,-30,26)
    kg=mk(ZKING,KSIT[0],KSIT[1],0,'king',z=ROOF_Z+.02); SL=[mk(C,x,y,0,'sl%d'%i) for i,(C,x,y,rz) in enumerate(SLP)]; staff_prop(3.2,RZY+.3,ROOF_Z+.3,lean=-7)
    ZZ=[zzz((lambda H=H: H['head'].matrix_world.translation),ph=i*.23) for i,H in enumerate(SL)]
    kz=zzz((lambda: kg['head'].matrix_world.translation),ph=.6,size=.42)
    def bg(t):
        upd_diners(D,t); upd_kwalkers(Wk,t)
        for i,H in enumerate(SL): C,x,y,rz=SLP[i]; lie(H,x,y,rz,t,i*1.3)
        for z_ in ZZ: z_(t)
    def ksleep(t,k=1.0):
        sit(kg,k,ROOF_Z+.04,legs=90)
        if k<1: kg['root'].location[2]=L(ROOF_Z+.028,kg['root'].location[2],k)
        kg['root'].location[0]=KSIT[0]; kg['root'].location[1]=KSIT[1]-.5*(1-k); kg['root'].rotation_euler=(0,0,0)
        kg['head'].rotation_euler=(R(30*k+3*math.sin(t*1.6)*k),0,R(10*k)); kg['arm'][1].rotation_euler=(R(-38*k),0,0); kg['arm'][-1].rotation_euler=(R(-38*k),0,0)
        cr=kg['kz']['crown']; cr.rotation_euler=(R(-5-14*k),R(10+16*k),0)
    return dict(kg=kg,SL=SL,bg=bg,ksleep=ksleep,kz=kz,S=S)
def SUNRISE():
    Q=roof_morning(); kg=Q['kg']; FILLE[0]=40; TC=ws(227)-.1
    sun=oico((150,10,16),11,M('#FFD9A0',.3,emit=9),sub=3)
    def upd(t):
        Q['bg'](t); Q['ksleep'](t,1.0); blink(kg,t,force=1); zeyes(kg,0); face(kg,mouth='O' if math.sin(t*1.6)>0 else 'o'); Q['kz'](t)
        if t<TC:
            q=ease(t/TC); camset(LV((-17,-.2,2.7),(-15.5,-.2,3.1),q),LV((20,0,7.0),(24,0,8.0),q),L(24,26,q),8)
        else:
            q=ease((t-TC)/(DUR-TC)); camset(LV((-5.6,-14.6,ROOF_Z+5.6),(-4.8,-14.0,ROOF_Z+4.9),q),LV((.6,-8.6,ROOF_Z+.8),(.8,-8.4,ROOF_Z+.9),q),L(22,24,q),8)
    return dict(upd=upd)
SHOTS['SUNRISE']=SUNRISE
def ENOUGH():
    Q=roof_morning(clock=(5,52)); kg=Q['kg']; FILLE[0]=60
    def upd(t):
        Q['bg'](t); w=tl(t,.25,.4); up=tl(t,.75,1.35); Q['ksleep'](t,1-up)
        blink(kg,t,force=0 if w>.5 else 1); zeyes(kg,1.2*w); zglow(kg,.9*w*(1-tl(t,.6,1.2))); face(kg,mouth='frown' if w>.5 else 'o',brow=-.05*w,brow_r=-18*w)
        if w>.5: kg['head'].rotation_euler=(R(L(30,-4,up)),0,R(L(10,0,up)))
        if up>.9: kg['arm'][1].rotation_euler=(R(-25),R(-20),0); kg['arm'][-1].rotation_euler=(R(-25),R(20),0)
        h=kg['head'].matrix_world.translation; q=ease(t/DUR); camset(LV((2.6,KSIT[1]-3.3,ROOF_Z+1.5),(2.4,KSIT[1]-3.6,ROOF_Z+2.2),q),(h.x,h.y,h.z+.25),L(32,34,q),4.0)
    return dict(upd=upd)
SHOTS['ENOUGH']=ENOUGH
def LEAVING():
    Q=roof_morning(clock=(5,53)); kg=Q['kg']; FILLE[0]=60
    def upd(t):
        Q['bg'](t); Q['ksleep'](t,0.0); blink(kg,t); zeyes(kg,1.15); talk(kg,t,*wt(237,241),rate=8,rest='frown'); face(kg,brow=-.05,brow_r=-18)
        k=tl(t,ws(239)-.1,ws(239)+.12); kg['arm'][1].rotation_euler=(R(-25-70*k),R(-20-55*k),0); kg['arm'][-1].rotation_euler=(R(-25),R(20),0); kg['head'].rotation_euler=(R(-4),0,R(-12*k))
        SL=Q['SL']; e=tl(t,ws(240),ws(240)+.15)*(1-tl(t,ws(241)+.2,ws(241)+.4)); blink(SL[1],t,force=1-e); zeyes(SL[1],.8*e)
        h=kg['head'].matrix_world.translation; q=ease(t/DUR); camset(LV((2.9,KSIT[1]-4.4,ROOF_Z+1.25),(2.7,KSIT[1]-4.0,ROOF_Z+1.3),q),(h.x-.2,h.y,h.z+.1),L(26,28,q),4.0)
    return dict(upd=upd)
SHOTS['LEAVING']=LEAVING
# ---------------------------------------------------------------- nobody follows / new careers
def day_street(clock=(8,10),seed=12,pool=None,skip=(),walk=True,rsign='CHACHA MAGHAZ HOUSE',mood='khi_am',nost=()):
    S=burns(mood,clock=clock,night=.0,rest_sign=rsign,nost=nost); TB=street_tables(8,skip=skip)
    D=diners(seed,TB,pool=pool or MIX); Wk=kwalkers(seed+2,((WLANE,1),(-WLANE,-1)),4,-30,26,pool=pool or MIX) if walk else []
    def bg(t):
        upd_diners(D,t); upd_kwalkers(Wk,t); spin_fans(t)
    return dict(S=S,TB=TB,bg=bg)
def NOBODY2():
    Q=day_street(walk=False,skip=(0,1,3)); kg=mk(ZKING,0,0,90,'king'); st=staff(kg,1); FILLE[0]=20
    wv=mk(ZVAR[5],-9.5,WLANE+.2,90,'waver'); wc=chai(wv,-1)
    def upd(t):
        Q['bg'](t); s=1.3*min(t,.75); x=2.0+s
        kg['root'].location[0]=x; kg['root'].location[1]=-WLANE+.1; kg['root'].rotation_euler[2]=R(90)
        if t<.75: walk(kg,s,step=.5,arm=16)
        else: stand(kg,t)
        kpose(kg,1); blink(kg,t); k=tl(t,.72,.92)*(1-tl(t,1.12,1.3)); e=tl(t,1.15,1.3); kg['head'].rotation_euler=(0,0,R(84*k)); face(kg,mouth='O' if e>.5 else 'frown',brow=.06*e-.04*(1-e),brow_r=12*e-14*(1-e)); zeyes(kg,1+.3*e)
        hstand(wv,t); hold_chai(wv,wc,-1,a=-66); wave_hi(wv,t,.9,1,dur=3); face(wv,mouth='grin'); look_at(wv,hp(kg),.5)
        q=ease(t/DUR); camset(LV((9.6,-1.2,1.9),(9.2,-1.3,1.9),q),(x-2.4,-1.4,1.95),L(24,25,q),8)
    return dict(upd=upd)
SHOTS['NOBODY2']=NOBODY2
def RICK():
    faisal('khi_am',0.0,stop_x=70); FILLE[0]=25
    V=krick((0,LANES[1],0),0,'#2E8A3A',seed=7,slogan='ZOMBIE TAXI')
    dr=mk(ZRICK,0,0,90,'zrick'); dr['root'].parent=V['root']; pa=mk(AUNTY_R,0,0,90,'aunty'); pa['root'].parent=V['root']
    T=traffic(41,-60,90,[FLANES[2]]+FLANES[3:],gap=(5,12)); sidewalk_tokens(8,-40,90,60); B.done('ppl')
    def upd(t):
        run_traffic(T,t,.75); x=-6+8.0*t; roll(V,x,LANES[1],0,8.0*t); V['root'].location[2]=.02*abs(math.sin(t*17))
        sit(dr,1,.86,legs=90); dr['root'].location[0]=.55; dr['root'].location[1]=0; dr['root'].rotation_euler=(0,0,R(90)); blink(dr,t)
        arm_to(dr,1,(1.5,-.5,1.52),1); hk=.5+.5*math.sin(t*16); arm_to(dr,-1,(1.5,.5,1.52+.04*hk),1); face(dr,mouth='grin',brow=.04); zeyes(dr,1.1); dr['head'].rotation_euler=(0,0,R(-22+6*math.sin(t*3)))
        sit(pa,1,.82,legs=90); pa['root'].location[0]=-1.35; pa['root'].location[1]=0; pa['root'].rotation_euler=(0,0,R(90)); blink(pa,t)
        pa['arm'][1].rotation_euler=(R(-40),0,0); k=.5+.5*math.sin(t*6); pa['arm'][-1].rotation_euler=(R(-80-12*k),R(10),0); face(pa,mouth='flat',brow=-.02,brow_r=-8)
        q=ease(t/DUR); camset((x+6.4-.5*q,LANES[1]-3.4,1.85),(x+.3,LANES[1],1.8),L(27,29,q),5.6)
    return dict(upd=upd)
SHOTS['RICK']=RICK
def CHAIZ():
    Q=day_street(walk=False,skip=(0,1)); FILLE[0]=25
    ce=chai_counter(0,-1.75,180)
    cw=mk(ZCHAI,0,-2.65,180,'zchai'); kt=kettle(cw,1); cu=[mk(CROWD[1],-2.6,-1.6,128,'c1'),mk(CROWD[18],2.6,-1.6,-128,'c2')]; cups=[chai(cu[0],-1),chai(cu[1],1)]
    st=ocyl((0,0,0),.012,1.0,M('#B5713A',.4,emit=.3),rot=(0,0,0),seg=6); cc=chai(cw,-1); steam((.6,-1.75,1.6),0,9,n=8,seed=2,size=.07)
    def upd(t):
        Q['bg'](t); hstand(cw,t); k=.5+.5*math.sin(t*4.0); cw['arm'][1].rotation_euler=(R(-150-12*k),0,R(10)); upright(kt,cw,1,tilt=-55); hold_chai(cw,cc,-1,a=-58); face(cw,mouth='grin',brow=.05); zeyes(cw,1.1)
        for i,H in enumerate(cu): hstand(H,t); hold_chai(H,cups[i],(-1,1)[i],a=-70); face(H,mouth='grin'); look_at(H,hp(cw),.6)
        kp=kt.matrix_world@Vector((0,-.42,.2)); cp=ce.matrix_world@Vector((.35,.08,1.16)); stream(kp,cp,st)
        q=ease(t/DUR); camset(LV((.8,2.3,1.9),(.6,1.9,1.95),q),(0,-2.5,1.95),L(25,27,q),5.6)
    return dict(upd=upd)
SHOTS['CHAIZ']=CHAIZ
def CRICZ():
    BE=beach('khi_am',sign_at=(70,-9.2),ssize=.4); FILLE[0]=20
    bw=mk(ZCRIC,0,0,90,'zcric'); bt=mk(dict(CRICK[0],top='#2B58C9',trim='#F4F1EA',stripe='#2B58C9',cap='#2B58C9',accent='#2B58C9'),5.2,-4.6,-90,'bat'); b_=bat(bt,1); se,SS=stumps(6.6,-4.0,0)
    fl=[mk(CRICK[1],1.5,-8.2,60,'f1'),mk(CRICK[2],2.2,.2,120,'f2'),mk(CRICK[3],-6.5,-8.8,70,'f3')]
    ball=oico((0,0,-9),.1,M('#F4F1EA',.4,emit=.4),sub=2); TR=.72; TH=1.08
    def upd(t):
        d=min(t,TR+.25)*4.2; x=-9.5+d; bw['root'].location[0]=x; bw['root'].location[1]=-4.0; bw['root'].rotation_euler[2]=R(90)
        if t<TR+.25: run(bw,d)
        else: stand(bw,t)
        a=tl(t,TR-.3,TR+.1); bw['arm'][1].rotation_euler=(R(L(30,-205,a)) if t<TR+.25 else R(-160),0,0); blink(bw,t); zeyes(bw,1.1)
        rel=Vector((-9.5+TR*4.2+.3,-4.0-.6,3.0))
        if t<TR: ball.location=(0,0,-9)
        elif t<TH: q=(t-TR)/(TH-TR); ball.location=(L(rel.x,6.55,q),L(rel.y,-4.0,q),L(rel.z,.9,q)-1.2*q*(1-q)*0+.0)
        else: d2=t-TH; ball.location=(6.55+2.5*d2,-4.0+.6*d2,max(.1,.9+2*d2-4.9*d2*d2))
        hstand(bt,t); k=tl(t,TH-.15,TH+.05); bt['arm'][1].rotation_euler=(R(L(-35,-120,k)),R(L(-30,20,k)),0); bt['arm'][-1].rotation_euler=(R(L(-30,-100,k)),R(20),0); face(bt,mouth='O' if t>TH else 'flat',brow=.06 if t>TH else 0)
        if t>TH:
            d2=t-TH
            for i,o in enumerate(SS[:3]): o.rotation_euler=(R((i-1)*70*min(1,d2*3)),R(80*min(1,d2*3)),0); o.location=(.5*min(1,d2*3)*(1+.3*i),(i-1)*.16+(i-1)*.5*min(1,d2*3),.6-.45*min(1,d2*3))
            for i,o in enumerate(SS[3:]): o.location=(.6*d2*3,( -.08 if i==0 else .08)+(i-.5)*2.4*d2,max(.03,1.22+3*d2-4.9*d2*d2))
        cel=tl(t,TH+.1,TH+.35)
        if cel>0: shock(bw,cel); bw['root'].location[2]=bw['z0']+.008+.35*abs(math.sin((t-TH)*7)); face(bw,mouth='grin',brow=.06)
        for i,H in enumerate(fl):
            hstand(H,t); look_at(H,ball.location if t<TH else hp(bw),.7)
            if cel>0: shock(H,cel); H['root'].location[2]=H['z0']+.008+.3*abs(math.sin((t-TH)*7+i)); face(H,mouth='grin')
        if t<TH-.14: camset((x+5.6,-6.9,1.15),(x+.4,-4.0,1.75),28,8)
        else: q=ease((t-TH+.14)/(DUR-TH+.14)); camset(LV((9.4,-1.9,.75),(9.7,-1.6,.95),q),(6.2,-4.1,1.0),L(24,22,q),8)
    return dict(upd=upd)
SHOTS['CRICZ']=CRICZ
def BOSS():
    Q=day_street(walk=False,skip=(0,1,3)); kg=mk(ZKING,3.6,-WLANE+.1,90,'king'); st=staff(kg,1); FILLE[0]=25
    zd=mk(ZED,6.6,-WLANE+.3,-90,'zed'); c1=chai(zd,1); c2=chai(zd,-1)
    def upd(t):
        Q['bg'](t); stand(kg,t); kpose(kg,1); kg['root'].location[0]=3.6; kg['root'].rotation_euler[2]=R(90); blink(kg,t); face(kg,mouth='frown',brow=-.02,brow_r=-6); look_at(kg,hp(zd),.6,maxpitch=25)
        stand(zd,t); blink(zd,t); zd['root'].rotation_euler[2]=R(-90); k=tl(t,ws(262),ws(262)+.3); hold_chai(zd,c1,1,a=-64,sip=.0); hold_chai(zd,c2,-1,a=L(-60,-92,k),out=6); zd['head'].rotation_euler[1]=0
        talk(zd,t,*wt(261,266),rate=7.5,rest='grin'); face(zd,brow=.05); look_at(zd,hp(kg),.8,maxpitch=30); zeyes(zd,1.1)
        q=ease(t/DUR); camset(LV((4.5,-.7,2.05),(4.7,-.9,2.05),q),(6.55,-WLANE+.3,1.86),L(40,42,q),4.0)
    return dict(upd=upd)
SHOTS['BOSS']=BOSS
# ---------------------------------------------------------------- one month later / Monday morning
def MONTH():
    faisal('khi',0.0,stop_x=0,clear=12); FILLE[0]=20
    Qp=[(CROWD[0],-4.6,0),(ZVAR[6],-2.7,0),(CROWD[14],-.8,0),(ZVAR[3],1.1,0),(WALEED,3.0,0),(ZVAR[9],4.9,0)]
    P=[mk(C,x,RW+.85,0,'q%d'%i) for i,(C,x,_) in enumerate(Qp)]; ph=phone_in_hand(P[4],1,'#BFE0FF',em=1.5)
    np_=in_hand(P[1],1,lambda e: obox((0,-.1,.12),(.26,.01,.2),M('#E8E4DA',.8),.004,e))
    bus=w11((-30,LANES[2],0),0,seed=6,col='#1E8A4A',accent='#F2C14E'); bus_heads(bus,random.Random(5)); mb=kbike((0,LANES[0],0),0,'#C8372D',rider=ZVAR[5],name='zbiker')
    T=traffic(51,-70,90,[FLANES[1]]+FLANES[3:],gap=(6,14)); sidewalk_tokens(9,-60,90,70,skip=lambda x,y: abs(x)<9 and y>0); B.done('ppl')
    def upd(t):
        run_traffic(T,t,.8); bd=18.0*ease_out(t/DUR); roll(bus,-30+bd,LANES[2],0,bd); roll(mb,-16+10*t,LANES[0],0,10*t)
        for i,H in enumerate(P):
            hstand(H,t);
            if i==1: H['arm'][1].rotation_euler=(R(-74),0,R(8)); H['head'].rotation_euler[0]=R(14)
            elif i==4: hold_phone(H,1,1.0); H['head'].rotation_euler[0]=R(20)
            elif i in (3,5): look_at(H,(bus['root'].location[0],LANES[2],2.5),.7)
            else: look_at(H,(bus['root'].location[0],LANES[2],2.5),.5)
            if H['C'].get('zombie'): zeyes(H,1.0); face(H,mouth='smile')
            else: face(H,mouth='smile')
        q=ease(t/DUR); camset(LV((6.6,10.3,2.0),(6.0,10.6,2.0),q),LV((.9,RW+.8,1.85),(1.1,RW+.8,1.85),q),L(27,29,q),8)
    return dict(upd=upd)
SHOTS['MONTH']=MONTH
def MONDAY():
    faisal('khi_am',0.0,stop_x=DOORX-9.5,clear=20.0,gantry_x=8); T,TS,Bs=jam(); FILLE[0]=45; TC=ws(281)-.25
    point((BUSX,BY,3.1),300,(1,.95,.85),r=.8,shadow=False)
    PS=[(dict(CROWD[3],wide=1.0),-1.5),(dict(ZVAR[10]),.1),(WALEED,1.7),(dict(ZED),3.1)]; P=[mk(C,BUSX+lx,BY+.72,90,'ps%d'%i,z=Bs['z0']) for i,(C,lx) in enumerate(PS)]; bus_heads(Bs,random.Random(4),skipx=(-1.5,.1,1.7,3.1))
    for H in P:
        u=H['u']
        if not H['C'].get('zombie'):
            for s in (-1,1): obox((s*.25*u,-.62*u-.006,.47*u),(.13*u,.004,.028*u),M(shade(H['C']['skin'],.62),.7),.002,H['head'])
    def upd(t):
        run_traffic(TS,t,.25)
        yw=tl(t,TC+.15,TC+.45)*(1-tl(t,TC+1.25,TC+1.5))
        for i,H in enumerate(P):
            stand(H,t); H['root'].location[2]=Bs['z0']+.008; H['root'].rotation_euler=(0,0,R(90)); s_in=-1
            arm_to(H,1,(BUSX+PS[i][1]+.25,BY+.05,3.27),1); H['arm'][-1].rotation_euler=(R(-6),0,0)
            sw=.03*math.sin(t*1.7+i); H['root'].rotation_euler[1]=sw; H['head'].rotation_euler=(R(10+6*math.sin(t*.9+i*1.7)),0,R(74))
            y_=yw if i>=2 else (.5+.5*math.sin(t*.8+i*2.3))**6
            droopy(H,.52+.48*y_); face(H,mouth='O' if y_>.4 else 'flat',brow=-.02);
            if H['C'].get('zombie'): zeyes(H,.8*(1-y_))
            H['head'].rotation_euler[0]=R(10-18*y_)
        nd=tl(t,TC+1.55,TC+1.8)
        if nd>0:
            P[2]['head'].rotation_euler=(R(6),0,R(74-36*nd)); P[3]['head'].rotation_euler=(R(6),0,R(74+34*nd)); face(P[2],mouth='smile'); face(P[3],mouth='smile')
        if t<TC:
            q=t/TC; x=BUSX+L(-2.0,2.0,ease(q)); camset((x,BY+3.9,2.9),(x,BY+1.6,2.92),40,8)
        else:
            q=ease((t-TC)/(DUR-TC)); camset(LV((BUSX+2.5,BY+4.3,2.9),(BUSX+2.45,BY+4.8,2.9),q),(BUSX+2.4,BY+1.6,2.92),L(40,42,q),8)
    return dict(upd=upd)
SHOTS['MONDAY']=MONDAY
# ---------------------------------------------------------------- finale
RS2='ZOMBIE KING MAGHAZ HOUSE'
def finale_set(clock=(9,30),street=True,walk=True,skip=(0,1),dskip=()):
    S=burns('night',clock=clock,rest_sign=RS2); RT=rest_tables(dress=(2,2,2,1,2)); TB=street_tables(8,skip=skip); B.done('x')
    RD=diners(13,RT,skip=(0,),pool=MIX); SD=diners(14,TB,pool=MIX,skip=dskip) if street else []; Wk=kwalkers(15,((-WLANE,-1),),4,-30,24,pool=MIX) if walk else []
    kg=mk(ZKING_CHEF,-4.9,BW+2.05,0,'kingchef')
    def bg(t):
        upd_diners(RD,t); upd_diners(SD,t); upd_kwalkers(Wk,t); spin_fans(t)
    def kcook(t):
        cook_anim(kg,t); kg['root'].location[0]=-4.9; kg['root'].location[1]=BW+2.05; kg['root'].rotation_euler[2]=0; blink(kg,t); zeyes(kg,1.1); face(kg,mouth='grin',brow=.03)
    return dict(S=S,RT=RT,TB=TB,kg=kg,bg=bg,kcook=kcook)
def KINGQ():
    Q=finale_set(street=False,walk=False); kg=Q['kg']; FILLE[0]=25
    sh=empty((0,BW-.05,4.62)); obox((0,0,-2.3),(2.3,.05,2.3),M('#8A8E96',.5,metal=.5),.0,sh)
    for j in range(13): obox((0,-.06,-4.4+j*.36),(2.3,.02,.03),M('#5A5E66',.5),0,sh)
    sign('NOW OPEN',(3.4,BW-1.2,1.5),.34,'#FFFFFF','#C8372D',n=(0,-1,0),e=2.5,pad=.2,th=.06,parent=empty((0,0,0)),always=True)
    for sx in (-1,1): obox((3.4+sx*.9,BW-1.15,.55),(.04,.04,.55),M('#5A5E66',.5),0)
    def upd(t):
        Q['bg'](t); stand(kg,t); kg['root'].location[0]=0; kg['root'].location[1]=BW+1.3; kg['root'].rotation_euler[2]=0; blink(kg,t); zeyes(kg,1.1); face(kg,mouth='smirk',brow=.03)
        kg['arm'][1].rotation_euler=(0,R(-30),0); kg['arm'][-1].rotation_euler=(0,R(30),0)
        k=tl(t,.2,.95); sh.scale=(1,1,max(.02,1-k))
        q=ease(t/DUR); camset(LV((.25,1.7,1.4),(.2,2.0,1.4),q),(0,BW+.6,2.0),L(31,32,q),8)
    return dict(upd=upd)
SHOTS['KINGQ']=KINGQ
def RESTO():
    Q=finale_set(walk=False); kg=Q['kg']; FILLE[0]=30
    qu=[mk(C,x,BW-.9,0 if i%2 else 180,'qu%d'%i) for i,(C,x) in enumerate(((CROWD[6],-6.9),(dict(ZVAR[4]),-3.0),(CROWD[19],-1.1),(dict(ZVAR[1],chefhat=None),.9)))]
    def upd(t):
        Q['bg'](t); Q['kcook'](t)
        for i,H in enumerate(qu): hstand(H,t); H['root'].rotation_euler[2]=R(180); look_at(H,hp(kg),.7); face(H,mouth='grin');
        q=ease(t/DUR); camset(LV((3.4,-3.8,1.5),(2.8,-3.2,1.6),q),LV((-1.4,BW,3.5),(-1.9,BW,3.4),q),L(18,19,q),8)
    return dict(upd=upd)
SHOTS['RESTO']=RESTO
WSEAT=(ZTAB[0]+1.28,ZTAB[1],-90)
def DIEFOR():
    Q=finale_set(street=False,walk=False); kg=Q['kg']; FILLE[0]=30; TC=ws(301)-.2
    wa=mk(WALEED,0,0,0,'wa'); zd=mk(ZED,0,0,0,'zed'); sp=spoon(wa,1); steam((ZTAB[0],ZTAB[1],1.5),0,9,n=10,seed=7,size=.06)
    sparkles((WSEAT[0],WSEAT[1],1.95),.7,ws(300),9,n=22,size=.03,seed=6,rise=.5)
    def upd(t):
        Q['bg'](t); sitat(zd,ZSEAT,t); diner(zd,ZSEAT,t,1.0); zd['head'].rotation_euler[1]=0; zeyes(zd,1.1); face(zd,mouth='grin')
        sitat(wa,WSEAT,t); m=root_mat(wa); c=tl(t,.35,1.0); mouth=m@Vector((.05,-.36,1.9)); pl=Vector((ZTAB[0]+.25,ZTAB[1]+.1,1.52)); arm_to(wa,1,pl.lerp(mouth,c),1); upright(sp,wa,1); rs=m@Vector((-.36,-.82,0)); rs.z=1.44; arm_to(wa,-1,rs,1)
        e=tl(t,1.0,1.2); face(wa,mouth='grin' if e>.5 else 'smile',brow=.06*e,eyes=1+.25*e)
        stand(kg,t); kg['root'].location[0]=ZTAB[0]+.2; kg['root'].location[1]=ZTAB[1]+1.95; kg['root'].rotation_euler[2]=0; blink(kg,t); zeyes(kg,1.1)
        kk=tl(t,TC,TC+.3); kg['arm'][1].rotation_euler=(R(-30-100*kk),R(-20+34*kk),0); kg['arm'][-1].rotation_euler=(R(-20),R(16),0); face(kg,mouth='grin',brow=.04); zglow(kg,.7*tl(t,ws(303),ws(303)+.2))
        if t>TC+.5: kg['lids'][0].scale=(1,1,1)
        if t<TC:
            q=ease(t/TC); camset(LV((ZTAB[0]-1.5,ZTAB[1]-1.9,1.75),(ZTAB[0]-1.2,ZTAB[1]-1.7,1.78),q),(WSEAT[0]-.2,WSEAT[1]+.1,1.72),L(32,35,q),4.0)
        else:
            h=hp(kg); q=ease((t-TC)/(DUR-TC)); camset(LV((ZTAB[0]-.5,ZTAB[1]-.9,1.45),(ZTAB[0]-.4,ZTAB[1]-.6,1.5),q),(h[0],h[1],h[2]+.1),L(30,33,q),4.0)
    return dict(upd=upd)
SHOTS['DIEFOR']=DIEFOR
def CTA():
    Q=finale_set(skip=(1,),dskip=(0,)); kg=Q['kg']; FILLE[0]=40
    TB=Q['TB']; st=TB[0][1]; wa=mk(WALEED,0,0,0,'wa'); zd=mk(ZED,0,0,0,'zed'); c1=chai(wa,1); c2=chai(zd,-1)
    FW=[firework((-6,-9,22),.6,'#FF5A8A',seed=1),firework((16,9,26),1.2,'#FFD23F',seed=2),firework((30,-8,24),1.9,'#5AD2FF',seed=3),firework((2,10,28),2.5,'#9AFF7A',seed=4)]
    def upd(t):
        Q['bg'](t); Q['kcook'](t); k=tl(t,.25,.6)
        sitat(wa,st[1],t); sitat(zd,st[0],t); zd['head'].rotation_euler[1]=0
        hold_chai(wa,c1,1,a=L(-70,-104,k)); wa['arm'][-1].rotation_euler=(R(-46),0,0); hold_chai(zd,c2,-1,a=L(-70,-104,k)); zd['arm'][1].rotation_euler=(R(-46),0,0)
        look_at(wa,CAM.location,.9,maxyaw=85,maxpitch=40); look_at(zd,CAM.location,.9,maxyaw=85,maxpitch=40); face(wa,mouth='grin',brow=.05); face(zd,mouth='grin',brow=.05); zeyes(zd,1.15)
        for f in FW: f(t)
        q=ease(max(0,(t-.55)/(DUR-.55))); camset(LV((9.0,-4.5,2.25),(-9.5,-.2,4.9),q),LV((9.0,.8,1.7),(30,0,7.6),q),L(24,22,q),8)
    return dict(upd=upd)
SHOTS['CTA']=CTA
