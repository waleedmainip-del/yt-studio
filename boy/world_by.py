# sets for "Every Pakistani boy lives the same life": Waleed's messy bedroom, drawing room, Bilal's street corner
ASSET='/home/claude/boy/assets/'
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
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=False):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot
    try: a.data.use_shadow=shadow
    except Exception: pass
    return a
CLOTH=['#C6453A','#2F4E8C','#F4F1EA','#22242B','#3E9C5A','#E8C25A','#7A4EC2','#8A6A4A','#2F8C99']
def cloth_flat(x,y,z,sx,sy,col,rz=0,th=.03):
    B.box((x,y,z+th),(sx,sy,th),M(col,.85,kind='fabric',spec=.2),.02,rot=(0,0,R(rz)))
def bottle(x,y,z,h=.26,r=.04,col='#7FC8E8',cap='#2F4E8C',alpha=.6):
    B.cyl((x,y,z+h/2),r,h,M(col,.08,spec=.9,alpha=alpha),seg=12,rot=(0,0,0)); B.cyl((x,y,z+h+.02),r*.45,.04,M(cap,.4),seg=8,rot=(0,0,0))
def can(x,y,z,col='#1E1F26',band='#3E9C5A',tip=False):
    if tip: B.cyl((x,y,z+.035),.035,.13,M(col,.3,metal=.6),seg=12,rot=(0,R(90),0)); return
    B.cyl((x,y,z+.065),.035,.13,M(col,.3,metal=.6),seg=12,rot=(0,0,0)); B.cyl((x,y,z+.07),.036,.03,M(band,.3,metal=.5),seg=12,rot=(0,0,0))
# ---------------------------------------------------------------- BEDROOM (origin)
BR=dict(x0=-3.0,x1=3.0,y0=-2.6,y1=2.6,h=3.4)
BED=dict(x0=-3.0,x1=-.3,y0=.35,y1=2.45,top=.66)     # mattress top z=.66, head at west wall
DESK=dict(x=2.62,y0=-.9,y1=1.1,top=.86)            # desk against east wall
CHAIR=(1.75,.15)                                    # gaming chair seat centre, seat top .56, faces +x (to the desk)
def bedroom(night=False):
    x0,x1,y0,y1,h=BR['x0'],BR['x1'],BR['y0'],BR['y1'],BR['h']
    WALL=M('#D8C7A8',.85,kind='wall');
    B.box((0,0,-.05),(x1+.2,y1+.2,.05),M('#9A7A5A',.55,kind='wall',spec=.4),0)
    for i in range(-3,3):
        for j in range(-3,3): B.box((i+.5,j+.5,.002),(.49,.49,.002),M(['#A8865E','#9A7A5A'][(i+j)%2],.5,spec=.4),0)
    B.box((-.2,-.4,.006),(1.4,1.0,.004),M('#3B4F78',.9,kind='fabric'),0); B.box((-.2,-.4,.008),(1.25,.85,.004),M('#C9B48F',.9,kind='fabric'),0)
    for (cx,cy,sx,sy) in ((0,y1,x1,.1),(x0,0,.1,y1),(x1,0,.1,y1)): B.box((cx,cy,h/2),(sx,sy,h/2),WALL,0)
    B.box(((x0+1.42)/2,y0,h/2),((1.42-x0)/2,.1,h/2),WALL,0); B.box(((2.58+x1)/2,y0,h/2),((x1-2.58)/2,.1,h/2),WALL,0)
    B.box((0,0,h+.05),(x1,y1,.05),M('#EDE6DA',.8,kind='wall'),0)
    for (cx,cy,sx,sy) in ((0,y1-.12,x1,.02),((x0+1.42)/2,y0+.12,(1.42-x0)/2,.02),(x0+.12,0,.02,y1),(x1-.12,0,.02,y1)): B.box((cx,cy,.07),(sx,sy,.07),M('#F4F1EA',.6),.01)
    # window (north wall, x 0.6..2.0) with curtains
    wx=1.3
    B.box((wx,y1-.06,1.9),(.75,.03,.65),M('#F4F1EA',.5),.01)
    B.box((wx,y1-.07,1.9),(.68,.02,.58),M('#1E2A4A' if night else '#BFE3F5',.1,emit=(.5 if night else 2.2)),0)
    B.box((wx,y1-.09,1.9),(.02,.02,.58),M('#F4F1EA',.5),0); B.box((wx,y1-.09,1.9),(.68,.02,.02),M('#F4F1EA',.5),0)
    for s in (-1,1): B.box((wx+s*.95,y1-.16,1.85),(.22,.05,1.05),M('#7A4EC2',.8,kind='fabric'),.06)
    B.cyl((wx,y1-.2,2.95),.02,2.2,M('#C9CDD6',.3,metal=.8),seg=8,rot=(0,R(90),0))
    if night:
        for k in range(8): B.ico((wx-.5+k*.14,y1-.05,1.55+(k%3)*.25),.02,M('#FFE2A8',.2,emit=4),sub=1)
    # BED: frame, mattress, pillow, crumpled sheet (blanket is a separate object)
    bx0,bx1,by0,by1,top=BED['x0'],BED['x1'],BED['y0'],BED['y1'],BED['top']; cx=(bx0+bx1)/2; cy=(by0+by1)/2
    B.box((cx,cy,.18),((bx1-bx0)/2,(by1-by0)/2,.18),WOODB,.02); B.box((bx0+.06,cy,.75),(.06,(by1-by0)/2,.75),WOODB,.03)
    for yy in (by0,by1): B.box((bx1-.04,yy,.25),(.05,.05,.25),WOODB,.01)
    B.box((cx,cy,.52),((bx1-bx0)/2-.04,(by1-by0)/2-.04,.14),M('#E9E4DA',.85,kind='fabric'),.06)
    B.box((bx0+.42,cy-.38,top+.035),(.28,.38,.04),M('#F4F1EA',.8,kind='fabric'),.035,rot=(0,0,R(8)))
    B.box((bx0+.4,cy+.5,top+.035),(.22,.3,.04),M('#C6453A',.8,kind='fabric'),.035,rot=(0,0,R(-12)))
    # nightstand + lamp + headphones
    B.box((bx0+.3,by0-.32,.3),(.26,.24,.3),WOODB,.02); B.cyl((bx0+.3,by0-.32,.7),.05,.2,M('#C9A24A',.4,metal=.5),seg=10,rot=(0,0,0)); B.cyl((bx0+.3,by0-.32,.92),.18,.22,M('#F4E8C8',.6,emit=(1.6 if night else .2)),seg=14,rot=(0,0,0),r2=.12)
    B.box((bx0+.22,by0-.36,.63),(.08,.1,.03),M('#22242B',.4),.02)
    # DESK + monitor + keyboard + bottles, cans, chips, plates
    dx,dy0,dy1,dt=DESK['x'],DESK['y0'],DESK['y1'],DESK['top']; dcy=(dy0+dy1)/2
    B.box((dx,dcy,dt-.03),(.36,(dy1-dy0)/2,.03),M('#2B2C33',.4),.01)
    for yy in (dy0+.05,dy1-.05):
        for xx in (dx-.3,dx+.3): B.box((xx,yy,(dt-.06)/2),(.025,.025,(dt-.06)/2),M('#1A1B22',.4,metal=.5),.005)
    B.box((dx+.12,dcy+.1,dt+.02),(.12,.18,.02),M('#1A1B22',.4),.01); B.box((dx+.16,dcy+.1,dt+.22),(.03,.03,.2),M('#1A1B22',.4),.01)
    B.box((dx+.14,dcy+.1,dt+.6),(.03,.52,.3),M('#111216',.3),.02)
    img_plane(.98,.55,img_mat('mon_game',1.6 if night else .9),(dx+.105,dcy+.1,dt+.6),(0,0,R(-90)))
    B.box((dx-.15,dcy+.1,dt+.012),(.1,.3,.012),M('#22242B',.4),.006)
    for k in range(12): B.box((dx-.17+(k%2)*.07,dcy-.12+(k//2)*.07,dt+.026),(.025,.025,.004),M(['#E8505B','#2F8C99','#F2C12E'][k%3],.3,emit=(1.2 if night else .4)),0)
    B.box((dx-.12,dcy-.38,dt+.008),(.06,.09,.006),M('#22242B',.4),.01)
    for i,(yy,col) in enumerate(((dy0+.12,'#7FC8E8'),(dy0+.24,'#9FD89A'),(dy1-.12,'#F4C07A'))): bottle(dx-.22,yy,dt,col=col)
    for i,yy in enumerate((dy0+.36,dy0+.46)): can(dx-.05,yy,dt,col='#1E1F26',band=['#3E9C5A','#E8505B'][i])
    can(dx-.25,dy1-.3,dt,tip=True)
    B.box((dx-.2,dy1-.55,dt+.02),(.12,.09,.02),M('#F2C12E',.4,spec=.7),.03,rot=(0,0,R(20))); B.box((dx-.08,dy1-.38,dt+.02),(.08,.06,.016),M('#E8505B',.4,spec=.7),.02,rot=(0,0,R(-30)))
    B.cyl((dx-.25,dy0+.62,dt+.012),.12,.012,M('#FFFFFF',.2,spec=.8),seg=16,rot=(0,0,0))
    # bottles + cans on the floor near the desk and bed
    for (xx,yy,tp) in ((2.1,-1.5,False),(2.3,-1.2,True),(-.05,.15,True),(.3,-1.9,False)): bottle(xx,yy,0,col='#7FC8E8',alpha=.6) if not tp else can(xx,yy,0,tip=True)
    # clothes everywhere
    r=random.Random(7)
    for k,(xx,yy,sx,sy,rz) in enumerate(((-.6,-.9,.32,.22,20),(.4,-1.6,.28,.2,-35),(1.2,-.6,.3,.22,60),(-1.6,-1.7,.34,.24,10),(.9,1.6,.26,.2,-15),(-.2,-2.1,.3,.2,40),(1.9,-2.0,.25,.18,-60))):
        cloth_flat(xx,yy,0,sx,sy,CLOTH[k%len(CLOTH)],rz)
    # WARDROBE (south wall, west) open with clothes spilling
    B.box((-2.1,y0+.35,1.25),(.8,.3,1.25),WOODB,.02)
    B.box((-2.1,y0+.08,1.25),(.76,.02,1.2),M('#3A2618',.7),0)
    for k in range(6): B.box((-2.6+k*.2,y0+.4,1.55),(.08,.22,.45),M(CLOTH[k],.8,kind='fabric'),.04)
    B.box((-1.35,y0+.95,1.25),(.03,.4,1.2),WOODB,.01,rot=(0,0,R(-25)))
    cloth_flat(-1.9,y0+.85,0,.3,.2,'#2F8C99',30); cloth_flat(-1.6,y0+.95,.06,.26,.18,'#C6453A',-20)
    # dusty dumbbells
    for k in range(2):
        xx=-.9+k*.35; B.cyl((xx,y0+.45,.06),.06,.3,M('#3A3B45',.5,metal=.6),seg=10,rot=(0,R(90),0) if False else (R(90),0,0))
    # door (south wall, east)  centre x=2.0
    # door opening x 1.45..2.55 in the south wall: wall pieces around it, frame, hinged leaf (opens inward), hallway behind
    B.box((2.0,y0,1.3),(.6,.13,1.3),M('#000000',1),0) if False else None
    B.box((2.0,y0,2.95),(.56,.1,.45),WALL,0)
    for s_ in (-1,1): B.box((2.0+s_*.58,y0,1.3),(.04,.13,1.3),M('#5A3820',.5,kind='wall'),.005)
    B.box((2.0,y0,2.62),(.62,.13,.04),M('#5A3820',.5,kind='wall'),.005)
    hinge=empty((1.46,y0+.02,0)); obox((.54,0,1.3),(.53,.03,1.28),M('#8A5A3A',.5,kind='wall'),.01,hinge); obox((.98,.05,1.15),(.03,.03,.06),M('#C9CDD6',.2,metal=.9),.005,hinge); obox((.98,-.05,1.15),(.03,.03,.06),M('#C9CDD6',.2,metal=.9),.005,hinge)
    B.box((2.0,y0-1.0,-.05),(1.6,1.0,.05),M('#C9C0B0',.6,kind='wall'),0); B.box((2.0,y0-2.0,1.7),(1.6,.1,1.7),M('#E8DCC4',.85,kind='wall'),0)
    for s_ in (-1,1): B.box((2.0+s_*1.55,y0-1.0,1.7),(.1,1.0,1.7),M('#E8DCC4',.85,kind='wall'),0)
    B.box((2.0,y0-1.0,3.45),(1.6,1.0,.05),M('#F4F1EA',.8),0); B.box((2.0,y0-1.9,1.9),(.4,.03,.3),M('#5C8C6A',.6),.01)
    if not night: area((2.0,y0-1.0,3.2),40,(2,1.6),(1,.95,.85))
    # posters (text fully on the wall, never overlapping the window/bed)
    img_plane(.62,.86,img_mat('poster_car',.25),(-1.7,y1-.11,2.15),(0,0,0))
    img_plane(.5,.7,img_mat('poster_gym',.25),(.55,y0+.11,2.05),(0,0,R(180)))
    # wall clock on east wall above desk, hands set later
    B.cyl((x1-.11,0.1,2.6),.24,.04,M('#F4F1EA',.4),seg=24,rot=(0,R(90),0)); B.cyl((x1-.13,0.1,2.6),.25,.02,M('#22242B',.4),seg=24,rot=(0,R(90),0))
    for k in range(12):
        a=2*pi*k/12; B.box((x1-.135,0.1+.2*math.sin(a),2.6+.2*math.cos(a)),(.004,.012,.02 if k%3==0 else .01),M('#22242B',.4),0,rot=(R(-math.degrees(a)),0,0))
    hrs=empty((x1-.14,0.1,2.6)); mins=empty((x1-.14,0.1,2.6))
    obox((0,0,.07),(.006,.012,.08),M('#22242B',.3),0,hrs); obox((0,0,.1),(.004,.008,.12),M('#22242B',.3),0,mins)
    # ceiling fan + light
    fan=empty((0,0,h-.25)); B.cyl((0,0,h-.1),.03,.2,M('#F4F1EA',.5),seg=8,rot=(0,0,0)); B.cyl((0,0,h-.25),.12,.1,M('#F4F1EA',.5),seg=14,rot=(0,0,0))
    for k in range(3): obox((math.cos(2*pi*k/3)*.48,math.sin(2*pi*k/3)*.48,0),(.48,.07,.008),M('#F4F1EA',.5),.01,fan,rot=(0,0,2*pi*k/3))
    if night:
        area((0,0,h-.2),18,(2,2),(.5,.6,1.0))
        area((dx-.1,dcy+.1,1.5),45,(.5,1.0),(.55,.6,1.0),rot=(0,R(90),0))
        point((bx0+.3,by0-.32,1.0),20,(1,.75,.45),.2,shadow=False)
    else:
        area((0,0,h-.2),70,(4,4),(1,.95,.86)); area((wx,y1-.4,1.9),110,(1.4,1.2),(1,.95,.85),rot=(R(-90),0,0)); area((-1.0,-1.6,2.8),20,(2,2),(1,.9,.8))
    return dict(fan=fan,hrs=hrs,mins=mins,door=hinge)
WOODB=M('#6E4428',.6,kind='wall')
def set_clock(D,hh,mm):
    D['hrs'].rotation_euler=(R(-((hh%12)+mm/60)*30),0,0); D['mins'].rotation_euler=(R(-mm*6),0,0)
def gaming_chair(x,y,rz,charger=True):
    """seat top .56, back on the far side from the desk; returns nothing (static)"""
    a=R(rz); c,s_=math.cos(a),math.sin(a)
    def P(dx,dy,z): return (x+dx*c-dy*s_,y+dx*s_+dy*c,z)
    BL=M('#1A1B22',.5); RD=M('#C6453A',.5)
    B.box(P(0,0,.5),(.28,.28,.06),BL,.05,rot=(0,0,a)); B.box(P(-.3,0,1.05),(.05,.27,.5),BL,.06,rot=(0,R(-8),a)); B.box(P(-.33,0,1.05),(.02,.1,.42),RD,.01,rot=(0,R(-8),a))
    B.cyl(P(0,0,.28),.04,.4,M('#888C96',.3,metal=.8),seg=8,rot=(0,0,0))
    for k in range(5): an=2*pi*k/5; B.box(P(.22*math.cos(an),.22*math.sin(an),.06),(.13,.025,.02),BL,.01,rot=(0,0,a+an))
    for sy in (-1,1): B.box(P(0,sy*.3,.72),(.2,.03,.03),BL,.01,rot=(0,0,a)); B.box(P(0,sy*.3,.62),(.02,.02,.1),BL,0,rot=(0,0,a))
    if charger:   # charger cable tangled around the chair stem and legs
        for k in range(26):
            an=k*.55; rr=.06+.02*math.sin(k); B.cyl(P(rr*math.cos(an),rr*math.sin(an),.14+k*.012),.007,.06,M('#F4F5FA',.4),seg=6,rot=(R(70),0,an))
        for k in range(12): B.ico(P(.25+k*.06,.12+.05*math.sin(k),.008),.008,M('#F4F5FA',.4),sub=1)
        B.box(P(.95,.15,.012),(.03,.02,.012),M('#F4F5FA',.4),.004)
# ---------------------------------------------------------------- DRAWING ROOM (x=40)
LX=40
DRDOOR=[None]
def drawing_room():
    x0,x1,y0,y1,h=LX-4,LX+4,-3.4,3.4,3.4; WALL=M('#E9DFC9',.85,kind='wall')
    B.box((LX,0,-.05),(4.2,3.6,.05),M('#E2D8C6',.3,kind='wall',spec=.6),0)
    for (cx,cy,sx,sy) in ((LX,y1,4,.1),(LX,y0,4,.1),(x1,0,.1,3.4)): B.box((cx,cy,h/2),(sx,sy,h/2),WALL,0)
    B.box((x0,(y0-2.38)/2,h/2),(.1,(-2.38-y0)/2,h/2),WALL,0); B.box((x0,(-1.22+y1)/2,h/2),(.1,(y1+1.22)/2,h/2),WALL,0); B.box((x0,-1.8,2.98),(.1,.6,.42),WALL,0)
    for s_ in (-1,1): B.box((x0,-1.8+s_*.6,1.3),(.13,.04,1.3),M('#5A3820',.5,kind='wall'),.005)
    B.box((LX,0,h+.05),(4,3.4,.05),M('#F4F1EA',.8,kind='wall'),0); B.box((LX,0,h-.02),(1.2,1.0,.02),M('#FFF6E8',.3,emit=.12),0)
    # rug
    B.box((LX,.3,.005),(2.4,1.7,.004),M('#7E1A2C',.9,kind='fabric'),0); B.box((LX,.3,.007),(2.1,1.45,.004),M('#C9A24A',.9,kind='fabric'),0); B.box((LX,.3,.009),(1.8,1.2,.004),M('#7E1A2C',.9,kind='fabric'),0)
    SOF=M('#2F4E8C',.7,kind='fabric'); SOF2=M('#24406E',.7,kind='fabric')
    # 3-seater on north wall facing -y: seat top .52 at y 2.55
    B.box((LX,2.6,.3),(1.5,.5,.22),SOF,.08); B.box((LX,3.0,.85),(1.5,.14,.4),SOF2,.08)
    for s in (-1,1): B.box((LX+s*1.55,2.6,.55),(.12,.5,.25),SOF2,.06)
    for k in range(3): B.box((LX-1.0+k*1.0,2.55,.56),(.46,.42,.04),SOF,.05)
    # single sofas west (facing +x) and east (facing -x)
    for s,xx in ((-1,LX-2.6),(1,LX+2.6)):
        B.box((xx,.3,.3),(.5,.55,.22),SOF,.08); B.box((xx+s*.42,.3,.85),(.12,.55,.4),SOF2,.08)
        for sy in (-1,1): B.box((xx,.3+sy*.6,.55),(.5,.1,.25),SOF2,.06)
    # centre table with chai, biscuits, namak paare
    B.box((LX,.4,.42),(.8,.45,.03),M('#3A2618',.4,spec=.5),.02)
    for xx in (-.7,.7):
        for yy in (-.35,.35): B.box((LX+xx,.4+yy,.2),(.03,.03,.2),M('#3A2618',.4),.01)
    for k,(xx,yy) in enumerate(((-.45,.15),(-.2,.6),(.3,.6),(.5,.15))):
        B.cyl((LX+xx,.4+yy,.47),.04,.08,M('#FFFFFF',.2,spec=.8),seg=12,rot=(0,0,0)); B.cyl((LX+xx,.4+yy,.505),.034,.004,M('#B5793F',.3),seg=12,rot=(0,0,0)); B.cyl((LX+xx,.4+yy,.452),.07,.006,M('#FFFFFF',.2),seg=14,rot=(0,0,0))
    B.cyl((LX,.4,.46),.18,.02,M('#E8E2D6',.2,spec=.8),seg=18,rot=(0,0,0))
    for k in range(7): B.cyl((LX+.1*math.cos(k),.4+.1*math.sin(k*1.3),.48+.01*(k%2)),.035,.012,M('#D9A05A',.6),seg=10,rot=(0,0,0))
    # TV unit on south wall with TV
    B.box((LX,y0+.35,.3),(1.2,.25,.3),M('#3A2618',.5),.02); B.box((LX,y0+.16,1.35),(.85,.04,.5),M('#0B0C10',.2,spec=.9),.02)
    for k in range(3): B.cyl((LX-.9+k*.9,y0+.35,.7),.08,.2,M(['#C9A24A','#2F8C99','#C6453A'][k],.4,spec=.6),seg=10,rot=(0,0,0))
    # curtains + window (east wall)
    B.box((x1-.06,1.0,1.9),(.03,.8,.7),M('#BFE3F5',.1,emit=2.0),0)
    for s in (-1,1): B.box((x1-.15,1.0+s*1.05,1.85),(.05,.25,1.1),M('#C9A24A',.8,kind='fabric'),.06)
    # landscape painting above sofa + wall lamps
    B.box((LX,y1-.08,2.25),(.9,.03,.5),M('#C9A24A',.4,metal=.6),.01); img_plane(1.64,.84,img_mat('painting',.3),(LX,y1-.115,2.25),(0,0,0))
    for s in (-1,1): B.box((LX+s*2.2,y1-.1,2.3),(.1,.06,.16),M('#FFE2A8',.3,emit=2.0),.02)
    # door west wall (entrance) centre y=-1.8
    dh=empty((x0+.06,-2.33,0)); obox((0,.53,1.3),(.03,.52,1.28),M('#6E4428',.5,kind='wall'),.01,dh); obox((.05,.95,1.15),(.03,.03,.06),M('#C9A24A',.2,metal=.9),.005,dh)
    B.box((x0-1.0,-1.8,-.05),(1.0,1.2,.05),M('#C9C0B0',.6,kind='wall'),0); B.box((x0-1.9,-1.8,1.7),(.1,1.2,1.7),M('#E8DCC4',.85,kind='wall'),0); B.box((x0-1.0,-3.0,1.7),(1.0,.1,1.7),M('#E8DCC4',.85,kind='wall'),0); B.box((x0-1.0,-.6,1.7),(1.0,.1,1.7),M('#E8DCC4',.85,kind='wall'),0); B.box((x0-1.0,-1.8,3.45),(1.0,1.2,.05),M('#F4F1EA',.8),0)
    # plants
    for (xx,yy) in ((LX-3.5,2.9),(LX+3.5,-2.9)):
        B.cyl((xx,yy,.25),.2,.5,M('#C9B48F',.6),seg=12,rot=(0,0,0))
        for j in range(6): B.ico((xx+.2*math.cos(j),yy+.2*math.sin(j),.7+j*.08),.2,LEAF[j%4],sub=1,sc=(1,1,.7))
    DRDOOR[0]=dh
    area((LX,0,h-.2),100,(6,5),(1,.93,.84)); area((x1-.4,1.0,1.9),80,(1.6,1.4),(1,.95,.85),rot=(0,R(-90),0)); area((LX,y0+1.0,1.8),25,(3,1),(1,.9,.8),rot=(R(90),0,0))
LEAF=[M('#3E8E4A',.7,kind='leaves'),M('#5FA84A',.7,kind='leaves'),M('#2F7A45',.7,kind='leaves'),M('#74B85A',.7,kind='leaves')]
# ---------------------------------------------------------------- BILAL'S STREET CORNER (x=-40), afternoon
SX=-40
def street_corner():
    B.box((SX,0,-.05),(10,8,.05),M('#8A857C',.8,kind='asphalt'),0); B.box((SX,2.2,.06),(10,1.4,.06),M('#B5AE9F',.8,kind='wall'),.01)
    for k in range(4):
        xx=SX-4.5+k*3.0; B.box((xx,3.75,2.0),(1.45,.25,2.0),M(['#E9DFC9','#D8C7A8','#C9D6D2','#E8D4C0'][k],.8,kind='wall'),0)
        B.box((xx,3.45,1.25),(1.2,.06,1.15),M('#9AA0A8',.4,metal=.6),.01)
        for j in range(12): B.box((xx,3.4,.25+j*.18),(1.18,.01,.01),M('#7A808A',.4,metal=.6),0)
        B.box((xx,3.42,2.75),(1.3,.05,.28),M(['#C6453A','#2F4E8C','#3E9C5A','#F2C12E'][k],.5),.02)
    text('BILAL MOBILES',(SX-1.5,3.36,2.75),(0,-1,0),.26,M('#FFFFFF',.3,emit=.6),ex=.01)
    text('KARACHI TIKKA',(SX+1.5,3.36,2.75),(0,-1,0),.24,M('#FFFFFF',.3,emit=.6),ex=.01)
    # bike
    bx,by=SX+.9,1.0
    for dx in (-.55,.55): B.cyl((bx+dx,by,.33),.3,.08,M('#111216',.8),seg=16,rot=(R(90),0,0)); B.cyl((bx+dx,by,.33),.14,.09,M('#888C96',.3,metal=.8),seg=12,rot=(R(90),0,0))
    B.box((bx,by,.62),(.5,.12,.14),M('#C6453A',.3,metal=.4),.06); B.box((bx-.15,by,.8),(.32,.13,.06),M('#1A1B22',.6),.04); B.box((bx+.52,by,.95),(.04,.35,.03),M('#888C96',.3,metal=.8),.01)
    for k in range(3): B.cyl((SX-3+k*3,1.6,2.0),.08,4.0,M('#5A5550',.6),seg=8,rot=(0,0,0))
    for k in range(2): B.box((SX-1.5+k*3,1.6,3.95),(1.5,.008,.008),M('#1A1B22',.5),0)
    area((SX,-2,6),250,(10,6),(1,.92,.8),rot=(R(25),0,0))
# ---------------------------------------------------------------- props
def phone_obj(screen='scr_lock'):
    """phone in portrait, screen facing -y local; returns (phone, screen plane)"""
    o=obox((0,0,0),(.045,.007,.09),M('#1A1B22',.3,metal=.3),.01)
    sc=img_plane(.082,.165,img_mat(screen,1.2),(0,-.0085,0),(0,0,0),o); return o,sc
def set_screen(sc,name,emit=1.2): sc.data.materials[0]=img_mat(name,emit)
def blanket():
    o=obox((0,0,0),(1.05,.85,.12),M('#2F7A8C',.85,kind='fabric'),.1)
    for k in range(5): obox((-.9+k*.45,0,.121),(.04,.84,.004),M('#F2C12E',.85,kind='fabric'),0,o)
    return o
def lie(H,x,y,z,head_dir=-1):
    """lie on the back, head toward -x (head_dir=-1) or +x, face up. x,y = hip centre; z = surface height"""
    u=H['u']; legs0(H); arms(H,0,0,4,0,0,-4); H['root'].rotation_euler=(R(-90),0,R(90*(-head_dir)))
    # root origin is at the feet: place feet 4.0u from head side... body axis along x
    H['root'].location=(x-head_dir*2.0*u,y,z+.55*u+.075)
# ---------------------------------------------------------------- draped blanket (follows whatever is under it: mattress, body, pillow)
class Drape:
    def __init__(self,x0,x1,y0,y1,nx=46,ny=30,col='#2F7A8C',stripe='#F2C12E',bed=None):
        self.x0,self.x1,self.y0,self.y1,self.nx,self.ny=x0,x1,y0,y1,nx,ny; self.bed=bed
        vs=[(0,0,0)]*((nx+1)*(ny+1)); fs=[]
        for i in range(nx):
            for j in range(ny): a=i*(ny+1)+j; fs.append((a,a+ny+1,a+ny+2,a+1))
        me=bpy.data.meshes.new('drape'); me.from_pydata(vs,[],fs); me.update()
        o=bpy.data.objects.new('drape',me); _col.objects.link(o); m=M(col,.9,kind='fabric',spec=.15); me.materials.append(m)
        mod=o.modifiers.new('sol','SOLIDIFY'); mod.thickness=.035; mod.offset=1
        o.modifiers.new('sub','SUBSURF').levels=1
        for poly in me.polygons: poly.use_smooth=True
        self.o=o; self.me=me
    def update(self,edge_x=None):
        """edge_x: head-side edge of the blanket (x). Blanket spans edge_x .. x1"""
        sc=bpy.context.scene; self.o.hide_viewport=True; bpy.context.view_layer.update(); dg=bpy.context.evaluated_depsgraph_get()
        e=self.x0 if edge_x is None else edge_x; nx,ny=self.nx,self.ny; Z=[[0]*(ny+1) for _ in range(nx+1)]
        bx0,bx1,by0,by1,top=self.bed['x0'],self.bed['x1'],self.bed['y0'],self.bed['y1'],self.bed['top']
        for i in range(nx+1):
            x=L(e,self.x1,i/nx)
            for j in range(ny+1):
                y=L(self.y0,self.y1,j/ny); hit,loc,nrm,idx,ob,mx=sc.ray_cast(dg,Vector((x,y,3.0)),Vector((0,0,-1)),distance=3.0)
                z=loc.z if hit else top
                if not (by0<y<by1) : z=min(z,top)
                Z[i][j]=z+.045
        # relax: blanket can't follow tiny gaps — take local max and smooth, then let edges past the bed side hang down
        for it in range(2):   # dilate so thin parts (hands, shoes) never poke through
            Z2=[r[:] for r in Z]
            for i in range(nx+1):
                for j in range(ny+1): Z2[i][j]=max(Z[a][b] for a in (i-1,i,i+1) for b in (j-1,j,j+1) if 0<=a<=nx and 0<=b<=ny)
            Z=Z2
        for it in range(3):
            Z2=[r[:] for r in Z]
            for i in range(nx+1):
                for j in range(ny+1):
                    nb=[Z[a][b] for a in (i-1,i,i+1) for b in (j-1,j,j+1) if 0<=a<=nx and 0<=b<=ny]
                    Z2[i][j]=max(Z[i][j],sum(nb)/len(nb))
            Z=Z2
        vs=[]
        for i in range(nx+1):
            x=L(e,self.x1,i/nx)
            for j in range(ny+1):
                y=L(self.y0,self.y1,j/ny); z=Z[i][j]
                if y<by0: d=by0-y; y=by0-.02; z=top+.02-d*1.6
                if y>by1: d=y-by1; y=by1+.02; z=top+.02-d*1.6
                if x>bx1: d=x-bx1; x=bx1+.02; z=min(z,top+.02-d*1.6)
                vs.append((x,y,z))
        for k,v in enumerate(vs): self.me.vertices[k].co=v
        self.me.update(); self.o.hide_viewport=False

def chappal():
    o=obox((0,0,0),(.05,.12,.012),M('#6E4428',.6),.01); obox((0,.03,.025),(.045,.02,.015),M('#C6453A',.6),.005,o); return o
def shirt_obj(col='#E8C25A'):
    o=empty((0,0,0)); obox((0,0,0),(.24,.02,.3),M(col,.85,kind='fabric',spec=.2),.03,o)
    for s_ in (-1,1): obox((s_*.3,0,.16),(.08,.02,.12),M(col,.85,kind='fabric',spec=.2),.02,o,rot=(0,R(s_*40),0))
    obox((0,-.021,.25),(.07,.004,.05),M(shade(col,.8),.85),0,o); return o
def chips():
    return obox((0,0,0),(.08,.03,.11),M('#F2C12E',.35,spec=.7),.03)
