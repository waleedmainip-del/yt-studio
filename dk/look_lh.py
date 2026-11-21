# lighting moods + render setup. call setup_render(mood) after scene built
def world_sky(top,bottom,strength=.8,cloud='#FFFFFF',cov=.5,cstr=.85):
    sc=bpy.context.scene; w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; nt=w.node_tree
    bg=nt.nodes['Background']; tc=nt.nodes.new('ShaderNodeTexCoord'); sep=nt.nodes.new('ShaderNodeSeparateXYZ'); rp=nt.nodes.new('ShaderNodeValToRGB')
    nt.links.new(tc.outputs['Generated'],sep.inputs[0]); nt.links.new(sep.outputs['Z'],rp.inputs[0])
    rp.color_ramp.elements[0].position=.48; rp.color_ramp.elements[0].color=hexc(bottom); rp.color_ramp.elements[1].position=.85; rp.color_ramp.elements[1].color=hexc(top)
    # cloud layer: project view direction onto a plane, noise -> ramp, masked above horizon
    zc=nt.nodes.new('ShaderNodeMath'); zc.operation='ADD'; zc.inputs[1].default_value=.18; nt.links.new(sep.outputs['Z'],zc.inputs[0])
    cx=nt.nodes.new('ShaderNodeMath'); cx.operation='DIVIDE'; nt.links.new(sep.outputs['X'],cx.inputs[0]); nt.links.new(zc.outputs[0],cx.inputs[1])
    cy=nt.nodes.new('ShaderNodeMath'); cy.operation='DIVIDE'; nt.links.new(sep.outputs['Y'],cy.inputs[0]); nt.links.new(zc.outputs[0],cy.inputs[1])
    cmb=nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(cx.outputs[0],cmb.inputs[0]); nt.links.new(cy.outputs[0],cmb.inputs[1])
    nz=nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value=1.7; nz.inputs['Detail'].default_value=float(os.environ.get('SKYDET','6')); nz.inputs['Roughness'].default_value=.55; nt.links.new(cmb.outputs[0],nz.inputs['Vector'])
    cr=nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position=cov; cr.color_ramp.elements[1].position=cov+.2; nt.links.new(nz.outputs['Fac'],cr.inputs[0])
    hm=nt.nodes.new('ShaderNodeMapRange'); hm.inputs['From Min'].default_value=.02; hm.inputs['From Max'].default_value=.22; nt.links.new(sep.outputs['Z'],hm.inputs['Value'])
    fm=nt.nodes.new('ShaderNodeMath'); fm.operation='MULTIPLY'; nt.links.new(cr.outputs['Color'],fm.inputs[0]); nt.links.new(hm.outputs['Result'],fm.inputs[1])
    fm2=nt.nodes.new('ShaderNodeMath'); fm2.operation='MULTIPLY'; fm2.inputs[1].default_value=cstr; nt.links.new(fm.outputs[0],fm2.inputs[0])
    mx=nt.nodes.new('ShaderNodeMix'); mx.data_type='RGBA'; nt.links.new(fm2.outputs[0],mx.inputs['Factor']); nt.links.new(rp.outputs['Color'],mx.inputs[6]); mx.inputs[7].default_value=hexc(cloud)
    nt.links.new(mx.outputs[2],bg.inputs[0]); bg.inputs[1].default_value=strength
    w['cloudmix']=mx.name
    return w,rp,bg
MOODS={
 'storm':  dict(sun=(72,150),e=1.25,col=(1,.8,.66),top='#4A5470',bot='#C9A6A0',sky=.8,mist='#9C98A8',cloud='#5E6378',cov=.36,cstr=.95),
 'dawn':   dict(sun=(70,135),e=1.6,col=(1,.78,.62),top='#6E86A8',bot='#F2C7A8',sky=.75,mist='#C9C2CC'),
 'day':    dict(sun=(50,140),e=3.0,col=(1,.95,.86),top='#3A86E0',bot='#BFE0FF',sky=.85,mist='#CFE3F5'),
 'morning':dict(sun=(62,120),e=2.7,col=(1,.9,.76),top='#4C92E0',bot='#FFE3C2',sky=.8,mist='#E8E0D6'),
 'morning_s':dict(sun=(58,40),e=2.9,col=(1,.92,.8),top='#4A90E2',bot='#FFE6CC',sky=.85,mist='#E6E2DA',cloud='#FFFFFF',cov=.56),
 'afternoon':dict(sun=(58,-60),e=2.8,col=(1,.88,.7),top='#3F86D8',bot='#FFE0B8',sky=.8,mist='#E8D8C4'),
 'golden': dict(sun=(74,-62),e=2.6,col=(1,.72,.45),top='#5C7FC8',bot='#FFB878',sky=.75,mist='#F2C7A0',cloud='#F2A6A0',cov=.47,cstr=.8),
 'mars':   dict(sun=(55,-50),e=2.6,col=(1,.78,.6),top='#C8624A',bot='#F6C6A0',sky=.9,mist='#E8A888',cloud='#F2B8A0',cov=.52,cstr=.6),
 'invade': dict(sun=(60,140),e=1.5,col=(.85,.85,1.0),top='#3A3A6E',bot='#B8A8D8',sky=.7,mist='#A8A0C8',cloud='#6A6A9A',cov=.4,cstr=.9),
 'city':   dict(sun=(52,-135),e=3.0,col=(1,.93,.82),top='#3E80D8',bot='#F6E2C6',sky=.85,mist='#DCD8D2',cloud='#FFFFFF',cov=.55,cstr=.85),
 'doom':   dict(sun=(62,-135),e=1.9,col=(1,.5,.46),top='#16060E',bot='#7A2630',sky=1.25,mist='#4A1A24',cloud='#2A0E16',cov=.35,cstr=.9),
 'ash':    dict(sun=(66,-135),e=1.1,col=(1,.82,.66),top='#4E4850',bot='#B4A496',sky=.7,mist='#9A8E86',cloud='#6E6466',cov=.3,cstr=.9),
 'field':  dict(sun=(50,-40),e=3.0,col=(1,.93,.8),top='#3E86DC',bot='#D8ECFF',sky=.85,mist='#D8E4EE',cloud='#FFFFFF',cov=.5),
 'lava':   dict(sun=(76,-60),e=1.6,col=(1,.6,.4),top='#3A2A3A',bot='#E86A3A',sky=.7,mist='#8A4A3A',cloud='#5A3A3A',cov=.4,cstr=.9),
 'sunset': dict(sun=(80,-58),e=2.3,col=(1,.62,.38),top='#5A6CB8',bot='#FF9C68',sky=.8,mist='#F0A884',cloud='#E89A9C',cov=.46,cstr=.8),
}
def setup_render(mood='day',interior=False,shadow_dist=60,res=100,samples=None,mist=True,cascades=3):
    sc=bpy.context.scene; m=MOODS[mood]
    bpy.ops.object.light_add(type='SUN'); S=bpy.context.object; S.rotation_euler=(R(m['sun'][0]),0,R(m['sun'][1])); S.data.energy=m['e']; S.data.color=m['col']; S.data.angle=R(2.0)
    S.data.shadow_cascade_max_distance=shadow_dist; S.data.shadow_cascade_count=cascades; S.data.shadow_cascade_fade=.15
    w,rp,bg=world_sky(m['top'],m['bot'],m['sky'],m.get('cloud','#FFFFFF'),m.get('cov',.55),m.get('cstr',.85))
    sc.render.resolution_x=1080; sc.render.resolution_y=1920; sc.render.resolution_percentage=res; sc.render.engine='BLENDER_EEVEE'; e=sc.eevee
    e.taa_render_samples=samples or SAMPLES; e.use_gtao=os.environ.get('GTAO','1')=='1'; e.gtao_distance=1.0; e.gtao_factor=1.2; e.use_soft_shadows=os.environ.get('SOFT','1')=='1'; e.use_bloom=True; e.bloom_intensity=.035; e.bloom_threshold=1.1
    e.use_gtao_bent_normals=os.environ.get('GBN','1')=='1'; e.use_gtao_bounce=os.environ.get('GBN','1')=='1'; e.use_ssr=bool(SSR[0]); e.ssr_quality=.25; e.ssr_max_roughness=.3; e.ssr_thickness=.4; e.shadow_cascade_size='2048'; e.shadow_cube_size='1024'; e.use_shadow_high_bitdepth=True; e.light_threshold=.05
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='Medium High Contrast'
    if mist and not interior:
        bpy.context.view_layer.use_pass_mist=True; w.mist_settings.start=35; w.mist_settings.depth=110; w.mist_settings.falloff='QUADRATIC'
        sc.use_nodes=True; ct=sc.node_tree; rl=ct.nodes['Render Layers']; cp=ct.nodes['Composite']
        mx=ct.nodes.new('CompositorNodeMixRGB'); mul=ct.nodes.new('CompositorNodeMath'); mul.operation='MULTIPLY'; mul.inputs[1].default_value=.3
        ct.links.new(rl.outputs['Mist'],mul.inputs[0]); ct.links.new(mul.outputs[0],mx.inputs[0]); ct.links.new(rl.outputs['Image'],mx.inputs[1]); mx.inputs[2].default_value=hexc(m['mist']); ct.links.new(mx.outputs[0],cp.inputs['Image'])
    return S,w,rp,bg
SSR=[0]
CAM=None
def make_cam():
    global CAM,TGT
    sc=bpy.context.scene; CAM=bpy.data.objects.new('cam',bpy.data.cameras.new('cam')); _col.objects.link(CAM); CAM.data.clip_end=400; CAM.data.clip_start=.05
    TGT=empty((0,0,0)); c=CAM.constraints.new('TRACK_TO'); c.target=TGT; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'; sc.camera=CAM; CAM.data.dof.use_dof=os.environ.get('DOF','1')=='1'
    return CAM
SHAKE=[0.0]; TNOW=[0.0]
def camset(loc,tg,lens,fs=5.6,focus=None,roll=0):
    r=random.Random(int(TNOW[0]*60)); s=SHAKE[0]
    CAM.location=(loc[0]+r.uniform(-s,s),loc[1]+r.uniform(-s,s),loc[2]+r.uniform(-s,s)); TGT.location=tg; CAM.data.lens=lens; CAM.data.dof.aperture_fstop=fs
    CAM.data.dof.focus_distance=max(.3,(Vector(loc)-Vector(focus or tg)).length)
    CAM.data.dof.use_dof=(fs<7.5) and os.environ.get('DOF','1')=='1'
    bpy.context.scene.eevee.bokeh_max_size=float(os.environ.get('BOKEH','100'))
INT={
 'night':  dict(sun=(62,180),e=.9,col=(.55,.68,1.0),top='#16203A',bot='#24345A',sky=.35,fill=(.5,.6,1.0),fe=28,cloud='#2A3550',cov=.5),
 'evening':dict(sun=(78,200),e=1.2,col=(1,.7,.5),top='#4C5C9A',bot='#F2A070',sky=.55,fill=(1,.88,.72),fe=110,cloud='#E8A0A0',cov=.5),
 'morning':dict(sun=(52,200),e=3.4,col=(1,.9,.74),top='#5A9BE6',bot='#FFE9CC',sky=.9,fill=(1,.95,.88),fe=160,cloud='#FFFFFF',cov=.55),
 'day':    dict(sun=(48,195),e=3.0,col=(1,.96,.9),top='#4C92E0',bot='#D8EBFF',sky=.9,fill=(1,.97,.94),fe=150,cloud='#FFFFFF',cov=.55),
}
def setup_interior(kind,room=(0,0,3.3),res=100,samples=None,shadow_dist=18):
    sc=bpy.context.scene; m=INT[kind]
    bpy.ops.object.light_add(type='SUN'); S=bpy.context.object; S.rotation_euler=(R(m['sun'][0]),0,R(m['sun'][1])); S.data.energy=m['e']; S.data.color=m['col']; S.data.angle=R(1.5)
    S.data.shadow_cascade_max_distance=shadow_dist; S.data.shadow_cascade_count=2; S.data.shadow_cascade_fade=.1
    w,rp,bg=world_sky(m['top'],m['bot'],m['sky'],m['cloud'],m['cov'],.6)
    bpy.ops.object.light_add(type='AREA',location=(room[0],room[1],room[2]-.15)); A=bpy.context.object; A.data.energy=m['fe']; A.data.size=4.0; A.data.color=m['fill']; A.data.use_shadow=False if hasattr(A.data,'use_shadow') else None
    sc.render.resolution_x=1080; sc.render.resolution_y=1920; sc.render.resolution_percentage=res; sc.render.engine='BLENDER_EEVEE'; e=sc.eevee
    e.taa_render_samples=samples or SAMPLES; e.use_gtao=True; e.gtao_distance=.8; e.gtao_factor=1.3; e.use_soft_shadows=os.environ.get('SOFT','1')=='1'; e.use_bloom=True; e.bloom_intensity=.04; e.bloom_threshold=1.0
    e.use_ssr=False; e.shadow_cascade_size='2048'; e.shadow_cube_size=os.environ.get('CUBE','1024'); e.use_shadow_high_bitdepth=True; e.light_threshold=.03
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='Medium High Contrast'
    return S,A,w,bg
def point(loc,e,col=(1,.85,.6),r=.1,shadow=None):
    bpy.ops.object.light_add(type='POINT',location=loc); p=bpy.context.object; p.data.energy=e; p.data.color=col; p.data.shadow_soft_size=r
    if shadow is None: shadow=os.environ.get('PSHADOW','1')=='1'
    p.data.use_shadow=shadow; return p
