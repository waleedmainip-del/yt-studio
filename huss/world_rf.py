# sets for "Huss Huss": downtown avenue (+ small park) and Huss's apartment
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=True):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot; a.data.use_shadow=shadow; return a
def spot(loc,tg,e,col=(1,1,1),ang=60,blend=.5,r=.1):
    bpy.ops.object.light_add(type='SPOT',location=loc); s=bpy.context.object; s.data.energy=e; s.data.color=col; s.data.spot_size=R(ang); s.data.spot_blend=blend; s.data.shadow_soft_size=r
    d=Vector(tg)-Vector(loc); s.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); return s
def setup_dark(sky='#0A0F1E',strength=.25,res=100,samples=None,bloom=.06):
    sc=bpy.context.scene; w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']
    bg.inputs[0].default_value=hexc(sky); bg.inputs[1].default_value=strength
    sc.render.resolution_x=1080; sc.render.resolution_y=1920; sc.render.resolution_percentage=res; sc.render.engine='BLENDER_EEVEE'; e=sc.eevee
    e.taa_render_samples=samples or SAMPLES; e.use_gtao=True; e.gtao_distance=.8; e.gtao_factor=1.2; e.use_soft_shadows=True; e.use_bloom=True; e.bloom_intensity=bloom; e.bloom_threshold=1.0
    e.shadow_cascade_size='2048'; e.shadow_cube_size='1024'; e.use_shadow_high_bitdepth=True; e.light_threshold=.02
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='Medium High Contrast'; return w,bg
def seg(a,b,r,mat,sides=8):
    a=Vector(a); b=Vector(b); d=b-a; c=(a+b)/2; rot=d.to_track_quat('Z','Y').to_euler(); B.cyl(tuple(c),r,d.length,mat,rot=tuple(rot),seg=sides)
LEAF=M('#3E8E4A',.7,kind='leaves'); LEAF2=M('#5FA84A',.7,kind='leaves'); TRUNK=M('#6B4A30',.8,kind='wood')
def tree(x,y,z,s,seed):
    r=random.Random(seed); B.cyl((x,y,z+1.1*s),.14*s,2.2*s,TRUNK,seg=8)
    for i in range(4): B.ico((x+r.uniform(-.5,.5)*s,y+r.uniform(-.5,.5)*s,z+(2.4+r.uniform(0,.8))*s),(.8+r.random()*.35)*s,LEAF if i%2 else LEAF2,sc=(1,1,.85),sub=1)
FAC=['#C9B79C','#B8C4CC','#D9C2A8','#9CA8B8','#E0D6C4','#A8B0A0','#C2A894','#8E98A8']
def building(x,yface,side,w,d,h,col,seed,shop=True):
    """side=+1 building north of road (face at y=yface looking -y), -1 south"""
    r=random.Random(seed); cm=M(col,.75,kind='wall'); yc=yface+side*d/2; fy=yface-side*.01
    B.box((x,yc,h/2),(w/2,d/2,h/2),cm,.03)
    GL=M('#5E7A94',.15,spec=.9); LIT=M('#FFE7B8',.3,emit=1.4); FR=M(shade(col,.7),.6)
    for k in range(1,int(h/3.2)):
        z=k*3.2+1.2
        if z>h-1: break
        for i in range(int(w/2.2)):
            xx=x-w/2+1.1+i*2.2
            B.box((xx,fy,z),(.75,.02,.85),LIT if r.random()<.22 else GL,0); B.box((xx,fy-side*.03,z-.92),(.85,.06,.05),FR,.01)
    B.box((x,fy-side*.05,h+.1),(w/2+.1,.12,.12),FR,.02)
    if shop:
        sc=r.choice(['#C9452E','#2B58C9','#35975A','#E6A31C','#7448C2','#16909E'])
        B.box((x,fy-side*.02,1.5),(w/2-.4,.03,1.2),M('#9FC7D8',.08,spec=1.0),0)
        B.box((x,fy-side*.25,3.0),(w/2-.2,.3,.08),M(sc,.6),.02,rot=(R(-12*side),0,0))
        B.box((x,fy-side*.06,3.45),(w/2-.6,.05,.28),M(sc,.5,emit=.4),.02)
CLEARP=[False]
def street(night=False):
    ROAD=M('#3A3D44',.85,kind='asphalt'); SW=M('#B9B4AA',.7,kind='concrete',sc=1.2); CURB=M('#9A968E',.6); LINE=M('#F2F0E6',.5); YEL=M('#F2C12E',.5)
    B.box((0,0,-.05),(80,4,.05),ROAD,0)
    for s in (-1,1): B.box((0,s*5.5,.07),(80,1.5,.07),SW,0); B.box((0,s*4.02,.08),(80,.06,.08),CURB,.01)
    for x in range(-78,80,6): B.box((x,0,.003),(1.5,.08,.003),YEL,0)
    for i in range(10): B.box((-2+i*0,0,0),(0,0,0),LINE,0) if False else None
    for i in range(9): B.box((0,-3.6+i*.9,.004),(1.6,.3,.004),LINE,0)
    r=random.Random(5); x=-70; k=0
    while x<70:
        w=r.uniform(7,12)
        for side in (-1,1):
            if side==-1 and 18<x<38: continue        # park gap on the south side
            building(x+w/2,side*7.0,side,w,r.uniform(8,14),r.uniform(14,36),r.choice(FAC),k*3+side)
        x+=w+.3; k+=1
    # far skyline
    for i in range(30):
        xx=r.uniform(-90,90); yy=r.choice((-1,1))*r.uniform(26,60); h=r.uniform(30,80); B.box((xx,yy,h/2),(r.uniform(4,8),r.uniform(4,8),h/2),M(r.choice(FAC),.7,kind='wall'),0)
    # street furniture
    for x in range(-60,62,12):
        for s in (-1,1):
            B.cyl((x,s*4.5,2.4),.07,4.8,M('#2B313A',.4,metal=.7),seg=8); seg((x,s*4.5,4.75),(x,s*3.6,4.75),.05,M('#2B313A',.4,metal=.7)); B.box((x,s*3.5,4.7),(.25,.15,.06),M('#FFF1D0',.3,emit=(4.0 if night else .6)),.02)
            if not(18<x<38 and s==-1): tree(x+6,s*5.9,.14,.85,int(x*7+s))
    # bus stop + bins + hydrants
    B.box((8,6.4,1.2),(1.6,.04,1.1),M('#9FC7D8',.08,spec=1.0,alpha=.4),0); B.box((8,5.9,2.35),(1.8,.6,.06),M('#2B313A',.4,metal=.6),.02)
    for x in (-14,5,26,44):
        B.cyl((x,-4.6,.45),.22,.7,M('#2E7D5A',.5),seg=12); B.cyl((x+1.2,4.7,.35),.12,.5,M('#C9302C',.4),seg=10)
    # park (south side gap)
    GR=M('#5E9E40',.85,kind='grass',h2='#4A8A34')
    B.box((28,-14,.06),(10,7,.06),GR,0)
    for i in range(9):
        tx,ty=r.uniform(19,37),r.uniform(-9,-20); ts=r.uniform(1.0,1.4)
        if CLEARP[0] and math.hypot(tx-28,ty+14)<8: continue
        tree(tx,ty,.1,ts,i+500)
    for x in (24,30): B.box((x,-8.6,.45),(1.2,.3,.05),M('#8A5A3A',.6,kind='wood',sc=3),.02); B.box((x,-8.85,.75),(1.2,.05,.3),M('#8A5A3A',.6,kind='wood',sc=3),.02); B.box((x,-8.6,.22),(1.1,.25,.22),M('#3E4652',.5,metal=.6),.02)
    B.cyl((32,-15,.4),1.6,.8,M('#BDB5A6',.7,kind='concrete',sc=.5),seg=24); B.cyl((32,-15,.78),1.4,.04,M('#5EB6E0',.1,emit=.3,spec=1.0),seg=24)
    # parked cars
    for x,s,c in ((-22,1,'#2B58C9'),(-8,-1,'#E8E4D8'),(14,1,'#3A3D47'),(46,-1,'#C9452E')): car(x,s*3.1,c,rz=0)
    B.done('street')
def car(x,y,col,rz=0,sport=False,police=False,parent=None):
    r=empty((x,y,0),rot=(0,0,R(rz))) if parent is None else parent
    BODY=M(col,.25,metal=.4); GL=M('#22303E',.05,spec=1.0); TIRE=M('#111216',.8); RIM=M('#B9C2CC',.3,metal=.8)
    L,W=(2.3,1.0) if not sport else (2.4,1.05)
    obox((0,0,.55),(L,W,.32 if not sport else .26),BODY,.08,r)
    if sport: obox((-.2,0,.95),(1.0,.85,.18),GL,.12,r,rot=(0,R(-6),0)); obox((L-.05,0,.62),(.05,.8,.06),M('#FFF2C8',.3,emit=6),.01,r); obox((-L-.02,0,.9),(.06,.95,.04),BODY,.01,r)
    else: obox((-.2,0,1.12),(1.3,.92,.3),BODY,.1,r); obox((-.2,0,1.12),(1.25,.94,.24),GL,.04,r); obox((L+.02,.6,.6),(.03,.2,.08),M('#FFF2C8',.3,emit=4),.01,r); obox((L+.02,-.6,.6),(.03,.2,.08),M('#FFF2C8',.3,emit=4),.01,r)
    if police:
        obox((-.1,0,1.45),(.25,.7,.06),M('#22242B',.4),.02,r); obox((-.1,.38,1.53),(.2,.28,.06),M('#2050FF',.3,emit=6),.02,r); obox((-.1,-.38,1.53),(.2,.28,.06),M('#FF2A2A',.3,emit=6),.02,r)
        obox((0,0,.55),(L+.01,W+.01,.08),M('#1B2A4A',.4),.02,r)
    for sx in (-1.45,1.45):
        for sy in (-1,1): ocyl((sx,sy*(W-.02),.34),.34,.24,TIRE,r,rot=(R(90),0,0),seg=16); ocyl((sx,sy*(W+.1),.34),.17,.02,RIM,r,rot=(R(90),0,0),seg=12)
    return r

def apartment():
    """bedroom (x<0), bathroom (x 0..3), kitchen (x 3..7). all face -y. night, moonlight"""
    FLR=M('#6B5644',.6,kind='wood',sc=1.5); WALL=M('#3E4A5E',.85,kind='wall'); WALL2=M('#E3DED4',.8,kind='wall'); TILE=M('#DCE6E8',.3,kind='tile',h2='#BFD0D4',sc=3)
    B.box((0,0,-.05),(8,3,.05),FLR,0); B.box((0,2.6,1.6),(8,.05,1.6),WALL,0)
    for x in (-.05,3.0): B.box((x,1.2,1.6),(.05,1.4,1.6),WALL2,0)
    B.box((1.5,2.55,1.6),(1.45,.02,1.6),TILE,0)
    # bedroom: bed, nightstand, clock, window w/ city lights, poster of himself
    B.box((-2.6,1.4,.3),(1.1,1.0,.3),M('#2B2C33',.6),.04); B.box((-2.6,1.4,.62),(1.0,.95,.08),M('#E8E4D8',.9,kind='fabric'),.04); B.box((-2.6,.9,.7),(1.0,.45,.1),M('#1E2A4A',.9,kind='fabric'),.05)
    B.box((-2.6,2.25,.9),(1.1,.1,.6),M('#2B2C33',.6),.03); B.box((-2.6,2.1,.75),(.4,.18,.08),M('#F2F0E6',.9,kind='fabric'),.05)
    B.box((-1.15,2.0,.3),(.3,.3,.3),M('#4A3A2E',.6,kind='wood'),.02)
    B.box((-1.15,1.9,.72),(.2,.08,.12),M('#15161A',.4),.02)
    text('3:47',(-1.15,1.81,.72),(0,-1,0),.13,M('#FF3A2A',.3,emit=8.0),ex=.004)
    B.box((-4.2,2.56,1.8),(1.0,.02,.8),M('#1A2A4A',.3,emit=.4),0)
    for i in range(14): B.box((-4.9+i*.1,2.54,1.2+(i*37%9)*.1),(.03,.005,.25),M('#FFE7B8',.3,emit=2.0),0)
    B.box((-1.9,2.56,2.1),(.35,.01,.5),M('#C9302C',.6),0)
    # bathroom: sink, round mirror, toothbrush cup
    B.box((1.5,2.25,.85),(.6,.3,.06),M('#F4F7F5',.2),.02); B.box((1.5,2.3,.4),(.5,.25,.4),M('#3E4652',.5),.02)
    B.cyl((1.5,2.53,1.75),.45,.03,M('#C8CCD2',.2,metal=.9),rot=(R(90),0,0),seg=40); g=None
    B.cyl((1.8,2.3,.98),.05,.18,M('#5EB6E0',.3),seg=10); B.box((1.83,2.3,1.12),(.01,.01,.1),M('#F2F0E6',.4),.003)
    # kitchen: counter, fridge, bowl of cereal, coffee machine
    B.box((5.0,2.2,.45),(1.8,.38,.45),M('#5A4636',.6,kind='wood'),.02); B.box((5.0,2.2,.92),(1.85,.42,.03),M('#2B2C33',.3),.01)
    B.box((6.6,2.1,1.0),(.42,.45,1.0),M('#E8ECEF',.3,metal=.2),.03)
    B.cyl((4.4,2.1,1.0),.15,.1,M('#F4F1EA',.3),seg=16,r2=.1); B.cyl((4.4,2.1,1.06),.13,.02,M('#E0B25A',.8),seg=16)
    B.box((3.8,2.2,1.1),(.15,.15,.18),M('#22242B',.3,metal=.5),.02)
    B.done('apt')
    mirror=obox((1.5,2.5,1.75),(.43,.005,.43),M('#BFD0E0',.03,metal=1.0,spec=1.0),0)
    mirror.rotation_euler=(0,0,0); mirror.scale=(1,1,1)
    return mirror
