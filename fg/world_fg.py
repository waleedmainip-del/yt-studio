# Sets for "Family Group": Waleed's room, Abbu's room, lounge (Dadi), night lane (Chacha's door + Phuppo's gate), Phuppo's drawing room.
BALLS=[]
def lamp_glow(x,y,z,col='#FFE2A8',e=5,P=60,rgb=(1,.82,.6)):
    B.ico((x,y,z),.09,M(col,.2,emit=e),sub=2); point((x,y,z-.1),P,rgb,r=.15)
def frame(x,y,z,w,h,col,face=(0,-1,0),inner='#F4F1EA'):
    B.box((x,y,z),(w,.02,h),M('#5E3A22',.5,kind='wood'),.01); B.box((x,y-.025,z),(w-.05,.01,h-.05),M(col,.6),0)
def bed(x,y,w=1.0,L=2.2,top='#3A5A8A',pil='#F4F1EA',rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#6E4A2E',.5,kind='wood')
    obox((0,0,.3),(w,L/2,.18),wd,.03,e); obox((0,0,.55),(w-.05,L/2-.05,.12),M('#F2EEE4',.7,kind='fabric'),.05,e)
    obox((0,L/2-.08,.95),(w,.08,.55),wd,.03,e); obox((0,L/2-.42,.72),(w-.25,.2,.1),M(pil,.7,kind='fabric'),.07,e)
    obox((0,-.25,.69),(w-.02,L/2-.55,.05),M(top,.8,kind='fabric'),.03,e)
    return e
def home_fg():
    Ht=3.6; fl=M('#C9B79C',.6,kind='tile',sc=1.4,h2='#B8A486')
    B.box((1.5,0,-.05),(15,4.5,.05),fl,0); B.box((1.5,0,Ht+.05),(15,4.5,.05),M('#F2EEE6',.9),0)
    B.box((1.5,3.0,Ht/2),(15,.1,Ht/2),M('#E8DCC8',.9,kind='wall'),0)
    for x in (-3.6,5.6):
        B.box((x,1.0,Ht/2),(.1,2.0,Ht/2),M('#E8DCC8',.9,kind='wall'),0); B.box((x,-1.6,Ht-.35),(.1,.6,.35),M('#E8DCC8',.9,kind='wall'),0)
    for x in (-13.5,16.5): B.box((x,0,Ht/2),(.1,4.5,Ht/2),M('#E8DCC8',.9,kind='wall'),0)
    # --- Waleed's room (x -13..-3.6): bed, desk, posters, window, lamp
    B.box((-8.5,2.9,Ht/2),(4.9,.02,Ht/2),M('#4A6E8A',.85,kind='wall'),0)              # blue accent wall
    bed(-9.2,1.75,1.0,2.4,'#2E3A5A','#E8C547',rz=90)
    B.box((-11.2,2.5,.45),(.45,.4,.45),M('#6E4A2E',.5,kind='wood'),.02); B.cyl((-11.2,2.5,1.05),.12,.3,M('#E8E2D6',.5),seg=12)
    B.cyl((-11.2,2.5,1.32),.25,.25,M('#F4E2B0',.4,emit=1.5),seg=14,r2=.15); point((-11.2,2.3,1.5),45,(1,.8,.55),r=.2)
    B.box((-6.0,2.55,.95),(1.0,.4,.04),M('#2A2C34',.4),.01)
    for sx in (-1,1): B.box((-6.0+sx*.95,2.55,.47),(.04,.36,.47),M('#2A2C34',.4),0)
    B.box((-6.0,2.6,1.25),(.45,.03,.28),M('#16171C',.3),.01); B.box((-6.0,2.58,1.25),(.42,.01,.25),M('#3A5AFF',.3,emit=1.2),0)
    frame(-8.0,2.86,2.5,.55,.75,'#C8372D'); stext('PSL',(-8.0,2.83,2.55),.26,'#F4F1EA'); frame(-10.2,2.86,2.45,.45,.6,'#2E8A6A')
    B.box((-12.6,2.88,2.2),(.6,.02,.6),M('#1E2A4A',.1,emit=.35),0); B.box((-12.6,2.86,2.2),(.66,.03,.66),M('#F4F1EA',.6),0)
    B.box((-6.4,-1.0,.02),(1.3,1.0,.01),M('#7A4A8A',.9,kind='fabric'),0)                    # rug
    # --- Abbu's room (x -3.6..5.6): double bed, wardrobe, clock, frames, night bulb
    bed(1.2,1.6,1.4,2.5,'#7A3A2E','#F4F1EA')
    B.box((3.9,2.55,1.6),(1.0,.4,1.6),M('#8A5E3A',.5,kind='wood'),.02); B.box((3.9,2.14,1.6),(.02,.01,1.4),M('#5E3A22',.5),0)
    B.box((-1.3,2.6,.4),(.45,.35,.4),M('#8A5E3A',.5,kind='wood'),.02); B.cyl((-1.3,2.6,.95),.1,.25,M('#C9CED8',.3,metal=.6),seg=10)
    B.cyl((1.2,2.88,2.75),.32,.05,M('#F4F1EA',.4),seg=24,rot=(R(90),0,0)); B.cyl((1.2,2.86,2.75),.34,.04,M('#2A2C34',.4),seg=24,rot=(R(90),0,0))
    for k,(x,c) in enumerate(((-.6,'#C9A06A'),(3.0,'#9FD3C7'))): frame(x,2.86,2.4,.35,.45,c)
    B.ico((1.2,0,Ht-.2),.08,M('#AFC8FF',.2,emit=3),sub=2); point((1.2,0,Ht-.4),70,(.65,.75,1.0),r=.2)
    B.box((-2.4,-1.5,.02),(.6,1.0,.01),M('#2E6B4F',.9,kind='fabric'),0)                     # prayer mat
    # --- lounge (x 5.6..16.5): takht with cushions, TV, side table, lamp, door
    B.box((11.0,2.2,.35),(1.8,.7,.35),M('#6E4A2E',.5,kind='wood'),.03); B.box((11.0,2.2,.75),(1.75,.65,.06),M('#C8372D',.8,kind='fabric'),.03)
    for x in (9.8,11.0,12.2): B.box((x,2.75,1.05),(.45,.15,.3),M(random.Random(int(x*10)).choice(['#E8C547','#2E6B4F','#F4E2B0']),.8,kind='fabric'),.08)
    B.box((14.6,-1.0,.5),(.35,1.0,.5),M('#3A2E28',.5,kind='wood'),.02); B.box((14.5,-1.0,1.35),(.04,.9,.5),M('#101218',.2),.01); B.box((14.45,-1.0,1.35),(.01,.85,.45),M('#1E3A6A',.2,emit=.5),0)
    B.box((13.2,2.4,.35),(.3,.3,.35),M('#6E4A2E',.5,kind='wood'),.02); B.cyl((13.2,2.4,.9),.16,.5,M('#F4E2B0',.4,emit=2.2),seg=14,r2=.1); point((13.2,2.2,1.2),70,(1,.8,.55),r=.2)
    frame(11.0,2.86,2.4,.9,.5,'#1E4D38'); stext('ALLAH',(11.0,2.83,2.4),.18,'#E8C547')
    B.box((16.4,1.2,1.3),(.04,.7,1.3),M('#5E3A22',.5,kind='wood'),.02)
    B.box((8.0,-.5,.02),(1.6,1.2,.01),M('#8A2E3A',.9,kind='fabric'),0)
    B.done('home')
ABBU_BED=(1.2,1.6); DADI_SEAT=(11.0,2.0)
def lane_fg():
    """night lane: Chacha's green door (x=-6), Waleed's own gate (x=0); Phuppo's blue gate far down the road (x=+40)."""
    road=M('#4E4F54',.85,kind='asphalt',sc=.6); G=2.8
    B.box((15,-3,-.05),(45,7,.05),road,0); B.box((15,G-.8,.06),(45,.8,.06),M('#B0A898',.85,kind='concrete',sc=.8),.01)
    cols=['#D8C8A8','#C9DCE4','#E8D6C0','#D4E0C8','#E8C8B8','#C8C0D8']
    for i,cx in enumerate(range(-20,60,8)):
        if 36<=cx<=44: continue
        c=cols[i%len(cols)]; B.box((cx,G+2.5,2.8),(3.8,2.5,2.8),M(c,.85,kind='wall'),0); B.box((cx,G+2.5,5.65),(3.9,2.6,.08),M(shade(c,.8),.8),0)
        for x in (cx-2,cx+2): B.box((x,G-.02,3.9),(.6,.03,.5),M('#FFD98A' if (i+int(x))%3 else '#2A3A5A',.2,emit=1.6 if (i+int(x))%3 else 0),0)
    # Chacha's door
    B.box((-6,G-.03,1.15),(.65,.04,1.15),M('#2E6B4F',.5,kind='wood'),.02); B.box((-6.5,G-.08,1.15),(.04,.03,.12),M('#C9A24A',.3,metal=.8),.01)
    B.box((-6,G-.1,2.6),(.18,.1,.08),M('#FFE6B0',.2,emit=5),.01); point((-6,G-.5,2.5),55,(1,.85,.6),r=.12)
    # Waleed's gate
    B.box((0,G-.03,1.2),(1.0,.04,1.2),M('#2A2C34',.35,metal=.6),.01)
    # Phuppo's house at x=40: cream bungalow, blue gate, nameplate, bell, bougainvillea
    P=40
    B.box((P,G+3.0,3.0),(4.5,3.0,3.0),M('#F2E6C8',.85,kind='wall'),0); B.box((P,G+3.0,6.1),(4.7,3.2,.12),M('#C9B08A',.8),0)
    B.box((P,G+.12,1.2),(4.5,.15,1.2),M('#F2E6C8',.85,kind='wall'),0)
    B.box((P,G-.05,1.3),(1.1,.05,1.25),M('#2E5A9A',.4,metal=.5),.01)
    B.box((P+1.65,G-.05,1.95),(.4,.02,.18),M('#F4F1EA',.3),.01); stext('NASREEN VILLA',(P+1.65,G-.07,1.95),.075,'#2E5A9A')
    B.box((P+1.4,G-.06,1.45),(.08,.04,.1),M('#C9CED8',.4),.01); B.box((P+1.4,G-.09,1.45),(.03,.01,.03),M('#C8372D',.4,emit=1.5),0)
    B.box((P-1.45,G-.1,2.7),(.15,.1,.08),M('#FFE6B0',.2,emit=5),.01); point((P-1.45,G-.5,2.6),60,(1,.85,.6),r=.12)
    for k in range(7): B.ico((P-3.8+k*1.2,G+.25,2.55+random.Random(k).uniform(0,.3)),.38,M(random.Random(k+3).choice(['#D9367A','#E8559A','#C2306A']),.85,kind='leaves'),sub=1,sc=(1.2,.8,.7))
    for x in (-14,-2,12,26,52):
        B.cyl((x,G-1.5,3.0),.08,6.0,M('#5A5E66',.4,metal=.6),seg=8); B.box((x+.45,G-1.5,5.9),(.5,.08,.05),M('#5A5E66',.4,metal=.6),.01)
        B.box((x+.85,G-1.5,5.82),(.18,.1,.04),M('#FFE6B0',.2,emit=6),.01); point((x+.85,G-1.7,5.5),700,(1,.82,.55),r=.3)
    for i in range(3):
        y=G-1.4+i*.02; z=5.3-i*.12; B.cyl((15,y,z),.012,90,M('#16171C',.6),seg=6,rot=(0,R(90),0))
    B.box((15,-10,1.4),(45,.2,1.4),M('#CFC6B4',.85,kind='wall'),0)
    for x in (-10,5,22,34,48): tree(x,-9.2,1.0)
    car((-12,G-2.6,0),0,'#8A9098',seed=5); car((22,G-2.6,0),0,'#C8372D',seed=6)
    B.done('lane')
CHACHA_DOOR=(-6,2.8); PHUPPO_GATE=(40,2.8)
def phuppo_in():
    """Phuppo's drawing room: floral sofa, coffee table, showcase, wall clock, curtains (placed at x=100)."""
    X=100; Ht=3.6
    B.box((X,0,-.05),(6,4,.05),M('#E0D2BC',.5,kind='tile',sc=1.6,h2='#D2C2A8'),0); B.box((X,0,Ht+.05),(6,4,.05),M('#F4F1EA',.9),0)
    B.box((X,2.6,Ht/2),(6,.1,Ht/2),M('#E8C8C8',.9,kind='wall'),0)
    for x in (X-6,X+6): B.box((x,0,Ht/2),(.1,4,Ht/2),M('#E8D8D0',.9,kind='wall'),0)
    fab=M('#9A3A5A',.85,kind='fabric')
    B.box((X,1.9,.4),(1.7,.55,.4),fab,.06); B.box((X,2.35,.95),(1.7,.15,.45),fab,.06)
    for sx in (-1,1): B.box((X+sx*1.65,1.9,.65),(.15,.55,.25),fab,.05)
    for x in (X-.9,X,X+.9): B.box((x,2.15,.95),(.35,.1,.28),M('#E8C547',.8,kind='fabric'),.08)
    B.box((X,.7,.42),(.85,.5,.04),M('#C9CED8',.1,alpha=.5),.01); B.box((X,.7,.2),(.75,.4,.2),M('#6E4A2E',.5,kind='wood'),.02)
    B.box((X+3.6,2.25,1.4),(1.0,.3,1.4),M('#6E4A2E',.5,kind='wood'),.02)
    for z in (1.0,1.6,2.2):
        B.box((X+3.6,2.0,z),(.9,.02,.25),M('#BFE3F2',.05,alpha=.35),0)
        for k in range(5): B.cyl((X+3.0+k*.3,2.2,z),.08,.04,M('#F4F1EA',.25),seg=14,rot=(R(80),0,0))
    B.cyl((X-3.2,2.48,2.6),.3,.05,M('#C9A24A',.3,metal=.8),seg=24,rot=(R(90),0,0)); B.cyl((X-3.2,2.45,2.6),.25,.03,M('#F4F1EA',.4),seg=24,rot=(R(90),0,0))
    for x in (X-5.1,X-3.9): B.box((x,2.45,2.0),(.55,.08,1.6),M('#D9B24A',.9,kind='fabric'),.04)
    B.box((X-4.5,2.48,2.0),(.6,.02,1.0),M('#1E2A4A',.1,emit=.3),0)
    B.ico((X,.5,Ht-.25),.12,M('#FFF2D8',.2,emit=5),sub=2); point((X,.5,Ht-.5),180,(1,.92,.8),r=.3)
    B.box((X,-.6,.02),(1.8,1.2,.01),M('#2E4A8A',.9,kind='fabric'),0)
    B.done('phuppo_in')
PH_X=100
