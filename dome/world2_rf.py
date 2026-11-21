# props + pose helpers for "The City Under the Dome"
def hide(o): o.scale=(0,0,0)
def show(o,s=(1,1,1)): o.scale=s
def hideH(H): H['root'].scale=(0,0,0)
def no_shadow(Hc):
    for o in Hc['root'].children_recursive:
        if o.type=='MESH': o.visible_shadow=False
def wrench(H,s=1):
    u=H['u']; P=H['arm'][s]; STL=M('#B9C2CC',.25,metal=.9); GRP=M('#C9452E',.5)
    e=empty((s*.5*u,-.05*u,-1.85*u),P)
    obox((0,0,-.12),(.03,.022,.2),GRP,.01,e); obox((0,0,-.4),(.022,.016,.14),STL,.008,e)
    obox((0,0,-.58),(.07,.02,.06),STL,.01,e); obox((-.04,0,-.66),(.025,.02,.05),STL,.006,e); obox((.04,0,-.67),(.022,.02,.05),STL,.006,e)
    return e
def headlamp(H,on=True,e=220):
    u=H['u']; Hd=H['head']
    obox((0,0,1.0*u),(.645*u,.645*u,.06*u),M('#22242B',.6),.02*u,Hd)
    obox((0,-.66*u,1.0*u),(.14*u,.06*u,.11*u),M('#3A3D47',.4,metal=.5),.03*u,Hd)
    lens=ocyl((0,-.72*u,1.0*u),.09*u,.02,M('#FFF6D8',.2,emit=(6.0 if on else .0)),Hd)
    sp=None
    if on:
        bpy.ops.object.light_add(type='SPOT',location=(0,0,0)); sp=bpy.context.object; sp.parent=Hd; sp.location=(0,-.8*u,1.0*u); sp.rotation_euler=(R(-90),0,0)
        sp.data.energy=e; sp.data.spot_size=R(38); sp.data.spot_blend=.6; sp.data.color=(1,.95,.82); sp.data.shadow_soft_size=.02
    return sp
def nova_extras(H):
    u=H['u']; root=H['root']; fr=-.5*u
    obox((0,0,4.02*u),(.48*u,.48*u,.1*u),M('#2E6E78',.5),.04*u,root)                       # suit collar ring
    for (x,z,c) in ((-.45,3.45,'#2E6E78'),(.5,2.6,'#C9CDD6'),(-.2,2.45,'#8E3B32')): obox((x*u,fr-.022,z*u),(.16*u,.01,.13*u),M(c,.8,kind='fabric'),.01,root)
    for x in (-.65,.62): obox((x*u,fr-.06,2.1*u),(.17*u,.06,.14*u),M('#4A3526',.7),.02*u,root)   # belt pouches
    for s in (-1,1): obox((s*1.02*u,0,3.6*u),(.06*u,.52*u,.06*u),M('#2E6E78',.5),.01,root)
    obox((0,.62*u,3.0*u),(.42*u,.16*u,.62*u),M('#3E4652',.5,metal=.4),.06*u,root)            # small air tank
    obox((0,.8*u,3.62*u),(.12*u,.06*u,.1*u),M('#E8743B',.5),.02*u,root)
def cloth(H,s=1):
    u=H['u']; e=empty((s*.5*u,-.1*u,-2.0*u),H['arm'][s]); obox((0,0,0),(.09,.06,.07),M('#E8E4D8',.9,kind='fabric'),.03,e); return e
def mop(H):
    u=H['u']; e=empty((.5*u,-.1*u,-1.85*u),H['arm'][1])
    obox((0,0,.05),(.018,.018,.75),M('#8A6A4A',.6,kind='wood'),.008,e,rot=(0,0,0)); obox((0,0,-.78),(.16,.1,.08),M('#D8D2C0',.95,kind='fabric'),.04,e)
    return e
def roller(H):
    u=H['u']; e=empty((.5*u,-.1*u,-1.85*u),H['arm'][1])
    obox((0,0,-.25),(.015,.015,.3),M('#3E4652',.4,metal=.6),.005,e); obox((0,0,-.58),(.2,.05,.05),M('#2A85C8',.4),.04,e)
    return e
def crawl(H,hip,yaw,t,rate=4.0,amp=14):
    """hands-and-knees crawl; hip=(x,y,z) world, yaw deg (0 = facing -y)"""
    u=H['u']; pitch=R(72); r=H['root']; r.rotation_euler=(pitch,0,R(yaw))
    off=Euler((pitch,0,R(yaw))).to_matrix()@Vector((0,0,2.0*u)); p=Vector(hip)-off; r.location=tuple(p)
    ph=math.sin(t*rate)
    for s in (1,-1):
        H['leg'][s].rotation_euler=(R(-38+amp*ph*s),0,0); H['leg'][s].location[2]=2.0*u
        H['arm'][s].rotation_euler=(R(-74-amp*ph*s),0,R(-s*4))
    H['head'].rotation_euler=(R(-58),0,0)
def swing(H,k,both=True):
    """k: 0 = raised behind head, 1 = struck forward"""
    a=L(-175,-62,k)
    H['arm'][1].rotation_euler=(R(a),R(-6),R(14));
    if both: H['arm'][-1].rotation_euler=(R(a+6),R(6),R(-14))
    H['root'].rotation_euler[0]=R(L(-6,10,k))
def dust_motes(center,n,t0,t1,seed=3,vel=(0,-.35,0),spread=(.8,.05,.25),mat=None):
    r=random.Random(seed); mat=mat or M('#FFF1D0',.3,emit=3.0,alpha=.8); ms=[]
    for i in range(n):
        o=oico(center,r.uniform(.004,.008),mat,sub=1); ms.append((o,Vector((r.uniform(-spread[0],spread[0]),r.uniform(-spread[1],spread[1]),r.uniform(-spread[2],spread[2]))),r.uniform(0,1),r.uniform(.7,1.3)))
    def f(o,t):
        pass
    def upd(t):
        for o,d,ph,sp in ms:
            q=((t-t0)/(t1-t0)*sp+ph)%1.0
            o.location=tuple(Vector(center)+d*(.2+q)+Vector(vel)*q*3+Vector((0,0,.05*math.sin(t*3+ph*6))))
            o.scale=(1,1,1) if t>=t0 else (0,0,0)
    return upd
