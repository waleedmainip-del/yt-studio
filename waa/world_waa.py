# World for the "World Auctions Arena" demo: a luxury auction hall (brand-new set) + the placement gantry for the street clip.
MOODS['waa_hall']=dict(sun=(60,-160),e=.25,col=(1,.9,.8),top='#0A0810',bot='#1A1420',sky=.3,mist='#1A1420',cloud='#201A28',cov=.3,cstr=.5)
AHX=10.0; AY0=-13.0; AY1=11.0; AHZ=9.6; STG=.7; STY=3.6; PX=-5.6; PY=5.2; TTX=2.6; TTY=7.3
def vchair(x,y,rz,col='#7A1F2E'):
    """velvet auction chair (seat top .56) facing rz"""
    e=empty((x,y,0),rot=(0,0,R(rz))); cm=M(col,.8,kind='fabric'); gm=M(GOLD,.3,metal=.8)
    obox((0,0,.47),(.44,.4,.09),cm,.05,e)
    for sx in (-.36,.36):
        for sy in (-.32,.32): ocyl((sx,sy,.19),.035,.38,gm,e,rot=(0,0,0),seg=6)
    obox((0,.42,1.0),(.44,.06,.5),cm,.06,e,rot=(R(-6),0,0)); obox((0,.47,1.53),(.3,.03,.05),gm,.02,e)
    return e
def supercar(loc,rz,col='#C8102E',parent=None):
    """low wedge supercar, faces +x, about 6.2 long (sized for the 2.5 m avatars)"""
    root=empty(loc,parent,rot=(0,0,R(rz))); s=1.5
    body=M(col,.18,metal=.55,spec=.9); gl=M('#10141C',.05,spec=1.0); blk=M('#101116',.5); W=[]
    def b(c,h,m,bv=.1,rot=(0,0,0)): return obox(tuple(v*s for v in c),tuple(v*s for v in h),m,bv*s,root,rot=rot)
    b((0,0,.42),(2.05,.9,.2),body,.12); b((1.25,0,.57),(.8,.86,.09),body,.08,rot=(0,R(7),0)); b((-1.35,0,.66),(.7,.88,.14),body,.1)
    b((-.15,0,.86),(.85,.74,.17),gl,.14); b((-.2,0,.99),(.6,.7,.055),body,.05); b((.62,0,.8),(.3,.72,.03),gl,.02,rot=(0,R(-28),0))
    b((-1.95,0,.95),(.09,.86,.025),blk,.02)
    for sy in (-1,1):
        b((-1.9,sy*.7,.86),(.03,.03,.08),blk,.01)
        b((2.02,sy*.62,.5),(.04,.2,.05),M('#FFF6D8',.2,emit=3.0),.02); b((-2.05,sy*.6,.6),(.03,.22,.04),M('#FF2A1A',.3,emit=2.2),.02)
        b((.1,sy*.905,.5),(.7,.012,.06),blk,.01)
    b((2.08,0,.3),(.03,.6,.07),blk,.02)
    for sx in (-1.3,1.3):
        for sy in (-.86,.86): W.append(wheel((sx*s,sy*s,.36*s),.36*s,.26*s,root))
    return dict(root=root,wheels=W)
def arena():
    """auction hall. audience looks +y at the stage (top STG, front edge y=STY). screen on the back wall. returns dict(scr pages, turntable)"""
    NIGHT[0]=1.0; S=setup_world('waa_hall',shadow=40)
    wal=M('#3A2418',.55,kind='wood',sc=.7); wal2=M('#2A1810',.5,kind='wood',sc=.7); gm=M(GOLD,.3,metal=.85); blk=M('#15121A',.75,kind='fabric'); mar=M('#2A2630',.25,spec=.8,kind='tile',sc=2.2)
    red=M('#8A1424',.85,kind='fabric',sc=.8); yc=(AY0+AY1)/2; yh=(AY1-AY0)/2
    B.box((0,yc,-.1),(AHX,yh,.1),mar,0); B.box((0,(AY0+STY)/2,.008),(1.15,(STY-AY0)/2,.01),red,0)
    for sx in (-1,1): B.box((sx*1.2,(AY0+STY)/2,.012),(.05,(STY-AY0)/2,.012),gm,0)
    PC=[('#2E6FA8','#F2C14E','#E8554D'),('#1E6A3A','#F4E9C8','#C8662C'),('#7A2E5A','#F2A0B8','#F4F1EA'),('#C8662C','#2A3A6A','#F2E3C4')]
    for sx in (-1,1):
        B.box((sx*(AHX+.15),yc,AHZ/2),(.15,yh,AHZ/2),wal,0); B.box((sx*(AHX-.02),yc,.5),(.04,yh,.5),wal2,0); B.box((sx*(AHX-.05),yc,1.03),(.06,yh,.035),gm,0)
        for k,y in enumerate((-10.5,-6.5,-2.5,1.5)):
            B.box((sx*(AHX-.1),y+2.0,AHZ/2),(.12,.22,AHZ/2),wal2,.02); B.box((sx*(AHX-.24),y+2.0,AHZ-.6),(.05,.3,.12),gm,.02)
            pc=PC[(k+(2 if sx>0 else 0))%4]
            B.box((sx*(AHX-.06),y,3.9),(.05,1.25,1.0),gm,.03); B.box((sx*(AHX-.1),y,3.9),(.03,1.1,.85),M(pc[0],.7),0)
            B.box((sx*(AHX-.13),y-.3,3.6),(.012,.5,.4),M(pc[1],.7),0); B.ico((sx*(AHX-.14),y+.45,4.2),.3,M(pc[2],.6),sc=(.15,1,1),sub=2)
            B.box((sx*(AHX-.2),y,5.25),(.1,.35,.05),gm,.02); B.ico((sx*(AHX-.22),y,5.1),.11,M('#FFE0A0',.3,emit=5.0),sub=2)
    B.box((0,AY0-.15,AHZ/2),(AHX,.15,AHZ/2),wal,0); B.box((0,AY1+.15,AHZ/2),(AHX,.15,AHZ/2),blk,0); B.box((0,yc,AHZ+.1),(AHX,yh,.1),M('#17131C',.7),0)
    for y in (-9,-3,3): B.box((0,y,AHZ-.08),(AHX,.18,.08),gm,0)
    for sx in (-5,0,5): B.box((sx,yc,AHZ-.06),(.12,yh,.06),wal2,0)
    for cx in (-5.6,5.6):                                                                        # chandeliers (off the centre line so the screen stays clear)
        for y in (-7.5,-1.5):
            B.cyl((cx,y,AHZ-.7),.04,1.4,gm,seg=6); B.cyl((cx,y,AHZ-1.45),1.3,.1,gm,seg=20); B.cyl((cx,y,AHZ-1.85),.8,.08,gm,seg=16)
            for k in range(10): a=k*pi/5; B.ico((cx+1.3*math.cos(a),y+1.3*math.sin(a),AHZ-1.62),.12,M('#FFE6B0',.3,emit=3.2),sub=2)
            for k in range(6): a=k*pi/3; B.ico((cx+.8*math.cos(a),y+.8*math.sin(a),AHZ-2.0),.1,M('#FFE6B0',.3,emit=3.2),sub=2)
    # back wall (behind the audience): double doors, two big canvases, sconces
    yb=AY0+.03; B.box((0,yb,2.2),(1.5,.06,2.2),gm,.02); 
    for sx in (-1,1): B.box((sx*.68,yb+.05,2.1),(.64,.04,2.05),wal2,.03); B.box((sx*.68,yb+.1,2.9),(.42,.02,.9),wal,.02); B.box((sx*.68,yb+.1,1.0),(.42,.02,.6),wal,.02); B.box((sx*.14,yb+.12,2.0),(.03,.04,.3),gm,.01)
    for sx,pc in ((-1,PC[1]),(1,PC[3])):
        B.box((sx*5.4,yb+.02,4.2),(2.0,.05,1.5),gm,.03); B.box((sx*5.4,yb+.06,4.2),(1.82,.03,1.32),M(pc[0],.7),0); B.box((sx*5.4-.5,yb+.09,3.75),(.9,.012,.6),M(pc[1],.7),0)
        B.ico((sx*5.4+.7,yb+.1,4.7),.42,M(pc[2],.6),sc=(1,.12,1),sub=2); B.box((sx*5.4,yb+.2,5.95),(.6,.1,.05),gm,.02); B.ico((sx*5.4,yb+.22,5.8),.12,M('#FFE0A0',.3,emit=5.0),sub=2)
    for x in (-8.3,-2.7,2.7,8.3): B.box((x,yb+.08,3.3),(.1,.08,.3),gm,.03); B.ico((x,yb+.2,3.7),.16,M('#FFE0A0',.3,emit=4.5),sub=2)
    # stage, steps, footlights
    B.box((0,(STY+AY1)/2,STG/2),(AHX,(AY1-STY)/2,STG/2),M('#1C1820',.35,spec=.7),0); B.box((0,STY-.04,STG-.06),(AHX,.05,.06),gm,0)
    B.box((0,STY-.45,STG/4),(1.3,.45,STG/4),red,0)
    for k in range(15):
        if abs(-8.4+k*1.2)>1.5: B.box((-8.4+k*1.2,STY+.2,STG+.05),(.12,.08,.05),M('#FFF2D0',.3,emit=4.0),.01)
    # velvet drapes either side of the screen
    for k in range(10):
        for sx in (-1,1): B.box((sx*(5.3+k*.5),AY1-.12,AHZ/2+.3),(.26,.08+.04*(k%2),AHZ/2-.3),M('#5A0F1C' if k%2 else '#7A1626',.8,kind='fabric'),.02)
    B.box((0,AY1-.2,5.9),(4.85,.08,1.85),M('#0A0A0E',.4),.03); B.box((0,AY1-.14,5.9),(4.97,.06,1.97),gm,.02)
    sign('WORLD AUCTIONS ARENA',(0,AY1-.2,8.5),.5,'#FFD86A','#0E0C12',n=(0,-1,0),e=2.2,pad=.2,th=.1,frame=GOLD,always=True)
    # podium + mic
    B.box((PX,PY,STG+.55),(.62,.55,.55),wal,.04); B.box((PX,PY,STG+1.14),(.72,.62,.045),wal2,.03); B.box((PX,PY-.56,STG+.62),(.3,.012,.3),gm,.0,rot=(0,R(45),0))
    B.cyl((PX-.42,PY-.2,STG+1.42),.02,.5,M('#22242B',.4,metal=.6),seg=6); B.ico((PX-.42,PY-.22,STG+1.7),.065,M('#16171C',.5),sub=2)
    # the lots waiting at the side: a painting on an easel, a vase on a pedestal
    for sx in (-1,1): B.box((-8.1+sx*.55,9.4,STG+1.3),(.04,.04,1.3),wal2,0,rot=(R(8),0,0))
    B.box((-8.1,9.25,STG+1.75),(.9,.05,1.1),gm,.02); B.box((-8.1,9.19,STG+1.75),(.78,.03,.98),M('#2E6FA8',.7),0); B.ico((-8.3,9.15,STG+2.05),.34,M('#F2C14E',.6),sc=(1,.1,1),sub=2)
    B.box((-8.1,9.16,STG+1.2),(.78,.012,.34),M('#1E6A3A',.7),0)
    B.box((8.5,5.2,STG+.6),(.4,.4,.6),M('#F4F1EA',.3,spec=.8),.03); B.cyl((8.5,5.2,STG+1.62),.2,.8,M('#2B58C9',.25,spec=.9),seg=14,r2=.32); B.cyl((8.5,5.2,STG+2.12),.16,.2,gm,seg=14)
    # turntable ring glow
    B.cyl((TTX,TTY,STG+.02),3.62,.04,M('#FFE6B0',.3,emit=3.0),seg=48)
    B.done('arena')
    tt=empty((TTX,TTY,STG+.16)); ocyl((0,0,-.08),3.5,.16,M('#D8D2C4',.25,metal=.6,spec=.8),tt,rot=(0,0,0),seg=48); car=supercar((0,0,0),0,parent=tt)
    # LED screen pages
    scr=empty((0,AY1-.3,5.9)); G={}
    obox((0,0,0),(4.6,.01,1.6),M('#0B1230',.4,emit=.5),0,scr)
    ge=M('#FFD23F',.4,emit=2.4); wh=M('#FFFFFF',.4,emit=2.2); rd=M('#FF4A3A',.4,emit=2.6)
    def page(name,lines): G[name]=[text(b_,(0,-.03,z),(0,-1,0),s_,m_,ex=.004,parent=scr) for b_,z,s_,m_ in lines]
    page('brand',[('WORLD',.95,.78,ge),('AUCTIONS',0,.78,ge),('ARENA',-.95,.78,ge)])
    page('lot',[('LOT 07',.8,.6,wh),('2 CRORE',-.5,.95,ge)]); page('three',[('LOT 07',.8,.6,wh),('3 CRORE',-.5,.95,ge)])
    page('sold',[('SOLD!',.6,1.15,rd),('PADDLE 27',-.85,.62,wh)])
    # lights
    L=[spotd((TTX,TTY-.8,9.3),3600,(1,.97,.92),72),spotd((PX,PY+.3,9.3),1900,(1,.92,.8),62),spotd((0,-2.4,9.3),3400,(1,.87,.68),115,r=1.2),
       spotd((0,-8.6,9.3),2200,(1,.85,.64),115,shadow=False),point((-6,8.5,5.0),320,(1,.9,.78),r=1.0,shadow=False),point((0,1.6,3.4),420,(1,.9,.8),r=1.5,shadow=False),
       point((-8.4,-4,4.4),480,(1,.84,.62),r=1.0,shadow=False),point((8.4,-4,4.4),480,(1,.84,.62),r=1.0,shadow=False),point((0,-11.4,4.6),520,(1,.84,.62),r=1.0,shadow=False),
       point((0,-6.5,6.2),1500,(1,.88,.7),r=2.0,shadow=False),point((0,-.5,6.2),1500,(1,.88,.7),r=2.0,shadow=False),point((0,6.2,6.6),1700,(1,.93,.82),r=2.0,shadow=False),
       point((-7.2,9.2,5.2),520,(1,.8,.7),r=1.0,shadow=False),point((7.2,9.2,5.2),520,(1,.8,.7),r=1.0,shadow=False)]
    for l in L: l.data.specular_factor=.4
    return dict(G=G,tt=tt,car=car,L=L)
def spotd(loc,e,col,size=80,blend=.6,shadow=True,r=.5):
    bpy.ops.object.light_add(type='SPOT',location=loc); p=bpy.context.object; p.data.energy=e; p.data.color=col; p.data.spot_size=R(size); p.data.spot_blend=blend
    p.data.shadow_soft_size=r; p.data.use_shadow=shadow; return p
def scr_show(Ar,name):
    for k,objs in Ar['G'].items():
        for o in objs: o.scale=(1,1,1) if k==name else (0,0,0)
def gantry(x=10.0,z0=9.4):
    """advertising gantry across the street (for the placement clip). board faces -x"""
    st=M('#3A3D47',.4,metal=.6);
    for sy in (-1,1): B.cyl((x,sy*4.95,(z0+3.4)/2),.16,z0+3.4,st,seg=10); B.box((x,sy*4.95,.12),(.4,.4,.12),M('#8A8E96',.7),0)
    B.box((x,0,z0-.12),(.14,5.1,.12),st,0); B.box((x,0,z0+3.5),(.14,5.1,.1),st,0)
    B.box((x-.05,0,z0+1.7),(.08,4.75,1.62),M('#0E0C12',.5),0); B.box((x-.02,0,z0+1.7),(.06,4.87,1.74),M(GOLD,.3,metal=.8),0)
    for sy in (-3.2,-1.6,0,1.6,3.2): B.box((x-.9,sy,z0+3.75),(.5,.05,.04),st,0); B.box((x-1.4,sy,z0+3.62),(.12,.14,.07),M('#FFF2D0',.3,emit=5.0),.02)
    B.done('gantry')
    gm=M('#FFD86A',.4,emit=1.6); wm=M('#F4F1EA',.5,emit=.9)
    text('WORLD AUCTIONS',(x-.15,0,z0+2.35),(-1,0,0),.9,gm,ex=.01); text('ARENA',(x-.15,0,z0+1.25),(-1,0,0),.9,gm,ex=.01)
    text('BARKI ROAD, LAHORE',(x-.15,0,z0+.42),(-1,0,0),.46,wm,ex=.008)
    point((x-3.5,0,z0+3.2),900,(1,.93,.8),r=1.0,shadow=False)
