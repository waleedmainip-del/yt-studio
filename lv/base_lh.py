import bpy, bmesh, sys, math, random, zlib, json, os, time
from mathutils import Matrix, Vector, Euler
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['0']
SHOT=args[0]; PCT=int(args[1]) if len(args)>1 else 100; SAMPLES=int(args[2]) if len(args)>2 else 16
random.seed(21); R=math.radians; pi=math.pi
bpy.ops.wm.read_factory_settings(use_empty=True)
_col=bpy.context.scene.collection
def dseed(s): return (zlib.crc32(s.encode())%9973)/997.3
def lin(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def hexc(h):
    h=h.lstrip('#'); return tuple(lin(int(h[i:i+2],16)/255) for i in (0,2,4))+(1,)
def shade(h,f):
    h=h.lstrip('#'); v=[min(255,max(0,int(int(h[i:i+2],16)*f))) for i in (0,2,4)]; return '#%02X%02X%02X'%tuple(v)
_m={}
def M(h,rough=.6,metal=0,emit=0,kind=None,spec=.5,h2=None,sc=1.0,alpha=1.0):
    k=(h,rough,metal,emit,kind,spec,h2,sc,alpha)
    if k in _m: return _m[k]
    m=bpy.data.materials.new(h+(kind or '')); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=hexc(h); b.inputs['Roughness'].default_value=rough; b.inputs['Metallic'].default_value=metal
    b.inputs['Specular IOR Level'].default_value=spec
    if emit: b.inputs['Emission Color'].default_value=hexc(h); b.inputs['Emission Strength'].default_value=emit
    if alpha<1: b.inputs['Alpha'].default_value=alpha; m.blend_method='BLEND'; m.shadow_method='NONE'; m.show_transparent_back=False
    if kind:
        tc=nt.nodes.new('ShaderNodeTexCoord'); OB=tc.outputs['Object']
        def noise(scale,detail=4,vec=None):
            n=nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value=scale; n.inputs['Detail'].default_value=min(detail,float(os.environ.get('NDET','16')))
            nt.links.new(vec or OB,n.inputs['Vector']); return n
        def bump(src,strength,dist=.02,normal=None):
            bp=nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value=strength; bp.inputs['Distance'].default_value=dist
            nt.links.new(src,bp.inputs['Height'])
            if normal is not None: nt.links.new(normal,bp.inputs['Normal'])
            nt.links.new(bp.outputs['Normal'],b.inputs['Normal']); return bp
        def ramp(src,c1,c2,p0=.35,p1=.65):
            r=nt.nodes.new('ShaderNodeValToRGB'); r.color_ramp.elements[0].position=p0; r.color_ramp.elements[1].position=p1
            r.color_ramp.elements[0].color=hexc(c1); r.color_ramp.elements[1].color=hexc(c2)
            nt.links.new(src,r.inputs['Fac']); nt.links.new(r.outputs['Color'],b.inputs['Base Color']); return r
        def wave(scale,direction='Z',profile='SAW',dist=0.0):
            w=nt.nodes.new('ShaderNodeTexWave'); w.wave_type='BANDS'; w.bands_direction=direction; w.wave_profile=profile
            w.inputs['Scale'].default_value=scale; w.inputs['Distortion'].default_value=dist; w.inputs['Detail'].default_value=0
            nt.links.new(OB,w.inputs['Vector']); return w
        if kind=='fabric': bump(noise(90*sc,2).outputs['Fac'],.25,.01); ramp(noise(2.5,2).outputs['Fac'],shade(h,.93),shade(h,1.05))
        if kind=='asphalt': ramp(noise(1.2,6).outputs['Fac'],shade(h,.88),shade(h,1.1)); bump(noise(60,3).outputs['Fac'],.35,.01)
        if kind=='wall': ramp(noise(.6,3).outputs['Fac'],shade(h,.93),shade(h,1.04)); bump(noise(30,2).outputs['Fac'],.08,.01)
        if kind=='siding':
            w=wave(2*pi/(20*.21)); ramp(noise(.8,3).outputs['Fac'],shade(h,.95),shade(h,1.03)); bump(w.outputs['Fac'],.55,.02)
        if kind=='shingle':
            w=wave(2*pi/(20*.24)); n=noise(3.0,3); mx=nt.nodes.new('ShaderNodeMix'); mx.data_type='FLOAT'; mx.inputs['Factor'].default_value=.25
            nt.links.new(w.outputs['Fac'],mx.inputs['A']); nt.links.new(n.outputs['Fac'],mx.inputs['B'])
            ramp(noise(1.6,4).outputs['Fac'],shade(h,.82),shade(h,1.12)); bump(mx.outputs['Result'],.7,.03)
        if kind=='wood':
            w=nt.nodes.new('ShaderNodeTexWave'); w.wave_type='BANDS'; w.bands_direction='X'; w.inputs['Scale'].default_value=3*sc; w.inputs['Distortion'].default_value=6; w.inputs['Detail'].default_value=3
            nt.links.new(OB,w.inputs['Vector']); ramp(w.outputs['Fac'],shade(h,.82),shade(h,1.1),.2,.8); bump(noise(40,3).outputs['Fac'],.12,.01)
        if kind=='grass':
            ramp(noise(.35,5).outputs['Fac'],h2 or shade(h,.85),shade(h,1.12),.3,.7); bump(noise(120,2).outputs['Fac'],.35,.01)
        if kind=='concrete':
            t=nt.nodes.new('ShaderNodeTexBrick'); t.inputs['Color1'].default_value=hexc(h); t.inputs['Color2'].default_value=hexc(shade(h,.95)); t.inputs['Mortar'].default_value=hexc(shade(h,.62))
            t.inputs['Scale'].default_value=1.0/sc; t.inputs['Mortar Size'].default_value=.008; t.inputs['Brick Width'].default_value=1.0; t.inputs['Row Height'].default_value=1.0; t.inputs['Bias'].default_value=0; t.offset=0
            nt.links.new(OB,t.inputs['Vector']); nt.links.new(t.outputs['Color'],b.inputs['Base Color']); bump(t.outputs['Fac'],-.3,.01)
        if kind=='scales':
            v=nt.nodes.new('ShaderNodeTexVoronoi'); v.feature='DISTANCE_TO_EDGE'; v.inputs['Scale'].default_value=14*sc; nt.links.new(OB,v.inputs['Vector'])
            ramp(noise(3*sc,3).outputs['Fac'],shade(h,.9),shade(h,1.08)); bump(v.outputs['Distance'],.35,.02)
        if kind=='tile':
            t=nt.nodes.new('ShaderNodeTexChecker'); t.inputs['Color1'].default_value=hexc(h); t.inputs['Color2'].default_value=hexc(h2 or shade(h,.85)); t.inputs['Scale'].default_value=sc
            nt.links.new(OB,t.inputs['Vector']); nt.links.new(t.outputs['Color'],b.inputs['Base Color']); bump(noise(60,2).outputs['Fac'],.08,.005)
        if kind=='leaves':
            ramp(noise(1.2,3).outputs['Fac'],shade(h,.82),shade(h,1.15),.3,.7); bump(noise(25,3).outputs['Fac'],.4,.02)
    _m[k]=m; return m
def glow(col,e=3.0): return M(col,.3,emit=e)
def rgb(h): return hexc(h)
# ---------- batched static geometry
class Batch:
    def __init__(s): s.b={}; s.objs=[]
    def bm(s,mat,bevel,smooth):
        k=(mat,bevel,smooth)
        if k not in s.b: s.b[k]=bmesh.new()
        return s.b[k]
    def box(s,loc,size,mat,bevel=.03,rot=(0,0,0)):
        Mx=Matrix.Translation(loc)@Euler(rot).to_matrix().to_4x4()@Matrix.Diagonal((size[0]*2,size[1]*2,size[2]*2,1))
        bmesh.ops.create_cube(s.bm(mat,bevel,False),size=1,matrix=Mx)
    def cyl(s,loc,r,d,mat,rot=(0,0,0),seg=16,r2=None,bevel=0):
        Mx=Matrix.Translation(loc)@Euler(rot).to_matrix().to_4x4()
        bmesh.ops.create_cone(s.bm(mat,bevel,True),cap_ends=True,segments=seg,radius1=r,radius2=r if r2 is None else r2,depth=d,matrix=Mx)
    def ico(s,loc,r,mat,sc=(1,1,1),sub=2,rot=(0,0,0)):
        Mx=Matrix.Translation(loc)@Euler(rot).to_matrix().to_4x4()@Matrix.Diagonal((sc[0],sc[1],sc[2],1))
        bmesh.ops.create_icosphere(s.bm(mat,0,False),subdivisions=sub,radius=r,matrix=Mx)
    def poly(s,pts,mat,thick=0.0):
        bm=s.bm(mat,0,False); vs=[bm.verts.new(p) for p in pts]; bm.faces.new(vs)
    def done(s,name='batch'):
        items=list(s.b.items()); s.b={}; out=[]
        for (mat,bevel,smooth),bm in items:
            me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
            o=bpy.data.objects.new(name,me); _col.objects.link(o); me.materials.append(mat)
            if smooth:
                for p in me.polygons: p.use_smooth=True
                me.use_auto_smooth=True; me.auto_smooth_angle=R(40)
            if bevel:
                md=o.modifiers.new('bv','BEVEL'); md.width=bevel; md.segments=int(os.environ.get('BSEG','2')); md.limit_method='ANGLE'
            out.append(o); s.objs.append(o)
        return out
B=Batch()
# ---------- object helpers (fast, no bpy.ops)
def obox(loc,size,mat,bevel=.03,parent=None,rot=(0,0,0),seg=2):
    bm=bmesh.new(); bmesh.ops.create_cube(bm,size=1,matrix=Matrix.Diagonal((size[0]*2,size[1]*2,size[2]*2,1))); me=bpy.data.meshes.new('p'); bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new('p',me); o.location=loc; o.rotation_euler=rot; _col.objects.link(o)
    if bevel:
        md=o.modifiers.new('bv','BEVEL'); md.width=bevel; md.segments=seg
    me.materials.append(mat)
    if parent: o.parent=parent
    return o
def ocyl(loc,r,d,mat,parent=None,sc=(1,1,1),rot=(R(90),0,0),seg=20,r2=None):
    bm=bmesh.new(); bmesh.ops.create_cone(bm,cap_ends=True,segments=seg,radius1=r,radius2=r if r2 is None else r2,depth=d); me=bpy.data.meshes.new('c'); bm.to_mesh(me); bm.free()
    o=bpy.data.objects.new('c',me); o.location=loc; o.rotation_euler=rot; o.scale=sc; _col.objects.link(o); me.materials.append(mat)
    if parent: o.parent=parent
    return o
def oico(loc,r,mat,parent=None,sc=(1,1,1),sub=3,smooth=True,rot=(0,0,0)):
    bm=bmesh.new(); bmesh.ops.create_icosphere(bm,subdivisions=sub,radius=r); me=bpy.data.meshes.new('i'); bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth=True
    o=bpy.data.objects.new('i',me); o.location=loc; o.scale=sc; o.rotation_euler=rot; _col.objects.link(o); me.materials.append(mat)
    if parent: o.parent=parent
    return o
def omesh(verts,faces,mat,parent=None,loc=(0,0,0),thick=0.0):
    me=bpy.data.meshes.new('m'); me.from_pydata(verts,[],faces); me.update(); o=bpy.data.objects.new('m',me); o.location=loc; _col.objects.link(o); me.materials.append(mat)
    if thick:
        md=o.modifiers.new('sol','SOLIDIFY'); md.thickness=thick; md.offset=0
    if parent: o.parent=parent
    return o
def empty(loc,parent=None,rot=(0,0,0)):
    e=bpy.data.objects.new('e',None); e.location=loc; e.rotation_euler=rot; _col.objects.link(e)
    if parent: e.parent=parent
    return e
def text(body,loc,n,size,mat,ex=.03,parent=None):
    cu=bpy.data.curves.new('t','FONT'); cu.body=body; cu.align_x='CENTER'; cu.align_y='CENTER'; cu.size=size; cu.extrude=ex
    o=bpy.data.objects.new('t',cu); o.location=loc; o.rotation_euler=(R(90),0,math.atan2(n[0],-n[1])); _col.objects.link(o); cu.materials.append(mat)
    if parent: o.parent=parent
    return o
def ease(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def ease_out(x): x=max(0,min(1,x)); return 1-(1-x)**3
def ease_in(x): x=max(0,min(1,x)); return x**3
def pop(t): return 0 if t<=0 else max(0,1-math.exp(-8*t)*math.cos(12*t))
def L(a,b,f): return a+(b-a)*f
def LV(a,b,f): return tuple(L(x,y,f) for x,y in zip(a,b))
def fall(t,z0,zf,g=14,e=.4):
    if t<=0: return z0
    t1=math.sqrt(max(1e-6,2*(z0-zf)/g))
    if t<t1: return z0-.5*g*t*t
    v=g*t1*e; t-=t1
    while v>.3:
        T=2*v/g
        if t<T: return zf+v*t-.5*g*t*t
        t-=T; v*=e
    return zf
def lerp_angle(a,b,f): return a+((b-a+180)%360-180)*f
def face_dir(dx,dy): return math.degrees(math.atan2(dx,-dy))
