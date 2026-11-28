# "Everyone is from Islamabad" (vampire): shots. Rig note: brow_r POSITIVE = angry slant, NEGATIVE = worried slant.
SEQ=[('QUEUE', 0.0), ('EVERY', 2.633), ('HERO', 4.4), ('PIRATE', 6.4), ('EVEN', 8.3), ('AREFROM', 10.6), ('ASLEEP', 11.967), ('STRANGER', 15.367), ('KIS', 18.3), ('RED', 20.567), ('THREEAM', 22.4), ('ARRIVES', 24.867), ('OLD', 27.567), ('EMPTIED', 29.2), ('MOVIES', 31.7), ('NINE05', 35.133), ('NOBODY', 36.933), ('SAVER', 39.067), ('FINDS', 41.867), ('WALEED', 43.867), ('KHOON', 45.4), ('NAU', 47.267), ('NEWPLAN', 49.767), ('INVITED', 51.467), ('BELL', 54.7), ('KAUN', 56.3), ('COUNT', 57.367), ('GRADEQ', 59.167), ('GRADE', 60.833), ('SATRAH', 61.633), ('ADDRESS', 63.867), ('G102', 65.433), ('G101', 67.633), ('G103', 69.367), ('G104', 70.5), ('HUNTING', 71.967), ('DEFEATED', 73.767), ('RESTS', 76.0), ('MONKEY', 78.033), ('WAPAS', 79.467), ('BETTER', 81.2), ('FIVEAM', 82.9), ('ATONCE', 86.067), ('BETA', 87.133), ('DHOOP', 88.733), ('NAHI', 90.1), ('RUNS', 91.667), ('OFFICE', 94.2), ('COOL', 95.467), ('WORKING', 97.533), ('NAYE', 98.933), ('MONTH', 101.767), ('BECAUSE', 104.7), ('OFFICER', 106.1), ('DESK', 108.467), ('FITS', 110.267), ('WOLF', 111.467), ('NAU2', 113.6), ('SURVIVE', 116.133)]
END=119.1333
WI={'QUEUE': 0, 'EVERY': 7, 'HERO': 11, 'PIRATE': 16, 'EVEN': 21, 'AREFROM': 28, 'ASLEEP': 31, 'STRANGER': 41, 'KIS': 49, 'RED': 57, 'THREEAM': 62, 'ARRIVES': 69, 'OLD': 75, 'EMPTIED': 79, 'MOVIES': 86, 'NINE05': 96, 'NOBODY': 100, 'SAVER': 106, 'FINDS': 111, 'WALEED': 117, 'KHOON': 121, 'NAU': 125, 'NEWPLAN': 132, 'INVITED': 136, 'BELL': 145, 'KAUN': 150, 'COUNT': 152, 'GRADEQ': 156, 'GRADE': 159, 'SATRAH': 160, 'ADDRESS': 166, 'G102': 170, 'G101': 175, 'G103': 180, 'G104': 183, 'HUNTING': 186, 'DEFEATED': 191, 'RESTS': 196, 'MONKEY': 202, 'WAPAS': 207, 'BETTER': 211, 'FIVEAM': 217, 'ATONCE': 226, 'BETA': 228, 'DHOOP': 233, 'NAHI': 236, 'RUNS': 239, 'OFFICE': 247, 'COOL': 250, 'WORKING': 256, 'NAYE': 259, 'MONTH': 267, 'BECAUSE': 274, 'OFFICER': 278, 'DESK': 284, 'FITS': 291, 'WOLF': 295, 'NAU2': 303, 'SURVIVE': 310}
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
HG=(9.4,4.75)          # the gate of the hero house (cx=7)
AB=(8.2,7.75,3.55)     # aunty's spot on the balcony
# ================================================================ hook: everyone is from Islamabad
QX=[0.0,1.9,3.8,5.7,7.6,9.5]; QP=[QX[4],QX[2],QX[3],QX[0],QX[1],QX[5]]; QC=(-4.2,2.2,1.9)
def queue(mood='ib_day'):
    sector(mood,0.0,stars=False,signal='green'); FILLE[0]=40
    B.cyl((3.6,5.95,3.0),.06,6.0,M('#C9CED8',.4,metal=.5),seg=8); sign('BUS STOP  G-10',(3.52,5.91,5.5),.26,'#FFFFFF','#1E6A3A',n=(-.92,-.39,0),pad=.18,th=.06,frame='#F6F4EE'); B.done('stop')
    G=[mk(UNCLEQ,QP[0],5.0,-90,'q0'),mk(SUPER,QP[1],5.0,-90,'q1'),mk(PIRATE,QP[2],5.0,-90,'q2'),mk(WALEED,QP[3],5.0,-90,'waleed'),vamp(QP[4],5.0,-90,'drac'),mk(AUNTY,QP[5],5.0,-90,'q5')]
    mask(G[1]); cape(G[1],'#16909E','#F2C14E',collar=False); pirate_hat(G[2]); um=umbrella(); return G,um
def queue_idle(G,um,t):
    for k,H in enumerate(G): standp(H,t,QP[k],5.0,-90); fc(H,('calm','happy','firm','calm','flat','calm')[k])
    cape_flap(G[1],t,amp=3); cape_flap(G[4],t,amp=3); hold(G[4],1,-64); h=handw(G[4],1); um.location=(h.x,h.y,h.z-.25)
def QUEUE():
    G,um=queue()
    def upd(t):
        queue_idle(G,um,t); G[0]['head'].rotation_euler[0]=R(10); look_at(G[3],QC,ease((t-.9)/.35)); fc(G[3],'happy' if t>1.1 else 'calm')
        cam2(t,(-4.9,1.9,1.9),(-4.3,2.15,1.9),(4.0,5.6,1.7),30)
    return dict(upd=upd)
SHOTS['QUEUE']=QUEUE
def EVERY():
    G,um=queue()
    def upd(t):
        queue_idle(G,um,t)
        for k,H in enumerate(G):
            q=ease((t-we(9)+.3-.06*k)/.18); look_at(H,QC,max(q,1.0 if k==3 else 0)); fc(H,'happy' if q>.5 or k==3 else ('calm','happy','firm','calm','flat','calm')[k])
        cam2(t,(-4.1,2.25,1.95),(-3.85,2.4,1.95),(3.4,5.5,1.8),32)
    return dict(upd=upd)
SHOTS['EVERY']=EVERY
def HERO():
    sector('ib_day',0.0,stars=False); FILLE[0]=30; s=mk(SUPER,-7,10.4,10,'super',z=7.43); mask(s); cape(s,'#16909E','#F2C14E',collar=False); cu=cup_of(s,1)
    def upd(t):
        standp(s,t,-7,10.4,10); cape_flap(s,t,a=14,amp=9,w=6); crossed(s) if t<.0 else None; s['arm'][-1].rotation_euler=(R(18),0,R(-28)); hold_chai(s,cu,1,sip=ease((t-.9)/.4)); fc(s,'smug')
        cam2(t,(-5.6,6.3,7.2),(-5.9,6.8,7.5),(-7,10.4,9.5),30)
    return dict(upd=upd)
SHOTS['HERO']=HERO
def PIRATE_():
    deck(); FILLE[0]=30; p=mk(PIRATE,.4,2.4,-8,'pirate'); pirate_hat(p); cu=cup_of(p,1)
    def upd(t):
        standp(p,t,.4,2.4,-8); p['root'].rotation_euler[1]=R(2.5*math.sin(t*1.6)); hold_chai(p,cu,1,sip=.9*ease((t-.7)/.4)); p['arm'][-1].rotation_euler=(R(14),0,R(-24)); fc(p,'firm')
        cam2(t,(1.6,-2.9,1.5),(1.4,-2.3,1.6),(.4,2.4,2.2),36); CAM.rotation_euler[1]+=R(1.5*math.sin(t*1.6))
    return dict(upd=upd)
SHOTS['PIRATE']=PIRATE_
def EVEN():
    sector('ib_night',1.0); FILLE[0]=120; d=vamp(2,0,0,'drac'); BT=bats(7); lamp((2.6,-2.6,3.2),260,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,2,0,0,flap=1.6); fc(d,'smug'); d['head'].rotation_euler[0]=R(-6); claws(d,t,.25); bats_fly(BT,t,(-6,26,10),(5.5,-3,.4),spread=4)
        cam2(t,(2.5,-3.6,1.05),(2.4,-2.9,1.2),(2,0,2.2),30)
    return dict(upd=upd)
SHOTS['EVEN']=EVEN
def AREFROM():
    sector('ib_night',1.0); FILLE[0]=120; d=vamp(2,0,0,'drac'); cu=cup_of(d,1); lamp((2.6,-2.6,3.2),260,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,2,0,0); k=ease((t-.25)/.35); hold_chai(d,cu,1,sip=.95*k*(1-ease((t-1.05)/.25))); fc(d,'happy' if t>1.05 else 'calm'); d['arm'][-1].rotation_euler=(R(-6),0,0)
        cam2(t,(2.2,-3.9,2.3),(2.2,-3.5,2.3),(2,0,2.05),32)
    return dict(upd=upd)
SHOTS['AREFROM']=AREFROM
# ================================================================ the rules of this world
def ASLEEP():
    sector('ib_night',1.0); FILLE[0]=0; P=[(lightpane(x,y,z,hx,hz,3.4),x) for (x,y,z,hx,hz) in WINS if -12<x<45]
    def upd(t):
        for o,x in P: o.scale=(0,0,0) if t>1.25+(x+2)*.035 else (1,1,1)
        cam2(t,(-3.0,-5.2,4.4),(-2.0,-5.0,4.5),(16,9,4.5),24)
    return dict(upd=upd)
SHOTS['ASLEEP']=ASLEEP
SP=dict(n=(12.6,4.9,-62),u=(9.2,5.0,58),a=(7.2,5.25,48))
def stranger():
    sector('ib_gold',0.0,stars=False,awake=.0); FILLE[0]=70; n=mk(NEWBOY,*SP['n'],'newboy'); u=mk(UNCLEQ,*SP['u'],'uncleq'); a=mk(AUNTY,*SP['a'],'aunty')
    bg=empty((13.6,5.4,0)); obox((0,0,.55),(.28,.2,.45),M('#2B58C9',.5),.06,bg); obox((0,0,1.25),(.03,.03,.3),M('#C9CED8',.3,metal=.7),0,bg); return n,u,a
def STRANGER():
    n,u,a=stranger()
    def upd(t):
        for k,H in zip('nua',(n,u,a)): standp(H,t,*SP[k])
        fc(n,'happy'); wave_hi(n,t,.15,1,1.2); fc(u,'firm'); fc(a,'firm'); crossed(u); look_at(u,headw(n),.7); look_at(a,headw(n),.7); look_at(n,headw(u),.6)
        k=ease((t-1.5)/.4); a['root'].rotation_euler[1]=R(-5*k); u['root'].rotation_euler[1]=R(-4*k)
        c1(t,n,yaw=18,dist=3.0,lens=38,ref=-62)
    return dict(upd=upd)
SHOTS['STRANGER']=STRANGER
def KIS():
    n,u,a=stranger(); FILLE[0]=150; PU=(9.9,4.35,73); PA=(10.1,2.55,106); CP=(13.5,3.45,2.0)
    def upd(t):
        standp(n,t,*SP['n']); n['root'].location[2]=-40; standp(u,t,*PU); standp(a,t,*PA); fc(a,'firm'); fc(u,'firm'); speak(a,t,49,52,gesture=False); speak(u,t,53,56,gesture=False)
        ka=ease(t/.25)*(1-ease((t-we(52)-.05)/.3)); ku=ease((t-ws(53)+.1)/.25); a['root'].rotation_euler[0]=R(7*ka); u['root'].rotation_euler[0]=R(8*ku)
        a['arm'][1].rotation_euler=(R(-78*ka+5*math.sin(t*9)*ka),0,R(6)); look_at(u,CP,.9); look_at(a,CP,.9)
        cam2(t,(13.8,3.45,2.0),(13.5,3.45,2.0),(10.0,3.47,1.72),21.5)
    return dict(upd=upd)
SHOTS['KIS']=KIS
def redlight():
    sector('ib_night',1.0,signal='red'); FILLE[0]=30; C=kcar((-12.6,-2.0,0),180,'#F4F1EA',4); lamp((-12.6,-5.2,3.0),160,(1,.86,.62)); return C
def RED():
    C=redlight()
    def upd(t):
        roll(C,-12.6,-2.0,180,0); cam2(t,(-2.0,-.9,4.6),(-3.0,-1.0,4.4),(-20,-2.8,1.9),32)
    return dict(upd=upd)
SHOTS['RED']=RED
def THREEAM():
    C=redlight(); lf=empty((0,0,-9)); obox((0,0,0),(.12,.07,.006),M('#B8862A',.7),0,lf)
    def upd(t):
        roll(C,-12.6,-2.0,180,0); lf.location=(-30+4.2*t,1.2+.5*math.sin(t*2),.12+.1*abs(math.sin(t*5))); lf.rotation_euler=(t*4,t*3,t*2)
        cam2(t,(-21.6,-2.6,.85),(-23.6,-2.9,1.3),(-13.5,-2.2,1.5),24,(-13.5,-2.2,2.2))
    return dict(upd=upd)
SHOTS['THREEAM']=THREEAM
# ================================================================ the vampire king arrives
def ARRIVES():
    sector('ib_night',1.0); FILLE[0]=60; d=vamp(0,0,0,'drac'); BT=bats(9); lp=lamp((0,0,0),1500,(.7,.8,1.0))
    def upd(t):
        q=ease(t/DUR); p=LV((62,1.5,26),(4.4,1.3,3.8),q); vfly(d,t,p,-90); lp.location=(p[0]-2.5,p[1]-2.5,p[2]+2); bats_fly(BT,t,(p[0]+5.0,p[1]+.5,p[2]+1.6),(-.001,0,0),spread=2.4)
        cam2(t,(.6,-2.8,1.4),(.9,-2.5,1.5),(p[0],p[1],p[2]+.6),28)
    return dict(upd=upd)
SHOTS['ARRIVES']=ARRIVES
VP=(2.0,0.0)
def OLD():
    sector('ib_night',1.0); FILLE[0]=130; d=vamp(VP[0],VP[1],0,'drac'); lamp((3.2,-2.8,3.4),240,(.6,.7,1.0))
    def upd(t):
        k=ease(t/.4); vstand(d,t,VP[0],VP[1],0,flap=2.2-1.2*k); d['root'].location[2]=1.6*(1-k)**2; fc(d,'smug'); d['head'].rotation_euler[0]=R(14*(1-ease((t-.35)/.4)))
        for s in (1,-1): d['leg'][s].rotation_euler[0]=R(-14*math.sin(pi*min(1,t/.5)))
        c1(t,d,yaw=-14,dist=2.7,lens=40,dz=-.25,tz=-.1,ref=0)
    return dict(upd=upd)
SHOTS['OLD']=OLD
def EMPTIED():
    sector('ib_night',1.0); FILLE[0]=110; d=vamp(VP[0],VP[1],0,'drac'); lamp((3.2,-2.8,3.4),200,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,VP[0],VP[1],0,flap=1.5); fc(d,'smug'); d['head'].rotation_euler[2]=R(22*math.sin(t*1.5)); claws(d,t,.18)
        q=ease(t/DUR); a=R(-38+34*q); camset((VP[0]+4.3*math.sin(a),VP[1]-4.3*math.cos(a),1.0),(VP[0],VP[1],2.0),28,8)
    return dict(upd=upd)
SHOTS['EMPTIED']=EMPTIED
def MOVIES():
    sector('ib_night',1.0); FILLE[0]=110; d=vamp(VP[0],VP[1],0,'drac'); fl=lamp((2,-3,5),0,(.8,.85,1.0))
    def upd(t):
        k=ease((t-.5)/.35); vstand(d,t,VP[0],VP[1],0,flap=1.2+1.6*k); claws(d,t,k); fc(d,'shout' if k>.4 else 'smug'); d['head'].rotation_euler[0]=R(-16*k)
        fl.data.energy=26000 if (1.02<t<1.1 or 1.3<t<1.36) else 0
        cam2(t,(2.9,-5.2,.8),(2.6,-4.2,.9),(2,0,1.8),24,(2,0,2.0))
    return dict(upd=upd)
SHOTS['MOVIES']=MOVIES
def NINE05():
    sector('ib_night',1.0); FILLE[0]=0; d=vamp(VP[0],VP[1],0,'drac'); lf=empty((0,0,-9)); obox((0,0,0),(.12,.07,.006),M('#B8862A',.7),0,lf)
    def upd(t):
        vstand(d,t,VP[0],VP[1],0,flap=.6); claws(d,t,1.0); fc(d,'shout'); d['head'].rotation_euler[0]=R(-16)
        lf.location=(8-3.6*t,-1.6+.4*math.sin(t*2.2),.12+.1*abs(math.sin(t*5))); lf.rotation_euler=(t*4,t*3,t*2)
        cam2(t,(13.5,-3.6,7.2),(14.2,-3.6,7.6),(-2,.6,-1.4),24)
    return dict(upd=upd)
SHOTS['NINE05']=NINE05
def NOBODY():
    sector('ib_night',1.0); FILLE[0]=120; d=vamp(VP[0],VP[1],0,'drac'); lamp((3.2,-2.8,3.4),200,(.6,.7,1.0))
    def upd(t):
        k=1-ease((t-.2)/.7); vstand(d,t,VP[0],VP[1],0,flap=.7); claws(d,t,k); fc(d,'worry' if k<.5 else 'shout'); a=ease((t-.9)/.3); b=ease((t-1.5)/.35); d['head'].rotation_euler=(R(-16*k),0,R(-42*a+84*b))
        c1(t,d,yaw=8,dist=3.6,lens=36,tz=-.35,ref=0)
    return dict(upd=upd)
SHOTS['NOBODY']=NOBODY
def SAVER():
    sector('ib_night',1.0); FILLE[0]=120; d=vamp(VP[0],VP[1],0,'drac'); lamp((3.2,-2.8,3.4),200,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,VP[0],VP[1],0,flap=.7); fc(d,'worry'); speak(d,t,106,110,gesture=False); what_pose(d,ease((t-we(108))/.3),t,.7); d['head'].rotation_euler[2]=R(-16+32*ease((t-we(108))/.4))
        c1(t,d,yaw=-12,dist=3.0,lens=40,ref=0)
    return dict(upd=upd)
SHOTS['SAVER']=SAVER
def naan(H): return in_hand(H,-1,lambda e:(obox((0,0,-.3),(.2,.08,.24),M('#F4F1EA',.8,kind='fabric'),.04,e),obox((0,0,-.05),(.16,.03,.05),M('#F4F1EA',.8),.02,e),obox((0,0,-.2),(.14,.085,.07),M('#D9A45A',.8),.02,e)))
def FINDS():
    sector('ib_night',1.0); FILLE[0]=110; w=mk(WALEED,24.5,5.0,-90,'waleed'); naan(w); d=vamp(16.6,2.4,-45,'drac'); lamp((14.6,1.0,2.6),150,(.6,.7,1.0))
    def upd(t):
        walk_path(w,[(24.5,5.0),(22,5.0)],t,-.5,DUR+.6,step=.55,arm=20); blink(w,t); fc(w,'calm'); w['arm'][-1].rotation_euler=(0,0,0)
        q=ease((t-.55)/.5); vstand(d,t,16.6,2.4,-45+85*q,flap=.5); look_at(d,headw(w),ease((t-.45)/.4),maxyaw=80); fc(d,'bored' if t<.5 else 'smug')
        cam2(t,(13.6,-.6,1.8),(13.9,-.4,1.85),(18.5,2.6,2.0),30)
    return dict(upd=upd)
SHOTS['FINDS']=FINDS
def WALEED_():
    sector('ib_night',1.0); FILLE[0]=110; w=mk(WALEED,22,5.0,-90,'waleed'); naan(w)
    def upd(t):
        x=22.6-1.25*t; w['root'].location[0]=x; w['root'].rotation_euler[2]=R(-90); walk(w,1.25*t,step=.55,arm=20); blink(w,t); fc(w,'calm'); w['arm'][-1].rotation_euler=(0,0,0)
        camset((x-3.1,2.9,1.9),(x-.1,5.0,1.35),38,8)
    return dict(upd=upd)
SHOTS['WALEED']=WALEED_
WK=(19.0,5.0); DK=(16.8,5.0)
def KHOON():
    sector('ib_night',1.0); FILLE[0]=130; d=vamp(DK[0],DK[1],90,'drac'); fl=lamp((19,3,3),0,(.8,.85,1.0)); lamp((18.4,2.6,2.2),160,(.6,.7,1.0))
    def upd(t):
        k=ease(t/.3); vstand(d,t,DK[0],DK[1],90,flap=2.4-1.2*k); d['root'].location[2]=.9*(1-k)**2; claws(d,t,k); fc(d,'shout'); speak(d,t,121,124,gesture=False); face(d,brow_r=14)
        fl.data.energy=22000 if .3<t<.37 else 0
        c1(t,d,yaw=16,dist=3.3,lens=30,dz=-1.1,tz=.15,ref=90)
    return dict(upd=upd)
SHOTS['KHOON']=KHOON
def NAU():
    sector('ib_night',1.0); FILLE[0]=120; w=mk(WALEED,WK[0],WK[1],-90,'waleed'); naan(w); ph=phone_of(w,1)
    def upd(t):
        standp(w,t,WK[0],WK[1],-90); fc(w,'bored'); speak(w,t,125,131,gesture=False); k=ease((t-.05)/.3)*(1-ease((t-we(128)-.15)/.3)); phone_up(w,1,k,h=3.5,fw=1.3,sx=.5); w['head'].rotation_euler[0]=R(12*k); w['arm'][-1].rotation_euler=(0,0,0)
        c1(t,w,yaw=-18,dist=2.9,lens=40,ref=-90)
    return dict(upd=upd)
SHOTS['NAU']=NAU
def NEWPLAN():
    sector('ib_night',1.0); FILLE[0]=120; d=vamp(DK[0],DK[1],90,'drac'); lamp((17.8,2.4,2.6),160,(.6,.7,1.0))
    def upd(t):
        q=ease((t-.15)/.45); vstand(d,t,DK[0],DK[1],90-80*q,flap=.6); k=1-ease(t/.35); claws(d,t,k); i=ease((t-ws(134)+.15)/.25)
        fc(d,'worry' if t<.5 else ('wow' if i>.5 else 'flat'))
        if i>0: d['arm'][1].rotation_euler=(R(-150*i),0,R(8)); d['head'].rotation_euler[2]=R(-38*i)
        cam2(t,(18.2,1.3,1.9),(18.0,1.6,1.9),(DK[0]+.3,DK[1],2.0),34)
    return dict(upd=upd)
SHOTS['NEWPLAN']=NEWPLAN
# ================================================================ the house
def bellbox():
    e=empty((7.9,5.97,1.4)); obox((0,0,0),(.11,.03,.16),M('#C9CED8',.4,metal=.6),.02,e); b=oico((0,-.035,.02),.045,M('#FFD890',.3,emit=2.5),e,sub=2); obox((0,-.03,-.09),(.06,.006,.02),M('#16171C',.5),0,e); return e,b
def INVITED():
    sector('ib_night',1.0); FILLE[0]=110; d=vamp(HG[0],3.0,180,'drac'); bellbox(); sh=obox((HG[0],5.55,1.5),(1.5,.02,1.6),M('#FF3A4A',.3,emit=3.0,alpha=.35),0); lp=lightpane(); fl=lamp((HG[0],4.6,2.4),0,(1,.25,.3)); sk=oico((HG[0],5.45,2.1),.42,M('#FF4A5A',.3,emit=6.0),0,sub=1)
    def upd(t):
        a=ease((t-.1)/.9); b=ease((t-1.15)/.25); c=ease((t-1.45)/.5); y=3.0+2.1*a-.9*b
        standp(d,t,HG[0],y,180); walk(d,2.1*a,step=.5,arm=18) if a<1 else None; cape_flap(d,t,amp=5+10*b*(1-c)); d['root'].rotation_euler[0]=R(-13*b*(1-c)); fc(d,'shock' if b>.3 else 'smug')
        if b>.2: hands_head(d,(1-c)*.0); d['arm'][1].rotation_euler=(R(-95*(1-c)),0,R(20)); d['arm'][-1].rotation_euler=(R(-95*(1-c)),0,R(-20))
        sh.scale=(1,1,1) if 1.12<t<1.5 and int(t*30)%2==0 else (0,0,0); fl.data.energy=900 if 1.12<t<1.5 else 0; z_=(1+.5*math.sin(t*60)) if 1.12<t<1.42 else 0; sk.scale=(z_,z_,z_); sk.rotation_euler=(t*9,t*7,t*5)
        cam2(t,(15.6,3.1,1.8),(15.0,3.3,1.8),(HG[0],y+.3,1.95),40)
    return dict(upd=upd)
SHOTS['INVITED']=INVITED
def BELL():
    sector('ib_night',1.0); FILLE[0]=90; d=vamp(8.8,4.95,-90,'drac'); e,b=bellbox(); lp=lightpane(e=0.0); lamp((6.9,4.4,2.0),40,(1,.86,.62),r=.3)
    def upd(t):
        vstand(d,t,8.8,4.95,-90,flap=.4); k=ease((t-.15)/.4); p=ease((t-.62)/.1)*(1-ease((t-.85)/.12)); arm_to(d,-1,(7.93,5.84-.05*p+.08,1.42),k,base=(0,0,0)); fc(d,'smug'); d['head'].rotation_euler[2]=R(-20)
        b.scale=(1+.5*p,)*3; e.location=(7.9,5.97+.012*p,1.4)
        cam2(t,(5.5,2.9,1.65),(5.8,3.1,1.65),(8.6,5.3,1.9),32)
    return dict(upd=upd)
SHOTS['BELL']=BELL
def house(dy=HG[1]):
    sector('ib_night',1.0); FILLE[0]=110; d=vamp(HG[0],dy,180,'drac'); a=mk(AUNTY,AB[0],AB[1],0,'aunty',z=AB[2]); bellbox(); lp=lightpane(); lamp((8.6,6.4,6.0),90,(1,.86,.62)); return d,a,lp
def aunty_idle(a,t,d): standp(a,t,AB[0],AB[1],0); a['root'].location[2]=AB[2]; a['head'].rotation_euler=(R(26),0,R(14))
def drac_gate(d,t): vstand(d,t,HG[0],HG[1],180,flap=.5); d['head'].rotation_euler=(R(-30),0,R(-12))
def acam(t,lens=38): cam2(t,(11.2,5.2,3.4),(11.0,5.4,3.5),(AB[0],AB[1],AB[2]+1.95),lens)
def dcam(t,lens=26,z=3.3): cam2(t,(8.95,6.7,z),(9.0,6.62,z-.05),(HG[0],HG[1],2.05),lens)
def KAUN():
    d,a,lp=house()
    def upd(t):
        drac_gate(d,t); aunty_idle(a,t,d); fc(a,'firm'); speak(a,t,150,151,gesture=False); acam(t)
    return dict(upd=upd)
SHOTS['KAUN']=KAUN
def COUNT():
    d,a,lp=house()
    def upd(t):
        drac_gate(d,t); aunty_idle(a,t,d); fc(d,'smug'); speak(d,t,152,155,gesture=False); k=ease((t-we(152)-.05)/.3)*(1-ease((t-we(154))/.3)); d['root'].rotation_euler[0]=R(-16*k); d['arm'][1].rotation_euler=(R(-60*k),0,R(-40*k)); d['arm'][-1].rotation_euler=(R(20*k),0,R(-30*k)); cape_flap(d,t,amp=5+6*k)
        dcam(t)
    return dict(upd=upd)
SHOTS['COUNT']=COUNT
def GRADEQ():
    d,a,lp=house()
    def upd(t):
        drac_gate(d,t); aunty_idle(a,t,d); fc(a,'firm'); speak(a,t,156,158,gesture=False); k=ease((t-we(156))/.25); a['root'].rotation_euler[0]=R(7*k); a['head'].rotation_euler[0]=R(26+8*k)
        acam(t,44)
    return dict(upd=upd)
SHOTS['GRADEQ']=GRADEQ
def GRADE():
    d,a,lp=house()
    def upd(t):
        drac_gate(d,t); aunty_idle(a,t,d); fc(d,'worry'); speak(d,t,159,159,gesture=False); d['head'].rotation_euler[1]=R(9*ease(t/.3))
        dcam(t,36)
    return dict(upd=upd)
SHOTS['GRADE']=GRADE
def SATRAH():
    d,a,lp=house()
    def upd(t):
        drac_gate(d,t); aunty_idle(a,t,d); fc(a,'firm'); speak(a,t,160,165,gesture=False); k=ease((t-we(165)-.02)/.3); a['root'].rotation_euler[2]=R(150*k); a['root'].location[1]=AB[1]+.75*k; a['arm'][1].rotation_euler=(R(-55*(1-k)*abs(math.sin(t*7))),0,R(38*(1-k)))
        lp.location[2]=-80 if t>we(165)+.38 else 4.6
        acam(t,36)
    return dict(upd=upd)
SHOTS['SATRAH']=SATRAH
# ================================================================ lost in the sectors
def paper(H,s=1): return in_hand(H,s,lambda e:(obox((0,-.14,.12),(.16,.008,.22),M('#E8D8B0',.8),.004,e,rot=(R(-50),0,0)),obox((0,-.15,.3),(.17,.02,.02),M('#8A6238',.7),.008,e,rot=(R(-50),0,0))))
def ADDRESS():
    sector('ib_night',1.0); FILLE[0]=120; d=vamp(9.0,3.2,-20,'drac'); pp=paper(d,1); lamp((10.2,.8,3.0),180,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,9.0,3.2,-20,flap=.5); k=ease(t/.4); phone_up(d,1,k,h=3.55,fw=1.25,sx=.3); d['head'].rotation_euler[0]=R(18*k); fc(d,'firm')
        c1(t,d,yaw=14,dist=3.2,lens=38,ref=-20,tz=-.3)
    return dict(upd=upd)
SHOTS['ADDRESS']=ADDRESS
def G102():
    sector('ib_night',1.0); FILLE[0]=60; pm=M('#E8D8B0',.85); e=empty((2,-1,1.8)); obox((0,0,0),(.2,.006,.15),pm,.004,e); obox((0,0,.155),(.21,.014,.014),M('#8A6238',.7),.006,e); obox((0,0,-.155),(.21,.014,.014),M('#8A6238',.7),.006,e)
    ink=M('#3A1410',.6); text('G-10/2',(0,-.008,.045),(0,-1,0),.085,ink,ex=.002,parent=e); text('STREET 43',(0,-.008,-.065),(0,-1,0),.06,ink,ex=.002,parent=e)
    for s in (-1,1): obox((s*.235,-.01,-.03),(.045,.03,.06),M(DRAC['skin'],.55),.02,e)
    lamp((2,-2.2,2.2),30,(1,.9,.75),r=.3)
    def upd(t):
        e.rotation_euler=(R(-8+1.2*math.sin(t*2.3)),R(1.5*math.sin(t*1.7)),0); e.location=(2,-1,1.8+.004*math.sin(t*3))
        cam2(t,(2,-2.2,1.84),(2,-2.05,1.83),(2,-1,1.8),50,fs=2.0)
    return dict(upd=upd)
SHOTS['G102']=G102
def board(txt,x,y,n,h=3.3,size=.36):
    B.cyl((x,y+n[1]*-.1,h/2+.3),.06,h+.6,M('#C9CED8',.4,metal=.5),seg=8); sign(txt,(x,y,h),size,'#FFFFFF','#1E6A3A',n=n,e=1.8,pad=.22,th=.06,frame='#F6F4EE'); B.done('board')
def G101():
    sector('ib_night',1.0); board('G-10/1',-14.9,4.9,(0,-1,0)); FILLE[0]=130; d=vamp(-13.3,4.3,8,'drac'); lamp((-13,1.6,3.2),200,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,-13.3,4.3,8,flap=.5); fc(d,'worry'); k=ease((t-.15)/.35); d['head'].rotation_euler=(R(-22*k),0,R(-34*k)); headtouch(d,-1,ease((t-.7)/.3),dx=-.3,dy=-.2,dz=.75)
        cam2(t,(-12.9,-.5,1.5),(-13.0,-.1,1.55),(-14.2,4.6,2.95),30)
    return dict(upd=upd)
SHOTS['G101']=G101
def G103():
    sector('ib_night',1.0); board('G-10/3',23.0,-4.9,(0,1,0)); FILLE[0]=130; d=vamp(24.7,-4.2,180,'drac'); BT=bats(4); lamp((25,-1.6,3.2),200,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,24.7,-4.2,180,flap=.6); d['root'].location[2]=.5+.08*math.sin(t*4); fc(d,'shock'); d['head'].rotation_euler=(R(-20),0,R(34)); what_pose(d,1,t,.6); bats_fly(BT,t,(27,-3.4,3.6),(-.5,0,.1),spread=.7)
        cam2(t,(24.4,.4,1.6),(24.3,0,1.65),(23.8,-4.6,3.0),30)
    return dict(upd=upd)
SHOTS['G103']=G103
def G104():
    sector('ib_night',1.0); board('G-10/4',39.6,4.9,(0,-1,0)); FILLE[0]=130; d=vamp(41.2,4.3,8,'drac'); lamp((41.5,1.6,3.2),200,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,41.2,4.3,8,flap=.5); fc(d,'sad'); k=ease((t-.25)/.3); headtouch(d,1,k,dx=.1,dy=-.72,dz=.7); d['head'].rotation_euler=(R(16*k),0,0)
        cam2(t,(41.5,-.5,1.5),(41.4,-.1,1.55),(40.3,4.6,2.95),30)
    return dict(upd=upd)
SHOTS['G104']=G104
def HUNTING():
    sector('ib_night',1.0); FILLE[0]=90; X0,Y0=35.0,0.0; d=vamp(X0,Y0,0,'drac'); BT=bats(6); lamp((X0+1.6,Y0-2.6,1.2),170,(.6,.7,1.0)); lamp((X0-1.8,Y0+1.6,3.8),220,(1,.3,.3))
    def upd(t):
        k=ease(t/.35); vstand(d,t,X0,Y0,0,flap=2.2); fc(d,'smug'); d['head'].rotation_euler[0]=R(-10*k)
        for s_ in (1,-1): d['arm'][s_].rotation_euler=(R(-100*k+3*math.sin(t*5+s_)),0,R(s_*66*k))
        for j,b in enumerate(BT): a=t*2.6+j*1.05; bat_fly(b,t,(X0+2.7*math.cos(a),Y0+.6+1.2*math.sin(a),3.9+.4*math.sin(t*3+j)),rz=math.degrees(a)+180,ph=j)
        cam2(t,(X0+.45,Y0-4.5,.55),(X0+.4,Y0-4.15,.6),(X0,Y0,2.3),26)
    return dict(upd=upd)
SHOTS['HUNTING']=HUNTING
def DEFEATED():
    sector('ib_night',1.0); B.cyl((28.6,4.9,1.9),.05,3.8,M('#C9CED8',.4,metal=.5),seg=8)
    sign('STREET 42',(28.6,4.82,3.55),.2,'#FFFFFF','#27365A',n=(0,-1,0),e=1.6,pad=.13,th=.04); sign('STREET 44',(28.6,4.82,3.05),.2,'#FFFFFF','#27365A',n=(0,-1,0),e=1.6,pad=.13,th=.04); B.done('st')
    FILLE[0]=120; d=vamp(30.2,4.4,6,'drac'); lamp((30.6,1.8,3.0),170,(.6,.7,1.0))
    def upd(t):
        vstand(d,t,30.2,4.4,6,flap=.3); k=ease(t/.8); d['root'].rotation_euler[0]=R(7*k); d['head'].rotation_euler[0]=R(30*k); fc(d,'sad')
        for s in (1,-1): d['arm'][s].rotation_euler=(R(6*k),0,R(-s*3))
        cam2(t,(30.4,-.9,1.35),(30.3,-.3,1.45),(29.5,4.6,2.7),30)
    return dict(upd=upd)
SHOTS['DEFEATED']=DEFEATED
# ================================================================ Margalla
BN=(-1.5,1.75,0)
def RESTS():
    viewpt(board=False); FILLE[0]=110; d=vamp(*BN,'drac'); d['home']=BN; m=monkey((3.4,.1,0),-110,1.5); lamp((-1.5,4.5,3.4),120,(.6,.7,1.0))
    def upd(t):
        sitp(d,t,seat=.66); cape_flap(d,t,a=2,amp=2); k=ease(t/.8); d['head'].rotation_euler[0]=R(4+14*k); fc(d,'sad'); blink(d,t)
        g=ease(t/1.3); m['root'].location=LV((3.4,.1,0),(.9,.9,0),g); m['root'].rotation_euler[2]=R(-110); monkey_pose(m,t,'run' if g<.97 else 'stand',look=(0,0))
        cam2(t,(-4.9,-1.7,1.6),(-4.6,-1.5,1.65),(-.85,1.6,1.7),28)
    return dict(upd=upd)
SHOTS['RESTS']=RESTS
def MONKEY_():
    viewpt(); FILLE[0]=150; d=vamp(*BN,'drac'); d['home']=BN; m=monkey((.3,1.62,.66),0,1.5)
    def upd(t):
        sitp(d,t,seat=.66); k=ease((t-.72)/.12); g=t<.72; cape_flap(d,t,a=2,amp=2); d['cape'].scale=(1,1,1) if g else (0,0,0); m['cape'].scale=(0,0,0) if g else (1,1,1)
        blink(d,t,force=1) if t<.7 else None; fc(d,'calm' if g else 'shock'); d['head'].rotation_euler=(R(12*(1-k)),0,R(48*k))
        if g: m['root'].location=(.3,1.62,.66); m['root'].rotation_euler[2]=R(55); monkey_pose(m,t,'stand',arm={1:60+70*ease((t-.25)/.3)},look=(10,-10))
        else: q=t-.72; m['root'].location=(.3+5.2*q,1.62-1.3*min(q,.5)*2*.5,.66*max(0,1-q*4)); m['root'].rotation_euler[2]=R(90); monkey_pose(m,t,'run')
        cam2(t,(2.7,-1.7,1.7),(2.6,-1.55,1.72),(-.9,1.7,1.85),34)
    return dict(upd=upd)
SHOTS['MONKEY']=MONKEY_
def WAPAS():
    viewpt(); FILLE[0]=150; d=vamp(-.6,1.0,90,'drac',cap=False)
    def upd(t):
        standp(d,t,-.6,1.0,90); fc(d,'shout'); speak(d,t,207,210,gesture=False); face(d,brow_r=12); pointw(d,1,(7,-1,2.0),ease(t/.2)); d['arm'][-1].rotation_euler=(R(-40-10*math.sin(t*11)),0,R(-24)); d['root'].location[2]=.05*abs(math.sin(t*10))
        c1(t,d,yaw=-38,dist=3.2,lens=36,ref=90,tz=-.3)
    return dict(upd=upd)
SHOTS['WAPAS']=WAPAS
def BETTER():
    viewpt(); FILLE[0]=160; m=monkey((2.3,-2.15,1.65),180,1.5,caped=True); m2=monkey((4.6,-2.15,1.65),160,1.3); lamp((2.6,.6,2.4),90,(1,.86,.62))
    def upd(t):
        monkey_pose(m,t,'stand',arm={1:8,-1:8},look=(0,14)); m['arm'][1].rotation_euler=(R(10),0,R(-55)); m['arm'][-1].rotation_euler=(R(10),0,R(55)); m['cape'].rotation_euler[0]=R(14+8*math.sin(t*5))
        c=abs(math.sin(t*9)); monkey_pose(m2,t,'sit',arm={1:95,-1:95},look=(-30,6)); m2['arm'][1].rotation_euler=(R(-95),0,R(-30*c)); m2['arm'][-1].rotation_euler=(R(-95),0,R(30*c))
        cam2(t,(3.0,2.6,1.15),(3.0,2.2,1.2),(3.1,-2.15,2.75),35)
    return dict(upd=upd)
SHOTS['BETTER']=BETTER
# ================================================================ five a.m.
WKC=[UNCLE,UNCLE2,UNCLE3,WALKA,WALKB,UNCLEQ]; WKP=[(5.0,-1.4),(6.6,.9),(9.2,-.5),(11.6,1.5),(12.6,-1.9),(15.6,.2),(18.4,-1.5),(19.6,1.6),(23,0)]
def walkers(n=9):
    G=[]
    for k in range(n):
        c=WKC[k] if k<6 else dict(person(310+k*7),h=(.95,1.05,1.0)[k%3]); G.append(mk(c,WKP[k][0],WKP[k][1],-90,'wk%d'%k))
    return G
def walkers_go(G,t,v=2.1,x0=0.0):
    for k,H in enumerate(G): H['root'].location[0]=WKP[k][0]+x0-v*t; H['root'].location[1]=WKP[k][1]; H['root'].rotation_euler[2]=R(-90); walk(H,v*t+k*.7,step=.62,arm=62,lean=5); blink(H,t); fc(H,'firm' if k%3 else 'happy')
def FIVEAM():
    track(); FILLE[0]=60; G=walkers(9)
    def upd(t):
        walkers_go(G,t); cam2(t,(-7.5,.3,1.25),(-8.3,.3,1.3),(10,0,2.3),38)
    return dict(upd=upd)
SHOTS['FIVEAM']=FIVEAM
def ATONCE():
    track(); FILLE[0]=110; G=walkers(6)
    def upd(t):
        walkers_go(G,t,x0=-2); x=3.6-2.1*t; camset((x-3.4,-.1,1.9),(x+1.6,-.2,2.2),35,8)
    return dict(upd=upd)
SHOTS['ATONCE']=ATONCE
DV=(-.3,4.6); UA=(1.0,2.5,165); UB=(3.2,1.7,200); UC=(-2.6,1.9,150)
def shadesc(dy=DV[1],cap=False):
    track(); FILLE[0]=120; d=vamp(DV[0],dy,0,'drac',cap=False); G=[mk(UNCLE,*UA,'uncle'),mk(UNCLE2,*UB,'uncle2'),mk(UNCLE3,*UC,'uncle3')]; return d,G
def cower(d,t,k=1.0):
    hands_head(d,k,dx=.7,dz=5.6,dy=-.5); d['root'].rotation_euler[0]=R(-6*k); fc(d,'worry')
def BETA():
    d,G=shadesc(); u,u2,u3=G
    def upd(t):
        standp(d,t,DV[0],DV[1],0); cower(d,t); standp(u,t,*UA); fc(u,'worry'); speak(u,t,228,232,gesture=False); u['arm'][1].rotation_euler=(R(-74+8*math.sin(t*8)),0,R(10)); look_at(u,headw(d),.8)
        for k,H in ((1,u2),(2,u3)): standp(H,t,*(UB if k==1 else UC)); walk(H,1.6*t+k,step=.5,arm=50); look_at(H,headw(d),.8); fc(H,'wow')
        cam2(t,(3.4,4.9,1.9),(3.2,4.7,1.92),(1.0,2.5,1.9),40)
    return dict(upd=upd)
SHOTS['BETA']=BETA
def DHOOP():
    d,G=shadesc(); u,u2,u3=G; steam((DV[0],3.2,3.4),.5,2.0,n=9,seed=3,size=.12)
    def upd(t):
        q=ease(t/DUR*1.1); y=DV[1]-1.5*q; standp(d,t,DV[0],y,0); d['root'].rotation_euler[0]=R(-11); fc(d,'scream')
        for s in (1,-1): d['arm'][s].rotation_euler=(R(-78),0,R(s*10)); d['leg'][s].rotation_euler[0]=R(-14)
        standp(u,t,1.25,y-2.05,180); standp(u2,t,-1.85,y-2.05,180); walk(u,-1.5*q,step=.4,arm=0); walk(u2,-1.5*q,step=.4,arm=0); fc(u,'happy'); fc(u2,'laugh'); speak(u,t,233,235,gesture=False)
        arm_to(u,1,tuple(handw(d,-1)),1,base=(0,0,0)); arm_to(u2,-1,tuple(handw(d,1)),1,base=(0,0,0)); u['arm'][-1].rotation_euler=(R(-150),0,R(-20)); look_at(u,headw(d),.7); look_at(u2,headw(d),.7)
        standp(u3,t,-4.3,y-2.6,205); arms_up(u3,1,t,spread=20,jig=12); fc(u3,'happy')
        cam2(t,(5.0,5.4,2.2),(4.7,5.1,2.25),(.35,y-1.0,2.0),26)
    return dict(upd=upd)
SHOTS['DHOOP']=DHOOP
def NAHI():
    d,G=shadesc(3.1); u,u2,u3=G; steam((DV[0],3.1,3.3),0,2.2,n=12,seed=5,size=.13); steam((DV[0]+.5,3.0,2.9),.1,2.2,n=8,seed=6,size=.1)
    def upd(t):
        standp(d,t,DV[0],3.1,0); d['root'].rotation_euler[0]=R(-11); d['root'].location[0]=DV[0]+.03*math.sin(t*38); fc(d,'scream'); speak(d,t,236,238,gesture=False); face(d,brow_r=-12,eyes=1.3)
        for s in (1,-1): d['arm'][s].rotation_euler=(R(-78),0,R(s*10))
        standp(u,t,1.25,1.05,180); standp(u2,t,-1.85,1.05,180); arm_to(u,1,tuple(handw(d,-1)),1,base=(0,0,0)); arm_to(u2,-1,tuple(handw(d,1)),1,base=(0,0,0)); u3['root'].location=(0,0,-40)
        cam2(t,(-.1,-1.3,2.5),(-.15,-.9,2.5),(DV[0],3.1,1.95),50)
    return dict(upd=upd)
SHOTS['NAHI']=NAHI
def RUNS():
    track(); FILLE[0]=40; P=[(-20.9,2.2),(-23.3,5.8),(-25.6,8.2),(-26,10.4)]; d=vamp(P[0][0],P[0][1],160,'drac',cap=False)
    for k in range(7):
        q=k/7.; pt=LV((P[0][0],P[0][1],2.6),(P[2][0],P[2][1],2.6),q); puff((pt[0]+.3,pt[1]-.3,2.6),.1+q*DUR*.7,size=.3,n=5,col=M('#D8D8DC',.9,alpha=.6),rise=.6,life=.8,seed=k)
    def upd(t):
        walk_path(d,P,t,-.05,DUR-.12,step=.9,arm=60,run_=True,ease_in=.05,ease_out_=.05); fc(d,'scream'); hands_head(d,.8,dx=.7,dz=5.6,dy=-.4)
        if t>DUR-.14: d['root'].location[2]=-40
        cam2(t,(-19.3,.6,1.7),(-19.6,1.1,1.75),(-25,9.2,3.2),24)
    return dict(upd=upd)
SHOTS['RUNS']=RUNS
# ================================================================ the office
DR=(4.9,4.25,0); CK=(-2.6,2.75,0); D2=(2.4,2.75,0)
def ofc(clerk=True,**kw):
    daftar(**kw); FILLE[0]=40; fan=empty((0,.5,4.9)); obox((0,0,.15),(.04,.04,.2),M('#C9CED8',.4,metal=.5),0,fan); obox((0,0,0),(.14,.14,.07),M('#E8E2D0',.5),.03,fan)
    for k in range(3): obox((.75*math.cos(k*2.094),.75*math.sin(k*2.094),0),(.65,.09,.012),M('#E8E2D0',.5),.01,fan,rot=(R(8),0,k*2.094))
    c=None
    if clerk: c=mk(CLERK,*CK,'clerk'); c['home']=CK
    return fan,c
def csleep(c,t): sitp(c,t,seat=.68); c['head'].rotation_euler=(R(34+2*math.sin(t*1.6)),0,R(10)); blink(c,t,force=1); fc(c,'calm'); crossed(c)
def OFFICE():
    fan,c=ofc(); d=vamp(*DR,'drac',cap=False); fl=lamp((4.9,4.6,2.2),0,(1,.85,.6))
    def upd(t):
        fan.rotation_euler[2]=t*1.3; csleep(c,t); standp(d,t,*DR); d['root'].rotation_euler[0]=R(-5); fc(d,'worry'); fl.data.energy=900*(1-ease(t/.35))
        for s in (1,-1): d['arm'][s].rotation_euler=(R(14),0,R(s*26))
        cam2(t,(-1.6,-4.6,2.3),(-1.2,-4.0,2.25),(1.8,3.2,2.0),22)
    return dict(upd=upd)
SHOTS['OFFICE']=OFFICE
def COOL():
    fan,c=ofc(); d=vamp(*DR,'drac',cap=False)
    def upd(t):
        fan.rotation_euler[2]=1.6+t*1.3; csleep(c,t); standp(d,t,*DR); d['root'].rotation_euler[0]=R(-5); k=ease((t-we(252))/.4)
        blink(d,t,force=1) if we(250)+.3<t<we(254) else None; fc(d,'calm' if t>we(250) else 'worry'); d['head'].rotation_euler=(R(-10*(1-k)),0,R(-30*ease((t-we(254)-.1)/.35)))
        for s in (1,-1): d['arm'][s].rotation_euler=(R(14*(1-k)),0,R(s*26*(1-k)))
        c1(t,d,yaw=-16,dist=3.0,lens=38,ref=0,tz=-.3)
    return dict(upd=upd)
SHOTS['COOL']=COOL
def WORKING():
    fan,c=ofc(); jk=obox((2.4,3.16,1.5),(.42,.06,.42),M('#3A3D47',.8,kind='fabric'),.05)
    def upd(t):
        fan.rotation_euler[2]=3.2+t*1.3; csleep(c,t)
        cam2(t,(1.9,-3.4,1.9),(1.2,-3.2,1.9),(-1.0,2.4,1.6),24)
    return dict(upd=upd)
SHOTS['WORKING']=WORKING
def NAYE():
    fan,c=ofc(); cu=cup_of(c,-1); fl=empty((0,0,-9)); obox((0,0,0),(.3,.22,.02),M('#D9C9A0',.8),.005,fl)
    def upd(t):
        fan.rotation_euler[2]=4.6+t*1.3; sitp(c,t,seat=.68); k=ease(t/.3); c['head'].rotation_euler=(R(34*(1-k)),0,R(-16*k)); fc(c,'bored'); speak(c,t,259,266,gesture=False)
        a=ease((t-we(261))/.3)*(1-ease((t-we(263)-.1)/.3)); pointw(c,1,(2.4,1.4,1.3),a) if a>0 else None; hold_chai(c,cu,-1,sip=.9*ease((t-we(266)-.05)/.3))
        fl.location=(-2.0,1.0-.25*ease((t-we(263))/.4),1.09)
        c1(t,c,yaw=14,dist=3.0,lens=38,tz=-.35,ref=0)
    return dict(upd=upd)
SHOTS['NAYE']=NAYE
# ================================================================ one month later
def MONTH():
    sector('ib_noon',0.0,stars=False); FILLE[0]=70; a=mk(AUNTY,AB[0],AB[1],0,'aunty',z=AB[2])
    can=in_hand(a,1,lambda e:(obox((0,-.12,-.05),(.11,.14,.12),M('#2E8A4A',.5),.03,e),obox((0,-.34,.02),(.025,.12,.025),M('#2E8A4A',.5),.01,e,rot=(R(-30),0,0))))
    for k in range(5): B.box((4.2+k*1.1,7.3,3.75),(.2,.14,.16),M('#B8674A',.8),.03); B.ico((4.2+k*1.1,7.3,4.05),.24,M(BOUG[k%4],.85,kind='leaves'),sub=1)
    B.done('pots')
    def upd(t):
        standp(a,t,AB[0],AB[1],0); a['root'].location[2]=AB[2]; hold(a,1,-58+5*math.sin(t*3),z=6); a['head'].rotation_euler[0]=R(16); fc(a,'happy'); blink(a,t)
        cam2(t,(11.8,1.2,3.0),(11.5,1.6,3.2),(7.7,7.6,5.0),40)
    return dict(upd=upd)
SHOTS['MONTH']=MONTH
def deskdrac(**kw):
    fan,c=ofc(files2=False,**kw); d=vamp(*D2,'drac',C=DRAC2,cap=False); d['home']=D2; lanyard(d); fl=empty((0,0,-9)); obox((0,0,0),(.42,.012,.3),M('#C9B48A',.8),.006,fl); obox((0,-.014,0),(.2,.004,.08),M('#F4F1EA',.7),.002,fl)
    st=in_hand(d,1,lambda e:(obox((0,-.05,-.12),(.06,.06,.05),M('#16171C',.5),.01,e),obox((0,-.05,-.03),(.035,.035,.08),M('#6B4A2E',.6),.01,e)))
    return fan,c,d,fl
def BECAUSE():
    fan,c,d,fl=deskdrac(plate=True)
    def upd(t):
        fan.rotation_euler[2]=t*1.3; csleep(c,t); sitp(d,t,seat=.68); fc(d,'calm'); h=headw(d); fl.location=(h.x,h.y-.62,h.z-.05); fl.rotation_euler=(R(-8),0,0)
        for s in (1,-1): arm_to(d,s,(h.x+s*.34,h.y-.6,h.z-.22),1,base=(0,0,0))
        cam2(t,(4.0,-4.4,1.9),(3.6,-3.6,1.9),(2.4,2.2,1.75),30)
    return dict(upd=upd)
SHOTS['BECAUSE']=BECAUSE
def OFFICER():
    fan,c,d,fl=deskdrac(plate=True)
    def upd(t):
        fan.rotation_euler[2]=2+t*1.3; csleep(c,t); sitp(d,t,seat=.68); k=ease((t-.1)/.35); h=headw(d); fl.location=(h.x-.55*k,h.y-.62-.3*k,h.z-.05-.86*k); fl.rotation_euler=(R(-8-80*k),0,R(12*k)); fc(d,'smug')
        arm_to(d,-1,(h.x-.34-.3*k,h.y-.6-.2*k,h.z-.22-.75*k),1,base=(0,0,0)); q=max(0,math.sin((t-we(280))*9))**3 if t>we(279) else 0
        d['arm'][1].rotation_euler=(R(-64+26*q),0,R(-6)) if k>.6 else d['arm'][1].rotation_euler
        if k<=.6: arm_to(d,1,(h.x+.34,h.y-.6,h.z-.22),1,base=(0,0,0))
        cam2(t,(2.9,-2.5,1.75),(2.8,-2.1,1.75),(2.4,2.3,1.72),34)
    return dict(upd=upd)
SHOTS['OFFICER']=OFFICER
def DESK():
    fan,c=ofc(coffin=True,files2=False); jk=obox((2.4,3.16,1.5),(.42,.06,.42),M('#16171C',.8,kind='fabric'),.05); cu=cup_of(c,1)
    def upd(t):
        fan.rotation_euler[2]=t*1.3; sitp(c,t,seat=.68); fc(c,'bored'); hold_chai(c,cu,1,sip=.5+.5*math.sin(t*2)); c['head'].rotation_euler[2]=R(-20)
        cam2(t,(.9,-5.6,2.0),(.6,-5.0,2.0),(-1.0,3.2,1.7),21)
    return dict(upd=upd)
SHOTS['DESK']=DESK
def FITS():
    fan,c=ofc(clerk=False,coffin=True,files2=False); c=mk(CLERK,-2.7,2.9,40,'clerk'); cu=cup_of(c,1)
    def upd(t):
        fan.rotation_euler[2]=3+t*1.3; standp(c,t,-2.7,2.9,40); k=ease((t-.15)/.3); hold_chai(c,cu,1,a=-62-50*k); fc(c,'happy'); c['head'].rotation_euler[2]=R(28*k)
        cam2(t,(-3.0,-1.6,1.8),(-3.1,-1.2,1.8),(-3.6,3.4,1.75),30)
    return dict(upd=upd)
SHOTS['FITS']=FITS
# ================================================================ the werewolf
WF=(2.0,.2)
def WOLF_():
    sector('ib_night',1.0); FILLE[0]=130; w=mk(WOLF,WF[0],WF[1],0,'wolf'); wolfify(w); lamp((3.2,-2.6,3.2),200,(.6,.7,1.0)); lamp((1.2,-2.4,3.3),320,(1,.9,.76)); fl=lamp((2,-3,5),0,(.8,.85,1.0))
    def upd(t):
        k=ease((t-.35)/.4); standp(w,t,WF[0],WF[1],0); w['head'].rotation_euler[0]=R(-16*k); fc(w,'shout')
        claws(w,t,k)
        w['root'].rotation_euler[0]=R(-8*k); fl.data.energy=24000 if 1.0<t<1.07 else 0
        cam2(t,(.7,-4.4,1.2),(.9,-3.8,1.3),(2.0,.2,2.7),28)
    return dict(upd=upd)
SHOTS['WOLF']=WOLF_
def tiffin(H,s=-1): return in_hand(H,s,lambda e:(ocyl((0,0,-.2),.1,.12,M('#C9CED8',.25,metal=.9),e,rot=(0,0,0),seg=12),ocyl((0,0,-.33),.1,.12,M('#C9CED8',.25,metal=.9),e,rot=(0,0,0),seg=12),obox((0,0,-.12),(.02,.11,.05),M('#C9CED8',.3,metal=.8),.005,e)))
def NAU2():
    sector('ib_night',1.0); FILLE[0]=130; d=vamp(5.6,-.9,-30,'drac',C=DRAC2,cap=False); lanyard(d); tiffin(d,-1); ph=phone_of(d,1); w=mk(WOLF,WF[0],WF[1],0,'wolf'); wolfify(w); lamp((6.6,-3.4,3.0),200,(.6,.7,1.0))
    def upd(t):
        standp(d,t,5.6,-.9,-30); fc(d,'bored'); speak(d,t,303,309,gesture=False); k=ease((t-.05)/.3)*(1-ease((t-we(306)-.15)/.3)); phone_up(d,1,k,h=3.5,fw=1.3,sx=.5); d['head'].rotation_euler[2]=R(-40*(1-k)); d['arm'][-1].rotation_euler=(0,0,0)
        standp(w,t,WF[0],WF[1],0); fc(w,'sad')
        c1(t,d,yaw=-35,dist=3.0,lens=40,ref=-30)
    return dict(upd=upd)
SHOTS['NAU2']=NAU2
def SURVIVE():
    sector('ib_night',1.0); FILLE[0]=140; wa=mk(WALEED,7.0,-.8,0,'waleed'); d=vamp(5.4,1.4,-14,'drac',C=DRAC2,cap=False); lanyard(d); tiffin(d,-1); w=mk(WOLF,8.6,1.4,14,'wolf'); wolfify(w)
    m=monkey((5.9,6.2,1.99),0,1.4,caped=True); a=mk(AUNTY,AB[0],AB[1],0,'aunty',z=AB[2]); lp=lightpane(); lamp((7,-3.5,3.4),260,(.6,.7,1.0)); lamp((6.5,5.0,4.2),120,(1,.86,.62))
    def upd(t):
        standp(wa,t,7.0,-.8,0); fc(wa,'happy'); speak(wa,t,310,317,gesture=False); k=ease((t-ws(311)+.1)/.25); what_pose(wa,(1-k)*ease(t/.3),t,.5)
        if k>0: wa['arm'][1].rotation_euler=(R(-86*k),0,R(4)); wa['arm'][-1].rotation_euler=(R(-4),0,0)
        standp(d,t,5.4,1.4,-14); crossed(d); fc(d,'smug'); standp(w,t,8.6,1.4,14); fc(w,'sad'); w['head'].rotation_euler[0]=R(18); monkey_pose(m,t,'sit',look=(0,-8)); standp(a,t,AB[0],AB[1],0); a['root'].location[2]=AB[2]; a['head'].rotation_euler[0]=R(24); fc(a,'firm'); crossed(a)
        cam2(t,(7.0,-5.7,1.9),(7.0,-5.3,1.9),(7.0,1.0,1.6),30)
    return dict(upd=upd)
SHOTS['SURVIVE']=SURVIVE
