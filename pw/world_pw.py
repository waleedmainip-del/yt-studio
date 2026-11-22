# Sets for "The Peshawari Brother": old-city street with carved wooden door (Hamid's house), hujra guest room
# (floor cushions, carpets, dastarkhwan, niches, brass lamps), Qissa Khwani bazaar (wooden balconies, chappal shop,
# kahwa stall with copper samovar), old Corolla interior (dashboard + fuel meter) and props (food, kahwa, gifts).
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
WOOD=M('#5A3418',.55,kind='wood',sc=.7); WOOD2=M('#7A4A22',.55,kind='wood',sc=.7); BRICK=M('#A8643E',.85,kind='wall',h2='#8E5030',sc=2.2)
RUGS=['#8A1F2A','#2A3A6A','#6A2A1A','#1F4D3A']
def carved_panel(x,y,z,w,h,rot=0,col=WOOD):
    e=empty((x,y,z),rot=(0,0,R(rot))); obox((0,0,0),(w,.06,h),col,.02,e)
    for i in range(3):
        for j in range(4): obox((-w*.6+i*w*.6,-.07,-h*.7+j*h*.47),(w*.22,.02,h*.17),WOOD2,.03,e); oico((-w*.6+i*w*.6,-.1,-h*.7+j*h*.47),.035,M('#C9A24A',.3,metal=.8),e,sub=1)
    return e
def house_street(seed=4):
    r=random.Random(seed)
    B.box((0,0,-.05),(30,8,.05),M('#8E8478',.85,kind='tile',h2='#7A7064',sc=2.5),0)
    for s in (-1,1):
        for k in range(8):
            x=-21+k*6; h=r.uniform(6,9); B.box((x,s*4.0,h/2),(3.0,.5,h/2),BRICK if r.random()<.6 else M(r.choice(['#C9B48A','#E8D8B0','#B8A080']),.85,kind='wall'),0)
            for j in range(2):
                B.box((x+r.uniform(-1.5,1.5),s*3.45,3.9+j*2.3),(.8,.25,.6),WOOD,.03)
                for q in range(5): B.box((x-.6+.3*q,s*3.18,3.9+j*2.3),(.03,.02,.5),WOOD2,0)
    # Hamid's door (north side, x=0)
    B.box((0,3.5,1.6),(1.1,.1,1.6),M('#2A1A0E',.6),0)
    d=empty((-.55,3.42,0)); obox((.55,0,1.4),(.55,.05,1.4),WOOD,.02,d); carved_panel(.55+0,-.06,1.4,.35,.9,0);
    d2=empty((.55,3.42,0)); obox((-.55,0,1.4),(.55,.05,1.4),WOOD,.02,d2)
    for x in (-.25,.25): oico((x,3.32,1.4),.05,M('#C9A24A',.3,metal=.8),sub=1)
    B.box((0,3.35,3.0),(1.3,.18,.12),WOOD2,.03); B.box((0,3.3,3.25),(1.5,.25,.08),M('#D9B24A',.4,metal=.5),.02)
    for x in (-1.6,1.6): B.cyl((x,3.3,2.9),.08,.3,M('#D9B24A',.3,metal=.7),seg=8); B.ico((x,3.3,2.7),.1,M('#FFE8A0',.3,emit=2),sub=1)
    wires(-28,28,-3.5,3.5,5.8,5,seed)
    for x in (-9,8): motorbike((x,-2.6,0),r.choice([0,180]),r.choice(['#C8372D','#16171C']))
    return d,d2
def hujra():
    fl=M('#C8A878',.8,kind='tile',sc=1.5); wl=M('#EFE3C8',.9,kind='wall')
    B.box((0,0,-.05),(4.4,3.6,.05),fl,0); B.box((0,0,3.3),(4.4,3.6,.05),M('#F4EEE0',.9),0)
    B.box((0,3.6,1.65),(4.4,.1,1.65),wl,0); B.box((-4.4,0,1.65),(.1,3.6,1.65),wl,0); B.box((4.4,0,1.65),(.1,3.6,1.65),wl,0)
    for x in (-3.2,-1.1,1.1,3.2): B.box((x,3.52,1.8),(.45,.06,.7),M('#D8C8A8',.8),.0); B.box((x,3.48,2.55),(.5,.05,.06),WOOD2,0); B.cyl((x,3.4,1.5),.1,.25,M('#C9A24A',.3,metal=.8),seg=10,r2=.06)
    for k,(x,y) in enumerate(((-2.2,1.0),(2.2,1.0),(0,-1.2),(0,2.2))): B.box((x,y,.012),(1.9,1.0,.012),M(RUGS[k],.95,kind='fabric',h2='#E8C07A',sc=3),0)
    # floor cushions (toshak) along walls + gol takiye
    for y in (3.1,):
        B.box((0,y,.12),(4.0,.42,.12),M('#7A1F2A',.9,kind='fabric',h2='#D9B24A',sc=5),.06)
        for x in range(-3,4): B.cyl((x*1.1,y+.25,.42),.16,.6,M('#8A2A3A',.9,kind='fabric'),rot=(0,R(90),0),seg=12)
    for x in (-4.0,4.0): B.box((x,1.0,.12),(.42,2.2,.12),M('#7A1F2A',.9,kind='fabric',h2='#D9B24A',sc=5),.06)
    # dastarkhwan (floor cloth) in the middle
    B.box((0,1.2,.02),(1.6,.75,.01),M('#F4EEE0',.8,kind='fabric',h2='#C8372D',sc=8),0)
    B.box((0,3.56,2.9),(.9,.03,.3),M('#2B5A3A',.6),0); stext('KHUSH AAMDEED',(0,3.52,2.9),.2,'#F2C14E',e=.4)
    B.box((0,0,3.24),(.4,.4,.02),M('#FFFFFF',.3,emit=2.2),0)
    B.box((0,-3.6,1.65),(4.4,.1,1.65),wl,0)
def food(kind,loc,s=1.0):
    e=empty(loc)
    if kind=='kebab':
        ocyl((0,0,.02),.3*s,.03,M('#F4F1EA',.4),e,rot=(0,0,0),seg=20)
        for k in range(4): ocyl((-.12*s+.08*s*k,.02*(k%2),.06),.08*s,.025,M('#6A3A1A',.7),e,rot=(0,0,0),seg=10)
    elif kind=='karahi':
        ocyl((0,0,.08*s),.32*s,.16*s,M('#2A2C34',.4,metal=.7),e,rot=(0,0,0),seg=18,r2=.22*s); ocyl((0,0,.15*s),.29*s,.02,M('#C8502A',.6),e,rot=(0,0,0),seg=18)
        for dx in (-1,1): ocyl((dx*.34*s,0,.15*s),.06*s,.02,M('#2A2C34',.4,metal=.7),e,rot=(R(90),0,0),seg=10)
    elif kind=='pulao':
        ocyl((0,0,.02),.42*s,.03,M('#C9A24A',.3,metal=.7),e,rot=(0,0,0),seg=22); oico((0,0,.18*s),.38*s,M('#F2DCA0',.8),e,sc=(1,1,.75),sub=2)
        for k in range(8): a=k*.8; oico((math.cos(a)*.2*s,math.sin(a)*.2*s,.3*s),.03*s,M(['#E8641E','#6A3A1A','#2B8A5A'][k%3],.6),e,sub=1)
    elif kind=='naan':
        for k in range(3): ocyl((0,0,.02+.025*k),.24*s,.02,M('#D9A050',.8),e,rot=(0,0,0),seg=14)
    elif kind=='kahwa':
        ocyl((0,0,.12*s),.1*s,.22*s,M('#C9A24A',.3,metal=.8),e,rot=(0,0,0),seg=12,r2=.06*s); obox((.13*s,0,.15*s),(.06*s,.015,.015),M('#C9A24A',.3,metal=.8),0,e,rot=(0,R(-40),0))
        for dx in (-.25,-.38): ocyl((dx*s,0,.04*s),.045*s,.06*s,M('#F4F1EA',.4),e,rot=(0,0,0),seg=10); ocyl((dx*s,0,.075*s),.04*s,.005,M('#8AB83A',.4),e,rot=(0,0,0),seg=10)
    return e
def gift_bag(e,s=1.0):
    obox((0,-.1,.22*s),(.2*s,.1*s,.22*s),M('#C8372D',.6,kind='fabric'),.02,e); ocyl((0,-.1,.5*s),.01,.25*s,M('#D9B24A',.5),e,rot=(0,R(90),0),seg=5)
    oico((-.08*s,-.1,.45*s),.06*s,M('#8A5A2A',.6),e,sub=1); oico((.06*s,-.1,.47*s),.05*s,M('#D9B24A',.6),e,sub=1); obox((0,-.1,.48*s),(.12*s,.05*s,.04*s),M('#7448C2',.8,kind='fabric'),.02,e)
def wallet(e,s=1.0): obox((0,-.08,.05),(.08*s,.02,.05*s),M('#3A2414',.6),.01,e)
# ---------------------------------------------------------------- Qissa Khwani bazaar
def qk_bazaar(seed=9):
    r=random.Random(seed)
    B.box((0,0,-.05),(40,4,.05),M('#7E7468',.85,kind='tile',h2='#6A6054',sc=3),0)
    cols=['#A8643E','#C9B48A','#8E5030','#B8A080','#D8C8A8']; scols=['#1F4D3A','#7A1F1F','#2B3A7A','#5A3418']
    names_n=['QISSA KHWANI KAHWA','DRY FRUIT HOUSE',None,'KHAN CHAPPAL','PESHAWAR SILVER','CHAPLI KABAB']
    names_s=['NAMAK MANDI TIKKA','BOOK CORNER',None,'SHAWL MAHAL','GOLD SMITH','PAKOL HOUSE']
    xs=[-26,-18,-6.5,6.5,15,23]
    for i,x in enumerate(xs):
        facade(x,6.6,r.randint(2,3),r.choice(cols),names_n[i] or 'TAILOR MASTER',r.choice(scols),seed*10+i,1,Y=3.2,trim='#5A3418')
        facade(x,6.6,r.randint(2,3),r.choice(cols),names_s[i] or 'MOBILE ZONE',r.choice(scols),seed*20+i,-1,Y=3.2,trim='#5A3418')
    facade(0,6.4,3,'#A8643E','KHAN PESHAWARI CHAPPAL','#5A3418',seed*7,1,Y=3.2,trim='#5A3418')
    facade(0,6.4,2,'#C9B48A','QISSA KHWANI KAHWA','#1F4D3A',seed*9,-1,Y=3.2,trim='#5A3418')
    # chappal display racks in front of the chappal shop
    for k in range(3):
        B.box((-2.0+2.0*k,2.6,.6),(.8,.15,.6),WOOD,.02)
        for i in range(4):
            for j in range(3): B.box((-2.5+2.0*k+.28*i,2.48,.25+.38*j),(.11,.08,.05),M(r.choice(['#5A3418','#3A2414','#8A5A2A','#16171C']),.6),.03,rot=(R(70),0,0))
    # kahwa samovar stall in front of the kahwa house
    B.box((.0,-2.5,.45),(1.0,.4,.45),WOOD,.02); B.cyl((0,-2.5,1.3),.3,.8,M('#C8703F',.3,metal=.8),seg=16,r2=.22); B.ico((0,-2.5,1.8),.15,M('#C8703F',.3,metal=.8),sub=1)
    for k in range(6): B.cyl((-.7+.28*k,-2.3,.96),.05,.08,M('#F4F1EA',.4),seg=10)
    B.box((0,-2.9,2.5),(1.2,.05,.5),M('#2B5A3A',.6),0)
    for x in range(-28,29,7): banner_x(x,4.5,r.choice(['#7A1F1F','#1F4D3A','#2B3A7A']))
    wires(-30,30,-3.1,3.1,5.4,6,seed)
def banner_x(x,z,col):
    B.box((x,0,z),(.05,3.2,.25),M(col,.85,kind='fabric'),.01,rot=(R(5),0,0))
def chappal(e,s=1.0):
    obox((0,-.08,.02),(.06*s,.14*s,.015),M('#3A2414',.6),.02,e); obox((0,-.12,.04),(.06*s,.05*s,.02),M('#5A3418',.6),.02,e)
# ---------------------------------------------------------------- car interior (old Corolla, right-hand drive)
def car_int():
    S=1.6; sv=lambda v: tuple(a*S for a in v)
    body=M('#C8C8C4',.35,spec=.9); dash=M('#2A2C34',.6); seat=M('#6A5A4A',.9,kind='fabric',sc=4)
    bx=lambda loc,size,mat,bev=0,rot=(0,0,0): B.box(sv(loc),sv(size),mat,bev*S,rot=rot)
    bx((0,0,-.05),(2.0,2.6,.05),M('#3A3A40',.9,kind='fabric'))
    bx((0,-1.35,.75),(1.0,.3,.25),dash,.08); bx((0,-1.55,1.0),(1.0,.5,.06),dash,.06,(R(-15),0,0))
    for x in (-.5,.5): bx((x,.0,.28),(.3,.36,.1),seat,.06); bx((x,.38,.72),(.28,.1,.42),seat,.06,(R(-12),0,0))
    sw=empty(sv((.5,-1.05,.98)),rot=(R(-70),0,0)); ocyl((0,0,0),.2*S,.03*S,M('#16171C',.5),sw,rot=(0,0,0),seg=24); ocyl((0,0,0),.06*S,.05*S,M('#16171C',.5),sw,rot=(0,0,0),seg=12)
    g=empty(sv((.36,-1.22,1.07)),rot=(R(-70),0,0)); ocyl((0,0,0),.14*S,.01,M('#16171C',.4),g,rot=(0,0,0),seg=24); ocyl((0,0,.006),.125*S,.006,M('#F4F1EA',.5,emit=.8),g,rot=(0,0,0),seg=24)
    needle=empty((0,0,.014),g); obox((0,.06*S,0),(.006*S,.06*S,.003),M('#C8372D',.4,emit=1.5),0,needle)
    text('E',(-.09*S,-.03*S,.014),(0,0,1),.05*S,M('#C8372D',.4,emit=1.5),ex=0,parent=g); text('F',(.09*S,-.03*S,.014),(0,0,1),.05*S,M('#16171C',.4),ex=0,parent=g)
    bx((0,-1.85,1.45),(1.0,.02,.45),M('#BFD6E8',.05,spec=1.0,alpha=.12),0,(R(-30),0,0)); bx((0,0,1.75),(1.05,1.3,.04),M('#D8D4CC',.9,kind='fabric'))
    for s_ in (-1,1): bx((s_*1.05,0,1.25),(.04,1.3,.5),M('#BFD6E8',.05,spec=1.0,alpha=.12)); bx((s_*1.05,0,.55),(.05,1.3,.25),body,.02)
    bx((0,-1.5,1.35),(.06,.02,.03),M('#16171C',.4)); B.ico(sv((0,-1.52,1.25)),.05*S,M('#D9B24A',.4,metal=.6),sub=1)
    r=random.Random(2)
    for k in range(10): x=r.uniform(-14,14); B.box((x,r.choice([-9,9])+r.uniform(-2,2),r.uniform(2,5)),(r.uniform(1.5,3),1.0,r.uniform(2,5)),M(r.choice(['#A8643E','#C9B48A','#8E5030','#D8C8A8']),.85,kind='wall'),0)
    B.box((0,-20,-.06),(30,30,.05),M('#5E6068',.85,kind='asphalt'),0)
    return needle,sw
