# Worlds for "Everyone is from Islamabad" (vampire film). All new sets:
#   sector()  residential sector street along x: walled two-storey houses with balconies, bougainvillea, pines; junction + traffic signal at x=-21
#   viewpt()  Margalla view point at night: terrace, railing, city lights far below      track()  sunrise walking track in a park + office door
#   daftar()  the government office (towers of files)                                   deck()   pirate ship deck (one hook shot)
MOODS['ib_night']=dict(sun=(52,-40),e=.95,col=(.62,.72,1.0),top='#060A24',bot='#27336E',sky=.95,mist='#18214A',cloud='#2A3466',cov=.3,cstr=.55)
MOODS['ib_day']=dict(sun=(52,-38),e=2.5,col=(1,.95,.85),top='#2F86E0',bot='#CFE8FF',sky=.95,mist='#DCE8F2',cloud='#FFFFFF',cov=.6,cstr=.9)
MOODS['ib_noon']=dict(MOODS['ib_day'],sun=(50,-62),e=2.3)
MOODS['ib_gold']=dict(sun=(70,-56),e=2.6,col=(1,.82,.58),top='#5B86CC',bot='#FFD0A0',sky=.92,mist='#F0CDA8',cloud='#FFE0C0',cov=.4,cstr=.85)
MOODS['ib_dawn']=dict(sun=(80,84),e=2.4,col=(1,.72,.46),top='#6A7FD0',bot='#FFC08A',sky=.95,mist='#F2C8A8',cloud='#FFD0B0',cov=.4,cstr=.85)
MOODS['ib_pre']=dict(sun=(52,-40),e=.8,col=(.62,.72,1.0),top='#070A26',bot='#4A3A7A',sky=.95,mist='#1E2250',cloud='#3A3470',cov=.3,cstr=.55)
MOODS['ib_in']=dict(sun=(60,-160),e=.25,col=(1,.9,.8),top='#14140F',bot='#1E1C16',sky=.5,mist='#1A1812',cloud='#1E1C16',cov=.3,cstr=.5)
HX=[-63,-49,-35,-7,7,21,35,49,63]; HCOL=['#F1E8DA','#E6DCC8','#F6F4EE','#DDD2C0','#EDE4D2','#D9DEE2','#F4EFE4','#E2D6C2']; WINS=[]; SIG={}
BOUG=['#D83A8A','#E8559C','#C82A7A','#F06AA8']
def ilamp1(x,y,h=6.2,s=1):
    pm=M('#3A3D44',.5,metal=.5); B.cyl((x,y,h/2),.09,h,pm,seg=8,r2=.06); B.box((x,y-s*.9,h-.05),(.04,.9,.035),pm,0); B.box((x,y-s*1.7,h-.1),(.2,.42,.06),pm,.02); B.box((x,y-s*1.7,h-.17),(.15,.36,.02),lit('#FFD9A0',9.0),0)
def ihouse(cx,side,seed,awake=0.0):
    """two-storey house on a 14 m plot. side=+1 north of the road (front faces -y). gate at cx+2.4, balcony x cx-4..cx+2 at z 3.45"""
    r=random.Random(seed); s=side; wc=HCOL[seed%8]; wl=M(wc,.85,kind='wall'); ac=M(r.choice(['#8A5A36','#6B4A2E','#7A6A5A','#9A4A3A']),.7,kind='wood',sc=.6); gl=M('#18233A',.15,spec=1.0); wh=M('#F6F4EE',.7); dk=M('#2A2C34',.5,metal=.4)
    fy=s*9.0; cy=s*13.5; W=6.0; wy=s*6.2
    B.box((cx,cy,3.4),(W,4.5,3.4),wl,0); B.box((cx,cy,6.95),(W+.25,4.75,.15),wh,0); B.box((cx,cy,7.25),(W,4.5,.18),wl,0)
    B.box((cx+3.6,cy+s*1.5,8.2),(1.6,1.6,.8),wl,0); B.box((cx+3.6,cy+s*1.5,9.15),(1.9,1.9,.12),M('#9A4A3A',.8),0,rot=(R(s*8),0,0))
    B.cyl((cx-3.4,cy+s*1.0,8.0),.75,1.3,M(r.choice(['#2B58C9','#16171C','#E8E2D0']),.6),seg=10); B.box((cx-.5,cy-s*2,7.7),(.5,.4,.35),M('#C9CED8',.5,metal=.3),.04)
    B.box((cx+4.9,fy-s*.1,3.4),(.9,.12,3.4),ac,0)                                                                    # wood accent strip
    # windows / doors (front)
    for (wx,wz,hx,hz) in ((cx-3.1,1.7,1.3,.9),(cx-1.0,4.6,1.2,1.1),(cx+3.3,4.7,.8,.8)):
        B.box((wx,fy-s*.03,wz),(hx,.04,hz),gl,0); B.box((wx,fy-s*.06,wz-hz-.06),(hx+.1,.1,.06),wh,0); B.box((wx,fy-s*.06,wz),(.04,.05,hz),wh,0)
        if s>0: WINS.append((wx,fy-.09,wz,hx-.06,hz-.06))
        if r.random()<awake: B.box((wx,fy-s*.07,wz),(hx-.06,.01,hz-.06),lit(r.choice(['#FFD890','#FFE9B8']),3.0),0)
    B.box((cx+.9,fy-s*.04,1.25),(.6,.05,1.25),ac,.02); B.box((cx+.9,fy-s*.3,2.75),(1.2,.5,.08),wh,0)                                # door + canopy
    # balcony
    B.box((cx-1.0,fy-s*.9,3.45),(3.0,.9,.1),wh,0); B.box((cx-1.0,fy-s*1.76,3.95),(3.0,.03,.42),M('#BFE0F0',.1,spec=1.0,alpha=.35),0); B.box((cx-1.0,fy-s*1.76,4.42),(3.02,.05,.04),dk,0)
    for k in (-1,1): B.box((cx-1.0+k*3.0,fy-s*.9,3.98),(.04,.9,.46),dk,0)
    for k in (-1,1): B.box((cx-1.0+k*2.9,fy-s*1.7,1.72),(.1,.1,1.72),wl,0)
    # lawn + boundary wall + gate
    B.box((cx,s*7.6,.06),(6.9,1.35,.06),M('#3F7A3A',.95,kind='grass',sc=.6),0)
    bw=M(shade(wc,.93),.9,kind='wall'); cp=M(shade(wc,.75),.8)
    for (x0,x1) in ((cx-7.0,cx+.75),(cx+4.05,cx+7.0)): B.box(((x0+x1)/2,wy,.95),((x1-x0)/2,.12,.95),bw,0); B.box(((x0+x1)/2,wy,1.94),((x1-x0)/2+.02,.16,.05),cp,0)
    for gx in (cx+.9,cx+3.9): B.box((gx,wy,1.2),(.2,.2,1.2),bw,0); B.box((gx,wy,2.45),(.26,.26,.06),cp,0); B.ico((gx,wy,2.68),.16,lit('#FFE2A0',5.0),sub=1)
    gm=M(r.choice(['#2A2C34','#3A2A22','#27365A','#4A3D32']),.5,metal=.5); B.box((cx+2.4,wy,1.05),(1.3,.05,1.0),gm,0)
    for k in range(7): B.box((cx+1.25+k*.38,wy-s*.06,1.05),(.03,.02,.95),M('#C9A24A',.4,metal=.7),0)
    for k in range(r.randint(2,4)): bx=r.uniform(cx-6.3,cx+.2); B.ico((bx,wy+s*.1,1.95+r.uniform(0,.3)),r.uniform(.45,.75),M(r.choice(BOUG),.85,kind='leaves'),sc=(1.3,.7,.8),sub=1)
    pine(cx-5.6,s*7.7,r.uniform(.8,1.0)); B.ico((cx+5.6,s*7.6,.7),.6,M(GRN[seed%4],.85,kind='leaves'),sc=(1,1,.9),sub=1)
    if r.random()<.5: rtree(cx-2.5+r.uniform(-1,1),s*7.6,r.uniform(.7,.9),seed=seed)
def sector(mood='ib_night',night=1.0,awake=0.0,stars=True,signal='red'):
    """street along x. road y -4..4, walks 4..6, boundary walls at +-6.2, house fronts at +-9. junction (cross street along y) at x -25..-17. lamps on the north walk"""
    NIGHT[0]=night; S=setup_world(mood,shadow=75); r=random.Random(11); WINS.clear(); SIG.clear()
    B.box((0,0,-.1),(200,200,.1),M('#3F7A3A',.95,kind='grass',sc=2.0),0)
    asp=M('#303136',.92,kind='asphalt',sc=1.4); kb=M('#CFCBC0',.8,kind='concrete',sc=.5); pv=M('#B9AE9A',.85,kind='tile',sc=.7); wl=M('#F4F1EA',.6); yl=M('#F2C14E',.6)
    B.box((0,0,-.02),(120,4.0,.06),asp,0); B.box((-21,0,-.021),(4.0,120,.06),asp,0)
    for s in (1,-1):
        for (x0,x1) in ((-120,-25.6),(-16.4,120)): B.box(((x0+x1)/2,s*5.1,.08),((x1-x0)/2,1.1,.08),pv,0); B.box(((x0+x1)/2,s*4.06,.1),((x1-x0)/2,.08,.1),kb,.02)
        B.box((0,s*3.75,.045),(120,.05,.005),wl,0)
    for k in range(-30,31):
        if -26<k*4.0<-15: continue
        B.box((k*4.0,0,.045),(1.0,.06,.005),wl,0)
    for k in range(7): B.box((-15.2,-3.3+k*1.1,.046),(1.0,.3,.005),wl,0)                                         # zebra
    B.box((-16.6,-2.0,.046),(.12,1.9,.005),wl,0)
    for i,cx in enumerate(HX):
        ihouse(cx,1,20+i,awake); ihouse(cx+0,-1,40+i,awake)
    for k in range(-4,5):
        x=k*14.0
        if abs(x+21)<6: x+=7
        ilamp1(x,5.6)
        if night>0 and abs(x)<45: point((x,4.0,5.6),520*night,(1,.82,.56),r=.5,shadow=False)
    # rows behind + far city
    for s in (1,-1):
        for k in range(-6,7):
            x=k*14.0+r.uniform(-1,1); y=s*(27+r.uniform(0,2)); c=HCOL[(k+s)%8]; h=r.uniform(6,8)
            if abs(x+21)<6: continue
            B.box((x,y,h/2),(5.6,4.2,h/2),M(c,.9,kind='wall'),0); B.box((x,y,h+.1),(5.8,4.4,.12),M('#F6F4EE',.7),0); B.cyl((x+2,y,h+.8),.7,1.2,M('#2B58C9',.6),seg=8)
            for q in range(2):
                if r.random()<awake+.12: B.box((x-2.5+q*4,y-s*4.22,4.6),(.9,.02,.7),lit('#FFD890',2.5),0)
        for k in range(46): (pine if k%3 else rtree)(r.uniform(-110,110),s*r.uniform(21,23.5) if k<16 else s*r.uniform(34,95),r.uniform(1.0,1.9))
        for k in range(34):
            x=r.uniform(-120,120); y=s*r.uniform(40,110); w=r.uniform(4,7); h=r.uniform(6,12); B.box((x,y,h/2),(w,w,h/2),M(r.choice(HCOL),.9,kind='wall'),0)
            if r.random()<awake+.2: B.box((x,y-s*(w+.02),h*.6),(.8,.02,.6),lit('#FFD890',2.5),0)
    # traffic signal for traffic heading -x (stops at x=-16.4, lane y=-2)
    pm=M('#3A3D44',.5,metal=.5); B.cyl((-25.9,-4.9,2.6),.1,5.2,pm,seg=8); B.box((-25.7,-4.9,4.6),(.16,.2,.58),M('#16171C',.5),.03)
    for i,(nm,c) in enumerate((('red','#FF2A1A'),('yellow','#FFC21A'),('green','#2AE04A'))):
        on=(nm==signal); B.ico((-25.52,-4.9,4.98-i*.38),.13,M(c,.3,emit=(9.0 if on else .08)),sub=2)
    if signal=='red' and night>0: point((-24.6,-4.9,4.9),60,(1,.2,.15),r=.2,shadow=False)
    # Margalla + white mosque far north
    for (cx,cy,sx,sy,sz,c) in ((-90,215,110,34,44,'#2C5C34'),(50,225,120,36,56,'#27552F'),(170,212,80,30,40,'#2C5C34'),(0,270,200,40,76,'#21482A'),(-150,250,90,34,58,'#21482A')):
        B.ico((cx,cy,-2),1.0,M(c,.95,kind='leaves',sc=3.0),sc=(sx,sy,sz),sub=3)
    mw=M('#F6F4EE',.5); B.cyl((70,150,8),20,16,mw,seg=8,r2=1.2); B.box((70,150,1.5),(21,21,1.5),mw,0)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((70+sx*23,150+sy*23,18),1.3,36,mw,seg=8,r2=.8); B.cyl((70+sx*23,150+sy*23,38.5),.8,5,M('#E6B93A',.3,metal=.8),seg=8,r2=.05)
    if stars and night>.5:
        for k in range(170): a=r.uniform(0,6.283); el=r.uniform(.1,1.25); d=430; B.ico((d*math.cos(a)*math.cos(el),d*math.sin(a)*math.cos(el),d*math.sin(el)),r.uniform(.5,1.2),M('#FFFFFF',.3,emit=6.0),sub=1)
        B.ico((-70,400,170),22,M('#FFF6D8',.3,emit=3.2),sub=3)
    B.done('sector'); return S
def sboard(body,loc,n=(0,-1,0),size=.34,pole_h=None,bg='#1E6A3A'):
    """green sector board on a pole (built into the batch: call before B.done or follow with B.done)"""
    x,y,z=loc
    if pole_h: B.cyl((x-n[0]*.08,y-n[1]*.08,pole_h/2),.06,pole_h,M('#C9CED8',.4,metal=.5),seg=8)
    sign(body,(x,y,z),size,'#FFFFFF',bg,n=n,e=1.6,pad=.2,th=.06,frame='#F6F4EE')
# ================================================================ Margalla view point
def viewpt(mood='ib_pre',board=True):
    """terrace x -9..9, y -2..9. railing on the south edge (y=-2): the city lies far below to the south. bench at (-1.5,1.6) facing south. pines + hill rise to the north"""
    NIGHT[0]=1.0; S=setup_world(mood,shadow=60); r=random.Random(31)
    st=M('#8E8778',.9,kind='tile',sc=.9); B.box((0,3.5,-.15),(9.5,5.6,.15),st,0); B.box((0,-2.15,.25),(9.6,.25,.4),M('#7A7468',.9,kind='concrete',sc=.6),.04)
    for k in range(-4,5): B.box((k*2.3,-2.15,.95),(.16,.16,.5),M('#7A7468',.9,kind='concrete'),.03); B.ico((k*2.3,-2.15,1.52),.13,M('#8A8478',.8),sub=1)
    for z in (.85,1.25): B.box((0,-2.15,z),(9.4,.045,.045),M('#2A2C34',.5,metal=.5),0)
    B.box((0,-80,-46),(700,80,.5),M('#0C1020',.95),0); B.box((0,-420,-46),(900,300,.5),M('#0A0E1C',.95),0)
    # the city below: sectors = blocks of lights, avenues = bright lines
    lc=['#FFD48A','#FFE9B8','#FFB060','#BFE6FF','#FFF6D8']
    for bx in range(-9,10):
        for by in range(1,13):
            x0=bx*46; y0=-70-by*42
            if r.random()<.1: continue
            for k in range(24): B.ico((x0+r.uniform(-18,18),y0+r.uniform(-16,16),-45+r.uniform(0,3)),r.uniform(.35,.8),M(r.choice(lc),.3,emit=9.0),sub=1)
    for by in (2,6,10):
        for k in range(120): B.ico((-460+k*7.8,-70-by*42+21,-45),.7,M('#FFB060',.3,emit=12.0),sub=1)
    for bx in (-3,2):
        for k in range(70): B.ico((bx*46+23,-80-k*7.5,-45),.7,M('#FFE9B8',.3,emit=12.0),sub=1)
    # slope below the railing + trees
    B.ico((0,-14,-26),1.0,M('#14301E',.95,kind='leaves',sc=2.0),sc=(60,14,26),sub=3)
    for k in range(26): pine(r.uniform(-34,34),r.uniform(-9,-4.2),r.uniform(1.2,2.0),z=r.uniform(-9,-5),col='#1E4A2A')
    # north: rising hill, pines
    B.ico((0,34,-4),1.0,M('#183A22',.95,kind='leaves',sc=2.0),sc=(70,24,16),sub=3); B.ico((-40,60,-4),1.0,M('#14301E',.95,kind='leaves',sc=2.0),sc=(80,30,30),sub=3); B.ico((50,70,-4),1.0,M('#14301E',.95),sc=(80,30,36),sub=3)
    for k in range(44):
        x=r.uniform(-30,30); y=r.uniform(10.5,26); pine(x,y,r.uniform(1.3,2.2),z=max(0,(y-9)*.42)-.4,col=r.choice(['#1E4A2A','#24552F','#1A4226']))
    for (x,y) in ((-7.6,7.4),(7.8,6.6),(-8.2,.6),(8.3,1.2)): pine(x,y,1.5,col='#24552F')
    # bench, lamp, telescope, bin, sign
    wd=M('#8A5A36',.6,kind='wood',sc=.6); dk=M('#2A2C34',.5,metal=.5)
    B.box((-1.5,1.6,.62),(1.3,.3,.045),wd,.02); B.box((-1.5,1.98,1.05),(1.3,.04,.28),wd,.02)
    for k in (-1,1): B.box((-1.5+k*1.1,1.7,.3),(.05,.3,.3),dk,.01)
    B.cyl((4.6,3.2,2.2),.09,4.4,dk,seg=8); B.ico((4.6,3.2,4.55),.3,lit('#FFD9A0',8.0,always=True),sub=2); B.box((4.6,3.2,4.9),(.36,.36,.05),dk,.02); point((4.6,3.0,4.2),480,(1,.82,.56),r=.4,shadow=False)
    B.cyl((-5.2,-1.2,.7),.06,1.4,dk,seg=8); B.cyl((-5.2,-1.35,1.5),.13,.6,M('#C9CED8',.3,metal=.8),rot=(R(78),0,0),seg=12)
    dustbin(6.6,-.8)
    if board:
        for k in (-1,1): B.cyl((3.2+k*1.9,8.4,1.3),.08,2.6,wd,seg=6)
        sign('MARGALLA VIEW POINT',(3.2,8.3,2.3),.3,'#FFFFFF','#2F5D50',n=(0,-1,0),e=1.5,pad=.2,th=.06,frame='#E6B93A')
    for k in range(190): a=r.uniform(0,6.283); el=r.uniform(.08,1.25); d=520; B.ico((d*math.cos(a)*math.cos(el),d*math.sin(a)*math.cos(el),d*math.sin(el)),r.uniform(.6,1.4),M('#FFFFFF',.3,emit=6.0),sub=1)
    B.ico((60,-470,150),24,M('#FFF6D8',.3,emit=3.2),sub=3)
    B.done('viewpt'); return S
# ================================================================ sunrise walking track (+ the office door at the west end)
def track(mood='ib_dawn'):
    """track along x (y -2.6..2.6), sun low in the east (+x). big tree with shade at (0,5.2). grey office block north-west: door at (-26,9.4) facing south"""
    NIGHT[0]=0.0; S=setup_world(mood,shadow=110); r=random.Random(53)
    B.box((0,0,-.1),(220,160,.1),M('#5A9A46',.95,kind='grass',sc=2.0),0); B.box((0,0,-.02),(160,2.6,.06),M('#B8674A',.9,kind='asphalt',sc=1.0),0)
    for s in (1,-1): B.box((0,s*2.5,.045),(160,.06,.005),M('#F4F1EA',.6),0); B.box((0,s*2.75,.06),(160,.1,.06),M('#CFCBC0',.8),.02)
    for k in range(-30,31): B.box((k*5.0,0,.045),(.06,2.4,.005),M('#F4F1EA',.6),0) if k%4==0 else None
    for k in range(-9,10):
        x=k*11.0+3
        if abs(x)<4 or abs(x+26)<7: continue
        (jac if k%3==0 else (pine if k%3==1 else rtree))(x,6.4+r.uniform(-.5,.8),r.uniform(1.2,1.6),**({'seed':k} if k%3!=1 else {}))
        (rtree if k%2 else pine)(x+4,-6.2+r.uniform(-.8,.5),r.uniform(1.2,1.6))
    rtree(0,5.4,2.1,seed=5)                                                           # the shade tree
    for k in range(70): (pine if k%3 else rtree)(r.uniform(-110,110),r.choice((-1,1))*r.uniform(12,70),r.uniform(1.2,2.2))
    for k in range(-5,6):
        if k%2==0: bench(k*13.0+6,-3.9,0)
        else: dustbin(k*13.0+6,-3.6)
        flowers(k*13.0-2,k*13.0+2,3.3,4.0,10,k+70,z=.12)
    # exercise bars
    dk=M('#2B58C9',.5,metal=.4)
    for k in (-1,1): B.cyl((12+k*1.0,-5.2,1.1),.06,2.2,dk,seg=8)
    B.cyl((12,-5.2,2.15),.045,2.0,M('#F2C14E',.4,metal=.5),rot=(0,R(90),0),seg=8)
    # office block
    cc=M('#9A9890',.9,kind='concrete',sc=.9); B.box((-26,16,5.5),(9,6.5,5.5),cc,0); B.box((-26,16,11.15),(9.3,6.8,.15),M('#7E7C74',.9),0)
    for f in range(3):
        for k in range(-3,4):
            if f==0 and abs(k)<1: continue
            B.box((-26+k*2.4,9.47,2.3+f*3.4),(.8,.04,.9),M('#3A4656',.3),0); B.box((-26+k*2.4,9.42,1.3+f*3.4),(.95,.1,.06),M('#7E7C74',.9),0)
    B.box((-26,9.46,1.35),(1.0,.05,1.35),M('#14161C',.9),0); B.box((-26,9.3,2.85),(1.5,.3,.1),M('#7E7C74',.9),0)
    for k in range(3): B.box((-26,8.6-k*.4,.12+.0-k*.04),(1.8,.2,.06),M('#8A8880',.9),0)
    sign('DEPARTMENT OF PENDING FILES',(-26,9.36,3.6),.3,'#FFFFFF','#27365A',n=(0,-1,0),e=.0,pad=.2,th=.06,frame='#E6B93A')
    for (cx,cy,sx,sy,sz,c) in ((-70,215,95,34,40,'#4A8A4E'),(40,225,110,36,52,'#427C46'),(140,212,80,30,38,'#4A8A4E'),(0,265,170,40,70,'#3A7040')):
        B.ico((cx,cy,-2),1.0,M(c,.95,kind='leaves',sc=3.0),sc=(sx,sy,sz),sub=3)
    B.ico((300,-40,22),15,M('#FFE2A0',.3,emit=9.0),sub=3)                                # the sun, low in the east
    for k in range(24): x=r.uniform(-120,120); y=r.choice((-1,1))*r.uniform(60,130); w=r.uniform(5,9); h=r.uniform(8,20); B.box((x,y,h/2),(w,w,h/2),M(r.choice(HCOL),.9,kind='wall'),0)
    B.done('track'); return S
# ================================================================ the office
def daftar(night=False,coffin=False,plate=False,files2=True):
    """room x -6..6, y -4.5..5, open to -y. clerk's desk at (-2.6,1.4), second desk at (2.4,1.4) (chairs behind at y 2.6). door in the back wall at x=4.9"""
    NIGHT[0]=1.0; S=setup_world('ib_in',shadow=30); r=random.Random(9); wl=M('#C9C2A8',.9,kind='wall'); wd=M('#6B4A2E',.6,kind='wood',sc=.6); wd2=M('#8A6238',.55,kind='wood',sc=.6); st=M('#6E7A72',.5,metal=.5)
    B.box((0,-3,-.1),(8,10,.1),M('#8A8274',.9,kind='tile',sc=.9),0); B.box((0,5.1,2.6),(6.3,.1,2.6),wl,0)
    for sx in (-1,1): B.box((sx*6.3,-3,2.6),(.1,8.2,2.6),wl,0)
    B.box((0,-3,5.3),(6.4,8.3,.1),M('#D8D2BC',.9),0); B.box((0,5.0,.5),(6.2,.03,.5),M('#7A8A72',.8),0)
    FC=['#D9C9A0','#C9B48A','#E8D8B0','#B8A47A','#8FB8D8','#E8A0A0','#A8C8A0','#F2D48A']
    def stack(x,y,n,seed,w=.34,d=.26):
        q=random.Random(seed)
        for k in range(n): B.box((x+q.uniform(-.04,.04),y+q.uniform(-.03,.03),.05+k*.085),(w,d,.04),M(q.choice(FC),.8),.006,rot=(0,0,q.uniform(-.2,.2)))
    for k in range(16):
        x=-5.6+k*.74
        if 4.0<x<5.8: continue
        stack(x,4.55,r.randint(18,40),k)
    for k in range(9): stack(-5.7,3.6-k*.75,r.randint(10,30),40+k);
    for k in range(6): stack(5.7,3.6-k*.75,r.randint(10,26),60+k)
    for (ax,ay) in ((-.4,4.5),(1.6,4.5)): B.box((ax,ay,1.3),(.7,.35,1.3),st,.02); B.box((ax,ay-.36,1.3),(.02,.01,1.2),M('#4A5650',.5),0); stack(ax,ay,7,80+int(ax),w=.3)
    for i,(dx,ch) in enumerate(((-2.6,True),(2.4,True))):
        B.box((dx,1.4,.5),(1.3,.6,.5),wd,.03); B.box((dx,1.4,1.03),(1.4,.68,.04),wd2,.02)
        if i==0 or files2: stack(dx-.95,1.5,6+i*5,90+i); stack(dx+1.0,1.3,3+i*6,95+i)
        B.box((dx,2.75,.62),(.36,.36,.05),M('#3A3D44',.7,kind='fabric'),.04); B.box((dx,3.1,1.25),(.36,.05,.6),M('#3A3D44',.7,kind='fabric'),.05)
        for ex in (-.28,.28):
            for ey in (-.28,.28): B.cyl((dx+ex,2.75+ey,.3),.03,.6,M('#2A2C34',.4,metal=.5),seg=5)
    B.cyl((-2.0,1.25,1.2),.16,.04,M('#2F5D50',.5),seg=10); B.cyl((-2.0,1.25,1.42),.025,.44,M('#C9A24A',.3,metal=.8),seg=6); B.box((-2.0,1.2,1.66),(.2,.12,.07),M('#2F7D50',.5,emit=.6),.04); point((-2.0,1.0,1.5),26,(.7,1,.75),r=.15,shadow=False)
    B.cyl((-5.2,4.96,3.7),.42,.05,M('#F4F1EA',.5),rot=(R(90),0,0),seg=20); B.box((-5.2,4.92,3.82),(.015,.01,.16),M('#16171C',.5),0); B.box((-5.08,4.92,3.7),(.13,.01,.015),M('#16171C',.5),0)
    sign('KAAM JAARI HAI',(-2.2,4.98,4.3),.24,'#16171C','#E8D8B0',n=(0,-1,0),pad=.16,th=.04,frame='#6B4A2E')
    # window (west wall) with blinds
    B.box((-6.18,-.4,2.9),(.03,1.2,1.0),M('#F2D8A0',.3,emit=(.25 if night else 2.2)),0)
    for k in range(11): B.box((-6.14,-.4,1.98+k*.19),(.03,1.25,.075),M('#B8B09A',.8),0)
    # door in the back wall
    B.box((4.9,5.02,1.35),(.85,.05,1.4),wd,.02); B.box((4.9,4.98,1.9),(.55,.02,.6),M('#BFD0D8',.2,emit=(.1 if night else .9)),0); B.cyl((4.3,4.94,1.3),.05,.1,M('#E6B93A',.3,metal=.9),rot=(R(90),0,0),seg=8)
    # tube lights (dim) + cobweb corner
    for k in (-3,2.5): B.box((k,0,5.12),(.9,.07,.04),lit('#E8F0D8',2.2 if not night else 1.2,always=True),0)
    if coffin:
        cm=M('#3A2618',.6,kind='wood',sc=.5); B.box((-4.3,3.9,1.55),(.62,.26,1.55),cm,.06,rot=(R(8),0,0)); B.box((-4.3,3.6,1.55),(.5,.02,1.4),M('#5A3A22',.6),.02,rot=(R(8),0,0)); B.box((-4.3,3.56,2.3),(.05,.01,.4),M('#E6B93A',.3,metal=.8),0,rot=(R(8),0,0)); B.box((-4.3,3.56,2.4),(.22,.01,.05),M('#E6B93A',.3,metal=.8),0,rot=(R(8),0,0))
        sign('IN A MEETING',(-4.3,3.42,1.3),.15,'#16171C','#F4F1EA',n=(0,-1,0),pad=.1,th=.02,frame='#C8372D')
    if plate:
        B.box((2.4,.86,1.12),(.62,.06,.1),M('#16171C',.5),.01,rot=(R(-18),0,0)); text('C. DRACULA  GRADE-17',(2.4,.79,1.125),(0,-.95,.31),.1,M('#E6B93A',.4,emit=.4),ex=.004)
    point((0,-2.5,3.0),420 if not night else 300,(1,.93,.78),r=1.2,shadow=False); point((-3.5,2.0,3.2),150,(1,.9,.7),r=1.0,shadow=False); point((3.5,2.0,3.2),150,(.85,.95,1.0),r=1.0,shadow=False)
    B.done('daftar'); return S
# ================================================================ pirate ship deck (hook)
def deck():
    NIGHT[0]=0.0; S=setup_world('ib_day',shadow=40); r=random.Random(5); wd=M('#9A6A3E',.7,kind='wood',sc=.5); wd2=M('#6B4A2E',.7,kind='wood',sc=.5)
    B.box((0,0,-30.2),(600,600,.2),M('#1E7AA8',.25,spec=.9),0)
    for k in range(60): B.box((r.uniform(-200,200),r.uniform(-30,220),-29.95),(r.uniform(2,6),.25,.05),M('#DFF2FA',.5),0)
    B.box((0,2,-.15),(6,9,.15),wd,0)
    for k in range(-8,9): B.box((k*.7,2,.005),(.015,9,.005),wd2,0)
    for s in (-1,1):
        B.box((s*5.9,2,.55),(.12,9,.55),wd2,.03); B.box((s*5.9,2,1.14),(.2,9,.06),wd,.03)
    B.box((0,10.9,.55),(6,.12,.55),wd2,.03); B.box((0,10.9,1.14),(6.1,.2,.06),wd,.03)
    B.cyl((0,5.5,7),.3,14,wd2,seg=10); B.box((0,5.4,8.2),(4.6,.06,3.2),M('#C9BEA6',.95,kind='fabric'),.04); B.box((0,5.45,11.6),(4.9,.1,.1),wd2,0); B.box((0,5.45,4.9),(4.9,.1,.1),wd2,0)
    B.box((0,5.3,13.6),(.9,.02,.55),M('#16171C',.8,kind='fabric'),0); B.ico((0,5.26,13.6),.22,M('#F4F1EA',.6),sub=1)
    for (x,y) in ((-3.6,7.5),(-4.4,6.4),(3.9,8.2)): B.cyl((x,y,.55),.5,1.1,wd2,seg=12); B.cyl((x,y,.3),.52,.06,M('#3A3D44',.5,metal=.5),seg=12); B.cyl((x,y,.85),.52,.06,M('#3A3D44',.5,metal=.5),seg=12)
    B.box((3.6,4.2,.4),(.7,.5,.4),wd2,.04); B.box((3.6,4.2,.84),(.72,.52,.05),M('#E6B93A',.3,metal=.8),.02)
    B.done('deck'); return S
