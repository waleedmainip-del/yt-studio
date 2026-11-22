
# ---------------------------------------------------------------- Rishtay Wali Aunty worlds
def frame_pic(x,y,z,w,h,col,face_dir=(0,-1,0),border='#C9A24A'):
    if face_dir[1]!=0:
        B.box((x,y,z),(w/2+.04,.02,h/2+.04),M(border,.4,metal=.5),.01); B.box((x,y-.015*face_dir[1]*-1,z),(w/2,.01,h/2),M(col,.6),0)
    else:
        B.box((x,y,z),(.02,w/2+.04,h/2+.04),M(border,.4,metal=.5),.01); B.box((x+.015*face_dir[0],y,z),(.01,w/2,h/2),M(col,.6),0)
def curtain(x,y,z,w,h,col,col2):
    for k in range(int(w/.18)):
        B.box((x-w/2+.09+k*.18,y,z),(.08,.05+.03*(k%2),h/2),M(col if k%3 else col2,.9,kind='fabric'),.03)
def colony(seed=5,x0=-30,x1=30,hero=True,cars=True):
    """residential lane: road along x at y=0 (width 6), house facades at y=+-5.5 with gates and boundary walls"""
    r=random.Random(seed); ROAD=M('#4A4C52',.9,kind='asphalt'); SW=M('#B8B0A0',.85,kind='concrete',sc=.7)
    B.box(((x0+x1)/2,0,-.05),((x1-x0)/2+10,30,.05),M('#8C8676',.9,kind='concrete'),0)
    B.box(((x0+x1)/2,0,.002),((x1-x0)/2,3.0,.002),ROAD,0)
    for s in (-1,1): B.box(((x0+x1)/2,s*3.6,.09),((x1-x0)/2,.6,.09),SW,.01); B.box(((x0+x1)/2,s*3.0,.1),((x1-x0)/2,.06,.1),M('#D8D2C4',.8),.01)
    PAL=['#F2E6D0','#E8D8C0','#D8E4E8','#F0D8C8','#E4E8D0','#F4ECE0','#D8C8B8','#E8E0F0']
    for s in (-1,1):
        x=x0
        while x<x1:
            w=r.uniform(7.0,9.5)
            if s==1 and hero and x<4.5 and x+w>-4.5:
                if x<-4.5-2.5: w=-4.5-x
                else: x=4.5; continue
            cx=x+w/2; col=r.choice(PAL); WL=M(col,.85,kind='wall'); fl=r.choice((2,2,3))
            yb=s*(5.4+3.5)
            # house block set back behind boundary wall
            B.box((cx,s*8.2,fl*1.6),(w/2-.15,3.0,fl*1.6),WL,.02)
            for f in range(fl):
                z=1.6+f*3.2
                for k in range(2):
                    wx=cx-w/4+k*w/2; B.box((wx,s*5.18,z),(.75,.04,.65),M('#2A3440',.08,spec=.9),.01); B.box((wx,s*5.17,z),(.82,.02,.72),M('#F4F1EA',.6),.0)
                    B.box((wx,s*5.12,z-.72),(.9,.12,.04),M('#C8C0B0',.7),.01)
                    if r.random()<.5: B.box((wx,s*5.05,z+.85),(.95,.25,.03),M(r.choice(('#2E6E9E','#C9452E','#2E7D5A','#8A5A2A')),.5),.01)
                if f>0 and r.random()<.6:
                    B.box((cx,s*5.0,z-1.55),(w/2-.5,.4,.06),M('#D8D2C4',.8),.01)
                    for k in range(7): B.box((cx-w/2+.8+k*(w-1.6)/6,s*4.65,z-1.25),(.03,.03,.3),M('#3A3A40',.4,metal=.6),0)
            B.box((cx,s*5.2,fl*3.2+.25),(w/2-.15,.1,.25),M(shade(col,.85),.85,kind='wall'),.01)
            # boundary wall + gate
            gx=cx+r.uniform(-1.5,1.5)
            for a_,b_ in ((x+.1,gx-1.3),(gx+1.3,x+w-.1)):
                if b_>a_: B.box(((a_+b_)/2,s*4.4,.9),((b_-a_)/2,.12,.9),M(shade(col,.9),.85,kind='wall'),.02); B.box(((a_+b_)/2,s*4.4,1.84),((b_-a_)/2+.02,.16,.05),M('#B8B0A0',.8),.01)
            GC=r.choice(('#2B2F3A','#5A3A22','#2E5A4A','#4A2A2E'))
            for k in range(2): B.box((gx-.62+k*1.24,s*4.42,.95),(.6,.04,.9),M(GC,.4,metal=.5),.01)
            for k in range(10): B.box((gx-1.15+k*.255,s*4.38,1.0),(.015,.02,.8),M(shade(GC,1.4),.4,metal=.6),0)
            B.box((gx,s*4.38,2.05),(1.3,.05,.18),M(GC,.4,metal=.5),.01)
            text(r.choice(('House 12','Plot 7','Villa 3','No. 21','House 45','Plot 9')),(gx+1.9,s*4.27,1.55),(0,-s,0),.09,M('#2B2C33',.5),ex=.003)
            if r.random()<.6: tree(x+r.uniform(.6,w-.6),s*4.9,1.8,r.uniform(.8,1.1),r.randint(0,999))
            if cars and s==1 and r.random()<.5: car(cx+r.uniform(-2,2),s*2.25,r.choice(('#C9CDD6','#F4F1EA','#2B2C33','#9E3B4E','#3E5A7A')),0 if r.random()<.5 else 180)
            x+=w
    if hero:
        WL=M('#F0E4CC',.85,kind='wall'); B.box((0,8.2,3.2),(4.45,3.0,3.2),WL,.02)
        for f in range(2):
            z=1.6+f*3.2
            for k in (-1,1): B.box((k*2.2,5.18,z),(.75,.04,.65),M('#2A3440',.08,spec=.9),.01); B.box((k*2.2,5.17,z),(.82,.02,.72),M('#F4F1EA',.6),0); B.box((k*2.2,5.05,z+.85),(.95,.25,.03),M('#2E7D5A',.5),.01)
        B.box((0,5.2,6.65),(4.45,.1,.25),M('#E0D0B4',.85,kind='wall'),.01)
        for a_,b_ in ((-4.5,-1.3),(1.3,4.5)): B.box(((a_+b_)/2,4.4,.9),((b_-a_)/2,.12,.9),M('#E8D8BC',.85,kind='wall'),.02); B.box(((a_+b_)/2,4.4,1.84),((b_-a_)/2+.02,.16,.05),M('#B8B0A0',.8),.01)
        for k in range(2): B.box((-.62+k*1.24,4.42,.95),(.6,.04,.9),M('#1F3A5A',.4,metal=.5),.01)
        for k in range(10): B.box((-1.15+k*.255,4.38,1.0),(.015,.02,.8),M('#3E5A7A',.4,metal=.6),0)
        B.box((1.75,4.27,1.35),(.06,.02,.09),M('#F4F1EA',.4),.01); B.cyl((1.75,4.25,1.35),.025,.01,M('#C9302C',.4),rot=(R(90),0,0),seg=10)
        B.box((-1.95,4.27,1.5),(.35,.02,.14),M('#2B2C33',.4,metal=.4),.01); text('House 24',(-1.95,4.255,1.5),(0,-1,0),.09,M('#E8C25A',.4),ex=.003)
        tree(3.6,4.9,1.8,1.0,77); tree(-3.6,4.9,1.8,.9,78)
    for x in range(int(x0),int(x1),9):
        B.cyl((x,-3.9,4.5),.09,9,M('#8A8478',.8,kind='concrete'),seg=8); B.box((x+.5,-3.9,8.6),(.6,.05,.05),M('#5A5F66',.5),0)
        B.box((x+1.0,-3.9,8.5),(.18,.1,.06),M('#FFF2D8',.3,emit=.3),.02)
    wires(x0,x1,-3.9,-3.9,8.6,4,seed)
    for k in range(10):
        xx=r.uniform(x0-20,x1+20); yy=r.choice((-1,1))*r.uniform(16,40); h=r.uniform(6,14)
        B.box((xx,yy,h/2),(r.uniform(4,8),r.uniform(3,6),h/2),M(r.choice(PAL),.95,kind='wall'),0)
    B.done('colony')

def drawing_room():
    """Pakistani drawing room. floor x -4..4, y -3.6..3; back wall y=3, left wall x=-4, right wall x=4.
    Door in back wall at x=-2.6 (opening). TV on right wall at (3.92,-.4). Abbu armchair at (2.2,-.4) facing +x.
    Big sofa against left wall at x=-3.3 facing +x, seat center y=.8. Two-seater against back wall x=.6 facing -y."""
    FLR=M('#C8B89A',.45,kind='tile',h2='#B8A888',sc=1.6); WAL=M('#E8DCC4',.85,kind='wall'); WAL2=M('#A8C4B0',.85,kind='wall'); WOOD=M('#5A3420',.5,kind='wood',sc=2)
    B.box((0,0,-.05),(4.2,3.8,.05),FLR,0); B.box((0,0,3.25),(4.2,3.8,.05),M('#F4F1EA',.9),0)
    B.box((-.6,3.05,1.6),(3.4,.05,1.6),WAL,0); B.box((-3.75,3.05,2.85),(.45,.05,.4),WAL,0); B.box((-2.6,3.05,2.85),(.7,.05,.4),WAL,0)
    B.box((-4.05,0,1.6),(.05,3.8,1.6),WAL2,0); B.box((4.05,0,1.6),(.05,3.8,1.6),WAL2,0)
    for s,x in ((1,-4.0),(-1,4.0)): B.box((x,0,.08),(.02,3.8,.08),WOOD,0)
    B.box((0,3.0,.08),(4,.02,.08),WOOD,0)
    # door (open, leaf swung) + passage behind
    B.box((-2.6,3.02,1.2),(.62,.06,1.22),M('#4A2A18',.5,kind='wood'),.02)
    door=obox((-3.18,3.0,1.1),(.04,.55,1.1),M('#6B4026',.45,kind='wood',sc=2),.02)
    B.box((-2.6,4.2,1.6),(1.4,.05,1.6),M('#D8CCB0',.9,kind='wall'),0); B.box((-2.6,3.6,-.02),(1.4,.6,.02),FLR,0)
    # carpet
    B.box((-.3,.6,.012),(2.2,1.6,.012),M('#8E2A3A',.9,kind='fabric'),0); B.box((-.3,.6,.02),(1.95,1.35,.012),M('#C9A24A',.9,kind='fabric'),0); B.box((-.3,.6,.026),(1.7,1.1,.012),M('#7A1E2E',.9,kind='fabric'),0)
    for k in range(6): B.box((-.3,.6,.03),(1.5-k*.22,.05,.01),M('#E8D8B8',.9,kind='fabric'),0)
    # big sofa (left wall)
    SOF=M('#2E5A6E',.85,kind='fabric'); SOF2=M('#24485A',.85,kind='fabric')
    B.box((-3.45,.8,.2),(.45,1.4,.2),SOF2,.06); B.box((-3.42,.8,.44),(.42,1.3,.05),SOF,.05); B.box((-3.8,.8,.85),(.14,1.4,.4),SOF2,.08)
    for sy in (-1,1): B.box((-3.45,.8+sy*1.45,.58),(.45,.12,.3),SOF2,.06)
    for k in range(3): B.box((-3.55,.05+k*.75,.85),(.1,.25,.2),M(('#C9A24A','#E8D8B8','#C9452E')[k],.9,kind='fabric'),.07)
    # two-seater on back wall
    B.box((.6,2.45,.2),(1.0,.45,.2),SOF2,.06); B.box((.6,2.42,.44),(.95,.42,.05),SOF,.05); B.box((.6,2.85,.85),(1.0,.14,.4),SOF2,.08)
    for sx in (-1,1): B.box((.6+sx*1.05,2.45,.58),(.12,.45,.3),SOF2,.06)
    # armchair for Abbu
    AC=M('#7A4A2A',.8,kind='fabric')
    B.box((2.1,-.4,.2),(.42,.45,.2),AC,.06); B.box((2.12,-.4,.44),(.4,.42,.05),M('#8A5A3A',.8,kind='fabric'),.05); B.box((1.75,-.4,.85),(.12,.45,.42),AC,.08)
    for sy in (-1,1): B.box((2.1,-.4+sy*.48,.6),(.42,.1,.28),AC,.06)
    # TV unit right wall
    B.box((3.8,-.4,.35),(.22,1.2,.35),WOOD,.02); B.box((3.97,-.4,1.55),(.04,.95,.55),M('#111216',.2,metal=.3),.02)
    tvs=obox((3.92,-.4,1.55),(.005,.9,.5),M('#2E9E4A',.5,emit=1.2),0)
    for k in range(4): B.box((3.8,-1.2+k*.5,.75),(.18,.12,.05),M(('#C9A24A','#2E86C1','#C9452E','#F4F1EA')[k],.4),.02)
    B.cyl((3.7,.6,.78),.06,.12,M('#2B2C33',.5),seg=10)
    # center table with tea set
    B.box((-1.6,.8,.42),(.5,.75,.03),M('#C8D8E8',.05,spec=1.0,alpha=.5),.01); B.box((-1.6,.8,.2),(.45,.7,.02),WOOD,.01)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((-1.6+sx*.42,.8+sy*.68,.21),.025,.42,M('#C9A24A',.3,metal=.8),seg=8)
    B.box((-1.6,.8,.46),(.28,.2,.015),M('#C9CDD6',.25,metal=.85),.01)
    for k in range(3): B.cyl((-1.75+k*.15,.75,.5),.035,.06,M('#F4F1EA',.3),seg=10)
    B.cyl((-1.55,.95,.52),.07,.12,M('#F4F1EA',.3),seg=12); B.cyl((-1.3,.55,.47),.12,.015,M('#F4F1EA',.3),seg=16)
    for k in range(5): B.cyl((-1.36+k*.03,.55,.49),.03,.01,M('#C98A3A',.6),seg=8)
    # showcase cabinet back wall right
    B.box((2.9,2.75,1.0),(.75,.22,1.0),WOOD,.02); B.box((2.9,2.53,1.25),(.7,.01,.65),M('#C8D8E8',.05,spec=1.0,alpha=.35),0)
    for z in (.85,1.35,1.8):
        B.box((2.9,2.7,z-.05),(.68,.18,.015),M('#E8E0D0',.5),0)
        for k in range(5): B.cyl((2.35+k*.28,2.72,z+.1),.1,.02,M(('#F4F1EA','#C9A24A','#2E86C1')[k%3],.3),rot=(R(80),0,0),seg=14)
    # window with curtains (back wall left of two-seater)
    B.box((-1.1,3.02,1.75),(.7,.02,.75),M('#BFE0F5',.05,emit=2.2),0); B.box((-1.1,3.0,1.75),(.75,.03,.8),M('#F4F1EA',.5),.01)
    for k in range(3): B.box((-1.1,2.99,1.25+k*.5),(.72,.02,.015),M('#3A3A40',.4,metal=.6),0)
    curtain(-1.95,2.9,1.65,.5,2.2,'#C9452E','#A83A28'); curtain(-.25,2.9,1.65,.5,2.2,'#C9452E','#A83A28'); B.box((-1.1,2.92,2.8),(1.2,.03,.03),M('#C9A24A',.3,metal=.8),0)
    # wall decor: calligraphy frame, clock, family photo, AC
    frame_pic(.6,3.0,2.05,1.0,.45,'#1E4A3A'); text('بسم اللہ',(.6,2.975,2.03),(0,-1,0),.12,M('#E8C25A',.3,metal=.6),ex=.003) if False else B.box((.6,2.975,2.05),(.38,.005,.04),M('#E8C25A',.3,metal=.6),0)
    B.cyl((-4.0,-1.4,2.3),.25,.04,M('#F4F1EA',.4),rot=(0,R(90),0),seg=24); B.cyl((-3.98,-1.4,2.3),.27,.03,M('#5A3420',.5),rot=(0,R(90),0),seg=24)
    B.box((-3.97,-1.4,2.36),(.01,.01,.13),M('#1E1A18',.5),0); B.box((-3.97,-1.34,2.3),(.01,.08,.01),M('#1E1A18',.5),0)
    frame_pic(-4.0,1.2,2.2,.8,.55,'#D8A878',face_dir=(1,0,0)); frame_pic(-4.0,2.3,2.25,.45,.6,'#8AA8C8',face_dir=(1,0,0))
    B.box((1.0,-3.6,2.7),(.6,.12,.18),M('#F4F1EA',.4),.04)
    B.box((3.98,1.6,2.6),(.1,.5,.16),M('#F4F1EA',.4),.04)
    # plant + side lamp
    B.cyl((3.6,2.6,.25),.2,.5,M('#C98A5A',.7,kind='concrete'),seg=14)
    for k in range(7): B.cyl((3.6+.15*math.cos(k),2.6+.15*math.sin(k),.8),.12,.6,M('#3E7A3A',.7),rot=(R(20*math.cos(k*2)),R(20*math.sin(k*2)),0),seg=6)
    B.cyl((-3.6,2.6,.3),.18,.6,WOOD,seg=10); B.cyl((-3.6,2.6,.95),.06,.7,M('#C9A24A',.3,metal=.7),seg=8); B.cyl((-3.6,2.6,1.4),.25,.3,M('#F4E8C8',.6,emit=.6),seg=14,r2=.15)
    B.done('room'); return dict(door=door,tv=tvs)

def bedroom():
    """Hamza's bedroom: floor x -3..3, y -3..2.7, back wall y=2.7. bed head at back wall, bed x -.7..1.1 (center .2), y -.2..2.6, mattress top z=.55"""
    FLR=M('#B89A78',.5,kind='wood',sc=2.5); WAL=M('#8FB0C8',.85,kind='wall'); WAL2=M('#E8E2D4',.85,kind='wall'); WOOD=M('#4A2E1E',.5,kind='wood',sc=2)
    B.box((0,0,-.05),(3.2,3.2,.05),FLR,0); B.box((0,2.75,1.5),(3.2,.05,1.5),WAL,0); B.box((-3.05,0,1.5),(.05,3.2,1.5),WAL2,0); B.box((3.05,0,1.5),(.05,3.2,1.5),WAL2,0); B.box((0,0,3.05),(3.2,3.2,.05),M('#F4F1EA',.9),0)
    # bed
    B.box((.2,1.2,.22),(.95,1.45,.12),WOOD,.03); B.box((.2,2.62,.75),(1.0,.08,.65),WOOD,.04); B.box((.2,-.25,.35),(1.0,.06,.25),WOOD,.03)
    B.box((.2,1.2,.45),(.9,1.38,.12),M('#F4F1EA',.8,kind='fabric'),.05)
    B.box((.2,2.25,.62),(.65,.22,.09),M('#F4F1EA',.8,kind='fabric'),.07)
    # posters, cricket bat, study table with laptop, cupboard, window
    B.box((-1.6,2.72,1.9),(.42,.01,.58),M('#1F3A5A',.5),0); B.box((-1.6,2.71,2.1),(.3,.005,.18),M('#E8C25A',.4),0); B.box((-1.6,2.71,1.7),(.2,.005,.2),M('#C9452E',.4),0)
    B.box((1.9,2.72,2.0),(.35,.01,.45),M('#2E7D5A',.5),0); B.cyl((1.9,2.71,2.0),.2,.01,M('#F4F1EA',.5),rot=(R(90),0,0),seg=18)
    B.box((2.6,2.6,.55),(.05,.03,.5),M('#D8B880',.5,kind='wood'),.01,rot=(R(-8),0,0)); B.box((2.6,2.62,1.15),(.02,.02,.12),M('#2B2C33',.6),0)
    B.box((-2.4,1.5,.75),(.55,.35,.03),WOOD,.01)
    for sx in (-1,1):
        for sy in (-1,1): B.box((-2.4+sx*.5,1.5+sy*.3,.37),(.03,.03,.37),WOOD,0)
    B.box((-2.4,1.5,.79),(.28,.2,.01),M('#2B2C33',.3,metal=.5),.005); B.box((-2.4,1.68,.95),(.28,.01,.18),M('#2B2C33',.3,metal=.5),.005,rot=(R(-10),0,0))
    B.box((-2.4,1.67,.95),(.25,.005,.15),M('#7FD3FF',.3,emit=.5),0,rot=(R(-10),0,0))
    for k in range(3): B.box((-2.75+k*.12,1.35,.86),(.04,.12,.06),M(('#C9452E','#2E86C1','#E8C25A')[k],.5),.01)
    B.box((-3.0,-1.2,1.1),(.3,.9,1.1),M('#D8C8A8',.5,kind='wood'),.02); B.box((-2.7,-1.2,1.1),(.005,.01,1.0),M('#5A3420',.5),0)
    B.box((3.02,-1.7,1.15),(.03,.55,1.15),M('#3A3026',.9),0); B.box((3.0,-1.7,2.35),(.05,.62,.06),M('#4A2E1E',.5,kind='wood'),.01)
    for sy in (-1,1): B.box((3.0,-1.7+sy*.6,1.15),(.05,.05,1.2),M('#4A2E1E',.5,kind='wood'),.01)
    bdoor=obox((2.5,-2.28,1.1),(.5,.04,1.1),M('#6B4026',.45,kind='wood',sc=2),.02)
    B.box((3.03,.4,1.75),(.02,.8,.65),M('#FFE6B8',.1,emit=3.0),0); curtain(2.98,.4,1.75,.01,1.6,'#E8C25A','#D8B048') if False else None
    for sy in (-1,1): B.box((2.95,.4+sy*.75,1.7),(.05,.22,.95),M('#2E6E9E',.9,kind='fabric'),.03)
    B.box((.2,0.3,.012),(1.6,.8,.01),M('#5A6B8A',.9,kind='fabric'),0)
    for k in range(4): B.box((-1.0+k*.3,-1.0,.05),(.12,.07,.05),M(('#F4F1EA','#2B2C33','#C9452E','#3E5A7A')[k],.8,kind='fabric'),.03,rot=(0,0,R(30*k)))
    B.box((1.6,2.4,.3),(.25,.22,.3),WOOD,.02); B.cyl((1.6,2.4,.68),.08,.08,M('#F4F1EA',.4),seg=12); B.box((1.75,2.35,.62),(.05,.09,.01),M('#2B2C33',.3),0)
    B.box((0,2.73,2.75),(.3,.02,.1),M('#F4F1EA',.4),.03)
    B.done('bed')
    blanket=obox((0,0,0),(.88,.75,.1),M('#C9452E',.9,kind='fabric'),.06)
    return dict(blanket=blanket,door=bdoor)

def rooftop():
    """Bilal's rooftop at dusk: roof slab z=0, x -4..4, y -3..3; parapet; water tanks; charpai at (0,.6) seat .45; laundry line"""
    SL=M('#B8AC98',.9,kind='concrete',sc=.6); PW=M('#D8C8B0',.85,kind='wall')
    B.box((0,0,-.1),(6,5,.1),SL,0)
    for s in (-1,1): B.box((s*6,0,.5),(.12,5,.5),PW,.02); B.box((0,s*5,.5),(6,.12,.5),PW,.02)
    for k,x in enumerate((-3.6,-2.6)): B.cyl((x,3.8,.6),.45,1.2,M(('#2B2C33','#3E7AB8')[k],.5),seg=20); B.cyl((x,3.8,1.25),.47,.08,M('#1E1E22',.5),seg=20)
    B.box((3.5,3.6,1.1),(1.2,.9,1.1),PW,.02); B.box((3.5,2.68,.95),(.45,.03,.95),M('#5A3A22',.5,kind='wood'),.01)
    W=M('#6B4026',.6,kind='wood')
    B.box((0,.6,.4),(1.0,.5,.05),W,.02)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((sx*.95,.6+sy*.45,.2),.05,.4,W,seg=8)
    for k in range(9): B.box((0,.2+k*.1,.44),(.95,.015,.01),M('#E8D8B0',.9),0)
    for k in range(9): B.box((-.85+k*.21,.6,.445),(.015,.45,.01),M('#D8C8A0',.9),0)
    B.box((-1.6,-.2,.25),(.25,.25,.25),M('#2E6E9E',.5),.04)
    B.box((-4.5,-2.5,1.8),(.02,.02,1.8),M('#5A5F66',.4,metal=.6),0); B.box((4.5,-2.5,1.8),(.02,.02,1.8),M('#5A5F66',.4,metal=.6),0); B.box((0,-2.5,3.55),(4.5,.008,.008),M('#2B2C33',.5),0)
    r=random.Random(3)
    for k in range(7): B.box((-3.6+k*1.1,-2.5,3.2),(.3,.01,.35),M(r.choice(('#C9452E','#2E86C1','#F4F1EA','#E8C25A','#2E7D5A')),.9,kind='fabric'),0)
    for k in range(14):
        xx=r.uniform(-30,30); yy=r.uniform(8,40)*r.choice((-1,1)); h=r.uniform(4,12)
        if abs(xx)<9 and abs(yy)<9: continue
        B.box((xx,yy,h/2-3.2),(r.uniform(3,6),r.uniform(3,6),h/2),M(r.choice(('#E8D8C0','#D8C8B8','#F0E0D0','#C8B8A8')),.95,kind='wall'),0)
        B.box((xx,yy,h-3.2+.4),(r.uniform(2.5,5),.1,.4),M('#C8B8A8',.9),0)
    for k in range(6): B.cyl((r.uniform(-25,25),r.uniform(12,35),5),.08,10,M('#5A5F66',.5),seg=6)
    B.done('roof')

def clinic():
    """the doctor's study, seen as a video call: desk at y=.6 (top z=.78), she sits behind at (0,1.3) facing -y; back wall y=2.4"""
    WAL=M('#E8EEF0',.85,kind='wall'); WOOD=M('#7A5A3A',.5,kind='wood',sc=2)
    B.box((0,0,-.05),(3,3,.05),M('#C8C0B4',.5,kind='tile',sc=1.5),0); B.box((0,2.45,1.5),(3,.05,1.5),WAL,0); B.box((-2.5,0,1.5),(.05,3,1.5),WAL,0); B.box((2.5,0,1.5),(.05,3,1.5),WAL,0)
    B.box((0,.6,.76),(.8,.4,.03),WOOD,.01); B.box((0,.95,.38),(.78,.04,.38),WOOD,.01)
    B.box((-1.3,2.25,1.2),(.7,.18,1.2),WOOD,.02); r=random.Random(9)
    for z in (.5,1.0,1.5,2.0):
        B.box((-1.3,2.2,z-.03),(.66,.16,.015),WOOD,0); x=-1.9
        while x<-.7:
            w=r.uniform(.05,.1); h=r.uniform(.25,.38); B.box((x+w/2,2.2,z+h/2),(w/2-.005,.12,h/2),M(r.choice(('#2E5A8A','#8E2A3A','#2E7D5A','#E8DCC0','#5A3A6A','#C9A24A')),.5),.005); x+=w+.01
    for k in range(3): frame_pic(.55+k*.6,2.42,1.95,.42,.3,'#F4F1EA',border='#2B2C33'); B.box((.55+k*.6,2.4,1.95),(.15,.003,.06),M('#2E5A8A',.5),0)
    B.box((1.4,2.2,.5),(.3,.2,.5),WOOD,.02); B.cyl((1.4,2.2,1.12),.12,.25,M('#C98A5A',.7),seg=12)
    for k in range(6): B.cyl((1.4+.08*math.cos(k),2.2+.08*math.sin(k),1.4),.08,.4,M('#3E7A3A',.7),rot=(R(18*math.cos(k*2)),R(18*math.sin(k*2)),0),seg=6)
    B.box((.45,.55,.81),(.18,.13,.015),M('#F4F1EA',.5),.005); B.cyl((-.45,.6,.84),.04,.1,M('#F4F1EA',.3),seg=10)
    B.cyl((-.2,.5,.8),.08,.01,M('#2B2C33',.3,metal=.6),rot=(0,0,0),seg=16)
    B.box((0,2.43,2.6),(.5,.01,.2),M('#E8C25A',.4),0)
    B.done('clinic')

# ================================================================ MEHNDI NIGHT worlds
def sign(body,loc,n,w,h,fg='#FFE9A8',bg=None,emit=0.0,ex=.012,border=None):
    """readable sign: optional backing plate, text fitted to (w,h) and pushed in front of the surface along n"""
    nv=Vector(n).normalized(); L_=Vector(loc)
    if bg: B.box(tuple(L_),(w/2 if abs(nv.y)>.5 else .015, .015 if abs(nv.y)>.5 else w/2, h/2),M(bg,.6),.005)
    if border: B.box(tuple(L_-nv*.005),(w/2+.04 if abs(nv.y)>.5 else .012, .012 if abs(nv.y)>.5 else w/2+.04, h/2+.04),M(border,.3,metal=.6),.005)
    t=text(body,tuple(L_+nv*(.03+ex)),n,1.0,M(fg,.35,emit=emit),ex=ex); bpy.context.view_layer.update()
    dw,dh=t.dimensions.x,t.dimensions.y
    s=min(w*.88/max(dw,1e-3),h*.8/max(dh,1e-3)); t.scale=(s,s,1); return t
def bulbs(a,b,n,sag,col,seed=0,size=.035):
    a=Vector(a); b=Vector(b); r=random.Random(seed); cols=col if isinstance(col,(list,tuple)) and not isinstance(col,str) else [col]
    for i in range(n):
        q=(i+.5)/n; p=a+(b-a)*q; p.z-=sag*4*q*(1-q)
        B.cyl(tuple(p),size,size*1.4,M(r.choice(cols),.3,emit=4.0),rot=(0,0,0),seg=6)
    for i in range(12):
        q0=i/12; q1=(i+1)/12; p0=a+(b-a)*q0; p0.z-=sag*4*q0*(1-q0); p1=a+(b-a)*q1; p1.z-=sag*4*q1*(1-q1); seg(tuple(p0),tuple(p1),.006,M('#2B2C33',.5),4)
def marigold(a,b,n,seed=0):
    a=Vector(a); b=Vector(b); r=random.Random(seed)
    for i in range(n):
        q=i/(n-1); p=a+(b-a)*q; p.z-=.25*4*q*(1-q)
        B.cyl(tuple(p),.07,.1,M(r.choice(('#F28C18','#F2B705','#E86A10')),.85,kind='fabric'),rot=(R(r.uniform(0,90)),0,0),seg=8)
def hanging_strand(x,y,z,l,seed=0):
    r=random.Random(seed)
    for k in range(int(l/.13)): B.cyl((x,y,z-k*.13),.06,.11,M(r.choice(('#F28C18','#F2B705','#E86A10','#C9302C')),.85,kind='fabric'),rot=(0,0,0),seg=8)
def chair_plastic(x,y,rz,col='#C9302C'):
    e=empty((x,y,0),rot=(0,0,R(rz))); m=M(col,.4)
    obox((0,0,.44),(.23,.22,.03),m,.02,e); obox((0,.2,.72),(.23,.03,.26),m,.03,e,rot=(R(-8),0,0))
    for sx in (-1,1):
        for sy in (-1,1): obox((sx*.19,sy*.18,.22),(.025,.025,.22),m,.01,e)
    return e
def sofa_chair(x,y,rz,col='#F4EEDD',trim='#C9A24A'):
    e=empty((x,y,0),rot=(0,0,R(rz)))
    obox((0,0,.22),(.36,.33,.2),M(col,.7,kind='fabric'),.05,e); obox((0,.3,.7),(.36,.06,.38),M(col,.7,kind='fabric'),.06,e)
    for sx in (-1,1): obox((sx*.36,0,.5),(.05,.33,.12),M(trim,.35,metal=.6),.02,e)
    return e
def mehndi_venue(seed=11):
    """night lawn. stage x -4.5..4.5, y 2..6.2, top z=.6. front row sofa chairs at y=-.6 facing +y. DJ booth at (6.3,2.6). lawn extends y -14..9"""
    r=random.Random(seed)
    B.box((0,-3,-.05),(22,16,.05),M('#3E6A2E',.95,kind='grass',sc=.6),0)
    B.box((0,-3,.006),(1.1,12,.006),M('#9E1B2E',.9,kind='fabric'),0)
    for s in (-1,1): B.box((s*1.12,-3,.012),(.05,12,.006),M('#E8C25A',.5),0)
    # stage
    STG=M('#7A1E2E',.8,kind='fabric'); B.box((0,4.1,.3),(4.6,2.1,.3),STG,.02); B.box((0,1.98,.3),(4.6,.02,.3),M('#E8C25A',.4,metal=.6),0)
    for k in range(3): B.box((0,1.75-k*.25,.1+k*.0),(1.0,.13,.1+.1*(2-k)),M('#5A1420',.8,kind='fabric'),.01) if False else None
    B.box((0,1.85,.4),(1.0,.14,.2),M('#5A1420',.8,kind='fabric'),.01); B.box((0,1.6,.2),(1.0,.14,.2),M('#5A1420',.8,kind='fabric'),.01)
    B.box((0,4.1,.605),(4.4,1.95,.005),M('#F4EEDD',.85,kind='fabric'),0)
    for x in range(-4,5,2): B.box((x+.5,4.1,.612),(.5,1.9,.004),M('#E8C25A',.85,kind='fabric'),0)
    # backdrop drapes
    cols=('#F2B705','#E86A10','#C9302C','#2E8B57','#F2B705','#E86A10','#D63384')
    for k in range(19): x=-4.5+k*.5; B.box((x,6.25,2.4),(.24,.06+.04*(k%2),2.0),M(cols[k%len(cols)],.85,kind='fabric'),.05)
    B.box((0,6.35,4.5),(4.8,.1,.15),M('#C9A24A',.3,metal=.7),.02)
    for k in range(12): hanging_strand(-4.4+k*.8,6.1,4.3,1.6+.6*(k%3),seed+k)
    # round frame with title
    B.cyl((0,6.12,3.0),1.25,.08,M('#C9A24A',.3,metal=.75),rot=(R(90),0,0),seg=40); B.cyl((0,6.08,3.0),1.12,.06,M('#5A1420',.7,kind='fabric'),rot=(R(90),0,0),seg=40)
    for k in range(24): a=k/24*2*math.pi; B.cyl((1.2*math.cos(a),6.02,3.0+1.2*math.sin(a)),.07,.1,M(('#F28C18','#F2B705')[k%2],.85),rot=(R(90),0,0),seg=8)
    sign('MEHNDI',(0,6.03,3.25),(0,-1,0),1.9,.55,fg='#FFD34D',emit=1.2); sign('NIGHT',(0,6.03,2.7),(0,-1,0),1.3,.4,fg='#FFFFFF',emit=.8)
    # couple's jhoola-sofa (empty) + bolsters
    B.box((0,5.4,.85),(1.2,.4,.25),M('#E8C25A',.5,kind='fabric'),.06); B.box((0,5.75,1.4),(1.25,.08,.6),M('#C9A24A',.35,metal=.6),.05)
    for s in (-1,1): B.cyl((s*1.0,5.25,1.15),.14,.5,M('#C9302C',.8,kind='fabric'),rot=(0,R(90),0),seg=12)
    for s in (-1,1):
        B.cyl((s*1.35,5.4,2.6),.04,4.0,M('#C9A24A',.35,metal=.7),seg=8)
        for k in range(6): B.cyl((s*1.35,5.4,1.0+k*.6),.09,.12,M('#F2B705',.85),rot=(0,0,0),seg=8)
    # dhol + mehndi thaal on stage
    B.cyl((3.5,5.2,.85),.25,.55,M('#8A2A1E',.5,kind='wood'),rot=(0,R(90),0),seg=18)
    for s in (-1,1): B.cyl((3.5+s*.28,5.2,.85),.26,.03,M('#E8D8B0',.6),rot=(0,R(90),0),seg=18)
    B.cyl((-3.4,5.3,.66),.35,.04,M('#C9A24A',.3,metal=.8),rot=(0,0,0),seg=24)
    for k in range(6): a=k/6*2*math.pi; B.cyl((-3.4+.22*math.cos(a),5.3+.22*math.sin(a),.75),.04,.12,M('#F4EEDD',.4,emit=2.0),rot=(0,0,0),seg=8)
    # pillars + uplights
    for s in (-1,1):
        for y in (2.1,6.1):
            B.cyl((s*4.5,y,2.6),.12,5.2,M('#F4EEDD',.6),seg=12)
            for k in range(14): B.cyl((s*4.5,y-.13,.4+k*.33),.06,.08,M(('#F28C18','#F2B705')[k%2],.85),rot=(0,0,0),seg=8)
    # light canopy over lawn
    for k in range(9):
        y=6.0-k*2.0; bulbs((-9,y,5.2),(9,y,5.2),40,.8,('#FFE9A8','#FFD34D','#FFF2D8'),seed+k)
    for x in (-9,-4.5,0,4.5,9): bulbs((x,6.2,5.4),(x,-12,5.4),44,.6,('#FFE9A8','#FF9F43'),seed+50+int(x))
    for k in range(10): marigold((-4.5+k*.0,2.05,4.9) if False else (-4.5,2.05,5.0),(4.5,2.05,5.0),30,seed+77) if k==0 else None
    # DJ booth stage-right
    B.box((6.3,2.6,.5),(.9,.45,.5),M('#1E1E24',.4),.03); B.box((6.3,2.15,.55),(.88,.01,.42),M('#2B2C33',.3,metal=.5),0)
    sign('DJ ZAIN',(6.3,2.13,.6),(0,-1,0),1.4,.4,fg='#7FD3FF',emit=2.0)
    B.box((6.3,2.7,1.02),(.5,.25,.03),M('#2B2C33',.3,metal=.6),.01)
    for s in (-1,1): B.cyl((6.3+s*.25,2.7,1.06),.1,.02,M('#111216',.3,metal=.6),rot=(0,0,0),seg=18)
    B.box((6.3,2.85,1.2),(.14,.01,.1),M('#9FD8FF',.3,emit=1.5),0,rot=(R(-15),0,0))
    for x in (5.2,7.4):
        B.box((x,2.9,.75),(.35,.35,.75),M('#141418',.5),.02)
        for z in (.45,1.05): B.cyl((x,2.54,z),.22,.03,M('#2B2C33',.6),rot=(R(90),0,0),seg=18); B.cyl((x,2.52,z),.08,.03,M('#5A5F66',.4,metal=.5),rot=(R(90),0,0),seg=12)
    for x in (5.0,7.6): B.cyl((x,3.4,1.5),.04,3.0,M('#2B2C33',.4,metal=.6),seg=8); B.box((x,3.4,3.1),(.12,.12,.15),M('#2B2C33',.4),.02); B.cyl((x,3.28,3.05),.08,.05,M('#C59BFF',.3,emit=6.0),rot=(R(90),0,0),seg=10)
    # front row sofa chairs + rows of plastic chairs
    for x in (-3.0,-2.0,-1.0,1.0,2.0,3.0): sofa_chair(x,-.8,180,('#F4EEDD','#E8C25A','#F4EEDD')[int(x)%3])
    for row,y in enumerate((-2.6,-3.8,-5.0)):
        for x in (-4.2,-3.4,-2.6,-1.8,1.8,2.6,3.4,4.2): chair_plastic(x+r.uniform(-.05,.05),y,180+r.uniform(-8,8),('#C9302C','#F4F1EA','#2E6E9E')[row])
    # round tables at sides
    for (x,y) in ((-8,-2),(-8,-6),(8,-2),(8,-6),(-7.5,2),(9,1)):
        B.cyl((x,y,.38),.7,.76,M('#F4F1EA',.6,kind='fabric'),rot=(0,0,0),seg=24); B.cyl((x,y,.78),.72,.02,M('#E8C25A',.5,kind='fabric'),rot=(0,0,0),seg=24)
        B.cyl((x,y,.86),.12,.14,M('#F28C18',.8),rot=(0,0,0),seg=12)
        for k in range(5): a=k/5*2*math.pi; chair_plastic(x+1.05*math.cos(a),y+1.05*math.sin(a),math.degrees(a)-90,'#F4F1EA')
    # trees with lights around
    for (x,y) in ((-12,-10),(-12,-3),(-12,4),(12,-10),(12,-3),(12,4),(-6,8.5),(6,8.5),(0,9.5)):
        tree(x,y,0,1.3,r.randint(0,999))
        for k in range(5): bulbs((x-1,y-1,1.5+k*.6),(x+1,y+1,1.6+k*.6),10,.2,('#FFE9A8',),k)
    # back walls of the lawn (house + boundary) for depth
    B.box((0,10.5,3.5),(16,.3,3.5),M('#E8D8C0',.9,kind='wall'),0)
    for k in range(7): B.box((-12+k*4,10.18,4.2),(.7,.02,.6),M('#FFE6B8',.3,emit=1.8),0)
    for x in (-16,16): B.box((x,-3,1.5),(.25,14,1.5),M('#D8C8B0',.9,kind='wall'),0)
    B.box((0,-17,1.5),(16,.25,1.5),M('#D8C8B0',.9,kind='wall'),0)
    B.done('venue')

def backstage(seed=12):
    """shamiana tent room behind the stage: floor x -3..3, y -2.5..2.5. back panel y=2.5. opening at x=3 (right) showing venue lights"""
    r=random.Random(seed)
    B.box((0,0,-.05),(3.4,2.9,.05),M('#9E1B2E',.9,kind='fabric'),0); B.box((0,0,.006),(2.6,2.0,.004),M('#C9A24A',.9,kind='fabric'),0)
    for k in range(13):
        x=-3+k*.5; B.box((x,2.55,1.4),(.25,.04,1.4),M(('#F4EEDD','#9E1B2E')[k%2],.9,kind='fabric'),0)
    for k in range(11):
        y=-2.5+k*.5; B.box((-3.05,y,1.4),(.04,.25,1.4),M(('#F4EEDD','#9E1B2E')[k%2],.9,kind='fabric'),0)
    for k in range(5): y=1.0+k*.36; B.box((3.05,y,1.4),(.04,.18,1.4),M(('#F4EEDD','#9E1B2E')[k%2],.9,kind='fabric'),0)
    B.box((0,0,2.85),(3.4,2.9,.05),M('#F4EEDD',.9,kind='fabric'),0)
    for k in range(6): B.box((0,-2.5+k*1.0,2.78),(3.0,.03,.03),M('#C9A24A',.4,metal=.6),0)
    # tube light + fairy lights
    B.box((-1,2.48,2.4),(.6,.03,.03),M('#F4F8FF',.2,emit=6.0),0)
    bulbs((-2.9,2.45,2.6),(2.9,2.45,2.6),26,.3,('#FFE9A8','#FFD34D'),seed)
    # mirror on stand
    B.box((-2.2,2.3,1.3),(.45,.03,.7),M('#C9A24A',.3,metal=.7),.02); B.box((-2.2,2.26,1.3),(.4,.01,.65),M('#C8D8E8',.02,metal=1.0,spec=1.0),0)
    B.box((-2.2,2.3,.3),(.04,.04,.3),M('#3A3A40',.4),0)
    # clothes rack with kurtas
    for s in (-1,1): B.cyl((-2.6,.4+s*.8,.9),.025,1.8,M('#8A8F99',.3,metal=.8),seg=8)
    B.cyl((-2.6,.4,1.8),.025,1.6,M('#8A8F99',.3,metal=.8),rot=(R(90),0,0),seg=8)
    for k,c in enumerate(('#F2C14E','#2E8B57','#E8742A','#F4F1EA','#D63384','#F2B705')): B.box((-2.6,-.2+k*.24,1.35),(.03,.1,.42),M(c,.85,kind='fabric'),.02)
    # soft-drink crates + marigold baskets + plastic chairs
    for k in range(3): B.box((2.3,-1.8+k*.0,.15+k*.3),(.3,.22,.14),M(('#C9302C','#2E6E9E','#C9302C')[k],.5),.02)
    for k in range(6): B.cyl((2.15+k%3*.12,-1.8,1.0+(k//3)*0.0),.03,.16,M('#1E1E22',.2,alpha=.6),rot=(0,0,0),seg=8) if False else None
    for (x,y) in ((1.0,2.0),(1.6,2.0)):
        B.cyl((x,y,.15),.22,.3,M('#8A6A3A',.8,kind='wood'),rot=(0,0,0),seg=14)
        for k in range(8): B.cyl((x+.12*math.cos(k),y+.12*math.sin(k),.33),.06,.08,M(('#F28C18','#F2B705')[k%2],.85),rot=(0,0,0),seg=8)
    chairs=[chair_plastic(-1.2,1.6,15,'#F4F1EA'),chair_plastic(.9,-.2,30,'#C9302C'),chair_plastic(1.6,1.2,-20,'#F4F1EA')]
    # glimpse of venue through opening
    for k in range(20): B.cyl((6+r.uniform(0,6),r.uniform(-3,0),r.uniform(2,4.5)),.05,.07,M('#FFE9A8',.3,emit=5),rot=(0,0,0),seg=6)
    B.box((9,-1,0),(4,4,.02),M('#2E4A24',.9),0)
    B.done('back'); return chairs

def courtyard(seed=13):
    """morning aangan: brick floor x -5..5, y -3..4; back wall y=4 with doors; charpai at (0,.8) seat .45 long axis x"""
    r=random.Random(seed); BR=M('#B0644A',.85,kind='brick',sc=1.2)
    B.box((0,0,-.05),(6,5,.05),BR,0)
    WAL=M('#EEE4D0',.9,kind='wall'); B.box((0,4.05,2.2),(6,.1,2.2),WAL,0); B.box((-6.05,0,2.2),(.1,5,2.2),WAL,0); B.box((6.05,0,2.2),(.1,5,2.2),WAL,0)
    B.box((0,4.0,.35),(6,.06,.35),M('#7A8E9E',.8),0)
    for x in (-3.5,0.0,3.5):
        B.box((x,3.97,1.1),(.6,.04,1.1),M('#3E6E8E',.5,kind='wood'),.02); B.box((x,3.95,1.1),(.02,.02,1.05),M('#2B2C33',.5),0)
        B.box((x,3.94,2.45),(.7,.06,.12),M('#C8B8A0',.8),.01)
    # leftover decorations from mehndi
    for k in range(3): marigold((-5.5,3.9-k*.02,3.6-k*.25),(5.5,3.9,3.6-k*.25),36,seed+k)
    bulbs((-5.8,3.8,3.9),(5.8,3.8,3.9),30,.4,('#E8E0C8',),seed)
    # charpai
    W=M('#6B4026',.6,kind='wood'); B.box((0,.8,.4),(1.05,.5,.05),W,.02)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((sx*1.0,.8+sy*.45,.2),.05,.4,W,rot=(0,0,0),seg=8)
    for k in range(9): B.box((0,.4+k*.1,.44),(1.0,.015,.01),M('#E8D8B0',.9),0)
    # stacked chairs, potted plants, clothes line, tap, tea table
    for k in range(4): chair_plastic(4.6,2.6,180,'#C9302C').location=(4.6,2.6,k*.12)
    for (x,y) in ((-5.3,3.3),(-4.6,3.4),(5.3,-2.5)):
        B.cyl((x,y,.22),.22,.44,M('#B05A3A',.8,kind='concrete'),rot=(0,0,0),seg=12)
        for k in range(6): B.cyl((x+.12*math.cos(k),y+.12*math.sin(k),.6),.1,.45,M('#3E7A3A',.7),rot=(R(15*math.cos(k*2)),R(15*math.sin(k*2)),0),seg=6)
    B.cyl((-5.9,-2.5,1.9),.02,3.8,M('#5A5F66',.5),rot=(R(90),0,0),seg=6) if False else None
    B.box((-1.0,-2.8,2.0),(5,.006,.006),M('#2B2C33',.5),0)
    for k,c in enumerate(('#F2C14E','#2E8B57','#F4F1EA','#E8742A','#9E1B2E')): B.box((-4.5+k*1.6,-2.8,1.65),(.3,.01,.35),M(c,.9,kind='fabric'),0)
    B.box((2.2,.9,.25),(.3,.3,.25),M('#2E6E9E',.5),.03); B.cyl((2.2,.9,.55),.05,.1,M('#F4F1EA',.3),rot=(0,0,0),seg=10)
    # sky/neighbouring roofs
    for k in range(6): B.box((-12+k*5,8,3+r.uniform(0,3)),(2.2,2,3+r.uniform(0,3)),M(r.choice(('#E8D8C0','#D8C8B8','#F0E0D0')),.95,kind='wall'),0)
    B.done('yard')
