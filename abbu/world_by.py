# sets for "Everyone Is Abbu": Waleed's lounge packed for the final (origin), the gali outside at night (x=60)
ASSET='/home/claude/abbu/assets/'
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
def plant(x,y,s=1.0,pot='#B5563A'):
    B.cyl((x,y,.22*s),.2*s,.44*s,M(pot,.8),seg=14,rot=(0,0,0))
    for j in range(6): B.ico((x+.16*s*math.cos(j*1.1),y+.16*s*math.sin(j*1.1),(.62+j*.07)*s),.19*s,LEAF[j%4],sub=1,sc=(1,1,.75))
# ================================================================ LOUNGE (origin): TV on the north wall
RMx=(-4.2,4.2); RMy=(-3.6,3.6); RH=3.3

def tree(x,y,h=4.2,s=1.0,seed=0):
    r=random.Random(seed); B.cyl((x,y,h*.4),.13*s,h*.8,M('#6E5038',.85,kind='bark'),seg=10,rot=(0,0,0))
    for k in range(7): B.ico((x+r.uniform(-.9,.9)*s,y+r.uniform(-.9,.9)*s,h*.78+r.uniform(-.3,.7)*s),r.uniform(.7,1.1)*s,LEAF[k%4],sub=2)
def face_sign(name,x,y,z,w,h,side,emit=.55):
    """sign on a wall facing +x (side=-1 wall at -x) or -x (side=+1)"""
    return img_plane(w,h,img_mat(name,emit),(x,y,z),(0,0,R(-90 if side>0 else 90)))
# ================================================================ 1. CITY MALL (origin): atrium along +y, shops both sides
MALL=(-7,7,-6,30)
def mall():
    x0,x1,y0,y1=MALL; yc=(y0+y1)/2; hy=(y1-y0)/2; h=8.0
    B.box((0,yc,-.05),(x1,hy,.05),M('#E8E2D6',.25,kind='tile',spec=.8),0)
    for k in range(int(y0),int(y1),2): B.box((0,k,.003),(1.6,.04,.003),M('#C9A27A',.4),0)
    B.box((0,yc,h+.05),(x1,hy,.05),M('#F4F5FA',.7),0); B.box((0,yc,h+.02),(2.2,hy-2,.03),M('#CFE8FF',.1,emit=1.0),0)
    B.box((0,y1,h/2),(x1,.1,h/2),M('#D9C3A5',.8,kind='wall'),0); B.box((0,y0,h/2),(x1,.1,h/2),M('#D9C3A5',.8,kind='wall'),0)
    SH=['s_style','s_shoes','s_phone','s_sweet','s_food','s_cinema']
    for s in (-1,1):
        B.box((s*(x1+.1),yc,h/2),(.1,hy,h/2),M('#E8DCC4',.8,kind='wall'),0)
        B.box((s*(x1-1.8),yc,4.05),(1.8,hy,.08),M('#C9CDD6',.3,metal=.5),.02)                       # mezzanine walkway
        B.box((s*(x1-3.55),yc,4.6),(.03,hy,.5),M('#BFD8E8',.05,spec=.9,alpha=.3),0); B.box((s*(x1-3.55),yc,5.12),(.05,hy,.03),M('#C9CDD6',.3,metal=.7),.01)
        for k,yy in enumerate(range(int(y0)+3,int(y1),7)):
            c=['#13203A','#6C3FA0','#2E6B4A','#E8A33A','#C8102E','#16171C'][(k+(s>0)*3)%6]
            B.box((s*(x1-.02),yy,1.5),(.04,2.9,1.5),M('#BFD8E8',.05,spec=.9,alpha=.35),0)
            B.box((s*(x1-.05),yy,3.3),(.08,3.0,.35),M(c,.5),.02); face_sign(SH[(k+(s>0)*2)%6],s*(x1-.14),yy,3.3,2.7,.66,s,.7)
            for j in range(4): B.box((s*(x1-.9),yy-1.6+j*1.05,.8),(.25,.35,.8),M(['#C8102E','#2F6FE0','#F2C12E','#7FA05A'][(j+k)%4],.6,kind='fabric'),.02)
            face_sign(SH[(k+(s>0)*4+1)%6],s*(x1-.14),yy,6.8,2.2,.55,s,.6)
        for yy in range(int(y0)+2,int(y1),6): B.cyl((s*(x1-3.6),yy,2.0),.18,4.0,M('#F4F5FA',.4),rot=(0,0,0),seg=16)
    # escalator (parked) + planters + banners + AC vents with the notice
    B.box((-1.2,22,2.0),(.6,4.2,.12),M('#9AA2AC',.3,metal=.7),.02,rot=(R(25),0,0)); B.box((-1.2,22,2.4),(.65,4.2,.35),M('#BFD8E8',.05,alpha=.3),0,rot=(R(25),0,0))
    for yy in (2,12): B.box((0,yy,.3),(1.2,.4,.3),M('#8A6A4A',.6,kind='wood'),.02); [B.ico((-.8+j*.4,yy,.75),.32,LEAF[j%4],sub=2) for j in range(5)]
    for k,yy in enumerate((5,15,25)): img_plane(2.6,.65,img_mat('s_mall',.6),(0,yy,6.4),(0,0,0)); B.box((0,yy+.02,6.4),(1.35,.01,.35),M('#16171C',.4),0)
    for yy in range(int(y0)+2,int(y1),5):
        for s in (-1,1): B.box((s*2.6,yy,h-.02),(.5,.25,.02),M('#9AA2AC',.4,metal=.5),.01); [B.box((s*2.6,yy-.18+j*.12,h-.045),(.45,.015,.005),M('#3A3B42',.4),0) for j in range(4)]
    img_plane(2.0,.72,img_mat('ac_off',.6),(-1.8,3.96,4.9),(0,0,0))
    B.box((-1.8,4.02,4.9),(1.05,.02,.4),M('#16171C',.4),0); B.cyl((-1.8,4.02,6.6),.02,3.0,M('#16171C',.4),rot=(0,0,0),seg=6)
    # store interior bits: clothing racks + cashier counter (east side, y 5..9)
    B.box((5.2,7.0,.55),(.5,1.2,.55),M('#F4F5FA',.3),.03); B.box((5.2,7.0,1.12),(.55,1.25,.03),M('#C9A27A',.4,kind='wood'),.01)
    B.box((5.2,7.45,1.25),(.15,.12,.12),M('#16171C',.4),.02)
    for j in range(5): B.box((3.6,4.2+j*.5,1.3),(.03,.2,.38),M(['#C8102E','#2F6FE0','#F2C12E','#7FA05A','#F4F5FA'][j],.7,kind='fabric'),.01)
    B.cyl((3.6,5.2,1.7),.02,2.4,M('#C9CDD6',.3,metal=.8),rot=(R(90),0,0),seg=8)
    for s in (-1,1): B.cyl((3.6,5.2+s*1.2,.85),.02,1.7,M('#C9CDD6',.3,metal=.8),rot=(0,0,0),seg=8)
    # ATM (west wall, y 11)
    B.box((-6.55,7.5,1.0),(.4,.45,1.0),M('#0B5A6E',.4),.03); B.box((-6.2,7.5,1.35),(.06,.36,.28),M('#16171C',.3),.01)
    ATM=img_plane(.6,.45,img_mat('atm1',1.0),(-6.13,7.5,1.38),(0,0,R(90))); B.box((-6.15,7.5,.95),(.08,.3,.08),M('#C9CDD6',.3,metal=.7),.01)
    B.box((-6.5,7.5,2.2),(.42,.48,.2),M('#062F3A',.4),.02)
    # food court tables (y 18..27)
    for i,(tx,ty) in enumerate(((1.2,17),(-1.6,17.5),(1.5,23.2),(-1.8,23.8))):
        B.cyl((tx,ty,.74),.55,.04,M('#F4F5FA',.3),rot=(0,0,0),seg=20); B.cyl((tx,ty,.37),.05,.74,M('#9AA2AC',.3,metal=.7),rot=(0,0,0),seg=10)
        for a in range(4): B.box((tx+.85*math.cos(a*pi/2),ty+.85*math.sin(a*pi/2),.45),(.2,.2,.03),M('#C8102E',.5),.02)
    area((0,yc,h-.3),1200,(12,hy*2),(1,.96,.9)); area((0,yc,4),200,(10,hy*2),(1,.95,.88))
    return dict(atm=ATM)
TABLE=(1.2,17)
# ================================================================ 2. BARBER (BX)  3. CINEMA (CX)
BX=150; CX=100
def barber():
    x=BX; hx,hy,h=3.0,2.6,3.0; W_=M('#F4EBDD',.85,kind='wall')
    B.box((x,0,-.05),(hx,hy,.05),M('#16171C',.3,kind='tile',spec=.7),0)
    for i in range(-3,3):
        for j in range(-3,3):
            if (i+j)%2==0: B.box((x+i*1.0+.5,j*.87+.43,.002),(.5,.435,.002),M('#F4F5FA',.3,kind='tile'),0)
    B.box((x,0,h+.05),(hx,hy,.05),M('#F4F5FA',.8),0); B.box((x,hy,h/2),(hx,.08,h/2),W_,0); B.box((x-hx,0,h/2),(.08,hy,h/2),W_,0); B.box((x+hx,0,h/2),(.08,hy,h/2),W_,0)
    B.box((x-1.8,-hy,h/2),(1.2,.08,h/2),W_,0); B.box((x+1.8,-hy,h/2),(1.2,.08,h/2),W_,0); B.box((x,-hy,2.7),(.6,.08,.3),W_,0)
    B.box((x,hy-.06,1.55),(2.0,.02,.6),M('#DDE6EE',.03,metal=1.0),.01); B.box((x,hy-.1,.85),(2.2,.18,.06),M('#7A5236',.5),.01)
    for k in range(6): B.cyl((x-1.6+k*.6,hy-.12,.98),.04,.2,M(['#2F6FE0','#C8102E','#F2C12E'][k%3],.3),rot=(0,0,0),seg=10)
    for s in (-1,1):
        cx=x+s*1.0; B.cyl((cx,1.4,.25),.25,.5,M('#C9CDD6',.3,metal=.8),rot=(0,0,0),seg=16); B.box((cx,1.4,.6),(.3,.3,.08),M('#7A1E2E',.5),.04); B.box((cx,1.08,1.05),(.3,.06,.45),M('#7A1E2E',.5),.04)
        for t_ in (-1,1): B.box((cx+t_*.32,1.4,.8),(.04,.28,.04),M('#C9CDD6',.3,metal=.8),.01)
    img_plane(.9,1.2,img_mat('poster',.4),(x-hx+.1,0,1.7),(0,0,R(-90)))
    img_plane(2.4,.6,img_mat('s_barber',.6),(x,-hy-.1,2.7),(0,0,0))
    B.cyl((x+hx-.12,-1.6,1.6),.08,1.0,M('#F4F5FA',.3),rot=(0,0,0),seg=14)
    for k in range(4): B.cyl((x+hx-.12,-1.6,1.25+k*.22),.085,.08,M('#C8102E',.3),rot=(R(15),0,0),seg=14)
    B.box((x-2.4,-1.4,.42),(.4,.8,.04),M('#2B2C33',.5),.02); B.box((x-2.75,-1.4,.75),(.05,.8,.3),M('#2B2C33',.5),.02)
    area((x,0,h-.1),260,(4,4),(1,.96,.9))
    return dict(chairs=[(x-1.0,1.4,180,.66),(x+1.0,1.4,180,.66)])
def cinema():
    x=CX; B.box((x,0,-.05),(7,8,.05),M('#2A1A1E',.8,kind='fabric'),0); B.box((x,0,6.05),(7,8,.05),M('#16171C',.8),0)
    for s in (-1,1): B.box((x+s*7,0,3),(.1,8,3),M('#3A1E24',.8,kind='fabric'),0)
    B.box((x,8,3),(7,.1,3),M('#16171C',.8),0); SCR=img_plane(9.0,3.94,img_mat('screen',.5),(x,7.85,3.2),(0,0,0))
    for r_ in range(7):
        yy=3.0-r_*1.1; zz=r_*.22
        B.box((x,yy-.3,zz/2),(6.5,.55,zz/2+.001),M('#2A1A1E',.8),0) if r_ else None
        for c in range(-5,6):
            if c==0: continue
            B.box((x+c*.62,yy,zz+.42),(.26,.24,.06),M('#9E1A2E',.7,kind='fabric'),.03); B.box((x+c*.62,yy-.26,zz+.78),(.26,.05,.34),M('#9E1A2E',.7,kind='fabric'),.03)
    for s in (-1,1):
        for k in range(4): B.box((x+s*6.9,-4+k*3,2.6),(.02,.15,.08),M('#FFD58A',.2,emit=4),.01)
    area((x,6.5,3.2),900,(9,4),(.75,.85,1.0),rot=(R(90),0,0)); area((x,0,5.8),120,(10,10),(1,.9,.8))
    return dict(screen=SCR,seat=lambda r_,c:(x+c*.62,3.0-r_*1.1,0,r_*.22+.47))
# ================================================================ 4. NIGHT ROAD (RX) with switch poles + the slow taxi
RX=200
def night_road():
    x=RX; B.box((x,20,-.06),(30,60,.05),M('#5A564E',.9,kind='ground'),0); B.box((x,20,-.005),(3.6,60,.01),M('#3A3836',.85,kind='asphalt'),0)
    for k in range(-30,80,6): B.box((x,k,.008),(.08,1.3,.004),M('#E8E2D6',.6),0)
    SH=['s_karyana','s_sweet','s_phone','s_hotel','s_shoes','s_style']; LIT=[]
    for s in (-1,1):
        B.box((x+s*4.7,20,.09),(1.1,60,.09),M('#8C8676',.85,kind='tile'),0)
        for k,yy in enumerate(range(-24,72,8)):
            c=['#C9B79C','#B8C8D8','#D9C3A5','#E4D4BC'][(k+(s>0))%4]; B.box((x+s*9.2,yy,3.5),(3.4,3.6,3.5),M(c,.85,kind='wall'),.02)
            B.box((x+s*5.82,yy,1.3),(.02,2.8,1.3),M('#FFD58A',.3,emit=.0),0)
            sg=face_sign(SH[(k+(s>0)*2)%6],x+s*5.75,yy,3.2,4.0,1.0,s,1.1); win=obox((x+s*5.81,yy,1.3),(.02,2.6,1.2),M('#FFE2A8',.3,emit=2.4),0)
            LIT.append(dict(y=yy,s=s,sign=sg,win=win,name=SH[(k+(s>0)*2)%6]))
            B.box((x+s*5.85,yy,5.0),(.03,2.4,.55),M('#2E3A4E',.1,spec=.9),0)
        for k,yy in enumerate(range(-22,72,8)):
            B.cyl((x+s*4.1,yy+4,3.0),.07,6.0,M('#5A5E66',.5,metal=.5),rot=(0,0,0),seg=8); B.box((x+s*3.6,yy+4,5.95),(.55,.05,.05),M('#5A5E66',.5,metal=.5),.01)
            lamp=obox((x+s*3.15,yy+4,5.88),(.22,.14,.06),M('#FFF2C8',.3,emit=6),.01); box=obox((x+s*4.1+(-.13 if s>0 else .13),yy+4,1.35),(.07,.12,.16),M('#C9CDD6',.4,metal=.5),.02)
            sw=empty((x+s*4.1+(-.21 if s>0 else .21),yy+4,1.38)); obox((0,0,0),(.015,.03,.05),M('#F4F5FA',.4),.005,sw)
            pl=point((x+s*3.0,yy+4,5.6),180,(1,.85,.6),.3,shadow=False)
            LIT.append(dict(y=yy+4,s=s,lamp=lamp,sw=sw,pl=pl,pole=(x+s*4.1,yy+4)))
    for k in range(-3,10): B.cyl((x,k*8,6.4),.012,9,M('#16171C',.6),rot=(0,R(90),0),seg=4)
    area((x,20,30),300,(40,80),(.5,.6,1.0))
    return LIT
def lit_set(e,on):
    if 'lamp' in e: e['lamp'].scale=(1,1,1) if on else (.0,.0,.0); e['pl'].data.energy=180 if on else 0; e['sw'].rotation_euler=(0,R(0 if on else 180),0)
    else: e['win'].scale=(1,1,1) if on else (0,0,0); e['sign'].data.materials[0]=img_mat(e['name'],1.1 if on else .05)
def taxi(x,y,rz=0):
    """yellow taxi with a real interior, faces +y, right-hand drive (same build as a family van, taxi livery)"""
    r=empty((x,y,0),rot=(0,0,R(rz)))
    BODY=M('#F2C12E',.25,metal=.3); GL=M('#BFD8E8',.05,spec=.9,alpha=.18); SEAT=M('#3A3B42',.7,kind='fabric'); DASH=M('#2A2C33',.55)
    TIRE=M('#111216',.8); RIM=M('#C9CDD6',.3,metal=.8); IN=M('#CFC6B8',.8,kind='fabric')
    W,Lf,Lr=1.2,2.45,-2.35
    obox((0,0,.12),(W-.04,2.3,.04),M('#3A3B42',.8),.01,r); obox((0,(Lf+Lr)/2,.52),(W,(Lf-Lr)/2,.3),BODY,.08,r); obox((0,Lf-.55,.86),(W,.55,.06),BODY,.06,r)
    for s in (-1,1):
        obox((s*W,-.6,2.22),(.05,1.7,.06),BODY,.03,r)
        for yy in (1.12,-.15,-2.28): obox((s*W,yy,1.55),(.05,.06,.72),BODY,.02,r)
        obox((s*(W+.005),-.5,1.55),(.012,1.8,.62),GL,0,r); obox((s*(W+.01),-.5,.6),(.005,2.2,.04),M('#16171C',.5),0,r)
    obox((0,-.6,2.3),(W,1.75,.05),BODY,.04,r); obox((0,-.6,2.24),(W-.06,1.7,.01),IN,0,r)
    obox((0,1.32,1.55),(W-.04,.02,.72),GL,0,r,rot=(R(-12),0,0)); obox((0,-2.32,1.55),(W-.04,.02,.66),GL,0,r,rot=(R(6),0,0)); obox((0,Lr,.6),(W,.04,.3),BODY,.03,r)
    img_plane(.7,.26,img_mat('taxi',.9),(0,-.6,2.52),(0,0,R(180)),parent=r); obox((0,-.6,2.52),(.37,.08,.14),M('#16171C',.5),.02,r); img_plane(.7,.26,img_mat('taxi',.9),(0,-.69,2.52),(0,0,0),parent=r)
    obox((0,1.02,.95),(W-.06,.2,.12),DASH,.05,r); obox((0,.92,.86),(W-.08,.08,.06),DASH,.03,r); obox((.3,1.0,1.1),(.12,.04,.05),M('#F2E2B0',.3,emit=1.0),.01,r)
    st=empty((.58,.82,1.0),r,rot=(R(62),0,0)); ocyl((0,0,0),.21,.035,M('#16171C',.4),st,seg=20); obox((0,0,0),(.2,.025,.015),M('#16171C',.4),.005,st)
    obox((0,1.15,2.12),(.14,.02,.05),M('#16171C',.4),.01,r)
    for s in (-1,1): obox((s*.58,.12,.37),(.36,.34,.08),SEAT,.05,r); obox((s*.58,-.26,.95),(.36,.08,.52),SEAT,.06,r,rot=(R(-8),0,0))
    obox((0,-1.5,.37),(1.0,.36,.08),SEAT,.05,r); obox((0,-1.89,.95),(1.0,.08,.52),SEAT,.06,r,rot=(R(-6),0,0))
    for yy in (1.55,-1.45):
        for s in (-1,1): ocyl((s*(W-.05),yy,.36),.36,.24,TIRE,r,rot=(0,R(90),0),seg=18); ocyl((s*(W+.07),yy,.36),.18,.02,RIM,r,rot=(0,R(90),0),seg=12)
    for s in (-1,1): obox((s*.75,Lf+.01,.62),(.2,.02,.07),M('#FFF2C8',.3,emit=3),.01,r); obox((s*.8,Lr-.03,.66),(.18,.02,.07),M('#E8303A',.3,emit=2.5),.01,r)
    return dict(root=r,steer=st,seats=dict(drv=(.58,.12),pas=(-.58,.12),back=(-.45,-1.5)),seat_h=.45)
def seat_world(C,key):
    lx,ly=C['seats'][key]; bpy.context.view_layer.update(); return C['root'].matrix_world@Vector((lx,ly,0))
def bike(x,y,col,rz=0):
    r=empty((x,y,0),rot=(0,0,R(rz))); T=M('#111216',.8)
    for yy in (.62,-.62): ocyl((0,yy,.32),.32,.09,T,r,rot=(0,R(90),0),seg=16)
    obox((0,0,.62),(.12,.55,.12),M(col,.3,metal=.4),.04,r); obox((0,-.2,.8),(.14,.32,.05),M('#1A1B22',.6),.03,r); obox((0,.62,.95),(.32,.03,.03),M('#2B2C33',.4),.01,r)
    return r
# ================================================================ 5. HOME (HX): Abbu's lounge — AC, four lights, switchboard
HX=300
def home():
    x=HX; hx,hy,h=3.4,2.8,3.0; W_=M('#E6CFC2',.85,kind='wall'); W2=M('#C9D6D2',.85,kind='wall')
    B.box((x,0,-.05),(hx,hy,.05),M('#B9A890',.4,kind='tile',spec=.5),0); B.box((x,0,h+.05),(hx,hy,.05),M('#F4F1EA',.8),0)
    B.box((x,hy,h/2),(hx,.08,h/2),W2,0); B.box((x-hx,0,h/2),(.08,hy,h/2),W_,0); B.box((x+hx,0,h/2),(.08,hy,h/2),W_,0)
    B.box((x-2.0,-hy,h/2),(1.4,.08,h/2),W_,0); B.box((x+2.2,-hy,h/2),(1.2,.08,h/2),W_,0); B.box((x+.2,-hy,2.7),(.6,.08,.3),W_,0)
    B.box((x,0,.007),(1.6,1.2,.005),M('#2E5A8C',.9,kind='fabric'),0); B.box((x,0,.011),(1.4,1.0,.004),M('#C9A24A',.9,kind='fabric'),0)
    SOF=M('#7A4A2E',.7,kind='fabric')                                         # sofa on the north wall, facing -y
    B.box((x,hy-.6,.22),(1.5,.45,.22),SOF,.06); B.box((x,hy-.18,.68),(1.5,.12,.38),SOF,.06)
    for s in (-1,1): B.box((x+s*1.6,hy-.6,.42),(.12,.45,.2),SOF,.06)
    for k in range(3): B.box((x-1.0+k*1.0,hy-.62,.47),(.45,.38,.04),M('#9A6A4A',.7,kind='fabric'),.05)
    B.box((x,.9,.35),(.7,.4,.025),M('#5A3A26',.4,kind='wood'),.02)
    for s in (-1,1):
        for t_ in (-1,1): B.box((x+s*.6,.9+t_*.32,.17),(.025,.025,.17),M('#3A2618',.5),.005)
    # split AC above the sofa
    B.box((x,hy-.13,2.45),(.55,.12,.16),M('#F4F5FA',.3),.04); B.box((x,hy-.26,2.36),(.5,.01,.03),M('#3A3B42',.4),0); B.box((x+.42,hy-.255,2.5),(.04,.005,.012),M('#22C55E',.3,emit=4),0)
    # four ceiling lights
    LT=[]
    for i,(lx,ly) in enumerate(((-1.6,-1.1),(1.6,-1.1),(-1.6,1.4),(1.6,1.4))):
        B.cyl((x+lx,ly,h-.02),.2,.04,M('#C9CDD6',.3,metal=.5),rot=(0,0,0),seg=16); bulb=oico((x+lx,ly,h-.1),.12,M('#FFF6E0',.2,emit=3),sub=2)
        pl=point((x+lx,ly,h-.35),120,(1,.9,.75),.2,shadow=(i==0)); LT.append((bulb,pl))
    # switchboard on the east wall
    B.box((x+hx-.1,-.8,1.3),(.02,.32,.2),M('#F4F5FA',.3),.01); SW=[]
    for k in range(4): e=empty((x+hx-.13,-1.0+k*.13,1.32)); obox((0,0,0),(.012,.035,.06),M('#E8E2D6',.4),.004,e); SW.append(e)
    B.box((x+hx-.13,-.8,1.17),(.01,.25,.02),M('#C8102E',.4,emit=.8),0)
    # TV on the south-east, clock, calendar, photos, window
    B.box((x+2.6,-2.55,.4),(.6,.22,.4),M('#4A2E1E',.5,kind='wood'),.02); B.box((x+2.6,-2.62,1.35),(.55,.03,.32),M('#111216',.3),.02)
    B.cyl((x-2.6,hy-.07,2.3),.2,.03,M('#F4F5FA',.4),rot=(R(90),0,0),seg=24); B.box((x-2.6,hy-.09,2.3),(.01,.01,.13),M('#16171C',.4),0)
    for k in range(3): B.box((x-hx+.1,-1.2+k*.8,1.8),(.02,.28,.22),M('#C9A24A',.3,metal=.6),.01); B.box((x-hx+.12,-1.2+k*.8,1.8),(.005,.22,.16),M(['#7FA05A','#5A6E8C','#C98A6A'][k],.6),0)
    B.box((x-hx+.08,1.6,1.6),(.02,.7,.6),M('#F4F1EA',.5),.01); B.box((x-hx+.09,1.6,1.6),(.02,.62,.52),M('#13203A',.1,emit=.4),0)
    plant(x+2.9,2.3,1.1); plant(x-2.9,-2.2,1.0)
    area((x,0,h-.1),70,(4,4),(1,.92,.8))
    return dict(lights=LT,sw=SW,sofa=(x,hy-.62,0,.47),board=(x+hx-.13,-.8,1.32))
def lights_set(D,mask):
    for (bulb,pl),on in zip(D['lights'],mask): bulb.scale=(1,1,1) if on else (.6,.6,.6); bulb.data.materials[0]=bulb.data.materials[0]; pl.data.energy=120 if on else 0
# ================================================================ props
def phone_obj(screen='ph_chat'):
    e=empty((0,0,0)); obox((0,0,0),(.04,.007,.082),M('#15161A',.3),.006,e); sc=img_plane(.072,.148,img_mat(screen,1.2),(0,-.0075,0),(0,0,0),parent=e); return e,sc
def shirt_obj():
    e=empty((0,0,0)); obox((0,0,0),(.24,.02,.3),M('#2F6FE0',.7,kind='fabric'),.02,e); obox((0,0,.31),(.04,.02,.04),M('#C9CDD6',.3,metal=.8),.005,e)
    for s in (-1,1): obox((s*.3,0,.12),(.08,.02,.16),M('#2F6FE0',.7,kind='fabric'),.02,e,rot=(0,R(s*30),0))
    img_plane(.12,.06,img_mat('tag',.6),(.16,-.025,-.18),(0,0,0),parent=e); return e
def tray_obj(kind='roti'):
    e=empty((0,0,0)); obox((0,0,0),(.24,.17,.012),M('#C8102E',.5),.008,e)
    ocyl((-.08,0,.03),.09,.03,M('#F4F5FA',.3),e,rot=(0,0,0),seg=16); ocyl((-.08,0,.045),.07,.01,M('#E8A33A',.6),e,rot=(0,0,0),seg=16)
    for k in range(3): ocyl((.11,0,.02+k*.012),.09,.01,M('#D9A65A',.7),e,rot=(0,0,0),seg=16)
    return e
def scissors_obj():
    e=empty((0,0,0))
    for s in (-1,1): obox((0,0,0),(.01,.004,.07),M('#C9CDD6',.25,metal=.9),.003,e,rot=(0,R(s*12),0))
    return e
def pizza_obj():
    e=empty((0,0,0)); obox((0,0,0),(.22,.22,.03),M('#E8DCC4',.7),.01,e); obox((0,0,.032),(.15,.15,.002),M('#C8102E',.5),0,e); return e
def specs_obj():
    e=empty((0,0,0))
    for s in (-1,1): obox((s*.06,0,0),(.045,.004,.03),M('#16171C',.3),.004,e)
    obox((0,0,.0),(.02,.004,.006),M('#16171C',.3),0,e); return e
