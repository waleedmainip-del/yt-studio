# Shots for "In This World, Everyone Is Lahori". Cuts sit on narration sentence starts (audio/words.json).
SHOTS={}
END=111.3
SEQ=[('OPEN',0.0),('EVERY',2.45),('PRES',4.15),('POLICE',5.55),('TEASE',7.0),('DAWN',10.3),('SHOUT',13.85),('LIGHT',17.4),('RICK',19.6),('JAM',23.2),
     ('ARRIVE',26.7),('RAMP',29.95),('CONQ',32.0),('SILENT',34.6),('UNCLE',38.15),('OFFER',40.65),('CONF',43.85),('ACCEPT',45.95),('DHABA',47.9),('BITE',51.95),
     ('WIDE',53.7),('POWER',55.25),('SMILE',57.2),('ARMY',60.85),('LASER',64.55),('SLIP',68.6),('HIT',70.25),('FREEZE',72.9),('LEAVE',74.8),('STOP',76.15),
     ('ASK',79.15),('PACK',81.1),('BUY',84.0),('DELIV',85.75),('MARS',88.95),('MARSK',92.65),('PRESM',94.95),('BRANCH',99.45),('MSG',101.8),('LOOP',108.6)]
SHIP_AT=(-26.0,0.0,2.45); ZPOS=(-18.6,0.15); CHPOS=(-16.75,0.2)
def hide(o): o.scale=(0,0,0)
def hideH(H): H['root'].scale=(0,0,0)
def tl(t,a,b): return ease((t-a)/max(1e-3,b-a))

# ---------------------------------------------------------------- props
WHITE=M('#F4F1EA',.35); TEA=M('#B07A4A',.4); INKM=M('#16171C',.5)
def cup(parent,loc,s=1.0):
    e=empty(loc,parent); ocyl((0,0,0),.065*s,.1*s,WHITE,e,rot=(0,0,0),seg=14); ocyl((0,0,.048*s),.055*s,.005,TEA,e,rot=(0,0,0),seg=14)
    ocyl((.075*s,0,.005*s),.025*s,.012*s,WHITE,e,rot=(R(90),0,0),seg=10); return e
def hand_loc(H,s=1): u=H['u']; return (s*.5*u,-.05*u,-2.08*u)
def in_hand(H,s,builder):
    e=empty(hand_loc(H,s),H['arm'][s]); builder(e); return e
def tray(parent,loc):
    e=empty(loc,parent); ocyl((0,0,0),.32,.025,M('#C9CED8',.25,metal=.9),e,rot=(0,0,0),seg=24); c1=cup(e,(-.1,0,.06)); c2=cup(e,(.12,.02,.06)); return e,c1,c2
def blaster(parent,loc,glowm):
    e=empty(loc,parent); obox((0,-.18,0),(.06,.26,.07),M('#2B2F3A',.3,metal=.8),.02,e); obox((0,-.05,-.08),(.04,.05,.1),M('#2B2F3A',.3,metal=.8),.01,e)
    tip=oico((0,-.45,0),.05,glowm,e,sub=1); return e,tip
def slipper_obj():
    e=empty((0,0,-50)); obox((0,0,0),(.12,.27,.022),M('#2B6FD0',.6),.015,e); obox((0,.08,.03),(.1,.02,.035),M('#F4F1EA',.5),.01,e,rot=(R(-20),0,0)); return e
def helmet(H):
    u=H['u']; return oico((0,-.05*u,1.05*u),1.32*u,M('#BFE6FF',.05,spec=1.0,alpha=.12,emit=.08),H['head'],sc=(1,1,1.12),sub=3)
def thumb(H,s=1):
    u=H['u']; return obox((s*.5*u,-.3*u,-1.75*u),(.1*u,.12*u,.25*u),H['skinm'],.05*u,H['arm'][s])
def podium(x,y,col='#5E3A22',emblem='#35975A'):
    B.box((x,y,.62),(.55,.42,.62),M(col,.6,kind='wood',sc=.6),.04); B.box((x,y,1.27),(.62,.48,.04),M(shade(col,1.2),.6),.02)
    B.box((x,y-.43,.75),(.25,.01,.25),M(emblem,.5),0); B.cyl((x,y-.25,1.45),.012,.35,INKM,seg=6,rot=(R(-20),0,0)); B.ico((x,y-.3,1.62),.04,INKM,sub=1)
def flag(x,y,h=4.0,mars=False):
    B.cyl((x,y,h/2),.04,h,M('#C9CED8',.3,metal=.8),seg=8)
    if mars: B.box((x+.8,y,h-.5),(.75,.02,.45),M('#C8372D',.6,kind='fabric'),0); B.ico((x+.8,y-.03,h-.5),.18,M('#F2C14E',.5),sc=(1,.2,1),sub=1)
    else:
        B.box((x+.35,y,h-.5),(.22,.02,.45),M('#F4F1EA',.6,kind='fabric'),0); B.box((x+1.03,y,h-.5),(.56,.02,.45),M('#11693A',.6,kind='fabric'),0)
        B.ico((x+1.02,y-.03,h-.5),.2,M('#F4F1EA',.5),sc=(1,.15,1),sub=1); B.ico((x+1.1,y-.04,h-.45),.17,M('#11693A',.5),sc=(1,.15,1),sub=1)
def bunting(x0,x1,y,z,n=14):
    for i in range(n):
        a=x0+(x1-x0)*(i+.5)/n; zz=z-.35*math.sin(pi*(i+.5)/n)
        B.box((a,y,zz),(.16,.01,.16),M(['#11693A','#F4F1EA'][i%2],.7,kind='fabric'),0,rot=(0,R(45),0))
def birds(n,seed,p0,p1,t0,dur,z0=8):
    r=random.Random(seed); out=[]
    for i in range(n):
        e=empty((0,0,-80)); bm=M('#1A1A22',.6); wl=empty((0,0,0),e); wr=empty((0,0,0),e)
        obox((-.18,0,0),(.18,.05,.012),bm,0,wl); obox((.18,0,0),(.18,.05,.012),bm,0,wr); oico((0,0,0),.06,bm,e,sc=(.7,1.6,.7),sub=1)
        off=Vector((r.uniform(-3,3),r.uniform(-2,2),r.uniform(-1.5,1.5))); ph=r.uniform(0,6); dl=r.uniform(0,.4)
        def fn(o,t,wl=wl,wr=wr,off=off,ph=ph,dl=dl):
            q=(t-t0-dl)/dur
            if q<0: o.location=Vector(p0)+off; o.scale=(1,1,1)
            else: o.location=Vector(p0).lerp(Vector(p1),min(1.5,q))+off+Vector((0,0,1.5*q)); o.scale=(1,1,1)
            d=Vector(p1)-Vector(p0); o.rotation_euler=(0,0,math.atan2(-d.x,d.y)); f=math.sin(t*22+ph)*.9
            wl.rotation_euler[1]=f; wr.rotation_euler[1]=-f
        fx.add(e,fn); out.append(e)
    return out
def kites(n,seed,cx=0,cy=20):
    r=random.Random(seed)
    for i in range(n):
        x=cx+r.uniform(-30,30); y=cy+r.uniform(-5,30); z=r.uniform(16,30); c=r.choice(['#E8554D','#F2C14E','#4D8FE8','#6FC38A','#CF3F78','#7448C2'])
        e=empty((x,y,z)); omesh([(0,0,.6),(.45,0,0),(0,0,-.75),(-.45,0,0)],[(0,1,2,3)],M(c,.6,kind='fabric'),e)
        ph=r.uniform(0,6)
        def fn(o,t,ph=ph,z=z): o.rotation_euler=(R(10)*math.sin(t*1.3+ph),R(14)*math.sin(t*.9+ph),R(8)*math.sin(t*1.1+ph)); o.location[2]=z+.4*math.sin(t*.8+ph)
        fx.add(e,fn)
def confetti(center,t0,n=60,seed=8):
    r=random.Random(seed)
    for i in range(n):
        o=obox((0,0,0),(.05,.03,.004),M(r.choice(['#E8554D','#F2C14E','#4D8FE8','#6FC38A','#CF3F78','#F4F1EA']),.5,emit=.3),0); o.scale=(0,0,0)
        v=Vector((r.uniform(-3,3),r.uniform(-2,1),r.uniform(3,7))); sp=Vector((r.uniform(-9,9),r.uniform(-9,9),r.uniform(-9,9)))
        def fn(o,t,v=v,sp=sp):
            tt=t-t0
            if tt<=0: o.scale=(0,0,0); return
            g=6.0; vz=v.z-g*tt; z=center[2]+v.z*tt-.5*g*tt*tt if vz>-1.6 else center[2]+v.z*(v.z+1.6)/g-.5*g*((v.z+1.6)/g)**2-1.6*(tt-(v.z+1.6)/g)
            o.location=(center[0]+v.x*tt*.6,center[1]+v.y*tt*.6,max(.02,z)); o.scale=(1,1,1); o.rotation_euler=tuple(s_*tt for s_ in sp)
        fx.add(o,fn)

# ---------------------------------------------------------------- crowd
SKL=['#C98F62','#B97A4E','#D9A074','#A86F47','#8A5A3C','#E0AE84','#C08A5C']; HRL=['#15120F','#1E1A18','#2A1B14','#3B2314','#2A2420']
MEN=['#F4F1EA','#E8E2D0','#BFD6E8','#9AA4B0','#2A2C34','#6B7A4A','#C9B48A','#8FB8D8','#D8C8B8','#A8C8B0','#7A6A8A']
WOM=['#E8554D','#CF3F78','#F2C14E','#35975A','#7448C2','#16909E','#F28AA0','#E6A31C','#2B58C9','#B8D86A']
def lahori_design(seed):
    r=random.Random(seed*17+3); g=r.random(); c=dict(skin=r.choice(SKL),hair=r.choice(HRL),eye='#2A1A12',kurta=True,shalwar=True,cuff=True)
    if g<.42:
        top=r.choice(WOM); c.update(top=top,trim=shade(top,.75),pants=r.choice([shade(top,.6),'#F4F1EA',r.choice(WOM)]),hairstyle=r.choice(['long','bun','long','ponytail']),
              dupatta=r.choice(WOM),dupatta_trim='#E6B53A',lashes=True,earrings=r.random()<.6,bangles=r.random()<.5,shoes=r.choice(['#C9A27A','#F4F1EA','#7A1F2E']),
              accent='#E6B53A',sole='#3A2A1E',h=r.choice([.92,.95,.97]),button='#E6B53A',tie_c=r.choice(WOM))
        if c['hairstyle']=='ponytail': c['braid']=r.random()<.5
    else:
        top=r.choice(MEN); c.update(top=top,trim=shade(top,.8),pants=r.choice([top,'#F4F1EA',top]),hairstyle=r.choice(['short','quiff','fringe','old','short']),h=r.choice([.95,.98,1.0,1.03,1.06]),button=shade(top,.7))
        if r.random()<.55: c['sandals']=r.choice(['#5E3A1E','#3E2A1A','#7A4A22'])
        else: c.update(shoes=r.choice(['#22242B','#3A2A1E','#F4F5FA']),accent='#22242B',sole='#F0F1F5')
        if r.random()<.25: c['waistcoat']=r.choice(['#2A2C34','#6B4A2E','#3A4A5A','#5A2A2A'])
        if r.random()<.15: c['topi']=r.choice(['#F4F1EA','#7A6A55'])
        if r.random()<.4: c['stache']=r.choice(HRL)
        elif r.random()<.25: c['beard']=r.choice(HRL)
        if c['hairstyle']=='old': c['hair']=r.choice(['#6B6B74','#A2A2AA','#2A2420'])
        if r.random()<.15: c.update(kurta=False,shalwar=False,top=r.choice(['#F4F1EA','#2B58C9','#D2473A','#22242B']),pants=r.choice(['#27365A','#3A3D47','#4A3D32']),short=True)
    if r.random()<.1: c['h']=r.choice([.74,.78]); c['short']=True
    return c
ALS=['#7E6F9A','#6E8A9A','#7A9A7E','#8A7AA0','#6A7A9A','#9A7A8E']
def soldier_design(seed):
    r=random.Random(seed*29+1); sk=r.choice(ALS)
    return dict(skin=sk,hair='#4A3F63',hairstyle='bald',alien=True,top='#23252E',trim='#15161C',pants='#1E2028',boots='#2B2F3A',gloves='#2B2F3A',belt='#2B2F3A',buckle='#35C8FF',
                armour=r.choice(['#2B2F3A','#3A3046','#2A3A3A']),eye='#0B0B12',brow_c=shade(sk,.6),h=r.choice([1.1,1.14,1.18]),wide=1.05,face_w=.3)
def mars_design(seed):
    r=random.Random(seed*31+7); sk=r.choice(ALS); g=r.random()<.4; top=r.choice(WOM if g else MEN)
    c=dict(skin=sk,hair='#4A3F63',hairstyle='bald',alien=True,no_armour=True,kurta=True,shalwar=True,cuff=True,top=top,trim=shade(top,.75),pants=r.choice(['#F4F1EA',shade(top,.6)]),
           sandals=r.choice(['#5E3A1E','#3E2A1A']),eye='#0B0B12',brow_c=shade(sk,.6),h=r.choice([1.02,1.06,1.1]),wide=1.0,face_w=.3,button=shade(top,.7))
    if g: c.update(dupatta=r.choice(WOM),dupatta_trim='#E6B53A',bangles=True)
    elif r.random()<.3: c['waistcoat']=r.choice(['#2A2C34','#6B4A2E'])
    return c
class Crowd:
    def __init__(s): s.p=[]
    def add(s,H,mode,**kw): d=dict(H=H,mode=mode); d.update(kw); s.p.append(d); return d
def make_crowd(n,seed,kind='lahori',zones=((-30,30,4.6,6.9),(-30,30,-6.9,-4.6)),walk_frac=.6,avoid=()):
    r=random.Random(seed); C=Crowd(); des={'lahori':lahori_design,'alien':soldier_design,'mars':mars_design}[kind]
    for i in range(n):
        for _ in range(20):
            z=r.choice(zones); x=r.uniform(z[0],z[1]); y=r.uniform(z[2],z[3])
            if not any(a[0]<x<a[1] and a[2]<y<a[3] for a in avoid): break
        D=des(seed*1000+i); w=r.random()<walk_frac
        if w:
            dr=r.choice([-1,1]); H=avatar_lh((x,y,.07 if abs(y)>4.1 else 0),90*dr,D,name='c%d_%d'%(seed,i)); C.add(H,'walk',x0=x,y=y,dir=dr,v=r.uniform(.9,1.25),xa=z[0],xb=z[1])
        else:
            rz=r.choice([0,180,90,-90,r.uniform(-180,180)]) if abs(y)>4.1 else r.uniform(-180,180)
            H=avatar_lh((x,y,.07 if abs(y)>4.1 else 0),rz,D,name='c%d_%d'%(seed,i)); C.add(H,'stand',rz=rz)
    return C
def upd_crowd(C,tg,freeze=None,look=None,react=0.0,cheer=0.0):
    for i,d in enumerate(C.p):
        H=d['H']; blink(H,tg)
        if d['mode']=='walk':
            te=tg if freeze is None else min(tg,freeze); L_=d['xb']-d['xa']; x=d['xa']+((d['x0']-d['xa'])+d['dir']*d['v']*te)%L_
            H['root'].location[0]=x; H['root'].location[1]=d['y']; H['root'].rotation_euler[2]=R(90*d['dir'])
            if freeze is None or tg<freeze: walk(H,abs(d['v']*te),step=.55)
            else: legs0(H); arms(H,0,0,0,0,0,0); H['root'].location[2]=H['z0']+.008; H['root'].rotation_euler[0]=0
        else: stand(H,tg+i)
        if look is not None and (freeze is None or tg>=freeze):
            look_at(H,look,1.0,maxyaw=80)
            if react>0:
                k=react*(.6+.4*((i*37)%10)/10); H['arm'][1].rotation_euler=(R(-25*k),0,R(10*k)); H['arm'][-1].rotation_euler=(R(-25*k),0,R(-10*k)); face(H,mouth='O',brow=.06*k,eyes=1+.25*k)
        elif d['mode']=='stand': gaze_idle(H,tg+i*1.3)
        if cheer>0:
            ph=math.sin(tg*9+i)*.5+.5; k=cheer
            H['arm'][1].rotation_euler=(R(-160*k),0,R((14+10*ph)*k)); H['arm'][-1].rotation_euler=(R(-150*k),0,R((-14-10*ph)*k)); face(H,mouth='grin'); H['root'].location[2]+=.08*k*ph

# ---------------------------------------------------------------- traffic
VCOL=['#F4F5FA','#C8372D','#2B58C9','#1A1A1E','#C9CED8','#E6A31C','#35975A','#8A8E96']
def make_traffic(n,seed,lanes=((2.0,1),(-2.0,-1)),xr=(-60,60),kinds=('car','car','rick','bike','rick')):
    r=random.Random(seed); T=[]
    for i in range(n):
        y,dr=r.choice(lanes); k=r.choice(kinds); x=r.uniform(*xr)
        if k=='car': V=car((x,y,0),0,r.choice(VCOL),seed*50+i)
        elif k=='rick': V=rickshaw((x,y,0),0,r.choice(['#2E8A3A','#E6A31C','#2E8A3A','#1F6E8A']),seed*50+i)
        else:
            V=motorbike((x,y,0),0,r.choice(['#C8372D','#1A1A1E','#2B58C9'])); D=lahori_design(seed*77+i)
            Hr=avatar_lh((0,0,0),-90,D,name='rider%d_%d'%(seed,i)); Hr['root'].parent=V['root']; Hr['root'].location=(-.15,0,.42); Hr['root'].rotation_euler=(0,0,R(-90))
            sit(Hr,1.0,.55,legs=70); Hr['z0']=0; arms(Hr,-70,0,6,-70,0,-6); V['rider']=Hr
        V['root'].scale=(1.3,1.3,1.3); V['r']*=1.3; V['x0']=x; V['y']=y; V['dir']=dr; V['v']=r.uniform(6,9) if k!='bike' else r.uniform(8,11); V['xr']=xr; V['kind']=k; T.append(V)
    return T
def upd_traffic(T,tg,speed=1.0,stopped=None):
    for V in T:
        L_=V['xr'][1]-V['xr'][0]; v=V['v']*speed
        if stopped is not None: v=V['v']*stopped(V)
        d=v*tg; x=V['xr'][0]+((V['x0']-V['xr'][0])+V['dir']*d)%L_
        drive(V,x,V['y'],0 if V['dir']>0 else 180,d)
        if 'rider' in V: blink(V['rider'],tg)

# ---------------------------------------------------------------- common street set
def street_set(mood='morning_s',crowd_n=24,traffic_n=10,seed=1,kind='lahori',theme='lahore',avoid=(),walk_frac=.6,zones=None):
    W=bazaar(theme,seed=3 if theme=='lahore' else 5); setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=55)
    C=make_crowd(crowd_n,seed,kind,zones=zones or ((-30,30,4.6,6.9),(-30,30,-6.9,-4.6)),walk_frac=walk_frac,avoid=((-4.6,-2.4,4.9,6.3),(3.4,5.6,4.9,6.3),(-9.1,-6.9,-6.3,-4.9),(12.5,21.5,3.5,7.0))+tuple(avoid))
    T=make_traffic(traffic_n,seed) if traffic_n else []
    if theme=='lahore': kites(7,seed)
    return W,C,T
def ship_landed(delivery=False):
    S=saucer(SHIP_AT,delivery); S['root'].rotation_euler=(0,0,R(90)); S['hinge'].rotation_euler[0]=R(22); return S
def zorak(loc=(ZPOS[0],ZPOS[1],0),rz=90,hel=True,C_=None):
    H=avatar_lh(loc,rz,C_ or ZORAK,name='zorak'); H['helmet']=helmet(H) if hel else None; return H
def army(n=6,seed=4,x0=-24.5,x1=-20.8):
    out=[]
    YS=[-3.0,3.0,-2.2,2.2,-1.4,1.4]
    for i in range(n):
        y=YS[i%6]; x=-19.8 if i%2 else -19.0
        H=avatar_lh((x,y,0),90,soldier_design(seed*10+i),name='sold%d'%i); bl,tip=blaster(H['arm'][1],hand_loc(H,1),M('#5AF0FF',.2,emit=0.0)); H['tip']=tip; H['tipm']=tip.data.materials[0]; out.append(H)
    return out
def ship_lights(S,t):
    for i,o in enumerate(S['lights']): k=.6+.4*math.sin(t*6+i*.8); o.scale=(k,k,k)
def talk(H,t,t0,t1): mouth_talk(H,t,t0,t1)

# ================================================================== SHOTS
def OPEN_(loop=False):
    W,C,T=street_set(crowd_n=34,traffic_n=24,seed=1); BI=birds(7,2,(-30,-8,14),(30,25,20),99.0 if loop else 0.0,5.0)
    P0=((-52,-1.5,24),(-8,1.5,1.5),24); P1=((-25,-1.2,6.2),(-2,1.2,2.4),24)
    def upd(t):
        if loop: tg=t-DUR; q=ease(t/DUR); camp=LV((-120,-3,70),P0[0],q); tgt=LV((-20,1,8),P0[1],q); lens=P0[2]
        else: tg=t; q=ease(t/2.45); camp=LV(P0[0],P1[0],q); tgt=LV(P0[1],P1[1],q); lens=P0[2]
        upd_crowd(C,tg); upd_traffic(T,tg); camset(camp,tgt,lens,16)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_; SHOTS['LOOP']=lambda: OPEN_(True)

def EVERY_():
    W,C,T=street_set(crowd_n=22,traffic_n=10,seed=2,avoid=((-2,9,-6.2,-4.0),)); Hm=avatar_lh((3.8,-4.95,.07),-90,HAMZA,name='hamza'); c=in_hand(Hm,1,lambda e: cup(e,(0,-.06,.02)))
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); upd_traffic(T,tg); blink(Hm,tg)
        d=1.15*t; Hm['root'].location[0]=3.8-d; walk(Hm,d,step=.55); Hm['arm'][1].rotation_euler=(R(-62),0,R(8)); face(Hm,mouth='smirk' if t>.7 else 'smile',brow=.02 if t>.7 else 0)
        if t>.75: look_at(Hm,(Hm['root'].location[0]-3.2,-2.6,2.0),ease((t-.75)/.3)*.8)
        x=Hm['root'].location[0]; camset((x-4.1,-3.25,2.0),(x,-4.95,1.95),32,4.0)
    return dict(upd=upd)
SHOTS['EVERY']=EVERY_

def PRES_():
    W,C,T=street_set(crowd_n=10,traffic_n=0,seed=3,avoid=((-6,6,-6.9,3),))
    B.box((0,1.8,.25),(4.2,2.4,.25),M('#7A1F2E',.8,kind='fabric'),.05); podium(0,.6); flag(-3.2,2.6,4.4); flag(2.2,2.6,4.4); bunting(-4,4,3.9,4.2); B.done('stage')
    P=avatar_lh((0,1.15,.5),0,dict(skin='#C08A5C',hair='#2A2420',hairstyle='short',top='#16171C',trim='#0E0F12',pants='#F4F1EA',kurta=True,shalwar=True,cuff=True,shoes='#16171C',accent='#16171C',
                 sole='#16171C',topi='#3A3A40',stache='#2A2420',stache_style='strong',button='#C9A24A',h=1.02,wide=1.08,face_w=.6),name='pres')
    cp=in_hand(P,-1,lambda e: cup(e,(0,-.06,.02))); au=[avatar_lh((x,y,0),180,lahori_design(900+i),name='aud%d'%i) for i,(x,y) in enumerate(((-1.6,-2.3),(1.4,-2.6),(-.2,-3.1),(2.6,-2.0)))]
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); stand(P,tg); blink(P,tg)
        for i,A in enumerate(au): stand(A,tg+i); blink(A,tg+i); look_at(A,(0,1.15,2.8),.7)
        s=tl(t,.45,.8)*(1-tl(t,1.15,1.4)); arm_to(P,-1,(0,.4,2.65+.05),s,base=(R(-35),0,0)) if s>0 else arms(P,-35,0,4,-35,0,-4)
        face(P,mouth='smile' if s<.5 else 'flat',brow=.02,eyes=.75 if s>.5 else 1); P['head'].rotation_euler[0]=R(-12*s)
        camset((.3,-3.4,2.3),(0,1.0,2.4),36,4.0)
    return dict(upd=upd)
SHOTS['PRES']=PRES_

def POLICE_():
    W,C,T=street_set(crowd_n=14,traffic_n=12,seed=4); B.cyl((6,0,.12),1.1,.24,M('#F2C14E',.6),seg=24); B.cyl((6,0,.26),.9,.06,M('#F4F1EA',.6),seg=24); B.done('island')
    Pc=avatar_lh((6,0,.29),0,dict(skin='#B97A4E',hair='#15120F',hairstyle='cap',cap='#1A2A3A',top='#2E3A4A',trim='#1E2A3A',pants='#2E3A4A',shoes='#16171C',accent='#16171C',sole='#16171C',
                  stache='#15120F',belt='#3A2A1E',h=1.0,emblem='#C9A24A',medals=['#C9A24A','#C8372D']),name='cop')
    cp=in_hand(Pc,-1,lambda e: cup(e,(0,-.06,.02))); ws=obox((0,-.66*Pc['u'],.42*Pc['u']),(.05,.05,.03),M('#C9CED8',.3,metal=.9),.01,Pc['head'])
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); upd_traffic(T,tg); stand(Pc,tg); blink(Pc,tg)
        w=math.sin(t*7); Pc['arm'][1].rotation_euler=(R(-15),0,R(95+25*w)); Pc['arm'][-1].rotation_euler=(R(-60),0,R(-6))
        Pc['head'].rotation_euler=(0,0,R(28*math.sin(t*2.3))); face(Pc,mouth='o',brow=.04)
        camset((3.6,-3.4,1.35),(6,0,2.05),32,5.6)
    return dict(upd=upd)
SHOTS['POLICE']=POLICE_

def TEASE_():
    W,C,T=street_set(crowd_n=16,traffic_n=0,seed=5,avoid=((2.6,6.4,3.8,6.9),)); T=make_traffic(8,5,lanes=((-2.0,-1),)); A=avatar_lh((4.4,4.55,.07),0,mars_design(5),name='tease')
    jl=in_hand(A,-1,lambda e: oico((0,-.1,.04),.09,M('#F2A11A',.35,emit=.3),e,sc=(1,1,.45),sub=1)); th=thumb(A,1); th.scale=(0,0,0)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); upd_traffic(T,tg); stand(A,tg); blink(A,tg); ta=9.41-T0
        e=tl(t,.3,.7)*(1-tl(t,1.3,1.6)) + tl(t,1.9,2.2)*(1-tl(t,2.5,2.8))
        arm_to(A,-1,(4.4,4.0,2.55),e,base=(R(-40),0,0)) if e>0 else arms(A,-12,0,0,-40,0,-6)
        face(A,mouth='o' if e>.5 else ('grin' if t>ta else 'smile'),brow=.03,eyes=.8 if e>.5 else 1)
        k=tl(t,ta-.15,ta+.15);
        if k>0: A['arm'][1].rotation_euler=(R(-75*k),0,R(18*k)); th.scale=(k,k,k); A['head'].rotation_euler=(R(-6*k),R(8*k),0)
        else: th.scale=(0,0,0)
        camset((4.05,1.0,2.1),(4.4,4.55,2.0),32,4.0)
    return dict(upd=upd)
SHOTS['TEASE']=TEASE_

def DAWN_():
    W,C,T=street_set('golden',crowd_n=6,traffic_n=2,seed=6); BI=birds(9,3,(-40,10,9),(30,-10,16),0.4,3.2)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); upd_traffic(T,tg); q=ease(t/DUR); camset(LV((-34,-1.5,12),(-24,-.5,9),q),(20,6,9),24,16)
    return dict(upd=upd)
SHOTS['DAWN']=DAWN_

def SHOUT_():
    W,C,T=street_set('morning',crowd_n=8,traffic_n=0,seed=7,avoid=((-16,-10,4.0,7.0),)); T=make_traffic(4,7,lanes=((-2.0,-1),))
    B.box((-13,6.35,4.1),(1.3,.7,.07),M('#F4EBDA',.7),.02)
    for j in range(12): B.box((-14.2+j*.22,5.68,4.46),(.02,.02,.3),M('#2A2C34',.4,metal=.6),0)
    B.box((-13,5.68,4.77),(1.3,.025,.025),M('#2A2C34',.4,metal=.6),0)
    for bx in (-17.5,-8.5):
        B.box((bx,6.45,7.1),(1.0,.6,.07),M('#F4EBDA',.7),.02); B.box((bx,5.86,7.46),(1.0,.02,.32),M('#2A2C34',.4,metal=.6),.0)
    B.done('balc')
    Hc=avatar_lh((-13,6.4,4.17),0,CHACHA,name='chacha'); N1=avatar_lh((-17.5,6.6,7.17),20,lahori_design(301),name='n1'); N2=avatar_lh((-8.5,6.6,7.17),-20,lahori_design(302),name='n2')
    BI=birds(10,4,(-13,9,11),(-33,-6,18),.4,2.4)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); upd_traffic(T,tg); stand(Hc,tg); blink(Hc,tg); s0,s1=14.0-T0,16.61-T0
        k=tl(t,s0-.25,s0)*(1-tl(t,s1,s1+.4)); mp=root_mat(Hc)@Vector((0,-.9*Hc['u'],4.6*Hc['u']))
        for s in (1,-1): arm_to(Hc,s,(mp.x+s*.12,mp.y,mp.z),k,base=(0,0,0))
        Hc['head'].rotation_euler[0]=R(-14*k); Hc['root'].rotation_euler[0]=R(-6*k)
        face(Hc,mouth='shout' if s0<t<s1 else 'flat',brow=.05*k,eyes=1+.2*k)
        for N,ts in ((N1,1.5),(N2,2.0)):
            p=tl(t,ts,ts+.35); N['root'].location[2]=N['z0']-1.8*(1-p)+.008; stand(N,tg); N['root'].location[2]=N['z0']-1.8*(1-p)+.008; face(N,mouth='frown',brow=-.02,brow_r=-18); look_at(N,(-13,6.4,6.5),.9); blink(N,tg)
        camset((-13.4,2.2,5.0),(-13,6.3,5.6),30,16)
    return dict(upd=upd)
SHOTS['SHOUT']=SHOUT_

def LIGHT_():
    W,C,T=street_set(crowd_n=10,traffic_n=0,seed=8); TL=traffic_light(-12,4.45)
    T2=make_traffic(16,8,lanes=((2.0,1),),xr=(-60,40));
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); tl_set(TL,1 if t<.35 else 0); upd_traffic(T2,tg,1.15)
        camset((-11.3,-.6,2.6),(-12,4.45,4.55),34,4.0,focus=(-12,4.3,4.7))
    return dict(upd=upd)
SHOTS['LIGHT']=LIGHT_

def RICK_():
    W,C,T=street_set(crowd_n=12,traffic_n=0,seed=9); TL=traffic_light(1.5,-4.45,180)
    Rk=rickshaw((-2,-2.0,0),180,'#2E8A3A'); Rk['root'].scale=(1.3,1.3,1.3); Rk['r']*=1.3
    Dv=avatar_lh((0,0,0),90,dict(skin='#A86F47',hair='#15120F',hairstyle='short',top='#9AA4B0',trim='#7A8490',pants='#9AA4B0',kurta=True,shalwar=True,sandals='#3E2A1A',stache='#15120F',topi='#F4F1EA',h=1.0),name='driver')
    Dv['root'].parent=Rk['root']; Dv['root'].location=(.15,0,.42); Dv['root'].rotation_euler=(0,0,R(90)); sit(Dv,1,.5,legs=80); Dv['z0']=0
    Cr=car((-8.2,-2.0,0),180,'#C9CED8',3); Cr['root'].scale=(1.3,1.3,1.3)
    Bk=motorbike((-7.6,-3.05,0),180,'#1A1A1E'); Bk['root'].scale=(1.3,1.3,1.3)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); tl_set(TL,0); blink(Dv,tg); s0,s1=21.6-T0,22.81-T0
        k=tl(t,s0-.35,s0)
        Dv['root'].location[1]=.28*k; Dv['root'].rotation_euler[0]=R(-10*k); Dv['head'].rotation_euler=(R(-6*k),0,R(50*k))
        Dv['arm'][-1].rotation_euler=(R(-70-40*k*abs(math.sin(t*9))),0,R(-30*k)); Dv['arm'][1].rotation_euler=(R(-75),0,R(6))
        face(Dv,mouth='shout' if s0<t<s1 else ('frown' if t>.6 else 'flat'),brow=.04*k,brow_r=-14)
        Rk['root'].location[2]=.01*math.sin(t*30)
        camset((2.2,-6.6,1.75),(-2.6,-2.0,1.75),30,5.6,focus=(-2,-2,2))
    return dict(upd=upd)
SHOTS['RICK']=RICK_

def JAM_():
    W,C,T=street_set(crowd_n=26,traffic_n=0,seed=10); r=random.Random(10); V=[]
    for lane in (-3.1,-1.1,1.1,3.1):
        x=-30
        while x<30:
            k=r.random(); v=(car((x,lane,0),0 if lane>0 else 180,r.choice(VCOL),int(x*7)) if k<.45 else rickshaw((x,lane,0),0 if lane>0 else 180,r.choice(['#2E8A3A','#E6A31C']),int(x)) if k<.8 else motorbike((x,lane,0),0 if lane>0 else 180,r.choice(['#C8372D','#1A1A1E'])))
            v['root'].scale=(1.3,1.3,1.3); v['r']*=1.3; v['x0']=x; v['y']=lane; v['dir']=1 if lane>0 else -1; v['jit']=r.uniform(-.2,.2); V.append(v); x+=r.uniform(5.2,7.0) if k<.8 else 3.4
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); go=24.47-T0
        for v in V:
            d=max(0,t-go-abs(v['jit'])*.2); d=8.0*(d-.25*(1-math.exp(-d/.25))) if d>0 else 0
            x=v['x0']+v['dir']*d; y=v['y']+v['jit']*math.sin(d*.3); drive(v,x,y,(0 if v['dir']>0 else 180)+R(0)*v['jit'],d)
        q=ease(t/DUR); camset((0+2*q,-.01,30-2*q),(0+2*q,0,0),30,16)
    return dict(upd=upd)
SHOTS['JAM']=JAM_

def ARRIVE_():
    W,C,T=street_set('morning_s',crowd_n=22,traffic_n=6,seed=11,avoid=((-9,-4,-7,-2.5),)); S=saucer((SHIP_AT[0],SHIP_AT[1],60)); S['root'].rotation_euler=(0,0,R(90)); S['hinge'].rotation_euler[0]=R(-85)
    sun=[o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN'][0]; e0=sun.data.energy
    Bm=avatar_lh((-10.4,-3.75,0),-110,BILAL,name='bilal'); cu=in_hand(Bm,1,lambda e: cup(e,(0,-.06,.02)))
    def upd(t):
        tg=T0+t; land=29.9-T0; q=ease_out(min(1,t/land)); z=L(60,SHIP_AT[2],q); S['root'].location=(SHIP_AT[0],SHIP_AT[1],z); S['root'].rotation_euler[2]=R(90+40*(1-q)); ship_lights(S,t)
        S['beam'].scale=(1,1,1) if t<land-.2 else (0,0,0)
        sun.data.energy=L(e0,e0*.55,tl(t,0,1.5)); upd_traffic(T,tg,1-tl(t,.5,1.5))
        upd_crowd(C,tg,freeze=T0+.6,look=(SHIP_AT[0],0,z),react=tl(t,.8,1.6))
        stand(Bm,tg); blink(Bm,tg); look_at(Bm,(SHIP_AT[0],0,z),tl(t,.4,.9)); face(Bm,mouth='O' if t>.9 else 'smile',eyes=1+.25*tl(t,.9,1.2),brow=.05)
        dr=tl(t,1.4,1.5);
        if t<1.45: Bm['arm'][1].rotation_euler=(R(-60),0,R(8)); cu.parent=Bm['arm'][1]; cu.location=hand_loc(Bm,1)
        else:
            tt=t-1.45; cu.parent=None; p0=Vector((-10.4+.1,-3.75-.55,1.0)); cu.location=(p0.x,p0.y-.4*tt,max(.06,p0.z-.5*9.8*tt*tt)); cu.rotation_euler=(min(1.6,tt*8),0,0); Bm['arm'][1].rotation_euler=(R(-20),0,R(8))
        camset((-6.0,-3.75,1.1),(-20,-.5,max(3.4,z*.55)),24,16)
    return dict(upd=upd)
SHOTS['ARRIVE']=ARRIVE_

def RAMP_():
    W,C,T=street_set('invade',crowd_n=16,traffic_n=0,seed=12,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak((-23.6,0,1.15),90)
    pf=puff((-20.8,0,.1),.0,.6,8,PUFFD,.4,1.6,(1.5,0,0),seed=5)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg,freeze=T0-5,look=(-21,0,2),react=.5); ship_lights(S,t); blink(Z,tg)
        o=tl(t,0,.9); S['hinge'].rotation_euler[0]=R(L(-85,22,o)); S['beam'].scale=(0,0,0)
        if t<1.0: Z['root'].scale=(0,0,0)
        else:
            Z['root'].scale=(Z['C'].get('wide',1),1+(Z['C'].get('wide',1)-1)*.45,1); f=walk_path(Z,[(-23.6,0),(-20.7,0),(-18.6,.15)],t,1.0,DUR+.2,step=.62,arm=18)
            x=Z['root'].location[0]; Z['z0']=max(0,L(1.18,0,(x+23.6)/2.9)) if x<-20.7 else 0
        face(Z,mouth='flat',brow=-.04,brow_r=-24,eyes=.85)
        camset((-15.4,-2.4,.7),(-20.6,0,2.3),26,16)
    return dict(upd=upd)
SHOTS['RAMP']=RAMP_

def CONQ_():
    W,C,T=street_set('invade',crowd_n=6,traffic_n=0,seed=13,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak()
    def upd(t):
        tg=T0+t; upd_crowd(C,tg,freeze=T0-5,look=(-18,0,2.5),react=.5); ship_lights(S,t); stand(Z,tg); blink(Z,tg)
        talk(Z,t,32.13-T0,34.03-T0); face(Z,brow=-.04,brow_r=-24,eyes=.85)
        k=tl(t,.6,1.0); Z['arm'][1].rotation_euler=(R(-80*k),0,R(10*k)); Z['arm'][-1].rotation_euler=(R(-10),0,R(-6)); Z['head'].rotation_euler=(R(4),0,0)
        if t>2.3: face(Z,mouth='flat')
        q=ease(t/DUR); camset((-16.2+.3*q,-1.3,1.75),(-18.6,.15,2.55),32,4.0,focus=(-18.6,.15,2.55))
    return dict(upd=upd)
SHOTS['CONQ']=CONQ_

def crowd_line(seed=14,n=12):
    out=[]; r=random.Random(seed)
    for i in range(n):
        x=-14.6+(i%4)*1.2+r.uniform(-.25,.25); y=1.4+(i//4)*1.1+r.uniform(-.2,.2)
        out.append(avatar_lh((x,y,0),-90+r.uniform(-15,15),lahori_design(seed*100+i),name='cl%d'%i))
    return out
def SILENT_():
    W,C,T=street_set('invade',crowd_n=8,traffic_n=0,seed=14,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak()
    CL=crowd_line(); Bm=avatar_lh((-13.4,.3,0),-80,BILAL,name='bilal'); sm=in_hand(Bm,1,lambda e: oico((0,-.12,.02),.1,M('#E0A040',.5),e,sc=(1,.8,.6),sub=1))
    def upd(t):
        tg=T0+t; upd_crowd(C,tg,freeze=T0-6,look=(-18,0,2.5)); ship_lights(S,t); stand(Z,T0); blink(Z,tg)
        for i,A in enumerate(CL): stand(A,T0); A['root'].location[2]=A['z0']+.008; look_at(A,(-18.6,0,3),1); face(A,mouth='flat' if i%3 else 'o',brow=.02); blink(A,tg+i*.7)
        stand(Bm,T0); Bm['root'].location[2]=Bm['z0']+.008; mp=root_mat(Bm)@Vector((0,-.8*Bm['u'],4.5*Bm['u'])); arm_to(Bm,1,mp,1); face(Bm,mouth='O',eyes=1.15,brow=.04); blink(Bm,tg); look_at(Bm,(-18.6,0,3),.6)
        Bm['head'].rotation_euler[2]+=R(30)*tl(t,2.3,2.6)
        q=ease(t/DUR); camset((-20.2+.9*q,-2.5,2.5),(-12.8,1.8,1.8),30,16)
    return dict(upd=upd)
SHOTS['SILENT']=SILENT_

def chacha_tray(Hc):
    e,c1,c2=tray(Hc['root'],(0,-.95*Hc['u'],2.05*Hc['u']))
    return e,c1,c2
def UNCLE_():
    W,C,T=street_set('invade',crowd_n=8,traffic_n=0,seed=15,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak(); CL=crowd_line(15,8)
    Hc=avatar_lh((-12.6,.6,0),-90,CHACHA,name='chacha'); e,c1,c2=chacha_tray(Hc)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg,freeze=T0-6,look=(-18,0,2.5)); ship_lights(S,t); stand(Z,T0); blink(Z,tg); face(Z,mouth='flat',brow=-.04,brow_r=-24,eyes=.85)
        for i,A in enumerate(CL): stand(A,T0); look_at(A,Hc['root'].location+Vector((0,0,2)),1); face(A,mouth='o',brow=.03); blink(A,tg+i)
        walk_path(Hc,[(-12.6,.6),(-16.75,.2)],t,0,DUR+.4,step=.42,arm=0); arms(Hc,-48,0,12,-48,0,-12); face(Hc,mouth='flat',brow=0); blink(Hc,tg)
        x=Hc['root'].location[0]; camset((x-.5,-3.75,1.6),(x-.6,.3,1.65),32,16)
    return dict(upd=upd)
SHOTS['UNCLE']=UNCLE_

def OFFER_():
    W,C,T=street_set('invade',crowd_n=6,traffic_n=0,seed=16,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak(); CL=crowd_line(16,8)
    Hc=avatar_lh((CHPOS[0],CHPOS[1],0),-90,CHACHA,name='chacha'); e,c1,c2=chacha_tray(Hc)
    def upd(t):
        tg=T0+t; ship_lights(S,t); stand(Z,tg); blink(Z,tg); stand(Hc,tg); blink(Hc,tg); upd_crowd(C,tg,freeze=T0-6,look=(-18,0,2.5))
        for i,A in enumerate(CL): stand(A,T0); look_at(A,(-17.5,0,2.2),1); face(A,mouth='o'); blink(A,tg+i)
        k=tl(t,0,.5); arms(Hc,-48-30*k,0,12,-48-30*k,0,-12); e.location=(0,-(.95+.45*k)*Hc['u'],(2.05+.55*k)*Hc['u'])
        talk(Hc,t,40.76-T0,43.17-T0); face(Hc,brow=.03); look_at(Hc,(-18.6,0,3.0),.9)
        face(Z,mouth='flat',brow=-.04+.08*tl(t,2.6,3.0),brow_r=-24+30*tl(t,2.6,3.0),eyes=.85); look_at(Z,(CHPOS[0],CHPOS[1],1.6),tl(t,.3,.8)*.8)
        camset((-17.6,-5.6,1.9),(-17.6,.15,2.3),26,5.6)
    return dict(upd=upd)
SHOTS['OFFER']=OFFER_

def CONF_():
    W,C,T=street_set('invade',crowd_n=4,traffic_n=0,seed=17,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak()
    Hc=avatar_lh((CHPOS[0],CHPOS[1],0),-90,CHACHA,name='chacha'); e,c1,c2=chacha_tray(Hc)
    def upd(t):
        tg=T0+t; ship_lights(S,t); stand(Z,tg); blink(Z,tg); stand(Hc,tg); arms(Hc,-78,0,12,-78,0,-12); e.location=(0,-1.4*Hc['u'],2.6*Hc['u']); face(Hc,mouth='smile',brow=.02)
        face(Z,mouth='flat',brow=.05,brow_r=12,eyes=1.05); Z['head'].rotation_euler=(R(14*tl(t,.2,.6)),R(12*tl(t,.4,.9)),R(-10*math.sin(t*2.2)*tl(t,.9,1.2)))
        camset((-16.6,-1.35,2.45),(-18.6,.15,2.5),38,4.0,focus=(-18.6,.15,2.5))
    return dict(upd=upd)
SHOTS['CONF']=CONF_

def ACCEPT_():
    W,C,T=street_set('invade',crowd_n=4,traffic_n=0,seed=18,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak()
    Hc=avatar_lh((CHPOS[0],CHPOS[1],0),-90,CHACHA,name='chacha'); e,c1,c2=chacha_tray(Hc); zc=in_hand(Z,1,lambda e_: cup(e_,(0,-.06,.02),1.0)); zc.scale=(0,0,0)
    def upd(t):
        tg=T0+t; ship_lights(S,t); stand(Z,tg); blink(Z,tg); stand(Hc,tg); blink(Hc,tg); arms(Hc,-78,0,12,-78,0,-12); e.location=(0,-1.4*Hc['u'],2.6*Hc['u']); face(Hc,mouth='smile',brow=.02)
        c1w=Hc['root'].matrix_world@Vector((0,-1.4*Hc['u'],2.6*Hc['u'])) if False else root_mat(Hc)@Vector((-.1*0,-1.4*Hc['u']-.0,2.6*Hc['u']+.06))
        k=tl(t,.15,.65); got=t>.7; up=tl(t,.9,1.4)
        if not got: arm_to(Z,1,c1w,k,base=(0,0,0)); zc.scale=(0,0,0); c1.scale=(1,1,1)
        else:
            c1.scale=(0,0,0); zc.scale=(1,1,1); mp=root_mat(Z)@Vector((0,-.9*Z['u'],4.5*Z['u'])); arm_to(Z,1,c1w.lerp(mp,up),1)
        face(Z,mouth='o' if up>.7 else 'flat',brow=.02,eyes=.9); Z['head'].rotation_euler=(R(-6*up),0,0)
        camset((-17.6,-4.3,2.05),(-17.8,.15,2.25),30,4.0)
    return dict(upd=upd)
SHOTS['ACCEPT']=ACCEPT_

# ------------------------------------------------------------------ dhaba
DH=dict(zx=17.0,zy=5.78,cy=4.22)
def dhaba_set(crowd_n=10,seed=20):
    W,C,T=street_set('morning_s',crowd_n=crowd_n,traffic_n=0,seed=seed,avoid=((10,24,2.8,7.0),)); T=make_traffic(5,seed,lanes=((-2.0,-1),))
    Z=avatar_lh((DH['zx'],DH['zy'],0),0,ZORAK,name='zorak'); sit(Z,1,.56); Z['z0']=0
    Hc=avatar_lh((DH['zx'],DH['cy'],0),180,CHACHA,name='chacha'); sit(Hc,1,.56)
    J=avatar_lh((17.6,8.75,0),0,JAMEEL,name='jameel')
    Bm=avatar_lh((19.6,5.78,0),0,BILAL,name='bilal'); sit(Bm,1,.56)
    K=karahi_obj((DH['zx'],5.0,.95),.75); KB=karahi_obj((17.0,8.0,1.05),1.1)
    fl=point((17,8.0,1.3),180,(1,.55,.25),.3,shadow=False); steam((DH['zx'],5.0,1.3),0,6,14,7,.07); steam((17.0,8.0,1.5),0,6,14,9,.09)
    flame(lambda t:(17.0,8.05,1.0),0,dur=99,size=.12,seed=3,dirv=(0,0,1))
    return W,C,T,Z,Hc,J,Bm,K,fl
def DHABA_():
    W,C,T,Z,Hc,J,Bm,K,fl=dhaba_set(12,20); hideH(Z) if False else None
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); upd_traffic(T,tg)
        for H_ in (Z,Hc,Bm): blink(H_,tg); H_['root'].location[2]=.56-1.5*H_['u']
        J['root'].location[2]=.008; blink(J,tg); J['arm'][-1].rotation_euler=(R(-70+12*math.sin(t*5)),0,R(-20+18*math.sin(t*5))); J['arm'][1].rotation_euler=(R(-20),0,R(10)); face(J,mouth='flat',brow=-.02)
        Z['arm'][1].rotation_euler=(R(-55),0,R(10)); Z['arm'][-1].rotation_euler=(R(-50),0,R(-10)); face(Z,mouth='flat',brow=.03,eyes=1.0); look_at(Z,(17,5.0,1.1),.8)
        Hc['arm'][1].rotation_euler=(R(-50),0,0); Hc['arm'][-1].rotation_euler=(R(-50),0,0); face(Hc,mouth='smile'); look_at(Hc,(DH['zx'],DH['zy'],2.2),.6)
        face(Bm,mouth='o',eyes=1.2,brow=.05); look_at(Bm,(17,5.0,1.1),1); Bm['arm'][1].rotation_euler=(R(-45),0,0); Bm['arm'][-1].rotation_euler=(R(-45),0,0)
        fl.data.energy=150+60*math.sin(t*17)*math.sin(t*7.3)
        q=ease(t/DUR); camset((14.4+1.0*q,.6,2.45),(17.2,5.6,1.55),27,16)
    return dict(upd=upd)
SHOTS['DHABA']=DHABA_
def dhaba_close(view):
    W,C,T,Z,Hc,J,Bm,K,fl=dhaba_set(6,21); food=in_hand(Z,1,lambda e: oico((0,-.12,.02),.08,M('#C2552A',.5),e,sc=(1.2,1,.7),sub=1))
    sp=sparkles((DH['zx'],DH['zy'],2.9),.6,.2,1.4,26,.05,9,.6) if view=='WIDE' else None
    if view=='WIDE':
        for s in (-1,1): puff((DH['zx']+s*.5,DH['zy'],3.0),.35,.12,5,PUFF,.6,.9,(s*.4,0,.3),seed=11+s); puff((DH['zx']+s*.5,DH['zy'],3.0),.9,.12,5,PUFF,.6,.9,(s*.4,0,.3),seed=13+s)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); upd_traffic(T,tg)
        for H_ in (Z,Hc,Bm): blink(H_,tg); H_['root'].location[2]=.56-1.5*H_['u']
        fl.data.energy=150+60*math.sin(t*17)*math.sin(t*7.3); J['arm'][-1].rotation_euler=(R(-70+12*math.sin(t*5)),0,R(-20+18*math.sin(t*5)))
        mp=root_mat(Z)@Vector((0,-.9*Z['u'],4.5*Z['u'])); kp=Vector((DH['zx'],5.0,1.25))
        if view=='BITE':
            a=tl(t,.1,.45); b=tl(t,.45,.8); c=tl(t,1.0,1.3); tgt=kp.lerp(mp,b) if a>=1 else kp
            arm_to(Z,1,tgt,max(a,1-c) if t<1.0 else 1-c,base=(R(-55),0,R(10))); food.scale=(0,0,0) if t>.85 else (1,1,1)
            chew=t>.85; face(Z,mouth=('o' if int(t*8)%2 else 'flat') if chew else 'flat',brow=.03); Z['head'].rotation_euler=(R(-4*b+3*math.sin(t*16)*chew),0,0)
            camset((16.3,3.3,2.0),(DH['zx'],DH['zy'],2.1),38,4.0)
        elif view=='WIDE':
            food.scale=(0,0,0); w=tl(t,.15,.3); face(Z,mouth='O' if w>.5 else 'flat',brow=.06*w,eyes=1+.5*w); Z['arm'][1].rotation_euler=(R(-55),0,R(10))
            Z['root'].location[0]=DH['zx']+.02*math.sin(t*60)*w*(1-tl(t,1.0,1.4)); Z['head'].rotation_euler=(R(-8*w),0,0)
            for o in Z.get('xeyes',[]):
                if '_s0' not in o: o['_s0']=tuple(o.scale)
                k=1+.45*w; o.scale=tuple(v*k for v in o['_s0'])
            q=ease(t/DUR); camset((DH['zx']+.2,3.2+.3*q,2.35),(DH['zx'],DH['zy'],2.3),42+8*q,4.0)
        elif view=='POWER':
            food.scale=(0,0,0); s=tl(t,0,.35); Z['root'].location[2]=L(.56-1.5*Z['u'],.008,s)
            for q_ in (1,-1): Z['leg'][q_].rotation_euler[0]=-R(90)*(1-s)
            Z['root'].location[1]=DH['zy']+.25*s; k=tl(t,.3,.7); Z['arm'][1].rotation_euler=(R(-165*k),0,R(10*k)); Z['arm'][-1].rotation_euler=(R(-20),0,R(-30*k))
            talk(Z,t,55.37-T0,56.79-T0); face(Z,brow=.04,brow_r=-10,eyes=1.25); Z['head'].rotation_euler=(R(-10*k),0,0)
            camset((DH['zx']+1.7,3.5,1.0),(DH['zx'],DH['zy']+.25,2.5),26,16)
        elif view=='SMILE':
            food.scale=(0,0,0); Z['root'].location[2]=.008
            for q_ in (1,-1): Z['leg'][q_].rotation_euler[0]=0
            Z['root'].location[1]=DH['zy']+.25; Z['arm'][1].rotation_euler=(R(-40),0,0); face(Z,mouth='o',eyes=1.2)
            talk(Hc,t,58.72-T0,60.37-T0); face(Hc,brow=.04,brow_r=-6); look_at(Hc,(DH['zx'],DH['zy']+.25,2.3),.55); k=tl(t,1.6,2.0)
            Hc['arm'][1].rotation_euler=(R(-50-60*k),0,R(-10*k)); Hc['root'].rotation_euler[2]=R(180)
            camset((19.9,6.9,2.45),(DH['zx'],DH['cy'],1.75),50,4.0,focus=(DH['zx'],DH['cy'],1.75))
    return dict(upd=upd)
for _v in ('BITE','WIDE','POWER','SMILE'): SHOTS[_v]=(lambda v=_v: dhaba_close(v))

# ------------------------------------------------------------------ battle
def ARMY_():
    W,C,T=street_set('invade',crowd_n=8,traffic_n=0,seed=22,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); A=army()
    def upd(t):
        tg=T0+t; upd_crowd(C,tg,freeze=T0-9,look=(-21,0,2.5),react=.4); ship_lights(S,t)
        for i,H_ in enumerate(A):
            stand(H_,tg+i); blink(H_,tg+i); k=tl(t,63.1-T0+i*.06,63.5-T0+i*.06); H_['arm'][1].rotation_euler=(R(-15-75*k),0,R(4)); face(H_,mouth='flat',brow=-.03,brow_r=-20)
            H_['head'].rotation_euler[2]=R(15*math.sin(t*1.7+i))*(1-k); H_['tipm'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=12*tl(t,63.4-T0,64.4-T0)
            if i==0: H_['root'].location[2]=H_['z0']+.008+.02*abs(math.sin(t*9))*(1-k)
        q=ease(t/DUR); camset((-13.2-.6*q,-3.4,1.2),(-19.2,0,2.0),28,16)
    return dict(upd=upd)
SHOTS['ARMY']=ARMY_

def LASER_():
    W,C,T=street_set('invade',crowd_n=10,traffic_n=0,seed=23,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); A=army(4,5)
    Bk=motorbike((0,-1.6,0),180,'#C8372D'); Bk['root'].scale=(1.3,1.3,1.3); Bk['r']*=1.3
    Hm=avatar_lh((0,0,0),-90,HAMZA,name='hamza'); Hm['root'].parent=Bk['root']; Hm['root'].location=(-.15,0,.42); Hm['root'].rotation_euler=(0,0,R(-90)); sit(Hm,1,.55,legs=70); Hm['z0']=0
    ph=in_hand(Hm,1,lambda e: obox((0,-.1,.05),(.06,.01,.11),M('#16171C',.2,spec=.9),.01,e))
    LZ=[ocyl((0,0,-50),.07,2.6,M('#FF3A5A',.2,emit=14),rot=(0,R(90),0),seg=10) for i in range(2)]
    hitp=Vector((-3.5,-6.6,3.6)); sp=sparkles(hitp,.5,67.9-T0,68.5-T0,24,.06,4,.5)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg,freeze=T0-9,look=(-12,-1.6,1.5),react=.6); ship_lights(S,t)
        for i,H_ in enumerate(A):
            stand(H_,tg+i); blink(H_,tg+i); H_['arm'][1].rotation_euler=(R(-90),0,R(4)); face(H_,mouth='flat',brow=-.03,brow_r=-20); H_['tipm'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=12
        x=6-5.2*t; drive(Bk,x,-1.6,180,5.2*t); blink(Hm,tg); Hm['head'].rotation_euler=(R(28),0,0); Hm['arm'][1].rotation_euler=(R(-95),0,R(18)); Hm['arm'][-1].rotation_euler=(R(-70),0,R(-6))
        face(Hm,mouth='smile',brow=.0,eyes=.8); lean=math.sin(pi*tl(t,1.4,2.15))*1.0
        Bk['root'].rotation_euler[0]=R(-24*lean); Bk['root'].location[2]=.0
        for i,(t0_,y_,z_) in enumerate(((65.9-T0,-1.6,1.75),(67.5-T0,-3.0,2.9))):
            q=t-t0_; o=LZ[i]
            if q<0 or q>.7: o.location=(0,0,-50)
            else: o.location=(-20.5+42*q,y_+(-3.6*q if i==1 else 0),z_+(1.0*q if i==1 else 0))
        camset((-10.0,-6.7,1.3),(-12.5,-1.6,1.7),26,16)
    return dict(upd=upd)
SHOTS['LASER']=LASER_

ZR=dict(x=-12.0,y=-5.0)
def SLIP_():
    W,C,T=street_set('invade',crowd_n=8,traffic_n=0,seed=24,avoid=((-30,-12,-4.5,4.5),(-14,-10,-7,-4),)); Za=avatar_lh((ZR['x'],ZR['y'],.07),160,ZARA,name='zara'); sl=slipper_obj()
    def upd(t):
        tg=T0+t; upd_crowd(C,tg,freeze=T0-9,look=(-18,0,2.6),react=.3); stand(Za,tg); blink(Za,tg)
        a=tl(t,.0,.35); b=tl(t,.45,.7); face(Za,mouth='flat',brow=-.02,brow_r=-18,eyes=.9); look_at(Za,(-18.6,.15,3),.8)
        Za['arm'][1].rotation_euler=(R(L(-20,40,a)-200*b),0,R(10)); Za['arm'][-1].rotation_euler=(R(-30),0,R(-10)); Za['root'].rotation_euler[0]=R(6*b)
        hp=root_mat(Za)@Vector((.5*Za['u'],.3*Za['u']+.6*a*(1-b),(2.0+1.8*a)*Za['u']))
        if t<.6: sl.location=hp if a>0 else (0,0,-50); sl.rotation_euler=(R(40),0,0)
        else:
            q=(t-.6); p0=hp; p1=Vector((-18.6,.15,3.25)); f=q/1.25; sl.location=p0.lerp(p1,f)+Vector((0,0,2.2*f*(1-f)*4*.5)); sl.rotation_euler=(q*18,q*7,0)
        camset((-9.5,-2.2,1.8),(ZR['x']-.7,ZR['y'],2.0),32,5.6,focus=(ZR['x'],ZR['y'],2))
    return dict(upd=upd)
SHOTS['SLIP']=SLIP_

def HIT_():
    W,C,T=street_set('invade',crowd_n=6,traffic_n=0,seed=25,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak(); A=army(4,5); sl=slipper_obj()
    th=71.55-T0; sp=sparkles((-18.25,.05,3.0),.4,th,th+.6,20,.06,6,.3)
    def upd(t):
        tg=T0+t; ship_lights(S,t); stand(Z,tg); blink(Z,tg); upd_crowd(C,tg,freeze=T0-9,look=(-18,0,2.6))
        for i,H_ in enumerate(A): stand(H_,tg+i); H_['arm'][1].rotation_euler=(R(-90),0,R(4)); face(H_,mouth='flat',brow=-.03,brow_r=-20); H_['tipm'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=12
        p1=Vector((-18.25,.05,3.0)); p0=p1+Vector((6.2,-5.0,-1.0))
        if t<th: f=1-(th-t)/1.3; sl.location=p0.lerp(p1,max(0,f))+Vector((0,0,1.2*max(0,f)*(1-max(0,f)))); sl.rotation_euler=(t*18,t*7,0); face(Z,mouth='flat',brow=-.04,brow_r=-24,eyes=.85)
        else:
            q=t-th; sl.location=(p1.x+.9*q,p1.y-.6*q,max(.03,p1.z+2.0*q-4.9*q*q)); sl.rotation_euler=(th*18+q*10,th*7,0)
            j=math.exp(-q*5)*math.sin(q*30); Z['head'].rotation_euler=(R(-14*math.exp(-q*3)),R(10*j),0); face(Z,mouth='o',brow=.05,eyes=.55 if q<.25 else 1.1)
        camset((-16.3,-1.8,2.6),(-18.6,.15,2.65),34,4.0)
    return dict(upd=upd)
SHOTS['HIT']=HIT_

def FREEZE_():
    W,C,T=street_set('invade',crowd_n=16,traffic_n=0,seed=26,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak(); A=army(6,6); sl=slipper_obj(); sl.location=(-17.1,-.6,.03); sl.rotation_euler=(0,0,.5)
    def upd(t):
        tg=T0+t; ship_lights(S,t); stand(Z,T0); blink(Z,tg); face(Z,mouth='flat',brow=.06,eyes=1.15); upd_crowd(C,tg,freeze=T0-9,look=(-18,0,2.6))
        for i,H_ in enumerate(A): stand(H_,T0); H_['arm'][1].rotation_euler=(R(-90),0,R(4)); face(H_,mouth='o',brow=.05); H_['tipm'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=12*(1-tl(t,1.0,1.6))
        q=ease(t/DUR); camset(LV((-12.6,-3.6,4.4),(-11.6,-3.9,5.4),q),(-19.5,0,2.0),26,16)
    return dict(upd=upd)
SHOTS['FREEZE']=FREEZE_

def LEAVE_():
    W,C,T=street_set('invade',crowd_n=4,traffic_n=0,seed=27,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak()
    def upd(t):
        tg=T0+t; ship_lights(S,t); stand(Z,tg); blink(Z,tg); talk(Z,t,74.92-T0,75.58-T0); face(Z,brow=.05,brow_r=10,eyes=.9)
        Z['head'].rotation_euler=(R(6),0,R(25*math.sin(t*4.5)*(1-tl(t,.9,1.1)))); k=tl(t,.9,1.3); Z['root'].rotation_euler[2]=R(90+150*k)
        Z['root'].location[2]=Z['z0']+.008+.05*abs(math.sin(t*8))*k; Z['root'].rotation_euler[0]=R(8*k)
        camset((-16.4,-1.2,2.5),(-18.6,.15,2.55),36,4.0)
    return dict(upd=upd)
SHOTS['LEAVE']=LEAVE_

def STOP_():
    W,C,T=street_set('invade',crowd_n=14,traffic_n=0,seed=28,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak(); A=army(4,7)
    def upd(t):
        tg=T0+t; ship_lights(S,t); upd_crowd(C,tg,freeze=T0-9,look=(-19,0,2.6))
        for i,H_ in enumerate(A): stand(H_,tg+i); blink(H_,tg+i); look_at(H_,Z['root'].location+Vector((0,0,2.5)),.8); face(H_,mouth='flat')
        ts=77.0-T0; tr=tl(t,77.9-T0,78.7-T0)
        if t<ts:
            walk_path(Z,[(-18.6,.15),(-19.7,0)],t,0,ts+.15,step=.35,arm=8)
        else:
            legs0(Z); Z['root'].location=(-19.7,0,.008); Z['root'].rotation_euler=(0,0,R(-90+180*tr)); idle(Z,tg)
        face(Z,mouth='flat',brow=.03); blink(Z,tg)
        camset((-11.8,-3.3,2.0),(-20.8,0,2.2),30,16)
    return dict(upd=upd)
SHOTS['STOP']=STOP_

def ASK_():
    W,C,T=street_set('invade',crowd_n=4,traffic_n=0,seed=29,avoid=((-30,-12,-4.5,4.5),)); S=ship_landed(); Z=zorak((-19.7,0,0),90)
    def upd(t):
        tg=T0+t; ship_lights(S,t); stand(Z,tg); blink(Z,tg)
        k=tl(t,0,.4); mp=root_mat(Z)@Vector((0,-1.1*Z['u'],3.3*Z['u']))
        for s in (1,-1): arm_to(Z,s,(mp.x,mp.y+s*.06,mp.z),k)
        Z['head'].rotation_euler=(R(8*k),R(-12*k),0); Z['root'].rotation_euler[1]=R(4*math.sin(t*3))*k
        talk(Z,t,79.27-T0,80.86-T0); face(Z,brow=.06,brow_r=16,eyes=1.1)
        camset((-17.5,-1.05,2.35),(-19.7,0,2.55),38,4.0)
    return dict(upd=upd)
SHOTS['ASK']=ASK_

def PACK_():
    W,C,T=street_set('invade',crowd_n=8,traffic_n=0,seed=30,avoid=((-30,-12,-4.5,4.5),)); CL=crowd_line(30,6)
    Hc=avatar_lh((-15.6,.3,0),-90,CHACHA,name='chacha'); J=avatar_lh((-15.0,1.6,0),-100,JAMEEL,name='jameel')
    def upd(t):
        tg=T0+t; upd_crowd(C,tg,freeze=T0-9,look=(-21,0,2.6))
        for i,A in enumerate(CL): stand(A,tg+i); blink(A,tg+i); look_at(A,(-15.6,.3,2.2),.8); face(A,mouth='smile' if t>2.2 else 'flat')
        stand(Hc,tg); blink(Hc,tg); stand(J,tg); blink(J,tg)
        k=tl(t,0,.5); u=Hc['u']
        for s in (1,-1): Hc['arm'][s].rotation_euler=(R(-62*k),0,R(-s*58*k))
        talk(Hc,t,82.6-T0,84.0-T0); face(Hc,brow=-.02+.08*tl(t,2.6,2.8),brow_r=-4,eyes=.72)
        J['arm'][-1].rotation_euler=(R(-20),0,R(-8)); face(J,mouth='smirk',brow=.02,eyes=.8); look_at(J,(-21,0,3),.5)
        camset((-17.5,-1.4,1.85),(-15.6,.4,1.75),34,4.0,focus=(-15.6,.3,1.75))
    return dict(upd=upd)
SHOTS['PACK']=PACK_

def BUY_():
    W,C,T=street_set('morning_s',crowd_n=8,traffic_n=0,seed=31,avoid=((10,24,2.5,7.0),)); J=avatar_lh((17.0,7.45,0),0,JAMEEL,name='jameel')
    KB=karahi_obj((17.0,8.0,1.05),1.1); flame(lambda t:(17.0,8.05,1.0),0,dur=99,size=.12,seed=3,dirv=(0,0,1)); steam((17.0,8.0,1.5),0,6,14,9,.09)
    Q=[avatar_lh((17.0+i*.8,6.1-i*.9,0),160,soldier_design(60+i),name='q%d'%i) for i in range(5)]
    bags=[in_hand(H_,1,lambda e: (obox((0,-.05,-.12),(.12,.08,.16),M('#F4F1EA',.7),.02,e),obox((0,-.05,-.06),(.125,.085,.03),M('#C8372D',.6),.01,e))) for H_ in Q]
    for b_ in bags: b_.scale=(0,0,0)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); stand(J,tg); blink(J,tg); face(J,mouth='smile',brow=.02)
        k=abs(math.sin(t*3.4)); J['arm'][1].rotation_euler=(R(-60-20*k),0,R(5)); J['arm'][-1].rotation_euler=(R(-60-20*(1-k)),0,R(-5))
        for i,H_ in enumerate(Q):
            got=t>.3+i*.35; bags[i].scale=(1,1,1) if got else (0,0,0)
            if got and i==0:
                f=walk_path(H_,[(17.0,6.1),(15.6,3.6),(11.5,1.5)],t,.4,DUR+1.5,step=.55); H_['arm'][1].rotation_euler=(R(-20),0,0)
            else: stand(H_,tg+i); look_at(H_,(17,7.4,2.5),.6); H_['arm'][1].rotation_euler=(R(-25 if got else 0),0,0)
            face(H_,mouth='grin' if got else 'o',eyes=1.1); blink(H_,tg+i)
        camset((12.8,2.0,2.6),(17.6,5.6,1.8),28,16)
    return dict(upd=upd)
SHOTS['BUY']=BUY_

def DELIV_():
    W,C,T=street_set('morning_s',crowd_n=20,traffic_n=0,seed=32,avoid=((-30,-12,-4.5,4.5),)); S=saucer(SHIP_AT,True); S['root'].rotation_euler=(0,0,R(90)); S['hinge'].rotation_euler[0]=R(-85)
    CL=crowd_line(32,8)
    def upd(t):
        tg=T0+t; ship_lights(S,t); up=tl(t,.4,DUR); q=up*up
        S['root'].location=(SHIP_AT[0]-36*q,SHIP_AT[1]+8*q,SHIP_AT[2]+32*q+.3*math.sin(t*3)); S['root'].rotation_euler=(R(8*tl(t,.4,1.2)),0,R(90-20*q)); S['beam'].scale=(0,0,0)
        upd_crowd(C,tg,look=S['root'].location,cheer=tl(t,.5,1.0))
        for i,A in enumerate(CL):
            stand(A,tg+i); blink(A,tg+i); look_at(A,S['root'].location,1,maxpitch=60); w=math.sin(t*9+i); A['arm'][1].rotation_euler=(R(-150),0,R(20+25*w)); face(A,mouth='grin')
        p=S['root'].location; camset((-8.6,-3.4,1.4),(p.x*.8-8.6*.2,p.y*.6,p.z*.85+1.2),26,16)
    return dict(upd=upd)
SHOTS['DELIV']=DELIV_

# ------------------------------------------------------------------ Mars
def mars_set(crowd_n=26,seed=40,avoid=()):
    W,C,T=street_set('mars',crowd_n=crowd_n,traffic_n=0,seed=seed,kind='mars',theme='mars',avoid=avoid)
    for x in (-6.5,6.5): B.cyl((x,-4.6,3.4),.16,6.8,M('#C9CED8',.3,metal=.8),seg=10); B.cyl((x,4.6,3.4),.16,6.8,M('#C9CED8',.3,metal=.8),seg=10)
    B.box((0,0,6.9),(7.0,4.8,.08),M('#C9CED8',.3,metal=.8),.02); B.box((0,-4.75,6.5),(6.6,.1,.55),M('#1F4D3A',.6),.04); B.done('arch')
    sign_text('LAHORI FOOD STREET - MARS',(0,-4.88,6.5),.62,'#F6E7B0',(0,-1,0),e=2.5)
    for m,(x,y,z,r_) in enumerate(((-30,120,60,9),(40,140,42,5))): oico((x,y,z),r_,M(['#D8C8B8','#B8A89A'][m],.9,kind='concrete',sc=.1),sub=3)
    return W,C,T
def MARS_():
    W,C,T=mars_set(32,40)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); q=ease(t/DUR); camset(LV((-52,-1.5,24),(-25,-1.2,6.2),q),LV((-8,1.5,1.5),(-2,1.2,2.4),q),24,16)
    return dict(upd=upd)
SHOTS['MARS']=MARS_
def MARSK_():
    W,C,T=mars_set(18,41,avoid=((-6,4,-6.9,-4.0),)); G=[avatar_lh((2.0+i*1.1,-4.95+(i%2)*.45,.07),-90,mars_design(500+i),name='mk%d'%i) for i in range(3)]
    cup(G[0]['arm'][1],hand_loc(G[0],1)); oico(hand_loc(G[1],-1),.09,M('#F2A11A',.35,emit=.3),G[1]['arm'][-1],sc=(1,1,.45),sub=1)
    def upd(t):
        tg=T0+t; upd_crowd(C,tg)
        for i,H_ in enumerate(G):
            d=1.0*t; H_['root'].location[0]=2.0+i*1.1-d; walk(H_,d+i*.3,step=.55); blink(H_,tg+i); face(H_,mouth='grin' if i!=1 else 'smile')
            if i==0: H_['arm'][1].rotation_euler=(R(-60),0,R(8))
            if i==1: look_at(H_,G[0]['root'].location+Vector((0,0,2.3)),.8)
        x=G[1]['root'].location[0]; camset((x-4.6,-2.2,2.1),(x,-4.95,2.05),30,4.0)
    return dict(upd=upd)
SHOTS['MARSK']=MARSK_
ZP=dict(ZORAK); ZP.update(no_armour=True,kurta=True,shalwar=True,cuff=True,top='#F4F1EA',trim='#D6C9AE',pants='#F4F1EA',waistcoat='#1F4D3A',sandals='#5E3A1E',boots=None,gloves=None,belt='#F4F1EA',buckle='#F4F1EA',button='#C9A24A')
def pres_mars(view):
    W,C,T=mars_set(10,42,avoid=((-6,6,-6.9,3.5),))
    B.box((0,1.8,.25),(4.2,2.4,.25),M('#7A1F2E',.8,kind='fabric'),.05); podium(-1.0,.6,'#3A3046','#C8372D'); flag(-3.6,2.6,4.4,True); flag(2.6,2.6,4.4,True)
    B.box((0,3.2,3.2),(3.0,.08,.7),M('#1F4D3A',.6),.05); B.done('stagem')
    bn=text('2ND BRANCH',(0,3.08,3.2),(0,-1,0),.9,M('#F6E7B0',.3,emit=2.5),.03); bn.scale=(0,0,0)
    Z=avatar_lh((-1.0,1.15,.5),0,ZP,name='zorakp')
    au=[avatar_lh((x,y,0),180,mars_design(700+i),name='ma%d'%i) for i,(x,y) in enumerate(((-2.6,-2.3),(-1.1,-2.9),(.6,-2.4),(4.6,-3.0),(-2.0,-4.2),(-3.6,-3.2),(1.4,-3.6)))]
    rib=[obox((x,-.55,1.3),(1.0,.02,.07),M('#C8372D',.5),.01) for x in (.9,2.9)]; posts=[B.cyl((x,-.55,.85),.05,1.7,M('#C9CED8',.3,metal=.8),seg=8) for x in (-.1,3.9)]; B.done('rib')
    sc=empty((0,0,0)); obox((.0,-.3,0),(.03,.32,.05),M('#C9CED8',.25,metal=.9),.01,sc); obox((0,.08,0),(.08,.08,.03),M('#E8554D',.5),.02,sc)
    cf=confetti((1.9,-.5,3.5),101.2-T0,70,8) if view=='BRANCH' else None
    def upd(t):
        tg=T0+t; upd_crowd(C,tg); stand(Z,tg); blink(Z,tg)
        for i,A in enumerate(au): stand(A,tg+i); blink(A,tg+i); look_at(A,(-1,1.15,3.0),.7)
        if view=='PRESM':
            talk(Z,t,97.2-T0,99.51-T0); face(Z,brow=-.02,brow_r=-10,eyes=.95); k=tl(t,2.0,2.4); Z['arm'][1].rotation_euler=(R(-70*k),0,R(14*k)); Z['arm'][-1].rotation_euler=(R(-40),0,R(-6))
            sc.scale=(0,0,0)
            for i,A in enumerate(au): face(A,mouth='o' if t>3.0 else 'flat',brow=.02)
            q=ease(t/DUR); camset((1.6,-1.5+.4*q,2.5),(-1.0,1.15,2.8),30,5.6,focus=(-1,1.15,2.9))
        else:
            talk(Z,t,99.58-T0,101.81-T0); face(Z,brow=.04,eyes=1.0); cut=101.0-T0
            Z['root'].location=(L(-1.0,1.9,tl(t,0,.6)),L(1.15,.0,tl(t,0,.6)),L(.5,0.0,tl(t,0,.6))+.008)
            hp=root_mat(Z)@Vector((.5*Z['u'],-.9*Z['u'],2.3*Z['u'])); arm_to(Z,1,(1.9,-.55,1.3+.15*(1-tl(t,cut-.3,cut))),tl(t,.5,.9))
            sc.location=(1.9,-.62,1.35); sc.rotation_euler=(0,0,R(25*math.sin(min(t,cut)*14)*(1-tl(t,cut,cut+.1))))
            c=tl(t,cut,cut+.4); rib[0].rotation_euler=(0,R(-70*c),0); rib[1].rotation_euler=(0,R(70*c),0); rib[0].location=(.9-.6*c,-.55,1.3-.5*c); rib[1].location=(2.9+.6*c,-.55,1.3-.5*c)
            bn.scale=(c,c,c); face(Z,mouth='grin' if t>cut else None)
            for i,A in enumerate(au):
                if t>cut: ph=math.sin(t*9+i)*.5+.5; A['arm'][1].rotation_euler=(R(-160),0,R(14+10*ph)); A['arm'][-1].rotation_euler=(R(-150),0,R(-14-10*ph)); face(A,mouth='grin'); A['root'].location[2]+=.08*ph
            q=ease(t/DUR); camset((3.8,-4.6+.5*q,4.3),(1.1,0.4,2.1),28,16)
    return dict(upd=upd)
for _v in ('PRESM','BRANCH'): SHOTS[_v]=(lambda v=_v: pres_mars(v))

def MSG_():
    SP=space(); blk=[]
    for o in SP['bb'].children:
        if o.type=='FONT': blk.append(o)
    def upd(t):
        msg=105.9-T0; on=t>msg and (int((t-msg)*6)%2==0 or t>msg+.8)
        for o in blk: o.scale=(1,1,1) if on or t<msg-1.2 else (0,0,0)
        SP['planet'].rotation_euler[2]=t*.05; SP['bb'].rotation_euler=(0,R(3*math.sin(t*.6)),R(-6+3*math.sin(t*.4)))
        q=ease(t/DUR); camset(LV((-6,-22,6),(1.2,6,3.5),q),LV((0,40,0),(2.5,22,3),q),28,16)
    return dict(upd=upd)
SHOTS['MSG']=MSG_
