exec(open('/home/claude/murree/base_by.py').read())
for _f in ('chars_by','cast_by','look_by','anim_by','fx_by','world_by'): exec(open('/home/claude/murree/%s.py'%_f).read())
SET=args[3]; out=args[4]; cams=eval(args[5])
if SET=='mw': motorway(); dhaba(); C=hero_car(HERO_LANE,HERO_Y,0); car(LANES[3],HERO_Y,'#E8A33A',90,roof='pateela'); D=donkey_cart(LANES[3]+1.9,HERO_Y+3,90); B.done('m'); setup_render('morning',res=PCT,samples=SAMPLES,shadow_dist=60)
elif SET=='mt': mountain_road(); C=hero_car(MX+2.2,4,0); B.done('m'); setup_render('snowy',res=PCT,samples=SAMPLES,shadow_dist=40)
elif SET=='mall': mall_road(); B.done('m'); setup_interior('night',(LX,0,8),res=PCT,samples=SAMPLES,shadow_dist=30)
elif SET=='hotel': hotel(); B.done('m'); setup_interior('day',(HX,0,3.6),res=PCT,samples=SAMPLES); bpy.context.scene.view_settings.exposure=-.5
elif SET=='roof': home_roof(); B.done('m'); setup_render('snowy',res=PCT,samples=SAMPLES,shadow_dist=30)
make_cam(); sc=bpy.context.scene
for i,(loc,tg,lens) in enumerate(cams):
    camset(loc,tg,lens,8); sc.render.filepath=out+'_%d.png'%i; bpy.ops.render.render(write_still=True)
