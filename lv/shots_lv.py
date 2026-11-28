# Lahore vampire prince vs rishta aunties: shots. Rig note: brow_r POSITIVE = angry slant, NEGATIVE = worried slant.
SEQ=[('TOWN', 0.0), ('EXCEPT', 3.0), ('NIGHT', 4.7), ('PRINCE', 6.2), ('OLD350', 8.8), ('NEVER', 10.867), ('PICKED', 12.567), ('RULE', 14.467), ('NOKNOCK', 17.567), ('AAO', 19.2), ('FANGS', 21.433), ('KHOON', 23.7), ('LOOKUP', 25.967), ('GORA', 28.2), ('VIAH', 31.367), ('SOFA', 33.7), ('BHAAG', 37.067), ('TOOLATE', 39.6), ('QA1', 42.467), ('HAAYE', 44.567), ('KUNWARA', 46.633), ('GHARQ', 47.767), ('QA3', 50.467), ('SHIFT', 52.833), ('PHONE', 54.633), ('TRAVELS', 55.5), ('FOURMIN', 57.867), ('ELEVEN', 59.0), ('NIECE', 60.767), ('PHOTOS', 62.2), ('DOCTOR', 63.767), ('CANADA', 65.433), ('ANYV', 67.167), ('BAT', 69.2), ('FLEW', 70.6), ('NOHELP', 72.133), ('WALLS', 73.433), ('EVERY', 74.867), ('NORUN', 76.767), ('RANAT', 78.133), ('OYE', 79.567), ('SELFIE', 81.2), ('NOPHOTO', 82.367), ('CALLED', 83.5), ('MOTHER', 86.867), ('LANDED', 87.867), ('STORM', 89.867), ('NOMOVE', 90.933), ('STARE', 92.767), ('STARE2', 94.367), ('SPOKE', 95.633), ('LARKI', 97.467), ('WAITING', 99.267), ('THIS', 100.5), ('RAN', 102.2), ('TRANS', 103.367), ('LAW', 105.867), ('NEVERFLY', 109.2), ('SAFE', 111.4), ('LOCKED', 113.633), ('PHOFF', 114.567), ('BUT', 115.533), ('NOINV', 116.933), ('PUTTAR', 118.7), ('MITHAI', 120.333), ('SURVIVE', 121.7)]
END=125.0
WI={'TOWN': 0, 'EXCEPT': 8, 'NIGHT': 10, 'PRINCE': 14, 'OLD350': 21, 'NEVER': 27, 'PICKED': 33, 'RULE': 41, 'NOKNOCK': 50, 'AAO': 54, 'FANGS': 59, 'KHOON': 64, 'LOOKUP': 70, 'GORA': 77, 'VIAH': 83, 'SOFA': 88, 'BHAAG': 100, 'TOOLATE': 107, 'QA1': 116, 'HAAYE': 121, 'KUNWARA': 126, 'GHARQ': 130, 'QA3': 136, 'SHIFT': 140, 'PHONE': 144, 'TRAVELS': 146, 'FOURMIN': 151, 'ELEVEN': 154, 'NIECE': 160, 'PHOTOS': 165, 'DOCTOR': 169, 'CANADA': 173, 'ANYV': 178, 'BAT': 185, 'FLEW': 190, 'NOHELP': 195, 'WALLS': 199, 'EVERY': 204, 'NORUN': 209, 'RANAT': 213, 'OYE': 217, 'SELFIE': 221, 'NOPHOTO': 225, 'CALLED': 229, 'MOTHER': 238, 'LANDED': 240, 'STORM': 246, 'NOMOVE': 249, 'STARE': 254, 'STARE2': 258, 'SPOKE': 260, 'LARKI': 264, 'WAITING': 268, 'THIS': 271, 'RAN': 277, 'TRANS': 280, 'LAW': 286, 'NEVERFLY': 294, 'SAFE': 298, 'LOCKED': 305, 'PHOFF': 307, 'BUT': 309, 'NOINV': 313, 'PUTTAR': 318, 'MITHAI': 322, 'SURVIVE': 327}
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
def call(H,s=1,k=1.0,dz=-.5):
    """phone to the cheek with a rigid arm (it has to cross the chest); dz lowers the hand so the mouth stays visible"""
    u=H['u']; arm_to(H,s,H['head'].matrix_world@Vector((s*.85*u,-.25*u,dz*u)),k,base=(0,0,0))
def runp(H,t,x0,y0,rz,v=6.0,ph=0.0):
    """run in a straight line from (x0,y0) heading rz"""
    f=fwd(rz); d=v*t; H['root'].location[0]=x0+f[0]*d; H['root'].location[1]=y0+f[1]*d; H['root'].rotation_euler[2]=R(rz); run(H,d+ph,arm=50); blink(H,t)
def lamp(loc,e,col=(1,.86,.62),r=.6,shadow=False): return point(loc,e,col,r=r,shadow=shadow)
# ================================================================ helpers
def vstand(d,t,x,y,rz,flap=1.0): standp(d,t,x,y,rz); cape_flap(d,t,k=flap) if 'capeP' in d else None
def vfly(d,t,p,rz,tilt=62):
    standp(d,t,p[0],p[1],rz); d['root'].location=p; d['root'].rotation_euler=(R(tilt),0,R(rz)); d['head'].rotation_euler=(R(-tilt*.8),0,0)
    for s in (1,-1): d['arm'][s].rotation_euler=(R(-162),0,R(s*10)); d['leg'][s].rotation_euler=(R(5*math.sin(t*5+s)),0,0)
    cape_flap(d,t,a=3,amp=8,w=10)
def claws(d,t,k=1.0):
    for s in (1,-1): d['arm'][s].rotation_euler=(R(-118*k+3*math.sin(t*9+s)),0,R(s*30*k))
def bats(n,seed=1): return [bat(s=1.25) for k in range(n)]
def bats_fly(BT,t,p0,v,spread=3.0,seed=1):
    r=random.Random(seed)
    for k,b in enumerate(BT):
        o=(r.uniform(-spread,spread),r.uniform(-spread,spread),r.uniform(-spread*.5,spread*.5)); ph=r.uniform(0,6)
        bat_fly(b,t,(p0[0]+o[0]+v[0]*t+.4*math.sin(t*3+ph),p0[1]+o[1]+v[1]*t,p0[2]+o[2]+v[2]*t+.35*math.sin(t*4+ph)),rz=math.degrees(math.atan2(v[0],-v[1])),ph=ph)
def umbrella():
    e=empty((0,0,-40)); ocyl((0,0,.75),.02,1.5,M('#3A2A1E',.6),e,rot=(0,0,0),seg=6); ocyl((0,0,1.5),1.25,.34,M('#16171C',.8,kind='fabric'),e,rot=(0,0,0),seg=10,r2=.06); return e
def lightpane(x=6.0,y=8.9,z=4.6,hx=1.14,hz=1.04,e=3.2): return obox((x,y,z),(hx,.012,hz),M('#FFD890',.4,emit=e),0)
PS=(1.2,-.7,-35); AS=(-1.3,-.9,48)        # standing marks in the drawing room: prince, aunty (x,y,rz)
def pstand(d,t,x,y,rz,flap=1.0):
    standp(d,t,x,y,rz)
    if 'capeP' in d: cape_flap(d,t,k=flap)
def room(w4=False):
    """drawing room with Khala, the prince and Waleed (in his armchair, on his phone)"""
    W4[0]=w4; baithak(); FILLE[0]=26; a=mk(KHALA,AS[0],AS[1],AS[2],'khala'); d=prince(PS[0],PS[1],PS[2]); w=mk(WALEED,CHW[0],CHW[1],CHW[2],'waleed'); w['home']=CHW; phone_of(w,1); d['home']=MD; a['home']=CHA
    return a,d,w
def wsit(w,t,look=0.0):
    sitp(w,t,seat=.5); phone_up(w,1,1,h=3.0,fw=1.2,sx=.25); w['head'].rotation_euler[0]=R(24*(1-look)); w['arm'][-1].rotation_euler=(R(-38),0,R(-6)); fc(w,'bored'); blink(w,t)
def psit(d,t):
    sitp(d,t,seat=.53); P=d['capeP']; P[0].rotation_euler[0]=R(4+1.5*math.sin(t*2)); P[1].rotation_euler[0]=R(6); P[2].rotation_euler[0]=R(62)
    for s in (1,-1): d['arm'][s].rotation_euler=(R(-42),0,R(s*4))
def asit(a,t):
    sitp(a,t,seat=.5); a['arm'][-1].rotation_euler=(R(-40),0,R(-4)); a['arm'][1].rotation_euler=(R(-40),0,R(4))
def book(H,s=-1): return in_hand(H,s,lambda e:(obox((0,-.16,.02),(.16,.2,.025),M('#2B58C9',.6),.01,e),obox((0,-.16,.048),(.15,.19,.004),M('#F4F1EA',.7),0,e)))
# ================================================================ hook
TW=[TOWN1,TOWN2,TOWN3,dict(TOWN1,top='#C8372D',hair='#2A1B14',scarf='#F4F1EA',skin='#D9B090',pants='#3A3D47',stripe='#F4F1EA'),dict(TOWN2,top='#D8B45A',hair='#7A3A1A',pants='#27365A',skin='#EAC8A8'),dict(TOWN3,top='#3A5A4A',waistcoat='#1E2A22',hair='#B8B8C0',beard='#B8B8C0',skin='#E0B898')]
def s_TOWN():
    plaza(); FILLE[0]=95; d=prince(0,2,0); BT=bats(7); T=[mk(c,0,0,0,'t%d'%i) for i,c in enumerate(TW)]; lp=lamp((0,0,0),420,(1,.3,.3))
    R0=[(-1.0,-3.1,4.0),(1.0,-3.5,4.1),(0,-1.3,3.9),(-2.2,.4,4.2),(2.3,0,4.1),(3.4,2.6,4.3)]; lp2=lamp((0,0,0),300,(1,.85,.6),r=1)
    def upd(t):
        cy=-6.5-4.0*t; p=(.25*math.sin(t*2.2),2.2-4.5*t,3.5-.6*ease(t/1.2)+.12*math.sin(t*5)); vfly(d,t,p,0); fc(d,'shout'); face(d,brow_r=14); lp.location=(p[0],p[1]-1.6,p[2]-.6)
        for j,b in enumerate(BT): a=t*3.0+j*.9; bat_fly(b,t,(p[0]+2.6*math.cos(a),p[1]+1.2+1.0*math.sin(a),p[2]+1.0+.5*math.sin(t*3+j)),rz=0,ph=j)
        for j,(H,(x,y,v)) in enumerate(zip(T,R0)): runp(H,t,x,y,0,v,ph=j*.37); fc(H,'scream'); arms_up(H,1,t,spread=24,jig=14)
        lp2.location=(0,cy+3.4,3.0); camset((.15*math.sin(t*1.7),cy,1.0),(0,cy+5.0,2.0),20,8)
    return dict(upd=upd)
SHOTS['TOWN']=s_TOWN
def s_EXCEPT():
    gali(); FILLE[0]=110; w=mk(WALEED,-12.0,-.2,0,'waleed'); cu=cup_of(w,1); d=prince(-10.7,2.2,8); b=mk(BOYB,-14.7,.8,-24,'boyb'); cb=cup_of(b,1); lamp((-11.5,-2.6,2.4),150,(1,.85,.6))
    def upd(t):
        standp(w,t,-12.0,-.2,0); hold_chai(w,cu,1,sip=.95*ease((t-.4)/.3)); fc(w,'bored'); blink(w,t); w['arm'][-1].rotation_euler=(0,0,0)
        pstand(d,t,-10.7,2.2,8,flap=2); claws(d,t,ease(t/.2)); fc(d,'shout'); face(d,brow_r=14); d['root'].location[2]=.05*abs(math.sin(t*12))
        standp(b,t,-14.7,.8,-24); hold_chai(b,cb,1,sip=.5); fc(b,'bored'); look_at(b,headw(d),.6)
        cam2(t,(-11.75,-3.0,1.75),(-11.75,-2.85,1.75),(-11.45,1.0,1.6),28)
    return dict(upd=upd)
SHOTS['EXCEPT']=s_EXCEPT
# ================================================================ the prince arrives
def s_NIGHT():
    gali(stall=False); FILLE[0]=20; BT=bats(5)
    def upd(t):
        bats_fly(BT,t,(20,0,12),(-6,0,-1.2),spread=2.2); cam2(t,(-22,-.4,1.9),(-19.5,-.4,2.1),(40,0,10.5),22)
    return dict(upd=upd)
SHOTS['NIGHT']=s_NIGHT
def s_PRINCE():
    gali(); FILLE[0]=120; d=prince(6.0,0,-90); BT=bats(6); lamp((3.2,-1.6,1.4),200,(.6,.7,1.0)); lamp((7.6,1.5,3.6),220,(1,.3,.35)); puff((6,0,.2),.62,size=.3,n=8,col=M('#C8B8A8',.9,alpha=.5),rise=.3,life=.9,seed=2)
    def upd(t):
        k=ease(t/.65); pstand(d,t,6.0,0,-90,flap=2.6-1.6*k); d['root'].location[2]=7.0*(1-k)**2; c=ease((t-.62)/.15)*(1-ease((t-.85)/.35)); d['root'].rotation_euler[0]=R(14*c)
        for s in (1,-1): d['arm'][s].rotation_euler=(R(-20-60*(1-k)),0,R(s*(18+50*(1-k))))
        fc(d,'smug'); bats_fly(BT,t,(8,0,6.5),(-1.5,0,-.4),spread=1.8); cam2(t,(1.9,-1.5,.9),(2.3,-1.3,1.0),(6.0,0,2.2),26)
    return dict(upd=upd)
SHOTS['PRINCE']=s_PRINCE
def s_OLD350():
    gali(); FILLE[0]=55; d=prince(6.0,0,-90); lamp((3.6,-1.4,2.6),110,(.6,.7,1.0)); lamp((7.6,1.5,3.6),220,(1,.3,.35))
    def upd(t):
        pstand(d,t,6.0,0,-90,flap=.6); fc(d,'smug'); blink(d,t); d['head'].rotation_euler[1]=R(5*ease(t/DUR)); c1(t,d,yaw=16,dist=2.5,lens=44,ref=-90)
    return dict(upd=upd)
SHOTS['OLD350']=s_OLD350
def s_NEVER():
    gali(); FILLE[0]=70; d=prince(6.0,0,-90); BT=bats(6); lamp((3.6,-1.2,1.0),170,(.6,.7,1.0)); lamp((7.8,1.4,3.8),240,(1,.3,.35))
    def upd(t):
        k=ease(t/.3); pstand(d,t,6.0,0,-90,flap=2.2); fc(d,'smug'); d['head'].rotation_euler[0]=R(-8*k)
        for s in (1,-1): d['arm'][s].rotation_euler=(R(-96*k+3*math.sin(t*5+s)),0,R(s*62*k))
        for j,b in enumerate(BT): a=t*2.8+j*1.05; bat_fly(b,t,(6+2.4*math.cos(a),1.5*math.sin(a),4.0+.3*math.sin(t*3+j)),rz=math.degrees(a)+180,ph=j)
        cam2(t,(2.2,-.9,.5),(2.7,-.8,.55),(6.0,0,2.35),24)
    return dict(upd=upd)
SHOTS['NEVER']=s_NEVER
def s_PICKED():
    gali(); FILLE[0]=36; d=prince(0,-1.0,180); lamp((1.6,1.6,2.6),50,(1,.8,.55))
    def upd(t):
        pstand(d,t,0,-1.0,180,flap=.8); k=ease((t-.25)/.3); pointw(d,1,(-1.8,3.2,5.4),k); fc(d,'smug'); face(d,eyes=.8); d['head'].rotation_euler[0]=R(-8*k)
        c1(t,d,yaw=-24,dist=3.0,lens=34,ref=180,tz=-.25,dz=-.35)
    return dict(upd=upd)
SHOTS['PICKED']=s_PICKED
def s_RULE():
    G=gali(); FILLE[0]=14; d=prince(0,-1.6,180)
    def upd(t):
        walk_path(d,[(0,-2.2),(0,.8)],t,-.1,we(45)+.1,step=.6,arm=22); cape_flap(d,t,k=1.2); k=ease((t-we(46))/.3); fc(d,'smug'); blink(d,t)
        if k>0: arm_to(d,1,(-.55,2.9,2.05+.05*math.sin(t*3)),k,base=(0,0,0))
        h=headw(d); camset((.08,3.05,1.9),(h.x*.5,h.y,h.z-.12),28,8)
    return dict(upd=upd)
SHOTS['RULE']=s_RULE
def s_NOKNOCK():
    G=gali(); FILLE[0]=60; d=prince(0,1.55,180); a=mk(KHALA,0,4.7,0,'khala',z=.33)
    def upd(t):
        k=ease((t-.15)/.22); door_open(G,k); pstand(d,t,0,1.55,180,flap=.6); arm_to(d,1,(-.3,3.05,2.35),1,base=(0,0,0)); fc(d,'shock' if k>.3 else 'smug'); d['root'].rotation_euler[0]=R(-7*ease((t-.3)/.2))
        y=4.7-.9*ease((t-.35)/.4); standp(a,t,0,y,0); a['root'].location[2]=.33; fc(a,'happy'); arms_up(a,ease((t-.5)/.25),t,spread=26,jig=0)
        cam2(t,(-2.5,-.7,1.9),(-2.3,-.5,1.9),(.15,3.2,1.9),26)
    return dict(upd=upd)
SHOTS['NOKNOCK']=s_NOKNOCK
def s_AAO():
    G=gali(); FILLE[0]=30; a=mk(KHALA,0,3.8,0,'khala',z=.33); lamp((.6,1.6,2.6),40,(1,.85,.6))
    def upd(t):
        door_open(G,1); standp(a,t,0,3.8,0); a['root'].location[2]=.33; fc(a,'happy'); speak(a,t,54,58,gesture=False)
        for s in (1,-1): a['arm'][s].rotation_euler=(R(-78+22*math.sin(t*9+s)),0,R(s*16))
        a['root'].rotation_euler[0]=R(5*math.sin(t*4.5)); cam2(t,(.4,.7,2.0),(.35,1.1,2.0),(0,3.8,1.95),32)
    return dict(upd=upd)
SHOTS['AAO']=s_AAO
# ================================================================ the drawing room
def s_FANGS():
    a,d,w=room()
    def upd(t):
        wsit(w,t); pstand(d,t,*PS,flap=1.4); k=ease((t-we(60))/.25); claws(d,t,k); fc(d,'shout' if k>.4 else 'smug'); look_at(d,headw(a),.5)
        standp(a,t,*AS); fc(a,'happy'); look_at(a,headw(d),.8); blink(a,t)
        cam2(t,(-3.1,-2.2,1.85),(-2.9,-1.9,1.8),(1.2,-.7,1.85),30)
    return dict(upd=upd)
SHOTS['FANGS']=s_FANGS
def s_KHOON():
    a,d,w=room(); lamp((2.4,-2.4,1.2),90,(1,.3,.3))
    def upd(t):
        wsit(w,t); standp(a,t,*AS); pstand(d,t,*PS,flap=1.6); claws(d,t,1); fc(d,'shout'); speak(d,t,64,69,gesture=False); face(d,brow_r=14); d['root'].rotation_euler[0]=R(6*math.sin(t*5))
        c1(t,d,yaw=22,dist=2.7,lens=38,ref=PS[2],dz=-.5,tz=.05)
    return dict(upd=upd)
SHOTS['KHOON']=s_KHOON
def s_LOOKUP():
    a,d,w=room()
    def upd(t):
        wsit(w,t); standp(a,t,*AS); a['root'].location[2]=-40; pstand(d,t,*PS,flap=.5); k=1-.6*ease(t/.5); claws(d,t,k); fc(d,'worry'); look_at(d,(AS[0],AS[1],1.9),.8)
        u=ease(t/(we(74)+.05)); dn=ease((t-we(75)+.1)/.45); z=.35+2.25*u-1.5*dn; camset((AS[0]+.3,AS[1]-.2,1.75),(PS[0],PS[1],z),40,8)
    return dict(upd=upd)
SHOTS['LOOKUP']=s_LOOKUP
def s_GORA():
    a,d,w=room()
    def upd(t):
        wsit(w,t); pstand(d,t,*PS,flap=.5); claws(d,t,.25); fc(d,'worry'); look_at(d,headw(a),.7); blink(d,t)
        standp(a,t,*AS); fc(a,'smug'); speak(a,t,77,82,gesture=False); look_at(a,headw(d),.8)
        k1=ease((t-ws(77)+.1)/.2)*(1-ease((t-we(78))/.2)); k2=ease((t-ws(79)+.1)/.2)*(1-ease((t-we(79)-.1)/.2)); k3=ease((t-ws(80)+.1)/.2)
        a['arm'][1].rotation_euler=(R(-70*k1-150*k2-62*k3),0,R(10+8*k3*math.sin(t*8))); a['arm'][-1].rotation_euler=(R(-30*k3),0,R(-8))
        c1(t,a,yaw=-14,dist=2.9,lens=36,ref=AS[2],tz=-.3)
    return dict(upd=upd)
SHOTS['GORA']=s_GORA
def s_VIAH():
    a,d,w=room()
    def upd(t):
        wsit(w,t); pstand(d,t,*PS,flap=.4); q=ease((t-we(86)+.02)/.22); d['root'].rotation_euler[0]=R(-7*q); fc(d,'worry' if q<.5 else 'shock'); speak(d,t,87,87,gesture=False); look_at(d,headw(a),.7)
        standp(a,t,*AS); k=ease(t/.4); a['root'].rotation_euler[0]=R(9*k); fc(a,'smug'); speak(a,t,83,86,gesture=False); look_at(a,headw(d),.45); a['arm'][1].rotation_euler=(R(-64*k),0,R(22))
        ha=headw(a); hd=headw(d); tg=LV((ha.x,ha.y,ha.z-.2),(hd.x,hd.y,hd.z-.2),q); camset((.75,-3.1,1.8),tg,46,8)
    return dict(upd=upd)
SHOTS['VIAH']=s_VIAH
def s_SOFA():
    a,d,w=room()
    def upd(t):
        wsit(w,t); standp(a,t,*AS); pstand(d,t,*PS,flap=.4); c1(t,w,yaw=-24,dist=3.0,lens=36,ref=CHW[2],push=.16,tz=-.3)
    return dict(upd=upd)
SHOTS['SOFA']=s_SOFA
def s_BHAAG():
    a,d,w=room()
    def upd(t):
        k=ease((t-ws(103)+.1)/.25)*(1-ease((t-we(106)-.1)/.3)); wsit(w,t,look=k); speak(w,t,100,106,gesture=False); w['head'].rotation_euler[2]=R(-28*k)
        standp(a,t,*AS); pstand(d,t,*PS,flap=.4); c1(t,w,yaw=-10,dist=2.2,lens=42,ref=CHW[2],tz=-.25)
    return dict(upd=upd)
SHOTS['BHAAG']=s_BHAAG
def s_TOOLATE():
    a,d,w=room(); bk=book(a,-1); sp=spotd((MD[0],MD[1]-.6,4.2),0,(1,.95,.8),size=42,blend=.5)
    def upd(t):
        wsit(w,t); psit(d,t); fc(d,'worry'); blink(d,t); d['head'].rotation_euler[0]=R(6); d['head'].rotation_euler[2]=R(22*math.sin(t*2.4)*(1-ease((t-we(111))/.2)))
        asit(a,t); fc(a,'firm'); k=ease((t-.5)/.4); a['arm'][-1].rotation_euler=(R(-40-22*k),0,R(-4)); a['arm'][1].rotation_euler=(R(-40-30*k),0,R(18*k)); look_at(a,headw(d),.9)
        on=ease((t-we(111))/.12); sp.data.energy=1500*on; FILLE[0]=26-14*on
        cam2(t,(2.0,-3.3,2.7),(1.8,-2.9,2.4),(1.2,.8,1.1),30)
    return dict(upd=upd)
SHOTS['TOOLATE']=s_TOOLATE
def qa(spot=True,w4=False):
    a,d,w=room(w4); bk=book(a,-1); sp=spotd((MD[0],MD[1]-.6,4.2),1200,(1,.95,.8),size=42,blend=.5); return a,d,w
def qa_idle(a,d,w,t):
    wsit(w,t); psit(d,t); asit(a,t); a['arm'][-1].rotation_euler=(R(-48),0,R(-4)); a['arm'][1].rotation_euler=(R(-70),0,R(18)); look_at(a,headw(d),.9); look_at(d,headw(a),.7); blink(a,t); blink(d,t)
def pcam(t,d,lens=40): c1(t,d,yaw=-16,dist=2.7,lens=lens,ref=0,tz=-.2)
def acam(t,a,lens=40,dist=2.6): c1(t,a,yaw=-30,dist=dist,lens=lens,ref=CHA[2],tz=-.2)
def s_QA1():
    a,d,w=qa()
    def upd(t):
        qa_idle(a,d,w,t); fc(d,'worry'); speak(d,t,117,120,gesture=False); d['head'].rotation_euler[0]=R(8*ease((t-ws(117))/.3)); pcam(t,d)
    return dict(upd=upd)
SHOTS['QA1']=s_QA1
def s_HAAYE():
    a,d,w=qa()
    def upd(t):
        qa_idle(a,d,w,t); fc(a,'shock'); speak(a,t,121,125,gesture=False); k=ease(t/.15); headtouch(a,1,k,dx=.9,dy=-.3,dz=.35); a['root'].rotation_euler[0]=R(-5*k); acam(t,a)
    return dict(upd=upd)
SHOTS['HAAYE']=s_HAAYE
def s_KUNWARA():
    a,d,w=qa()
    def upd(t):
        qa_idle(a,d,w,t); fc(d,'sad'); d['head'].rotation_euler[0]=R(16*ease(t/.4)); pcam(t,d,46)
    return dict(upd=upd)
SHOTS['KUNWARA']=s_KUNWARA
def s_GHARQ():
    a,d,w=qa(); fl=lamp((CHA[0]+1.2,CHA[1]-.6,2.0),0,(1,.85,.4))
    def upd(t):
        qa_idle(a,d,w,t); q=ease((t-ws(135)+.06)/.14); fc(a,'firm' if t<ws(133) else ('wow' if q<.5 else 'happy')); speak(a,t,130,132,gesture=False); speak(a,t,135,135,gesture=False)
        if q>0: a['root'].location[2]+=.3*q*abs(math.sin((t-ws(135))*9)); arms_up(a,q,t,spread=30,jig=10)
        fl.data.energy=260*q; c1(t,a,yaw=-30,dist=2.6*(1-.22*q),lens=40,ref=CHA[2],tz=-.2,push=0)
    return dict(upd=upd)
SHOTS['GHARQ']=s_GHARQ
def s_QA3():
    a,d,w=qa()
    def upd(t):
        qa_idle(a,d,w,t); fc(d,'worry'); speak(d,t,137,139,gesture=False); d['head'].rotation_euler[2]=R(14*math.sin(t*2.2)); pcam(t,d,42)
    return dict(upd=upd)
SHOTS['QA3']=s_QA3
def s_SHIFT():
    a,d,w=qa()
    def upd(t):
        qa_idle(a,d,w,t); fc(a,'smug'); speak(a,t,140,143,gesture=False); a['head'].rotation_euler[0]=R(16+6*math.sin(t*7)); a['arm'][1].rotation_euler=(R(-72+4*math.sin(t*14)),0,R(20+5*math.sin(t*14))); acam(t,a,44,2.4)
    return dict(upd=upd)
SHOTS['SHIFT']=s_SHIFT
# ================================================================ the aunty network
RING=[(-.35,-.75,137),(1.2,-1.55,180),(2.75,-.75,-137)]      # three aunties round the mooda (x,y,rz facing the prince)
def s_PHONE():
    a,d,w=qa(); phone_of(a,1)
    def upd(t):
        qa_idle(a,d,w,t); fc(a,'smug'); phone_up(a,1,1,h=3.1,fw=1.15,sx=.2); a['head'].rotation_euler[0]=R(22); a['arm'][-1].rotation_euler=(R(-70+6*math.sin(t*20)),0,R(-26)); c1(t,a,yaw=-30,dist=2.4,lens=44,ref=CHA[2],tz=-.42)
    return dict(upd=upd)
SHOTS['PHONE']=s_PHONE
def s_TRAVELS():
    gali(stall=False); FILLE[0]=10; P=[(obox((jx,y,z),(jw,.014,.64),M('#FFD27A',.4,emit=5.5),0),jx) for (jx,y,z,jw,side,on) in JH if (not on) and -8<jx<62]
    def upd(t):
        for o,x in P: o.scale=(1,1,1) if t>.3+max(0,x)*.03 else (0,0,0)
        cam2(t,(-5,-.6,8.6),(-2,-.6,8.2),(34,0,4.4),22)
    return dict(upd=upd)
SHOTS['TRAVELS']=s_TRAVELS
AC=[AUN2,AUN3,AUN4,AUN5,AUN6,AUN7]
def s_FOURMIN():
    G=gali(); FILLE[0]=60; A=[mk(c,0,0,0,'a%d'%i) for i,c in enumerate(AC)]; lamp((0,0,8),900,(1,.85,.6),r=2)
    PA=[[(-8,-1.6),(-2.6,-1.2)],[(-6.5,1.0),(-1.9,.6)],[(-10.5,.2),(-4.4,.3)],[(8,-1.4),(2.6,-1.2)],[(6.5,1.2),(1.9,.6)],[(10.5,0),(4.4,.3)]]
    def upd(t):
        for H,p in zip(A,PA): walk_path(H,p,t,-2.2,DUR+.2,step=.6,arm=30); fc(H,'firm')
        cam2(t,(0,-1.9,7.6),(0,-1.9,6.9),(0,1.2,.9),18)
    return dict(upd=upd)
SHOTS['FOURMIN']=s_FOURMIN
def s_ELEVEN():
    G=gali(); FILLE[0]=110; A=[mk(c,0,0,-90,'a%d'%i) for i,c in enumerate(AC)]; F=[(0,0),(2.4,-1.9),(2.4,1.9),(4.8,-.95),(4.8,.95),(7.2,0)]; lamp((-3,0,3.2),300,(1,.85,.6))
    def upd(t):
        for i,(H,(dx,y)) in enumerate(zip(A,F)): standp(H,t,1.4+dx-1.15*t,y,-90); walk(H,1.15*t+i*.37,step=.55,arm=24); fc(H,'firm'); H['head'].rotation_euler[0]=R(-4)
        cam2(t,(-4.2,.3,.8),(-4.5,.3,.85),(2.4,0,1.9),30)
    return dict(upd=upd)
SHOTS['ELEVEN']=s_ELEVEN
def ring(w4=False):
    a,d,w=qa(w4=w4); lamp((1.2,.9,2.1),150 if w4 else 0,(1,.9,.75),r=.8); A=[mk(c,x,y,rz,'r%d'%i) for i,(c,(x,y,rz)) in enumerate(zip((AUN2,AUN3,AUN4),RING))]; P=[photo(H,1,col) for H,col in zip(A,('#8FB8D8','#F2C14E','#B89AE0'))]; return a,d,w,A
def ring_idle(a,d,w,A,t,k=1.0,hide=()):
    qa_idle(a,d,w,t); fc(d,'scream' if k>.5 else 'worry'); d['head'].rotation_euler[0]=R(-6)
    for i,(H,(x,y,rz)) in enumerate(zip(A,RING)):
        standp(H,t,x,y,rz); fc(H,'happy'); H['root'].rotation_euler[0]=R(8*k)
        tg=headw(d); arm_to(H,1,(tg.x,tg.y,tg.z-.25+.08*math.sin(t*9+i)),k,base=(0,0,0))
        if i in hide: H['root'].location[2]=-40
def s_NIECE():
    a,d,w,A=ring()
    def upd(t):
        ring_idle(a,d,w,A,t,ease(t/.3)); cam2(t,(1.2,-4.0,3.3),(1.2,-3.7,3.15),(1.2,.1,1.2),18)
    return dict(upd=upd)
SHOTS['NIECE']=s_NIECE
def s_PHOTOS():
    a,d,w,A=ring(True); PP=[(.3,-2.1,163),(1.2,-9,180),(2.1,-2.1,-163)]
    def upd(t):
        ring_idle(a,d,w,A,t,1); d['root'].location[2]=-40; cp=Vector((1.2,.75,1.52))
        for i,(H,(x,y,rz)) in enumerate(zip(A,PP)):
            standp(H,t,x,y,rz); H['root'].rotation_euler[0]=R(8); fc(H,'laugh' if i else 'happy'); j=.07*math.sin(t*10+i*2)
            arm_to(H,1,(cp.x+(-.3 if i==0 else .3),cp.y,cp.z+.1+j),1,base=(0,0,0)); look_at(H,tuple(cp),.9)
        camset((cp.x+.03*math.sin(t*5),cp.y,cp.z+.02*math.sin(t*7)),(1.2,-2.1,1.6),20,8)
    return dict(upd=upd)
SHOTS['PHOTOS']=s_PHOTOS
def s_DOCTOR():
    a,d,w,A=ring(True)
    def upd(t):
        ring_idle(a,d,w,A,t,1); d['root'].location[2]=-40; speak(A[0],t,169,172,gesture=False); c1(t,A[0],yaw=18,dist=2.0,lens=34,ref=RING[0][2],tz=-.3)
    return dict(upd=upd)
SHOTS['DOCTOR']=s_DOCTOR
def s_CANADA():
    a,d,w,A=ring(True)
    def upd(t):
        ring_idle(a,d,w,A,t,1); d['root'].location[2]=-40; speak(A[2],t,173,177,gesture=False); c1(t,A[2],yaw=-18,dist=2.0,lens=34,ref=RING[2][2],tz=-.3)
    return dict(upd=upd)
SHOTS['CANADA']=s_CANADA
# ================================================================ the escape
def s_ANYV():
    a,d,w,A=ring()
    def upd(t):
        ring_idle(a,d,w,A,t,1,hide=(1,)); k=ease(t/.3); standp(d,t,MD[0],MD[1],0); d['root'].location[2]=.53*k; cape_flap(d,t,k=1.5); crossed(d,ease((t-.5)/.3)); fc(d,'firm'); face(d,brow_r=10)
        s=ease((t-DUR+.5)/.5); d['root'].rotation_euler[2]=R(720*s*s)
        cam2(t,(1.5,-2.6,1.0),(1.4,-2.3,1.05),(1.2,.9,2.25),30)
    return dict(upd=upd)
SHOTS['ANYV']=s_ANYV
def s_BAT():
    a,d,w,A=ring(); b=pbat(); pm=M('#8A6AC8',.9,alpha=.6); [puff((MD[0]+dx,MD[1]-.1,1.0+dz),.02,size=.5,n=9,col=pm,rise=.5,life=1.0,seed=q) for q,(dx,dz) in enumerate(((0,0),(.35,.5),(-.35,.9),(0,1.4),(.2,1.9)))]; lamp((1.2,-.8,1.6),90,(.7,.5,1.0))
    def upd(t):
        ring_idle(a,d,w,A,t,1,hide=(1,)); d['root'].location[2]=.53 if t<.1 else -40; crossed(d,1)
        q=ease((t-.12)/(DUR-.12)); P=[(MD[0],MD[1],1.5),(1.1,-.3,2.5),(.2,-1.5,3.3)]; i=min(1,int(q*2)); f=q*2-i; p=LV(P[i],P[i+1],f); bat_fly(b,t,p if t>.1 else (0,0,-50),rz=0,ph=0)
        cam2(t,(1.25,-2.0,.9),(1.25,-1.8,.95),(1.2,.9,1.75),24)
    return dict(upd=upd)
SHOTS['BAT']=s_BAT
def s_FLEW():
    gali(); FILLE[0]=40; b=pbat(); lp=lamp((0,0,0),500,(.7,.8,1.0))
    def upd(t):
        q=t/DUR; P=[(0,2.1,4.8),(-3.5,.2,5.5),(-8,-.3,4.6),(-13,0,4.0)]; i=min(2,int(q*3)); f=q*3-i; p=LV(P[i],P[i+1],f); bat_fly(b,t,p,rz=90,ph=0); lp.location=(p[0]-1,p[1]-1,p[2]+1.5)
        cam2(t,(-10.5,-1.6,2.6),(-10.5,-1.6,2.6),(p[0],p[1],p[2]),30)
    return dict(upd=upd)
SHOTS['FLEW']=s_FLEW
RP=(.1,6.4,-90)            # the prince's mark on the hero roof
def s_NOHELP():
    gali(); FILLE[0]=40; d=prince(RP[0],RP[1],RP[2],z=RZ); pm=M('#8A6AC8',.9,alpha=.55); [puff((RP[0],RP[1],RZ+1.0+q*.6),.02,size=.3,n=6,col=pm,rise=.4,life=.7,seed=q) for q in range(3)]; lamp((-1.8,5.4,RZ+2.6),110,(.62,.72,1.0)); lamp((1.4,7.6,RZ+2.4),70,(1,.82,.55))
    def upd(t):
        k=ease((t-.15)/.2); r_=ease((t-.8)/.3); e=ease((t-DUR+.55)/.15); pstand(d,t,*RP,flap=1.2); d['root'].location[2]=RZ if t>.12 else -40; d['root'].rotation_euler[0]=R(16*k*(1-r_)); fc(d,'worry' if t<.8 else ('happy' if e<.5 else 'shock'))
        for s in (1,-1): d['arm'][s].rotation_euler=(R(-34*k*(1-r_)),0,R(s*6))
        d['head'].rotation_euler[2]=R(-38*e); c1(t,d,yaw=-14,dist=2.7,lens=38,ref=-90,tz=-.25)
    return dict(upd=upd)
SHOTS['NOHELP']=s_NOHELP
def s_WALLS():
    gali(); FILLE[0]=22; lamp((2.0,6.3,RZ+2.2),45,(1,.86,.6))
    def upd(t): cam2(t,(2.0,4.0,RZ+1.35),(2.0,4.3,RZ+1.3),(2.0,7.89,RZ+.95),36)
    return dict(upd=upd)
SHOTS['WALLS']=s_WALLS
def s_EVERY():
    gali(posters=True); FILLE[0]=60; b=mk(BOYC,-3.4,2.75,180,'boyc',z=.32); br=in_hand(b,1,lambda e:(obox((0,0,-.2),(.02,.02,.2),M('#8A6238',.6),.005,e),obox((0,0,-.44),(.1,.03,.06),M('#F4F1EA',.7),.01,e)))
    lamp((-6,1.4,3.0),170,(1,.85,.6)); lamp((-2,1.4,3.0),170,(1,.85,.6)); lamp((3,1.4,3.0),150,(1,.85,.6))
    def upd(t):
        standp(b,t,-3.4,2.75,180); b['root'].location[2]=.32; b['arm'][1].rotation_euler=(R(-128+22*math.sin(t*6)),0,R(8)); b['arm'][-1].rotation_euler=(R(-60),0,R(-10)); fc(b,'happy')
        cam2(t,(-9.6,1.5,1.75),(-8.0,1.4,1.75),(2,3.1,2.1),28)
    return dict(upd=upd)
SHOTS['EVERY']=s_EVERY
def s_NORUN():
    gali(posters=True); FILLE[0]=70; d=prince(3,0,-90); fl=lamp((.5,-.8,2.0),0,(1,1,1),r=.2); lamp((1.2,-1.5,2.4),120,(.6,.7,1.0))
    def upd(t):
        pstand(d,t,3,0,-90,flap=1.6); k=1-ease((t-.7)/.3); claws(d,t,.25+.75*k); fc(d,'shout' if k>.5 else 'worry'); fl.data.energy=1600 if (t>.45 and int(t*10)%3==0) else 0
        c1(t,d,yaw=14,dist=3.1,lens=34,ref=-90,dz=-.3)
    return dict(upd=upd)
SHOTS['NORUN']=s_NORUN
def s_RANAT():
    gali(posters=True); FILLE[0]=120; C=[(BOYA,-2.0,-1.9,4.6),(BOYC,-3.9,0,4.4),(AUN6,-2.9,1.9,4.2),(BOYB,-6.4,-1.0,4.5),(AUN7,-7.0,1.1,4.3)]; A=[mk(c,x,y,90,'c%d'%i) for i,(c,x,y,v) in enumerate(C)]; lamp((2,0,3),300,(1,.85,.6))
    def upd(t):
        for i,(H,(c,x,y,v)) in enumerate(zip(A,C)): runp(H,t,x,y,90,v,ph=i*.4); fc(H,'laugh' if i%2 else 'happy'); arms_up(H,1,t,spread=20,jig=10,only=1)
        cam2(t,(6.0,.2,1.45),(6.3,.2,1.5),(-1,0,1.8),26)
    return dict(upd=upd)
SHOTS['RANAT']=s_RANAT
def s_OYE():
    gali(posters=True); FILLE[0]=110; b=mk(BOYA,0,0,90,'boya')
    def upd(t):
        standp(b,t,0,0,90); fc(b,'shout'); speak(b,t,217,220,gesture=False); pointw(b,1,(4,-.4,1.9),ease(t/.15)); b['root'].location[2]=.07*abs(math.sin(t*9)); b['arm'][-1].rotation_euler=(R(-140),0,R(-20))
        c1(t,b,yaw=-12,dist=2.5,lens=38,ref=90,tz=-.25)
    return dict(upd=upd)
SHOTS['OYE']=s_OYE
def s_SELFIE():
    gali(posters=True); FILLE[0]=70; b=mk(BOYB,0,-.6,-90,'boyb'); d=prince(1.6,1.5,-90); fl=lamp((-2.2,-.9,2.3),0,(1,1,1),r=.2)
    def upd(t):
        cp=(-1.75+.02*math.sin(t*6),-1.15,2.25+.02*math.sin(t*8)); standp(b,t,0,-.6,-90); fc(b,'laugh'); arm_to(b,1,(cp[0]+.3,cp[1]-.6,cp[2]-.75),1,base=(0,0,0)); b['arm'][-1].rotation_euler=(R(-8),0,R(-6)); look_at(b,cp,.9)
        pstand(d,t,1.6,1.5,-90,flap=.4); fc(d,'dead'); look_at(d,cp,.6); fl.data.energy=420 if .5<t<.58 else 0
        camset(cp,(.9,0,1.6),20,8)
    return dict(upd=upd)
SHOTS['SELFIE']=s_SELFIE
def s_NOPHOTO():
    gali(posters=True); FILLE[0]=110; b=mk(BOYB,0,-.8,-90,'boyb'); phone_of(b,1)
    def upd(t):
        standp(b,t,0,-.8,-90); fc(b,'worry'); speak(b,t,221,228,gesture=False); phone_up(b,1,1,h=3.5,fw=1.25,sx=.3); b['head'].rotation_euler[0]=R(14); b['arm'][-1].rotation_euler=(R(-70+8*math.sin(t*8)),0,R(-50))
        c1(t,b,yaw=-18,dist=2.3,lens=40,ref=-90,tz=-.25)
    return dict(upd=upd)
SHOTS['NOPHOTO']=s_NOPHOTO
# ================================================================ his mother
def s_CALLED():
    gali(); FILLE[0]=40; d=prince(-.9,9.3,-30,z=RZ); b=pbat(1.5); lamp((-1.6,6.8,RZ+2.6),120,(.62,.72,1.0)); lamp((.6,8.2,RZ+2.2),60,(1,.82,.55)); bl=lamp((0,0,0),70,(1,.75,.5),r=.3)
    def upd(t):
        r_=ease((t-we(232))/.3); pstand(d,t,-.9,9.3,-30,flap=.5); d['root'].location[2]=RZ; fc(d,'worry'); speak(d,t,229,232,gesture=False)
        d['arm'][1].rotation_euler=(R(-78-40*r_),0,R(62)); d['arm'][-1].rotation_euler=(R(-10),0,R(-6)); d['head'].rotation_euler[2]=R(30*(1-r_)); d['head'].rotation_euler[0]=R(-24*r_)
        h=handw(d,1); p0=(h.x,h.y,h.z+.22); p=LV(p0,(-7,3,RZ+13),r_*r_) if r_>0 else p0; bat_fly(b,t,p,rz=-30,ph=0); bl.location=(p[0]-.3,p[1]-.8,p[2]+.3)
        c1(t,d,yaw=0,dist=3.4,lens=32,ref=-30,tz=-.15,sx=.35)
    return dict(upd=upd)
SHOTS['CALLED']=s_CALLED
QP=(6.0,0,-90)
def qstand(q,t,flap=1.5): standp(q,t,*QP); cape_flap(q,t,a=6,amp=7,w=5,k=flap)
def s_MOTHER():
    gali(mood='lv_storm'); FILLE[0]=8; q=queen(-9,0,90); fl=lamp((-5,-1.5,7),0,(.85,.8,1.0),r=2); BT=bats(8); mn=oico((-59.6,2.5,52.7),10.0,M('#FFF2D0',.3,emit=3.0),None,sub=3)
    def upd(t):
        z=10.2-1.6*ease(t/DUR); standp(q,t,-9,0,90); q['root'].location[2]=z; cape_flap(q,t,a=40,amp=14,w=9)
        for s in (1,-1): q['arm'][s].rotation_euler=(R(-95),0,R(s*70))
        fc(q,'firm'); fl.data.energy=26000 if (.5<t<.58 or .72<t<.76) else 0; bats_fly(BT,t,(-9,0,z-.4),(0,0,0),spread=3.2)
        cam2(t,(1.5,-.5,1.0),(1.3,-.5,1.05),(-9,0,z+.85),40)
    return dict(upd=upd)
SHOTS['MOTHER']=s_MOTHER
def s_LANDED():
    gali(mood='lv_storm'); FILLE[0]=90; q=queen(*QP); BT=bats(8); dm=M('#C8B8A8',.9,alpha=.5); lamp((4.4,1.6,5.2),420,(.75,.7,1.0)); fl=lamp((6,0,4),0,(.85,.8,1.0),r=1)
    for k in range(8): a=k*.785; puff((6+1.3*math.cos(a),1.3*math.sin(a),.25),.34,size=.36,n=5,col=dm,rise=.3,life=1.0,drift=(1.6*math.cos(a),1.6*math.sin(a),0),seed=k)
    def upd(t):
        k=ease(t/.36); qstand(q,t,flap=2.6-1.4*k); q['root'].location[2]=9*(1-k)**2; c=ease((t-.34)/.12)*(1-ease((t-.6)/.5)); q['root'].rotation_euler[0]=R(16*c); fc(q,'firm')
        for s in (1,-1): q['arm'][s].rotation_euler=(R(-30-50*(1-k)),0,R(s*(20+50*(1-k))))
        fl.data.energy=30000 if .34<t<.42 else 0; bats_fly(BT,t,(7,0,6),(-1,0,-.3),spread=2.2); sh=.06*max(0,1-abs(t-.42)/.25)*math.sin(t*90)
        cam2(t,(3.5,1.9,4.4+sh),(3.8,1.7,4.0+sh),(6.0,0,1.3),30)
    return dict(upd=upd)
SHOTS['LANDED']=s_LANDED
def s_STORM():
    gali(mood='lv_storm'); FILLE[0]=60; q=queen(*QP); lamp((3.4,-1.6,1.2),160,(.75,.7,1.0)); lamp((7.6,1.4,3.8),240,(.7,.3,1.0))
    def upd(t): qstand(q,t,2.2); fc(q,'firm'); face(q,brow_r=12); c1(t,q,yaw=14,dist=2.6,lens=40,ref=-90,dz=-.7,tz=0)
    return dict(upd=upd)
SHOTS['STORM']=s_STORM
WALL=[(KHALA,0,0),(AUN2,-2.3,-1.7),(AUN3,-2.3,1.7),(AUN4,-4.6,0),(AUN5,-6.9,-1.5)]
def awall(): return [mk(c,x,y,90,'w%d'%i) for i,(c,x,y) in enumerate(WALL)]
def awall_idle(A,t):
    for i,(H,(c,x,y)) in enumerate(zip(A,WALL)): standp(H,t,x,y,90); crossed(H,1); fc(H,'firm'); blink(H,t) if i else None
def s_NOMOVE():
    gali(mood='lv_storm'); FILLE[0]=120; A=awall(); lamp((2.5,0,3.0),260,(1,.85,.6))
    def upd(t): awall_idle(A,t); cam2(t,(4.6,.2,1.2),(4.2,.2,1.25),(-1.6,0,1.85),24)
    return dict(upd=upd)
SHOTS['NOMOVE']=s_NOMOVE
def s_STARE():
    gali(mood='lv_storm'); FILLE[0]=26; q=queen(*QP); lamp((3.6,-1.2,2.6),80,(.75,.7,1.0))
    def upd(t): qstand(q,t,1.2); fc(q,'firm'); face(q,brow_r=12,eyes=.75+.0*t); c1(t,q,yaw=4,dist=2.0,lens=55,ref=-90,tz=-.02,push=.14)
    return dict(upd=upd)
SHOTS['STARE']=s_STARE
def s_STARE2():
    gali(mood='lv_storm'); FILLE[0]=50; A=awall(); lamp((2.0,.8,2.4),120,(1,.85,.6))
    def upd(t): awall_idle(A,t); face(A[0],brow_r=10,eyes=.72); c1(t,A[0],yaw=-4,dist=2.0,lens=55,ref=90,tz=-.02,push=.14)
    return dict(upd=upd)
SHOTS['STARE2']=s_STARE2
def s_SPOKE():
    gali(mood='lv_storm'); FILLE[0]=70; q=queen(*QP); lamp((3.4,-1.6,1.2),160,(.75,.7,1.0)); lamp((7.6,1.4,3.8),240,(.7,.3,1.0))
    def upd(t):
        qstand(q,t,1.4); fc(q,'firm'); k=ease((t-.5)/.5); q['arm'][1].rotation_euler=(R(-70*k),0,R(24*k)); face(q,mouth='o' if t>DUR-.25 else 'flat'); c1(t,q,yaw=-18,dist=3.2,lens=34,ref=-90,dz=-.8,tz=-.1)
    return dict(upd=upd)
SHOTS['SPOKE']=s_SPOKE
def s_LARKI():
    gali(mood='lv_storm'); FILLE[0]=22; q=queen(*QP); lamp((3.6,-1.2,2.6),40,(1,.85,.6))
    def upd(t):
        qstand(q,t,.6); k=ease(t/.3); q['root'].rotation_euler[0]=R(10*k); fc(q,'calm'); speak(q,t,264,267,gesture=False); q['arm'][1].rotation_euler=(R(-58*k),0,R(-24*k)); c1(t,q,yaw=16,dist=2.5,lens=40,ref=-90,tz=-.2)
    return dict(upd=upd)
SHOTS['LARKI']=s_LARKI
def s_WAITING():
    gali(mood='lv_storm'); FILLE[0]=80; q=queen(*QP); sc=in_hand(q,1,lambda e:(ocyl((0,-.1,0),.045,.4,M('#8A6238',.6),e,rot=(0,R(90),0),seg=8),)); pp=obox((0,-.1,-.5),(.17,.008,.5),M('#F2E6C8',.8),0,sc); lamp((3.6,-1.2,2.6),120,(1,.85,.6))
    LN=[obox((0,-.11,-.12-.1*i),(.12,.004,.012),M('#3A2A2A',.6),0,sc) for i in range(8)]
    def upd(t):
        qstand(q,t,.6); k=ease((t-.15)/.5); hold(q,1,-64,z=8); fc(q,'happy'); pp.scale=(1,1,max(.02,k)); pp.location=(0,-.1,-.5*max(.02,k))
        for i,o in enumerate(LN): o.scale=(1,1,1) if k*1.0>.14+.1*i else (0,0,0)
        c1(t,q,yaw=20,dist=3.3,lens=32,ref=-90,tz=-.75)
    return dict(upd=upd)
SHOTS['WAITING']=s_WAITING
def s_THIS():
    gali(mood='lv_storm'); FILLE[0]=60; a=mk(KHALA,-1.0,-.3,0,'khala'); q=queen(1.0,-.3,0); lamp((0,-2.0,3.6),200,(1,.88,.7),r=1)
    def upd(t):
        for i,H in enumerate((a,q)): standp(H,t,(-1.0,1.0)[i],-.3,0); H['head'].rotation_euler[0]=R(-34); fc(H,'happy'); H['arm'][1 if i else -1].rotation_euler=(R(-165+14*math.sin(t*9+i)),0,R((1 if i else -1)*18)); H['root'].rotation_euler[0]=R(-6)
        cape_flap(q,t,k=.5); cam2(t,(0,-2.1,3.7),(0,-2.1,3.5),(0,-.3,1.55),18)
    return dict(upd=upd)
SHOTS['THIS']=s_THIS
def s_RAN():
    gali(mood='lv_storm'); FILLE[0]=70; d=prince(8,.3,-90)
    def upd(t):
        runp(d,t,8,.3,-90,5.6); cape_flap(d,t,a=50,amp=10,w=14); fc(d,'scream'); arms_up(d,1,t,spread=22,jig=12); x=8-5.6*t
        camset((x-4.2,-.5,1.3),(x,.3,1.8),28,8)
    return dict(upd=upd)
SHOTS['RAN']=s_RAN
# ================================================================ Transylvania
def gate(G,k): G['dl'].rotation_euler[2]=R(95*k); G['dr'].rotation_euler[2]=R(-95*k)
def s_TRANS():
    G=qila_ext(); FILLE[0]=20; b=pbat(2.0); lp=lamp((0,0,0),400,(.7,.8,1.0)); puff((0,5.6,.4),DUR-.3,size=.4,n=7,col=M('#E6ECF6',.9,alpha=.6),rise=.4,life=.8,seed=3)
    def upd(t):
        q=min(1,t/(DUR-.45)); p=LV((0,-15,3.4),(0,6.6,2.4),q); p=(p[0]+.5*math.sin(t*5),p[1],p[2]+.3*math.sin(t*7)); bat_fly(b,t,p if q<1 else (0,0,-50),rz=180,ph=0); lp.location=(p[0]+1,p[1]-2,p[2]+2)
        gate(G,1-ease((t-DUR+.45)/.22)); cam2(t,(1.6,-19,2.2),(1.0,-11,2.0),(0,4,4.4),24)
    return dict(upd=upd)
SHOTS['TRANS']=s_TRANS
def s_LAW():
    qila(table=True); FILLE[0]=45; e=vampx(VAMPB,0,4.3,0,'ve'); l=vampx(VAMPA,-2.3,2.6,60,'vl',out='#1A1014',inn='#C9A24A'); r=vampx(VAMPC,2.3,2.6,-60,'vr',inn='#5A1F6A'); lamp((0,1.0,4.0),420,(1,.8,.55),r=1)
    def upd(t):
        standp(e,t,0,4.3,0); standp(l,t,-2.3,2.6,60); standp(r,t,2.3,2.6,-60); [cape_flap(H,t,k=.4) for H in (e,l,r)]; fc(e,'firm'); fc(l,'worry'); fc(r,'worry'); look_at(l,headw(e),.7); look_at(r,headw(e),.7)
        k=ease((t-ws(289))/.3); e['arm'][1].rotation_euler=(R(-150*k*(1-.5*ease((t-we(293)+.2)/.15))),0,R(10)); e['head'].rotation_euler[0]=R(8)
        cam2(t,(0,-4.4,3.5),(0,-3.6,2.9),(0,2.2,1.65),22)
    return dict(upd=upd)
SHOTS['LAW']=s_LAW
def s_NEVERFLY():
    qila(table=True); FILLE[0]=12; st=empty((0,3.3,1.5)); obox((0,-.9,0),(.014,.9,.014),M('#3A2618',.6),0,st); obox((0,-1.82,0),(.03,.04,.03),M('#C9A24A',.3,metal=.8),.01,st)
    def upd(t):
        tap=max([max(0,1-abs(t-ws(i)-.06)/.09) for i in (294,295,296,297)]); st.rotation_euler=(R(-13-2.6*tap),0,R(-2)); sh=.012*tap
        cam2(t,(0,.1,3.7+sh),(0,.45,3.1+sh),(.06,1.42,1.05),40)
    return dict(upd=upd)
SHOTS['NEVERFLY']=s_NEVERFLY
def gob(H,s=1): return in_hand(H,s,lambda e:(ocyl((0,-.12,.08),.07,.14,M('#C9A24A',.3,metal=.9),e,rot=(0,0,0),seg=10,r2=.05),ocyl((0,-.12,-.04),.015,.12,M('#C9A24A',.3,metal=.9),e,rot=(0,0,0),seg=6),ocyl((0,-.12,-.1),.05,.015,M('#C9A24A',.3,metal=.9),e,rot=(0,0,0),seg=10)))
def s_SAFE():
    qila(locks=True); FILLE[0]=50; d=prince(0,5.6,0); gob(d,1); lamp((1.5,1.5,3.2),260,(1,.8,.55),r=1)
    def upd(t):
        walk_path(d,[(0,5.6),(0,2.2)],t,-.3,DUR+1.2,step=.55,arm=16); cape_flap(d,t,k=1.0); hold(d,1,-62,z=8); fc(d,'happy'); blink(d,t)
        cam2(t,(.5,-2.4,1.3),(.45,-1.8,1.4),(0,3.4,2.3),26)
    return dict(upd=upd)
SHOTS['SAFE']=s_SAFE
def s_LOCKED():
    qila(locks=True); FILLE[0]=120
    def upd(t): cam2(t,(.3,3.6,2.5),(.2,5.2,2.7),(0,8.9,2.85),30)
    return dict(upd=upd)
SHOTS['LOCKED']=s_LOCKED
def s_PHOFF():
    qila(locks=True); FILLE[0]=60; d=prince(0,2.2,0); e=in_hand(d,1,lambda e:(obox((0,-.02,-.16),(.12,.21,.012),M('#16171C',.4),.01,e),)); scr=obox((0,-.02,-.174),(.105,.19,.003),M('#BFE0FF',.3,emit=3.0),0,e)
    def upd(t):
        pstand(d,t,0,2.2,0,flap=.4); h=headw(d); arm_to(d,1,(h.x+.25,h.y-1.4,h.z-.35),1,base=(0,0,0)); fc(d,'smug'); scr.scale=(1,1,1) if t<.42 else (0,0,0); d['arm'][-1].rotation_euler=(R(-60),0,R(-30))
        c1(t,d,yaw=-10,dist=2.4,lens=38,ref=0,tz=-.3)
    return dict(upd=upd)
SHOTS['PHOFF']=s_PHOFF
def knock(G,t,T):
    j=max([max(0,1-abs(t-x)/.07) for x in T]); G['dl'].rotation_euler[2]=R(1.6*j); G['dr'].rotation_euler[2]=R(-1.6*j)
    if G.get('locks'): G['locks'].location[1]=8.84-.03*j
def s_BUT():
    G=qila(locks=True); FILLE[0]=60; d=prince(0,-.6,0); gob(d,1)
    for i,x in enumerate((.3,.56,.82)): puff((-.8+i*.8,8.7,5.6),x,size=.16,n=4,col=M('#B8B8C0',.9,alpha=.5),rise=-.5,life=.7,seed=i)
    def upd(t):
        pstand(d,t,0,-.6,0,flap=.4); k=ease((t-.3)/.12); hold(d,1,-62-30*(1-k)*0,z=8); fc(d,'happy' if k<.5 else 'shock'); d['head'].rotation_euler[2]=R(0); knock(G,t,(.3,.56,.82))
        cam2(t,(.55,-3.7,1.85),(.5,-3.5,1.85),(0,-.6,2.25),30)
    return dict(upd=upd)
SHOTS['BUT']=s_BUT
GANG=[(KHALA,0,3.9),(None,1.95,1.9),(AUN2,-1.95,2.0),(AUN3,-.2,-.4),(AUN4,2.5,-.9),(AUN5,-2.5,-1.0)]
def gang():
    A=[]
    for i,(c,x,y) in enumerate(GANG):
        H=queen(x,y,180) if c is None else mk(c,x,y,180,'g%d'%i); A.append(H)
        if c is not None: mithai(H,-1,('#D83A8A','#F2C14E','#16909E','#E8742A','#6A4C93','#2E8A4A')[i])
    return A
def gang_idle(A,t,kn=0.0):
    for i,(H,(c,x,y)) in enumerate(zip(A,GANG)):
        standp(H,t,x,y,180); fc(H,'happy'); H['arm'][-1].rotation_euler=(R(-18+3*math.sin(t*3+i)),0,R(-10)); blink(H,t)
        if c is None: cape_flap(H,t,k=.6)
        elif i: H['arm'][1].rotation_euler=(R(-160+12*math.sin(t*8+i)),0,R(16))
def s_NOINV():
    G=qila_ext(); FILLE[0]=60; A=gang(); lamp((0,4.6,3.0),160,(1,.8,.55))
    def upd(t):
        gang_idle(A,t); a=A[0]; kn=abs(math.sin(t*10)); arm_to(a,1,(-.8,5.3,2.0+.12*kn),1,base=(0,0,0)); cam2(t,(0,5.55,2.5),(0,5.5,2.4),(0,2.6,1.75),20)
    return dict(upd=upd)
SHOTS['NOINV']=s_NOINV
def s_PUTTAR():
    G=qila_ext(); FILLE[0]=50; A=gang(); lamp((0,4.6,3.0),150,(1,.8,.55))
    def upd(t):
        gang_idle(A,t); a=A[0]; speak(a,t,318,321,gesture=False); a['arm'][1].rotation_euler=(R(-150+16*math.sin(t*9)),0,R(22)); a['arm'][-1].rotation_euler=(R(-100),0,R(-12)); a['root'].location[2]=.05*abs(math.sin(t*8))
        c1(t,a,yaw=-10,dist=1.55,lens=30,ref=180,tz=-.3,push=0)
    return dict(upd=upd)
SHOTS['PUTTAR']=s_PUTTAR
IN=[(KHALA,0,6.9),(None,2.0,7.8),(AUN2,-2.0,7.8)]
def inside():
    A=[]
    for i,(c,x,y) in enumerate(IN):
        H=queen(x,y,0) if c is None else mk(c,x,y,0,'i%d'%i); A.append(H)
        if c is not None: mithai(H,-1,('#D83A8A','#F2C14E','#16909E')[i])
    return A
def inside_idle(A,t,dy=0.0):
    for i,(H,(c,x,y)) in enumerate(zip(A,IN)):
        standp(H,t,x,y-dy,0); walk(H,dy+i*.3,step=.55,arm=0) if dy>0 else None; fc(H,'happy'); H['arm'][-1].rotation_euler=(R(-18),0,R(-10)); H['arm'][1].rotation_euler=(R(-160+12*math.sin(t*8+i)),0,R(16))
        if c is None: cape_flap(H,t,k=.6)
OUT=[(KHALA,0,9.9),(None,.95,11.9),(AUN2,-.95,11.9),(AUN3,0,13.9)]
def s_MITHAI():
    G=qila(locks=True); FILLE[0]=70; A=[]
    for i,(c,x,y) in enumerate(OUT):
        H=queen(x,y,0) if c is None else mk(c,x,y,0,'o%d'%i); A.append(H)
        if c is not None: mithai(H,-1,('#D83A8A','#F2C14E','#16909E','#E8742A')[i])
    lamp((0,6.6,3.4),260,(1,.82,.55),r=1)
    def upd(t):
        k=ease((t-.05)/.22); gate(G,-k); G['locks'].scale=(0,0,0) if t>.05 else (1,1,1); dy=2.1*ease((t-.2)/max(.3,DUR-.2))
        for i,(H,(c,x,y)) in enumerate(zip(A,OUT)):
            standp(H,t,x,y-dy,0); walk(H,dy*1.6+i*.3,step=.55,arm=0); fc(H,'happy'); H['arm'][-1].rotation_euler=(R(-18),0,R(-10)); H['arm'][1].rotation_euler=(R(-160+12*math.sin(t*8+i)),0,R(16))
            if c is None: cape_flap(H,t,k=.8)
        speak(A[0],t,322,326,gesture=False); cam2(t,(0,2.6,1.2),(0,3.2,1.25),(0,8.2,2.2),26)
    return dict(upd=upd)
SHOTS['MITHAI']=s_MITHAI
def s_SURVIVE():
    G=qila(locks=True); FILLE[0]=70; A=inside(); d=prince(0,-.6,0); lamp((0,4.0,3.6),500,(1,.82,.55),r=1)
    def upd(t):
        gate(G,-1); G['locks'].scale=(0,0,0); f=ease((t-1.25)/.5); inside_idle(A,t,dy=min(3.4,1.0*t))
        pstand(d,t,0,-.6,0,flap=.3); fc(d,'scream' if t<.55 else 'dead'); d['root'].rotation_euler[0]=R(-86*f*f); d['head'].rotation_euler[0]=R(0)
        cam2(t,(.5,-3.7,1.85),(.3,-3.3,1.8),LV((0,-.6,2.25),(0,3.6,1.9),f),30)
    return dict(upd=upd)
SHOTS['SURVIVE']=s_SURVIVE
