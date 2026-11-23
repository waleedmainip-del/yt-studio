# Sets for "Lahore - Everyone Is Secretly Rich":
#   canal(night)   - Lahore Canal Road with light strings and floats over the water (dusk for the plan, night for the walk home)
#   rooftop(stage) - Fort Road food-street rooftop restaurant facing the floodlit Badshahi Mosque
#   kitchen()      - the restaurant's dish-washing kitchen
# World scale: characters are ~2.3 units tall, so props are built ~1.3x real size.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
VSC=1.7   # vehicle scale to match the characters
def big_tree(x,y,s,col):
    B.cyl((x,y,1.6*s),.2*s,3.2*s,M('#5A4030',.85),seg=8)
    for dx,dy,dz,r_ in ((0,0,4.0,1.6),(.9,.3,3.5,1.15),(-.85,-.2,3.6,1.2),(.1,-.7,4.6,1.05),(-.2,.6,4.9,.95)): B.ico((x+dx*s,y+dy*s,dz*s),r_*s,M(shade(col,1+.12*math.sin(x*3+dz)),.85,kind='leaves'),sub=1)
def lotus(x,y,z,col,em):
    B.cyl((x,y,z+.12),.9,.2,M('#2F7A4A',.6),seg=14)
    for k in range(10): a=k*pi/5; B.box((x+math.cos(a)*.55,y+math.sin(a)*.55,z+.5),(.34,.12,.42),M(col,.4,emit=em),.08,rot=(0,R(-28),a))
    B.ico((x,y,z+.62),.3,M('#FFE08A',.3,emit=em*2),sub=1)
def canal(night=False,fx_=0.0):
    r=random.Random(21); em=5.0 if night else 2.2
    road=M('#3A3C44',.85,kind='asphalt'); grass=M('#4F8A45',.9,kind='leaves',h2='#447A3C',sc=3); rl=M('#1F6A46',.5,metal=.3)
    B.box((0,-5.6,-.06),(62,4.0,.06),road,0); B.box((0,23.6,-.06),(62,3.8,.06),road,0)
    for x in range(-58,59,6): B.box((x,-5.6,.006),(1.5,.08,.006),M('#F4F1EA',.6),0)
    for i,x in enumerate(range(-60,61,2)): B.box((x,-1.55,.07),(1.0,.14,.12),M('#F2C14E' if i%2 else '#16171C',.6),.02)
    B.box((0,1.0,.04),(62,2.45,.06),M('#B8A890',.85,kind='tile',h2='#A49478',sc=2.2),0)
    for y in (3.6,19.4):
        for x in range(-60,61,3): B.box((x,y,.72),(.07,.07,.7),rl,.02); B.ico((x,y,1.5),.1,M('#D9B24A',.3,metal=.8),sub=1)
        for z in (.55,.95,1.35): B.box((0,y,z),(62,.04,.045),rl,.01)
    B.box((0,4.35,0),(62,.65,.07),grass,0); B.box((0,5.95,-.55),(62,1.28,.06),grass,0,rot=(R(-24),0,0))
    B.box((0,11.5,-1.08),(62,4.6,.04),M('#2E6658',.07,spec=1.0),0)
    B.box((0,17.05,-.55),(62,1.28,.06),grass,0,rot=(R(24),0,0)); B.box((0,18.75,0),(62,.75,.07),grass,0); B.box((0,20.2,.02),(62,.7,.05),M('#B8A890',.85,kind='tile'),0)
    cols=['#3F7A3A','#4F8A3A','#356E38','#5A9444']
    for x in range(-56,57,8): big_tree(x+r.uniform(-1,1),4.45,r.uniform(2.0,2.5),r.choice(cols)); big_tree(x+4+r.uniform(-1,1),18.6,r.uniform(2.2,2.8),r.choice(cols))
    for x in range(-58,59,5): big_tree(x+r.uniform(-1,1),28.5+r.uniform(-1,1),r.uniform(2.4,3.2),r.choice(cols))
    for i in range(16):                                                    # far buildings with lit windows
        x=-60+i*8+r.uniform(-1,1); h=r.uniform(7,15); w=r.uniform(3,4.2); B.box((x,36,h/2),(w,3,h/2),M(r.choice(['#C9B8A0','#D8C8B0','#A8B4C0','#E0D0B8','#B8A088']),.8),0)
        for j in range(int(h/2.6)):
            for q in (-1.6,0,1.6): B.box((x+q,32.95,2.4+j*2.5),(.5,.04,.6),M('#FFE8B0',.2,emit=r.choice([0,em*.3,em*.5])),0)
    for x in range(-55,56,10):                                             # street lamps on the footpath
        B.cyl((x,3.42,3.4),.09,6.8,M('#2A2C34',.4,metal=.5),seg=8); B.box((x,2.95,6.75),(.07,.5,.05),M('#2A2C34',.4),.01); B.ico((x,2.5,6.62),.2,M('#FFE0A0',.3,emit=em*1.4),sub=1)
    bulbs=['#FF4F7A','#FFD23F','#35C8FF','#7CFC9A','#FF8A3A']
    for i,x in enumerate(range(-54,55,6)):                                 # light strings across the canal + their glow on the water
        N=22; c=bulbs[i%5]
        B.cyl((x,3.9,2.6),.06,5.2,M('#2A2C34',.4),seg=6); B.cyl((x,19.1,2.6),.06,5.2,M('#2A2C34',.4),seg=6)
        for k in range(N+1):
            y=3.9+15.2*k/N; z=5.1-1.5*math.sin(pi*k/N); B.ico((x,y,z),.11,M(c if k%2 else '#FFF3D0',.3,emit=em*1.5),sub=1)
            if k<N: y2=3.9+15.2*(k+1)/N; z2=5.1-1.5*math.sin(pi*(k+1)/N); B.box((x,(y+y2)/2,(z+z2)/2+.1),(.01,.36,.01),M('#16171C',.5),0,rot=(math.atan2(z2-z,y2-y),0,0))
        B.box((x,11.5,-1.03),(.3,4.2,.005),M(c,.2,emit=em*.35,alpha=.5),0)
    lotus(-6.5,11.0,-1.05,'#FF7AA8',em); lotus(5.5,12.8,-1.05,'#FFD23F',em); lotus(17,10.4,-1.05,'#7AD8FF',em); lotus(-19,12.2,-1.05,'#FF9A5A',em); lotus(33,11.6,-1.05,'#FF7AA8',em); lotus(44,12.9,-1.05,'#FFD23F',em)
    # sign gantry, milestone, bench, planters, bin
    B.cyl((-8.2,3.0,2.7),.09,5.4,M('#5A5E66',.4,metal=.6),seg=8); B.box((-8.2,2.92,4.75),(2.15,.05,.72),M('#0F6A3A',.6),.03); B.box((-8.2,2.9,4.75),(2.08,.04,.66),M('#F4F1EA',.6),.02); B.box((-8.2,2.88,4.75),(2.03,.04,.61),M('#0F6A3A',.6),.02)
    stext('CANAL ROAD',(-8.2,2.83,5.0),.36,'#FFFFFF',e=.6 if night else 0); stext('MALL ROAD    JAIL ROAD',(-8.2,2.83,4.48),.2,'#FFFFFF',e=.6 if night else 0)
    B.box((4.9,3.0,.45),(.34,.16,.45),M('#F4F1EA',.6),.04); B.box((4.9,3.0,.98),(.34,.16,.12),M('#F2C14E',.6),.06); stext('LAHORE',(4.9,2.82,.62),.14,'#16171C'); stext('0 KM',(4.9,2.82,.34),.15,'#16171C')
    wd=M('#6A4628',.6,kind='wood')
    for bx in (9.5,-15):
        B.box((bx,2.9,.62),(1.1,.3,.05),wd,.02); B.box((bx,3.2,1.05),(1.1,.05,.3),wd,.02)
        for sx in (-.9,.9): B.box((bx+sx,2.9,.3),(.06,.28,.3),M('#2A2C34',.4),.01)
    for px in (-12,-3.6,2.4,7.2,13,20):
        B.box((px,3.1,.3),(.42,.32,.3),M('#C96A3A',.7),.04)
        for k in range(6): B.ico((px+r.uniform(-.3,.3),3.1+r.uniform(-.2,.2),.75+r.uniform(0,.25)),.2,M(r.choice(['#E8554D','#F2C14E','#F28AA0','#3F8A4A','#3F8A4A']),.7),sub=1)
    B.cyl((12.2,3.0,.55),.3,1.1,M('#2B5AA8',.5),seg=10); stext('USE ME',(12.2,2.68,.7),.11,'#FFFFFF')
    B.done('canal')
    setup_world('night' if night else 'dusk',70)
    if night:
        for dx in (-20,-10,0,10): point((fx_+dx,2.5,6.3),1600,(1,.85,.6),r=.4,shadow=(dx in (-10,0)))
        point((fx_-6,-6,5),900,(.7,.8,1.0),r=2,shadow=False); point((fx_-4,11,3.5),1000,(1,.6,.75),r=2,shadow=False)
    else:
        point((0,-5,4.5),600,(1,.85,.7),r=2,shadow=False); point((0,11,3.5),500,(1,.7,.6),r=2,shadow=False)
    bike=motorbike((-4.3,1.6,0),205,'#C8372D'); bike['root'].scale=(1.4,)*3
    cars=[car((0,0,-50),90,c,seed=i) for i,c in enumerate(('#F4F1EA','#2B5AA8','#16171C'))]; rk=rickshaw((0,0,-50),90,'#2E8A3A');
    for v in cars+[rk]: v['root'].scale=(VSC,)*3
    return dict(bike=bike,cars=cars,rk=rk)
def vdrive(V,x,y,rotz,dist): drive(V,x,y,rotz,dist/VSC)
def traffic(S,tg):
    """two lanes on the near road, one direction each, constant gaps"""
    L_=110
    for i,v in enumerate(S['cars'][:2]+[S['rk']]):
        x=-55+((i*37+tg*6.5)%L_); vdrive(v,x,-7.7,0,tg*6.5)
    v=S['cars'][2]; x=55-((20+tg*7.5)%L_); vdrive(v,x,-4.6,180,tg*7.5)
# ---------------------------------------------------------------- rooftop restaurant
def chair(x,y,rz=0,col='#3A2A20',cu='#B8456A'):
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M(col,.5,kind='wood'); c=M(cu,.9,kind='fabric')
    obox((0,0,.56),(.3,.28,.04),c,.03,e); obox((0,.29,1.05),(.3,.04,.5),wd,.03,e); obox((0,.25,1.05),(.23,.02,.4),c,.03,e)
    for dx in (-.25,.25):
        for dy in (-.23,.23): obox((dx,dy,.27),(.035,.035,.27),wd,.01,e)
    return e
def rtable(x,y,rr=1.05,lit=True):
    B.cyl((x,y,.5),.09,1.0,M('#2A2C34',.4,metal=.5),seg=10); B.cyl((x,y,.03),.45,.06,M('#2A2C34',.4,metal=.5),seg=14)
    B.cyl((x,y,1.0),rr,.05,M('#F8F6F0',.85,kind='fabric'),seg=28); B.cyl((x,y,.86),rr*1.01,.26,M('#F1EEE6',.9,kind='fabric'),seg=28)
    B.cyl((x,y,1.1),.07,.16,M('#D9B24A',.3,metal=.8),seg=10); B.cyl((x,y,1.24),.055,.14,M('#FFE7B0',.2,emit=4.0 if lit else 0,alpha=.9),seg=10); B.cyl((x,y,1.33),.07,.03,M('#D9B24A',.3,metal=.8),seg=10)
def plate_b(x,y,z=1.03,rr=.2,gold=False):
    B.cyl((x,y,z+.012),rr,.024,M('#F8F6F0',.3,spec=.8),seg=18); B.cyl((x,y,z+.02),rr*.72,.02,M('#D9B24A',.3,metal=.8) if gold else M('#F2F0EA',.3,spec=.8),seg=18)
def glass_b(x,y,z=1.03,col='#F28A3A'):
    B.cyl((x,y,z+.09),.05,.18,M('#DCEAF2',.05,spec=1.0,alpha=.35),seg=10); B.cyl((x,y,z+.07),.042,.12,M(col,.4,alpha=.85),seg=10)
SEATS={'wa':(0,1.5,0),'bi':(-1.5,.25,72),'sh':(1.5,.25,-72)}
def hero_table(stage):
    rtable(0,0,1.05); rr=random.Random(4)
    for k,(x,y,rz) in SEATS.items(): chair(x,y,rz)
    pl=[(0,.68),(-.68,.12),(.68,.12)]
    if stage=='menu':
        for (x,y) in pl: plate_b(x,y); glass_b(x*1.25+.02,y+.3 if y<.5 else y-.02,col='#BFD6E8')
    elif stage=='feast':
        karahi_obj((-.32,.28,1.03),.62); karahi_obj((.36,.3,1.03),.5)
        plate_b(0,-.28,rr=.34,gold=True); B.ico((0,-.28,1.1),.25,M('#F2C14E',.8),sc=(1,1,.5),sub=2)                      # biryani
        for k in range(8): B.box((rr.uniform(-.17,.17),-.28+rr.uniform(-.17,.17),1.2+rr.uniform(0,.04)),(.05,.035,.03),M(rr.choice(['#8A4A22','#F28A3A','#F4F1EA']),.7),.01,rot=(0,0,rr.uniform(0,3)))
        plate_b(-.6,-.42,rr=.22); [B.cyl((-.68+j*.055,-.42,1.07),.026,.26,M('#6A3A22',.8),rot=(R(90),0,.25),seg=6) for j in range(4)]   # seekh kabab
        plate_b(.62,-.4,rr=.22); [B.cyl((.62+.015*j,-.4,1.055+j*.02),.19,.018,M('#E8C88A',.8,h2='#B5642A',sc=9),seg=14) for j in range(5)]  # naan
        B.cyl((.05,.72,1.08),.12,.1,M('#F8F6F0',.3),seg=14); B.cyl((.05,.72,1.12),.105,.03,M('#F4F6F2',.4),seg=14)        # raita
        plate_b(-.2,.75,rr=.16); B.ico((-.2,.75,1.09),.11,M('#4F9A3A',.8),sc=(1,1,.5),sub=1)
        for (x,y) in ((-.9,-.05),(.92,-.08),(.28,.86)): glass_b(x,y)
        B.cyl((-.9,.5,1.2),.085,.34,M('#BFD6E8',.05,spec=1.0,alpha=.4),seg=12); B.cyl((-.9,.5,1.16),.075,.24,M('#F28AA0',.4,alpha=.85),seg=12)
    else:                                                                                                                # after the feast: scraps, bones, stacked bowls
        for (x,y) in pl+[(-.35,-.35),(.4,-.3)]:
            plate_b(x,y)
            for k in range(3): B.box((x+rr.uniform(-.09,.09),y+rr.uniform(-.09,.09),1.065),(.04,.015,.012),M(rr.choice(['#F4EEE0','#8A4A22','#C2552A']),.6),.005,rot=(0,0,rr.uniform(0,3)))
        karahi_obj((-.05,.4,1.03),.5,food=False)
        for (x,y) in ((-.9,-.05),(.92,-.08),(.28,.86)): B.cyl((x,y,1.12),.05,.18,M('#DCEAF2',.05,spec=1.0,alpha=.35),seg=10)
        for k in range(4): B.box((rr.uniform(-.7,.7),rr.uniform(-.6,.6),1.035),(.07,.07,.004),M('#F4F1EA',.9),0,rot=(0,0,rr.uniform(0,3)))  # crumpled napkins
def receipt(start=(.4,-.5,1.06)):
    """bill folder + a very long receipt that unrolls over the table edge to the floor. returns (folder, setter(k 0..1))"""
    fo=empty(start); obox((0,0,.012),(.2,.14,.012),M('#16171C',.5),.01,fo); obox((0,0,.026),(.17,.11,.004),M('#D9B24A',.3,metal=.8),.002,fo)
    pm=M('#FFFFFF',.8,emit=.25); ink=M('#3A3D47',.7)
    def seg(parent,loc,rot,ln):
        e=empty(loc,parent,rot=rot); obox((0,-ln/2,0),(.11,ln/2,.003),pm,0,e)
        for k in range(int(ln/.09)): obox(((-.02 if k%3 else .0),-.05-k*.09,.004),(.07 if k%3 else .09,.012,.002),ink,0,e)
        obox((.075,-ln+.05,.004),(.03,.02,.002),M('#C8372D',.6),0,e); return e
    L1=.5; L2=1.0; L3=1.7
    s1=seg(None,(start[0],start[1]-.14,1.062),(0,0,0),L1); s2=seg(None,(start[0],start[1]-.14-L1,1.062),(R(88),0,0),L2); s3=seg(None,(start[0],start[1]-.14-L1-.04,.062),(0,0,0),L3)
    def setk(k):
        a=max(0,min(1,k/.18)); b=max(0,min(1,(k-.18)/.3)); c=max(0,min(1,(k-.48)/.52))
        for e,q in ((s1,a),(s2,b),(s3,c)): e.scale=(1,max(q,1e-4),1) if q>0 else (0,0,0)
    setk(0); return fo,setk
def jharoka(x,y,z,col,n=(1,0,0)):
    """carved wooden balcony window on a side wall facing +x or -x"""
    s=n[0]; wd=M(col,.6,kind='wood'); B.box((x+s*.3,y,z),(.3,.95,.9),wd,.04); B.box((x+s*.62,y,z+.1),(.02,.7,.55),M('#FFE2A0',.3,emit=2.2),0)
    for q in (-.47,0,.47): B.box((x+s*.64,y+q,z+.1),(.02,.03,.55),wd,0)
    for q in (-.25,.25): B.box((x+s*.64,y,z+.1+q),(.02,.7,.025),wd,0)
    B.box((x+s*.35,y,z+1.02),(.42,1.1,.07),wd,.03); B.box((x+s*.35,y,z-.95),(.4,1.05,.06),wd,.03)
    for k in range(5): B.ico((x+s*.35,y-.8+k*.4,z+1.2),.14,M(shade(col,1.3),.5),sub=1)
def mosque_night(x,y,z,s):
    sm=M('#C4583A',.8,emit=.55); dm=M('#FFF4E2',.5,emit=1.1); gold=M('#FFD26A',.3,emit=2.0)
    B.box((x,y,z+4*s),(17*s,5*s,4*s),sm,0)
    for k in range(-1,2):
        B.box((x+k*7*s,y-5.05*s,z+3.4*s),(1.7*s,.1,2.7*s),M('#FFD9A0',.4,emit=1.6),0); B.box((x+k*7*s,y-5.1*s,z+3.0*s),(1.2*s,.1,2.2*s),M('#3A1E16',.8),0)
        B.ico((x+k*7*s,y,z+(10 if k==0 else 8.5)*s),(4.7 if k==0 else 3.2)*s,dm,sc=(1,1,1.14),sub=3); B.cyl((x+k*7*s,y,z+(14.2 if k==0 else 11.7)*s),.14*s,1.6*s,gold,seg=8)
    for q in range(-5,6):
        if q%2: B.box((x+q*2.9*s,y-5.05*s,z+7.3*s),(.7*s,.1,.5*s),M('#FFE2B0',.4,emit=1.2),0)
    for sx in (-1,1):
        for sy in (-1,1):
            mx,my=x+sx*18*s,y+sy*5*s; B.cyl((mx,my,z+9.5*s),1.0*s,19*s,sm,seg=8,r2=.8*s); B.cyl((mx,my,z+15.5*s),1.35*s,.5*s,dm,seg=8); B.cyl((mx,my,z+19.6*s),.95*s,1.5*s,dm,seg=8); B.ico((mx,my,z+20.8*s),1.0*s,dm,sub=2); B.cyl((mx,my,z+22.2*s),.1*s,1.2*s,gold,seg=6)
    B.box((x,y-14*s,z+1.6*s),(34*s,.6*s,1.6*s),M('#A8482E',.85,emit=.3),0)                       # outer wall with merlons
    for q in range(-16,17): B.box((x+q*2*s,y-14*s,z+3.4*s),(.5*s,.5*s,.25*s),M('#A8482E',.85,emit=.3),0)
def rooftop(stage='menu'):
    r=random.Random(8); tile=M('#C8795A',.6,kind='tile',h2='#E8D8B8',sc=1.6); brick=M('#9A4A34',.85,kind='wall',h2='#843C2A',sc=2.2); wd=M('#4A2E1C',.6,kind='wood'); gold=M('#D9B24A',.3,metal=.8)
    B.box((0,-.5,-.08),(9,7.5,.08),tile,0)
    # back + side parapets with lantern pillars
    B.box((0,7.0,.5),(9,.18,.5),brick,.02); B.box((0,7.0,1.04),(9.1,.26,.06),M('#E8D8B8',.7),.02)
    for x in (-9,-6,-3,0,3,6,9):
        B.box((x,7.0,.8),(.26,.26,.8),brick,.02); B.box((x,7.0,1.66),(.32,.32,.06),M('#E8D8B8',.7),.02); B.box((x,7.0,1.95),(.14,.14,.2),M('#FFE2A0',.2,emit=5.0),.02); B.box((x,7.0,2.2),(.19,.19,.04),gold,.01)
    B.box((0,-8.0,.5),(9,.18,.5),brick,.02); B.box((0,-8.0,1.04),(9.1,.26,.06),M('#E8D8B8',.7),.02)
    for x in (-9,-6,-3,0,3,6,9):
        B.box((x,-8.0,.8),(.26,.26,.8),brick,.02); B.box((x,-8.0,1.66),(.32,.32,.06),M('#E8D8B8',.7),.02); B.box((x,-8.0,1.95),(.14,.14,.2),M('#FFE2A0',.2,emit=5.0),.02)
    # left: painted haveli wall with jharokas and arched lamp niches
    B.box((-9.2,-.5,2.6),(.25,7.5,2.7),M('#2B6A8A',.85,kind='wall',h2='#255E7C',sc=2),0); B.box((-9.0,-.5,.5),(.08,7.5,.5),M('#F2C14E',.8),0); B.box((-9.0,-.5,5.2),(.1,7.5,.14),M('#F2C14E',.8),.02)
    for i,y in enumerate((-5,-1.2,2.6)): jharoka(-9.05,y,3.3,['#7A2E1C','#1F6A46','#7A2E1C'][i])
    for y in (-3.1,.7,4.6): B.box((-8.98,y,1.75),(.05,.42,.62),M('#16425A',.8),.05); B.ico((-8.9,y,1.5),.14,M('#FFD27A',.2,emit=6.0),sub=1)
    # right: stair house with entry door + neon sign, waiter station
    B.box((9.6,3.2,2.3),(.9,3.0,2.3),M('#E8C87A',.85,kind='wall',h2='#D8B868',sc=2),0); B.box((8.68,3.2,1.5),(.05,.85,1.5),wd,.03); B.box((8.64,3.2,1.5),(.03,.7,1.35),M('#2A1A10',.7),.02)
    B.box((8.66,3.2,3.15),(.05,1.0,.1),gold,.02); B.box((8.6,3.2,3.85),(.06,1.75,.42),M('#16171C',.5),.04); stext('SHAHI ROOFTOP',(8.52,3.2,3.85),.36,'#FF4F8B',n=(-1,0,0),e=5.0)
    B.box((9.6,-3.5,1.2),(.9,3.7,1.2),M('#E8C87A',.85,kind='wall'),0); B.box((9.6,-3.5,2.46),(1.0,3.8,.06),M('#E8D8B8',.7),.02)
    B.box((8.2,-2.6,.55),(.45,1.2,.55),wd,.03); B.box((8.2,-2.6,1.13),(.5,1.25,.03),M('#F4F1EA',.3,spec=.8),.01)
    for k in range(6): B.cyl((8.2,-3.3,1.18+k*.035),.2,.03,M('#F8F6F0',.3,spec=.8),seg=16)
    B.cyl((8.2,-2.4,1.33),.1,.34,M('#C9CED8',.2,metal=.9),seg=12); B.box((8.2,-1.85,1.2),(.2,.14,.05),M('#7A1F2E',.8,kind='fabric'),.02)
    # BBQ counter with glowing coals at the back-left
    B.box((-6.6,5.3,.55),(1.3,.5,.55),brick,.03); B.box((-6.6,5.3,1.13),(1.35,.55,.04),M('#2A2C34',.4,metal=.6),.01); B.box((-6.6,5.3,1.18),(1.1,.36,.02),M('#FF6A2A',.4,emit=4.0),0)
    for k in range(9): B.cyl((-7.5+k*.22,5.3,1.25),.03,.8,M('#6A3A22',.8),rot=(R(90),0,0),seg=6)
    B.box((-6.6,6.0,2.6),(1.4,.05,.3),M('#16171C',.5),.03); stext('LIVE BBQ',(-6.6,5.93,2.6),.32,'#FFD23F',e=4.0)
    # plants, lantern stands
    for (x,y,s) in ((-8.2,6.2,1.3),(8.0,6.3,1.2),(-8.3,-6.6,1.4),(4.6,6.3,1.0),(-3.4,6.35,.9)):
        B.cyl((x,y,.3*s),.3*s,.6*s,M('#C96A3A',.7),seg=12,r2=.36*s)
        for k in range(8): a=k*.8; B.box((x+math.cos(a)*.18*s,y+math.sin(a)*.18*s,(1.0+r.uniform(0,.5))*s),(.05*s,.16*s,.45*s),M(shade('#3F8A4A',r.uniform(.8,1.2)),.7),.02,rot=(R(r.uniform(-25,25)),R(r.uniform(-25,25)),a))
    # string lights on four poles
    poles=[(-8.6,-7.6),(8.6,-7.6),(8.6,6.8),(-8.6,6.8)]
    for (x,y) in poles: B.cyl((x,y,2.7),.07,5.4,M('#2A2C34',.4),seg=8)
    def string(p0,p1,n,z=5.2,sag=.7):
        for k in range(n+1):
            f=k/n; B.ico((L(p0[0],p1[0],f),L(p0[1],p1[1],f),z-sag*math.sin(pi*f)),.085,M('#FFE2A0',.3,emit=6.0),sub=1)
    string(poles[0],poles[2],26); string(poles[1],poles[3],26); string(poles[3],poles[2],22,sag=.5); string(poles[0],poles[1],22,sag=.5); string(poles[0],poles[3],18,sag=.4); string(poles[1],poles[2],18,sag=.4)
    # other tables
    for (x,y) in ((-4.9,3.4),(4.7,3.7),(-5.6,-2.6)):
        rtable(x,y,.9)
        for k in range(3): a=k*2.1+x; plate_b(x+math.cos(a)*.5,y+math.sin(a)*.5); glass_b(x+math.cos(a+1)*.6,y+math.sin(a+1)*.6,col=r.choice(['#F28A3A','#F28AA0','#BFD6E8']))
    hero_table(stage)
    # the old city below + Badshahi Mosque beyond
    for i in range(46):
        x=r.uniform(-70,70); y=r.uniform(13,58); h=r.uniform(2,7); w=r.uniform(3,6); c=r.choice(['#4A3A34','#5A4A40','#3E3A44','#6A5444','#4E4038'])
        B.box((x,y,-9+h/2),(w,r.uniform(3,5),h/2+4),M(c,.9),0)
        if r.random()<.6: B.box((x+r.uniform(-1,1),y-r.uniform(3,5)-.05,-5+h/2+r.uniform(-1,1)),(.5,.05,.6),M('#FFD9A0',.3,emit=r.uniform(1,3)),0)
        if r.random()<.4: B.cyl((x+1,y,-4.4+h),.7,1.1,M('#2B5AA8',.6),seg=10)
        if r.random()<.3: B.cyl((x-1,y-1,-4.6+h),.6,.08,M('#C9CED8',.4,metal=.6),rot=(R(55),0,r.uniform(0,3)),seg=12)
    for i in range(40):
        x=r.uniform(-70,70); y=r.uniform(-60,-13); h=r.uniform(2,9); w=r.uniform(3,6)
        B.box((x,y,-9+h/2),(w,r.uniform(3,5),h/2+4),M(r.choice(['#4A3A34','#5A4A40','#3E3A44','#6A5444']),.9),0)
        if r.random()<.7: B.box((x+r.uniform(-1,1),y+r.uniform(3,5)+.05,-5+h/2+r.uniform(-1,1)),(.5,.05,.6),M('#FFD9A0',.3,emit=r.uniform(1,3)),0)
    for k in range(50): B.ico((r.uniform(-150,150),-200,r.uniform(10,130)),r.uniform(.18,.4),M('#FFFFFF',.3,emit=4.0),sub=0)
    mosque_night(0,92,-10,2.4)
    B.ico((-38,170,62),5.0,M('#FFF6DC',.3,emit=3.0),sub=2)
    for k in range(60): B.ico((r.uniform(-150,150),200,r.uniform(20,130)),r.uniform(.18,.4),M('#FFFFFF',.3,emit=4.0),sub=0)
    B.done('rooftop')
    setup_world('night',40); sc=bpy.context.scene; sc.eevee.bloom_intensity=.06
    point((0,-1.8,4.8),520,(1,.86,.66),r=1.2); point((0,0,1.9),22,(1,.8,.5),r=.15,shadow=False)
    point((-5,3,4.2),300,(1,.8,.6),r=1,shadow=False); point((5,3.5,4.2),300,(1,.8,.6),r=1,shadow=False); point((-6,-3,4.2),260,(1,.8,.6),r=1,shadow=False); point((5.5,-4,4.2),260,(1,.82,.64),r=1,shadow=False)
    point((0,-6.5,3.2),420,(.8,.85,1.0),r=2.5,shadow=False); point((-6.6,5.0,1.9),90,(1,.5,.25),r=.3,shadow=False)
# ---------------------------------------------------------------- kitchen
KX=(-2.6,-.8,1.0)
def kitchen():
    r=random.Random(6); st=M('#B8BEC8',.25,metal=.85); tile=M('#F2F4F2',.3,kind='tile',h2='#DDE4E2',sc=.9,spec=.7)
    B.box((0,0,-.05),(6,5,.05),M('#8A8E96',.5,kind='tile',h2='#74787F',sc=1.4),0); B.box((0,3.2,2.6),(6,.1,2.7),tile,0); B.box((-6,0,2.6),(.1,5,2.7),tile,0); B.box((6,0,2.6),(.1,5,2.7),tile,0); B.box((0,0,5.3),(6,5,.1),M('#E8E8E4',.9),0)
    B.box((0,3.08,1.5),(6,.03,.08),M('#C8372D',.5),0)
    # island sink counter (the three stand behind it, facing -y)
    B.box((0,.2,.55),(3.3,.55,.55),st,.03); B.box((0,.2,1.12),(3.35,.6,.03),st,.01)
    for x in KX:
        B.box((x,.2,1.1),(.62,.4,.06),M('#6A7078',.3,metal=.8),.02); B.box((x,.2,1.135),(.56,.34,.01),M('#BFE6F2',.1,spec=1.0,alpha=.8),0)
        B.cyl((x,.68,1.42),.03,.6,st,seg=8); B.box((x,.5,1.7),(.03,.2,.03),st,.01)
        for k in range(9): B.ico((x+r.uniform(-.45,.45),.2+r.uniform(-.25,.25),1.17+r.uniform(0,.08)),r.uniform(.05,.11),M('#FFFFFF',.3,emit=.6),sub=1)
    # towers of dirty plates
    for (x,y,n,z0) in ((-1.7,-.05,6,1.15),(2.35,.0,27,1.15),(-4.9,-.6,34,0),(4.9,-1.4,30,0),(.1,-.22,9,1.15)):
        for k in range(n): B.cyl((x+.025*math.sin(k*.7),y+.02*math.cos(k*.9),z0+.03+k*.045),.24,.035,M('#F8F6F0',.3,spec=.8),seg=16)
    # back wall: shelves with pots, hanging ladles, order rail, clock, sign
    for z in (2.3,3.3): B.box((0,2.85,z),(4.5,.28,.04),st,.01)
    for k in range(8): x=-3.9+k*1.1; B.cyl((x,2.85,2.3+.24),.26,.4,M(r.choice(['#3A3D47','#B8BEC8','#8A5A32']),.3,metal=.7),seg=14)
    for k in range(7): x=-3.6+k*1.2; B.cyl((x,2.85,3.3+.2),.2,.34,M(r.choice(['#C8372D','#F2C14E','#B8BEC8']),.4,metal=.4),seg=12)
    B.box((0,3.02,1.95),(4.5,.02,.02),st,0)
    for k in range(10): x=-4.2+k*.93; B.box((x,3.0,1.72),(.012,.012,.22),st,0); B.cyl((x,3.0,1.48),.07,.03,st,rot=(R(90),0,0),seg=10)
    B.cyl((4.9,3.05,3.9),.42,.06,M('#F4F1EA',.5),rot=(R(90),0,0),seg=24); B.box((4.9,3.0,4.05),(.02,.02,.16),M('#16171C',.5),0); B.box((5.02,3.0,3.9),(.13,.02,.02),M('#16171C',.5),0)
    B.box((.6,3.05,4.25),(1.7,.04,.42),M('#C8372D',.5),.03); stext('NO PAY = WASH',(.6,2.99,4.25),.32,'#FFFFFF')
    B.cyl((-5.2,-3.2,.5),.4,1.0,M('#3A3D47',.5),seg=12); B.box((5.3,1.8,1.3),(.5,.5,1.3),st,.03)
    B.done('kitchen')
    S,A,w,bg=setup_interior('day',room=(0,-1,5.1),res=PCT,samples=SAMPLES,shadow_dist=20); A.data.energy=130; A.data.size=7.0; A.data.color=(.92,.97,1.0)
    point((0,-4,3.4),300,(1,.95,.9),r=1.5); point((-4,1,3.6),70,(.8,.9,1.0),r=.6,shadow=False); point((4,1,3.6),70,(.8,.9,1.0),r=.6,shadow=False)
