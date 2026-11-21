# sets for "Lahore Lahore Aye": old-city lane / bazaar, Badshahi Masjid, Hamza's haveli home, rooftop skyline
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
BRICK=['#9C4A32','#A85A3E','#8E4430','#B86A4A']; PLAST=['#E8D2A8','#D9B88A','#C9D8C8','#E8C8B0','#B8C8D8','#F0E2C4','#D8A890']
SHUT=['#1F7A8C','#2B58C9','#2E8B6E','#C9452E','#E6A31C','#6C5FB0']; AWN=['#C9452E','#2E8B6E','#E6A31C','#2B58C9','#9E3B4E','#E07A2E','#16909E']
def haveli(x,yface,side,w,h,seed,shop=True,goods=True):
    """old-city house facing the lane. side=+1 north of lane (facade looking -y)"""
    r=random.Random(seed); brick=r.random()<.55; col=r.choice(BRICK) if brick else r.choice(PLAST)
    wall=M(col,.8,kind='concrete',sc=.28) if brick else M(col,.85,kind='wall'); d=6.0; yc=yface+side*d/2; fy=yface-side*.01
    B.box((x,yc,h/2),(w/2,d/2,h/2),wall,.02)
    trim=M(shade(col,.72) if brick else '#F2EDE2',.7); WOOD=M('#6B4026',.6,kind='wood',sc=2); DARK=M('#1E1A18',.9); GLASS=M('#3A4A5A',.2,spec=.8)
    B.box((x,fy-side*.06,h+.15),(w/2+.12,.18,.15),trim,.02)
    for i in range(int(w/1.1)):
        if r.random()<.5: B.box((x-w/2+.55+i*1.1,fy-side*.05,h+.42),(.3,.1,.12),trim,.02)
    # roof clutter
    if r.random()<.6: B.cyl((x+r.uniform(-w/3,w/3),yc+side*r.uniform(0,2),h+.6),.45,1.0,M(r.choice(['#2B2C33','#E8E4D8','#3E6FB0']),.5),seg=12)
    if r.random()<.4: seg((x-w/3,yc,h),(x-w/3,yc,h+2.4),.03,M('#5A5F66',.4,metal=.7))
    sh=r.choice(SHUT); SH=M(sh,.6,kind='wood',sc=2)
    for fl in range(1,int(h/3.1)):
        z=fl*3.1+1.4
        if z>h-.8: break
        n=max(1,int(w/2.4))
        for i in range(n):
            xx=x-w/2+w*(i+.5)/n
            if r.random()<.35:   # jharokha: carved wooden balcony
                B.box((xx,fy-side*.45,z-.75),(.85,.45,.1),WOOD,.03); B.box((xx,fy-side*.45,z+.95),(.9,.5,.08),WOOD,.04)
                for k in range(5): B.box((xx-.7+k*.35,fy-side*.88,z-.2),(.04,.04,.45),WOOD,.01)
                B.box((xx,fy-side*.88,z-.6),(.85,.04,.06),WOOD,.01); B.box((xx,fy-side*.02,z+.1),(.6,.02,.75),DARK,0)
                B.box((xx,fy-side*.45,z+1.12),(.6,.3,.12),WOOD,.06)
            else:
                B.box((xx,fy,z),(.45,.02,.65),GLASS if r.random()<.5 else DARK,0)
                B.box((xx,fy-side*.03,z+.75),(.55,.06,.08),trim,.01); B.box((xx,fy-side*.03,z-.72),(.55,.08,.05),trim,.01)
                for s in (-1,1): B.box((xx+s*.7,fy-side*.12,z),(.24,.03,.66),SH,.01,rot=(0,0,R(s*side*25)))
            if r.random()<.25: B.box((xx,fy-side*.2,z-.95),(.55,.2,.35),M('#C9CDD6',.4,metal=.5),.02)   # AC unit
    # ground floor
    if shop:
        aw=r.choice(AWN); B.box((x,fy-side*.02,1.35),(w/2-.35,.02,1.25),M('#2A2420',.9),0)
        B.box((x,fy-side*.7,2.75),(w/2-.2,.7,.04),M(aw,.7,kind='fabric'),.02,rot=(R(-14*side),0,0))
        for k in range(int(w/.8)): B.box((x-w/2+.4+k*.8,fy-side*1.38,2.6),(.18,.02,.16),M(aw if k%2 else '#F4F1EA',.7),.01)
        B.box((x,fy-side*.05,3.25),(w/2-.5,.04,.3),M(r.choice(['#F4F1EA','#F2C12E','#2E8B6E','#C9452E']),.5,emit=.15),.02)
        for k in range(r.randint(2,4)): B.box((x-w/2+.8+k*1.1,fy-side*.04,3.25),(.35,.01,.16),M(r.choice(['#C9452E','#1E1A18','#2B58C9']),.5),0)
        if goods: stall(x,fy-side*.9,side,w-1.0,r)
    else:
        B.box((x,fy-side*.02,1.25),(.75,.04,1.25),M(r.choice(SHUT),.6,kind='wood',sc=2),.02); B.box((x,fy-side*.06,2.6),(.95,.08,.14),trim,.02)
        for s in (-1,1): B.cyl((x+s*.95,fy-side*.12,1.3),.08,2.6,trim,seg=8)
        B.cyl((x,fy-side*.04,2.5),.75,.06,trim,rot=(R(90),0,0),seg=24)
        if r.random()<.6:
            for s in (-1,1): B.cyl((x+s*1.4,fy-side*.35,.3),.25,.6,M('#B8683A',.8),seg=10,r2=.32); B.ico((x+s*1.4,fy-side*.35,.85),.35,LEAF2,sub=1)
FRUIT=['#E2562E','#F2C12E','#5FA84A','#C9302C','#F28A2E','#7A3E9E']
def stall(x,y,side,w,r):
    T=M('#8A5A3A',.7,kind='wood',sc=3); B.box((x,y,.45),(w/2,.55,.45),T,.03)
    kind=r.choice(['fruit','spice','cloth','pots','sweets'])
    if kind=='fruit':
        for i in range(int(w/.55)):
            c=r.choice(FRUIT)
            for j in range(5): B.ico((x-w/2+.3+i*.55+r.uniform(-.1,.1),y+r.uniform(-.35,.35),.98+r.uniform(0,.12)),.09,M(c,.5),sub=1)
    elif kind=='spice':
        for i in range(int(w/.45)): B.cyl((x-w/2+.25+i*.45,y,1.05),.18,.3,M(r.choice(['#C9452E','#E6A31C','#8A5A2A','#F2C12E','#5A7A2E']),.9),seg=10,r2=.02)
    elif kind=='cloth':
        for i in range(int(w/.4)): B.box((x-w/2+.2+i*.4,y,1.0),(.17,.45,.1),M(r.choice(KUR),.85,kind='fabric'),.03)
        for i in range(int(w/.6)): B.box((x-w/2+.3+i*.6,y-side*.4,2.0),(.22,.02,.6),M(r.choice(KUR),.85,kind='fabric'),.01)
    elif kind=='pots':
        for i in range(int(w/.5)): B.cyl((x-w/2+.25+i*.5,y,1.06),.17,.22,M(r.choice(['#C9CDD6','#B8683A','#C9A24A']),.3,metal=.7),seg=12,r2=.12)
    else:
        for i in range(int(w/.5)): B.box((x-w/2+.25+i*.5,y,.98),(.2,.3,.06),M(r.choice(['#F2C12E','#F4F1EA','#E2562E','#D98AA8']),.6),.02)
def wires(x0,x1,y0,y1,z,n,seed):
    r=random.Random(seed); W_=M('#1A1A1E',.6)
    for i in range(n):
        xa=r.uniform(x0,x1); xb=xa+r.uniform(-4,4); za=z+r.uniform(-.6,.8); zb=z+r.uniform(-.6,.8); sag=r.uniform(.3,.8); pts=[]
        for k in range(7):
            f=k/6; pts.append((L(xa,xb,f),L(y0,y1,f),L(za,zb,f)-sag*4*f*(1-f)))
        for a,b in zip(pts,pts[1:]): seg(a,b,.012,W_,sides=4)
KITE=['#C9302C','#2E8B6E','#F2C12E','#2B58C9','#E07A2E','#D98AA8','#7448C2']
def kites(center,spread,n,seed,zr=(14,34)):
    r=random.Random(seed); out=[]
    for i in range(n):
        p=Vector((center[0]+r.uniform(-spread,spread),center[1]+r.uniform(-spread*.4,spread),r.uniform(*zr)))
        k=empty(tuple(p)); s_=r.uniform(.5,.9); c=M(r.choice(KITE),.6)
        omesh([(0,0,s_),(s_*.75,0,0),(0,0,-s_*1.1),(-s_*.75,0,0)],[(0,1,2,3)],c,k)
        omesh([(0,-.01,-s_*1.1),(.2*s_,-.01,-s_*1.45),(-.2*s_,-.01,-s_*1.45)],[(0,1,2)],M(r.choice(KITE),.6),k)
        ph=r.uniform(0,6)
        def fn(o,t,p=p,ph=ph): o.location=(p.x+.4*math.sin(t*.9+ph),p.y,p.z+.5*math.sin(t*1.3+ph)); o.rotation_euler=(0,R(18)*math.sin(t*1.1+ph),R(10)*math.sin(t*.7+ph))
        fx.add(k,fn); out.append(k)
    return out
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
def lane(x0=-36,x1=36,bazaar=False,seed=5,shop_ratio=.75,wire=True,kite=True):
    """lane along x; walkable y in [-3.2,3.2]; facades at y=+-3.6"""
    GROUND=M('#9A6B4E',.85,kind='concrete',sc=.32); DRAIN=M('#5A5048',.8)
    B.box(((x0+x1)/2,0,-.05),((x1-x0)/2+20,30,.05),GROUND,0)
    for s in (-1,1): B.box(((x0+x1)/2,s*6.25,.03),((x1-x0)/2,.18,.03),DRAIN,0)
    r=random.Random(seed); k=0
    for side in (-1,1):
        x=x0
        while x<x1:
            w=r.uniform(4.5,7.5); h=r.uniform(8.5,14)
            haveli(x+w/2,side*6.5,side,w,h,seed*100+k,shop=r.random()<shop_ratio or bazaar); x+=w+.05; k+=1
    if wire: wires(x0,x1,-6.3,6.3,7.2,int((x1-x0)/2.5),seed+3)
    if bazaar:
        for i in range(int((x1-x0)/5)):
            xx=x0+2+i*5+r.uniform(-1,1)
            for s in (-1,1):
                c=r.choice(AWN); B.box((xx,s*4.7,2.35),(1.2,.7,.03),M(c,.8,kind='fabric'),.02,rot=(R(s*8),0,0))
                for cx in (-1.1,1.1): B.cyl((xx+cx,s*4.2,1.15),.03,2.3,M('#6B4026',.6),seg=6)
            if i%2==0:
                for j in range(6): B.ico((xx+r.uniform(-1,1),r.uniform(-5.5,5.5),5.6+r.uniform(-.3,.3)),.16,M(r.choice(['#F2C12E','#C9302C','#2E8B6E']),.5,emit=1.2),sub=1)
    # far roofs and minaret silhouettes for depth
    for i in range(40):
        xx=r.uniform(x0-20,x1+20); yy=r.choice((-1,1))*r.uniform(12,40); h=r.uniform(8,18)
        B.box((xx,yy,h/2),(r.uniform(3,6),r.uniform(3,6),h/2),M(r.choice(BRICK+PLAST),.85,kind='wall'),0)
    for xx,yy in ((x0+8,45),(x1-6,52)): minaret(xx,yy,0,.8)
    if kite: kites(((x0+x1)/2,10,0),25,14,seed+9)
def minaret(x,y,z,s=1.0,red=None):
    RED=M(red or '#A3472E',.8,kind='concrete',sc=.4); WHT=M('#F2EDE2',.5); h=s*32
    B.cyl((x,y,z+h/2),1.5*s,h,RED,seg=8)
    for k in range(4):
        zz=z+h*(k+1)/4.6; B.cyl((x,y,zz),1.95*s,.35*s,WHT,seg=8); B.cyl((x,y,zz-.4*s),1.7*s,.5*s,RED,seg=8)
        for i in range(8): a=2*pi*i/8; B.box((x+math.cos(a)*1.52*s,y+math.sin(a)*1.52*s,zz-3*s),(.04*s,.04*s,2.2*s),WHT,0,rot=(0,0,a))
    B.cyl((x,y,z+h+1.2*s),1.3*s,2.4*s,WHT,seg=8)
    for i in range(8): a=2*pi*i/8; B.cyl((x+math.cos(a)*1.1*s,y+math.sin(a)*1.1*s,z+h+1.2*s),.12*s,2.4*s,RED,seg=6)
    B.cyl((x,y,z+h+2.6*s),1.7*s,.3*s,WHT,seg=8); B.ico((x,y,z+h+3.4*s),1.2*s,WHT,sc=(1,1,1.1),sub=2); B.cyl((x,y,z+h+5.0*s),.08*s,1.6*s,M('#C9A24A',.3,metal=.8),seg=6)
def onion(x,y,z,r_,mat):
    B.cyl((x,y,z+.3*r_),r_*.92,.6*r_,mat,seg=32)
    B.ico((x,y,z+1.35*r_),r_*1.08,mat,sc=(1,1,.95),sub=3)
    B.cyl((x,y,z+2.45*r_),r_*.42,.9*r_,mat,seg=24,r2=.02)
    B.cyl((x,y,z+3.05*r_),.05*r_,.6*r_,M('#C9A24A',.3,metal=.85),seg=8); B.ico((x,y,z+2.95*r_),.1*r_,M('#C9A24A',.3,metal=.85),sub=1)
def badshahi(yf=30.0):
    """Badshahi-style masjid: prayer hall facade at y=yf facing -y, courtyard in front, 4 corner minarets"""
    RED=M('#A3472E',.8,kind='concrete',sc=.45); RED2=M('#8E3A26',.8); WHT=M('#F2EDE2',.45,spec=.4); STONE=M('#B8583E',.85,kind='concrete',sc=.9)
    B.box((0,yf-28,.0),(46,34,.12),STONE,0)
    for i in range(-44,46,4): B.box((i,yf-28,.125),(.06,34,.005),M('#E8DCC8',.6),0)
    W_=34; H_=16
    B.box((0,yf+6,H_/2),(W_,6,H_/2),RED,.05)
    B.box((0,yf-.2,H_*.62),(8.5,.4,H_*.62),RED,.05)                      # central iwan pishtaq
    B.box((0,yf-.42,H_*.55),(5.6,.05,H_*.5),RED2,0)
    B.box((0,yf-.6,H_*.45),(4.2,.05,H_*.44),M('#2A1E18',.9),0)
    B.cyl((0,yf-.6,H_*.85),4.2,.08,M('#2A1E18',.9),rot=(R(90),0,0),seg=32)
    for s in (-1,1):
        B.box((s*8.6,yf-.6,H_*.62),(.25,.25,H_*.62),WHT,.02); B.box((0,yf-.62,H_*1.24),(8.7,.25,.25),WHT,.02)
        B.box((s*5.7,yf-.48,H_*.5),(.12,.12,H_*.5),WHT,.01)
        for k in range(5):                                                   # side arcades
            xx=s*(11+k*4.6); B.box((xx,yf-.02,4.4),(1.5,.05,4.2),M('#2A1E18',.9),0); B.cyl((xx,yf-.02,8.4),1.5,.06,M('#2A1E18',.9),rot=(R(90),0,0),seg=20)
            B.box((xx,yf-.06,4.4),(1.75,.06,.12),WHT,0); B.box((xx-2.3*s*0+2.3,yf-.07,5.5),(.12,.08,5.4),WHT,0)
        B.cyl((s*8.9,yf-.3,H_*1.36),.45,2.0,WHT,seg=8); B.ico((s*8.9,yf-.3,H_*1.36+1.3),.55,WHT,sub=1)
        B.cyl((s*W_,yf-.1,H_/2+1),.9,H_+2,RED,seg=8); B.cyl((s*W_,yf-.1,H_+3),1.1,1.4,WHT,seg=8); B.ico((s*W_,yf-.1,H_+4.3),.9,WHT,sub=1)
    B.box((0,yf-.3,H_+.4),(W_,.35,.4),WHT,.02)
    for i in range(-33,34,2): B.box((i,yf-.5,H_+1.0),(.35,.2,.3),WHT,.02)
    onion(0,yf+6,H_+.2,6.2,WHT); onion(-15,yf+6,H_+.2,4.4,WHT); onion(15,yf+6,H_+.2,4.4,WHT)
    for s in (-1,1):
        for yy in (yf+10,yf-62):
            minaret(s*46,yy,0,1.1)
    # courtyard walls with arcades + gateway steps at the far end
    for s in (-1,1):
        B.box((s*46,yf-28,3.5),(1.0,32,3.5),RED,.04)
        for k in range(14): B.box((s*45,yf-56+k*4,2.6),(.05,1.2,2.2),M('#2A1E18',.9),0)
    B.box((0,yf-62,4.5),(44,1.2,4.5),RED,.04)
    B.box((0,yf-62.5,7),(7,1.6,7),RED,.04); B.box((0,yf-63.2,5.2),(3.2,.1,5.0),M('#2A1E18',.9),0)
    for k in range(6): B.box((0,yf-65-k*.6,.15+k*.3),(10-k*.4,.4,.15+k*.3),STONE,.02)
    # garden strips + trees + pool
    B.box((0,yf-26,.14),(2.5,9,.03),M('#5EB6E0',.1,emit=.15,spec=1.0),0); B.box((0,yf-26,.12),(2.8,9.3,.04),WHT,0)
    for s in (-1,1):
        for k in range(5): tree(s*40,yf-52+k*10,.12,1.1,k*7+s,palm=(k%2==0))
def skyline(seed=3,cx=0,cy=0,R_=90):
    """dense low city for aerial shots, around the masjid"""
    r=random.Random(seed)
    for i in range(520):
        a=r.uniform(0,2*pi); d=r.uniform(20,R_); x=cx+d*math.cos(a); y=cy+d*math.sin(a)
        if -50<x<50 and -45<y<45: continue
        w=r.uniform(4,9); dd=r.uniform(4,9); h=r.uniform(5,16); col=r.choice(BRICK+PLAST+PLAST)
        B.box((x,y,h/2),(w/2,dd/2,h/2),M(col,.85,kind='wall'),0)
        if r.random()<.35: B.cyl((x+r.uniform(-1,1),y+r.uniform(-1,1),h+.5),.5,1.0,M(r.choice(['#2B2C33','#E8E4D8','#3E6FB0']),.5),seg=10)
        if r.random()<.25: B.box((x,y,h+.35),(w/2,.06,.35),M(shade(col,.8),.8),0)
        if r.random()<.12: tree(x+w/2+1,y,0,r.uniform(1.2,1.8),i)
    B.box((0,0,-.06),(200,200,.05),M('#8E7A62',.95,kind='wall'),0)
def home():
    """haveli room: bedroom (x<1.5) + kitchen (x>2.5). back wall y=2.6, facing -y"""
    FLR=M('#C9B79C',.5,kind='tile',h2='#B8A486',sc=2.2); WALL=M('#7EC4BE',.85,kind='wall'); WALL2=M('#F0E2C4',.85,kind='wall'); WOOD=M('#6B4026',.6,kind='wood',sc=2)
    B.box((0,0,-.05),(7,3.5,.05),FLR,0); B.box((0,2.65,1.75),(7,.05,1.75),WALL,0); B.box((-4.3,0,1.75),(.05,3.5,1.75),WALL,0); B.box((0,0,3.55),(7,3.5,.05),M('#F4F1EA',.9),0)
    B.box((2.1,1.6,1.75),(.08,1.05,1.75),WALL2,.02); B.box((2.1,0.0,3.0),(.08,.55,.5),WALL2,.02)
    for x in (-4.2,): pass
    B.box((0,2.6,.15),(7,.04,.15),M('#2E6E6A',.7),0); B.box((0,2.6,2.6),(7,.03,.05),M('#E8C25A',.5),0)
    # bedroom: charpai bed, side table, ornate mirror, window jaali, poster, rug
    B.box((-3.0,1.6,.4),(1.0,.9,.06),WOOD,.03)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((-3.0+sx*.95,1.6+sy*.85,.2),.06,.4,WOOD,seg=8)
    B.box((-3.0,1.6,.5),(.95,.85,.06),M('#E8D8B8',.9,kind='fabric'),.03); B.box((-3.0,2.25,.62),(.6,.18,.1),M('#C9452E',.9,kind='fabric'),.05)
    B.box((-3.0,1.4,.58),(.9,.55,.05),M('#2E6E9E',.9,kind='fabric'),.04)
    B.box((-1.0,0.6,.012),(1.4,1.0,.012),M('#9E3B4E',.9,kind='fabric'),0); B.box((-1.0,0.6,.02),(1.2,.8,.012),M('#E8C25A',.9,kind='fabric'),0)
    B.box((-.2,2.58,1.75),(.62,.03,.82),M('#C9A24A',.35,metal=.7),.06)
    B.box((-1.9,2.6,1.9),(.6,.02,.7),M('#F2EDE2',.6),0)
    for i in range(6):
        for j in range(7): B.cyl((-2.3+i*.16,2.58,1.4+j*.15),.05,.02,M('#6B4026',.6),rot=(R(90),0,0),seg=6)
    B.box((-1.9,2.55,1.9),(.6,.01,.7),M('#FFF2D8',.3,emit=1.5),0)
    B.box((-3.8,1.0,.45),(.3,.3,.45),WOOD,.02); B.box((-3.8,1.0,.95),(.12,.12,.06),M('#C9CDD6',.3,metal=.8),.01)
    B.box((-4.24,0,2.1),(.01,.5,.6),M('#2E8B6E',.6),0); text('LAHORE',(-4.23,0,2.1),(1,0,0),.18,M('#F4F1EA',.4),ex=.004)
    B.box((-4.24,-1.4,1.0),(.02,.5,1.0),WOOD,.02)
    # kitchen: counter, stove with pot, steel utensils, shelf, gas cylinder, fridge
    B.box((4.6,2.25,.45),(2.2,.38,.45),M('#F4F1EA',.6),.02); B.box((4.6,2.25,.92),(2.25,.42,.03),M('#5A5F66',.25,metal=.3),.01)
    B.box((4.0,2.2,1.0),(.45,.25,.05),M('#2B2C33',.3,metal=.6),.01)
    for sx in (-.2,.2): B.cyl((4.0+sx,2.2,1.07),.13,.04,M('#1E1A18',.5),seg=12)
    B.cyl((3.8,2.2,1.2),.2,.25,M('#C9CDD6',.25,metal=.9),seg=18); B.cyl((4.2,2.2,1.14),.17,.12,M('#2B2C33',.4,metal=.6),seg=18)
    B.box((4.8,2.55,1.9),(1.5,.12,.03),WOOD,.01)
    for i in range(9): B.cyl((3.5+i*.33,2.5,2.05),.09,.25 if i%2 else .18,M('#C9CDD6',.25,metal=.9),seg=12)
    B.cyl((5.7,2.3,1.08),.11,.3,M('#F2EDE2',.4),seg=12)
    B.box((6.4,2.1,1.05),(.45,.45,1.05),M('#C2D8E0',.3,metal=.2),.04)
    B.cyl((5.5,1.8,.4),.22,.8,M('#C9302C',.4,metal=.3),seg=14)
    B.box((3.2,2.62,2.6),(.5,.02,.5),M('#F2EDE2',.6),0)
    mirror=obox((-.2,2.555,1.75),(.55,.005,.75),M('#C8D8E8',.03,metal=1.0,spec=1.0),0)
    B.done('home'); return mirror
