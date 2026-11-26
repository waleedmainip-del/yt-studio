# extra animation helpers for avatars + Ember
def root_mat(H):
    r=H['root']; return Matrix.Translation(r.location)@r.rotation_euler.to_matrix().to_4x4()
def arm_to(H,s,target,k=1.0,base=None):
    """point arm s of avatar H toward world target (blend k with base rotation)"""
    Mi=root_mat(H).inverted(); P=H['arm'][s]; u=H['u']
    sh=Vector(P.location)+Vector((s*.5*u,0,0)); tl=Mi@Vector(target); d=(tl-sh)
    if d.length<1e-5: return
    d.normalize(); a=math.asin(max(-1,min(1,d.y))); b=math.atan2(-d.x,-d.z)
    b0=base or (0,0,0)
    P.rotation_euler=(L(b0[0],a,k),L(b0[1],b,k),L(b0[2],0,k))
def arms(H,rx1=0,ry1=0,rz1=0,rx2=0,ry2=0,rz2=0):
    H['arm'][1].rotation_euler=(R(rx1),R(ry1),R(rz1)); H['arm'][-1].rotation_euler=(R(rx2),R(ry2),R(rz2))
def legs0(H):
    for q in (1,-1): H['leg'][q].rotation_euler=(0,0,0); H['leg'][q].location[2]=2.0*H['u']
def sit(H,k,seat_h,legs=90):
    u=H['u']
    for q in (1,-1): H['leg'][q].rotation_euler[0]=-R(legs)*k; H['leg'][q].location[2]=2.0*u
    H['root'].location[2]=L(H['z0']+.008,seat_h-1.5*u,k)
def look_at(H,target,amt=1.0,maxyaw=60,maxpitch=35):
    Mi=root_mat(H).inverted(); u=H['u']; tl=Mi@Vector(target); hp=Vector((0,0,4.75*u)); d=tl-hp
    yaw=math.atan2(d.x,-d.y); pit=math.atan2(-d.z,math.hypot(d.x,d.y))
    yaw=max(-R(maxyaw),min(R(maxyaw),yaw)); pit=max(-R(maxpitch),min(R(maxpitch),pit))
    H['head'].rotation_euler[2]=yaw*amt; H['head'].rotation_euler[0]=pit*amt
def heading_to(H,target):
    dx=target[0]-H['root'].location[0]; dy=target[1]-H['root'].location[1]; return math.degrees(math.atan2(dx,-dy))
def path_pos(pts,d):
    """position + heading(deg) at distance d along polyline pts"""
    acc=0
    for i in range(len(pts)-1):
        a=Vector(pts[i]); b=Vector(pts[i+1]); sl=(b-a).length
        if d<=acc+sl or i==len(pts)-2:
            f=max(0,min(1,(d-acc)/max(1e-6,sl))); p=a.lerp(b,f); h=math.degrees(math.atan2(b.x-a.x,-(b.y-a.y))); return p,h
        acc+=sl
def path_len(pts): return sum((Vector(pts[i+1])-Vector(pts[i])).length for i in range(len(pts)-1))
def walk_path(H,pts,t,t0,t1,z=None,step=.55,ease_in=.25,ease_out_=.25,run_=False,arm=26,mood=0,turn_smooth=True):
    """walk along polyline between t0..t1 with soft start/stop; returns progress 0..1"""
    Lt=path_len(pts); T=t1-t0; q=max(0,min(1,(t-t0)/T))
    # trapezoid velocity profile
    a=ease_in; b=ease_out_; vmax=1/(1-(a+b)/2)
    if q<a: f=vmax*q*q/(2*a)
    elif q<1-b: f=vmax*(a/2+(q-a))
    else: r_=1-q; f=1-vmax*r_*r_/(2*b)
    d=Lt*max(0,min(1,f)); p,h=path_pos(pts,d)
    if turn_smooth:
        p2,h2=path_pos(pts,min(Lt,d+.5)); h=lerp_angle(h,h2,.5)
    H['root'].location[0]=p.x; H['root'].location[1]=p.y
    if z is not None: H['z0']=z
    H['root'].rotation_euler[2]=R(h)
    if 0<q<1 or d<Lt-1e-3:
        if run_: run(H,d,arm=arm)
        else: walk(H,d,step=step,arm=arm,mood=mood)
        # fade stride at ends
        k=min(1,q/max(1e-3,a))*min(1,(1-q)/max(1e-3,b))
        for s_ in (1,-1): H['leg'][s_].rotation_euler[0]*=k; H['arm'][s_].rotation_euler[0]*=k
    return q
def stand(H,t):
    legs0(H); idle(H,t)
def mouth_talk(H,t,t0,t1,shapes=('o','flat','O','flat'),rate=7.0,rest='flat'):
    if t0<=t<t1: face(H,mouth=shapes[int((t-t0)*rate)%len(shapes)])
    elif t>=t1: face(H,mouth=rest)
# ---- dragon helpers
def d_world_head(D):
    return D['head'].matrix_world.translation
def dset(D,loc=None,rz=None,pitch=None,roll=None):
    r=D['root']
    if loc is not None: r.location=loc
    if rz is not None: r.rotation_euler[2]=R(rz)
    if pitch is not None: r.rotation_euler[0]=R(pitch)
    if roll is not None: r.rotation_euler[1]=R(roll)
def dhop(D,t,t0,dur,h,base_z):
    q=(t-t0)/dur
    if 0<q<1: return base_z+4*h*q*(1-q)
    return base_z
def dflap(D,t,rate=7.0,amp=40,fold=.2):
    wings(D,fold,amp*math.sin(t*rate*2*pi)+10)
def pouch(H,col=None,depth=.075):
    """bulging kangaroo pocket pouch on the hoodie front (hides Ember's body). returns pivot empty (scale it to wiggle)"""
    u=H['u']; c=col or H['C']['top']; fr=-.5*u
    for ch in H['root'].children:
        lx,ly,lz=ch.location
        if ch.type=='MESH' and abs(abs(lx)-.58*u)<.01 and abs(lz-2.62*u)<.01: ch.scale=(0,0,0)
        if ch.type=='MESH' and abs(lx)<.01 and abs(lz-2.5*u)<.01 and abs(ly-(fr-.012))<.01: ch.scale=(0,0,0)
    pv=empty((0,fr,2.12*u),H['root'])
    obox((0,-depth,.3*u),(.68*u,depth,.3*u),M(c,.8,kind='fabric',spec=.2),.065,pv)
    obox((0,-2*depth+.004,.56*u),(.56*u,.008,.018*u),M(shade(c,.78),.8),.004,pv)
    return pv
def _hand_local(H,s,a,b,c=0.0):
    u=H['u']; v=Vector((s*.5*u,0,-1.8*u)); return Vector(H['arm'][s].location)+Euler((a,b,c)).to_matrix()@v
def arm_reach(H,s,target,k=1.0,base=(0,0,0)):
    """rotate arm so the hand centre lands as close as possible to world target"""
    tl=root_mat(H).inverted()@Vector(target)
    best=(0,0); be=1e9
    for a in [R(x) for x in range(-180,61,12)]:
        for b in [R(x) for x in range(-90,91,12)]:
            e=(_hand_local(H,s,a,b)-tl).length
            if e<be: be=e; best=(a,b)
    st=R(6)
    for _ in range(18):
        a0,b0=best; imp=False
        for da,db in ((st,0),(-st,0),(0,st),(0,-st)):
            e=(_hand_local(H,s,a0+da,b0+db)-tl).length
            if e<be: be=e; best=(a0+da,b0+db); imp=True
        if not imp: st*=.5
    H['arm'][s].rotation_euler=(L(base[0],best[0],k),L(base[1],best[1],k),L(base[2],0,k))
    return be

def egg_fx(E,glowcol='#FFD27A'):
    """make shell faintly emissive + cracks glow gold; returns shell material"""
    sm=E['shell_mat']=bpy.data.materials.new('eggshell'); sm.use_nodes=True; b=sm.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=hexc('#A8E6DC'); b.inputs['Roughness'].default_value=.35; b.inputs['Emission Color'].default_value=hexc(glowcol); b.inputs['Emission Strength'].default_value=0
    for o in E['root'].children_recursive:
        if o.type=='MESH' and o.data.materials and o.data.materials[0].name.startswith('#A8E6DC'): o.data.materials[0]=sm
    cm=M('#FFD27A',.3,emit=3.0)
    for o in E['cracks']: o.data.materials[0]=cm
    return sm
def egg_shine(E,k):
    E['shell_mat'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=k
