# Shots for "Khana Khul Gaya". SEQ/END are filled by gen_seq.py.
SHOTS={}
END=87.4
SEQ=[('HOOK', 0.0), ('KHANA0', 4.0), ('HALL', 5.567), ('AMMI', 13.033), ('MISSION', 17.0), ('WHISPER', 19.5), ('CHAOS', 20.8), ('PLATES', 25.367), ('ASK', 31.067), ('UNBORN', 32.567), ('BILAL', 36.0), ('DAIG', 40.7), ('QORMA', 47.8), ('UNCLE', 56.733), ('WTRICK', 59.067), ('RUNOFF', 61.867), ('WIN', 66.133), ('WALKBACK', 67.733), ('VIP', 74.633), ('WREPLY', 78.0), ('AMMI2', 80.567), ('CTA', 83.867)]
import os as _os
FILLE=[30.0]; _FL=[]
_camset0=camset
def camset(loc,tg,lens,*a,**k):
    _camset0(loc,tg,lens,*a,**k)
    if not _FL: _FL.append(point((0,0,0),FILLE[0],(1,.93,.85),r=.4,shadow=False))
    v=Vector(tg)-Vector(loc); _FL[0].location=Vector(loc)+Vector((0,0,.3)); _FL[0].data.energy=FILLE[0]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0
def we(i): return W_[i]['e']-T0
def mk(C,x,y,rz,name,z=0.0): return avatar_bg((x,y,z),rz,C,name=name)
def fwd(rz): return (math.sin(R(rz)),-math.cos(R(rz)))
def drift(c0,tg,t,a=.06): q=ease(t/DUR); return LV(c0,(L(c0[0],tg[0],a),L(c0[1],tg[1],a),c0[2]),q)
def closecam(H,rz,side=.3,dist=3.0,dz=.05,tz=-.3,lens=36):
    h=hp(H); f=fwd(rz); rt=(-f[1],f[0])
    return (h[0]+f[0]*dist+rt[0]*side,h[1]+f[1]*dist+rt[1]*side,h[2]+dz),(h[0],h[1],h[2]+tz),lens
def hall_set(open_k=0.0):
    hall(); _S,_A,_w,_bg=setup_interior('evening',room=(0,0,HH),res=PCT,samples=SAMPLES,shadow_dist=24); _A.data.energy*=.45
    cs=curtain_obj(open_k); return cs
def plate(parent=None,loc=(0,0,0),food=None):
    e=empty(loc,parent); ocyl((0,0,0),.15,.015,M('#F7F5EF',.2),e,rot=(0,0,0))
    if food=='leg': obox((0,0,.03),(.07,.04,.025),M('#8A3A1A',.6),.02,e); ocyl((.08,0,.03),.012,.06,M('#F4EAD0',.4),e,rot=(0,R(90),0))
    if food=='legs3':
        for k in range(3): obox(((k-1)*.07,(k%2)*.03,.03),(.05,.03,.022),M('#8A3A1A',.6),.015,e)
    return e
def ots(sp,ls,back=2.2,lens=28):
    a=Vector(hp(sp)); b=Vector(hp(ls)); d=(b-a); dl=d.length; d.z=0; d.normalize(); pr=Vector((-d.y,d.x,0))
    if pr.y>0: pr=-pr
    m=(a+b)/2; c=m+pr*back+d*(.35*dl)+Vector((0,0,.05)); tg=a.lerp(b,.25); return (c.x,c.y,c.z),(tg.x,tg.y,tg.z-.35),lens
def twoshot(A,B,back=2.6,lens=26):
    a=Vector(hp(A)); b=Vector(hp(B)); m=(a+b)/2; d=b-a; d.z=0; d.normalize(); pr=Vector((-d.y,d.x,0))
    if pr.y>0: pr=-pr
    c=m+pr*back+Vector((0,0,.05)); return (c.x,c.y,c.z),(m.x,m.y,m.z-.35),lens
def hold(H,obj,s=1,dz=0.0):
    obj.location=H['arm'][s].matrix_world@Vector(hand_loc(H,s))+Vector((0,0,dz))
def present(H,s,k=1.0,z=3.3,x=.3,y=-1.4):
    u=H['u']; arm_to(H,s,root_mat(H)@Vector((s*x*u,y*u,z*u)),k)
# seated guests around tables
def seated(n=12,seed=1,tables=None,skip=()):
    r=random.Random(seed); P=[]; i=0
    for ti,(tx,ty) in enumerate(tables or TABLES[:6]):
        seats=round_table(tx,ty,6,seed=ti) if False else [(tx+1.45*math.sin(R(a)),ty-1.45*math.cos(R(a)),a) for a in range(0,360,60)]
        for j,(x,y,a) in enumerate(seats):
            chair(x,y,a+180)
            if i<n and (ti,j) not in skip and r.random()<.75:
                H=mk(GUESTS[(i+seed)%len(GUESTS)],x,y,a,'g%d_%d'%(ti,j)); H['seat']=(x,y,a); H['ph']=r.uniform(0,6); P.append(H); i+=1
    return P
def tables_only(tabs):
    for ti,(tx,ty) in enumerate(tabs): round_table(tx,ty,6)
def sit_all(P,t,react=None):
    for H in P:
        seat(H,t,.5); x,y,a=H['seat']; H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(a)); blink(H,t)
        if react: react(H,t)
        else: face(H,mouth='smile' if math.sin(t*.8+H['ph'])>-.3 else 'grin',brow=.02)
# ================================================================ HOOK / HALL
def HOOK():
    cs=hall_set(); tables_only(TABLES[:6]); P=seated(14,1)
    w=mk(WAITER,-9,4.0,90,'waiter')
    def upd(t):
        sit_all(P,t); q=ease(t/DUR)
        stand(w,t); blink(w,t); face(w,mouth='smile'); w['root'].location=(L(-9,-3,q),4.0,0); walk(w,q*6,step=.5)
        camset(LV((0,-9.0,3.4),(0,-7.6,2.9),q),LV((0,2,1.5),(0,3,1.6),q),20,6)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
def KHANA0():
    cs=hall_set(); tables_only(TABLES[:6]); P=seated(14,1); un=mk(UNCLE,-2.4,.6,180,'uncle')
    def upd(t):
        stand(un,t); blink(un,t); un['root'].rotation_euler[2]=R(150); u=un['u']
        un['root'].rotation_euler[0]=R(7); talk(un,t,*wt(12,15),rest='flat'); face(un,eyes=1.3,brow=.07)
        k=tl(t,ws(14),ws(15)+.2)
        sit_all(P,t,react=lambda H,t: (face(H,mouth='O',eyes=1.0+.4*k,brow=.06*k),look_at(H,(0,CURT_Y,1.6),.8*k)))
        c0,tg,ln=closecam(un,150,.35,2.2,lens=30,tz=-.35); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['KHANA0']=KHANA0
def HALL():
    cs=hall_set(); tables_only(TABLES[:6]); P=seated(14,1)
    def upd(t):
        k=tl(t,ws(29)-.2,ws(31)+.2)
        sit_all(P,t,react=lambda H,t: (face(H,mouth='smile',brow=.02),look_at(H,(0,CURT_Y,2.0),.85*k)))
        q=ease(t/DUR)
        if t<ws(29)-.1: camset(LV((-10.5,-8.5,4.6),(-9.5,-7.5,4.2),q),(0,0,1.2),18,6)
        else: q2=tl(t,ws(29)-.1,DUR); camset(LV((3.0,-3.4,1.35),(3.0,.4,1.45),q2),(0,CURT_Y,2.2),24,6)
    return dict(upd=upd)
SHOTS['HALL']=HALL
WT=(-6,1.8)   # Waleed & Ammi's table (TABLES[5])
def AMMI_():
    cs=hall_set(); tables_only([WT,(-6,-1.5),(0,1.8)]); am=mk(AMMI,0,0,0,'ammi'); wa=mk(WALEED,0,0,0,'wa')
    sa=(WT[0]+1.45*math.sin(R(120)),WT[1]-1.45*math.cos(R(120)),120); sw=(WT[0]+1.45*math.sin(R(60)),WT[1]-1.45*math.cos(R(60)),60)
    chair(*sa[:2],sa[2]+180); chair(*sw[:2],sw[2]+180)
    def upd(t):
        for H,(x,y,a) in ((am,sa),(wa,sw)): seat(H,t,.5); H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(a)); blink(H,t)
        am['root'].rotation_euler[2]=R(120-35); wa['root'].rotation_euler[2]=R(60+35)
        talk(am,t,*wt(37,48),rest='smile'); face(am,brow=.04); look_at(am,hp(wa),.7); look_at(wa,hp(am),.7); face(wa,mouth='flat',brow=.03)
        u=am['u']; arm_to(am,1,root_mat(am)@Vector((.3*u,-1.4*u,3.2*u)),tl(t,ws(40),ws(41)))
        c0,tg,ln=closecam(am,120-35,-.3,2.5,lens=30,tz=-.4); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['AMMI']=AMMI_
def MISSION():
    cs=hall_set(); tables_only([WT,(-6,-1.5),(0,1.8)]); wa=mk(WALEED,0,0,0,'wa'); sw=(WT[0]+1.45*math.sin(R(60)),WT[1]-1.45*math.cos(R(60)),60); chair(*sw[:2],sw[2]+180)
    w=mk(WAITER,.6,CURT_Y-.55,0,'waiter')
    def upd(t):
        seat(wa,t,.5); wa['root'].location=(sw[0],sw[1],0); wa['root'].rotation_euler=(0,0,R(60+35)); blink(wa,t)
        k=tl(t,.0,.4); face(wa,mouth='flat',brow=-.06,brow_r=-14,eyes=.8); wa['head'].rotation_euler[0]=R(-4*k)
        stand(w,t); blink(w,t); w['root'].rotation_euler[2]=R(180); kc=tl(t,we(52)+.2,we(52)+.6); arm_to(w,1,Vector((.3,CURT_Y-.05,1.6)),kc)
        if t<we(52)+.15: c0,tg,ln=closecam(wa,60+35,0,1.9,lens=32,tz=-.4); camset(drift(c0,tg,t,.15),tg,ln,2.8)
        else: camset((1.6,CURT_Y-3.6,1.7),(.4,CURT_Y,1.55),26,4)
    return dict(upd=upd)
SHOTS['MISSION']=MISSION
def WHISPER():
    cs=hall_set(); tables_only([(0,1.8),(-6,1.8),(6,1.8)]); P=seated(8,3,tables=[(0,1.8),(6,1.8)]); un=mk(UNCLE,-2.2,3.6,180,'uncle')
    def upd(t):
        stand(un,t); blink(un,t); un['root'].rotation_euler[2]=R(200); u=un['u']; pass
        talk(un,t,*wt(53,56),rest='O'); face(un,eyes=1.35,brow=.08); un['root'].rotation_euler[0]=R(6)
        k=tl(t,ws(56),ws(56)+.4)
        sit_all(P,t,react=lambda H,t: (face(H,mouth='O',eyes=1+.5*k,brow=.07*k),look_at(H,(0,CURT_Y,1.6),.8*k)))
        c0,tg,ln=closecam(un,200,.0,1.6,lens=26,tz=-.35); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['WHISPER']=WHISPER
def CHAOS():
    cs=hall_set(0.0); tables_only([(-6,-1.5),(0,-1.5),(6,-1.5),(-6,1.8),(0,1.8),(6,1.8)])
    r=random.Random(5); RUN=[]; CH=[]; STAND=[]
    for i,(tx,ty) in enumerate([(-6,1.8),(0,1.8),(6,1.8)]):
        for j,a in enumerate((120,180,240)):
            x=tx+1.45*math.sin(R(a)); y=ty-1.45*math.cos(R(a)); c=chair(x,y,a+180); H=mk(GUESTS[(i*3+j)%len(GUESTS)],x,y,a,'r%d%d'%(i,j))
            lx=tx+(1.6 if j==0 else -1.6 if j==2 else 0); pts=[(x,y),(lx,y+.25),(lx,5.0)] if j!=1 else [(x,y),(x,5.0)]
            RUN.append((H,pts,(.05 if j==1 else .3)+r.uniform(0,.15),a)); CH.append((c,a,.1+r.uniform(0,.2),r.choice([-1,1])))
    for i,(tx,ty) in enumerate([(-6,-1.5),(0,-1.5),(6,-1.5)]):
        for j,a in enumerate((90,180,270)):
            x=tx+1.45*math.sin(R(a)); y=ty-1.45*math.cos(R(a)); chair(x,y,a+180); H=mk(GUESTS[(9+i*3+j)%len(GUESTS)],x,y,a,'s%d%d'%(i,j)); H['ph']=r.uniform(0,6); STAND.append((H,x,y,a))
    def upd(t):
        cs(tl(t,-.5,.6))
        for H,pts,d0,a in RUN:
            if t<d0+.25: seat(H,t,.5); H['root'].location=(pts[0][0],pts[0][1],0); H['root'].rotation_euler=(0,0,R(a)); face(H,mouth='O',eyes=1.3)
            else: walk_path(H,pts,t,d0+.25,DUR-.1,run_=True,ease_in=.1,ease_out_=.15); face(H,mouth='grin',brow=-.06,brow_r=-12)
            blink(H,t)
        for H,x,y,a in STAND:
            k=tl(t,.2+H['ph']*.05,.6+H['ph']*.05)
            if k<.5: seat(H,t,.5)
            else: stand(H,t)
            H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(L(a,180,k))); blink(H,t); face(H,mouth='O',eyes=1.3,brow=.06)
            H['arm'][1].rotation_euler=(R(-150*k),0,R(10))
        for c,a,d0,sg in CH:
            k=tl(t,d0+.25,d0+.6); c.rotation_euler=(R(-82*k),0,R(a+180+sg*20*k))
        q=ease(t/DUR); camset(LV((7.5,-4.5,3.2),(6.8,-3.8,3.0),q),(0,2.2,1.0),20,6)
    return dict(upd=upd)
SHOTS['CHAOS']=CHAOS
# --------------------------------------------------------------- buffet battles
def buffet_set(n=8,seed=7,avoid=()):
    cs=hall_set(1.0); r=random.Random(seed); P=[]
    for k in range(n):
        x=-10+k*20/(n-1)+r.uniform(-.2,.2)
        if any(abs(x-a)<1.0 for a in avoid): continue
        H=mk(GUESTS[(k+seed)%len(GUESTS)],x,BUF_Y-1.0-r.choice([0,.0,1.0]),0,'b%d'%k); H['root'].rotation_euler[2]=R(180); H['ph']=r.uniform(0,6); P.append(H)
    return P
def jostle(P,t):
    for H in P:
        stand(H,t); blink(H,t); b=math.sin(t*6+H['ph']); H['root'].rotation_euler=(0,R(4*b),R(180+10*b)); face(H,mouth='grin' if b>0 else 'O',brow=-.05)
        H['arm'][1].rotation_euler=(R(-70-20*b),0,R(10)); H['arm'][-1].rotation_euler=(R(-40+15*b),0,R(-10))
def PLATES_():
    P=buffet_set(7,7,avoid=(PLATES[0],-5.0)); au=mk(PLATE_AUNTY,PLATES[0]+1.2,BUF_Y-1.5,0,'aunty'); wa=mk(WALEED,PLATES[0]-.4,BUF_Y-1.1,0,'wa')
    stack=empty((0,0,0)); [ocyl((0,0,k*.025),.15,.015,M('#F7F5EF',.2),stack,rot=(0,0,0)) for k in range(5)]
    def upd(t):
        jostle(P,t); stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(180); face(wa,mouth='O' if t<ws(74) else 'flat',brow=.05)
        k=tl(t,ws(69)-.3,ws(69)); arm_to(wa,1,Vector((PLATES[0]-.1,PLATES[1]-.1,.86)),k*(1-tl(t,ws(73),ws(73)+.3)))
        stand(au,t); blink(au,t); au['root'].rotation_euler[2]=R(0); present(au,1,1,3.0,.0,-1.3); present(au,-1,1,3.0,.0,-1.3); hold(au,stack,1,.02); stack.location.x-=.25*au['u']
        face(au,mouth='smirk',brow=-.02); look_at(wa,hp(au),.7*tl(t,ws(74),ws(75)))
        if t<ws(74)-.1: camset((PLATES[0]-1.7,BUF_Y-3.0,1.7),(PLATES[0]+.2,PLATES[1]-.5,1.0),26,2.8)
        else: c0,tg,ln=closecam(au,0,-.4,2.6,lens=28,tz=-.6); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['PLATES']=PLATES_
def AUNTY_TALK(a,b,who,cam):
    def S_():
        P=buffet_set(6,8,avoid=(PLATES[0],-5.0,-8.0)); au=mk(PLATE_AUNTY,PLATES[0]+.9,BUF_Y-2.0,0,'aunty'); wa=mk(WALEED,PLATES[0]-.3,BUF_Y-1.4,0,'wa')
        stack=empty((0,0,0)); [ocyl((0,0,k*.025),.15,.015,M('#F7F5EF',.2),stack,rot=(0,0,0)) for k in range(5)]
        rw=face_dir(.9+.3,-.6); ra=face_dir(-1.2,.6)
        def upd(t):
            jostle(P,t); stand(wa,t); stand(au,t); blink(wa,t); blink(au,t); wa['root'].rotation_euler[2]=R(rw); au['root'].rotation_euler[2]=R(ra)
            present(au,1,1,3.0,.0,-1.3); present(au,-1,1,3.0,.0,-1.3); hold(au,stack,1,.02)
            if who=='wa': talk(wa,t,*wt(a,b),rest='smile'); face(wa,brow=.05); face(au,mouth='flat',brow=-.06,brow_r=-10); present(wa,1,tl(t,ws(81),ws(82)),3.2,.3,-1.5)
            else: talk(au,t,*wt(a,b),rest='smirk'); face(au,brow=-.03); face(wa,mouth='O',eyes=1.25,brow=.06)
            look_at(wa,hp(au),.7); look_at(au,hp(wa),.7)
            if cam=='au': c0,tg,ln=ots(au,wa,3.0,24)
            else: c0,tg,ln=ots(wa,au,3.0,24)
            camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
SHOTS['ASK']=AUNTY_TALK(80,82,'wa','au')
SHOTS['UNBORN']=AUNTY_TALK(83,93,'au','au')
def BILAL_():
    P=buffet_set(6,9,avoid=(RAITA[0],RAITA[0]+1.5,RAITA[0]-1.5)); bi=mk(BILAL,RAITA[0]+.2,BUF_Y-1.3,0,'bilal'); wa=mk(WALEED,RAITA[0]+1.3,BUF_Y-1.6,0,'wa')
    pl=plate(); rb=face_dir(1.1,-.3); rw=face_dir(-1.1,.3)
    def upd(t):
        jostle(P,t); stand(bi,t); stand(wa,t); blink(bi,t); blink(wa,t); bi['root'].rotation_euler[2]=R(rb); wa['root'].rotation_euler[2]=R(rw)
        kg=tl(t,ws(96),ws(98)); mid=Vector(hp(bi)).lerp(Vector(hp(wa)),.5)+Vector((0,0,-1.25))
        if t<ws(98): present(bi,1,1,3.1,.25,-1.4); hold(bi,pl,1,.02)
        else: arm_to(bi,1,mid,1-tl(t,ws(100),ws(101))); arm_to(wa,1,mid,1); pl.location=mid+Vector((0,0,.03))
        if t>ws(101): present(wa,1,1,3.1,.25,-1.4); hold(wa,pl,1,.02)
        talk(bi,t,*wt(101,107),rest='smile'); face(bi,brow=-.03,brow_r=-8); face(wa,mouth='O' if t<ws(101) else 'smile',eyes=1.15,brow=.04)
        look_at(bi,hp(wa),.7); look_at(wa,hp(bi),.7)
        if t<ws(101)-.1: c0,tg,ln=twoshot(bi,wa,2.6); camset(c0,tg,ln,2.8)
        else: c0,tg,ln=ots(bi,wa); camset(drift(c0,tg,t),tg,ln,2.8)
        if t>ws(104): u=bi['u']; arm_to(bi,-1,Vector((RAITA[0],RAITA[1]-.1,1.0)),tl(t,ws(104),ws(105)))
    return dict(upd=upd)
SHOTS['BILAL']=BILAL_
def DAIG_():
    P=buffet_set(6,10,avoid=(DAIG[0],DAIG[0]+1.4,DAIG[0]-1.4)); au=mk(SHOP_AUNTY,DAIG[0]-.2,DAIG[1]-.95,0,'aunty'); wa=mk(WALEED,DAIG[0]+1.4,DAIG[1]-1.6,0,'wa')
    bag=empty((0,0,0)); obox((0,0,0),(.2,.1,.22),M('#3A8ADA',.4,alpha=.75),.02,bag); obox((0,0,-.05),(.18,.08,.14),M('#E8A040',.7),.02,bag)
    ra=180; rw=face_dir(-1.6,.6)
    def upd(t):
        jostle(P,t); stand(au,t); stand(wa,t); blink(au,t); blink(wa,t); wa['root'].rotation_euler[2]=R(rw); u=au['u']
        kt=tl(t,ws(120)-.3,ws(120)); au['root'].rotation_euler[2]=R(L(180,face_dir(1.6,-.6),kt))
        sc=math.sin(t*9); arm_to(au,1,Vector((DAIG[0]+.05,DAIG[1]-.15,1.5+.08*sc)),1-kt); arm_to(au,-1,Vector((DAIG[0]-.3,DAIG[1]-.45,1.25)),1-kt)
        hold(au,bag,-1,-.1);
        if kt>0: present(au,-1,kt,2.9,.3,-1.2)
        talk(au,t,*wt(120,125),rest='smile'); face(au,brow=.05); face(wa,mouth='flat',brow=-.08,brow_r=-14,eyes=.8); look_at(wa,hp(au),.7)
        if t<ws(120)-.2: camset((DAIG[0]-1.3,DAIG[1]-1.5,2.25),(DAIG[0],DAIG[1],1.3),26,2.8)
        else: c0,tg,ln=ots(au,wa); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['DAIG']=DAIG_
LEGP=(QORMA[0]+.08,QORMA[1]-.05,1.1)
def qorma_set(uncle_gone=0):
    P=buffet_set(6,11,avoid=(QORMA[0],QORMA[0]+1.3,QORMA[0]-1.3,QORMA[0]+2.6,QORMA[0]-2.6)); wa=mk(WALEED,QORMA[0]-.75,QORMA[1]-1.05,0,'wa'); un=mk(UNCLE,QORMA[0]+.8,QORMA[1]-1.05,0,'uncle')
    leg=empty(LEGP); obox((0,0,0),(.07,.045,.035),M('#8A3A1A',.6),.025,leg); ocyl((.085,0,0),.014,.07,M('#F4EAD0',.4),leg,rot=(0,R(90),0))
    sp=empty((0,0,0)); ocyl((0,0,0),.012,.5,M('#C9CED8',.2,metal=.9),sp,rot=(R(70),0,0)); ocyl((0,.22,-.08),.045,.015,M('#C9CED8',.2,metal=.9),sp,rot=(0,0,0))
    return P,wa,un,leg,sp
def QORMA_():
    P,wa,un,leg,sp=qorma_set()
    def upd(t):
        jostle(P,t); stand(wa,t); stand(un,t); blink(wa,t); blink(un,t)
        k1=tl(t,ws(141)-.3,ws(141)+.2); kw=tl(t,ws(145),ws(146))
        un['root'].rotation_euler[2]=R(L(180,face_dir(-1.5,.0),tl(t,ws(146)+.3,ws(146)+.8))); wa['root'].rotation_euler[2]=R(L(180,face_dir(1.5,0),tl(t,ws(146)+.3,ws(146)+.8)))
        hand=Vector((QORMA[0]+.05,QORMA[1]-.35,1.35))
        arm_to(un,1,hand+Vector((.05,0,0)),k1); arm_to(wa,1,hand+Vector((-.06,0,.02)),kw)
        sp.location=hand+Vector((0,.15,-.1)); sp.rotation_euler=(0,0,0)
        st=tl(t,ws(146)+.4,ws(146)+1.0)
        face(un,mouth='flat',brow=-.05-.05*st,brow_r=-10-10*st,eyes=1-.2*st); face(wa,mouth='flat',brow=-.06-.04*st,brow_r=-12-8*st,eyes=1-.2*st)
        look_at(un,hp(wa) if st>0 else LEGP,.7); look_at(wa,hp(un) if st>0 else LEGP,.7)
        if t<ws(135)-.1: camset((QORMA[0]-.1,QORMA[1]+.95,1.65),(QORMA[0],QORMA[1]-.3,1.1),28,2.8)
        elif t<ws(140)-.1: q=tl(t,ws(135)-.1,ws(140)); camset(LV((QORMA[0]+.1,QORMA[1]+.8,1.5),(QORMA[0]+.1,QORMA[1]+.6,1.4),q),LEGP,32,2.8)
        elif t<ws(146)+.3: camset((QORMA[0]+.05,QORMA[1]+1.2,1.7),(QORMA[0]+.05,QORMA[1]-.8,1.4),26,2.8)
        else: q=tl(t,ws(146)+.3,DUR); camset(LV((QORMA[0]+.05,QORMA[1]+1.8,1.75),(QORMA[0]+.05,QORMA[1]+1.3,1.72),q),(QORMA[0]+.05,QORMA[1]-1.05,1.6),26,2.8)
    return dict(upd=upd)
SHOTS['QORMA']=QORMA_
def STARE(a,b,who):
    def S_():
        P,wa,un,leg,sp=qorma_set(); hand=Vector((QORMA[0]+.05,QORMA[1]-.35,1.35))
        def upd(t):
            jostle(P,t); stand(wa,t); stand(un,t); blink(wa,t); blink(un,t)
            un['root'].rotation_euler[2]=R(face_dir(-1.5,0)); wa['root'].rotation_euler[2]=R(face_dir(1.5,0))
            arm_to(un,1,hand+Vector((.05,0,0)),1); arm_to(wa,1,hand+Vector((-.06,0,.02)),1); sp.location=hand+Vector((0,.15,-.1))
            sp_,ls=(un,wa) if who=='un' else (wa,un)
            talk(sp_,t,*wt(a,b),rest='flat'); look_at(sp_,hp(ls),.7); look_at(ls,hp(sp_),.7)
            if who=='un': face(un,brow=-.08,brow_r=-16); face(wa,mouth='flat',brow=-.06,eyes=.85)
            else:
                face(wa,brow=.03,brow_r=6); face(un,mouth='flat',brow=-.05); kp=tl(t,ws(154),ws(155)); arm_to(wa,-1,root_mat(wa)@Vector((-.6*wa['u'],-1.8*wa['u'],4.0*wa['u'])),kp)
            c0,tg,ln=ots(sp_,ls); camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
SHOTS['UNCLE']=STARE(147,152,'un'); SHOTS['WTRICK']=STARE(153,159,'wa')
def RUNOFF():
    P,wa,un,leg,sp=qorma_set(); hand=Vector((QORMA[0]+.05,QORMA[1]-.35,1.35))
    def upd(t):
        jostle(P,t); stand(wa,t); blink(wa,t); blink(un,t); wa['root'].rotation_euler[2]=R(face_dir(1.5,0)); arm_to(wa,1,hand+Vector((-.06,0,.02)),1); sp.location=hand+Vector((0,.15,-.1))
        go=ws(165)-.1
        if t<go:
            stand(un,t); un['root'].rotation_euler[2]=R(face_dir(-1.5,0)); arm_to(un,1,hand+Vector((.05,0,0)),1)
            un['head'].rotation_euler[2]=R(25*tl(t,ws(161),ws(162))*(1 if (t*2)%2<1 else .6)); face(un,mouth='flat',eyes=.9,brow=.03); look_at(un,(KHEER[0],KHEER[1],1.2),tl(t,ws(161),ws(162)))
        else: walk_path(un,[(QORMA[0]+.8,QORMA[1]-1.05),(QORMA[0]+2.6,QORMA[1]-1.4),(KHEER[0]-.3,KHEER[1]-1.0)],t,go,DUR+.3,run_=True,ease_in=.12); face(un,mouth='grin',brow=.05)
        face(wa,mouth='flat',brow=-.04,eyes=.9); look_at(wa,hp(un),.6)
        q=ease(t/DUR); camset(LV((QORMA[0]-.5,QORMA[1]-4.2,1.9),(QORMA[0]+.6,QORMA[1]-4.4,1.9),q),(QORMA[0]+1.4,QORMA[1]-1.0,1.3),22,4)
    return dict(upd=upd)
SHOTS['RUNOFF']=RUNOFF
def WIN():
    P,wa,un,leg,sp=qorma_set(); hidep=lambda H: setattr(H['root'],'location',(0,0,-40)); un['root'].location=(0,0,-40)
    pl=plate()
    def upd(t):
        jostle(P,t); stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(180); un['root'].location=(0,0,-40)
        present(wa,-1,1,3.1,.25,-1.4); hold(wa,pl,-1,.02)
        k=tl(t,.2,.7); kl=tl(t,.7,1.2); hand=Vector((QORMA[0]+.05,QORMA[1]-.35,1.35))
        if t<.7: arm_to(wa,1,hand,1); sp.location=hand+Vector((0,.15,-.1)); leg.location=LEGP
        else: sp.location=hand+Vector((0,.15,-.1)); leg.location=Vector(LEGP).lerp(pl.location+Vector((0,0,.05)),kl); arm_to(wa,1,Vector(LEGP).lerp(pl.location+Vector((0,0,.25)),kl),1)
        if t>1.3: present(wa,1,1,4.6,.3,-1.2)
        face(wa,mouth='grin' if t>1.2 else 'smirk',brow=.04,eyes=1.15)
        c0,tg,ln=closecam(wa,180,.3,2.4,lens=28,tz=-.45); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['WIN']=WIN
def stain(H):
    e=empty((0,0,0),H['root']); u=H['u']
    obox((.25*u,-.56*u,3.3*u),(.22*u,.01,.28*u),M('#B0501A',.7),.02*u,e); obox((-.1*u,-.56*u,3.0*u),(.12*u,.01,.1*u),M('#B0501A',.7),.02*u,e)
def sock(H,s=-1):
    e=empty((0,0,0),H['leg'][s]); u=H['u']; obox((0,-.05*u,-2.85*u),(.3*u,.36*u,.12*u),M('#F4F1EA',.85,kind='fabric'),.03*u,e)
def WALKBACK():
    cs=hall_set(1.0); tables_only([(-6,-1.5),(0,-1.5),(6,-1.5),(-3,-4.5),(3,-4.5)]); wa=mk(WALEED,QORMA[0]-.7,QORMA[1]-1.2,180,'wa'); stain(wa); sock(wa)
    pl=plate(food='leg'); P=buffet_set(5,12,avoid=(QORMA[0],))
    for k,(x,y,a) in enumerate(((-4,2.6,80),(2,2.2,-60),(5,3.0,30),(-1,3.4,120))): c=chair(x,y,a); c.rotation_euler=(R(-82),0,R(a))
    shoe=empty((1.2,1.0,.06)); obox((0,0,0),(.12,.2,.06),M('#3A2A1E',.5),.03,shoe); shoe.rotation_euler=(0,0,R(40))
    def upd(t):
        jostle(P,t); blink(wa,t)
        walk_path(wa,[(QORMA[0]-.7,QORMA[1]-1.2),(1.5,2.6),(-2.0,-.2),(-5.5,-3.8)],t,.2,DUR+3.5,step=.42,arm=10,ease_in=.15)
        present(wa,1,1,3.4,.25,-1.4); hold(wa,pl,1,.02); face(wa,mouth='smirk',brow=.06,eyes=.85); wa['head'].rotation_euler[0]=R(-8)
        p=wa['root'].location
        if t<ws(179)-.1: camset((p.x-3.0,p.y-4.0,1.2),(p.x,p.y,1.4),22,4)
        elif t<ws(182)-.1: camset((p.x-1.0,p.y-1.8,1.55),(p.x,p.y,1.45),30,2.8)
        elif t<ws(185)-.1: camset((p.x-.9,p.y-1.6,.45),(p.x,p.y,.2),30,2.8)
        else: camset((p.x-2.2,p.y-3.2,.7),(p.x,p.y,1.6),20,4)
    return dict(upd=upd)
SHOTS['WALKBACK']=WALKBACK
def VIP_(a,b,who,react=None):
    def S_():
        cs=hall_set(1.0); am=mk(AMMI,VIP[0],VIP[1]+.95,0,'ammi'); chair(VIP[0],VIP[1]+.95,180); wa=mk(WALEED,VIP[0]+1.4,VIP[1]-1.2,0,'wa'); stain(wa); sock(wa)
        p3=plate(None,(VIP[0],VIP[1]+.25,.8),food='legs3'); pw=plate(food='leg')
        ra=face_dir(1.4,-2.1); rw=face_dir(-1.4,2.1)
        def upd(t):
            seat(am,t,.5); am['root'].location=(VIP[0],VIP[1]+.95,0); am['root'].rotation_euler=(0,0,R(ra*.5)); blink(am,t)
            stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(rw); present(wa,1,1,3.2,.25,-1.4); hold(wa,pw,1,.02)
            sp,ls=(am,wa) if who=='am' else (wa,am)
            talk(sp,t,*wt(a,b),rest='smile' if who=='am' else 'flat'); look_at(sp,hp(ls),.7); look_at(ls,hp(sp),.6)
            if who=='am': face(am,brow=.03); face(wa,mouth='O',eyes=1.3,brow=.07); arm_to(am,1,Vector((VIP[0]+.2,VIP[1]+.25,1.0)),tl(t,ws(197),ws(198)) if a<197<=b else 0)
            else: face(wa,brow=-.04,brow_r=-10,eyes=.85); face(am,mouth='smile',brow=.02)
            if react: react(am,wa,t)
            if who=='am' and not (react and t>ws(214)): camset(LV((VIP[0]+.5,VIP[1]-1.9,2.25),(VIP[0]+.45,VIP[1]-1.7,2.2),ease(t/DUR)),(VIP[0],VIP[1]+.45,.95),26,2.8)
            else: c0,tg,ln=closecam(wa,rw if who!='am' else face_dir(8,10),.35,2.3,lens=28,tz=-.4); camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
def _turn(am,wa,t):
    k=tl(t,ws(214)+.1,ws(214)+.8); wa['root'].rotation_euler[2]=R(L(face_dir(-1.4,2.1),face_dir(8,10),k)); face(wa,mouth='flat',brow=-.1,brow_r=-18,eyes=.8)
SHOTS['VIP']=VIP_(190,200,'am'); SHOTS['WREPLY']=VIP_(201,207,'wa'); SHOTS['AMMI2']=VIP_(208,214,'am',react=_turn)
def CTA():
    cs=hall_set(1.0); tables_only([(-6,-1.5),(0,-1.5),(6,-1.5),(-6,1.8),(0,1.8),(6,1.8)]); P=buffet_set(9,13)
    for k in range(10):
        r=random.Random(k); c=chair(r.uniform(-9,9),r.uniform(-3,3.8),r.uniform(0,360)); c.rotation_euler=(R(-82 if k%3 else 0),0,R(r.uniform(0,360)))
    wa=mk(WALEED,VIP[0]+1.4,VIP[1]-1.2,0,'wa'); stain(wa); sock(wa)
    def upd(t):
        jostle(P,t); stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(face_dir(8,10)); face(wa,mouth='flat',brow=-.1,brow_r=-18,eyes=.8)
        q=ease(t/DUR); camset(LV((-8.4,-9.3,1.95),(-8.0,-8.9,1.95),q),(4,4.5,1.2),L(20,24,q),6)
    return dict(upd=upd)
SHOTS['CTA']=CTA
SEQ=[('HOOK', 0.0), ('KHANA0', 4.0), ('HALL', 5.567), ('AMMI', 13.033), ('MISSION', 17.0), ('WHISPER', 19.5), ('CHAOS', 20.8), ('PLATES', 25.367), ('ASK', 31.067), ('UNBORN', 32.567), ('BILAL', 36.0), ('DAIG', 40.7), ('QORMA', 47.8), ('UNCLE', 56.733), ('WTRICK', 59.067), ('RUNOFF', 61.867), ('WIN', 66.133), ('WALKBACK', 67.733), ('VIP', 74.633), ('WREPLY', 78.0), ('AMMI2', 80.567), ('CTA', 83.867)]
END=87.4
