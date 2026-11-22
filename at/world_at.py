# Sets for "Ashraf Tawa Takes Over" (invented local legend): old-Lahore mohalla chowk with a mud akhara and posters,
# a desi gym, a barber shop, Dadi's courtyard.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
def poster(loc,n=(0,-1,0),s=1.0,rz=0,col='#C8372D',tag='ASHRAF TAWA'):
    e=empty(loc,rot=(0,0,R(rz))); obox((0,0,0),(.42*s,.01,.6*s),M('#F2E6C8',.85),.0,e); obox((0,-.012,.12*s),(.36*s,.005,.4*s),M(col,.7),0,e)
    oico((0,-.02,.28*s),.13*s,M('#1A1411',.6),e,sc=(1,.2,1),sub=1); obox((0,-.02,-.02*s),(.22*s,.005,.14*s),M('#1A1411',.6),.02,e)
    obox((0,-.025,.24*s),(.12*s,.004,.025*s),M('#D9B24A',.3,emit=.5),.0,e); obox((0,-.026,.2*s),(.1*s,.004,.02*s),M('#1A1411',.6),0,e)
    text(tag,(0,-.03,-.42*s),(0,-1,0),.09*s,M('#1A1411',.5),ex=.003,parent=e); return e
def old_house(cx,w,Y,s,seed,h=None):
    r=random.Random(seed); c=r.choice(['#C9A27A','#B8896A','#D4B48C','#A87A5A','#C8B090']); h=h or r.choice([7,8.5,10]); yc=Y+s*3
    B.box((cx,yc,h/2),(w/2-.04,3,h/2),M(c,.95,kind='wall',h2=shade(c,.8),sc=.6),0)
    for f in range(1,int(h/3)):
        z=f*3.0; B.box((cx,Y-s*.5,z),(w*.3,.5,.06),M('#6A4A30',.7,kind='wood'),.02)
        for k in range(int(w*.6/.22)): B.box((cx-w*.3+.1+k*.22,Y-s*.95,z+.45),(.03,.03,.42),M('#5A3A22',.6,kind='wood'),0)
        B.box((cx,Y-s*.95,z+.9),(w*.3,.04,.04),M('#5A3A22',.6,kind='wood'),0)
        B.box((cx,Y-s*.02,z+1.4),(.45,.04,.7),M('#3A2A1E',.6,kind='wood'),.02)
    B.box((cx,Y-s*.03,1.2),(.7,.05,1.2),M(r.choice(['#2B5A8A','#3A6A3A','#7A2F2F','#5A3A22']),.6,kind='wood'),.02)
    B.box((cx,Y-s*.04,2.55),(.85,.08,.2),M(shade(c,.8),.8),.03)
    if r.random()<.6: B.cyl((cx+r.uniform(-1,1),yc,h+.6),.5,1.0,M('#2A2C34',.5),seg=10)
def chowk():
    r=random.Random(4)
    B.box((0,0,-.05),(40,20,.05),M('#9A8268',.95,kind='tile',h2='#8A7258',sc=.9),0)
    # akhara: sunken mud ring with a low brick rim
    B.cyl((0,4,.02),3.4,.06,M('#A8744A',.95,kind='concrete',sc=.4),seg=40); B.cyl((0,4,.12),3.6,.24,M('#8A4A30',.9,kind='tile',h2='#6A3A22',sc=3),seg=40)
    B.cyl((0,4,.13),3.4,.26,M('#A8744A',.95,kind='concrete',sc=.4),seg=40)
    for k in range(14):
        a=k*2*pi/14; x=math.cos(a)*4.2; y=4+math.sin(a)*4.2
        if y<3.0: continue
        B.box((x,y,.2),(.5,.2,.2),M('#C9A27A',.8,kind='wood'),.03,rot=(0,0,a+pi/2))
    # houses around three sides
    x=-20
    while x<20: w=r.choice([5,6,7]); old_house(x+w/2,w,10.5,1,int(x*7)+50); x+=w
    for s in (-1,1):
        y=-8
        while y<10: w=r.choice([5,6,7]); B.box((s*15,y+w/2,4),(3,w/2-.05,4+r.uniform(0,2)),M(r.choice(['#C9A27A','#B8896A','#D4B48C']),.95,kind='wall'),0); y+=w
    # posters + bunting + banner
    for (x,z) in ((-9,2.0),(-5,2.3),(6.5,2.1),(10,2.2),(-13,1.9)): poster((x,10.45,z),s=1.2,col=r.choice(['#C8372D','#2B5AA8','#2B8A5A']))
    for k in range(3):
        y=6.5+k*2.0
        for j in range(24):
            f=j/23; x=-12+24*f; z=6.2-.8*math.sin(pi*f)
            B.box((x,y,z),(.12,.01,.16),M(['#C8372D','#F2C14E','#2B8A5A','#2B5AA8','#F4F1EA'][j%5],.8,kind='fabric'),0,rot=(0,0,0))
    B.box((0,10.4,5.6),(4.0,.05,.5),M('#F2C14E',.6),.03); stext('DANGAL  -  MOHALLA CHOWK',(0,10.34,5.6),.3,'#7A1F1F')
    # tea stall + parked bikes + cart + pigeons
    B.box((-11,6,.55),(1.2,.6,.55),M('#3A6A3A',.6,kind='wood'),.03); B.cyl((-11.4,6,1.25),.22,.3,M('#C9CED8',.3,metal=.8),seg=12)
    B.box((11,6.2,.5),(1.0,.5,.08),M('#7A5236',.7,kind='wood'),.02)
    for dx in (-.8,.8): B.cyl((11+dx,5.6,.32),.32,.06,M('#2A2C34',.6),rot=(R(90),0,0),seg=12)
    for k in range(12): B.box((r.uniform(-12,12),r.uniform(-5,9),.12),(.12,.07,.08),M(r.choice(['#7A7E88','#9AA0A8','#5A5E66']),.7),.03,rot=(0,0,r.uniform(0,3)))
    pole(-13,8,8.5); pole(13,8,8.5); wires(-15,15,8,8,8.0,4,3)
    for (x,y) in ((-13.5,-5),(13.5,-4)): tree(x,y,1.4,'#4E7E3A','#5A3E28')
def dhol_obj(e,s=1.0):
    ocyl((0,-.25,0),.25*s,.5*s,M('#8A4A2A',.6,kind='wood'),e,rot=(0,R(90),0),seg=16);
    for sx in (-1,1): ocyl((sx*.26*s,-.25,0),.26*s,.02,M('#E8DCC0',.7),e,rot=(0,R(90),0),seg=16)
    for k in range(6): obox((0,-.25,0),(.26*s,.005,.005),M('#D9B24A',.4),0,e,rot=(R(30*k),0,0))
def gym():
    fl=M('#2A2C30',.8,kind='concrete',sc=.6); wl=M('#7A8A8A',.9,kind='wall')
    B.box((0,0,-.05),(4,3,.05),fl,0); B.box((0,3,1.6),(4,.08,1.6),wl,0); B.box((-4,0,1.6),(.08,3,1.6),wl,0); B.box((4,0,1.6),(.08,3,1.6),wl,0); B.box((0,0,3.2),(4,3,.05),M('#5A5E66',.9),0)
    B.box((1.6,2.9,1.6),(1.8,.02,1.0),M('#BFD6E8',.05,spec=1.0),.0)
    for x in (-2.8,-1.6): B.box((x,2.6,.7),(.3,.35,.7),M('#3A3D44',.4,metal=.6),.02)
    for k in range(6): B.cyl((-2.2+k*.15,2.7,.9+.0),.18-.01*k,.05,M('#16171C',.5,metal=.4),rot=(0,R(90),0),seg=14)
    B.box((0,1.0,.5),(1.1,.3,.06),M('#2A2C34',.5),.02); B.box((0,1.0,.25),(.06,.06,.25),M('#5A5E66',.4,metal=.6),0)
    B.cyl((0,1.0,1.35),.02,2.0,M('#C9CED8',.3,metal=.9),rot=(0,R(90),0),seg=8)
    for sx in (-1,1): B.cyl((sx*.9,1.0,1.35),.25,.08,M('#16171C',.5),rot=(0,R(90),0),seg=16)
    for sx in (-1,1): B.box((sx*1.0,1.0,.7),(.05,.05,.7),M('#C8372D',.5,metal=.4),0)
    poster((-1.0,2.9,2.0),s=1.6,col='#C8372D',tag='BE LIKE ASHRAF'); stext('PEHLWAN GYM',(1.6,2.86,2.85),.3,'#F2C14E',e=.6)
    B.box((0,0,3.12),(.6,.6,.02),M('#FFFFFF',.3,emit=3),0)
    for k in range(4): B.box((3.9,-1.8+k*.9,1.4),(.05,.3,.3),M(['#C8372D','#F2C14E','#2B5AA8','#2B8A5A'][k],.5),.02)
def barber():
    fl=M('#E8E2D6',.4,kind='tile',h2='#2A2C34',sc=1.6,spec=.6); wl=M('#9FD0C8',.9,kind='wall')
    B.box((0,0,-.05),(4,3,.05),fl,0); B.box((0,3,1.6),(4,.08,1.6),wl,0); B.box((-4,0,1.6),(.08,3,1.6),wl,0); B.box((4,0,1.6),(.08,3,1.6),wl,0); B.box((0,0,3.2),(4,3,.05),M('#F4F1EA',.9),0)
    B.box((0,2.9,1.7),(3.0,.02,.7),M('#DCEAF2',.05,spec=1.0),0); B.box((0,2.85,.9),(3.0,.2,.04),M('#F4F1EA',.4),.01)
    for x in (-1.5,1.5):
        B.cyl((x,2.0,.25),.25,.5,M('#C9CED8',.3,metal=.9),seg=12); B.box((x,2.0,.62),(.35,.32,.08),M('#C8372D',.4,spec=.6),.04); B.box((x,2.32,1.0),(.33,.06,.45),M('#C8372D',.4,spec=.6),.04)
    for k in range(6): B.cyl((-1.2+k*.25,2.82,1.02),.04,.16,M(['#2B5AA8','#F2C14E','#35975A','#C8372D','#F4F1EA','#7448C2'][k],.3,spec=.8),seg=8)
    poster((2.9,2.9,2.3),s=1.1,col='#2B5AA8',tag='ASHRAF CUT  Rs 300'); stext('HAIR CUT  150',(-2.6,2.86,2.6),.18,'#7A1F1F')
    B.cyl((-3.7,2.6,1.6),.08,1.2,M('#F4F1EA',.4,kind='fabric',h2='#C8372D',sc=6),seg=10)
    B.box((0,0,3.12),(.8,.3,.02),M('#FFFFFF',.3,emit=3),0)
def courtyard():
    fl=M('#B8896A',.9,kind='tile',h2='#A87A5A',sc=1.3); wl=M('#E6CFA8',.95,kind='wall')
    B.box((0,0,-.05),(5,4,.05),fl,0); B.box((0,4,1.8),(5,.1,1.8),wl,0); B.box((-5,0,1.8),(.1,4,1.8),wl,0); B.box((5,0,1.8),(.1,4,1.8),wl,0)
    B.box((0,3.92,1.2),(.7,.05,1.2),M('#3A6A8A',.6,kind='wood'),.02)
    # takht (wooden platform) + gao takiya + hookah-free tea tray, clay pots, tulsi, clothes line, sun
    B.box((0,2.2,.25),(1.4,.8,.25),M('#6A3A22',.6,kind='wood'),.03); B.box((0,2.2,.53),(1.38,.78,.03),M('#F4F1EA',.8,kind='fabric',h2='#2B5AA8',sc=5),.02)
    B.cyl((0,2.85,.75),.2,1.3,M('#8E1F2A',.9,kind='fabric',h2='#D9B24A',sc=5),rot=(0,R(90),0),seg=12)
    for (x,y,r_) in ((-4,3.2,.35),(-3.4,3.4,.28),(4.1,3.1,.4)): B.cyl((x,y,r_),r_,r_*2,M('#B5603F',.85,kind='concrete',sc=.5),seg=12,r2=r_*.55)
    B.box((3.2,1.4,.45),(.3,.3,.45),M('#D8C8A8',.9,kind='wall'),.02); B.ico((3.2,1.4,1.1),.35,M('#3F7A3A',.85,kind='leaves'),sub=1)
    for k in range(5): B.box((-2.5+k*.5,3.6,2.6-.05*math.sin(k)),(.2,.01,.35),M(['#E8554D','#F4F1EA','#4D8FE8','#F2C14E','#CF3F78'][k],.9,kind='fabric'),0)
    B.cyl((-1.5,3.6,2.95),.006,3.2,M('#16171C',.6),rot=(0,R(90),0),seg=4)
    poster((-3.2,3.88,1.9),s=1.0,col='#2B8A5A'); tree(-6.8,6,1.3,'#4E7E3A','#5A3E28'); B.box((0,8,3),(10,.3,3),M('#C9A27A',.95,kind='wall'),0)
