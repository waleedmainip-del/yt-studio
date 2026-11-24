# sets for "Match Day — Light Gayi": Waleed's lounge packed for the final (origin), the gali outside at night (x=60)
ASSET='/home/claude/match/assets/'
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
TVC=(0,3.42,1.75); TVW,TVH=2.6,1.46
SOFA_H=.47; FLOOR_H=.14; CHAIR_H=.5
# seats: (x,y,heading_deg,seat_h)  — heading 180 faces +y (the TV)
SEATS=dict(
 abbu=(-.3,-.55,180,SOFA_H), chacha=(.55,-.55,180,SOFA_H), phupha=(1.4,-.55,185,SOFA_H), sofa_l=(-1.15,-.55,175,SOFA_H),
 dada=(3.15,.3,225,CHAIR_H),
 l1=(-3.45,1.4,120,SOFA_H), l2=(-3.45,.55,125,SOFA_H), l3=(-3.45,-.3,135,SOFA_H),
 f1=(-1.6,1.2,180,FLOOR_H), f2=(-.75,1.35,185,FLOOR_H), f3=(1.3,1.3,175,FLOOR_H), f4=(2.1,1.15,165,FLOOR_H),
 c1=(-2.4,-1.9,165,CHAIR_H), c2=(-1.2,-2.0,180,CHAIR_H), c3=(.6,-2.05,180,CHAIR_H), c4=(1.8,-2.0,190,CHAIR_H), c5=(3.0,-1.8,200,CHAIR_H),
)
STAND=[(-3.0,-3.0,170),(-1.8,-3.1,180),(-.6,-3.15,182),(.6,-3.15,178),(1.8,-3.1,185),(3.2,-2.9,195),(3.6,-1.0,140)]
UPS=(2.3,3.1)
ALMARI=(3.95,-2.4)
def lounge():
    x0,x1=RMx; y0,y1=RMy; h=RH
    W_=M('#E8D4B0',.85,kind='wall'); W2=M('#C9A87A',.85,kind='wall')
    B.box((0,0,-.05),(x1+.2,y1+.2,.05),M('#B9A890',.4,kind='tile',spec=.5),0)
    B.box((0,-.2,.006),(2.6,1.8,.004),M('#7A1E2E',.9,kind='fabric'),0); B.box((0,-.2,.009),(2.3,1.5,.004),M('#C9A24A',.9,kind='fabric'),0); B.box((0,-.2,.012),(2.1,1.3,.004),M('#7A1E2E',.9,kind='fabric'),0)
    B.box((0,y1,h/2),(x1,.1,h/2),W2,0); B.box((x0,0,h/2),(.1,y1,h/2),W_,0); B.box((x1,0,h/2),(.1,y1,h/2),W_,0)
    B.box((-3.5,y0,h/2),(.7,.1,h/2),W_,0); B.box((1.1,y0,h/2),(3.1,.1,h/2),W_,0); B.box((-2.4,y0,2.85),(.4,.1,.45),W_,0)
    B.box((0,0,h+.05),(x1,y1,.05),M('#F4EBDD',.8),0)
    for (cx,cy,sx,sy) in ((0,y1-.12,x1,.02),(x0+.12,0,.02,y1),(x1-.12,0,.02,y1)): B.box((cx,cy,.07),(sx,sy,.07),M('#7A5236',.6),.01)
    # TV wall unit + giant TV + speakers + UPS & socket
    B.box((0,y1-.35,.3),(1.9,.3,.3),M('#5A3A26',.5,kind='wall'),.02); B.box((0,y1-.35,.62),(1.92,.32,.02),M('#3A2618',.4),.01)
    B.box((TVC[0],TVC[1]-.03,TVC[2]),(TVW/2+.05,.04,TVH/2+.05),M('#111216',.3),.02)
    TV=img_plane(TVW,TVH,img_mat('tv_score',1.0),(TVC[0],TVC[1]-.075,TVC[2]),(0,0,0))
    for s in (-1,1): B.box((s*1.65,y1-.35,.95),(.13,.13,.32),M('#1A1B22',.4),.02); B.cyl((s*1.65,y1-.49,1.0),.07,.01,M('#3A3B42',.4),rot=(R(90),0,0))
    B.box((UPS[0],UPS[1],.25),(.18,.3,.25),M('#2B2C33',.45),.02); UPSF=img_plane(.3,.4,img_mat('ups_dead',.6),(UPS[0],UPS[1]-.305,.3),(0,0,0))
    B.box((UPS[0]+.5,y1-.11,.45),(.07,.02,.07),M('#F4F5FA',.3),.01)
    PLUG=empty((UPS[0]+.5,y1-.16,.45)); obox((0,0,0),(.03,.04,.03),M('#1A1B22',.4),.01,PLUG)
    B.cyl((UPS[0]+.25,y1-.2,.3),.01,.5,M('#1A1B22',.4),rot=(0,R(90),R(30)),seg=6)
    # 3-seat sofa facing the TV + L sofa on the west + Dada's armchair + plastic chairs + floor cushions
    SOF=M('#6E1E2E',.8,kind='fabric'); SOF2=M('#8A2A3A',.8,kind='fabric')
    B.box((.15,-.75,.22),(1.75,.45,.22),SOF,.06); B.box((.15,-1.12,.7),(1.75,.12,.38),SOF,.06);
    for s in (-1,1): B.box((.15+s*1.82,-.75,.45),(.12,.45,.2),SOF,.06)
    for k in range(4): B.box((-1.15+k*.85,-.7,.46),(.4,.4,.04),SOF2,.05)
    B.box((-3.72,.55,.22),(.45,1.6,.22),SOF,.06); B.box((-4.02,.55,.7),(.12,1.6,.38),SOF,.06)
    for k in range(3): B.box((-3.67,1.4-k*.85,.46),(.4,.4,.04),SOF2,.05)
    B.box((3.25,.45,.25),(.45,.45,.25),M('#5A4030',.7,kind='fabric'),.08); B.box((3.55,.6,.7),(.12,.4,.4),M('#5A4030',.7,kind='fabric'),.06,rot=(0,0,R(-30)))
    for nm in ('c1','c2','c3','c4','c5'):
        x,y,hd,_=SEATS[nm]; a=R(hd);
        B.box((x,y,.46),(.27,.25,.03),M('#E8E2D6',.4),.02,rot=(0,0,a)); B.box((x-.0*math.sin(a),y-.0,.24),(.22,.2,.22),M('#E8E2D6',.4),.02,rot=(0,0,a))
        bx=x-.26*math.sin(a+pi); by=y+.26*math.cos(a+pi); B.box((bx,by,.78),(.25,.03,.3),M('#E8E2D6',.4),.02,rot=(0,0,a))
    for nm in ('f1','f2','f3','f4'): x,y,_,_=SEATS[nm]; B.box((x,y,.07),(.3,.3,.07),M(['#2F6FE0','#E8A33A','#2E6B4A','#C8102E'][hash(nm)%4],.8,kind='fabric'),.05)
    # coffee table with the pakora tray, chai cups, ketchup
    B.box((0,.45,.4),(.9,.4,.03),M('#5A3A26',.4,kind='wall'),.02)
    for s in (-1,1):
        for t_ in (-1,1): B.box((s*.8,.45+t_*.32,.2),(.03,.03,.2),M('#3A2618',.5),.005)
    B.cyl((0,.45,.45),.32,.03,M('#C9CDD6',.3,metal=.7),seg=24,rot=(0,0,0))
    PAK=[]
    for k in range(30):
        a=k*2.4; rr=.06+.21*math.sqrt((k+.5)/30); PAK.append(oico((math.cos(a)*rr,.45+math.sin(a)*rr,.5+.02*(k%3)),.045,M('#C98A2A',.7,kind='fabric'),sc=(1.1,1,.7)))
    for k in range(6): B.cyl((-.7+k*.25,.75,.47),.035,.07,M('#F4EBDD',.4),seg=10,rot=(0,0,0))
    B.cyl((.65,.2,.5),.04,.18,M('#C8102E',.5),seg=10,rot=(0,0,0))
    # almari (cupboard) with Dada's radio, wall clock, photo frames, Pakistan flag bunting, window, fan, tube light
    ax,ay=ALMARI; B.box((ax-.3,ay,1.05),(.3,.6,1.05),M('#6E4A30',.5,kind='wall'),.02); B.box((ax-.61,ay,1.05),(.01,.01,.95),M('#3A2618',.6),0)
    for k in range(5): B.box((-3.0+k*1.5,y1-.12,2.85),(.4,.01,.25),M(['#0B7A3B','#F4F5FA'][k%2],.8,kind='fabric'),0,rot=(0,R(8*(k%2*2-1)),0))
    for k in range(3): B.box((x0+.12,-1.6+k*.8,1.9),(.02,.28,.2),M('#C9A24A',.3,metal=.6),.01); B.box((x0+.135,-1.6+k*.8,1.9),(.005,.22,.15),M(['#7FA05A','#5A6E8C','#C98A6A'][k],.6),0)
    B.box((x1-.12,1.5,1.7),(.02,.7,.6),M('#F4F1EA',.5),.01); B.box((x1-.13,1.5,1.7),(.02,.62,.52),M('#13203A',.1,emit=.3),0)
    fan=empty((0,-.2,h-.25)); B.cyl((0,-.2,h-.1),.03,.2,M('#F4F1EA',.5),seg=8,rot=(0,0,0)); B.cyl((0,-.2,h-.25),.12,.1,M('#F4F1EA',.5),seg=14,rot=(0,0,0))
    for k in range(3): obox((math.cos(2*pi*k/3)*.48,math.sin(2*pi*k/3)*.48,0),(.48,.07,.008),M('#F4F1EA',.5),.01,fan,rot=(0,0,2*pi*k/3))
    TUBE=obox((-3.9,0,2.6),(.03,.6,.025),M('#F4FAFF',.2,emit=8),.01)
    plant(-3.6,2.9,1.1)
    Ls={}; Ls['tube']=area((-3.6,0,2.6),180,(.4,1.4),(.95,.98,1.0),rot=(0,R(-90),0)); Ls['fill']=area((0,-.5,h-.15),160,(5,5),(1,.92,.8)); Ls['tv']=area((0,2.6,1.6),120,(2.4,1.2),(.7,.85,1.0),rot=(R(90),0,0))
    return dict(tv=TV,ups=UPSF,plug=PLUG,pak=PAK,fan=fan,tube=TUBE,L=Ls)
def room_lights(D,on,tv=True):
    for k,a in D['L'].items():
        if 'e0' not in a: a['e0']=a.data.energy
        a.data.energy=a['e0'] if (on and (k!='tv' or tv)) else a['e0']*.0
    D['tube'].scale=(1,1,1) if on else (0,0,0)
# ================================================================ THE GALI at night (x=60): street along +x
GX=60
def gali():
    B.box((GX,0,-.05),(18,6,.05),M('#6E6A64',.85,kind='asphalt'),0); B.box((GX,0,.004),(18,.15,.004),M('#4A4640',.8),0)
    rnd=random.Random(3); cols=['#E8D4B0','#C9D6D2','#D9C3A5','#E4D4BC','#C9B79C','#B8C8D8']
    for s in (-1,1):
        for k in range(7):
            x=GX-15+k*5; c=cols[(k+(s>0)*3)%6]; B.box((x,s*5.6,3.2),(2.45,1.6,3.2),M(c,.85,kind='wall'),.02)
            B.box((x-.8,s*4.0,1.1),(.5,.04,1.0),M('#6E4A30',.5),.01); B.box((x+.9,s*4.0,1.6),(.55,.03,.45),M('#FFD58A',.2,emit=1.3 if rnd.random()<.7 else .1),0)
            B.box((x,s*4.0,6.45),(2.5,.2,.08),M('#B98A5A',.7),.01); B.box((x+.9,s*3.6,3.5),(.9,.4,.05),M('#9C968A',.8),.01)
            B.box((x,s*4.25,.18),(2.45,.25,.18),M('#9C968A',.8),.01)
    for k in range(-16,17):
        for j in range(5): B.ico((GX+k*1.1,-3.8+j*1.9,4.3-.35*math.sin(pi*j/4)),.06,M(['#FFE7B0','#7FE0A0','#FF8A80'][(k+j)%3],.2,emit=10),sub=1)
    for k in range(5): B.box((GX-10+k*5,0,5.2),(.008,4,.008),M('#1A1B22',.5),0)
    for k in range(-2,3): B.box((GX+k*7,-3.9,3.2),(.9,.02,.6),M('#0B7A3B',.8,kind='fabric'),0)
    area((GX,0,6),700,(30,7),(1,.85,.65)); area((GX,-3,3),120,(20,2),(.6,.7,1.0),rot=(R(40),0,0))
def dhol_obj():
    e=empty((0,0,0)); ocyl((0,0,0),.2,.55,M('#C8102E',.5),e,rot=(0,R(90),0),seg=18)
    for s in (-1,1): ocyl((s*.28,0,0),.21,.02,M('#E8DCC4',.6),e,rot=(0,R(90),0),seg=18)
    obox((0,0,.2),(.25,.01,.01),M('#F2C12E',.4),0,e); return e
def stick_obj():
    e=empty((0,0,0)); obox((0,0,0),(.012,.012,.2),M('#C9A27A',.6),.004,e); return e
def radio_obj():
    e=empty((0,0,0)); obox((0,0,0),(.22,.08,.13),M('#6E4A30',.45,kind='wall'),.03,e); ocyl((-.1,-.081,0),.07,.01,M('#C9C2B4',.6),e,seg=16)
    obox((.08,-.081,.03),(.08,.004,.04),M('#F2E2B0',.3,emit=.8),.005,e); ocyl((.16,0,.2),.006,.3,M('#C9CDD6',.3,metal=.8),e,rot=(R(-15),0,R(20)),seg=6); return e
def phone_obj(screen='ph_buffer'):
    e=empty((0,0,0)); obox((0,0,0),(.04,.007,.082),M('#15161A',.3),.006,e); sc=img_plane(.072,.148,img_mat(screen,1.2),(0,-.0075,0),(0,0,0),parent=e); return e,sc
def mithai_obj():
    e=empty((0,0,0)); obox((0,0,0),(.16,.12,.05),M('#F2C12E',.5),.01,e); obox((0,0,.052),(.165,.125,.006),M('#C8102E',.5),.005,e); return e
def tasbeeh_obj(n=14):
    e=empty((0,0,0)); beads=[]
    for k in range(n): a=2*pi*k/n; beads.append(oico((.06*math.cos(a),0,-.08+.06*math.sin(a)),.012,M('#2E6B4A',.3),e,sub=1))
    return e,beads
