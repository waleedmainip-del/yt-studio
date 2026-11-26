# World Auctions Arena demo - shots. PLACE = "option 1" placement clip, the rest = "option 2" story teaser.
SEQ=[('PLACE', 0.0), ('HOOK', 4.0), ('EXCEPT', 6.333), ('STAGE', 7.467), ('LOOK', 9.533), ('AUCT', 10.467), ('BIDS', 11.467), ('RAISED', 12.7), ('WASH', 14.7), ('GAVEL', 16.533), ('P27', 18.1), ('FIVE', 19.9), ('ABBU', 22.033), ('ENDWIDE', 23.6), ('CAREFUL', 25.767)]
END=28.5333
WI={'PLACE': -1, 'HOOK': 0, 'EXCEPT': 6, 'STAGE': 8, 'LOOK': 16, 'AUCT': 18, 'BIDS': 20, 'RAISED': 22, 'WASH': 27, 'GAVEL': 31, 'P27': 34, 'FIVE': 37, 'ABBU': 42, 'ENDWIDE': 46, 'CAREFUL': 50}
SHOTS={}
SEATA=[(2.2,-1.0),(4.5,-1.0),(-2.2,-1.0),(-4.5,-1.0),(2.2,-3.8),(4.5,-3.8),(-2.2,-3.8),(-4.5,-3.8),(2.2,-6.6),(4.5,-6.6),(-2.2,-6.6),(-4.5,-6.6)]
PNUM=['27','12','41','08','19','33','05','16','22','30','11','07']
STAGEP=(TTX,TTY,2.4)
def paddle(num):
    """bidding paddle (free object, placed at a hand each frame): number readable from both sides"""
    e=empty((0,0,-5)); ocyl((0,0,.18),.035,.5,M('#5A3A22',.5,kind='wood'),e,rot=(0,0,0),seg=8)
    ocyl((0,0,.62),.33,.04,M('#F4F1EA',.5),e,seg=24); ocyl((0,0,.62),.36,.03,M(GOLD,.3,metal=.8),e,seg=24)
    for n in ((0,-1,0),(0,1,0)): text(num,(0,n[1]*.03,.62),n,.36,M('#16171C',.5),ex=.004,parent=e)
    return e
def gavel():
    e=empty((0,0,-5)); wm=M('#6B3A1E',.4,kind='wood'); ocyl((0,0,.2),.03,.5,wm,e,rot=(0,0,0),seg=8); ocyl((0,0,.45),.09,.3,wm,e,rot=(0,R(90),0),seg=12)
    for sx in (-1,1): ocyl((sx*.13,0,.45),.095,.03,M(GOLD,.3,metal=.8),e,rot=(0,R(90),0),seg=12)
    return e
def note500():
    e=empty((0,0,-5)); obox((0,0,.16),(.3,.006,.14),M('#2E8A5A',.6),.0,e); obox((0,0,.16),(.26,.008,.1),M('#BFE6C8',.6),0,e)
    for n in ((0,-1,0),(0,1,0)): text('500',(0,n[1]*.012,.16),n,.15,M('#14402A',.5),ex=.002,parent=e)
    return e
def arena_set(n=12):
    Ar=arena(); A=dict(ar=Ar,aud=[],pad=[])
    for i,(x,y) in enumerate(SEATA[:n]):
        vchair(x,y,180,['#7A1F2E','#5A1626'][(i//2)%2]); H=mk(ACAST[i],x,y,180,'a%d'%i); H['home']=(x,y,180); A['aud'].append(H); A['pad'].append(paddle(PNUM[i]))
    A['wa']=A['aud'][0]; A['seth']=A['aud'][1]
    A['au']=mk(AUCT,PX,PY+1.0,0,'auct',z=STG); A['gv']=gavel(); FILLE[0]=30; return A
def turn(A,t): A['ar']['tt'].rotation_euler[2]=R(25+(T0+t)*16)
def pad_set(A,i,k=0.0,t=0.0,wob=0.0,s=-1):
    H=A['aud'][i]; H['arm'][s].rotation_euler=(R(L(-40,-168,k)+wob*3*math.sin(t*9+i)),R(s*(-4+9*k)),0)
    p=A['pad'][i]; p.location=handw(H,s); p.rotation_euler=(R(-78*(1-ease(k*3.2))),0,R(6*math.sin(t*7+i)*wob*k))
def aud_idle(A,t,m='watch',look=None,skip=()):
    for i,H in enumerate(A['aud']):
        if i in skip: continue
        sitp(H,t,seat=.56,lean=2); look_at(H,look or STAGEP,1.0,maxyaw=70,maxpitch=30); mood(H,m); pad_set(A,i,0.0,t)
def clap(H,t,ph=0.0):
    c=abs(math.sin(t*13+ph))
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-72),R(-s*(10+16*c)),0)
def auct_idle(A,t,m='calm'):
    au=A['au']; standp(au,t,PX,PY+1.0,0); mood(au,m); au['arm'][1].rotation_euler=(R(-62),R(6),0); gv=A['gv']; gv.location=handw(au,1); gv.rotation_euler=(R(40),0,0)
def wal_sit(A,t,k=0.0,wob=0.0):
    wa=A['wa']; sitp(wa,t,seat=.56,lean=0); pad_set(A,0,k,t,wob)
# ---------------------------------------------------------------- option 1: brand placement inside a normal street scene
def PLACE():
    W=mohalla('P',seed=3); gantry(10.0,9.4); FILLE[0]=0
    def upd(t):
        q=ease(t/DUR); camset(LV((-9,-.6,8.2),(-4.6,-.4,9.7),q),LV((10,0,10.4),(10,0,11.0),q),24,8)
    return dict(upd=upd)
SHOTS['PLACE']=PLACE
# ---------------------------------------------------------------- option 2: the story teaser
def HOOK():
    A=arena_set()
    def upd(t):
        scr_show(A['ar'],'brand'); turn(A,t); aud_idle(A,t,'calm'); wal_sit(A,t); mood(A['wa'],'tense'); auct_idle(A,t)
        q=ease(t/DUR); camset(LV((0,-12.2,4.9),(0,-10.4,4.1),q),(.4,7.0,3.5),20,8)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
def EXCEPT():
    A=arena_set(8); wa=A['wa']
    def upd(t):
        scr_show(A['ar'],'brand'); turn(A,t); aud_idle(A,t,'calm'); wal_sit(A,t); auct_idle(A,t)
        look_at(wa,(2.2+7*math.sin(t*4.2),6,2.6),1.0,maxyaw=55); face(wa,mouth='flat',brow=.05,brow_r=0,eyes=1.15)
        q=ease(t/DUR); camset(LV((1.2,3.0,2.05),(1.3,2.6,2.0),q),(1.92,-1.0,1.72),38,8)
    return dict(upd=upd)
SHOTS['EXCEPT']=EXCEPT
def STAGE():
    A=arena_set(4)
    def upd(t):
        scr_show(A['ar'],'brand'); turn(A,t); aud_idle(A,t,'calm'); wal_sit(A,t); auct_idle(A,t)
        q=ease(t/DUR); camset(LV((0,-2.6,1.85),(.1,-1.3,1.9),q),(1.3,7.3,2.7),19,8)
    return dict(upd=upd)
SHOTS['STAGE']=STAGE
def LOOK():
    A=arena_set(8); wa=A['wa']
    def upd(t):
        scr_show(A['ar'],'brand'); turn(A,t); aud_idle(A,t,'calm'); wal_sit(A,t); auct_idle(A,t); wa['root'].rotation_euler[0]=R(9*ease(t/.4))
        look_at(wa,STAGEP,1.0); face(wa,mouth='grin' if t>.35 else 'o',brow=.06,eyes=1.3)
        q=ease(t/DUR); camset(LV((2.55,1.75,1.9),(2.5,1.5,1.88),q),(2.2,-.85,1.74),42,8)
    return dict(upd=upd)
SHOTS['LOOK']=LOOK
def AUCT_():
    A=arena_set(4); au=A['au']; gv=A['gv']
    def upd(t):
        scr_show(A['ar'],'lot'); turn(A,t); aud_idle(A,t,'watch'); wal_sit(A,t); standp(au,t,PX,PY+1.0,0); mood(au,'shout'); speak(au,t,18,19,gesture=False)
        sw=math.sin(t*5.5); look_at(au,(4*sw,-3,2),1.0,maxyaw=50); au['arm'][-1].rotation_euler=(R(-78),R(-(20+26*sw)),0)
        au['arm'][1].rotation_euler=(R(-95+10*math.sin(t*9)),R(8),0); gv.location=handw(au,1); gv.rotation_euler=(R(20),0,0)
        q=ease(t/DUR); camset(LV((-4.5,1.9,2.75),(-4.7,2.3,2.75),q),(PX+.1,PY+1.0,STG+1.9),32,8)
    return dict(upd=upd)
SHOTS['AUCT']=AUCT_
def BIDS():
    A=arena_set(); wa=A['wa']; ORD=[(1,.08),(4,.36),(5,.6),(9,.8)]
    def upd(t):
        scr_show(A['ar'],'three'); turn(A,t); aud_idle(A,t,'watch'); wal_sit(A,t); auct_idle(A,t,'shout')
        for i,t0 in ORD:
            k=ease(tl(t,t0,t0+.16)); pad_set(A,i,k,t,1.0);
            if k>.3: mood(A['aud'][i],'happy')
        look_at(wa,(2.2+8*math.sin(t*5.5),-1.0,2.9),1.0,maxyaw=75); face(wa,mouth='o',brow=.05,brow_r=-8,eyes=1.2)
        q=ease(t/DUR); camset(LV((-.3,3.5,2.9),(-.1,3.2,2.85),q),(3.75,-2.2,1.95),26,8)
    return dict(upd=upd)
SHOTS['BIDS']=BIDS
def RAISED():
    A=arena_set(8); wa,se=A['wa'],A['seth']; t1=ws(24)-.12
    def upd(t):
        scr_show(A['ar'],'three'); turn(A,t); aud_idle(A,t,'watch'); auct_idle(A,t,'shout'); k=ease(tl(t,t1,t1+.4)); wal_sit(A,t,k,1.0)
        look_at(wa,hp(se),k,maxyaw=42); face(wa,mouth='flat',brow=.05,brow_r=-8,eyes=1.1); wa['root'].rotation_euler[1]=R(-5*k)
        look_at(se,hp(wa),ease(tl(t,t1+.3,t1+.6)),maxyaw=50)
        q=ease(t/DUR); camset(LV((3.35,4.4,3.3),(3.35,4.0,3.2),q),(3.35,-1.6,1.75),30,8)
    return dict(upd=upd)
SHOTS['RAISED']=RAISED
def WASH():
    A=arena_set(8); wa,se=A['wa'],A['seth']
    def upd(t):
        scr_show(A['ar'],'three'); turn(A,t); aud_idle(A,t,'watch'); auct_idle(A,t,'shout'); wal_sit(A,t,1.0,1.0); wa['root'].rotation_euler[1]=R(-5)
        look_at(wa,hp(se),1.0,maxyaw=38); face(wa,brow=.05,brow_r=-8,eyes=1.1); speak(wa,t,27,30,gesture=False)
        q=ease(t/DUR); camset(LV((2.8,3.3,2.4),(2.76,3.0,2.38),q),(2.48,-1.0,2.3),30,8)
    return dict(upd=upd)
SHOTS['WASH']=WASH
def GAVEL():
    A=arena_set(4); au=A['au']; gv=A['gv']; t1=ws(31)-.02; t2=ws(34)-.1
    def upd(t):
        turn(A,t); aud_idle(A,t,'watch'); wal_sit(A,t,1.0,1.0); standp(au,t,PX,PY+1.0,0); mood(au,'shout'); speak(au,t,31,36,gesture=False)
        up=ease(tl(t,t1-.3,t1-.08)); dn=tl(t,t1-.06,t1+.03); scr_show(A['ar'],'sold' if dn>=1 else 'three')
        a=L(-62,-150,up)*(1-dn)+(-64)*dn; au['arm'][1].rotation_euler=(R(a),R(6),0); gv.location=handw(au,1); gv.rotation_euler=(R(L(40*(1-up),90,dn)),0,0)
        p=ease(tl(t,t2,t2+.2)); look_at(au,(2.2,-1.0,2.6),1.0,maxyaw=60)
        if p>0: pointw(au,-1,(2.2,-1.0,2.9),p)
        SHAKE[0]=.035*max(0,1-abs(t-t1-.05)/.12)
        q=ease(t/DUR); camset(LV((-4.2,2.2,2.9),(-4.35,2.6,2.9),q),(PX+.12,PY+.8,STG+1.75),34,8)
    return dict(upd=upd)
SHOTS['GAVEL']=GAVEL
def P27():
    A=arena_set(4); wa=A['wa']
    def upd(t):
        SHAKE[0]=0; scr_show(A['ar'],'sold'); turn(A,t); aud_idle(A,t,'watch'); wal_sit(A,t,1.0,.4); auct_idle(A,t,'happy'); pointw(A['au'],-1,(2.2,-1.0,2.9),1.0)
        look_at(wa,(0,10.7,5.9),1.0,maxpitch=30)
        for i in (1,2,3): look_at(A['aud'][i],hp(wa),1.0,maxyaw=80)
        q=ease(t/DUR); camset(LV((.9,-4.5,2.75),(.9,-4.1,2.77),q),(2.46,5.58,3.3),19,8)
    return dict(upd=upd)
SHOTS['P27']=P27
def FIVE():
    A=arena_set(8); wa=A['wa']; nt=note500()
    def upd(t):
        scr_show(A['ar'],'sold'); turn(A,t); aud_idle(A,t,'happy'); auct_idle(A,t,'happy'); wal_sit(A,t,1.0,0.0)
        for i in range(1,8): clap(A['aud'][i],t,i*.7); look_at(A['aud'][i],hp(wa),1.0,maxyaw=80)
        k=ease(tl(t,.35,.8)); arm_to(wa,1,(1.95,-.4,1.22),k,base=(R(-40),R(-4),0)); nt.location=Vector(handw(wa,1))+Vector((0,.12,.1)); nt.rotation_euler=(0,0,0); nt.scale=tuple(3*[1.3*k])
        look_at(wa,Vector(handw(wa,1))+Vector((0,0,.3)),k,maxpitch=14); face(wa,mouth='O',brow=.07,brow_r=-14,eyes=1.3)
        q=ease(t/DUR); camset(LV((2.5,2.9,2.15),(2.45,2.5,2.12),q),(2.4,-1.0,2.1),34,8)
    return dict(upd=upd)
SHOTS['FIVE']=FIVE
def ABBU_():
    A=arena_set(8); wa=A['wa']; dr=[oico((0,0,-5),.035,M('#9FD8FF',.2,emit=.8),None,sub=1) for k in range(3)]
    def upd(t):
        scr_show(A['ar'],'sold'); turn(A,t); aud_idle(A,t,'happy'); auct_idle(A,t,'happy'); wal_sit(A,t,1.0,0.0)
        for i in range(1,8): clap(A['aud'][i],t,i*.7)
        face(wa,brow=.07,brow_r=-14,eyes=1.25); speak(wa,t,42,45,gesture=False); wa['root'].location[0]+=.01*math.sin(t*30)
        bpy.context.view_layer.update(); h=Vector(hp(wa))
        for k,o in enumerate(dr):
            q=((t*1.2+k*.37)%1.0); o.location=(h.x+(-.36,.38,-.3)[k],h.y+.3,h.z+.22-.5*q); o.scale=tuple(3*[1-q*.5])
        q=ease(t/DUR); camset(LV((2.5,1.7,1.88),(2.45,1.45,1.86),q),(2.2,-.9,1.76),46,8)
    return dict(upd=upd)
SHOTS['ABBU']=ABBU_
def ENDWIDE():
    A=arena_set(); wa=A['wa']
    def upd(t):
        scr_show(A['ar'],'brand'); turn(A,t); aud_idle(A,t,'happy'); auct_idle(A,t,'happy'); wal_sit(A,t,1.0,0.0)
        for i in range(1,12): clap(A['aud'][i],t,i*.7)
        q=ease(t/DUR); camset(LV((-.8,-11.6,3.6),(0,-12.4,6.2),q),(.4,7.0,3.8),19,8)
    return dict(upd=upd)
SHOTS['ENDWIDE']=ENDWIDE
def CAREFUL():
    A=arena_set(8); wa=A['wa']
    def upd(t):
        scr_show(A['ar'],'brand'); turn(A,t); aud_idle(A,t,'calm'); auct_idle(A,t,'calm'); k=ease(tl(t,0,.3)); wal_sit(A,t,0.0,0.0)
        for s in (1,-1): wa['arm'][s].rotation_euler=(R(14),R(-s*7),0)                         # sitting on his own hands
        A['pad'][0].location=(0,0,-5); look_at(wa,(2.2+9*math.sin(t*3.6),6,2.2),1.0,maxyaw=45); face(wa,mouth='strain',brow=.06,brow_r=-12,eyes=1.2)
        wa['root'].location[2]+=.01*math.sin(t*18)
        q=ease(t/DUR); camset(LV((1.75,3.0,2.05),(1.75,2.6,2.0),q),(1.95,-1.0,1.78),36,8)
    return dict(upd=upd)
SHOTS['CAREFUL']=CAREFUL
