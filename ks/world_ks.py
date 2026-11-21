# Sets for "The Karachi Survivor": flooded Saddar-style street with old apartment blocks and a corner cold-drink shop,
# Daniyal's small flat, phone close-ups (screen floating in a dark void). Rain + blackout controls.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
GRID=[]   # (material, base strength) — dimmed to 0 when the electricity goes
LAMPS=[]  # (light, base energy)
def gmat(col,e):
    m=bpy.data.materials.new('grid'); m.use_nodes=True; b=m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value=hexc(col); b.inputs['Emission Color'].default_value=hexc(col); b.inputs['Emission Strength'].default_value=e
    GRID.append((b,e)); return m
def glamp(loc,e,col=(1,.85,.6),r=.3):
    p=point(loc,e,col,r,False); LAMPS.append((p,e)); return p
def grid(k):
    for b,e in GRID: b.inputs['Emission Strength'].default_value=e*k
    for p,e in LAMPS: p.data.energy=e*k
def flat_block(cx,w,side,seed,Y=5.0):
    r=random.Random(seed); c=r.choice(['#D8CFC0','#C9B9A0','#E2D6C2','#B8C2C8','#D8C0A8','#C8C8B8','#E8D8C0']); stain=shade(c,.78)
    fl=r.choice([4,5,6]); fh=3.0; h=fl*fh+.5; s=side; yb=Y if s>0 else -Y; d=5.0; yc=yb+s*d
    B.box((cx,yc,h/2),(w/2-.05,d,h/2),M(c,.95,kind='wall',h2=stain,sc=.7),0)
    for f in range(1,fl):
        z=f*fh
        B.box((cx,yb-s*.6,z),(w/2-.2,.6,.08),M(shade(c,.85),.9,kind='concrete'),.02)
        B.box((cx,yb-s*1.18,z+.55),(w/2-.2,.04,.5),M(shade(c,.9),.9,kind='concrete'),.01)
        for k in range(int(w/1.6)):
            x=cx-w/2+.9+k*1.6; wl=gmat(r.choice(['#FFD98A','#FFE7B0','#D8F0FF']),r.uniform(1.2,2.6)) if r.random()<.55 else M('#2A3440',.2,spec=.8)
            B.box((x,yb-s*.02,z+1.5),(.45,.04,.6),wl,.01)
        if r.random()<.6: B.box((cx+r.uniform(-w/3,w/3),yb-s*1.25,z+1.0),(.4,.02,.35),M(r.choice(['#E8554D','#F4F1EA','#4D8FE8','#F2C14E','#35975A']),.9,kind='fabric'),0)
        if r.random()<.5: B.box((cx+r.uniform(-w/3,w/3),yb-s*.25,z+2.1),(.35,.2,.22),M('#E8E8E4',.5),.03)
    B.box((cx,yb-s*.02,h+.3),(w/2-.05,.08,.3),M(c,.9,kind='wall'),0)
    if r.random()<.8: B.cyl((cx+r.uniform(-1,1),yc,h+.9),.6,1.2,M(r.choice(['#2A2C34','#3A6A9A']),.5),seg=10)
    for k in range(r.randint(1,3)): B.box((cx+r.uniform(-w/2,w/2),yc,h+2.5),(.03,.03,2.0),M('#3A3D44',.5,metal=.5),0)
    # ground floor shutters
    for k in range(max(1,int(w/3.2))):
        x=cx-w/2+1.6+k*3.2; B.box((x,yb-s*.03,1.3),(1.3,.05,1.25),M(r.choice(['#5A6A70','#7A6A5A','#4A5A4A','#6A5A6A']),.6,metal=.5),.01)
        for j in range(12): B.box((x,yb-s*.08,.2+j*.2),(1.3,.01,.012),M('#3A3D44',.5,metal=.4),0)
        B.box((x,yb-s*.4,2.9),(1.5,.4,.25),M(r.choice(['#C8372D','#2B58C9','#35975A','#F2C14E','#F4F1EA']),.6),.02)
def minibus(loc,rotz=0):
    e=empty(loc,rot=(0,0,R(rotz))); cols=['#F2C14E','#2B8A7A','#C8372D','#2B58C9','#CF3F78']
    obox((0,0,1.25),(3.2,1.05,.95),M('#2B8A7A',.5),.08,e); obox((0,0,2.3),(3.2,1.08,.15),M('#F2C14E',.5),.05,e); obox((3.22,0,1.55),(.04,.9,.5),M('#1A2433',.06,spec=1.0),.02,e)
    for sy in (-1,1):
        for k in range(6): obox((-2.6+k*.95,sy*1.07,1.65),(.38,.02,.32),M('#1A2433',.06,spec=1.0),.02,e)
        for k in range(14): obox((-3.0+k*.45,sy*1.08,.65),(.18,.01,.12),M(cols[k%5],.4,emit=.3),.0,e,rot=(0,R(45),0))
        obox((0,sy*1.08,2.05),(3.0,.01,.06),M('#C8372D',.5),0,e)
    for (wx,sy) in ((2.2,-1),(2.2,1),(-2.0,-1),(-2.0,1)): wheel((wx,sy*.95,.45),.45,.25,e)
    for k in range(5): obox((3.24,-.8+k*.4,2.42),(.02,.12,.08),M(cols[k],.4,emit=.6),.0,e)
    return e
SHOPX=6.0
def street():
    r=random.Random(3)
    B.box((0,0,-.3),(90,4.0,.3),M('#2E3034',.95,kind='asphalt'),0)
    for s in (-1,1): B.box((0,s*4.5,-.05),(90,.5,.25),M('#9A968C',.9,kind='concrete'),.02)
    x=-44; i=0
    while x<44:
        w=r.choice([8,9,10,11])
        if x<SHOPX+2.6 and x+w>SHOPX-2.6:
            if SHOPX-2.6-x>2.5: flat_block((x+SHOPX-2.6)/2,SHOPX-2.6-x,1,i*7+5)
            x=SHOPX+2.6; i+=1; continue
        flat_block(x+w/2,w,1,i*7+5); x+=w; i+=1
    x=-44
    while x<44: w=r.choice([8,9,10]); flat_block(x+w/2,w,-1,i*11+3); x+=w; i+=1
    # poles + tangled wires + KESC-style transformer
    for x in range(-40,41,11): pole(x,4.3,9.0)
    wires(-44,44,4.3,4.3,8.5,7,3); wires(-44,44,4.3,-4.4,8.8,6,9)
    B.box((-7.5,4.3,6.2),(.6,.4,.5),M('#6E7378',.5,metal=.5),.03); B.cyl((-7.5,4.3,6.9),.08,.4,M('#C8C2B0',.5),seg=6)
    # floating debris
    for k in range(10): B.box((r.uniform(-30,30),r.uniform(-3.5,3.5),.05),(r.uniform(.1,.3),r.uniform(.08,.2),.02),M(r.choice(['#C8372D','#F4F1EA','#4D8FE8','#7A5A3A']),.8),.01,rot=(0,0,r.uniform(0,3)))
    for (x,y) in ((-16,4.6),(18,-4.6)): tree(x,y,1.2,'#3F7A3A','#4A3220')
def water(z=.32):
    w=M('#5E6E6A',.05,spec=1.0,alpha=.82); B.box((0,0,z/2-.3),(90,5.0,z/2+.3),w,0); B.done('water')
def cornershop(x=SHOPX,Y=5.0):
    wl=M('#E8E2D2',.9,kind='wall'); B.box((x,Y+3.3,1.6),(2.6,.1,1.6),wl,0); B.box((x-2.55,Y+1.6,1.6),(.08,1.7,1.6),wl,0); B.box((x+2.55,Y+1.6,1.6),(.08,1.7,1.6),wl,0)
    B.box((x,Y+1.6,3.25),(2.65,1.75,.06),M('#B8B0A0',.9,kind='concrete'),0); B.box((x,Y+1.6,.01),(2.5,1.6,.02),M('#B8A890',.6,kind='tile',sc=1.5),0)
    B.box((x,Y+.02,.3),(2.6,.06,.3),M('#3A6A8A',.6),.02)
    B.box((x,Y-.9,3.15),(3.0,.95,.06),M('#2B58C9',.8,kind='fabric',h2='#F4F1EA',sc=5),.02,rot=(R(-8),0,0))
    B.box((x,Y-.02,3.6),(2.7,.08,.38),M('#C8372D',.6),.02); stext('BISMILLAH COLD DRINK CORNER',(x,Y-.12,3.6),.2,'#FFF3B0',e=.4)
    B.box((x,Y+.6,.55),(2.3,.4,.55),M('#7A5A3A',.7,kind='wood'),.03); B.box((x,Y+.6,1.12),(2.35,.45,.03),M('#C9C2B0',.4,spec=.7),.01)
    # fridge (empty) + shelves of snacks + sign
    B.box((x+1.7,Y+2.0,1.1),(.55,.45,1.1),M('#E8E8E4',.4),.04); B.box((x+1.7,Y+1.54,1.15),(.48,.02,.95),M('#BFD6E8',.05,spec=1.0,alpha=.4),.01)
    B.box((x+1.7,Y+1.56,2.15),(.5,.02,.1),gmat('#C8372D',1.4),.0)
    for z in (.7,1.25,1.8): B.box((x+1.7,Y+2.0,z),(.5,.4,.015),M('#C9CED8',.4),.0)
    for row in range(3):
        for k in range(9): B.box((x-2.1+k*.3,Y+3.05,.9+row*.55),(.12,.1,.16),M(r_col(row,k),.6),.02)
    B.box((x-.8,Y+3.18,2.6),(1.3,.04,.3),M('#16171C',.6),.02); stext('NO UDHAAR',(x-.8,Y+3.13,2.6),.18,'#F2C14E')
    B.box((x,Y+1.6,3.15),(.5,.5,.02),gmat('#FFFFFF',4.0),0)  # tube light
    B.cyl((x+.4,Y+1.6,3.0),.03,.3,M('#3A3D44',.5),seg=6)
    # crates + stool outside
    for (dx,dy) in ((-2.0,-.4),(-1.6,-.6)): B.box((x+dx,Y+dy,.42+.0),(.25,.2,.12),M('#C8372D',.6),.02)
def r_col(a,b): return ['#C8372D','#F2C14E','#2B58C9','#35975A','#F28A3A','#7448C2'][(a*3+b)%6]
def ceiling_fan(loc,par=None):
    e=empty(loc,par); ocyl((0,0,.15),.025,.3,M('#5A5E66',.5,metal=.5),e,rot=(0,0,0),seg=6); ocyl((0,0,0),.12,.1,M('#6A6E76',.5,metal=.5),e,rot=(0,0,0),seg=12)
    bl=empty((0,0,-.02),e)
    for a in range(3): obox((math.cos(a*2.094)*.45,math.sin(a*2.094)*.45,0),(.42,.08,.01),M('#8A6A4A',.6,kind='wood'),.01,bl,rot=(0,0,a*2.094))
    return bl
def flat_room():
    fl=M('#C9B8A0',.4,kind='tile',h2='#B8A890',sc=1.4,spec=.6); wl=M('#9FC8C0',.9,kind='wall'); wl2=M('#E8E2D6',.9,kind='wall')
    B.box((0,0,-.05),(3.4,2.8,.05),fl,0); B.box((0,0,3.2),(3.4,2.8,.05),M('#F4F1EA',.9),0)
    B.box((-3.4,0,1.6),(.08,2.8,1.6),wl,0); B.box((3.4,-1.4,1.6),(.08,1.4,1.6),wl,0); B.box((3.4,2.2,1.6),(.08,.6,1.6),wl,0)
    B.box((3.4,.8,.45),(.08,1.0,.45),wl,0); B.box((3.4,.8,2.85),(.08,1.0,.35),wl,0)  # window opening y -.2..1.8, z .9-2.5
    B.box((0,2.8,1.6),(3.4,.08,1.6),wl2,0)
    for z in (.9,2.5): B.box((3.38,.8,z),(.06,1.05,.04),M('#2F4F4F',.5,metal=.4),0)
    for k in range(6): B.box((3.36,-.15+k*.38,1.7),(.02,.02,.8),M('#2F4F4F',.5,metal=.4),0)
    B.box((3.42,.8,1.7),(.01,1.0,.8),M('#9AB0C0',.05,spec=1.0,alpha=.25),0)
    # bed with crumpled sheet, side table, cupboard, poster, mirror, bucket catching a leak
    wd=M('#6A4A30',.6,kind='wood')
    B.box((-1.6,1.3,.25),(1.2,1.0,.25),wd,.03); B.box((-1.6,1.3,.58),(1.15,.95,.1),M('#F4F1EA',.8,kind='fabric'),.05); B.box((-1.9,1.6,.72),(.45,.3,.1),M('#E8DCC6',.9,kind='fabric'),.06)
    B.box((-1.3,1.1,.72),(.7,.75,.06),M('#2B8A7A',.9,kind='fabric',h2='#F2C14E',sc=4),.05,rot=(0,0,R(8)))
    B.box((-2.95,2.5,.5),(.32,.25,.5),wd,.03); B.box((-1.6,2.6,1.1),(1.2,.12,.18),wd,.02)
    B.box((1.8,2.4,1.1),(.9,.38,1.1),M('#8A6A4A',.6,kind='wood'),.03); B.box((1.8,2.0,1.1),(.01,.01,1.0),M('#3A2A1E',.5),0)
    B.box((-3.31,-.8,1.8),(.02,.55,.75),M('#16171C',.7),.01); B.box((-3.3,-.8,1.8),(.02,.5,.7),M('#2B58C9',.7,h2='#F2C14E',sc=2),0)
    B.cyl((2.4,-1.6,.22),.25,.44,M('#2B58C9',.5),seg=14,r2=.3); B.cyl((2.4,-1.6,.4),.22,.02,M('#7FA8C0',.1,spec=1.0,alpha=.8),seg=14)
    B.box((2.4,-1.6,3.14),(.25,.25,.02),M('#7A8A7A',.9),0)  # damp patch
    B.box((-3.35,1.3,2.4),(.03,.4,.04),M('#C9CED8',.4),0)
    B.box((0,0,3.12),(.5,.5,.02),M('#FFFFFF',.3,emit=2.5),0)
    # outside: rain-dark buildings
    for k in range(6): B.box((8+k*1.5,-8+k*5,4),(2,2,6),M(['#8A8A88','#7A7E80','#9A948A'][k%3],.9,kind='wall'),0)
    B.box((12,0,-3),(10,30,1),M('#4E5A5A',.2,spec=.9),0)
def rain(center,n=220,area=(10,10),h=8,seed=1,speed=12):
    r=random.Random(seed); m=M('#C8D8E8',.2,emit=.4,alpha=.45); drops=[]
    for i in range(n):
        o=obox((0,0,0),(.008,.008,.18),m,0); x=center[0]+r.uniform(-area[0]/2,area[0]/2); y=center[1]+r.uniform(-area[1]/2,area[1]/2); ph=r.uniform(0,h)
        def fn(o,t,x=x,y=y,ph=ph): o.location=(x+.15*((ph+t*speed)%h)/h,y,h-((ph+t*speed)%h))
        fx.add(o,fn)
def ripples(center,n=18,area=(8,8),z=.33,seed=2):
    r=random.Random(seed); m=M('#C8D8E8',.2,emit=.3,alpha=.5)
    for i in range(n):
        o=ocyl((0,0,0),1.0,.004,m,None,rot=(0,0,0),seg=16); x=center[0]+r.uniform(-area[0]/2,area[0]/2); y=center[1]+r.uniform(-area[1]/2,area[1]/2); ph=r.uniform(0,1); per=r.uniform(.6,1.1)
        def fn(o,t,x=x,y=y,ph=ph,per=per):
            q=((t/per)+ph)%1; o.location=(x,y,z); k=.04+.3*q; o.scale=(k,k,1) if q<.95 else (0,0,0)
        fx.add(o,fn)
def phone_ui(kind,t0=0.0):
    """a giant phone in a black void at z=-200; returns dict with screen elements"""
    root=empty((0,0,-200)); ui=lambda c,e=1.2: M(c,.6,emit=e,spec=0)
    obox((0,.1,0),(1.25,.08,2.45),M('#16171C',.3,spec=.9),.18,root); obox((0,0,0),(1.12,.01,2.3),ui('#0E1A26',.8),.0,root)
    obox((0,-.02,2.15),(.25,.01,.04),ui('#000000',0),.02,root)
    text('9:41',(-.85,-.02,2.05),(0,-1,0),.12,ui('#FFFFFF',1.5),ex=0,parent=root)
    D={'root':root}
    if kind=='rain':
        nb=empty((0,-.03,1.2),root); obox((0,0,0),(1.0,.01,.38),ui('#F4F1EA',1.3),.08,nb); text('WEATHER ALERT',(-.35,-.02,.18),(0,-1,0),.11,ui('#C8372D',1.6),ex=0,parent=nb)
        text('Heavy rain expected today',(0,-.02,-.08),(0,-1,0),.13,ui('#16171C',.6),ex=0,parent=nb)
        for k in range(5): oico((-.6+k*.3,-.02,.3),.08,ui('#4D8FE8',1.4),root,sub=1,sc=(1,.3,1.3))
        text('KARACHI  32°',(0,-.02,-.2),(0,-1,0),.2,ui('#FFFFFF',1.4),ex=0,parent=root); D['nb']=nb
    if kind=='map':
        obox((0,-.015,0),(1.1,.005,2.2),ui('#E8E4D8',.9),.0,root)
        for (x,z,w,h,a) in ((0,.3,1.1,.06,0),(-.2,0,.06,2.2,0),(.4,-.6,.06,1.6,0),(0,-1.1,1.1,.05,0),(.2,.9,.8,.04,R(30))): obox((x,-.02,z),(w,.004,h),ui('#FFFFFF',1.2),0,root,rot=(0,a,0))
        obox((.6,-.02,1.4),(.35,.004,.3),ui('#A8D8A0',.9),0,root); obox((-.6,-.02,-.6),(.3,.004,.5),ui('#9FC8E8',.9),0,root)
        pin=empty((-.2,-.04,.3),root); ocyl((0,0,0),.11,.01,ui('#2B7FE8',2.5),pin,seg=20); ocyl((0,0,0),.2,.008,M('#2B7FE8',.6,emit=.8,alpha=.35),pin,seg=20); D['pin']=pin
        text('Daniyal  ·  0 m moved',(0,-.03,-1.85),(0,-1,0),.13,ui('#16171C',.5),ex=0,parent=root)
        obox((0,-.02,-1.85),(1.0,.004,.17),ui('#FFFFFF',1.2),.04,root)
        text('LIVE',(-.85,-.03,1.85),(0,-1,0),.1,ui('#C8372D',2),ex=0,parent=root)
    if kind=='call':
        oico((0,-.03,.8),.42,ui('#7A9A5A',1.0),root,sub=2,sc=(1,.2,1)); text('Z',(0,-.1,.72),(0,-1,0),.45,ui('#FFFFFF',1.6),ex=0,parent=root)
        text('Zain',(0,-.03,.05),(0,-1,0),.26,ui('#FFFFFF',1.6),ex=0,parent=root); text('Lahore',(0,-.03,-.25),(0,-1,0),.15,ui('#9FC8E8',1.4),ex=0,parent=root)
        for x,c in ((-.5,'#E8423A'),(.5,'#35C85A')): ocyl((x,-.03,-1.4),.2,.01,ui(c,2.2),root,seg=20)
        D['ring']=[ocyl((0,-.025,.8),.5,.004,M('#FFFFFF',.6,emit=1.2,alpha=.4),root,seg=24) for k in range(2)]
    return D
