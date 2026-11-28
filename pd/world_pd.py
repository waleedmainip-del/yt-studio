# Worlds for "Pindi vs the Dinosaur". All sets are new for this film:
#   isb()     Islamabad avenue running north (+y) to the Margalla hills: cafe terrace (west), check post (east), jacaranda + pine trees
#   pindi()   Rawalpindi night street under the elevated bus track: chai dhaba, bike works, neon signs
#   hiway()   night road between the two cities        office()  mamu's meeting room
MOODS['pd_gold']=dict(sun=(70,-58),e=2.7,col=(1,.8,.55),top='#4C7CCB',bot='#FFCB96',sky=.92,mist='#F0CDA8',cloud='#FFDDBE',cov=.45,cstr=.85)
MOODS['pd_dusk']=dict(sun=(77,-64),e=2.1,col=(1,.7,.5),top='#3F4A9E',bot='#FFAE7E',sky=.85,mist='#CFA08E',cloud='#F4A8A0',cov=.45,cstr=.85)
MOODS['pd_night']=dict(sun=(52,-150),e=.75,col=(.6,.7,1.0),top='#050818',bot='#1C2850',sky=.6,mist='#161E3A',cloud='#232C52',cov=.35,cstr=.6)
MOODS['pd_pindi']=dict(sun=(50,-150),e=1.1,col=(.62,.72,1.0),top='#080C28',bot='#2A2F66',sky=1.1,mist='#1A2040',cloud='#262E58',cov=.35,cstr=.6)
MOODS['pd_day']=dict(sun=(54,-40),e=3.0,col=(1,.94,.82),top='#3A8CE4',bot='#D6ECFF',sky=.95,mist='#DCE8F2',cloud='#FFFFFF',cov=.5,cstr=.9)
MOODS['pd_in']=dict(sun=(60,-160),e=.4,col=(1,.9,.8),top='#101018',bot='#1A1A24',sky=.3,mist='#1A1A24',cloud='#20202A',cov=.3,cstr=.5)
def spotd(loc,e,col,size=80,blend=.6,shadow=True,r=.5):
    bpy.ops.object.light_add(type='SPOT',location=loc); p=bpy.context.object; p.data.energy=e; p.data.color=col; p.data.spot_size=R(size); p.data.spot_blend=blend
    p.data.shadow_soft_size=r; p.data.use_shadow=shadow; return p
GRN=['#3F7A3A','#4F8A3A','#356E34','#467F38']; JAC=['#9A7AD8','#B08AE8','#8466C8','#A27CDC']
def pine(x,y,s=1.0,z=0.0,col='#2F6A3A'):
    B.cyl((x,y,z+1.0*s),.16*s,2.0*s,M('#5A4030',.85),seg=6)
    for k in range(4): B.cyl((x,y,z+(2.0+k*1.25)*s),(1.55-.33*k)*s,1.9*s,M(shade(col,1-.06*k),.9,kind='leaves'),seg=7,r2=.05*s)
def jac(x,y,s=1.0,seed=0):
    r=random.Random(seed); B.cyl((x,y,1.6*s),.17*s,3.2*s,M('#5E4636',.85),seg=7)
    for k in range(8): a=k*.8+r.uniform(0,.5); rr=r.uniform(.2,1.25)*s; B.ico((x+math.cos(a)*rr,y+math.sin(a)*rr,(3.5+r.uniform(0,1.5))*s),r.uniform(.85,1.3)*s,M(r.choice(JAC),.85,kind='leaves'),sub=1)
def rtree(x,y,s=1.0,seed=0,z=0.0):
    r=random.Random(seed); B.cyl((x,y,z+1.3*s),.17*s,2.6*s,M('#6B4A2E',.85),seg=7)
    for k in range(7): a=k*.9+r.uniform(0,.5); rr=r.uniform(.2,1.1)*s; B.ico((x+math.cos(a)*rr,y+math.sin(a)*rr,z+(3.0+r.uniform(0,1.4))*s),r.uniform(.9,1.35)*s,M(r.choice(GRN),.85,kind='leaves'),sub=1)
def ilamp(x,y,h=8.6):
    pm=M('#E4E7EC',.4,metal=.4); B.cyl((x,y,h/2),.12,h,pm,seg=8,r2=.08); B.cyl((x,y,.25),.2,.5,M('#9AA0A8',.5),seg=8)
    for a in (1,-1): B.box((x+a*1.15,y,h-.05),(1.15,.05,.04),pm,0); B.box((x+a*2.2,y,h-.12),(.5,.2,.06),M('#C9CED8',.4),.03); B.box((x+a*2.2,y,h-.19),(.42,.15,.02),lit('#FFE9B8',9.0),0)
def flowers(x0,x1,y0,y1,n,seed,z=.3):
    r=random.Random(seed)
    for k in range(n): B.ico((r.uniform(x0,x1),r.uniform(y0,y1),z+r.uniform(0,.12)),r.uniform(.1,.17),M(r.choice(['#F2C14E','#E8554D','#F28AA0','#FFFFFF','#B08AE8','#FF8A1E']),.7),sub=1)
def iblock(x,y,w,d,fl,col,side,seed,sg=None,sgc='#27365A'):
    """modern Islamabad block: w along the avenue (y), d deep (x). side=+1 east of the road (front faces -x), -1 west"""
    r=random.Random(seed); h=fl*3.3+.6; fx=x-side*d; wl=M(col,.85,kind='wall'); gl=M('#2A3F5A',.15,spec=1.0); wh=M('#F6F4EE',.7)
    B.box((x,y,h/2),(d,w,h/2),wl,0); B.box((x,y,h+.2),(d+.15,w+.15,.2),wh,0)
    for f in range(fl):
        z=1.9+f*3.3
        if f==0:
            B.box((fx-side*.03,y,1.6),(.04,w-.5,1.25),gl,0)
            for k in range(int(w//2.4)+1): B.box((fx-side*.06,y-w+.5+k*(2*w-1)/max(1,int(w//2.4)),1.6),(.06,.07,1.3),wh,0)
            B.box((fx-side*.75,y,3.05),(.75,w-.2,.07),M(r.choice(['#2F5D50','#7A1F2E','#27365A','#C9A27A']),.8,kind='fabric'),.02)
        else:
            B.box((fx-side*.03,y,z+.1),(.04,w-.7,.85),gl,0); B.box((fx-side*.1,y,z-.85),(.12,w-.3,.09),wh,0)
            nk=int(w//1.6)
            for k in range(nk+1):
                yy=y-w+.7+k*(2*w-1.4)/max(1,nk); B.box((fx-side*.07,yy,z+.1),(.07,.06,.9),wh,0)
                if k<nk and r.random()<.5: B.box((fx-side*.05,yy+(w-.7)/max(1,nk),z+.1),(.02,(w-.7)/max(1,nk)-.12,.78),lit('#FFE2A0',2.2),0)
    if r.random()<.6: B.box((x+side*r.uniform(-d/3,d/3),y+r.uniform(-w/3,w/3),h+1.0),(1.0,1.2,.6),M('#C9CED8',.5,metal=.3),.05)
    if sg: sign(sg,(fx-side*.12,y,3.95),.42,'#FFFFFF',sgc,n=(-side,0,0),e=2.0,pad=.22)
def cafe_table(x,y,um=None,tall=False):
    wd=M('#8A5A36',.6,kind='wood',sc=.6); ch=M('#2A2C34',.4,metal=.5); h=1.25 if tall else .86
    B.cyl((x,y,h/2),.05,h,ch,seg=8); B.cyl((x,y,.03),.3,.06,ch,seg=12); B.cyl((x,y,h+.03),.62 if not tall else .5,.06,wd,seg=18)
    if um:
        B.cyl((x,y,2.0),.035,4.0,M('#E8EAEE',.4,metal=.5),seg=6)
        for k in range(8): a=k*pi/4; B.box((x+math.cos(a)*.95,y+math.sin(a)*.95,3.75),(1.0,.42,.03),M(um if k%2==0 else '#F6F4EE',.8,kind='fabric'),.0,rot=(0,R(14),a))
    if not tall:
        for a in (0,pi*2/3,pi*4/3):
            cx=x+math.cos(a+.5)*1.1; cy=y+math.sin(a+.5)*1.1; B.box((cx,cy,.56),(.24,.24,.03),M('#F4F1EA',.6),.02); B.box((cx+math.cos(a+.5)*.23,cy+math.sin(a+.5)*.23,.9),(.03,.24,.32),M('#F4F1EA',.6),.02,rot=(0,0,a+.5))
            for dx in (-.19,.19):
                for dy in (-.19,.19): B.cyl((cx+dx,cy+dy,.27),.018,.54,ch,seg=5)
def bench(x,y,rz=0):
    wd=M('#9A6A3E',.6,kind='wood',sc=.6); c=math.cos(R(rz)); s=math.sin(R(rz))
    B.box((x,y,.55),(1.0,.26,.04),wd,.02,rot=(0,0,R(rz))); B.box((x+s*.26,y-c*.26,.95),(1.0,.03,.24),wd,.02,rot=(0,0,R(rz)))
    for k in (-1,1): B.box((x+c*k*.85,y+s*k*.85,.27),(.04,.24,.27),M('#2A2C34',.4,metal=.5),.01,rot=(0,0,R(rz)))
def dustbin(x,y): B.cyl((x,y,.5),.26,1.0,M('#2E8A4A',.5),seg=10); B.cyl((x,y,1.03),.28,.06,M('#1F6A36',.5),seg=10)
BARR={}
def isb(mood='pd_gold',night=0.0,post=True,arm=True,stars=False):
    """avenue along y. carriageways x 2..9.5 (east, the dino side) and -9.5..-2 (west). median -2..2. walks 9.5..14. cafe terrace west at y -9..3. check post east at y=16"""
    NIGHT[0]=night; S=setup_world(mood,shadow=95); r=random.Random(7); BARR.clear()
    B.box((0,60,-.1),(260,260,.1),M('#4A9444',.95,kind='grass',sc=2.0),0)
    asp=M('#35363C',.92,kind='asphalt',sc=1.4); kb=M('#D8D4CA',.8,kind='concrete',sc=.5); pv=M('#D9C8AE',.85,kind='tile',sc=.8); wl=M('#F4F1EA',.6); yl=M('#F2C14E',.6)
    B.box((0,30,-.02),(9.5,190,.06),asp,0)
    B.box((0,30,.14),(2.0,190,.14),kb,.03); B.box((0,30,.3),(1.75,190,.03),M('#4E9A46',.95,kind='grass',sc=.7),0)
    for s in (1,-1):
        B.box((s*11.75,30,.1),(2.25,190,.1),pv,0); B.box((s*9.6,30,.12),(.12,190,.12),kb,.02)
        B.box((s*2.25,30,.045),(.07,190,.005),yl,0); B.box((s*9.3,30,.045),(.07,190,.005),wl,0)
        for k in range(-40,56): B.box((s*5.75,k*4.0,.045),(.07,1.0,.005),wl,0)
    for k in range(-11,16):
        y=k*14.0+7; ilamp(0,y)
        if night>0 and -30<y<60: point((0,y,7.6),900*night,(1,.86,.62),r=.5,shadow=False)
    for k in range(-26,36):
        y=k*5.6
        if abs(y-16)<4: continue
        flowers(-1.4,1.4,y-.9,y+.9,7,k+100)
        if k%3==0: B.ico((0,y+2.6,.75),.62,M(GRN[k%4],.85,kind='leaves'),sc=(1.5,1.1,.9),sub=1)
    # trees along the walks: jacaranda + pine + round, never the same twice in a row
    for s in (1,-1):
        for k in range(-18,24):
            y=k*8.2+(2.0 if s>0 else -1.5)
            if s<0 and -10<y<4: continue
            if s>0 and 12<y<21: continue
            kind=(k+(0 if s>0 else 1))%3; x=s*12.9
            B.box((x,y,.22),(.7,.7,.04),M('#5A4636',.9),0)
            if kind==0: jac(x,y,r.uniform(1.25,1.5),seed=k*3+s)
            elif kind==1: pine(x,y,r.uniform(1.15,1.4))
            else: rtree(x,y,r.uniform(1.25,1.5),seed=k*5+s)
        for k in range(-12,16):
            y=k*11.5+5
            if s<0 and -12<y<6: continue
            if s>0 and 11<y<22: continue
            (bench(s*10.6,y,90*s) if k%2==0 else dustbin(s*10.3,y))
        B.box((s*14.6,30,.5),(.35,190,.5),M('#3F7A3A',.9,kind='leaves'),.12)
    # blocks both sides
    WC=['#F4EFE4','#EDE4D2','#F6F4EE','#E6DCC8','#F1E8DA','#DDE4E8']; SG=[('BLUE AREA PLAZA','#27365A'),None,('CAPITAL PHARMACY','#1E6A3A'),None,('GREEN LEAF BAKERS','#7A1F2E'),None,('F-7 BOOKS','#3A3A44'),None]
    for s in (1,-1):
        y=-150.0; k=0
        while y<120:
            w=r.uniform(7,11); fl=r.choice([3,4,4,5,6]); d=r.uniform(6,9)
            if not (s<0 and -13<y+w<7 and y-w< 7) :
                sg=SG[(k+(3 if s<0 else 0))%8]
                if s>0 and 8<y<26: sg=None
                iblock(s*(17.5+d),y+w,w,d,fl,WC[(k+s)%6],s,int(k*7+s*3+50),sg[0] if sg else None,sg[1] if sg else '#27365A')
            y+=2*w+r.uniform(2.5,5); k+=1
            if r.random()<.7: (pine if k%2 else rtree)(s*(17.2+r.uniform(0,2)),y-1.6,r.uniform(1.3,1.7))
        for k in range(26):
            x=s*r.uniform(40,120); yy=r.uniform(-150,120); w=r.uniform(5,10); h=r.uniform(8,26); B.box((x,yy,h/2),(w,w,h/2),M(r.choice(WC),.9,kind='wall'),0)
            for f in range(int(h//3.3)): B.box((x-s*(w+.02),yy,1.9+f*3.3),(.03,w-.6,.8),M('#2A3F5A',.2),0)
        for k in range(60): (pine if k%3 else rtree)(s*r.uniform(27,130),r.uniform(-150,125),r.uniform(1.4,2.3))
    # cafe (west): facade x=-17, terrace on the walk
    B.box((-21.5,-3,3.9),(4.5,9.5,3.9),M('#F1E8DA',.85,kind='wall'),0); B.box((-21.5,-3,7.95),(4.7,9.7,.18),M('#2F5D50',.6),0)
    B.box((-16.97,-3,1.7),(.05,8.6,1.45),M('#2A3F5A',.12,spec=1.0),0); B.box((-16.2,-3,3.3),(.85,9.2,.07),M('#2F5D50',.8,kind='fabric'),.02); B.box((-15.38,-3,3.14),(.03,9.2,.14),M('#F6F4EE',.8,kind='fabric'),0)
    for k in range(7): B.box((-16.93,-11.4+k*2.8,1.7),(.07,.08,1.5),M('#F6F4EE',.7),0)
    sign('CAFE MARGALLA',(-16.9,-3,5.2),.62,'#F6F4EE','#2F5D50',n=(1,0,0),e=2.5,pad=.3)
    B.box((-16.85,-3,.4),(.22,9.0,.4),M('#8A5A36',.7,kind='wood'),.03); flowers(-17.0,-16.7,-11.5,5.5,46,5,z=.86)
    cafe_table(-12.2,-7.2,'#2F5D50'); cafe_table(-13.3,1.4,'#2F5D50'); cafe_table(-11.6,-2.6,tall=True)
    for k in range(9):
        if k in (3,4,5,6): continue
        yy=-9.3+k*1.45; B.box((-10.0,yy,.38),(.3,.55,.38),M('#F6F4EE',.7),.04); B.ico((-10.0,yy,.95),.42,M(GRN[k%4],.85,kind='leaves'),sc=(.8,1.2,.75),sub=1)
    flowers(-10.2,-9.8,-9.8,-5.9,10,9,z=1.2); flowers(-10.2,-9.8,.3,2.8,8,10,z=1.2)
    B.box((-14.6,3.3,1.0),(.05,.5,1.0),M('#2A2C34',.6),.02); sign('ICED LATTE  950',(-14.52,3.3,1.3),.2,'#F6F4EE','#2A2C34',n=(1,0,0),pad=.14,th=.04)
    for k in range(14):
        yy=-11.5+k*1.25; B.ico((-13.0+.25*math.sin(k*1.3),yy,3.95-.2*abs(math.sin(k*.9))),.07,lit('#FFE2A0',6.0,always=True),sub=1)
    # check post (east carriageway)
    if post:
        B.box((11.3,16,1.3),(1.1,1.1,1.3),M('#F6F4EE',.7),.04); B.box((11.3,16,.5),(1.12,1.12,.14),M('#27365A',.6),0); B.box((11.3,16,2.72),(1.4,1.4,.12),M('#27365A',.6),.03)
        B.box((10.18,16,1.75),(.03,.7,.45),M('#2A3F5A',.12,spec=1.0),0); sign('CHECK POST',(11.3,14.82,2.2),.24,'#FFFFFF','#27365A',n=(0,-1,0),pad=.14,th=.05)
        B.box((9.85,17.3,.65),(.16,.16,.65),M('#C8372D',.5),.02); B.box((2.15,17.3,.55),(.1,.1,.55),M('#C9CED8',.4,metal=.6),.02)
        e=empty((9.85,17.3,1.3)); BARR['arm']=e
        for k in range(10): obox((-.39-k*.78,0,0),(.39,.06,.09),M('#C8372D' if k%2==0 else '#F6F4EE',.5),.0,e)
        obox((.45,0,0),(.4,.14,.14),M('#3A3D44',.5),.03,e)
        if not arm: e.location=(0,0,-60)
        for k in range(5): B.cyl((2.6+k*1.6,19.2,.38),.2,.76,M('#FF8A1E',.5),seg=8,r2=.07); B.cyl((2.6+k*1.6,19.2,.44),.14,.12,M('#F6F4EE',.5),seg=8,r2=.11)
    # gantry sign far down the avenue
    for s in (1,-1): B.cyl((s*10.2,-46,4.2),.2,8.4,M('#C9CED8',.4,metal=.5),seg=8)
    B.box((0,-46,8.3),(10.4,.15,.15),M('#C9CED8',.4,metal=.5),0)
    sign('RAWALPINDI  12 km',(5.75,-46.2,7.2),.62,'#FFFFFF','#1E6A3A',n=(0,1,0),e=1.5,pad=.3,frame='#F6F4EE')
    sign('MARGALLA HILLS',(-5.75,-45.8,7.2),.62,'#FFFFFF','#1E6A3A',n=(0,-1,0),e=1.5,pad=.3,frame='#F6F4EE')
    # the hills + white mosque
    for (cx,cy,sx,sy,sz,c) in ((-70,215,95,34,40,'#3C7440'),(40,225,110,36,52,'#356A3A'),(140,212,80,30,38,'#3C7440'),(-150,235,90,34,46,'#2F6236'),(0,265,170,40,70,'#2C5C34'),(-90,290,150,40,84,'#27552F'),(110,295,150,40,78,'#27552F'),(20,172,46,13,13,'#427C44')):
        B.ico((cx,cy,-2),1.0,M(c,.95,kind='leaves',sc=3.0),sc=(sx,sy,sz),sub=3)
    for k in range(150):
        cx=r.uniform(-160,190); cy=r.uniform(182,232); zz=20+r.uniform(-6,10)
        pine(cx,cy,r.uniform(2.2,3.6),z=zz-12,col=r.choice(['#2A5E34','#2F6A3A','#25552F']))
    for k in range(34):
        a=r.uniform(-1,1); cx=20+a*40; cy=166+r.uniform(-4,3); zz=10.5*(1-a*a)**.5; (pine if k%3 else rtree)(cx,cy,r.uniform(.8,1.2),z=zz-1.5)
    mw=M('#F6F4EE',.5)
    B.cyl((-64,150,9),24,18,mw,seg=8,r2=1.5); B.box((-64,150,1.5),(25,25,1.5),mw,0); B.cyl((-64,150,19.5),.5,3,M('#E6B93A',.3,metal=.8),seg=6,r2=.05)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((-64+sx*27,150+sy*27,21),1.5,42,mw,seg=8,r2=.9); B.cyl((-64+sx*27,150+sy*27,45),.9,6,M('#E6B93A',.3,metal=.8),seg=8,r2=.05)
    if stars:
        for k in range(160): a=r.uniform(0,6.283); el=r.uniform(.12,1.2); d=420; B.ico((d*math.cos(a)*math.cos(el),60+d*math.sin(a)*math.cos(el),d*math.sin(el)),r.uniform(.5,1.2),M('#FFFFFF',.3,emit=6.0),sub=1)
        B.ico((-150,330,210),20,M('#FFF6D8',.3,emit=3.5),sub=3)
    B.done('isb'); return S
# ================================================================ Rawalpindi street (night)
PSHOP=[('RAJA MOBILE ZONE','#1E4FA8','mob'),('USTAD BIKE WORKS','#C8232B','bike'),('PINDI TIKKA HOUSE','#E6701E','tikka'),('CHACHA CHAI HOTEL','#1E6A3A','chai'),('BISMILLAH PUNCTURE','#16171C','tyre'),('SATELLITE PAAN','#7A1F7A','paan'),
       ('SHAHEEN CLOTH','#B8862A','cloth'),('AL-MADINA BAKERY','#7A1F2E','mob'),('BABA BATTERY','#2B58C9','tyre'),('RAJA BAZAAR SWEETS','#C8372D','cloth'),('KASHMIR NAAN','#2F5D50','tikka'),('NEW PINDI MEDICOS','#1E6A3A','mob')]
PWALL=['#D8C4A0','#C9A27A','#B8A890','#E0C8A8','#C8B8A8','#D4B48C','#BFB5A2','#CDAE8E']
def pshop(cx,side,w,fl,name,col,kind,seed,light=True):
    """shop house: front at y=side*11.5 facing the road. w = half width"""
    r=random.Random(seed); s=side; fy=s*11.5; d=4.5; cy=fy+s*d; wc=PWALL[seed%8]; wl=M(wc,.9,kind='wall'); h=fl*3.2+3.6; n=(0,-s,0); dk=M('#22242B',.7)
    B.box((cx,cy,h/2),(w,d,h/2),wl,0); B.box((cx,cy,h+.15),(w+.1,d+.1,.15),M(shade(wc,.8),.9),0)
    B.box((cx,fy+s*1.4,1.55),(w-.25,1.4,1.55),M('#17181C',.9),0)                                   # dark open shop mouth
    B.box((cx,fy+s*.15,3.3),(w-.1,.2,.2),M('#6E7378',.5,metal=.5),0)                                # shutter box
    sign(name,(cx,fy-s*.2,4.15),.44 if len(name)<17 else .38,'#FFFFFF',col,n=n,e=3.0,pad=.24,w=min(w-.5,len(name)*.16) if len(name)*.345*.44+.24>w else None)
    B.box((cx,fy-s*.9,3.05),(w-.1,.9,.05),M(shade(col,.8),.8,kind='fabric'),.01,rot=(R(-s*10),0,0))
    if light: B.box((cx,fy+s*.3,2.95),(w*.7,.04,.04),lit('#F4F8FF',9.0),0)
    for f in range(fl):
        z=5.6+f*3.2
        for k in (-1,1):
            lt_=r.random()<.55; B.box((cx+k*w*.45,fy-s*.02,z),(w*.26,.05,.75),lit(r.choice(['#FFD890','#FFE9B8','#BFE6FF']),2.4) if lt_ else M('#27303C',.3),0); B.box((cx+k*w*.45,fy-s*.06,z-.85),(w*.3,.1,.06),M(shade(wc,.75),.8),0)
        if r.random()<.6: B.box((cx,fy-s*.55,z-.75),(w-.3,.55,.06),M(shade(wc,.7),.9),0); B.box((cx,fy-s*1.08,z-.3),(w-.3,.03,.42),M('#3A3D44',.5,metal=.4),0)
        if r.random()<.5: B.box((cx+r.uniform(-w*.6,w*.6),fy-s*.3,z-1.2),(.45,.28,.3),M('#D8DCE2',.5),.03)
    B.cyl((cx+r.uniform(-w/2,w/2),cy,h+1.0),.7,1.4,M(r.choice(['#2B58C9','#16171C','#E8E2D0']),.6),seg=10)
    y0=fy-s*.6
    if kind=='bike':
        for k in range(4): B.cyl((cx-w*.6+k*.5,y0,.34+.14*(k%2)),.34,.14,M('#141418',.8),rot=(R(90),0,0),seg=14)
        B.box((cx+w*.5,y0-s*.2,.5),(.5,.35,.5),M('#C8232B',.5,metal=.3),.04); B.box((cx+w*.5,y0-s*.2,1.05),(.55,.4,.05),M('#3A3D44',.5,metal=.5),.01)
    elif kind=='tyre':
        for k in range(5): B.cyl((cx-w*.5,y0,.14+k*.26),.42,.24,M('#141418',.85),seg=14)
        for k in range(3): B.cyl((cx+w*.4+k*.3,y0,.42),.42,.2,M('#141418',.85),rot=(R(90),0,R(20)),seg=14)
    elif kind=='tikka':
        B.box((cx,y0,.55),(1.3,.4,.55),M('#3A3D44',.6,metal=.4),.03); B.box((cx,y0,1.12),(1.25,.36,.03),lit('#FF6A1E',6.0,always=True),0)
        for k in range(7): B.cyl((cx-1.0+k*.33,y0,1.2),.02,.9,M('#C9CED8',.3,metal=.8),rot=(R(90),0,0),seg=5); B.box((cx-1.0+k*.33,y0,1.2),(.05,.25,.05),M('#8A3A1E',.7),.02)
    elif kind=='cloth':
        for k in range(5): B.box((cx-w*.6+k*w*.3,y0+s*.4,1.9),(.3,.05,.9),M(r.choice(['#E8554D','#F2C14E','#35975A','#7448C2','#16909E','#F28AA0']),.85,kind='fabric'),.02)
    elif kind=='paan':
        B.box((cx,y0,.6),(.9,.4,.6),M('#7A1F7A',.6),.03)
        for k in range(8): B.cyl((cx-.7+k*.2,y0-s*.1,1.32),.07,.22,M(r.choice(['#E8554D','#F2C14E','#35975A','#2B58C9']),.4),seg=8)
    elif kind=='mob':
        B.box((cx,y0+s*.3,.55),(w*.7,.3,.55),M('#E8EAEE',.4),.03); B.box((cx,y0+s*.3,1.14),(w*.68,.28,.04),M('#BFE6F2',.1,spec=1.0,alpha=.4),0)
        for k in range(6): B.box((cx-w*.5+k*w*.2,y0+s*.3,1.2),(.06,.1,.012),lit(r.choice(['#7AD0FF','#FFFFFF','#FF9AC8']),2.0,always=True),0)
def bulbs(x0,x1,y,z,n,seed,sag=.6,cols=('#FFE2A0',)):
    r=random.Random(seed)
    for k in range(n+1):
        a=k/n; B.ico((L(x0,x1,a),y,z-sag*4*a*(1-a)),.09,lit(cols[k%len(cols)],7.0,always=True),sub=1)
def pindi(mood='pd_pindi',night=1.0,dhaba=True,cup=False):
    """street along x. bus track over the median (y -2.6..2.6, deck z 7.6+). lanes y 2.6..9 (north) and -9..-2.6. walks out to +-11.5.
    dhaba = CHACHA CHAI HOTEL, north side, x -4.6..4.6: open front, counter at y 12.4, tables on the walk"""
    NIGHT[0]=night; S=setup_world(mood,shadow=70); r=random.Random(23)
    B.box((0,0,-.1),(140,60,.1),M('#2E2F34',.92,kind='asphalt',sc=1.5),0)
    for k in range(40): B.box((r.uniform(-60,60),r.choice((-1,1))*r.uniform(3,8.6),.012),(r.uniform(.5,1.6),r.uniform(.4,1.0),.006),M(r.choice(['#26272B','#38393F']),.95),0)
    for s in (1,-1):
        B.box((0,s*10.25,.09),(140,1.25,.09),M('#8A8078',.9,kind='tile',sc=.7),0); B.box((0,s*9.0,.1),(140,.1,.1),M('#B8B2A6',.8),0)
        for k in range(-30,31): B.box((k*4.2,s*5.8,.012),(.9,.06,.005),M('#D8D4CA',.7),0)
    cc=M('#B4B0A6',.9,kind='concrete',sc=.8); cd=M('#9A968C',.9,kind='concrete',sc=.8)
    B.box((0,0,.2),(140,1.1,.2),cd,.03)
    for k in range(-5,6):
        x=k*14.0+7; B.box((x,0,3.75),(.85,.85,3.75),cc,.12); B.box((x,0,7.2),(1.3,2.7,.45),cc,.1)
        for sy in (-1,1): B.box((x,sy*.87,1.2),(.5,.02,.5),M(r.choice(['#C8372D','#F2C14E','#1E6A3A','#F4F1EA']),.8),0)       # posters on the pillars
    B.box((0,0,8.1),(140,3.3,.5),cc,.05)
    for sy in (-1,1): B.box((0,sy*3.25,9.0),(140,.1,.5),cd,.02); B.box((0,sy*3.36,8.75),(140,.02,.14),M('#C8372D',.5),0); B.box((0,sy*3.22,7.56),(140,.05,.05),lit('#FFE2A0',5.0),0)
    for k in range(-9,10):
        x=k*7.3; i=(k+9)%12; nm,col,kind=PSHOP[i]
        if dhaba and abs(x)<5: continue
        pshop(x,1,3.45,2+(k%3==0)+(k%4==1),nm,col,kind,100+k)
    for k in range(-9,10):
        x=k*7.3+2.0; i=(k+15)%12; nm,col,kind=PSHOP[i]; pshop(x,-1,3.45,2+(k%2)+(k%5==0),nm,col,kind,300+k,light=(k%2==0))
    for k in range(60):
        x=r.uniform(-75,75); y=r.choice((-1,1))*r.uniform(24,60); w=r.uniform(3,6); h=r.uniform(8,20); B.box((x,y,h/2),(w,w,h/2),M(r.choice(PWALL),.9,kind='wall'),0)
        for f in range(int(h//3.2)):
            if r.random()<.5: B.box((x+r.uniform(-w*.5,w*.5),y-(w+.03)*(1 if y>0 else -1),2+f*3.2),(.5,.03,.6),lit('#FFD890',2.0),0)
    # poles + wires + bulb strings + bunting
    for k in range(-6,7):
        for s in (1,-1): pole(k*12.0+3,s*9.6,8.6)
    for s in (1,-1): wires(-70,70,s*9.6,s*11.3,7.4,26,int(40+s))
    wires(-70,70,-3.4,-9.6,7.3,14,59)
    for k in range(-5,6): bulbs(k*12.0+3,k*12.0+15,9.4,6.4,11,k,cols=('#FFE2A0','#FF9AC8','#9AE8FF','#B8FF9A')); bulbs(k*12.0+3,k*12.0+15,-9.4,6.2,9,k+30)
    fl=[M(c,.8,kind='fabric') for c in ('#C8372D','#F2C14E','#1E6A3A','#F4F1EA','#2B58C9')]
    for k in range(-4,5):
        for j in range(12): a=j/11; B.box((k*14.0+7,-L(3.4,9.5,a),7.0-.5*4*a*(1-a)),(.02,.16,.2),fl[(j+k)%5],0)
    if dhaba:
        wc=M('#C9B48A',.9,kind='wall'); wd=M('#7A5A3A',.8,kind='wood',sc=.6)
        B.box((0,18.4,5.2),(4.6,.2,5.2),wc,0); B.box((0,15,10.3),(4.7,3.6,.15),M(shade('#C9B48A',.8),.9),0); B.box((0,15,3.5),(4.6,3.4,.1),M('#8A8274',.9),0)
        for sx in (-1,1): B.box((sx*4.5,15,5.2),(.12,3.4,5.2),wc,0)
        B.box((0,11.6,7.0),(4.6,.15,3.4),wc,0)
        for k in (-1,1): B.box((k*2.1,11.5,7.3),(1.0,.05,.8),lit('#FFD890',2.4),0)
        sign('CHACHA CHAI HOTEL',(0,11.3,4.35),.5,'#FFFFFF','#1E6A3A',n=(0,-1,0),e=3.0,pad=.26,frame='#F2C14E')
        B.box((0,18.25,2.2),(4.4,.03,1.2),M('#2E6A6A',.7),0); B.box((0,12.1,3.3),(3.6,.04,.04),lit('#F4F8FF',10.0,always=True),0); B.box((0,17.9,3.2),(3.0,.04,.04),lit('#FFE9B8',8.0,always=True),0)
        B.box((-1.6,12.7,.6),(2.6,.5,.6),M('#3F7F7A',.6),.03); B.box((-1.6,12.7,1.23),(2.7,.56,.04),M('#C9CED8',.3,metal=.7),.01)
        for k,xx in enumerate((-3.4,-2.6,-1.7)): B.cyl((xx,12.7,1.52),.26,.52,M('#C9CED8',.25,metal=.9),seg=12,r2=.2); B.cyl((xx,12.7,1.82),.1,.1,M('#C9CED8',.25,metal=.9),seg=8); B.box((xx+.3,12.7,1.6),(.14,.03,.03),M('#C9CED8',.25,metal=.9),0,rot=(0,R(-30),0))
        B.box((-.4,12.7,1.3),(.5,.3,.05),M('#16171C',.6),.01); B.box((-.4,12.7,1.34),(.4,.22,.012),lit('#FF7A1E',6.0,always=True),0)
        for k in range(8): B.cyl((.5+.22*(k%4),12.6+.2*(k//4),1.33),.07,.14,M('#F6F4EE',.4),seg=8,r2=.09)
        for (bx,by) in ((2.9,13.0),(2.9,16.2),(-2.6,16.4)):
            B.box((bx,by,.5),(1.0,.5,.04),wd,.02)
            for dx in (-.9,.9):
                for dy in (-.4,.4): B.cyl((bx+dx,by+dy,.25),.04,.5,wd,seg=6)
        B.box((0,18.2,3.9),(1.2,.03,.6),M('#F4F1EA',.6),0)
        for k in range(6): B.box((-1.0+k*.4,18.17,3.9),(.14,.01,.2),M(r.choice(['#C8372D','#1E6A3A','#2B58C9','#F2C14E']),.6),0)
        point((0,14.5,3.0),500,(1,.86,.62),r=.4,shadow=False); point((0,9.6,3.2),900,(1,.9,.72),r=.4,shadow=False)
    for (x,y,e,c) in ((-21,8.2,1500,(.55,.72,1.0)),(-14,8.2,1300,(1,.5,.4)),(-7.5,8.2,1300,(1,.8,.55)),(7.5,8.2,1300,(1,.8,.55)),(14.5,8.2,1500,(1,.62,.3)),(22,8.2,1300,(.85,.45,1.0)),(-9,-8.2,1300,(.5,1.0,.65)),(0,-8.2,1200,(1,.85,.6)),(9.5,-8.2,1500,(.55,.78,1.0)),(-20,-8.2,1100,(1,.8,.5)),(20,-8.2,1100,(1,.55,.55)),(-30,8.2,1100,(1,.85,.6)),(30,8.2,1100,(.6,.8,1.0)),(0,9.3,800,(1,.9,.75)),(-14,9.3,550,(1,.9,.75)),(14,9.3,550,(1,.9,.75))):
        point((x,y,3.4 if abs(y)<9 else 8.6),e,c,r=.5,shadow=False)
    for k in range(120): a=r.uniform(0,6.283); el=r.uniform(.15,1.2); d=380; B.ico((d*math.cos(a)*math.cos(el),d*math.sin(a)*math.cos(el),d*math.sin(el)),r.uniform(.5,1.1),M('#FFFFFF',.3,emit=6.0),sub=1)
    B.done('pindi'); return S
# ================================================================ night road between the cities
def hiway(mood='pd_night',moon=True):
    """road along y, bikes ride north (+y). carriageway x -8.5..8.5, lamps both sides, green sign gantry at y=60 facing south"""
    NIGHT[0]=1.0; S=setup_world(mood,shadow=90); r=random.Random(41)
    B.box((0,100,-.1),(300,400,.1),M('#1E2A22',.95,kind='grass',sc=3.0),0); B.box((0,100,-.02),(8.5,400,.06),M('#2C2D32',.92,kind='asphalt',sc=1.5),0)
    for s in (1,-1):
        B.box((s*8.3,100,.045),(.08,400,.005),M('#F4F1EA',.6),0); B.box((s*9.3,100,.5),(.12,400,.06),M('#C9CED8',.35,metal=.7),0)
        for k in range(-60,140): B.box((s*9.3,k*3.6,.26),(.06,.06,.26),M('#9AA0A8',.5),0)
        for k in range(-20,40):
            y=k*16.0+(0 if s>0 else 8); B.cyl((s*10.2,y,4.6),.11,9.2,M('#C9CED8',.4,metal=.5),seg=7,r2=.07); B.box((s*9.2,y,9.1),(1.1,.05,.04),M('#C9CED8',.4,metal=.5),0); B.box((s*8.3,y,9.02),(.45,.18,.03),lit('#FFD48A',10.0),0)
            if -40<y<110: point((s*8.2,y,8.4),1300,(1,.78,.48),r=.6,shadow=False)
    for k in range(-60,140):
        for x in (-2.83,2.83): B.box((x,k*5.0,.045),(.07,1.2,.005),M('#F4F1EA',.6),0)
    for s in (1,-1): B.cyl((s*10.8,62,6.5),.24,13.0,M('#C9CED8',.4,metal=.5),seg=8)
    B.box((0,62,12.9),(11,.18,.18),M('#C9CED8',.4,metal=.5),0)
    sign('ISLAMABAD  12 km',(0,61.7,11.7),.8,'#FFFFFF','#1E6A3A',n=(0,-1,0),e=2.5,pad=.36,frame='#F6F4EE')
    for k in range(700):
        s=r.choice((1,-1)); x=s*r.uniform(22,260); y=r.uniform(-120,420); h=r.uniform(.5,14)
        B.ico((x,y,h),r.uniform(.12,.3),M(r.choice(['#FFD48A','#FFE9B8','#FFB060','#BFE6FF','#FF7A6A']),.3,emit=8.0),sub=1)
    for k in range(70):
        s=r.choice((1,-1)); x=s*r.uniform(24,140); y=r.uniform(-80,300); w=r.uniform(4,9); h=r.uniform(6,22); B.box((x,y,h/2),(w,w,h/2),M('#1C2030',.9),0)
        for f in range(int(h//3)):
            for q in range(3):
                if r.random()<.45: B.box((x-s*(w+.03),y-w+.8+q*(2*w-1.6)/2,2+f*3),(.03,.5,.6),M('#FFD890',.3,emit=3.0),0)
    for k in range(90): (pine if k%2 else rtree)(r.choice((1,-1))*r.uniform(12.5,22),r.uniform(-60,260),r.uniform(1.4,2.2))
    for (cx,cy,sx,sy,sz) in ((-80,470,150,40,62),(90,480,170,40,78),(0,520,260,40,95)): B.ico((cx,cy,-2),1.0,M('#0E1626',.95),sc=(sx,sy,sz),sub=3)
    for k in range(200): a=r.uniform(0,6.283); el=r.uniform(.12,1.2); d=430; B.ico((d*math.cos(a)*math.cos(el),60+d*math.sin(a)*math.cos(el),d*math.sin(el)),r.uniform(.6,1.3),M('#FFFFFF',.3,emit=6.0),sub=1)
    if moon: B.ico((-90,430,215),19,M('#FFF6D8',.3,emit=3.5),sub=3)
    B.done('hiway'); return S
# ================================================================ mamu's office
def office(meeting=True):
    """room x -5..5, y -4.2..4.2, open towards -y. PA desk at (-2.4,-.6) by the meeting-room door (x 1..3 on the back wall). table for the MAMU shot is built at y 0 when meeting=False (inside view)"""
    NIGHT[0]=1.0; S=setup_world('pd_in',shadow=30); r=random.Random(3); wl=M('#E9E2D2',.85,kind='wall'); wd=M('#6B4A2E',.6,kind='wood',sc=.6); wd2=M('#8A6238',.55,kind='wood',sc=.6)
    B.box((0,0,-.1),(8,7,.1),M('#7A1F2E' if not meeting else '#B8B0A0',.9,kind='fabric' if not meeting else 'tile',sc=.8),0); B.box((0,4.3,2.4),(5.3,.1,2.4),wl,0)
    for sx in (-1,1): B.box((sx*5.3,0,2.4),(.1,4.4,2.4),wl,0)
    B.box((0,0,4.9),(5.4,4.5,.1),M('#F4F1EA',.9),0); B.box((0,4.18,.6),(5.2,.04,.6),wd,0); B.box((0,4.16,1.22),(5.2,.05,.03),wd2,0)
    for k in (-3,0,3): B.box((k,0,4.76),(.7,.25,.03),lit('#FFF6E8',2.5,always=True),0)
    if meeting:
        B.box((2.0,4.15,1.5),(.85,.06,1.5),wd2,.02); B.box((2.0,4.12,1.5),(.95,.04,1.6),wd,0); B.cyl((2.6,4.05,1.4),.05,.12,M('#E6B93A',.3,metal=.9),rot=(R(90),0,0),seg=8)
        sign('MEETING IN PROGRESS',(2.0,4.05,3.5),.2,'#FFFFFF','#B8232E',n=(0,-1,0),e=5.0,pad=.14,th=.06,always=True)
        B.box((2.0,1.5,.55),(1.5,.6,.55),wd,.03); B.box((2.0,1.5,1.12),(1.6,.68,.04),wd2,.02)
        B.box((3.0,1.55,1.42),(.4,.03,.26),M('#16171C',.4),.02); B.box((3.0,1.58,1.2),(.1,.1,.06),M('#16171C',.4),0)
        for k in range(5): B.box((1.0,1.45+.02*k,1.18+.045*k),(.3,.22,.02),M(r.choice(['#F4F1EA','#F2C14E','#8FB8D8','#E8554D']),.7),.005)
        B.cyl((-4.3,3.3,.35),.32,.7,M('#B8862A',.5),seg=10,r2=.24)
        for k in range(6): a=k*1.05; B.box((-4.3+.35*math.cos(a),3.3+.35*math.sin(a),1.3),(.05,.22,.6),M(GRN[k%4],.8,kind='leaves'),.02,rot=(R(18)*math.sin(a),R(18)*math.cos(a),a))
        for k in range(3): B.box((-4.0+k*1.5,4.17,3.0),(.5,.03,.38),M('#F4F1EA',.6),0); B.box((-4.0+k*1.5,4.15,3.0),(.42,.03,.3),M(('#8FB8D8','#C9B48A','#A8C8B0')[k],.6),0)
        B.box((4.3,2.5,.45),(.5,1.3,.08),M('#27365A',.8,kind='fabric'),.05); B.box((4.72,2.5,.9),(.1,1.3,.45),M('#27365A',.8,kind='fabric'),.06)
        point((1.2,-2.2,2.6),420,(1,.93,.82),r=.4,shadow=False); point((2,3.0,4.3),22,(1,.5,.45),r=.3,shadow=False)
    else:
        B.box((0,.6,1.0),(3.6,1.15,.06),wd2,.04); B.box((0,.6,.5),(3.0,.7,.5),wd,.03)
        for k in range(-2,3):
            for sy in (-1,1):
                if sy<0 and k==0: continue
                B.box((k*1.45,.6+sy*1.75,.62),(.36,.36,.06),M('#27365A',.8,kind='fabric'),.04); B.box((k*1.45,.6+sy*2.08,1.2),(.36,.06,.55),M('#27365A',.8,kind='fabric'),.05)
                for dx in (-.28,.28):
                    for dy in (-.28,.28): B.cyl((k*1.45+dx,.6+sy*1.75+dy,.3),.03,.6,M('#2A2C34',.4,metal=.5),seg=5)
        for k in range(-2,3):
            B.cyl((k*1.4+.1,1.2,1.1),.07,.1,M('#F6F4EE',.4),seg=10,r2=.09); B.cyl((k*1.4+.1,1.2,1.06),.13,.015,M('#F6F4EE',.4),seg=12)
            B.box((k*1.4-.3,1.15,1.075),(.22,.3,.012),M('#F4F1EA',.6),0)
        B.cyl((.9,.3,1.08),.3,.03,M('#F6F4EE',.4),seg=14)
        for k in range(5): B.box((.78+.12*(k%3),.24+.12*(k//3),1.14),(.08,.07,.04),M('#C98A3A',.7),.02,rot=(0,0,k*.7))
        B.cyl((-.9,.25,1.2),.14,.26,M('#C9CED8',.25,metal=.9),seg=12,r2=.1)
        B.cyl((3.3,4.17,3.4),.42,.05,M('#F4F1EA',.5),rot=(R(90),0,0),seg=20); B.box((3.3,4.13,3.52),(.015,.01,.14),M('#16171C',.5),0); B.box((3.42,4.13,3.4),(.12,.01,.015),M('#16171C',.5),0)
        B.box((-2.6,4.17,3.1),(1.2,.03,.7),M('#F4F1EA',.6),0); B.box((-2.6,4.15,3.1),(1.1,.03,.6),M('#8FB8D8',.6),0); B.box((-2.6,4.14,2.85),(1.1,.03,.2),M('#4E9A46',.7),0)
        sign('ANNUAL MEETING No. 47',(-2.6,4.1,4.15),.17,'#FFFFFF','#27365A',n=(0,-1,0),pad=.12,th=.04)
        point((0,-1.2,3.7),420,(1,.93,.82),r=.4,shadow=False); point((0,2.5,3.6),200,(1,.9,.75),r=.4,shadow=False)
    B.done('office'); return S
