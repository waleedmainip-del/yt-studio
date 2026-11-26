# entry: blender -b -P film_lh.py -- <shot#> <pct> <samples> still|anim <t-list | f0 f1>
import os
LH=os.environ.get('LH','/home/claude/kvl')
exec(open(LH+'/base_lh.py').read())
for _f in ('chars_base','look_lh','anim_lh','fx_lh','chars_lh','chars_dk','chars_bd','chars_bg','cast_kz','cast_kvl','world_lh','world_kb','world_kz','world_kz2','world_kz3','gen_kb','world_kvl','kit_kvl','shots_kvl','shots_kvl2','shots_kvl3','thumb_kvl'): exec(open(LH+'/%s.py'%_f).read())
FPS=30; MODE=args[3] if len(args)>3 else 'anim'
if SHOT=='T': SN=99; KEY='THUMB'; T0=0.0; T1=2.0; DUR=2.0; G0=0; G1=60
else: SN=int(SHOT); KEY,T0=SEQ[SN-1]; T1=SEQ[SN][1] if SN<len(SEQ) else END; DUR=T1-T0; G0=int(round(T0*FPS)); G1=int(round(T1*FPS))
make_cam(); sc=bpy.context.scene
if SHOTS[KEY] is None: print('UI SHOT',KEY); sys.exit(0)
spec=SHOTS[KEY]()
OUTR=os.environ.get('OUTR',LH+'/render')
TRAIL=[]
if BALLS:
    for k in range(7): TRAIL.append(oico((0,0,-9),BALLS[0].children[0].dimensions.x/2*(1-.12*(k+1)) if BALLS[0].children else .09,M('#F6F9C0',.5,emit=2.2,alpha=.55-.06*k),None,sub=2))
def upd_all(t):
    TNOW[0]=t; hist=[]
    if TRAIL:
        for k in range(len(TRAIL),0,-1): spec['upd'](t-k*.02); hist.append(BALLS[0].matrix_world.translation.copy() if BALLS[0].parent else BALLS[0].location.copy())
    spec['upd'](t); fx.upd(t); bpy.context.view_layer.update(); spec['upd'](t); fx.upd(t)
    if TRAIL:
        bpy.context.view_layer.update(); cur=BALLS[0].matrix_world.translation.copy(); hist=hist[::-1]
        sp=(cur-hist[0]).length/.02 if hist else 0
        for k,o in enumerate(TRAIL):
            ok=sp>4.0 and cur.z>-1 and hist[k].z>-1 and (hist[k]-cur).length<3.0
            o.location=hist[k] if ok else (0,0,-9); o.scale=(1,1,1) if ok else (0,0,0)
def _vis_corners(cs):
    from bpy_extras.object_utils import world_to_camera_view
    pv=[world_to_camera_view(sc,sc.camera,c) for c in cs]
    ins=[(-.002<=q.x<=1.002 and -.002<=q.y<=1.002 and q.z>0) for q in pv]
    return any(ins),all(ins)
def _board_auto():
    if not BOARDOBJ or KEY in BOARDKEEP: return
    cs=[Vector((x,BACKY-.2,z)) for x in (-3.45,3.45) for z in (3.72,9.05)]
    for k in range(17):
        upd_all(min(DUR*k/16,DUR-1e-3)); bpy.context.view_layer.update(); a_,l_=_vis_corners(cs)
        if a_ and not l_:
            for o in BOARDOBJ: o.hide_render=True; o.hide_viewport=True
            print('BOARDAUTO',KEY,'hide',round(DUR*k/16,2),flush=True); return
    print('BOARDAUTO',KEY,'show',flush=True)
_board_auto()
def _txt_scan():
    bad={}
    for k in range(17):
        t=min(DUR*k/16,DUR-1e-3); upd_all(t); bpy.context.view_layer.update()
        for o in bpy.data.objects:
            if o.type!='FONT' or o.hide_render or o in BOARDOBJ: continue
            mw=o.matrix_world
            if abs(mw.to_3x3().determinant())<1e-9: continue
            p_=o; hid=False
            while p_ is not None:
                if p_.hide_render: hid=True
                p_=p_.parent
            if hid: continue
            cs=[mw@Vector(c) for c in o.bound_box]; a_,l_=_vis_corners(cs)
            if a_ and not l_: bad.setdefault(o.name,[]).append(round(t,2))
    return bad
def _txt_auto():
    for nm,ts in _txt_scan().items():
        if len(ts)<2: continue
        o=bpy.data.objects[nm]; o.hide_render=True; o.hide_viewport=True
        for kk in ('board','frame'):
            if kk in o.keys() and o[kk] in bpy.data.objects: bpy.data.objects[o[kk]].hide_render=True; bpy.data.objects[o[kk]].hide_viewport=True
        print('TXTHIDE',KEY,repr(o.data.body),ts[0],ts[-1],len(ts),flush=True)
_txt_auto()
if MODE=='txt':
    bad=_txt_scan()
    print('TXTCUT',SN,KEY,{bpy.data.objects[k].data.body:(v[0],v[-1],len(v)) for k,v in bad.items()},flush=True)
elif MODE=='probe':
    from bpy_extras.object_utils import world_to_camera_view
    t=float(args[4]); upd_all(t); dg=bpy.context.evaluated_depsgraph_get(); cam=sc.camera; o=cam.matrix_world.translation
    fr=[cam.matrix_world@v for v in cam.data.view_frame(scene=sc)]
    for j in range(5):
        row=[]
        for i in range(3):
            u=(i+.5)/3; v=(j+.5)/5; top=fr[1].lerp(fr[0],u); bot=fr[2].lerp(fr[3],u); p_=top.lerp(bot,v)
            hit,loc,n,idx,ob,m=sc.ray_cast(dg,o,(p_-o).normalized())
            rt=ob
            while rt is not None and rt.parent is not None: rt=rt.parent
            row.append('%s%s@%.1f'%(ob.name[:9] if ob else '-',tuple(round(x,1) for x in rt.matrix_world.translation) if rt else '',(loc-o).length if hit else 0))
        print('PROBE',' | '.join(row),flush=True)
    import os as _os
    for uv in [x for x in _os.environ.get('PUV','').split(';') if x]:
        u,v=[float(x) for x in uv.split(',')]; top=fr[3].lerp(fr[0],u); bot=fr[2].lerp(fr[1],u); p_=top.lerp(bot,v)
        hit,loc,n,idx,ob,m=sc.ray_cast(dg,o,(p_-o).normalized())
        print('PUV',uv,ob.name if ob else None,tuple(round(x,2) for x in loc) if hit else None,tuple(round(x,2) for x in ob.dimensions) if ob else None,flush=True)
    for nm in args[5:]:
        ob=bpy.data.objects.get(nm)
        if ob: print('POS',nm,tuple(round(x,2) for x in ob.matrix_world.translation),tuple(round(x,2) for x in world_to_camera_view(sc,cam,ob.matrix_world.translation)))
elif MODE=='clip':
    # physics check: no two characters may occupy the same space (2D oriented boxes of torso+arms)
    def box(H):
        m=H['root'].matrix_world; u=H['u']; c=m.translation; a=m.to_euler()[2]; return c,a,2.0*u*H['C'].get('wide',1.0),.52*u
    def sep(A,B_):
        (c1,a1,w1,d1),(c2,a2,w2,d2)=A,B_
        if abs(c1.z-c2.z)>1.0: return True
        dx=c2.x-c1.x; dy=c2.y-c1.y
        for a in (a1,a1+pi/2,a2,a2+pi/2):
            ax=(math.cos(a),math.sin(a)); pr=abs(dx*ax[0]+dy*ax[1]); r=0
            for (aa,w,d) in ((a1,w1,d1),(a2,w2,d2)): r+=abs(w*(math.cos(aa)*ax[0]+math.sin(aa)*ax[1]))+abs(d*(-math.sin(aa)*ax[0]+math.cos(aa)*ax[1]))
            if pr>r-.03: return True
        return False
    bad=set()
    for f in range(6):
        t=DUR*(f+.5)/6; upd_all(t); bpy.context.view_layer.update(); Bx=[('%s(%.1f,%.1f|w%.2f)'%(H['root'].name,H['root'].matrix_world.translation.x,H['root'].matrix_world.translation.y,2.0*H['u']*H['C'].get('wide',1.0)),box(H)) for H in ALLH]
        for i in range(len(Bx)):
            for j in range(i+1,len(Bx)):
                if not sep(Bx[i][1],Bx[j][1]): bad.add((Bx[i][0],Bx[j][0]))
    print('CLIP',SN,KEY,sorted(bad),flush=True)
elif MODE=='still':
    os.makedirs(OUTR+'/stills',exist_ok=True)
    for t in [(DUR*float(x[1:]) if x.startswith('f') else float(x)) for x in args[4].split(',')]:
        if t<0: t=DUR+t
        upd_all(t); sc.render.filepath=OUTR+'/stills/S%02d_%s_%05.2f.png'%(SN,KEY,t); bpy.ops.render.render(write_still=True); print('STILL',SN,KEY,t,flush=True)
else:
    out=OUTR+'/frames/S%02d'%SN; os.makedirs(out,exist_ok=True); t0w=time.time()
    def _h(scene,*a_):
        upd_all(scene.frame_current/FPS-T0); print('FRAME',scene.frame_current,round(time.time()-t0w,1),flush=True)
    bpy.app.handlers.frame_change_pre.append(_h)
    sc.frame_start=G0; sc.frame_end=G1-1
    if len(args)>5: sc.frame_start=int(args[4]); sc.frame_end=int(args[5])-1
    sc.render.use_overwrite=False; sc.render.image_settings.file_format='PNG'; sc.render.image_settings.compression=15
    sc.render.fps=FPS; sc.render.filepath=out+'/f#####'
    bpy.ops.render.render(animation=True); print('SHOT_DONE',SN,flush=True)
