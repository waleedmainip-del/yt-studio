exec(open('/home/claude/boy/base_by.py').read())
for _f in ('chars_by','cast_by','look_by','anim_by','fx_by','world_by'): exec(open('/home/claude/boy/%s.py'%_f).read())
# usage: blender -b -P sheet_by.py -- NAME PCT SAMPLES mode   (mode: char | lineup | env)
NAME=args[0]; MODE=args[3] if len(args)>3 else 'char'
OUT='/home/claude/boy/sheets'; os.makedirs(OUT,exist_ok=True)
sc=bpy.context.scene; make_cam()
def headpos(H): u=H['u']; return tuple(root_mat(H)@Vector((0,0,4.75*u)))
CH={'waleed':WALEED,'ammi':AMMI,'bilal':BILAL,'uncle':UNCLE,'aunty':AUNTY2}
def studio():
    B.box((0,0,-.05),(20,20,.05),M('#D9D3C7',.8),0); B.box((0,6,4),(20,.1,4),M('#EEEAE2',.85),0)
    for k in range(0,9): B.box((-8+2*k,5.85,.012),(.006,.006,.012),M('#888888',.5),0)
    B.done('studio'); setup_interior('day',(0,0,4),res=PCT,samples=SAMPLES); bpy.context.scene.world.color=(1,1,1)
def snap(fn):
    sc.render.filepath=OUT+'/'+fn; bpy.ops.render.render(write_still=True); print('SNAP',fn,flush=True)
if MODE=='lineup':
    studio(); keys=['waleed','bilal','uncle','aunty','ammi']; HS=[]
    for i,k in enumerate(keys):
        H=person((-4.5+i*1.5,0,0),0,CH[k],'smile',name=k); stand(H,0); arms(H,-10,0,5,-10,0,-5); HS.append(H)
    # height ruler
    for z in range(0,25):
        B.box((-6.2,0,z*.1),(.08 if z%5 else .16,.01,.004),M('#22242B',.4),0)
    B.box((-6.2,0,1.25),(.01,.01,1.25),M('#22242B',.4),0); B.done('ruler')
    sc.render.resolution_x=1920; sc.render.resolution_y=1080
    camset((0,-12.5,1.4),(0,0,1.2),40,22)
    snap('lineup.png')
    for i,k in enumerate(keys):
        H=HS[i]; bpy.context.view_layer.update(); top=max((o.matrix_world@Vector(c)).z for o in [H['root']]+list(H['root'].children_recursive) if o.type=='MESH' for c in o.bound_box)
        print('HEIGHT',k,round(top,3),flush=True)
elif MODE=='char':
    studio(); C=CH[NAME]; H=person((0,0,0),0,C,'smile',name=NAME)
    u=H['u']; hz=4.75*u
    for i,rz in enumerate((0,-45,-90,180)):
        legs0(H); stand(H,0); H['root'].rotation_euler=(0,0,R(rz)); arms(H,-8,0,6,-8,0,-6); face(H,mouth='smile'); H['head'].rotation_euler=(0,0,0)
        camset((0,-6.2,1.25),(0,0,1.15),42,22); snap('%s_v%d.png'%(NAME,i))
    # walking pose
    H['root'].rotation_euler=(0,0,R(-35)); walk_path(H,[(-.5,0),(.5,0)],.37,0,2.0,step=.55,arm=26); H['root'].location=(0,0,H['root'].location[2]); H['root'].rotation_euler=(0,0,R(-60))
    camset((0,-6.2,1.25),(0,0,1.15),42,22); snap('%s_walk.png'%NAME)
    # sitting pose on a cube seat
    seat=obox((0,0,.27),(.3,.3,.27),M('#8E1F33',.6,kind='fabric'),.03)
    legs0(H); H['root'].location=(0,0,0); H['root'].rotation_euler=(0,0,R(-30)); seat.rotation_euler=(0,0,R(-30)); H['z0']=0; sit(H,1.0,.55,90); arms(H,-35,0,8,-35,0,-8)
    camset((0,-6.2,1.0),(0,0,.95),42,22); snap('%s_sit.png'%NAME); hide(seat)
    legs0(H); H['root'].location=(0,0,0); stand(H,0); H['root'].rotation_euler=(0,0,R(-12)); arms(H,-8,0,6,-8,0,-6)
    EX=[('happy',dict(mouth='grin',brow=.03,eyes=1.0),(0,0,0)),('angry',dict(mouth='frown',brow=-.06,brow_r=20,eyes=1.05),(R(-4),0,0)),
        ('confused',dict(mouth='flat',brow=.02,brow_r=14,eyes=.85),(0,R(12),0)),('surprised',dict(mouth='O',brow=.08,eyes=1.35),(R(-6),0,0)),('laughing',dict(mouth='grin',brow=.05,eyes=.12),(R(-10),0,0))]
    for nm,kw,hr in EX:
        face(H,**kw); H['head'].rotation_euler=hr
        if nm=='angry': arms(H,-40,0,-30,-40,0,30)
        elif nm=='confused': arms(H,-8,0,6,-120,0,-50)
        elif nm=='surprised': arms(H,-30,0,-60,-30,0,60)
        else: arms(H,-8,0,6,-8,0,-6)
        h=headpos(H)
        camset((h[0]+.35,h[1]-2.1,h[2]-.05),(h[0],h[1],h[2]-.12),62,22); snap('%s_x_%s.png'%(NAME,nm))
elif MODE=='env':
    D=bedroom(night=(NAME=='night')); gaming_chair(CHAIR[0],CHAIR[1],0); drawing_room(); street_corner(); B.done('env'); setup_interior('night' if NAME=='night' else 'day',(0,0,3.4),res=PCT,samples=SAMPLES,shadow_dist=12); bpy.context.scene.view_settings.exposure=(-.2 if NAME=='night' else -.7)
    set_clock(D,11,47)
    w=person((0,0,0),0,WALEED,'smile',name='waleed'); lie(w,-1.35,1.25,BED['top']); dr=Drape(-2.9,-.1,.15,2.65,bed=BED); dr.update(-1.9); 
    ph,scr=phone_obj('scr_cat2'); ph.location=(-.9,-.2,1.2)
    V=[('bed',(1.2,-1.6,2.0),(-1.6,1.2,.8),20),('lie',(-.4,-.6,1.9),(-1.6,1.4,.9),26),('desk',(-.6,-1.2,1.7),(2.4,.3,1.0),20),('door',(-1.2,1.6,1.9),(1.6,-2.0,1.2),20),('wall',(.5,-.5,1.6),(-1.7,2.5,1.9),24),('clock',(.8,.1,2.4),(3.0,.1,2.5),30),
       ('lr',(LX-3.4,-2.8,2.2),(LX+.5,1.5,.8),20),('lr2',(LX+2.8,-2.6,2.0),(LX-1,1.8,.8),20),('street',(SX+1.2,-3.5,1.8),(SX,2.5,1.6),22)]
    for nm,loc,tg,lens in V:
        camset(loc,tg,lens,22); snap('env_%s_%s.png'%(NAME,nm))
