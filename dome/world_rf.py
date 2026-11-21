# sets for "The City Under the Dome"
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
    return w,bg
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=True):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot; a.data.use_shadow=shadow; return a
def spot(loc,tg,e,col=(1,1,1),ang=60,blend=.5,r=.1):
    bpy.ops.object.light_add(type='SPOT',location=loc); s=bpy.context.object; s.data.energy=e; s.data.color=col; s.data.spot_size=R(ang); s.data.spot_blend=blend; s.data.shadow_soft_size=r
    d=Vector(tg)-Vector(loc); s.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); return s
def sun(rot,e,col=(1,1,1),ang=1.5):
    bpy.ops.object.light_add(type='SUN'); S=bpy.context.object; S.rotation_euler=rot; S.data.energy=e; S.data.color=col; S.data.angle=R(ang)
    S.data.shadow_cascade_max_distance=60; S.data.shadow_cascade_count=3; return S
def seg(a,b,r,mat,sides=8):
    a=Vector(a); b=Vector(b); d=b-a; c=(a+b)/2; rot=d.to_track_quat('Z','Y').to_euler(); B.cyl(tuple(c),r,d.length,mat,rot=tuple(rot),seg=sides)
GLASSM=M('#CFEFFF',.04,spec=1.0,alpha=.10)
PAINT=M('#2A8ACB',.55,emit=1.25,kind='leaves')          # blue paint, mottled like water
PAINT2=M('#1A66A3',.5,emit=.45,kind='leaves')
PAINT_E=M('#2479BA',.55,emit=.7,kind='leaves')
FRESH=M('#2A85C8',.25,emit=.5,spec=.8)                    # glossy fresh paint
RIB=M('#9AA8B8',.3,metal=.7,emit=.15)
SAND=M('#E2B47A',.85,kind='asphalt'); SAND2=M('#D49E62',.9,kind='asphalt')
CONC=['#E8DCC8','#CFE3E0','#E7C3B0','#C9D3E6','#F0E6D0','#D8C8DE']
WIN=M('#FFE7B8',.3,emit=2.2); WIN2=M('#BFE9FF',.3,emit=1.6); WIND=M('#24364A',.2,spec=.9)
LEAF=M('#3E8E4A',.7,kind='leaves'); LEAF2=M('#5FA84A',.7,kind='leaves'); TRUNK=M('#6B4A30',.8,kind='wood')

# ------------------------------------------------------------------ the dome (radius RD, centre DC); a hole region can be cut
RD=36.0; DC=(0,0,-4.0)
def dome_shell(hole=None,paint=PAINT,ribs=True,nth=48,nph=10):
    """hole: (theta_deg, phi_deg, half_width_deg, half_height_deg) region removed"""
    ph0=math.asin(4/RD); vs=[]; fs=[]
    def P(th,ph): return (DC[0]+RD*math.cos(ph)*math.cos(th),DC[1]+RD*math.cos(ph)*math.sin(th),DC[2]+RD*math.sin(ph))
    phs=[ph0+(pi/2-.02-ph0)*j/nph for j in range(nph+1)]; ths=[2*pi*i/nth for i in range(nth)]
    for ph in phs:
        for th in ths: vs.append(P(th,ph))
    for j in range(nph):
        for i in range(nth):
            th=(ths[i]+pi/nth); ph=(phs[j]+phs[j+1])/2
            if hole:
                dth=(math.degrees(th)-hole[0]+180)%360-180
                if abs(dth)<hole[2] and abs(math.degrees(ph)-hole[1])<hole[3]: continue
            a=j*nth+i; b=j*nth+(i+1)%nth; fs.append((a,b,b+nth,a+nth))
    vs.append(P(0,pi/2)); top=len(vs)-1
    for i in range(nth): fs.append((nph*nth+i,nph*nth+(i+1)%nth,top))
    o=omesh(vs,fs,paint); o.name='dome'
    for p in o.data.polygons: p.use_smooth=True
    if ribs:
        for i in range(0,nth,2):
            for j in range(nph):
                th=ths[i]; ph=phs[j]
                if hole and abs((math.degrees(th)-hole[0]+180)%360-180)<hole[2]-2 and abs(math.degrees(ph)-hole[1])<hole[3]-1: continue
                seg(P(th,phs[j]),P(th,phs[j+1]),.18,RIB,6)
        for j in range(1,nph,2):
            for i in range(nth):
                th=ths[i]; ph=phs[j]
                if hole and abs((math.degrees(th)-hole[0]+180)%360-180)<hole[2] and abs(math.degrees(ph)-hole[1])<hole[3]: continue
                seg(P(ths[i],ph),P(ths[(i+1)%nth],ph),.15,RIB,6)
    B.done('ribs')
    return o
def zmax_at(r): return DC[2]+math.sqrt(max(0,RD*RD-r*r))
def tower(x,y,w,d,h,col,seed,roof_garden=False):
    r=random.Random(seed); cm=M(col,.7,kind='wall'); tm=M(shade(col,.78),.6)
    B.box((x,y,h/2),(w/2,d/2,h/2),cm,.05)
    fl=3.0; n=int(h/fl)
    for k in range(n):
        z=1.6+k*fl
        if z>h-.8: break
        wm=WIN if r.random()<.62 else (WIN2 if r.random()<.5 else WIND)
        for sx in (-1,1): B.box((x+sx*(w/2+.01),y,z),(.01,d/2-.35,.55),wm,0)
        wm=WIN if r.random()<.62 else WIND
        for sy in (-1,1): B.box((x,y+sy*(d/2+.01),z),(w/2-.35,.01,.55),wm,0)
        B.box((x,y,z+.95),(w/2+.06,d/2+.06,.06),tm,.02)
    B.box((x,y,h+.15),(w/2+.12,d/2+.12,.15),tm,.03)
    if roof_garden:
        B.box((x,y,h+.4),(w/2-.3,d/2-.3,.12),M('#4E8A3C',.8,kind='grass'),.03)
        for i in range(3): tree(x+r.uniform(-w/3,w/3),y+r.uniform(-d/3,d/3),h+.45,.7+r.random()*.4,seed+i)
    else:
        B.box((x+r.uniform(-w/4,w/4),y+r.uniform(-d/4,d/4),h+.7),(.6,.6,.5),M('#8A929C',.5,metal=.4),.04)
def tree(x,y,z,s,seed):
    r=random.Random(seed); B.cyl((x,y,z+.9*s),.12*s,1.8*s,TRUNK,seg=8)
    for i in range(4): B.ico((x+r.uniform(-.5,.5)*s,y+r.uniform(-.5,.5)*s,z+(2.0+r.uniform(0,.8))*s),(.7+r.random()*.35)*s,LEAF if i%2 else LEAF2,sc=(1,1,.85),sub=1)
CORR=[True]
def city(mode='blue',crowd_n=0,hole=None):
    """plaza at origin, Chancellor hall to the north (+y). mode blue|sun"""
    r=random.Random(4)
    TILE=M('#DCD5C6',.55,kind='tile',h2='#CBC3B2',sc=.5); STONE=M('#BDB5A6',.7,kind='concrete',sc=.8)
    B.box((0,0,-.05),(RD,RD,.05),STONE,0)
    B.cyl((0,0,.01),10.0,.02,TILE,seg=48)
    # fountain
    B.cyl((0,0,.3),2.4,.6,M('#C9C1B0',.6,kind='concrete',sc=.5),seg=32); B.cyl((0,0,.56),2.15,.04,M('#5EB6E0',.1,emit=.35,spec=1.0),seg=32)
    B.cyl((0,0,1.1),.35,1.6,M('#C9C1B0',.6),seg=16); B.cyl((0,0,1.95),1.0,.12,M('#C9C1B0',.6),seg=24); B.cyl((0,0,2.4),.18,.9,M('#C9C1B0',.6),seg=12)
    B.ico((0,0,2.95),.32,M('#E0B25A',.3,metal=.8),sub=2)
    # planters + trees ring
    for i in range(8):
        a=2*pi*i/8+pi/8; x,y=6.6*math.cos(a),6.6*math.sin(a)
        if y>5.5: continue
        B.box((x,y,.35),(.9,.9,.35),M('#9C8E78',.7,kind='concrete',sc=.4),.04); B.box((x,y,.71),(.8,.8,.02),M('#4A3A2A',.9),0); tree(x,y,.7,1.0,i+11)
    # benches + lamps
    for i in range(8):
        a=2*pi*i/8; x,y=4.2*math.cos(a),4.2*math.sin(a)
        if y>3: continue
        B.box((x,y,.45),(.8,.25,.05),M('#8A5A3A',.6,kind='wood',sc=3),.02,rot=(0,0,a+pi/2)); B.box((x,y,.22),(.7,.2,.22),M('#3E4652',.5,metal=.6),.02,rot=(0,0,a+pi/2))
    LAMPS=[]
    for i in range(6):
        a=2*pi*i/6+.3; x,y=8.6*math.cos(a),8.6*math.sin(a)
        if y>6: continue
        B.cyl((x,y,1.9),.07,3.8,M('#2B313A',.4,metal=.7),seg=10); B.ico((x,y,3.9),.25,M('#FFE2B0',.3,emit=5.0),sub=2); LAMPS.append((x,y,3.9))
    # banners
    for x in (-5.5,5.5):
        B.cyl((x,5.0,2.5),.06,5.0,M('#2B313A',.4,metal=.7),seg=8); B.box((x+.55,5.0,3.6),(.5,.02,1.0),M('#1E5FA8',.7,kind='fabric'),.01)
    # Chancellor hall (north)
    HC='#E6E2D8'; hm=M(HC,.6,kind='wall'); B.box((0,15.5,7),(7,4,7),hm,.06)
    for x in (-5,-3,-1,1,3,5): B.cyl((x,11.2,3.5),.38,7.0,M('#F2EEE4',.5),seg=16)
    B.box((0,11.0,7.25),(6.4,.5,.25),hm,.04)
    for k in range(4): B.box((0,8.6+k*.55,.15*(k+1)),(6.0,.3,.15*(k+1)),M('#D8D2C4',.6,kind='concrete',sc=.6),.02)
    B.box((0,10.95,.6),(6.4,.45,.6),M('#D8D2C4',.6,kind='concrete',sc=.6),.02)
    B.box((0,11.4,2.2),(1.5,.06,2.2),M('#3A2A1E',.5,kind='wood'),.02)
    B.box((0,10.2,4.9),(2.6,1.2,.12),hm,.04)
    for x in [-2.4+i*.4 for i in range(13)]: B.box((x,9.05,5.3),(.04,.04,.35),M('#C9CDD6',.3,metal=.8),.005)
    B.box((0,9.05,5.66),(2.6,.06,.04),M('#C9CDD6',.3,metal=.8),.01)
    B.cyl((0,11.45,9.6),1.6,.12,M('#1E5FA8',.4,emit=.3),rot=(R(90),0,0),seg=40); B.cyl((0,11.38,9.6),1.2,.1,M('#E8E4D8',.4),rot=(R(90),0,0),seg=40)
    for k in range(3): B.box((0,11.32,9.2+k*.35),(.75,.02,.05),M('#1E5FA8',.4),.01,rot=(0,R(8*math.sin(k)),0))
    for x in (-4.5,4.5): B.box((x,11.4,5.5),(.9,.03,2.6),M('#1E5FA8',.7,kind='fabric'),.01)
    # towers ring
    k=0
    for ring,nn in ((15.5,14),(23.0,18),(29.5,20)):
        for i in range(nn):
            a=2*pi*(i+(.5 if ring==23 else 0))/nn; x,y=ring*math.cos(a),ring*math.sin(a)
            if ring==15.5 and y>8 and abs(x)<9: continue
            if CORR[0] and y<-8 and abs(x)<8: continue
            w=r.uniform(4,6.5); d=r.uniform(4,6.5); hmax=zmax_at(math.hypot(x,y)+4)-2.5; h=min(hmax,r.uniform(9,24) if ring<20 else r.uniform(6,16))
            if h<4: continue
            tower(x,y,w,d,h,r.choice(CONC),k*7+3,roof_garden=r.random()<.35); k+=1
    # sky bridges
    for i in range(10):
        a=2*pi*i/10; x0,y0=15.5*math.cos(a),15.5*math.sin(a); x1,y1=23*math.cos(a+.17),23*math.sin(a+.17); z=6+r.random()*5
        if y0>8 and abs(x0)<9: continue
        seg((x0,y0,z),(x1,y1,z),.55,M('#DDE6EC',.4,metal=.2),8)
    B.done('city')
    dome_shell(hole=hole)
    return LAMPS

# ------------------------------------------------------------------ pipe tunnel along the dome glass. glass plane y=0, inside y<0, outside y>0
ED=dict(x0=-7.0,x1=7.0,h=4.6,d=3.2,bx0=-1.6,bx1=1.6,bz0=.05,bz1=2.65,sc=(.35,1.62),cz=1.62)
def crack_pts(seed=5,x0=-5.2,x1=5.2,z=1.62):
    r=random.Random(seed); pts=[]; x=x0; zz=z
    while x<x1: pts.append((x,zz)); x+=r.uniform(.08,.22); zz=z+.12*math.sin(x*.9)+r.uniform(-.035,.035)
    pts.append((x1,z)); return pts
def crack_obj(width=.006,glow=6.0,col='#FFF3D6',y=-.05,seed=5,branches=True):
    pts=crack_pts(seed); vs=[]; fs=[]
    def strip(P,w):
        b=len(vs)
        for i,(x,z) in enumerate(P):
            ww=w*(.6+.4*math.sin(i*1.7)**2); vs.append((x,y,z-ww)); vs.append((x,y,z+ww))
        for i in range(len(P)-1): fs.append((b+2*i,b+2*i+2,b+2*i+3,b+2*i+1))
    strip(pts,width)
    if branches:
        r=random.Random(seed+1)
        for k in range(14):
            i=r.randrange(2,len(pts)-3); x,z=pts[i]; sgn=r.choice((-1,1)); P=[(x,z)]
            for j in range(r.randint(2,4)): x+=r.uniform(.05,.14)*r.choice((-1,1)); z+=sgn*r.uniform(.04,.1); P.append((x,z))
            strip(P,width*.6)
    o=omesh(vs,fs,M(col,.3,emit=glow)); o.name='crack'; return o
def edge(mode='day',scrape=False,burst=False,painted=False,seed=1):
    """mode: day|night|alarm|dawn. returns dict of handles"""
    x0,x1,h,d=ED['x0'],ED['x1'],ED['h'],ED['d']; out={}
    GRATE=M('#4E5560',.45,metal=.6,kind='tile',h2='#3E444D',sc=6); WALL=M('#5A6470',.6,metal=.3,kind='wall'); CEIL=M('#3A414B',.6,metal=.4)
    STEEL=M('#7B8794',.35,metal=.8); TEAL=M('#2E8C8A',.35,metal=.5); COPPER=M('#B8703E',.3,metal=.85); REDP=M('#B23A2E',.4,metal=.4); YEL=M('#F2C12E',.5); BLK=M('#1B1D22',.5)
    B.box(((x0+x1)/2,-d/2,-.05),((x1-x0)/2,d/2,.05),GRATE,0); B.box(((x0+x1)/2,-d/2,h+.05),((x1-x0)/2,d/2,.05),CEIL,0); B.box(((x0+x1)/2,-d-.05,h/2),((x1-x0)/2,.05,h/2),WALL,0)
    for xx in (x0,x1): B.box((xx,-d/2,h/2),(.05,d/2,h/2),WALL,0)
    # hazard band near glass
    for i in range(int((x1-x0)/.3)):
        B.box((x0+.15+i*.3,-.3,.004),(.15,.12,.004),YEL if i%2 else BLK,0,rot=(0,0,0))
    # railing (inner side)
    for x in [x0+.5+i*1.0 for i in range(int(x1-x0))]: B.cyl((x,-2.75,.55),.03,1.1,STEEL,seg=8)
    for z in (.55,1.08): seg((x0,-2.75,z),(x1,-2.75,z),.03,STEEL,8)
    # back wall pipes + valves + gauges
    for z,rr,m in ((.4,.11,TEAL),(.75,.07,COPPER),(3.55,.16,STEEL),(3.95,.09,REDP),(4.22,.07,COPPER)): seg((x0,-d+.25,z),(x1,-d+.25,z),rr,m,12)
    for x in (-5.5,-2.0,1.5,4.8): seg((x,-d+.22,0),(x,-d+.22,h),.08,STEEL,10); B.cyl((x,-d+.42,1.6),.2,.04,REDP,rot=(R(90),0,0),seg=16)
    for x in (-4.2,.2,3.2): B.cyl((x,-d+.08,2.2),.16,.06,STEEL,rot=(R(90),0,0),seg=16); B.cyl((x,-d+.115,2.2),.13,.01,M('#F4F1E6',.4,emit=.4),rot=(R(90),0,0),seg=16)
    # big air duct along the glass (Nova's job)
    seg((x0,-.62,1.05),(x1,-.62,1.05),.22,M('#9AA6B2',.3,metal=.7),16)
    for x in [x0+.7+i*1.4 for i in range(10)]: B.cyl((x,-.62,1.05),.25,.06,M('#6E7884',.35,metal=.75),rot=(0,R(90),0),seg=16)
    for x in (-3.6,2.6): B.box((x,-.62,.5),(.05,.05,.5),STEEL,.01)
    # ceiling pipes + lamps
    for y,rr,m in ((-.6,.09,TEAL),(-1.5,.12,STEEL),(-2.4,.07,COPPER)): seg((x0,y,h-.25),(x1,y,h-.25),rr,m,10)
    LAMPS=[]
    for x in (-5,-1.7,1.7,5):
        B.box((x,-1.5,h-.42),(.45,.12,.05),M('#2B313A',.4,metal=.6),.02); lm=M('#FFE9C8',.3,emit=(4.0 if mode=='day' else .25 if mode in('night','dawn') else .6)); B.box((x,-1.5,h-.48),(.4,.09,.02),lm,0); LAMPS.append((x,-1.5,h-.6))
    # warning signs
    SGN=M('#F2C12E',.5)
    for x in (-3.8,3.6):
        B.box((x,-2.78,1.45),(.45,.02,.3),SGN,.02); B.box((x,-2.797,1.45),(.42,.002,.27),BLK,0)
        text('KEEP AWAY',(x,-2.8,1.53),(0,-1,0),.13,SGN,ex=.002); text('FROM THE GLASS',(x,-2.8,1.36),(0,-1,0),.09,SGN,ex=.002)
    # dome frame ribs at y=0
    for x in [-6.4,-4.8,-1.6,1.6,4.8,6.4]: B.box((x,0,h/2),(.09,.12,h/2),RIB,.02)
    for z in (.05,ED['bz1'],h-.05): B.box(((x0+x1)/2,0,z),((x1-x0)/2,.12,.07),RIB,.02)
    # paint layer (inner face, y=-.035) around the burst rectangle
    bx0,bx1,bz0,bz1=ED['bx0'],ED['bx1'],ED['bz0'],ED['bz1']
    for (a,b_,c,e_) in ((x0,bx0,0,h),(bx1,x1,0,h),(bx0,bx1,bz1,h)): B.box(((a+b_)/2,-.035,(c+e_)/2),((b_-a)/2,.008,(e_-c)/2),PAINT_E,0)
    B.done('edge')
    # paint tiles inside the burst rectangle (removable)
    tiles=[]; T=.2
    nx=int(round((bx1-bx0)/T)); nz=int(round((bz1-bz0)/T))
    for i in range(nx):
        for j in range(nz):
            cx=bx0+T*(i+.5); cz=bz0+(bz1-bz0)*(j+.5)/nz
            o=obox((cx,-.035,cz),(T/2,.008,(bz1-bz0)/nz/2),PAINT_E,0); tiles.append(o)
    out['tiles']=tiles
    # glass (one sheet unless bursting)
    if not burst:
        g=obox(((x0+x1)/2,0,h/2),((x1-x0)/2,.01,h/2),GLASSM,0); g.name='glass_dome'
    out['crack']=crack_obj(width=.007 if not scrape else .014, glow=(7.0 if mode in('day',) else 5.0), col=('#FFF3D6' if mode!='night' else '#CFE6FF'))
    if painted:
        out['fresh']=[]
        pts=crack_pts()
        for i in range(0,len(pts)-1,3):
            a=pts[i]; b_=pts[min(i+3,len(pts)-1)]; out['fresh'].append(obox(((a[0]+b_[0])/2,-.055,(a[1]+b_[1])/2),(abs(b_[0]-a[0])/2+.06,.004,.16),FRESH,.01))
    # outside: desert at dawn, seen through holes
    desert_backdrop()
    # lights
    for p in LAMPS:
        if mode=='day': area(p,140,(.9,.3),(1,.92,.8),shadow=(p[0]==-1.7))
        elif mode=='alarm': area(p,25,(.9,.3),(1,.9,.8),shadow=False)
        else: area(p,22,(.9,.3),(.6,.75,1),shadow=False)
    if mode in ('dawn','alarm'): sun((R(-78),0,0),3.0,(1,.8,.58),2.0)
    out['glowfill']=area((0,-.9,1.8),(60 if mode=='day' else 30),(10,3),(.45,.7,1.0),rot=(R(-90),0,0),shadow=False)
    return out
def desert_backdrop(sunz=6.0):
    B.box((0,150,-.4),(220,150,.3),SAND,0)
    r=random.Random(9)
    for i in range(26):
        x=r.uniform(-90,90); y=r.uniform(15,160); s=r.uniform(6,22); B.ico((x,y,-s*.55),s,SAND2 if i%3 else SAND,sc=(1.6,1,.55),sub=2)
    # sky bands behind (emissive so they read through the hole)
    for z0,z1,c,e in ((-2,8,'#FFB067',2.2),(8,20,'#F7C7A0',1.8),(20,45,'#B9C6E6',1.4),(45,140,'#6E8FCC',1.2)):
        B.box((0,260,(z0+z1)/2),(400,1,(z1-z0)/2),M(c,.5,emit=e),0)
    B.cyl((-14,258,sunz),7,.5,M('#FFF1C8',.2,emit=14.0),rot=(R(90),0,0),seg=40)
    B.done('desert')

# ------------------------------------------------------------------ Pops' workshop
def workshop():
    WOOD=M('#8A5E3C',.55,kind='wood',sc=2); PL=M('#C9B79C',.8,kind='wall'); FLR=M('#7A5A40',.6,kind='wood',sc=1.5); MET=M('#6E7884',.4,metal=.7)
    x0,x1,y0,y1,h=-3.2,3.2,-2.6,2.6,3.2
    B.box((0,0,-.05),(3.3,2.7,.05),FLR,0); B.box((0,0,h+.05),(3.3,2.7,.05),M('#5A4636',.8,kind='wood'),0)
    B.box((0,y1,h/2),(3.3,.06,h/2),PL,0); B.box((x0,0,h/2),(.06,2.7,h/2),PL,0); B.box((x1,0,h/2),(.06,2.7,h/2),PL,0)
    for x in (-2.4,-.8,.8,2.4): B.box((x,0,h-.12),(.1,2.6,.12),WOOD,.02)
    # round porthole window on back wall showing the painted dome
    B.cyl((1.9,y1-.02,2.0),.62,.1,M('#B8873A',.3,metal=.85),rot=(R(90),0,0),seg=32); B.cyl((1.9,y1-.05,2.0),.52,.04,M('#2A86C8',.5,emit=.9),rot=(R(90),0,0),seg=32)
    # workbench along back wall
    B.box((-.8,y1-.55,.95),(1.9,.5,.06),WOOD,.02)
    for x in (-2.55,.95):
        for y in (y1-.95,y1-.15): B.box((x,y,.46),(.06,.06,.46),WOOD,.01)
    B.box((-.8,y1-.55,.3),(1.8,.45,.03),WOOD,.01)
    # pegboard + tools
    B.box((-.8,y1-.08,1.9),(1.7,.02,.75),M('#B89A70',.8),.01)
    r=random.Random(3)
    for i in range(14):
        x=-2.3+i*.22; c=r.choice(['#C9CDD6','#B23A2E','#2E6E78','#E0B25A'])
        B.box((x,y1-.12,1.95+r.uniform(-.3,.3)),(.025,.02,r.uniform(.12,.3)),M(c,.35,metal=.6),.005)
    # vise + toolbox + lamp on bench
    B.box((-2.1,y1-.6,1.1),(.12,.18,.1),MET,.02); B.box((.4,y1-.6,1.12),(.3,.18,.14),M('#B23A2E',.4,metal=.4),.02)
    B.cyl((-.2,y1-.55,1.02),.12,.04,MET,seg=12); seg((-.2,y1-.55,1.02),(-.1,y1-.65,1.6),.025,MET); B.cyl((.05,y1-.75,1.62),.12,.15,M('#2E6E78',.5),rot=(R(60),0,0),seg=14,r2=.06)
    # blueprint of the dome on the left wall
    B.box((x0+.07,.2,1.9),(.02,1.1,.75),M('#1D3E6E',.6),.01)
    BL=M('#E8F2FF',.4,emit=1.2)
    for i in range(24):
        a=pi*i/23; a2=pi*(i+1)/23
        p=(x0+.1,.2+.8*math.cos(a),1.35+.95*math.sin(a)*.95); q=(x0+.1,.2+.8*math.cos(a2),1.35+.95*math.sin(a2)*.95); seg(p,q,.008,BL,4)
    seg((x0+.1,-.6,1.35),(x0+.1,1.0,1.35),.008,BL,4)
    for k in range(4): seg((x0+.1,.2,1.35),(x0+.1,.2+.8*math.cos(pi*(k+1)/5),1.35+.9*math.sin(pi*(k+1)/5)),.006,BL,4)
    # shelves with jars
    for z in (1.4,2.0,2.6):
        B.box((x1-.25,-.6,z),(.2,1.2,.025),WOOD,.01)
        for k in range(6): B.cyl((x1-.25,-1.6+k*.38,z+.12),.07,.2,M(r.choice(['#C9A26A','#8FB8A8','#D8C8A0','#A8B8C8']),.2,alpha=.85),seg=10)
    # armchair + rug + side table + teapot
    B.box((1.6,-1.3,.03),(1.2,.9,.01),M('#9C3A2E',.9,kind='fabric'),0)
    B.box((2.1,-1.6,.32),(.45,.45,.18),M('#4E6A58',.8,kind='fabric'),.06); B.box((2.1,-1.98,.75),(.45,.1,.45),M('#4E6A58',.8,kind='fabric'),.06)
    for s in (-1,1): B.box((2.1+s*.45,-1.6,.5),(.08,.45,.25),M('#4E6A58',.8,kind='fabric'),.04)
    B.cyl((1.1,-1.8,.45),.3,.04,WOOD,seg=16); B.cyl((1.1,-1.8,.22),.04,.44,WOOD,seg=8); B.ico((1.1,-1.8,.56),.1,M('#E8E4D8',.3),sub=2)
    # old photo frames
    for i,x in enumerate((-2.6,-2.0)): B.box((x,y1-.08,2.85),(.22,.02,.17),M('#3A2A1E',.5),.01); B.box((x,y1-.1,2.85),(.18,.01,.13),M(['#9A8A70','#7E9AA8'][i],.7),0)
    B.done('workshop')
    lamp=point((-.2,y1-.9,2.1),60,(1,.78,.5),.15); hang=point((0,-.3,2.7),70,(1,.82,.58),.3)
    B.cyl((0,-.3,2.85),.25,.2,M('#2E3A2E',.5),seg=16,r2=.08); B.ico((0,-.3,2.74),.09,M('#FFE2B0',.3,emit=6.0),sub=2); B.done('lamp')
    fill=area((0,-2.2,2.4),80,(3,2),(1,.86,.7),rot=(R(70),0,0),shadow=False)
    return dict(lamp=lamp,hang=hang)

# ------------------------------------------------------------------ outside: the dried seabed (grass=True for the ending)
def seabed(grass=False,hole=True,dome=True):
    G=M('#6FAE48',.85,kind='grass',h2='#4E8E36') if grass else SAND
    B.box((0,0,-.3),(300,300,.3),G,0)
    r=random.Random(12)
    for i in range(30):
        x=r.uniform(-140,140); y=r.uniform(-200,-90); s=r.uniform(8,26)
        B.ico((x,y,-s*.6),s,(M('#5E9E40',.85,kind='grass') if grass else (SAND2 if i%3 else SAND)),sc=(1.7,1,.5),sub=2)
    # dried coral + rocks
    for i in range(40):
        x=r.uniform(-34,34); y=r.uniform(-80,-39)
        if abs(x)<5 and y>-52: continue
        c=r.choice(['#EDE4D6','#E8D2C8','#D9CBB8']) if not grass else r.choice(['#EDE4D6','#9A9488'])
        for k in range(r.randint(2,5)): B.cyl((x+r.uniform(-.4,.4),y+r.uniform(-.4,.4),.5),.08,1.0+r.random(),M(c,.8),rot=(r.uniform(-.5,.5),r.uniform(-.5,.5),0),seg=6)
        B.ico((x+r.uniform(-1,1),y+r.uniform(-1,1),.1),r.uniform(.3,.8),M('#8E8678',.9),sc=(1.3,1,.6),sub=1)
    # shipwreck
    HULL=M('#5A4636',.8,kind='wood',sc=2)
    B.box((-16,-56,1.2),(5,1.6,1.4),HULL,.3,rot=(R(18),R(-8),R(28))); B.cyl((-15.5,-55.6,4.2),.15,6,HULL,rot=(R(25),0,R(28)),seg=8)
    B.box((-13,-57,.8),(1.5,1.2,.9),HULL,.2,rot=(R(-10),0,R(20)))
    if grass:
        for i in range(60):
            x=r.uniform(-45,45); y=r.uniform(-110,-42)
            if abs(x)<7 and y>-62: continue
            tree(x,y,0,r.uniform(1.4,2.2),i+300)
        for i in range(260):
            x=r.uniform(-22,22); y=r.uniform(-62,-37); B.ico((x,y,.12),.07,M(r.choice(['#F2E25A','#F2F2F2','#E87AA0','#B88AE0']),.6),sub=1)
    B.done('seabed')
    hl=(270,9,9,8) if hole else None
    if dome: dome_shell(hole=hl,paint=M('#2B76B4',.45,spec=.8))
    return dict()
