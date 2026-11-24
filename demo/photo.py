exec(open('/home/claude/demo/base_by.py').read())
for _f in ('chars_by','cast_by','look_by','anim_by','fx_by','world_by','shots_by'): exec(open('/home/claude/demo/%s.py'%_f).read())
make_cam(); spec=SHOTS['P_photo'](); spec['upd'](1.0); sc=bpy.context.scene; sc.render.filepath='/home/claude/demo/assets/zain_photo.png'; bpy.ops.render.render(write_still=True)
