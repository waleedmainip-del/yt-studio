exec(open('/home/claude/murree/base_by.py').read())
for _f in ('chars_by','cast_by','look_by','anim_by','fx_by','world_by','shots_by'): exec(open('/home/claude/murree/%s.py'%_f).read())
make_cam(); DUR=4.0; spec=SHOTS['R_snowman'](); spec['upd'](.1)
am=[o for o in bpy.data.objects if o.name.startswith('ammi')]
_camset((RX-.6,-4.2,1.5),(RX,.4,1.1),20,8,focus=(RX,.4,1.2))
sc=bpy.context.scene; sc.render.filepath='/home/claude/murree/assets/roof_photo.png'; bpy.ops.render.render(write_still=True)
