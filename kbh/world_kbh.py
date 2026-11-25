# Sets for "Everyone Is a Bhaiya from Karachi"
# Geography: one long road along x (traffic both ways), north sidewalk y 2..5 with apartment blocks (shops below) at y>=5,
# south side buildings at y<=-10. Waleed walks toward +x (the airport). Biryani stall on north sidewalk at x=STALL_X.
# Airport terminal set at x=AIR_X, counter inside, parking lot in front (south).
BALLS=[]
ROAD_Y=(-7.0,2.0); NS=5.0; SS=-10.0; STALL_X=46.0; AIR_X=220.0
WIN_MATS=[]   # emissive window materials (for the blackout)
SHOP_SIGNS=['BHAIYA MOBILE ZONE','NEW STAR GENERAL STORE','AL-NOOR MEDICAL','KARACHI CLOTH HOUSE','PAAN CORNER','FAST PHOTOSTAT','ABDUL HAMEED TAILORS','CITY SWEETS','HAPPY TYRE SHOP','MAKKAH HARDWARE','RAFIQ ELECTRONICS','NOOR BAKERY']
def winmat(col,e): m=M(col,.2,emit=e); WIN_MATS.append((m,e)); return m
def apt_block(cx,w,floors,col,sign,scol,side,seed):
    """Karachi apartment block: ground-floor shop with shutter + sign, balconies, AC units, water tanks, dishes, washing lines"""
    r=random.Random(seed); s=side; FH=2.9; H=3.6+floors*FH; y0=(NS if s>0 else SS); yf=y0; yb=y0+6.0*s; yc=(yf+yb)/2
    wall=M(col,.88,kind='wall'); tr=M(shade(col,.82),.8); dk=M('#141820',.5)
    B.box((cx,yc,H/2),(w/2,3.0,H/2),wall,0)
    B.box((cx,yf-.05*s,H+.15),(w/2+.05,.1,.15),tr,.02)
    # roof: tanks + dish + railing
    for k in range(r.randint(1,3)):
        tx=cx-w/2+1+k*1.6+r.uniform(0,.4); B.cyl((tx,yc+s*r.uniform(-1,1),H+.75),.55,1.2,M(r.choice(['#2A2C34','#3A6EA8','#E8E2D0']),.6),seg=16)
    if r.random()<.7: B.cyl((cx+w/2-1.2,yf+1.0*s,H+.9),.45,.05,M('#E8E8EA',.4),seg=18,rot=(R(55),0,0)); B.cyl((cx+w/2-1.2,yf+1.2*s,H+.5),.03,.8,M('#9A9EA6',.4,metal=.6),seg=6)
    # ground floor shop
    shut=M('#8A9098',.45,metal=.6); B.box((cx,yf+.4*s,1.6),(w/2-.35,.06,1.4),dk,0)
    up=r.random()<.75
    B.box((cx,yf-.02*s,2.85 if up else 1.55),(w/2-.35,.05,.25 if up else 1.45),shut,0)
    if up:
        for k in range(5): B.box((cx-w/2+.8+k*(w-1.6)/4,yf+.6*s,.25+k%2*.9),(.28,.25,.25+k%2*.3),M(r.choice(['#C8372D','#2E6B4F','#E8C547','#5A7FB0','#F4F1EA','#E28A3A']),.7),.03)
        point((cx,yf+1.2*s,2.6),90,(1,.92,.8),r=.3)
    B.box((cx,yf-.12*s,3.35),(w/2-.2,.08,.38),M(scol,.45),.02); stext(sign,(cx,yf-.17*s,3.35),min(.34,(w-.8)/max(6,len(sign))*1.55),'#FFFFFF' if scol not in ('#E8C547','#F4F1EA','#F4D35E') else '#16171C',n=(0,-s,0))
    B.box((cx,yf-.5*s,3.0),(w/2,.5,.05),M(r.choice(['#2E8A6A','#C8372D','#2A5A9A','#E28A3A']),.7,kind='fabric'),.01)
    # upper floors: windows + balconies + AC units + laundry
    for f in range(floors):
        z=3.6+f*FH+1.4
        for k in range(int(w//2.2)):
            x=cx-w/2+1.1+k*2.2; lit=r.random()<.55
            B.box((x,yf-.03*s,z),(.6,.04,.6),winmat('#FFE6B0' if lit else '#9AB8D8',1.3 if lit else 0.0) if lit else M('#2A3A4E',.15,spec=.8),.02)
            B.box((x,yf-.06*s,z),(.66,.03,.66),tr,.01)
            if k%2==0:
                B.box((x,yf-.55*s,z-.72),(.95,.55,.06),M('#B8AE9C',.8,kind='concrete'),.01); B.box((x,yf-1.08*s,z-.42),(.95,.03,.28),M(r.choice(['#3A6E5A','#7A4A2E','#5A5E66']),.5,metal=.3),.0)
                if r.random()<.5:
                    for j in range(3): B.box((x-.6+j*.5,yf-.9*s,z-.15),(.16,.01,.22),M(r.choice(['#C8372D','#F4F1EA','#2E6BAF','#E8C547','#D9367A']),.9,kind='fabric'),.0)
            elif r.random()<.7: B.box((x+.5,yf-.25*s,z-.5),(.32,.22,.22),M('#E8E8EA',.5),.03); B.box((x+.5,yf-.47*s,z-.5),(.2,.01,.14),M('#9A9EA6',.5),0)
def wires_k(x0,x1,y,z,n,seed):
    r=random.Random(seed)
    for k in range(n): B.cyl(((x0+x1)/2,y+r.uniform(-.3,.3),z+r.uniform(-.4,.4)),.012,x1-x0,M('#16171C',.6),seg=5,rot=(0,R(90),0))
def crow(x,y,z,rz=0,parent=None):
    e=empty((x,y,z),parent,rot=(0,0,R(rz))); b=M('#1A1A1E',.5); g=M('#5A5E66',.6)
    obox((0,0,.09),(.13,.06,.07),b,.03,e); obox((.11,0,.15),(.06,.05,.05),g,.02,e); obox((.18,0,.15),(.04,.012,.012),M('#2A2C34',.4),0,e); obox((-.15,0,.1),(.07,.04,.015),b,.01,e)
    return e
def road(x0,x1):
    B.box(((x0+x1)/2,(ROAD_Y[0]+ROAD_Y[1])/2,-.06),((x1-x0)/2,(ROAD_Y[1]-ROAD_Y[0])/2,.06),M('#5E5C58',.85,kind='asphalt',sc=.6),0)
    B.box(((x0+x1)/2,(ROAD_Y[1]+NS)/2,.07),((x1-x0)/2,(NS-ROAD_Y[1])/2,.08),M('#B8AE9C',.85,kind='tile',sc=1.6,h2='#A89E8C'),.01)
    B.box(((x0+x1)/2,(ROAD_Y[0]+SS)/2,.07),((x1-x0)/2,(ROAD_Y[0]-SS)/2,.08),M('#B8AE9C',.85,kind='tile',sc=1.6,h2='#A89E8C'),.01)
    for k in range(int((x1-x0)/4)): B.box((x0+2+k*4,(ROAD_Y[0]+ROAD_Y[1])/2,.002),(1.0,.08,.003),M('#E8E2D0',.7),0)
    B.box(((x0+x1)/2,ROAD_Y[1]+.02,.08),((x1-x0)/2,.06,.09),M('#E8C547',.6),0)
    for k in range(int((x1-x0)/1.0)): B.box((x0+.5+k,ROAD_Y[0]-.02,.08),(.5,.06,.09),M('#16171C' if k%2 else '#F4F1EA',.6),0)
def city(x0=-30,x1=80,seed=3,rain=False):
    r=random.Random(seed); road(x0-10,x1+10)
    cols=['#E8D8C0','#C9D8D0','#E0C8B0','#D4D0C0','#C8D0DC','#E8E0C8','#D8C0B8','#C0C8B8']
    x=x0; i=0
    while x<x1:
        w=r.choice([6.0,7.0,8.0]); fl=r.choice([3,4,4,5])
        if not (STALL_X-5<x+w/2<STALL_X+5): apt_block(x+w/2,w,fl,cols[i%len(cols)],SHOP_SIGNS[i%len(SHOP_SIGNS)],r.choice(['#C8372D','#2E6B4F','#1E3FA0','#E8C547','#7A1E2E','#16171C']),1,seed*10+i)
        else: apt_block(x+w/2,w,fl,cols[i%len(cols)],'',r.choice(['#2E6B4F']),1,seed*10+i)
        apt_block(x+w/2+1.5,w,fl+r.choice([-1,0,1]),cols[(i+3)%len(cols)],SHOP_SIGNS[(i+5)%len(SHOP_SIGNS)],r.choice(['#C8372D','#2E6B4F','#1E3FA0','#E8C547']),-1,seed*20+i)
        x+=w; i+=1
    # poles, wire tangles, crows, trees, billboards
    for k in range(int((x1-x0)/9)):
        px=x0+4+k*9; B.cyl((px,NS-.6,4.6),.12,9.2,M('#8A8A88',.7,kind='concrete'),seg=8); B.box((px,NS-.6,8.6),(.05,1.2,.05),M('#5A5E66',.5,metal=.5),0)
        B.box((px,NS-1.3,7.7),(.35,.3,.4),M('#6E747C',.5,metal=.5),.03)
        B.cyl((px,SS+.6,4.6),.12,9.2,M('#8A8A88',.7,kind='concrete'),seg=8)
        if k%2==0: B.box((px,NS-1.6,8.0),(.6,.05,.08),M('#5A5E66',.5,metal=.5),0); B.box((px+.5,NS-1.8,7.9),(.25,.12,.05),winmat('#FFF4D8',0.0),.01)
    wires_k(x0,x1,NS-.6,8.0,6,seed); wires_k(x0,x1,SS+.6,8.0,5,seed+1);
    for k in range(int((x1-x0)/18)): B.cyl((x0+9+k*18,(NS+SS)/2,8.3),.01,abs(NS-SS)-1.2,M('#16171C',.6),seg=5,rot=(R(90),0,0))
    for k in range(int((x1-x0)/7)):
        tx=x0+3+k*7+r.uniform(-1,1)
        if abs(tx-STALL_X)>5 and r.random()<.55: tree(tx,NS-.9 if k%2 else SS+1.2,r.uniform(1.0,1.3),col=r.choice(['#4F8A3A','#5E9A3E','#3F7A3A']))
    for k in range(3):
        bx=x0+20+k*35; B.cyl((bx,SS-2,6),.18,12,M('#5A5E66',.5,metal=.5),seg=8); B.box((bx,SS-1.9,11.5),(3.2,.12,1.4),M('#F4F1EA',.6),.02)
        txt=['CHAI? HAAN BHAIYA','KARACHI WALON KA DIL BARA','BAS DO MINUTE TOURS'][k]; B.box((bx,SS-1.78,11.5),(3.05,.02,1.25),M(['#C8372D','#2E6B4F','#1E3FA0'][k],.5),0); stext(txt,(bx,SS-1.74,11.5),.36,'#FFFFFF',n=(0,1,0))
    # skyline beyond
    for k in range(14):
        hx=x0+k*(x1-x0)/13; hh=r.uniform(14,30); B.box((hx,NS+18+r.uniform(0,6),hh/2),(r.uniform(2.5,4.5),2.5,hh/2),M(r.choice(['#B8C0C8','#C8C0B0','#A8B0B8']),.85,kind='wall'),0)
        for j in range(int(hh/3)): B.box((hx,NS+15.4,1.5+j*3),(2.0,.02,.4),winmat('#FFE6B0',1.0) if r.random()<.4 else M('#5A6A7E',.2,spec=.6),0)
    B.done('city')
def stall():
    """BHAIYA BIRYANI CENTRE: cart with two daigs, plastic tables/chairs, tube lights, banner"""
    X=STALL_X; Y=NS-1.6
    wd=M('#7A5232',.5,kind='wood'); B.box((X,Y+.2,.55),(1.6,.55,.5),M('#C8372D',.5),.03); B.box((X,Y+.2,1.08),(1.65,.6,.04),M('#C9CED8',.3,metal=.7),.01)
    stext('BHAIYA BIRYANI CENTRE',(X,Y-.38,.62),.17,'#FFFFFF')
    for k,dx in enumerate((-.75,.75)):
        B.cyl((X+dx,Y+.25,1.42),.48,.62,M('#B8BCC4',.22,metal=.85),seg=24,r2=.42); B.cyl((X+dx,Y+.25,1.74),.43,.03,M('#E8A040' if k==0 else '#D86A2A',.8),seg=24)
        for j in range(8): B.box((X+dx+random.Random(j+k*9).uniform(-.28,.28),Y+.25+random.Random(j+k*19).uniform(-.28,.28),1.77),(.035,.035,.02),M(['#F4F1EA','#8A3A1A','#E8C547'][j%3],.7),.01)
    # canopy + banner + tube lights
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((X+sx*2.4,Y+.5+sy*1.3,1.4),.04,2.8,M('#9A9EA6',.4,metal=.6),seg=6)
    B.box((X,Y+.5,2.82),(2.55,1.45,.04),M('#2E6B4F',.7,kind='fabric'),.0)
    for k in range(10): B.box((X-2.45+k*.54,Y-.95,2.66),(.27,.02,.16),M('#E8C547' if k%2 else '#2E6B4F',.7,kind='fabric'),.0)
    B.box((X,Y-.97,2.25),(2.2,.02,.22),M('#F4F1EA',.5),0); stext('HAR PLATE MEIN BOTI',(X,Y-1.0,2.25),.16,'#C8372D')
    B.box((X,Y-.85,2.7),(.7,.03,.03),M('#F4FAFF',.1,emit=8),.01); point((X,Y-.4,2.4),220,(.93,.97,1),r=.3)
    return (X,Y)
STALL_TABLES=[(STALL_X-2.6,NS-4.0),(STALL_X+.2,NS-4.3),(STALL_X+2.9,NS-4.0)]
def stall_tables():
    for i,(x,y) in enumerate(STALL_TABLES):
        B.box((x,y,.7),(.6,.45,.03),M(['#E8E2D0','#2E8A6A','#E8C547'][i],.4),.02)
        for sx in (-1,1):
            for sy in (-1,1): B.cyl((x+sx*.52,y+sy*.38,.35),.02,.7,M(['#E8E2D0','#2E8A6A','#E8C547'][i],.4),seg=6)
def pchair_k(x,y,rz,col='#C8372D'):
    e=empty((x,y,0),rot=(0,0,R(rz))); m=M(col,.35)
    obox((0,0,.44),(.23,.23,.03),m,.03,e); obox((0,.21,.75),(.23,.03,.3),m,.03,e)
    for sx in (-1,1):
        for sy in (-1,1): obox((sx*.2,sy*.2,.22),(.025,.025,.22),m,0,e)
    return e
def rain_drops(n,center,size=(14,10),top=7.0,seed=8):
    r=random.Random(seed); mt=M('#C8D8E8',.1,alpha=.55); D=[]
    for i in range(n):
        o=obox((0,0,0),(.008,.008,.16),mt,0,None); D.append((o,r.uniform(-size[0]/2,size[0]/2),r.uniform(-size[1]/2,size[1]/2),r.uniform(0,1)))
    def upd(t,k=1.0):
        for o,dx,dy,ph in D:
            if k<=0: o.location=(0,0,-50); continue
            z=top-((t*9.0+ph*top)%top); o.location=(center[0]+dx+.4*z*.1,center[1]+dy,z)
    return upd
def flood_plane(x0,x1,y0,y1):
    w=obox(((x0+x1)/2,(y0+y1)/2,-1),((x1-x0)/2,(y1-y0)/2,.02),M('#5E6A6E',.03,spec=1.0),0,None); return w
# ---------------------------------------------------------------- airport
def airport():
    X=AIR_X; tg=M('#2A3A4E',.06,spec=1.0)
    B.box((X,8,-.05),(30,22,.05),M('#9A9890',.85,kind='asphalt',sc=.6),0)
    B.box((X,6,4),(22,1.2,4),M('#E8E8EA',.6,kind='wall'),0)
    for k in range(10): B.box((X-18+k*4,4.75,3.2),(1.7,.05,2.6),tg,.0)
    B.box((X,3.6,7.4),(23,3.2,.25),M('#F4F5FA',.5),.05)
    for k in range(8): B.cyl((X-19+k*5.4,2.0,3.6),.22,7.2,M('#C9CED8',.3,metal=.7),seg=12)
    B.box((X,4.5,6.4),(6.5,.1,.6),M('#1E3FA0',.5),.02); stext('KARACHI AIRPORT  •  DEPARTURES',(X,4.38,6.4),.5,'#FFFFFF')
    B.box((X,-.2,.1),(24,1.6,.12),M('#B8AE9C',.85,kind='tile',sc=1.6),.01)
    for k in range(7): palm(X-18+k*6,-1.8,1.1,seed=k)
    # inside counter (seen through a separate interior at y>12)
    B.box((X,16,-.04),(8,4,.04),M('#D8D4CC',.3,kind='tile',sc=1.4),0); B.box((X,20,3),(8,.1,3),M('#E8E8EA',.6,kind='wall'),0)
    for sx in (-1,1): B.box((X+sx*8,16,3),(.1,4,3),M('#E8E8EA',.6,kind='wall'),0)
    B.box((X,16,6.05),(8,4,.05),M('#F4F5FA',.6),0)
    B.box((X,17.2,.55),(3.0,.4,.55),M('#1E3FA0',.4),.03); B.box((X,17.2,1.12),(3.05,.45,.03),M('#F4F5FA',.3),.01)
    B.box((X,19.85,3.2),(3.5,.05,.6),M('#16171C',.4),.02); stext('CHECK-IN  •  FLIGHT KB-6:00  •  DELAYED',(X,19.8,3.2),.19,'#E8C547')
    for k in range(3): B.box((X-1.8+k*1.8,17.35,1.35),(.25,.06,.2),M('#16171C',.3),.01)
    for k in range(6): B.box((X-6.5+k*2.6,15.8,5.8),(.9,.04,.04),M('#F4FAFF',.1,emit=8),.01)
    point((X,15,5.4),260,(.95,.97,1),r=1.2)
    B.done('airport')
PARK_X=AIR_X; PARK_Y=-14.0
def parking():
    X=PARK_X; Y=PARK_Y
    B.box((X,Y,-.04),(18,9,.04),M('#6E6C68',.85,kind='asphalt',sc=.6),0)
    for k in range(12): B.box((X-16+k*3,Y+7.6,.005),(.05,1.4,.005),M('#E8E2D0',.6),0); B.box((X-16+k*3,Y-7.6,.005),(.05,1.4,.005),M('#E8E2D0',.6),0)
    for k in range(9): car((X-14+k*3.5,Y+7.6,0),90 if k%2 else -90,random.Random(k).choice(['#C8372D','#F4F1EA','#2A2C34','#3A6EA8','#C9CED8','#E8C547']),seed=k)
    for k in range(7): car((X-13+k*4.2,Y-7.6,0),-90,random.Random(k+20).choice(['#F4F1EA','#2E6B4F','#8A8A90','#C8372D']),seed=k+20)
    for k in range(4):
        px=X-12+k*8; B.cyl((px,Y,4),.1,8,M('#5A5E66',.5,metal=.5),seg=8); B.box((px,Y,8.05),(.4,.2,.08),M('#FFE6B0',.2,emit=4),.02)
    stumps=empty((X+5.5,Y,0))
    for k in range(3): ocyl((0,(k-1)*.11,.36),.022,.72,M('#E8D8B0',.5),stumps,seg=6)
    B.done('parking')
