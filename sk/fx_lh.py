# deterministic FX driven by time t (seconds in shot)
PUFF=M('#F2EEEA',.9,spec=.1); PUFFD=M('#BDB6B0',.95,spec=.1); FIRE1=M('#FFB23A',.4,emit=8.0); FIRE2=M('#FF6A1A',.4,emit=6.0); SPARK=M('#FFE28A',.3,emit=9.0); GOLDL=M('#FFD36A',.3,emit=5.0)
class FX:
    def __init__(s): s.items=[]
    def add(s,o,fn): s.items.append((o,fn))
    def upd(s,t):
        for o,fn in s.items: fn(o,t)
fx=FX()
def _hide(o): o.scale=(0,0,0)
def puff(loc,t0,size=.12,n=5,col=None,rise=.25,life=1.0,drift=(0,0,0),seed=1,parent=None):
    r=random.Random(seed)
    for i in range(n):
        off=Vector((r.uniform(-1,1),r.uniform(-1,1),r.uniform(-.3,1)))*size*.6; sz=size*r.uniform(.6,1.1); dl=r.uniform(0,.12); lf=life*r.uniform(.7,1.1)
        o=oico((0,0,0),1.0,col or PUFF,parent,sub=2,smooth=False); o.scale=(0,0,0)
        def fn(o,t,off=off,sz=sz,dl=dl,lf=lf,i=i):
            q=(t-t0-dl)/lf
            if q<=0 or q>=1: o.scale=(0,0,0); return
            g=sz*(min(1,q*4)**.5)*(1+.6*q)*(1-q)**1.4
            p=Vector(loc)+off*(1+q*1.6)+Vector((drift[0]*q,drift[1]*q,drift[2]*q+rise*q))
            o.location=p; o.scale=(g,g,g*.9); o.rotation_euler=(q*2+i,q*1.5,i)
        fx.add(o,fn)
def flame(loc_fn,t0,dur=.45,size=.07,seed=2,dirv=(0,-1,0),parent=None):
    r=random.Random(seed)
    for i in range(7):
        m=FIRE1 if i%2 else FIRE2; o=oico((0,0,0),1.0,m,parent,sub=1,smooth=False); o.scale=(0,0,0); dl=i*.035; jit=Vector((r.uniform(-1,1),r.uniform(-1,1),r.uniform(-1,1)))
        def fn(o,t,dl=dl,jit=jit,i=i):
            q=(t-t0-dl)/dur
            if q<=0 or q>=1: o.scale=(0,0,0); return
            base=Vector(loc_fn(t)); d=Vector(dirv).normalized()
            p=base+d*size*(1.5+q*5.0)+jit*size*.5*q+Vector((0,0,size*2*q*q))
            g=size*(1.2-q)*(.7+.3*math.sin(t*60+i)); o.location=p; o.scale=(g,g,g); o.rotation_euler=(t*9+i,t*7,i)
        fx.add(o,fn)
def sparkles(center,radius,t0,t1,n=30,size=.03,seed=3,rise=.4,mat=None):
    r=random.Random(seed)
    for i in range(n):
        p=Vector(center)+Vector((r.uniform(-1,1),r.uniform(-1,1),r.uniform(-.5,1)))*radius; ts=r.uniform(t0,t1); lf=r.uniform(.35,.8); sz=size*r.uniform(.6,1.3)
        o=oico((0,0,0),1.0,mat or SPARK,sub=1,smooth=False); o.scale=(0,0,0)
        def fn(o,t,p=p,ts=ts,lf=lf,sz=sz):
            q=(t-ts)/lf
            if q<=0 or q>=1: o.scale=(0,0,0); return
            g=sz*math.sin(pi*q); o.location=p+Vector((0,0,rise*q)); o.scale=(g,g,g); o.rotation_euler=(q*6,q*4,0)
        fx.add(o,fn)
def ballistic(objs_spec,t0,g=9.8,floor=0.0,e=.35,fric=.5):
    """objs_spec: list of (obj,p0,v0,spin) ; obj rests after bounces on plane z=floor"""
    for (o,p0,v0,spin) in objs_spec:
        def fn(o,t,p0=Vector(p0),v0=Vector(v0),spin=spin):
            tt=t-t0
            if tt<=0: o.location=p0; return
            x=p0.x+v0.x*min(tt,1.2)*fric+v0.x*min(tt,1.2)*(1-fric)*.0; y=p0.y+v0.y*min(tt,1.2)*fric
            x=p0.x+v0.x*(1-math.exp(-tt*2.2))/2.2; y=p0.y+v0.y*(1-math.exp(-tt*2.2))/2.2
            z=bounce_z(tt,p0.z,v0.z,floor,g,e)
            o.location=(x,y,z); k=math.exp(-tt*1.5); o.rotation_euler=(spin[0]*(1-k)/1.5,spin[1]*(1-k)/1.5,spin[2]*(1-k)/1.5)
        fx.add(o,fn)
def bounce_z(t,z0,vz,floor,g=9.8,e=.35):
    # projectile with bounces
    z=z0; v=vz; tt=t
    for _ in range(6):
        disc=v*v+2*g*(z-floor); tl=(v+math.sqrt(max(0,disc)))/g
        if tt<tl: return z+v*tt-.5*g*tt*tt
        tt-=tl; v=abs(v-g*tl)*e; z=floor
        if v<.15: return floor
    return floor
def falling_leaves(x0,x1,y0,y1,ztop,n,seed=5,speed=.55,period=None):
    r=random.Random(seed)
    for i in range(n):
        x=r.uniform(x0,x1); y=r.uniform(y0,y1); ph=r.uniform(0,1); sw=r.uniform(.15,.4); fr_=r.uniform(1.2,2.2); sp=speed*r.uniform(.8,1.3)
        o=obox((0,0,0),(.06,.045,.004),LEAF[r.randrange(5)],0); P=period or (ztop/sp)
        def fn(o,t,x=x,y=y,ph=ph,sw=sw,fr_=fr_,sp=sp,P=P):
            q=((t/P)+ph)%1.0; z=ztop*(1-q)
            o.location=(x+sw*math.sin(t*fr_+ph*9),y+sw*.6*math.cos(t*fr_*.8+ph*5),z); o.rotation_euler=(math.sin(t*fr_*1.3+ph)*1.0,math.cos(t*fr_+ph*3)*.8,t*.7+ph*6)
        fx.add(o,fn)
def steam(loc,t0,t1,n=10,seed=6,size=.05):
    r=random.Random(seed)
    for i in range(n):
        ts=t0+(t1-t0)*i/n+r.uniform(0,.1); lf=r.uniform(.7,1.1); off=Vector((r.uniform(-.06,.06),r.uniform(-.06,.06),0))
        o=oico((0,0,0),1.0,M('#F4F4F4',.9,alpha=.45),sub=2); o.scale=(0,0,0)
        def fn(o,t,ts=ts,lf=lf,off=off):
            q=(t-ts)/lf
            if q<=0 or q>=1: o.scale=(0,0,0); return
            g=size*(.5+q*1.5)*math.sin(pi*q)**.6; o.location=Vector(loc)+off+Vector((.04*math.sin(q*6+ts*3),0,.35*q)); o.scale=(g,g,g*1.3)
        fx.add(o,fn)
def crown_ring(center_fn,t0,r=.32,n=12):
    out=[]
    for i in range(n):
        a=i/n*2*pi; spike=(i%2==0)
        o=oico((0,0,0),1.0,GOLDL,sub=1,smooth=False); o.scale=(0,0,0)
        def fn(o,t,a=a,spike=spike,i=i):
            k=ease((t-t0-i*.025)/.5)
            if k<=0: o.scale=(0,0,0); return
            c=Vector(center_fn(t)); aa=a+t*.6
            o.location=c+Vector((r*math.cos(aa),r*math.sin(aa),(.1 if spike else 0)*k+.015*math.sin(t*5+i)))
            g=(.07 if spike else .045)*k; o.scale=(g,g,g*(2.0 if spike else 1)); o.rotation_euler=(0,0,aa)
        fx.add(o,fn)
