# Shots part 2: apocalypse, restaurant, zombie army vs Karachi traffic, the bus.
def ots2(sp,ls,back=1.5,side=.8,dz=.2,tz=-.25,lens=38):
    a=Vector(hp(sp)); b=Vector(hp(ls)); d=(a-b); d.z=0; d.normalize(); pr=Vector((-d.y,d.x,0))
    c=b-d*back+pr*side+Vector((0,0,dz)); return (c.x,c.y,c.z),(a.x,a.y,a.z+tz),lens
def staff(H,s=1,h=3.5):
    u=H['u']; e=empty((s*1.52*u,-1.72*u,.04),H['root']); wd=M('#3A2A22',.6,kind='wood',sc=.6); gd=M('#E6B93A',.25,metal=.9)
    ocyl((0,0,h/2),.05,h,wd,e,rot=(0,0,0),seg=8); ocyl((0,0,h-.1),.12,.12,gd,e,rot=(0,0,0),seg=8); oico((0,0,h+.16),.2,M('#7CFF8A',.2,emit=6),e,sub=2)
    for k in range(3): a=k*2.1; obox((math.cos(a)*.17,math.sin(a)*.17,h+.12),(.025,.025,.16),gd,.005,e,rot=(0,0,a))
    return e
def kpose(H,s=1): H['arm'][s].rotation_euler=(R(-55),0,0)
# ---------------------------------------------------------------- APOC: they come out of the sea
def APOC():
    BE=beach('night',sign_at=(60,-9),ssize=.36); FILLE[0]=28
    cs=(ZKING,ZED,ZVAR[8],ZVAR[2],ZVAR[0],ZVAR[7],ZVAR[1],ZVAR[4]); pos=[(0,8.2),(-2.9,10.4),(3.0,10.8),(-5.6,12.6),(5.9,13.2),(-1.2,13.9),(2.2,16.0),(-8.4,15.4)]
    Z=[mk(C,0,0,0,'z%d'%i) for i,C in enumerate(cs)]; st=staff(Z[0],1)
    r=random.Random(5)
    for ix in range(10):
        for iy in range(7):
            y=20.5+iy*5.8+r.uniform(-1.5,1.5); x=-26+ix*5.7+r.uniform(-1.5,1.5); tok_z(r,x,y,r.uniform(-8,8),z=-min(1.75,(y-5)*.2))
    B.done('seaz')
    point((0,16,5),1600,(.5,1.0,.65),r=3,shadow=False); point((0,3,6),1100,(.6,.75,1.0),r=3,shadow=False); point((0,9,4),900,(.75,.85,1.0),r=2,shadow=False)
    def upd(t):
        for i,H in enumerate(Z):
            x,y0=pos[i]; d=.95*t+ .0; y=y0-d; z=-min(1.75,max(0,(y-4.6))*.2); H['z0']=z
            H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=0
            walk(H,d+i*.27,step=.36 if i else .5,arm=0)
            if i: zpose(H,t); H['root'].rotation_euler[1]+=R(3.5)*math.sin(t*3.1+H['seed'])
            else: zpose(H,t,base=-70); kpose(H,1)
            blink(H,t); face(H,mouth='flat' if i else 'frown',brow=-.03,brow_r=-12)
        q=ease(t/DUR); camset(LV((1.2,.6,.8),(1.5,-1.2,.9),q),LV((0,7.4,3.0),(0,5.6,2.8),q),L(24,26,q),8)
    return dict(upd=upd)
SHOTS['APOC']=APOC
# ---------------------------------------------------------------- MOVIES: in the movies everyone screams and runs
def MOVIES():
    MV=movie_street(); FILLE[0]=60; bars=letterbox(26)
    ppl=[dict(FRIENDS[3]),dict(FRIENDS[0]),dict(CROWD[7]),dict(CROWD[10]),dict(CROWD[14],kurta=False,shalwar=False,pants='#27365A',dupatta=None),dict(CROWD[3])]
    lanes=[(-4.3,13.0),(-2.2,9.5),(0.0,12.0),(2.2,19.5),(4.4,23.0),(-1.0,18.5)]
    P=[mk(C,0,0,-90,'run%d'%i) for i,C in enumerate(ppl)]
    Z=[mk(C,0,0,-90,'mz%d'%i) for i,C in enumerate((ZVAR[8],ZVAR[2],ZVAR[5],ZVAR[9]))]; zl=[(-3.2,20.5),(1.2,22.5),(-1.0,25.5),(3.6,24.5)]
    r=random.Random(3)
    for ix in range(9):
        for iy in range(5): tok_z(r,30+ix*1.9+r.uniform(-.2,.2),-4.4+iy*2.2+r.uniform(-.15,.15),-90)
    G=B.done('mvz')
    def upd(t):
        for i,H in enumerate(P):
            y,x0=lanes[i]; d=3.1*t; H['root'].location[0]=x0-d; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(-90); run(H,d+i*.4); shock(H,1)
            H['arm'][1].rotation_euler[0]+=R(8)*math.sin(t*14+i); H['arm'][-1].rotation_euler[0]+=R(8)*math.sin(t*14+i+2); face(H,mouth='O',brow=.06,brow_r=14,eyes=1.2); blink(H,t,force=0)
        for i,H in enumerate(Z):
            y,x0=zl[i]; d=1.9*t; H['root'].location[0]=x0-d; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(-90); walk(H,d+i*.3,step=.42,arm=0); zpose(H,t); face(H,mouth='O',brow=-.03,brow_r=-12)
        for o in G: o.location=(-1.9*t,0,.06*abs(math.sin(t*3)))
        q=t/DUR; camset((3.4-2.4*t*.55,-.5+.5*q,1.05),(9.0-3.1*t*.55,.2,1.85),26,8)
    return dict(upd=upd)
SHOTS['MOVIES']=MOVIES
# ---------------------------------------------------------------- the restaurant
ZTAB=RTAB[0]; ZSEAT=(ZTAB[0]-1.28,ZTAB[1],90); ZENT=(0.0,BW+.9)
def rest_set(clock=(0,12),street=True,rdin=True,zed_cfg=ZED,dress=(2,1,2,1,2),rsign='CHACHA MAGHAZ HOUSE',mood='night',skip=(0,1),roof_sx=0.0):
    S=burns(mood,clock=clock,rest_sign=rsign,roof_sx=roof_sx); RT=rest_tables(dress=dress); TB=street_tables(8,skip=skip) if street else []; B.done('x')
    zed=mk(zed_cfg,ZENT[0],ZENT[1],180,'zed'); wa=mk(WAITER,1.3,BW+2.0,0,'waiter'); ck=mk(COOK,-4.9,BW+2.05,0,'cook')
    RD=diners(7,RT,skip=(0,)) if rdin else []; SD=diners(8,TB) if street else []
    def bg(t):
        upd_diners(RD,t); upd_diners(SD,t); cook_anim(ck,t); spin_fans(t)
    return dict(S=S,RT=RT,TB=TB,zed=zed,waiter=wa,cook=ck,bg=bg,RD=RD,SD=SD)
def waiter_idle(H,t,x,y,rz):
    hstand(H,t); H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(rz)
    H['arm'][-1].rotation_euler=(R(-72),0,R(-10)); H['arm'][1].rotation_euler=(R(-18),0,0)
def waiter_write(H,t,k=1.0):
    pd=H['kz']['pad'].matrix_world.translation; arm_to(H,1,(pd.x,pd.y,pd.z+.12+.02*math.sin(t*26)),k,base=(R(-18),0,0)); H['head'].rotation_euler[0]=R(16*k)
def BURNS():
    Q=rest_set(clock=(0,10),skip=(0,1,5)); zed=Q['zed']; wa=Q['waiter']; TC=ws(95)-.08; FILLE[0]=45
    Wk=kwalkers(9,((-WLANE,-1),),4,-30,-5)
    def upd(t):
        Q['bg'](t); upd_kwalkers(Wk,t); waiter_idle(wa,t,3.4,BW+4.2,-60)
        if t<TC:
            d=1.25*t; zed['root'].location[0]=-26.6+d; zed['root'].location[1]=WLANE; zed['root'].rotation_euler[2]=R(90); walk(zed,d,step=.36,arm=0); zpose(zed,t); blink(zed,t); face(zed,mouth='flat',brow=-.03,brow_r=-10)
            q=t/TC; camset((-19.4,.3,1.2),(-33.0,.9,5.3),L(20,21,q),8)
        else:
            zwalk(zed,[(-1.6,2.3),(-.2,3.6),(0,BW+.5)],t,TC,DUR+.25,ease_in=.1,ease_out_=.3); blink(zed,t); face(zed,mouth='O' if t>DUR-.5 else 'flat',brow=-.03,brow_r=-10)
            q=ease((t-TC)/(DUR-TC)); camset(LV((3.9,-4.9,1.75),(3.3,-4.3,1.8),q),LV((.2,BW,2.9),(.1,BW+.4,2.9),q),L(19,20,q),8)
    return dict(upd=upd)
SHOTS['BURNS']=BURNS
def zed_roar(zed,t,k=1.0):
    stand(zed,t); zed['root'].location[0]=ZENT[0]; zed['root'].location[1]=ZENT[1]; zed['root'].rotation_euler[2]=R(180)
    for s in (1,-1): zed['arm'][s].rotation_euler=(R(L(-84,-158,k)),R(-s*24*k),R(s*5*math.sin(t*22)*k))
    zed['head'].rotation_euler=(R(-14*k),0,R(3*math.sin(t*25)*k)); face(zed,mouth='shout' if k>.3 else 'flat',brow=-.04,brow_r=-16); zeyes(zed,1+.3*k)
def BRAINS():
    Q=rest_set(clock=(0,11)); zed=Q['zed']; wa=Q['waiter']; FILLE[0]=55
    point((0,BW-1.6,3.0),240,(.45,1.0,.55),r=1.5,shadow=False)
    def upd(t):
        Q['bg'](t); waiter_idle(wa,t,3.4,BW+4.2,-60); k=tl(t,.02,.22)
        zed_roar(zed,t,k); SHAKE[0]=.012*k
        q=ease(t/DUR); camset(LV((.95,BW+3.5,.95),(.8,BW+3.1,1.0),q),(0,BW+.9,2.05),L(23,25,q),4.0)
    return dict(upd=upd)
SHOTS['BRAINS']=BRAINS
def NOBODY():
    Q=rest_set(clock=(0,11),street=False); zed=Q['zed']; wa=Q['waiter']; FILLE[0]=40
    def upd(t):
        Q['bg'](t); waiter_idle(wa,t,3.4,BW+4.2,-60); wa['head'].rotation_euler=(R(14),0,0)
        zed_roar(zed,t,1-.55*tl(t,.35,1.0)); face(zed,mouth='O')
        q=ease(t/DUR); camset(LV((-1.25,BW-1.5,2.85),(-1.1,BW-1.2,2.8),q),(1.0,BW+5.6,1.15),22,8)
    return dict(upd=upd)
SHOTS['NOBODY']=NOBODY
WPOS=(1.35,BW+2.0)
def zw_pose(Q,t,write=1.0):
    zed=Q['zed']; wa=Q['waiter']
    stand(zed,t); zed['root'].location[0]=ZENT[0]; zed['root'].location[1]=ZENT[1]; zed['root'].rotation_euler[2]=R(face_dir(WPOS[0]-ZENT[0],WPOS[1]-ZENT[1])); zpose(zed,t,.45,base=-60); blink(zed,t)
    waiter_idle(wa,t,WPOS[0],WPOS[1],face_dir(ZENT[0]-WPOS[0],ZENT[1]-WPOS[1])); blink(wa,t)
def WAITERS():
    Q=rest_set(clock=(0,12),street=False,rdin=False); zed=Q['zed']; wa=Q['waiter']; FILLE[0]=30; wa['z0']=-40
    P=Vector((1.3,BW+2.6,1.45)); e=empty(tuple(P),rot=(R(52),0,0)); sk=M(WAITER['skin'],.55); ink=M('#1E2A6A',.5)
    obox((0,0,0),(.2,.27,.012),M('#F8F6EE',.75),.004,e); obox((0,.245,.014),(.2,.028,.004),M('#C8372D',.6),.001,e)
    for k in range(7): obox((0,.17-k*.062,.0125),(.185,.0012,.0008),M('#9AB8E0',.6),0,e)
    def tx(body,x,y,sz,m):
        o=text(body,(x,y,.0135),(0,-1,0),sz,m,ex=.0006,parent=e); o.rotation_euler=(0,0,0); return o
    tx('ORDER',0,.2,.04,M('#C8372D',.5)); W3=[tx('ONE',-.11,.105,.05,ink),tx('BRAIN',.065,.105,.05,ink),tx('MASALA',-.03,.035,.05,ink)]
    obox((-.25,-.2,-.035),(.075,.1,.05),sk,.02,e); obox((-.33,-.33,-.05),(.09,.12,.07),M('#F4F1EA',.8,kind='fabric'),.02,e)
    hd=empty((0,0,0),e); obox((.05,-.07,.05),(.06,.07,.045),sk,.02,hd); obox((.14,-.2,.045),(.085,.11,.065),M('#F4F1EA',.8,kind='fabric'),.02,hd)
    ocyl((-.005,.015,.07),.011,.2,M('#F2C14E',.5),hd,rot=(R(-38),R(-20),0),seg=6)
    T3=(.2,.47,.75); X3=((-.16,.105),(-.02,.105),(-.1,.035),(.08,.035))
    def upd(t):
        Q['bg'](t); stand(zed,t); zed['root'].location[0]=ZENT[0]; zed['root'].location[1]=ZENT[1]; hstand(wa,t)
        for i,o in enumerate(W3):
            k=min(1,max(0,(t-T3[i])/.2)); o.scale=(k,1,1) if k>0 else (0,0,0)
        q=min(1,max(0,(t-.15)/.85)); i=min(2,int(q*3)); f=q*3-i; a=Vector((X3[i][0],X3[i][1],0)); b_=Vector((X3[i][0]+.16,X3[i][1],0)) if i<2 else Vector((X3[3][0],X3[3][1],0))
        p=a.lerp(b_,f); r_=tl(t,1.0,1.18); hd.location=(p.x+.17*r_,p.y-.14*r_+.01*math.sin(t*40)*(1-r_),.03*r_)
        n=Vector((0,-math.sin(R(52)),math.cos(R(52)))); c=P+n*.82+Vector((.1,0,.05)); camset(tuple(c),tuple(P+Vector((0,0,.02))),50,2.8)
    return dict(upd=upd)
SHOTS['WAITER']=WAITERS
def ORDER():
    Q=rest_set(clock=(0,12),street=False); zed=Q['zed']; wa=Q['waiter']; FILLE[0]=30
    def upd(t):
        Q['bg'](t); zw_pose(Q,t); k=1-tl(t,ws(113)-.15,ws(113)+.1); waiter_write(wa,t,k); wa['head'].rotation_euler[0]=R(16*k)
        for s_ in (1,-1): zed['arm'][s_].rotation_euler=(R(-14+3*math.sin(t*1.7+s_)),0,0)
        zed['head'].rotation_euler[1]=R(7*math.sin(t*1.3))
        talk(wa,t,*wt(110,115),rest='smile'); face(wa,brow=.05*(1-k)); look_at(wa,hp(zed),1-k,maxpitch=20)
        if k<.5: wa['arm'][1].rotation_euler=(R(-44-6*math.sin(t*9)),R(-14),R(10))
        c,tg,ln=ots2(wa,zed,back=.12,side=-1.0,dz=.1,tz=-.4,lens=37); q=ease(t/DUR); camset(c,tg,ln+2.0*q,5.6)
    return dict(upd=upd)
SHOTS['ORDER']=ORDER
def spoon(H,s=1):
    def b(e): obox((0,-.05,.1),(.012,.012,.14),M('#C9CED8',.25,metal=.9),.004,e); oico((0,-.05,.26),.045,M('#C9CED8',.25,metal=.9),e,sc=(1,.5,1.3),sub=1); oico((0,-.06,.27),.035,M('#B5642A',.5),e,sc=(1,.5,1.1),sub=1)
    return in_hand(H,s,b)
def zed_sit(zed,t):
    sitat(zed,ZSEAT,t); zed['head'].rotation_euler[1]=0
def zed_eat(zed,sp,t,c):
    """c 0..1: spoon from karahi to mouth"""
    m=root_mat(zed); mouth=m@Vector((.05,-.36,1.9)); pl=Vector((ZTAB[0]-.25,ZTAB[1]-.1,1.52)); arm_to(zed,1,pl.lerp(mouth,c),1); upright(sp,zed,1)
    rs=m@Vector((-.36,-.82,0)); rs.z=1.44; arm_to(zed,-1,rs,1)
def BITE():
    Q=rest_set(clock=(0,14),street=False); zed=Q['zed']; wa=Q['waiter']; sp=spoon(zed,1); FILLE[0]=30
    def upd(t):
        Q['bg'](t); zed_sit(zed,t); waiter_idle(wa,t,ZTAB[0]+.9,ZTAB[1]+1.75,0); wa['arm'][-1].rotation_euler=(R(-10),0,0); wa['kz']['pad'].scale=(0,0,0); look_at(wa,hp(zed),.6); face(wa,mouth='smile')
        c=tl(t,ws(119)-.1,ws(121)-.15); zed_eat(zed,sp,t,c)
        zed['head'].rotation_euler[0]=R(L(20,2,c)); face(zed,mouth='flat' if c<.92 else 'o',brow=.05 if c<.9 else .02,brow_r=10 if c<.9 else 0); zeyes(zed,1.0)
        q=ease(t/DUR); camset(LV((6.75,ZTAB[1]-1.25,1.8),(6.45,ZTAB[1]-1.05,1.82),q),(ZSEAT[0]+.25,ZSEAT[1],1.72),L(30,33,q),4.0)
    return dict(upd=upd)
SHOTS['BITE']=BITE
def EYES():
    Q=rest_set(clock=(0,14),street=False,rdin=False); zed=Q['zed']; wa=Q['waiter']; sp=spoon(zed,1); FILLE[0]=30
    h0=(ZSEAT[0],ZSEAT[1],1.93); sparkles(h0,.75,ws(125)-.05,9,n=26,size=.035,seed=4,rise=.5)
    def upd(t):
        Q['bg'](t); zed_sit(zed,t); waiter_idle(wa,t,ZTAB[0]+.9,ZTAB[1]+1.75,0)
        zed_eat(zed,sp,t,.25); k=tl(t,ws(125)-.12,ws(125)+.12); zglow(zed,1.25*k+.08*k*math.sin(t*14)); zeyes(zed,1+.35*k)
        zed['head'].rotation_euler[0]=R(-4*k); face(zed,mouth='o' if k<.5 else 'grin',brow=.06*k,brow_r=0); blink(zed,t,force=0)
        q=ease(t/DUR); camset(LV((5.25,ZTAB[1]-.55,1.9),(4.95,ZTAB[1]-.45,1.92),q),(ZSEAT[0],ZSEAT[1],1.9),L(48,52,q),2.8)
    return dict(upd=upd)
SHOTS['EYES']=EYES
def KYA():
    Q=rest_set(clock=(0,15),street=True,roof_sx=1.75); zed=Q['zed']; wa=Q['waiter']; sp=spoon(zed,1); FILLE[0]=30
    def upd(t):
        Q['bg'](t); zed_sit(zed,t); waiter_idle(wa,t,ZTAB[0]+.9,ZTAB[1]+1.75,0); wa['kz']['pad'].scale=(0,0,0); wa['arm'][-1].rotation_euler=(R(-10),0,0)
        zed_eat(zed,sp,t,.12); zglow(zed,.5); zeyes(zed,1.2); talk(zed,t,*wt(127,130),rest='grin'); face(zed,brow=.06)
        look_at(zed,hp(wa),.85,maxyaw=80,maxpitch=25); k=tl(t,ws(128),ws(128)+.25); arm_to(zed,-1,(ZTAB[0],ZTAB[1],1.5),k,base=tuple(zed['arm'][-1].rotation_euler))
        q=ease(t/DUR); camset(LV((ZTAB[0]-.7,ZTAB[1]+2.8,2.2),(ZTAB[0]-.75,ZTAB[1]+2.5,2.15),q),(ZSEAT[0]+.15,ZSEAT[1],1.78),L(34,36,q),4.0)
    return dict(upd=upd)
SHOTS['KYA']=KYA
def MAGHAZ():
    REST_NOSIGN.add('FAMILY HALL UPSTAIRS'); Q=rest_set(clock=(0,15),street=False); zed=Q['zed']; wa=Q['waiter']; sp=spoon(zed,1); FILLE[0]=30; TC=ws(136)-.1
    u=zed['u']; bl=[ocyl((s*.43*u,-.62*u-.006,.36*u),.12*u,.006,M('#F08A8A',.7),zed['head']) for s in (-1,1)]
    hearts(lambda t: hp(zed,.35),TC+.2,TC+1.6,n=7,seed=2,size=.9)
    def upd(t):
        Q['bg'](t); zed_sit(zed,t); wx,wy=ZTAB[0]+.9,ZTAB[1]+1.75
        waiter_idle(wa,t,wx,wy,0); wa['kz']['pad'].scale=(0,0,0); talk(wa,t,*wt(131,141),rest='grin'); face(wa,brow=.05)
        g=math.sin(t*7.5); wa['arm'][1].rotation_euler=(R(-66-12*g),R(-14),0); wa['arm'][-1].rotation_euler=(R(-28),0,0); look_at(wa,hp(zed),.7,maxpitch=25)
        fast=t>=TC; c=.5+.5*math.sin(t*(13 if fast else 5)); zed_eat(zed,sp,t,c); zglow(zed,.6); zeyes(zed,1.2); face(zed,mouth='grin' if c<.6 else 'o',brow=.05)
        k=tl(t,TC,TC+.5)
        for o in bl: o.scale=(k,k,k)
        if not fast:
            look_at(zed,hp(wa),.5,maxyaw=70,maxpitch=20); q=ease(t/TC); camset(LV((4.5,ZTAB[1]-1.2,1.4),(4.6,ZTAB[1]-1.05,1.42),q),(wx,wy,2.02),L(29,31,q),4.0)
        else:
            q=ease((t-TC)/(DUR-TC)); camset(LV((7.1,ZTAB[1]-1.9,1.95),(6.9,ZTAB[1]-1.7,1.95),q),(ZSEAT[0]+.75,ZTAB[1]+.2,1.75),L(22,24,q),4.0)
    return dict(upd=upd)
SHOTS['MAGHAZ']=MAGHAZ
# ---------------------------------------------------------------- zombie army vs Shahrah-e-Faisal
KX,KY=0.0,6.9; JX=44.0; BUSX=JX+7.0
GEN=[(ZVAR[8],-2.7,4.4),(ZVAR[2],-2.7,9.5),(ZVAR[7],-5.3,6.9),(ZVAR[0],-5.4,2.5),(ZVAR[1],-5.5,11.3),(ZVAR[9],-8.0,4.6),(ZVAR[12],-8.1,9.2)]
def army(n=7):
    kg=mk(ZKING,KX,KY,90,'king'); st=staff(kg,1); Z=[mk(C,x,y,90,'gen%d'%i) for i,(C,x,y) in enumerate(GEN[:n])]; return kg,Z
def army_walk(kg,Z,t,s,x0=0.0):
    kg['root'].location[0]=KX+x0+s; kg['root'].location[1]=KY; kg['root'].rotation_euler[2]=R(90); walk(kg,s,step=.5,arm=16); kpose(kg,1); blink(kg,t); face(kg,mouth='frown',brow=-.04,brow_r=-14)
    for i,H in enumerate(Z):
        C,x,y=GEN[i]; H['root'].location[0]=x+x0+s; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(90); walk(H,s+i*.3,step=.36,arm=0); zpose(H,t); H['root'].rotation_euler[1]+=R(3.5)*math.sin(t*3.1+H['seed']); blink(H,t)
        face(H,mouth='O' if (i+int(t*2))%3==0 else 'flat',brow=-.03,brow_r=-10)
def jam(seed=31,x1=JX+125,night=False,bus=True,south=True):
    def skip(cx,y,L_): return bus and abs(y-LANES[2])<1.5 and abs(cx-BUSX)<L_/2+7.2
    T=traffic(seed,JX,x1,FLANES[:3],gap=(.9,1.7),mix=(50,18,20,9,3),skip=skip)
    TS=traffic(seed+1,-40,x1,FLANES[3:],gap=(2.0,5.0)) if south else []
    Bs=None
    if bus: Bs=w11((BUSX,LANES[2],0),0,seed=9,col='#2B58C9',accent='#F2C14E')
    return T,TS,Bs
def ARMY():
    faisal('khi_dusk',.55,stop_x=JX-6); FILLE[0]=90; kg,Z=army()
    G=horde(6,-10.5,18,2.5,5,dy=2.1); night_lights((-20,0,20),y=6,e=1800)
    def upd(t):
        s=1.0*t; army_walk(kg,Z,t,s); upd_horde(G,t,v=1.0)
        q=t/DUR; camset((5.2+s*.9,5.4+.4*q,.8+.2*q),(KX+s,KY,2.25),L(24,26,q),5.6)
    return dict(upd=upd)
SHOTS['ARMY']=ARMY
def FAISALS():
    faisal('khi_dusk',.55,stop_x=JX-6); FILLE[0]=0; kg,Z=army(5)
    T,TS,Bs=jam(south=False); bus_heads(Bs,random.Random(3))
    G=horde(7,-9.5,30,2.5,5,dy=2.1)+horde(8,-4.0,34,-10.9,5,dy=2.1)
    def upd(t):
        s=1.0*t; army_walk(kg,Z,t,s); upd_horde(G,t,v=1.0)
        q=ease(t/DUR); camset(LV((-50,9.5,20),(-30,8.2,13.5),q),LV((20,6.5,4),(36,6.9,6.5),q),L(26,30,q),8)
    return dict(upd=upd)
SHOTS['FAISAL']=FAISALS
def jam_scene(mood,night,clock_txt):
    faisal(mood,night,stop_x=JX-6,gantry_x=8)
    billboard(JX+12,RW+1.9,clock_txt,'#16171C','#FF5A2A',size=.7,z=9.0,n=(-1,0,0),e=4.0)
    T,TS,Bs=jam(); bus_heads(Bs,random.Random(3)); kg,Z=army()
    r=random.Random(9)
    for ix in range(14):
        for iy in range(5):
            x=JX-17.5-ix*1.7+r.uniform(-.2,.2); y=2.5+iy*2.1+r.uniform(-.12,.12); tok_z(r,x,y,90)
    B.done('jz')
    if night>.8: night_lights((JX-20,JX,JX+20,JX+40),y=6,e=2400)
    X0=JX-6.0   # king's x
    def place(t,slump=0.0):
        run_traffic(TS,t,.25)
        kg['root'].location[0]=X0; kg['root'].location[1]=KY; kg['root'].rotation_euler[2]=R(90); stand(kg,t); kpose(kg,1); blink(kg,t)
        for i,H in enumerate(Z):
            C,x,y=GEN[i]; H['root'].location[0]=X0+x*1.0; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(90)
            if slump and i in (0,3,5): sit(H,1,0.0,legs=90); H['arm'][1].rotation_euler=(R(-30),0,0); H['arm'][-1].rotation_euler=(R(-30),0,0); H['head'].rotation_euler=(R(26),0,R(8)); face(H,mouth='frown'); zeyes(H,.8)
            else: stand(H,t); zpose(H,t,1-slump*.8,base=-84); H['head'].rotation_euler=(R(14*slump),R(9),0); face(H,mouth='flat')
            blink(H,t)
    return dict(kg=kg,Z=Z,place=place,X0=X0,bus=Bs)
def SIXPM():
    J=jam_scene('khi_dusk',.55,'6:00 PM'); kg=J['kg']; FILLE[0]=60; TC=ws(159)-.12; X0=J['X0']
    def upd(t):
        J['place'](t)
        if t<TC:
            face(kg,mouth='O',brow=.05); q=ease(t/TC); camset(LV((X0-9,6.9,6.6),(X0-6.5,6.9,5.9),q),LV((JX+26,7.4,2.6),(JX+30,7.4,2.6),q),L(26,28,q),8)
        else:
            q=(t-TC)/(DUR-TC); kg['head'].rotation_euler=(0,0,R(22*math.sin(q*5.5))); face(kg,mouth='flat',brow=-.02,brow_r=4); zeyes(kg,1.15)
            camset((X0+3.1-.2*q,KY-1.0,2.85),(X0,KY,2.72),L(40,43,q),4.0)
    return dict(upd=upd)
SHOTS['SIXPM']=SIXPM
def FOURFEET():
    J=jam_scene('khi_night',1.0,'9:00 PM'); kg=J['kg']; Z=J['Z']; FILLE[0]=170; X0=J['X0']
    yl=M('#F2C14E',.5); wh=M('#F4F1EA',.6); SP=(X0+.05,2.55,1.25)
    B.box((X0-.55,3.6,.006),(.06,1.9,.006),wh,0); B.box((X0+.28,2.2,.03),(.61,.035,.03),yl,.005); B.box((X0-.4,2.2,.09),(.12,.1,.09),yl,.03)
    for k in range(5): B.box((X0-.2+k*.24,2.2,.062),(.006,.035,.004),M('#16171C',.5),0)
    B.done('tape'); sign('4 FT',SP,.40,'#16171C','#F2C14E',n=(-.7,-.7,0),e=1.2,pad=.18,th=.06,parent=empty((0,0,0)),always=True)
    obox((SP[0],SP[1],.44),(.04,.04,.44),M('#5A5E66',.5),0)
    def upd(t):
        J['place'](t,slump=1.0)
        Z[0]['root'].location[0]=X0+.2; Z[0]['root'].location[1]=7.0; Z[5]['root'].location[0]=X0+2.3; Z[5]['root'].location[1]=2.5
        q=ease(t/DUR); c=LV((X0-3.7,.65,2.5),(X0-3.3,.95,2.35),q); a=tl(t,1.0,1.4)
        kg['root'].location[1]=KY-2.6; kg['root'].rotation_euler[2]=R(-70); kg['arm'][-1].rotation_euler=(R(-12),0,0)
        look_at(kg,LV((SP[0],SP[1],1.6),(c[0],c[1],c[2]+.2),a),1.0,maxpitch=20)
        if t>1.5: kg['head'].rotation_euler[2]+=R(9*math.sin((t-1.5)*6.5))
        face(kg,mouth='frown' if a<.5 else 'flat',brow=-.03,brow_r=-8 if a<.5 else 5); zeyes(kg,.8)
        camset(c,LV((X0+2.4,5.4,.95),(X0+2.6,5.3,.9),q),L(21,23,q),8)
    return dict(upd=upd)
SHOTS['FOURFEET']=FOURFEET
# ---------------------------------------------------------------- the W-11
DOORX=BUSX-3.1; BY=LANES[2]
def bus_scene(packed=False,stop_wal=False):
    faisal('khi_night',1.0,stop_x=DOORX-9.5,clear=20.0,gantry_x=8); T,TS,Bs=jam(); FILLE[0]=70
    night_lights((JX-10,JX+10,JX+30),y=8,e=2600); point((BUSX-1,BY,3.0),420,(1,.9,.7),r=.8,shadow=False); point((DOORX+.5,BY+3.6,3.4),900,(1,.9,.75),r=1.2,shadow=False)
    co=mk(CONDUCTOR,DOORX,BY+1.2,180,'conductor',z=Bs['z0'])
    IN=[]; RF=[]
    if packed:
        bus_heads(Bs,random.Random(3),zombie=True,skipx=(-1.5,1.75,-4.3))
        for i,(C,lx) in enumerate(((ZVAR[7],-1.5),(ZVAR[6],1.75),(ZVAR[10],-4.3))):
            H=mk(C,BUSX+lx,BY+.78,180,'in%d'%i,z=Bs['z0']); IN.append(H)
        for i,(C,lx) in enumerate(((ZVAR[9],-2.6),(ZVAR[11],.3),(ZVAR[4],3.0))):
            H=mk(C,BUSX+lx,BY+.55,180,'rf%d'%i,z=0); RF.append(H)
    else: bus_heads(Bs,random.Random(3))
    def base(t):
        run_traffic(TS,t,.25)
        for i,H in enumerate(IN): stand(H,t); zpose(H,t,1.0,base=-97,amp=3); blink(H,t); face(H,mouth='O' if i==1 else 'flat')
        for i,H in enumerate(RF):
            sit(H,1,Bs['roof']+.17,legs=90); H['root'].rotation_euler[2]=R(180); zpose(H,t,.5,base=-50); blink(H,t); face(H,mouth='grin' if i==1 else 'flat'); H['head'].rotation_euler=(R(8),0,R(10*math.sin(t*1.2+i)))
    return dict(bus=Bs,co=co,base=base,IN=IN,RF=RF)
def cond_door(co,t,Bs,wave=0.0,lean=0.0):
    hstand(co,t); co['z0']=Bs['z0']; co['root'].location=(DOORX,BY+1.2,Bs['z0']+.008); co['root'].rotation_euler=(R(-6*lean),0,R(180))
    arm_to(co,-1,(DOORX-.58,BY+1.77,2.6),1); co['arm'][1].rotation_euler=(R(-95-40*wave*(.5+.5*math.sin(t*10))),R(-18),0)
def CONDUCTORS():
    Q=bus_scene(); co=Q['co']; Bs=Q['bus']
    Z=[mk(ZVAR[0],DOORX-2.0,BY+3.7,0,'w0'),mk(ZVAR[12],DOORX+2.3,BY+3.9,0,'w1'),mk(ZVAR[8],DOORX-3.9,BY+5.4,0,'w2')]
    def upd(t):
        Q['base'](t); cond_door(co,t,Bs,wave=tl(t,ws(172)-.2,ws(172)+.1),lean=1); talk(co,t,*wt(169,175),rate=8,rest='grin'); face(co,brow=.05)
        for i,H in enumerate(Z):
            stand(H,t); zpose(H,t,.5,base=-70); blink(H,t); look_at(H,hp(co),.8,maxpitch=30); face(H,mouth='O' if i==0 else 'flat',brow=.05,brow_r=8); H['head'].rotation_euler[1]=R(8 if i%2 else -8)
        q=ease(t/DUR); camset(LV((DOORX+.7,BY+6.6,1.85),(DOORX+.55,BY+6.0,1.9),q),(DOORX-.1,BY+1.4,2.6),L(29,31,q),5.6)
    return dict(upd=upd)
SHOTS['CONDUCTOR']=CONDUCTORS
def PACK():
    Q=bus_scene(packed=True); co=Q['co']; Bs=Q['bus']; z=mk(ZVAR[3],0,0,90,'last')
    def upd(t):
        Q['base'](t)
        k=tl(t,.3,2.6); y=L(3.3,1.75,k); zz=.52*(1-tl(y,2.1,2.5)) if y>2.0 else L(.52,Bs['z0'],1-tl(y,1.78,2.0))
        stand(z,t); z['z0']=zz; z['root'].location=(DOORX,BY+y,zz+.008); z['root'].rotation_euler=(0,0,R(90)); zpose(z,t,1,base=-84); face(z,mouth='O',brow=.05,brow_r=8); blink(z,t)
        hstand(co,t); co['z0']=0; cy=BY+y+1.8+.05*math.sin(t*16); co['root'].location=(DOORX,cy,.008); co['root'].rotation_euler=(R(7),0,0)
        for s in (1,-1): arm_to(co,s,(DOORX+s*.3,BY+y+.6,1.5+zz),1)
        face(co,mouth='strain',brow=-.03,brow_r=-10)
        q=ease(t/DUR); camset(LV((DOORX-4.6,BY+5.6,1.9),(DOORX-4.0,BY+5.2,2.1),q),LV((DOORX+1.6,BY+1.2,2.55),(DOORX+1.4,BY+1.2,2.6),q),L(19,20,q),8)
    return dict(upd=upd)
SHOTS['PACK']=PACK
WALP=(DOORX+3.4,BY+4.3); ZLAND=(DOORX+1.9,BY+3.15)
def scare_set():
    Q=bus_scene(packed=True); co=Q['co']; Bs=Q['bus']; z=mk(ZVAR[5],0,0,0,'fan'); wa=mk(WALEED,WALP[0],WALP[1],0,'wa'); ph=phone_in_hand(wa,1,'#BFE0FF',em=2.5)
    def wal(t,look=0.0):
        hstand(wa,t); wa['root'].location[0]=WALP[0]; wa['root'].location[1]=WALP[1]; wa['root'].rotation_euler[2]=R(35); hold_phone(wa,1,1.0); wa['arm'][-1].rotation_euler=(R(-6),0,0)
        wa['head'].rotation_euler=(R(L(22,2,look)),0,0)
    return dict(Q=Q,z=z,wa=wa,wal=wal,co=co,bus=Bs)
CONDG=(DOORX-1.9,BY+2.7)
def cond_ground(co,t,look):
    hstand(co,t); co['z0']=0; co['root'].location=(CONDG[0],CONDG[1],.008); co['root'].rotation_euler=(0,0,R(90)); co['arm'][1].rotation_euler=(R(-40),0,0); look_at(co,look,.7); face(co,mouth='smile')
def SCARE():
    S_=scare_set(); Q=S_['Q']; z=S_['z']; wa=S_['wa']; Bs=S_['bus']; co=S_['co']; TJ=ws(187)-.1
    def upd(t):
        Q['base'](t); cond_ground(co,t,(ZLAND[0],ZLAND[1],2))
        S_['wal'](t,0.0); face(wa,mouth='flat'); wa['arm'][1].rotation_euler[0]+=R(1.5*math.sin(t*12))
        if t<TJ:
            k0=tl(t,.05,TJ-.05); p=Vector((DOORX,BY+L(1.0,2.0,k0),L(Bs['z0'],.52,tl(k0,.55,1.0)))); hgt=0; k=0
        else:
            k=tl(t,TJ,TJ+.5); p0=Vector((DOORX,BY+2.0,.52)); p1=Vector((ZLAND[0],ZLAND[1],0)); p=p0.lerp(p1,k); hgt=.85*math.sin(pi*k)
        stand(z,t); z['z0']=p.z+hgt; z['root'].location=(p.x,p.y,p.z+hgt+.008); z['root'].rotation_euler=(0,0,R(L(180,face_dir(WALP[0]-ZLAND[0],WALP[1]-ZLAND[1]),k)))
        up=tl(t,TJ+.05,TJ+.45)
        for s in (1,-1): z['arm'][s].rotation_euler=(R(L(-84,-150,up)),R(-s*50*up),R(s*6*math.sin(t*24)*up))
        if k>=1: z['root'].location[2]=.008+.03*abs(math.sin((t-TJ)*9))*max(0,1-(t-TJ-.5)*2)
        z['head'].rotation_euler=(R(-10*up),0,R(4*math.sin(t*26)*up)); face(z,mouth='shout' if up>.4 else 'flat',brow=-.04,brow_r=-16); zeyes(z,1+.3*up); zglow(z,.5*up); blink(z,t,force=0)
        q=ease(t/DUR); camset(LV((DOORX+8.9,BY+2.7,1.75),(DOORX+8.1,BY+2.7,1.75),q),(DOORX+2.5,BY+3.5,1.85),L(26,28,q),5.6)
    return dict(upd=upd)
SHOTS['SCARE']=SCARE
def HALKA2():
    S_=scare_set(); Q=S_['Q']; z=S_['z']; wa=S_['wa']; Bs=S_['bus']; co=S_['co']
    def upd(t):
        Q['base'](t); cond_ground(co,t,hp(wa))
        lk=tl(t,ws(195)-.15,ws(195)+.1)*(1-tl(t,ws(200)+.25,ws(200)+.5)); S_['wal'](t,lk); talk(wa,t,*wt(195,200),rest='flat'); face(wa,brow=-.01,brow_r=3)
        if lk>.3: look_at(wa,hp(z),.5*lk,maxpitch=10)
        dr=tl(t,ws(197),ws(199)); stand(z,t); z['root'].location=(ZLAND[0],ZLAND[1],.008); z['root'].rotation_euler=(0,0,R(face_dir(WALP[0]-ZLAND[0],WALP[1]-ZLAND[1])))
        for s in (1,-1): z['arm'][s].rotation_euler=(R(L(-150,-4,dr)),R(-s*50*(1-dr)),0)
        z['head'].rotation_euler=(R(L(-10,16,dr)),0,0); face(z,mouth='shout' if dr<.2 else 'frown',brow=L(-.04,.05,dr),brow_r=L(-16,12,dr)); zeyes(z,L(1.3,.9,dr)); zglow(z,.5*(1-dr))
        h=hp(wa); q=ease(t/DUR); camset(LV((DOORX+5.3,BY+2.25,1.9),(DOORX+5.0,BY+2.3,1.92),q),(h[0]-.45,h[1]-.2,h[2]-.15),L(33,36,q),4.0)
    return dict(upd=upd)
SHOTS['HALKA2']=HALKA2
