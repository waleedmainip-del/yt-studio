# entry: blender -b -P film_lh.py -- <shot#> <pct> <samples> still|anim <t-list | f0 f1>
import os
LH=os.environ.get('LH','/home/claude/pb')
exec(open(LH+'/base_lh.py').read())
for _f in ('chars_base','look_lh','anim_lh','fx_lh','chars_lh','chars_dk','chars_bd','cast_pb','world_lh','world_pb','shots_pb'): exec(open(LH+'/%s.py'%_f).read())
FPS=30; MODE=args[3] if len(args)>3 else 'anim'
SN=int(SHOT); KEY,T0=SEQ[SN-1]; T1=SEQ[SN][1] if SN<len(SEQ) else END; DUR=T1-T0; G0=int(round(T0*FPS)); G1=int(round(T1*FPS))
make_cam(); spec=SHOTS[KEY](); sc=bpy.context.scene
OUTR=os.environ.get('OUTR',LH+'/render')
def upd_all(t):
    TNOW[0]=t; spec['upd'](t); fx.upd(t); bpy.context.view_layer.update(); spec['upd'](t); fx.upd(t)
if MODE=='probe':
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
    for nm in args[5:]:
        ob=bpy.data.objects.get(nm)
        if ob: print('POS',nm,tuple(round(x,2) for x in ob.matrix_world.translation),tuple(round(x,2) for x in world_to_camera_view(sc,cam,ob.matrix_world.translation)))
elif MODE=='still':
    os.makedirs(OUTR+'/stills',exist_ok=True)
    for t in [float(x) for x in args[4].split(',')]:
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
