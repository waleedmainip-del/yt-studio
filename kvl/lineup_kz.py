import os
LH=os.environ.get('LH','/home/claude/kz')
exec(open(LH+'/base_lh.py').read())
for _f in ('chars_base','look_lh','anim_lh','fx_lh','chars_lh','chars_dk','chars_bd','chars_bg','cast_kz','world_lh','world_kb','gen_kb'): exec(open(LH+'/%s.py'%_f).read())
make_cam(); G=os.environ.get('GRP','H'); D=CAST if G=='H' else (ZCAST if G=='Z' else dict(('C%02d'%i,c) for i,c in enumerate(CROWD[:12] if G=='C' else CROWD[12:])))
if G=='E': D=dict(F1=FRIENDS[0],F2=FRIENDS[1],F3=FRIENDS[2],F4=FRIENDS[3],DHOLI2=DHOLI2,BAT1=CRICK[0],BAT2=CRICK[1],BAT3=CRICK[2],BAT4=CRICK[3],ZRICK=ZRICK,ZCHAI=ZCHAI,ZCRIC=ZCRIC)
if G=='Y': D=dict(('Z%02d'%i,c) for i,c in enumerate(ZVAR[10:]))
names=list(D.keys()); R0=int(os.environ.get('ROW','0')); names=names[R0*6:R0*6+6]; n=len(names); sp=2.55
B.box((0,0,-.05),(sp*n/2+2,6,.05),M('#8FA0B4' if G!='Z' else '#6E7A8E',.9),0); B.box((0,3.2,3),(sp*n/2+2,.1,3.6),M('#7E90A6' if G!='Z' else '#5E6A80',.95),0); B.done('studio')
for i,nm in enumerate(names):
    x=-(n-1)*sp/2+i*sp; H=avatar_kz((x,0,0),-18,D[nm],name=nm); stand(H,0); blink(H,1.0,force=0); face(H,mouth='smile' if G!='Z' else 'flat')
    if D[nm].get('zombie'):
        for s in (1,-1): H['arm'][s].rotation_euler=(R(-62),0,R(s*5))
    stext(nm,(x,-.9,2.5*D[nm].get('h',1)+.45),.25,'#FFFFFF',e=.6)
S,A,w,bg=setup_interior('day',room=(0,-1,6.0),res=100,samples=SAMPLES,shadow_dist=20); A.data.energy=150; A.data.size=14; point((0,-9,4.0),1500,(1,.97,.92),r=2.5,shadow=False)
sc=bpy.context.scene; sc.render.resolution_x=2160; sc.render.resolution_y=620; CAM.data.type='ORTHO'; CAM.data.ortho_scale=sp*6+1.5; CAM.location=(0,-14,1.82); TGT.location=(0,0,1.82); CAM.data.dof.use_dof=False
sc.render.filepath=LH+'/render/lineup_%s%d.png'%(G,R0); bpy.ops.render.render(write_still=True)
