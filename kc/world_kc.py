# Sets for "Karachi wale biryani ke mamle mein compromise nahi karte" (Pakistan city series, Karachi ep 2):
#   suv(...)        - big family SUV built with a full interior (seats, dash, wheel, mirror, belts); car floor at local z=0
#   drive_k()       - the SUV interior on Shahrah-e-Faisal style road; the roadside strip scrolls past (scene 1)
#   rest_k()        - small, packed biryani restaurant: open front with degs + cook, tiled dining hall, parked SUV (scenes 2-5)
# Uses helpers from world_kb (palm, bush, pchair, stool, deg, bulb_string, stext, plate_spoon, biryani_box ...).
SUV_COL='#E9ECEF'
CAR_SEATS={'al':(-.9,-.55),'wa':(.9,-.55),'zo':(-.9,1.55),'ay':(.9,1.55)}      # Ali drives (right-hand drive, car faces -y)
def car_seat(e,x,y,col,z0=0.0):
    fab=M(col,.85,kind='fabric'); dk=M(shade(col,.7),.85,kind='fabric')
    obox((x,y,.42+z0),(.5,.42,.1),fab,.06,e); obox((x,y,.18+z0),(.42,.36,.18),M('#2A2C34',.7),.02,e)
    obox((x,y+.46,1.05+z0),(.5,.09,.6),fab,.06,e,rot=(R(10),0,0)); obox((x,y+.6,1.85+z0),(.27,.08,.18),dk,.06,e,rot=(R(10),0,0))
    for sx in (-.15,.15): ocyl((x+sx,y+.58,1.66+z0),.025,.14,M('#C9CED8',.3,metal=.8),e,rot=(0,0,0),seg=6)
def suv(loc,rotz=0,col=SUV_COL,parked=False):
    """SUV, local frame: faces -y, cabin floor z=0, road at z=-.55. Interior is fully modelled."""
    e=empty(loc,rot=(0,0,R(rotz))); body=M(col,.3,metal=.35,spec=.7); trim=M('#1E2026',.5); chrome=M('#C9CED8',.2,metal=.9)
    gl=M('#9FB8C8',.03,spec=1.0,alpha=.16); dash=M('#2A2C34',.65); fab='#3A3E48'
    # lower body, hood, rear, wheel arches
    for sx in (-1,1): obox((sx*1.55,0,.3),(.06,3.6,.65),body,.04,e)                          # door/side skins (below windows)
    obox((0,-3.05,.45),(1.6,1.05,.6),body,.25,e); obox((0,3.95,.55),(1.6,.18,.6),body,.12,e)     # hood block / rear bumper area
    obox((0,0,-.3),(1.55,3.6,.06),trim,.02,e)                                                    # floor pan
    obox((0,.5,-.02),(1.45,2.9,.02),M('#2E3138',.9,kind='fabric'),0,e)                           # carpet
    obox((0,-3.0,1.06),(1.58,1.0,.04),body,.04,e,rot=(R(-4),0,0))                               # hood top
    for sy in (-1,1):
        obox((sy*.62,-4.05,.62),(.36,.04,.14),M('#FFF6D8',.2,emit=1.5),.03,e); obox((sy*1.35,4.12,.95),(.18,.04,.3),M('#E8301A',.3,emit=1.2),.03,e)
    obox((0,-4.1,.35),(1.55,.08,.18),chrome,.05,e); obox((0,-4.08,.66),(.7,.03,.16),trim,.02,e)
    obox((0,-4.15,.12),(.42,.02,.12),M('#F4F1EA',.5),.01,e); stext('BKZ 786',(0,-4.18,.12),.11,'#16171C',parent=e)
    W=[]
    for sx in (-1.5,1.5):
        for sy in (-2.75,2.75): W.append(wheel((sx,sy,-.0),.55,.34,e)); obox((sx*1.02,sy,.55),(.08,.85,.12),trim,.06,e)
    # window frame / pillars / roof
    obox((0,.6,2.5),(1.58,3.35,.06),body,.05,e); obox((0,.6,2.43),(1.45,3.2,.02),M('#D8D2C4',.8,kind='fabric'),0,e)
    for sx in (-1,1):
        for y in (.55,2.65): obox((sx*1.55,y,1.75),(.05,.1,.72),body,.02,e)
        obox((sx*1.53,-1.55,1.75),(.05,.08,.78),body,.02,e,rot=(R(-30),0,0))
        obox((sx*1.55,3.85,1.75),(.05,.12,.72),body,.02,e)
        obox((sx*1.555,.65,1.62),(.012,3.2,.56),gl,0,e)                                         # side glass
        obox((sx*1.7,-1.35,1.25),(.14,.04,.1),body,.03,e); obox((sx*1.78,-1.36,1.25),(.03,.02,.07),M('#9FB8C8',.05,metal=.9),0,e)   # side mirrors
    obox((0,-1.62,1.78),(1.5,.012,.72),gl,0,e,rot=(R(-30),0,0))                                 # windshield
    obox((0,3.93,1.75),(1.45,.012,.62),gl,0,e,rot=(R(8),0,0))                                   # rear glass
    obox((0,-2.0,1.17),(1.5,.06,.05),trim,.02,e)
    # dashboard + cockpit
    obox((0,-1.72,.95),(1.5,.32,.26),dash,.08,e); obox((0,-1.55,1.18),(1.5,.18,.06),M('#3A3E48',.6),.04,e)
    obox((0,-1.45,.82),(.22,.22,.3),dash,.04,e)                                                  # centre console
    obox((0,-1.42,1.0),(.16,.02,.09),M('#1E90FF',.2,emit=1.5),.01,e)                            # radio screen
    for x in (-.55,-.18,.18,.55): obox((x,-1.42,1.12),(.1,.02,.035),M('#16171C',.4),.01,e)       # AC vents
    sw=empty((-.9,-1.25,1.18),e,rot=(R(62),0,0)); [obox((math.cos(a*.5236)*.23,math.sin(a*.5236)*.23,0),(.04,.065,.035),M('#16171C',.4),.015,sw,rot=(0,0,a*.5236)) for a in range(12)]; obox((0,0,0),(.06,.2,.02),M('#16171C',.4),.01,sw); ocyl((0,0,-.12),.04,.25,M('#16171C',.4),sw,rot=(0,0,0),seg=8)
    ocyl((0,-1.15,.55),.03,.35,chrome,e,rot=(R(20),0,0),seg=8); oico((0,-1.1,.75),.06,M('#16171C',.4),e,sub=1)   # gear stick
    obox((0,-1.3,2.32),(.2,.04,.06),M('#2A2C34',.4),.02,e); obox((0,-1.33,2.32),(.18,.01,.045),M('#BFD0DA',.05,metal=.95),0,e)   # mirror
    for k in range(9): oico((0,-1.31,2.22-k*.045),.018,M('#2E8A5A',.4),e,sub=1)               # tasbeeh
    oico((0,-1.31,1.81),.03,M('#D9B24A',.3,metal=.7),e,sub=1)
    obox((.65,-1.5,1.23),(.08,.05,.04),M('#7CFC9A',.5),.02,e)                                    # air freshener
    for (k,(x,y)) in CAR_SEATS.items(): car_seat(e,x,y,fab)
    obox((0,1.55,.75),(.12,.42,.2),M('#3A3E48',.85,kind='fabric'),.04,e)                         # rear armrest
    obox((0,-.55,.6),(.18,.5,.25),dash,.04,e)                                                    # front console box
    for sx in (-1,1):
        obox((sx*1.47,.1,.75),(.04,1.4,.3),M('#3A3E48',.75),.03,e); obox((sx*1.46,.1,1.02),(.05,1.4,.04),M('#C9B49A',.6),.02,e)   # door panels
    obox((0,3.2,.45),(1.45,.6,.1),M('#2E3138',.9,kind='fabric'),.02,e)                         # boot floor
    return dict(root=e,wheels=W)
def belts(P,keys=('al','wa','zo','ay')):
    """diagonal seat belts over each seated occupant (parented to the occupant)"""
    for k in keys:
        H=P[k]; s=1 if CAR_SEATS[k][0]<0 else -1; e=H['root']
        obox((s*.12,-.21,1.5),(.035,.012,.48),M('#16171C',.6),0,e,rot=(0,R(s*38),0))
def drive_bg(L_=160.0):
    """roadside strip (merged) that scrolls along +y; tile length L_, built twice for seamless wrap"""
    r=random.Random(5); z0=-.55
    for rep in (0,1):
        yo=rep*L_
        B.box((0,yo,z0-.05),(40,L_/2,.05),M('#4A4C54',.85,kind='asphalt'),0)
        for k in range(int(L_/6)): B.box((-1.9,yo-L_/2+k*6,z0+.005),(.08,1.4,.005),M('#F4F1EA',.6),0); B.box((5.9,yo-L_/2+k*6,z0+.005),(.08,1.4,.005),M('#F4F1EA',.6),0)
        B.box((-5.5,yo,z0+.25),(1.2,L_/2,.25),M('#B8A890',.85,kind='concrete'),0)                 # median
        for k in range(int(L_/14)):
            y=yo-L_/2+k*14+r.uniform(-2,2); palm(-5.5,y,1.0,int(y*7)%997)
            B.ico((-5.5+r.uniform(-.5,.5),y+7,z0+.8),.7,M('#3F7A3A',.85,kind='leaves'),sub=1)
        for k in range(int(L_/22)):
            y=yo-L_/2+k*22; B.cyl((9.6,y,z0+3.8),.1,7.6,M('#5A5E66',.4,metal=.6),seg=8); B.box((8.6,y,z0+7.5),(1.0,.08,.06),M('#5A5E66',.4),.01); B.ico((7.7,y,z0+7.4),.2,M('#FFF6D8',.3,emit=1.0),sub=1)
        B.box((11,yo,z0+.15),(2.2,L_/2,.15),M('#C8B89A',.85,kind='tile'),0)
        x=-L_/2
        while x<L_/2:
            w=r.uniform(7,11); h=r.uniform(8,24); col=r.choice(['#E8D8B8','#C9D6D8','#D8C4A0','#B8C8D0','#E6C8B0','#D0D0C8'])
            y=yo+x+w/2; B.box((18,y,z0+h/2),(4,w/2-.25,h/2),M(col,.85,kind='wall',sc=.8),0)
            for j in range(int(h/3)):
                for q in range(int(w/2.4)): B.box((13.95,y-w/2+1.2+q*2.4,z0+2+j*3),(.04,.5,.6),M('#5E7A8A',.1,spec=.9),0)
            if r.random()<.45: B.box((14.3,y,z0+h-1.0),(.12,min(3.2,w/2-.6),.8),M(r.choice(['#C8372D','#1E6A3A','#2B58C9','#D9811A']),.5),.03); B.box((14.15,y,z0+h-1.0),(.02,min(3.0,w/2-.8),.6),M('#F4F1EA',.6),0)
            x+=w
        for k in range(3):
            y=yo-L_/2+20+k*50; B.cyl((-9.5,y,z0+4),.25,8,M('#5A5E66',.4,metal=.5),seg=8); B.box((-9.5,y,z0+9),(.15,4,1.8),M('#F4F1EA',.6),.05)
            B.box((-9.35,y,z0+9),(.02,3.8,1.6),M(['#C8372D','#1E6A3A','#D9811A'][k],.5),0)
        for k in range(int(L_/9)):
            y=yo-L_/2+k*9+r.uniform(-2,2); B.box((-14,y,z0+r.uniform(3,9)),(3,r.uniform(2.5,4),r.uniform(3,9)),M(r.choice(['#D8C4A0','#C9D6D8','#E8D8B8']),.85,kind='wall'),0)
    return B.done('drivebg')
def drive_k():
    bg=drive_bg(); car=suv((0,0,0),0)
    setup_world('day',60)
    point((0,.2,2.2),90,(1,.95,.88),r=1.0,shadow=False); point((0,-3.5,2.4),260,(1,.97,.9),r=2.0,shadow=False)
    return dict(bg=bg,car=car)
def scroll(bg,t,v=9.0,L_=160.0):
    for o in (bg if isinstance(bg,(list,tuple)) else [bg]): o.location[1]=((t*v)%L_)-L_/2
# ------------------------------------------------------------------ restaurant
HT=(0,4.9)                                       # hero table centre (long axis along y)
TSEATS={'wa':(-1.2,4.0),'ay':(-1.2,5.8),'zo':(1.2,4.0),'al':(1.2,5.8)}
def tseat_rz(k): return 90 if TSEATS[k][0]<0 else -90
COUNTER_Y=.4
def rest_k(car_=True):
    r=random.Random(11); tileW=M('#F2F6F6',.35,kind='tile',h2='#DCE6E6',sc=2.4); tileG=M('#1E7A5A',.35,kind='tile',h2='#17684C',sc=2.4)
    ch=M('#C9CED8',.25,metal=.85); wd=M('#6E4A2E',.6,kind='wood',sc=.6)
    B.box((0,0,-.05),(40,30,.05),M('#4A4C54',.85,kind='asphalt'),0)
    B.box((0,-2.0,.08),(30,2.0,.08),M('#B8A890',.85,kind='tile'),0)
    B.box((0,5.0,.02),(6,5.0,.02),M('#D8D0C0',.6,kind='tile',h2='#C8C0B0',sc=2.0),0)      # dining floor
    # walls
    for sx in (-1,1): B.box((sx*6.1,5.0,2.2),(.1,5.0,2.2),tileW,0); B.box((sx*6.0,5.0,.7),(.02,5.0,.7),tileG,0)
    B.box((0,10.05,2.2),(6.2,.1,2.2),tileW,0); B.box((0,9.97,.7),(6.1,.02,.7),tileG,0)
    B.box((0,5.0,4.45),(6.2,5.1,.06),M('#E8E4DA',.8),0)
    # front facade + giant sign
    B.box((0,.05,5.4),(6.4,.25,1.0),M('#E8D8B8',.8,kind='wall'),0)
    B.box((0,-.25,5.4),(5.8,.08,.85),M('#1E6A3A',.5),.05); B.box((0,-.34,5.4),(5.6,.02,.72),M('#F2C14E',.5),0)
    stext('AL-NOOR BIRYANI',(0,-.37,5.62),.56,'#C8372D',e=.4); stext('& PHOTOCOPY CENTRE',(0,-.37,5.08),.3,'#1E6A3A')
    for sx in (-1,1): B.box((sx*6.25,.05,2.2),(.2,.25,2.2),M('#E8D8B8',.8,kind='wall'),0)
    for k in range(12): B.box((-5.5+k*1.0,-.7,4.25),(.5,.8,.02),M('#C8372D' if k%2 else '#F4F1EA',.6),0,rot=(R(-12),0,0))
    # front counter + degs + cook area
    B.box((0,COUNTER_Y,.55),(2.6,.45,.55),M('#B8C4CC',.4,kind='tile'),.02); B.box((0,COUNTER_Y,1.12),(2.7,.5,.03),ch,.01)
    B.done('rest0')
    for x,lid in ((-1.6,False),(0.0,True),(1.6,False)):
        e_=empty((x,COUNTER_Y+.05,1.15)); B.cyl((x,COUNTER_Y+.05,1.55),.55,.8,M('#7A3E1A',.3,metal=.85),seg=24,r2=.66); B.cyl((x,COUNTER_Y+.05,1.96),.62,.05,M('#5A2E12',.3,metal=.85),seg=24)
        if lid: B.cyl((x,COUNTER_Y+.05,2.0),.58,.06,M('#8E5A2A',.4,metal=.6),seg=24); B.ico((x,COUNTER_Y+.05,2.1),.08,M('#5A2E12',.4,metal=.7),sub=1)
        else:
            B.cyl((x,COUNTER_Y+.05,1.95),.57,.03,M('#F2C45A',.6),seg=24)
            for k in range(16): B.ico((x+r.uniform(-.42,.42),COUNTER_Y+.05+r.uniform(-.42,.42),1.99),.04,M(r.choice(['#F4EEDC','#E8A23A','#C8622A','#F4EEDC','#9A4A1E']),.6),sub=1)
    for k in range(10): B.cyl((2.35,COUNTER_Y-.1+k*.0,1.18+k*.03),.18,.025,M('#F4F1EA',.3),seg=16)     # plate stack
    B.box((-2.4,COUNTER_Y,1.25),(.22,.18,.12),M('#E8E4DA',.6),.03)                                 # cash box
    # photocopy machine in the corner (the joke)
    B.box((-5.3,1.4,.6),(.45,.4,.6),M('#D8D8D2',.5),.04); B.box((-5.3,1.4,1.25),(.45,.4,.06),M('#5A5E66',.4),.02); B.box((-5.3,1.15,1.28),(.25,.02,.04),M('#7CFC9A',.3,emit=1.5),.01)
    stext('PHOTOCOPY Rs 10',(-5.3,.98,1.55),.12,'#C8372D')
    # menu board
    B.box((0,9.92,3.1),(2.2,.04,.8),M('#16171C',.6),.03)
    stext('MENU',(0,9.86,3.62),.24,'#F2C14E',n=(0,-1,0))
    for k,(a,b) in enumerate((('CHICKEN BIRYANI','Rs 450'),('BEEF BIRYANI','Rs 500'),('RAITA','Rs 60'),('SALAD','Rs 40'))):
        stext(a,(-.8,9.86,3.28-k*.24),.13,'#F4F1EA'); stext(b,(1.3,9.86,3.28-k*.24),.13,'#F2C14E')
    # tube lights + fans
    for x in (-3,0,3):
        for y in (3.5,7.5): B.box((x,y,4.35),(.6,.05,.04),M('#F4FAFF',.2,emit=6),.02)
    FANS=[]
    for x,y in ((-2.8,5.5),(2.8,5.5)):
        B.cyl((x,y,4.2),.03,.4,M('#3A3E48',.4),seg=6); FANS.append(empty((x,y,3.95)))
        oc=ocyl((0,0,0),.15,.12,M('#E8E4DA',.4),FANS[-1],rot=(0,0,0),seg=12)
        for a in range(3): obox((math.cos(a*2.094)*.6,math.sin(a*2.094)*.6,0),(.55,.1,.012),M('#E8E4DA',.5),.01,FANS[-1],rot=(0,0,a*2.094))
    # hero table: steel top, long along y
    B.box((HT[0],HT[1],1.0),(.62,1.6,.03),ch,.02)
    for sx in (-.5,.5):
        for sy in (-1.45,1.45): B.cyl((HT[0]+sx,HT[1]+sy,.5),.03,1.0,ch,seg=6)
    B.cyl((HT[0],HT[1]+1.1,1.12),.07,.2,M('#C9CED8',.1,spec=1,alpha=.5),seg=10); B.cyl((HT[0]+.15,HT[1]+1.15,1.08),.05,.12,M('#E8554D',.5),seg=8)
    for k,(x,y) in TSEATS.items(): stool(x,y,'#C8372D' if k in ('wa','al') else '#2B58C9')
    # other tables with customers
    BG=[]
    for tx,ty in ((-4.0,3.6),(4.0,3.6),(-4.0,7.6),(4.0,7.6)):
        B.box((tx,ty,1.0),(.6,.9,.03),ch,.02)
        for sx in (-.5,.5):
            for sy in (-.8,.8): B.cyl((tx+sx,ty+sy,.5),.03,1.0,ch,seg=6)
        for sy in (-.45,.45): B.cyl((tx,ty+sy,1.07),.2,.04,M('#F4F1EA',.3),seg=14); B.cyl((tx,ty+sy,1.1),.16,.03,M('#F2C45A',.6),seg=14)
        for sx in (-1,1):
            if r.random()<.8: stool(tx+sx*1.1,ty,r.choice(['#C8372D','#2B58C9'])); BG.append((tx+sx*1.1,ty,-90*sx))
    # street side: opposite shops, palm, bikes, rickshaw
    for k,(cx,sg,c) in enumerate(((-13,'FAZAL MEDICAL STORE','#2B58C9'),(-21,'NEW CHAI SHOP','#1E6A3A'),(13,'ITTEFAQ TAILORS','#7A1F2E'),(21,'KARACHI PAN SHOP','#D9811A'))):
        facade(cx,7.5,3,r.choice(['#E8D8B8','#C9D6D8','#D8C4A0']),sg,c,40+k,side=1,Y=.2)
    for k in range(5): facade(-24+k*12,11,r.randint(3,5),r.choice(['#E8D8B8','#C9D6D8','#D8C4A0','#B8C8D0']),r.choice(['AL-MADINA STORE','SUPER MART','FRESH JUICE','MOBILE HUB','BAKERY']),r.choice(['#C8372D','#1E6A3A','#2B58C9']),60+k,side=-1,Y=9.5)
    B.box((0,-9.2,.08),(30,1.2,.08),M('#B8A890',.85,kind='tile'),0)
    palm(-8.5,-2.8,1.0,3); palm(9,-2.9,1.1,4)
    wires(-25,25,-.6,-8.6,6.6,4,8)
    B.done('rest')
    S=dict(bg=BG,fans=FANS)
    if car_: S['car']=suv((-9.0,-5.4,.55),90)
    for x in (6.5,7.5): mb=motorbike((x,-3.4,0),90,r.choice(['#C8372D','#16171C'])); mb['root'].scale=(1.4,)*3
    rk=rickshaw((14,-6.2,0),180,'#2E8A3A'); rk['root'].scale=(VSC,)*3
    setup_world('dusk',60)
    point((0,3.5,4.0),420,(.9,.97,1.0),r=1.5,shadow=True); point((0,7.5,4.0),380,(.9,.97,1.0),r=1.5,shadow=False); point((-3,5.5,3.8),200,(.9,.97,1.0),r=1.0,shadow=False); point((3,5.5,3.8),200,(.9,.97,1.0),r=1.0,shadow=False); point((0,-1.0,3.2),160,(1,.85,.65),r=1.2,shadow=False)
    point((0,-7,4),500,(1,.8,.6),r=3,shadow=False)
    return S
def fans_spin(S,t):
    for f in S['fans']: f.rotation_euler[2]=t*9.0
