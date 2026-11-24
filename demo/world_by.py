# sets for "Demo Ka Millionaire": Waleed's trading room (origin), house gate street (x=40),
# rooftop at night (x=40,y=-40), mobile shop street at night (x=-40), main road: Pizza Point + car showroom (x=80)
ASSET='/home/claude/demo/assets/'
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
    """quad in the XZ plane facing -y (w x h, centred)"""
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
def plant(x,y,s=1.0,pot='#B5563A'):
    B.cyl((x,y,.22*s),.2*s,.44*s,M(pot,.8),seg=14,rot=(0,0,0))
    for j in range(6): B.ico((x+.16*s*math.cos(j*1.1),y+.16*s*math.sin(j*1.1),(.62+j*.07)*s),.19*s,LEAF[j%4],sub=1,sc=(1,1,.75))
def tree(x,y,h=4.2,s=1.0,seed=0):
    r=random.Random(seed); B.cyl((x,y,h*.4),.13*s,h*.8,M('#6E5038',.85,kind='bark'),seg=10,rot=(0,0,0))
    for k in range(7): B.ico((x+r.uniform(-.9,.9)*s,y+r.uniform(-.9,.9)*s,h*.78+r.uniform(-.3,.7)*s),r.uniform(.7,1.1)*s,LEAF[k%4],sub=2)
WOODB=M('#5A3A26',.55,kind='wall')
def gaming_chair(x,y,rz):
    a=R(rz); c,s_=math.cos(a),math.sin(a)
    def P(dx,dy,z): return (x+dx*c-dy*s_,y+dx*s_+dy*c,z)
    BL=M('#1A1B22',.5); AC=M('#2F6FE0',.5)
    B.box(P(0,0,.5),(.28,.28,.06),BL,.05,rot=(0,0,a)); B.box(P(-.3,0,1.05),(.05,.27,.5),BL,.06,rot=(0,R(-8),a)); B.box(P(-.33,0,1.05),(.02,.1,.42),AC,.01,rot=(0,R(-8),a))
    B.cyl(P(0,0,.28),.04,.4,M('#888C96',.3,metal=.8),seg=8,rot=(0,0,0))
    for k in range(5): an=2*pi*k/5; B.box(P(.22*math.cos(an),.22*math.sin(an),.06),(.13,.025,.02),BL,.01,rot=(0,0,a+an))
    for sy in (-1,1): B.box(P(0,sy*.3,.72),(.2,.03,.03),BL,.01,rot=(0,0,a)); B.box(P(0,sy*.3,.62),(.02,.02,.1),BL,0,rot=(0,0,a))
# ================================================================ TRADING ROOM (origin)
RM=dict(x0=-3.0,x1=3.0,y0=-2.6,y1=2.6,h=3.3)
DESK=dict(x=2.55,y=0.2,top=.78)                 # desk on the east wall, Waleed faces +x
CHAIR=(1.72,0.2)
LAPTOP=(2.42,0.2)                                # laptop base centre on the desk
BEDR=dict(x0=-3.0,x1=-1.0,y0=.4,y1=2.5,top=.6)
def trading_room(mode='day'):
    """mode: day / night (screen + LED glow) / dark (power cut: everything off)"""
    x0,x1,y0,y1,h=RM['x0'],RM['x1'],RM['y0'],RM['y1'],RM['h']
    WALL=M('#55707E',.85,kind='wall'); WALL2=M('#E6E0D4',.85,kind='wall')
    B.box((0,0,-.05),(x1+.2,y1+.2,.05),M('#9AA0A6',.35,kind='wall',spec=.6),0)
    for i in range(-3,3):
        for j in range(-3,3): B.box((i+.5,j+.5,.002),(.495,.495,.002),M(['#C9CCCF','#BCC0C4'][(i+j)%2],.35,spec=.6),0)
    B.box((.2,-.6,.006),(1.3,.95,.004),M('#2A2F3A',.9,kind='fabric'),0); B.box((.2,-.6,.008),(1.15,.8,.004),M('#3C4658',.9,kind='fabric'),0)
    B.box((0,y1,h/2),(x1,.1,h/2),WALL2,0); B.box((x0,0,h/2),(.1,y1,h/2),WALL,0); B.box((x1,0,h/2),(.1,y1,h/2),WALL,0)
    B.box(((x0+1.42)/2,y0,h/2),((1.42-x0)/2,.1,h/2),WALL2,0); B.box(((2.58+x1)/2,y0,h/2),((x1-2.58)/2,.1,h/2),WALL2,0); B.box((2.0,y0,2.95),(.56,.1,.35),WALL2,0)
    B.box((0,0,h+.05),(x1,y1,.05),M('#EDE9E2',.8,kind='wall'),0)
    for (cx,cy,sx,sy) in ((0,y1-.12,x1,.02),(x0+.12,0,.02,y1),(x1-.12,0,.02,y1)): B.box((cx,cy,.07),(sx,sy,.07),M('#2B2F36',.5),.01)
    # window north wall (x -.2..1.2) with blinds; outside: sky
    wx=.5; dark=(mode!='day')
    B.box((wx,y1-.06,1.85),(.72,.03,.62),M('#F4F1EA',.5),.01)
    B.box((wx,y1-.07,1.85),(.65,.02,.55),M('#1B2440' if dark else '#BFE3F5',.1,emit=(.25 if dark else 2.0)),0)
    for k in range(9): B.box((wx,y1-.12,1.38+k*.11),(.66,.012,.022),M('#E8E2D6',.6),0,rot=(R(-20),0,0))
    # BED (west, head to west wall) with grey sheet
    bx0,bx1,by0,by1,top=BEDR['x0'],BEDR['x1'],BEDR['y0'],BEDR['y1'],BEDR['top']; cx=(bx0+bx1)/2; cy=(by0+by1)/2
    B.box((cx,cy,.16),((bx1-bx0)/2,(by1-by0)/2,.16),M('#2B2F36',.5),.02); B.box((bx0+.06,cy,.72),(.06,(by1-by0)/2,.72),M('#2B2F36',.5),.03)
    B.box((cx,cy,.46),((bx1-bx0)/2-.04,(by1-by0)/2-.04,.14),M('#D8DDE3',.85,kind='fabric'),.06)
    B.box((cx+.2,cy,.62),((bx1-bx0)/2-.25,(by1-by0)/2-.02,.04),M('#3C4658',.85,kind='fabric'),.04)
    B.box((bx0+.4,cy,top+.04),(.24,.55,.06),M('#F4F1EA',.8,kind='fabric'),.05)
    # DESK (east wall): L-top, laptop, 2nd monitor with chart, router shelf, LED strip
    dx,dy,dt=DESK['x'],DESK['y'],DESK['top']
    B.box((dx,dy,dt-.03),(.4,1.05,.03),M('#E8E2D6',.4),.01)
    for yy in (dy-1.0,dy+1.0):
        for xx in (dx-.33,dx+.33): B.box((xx,yy,(dt-.06)/2),(.025,.025,(dt-.06)/2),M('#1A1B22',.4,metal=.5),.005)
    # second monitor (big chart) at the back, left of the laptop
    B.box((dx+.22,dy+.62,dt+.02),(.1,.14,.02),M('#1A1B22',.4),.01); B.box((dx+.25,dy+.62,dt+.2),(.025,.025,.18),M('#1A1B22',.4),.01)
    B.box((dx+.23,dy+.62,dt+.55),(.025,.46,.27),M('#111216',.3),.02)
    MON=img_plane(.86,.48,img_mat('lap_demo',.9),(dx+.2,dy+.62,dt+.55),(0,0,R(-90)))
    # laptop (base + hinged screen facing -x)
    lx,ly=LAPTOP; B.box((lx,ly,dt+.012),(.17,.24,.012),M('#B9BEC6',.3,metal=.7),.006); B.box((lx-.02,ly,dt+.026),(.12,.2,.002),M('#22242B',.5),0)
    lid=empty((lx+.16,ly,dt+.024),rot=(0,R(12),0)); obox((0,0,.16),(.008,.24,.16),M('#B9BEC6',.3,metal=.7),.006,lid)
    LAP=img_plane(.44,.27,img_mat('lap_demo',1.0),(-.011,0,.165),(0,0,R(-90)),parent=lid)
    # router + LEDs on a shelf above desk, LED strip under the shelf
    B.box((x1-.18,dy-.55,1.7),(.16,.5,.02),M('#E8E2D6',.4),.01)
    B.box((x1-.2,dy-.75,1.76),(.08,.13,.04),M('#F4F5FA',.3),.02)
    for k in range(2): B.cyl((x1-.24,dy-.84+k*.18,1.86),.008,.16,M('#F4F5FA',.3),seg=6,rot=(0,0,0))
    LEDS=[]
    for k in range(4): LEDS.append(obox((x1-.285,dy-.82+k*.045,1.77),(.004,.01,.006),M('#38E07A',.2,emit=6),0))
    for k in range(3): B.box((x1-.2,dy-.35+k*.12,1.8),(.07,.04,.08),M(['#2F6FE0','#E8505B','#F2C12E'][k],.5),.01)  # books
    STRIP=obox((x1-.19,dy-.55,1.675),(.01,.48,.006),M('#9B5CFF',.2,emit=(5 if mode=='night' else (1.5 if mode=='day' else 0))),0)
    # props on desk: Eidi envelope, bike-fund jar, mug, phone stand, mouse
    B.box((dx-.12,dy-.55,dt+.01),(.09,.06,.006),M('#16A34A',.5),.004,rot=(0,0,R(15)))
    img_plane(.16,.1,img_mat('lbl_eidi',.4),(dx-.12,dy-.55,dt+.0175),(R(90),0,R(105)))
    JAR=dict(x=dx-.05,y=dy-.82); B.cyl((JAR['x'],JAR['y'],dt+.1),.07,.2,M('#BFE3F5',.05,spec=.9,alpha=.35),seg=16,rot=(0,0,0)); B.cyl((JAR['x'],JAR['y'],dt+.21),.06,.02,M('#C9A24A',.3,metal=.7),seg=16,rot=(0,0,0))
    img_plane(.1,.05,img_mat('lbl_bike',.4),(JAR['x']-.072,JAR['y'],dt+.1),(0,0,R(-90)))
    B.cyl((dx-.15,dy+.4,dt+.05),.04,.1,M('#F4F1EA',.3),seg=12,rot=(0,0,0)); B.box((dx-.12,dy-.22,dt+.012),(.04,.025,.012),M('#22242B',.4),.01)
    # posters + wall clock
    img_plane(.6,.84,img_mat('poster_trader',.25),(x0+.11,-.9,1.95),(0,0,R(-90)))
    img_plane(.84,.6,img_mat('poster_lambo',.25),(-1.6,y1-.11,2.05),(0,0,0))
    # wardrobe south wall west
    B.box((-2.0,y0+.33,1.2),(.85,.28,1.2),WOODB,.02); B.box((-2.0,y0+.05,1.2),(.02,.01,1.15),M('#2A1A10',.6),0)
    for s in (-1,1): B.box((-2.0+s*.08,y0+.02,1.2),(.015,.02,.12),M('#C9CDD6',.2,metal=.9),0)
    plant(2.6,y1-.45,1.0,'#2B2F36')
    # door (south wall, x 1.42..2.58) hinged, hallway behind
    for s_ in (-1,1): B.box((2.0+s_*.58,y0,1.3),(.04,.13,1.3),M('#3A2A1E',.5,kind='wall'),.005)
    B.box((2.0,y0,2.62),(.62,.13,.04),M('#3A2A1E',.5,kind='wall'),.005)
    hinge=empty((1.46,y0+.02,0)); obox((.54,0,1.3),(.53,.03,1.28),M('#7A5236',.5,kind='wall'),.01,hinge); obox((.98,.05,1.15),(.03,.03,.06),M('#C9CDD6',.2,metal=.9),.005,hinge); obox((.98,-.05,1.15),(.03,.03,.06),M('#C9CDD6',.2,metal=.9),.005,hinge)
    B.box((2.0,y0-1.0,-.05),(1.6,1.0,.05),M('#C9C0B0',.6,kind='wall'),0); B.box((2.0,y0-2.0,1.7),(1.6,.1,1.7),M('#E8DCC4',.85,kind='wall'),0)
    for s_ in (-1,1): B.box((2.0+s_*1.55,y0-1.0,1.7),(.1,1.0,1.7),M('#E8DCC4',.85,kind='wall'),0)
    B.box((2.0,y0-1.0,3.35),(1.6,1.0,.05),M('#F4F1EA',.8),0)
    # ceiling light panel + fan
    PANEL=obox((0,0,h-.02),(.45,.45,.015),M('#FFF8EC',.3,emit=(1.2 if mode=='day' else (.6 if mode=='night' else 0))),.01)
    fan=empty((-.6,.4,h-.25)); B.cyl((-.6,.4,h-.1),.03,.2,M('#F4F1EA',.5),seg=8,rot=(0,0,0)); B.cyl((-.6,.4,h-.25),.12,.1,M('#F4F1EA',.5),seg=14,rot=(0,0,0))
    for k in range(3): obox((math.cos(2*pi*k/3)*.48,math.sin(2*pi*k/3)*.48,0),(.48,.07,.008),M('#F4F1EA',.5),.01,fan,rot=(0,0,2*pi*k/3))
    L_={}
    if mode=='day':
        L_['a']=area((0,0,h-.2),90,(4,4),(1,.95,.88)); area((wx,y1-.4,1.85),110,(1.3,1.1),(1,.96,.88),rot=(R(-90),0,0)); area((2.0,y0-1.0,3.1),40,(2,1.6),(1,.95,.85))
    elif mode=='night':
        L_['a']=area((0,0,h-.2),40,(3,3),(.55,.62,1.0)); area((-1.5,-1.2,2.6),25,(2,2),(1,.8,.6)); L_['scr']=area((dx-.45,dy,1.25),55,(.6,.8),(.6,.75,1.0),rot=(0,R(-90),0)); point((x1-.3,dy-.55,1.55),12,(.7,.4,1.0),.3,shadow=False)
        area((2.0,y0-1.0,3.1),12,(2,1.6),(1,.85,.65))
    else:
        L_['a']=area((0,0,h-.2),6,(3,3),(.35,.42,.7)); L_['scr']=area((dx-.45,dy,1.25),30,(.5,.6),(.6,.75,1.0),rot=(0,R(-90),0))
    return dict(fan=fan,door=hinge,lap=LAP,lid=lid,mon=MON,leds=LEDS,strip=STRIP,panel=PANEL,L=L_)
def door_set(D,k): D['door'].rotation_euler[2]=R(92*ease(k))
# ================================================================ HOUSE GATE STREET (x=40), evening
GX=40
def gate_street():
    """Waleed's gate faces -y. gate opening x=GX-1..GX+1 at y=0. street y<0"""
    B.box((GX,-4,-.05),(14,6,.05),M('#77736C',.85,kind='asphalt'),0); B.box((GX,-.9,.07),(14,.9,.07),M('#B5AE9F',.8,kind='wall'),.01)
    for k in range(-6,7): B.box((GX+k*2,-4.6,.003),(.5,.05,.003),M('#E8E2D6',.6),0)
    WALLC=M('#E3D3B4',.85,kind='wall'); TOPC=M('#B98A5A',.7)
    for s in (-1,1):
        B.box((GX+s*4.6,.15,1.0),(3.6,.15,1.0),WALLC,.01); B.box((GX+s*4.6,.15,2.05),(3.65,.2,.05),TOPC,.01)
        B.box((GX+s*1.15,.15,1.25),(.18,.2,1.25),M('#D2BE98',.8,kind='wall'),.01); B.box((GX+s*1.15,.15,2.55),(.24,.26,.06),TOPC,.01)
        B.ico((GX+s*1.15,.15,2.7),.12,M('#FFE2A8',.2,emit=4),sub=2)
    # metal gate: two leaves, one open
    GT=M('#2F3A48',.4,metal=.7)
    for k,(x,rz) in enumerate(((GX-.5,0),(GX+.94,R(-70)))):
        g=empty((x if k==0 else GX+.96,.12,0),rot=(0,0,rz))
        ox=0 if k==0 else -.46
        obox((ox,0,1.0),(.46,.03,.95),GT,.01,g)
        for j in range(6): obox((ox-.38+j*.15,-.035,1.05),(.015,.01,.8),M('#C9A24A',.3,metal=.8),0,g)
    img_plane(.5,.18,img_mat('lbl_house',.5) if os.path.exists(ASSET+'lbl_house.png') else M('#F4F1EA',.5),(GX+1.15,-.07,1.75),(0,0,0))
    # house behind: two storeys, balcony, windows lit
    B.box((GX,8.0,3.2),(6,5.8,3.2),M('#EFE4CF',.85,kind='wall'),.02); B.box((GX,2.25,6.45),(6.1,.25,.08),TOPC,.01); B.box((GX,1.2,.03),(5.8,1.0,.03),M('#C9B8A0',.5,kind='tile'),0)
    for k,(x,z) in enumerate(((GX-3.5,1.6),(GX+3.5,1.6),(GX-3.5,4.6),(GX,4.6),(GX+3.5,4.6))):
        B.box((x,2.17,z),(.6,.03,.55),M('#F7E2B0',.2,emit=1.4 if k%2 else .9),0); B.box((x,2.19,z),(.7,.04,.62),M('#6E4A30',.5),.01)
    B.box((GX,2.17,1.3),(.55,.02,1.15),M('#6E4A30',.5),.01)   # front door
    B.box((GX,1.6,3.3),(2.4,.6,.06),M('#D2BE98',.8,kind='wall'),.01); B.box((GX,1.02,3.6),(2.4,.03,.3),GT,.01)
    plant(GX-2.4,.9,1.1); plant(GX+2.6,.9,.9,'#8C4A30'); tree(GX-4.2,1.3,3.6,.8,9)
    # neighbour houses + street lamp + parked car + electric poles
    for s in (-1,1):
        B.box((GX+s*12,5.0,3.0),(4,4.6,3.0),M(['#D9C3A5','#C9D6D2'][s>0],.85,kind='wall'),.02)
        for z in (1.6,4.4): B.box((GX+s*12,.38,z),(.6,.03,.5),M('#F7E2B0',.2,emit=1.1),0)
    B.cyl((GX-5.5,-1.6,2.4),.07,4.8,M('#5A5550',.6),seg=8,rot=(0,0,0)); B.box((GX-5.1,-1.9,4.75),(.45,.12,.06),M('#5A5550',.6),.02); B.box((GX-4.75,-1.9,4.68),(.14,.1,.03),M('#FFE7B8',.2,emit=8),.01)
    for k in range(2): B.box((GX-5.5+k*.01,-1.0,4.6-k*.25),(9,.008,.008),M('#1A1B22',.5),0)
    tree(GX+7,-1.2,4.4,1.0,3); tree(GX-8.5,-1.0,4.0,.9,5)
    car_parked(GX+6.2,-3.0,'#8E9AA6',0)
    area((GX,-4,7),180,(14,8),(1,.78,.6),rot=(R(28),0,0)); point((GX-4.75,-1.95,4.4),180,(1,.85,.6),.3)
    for s in (-1,1): point((GX+s*1.15,-.2,2.6),25,(1,.85,.6),.15,shadow=False)
def car_parked(x,y,col,rz=0):
    r=empty((x,y,0),rot=(0,0,R(rz))); BODY=M(col,.25,metal=.4); GL=M('#22303E',.05,spec=1.0); TIRE=M('#111216',.8); RIM=M('#B9C2CC',.3,metal=.8)
    obox((0,0,.6),(2.1,.88,.3),BODY,.08,r); obox((-.15,0,1.12),(1.2,.82,.26),BODY,.1,r); obox((-.15,0,1.12),(1.15,.84,.2),GL,.04,r)
    for sx in (-1.35,1.35):
        for sy in (-1,1): ocyl((sx,sy*.86,.33),.33,.2,TIRE,r,rot=(R(90),0,0),seg=16); ocyl((sx,sy*.97,.33),.17,.02,RIM,r,rot=(R(90),0,0),seg=12)
    for sy in (-1,1): obox((2.11,sy*.6,.68),(.02,.18,.06),M('#FFF2C8',.3,emit=2),.01,r); obox((-2.11,sy*.6,.7),(.02,.18,.06),M('#E8303A',.3,emit=2),.01,r)
    return r
def bike(x,y,rz=0,col='#C8102E',box=True):
    """delivery motorbike, wheels on the ground (r .32), faces +x locally"""
    r=empty((x,y,0),rot=(0,0,R(rz))); C_=M(col,.3,metal=.4); BL=M('#1B1B20',.7)
    for sx in (-.62,.62): ocyl((sx,0,.32),.32,.09,M('#111216',.8),r,rot=(R(90),0,0),seg=18); ocyl((sx,0,.32),.16,.1,M('#C9CDD6',.3,metal=.9),r,rot=(R(90),0,0),seg=10)
    obox((0,0,.62),(.42,.12,.16),C_,.05,r); obox((-.22,0,.8),(.34,.13,.05),BL,.03,r); obox((.5,0,.72),(.08,.06,.32),M('#3A3B45',.4,metal=.6),.02,r,rot=(0,R(-20),0))
    obox((.58,0,1.02),(.04,.36,.025),M('#C9CDD6',.3,metal=.8),.01,r); obox((.66,0,.86),(.06,.09,.1),M('#FFF2C8',.3,emit=2),.02,r); obox((-.62,0,.45),(.12,.1,.04),M('#3A3B45',.4,metal=.6),.01,r)
    if box:
        obox((-.62,0,1.12),(.26,.24,.24),M(col,.5),.03,r); img_plane(.4,.1,img_mat('sign_pizza',.6),(-.62,-.245,1.15),(0,0,0),parent=r)
    return r
# ================================================================ ROOFTOP at night, load shedding (x=40,y=-40)
RX,RY=40,-40
def rooftop():
    B.box((RX,RY,-.05),(6,5,.05),M('#8E877C',.92),0)
    WALL=M('#B9AE9E',.85)
    for s in (-1,1): B.box((RX+s*6,RY,.5),(.12,5,.5),WALL,.01); B.box((RX,RY+s*5,.5),(6,.12,.5),WALL,.01)
    # stair room (door to the stairs) at the back left, door open with faint light
    B.box((RX-3.6,RY+3.6,1.3),(1.4,1.2,1.3),M('#C9BDA8',.85),.02); B.box((RX-3.6,RY+2.38,1.05),(.45,.03,1.0),M('#1A1612',.8),0)
    B.box((RX-3.6,RY+2.36,1.05),(.38,.02,.9),M('#FFB46A',.2,emit=.15),0)
    B.cyl((RX+3.4,RY+3.3,.75),.62,1.5,M('#2C2C30',.5),seg=24,rot=(0,0,0)); B.cyl((RX+3.4,RY+3.3,1.55),.64,.1,M('#2C2C30',.5),seg=24,rot=(0,0,0))
    B.cyl((RX-4.6,RY-2.8,1.0),.03,2.0,M('#9A9A9A',.4,metal=.6),seg=8,rot=(0,0,0)); B.ico((RX-4.6,RY-2.95,1.85),.4,M('#D8D8D8',.4),sc=(1,.35,1))
    for k in range(5): B.cyl((RX-5.5+k*.01,RY+1.0-k*.5,2.2),.006,11,M('#1A1B22',.5),seg=4,rot=(0,R(90),0))   # clothes line wire
    for k,col in enumerate(('#C8102E','#2F6FE0','#F2C12E')): B.box((RX-2+k*1.2,RY+1.0,1.9),(.3,.01,.32),M(col,.85,kind='fabric'),.01)
    plant(RX+4.8,RY-3.8,1.0); B.box((RX+1.5,RY-3.9,.25),(.6,.4,.25),M('#5A6E8C',.6),.02)
    # dark neighbourhood: blocky roofs, only a few UPS-lit windows, a far lit area with generator, stars + moon
    rnd=random.Random(11)
    for k in range(70):
        x=RX+rnd.uniform(-60,60); y=RY+rnd.uniform(12,90); w=rnd.uniform(4,9); h=rnd.uniform(3,14)
        if abs(x-RX)<8 and y<RY+16: continue
        B.box((x,y,h/2-.5),(w/2,w/2,h/2),M(rnd.choice(['#3A3F4C','#343844','#2E323C','#40444F']),.9),0)
        if rnd.random()<.28: B.box((x+rnd.uniform(-w/3,w/3),y-w/2-.02,h*rnd.uniform(.3,.8)),(.35,.02,.3),M('#FFC879',.2,emit=rnd.uniform(1.5,3)),0)
    for k in range(40):   # far bright district (has power)
        x=RX+rnd.uniform(25,70); y=RY+rnd.uniform(70,120); B.box((x,y,rnd.uniform(1,6)),(.4,.02,.3),M('#FFE2B0',.2,emit=4),0)
    for k in range(160):
        a=rnd.uniform(0,2*pi); e=rnd.uniform(.25,1.2); d_=300
        B.ico((RX+d_*math.cos(a)*math.cos(e),RY+d_*math.sin(a)*math.cos(e)+60,d_*math.sin(e)),rnd.uniform(.3,.7),M('#FFFFFF',.2,emit=rnd.uniform(3,8)),sub=1)
    B.ico((RX-40,RY+180,90),7,M('#F4F1E6',.2,emit=3),sub=3)
    area((RX-10,RY+40,40),3000,(30,30),(.45,.55,.9),rot=(R(-40),0,R(180)))
    area((RX,RY,8),420,(12,10),(.55,.62,.95)); area((RX,RY-9,5),160,(10,4),(.5,.58,.9),rot=(R(60),0,0))
# ================================================================ MOBILE SHOP STREET, night (x=-40)
SX=-40
SHOP=dict(x=SX,y=2.0)        # counter front at y=1.25; shopkeeper behind (y~2.0), customer in front (y~.5)
def shop_street():
    B.box((SX,-1,-.05),(14,7,.05),M('#6E6A64',.85,kind='asphalt'),0); B.box((SX,1.0,.06),(14,.9,.06),M('#9C968A',.8,kind='wall'),.01)
    # the lit mobile shop: open front, counter, glass display, shelves, tube light (UPS), posters
    x,y=SHOP['x'],SHOP['y']
    B.box((x,y+1.55,1.6),(1.9,.1,1.6),M('#E7EEF2',.8,kind='wall'),0)
    for s in (-1,1): B.box((x+s*1.95,y+.4,1.6),(.1,1.25,1.6),M('#D8D2C4',.8,kind='wall'),0)
    B.box((x,y+.4,3.25),(2.05,1.3,.06),M('#BFB8AA',.8),0); B.box((x,y+.4,0),(1.9,1.25,.02),M('#D6D9DC',.4,spec=.6),0)
    img_plane(3.6,.9,img_mat('sign_mobile',1.4),(x,y-.88,3.65),(0,0,0)); B.box((x,y-.84,3.65),(1.85,.04,.5),M('#22242B',.5),.01)
    # counter with glass top + phones inside
    B.box((x,y-.75,.5),(1.4,.3,.5),M('#2B3A55',.5),.02); B.box((x,y-.75,1.02),(1.42,.32,.02),M('#CFE8F5',.05,spec=.9,alpha=.35),0)
    for k in range(8): B.box((x-1.15+k*.33,y-.75,.92),(.05,.09,.006),M('#111216',.3),.004); B.box((x-1.15+k*.33,y-.756,.926),(.042,.078,.002),M(['#7FD3FF','#F2C12E','#9BE07A','#F48FB1'][k%4],.3,emit=.8),0)
    # shelves with boxes / scratch cards
    for z in (1.2,1.7,2.2):
        B.box((x,y+1.35,z),(1.7,.18,.02),M('#E8E2D6',.5),.01)
        for k in range(12): B.box((x-1.55+k*.28,y+1.32,z+.1),(.1,.08,.09),M(['#C8102E','#1D3E8A','#16A34A','#F2C12E','#7A4EC2'][k%5],.5),.01)
    img_plane(.6,.8,img_mat('sign_pkg',.7),(x+1.2,y+1.43,2.75),(0,0,0)); img_plane(.6,.8,img_mat('sign_pkg',.7),(x-1.84,y+.6,2.0),(0,0,R(-90)))
    TUBE=obox((x,y+.2,3.15),(1.0,.04,.03),M('#F4FAFF',.2,emit=9),.01)
    B.box((x+1.6,y+1.2,.3),(.25,.2,.3),M('#22242B',.5),.02); B.box((x+1.6,y+1.0,.45),(.08,.01,.04),M('#38E07A',.2,emit=5),0)   # UPS
    # neighbouring shops: shutters down (load shedding)
    for k,s in enumerate((-1,1)):
        for j in range(2):
            xx=x+s*(4.2+j*4.0); B.box((xx,y+.4,1.7),(1.9,1.3,1.7),M(['#D9C3A5','#C9B79C','#CDBBA2','#B49A80'][k*2+j],.85,kind='wall'),.01)
            B.box((xx,y-.92,1.3),(1.6,.04,1.2),M('#7A808A',.4,metal=.6),.01)
            for q in range(14): B.box((xx,y-.97,.15+q*.17),(1.58,.008,.008),M('#5A606A',.4,metal=.6),0)
            B.box((xx,y-.95,2.8),(1.7,.05,.3),M(['#5A6E8C','#8C4A30','#2E6B4A','#6C5FB0'][k*2+j],.5),.01)
    # street: dark lamp pole, parked bike, wires, a stray chair, distant houses (dark)
    B.cyl((x-2.6,.6,2.4),.07,4.8,M('#5A5550',.6),seg=8,rot=(0,0,0))
    for k in range(3): B.box((x,.6-k*.01,4.5-k*.2),(12,.008,.008),M('#1A1B22',.5),0)
    bike(x+3.0,-.5,180,'#2F3A48',box=False)
    B.box((x,-8,2.5),(14,.5,3),M('#2E323C',.9),0)
    for k in range(5): B.box((x-10+k*5,-7.48,1.5+(k%2)),(.4,.02,.3),M('#FFC879',.2,emit=2),0)
    # night sky dome light, the shop's own lights
    area((x,y-.2,3.0),260,(3.2,1.6),(.92,.97,1.0)); area((x,-3,5),40,(10,6),(.4,.5,.85))
    point((x,y-1.6,2.2),60,(.9,.95,1.0),.4,shadow=False)
    return dict(tube=TUBE)
# ================================================================ MAIN ROAD: Pizza Point + Prestige Motors (x=80), afternoon
PX=80
PIZ=dict(x=PX,y=2.0)          # pizza shop front glass at y=1.0, door at x=PX+1.2
SHW=dict(x=PX+9.0,y=2.4)      # showroom glass front at y=1.0
def lambo(x,y,rz=0,col='#F2C12E'):
    r=empty((x,y,0),rot=(0,0,R(rz))); BODY=M(col,.18,metal=.5,spec=.9); GL=M('#10161E',.25,spec=.4); TIRE=M('#111216',.8); RIM=M('#2B2C33',.25,metal=.9)
    # low wedge body
    obox((0,0,.48),(2.15,.98,.22),BODY,.06,r); obox((1.6,0,.42),(.6,.96,.12),BODY,.06,r,rot=(0,R(8),0)); obox((-.1,0,.78),(1.15,.86,.14),BODY,.08,r,rot=(0,R(-3),0))
    obox((.2,0,.88),(.75,.8,.12),GL,.06,r,rot=(0,R(-14),0)); obox((-.75,0,.86),(.5,.78,.1),GL,.05,r,rot=(0,R(10),0))
    obox((-2.1,0,.86),(.12,.98,.03),BODY,.01,r)
    for sy in (-1,1):
        obox((2.12,sy*.62,.46),(.03,.24,.035),M('#FFF8E0',.2,emit=4),.005,r,rot=(0,0,R(sy*10))); obox((-2.16,sy*.6,.55),(.02,.3,.04),M('#E8303A',.2,emit=3),.005,r)
        obox((0.4,sy*.99,.45),(.5,.01,.1),M('#111216',.4),.01,r)
    for sx in (-1.35,1.4):
        for sy in (-1,1): ocyl((sx,sy*.9,.34),.34,.26,TIRE,r,rot=(R(90),0,0),seg=18); ocyl((sx,sy*1.04,.34),.22,.02,RIM,r,rot=(R(90),0,0),seg=10)
    return r
def main_road():
    B.box((PX+4,-3.5,-.05),(16,6,.05),M('#5E5C58',.85,kind='asphalt'),0); B.box((PX+4,.0,.08),(16,1.0,.08),M('#C9C2B4',.8,kind='wall'),.01)
    for k in range(-7,9): B.box((PX+k*2.2,-3.6,.003),(.6,.06,.003),M('#E8E2D6',.6),0)
    # ---- Pizza Point: red/white front, glass, oven glow, tables, menu board
    x,y=PIZ['x'],PIZ['y']
    B.box((x,y+1.6,1.8),(2.6,.1,1.8),M('#F4E9D8',.8,kind='wall'),0)
    for s in (-1,1): B.box((x+s*2.65,y+.3,1.8),(.12,1.4,1.8),M('#C8102E',.6),.01)
    B.box((x,y+.3,3.6),(2.75,1.4,.08),M('#E8E2D6',.8),0); B.box((x,y+.3,.0),(2.6,1.35,.02),M('#D8C9B0',.4,spec=.5,kind='tile'),0)
    img_plane(4.4,1.1,img_mat('sign_pizza',1.2),(x,y-1.18,3.0),(0,0,0)); B.box((x,y-1.14,3.0),(2.25,.04,.6),M('#7A0A18',.5),.01)
    B.box((x,y-1.06,.25),(2.6,.06,.25),M('#C8102E',.6),.01)
    for k,xx in enumerate((x-1.4,x+.3)): B.box((xx,y-1.06,1.4),(.85 if k==0 else .7,.02,.9),M('#BFE3F5',.05,spec=.9,alpha=.3),0)
    B.box((x+1.6,y-1.06,1.3),(.55,.02,1.05),M('#BFE3F5',.05,spec=.9,alpha=.25),0); B.box((x+1.6,y-1.08,1.3),(.58,.03,1.08),M('#7A0A18',.5),0) if False else None
    for s in (-1,1): B.box((x+s*1.0,y-1.06,1.4),(.05,.08,1.2),M('#7A0A18',.5),.01)
    # inside: counter, oven (glow), menu, 2 tables
    B.box((x-.5,y+1.0,.55),(1.3,.35,.55),M('#7A0A18',.5),.02); B.box((x-.5,y+1.0,1.12),(1.32,.37,.03),M('#E8E2D6',.3),.01)
    B.box((x+1.4,y+1.3,1.0),(.8,.25,.8),M('#6E5A4A',.7),.04); B.box((x+1.4,y+1.04,.95),(.4,.02,.25),M('#FF8A30',.2,emit=6),0)
    img_plane(1.4,.7,img_mat('box_lid',.6),(x-.5,y+1.48,2.3),(0,0,0))
    for k in range(2):
        tx=x-1.6+k*1.3; B.cyl((tx,y-.2,.74),.35,.03,M('#F4F1EA',.4),seg=18,rot=(0,0,0)); B.cyl((tx,y-.2,.37),.04,.74,M('#3A3B45',.4,metal=.6),seg=8,rot=(0,0,0))
    point((x,y+.3,3.2),120,(1,.9,.75),.5,shadow=False)
    # stacked pizza boxes on a stool by the door, delivery bike parked in front
    for k in range(4): B.box((x+2.2,y-1.4,.5+k*.07),(.2,.2,.03),M('#E9D2A6',.6),.01)
    # ---- Prestige Motors showroom: big glass front, yellow car inside, spot lights
    sx,sy_=SHW['x'],SHW['y']
    B.box((sx,sy_+2.4,2.4),(3.6,.1,2.4),M('#2B2C33',.5),0)
    for s in (-1,1): B.box((sx+s*3.6,sy_+.7,2.4),(.12,1.8,2.4),M('#1A1B22',.4,metal=.4),.01)
    B.box((sx,sy_+.7,4.8),(3.7,1.8,.12),M('#1A1B22',.4,metal=.4),.01); B.box((sx,sy_+.7,.02),(3.6,1.75,.02),M('#E8E8EC',.12,spec=.9),0)
    img_plane(6.0,1.05,img_mat('sign_showroom',1.4),(sx,sy_-1.18,4.2),(0,0,0))
    for k in range(3): B.box((sx-2.4+k*2.4,sy_-1.08,2.1),(1.17,.02,1.95),M('#D8ECF5',.03,spec=1.0,alpha=.18),0); B.box((sx-1.2+k*2.4,sy_-1.08,2.1),(.04,.05,1.95),M('#1A1B22',.4,metal=.5),0)
    B.box((sx,sy_-1.08,.08),(3.6,.06,.08),M('#1A1B22',.4,metal=.5),0)
    CAR=lambo(sx,sy_+.6,180,'#F2C12E')
    for k in range(3): point((sx-2+k*2,sy_+.6,4.4),160,(1,.97,.92),.3,shadow=False)
    # rope barrier + plant outside showroom, footpath tiles, trees, other shops, cars passing area
    for k in range(3): B.cyl((sx-1.5+k*1.5,-.4,.45),.04,.9,M('#C9A24A',.2,metal=.8),seg=10,rot=(0,0,0)); B.ico((sx-1.5+k*1.5,-.4,.92),.06,M('#C9A24A',.2,metal=.8),sub=2)
    plant(sx+3.2,-.3,1.2,'#2B2C33'); plant(x-2.9,-.35,1.0)
    tree(PX-6,.75,4.6,.8,2); tree(PX+15,-.4,4.4,1.0,8)
    for k,col in enumerate(('#D9C3A5','#C9D6D2')):
        xx=PX-11+k*30; B.box((xx,4.0,3.2),(3.8,2.6,3.2),M(col,.85,kind='wall'),.02)
        for z in (1.4,4.2): B.box((xx,1.38,z),(1.4,.03,.5),M('#9FC8E0',.1,spec=.9),0)
    car_parked(PX-3.5,-4.6,'#2F4E8C',0); car_parked(PX+16,-2.3,'#E8E2D6',180)
    for k in range(-1,3): B.cyl((PX-4+k*9,-.7,3.0),.08,6.0,M('#5A5550',.6),seg=8,rot=(0,0,0))
    B.box((PX+6,-.7,5.7),(13,.01,.01),M('#1A1B22',.5),0)
    return dict(car=CAR)
# ================================================================ props
def phone_obj(screen='ph_signal'):
    e=empty((0,0,0)); obox((0,0,0),(.04,.007,.082),M('#15161A',.3),.006,e); sc=img_plane(.072,.148,img_mat(screen,1.2),(0,-.0075,0),(0,0,0),parent=e); return e,sc
def pizza_box():
    e=empty((0,0,0)); obox((0,0,0),(.2,.2,.03),M('#E9D2A6',.6),.008,e); img_plane(.34,.34,img_mat('box_lid',.25),(0,0,.0305),(R(-90),0,0),parent=e) if False else None
    lid=img_plane(.36,.36,img_mat('box_lid',.3),(0,0,.031),(R(90)*0,0,0),parent=e); lid.rotation_euler=(R(-90),0,0); return e
def note_obj(kind='note100'):
    e=empty((0,0,0)); img_plane(.15,.075,img_mat(kind,.3),(0,0,0),(R(90),0,0),parent=e); return e
def helmet_obj(col='#C8102E'):
    e=empty((0,0,0)); oico((0,0,0),.19,M(col,.25,spec=.8),e,sc=(1,1.08,.95)); obox((0,-.15,-.02),(.15,.05,.08),M('#1B1B20',.05,spec=1.0),.04,e); obox((0,0,-.17),(.17,.16,.03),M('#1B1B20',.5),.02,e)
    return e
