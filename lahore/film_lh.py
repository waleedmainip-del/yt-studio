exec(open('/home/claude/lahore/base_lh.py').read())
for _f in ('chars_lh','cast_lh','look_lh','anim_lh','fx_lh','world_lh','shots_lh'): exec(open('/home/claude/lahore/%s.py'%_f).read())
FPS=int(os.environ.get('FPS','24')); MODE=args[3] if len(args)>3 else 'anim'
SN=int(SHOT); KEY,T0=SEQ[SN-1]; T1=SEQ[SN][1] if SN<len(SEQ) else END; DUR=T1-T0; G0=int(round(T0*FPS)); G1=int(round(T1*FPS))
make_cam(); spec=SHOTS[KEY](); sc=bpy.context.scene
def upd_all(t):
    TNOW[0]=t; spec['upd'](t); fx.upd(t)
if MODE=='still':
    for t in [float(x) for x in args[4].split(',')]:
        if t<0: t=DUR+t
        upd_all(t); sc.render.filepath='/home/claude/lahore/stills/S%02d_%05.2f.png'%(SN,t); bpy.ops.render.render(write_still=True); print('STILL',SN,KEY,t,flush=True)
else:
    out='/home/claude/lahore/frames/S%02d'%SN; os.makedirs(out,exist_ok=True); t0w=time.time()
    def _h(scene,*a_):
        upd_all(scene.frame_current/FPS-T0); print('FRAME',scene.frame_current,round(time.time()-t0w,1),flush=True)
    bpy.app.handlers.frame_change_pre.append(_h)
    sc.frame_start=G0; sc.frame_end=G1-1
    if len(args)>5: sc.frame_start=int(args[4]); sc.frame_end=int(args[5])-1
    sc.render.use_overwrite=False; sc.render.image_settings.file_format='PNG'; sc.render.image_settings.compression=15
    sc.render.fps=FPS; sc.render.filepath=out+'/f#####'
    bpy.ops.render.render(animation=True); print('SHOT_DONE',SN,flush=True)
