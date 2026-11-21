# sets for "Never Trust Your Reflection". Every set puts its mirror plane at y=0; build(fl=True) builds the mirrored copy behind the glass.
def setup_dark(sky='#0A0F1E',strength=.25,res=100,samples=None,ssr=False,bloom=.06,mist=None):
    sc=bpy.context.scene; w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; bg=w.node_tree.nodes['Background']
    bg.inputs[0].default_value=hexc(sky); bg.inputs[1].default_value=strength
    sc.render.resolution_x=1080; sc.render.resolution_y=1920; sc.render.resolution_percentage=res; sc.render.engine='BLENDER_EEVEE'; e=sc.eevee
    e.taa_render_samples=samples or SAMPLES; e.use_gtao=True; e.gtao_distance=.8; e.gtao_factor=1.2; e.use_soft_shadows=True; e.use_bloom=True; e.bloom_intensity=bloom; e.bloom_threshold=1.0
    e.use_ssr=ssr; e.ssr_quality=.5; e.ssr_max_roughness=.4; e.ssr_thickness=.5; e.use_ssr_halfres=False
    e.shadow_cascade_size='2048'; e.shadow_cube_size='1024'; e.use_shadow_high_bitdepth=True; e.light_threshold=.02
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='Medium High Contrast'
    if mist:
        bpy.context.view_layer.use_pass_mist=True; w.mist_settings.start=mist[1]; w.mist_settings.depth=mist[2]; w.mist_settings.falloff='QUADRATIC'
        sc.use_nodes=True; ct=sc.node_tree; rl=ct.nodes['Render Layers']; cp=ct.nodes['Composite']
        mx=ct.nodes.new('CompositorNodeMixRGB'); mul=ct.nodes.new('CompositorNodeMath'); mul.operation='MULTIPLY'; mul.inputs[1].default_value=mist[3]
        ct.links.new(rl.outputs['Mist'],mul.inputs[0]); ct.links.new(mul.outputs[0],mx.inputs[0]); ct.links.new(rl.outputs['Image'],mx.inputs[1]); mx.inputs[2].default_value=hexc(mist[0]); ct.links.new(mx.outputs[0],cp.inputs['Image'])
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=True):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot; a.data.use_shadow=shadow; return a
def spot(loc,tg,e,col=(1,1,1),ang=60,blend=.5,r=.1):
    bpy.ops.object.light_add(type='SPOT',location=loc); s=bpy.context.object; s.data.energy=e; s.data.color=col; s.data.spot_size=R(ang); s.data.spot_blend=blend; s.data.shadow_soft_size=r
    d=Vector(tg)-Vector(loc); s.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); return s
GLASSM=M('#BFE6F2',.05,spec=1.0,alpha=.10)
def wall_with_hole(x0,x1,z1,hx0,hx1,hz0,hz1,mat,y=0.0,th=.06):
    """wall in plane y with rectangular opening"""
    if hx0>x0: B.box(((x0+hx0)/2,y,z1/2),((hx0-x0)/2,th,z1/2),mat,0)
    if x1>hx1: B.box(((x1+hx1)/2,y,z1/2),((x1-hx1)/2,th,z1/2),mat,0)
    B.box(((hx0+hx1)/2,y,hz0/2),((hx1-hx0)/2,th,hz0/2),mat,0)
    B.box(((hx0+hx1)/2,y,(z1+hz1)/2),((hx1-hx0)/2,th,(z1-hz1)/2),mat,0)

# ------------------------------------------------------------------ 1. pool locker room
LK=dict(x0=-4.2,x1=4.2,d=6.0,h=3.4,mx0=-2.7,mx1=2.7,mz0=1.3,mz1=2.95)
def locker_room():
    x0,x1,d,h=LK['x0'],LK['x1'],LK['d'],LK['h']
    TILEF=M('#DDEFF2',.25,kind='tile',h2='#8FC7D1',sc=1.25,spec=.6); WT=M('#F4F7F5',.35,kind='tile',h2='#E6EEEC',sc=2.5,spec=.5); TEAL=M('#1F8A8C',.3,kind='tile',h2='#1A7A7E',sc=2.5,spec=.6)
    CEIL=M('#DDE6E8',.9,emit=.55); LKB=M('#27447A',.4,metal=.3); LKB2=M('#C9452E',.4,metal=.3); WOODM=M('#B98A5A',.5,kind='wood',sc=3); CHR=M('#C8CCD2',.2,metal=.9); WHT=M('#F7F8F6',.25,spec=.7)
    for fl in (False,True):
        s=-1 if fl else 1           # y sign: real room is y<0, mirrored copy y>0
        Y=lambda y: -s*y            # y given as positive depth from the mirror wall
        B.box(((x0+x1)/2,Y(d/2),-.05),((x1-x0)/2,d/2,.05),TILEF,0); B.box(((x0+x1)/2,Y(d/2),h+.05),((x1-x0)/2,d/2,.05),CEIL,0)
        for xx in (x0,x1):
            B.box((xx,Y(d/2),.8),(.06,d/2,.8),TEAL,0); B.box((xx,Y(d/2),1.63),(.075,d/2,.03),M('#F2C12E',.4),.005); B.box((xx,Y(d/2),(h+1.66)/2),(.06,d/2,(h-1.66)/2),WT,0)
        B.box(((x0+x1)/2,Y(d),.8),((x1-x0)/2,.06,.8),TEAL,0); B.box(((x0+x1)/2,Y(d),(h+1.6)/2),((x1-x0)/2,.06,(h-1.6)/2),WT,0)
        # door + exit sign on the far (south) wall
        B.box((2.4,Y(d-.07),1.3),(.62,.03,1.3),M('#E8E2D2',.5),.01); B.box((2.4,Y(d-.11),1.7),(.2,.01,.28),M('#9FC7D8',.1,spec=1),0); B.box((2.9,Y(d-.12),1.25),(.03,.03,.1),CHR,.01)
        B.box((2.4,Y(d-.1),2.85),(.34,.03,.12),M('#39D98A',.4,emit=3.0),.01)
        # lockers along both side walls
        for side,xx in ((-1,x0+.36),(1,x1-.36)):
            for k in range(8):
                yy=.75+k*.62
                if yy>d-.5: break
                m=LKB if (k+ (0 if side<0 else 1))%3 else LKB2
                B.box((xx,Y(yy),1.12),(.3,.29,1.1),m,.012); B.box((xx-side*.305,Y(yy),1.12),(.006,.25,1.04),M(shade('#27447A' if m is LKB else '#C9452E',1.12),.4,metal=.3),.004)
                for v in range(3): B.box((xx-side*.315,Y(yy),1.95-v*.06),(.004,.16,.012),M('#141A28',.5),0)
                B.box((xx-side*.318,Y(yy+.17*s*side),1.2),(.006,.02,.07),CHR,.004); B.box((xx-side*.316,Y(yy),1.62),(.004,.06,.04),M('#F4F1EA',.5),0)
            B.box((xx,Y(d/2),.02),(.32,d/2-.3,.02),M('#3A3D47',.6),0)
        # benches
        for bx in (-1.9,1.9):
            for k in range(3): B.box((bx-.14+k*.14,Y(3.3),.52),(.06,1.25,.025),WOODM,.008)
            for yy in (2.3,4.3):
                B.box((bx,Y(yy),.25),(.03,.03,.25),CHR,.005); B.box((bx,Y(yy),.02),(.2,.04,.02),CHR,.005)
        # towel, kick boards, wet-floor sign, drain
        B.box((-1.9,Y(2.9),.56),(.2,.3,.02),M('#F2C12E',.9,kind='fabric'),.01); B.box((1.9,Y(3.9),.58),(.17,.24,.045),M('#E8ECF2',.9,kind='fabric'),.02)
        for k,c in enumerate(('#D2473A','#2B58C9','#35975A','#E6A31C')): B.box((x1-1.1,Y(d-.35-k*.07),.45),(.24,.03,.38),M(c,.7),.02)
        B.box((0,Y(3.6),.004),(.14,.14,.004),CHR,.002)
        for k in range(4): B.box((0,Y(3.6-.09+k*.06),.009),(.11,.008,.002),M('#22242B',.5),0)
        B.box((-.9,Y(4.6),.36),(.02,.2,.36),M('#F2C12E',.5),.006,rot=(R(14*s),0,0)) if False else None
        B.box((-1.0,Y(4.7),.36),(.2,.012,.36),M('#F2C12E',.5),.006); B.box((-1.0,Y(4.685),.42),(.07,.004,.09),M('#22242B',.5),0)
        # sink counter under the mirror
        cx0,cx1=LK['mx0']-.2,LK['mx1']+.2
        B.box(((cx0+cx1)/2,Y(.33),1.02),((cx1-cx0)/2,.33,.045),WHT,.012); B.box(((cx0+cx1)/2,Y(.3),.5),((cx1-cx0)/2-.05,.26,.47),M('#1F6E78',.5),.01)
        for bx in (-1.8,0,1.8):
            B.box((bx,Y(.36),1.062),(.3,.2,.006),M('#C9D6DA',.15,spec=.9),.004); B.cyl((bx,Y(.36),1.066),.03,.004,M('#22242B',.4),seg=12)
            B.cyl((bx,Y(.1),1.16),.022,.2,CHR,seg=10); B.box((bx,Y(.19),1.25),(.02,.1,.016),CHR,.006)
            B.box((bx+.42,Y(.1),1.16),(.05,.04,.09),M('#F4F1EA',.4),.012); B.box((bx+.42,Y(.1),1.09),(.02,.02,.02),M('#2FA8B8',.4),.004)
        # ceiling light strips
        for lx in (-2.2,0,2.2):
            for yy in (1.3,4.2): B.box((lx,Y(yy),h-.03),(.5,.09,.03),M('#F2FBFF',.3,emit=3.0),.01)
        # mirror wall + frame (only once: it sits in the plane)
        if not fl:
            wall_with_hole(x0,x1,h,LK['mx0'],LK['mx1'],LK['mz0'],LK['mz1'],WT,y=0.0,th=.05)
            fm=M('#C8CCD2',.25,metal=.9); mx0,mx1,mz0,mz1=LK['mx0'],LK['mx1'],LK['mz0'],LK['mz1']
            for zz in (mz0,mz1): B.box(((mx0+mx1)/2,0,zz),((mx1-mx0)/2+.04,.07,.035),fm,.01)
            for xx in (mx0,mx1): B.box((xx,0,(mz0+mz1)/2),(.035,.07,(mz1-mz0)/2),fm,.01)
    B.done('batch_lk')
    g=obox(((LK['mx0']+LK['mx1'])/2,0,(LK['mz0']+LK['mz1'])/2),((LK['mx1']-LK['mx0'])/2,.004,(LK['mz1']-LK['mz0'])/2),GLASSM,0); g.name='glass_m'
    for s in (-1,1):
        for lx in (-2.2,0,2.2):
            for yy in (1.3,4.2): area((lx,-s*yy,LK['h']-.08),42,(1.0,.2),(.86,.95,1.0),shadow=(lx==0))
    return g

# ------------------------------------------------------------------ 2. rainy night street. storefront glass plane y=0, sidewalk y in [-2.6,0], road south of it
def neon_text(body,loc,size,col,e=6.0,n=(0,-1,0)):
    text(body,loc,n,size,M(col,.3,emit=e),ex=.02)
def street(puddle=None):
    BR1=M('#5A3A34',.8,kind='concrete',sc=.22); BR2=M('#3E4658',.8,kind='concrete',sc=.22); BR3=M('#6B5A48',.8,kind='concrete',sc=.22)
    ASPH=M('#14161B',.13,spec=.9); WALK=M('#3C3F48',.28,kind='concrete',sc=1.0,spec=.7); CURB=M('#5A5D66',.4); DK=M('#0C0E14',.6); FRM=M('#1B1D24',.4,metal=.5)
    # road + far sidewalk
    B.box((0,-6.3,-.06),(30,3.7,.05),ASPH,0); B.box((0,-2.62,-.02),(30,.1,.09),CURB,.02); B.box((0,-10.0,-.02),(30,.1,.09),CURB,.02); B.box((0,-12,-.03),(30,2,.1),WALK,0)
    for k in range(-7,8): B.box((k*3.6,-6.3,-.008),(.9,.07,.004),M('#C9C4A8',.3),0)
    # near sidewalk (optionally with an elliptical puddle hole)
    if puddle:
        px,py,ra,rb=puddle; N=28; el=[(px+ra*math.cos(2*pi*i/N)*(1+.12*math.sin(5*2*pi*i/N)),py+rb*math.sin(2*pi*i/N)*(1+.1*math.cos(3*2*pi*i/N))) for i in range(N)]
        def sq(i):
            a=2*pi*i/N; c,s_=math.cos(a),math.sin(a); m=max(abs(c),abs(s_)); return (px+c/m*4.0, max(-2.52,min(0,py+s_/m*4.0)))
        for i in range(N):
            j=(i+1)%N; B.poly([(el[i][0],el[i][1],.07),(el[j][0],el[j][1],.07),(sq(j)[0],sq(j)[1],.07),(sq(i)[0],sq(i)[1],.07)],WALK)
            B.poly([(el[i][0],el[i][1],.07),(el[i][0],el[i][1],-.3),(el[j][0],el[j][1],-.3),(el[j][0],el[j][1],.07)],DK)
        for sx in (-1,1): B.box((px+sx*17,-1.26,0),(13,1.26,.07),WALK,0)
        B.done('batch_walk'); w=omesh([(x,y,.062) for x,y in el],[list(range(N))],M('#9FC4E8',.02,spec=1.0,alpha=.22)); w.name='glass_puddle'
    else: B.box((0,-1.26,0),(30,1.26,.07),WALK,0)
    # three storefronts on the near side
    def shop(cx,w,brick,floors,kind,sign,scol):
        x0,x1=cx-w/2,cx+w/2; H=3.3+floors*3.0
        wall_with_hole(x0,x1,3.3,x0+.5,x1-.5,.55,2.75,M('#1E2230',.5),y=.06,th=.07)
        for xx in (x0+.5,x1-.5,cx): B.box((xx,.0,1.65),(.05,.06,1.1),FRM,.01)
        for zz in (.55,2.75): B.box((cx,.0,zz),(w/2-.5,.07,.045),FRM,.01)
        B.box((cx,.25,3.3+floors*1.5),(w/2,.3,floors*1.5),brick,0); B.box((cx,-.02,3.32),(w/2,.12,.06),M('#22242B',.5),.01); B.box((cx,.1,H+.12),(w/2+.05,.5,.12),M('#2A2C34',.6),.02)
        r=random.Random(int(cx*7)+3)
        for f in range(floors):
            for k in range(int(w//1.9)):
                wx=x0+.95+k*1.9+ (w-(int(w//1.9))*1.9)/2; wz=4.6+f*3.0; lit=r.random()<.45
                B.box((wx,-.06,wz),(.55,.03,.8),M(r.choice(['#F2C46B','#FFDFA0','#9FD8F2']) ,.4,emit=r.uniform(1.2,2.4)) if lit else M('#10141E',.1,spec=.9),0)
                B.box((wx,-.08,wz),(.6,.03,.035),FRM,0); B.box((wx,-.08,wz),(.03,.03,.85),FRM,0); B.box((wx,-.12,wz-.86),(.66,.08,.04),M('#8A8E96',.6),.01)
                if lit and r.random()<.5: B.box((wx+r.uniform(-.2,.2),-.02,wz-.45),(.12,.02,.3),M('#1A1C22',.8),0)
            if r.random()<.7: B.box((x0+r.uniform(.6,w-.6),-.3,4.0+f*3.0),(.32,.2,.2),M('#B8BCC2',.5,metal=.4),.02)
        # awning + sign
        if kind!='dark':
            for k in range(8): B.box((x0+.5+(k+.5)*(w-1)/8,-.5,3.0),((w-1)/16,.5,.03),M(scol if k%2 else '#F4F1EA',.8,kind='fabric'),.005,rot=(R(-14),0,0))
        neon_text(sign,(cx,-.2,3.72),.42,scol,7.0)
        point((cx,-.9,3.4),260 if kind!='dark' else 90,hexc(scol)[:3],.3,shadow=False)
        if kind=='wash':
            B.box((cx,2.4,1.7),(w/2-.3,.05,1.6),M('#DDF6FA',.5,emit=1.6),0); B.box((cx,1.3,-.0),(w/2,1.3,.05),M('#C9E2E6',.3,kind='tile',h2='#8FB9C2',sc=1.5),0)
            for k in range(4):
                mx=x0+1.0+k*(w-2)/3; B.box((mx,2.0,.75),(.42,.35,.75),M('#F4F7F8',.3),.03); B.cyl((mx,1.63,.8),.26,.04,M('#22364A',.1,spec=1),rot=(R(90),0,0),seg=20); B.cyl((mx,1.66,.8),.3,.03,M('#C8CCD2',.2,metal=.9),rot=(R(90),0,0),seg=20)
                B.box((mx,1.64,1.36),(.3,.01,.06),M('#2FA8B8',.4,emit=1.5),0)
            B.box((cx,.9,.45),(.9,.2,.04),M('#B98A5A',.5,kind='wood'),.01); point((cx,1.2,2.8),300,(.75,.95,1.0),.4,shadow=False)
        if kind=='noodle':
            B.box((cx,2.4,1.7),(w/2-.3,.05,1.6),M('#7A2A1E',.7,emit=.5),0); B.box((cx,1.3,0),(w/2,1.3,.05),M('#5A3A24',.5,kind='wood'),0)
            B.box((cx,1.5,.95),(w/2-.8,.3,.05),M('#8A5A36',.5,kind='wood'),.01); B.box((cx,1.5,.47),(w/2-.85,.25,.47),M('#3A2A1E',.6),.01)
            for k in range(4):
                sx_=x0+1.2+k*(w-2.4)/3; B.cyl((sx_,.95,.6),.17,.05,M('#C9452E',.6),seg=12); B.cyl((sx_,.95,.3),.03,.6,FRM,seg=8)
                B.cyl((sx_,1.5,2.35),.16,.34,M('#FF5A3A',.5,emit=3.0),seg=12); B.cyl((sx_,1.5,1.03),.11,.07,M('#F4F1EA',.4),seg=12,r2=.07)
            point((cx,1.3,2.5),300,(1,.55,.35),.4,shadow=False)
        if kind=='dark':
            # the mirror world behind the dark glass: mirrored sidewalk, curb, wet road and a lamp glow
            B.box((cx,1.26,0),(w/2+3,1.26,.07),WALK,0); B.box((cx,2.62,-.02),(w/2+3,.1,.09),CURB,.02); B.box((cx,6.3,-.06),(w/2+3,3.7,.05),ASPH,0)
            B.box((cx,10.4,3),(w/2+6,.2,5),M('#0E1220',.8),0)
            for k in range(5): B.box((cx-5+k*2.5,10.1,2.2+ (k%2)*2.3),(.5,.03,.7),M(['#F2C46B','#9FD8F2','#FF7A5A'][k%3],.4,emit=1.5),0)
            B.box((cx,.3,3.05),(w/2-.5,.3,.3),M('#10121A',.8),0)
    shop(-7.5,7.0,BR1,3,'wash','24H  WASH','#39D9E8'); shop(0,6.0,BR2,4,'dark','PHARMACY','#6BE38A'); shop(7.5,7.0,BR3,3,'noodle','NOODLES','#FF4A3A')
    for cx,w,br,fl in ((-15.5,9,BR2,4),(15.5,9,BR1,5)):
        B.box((cx,.3,(3.3+fl*3)/2),(w/2,.3,(3.3+fl*3)/2),br,0)
        r=random.Random(int(cx))
        for f in range(fl+1):
            for k in range(4): B.box((cx-w/2+1.2+k*2.1,-.02,1.6+f*3.0),(.55,.03,.8),M('#F2C46B',.4,emit=1.6) if r.random()<.4 else M('#10141E',.1,spec=.9),0)
    # far side of the street: silhouettes with lit windows + neon
    r=random.Random(9); xx=-28
    while xx<28:
        w=r.uniform(5,8); fl=r.randint(3,6); H=3.3+fl*3; br=r.choice([BR1,BR2,BR3]); B.box((xx+w/2,-14.5,H/2),(w/2-.03,.5,H/2),br,0); B.box((xx+w/2,-14.3,H+.1),(w/2,.7,.1),M('#2A2C34',.6),0)
        for f in range(fl+1):
            for k in range(int(w//1.8)):
                lit=r.random()<.4; B.box((xx+.9+k*1.8,-13.97,1.7+f*3.0),(.5,.03,.75),M(r.choice(['#F2C46B','#FFDFA0','#9FD8F2','#F2A0C8']),.4,emit=r.uniform(1,2.2)) if lit else M('#10141E',.1,spec=.9),0)
        if r.random()<.7:
            col=r.choice(['#FF4AA8','#39D9E8','#F2C12E','#8A6BFF']); B.box((xx+w/2,-13.9,3.5),(w/2-1,.06,.28),M(col,.3,emit=5.0),.02); point((xx+w/2,-13.0,3.2),350,hexc(col)[:3],.4,shadow=False)
        xx+=w
    # street furniture
    LAMPM=M('#22252C',.4,metal=.6)
    for lx in (-11,-3.6,3.6,11):
        B.cyl((lx,-2.3,2.4),.07,4.8,LAMPM,seg=10); B.box((lx,-2.75,4.8),(.06,.5,.05),LAMPM,.01); B.box((lx,-3.15,4.72),(.16,.24,.06),M('#FFE2A8',.3,emit=9.0),.02); B.cyl((lx,-2.3,.15),.13,.3,LAMPM,seg=10)
        spot((lx,-3.1,4.6),(lx,-2.6,0),2600,(1,.82,.55),120,.7,.15)
    B.cyl((-2.2,-2.1,.5),.3,.9,M('#2F5E4A',.5,metal=.3),seg=14); B.cyl((-2.2,-2.1,.97),.32,.06,M('#22252C',.5),seg=14)
    B.cyl((5.2,-2.2,.3),.14,.6,M('#C9452E',.4),seg=10); B.cyl((5.2,-2.2,.62),.1,.1,M('#C9452E',.4),seg=10); B.box((5.2,-2.2,.38),(.24,.05,.05),M('#C9452E',.4),.02)
    for k in range(3): B.box((-5.6+k*.02,-.5-k*.0,.25+k*.42),(.34,.26,.2),M(['#8A5A36','#7A4E2E','#96643C'][k],.7,kind='wood'),.01)
    B.cyl((8.6,-2.25,1.5),.04,3.0,LAMPM,seg=8); B.box((8.6,-2.25,2.85),(.3,.03,.3),M('#2B58C9',.4),.02); B.box((8.6,-2.29,2.85),(.2,.01,.12),M('#F4F5FA',.4),0)
    B.box((10.2,-1.0,.5),(.9,.22,.04),M('#8A5A36',.5,kind='wood'),.01); B.box((10.2,-.85,.85),(.9,.03,.22),M('#8A5A36',.5,kind='wood'),.01)
    for sx in (-.8,.8): B.box((10.2+sx,-1.0,.25),(.04,.2,.25),LAMPM,.01)
    # parked car on the far lane + overhead wires
    cc=(-9.5,-8.6); B.box((cc[0],cc[1],.62),(2.1,.88,.36),M('#2B58C9',.25,metal=.4),.14); B.box((cc[0]-.15,cc[1],1.2),(1.15,.78,.3),M('#2B58C9',.25,metal=.4),.16); B.box((cc[0]-.15,cc[1]+.79,1.22),(.95,.01,.2),M('#0E1420',.05,spec=1),0)
    for sx in (-1.3,1.3):
        for sy in (-.86,.86): B.cyl((cc[0]+sx,cc[1]+sy,.36),.36,.24,M('#111216',.7),rot=(R(90),0,0),seg=18)
    B.box((cc[0]+2.1,cc[1],.68),(.02,.6,.08),M('#FF3A2A',.3,emit=3.0),0)
    for k in range(3): B.cyl((0,-3.0-k*.25,6.2+k*.2),.012,60,M('#0A0A0E',.6),rot=(0,R(90),0),seg=6)
    # glossy puddles on the road
    r=random.Random(4)
    for k in range(14): B.cyl((r.uniform(-14,14),r.uniform(-9.5,-3.2),-.008),r.uniform(.4,1.1),.004,M('#0A0C12',.02,spec=1.0),seg=14)
    B.done('batch_st')
    g=obox((0,-.03,1.65),(2.5,.004,1.1),M('#0B1424',.03,spec=1.0,alpha=.32),0); g.name='glass_shop'
    return g
def rain(cx,cy,n=420,seed=2,box=(9,7,9),speed=13.0):
    r=random.Random(seed); m=M('#CFE6FF',.3,emit=.8,alpha=.28); objs=[]
    for c in range(2):
        bm=bmesh.new()
        for i in range(n):
            x=cx+r.uniform(-box[0],box[0]); y=cy+r.uniform(-box[1],box[1]); z=r.uniform(0,box[2]); ln=r.uniform(.18,.34)
            bmesh.ops.create_cube(bm,size=1,matrix=Matrix.Translation((x,y,z))@Euler((R(4),R(-7),0)).to_matrix().to_4x4()@Matrix.Diagonal((.006,.006,ln,1)))
        me=bpy.data.meshes.new('rain'); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new('glass_rain%d'%c,me); _col.objects.link(o); me.materials.append(m); objs.append(o)
    Hh=box[2]
    def fn(o,t):
        d=(speed*t)%Hh; objs[0].location=(0,0,-d); objs[1].location=(0,0,Hh-d)
    fx.add(objs[0],fn)

# ------------------------------------------------------------------ 3. the house: entry hall / living room. tall mirror on the north wall (y=0)
def clock_face(c,r,n,mat_face,hh=9,mm=17):
    """wall clock at c, facing direction n=(0,-1) (south) or other axis-aligned; hands stopped at hh:mm"""
    x,y,z=c; HM=M('#15161A',.4)
    B.cyl((x,y,z),r,.05,M('#2A2420',.5),rot=(R(90),0,0),seg=28); B.cyl((x,y+n*.03,z),r*.88,.012,mat_face,rot=(R(90),0,0),seg=28)
    for k in range(12): a=k*pi/6; B.box((x+r*.72*math.sin(a),y+n*.04,z+r*.72*math.cos(a)),(r*.035,.004,r*.035),HM,0)
    sg=-n   # viewer on the n side: clockwise appears along -x*n ... for n=-1 (viewer south) clockwise = +x when going from 12 to 3
    for ang,ln,wd in (((hh%12+mm/60)*pi/6,r*.45,r*.045),(mm*pi/30,r*.68,r*.03)):
        dx=math.sin(ang)*sg; dz=math.cos(ang); B.box((x+dx*ln/2,y+n*.05,z+dz*ln/2),(wd,.004,ln/2),HM,0,rot=(0,math.atan2(dx,dz),0))
HCLK={}
def clock_set(sec,frozen=False):
    """seconds since 9:17:00"""
    T=9*3600+17*60+sec
    for nm in ('gf','wall'):
        d=HCLK[nm]; d['h'].rotation_euler=(0,(T/3600%12)*pi/6,0); d['m'].rotation_euler=(0,(T/60%60)*pi/30,0); d['s'].rotation_euler=(0,(math.floor(sec)%60+ (0 if frozen else min(1,(sec%1)*6)) - (0 if frozen else 1) + 42)*pi/30,0)
    HCLK['pend'].rotation_euler=(0,R(11) if frozen else R(11)*math.cos(sec*pi),0)
HLm=dict(x0=-.62,x1=.62,z0=.35,z1=2.75)
def house(mode='frozen'):
    x0,x1,d,h=-4.4,4.4,6.6,3.3
    WALLG=M('#1F5248',.85,kind='wall'); WAIN=M('#EDE6D2',.6); FLW=M('#7A4A2A',.45,kind='wood',sc=2.2,spec=.5); CEIL=M('#EFE9DC',.9,emit=.03)
    MUST=M('#D9A21F',.85,kind='fabric'); DKW=M('#3A2418',.5,kind='wood',sc=3); BRASS=M('#C9A24A',.3,metal=.9)
    for fl in (False,True):
        s=-1 if fl else 1; Y=lambda y: -s*y
        B.box((0,Y(d/2),-.05),((x1-x0)/2,d/2,.05),FLW,0); B.box((0,Y(d/2),h+.05),((x1-x0)/2,d/2,.05),CEIL,0)
        for xx in (x0,x1):
            B.box((xx,Y(d/2),h/2),(.06,d/2,h/2),WALLG,0); B.box((xx-(.07 if xx<0 else -.07),Y(d/2),.5),(.02,d/2,.5),WAIN,.004); B.box((xx-(.09 if xx<0 else -.09),Y(d/2),1.02),(.03,d/2,.03),WAIN,.008)
        B.box((0,Y(d),h/2),((x1-x0)/2,.06,h/2),WALLG,0)
        # front door (south wall), ajar, with street glow
        B.box((2.6,Y(d-.08),1.35),(.7,.04,1.35),M('#0C1220',.6,emit=.15),0); B.box((1.93,Y(d-.68),1.32),(.04,.6,1.3),M('#A8362C',.5),.02,rot=(0,0,R(-3*s)))
        for xx in (1.88,3.32): B.box((xx,Y(d-.1),1.38),(.06,.07,1.4),WAIN,.01)
        B.box((2.6,Y(d-.1),2.78),(.78,.07,.06),WAIN,.01); B.box((2.6,Y(d-.5),.012),(.6,.38,.012),M('#5A3A24',.9,kind='fabric'),.005)
        # coat rack + shoes by the door
        B.cyl((3.9,Y(d-.6),1.0),.035,2.0,DKW,seg=8); B.box((3.9,Y(d-.6),1.75),(.12,.2,.35),M('#27447A',.9,kind='fabric'),.05); B.box((3.82,Y(d-.42),1.6),(.1,.12,.4),M('#C9452E',.9,kind='fabric'),.05)
        for k,c in enumerate(('#F4F5FA','#22242B','#CF3F78')): B.box((3.6-k*.32,Y(d-.25),.06),(.1,.16,.06),M(c,.5),.03)
        # rug + sofa + side table + lamp
        B.box((.9,Y(3.5),.01),(1.9,1.35,.01),M('#A8362C',.95,kind='fabric',sc=2),.004); B.box((.9,Y(3.5),.017),(1.65,1.1,.006),M('#E8D9B8',.95,kind='fabric',sc=2),.003); B.box((.9,Y(3.5),.021),(1.4,.85,.004),M('#1F5248',.95,kind='fabric',sc=2),.002)
        B.box((3.75,Y(3.4),.42),(.45,1.25,.2),MUST,.08); B.box((4.12,Y(3.4),.85),(.14,1.25,.42),MUST,.08)
        for yy in (2.2,4.6): B.box((3.75,Y(yy),.6),(.45,.14,.3),MUST,.07)
        for k,c in enumerate(('#1F5248','#A8362C')): B.box((3.85,Y(2.8+k*1.2),.76),(.12,.24,.22),M(c,.9,kind='fabric'),.07)
        B.cyl((3.7,Y(1.5),.5),.3,.04,DKW,seg=18); B.cyl((3.7,Y(1.5),.25),.04,.5,DKW,seg=8); B.cyl((3.7,Y(1.5),.02),.2,.04,DKW,seg=14)
        B.cyl((3.7,Y(1.5),.9),.03,.75,BRASS,seg=8); B.cyl((3.7,Y(1.5),1.42),.24,.34,M('#FFE2B0',.6,emit=2.2),seg=16,r2=.15)
        # staircase up along the west wall + basement door underneath (ajar, black gap)
        for k in range(9): B.box((x0+.62,Y(1.2+k*.42),.16+k*.32),(.56,.21,.16+k*.0),DKW,.01); B.box((x0+.62,Y(1.2+k*.42),(k*.32)/2),(.54,.2,max(.01,(k*.32)/2)),WAIN,0)
        for k in range(0,9,2): B.cyl((x0+1.14,Y(1.2+k*.42),.8+k*.32),.025,.95,WAIN,seg=8)
        B.box((x0+1.14,Y(2.9),2.6),(.04,2.0,.04),DKW,.01,rot=(R(-37.3*s),0,0))
        B.box((x0+1.2,Y(5.2),1.1),(.02,.5,1.1),M('#050608',.9),0); B.box((x0+1.5,Y(5.62),1.08),(.3,.04,1.08),M('#C9B48A',.5),.015,rot=(0,0,R(38*s)))
        # pictures, plant, clocks stopped at 9:17
        for k,(px_,c1,c2) in enumerate(((-2.6,'#F2D9A8','#4A86B8'),(-1.75,'#CFE3EE','#C9452E'),(1.8,'#E8D9B8','#35975A'))):
            B.box((px_,Y(.06),1.9+.12*(k%2)),(.32,.02,.4),DKW,.008); B.box((px_,Y(.085),1.9+.12*(k%2)),(.26,.006,.34),M(c1,.7),0); B.box((px_,Y(.09),1.78+.12*(k%2)),(.2,.006,.12),M(c2,.7),0)
        B.cyl((2.9,Y(.5),.3),.24,.6,M('#C9452E',.6),seg=14,r2=.18)
        for k in range(9): a_=k*.7; B.ico((2.9+.22*math.cos(a_),Y(.5+.22*math.sin(a_)*s),.75+.14*(k%4)),.2,M(['#3F8A4A','#4E9A55','#367A40'][k%3],.7),sc=(1,1,1.4),sub=1)
        clock_face((x1-.1,Y(3.4),2.45),.34,0,M('#F7F2E2',.5)) if False else None
        # grandfather clock on the east side of the north wall
        gx=3.2; B.box((gx,Y(.3),1.15),(.3,.22,1.15),DKW,.02); B.box((gx,Y(.3),2.36),(.34,.25,.08),DKW,.02); B.box((gx,Y(.53),.75),(.16,.006,.5),M('#0E0C0A',.2,spec=1),0); (B.cyl((gx,Y(.55),.62),.09,.02,BRASS,rot=(R(90),0,0),seg=16),B.box((gx,Y(.55),.9),(.012,.006,.3),BRASS,0)) if fl else None
        B.cyl((gx,Y(.535),1.95),.2,.012,M('#F7F2E2',.5),rot=(R(90),0,0),seg=24)
        hmat=M('#15161A',.4); sg=1 if not fl else -1
        for k in range(12): a=k*pi/6; B.box((gx+.165*math.sin(a),Y(.543),1.95+.165*math.cos(a)),(.008 if k%3 else .014,.003,.02 if k%3 else .028),hmat,0,rot=(0,a,0))
        B.cyl((gx,Y(.546),1.95),.018,.012,BRASS,rot=(R(90),0,0),seg=10)
        for ang,ln,wd in (((9+17/60)*pi/6,.095,.016),(17*pi/30,.155,.009)):
            if fl: dx=math.sin(ang); dz=math.cos(ang); B.box((gx+dx*ln/2,Y(.545),1.95+dz*ln/2),(wd,.004,ln/2),hmat,0,rot=(0,math.atan2(dx,dz),0))
        # round wall clock high on the west side of the north wall
        wx=-.0; 
        if not fl:
            wall_with_hole(x0,x1,h,HLm['x0'],HLm['x1'],HLm['z0'],HLm['z1'],WALLG,y=0.0,th=.05)
            B.box((0,-.07,.5),((x1-x0)/2,.02,.5),WAIN,.004) if False else None
            for xx in (HLm['x0'],HLm['x1']): B.box((xx,0,(HLm['z0']+HLm['z1'])/2),(.07,.08,(HLm['z1']-HLm['z0'])/2+.07),BRASS,.02)
            for zz in (HLm['z0'],HLm['z1']): B.box((0,0,zz),((HLm['x1']-HLm['x0'])/2+.07,.08,.07),BRASS,.02)
            B.box((0,0,HLm['z1']+.2),(.3,.06,.1),BRASS,.04)
        cx_=-1.9; B.cyl((cx_,Y(.08),2.72),.3,.05,DKW,rot=(R(90),0,0),seg=28); B.cyl((cx_,Y(.11),2.72),.26,.012,M('#F7F2E2',.5),rot=(R(90),0,0),seg=28)
        for k in range(12): a=k*pi/6; B.box((cx_+.21*math.sin(a),Y(.12),2.72+.21*math.cos(a)),(.012,.004,.012),hmat,0)
        for ang,ln,wd in (((9+17/60)*pi/6,.12,.02),(17*pi/30,.2,.011)):
            if fl: dx=math.sin(ang); dz=math.cos(ang); B.box((cx_+dx*ln/2,Y(.125),2.72+dz*ln/2),(wd,.004,ln/2),hmat,0,rot=(0,math.atan2(dx,dz),0))
        # ceiling pendant
        B.cyl((.6,Y(3.3),h-.3),.012,.6,hmat,seg=6); B.cyl((.6,Y(3.3),h-.72),.3,.26,M('#F2E2B8',.6,emit=1.6),seg=18,r2=.12)
    B.done('batch_hs')
    g=obox((0,0,(HLm['z0']+HLm['z1'])/2),((HLm['x1']-HLm['x0'])/2,.004,(HLm['z1']-HLm['z0'])/2),M('#BFE6F2',.08,spec=.06,alpha=.08),0); g.name='glass_m'
    # animated hands + pendulum for the real-side clocks
    HCLK.clear(); hm=M('#15161A',.4); rd=M('#C9302A',.4); br=M('#C9A24A',.3,metal=.9)
    for nm,(cx,cy,cz),lh,lm,wh in (('gf',(3.2,-.548,1.95),.095,.155,.016),('wall',(-1.9,-.128,2.72),.12,.2,.02)):
        d={}
        for key,ln,wd,mat,dy in (('h',lh,wh,hm,0),('m',lm,wh*.55,hm,-.004),('s',lm*1.02,wh*.22,rd,-.008)):
            e=empty((cx,cy+dy,cz)); obox((0,0,ln/2),(wd,.003,ln/2),mat,0,e); d[key]=e
        HCLK[nm]=d
    pe=empty((3.2,-.555,1.2)); obox((0,0,-.3),(.012,.006,.3),br,0,pe); ocyl((0,0,-.6),.09,.02,br,pe,seg=18); HCLK['pend']=pe
    clock_set(0,frozen=True)
    cold=(mode=='frozen'); col=(.62,.78,1.0) if cold else (1,.86,.66); e=1.0 if cold else 1.25
    for s in (-1,1):
        point((.6,-s*3.3,h-1.7),95*e,col,.3,shadow=False); area((0,-s*3.3,h-.12),170*e,(4,3),col,shadow=(s==1)); point((3.7,-s*1.5,1.5),90*e,(1,.8,.55) if not cold else (.7,.82,1),.2,shadow=False); point((-2.4,-s*5.0,2.6),160*e,col,.4,shadow=False)
    return g

# ------------------------------------------------------------------ 4. basement. giant mirror on the north wall (y=0); behind it a pale blue void
BSm=dict(x0=-1.35,x1=1.35,z0=.12,z1=3.0)
def basement():
    x0,x1,d,h=-3.8,3.8,6.4,3.3
    BRK=M('#5E4038',.85,kind='concrete',sc=.2); FLC=M('#4A4C52',.6,kind='concrete',sc=1.2); JO=M('#3A2A1E',.6,kind='wood',sc=3); MET=M('#6A6E76',.4,metal=.7); DKW=M('#3A2418',.5,kind='wood',sc=3)
    B.box((0,-d/2,-.05),((x1-x0)/2,d/2,.05),FLC,0); B.box((0,-d/2,h+.2),((x1-x0)/2,d/2,.05),M('#2A2420',.9),0)
    for k in range(9): B.box((x0+.4+k*.9,-d/2,h+.04),(.06,d/2,.12),JO,.01)
    for xx in (x0,x1): B.box((xx,-d/2,h/2),(.08,d/2,h/2),BRK,0)
    B.box((0,-d,h/2),((x1-x0)/2,.08,h/2),BRK,0)
    wall_with_hole(x0,x1,h+.2,BSm['x0'],BSm['x1'],BSm['z0'],BSm['z1'],BRK,y=0.0,th=.08)
    # ornate mirror frame
    FR=M('#2A1F18',.4,kind='wood',sc=4); GD=M('#B8923A',.3,metal=.9)
    for xx in (BSm['x0'],BSm['x1']): B.box((xx,-.02,(BSm['z0']+BSm['z1'])/2),(.13,.12,(BSm['z1']-BSm['z0'])/2+.13),FR,.03); B.box((xx,-.13,(BSm['z0']+BSm['z1'])/2),(.03,.02,(BSm['z1']-BSm['z0'])/2),GD,.01)
    for zz in (BSm['z0'],BSm['z1']): B.box((0,-.02,zz),((BSm['x1']-BSm['x0'])/2+.13,.12,.13),FR,.03)
    B.box((0,-.02,BSm['z1']+.22),(.5,.1,.12),FR,.05); B.ico((0,-.1,BSm['z1']+.22),.1,GD,sub=2)
    # stairs down along the west wall, from the south (top) to the middle of the room
    for k in range(10): B.box((x0+.65,-d+.5+k*.4,2.9-k*.3),(.6,.2,.04),DKW,.01); B.box((x0+1.22,-d+.5+k*.4,(2.9-k*.3)/2),(.03,.03,(2.9-k*.3)/2),DKW,0) if k%3==0 else None
    B.box((x0+1.24,-d+2.3,3.25-1.35),(.03,2.1,.03),DKW,.01,rot=(R(-36.9),0,0)) 
    B.box((x0+.65,-d+.09,3.0+ .0),(.55,.02,.0),DKW,0) if False else None
    # high window on the east wall + pipes + shelves + boxes + boiler
    B.box((x1-.05,-2.2,2.55),(.05,.75,.4),M('#141A28',.3),0)
    for k in range(3): B.cyl((0,-1.3-k*.3,h-.25-k*.0),.05,(x1-x0),MET,rot=(0,R(90),0),seg=10)
    B.cyl((x1-.5,-.6,h/2),.07,h,MET,seg=10)
    for z in (.5,1.2,1.9): B.box((x1-.4,-4.6,z),(.32,1.0,.03),JO,.008)
    for xx_ in (-3.6,-5.6): B.box((x1-.4,xx_,1.0),(.3,.03,1.0),JO,.008)
    r=random.Random(3)
    for z in (.53,1.23,1.93):
        yy=-5.4
        while yy<-3.8:
            w=r.uniform(.1,.22); hh=r.uniform(.12,.3); B.box((x1-.4,yy+w,z+hh),(r.uniform(.15,.26),w,hh),M(r.choice(['#B98A5A','#8A5A36','#C9452E','#2B58C9','#D8D2C8','#35975A']),.7),.015); yy+=2*w+.05
    for (bx,by,sz,c) in ((1.9,-.7,.38,'#B98A5A'),(2.5,-.9,.3,'#A87A4C'),(2.0,-.75,.26,'#C49A6C')): B.box((bx,by,sz if c!='#C49A6C' else .76+sz),(sz,sz,sz),M(c,.8),.015)
    B.cyl((-2.9,-.8,.8),.45,1.6,M('#D8D2C8',.4,metal=.3),seg=18); B.cyl((-2.9,-.8,1.65),.3,.14,MET,seg=14); B.cyl((-2.9,-.8,2.5),.06,1.6,MET,seg=8)
    B.box((-1.9,-5.9,.45),(.5,.35,.45),M('#F4F7F8',.3),.03); B.cyl((-1.9,-5.53,.5),.24,.03,M('#22364A',.1,spec=1),rot=(R(90),0,0),seg=18)
    B.cyl((.3,-3.2,h-.35),.01,.7,M('#15161A',.5),seg=6); B.ico((.3,-3.2,h-.75),.07,M('#FFE2A8',.4,emit=4.0),sub=2)
    # the other side: pale blue void with a faint floor
    B.box((0,3.0,-.05),(5,3,.05),M('#7FB6D8',.6,emit=.06),0); B.box((0,6.0,3),(6,.1,4),M('#9FD2F2',.6,emit=.22),0)
    for sx in (-1,1): B.box((sx*5,3,3),(.1,3,4),M('#7FB6D8',.6,emit=.1),0)
    B.done('batch_bs')
    g=obox((0,0,(BSm['z0']+BSm['z1'])/2),((BSm['x1']-BSm['x0'])/2,.004,(BSm['z1']-BSm['z0'])/2),M('#BFE6FF',.08,spec=.12,alpha=.14,emit=.08),0); g.name='glass_m'
    cloth=obox((x1-.14,-2.2,2.5),(.03,.85,.52),M('#4A3D32',.95,kind='fabric'),.02); cloth.name='glass_cloth'
    return g,cloth
