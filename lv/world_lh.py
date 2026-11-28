# Sets for "In This World, Everyone Is Lahori": bazaar street (+dhaba, chai stall, traffic light, skyline), vehicles,
# saucer, Mars food street (same kit, Mars palette) and space. Street runs along X; road y in [-4,4]; north shops face -y at y=7.
TXT=[]
def sign_text(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None):
    o=text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=.02,parent=parent); TXT.append(o); return o

def facade(cx,w,floors,col,sign,scol,seed,side=1,Y=7.0,trim='#F4EBDA',shop=True,mars=False):
    r=random.Random(seed); s=side; FH=3.0; H=3.4+floors*FH
    wall=M(col,.85,kind='wall'); tr=M(trim,.7); dk=M('#141820',.4); glass=M('#1E2A3C',.12,spec=.8)
    wood=M(r.choice(['#6E4A2E','#7A5236','#5E3A22','#2F6E6A']),.6,kind='wood',sc=.6)
    yf=Y*s; yb=(Y+4.0)*s; yc=(yf+yb)/2
    if shop: B.box((cx,yc,H/2),(w/2,2.0,H/2),wall,0)
    else:
        B.box((cx,yc,(H+3.4)/2),(w/2,2.0,(H-3.4)/2),wall,0); B.box((cx,yb-.15*s,1.7),(w/2,.15,1.7),wall,0)
        for xx in (cx-w/2+.15,cx+w/2-.15): B.box((xx,yc,1.7),(.15,2.0,1.7),wall,0)
        B.box((cx,yc,.02),(w/2-.3,1.9,.03),M('#6E5A48',.7,kind='tile',h2='#5A4838',sc=2.0),0)
    B.box((cx,yf-.06*s,H+.12),(w/2+.06,.12,.12),tr,.02); B.box((cx,yf-.03*s,3.4),(w/2+.02,.08,.08),tr,.01)
    for k in range(int(w//1.2)+1): B.box((cx-w/2+.3+k*1.2,yf-.06*s,H+.36),(.12,.06,.14),tr,.01)
    # ground floor shop
    if shop:
        B.box((cx,yf+.02*s,1.55),(w/2-.35,.03,1.45),M('#1A1612',.8),0)
        B.box((cx,yf+1.2*s,1.4),(w/2-.4,.05,1.3),M(shade(col,.45),.8),0)
        for k in range(3):
            zz=.55+k*.75; B.box((cx,yf+.9*s,zz),(w/2-.5,.3,.03),wood,.005)
            for j in range(int((w-1)/.42)):
                B.box((cx-w/2+.7+j*.42,yf+.85*s,zz+.17),(.15,.12,.15),M(r.choice(['#E8554D','#F2C14E','#4D8FE8','#6FC38A','#F4F1DE','#C9772B','#9B6FD0']),.6),.01)
        for xx in (cx-w/2+.2,cx+w/2-.2): B.box((xx,yf,1.6),(.2,.12,1.6),wall,.02)
        B.box((cx,yf-.02*s,3.05),(w/2-.35,.1,.25),M('#8A8E96',.5,metal=.5),.03)
        n=10
        for k in range(n): B.box((cx-w/2+.4+(k+.5)*(w-.8)/n,yf-.55*s,3.0),((w-.8)/n/2,.6,.025),M(scol if k%2 else '#F4F1EA',.85,kind='fabric'),.005,rot=(R(-18*s),0,0))
        B.box((cx,yf-.12*s,3.72),(w/2-.6,.06,.36),M(scol,.6),.03); B.box((cx,yf-.17*s,3.72),(w/2-.75,.02,.3),M('#FFF8E8',.6),0)
        sign_text(sign,(cx,yf-.2*s,3.69),.34 if len(sign)<14 else .27,shade(scol,.65),(0,-s,0))
    # upper floors
    for f in range(floors):
        zb=3.4+f*FH; nwin=max(1,int(w//2.1))
        for k in range(nwin):
            wx=cx-w/2+(k+.5)*w/nwin; wz=zb+1.55; kind=r.random()
            B.box((wx,yf-.01*s,wz),(.5,.03,.72),glass,0)
            B.box((wx,yf-.05*s,wz+.76),(.6,.07,.06),tr,.01); B.box((wx,yf-.05*s,wz-.76),(.62,.1,.06),tr,.01)
            for sx in (-1,1): B.box((wx+sx*.53,yf-.05*s,wz),(.04,.05,.74),tr,.005)
            if kind<.35:   # wooden shutters half open
                for sx in (-1,1): B.box((wx+sx*.82,yf-.1*s,wz),(.27,.03,.7),wood,.01,rot=(0,0,R(sx*-35*s)))
            elif kind<.6:  # balcony with railing
                B.box((wx,yf-.55*s,zb+.68),(.95,.55,.06),tr,.02)
                for j in range(9): B.box((wx-.88+j*.22,yf-1.06*s,zb+.98),(.02,.02,.28),M('#2A2C34',.4,metal=.6),0)
                B.box((wx,yf-1.06*s,zb+1.26),(.95,.025,.025),M('#2A2C34',.4,metal=.6),0)
                if r.random()<.6: B.cyl((wx+.6,yf-.7*s,zb+.85),.12,.24,M('#B5542E',.7),seg=10); B.ico((wx+.6,yf-.7*s,zb+1.07),.18,M('#3F8A3A',.8),sub=1)
                if r.random()<.5:
                    for j in range(4): B.box((wx-.6+j*.38,yf-.9*s,zb+2.15),(.14,.01,.22),M(r.choice(['#E8554D','#F2C14E','#4D8FE8','#F4F1DE','#9B6FD0']),.9),0)
                    B.cyl((wx,yf-.9*s,zb+2.38),.008,1.9,dk,rot=(0,R(90),0),seg=5)
            elif kind<.78: # jharoka (projecting carved window box)
                B.box((wx,yf-.35*s,wz),(.7,.35,.85),M(shade(col,.9),.8),.04); B.box((wx,yf-.71*s,wz),(.5,.02,.62),glass,0)
                B.box((wx,yf-.4*s,wz+.98),(.8,.42,.12),tr,.06); B.box((wx,yf-.4*s,wz-.95),(.75,.4,.1),tr,.05)
                for j in range(3): B.box((wx-.35+j*.35,yf-.72*s,wz),(.02,.02,.62),wood,0)
            else:          # AC unit
                B.box((wx+.4,yf-.25*s,wz-1.0),(.38,.22,.22),M('#D8DCE2',.5),.03); B.cyl((wx+.4,yf-.48*s,wz-1.0),.15,.02,M('#5A5E66',.5),rot=(R(90),0,0),seg=12)
        if r.random()<.5: B.box((cx+r.uniform(-w/3,w/3),yf-.04*s,zb+.3),(r.uniform(.6,1.2),.03,.18),M(r.choice(['#E8554D','#2B58C9','#35975A']),.6),.01)
    # roof: water tanks, dish, rods
    for k in range(r.randint(1,2)): B.cyl((cx+r.uniform(-w/3,w/3),yc+r.uniform(-1,1),H+.6),.45,1.0,M('#1A1C22' if not mars else '#C9CED8',.6),seg=14)
    if r.random()<.5: B.cyl((cx+r.uniform(-w/3,w/3),yc,H+.5),.02,1.0,dk,seg=5); B.cyl((cx,yc,H+1.0),.3,.06,M('#D8DCE2',.4),rot=(R(55),0,0),seg=14)
    return H

def mosque(x,y,s=1.0,col='#B8634A',dome='#F2EEE6'):
    sm=M(col,.85,kind='wall'); dm=M(dome,.5); gold=M('#D9B24A',.3,metal=.8)
    B.box((x,y,4*s),(16*s,5*s,4*s),sm,0)
    for k in range(-1,2):
        B.box((x+k*7*s,y-5.1*s,3.4*s),(1.6*s,.1,2.6*s),M('#3A2A22',.8),0); B.ico((x+k*7*s,y,10*s if k==0 else 8.4*s),(4.6 if k==0 else 3.1)*s,dm,sc=(1,1,1.12),sub=3)
        B.cyl((x+k*7*s,y,(13.9 if k==0 else 11.4)*s),.12*s,1.4*s,gold,seg=8)
    for sx in (-1,1):
        for sy in (-1,1):
            mx,my=x+sx*16*s,y+sy*5*s; B.cyl((mx,my,9*s),1.0*s,18*s,sm,seg=8,r2=.8*s); B.cyl((mx,my,15*s),1.3*s,.5*s,M('#F2EEE6',.6),seg=8)
            B.cyl((mx,my,18.3*s),.95*s,1.4*s,M('#F2EEE6',.6),seg=8); B.ico((mx,my,19.4*s),1.0*s,dm,sub=2)

def wires(x0,x1,y0,y1,z,n,seed):
    r=random.Random(seed); dk=M('#121318',.6)
    for i in range(n):
        x=r.uniform(x0,x1); za=z+r.uniform(-.6,.8); zb=z+r.uniform(-.6,.8); sag=r.uniform(.3,.9); pts=8; dx=r.uniform(-3,3)
        for j in range(pts):
            a=j/pts; b=(j+1)/pts; pa=(x+dx*a,L(y0,y1,a),L(za,zb,a)-sag*4*a*(1-a)); pb=(x+dx*b,L(y0,y1,b),L(za,zb,b)-sag*4*b*(1-b))
            d=Vector(pb)-Vector(pa); B.cyl(tuple((Vector(pa)+Vector(pb))/2),.012,d.length,dk,rot=d.to_track_quat('Z','Y').to_euler(),seg=4)

def pole(x,y,h=8.5):
    pm=M('#7A7E86',.6,kind='concrete',sc=.3); B.cyl((x,y,h/2),.13,h,pm,seg=8,r2=.09)
    B.box((x,y,h-.6),(.9,.05,.05),M('#3A3D44',.5),0); B.box((x+.3,y+.25,h-1.6),(.3,.25,.4),M('#6E7378',.5,metal=.4),.03)

def traffic_light(x,y,rot=0):
    pm=M('#2A2C34',.4,metal=.5); root=empty((x,y,0),rot=(0,0,R(rot)))
    obox((0,0,2.3),(.07,.07,2.3),pm,.01,root); obox((0,-.15,4.7),(.28,.2,.78),M('#1B1D24',.4),.05,root)
    cols=[('#FF2A1A','#3A0A08'),('#FFB21A','#3A2A08'),('#2AE85A','#0A3A14')]; L_=[]
    for i,(on,off) in enumerate(cols):
        z=5.22-i*.5; obox((0,-.36,z+.16),(.2,.12,.03),pm,.01,root)
        a=ocyl((0,-.36,z),.17,.04,M(on,.3,emit=9.0),root,seg=20); b=ocyl((0,-.355,z),.17,.04,M(off,.4),root,seg=20); L_.append((a,b))
    return dict(root=root,lamps=L_)
def tl_set(T,state):
    for i,(a,b) in enumerate(T['lamps']):
        on=(i==state); a.scale=(1,1,1) if on else (0,0,0); b.scale=(0,0,0) if on else (1,1,1)

def wheel(loc,r,w,parent,mat=None):
    e=empty(loc,parent); ocyl((0,0,0),r,w,mat or M('#141418',.8),e,rot=(R(90),0,0),seg=18); ocyl((0,0,0),r*.55,w*1.04,M('#C9CED8',.3,metal=.8),e,rot=(R(90),0,0),seg=12)
    obox((0,0,0),(r*.5,w*.53,.02),M('#5A5E66',.5),0,e); return e
def car(loc,rotz,col,seed=0):
    r=random.Random(seed); root=empty(loc,rot=(0,0,R(rotz))); body=M(col,.3,metal=.3,spec=.6); gl=M('#1A2433',.06,spec=1.0); W=[]
    obox((0,0,.62),(2.05,.86,.33),body,.16,root); obox((-.18,0,1.16),(1.18,.78,.3),body,.2,root)
    obox((-.18,0,1.18),(1.2,.79,.24),gl,.12,root); obox((.92,0,1.15),(.06,.72,.22),gl,.05,root,rot=(0,R(-30),0)); obox((-1.3,0,1.15),(.06,.72,.22),gl,.05,root,rot=(0,R(28),0))
    for sy in (-1,1):
        obox((2.04,sy*.6,.72),(.03,.16,.07),M('#FFF6D8',.2,emit=2.5),.02,root); obox((-2.04,sy*.62,.74),(.03,.14,.06),M('#E8301A',.3,emit=2.0),.02,root)
    obox((2.06,0,.5),(.04,.7,.08),M('#C9CED8',.3,metal=.8),.02,root); obox((-2.06,0,.5),(.04,.7,.08),M('#C9CED8',.3,metal=.8),.02,root)
    for sx in (-1.3,1.3):
        for sy in (-.84,.84): W.append(wheel((sx,sy,.36),.36,.24,root))
    if r.random()<.35: obox((-.18,0,1.52),(.8,.6,.06),M('#2A2C34',.5),.02,root); obox((-.18,0,1.66),(.7,.5,.12),M(r.choice(['#E8554D','#4D8FE8','#F2C14E']),.8,kind='fabric'),.05,root)
    return dict(root=root,wheels=W,r=.36)
def rickshaw(loc,rotz,col='#2E8A3A',seed=0):
    root=empty(loc,rot=(0,0,R(rotz))); body=M(col,.4,metal=.2); blk=M('#16171C',.6); W=[]
    obox((-.35,0,.72),(.75,.68,.32),body,.12,root); obox((.6,0,.6),(.28,.3,.22),body,.1,root); obox((.92,0,.85),(.05,.42,.42),M('#1A2433',.08,spec=1),.04,root,rot=(0,R(-14),0))
    obox((-.1,0,1.62),(1.15,.72,.06),blk,.05,root); obox((-.1,0,1.5),(1.15,.73,.08),M('#F2C14E',.6),.03,root)
    for sx in (-1.2,.75):
        for sy in (-.68,.68): obox((sx,sy,1.2),(.03,.03,.42),M('#C9CED8',.3,metal=.8),.0,root)
    obox((-.75,0,1.05),(.3,.62,.12),M('#7A1F2E',.7,kind='fabric'),.05,root); obox((.35,0,.98),(.2,.2,.05),M('#2A2C34',.5),.02,root)
    for i,c in enumerate(['#E8554D','#F2C14E','#4D8FE8','#6FC38A']): obox((-1.1+i*.05,.69,.55+i*.1),(.04,.01,.04),M(c,.5,emit=.8),0,root)
    obox((-1.12,0,.9),(.03,.5,.18),M('#F4F1DE',.5),.01,root)
    W.append(wheel((.9,0,.28),.28,.16,root)); W.append(wheel((-.75,-.62,.28),.28,.16,root)); W.append(wheel((-.75,.62,.28),.28,.16,root))
    return dict(root=root,wheels=W,r=.28)
def motorbike(loc,rotz,col='#C8372D'):
    root=empty(loc,rot=(0,0,R(rotz))); body=M(col,.35,metal=.3); ch=M('#C9CED8',.3,metal=.85); W=[]
    obox((.05,0,.62),(.5,.13,.14),body,.07,root); obox((-.32,0,.8),(.38,.15,.06),M('#16171C',.7),.05,root); obox((.55,0,.9),(.06,.06,.32),ch,.02,root,rot=(0,R(-22),0))
    obox((.66,0,1.2),(.04,.36,.03),ch,.01,root); obox((.62,0,1.05),(.06,.1,.08),M('#FFF6D8',.2,emit=2),.02,root)
    obox((-.25,0,.42),(.35,.12,.1),ch,.03,root)
    W.append(wheel((.62,0,.32),.32,.1,root)); W.append(wheel((-.6,0,.32),.32,.1,root))
    return dict(root=root,wheels=W,r=.32)
def drive(V,x,y,rotz,dist):
    V['root'].location=(x,y,0); V['root'].rotation_euler[2]=R(rotz)
    for w in V['wheels']: w.rotation_euler[1]=dist/V['r']

def stall_chai(x,y):
    wd=M('#8A5A36',.6,kind='wood',sc=.6); ch=M('#C9CED8',.3,metal=.85)
    B.box((x,y,.5),(.9,.5,.5),wd,.03); B.box((x,y,1.02),(.95,.55,.03),M('#F4F1DE',.6),.01)
    for sx in (-.85,.85): B.cyl((x+sx,y+.45,1.55),.025,1.1,ch,seg=6)
    B.box((x,y+.1,2.12),(1.05,.7,.04),M('#C8372D',.8,kind='fabric'),.01,rot=(R(8),0,0))
    B.cyl((x-.45,y,1.16),.16,.22,ch,seg=14); B.cyl((x-.45,y,1.3),.1,.08,ch,seg=12)
    for i in range(6): B.cyl((x+.05+i*.12,y-.2,1.09),.035,.1,M('#F4F1EA',.4),seg=8)
    B.cyl((x+.5,y+.15,1.12),.12,.16,M('#3A2A1E',.5),seg=12)
def stall_jalebi(x,y):
    wd=M('#9A6A48',.6,kind='wood',sc=.6)
    B.box((x,y,.5),(.9,.5,.5),wd,.03); B.box((x,y,1.03),(.95,.55,.03),M('#F4F1DE',.6),.01); B.box((x,y+.1,2.12),(1.05,.7,.04),M('#F2C14E',.8,kind='fabric'),.01,rot=(R(8),0,0))
    for sx in (-.85,.85): B.cyl((x+sx,y+.45,1.55),.025,1.1,M('#C9CED8',.3,metal=.85),seg=6)
    for i in range(14): B.ico((x-.6+(i%7)*.2,y-.15+(i//7)*.2,1.1),.08,M('#F2A11A',.35,emit=.3),sc=(1,1,.4),sub=1)
    B.cyl((x+.55,y+.1,1.1),.3,.1,M('#16171C',.4,metal=.5),seg=16)

def karahi_obj(loc,s=1.0,parent=None,food=True):
    e=empty(loc,parent); bm=M('#1A1A1E',.35,metal=.7)
    bm_=bmesh.new(); bmesh.ops.create_uvsphere(bm_,u_segments=24,v_segments=12,radius=.45*s)
    for v in [v for v in bm_.verts if v.co.z>0]: bm_.verts.remove(v)
    me=bpy.data.meshes.new('kh'); bm_.to_mesh(me); bm_.free(); o=bpy.data.objects.new('kh',me); _col.objects.link(o); o.parent=e; o.location=(0,0,.45*s); me.materials.append(bm)
    md=o.modifiers.new('sol','SOLIDIFY'); md.thickness=.03*s
    for p in me.polygons: p.use_smooth=True
    for sx in (-1,1): ocyl((sx*.5*s,0,.42*s),.07*s,.03*s,bm,e,rot=(0,R(90),0),seg=10)
    if food:
        ocyl((0,0,.33*s),.4*s,.04*s,M('#B8461E',.55),e,rot=(0,0,0),seg=24)
        r=random.Random(3)
        for i in range(16): oico((r.uniform(-.28,.28)*s,r.uniform(-.28,.28)*s,.37*s),.06*s,M(r.choice(['#C2552A','#A8401C','#3F8A3A','#F2EEE6']),.5),e,sub=1)
    return e

def dhaba(x0,x1,Y=7.0):
    """open kitchen at the base of a north building + tables on the sidewalk"""
    cx=(x0+x1)/2; w=x1-x0; wd=M('#5E3A22',.6,kind='wood',sc=.6); ch=M('#C9CED8',.3,metal=.85)
    B.box((cx,Y+1.0,.5),(w/2-.5,.45,.5),M('#3A2A22',.6,kind='concrete',sc=.4),.02); B.box((cx,Y+1.0,1.02),(w/2-.45,.5,.03),M('#2A2C34',.4,metal=.6),.01)
    B.box((cx,Y+2.0,1.6),(w/2-.4,.05,1.5),M('#5A3A2A',.8),0)
    for i in range(4): B.cyl((cx-w/3+i*w/4.5,Y+1.95,2.2),.18,.05,ch,rot=(R(90),0,0),seg=14)
    for i in range(5): B.cyl((cx-w/2+1+i*(w-2)/4,Y-.6,2.9),.008,.5,M('#16171C',.5),seg=4); B.ico((cx-w/2+1+i*(w-2)/4,Y-.6,2.62),.09,M('#FFD98A',.2,emit=8),sub=1)
    chairs=[]
    for i in range(3):
        tx=cx-w/2+1.4+i*(w-2.8)/2; ty=Y-2.0
        B.box((tx,ty,.92),(.55,.42,.03),M('#E8E4DA',.5),.01)
        for sx in (-.45,.45):
            for sy in (-.34,.34): B.cyl((tx+sx,ty+sy,.46),.025,.92,ch,seg=6)
        for sy in (-1,1):
            c=(tx,ty+sy*.78); chairs.append((c,0 if sy<0 else 180))
            cm=M(['#C8372D','#2B58C9','#F4F1EA'][i],.5)
            B.box((c[0],c[1],.54),(.24,.24,.025),cm,.02)
            for sx in (-.18,.18):
                for sy2 in (-.2,.2): B.cyl((c[0]+sx,c[1]+sy2,.27),.018,.54,cm,seg=6)
            B.box((c[0],c[1]+sy*.23,.82),(.24,.02,.28),cm,.02)
    return chairs

def tree(x,y,s=1.0,col='#4F8A3A',trunk='#6B4A2E'):
    B.cyl((x,y,1.2*s),.14*s,2.4*s,M(trunk,.8),seg=8)
    for dx,dy,dz,r_ in ((0,0,3.0,1.25),(.6,.3,2.6,.9),(-.55,-.2,2.7,.95),(.1,-.5,3.5,.85)): B.ico((x+dx*s,y+dy*s,dz*s),r_*s,M(col,.85,kind='leaves'),sub=1)
def skyline(seed,mars=False):
    r=random.Random(seed); pal=(['#B8624A','#C98A5A','#A8503A','#D8A070'] if mars else ['#D8C4A0','#C9A27A','#E0C8A8','#B8A890','#D4B48C','#C8B8A8','#E6D6BE'])
    win=M('#2A3444',.3); tops=M('#8A7E70' if not mars else '#7A3A2A',.8)
    def blk(x,y,w,d,h):
        c=r.choice(pal); B.box((x,y,h/2),(w/2,d/2,h/2),M(c,.9,kind='wall'),0); B.box((x,y,h+.15),(w/2+.1,d/2+.1,.15),tops,0)
        for f in range(int(h//3)):
            for k in range(int(w//2.2)):
                if r.random()<.55: B.box((x-w/2+1.1+k*2.2,y-d/2-.02,1.8+f*3),(.45,.03,.6),win,0)
        if r.random()<.4: B.cyl((x+r.uniform(-w/4,w/4),y,h+.7),.4,1.0,M('#1A1C22' if not mars else '#C9CED8',.6),seg=10)
    for y0 in (13,24,36,50):
        x=-130
        while x<150:
            w=r.uniform(6,11); h=r.uniform(6,16)+y0*.15; blk(x+w/2,y0+r.uniform(0,6),w,r.uniform(6,9),h); x+=w+r.uniform(0,1.5)
            if r.random()<.25: tree(x,y0-1.5,r.uniform(.9,1.3),'#4F8A3A' if not mars else '#8A6A9A')
        x=-130
        while x<150:
            w=r.uniform(6,11); h=r.uniform(6,16)+y0*.15; blk(x+w/2,-y0-r.uniform(0,6),w,r.uniform(6,9),h); x+=w+r.uniform(0,1.5)
    for x0 in (74,-74):
        for k in range(6):
            w=r.uniform(7,10); h=r.uniform(8,18); blk(x0+(k*9 if x0>0 else -k*9),r.uniform(-6,6),w,r.uniform(7,10),h)
def bazaar(theme='lahore',seed=1):
    mars=(theme=='mars'); B.objs=[]
    if mars:
        cols=['#C8623A','#D98A4A','#B8503A','#E0A060','#9E4A3A','#CF7A52','#E4B07A']; GR=M('#A8482C',.9,kind='concrete',sc=.4); RD=M('#5A2A22',.7,kind='asphalt'); WALKM=M('#C27A5A',.8,kind='concrete',sc=.5)
    else:
        cols=['#E8B26A','#D96E5A','#5FA8A0','#E8D2A8','#C98ACF','#7FA8D8','#F0C87A','#B8D86A','#E89A6A','#D8C4B0']; GR=M('#9A9484',.9,kind='concrete',sc=.4); RD=M('#3A3C42',.75,kind='asphalt'); WALKM=M('#A8A296',.8,kind='concrete',sc=.5)
    B.box((0,0,-.06),(70,4.2,.05),RD,0)
    for k in range(-14,15): B.box((k*5,0,-.004),(1.1,.08,.004),M('#E8E2C8',.4),0)
    for s_ in (-1,1):
        B.box((0,s_*5.6,0),(70,1.5,.07),WALKM,0)
        for k in range(-70,70): B.box((k*1.0+.5,s_*4.12,.04),(.5,.1,.08),M('#F2C14E' if k%2 else '#1A1A1E',.6),0)
    B.box((0,0,-.3),(200,200,.2),GR,0)
    signs=(['MARS KARAHI 2ND BRANCH','ZERO-G JALEBI','CHAI ON MARS','RED PLANET NASHTA','ORBIT PAAN','CRATER TIKKA','LAHORI FOOD ST'] if mars else
           ['LAHORI CHAI','SHAHI NASHTA','MOBILE ZONE','JALEBI HOUSE','PAAN CORNER','BHAI JAAN TAILORS','FRESH JUICE','KHAN SWEETS','GOL GAPPAY'])
    scols=['#C8372D','#2B58C9','#35975A','#E6A31C','#7448C2','#16909E','#CF3F78']
    r=random.Random(seed); x=-44; i=0
    while x<44:
        w=r.uniform(5.5,8.0)
        if not mars and 13<x+w/2<21:   # dhaba slot
            facade(17,8.0,r.randint(2,3),'#E8C07A','USTAD JAMEEL KARAHI','#1F4D3A',77,1,shop=False); x=21; continue
        facade(x+w/2,w,r.randint(2,4),r.choice(cols),signs[i%len(signs)],r.choice(scols),seed*100+i,1,mars=mars); x+=w; i+=1
    x=-44
    while x<44:
        w=r.uniform(5.5,8.0); facade(x+w/2,w,r.randint(2,4),r.choice(cols),signs[(i+3)%len(signs)],r.choice(scols),seed*100+i+50,-1,mars=mars); x+=w; i+=1
    chairs=[]
    if not mars:
        B.box((17,7.0,1.65),(3.6,.12,.06),M('#1F4D3A',.6),0); chairs=dhaba(13,21)
        B.box((17,6.85,3.75),(3.4,.08,.42),M('#1F4D3A',.6),.03); sign_text('USTAD JAMEEL KARAHI',(17,6.75,3.72),.36,'#F6E7B0',(0,-1,0),e=1.5)
        for k in range(10): B.box((13.4+(k+.5)*.72,6.4,3.02),(.36,.62,.025),M('#1F4D3A' if k%2 else '#F4F1EA',.85,kind='fabric'),.005,rot=(R(-18),0,0))
        stall_chai(-3.5,5.6); stall_jalebi(4.5,5.6); stall_chai(-8,-5.6)
        mosque(118,0,1.35); mosque(12,92,1.4); skyline(seed)
        for tx in (-36,-27,-15,8,26,38): tree(tx,6.4 if tx%2 else -6.4,1.0)
        for px in range(-40,41,10): pole(px,4.4); pole(px+5,-4.4)
        wires(-44,44,4.4,-4.4,8.0,46,seed)
    else:
        skyline(seed,True)
        for i_ in range(5): B.ico((-60+i_*40,70+i_*9,0),12+i_*3,M('#BFE6F2',.05,spec=1.0,alpha=.25),sc=(1,1,.7),sub=3)
        B.ico((120,0,0),16,M('#BFE6F2',.05,spec=1.0,alpha=.25),sc=(1,1,.7),sub=3)
        stall_chai(-3.5,5.6); stall_jalebi(4.5,5.6)
        B.box((17,7.0,1.6),(3.6,.12,1.5),M('#3A2A22',.6),0)
        for px in range(-40,41,10): B.cyl((px,4.4,3),.08,6,M('#C9CED8',.3,metal=.8),seg=8); B.ico((px,4.4,6.1),.25,M('#7AF0FF',.2,emit=6),sub=2)
    B.done('bazaar')
    return dict(chairs=chairs)

# ---------------------------------------------------------------- saucer
def saucer(loc,delivery=False):
    root=empty(loc); hull=M('#8E95A4',.25,metal=.85); dark=M('#2B2F3A',.3,metal=.8); bl=M('#35C8FF',.2,emit=7.0); pur=M('#7A5CFF',.15,spec=.9,emit=.4)
    oico((0,0,0),6.0,hull,root,sc=(1,1,.22),sub=4); oico((0,0,-.25),5.2,dark,root,sc=(1,1,.18),sub=3)
    oico((0,0,1.0),2.4,pur,root,sc=(1,1,.62),sub=3); ocyl((0,0,.95),2.6,.2,dark,root,rot=(0,0,0),seg=40)
    L_=[]
    for i in range(24):
        a=i/24*2*pi; L_.append(oico((5.85*math.cos(a),5.85*math.sin(a),0),.16,bl,root,sub=1))
    ocyl((0,0,-1.3),1.8,.06,M('#BFF4FF',.2,emit=4.0),root,rot=(0,0,0),seg=32)
    for i in range(3):
        a=i/3*2*pi+.5; ocyl((3.2*math.cos(a),3.2*math.sin(a),-1.6),.12,1.6,dark,root,rot=(0,0,0),seg=8); ocyl((3.4*math.cos(a),3.4*math.sin(a),-2.4),.45,.08,dark,root,rot=(0,0,0),seg=14)
    hinge=empty((0,-2.4,-1.25),root); ramp=obox((0,-1.6,0),(1.0,1.6,.06),dark,.03,hinge); obox((0,-1.6,.07),(.6,1.5,.01),bl,0,hinge)
    beam=ocyl((0,0,-6),2.2,9.5,M('#BFF4FF',.4,emit=1.2,alpha=.12),root,rot=(0,0,0),seg=32,r2=1.4); beam.name='glass_beam'
    D=None
    if delivery:
        D=empty((0,0,1.4),root); karahi_obj((0,0,0),5.5,D)
        for k in range(6):
            a=k/6*2*pi; obox((4.4*math.cos(a),4.4*math.sin(a),-.55),(.35,.25,.45),M('#F4F1EA',.7),.04,D); obox((4.4*math.cos(a),4.4*math.sin(a),-.1),(.1,.27,.06),M('#C8372D',.6),.02,D)
        sg=empty((0,-6.2,.6),root); obox((0,0,0),(3.2,.08,.55),M('#C8372D',.5),.06,sg); text('LAHORI DELIVERY',(0,-.1,0),(0,-1,0),.62,M('#FFF6D8',.4,emit=2.0),.02,sg)
    return dict(root=root,lights=L_,hinge=hinge,beam=beam,delivery=D)

# ---------------------------------------------------------------- space
def space(seed=4):
    sc=bpy.context.scene; w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True; nt=w.node_tree; bg=nt.nodes['Background']
    tc=nt.nodes.new('ShaderNodeTexCoord'); vo=nt.nodes.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value=420; nt.links.new(tc.outputs['Generated'],vo.inputs['Vector'])
    rp=nt.nodes.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].position=.0; rp.color_ramp.elements[0].color=(1,1,1,1); rp.color_ramp.elements[1].position=.06; rp.color_ramp.elements[1].color=(0,0,0,1)
    nt.links.new(vo.outputs['Distance'],rp.inputs[0]); nz=nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value=2.0; nt.links.new(tc.outputs['Generated'],nz.inputs['Vector'])
    r2=nt.nodes.new('ShaderNodeValToRGB'); r2.color_ramp.elements[0].color=hexc('#050616'); r2.color_ramp.elements[1].color=hexc('#2A1450'); r2.color_ramp.elements[0].position=.45; nt.links.new(nz.outputs['Fac'],r2.inputs[0])
    ad=nt.nodes.new('ShaderNodeMix'); ad.data_type='RGBA'; ad.blend_type='ADD'; ad.inputs['Factor'].default_value=1.0; nt.links.new(r2.outputs['Color'],ad.inputs[6]); nt.links.new(rp.outputs['Color'],ad.inputs[7])
    nt.links.new(ad.outputs[2],bg.inputs[0]); bg.inputs[1].default_value=1.0
    sc.render.resolution_x=1080; sc.render.resolution_y=1920; sc.render.resolution_percentage=PCT; sc.render.engine='BLENDER_EEVEE'; e=sc.eevee
    e.taa_render_samples=SAMPLES; e.use_gtao=True; e.use_bloom=True; e.bloom_intensity=.06; e.bloom_threshold=1.0; e.use_soft_shadows=True
    sc.view_settings.view_transform='Standard'; sc.view_settings.look='Medium High Contrast'
    bpy.ops.object.light_add(type='SUN'); S=bpy.context.object; S.rotation_euler=(R(60),0,R(-40)); S.data.energy=3.2; S.data.color=(1,.95,.88)
    planet=oico((0,40,0),9,M('#3FA87A',.7,kind='leaves',sc=.05),sub=5); ring=ocyl((0,40,0),15,.05,M('#E8C07A',.6,alpha=.85),rot=(R(72),R(10),0),seg=64); ring2=ocyl((0,40,0),12.5,.06,M('#F4E4B8',.6,alpha=.7),rot=(R(72),R(10),0),seg=64)
    moon=oico((-14,55,8),2.2,M('#C9C4BC',.9,kind='concrete',sc=.2),sub=3)
    bb=empty((2.5,22,3)); obox((0,0,0),(4.2,.12,1.4),M('#2B2F3A',.3,metal=.8),.08,bb); obox((0,-.13,0),(4.0,.02,1.25),M('#1F4D3A',.5,emit=.4),0,bb)
    text('LAHORI FOOD STREET',(0,-.18,.42),(0,-1,0),.6,M('#F6E7B0',.3,emit=3.0),.02,bb); text('OPENING SOON',(0,-.18,-.42),(0,-1,0),.72,M('#FF8A3A',.3,emit=5.0),.02,bb)
    for sx in (-3.4,3.4): obox((sx,0,-2.6),(.08,.08,1.4),M('#8E95A4',.3,metal=.8),.02,bb)
    sun=oico((60,140,30),14,M('#FFE2A0',.2,emit=12),sub=3)
    return dict(planet=planet,ring=ring,bb=bb)
