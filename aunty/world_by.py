# sets for "Everyone Is a Desi Aunty": Waleed's lounge packed for the final (origin), the gali outside at night (x=60)
ASSET='/home/claude/aunty/assets/'
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

def cone_(loc,r,h,mat,seg=8): B.cyl((loc[0],loc[1],loc[2]+h/2),r,h,mat,rot=(0,0,0),seg=seg,r2=0.0)
def tree(x,y,h=4.2,s=1.0,seed=0):
    r=random.Random(seed); B.cyl((x,y,h*.4),.13*s,h*.8,M('#6E5038',.85,kind='bark'),seg=10,rot=(0,0,0))
    for k in range(7): B.ico((x+r.uniform(-.9,.9)*s,y+r.uniform(-.9,.9)*s,h*.78+r.uniform(-.3,.7)*s),r.uniform(.7,1.1)*s,LEAF[k%4],sub=2)
def car(x,y,col,rz=0,parent=None):
    r=empty((x,y,0),rot=(0,0,R(rz)))
    if parent: r.parent=parent
    BODY=M(col,.25,metal=.4); GL=M('#22303E',.08,spec=.9); TIRE=M('#111216',.8); RIM=M('#B9C2CC',.3,metal=.8)
    obox((0,0,.62),(2.1,.92,.32),BODY,.08,r); obox((-.15,0,1.18),(1.25,.86,.28),BODY,.1,r); obox((-.15,0,1.18),(1.2,.88,.22),GL,.04,r)
    for sx in (-1.35,1.35):
        for sy in (-1,1): ocyl((sx,sy*.9,.34),.34,.2,TIRE,r,rot=(R(90),0,0),seg=16); ocyl((sx,sy*1.01,.34),.17,.02,RIM,r,rot=(R(90),0,0),seg=12)
    for sy in (-1,1): obox((2.11,sy*.6,.7),(.02,.18,.06),M('#FFF2C8',.3,emit=2),.01,r); obox((-2.11,sy*.6,.72),(.02,.18,.06),M('#E8303A',.3,emit=2.5),.01,r)
    return r
def bike(x,y,col,rz=0):
    r=empty((x,y,0),rot=(0,0,R(rz))); T=M('#111216',.8)
    for yy in (.62,-.62): ocyl((0,yy,.32),.32,.09,T,r,rot=(0,R(90),0),seg=16)
    obox((0,0,.62),(.12,.55,.12),M(col,.3,metal=.4),.04,r); obox((0,-.2,.8),(.14,.32,.05),M('#1A1B22',.6),.03,r); obox((0,.62,.95),(.32,.03,.03),M('#2B2C33',.4),.01,r)
    return r
# ================================================================ RICKSHAW with a real interior (faces +y locally)
def rickshaw(x,y,rz=0):
    r=empty((x,y,0),rot=(0,0,R(rz)))
    G=M('#0B7A3B',.35,metal=.2); Y=M('#F2C12E',.4); BK=M('#16171C',.6,kind='fabric'); SEAT=M('#7A1E2E',.7,kind='fabric'); CH=M('#C9CDD6',.3,metal=.8); T=M('#111216',.8)
    obox((0,-.15,.36),(.66,1.05,.04),M('#2B2C33',.7),.01,r)                 # floor
    obox((0,-.62,.5),(.68,.55,.16),G,.05,r)                                 # rear tub
    for s in (-1,1): obox((s*.68,-.62,.82),(.02,.5,.18),G,.02,r); obox((s*.685,-.62,.68),(.01,.5,.03),Y,0,r)
    obox((0,-1.16,.95),(.68,.02,.6),G,.02,r); obox((0,-1.18,.62),(.66,.01,.08),Y,0,r)
    obox((0,.62,.62),(.42,.45,.26),G,.08,r); obox((0,1.08,1.3),(.5,.03,.62),M('#BFD8E8',.05,spec=.9,alpha=.22),0,r)   # nose + windscreen
    obox((0,1.08,.66),(.44,.04,.2),Y,.03,r); obox((0,1.12,.75),(.12,.02,.06),M('#FFF2C8',.3,emit=2),.01,r)
    obox((0,-.08,2.42),(.72,1.18,.04),BK,.03,r)                              # canopy roof
    for s in (-1,1):
        for yy in (1.05,-.1,-1.15): ocyl((s*.69,yy,1.42),.022,2.0,CH,r,rot=(0,0,0),seg=8)
        obox((s*.7,-.6,2.32),(.01,.55,.08),M('#C8102E',.6,kind='fabric'),0,r)
    obox((0,.42,.72),(.2,.16,.06),SEAT,.04,r); obox((0,.42,.55),(.08,.1,.15),M('#2B2C33',.5),.02,r)   # driver seat
    obox((0,-.62,.7),(.62,.3,.06),SEAT,.04,r); obox((0,-.98,1.15),(.62,.06,.4),SEAT,.05,r)            # passenger bench
    hb=empty((0,.86,1.12),r); obox((0,0,0),(.34,.02,.02),CH,.01,hb); ocyl((0,0,-.2),.02,.4,CH,hb,rot=(R(-20),0,0),seg=8)
    for s in (-1,1): obox((s*.36,0,0),(.05,.03,.03),M('#16171C',.5),.01,hb)
    mir=empty((0,.98,2.05),r); obox((0,0,0),(.12,.015,.05),M('#16171C',.4),.01,mir); obox((0,-.016,0),(.11,.003,.042),M('#DDE6EE',.03,metal=1.0),0,mir)
    ocyl((0,1.0,1.95),.008,.25,M('#C9A24A',.3,metal=.6),r,rot=(0,0,0),seg=6); oico((0,1.0,1.8),.035,M('#C8102E',.4),r)
    ocyl((0,1.18,.28),.28,.12,T,r,rot=(0,R(90),0),seg=18)
    for s in (-1,1): ocyl((s*.74,-.65,.28),.28,.12,T,r,rot=(0,R(90),0),seg=18); ocyl((s*.81,-.65,.28),.13,.01,CH,r,rot=(0,R(90),0),seg=12)
    img_plane(.42,.14,img_mat('rplate',.3),(0,-1.19,.45),(0,0,0),parent=r)
    for k,c in enumerate(('#C8102E','#F2C12E','#2F6FE0','#F4F5FA')): obox((-.45+k*.3,-1.185,1.0),(.08,.004,.08),M(c,.4),0,r,rot=(0,R(45),0))
    return dict(root=r,hb=hb,mir=mir,seats=dict(drv=(0,.42,.78),back=(-.25,-.62,.76),back2=(.3,-.62,.76)))
def rk_world(K,lx,ly,lz):
    bpy.context.view_layer.update(); return K['root'].matrix_world@Vector((lx,ly,lz))
# ================================================================ 1. CITY ROAD (origin, road along +y)
ROADY=(-40,90)
def road():
    y0,y1=ROADY; yc=(y0+y1)/2; hy=(y1-y0)/2
    B.box((0,yc,-.06),(40,hy+20,.05),M('#8C8272',.9,kind='ground'),0)
    B.box((0,yc,-.005),(4,hy,.01),M('#4E4C4A',.85,kind='asphalt'),0)
    for k in range(int(y0),int(y1),6): B.box((0,k+1.5,.008),(.08,1.3,.004),M('#F4F1EA',.6),0)
    for s in (-1,1):
        B.box((s*5.1,yc,.09),(1.1,hy,.09),M('#B9B2A6',.85,kind='tile'),0); B.box((s*4.02,yc,.1),(.06,hy,.1),M('#E8E2D6',.7),0)
        for k in range(int(y0)+3,int(y1),5): B.box((s*4.02,k,.11),(.065,.5,.1),M('#111216',.7),0)
    SH=['shop_a','shop_b','shop_c','shop_d','shop_e','shop_f']; WC=['#E8D4B0','#C9D6D2','#D9C3A5','#F0E0C8','#C9B79C','#E6CFC2','#B8C8D8']
    rnd=random.Random(4); i=0
    for s in (-1,1):
        for y in range(y0+4,y1-2,7):
            c=WC[(i*3)%7]; hgt=rnd.choice([6.5,7.0,9.8]); cx=s*9.6; i+=1
            B.box((cx,y,hgt/2),(3.4,3.3,hgt/2),M(c,.85,kind='wall'),.02)
            B.box((s*6.21,y,1.3),(.02,2.6,1.3),M('#2B2420',.8),0)                      # shop opening (dark interior)
            for k in range(5): B.box((s*6.5,y-2+k*1.0,.6+.35*(k%2)),(.25,.4,.3+.2*(k%3)),M(['#C8102E','#F2C12E','#2F6FE0','#E8A33A','#7FA05A'][k],.6),.02)
            B.box((s*6.25,y,2.75),(.05,3.3,.12),M(shade(c,.7),.6),.02)
            img_plane(4.6,1.15,img_mat(SH[i%6],.55),(s*6.18,y,3.45),(0,0,R(-90 if s>0 else 90)))
            B.box((s*6.2,y,3.45),(.03,2.4,.66),M('#2B2C33',.6),.01)
            for fl in ([5.0] if hgt<8 else [5.0,7.8]):
                for dy in (-1.6,0,1.6): B.box((s*6.22,y+dy,fl),(.03,.45,.6),M('#3A4A5E',.15,spec=.9),.01); B.box((s*6.26,y+dy,fl-.65),(.06,.55,.05),M(shade(c,.75),.6),.01)
                B.box((s*6.4,y+1.6,fl-.2),(.25,.35,.22),M('#E8E2D6',.4),.02)
            B.box((cx,y,hgt+.1),(3.45,3.35,.1),M(shade(c,.8),.7),.01)
            for k in range(3): B.box((cx,y,hgt+.3+k*.25),(.02,.02,.12),M('#5A5550',.5),0) if k==0 else None
        for y in range(y0+6,y1,14):
            tree(s*5.4,y+3,h=4.6,s=.9,seed=y+(s>0)*100); B.box((s*5.4,y+3,.2),(.45,.45,.2),M('#9C968A',.8),.02)
        for y in range(y0+2,y1,12):
            B.cyl((s*4.4,y,3.2),.07,6.4,M('#5A5E66',.5,metal=.5),rot=(0,0,0),seg=8); B.box((s*3.8,y,6.3),(.65,.05,.05),M('#5A5E66',.5,metal=.5),.01); B.box((s*3.2,y,6.22),(.2,.12,.06),M('#FFF2C8',.3,emit=1.5),.01)
    for k in range(-3,13):                                                               # sagging wires across
        for j in range(3): B.cyl((0,k*7+2,6.6-.3*j),.012,13,M('#16171C',.6),rot=(0,R(90),0),seg=4)
    for y in (6,31,52): bike(5.0 if y!=31 else -5.0,y,['#C8102E','#16171C','#2F6FE0'][y%3],rz=8)
    # lassi stall + traffic post
    B.box((-5.3,22,.5),(.6,1.2,.5),M('#F4F5FA',.5),.03); B.box((-5.3,22,1.6),(.7,1.3,.04),M('#1E5AA8',.6,kind='fabric'),.02)
    for k in range(6): B.cyl((-5.0,21.4+k*.25,1.05),.05,.12,M('#FBF6E4',.3),seg=10,rot=(0,0,0))
    img_plane(1.8,.58,img_mat('lassi',.5),(-4.58,22,1.95),(0,0,R(90)))
    for k in range(2): B.cyl((-5.6,21.6+k*.8,1.2),.18,.4,M('#C9CDD6',.25,metal=.85),seg=14,rot=(0,0,0))
    B.cyl((-3.6,25.5,1.3),.03,2.6,M('#5A5E66',.5,metal=.5),rot=(0,0,0),seg=8); B.cyl((-3.6,25.5,2.6),1.1,.35,M('#F2C12E',.7,kind='fabric'),rot=(0,0,0),seg=10,r2=.05)
    img_plane(1.6,.4,img_mat('traffic',.4),(-3.6,24.9,2.1),(0,0,0))
    area((0,20,30),2000,(60,60),(1,.95,.88))
# ================================================================ 2. OFFICE: exterior gate (OX), waiting room (OX, WY), manager office (MX, WY)
OX=100; WY=40; MX=130
def office_ext():
    x=OX; B.box((x,10,-.06),(30,30,.05),M('#8C8272',.9,kind='ground'),0); B.box((x,-6,-.005),(30,3.5,.01),M('#4E4C4A',.85,kind='asphalt'),0)
    B.box((x,-1.4,.08),(30,1.1,.08),M('#B9B2A6',.85,kind='tile'),0)
    WL=M('#E4DCCC',.8,kind='wall')
    for s in (-1,1): B.box((x+s*9.3,1.0,1.0),(7.8,.15,1.0),WL,.02); B.box((x+s*1.6,1.0,1.4),(.3,.3,1.4),M('#C9B79C',.7,kind='wall'),.02); B.cyl((x+s*1.6,1.0,2.9),.22,.18,M('#FFF2C8',.3,emit=2),rot=(0,0,0),seg=12)
    for k in range(16): B.box((x-15+k*2,1.0,2.08),(.02,.02,.08),M('#5A5E66',.5,metal=.6),0) if abs(-15+k*2)>2 else None
    B.box((x,4.5,.06),(1.3,3.4,.06),M('#B9B2A6',.8,kind='tile'),0)                                       # path to door
    B.box((x,12,4.6),(9,4,4.6),M('#C9D6D2',.6,kind='wall'),.02)                                         # building
    for fl in (2.2,5.2,7.9):
        for k in range(-3,4):
            if fl<3 and abs(k)<1: continue
            B.box((x+k*2.4,7.98,fl),(.9,.03,.95 if fl<3 else 1.0),M('#2E4A66',.06,spec=.95),.01)
    B.box((x,7.98,1.3),(1.2,.04,1.3),M('#8FB8D8',.05,spec=.95,alpha=.5),0); B.box((x,7.95,2.65),(1.3,.06,.06),M('#5A5E66',.4,metal=.6),.01)
    B.box((x,7.9,3.35),(3.4,.08,.62),M('#13203A',.5),.02); img_plane(6.4,1.2,img_mat('office',.6),(x,7.83,3.35),(0,0,0))
    B.box((x,6.6,2.95),(1.8,1.4,.06),M('#C9CDD6',.3,metal=.6),.02)                                       # canopy
    for s in (-1,1): plant(x+s*2.2,7.4,1.2)
    # guard booth
    B.box((x+3.2,2.4,1.2),(.75,.75,1.2),M('#E8E2D6',.6,kind='wall'),.02); B.box((x+3.2,2.4,2.5),(.95,.95,.1),M('#9E3B4E',.6),.02); B.box((x+3.2,1.64,1.5),(.5,.02,.4),M('#2E4A66',.06,spec=.9),.01)
    for k,(dx,c) in enumerate(((-12,'#F4F5FA'),(-8,'#C8102E'),(8,'#2B2C33'),(12,'#2F6FE0'))): car(x+dx,4.6,c,rz=90)
    for k in range(-4,5): tree(x+k*6+3,-1.0 if k%2 else 18,h=4.8,s=1.0,seed=k+40) if k not in (0,) else None
    area((x,4,25),1800,(40,40),(1,.95,.88))
WROOM=(7,5,3.2)
def waiting_room():
    x,y=OX,WY; hx,hy,h=WROOM[0]/2,WROOM[1]/2,WROOM[2]
    W_=M('#DCE6E2',.85,kind='wall')
    B.box((x,y,-.05),(hx,hy,.05),M('#C9C2B4',.35,kind='tile',spec=.6),0); B.box((x,y,h+.05),(hx,hy,.05),M('#F4F5FA',.8),0)
    B.box((x,y+hy,h/2),(hx,.08,h/2),W_,0); B.box((x-hx,y,h/2),(.08,hy,h/2),W_,0); B.box((x+hx,y,h/2),(.08,hy,h/2),W_,0)
    B.box((x-2.2,y-hy,h/2),(1.3,.08,h/2),W_,0); B.box((x+2.2,y-hy,h/2),(1.3,.08,h/2),W_,0); B.box((x,y-hy,2.85),(.9,.08,.35),W_,0)
    B.box((x,y+hy-.05,.5),(hx,.03,.5),M('#5E8C9A',.6,kind='wall'),0)
    for k in range(5):                                                                              # chairs against the back wall
        cx=x-2.6+k*1.1; B.box((cx,y+hy-.55,.46),(.27,.25,.04),M('#2F6FA8',.5),.02); B.box((cx,y+hy-.3,.82),(.27,.04,.32),M('#2F6FA8',.5),.02)
        for s in (-1,1): B.box((cx+s*.22,y+hy-.55,.22),(.02,.2,.22),M('#5A5E66',.4,metal=.6),0)
    B.box((x+2.6,y-.6,.55),(.4,1.2,.55),M('#7A5236',.5),.02); B.box((x+2.6,y-.6,1.12),(.45,1.25,.03),M('#E8E2D6',.4),.01)        # reception desk
    B.box((x-3.2,y-1.6,.6),(.18,.18,.6),M('#F4F5FA',.4),.02); B.cyl((x-3.2,y-1.6,1.45),.17,.45,M('#8FC8F0',.1,alpha=.6),rot=(0,0,0),seg=14)
    plant(x-3.0,y+1.9,1.0); B.box((x,y+hy-.1,2.1),(.9,.02,.55),M('#13203A',.5),.01); B.box((x,y+hy-.12,2.1),(.82,.01,.47),M('#F2C12E',.6),0)
    B.box((x+2.0,y+hy-.1,2.2),(.3,.02,.3),M('#F4F5FA',.4),.01); B.box((x+2.0,y+hy-.12,2.2),(.24,.01,.24),M('#13203A',.4),0)
    B.box((x,y,h-.03),(.6,.25,.02),M('#F4FAFF',.2,emit=6),.01)
    return dict(seats=[(x-2.6+k*1.1,y+hy-.55,0,.5) for k in range(5)])
def manager_office():
    x,y=MX,WY; hx,hy,h=3.2,2.6,3.2; W_=M('#E8DCC4',.85,kind='wall')
    B.box((x,y,-.05),(hx,hy,.05),M('#8A6A4A',.4,kind='wood',spec=.5),0); B.box((x,y,h+.05),(hx,hy,.05),M('#F4F5FA',.8),0)
    B.box((x,y+hy,h/2),(hx,.08,h/2),M('#7A5236',.6,kind='wood'),0); B.box((x-hx,y,h/2),(.08,hy,h/2),W_,0); B.box((x+hx,y,h/2),(.08,hy,h/2),W_,0); B.box((x,y-hy,h/2),(hx,.08,h/2),W_,0)
    B.box((x,y+.9,.75),(1.3,.6,.04),M('#5A3A26',.4,kind='wood'),.02); B.box((x,y+1.45,.38),(1.25,.05,.36),M('#4A2E1E',.5,kind='wood'),.01)
    for s in (-1,1): B.box((x+s*1.2,y+.9,.37),(.05,.55,.37),M('#4A2E1E',.5,kind='wood'),.01)
    B.box((x,y+1.75,.5),(.3,.28,.06),M('#16171C',.5),.03); B.box((x,y+2.0,1.0),(.3,.06,.5),M('#16171C',.5),.04)   # manager chair
    for s in (-1,1): B.box((x+s*.55,y-.15,.46),(.25,.24,.04),M('#7A1E2E',.6,kind='fabric'),.03); B.box((x+s*.55,y-.38,.8),(.25,.04,.32),M('#7A1E2E',.6,kind='fabric'),.03)
    B.box((x+.75,y+.75,.8),(.14,.08,.02),M('#16171C',.4),.01); B.box((x+.75,y+.85,.98),(.2,.02,.14),M('#16171C',.3),.01)
    B.box((x-.8,y+.7,.81),(.25,.06,.04),M('#C9A24A',.3,metal=.7),.01)
    for k in range(4):                                                                                # bookshelf on the back wall
        B.box((x-2.3,y+2.35,.4+k*.55),(.7,.2,.02),M('#4A2E1E',.5),.01)
        for j in range(8): B.box((x-2.9+j*.17,y+2.35,.55+k*.55),(.06,.14,.13+.03*(j%3)),M(['#C8102E','#1E5AA8','#2E6B4A','#E8A33A','#6C3FA0'][(j+k)%5],.6),.005)
    B.box((x+2.2,y+2.52,1.8),(.7,.02,.55),M('#F4F5FA',.4),.01); B.box((x+2.2,y+2.5,1.8),(.62,.01,.47),M('#7FA05A',.6),0)
    B.box((x+hx-.05,y-.5,1.7),(.02,.9,.7),M('#BFE0FF',.1,emit=1.5),0)
    plant(x+2.6,y+1.9,1.0); B.box((x,y,h-.03),(.6,.25,.02),M('#F4FAFF',.2,emit=6),.01)
    return dict(desk_z=.79,boss=(x,y+1.68,0,.56),guest=(x+.55,y-.15,180,.5))
# ================================================================ 3. HOME STREET with opening windows (SX, lane along +y)
SX=200
def home_street(nwin=10):
    x=SX; B.box((x,20,-.06),(20,40,.05),M('#8C8272',.9,kind='ground'),0); B.box((x,20,-.005),(2.4,40,.01),M('#7A766E',.85,kind='asphalt'),0)
    for s in (-1,1): B.box((x+s*3.0,20,.06),(.6,40,.06),M('#B9B2A6',.85,kind='tile'),0)
    WC=['#F0E0C8','#C9D6D2','#E6CFC2','#D9C3A5','#E4DCCC','#C9E0D0','#F2D8B0']; WIN=[]
    for s in (-1,1):
        for k in range(8):
            y=-4+k*6.2; c=WC[(k*2+(s>0))%7]; fx=x+s*3.6; WM=M(c,.85,kind='wall'); TR=M(shade(c,.72),.6)
            B.box((x+s*7.05,y,3.4),(2.5,3.05,3.4),WM,.02); B.box((x+s*4.53,y,3.4),(.02,3.0,3.4),M('#7A6450',.9),0)     # body + dark interior face
            B.box((x+s*4.1,y,2.95),(.42,3.0,.05),M('#5A4636',.8),0); B.box((x+s*4.1,y,6.8),(.45,3.05,.05),WM,0)              # upper floor slab + roof edge
            for sy in (-1,1): B.box((x+s*4.1,y+sy*3.0,3.4),(.45,.05,3.4),WM,0)                                                   # party walls
            wy=y+.6
            B.box((x+s*3.7,(y-3.05+wy-.62)/2,3.4),(.06,(wy-.62-(y-3.05))/2,3.4),WM,.01); B.box((x+s*3.7,(wy+.62+y+3.05)/2,3.4),(.06,(y+3.05-wy-.62)/2,3.4),WM,.01)
            for z0,z1 in ((0,1.05),(2.45,4.0),(5.4,6.8)): B.box((x+s*3.7,wy,(z0+z1)/2),(.06,.62,(z1-z0)/2),WM,.01)
            B.box((x+s*3.64,y-1.9,1.1),(.02,.5,1.1),M('#6E4A30',.5,kind='wood'),.01)                      # door
            for fl,zc in ((0,1.75),(1,4.7)):
                WIN.append(dict(s=s,x=fx,y=wy,z=zc,fl=fl))
                B.box((x+s*3.66,wy,zc-.75),(.12,.75,.06),TR,.01); B.box((x+s*3.66,wy,zc+.75),(.12,.75,.06),TR,.01)
            B.box((x+s*3.75,y,3.15),(.14,3.0,.07),TR,.01); B.box((x+s*6.6,y,6.85),(3.0,3.1,.08),M(shade(c,.85),.7),.01)
            B.box((x+s*3.8,y-1.9,2.3),(.25,.6,.04),TR,.01); B.box((x+s*3.68,y+2.2,1.5),(.02,.25,.25),M('#2B2C33',.5),.005)
            if k%3==1: plant(x+s*3.25,y-1.0,.8)
            if k%2==0: B.box((x+s*3.9,y+.6,6.2),(.3,.6,.25),M('#E8E2D6',.4),.02)
    for k in range(-1,8):
        for j in range(4): B.ico((x+(j-1.5)*1.3,-4+k*6.2,5.9-.2*math.sin(j)),.05,M(['#FFE7B0','#7FE0A0','#FF8A80'][(k+j)%3],.2,emit=6),sub=1)
    for k in range(8): B.cyl((x,-4+k*6.2,6.0),.008,4.6,M('#16171C',.6),rot=(0,R(90),0),seg=4)
    tree(x-1.5,48,h=4.5,seed=7); tree(x+1.6,-9,h=4.5,seed=8)
    area((x,20,25),1500,(30,60),(1,.92,.8))
    return WIN
def shutters(w):
    """two wooden shutters hinged at the window edges; returns (left,right) empties to rotate"""
    s=w['s']; out=[]
    for side in (-1,1):
        hp=empty((w['x']-s*.0,w['y']+side*.62,w['z']))
        obox((0,-side*.31,0),(.025,.3,.68),M('#5E8C6A',.6,kind='wood'),.01,hp); obox((s*.03,-side*.31,0),(.01,.24,.6),M('#4A7A58',.6,kind='wood'),.005,hp)
        out.append((hp,side))
    return out
def shutters_set(SHU,s,k):
    for hp,side in SHU: hp.rotation_euler=(0,0,R(-s*side*100*k))
# ================================================================ 4. WALEED'S HOME (LX): small teal sitting room, TV on the east wall
LX=300
def living():
    x=LX; hx,hy,h=3.0,2.6,3.0; W_=M('#9CC8C0',.85,kind='wall'); W2=M('#E8DCC4',.85,kind='wall')
    B.box((x,0,-.05),(hx,hy,.05),M('#C9B496',.4,kind='tile',spec=.5),0); B.box((x,0,h+.05),(hx,hy,.05),M('#F4F1EA',.8),0)
    B.box((x,hy,h/2),(hx,.08,h/2),W_,0); B.box((x-hx,0,h/2),(.08,hy,h/2),W_,0); B.box((x+hx,0,h/2),(.08,hy,h/2),W2,0); B.box((x,-hy,h/2),(hx,.08,h/2),W_,0)
    B.box((x-.2,.1,.007),(1.4,1.0,.006),M('#B5563A',.9,kind='fabric'),0); B.box((x-.2,.1,.011),(1.2,.8,.004),M('#E8C25A',.9,kind='fabric'),0)
    SOF=M('#3A5A8C',.8,kind='fabric')                                                                  # sofa against the west wall, facing +x (TV)
    B.box((x-2.35,.1,.22),(.42,1.3,.22),SOF,.06); B.box((x-2.72,.1,.68),(.1,1.3,.36),SOF,.06)
    for s in (-1,1): B.box((x-2.35,.1+s*1.38,.42),(.42,.1,.2),SOF,.05)
    for k in range(3): B.box((x-2.32,-.72+k*.82,.47),(.38,.38,.04),M('#4A6A9C',.8,kind='fabric'),.05)
    B.box((x-.9,.1,.32),(.45,.7,.025),M('#6E4A30',.4,kind='wood'),.02)
    for s in (-1,1):
        for t_ in (-1,1): B.box((x-.9+s*.38,.1+t_*.6,.15),(.025,.025,.15),M('#4A2E1E',.5),.005)
    B.cyl((x-.75,.3,.4),.06,.12,M('#F4EBDD',.4),seg=12,rot=(0,0,0)); B.box((x-1.05,-.15,.37),(.12,.08,.02),M('#16171C',.4),.01)
    B.box((x+2.7,.1,.35),(.25,1.0,.35),M('#4A2E1E',.5,kind='wood'),.02)                                # TV unit (east wall)
    B.box((x+2.85,.1,1.45),(.04,.92,.54),M('#111216',.3),.02); TV=img_plane(1.76,.99,img_mat('tv_off',.2),(x+2.8,.1,1.45),(0,0,R(90)))
    B.box((x-2.92,.1,1.85),(.02,.75,.5),M('#C9A24A',.3,metal=.6),.01); B.box((x-2.9,.1,1.85),(.01,.68,.43),M('#7FA05A',.6),0)
    B.box((x+.8,hy-.05,1.55),(.75,.03,.6),M('#F4F1EA',.5),.01); B.box((x+.8,hy-.06,1.55),(.68,.01,.53),M('#BFE0FF',.1,emit=1.3),0)
    for s in (-1,1): B.box((x+.8+s*.95,hy-.12,1.55),(.2,.04,.95),M('#C8102E',.8,kind='fabric'),.02)
    B.cyl((x+1.6,-hy+.1,2.2),.18,.03,M('#F4F5FA',.4),rot=(R(90),0,0),seg=24); B.box((x+1.6,-hy+.12,2.2),(.01,.01,.12),M('#16171C',.4),0)
    plant(x+2.5,-2.1,1.0); plant(x-2.5,2.1,.9)
    B.cyl((x,0,h-.12),.03,.2,M('#F4F1EA',.5),seg=8,rot=(0,0,0)); fan=empty((x,0,h-.27))
    for k in range(3): obox((math.cos(2*pi*k/3)*.45,math.sin(2*pi*k/3)*.45,0),(.45,.06,.008),M('#F4F1EA',.5),.01,fan,rot=(0,0,2*pi*k/3))
    area((x,0,h-.1),220,(4,4),(1,.92,.82)); area((x+2.4,.1,1.4),60,(1.6,1.0),(.7,.85,1.0),rot=(0,R(-90),0))
    return dict(tv=TV,fan=fan,sofa=[(x-2.3,-.72+k*.82,90,.47) for k in range(3)])
# ================================================================ 5. NEWS STUDIO (NX) and 6. PM OFFICE (PX)
NX=400; PX=500
def studio():
    x=NX; B.box((x,0,-.05),(6,5,.05),M('#1A2238',.3,spec=.7),0)
    img_plane(7.5,2.35,img_mat('studio_wall',1.0),(x,3.0,2.0),(0,0,0))
    B.box((x,3.1,2.0),(3.9,.05,1.3),M('#0E1426',.4),.01)
    B.box((x,.6,.55),(1.6,.5,.55),M('#E8E2D6',.3,spec=.7),.04); B.box((x,.6,1.12),(1.7,.6,.03),M('#C9CDD6',.2,metal=.6),.02)
    img_plane(2.6,.49,img_mat('lower',.9,clip=True),(x,.08,.6),(0,0,0))
    B.box((x,1.55,.5),(.3,.28,.06),M('#16171C',.5),.03); B.box((x,1.8,1.0),(.3,.06,.5),M('#16171C',.5),.04)
    for s in (-1,1): B.box((x+s*3,2.5,2.0),(.05,.05,2.0),M('#2B2C33',.4,metal=.6),0); B.box((x+s*2.5,1.0,3.6),(.3,.3,.2),M('#16171C',.4),.03)
    area((x,-2,3.5),500,(4,2),(1,.97,.94),rot=(R(55),0,0)); area((x,3,4),200,(6,1),(.6,.7,1.0),rot=(R(-30),0,0))
    return dict(seat=(x,1.55,0,.56))
def pm_office():
    x=PX; hx,hy,h=4.0,3.2,3.8; W_=M('#E8DCC4',.8,kind='wall'); WD=M('#6E4A30',.45,kind='wood')
    B.box((x,0,-.05),(hx,hy,.05),M('#7A1E2E',.9,kind='fabric'),0); B.box((x,0,h+.05),(hx,hy,.05),M('#F4F1EA',.8),0)
    B.box((x,hy,h/2),(hx,.08,h/2),WD,0); B.box((x-hx,0,h/2),(.08,hy,h/2),W_,0); B.box((x+hx,0,h/2),(.08,hy,h/2),W_,0); B.box((x,-hy,h/2),(hx,.08,h/2),W_,0)
    for k in range(-3,4): B.box((x+k*1.1,hy-.1,h/2),(.04,.04,h/2),M('#4A2E1E',.5),0)
    B.box((x,1.1,.78),(1.6,.75,.05),M('#4A2E1E',.35,kind='wood',spec=.6),.03); B.box((x,1.8,.4),(1.55,.05,.38),WD,.01)
    for s in (-1,1): B.box((x+s*1.5,1.1,.38),(.06,.7,.38),WD,.01)
    B.box((x,2.0,.55),(.42,.38,.07),M('#7A1E2E',.6,kind='fabric'),.04); B.box((x,2.35,1.3),(.42,.08,.85),M('#7A1E2E',.6,kind='fabric'),.06)   # high-back chair
    # flag on a stand (behind, right)
    B.cyl((x+1.9,2.4,1.4),.025,2.8,M('#C9A24A',.3,metal=.7),rot=(0,0,0),seg=8)
    B.box((x+2.35,2.4,2.3),(.12,.01,.42),M('#F4F5FA',.6,kind='fabric'),0); B.box((x+2.95,2.4,2.3),(.48,.01,.42),M('#0B5A2E',.6,kind='fabric'),0)
    B.ico((x+2.9,2.385,2.33),.17,M('#F4F5FA',.6),sub=2,sc=(1,.05,1)); B.ico((x+2.97,2.38,2.36),.15,M('#0B5A2E',.6),sub=2,sc=(1,.05,1))
    B.box((x-1.9,2.5,1.0),(.6,.3,1.0),WD,.02)
    for k in range(4):
        for j in range(6): B.box((x-2.35+j*.18,2.4,.45+k*.45),(.06,.14,.15),M(['#7A1E2E','#13203A','#2E6B4A'][(j+k)%3],.6),.005)
    B.box((x,1.0,.86),(.2,.14,.04),M('#C9A24A',.3,metal=.7),.01); B.box((x-.8,1.2,.86),(.25,.18,.02),M('#F4F5FA',.4),.01)
    B.box((x+hx-.05,0,1.9),(.02,1.0,1.1),M('#BFE0FF',.1,emit=1.6),0)
    for s in (-1,1): B.box((x+hx-.1,s*1.1,1.9),(.04,.12,1.5),M('#C9A24A',.6,kind='fabric'),.02)
    area((x,0,h-.1),260,(5,5),(1,.93,.85)); area((x+3,0,2),120,(1,2),(1,.95,.88),rot=(0,R(-90),0))
    return dict(seat=(x,2.0,0,.6))
# ================================================================ props
def phone_obj(screen='gps1'):
    e=empty((0,0,0)); obox((0,0,0),(.04,.007,.082),M('#15161A',.3),.006,e); sc=img_plane(.072,.148,img_mat(screen,1.2),(0,-.0075,0),(0,0,0),parent=e); return e,sc
def glass_obj():
    e=empty((0,0,0)); ocyl((0,0,0),.045,.16,M('#FBF6E4',.3),e,rot=(0,0,0),seg=14); ocyl((0,0,.085),.047,.01,M('#F4F5FA',.2),e,rot=(0,0,0),seg=14); return e
def paper_obj(name,w=.21,h=.3):
    e=empty((0,0,0)); img_plane(w,h,img_mat(name,.35),(0,0,0),(0,0,0),parent=e); return e
def tiffin_obj():
    e=empty((0,0,0))
    for k in range(3): ocyl((0,0,k*.07),.09,.065,M('#C9CDD6',.25,metal=.85),e,rot=(0,0,0),seg=16)
    obox((0,0,.2),(.02,.08,.04),M('#C9CDD6',.25,metal=.85),.01,e); return e
def egg_obj():
    e=empty((0,0,0)); oico((0,0,0),.035,M('#F4F1EA',.4),e,sc=(.8,.8,1.05)); return e
def plate_obj():
    e=empty((0,0,0)); ocyl((0,0,0),.15,.02,M('#F4F5FA',.3),e,rot=(0,0,0),seg=20)
    for k in range(3): ocyl((.0,.0,.015+k*.012),.11,.01,M('#D9A65A',.7),e,rot=(0,0,0),seg=16)
    return e
def whistle_obj():
    e=empty((0,0,0)); obox((0,0,0),(.03,.012,.012),M('#C9CDD6',.25,metal=.85),.006,e); return e
