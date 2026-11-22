# sets for "Every Pakistani wedding is a war": Lahore shaadi hall (exterior lawn, hall with stage, dance floor, buffet) + groom's dressing room
def area(loc,e,size=(2,1),col=(1,1,1),rot=(0,0,0),shadow=False):
    bpy.ops.object.light_add(type='AREA',location=loc); a=bpy.context.object; a.data.energy=e; a.data.shape='RECTANGLE'; a.data.size=size[0]; a.data.size_y=size[1]; a.data.color=col; a.rotation_euler=rot
    try: a.data.use_shadow=shadow
    except Exception: pass
    return a
LEAF=[M('#3E8E4A',.7,kind='leaves'),M('#5FA84A',.7,kind='leaves'),M('#2F7A45',.7,kind='leaves'),M('#74B85A',.7,kind='leaves')]
GOLD=M('#D4AF5A',.28,metal=.85); GOLD2=M('#B8923E',.35,metal=.7); CREAM=M('#F3EADB',.75,kind='wall'); IVORY=M('#FBF6EC',.8,kind='fabric')
MAROON=M('#7E1A2C',.7,kind='fabric'); ROSE=[M('#C21E3A',.6),M('#F4F1EA',.6),M('#E8A0B4',.6),M('#F2C12E',.6),M('#E2562E',.6)]
BULB=M('#FFE2A8',.2,emit=4.0); BULB2=M('#FFF4DA',.2,emit=2.6); WOOD=M('#6E4428',.7,kind='wall')
def flower_ball(x,y,z,r=.22,seed=0,n=7):
    rr=random.Random(seed)
    for k in range(n): B.ico((x+rr.uniform(-r,r)*.7,y+rr.uniform(-r,r)*.7,z+rr.uniform(-r,r)*.6),r*.45,ROSE[(k+seed)%5],sub=1)
def garland(a,b,sag=.4,n=14,seed=0,size=.06):
    pts=[Vector(a).lerp(Vector(b),i/n)-Vector((0,0,sag*math.sin(pi*i/n))) for i in range(n+1)]
    for i,p in enumerate(pts): B.ico(tuple(p),size,ROSE[(i+seed)%5],sub=1)
def fairy(a,b,sag=.25,n=24,mat=None):
    mat=mat or BULB; pts=[Vector(a).lerp(Vector(b),i/n)-Vector((0,0,sag*math.sin(pi*i/n))) for i in range(n+1)]
    for p in pts: B.ico(tuple(p),.035,mat,sub=1)
def chandelier(x,y,z,s=1.0):
    B.cyl((x,y,z+.6*s),.02,1.2*s,GOLD,seg=6)
    for ring,(rad,dz,n) in enumerate(((.55*s,0,14),(.38*s,-.28*s,10),(.2*s,-.52*s,6))):
        B.cyl((x,y,z+dz),rad,.05,GOLD,seg=20,rot=(0,0,0))
        for k in range(n):
            a=2*pi*k/n; B.ico((x+rad*math.cos(a),y+rad*math.sin(a),z+dz-.12),.045*s,M('#FFF8E8',.05,emit=3.0),sub=1,sc=(1,1,2.2))
    B.ico((x,y,z-.72*s),.09*s,M('#FFF8E8',.05,emit=3.0),sub=1,sc=(1,1,1.6))
def chair(x,y,rz,sash='#C9A24A'):
    a=R(rz); c,s_=math.cos(a),math.sin(a)
    def P(dx,dy,z): return (x+dx*c-dy*s_,y+dx*s_+dy*c,z)
    B.box(P(0,0,.5),(.24,.24,.04),IVORY,.03,rot=(0,0,a))
    for dx in (-.2,.2):
        for dy in (-.2,.2): B.box(P(dx,dy,.25),(.025,.025,.25),GOLD2,.005,rot=(0,0,a))
    B.box(P(0,.22,.95),(.24,.04,.42),IVORY,.04,rot=(0,0,a)); B.box(P(0,.25,.9),(.25,.012,.09),M(sash,.4,metal=.3),.01,rot=(0,0,a))
def round_table(x,y,seed=0,chairs=6,cloth='#FBF6EC',runner='#7E1A2C'):
    B.cyl((x,y,.43),.95,.86,M(cloth,.85,kind='fabric'),seg=28,r2=1.05); B.cyl((x,y,.865),.96,.02,M(cloth,.85,kind='fabric'),seg=28,rot=(0,0,0))
    B.cyl((x,y,.88),.55,.012,M(runner,.6,kind='fabric'),seg=24,rot=(0,0,0))
    B.cyl((x,y,1.1),.04,.45,GOLD,seg=8,rot=(0,0,0)); flower_ball(x,y,1.38,.2,seed)
    for k in range(6):
        a=2*pi*k/6+.3; B.cyl((x+.72*math.cos(a),y+.72*math.sin(a),.885),.13,.01,M('#FFFFFF',.2,spec=.9),seg=16,rot=(0,0,0)); B.cyl((x+.62*math.cos(a+.3),y+.62*math.sin(a+.3),.96),.03,.16,M('#E8F2FF',.05,spec=1.0,alpha=.5),seg=8,rot=(0,0,0))
    for k in range(chairs):
        a=2*pi*k/chairs; chair(x+1.35*math.cos(a),y+1.35*math.sin(a),math.degrees(a)+90,sash=['#C9A24A','#7E1A2C'][seed%2])
HALL=dict(x0=-16,x1=16,y0=-14,y1=14,h=6.5)
def hall(lights=True):
    x0,x1,y0,y1,h=HALL['x0'],HALL['x1'],HALL['y0'],HALL['y1'],HALL['h']
    # floor: marble with carpet runners
    B.box((0,0,-.05),(x1+.5,y1+.5,.05),M('#E9DFCF',.25,kind='wall',spec=.6),0)
    for i in range(-15,16,2):
        for j in range(-13,14,2): B.box((i,j,.002),(.98,.98,.002),M(['#EFE6D6','#E2D5C0'][(i//2+j//2)%2],.22,spec=.6),0)
    B.box((0,-8.5,.008),(1.2,5.5,.006),MAROON,0)   # aisle carpet from entrance
    # walls with gold panels
    for (cx,cy,sx,sy) in ((0,y1,x1,.15),(0,y0,x1,.15),(x0,0,.15,y1),(x1,0,.15,y1)): B.box((cx,cy,h/2),(sx,sy,h/2),CREAM,0)
    for side,xx in ((-1,x0+.17),(1,x1-.17)):
        for j in range(-12,13,4):
            B.box((xx,j,2.6),(.02,1.4,1.9),M('#F7EFE0',.6,kind='wall'),.01); B.box((xx,j,2.6),(.03,1.5,.04),GOLD,.005); B.box((xx,j,4.55),(.03,1.5,.04),GOLD,.005)
            B.box((xx,j,.65),(.03,1.5,.04),GOLD,.005); B.box((xx-side*.03,j,3.9),(.03,.12,.25),M('#FFE9C0',.3,emit=2.0),.01)
    # ceiling drapes (swags) + fairy light canopy
    B.box((0,0,h+.05),(x1,y1,.05),M('#FBF6EC',.8,kind='fabric'),0)
    for j in range(-12,13,3):
        for i in range(-14,15,4): B.box((i,j,h-.35+.25*math.cos((i%4)*.8)),(2.0,1.4,.04),IVORY,.2,rot=(R(4),0,0))
    for i in range(-14,15,2): fairy((i,y0+.3,h-.2),(i,y1-.3,h-.2),sag=.5,n=40,mat=BULB2)
    for (cx,cy) in ((-8,-6),(0,-6),(8,-6),(-8,2),(8,2),(-8,9),(8,9)): chandelier(cx,cy,h-1.4)
    chandelier(0,1,h-1.2,1.4)
    # columns wrapped with flowers
    for cx in (-11,-5.5,5.5,11):
        for cy in (-9,-2,6):
            B.cyl((cx,cy,h/2),.32,h,M('#F7EFE0',.5,kind='wall'),seg=16,rot=(0,0,0)); B.cyl((cx,cy,.15),.42,.3,GOLD2,seg=16,rot=(0,0,0)); B.cyl((cx,cy,h-.15),.42,.3,GOLD2,seg=16,rot=(0,0,0))
            for k in range(10): a=k*.9; B.ico((cx+.33*math.cos(a),cy+.33*math.sin(a),.6+k*.52),.11,ROSE[k%5],sub=1)
    # STAGE
    B.box((0,11.5,.3),(6.0,2.5,.3),M('#F3EADB',.5,kind='wall'),.02); B.box((0,9.0,.31),(6.02,.02,.3),GOLD,.005)
    for k in range(3): B.box((0,8.55-k*.0,.1+k*.1),(2.0,.3+.0,.1+k*.1),M('#EDE2CF',.5,kind='wall'),.01) if k==0 else None
    B.box((0,8.75,.1),(2.0,.25,.1),M('#EDE2CF',.5,kind='wall'),.01); B.box((0,8.5,.05),(2.0,.25,.05),M('#EDE2CF',.5,kind='wall'),.01)
    B.box((0,11.2,.605),(5.8,2.2,.004),MAROON,0)
    # golden sofa (seat top z=1.12) at y=11.6
    sofa_y=11.6; B.box((0,sofa_y,.86),(1.6,.5,.26),M('#E8D6B0',.55,kind='fabric'),.08); B.box((0,sofa_y+.45,1.55),(1.7,.12,.65),GOLD,.12)
    B.box((0,sofa_y+.36,1.45),(1.5,.06,.5),M('#8E1F33',.6,kind='fabric'),.1)
    for s in (-1,1): B.box((s*1.62,sofa_y,1.2),(.14,.5,.3),GOLD,.08); B.ico((s*1.65,sofa_y+.45,2.2),.12,GOLD,sub=2)
    for i in range(5): B.box((-1.2+i*.6,sofa_y-.12,1.14),(.26,.3,.04),M(['#8E1F33','#E8C25A'][i%2],.6,kind='fabric'),.04)
    # floral backdrop + arch + fairy-light curtain
    B.box((0,13.7,3.2),(6.0,.1,3.2),M('#2A0E16',.8,kind='fabric'),0)
    for i in range(48): fairy((-5.8+i*.25,13.55,6.2),(-5.8+i*.25,13.55,.7),sag=0,n=18,mat=BULB)
    for k in range(60):
        a=pi*k/59; flower_ball(3.6*math.cos(a),13.4,1.0+4.2*math.sin(a),.28,k,5)
    for s in (-1,1):
        for k in range(8): flower_ball(s*3.6,13.4,.7+k*.38,.3,k+20,5)
        B.cyl((s*4.9,10.6,.95),.08,.7,GOLD,seg=8,rot=(0,0,0)); flower_ball(s*4.9,10.6,1.6,.4,s+5,10)
        B.cyl((s*4.9,12.6,.95),.08,.7,GOLD,seg=8,rot=(0,0,0)); flower_ball(s*4.9,12.6,1.6,.4,s+7,10)
    text('HAMZA',(0,13.52,5.05),(0,-1,0),.42,M('#FFE2A8',.2,emit=3.0),ex=.02)
    text('weds',(0,13.52,4.65),(0,-1,0),.22,M('#FFE2A8',.2,emit=2.5),ex=.015)
    # DANCE FLOOR (LED checker) — the tiles get animated colors from dance_lights()
    for i in range(-4,4):
        for j in range(-3,5): B.box((i+.5,j+.5,.012),(.48,.48,.01),M(['#F7F2FF','#2A2440'][(i+j)%2],.15,spec=.9,emit=(.4 if (i+j)%2==0 else 0)),0)
    B.box((0,1,.008),(4.1,4.1,.006),GOLD2,0)
    # DJ booth + speakers
    B.box((7.0,7.8,.6),(1.2,.45,.6),M('#1A1B22',.4),.03); B.box((7.0,7.55,.75),(1.15,.02,.3),M('#3B2A6E',.3,emit=1.5),0)
    for s in (5.4,8.6):
        B.box((s,8.0,.9),(.3,.3,.9),M('#121318',.5),.03)
        for z in (.55,1.25): B.cyl((s,7.69,z),.18,.02,M('#2A2B33',.4),seg=16)
    # tables left and right
    k=0
    for side in (-1,1):
        for (tx,ty) in ((10.0,-6.5),(13.5,-3.0),(10.0,.5),(13.5,4.0),(10.0,-10.5),(13.5,-11.5)):
            round_table(side*tx,ty,k); k+=1
    # BUFFET along the west side: counter x[-15.2,-13.8], y[-11,-3.5]; waiter stands at x=-14.9, faces +x
    B.box((-14.4,-7.2,.45),(.6,3.9,.45),M('#FBF6EC',.85,kind='fabric'),.02); B.box((-14.4,-7.2,.91),(.62,3.92,.02),M('#FFFFFF',.4),.01)
    B.box((-13.79,-7.2,.45),(.01,3.9,.42),M('#8E1F33',.7,kind='fabric'),0)
    for k in range(7):
        a=k*.55; B.box((-13.78,-10.8+k*1.2,.75),(.012,.25,.12),M('#E8C25A',.5,metal=.5),0)
    B.box((-15.78,-7.2,2.8),(.05,4.2,.9),M('#3A0E18',.8,kind='fabric'),0); text('SHAADI BUFFET',(-15.71,-7.2,3.0),(1,0,0),.4,M('#FFE2A8',.2,emit=2.6),ex=.02)
    for k in range(18): fairy((-15.7,-11.3+k*.48,3.75),(-15.7,-11.3+k*.48,1.95),sag=0,n=12,mat=BULB)
    DISH=[]
    for k,lab in enumerate(('NAAN','KARAHI','QORMA','BIRYANI','RAITA')):
        y=-10.2+k*1.55; B.box((-14.4,y,.98),(.36,.5,.06),M('#C9CDD6',.2,metal=.9),.02); B.box((-14.4,y,.94),(.4,.54,.02),M('#B0B4BE',.3,metal=.8),.01)
        for sy in (-.5,.5): B.cyl((-14.4,y+sy,.85),.012,.18,M('#C9CDD6',.2,metal=.9),seg=6,rot=(0,0,0))
        B.box((-13.95,y,1.08),(.02,.2,.07),M('#1A1B22',.4),.005,rot=(0,R(-30),0)); text(lab,(-13.93,y,1.08),(1,0,0),.06,M('#FFE2A8',.2,emit=2.0),ex=.004)
        DISH.append(y)
    # entrance doors (south wall) with flower arch
    B.box((0,y0+.05,1.5),(1.6,.18,1.5),M('#3A2218',.5,kind='wall'),.02)
    for s in (-1,1): B.box((s*.8,y0+.2,1.5),(.75,.04,1.45),M('#6E4428',.5,kind='wall'),.02); B.box((s*.2,y0+.25,1.4),(.03,.03,.25),GOLD,.01)
    for k in range(30): a=pi*k/29; flower_ball(2.0*math.cos(a),y0+.4,.4+3.0*math.sin(a),.24,k,4)
    # lights
    if lights:
        area((0,0,h-.3),900,(28,24),(1,.86,.66))
        area((0,10.0,4.6),420,(10,2.5),(1,.9,.75),rot=(R(25),0,0))
        area((-12.6,-7.2,3.6),180,(2,7),(1,.88,.7),rot=(0,R(-30),0))
        area((0,1,5.4),220,(7,7),(1,.85,.75))
        area((0,0,.4),1400,(30,26),(1,.84,.66),rot=(R(180),0,0))
        for (lx,ly,rz) in ((-13,0,90),(13,0,-90),(0,-11.5,180),(0,11.0,0)):
            area((lx,ly,3.2),500,(20 if rz in (0,180) else 26,5),(1,.86,.7),rot=(R(90),0,R(rz)))
    return dict(dish=DISH)
def dance_lights(tiles=None):
    """colored moving spot lights over the dance floor"""
    L=[]
    for k,col in enumerate(((1,.25,.55),(.3,.45,1),(1,.75,.2),(.4,1,.6))):
        bpy.ops.object.light_add(type='SPOT',location=(0,1,5.8)); sp=bpy.context.object; sp.data.energy=900; sp.data.color=col; sp.data.spot_size=R(32); sp.data.spot_blend=.6
        try: sp.data.use_shadow=False
        except Exception: pass
        L.append(sp)
    def upd(t):
        for k,sp in enumerate(L):
            a=t*.9+k*pi/2; sp.rotation_euler=(R(25)*math.cos(a*1.3),R(25)*math.sin(a),0)
    return upd
def exterior():
    """night lawn in front of the hall: facade with light-curtains, gate, cars, lawn"""
    x0,x1,y0,h=-16,16,-14,6.5
    B.box((0,-40,-.05),(60,30,.05),M('#2E5A2E',.9,kind='grass'),0)
    B.box((0,-24,.004),(3.2,10.5,.004),M('#4A4A52',.8,kind='asphalt'),0)
    for s in (-1,1): B.box((s*3.4,-24,.06),(.15,10.5,.06),M('#BDB5A6',.7),.01)
    # facade
    B.box((0,y0-.2,h/2+.5),(x1+.6,.25,h/2+.5),M('#EDE1CB',.6,kind='wall'),0)
    B.box((0,y0-.5,h+1.2),(x1+.8,.3,.3),GOLD2,.02)
    for i in range(-15,16,3):
        B.box((i,y0-.5,h/2),(.22,.12,h/2),M('#F5EBD8',.5,kind='wall'),.02)
    for i in range(-15,16,1): fairy((i+.0,y0-.62,h+.9),(i,y0-.62,.4),sag=0,n=30,mat=[BULB,M('#FFB0C8',.2,emit=3.5),M('#B0D0FF',.2,emit=3.5)][i%3])
    text('ROYAL PALM MARQUEE',(0,y0-.82,h+1.22),(0,-1,0),.55,M('#FFE2A8',.2,emit=3.2),ex=.03)
    # entrance arch outside
    for k in range(36): a=pi*k/35; flower_ball(2.4*math.cos(a),y0-1.2,.5+3.4*math.sin(a),.3,k,4)
    B.box((0,y0-.4,1.5),(1.6,.1,1.5),M('#FFDFA0',.2,emit=1.5),0)
    # red carpet
    B.box((0,y0-6,.01),(1.2,6,.008),MAROON,0)
    # trees with fairy lights, lamp posts
    rr=random.Random(5)
    for s in (-1,1):
        for k in range(5):
            x=s*(6+k*2.6); y=-17.5-rr.uniform(0,1.2); B.cyl((x,y,1.4),.16,2.8,M('#5A3E28',.85),seg=8)
            for j in range(5): B.ico((x+rr.uniform(-.8,.8),y+rr.uniform(-.8,.8),3.0+rr.uniform(0,1)),.9,LEAF[j%4],sub=1,sc=(1,1,.85))
            for j in range(14): a=j*.75; B.ico((x+.95*math.cos(a),y+.95*math.sin(a),2.6+j*.12),.05,BULB,sub=1)
        for k in range(4):
            x=s*4.2; y=-17-k*3.2; B.cyl((x,y,1.6),.06,3.2,M('#1A1B22',.4,metal=.6),seg=8); B.ico((x,y,3.3),.22,M('#FFF0C8',.2,emit=4),sub=2)
    # parked cars
    for k,(x,y,col) in enumerate(((-8,-24,'#F4F5FA'),(-11.5,-24.5,'#1A1B22'),(8.5,-23.5,'#9AA0A8'),(12,-25,'#7E1A2C'),(-9,-30,'#2F4E8C'),(10,-30,'#F4F5FA'))):
        car(x,y,90,col)
    area((0,-18,8),3200,(30,10),(1,.82,.6)); area((0,-22,3),900,(14,6),(1,.85,.7),rot=(R(70),0,0))
    return None
def car(x,y,rz,col):
    a=R(rz); c,s_=math.cos(a),math.sin(a)
    def P(dx,dy,z): return (x+dx*c-dy*s_,y+dx*s_+dy*c,z)
    B.box(P(0,0,.55),(1.05,2.1,.32),M(col,.25,metal=.6),.12,rot=(0,0,a)); B.box(P(0,-.15,1.05),(.92,1.15,.28),M('#1E2530',.08,spec=1.0),.14,rot=(0,0,a))
    for dx in (-.95,.95):
        for dy in (-1.3,1.3): B.cyl(P(dx,dy,.33),.33,.22,M('#111216',.8),seg=14,rot=(0,R(90),a))
    for dx in (-.65,.65): B.box(P(dx,2.08,.62),(.18,.03,.08),M('#FFF4DA',.2,emit=2.0),.02,rot=(0,0,a))
# ---------------------------------------------------------------- groom's dressing room (separate set at x=60)
GX,GY=60,0
def dressing_room():
    x,y=GX,GY; W_=M('#BFD8D2',.8,kind='wall')
    B.box((x,y,-.05),(3.2,2.8,.05),M('#8A5A3A',.5,kind='wall',spec=.5),0)
    for i in range(-3,3):
        for j in range(-3,3): B.box((x+i+.5,y+j+.5,.002),(.48,.48,.002),M(['#9A6A48','#8A5A3A'][(i+j)%2],.45,spec=.5),0)
    B.box((x,y+1.5,.006),(1.6,.9,.004),M('#7E1A2C',.8,kind='fabric'),0); B.box((x,y+1.5,.008),(1.4,.75,.004),M('#C9A24A',.7,kind='fabric'),0)
    for (cx,cy,sx,sy) in ((x,y+2.8,3.2,.1),(x,y-2.8,3.2,.1),(x-3.2,y,.1,2.8),(x+3.2,y,.1,2.8)): B.box((cx,cy,1.75),(sx,sy,1.75),W_,0)
    B.box((x,y,3.55),(3.2,2.8,.05),M('#F4F1EA',.8,kind='wall'),0)
    for (cx,cy,sx,sy) in ((x,y+2.68,3.2,.02),(x-3.08,y,.02,2.8),(x+3.08,y,.02,2.8)): B.box((cx,cy,.08),(sx,sy,.08),M('#F4F1EA',.6),.01)
    # dressing table + bulb mirror on north wall (mirror center x, y+2.66)
    B.box((x,y+2.3,.42),(1.1,.38,.42),M('#F4F1EA',.5,kind='wall'),.02); B.box((x,y+2.3,.86),(1.15,.42,.03),M('#E8E2D6',.3),.01)
    B.box((x,y+2.66,1.9),(.85,.03,.75),M('#A9BDD0',.12,emit=.35,spec=1.0),.01); B.box((x,y+2.67,1.9),(.92,.02,.82),M('#F4F1EA',.5),.01)
    for k in range(9):
        B.ico((x-.88+k*.22,y+2.62,2.7),.05,BULB,sub=1)
    for k in range(7): B.ico((x-.92,y+2.62,1.2+k*.22),.05,BULB,sub=1); B.ico((x+.92,y+2.62,1.2+k*.22),.05,BULB,sub=1)
    for k,(dx,col,hh) in enumerate(((-.8,'#C9A24A',.18),(-.6,'#E8A0B4',.14),(.55,'#2F4E8C',.2),(.75,'#F4F1EA',.12),(.35,'#1A1B22',.08))): B.cyl((x+dx,y+2.25,.9+hh/2),.04,hh,M(col,.2,spec=.9),seg=10,rot=(0,0,0))
    B.box((x-.2,y+2.2,.92),(.12,.08,.02),M('#1A1B22',.4),.01)
    # groom's chair (seat .55) facing mirror (+y) at (x, y+1.2)
    B.box((x,y+1.1,.5),(.32,.3,.06),M('#7E1A2C',.6,kind='fabric'),.04); B.box((x,y+.82,1.0),(.32,.06,.5),M('#7E1A2C',.6,kind='fabric'),.04)
    for dx in (-.28,.28):
        for dy in (.85,1.35): B.cyl((x+dx,y+dy,.24),.025,.48,GOLD2,seg=6,rot=(0,0,0))
    # clothes rack with garment bags (east wall)
    B.box((x+2.6,y+.2,1.95),(.03,1.2,.03),M('#C9CDD6',.3,metal=.8),.01)
    for dy in (-1.0,1.4): B.box((x+2.6,y+dy,.98),(.03,.03,.98),M('#C9CDD6',.3,metal=.8),.01)
    for k,col in enumerate(('#F4F1EA','#8E1F33','#1E1F26','#E8C25A','#2F8C99')): B.box((x+2.6,y-.8+k*.42,1.35),(.25,.16,.55),M(col,.7,kind='fabric'),.06)
    # window (west wall) with night city + curtains
    B.box((x-3.08,y+.3,1.9),(.02,.9,.7),M('#1E2A4A',.4,emit=.6),0)
    for k in range(10): B.box((x-3.06,y-.4+k*.15,1.6+(k%3)*.2),(.005,.03,.03),M('#FFE2A8',.2,emit=3.0),0)
    for s in (-1,1): B.box((x-3.0,y+.3+s*1.05,1.9),(.04,.28,1.15),M('#C9A24A',.8,kind='fabric'),.06)
    # sofa (south) + side table with chai cups, AC unit, ceiling fan, door (east)
    B.box((x-1.4,y-2.35,.42),(1.0,.35,.22),M('#5C3A5A',.7,kind='fabric'),.08); B.box((x-1.4,y-2.62,.85),(1.0,.1,.4),M('#5C3A5A',.7,kind='fabric'),.08)
    B.box((x+.9,y-2.3,.36),(.3,.3,.36),M('#6E4428',.5),.02)
    B.box((x+1.5,y+2.66,3.0),(.6,.12,.18),M('#F4F5FA',.4),.04)
    B.cyl((x,y,3.4),.06,.25,M('#F4F1EA',.5),seg=8,rot=(0,0,0))
    B.box((x+3.08,y-1.2,1.15),(.03,.55,1.15),M('#6E4428',.5,kind='wall'),.02); B.cyl((x+3.04,y-.8,1.1),.04,.06,GOLD,seg=8,rot=(0,R(90),0))
    # framed photo + flowers on dressing table
    B.box((x-2.2,y+2.66,2.1),(.35,.02,.25),GOLD2,.01); B.box((x-2.2,y+2.64,2.1),(.3,.01,.2),M('#C98F62',.6),0)
    flower_ball(x+.95,y+2.2,1.08,.14,3,6)
    fan=empty((x,y,3.25))
    for k in range(3): obox((math.cos(2*pi*k/3)*.5,math.sin(2*pi*k/3)*.5,0),(.5,.07,.01),M('#F4F1EA',.5),.01,fan,rot=(0,0,2*pi*k/3))
    area((x,y,3.3),160,(3,3),(1,.9,.78)); area((x,y+2.2,2.2),70,(1.6,.3),(1,.92,.8),rot=(R(-80),0,0))
    point((x-.9,y+2.5,1.9),25,(1,.85,.6),.2,shadow=False); point((x+.9,y+2.5,1.9),25,(1,.85,.6),.2,shadow=False)
    return fan
# ---------------------------------------------------------------- props
def notebook(H,s=-1):
    o=obox((0,0,0),(.09,.012,.12),M('#2F4E8C',.6),.005); obox((0,-.013,0),(.07,.002,.1),M('#F4F1EA',.6),0,o); return o
def plate(fill='#E8A040'):
    o=ocyl((0,0,0),.16,.02,M('#FFFFFF',.2,spec=.8),rot=(0,0,0));
    for k in range(9): oico((math.cos(k)*.07,math.sin(k*1.7)*.07,.025),.035,M([fill,'#F4E8C8','#C9302C'][k%3],.7),o,sub=1)
    return o
def wallet():
    o=obox((0,0,0),(.06,.012,.045),M('#4A2E1E',.5),.006); return o
def dslr():
    o=obox((0,0,0),(.09,.05,.06),M('#1A1B22',.35),.01); ocyl((0,-.08,0),.04,.07,M('#0B0C10',.2,spec=.9),o); oico((-.05,-.01,.07),.015,M('#FFFFFF',.1,emit=0),o,sub=1); return o
def tray_lid():
    o=obox((0,0,0),(.36,.5,.04),M('#D8DCE4',.15,metal=.95),.03); obox((0,0,.07),(.08,.03,.03),M('#C9CDD6',.2,metal=.9),.01,o); return o
