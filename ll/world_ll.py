# Sets for "Lahore Lahore Ayy!": Hamza's room (mirror wardrobe, cricket posters) + kitchen, night food street
# with neon signs and a new car, Walled City lane (Delhi Gate style arch, havelis, jharokas), Badshahi-style mosque
# courtyard (red sandstone, white marble domes, minarets).
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
RED=M('#B5503A',.8,kind='wall',h2='#9A4030',sc=1.6); MARB=M('#F2EEE6',.35,spec=.8)
def home_ll():
    fl=M('#B8A890',.4,kind='tile',sc=1.0); wl=M('#7FB08A',.9,kind='wall'); wl2=M('#F0E6CC',.9,kind='wall')
    # bedroom x<0, kitchen x>0 (wall between at x=0 with a door gap)
    B.box((0,0,-.05),(7,3.4,.05),fl,0); B.box((0,0,3.2),(7,3.4,.05),M('#F4F1EA',.9),0)
    B.box((-3.5,3.4,1.6),(3.5,.1,1.6),wl,0); B.box((3.5,3.4,1.6),(3.5,.1,1.6),wl2,0); B.box((-7,0,1.6),(.1,3.4,1.6),wl,0); B.box((7,0,1.6),(.1,3.4,1.6),wl2,0)
    B.box((0,1.9,1.6),(.1,1.5,1.6),wl,0); B.box((0,-2.4,1.6),(.1,1.0,1.6),wl,0); B.box((0,-.5,2.75),(.1,.9,.45),wl,0)
    wd=M('#6A4A2E',.55,kind='wood')
    B.box((-5.3,2.2,.3),(1.2,1.0,.3),wd,.03); B.box((-5.3,2.2,.66),(1.15,.95,.08),M('#E8E2D6',.8,kind='fabric'),.05); B.box((-5.3,2.2,.76),(1.1,.7,.05),M('#C8372D',.9,kind='fabric',h2='#16171C',sc=3),.04)
    # wardrobe with full mirror (facing +x into room)
    B.box((-2.0,3.0,1.2),(.9,.35,1.2),wd,.03); B.box((-2.0,2.63,1.25),(.45,.02,.95),M('#DDE8F0',.02,metal=1.0,spec=1.0),0)
    for k,(x,c,tx) in enumerate(((-6.95,'#2B8A5A','PAKISTAN'),(-6.95,'#16171C','LAHORE QALANDARS?'))): B.box((x,-.8+k*1.4,2.0),(.02,.5,.65),M(c,.6),0); stext(tx,(x+.03,-.8+k*1.4,2.0),.12,'#FFFFFF',n=(1,0,0),e=.3)
    B.box((-3.6,-3.0,.4),(.7,.35,.4),wd,.02); B.box((-3.6,-3.0,.82),(.25,.15,.02),M('#16171C',.4),0)
    # kitchen: counter, stove, fridge, pots
    B.box((4.5,2.9,.45),(2.3,.45,.45),M('#E8E4DA',.4),.02); B.box((4.5,2.9,.92),(2.32,.47,.03),M('#3A3A40',.3,spec=.9),0)
    for x in (3.6,4.3): B.cyl((x,2.85,.98),.18,.06,M('#16171C',.4),seg=14); B.cyl((x,2.85,1.1),.17,.2,M('#C9CED8',.3,metal=.8),seg=14)
    B.box((6.5,2.8,1.0),(.4,.45,1.0),M('#E8E8E4',.35),.04); B.box((5.2,3.32,2.2),(1.4,.08,.4),M('#E8E4DA',.4),.02)
    for k in range(5): B.cyl((4.0+.3*k,3.25,2.6),.08,.12,M(['#C8372D','#F2C14E','#2B8A5A'][k%3],.6),seg=8)
    B.box((0,0,3.14),(.5,.5,.02),M('#FFFFFF',.3,emit=2.2),0); B.box((-4,1.5,3.14),(.5,.5,.02),M('#FFFFFF',.3,emit=2.2),0); B.box((4,1.5,3.14),(.5,.5,.02),M('#FFFFFF',.3,emit=2.2),0)
def keys(e,s=1.0): oico((0,-.08,.04),.025*s,M('#C9CED8',.2,metal=.9),e,sub=1); obox((.03*s,-.08,.0),(.012*s,.004,.05*s),M('#C9CED8',.2,metal=.9),0,e); obox((-.03*s,-.08,.0),(.03*s,.01,.04*s),M('#16171C',.4),.01,e)
# ---------------------------------------------------------------- night food street (MM Alam style)
def night_street(seed=12):
    r=random.Random(seed)
    B.box((0,0,-.05),(40,8,.05),M('#3A3C44',.85,kind='asphalt'),0); B.box((0,-9,-.04),(40,1.0,.05),M('#6A6A70',.8,kind='tile'),0); B.box((0,9,-.04),(40,1.0,.05),M('#6A6A70',.8,kind='tile'),0)
    for x in range(-36,37,4): B.box((x,0,.01),(1.0,.06,.01),M('#F4F1EA',.6),0)
    names=['CAFE AAJ','BBQ TONIGHT','LAHORI CHARGHA','FALOODA','ZINGER POINT','PAN SHOP','CHAI WALA','BURGER LAB']
    for s in (-1,1):
        for i in range(8):
            x=-31+i*8.8; h=r.uniform(7,11); B.box((x,s*13,h/2),(4.2,3.0,h/2),M(r.choice(['#2A2C34','#3A3D47','#4A3D32','#E8D8B0']),.6),0)
            B.box((x,s*10.0,1.5),(3.8,.05,1.3),M('#FFE8B0',.2,emit=1.6,alpha=.7),0)
            c=r.choice(['#FF4F7A','#35C8FF','#F2C14E','#7CFF6B','#FF8A3A']); B.box((x,s*9.95,3.4),(3.0,.08,.4),M('#16171C',.4),.02); stext(names[(i+(s>0)*3)%8],(x,s*9.88,3.4),.4,c,n=(0,-s,0),e=3.0)
            for j in range(int(h/3)): B.box((x+r.uniform(-2.5,2.5),s*9.98,4.6+j*2.6),(.6,.04,.5),M('#FFE8B0',.2,emit=r.choice([0,.8,1.4])),0)
    for x in range(-34,35,8):
        for s in (-1,1): B.cyl((x,s*8.4,3.2),.08,6.4,M('#5A5E66',.3,metal=.7),seg=8); B.box((x,s*7.6,6.3),(.9,.12,.06),M('#5A5E66',.3,metal=.7),0); B.ico((x,s*6.9,6.2),.18,M('#FFE0A0',.3,emit=6),sub=1)
    for k in range(5): car((r.uniform(-30,30),r.choice([-7.2,7.2]),0),r.choice([90,-90]),r.choice(['#C8372D','#F4F1EA','#16171C','#2B5AA8']),seed=k)
    return car((1.5,-1.9,0),90,'#E8E8EC',seed=9)
# ---------------------------------------------------------------- Walled City lane + Delhi-gate style arch
def walled_city(seed=14):
    r=random.Random(seed)
    B.box((0,0,-.05),(40,3.6,.05),M('#A89A88',.85,kind='tile',h2='#958878',sc=2.8),0)
    cols=['#C89A6A','#B8806A','#D8B890','#A8705A','#E0C8A0']
    for s in (-1,1):
        for i in range(9):
            x=-32+i*8; h=r.uniform(7,10); col=r.choice(cols)
            B.box((x,s*5.2,h/2),(3.9,1.6,h/2),M(col,.85,kind='wall',h2=shade(col,.85),sc=2),0)
            for j in range(2):
                z=3.6+j*2.6
                for q in (-1.8,0,1.8):
                    e=x+q; B.box((e,s*3.55,z),(.55,.35,.7),M('#6A4428',.55,kind='wood'),.04); B.box((e,s*3.18,z),(.42,.02,.5),M('#2A3A4A',.2,spec=.7),0)
                    B.box((e,s*3.5,z+.82),(.65,.45,.1),M('#5A3418',.55,kind='wood'),.03)
            B.box((x,s*3.62,1.4),(1.0,.05,1.4),M('#3A2414',.6),0) if r.random()<.5 else None
    # gate arch at the end of the lane
    g=M('#B5503A',.8,kind='wall',h2='#9A4030',sc=1.6)
    for s in (-1,1): B.box((30,s*2.8,4.5),(1.5,1.4,4.5),g,.05); B.cyl((30,s*4.4,5.2),1.0,10.4,g,seg=10); B.ico((30,s*4.4,10.6),1.0,MARB,sub=2)
    B.box((30,0,8.0),(1.5,1.5,1.0),g,.05); B.box((29.0,0,6.6),(.1,1.4,.5),M('#F2EEE6',.5),0); stext('DELHI GATE',(28.85,0,6.6),.35,'#7A1F1F',n=(-1,0,0))
    for k in range(9): a=pi*k/8; B.box((28.6,math.cos(a)*1.4,6.2+math.sin(a)*1.1),(.12,.2,.2),MARB,.02)
    wires(-34,28,-3.4,3.4,5.0,7,seed)
    for x in (-12,6): stall_chai(x,2.6) if 'stall_chai' in globals() else None
# ---------------------------------------------------------------- Badshahi-style mosque courtyard
def badshahi():
    B.box((0,0,-.05),(70,70,.05),M('#C8A888',.85,kind='tile',h2='#B89878',sc=4),0)
    B.box((0,24,.6),(26,4,.6),RED,.05)
    for k in range(-9,10): B.box((k*2.6,21.6,3.4),(1.1,.4,2.0),RED,.04); B.box((k*2.6,21.25,3.3),(.75,.05,1.5),M('#7A2A1E',.6),0)
    B.box((0,24,4.0),(24,3.0,3.0),RED,.05); B.box((0,21.3,6.4),(5.0,.3,6.4),RED,.05); B.box((0,21.05,6.0),(3.6,.05,5.0),M('#7A2A1E',.6),0)
    for k in range(-11,12): B.box((k*2.1,21.2,7.25),(.15,.25,.3),MARB,.02)
    for x,rr in ((0,4.6),(-11,3.4),(11,3.4)): B.cyl((x,25,7.6),rr*.95,1.2,RED,seg=20); B.ico((x,25,8.2+rr*.5),rr,MARB,sc=(1,1,1.12),sub=3); B.cyl((x,25,8.2+rr*1.62),.12,rr*.4,M('#D9B24A',.3,metal=.8),seg=8)
    for (x,y) in ((-26,26),(26,26),(-26,-26),(26,-26)):
        B.cyl((x,y,9.0),1.6,18.0,RED,seg=8)
        for z in (6,12,18): B.cyl((x,y,z),1.9,.3,MARB,seg=8)
        B.cyl((x,y,19.0),1.2,2.0,RED,seg=8)
        for a in range(8): B.cyl((x+math.cos(a*pi/4)*1.1,y+math.sin(a*pi/4)*1.1,20.6),.08,1.2,MARB,seg=6)
        B.ico((x,y,21.8),1.4,MARB,sc=(1,1,1.1),sub=2)
    for s in (-1,1): B.box((s*27,0,2.5),(.8,27,2.5),RED,.05)
    B.box((0,0,.15),(5,5,.15),MARB,.02); B.box((0,0,.32),(4.4,4.4,.02),M('#6AB8E0',.08,spec=1,alpha=.75),0)
    for x in range(-24,25,4): B.box((x,-27,2.5),(1.6,.8,2.5),RED,.05)
