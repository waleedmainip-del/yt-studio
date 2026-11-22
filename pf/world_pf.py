# Sets for "The Punjabi Family": the family lounge (sofas, TV wall, dining corner), Arslan's messy bedroom with a white fan,
# Allama-Iqbal-style departures hall (glass wall, counters, trolleys), aircraft cabin, phone video-call UI.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
def sofa(x,y,w=2.2,rz=0,col='#7A3A2A'):
    e=empty((x,y,0),rot=(0,0,R(rz))); m=M(col,.9,kind='fabric',h2=shade(col,.8),sc=4); wd=M('#4A2A18',.6,kind='wood')
    obox((0,0,.3),(w/2,.45,.16),m,.08,e); obox((0,.36,.75),(w/2,.12,.35),m,.08,e); obox((-w/2,0,.5),(.12,.45,.22),m,.06,e); obox((w/2,0,.5),(.12,.45,.22),m,.06,e)
    for dx in (-w/2+.1,w/2-.1): obox((dx,-.35,.07),(.05,.05,.07),wd,.01,e)
    for k in range(int(w/.75)): obox((-w/2+.45+k*.75,.18,.62),(.18,.08,.18),M('#D9B24A',.8,kind='fabric'),.06,e,rot=(R(-15),0,0))
    return e
def lounge():
    fl=M('#C8B8A0',.35,kind='tile',h2='#B8A890',sc=1.0,spec=.7); wl=M('#A8C8A0',.9,kind='wall'); wl2=M('#EFE6D2',.9,kind='wall')
    W_,D_=5.2,3.8
    B.box((0,0,-.05),(W_,D_,.05),fl,0); B.box((0,0,3.4),(W_,D_,.05),M('#F4F1EA',.9),0)
    B.box((0,D_,1.7),(W_,.1,1.7),wl,0); B.box((-W_,0,1.7),(.1,D_,1.7),wl2,0); B.box((W_,0,1.7),(.1,D_,1.7),wl2,0)
    B.box((0,D_-.12,.08),(W_,.03,.08),M('#5A3A22',.6,kind='wood'),0)
    # carpet + centre table
    B.box((0,.9,.008),(2.4,1.5,.008),M('#7A1F2E',.95,kind='fabric',h2='#2B3A6A',sc=2.4),0)
    B.box((0,.9,.38),(.9,.45,.03),M('#BFD6E8',.05,spec=1.0,alpha=.5),.02); B.box((0,.9,.2),(.85,.4,.02),M('#4A2A18',.6,kind='wood'),.01)
    for dx in (-.8,.8):
        for dy in (.55,1.25): B.box((dx,dy,.19),(.03,.03,.19),M('#C9A24A',.3,metal=.8),0)
    B.cyl((.3,.95,.47),.12,.14,M('#F4F1EA',.4),seg=12,r2=.1);
    for k in range(4): B.ico((.3+.05*math.cos(k*1.6),.95+.05*math.sin(k*1.6),.56),.04,M('#E8423A',.5),sub=1)
    # TV wall on the left, clock + photos on back wall, fridge on right in dining corner
    B.box((-W_+.25,0,.35),(.2,1.3,.35),M('#4A2A18',.6,kind='wood'),.03); B.box((-W_+.18,0,1.3),(.04,1.0,.58),M('#16171C',.3,spec=.8),.02); B.box((-W_+.15,0,1.3),(.01,.92,.5),M('#2A4A6A',.3,emit=.6),0)
    B.cyl((0,D_-.08,2.75),.32,.05,M('#F4F1EA',.5),rot=(R(90),0,0),seg=24); B.cyl((0,D_-.11,2.75),.3,.02,M('#16171C',.5),rot=(R(90),0,0),seg=24)
    for k in range(12): a=k*pi/6; B.box((math.sin(a)*.25,D_-.13,2.75+math.cos(a)*.25),(.012,.01,.03),M('#F4F1EA',.5),0,rot=(0,a,0))
    for (x,z,c) in ((-2.0,2.4,'#E8C88A'),(-1.3,2.6,'#9FC8E0'),(1.4,2.5,'#E8A0A0'),(2.1,2.3,'#A8D0A0')): B.box((x,D_-.07,z),(.28,.03,.22),M('#5A3A22',.6,kind='wood'),.02); B.box((x,D_-.1,z),(.22,.01,.16),M(c,.7),0)
    B.box((W_-.4,2.6,1.0),(.35,.4,1.0),M('#E8E8E4',.35),.04); B.box((W_-.76,2.6,1.35),(.01,.35,.25),M('#C9CED8',.3,metal=.8),0)
    # dining table for food packing
    B.box((3.4,.6,.78),(.9,.6,.04),M('#6A3A22',.5,kind='wood'),.03)
    for dx in (-.8,.8):
        for dy in (-.5,.5): B.box((3.4+dx,.6+dy,.38),(.04,.04,.38),M('#6A3A22',.5,kind='wood'),.01)
    # curtains + window on right wall
    B.box((W_-.05,-1.4,1.9),(.03,.9,.8),M('#9FC8E0',.05,spec=1.0,alpha=.3),0)
    for dy in (-2.45,-.35): B.box((W_-.12,dy,1.9),(.05,.25,1.4),M('#C8372D',.9,kind='fabric',h2='#7A1F2E',sc=6),.03)
    B.box((0,0,3.32),(.6,.6,.02),M('#FFFFFF',.3,emit=2.4),0)
    for x in (-5.0,5.0): pass
    sofa(0,2.85,2.6,0,'#7A3A2A'); sofa(-3.6,1.0,1.6,90,'#7A3A2A')
    B.box((-2.7,2.9,.45),(.3,.3,.45),M('#4A2A18',.6,kind='wood'),.02); B.cyl((-2.7,2.9,1.0),.12,.2,M('#D9B24A',.3,metal=.6),seg=10); B.cyl((-2.7,2.9,1.35),.25,.35,M('#F4E8C8',.8,emit=.6),seg=12,r2=.15)
def ceiling_fan_w(loc):
    e=empty(loc); ocyl((0,0,.18),.02,.36,M('#F4F1EA',.5),e,rot=(0,0,0),seg=6); ocyl((0,0,0),.14,.12,M('#F4F1EA',.4),e,rot=(0,0,0),seg=14); ocyl((0,0,-.08),.09,.04,M('#FFF2D0',.3,emit=2),e,rot=(0,0,0),seg=12)
    bl=empty((0,0,.01),e)
    for a in range(3): obox((math.cos(a*2.094)*.5,math.sin(a*2.094)*.5,0),(.46,.09,.012),M('#F4F1EA',.5),.02,bl,rot=(0,0,a*2.094))
    return bl
def bedroom():
    fl=M('#D8C8B0',.45,kind='wood',sc=.8); wl=M('#9FB8D8',.9,kind='wall')
    B.box((0,0,-.05),(3.6,3.0,.05),fl,0); B.box((0,0,3.2),(3.6,3.0,.05),M('#F4F1EA',.9),0)
    B.box((0,3.0,1.6),(3.6,.08,1.6),wl,0); B.box((-3.6,0,1.6),(.08,3.0,1.6),wl,0); B.box((3.6,0,1.6),(.08,3.0,1.6),wl,0)
    wd=M('#5A3A22',.6,kind='wood'); r=random.Random(3)
    B.box((-1.8,1.6,.28),(1.2,1.2,.28),wd,.03); B.box((-1.8,1.6,.62),(1.15,1.15,.1),M('#E8E2D6',.8,kind='fabric'),.05); B.box((-2.3,2.5,.78),(.5,.25,.1),M('#F4F1EA',.8,kind='fabric'),.05)
    B.box((-1.5,1.2,.78),(.8,.7,.08),M('#2B5AA8',.9,kind='fabric',h2='#F2C14E',sc=3),.05,rot=(0,0,R(20)))
    # mess: clothes piles, shoes, cricket bat, books, chips packet, laptop
    for k in range(9): B.box((r.uniform(-1,2.8),r.uniform(-2,2.5),.05+.02*k%3),(r.uniform(.2,.35),r.uniform(.15,.3),.04),M(r.choice(['#C8372D','#16171C','#F4F1EA','#2B8A5A','#7448C2','#F2C14E']),.9,kind='fabric'),.03,rot=(0,0,r.uniform(0,3)))
    for k in range(4): B.box((r.uniform(0,2.5),r.uniform(-1.5,1.5),.06),(.14,.06,.06),M(r.choice(['#F4F5FA','#16171C']),.5),.03,rot=(0,0,r.uniform(0,3)))
    B.box((3.3,2.6,.55),(.06,.1,.55),M('#D9B48A',.6,kind='wood'),.02,rot=(0,R(-12),0))
    B.box((2.6,2.6,.4),(.6,.35,.4),wd,.02); B.box((2.6,2.6,.82),(.25,.18,.02),M('#2A2C34',.3,metal=.5),.01)
    for k in range(5): B.box((2.2+.12*k,2.65,.9+.05*k),(.05,.15,.11),M(['#C8372D','#2B5AA8','#F2C14E','#35975A','#F4F1EA'][k],.6),.01)
    B.box((0,2.95,1.9),(.5,.02,.7),M('#16171C',.6),.01); stext('CANADA',(0,2.93,2.3),.12,'#E8423A',e=.5); B.box((0,2.93,1.8),(.35,.01,.35),M('#E8423A',.6),0)
    B.box((-3.55,0,1.9),(.02,.7,.5),M('#9FC8E0',.05,spec=1.0,alpha=.3),0); B.box((-3.5,0,1.9),(.03,.75,.55),M('#F4F1EA',.5),0)
    B.box((1.6,-2.9,1.5),(.6,.08,1.5),M('#8A6A4A',.6,kind='wood'),.02)
def airport():
    fl=M('#D8D6D0',.25,kind='tile',h2='#C8C6C0',sc=.7,spec=.9); r=random.Random(8)
    B.box((0,0,-.05),(30,14,.05),fl,0); B.box((0,0,8.0),(30,14,.2),M('#E8E8E4',.6),0)
    for x in range(-24,25,6): B.box((x,0,7.75),(.2,14,.15),M('#C9CED8',.3,metal=.8),0)
    # glass wall at the back with apron + aircraft tail outside
    B.box((0,12,4),(30,.05,4),M('#BFD6E8',.05,spec=1.0,alpha=.18),0)
    for x in range(-28,29,4): B.box((x,12,4),(.08,.1,4),M('#8A8E96',.3,metal=.8),0)
    B.box((0,12,2.6),(30,.08,.06),M('#8A8E96',.3,metal=.8),0)
    B.box((0,30,-.1),(60,18,.1),M('#6E7078',.85,kind='asphalt'),0)
    e=empty((4,22,0)); obox((0,0,2.6),(10,1.4,1.4),M('#F4F5FA',.4),.6,e); obox((-9,0,5.0),(1.6,.12,2.4),M('#2B8A5A',.4),.1,e,rot=(0,R(-20),0)); obox((0,0,2.0),(10,1.42,.25),M('#2B8A5A',.4),.1,e)
    obox((-1,0,1.8),(1.6,8.0,.18),M('#E8E8E4',.4),.05,e);
    for k in range(14): obox((8-k*1.2,-1.42,3.0),(.18,.02,.16),M('#1A2433',.1,spec=1),.05,e)
    # departures board + counters + signs
    B.box((-6,9,5.3),(3.2,.12,1.0),M('#16171C',.5),.04); stext('DEPARTURES',(-6,8.86,6.0),.3,'#F2C14E',e=1.5)
    for k,(a,b) in enumerate((('PK 781  TORONTO','ON TIME'),('PK 203  DUBAI','BOARDING'),('PK 757  LONDON','DELAYED'))): stext(a,(-7.2,8.86,5.55-k*.4),.18,'#F4F1EA',e=1.2); stext(b,(-4.4,8.86,5.55-k*.4),.18,['#35C85A','#F2C14E','#E8423A'][k],e=1.4)
    for k in range(4):
        x=2+k*3.0; B.box((x,8.2,.55),(1.1,.5,.55),M('#E8E8E4',.4),.04); B.box((x,8.6,1.9),(1.0,.08,.3),M('#2B8A5A',.5),.02); stext('COUNTER %d'%(k+1),(x,8.5,1.9),.14,'#FFFFFF',e=.6)
        B.box((x,8.0,1.2),(.25,.18,.15),M('#16171C',.4),.02)
    for k in range(10): B.box((-12+k*2.2,4.5,.5),(.05,.05,.5),M('#C9CED8',.3,metal=.8),0)
    B.box((-2,4.5,.92),(10,.02,.03),M('#2B5AA8',.5),0)
    stext('ALL PASSENGERS  >  GATE 12',(6,11.8,6.6),.3,'#F4F1EA',e=1.2); B.box((6,11.9,6.6),(3.0,.05,.3),M('#2B8A5A',.5),.02)
    for (x,y) in ((-10,6),(11,6),(-13,-3)): B.cyl((x,y,.35),.4,.7,M('#F4F1EA',.5),seg=12,r2=.35); B.ico((x,y,1.3),.6,M('#3F8A4A',.85,kind='leaves'),sc=(1,1,1.4),sub=1)
    for k in range(6): B.box((-12+k*.7,-4,.45),(.3,.3,.04),M('#2B5AA8',.4),.02);
    B.box((-10.2,-4.2,.25),(2.2,.05,.25),M('#5A5E66',.3,metal=.7),0)
    for k in range(8): B.box((0,0,7.6),(.6,.6,.02),M('#FFFFFF',.3,emit=3.0),0) if False else B.box((-21+k*6,4,7.6),(.6,.6,.02),M('#FFFFFF',.3,emit=3.0),0)
def trolley(e,s=1.0):
    st=M('#C9CED8',.3,metal=.8); obox((0,0,.35),(.45,.3,.03),st,.01,e)
    for dx in (-.4,.4):
        for dy in (-.25,.25): ocyl((dx,dy,.1),.06,.04,M('#16171C',.6),e,rot=(R(90),0,0),seg=10)
    obox((-.45,0,.75),(.03,.3,.4),st,.01,e); ocyl((-.5,0,1.15),.02,.6,st,e,rot=(R(90),0,0),seg=6)
    cols=['#2B5AA8','#C8372D','#16171C','#7448C2','#F2C14E']
    for k in range(4): obox((.05,0,.5+k*.22),(.35-.03*k,.26,.1),M(cols[k],.6,kind='fabric'),.04,e)
def cabin():
    fl=M('#3A4A6A',.9,kind='fabric',sc=3); wl=M('#E8E6E0',.5)
    B.box((0,0,-.05),(2.0,12,.05),fl,0)
    for s in (-1,1): B.box((s*2.0,0,1.3),(.1,12,1.5),wl,0)
    B.box((0,0,2.75),(2.0,12,.08),wl,0)
    for s in (-1,1): B.box((s*1.4,0,2.3),(.55,12,.2),M('#D8D6D0',.5),.05)
    for k in range(10):
        y=-8+k*1.6
        for s in (-1,1):
            B.box((s*1.94,y,1.45),(.04,.22,.3),M('#9FC8E8',.2,emit=.8),.06)
            for j in range(3):
                x=s*(.55+j*.45); B.box((x,y,.45),(.2,.25,.06),M('#2B3A6A',.8,kind='fabric'),.03); B.box((x,y+.25,.95),(.2,.06,.5),M('#2B3A6A',.8,kind='fabric'),.03); B.box((x,y+.27,1.4),(.18,.07,.08),M('#F4F1EA',.8),.02)
        B.box((0,y,2.65),(.1,.05,.02),M('#FFFFFF',.3,emit=2),0)
def phone_call(kind='incoming'):
    root=empty((0,0,-200)); ui=lambda c,e=1.2: M(c,.6,emit=e,spec=0)
    obox((0,.1,0),(1.25,.08,2.45),M('#16171C',.3,spec=.9),.18,root); obox((0,0,0),(1.12,.01,2.3),ui('#1A2A20',.8),.0,root)
    obox((0,-.02,2.15),(.25,.01,.04),ui('#000000',0),.02,root)
    oico((0,-.03,.8),.42,ui('#C9905F',1.0),root,sub=2,sc=(1,.2,1)); obox((0,-.05,1.05),(.32,.02,.12),ui('#4A4440',1.0),.04,root); obox((0,-.06,.62),(.18,.02,.05),ui('#2A1A12',1.0),.02,root)
    for sx in (-1,1): ocyl((sx*.14,-.06,.85),.05,.01,ui('#FFFFFF',1.5),root,seg=12); ocyl((sx*.14,-.07,.85),.025,.01,ui('#1A1411',.5),root,seg=10)
    text('ABBA',(0,-.03,.05),(0,-1,0),.28,ui('#FFFFFF',1.6),ex=0,parent=root); text('Video call...',(0,-.03,-.28),(0,-1,0),.14,ui('#9FE8B0',1.4),ex=0,parent=root)
    for x,c in ((-.5,'#E8423A'),(.5,'#35C85A')): ocyl((x,-.03,-1.4),.2,.01,ui(c,2.2),root,seg=20)
    rings=[ocyl((0,-.025,.8),.5,.004,M('#FFFFFF',.6,emit=1.2,alpha=.4),root,seg=24) for k in range(2)]
    return dict(root=root,ring=rings)
