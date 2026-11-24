# Sets for "Baddie Ghar Par": BREW & BLISS cafe, Zoya's gate + street (night / day), kitchen-dining room. None reused from earlier videos.
GY_=3.2     # Zoya's boundary wall line (street side faces -y)
def plant(x,y,z=0,s=1.0,seed=1,pot='#E8E2D6'):
    r=random.Random(seed); B.cyl((x,y,z+.28*s),.26*s,.56*s,M(pot,.6),seg=12,r2=.2*s)
    for k in range(7):
        a=k*0.9+r.uniform(0,.4); h=.7+r.uniform(0,.6)
        B.ico((x+math.cos(a)*.22*s,y+math.sin(a)*.22*s,z+(h+.3)*s),.3*s,M(r.choice(['#3F7A3A','#2E6B3A','#4F8A3A']),.8,kind='leaves'),sc=(1,.5,.7),sub=1,rot=(r.uniform(-.5,.5),0,a))
def chair_cafe(x,y,rz,col='#2A2C34',seat='#C89A6A'):
    e=empty((x,y,0),rot=(0,0,R(rz))); mm=M(col,.4,metal=.6)
    obox((0,0,.58),(.34,.34,.045),M(seat,.6,kind='wood'),.03,e)
    for sx in (-1,1):
        for sy in (-1,1): obox((sx*.28,sy*.28,.29),(.025,.025,.29),mm,.01,e)
    obox((0,.31,1.0),(.32,.03,.3),M(seat,.6,kind='wood'),.03,e); obox((0,.31,.75),(.3,.02,.04),mm,.01,e)
    return e
def table_round(x,y,r_=.7,h=1.0,top='#F2EEE6'):
    B.cyl((x,y,h-.03),r_,.06,M('#D8CEC0',.35),seg=28); B.cyl((x,y,h/2),.06,h,M('#2A2C34',.4,metal=.6),seg=10); B.cyl((x,y,.03),.32,.06,M('#2A2C34',.4,metal=.6),seg=20)
def cafe_z():
    """BREW & BLISS: warm interior, brick back wall, window wall onto a sunny street, counter + menu board, pendants, plants."""
    W,D,Ht=7.0,5.0,4.2
    B.box((0,0,-.05),(W,D,.05),M('#C79A6A',.55,kind='tile',sc=2.2,h2='#B2855A'),0)                                  # wood floor
    B.box((0,D,Ht/2),(W,.1,Ht/2),M('#B5684A',.85,kind='tile',sc=.35,h2='#E8D8C8'),0)                                            # brick back wall
    B.box((0,0,Ht+.05),(W,D,.05),M('#3A2E28',.9,kind='wood'),0); B.box((0,-D,Ht/2),(W,.1,Ht/2),M('#EFE6D8',.9,kind='wall'),0)
    for x in (-W,W): B.box((x,0,Ht/2),(.1,D,Ht/2),M('#EFE6D8',.9,kind='wall'),0)
    # window wall on the left (x=-W): frames + bright street outside
    for k in range(4):
        y=-3.0+k*2.0; B.box((-W+.05,y,2.2),(.04,.9,1.5),M('#BFE3F2',.05,emit=.9,alpha=.35),0)
        B.box((-W+.08,y-.95,2.2),(.06,.05,1.55),M('#1E2026',.4,metal=.5),0)
    B.box((-W+.08,0,.65),(.06,D,.05),M('#1E2026',.4,metal=.5),0); B.box((-W+.08,0,3.75),(.06,D,.05),M('#1E2026',.4,metal=.5),0)
    for k in range(6): B.box((-W-2.5,-4+k*1.6,1.5+k%2*.6),(.5,.6,1.5+k%2*.6),M(random.Random(k).choice(['#F2C14E','#E8A0A8','#9FD3C7','#F4F1EA']),.8),0)  # street beyond glass
    # counter + espresso machine + menu board on the right
    B.box((4.8,1.8,.6),(1.6,.55,.6),M('#2E3A34',.6,kind='wood'),.02); B.box((4.8,1.8,1.23),(1.7,.62,.04),M('#F4F1EA',.25,kind='marble'),.01)
    B.box((5.2,2.0,1.55),(.4,.3,.3),M('#C9CED8',.25,metal=.9),.04); B.box((5.2,1.68,1.45),(.08,.06,.1),M('#16171C',.4),.01)
    for k in range(5): B.cyl((4.0+k*.22,1.6,1.33),.06,.16,M(random.Random(k+5).choice(['#F4F1EA','#E8C547','#9FD3C7']),.4),seg=10)
    B.box((4.8,D-.12,2.8),(1.6,.04,.75),M('#22262A',.7),.02)
    stext('MENU',(4.8,D-.17,3.3),.22,'#F4F1EA',n=(0,-1,0));
    for i,(a,b) in enumerate((('ICED LATTE','650'),('CARAMEL FRAPPE','790'),('MATCHA','720'),('CROISSANT','450'))):
        stext(a,(4.35,D-.17,2.95-i*.25),.11,'#F4F1EA',n=(0,-1,0)); stext(b,(5.95,D-.17,2.95-i*.25),.11,'#E8C547',n=(0,-1,0))
    # neon sign on brick
    B.box((-1.2,D-.12,3.15),(1.85,.03,.48),M('#2A1E1A',.6),.02)
    stext('BREW & BLISS',(-1.2,D-.17,3.15),.34,'#FFD27A',n=(0,-1,0),e=3.0)
    stext('but first, coffee',(-1.2,D-.17,2.72),.13,'#FF9EC4',n=(0,-1,0),e=2.5)
    # shelves with jars/cups + frames
    for z in (1.7,2.25):
        B.box((2.2,D-.25,z),(.9,.15,.03),M('#6E4A2E',.6,kind='wood'),.01)
        for k in range(5): B.cyl((1.55+k*.32,D-.25,z+.12),.07,.2,M(random.Random(k+int(z*10)).choice(['#F4F1EA','#2E6B4F','#E8C547','#C8372D']),.4),seg=10)
    for i,(x,c) in enumerate(((-4.2,'#E8A0A8'),(-3.3,'#9FD3C7'))): B.box((x,D-.13,2.2),(.35,.02,.45),M('#F4F1EA',.6),.01); B.box((x,D-.15,2.2),(.28,.01,.37),M(c,.6),0)
    # pendants
    for x in (-3,0,3):
        B.box((x,.2,Ht-.5),(.008,.008,.5),M('#16171C',.5),0); B.cyl((x,.2,Ht-1.05),.25,.25,M('#1E2026',.4,metal=.6),seg=18,r2=.08)
        B.ico((x,.2,Ht-1.15),.1,M('#FFE2A8',.2,emit=6),sub=2)
        point((x,.2,Ht-1.3),260,(1,.82,.6),r=.15)
    # other tables / plants
    for (x,y) in ((-3.6,1.8),(3.2,-1.8),(-4.0,-2.2)):
        table_round(x,y,.6); chair_cafe(x-.95,y,90); chair_cafe(x+.95,y,-90)
    plant(-6.2,4.2,s=1.4,seed=1); plant(6.3,-4,s=1.3,seed=2); plant(-6.2,-4.3,s=1.1,seed=3); plant(6.3,4.2,s=1.0,seed=4)
    B.done('cafe')
TABLE=(0,.6)
def gate_leaves():
    """black steel double gate; returns hinge empties (x=-1.3 / +1.3) — rotate z to open (inward = +y)"""
    gm=M('#1C1E24',.35,metal=.7); gold=M('#C9A24A',.3,metal=.9); out=[]
    for s in (-1,1):
        h=empty((s*1.3,GY_,0)); L_=1.28
        for z in (.15,1.2,2.35): obox((-s*L_/2,0,z),(L_/2,.05,.05),gm,.01,h)
        for k in range(9): obox((-s*(.08+k*.145),0,1.25),(.022,.03,1.15),gm,.005,h)
        obox((-s*L_/2,0,.62),(L_/2-.04,.02,.45),gm,.01,h)
        obox((-s*(L_-.06),-.07,1.25),(.03,.04,.12),gold,.01,h)
        out.append(h)
    return out
def house_z(night=True):
    """street + Zoya's boundary wall with the black gate, house behind, neighbours either side, Waleed's bike."""
    G=GY_; road=M('#55565A',.85,kind='asphalt',sc=.6)
    B.box((0,-4,-.05),(40,9,.05),road,0); B.box((0,G-.9,.06),(40,.9,.06),M('#B8B0A2',.85,kind='concrete',sc=.8),.01)   # footpath
    B.box((0,G-1.82,.08),(40,.04,.08),M('#E8E2D6',.7),.01)
    for k in range(12): B.box((-30+k*5.5,-5.5,.003),(1.2,.06,.003),M('#E8E2D6',.6),0)   # lane dashes
    wall=M('#E8DCC4',.85,kind='wall',sc=.6); cap=M('#B8A88A',.8)
    for a,b in ((-9,-1.42),(1.42,9)):
        B.box(((a+b)/2,G+.12,1.3),((b-a)/2,.15,1.3),wall,0); B.box(((a+b)/2,G+.12,2.66),((b-a)/2+.04,.2,.07),cap,.01)
    for x in (-1.5,1.5):
        B.box((x,G+.12,1.5),(.18,.22,1.5),M('#D8C8A8',.8,kind='wall'),.02); B.box((x,G+.12,3.05),(.22,.26,.06),cap,.01)
        B.box((x,G-.14,3.25),(.12,.12,.16),M('#1C1E24',.4,metal=.6),.02); B.box((x,G-.14,3.25),(.09,.13,.12),M('#FFE6B0',.2,emit=4 if night else .4),.01)
        if night: point((x,G-.4,3.2),60,(1,.85,.6),r=.1)
    B.box((1.95,G-.04,1.85),(.32,.02,.2),M('#F4F1EA',.3,kind='marble'),.01); stext('27-B',(1.95,G-.07,1.88),.17,'#2A2C34')
    B.box((-2.25,G-.04,1.5),(.13,.05,.08),M('#C9CED8',.4),.01); B.box((-2.25,G-.1,1.5),(.03,.01,.03),M('#C8372D',.4,emit=1),0)      # door bell
    # house behind: 2 storeys, lit windows
    hc=M('#F2EEE4',.85,kind='wall'); win=M('#FFD98A' if night else '#7A9AAA',.2,emit=2.2 if night else 0)
    B.box((0,G+7.0,3.2),(5.5,4.0,3.2),hc,0); B.box((0,G+7.0,6.55),(5.7,4.2,.15),M('#C9BFAE',.8),0)
    for x in (-3.4,0,3.4):
        for z in (1.8,4.8):
            if (x,z)==(0,1.8): continue
            B.box((x,G+2.98,z),(.85,.03,.7),win,0); B.box((x,G+2.94,z),(.95,.04,.06),M('#6E5A44',.6),0); B.box((x,G+2.94,z-.75),(.95,.08,.05),M('#C9BFAE',.8),0)
    B.box((0,G+2.98,1.35),(.65,.04,1.35),M('#5E3A22',.6,kind='wood'),.02); B.box((0,G+2.9,2.85),(.85,.12,.06),M('#C9BFAE',.8),.01)                       # front door
    B.box((0,G+1.6,0.05),(4.8,1.4,.05),M('#9A9488',.85,kind='tile',sc=1.5),0)
    for k in range(4): plant(-3.6+k*.5*0+[0,1.2,5.8,7.0][k]-0.0,G+2.4,s=.9,seed=10+k)                          # porch
    for k in range(10): B.ico((-8+k*.8+random.Random(k).uniform(-.2,.2),G+.25,2.75+random.Random(k+9).uniform(0,.35)),.42,M(random.Random(k+3).choice(['#D9367A','#E8559A','#C2306A']),.85,kind='leaves'),sub=1,sc=(1.2,.8,.7))   # bougainvillea
    for k in range(6): B.ico((4.5+k*.75,G+.3,2.8+random.Random(k).uniform(0,.3)),.36,M('#3F7A3A',.85,kind='leaves'),sub=1,sc=(1.2,.8,.7))
    # neighbours
    for cx,col in ((-14,'#C9DCE4'),(14,'#F0D2B8')):
        B.box((cx,G+.12,1.3),(5,.15,1.3),M(col,.85,kind='wall'),0); B.box((cx,G+4.5,3.0),(4.5,3.6,3.0),M(shade(col,.95),.85,kind='wall'),0)
        for x in (cx-2,cx+2): B.box((x,G+.88,4.4),(.7,.03,.6),win if night else M('#7A9AAA',.2),0)
    # street lamp + far side wall + parked car + trees
    B.cyl((-6.5,G-1.6,3.0),.08,6.0,M('#5A5E66',.4,metal=.6),seg=8); B.box((-6.0,G-1.6,5.95),(.55,.08,.05),M('#5A5E66',.4,metal=.6),.01)
    B.box((-5.55,G-1.6,5.86),(.2,.12,.05),M('#FFE6B0',.2,emit=6 if night else .3),.01)
    if night: point((-5.55,G-1.8,5.6),900,(1,.82,.55),r=.3)
    B.box((0,-11.5,1.4),(40,.2,1.4),M('#D8D0C0',.85,kind='wall'),0)
    for x in (-10,-3,6,12): tree(x,-10.5,1.1)
    car((-9.0,G-2.6,0),0,'#C9CED8',seed=3)
    B.done('street')
    return gate_leaves()
def dish(x,y,z,r_=.17,col='#F4F1EA',tilt=0):
    B.cyl((x,y,z),r_,.03,M(col,.25,spec=.8),seg=20,rot=(tilt,0,0),r2=r_*.8)
def kitchen_z(night=True):
    """kitchen with steel sink under a window, tiled wall, plate rack, stove; dining table on the right (x>3)."""
    Ht=3.6; W=7.5
    B.box((0,0,-.05),(W,4,.05),M('#D8D2C6',.6,kind='tile',sc=1.3),0)
    B.box((0,2.4,Ht/2),(W,.1,Ht/2),M('#F2EEE6',.9,kind='wall'),0); B.box((0,0,Ht+.05),(W,4,.05),M('#F4F1EA',.9),0)
    B.box((-1.5,2.28,1.55),(2.6,.02,.55),M('#9FD3C7',.35,kind='tile',sc=3.0,h2='#F4F1EA'),0)            # splash tiles
    for x in (-W,): B.box((x,0,Ht/2),(.1,4,Ht/2),M('#EFE8DA',.9,kind='wall'),0)
    # counter + sink
    B.box((-1.5,1.85,.55),(2.6,.5,.55),M('#5E7A6A',.6,kind='wood'),.02); B.box((-1.5,1.82,1.13),(2.65,.55,.04),M('#C9C2B4',.35,kind='marble'),.01)
    B.box((-1.0,1.78,1.06),(.7,.36,.1),M('#C9CED8',.2,metal=.9),.02); B.box((-1.0,1.78,1.0),(.62,.3,.06),M('#8A9098',.3,metal=.9),.01)
    B.cyl((-1.0,2.15,1.35),.03,.5,M('#C9CED8',.2,metal=.9),seg=10); B.box((-1.0,2.0,1.58),(.03,.17,.03),M('#C9CED8',.2,metal=.9),.01)
    for k in range(5): dish(-1.25+k*.06,1.7,1.05+k*.035,col=random.Random(k).choice(['#F4F1EA','#E8C547','#9FD3C7']))
    B.cyl((-.75,1.85,1.2),.16,.25,M('#C9CED8',.25,metal=.9),seg=16)                                   # pot in the sink
    for k in range(4): B.cyl((-2.6+k*.07,1.95,1.32),.18,.02,M('#F4F1EA',.25),seg=20,rot=(R(80),0,0))    # rack plates
    B.box((-2.45,1.95,1.25),(.35,.15,.1),M('#C9CED8',.3,metal=.8),.01)
    B.box((-1.0,1.7,1.22),(.06,.04,.08),M('#2E8A6A',.4),.01); B.box((-.85,1.7,1.18),(.08,.05,.03),M('#E8C547',.6),.01)            # soap + sponge
    # window above the sink
    B.box((-1.0,2.3,2.4),(.75,.02,.55),M('#1E2A4A' if night else '#BFE3F2',.1,emit=.3 if night else 1.0),0)
    B.box((-1.0,2.26,2.4),(.8,.04,.6),M('#F4F1EA',.6),.01); B.box((-1.0,2.24,2.4),(.02,.03,.55),M('#F4F1EA',.6),0)
    # stove + shelves + jars
    B.box((.75,1.85,1.2),(.45,.35,.05),M('#16171C',.3,metal=.6),.01)
    for x in (.55,.95): B.cyl((x,1.85,1.27),.12,.04,M('#2A2C34',.3,metal=.7),seg=14)
    B.cyl((.95,1.85,1.42),.18,.26,M('#3A3E48',.3,metal=.7),seg=16)
    B.box((-1.5,2.2,2.95),(1.6,.18,.03),M('#6E4A2E',.6,kind='wood'),.01)
    for k in range(7): B.cyl((-2.8+k*.42,2.2,3.1),.1,.26,M(random.Random(k+20).choice(['#E8C547','#C8372D','#F4F1EA','#8A5A36']),.5),seg=12)
    B.box((-3.6,1.6,1.6),(.45,.45,1.6),M('#E8E8E2',.4),.02); B.box((-3.6,1.13,1.6),(.02,.01,.4),M('#C9CED8',.3,metal=.8),0)       # fridge
    # dining corner on the right
    B.box((4.2,.6,.95),(1.1,.65,.04),M('#8A5A36',.45,kind='wood'),.02)
    for sx in (-1,1):
        for sy in (-1,1): B.box((4.2+sx*1.0,.6+sy*.55,.47),(.05,.05,.47),M('#6E4A2E',.5,kind='wood'),0)
    for (x,y) in ((3.7,.25),(4.7,.25),(4.2,1.0)): dish(x,y,1.0,.2,'#F4F1EA')
    B.cyl((4.2,.6,1.1),.2,.18,M('#C9CED8',.25,metal=.9),seg=16)
    for (x,y,b) in ((3.55,-.5,-1),(4.85,-.5,-1),(4.2,1.75,1)):                           # dining chairs (seat .58, back away from table)
        cw=M('#6E4A2E',.55,kind='wood'); B.box((x,y,.56),(.3,.3,.04),cw,.02)
        for sx in (-1,1):
            for sy in (-1,1): B.box((x+sx*.25,y+sy*.25,.27),(.03,.03,.27),cw,0)
        B.box((x,y+b*.28,1.0),(.3,.03,.42),cw,.02)
    B.box((6.2,2.3,2.2),(.5,.02,.4),M('#F4F1EA',.6),.01); B.box((6.2,2.28,2.2),(.42,.01,.32),M('#C8956A',.6),0)    # frame
    lamp=M('#FFF2D8',.2,emit=4)
    B.box((-1.0,0,Ht-.05),(1.0,.12,.03),lamp,0); B.box((4.2,.6,Ht-.05),(.6,.12,.03),lamp,0)
    point((-1.0,.6,Ht-.4),220,(1,.95,.88),r=.4); point((4.2,.6,Ht-.4),180,(1,.9,.78),r=.4)
    B.done('kitchen')
SINK=(-1.0,1.05)
