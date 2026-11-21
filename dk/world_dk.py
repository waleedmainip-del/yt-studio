# Sets for "The Guy Who Couldn't Be Killed": Maple Avenue (brownstones, fire escapes, water towers, deli, clock),
# taxis/bus/truck, crash field, volcano, kitchen. Avenue runs along X; road |y|<4.5; sidewalks 4.5-7.5; fronts at y=+-7.5.
BRICK=['#9C4A36','#B5603F','#7E3B2E','#A8724E','#C9A27A','#8A5A44','#6E4A3E','#B88A60','#9E5848','#D2B48C']
SHOPS=[('SAL\'S SANDWICHES','#2E7D4F'),('PIZZA','#C8372D'),('LAUNDRY','#2F6EA8'),('BAGELS','#D98A1C'),('BOOKS','#6B3FA0'),('COFFEE','#5A3A26'),
       ('HARDWARE','#B23A2E'),('FLOWERS','#D45A8A'),('BARBER','#1F3F7A'),('DINER','#C23B3B'),('PHARMACY','#2E8A6E'),('DELI','#1F6F4A')]
def sign_text(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=.02,parent=parent)

def brownstone(cx,w,floors,col,seed,side=1,Y=7.5,shop=None,stoop=False,fire=None,tower=None,lit=.25):
    r=random.Random(seed); s=side; FH=3.1; G=3.6; H=G+floors*FH; D=7.0
    brick=M(col,.88,kind='wall',h2=shade(col,.82),sc=1.4); trim=M(r.choice(['#EDE3CF','#E2D6BE','#F2EEE4','#D8CBB0']),.7); dk=M('#121418',.4)
    glass=M('#1C2533',.08,spec=.9); warm=M('#FFD9A0',.4,emit=1.6); metal=M('#22252B',.45,metal=.6)
    yf=Y*s; yc=(Y+D/2)*s
    B.box((cx,yc,H/2),(w/2,D/2,H/2),brick,0)
    # cornice + dentils + brackets
    B.box((cx,yf-.25*s,H+.25),(w/2+.12,.32,.22),trim,.03); B.box((cx,yf-.12*s,H-.05),(w/2+.05,.18,.06),trim,.01)
    for k in range(int(w/.5)): B.box((cx-w/2+.25+k*.5,yf-.2*s,H-.18),(.08,.12,.07),trim,.005)
    for k in range(int(w/1.6)+1): B.box((cx-w/2+.2+k*(w-.4)/max(1,int(w/1.6)),yf-.3*s,H+.0),(.1,.2,.25),trim,.02)
    B.box((cx,yf-.08*s,G+.05),(w/2+.04,.12,.12),trim,.02)
    # upper windows
    nw=max(2,int(w/1.65)); sp=(w-.6)/nw
    for f in range(floors):
        z=G+f*FH+1.45
        for k in range(nw):
            x=cx-w/2+.3+sp*(k+.5)
            B.box((x,yf-.03*s,z),(.42,.08,.78),trim,.02); B.box((x,yf-.07*s,z),(.34,.05,.7),warm if r.random()<lit else glass,.0)
            B.box((x,yf-.1*s,z),(.02,.04,.7),trim,0); B.box((x,yf-.1*s,z+.05),(.34,.04,.02),trim,0)
            B.box((x,yf-.12*s,z+.92),(.5,.12,.12),trim,.02); B.box((x,yf-.14*s,z-.84),(.48,.16,.05),trim,.01)
            if r.random()<.35: B.box((x+r.uniform(-.1,.1),yf-.11*s,z+.2),(.3,.03,.55),M(r.choice(['#E8D2A8','#D9A0A0','#9FC2D9','#F4F1EA']),.9,kind='fabric'),.0)
            if r.random()<.18: B.box((x,yf-.32*s,z-.55),(.3,.25,.2),M('#C9CED8',.5,metal=.2),.02); B.box((x,yf-.58*s,z-.55),(.22,.01,.12),M('#5A5E66',.5),0)
            if r.random()<.12: B.box((x,yf-.3*s,z-.86),(.44,.18,.08),M('#5E3A22',.8),.01); [B.ico((x-.3+j*.2,yf-.3*s,z-.7),.12,M(r.choice(['#C8372D','#E8C24E','#5FA84A','#D45A8A']),.8,kind='leaves'),sub=1) for j in range(4)]
    # fire escape
    if fire is None: fire=r.random()<.55
    if fire:
        fx0=cx+r.choice([-1,1])*sp*.5
        for f in range(floors):
            z=G+f*FH+.55; B.box((fx0,yf-.62*s,z),(1.45,.55,.03),metal,0)
            B.box((fx0,yf-1.16*s,z+.5),(1.45,.02,.02),metal,0); B.box((fx0,yf-1.16*s,z+.25),(1.45,.015,.015),metal,0)
            for j in range(13): B.box((fx0-1.4+j*.233,yf-1.16*s,z+.25),(.012,.012,.25),metal,0)
            for sx in (-1.45,1.45): B.box((fx0+sx,yf-.62*s,z+.25),(.012,.55,.012),metal,0)
            if f<floors-1:
                L_=math.hypot(2.0,FH); ang=math.atan2(FH,2.0)
                B.box((fx0,yf-.82*s,z+FH/2),(L_/2,.18,.02),metal,0,rot=(0,-ang,0))
        B.box((fx0+.9,yf-1.0*s,G-.6),(.18,.02,.9),metal,0)
    # roof: water tower / chimneys / parapet
    if tower is None: tower=r.random()<.3
    B.box((cx,yc,H+.55),(w/2,D/2,.08),M('#5A5E66',.9,kind='concrete'),0)
    for k in range(r.randint(1,2)): B.box((cx+r.uniform(-w/3,w/3),yc+r.uniform(-1,2)*s,H+1.0),(.3,.3,.55),brick,.02)
    if tower:
        tx=cx+r.uniform(-w/4,w/4); ty=yc+1.2*s; wood=M('#7A5A3E',.85,kind='wood',sc=.8)
        for dx in (-.7,.7):
            for dy in (-.7,.7): B.box((tx+dx,ty+dy,H+1.4),(.05,.05,.9),metal,0)
        B.cyl((tx,ty,H+3.3),1.05,2.2,wood,seg=18); B.cyl((tx,ty,H+4.75),1.12,.7,M('#4A4E56',.6),seg=18,r2=.05)
        for z in (H+2.5,H+3.3,H+4.1): B.cyl((tx,ty,z),1.07,.05,metal,seg=18)
    # ground floor
    if shop:
        name,scol=shop; aw=M(scol,.85,kind='fabric')
        B.box((cx,yf+.06*s,1.65),(w/2-.4,.04,1.5),M('#2A1E16',.6),0)
        B.box((cx,yf+.03*s,1.85),(w/2-.6,.03,1.2),M('#FFE2B0',.5,emit=.9) if r.random()<.7 else glass,0)
        B.box((cx,yf-.02*s,1.85),(w/2-.6,.02,1.2),M('#BFD6E8',.05,spec=1.0,alpha=.35),0)
        for xx in (cx-w/2+.4,cx+w/2-.4): B.box((xx,yf-.04*s,1.65),(.08,.1,1.6),M('#2A1E16',.6),.01)
        B.box((cx+w/2-1.0,yf-.0*s,1.25),(.45,.06,1.15),M('#3A2A20',.5),.01); B.box((cx+w/2-.8,yf-.07*s,1.2),(.03,.03,.03),M('#D9B24A',.3,metal=.9),.0)
        n=max(4,int(w/.8))
        for k in range(n): B.box((cx-w/2+.4+(k+.5)*(w-.8)/n,yf-.75*s,3.05),((w-.8)/n/2,.85,.03),aw if k%2==0 else M(shade(scol,1.25),.85,kind='fabric'),.005,rot=(R(-20*s),0,0))
        B.box((cx,yf-1.55*s,2.72),(w/2-.4,.03,.18),aw,.005)
        sign_text(name,(cx,yf-1.6*s,2.66),.22,'#F4F1EA',n=(0,-s,0))
        B.box((cx,yf-.08*s,3.35),(w/2-.5,.06,.24),M('#1E2228',.6),.02); sign_text(name,(cx,yf-.16*s,3.25),.32,'#F2D46A',n=(0,-s,0),e=1.2)
    else:
        sx=cx+r.choice([-1,1])*(w/2-1.4)
        for k in range(6): B.box((sx,yf-(2.0-k*.3)*s,.12+k*.22),(.85,.3+.0,.12),M('#7A5A48',.8,kind='concrete') if col in ('#C9A27A','#D2B48C') else M(shade(col,.7),.85,kind='concrete'),.01)
        for d_ in (-.86,.86):
            B.box((sx+d_,yf-1.25*s,1.25),(.02,1.0,.02),metal,0,rot=(R(30*s),0,0))
            for j in range(5): B.box((sx+d_,yf-(2.1-j*.42)*s,.45+j*.25+.4),(.01,.01,.4),metal,0)
        B.box((sx,yf+.02*s,2.15),(.6,.06,.95),M('#3A2418',.4,kind='wood'),.02); B.box((sx,yf-.02*s,3.15),(.7,.06,.2),trim,.02)
        B.box((sx+.35,yf-.06*s,2.1),(.03,.03,.03),M('#D9B24A',.3,metal=.9),0)
        for xx in (cx-w/2+1.0,cx+w/2-1.0):
            if abs(xx-sx)>1.3: B.box((xx,yf-.03*s,2.2),(.5,.06,.7),trim,.02); B.box((xx,yf-.08*s,2.2),(.42,.03,.62),glass,0)
        B.box((cx,yf-.5*s,.35),(w/2-.2,.5,.35),M(shade(col,.6),.9,kind='concrete'),0)
        for k in range(int(w/.4)): B.box((cx-w/2+.3+k*.4,yf-1.0*s,.55),(.012,.012,.5),metal,0)
    return H

def street_lamp(x,y,side=1):
    gm=M('#2E4A3A',.4,metal=.5); B.cyl((x,y,2.4),.09,4.8,gm,seg=10); B.cyl((x,y,.2),.18,.4,gm,seg=10)
    B.box((x,y-.6*side,4.8),(.04,.6,.04),gm,0); B.cyl((x,y-1.15*side,4.7),.22,.25,gm,seg=10,r2=.1); B.cyl((x,y-1.15*side,4.55),.16,.06,M('#FFE7B8',.3,emit=2.0),seg=10)
def hydrant(x,y):
    rm=M('#C8372D',.45); B.cyl((x,y,.3),.13,.6,rm,seg=10); B.cyl((x,y,.66),.15,.12,rm,seg=10,r2=.06); B.box((x,y,.42),(.22,.06,.06),rm,.02)
def mailbox(x,y):
    bm=M('#2F5EA8',.4); B.box((x,y,.75),(.32,.3,.45),bm,.06); B.box((x,y,1.2),(.32,.3,.1),bm,.1)
    for dx in (-.25,.25): B.box((x+dx,y,.15),(.04,.25,.15),bm,0)
def trashcan(x,y):
    B.cyl((x,y,.45),.28,.9,M('#3A5A44',.5,metal=.3),seg=14); B.cyl((x,y,.92),.3,.06,M('#2A3A30',.5),seg=14)
def newsbox(x,y,col):
    B.box((x,y,.55),(.25,.22,.42),M(col,.5),.03); B.box((x,y-.23,.75),(.18,.01,.12),M('#E8ECF0',.1,spec=.9),0)
def bench(x,y,rz=0):
    wd=M('#6E4A2E',.7,kind='wood'); mt=M('#22252B',.4,metal=.6)
    B.box((x,y,.45),(.9,.22,.03),wd,.01,rot=(0,0,R(rz))); B.box((x,y+.22,.75),(.9,.03,.18),wd,.01,rot=(0,0,R(rz)))
    for dx in (-.8,.8): B.box((x+dx,y,.22),(.03,.2,.22),mt,0)
def street_clock(x,y,frozen=False):
    gm=M('#1F3A2E',.35,metal=.6); gold=M('#D9B24A',.3,metal=.9)
    B.cyl((x,y,2.0),.14,4.0,gm,seg=12); B.cyl((x,y,.15),.3,.3,gm,seg=12)
    hd=empty((x,y,4.6)); obox((0,0,0),(.62,.32,.62),gm,.1,hd)
    for s in (-1,1):
        ocyl((0,s*.33,0),.5,.02,M('#F4F1E4',.3,emit=.6),hd,rot=(R(90),0,0),seg=28); ocyl((0,s*.345,0),.53,.015,gold,hd,rot=(R(90),0,0),seg=28)
        for k in range(12): a=R(k*30); obox((.42*math.sin(a),s*.36,.42*math.cos(a)),(.02,.005,.05),M('#1B1B22',.5),0,hd,rot=(0,-a*s,0))
    obox((0,0,.75),(.12,.12,.15),gold,.04,hd)
    hands=[]
    for s in (-1,1):
        hh=empty((0,s*.37,0),hd); obox((0,0,.14),(.025,.004,.15),M('#1B1B22',.4),.0,hh); mh=empty((0,s*.375,0),hd); obox((0,0,.21),(.016,.004,.22),M('#1B1B22',.4),.0,mh)
        hands.append((hh,mh,s))
    return dict(head=hd,hands=hands)
def clock_set(C,tsec):  # tsec: clock time in seconds (hour hand slow)
    for hh,mh,s in C['hands']:
        hh.rotation_euler=(0,s*R(tsec/120*1.0+250),0); mh.rotation_euler=(0,s*R(tsec*6/10),0)

def taxi(loc,rotz,seed=0):
    V=car(loc,rotz,'#F2C21B',seed=99); root=V['root']
    obox((-.18,0,1.52),(.32,.12,.1),M('#FFF6D8',.3,emit=1.2),.03,root); sign_text('TAXI',(-.18,-.13,1.5),.12,'#1B1B22',n=(0,-1,0),parent=root)
    for s in (-1,1):
        for k in range(10): obox((-1.6+k*.34,s*.865,.62),(.085,.01,.05),M('#1B1B22' if k%2 else '#F4F1EA',.5),0,root)
    return V
def bus(loc,rotz):
    root=empty(loc,rot=(0,0,R(rotz))); bm=M('#2F6EA8',.35,metal=.2); wm=M('#F4F1EA',.4); gl=M('#1A2433',.06,spec=1.0); W=[]
    obox((0,0,1.75),(5.6,1.25,1.45),bm,.25,root); obox((0,0,.62),(5.62,1.27,.32),wm,.08,root)
    for s in (-1,1):
        obox((0,s*1.26,2.1),(5.1,.02,.6),gl,.02,root)
        for k in range(8): obox((-4.6+k*1.3,s*1.275,2.1),(.04,.01,.62),bm,0,root)
    obox((5.61,0,2.0),(.02,1.1,.9),gl,.02,root); obox((5.63,0,3.0),(.02,.9,.18),M('#1B1B22',.4),0,root); sign_text('42 MAPLE AVE',(5.66,0,2.94),.16,'#F2B21B',n=(1,0,0),e=1.5,parent=root)
    for sx in (-3.8,3.6):
        for sy in (-1.15,1.15): W.append(wheel((sx,sy,.52),.52,.3,root))
    return dict(root=root,wheels=W,r=.52)
def truck(loc,rotz,col='#E8E6E0',logo='SPEEDY MOVERS'):
    root=empty(loc,rot=(0,0,R(rotz))); bm=M(col,.45); cab=M('#C8372D',.35,metal=.3); gl=M('#1A2433',.06,spec=1.0); W=[]
    obox((-.9,0,2.0),(3.0,1.2,1.5),bm,.08,root); obox((3.0,0,1.35),(1.0,1.15,.95),cab,.15,root); obox((3.4,0,1.85),(.5,1.1,.45),gl,.08,root)
    obox((4.02,0,.9),(.05,1.0,.25),M('#C9CED8',.3,metal=.8),.03,root)
    for s in (-1,1): sign_text(logo,(-.9,s*1.22,2.2),.42,'#2F5EA8',n=(0,s,0),parent=root)
    for sx in (-2.8,-1.6,3.0):
        for sy in (-1.05,1.05): W.append(wheel((sx,sy,.5),.5,.3,root))
    return dict(root=root,wheels=W,r=.5)

def city(seed=1,ash=False,special=((1,4.0,SHOPS[0]),(1,-2.0,None)),clear=((1,-15,11),)):
    clr=lambda x,s: any(c[0]==s and c[1]<x<c[2] for c in clear)
    r=random.Random(seed)
    asph=M('#34363C',.85,kind='asphalt'); B.box((0,0,-.05),(150,4.5,.05),asph,0)
    side=M('#B8B2A8',.85,kind='concrete',sc=.5)
    for s in (-1,1):
        B.box((0,s*6.0,.07),(150,1.5,.07),side,0); B.box((0,s*4.52,.075),(150,.08,.08),M('#9A958C',.7,kind='concrete'),.01)
        for k in range(-75,76): B.box((k*2.0,s*6.0,.142),(.012,1.5,.004),M('#8E8A82',.9),0)
    for k in range(-37,38): B.box((k*4.0,0,.002),(1.0,.08,.003),M('#F2D46A',.6),0)
    for s in (-1,1): B.box((0,s*4.2,.002),(150,.06,.003),M('#EDEBE4',.6),0)
    for cx in (-18.0,20.0):
        for k in range(12): B.box((cx,-3.9+k*.71,.003),(1.6,.18,.004),M('#EDEBE4',.6),0)
    for x in (-9,6,27,-31): B.cyl((x,1.5 if x%2 else -1.6,.005),.4,.012,M('#4A4C52',.5,metal=.6),seg=16)
    for s in (-1,1):
        x=-70; i=0
        while x<70:
            w=r.choice([5.0,5.5,6.0,6.5,7.0,8.0]); fl=r.randint(3,5); col=r.choice(BRICK)
            shop=SHOPS[(i*5+(0 if s>0 else 7))%len(SHOPS)] if r.random()<.62 else None
            if shop and shop[0]==SHOPS[0][0]: shop=SHOPS[11]
            for sd,xc,sp_ in special:
                if sd==s and x<=xc<x+w: shop=sp_
            brownstone(x+w/2,w,fl,col,seed*100+i*7+(s>0),side=s,shop=shop,lit=.12 if ash else .22)
            x+=w; i+=1
        for x in range(-64,65,11):
            if not clr(x+(2 if s>0 else -3),s): street_lamp(x+(2 if s>0 else -3),s*4.85,side=s)
        for x in range(-60,61,14):
            if r.random()<.8 and not clr(x+5*s,s): tree(x+5*s,s*5.1,.95,r.choice(['#4F8A3A','#5E9A44','#467E36']),'#5A3E28'); B.box((x+5*s,s*5.1,.15),(.6,.6,.02),M('#5A4030',.9),0)
        for x in r.sample(range(-50,50,3),9):
            k=r.random()
            if clr(x,s): continue
            if k<.25: hydrant(x,s*4.75)
            elif k<.45: mailbox(x,s*4.85)
            elif k<.7: trashcan(x,s*4.8)
            elif k<.85: newsbox(x,s*4.8,r.choice(['#C8372D','#2F6EA8','#E8C24E']))
            else: bench(x,s*4.95)
    skyline_city(seed)
def skyline_city(seed):
    r=random.Random(seed+3)
    for s in (-1,1):
        for k in range(26):
            x=-120+k*9.5+r.uniform(-2,2); y=s*r.uniform(22,40); w=r.uniform(6,12); h=r.uniform(14,44)
            col=r.choice(['#8A96A8','#A8A6A0','#9AA4B0','#B8AFA0','#7E8898'])
            B.box((x,y,h/2),(w/2,w/2,h/2),M(col,.7,kind='concrete'),0)
            for z in range(4,int(h)-2,3): B.box((x,y-s*w/2-.02*s,z),(w/2-.4,.02,.6),M('#3A4658',.15,spec=.9),0)
            if r.random()<.25: B.box((x,y,h+1.5),(.08,.08,1.5),M('#9A9EA6',.5,metal=.6),0)
    # far end: clock tower + skyscrapers
    tw=M('#C9B48C',.8,kind='concrete'); B.box((115,0,22),(5,5,22),tw,0); B.box((115,0,46),(4,4,2.5),tw,.1); B.cyl((115,0,50),3.0,5,M('#4E7A6A',.5,metal=.3),seg=4,r2=.1)
    ocyl((110.0,0,40),3.0,.2,M('#F4F1E4',.3,emit=.8),None,rot=(0,R(90),0),seg=32)
    for k in range(6): B.box((140+r.uniform(-5,5),r.uniform(-30,30),r.uniform(20,40)),(r.uniform(5,8),r.uniform(5,8),r.uniform(20,40)),M(r.choice(['#8A96A8','#A8A6A0','#7E8898']),.7,kind='concrete'),0)
    for k in range(6): B.box((-140+r.uniform(-5,5),r.uniform(-30,30),r.uniform(20,40)),(r.uniform(5,8),r.uniform(5,8),r.uniform(20,40)),M(r.choice(['#8A96A8','#A8A6A0','#7E8898']),.7,kind='concrete'),0)

def mover_rig(x,side=1,Y=7.5,z=12.5):
    # beam out of a top window + pulley + rope, piano hangs below
    mt=M('#2A2C34',.45,metal=.6); s=side
    B.box((x,Y*s-1.2*s,z),(.12,1.4,.12),mt,.01); B.cyl((x,Y*s-2.5*s,z-.15),.18,.1,mt,seg=12,rot=(0,R(90),0))
    rope=obox((x,Y*s-2.6*s,z-1.0),(.02,.02,.85),M('#C9B48C',.8,kind='fabric'),0)
    return rope

def crash_field():
    g=M('#6FA048',.9,kind='grass',sc=.6); B.box((0,0,-.05),(200,200,.05),g,0)
    r=random.Random(4); hull=M('#E8ECF0',.35,metal=.3); blu=M('#2F5EA8',.4); win=M('#1A2433',.08,spec=1)
    root=empty((0,8,0),rot=(0,0,R(-25)))
    obox((-3.5,0,1.9),(4.0,1.8,1.8),hull,.8,root,rot=(0,R(-4),0)); obox((5.8,.8,1.6),(3.6,1.8,1.7),hull,.8,root,rot=(R(8),R(6),R(14)))
    for k in range(9): obox((-6.5+k*.9,-1.82,2.4),(.18,.02,.22),win,.05,root)
    obox((-3.5,-1.83,1.2),(4.0,.02,.12),blu,0,root)
    obox((1.5,-5.5,.4),(1.6,4.5,.12),hull,.08,root,rot=(R(10),0,R(-12))); obox((-8.2,0,3.6),(.9,.12,2.0),hull,.2,root,rot=(0,R(-20),0)); obox((-8.4,0,4.8),(.6,.13,.5),blu,.1,root)
    for k in range(14): obox((r.uniform(-12,14),r.uniform(-10,8),.15),(r.uniform(.2,.8),r.uniform(.2,.6),r.uniform(.05,.25)),hull if k%3 else M('#3A3C42',.6),.05,root,rot=(r.uniform(-.5,.5),r.uniform(-.5,.5),r.uniform(0,6)))
    for k in range(5): B.ico((r.uniform(-20,20),r.uniform(-4,30),.2),r.uniform(.6,1.4),M('#5A8A3A',.9,kind='leaves'),sub=1)
    for k in range(18): tree(r.uniform(-60,60),r.uniform(25,70),r.uniform(1.1,1.8),r.choice(['#4F8A3A','#5E9A44']),'#5A3E28')
    return root
def volcano_set():
    rk=M('#3A2E2A',.9,kind='concrete',sc=.4); lava=M('#FF6A1A',.4,emit=2.6); crust=M('#1E1816',.9,kind='concrete',sc=.6)
    B.box((0,0,-.05),(200,200,.05),crust,0)
    B.cyl((0,60,14),55,28,rk,seg=28,r2=12); B.cyl((0,60,29),12.5,2,M('#2A2220',.9),seg=28,r2=10)
    pool=ocyl((0,4,.02),5.5,.05,lava,None,rot=(0,0,0),seg=28)
    r=random.Random(7)
    for k in range(40):
        a=r.uniform(0,6.28); d=r.uniform(5.6,7.5); B.ico((math.cos(a)*d,4+math.sin(a)*d,.2),r.uniform(.4,1.0),rk,sc=(1,1,.6),sub=1)
    for k in range(6): B.box((r.uniform(-30,30),60+r.uniform(-40,-15),r.uniform(2,10)),(.6,8,.08),lava,0,rot=(R(r.uniform(15,30)),0,R(r.uniform(-30,30))))
    for k in range(30): B.ico((r.uniform(-40,40),r.uniform(-10,40),.3),r.uniform(.3,1.8),rk,sc=(1,1,.7),sub=1)
    return pool
def kitchen():
    wl=M('#F2E6C8',.85,kind='wall'); fl=M('#C9B08A',.8,kind='tile',h2='#B89C78',sc=1.5); cab=M('#7FA8C9',.55); top=M('#EDEBE4',.3)
    B.box((0,0,-.05),(5,5,.05),fl,0); B.box((0,3.0,1.6),(5,.1,1.6),wl,0); B.box((-3.2,0,1.6),(.1,5,1.6),wl,0)
    B.box((0,2.6,.45),(2.6,.35,.45),cab,.02); B.box((0,2.6,.93),(2.65,.4,.04),top,.01); B.box((0,2.8,2.3),(2.4,.2,.4),cab,.02)
    for k in range(5): B.box((-2.1+k*1.05,2.24,.45),(.48,.02,.38),M(shade('#7FA8C9',1.15),.5),.01); B.cyl((-2.1+k*1.05,2.2,.7),.03,.03,M('#D9B24A',.3,metal=.9),rot=(R(90),0,0))
    B.box((1.5,2.6,1.05),(.5,.3,.1),M('#C9CED8',.3,metal=.8),.02); B.box((-1.2,2.75,1.2),(.25,.15,.28),M('#E8554D',.4),.05)
    B.box((-3.1,0,1.9),(.02,.9,.7),M('#BFE0FF',.2,emit=1.2),0)
    for k in range(6): B.box((-3.08,-.9+k*.36,1.9),(.02,.02,.72),M('#F4F1EA',.5),0)
    B.box((1.0,-.2,.75),(.8,.6,.04),M('#8A5A3A',.5,kind='wood'),.02)
    for dx in (-.7,.7):
        for dy in (-.5,.5): B.box((1.0+dx,-.2+dy,.37),(.04,.04,.37),M('#8A5A3A',.5),0)
    B.cyl((1.0,-.2,.86),.22,.18,M('#F4F1EA',.4),seg=14); B.ico((.6,0,.85),.12,M('#E8554D',.6),sub=1)
    for k in range(4): B.box((-2.6+k*.5,2.95,2.0+.0),(.18,.02,.24),M(random.Random(k).choice(['#E8554D','#F2C14E','#6FC38A','#4D8FE8']),.5),.01)
    return None
