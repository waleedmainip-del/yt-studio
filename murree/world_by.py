# sets for "Murree — Sab Ek Hi Din": motorway toll plaza + jam (x=0), snowy mountain road (x=100),
# Mall Road at night (x=200), hotel lobby (x=300), home rooftop with snow (x=400)
ASSET='/home/claude/murree/assets/'
_IMG={}
def img_mat(name,emit=1.0,clip=False):
    k=(name,emit,clip)
    if k in _IMG: return _IMG[k]
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']; tx=nt.nodes.new('ShaderNodeTexImage')
    tx.image=bpy.data.images.load(ASSET+'%s.png'%name,check_existing=True); tx.extension='CLIP'
    nt.links.new(tx.outputs['Color'],b.inputs['Base Color']); nt.links.new(tx.outputs['Color'],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=emit; b.inputs['Roughness'].default_value=.4
    if clip: nt.links.new(tx.outputs['Alpha'],b.inputs['Alpha']); m.blend_method='CLIP'
    _IMG[k]=m; return m
def img_plane(w,h,mat,loc=(0,0,0),rot=(0,0,0),parent=None):
    me=bpy.data.meshes.new('ip'); me.from_pydata([(-w/2,0,-h/2),(w/2,0,-h/2),(w/2,0,h/2),(-w/2,0,h/2)],[],[(0,1,2,3)]); uv=me.uv_layers.new(name='uv')
    for i,c in enumerate(((0,0),(1,0),(1,1),(0,1))): uv.data[i].uv=c
    me.update(); o=bpy.data.objects.new('ip',me); o.location=loc; o.rotation_euler=rot; _col.objects.link(o); me.materials.append(mat)
    if parent: o.parent=parent
    return o
def set_screen(o,name,emit=1.2): o.data.materials[0]=img_mat(name,emit)
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=False):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot
    try: a.data.use_shadow=shadow
    except Exception: pass
    return a
LEAF=[M('#3E8E4A',.7,kind='leaves'),M('#5FA84A',.7,kind='leaves'),M('#2F7A45',.7,kind='leaves'),M('#74B85A',.7,kind='leaves')]
SNOW=M('#F4F7FA',.55,kind='wall'); SNOW2=M('#E6EDF3',.6,kind='wall')
PINE=[M('#1F5A3C',.8,kind='leaves'),M('#2A6B47',.8,kind='leaves'),M('#174A32',.8,kind='leaves')]
def cone_(loc,r,h,mat,seg=8):
    B.cyl((loc[0],loc[1],loc[2]+h/2),r,h,mat,rot=(0,0,0),seg=seg,r2=0.0)
def tree(x,y,h=4.2,s=1.0,seed=0):
    r=random.Random(seed); B.cyl((x,y,h*.4),.13*s,h*.8,M('#6E5038',.85,kind='bark'),seg=10,rot=(0,0,0))
    for k in range(7): B.ico((x+r.uniform(-.9,.9)*s,y+r.uniform(-.9,.9)*s,h*.78+r.uniform(-.3,.7)*s),r.uniform(.7,1.1)*s,LEAF[k%4],sub=2)
def pine(x,y,h=6.0,snow=True,seed=0,z0=0.0):
    r=random.Random(seed); B.cyl((x,y,z0+h*.2),.16,h*.4,M('#5A4030',.85,kind='bark'),seg=8,rot=(0,0,0))
    for k in range(4):
        rr=(1.5-k*.32)*h/6; zz=z0+h*(.28+k*.18)
        cone_((x,y,zz),rr,h*.3,PINE[(k+seed)%3],seg=9)
        if snow: cone_((x,y,zz+h*.07),rr*.75,h*.17,SNOW,seg=9)
def plant(x,y,s=1.0,pot='#B5563A'):
    B.cyl((x,y,.22*s),.2*s,.44*s,M(pot,.8),seg=14,rot=(0,0,0))
    for j in range(6): B.ico((x+.16*s*math.cos(j*1.1),y+.16*s*math.sin(j*1.1),(.62+j*.07)*s),.19*s,LEAF[j%4],sub=1,sc=(1,1,.75))
# ---------------------------------------------------------------- vehicles
def car(x,y,col,rz=0,parent=None,roof=None):
    """traffic car (faces +x locally), wheels on the ground"""
    r=empty((x,y,0),rot=(0,0,R(rz)));
    if parent: r.parent=parent
    BODY=M(col,.25,metal=.4); GL=M('#22303E',.08,spec=.9); TIRE=M('#111216',.8); RIM=M('#B9C2CC',.3,metal=.8)
    obox((0,0,.62),(2.1,.92,.32),BODY,.08,r); obox((-.15,0,1.18),(1.25,.86,.28),BODY,.1,r); obox((-.15,0,1.18),(1.2,.88,.22),GL,.04,r)
    for sx in (-1.35,1.35):
        for sy in (-1,1): ocyl((sx,sy*.9,.34),.34,.2,TIRE,r,rot=(R(90),0,0),seg=16); ocyl((sx,sy*1.01,.34),.17,.02,RIM,r,rot=(R(90),0,0),seg=12)
    for sy in (-1,1): obox((2.11,sy*.6,.7),(.02,.18,.06),M('#FFF2C8',.3,emit=2),.01,r); obox((-2.11,sy*.6,.72),(.02,.18,.06),M('#E8303A',.3,emit=2.5),.01,r)
    if roof=='pateela':
        for sy in (-.55,.55): obox((-.15,sy,1.48),(1.0,.04,.03),M('#2B2C33',.4,metal=.6),.01,r)
        ocyl((-.3,0,1.68),.42,.42,M('#B9C2CC',.25,metal=.85),r,rot=(0,0,0),seg=20); ocyl((-.3,0,1.9),.44,.04,M('#9AA2AC',.25,metal=.85),r,rot=(0,0,0),seg=20)
        obox((.55,.1,1.62),(.3,.3,.14),M('#C8102E',.7,kind='fabric'),.05,r); obox((.5,-.4,1.6),(.25,.22,.12),M('#2F6FE0',.7,kind='fabric'),.05,r)
    if roof=='luggage':
        for k,(c,dx) in enumerate((('#6C3FA0',-.8),('#E8A33A',-.1),('#2E6B4A',.6))): obox((dx,0,1.62+.02*k),(.32,.5,.16),M(c,.7,kind='fabric'),.05,r)
        for sy in (-.55,.55): obox((-.15,sy,1.48),(1.0,.04,.03),M('#2B2C33',.4,metal=.6),.01,r)
    return r
HERO_COL='#F4F5FA'
def hero_car(x,y,rz=0,col=None,open_side=None):
    """Waleed's family car with a real interior: faces +y locally, right-hand drive. Returns dict of parts"""
    r=empty((x,y,0),rot=(0,0,R(rz)))
    BODY=M(col or HERO_COL,.22,metal=.35); TRIM=M('#2B2C33',.5); GL=M('#BFD8E8',.05,spec=.9,alpha=.18); SEAT=M('#4A3A32',.7,kind='fabric'); DASH=M('#2A2C33',.55)
    TIRE=M('#111216',.8); RIM=M('#C9CDD6',.3,metal=.8); IN=M('#CFC6B8',.8,kind='fabric')
    W,Lf,Lr=1.22,2.55,-2.45     # half width, front, rear
    obox((0,0,.12),(W-.04,2.35,.04),M('#3A3B42',.8),.01,r)                       # floor
    obox((0,(Lf+Lr)/2,.52),(W,(Lf-Lr)/2,.3),BODY,.08,r)                          # lower body (hip line .82)
    obox((0,Lf-.55,.86),(W,.55,.06),BODY,.06,r)                                   # bonnet top
    for s in (-1,1):
        obox((s*W,-.65,2.22),(.05,1.75,.06),BODY,.03,r)                            # roof rails sides
        for yy in (1.12,-.15,-2.38): obox((s*W,yy,1.55),(.05,.06,.72),BODY,.02,r)    # pillars
        if s!=open_side: obox((s*(W+.005),-.5,1.55),(.012,1.85,.62),GL,0,r)        # side glass
        obox((s*(W+.03),Lf-1.0,.65),(.02,.06,.03),M('#C9CDD6',.3,metal=.8),.005,r)
    obox((0,-.62,2.3),(W,1.82,.05),BODY,.04,r); obox((0,-.62,2.24),(W-.06,1.78,.01),IN,0,r)   # roof + headliner
    obox((0,1.32,1.55),(W-.04,.02,.72),GL,0,r,rot=(R(-12),0,0))                     # windscreen
    obox((0,-2.42,1.55),(W-.04,.02,.66),GL,0,r,rot=(R(6),0,0)); obox((0,Lr,.6),(W,.04,.3),BODY,.03,r)
    # dashboard, steering (right), gear, mirror, dangling tasbeeh
    obox((0,1.02,.95),(W-.06,.2,.12),DASH,.05,r); obox((0,.92,.86),(W-.08,.08,.06),DASH,.03,r)
    st=empty((.58,.82,1.0),r,rot=(R(62),0,0)); ocyl((0,0,0),.21,.035,M('#16171C',.4),st,seg=20); obox((0,0,0),(.2,.025,.015),M('#16171C',.4),.005,st); ocyl((0,0,-.12),.03,.24,DASH,st,seg=8)
    obox((0,1.15,2.12),(.14,.02,.05),M('#16171C',.4),.01,r); ocyl((0,1.14,1.9),.008,.4,M('#C9A24A',.3,metal=.6),r,rot=(0,0,0),seg=6)
    oico((0,1.14,1.7),.04,M('#2E6B4A',.4),r)
    # seats: driver (+x), passenger (-x), back bench
    for s in (-1,1):
        obox((s*.58,.12,.37),(.36,.34,.08),SEAT,.05,r); obox((s*.58,-.26,.95),(.36,.08,.52),SEAT,.06,r,rot=(R(-8),0,0))
    obox((0,-1.55,.37),(1.0,.36,.08),SEAT,.05,r); obox((0,-1.94,.95),(1.0,.08,.52),SEAT,.06,r,rot=(R(-6),0,0))
    for s in (-1,1): obox((s*(W-.03),-.5,.75),(.03,1.8,.25),IN,.01,r)           # door cards
    # wheels + lights + plate
    for yy in (1.6,-1.5):
        for s in (-1,1): ocyl((s*(W-.05),yy,.36),.36,.24,TIRE,r,rot=(0,R(90),0),seg=18); ocyl((s*(W+.07),yy,.36),.18,.02,RIM,r,rot=(0,R(90),0),seg=12)
    for s in (-1,1): obox((s*.75,Lf+.01,.62),(.2,.02,.07),M('#FFF2C8',.3,emit=2),.01,r); obox((s*.8,Lr-.03,.66),(.18,.02,.07),M('#E8303A',.3,emit=2.5),.01,r)
    img_plane(.6,.15,img_mat('plate',.4),(0,Lf+.03,.45),(0,0,R(180)),parent=r); img_plane(.6,.15,img_mat('plate',.4),(0,Lr-.06,.45),(0,0,0),parent=r)
    # luggage in the boot + roof bag
    obox((0,-.6,2.5),(.7,.9,.16),M('#2E6B4A',.7,kind='fabric'),.06,r)
    return dict(root=r,steer=st,seats=dict(drv=(.58,.12),pas=(-.58,.12),back=(0,-1.55)),seat_h=.45)
def seat_world(C,key):
    m=C['root'].matrix_world; lx,ly=C['seats'][key]; p=m@Vector((lx,ly,0)); return p
def donkey_cart(x,y,rz=0):
    r=empty((x,y,0),rot=(0,0,R(rz))); D_=M('#8A8580',.85,kind='fabric'); DK=M('#5A5550',.85)
    body=empty((1.6,0,0),r)
    obox((0,0,1.0),(.6,.24,.24),D_,.08,body); obox((.7,0,1.35),(.16,.13,.32),D_,.06,body,rot=(0,R(-30),0)); obox((.95,0,1.6),(.26,.14,.14),D_,.06,body)
    obox((1.15,0,1.56),(.08,.12,.09),M('#E8E2D6',.8),.04,body)
    for s in (-1,1):
        obox((.85,s*.08,1.86),(.04,.035,.16),D_,.02,body,rot=(R(s*12),0,0)); oico((1.02,s*.14,1.66),.03,M('#111216',.3),body)
    legs=[]
    for lx in (-.45,.45):
        for s in (-1,1): e=empty((lx,s*.15,.85),body); obox((0,0,-.42),(.07,.07,.42),D_,.03,e); obox((0,0,-.82),(.075,.075,.04),DK,.01,e); legs.append(e)
    obox((-.62,0,1.15),(.04,.04,.22),DK,.01,body,rot=(0,R(25),0))
    # cart: flat bed, two wheels, shafts
    obox((-.5,0,.85),(.9,.75,.05),M('#8C6A4A',.8,kind='wall'),.02,r);
    for s in (-1,1):
        ocyl((-.5,s*.82,.55),.55,.07,M('#5A4030',.8),r,rot=(R(90),0,0),seg=16); obox((.7,s*.32,.92),(.9,.03,.03),M('#5A4030',.8),.01,r)
        obox((-.5,s*.73,1.05),(.9,.03,.2),M('#8C6A4A',.8,kind='wall'),.01,r)
    for k,c in enumerate(('#F2C12E','#C8102E','#3E8E4A')): obox((-.9+k*.35,0,1.0),(.16,.3,.12),M(c,.7,kind='fabric'),.04,r)
    return dict(root=r,body=body,legs=legs)
def donkey_walk(D,t,speed=1.0):
    ph=t*6.5*speed
    for i,e in enumerate(D['legs']): e.rotation_euler[1]=R(22*math.sin(ph+(0 if i in (0,3) else pi)))
    D['body'].location[2]=.03*abs(math.sin(ph))
def monkey(x,y,z,rz=0,seed=0):
    r=empty((x,y,z),rot=(0,0,R(rz))); F=M('#8A6A4A',.85,kind='fabric'); FC=M('#E8B89A',.7)
    obox((0,0,.25),(.14,.11,.18),F,.06,r); obox((0,0,.55),(.13,.12,.12),F,.05,r); obox((0,-.11,.53),(.09,.02,.08),FC,.03,r)
    for s in (-1,1): oico((s*.06,-.13,.57),.02,M('#111216',.3),r); oico((s*.15,0,.6),.04,FC,r); obox((s*.16,-.05,.2),(.035,.035,.14),F,.02,r)
    ocyl((0,.14,.15),.02,.35,F,r,rot=(R(60),0,0),seg=6); return r
# ================================================================ MOTORWAY: toll plaza + jam (x=0), road runs along +y
LANES=[-5.4,-1.8,1.8,5.4]      # lane centres (x)
HERO_LANE=1.8; HERO_Y=-14.0
def motorway(jam=True,hero=True):
    B.box((0,0,-.05),(14,90,.05),M('#4C4B48',.85,kind='asphalt'),0)
    for xx in (-3.6,0,3.6):
        for k in range(-40,40,2): B.box((xx,k*2.0,.003),(.06,1.0,.003),M('#E8E2D6',.6),0)
    for s in (-1,1): B.box((s*7.3,0,.003),(.08,90,.003),M('#F2C12E',.5),0)
    B.box((-7.8,0,.35),(.15,90,.35),M('#B9B4AA',.7,kind='wall'),.02)
    B.box((7.8,-56,.35),(.15,35,.35),M('#B9B4AA',.7,kind='wall'),.02); B.box((7.8,46.5,.35),(.15,43.5,.35),M('#B9B4AA',.7,kind='wall'),.02)
    B.box((14,-12,-.02),(6,10,.02),M('#A89A80',.9),0)
    for s in (-1,1): B.box((s*20,0,-.03),(12,90,.03),M('#7FA05A',.9,kind='leaves'),0)
    # toll plaza canopy at y=20: pillars + roof + booths + barriers + big sign
    for xx in (-7.2,-3.6,0,3.6,7.2):
        B.box((xx,20,2.8),(.25,.25,2.8),M('#D8D2C4',.7),.02)
        if abs(xx)<7: B.box((xx,20,1.1),(.55,1.4,1.1),M('#E8E2D6',.6),.03); B.box((xx,19.0,1.5),(.5,.02,.35),M('#9FC8E0',.1,spec=.9),0)
    B.box((0,20,5.7),(8.2,2.6,.3),M('#2F6FE0',.5),.03); B.box((0,20,5.38),(8.0,2.5,.02),M('#F4F7FA',.3,emit=1.2),0)
    img_plane(9.0,1.3,img_mat('sign_toll',1.0),(0,17.36,5.7),(0,0,0))
    for xx in LANES: B.box((xx+.9,18.6,1.05),(.9,.03,.03),M('#E8303A',.5),.01)
    # hills + far mountains with snow, power pylons, billboards
    rnd=random.Random(4)
    for k in range(16):
        x=rnd.uniform(-90,90); y=rnd.uniform(110,170); h=rnd.uniform(25,55)
        cone_((x,y,-1),rnd.uniform(25,40),h,M(rnd.choice(['#5E7A6A','#6C8574','#57705F']),.95),seg=7)
        cone_((x,y,-1+h*.62),rnd.uniform(25,40)*.38*1.0,h*.38,SNOW,seg=7)
    for k in range(10): pine(rnd.choice((-1,1))*rnd.uniform(11,26),rnd.uniform(-60,80),rnd.uniform(5,8),snow=False,seed=k)
    img_plane(6,3,img_mat('bill_murree',.8),(-11,40,5.0),(0,0,R(15))); B.cyl((-11,40.2,1.8),.12,3.6,M('#5A5550',.6),rot=(0,0,0))
    cars=[]
    if jam:
        cols=['#C8102E','#2F4E8C','#E8E2D6','#2B2C33','#8E9AA6','#F2C12E','#2E6B4A','#B9C2CC','#6C3FA0','#C9A24A']; rnd=random.Random(9)
        for li,xx in enumerate(LANES):
            for k in range(14):
                yy=-70+k*6.2+(li*1.7)%3
                if abs(xx-HERO_LANE)<.1 and abs(yy-HERO_Y)<5.5: continue
                if abs(xx-5.4)<.1 and abs(yy-HERO_Y)<9: continue        # donkey / chai path
                if abs(xx+1.8)<.1 and abs(yy-HERO_Y)<4.6: continue       # Phupho's car slot
                if 15<yy<25: continue
                roof='luggage' if rnd.random()<.35 else None
                cars.append(car(xx,yy,rnd.choice(cols),90,roof=roof))
    return cars
DHABA=(11.2,-12.0)
def dhaba():
    x,y=DHABA
    B.box((x,y,0.0),(2.6,2.2,.06),M('#9C8E78',.9),.01)
    for s in (-1,1):
        for t_ in (-1,1): B.box((x+s*2.3,y+t_*1.9,1.35),(.07,.07,1.35),M('#5A4030',.8),.01)
    B.box((x,y,2.75),(2.6,2.2,.04),M('#C8102E',.7,kind='fabric'),.02)
    img_plane(3.0,.8,img_mat('sign_chai',.9),(x-2.62,y,2.4),(0,0,R(-90)))
    B.box((x-.9,y,.55),(.45,1.4,.55),M('#7A5236',.7,kind='wall'),.02); B.box((x-.9,y-.6,1.2),(.25,.25,.1),M('#2B2C33',.5,metal=.4),.02)
    B.cyl((x-.9,y-.6,1.4),.14,.3,M('#B9C2CC',.3,metal=.85),seg=14,rot=(0,0,0)); B.cyl((x-.9,y-.6,1.32),.18,.06,M('#FF8A30',.3,emit=4),seg=14,rot=(0,0,0))
    for k in range(5): B.cyl((x-.75-k*.06,y+.3+k*.12,1.15),.035,.08,M('#F4EBDD',.4),seg=10,rot=(0,0,0))
    for k in range(2): B.box((x+1.0,y-1.0+k*2.0,.25),(.25,.9,.06),M('#2F6FE0',.6),.02); B.box((x+1.0,y-1.0+k*2.0,.12),(.03,.85,.12),M('#2F6FE0',.6),0)
    B.box((x+1.9,y,.45),(.3,.6,.45),M('#5A6E8C',.6),.02)
# ================================================================ SNOWY MOUNTAIN ROAD (x=100), road along +y climbing
MX=100
def mountain_road():
    B.box((MX,0,-.05),(5,80,.05),M('#5E5C58',.8,kind='asphalt'),0)
    for k in range(-38,40,3): B.box((MX,k*2.0,.004),(.08,1.1,.003),M('#E8E2D6',.6),0)
    for s in (-1,1):
        B.box((MX+s*10,0,.15),(5,80,.2),SNOW,0);
        for k in range(-20,21): B.ico((MX+s*(5.6+random.Random(k).uniform(0,1.2)),k*4.0,.15),random.Random(k*7).uniform(.6,1.2),SNOW2,sub=2,sc=(1,1.6,.4))
        B.box((MX+s*5.05,0,.32),(.08,80,.32),M('#C9CDD6',.3,metal=.7),.01)
        for k in range(-26,27): B.box((MX+s*5.05,k*3.0,.25),(.05,.05,.25),M('#9AA2AC',.3,metal=.7),0)
    # slopes/mountains both sides with pines
    rnd=random.Random(21)
    for k in range(40):
        s=rnd.choice((-1,1)); x=MX+s*rnd.uniform(9,40); y=rnd.uniform(-70,90); pine(x,y,rnd.uniform(6,11),True,seed=k,z0=.3)
    for k in range(10):
        s=rnd.choice((-1,1)); cone_((MX+s*rnd.uniform(45,90),rnd.uniform(20,160),-1),rnd.uniform(25,40),rnd.uniform(30,60),SNOW2,seg=8)
    # roadside price boards for bhutta (50 / 100) and the bhutta cart near "Mall Road" sign
    for k,(yy,nm) in enumerate(((-20,'price_50'),(-4,'price_100'))):
        B.box((MX-5.9,yy,.9),(.05,.05,.9),M('#5A4030',.8),0); img_plane(1.1,.8,img_mat(nm,.6),(MX-5.9,yy-.06,1.9),(0,0,R(20)))
    BH=dict(x=MX-6.6,y=12.0)
    B.box((BH['x'],BH['y'],.7),(.7,.45,.06),M('#7A5236',.7,kind='wall'),.02)
    for s in (-1,1): ocyl((BH['x']+s*.5,BH['y']-.5,.3),.3,.06,M('#3A3B42',.8),None,rot=(R(90),0,0),seg=14)
    B.cyl((BH['x']+.15,BH['y'],.85),.35,.2,M('#2B2C33',.5,metal=.5),seg=16,rot=(0,0,0)); B.cyl((BH['x']+.15,BH['y'],.96),.3,.04,M('#FF6A20',.3,emit=6),seg=16,rot=(0,0,0))
    for k in range(6): obox((BH['x']+.0+k*.06,BH['y']-.1+(k%2)*.12,1.0),(.04,.13,.04),M('#F2C12E',.5),.03,rot=(0,R(90),R(k*20)))
    img_plane(1.2,.8,img_mat('price_300',.7),(BH['x']+.2,BH['y']-.52,1.55),(0,0,R(10)))
    B.box((BH['x']+.2,BH['y']-.5,1.15),(.04,.04,.4),M('#5A4030',.8),0)
    img_plane(2.4,.7,img_mat('sign_mall',.6),(MX-6.2,30,2.6),(0,0,R(10))); B.box((MX-6.2,30.1,1.2),(.06,.06,1.2),M('#5A4030',.8),0)
    # stuck cars further up + snow on cars
    for k,(xx,yy,c) in enumerate(((MX+2.2,24,'#C8102E'),(MX-2.2,30,'#2F4E8C'),(MX+2.2,36,'#E8E2D6'),(MX-2.2,42,'#2B2C33'),(MX+2.2,50,'#F2C12E'))):
        car(xx,yy,c,90+rnd.uniform(-8,8),roof=None); B.box((xx,yy,1.5),(1.0,.8,.08),SNOW,.05)
    area((MX,0,30),900,(40,80),(.9,.95,1.0))
    return BH
# ================================================================ MALL ROAD at night (x=200) street along +x at y=0
LX=200
def mall_road():
    B.box((LX,0,-.05),(30,8,.05),M('#8E8880',.7,kind='tile'),0)
    for k in range(-14,15): B.box((LX+k*2,0,.002),(.02,8,.002),M('#7A746C',.7),0)
    # shops on the north side, railing + valley view on the south side
    cols=['#7A2E3A','#2E4E7A','#5A3A7A','#2E6B4A','#8C5A2A','#3A5A6A']
    for k in range(8):
        x=LX-21+k*6; c=cols[k%6]
        B.box((x,6.5,3.5),(2.9,1.5,3.5),M('#E6DCC8' if k%2 else '#D8CDB8',.85,kind='wall'),.02)
        B.box((x,4.96,1.4),(2.4,.04,1.25),M('#FFE2A8',.2,emit=1.6),0); B.box((x,4.9,3.05),(2.8,.12,.4),M(c,.5),.02)
        img_plane(5.2,.7,img_mat('shop%d'%(k%6),1.3),(x,4.77,3.05),(0,0,0))
        for z in (4.6,6.0): B.box((x-1.2,4.98,z),(.5,.03,.45),M('#FFD58A',.2,emit=1.2),0); B.box((x+1.2,4.98,z),(.5,.03,.45),M('#FFD58A',.2,emit=1.2),0)
    for k in range(-14,15):     # string lights
        for j in range(5): B.ico((LX+k*2+j*.4,3.0+.5*math.sin(j*.8),5.2-.3*math.sin(pi*j/4)),.06,M('#FFE7B0',.2,emit=10),sub=1)
    for k in range(-30,31,2): B.box((LX+k,-5.0,.55),(.04,.04,.55),M('#2B2C33',.4,metal=.6),0)
    B.box((LX,-5.0,1.08),(30,.05,.04),M('#2B2C33',.4,metal=.6),0); B.box((LX,-5.0,.6),(30,.03,.02),M('#2B2C33',.4,metal=.6),0)
    for k in range(-6,7,2): B.cyl((LX+k*4,-4.5,2.2),.08,4.4,M('#2B2C33',.5,metal=.5),seg=8,rot=(0,0,0)); B.ico((LX+k*4,-4.5,4.5),.25,M('#FFF2C8',.2,emit=14),sub=2)
    # valley: dark hills with village lights
    rnd=random.Random(5)
    for k in range(14): cone_((LX+rnd.uniform(-60,60),rnd.uniform(-60,-30),-12),rnd.uniform(15,25),rnd.uniform(14,26),M('#1E2A3A',.95),seg=7)
    for k in range(80): B.box((LX+rnd.uniform(-70,70),rnd.uniform(-70,-28),rnd.uniform(-6,6)),(.15,.02,.12),M('#FFC879',.2,emit=4),0)
    for k in range(120):
        a=rnd.uniform(0,2*pi); e=rnd.uniform(.2,1.1); B.ico((LX+250*math.cos(a)*math.cos(e),250*math.sin(a)*math.cos(e)-60,250*math.sin(e)),rnd.uniform(.3,.6),M('#FFFFFF',.2,emit=5),sub=1)
    mk=[monkey(LX-2.5,-5.0,1.12,170,1),monkey(LX+.3,-5.0,1.12,200,2),monkey(LX+2.2,-5.0,1.12,160,3)]
    area((LX,0,7),900,(30,10),(1,.88,.7)); area((LX,-12,6),200,(30,6),(.5,.6,.95),rot=(R(60),0,0))
    return mk
# ================================================================ HOTEL LOBBY (x=300)
HX=300
def hotel():
    B.box((HX,0,-.05),(5,4,.05),M('#8C5A3A',.45,kind='wall',spec=.5),0)
    B.box((HX,0,.002),(2.4,1.6,.003),M('#7A1E2E',.9,kind='fabric'),0)
    W_=M('#E8DCC4',.85,kind='wall'); WD=M('#6E4A30',.5,kind='wall')
    B.box((HX,4,1.8),(5,.1,1.8),W_,0); B.box((HX-5,0,1.8),(.1,4,1.8),W_,0); B.box((HX+5,0,1.8),(.1,4,1.8),W_,0)
    for x in (HX-4.0,HX+4.0): B.box((x,3.88,.6),(.9,.02,.6),WD,0)
    # reception desk + rate board + bell + key board
    B.box((HX,1.6,.6),(1.8,.4,.6),WD,.03); B.box((HX,1.6,1.22),(1.85,.45,.03),M('#E8E2D6',.3,spec=.6),.01)
    B.cyl((HX-.9,1.4,1.27),.06,.04,M('#C9A24A',.25,metal=.9),seg=14,rot=(0,0,0)); B.ico((HX-.9,1.4,1.3),.05,M('#C9A24A',.25,metal=.9),sub=2,sc=(1,1,.6))
    img_plane(2.0,1.4,img_mat('rate_board',.9),(HX,3.88,2.3),(0,0,0))
    for k in range(12): B.box((HX+2.6+(k%4)*.25,3.88,1.8+(k//4)*.3),(.04,.02,.06),M('#C9A24A',.3,metal=.8),0)
    img_plane(1.6,.5,img_mat('sign_hotel',1.0),(HX-2.4,3.88,2.9),(0,0,0))
    # window to the side with pure fog outside
    B.box((HX-4.93,-.5,1.7),(.04,1.4,.9),M('#F4F6F8',.2,emit=1.6),0)
    for k in range(3): B.box((HX-4.9,-.5-1.4+k*1.4,1.7),(.05,.04,.92),WD,0)
    B.box((HX-4.9,-.5,.78),(.06,1.45,.04),WD,0); B.box((HX-4.9,-.5,2.62),(.06,1.45,.04),WD,0)
    # lounge chairs, plant, chandelier, heater
    for k in range(2): B.box((HX+3.0,-1.5+k*1.4,.35),(.4,.4,.15),M('#2E4E7A',.8,kind='fabric'),.06); B.box((HX+3.35,-1.5+k*1.4,.7),(.07,.4,.3),M('#2E4E7A',.8,kind='fabric'),.05)
    plant(HX+4.4,3.3,1.1,'#2B2C33'); plant(HX-4.4,3.3,1.0,'#2B2C33')
    B.ico((HX,.5,3.3),.3,M('#FFE7B0',.2,emit=6),sub=2);
    for k in range(6): B.ico((HX+.45*math.cos(k),.5+.45*math.sin(k),3.15),.08,M('#FFE7B0',.2,emit=5),sub=1)
    B.box((HX,0,3.65),(5,4,.05),M('#F4EBDD',.8),0)
    area((HX,0,3.4),300,(6,5),(1,.9,.78)); area((HX-4.6,-.5,1.7),140,(1.5,2),(.9,.95,1.0),rot=(0,R(90),0))
# ================================================================ HOME ROOFTOP in snow (x=400)
RX=400
def home_roof():
    B.box((RX,0,-.05),(5,4,.05),M('#9E978A',.9),0); B.box((RX,0,.03),(4.9,3.9,.03),SNOW,0)
    for s in (-1,1): B.box((RX+s*5,0,.55),(.12,4,.55),M('#E3D3B4',.85,kind='wall'),.01); B.box((RX,s*4,.55),(5,.12,.55),M('#E3D3B4',.85,kind='wall'),.01)
    for s in (-1,1): B.box((RX+s*5,0,1.13),(.16,4,.05),SNOW,.02); B.box((RX,s*4,1.13),(5,.16,.05),SNOW,.02)
    B.cyl((RX+3.4,2.6,.75),.6,1.5,M('#2C2C30',.5),seg=24,rot=(0,0,0)); B.cyl((RX+3.4,2.6,1.6),.62,.12,SNOW,seg=24,rot=(0,0,0))
    for k,c in enumerate(('#2F6FE0','#E8A33A')): B.box((RX-3.2+k*1.3,2.4,1.8),(.35,.01,.35),M(c,.85,kind='fabric'),.01)
    B.cyl((RX-4.6,2.4,1.9),.006,.0+9,M('#1A1B22',.5),seg=4,rot=(0,R(90),0))
    # snowman: 3 balls, Waleed's beanie, Abbu's muffler, carrot nose, coal eyes, stick arms
    sx,sy=RX+.4,.6
    B.ico((sx,sy,.45),.5,SNOW,sub=3); B.ico((sx,sy,1.15),.36,SNOW,sub=3); B.ico((sx,sy,1.66),.27,SNOW,sub=3)
    B.cyl((sx,sy,1.9),.24,.18,M('#2F6FE0',.8,kind='fabric'),seg=18,rot=(0,0,0)); B.ico((sx,sy,2.02),.07,M('#F4F5FA',.8,kind='fabric'),sub=2)
    B.cyl((sx,sy,1.42),.3,.1,M('#9E2B3A',.85,kind='fabric'),seg=18,rot=(0,0,0)); B.box((sx+.18,sy-.25,1.25),(.07,.03,.2),M('#9E2B3A',.85,kind='fabric'),.02)
    B.cyl((sx,sy-.38,1.66),.05,.22,M('#F08A24',.6),rot=(R(90),0,0),seg=10,r2=0.0)
    for s in (-1,1): B.ico((sx+s*.09,sy-.25,1.74),.03,M('#111216',.4),sub=1); B.box((sx+s*.48,sy,1.25),(.3,.02,.02),M('#5A4030',.8),0,rot=(0,R(s*-25),0))
    for k in range(3): B.ico((sx,sy-.36,1.1-k*.13),.03,M('#111216',.4),sub=1)
    # neighbourhood roofs under snow
    rnd=random.Random(8)
    for k in range(30):
        x=RX+rnd.uniform(-40,40); y=rnd.uniform(9,60); w=rnd.uniform(4,8); h=rnd.uniform(3,10)
        B.box((x,y,h/2-.5),(w/2,w/2,h/2),M(rnd.choice(['#D9C3A5','#C9B79C','#E4D4BC','#B49A80']),.9),0); B.box((x,y,h-.45),(w/2,w/2,.06),SNOW,0)
    for k in range(6): pine(RX+rnd.uniform(-30,30),rnd.uniform(12,40),rnd.uniform(5,8),True,seed=k)
    flakes=[]
    for k in range(90): flakes.append(oico((RX+rnd.uniform(-6,6),rnd.uniform(-6,5),rnd.uniform(0,5)),.025,SNOW))
    return dict(snowman=(sx,sy),flakes=flakes)
def snowfall(F,t,spd=.6):
    for i,f in enumerate(F):
        z0=(i*.37)%5; z=(z0-t*spd)%5; f.location[2]=z; f.location[0]+= .002*math.sin(t*2+i)
# ================================================================ props
def phone_obj(screen='ph_ammi'):
    e=empty((0,0,0)); obox((0,0,0),(.04,.007,.082),M('#15161A',.3),.006,e); sc=img_plane(.072,.148,img_mat(screen,1.2),(0,-.0075,0),(0,0,0),parent=e); return e,sc
def cup_obj():
    e=empty((0,0,0)); ocyl((0,0,0),.035,.08,M('#F4EBDD',.4),e,seg=10); ocyl((0,0,.035),.03,.01,M('#B5703A',.4),e,seg=10); return e
def plate_obj():
    e=empty((0,0,0)); ocyl((0,0,0),.16,.02,M('#F4F5FA',.3),e,seg=18); oico((0,0,.03),.11,M('#E0A040',.7),e,sc=(1,1,.35)); return e
def bhutta_obj():
    e=empty((0,0,0)); obox((0,0,0),(.035,.035,.13),M('#E8B830',.5),.03,e); obox((0,0,-.14),(.02,.02,.04),M('#7FA05A',.7),.01,e); return e
