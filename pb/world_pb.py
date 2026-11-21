# Sets for "The Pindi Boys": residential Pindi gali (day + night), GT road through mustard fields, roadside petrol pump, the old Mehran.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
NIGHT=[False]
def win_mat(r):
    if NIGHT[0] and r.random()<.7: return M(r.choice(['#FFD98A','#FFE7B0','#BFE0FF']),.3,emit=r.uniform(1.8,3.5))
    return M(r.choice(['#2A3A4A','#3A4A5A','#22303E']),.15,spec=.9)
def gali_house(cx,w,side,seed,hero=False):
    r=random.Random(seed); Y=3.6 if side>0 else -3.6; d=4.0; c=r.choice(['#E8C9A0','#D9B48A','#C9D8C0','#F0D8C0','#D8C8E0','#E6D2A8','#C8B8A0','#B8CCD8']) if not hero else '#E9D3B0'
    floors=r.choice([2,3]) if not hero else 2; fh=3.1; h=floors*fh+.3; s=side; yc=Y+s*d
    B.box((cx,yc,h/2),(w/2-.04,d,h/2),M(c,.9,kind='wall'),0)
    B.box((cx,Y+s*.02,.35),(w/2-.04,.06,.35),M(shade(c,.75),.9,kind='concrete'),0)
    for f in range(floors):
        z=f*fh
        if f>0:
            # jharoka balcony
            B.box((cx-w*.15,Y-s*.45,z+.05),(w*.28,.5,.07),M(shade(c,.85),.8,kind='concrete'),.02)
            for k in range(int(w*.56/.25)): B.box((cx-w*.15-w*.28+.1+k*.25,Y-s*.88,z+.55),(.025,.025,.5),M(r.choice(['#2F4F4F','#4A2E2A','#1F3A5A']),.5,metal=.3),0)
            B.box((cx-w*.15,Y-s*.88,z+1.06),(w*.28,.04,.04),M('#2A2C34',.5,metal=.3),0)
            B.box((cx-w*.15,Y-s*.02,z+1.5),(.55,.05,.9),M('#5A3A22',.7,kind='wood'),.02)
            B.box((cx+w*.22,Y-s*.03,z+1.7),(.5,.05,.55),win_mat(r),.01); B.box((cx+w*.22,Y-s*.07,z+2.3),(.62,.1,.06),M(shade(c,.8),.8),.01)
            if r.random()<.5: B.box((cx+w*.22,Y-s*.2,z+1.05),(.35,.18,.22),M('#E8E8E4',.5),.03)  # AC unit
        B.box((cx,Y-s*.05,z+fh),(w/2,.12,.07),M(shade(c,.8),.8,kind='concrete'),.01)
    # parapet + water tank
    B.box((cx,Y-s*.05,h+.35),(w/2-.05,.08,.35),M(c,.9,kind='wall'),.01)
    if r.random()<.75: B.cyl((cx+r.uniform(-1,1),yc,h+.85),.62,1.1,M(r.choice(['#2A2C34','#3A6A9A','#E8E8E4']),.5),seg=12)
    # ground floor: gate + small window
    gc=r.choice(['#2F6A4A','#2B4A7A','#7A2F2F','#3A3D44','#6A4A2A']) if not hero else '#2F6A4A'
    gx=cx+(w*.18 if not hero else 0); gw=1.25 if not hero else 1.55
    B.box((gx,Y-s*.06,1.3),(gw,.06,1.3),M(gc,.45,metal=.4),.02)
    for k in range(int(gw*2/.22)): B.box((gx-gw+.11+k*.22,Y-s*.1,1.85),(.018,.018,.55),M('#D9B24A',.3,metal=.8),0)
    B.box((gx,Y-s*.11,1.25),(.015,.02,1.25),M(shade(gc,.6),.5),0)
    B.box((gx,Y-s*.14,2.75),(gw+.15,.12,.12),M(shade(c,.8),.8),.02)
    B.box((cx-w*.25,Y-s*.03,1.6),(.45,.05,.5),win_mat(r),.01);
    for k in range(5): B.box((cx-w*.25-.36+k*.18,Y-s*.09,1.6),(.015,.015,.5),M('#2A2C34',.5,metal=.4),0)
    B.box((gx+gw+.35,Y-s*.08,2.2),(.18,.04,.12),M('#2B58C9',.5),.01)
    if NIGHT[0]: B.ico((gx-gw-.3,Y-s*.18,2.5),.11,M('#FFE7B0',.3,emit=6),sub=1)
    return gx
HERO_X=0.0
def gali(night=False):
    NIGHT[0]=night; r=random.Random(11)
    B.box((0,0,-.05),(70,3.62,.05),M('#A8826A',.9,kind='tile',h2='#8E6A54',sc=2.4),0)
    for s in (-1,1): B.box((0,s*3.45,.03),(70,.16,.05),M('#5A5A58',.9,kind='concrete'),0); B.box((0,s*3.25,.02),(70,.06,.02),M('#7A7A78',.8),0)
    GX=gali_house(0,7,1,1,True); x=3.5; i=1
    while x<34: w=r.choice([6,7,8]); gali_house(x+w/2,w,1,i*3+1); x+=w; i+=1
    x=-3.5
    while x>-34: w=r.choice([6,7,8]); gali_house(x-w/2,w,1,i*3+1); x-=w; i+=1
    x=-34; i=0
    while x<34:
        w=r.choice([6,7,8]); gali_house(x+w/2,w,-1,i*5+40); x+=w; i+=1
    for x in (-24,-10,6,20): pole(x,3.2,8.0)
    wires(-34,34,3.2,3.2,7.6,5,4); wires(-34,34,3.2,-3.2,7.8,6,5)
    for (x,y) in ((-13.5,3.0),(9.5,-3.0),(16,3.1)): B.cyl((x,y,.25),.25,.5,M('#B5603F',.8),seg=10,r2=.2); B.ico((x,y,.75),.4,M('#4F8A3A',.85,kind='leaves'),sub=1)
    tree(-18.5,2.6,1.3,'#4F7E3A','#5A3E28'); tree(13,-2.6,1.2,'#5E8A44','#5A3E28')
    # laundry line between balconies
    for k in range(6): B.box((-7.5+k*.5,2.4,5.2-.06*math.sin(k)),(.18,.015,.3),M(['#E8554D','#F4F1EA','#4D8FE8','#F2C14E','#35975A','#CF3F78'][k],.9,kind='fabric'),0)
    B.cyl((-6.25,2.4,5.5),.008,3.4,M('#16171C',.6),rot=(0,R(90),0),seg=4)
    if night:
        for x in (-24,-10,6,20): B.box((x,2.6,6.4),(.08,.6,.05),M('#3A3D44',.5),0); B.box((x,2.05,6.32),(.18,.14,.05),M('#FFE2A0',.3,emit=8),.01)
    return GX
# ---------------------------------------------------------------- GT road
def eucalyptus(x,y,s=1.0):
    B.cyl((x,y,4*s),.16*s,8*s,M('#E8E2D6',.7),seg=8,r2=.09*s)
    for dz,dx,r_ in ((8.4,0,1.5),(7.4,.8,1.1),(7.0,-.7,1.0),(9.2,.3,1.0)): B.ico((x+dx*s,y,dz*s),r_*s,M('#6A8A5A',.9,kind='leaves'),sc=(1,1,.75),sub=1)
def gt_road():
    r=random.Random(7)
    B.box((0,0,-.05),(320,4.4,.05),M('#3A3C40',.9,kind='asphalt'),0); B.box((0,0,.005),(320,.08,.005),M('#F2C14E',.6),0)
    for s in (-1,1): B.box((0,s*4.25,.006),(320,.07,.005),M('#F4F1EA',.6),0); B.box((0,s*5.6,-.03),(320,1.3,.05),M('#B8A27A',.95,kind='concrete',sc=.4),0)
    for s in (-1,1): B.box((0,s*40,-.08),(320,33,.05),M('#7A9A3A',.95,kind='grass',sc=.3),0)
    for k in range(900):
        x=r.uniform(-160,160); y=r.choice([1,-1])*r.uniform(8,45)
        if r.random()<.75: B.box((x,y,.25),(r.uniform(.8,1.6),r.uniform(.8,1.6),.28),M(r.choice(['#F2C81E','#E8B81A','#F6D23A']),.85,kind='leaves'),.05)
    for x in range(-155,156,9): eucalyptus(x+r.uniform(-2,2),7.2+r.uniform(0,1),r.uniform(.9,1.15)); eucalyptus(x+4+r.uniform(-2,2),-7.4-r.uniform(0,1),r.uniform(.9,1.15))
    for x in range(-150,151,50):
        B.cyl((x,6.4,1.2),.06,2.4,M('#C9CED8',.4,metal=.6),seg=6); B.box((x,6.35,2.4),(1.1,.04,.5),M('#1F6A3A',.5),.03); stext('PINDI  %d km'%(abs(x)//10+4),(x,6.3,2.45),.24,'#F4F1EA'); stext('MURREE  58 km',(x,6.3,2.15),.16,'#F4F1EA')
    for x in range(-156,157,6): B.box((x,4.9,.3),(.1,.12,.3),M('#F4F1EA',.6),.02); B.box((x,4.9,.55),(.11,.13,.08),M('#C8372D',.6),.02)
    for x in range(-150,151,40): B.box((x,-5.2,.35),(.22,.12,.35),M('#F4F1EA',.7),.06); B.box((x,-5.2,.62),(.23,.13,.08),M('#F2C14E',.6),.04)
    for k in range(7):  # pylons
        x=-150+k*50;
        for dy in (-1,1):
            for dx in (-1,1): B.cyl((x+dx*.9,30+dy*.9,8),.09,16,M('#8A8E96',.5,metal=.6),seg=5,rot=(R(-3*dy),R(3*dx),0))
        B.box((x,30,14.5),(3.2,.12,.12),M('#8A8E96',.5,metal=.6),0); B.box((x,30,12),(2.4,.12,.12),M('#8A8E96',.5,metal=.6),0)
    for z in (14.4,11.9):
        B.box((0,30,z-.3),(170,.02,.02),M('#2A2C34',.6),0)
    for k in range(12): x=-200+k*36; B.ico((x,160+r.uniform(0,40),-20),r.uniform(40,70),M(r.choice(['#5A7A8A','#6A8A9A','#4E6E80']),.95),sc=(1.8,1,.9),sub=2)
    for k in range(10): x=r.uniform(-140,140); B.box((x,r.choice([-1,1])*r.uniform(22,40),1.4),(2.5,2,1.4),M(r.choice(['#C8A27A','#B8926A','#D8B48A']),.9,kind='wall'),.02)
# ---------------------------------------------------------------- petrol pump
def dispenser(x,y,col='#C8372D'):
    e=empty((x,y,0)); obox((0,0,.85),(.42,.3,.85),M('#F4F1EA',.5),.04,e); obox((0,0,1.78),(.44,.32,.12),M(col,.5),.03,e)
    obox((0,-.31,1.25),(.32,.01,.22),M('#0E1418',.4),.0,e); obox((-.25,-.33,.75),(.06,.03,.25),M('#2A2C34',.5),.01,e)
    ocyl((-.25,-.4,.6),.035,.35,M('#16171C',.6),e,rot=(R(90),0,0),seg=6)
    return e
def pump():
    r=random.Random(5); cn=M('#C9C6BE',.9,kind='concrete',sc=.6)
    B.box((0,0,-.05),(60,30,.05),M('#4A4A4E',.9,kind='asphalt'),0); B.box((0,6,.0),(14,7,.04),cn,0)
    for (x,y) in ((-3.2,4.0),(3.2,4.0),(-3.2,8.0),(3.2,8.0)): B.box((x,y,2.6),(.28,.28,2.6),M('#F4F1EA',.5),.03)
    B.box((0,6,5.4),(5.6,3.4,.35),M('#F4F1EA',.5),.04); B.box((0,6,5.05),(5.65,3.45,.06),M('#C8372D',.5),.02)
    for s in (-1,1): B.box((0,6+s*3.46,5.45),(5.7,.04,.3),M('#C8372D',.5,emit=.4),0)
    stext('PAK FUEL',(0,2.5,5.42),.42,'#FFFFFF',e=1.5)
    for (x,y) in ((-3.0,5.0),(0,5.0),(3.0,5.0),(-3.0,7.0),(0,7.0),(3.0,7.0)): B.box((x,y,5.0),(.9,.25,.03),M('#FFFFFF',.3,emit=6),0)
    for y in (4.0,8.0): B.box((0,y,.12),(2.7,.36,.12),M('#F2C14E',.6,kind='concrete'),.03)
    # shop + price board
    B.box((10.5,12,2.0),(4,2.5,2.0),M('#E8E2D6',.85,kind='wall'),.02); B.box((10.5,9.48,1.3),(2.8,.04,1.0),M('#FFE8C4',.5,emit=.8),0); B.box((10.5,9.3,3.3),(4.1,.3,.4),M('#C8372D',.5),.03); stext('TUCK SHOP',(10.5,8.98,3.3),.32,'#FFFFFF',e=1)
    B.box((-8.5,3.4,2.4),(.08,.08,2.4),M('#3A3D44',.5,metal=.4),0); B.box((-8.5,3.35,4.4),(1.0,.06,.9),M('#16171C',.6),.03)
    stext('PETROL',(-8.5,3.28,4.95),.22,'#F2C14E',e=1.2); stext('252.10',(-8.5,3.28,4.6),.3,'#FF5A3A',e=2.5); stext('DIESEL',(-8.5,3.28,4.2),.2,'#F2C14E',e=1.2); stext('258.40',(-8.5,3.28,3.88),.3,'#FF5A3A',e=2.5)
    # air & water
    B.box((7.0,3.0,.6),(.3,.3,.6),M('#2B58C9',.5,metal=.2),.03); stext('AIR',(7.0,2.68,1.0),.14,'#FFFFFF')
    for k in range(8): B.box((-14+k*4,-4.5,.25),(1.6,.3,.25),M('#F4F1EA' if k%2 else '#C8372D',.6),.02)
    for (x,y) in ((-11,13),(14,14),(-16,8),(17,6)): tree(x,y,1.3,r.choice(['#4F7E3A','#5E8A44']),'#5A3E28')
    pole(-12,-3,8.5); pole(12,-3,8.5); wires(-30,30,-3,-3,8.0,3,2)
    for k in range(9): x=-40+k*10; B.box((x,26+r.uniform(0,6),r.uniform(3,6)),(4,3,r.uniform(3,6)),M(r.choice(['#8A7E78','#7A7480','#94887A']),.9,kind='wall'),0)
    D=[dispenser(-2.0,4.0),dispenser(2.0,4.0),dispenser(-2.0,8.0,'#2B58C9'),dispenser(2.0,8.0,'#2B58C9')]
    return D
# ---------------------------------------------------------------- the old Mehran (faces +x), driver on the right (-y)
def mehran(loc,rotz=0,col='#9CC7E4'):
    root=empty(loc,rot=(0,0,R(rotz))); body=M(col,.35,metal=.2,spec=.6); gl=M('#BFD6E8',.05,spec=1.0,alpha=.12); bk=M('#1E1F24',.7); ch=M('#C9CED8',.3,metal=.9); W=[]
    obox((0,0,.62),(2.25,1.1,.36),body,.08,root)          # lower body
    obox((1.75,0,1.06),(.55,1.06,.12),body,.06,root)      # bonnet
    obox((-1.95,0,1.06),(.32,1.06,.12),body,.06,root)     # boot
    for sy in (-1,1):
        obox((-.15,sy*1.06,1.3),(1.55,.05,.18),body,.03,root)          # belt line panel
        for x in (1.18,-.3,-1.55): obox((x,sy*1.04,2.02),(.06,.05,.76),body,.02,root)  # pillars
        obox((-.15,sy*1.08,2.02),(1.35,.01,.62),gl,0,root)
        obox((2.27,sy*.75,.82),(.04,.2,.12),M('#FFF6D8',.2,emit=2.5),.04,root); obox((-2.27,sy*.8,.85),(.03,.14,.14),M('#E8301A',.3,emit=1.6),.02,root)
        obox((.1,sy*1.12,.55),(1.0,.02,.04),ch,.01,root)
    obox((-.2,0,2.8),(1.48,1.08,.06),body,.04,root)                 # roof
    obox((1.3,0,2.0),(.04,1.0,.72),gl,0,root,rot=(0,R(-18),0)); obox((-1.62,0,2.0),(.04,1.0,.7),gl,0,root,rot=(0,R(14),0))
    obox((2.3,0,.6),(.06,1.12,.1),ch,.03,root); obox((-2.3,0,.6),(.06,1.12,.1),ch,.03,root); obox((2.3,0,.82),(.02,.38,.1),bk,.01,root)
    obox((-2.31,0,.82),(.01,.38,.12),M('#F4F1EA',.6),0,root); text('LEA 2007',(-2.33,0,.82),(-1,0,0),.11,M('#16171C',.5),ex=.003,parent=root)
    # interior: seats, dash, wheel
    st=M('#5A3A2A',.8,kind='fabric')
    for sy in (-.5,.5): obox((.15,sy,.66),(.38,.38,.08),st,.04,root); obox((-.25,sy,1.2),(.08,.38,.5),st,.04,root)
    obox((-1.05,0,.66),(.38,.9,.08),st,.04,root); obox((-1.45,0,1.2),(.08,.9,.5),st,.04,root)
    obox((1.05,0,1.25),(.18,1.0,.14),M('#2A2C34',.7),.03,root)
    sw=empty((.78,-.5,1.38),root,rot=(0,R(-60),0)); ocyl((0,0,0),.24,.05,M('#16171C',.5),sw,rot=(0,0,0),seg=16); ocyl((0,0,-.2),.04,.4,M('#16171C',.5),sw,rot=(0,0,0),seg=6)
    for (wx,sy) in ((1.45,-1),(1.45,1),(-1.45,-1),(-1.45,1)): W.append(wheel((wx,sy*1.02,.42),.42,.26,root))
    return dict(root=root,wheels=W,r=.42,wheel=sw)
