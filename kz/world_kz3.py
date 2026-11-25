# Small sets: pm_stage(), moon(), beach(), movie_street(), rooftop dressing, flood props, bed shop.
def star_world(top='#050616',glow='#1A1450',strength=1.0,stars=420):
    sc=bpy.context.scene; w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; nt=w.node_tree; bg=nt.nodes['Background']
    tc=nt.nodes.new('ShaderNodeTexCoord'); vo=nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value=stars; nt.links.new(tc.outputs['Generated'],vo.inputs['Vector'])
    rp=nt.nodes.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].position=.0; rp.color_ramp.elements[0].color=(1,1,1,1); rp.color_ramp.elements[1].position=.06; rp.color_ramp.elements[1].color=(0,0,0,1)
    nt.links.new(vo.outputs['Distance'],rp.inputs[0]); nz=nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value=2.0; nt.links.new(tc.outputs['Generated'],nz.inputs['Vector'])
    r2=nt.nodes.new('ShaderNodeValToRGB'); r2.color_ramp.elements[0].color=hexc(top); r2.color_ramp.elements[1].color=hexc(glow); r2.color_ramp.elements[0].position=.45; nt.links.new(nz.outputs['Fac'],r2.inputs[0])
    ad=nt.nodes.new('ShaderNodeMix'); ad.data_type='RGBA'; ad.blend_type='ADD'; ad.inputs['Factor'].default_value=1.0; nt.links.new(r2.outputs['Color'],ad.inputs[6]); nt.links.new(rp.outputs['Color'],ad.inputs[7])
    nt.links.new(ad.outputs[2],bg.inputs[0]); bg.inputs[1].default_value=strength
    sc.render.resolution_x=1080; sc.render.resolution_y=1920; sc.render.resolution_percentage=PCT; sc.render.engine='BLENDER_EEVEE'; e=sc.eevee
    e.taa_render_samples=SAMPLES; e.use_gtao=True; e.gtao_distance=1.0; e.gtao_factor=1.2; e.use_bloom=True; e.bloom_intensity=.05; e.bloom_threshold=1.0; e.use_soft_shadows=True
    e.shadow_cascade_size='2048'; e.shadow_cube_size='1024'; e.use_shadow_high_bitdepth=True
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='Medium High Contrast'
def flag_pk(x,y,h=4.6,rz=0,parent=None):
    """green flag with white hoist band, crescent and star on a gold pole"""
    e=empty((x,y,0),parent,rot=(0,0,R(rz))); gold=M('#D9B24A',.3,metal=.9); gr=M('#0E5A36',.6,kind='fabric'); wh=M('#F6F4EE',.6,kind='fabric')
    ocyl((0,0,h/2),.045,h,gold,e,rot=(0,0,0),seg=8); oico((0,0,h+.08),.1,gold,e,sub=1); ocyl((0,0,.06),.3,.12,gold,e,rot=(0,0,0),seg=14)
    obox((.26,0,h-.75),(.22,.012,.62),wh,.004,e); obox((1.08,0,h-.75),(.62,.012,.62),gr,.004,e)
    for n in (-1,1):
        ocyl((1.1,n*.016,h-.75),.3,.006,wh,e,seg=24); ocyl((1.2,n*.02,h-.7),.25,.006,gr,e,seg=24); obox((1.36,n*.02,h-.6),(.075,.004,.075),wh,0,e,rot=(0,R(45),0))
    return e
def pm_stage():
    wood=M('#6B4226',.5,kind='wood',sc=.5); B.box((0,2,-.05),(12,10,.05),M('#7A1F2E',.85,kind='fabric'),0)
    B.box((0,6.0,3.5),(12,.2,3.6),M('#123E2A',.85,kind='fabric'),0)
    for k in range(25): B.box((-12+k*1.0,5.78,3.5),(.2,.1,3.6),M('#0E3322' if k%2 else '#17513A',.85,kind='fabric'),.08)
    B.box((0,5.7,6.6),(12,.3,.5),M('#D9B24A',.4,metal=.6),.05); B.box((0,5.6,.25),(12,.25,.25),M('#D9B24A',.4,metal=.6),.03)
    sign('PRIME MINISTER',(0,5.55,4.95),.34,'#F6E7B0','#0E3322',n=(0,-1,0),e=1.2,pad=.22,th=.08,frame='#D9B24A',always=True)
    B.cyl((0,5.62,3.4),.95,.08,M('#D9B24A',.3,metal=.8),rot=(R(90),0,0),seg=36); B.cyl((0,5.56,3.4),.8,.06,M('#0E5A36',.5),rot=(R(90),0,0),seg=36)
    B.cyl((-.08,5.5,3.42),.42,.05,M('#F6F4EE',.5),rot=(R(90),0,0),seg=28); B.cyl((.05,5.47,3.48),.36,.05,M('#0E5A36',.5),rot=(R(90),0,0),seg=28); B.box((.3,5.47,3.62),(.1,.02,.1),M('#F6F4EE',.5),0,rot=(0,R(45),0))
    # podium
    B.box((0,.0,.62),(.95,.5,.62),wood,.04); B.box((0,-.05,1.3),(1.1,.62,.06),M('#4A2C18',.5,kind='wood',sc=.5),.03,rot=(R(-8),0,0)); B.box((0,-.52,.7),(.6,.02,.42),M('#D9B24A',.3,metal=.8),.02)
    sign('PM',(0,-.55,.7),.44,'#0E3322','#D9B24A',n=(0,-1,0),pad=.12,th=.02)
    cols=['#C8372D','#2B58C9','#F2C14E','#16171C','#35975A']
    for i in range(5):
        x=-.7+i*.35; B.cyl((x,-.25,1.62),.018,.5,M('#22242B',.4),rot=(R(-20),0,R((i-2)*-7)),seg=6); B.box((x-(i-2)*.03,-.36,1.9),(.085,.085,.1),M(cols[i],.5),.02); B.ico((x-(i-2)*.035,-.4,2.02),.07,M('#2A2C34',.8),sub=1)
    B.done('pm')
    F=[flag_pk(-3.3,3.2,4.9),flag_pk(1.55,3.2,4.9)]
    S,A,w,bg=setup_interior('evening',room=(0,-1,7.0),res=PCT,samples=SAMPLES,shadow_dist=22); A.data.energy=260; A.data.size=9
    point((-4,-6,5),1500,(1,.95,.86),r=1.5,shadow=True); point((5,-5,4),900,(1,.9,.8),r=1.5,shadow=False); point((0,3,6.5),500,(1,.85,.6),r=1,shadow=False)
    return dict(flags=F)
def moon():
    reg=M('#9A9A9E',.95,kind='wall'); rk=M('#77777C',.95); r=random.Random(6)
    B.box((0,30,-.5),(120,120,.5),reg,0)
    for i in range(46):
        x=r.uniform(-30,30); y=r.uniform(-4,70); s=r.uniform(.5,3.2)
        if abs(x)<4.5 and y<6: continue
        B.cyl((x,y,.02),s,.06,M('#6E6E74',.95),seg=18); B.cyl((x,y,.05),s*.82,.06,M('#84848A',.95),seg=18)
        for k in range(10): a=k*.63; B.ico((x+math.cos(a)*s,y+math.sin(a)*s,.05),s*.2,reg,sc=(1,1,.5),sub=1)
    for i in range(40): B.ico((r.uniform(-26,26),r.uniform(-3,50),r.uniform(0,.15)),r.uniform(.12,.5),rk,sc=(1,r.uniform(.7,1.2),r.uniform(.5,.9)),sub=1)
    for i in range(7): B.ico((-60+i*20+r.uniform(-4,4),95,-3),r.uniform(9,16),reg,sc=(1.6,1,.55),sub=2)
    B.done('moon')
    star_world()
    bpy.ops.object.light_add(type='SUN'); S=bpy.context.object; S.rotation_euler=(R(58),0,R(-48)); S.data.energy=3.6; S.data.color=(1,.97,.92); S.data.angle=R(1.0)
    earth=oico((-9,120,40),17,M('#2B6FD8',.6,emit=.35),sub=4)
    for (a,b,c,sx,sy) in ((-.5,.2,.3,6,5),(.35,-.3,.1,5,7),(.1,.5,-.2,4,3.5),(-.2,-.5,.4,3.5,3),(.55,.3,.5,3,3)):
        v=Vector((a,-1,b)).normalized()*16.6; oico((-9+v.x,120+v.y,40+v.z+c),1,M('#3FA85A',.7,emit=.25),None,sc=(sx,1.2,sy),sub=2)
    for i in range(7): v=Vector((r.uniform(-.8,.8),-1,r.uniform(-.8,.8))).normalized()*17.0; oico((-9+v.x,120+v.y,40+v.z),1,M('#F4F8FF',.6,emit=.5),None,sc=(r.uniform(3,6),1,r.uniform(1,2)),sub=2)
    point((0,-6,3.5),700,(.8,.86,1.0),r=2,shadow=False)
    return dict(earth=earth)
def beach(mood='night',seed=4,sign_at=(14,-5.2),ssize=.52):
    """Sea View beach. land y<0, shoreline ~y=3, sea beyond. skyline along +x."""
    night=mood=='night'; NIGHT[0]=1.0 if night else 0.0; r=random.Random(seed)
    sand=M('#D9C39A' if not night else '#A89878',.95,kind='wall'); wet=M('#B8A27C' if not night else '#8A7A60',.6)
    B.box((0,-40,-.1),(160,46,.1),sand,0); B.box((0,4,-.14),(160,3,.1),wet,0,rot=(R(-1.5),0,0))
    for i in range(60): B.ico((r.uniform(-60,60),r.uniform(-30,2),-.02),r.uniform(.5,1.6),sand,sc=(1,1,.12),sub=1)
    sea=M('#1E4E7A' if not night else '#0E2440',.08,spec=1.0); B.box((0,130,-.32),(400,126,.1),sea,0)
    fm=M('#F4F8FF',.5,emit=.5 if night else 0)
    for k in range(4):
        y=5.2+k*4.5
        for j in range(18): B.box((-70+j*8+r.uniform(-2,2),y+r.uniform(-.4,.4),-.2),(r.uniform(1.5,3.5),.16,.02),fm,.01)
    # shore dressing: huts with thatched umbrellas, boat, sign, palms, stall
    for i,x in enumerate((-17,-9.5,11,19,27)):
        B.cyl((x,-7.5,1.5),.09,3.0,M('#6B4A2E',.8),seg=8); B.cyl((x,-7.5,3.2),2.0,.7,M('#C9A45A',.9,kind='fabric'),seg=14,r2=.15)
        for k in range(14): a=k*.45; B.box((x+math.cos(a)*1.85,-7.5+math.sin(a)*1.85,2.78),(.2,.05,.14),M('#B8924A',.9),0,rot=(0,0,a))
        B.cyl((x,-7.5,.5),.75,.06,M('#8A5A36',.7,kind='wood',sc=.6),seg=14)
    for i,x in enumerate((-30,-22,5,34,44)): palm(x,-11-(i%2)*2,1.25,seed=i+3)
    bm=M('#2B6FB8',.6,kind='wood',sc=.5); B.box((-13,-1.5,.5),(2.6,.9,.42),bm,.25,rot=(0,R(-5),R(18))); B.box((-13,-1.5,.82),(2.4,.75,.06),M('#F4F1EA',.6),.02,rot=(0,R(-5),R(18))); B.box((-13,-1.5,.98),(2.3,.06,.06),M('#C8372D',.6),0,rot=(0,R(-5),R(18)))
    sx_,sy_=sign_at; hw_=14*ssize*.345+.3
    for sx in (-hw_+.25,hw_-.25): B.cyl((sx_+sx,sy_,1.2),.07,2.4,M('#6B4A2E',.8),seg=6)
    sign('SEA VIEW BEACH',(sx_,sy_-.08,2.7),ssize,'#FFFFFF','#1E6A8A',n=(0,-1,0),e=2.2,pad=.3,th=.1,frame='#F4F1EA',always=True)
    # promenade wall + lamps + skyline far along the shore
    B.box((0,-16,.5),(160,.4,.5),M('#C9C2B2',.85,kind='concrete',sc=.5),.03)
    for x in range(-60,61,12): street_lamp(x,-16.5,6.5,arms=(1,))
    for i in range(22):
        x=-150+i*14+r.uniform(-3,3); w=r.uniform(8,13); h=r.uniform(14,52); yb=-34-r.uniform(0,14)
        B.box((x,yb,h/2),(w/2,6,h/2),M(r.choice(['#3A4258','#2E3648','#454C60']) if night else r.choice(['#C9D6E0','#D9C4A8','#E8E2D6']),.8),0)
        for f in range(int(h//3.4)):
            for k in range(int(w//2.4)):
                if r.random()<.45: B.box((x-w/2+1.2+k*2.4,yb+6.02,3.5+f*3.4),(.6,.04,.8),lit(r.choice(WINL),2.4) if night else M('#2A3444',.2,spec=.9),0)
    B.done('beach')
    S=setup_world(mood,70)
    mo=None
    if night:
        mo=oico((6,330,62),26,M('#FFF6D8',.4,emit=4.0),sub=3)
        for k in range(9): obox((6+r.uniform(-2.5,2.5),14+k*9,-.2),(r.uniform(1.2,3.0),.5,.02),M('#FFF2C8',.3,emit=1.6,alpha=.55),0)
        point((0,-4,5),900,(.75,.85,1.0),r=3,shadow=False); point((0,8,4.5),1200,(.6,.8,1.0),r=3,shadow=True)
    return dict(moon=mo,sun=S)
def movie_street():
    """generic foreign-movie downtown: glass canyon, yellow cabs, hydrant. camera looks along +x."""
    NIGHT[0]=.6; r=random.Random(12)
    B.box((40,0,-.05),(140,6.5,.05),M('#33353B',.8,kind='asphalt'),0); B.box((40,0,-.3),(200,120,.2),M('#77787C',.9),0)
    for k in range(40): B.box((-60+k*6,0,.004),(1.4,.09,.004),M('#F2C14E',.5),0)
    for s in (-1,1):
        B.box((40,s*8.2,.1),(140,1.7,.1),M('#9A9CA0',.85,kind='concrete',sc=.8),0)
        x=-60; i=0
        while x<170:
            w=r.uniform(12,20); tower(x+w/2,s*10,w,14,r.randint(12,26),r.choice(['#8E97A6','#7C8696','#9AA4B2','#6E7888']),s,900+i*2+(s>0),style=2,sign_=None); x+=w+.6; i+=1
        for k in range(12): B.cyl((-50+k*17,s*6.9,2.6),.07,5.2,M('#2A2C34',.4),seg=6); B.box((-50+k*17,s*6.3,5.2),(.1,.6,.05),M('#2A2C34',.4),0); B.ico((-50+k*17,s*5.8,5.1),.16,lit('#DFF0FF',9,always=True),sub=1)
    B.cyl((7.4,7.3,.4),.16,.8,M('#C8372D',.5),seg=10); B.ico((7.4,7.3,.85),.18,M('#C8372D',.5),sub=1)
    B.done('movie')
    S=setup_world('invade',70)
    cabs=[kcar((3.4,4.3,0),-28,'#F2C14E',seed=3)]
    for c in cabs: obox((-.18,0,1.52),(.3,.2,.08),lit('#FFE14A',3,always=True),.02,c['root'])
    return dict(cabs=cabs)
def letterbox(lens,frac=.1):
    """black bars parented to the camera (movie look)"""
    d=.5; hv=d*18.0/lens; out=[]
    for s in (-1,1):
        o=obox((0,s*hv*(1-frac),-d),(d*.7,hv*frac,.001),M('#000000',1.0,spec=0),0,CAM); o.name='bar'; out.append(o)
    return out
def rooftop():
    """dressing on the ROOF building (south side, opposite the restaurant): zombies' lookout"""
    z=ROOF_Z; y0=-BW; y1=-BW-12.0; x0,x1=ROOF_X; r=random.Random(3); wall=M('#D99A8A',.85,kind='wall'); tr=M('#F2EBDA',.8)
    B.box(((x0+x1)/2,(y0+y1)/2,z+.02),((x1-x0)/2,6.0,.03),M('#B8785A',.8,kind='tile',sc=1.6,h2='#A86A4E'),0)
    for (cx,cy,hx,hy) in (((x0+x1)/2,y1+.15,(x1-x0)/2,.15),(x0+.15,(y0+y1)/2,.15,6.0),(x1-.15,(y0+y1)/2,.15,6.0)): B.box((cx,cy,z+.55),(hx,hy,.55),wall,.02); B.box((cx,cy,z+1.13),(hx+.05,hy+.05,.05),tr,.01)
    # stair-head room with door + bulb
    B.box((x0+2.0,y1+2.0,z+1.5),(1.7,1.7,1.5),wall,.03); B.box((x0+2.0,y1+2.0,z+3.08),(1.9,1.9,.1),tr,.02); B.box((x0+3.72,y1+2.0,z+1.1),(.03,.55,1.1),M('#2E7A6A',.6,kind='wood',sc=.8),.01)
    B.ico((x0+3.9,y1+2.0,z+2.55),.1,lit('#FFE6A0',8,always=True),sub=1)
    # water tank on stand, dish, AC units
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((x1-2.4+sx*.8,y1+2.4+sy*.8,z+.8),.07,1.6,M('#5A5E66',.5),seg=6)
    B.cyl((x1-2.4,y1+2.4,z+2.5),1.15,1.8,M('#2B6FB8',.5),seg=20); B.cyl((x1-2.4,y1+2.4,z+3.45),.5,.12,M('#1E4E8A',.5),seg=14)
    B.cyl((x1-5.2,y1+1.4,z+.6),.04,1.2,M('#5A5E66',.5),seg=6); B.cyl((x1-5.2,y1+1.5,z+1.3),.6,.1,M('#D8DCE2',.4),rot=(R(58),0,0),seg=18)
    B.box((x0+5.4,y1+.8,z+.42),(.5,.3,.4),M('#D8DCE2',.5),.03); B.cyl((x0+5.4,y1+1.12,z+.42),.24,.02,M('#5A5E66',.5),rot=(R(90),0,0),seg=12)
    # clothesline
    for sx in (x0+5.0,x1-4.2): B.cyl((sx,y1+4.6,z+1.2),.04,2.4,M('#5A5E66',.5),seg=6)
    B.box(((x0+5.0+x1-4.2)/2,y1+4.6,z+2.3),((x1-4.2-x0-5.0)/2,.008,.008),M('#16171C',.5),0)
    for k in range(8): B.box((x0+5.6+k*1.0,y1+4.6,z+1.85),(.3,.012,.42 if k%2 else .3),M(['#E8554D','#F2C14E','#4D8FE8','#F4F1DE','#9B6FD0','#6FC38A','#FF8A3A','#F4F1EA'][k],.9,kind='fabric'),.004)
    # potted plants + pigeon coop
    for k in range(5): xx=x0+1.0+k*.9; B.cyl((x1-.8,y1+5.0+k*1.1,z+.25),.2,.4,M('#B5542E',.7),seg=10); B.ico((x1-.8,y1+5.0+k*1.1,z+.68),.3,M(['#3F8A3A','#4F9A4A'][k%2],.85,kind='leaves'),sub=1)
    B.box((x0+1.2,y1+6.2,z+.7),(.6,.9,.65),M('#7A4E2A',.6,kind='wood',sc=.6),.02); B.box((x0+1.82,y1+6.2,z+.75),(.01,.8,.5),M('#C9CED8',.3,metal=.6,alpha=.5),0)
    for k in range(3): B.ico((x0+1.3+k*.05,y1+5.7+k*.45,z+1.48),.12,M(['#8A8E96','#F4F1EA','#5A5E66'][k],.7),sc=(1,1.5,.9),sub=1)
    B.done('rooftop')
    return dict(z=z)
def flood_props():
    """things drifting in the flooded street"""
    P=[]
    for (x,y,c) in ((-3,2.6,'#C8372D'),(6,-2.8,'#2B58C9')):
        e=pchair(x,y,37,c); e.location[2]=.42; e.rotation_euler[0]=R(14); P.append(e)
    e=empty((1.5,3.2,.84)); oico((0,0,0),.22,M('#F2C14E',.5),e,sub=2); P.append(e)
    e=empty((-6.5,-2.2,.86)); obox((0,0,0),(.14,.3,.04),M('#2B6FB8',.6),.03,e); obox((0,-.05,.05),(.1,.03,.05),M('#2B6FB8',.6),.02,e); P.append(e)
    e=empty((9.5,1.6,.84)); ocyl((0,0,.1),.45,.3,M('#3A8A9A',.5),e,rot=(0,0,0),seg=16); P.append(e)
    return P
def bed_shop(x,y):
    """the loneliest shop in Karachi: a dusty bed on display, cobwebs, 90% OFF"""
    wd=M('#7A4E2A',.6,kind='wood',sc=.6)
    B.box((x,y,.45),(1.5,.95,.1),wd,.03); B.box((x,y,.72),(1.42,.88,.17),M('#DCE4F0',.8,kind='fabric'),.08); B.box((x-1.0,y,.98),(.34,.6,.1),M('#F4F8FF',.8,kind='fabric'),.07)
    B.box((x-1.5,y,.85),(.07,.95,.85),wd,.03); B.box((x+1.5,y,.55),(.07,.95,.55),wd,.03)
    for sx in (-1.4,1.4):
        for sy in (-.85,.85): B.cyl((x+sx,y+sy,.2),.07,.4,wd,seg=8)
    B.box((x+.5,y,.92),(.9,.86,.012),M('#B8A8E0',.8,kind='fabric'),.005)
    web=M('#F4F4F4',.6,emit=.5)
    for (P,a0,a1,rad) in (((x-1.5,y-.95,1.7),0,-80,1.0),((x+1.5,y-.95,1.1),180,265,.7)):
        pts=[]
        for k in range(6):
            a=R(L(a0,a1,k/5)); q=(P[0]+math.cos(a)*rad,P[1],P[2]+math.sin(a)*rad); pts.append(q); bseg(P,q,.006,web,4)
        for f in (.35,.65,.95):
            for k in range(5): bseg(tuple(Vector(P).lerp(Vector(pts[k]),f)),tuple(Vector(P).lerp(Vector(pts[k+1]),f)),.005,web,4)
    sign('BEDS',(x,y+1.1,2.78),.5,'#FFF6D8','#3A4A8A',n=(0,-1,0),e=2.0,pad=.28,th=.1,frame='#F4F1EA',always=True)
    sign('90% OFF',(x,y+1.1,1.9),.34,'#16171C','#F2C14E',n=(0,-1,0),e=1.4,pad=.18,th=.08,always=True)
    sign('NEVER USED',(x,y+1.1,1.27),.26,'#FFFFFF','#C8372D',n=(0,-1,0),e=1.4,pad=.13,th=.08,always=True)
    for sx in (-1.5,1.5): B.cyl((x+sx,y+1.16,1.6),.05,3.2,M('#5A5E66',.5),seg=6)
def chai_counter(x,y,rz=0,label='CHAI  20'):
    """open chai counter (no awning): faces rz, seller stands behind"""
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#8A5A36',.6,kind='wood',sc=.6); st=M('#C9CED8',.25,metal=.9)
    obox((0,0,.5),(.95,.36,.5),wd,.03,e); obox((0,0,1.02),(1.0,.4,.025),M('#F2EEE6',.4,kind='tile',sc=6,h2='#C8372D'),.01,e)
    obox((-.6,0,1.1),(.2,.2,.06),M('#2A2C34',.5),.02,e); ocyl((-.6,0,1.17),.13,.03,lit('#FF7A1A',6,always=True),e,rot=(0,0,0),seg=12)
    ocyl((-.6,0,1.32),.17,.26,st,e,rot=(0,0,0),seg=16,r2=.12); ocyl((-.6,0,1.47),.08,.05,M('#2A2C34',.4),e,rot=(0,0,0),seg=10)
    for i in range(6): ocyl((-.05+(i%3)*.2,-.12+(i//3)*.2,1.1),.055,.11,M('#F6F4EE',.4),e,rot=(0,0,0),seg=10,r2=.07)
    ocyl((.72,.05,1.2),.12,.3,M('#BFE6F2',.1,spec=1,alpha=.45),e,rot=(0,0,0),seg=12); ocyl((.72,.05,1.13),.1,.14,M('#C9A45A',.6),e,rot=(0,0,0),seg=10)
    sign(label,(0,-.38,.55),.24,'#FFF6D8','#7A1F2E',n=(0,-1,0),e=1.5,pad=.12,th=.03,parent=e,always=True)
    return e
