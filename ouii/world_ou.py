# sets for "We came for one drink" (OUII): warm restaurant interior + modern Lahore boulevard exterior + food props
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=False):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot; a.data.use_shadow=shadow; return a
def seg(a,b,r,mat,sides=6):
    a=Vector(a); b=Vector(b); d=b-a; c=(a+b)/2; rot=d.to_track_quat('Z','Y').to_euler(); B.cyl(tuple(c),r,d.length,mat,rot=tuple(rot),seg=sides)
LEAF=[M('#3E8E4A',.7,kind='leaves'),M('#5FA84A',.7,kind='leaves'),M('#2F7A45',.7,kind='leaves'),M('#74B85A',.7,kind='leaves'),M('#4C9A50',.7,kind='leaves')]
ORANGE='#EC9E34'; OR2='#D9822A'; CREAM='#F4E6CC'; WALNUT='#5A3A26'; OAK='#B9824E'; CHAR='#26262C'; BRASS='#C9A24A'
_IMG={}
def img_mat(name,emit=1.0,tint='#FFFFFF',clip=True,base=False):
    k=(name,emit,tint,clip,base)
    if k in _IMG: return _IMG[k]
    m=bpy.data.materials.new(name); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']; tx=nt.nodes.new('ShaderNodeTexImage')
    tx.image=bpy.data.images.load('/home/claude/ouii/assets/%s.png'%name,check_existing=True); tx.extension='CLIP'
    mix=nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type='MULTIPLY'; mix.inputs[0].default_value=1; mix.inputs[2].default_value=hexc(tint); nt.links.new(tx.outputs['Color'],mix.inputs[1])
    nt.links.new(mix.outputs[0],b.inputs['Base Color']); nt.links.new(mix.outputs[0],b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=emit; b.inputs['Roughness'].default_value=.5
    nt.links.new(tx.outputs['Alpha'],b.inputs['Alpha']); m.blend_method='CLIP' if clip else 'BLEND'; m.alpha_threshold=.5; m.shadow_method='NONE'
    _IMG[k]=m; return m
def img_plane(w,h,mat,loc=(0,0,0),rot=(0,0,0),parent=None):
    """quad in the XZ plane facing -y, w x h, centred"""
    me=bpy.data.meshes.new('ip'); me.from_pydata([(-w/2,0,-h/2),(w/2,0,-h/2),(w/2,0,h/2),(-w/2,0,h/2)],[],[(0,1,2,3)]); uv=me.uv_layers.new(name='uv')
    for i,c in enumerate(((0,0),(1,0),(1,1),(0,1))): uv.data[i].uv=c
    me.update(); o=bpy.data.objects.new('ip',me); o.location=loc; o.rotation_euler=rot; _col.objects.link(o); me.materials.append(mat)
    if parent: o.parent=parent
    return o
LOGO_AR=2.158
def LOGO(loc,n,h,emit=4.0,tint='#FFFFFF',parent=None,rot=None):
    """real OUII wordmark (white letters) as a glowing cut-out, h = letter-block height"""
    return img_plane(h*LOGO_AR,h,img_mat('logo_white',emit,tint),loc,rot if rot is not None else (0,0,math.atan2(n[0],-n[1])),parent)
def LOGOD(loc,n,d,emit=1.2,parent=None,rot=None):
    """orange disc logo"""
    return img_plane(d,d,img_mat('logo_disc',emit),loc,rot if rot is not None else (0,0,math.atan2(n[0],-n[1])),parent)
def plant(x,y,z,s=1.0,seed=1,pot='#E8DCC8'):
    r=random.Random(seed); B.cyl((x,y,z+.22*s),.2*s,.44*s,M(pot,.6),seg=12,r2=.26*s)
    for i in range(7):
        a=2*pi*i/7+r.uniform(-.3,.3); h=r.uniform(.5,.95)*s
        B.box((x+math.cos(a)*.16*s,y+math.sin(a)*.16*s,z+.44*s+h/2),(.035*s,.11*s,h/2),LEAF[i%5],.02,rot=(R(r.uniform(-22,22)),R(r.uniform(-22,22)),a))
def hanging_plant(x,y,z,s=1.0,seed=1):
    r=random.Random(seed); B.cyl((x,y,z-.15*s),.02,.3*s,M(CHAR,.5),seg=6); B.cyl((x,y,z-.42*s),.2*s,.24*s,M('#C96F3E',.7),seg=12,r2=.14*s)
    for i in range(8):
        a=2*pi*i/8; ln=r.uniform(.4,.9)*s
        B.box((x+math.cos(a)*.2*s,y+math.sin(a)*.2*s,z-.42*s-ln/2),(.03*s,.07*s,ln/2),LEAF[i%5],.02,rot=(R(r.uniform(-8,8)),R(r.uniform(-8,8)),a))
def pendant(x,y,zc,drop=1.2,col=ORANGE,r_=.32,light=0):
    B.cyl((x,y,zc-drop/2),.012,drop,M(CHAR,.5),seg=6)
    B.cyl((x,y,zc-drop-.14),r_,.28,M(col,.45,metal=.15),seg=20,r2=.09); B.cyl((x,y,zc-drop-.3),r_*.98,.03,M(shade(col,.8),.5),seg=20)
    B.ico((x,y,zc-drop-.3),.12,M('#FFE2A8',.3,emit=9.0),sub=2)
    if light: point((x,y,zc-drop-.55),light,(1,.74,.42),.25,shadow=False)
def chair_static(x,y,rz,col=OAK,seat=ORANGE):
    """wooden cafe chair; seat top z=.52; faces -y when rz=0 (back at +y)"""
    Mx=Matrix.Translation((x,y,0))@Euler((0,0,R(rz))).to_matrix().to_4x4()
    def P(lx,ly,lz): return tuple(Mx@Vector((lx,ly,lz)))
    W=M(col,.55,kind='wall')
    for sx in (-.4,.4):
        for sy in (-.36,.36): B.cyl(P(sx,sy,.23),.045,.46,W,seg=8)
    B.box(P(0,0,.47),(.47,.43,.05),M(seat,.8,kind='fabric'),.03,rot=(0,0,R(rz)))
    for sx in (-.4,.4): B.box(P(sx,.4,.95),(.045,.04,.48),W,.015,rot=(0,0,R(rz)))
    B.box(P(0,.41,1.22),(.46,.04,.17),W,.03,rot=(0,0,R(rz))); B.box(P(0,.41,.85),(.42,.03,.05),W,.015,rot=(0,0,R(rz)))
def chair_obj(x,y,rz,col=OAK,seat=ORANGE):
    e=empty((x,y,0),rot=(0,0,R(rz))); W=M(col,.55,kind='wall')
    for sx in (-.4,.4):
        for sy in (-.36,.36): ocyl((sx,sy,.23),.045,.46,W,e,rot=(0,0,0),seg=8)
    obox((0,0,.47),(.47,.43,.05),M(seat,.8,kind='fabric'),.03,e)
    for sx in (-.4,.4): obox((sx,.4,.95),(.045,.04,.48),W,.015,e)
    obox((0,.41,1.22),(.46,.04,.17),W,.03,e); obox((0,.41,.85),(.42,.03,.05),W,.015,e)
    return e
def table_static(x,y,w=2.2,d=1.3,h=1.12,top='#8A5A38'):
    B.box((x,y,h-.04),(w/2,d/2,.04),M(top,.4,kind='wall'),.03)
    B.box((x,y,h-.1),(w/2-.12,d/2-.12,.03),M(shade(top,.75),.5),.01)
    B.cyl((x,y,h/2-.05),.07,h-.14,M(CHAR,.35,metal=.6),seg=12); B.cyl((x,y,.03),.42,.06,M(CHAR,.35,metal=.6),seg=20)
TH=1.12   # hero table top height
GT=[(-4.5,-.7),(3.4,-3.6),(-3.4,-4.6)]   # guest tables
def restaurant(door_open=0.0,light=True):
    """room x[-7,7] y[-6,6]; hero table at origin; counter + neon OUII on back wall (y=6); glass entrance on west wall (x=-7, y in [-3.6,-1.2])"""
    FLR=M('#B98A5E',.5,kind='wall'); WALL=M('#F2DFC2',.85,kind='wall'); TERRA=M('#D8743C',.85,kind='wall'); PANEL=M(WALNUT,.55,kind='wood',sc=2.5); CEIL=M('#3A2A20',.9,kind='wall')
    B.box((0,0,-.05),(7.2,6.2,.05),FLR,0)
    for i in range(-11,12): B.box((i*.62,0,.002),(.006,6.1,.002),M('#8A6240',.6),0)
    B.box((0,6.05,2.3),(7.2,.05,2.3),WALL,0); B.box((7.05,0,2.3),(.05,6.2,2.3),TERRA,0); B.box((0,0,4.62),(7.2,6.2,.05),CEIL,0)
    # west wall with door opening y[-3.7,-1.1] z[0,3.1], window y[.2,4.6]
    B.box((-7.05,-5.0,2.3),(.05,1.25,2.3),WALL,0); B.box((-7.05,-2.4,3.85),(.05,1.35,.75),WALL,0); B.box((-7.05,-.45,2.3),(.05,.65,2.3),WALL,0)
    B.box((-7.05,2.4,.5),(.05,2.2,.5),WALL,0); B.box((-7.05,2.4,3.95),(.05,2.2,.65),WALL,0); B.box((-7.05,5.3,2.3),(.05,.75,2.3),WALL,0)
    GL=M('#BFE0F0',.05,spec=1.0,alpha=.16); FRM=M(CHAR,.4,metal=.5)
    obox((-7.05,2.4,2.15),(.02,2.2,1.15),GL,0)
    for yy in (.2,1.65,3.15,4.6): B.box((-7.05,yy,2.15),(.06,.05,1.17),FRM,.01)
    for zz in (1.0,3.3): B.box((-7.05,2.4,zz),(.07,2.25,.05),FRM,.01)
    # south wall (behind most cameras) with windows
    B.box((0,-6.05,.5),(7.2,.05,.5),WALL,0); B.box((0,-6.05,3.95),(7.2,.05,.65),WALL,0)
    for xx in (-6.6,-2.2,2.2,6.6): B.box((xx,-6.05,2.15),(.6 if abs(xx)>6 else .25,.05,1.15),WALL,0)
    obox((0,-6.06,2.15),(7.0,.02,1.15),GL,0)
    # wall panelling + trims
    B.box((0,5.98,.6),(7.1,.03,.6),PANEL,.01); B.box((6.98,0,.6),(.03,6.1,.6),PANEL,.01); B.box((0,5.96,1.22),(7.1,.05,.03),M(BRASS,.3,metal=.8),.01); B.box((6.96,0,1.22),(.05,6.1,.03),M(BRASS,.3,metal=.8),.01)
    for i in range(24): B.box((6.97,-5.8+i*.5,2.9),(.03,.07,1.65),M(OAK,.5,kind='wood',sc=3),.01)      # east wall wood slats
    for i in range(6): B.box((-6+i*2.4,0,4.5),(.09,6.1,.09),M('#2A1D16',.6,kind='wood'),.01)                 # ceiling beams
    # entrance doors (two glass leaves hinged at y=-3.7 and y=-1.1), handles, mat, EXIT sign
    DR=[]
    for s,hy in ((1,-3.7),(-1,-1.1)):
        e=empty((-7.05,hy,0),rot=(0,0,R(s*door_open*-78))); DR.append((s,e))
        obox((0,s*.65,1.55),(.03,.65,1.55),M('#BFE0F0',.05,spec=1.0,alpha=.22),0,e)
        for zz in (.06,3.04): obox((0,s*.65,zz),(.045,.65,.06),FRM,.01,e)
        for yy in (.03,1.27): obox((0,s*yy,1.55),(.045,.04,1.55),FRM,.01,e)
        obox((.07,s*1.12,1.5),(.025,.025,.38),M(BRASS,.25,metal=.9),.01,e); obox((-.07,s*1.12,1.5),(.025,.025,.38),M(BRASS,.25,metal=.9),.01,e)
    B.box((-7.05,-2.4,3.14),(.08,1.36,.05),FRM,.01); B.box((-6.2,-2.4,.012),(.75,1.1,.012),M('#3A2A20',.95,kind='fabric'),0)
    B.box((-6.93,-2.4,3.45),(.03,.5,.16),M('#1F8A4C',.4,emit=2.5),.02); text('EXIT',(-6.9,-2.4,3.45),(1,0,0),.2,M('#FFFFFF',.3,emit=3),ex=.004)
    B.box((6.93,-4.6,3.3),(.03,.7,.18),M(CHAR,.5),.02); text('WASHROOM',(6.9,-4.6,3.3),(-1,0,0),.17,M('#FFE2A8',.3,emit=3),ex=.004)
    B.box((6.97,-4.6,1.55),(.03,.62,1.55),M(WALNUT,.5,kind='wood',sc=2),.02); B.cyl((6.9,-4.15,1.45),.05,.06,M(BRASS,.25,metal=.9),rot=(0,R(90),0),seg=10)
    # street seen through door/window: sunset backdrop + silhouettes
    B.box((-13,0,6),(.05,16,8),M('#FFB878',.9,emit=1.6),0); B.box((-9.5,0,-.04),(2.5,14,.04),M('#8E8478',.9,kind='concrete',sc=.6),0)
    for i,(yy,h,c) in enumerate([(-6,7,'#D8C2A0'),(-1.5,9,'#C9A888'),(3,6.5,'#E0C8A8'),(7,8,'#B89878')]): B.box((-12.2,yy,h/2),(.4,2.1,h/2),M(c,.9,kind='wall'),0)
    for yy in (-4.6,.4,5.2):
        B.cyl((-9.4,yy,1.4),.12,2.8,M('#6B4A30',.8,kind='wood'),seg=8)
        for k in range(4): B.ico((-9.4+(k%2)*.5-.25,yy+(k//2)*.5-.25,3.2+.3*(k%3)),.75,LEAF[k],sc=(1,1,.85),sub=1)
    # ---- back counter + kitchen pass + shelves + menu boards + neon
    CT=M('#3B2A22',.5,kind='wood',sc=2); TOP=M('#EDE3D2',.25,spec=.8)
    B.box((1.2,4.75,.62),(3.6,.42,.62),CT,.02); B.box((1.2,4.7,1.27),(3.7,.5,.035),TOP,.015)
    for i in range(12): B.box((-2.2+i*.62,4.31,.62),(.03,.012,.55),M(OAK,.5,kind='wood',sc=3),.004)
    B.box((1.2,4.3,.08),(3.6,.02,.08),M(BRASS,.3,metal=.8),.005); B.cyl((1.2,4.29,.68),.42,.03,M(ORANGE,.5,emit=.5),rot=(R(90),0,0),seg=32); LOGOD((1.2,4.27,.68),(0,-1,0),.8,emit=.8)
    B.box((1.2,5.95,2.35),(3.7,.06,.04),M(OAK,.5,kind='wood',sc=3),.01); B.box((1.2,5.95,3.0),(3.7,.06,.04),M(OAK,.5,kind='wood',sc=3),.01)
    r=random.Random(4)
    for i in range(22):
        xx=-2.3+i*.33; zz=2.39 if i%2 else 3.04; c=r.choice(['#E8DCC8','#F28A2E','#2E8B6E','#C9302C','#F2C12E','#FFFFFF','#8A5A38'])
        if i%3==0: B.cyl((xx,5.9,zz+.16),.07,.32,M(c,.3,spec=.8),seg=10); B.cyl((xx,5.9,zz+.38),.03,.12,M(c,.3),seg=8)
        elif i%3==1: B.cyl((xx,5.9,zz+.09),.09,.18,M('#FFFFFF',.4),seg=12,r2=.07)
        else: B.box((xx,5.9,zz+.12),(.1,.07,.12),M(c,.6),.02)
    for k,xx in enumerate((-1.6,.2,2.0,3.8)):          # menu boards
        B.box((xx,5.97,3.75),(.8,.03,.5),M('#1B1B20',.7),.02); LOGO((xx,5.93,4.1),(0,-1,0),.16,emit=2.5,tint=ORANGE)
        for j in range(5): B.box((xx-.15+.1*(j%2),5.93,3.95-j*.13),(.42-.1*(j%2),.008,.022),M('#F4E6CC',.5,emit=.5),0)
    # espresso machine, POS, cake dome, cup stacks, juice dispensers
    B.box((3.6,4.95,1.6),(.55,.3,.3),M('#C9CDD6',.25,metal=.9),.04); B.box((3.6,4.72,1.42),(.5,.08,.04),M(CHAR,.4),.01)
    for s in (-.25,.25): B.cyl((3.6+s,4.7,1.5),.035,.14,M(CHAR,.4,metal=.6),seg=8)
    B.box((.2,4.6,1.52),(.22,.04,.2),M(CHAR,.3),.02,rot=(R(-18),0,0)); B.box((.2,4.62,1.5),(.19,.03,.16),M('#7FD3FF',.3,emit=1.2),.01,rot=(R(-18),0,0)); B.box((.2,4.7,1.34),(.14,.14,.05),M(CHAR,.4),.02)
    B.cyl((1.8,4.7,1.33),.34,.05,M('#FFFFFF',.3),seg=20); B.cyl((1.8,4.7,1.45),.26,.18,M('#E8B48C',.6),seg=18); B.cyl((1.8,4.7,1.56),.27,.05,M('#F4E6CC',.5),seg=18)
    obox((1.8,4.7,1.62),(.3,.3,.26),M('#DDEEF6',.03,spec=1.0,alpha=.14),.12)
    for k,c in enumerate(('#F2A65A','#E0483A','#F2C12E')):
        B.cyl((-1.6+k*.5,4.85,1.62),.17,.6,M(c,.15,spec=.9,alpha=.85),seg=14); B.cyl((-1.6+k*.5,4.85,1.95),.18,.06,M(CHAR,.4),seg=14); B.box((-1.6+k*.5,4.66,1.4),(.03,.05,.03),M('#C9CDD6',.3,metal=.9),.005)
    for k in range(5): B.cyl((2.7+.0*k,4.6,1.31+k*.05),.07,.1,M('#FFFFFF',.5),seg=10,r2=.085)
    # kitchen pass (dark opening with warm glow) on the right of back wall
    B.box((5.6,5.98,2.2),(1.0,.04,.75),M('#1A1512',.9),0); B.box((5.6,5.9,1.42),(1.1,.16,.04),M('#C9CDD6',.25,metal=.9),.01); B.box((5.6,5.94,2.55),(.9,.01,.3),M('#FFB45A',.4,emit=2.2),0)
    for s in (-.5,.5): B.cyl((5.6+s,5.85,2.75),.11,.2,M('#C9CDD6',.3,metal=.9),seg=12,r2=.02)
    # neon OUII on brick feature panel, back wall left
    B.box((-4.3,5.97,2.75),(2.2,.04,1.55),M('#9C4A32',.8,kind='concrete',sc=.22),.02)
    B.cyl((-4.3,5.93,3.05),1.03,.05,M('#FFE2B0',.3,emit=3.0),rot=(R(90),0,0),seg=48); LOGOD((-4.3,5.89,3.05),(0,-1,0),1.95,emit=.55)
    text('sometimes we forget',(-4.3,5.9,1.78),(0,-1,0),.24,M('#FFF3E0',.3,emit=4.5),ex=.012); text("we're a restaurant",(-4.3,5.9,1.47),(0,-1,0),.24,M('#FFF3E0',.3,emit=4.5),ex=.012)
    B.box((-4.3,4.9,.5),(2.0,.42,.26),M(OR2,.8,kind='fabric'),.1); B.box((-4.3,5.5,1.15),(2.0,.16,.62),M(OR2,.8,kind='fabric'),.1); B.box((-4.3,5.0,.14),(2.05,.5,.14),PANEL,.02)   # banquette
    for xx in (-5.4,-3.2): table_static(xx,3.9,1.2,.9)
    # east wall booths, framed posters, shelves with plants
    for k,yy in enumerate((2.6,-.4)):
        B.box((6.35,yy,.5),(.5,1.1,.26),M('#2E6E62',.8,kind='fabric'),.1); B.box((6.78,yy,1.15),(.14,1.1,.62),M('#2E6E62',.8,kind='fabric'),.1); table_static(5.1,yy,1.1,1.5)
        chair_static(4.05,yy,90,seat='#2E6E62')
    for k,(yy,c) in enumerate(((1.1,ORANGE),(-1.9,'#2E8B6E'),(4.2,'#F2C12E'))):
        B.box((6.9,yy,3.0),(.03,.48,.62),M(CHAR,.5),.02); B.box((6.87,yy,3.0),(.01,.42,.56),M('#F4E6CC',.6),0); B.cyl((6.85,yy,3.05),.24,.012,M(c,.5),rot=(0,R(90),0),seg=20)
    # other tables with chairs
    table_static(0,0)
    for (tx,ty) in GT:
        table_static(tx,ty,1.5,1.1)
        chair_static(tx-1.35,ty,90); chair_static(tx+1.35,ty,-90)
    # plants + pendants + string lights
    plant(-6.4,5.4,0,1.6,1); plant(6.3,5.3,0,1.5,2); plant(-6.4,-.4,0,1.4,3,pot=ORANGE); plant(6.4,-5.4,0,1.5,4); plant(-6.4,-5.4,0,1.3,5)
    for i,(xx,yy) in enumerate(((-5.2,1.8),(2.9,1.6),(-2.6,-2.6),(5.6,-2.2),(0.2,3.2))): hanging_plant(xx,yy,4.5,1.0+.2*(i%2),i+3)
    for (xx,yy,c,lt) in ((0,0,ORANGE,0),(GT[0][0],GT[0][1],'#F2C12E',0),(GT[1][0],GT[1][1],ORANGE,0),(GT[2][0],GT[2][1],'#E8DCC8',0),(5.1,2.6,ORANGE,0),(5.1,-.4,'#F2C12E',0),(-5.4,3.9,'#E8DCC8',0),(-3.2,3.9,ORANGE,0)): pendant(xx,yy,4.55,1.15,c)
    for k,xx in enumerate((-1.5,.5,2.5,4.2)): pendant(xx,4.55,4.55,.85,'#E8DCC8',.22)
    for i in range(30):
        f=i/29; B.ico((-6.8+13.6*f,-5.85,3.9-.35*math.sin(pi*((f*5)%1))),.05,M('#FFD88A',.3,emit=8),sub=1)
    B.done('resto')
    if light:
        S,A,w,bg=setup_interior('evening',room=(0,0,4.4),res=PCT,samples=SAMPLES)
        A.data.size=9; A.data.energy=260; A.data.color=(1,.84,.62)
        point((0,-.2,3.0),190,(1,.72,.42),.35); point((-4.3,4.3,2.6),70,(1,.66,.3),.4,shadow=False); point((1.5,3.6,3.2),150,(1,.8,.55),.4,shadow=False)
        point((4.6,-1.2,3.1),110,(1,.74,.46),.4,shadow=False); point((-4.2,-2.6,3.1),110,(1,.78,.5),.4,shadow=False)
        area((-6.6,-2.4,2.4),260,(2.4,2.8),(1,.7,.45),rot=(0,R(-90),0))
    return DR
def set_doors(DR,k):
    for s,e in DR: e.rotation_euler[2]=R(s*k*-78)
# ---------------------------------------------------------------- food + props (object based, parent empties)
GLASSM=M('#DCEFF4',.03,spec=1.0,alpha=.2); ICE=M('#EAF6FA',.05,spec=1.0,alpha=.55); PEACH=M('#EE8E44',.25,spec=.6,emit=.22); PEACHS=M('#FFB36A',.35,emit=.35)
def tea(loc,fill=1.0,scale=1.0,drops=True,seed=1):
    """OUII peach iced tea: clear plastic cup (h .46) with dome lid, white logo, straw, ice, peach slices"""
    e=empty(loc); e.scale=(scale,)*3; r=random.Random(seed)
    ocyl((0,0,.235),.105,.46,GLASSM,e,rot=(0,0,0),seg=24,r2=.15); ocyl((0,0,.012),.1,.02,M('#DCEFF4',.05,spec=1.0,alpha=.45),e,rot=(0,0,0),seg=24)
    ocyl((0,0,.465),.158,.022,M('#F2F8FA',.08,spec=1.0,alpha=.5),e,rot=(0,0,0),seg=24); oico((0,0,.47),.15,M('#EAF6FA',.03,spec=1.0,alpha=.16),e,sc=(1,1,.5),sub=3)
    lq=ocyl((0,0,.03+.19*fill),.099,.38*fill,PEACH,e,rot=(0,0,0),seg=24,r2=.099+.037*fill); lq2=ocyl((0,0,.035+.38*fill),.134*(.75+.25*fill),.012,M('#FFC98A',.2,emit=.6),e,rot=(0,0,0),seg=24)
    ice=[]
    for i in range(6):
        a=r.uniform(0,6.28); o=obox((.05*math.cos(a),.05*math.sin(a),.1+.055*i),(.042,.042,.042),ICE,.012,e,rot=(r.uniform(0,3),r.uniform(0,3),r.uniform(0,3))); ice.append(o)
    for i,(a,z) in enumerate(((.4,.2),(2.6,.31),(4.4,.12))): ocyl((.085*math.cos(a),.085*math.sin(a),z),.06,.02,PEACHS,e,rot=(R(90),0,a+1.57),seg=14)
    st=ocyl((.02,.02,.42),.014,.6,M('#F4F1EA',.5),e,rot=(R(6),R(-7),0),seg=8)
    for k in range(4): ocyl((.02-.012*(k-1.5),.02+.01*(k-1.5),.24+k*.12),.0155,.04,M(ORANGE,.5),e,rot=(R(6),R(-7),0),seg=8)
    for a in (0.0,3.14159):
        LOGO((.136*math.sin(a),-.136*math.cos(a),.26),(0,-1,0),.062,emit=1.2,parent=e,rot=(R(-5),0,a))
    if drops:
        for i in range(26):
            a=r.uniform(0,6.28); z=r.uniform(.06,.42); rr=.107+.045*(z-.005)/.46
            oico((rr*math.cos(a),rr*math.sin(a),z),r.uniform(.006,.011),M('#F4FBFD',.02,spec=1.0,alpha=.7),e,sc=(1,1,1.5),sub=1)
    return dict(root=e,liq=lq,liq2=lq2,ice=ice,straw=st)
GLAZE=['#B8521E','#C9622A','#A84818','#D2702E']
def wing(parent,loc,rot=(0,0,0),s=1.0,k=0):
    e=empty(loc,parent,rot=rot); g=M(GLAZE[k%4],.22,spec=.9)
    oico((0,0,0),.075*s,g,e,sc=(1.7,1,.85),sub=2); oico((.13*s,0,.005),.05*s,g,e,sc=(1.2,1,.9),sub=2); oico((-.14*s,0,0),.03*s,M('#F2E2C4',.5),e,sub=1)
    for i in range(5): oico(((-.08+.045*i)*s,(.02 if i%2 else -.03)*s,.062*s),.008*s,M('#F7EBCF',.5),e,sub=1)
    return e
def wings_bowl(loc,n=9,scale=1.0,seed=3):
    """Dynamight Chipotle Wings in the orange OUII paper bowl, creamy drizzle + spring onion"""
    e=empty(loc); e.scale=(scale,)*3; r=random.Random(seed); PB=M(ORANGE,.55)
    ocyl((0,0,.12),.2,.24,PB,e,rot=(0,0,0),seg=28,r2=.3); ocyl((0,0,.243),.305,.016,M('#F7EBD6',.5),e,rot=(0,0,0),seg=28); ocyl((0,0,.235),.285,.012,M('#7A3A16',.5),e,rot=(0,0,0),seg=28)
    for a in (0.0,3.14159): LOGO((.262*math.sin(a),-.262*math.cos(a),.125),(0,-1,0),.085,emit=.9,parent=e,rot=(R(-22),0,a))
    W=[]
    for i in range(n):
        a=2*pi*i/max(1,min(n,6))+r.uniform(-.2,.2); rad=.16 if i<6 else .05; z=.28 if i<6 else .37
        W.append(wing(e,(rad*math.cos(a),rad*math.sin(a),z+r.uniform(0,.02)),(r.uniform(-.3,.3),r.uniform(-.3,.3),a+r.uniform(-.5,.5)),1.0,i))
    if n>1:
        for i in range(9): oico((r.uniform(-.17,.17),r.uniform(-.17,.17),.36+r.uniform(0,.05)),r.uniform(.02,.034),M('#F2D9B0',.35),e,sc=(1.3,1,.45),sub=1)
        for i in range(12): obox((r.uniform(-.2,.2),r.uniform(-.2,.2),.39+r.uniform(0,.04)),(.02,.008,.006),LEAF[3],0,e,rot=(r.uniform(0,3),0,r.uniform(0,3)))
    ocyl((.4,-.16,.05),.075,.09,M('#F7EBD6',.4),e,rot=(0,0,0),seg=14,r2=.09); ocyl((.4,-.16,.09),.08,.012,M('#F2D9B0',.3),e,rot=(0,0,0),seg=14)
    return dict(root=e,wings=W)
def fries(loc,rz=0,seed=2):
    e=empty(loc,rot=(0,0,R(rz))); r=random.Random(seed); obox((0,0,.11),(.13,.09,.11),M('#E0483A',.6),.02,e); obox((0,-.095,.12),(.08,.004,.05),M('#FFFFFF',.5),.004,e)
    for i in range(16): obox((r.uniform(-.1,.1),r.uniform(-.06,.06),.27+r.uniform(-.03,.05)),(.016,.016,.11),M('#F2C24A',.6),.005,e,rot=(r.uniform(-.35,.35),r.uniform(-.35,.35),0))
    return e
def burger(loc,seed=1):
    e=empty(loc); ocyl((0,0,.012),.22,.024,M('#F4F1EA',.4),e,rot=(0,0,0),seg=20)
    ocyl((0,0,.06),.15,.07,M('#D9963E',.6),e,rot=(0,0,0),seg=18); ocyl((0,0,.105),.165,.025,LEAF[1],e,rot=(0,0,0),seg=12); ocyl((0,0,.135),.155,.045,M('#5A2E1A',.7),e,rot=(0,0,0),seg=18)
    obox((0,0,.165),(.16,.16,.008),M('#F2B81E',.5),.004,e,rot=(0,0,.6)); ocyl((0,0,.18),.15,.02,M('#C9302C',.5),e,rot=(0,0,0),seg=14); oico((0,0,.2),.155,M('#D9963E',.55),e,sc=(1,1,.6),sub=2)
    return e
def plate_pasta(loc):
    e=empty(loc); ocyl((0,0,.015),.26,.03,M('#F4F1EA',.35),e,rot=(0,0,0),seg=22); oico((0,0,.06),.17,M('#F2D28A',.6),e,sc=(1,1,.42),sub=2); oico((0,0,.1),.1,M('#D2472A',.5),e,sc=(1,1,.4),sub=2)
    for a in (0,2,4): obox((.05*math.cos(a),.05*math.sin(a),.135),(.03,.016,.004),LEAF[1],.003,e,rot=(0,0,a))
    return e
def nachos(loc,seed=5):
    e=empty(loc); r=random.Random(seed); ocyl((0,0,.03),.24,.06,M('#2B2C33',.4),e,rot=(0,0,0),seg=20,r2=.3)
    for i in range(14):
        a=r.uniform(0,6.28); d=r.uniform(0,.19); omesh([(0,0,0),(.11,0,0),(.055,.1,0)],[(0,1,2)],M('#F2C24A',.6),e,loc=(d*math.cos(a),d*math.sin(a),.08+r.uniform(0,.07)),thick=.008).rotation_euler=(r.uniform(-.6,.6),r.uniform(-.6,.6),a)
    oico((0,0,.14),.07,M('#F4F1EA',.4),e,sc=(1,1,.5),sub=2); oico((.07,.03,.13),.05,M('#5FA84A',.5),e,sc=(1,1,.5),sub=2); oico((-.06,-.04,.13),.05,M('#C9302C',.5),e,sc=(1,1,.5),sub=2)
    return e
def napkin_box(loc):
    e=empty(loc); obox((0,0,.07),(.1,.06,.07),M(CHAR,.4),.01,e); obox((0,0,.15),(.085,.045,.02),M('#FFFFFF',.8),.005,e); return e
def menu_card(loc,rz=0):
    e=empty(loc,rot=(0,0,R(rz))); obox((0,0,.006),(.17,.24,.006),M(CHAR,.5),.004,e); obox((0,.1,.014),(.1,.03,.002),M(ORANGE,.4,emit=.6),0,e)
    for j in range(4): obox((0,.02-j*.05,.014),(.12,.01,.002),M('#F4E6CC',.5),0,e)
    return e
def bill_folder(loc):
    e=empty(loc); cov=M('#1B1B20',.45); back=obox((0,0,0),(.13,.008,.2),cov,.006,e); hinge=empty((-.13,-.008,0),e); front=obox((.13,-.004,0),(.13,.006,.2),cov,.006,hinge)
    paper=obox((0,-.012,0),(.105,.003,.17),M('#FFFFFF',.6,emit=.25),0,e); obox((0,-.016,.13),(.06,.002,.018),M(ORANGE,.5),0,e)
    for j in range(9): obox((-.02 if j%2 else 0,-.016,.09-j*.027),(.075,.002,.006),M('#3A3D47',.6),0,e)
    obox((.03,-.016,-.15),(.06,.002,.012),M('#C9302C',.5),0,e)
    return dict(root=e,hinge=hinge,paper=paper)
def tray(parent=None,loc=(0,0,0)):
    e=empty(loc,parent); ocyl((0,0,0),.34,.03,M('#2B2C33',.35,metal=.3),e,rot=(0,0,0),seg=24); ocyl((0,0,.018),.33,.01,M('#3A3D47',.5),e,rot=(0,0,0),seg=24); return e
# ---------------------------------------------------------------- exterior: modern Lahore boulevard with the OUII storefront
MOD=['#E8DCC8','#D8C2A0','#C9D2D8','#F0E8DC','#B8A890','#D9C8B8','#A8B4BC','#E4CDB0']
def car(x,y,col,rz=0):
    r=empty((x,y,0),rot=(0,0,R(rz)))
    BODY=M(col,.18,metal=.5); GL=M('#22303E',.05,spec=1.0); TIRE=M('#111216',.8); RIM=M('#D8DEE6',.25,metal=.9)
    obox((0,0,.55),(2.25,.95,.3),BODY,.1,r); obox((-.25,0,1.08),(1.2,.86,.3),BODY,.14,r); obox((-.25,0,1.09),(1.15,.88,.24),GL,.06,r)
    for s in (-1,1): obox((2.24,s*.62,.62),(.03,.2,.07),M('#FFF2C8',.3,emit=4),.01,r); obox((-2.24,s*.62,.66),(.03,.22,.07),M('#E8262A',.3,emit=2),.01,r)
    W=[]
    for sx in (-1.4,1.4):
        for sy in (-1,1): W.append(ocyl((sx,sy*(.93),.34),.34,.24,TIRE,r,rot=(R(90),0,0),seg=18)); ocyl((sx,sy*1.05,.34),.2,.02,RIM,r,rot=(R(90),0,0),seg=14)
    r['wheels']=0; return r
def block(x,y,w,d,h,seed,face=-1,glow=True):
    """modern commercial block; lit windows on the side facing `face` (y direction)"""
    r=random.Random(seed); col=r.choice(MOD); B.box((x,y,h/2),(w/2,d/2,h/2),M(col,.8,kind='wall'),.02); B.box((x,y,h+.12),(w/2+.1,d/2+.1,.12),M(shade(col,.8),.7),.02)
    fy=y+face*(d/2+.01)
    for fl in range(1,int(h/3.2)+1):
        z=fl*3.2-1.2
        if z>h-.9: break
        n=max(1,int(w/2.0))
        for i in range(n):
            xx=x-w/2+w*(i+.5)/n; lit=glow and r.random()<.45
            B.box((xx,fy,z),(.62,.02,.8),M('#FFD9A0',.3,emit=1.8) if lit else M('#33485C',.15,spec=.9),0); B.box((xx,fy+face*.03,z-.86),(.7,.05,.04),M(shade(col,.7),.7),.01)
    if r.random()<.6: B.box((x+r.uniform(-w/4,w/4),y,h+.7),(.9,.7,.5),M('#C9CDD6',.4,metal=.4),.03)
    if r.random()<.5:
        c=r.choice(['#2E8B6E','#C9302C','#2B58C9','#F2C12E','#7448C2']); B.box((x,fy+face*.06,3.6),(w/2-.6,.05,.36),M(c,.5,emit=.5),.02); B.box((x,fy,1.6),(w/2-.5,.02,1.5),M('#2A2D36',.25,spec=.9),0)
def palm(x,y,s=1.0,seed=1):
    r=random.Random(seed); B.cyl((x,y,2.6*s),.16*s,5.2*s,M('#8A6A48',.8,kind='wood'),seg=8,r2=.11*s)
    for i in range(8):
        a=2*pi*i/8+r.uniform(-.2,.2); B.box((x+math.cos(a)*1.0*s,y+math.sin(a)*1.0*s,5.05*s),(1.1*s,.22*s,.03),LEAF[i%5],0,rot=(0,R(24),a))
    B.ico((x,y,5.2*s),.28*s,LEAF[2],sub=1)
def streetlamp(x,y,side=1):
    B.cyl((x,y,2.6),.07,5.2,M(CHAR,.4,metal=.6),seg=8); B.box((x,y-side*.5,5.2),(.06,.5,.05),M(CHAR,.4,metal=.6),.01); B.box((x,y-side*1.0,5.14),(.14,.22,.05),M('#FFE2A8',.3,emit=7),.02)
def ouii_front(night=False):
    """OUII storefront, facade plane y=6 facing -y, door centred x=0 (opening x[-1.3,1.3] z[0,3.1])"""
    WALLC=M('#2B211C',.7,kind='wall'); B.box((0,10,4.6),(7.0,4,4.6),WALLC,.03); B.box((0,10,9.35),(7.2,4.2,.15),M('#1B1512',.7),.03)
    FR=M(CHAR,.4,metal=.5); GL=M('#F2A85A',.25,emit=1.5 if night else .85)
    for s in (-1,1):
        B.box((s*4.0,5.99,1.9),(2.5,.02,1.5),GL,0)
        for xx in (-2.5,0,2.5): B.box((s*4.0+xx,5.95,1.9),(.05,.05,1.55),FR,.01)
        B.box((s*4.0,5.95,.36),(2.55,.06,.36),M(WALNUT,.55,kind='wood',sc=2.5),.02); B.box((s*4.0,5.95,3.42),(2.55,.05,.05),FR,.01)
        # silhouettes of pendants/tables through the glass
        for k in range(3): B.cyl((s*4.0-1.6+k*1.6,6.4,2.9),.26,.24,M(ORANGE,.4,emit=1.5),seg=14,r2=.08)
        B.box((s*4.0,5.6,.3),(2.3,.28,.3),M('#3A2A20',.7,kind='wood'),.03)
        for k in range(6): B.ico((s*4.0-2.0+k*.8,5.6,.72+.08*(k%2)),.3,LEAF[k%5],sc=(1,1,.8),sub=1)
    B.box((0,6.4,1.55),(1.3,.02,1.55),M('#F2B06A',.25,emit=1.6 if night else .9),0)
    DR=[]
    for s,hx in ((1,-1.3),(-1,1.3)):
        e=empty((hx,5.93,0)); DR.append((s,e)); obox((s*.65,0,1.55),(.65,.03,1.55),M('#BFE0F0',.05,spec=1.0,alpha=.25),0,e)
        for zz in (.06,3.04): obox((s*.65,0,zz),(.65,.045,.06),FR,.01,e)
        for xx in (.03,1.27): obox((s*xx,0,1.55),(.04,.045,1.55),FR,.01,e)
        obox((s*1.12,-.07,1.5),(.025,.025,.38),M(BRASS,.25,metal=.9),.01,e)
    B.box((0,5.9,3.16),(1.4,.08,.06),FR,.01)
    # awning + sign band + wordmark
    B.box((0,5.05,3.75),(6.9,.95,.05),M(ORANGE,.7,kind='fabric'),.02,rot=(R(-13),0,0))
    for k in range(23): B.box((-6.6+k*.6,4.13,3.42),(.15,.02,.14),M(ORANGE if k%2 else '#FFF3E0',.7),.01)
    B.box((0,5.9,5.6),(4.6,.1,1.15),M('#1B1512',.6),.04); B.box((0,5.83,5.6),(4.45,.04,1.0),M('#2B211C',.6),.02)
    LOGO((0,5.78,5.62),(0,-1,0),1.55,emit=7.0 if night else 4.5)
    for s_ in (-1,1): B.box((s_*6.6,5.55,6.6),(.06,.45,.06),FR,.01); B.cyl((s_*6.6,5.1,5.9),.7,.1,M(ORANGE,.5,emit=.6),rot=(0,R(90),0),seg=32); LOGOD((s_*6.6-.06,5.1,5.9),(-1,0,0),1.3,emit=1.6); LOGOD((s_*6.6+.06,5.1,5.9),(1,0,0),1.3,emit=1.6)
    text("sometimes we forget we're a restaurant",(0,5.76,4.62),(0,-1,0),.24,M('#FFF3E0',.3,emit=3.5),ex=.01)
    for s in (-1,1):
        B.cyl((s*6.2,5.3,.35),.34,.7,M(ORANGE,.6),seg=14,r2=.42)
        for k in range(5): B.ico((s*6.2+.2*math.cos(k*1.3),5.3+.2*math.sin(k*1.3),1.05+.2*(k%3)),.36,LEAF[k],sc=(1,1,.9),sub=1)
        B.box((s*1.9,5.86,2.3),(.12,.06,.2),M(CHAR,.4),.02); B.ico((s*1.9,5.74,2.3),.09,M('#FFE2A8',.3,emit=8),sub=1)
    for i in range(26):
        f=i/25; B.ico((-6.8+13.6*f,4.05,3.35-.22*math.sin(pi*((f*4)%1))),.055,M('#FFD88A',.3,emit=9),sub=1)
    # A-frame board + bench
    B.box((3.0,4.3,.55),(.36,.03,.55),M(CHAR,.6),.02,rot=(R(-12),0,0)); LOGO((3.0,4.25,.78),(0,-1,0),.2,emit=2.0,rot=(R(-12),0,0))
    for j in range(3): B.box((3.0,4.27+.04*j,.52-j*.14),(.24,.01,.02),M('#F4E6CC',.5),0,rot=(R(-12),0,0))
    return DR
def boulevard(night=False,aerial=False,seed=9):
    """street along x. sidewalk N y[2.4,6], road y[-8,2.4], sidewalk S y[-11,-8]; OUII on north side at x=0"""
    ASP=M('#3A3C42',.85,kind='asphalt'); PAVE=M('#B9AE9C',.8,kind='concrete',sc=.5); L=110 if aerial else 60
    B.box((0,-2.8,-.05),(L,5.2,.05),ASP,0); B.box((0,4.2,.03),(L,1.8,.08),PAVE,.02); B.box((0,-9.5,.03),(L,1.5,.08),PAVE,.02)
    for i in range(-int(L/4),int(L/4)+1): B.box((i*4,-2.8,.004),(1.1,.07,.004),M('#F2EFE8',.6),0)
    for yy in (2.1,-7.7): B.box((0,yy,.004),(L,.06,.004),M('#F2C12E',.6),0)
    DR=ouii_front(night); r=random.Random(seed)
    x=7.3; k=0
    while x<L-6:
        w=r.uniform(7,12); block(x+w/2,10,w,8,r.uniform(9,22),seed*10+k); x+=w+.25; k+=1
    x=-7.3
    while x>-L+6:
        w=r.uniform(7,12); block(x-w/2,10,w,8,r.uniform(9,22),seed*10+k); x-=w+.25; k+=1
    x=-L+4
    while x<L-6:
        w=r.uniform(8,13)
        if not (aerial and abs(x+w/2)<w/2+9): block(x+w/2,-15,w,8,r.uniform(8,20),seed*10+k,face=1)
        x+=w+.25; k+=1
    for i in range(-int(L/9),int(L/9)+1):
        xx=i*9+4.5
        if abs(xx)>7: palm(xx,3.1,r.uniform(.9,1.15),i)
        if abs(xx+2)>7: palm(xx+2,-8.6,r.uniform(.9,1.15),i+50)
        if abs(i*9)>6: streetlamp(i*9,2.8,1)
        if abs(i*9+4.5)>9 or not aerial: streetlamp(i*9+4.5,-8.3,-1)
    if aerial:
        # wider city: blocks, cross streets, trees, far minarets + a dome for a Lahore silhouette
        for i in range(420):
            xx=r.uniform(-150,150); yy=r.choice((-1,1))*r.uniform(22,150)
            if yy>0 and abs(xx)<8 and yy<30: continue
            if yy<0 and abs(xx)<16: continue
            w=r.uniform(6,13); d=r.uniform(6,13); h=r.uniform(6,20)*(1.6 if r.random()<.08 else 1); col=r.choice(MOD+['#C9A888','#B86A4A','#D8B890'])
            B.box((xx,yy,h/2),(w/2,d/2,h/2),M(col,.85,kind='wall'),0)
            if r.random()<.5: B.box((xx,yy-d/2-.02,h*.55),(w/2-.6,.02,h*.3),M('#FFD9A0',.3,emit=1.4) if r.random()<.5 else M('#33485C',.2),0)
            if r.random()<.3: B.cyl((xx+r.uniform(-1,1),yy+r.uniform(-1,1),h+.5),.5,1.0,M(r.choice(['#2B2C33','#E8E4D8','#3E6FB0']),.5),seg=10)
            if r.random()<.2:
                for q in range(3): B.ico((xx+w/2+1.2,yy+q*1.5-1.5,3.2),1.5,LEAF[q],sc=(1,1,.9),sub=1)
        for (mx,my) in ((-70,120),(-52,128),(64,-120)):
            B.cyl((mx,my,17),1.6,34,M('#A3472E',.8,kind='concrete',sc=.4),seg=8); B.ico((mx,my,35.5),1.6,M('#F2EDE2',.5),sub=2)
        B.ico((-61,124,13),7,M('#F2EDE2',.5),sc=(1,1,.9),sub=3); B.box((-61,124,6),(11,7,6),M('#A3472E',.8,kind='concrete',sc=.4),0)
        B.box((0,0,-.1),(260,260,.05),M('#8E8478',.95,kind='wall'),0)
        B.box((0,-85,-.04),(6.5,77,.04),ASP,0)
        for i in range(30): B.box((0,-12-i*5,.006),(.07,1.2,.004),M('#F2EFE8',.6),0)
        for i in range(16):
            for s_ in (-1,1): palm(s_*8.2,-14-i*9,r.uniform(.95,1.2),i+90)
    return DR
