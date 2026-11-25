# Shots for "Everyone Is a Bhaiya from Karachi". SEQ/END filled by gen_seq.py.
SHOTS={}
END=103.6333
SEQ=[('HOOK', 0.0), ('FLIGHT', 3.033), ('DOODH', 7.433), ('POLICE', 9.167), ('ASK1', 10.833), ('ASK2', 17.667), ('HOUR', 21.6), ('STALL', 24.7), ('ALOO', 30.2), ('ABAY', 33.7), ('SIT', 35.633), ('TALEEM', 39.8), ('PLATES', 42.833), ('GIVEUP', 45.333), ('SHABASH', 48.167), ('DROP', 49.7), ('BAND', 53.433), ('RIVER', 55.267), ('CHILL', 59.033), ('DARK', 61.767), ('TORCH', 64.933), ('AIRRUN', 68.867), ('MERI', 73.7), ('FLIGHTQ', 75.133), ('WAIT', 79.067), ('CRICKET', 83.6), ('SUNRISE', 86.933), ('CHALO', 89.767), ('RUK', 91.5), ('OUTRO', 94.933), ('CTA', 100.2)]
FILLE=[35.0]; _FL=[]
_camset0=camset
def camset(loc,tg,lens,*a,**k):
    _camset0(loc,tg,lens,*a,**k)
    if not _FL: _FL.append(point((0,0,0),FILLE[0],(1,.93,.85),r=.4,shadow=False))
    _FL[0].location=Vector(loc)+Vector((0,0,.3)); _FL[0].data.energy=FILLE[0]
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
def twoshot(A,B_,back=2.6,lens=26,side=-1):
    a=Vector(hp(A)); b=Vector(hp(B_)); m=(a+b)/2; d=b-a; d.z=0; d.normalize(); pr=Vector((-d.y,d.x,0))
    if (pr.y>0)!=(side>0): pr=-pr
    c=m+pr*back+Vector((0,0,.05)); return (c.x,c.y,c.z),(m.x,m.y,m.z-.35),lens
def ots(sp,ls,back=2.3,lens=28,side=-1):
    a=Vector(hp(sp)); b=Vector(hp(ls)); d=(b-a); dl=d.length; d.z=0; d.normalize(); pr=Vector((-d.y,d.x,0))
    if (pr.y>0)!=(side>0): pr=-pr
    m=(a+b)/2; c=m+pr*back+d*(.35*dl)+Vector((0,0,.05)); tg=a.lerp(b,.25); return (c.x,c.y,c.z),(tg.x,tg.y,tg.z-.35),lens
def facing(H,p,k=1.0):
    r=H['root'].location; H['root'].rotation_euler[2]=R(face_dir(p[0]-r.x,p[1]-r.y)) if k>=1 else H['root'].rotation_euler[2]
def wave_hi(H,t,t0,s=1):
    k=tl(t,t0,t0+.25)*(1-tl(t,t0+1.4,t0+1.7)); H['arm'][s].rotation_euler=(R(-165*k),0,R(s*(12+10*math.sin((t-t0)*10))*k))
def walk_to(H,pts,t,t0,t1,**kw): return walk_path(H,pts,t,t0,t1,**kw)
WY=3.2   # Waleed's walking line on the north sidewalk
def street(mood='city',x0=-30,x1=80):
    city(x0,x1); setup_world(mood,shadow=60)
def backpack_on(H): pass
# ---------------------------------------------------------------- HOOK: crowd greets Waleed
def HOOK():
    street('city'); wa=mk(WALEED,-6,WY,90,'wa'); G=[]
    for i,(x,y,c) in enumerate(((-2.5,4.5,0),(1.0,4.4,3),(3.8,1.6,6),(-1.0,1.6,9),(6.5,4.5,12),(9.5,1.7,15))):
        H=mk(CROWD[c],x,y,0,'g%d'%i); G.append(H)
    rk=rickshaw((14,-1.5,0),180,'#2E8A3A',seed=2); bus=minibus((-14,-4.5,0),0,seed=1)
    cr=[crow(-4+k*3.1,NS-.6+.05*(k%2),8.0+.03*k,90*(k%2)) for k in range(5)]
    def upd(t):
        x=walk_to(wa,[(-6,WY),(3,WY)],t,0,DUR+1.5,step=.42)
        p=wa['root'].location; blink(wa,t); face(wa,mouth='smile',brow=.03)
        for i,H in enumerate(G):
            stand(H,t); blink(H,t); facing(H,p); look_at(H,hp(wa),.7); wave_hi(H,t,.15+i*.28,1); face(H,mouth='grin' if math.sin(t*3+i)>0 else 'smile',brow=.04)
        drive(rk,L(14,-6,t/DUR*1.0),-1.5,180,L(14,-6,t/DUR)); bus.location=(L(-14,-4,t/DUR),-4.5,0)
        q=ease(t/DUR); camset(LV((-3.0,-5.6,2.1),(-1.0,-5.2,2.0),q),LV((1.0,3.0,1.4),(2.6,3.2,1.4),q),20,6)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
def FLIGHT():
    street('city'); wa=mk(WALEED,0,WY,90,'wa'); G=[mk(CROWD[1],4.2,4.4,0,'g1'),mk(CROWD[4],5.5,1.8,0,'g2')]
    def upd(t):
        walk_to(wa,[(0,WY),(2.6,WY)],t,0,DUR+.8,step=.42); blink(wa,t)
        u=wa['u']; k=tl(t,ws(12)-.2,ws(12)+.2)*(1-tl(t,ws(17),ws(17)+.3))
        arm_to(wa,-1,root_mat(wa)@Vector((-.3*u,-1.4*u,3.6*u)),k); look_at(wa,wa['arm'][-1].matrix_world@Vector(hand_loc(wa,-1)),.8*k,maxpitch=45)
        face(wa,mouth='smirk' if t>ws(18) else 'smile',brow=.04, brow_r=6 if t>ws(18) else 0)
        for H in G: stand(H,t); blink(H,t); facing(H,wa['root'].location); face(H,mouth='smile')
        c0,tg,ln=closecam(wa,90,-.6,2.6,lens=30,tz=-.35); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['FLIGHT']=FLIGHT
def GREET(C,a,b,prop=None,cam_side=-1):
    def S_():
        street('city'); wa=mk(WALEED,6,WY,90,'wa'); g=mk(C,9.2,WY+.15,-90,'gr')
        extra=prop(g) if prop else None
        def upd(t):
            walk_to(wa,[(6,WY),(7.4,WY)],t,0,DUR+.2,step=.42); blink(wa,t); look_at(wa,hp(g),.6); face(wa,mouth='smile',brow=.03)
            stand(g,t); blink(g,t); facing(g,wa['root'].location); look_at(g,hp(wa),.8); talk(g,t,*wt(a,b),rest='grin'); face(g,brow=.05); wave_hi(g,t,.05,1)
            if extra: extra(g,t)
            c0,tg,ln=ots(g,wa,2.4,26,side=cam_side); camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
def _milk(g):
    e=empty((0,0,0),g['arm'][-1]); u=g['u']; e.location=(-.5*u,-.1*u,-2.4*u); ocyl((0,0,-.18),.16,.36,M('#C9CED8',.25,metal=.85),e,seg=14); ocyl((0,0,.03),.07,.06,M('#C9CED8',.25,metal=.85),e,seg=10)
    return lambda g,t: None
def _salute(g):
    def f(g,t): g['arm'][1].rotation_euler=(R(-150),0,R(35)) if t>.3 else g['arm'][1].rotation_euler
    return f
SHOTS['DOODH']=GREET(DOODH,22,26,_milk)
SHOTS['POLICE']=GREET(POLICE,27,30,_salute,cam_side=-1)
def ASKSET(C,a,b,ask_word,point_at=None):
    def S_():
        street('afternoon' if C is MAN2 else 'city'); wa=mk(WALEED,12,WY,90,'wa'); m=mk(C,13.8,WY+.2,-90,'man')
        def upd(t):
            stand(wa,t); blink(wa,t); facing(wa,m['root'].location); stand(m,t); blink(m,t); facing(m,wa['root'].location)
            look_at(wa,hp(m),.8); look_at(m,hp(wa),.8)
            if t<ws(a)-.05: face(wa,mouth='O' if t>ws(ask_word) else 'smile',brow=.04); face(m,mouth='smile')
            else:
                talk(m,t,*wt(a,b),rest='grin'); face(m,brow=.05); face(wa,mouth='smile',brow=.03)
                kp=tl(t,ws(a)+.6,ws(a)+1.0); u=m['u']; arm_to(m,1,root_mat(m)@Vector((.6*u,-2.2*u,4.2*u)),kp)
                look_at(m,(40,WY,2.0),.6*kp*(1-tl(t,ws(b)-1.0,ws(b)-.6)))
            if t<ws(a)-.05: c0,tg,ln=twoshot(wa,m,3.3,24); camset(drift(c0,tg,t),tg,ln,2.8)
            else: c0,tg,ln=ots(m,wa,2.2,28); camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
SHOTS['ASK1']=ASKSET(MAN1,40,53,35)
SHOTS['ASK2']=ASKSET(MAN2,60,63,57)
def HOUR():
    street('golden',x0=-10,x1=110); wa=mk(WALEED,30,WY,90,'wa')
    sg=empty((38,NS-.9,0)); ocyl((0,0,1.3),.05,2.6,M('#9A9EA6',.4,metal=.6),sg,seg=8)
    for k,(rz,txt) in enumerate(((0,'AIRPORT  2 MIN  >'),(180,'<  AIRPORT  2 MIN'))):
        a=empty((0,0,2.35-k*.45),sg); obox((0,0,0),(.85,.02,.17),M('#2E8A3A',.5),.01,a); stext(txt,(38,NS-.93,2.35-k*.45),.14,'#FFFFFF')
    def upd(t):
        walk_to(wa,[(30,WY),(37.2,WY)],t,0,DUR,step=.36,arm=8); blink(wa,t); face(wa,mouth='flat',brow=-.05,eyes=.85); wa['head'].rotation_euler[0]+=R(6)
        if t>DUR*.7: look_at(wa,(38,NS-.9,2.2),.7)
        q=ease(t/DUR); camset(LV((33.5,-1.2,1.8),(35.8,-.6,1.75),q),LV((32,WY,1.5),(37.6,WY+.4,1.9),q),24,4)
    return dict(upd=upd)
SHOTS['HOUR']=HOUR
# ---------------------------------------------------------------- biryani stall
SX,SY=STALL_X,NS-1.6
def stall_set(mood='golden',n_eaters=4):
    city(STALL_X-30,STALL_X+30); stall(); stall_tables(); setup_world(mood,shadow=40)
    bw=mk(BIRYANI,SX+.2,SY+1.1,0,'biryani')
    E=[]
    seats=[(STALL_TABLES[0][0]-1.55,STALL_TABLES[0][1],90,0),(STALL_TABLES[0][0],STALL_TABLES[0][1]-1.45,180,5),(STALL_TABLES[2][0],STALL_TABLES[2][1]-1.45,180,8),(STALL_TABLES[2][0]+1.55,STALL_TABLES[2][1],-90,11)]
    for i,(x,y,rz,c) in enumerate(seats[:n_eaters]):
        pchair_k(x,y,rz); H=mk(CROWD[c],x,y,rz,'e%d'%i); H['seat']=(x,y,rz); E.append(H)
    return bw,E
def eat(H,t,freeze=False):
    seat(H,t,.44); x,y,rz=H['seat']; H['root'].location=(x,y,0); H['root'].rotation_euler=(0,0,R(rz))
    if not freeze: blink(H,t); k=(math.sin(t*3.2+x)*.5+.5); H['arm'][1].rotation_euler=(R(-60-40*k),0,R(10)); face(H,mouth='O' if k>.7 else 'smile')
def STALL():
    bw,E=stall_set(); wa=mk(WALEED,SX-6,WY,90,'wa')
    def upd(t):
        for H in E: eat(H,t)
        stand(bw,t); blink(bw,t); bw['arm'][1].rotation_euler=(R(-70-20*math.sin(t*4)),0,R(10)); face(bw,mouth='smile')
        walk_to(wa,[(SX-6,WY),(SX-1.0,SY-1.1)],t,0,DUR-.6,step=.42); blink(wa,t); face(wa,mouth='smile',brow=.04); look_at(wa,(SX,SY,1.6),.6*tl(t,DUR*.4,DUR*.6))
        q=ease(t/DUR)
        if t<ws(85)-.1: camset(LV((SX-3,-2.8,2.4),(SX-2.0,-2.2,2.2),q),(SX-.5,SY,1.5),22,5)
        else: camset((SX-1.0,SY-4.8,1.8),(SX-.7,SY-.8,1.45),24,4)
    return dict(upd=upd)
SHOTS['STALL']=STALL
WP=(SX-.9,SY-1.15)     # Waleed at the counter
def ALOO():
    bw,E=stall_set(); wa=mk(WALEED,WP[0],WP[1],0,'wa'); cr=crow(SX+1.6,SY-.95,2.86,-90)
    sp=empty((0,0,0)); ocyl((0,0,0),.012,.45,M('#C9CED8',.2,metal=.9),sp,rot=(R(70),0,0))
    def upd(t):
        fr=t>we(95)
        for H in E: eat(H,t,freeze=fr)
        stand(wa,t); blink(wa,t); facing(wa,(SX,SY+1.1)); look_at(wa,hp(bw),.7); talk(wa,t,*wt(90,95),rest='smile'); face(wa,brow=.04)
        if fr: face(wa,mouth='smile',brow=.06,eyes=1.1)
        stand(bw,t); blink(bw,t); facing(bw,wa['root'].location)
        hand=bw['arm'][1].matrix_world@Vector(hand_loc(bw,1))
        if not fr: bw['arm'][1].rotation_euler=(R(-75),0,R(10)); sp.location=hand; face(bw,mouth='smile')
        else:
            bw['arm'][1].rotation_euler=(R(-75),0,R(10)); face(bw,mouth='flat',eyes=1.4,brow=-.08,brow_r=-18)
            k=tl(t,we(95)+.15,we(95)+.55); p0=Vector(hand); sp.location=p0.lerp(Vector((p0.x,p0.y-.2,.13)),k*k); sp.rotation_euler=(R(70+60*k),0,R(30*k))
            for H in E: face(H,mouth='O',eyes=1.3); look_at(H,hp(wa),.8)
        cr.rotation_euler[2]=R(-90+ (0 if fr else 25*math.sin(t*6))); cr.children[1].rotation_euler[1]=0 if fr else R(15*math.sin(t*14))
        if t<we(95)+.1: camset((SX+1.1,SY-3.4,1.9),(SX-.35,SY+.2,1.45),26,4)
        else: q=tl(t,we(95)+.1,DUR); camset(LV((SX+1.8,SY-5.6,2.4),(SX+1.6,SY-5.2,2.3),q),(SX-.4,SY-.8,1.3),20,5)
    return dict(upd=upd)
SHOTS['ALOO']=ALOO
def ABAY():
    bw,E=stall_set(); wa=mk(WALEED,WP[0],WP[1],0,'wa')
    def upd(t):
        for H in E: eat(H,t,freeze=True); face(H,mouth='flat',eyes=1.2); look_at(H,hp(wa),.8)
        stand(wa,t); blink(wa,t); facing(wa,(SX,SY+1.1)); look_at(wa,hp(bw),.7); face(wa,mouth='O',eyes=1.25,brow=.06)
        stand(bw,t); blink(bw,t); facing(bw,wa['root'].location); look_at(bw,hp(wa),.8); talk(bw,t,*wt(96,99),rest='flat'); face(bw,brow=-.08,brow_r=-16)
        bw['root'].rotation_euler[0]=R(-8*tl(t,.0,.6))
        c0,tg,ln=closecam(bw,face_dir(wa['root'].location.x-bw['root'].location.x,wa['root'].location.y-bw['root'].location.y),.2,L(1.75,1.35,ease(t/DUR)),dz=.35,lens=24,tz=-.2); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['ABAY']=ABAY
TSEAT=(STALL_TABLES[1][0],STALL_TABLES[1][1]-1.45)
def SIT():
    bw,E=stall_set(); E[1]['root'].location=(0,0,-60); E.pop(1); wa=mk(WALEED,WP[0],WP[1],0,'wa'); un=mk(UNCLE,STALL_TABLES[1][0]+.8,STALL_TABLES[1][1]+1.3,180,'uncle')
    pchair_k(TSEAT[0],TSEAT[1],180); h1=mk(CROWD[5],0,0,0,'h1'); h2=mk(CROWD[8],0,0,0,'h2')
    def upd(t):
        for H in E: eat(H,t,freeze=True); face(H,mouth='smile'); look_at(H,hp(wa),.6)
        stand(bw,t); blink(bw,t); facing(bw,wa['root'].location); face(bw,mouth='smile',eyes=.7)
        t0w,t1w=ws(104)-.3,ws(108)
        if t<t1w: walk_to(wa,[WP,(WP[0]-.3,.7),(WP[0]+.1,-.4),TSEAT],t,t0w,t1w,step=.32) if t>t0w else (stand(wa,t),setattr(wa['root'],'location',(WP[0],WP[1],0)))
        else: seat(wa,t,.44); wa['root'].location=(TSEAT[0],TSEAT[1],0); wa['root'].rotation_euler[2]=R(180)
        blink(wa,t); face(wa,mouth='O',eyes=1.15,brow=.05)
        for H,dx in ((h1,-1.0),(h2,1.0)):
            stand(H,t); H['root'].location=(TSEAT[0]+dx,TSEAT[1]-.45,0) if t>t1w-.4 else (0,0,-60); facing(H,(TSEAT[0],TSEAT[1])); blink(H,t); face(H,mouth='smile',brow=.03)
            kk=tl(t,t1w-.3,t1w+.2)*(1-tl(t,DUR-.6,DUR-.2)); arm_to(H,1 if dx<0 else -1,Vector(hp(wa))+Vector((-dx*.35,0,-.8)),kk)
        stand(un,t); blink(un,t); facing(un,wa['root'].location); look_at(un,hp(wa),.6); face(un,mouth='smile')
        q=ease(t/DUR); camset(LV((TSEAT[0]+1.6,TSEAT[1]-3.6,3.4),(TSEAT[0]+1.4,TSEAT[1]-3.2,3.3),q),LV((WP[0],WP[1]-.4,1.3),(TSEAT[0],TSEAT[1],1.05),tl(t,ws(104),ws(108))),22,4)
    return dict(upd=upd)
SHOTS['SIT']=SIT
def table_set(plates=1):
    bw,E=stall_set(n_eaters=2); pchair_k(TSEAT[0],TSEAT[1],180); wa=mk(WALEED,TSEAT[0],TSEAT[1],180,'wa')
    un=mk(UNCLE,STALL_TABLES[1][0]+1.55,STALL_TABLES[1][1]+.05,-90,'uncle'); pchair_k(STALL_TABLES[1][0]+1.55,STALL_TABLES[1][1]+.05,-90)
    P=[]
    for k in range(3):
        e=empty((TSEAT[0]-.05+(k-1)*.0,TSEAT[1]+1.2,1.06+k*.03)); ocyl((0,0,0),.17,.015,M('#F7F5EF',.2),e,rot=(0,0,0))
        food=empty((0,0,.015),e); ocyl((0,0,0),.13,.04,M('#E8A040',.75),food,rot=(0,0,0)); obox((.05,.03,.04),(.045,.035,.03),M('#E8D8A0',.6),.02,food)
        P.append((e,food))
    return bw,E,wa,un,P
def seated_w(wa,t): seat(wa,t,.44); wa['root'].location=(TSEAT[0],TSEAT[1],0); wa['root'].rotation_euler=(0,0,R(180)); blink(wa,t)
def seated_u(un,t): seat(un,t,.44); un['root'].location=(STALL_TABLES[1][0]+1.55,STALL_TABLES[1][1]+.05,0); un['root'].rotation_euler=(0,0,R(-90)); blink(un,t)
def TALEEM():
    bw,E,wa,un,P=table_set()
    def upd(t):
        for H in E: eat(H,t)
        stand(bw,t); blink(bw,t); facing(bw,wa['root'].location)
        seated_w(wa,t); seated_u(un,t); facing(un,wa['root'].location); look_at(un,hp(wa),.7); look_at(wa,hp(un),.7)
        talk(un,t,*wt(109,115),rest='smile'); face(un,brow=.05); face(wa,mouth='O',eyes=1.1,brow=.04)
        u=un['u']; arm_to(un,1,root_mat(un)@Vector((.4*u,-1.6*u,4.0*u)),tl(t,ws(112),ws(113)))
        for i,(e,f) in enumerate(P): e.location=(TSEAT[0]-.05,TSEAT[1]+1.2,1.06+i*.03) if i==0 else (0,0,-30)
        c0,tg,ln=ots(un,wa,2.3,26,side=-1); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['TALEEM']=TALEEM
def PLATES():
    bw,E,wa,un,P=table_set()
    def upd(t):
        for H in E: eat(H,t)
        stand(bw,t); blink(bw,t); facing(bw,wa['root'].location); seated_w(wa,t); seated_u(un,t); facing(un,wa['root'].location); face(un,mouth='smile'); look_at(un,hp(wa),.6)
        n=1+int(min(2,t/(DUR*.3)))
        for i,(e,f) in enumerate(P):
            e.location=(TSEAT[0]-.05,TSEAT[1]+1.2,1.06+i*.03) if i<n else (0,0,-30)
            f.scale=(1,1,1) if i==n-1 and t<DUR*.85 else (0,0,0)
        sp=(math.sin(t*7)*.5+.5); wa['arm'][1].rotation_euler=(R(-70-35*sp),0,R(8)); face(wa,mouth='O' if sp>.6 else 'flat',eyes=.8-.2*tl(t,DUR*.5,DUR),brow=-.03)
        wa['root'].rotation_euler[0]=R(-6*tl(t,DUR*.6,DUR))
        q=ease(t/DUR); camset(LV((TSEAT[0]-1.3,TSEAT[1]+3.2,2.4),(TSEAT[0]-1.1,TSEAT[1]+2.9,2.3),q),(TSEAT[0],TSEAT[1]+.6,1.05),28,2.8)
    return dict(upd=upd)
SHOTS['PLATES']=PLATES
def GIVEUP():
    bw,E,wa,un,P=table_set()
    def upd(t):
        for H in E: eat(H,t,freeze=t>ws(130)-.1);
        stand(bw,t); blink(bw,t); facing(bw,wa['root'].location); seated_w(wa,t); seated_u(un,t); facing(un,wa['root'].location); look_at(un,hp(wa),.6)
        for i,(e,f) in enumerate(P): e.location=(TSEAT[0]-.05,TSEAT[1]+1.2,1.06+i*.03); f.scale=(0,0,0)
        talk(wa,t,*wt(122,129),rest='smile'); face(wa,brow=-.03,eyes=.85); wa['root'].rotation_euler[0]=R(-5)
        face(un,mouth='grin' if t>we(129) else 'smile',brow=.04)
        c0,tg,ln=closecam(wa,180,.3,2.3,lens=30,tz=-.35); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['GIVEUP']=GIVEUP
def SHABASH():
    bw,E,wa,un,P=table_set()
    def upd(t):
        for H in E:
            eat(H,t,freeze=True); H['arm'][1].rotation_euler=(R(-160),0,R(15)); face(H,mouth='grin',brow=.05); look_at(H,hp(wa),.7)
        stand(bw,t); blink(bw,t); facing(bw,wa['root'].location); bw['arm'][1].rotation_euler=(R(-165),0,R(20)); bw['arm'][-1].rotation_euler=(R(-165),0,R(-20)); talk(bw,t,*wt(130,131),rest='grin')
        seated_w(wa,t); seated_u(un,t); facing(un,wa['root'].location); un['arm'][1].rotation_euler=(R(-60),0,R(-40)); face(un,mouth='grin',brow=.05)
        face(wa,mouth='smile',eyes=.8)
        for i,(e,f) in enumerate(P): e.location=(TSEAT[0]-.05,TSEAT[1]+1.2,1.06+i*.03); f.scale=(0,0,0)
        q=ease(t/DUR); camset(LV((SX-3.7,SY-2.0,2.5),(SX-3.4,SY-2.1,2.4),q),(SX+.6,TSEAT[1]+.6,1.2),20,5)
    return dict(upd=upd)
SHOTS['SHABASH']=SHABASH
# ---------------------------------------------------------------- rain
def DROP():
    bw,E,wa,un,P=table_set()
    drop=obox((0,0,0),(.02,.02,.04),M('#C8E0F0',.05,alpha=.7,spec=1.0),.018,None)
    def upd(t):
        for H in E: eat(H,t)
        stand(bw,t); blink(bw,t); facing(bw,wa['root'].location); seated_w(wa,t); seated_u(un,t); facing(un,wa['root'].location)
        for i,(e,f) in enumerate(P): e.location=(TSEAT[0]-.05,TSEAT[1]+1.2,1.06+i*.03); f.scale=(0,0,0)
        nose=Vector(hp(wa))+Vector((0,.33*wa['u']*2,-.2))
        k=tl(t,.15,ws(137)); drop.location=nose+Vector((0,0,3.2*(1-k))) if t<ws(137)+.05 else (0,0,-40)
        face(wa,mouth='O' if t>ws(137) else 'flat',eyes=1.0+.35*tl(t,ws(137),ws(137)+.2),brow=.06*tl(t,ws(137),ws(137)+.2)); look_at(wa,(TSEAT[0],TSEAT[1]+.4,4),.7*tl(t,ws(137),ws(138)),maxpitch=45)
        c0,tg,ln=closecam(wa,180,.15,1.9,lens=32,tz=-.3); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['DROP']=DROP
def BAND():
    city(STALL_X-30,STALL_X+30,rain=True); setup_world('storm',shadow=40)
    rn=rain_drops(260,(STALL_X+8,2.0),size=(16,10)); X=STALL_X+8
    sh=empty((X,NS-.04,0)); shutter=obox((0,0,1.6),(2.6,.04,1.4),M('#8A9098',.45,metal=.6),0,sh)
    sk=mk(SHOPKEEP,X-.6,NS-.7,0,'sk'); P=[mk(CROWD[c],X+dx,NS-1.0+dy,180,'p%d'%c) for c,dx,dy in ((2,3.0,-.2),(7,-3.2,-.3))]
    def upd(t):
        rn(t,1.0); k=tl(t,ws(140),DUR-.2); shutter.location=(0,0,1.6+2.6*(1-k)); shutter.scale=(1,1,1)
        stand(sk,t); blink(sk,t); talk(sk,t,*wt(139,142),rest='O'); face(sk,brow=.08,eyes=1.3)
        sk['root'].rotation_euler[2]=R(L(0,180,tl(t,ws(140)-.2,ws(140))))
        for s in (1,-1): arm_to(sk,s,Vector((X-.6+s*.35,NS-.15,L(3.1,1.4,k))),tl(t,ws(140)-.1,ws(140)+.2))
        for H in P:
            k2=tl(t,ws(139),ws(141)); stand(H,t); blink(H,t); H['root'].rotation_euler[2]=R(L(0,180,k2)); face(H,mouth='O',eyes=1.2)
            H['arm'][1].rotation_euler=(R(-150*k2),0,R(20))
        q=ease(t/DUR); camset(LV((X-.4,-1.8,1.9),(X-.4,-1.2,1.85),q),(X-.4,NS-.5,1.8),24,4)
    return dict(upd=upd)
SHOTS['BAND']=BAND
def RIVER():
    city(STALL_X-30,STALL_X+30,rain=True); setup_world('storm',shadow=40); rn=rain_drops(300,(STALL_X+2,1.5),size=(14,10))
    wl=flood_plane(STALL_X-40,STALL_X+40,SS,NS)
    rk=rickshaw((STALL_X+6,-2.5,0),180,'#2E8A3A',seed=3); P=[]
    for i,(c,x,y,z) in enumerate(((3,STALL_X-3.0,4.0,.0),(10,STALL_X-1.2,4.4,0),(13,STALL_X+1.0,4.1,0))):
        H=mk(CROWD[c],x,y,0,'w%d'%i); P.append(H)
    cars=[car((STALL_X-9,-4.5,0),0,'#C9CED8',seed=4),car((STALL_X+14,-1.2,0),180,'#C8372D',seed=5)]
    def upd(t):
        rn(t,1.0); lvl=L(.02,.55,ease(tl(t,0,ws(150)+.3))); wl.location.z=lvl
        drive(rk,STALL_X+6-1.2*t,-2.5,180,1.2*t)
        for i,H in enumerate(P):
            seat(H,t,.4) if i==1 else stand(H,t); blink(H,t); H['root'].location.z=0
            if i==1: H['root'].location=(STALL_X-1.2,4.4,.0)
            face(H,mouth='smile',eyes=.8); H['arm'][1].rotation_euler=(R(-60),0,R(10)) if i==0 else H['arm'][1].rotation_euler
        q=ease(t/DUR); camset(LV((STALL_X-8,-6.0,2.6),(STALL_X-6.5,-5.4,2.4),q),(STALL_X,1.0,.8),20,6)
    return dict(upd=upd)
SHOTS['RIVER']=RIVER
def CHILL():
    city(STALL_X-30,STALL_X+30,rain=True); setup_world('storm',shadow=40); rn=rain_drops(220,(STALL_X+2,1),size=(10,8))
    wl=flood_plane(STALL_X-40,STALL_X+40,SS,NS); wl.location.z=.45
    rk=rickshaw((STALL_X+1.2,-.2,0),180,'#2E8A3A',seed=3); rk['root'].scale=(1.5,)*3
    rw=mk(RICKSHAW,0,0,0,'rw'); rw['root'].parent=rk['root']; rw['root'].location=(.3,0,.5); rw['root'].rotation_euler=(0,0,R(90)); rw['root'].scale=(1/1.5,)*3
    wa=mk(WALEED,STALL_X+.9,-2.7,180,'wa')
    def upd(t):
        rn(t,1.0); sit(rw,1,.85,legs=80); blink(rw,t); talk(rw,t,*wt(153,160),rest='smile'); face(rw,brow=.03,eyes=.75)
        rw['arm'][-1].rotation_euler=(R(-75),0,R(-8)); rw['arm'][1].rotation_euler=(R(-100+18*math.sin(t*3)),0,R(40))
        look_at(rw,hp(wa),.8)
        stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(180); face(wa,mouth='O',eyes=1.2,brow=.05); look_at(wa,(STALL_X+.8,-.2,1.6),.7)
        for s in (1,-1): wa['arm'][s].rotation_euler=(R(-40),0,R(s*30))
        q=ease(t/DUR); camset(LV((STALL_X-1.3,-5.2,1.9),(STALL_X-1.0,-4.9,1.85),q),(STALL_X+.8,-.6,1.5),28,4)
    return dict(upd=upd)
SHOTS['CHILL']=CHILL
# ---------------------------------------------------------------- blackout + torches
def DARK():
    city(STALL_X-40,STALL_X+40,rain=True); setup_world('night',shadow=40); wl=flood_plane(STALL_X-50,STALL_X+50,SS,NS); wl.location.z=.4
    def upd(t):
        k=0
        for i,(m,e) in enumerate(WIN_MATS):
            off=tl(t,ws(163)+(i%17)*.06,ws(163)+(i%17)*.06+.05); n=m.node_tree.nodes.get('Principled BSDF') if m.node_tree else None
            if n: n.inputs['Emission Strength'].default_value=e*(1-off)
        q=ease(t/DUR); camset(LV((STALL_X-12,-8.6,5.5),(STALL_X-11,-8.2,5.4),q),(STALL_X,6,7.5),18,8)
    return dict(upd=upd)
SHOTS['DARK']=DARK
def TORCH():
    city(STALL_X-30,STALL_X+30,rain=True); setup_world('night',shadow=40); wl=flood_plane(STALL_X-40,STALL_X+40,SS,NS); wl.location.z=.4
    for m,e in WIN_MATS:
        n=m.node_tree.nodes.get('Principled BSDF') if m.node_tree else None
        if n: n.inputs['Emission Strength'].default_value=0
    P=[]; r=random.Random(4)
    spots=[(STALL_X-4,4.2),(STALL_X-2.3,4.4),(STALL_X-.6,4.1),(STALL_X+1.1,4.4),(STALL_X+2.8,4.2),(STALL_X+4.5,4.4),(STALL_X-3.2,2.6),(STALL_X+3.6,2.6)]
    for i,(x,y) in enumerate(spots):
        H=mk(CROWD[(i*3)%len(CROWD)],x,y,0,'t%d'%i); ph=phone_in_hand(H,1,'#FFFFFF',em=0); l=point((0,0,0),0,(1,.97,.9),r=.05,shadow=False); H['ph']=i; P.append((H,ph,l))
    wa=mk(WALEED,STALL_X+.2,2.4,0,'wa')
    def upd(t):
        for H,ph,l in P:
            stand(H,t); blink(H,t); H['root'].location.z=0; k=tl(t,ws(174)-.05,ws(174)+.15); u=H['u']
            arm_to(H,1,root_mat(H)@Vector((.35*u,-1.7*u,(3.2+1.0*k)*u)),k); l.location=ph.matrix_world.translation+Vector((0,-.2,0)); l.data.energy=30*k
            face(H,mouth='smile',eyes=.8)
        stand(wa,t); blink(wa,t); face(wa,mouth='O',eyes=1.2,brow=.06); wa['root'].rotation_euler[2]=0; wa['head'].rotation_euler[2]=R(45*math.sin((t-ws(174))*2.2)*tl(t,ws(174),ws(174)+.4))
        FILLE[0]=160
        q=ease(t/DUR); camset(LV((STALL_X+.2,-3.6,1.9),(STALL_X+.2,-2.6,1.85),q),(STALL_X+.2,3.6,1.6),22,4)
    return dict(upd=upd)
SHOTS['TORCH']=TORCH
# ---------------------------------------------------------------- airport
def air_night():
    airport(); setup_world('night',shadow=50)
    for k in range(6): point((AIR_X-15+k*6,1.0,6.6),400,(1,.9,.75),r=.5)
def AIRRUN():
    air_night(); wa=mk(WALEED,AIR_X-12,-3.0,0,'wa'); rk=rickshaw((AIR_X-14,-4.6,0),0,'#2E8A3A',seed=6)
    def upd(t):
        walk_to(wa,[(AIR_X-12,-3.0),(AIR_X-4,-1.0),(AIR_X+.5,4.2)],t,0,DUR+.4,run_=True,ease_in=.1); blink(wa,t); face(wa,mouth='O',brow=.06,eyes=1.2)
        q=ease(t/DUR); camset(LV((AIR_X-2,-10.5,2.6),(AIR_X-1,-9.0,2.4),q),LV((AIR_X-9,-1.5,1.6),(AIR_X-1,2.5,2.0),q),22,6)
    return dict(upd=upd)
SHOTS['AIRRUN']=AIRRUN
CW=(AIR_X+.2,18.0); WC=(AIR_X+.2,16.2)
def counter_set():
    airport(); _S,_A,_w,_bg=setup_interior('day',room=(AIR_X,16,6.0),res=PCT,samples=SAMPLES,shadow_dist=18); _A.data.energy*=.45; FILLE[0]=15
    cw=mk(COUNTER,CW[0],CW[1],0,'counter'); wa=mk(WALEED,WC[0],WC[1],180,'wa')
    Q=[mk(CROWD[c],AIR_X+x,16.0,180,'q%d'%c) for c,x in ((4,-3.2),(9,3.4))]
    return cw,wa,Q
def COUNTER_A(a,b,who):
    def S_():
        cw,wa,Q=counter_set()
        def upd(t):
            stand(cw,t); blink(cw,t); stand(wa,t); blink(wa,t); facing(wa,cw['root'].location); facing(cw,wa['root'].location)
            for H in Q: stand(H,t); blink(H,t); face(H,mouth='flat',eyes=.7)
            look_at(wa,hp(cw),.7); look_at(cw,hp(wa),.7)
            if who=='wa':
                talk(wa,t,*wt(a,b),rest='O'); face(wa,brow=.08,eyes=1.3); face(cw,mouth='smile',eyes=.8)
                for s in (1,-1): arm_to(wa,s,Vector((WC[0]+s*.35,17.0,1.15)),tl(t,0,.25))
                c0,tg,ln=ots(wa,cw,2.2,26,side=-1)
            else:
                talk(cw,t,*wt(a,b),rest='smile'); face(cw,brow=.03,eyes=.85); face(wa,mouth='O',eyes=1.25,brow=.06)
                u=cw['u']; arm_to(cw,1,root_mat(cw)@Vector((.5*u,-1.6*u,4.0*u)),tl(t,ws(206),ws(207)))
                c0,tg,ln=ots(cw,wa,2.2,26,side=1)
            camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
SHOTS['MERI']=COUNTER_A(196,199,'wa'); SHOTS['FLIGHTQ']=COUNTER_A(200,211,'cw')
def park_night():
    airport(); parking(); setup_world('night',shadow=50)
    for k in range(4): point((PARK_X-12+k*8,PARK_Y,7.6),2200,(1,.88,.7),r=.6)
def WAIT():
    park_night(); wa=mk(WALEED,PARK_X-6,PARK_Y+3.0,0,'wa'); g1=mk(CROWD[6],PARK_X-4.6,PARK_Y+2.6,0,'g1'); g2=mk(CROWD[11],PARK_X-7.4,PARK_Y+2.5,0,'g2')
    cup_=empty((0,0,0)); ocyl((0,0,0),.05,.09,M('#F4F1EA',.3),cup_,rot=(0,0,0)); ocyl((0,0,.04),.045,.01,M('#B07A4A',.4),cup_,rot=(0,0,0))
    par=empty((0,0,0)); ocyl((0,0,0),.16,.025,M('#D8A050',.7),par,rot=(R(90),0,0))
    def upd(t):
        stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=0
        for H,obj,tw in ((g1,cup_,ws(219)),(g2,par,ws(222))):
            stand(H,t); blink(H,t); facing(H,wa['root'].location); look_at(H,hp(wa),.7); face(H,mouth='smile',brow=.03)
            s=1 if H is g1 else -1; k=tl(t,tw-.6,tw-.1)*(1-tl(t,tw+.4,tw+.8)); mid=Vector(hp(H)).lerp(Vector(hp(wa)),.55)+Vector((0,0,-1.25))
            if t<tw: arm_to(H,s,mid,k); obj.location=mid if k>.6 else H['arm'][s].matrix_world@Vector(hand_loc(H,s))
            else: arm_to(H,s,mid,k); arm_to(wa,-s,mid,1); obj.location=wa['arm'][-s].matrix_world@Vector(hand_loc(wa,-s))
        look_at(wa,hp(g1) if t<ws(221) else hp(g2),.6); face(wa,mouth='smile' if t>ws(219) else 'O',eyes=1.05)
        q=ease(t/DUR); camset(LV((PARK_X-6,PARK_Y-1.0,1.8),(PARK_X-6,PARK_Y-.4,1.75),q),(PARK_X-6,PARK_Y+2.8,1.45),24,4)
    return dict(upd=upd)
SHOTS['WAIT']=WAIT
def CRICKET():
    park_night(); bat=mk(CROWD[2],PARK_X+5.5,PARK_Y-1.0,180,'bat'); bow=mk(CROWD[7],PARK_X-4.5,PARK_Y,90,'bowl'); fl=[mk(CROWD[c],PARK_X+x,PARK_Y+y,rz,'f%d'%c) for c,x,y,rz in ((13,1,3.6,180),(16,-1,-3.4,0),(19,8.5,2.5,-120))]
    wa=mk(WALEED,PARK_X+7.6,PARK_Y-1.3,-90,'wa')
    bl=empty((0,0,0)); oico((0,0,0),.05,M('#F4F1EA',.4),bl,sub=2); BALLS.append(bl)
    bt=empty((0,0,0),bat['arm'][1]); bt.location=(.5*bat['u'],-.1*bat['u'],-2.3*bat['u']); obox((0,0,-.35),(.045,.02,.35),M('#E8D8B0',.5,kind='wood'),.01,bt)
    def upd(t):
        for H in fl: stand(H,t); blink(H,t); face(H,mouth='grin'); H['root'].rotation_euler[2]=R(face_dir(bl.location.x-H['root'].location.x,bl.location.y-H['root'].location.y))
        stand(wa,t); blink(wa,t); face(wa,mouth='grin',brow=.04); wa['arm'][1].rotation_euler=(R(-70),0,R(10))
        cyc=1.6; tt=t%cyc
        stand(bow,t); blink(bow,t); bow['arm'][1].rotation_euler=(R(-180*tl(tt,0,.5)),0,R(10)); face(bow,mouth='O')
        stand(bat,t); blink(bat,t); bat['arm'][1].rotation_euler=(R(-40-90*tl(tt,.75,.9)),0,R(-40+60*tl(tt,.75,.9))); face(bat,mouth='grin',brow=.05)
        a=Vector((PARK_X-4.1,PARK_Y,2.0)); b=Vector((PARK_X+5.1,PARK_Y-.6,.6)); c=Vector((PARK_X-2,PARK_Y+5,5))
        if tt<.5: bl.location=bow['arm'][1].matrix_world@Vector(hand_loc(bow,1))
        elif tt<.85: k=(tt-.5)/.35; p=a.lerp(b,k); p.z=L(a.z,b.z,k)+(0 if k<.6 else -1.2*(k-.6)*(1-k)); bl.location=p
        else: k=min(1,(tt-.85)/.75); p=b.lerp(c,k); p.z=L(b.z,c.z,k)+4*k*(1-k); bl.location=p
        q=ease(t/DUR); camset(LV((PARK_X-8.0,PARK_Y-2.0,2.3),(PARK_X-7.2,PARK_Y-1.8,2.2),q),(PARK_X+5.5,PARK_Y-.4,1.0),22,6)
    return dict(upd=upd)
SHOTS['CRICKET']=CRICKET
# ---------------------------------------------------------------- sunrise
def dawn_set():
    airport(); parking(); setup_world('dawn',shadow=60)
def SUNRISE():
    dawn_set(); pl=mk(PILOT,PARK_X-12,PARK_Y+5.5,90,'pilot'); bag=empty((0,0,0)); obox((0,0,.32),(.22,.12,.3),M('#16213A',.5),.03,bag)
    wa=mk(WALEED,PARK_X+1.0,PARK_Y+4.5,-90,'wa')
    def upd(t):
        walk_to(pl,[(PARK_X-12,PARK_Y+5.5),(PARK_X-1.4,PARK_Y+4.6)],t,0,DUR-.3,step=.38); blink(pl,t); face(pl,mouth='smile',brow=.02)
        u=pl['u']; bag.location=pl['root'].matrix_world@Vector((.75*u,-.3*u,0)); bag.rotation_euler[2]=pl['root'].rotation_euler[2]
        stand(wa,t); blink(wa,t); face(wa,mouth='O',eyes=1.1); look_at(wa,hp(pl),.6)
        q=ease(t/DUR); camset(LV((PARK_X-4,PARK_Y-3.0,1.6),(PARK_X-3.2,PARK_Y-2.4,1.6),q),LV((PARK_X-9,PARK_Y+5.4,1.7),(PARK_X-2,PARK_Y+4.8,1.6),q),24,6)
    return dict(upd=upd)
SHOTS['SUNRISE']=SUNRISE
def pair_dawn():
    dawn_set(); pl=mk(PILOT,PARK_X-1.4,PARK_Y+4.6,90,'pilot'); wa=mk(WALEED,PARK_X+.2,PARK_Y+4.5,-90,'wa')
    cup_=empty((0,0,0),wa['arm'][-1]); cup_.location=(-.5*wa['u'],-.3*wa['u'],-2.15*wa['u']); ocyl((0,0,0),.05,.09,M('#F4F1EA',.3),cup_,rot=(0,0,0))
    bt=empty((0,0,0),wa['arm'][1]); bt.location=(.5*wa['u'],-.1*wa['u'],-2.3*wa['u']); obox((0,0,-.35),(.045,.02,.35),M('#E8D8B0',.5,kind='wood'),.01,bt)
    G=[mk(CROWD[c],PARK_X+x,PARK_Y+y,rz,'d%d'%c) for c,x,y,rz in ((13,2.4,5.8,-110),(16,2.6,3.4,-60),(2,1.0,7.6,-150))]
    return pl,wa,G
def CHALO():
    pl,wa,G=pair_dawn()
    def upd(t):
        stand(pl,t); blink(pl,t); stand(wa,t); blink(wa,t); facing(pl,wa['root'].location); facing(wa,pl['root'].location); look_at(pl,hp(wa),.7); look_at(wa,hp(pl),.6)
        talk(pl,t,*wt(241,244),rest='smile'); face(pl,brow=.03); face(wa,mouth='flat',eyes=.9)
        u=pl['u']; arm_to(pl,1,root_mat(pl)@Vector((.5*u,-1.7*u,4.0*u)),tl(t,ws(243),ws(244)))
        for H in G: stand(H,t); blink(H,t); facing(H,wa['root'].location); face(H,mouth='smile')
        c0,tg,ln=ots(pl,wa,3.2,30); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['CHALO']=CHALO
def RUK():
    pl,wa,G=pair_dawn()
    def upd(t):
        stand(pl,t); blink(pl,t); stand(wa,t); blink(wa,t); facing(pl,wa['root'].location); facing(wa,pl['root'].location); look_at(pl,hp(wa),.7); look_at(wa,hp(pl),.6)
        talk(wa,t,*wt(245,251),rest='grin'); face(wa,brow=.04); face(pl,mouth='O' if t>we(251) else 'flat',eyes=1.15 if t>we(251) else .9,brow=.04)
        wa['arm'][-1].rotation_euler=(R(-70),0,R(-12)); kb=tl(t,ws(249),ws(250)); wa['arm'][1].rotation_euler=(R(-60-50*kb),0,R(15))
        for H in G: stand(H,t); blink(H,t); facing(H,wa['root'].location); face(H,mouth='grin')
        c0,tg,ln=ots(wa,pl,3.2,30); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['RUK']=RUK
def OUTRO():
    pl,wa,G=pair_dawn()
    more=[mk(CROWD[c],PARK_X+x,PARK_Y+y,0,'o%d'%c) for c,x,y in ((6,-3.2,3.0),(11,-4.6,3.2),(19,3.8,4.0))]
    def upd(t):
        for H in [pl]+G+more:
            stand(H,t); blink(H,t); facing(H,(PARK_X,PARK_Y-2)); face(H,mouth='grin' if math.sin(t*2+H['seed'])>0 else 'smile'); wave_hi(H,t,.2+H['seed']%5*.12,1)
        stand(wa,t); blink(wa,t); facing(wa,(PARK_X,PARK_Y-2)); face(wa,mouth='grin',brow=.05); wa['arm'][-1].rotation_euler=(R(-70),0,R(-12)); wa['arm'][1].rotation_euler=(R(-150),0,R(15))
        q=ease(t/DUR); camset(LV((PARK_X+.2,PARK_Y-4.0,1.6),(PARK_X+.2,PARK_Y-5.2,2.6),q),(PARK_X-.4,PARK_Y+4.4,1.6),L(26,20,q),6)
    return dict(upd=upd)
SHOTS['OUTRO']=OUTRO
def CTA():
    bw,E=stall_set('golden',n_eaters=0); pl=empty((SX-.4,SY-.4,1.12)); ocyl((0,0,0),.2,.02,M('#F7F5EF',.2),pl,rot=(0,0,0)); ocyl((0,0,.02),.16,.05,M('#E8A040',.75),pl,rot=(0,0,0))
    al=empty((SX-.34,SY-.42,1.2)); oico((0,0,0),.07,M('#E8D8A0',.6),al,sub=2)
    def upd(t):
        stand(bw,t); blink(bw,t); facing(bw,(SX-.4,SY-4)); face(bw,mouth='smirk',brow=-.04,brow_r=-10)
        u=bw['u']; arm_to(bw,1,Vector((SX-.34,SY-.42,1.32+.04*math.sin(t*3))),tl(t,.2,.6)); al.location=bw['arm'][1].matrix_world@Vector(hand_loc(bw,1)) if t>.6 else (SX-.34,SY-.42,1.2)
        q=ease(t/DUR); camset(LV((SX-.4,SY-2.0,1.55),(SX-.4,SY-1.6,1.5),q),(SX-.38,SY-.4,1.3),32,2.8)
    return dict(upd=upd)
SHOTS['CTA']=CTA
SEQ=[('HOOK', 0.0), ('FLIGHT', 3.033), ('DOODH', 7.433), ('POLICE', 9.167), ('ASK1', 10.833), ('ASK2', 17.667), ('HOUR', 21.6), ('STALL', 24.7), ('ALOO', 30.2), ('ABAY', 33.7), ('SIT', 35.633), ('TALEEM', 39.8), ('PLATES', 42.833), ('GIVEUP', 45.333), ('SHABASH', 48.167), ('DROP', 49.7), ('BAND', 53.433), ('RIVER', 55.267), ('CHILL', 59.033), ('DARK', 61.767), ('TORCH', 64.933), ('AIRRUN', 68.867), ('MERI', 73.7), ('FLIGHTQ', 75.133), ('WAIT', 79.067), ('CRICKET', 83.6), ('SUNRISE', 86.933), ('CHALO', 89.767), ('RUK', 91.5), ('OUTRO', 94.933), ('CTA', 100.2)]
END=103.6333
