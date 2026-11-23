exec(open('/home/claude/rich/base_lr.py').read())
for _f in ('chars_lr','cast_lr','look_lr','anim_lr','fx_lr','world_base_lr','world_lr','shots_lr'): exec(open('/home/claude/rich/%s.py'%_f).read())
FPS=int(os.environ.get('FPS','30')); MODE=args[3] if len(args)>3 else 'anim'
SN=int(SHOT); KEY,T0=SEQ[SN-1]; T1=SEQ[SN][1] if SN<len(SEQ) else END; DUR=T1-T0; G0=int(round(T0*FPS)); G1=int(round(T1*FPS))
make_cam(); spec=SHOTS[KEY](); sc=bpy.context.scene
def upd_all(t):
    TNOW[0]=t; spec['upd'](t); fx.upd(t)
if MODE=='collide': pass
elif MODE=='still':
    for t in [float(x) for x in args[4].split(',')]:
        if t<0: t=DUR+t
        upd_all(t); sc.render.filepath='/home/claude/rich/stills/S%02d_%05.2f.png'%(SN,t); bpy.ops.render.render(write_still=True); print('STILL',SN,KEY,t,flush=True)
else:
    out='/home/claude/rich/frames/S%02d'%SN; os.makedirs(out,exist_ok=True); t0w=time.time()
    def _h(scene,*a_):
        upd_all(scene.frame_current/FPS-T0); print('FRAME',scene.frame_current,round(time.time()-t0w,1),flush=True)
    bpy.app.handlers.frame_change_pre.append(_h)
    sc.frame_start=G0; sc.frame_end=G1-1
    if len(args)>5: sc.frame_start=int(args[4]); sc.frame_end=int(args[5])-1
    sc.render.use_overwrite=False; sc.render.image_settings.file_format='PNG'; sc.render.image_settings.compression=15
    sc.render.fps=FPS; sc.render.filepath=out+'/f#####'
    bpy.ops.render.render(animation=True); print('SHOT_DONE',SN,flush=True)
if MODE=='collide':
    import json as _j
    from mathutils.bvhtree import BVHTree
    dg=bpy.context.evaluated_depsgraph_get()
    def desc(o):
        out=[]; st=[o]
        while st:
            x=st.pop(); out+= [c for c in x.children]; st+=list(x.children)
        return [c for c in out if c.type=='MESH']
    roots=[H['root'] for H in PEOPLE]; charobs=set()
    for r_ in roots:
        for c in desc(r_): charobs.add(c.name)
    def build(objs):
        V=[];P=[];own=[]
        for o in objs:
            ev=o.evaluated_get(dg); me=ev.to_mesh(); mw=o.matrix_world; b=len(V)
            V+= [mw@v.co for v in me.vertices]
            for p in me.polygons: P.append([b+i for i in p.vertices]); own.append(o.name)
            ev.to_mesh_clear()
        return (BVHTree.FromPolygons(V,P,epsilon=0.0) if P else None),own
    statics=[o for o in bpy.data.objects if o.type=='MESH' and o.name not in charobs and o.visible_get()]
    statics=[o for o in statics if not (o.dimensions.z<.04 and o.dimensions.x*o.dimensions.y>3)]
    rep=[]
    for t in [float(x) for x in args[4].split(',')]:
        if t<0: t=DUR+t
        upd_all(t); bpy.context.view_layer.update(); dg.update()
        sb,sown=build(statics)
        chs=[]
        for H in PEOPLE:
            if H['root'].scale.x==0: continue
            bv,_=build(desc(H['root'])); chs.append((H['nm'],bv))
        for i,(n1,b1) in enumerate(chs):
            if b1 is None: continue
            if sb:
                hits=b1.overlap(sb); objs=sorted(set(sown[j] for _,j in hits))
                if objs: rep.append(dict(t=t,a=n1,b='STATIC',n=len(hits),objs=objs[:6]))
            for n2,b2 in chs[i+1:]:
                if b2 is None: continue
                h=b1.overlap(b2)
                if h: rep.append(dict(t=t,a=n1,b=n2,n=len(h)))
    _j.dump(rep,open('/home/claude/rich/stills/collide_S%02d.json'%SN,'w'),indent=0); print('COLLIDE',SN,len(rep),flush=True)
