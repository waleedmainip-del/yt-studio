# kit for "Karachi vs Lahore": generic helpers lifted from the kz shot files
FILLE=[35.0]; _FL=[]
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
def cook_anim(H,t,ph=0.0):
    hstand(H,t); c=math.sin(t*6+ph); H['arm'][1].rotation_euler=(R(-62-14*c),0,R(6)); H['arm'][-1].rotation_euler=(R(-58+12*c),0,R(-6)); H['head'].rotation_euler[0]=R(12)
def ots2(sp,ls,back=1.5,side=.8,dz=.2,tz=-.25,lens=38):
    a=Vector(hp(sp)); b=Vector(hp(ls)); d=(a-b); d.z=0; d.normalize(); pr=Vector((-d.y,d.x,0))
    c=b-d*back+pr*side+Vector((0,0,dz)); return (c.x,c.y,c.z),(a.x,a.y,a.z+tz),lens
def staff(H,s=1,h=3.5):
    u=H['u']; e=empty((s*1.52*u,-1.72*u,.04),H['root']); wd=M('#3A2A22',.6,kind='wood',sc=.6); gd=M('#E6B93A',.25,metal=.9)
    ocyl((0,0,h/2),.05,h,wd,e,rot=(0,0,0),seg=8); ocyl((0,0,h-.1),.12,.12,gd,e,rot=(0,0,0),seg=8); oico((0,0,h+.16),.2,M('#7CFF8A',.2,emit=6),e,sub=2)
    for k in range(3): a=k*2.1; obox((math.cos(a)*.17,math.sin(a)*.17,h+.12),(.025,.025,.16),gd,.005,e,rot=(0,0,a))
    return e
def kpose(H,s=1): H['arm'][s].rotation_euler=(R(-55),0,0)
def waiter_idle(H,t,x,y,rz):
    hstand(H,t); H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(rz)
    H['arm'][-1].rotation_euler=(R(-72),0,R(-10)); H['arm'][1].rotation_euler=(R(-18),0,0)
def waiter_write(H,t,k=1.0):
    pd=H['kz']['pad'].matrix_world.translation; arm_to(H,1,(pd.x,pd.y,pd.z+.12+.02*math.sin(t*26)),k,base=(R(-18),0,0)); H['head'].rotation_euler[0]=R(16*k)
def spoon(H,s=1):
    def b(e): obox((0,-.05,.1),(.012,.012,.14),M('#C9CED8',.25,metal=.9),.004,e); oico((0,-.05,.26),.045,M('#C9CED8',.25,metal=.9),e,sc=(1,.5,1.3),sub=1); oico((0,-.06,.27),.035,M('#B5642A',.5),e,sc=(1,.5,1.1),sub=1)
    return in_hand(H,s,b)
def staff_prop(x,y,z,lean=10,h=3.5):
    e=empty((x,y,z),rot=(R(lean),0,0)); wd=M('#3A2A22',.6,kind='wood',sc=.6); gd=M('#E6B93A',.25,metal=.9)
    ocyl((0,0,h/2),.05,h,wd,e,rot=(0,0,0),seg=8); ocyl((0,0,h-.1),.12,.12,gd,e,rot=(0,0,0),seg=8); oico((0,0,h+.16),.2,M('#7CFF8A',.2,emit=6),e,sub=2); return e
def droopy(H,k=.5):
    u=H['u']
    for o in H['lids']: o.scale=(1,1,k); o.location[2]=(.66+.16*(1-k))*u
def stream(p0,p1,o):
    d=Vector(p1)-Vector(p0); o.location=tuple((Vector(p0)+Vector(p1))/2); o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); o.scale=(1,1,d.length)
def kettle(H,s=1):
    def b(e): ocyl((0,-.1,.1),.15,.24,M('#C9CED8',.25,metal=.9),e,rot=(0,0,0),seg=16,r2=.1); ocyl((0,-.1,.24),.07,.05,M('#2A2C34',.4),e,rot=(0,0,0),seg=10); obox((0,-.3,.12),(.025,.1,.025),M('#C9CED8',.25,metal=.9),.008,e,rot=(R(-32),0,0))
    return in_hand(H,s,b)
def bat(H,s=1):
    def b(e): obox((0,-.05,-.74),(.085,.03,.42),M('#D9B982',.6,kind='wood',sc=.5),.02,e); ocyl((0,-.05,-.17),.035,.32,M('#2A2C34',.5),e,rot=(0,0,0),seg=8)
    return in_hand(H,s,b)
def stumps(x,y,rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz))); S_=[ocyl((0,(k-1)*.16,.6),.03,1.2,M('#F2E2B0',.6),e,rot=(0,0,0),seg=8) for k in range(3)]; S_+=[obox((0,dy,1.22),(.02,.075,.02),M('#F2E2B0',.6),.005,e) for dy in (-.08,.08)]; return e,S_
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
def firework2(c,t0,col,n=64,seed=1,rad=5.0,size=.15,flash=2600):
    r=random.Random(seed); m=M(col,.3,emit=18); P=[]
    for i in range(n):
        v=Vector((r.gauss(0,1),r.gauss(0,.45),r.gauss(0,1))).normalized()*r.uniform(.72,1.0)
        o=oico((0,0,-90),size,m,sub=1); o.rotation_euler=v.to_track_quat('Z','Y').to_euler(); P.append((o,v))
    rk=oico((0,0,-90),.1,M('#FFF2C0',.3,emit=14),sub=1); L_=point((c[0],c[1],c[2]),0,hexc(col)[:3],r=1.5,shadow=False)
    def upd(t):
        d=t-t0
        if -.45<=d<0: k=1+d/.45; rk.location=(c[0]+.3*(1-k),c[1],c[2]-5.5*(1-k)); rk.scale=(1,1,3)
        else: rk.location=(0,0,-90)
        L_.data.energy=flash*math.exp(-max(0,d)*4.0) if 0<=d<1.6 else 0
        for o,v in P:
            if d<0 or d>1.7: o.location=(0,0,-90); continue
            q=1-math.exp(-d*3.0); o.location=(c[0]+v.x*rad*q,c[1]+v.y*rad*q,c[2]+v.z*rad*q-1.0*d*d)
            k=max(0,1-d/1.7); st=1+3.0*math.exp(-d*3.5); o.scale=(k,k,k*st)
    return upd
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
