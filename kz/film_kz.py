# entry: blender -b -P film_lh.py -- <shot#> <pct> <samples> still|anim <t-list | f0 f1>
import os
LH=os.environ.get('LH','/home/claude/kz')
exec(open(LH+'/base_lh.py').read())
for _f in ('chars_base','look_lh','anim_lh','fx_lh','chars_lh','chars_dk','chars_bd','chars_bg','cast_kz','world_lh','world_kb','world_kz','world_kz2','world_kz3','gen_kb','shots_kz','shots_kz2','shots_kz3'): exec(open(LH+'/%s.py'%_f).read())
FPS=30; MODE=args[3] if len(args)>3 else 'anim'
SN=int(SHOT); KEY,T0=SEQ[SN-1]; T1=SEQ[SN][1] if SN<len(SEQ) else END; DUR=T1-T0; G0=int(round(T0*FPS)); G1=int(round(T1*FPS))
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
