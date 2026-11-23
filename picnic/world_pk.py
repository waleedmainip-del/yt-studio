# ================================================================ PICNIC KARACHI — sets: jammed Karachi road, open jeep, Karachi United Stadium picnic (day/night), lanterns
def sign(body,loc,n,w,h,fg='#FFFFFF',bg=None,emit=0.0,ex=.012,border=None):
    nv=Vector(n).normalized(); L_=Vector(loc); ya=abs(nv.y)>.5
    if border: B.box(tuple(L_-nv*.012),(w/2+.06 if ya else .012, .012 if ya else w/2+.06, h/2+.06),M(border,.3,metal=.6),.005)
    if bg: B.box(tuple(L_),(w/2 if ya else .015, .015 if ya else w/2, h/2),M(bg,.6),.005)
    t=text(body,tuple(L_+nv*(.03+ex)),n,1.0,M(fg,.35,emit=emit),ex=ex); bpy.context.view_layer.update()
    dw,dh=t.dimensions.x,t.dimensions.y
    s=min(w*.9/max(dw,1e-3),h*.76/max(dh,1e-3)); t.scale=(s,s,1); return t
VS=1.9   # vehicles are scaled to the avatars (an avatar is ~1.95 tall and 1.7 wide)
def bigcar(x,y,col,rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz))); car(0,0,col,parent=e); e.scale=(VS,VS,VS); return e
def bigrick(x,y,rz=0,col='#2E8B6E'):
    e=rickshaw(x,y,rz,col); e.scale=(1.75,1.75,1.75); return e
def bigbike(x,y,rz=0,col='#C9302C'):
    e=bike(x,y,rz,col); e.scale=(1.8,1.8,1.8); return e
def citybus(x,y,rz=0,col='#C9302C',seed=1):
    r=random.Random(seed); e=empty((x,y,0),rot=(0,0,R(rz))); BD=M(col,.35,metal=.2); GL=M('#22303E',.08,spec=1.0); CH=M('#C9CDD6',.3,metal=.8)
    obox((0,0,2.5),(7.0,2.0,1.7),BD,.18,e); obox((0,0,3.2),(6.7,2.03,.55),GL,.05,e); obox((0,0,4.3),(7.05,2.05,.14),M('#F2C14E',.4),.06,e); obox((0,0,4.62),(5.6,1.6,.16),CH,.03,e)
    for k in range(12):
        c=r.choice(('#F2C14E','#2E8B57','#2E6E9E','#F4F1EA','#D63384','#E8742A'))
        for s in (-1,1): obox((-6.2+k*1.12,s*2.02,1.75),(.45,.02,.45),M(c,.4),.01,e)
    for s in (-1,1):
        obox((7.02,s*1.3,1.5),(.04,.38,.2),M('#FFF2C8',.3,emit=3),.01,e); obox((-7.02,s*1.3,1.6),(.04,.38,.2),M('#E8262A',.3,emit=2),.01,e)
        for k in range(9): obox((-5.6+k*1.4,s*2.04,3.2),(.04,.02,.55),BD,.0,e)
    obox((7.03,0,3.2),(.03,1.8,.55),M('#9FC7D8',.08,spec=1.0),.01,e); obox((7.1,0,1.0),(.12,2.0,.2),CH,.04,e)
    for sx in (-4.4,4.4):
        for sy in (-1,1): ocyl((sx,sy*1.85,.85),.85,.5,M('#111216',.8),e,rot=(R(90),0,0),seg=18); ocyl((sx,sy*2.1,.85),.45,.04,CH,e,rot=(R(90),0,0),seg=14)
    return e
def jeep(x,y,rz=90,col='#5A6B3A'):
    """open-top jeep sized for the avatars. local +x is forward... built along local X, then rotated by rz-90 so rz=90 faces world +x. seats: front (x=.75), back (x=-1.85), y=+-1.0, cushion top z=1.25"""
    e=empty((x,y,0),rot=(0,0,R(rz-90))); BD=M(col,.35,metal=.3); DK=M('#22242B',.6); ST=M('#3A2A1E',.7,kind='fabric'); CH=M('#C9CDD6',.3,metal=.8)
    obox((0,0,.62),(4.1,2.1,.14),DK,.04,e)                                   # floor
    obox((3.1,0,1.2),(1.15,2.05,.5),BD,.14,e); obox((4.22,0,1.05),(.1,1.5,.3),DK,.03,e)   # hood + grille
    for s in (-1,1):
        obox((.0,s*2.08,1.12),(3.0,.12,.5),BD,.06,e)                          # low doors/sides
        obox((4.25,s*1.45,1.22),(.06,.3,.22),M('#FFF2C8',.3,emit=4),.03,e); obox((-3.05,s*1.6,1.2),(.05,.25,.2),M('#E8262A',.3,emit=2),.02,e)
        obox((2.0,s*2.0,2.35),(.06,.06,.75),DK,.01,e)                          # windshield posts
        obox((-2.95,s*1.95,1.9),(.07,.07,1.3),DK,.02,e)                        # roll bar posts
        ocyl((2.1,s*2.42,1.75),.04,.5,DK,e,rot=(R(90),0,0),seg=8); obox((2.1,s*2.68,1.95),(.03,.16,.2),DK,.02,e)   # mirrors
    obox((-3.0,0,1.1),(.14,2.1,.52),BD,.06,e); obox((-2.95,0,3.15),(.07,2.0,.07),DK,.02,e)   # tailgate + roll bar top
    obox((2.0,0,3.07),(.06,2.05,.06),DK,.01,e); obox((2.0,0,1.68),(.06,2.05,.06),DK,.01,e); obox((2.0,0,2.38),(.015,1.95,.66),M('#BFD8E8',.05,spec=1.0,alpha=.22),0,e)
    obox((1.75,0,1.45),(.3,2.0,.22),DK,.08,e)                                 # dashboard
    ocyl((1.42,-1.0,1.72),.34,.06,DK,e,rot=(0,R(72),0),seg=18)                # steering wheel (right-hand drive)
    for sx in (.75,-1.85):
        for s in (-1,1):
            obox((sx,s*1.0,1.02),(.5,.82,.23),ST,.08,e); obox((sx-.52,s*1.0,1.55),(.12,.8,.42),ST,.08,e)
    obox((-3.3,0,1.3),(.2,.75,.75),DK,.2,e)                                    # spare wheel
    for sx in (-2.3,2.75):
        for sy in (-1,1): ocyl((sx,sy*2.05,.78),.78,.5,M('#111216',.8),e,rot=(R(90),0,0),seg=18); ocyl((sx,sy*2.31,.78),.42,.04,CH,e,rot=(R(90),0,0),seg=14)
    return e
JEEP_SEATS={'fr':(.75,-1.0),'fl':(.75,1.0),'br':(-1.85,-1.0),'bl':(-1.85,1.0)}   # jeep-local (x forward, y left); cushion top z=1.25

def tower(x,y,w,d,h,r,col,glass='#5E7FA0'):
    WALLm=M(col,.85,kind='wall'); B.box((x,y,h/2),(w/2,d/2,h/2),WALLm,.02)
    fl=int(h/3.4); nw=max(2,int(w/2.2)); sgn=-1 if y>0 else 1; yf=y+sgn*d/2
    for f in range(1,fl):
        for k in range(nw):
            wx=x-w/2+w*(k+.5)/nw
            B.box((wx,yf+sgn*.02,f*3.4+1.5),(w/nw*.34,.03,1.0),M(r.choice((glass,shade(glass,.8),shade(glass,1.15))),.12,spec=1.0),0)
            if r.random()<.22: B.box((wx,yf+sgn*.3,f*3.4+.55),(.38,.26,.24),M('#D8DEE6',.4),.03)
        B.box((x,yf+sgn*.1,f*3.4+.1),(w/2+.05,.14,.08),M(shade(col,.8),.85),.01)
    B.box((x,y,h+.3),(w/2+.1,d/2+.1,.3),M(shade(col,.75),.85),.02)
    if r.random()<.6: B.cyl((x+r.uniform(-w/4,w/4),y,h+1.6),.7,2.0,M('#3E4450',.5),seg=10)
def road(seed=5):
    """Jammed 4-lane one-way Karachi road along +x. Lanes at y=-7.5,-2.5,2.5,7.5. Hero jeep slot: lane y=-2.5, x=0. Returns list of (obj,x0,lane,phase) for creeping traffic."""
    r=random.Random(seed); ASP=M('#3F4148',.9,kind='asphalt'); SW=M('#B8B0A0',.85,kind='concrete',sc=.8)
    B.box((0,0,-.05),(150,10.2,.05),ASP,0)
    for ly in (-5,0,5):
        for k in range(-36,37): B.box((k*4.0,ly,.006),(1.1,.09,.004),M('#E8E4D8',.7),0)
    for s in (-1,1):
        B.box((0,s*12.6,.11),(150,2.4,.11),SW,.01); B.box((0,s*10.3,.13),(150,.14,.13),M('#D8C24A' if s<0 else '#2B2C33',.7),.01)
    # buildings with ground-floor shops
    names=['CLIFTON MOBILES','BOAT BASIN BBQ','TARIQ ROAD FABRICS','SADDAR ELECTRONICS','KARACHI BAKERS','SEA BREEZE PHARMACY','ZAMZAMA TAILORS','BURNS ROAD NIHARI','DEFENCE MOTORS','GULSHAN SWEETS','NAZIMABAD BOOKS','KORANGI TYRES']
    cols=['#D8CDB8','#C9BFAE','#E0D6C4','#BFC6CC','#D6C8B4','#C8D0C8','#E4DCCB']; scol=['#1F5A7A','#8E2A3A','#2E6E4A','#5A3A8A','#B05A1E','#22303E','#7A1E4A','#1F6E6E']
    for s in (-1,1):
        x=-150.0; i=0
        while x<150:
            w=r.uniform(11,18); h=r.uniform(14,34); d=r.uniform(10,14); yc=s*(14.8+d/2)
            tower(x+w/2,yc,w-.6,d,h,r,r.choice(cols),glass=r.choice(('#5E7FA0','#6E8A8A','#4A6A8A')))
            yf=s*14.8; nrm=-s
            B.box((x+w/2,yf+nrm*.05,1.7),(w/2-.6,.05,1.5),M('#2A2420',.9),0)
            sign(names[(i+(0 if s<0 else 5))%len(names)],(x+w/2,yf+nrm*.3,3.9),(0,nrm,0),w-2.0,1.0,fg='#FFFFFF',bg=scol[(i+(2 if s>0 else 0))%len(scol)],emit=.4,border='#C9A24A')
            B.box((x+w/2,yf+nrm*.9,3.2),(w/2-.5,.9,.05),M(r.choice(('#B03A2E','#1F5A7A','#2E6E4A','#C98A2A')),.85,kind='fabric'),.02,rot=(R(-9*nrm),0,0))
            for k in range(int(w/1.6)): B.box((x+1.0+k*1.6,yf+nrm*.5,.55+.15*r.random()),(.5,.35,.5),M(r.choice(('#C9302C','#2E6E9E','#F2C14E','#2E8B57','#E8742A','#F4F1EA','#6B4A2A')),.7),.03)
            x+=w; i+=1
    # sidewalk life: palms, poles, wires, hoardings
    for s in (-1,1):
        for k in range(-14,15):
            tree(k*10+3.5*s,s*11.9,.22,1.9,seed+k,palm=True)
            if k%2==0:
                B.cyl((k*10-2,s*11.0,4.5),.12,9.0,M('#6A6F78',.5,metal=.4),seg=8); B.box((k*10-2,s*9.6,8.9),(.1,1.5,.07),M('#6A6F78',.5),.0); B.box((k*10-2,s*8.3,8.8),(.3,.5,.08),M('#FFF2D8',.3,emit=.6),.03)
        wires(-150,150,s*11.0,s*11.0-.01,8.2,0,seed)
    for k in range(-14,14):
        for s in (-1,1):
            pa=(k*20-2,s*11.0,8.3); pb=(k*20+18,s*11.0,8.3)
            for q in range(8):
                f0=q/8; f1=(q+1)/8; z0=8.3-1.2*4*f0*(1-f0); z1=8.3-1.2*4*f1*(1-f1); seg((L(pa[0],pb[0],f0),pa[1],z0),(L(pa[0],pb[0],f1),pa[1],z1),.02,M('#1A1A1E',.6),sides=4)
    # big hoardings facing the oncoming traffic (-x), readable from the jam
    for (bx,by,txt,c) in ((46,-13.2,'MEGA SALE','#C9302C'),(88,13.2,'CHAI TIME','#2E6E4A')):
        B.cyl((bx,by,5.5),.2,11,M('#5A5F66',.5,metal=.4),seg=8); B.box((bx,by,12.2),(.14,4.4,2.1),M(c,.5),.03)
        sign(txt,(bx-.16,by,12.2),(-1,0,0),8.0,3.2,fg='#FFFFFF',emit=.5)
    # flyover crossing far ahead + signal gantry
    B.box((112,0,9.0),(5.5,60,.6),M('#B8B4AA',.85,kind='concrete'),.05); B.box((106.6,0,10.0),(.2,60,.5),M('#A8A49A',.85),.02); B.box((117.4,0,10.0),(.2,60,.5),M('#A8A49A',.85),.02)
    for py in (-30,-11.5,11.5,30): B.box((112,py,4.2),(1.3,1.3,4.2),M('#A8A49A',.85,kind='concrete'),.08)
    for py in (-11.2,11.2): B.cyl((36,py,4.2),.18,8.4,M('#5A5F66',.5,metal=.4),seg=8)
    B.box((36,0,8.3),(.16,11.3,.16),M('#5A5F66',.5,metal=.4),.02)
    for ly in (-7.5,-2.5,2.5,7.5):
        B.box((35.8,ly,7.5),(.2,.36,.85),M('#22242B',.5),.05); B.box((35.58,ly,8.0),(.03,.2,.2),M('#FF3B30',.3,emit=9),.08); B.box((35.58,ly,7.5),(.03,.2,.2),M('#4A3A10',.5),.08); B.box((35.58,ly,7.0),(.03,.2,.2),M('#123A1E',.5),.08)
    B.box((0,0,-.3),(260,200,.1),M('#8A8274',.95),0)
    for k in range(40):
        xx=r.uniform(-200,220); yy=r.choice((-1,1))*r.uniform(34,90); h=r.uniform(14,46); B.box((xx,yy,h/2),(r.uniform(5,9),r.uniform(5,9),h/2),M(r.choice(('#C9C2B4','#B8B8B8','#D6CEBE','#A8B0B8')),.95,kind='wall'),0)
    B.done('road')
    # traffic
    CC=['#F4F4F2','#C9CDD6','#22242B','#8E2A3A','#2E5A8A','#D8D2C0','#5A6170','#F4F4F2','#C9CDD6']; V=[]
    for li,ly in enumerate((-7.5,-2.5,2.5,7.5)):
        x=-118.0+r.uniform(0,3)
        while x<100:
            kind=r.choice(('car','car','car','car','bus','rick','rick','bikes')); ln={'car':8.6,'bus':14.2,'rick':4.2,'bikes':3.8}[kind]; xc=x+ln/2
            if ly==-2.5 and abs(xc)<ln/2+5.6: x=5.6+r.uniform(.8,1.4); continue
            if kind=='car': o=bigcar(xc,ly+r.uniform(-.25,.25),r.choice(CC),0)
            elif kind=='bus': o=citybus(xc,ly,0,r.choice(('#C9302C','#2E6E9E','#2E8B57','#E8742A')),seed=int(x*7))
            elif kind=='rick': o=bigrick(xc,ly+r.uniform(-.8,.8),0,r.choice(('#2E8B6E','#2E6E9E','#C9A24A','#1F6E6E')))
            else: o=bigbike(xc,ly-1.2,0,r.choice(('#C9302C','#22242B','#2E5A8A'))); bigbike(xc+.6,ly+1.3,0,'#C9302C')
            V.append((o,o.location[0],li,r.uniform(0,6))); x+=ln+r.uniform(.9,1.8)
    return V

# ---------------------------------------------------------------- venue
PAST=['#F2B8C6','#BFE0D6','#F7E3A1','#C9D8F0','#F4C9A8','#D9C8F0','#E3EEC2','#F0D0D0','#B8E0F0','#FFF6E8','#E8A0A0','#9FD0C0']
CLO=['#C9302C','#2E6E9E','#F2C14E','#2E8B57','#8E2A6A','#E8742A','#F4F1EA','#1F8A8A','#D63384','#5A3A8A','#3E5A7A','#22242B','#E8DCC0','#6C5FB0']
SKN=['#D6A07A','#C68A5E','#B9835C','#A8714A','#E0AA80','#9A6A48']; HAIRS=['#14110F','#1E1A18','#2A1E16','#3A2A1E']
MAT_W=2.3; MAT_D=1.75
def mat_xy(i,j,side): return (side*(7.0+6.2*i), 14.0+5.3*j)
def picnic_mat(x,y,r,rot=0.0,props=True):
    c=r.choice(PAST); c2=shade(c,.82)
    B.box((x,y,.03),(MAT_W,MAT_D,.025),M(c,.9,kind='fabric'),.01,rot=(0,0,rot))
    for k in (-1.5,-.5,.5,1.5): B.box((x+k*MAT_W/2*math.cos(rot),y+k*MAT_W/2*math.sin(rot),.058),(.07,MAT_D,.004),M(c2,.9,kind='fabric'),0,rot=(0,0,rot))
    if props:
        ca,sa=math.cos(rot),math.sin(rot)
        def P(dx,dy): return (x+dx*ca-dy*sa,y+dx*sa+dy*ca)
        px,py=P(r.uniform(-.3,.3),r.uniform(-.2,.2)); B.box((px,py,.2),(.34,.26,.15),M('#B8905A',.7,kind='wood'),.04,rot=(0,0,rot)); B.box((px,py,.37),(.36,.03,.03),M('#8A6A3A',.7),.01,rot=(0,0,rot))
        for k in range(2):
            qx,qy=P(r.choice((-1,1))*r.uniform(1.3,1.9),r.choice((-1,1))*r.uniform(.9,1.4)); B.box((qx,qy,.16),(.3,.3,.11),M(r.choice(PAST),.9,kind='fabric'),.09,rot=(0,0,r.uniform(0,3)))
def far_person(x,y,rz,r):
    """cheap seated figure for distant mats (boxes only)"""
    ca,sa=math.cos(rz),math.sin(rz); top=M(r.choice(CLO),.85); sk=M(r.choice(SKN),.6); hr=M(r.choice(HAIRS),.6); pt=M(r.choice(('#22242B','#3B4F78','#E8DCC0','#5A6170','#2F3440')),.85)
    fx,fy=sa,-ca
    B.box((x,y,.72),(.42,.21,.42),top,0,rot=(0,0,rz)); B.box((x,y,1.42),(.27,.27,.27),sk,0,rot=(0,0,rz)); B.box((x-fx*.06,y-fy*.06,1.62),(.29,.26,.12),hr,0,rot=(0,0,rz))
    B.box((x+fx*.45,y+fy*.45,.2),(.4,.42,.14),pt,0,rot=(0,0,rz))
    for s in (-1,1): B.box((x+ca*s*.55,y+sa*s*.55,.62),(.11,.12,.4),top,0,rot=(0,0,rz))
def lantern_geo(x,y,z,s=1.0,lit=True):
    PAP=M('#FFC978',.5,emit=4.2 if lit else 0.0); B.box((x,y,z),(.26*s,.26*s,.34*s),PAP,0); B.box((x,y,z+.345*s),(.2*s,.2*s,.02*s),M('#E8A04A',.5,emit=1.5 if lit else 0),0)
    if lit: B.box((x,y,z-.3*s),(.07*s,.07*s,.06*s),M('#FFF2C8',.3,emit=16),0)
def venue(night=False,seed=11,dusk=False):
    """Karachi United Stadium picnic. Gate at y=0 facing -y, central aisle x=0 (7 wide) running +y. 520 mats: 10 cols each side x 26 rows. DJ stage y~158. 10 activity tents along x=+74.
    returns dict(det=[(x,y,rot)] mats reserved for detailed people, hero=(x,y), bulbs)"""
    r=random.Random(seed); lit=night or dusk
    GR=M('#5E9E4A',.95,kind='grass',h2='#4E8A3E'); B.box((0,80,-.05),(96,100,.05),GR,0)
    for k in range(-9,10): B.box((k*10,80,.004),(5,100,.003),M('#66A852' if k%2 else '#578F45',.95,kind='grass'),0)
    WH=M('#F2F2EC',.8)
    for (cx,cy,hx,hy) in ((0,80,82,.09),(0,6,82,.09),(0,170,82,.09),(-82,88,.09,82),(82,88,.09,82)): B.box((cx,cy,.008),(hx,hy,.004),WH,0)
    B.box((0,-6,-.03),(96,14,.05),M('#B8AE9A',.9,kind='concrete',sc=1.2),0)             # forecourt
    B.box((0,84,.012),(3.5,84,.008),M('#D8CBB0',.9,kind='concrete',sc=.7),0)                # central aisle path
    # perimeter: wall, west bleachers, floodlights, trees, skyline
    WALLm=M('#D9D2C4',.85,kind='wall')
    for (cx,cy,hx,hy) in ((-52,0,43,.3),(52,0,43,.3),(0,178,96,.3),(96,89,.3,89)): B.box((cx,cy,1.5),(hx,hy,1.5),WALLm,.03)
    for k in range(9):
        B.box((-90-k*1.1,88,.5+k*.55),(.6,78,.5+k*.55),M('#C8CDD4',.8,kind='concrete',sc=1.5),.02)
        for q in range(-12,13): B.box((-90-k*1.1,88+q*6,1.08+k*1.1),(.5,2.6,.06),M(('#2E6E9E','#C9302C','#F2C14E')[(q+k)%3],.6),.02)
    B.box((-101,88,6.8),(.3,78,6.8),WALLm,.03); B.box((-95,88,12.4),(6.5,78,.18),M('#E8E8E4',.6),.02,rot=(0,R(-6),0))
    for kx in range(-10,11,5): B.cyl((-89.2,88+kx*7,6.2),.14,12.4,M('#8A8F99',.4,metal=.6),seg=8)
    for (fx,fy) in ((-88,2),(88,2),(-88,176),(88,176)):
        B.cyl((fx,fy,15),.45,30,M('#8A8F99',.4,metal=.6),seg=10); B.box((fx,fy,30.5),(2.6,.35,1.6),M('#3A3E48',.5),.05)
        for a in range(4):
            for b_ in range(3): B.box((fx-1.9+a*1.27,fy+(-.4 if fy<50 else .4),29.3+b_*1.1),(.42,.06,.4),M('#FFF6DC',.3,emit=7.0 if lit else .6),.05)
    for k in range(34):
        tx=-96+k*5.9; tree(tx,-.9+r.uniform(-.3,.3),0,r.uniform(1.6,2.1),seed+k,palm=(k%3==0)) if abs(tx)>9 else None
        tree(99.5,k*5.4,0,r.uniform(1.7,2.3),seed+100+k,palm=(k%4==1)); tree(-96+k*5.9,181,0,r.uniform(1.8,2.6),seed+200+k,palm=(k%3==1))
    for k in range(46):
        a=r.uniform(0,2*pi); d=r.uniform(150,260); xx=math.cos(a)*d; yy=88+math.sin(a)*d; h=r.uniform(18,70)
        B.box((xx,yy,h/2),(r.uniform(6,11),r.uniform(6,11),h/2),M(r.choice(('#C9C2B4','#B8BCC4','#D6CEBE','#A8B0B8','#BFC8D0')),.95,kind='wall',emit=0),0)
        if lit:
            for q in range(int(h/5)): B.box((xx,yy-math.copysign(1,yy-88)*0,h*.15+q*4.2),(r.uniform(2,5),r.uniform(6.1,11.1),.5),M('#FFD890',.5,emit=1.4),0)
    # gate
    GP=M('#2E5A8A',.5);
    for s in (-1,1): B.box((s*8.2,-.2,3.9),(1.0,.9,3.9),M('#F2EFE6',.8,kind='wall'),.08); B.box((s*8.2,-.2,7.95),(1.25,1.15,.18),GP,.04)
    B.box((0,-.2,8.9),(9.4,.7,1.05),GP,.08)
    sign('KARACHI UNITED STADIUM',(0,-.95,8.9),(0,-1,0),13.6,1.3,fg='#FFFFFF',emit=.6 if lit else .2)
    B.box((0,-.5,5.55),(3.3,.06,1.55),M('#69C0E3',.6,emit=.5 if lit else 0),.03); img_plane(LOGO,(0,-.58,5.55),6.4,2.87,(0,-1,0),emit=.9 if lit else .0)
    for s in (-1,1): B.cyl((s*3.0,-.5,7.0),.03,1.0,M('#8A8F99',.4),seg=6)
    for s in (-1,1):
        B.box((s*13.5,-3.4,1.5),(1.6,1.3,1.5),M('#F4F1EA',.8,kind='wall'),.06); B.box((s*13.5,-4.75,1.75),(1.2,.06,.55),M('#22303E',.08,spec=1.0),.02); B.box((s*13.5,-3.4,3.2),(1.9,1.6,.14),GP,.05)
    # bunting over aisle + festoon poles
    FL=['#E8556A','#F2C14E','#4FB3A5','#5B8DEF','#F28C4E','#B56AD8']; bulbs=[]
    for k in range(27):
        yy=10+k*6.0
        for s in (-1,1):
            B.cyl((s*3.9,yy,2.4),.07,4.8,M('#6B4A2A',.6,kind='wood'),seg=8)
            if k<26:
                for q in range(6):
                    f=(q+.5)/6; zz=4.7-.55*4*f*(1-f); B.ico((s*3.9,yy+6.0*f,zz),.13,M('#FFE2A0',.3,emit=9.0 if lit else .8),sub=1)
                    seg((s*3.9,yy+6.0*q/6,4.7-.55*4*(q/6)*(1-q/6)),(s*3.9,yy+6.0*(q+1)/6,4.7-.55*4*((q+1)/6)*(1-(q+1)/6)),.012,M('#1A1A1E',.6),sides=4)
        if k%2==0:
            for q in range(11):
                f=(q+.5)/11; xx=-3.9+7.8*f; zz=4.75-.5*4*f*(1-f); c=M(FL[(q+k)%6],.8,kind='fabric')
                B.poly([(xx-.3,yy,zz),(xx+.3,yy,zz),(xx,yy,zz-.55)],c); B.poly([(xx+.3,yy+.001,zz),(xx-.3,yy+.001,zz),(xx,yy+.001,zz-.55)],c)
    # mats + people
    det=[]; hero=mat_xy(0,3,-1)
    for side in (-1,1):
        for i in range(10):
            for j in range(26):
                x,y=mat_xy(i,j,side); rot=r.uniform(-.12,.12); x+=r.uniform(-.35,.35); y+=r.uniform(-.3,.3)
                if (side,i,j)==(-1,0,3): picnic_mat(hero[0],hero[1],r,0.0,props=False); continue
                picnic_mat(x,y,r,rot)
                if i<=1 and 1<=j<=6 and (i+j+(side>0))%1==0 and not (i==1 and j%2==0): det.append((x,y,rot,side,i,j)); continue
                if r.random()<.1: continue
                n=r.choice((2,2,3,3,4)); a0=r.uniform(0,6.28)
                for q in range(n):
                    a=a0+q*2*pi/n+r.uniform(-.3,.3); px=x+math.cos(a)*1.25; py=y+math.sin(a)*.95; far_person(px,py,math.atan2(x-px,-(y-py)),r)
                if lit and r.random()<.75: lantern_geo(x+r.uniform(-.5,.5),y+r.uniform(-.4,.4),.42,1.0,lit=True)
    # DJ stage
    SY=158; DKm=M('#22242B',.5)
    B.box((0,SY+3,.7),(11,5,.7),M('#3A3E48',.6),.05); B.box((0,SY+7.6,4.6),(10.5,.3,3.2),DKm,.03)
    for a in range(9):
        for b_ in range(4): B.box((-8.4+a*2.1,SY+7.25,2.6+b_*1.35),(.9,.05,.55),M(FL[(a+b_)%6],.4,emit=3.2 if lit else 1.2),.04)
    for s in (-1,1):
        B.cyl((s*10.6,SY-.5,4.6),.18,9.2,M('#8A8F99',.3,metal=.8),seg=8);
        for b_ in range(3): B.box((s*9.0,SY-.6,2.0+b_*1.5),(1.0,.9,.72),DKm,.06); B.cyl((s*9.0,SY-1.52,2.0+b_*1.5),.5,.06,M('#3A3E48',.4),rot=(R(90),0,0),seg=18)
    B.box((0,SY-.5,9.2),(10.8,.2,.2),M('#8A8F99',.3,metal=.8),.02)
    for a in range(7): B.box((-7.5+a*2.5,SY-.5,8.85),(.3,.3,.3),DKm,.06); B.box((-7.5+a*2.5,SY-.72,8.7),(.2,.04,.2),M(FL[a%6],.3,emit=8 if lit else 2),.04)
    img_plane(LOGO,(0,SY+7.2,6.6),7.6,3.4,(0,-1,0),emit=1.6 if lit else .6)
    B.box((0,SY+.2,2.05),(2.6,.8,.65),DKm,.05); B.box((0,SY-.62,2.05),(2.5,.03,.5),M('#5B8DEF',.4,emit=2.2 if lit else .8),.02)
    for s in (-1,1): B.cyl((s*1.1,SY+.2,2.76),.42,.08,M('#111216',.4),seg=20); B.cyl((s*1.1,SY+.2,2.81),.14,.02,M('#C9302C',.4),seg=12)
    B.box((0,SY+.2,2.78),(.5,.4,.06),M('#3A3E48',.4),.02)
    # activity vendors: 10 plain tents (no specific activities shown)
    TC=['#E8556A','#F2C14E','#4FB3A5','#5B8DEF','#F28C4E','#B56AD8','#E8556A','#4FB3A5','#F2C14E','#5B8DEF']
    for k in range(10):
        ty=22+k*13.0; tx=75.0; c=M(TC[k],.85,kind='fabric'); WHm=M('#F7F3EA',.85,kind='fabric')
        for (dx,dy) in ((-3.4,-3.6),(-3.4,3.6),(3.4,-3.6),(3.4,3.6)): B.cyl((tx+dx,ty+dy,1.7),.07,3.4,M('#E8E8E4',.4,metal=.5),seg=8)
        B.box((tx,ty,3.45),(3.7,3.9,.07),c,.03); B.cyl((tx,ty,4.3),5.1,1.6,WHm if k%2 else c,seg=4,r2=.2,rot=(0,0,R(45)))
        B.box((tx-2.6,ty,1.0),(.75,3.0,.05),M('#B8905A',.6,kind='wood'),.03); B.box((tx-2.6,ty,.5),(.7,2.9,.48),WHm,.02)
        for q in range(8):
            f=(q+.5)/8; B.poly([(tx-3.42,ty-3.6+7.2*f-.3,3.35),(tx-3.42,ty-3.6+7.2*f+.3,3.35),(tx-3.42,ty-3.6+7.2*f,2.85)],M(FL[(q+k)%6],.8,kind='fabric'))
        if lit: B.ico((tx-1.5,ty,3.1),.2,M('#FFE2A0',.3,emit=9),sub=1)
    B.box((0,88,-.3),(400,400,.1),M('#8A8274',.95),0)
    B.done('venue')
    return dict(det=det,hero=hero,SY=SY)
def lantern_groups(n=1000,seed=3,groups=25):
    """n sky lanterns in `groups` rigid clusters (each cluster rises/sways as one object). returns [(obj,phase,speed,sway)]"""
    r=random.Random(seed); out=[]; per=n//groups
    for g in range(groups):
        for k in range(per):
            lantern_geo(r.uniform(-78,78),r.uniform(8,172),r.uniform(0,62),r.uniform(.9,1.5),lit=True)
        e=empty((0,0,0))
        for o in B.done('lan%d'%g): o.parent=e
        out.append((e,r.uniform(0,6.28),r.uniform(.55,1.15),r.uniform(.6,1.8)))
    return out
def lantern_obj(s=1.0):
    e=empty((0,0,0)); obox((0,0,0),(.26*s,.26*s,.34*s),M('#FFC978',.5,emit=4.2),.02,e); obox((0,0,.345*s),(.2*s,.2*s,.02*s),M('#E8A04A',.5,emit=1.5),.01,e); obox((0,0,-.3*s),(.07*s,.07*s,.06*s),M('#FFF2C8',.3,emit=16),.02,e); return e
LOGO='/home/claude/picnic/logo_crop.jpg'
_IM={}
def img_mat(path,emit=0.0):
    k=(path,emit)
    if k in _IM: return _IM[k]
    m=bpy.data.materials.new('img'); m.use_nodes=True; nt=m.node_tree; b=nt.nodes['Principled BSDF']; t=nt.nodes.new('ShaderNodeTexImage'); t.image=bpy.data.images.load(path,check_existing=True)
    nt.links.new(t.outputs['Color'],b.inputs['Base Color']); b.inputs['Roughness'].default_value=.6
    if emit:
        nt.links.new(t.outputs['Color'],b.inputs['Emission']); b.inputs['Emission Strength'].default_value=emit
    _IM[k]=m; return m
def img_plane(path,loc,w,h,n=(0,-1,0),emit=0.0,parent=None):
    me=bpy.data.meshes.new('ip'); me.from_pydata([(-w/2,0,-h/2),(w/2,0,-h/2),(w/2,0,h/2),(-w/2,0,h/2)],[],[(0,1,2,3)]); uv=me.uv_layers.new(name='uv')
    for i,c in enumerate(((0,0),(1,0),(1,1),(0,1))): uv.data[i].uv=c
    o=bpy.data.objects.new('ip',me); o.location=loc; o.rotation_euler=(0,0,math.atan2(n[0],-n[1])); _col.objects.link(o); me.materials.append(img_mat(path,emit))
    if parent: o.parent=parent
    return o
def studio():
    B.box((0,0,-.05),(30,30,.05),M('#E9E6DF',.9),0); B.box((0,6,6),(30,.2,6),M('#E9E6DF',.9),0); B.done('studio')
