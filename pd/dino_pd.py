# "Pindi vs the Dinosaur": the T-Rex (Sheru) and the Pindi 70cc bike.
# Dino faces -y at rz=0 (same as the avatars). Legs are 2-bone IK so the feet stay planted (no sliding).
DG='#4FAE3C'; DGD='#2C7A2E'; DBL='#F1E3A4'
def dino(loc=(0,0,0),rz=0,s=1.0,name='sheru'):
    root=empty(loc,rot=(0,0,R(rz))); root.name=name; root.scale=(s,)*3
    g=M(DG,.72,spec=.25); gd=M(DGD,.78,spec=.2); bl=M(DBL,.78,spec=.2); wh=M('#FFF8E6',.4); mo=M('#A82A3A',.6); tg=M('#EE6E86',.55); bk=M('#141418',.35); cl=M('#F4EAD0',.45)
    HZ=4.75; Lt=2.9; Ls=2.9; AZ=.5
    hip=empty((0,0,HZ),root)
    obox((0,-1.5,.35),(1.45,2.55,1.55),g,.5,hip); obox((0,-1.6,-.95),(1.18,2.2,.55),bl,.35,hip)            # torso + belly
    obox((0,-3.75,.75),(1.2,.75,1.3),g,.45,hip); obox((0,-3.85,-.3),(.95,.6,.6),bl,.3,hip)                  # chest
    obox((0,.75,.4),(1.3,.9,1.4),g,.5,hip)                                                                # rump
    for k in range(5): obox((0,-3.3+k*1.0,1.86+(.04 if k in (1,2) else 0)),(.95-.05*abs(k-2),.2,.08),gd,.05,hip)
    for k in range(6): obox((0,-3.6+k*.95,1.98),(.13,.3,.3),gd,.06,hip,rot=(R(45),0,0))                       # dorsal plates
    # tail: 6 segments
    T=[]; par=hip; py=(0,1.3,.35); TW=[(1.15,1.2),(.95,.98),(.76,.78),(.57,.58),(.4,.4),(.24,.24)]
    for i,(w,h) in enumerate(TW):
        e=empty(py,par); obox((0,.85,0),(w,1.0,h),g,min(w,h)*.42,e); obox((0,.85,-h*.55),(w*.72,.9,h*.45),bl,min(w,h)*.3,e)
        obox((0,.55,h+.02),(w*.62,.17,.07),gd,.04,e); obox((0,1.25,h+.0),(w*.55,.15,.07),gd,.04,e)
        obox((0,.9,h+.05),(.1,.22*(1-.1*i),.22*(1-.1*i)),gd,.05,e,rot=(R(45),0,0))
        T.append(e); par=e; py=(0,1.6,0)
    # neck + head
    neck=empty((0,-4.0,1.25),hip); obox((0,-.35,1.0),(.95,.85,1.45),g,.4,neck); obox((0,-.95,.75),(.7,.3,1.1),bl,.2,neck)
    obox((0,.42,1.5),(.6,.12,.07),gd,.04,neck); obox((0,.42,.9),(.66,.12,.07),gd,.04,neck)
    for z in (.5,1.3,2.05): obox((0,.55,z),(.12,.26,.26),gd,.06,neck,rot=(R(45),0,0))
    head=empty((0,-.55,2.2),neck)
    obox((0,-.35,.45),(1.28,1.3,.98),g,.34,head)                                   # skull
    obox((0,-2.35,.14),(1.02,1.15,.62),g,.26,head)                                 # snout
    obox((0,-2.2,-.5),(.86,1.25,.04),mo,.0,head)                                   # roof of the mouth
    for sx in (-1,1):
        obox((sx*.48,-3.44,.62),(.13,.1,.09),gd,.04,head)                          # nostril
        for k in range(6): obox((sx*.93,-3.3+k*.38,-.6),(.07,.11,.2-.012*k),wh,.04,head)
    for k in range(5): obox((-.62+k*.31,-3.42,-.6),(.09,.07,.2),wh,.04,head)
    jaw=empty((0,-.15,-.5),head)
    obox((0,-1.55,-.36),(.92,1.75,.3),g,.2,jaw); obox((0,-1.6,-.62),(.72,1.5,.1),bl,.08,jaw); obox((0,-1.5,-.04),(.62,1.35,.05),tg,.04,jaw)
    for sx in (-1,1):
        for k in range(5): obox((sx*.82,-3.05+k*.42,.06),(.06,.1,.15-.012*k),wh,.035,jaw)
    for k in range(4): obox((-.48+k*.32,-3.2,.06),(.08,.06,.15),wh,.035,jaw)
    # eyes on the front corners of the skull, looking 30 deg outwards
    EY=[]; LID=[]; BRW=[]; PUP=[]
    for sx in (-1,1):
        a=R(30)*sx; f=Vector((math.sin(a),-math.cos(a),0)); c=Vector((sx*.92,-1.5,1.02))
        obox(tuple(c+Vector((0,.25,0))),(.5,.45,.52),gd,.16,head)                                             # socket
        ey=oico(tuple(c),.44,M('#FFD83A',.25,emit=.25),head,sub=3); EY.append(ey)
        pu=oico(tuple(c+f*.36),.2,bk,head,sc=(.62,.62,1.25),sub=2); PUP.append((pu,c,f)); oico(tuple(c+f*.44+Vector((sx*.02,0,.16))),.06,M('#FFFFFF',.2,emit=1.0),head,sub=1)
        lid=obox(tuple(c+Vector((0,-.02,.5))),(.5,.5,.26),g,.1,head); LID.append((lid,c)); br=obox(tuple(c+Vector((0,-.12,.62))),(.6,.56,.13),gd,.07,head); BRW.append((br,c,sx))
    # big shades (hidden until worn)
    sh=empty((0,0,-60),head); sm=M('#0E0F14',.12,spec=1.0)
    for sx in (-1,1):
        obox((sx*.78,-2.06,1.12),(.6,.06,.44),sm,.12,sh); obox((sx*1.36,-1.2,1.2),(.05,.9,.09),sm,.03,sh); obox((sx*.55,-2.13,1.3),(.18,.01,.05),M('#FFFFFF',.2,emit=.6),.0,sh,rot=(0,R(-20*sx),0))
    obox((0,-2.06,1.28),(.25,.05,.09),sm,.03,sh)
    # arms
    ARM=[]
    for sx in (-1,1):
        a=empty((sx*1.28,-3.75,-.2),hip); obox((0,-.08,-.5),(.22,.22,.6),g,.12,a); fa=empty((0,-.1,-1.0),a); obox((0,-.42,0),(.17,.48,.17),g,.1,fa)
        for dx in (-.09,.09): obox((dx,-.98,-.03),(.05,.14,.05),cl,.03,fa)
        ARM.append((a,fa))
    # legs
    LEG={}
    for sx in (1,-1):
        th=empty((sx*1.3,0,HZ),root); obox((0,.05,-1.3),(.8,1.05,1.75),g,.45,th); obox((sx*.3,.0,-1.2),(.56,.5,.9),gd,.2,th)
        shn=empty((0,0,-Lt),th); obox((0,0,-1.45),(.5,.56,1.6),g,.3,shn)
        ft=empty((0,0,-Ls),shn); obox((0,-.5,-.2),(.74,1.1,.28),g,.2,ft); obox((0,.55,-.05),(.3,.3,.22),g,.14,ft)
        for dx in (-.48,0,.48): obox((dx,-1.72,-.28),(.2,.42,.2),g,.1,ft); obox((dx,-2.22,-.34),(.12,.22,.13),cl,.07,ft)
        LEG[sx]=(th,shn,ft)
    D=dict(root=root,hip=hip,tail=T,neck=neck,head=head,jaw=jaw,eyes=EY,lids=LID,brows=BRW,pups=PUP,arms=ARM,leg=LEG,shades=sh,HZ=HZ,Lt=Lt,Ls=Ls,AZ=AZ,s=s)
    dino_face(D,'calm'); return D
def _dleg(D,sx,fx,lift,hz,toe=0.0):
    Lt,Ls=D['Lt'],D['Ls']; vz=hz-(D['AZ']+lift); Dd=min(math.hypot(fx,vz),Lt+Ls-.03); al=math.atan2(fx,vz)
    be=math.acos(max(-1,min(1,(Lt*Lt+Dd*Dd-Ls*Ls)/(2*Lt*Dd)))); ga=math.acos(max(-1,min(1,(Lt*Lt+Ls*Ls-Dd*Dd)/(2*Lt*Ls)))); tt=al+be; ts=tt-(pi-ga)
    th,shn,ft=D['leg'][sx]; th.location[2]=hz; th.rotation_euler[0]=-tt; shn.rotation_euler[0]=pi-ga; ft.rotation_euler[0]=ts+toe
def dino_legs(D,dist=None,hz=0.0,S=4.2,lift=1.0,duty=.62,st=(.45,-.35)):
    """dist = distance walked along the facing direction (None = stand). returns the hip height used"""
    H=D['HZ']+hz
    if dist is None:
        _dleg(D,1,st[0],0,H); _dleg(D,-1,st[1],0,H); D['hip'].location[2]=H; return H
    cyc=S/duty; p=(dist/cyc)%1.0; H=H-.1+.16*abs(math.sin(2*pi*p+.5))
    for sx in (1,-1):
        q=(p+(0 if sx==1 else .5))%1.0
        if q<duty:
            k=q/duty; fx=S/2-S*k; toe=R(24)*ease(max(0,(k-.72)/.28)); lf=1.5*math.sin(toe)
        else:
            e=(q-duty)/(1-duty); fx=-S/2+S*ease(e); toe=R(24)*(1-e)**2-R(10)*math.sin(pi*e)*e; lf=lift*math.sin(pi*e)+1.5*math.sin(max(0,toe))*(1-e)
        _dleg(D,sx,fx,lf,H,toe)
    D['hip'].location[2]=H; return H
def dino_pose(D,t,dist=None,pitch=8,hz=0.0,neck=28,head=0,hyaw=0,jaw=0.0,roll=0.0,yaw=0.0,tail=1.0,sway=1.0,hroll=0.0,st=(.45,-.35),S=4.2,arms=0.0):
    """pitch/neck/head in degrees, positive = up. head = world pitch of the head. hyaw positive = turn to its left (+x side at rz=0 is its left? no: its RIGHT is -x) -> hyaw>0 turns toward +x"""
    dino_legs(D,dist,hz,S=S,st=st)
    br=math.sin(t*1.7)
    ph=0.0 if dist is None else 2*pi*dist/(S/.62)
    D['hip'].rotation_euler=(-R(pitch+.5*br*sway),R(roll+(2.2*math.sin(ph) if dist is not None else 0)),R(yaw+(2.5*math.sin(ph+1.2) if dist is not None else 0)))
    nk=neck+1.2*br*sway
    D['neck'].rotation_euler=(-R(nk),0,R(hyaw*.4))
    D['head'].rotation_euler=(-R(head)+R(pitch)+R(nk),R(hroll),R(hyaw*.6))
    D['jaw'].rotation_euler[0]=R(34*jaw)
    for i,e in enumerate(D['tail']):
        sw=(9+3*i)*math.sin(t*1.5-i*.7+(ph if dist is not None else 0))*tail
        e.rotation_euler=(R(pitch*(.42 if i<2 else (.16 if i==2 else 0))+2*math.sin(t*1.1+i)),0,R(sw*.5))
    for k,(a,fa) in enumerate(D['arms']):
        sx=-1 if k==0 else 1; w=math.sin(t*3.1+k*1.7)
        a.rotation_euler=(R(-18-55*arms+5*w),0,R(-sx*8*arms)); fa.rotation_euler=(R(-22-30*arms+8*w*(1+arms)),0,0)
DFACE=dict(calm=(.18,0,0,1.0),angry=(.42,-.06,20,.9),scared=(-.05,.2,-22,.62),happy=(.34,.04,-6,1.05),bored=(.55,-.02,4,1.0),curious=(.05,.12,-8,1.0),shut=(1.0,-.06,0,1.0),smug=(.48,.0,10,1.0))
def dino_face(D,m,k=1.0,mix=None):
    """lid 0 open..1 shut, brow raise, brow slant (+ angry), pupil size. mix=(other mood, 0..1) blends"""
    a=DFACE[m]
    if mix: b=DFACE[mix[0]]; a=tuple(L(x,y,mix[1]) for x,y in zip(a,b))
    lid,bz,br,pu=a
    for (o,c) in D['lids']: o.location[2]=c.z+.62-.6*lid; o.scale=(1,1,.35+.9*lid)
    for (o,c,sx) in D['brows']: o.location[2]=c.z+.66+bz-.3*max(0,lid-.3); o.rotation_euler=(R(-br*.5),R(sx*br),0)
    for (o,c,f) in D['pups']: o.scale=(.62*pu,.62*pu,1.25*pu)
def dino_eyes(D,dx=0.0,dz=0.0):
    """shift the pupils (look sideways / up-down), units ~ -1..1"""
    for (o,c,f) in D['pups']:
        rt=Vector((-f.y,f.x,0)); o.location=c+f*.36+rt*(.16*dx)+Vector((0,0,.14*dz))
def dino_blink(D,t,m='calm'):
    q=(t+1.3)%3.1
    if q<.12: dino_face(D,'shut')
    else: dino_face(D,m)
def dino_shades(D,k=1.0):
    D['shades'].location=(0,0,(-60 if k<=0 else 0)); D['shades'].scale=(k,k,k) if k>0 else (0,0,0)
def dino_headw(D): return D['head'].matrix_world@Vector((0,-1.2,.4))
def dino_mouthw(D): return D['head'].matrix_world@Vector((0,-3.4,-.4))
def dino_roar(t,t0,t1,a=1.0):
    """jaw amount for a roar between t0..t1 with a shake"""
    if t<t0 or t>t1+.25: return 0.0
    k=ease((t-t0)/.18)*(1-ease((t-t1)/.25)); return a*k*(.92+.08*math.sin(t*38))
# ---------------------------------------------------------------- bike
BKC=['#C8232B','#16171C','#1E4FA8','#C8232B','#E6A31C','#16171C','#C8232B','#2E8A4A']
def pbike(loc=(0,0,0),rz=0,col='#C8232B',rider=None,name='rider',pillion=None,sc=1.45,light=False,plate=None,flag=None):
    """Pindi 70cc. faces +x. V['piv'] = wheelie pivot on the rear axle (negative ry lifts the front). rider/pillion = cast dicts"""
    root=empty(loc,rot=(0,0,R(rz))); root.scale=(sc,)*3; rr=.33; piv=empty((-.64,0,rr),root); P=empty((.64,0,-rr),piv)       # P = bike frame origin under the bike centre
    body=M(col,.3,metal=.25,spec=.7); ch=M('#D4D8E0',.22,metal=.9); blk=M('#141418',.6); dm=M('#3A3D44',.45,metal=.6); W=[]
    obox((-.02,0,.6),(.52,.045,.045),dm,.02,P,rot=(0,R(-6),0)); obox((.06,0,.4),(.2,.11,.13),dm,.04,P); obox((.2,0,.45),(.1,.09,.1),ch,.03,P,rot=(0,R(-20),0))     # frame + engine
    for k in range(3): obox((.26,0,.4+.045*k),(.12,.1,.008),dm,0,P,rot=(0,R(-20),0))
    obox((.2,0,.8),(.27,.145,.12),body,.08,P); obox((.2,0,.925),(.2,.03,.008),M('#F4F1EA',.4),0,P)                             # tank
    for sy in (-1,1): obox((.12,sy*.15,.78),(.13,.012,.07),blk,.02,P); obox((.22,sy*.151,.86),(.2,.004,.02),M('#F2C14E',.4),0,P)
    obox((-.3,0,.86),(.38,.135,.05),blk,.045,P); obox((-.58,0,.9),(.1,.13,.05),blk,.04,P)                                       # seat
    for sy in (-1,1): obox((-.18,sy*.12,.62),(.2,.012,.1),body,.03,P)                                                           # side panel
    obox((-.64,0,.7),(.3,.075,.025),body,.02,P,rot=(0,R(8),0)); obox((-.96,0,.66),(.03,.07,.05),M('#E8301A',.3,emit=2.5),.02,P)  # rear guard + tail light
    obox((-.99,0,.52),(.012,.13,.075),M('#F4F1EA',.5),.01,P)
    if plate: text(plate,(-1.004,0,.52),(-1,0,0),.055,M('#16171C',.5),ex=.002,parent=P)
    obox((-.84,0,.86),(.16,.11,.012),ch,.0,P); obox((-.99,0,.9),(.012,.11,.05),ch,0,P)                                           # carrier
    for sy in (-1,1):
        ocyl((-.56,sy*.1,.55),.022,.5,ch,P,rot=(0,R(22),0),seg=8)                                                               # shocks
        ocyl((.54,sy*.075,.66),.022,.74,ch,P,rot=(0,R(-24),0),seg=8)                                                             # forks
        ocyl((.42,sy*.36,1.12),.028,.12,blk,P,rot=(R(90),0,0),seg=8)                                                             # grips
        ocyl((.4,sy*.26,1.24),.008,.22,ch,P,rot=(0,0,0),seg=6); ocyl((.4,sy*.26,1.36),.055,.012,ch,P,rot=(0,R(90),0),seg=12)     # mirrors
        obox((.5,sy*.2,.98),(.03,.03,.03),M('#FF9A1E',.3,emit=1.5),.012,P)                                                       # indicators
    obox((.42,0,1.1),(.025,.36,.018),ch,.008,P); obox((.45,0,1.02),(.05,.07,.07),blk,.02,P)                                      # bar + clock
    obox((.64,0,.68),(.26,.07,.022),ch,.02,P,rot=(0,R(-6),0))                                                                   # front guard
    ocyl((.56,0,.98),.105,.12,blk,P,rot=(0,R(90),0),seg=14); ocyl((.625,0,.98),.09,.012,M('#FFF6D8',.2,emit=7.0),P,rot=(0,R(90),0),seg=14)    # headlight
    ocyl((-.28,-.14,.34),.032,.95,ch,P,rot=(0,R(84),0),seg=10); ocyl((-.76,-.14,.39),.042,.05,M('#1A1A1E',.6),P,rot=(0,R(84),0),seg=10)        # straight pipe, no silencer
    obox((.12,-.13,.34),(.1,.02,.02),ch,0,P)
    if flag: ocyl((-.95,.1,1.4),.01,1.0,ch,P,rot=(0,0,0),seg=6); obox((-1.12,.1,1.76),(.17,.006,.11),M(flag,.7,kind='fabric'),0,P)
    W.append(wheel((.64,0,rr),rr,.09,P)); W.append(wheel((-.64,0,rr),rr,.11,P))
    V=dict(root=root,piv=piv,P=P,wheels=W,r=rr*sc,sc=sc,col=col,lamp=None)
    if light:
        bpy.ops.object.light_add(type='SPOT',location=(0,0,0)); lp=bpy.context.object; lp.data.energy=light; lp.data.color=(1,.93,.78); lp.data.spot_size=R(62); lp.data.spot_blend=.7; lp.data.use_shadow=False
        lp.parent=P; lp.location=(.7,0,.98); lp.rotation_euler=(0,R(-82),0); V['lamp']=lp
    for key,C_,x in (('rider',rider,-.2),('pillion',pillion,-.62)):
        if C_ is None: continue
        H=mk(C_,0,0,0,name+('' if key=='rider' else '_p')); H['root'].parent=P; H['root'].scale=(1/sc,)*3; H['root'].rotation_euler=(0,0,R(90)); V[key]=H; H['bx']=x
    bike_sit(V,0); return V
def bike_sit(V,t,lean=0.0,look=None):
    for key in ('rider','pillion'):
        H=V.get(key)
        if H is None: continue
        sit(H,1,.9*V['sc'],legs=78); H['root'].location=(H['bx'],0,H['root'].location[2]/V['sc']-.0); H['root'].rotation_euler=(R(lean),0,R(90)); blink(H,t)
        for s in (1,-1): H['arm'][s].rotation_euler=(R(-72 if key=='rider' else -30),0,R(s*(7 if key=='rider' else 2)))
        H['head'].rotation_euler=(0,0,0)
def bike_roll(V,x,y,rz,dist,wheelie=0.0,z=0.0,bank=0.0):
    V['root'].location=(x,y,z); V['root'].rotation_euler=(R(bank),0,R(rz)); V['piv'].rotation_euler[1]=-R(wheelie)
    for w in V['wheels']: w.rotation_euler[1]=dist/V['r']
def bike_idle(V,t,k=1.0):
    """engine shake while standing"""
    V['P'].location=(.64+.004*k*math.sin(t*61),.003*k*math.sin(t*47),-.33+.006*k*math.sin(t*53))
def bike_smoke(V,t0,n=6,every=.22,seed=1):
    """exhaust puffs from the open pipe"""
    for k in range(n): puff((-.84,-.14,.39),t0+k*every,size=.07,n=3,col=M('#C8CAD0',.9,alpha=.7),rise=.3,life=.6,drift=(-.7,0,0),seed=seed+k,parent=V['P'])
def dino_steps(v,d0,T,S=4.2,duty=.62):
    """times (and which foot) at which a foot lands, for a straight walk dist=d0+v*t"""
    cyc=S/duty; out=[]; k=int(d0/cyc)-1
    while (k*cyc-d0)/v<=T:
        for s,off in ((1,0.0),(-1,.5)):
            t=((k+off)*cyc-d0)/v
            if -.05<=t<=T: out.append((t,s))
        k+=1
    return sorted(out)
def dino_dust(x0,y0,rz,v,d0,T,S=4.2,size=.75,t1=None):
    """dust puffs where the feet land. returns the landing times (for the camera thump)"""
    f=(math.sin(R(rz)),-math.cos(R(rz))); rt=(math.cos(R(rz)),math.sin(R(rz))); dm=M('#B9B2A4',.95,alpha=.5); ST=[q for q in dino_steps(v,d0,T,S) if t1 is None or q[0]<t1]
    for i,(t,s) in enumerate(ST):
        d=v*t; px=x0+f[0]*(d+S/2+.9)+rt[0]*s*1.3; py=y0+f[1]*(d+S/2+.9)+rt[1]*s*1.3
        puff((px,py,.25),max(0,t),size=size,n=8,col=dm,rise=.45,life=.9,seed=40+i)
    return [t for t,_ in ST]
def thump(t,times,amp=.028):
    return sum(amp*math.exp(-(t-ti)*8)*math.sin((t-ti)*36) for ti in times if t>=ti)
