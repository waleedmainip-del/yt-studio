# Shots for "Everyone Is From Karachi" (part 1: helpers + act 1). SEQ/END filled by gen_seq.py.
SHOTS={}
END=120.2
SEQ=[('HOOK', 0.0), ('EVERY', 2.467), ('PM', 4.133), ('ASTRO', 6.033), ('ZOMB', 8.0), ('ZCHAI', 10.233), ('RUMOUR', 11.4), ('THREEAM', 14.333), ('CHAIAUR', 18.233), ('SHOCKS', 19.967), ('FLOOD', 22.033), ('BLACKOUT', 22.933), ('QUAKE', 23.767), ('ANSWER', 24.6), ('HALKA1', 27.0), ('APOC', 29.267), ('MOVIES', 32.033), ('BURNS', 35.533), ('BRAINS', 38.767), ('NOBODY', 40.4), ('WAITER', 41.567), ('ORDER', 42.967), ('BITE', 45.267), ('EYES', 47.833), ('KYA', 49.433), ('MAGHAZ', 51.333), ('ARMY', 54.833), ('FAISAL', 57.533), ('SIXPM', 60.367), ('FOURFEET', 62.9), ('CONDUCTOR', 65.7), ('PACK', 68.7), ('SCARE', 72.033), ('HALKA2', 74.933), ('PLAN', 77.2), ('ONEAM', 80.033), ('TWOAM', 81.833), ('THREEAM2', 83.567), ('FOURAM', 85.4), ('SUNRISE', 87.467), ('ENOUGH', 90.967), ('LEAVING', 93.1), ('NOBODY2', 94.9), ('RICK', 96.4), ('CHAIZ', 98.267), ('CRICZ', 99.6), ('BOSS', 101.633), ('MONTH', 104.033), ('MONDAY', 106.967), ('KINGQ', 111.567), ('RESTO', 112.767), ('DIEFOR', 114.767), ('CTA', 117.533)]
FILLE=[35.0]; _FL=[]
_camset0=camset
def camset(loc,tg,lens,*a,**k):
    _camset0(loc,tg,lens,*a,**k)
    if not _FL: _FL.append(point((0,0,0),FILLE[0],(1,.93,.85),r=.4,shadow=False)); _FL[0].data.specular_factor=0
    _FL[0].location=Vector(loc)+Vector((0,0,.3)); _FL[0].data.energy=FILLE[0]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0
def we(i): return W_[i]['e']-T0
def mk(C,x,y,rz,name,z=0.0): return avatar_kz((x,y,z),rz,C,name=name)
def fwd(rz): return (math.sin(R(rz)),-math.cos(R(rz)))
def closecam(H,rz,side=.3,dist=3.0,dz=.05,tz=-.3,lens=36):
    h=hp(H); f=fwd(rz); rt=(-f[1],f[0])
    return (h[0]+f[0]*dist+rt[0]*side,h[1]+f[1]*dist+rt[1]*side,h[2]+dz),(h[0],h[1],h[2]+tz),lens
def facing(H,p):
    r=H['root'].location; H['root'].rotation_euler[2]=R(face_dir(p[0]-r.x,p[1]-r.y))
def wave_hi(H,t,t0,s=1,dur=1.4):
    k=tl(t,t0,t0+.25)*(1-tl(t,t0+dur,t0+dur+.3)); H['arm'][s].rotation_euler=(R(-165*k),0,R(s*(12+10*math.sin((t-t0)*10))*k))
def upright(e,H,s,tilt=0.0,yaw=0.0):
    """keep a hand-held prop level whatever the arm does"""
    e.rotation_euler=(H['arm'][s].rotation_euler.to_matrix().inverted()@Euler((R(tilt),0,R(yaw))).to_matrix()).to_euler()
def chai_cup(e,s=1.0):
    ocyl((0,-.07,.07*s),.056*s,.14*s,M('#F6F4EE',.4),e,rot=(0,0,0),seg=14,r2=.076*s); ocyl((0,-.07,.136*s),.066*s,.012,M('#B5713A',.5),e,rot=(0,0,0),seg=14)
    obox((.088*s,-.07,.08*s),(.024*s,.012*s,.04*s),M('#F6F4EE',.4),.006,e)
def chai(H,s=1,sc=1.4): return in_hand(H,s,lambda e: chai_cup(e,sc))
def hold_chai(H,e,s=1,a=-62,sip=0.0,out=0.0):
    """arm forward with a level cup; sip 0..1 brings it to the mouth; out = degrees away from the body"""
    base=(R(a),R(-s*out),R(s*8)); H['arm'][s].rotation_euler=base
    if sip>0:
        m=root_mat(H); hh=H['C'].get('h',1.0); arm_to(H,s,m@Vector((s*.14,-.5*hh,1.78*hh)),sip,base=base)
    upright(e,H,s,tilt=-28*sip)
def spread(H,k,ang=68,fw=-10):
    for s in (1,-1): H['arm'][s].rotation_euler=(R(fw*k),R(-s*ang*k),0)
def zpose(H,t,k=1.0,amp=5.0,base=-84):
    for s in (1,-1): H['arm'][s].rotation_euler=(R(base+amp*math.sin(t*2.3+H['seed']+s))*k,0,R(s*4))
    H['head'].rotation_euler[1]=R(9*k)
def zwalk(H,pts,t,t0,t1,step=.36,**kw):
    q=walk_path(H,pts,t,t0,t1,step=step,arm=0,**kw); zpose(H,t); H['root'].rotation_euler[1]+=R(3.5)*math.sin(t*3.1+H['seed']); return q
def zstand(H,t,k=1.0):
    stand(H,t); zpose(H,t,k); blink(H,t)
def hstand(H,t):
    stand(H,t); blink(H,t)
    for s in (1,-1): H['arm'][s].rotation_euler=(R(2*math.sin(t*1.3+H['seed']+s)),0,0)
# ---------------------------------------------------------------- traffic
def simple_rider(V,r):
    root=V['root']; top=M(r.choice(TOKC),.8); sk=M(r.choice(TOKS),.55); pn=M(r.choice(['#2A2C34','#3A4A6A','#8A7A5A']),.85)
    obox((-.27,0,1.26),(.17,.27,.38),top,.04,root); obox((-.22,0,1.84),(.2,.2,.2),sk,.05,root); obox((-.22,.0,1.97),(.215,.215,.1),M(r.choice(['#15110E','#C8372D','#2A2C34','#F4F1EA','#2B58C9']),.45),.05,root)
    for sy in (-1,1):
        obox((.2,sy*.3,1.38),(.43,.075,.075),top,.02,root,rot=(0,R(19),0)); obox((-.05,sy*.2,.9),(.24,.1,.1),pn,.03,root); obox((.14,sy*.22,.62),(.09,.09,.26),pn,.03,root)
def rick_people(V,r,passenger=True):
    root=V['root']; sk=M(r.choice(TOKS),.55); tp=M(r.choice(['#8A6A4A','#D8CFB4','#5A7FB0','#B8B0A0']),.8)
    obox((.5,0,1.36),(.2,.4,.5),tp,.05,root); obox((.52,0,2.12),(.25,.25,.25),sk,.05,root); obox((.52,.0,2.34),(.265,.265,.07),M('#15110E',.6),.03,root)
    obox((.95,0,1.0),(.45,.38,.17),M('#3A3D47',.85),.04,root)
    for sy in (-1,1): obox((1.02,sy*.5,1.6),(.5,.085,.085),tp,.02,root,rot=(0,R(12),0))
    if passenger:
        pt=M(r.choice(TOKC),.8)
        obox((-1.4,0,1.3),(.2,.42,.5),pt,.05,root); obox((-1.38,0,2.05),(.24,.24,.24),M(r.choice(TOKS),.55),.05,root); obox((-1.38,.0,2.27),(.255,.255,.07),M(r.choice(['#15110E','#2A1E16']),.6),.03,root)
        obox((-.95,0,.98),(.45,.38,.17),pt,.04,root)
def bus_heads(V,r,zombie=False,skipx=()):
    root=V['root']
    for sy in (-1,1):
        for (x,y,z) in V['wins'][sy]:
            for dx in (-.38,.38):
                if r.random()<.2: continue
                if sy==1 and any(abs(x+dx-sx_)<1.35 for sx_ in skipx): continue
                sk=M(r.choice(ZS) if zombie else r.choice(TOKS),.55); zz=z-.12+r.uniform(-.06,.06)
                obox((x+dx,y-sy*.42,zz),(.26,.26,.25),sk,.05,root); obox((x+dx,y-sy*.4,zz+.25),(.275,.275,.07),M(r.choice(['#15110E','#2A1E16','#22301E']),.6),.03,root)
                obox((x+dx,y-sy*.42,zz-.55),(.4,.22,.3),M(r.choice(TOKC),.8),.04,root)
                for ex in (-.1,.1): obox((x+dx+ex,y-sy*.155,zz+.03),(.045,.006,.055),M('#F4F06A',.3,emit=1.8) if zombie else M('#1B1B22',.6),0,root)
VLEN=dict(car=6.6,rick=4.8,bike=3.2,bus=11.4,tank=10.8)
def mkveh(kind,x,y,d,r,i):
    rz=0 if d>0 else 180
    if kind=='car': V=kcar((x,y,0),rz,r.choice(CARC),seed=i)
    elif kind=='rick': V=krick((x,y,0),rz,r.choice(['#2E8A3A','#2B58C9','#F2C14E','#C8372D','#16909E']),seed=i); rick_people(V,r,r.random()<.7)
    elif kind=='bike': V=kbike((x,y,0),rz,r.choice(['#C8372D','#16171C','#2B58C9','#F2C14E'])); simple_rider(V,r)
    elif kind=='bus': V=w11((x,y,0),rz,seed=i,col=r.choice(['#2B58C9','#1E8A4A','#C8372D','#7448C2','#D9811A','#16909E']),accent=r.choice(['#F2C14E','#F4F1EA','#FF8A3A'])); bus_heads(V,r)
    else: V=tanker((x,y,0),rz,col=r.choice(['#F2C14E','#E2702A','#F4F1EA']))
    V['kind']=kind; V['x0']=x; V['y']=y; V['d']=d; V['rz']=rz; return V
def traffic(seed,xa,xb,lanes,gap=(2.5,7.0),mix=(52,16,18,10,4),skip=None):
    """fill lanes [(y,dir,speed),...] with vehicles between xa..xb (no overlaps). returns list"""
    r=random.Random(seed); T=[]; i=0
    for (y,d,v) in lanes:
        x=xa+r.uniform(0,5)
        while x<xb:
            k=r.choices(['car','rick','bike','bus','tank'],mix)[0]
            if abs(y)<5 and k in ('bus','tank'): k='car'
            L_=VLEN[k]
            if x+L_>xb: break
            cx=x+L_/2
            if not (skip and skip(cx,y,L_)):
                V=mkveh(k,cx,y+(r.uniform(-.5,.5) if k=='bike' else r.uniform(-.15,.15)),d,r,seed*100+i); V['v']=v; T.append(V); i+=1
            x+=L_+r.uniform(*gap)
    return T
def run_traffic(T,t,k=1.0):
    for V in T:
        dx=V['d']*V['v']*t*k; roll(V,V['x0']+dx,V['y'],V['rz'],V['v']*t*k)
FLANES=[(LANES[0],1,12.5),(LANES[1],1,10.0),(LANES[2],1,7.5),(-LANES[0],-1,12.5),(-LANES[1],-1,10.0),(-LANES[2],-1,7.5)]
def sidewalk_tokens(seed,xa,xb,n,sides=(1,-1),skip=None,stop_x=None):
    """static pedestrians on a 1.9 m grid along the sidewalks (never overlapping each other, trees, bins or the bus stop)"""
    r=random.Random(seed); cells=[(s,xa+.95+k*1.9) for s in sides for k in range(int((xb-xa)/1.9))]; r.shuffle(cells)
    for (s,x) in cells[:n]:
        y=s*(RW+r.uniform(2.85,3.7)); x+=r.uniform(-.05,.05)
        if skip and skip(x,y): continue
        if stop_x is not None and s>0 and abs(x-stop_x)<3.5: continue
        tok_h(r,x,y,r.choice([90,-90,90,-90,0,180]))
# ---------------------------------------------------------------- HOOK: aerial glide down the boulevard
def HOOK():
    faisal('khi',0.0,gantry_text='WELCOME TO KARACHI')
    T=traffic(11,-70,150,FLANES,gap=(3,9))
    sidewalk_tokens(3,-60,150,150,stop_x=0); B.done('ppl')
    def upd(t):
        run_traffic(T,t)
        q=ease_out(t/DUR)
        camset(LV((-62,3.5,32),(-7,6.2,11.6),q),LV((0,5,6),(34,6.9,7.3),q),L(22,27,q),8)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
# ---------------------------------------------------------------- food-street helpers
def sitat(H,st,t,h=.56):
    seat(H,t,h); H['root'].location[0]=st[0]; H['root'].location[1]=st[1]; H['root'].rotation_euler[2]=R(st[2])
def diner(H,st,t,ph=0.0,eating=True,rate=4.5):
    sitat(H,st,t); m=root_mat(H); c=.5+.5*math.cos(t*rate+ph); hh=H['C'].get('h',1.0)
    mouth=m@Vector((.05,-.34,1.9*hh)); pl=m@Vector((.3,-.95,0)); pl.z=1.42; rs=m@Vector((-.36,-.82,0)); rs.z=1.44
    arm_to(H,1,pl.lerp(mouth,c if eating else 0),1); arm_to(H,-1,rs,1); H['head'].rotation_euler[0]=R(9+7*c if eating else 3)
def kwalkers(seed,lanes,n_per,x0,x1,pool=None,v=1.0):
    r=random.Random(seed); P=[]; pool=pool or CROWD; k=0
    for (y,d) in lanes:
        for i in range(n_per):
            C=pool[(seed*7+k*5)%len(pool)]; H=mk(C,0,y,90*d,'wk%d_%d'%(seed,k)); P.append(dict(H=H,x0=x0+(x1-x0)*(i+r.uniform(.25,.6))/n_per,y=y,d=d,v=v)); k+=1
    return P
def upd_kwalkers(P,t):
    for p in P:
        H=p['H']; H['root'].location[0]=p['x0']+p['d']*p['v']*t; H['root'].location[1]=p['y']; H['root'].rotation_euler[2]=R(90*p['d']); walk(H,p['v']*t,step=.5); blink(H,t)
def diners(seed,tabs,skip=(),pool=None):
    D=[]; k=0; pool=pool or CROWD
    for i,tb in enumerate(tabs):
        if tb is None or i in skip: continue
        for j,st in enumerate(tb[1]):
            C=pool[(seed*3+k*7)%len(pool)]
            if C.get('h',1)<.8: C=pool[(seed*3+k*7+1)%len(pool)]
            D.append((mk(C,st[0],st[1],st[2],'dn%d_%d_%d'%(seed,i,j)),st,k*1.7)); k+=1
    return D
def upd_diners(D,t):
    for (H,st,ph) in D: diner(H,st,t,ph)
WLANE=2.95
def rain(n,center,size=(16,11),top=9.0,floor=.84,seed=8):
    r=random.Random(seed); m=M('#DCEBFA',.3,emit=.6,alpha=.5); S=[]
    for i in range(n): S.append((obox((0,0,0),(.008,.008,.24),m,0,None,rot=(R(4),R(-8),0)),r.uniform(-size[0]/2,size[0]/2),r.uniform(-size[1]/2,size[1]/2),r.uniform(0,1)))
    def upd(t):
        c=CAM.location
        for (o,dx,dy,ph) in S:
            q=(ph+t*1.55)%1.0; p=Vector((center[0]+dx+q*.9,center[1]+dy,top-(top-floor)*q)); o.location=p; k=0 if (p-c).length<3.2 else 1; o.scale=(k,k,k)
    return upd
def flash_light(loc,times,e=9000):
    p=point(loc,0,(1,1,1),r=1.0,shadow=False)
    def upd(t):
        v=0
        for t0 in times:
            if t0<=t<t0+.12: v=e*(1-(t-t0)/.12)
        p.data.energy=v
    return upd
# ---------------------------------------------------------------- EVERY: Waleed "and I mean EVERYONE"
def EVERY():
    faisal('khi',0.0,gantry_text='WELCOME TO KARACHI',stop_x=44)
    wa=mk(WALEED,-9.5,13.7,-90,'wa'); G=[]
    spots=[(-7.2,15.7,3),(-6.9,12.95,8),(-4.6,14.5,14),(-4.2,16.4,6),(-2.2,13.2,11),(-1.6,15.4,17),(.4,16.6,21),(.9,14.2,0),(4.3,13.0,9),(4.2,15.5,12),(6.6,14.3,15),(7.0,16.4,23)]
    for i,(x,y,c) in enumerate(spots): G.append(mk(CROWD[c],x,y,-90,'g%d'%i))
    bus=w11((-26,LANES[2],0),0,seed=4,col='#C8372D'); bus_heads(bus,random.Random(2)); T=traffic(21,-70,70,FLANES[:2]+FLANES[3:],gap=(4,10))
    sidewalk_tokens(5,14,90,40,sides=(1,)); sidewalk_tokens(6,-60,90,50,sides=(-1,)); B.done('ppl')
    def upd(t):
        run_traffic(T,t); roll(bus,-26+7.5*t,LANES[2],0,7.5*t)
        hstand(wa,t); k=tl(t,ws(10)-.14,ws(10)+.1); spread(wa,k)
        face(wa,mouth='grin' if k>.5 else 'smirk',brow=.05*k); look_at(wa,CAM.location,.8,maxpitch=20)
        for i,H in enumerate(G):
            hstand(H,t); look_at(H,CAM.location,.6); wave_hi(H,t,ws(10)-.05+i*.03,1 if i%2 else -1,dur=3.0); face(H,mouth='grin' if t>ws(10) else 'smile')
        q=ease(t/DUR); camset(LV((-13.9,13.0,2.95),(-13.3,13.2,2.9),q),(-9.5,13.75,1.8),L(27,31,tl(t,ws(10)-.12,ws(10)+.12)),4.5)
    return dict(upd=upd)
SHOTS['EVERY']=EVERY
# ---------------------------------------------------------------- PM
def PMS():
    pm_stage(); pm=mk(PM,0,1.2,0,'pm'); cup=chai(pm,-1); FILLE[0]=20
    e=empty((.55,.02,1.39)); ocyl((0,0,0),.26,.03,M('#F6F4EE',.4),e,rot=(0,0,0),seg=18); oico((0,0,.05),.2,M('#E8B23A',.7),e,sc=(1,1,.45),sub=2)
    for k in range(5): oico((.1*math.cos(k*1.3),.1*math.sin(k*1.3),.12),.05,M(['#8A4A1E','#C8372D','#3F8A3A'][k%3],.6),e,sub=1)
    e.rotation_euler=(R(-8),0,0); fl=flash_light((2.5,-6,3.2),(.25,.95,1.5))
    def upd(t):
        hstand(pm,t); talk(pm,t,*wt(11,16)); k=tl(t,ws(14)-.1,ws(14)+.25)
        hold_chai(pm,cup,-1,a=L(-70,-100,k)); pm['arm'][1].rotation_euler=(R(-66-6*math.sin(t*8)),R(-16),0)
        face(pm,brow=.04); look_at(pm,CAM.location,.5,maxpitch=12); fl(t)
        q=ease(t/DUR); camset(LV((.75,-3.9,2.45),(.55,-3.5,2.42),q),(0,1.2,2.2),36,5.6)
    return dict(upd=upd)
SHOTS['PM']=PMS
# ---------------------------------------------------------------- ASTRO
def ASTROS():
    moon(); a=mk(ASTRO,0,0,0,'astro'); cup=chai(a,1); flag_pk(-2.6,1.2,4.6); FILLE[0]=25
    rk=krick((2.5,6.6,0),-118,'#2E8A3A',seed=5,slogan='KARACHI TO MOON'); rick_people(rk,random.Random(4),False)
    B.box((-1.9,-.6,.3),(.5,.45,.3),M('#77777C',.95),.12); B.done('rock')
    kt=empty((-1.9,-.6,.62)); ocyl((0,0,.14),.2,.26,M('#C9CED8',.3,metal=.85),kt,rot=(0,0,0),seg=16,r2=.15); ocyl((0,0,.3),.1,.06,M('#2A2C34',.4),kt,rot=(0,0,0),seg=10); obox((.24,0,.2),(.1,.03,.03),M('#C9CED8',.3,metal=.85),.01,kt,rot=(0,R(-35),0))
    steam((-1.9,-.6,1.0),0,9,n=8,seed=3,size=.07)
    def upd(t):
        hstand(a,t); hop=.42*abs(math.sin(t*1.9+.3)); a['root'].location[2]=a['z0']+.008+hop
        for s in (1,-1): a['leg'][s].rotation_euler[0]=R(-s*10*hop/.42)
        k=tl(t,ws(19),ws(19)+.3); hold_chai(a,cup,1,a=L(-60,-112,k)); a['arm'][-1].rotation_euler=(R(-20-150*k),0,R(-18*k)); face(a,mouth='grin' if k>.5 else 'smile',brow=.04); look_at(a,CAM.location,.6)
        q=ease(t/DUR); camset(LV((1.25,-5.9,1.45),(1.05,-5.3,1.55),q),(.1,0,1.85),25,8)
    return dict(upd=upd)
SHOTS['ASTRO']=ASTROS
# ---------------------------------------------------------------- zombie horde helpers
def horde(seed,x0,nx,y0,ny,rz=90,groups=3,dx=1.7,dy=2.05,skip=None):
    """zombie tokens on a jittered grid, split into batch groups that can be moved (shamble)"""
    r=random.Random(seed); G=[]
    for g in range(groups):
        for ix in range(nx):
            for iy in range(ny):
                if (ix+iy)%groups!=g: continue
                x=x0-ix*dx+r.uniform(-.22,.22); y=y0+iy*dy+r.uniform(-.14,.14)
                if skip and skip(x,y): continue
                tok_z(r,x,y,rz)
        G.append(B.done('zg%d'%g))
    return G
def upd_horde(G,t,v=.85,d=(1,0)):
    for g,objs in enumerate(G):
        b=.07*abs(math.sin(t*3.0+g*2.1)); s=v*t
        for o in objs: o.location=(d[0]*s,d[1]*s,b)
def night_lights(xs,y=0,e=1500,z=8.5,col=(1,.85,.62)):
    return [point((x,y,z),e,col,r=1.2,shadow=False) for x in xs]
# ---------------------------------------------------------------- ZOMB: the horde / ZCHAI: ...with chai
ZFRONT=[(0,ZED,0,6.9),(1,ZVAR[1],-2.4,4.6),(2,ZVAR[3],-2.2,9.2),(3,ZVAR[8],-4.6,6.8),(4,ZVAR[2],-4.9,2.6),(5,ZVAR[7],-4.8,11.0),(6,ZVAR[0],-7.2,4.7),(7,ZVAR[4],-7.3,9.0)]
def zomb_set(cups=False):
    faisal('khi_night',1.0,stop_x=60); FILLE[0]=160
    Z=[]
    for (i,C,x,y) in ZFRONT: Z.append(mk(C,x,y,90,'z%d'%i))
    G=horde(4,-10.0,16,2.5,5,groups=3,dy=2.1)
    night_lights((-30,-10,10,30),y=6,e=2600); point((-6,6.5,5),900,(.5,1,.6),r=2,shadow=False)
    return Z,G
def ZOMB():
    Z,G=zomb_set()
    def upd(t):
        s=.85*t
        for i,H in enumerate(Z):
            x0=ZFRONT[i][2]; y0=ZFRONT[i][3]; H['root'].location[0]=x0+s; H['root'].location[1]=y0; H['root'].rotation_euler[2]=R(90)
            walk(H,s+i*.3,step=.36,arm=0); zpose(H,t); H['root'].rotation_euler[1]+=R(3.5)*math.sin(t*3.1+H['seed']); blink(H,t); face(H,mouth='O' if (i+int(t*2))%3==0 else 'flat',brow=-.03,brow_r=-10)
        upd_horde(G,t)
        q=t/DUR; camset((4.3+s*.85,6.3-.5*q,.8+.15*q),(0+s,6.9,1.72),L(26,29,q),5.6)
    return dict(upd=upd)
SHOTS['ZOMB']=ZOMB
def ZCHAI_S():
    Z,G=zomb_set(); cups=[chai(Z[i],1) for i in range(3)]; s0=.85*2.23
    def upd(t):
        for i,H in enumerate(Z):
            x0=ZFRONT[i][2]; y0=ZFRONT[i][3]; H['root'].location[0]=x0+s0; H['root'].location[1]=y0; H['root'].rotation_euler[2]=R(90); zstand(H,t,1.0 if i>2 else 0); blink(H,t)
            if i<3:
                k=tl(t,.12+i*.12,.4+i*.12); sp=.5+.5*math.sin(t*5+i*2.1) if i==0 else 0
                hold_chai(H,cups[i],1,a=L(-84,-100,k),sip=sp*k*(1 if i==0 else 0)); H['arm'][-1].rotation_euler=(R(-10),0,0); H['head'].rotation_euler[1]=0
                face(H,mouth='grin',brow=.05); look_at(H,CAM.location,.5)
            else: face(H,mouth='flat')
        for g,objs in enumerate(G):
            for o in objs: o.location=(s0,0,0)
        q=ease(t/DUR); camset(LV((s0+5.2,5.2,1.75),(s0+4.6,5.5,1.8),q),(s0-.6,6.9,1.95),38,4.0)
    return dict(upd=upd)
SHOTS['ZCHAI']=ZCHAI_S
# ---------------------------------------------------------------- RUMOUR: the loneliest shop in town
def RUMOUR():
    S=burns('night',clock=(2,55),nost=((1,-22),(1,-15)))
    bed_shop(-18.6,BW-1.5); stool(-16.0,BW-1.6,'#2B58C9'); TB=street_tables(8,skip=(2,5)); B.done('bed')
    bm=mk(BEDMAN,-16.0,BW-1.6,-28,'bedman'); D=diners(3,TB,skip=(0,3,4,7)); Wk=kwalkers(4,((-WLANE,-1),),3,-34,-18)
    fly=oico((0,0,0),.035,M('#16171C',.5),sub=1)
    def upd(t):
        seat(bm,t,.6); bm['root'].location[0]=-16.0; bm['root'].location[1]=BW-1.6; bm['root'].rotation_euler[2]=R(-28)
        headtouch(bm,1,1,dx=.45,dy=-.62,dz=.2); bm['arm'][-1].rotation_euler=(R(-28),0,0); bm['head'].rotation_euler=(R(10),R(-9),R(-6)); face(bm,mouth='frown',brow=-.02,brow_r=-8)
        h=Vector(hp(bm)); fly.location=(h.x+.55*math.cos(t*7),h.y+.45*math.sin(t*9),h.z+.5+.15*math.sin(t*13))
        upd_diners(D,t); upd_kwalkers(Wk,t)
        q=ease(t/DUR); camset(LV((-15.6,-1.6,2.1),(-16.2,-.6,2.0),q),LV((-17.9,BW-1.3,1.9),(-17.7,BW-1.3,1.85),q),L(22,25,q),5.6)
    return dict(upd=upd)
SHOTS['RUMOUR']=RUMOUR
# ---------------------------------------------------------------- THREEAM: the whole planet is awake
def cook_anim(H,t,ph=0.0):
    hstand(H,t); c=math.sin(t*6+ph); H['arm'][1].rotation_euler=(R(-62-14*c),0,R(6)); H['arm'][-1].rotation_euler=(R(-58+12*c),0,R(-6)); H['head'].rotation_euler[0]=R(12)
def THREEAM():
    S=burns('night',clock=(3,0)); TB=street_tables(8); B.done('x')
    D=diners(1,TB); Wk=kwalkers(2,((WLANE,1),(-WLANE,-1)),5,-34,30); ck=mk(COOK,-4.6,BW+2.0,0,'cook')
    def upd(t):
        upd_diners(D,t); upd_kwalkers(Wk,t); cook_anim(ck,t); spin_fans(t)
        q=ease(t/DUR); camset(LV((-30,-1.6,13.5),(-19,-.6,5.2),q),LV((30,.2,15.5),(40,.2,13.5),q),L(40,46,q),8)
    return dict(upd=upd)
SHOTS['THREEAM']=THREEAM
# ---------------------------------------------------------------- CHAIAUR
def CHAIAUR():
    S=burns('night',clock=(3,1),nost=((1,13),)); TB=street_tables(8); kchair(9.0,-.72,180,'#F2C14E'); B.done('x')
    F=[mk(FRIENDS[0],0,0,0,'f0'),mk(FRIENDS[2],0,0,0,'f2'),mk(FRIENDS[1],0,0,0,'f1'),mk(FRIENDS[3],11.1,-1.9,180,'f3')]; hs=(1,-1,1,1); cups=[chai(H,hs[i]) for i,H in enumerate(F)]
    D=diners(5,TB,skip=(0,3)); st=TB[0][1]; seats=(st[0],st[1],(9.0,-.72,180))
    kt=empty((0,0,0)); ocyl((0,0,.0),.2,.3,M('#C9CED8',.25,metal=.9),kt,rot=(0,0,0),seg=18,r2=.14); ocyl((0,0,.17),.09,.05,M('#2A2C34',.4),kt,rot=(0,0,0),seg=10); obox((0,-.26,.04),(.03,.12,.03),M('#C9CED8',.25,metal=.9),.01,kt,rot=(R(-30),0,0))
    obox((0,.22,.05),(.02,.03,.12),M('#2A2C34',.4),.01,kt); hand=obox((0,.3,.0),(.11,.1,.13),M(CHAIWALA['skin'],.55),.03,kt)
    def upd(t):
        k=tl(t,ws(52)-.05,ws(52)+.2); cam=Vector((9.0,5.2,2.9))
        for i,H in enumerate(F):
            if i<3: sitat(H,seats[i],t)
            else: hstand(H,t); H['root'].rotation_euler[2]=R(180)
            b=math.sin(t*11+i*1.7)*k; hold_chai(H,cups[i],hs[i],a=L(-70,-128,k)-6*b); H['arm'][-hs[i]].rotation_euler=(R(-46),0,0)
            talk(H,t,*wt(52,55),rate=8.0,rest='grin'); face(H,brow=.05*k); look_at(H,cam,.9,maxyaw=85,maxpitch=30)
        upd_diners(D,t)
        kt.location=(9.62,3.9,1.95+.03*math.sin(t*9)); kt.rotation_euler=(R(18),0,R(8))
        q=ease(t/DUR); camset((9.0,5.3-.3*q,2.95),(9.0,.5,1.5),L(29,31,q),8)
    return dict(upd=upd)
SHOTS['CHAIAUR']=CHAIAUR
# ---------------------------------------------------------------- SHOCKS: a meteor lands. nobody looks
def SHOCKS():
    S=burns('night',clock=(3,2)); TB=street_tables(8); B.done('x')
    D=diners(2,TB); wa=mk(WALEED,0,-WLANE,90,'wa'); cup=chai(wa,1)
    mt=oico((0,0,-50),.9,M('#FFB23A',.3,emit=14),sub=2); tail=[oico((0,0,-50),.7-.08*k,M('#FF6A1A',.3,emit=8,alpha=.7-.08*k),sub=1) for k in range(6)]
    fl=point((-26,0,3),0,(1,.7,.4),r=2,shadow=False); TI=ws(57)+.25; IMP=Vector((-27,0,.6)); P0=Vector((-52,4,34))
    for k in range(7): puff((IMP.x+random.Random(k).uniform(-2,2),IMP.y+random.Random(k+9).uniform(-2,2),1.0),TI+.02*k,size=.9,n=5,rise=2.6,life=1.6,seed=k)
    def upd(t):
        upd_diners(D,t)
        x=1.0+1.15*t; wa['root'].location[0]=x; wa['root'].location[1]=-WLANE; wa['root'].rotation_euler[2]=R(90); walk(wa,1.15*t,step=.5); blink(wa,t)
        sp=tl(t,TI+.15,TI+.5)*(1-tl(t,TI+1.0,TI+1.3)); hold_chai(wa,cup,1,a=-66,sip=sp); face(wa,mouth='smile',brow=.02)
        q=min(1,t/TI); p=P0.lerp(IMP,q*q)
        mt.location=p if t<TI else (0,0,-50)
        for k,o in enumerate(tail):
            qq=max(0,q-.04*(k+1)); o.location=P0.lerp(IMP,qq*qq) if t<TI else (0,0,-50)
        d=t-TI; fl.data.energy=60000*math.exp(-d*5) if d>=0 else 0; SHAKE[0]=.05*math.exp(-d*4) if d>=0 else 0
        c=ease(t/DUR); camset(LV((7.8,-2.2,1.7),(8.6,-2.1,1.7),c),(x-.2,-WLANE+.4,1.85),30,4.0)
    return dict(upd=upd)
SHOTS['SHOCKS']=SHOCKS
# ---------------------------------------------------------------- the flooded street
def flood_set():
    S=burns('khi_rain',clock=(4,20),flood=True,cooks=False,far=0,canopy=True,night=.35); B.done('x')
    FP=flood_props(); ch=charpai(0,0,0); ch.location=(-4,1.4,.36)
    un=mk(UNCLE,0,0,90,'uncle'); cup=chai(un,-1)
    car_=kcar((6.8,-2.4,-.28),18,'#C9CED8',seed=3); wa=mk(WALEED,0,0,0,'wa'); wcup=chai(wa,-1)
    wd=mk(CROWD[9],0,WLANE+.1,90,'wader'); pot=empty((0,0,0)); ocyl((0,0,.24),.36,.46,M('#7A3E1A',.3,metal=.85),pot,rot=(0,0,0),seg=18,r2=.46); ocyl((0,0,.5),.4,.05,M('#8E5A2A',.4,metal=.6),pot,rot=(0,0,0),seg=18)
    rn=rain(170,(0,0),size=(22,13))
    for o_ in bpy.data.objects:
        if o_.type=='LIGHT' and o_.data.type!='SUN': o_.data.specular_factor=0
    pl_=point((0,0,7),2500,(.85,.9,1.0),r=3,shadow=False); pl_.data.specular_factor=0; S['sun'].data.specular_factor=.12
    def pose(t,ux):
        ch.location=(ux,1.4,.36+.03*math.sin(t*2.2)); ch.rotation_euler=(R(1.5*math.sin(t*1.7)),0,0)
        sit(un,1,.985+.03*math.sin(t*2.2),legs=90); un['root'].location[0]=ux-.75; un['root'].location[1]=1.4; un['root'].rotation_euler=(0,0,R(90)); blink(un,t)
        for i,e in enumerate(FP): e.location[0]+=0; e.location[2]=[.42,.42,.84,.86,.84][i]+.025*math.sin(t*2.5+i)
        sit(wa,1,1.95,legs=90); m=car_['root'].matrix_world; wa['root'].location[0]=6.8-1.3*math.cos(R(18)); wa['root'].location[1]=-2.4-1.3*math.sin(R(18)); wa['root'].rotation_euler=(0,0,R(90+18)); blink(wa,t)
        hold_chai(wa,wcup,-1,a=-64,sip=.5+.5*math.sin(t*2.4)); wa['arm'][1].rotation_euler=(R(-30),0,0); face(wa,mouth='smile')
        wx=9+.8*t; wd['root'].location[0]=wx; wd['root'].location[1]=WLANE+.1; wd['root'].rotation_euler[2]=R(90); walk(wd,.8*t,step=.4,arm=0); blink(wd,t)
        for s in (1,-1): arm_to(wd,s,root_mat(wd)@Vector((s*.42,-.05,2.72)),1)
        pot.location=(wx,WLANE+.1,2.47*wd['C']['h']+.02); rn(t)
    return dict(un=un,cup=cup,pose=pose,wa=wa,S=S)
def FLOOD():
    F=flood_set(); un=F['un']
    def upd(t):
        ux=-3.4+.9*t; F['pose'](t,ux); hold_chai(un,F['cup'],-1,a=-66); un['arm'][1].rotation_euler=(R(-38),0,0); face(un,mouth='smile'); un['head'].rotation_euler=(R(4),0,0)
        camset((-11.5,-.6,3.6),(1.5,.4,1.2),22,8)
    return dict(upd=upd)
SHOTS['FLOOD']=FLOOD
def ANSWER():
    F=flood_set(); un=F['un']
    def upd(t):
        ux=-2.4+.9*t; F['pose'](t,ux); hold_chai(un,F['cup'],-1,a=-66,sip=tl(t,.5,.9)*(1-tl(t,1.5,1.9))); un['arm'][1].rotation_euler=(R(-38),0,0); face(un,mouth='smile'); look_at(un,hp(F['wa']),.5)
        k=tl(t,1.2,1.5); F['wa']['arm'][1].rotation_euler=(R(-30-125*k),0,R(14*k+8*k*math.sin(t*10)))
        q=ease(t/DUR); camset(LV((-10.5,-.9,5.4),(-8.2,-.7,3.9),q),LV((2.5,-.2,1.2),(3.4,-.4,1.3),q),L(22,25,q),8)
    return dict(upd=upd)
SHOTS['ANSWER']=ANSWER
def HALKA1():
    F=flood_set(); un=F['un']
    def upd(t):
        ux=-1.0+.5*t; F['pose'](t,ux); k=tl(t,ws(71),ws(71)+.3)
        hold_chai(un,F['cup'],-1,a=L(-62,-76,k),out=24*k); un['arm'][1].rotation_euler=(R(-34),0,0)
        talk(un,t,*wt(69,74),rest='smile'); face(un,brow=.05); look_at(un,CAM.location,.9,maxyaw=80)
        h=hp(un); q=ease(t/DUR); camset((h[0]+3.3-.3*q,h[1]-2.5,h[2]+.15),(h[0]+.15,h[1],h[2]-.3),34,4.0)
    return dict(upd=upd)
SHOTS['HALKA1']=HALKA1
# ---------------------------------------------------------------- BLACKOUT / QUAKE
def BLACKOUT():
    S=burns('night',clock=(3,5)); TB=street_tables(8); B.done('x')
    D=diners(6,TB); PH=[]
    for i,(H,st,ph) in enumerate(D):
        e=phone_in_hand(H,-1,'#DFF0FF',em=6.0); e.scale=(0,0,0); p=point((0,0,0),0,(.85,.92,1.0),r=.3,shadow=False); PH.append((e,p,H))
    def upd(t):
        upd_diners(D,t); on=1.0 if t<.14 else 0.0; power(on)
        for p_ in S['lights']: p_.data.energy=p_['e0']*on
        FILLE[0]=35*on+4
        for i,(e,p,H) in enumerate(PH):
            k=1 if t>.3+.013*i else 0; e.scale=(k,k,k); H['arm'][-1].rotation_euler=(R(-95),0,R(-10)) if k else H['arm'][-1].rotation_euler
            h=hp(H); f=fwd(math.degrees(H['root'].rotation_euler[2])); p.location=(h[0]+f[0]*.9,h[1]+f[1]*.9,h[2]-.1); p.data.energy=260*k
        camset((-3.5,-4.2,3.4),(9.5,.6,1.3),24,8)
    return dict(upd=upd)
SHOTS['BLACKOUT']=BLACKOUT
def QUAKE():
    S=burns('night',clock=(3,6)); TB=street_tables(8); B.done('x')
    D=diners(6,TB,skip=(1,)); a=mk(CROWD[1],0,0,0,'qa'); b=mk(CROWD[6],0,0,0,'qb'); cup=chai(a,1); st=TB[1][1]
    def upd(t):
        upd_diners(D,t); SHAKE[0]=.085
        sitat(a,st[0],t); sitat(b,st[1],t); diner(b,st[1],t,1.0)
        hold_chai(a,cup,1,a=-72,sip=tl(t,.15,.5)); a['arm'][-1].rotation_euler=(R(-48),0,0); face(a,mouth='flat',brow=.0); face(b,mouth='smile')
        for i,(H,s_,ph) in enumerate(D): H['root'].location[2]+=.02*math.sin(t*40+i)
        camset((-6.4,-4.3,2.05),(-9.2,-.8,1.6),30,5.6)
    return dict(upd=upd)
SHOTS['QUAKE']=QUAKE
