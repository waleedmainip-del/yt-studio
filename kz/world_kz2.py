# SET B: burns() - old-town Karachi night food street (colonial stone buildings, arcades, neon blade signs, bulb canopy,
# tawa / grill / deg stations, street tables, clock tower) + open-front restaurant CHACHA MAGHAZ HOUSE + rooftop.
BW=6.0; BX0=-50; BX1=50; RX=7.5; RDEP=9.5; RH=4.6          # street half width, extent, restaurant half width / depth / ceiling
ROOF_Z=4.9+3*3.5; ROOF_X=(-9.0,9.0)                         # rooftop (south building opposite the restaurant)
OLDC=['#E0C48C','#D8B878','#E8D2A0','#E0A890','#D99A8A','#A8D0C0','#A8C4E0','#F0E6CC','#C8B8D8','#E6B87A']
SHUT=['#2E7A6A','#2B58C9','#7A4A2A','#1E6A3A','#8A2A3A','#3A5A8A']
B_SIGNS=[('KARACHI KATAKAT','#C8372D'),('NIHARI WALA','#1E6A3A'),('RABRI HOUSE','#7448C2'),('BUN KABAB','#D9811A'),('SEEKH KABAB','#7A1F2E'),('FRY FISH','#2B6A8A'),('KULFI FALOODA','#B8456A'),
         ('SAJJI CORNER','#8A4A1E'),('DAHI BARAY','#35975A'),('HALEEM POINT','#2B58C9'),('LASSI SHOP','#16909E'),('PAAN BAHAR','#1E6A3A'),('CHAI ADDA','#7A1F2E'),('PARATHA ROLL','#D9811A')]
BLADES=['NIHARI','KABAB','CHAI','LASSI','KULFI','BBQ','ROLLS','PAAN','SAJJI','RABRI','FISH','HALEEM']
def vtext(body,loc,size,col,n,e=0.0):
    tm=M(col,.4,emit=round(e,3)) if e>0 else M(col,.5)
    if e>0 and (tm,round(e,3)) not in LITM: LITM.append((tm,round(e,3)))
    return text('\n'.join(body),loc,n,size,tm,ex=.012)
def blade(x,y,z,word,bg,col='#FFF6D8',side=1,size=.5):
    """vertical neon blade sign projecting from a facade (readable along the street from both directions)"""
    hh=len(word)*size*.5+.3; s=side
    B.box((x,y-s*.75,z),(.09,.5,hh),lit(bg,1.3,.5,always=True),.0); B.box((x,y-s*.75,z),(.07,.56,hh+.06),M('#F4F1EA',.5),0)
    for k in (-1,1): B.box((x,y-s*.12,z+k*hh*.7),(.03,.14,.03),M('#2A2C34',.5),0)
    for n in ((-1,0,0),(1,0,0)): vtext(word,(x+n[0]*.105,y-s*.75,z),size,col,n,e=3.2)
    for k in range(int(hh*2/.4)+1):
        for dy in (-.5,.5): B.ico((x,y-s*.75+dy,z-hh+k*.4),.045,lit('#FFE08A',6,always=True),sub=1)
def oldb(cx,w,fl,col,side,seed,sign_=None,scol='#C8372D',depth=11.0,open_front=False,fh=3.5,blade_=None,Y=None,plain_roof=False,sx=0.0,noac0=False):
    """colonial-era stone building. front at Y (default BW), body extends away from the street. returns roof height"""
    r=random.Random(seed); s=side; y0=s*(BW if Y is None else Y); yc=y0+s*depth/2; G=4.9; H=G+fl*fh
    wall=M(col,.85,kind='wall'); tr=M('#F2EBDA',.8); dk=M('#17140F',.8); iron=M('#22242B',.4,metal=.6)
    B.box((cx,yc,(G+H)/2),(w/2,depth/2,(H-G)/2),wall,0)                                   # upper body
    if not open_front: B.box((cx,y0+s*(depth/2+.6),G/2),(w/2,depth/2-.6,G/2),wall,0)        # ground body, set back 1.2 behind the arcade
    nb=max(1,round(w/3.4)); bw_=w/nb
    if not open_front:
        for k in range(nb+1): B.box((cx-w/2+k*bw_,y0+s*.3,G/2),(.28,.32,G/2),wall,.03); B.box((cx-w/2+k*bw_,y0+s*.3,3.3),(.34,.38,.1),tr,.02)
        for k in range(nb):
            bx=cx-w/2+(k+.5)*bw_
            B.box((bx,y0+s*.3,G-.45),(bw_/2,.3,.45),wall,0)
            for sx in (-1,1): B.box((bx+sx*(bw_/2-.5),y0+s*.3,G-1.05),(.42,.3,.42),wall,0,rot=(0,R(45),0))
            # shop inside the bay: shutter / goods / counter
            kind=r.random(); zb=1.9
            if kind<.3:
                B.box((bx,y0+s*1.15,zb),(bw_/2-.35,.05,zb),M(r.choice(['#8A8E96','#5A7FB0','#6A8A5A','#8A5A4A']),.5,metal=.4),0)
                for j in range(9): B.box((bx,y0+s*1.09,.35+j*.42),(bw_/2-.35,.02,.03),M('#3A3D44',.5),0)
            else:
                B.box((bx,y0+s*1.18,zb),(bw_/2-.3,.05,zb),M(shade(col,.5),.8),0)
                B.box((bx,y0+s*.75,.5),(bw_/2-.5,.3,.5),M(r.choice(['#7A4E2A','#8A5A36','#3A5A6A','#7A1F2E']),.6,kind='wood',sc=.6),.03); B.box((bx,y0+s*.75,1.03),(bw_/2-.45,.34,.03),M('#C9CED8',.3,metal=.7),.01)
                for j in range(int((bw_-1.2)/.36)):
                    B.cyl((bx-bw_/2+.75+j*.36,y0+s*.72,1.2),.11,.3,M(r.choice(['#E8554D','#F2C14E','#F4F1DE','#C9772B','#6FC38A','#B5713A']),.5),seg=8)
                for j in range(3):
                    B.box((bx,y0+s*1.1,1.7+j*.75),(bw_/2-.5,.14,.03),M('#5E3A22',.6),0)
                    for q in range(int((bw_-1.2)/.4)): B.box((bx-bw_/2+.75+q*.4,y0+s*1.05,1.86+j*.75),(.14,.1,.13),M(r.choice(['#E8554D','#F2C14E','#4D8FE8','#6FC38A','#F4F1DE','#9B6FD0','#FF8A3A']),.6),.01)
                B.box((bx,y0+s*.95,3.9),(.5,.03,.05),lit('#FFF3D0',7,always=True),0)             # tube light in the shop
            if r.random()<.6:
                ac=r.choice(['#C8372D','#2B58C9','#1E6A3A','#D9811A','#7448C2']); n_=6
                for j in range(n_): B.box((bx-bw_/2+.3+(j+.5)*(bw_-.6)/n_,y0-s*.5,3.5),((bw_-.6)/n_/2,.55,.025),M(ac if j%2 else '#F4F1EA',.85,kind='fabric'),.004,rot=(R(-16*s),0,0))
    else:
        for k in (-1,-.34,.34,1): B.box((cx+k*(w/2-.28),y0+s*.3,G/2),(.28,.32,G/2),wall,.03); B.box((cx+k*(w/2-.28),y0+s*.3,3.6),(.34,.38,.1),tr,.02)
        B.box((cx,y0+s*.3,G-.35),(w/2,.3,.35),wall,0)
    B.box((cx,y0-s*.12,G+.06),(w/2+.1,.42,.14),tr,.02)                                    # cornice above ground floor
    if sign_:
        sz=min(.58,(w-1.6)/(len(sign_)*.69)); hw,hh=sign(sign_,(cx+sx,y0-s*.42,G+.82),sz,'#FFF6D8',scol,n=(0,-s,0),e=3.0,pad=.3,th=.12,frame='#F2C14E',always=True)
        for k in range(int(hw*2/.42)+1):
            for dz in (-1,1): B.ico((cx+sx-hw+k*.42,y0-s*.5,G+.82+dz*(hh+.09)),.045,lit('#FFE08A',6,always=True),sub=1)
    # upper floors
    nw=max(2,round(w/2.5)); sh=M(r.choice(SHUT),.6,kind='wood',sc=.8)
    for f in range(fl):
        zb=G+f*fh; B.box((cx,y0-s*.08,zb+fh-.1),(w/2+.06,.16,.1),tr,.01)
        for k in range(nw):
            wx=cx-w/2+(k+.5)*w/nw; wz=zb+1.85; q=r.random()
            litw=r.random()<.5
            B.box((wx,y0-s*.02,wz),(.5,.04,1.0),lit(r.choice(WINL),r.uniform(1.8,3.2),always=True) if litw else M('#1A2030',.15,spec=.9),0)
            B.box((wx,y0-s*.06,wz+1.08),(.62,.09,.08),tr,.01); B.box((wx,y0-s*.06,wz+1.3),(.4,.07,.14),tr,.05); B.box((wx,y0-s*.07,wz-1.06),(.66,.12,.07),tr,.01)
            B.box((wx,y0-s*.05,wz),(.03,.03,1.0),tr,0); B.box((wx,y0-s*.05,wz+.2),(.5,.03,.03),tr,0)
            if q<.55:
                for sx in (-1,1): B.box((wx+sx*.78,y0-s*.12,wz),(.27,.035,1.0),sh,.01,rot=(0,0,R(sx*-28*s)))
            if q>.4 and f>0:
                B.box((wx,y0-s*.5,zb+.72),(.85,.5,.05),M('#8A8478',.8),.01)
                for j in range(8): B.box((wx-.8+j*.23,y0-s*.98,zb+1.05),(.018,.018,.3),iron,0)
                for sx in (-1,1): B.box((wx+sx*.83,y0-s*.5,zb+1.05),(.018,.48,.018),iron,0); B.box((wx+sx*.83,y0-s*.98,zb+1.05),(.02,.02,.32),iron,0)
                B.box((wx,y0-s*.98,zb+1.36),(.85,.025,.025),iron,0)
                if r.random()<.55: B.cyl((wx+.55,y0-s*.7,zb+.92),.13,.26,M('#B5542E',.7),seg=10); B.ico((wx+.55,y0-s*.7,zb+1.2),.2,M('#3F8A3A',.8),sub=1)
                if r.random()<.4:
                    for j in range(4): B.box((wx-.55+j*.36,y0-s*.99,zb+.72),(.13,.012,.26),M(r.choice(['#E8554D','#F2C14E','#4D8FE8','#F4F1DE','#9B6FD0','#6FC38A']),.9),0)
            elif r.random()<.25 and (f>0 or not (sign_ or noac0)): B.box((wx+.45,y0-s*.28,wz-1.25),(.4,.24,.24),M('#D8DCE2',.5),.03); B.cyl((wx+.45,y0-s*.53,wz-1.25),.16,.02,M('#5A5E66',.5),rot=(R(90),0,0),seg=12)
    # top: cornice, balustrade, pediment
    B.box((cx,y0-s*.15,H+.12),(w/2+.2,.5,.16),tr,.03)
    for k in range(int(w/.5)): B.cyl((cx-w/2+.25+k*.5,y0+s*.1,H+.62),.08,.7,tr,seg=6)
    B.box((cx,y0+s*.1,H+1.02),(w/2,.14,.07),tr,.02)
    if w>6.5 and not plain_roof:
        B.box((cx,y0+s*.1,H+1.5),(1.5,.16,.45),wall,.03); B.box((cx,y0+s*.1,H+2.0),(1.7,.2,.08),tr,.02); B.box((cx,y0+s*.1,H+2.25),(.9,.16,.2),wall,.08)
        text(str(r.choice([1921,1932,1938,1944,1951])),(cx,y0-s*.08,H+1.5),(0,-s,0),.44,M('#6A5238',.6),ex=.01)
    if not plain_roof:
        for k in range(r.randint(1,2)): B.cyl((cx+r.uniform(-w/3,w/3),yc+r.uniform(-1.5,1.5),H+.9),.6,1.4,M(r.choice(['#1A1C22','#2B6FB8']),.6),seg=14)
    if blade_: blade(cx+w/2 if r.random()<.5 else cx-w/2,y0,G+fh*1.25,blade_[0],blade_[1],side=s)
    return H
# ---------------------------------------------------------------- street furniture
def tawa(x,y,rz=0,food=True):
    """tawa counter facing rz (cook stands behind). returns empty"""
    e=empty((x,y,0),rot=(0,0,R(rz))); tl_=M('#F2EEE6',.4,kind='tile',sc=5,h2='#2E8A7A')
    obox((0,0,.52),(1.15,.55,.52),tl_,.02,e); obox((0,0,1.06),(1.2,.6,.03),M('#C9CED8',.3,metal=.8),.01,e)
    ocyl((-.3,0,1.16),.62,.09,M('#141416',.35,metal=.6),e,rot=(0,0,0),seg=28); ocyl((-.3,0,1.2),.56,.03,M('#2A1E16',.3,spec=.8),e,rot=(0,0,0),seg=28)
    ocyl((-.3,0,1.08),.5,.04,lit('#FF7A1A',6,always=True),e,rot=(0,0,0),seg=20)
    if food:
        r=random.Random(int(x*7+y*3))
        for k in range(16): a=r.uniform(0,6.28); q=r.uniform(0,.42); oico((-.3+math.cos(a)*q,math.sin(a)*q,1.24),r.uniform(.05,.09),M(r.choice(['#B5642A','#C87A3A','#8A4A1E','#D99A5A','#3F8A3A','#C8372D']),.5,spec=.6),e,sc=(1,1,.55),sub=1)
    for k in range(4): ocyl((.75,-.25+k*.02,1.1+k*.035),.2,.025,M('#F4F1EA',.4),e,rot=(0,0,0),seg=16)
    ocyl((.8,.25,1.2),.14,.24,M('#C9CED8',.3,metal=.8),e,rot=(0,0,0),seg=14); obox((.45,.3,1.14),(.14,.1,.06),M('#C8372D',.5),.02,e)
    return e
def grill(x,y,rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz))); blk=M('#1A1A1E',.5,metal=.5)
    obox((0,0,.95),(1.1,.28,.1),blk,.02,e)
    for sx in (-1,1):
        for sy in (-1,1): ocyl((sx*.95,sy*.2,.45),.03,.9,blk,e,rot=(0,0,0),seg=6)
    obox((0,0,1.02),(1.02,.22,.03),lit('#FF4A1A',7,always=True),0,e)
    for k in range(9):
        ocyl((-.85+k*.21,0,1.1),.012,.7,M('#C9CED8',.3,metal=.9),e,rot=(R(90),0,0),seg=5)
        for j in range(3): oico((-.85+k*.21,-.14+j*.14,1.1),.05,M(['#8A4A1E','#B5642A','#7A3A16'][(k+j)%3],.5),e,sub=1)
    return e
def ptable(x,y,rz=0,w=.66,d=.5,dress=0,seed=0):
    """pedestal table (top z=1.14 clears seated legs). dress: 0 empty, 1 plates+chai, 2 karahi feast"""
    e=empty((x,y,0),rot=(0,0,R(rz))); st=M('#C9CED8',.3,metal=.8); r=random.Random(seed*31+7)
    obox((0,0,1.12),(w,d,.025),M('#E8E2D0',.5),.015,e); obox((0,0,1.09),(w+.01,d+.01,.012),M('#C8372D',.5),.005,e)
    ocyl((0,0,.55),.06,1.08,st,e,rot=(0,0,0),seg=10); ocyl((0,0,.03),.3,.05,st,e,rot=(0,0,0),seg=16)
    if dress>=1:
        for sx in (-1,1):
            ocyl((sx*.36,.08,1.16),.15,.02,M('#F6F4EE',.4),e,rot=(0,0,0),seg=16); ocyl((sx*.36,.08,1.175),.1,.015,M(r.choice(['#C87A3A','#D9A050','#B5642A']),.6),e,rot=(0,0,0),seg=12)
            ocyl((sx*.3,-.3,1.2),.055,.11,M('#F6F4EE',.4),e,rot=(0,0,0),seg=10,r2=.045); ocyl((sx*.3,-.3,1.25),.047,.012,M('#B5713A',.5),e,rot=(0,0,0),seg=10)
        ocyl((0,.32,1.24),.07,.22,M('#BFE6F2',.1,spec=1,alpha=.5),e,rot=(0,0,0),seg=12)
    if dress>=2: karahi_obj((0,-.02,1.14),.42,e); ocyl((0,.02,1.15),.19,.012,M('#2A2C34',.5),e,rot=(0,0,0),seg=14)
    return e
def kchair(x,y,rz,col='#C8372D'): return pchair(x,y,rz,col)
def cart(x,y,rz,col,label,umb='#F2C14E'):
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#8A5A36',.6,kind='wood',sc=.6)
    obox((0,0,.85),(1.0,.55,.28),M(col,.5),.03,e); obox((0,0,1.15),(1.05,.6,.03),M('#C9CED8',.3,metal=.8),.01,e)
    for sx in (-1,1): w_=wheel((sx*1.1,0,.42),.42,.08,e,M('#3A2A1E',.7)); w_.rotation_euler=(0,0,R(90))
    ocyl((0,0,2.0),.03,1.7,M('#8A8E96',.4,metal=.6),e,rot=(0,0,0),seg=6)
    for k in range(8): a=k*pi/4; obox((math.cos(a)*.7,math.sin(a)*.7,2.72),(.72,.3,.02),M(umb if k%2 else '#F4F1EA',.8,kind='fabric'),.005,e,rot=(0,R(14),a))
    sign(label,(0,-.57,.85),.22,'#FFF6D8',shade(col,.6),n=(0,-1,0),e=2.0,pad=.1,th=.03,parent=e,always=True)
    for k in range(5): ocyl((-.6+k*.3,-.1,1.3),.1,.26,M(['#F2A11A','#E8554D','#6FC38A','#F4F1DE','#B5713A'][k],.4,spec=.7),e,rot=(0,0,0),seg=10)
    return e
def clock_tower(x,y,hh=3,mm=0):
    st=M('#D8B878',.85,kind='wall'); tr=M('#F2EBDA',.8); H=30.0
    B.box((x,y,H/2),(3.6,3.6,H/2),st,.05); B.box((x,y,.8),(4.3,4.3,.8),st,.05)
    for z in (7,13,17.2,26.8): B.box((x,y,z),(3.8,3.8,.16),tr,.03)
    for k in range(3): B.box((x-3.62,y,3.6+k*4.2),(.05,.8,1.3),lit('#FFD98A',2.2,always=True) if k!=1 else M('#1A2030',.2,spec=.9),0); B.box((x-3.66,y,5.0+k*4.2),(.06,.95,.12),tr,0)
    B.box((x,y,H+.6),(4.1,4.1,.6),tr,.06)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((x+sx*3.6,y+sy*3.6,H+2.2),.38,2.2,tr,seg=8); B.ico((x+sx*3.6,y+sy*3.6,H+3.5),.46,tr,sub=1)
    B.cyl((x,y,H+4.6),3.2,7.0,M('#7A3E2A',.7),seg=4,r2=.2,rot=(0,0,R(45))); B.cyl((x,y,H+9.0),.08,2.0,M('#D9B24A',.3,metal=.8),seg=6)
    c=empty((x-3.72,y,22.0)); ocyl((0,0,0),3.25,.14,tr,c,rot=(0,R(90),0),seg=40); ocyl((-.08,0,0),3.0,.05,lit('#FFF6D8',2.4,always=True),c,rot=(0,R(90),0),seg=40)
    for k in range(12): a=k*pi/6; obox((-.12,math.sin(a)*2.6,math.cos(a)*2.6),(.02,.08,.28 if k%3==0 else .14),M('#16171C',.5),0,c,rot=(-a,0,0))
    h1=empty((-.14,0,0),c); obox((0,0,.8),(.02,.14,.9),M('#16171C',.5),0,h1); h2=empty((-.16,0,0),c); obox((0,0,1.2),(.02,.09,1.35),M('#16171C',.5),0,h2)
    ocyl((-.18,0,0),.22,.04,M('#C8372D',.5),c,rot=(0,R(90),0),seg=12)
    C=dict(h=h1,m=h2); clock_set(C,hh,mm); return C
def clock_set(C,hh,mm):
    # face looks toward -x: seen from the street, 3 o'clock is at -y (screen right when looking +x). rotation about x.
    C['m'].rotation_euler=(R(mm*6.0),0,0); C['h'].rotation_euler=(R((hh%12+mm/60.0)*30.0),0,0)
FANS=[]
def fan(x,y,z):
    e=empty((x,y,z)); ocyl((0,0,.25),.025,.5,M('#C9CED8',.3,metal=.8),e,rot=(0,0,0),seg=6); ocyl((0,0,0),.14,.1,M('#F4F1EA',.4),e,rot=(0,0,0),seg=12)
    b=empty((0,0,-.03),e)
    for k in range(3): a=k*2*pi/3; obox((math.cos(a)*.55,math.sin(a)*.55,0),(.45,.09,.012),M('#E8E2D0',.5),.005,b,rot=(R(8),0,a))
    FANS.append(b); return b
def restaurant():
    """CHACHA MAGHAZ HOUSE: open-front dining hall on the north side, x -RX..RX, y BW..BW+RDEP"""
    y0=BW; y1=BW+RDEP; tl_=M('#F4F1EA',.4,kind='tile',sc=3.2,h2='#DCE8E4'); gr=M('#2E8A7A',.4,kind='tile',sc=3.2,h2='#27786A'); fl=M('#D8D2C4',.5,kind='tile',sc=1.1,h2='#8A3A2A')
    B.box((0,(y0+y1)/2+.2,.012),(RX,RDEP/2-.2,.012),fl,0)
    B.box((0,y1,RH/2),(RX,.12,RH/2),tl_,0); B.box((0,y1-.14,.75),(RX,.03,.75),gr,0); B.box((0,y1-.15,1.53),(RX,.04,.05),M('#D9B24A',.4,metal=.5),0)
    for sx in (-1,1):
        B.box((sx*RX,(y0+y1)/2+.6,RH/2),(.12,RDEP/2-.6,RH/2),tl_,0); B.box((sx*(RX-.14),(y0+y1)/2+.6,.75),(.03,RDEP/2-.6,.75),gr,0); B.box((sx*(RX-.15),(y0+y1)/2+.6,1.53),(.04,RDEP/2-.6,.05),M('#D9B24A',.4,metal=.5),0)
    B.box((0,(y0+y1)/2+.3,RH+.06),(RX,RDEP/2-.3,.06),M('#EDE8DC',.8),0)
    for x in (-4.6,0,4.6):
        for y in (y0+2.6,y0+6.4): B.box((x,y,RH-.05),(.9,.05,.035),lit('#FFF8E8',9,always=True),0)
    fan(-3.2,y0+4.6,RH-.5); fan(3.2,y0+4.6,RH-.5)
    for y in (y0+1.4,y0+4.5,y0+7.9): B.box((0,y,RH-.14),(RX,.14,.14),M('#C9B48A',.7,kind='wood',sc=.5),.02)
    B.box((0,(y0+y1)/2+.3,RH-.005),(RX,RDEP/2-.3,.01),M('#D9D2C2',.9),0)
    fr=M('#5E3A22',.6,kind='wood',sc=.6)
    for i,(yy,c1,c2) in enumerate(((y0+3.0,'#F2C14E','#C8372D'),(y0+5.6,'#6FC38A','#F4F1EA'),(y0+8.0,'#E28A3A','#7A1F2E'))):
        B.box((RX-.15,yy,2.9),(.03,.62,.48),fr,.01); B.box((RX-.18,yy,2.9),(.01,.54,.4),M(c1,.6),0); B.cyl((RX-.2,yy,2.86),.24,.02,M(c2,.5),rot=(0,R(90),0),seg=16)
        B.box((-RX+.15,yy,2.9),(.03,.62,.48),fr,.01); B.box((-RX+.18,yy,2.9),(.01,.54,.4),M(c2,.6),0); B.cyl((-RX+.2,yy,2.86),.24,.02,M(c1,.5),rot=(0,R(90),0),seg=16)
    sign('CASH ONLY',(-4.6,y1-.17,3.7),.3,'#16171C','#F2C14E',n=(0,-1,0),pad=.16,th=.04)
    sign('FAMILY HALL UPSTAIRS',(4.6,y1-.17,2.35),.2,'#FFFFFF','#7A1F2E',n=(0,-1,0),pad=.12,th=.04)
    # menu board + clock + shelf with jars on the back wall
    B.box((0,y1-.16,3.05),(2.5,.04,1.05),M('#1E4A36',.6),0); B.box((0,y1-.15,3.05),(2.6,.03,1.15),M('#D9B24A',.4,metal=.5),0)
    for i,(a,b) in enumerate((('MAGHAZ MASALA','350'),('NIHARI','400'),('KATAKAT','380'),('CHAI','50'))):
        text(a,(-.6,y1-.19,3.7-i*.42),(0,-1,0),.26,M('#FFF6D8',.5,emit=.6),ex=.006); text(b,(1.9,y1-.19,3.7-i*.42),(0,-1,0),.26,M('#F2C14E',.5,emit=.6),ex=.006)
    B.cyl((4.6,y1-.16,3.3),.42,.06,M('#F4F1EA',.5),rot=(R(90),0,0),seg=24); B.cyl((4.6,y1-.2,3.3),.45,.04,M('#2A2C34',.5),rot=(R(90),0,0),seg=24)
    B.box((4.6,y1-.21,3.42),(.015,.01,.14),M('#16171C',.5),0); B.box((4.72,y1-.21,3.3),(.12,.01,.015),M('#16171C',.5),0)
    B.box((-4.6,y1-.3,2.6),(1.5,.16,.03),M('#5E3A22',.6,kind='wood',sc=.6),.01)
    for k in range(8): B.cyl((-5.8+k*.35,y1-.3,2.8),.11,.34,M(['#C8372D','#F2C14E','#6FC38A','#B5713A','#E87AB8','#F4F1DE','#8A4A1E','#4D8FE8'][k],.3,spec=.8),seg=10)
    # wash basin on the right wall, drinks fridge on the left wall
    B.box((RX-.42,y1-1.4,1.0),(.3,.4,.08),M('#F6F4EE',.3,spec=.8),.04); B.cyl((RX-.3,y1-1.4,1.25),.02,.3,M('#C9CED8',.3,metal=.9),seg=6); B.box((RX-.17,y1-1.4,2.0),(.02,.36,.46),M('#BFE6F2',.1,spec=1),0)
    B.box((-RX+.6,y1-1.3,1.3),(.45,.55,1.3),M('#C8372D',.4,spec=.7),.04); B.box((-RX+1.06,y1-1.3,1.45),(.02,.45,1.0),lit('#DFF4FF',1.6,always=True),0)
    for j in range(3):
        for k in range(4): B.cyl((-RX+1.02,y1-1.62+k*.22,.75+j*.6),.07,.3,M(['#E8554D','#F2A11A','#6FC38A','#2A1E16'][(j+k)%4],.3,spec=.8),seg=8)
    # front counter with tawa (left bay), cash desk behind it
    T=tawa(-4.9,y0+1.1,0)
    B.box((-2.9,y0+2.6,.55),(.5,.9,.55),M('#5E3A22',.6,kind='wood',sc=.6),.03); B.box((-2.9,y0+2.6,1.12),(.55,.95,.03),M('#3A2A1E',.5),.01)
    B.box((-2.9,y0+2.9,1.3),(.22,.3,.14),M('#2A2C34',.5),.03)
    # low railing on the right bay front
    for x in (2.9,4.4,5.9,7.1): B.cyl((x,y0+.3,.55),.04,1.1,M('#2A2C34',.4,metal=.6),seg=6)
    B.box((5.0,y0+.3,1.08),(2.15,.04,.04),M('#2A2C34',.4,metal=.6),0); B.box((5.0,y0+.3,.6),(2.15,.03,.03),M('#2A2C34',.4,metal=.6),0)
RTAB=[(4.9,BW+2.7),(4.9,BW+6.4),(-4.6,BW+5.2),(-4.6,BW+8.0),(.6,BW+7.6)]
def rest_tables(dress=(0,1,2,1,2)):
    """tables + chairs in the restaurant. returns list of (table xy, [seat (x,y,rz)...])"""
    out=[]
    for i,(x,y) in enumerate(RTAB):
        ptable(x,y,0,dress=dress[i],seed=i); s1=(x-1.28,y,90); s2=(x+1.28,y,-90)
        for (sx,sy,rz) in (s1,s2): kchair(sx,sy,rz,['#C8372D','#2B58C9','#F4F1EA','#1E6A3A','#D9811A'][i])
        out.append(((x,y),[s1,s2]))
    return out
STAB=[(9.0,.8),(-9.0,-.8),(-15.0,.8),(15.0,-.8),(21.0,.8),(-21.0,-.8),(-27.0,.8),(27.0,-.8),(33.0,.8),(-33.0,-.8)]
def street_tables(n=10,dress=None,skip=()):
    out=[]
    for i,(x,y) in enumerate(STAB[:n]):
        if i in skip: out.append(None); continue
        ptable(x,y,0,dress=(dress[i] if dress else 1+i%2),seed=20+i); s1=(x-1.28,y,90); s2=(x+1.28,y,-90)
        for (sx,sy,rz) in (s1,s2): kchair(sx,sy,rz,['#2B58C9','#C8372D','#1E6A3A','#F4F1EA'][i%4])
        out.append(((x,y),[s1,s2]))
    return out
def burns(mood='night',seed=8,clock=(3,0),flood=False,rest=True,canopy=True,lights=True,roof=False,shadow=45,nost=(),rest_sign='CHACHA MAGHAZ HOUSE',night=None,cooks=True,far=.7,gap=None,roof_sx=0.0,nosigns=()):
    NIGHT[0]=(1.0 if mood in ('night','dusk') else 0.0) if night is None else night; r=random.Random(seed); FANS.clear()
    night=NIGHT[0]>0
    B.box((0,0,-.3),(260,260,.2),M('#55524C',.9,kind='concrete',sc=.4),0)
    B.box((0,0,-.03),(BX1-BX0,BW+1.3,.03),M('#8A7E6E' if night else '#9A9284',.65,kind='tile',sc=2.2,h2='#7E7364' if night else '#8E8678'),0)
    for s in (-1,1): B.box((0,s*(BW-.05),.05),(BX1-BX0,.08,.05),M('#B8B4A8',.7),0)
    for k in range(int((BX1-BX0)/2.4)): B.box((BX0+1.2+k*2.4,0,.004),(.5,.07,.004),M('#E8E2C8',.5),0)
    # buildings
    def _fill(a_,b_):
        xs=[a_]
        while b_-xs[-1]>13.5: xs.append(xs[-1]+r.uniform(6.6,9.6))
        if b_-xs[-1]>9.6: xs.append((xs[-1]+b_)/2)
        xs.append(b_); return [(xs[i],xs[i+1]) for i in range(len(xs)-1)]
    si=0
    segN=_fill(BX0-6,-RX)+[('REST',)]+_fill(RX,BX1+6) if rest else _fill(BX0-6,BX1+6)
    segS=_fill(BX0-6,ROOF_X[0])+[('ROOF',)]+_fill(ROOF_X[1],BX1+6)
    for s,segs in ((1,segN),(-1,segS)):
        for sg_ in segs:
            sg=B_SIGNS[si%len(B_SIGNS)]
            ns_=sg[0] in nosigns
            if sg_[0]=='REST': oldb(0,2*RX,3,'#E8D2A0',1,seed*100+si,sign_=rest_sign,scol='#1E6A3A',depth=RDEP+1.5,open_front=True,noac0=True)
            elif sg_[0]=='ROOF': oldb((ROOF_X[0]+ROOF_X[1])/2,ROOF_X[1]-ROOF_X[0],3,'#D99A8A',-1,seed*100+si,sign_=None if ns_ else sg[0],scol=sg[1],depth=12.0,plain_roof=True,sx=roof_sx,noac0=True)
            else:
                xa,xb=sg_; oldb((xa+xb)/2,xb-xa,r.randint(2,4),r.choice(OLDC),s,seed*100+si,sign_=None if ns_ else sg[0],scol=sg[1],noac0=True,depth=r.uniform(10,13),
                               blade_=(BLADES[si%len(BLADES)],r.choice(['#7A1F2E','#1E4A7A','#1E6A3A','#5A2A7A','#8A4A1E'])) if si%2==0 else None)
            si+=1
    if rest: restaurant()
    # far skyline behind both rows + street ends
    for s in (1,-1):
        x=BX0-60
        while x<BX1+70:
            w=r.uniform(9,18); h=r.uniform(22,60); y=s*(BW+r.uniform(22,48)); B.box((x+w/2,y,h/2),(w/2,7,h/2),M(r.choice(['#3A4258','#2E3648','#454C60','#39405A']) if night else r.choice(['#C9D6E0','#D9C4A8','#B8C4CC']),.8),0)
            for f in range(int(h//3.4)):
                for k in range(int(w//2.4)):
                    if r.random()<.42: B.box((x+1.2+k*2.4,y-s*7.02,4+f*3.4),(.6,.04,.8),lit(r.choice(WINL),r.uniform(1.6,3.0)) if night else M('#2A3444',.2,spec=.9),0)
            x+=w+r.uniform(1,7)
    C=clock_tower(BX1+11,0,*clock)
    # west end: closing block with an arch + banner
    B.box((BX0-10,0,9),(3,26,9),M('#C8B078',.85,kind='wall'),0)
    # banner arch over the street
    ax=-33.0; pm=M('#2A2C34',.4,metal=.5)
    for s in (-1,1): B.cyl((ax,s*(BW-.5),3.6),.14,7.2,pm,seg=8)
    B.box((ax,0,7.0),(.12,BW-.4,.75),lit('#7A1F2E',.8,.5,always=True),.02)
    for n in ((-1,0,0),(1,0,0)): text('BURNS ROAD FOOD STREET',(ax+n[0]*.14,0,7.0),n,.6,lit('#FFE9A0',3.4,always=True),ex=.012)
    for k in range(int((BW-.4)*2/.42)+1):
        for dz in (-.86,.86): B.ico((ax,-(BW-.4)+k*.42,7.0+dz),.055,lit(['#FF4F7A','#FFD23F','#35C8FF','#7CFC9A'][k%4],6,always=True),sub=1)
    if canopy:
        cols=['#FF4F7A','#FFD23F','#35C8FF','#7CFC9A','#FF8A3A','#FFF3D0']; bc=['#E8554D','#F2C14E','#4D8FE8','#6FC38A','#F4F1EA','#E87AB8','#FF8A3A']
        for i,x in enumerate(range(BX0+6,BX1-2,3)):
            if x-1.0<ax<x+4.0: continue
            sg_=1 if i%2==0 else -1
            if gap and gap[0]<=x<gap[1]: continue
            p0=(x,sg_*(BW-.62),6.8); p1=(x+3,-sg_*(BW-.62),6.8); n_=14
            for k in range(n_+1):
                f=k/n_; q=(L(p0[0],p1[0],f),L(p0[1],p1[1],f),p0[2]-.9*math.sin(pi*f)); B.ico(q,.075,lit(cols[(k+i)%len(cols)],5.5 if night else 1.0,always=True),sub=1)
                if k<n_:
                    f2=(k+1)/n_; q2=(L(p0[0],p1[0],f2),L(p0[1],p1[1],f2),p0[2]-.9*math.sin(pi*f2)); d=Vector(q2)-Vector(q)
                    B.cyl(tuple((Vector(q)+Vector(q2))/2+Vector((0,0,.05))),.008,d.length,M('#16171C',.5),rot=d.to_track_quat('Z','Y').to_euler(),seg=4)
        for i,x in enumerate(range(BX0+9,BX1-4,9)):          # bunting
            if abs(x-ax)<2.5 or (gap and gap[0]<=x<gap[1]): continue
            n_=17
            for k in range(n_):
                f=(k+.5)/n_; y=L(BW-.7,-(BW-.7),f); z=8.6-.7*math.sin(pi*f); B.box((x,y,z-.16),(.012,.15,.15),M(bc[(k+i)%len(bc)],.8,kind='fabric'),0,rot=(R(45),0,0))
            B.box((x,0,8.6-.35),(.008,BW-.7,.008),M('#16171C',.5),0)
    # street stations: tawas, grills, degs, carts along both fronts (clear of restaurant front)
    st=[]
    for i,x in enumerate(range(BX0+7,BX1-3,7)):
        for s in (1,-1):
            if s==1 and abs(x)<RX+1.5: continue
            if (s,x) in nost: continue
            k=(i+(0 if s==1 else 2))%4; y=s*(BW-1.4)
            if k==0: tawa(x,y,0 if s==1 else 180); st.append(('tawa',x,y,s))
            elif k==1: grill(x,y,0); st.append(('grill',x,y,s))
            elif k==2: deg(x-.6,y+s*.05,.9,lid=False); deg(x+.9,y+s*.05,.9,lid=True); st.append(('deg',x,y,s))
            else: cart(x,y,0 if s==1 else 180,r.choice(['#2B58C9','#C8372D','#1E6A3A','#7448C2']),r.choice(['KULFI','LASSI','GOLA GANDA','CHAAT','JUICE']),umb=r.choice(['#F2C14E','#E8554D','#35C8FF'])); st.append(('cart',x,y,s))
    if cooks:
        for (kd,x,y,s) in st:
            if kd=='cart': tok_h(r,x+1.75,y,0 if s==1 else 180)
            elif kd=='deg': tok_h(r,x+.15,y+s*1.02,0 if s==1 else 180,arms='fwd')
            else: tok_h(r,x-.3 if kd=='tawa' else x,y+s*.98,0 if s==1 else 180,arms='fwd')
    for s in (1,-1):
        for xx in list(range(BX0+3,-33,2))+list(range(35,BX1-2,2)):
            if r.random()<far: tok_h(r,xx+r.uniform(-.2,.2),s*r.uniform(2.15,3.05),90*s)
    if flood: B.box((0,0,.82),(BX1-BX0,BW+1.25,.02),M('#7A8A72',.1,spec=1.0,alpha=.86),0)
    B.done('burns')
    S=setup_world(mood,shadow); PL=[]
    if lights and night:
        for i,x in enumerate(range(BX0+8,BX1,9)): PL.append(point((x,(-1.5 if i%2 else 1.5),5.6),1300,(1,.8,.55),r=.8,shadow=False))
        if rest:
            PL.append(point((-3.4,BW+3.6,RH-1.0),230,(1,.9,.74),r=1.0,shadow=False)); PL.append(point((3.4,BW+3.6,RH-1.0),230,(1,.9,.74),r=1.0,shadow=True)); PL.append(point((0,BW+7.4,RH-1.0),190,(1,.9,.74),r=1.0,shadow=False))
    for p_ in PL: p_['e0']=p_.data.energy
    return dict(sun=S,clock=C,stations=st,lights=PL)
def spin_fans(t):
    for b in FANS: b.rotation_euler[2]=t*9.0
