# Sets for "The Sindhi Family": Chacha's baithak (floor seating, ajrak hangings, Hala tiles, carved doors), the house front on a
# Hyderabad-style lane (tile panels, jharokha, bougainvillea, neem), Ali's car. Food that keeps arriving.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
AJ=lambda: M('#8E1F2A',.9,kind='fabric',h2='#1F2A5A',sc=6)     # ajrak-like crimson/indigo
AJ2=lambda: M('#1F2A5A',.9,kind='fabric',h2='#8E1F2A',sc=9)
TILE=lambda: M('#F4F1EA',.35,kind='tile',h2='#2B5AA8',sc=6,spec=.7)
def bolster(x,y,rz=0,col='#8E1F2A'):
    B.cyl((x,y,.32 if abs(y)<3 else .68),.16,1.1,M(col,.9,kind='fabric',h2='#D9B24A',sc=5),rot=(0,R(90),R(rz)),seg=12)
def carved_door(x,y,w=1.6,h=2.6,rz=0,open_=0.0):
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#5A3420',.6,kind='wood'); br=M('#C9A24A',.3,metal=.8)
    obox((0,0,h+.15),(w/2+.2,.18,.15),wd,.03,e)
    for s in (-1,1):
        hg=empty((s*w/2,0,0),e,rot=(0,0,R(-s*80*open_)))
        obox((-s*w/4,0,h/2),(w/4,.05,h/2),wd,.02,hg)
        for k in range(4):
            for j in range(2): obox((-s*w/4+(j-.5)*w*.22,-.06,.45+k*.58),(w*.08,.02,.2),M('#4A2A18',.6,kind='wood'),.02,hg)
        for k in range(5): ocyl((-s*w/4,-.07,.3+k*.5),.035,.02,br,hg,rot=(R(90),0,0),seg=8)
    return e
def baithak():
    fl=M('#C9B48A',.5,kind='tile',h2='#B8A070',sc=1.1,spec=.6); wl=M('#E9DCC0',.9,kind='wall')
    W_,D_=5.0,3.6
    B.box((0,0,-.05),(W_,D_,.05),fl,0); B.box((0,0,3.6),(W_,D_,.05),M('#F2E8D4',.9),0)
    for s in (-1,1): B.box((s*W_,0,1.8),(.1,D_,1.8),wl,0)
    B.box((0,D_,1.8),(W_,.1,1.8),wl,0)
    # tile dado + wooden ceiling beams
    B.box((0,D_-.12,.55),(W_-.05,.03,.55),TILE(),.0); B.box((-W_+.12,0,.55),(.03,D_-.05,.55),TILE(),0); B.box((W_-.12,0,.55),(.03,D_-.05,.55),TILE(),0)
    B.box((0,D_-.14,1.12),(W_,.03,.04),M('#2B5AA8',.4),0)
    for x in (-3.6,-1.8,0,1.8,3.6): B.box((x,0,3.5),(.12,D_,.1),M('#5A3420',.6,kind='wood'),.02)
    # ajrak hangings + arched niches with brass + lantern
    B.box((-2.4,D_-.08,2.35),(1.0,.02,.75),AJ(),.02); B.box((2.4,D_-.08,2.35),(1.0,.02,.75),AJ2(),.02)
    for x in (-.6,.6):
        B.box((x,D_-.1,2.2),(.35,.05,.55),M('#D8C8A0',.8,kind='wall'),.04)
        B.cyl((x,D_-.2,1.86),.12,.3,M('#C9A24A',.3,metal=.8),seg=10,r2=.07)
    B.cyl((0,0,3.2),.015,.8,M('#3A2A1E',.5),seg=4); B.box((0,0,2.7),(.18,.18,.24),M('#C9A24A',.3,metal=.8),.05); B.box((0,0,2.7),(.14,.14,.2),M('#FFE2A0',.3,emit=6),.03)
    # window on the left wall with Hala-tile frame and jali
    B.box((-W_+.06,-.9,1.9),(.04,.8,.75),M('#9FC8E0',.05,spec=1.0,alpha=.25),0)
    for k in range(7): B.box((-W_+.08,-1.6+k*.23,1.9),(.02,.02,.72),M('#5A3420',.6,kind='wood'),0)
    B.box((-W_+.1,-.9,2.75),(.04,.95,.12),TILE(),.01); B.box((-W_+.1,-.9,1.05),(.04,.95,.12),TILE(),.01)
    # floor seating: gaddas along back and sides + bolsters
    for (x,y,w,d,rz,hh) in ((0,D_-.55,4.2,.45,0,.25),(-W_+.55,.6,.45,2.4,0,.14),(W_-.55,.6,.45,2.4,0,.14)):
        B.box((x,y,hh),(w,d,hh),M('#E8C86A',.9,kind='fabric',h2='#8E1F2A',sc=4),.06)
    for x in (-3.2,-1.6,0,1.6,3.2): bolster(x,D_-.15,0,['#8E1F2A','#1F2A5A','#2B8A5A'][int(abs(x))%3])
    for y in (-.8,.6,2.0): bolster(-W_+.25,y,90,'#8E1F2A'); bolster(W_-.25,y,90,'#1F2A5A')
    # rug + low table
    B.box((0,1.2,.01),(3.3,1.4,.01),M('#7A1F2E',.95,kind='fabric',h2='#D9B24A',sc=2.2),0)
    B.box((0,1.6,.32),(1.9,.55,.04),M('#6A3A22',.5,kind='wood'),.03)
    for dx in (-1.75,1.75):
        for dy in (1.2,2.0): B.box((dx,dy,.15),(.05,.05,.15),M('#6A3A22',.5,kind='wood'),.01)
    B.box((0,1.6,.365),(1.7,.45,.005),M('#F4F1EA',.8,kind='fabric',h2='#C8372D',sc=8),0)
    # side: TV cabinet + plants
    B.box((W_-.4,-2.6,.45),(.3,.8,.45),M('#5A3420',.6,kind='wood'),.03); B.box((W_-.32,-2.6,1.25),(.04,.65,.38),M('#16171C',.3,spec=.8),.02)
    B.cyl((-W_+.5,-2.9,.3),.25,.6,M('#B5603F',.8),seg=10,r2=.2); B.ico((-W_+.5,-2.9,1.0),.45,M('#3F7A3A',.85,kind='leaves'),sc=(1,1,1.3),sub=1)
    # doorway on front-right
    carved_door(3.0,-D_+.05,1.6,2.6,0,1.0)
    B.box((0,-D_,1.8),(W_,.1,1.8),wl,0) if False else None
    B.box((-1.0,-D_,1.8),(3.2,.1,1.8),wl,0); B.box((4.4,-D_,1.8),(.6,.1,1.8),wl,0); B.box((3.0,-D_,3.25),(.85,.1,.35),wl,0)
    # outside the window: neem + wall
    B.box((-9,0,2),(.3,8,2),M('#D8C8A8',.9,kind='wall'),0); tree(-7,1,1.2,'#4E7E3A','#5A3E28'); tree(-7.5,-3,1.1,'#5E8A44','#5A3E28')
def dish(x,y,kind,z=.37,s=1.0):
    e=empty((x,y,z)); pl=M('#F8F6F0',.3,spec=.8); st=M('#C9CED8',.25,metal=.8)
    if kind=='tea':
        for k,(dx,dy) in enumerate(((-.12,0),(.12,.05),(0,-.12))): ocyl((dx,dy,.005),.08,.01,pl,e,rot=(0,0,0),seg=14); ocyl((dx,dy,.05),.045,.08,M('#F4F1EA',.4),e,rot=(0,0,0),seg=12); ocyl((dx,dy,.088),.04,.005,M('#B5703A',.4),e,rot=(0,0,0),seg=12)
        ocyl((.3,.1,.08),.08,.16,st,e,rot=(0,0,0),seg=12); obox((.4,.1,.1),(.06,.01,.015),st,0,e)
        for k in range(5): ocyl((-.32+.05*k,.12,.015+.004*k),.05,.008,M('#D9A44A',.6),e,rot=(0,0,0),seg=10)
    if kind=='biryani':
        ocyl((0,0,.02),.26,.03,pl,e,rot=(0,0,0),seg=18); oico((0,0,.08),.2,M('#F2B84E',.8),e,sc=(1,1,.5),sub=2); r=random.Random(int(x*10+y*7))
        for k in range(8): obox((r.uniform(-.13,.13),r.uniform(-.13,.13),.15),(.035,.025,.02),M(r.choice(['#8A4A22','#F28A3A','#F4F1EA','#4F9A3A']),.7),.008,e,rot=(0,0,r.uniform(0,3)))
    if kind=='fruit':
        ocyl((0,0,.04),.22,.08,M('#C9A24A',.3,metal=.8),e,rot=(0,0,0),seg=16,r2=.12); r=random.Random(5)
        for k in range(9): oico((r.uniform(-.12,.12),r.uniform(-.12,.12),.12+r.uniform(0,.1)),.065,M(r.choice(['#F2C14E','#E8423A','#F28A1A','#7AB840']),.5),e,sub=1)
        obox((.05,0,.26),(.1,.03,.025),M('#F2D84E',.5),.01,e,rot=(0,R(30),0))
    if kind=='karahi': karahi_obj((0,0,.0),.6,parent=e)
    if kind=='kebab':
        ocyl((0,0,.01),.2,.02,pl,e,rot=(0,0,0),seg=16)
        for k in range(4): ocyl((-.09+.06*k,0,.05),.025,.24,M('#6A3A22',.8),e,rot=(R(90),0,R(10)),seg=6)
        oico((.1,.08,.04),.05,M('#E8E2C0',.6),e,sub=1)
    if kind=='halwa':
        ocyl((0,0,.03),.18,.06,M('#F4F1EA',.3),e,rot=(0,0,0),seg=16); ocyl((0,0,.065),.16,.02,M('#E87A2A',.5),e,rot=(0,0,0),seg=16)
        for k in range(5): oico((math.cos(k)*.09,math.sin(k)*.09,.08),.015,M('#7AB840',.5),e,sub=1)
    if kind=='naan':
        for k in range(4): ocyl((.01*k,0,.015+k*.02),.17,.018,M('#E8C88A',.8,h2='#B5642A',sc=9),e,rot=(0,0,0),seg=14)
    return e
def tiffin(e,s=1.0):
    st=M('#C9CED8',.22,metal=.85)
    for k in range(3): ocyl((0,-.1,.06+k*.11*s),.1*s,.1*s,st,e,rot=(0,0,0),seg=16)
    ocyl((0,-.1,.4*s),.015,.24*s,st,e,rot=(0,R(90),0),seg=6); ocyl((-.11*s,-.1,.25*s),.012,.36*s,st,e,rot=(0,0,0),seg=6); ocyl((.11*s,-.1,.25*s),.012,.36*s,st,e,rot=(0,0,0),seg=6)
def shopper(e,s=1.0,col='#F4F1EA',label=None):
    obox((0,-.1,.08*s),(.15*s,.08*s,.16*s),M(col,.8,kind='fabric'),.02,e); obox((0,-.1,.27*s),(.08*s,.006,.06*s),M('#16171C',.6),.0,e)
    if label: text(label,(0,-.19*s,.1*s),(0,-1,0),.04*s,M('#C8372D',.5),ex=.003,parent=e)
def pot_bag(e,s=1.0):
    obox((0,-.1,.1*s),(.17*s,.1*s,.17*s),M('#2B8A5A',.8,kind='fabric',h2='#F2C14E',sc=5),.04,e); ocyl((0,-.1,.32*s),.12*s,.05*s,M('#C9CED8',.25,metal=.8),e,rot=(0,0,0),seg=14)
# ---------------------------------------------------------------- house front on a Hyderabad lane
def lane(dusk=False):
    r=random.Random(9)
    B.box((0,0,-.05),(40,3.2,.05),M('#9A8C78',.9,kind='tile',h2='#8A7C68',sc=1.0),0)
    for s in (-1,1): B.box((0,s*3.25,.04),(40,.12,.06),M('#6E6A62',.9,kind='concrete'),0)
    # Chacha's house: tall facade, tiled panels, carved door, jharokha balcony, wind catcher
    c='#E8D6B4'; Y=3.4
    B.box((0,Y+3,3.6),(5.0,3,3.6),M(c,.9,kind='wall'),0)
    B.box((0,Y-.02,1.4),(1.45,.05,1.4),M('#C9A24A',.6),0)
    for x in (-3.4,3.4): B.box((x,Y-.04,1.6),(1.1,.03,1.1),TILE(),.0); B.box((x,Y-.06,1.6),(1.18,.02,1.18),M('#2B5AA8',.4),0)
    B.box((0,Y-.7,4.4),(2.0,.7,.1),M('#5A3420',.6,kind='wood'),.02); B.box((0,Y-1.35,4.95),(2.0,.05,.5),M('#5A3420',.6,kind='wood'),.01)
    for k in range(14): B.box((-1.8+k*.28,Y-1.38,4.95),(.03,.03,.45),M('#4A2A18',.6),0)
    B.box((0,Y-.7,5.55),(2.1,.75,.08),M('#5A3420',.6,kind='wood'),.02)
    for x in (-1.6,1.6): B.box((x,Y-.02,5.0),(.5,.05,.55),M('#2A3A4A',.2,spec=.8) if not dusk else M('#FFD98A',.3,emit=2.5),.01)
    B.box((0,Y+3,7.6),(5.05,3.05,.4),M(shade(c,.9),.9,kind='concrete'),.02); B.box((2.8,Y+1.5,8.6),(.6,.6,1.0),M(c,.9,kind='wall'),.03); B.box((2.8,Y+.88,8.9),(.5,.03,.5),M('#3A3D44',.5),0)
    B.box((0,Y-.02,3.05),(1.5,.06,.12),TILE(),.01); stext('HAJI MANZIL',(0,Y-.1,3.05),.16,'#1F2A5A')
    # neighbours
    for (cx,w,col) in ((-9,8,'#D8C8A8'),(9,8,'#C8D4C0'),(-17,8,'#E0C8B8'),(17,8,'#D4C0A0')):
        h=r.choice([6,7.5,9]); B.box((cx,Y+3,h/2),(w/2-.05,3,h/2),M(col,.9,kind='wall'),0)
        for k in range(3): B.box((cx-2.5+k*2.5,Y-.02,h*.7),(.5,.05,.6),M('#FFD98A',.3,emit=2.0) if dusk and r.random()<.6 else M('#2A3A4A',.2,spec=.8),.01)
        B.box((cx,Y-.03,1.2),(1.0,.05,1.2),M(r.choice(['#2B5AA8','#2B8A5A','#8E1F2A']),.5,metal=.3),.02)
    # opposite side wall + gate
    B.box((0,-4.6,1.3),(40,.25,1.3),M('#D8C8A8',.9,kind='wall'),0)
    # neem + bougainvillea + lamp + plants
    tree(-5.6,2.6,1.4,'#4E7E3A','#5A3E28')
    for k in range(18): B.ico((4.2+r.uniform(-.6,.6),Y-.3,1.5+r.uniform(0,2.4)),r.uniform(.15,.3),M(r.choice(['#D9367A','#E8429A','#C82A6A','#3F7A3A']),.8,kind='leaves'),sub=1)
    B.box((4.2,Y-.15,1.0),(.05,.05,1.0),M('#5A3E28',.8),0)
    for (x,c_) in ((-2.0,'#B5603F'),(2.1,'#B5603F')): B.cyl((x,Y-.35,.25),.22,.5,M(c_,.8),seg=10,r2=.17); B.ico((x,Y-.35,.75),.35,M('#3F7A3A',.85,kind='leaves'),sub=1)
    pole(-12,-3.4,7.5); pole(10,-3.4,7.5); wires(-20,20,-3.4,-3.4,7.2,3,2); wires(-20,20,-3.4,3.0,7.4,3,7)
    B.box((1.6,Y-.2,2.9),(.08,.3,.05),M('#3A3D44',.5),0); B.ico((1.6,Y-.4,2.82),.1,M('#FFE2A0',.3,emit=6 if dusk else .5),sub=1)
def sedan(loc,rotz=0,col='#7A1F2E'):
    root=empty(loc,rot=(0,0,R(rotz))); body=M(col,.25,metal=.4,spec=.8); gl=M('#1A2433',.06,spec=1.0); bk=M('#16171C',.6); ch=M('#C9CED8',.3,metal=.9); W=[]
    obox((0,0,.6),(2.3,1.0,.3),body,.12,root); obox((-.2,0,1.12),(1.25,.9,.28),body,.12,root); obox((-.2,0,1.14),(1.27,.91,.2),gl,.06,root)
    obox((1.02,0,1.1),(.12,.86,.22),gl,.04,root,rot=(0,R(-30),0)); obox((-1.42,0,1.1),(.1,.86,.2),gl,.04,root,rot=(0,R(30),0))
    for sy in (-1,1):
        obox((2.3,sy*.7,.72),(.03,.2,.08),M('#FFF6D8',.2,emit=2),.03,root); obox((-2.3,sy*.75,.75),(.03,.18,.08),M('#E8301A',.3,emit=1.6),.02,root)
        obox((-.2,sy*.9,1.16),(.03,.02,.24),body,.0,root); obox((.3,sy*1.0,.75),(.12,.02,.025),ch,.01,root)
    obox((2.33,0,.5),(.04,1.0,.1),bk,.03,root); obox((-2.33,0,.5),(.04,1.0,.1),bk,.03,root); obox((2.34,0,.68),(.01,.45,.08),ch,.01,root)
    for (wx,sy) in ((1.45,-1),(1.45,1),(-1.5,-1),(-1.5,1)): W.append(wheel((wx,sy*.92,.38),.38,.24,root))
    return dict(root=root,wheels=W,r=.38)
