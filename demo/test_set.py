exec(open('/home/claude/demo/base_by.py').read())
for _f in ('chars_by','cast_by','look_by','anim_by','fx_by','world_by'): exec(open('/home/claude/demo/%s.py'%_f).read())
SET=args[3]; out=args[4]; cams=eval(args[5])
if SET=='room': D=trading_room(args[6] if len(args)>6 else 'day'); gaming_chair(CHAIR[0],CHAIR[1],0); B.done('r'); setup_interior('day' if 'day' in args else 'night',(0,0,3.3),res=PCT,samples=SAMPLES); bpy.context.scene.view_settings.exposure=-.6
elif SET=='gate': gate_street(); B.done('g'); setup_render('sunset',res=PCT,samples=SAMPLES,shadow_dist=30)
elif SET=='roof': rooftop(); B.done('f'); setup_interior('night',(RX,RY,6),res=PCT,samples=SAMPLES)
elif SET=='shop': shop_street(); B.done('s'); setup_interior('night',(SX,0,6),res=PCT,samples=SAMPLES)
elif SET=='road': main_road(); B.done('m'); setup_render('afternoon',res=PCT,samples=SAMPLES,shadow_dist=40)
w=person(eval(args[7]) if len(args)>7 else (0,0,0),0,WALEED,'smile',name='w')
make_cam(); sc=bpy.context.scene
for i,(loc,tg,lens) in enumerate(cams):
    camset(loc,tg,lens,8); sc.render.filepath=out+'_%d.png'%i; bpy.ops.render.render(write_still=True)
