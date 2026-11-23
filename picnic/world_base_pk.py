# generic helpers (from shared toolkit)
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=True):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot; a.data.use_shadow=shadow; return a
def seg(a,b,r,mat,sides=6):
    a=Vector(a); b=Vector(b); d=b-a; c=(a+b)/2; rot=d.to_track_quat('Z','Y').to_euler(); B.cyl(tuple(c),r,d.length,mat,rot=tuple(rot),seg=sides)
LEAF=M('#3E8E4A',.7,kind='leaves'); LEAF2=M('#5FA84A',.7,kind='leaves'); TRUNK=M('#6B4A30',.8,kind='wood')
def tree(x,y,z,s,seed,palm=False):
    r=random.Random(seed)
    if palm:
        B.cyl((x,y,z+2.5*s),.16*s,5*s,TRUNK,seg=8)
        for i in range(7):
            a=2*pi*i/7; B.box((x+math.cos(a)*1.0*s,y+math.sin(a)*1.0*s,z+4.9*s),(1.1*s,.25*s,.03),LEAF,0,rot=(0,R(25),a))
        return
    B.cyl((x,y,z+1.1*s),.16*s,2.2*s,TRUNK,seg=8)
    for i in range(5): B.ico((x+r.uniform(-.6,.6)*s,y+r.uniform(-.6,.6)*s,z+(2.5+r.uniform(0,.9))*s),(.85+r.random()*.4)*s,LEAF if i%2 else LEAF2,sc=(1,1,.85),sub=1)
def wires(x0,x1,y0,y1,z,n,seed):
    r=random.Random(seed); W_=M('#1A1A1E',.6)
    for i in range(n):
        xa=r.uniform(x0,x1); xb=xa+r.uniform(-4,4); za=z+r.uniform(-.6,.8); zb=z+r.uniform(-.6,.8); sag=r.uniform(.3,.8); pts=[]
        for k in range(7):
            f=k/6; pts.append((L(xa,xb,f),L(y0,y1,f),L(za,zb,f)-sag*4*f*(1-f)))
        for a,b in zip(pts,pts[1:]): seg(a,b,.012,W_,sides=4)
KITE=['#C9302C','#2E8B6E','#F2C12E','#2B58C9','#E07A2E','#D98AA8','#7448C2']
def rickshaw(x,y,rz=0,col='#2E8B6E'):
    r=empty((x,y,0),rot=(0,0,R(rz))); BODY=M(col,.35,metal=.2); TOP=M('#1E1A18',.8,kind='fabric'); CH=M('#C9CDD6',.3,metal=.8); TI=M('#111216',.8)
    obox((0,0,.7),(1.0,.62,.35),BODY,.08,r); obox((-.2,0,1.45),(.9,.66,.06),TOP,.05,r); obox((.75,0,1.0),(.2,.5,.3),BODY,.06,r)
    obox((.85,0,1.2),(.03,.45,.25),M('#9FC7D8',.08,spec=1.0,alpha=.5),.01,r)
    for s in (-1,1): seg_o=obox((-.9,s*.6,1.05),(.03,.03,.4),CH,.005,r); obox((-.3,s*.63,.75),(.7,.01,.08),M('#F2C12E',.5),.005,r)
    obox((-.4,0,.95),(.5,.55,.06),M('#9E3B4E',.8,kind='fabric'),.03,r); obox((-.85,0,1.15),(.08,.55,.3),M('#9E3B4E',.8,kind='fabric'),.03,r)
    for sx,sy in ((-.6,.6),(-.6,-.6),(1.0,0)): ocyl((sx,sy,.25),.25,.12,TI,r,rot=(R(90),0,0),seg=14)
    obox((1.05,0,.75),(.04,.12,.05),M('#FFF2C8',.3,emit=4),.01,r); return r
def bike(x,y,rz=0,col='#C9302C'):
    r=empty((x,y,0),rot=(0,0,R(rz))); BODY=M(col,.35,metal=.3); TI=M('#111216',.8); CH=M('#C9CDD6',.3,metal=.8)
    for sx in (-.6,.6): ocyl((sx,0,.3),.3,.08,TI,r,rot=(R(90),0,0),seg=14)
    obox((0,0,.6),(.45,.14,.18),BODY,.05,r); obox((-.25,0,.82),(.35,.15,.05),M('#1E1A18',.6),.03,r); obox((.55,0,.9),(.04,.35,.03),CH,.01,r); obox((.5,0,.7),(.03,.03,.25),CH,.005,r,rot=(0,R(-20),0))
    return r
def car(x,y,col,rz=0,parent=None):
    r=empty((x,y,0),rot=(0,0,R(rz))) if parent is None else parent
    BODY=M(col,.18,metal=.5); GL=M('#22303E',.05,spec=1.0); TIRE=M('#111216',.8); RIM=M('#D8DEE6',.25,metal=.9)
    obox((0,0,.55),(2.25,.95,.3),BODY,.1,r); obox((-.25,0,1.08),(1.2,.86,.3),BODY,.14,r); obox((-.25,0,1.09),(1.15,.88,.24),GL,.06,r)
    for s in (-1,1): obox((2.24,s*.62,.62),(.03,.2,.07),M('#FFF2C8',.3,emit=4),.01,r); obox((-2.24,s*.62,.66),(.03,.22,.07),M('#E8262A',.3,emit=2),.01,r)
    obox((2.26,0,.45),(.03,.5,.08),M('#2B2C33',.4),.01,r)
    for sx in (-1.4,1.4):
        for sy in (-1,1): ocyl((sx,sy*(.93),.34),.34,.24,TIRE,r,rot=(R(90),0,0),seg=18); ocyl((sx,sy*1.05,.34),.2,.02,RIM,r,rot=(R(90),0,0),seg=14)
    return r
