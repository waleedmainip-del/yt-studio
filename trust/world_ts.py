# sets for "Not everyone in Karachi is your friend"
UMB=['#C0392B','#2E86C1','#27AE60','#E67E22','#8E44AD','#16A0A0','#F4F1EA']
def umbrella(x,y,col,h=2.4,r_=1.3):
    B.cyl((x,y,h/2),.04,h,M('#5A5F66',.5,metal=.5),seg=6)
    for k in range(8):
        a=2*pi*k/8; B.box((x+math.cos(a)*r_*.5,y+math.sin(a)*r_*.5,h-.1),(r_*.5,.32*r_,.02),M(col if k%2 else '#F4F1EA',.8,kind='fabric'),.01,rot=(0,R(-14),a))
def cart(x,y,seed,kind=None):
    r=random.Random(seed); kind=kind or r.choice(['fruit','veg','corn','juice','bangles','toys'])
    B.box((x,y,.85),(.9,.5,.06),M('#7A5A3A',.7,kind='wood'),.02)
    for dx in (-.75,.75):
        for dy in (-.4,.4): B.cyl((x+dx,y+dy,.42),.03,.84,M('#5A5F66',.5,metal=.5),seg=6)
    for dx in (-.7,.7): B.cyl((x+dx,y-.55,.25),.25,.06,M('#2B2C33',.6),rot=(R(90),0,0),seg=14)
    cols={'fruit':['#E2562E','#F2C12E','#5FA84A','#C9302C'],'veg':['#5FA84A','#3E8E4A','#C9302C','#F28A2E'],'corn':['#F2C12E','#E8C25A'],'juice':['#F28A2E','#E84393','#5FA84A'],
          'bangles':['#E84393','#8E44AD','#2E86C1','#F2C12E','#C9302C'],'toys':['#E2562E','#2E86C1','#F2C12E','#27AE60']}[kind]
    for i in range(18):
        c=r.choice(cols)
        if kind in ('juice',): B.cyl((x-.7+(i%6)*.28,y-.15+(i//6)*.15,.98),.05,.18,M(c,.3,alpha=.8),seg=8)
        elif kind=='bangles': B.cyl((x-.7+(i%6)*.28,y-.2+(i//6)*.2,.92),.08,.02,M(c,.3,metal=.5),seg=12)
        elif kind=='toys': B.box((x-.7+(i%6)*.28,y-.2+(i//6)*.2,.98),(.08,.06,.08),M(c,.5),.02)
        else: B.ico((x-.7+(i%6)*.28+r.uniform(-.05,.05),y-.25+(i//6)*.22,.97+r.uniform(0,.06)),.09,M(c,.5),sub=1)
    umbrella(x,y,r.choice(UMB))
def clocktower(x,y,s=1.0):
    ST=M('#C9A27A',.85,kind='concrete',sc=.4); WT=M('#E8DCC0',.6)
    B.box((x,y,6*s),(3*s,3*s,6*s),ST,.04); B.box((x,y,12.5*s),(2.4*s,2.4*s,.5*s),WT,.03)
    B.box((x,y,15.5*s),(2.0*s,2.0*s,3*s),ST,.04)
    for k in range(4):
        a=k*pi/2; B.cyl((x+math.sin(a)*2.02*s,y-math.cos(a)*2.02*s,15.8*s),1.2*s,.06,M('#F4F1EA',.4),rot=(R(90),0,a),seg=24)
        B.box((x+math.sin(a)*2.1*s,y-math.cos(a)*2.1*s,16.0*s),(.04*s,.02,.7*s),M('#1E1E22',.4),0,rot=(0,0,a))
    B.cyl((x,y,19.6*s),1.6*s,1.2*s,ST,seg=4,rot=(0,0,R(45)))
    B.cyl((x,y,21.5*s),.2*s,2.6*s,M('#8A6A4A',.6),seg=8,r2=.02)
    for k in range(10): B.box((x-2.6*s+k*.58*s,y-3.02*s,4*s),(.15*s,.04,1.6*s),M('#2A1E18',.9),0)
def market(seed=41):
    ph=street(-30,30,seed,shops=.95)
    r=random.Random(seed)
    for i in range(14):
        x=-26+i*4+r.uniform(-.6,.6); side=r.choice((-1,1)); cart(x,side*3.6,seed*10+i)
    clocktower(0,46,1.3)
    return ph
def teastall():
    """roadside dhaba: counter with kettle at y=+3.2, benches; street behind"""
    WD=M('#7A5A3A',.7,kind='wood'); B2=B
    B2.box((0,3.6,.6),(1.8,.5,.6),M('#C0392B',.6),.03); B2.box((0,3.6,1.24),(1.85,.55,.04),M('#5A5F66',.3,metal=.5),.01)
    B2.cyl((-.8,3.5,1.45),.35,.4,M('#C9CDD6',.25,metal=.9),seg=18,r2=.25); B2.cyl((-.8,3.5,1.3),.4,.1,M('#2B2C33',.5),seg=18)
    for k in range(8): B2.cyl((.2+k*.18,3.4,1.32),.05,.1,M('#F4F1EA',.3,alpha=.7),seg=10)
    B2.box((0,4.1,2.6),(2.3,.04,.5),M('#16A0A0',.6),.02); text('CHAI KHANA',(0,4.05,2.6),(0,-1,0),.22,M('#F4F1EA',.4),ex=.004)
    B2.box((0,3.4,2.95),(2.4,1.0,.03),M('#2E86C1',.8,kind='fabric'),.01,rot=(R(-8),0,0))
    for x in (-1.8,1.8): B2.cyl((x,2.6,1.5),.04,3.0,M('#5A5F66',.5,metal=.5),seg=6)
    for y in (0.6,-1.4):
        B2.box((0,y,.42),(1.6,.25,.04),WD,.02)
        for dx in (-1.4,1.4): B2.box((dx,y,.2),(.04,.2,.2),WD,0)
    B2.box((0,-.4,.62),(.9,.4,.03),WD,.02); B2.cyl((0,-.4,.3),.05,.6,M('#5A5F66',.5),seg=6)
    for k in range(3): B2.ico((-1.2+k*.35,3.3,1.9),.07,M('#FFE6B0',.3,emit=12),sub=1)
def mechanic_shop(x,y):
    """open-front mechanic shop at facade y (north side facing -y)"""
    B.box((x,y+1.2,1.4),(2.2,1.2,1.4),M('#2A2622',.9),0)
    for k in range(5): B.cyl((x-1.6+k*.8,y+.3,.35),.32,.12,M('#1E1E22',.7),rot=(R(90),0,0),seg=16)
    B.box((x+1.2,y+.6,.5),(.4,.3,.5),M('#C0392B',.5,metal=.3),.03)
    B.box((x,y-.05,3.0),(2.3,.06,.35),M('#F2C12E',.5),.02); text('AUTO REPAIR',(x,y-.1,3.0),(0,-1,0),.2,M('#1E1E22',.4),ex=.004)
    B.ico((x-1.0,y-.3,2.6),.1,M('#FFF2D8',.3,emit=25),sub=1); B.ico((x+1.0,y-.3,2.6),.1,M('#FFF2D8',.3,emit=25),sub=1)
def doorway(x,y):
    """home door (green) in a facade at y facing -y with lamp"""
    B.box((x,y,1.3),(.7,.06,1.3),M('#1F6B4A',.6,kind='wood',sc=2),.02); B.box((x,y-.05,2.75),(.95,.1,.15),M('#E8DCC0',.6),.02)
    B.ico((x+1.0,y-.25,2.5),.12,M('#FFE6B0',.3,emit=18),sub=1); B.box((x,y-.3,.08),(1.0,.35,.08),M('#B8B0A0',.8),.01)
