# World kit for "Everyone Is From Karachi": common helpers, vehicles (W-11 bus with interior, water tanker), token crowds,
# and SET A: faisal() - Shahrah-e-Faisal boulevard (towers, billboards, gantry sign, footbridge, bus stop).
BALLS=[]
MOODS['khi']=dict(sun=(58,-60),e=3.0,col=(1,.91,.76),top='#2F7FE0',bot='#C6E4FF',sky=.9,mist='#D8E6F2',cloud='#FFFFFF',cov=.52,cstr=.9)
MOODS['khi_am']=dict(sun=(64,118),e=2.6,col=(1,.9,.78),top='#4C92E0',bot='#FFE3C8',sky=.85,mist='#E8E0D6',cloud='#FFFFFF',cov=.56,cstr=.85)
MOODS['khi_dusk']=dict(sun=(78,-66),e=2.0,col=(1,.66,.42),top='#3E4E9A',bot='#FF9C68',sky=.9,mist='#D89A84',cloud='#F0909C',cov=.44,cstr=.85)
MOODS['khi_night']=dict(sun=(58,-140),e=.6,col=(.62,.72,1.0),top='#070C22',bot='#22305A',sky=.6,mist='#1A2240',cloud='#2A3458',cov=.42,cstr=.6)
MOODS['khi_dawn']=dict(sun=(82,96),e=1.9,col=(1,.7,.5),top='#5A78C8',bot='#FFB48A',sky=.9,mist='#F0B8A0',cloud='#FFC4B0',cov=.46,cstr=.85)
MOODS['khi_rain']=dict(sun=(62,140),e=1.5,col=(.86,.9,1.0),top='#56627A',bot='#A8B2BE',sky=.9,mist='#9AA4B0',cloud='#6E7888',cov=.3,cstr=.95)
NIGHT=[0.0]          # 0 = day, 1 = night. scales lit windows / signs / lamps
LITM=[]              # (material, emission) of everything electric (for the blackout)
VS=1.5               # car / rickshaw scale so vehicles fit ~2.5 m characters
def lit(col,e,rough=.35,always=False):
    k=1.0 if always else NIGHT[0]; ev=round(max(.0,e*k),3)
    m=M(col,rough,emit=ev) if ev>0 else M(col,rough)
    if ev>0 and (m,ev) not in LITM: LITM.append((m,ev))
    return m
def power(k):
    """blackout control: k=1 everything on, 0 off"""
    for m,e in LITM: m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=e*k
def sign(body,loc,size,col='#FFFFFF',bg='#1E6A3A',n=(0,-1,0),e=0.0,pad=.28,th=.1,parent=None,w=None,frame=None,always=False):
    """board sized to its text (text always fully on the board). returns half-size (hw,hh)"""
    a=math.atan2(n[0],-n[1]); hw=(w or len(body)*size*.345)+pad; hh=size*.6+pad*.7; nv=Vector((n[0],n[1],0)).normalized()
    bm=lit(bg,e*.35,.5,always) if e else M(bg,.55)
    if parent is None:
        B.box(loc,(hw,th/2,hh),bm,0,rot=(0,0,a))
        if frame: B.box(tuple(Vector(loc)-nv*.01),(hw+.09,th/2,hh+.09),M(frame,.4,metal=.4),0,rot=(0,0,a))
    else:
        obox(loc,(hw,th/2,hh),bm,.0,parent,rot=(0,0,a))
        if frame: obox(tuple(Vector(loc)-nv*.01),(hw+.09,th/2,hh+.09),M(frame,.4,metal=.4),0,parent,rot=(0,0,a))
    p=Vector(loc)+nv*(th/2+.014)
    ev=e*(1.0 if always else NIGHT[0]); tm=M(col,.4,emit=round(ev,3)) if ev>0 else M(col,.5)
    if ev>0 and (tm,round(ev,3)) not in LITM: LITM.append((tm,round(ev,3)))
    text(body,tuple(p),n,size,tm,ex=.012,parent=parent); return hw,hh
def bseg(p,q,rad,mat,seg=5):
    d=Vector(q)-Vector(p); B.cyl(tuple((Vector(p)+Vector(q))/2),rad,d.length,mat,rot=d.to_track_quat('Z','Y').to_euler(),seg=seg)
# ---------------------------------------------------------------- token people (static, batched): crowds far from camera
def token(x,y,rz,top,pants,skin,hair,h=1.0,zombie=False,z=0.0,arms=None,hat=None):
    u=.42*h; a=R(rz); c=math.cos(a); s=math.sin(a); rot=(0,0,a)
    def P(lx,ly,lz): return (x+lx*c-ly*s,y+lx*s+ly*c,z+lz)
    tm=M(top,.8); sk=M(skin,.55)
    B.box(P(0,0,1.0*u),(.98*u,.5*u,1.0*u),M(pants,.85),.03,rot=rot); B.box(P(0,0,3.0*u),(1.0*u,.5*u,1.0*u),tm,.03,rot=rot)
    B.box(P(0,0,4.75*u),(.62*u,.62*u,.6*u),sk,.05,rot=rot); B.box(P(0,.03*u,5.3*u),(.66*u,.66*u,.14*u),M(hat or hair,.6),.03,rot=rot); B.box(P(0,.5*u,4.95*u),(.66*u,.16*u,.4*u),M(hair,.6),.03,rot=rot)
    if zombie or arms=='fwd':
        for sx in (-1,1): B.box(P(sx*1.5*u,-.75*u,3.55*u),(.46*u,1.05*u,.44*u),tm,.03,rot=rot); B.box(P(sx*1.5*u,-1.95*u,3.55*u),(.43*u,.2*u,.42*u),sk,.03,rot=rot)
    elif arms=='up':
        for sx in (-1,1): B.box(P(sx*1.5*u,0,4.7*u),(.46*u,.46*u,1.05*u),tm,.03,rot=rot); B.box(P(sx*1.5*u,0,5.9*u),(.43*u,.43*u,.2*u),sk,.03,rot=rot)
    else:
        for sx in (-1,1): B.box(P(sx*1.5*u,0,2.95*u),(.46*u,.46*u,1.0*u),tm,.03,rot=rot); B.box(P(sx*1.5*u,0,1.8*u),(.43*u,.43*u,.18*u),sk,.03,rot=rot)
    em=M('#F4F06A',.3,emit=1.8) if zombie else M('#1B1B22',.6)
    for sx in (-1,1): B.box(P(sx*.25*u,-.625*u,4.82*u),(.1*u,.012,.13*u),em,0,rot=rot)
TOKC=['#C8372D','#2E6B4F','#E8C547','#5A7FB0','#D9367A','#F4F1EA','#7A4A8A','#E28A3A','#1E3FA0','#3A8A9A','#9A3A5A','#6A8A3A','#B05A3A','#C9A0E0','#5AB0A0','#E8956A','#D8CFB4','#F28AA0','#35975A']
TOKS=['#C58C5E','#B07A50','#D9A273','#9E6A44','#C9925F','#A9744C']
def tok_h(r,x,y,rz,z=0.0,arms=None):
    t=r.choice(TOKC); token(x,y,rz,t,r.choice([t,'#2A2C34','#3A4A6A','#8A7A5A','#F4F1EA']),r.choice(TOKS),r.choice(['#15110E','#2A1E16','#3A2A1E']),h=r.uniform(.86,1.05),z=z,arms=arms)
def tok_z(r,x,y,rz,z=0.0):
    token(x,y,rz,r.choice(['#C9D6E8','#8A6A4A','#5A7FB0','#C8372D','#7448C2','#D8CFB4','#2A2C34','#E28A3A','#1E8A4A','#F1F3F6','#D8A0B8','#B8B0A0']),r.choice(['#3A3D47','#2A2C34','#3A4258','#6A5A40','#27365A']),
          r.choice(ZS),r.choice(['#22301E','#2A2A34','#3A4A3A']),h=r.uniform(.9,1.1),zombie=True,z=z)
# ---------------------------------------------------------------- vehicles
ARTC=['#E8554D','#F2C14E','#4D8FE8','#E87AB8','#F4F1EA','#35975A','#FF8A3A','#9B6FD0','#2BC0B0']
def w11(loc,rz,seed=0,col='#2B58C9',accent='#F2C14E'):
    """Karachi W-11 minibus with truck art, open windows and a hollow interior (floor z0). Faces local +x, door on the left (+y) rear."""
    r=random.Random(seed); root=empty(loc,rot=(0,0,R(rz))); body=M(col,.4,metal=.2,spec=.6); ac=M(accent,.45); ch=M('#C9CED8',.25,metal=.9); gl=M('#1A2433',.06,spec=1.0); dk=M('#22242B',.6)
    Lh=5.2; Wd=1.65; z0=.85; zs=2.3; zt=3.3; z1=3.55; W=[]
    obox((0,0,z0-.14),(Lh,Wd,.14),dk,.04,root); obox((0,0,z1+.09),(Lh+.05,Wd+.05,.1),ac,.08,root)
    DX0,DX1=-3.9,-2.3   # door gap (left side)
    wins={-1:[],1:[]}
    for sy in (-1,1):
        segs=[(-Lh,DX0),(DX1,Lh-1.5)] if sy==1 else [(-Lh,Lh-1.5)]
        for xa,xb in segs:
            obox(((xa+xb)/2,sy*Wd,(z0+zs)/2-.07),((xb-xa)/2,.07,(zs-z0)/2+.07),body,.03,root)
            obox(((xa+xb)/2,sy*(Wd+.075),zs-.12),((xb-xa)/2,.012,.05),ch,.0,root)
            # truck-art band: diamonds / discs / stripes
            n=max(1,int((xb-xa)/.62))
            for k in range(n):
                x=xa+(k+.5)*(xb-xa)/n; c=M(r.choice(ARTC),.5,emit=.12)
                if k%3==0: obox((x,sy*(Wd+.078),1.55),(.2,.012,.2),c,.0,root,rot=(0,R(45),0))
                elif k%3==1: ocyl((x,sy*(Wd+.078),1.55),.2,.02,c,root,seg=12); ocyl((x,sy*(Wd+.086),1.55),.09,.02,M(r.choice(ARTC),.5,emit=.12),root,seg=10)
                else: obox((x,sy*(Wd+.078),1.55),(.07,.012,.26),c,.0,root); obox((x,sy*(Wd+.078),1.55),(.24,.012,.06),c,.0,root)
                obox((x,sy*(Wd+.076),1.08),(.26,.012,.1),M(r.choice(ARTC),.5,emit=.1),.0,root)
                obox((x,sy*(Wd+.03),z0-.36),(.03,.03,.1),ch,.0,root)     # hanging chains / bells
            obox(((xa+xb)/2,sy*(Wd+.03),z0-.27),((xb-xa)/2,.02,.02),ch,0,root)
        obox((-.75,sy*Wd,(zt+z1)/2),(Lh-.75,.07,(z1-zt)/2),body,.02,root); obox((-.75,sy*(Wd+.075),zt+.02),(Lh-.75,.012,.04),ac,0,root)
        xs=[-Lh+.1,-3.9,-2.3,-.7,.9,2.5,Lh-1.5]
        for i,xp in enumerate(xs): obox((xp,sy*Wd,(zs+zt)/2),(.09,.07,(zt-zs)/2),body,.02,root)
        for i in range(len(xs)-1):
            if sy==1 and i==1: continue
            wins[sy].append(((xs[i]+xs[i+1])/2,sy*Wd,(zs+zt)/2))
        for k in range(22): oico((-Lh+.3+k*.45,sy*(Wd+.08),zt+.15),.05,lit(r.choice(['#FF4F7A','#FFD23F','#35C8FF','#7CFC9A']),2.2,always=True),root,sub=1)
    # door frame + grab rail + step
    obox((DX0+.03,Wd,(z0+z1)/2),(.05,.08,(z1-z0)/2),ac,.01,root); obox((DX1-.03,Wd,(z0+z1)/2),(.05,.08,(z1-z0)/2),ac,.01,root)
    ocyl((DX0+.22,Wd+.12,2.1),.03,1.7,ch,root,rot=(0,0,0),seg=8); obox(((DX0+DX1)/2,Wd+.22,z0-.38),((DX1-DX0)/2-.05,.2,.05),dk,.02,root)
    # cab
    cx=Lh-.75
    obox((cx,0,(z0+zs)/2-.07),(.75,Wd,(zs-z0)/2+.07),body,.1,root); obox((Lh+.02,0,1.2),(.06,Wd-.15,.3),ch,.03,root)
    obox((Lh-.04,0,(zs+zt)/2+.02),(.04,Wd-.14,(zt-zs)/2+.04),gl,.02,root); obox((Lh-.03,0,(zs+zt)/2),(.05,.04,(zt-zs)/2+.04),ch,0,root)
    for sy in (-1,1):
        obox((cx+.1,sy*Wd,(zs+zt)/2),(.5,.04,(zt-zs)/2),gl,.02,root); obox((Lh-.02,sy*Wd,(zs+zt)/2),(.08,.07,(zt-zs)/2+.1),body,.02,root)
        obox((Lh+.06,sy*(Wd-.42),1.72),(.04,.24,.17),lit('#FFF6D8',3.0,always=True),.04,root); obox((Lh+.05,sy*(Wd-.42),.98),(.04,.2,.08),lit('#FFB23A',1.5,always=True),.02,root)
        obox((-Lh-.06,sy*(Wd-.3),1.5),(.04,.18,.22),lit('#E8301A',2.0,always=True),.03,root)
        obox((Lh+.3,sy*(Wd+.28),2.75),(.03,.14,.2),ch,.02,root); obox((Lh+.14,sy*(Wd+.14),2.75),(.16,.02,.02),dk,0,root)
        for k in range(3): obox((Lh+.3,sy*(Wd+.28),2.45-k*.14),(.012,.012,.07),M(ARTC[(k+seed)%len(ARTC)],.6),0,root)   # ribbons under mirrors
    obox((Lh+.08,0,.72),(.08,Wd+.02,.14),ch,.04,root); obox((-Lh-.08,0,.72),(.08,Wd+.02,.12),ch,.04,root)
    # crown board over the windshield
    obox((Lh-.25,0,z1+.55),(.08,Wd-.1,.42),M('#C8372D',.5),.05,root); obox((Lh-.16,0,z1+.55),(.02,Wd-.3,.3),ac,.02,root)
    text('W-11',(Lh-.13,0,z1+.55),(1,0,0),.44,M('#16171C',.5),ex=.01,parent=root)
    for k in range(7): oico((Lh-.2,-1.2+k*.4,z1+1.03),.07,lit(ARTC[k%len(ARTC)],2.5,always=True),root,sub=1)
    # back wall, rear window, ladder, plate
    obox((-Lh,0,(z0+zs)/2-.07),(.07,Wd,(zs-z0)/2+.07),body,.03,root); obox((-Lh,0,(zt+z1)/2),(.07,Wd,(z1-zt)/2),body,.02,root)
    for sy in (-1,1): obox((-Lh,sy*(Wd-.12),(zs+zt)/2),(.07,.12,(zt-zs)/2),body,.02,root)
    for sy in (-.55,-.15): ocyl((-Lh-.14,sy+1.2,2.3),.025,2.6,ch,root,rot=(0,0,0),seg=6)
    for k in range(7): obox((-Lh-.14,.85,1.2+k*.36),(.02,.2,.02),ch,0,root)
    obox((-Lh-.08,-.5,1.75),(.02,.62,.22),M('#F4F1EA',.5),.01,root); text('KHI 0011',(-Lh-.105,-.5,1.75),(-1,0,0),.2,M('#16171C',.5),ex=.005,parent=root)
    for k in range(5): obox((-Lh-.08,-1.3+k*.42,1.2),(.02,.16,.16),M(ARTC[(k*2+seed)%len(ARTC)],.5,emit=.12),0,root,rot=(R(45),0,0))
    # roof rack + luggage
    for sy in (-1,1): obox((-.6,sy*(Wd-.12),z1+.42),(Lh-1.1,.03,.03),ch,0,root)
    for k in range(8): obox((-Lh+.6+k*1.15,0,z1+.3),(.03,Wd-.12,.03),ch,0,root); obox((-Lh+.6+k*1.15,(Wd-.12),z1+.31),(.03,.03,.12),ch,0,root); obox((-Lh+.6+k*1.15,-(Wd-.12),z1+.31),(.03,.03,.12),ch,0,root)
    # interior: side benches, ceiling rail
    ocyl((-.6,0,z1-.25),.03,2*(Lh-1.6),ch,root,rot=(0,R(90),0),seg=8)
    obox((cx-.35,-.75,z0+.75),(.06,.5,.75),M('#3A2A22',.7),.04,root); obox((cx-.05,-.75,z0+.5),(.3,.45,.1),M('#3A2A22',.7),.05,root)   # driver seat
    ocyl((cx+.45,-.75,z0+1.25),.34,.05,dk,root,rot=(0,R(62),0),seg=18)
    for sx in (-3.3,3.5):
        for sy in (-1,1): W.append(wheel((sx,sy*(Wd-.22),.62),.62,.44,root))
    return dict(root=root,wheels=W,r=.62,z0=z0,L=Lh,W=Wd,roof=z1+.2,door=((DX0+DX1)/2,Wd),wins=wins,cab=(cx-.05,-.75))
def tanker(loc,rz,col='#F2C14E',tcol='#2B6FB8'):
    root=empty(loc,rot=(0,0,R(rz))); body=M(col,.4,metal=.2,spec=.6); tk=M(tcol,.35,metal=.3,spec=.7); ch=M('#C9CED8',.25,metal=.9); dk=M('#22242B',.6); gl=M('#1A2433',.06,spec=1.0); W=[]
    obox((0,0,.95),(4.9,1.3,.14),dk,.04,root); obox((3.9,0,2.2),(1.0,1.5,1.15),body,.14,root); obox((4.86,0,2.75),(.06,1.3,.45),gl,.03,root)
    for sy in (-1,1): obox((3.9,sy*1.5,2.75),(.6,.04,.42),gl,.03,root); obox((4.93,sy*1.0,1.5),(.04,.24,.17),lit('#FFF6D8',3.0,always=True),.04,root)
    obox((4.95,0,1.1),(.08,1.5,.16),ch,.04,root); obox((4.6,0,3.55),(.3,1.3,.2),M('#C8372D',.5),.06,root)
    ocyl((-.9,0,2.5),1.42,7.0,tk,root,rot=(0,R(90),0),seg=28)
    for x in (-4.3,-2.6,-.9,.8,2.5): ocyl((x,0,2.5),1.45,.14,ch,root,rot=(0,R(90),0),seg=28)
    ocyl((-.9,0,3.98),.42,.2,ch,root,rot=(0,0,0),seg=16); obox((-.9,0,2.5),(2.4,1.43,.3),M('#F4F1EA',.45),.0,root)
    for sy,n in ((-1,(0,-1,0)),(1,(0,1,0))): text('PAANI',(-.9,sy*1.445,2.5),n,.48,M('#16171C',.5),ex=.008,parent=root)
    obox((-4.5,0,1.5),(.1,.5,.3),ch,.03,root)
    for sx in (3.6,-2.2,-3.6):
        for sy in (-1,1): W.append(wheel((sx,sy*1.15,.62),.62,.44,root))
    return dict(root=root,wheels=W,r=.62)
def kcar(loc,rz,col,seed=0):
    c=car(loc,rz,col,seed); c['root'].scale=(VS,)*3; c['r']=.36*VS; return c
def krick(loc,rz,col='#2E8A3A',seed=0,slogan=None):
    """Karachi auto-rickshaw sized for the avatars, with a real cabin: driver seat (.55,0,.84), passenger bench (-1.35,0,.80). faces +x"""
    r=random.Random(seed); root=empty(loc,rot=(0,0,R(rz))); body=M(col,.4,metal=.2,spec=.6); blk=M('#16171C',.6); ch=M('#C9CED8',.25,metal=.9); yl=M('#F2C14E',.5); W=[]
    obox((.1,0,.45),(2.15,1.05,.06),blk,.03,root)
    obox((-2.08,0,1.1),(.06,1.05,.66),body,.04,root)                                        # back wall
    for sy in (-1,1):
        obox((-1.2,sy*1.05,.85),(.9,.05,.4),body,.04,root); obox((-1.2,sy*1.1,.98),(.86,.012,.05),yl,0,root)
        for k in range(4): obox((-1.9+k*.45,sy*1.105,.72),(.09,.012,.09),M(ARTC[(k+seed)%len(ARTC)],.5,emit=.12),0,root,rot=(0,R(45),0))
        for x_,z0_,z1_ in ((1.5,1.2,2.56),(-2.0,1.75,2.56),(-.3,1.25,2.56)): ocyl((x_,sy*1.0,(z0_+z1_)/2),.035,z1_-z0_,ch,root,rot=(0,0,0),seg=6)
    obox((-1.35,0,.72),(.4,.95,.08),M('#7A1F2E',.7,kind='fabric'),.05,root); obox((-1.85,0,1.25),(.1,.95,.5),M('#7A1F2E',.7,kind='fabric'),.06,root)
    obox((.55,0,.78),(.3,.5,.06),M('#3A2A22',.7),.04,root); obox((.18,0,1.2),(.06,.6,.42),M('#3A2A22',.7),.04,root)
    obox((1.9,0,.9),(.35,.55,.42),body,.14,root); obox((2.27,0,1.02),(.03,.2,.14),lit('#FFF6D8',3.0,always=True),.03,root); obox((1.9,0,1.34),(.36,.56,.03),yl,.01,root)
    for sy in (-1,1): ocyl((1.62,sy*.52,1.95),.03,1.25,blk,root,rot=(0,R(-8),0),seg=6)
    o=obox((1.66,0,2.0),(.012,.5,.52),M('#BFE6F2',.06,spec=1.0,alpha=.22),0,root,rot=(0,R(-8),0)); o.name='glass_ws'
    ocyl((1.5,0,1.5),.025,1.1,ch,root,rot=(R(90),0,0),seg=6); ocyl((1.62,0,1.32),.03,.4,blk,root,rot=(0,R(-25),0),seg=6)
    for sy in (-1,1): ocyl((1.5,sy*.52,1.5),.04,.16,blk,root,rot=(R(90),0,0),seg=8)
    obox((1.25,.42,1.5),(.07,.06,.09),M('#F4F1EA',.5),.01,root); obox((1.21,.42,1.5),(.005,.045,.05),lit('#FF4A2A',2.5,always=True),0,root)   # fare meter
    obox((-.25,0,2.62),(2.0,1.12,.07),blk,.06,root); obox((-.25,0,2.56),(2.02,1.14,.03),yl,.01,root)
    for k in range(9):
        for sy in (-1,1): obox((-2.0+k*.45,sy*1.14,2.47),(.035,.01,.06),M(ARTC[(k*2+seed)%len(ARTC)],.6),0,root)
    obox((-2.15,0,1.2),(.012,.8,.3),M('#F4F1EA',.5),.01,root)
    text(slogan or r.choice(['DEKH MAGAR PYAR SE','MAA KI DUA','HORN OK PLEASE']),(-2.165,0,1.2),(-1,0,0),.15,M('#16171C',.5),ex=.004,parent=root)
    for sy in (-1,1): obox((-2.14,sy*.86,.82),(.02,.12,.08),lit('#E8301A',2.0,always=True),.02,root)
    W.append(wheel((1.95,0,.36),.36,.18,root)); W.append(wheel((-1.35,-1.02,.36),.36,.18,root)); W.append(wheel((-1.35,1.02,.36),.36,.18,root))
    return dict(root=root,wheels=W,r=.36)
def kbike(loc,rz,col='#C8372D',rider=None,name='rider'):
    """motorbike x1.4; optional rider (cast dict) seated on it"""
    mb=motorbike(loc,rz,col); mb['root'].scale=(1.4,)*3; mb['r']=.32*1.4
    if rider is not None:
        H=avatar_kz((0,0,0),0,rider,name=name); H['root'].parent=mb['root']; H['root'].location=(-.05,0,.35); H['root'].rotation_euler=(0,0,R(90)); H['root'].scale=(1/1.4,)*3
        sit(H,1,.85,legs=80)
        for s in (1,-1): H['arm'][s].rotation_euler=(R(-75),0,R(s*8))
        mb['rider']=H
    return mb
def roll(V,x,y,rz,dist,z=0.0):
    V['root'].location=(x,y,z); V['root'].rotation_euler[2]=R(rz)
    for w in V['wheels']: w.rotation_euler[1]=dist/V['r']
CARC=['#F4F1EA','#C9CED8','#2A2C34','#C8372D','#2B58C9','#8A8E96','#F2C14E','#1E6A3A','#7A1F2E','#E8E2D0','#5A7FB0','#16171C']
# ---------------------------------------------------------------- buildings
WINL=['#FFD98A','#FFE9B8','#BFE6FF','#FFC870']
def tower(cx,y0,w,d,fl,col,side,seed,sign_=None,scol='#C8372D',style=0,fh=3.5,roofsign=None):
    """modern Karachi block. front face at y0, body extends away from the road (side=+1 north, -1 south)."""
    r=random.Random(seed); s=side; yc=y0+s*d/2; H=4.8+fl*fh; body=M(col,.75,kind='wall'); tr=M(shade(col,.78),.7); dkg=M('#1C2634',.08,spec=1.0); blu=M('#5E9AC8',.08,metal=.3,spec=1.0)
    B.box((cx,yc,H/2),(w/2,d/2,H/2),body,0); B.box((cx,yc,H+.25),(w/2+.15,d/2+.15,.25),tr,0)
    # ground floor shopfront
    B.box((cx,y0-s*.04,2.1),(w/2-.7,.05,1.75),dkg,0)
    for k in range(int(w//2.6)+1): B.box((cx-w/2+.7+k*(w-1.4)/max(1,int(w//2.6)),y0-s*.07,2.1),(.06,.05,1.75),M('#8A8E96',.4,metal=.5),0)
    B.box((cx,y0-s*.3,4.25),(w/2-.2,.3,.12),tr,0)
    if sign_: sign(sign_,(cx,y0-s*.5,4.95),min(.62,(w-2.2)/(len(sign_)*.69)),'#FFFFFF',scol,n=(0,-s,0),e=2.2,pad=.3,frame='#D8DCE2')
    def win():
        q=r.random()
        return lit(r.choice(WINL),r.uniform(1.6,3.2)) if q<.45*min(1,NIGHT[0]*2) else dkg
    for f in range(fl):
        z=4.8+f*fh+fh/2
        if style==0:
            n=max(2,int(w//2.5))
            for k in range(n): B.box((cx-w/2+(k+.5)*w/n,y0-s*.03,z),(w/n/2-.3,.04,fh/2-.6),win(),0)
            B.box((cx,y0-s*.1,z-fh/2+.08),(w/2,.1,.08),tr,0)
        elif style==1:
            B.box((cx,y0-s*.03,z+.1),(w/2-.25,.04,fh/2-.75),blu if NIGHT[0]<.5 else dkg,0)
            n=max(2,int(w//2.0))
            for k in range(n):
                if NIGHT[0]>=.5 and r.random()<.5: B.box((cx-w/2+(k+.5)*w/n,y0-s*.05,z+.1),(w/n/2-.08,.03,fh/2-.8),lit(r.choice(WINL),r.uniform(1.6,3.0)),0)
                B.box((cx-w/2+k*w/n,y0-s*.07,z+.1),(.05,.05,fh/2-.75),M('#D8DCE2',.4,metal=.5),0)
        else:
            B.box((cx,y0-s*.03,z),(w/2-.15,.04,fh/2-.06),blu if NIGHT[0]<.5 else dkg,0); n=max(3,int(w//1.8))
            for k in range(n+1): B.box((cx-w/2+.15+k*(w-.3)/n,y0-s*.07,z),(.04,.04,fh/2),M('#C9CED8',.3,metal=.6),0)
            if NIGHT[0]>=.5:
                for k in range(n):
                    if r.random()<.4: B.box((cx-w/2+.15+(k+.5)*(w-.3)/n,y0-s*.05,z),((w-.3)/n/2-.06,.03,fh/2-.12),lit(r.choice(WINL),r.uniform(1.4,2.8)),0)
        # x-end faces
        m=max(2,int(d//3.2))
        for sx in (-1,1):
            for k in range(m):
                if r.random()<.8: B.box((cx+sx*(w/2+.02),yc-d/2+(k+.5)*d/m,z),(.04,d/m/2-.45,fh/2-.7),win(),0)
        if style==0 and r.random()<.3: B.box((cx+r.uniform(-w/3,w/3),y0-s*.3,z-.7),(.42,.26,.26),M('#D8DCE2',.5),.03)   # AC unit
    if fl>=6 and r.random()<.45:
        bw=r.uniform(3.2,4.6); bh=r.uniform(8,13); bx=cx+r.uniform(-(w/2-bw/2-1),(w/2-bw/2-1)) if w>bw+2.4 else cx; bz=r.uniform(12,H-bh/2-3) if H-bh/2-3>12 else H/2+2
        bc,tc,words=r.choice(WRAPS); B.box((bx,y0-s*.12,bz),(bw/2,.08,bh/2),lit(bc,1.2,.5) if NIGHT[0]>=.5 else M(bc,.55),0); B.box((bx,y0-s*.1,bz),(bw/2+.12,.07,bh/2+.12),M('#F4F1EA',.5),0)
        tm=M(tc,.5,emit=round(1.5*NIGHT[0],3)) if NIGHT[0]>0 else M(tc,.5)
        text(words,(bx,y0-s*.215,bz),(0,-s,0),min(1.5,(bw-.6)/(max(len(q) for q in words.split('\n'))*.69)),tm,ex=.01)
    # roof clutter
    for k in range(r.randint(1,3)): B.cyl((cx+r.uniform(-w/3,w/3),yc+r.uniform(-d/4,d/4),H+1.1),.7,1.6,M(r.choice(['#1A1C22','#2B6FB8','#C9CED8']),.6),seg=14)
    if r.random()<.5: B.cyl((cx+r.uniform(-w/4,w/4),yc,H+3.0),.05,5.5,M('#C8372D',.5),seg=5); B.ico((cx,yc,H+5.8),.12,lit('#FF3A2A',6,always=True),sub=1)
    if roofsign:
        bw=min(w-1.5,len(roofsign[0])*roofsign[3]*.69+1.0)
        for sx in (-1,1): B.cyl((cx+sx*(bw/2-.4),y0+s*1.0,H+1.4),.1,2.4,M('#3A3D44',.5),seg=6)
        sign(roofsign[0],(cx,y0+s*.8,H+2.6+roofsign[3]*.3),roofsign[3],roofsign[2],roofsign[1],n=(0,-s,0),e=2.6,pad=.5,frame='#2A2C34')
    return H
def billboard(x,y,text_,bg,col,size=.7,z=8.5,n=(0,-1,0),poles=2,e=2.8):
    hw=len(text_)*size*.345+.5
    nv=Vector((n[0],n[1],0)).normalized(); t_=Vector((-nv.y,nv.x,0))
    for k in range(poles):
        p=Vector((x,y,0))-nv*.25+(t_*(hw-.6)*(1 if k else -1) if poles>1 else Vector((0,0,0)))
        B.cyl((p.x,p.y,(z-size)/2),.16,z-size,M('#5A5E66',.5,metal=.4),seg=8)
    sign(text_,(x,y,z),size,col,bg,n=n,e=e,pad=.5,th=.2,frame='#2A2C34')
    for k in (-1,0,1): B.box((x+t_.x*k*hw*.6+nv.x*.5,y+t_.y*k*hw*.6+nv.y*.5,z+size*.6+.75),(.1,.1,.06),lit('#FFF3D0',5),0)
def street_lamp(x,y,h=9.0,arms=(1,-1)):
    pm=M('#6E7378',.5,metal=.5); B.cyl((x,y,h/2),.13,h,pm,seg=8,r2=.09)
    for a in arms: B.box((x,y+a*1.3,h-.1),(.06,1.3,.05),pm,0); B.box((x,y+a*2.4,h-.2),(.22,.5,.07),M('#3A3D44',.5),.03); B.box((x,y+a*2.4,h-.28),(.16,.4,.02),lit('#FFE6B0',7.0),0)
def neem(x,y,s=1.0,seed=0):
    r=random.Random(seed); B.cyl((x,y,1.4*s),.2*s,2.8*s,M('#6B4A2E',.85),seg=8); B.box((x,y,.2),(.8,.8,.2),M('#A8A294',.85,kind='concrete',sc=.4),.03)
    for k in range(7): a=k*.9+r.uniform(0,.5); rr=r.uniform(.3,1.0)*s; B.ico((x+math.cos(a)*rr,y+math.sin(a)*rr,(3.2+r.uniform(0,1.3))*s),r.uniform(.9,1.35)*s,M(r.choice(['#3F7A3A','#4F8A3A','#356E34']),.85,kind='leaves'),sub=1)
def bus_stop(x,y,side=1):
    s=side; ch=M('#8A8E96',.4,metal=.6); rf=M('#C8372D',.5)
    for sx in (-2.2,2.2): B.cyl((x+sx,y+s*.9,1.7),.07,3.4,ch,seg=8)
    B.box((x,y+s*.3,3.45),(2.6,1.1,.07),rf,.03,rot=(R(-6*s),0,0)); B.box((x,y+s*.95,1.9),(2.2,.03,1.0),M('#BFE6F2',.1,spec=1,alpha=.28),0)
    B.box((x,y+s*.55,.62),(1.9,.28,.05),M('#2B58C9',.5),.03)
    for sx in (-1.6,1.6): B.box((x+sx,y+s*.55,.3),(.05,.24,.3),ch,.01)
    sign('BUS STOP',(x,y-s*.82,3.72),.34,'#FFFFFF','#2B58C9',n=(0,-s,0),e=1.5,pad=.2)
WRAPS=[('#C8372D','#FFFFFF','LAWN\nSALE'),('#F2C14E','#16171C','CHAI\nTIME'),('#1E6A8A','#FFFFFF','SEA\nVIEW'),('#D9367A','#FFFFFF','EID\nSALE'),('#2E6B4F','#FFE14A','BUN\nKABAB'),('#7448C2','#FFFFFF','5G\nFAST'),('#E2702A','#FFFFFF','MEGA\nSALE')]
FA_SIGNS=['KARACHI BROAST','BUN KABAB KING','MOBILE MALL','CHAI SHAI','SAMOSA POINT','FRESH JUICE BAR','MASTER TAILORS','SEA BREEZE HOTEL','BIRYANI EXPRESS','CRICKET STORE','CITY BANK','PAAN PALACE','KULFI CORNER','BOOK CENTRE']
FA_ROOF=[('CHAI 24/7','#FFE14A','#7A1F2E',1.5),('NO SLEEP SINCE 1947','#FFFFFF','#16213A',1.0),('BIRYANI > EVERYTHING','#FFFFFF','#C8372D',1.0),('HALKA LE BHAI','#16171C','#F2C14E',1.3),('SEA VIEW  >>','#FFFFFF','#1E6A8A',1.3)]
RW=12.4; MEDW=1.4; SWK=4.6; BLN=RW+SWK   # road half width, median half width, sidewalk width, building line
LANES=(3.3,6.9,10.5)
def faisal(mood='golden',night=0.0,seed=5,x0=-100,x1=180,gantry_x=34,bridge_x=86,stop_x=0,shadow=90,gantry_text='SHAHRAH-E-FAISAL',bridge_text='CITY OF LIGHTS',clear=7.0):
    NIGHT[0]=night; r=random.Random(seed); mid=(x0+x1)/2; hl=(x1-x0)/2
    B.box((mid+60,0,-.3),(hl+160,260,.2),M('#8E8A80',.9,kind='concrete',sc=.4),0)
    B.box((mid+60,0,-.05),(hl+160,RW,.05),M('#3C3E44',.8,kind='asphalt'),0)
    wl=M('#E8E6DC',.5); yl=M('#E8B83A',.5)
    for s in (-1,1):
        for ly in (5.1,8.7):
            for k in range(int((x1-x0+200)/7)): B.box((x0+3+k*7,s*ly,.004),(1.5,.08,.004),wl,0)
        B.box((mid+60,s*(MEDW+.3),.004),(hl+160,.08,.004),yl,0); B.box((mid+60,s*(RW-.25),.004),(hl+160,.08,.004),wl,0)
        B.box((mid+60,s*(RW+SWK/2),.09),(hl+160,SWK/2,.09),M('#BDB6A8',.85,kind='tile',sc=1.3,h2='#A9A294'),0)
        for k in range(int((x1-x0)/1.2)): B.box((x0+.6+k*1.2,s*(RW+.08),.1),(.6,.1,.1),M('#E8B83A' if k%2 else '#2A2C34',.6),0)
    # median: kerb, soil, hedges, palms, lamps
    B.box((mid+60,0,.14),(hl+160,MEDW,.14),M('#B8B4A8',.85,kind='concrete',sc=.5),0); B.box((mid,0,.29),(hl,MEDW-.25,.03),M('#6A5238',.9),0)
    for k in range(int((x1-x0)/1.2)):
        for s in (-1,1): B.box((x0+.6+k*1.2,s*MEDW,.15),(.6,.07,.15),M('#F4F1EA' if k%2 else '#2A2C34',.6),0)
    x=x0+4; i=0
    while x<x1:
        if i%4==0: palm(x,0,1.2,seed=i)
        elif i%4==2: street_lamp(x,0)
        else: B.box((x,0,.62),(1.9,.6,.34),M(r.choice(['#3F7A3A','#4A8A40']),.85,kind='leaves'),.14); B.ico((x+r.uniform(-1,1),r.uniform(-.2,.2),1.02),.2,M(r.choice(['#E8554D','#F2C14E','#E87AB8']),.7),sub=1)
        x+=6; i+=1
    # buildings both sides
    cols=['#E8E2D6','#C9D6E0','#D9C4A8','#B8C4CC','#E0B8A0','#A8BCC8','#F0E6D2','#C8B8A0','#9FB4C4','#D8CCB8']; acc=['#E8554D','#F2C14E','#2B8A7A','#D9367A','#E28A3A','#5A7FB0']
    si=0; ri=0
    for s in (1,-1):
        x=x0; i=0
        while x<x1+10:
            w=r.uniform(11,18); low=r.random()<.38; fl=r.randint(2,4) if low else r.randint(7,19); sb=r.uniform(0,2.0)
            rs=None
            if low and ri<40 and r.random()<.75: rs=FA_ROOF[ri%len(FA_ROOF)]; ri+=1
            tower(x+w/2,s*(BLN+sb),w,r.uniform(12,18),fl,r.choice(acc) if (low and r.random()<.5) else r.choice(cols),s,seed*100+si,sign_=FA_SIGNS[si%len(FA_SIGNS)],scol=r.choice(['#C8372D','#1E6A3A','#2B58C9','#7A1F2E','#16171C','#D9811A']),
                  style=0 if low else r.randint(0,2),roofsign=rs)
            x+=w+r.uniform(.4,1.4); i+=1; si+=1
        # far row: simple tall silhouettes
        x=x0-40
        while x<x1+220:
            w=r.uniform(14,26); h=r.uniform(40,110); y=s*(BLN+r.uniform(32,70)); c=r.choice(cols)
            B.box((x+w/2,y,h/2),(w/2,9,h/2),M(shade(c,.92),.8),0)
            for f in range(int(h//7)):
                B.box((x+w/2,y-s*9.02,5+f*7),(w/2-.6,.04,1.6),lit(r.choice(WINL),1.6) if (NIGHT[0]>=.5 and r.random()<.6) else M('#2A3444',.2,spec=.9),0)
            x+=w+r.uniform(2,10)
    # beyond x1: simple blocks lining the road into the haze
    for s in (1,-1):
        x=x1+12
        while x<x1+210:
            w=r.uniform(12,20); h=r.uniform(14,70); c=r.choice(cols); B.box((x+w/2,s*(BLN+8),h/2),(w/2,8,h/2),M(c,.8),0)
            for f in range(int(h//3.5)): B.box((x+w/2,s*BLN-s*.02,6.5+f*3.5),(w/2-.5,.04,1.0),lit(r.choice(WINL),1.6) if (NIGHT[0]>=.5 and r.random()<.5) else M('#2A3444',.2,spec=.9),0)
            x+=w+1
    # sidewalk dressing: trees, lamps, benches, bins, stalls
    for s in (1,-1):
        x=x0+6; i=0
        while x<x1:
            if abs(x-stop_x)>clear or s<0:
                if i%3==0: neem(x,s*(RW+1.1),1.0,seed=i*3+s)
                elif i%3==1: street_lamp(x,s*(RW+.7),7.5,arms=(-s,))
                else: B.cyl((x,s*(RW+.8),.5),.3,1.0,M('#2E6B4F',.5),seg=10); B.cyl((x,s*(RW+.8),1.02),.33,.06,M('#1E4A36',.5),seg=10)
            x+=8; i+=1
    bus_stop(stop_x,RW+1.2,1)
    # gantry sign over the north carriageway (faces -x: read by traffic going +x)
    gm=M('#8A8E96',.4,metal=.6)
    for y in (MEDW-.4,RW+.6): B.cyl((gantry_x,y,4.3),.2,8.6,gm,seg=10)
    for z in (7.3,8.6): B.box((gantry_x,(MEDW+RW)/2+.1,z),(.1,(RW-MEDW)/2+.6,.1),gm,0)
    for k in range(8): B.box((gantry_x,MEDW+.3+k*1.5,7.95),(.06,.06,.65),gm,0,rot=(R(30 if k%2 else -30),0,0))
    sign(gantry_text,(gantry_x-.25,(MEDW+RW)/2+.1,7.95),min(.9,11.0/(len(gantry_text)*.69)),'#FFFFFF','#1E7A4A',n=(-1,0,0),e=1.6,pad=.45,th=.14,frame='#F4F1EA')
    # pedestrian bridge
    bm=M('#2B6FB8',.45,metal=.3); x=bridge_x
    B.box((x,0,6.6),(1.5,RW+2.6,.14),M('#8A8E96',.6),0)
    for sx in (-1,1):
        B.box((x+sx*1.5,0,7.75),(.07,RW+2.6,.07),bm,0); B.box((x+sx*1.5,0,6.9),(.05,RW+2.6,.2),bm,0)
        for k in range(int((RW+2.6)*2/1.4)+1): B.box((x+sx*1.5,-(RW+2.6)+k*1.4,7.2),(.04,.04,.55),bm,0)
    for y in (-(RW+2.2),-.0,(RW+2.2)):
        for sx in (-1,1): B.cyl((x+sx*1.2,y,3.3),.22,6.6,M('#8A8E96',.5),seg=10)
    for s in (1,-1):
        for k in range(14): B.box((x+2.0+k*.62,s*(RW+2.6),6.5-k*.47),(.34,1.2,.08),M('#8A8E96',.6),0)
        B.box((x+6.0,s*(RW+3.75),4.2),(4.4,.05,.06),bm,0,rot=(0,R(37),0)); B.box((x+6.0,s*(RW+1.45),4.2),(4.4,.05,.06),bm,0,rot=(0,R(37),0))
    sign(bridge_text,(x-1.6,-6.9,7.15),.6,'#FFFFFF','#C8372D',n=(-1,0,0),e=1.8,pad=.35,th=.1)
    B.done('faisal')
    S=setup_world(mood,shadow); return S
