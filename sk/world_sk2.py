# Sialkot film, sets D-G: Scotland, the factory yard, the field/airport, Waleed's house gate.
# ---------------------------------------------------------------- set D: Scotland
def scotland():
    """a flat-topped grassy knoll at the origin (top z=1.0, radius 3) in highland hills, a loch behind"""
    NIGHT[0]=0.0; S=setup_world('sk_scot',shadow=70); r=random.Random(8); g1=M('#5E8A46',.95,kind='grass'); g2=M('#6E9A52',.95,kind='grass')
    B.box((0,0,-.1),(160,160,.1),g1,0); B.cyl((0,0,.5),3.0,1.0,g2,seg=28); B.ico((0,0,.1),5.4,g2,sc=(1,1,.2),sub=2)
    for (x,y,sx,sy,sz,c) in ((-38,62,34,24,13,'#4E7A40'),(26,70,40,26,17,'#587F4A'),(70,48,30,24,12,'#628A50'),(-74,40,30,22,11,'#567E46'),(0,110,60,30,22,'#6A8A66'),(-30,30,14,10,3.2,'#6E9A52'),(30,26,16,12,3.6,'#64904A')):
        B.ico((x,y,0),1.0,M(c,.95,kind='grass'),sc=(sx,sy,sz),sub=3)
    B.box((6,46,.04),(30,12,.04),M('#5E86A8',.2,spec=.9),0)                         # the loch
    for k in range(34):
        x=r.uniform(-16,16); y=r.uniform(2.5,22)
        if abs(x)<4.5 and y<6.5: continue
        B.ico((x,y,.3),r.uniform(.35,.7),M(r.choice(['#8A5A9A','#A06AA8','#7A4A8A','#B87AB0']),.9,kind='leaves'),sc=(1.3,1.2,.7),sub=1)
    for k in range(9): x=r.uniform(-14,14); y=r.uniform(6.5,20); B.ico((x,y,.2),r.uniform(.4,.9),M(r.choice(['#8A8E92','#7A7E82','#9A9E9E']),.9),sc=(1.2,1,.7),sub=1)
    for k in range(22): B.box((-11+k*1.0,12+.5*math.sin(k*.7),.45+.05*(k%2)),(.48,.3,.45),M(['#8A8E92','#7A7E82','#9A9E9E'][k%3],.9),.08,rot=(0,0,R(8*math.sin(k))))   # dry-stone wall
    for (x,y,rz) in ((-7,8,20),(-9.5,9.5,-40),(8,9,160),(10.5,7.5,100),(5,16,60)):      # sheep
        e=empty((x,y,0),rot=(0,0,R(rz))); obox((0,0,.7),(.55,.36,.34),M('#F4F1EA',.95,kind='fabric'),.2,e); obox((.62,0,.78),(.2,.17,.17),M('#2A2C34',.7),.07,e)
        for q in ((-.35,-.2),(.35,-.2),(-.35,.2),(.35,.2)): obox((q[0],q[1],.2),(.06,.06,.2),M('#2A2C34',.7),.02,e)
    B.box((-22,30,1.6),(3.4,2.4,1.6),M('#9A9A96',.9,kind='wall'),.03); B.box((-22,30,3.7),(3.7,2.7,.12),M('#4A4E56',.8),0); B.box((-22,30,4.3),(3.4,1.5,.55),M('#4A4E56',.8),.05); B.box((-20,30,5.0),(.3,.3,.7),M('#8A8E92',.9),.02)
    B.box((-22,27.58,1.0),(.45,.04,1.0),M('#5A3A22',.7,kind='wood'),0)
    for q in (-1.7,1.7): B.box((-22+q,27.58,2.0),(.45,.04,.5),M('#FFE9A8',.3,emit=1.0),0)
    B.done('scot'); return S
# ---------------------------------------------------------------- set E: Chacha Rafiq's factory yard
def factory():
    """yard: factory front along y=9 (roller door x -3..3), carton wall on the left (x -11.6..-8.2, y 6.8), container truck on the right. open towards -y"""
    NIGHT[0]=0.0; S=setup_world('sk_day',shadow=70); r=random.Random(14); wl=M('#E6D6BE',.85,kind='wall'); br=M('#B8573A',.85,kind='wall'); tr=M('#F2EBDA',.8)
    B.box((0,0,-.1),(60,40,.1),M('#9A948A',.9,kind='concrete',sc=1.4),0)
    B.box((0,14,4.0),(15,5,4.0),wl,0); B.box((0,9.0,.6),(15,.08,.6),br,0); B.box((0,14,8.15),(15.3,5.3,.15),tr,0)
    B.box((0,9.3,2.0),(3.0,.5,2.0),M('#1A1C22',.8),0)                               # the open roller door: dark inside, shelves of boxes
    B.box((0,8.98,4.25),(3.25,.1,.25),M('#8A8E96',.5,metal=.5),.02); B.box((0,8.96,3.9),(3.0,.06,.14),M('#6E7378',.5,metal=.5),0)
    for row in range(3):
        for k in range(8): B.box((-2.6+k*.75,8.95,.5+row*1.05),(.32,.2,.42),M(r.choice(['#C9A26A','#B88A52','#D8B47A']),.85),.02)
    sign('RAFIQ & SONS',(0,8.93,5.7),.62,'#FFF6D8','#0B6B3C',n=(0,-1,0),pad=.2,th=.12,frame='#E6B53A')
    sign('SPORTS GOODS EXPORTERS, SIALKOT',(0,8.93,4.78),.24,'#16171C','#F2EBDA',n=(0,-1,0),pad=.1,th=.08)
    for q in (-11,-7,7,11):
        B.box((q,8.97,5.2),(1.0,.05,.9),M('#27344A',.3,spec=.8),0); B.box((q,8.94,4.25),(1.15,.09,.06),tr,0)
        for qq in (-.5,0,.5): B.box((q+qq,8.95,5.2),(.03,.04,.9),tr,0)
    LAB=['GERMANY','BRAZIL','JAPAN','ENGLAND','U.S.A.','SPAIN','QATAR','FRANCE','ITALY','TURKEY','CANADA','MEXICO','CHINA','AUSTRALIA','U.A.E.','KOREA','EGYPT','KENYA','SWEDEN','POLAND','MALAYSIA']; k=0
    for row in range(7):                                                            # the tower of cartons, each going to a different country
        for col in range(3):
            if row==6 and col==2: continue
            carton_b(-11.6+col*1.72,6.8,.14+row*1.02,.84,.6,.5,LAB[k%21],n=(0,-1,0),size=.2 if len(LAB[k%21])<8 else .16); k+=1
    for q in (-11.6,-9.88,-8.16): B.box((q,6.8,.07),(.84,.62,.07),M('#8A6A46',.8,kind='wood'),0)
    e=empty((11.0,5.4,0)); cb=M('#2B58C9',.5,metal=.3); obox((.6,0,2.6),(3.6,1.25,1.3),cb,.03,e)             # container truck, side on
    for q in range(12): obox((-2.7+q*.6,-1.26,2.6),(.05,.02,1.25),M(shade('#2B58C9',.8),.5),0,e)
    obox((.6,0,1.2),(3.8,1.1,.12),M('#2A2C34',.6),.02,e); obox((-4.3,0,1.75),(.95,1.2,1.0),M('#F4F1EA',.4),.12,e); obox((-4.95,0,2.1),(.3,1.05,.5),M('#27344A',.2,spec=.9),.04,e)
    obox((-5.25,0,.95),(.1,1.2,.25),M('#C9CED8',.3,metal=.8),.03,e)
    for sx in (-4.3,1.6,3.0):
        for sy in (-1.05,1.05): wheel((sx,sy,.55),.55,.3,e)
    text('EXPORT',(11.6,5.4-1.3,2.6),(0,-1,0),.9,M('#F4F1EA',.5),ex=.01)
    for (x,y,s_) in ((-14.5,2.5,1.5),(15.5,-1.5,1.3)): tree(x,y,s_)
    B.box((0,-9,1.4),(30,.2,1.4),M('#D8C4A0',.85,kind='wall'),0); B.box((0,-9,2.9),(30,.28,.1),br,0)
    for (x,y) in ((5.2,7.6),(-5.0,7.8)): B.cyl((x,y,.35),.34,.55,br,seg=10,r2=.28); B.ico((x,y,1.0),.55,M('#4F8A3A',.85,kind='leaves'),sub=1)
    B.done('factory'); return S
# ---------------------------------------------------------------- set F: the empty field / the airport
def plane(parent=None):
    """airliner about 30 long, nose towards +x, wheels on z=0. plain white with a green tail (no airline markings)"""
    e=empty((0,0,0),parent); wh=M('#F6F6F2',.35,spec=.8); gn=M('#0B6B3C',.5); gy=M('#B8BEC8',.35,metal=.6)
    ocyl((0,0,3.4),1.75,22,wh,e,rot=(0,R(90),0),seg=20); oico((11,0,3.4),1.75,wh,e,sc=(2.0,1,1),sub=3); oico((-11,0,3.6),1.75,wh,e,sc=(3.2,.9,.85),sub=3)
    obox((12.7,0,3.9),(.5,1.0,.3),M('#16202E',.2,spec=.9),.1,e,rot=(0,R(18),0))
    for q in range(20): obox((-8.5+q*.95,-1.74,3.9),(.2,.03,.22),M('#16202E',.3),.02,e); obox((-8.5+q*.95,1.74,3.9),(.2,.03,.22),M('#16202E',.3),.02,e)
    for sy in (-1,1):
        obox((-1.2,sy*7.4,2.9),(1.9,6.2,.16),wh,.06,e,rot=(0,0,R(-sy*20))); ocyl((1.2,sy*4.6,2.0),.82,3.0,gy,e,rot=(0,R(90),0),seg=14); ocyl((2.6,sy*4.6,2.0),.6,.3,M('#16171C',.5),e,rot=(0,R(90),0),seg=14)
        obox((-13.6,sy*2.6,4.2),(.9,2.2,.1),wh,.04,e,rot=(0,0,R(-sy*24)))
        ocyl((-.6,sy*2.2,1.2),.08,1.6,gy,e,rot=(0,0,0),seg=6); wheel((-.6,sy*2.2,.55),.55,.35,e)
    obox((-13.6,0,6.6),(1.5,.12,2.4),gn,.05,e,rot=(0,R(-28),0)); obox((0,0,2.05),(9.5,1.76,.06),gn,0,e)
    ocyl((9.2,0,1.2),.07,1.6,gy,e,rot=(0,0,0),seg=6); wheel((9.2,0,.45),.45,.3,e)
    return e
def airfield(built=True):
    """same place before/after: built=False is an empty field, built=True has the terminal (y=40), apron and runway (along x at y=22)"""
    NIGHT[0]=0.0; S=setup_world('sk_day',shadow=110); r=random.Random(21)
    B.box((0,40,-.1),(220,160,.1),M('#7FA650',.95,kind='grass',sc=3),0)
    for k in range(60):
        x=r.uniform(-70,70); y=r.uniform(-6,70)
        if built and (10<y<54): continue
        B.ico((x,y,.18),r.uniform(.3,.7),M(r.choice(['#6E964A','#88AE58','#5E8A40']),.95,kind='leaves'),sc=(1.3,1.2,.5),sub=1)
    for k in range(26): x=-90+k*7.5+r.uniform(-2,2); tree(x,96+r.uniform(-4,4),r.uniform(2.2,3.4),col=r.choice(['#4F8A3A','#3F7A3A','#5F9A4A']))
    for (x,y,sx,sy,sz) in ((-60,140,60,30,14),(40,150,70,30,18),(110,130,50,26,12)): B.ico((x,y,0),1.0,M('#8AA690',.95),sc=(sx,sy,sz),sub=3)
    if built:
        B.box((0,22,.02),(110,3.6,.02),M('#3A3D44',.9,kind='concrete',sc=2),0)
        for k in range(22): B.box((-100+k*9.5,22,.045),(2.4,.14,.006),M('#F8F8F4',.6),0)
        B.box((0,33,.02),(34,6.5,.02),M('#8A8E92',.9,kind='concrete',sc=2),0)
        gl=M('#5A9AC8',.15,spec=1.0); wh=M('#F4F1EA',.6)
        B.box((0,45,3.6),(22,4.5,3.6),wh,.05); B.box((0,40.46,3.3),(21,.06,2.6),gl,0)
        for k in range(15): B.box((-21+k*3.0,40.42,3.3),(.08,.05,2.6),wh,0)
        B.box((0,44.6,7.5),(23,5.2,.3),M('#0B6B3C',.6),.05); B.box((0,40.4,.5),(21,.1,.5),M('#C9CED8',.5),0)
        B.cyl((27,46,7),1.6,14,wh,seg=14); B.cyl((27,46,15),2.8,2.2,gl,seg=14,r2=2.3); B.cyl((27,46,16.4),3.0,.5,M('#0B6B3C',.6),seg=14)
        sign('SIALKOT INTERNATIONAL AIRPORT',(0,40.2,9.3),.95,'#FFF6D8','#0B6B3C',n=(0,-1,0),pad=.3,th=.2,frame='#E6B53A')
        for k in range(9): B.cyl((-32+k*8,39,2.2),.07,4.4,M('#6E7378',.5,metal=.5),seg=6)
    B.done('airfield'); return S
# ---------------------------------------------------------------- set G: Waleed's house gate in Lahore, at night
def homegate():
    """street along x in front of the house wall (y=3.2). gate opening x -1.85..1.85, porch + door behind it. camera works from -y"""
    NIGHT[0]=1.0; S=setup_world('sk_night',shadow=50); r=random.Random(31); wl=M('#E0D2B8',.85,kind='wall'); br=M('#A8563A',.85,kind='wall'); tr=M('#F2EBDA',.8)
    B.box((0,0,-.1),(60,30,.1),M('#3E3E44',.9,kind='concrete',sc=1.6),0); B.box((0,2.3,.08),(40,.7,.08),M('#8A8078',.85,kind='tile',sc=.7),0)
    for sx in (-1,1):
        B.box((sx*11.0,3.2,1.5),(8.55,.18,1.5),wl,0); B.box((sx*11.0,3.2,3.06),(8.65,.26,.07),br,0); B.box((sx*2.15,3.2,1.75),(.3,.3,1.75),br,.03); B.box((sx*2.15,3.2,3.6),(.38,.38,.1),tr,.02)
        B.ico((sx*2.15,3.2,3.95),.26,M('#FFE2A8',.3,emit=6.0),sub=2)
    gm=M('#1E5A3A',.45,metal=.4)                                                     # gate leaves swung open (inwards)
    for sx in (-1,1):
        B.box((sx*1.82,4.3,1.4),(.05,.95,1.4),gm,.02)
        for k in range(5): B.box((sx*1.78,3.5+k*.42,1.4),(.02,.03,1.3),M('#E6B53A',.3,metal=.7),0)
    B.box((0,8,.06),(6,5,.06),M('#B88A6A',.85,kind='tile',sc=.7),0)
    B.box((0,13,4.0),(8,3,4.0),wl,0); B.box((0,13,8.15),(8.3,3.3,.15),tr,0); B.box((0,9.95,3.3),(3.2,.9,.12),tr,.03)
    for sx in (-1,1): B.cyl((sx*2.9,9.3,1.6),.16,3.2,tr,seg=10)
    B.box((0,9.98,1.45),(.75,.05,1.45),M('#5A3A22',.6,kind='wood'),.02); B.box((0,10.0,1.5),(.9,.04,1.55),tr,0); B.ico((.5,9.9,1.4),.05,M('#E6B53A',.3,metal=.8),sub=1)
    B.ico((0,9.6,3.05),.16,M('#FFE2A8',.3,emit=7.0),sub=2)
    for (q,z) in ((-4.6,2.2),(4.6,2.2),(-4.6,5.8),(0,5.8),(4.6,5.8)):
        B.box((q,9.97,z),(1.0,.05,.85),M('#FFD98A',.3,emit=1.5) if (q,z)!=(4.6,5.8) else M('#27344A',.3),0); B.box((q,9.94,z-.92),(1.15,.09,.06),tr,0)
        for qq in (-.5,.5): B.box((q+qq,9.95,z),(.03,.04,.85),tr,0)
    sign('27-B',(3.2,3.03,2.2),.2,'#16171C','#F2EBDA',n=(0,-1,0),pad=.1,th=.05,frame='#E6B53A')
    for k in range(16): B.ico((-6.5+r.uniform(-2.4,2.4),3.25+r.uniform(-.25,.2),3.0+r.uniform(-.1,.7)),r.uniform(.35,.6),M(r.choice(['#D8468A','#E86AA0','#3F7A3A','#4F8A3A','#C83A7A']),.85,kind='leaves'),sub=1)
    for (x,y) in ((-3.4,2.5),(3.9,2.5),(-2.0,8.6),(2.0,8.6)): B.cyl((x,y,.32),.3,.5,br,seg=10,r2=.24); B.ico((x,y,.95),.48,M('#3F7A3A',.85,kind='leaves'),sub=1)
    street_lamp(-9,-3.6,h=8.0,arms=(1,))
    for sx in (-1,1): B.box((sx*26,6,3.5),(6,5,3.5),M(['#C9A27A','#D8B48C'][sx>0],.85,kind='wall'),0)
    B.box((0,-8,1.5),(40,.2,1.5),M('#C9B8A0',.85,kind='wall'),0)
    for k in range(4): B.box((-14+k*9,-7.86,2.2),(1.0,.05,.8),M('#FFD98A',.3,emit=1.2) if k%2 else M('#27344A',.3),0)
    for k,(x,w_,h_,c) in enumerate(((-17,6.5,7.5,'#C9A27A'),(-3.5,6.0,9.0,'#D8C4A0'),(9.5,6.5,7.0,'#B8A088'),(23,6,8.5,'#C9A27A'))):      # houses across the street
        B.box((x,-14,h_/2),(w_,5,h_/2),M(c,.85,kind='wall'),0); B.box((x,-14,h_+.12),(w_+.2,5.2,.12),tr,0)
        for i in range(3):
            for j in range(2):
                on=(i+j+k)%3!=0; B.box((x-w_*.55+i*w_*.55,-8.97,2.4+j*3.2),(.8,.05,.75),M('#FFD98A',.3,emit=1.4) if on else M('#27344A',.3),0)
    for (x,y,s_) in ((-12,-6.2,1.5),(5.5,-6.0,1.3),(17,-6.4,1.6)): tree(x,y,s_)
    street_lamp(11,-3.6,h=8.0,arms=(1,))
    B.done('homegate')
    L=[point((0,9.3,2.9),520,(1,.86,.6),r=.4,shadow=True),point((-2.15,2.7,3.9),300,(1,.86,.62),r=.3,shadow=False),point((2.15,2.7,3.9),300,(1,.86,.62),r=.3,shadow=False),
       point((-9,-1.2,7.6),900,(1,.9,.72),r=.6,shadow=True),point((11,-1.2,7.6),700,(1,.9,.72),r=.6,shadow=False),point((0,-3.8,3.6),1100,(.85,.9,1.0),r=2.0,shadow=False),point((0,6.5,3.4),500,(1,.88,.7),r=1.5,shadow=False)]
    return dict(L=L)
