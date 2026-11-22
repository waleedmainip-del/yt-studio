# Sets for "Faisalabad: The Textile Kingdom": Clock Tower cloth bazaar (8-bazaar style lane, fabric drapes, banners),
# Rashid Cloth House interior (thaan shelves, counter, fan), Bilal's rooftop shoot (tank, laundry, kites),
# power-loom mill hall (moving looms), Instagram phone UI.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
FAB=['#C8372D','#2B5AA8','#F2C14E','#2B8A5A','#7448C2','#E8709A','#F28A3A','#16909E','#F4F1EA','#8A2A4A','#D9B24A','#3A6A8A']
def thaan(loc,col,parent=None,rot=(0,0,0),l=.9):
    # folded cloth bolt
    return obox(loc,(l/2,.22,.08),M(col,.9,kind='fabric',h2=shade(col,.82),sc=5),.04,parent,rot=rot)
def drape(x,y,z,col,h=2.2,s=1):
    B.box((x,y,z-h/2),(.28,.02,h/2),M(col,.9,kind='fabric',h2=shade(col,.8),sc=3),.01)
    B.cyl((x,y,z),.03,.7,M('#5A3A22',.6,kind='wood'),rot=(0,R(90),0),seg=6)
def clock_tower(x,y,s=1.0):
    st=M('#C8703F',.85,kind='wall',h2='#B05E32',sc=1.2); tr=M('#F2D8B0',.7); dk=M('#16171C',.4)
    B.box((x,y,2.0*s),(2.2*s,2.2*s,2.0*s),st,.05); B.box((x,y,4.1*s),(2.4*s,2.4*s,.15*s),tr,.04)
    B.box((x,y,8.0*s),(1.7*s,1.7*s,3.8*s),st,.05)
    for k in range(3): B.box((x,y-1.72*s,5.3*s+k*1.6*s),(.35*s,.04,.5*s),M('#2A2C34',.3,spec=.8),.02)
    B.box((x,y,12.1*s),(2.0*s,2.0*s,.3*s),tr,.05); B.box((x,y,13.4*s),(1.8*s,1.8*s,1.0*s),st,.05)
    B.ico((x,y,15.0*s),1.5*s,M('#F2E6D2',.6),sc=(1,1,1.05),sub=2); B.cyl((x,y,16.8*s),.05*s,.8*s,M('#D9B24A',.3,metal=.8),seg=6)
    for dx in (-1.6,1.6):
        for dy in (-1.6,1.6): B.box((x+dx*s,y+dy*s,13.7*s),(.18*s,.18*s,.9*s),tr,.04); B.ico((x+dx*s,y+dy*s,14.75*s),.3*s,tr,sub=1)
    hands=[]
    for (nx,ny) in ((0,-1),(0,1),(-1,0),(1,0)):
        cx,cy=x+nx*1.82*s,y+ny*1.82*s; rz=math.atan2(nx,-ny)
        e=empty((cx,cy,13.4*s),rot=(0,0,rz)); ocyl((0,0,0),.75*s,.06,M('#FFF8E8',.5,emit=.4),e,rot=(R(90),0,0),seg=28); ocyl((0,.02,0),.82*s,.04,M('#D9B24A',.3,metal=.7),e,rot=(R(90),0,0),seg=28)
        for k in range(12): a=k*pi/6; obox((math.sin(a)*.62*s,-.05,math.cos(a)*.62*s),(.03,.01,.07),dk,0,e,rot=(0,a,0))
        h1=empty((0,-.07,0),e); obox((0,0,.2*s),(.04,.01,.22*s),dk,0,h1); h2=empty((0,-.09,0),e); obox((0,0,.3*s),(.03,.01,.32*s),dk,0,h2); hands.append((h1,h2))
    return hands
def set_clock(hands,hh,mm):
    for h1,h2 in hands: h1.rotation_euler[1]=R((hh%12)*30+mm*.5); h2.rotation_euler[1]=R(mm*6)
def banner_x(x,z,col,txt=None):
    B.box((x,0,z),(.06,3.4,.35),M(col,.85,kind='fabric'),.01,rot=(R(4),0,0))
    if txt:
        for s in (-1,1): stext(txt,(x+s*.07,0,z),.22,'#FFFFFF',n=(s,0,0),e=.2)
def bazaar_ft(seed=8):
    r=random.Random(seed)
    B.box((0,0,-.05),(60,3.5,.05),M('#9A5A3A',.85,kind='tile',h2='#7E4630',sc=3.5),0)
    for s in (-1,1): B.box((0,s*3.35,.08),(60,.15,.08),M('#8A8E96',.8,kind='asphalt'),0)
    cols=['#E8C07A','#D98A5A','#C9B48A','#E8D8B0','#B8634A','#D9A06A','#F0E0C0']; scols=['#7A1F1F','#1F4D3A','#2B3A7A','#6A2A6A','#8A5A10']
    north=['MADINA LAWN','KHADDAR HOUSE',None,'BOSKI CENTRE','AL-NOOR TEXTILE','RESHAM GALI']; south=['CHUNRI MAHAL','DUPATTA KING',None,'SILK PALACE','COTTON CORNER','SHAHI KAPRA']
    xs=[-27,-19.5,-6.5,6.5,15,22.5]
    for i,x in enumerate(xs):
        w=6.6 if abs(x)>6 else 6.0
        facade(x,w,r.randint(2,3),r.choice(cols),north[i] or 'RESHAM HOUSE',r.choice(scols),seed*10+i,1,Y=3.5)
        facade(x,w,r.randint(2,3),r.choice(cols),south[i] or 'NEW LAWN HOUSE',r.choice(scols),seed*20+i,-1,Y=3.5)
    facade(0,6.4,3,'#E8D8B0','RASHID CLOTH HOUSE','#1F4D3A',seed*7,1,Y=3.5)
    facade(0,6.4,3,'#D9A06A','SALEEM CLOTH CENTRE','#7A1F1F',seed*9,-1,Y=3.5)
    # cloth drapes hanging in front of shops
    for s in (-1,1):
        for x in range(-29,30,2):
            if abs(x)<4: continue
            drape(x+r.uniform(-.3,.3),s*3.05,2.9,r.choice(FAB),h=r.uniform(1.6,2.3))
    for x in (-24,-14,-8,9,18):
        banner_x(x,4.6,r.choice(['#C8372D','#2B8A5A','#2B5AA8','#7448C2']),r.choice(['SALE','50% OFF','NEW LAWN','EID SALE']))
    wires(-30,30,-3.4,3.4,5.6,6,seed)
    hands=clock_tower(34,0,1.0)
    # carts with cloth rolls + bikes
    for (x,y,rz) in ((-11,-1.8,0),(12,1.9,0)):
        e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#7A5236',.6,kind='wood'); obox((0,0,.7),(1.0,.55,.05),wd,.02,e)
        for dx in (-.6,.6): ocyl((dx,-.58,.35),.32,.06,M('#3A2A1E',.6),e,rot=(R(90),0,0),seg=14); ocyl((dx,.58,.35),.32,.06,M('#3A2A1E',.6),e,rot=(R(90),0,0),seg=14)
        for k in range(6): ocyl((-.7+.28*k,0,.9+.08*(k%2)),.13,1.0,M(r.choice(FAB),.9,kind='fabric'),e,rot=(R(90),0,0),seg=12)
    motorbike((-4,-2.4,0),0,'#C8372D'); motorbike((8,2.5,0),180,'#16171C')
    for x in (-16,4): pole(x,3.2,7.5)
    return hands
def ifg_banner(loc=(0,3.2,4.6)):
    e=empty(loc); obox((0,.04,0),(2.9,.04,.5),M('#16171C',.4),.06,e); obox((0,0,0),(2.82,.02,.43),M('#16171C',.4),.03,e)
    t=text('INTERNATIONAL FASHION GROUP',(0,-.03,-.02),(0,-1,0),.3,M('#F2C14E',.3,emit=1.6),ex=.02,parent=e)
    for dx in (-2.75,2.75): oico((dx,-.05,0),.09,M('#F2C14E',.3,emit=2),e,sub=1)
    return e
def global_banner(loc=(0,-3.2,5.0)):
    e=empty(loc,rot=(0,0,R(180))); obox((0,.04,0),(3.6,.05,.75),M('#7A1F1F',.4),.06,e)
    text('GLOBAL',(0,-.04,.32),(0,-1,0),.34,M('#FFFFFF',.3,emit=1.6),ex=.02,parent=e)
    text('INTERNATIONAL FASHION GROUP',(0,-.04,-.25),(0,-1,0),.34,M('#F2C14E',.3,emit=1.6),ex=.02,parent=e)
    for dx in (-3.45,3.45):
        for dz in (-.6,.6): oico((dx,-.06,dz),.08,M('#FFF3B0',.3,emit=2.5),e,sub=1)
    return e
# ---------------------------------------------------------------- shop interior
def shop_int():
    fl=M('#D8CCB8',.4,kind='tile',h2='#C8BCA8',sc=1.0,spec=.7); wl=M('#E8E0C8',.9,kind='wall'); wd=M('#6A3A22',.55,kind='wood',sc=.8); r=random.Random(5)
    W_,D_=3.6,3.4
    B.box((0,0,-.05),(W_+2,D_+6,.05),fl,0); B.box((0,0,3.3),(W_,D_,.05),M('#F4F1EA',.9),0)
    B.box((0,D_,1.65),(W_,.1,1.65),wl,0); B.box((-W_,0,1.65),(.1,D_,1.65),wl,0); B.box((W_,0,1.65),(.1,D_,1.65),wl,0)
    # back shelves stacked with thaans (floor to ceiling)
    for x0 in (-2.4,0,2.4):
        B.box((x0,D_-.35,1.6),(1.15,.32,1.6),wd,.02)
        for k in range(7):
            z=.25+k*.42; B.box((x0,D_-.35,z-.17),(1.15,.33,.02),wd,0)
            for j in range(4): thaan((x0-.85+j*.57,D_-.42,z),r.choice(FAB),l=.5)
    # side wall shelves (left) + hanging dupattas (right)
    for k in range(5):
        z=.35+k*.5; B.box((-W_+.35,.8,z-.13),(.3,1.5,.02),wd,0)
        for j in range(5): thaan((-W_+.38,-.4+j*.55,z),r.choice(FAB),rot=(0,0,R(90)),l=.5)
    B.cyl((W_-.25,.8,2.6),.025,3.0,M('#C9A24A',.3,metal=.8),rot=(R(90),0,0),seg=6)
    for j in range(8): B.box((W_-.25,-.5+j*.38,1.8),(.02,.15,.8),M(r.choice(FAB),.9,kind='fabric'),.01)
    # counter with white lawn stack + yardstick + cash box + calculator
    B.box((0,1.25,.48),(2.2,.42,.48),wd,.03); B.box((0,1.25,.97),(2.25,.46,.02),M('#BFD6E8',.05,spec=1.0,alpha=.45),.01)
    B.box((0,.85,.05),(2.2,.04,.05),M('#3A2414',.6),0)
    for k in range(5): thaan((-1.3,1.25,1.05+k*.12),'#F4F1EA',l=.8)
    B.box((.4,1.3,1.0),(.9,.02,.01),M('#D9B24A',.5,kind='wood'),0); B.box((1.5,1.35,1.08),(.22,.16,.1),M('#2B5AA8',.5,metal=.3),.02); B.box((1.0,1.2,1.0),(.09,.13,.015),M('#16171C',.4),.01)
    # floor gadda behind counter, calendar, fan, tube light
    B.box((0,2.2,.08),(1.8,.6,.08),M('#F4F1EA',.9,kind='fabric',h2='#C8372D',sc=6),.04)
    B.box((-1.8,D_-.04,2.95),(.25,.02,.3),M('#F4F1EA',.6),0); B.box((-1.8,D_-.06,3.08),(.22,.01,.08),M('#C8372D',.6),0)
    B.box((1.2,D_-.06,3.15),(.7,.04,.04),M('#FFFFFF',.3,emit=3),0)
    # open front with rolled-up shutter, street + facing shops beyond
    B.box((0,-D_+.05,3.0),(W_,.2,.3),M('#8A8E96',.5,metal=.5),.04)
    B.box((0,-D_-4.2,2.5),(10,.2,2.5),M('#D9A06A',.85,kind='wall'),0)
    for x in range(-8,9,2): B.box((x,-D_-4.0,1.6),(.6,.05,1.0),M(r.choice(FAB),.9,kind='fabric'),.01)
    B.box((0,-D_-3.95,3.6),(4,.05,.35),M('#7A1F1F',.6),0); stext('SALEEM CLOTH CENTRE',(0,-D_-3.88,3.58),.3,'#FFF3B0',n=(0,1,0),e=.6)
def three_shirts(e,s=1.0):
    st=M('#C9CED8',.3,metal=.8); ocyl((0,0,1.75*s),.02,1.6*s,st,e,rot=(0,R(90),0),seg=6)
    for dx in (-.75,.75): ocyl((dx*s,0,.88*s),.02,1.75*s,st,e,rot=(0,0,0),seg=6); obox((dx*s,0,.02),(.04,.25,.02),st,0,e)
    shirts=[]
    for k,(c,p) in enumerate((('#F4F1EA','#2B5AA8'),('#16171C','#F2C14E'),('#E8709A','#F4F1EA'))):
        h=empty(((-.5+.5*k)*s,0,1.72*s),e); obox((0,0,-.03),(.12,.01,.03),st,0,h)
        obox((0,0,-.42*s),(.2*s,.05,.36*s),M(c,.85,kind='fabric'),.03,h); obox((0,0,-.12*s),(.3*s,.05,.08*s),M(c,.85,kind='fabric'),.03,h)
        obox((0,-.06,-.3*s),(.04*s,.01,.1*s),M(p,.6),0,h); shirts.append(h)
    return shirts
# ---------------------------------------------------------------- rooftop
def roof_set(seed=6):
    r=random.Random(seed); sl=M('#B8B0A4',.9,kind='asphalt',sc=1.5); pw=M('#E8D8C0',.85,kind='wall')
    B.box((0,0,-.1),(5,5,.1),sl,0)
    for (cx,cy,sx,sy) in ((0,5,5,.1),(0,-5,5,.1),(5,0,.1,5),(-5,0,.1,5)): B.box((cx,cy,.45),(sx,sy,.45),pw,.02)
    for k in range(9):
        for s in (-1,1): B.box((-4.2+k*1.05,s*5,.95),(.06,.06,.06),M('#C8703F',.7),0) if False else None
    # black water tank on stand (background)
    B.box((2.6,3.6,.7),(.9,.9,.05),M('#8A8E96',.4,metal=.6),0)
    for dx in (-.8,.8):
        for dy in (-.8,.8): B.box((2.6+dx,3.6+dy,.35),(.05,.05,.35),M('#5A5E66',.4,metal=.6),0)
    B.cyl((2.6,3.6,1.5),.85,1.6,M('#1A1C22',.55),seg=20); B.cyl((2.6,3.6,2.33),.3,.08,M('#1A1C22',.55),seg=16)
    for k in range(4): B.box((2.6,3.6,.95+k*.4),(.86,.86,.015),M('#26282E',.5),0) if False else B.cyl((2.6,3.6,.9+k*.4),.87,.03,M('#2A2C32',.5),seg=20)
    # laundry lines with clothes
    for (y,z) in ((1.8,2.0),(2.8,2.1)):
        for x in (-4.4,1.4): B.cyl((x,y,z/2),.03,z,M('#5A5E66',.4,metal=.6),rot=(0,0,0),seg=6)
        B.cyl((-1.5,y,z),.008,5.8,M('#16171C',.5),rot=(0,R(90),0),seg=4)
        for j in range(7): B.box((-4.0+j*.78,y,z-.32-r.uniform(0,.15)),(.25,.015,r.uniform(.22,.36)),M(r.choice(FAB),.9,kind='fabric'),.01)
    # charpai, plants, dish, AC unit
    e=empty((-3.2,-2.8,0),rot=(0,0,R(20))); wd=M('#7A5236',.6,kind='wood'); obox((0,0,.42),(.95,.5,.05),M('#E8D8B0',.9,kind='fabric',h2='#C8A878',sc=8),.02,e)
    for dx in (-.9,.9):
        for dy in (-.45,.45): obox((dx,dy,.2),(.05,.05,.2),wd,.01,e)
    for (x,y) in ((-4.4,4.2),(-3.6,4.4),(4.3,-4.3)): B.cyl((x,y,.25),.22,.5,M('#B5542E',.7),seg=12,r2=.17); B.ico((x,y,.75),.38,M('#3F8A3A',.85,kind='leaves'),sub=1,sc=(1,1,1.2))
    B.cyl((-4.3,-4.3,1.4),.03,1.8,M('#5A5E66',.4,metal=.6),seg=5); B.cyl((-4.3,-4.15,2.3),.45,.06,M('#D8DCE2',.4),rot=(R(60),0,0),seg=18)
    # neighbouring roofs + tanks + city
    for k in range(16):
        a=k*pi/8; d=r.uniform(11,18); x=math.cos(a)*d; y=math.sin(a)*d+3; h=r.uniform(-2,5)
        B.box((x,y,h/2-3),(r.uniform(2.5,4),r.uniform(2.5,4),(h+6)/2),M(r.choice(['#E8D8B0','#D98A5A','#C9B48A','#F0E0C0','#B8634A']),.85,kind='wall'),0)
        if r.random()<.7: B.cyl((x+r.uniform(-1,1),y+r.uniform(-1,1),h+.6),.5,1.2,M('#1A1C22',.55),seg=14)
        if r.random()<.4:
            for j in range(3): B.box((x-1+j*.7,y,h+.8),(.2,.01,.3),M(r.choice(FAB),.9,kind='fabric'),0)
    clock_tower(-14,30,1.0)
    kites=[]
    for k in range(4):
        e=empty((r.uniform(-12,12),r.uniform(18,28),r.uniform(9,14)),rot=(R(80),R(45),0)); obox((0,0,0),(.35,.01,.35),M(r.choice(['#E8423A','#F2C14E','#2B8A5A','#E8709A']),.6),.0,e); kites.append(e)
    return kites
def ring_light(e):
    st=M('#16171C',.4); ocyl((0,0,.75),.015,1.5,st,e,rot=(0,0,0),seg=6)
    for a in (0,2.1,4.2): obox((math.cos(a)*.2,math.sin(a)*.2,.05),(.2,.015,.015),st,0,e,rot=(0,0,a))
    ocyl((0,0,1.62),.24,.04,M('#FFFFFF',.3,emit=3.0),e,rot=(R(90),0,0),seg=24); ocyl((0,.01,1.62),.17,.05,M('#16171C',.4),e,rot=(R(90),0,0),seg=24)
def biryani_plate(e,s=1.0):
    ocyl((0,-.08,.05*s),.2*s,.03*s,M('#F4F1EA',.4),e,rot=(0,0,0),seg=20); oico((0,-.08,.09*s),.17*s,M('#E8B84A',.8),e,sc=(1,1,.4),sub=2)
    for k in range(5): oico(((k-2)*.05*s,-.08+.03*(k%2),.15*s),.03*s,M(['#C8372D','#2B8A5A','#F4F1EA','#8A4A20','#F2C14E'][k],.6),e,sub=1)
# ---------------------------------------------------------------- power loom mill
def mill_set(seed=4):
    r=random.Random(seed); fl=M('#8A8E96',.7,kind='asphalt',sc=1.2); wl=M('#D8D0C0',.9,kind='wall')
    B.box((0,0,-.05),(10,14,.05),fl,0); B.box((0,14,3),(10,.15,3),wl,0); B.box((-10,0,3),(.15,14,3),wl,0); B.box((10,0,3),(.15,14,3),wl,0)
    for k in range(8):  # sawtooth roof with skylights
        y=-12+k*3.4; B.box((0,y,6.2),(10,1.7,.08),M('#8A8E96',.6,metal=.4),0,rot=(R(18),0,0)); B.box((0,y+1.6,6.4),(10,.04,.55),M('#E8F4FF',.2,emit=1.4),0)
    for k in range(6):
        for x in (-5,0,5): B.box((x,-10+k*4,5.4),(.9,.06,.03),M('#FFFFFF',.3,emit=4),0)
    # windows on side walls
    for k in range(6):
        for s in (-1,1): B.box((s*9.88,-10+k*4,3.3),(.02,.9,.6),M('#E8F4FF',.2,emit=1.2),0)
    beaters=[]; rolls=[]
    for row in range(5):
        for col in range(3):
            x=-5.2+col*5.2; y=-6+row*3.2; e=empty((x,y,0)); fr=M('#3A6A5A',.5,metal=.5); dk=M('#26282E',.5,metal=.6)
            for dx in (-1.4,1.4): obox((dx,0,.7),(.12,.7,.7),fr,.02,e)
            obox((0,.55,.55),(1.35,.1,.1),dk,.02,e); ocyl((0,.65,.95),.18,2.7,M('#F4F1EA',.9,kind='fabric'),e,rot=(0,R(90),0),seg=16)
            obox((0,0,1.05),(1.3,.55,.01),M('#F4F1EA',.8,kind='fabric',h2='#E0DACC',sc=10),0,e,rot=(R(-12),0,0))
            for j in range(26): obox((-1.25+j*.1,-.45,1.15),(.004,.25,.004),M('#E8E2D6',.6),0,e,rot=(R(-30),0,0))
            ocyl((0,-.75,.55),.25,2.6,M('#E8E2D6',.9,kind='fabric'),e,rot=(0,R(90),0),seg=16); rolls.append(e)
            b=empty((0,.05,1.25),e); obox((0,0,0),(1.3,.05,.05),M('#C9A24A',.4,metal=.7),.01,b); beaters.append(b)
            obox((-1.65,0,.55),(.18,.25,.3),M('#5A6E8A',.5,metal=.4),.03,e)
    # cloth roll stacks + owner's desk near entrance
    for k in range(10): B.cyl((-8.5,-11+k*.62,.3+.55*(k%2)),.3,1.8,M(r.choice(['#F4F1EA','#E8E2D6','#9FC8E0','#F2E0B0']),.9,kind='fabric'),rot=(0,R(90),0),seg=14)
    B.box((6.5,-10,.42),(1.1,.55,.42),M('#5A3A22',.6,kind='wood'),.03); B.box((6.3,-10,.88),(.3,.22,.04),M('#C8372D',.7),.01)
    B.box((6.5,-8.9,.5),(.3,.3,.5),M('#2A2C34',.5),.02)
    B.box((0,-14,4),(10,.15,2),wl,0); B.box((-6,-14,1),(4,.15,1),wl,0); B.box((6,-14,1),(4,.15,1),wl,0)
    stext('MUKHTAR POWER LOOMS',(0,-13.8,5.2),.45,'#1F4D3A',n=(0,1,0))
    return beaters
# ---------------------------------------------------------------- phone UIs
def insta_ui():
    root=empty((0,0,-200)); ui=lambda c,e=1.2: M(c,.6,emit=e,spec=0)
    obox((0,.1,0),(1.25,.08,2.45),M('#16171C',.3,spec=.9),.18,root); obox((0,0,0),(1.12,.01,2.3),ui('#FAFAFA',1.0),.0,root)
    text('INTERNATIONAL_FASHION_GROUP',(0,-.03,1.95),(0,-1,0),.1,ui('#16171C',.6),ex=0,parent=root)
    ocyl((-.85,-.02,1.65),.12,.01,ui('#E8709A',1.2),root,seg=16); text('ifg_official',(-.2,-.03,1.7),(0,-1,0),.11,ui('#16171C',.6),ex=0,parent=root)
    pin=empty((0,0,0),root); text('London, United Kingdom',(-.05,-.03,1.53),(0,-1,0),.1,ui('#2B5AA8',1.4),ex=0,parent=pin); oico((-.75,-.03,1.54),.04,ui('#E8423A',2.0),pin,sub=1)
    # the "photo": roof, tank, laundry, Bilal posing
    obox((0,-.01,.45),(1.1,.01,1.0),ui('#9FC8E8',1.0),0,root); obox((0,-.02,-.25),(1.1,.01,.3),ui('#B8B0A4',1.0),0,root)
    ocyl((.6,-.03,.25),.25,.01,ui('#1A1C22',.8),root,seg=16,sc=(1,1,1.6));
    for k in range(5): obox((-.8+k*.2,-.03,.95),(.06,.01,.09),ui(FAB[k],1.0),0,root)
    obox((-.1,-.035,.15),(.13,.01,.25),ui('#F28A3A',1.0),0,root); obox((-.1,-.035,.5),(.1,.01,.1),ui('#C69062',1.0),0,root); obox((-.1,-.035,-.25),(.1,.01,.17),ui('#2A3350',1.0),0,root)
    hearts_=[]
    for k,(x,c) in enumerate(((-.9,'#E8423A'),(-.6,'#16171C'),(-.3,'#16171C'))): ocyl((x,-.03,-.75),.07,.01,ui(c,1.2),root,seg=14)
    text('3 likes',(-.75,-.03,-.98),(0,-1,0),.1,ui('#16171C',.6),ex=0,parent=root)
    text('New collection drop. 3 pieces only. #luxury #london',(0,-.03,-1.2),(0,-1,0),.075,ui('#16171C',.6),ex=0,parent=root)
    return dict(root=root,pin=pin)
def fan_ft(loc):
    e=empty(loc); ocyl((0,0,.2),.02,.4,M('#2A2C34',.5),e,rot=(0,0,0),seg=6); ocyl((0,0,0),.15,.13,M('#5A3A22',.4,kind='wood'),e,rot=(0,0,0),seg=14)
    bl=empty((0,0,.01),e)
    for a in range(3): obox((math.cos(a*2.094)*.55,math.sin(a*2.094)*.55,0),(.5,.1,.012),M('#8A5A30',.5,kind='wood'),.02,bl,rot=(0,0,a*2.094))
    return bl
def cash(e,s=1.0,n=4,col='#3E8A5A'):
    for k in range(n): obox((0,-.08,.03*s+k*.05*s),(.16*s,.08*s,.022*s),M(col,.7),.005,e,rot=(0,0,R(8*(k%2)))); obox((0,-.08,.03*s+k*.05*s),(.03*s,.082*s,.024*s),M('#F4F1EA',.6),0,e)
def pocket_stuff(e,s=1.0):
    obox((0,-.08,.05),(.13*s,.005,.065*s),M('#D98A3A',.7),0,e,rot=(R(-70),0,R(10))); obox((.03,-.09,.08),(.13*s,.005,.065*s),M('#D98A3A',.7),0,e,rot=(R(-70),0,R(-8)))
    obox((-.05,-.1,.13),(.06*s,.005,.12*s),M('#F4F1EA',.8),0,e,rot=(R(-75),0,R(25)))
