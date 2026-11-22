# Sets for "The Multani Prince": Multan skyline (octagonal brick shrine with white dome and blue tile bands, fort mound,
# palms, mango orchard, heat), Lahore intercity bus terminal (canopy, coach, bays), modern glass mall atrium (watch shop),
# halwa boxes, bag, violin.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
TILE=M('#2B6AB8',.35,spec=.9,kind='tile',h2='#F4F1EA',sc=6); TILE2=M('#1E8AA8',.35,spec=.9,kind='tile',h2='#F4F1EA',sc=9)
def shrine(x,y,s=1.0):
    br=M('#B8603A',.85,kind='wall',h2='#9A4A2A',sc=2.0); wh=M('#F4F1EA',.5)
    for k in range(8):  # octagonal lower drum, slight batter
        a=k*pi/4; B.box((x+math.cos(a)*5.2*s,y+math.sin(a)*5.2*s,5.0*s),(2.2*s,.6*s,5.0*s),br,.05,rot=(0,0,a+pi/2))
        B.box((x+math.cos(a)*5.83*s,y+math.sin(a)*5.83*s,7.0*s),(1.0*s,.05,1.6*s),TILE,.03,rot=(0,0,a+pi/2))
        B.box((x+math.cos(a)*5.83*s,y+math.sin(a)*5.83*s,2.2*s),(.8*s,.05,1.6*s),M('#3A2414',.7),0,rot=(0,0,a+pi/2))
        B.box((x+math.cos(a)*5.9*s,y+math.sin(a)*5.9*s,10.5*s),(.35*s,.35*s,.6*s),br,.05); B.ico((x+math.cos(a)*5.9*s,y+math.sin(a)*5.9*s,11.4*s),.4*s,wh,sub=1)
    B.cyl((x,y,10.2*s),5.6*s,.5*s,TILE2,seg=8)
    B.cyl((x,y,13.0*s),4.0*s,5.2*s,br,seg=8); B.cyl((x,y,15.7*s),4.1*s,.4*s,TILE,seg=8)
    B.ico((x,y,17.3*s),4.0*s,wh,sc=(1,1,.9),sub=3); B.cyl((x,y,21.2*s),.12*s,1.4*s,M('#D9B24A',.3,metal=.8),seg=6); B.ico((x,y,22.0*s),.3*s,M('#D9B24A',.3,metal=.8),sub=1)
def multan_set(seed=3):
    r=random.Random(seed)
    B.box((0,0,-.05),(80,80,.05),M('#C9A878',.9,kind='asphalt',h2='#B89868',sc=2),0)
    B.box((0,20,1.5),(26,12,1.5),M('#B8603A',.9,kind='wall',h2='#9A4A2A',sc=3),.3)   # fort mound wall
    for x in range(-24,25,4): B.box((x,8.2,3.3),(.8,.5,.3),M('#B8603A',.85,kind='wall'),.05)
    shrine(0,20,1.0)
    for k in range(14):
        x=r.uniform(-30,30); y=r.uniform(14,40)
        if abs(x)<9 and y<30: continue
        B.box((x,y,r.uniform(2,6)/2),(r.uniform(2,4),r.uniform(2,4),r.uniform(2,6)/2),M(r.choice(['#E8C07A','#D98A5A','#C9B48A','#F0E0C0','#B8634A']),.85,kind='wall'),0)
    for (x,y) in ((-9,4),(9,5),(-15,9),(14,10),(-20,3)):
        B.cyl((x,y,3.0),.22,6.0,M('#7A5A3A',.8),seg=8)
        for k in range(7): a=k*.9; B.box((x+math.cos(a)*1.2,y+math.sin(a)*1.2,6.1),(1.3,.28,.04),M('#3F8A3A',.85,kind='leaves'),.02,rot=(R(25)*math.sin(a),R(-25)*math.cos(a),a))
    mangos=[]
    for (x,y) in ((-6,-3),(6,-4),(-12,-6),(12,-8)):
        B.cyl((x,y,1.0),.3,2.0,M('#6B4A2E',.8),seg=8); B.ico((x,y,3.2),2.0,M('#2F7A32',.85,kind='leaves'),sc=(1,1,.8),sub=2)
        for k in range(9): a=k*.7; m=B.ico((x+math.cos(a)*1.7,y+math.sin(a)*1.7,2.6+.3*math.sin(k)),.15,M('#F2B01E',.5),sc=(1,1,1.3),sub=1)
    return None
def mango_crate(e,s=1.0):
    wd=M('#B88A4A',.7,kind='wood'); obox((0,0,.18*s),(.5*s,.35*s,.18*s),wd,.02,e)
    for i in range(4):
        for j in range(3): oico((-.36*s+.24*s*i,-.22*s+.22*s*j,.4*s),.11*s,M(['#F2B01E','#E8A01A','#F2C14E'][(i+j)%3],.5),e,sc=(1,1,1.25),sub=1)
# ---------------------------------------------------------------- bus terminal
def bus(e,col='#F4F1EA',stripe='#E8641E'):
    obox((0,0,1.9),(6.0,1.3,1.6),M(col,.35,spec=.9),.25,e); obox((0,-1.31,1.1),(6.0,.02,.18),M(stripe,.4),0,e); obox((0,-1.31,.75),(6.0,.02,.07),M('#16171C',.4),0,e)
    obox((0,-1.32,2.5),(5.0,.02,.6),M('#1A2433',.08,spec=1),0,e); obox((5.98,0,2.4),(.03,1.2,.8),M('#1A2433',.08,spec=1),0,e)
    for dx in (-4.0,3.6): ocyl((dx,-1.25,.5),.5,.35,M('#16171C',.7),e,rot=(R(90),0,0),seg=18); ocyl((dx,1.25,.5),.5,.35,M('#16171C',.7),e,rot=(R(90),0,0),seg=18)
    text('MULTAN EXPRESS',(-.5,-1.34,1.55),(0,-1,0),.32,M(stripe,.4),ex=.01,parent=e); obox((5.0,-1.32,1.6),(.45,.02,.9),M('#2A2C34',.4),0,e)
    for dy in (-.9,.9): oico((6.0,dy,1.0),.12,M('#FFF2D0',.3,emit=2),e,sub=1)
def terminal_set(seed=2):
    r=random.Random(seed); fl=M('#C8C2B4',.5,kind='tile',h2='#B8B2A4',sc=1.4)
    B.box((0,0,-.05),(40,20,.05),fl,0); B.box((0,-8,-.04),(40,5,.05),M('#5E6068',.85,kind='asphalt'),0)
    for x in range(-36,37,3): B.box((x,-3.0,.08),(1.2,.08,.08),M('#F2C14E',.6),0)
    B.box((0,-2.9,.12),(40,.15,.12),M('#9A9A96',.7),0)
    # canopy on columns
    B.box((0,2,5.2),(30,6,.25),M('#E8E8E4',.5),.05); B.box((0,-3.9,5.0),(30,.1,.5),M('#E8641E',.5),.02)
    for x in range(-27,28,6):
        for y in (-3.2,7.2): B.cyl((x,y,2.6),.2,5.2,M('#C9CED8',.3,metal=.7),seg=12)
    for x in range(-24,25,6): B.box((x,2,4.93),(.8,.8,.02),M('#FFFFFF',.3,emit=2.5),0)
    stext('LAHORE BUS TERMINAL',(0,-3.96,5.05),.4,'#FFFFFF',e=.6)
    # waiting hall glass + benches + kiosk + boards
    B.box((0,8,2.5),(30,.05,2.5),M('#BFD6E8',.05,spec=1.0,alpha=.25),0)
    for x in range(-28,29,4): B.box((x,8,2.5),(.06,.08,2.5),M('#8A8E96',.3,metal=.8),0)
    B.box((0,12,3),(30,.2,3),M('#E8D8B0',.85,kind='wall'),0)
    for k in range(5):
        x=-14+k*6; B.box((x,4.5,.42),(1.4,.3,.05),M('#2B5AA8',.5),.02); B.box((x,4.8,.75),(1.4,.05,.3),M('#2B5AA8',.5),.02)
        for dx in (-1.2,1.2): B.box((x+dx,4.5,.2),(.05,.25,.2),M('#8A8E96',.3,metal=.7),0)
    B.box((12,5.5,1.1),(1.4,.9,1.1),M('#C8372D',.6),.05); stext('COLD DRINKS',(12,4.58,1.9),.2,'#FFFFFF',e=.5)
    for k in range(6): B.box((11.3+.28*k,4.62,1.2),(.1,.01,.25),M(['#16171C','#E8641E','#2B8A5A'][k%3],.5),0)
    B.box((-8,7.8,3.6),(2.4,.1,.7),M('#16171C',.5),.04); stext('MULTAN  ARRIVED',(-8,7.68,3.75),.2,'#35C85A',e=1.4); stext('KARACHI  14:30',(-8,7.68,3.4),.2,'#F2C14E',e=1.4)
    for (x,y) in ((-30,-12),(-18,-13),(18,-13),(30,-12),(-34,10),(34,10)): tree(x,y,1.3)
    for k in range(8): B.box((r.uniform(-30,30),-15,r.uniform(3,6)),(r.uniform(3,5),1.5,r.uniform(3,6)),M(r.choice(['#E8D8B0','#D98A5A','#C9B48A']),.85,kind='wall'),0)
    bs=empty((-6,-6.5,0)); bus(bs); bs2=empty((14,-6.5,0)); bus(bs2,'#F4F1EA','#2B8A5A'); return bs
def halwa_box(e,s=1.0,open_=False):
    obox((0,0,.07*s),(.22*s,.16*s,.07*s),M('#C8372D',.5),.02,e); obox((0,-.161*s,.07*s),(.15*s,.003,.04*s),M('#F2C14E',.4,emit=.2),0,e)
    if open_: obox((0,0,.15*s),(.2*s,.14*s,.012),M('#8A4A1E',.6),.01,e)
    else: obox((0,0,.15*s),(.225*s,.165*s,.012),M('#D9B24A',.4,metal=.4),.01,e)
def halwa_piece(e,s=1.0):
    obox((0,-.08,.04*s),(.06*s,.04*s,.02*s),M('#8A4A1E',.6),.01,e)
    for k in range(3): oico((-.03*s+.03*s*k,-.08,.065*s),.012*s,M('#4F8A3A',.6),e,sub=1)
def duffel(e,s=1.0,col='#5A2A6A'):
    obox((0,0,.25*s),(.45*s,.25*s,.25*s),M(col,.85,kind='fabric',h2=shade(col,.8),sc=4),.12*s,e); ocyl((0,0,.52*s),.03*s,.6*s,M('#16171C',.6),e,rot=(0,R(90),0),seg=6)
    lid=empty((0,-.25*s,.48*s),e); obox((0,.25*s,0),(.44*s,.25*s,.02*s),M(col,.85,kind='fabric'),.02,lid)
    return lid
def violin(e,s=1.0):
    wd=M('#9A4A1E',.4,kind='wood',spec=.9); oico((0,-.06,.0),.12*s,wd,e,sc=(1,.35,1.4),sub=2); obox((0,-.06,.25*s),(.02*s,.015,.15*s),M('#16171C',.5),0,e)
    obox((.15*s,-.1,.05*s),(.005,.005,.3*s),M('#E8D8B0',.5),0,e,rot=(0,R(60),0))
# ---------------------------------------------------------------- mall atrium
def mall_set(seed=5):
    r=random.Random(seed); fl=M('#E8E4DC',.12,kind='tile',h2='#D8D4CC',sc=.8,spec=1.0)
    B.box((0,0,-.05),(24,18,.05),fl,0)
    for z,yb in ((4.5,3),(9,3)):  # upper galleries with glass rails
        for s in (-1,1): B.box((s*9,0,z),(5,18,.2),M('#F4F4F0',.4),.03); B.box((s*4.05,0,z+.6),(.03,18,.45),M('#BFD6E8',.05,spec=1.0,alpha=.3),0); B.box((s*4.05,0,z+1.07),(.05,18,.03),M('#C9CED8',.3,metal=.8),0)
        for s in (-1,1):
            for y in range(-15,16,6): B.box((s*12,y,z+1.8),(.1,2.6,1.6),M(r.choice(['#2B2C34','#F4F1EA','#C8372D','#16909E']),.4),.02); stext(r.choice(['ZARA?','KHAADI-ISH','SHOE LAB','J.LOOK','BOOKS']),(s*11.9,y,z+2.9),.25,'#16171C' ,n=(-s,0,0))
    B.box((0,0,13.5),(24,18,.1),M('#BFD6E8',.1,spec=1.0,alpha=.35),0)
    for y in range(-16,17,4): B.box((0,y,13.4),(4.2,.08,.08),M('#C9CED8',.3,metal=.8),0)
    # escalator
    B.box((-2.2,-6,2.25),(.7,4.5,.15),M('#C9CED8',.3,metal=.7),.05,rot=(R(-27),0,0)); B.box((-2.2,-6,2.6),(.72,4.5,.03),M('#2A2C34',.4),0,rot=(R(-27),0,0))
    # ground floor shops: watch shop on +x side, halwa/mango display, fountain + plants
    for y in (-12,-4,4,12):
        for s in (-1,1): B.box((s*12,y,2.0),(.1,3.6,2.0),M('#BFD6E8',.05,spec=1.0,alpha=.3),0); B.box((s*12.3,y,2.0),(.1,3.6,2.0),M(r.choice(['#F4F1EA','#E8D8B0','#2A2C34']),.6),0)
    B.box((12.05,4,4.1),(.1,3.6,.35),M('#16171C',.4),.02); stext('TIME HOUSE',(11.95,4,4.1),.35,'#D9B24A',n=(-1,0,0),e=1.0)
    for k in range(3):
        y=2.2+k*1.8; B.box((9.8,y,.5),(.5,.7,.5),M('#2A2C34',.4),.03); B.box((9.8,y,1.05),(.5,.7,.05),M('#BFD6E8',.05,spec=1.0,alpha=.4),.02)
        for j in range(4): B.cyl((9.8,y-.45+.3*j,1.02),.06,.02,M('#D9B24A',.2,metal=.9),seg=12)
    B.cyl((-5,8,.3),2.0,.6,M('#E8E4DC',.3),seg=24); B.cyl((-5,8,.55),1.85,.05,M('#6AB8E0',.1,spec=1,alpha=.7),seg=24); B.cyl((-5,8,1.0),.15,1.6,M('#E8E4DC',.3),seg=10)
    for (x,y) in ((6,-10),(-7,-12),(7,12)): B.cyl((x,y,.4),.5,.8,M('#F4F1EA',.4),seg=14,r2=.4); B.ico((x,y,1.6),.9,M('#3F8A3A',.85,kind='leaves'),sc=(1,1,1.4),sub=1)
    B.box((-9.5,-2,.45),(1.2,.6,.45),M('#7A5236',.6,kind='wood'),.03); stext('MANGO FESTIVAL',(-9.5,-2.62,1.2),.18,'#E8641E',e=.4)
    for k in range(6): B.ico((-10.4+.36*k,-2,.98),.15,M('#F2B01E',.5),sc=(1,1,1.25),sub=1)
    for k in range(10): B.box((0,0,13.3),(.5,.5,.02),M('#FFFFFF',.3,emit=2),0) if False else B.box((r.uniform(-3,3),r.uniform(-15,15),13.3),(.5,.5,.02),M('#FFFFFF',.3,emit=2.5),0)
def wristwatch(e,s=1.0):
    ocyl((0,-.08,.05),.06*s,.02,M('#D9B24A',.2,metal=.9),e,rot=(R(90),0,0),seg=16); ocyl((0,-.095,.05),.05*s,.005,M('#16171C',.3,spec=1),e,rot=(R(90),0,0),seg=16)
    for dz in (-.09,.19): obox((0,-.08,dz*s+.05*(1-s)),(.03*s,.005,.06*s),M('#3A2414',.6),0,e)
def notepad(e,s=1.0):
    obox((0,-.08,.05),(.08*s,.005,.11*s),M('#F2E6A8',.7),0,e,rot=(R(-50),0,0)); obox((.1*s,-.1,.07),(.005,.005,.1*s),M('#2B5AA8',.5),0,e,rot=(0,R(30),0))
