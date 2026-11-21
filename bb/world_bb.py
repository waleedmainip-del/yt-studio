# Sets for "The Islamabadi Burger Bachha": hill viewpoint, Islamabad sector avenue (kiosk, samosa cart, villa), sneaker closet,
# Pindi flyover adda (truck-art truck, tyre shop), dusk burger stall, villa dining room.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
def pine(x,y,s=1.0,col='#2F6A3E'):
    B.cyl((x,y,1.2*s),.16*s,2.4*s,M('#6B4A2E',.85,kind='wood',sc=.5),seg=7)
    for k in range(4): B.cyl((x,y,(2.2+k*1.15)*s),(1.5-k*.3)*s,1.7*s,M(shade(col,1+.06*k),.85,kind='leaves'),seg=9,r2=.05*s)
def shrub(x,y,s=1.0,col='#4F8A3A'):
    for dx,dy,r_ in ((0,0,.6),(.5,.15,.45),(-.45,-.1,.5)): B.ico((x+dx*s,y+dy*s,.35*s),r_*s,M(col,.85,kind='leaves'),sc=(1,1,.8),sub=1)
def hills(y0=140,seed=2,base=-30,cols=('#4E8A52','#3F7A48','#5C9A5A','#356E44')):
    r=random.Random(seed)
    for k in range(16):
        x=-260+k*35+r.uniform(-10,10); h=r.uniform(45,95); B.ico((x,y0+r.uniform(0,90),base),h,M(r.choice(cols),.95),sc=(1.6,1.2,1.0),sub=2)
def mosque_white(x,y,z,s=1.0):
    wt=M('#F6F3EA',.6); gd=M('#D9B24A',.3,metal=.8)
    for a in range(4): B.box((x+math.cos(a*pi/2)*4.2*s,y+math.sin(a*pi/2)*4.2*s,z+5.5*s),(6.5*s,.25*s,7.5*s),wt,0,rot=(R(40)*math.sin(a*pi/2),-R(40)*math.cos(a*pi/2),a*pi/2+pi/2))
    B.box((x,y,z+1.2*s),(8*s,8*s,1.2*s),wt,0)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((x+sx*10*s,y+sy*10*s,z+12*s),.7*s,24*s,wt,seg=8,r2=.45*s); B.cyl((x+sx*10*s,y+sy*10*s,z+25.5*s),.45*s,3*s,gd,seg=8,r2=.02)
def city_below(z=-28,seed=5):
    r=random.Random(seed); B.box((0,120,z-.5),(320,130,.5),M('#6E9A58',.95,kind='grass',sc=.2),0)
    for k in range(150):
        x=r.uniform(-200,200); y=r.uniform(30,190); w=r.uniform(3,8); h=r.uniform(3,12) if r.random()<.85 else r.uniform(18,34)
        if abs(x+20)<22 and abs(y-95)<22: continue
        B.box((x,y,z+h/2),(w,w*r.uniform(.7,1.3),h/2),M(r.choice(['#F2EEE4','#E4DCCB','#D8D2C6','#C9D2DA','#EDE3D0','#B9C4CC']),.8),0)
    for k in range(60): B.ico((r.uniform(-200,200),r.uniform(30,190),z+2),r.uniform(3,6),M(r.choice(['#3F7A48','#4E8A52','#2F6A3E']),.9),sc=(1,1,.7),sub=1)
    for y in (60,110,160): B.box((0,y,z+.05),(320,1.6,.05),M('#8A8C90',.8),0)
    for x in (-120,-40,60,140): B.box((x,120,z+.05),(1.6,130,.05),M('#8A8C90',.8),0)
    mosque_white(-20,95,z,1.0)
def viewpoint():
    st=M('#B9AE9C',.85,kind='tile',h2='#A89C8A',sc=1.4); rl=M('#7A5A3E',.7,kind='wood'); stn=M('#8E8576',.9,kind='concrete')
    B.box((0,0,-.5),(13,6,.5),st,0); B.box((0,-14,-3),(40,9,3.2),M('#5E8A4C',.95,kind='grass',sc=.4),0)
    for x in range(-12,13,3): B.box((x,5.2,.55),(.14,.14,.6),stn,.02)
    for z in (.55,1.05): B.box((0,5.2,z),(12.6,.07,.06),rl,.01)
    B.box((0,5.2,1.18),(12.8,.12,.04),rl,.01)
    for x in (-7.5,7.2):  # coin binoculars
        B.cyl((x,4.3,.6),.07,1.2,M('#3A3D44',.4,metal=.6),seg=8); B.box((x,4.35,1.3),(.16,.22,.12),M('#C8372D' if x<0 else '#2B58C9',.4,metal=.4),.04)
    for x in (-10.5,10.5): B.cyl((x,3.6,1.9),.06,3.8,M('#2A3A30',.4,metal=.5),seg=8); B.ico((x,3.6,3.9),.24,M('#FFF2C8',.3,emit=.6),sub=2)
    B.box((-9.6,1.2,.45),(.5,1.1,.04),rl,.02); B.box((-9.6,1.2,.22),(.4,1.0,.22),stn,.03)
    B.box((9.3,-1.5,.9),(.06,.9,.9),M('#2F6A3E',.5),.02); stext('VIEW POINT',(9.24,-1.5,1.35),.22,'#F4F1EA',n=(-1,0,0)); stext('1173 m',(9.24,-1.5,.95),.2,'#F2C14E',n=(-1,0,0))
    r=random.Random(7)
    for (x,y,s) in ((-15,2,1.5),(-17,-4,1.8),(15.5,1,1.6),(17,-5,1.4),(-14.5,6.5,1.2),(15,7,1.3),(-20,5,1.7),(21,3,1.6)): pine(x,y,s,r.choice(['#2F6A3E','#356E44','#2A6038']))
    for k in range(18): pine(r.uniform(-40,40),r.uniform(9,24),r.uniform(.9,1.6));
    B.box((0,16,-9),(60,9,8),M('#4E8A52',.95,kind='grass',sc=.3),0,rot=(R(-24),0,0))
    for x in (-11,-5.5,6,11.5): B.cyl((x,-4.6,.25),.45,.5,M('#B5603F',.8),seg=12,r2=.36); B.ico((x,-4.6,.85),.55,M('#D9577A' if x<0 else '#F2C14E',.8,kind='leaves'),sub=1)
    city_below(); hills(230,2,-28)

# ---------------------------------------------------------------- Islamabad sector
def modern_house(cx,w,Y,seed,h=6.4):
    r=random.Random(seed); wt=M(r.choice(['#F6F3EC','#EFEAE0','#F2F0EA']),.8,kind='wall'); wd=M(r.choice(['#8A5A3A','#6B4A2E','#A0683E']),.7,kind='wood'); gl=M('#27364A',.08,spec=1.0); gr=M('#5A5E66',.6,kind='concrete')
    B.box((cx,Y+4,h/2),(w/2-.6,3.6,h/2),wt,.03); B.box((cx-w*.18,Y+.5,h*.7),(w*.26,.5,h*.26),wt,.03); B.box((cx+w*.2,Y+.3,h*.3),(w*.2,.25,h*.3),wd,.02)
    B.box((cx-w*.18,Y-.02,h*.7),(w*.2,.04,h*.18),gl,0); B.box((cx+w*.2,Y+.03,1.25),(.55,.05,1.25),M('#3A2A1E',.6,kind='wood'),.02)
    B.box((cx,Y+4,h+.12),(w/2-.4,3.8,.12),gr,.02); B.box((cx-w*.18,Y+.5,h*.96+.1),(w*.28,.7,.08),gr,.02)
    B.box((cx,Y-3.2,.7),(w/2-.1,.14,.7),wt,.02); B.box((cx,Y-3.2,1.44),(w/2,.18,.05),gr,.01)
    for k in range(int(w/1.3)): B.ico((cx-w/2+.8+k*1.3,Y-2.75,1.55),.5,M(r.choice(['#3F7A48','#4E8A52']),.85,kind='leaves'),sc=(1.2,.8,.8),sub=1)
    B.box((cx+w*.2,Y-3.2,1.0),(1.3,.08,1.0),M('#2A2C34',.4,metal=.5),.02)
    for j in range(7): B.box((cx+w*.2-1.2+j*.4,Y-3.3,1.0),(.03,.03,.95),M('#C9CED8',.3,metal=.8),0)
    if r.random()<.7 and not (SKIPX[0] is not None and abs(cx-w/2+1.2-SKIPX[0])<5): pine(cx-w/2+1.2,Y-1.4,r.uniform(.8,1.1))
def kiosk(x,y):
    bk=M('#22242B',.5,metal=.3); wd=M('#A0683E',.6,kind='wood'); e=None
    B.box((x,y+1.2,1.5),(1.9,1.2,1.5),bk,.04); B.box((x,y-.05,2.0),(1.5,.06,.65),M('#FFE8C4',.5,emit=.5),0); B.box((x,y-.25,1.28),(1.75,.3,.06),wd,.02)
    B.box((x,y-.02,.62),(1.9,.04,.62),wd,.02); B.box((x,y-.75,2.95),(2.1,.8,.05),M('#E8DCC6',.8,kind='fabric',h2='#C8372D',sc=5),.02,rot=(R(-10),0,0))
    stext('BREW LAB',(x,y-.1,3.35),.36,'#F4F1EA',e=1.2); B.box((x,y-.06,3.35),(1.6,.04,.3),bk,.02)
    B.box((x+2.5,y-.1,1.2),(.5,.04,.8),M('#16171C',.6),.02); stext('FLAT WHITE  950',(x+2.5,y-.16,1.6),.085,'#F4F1EA'); stext('OAT LATTE  1,250',(x+2.5,y-.16,1.35),.085,'#F4F1EA'); stext('COLD BREW  1,100',(x+2.5,y-.16,1.1),.085,'#F4F1EA'); stext('MATCHA  1,450',(x+2.5,y-.16,.85),.085,'#9AD08A')
    B.box((x+.9,y+.3,1.55),(.3,.25,.22),M('#C9CED8',.3,metal=.9),.03); B.cyl((x-1.0,y-.3,1.42),.07,.2,M('#F4F1EA',.5),seg=10); B.cyl((x-.75,y-.3,1.42),.07,.2,M('#F4F1EA',.5),seg=10)
def samosa_cart(x,y):
    wd=M('#2B8A7A',.6,kind='wood'); B.box((x,y,.75),(1.0,.55,.08),wd,.02); B.box((x,y,.4),(.95,.5,.04),wd,.02)
    for dx in (-.85,.85): B.cyl((x+dx,y-.6,.34),.34,.06,M('#2A2C34',.6),rot=(R(90),0,0),seg=14)
    B.box((x-.3,y,1.12),(.55,.42,.3),M('#BFD6E8',.05,spec=1.0,alpha=.3),.01); r=random.Random(3)
    for k in range(14): B.box((x-.3+r.uniform(-.4,.4),y+r.uniform(-.3,.3),.9+r.uniform(0,.12)),(.09,.07,.06),M('#D9982E',.7),.02,rot=(0,0,r.uniform(0,3)))
    B.cyl((x+.55,y,.93),.3,.16,M('#3A3D44',.4,metal=.6),seg=14); B.cyl((x+.55,y,1.0),.26,.04,M('#C98A2E',.4,spec=.8),seg=14)
    B.cyl((x,y+.5,1.9),.03,2.3,M('#C9CED8',.4,metal=.6),seg=6)
    for a in range(8): B.box((x+math.cos(a*pi/4)*.75,y+.5+math.sin(a*pi/4)*.75,2.95),(.8,.3,.02),M('#E8554D' if a%2 else '#F4F1EA',.8,kind='fabric'),.0,rot=(0,R(14),a*pi/4))
    B.box((x,y-.58,1.0),(.7,.02,.14),M('#F2C14E',.6),.01); stext('SAMOSA  2 for 50',(x,y-.61,1.0),.1,'#7A1F1F')
HOUSES=[]; SKIPX=[None]
def sector(skip=None):
    B.box((0,0,-.05),(140,3.6,.05),M('#3E4046',.85,kind='asphalt'),0)
    for k in range(-34,35): B.box((k*4.0,0,.003),(1.0,.06,.003),M('#EDEBE4',.6),0)
    for s in (-1,1):
        B.box((0,s*4.9,.07),(140,1.3,.07),M('#CFC8BA',.8,kind='tile',h2='#BFB8AA',sc=2.0),0); B.box((0,s*3.62,.08),(140,.06,.08),M('#F2C14E' ,.7),.01)
        B.box((0,s*20,.02),(140,13.8,.02),M('#6FA04C',.9,kind='grass',sc=.5),0)
    r=random.Random(21); x=-66; i=0
    while x<66:
        w=r.choice([11,12,13]); modern_house(x+w/2,w,12.5,i*7+3,h=r.choice([6.0,6.8,7.4])); HOUSES.append((x+w/2,w)); x+=w; i+=1
    x=-66
    while x<66:
        w=r.choice([11,13]); B.box((x+w/2,-16,3.2),(w/2-.6,3.4,3.2),M(r.choice(['#F6F3EC','#EFEAE0']),.8,kind='wall'),.03); B.box((x+w/2,-9.3,.7),(w/2-.1,.14,.7),M('#F2F0EA',.8,kind='wall'),.02); x+=w
    for x in range(-63,64,9):
        sc_=r.uniform(1.0,1.35); sc2=r.uniform(1.0,1.3)
        if skip is None or abs(x-skip)>4: pine(x,7.3,sc_)
        pine(x+4.5,-7.2,sc2)
    for x in range(-60,61,6): shrub(x+1.5,6.4,.7,r.choice(['#4F8A3A','#5E9A44']));
    for x in range(-56,57,16):
        B.cyl((x,5.75,2.6),.07,5.2,M('#3A3D44',.4,metal=.6),seg=8); B.box((x,5.0,5.2),(.06,.8,.05),M('#3A3D44',.4,metal=.6),0); B.box((x,4.3,5.15),(.14,.3,.05),M('#FFF2C8',.3,emit=.8),.01)
    for x in (-52,-20,22,50): B.box((x,5.6,.45),(.9,.22,.04),M('#8A5A3A',.7,kind='wood'),.02); B.box((x,5.6,.22),(.7,.16,.22),M('#9A958C',.8,kind='concrete'),.02)
    B.cyl((17.5,5.7,1.4),.05,2.8,M('#C9CED8',.4,metal=.6),seg=6); B.box((17.5,5.66,2.5),(.7,.03,.28),M('#1F6A3A',.5),.02); stext('STREET 7',(17.5,5.62,2.5),.2,'#F4F1EA')
    hills(150,4,-12)
def villa_door(cx,Y=12.5):
    # hero entrance added on top of modern_house facade at cx
    B.box((cx,Y-1.6,.1),(1.6,1.6,.1),M('#D8D2C6',.6,kind='tile',h2='#C8C2B6',sc=3),.02); B.box((cx,Y-.1,1.5),(.9,.08,1.5),M('#5A3A22',.6,kind='wood'),.03); B.box((cx+.6,Y-.2,1.4),(.04,.04,.4),M('#D9B24A',.3,metal=.9),.01)
    for dx in (-1.5,1.5): B.cyl((cx+dx,Y-.7,.35),.3,.7,M('#F4F1EA',.6),seg=10,r2=.22); B.ico((cx+dx,Y-.7,1.15),.45,M('#3F7A48',.85,kind='leaves'),sc=(1,1,1.4),sub=1)
    B.box((cx,Y-.9,3.25),(1.9,.9,.08),M('#5A5E66',.6,kind='concrete'),.02); B.box((cx-1.25,Y-.2,2.2),(.12,.05,.2),M('#FFF2C8',.3,emit=1.2),.02)
    stext('HOUSE 14',(cx+1.55,Y-.16,2.0),.16,'#D9B24A')

# ---------------------------------------------------------------- closet (interior)
def closet():
    fl=M('#D9C8AE',.5,kind='wood',sc=.8); wl=M('#EFE9DF',.85,kind='wall'); wd=M('#F6F3EC',.5); rail=M('#C9CED8',.3,metal=.9)
    B.box((0,0,-.05),(3.2,2.6,.05),fl,0); B.box((0,2.6,1.7),(3.2,.08,1.7),wl,0); B.box((-3.2,0,1.7),(.08,2.6,1.7),wl,0); B.box((3.2,0,1.7),(.08,2.6,1.7),wl,0); B.box((0,0,3.42),(3.2,2.6,.05),wl,0)
    # sneaker wall (left half of back wall)
    for row in range(5):
        z=.45+row*.52; B.box((-1.55,2.36,z-.13),(1.45,.2,.02),wd,.01)
        for k in range(6):
            x=-2.75+k*.48; B.box((x,2.3,z),(.17,.13,.07),M('#FAFAFA',.5),.03); B.box((x+.03,2.3,z+.07),(.11,.11,.05),M('#FAFAFA',.5),.03); B.box((x,2.3,z-.06),(.18,.14,.02),M('#E9ECF2',.5),.01)
            B.box((x-.1,2.17,z+.01),(.04,.005,.03),M(['#C8372D','#2B58C9','#35975A','#F2C14E','#16171C','#CF3F78'][(row+k)%6],.5),.0)
    B.box((-1.55,2.4,3.05),(1.5,.16,.04),wd,.01)
    # hanging rail (right half)
    B.cyl((1.6,2.2,2.5),.025,2.9,rail,rot=(0,R(90),0),seg=8); B.box((1.6,2.36,1.45),(1.5,.2,1.45),M('#E6DFD2',.8),.01)
    cols=['#F4F1EA','#BFD6E8','#F2D8E0','#D8E8D0','#EDE3D0','#C9D2DA','#F6E7B8','#E4DCF0','#F4F1EA','#D9E8F2']
    for k,c in enumerate(cols): B.box((.35+k*.27,2.15,1.92),(.1,.16,.55),M(c,.8,kind='fabric'),.03); B.box((.35+k*.27,2.2,2.5),(.008,.008,.06),rail,0)
    for k in range(4): B.box((.6+k*.6,2.2,.28),(.24,.2,.14),M(['#EDE3D0','#C9D2DA','#F4F1EA','#D8E8D0'][k],.8,kind='fabric'),.03)
    # ring-light mirror on the left wall, perfume shelf, rug, pouf
    B.box((-3.1,-.2,1.75),(.03,.65,1.15),M('#DCEAF2',.05,spec=1.0),.01); B.box((-3.12,-.2,1.75),(.03,.72,1.22),M('#D9B24A',.3,metal=.8),.02)
    for k in range(6): B.ico((-3.05,-.85,.75+k*.4),.05,M('#FFF6E0',.3,emit=3),sub=1); B.ico((-3.05,.45,.75+k*.4),.05,M('#FFF6E0',.3,emit=3),sub=1)
    B.box((3.05,-.3,1.3),(.12,.7,.03),wd,.01)
    for k in range(5): B.box((3.02,-.8+k*.25,1.45),(.05,.05,.11),M(['#F2C14E','#BFD6E8','#F2D8E0','#22242B','#D8E8D0'][k],.2,spec=.9),.02)
    B.cyl((0,-.2,.012),1.5,.02,M('#E8DCC6',.9,kind='fabric',h2='#C9B48A',sc=4),seg=28); B.cyl((2.2,-1.2,.22),.38,.44,M('#C9B48A',.9,kind='fabric'),seg=16)
    B.box((0,0,3.36),(.5,.5,.03),M('#FFF6E0',.3,emit=2.2),.01)

# ---------------------------------------------------------------- Pindi adda
def truck_art(x,y,rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz))); cols=['#E8554D','#F2C14E','#2B8A7A','#2B58C9','#CF3F78','#F28A3A','#35975A']; r=random.Random(9)
    obox((0,0,.75),(3.4,1.05,.12),M('#2A2C34',.6),.03,e); obox((2.5,0,1.75),(.9,1.0,.95),M('#C8372D',.4,metal=.2),.08,e); obox((3.38,0,2.0),(.04,.85,.4),M('#1A2433',.06,spec=1.0),.02,e)
    obox((-.6,0,2.2),(2.3,1.08,1.35),M('#1F6A5A',.5),.04,e); obox((2.6,0,3.3),(1.2,1.1,.55),M('#F2C14E',.5),.06,e,rot=(0,R(-14),0)); obox((3.3,0,1.05),(.12,1.05,.2),M('#C9CED8',.3,metal=.9),.03,e)
    for sy in (-1,1):
        for i in range(5):
            for j in range(3): obox((-2.5+i*.95,sy*1.1,1.3+j*.85),(.4,.02,.36),M(cols[(i*2+j+ (0 if sy<0 else 3))%7],.5),.02,e); obox((-2.5+i*.95,sy*1.13,1.3+j*.85),(.18,.01,.18),M(cols[(i+j*3+1)%7],.4,emit=.2),.0,e,rot=(0,R(45),0))
        for i in range(12): obox((-2.8+i*.42,sy*1.12,.78),(.03,.01,.12+.05*(i%2)),M('#C9CED8',.3,metal=.9),0,e)
        obox((2.5,sy*1.02,1.95),(.5,.02,.38),M('#1A2433',.06,spec=1.0),.02,e)
    for k in range(7): obox((3.42,-.9+k*.3,3.2),(.02,.11,.2),M(cols[k],.4,emit=.3),.02,e,rot=(0,R(-14),0))
    for (wx,sy) in ((2.4,-1),(2.4,1),(-1.6,-1),(-1.6,1),(-2.6,-1),(-2.6,1)): wheel((wx,sy*.95,.48),.48,.26,e)
    for sy in (-1,1): obox((3.42,sy*.65,1.3),(.03,.16,.1),M('#FFF6D8',.2,emit=1.5),.02,e)
    return e
def tyre_stack(x,y,n=4,r_=.42):
    for k in range(n): B.cyl((x+.03*math.sin(k*2),y,.14+k*.27),r_,.26,M('#1E1F24',.85),seg=14); B.cyl((x+.03*math.sin(k*2),y,.14+k*.27),r_*.5,.27,M('#55585F',.6),seg=10)
def charpai(x,y,rz=0,col='#C8372D'):
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#7A5236',.7,kind='wood'); obox((0,0,.52),(1.0,.5,.03),M('#E8D2A8',.9,kind='fabric',h2=col,sc=3),.01,e)
    for dx in (-.98,.98):
        for dy in (-.48,.48): ocyl((dx,dy,.27),.045,.6,wd,e,rot=(0,0,0),seg=8)
    for dy in (-.5,.5): obox((0,dy,.52),(1.02,.03,.04),wd,.01,e)
    for dx in (-1.0,1.0): obox((dx,0,.52),(.03,.5,.04),wd,.01,e)
    return e
def old_block(cx,w,Y,seed):
    r=random.Random(seed); c=r.choice(['#D9B48A','#C8D2C0','#E6C9A0','#B8C8D0','#E8B8A0','#D8C890','#C9A8C0']); h=r.choice([8,10.5,13])
    B.box((cx,Y+4,h/2),(w/2-.05,4,h/2),M(c,.9,kind='wall'),0)
    for f in range(int(h/2.6)):
        z=2.9+f*2.6
        if f>0: B.box((cx,Y-.5,z-1.0),(w/2-.3,.5,.06),M(shade(c,.8),.8,kind='concrete'),.01);
        if f>0:
            for k in range(int(w/.5)): B.box((cx-w/2+.4+k*.5,Y-.95,z-.6),(.025,.025,.4),M('#3A4A3A',.5,metal=.4),0)
            B.box((cx,Y-.95,z-.2),(w/2-.3,.03,.03),M('#3A4A3A',.5,metal=.4),0)
        for k in range(max(1,int(w/2.4))): B.box((cx-w/2+1.2+k*2.4,Y-.02,z if f>0 else 1.5),(.55,.05,.75),M(r.choice(['#3A5A6A','#5A3A2A','#2A4A3A','#27364A']),.6,kind='wood'),.01)
    if r.random()<.6: B.cyl((cx+r.uniform(-1,1),Y+3,h+.8),.7,1.3,M(r.choice(['#2A2C34','#2B58C9','#F4F1EA']),.5),seg=10)
    if r.random()<.5: B.box((cx,Y-.3,h+1.2),(w/2-.6,.08,.9),M(r.choice(['#C8372D','#F2C14E','#2B58C9','#35975A']),.6),.02)
def adda():
    B.box((0,0,-.05),(120,4.0,.05),M('#4A4640',.9,kind='asphalt'),0); B.box((0,10,-.03),(120,6.0,.04),M('#A89878',.95,kind='concrete',sc=.5),0); B.box((0,-7,-.03),(120,3.0,.04),M('#A89878',.95,kind='concrete',sc=.5),0)
    cn=M('#B4B0A8',.9,kind='concrete'); r=random.Random(31)
    B.box((0,12,7.2),(120,3.4,.5),cn,.03)
    for s in (-1,1): B.box((0,12+s*3.4,8.0),(120,.14,.45),M('#9A968E',.9,kind='concrete'),.02)
    pc=['#F2C14E','#2B8A7A','#E8554D','#2B58C9']
    for i,x in enumerate(range(-54,55,12)):
        B.box((x,12,3.35),(.75,.75,3.35),cn,.04); B.box((x,12,6.5),(1.6,1.9,.35),cn,.04)
        for j in range(3): B.box((x,12,.6+j*.55),(.77,.77,.2),M(pc[(i+j)%4],.7),.01)
        B.box((x,11.22,3.2),(.55,.03,.75),M('#F4F1EA',.8),.01); stext(['PINDI','BOYS','ZINDABAD','METRO','SADDAR','RAJA BAZAR'][i%6],(x,11.18,3.2),.2,pc[(i+2)%4])
    # tyre shop + charpai + junk around pillars x=-6..6
    B.box((7.5,14.0,1.6),(2.6,.2,1.6),M('#2B8A7A',.8,kind='wall'),.02); B.box((7.5,13.7,3.0),(2.7,.1,.38),M('#F2C14E',.6),.02); stext('USTAD TYRE WORKS',(7.5,13.58,3.0),.26,'#7A1F1F')
    for (x,y,n) in ((5.6,13.2,5),(6.6,13.3,3),(9.4,13.2,6),(8.5,13.4,2)): tyre_stack(x,y,n)
    B.cyl((10.4,12.6,.5),.32,1.0,M('#2B58C9',.5,metal=.3),seg=12); B.box((4.7,13.3,.35),(.35,.3,.35),M('#C8372D',.6,metal=.3),.03)
    x=-60; i=0
    while x<60:
        w=r.choice([6,7,8,9]); old_block(x+w/2,w,19.5,i*5+2); x+=w; i+=1
    x=-60; i=0
    while x<60:
        w=r.choice([7,8,9]); c=r.choice(['#D9B48A','#C8D2C0','#E6C9A0','#B8C8D0']); B.box((x+w/2,-13,4),(w/2-.05,3,4),M(c,.9,kind='wall'),0); B.box((x+w/2,-9.9,1.3),(w/2-.4,.06,1.2),M(r.choice(['#3A5A6A','#5A3A2A','#2A4A3A','#8A8C90']),.6,kind='wood'),.01)
        B.box((x+w/2,-9.8,3.0),(w/2-.2,.1,.4),M(r.choice(['#C8372D','#F2C14E','#2B58C9','#35975A','#F4F1EA']),.6),.02); x+=w; i+=1
    for x in range(-50,51,14): pole(x,-5.2,8.0); pole(x+7,16.5,8.5)
    wires(-56,56,-5.2,-5.2,7.6,3,5); wires(-56,56,16.5,16.5,8.1,4,6)
    for (x,y) in ((-14,15.5),(15,15.8),(31,15.4),(-33,15.6)): tree(x,y,1.2,r.choice(['#5E8A3A','#6A9444']),'#5A3E28')
    for k in range(30): B.box((r.uniform(-40,40),r.uniform(5,16),.02),(r.uniform(.05,.14),r.uniform(.04,.1),.02),M(r.choice(['#8A7A60','#6A5E4A','#C8BFB0']),.9),.0,rot=(0,0,r.uniform(0,3)))
    for k in range(10): B.box((r.uniform(-90,90),r.uniform(40,60),r.uniform(6,11)),(r.uniform(4,7),4,r.uniform(6,11)),M(r.choice(['#C9B8A0','#B8A890','#C8C0B0']),.8,kind='concrete'),0)

# ---------------------------------------------------------------- dusk burger stall
def plastic_chair(x,y,rz=0,col='#C8372D'):
    e=empty((x,y,0),rot=(0,0,R(rz))); m=M(col,.45,spec=.6); obox((0,0,.56),(.27,.26,.03),m,.02,e); obox((0,.25,.9),(.27,.03,.34),m,.03,e)
    for dx in (-.23,.23):
        for dy in (-.22,.22): obox((dx,dy,.28),(.03,.03,.28),m,.01,e)
    return e
def burger_obj(parent=None,loc=(0,0,0),s=1.0):
    e=empty(loc,parent); bun=M('#D9982E',.6); ocyl((0,0,.03*s),.11*s,.05*s,bun,e,rot=(0,0,0),seg=14); ocyl((0,0,.075*s),.12*s,.035*s,M('#5A2E1A',.8),e,rot=(0,0,0),seg=14)
    obox((0,0,.1*s),(.125*s,.125*s,.008*s),M('#F2C14E',.5),.0,e,rot=(0,0,R(20))); ocyl((0,0,.115*s),.125*s,.015*s,M('#4F9A3A',.7),e,rot=(0,0,0),seg=10)
    oico((0,0,.135*s),.115*s,bun,e,sc=(1,1,.62),sub=2); return e
def stall():
    B.box((0,0,-.05),(60,5,.05),M('#3E3A38',.9,kind='asphalt'),0); B.box((0,8,-.02),(60,3.2,.05),M('#8A7E6A',.95,kind='concrete',sc=.5),0)
    wl=M('#C9B48A',.9,kind='wall'); B.box((0,10.6,2.2),(60,.2,2.2),wl,0); B.box((0,10.45,4.45),(60,.3,.08),M('#8A5A3A',.8),.01)
    post=['#C8372D','#2B58C9','#F2C14E','#35975A','#F4F1EA','#CF3F78']; r=random.Random(41)
    for k in range(26): x=-30+k*2.4+r.uniform(-.4,.4); B.box((x,10.38,r.uniform(1.4,3.4)),(r.uniform(.3,.6),.01,r.uniform(.35,.6)),M(r.choice(post),.8),.0,rot=(0,r.uniform(-.06,.06),0))
    stext('RAJA JEE BURGER POINT',(0,10.36,3.75),.42,'#7A1F1F');
    # cart
    cx,cy=0.0,7.6; rd=M('#C8372D',.5,metal=.2); stl=M('#C9CED8',.3,metal=.9)
    B.box((cx,cy,.55),(1.6,.6,.5),rd,.03); B.box((cx,cy,1.08),(1.65,.65,.04),stl,.02); B.box((cx-.7,cy,1.14),(.6,.45,.03),M('#2A2C34',.4,metal=.6),.02)
    for dx in (-1.2,1.2): B.cyl((cx+dx,cy-.66,.36),.36,.07,M('#22242B',.7),rot=(R(90),0,0),seg=14)
    for k in range(4): B.cyl((cx-.95+k*.18,cy+.05,1.19),.07,.03,M('#6A3A22',.8),seg=10)
    for k in range(3): B.cyl((cx+.3+k*.3,cy+.25,1.3),.07,.36,M(['#C8372D','#F2C14E','#F4F1EA'][k],.4),seg=10)
    B.box((cx+1.0,cy,1.3),(.35,.35,.2),M('#BFD6E8',.05,spec=1.0,alpha=.35),.01)
    for k in range(5): B.ico((cx+1.0+r.uniform(-.2,.2),cy+r.uniform(-.2,.2),1.2+.05*k),.1,M('#D9982E',.6),sc=(1,1,.6),sub=1)
    for dx in (-1.6,1.6): B.cyl((cx+dx,cy+.55,1.6),.035,3.2,stl,seg=6)
    B.box((cx,cy,3.2),(1.9,.95,.05),M('#F2C14E',.8,kind='fabric',h2='#C8372D',sc=4),.02,rot=(R(-6),0,0)); B.box((cx,cy-.9,2.85),(1.9,.03,.22),rd,.02); stext('BURGER  -  SHAMI  -  CHAI',(cx,cy-.94,2.85),.17,'#FFF3B0',e=.8)
    # menu board
    B.box((3.6,7.9,1.7),(.75,.05,1.0),M('#16171C',.7),.03); B.cyl((3.6,8.0,.4),.04,.8,M('#3A3D44',.5),seg=6)
    stext('MENU',(3.6,7.83,2.45),.2,'#F2C14E',e=.6)
    for k,(a,b_) in enumerate((('BUN KABAB','120'),('ANDA SHAMI','150'),('ZINGER','350'),('CHIPS','100'),('DOODH PATTI','80'))): stext('%s  %s'%(a,b_),(3.6,7.83,2.12-k*.27),.115,'#F4F1EA',e=.3)
    # seating
    for (tx,ty) in ((-2.6,3.6),):
        B.cyl((tx,ty,.5),.05,1.0,M('#F4F1EA',.5),seg=8); B.box((tx,ty,1.0),(.75,.75,.03),M('#2B58C9',.45,spec=.6),.03); B.cyl((tx,ty,.02),.3,.04,M('#F4F1EA',.5),seg=10)
    B.cyl((3.2,2.8,.5),.05,1.0,M('#F4F1EA',.5),seg=8); B.box((3.2,2.8,1.0),(.6,.6,.03),M('#35975A',.45,spec=.6),.03)
    for (x,y,rz,c) in ((2.4,2.6,-90,'#F2C14E'),(4.0,3.0,90,'#F2C14E'),(3.3,3.7,180,'#F2C14E')): plastic_chair(x,y,rz,c)
    # string bulbs
    for (x0,x1,y,z) in ((-9,9,5.2,4.3),(-9,9,8.6,4.5)):
        for k in range(19):
            f=k/18; x=x0+(x1-x0)*f; zz=z-.5*math.sin(pi*f); B.ico((x,y,zz),.09,M(['#FFE08A','#FF9A6A','#FFF2C8'][k%3],.3,emit=6),sub=1)
        for k in range(18):
            f0=k/18; f1=(k+1)/18; xa=x0+(x1-x0)*f0; xb=x0+(x1-x0)*f1; za=z-.5*math.sin(pi*f0)+.08; zb=z-.5*math.sin(pi*f1)+.08; B.box(((xa+xb)/2,y,(za+zb)/2),((xb-xa)/2+.02,.008,.008),M('#16171C',.6),0,rot=(0,-math.atan2(zb-za,xb-xa),0))
    for x in (-9,9): B.cyl((x,5.2,2.3),.05,4.6,M('#5A4030',.7,kind='wood'),seg=6); B.cyl((x,8.6,2.4),.05,4.8,M('#5A4030',.7,kind='wood'),seg=6)
    tree(-7.2,9.3,1.4,'#4E7A3A','#5A3E28'); tree(11,9.4,1.2,'#5E8A44','#5A3E28')
    B.cyl((6.2,9.2,.5),.34,1.0,M('#2B58C9',.5,metal=.3),seg=12); B.box((-5,9.6,.3),(.5,.35,.3),M('#8A5A3A',.7,kind='wood'),.02); B.box((-5.2,9.5,.8),(.35,.3,.2),M('#C8372D',.5),.02)
    for k in range(14):
        x=-56+k*8.5; h=r.uniform(6,13); c=r.choice(['#8A7E78','#7A7480','#94887A','#6E6E7C']); B.box((x,17+r.uniform(0,5),h/2),(3.8,3.5,h/2),M(c,.9,kind='wall'),0)
        for z in range(3,int(h)-1,3):
            for dx in (-1.8,0,1.8):
                if r.random()<.55: B.box((x+dx,13.4+ (0),z),(.5,.05,.6),M('#FFD98A',.3,emit=r.uniform(1.5,3.5)),0)
    for k in range(9): x=-52+k*13; B.box((x,-11,4),(5.5,3,4),M(r.choice(['#8A7E78','#7A7480','#94887A']),.9,kind='wall'),0)
    pole(-12,9.8,8.5); pole(13.5,9.8,8.5); wires(-40,40,9.8,9.8,8.0,4,3)

# ---------------------------------------------------------------- villa dining room (interior)
def dining_chair(x,y,rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#3A2A20',.5,kind='wood'); cu=M('#D8C8A8',.9,kind='fabric')
    obox((0,0,.56),(.26,.25,.04),cu,.03,e); obox((0,.25,1.0),(.26,.035,.45),wd,.03,e); obox((0,.21,1.0),(.2,.02,.36),cu,.03,e)
    for dx in (-.22,.22):
        for dy in (-.21,.21): obox((dx,dy,.27),(.03,.03,.27),wd,.01,e)
    return e
def feast(cx=0,cy=0,z=1.02):
    r=random.Random(5); pl=M('#F8F6F0',.3,spec=.8); gd=M('#D9B24A',.3,metal=.8)
    B.box((cx,cy,z+.005),(2.3,.28,.005),M('#7A1F2E',.9,kind='fabric',h2='#D9B24A',sc=6),.0)
    def plate(x,y,rr=.2): B.cyl((x,y,z+.02),rr,.025,pl,seg=18); B.cyl((x,y,z+.03),rr*.72,.02,gd if rr>.25 else pl,seg=18)
    # biryani mound
    plate(cx-1.2,cy,.36); B.ico((cx-1.2,cy,z+.1),.27,M('#F2C14E',.8),sc=(1,1,.55),sub=2)
    for k in range(9): B.box((cx-1.2+r.uniform(-.18,.18),cy+r.uniform(-.18,.18),z+.2+r.uniform(0,.05)),(.05,.035,.03),M(r.choice(['#8A4A22','#F28A3A','#F4F1EA']),.7),.01,rot=(0,0,r.uniform(0,3)))
    karahi_obj((cx-.35,cy+.05,z+.02),1.25); karahi_obj((cx+1.75,cy-.02,z+.02),1.0)
    # roast chicken
    plate(cx+.55,cy,.33); B.ico((cx+.55,cy,z+.15),.2,M('#B5642A',.5,spec=.7),sc=(1.3,1,.75),sub=2)
    for s in (-1,1): B.cyl((cx+.55+.22,cy+s*.14,z+.2),.05,.2,M('#B5642A',.5,spec=.7),rot=(0,R(60),s*.5),seg=8,r2=.02)
    # naan stack, salad, kebabs, raita, jug, glasses
    plate(cx+1.2,cy+.02,.26)
    for k in range(5): B.cyl((cx+1.2+.02*k,cy+.02,z+.05+k*.022),.22,.02,M('#E8C88A',.8,h2='#B5642A',sc=9),seg=14)
    for (x,y) in ((cx-1.9,cy+.3),(cx+2.0,cy-.35)): plate(x,y,.2); [B.cyl((x-.1+j*.07,y,z+.06),.03,.24,M('#6A3A22',.8),rot=(R(90),0,.3),seg=6) for j in range(4)]
    plate(cx-.8,cy-.42,.17); B.ico((cx-.8,cy-.42,z+.06),.12,M('#4F9A3A',.8),sc=(1,1,.5),sub=1); B.ico((cx-.76,cy-.4,z+.1),.04,M('#E8554D',.6),sub=1)
    B.cyl((cx+.1,cy-.45,z+.06),.13,.1,pl,seg=14); B.cyl((cx+.1,cy-.45,z+.1),.115,.03,M('#F4F6F2',.4),seg=14)
    B.cyl((cx-1.65,cy-.4,z+.17),.085,.34,M('#BFD6E8',.05,spec=1.0,alpha=.4),seg=12); B.cyl((cx-1.65,cy-.4,z+.13),.075,.24,M('#F28A3A',.4,alpha=.85),seg=12)
    for (x,y) in ((-1.9,-.75),(-.95,-.75),(0,-.75),(.95,-.75),(1.9,-.75),(-1.9,.75),(-.95,.75),(0,.75),(.95,.75),(1.9,.75)):
        plate(cx+x,cy+y,.17); B.cyl((cx+x+.24,cy+y+(.1 if y<0 else -.1),z+.07),.04,.13,M('#BFD6E8',.05,spec=1.0,alpha=.35),seg=10)
def dining():
    fl=M('#EDE8DE',.25,kind='tile',h2='#DAD2C4',sc=1.1,spec=.8); wl=M('#F1ECE2',.85,kind='wall'); wd=M('#4A3426',.5,kind='wood'); gd=M('#D9B24A',.3,metal=.8)
    B.box((0,0,-.05),(5.5,4.2,.05),fl,0); B.box((0,0,3.65),(5.5,4.2,.05),M('#F6F3EC',.9),0)
    # back wall with a wide window (hills outside)
    B.box((0,4.2,.45),(5.5,.1,.45),wl,0); B.box((0,4.2,3.3),(5.5,.1,.35),wl,0); B.box((-4.4,4.2,1.9),(1.1,.1,1.1),wl,0); B.box((4.4,4.2,1.9),(1.1,.1,1.1),wl,0)
    for x in (-3.3,-1.1,1.1,3.3): B.box((x,4.16,1.9),(.04,.05,1.05),M('#F6F3EC',.6),.0)
    B.box((0,4.16,1.9),(3.3,.05,.03),M('#F6F3EC',.6),.0); B.box((0,4.22,1.9),(3.3,.01,1.05),M('#DCEAF2',.05,spec=1.0,alpha=.12),0)
    for sx in (-1,1): B.box((sx*3.75,4.0,1.9),(.38,.08,1.45),M('#C9A27A',.9,kind='fabric',h2='#B08A62',sc=8),.04)
    B.cyl((0,4.0,3.3),.03,8.0,gd,rot=(0,R(90),0),seg=6)
    B.box((-5.5,0,1.8),(.1,4.2,1.85),wl,0); B.box((5.5,-2.6,1.8),(.1,1.6,1.85),wl,0); B.box((5.5,2.3,1.8),(.1,1.9,1.85),wl,0); B.box((5.5,-.3,3.0),(.1,.75,.65),wl,0)
    B.box((5.52,-.3,1.18),(.04,.75,1.18),M('#5A3A22',.6,kind='wood'),.02)  # front door (closed leaf seen ajar)
    for z in (.9,): B.box((0,4.08,z+.02),(5.4,.03,.04),M('#F6F3EC',.6),.01); B.box((-5.38,0,z+.02),(.03,4.1,.04),M('#F6F3EC',.6),.01)
    # table + chairs
    B.box((0,0,.98),(2.6,.95,.04),wd,.03)
    for dx in (-2.3,2.3):
        for dy in (-.75,.75): B.box((dx,dy,.47),(.07,.07,.47),wd,.02)
    # chandelier
    B.cyl((0,0,3.3),.02,.7,gd,seg=6); B.cyl((0,0,2.9),.55,.05,gd,seg=18)
    for k in range(10): a=k*2*pi/10; B.ico((math.cos(a)*.55,math.sin(a)*.55,2.82),.07,M('#FFF2D0',.3,emit=5),sub=1); B.cyl((math.cos(a)*.3,math.sin(a)*.3,2.7),.015,.3,M('#EAF4FA',.05,spec=1.0,alpha=.5),seg=5)
    # sideboard + art + plant + rug + shoe rack by the door
    B.box((-5.0,1.2,.5),(.35,1.3,.5),wd,.03); B.box((-5.0,1.2,1.03),(.38,1.35,.03),M('#F4F1EA',.3,spec=.8),.01)
    B.cyl((-5.0,.6,1.25),.12,.4,M('#2B8A7A',.3,spec=.8),seg=12,r2=.07); B.cyl((-5.0,1.8,1.2),.16,.3,M('#F4F1EA',.3),seg=12)
    B.box((-5.38,1.2,2.3),(.03,.95,.6),M('#27364A',.7),.02); B.box((-5.36,1.2,2.3),(.02,.85,.5),M('#E8A46A',.7,h2='#2B8A7A',sc=3),.0)
    B.cyl((-4.6,-3.3,.35),.32,.7,M('#F4F1EA',.5),seg=12,r2=.24)
    for k in range(7): a=k*.9; B.box((-4.6+math.cos(a)*.35,-3.3+math.sin(a)*.35,1.35+.1*(k%3)),(.5,.12,.02),M('#3F8A4A',.8,kind='leaves'),.01,rot=(0,R(55),a))
    B.box((0,0,.006),(3.4,1.9,.006),M('#B8456A',.95,kind='fabric',h2='#27365A',sc=2.5),0)
    B.box((4.9,-1.9,.35),(.35,.6,.35),M('#F6F3EC',.5),.03); B.box((4.9,-1.9,.72),(.37,.62,.02),wd,.01)
    for k in range(3): B.box((4.9,-2.3+k*.4,.82),(.13,.09,.06),M(['#FAFAFA','#FAFAFA','#22242B'][k],.5),.03)
    B.box((4.3,-.3,.008),(.7,.5,.008),M('#C9B48A',.95,kind='fabric',h2='#7A1F2E',sc=5),0); stext('SHOES OFF',(5.36,-1.9,1.6),.14,'#7A1F2E',n=(-1,0,0))
    feast(0,0,1.02)
    # outside the window
    B.box((0,30,-.5),(80,24,.2),M('#6FA04C',.9,kind='grass',sc=.4),0)
    for x in (-9,-4,3,8,13,-14): pine(x,9+abs(x)*.4,1.3)
    hills(260,6,-30)

# ---------------------------------------------------------------- jeep with an opening door
def jeep(loc,rotz,col='#E9ECF2'):
    root=empty(loc,rot=(0,0,R(rotz))); body=M(col,.3,metal=.3,spec=.7); gl=M('#1A2433',.06,spec=1.0); bk=M('#16171C',.6); W=[]
    obox((0,0,.95),(2.15,.98,.42),body,.1,root); obox((-.35,0,1.75),(1.45,.93,.42),body,.1,root); obox((-.35,0,1.78),(1.47,.94,.3),gl,.05,root)
    obox((1.13,0,1.72),(.05,.86,.3),gl,.03,root,rot=(0,R(-16),0)); obox((2.17,0,.98),(.04,.55,.2),bk,.02,root)
    for sy in (-1,1):
        obox((2.17,sy*.72,1.0),(.04,.17,.13),M('#FFF6D8',.2,emit=2.5),.04,root); obox((-2.17,sy*.8,1.0),(.03,.1,.2),M('#E8301A',.3,emit=2.0),.02,root)
        obox((1.35,sy*1.0,.62),(.55,.06,.1),bk,.03,root); obox((-1.35,sy*1.0,.62),(.55,.06,.1),bk,.03,root); obox((0,sy*1.0,.5),(.75,.1,.04),M('#C9CED8',.3,metal=.9),.02,root)
        obox((-.35,sy*.94,2.2),(1.3,.03,.03),M('#C9CED8',.3,metal=.9),.01,root)
    obox((2.2,0,.56),(.08,.95,.12),M('#C9CED8',.3,metal=.9),.03,root); obox((-2.2,0,.56),(.08,.95,.12),bk,.03,root); wheel((-2.33,0,1.15),.4,.2,root)
    for (wx,sy) in ((1.35,-1),(1.35,1),(-1.35,-1),(-1.35,1)): W.append(wheel((wx,sy*.92,.5),.5,.3,root))
    # driver door on the -y (camera) side, hinged at its front edge
    hinge=empty((.55,-.99,0),root); obox((-.55,0,1.0),(.54,.03,.36),body,.04,hinge); obox((-.55,-.005,1.75),(.5,.02,.28),gl,.03,hinge); obox((-.95,-.04,1.25),(.07,.02,.025),M('#C9CED8',.3,metal=.9),.01,hinge)
    obox((0,-.95,1.4),(.54,.01,.75),M('#22242B',.8),0,root)  # dark cabin behind the door
    return dict(root=root,wheels=W,r=.5,hinge=hinge)
