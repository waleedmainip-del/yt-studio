# Sets for "Darzi Ka Kal": bazaar with MASTER TAILORS shop (inside + street), Waleed's courtyard (x=60), Eidgah (x=150).
BALLS=[]
SHOP_W=2.6; SHOP_Y0=2.0; SHOP_Y1=6.2; SHOP_H=3.4
CURT=(1.75,5.0); COUNTER_Y=3.0; MACHINE=(-1.55,4.6)
def strlights(x0,x1,y,z,cols=('#FFD24A','#FF5A8A','#5AD0FF','#8AFF7A'),n=None,sag=.35,seed=1):
    n=n or int(abs(x1-x0)*2.2); B.cyl(((x0+x1)/2,y,z),.008,abs(x1-x0),M('#16171C',.6),seg=5,rot=(0,R(90),0))
    for k in range(n):
        u=k/(n-1); x=L(x0,x1,u); zz=z-sag*4*u*(1-u); B.ico((x,y,zz-.05),.045,M(cols[k%len(cols)],.2,emit=6),sub=1)
def shopfront(cx,name,col,ware,seed=0,deep=2.0):
    r=random.Random(seed); y=SHOP_Y0
    B.box((cx,y+deep,SHOP_H/2),(2.9,.1,SHOP_H/2),M(shade(col,.9),.85,kind='wall'),0)
    for sx in (-1,1): B.box((cx+sx*2.95,y+deep/2,SHOP_H/2),(.1,deep/2,SHOP_H/2),M('#CFC6B4',.85,kind='wall'),0)
    B.box((cx,y+deep/2,-.04),(2.9,deep/2,.04),M('#B8AE9C',.7,kind='tile',sc=1.5),0); B.box((cx,y+deep/2,SHOP_H+.04),(2.9,deep/2,.04),M('#E8E2D6',.9),0)
    B.box((cx,y-.05,SHOP_H+.45),(2.95,.08,.45),M(col,.5),.02); stext(name,(cx,y-.16,SHOP_H+.47),.36,'#FFFFFF' if col not in ('#E8C547','#F4F1EA') else '#16171C')
    B.box((cx,y+.02,SHOP_H+.06),(2.95,.12,.06),M('#5A5E66',.4,metal=.6),.01)
    B.box((cx,y+deep-.3,SHOP_H-.15),(1.0,.03,.03),M('#F4FAFF',.1,emit=7),.01); point((cx,y+deep/2,SHOP_H-.4),160,(.92,.96,1),r=.3)
    for k in range(7):
        x=cx-2.4+k*.8; c=r.choice(ware)
        B.box((x,y+deep-.35,1.0+(k%2)*.9),(.3,.2,.3),M(c,.6),.04)
    B.box((cx,y+.9,.5),(2.2,.35,.5),M('#6E4A2E',.5,kind='wood'),.02)
def bazaar(night=False):
    road=M('#7A766E',.85,kind='asphalt',sc=.6); B.box((0,-3,-.06),(40,6,.06),road,0)
    B.box((0,1.5,.08),(40,.5,.08),M('#B8AE9C',.85,kind='concrete',sc=.8),.01)
    # ---------------- MASTER TAILORS interior
    X0=-SHOP_W; X1=SHOP_W; wall=M('#D8E6DC',.9,kind='wall')
    B.box((0,(SHOP_Y0+SHOP_Y1)/2,-.04),(SHOP_W,(SHOP_Y1-SHOP_Y0)/2,.04),M('#CBBFA8',.6,kind='tile',sc=1.6,h2='#BBAE96'),0)
    B.box((0,SHOP_Y1,SHOP_H/2),(SHOP_W,.1,SHOP_H/2),wall,0); B.box((0,(SHOP_Y0+SHOP_Y1)/2,SHOP_H+.04),(SHOP_W,(SHOP_Y1-SHOP_Y0)/2,.04),M('#F2EEE6',.9),0)
    for sx in (-1,1): B.box((sx*(SHOP_W+.05),(SHOP_Y0+SHOP_Y1)/2,SHOP_H/2),(.1,(SHOP_Y1-SHOP_Y0)/2,SHOP_H/2),wall,0)
    B.box((0,SHOP_Y0-.05,SHOP_H+.55),(SHOP_W+.3,.1,.55),M('#1E3A6A',.45),.02); stext('MASTER TAILORS',(0,SHOP_Y0-.17,SHOP_H+.62),.44,'#F4D35E')
    stext('FIT GUARANTEE  •  EID ORDERS',(0,SHOP_Y0-.17,SHOP_H+.2),.15,'#FFFFFF')
    # counter + cutting table
    wd=M('#7A5232',.5,kind='wood'); B.box((0,COUNTER_Y,.5),(1.7,.3,.5),wd,.02); B.box((0,COUNTER_Y,1.02),(1.75,.34,.03),M('#5E3A22',.4,kind='wood'),.01)
    B.box((.9,COUNTER_Y-.05,1.06),(.35,.25,.02),M('#1E3FA0',.8,kind='fabric'),.01); B.box((-.9,COUNTER_Y,1.07),(.3,.2,.03),M('#E8C547',.8,kind='fabric'),.01)
    B.box((.2,4.2,.85),(1.1,.6,.04),M('#C9A06A',.5,kind='wood'),.01)
    for sx in (-1,1):
        for sy in (-1,1): B.box((.2+sx*1.0,4.2+sy*.5,.42),(.04,.04,.42),wd,0)
    B.box((.0,4.2,.9),(.6,.4,.01),M('#F4F1EA',.8,kind='fabric'),0); B.box((.7,4.3,.92),(.25,.02,.01),M('#C9CED8',.3,metal=.8),0)
    # sewing machine on its table
    mx,my=MACHINE; B.box((mx,my,.75),(.55,.35,.03),wd,.01)
    for sx in (-1,1): B.box((mx+sx*.5,my,.37),(.03,.3,.37),M('#2A2C34',.4,metal=.6),0)
    B.box((mx-.1,my,.95),(.28,.12,.18),M('#16171C',.25,spec=.8),.04); B.box((mx+.18,my,1.13),(.12,.12,.06),M('#16171C',.25),.03)
    B.box((mx-.3,my,.85),(.06,.1,.12),M('#16171C',.25),.02); B.cyl((mx+.32,my,1.02),.06,.04,M('#C9CED8',.3,metal=.8),seg=12,rot=(0,R(90),0))
    stext('SINGER',(mx-.1,my-.125,1.02),.05,'#E8C547')
    # back shelves of cloth rolls
    for z in (.6,1.3,2.0,2.7):
        B.box((-1.0,SHOP_Y1-.3,z),(1.4,.25,.02),wd,0)
        for k in range(6): B.cyl((-2.2+k*.48,SHOP_Y1-.3,z+.13),.11,.45,M(['#C8372D','#2E6B4F','#E8C547','#5A7FB0','#F4F1EA','#7A4A8A','#E28A3A'][(k+int(z*3))%7],.85,kind='fabric'),seg=10,rot=(R(90),0,0))
    # hanging finished suits on the left wall rail
    B.cyl((-SHOP_W+.25,3.9,2.4),.02,2.6,M('#C9CED8',.3,metal=.8),seg=6,rot=(R(90),0,0))
    for k in range(7):
        y=2.8+k*.36; c=['#F4F1EA','#2E6B4F','#C8372D','#E8C547','#5A7FB0','#9A3A5A','#D8CFB4'][k]
        B.box((-SHOP_W+.25,y,1.85),(.05,.16,.55),M(c,.85,kind='fabric'),.02); B.box((-SHOP_W+.25,y,2.38),(.02,.15,.02),M('#5E3A22',.4),0)
    # curtain to the back room: hangs to 0.38 m so feet show underneath
    cx,cy=CURT; B.cyl((cx,cy,3.0),.02,1.5,M('#C9A24A',.3,metal=.8),seg=6,rot=(0,R(90),0))
    for k in range(6): B.box((cx-.62+k*.25,cy+(k%2)*.04,1.69),(.13,.03,1.31),M('#8A2E3A' if k%2 else '#9A3A4A',.9,kind='fabric'),.02)
    B.box((cx,cy+.4,1.5),(.75,.02,1.5),M('#2A2028',.9),0)
    # tube light + clock
    B.box((0,SHOP_Y1-.08,3.0),(.6,.04,.04),M('#F4FAFF',.1,emit=8),.01); point((0,4.0,3.0),260,(.93,.97,1),r=.4)
    B.cyl((1.6,SHOP_Y1-.07,2.6),.2,.03,M('#F4F1EA',.4),seg=20,rot=(R(90),0,0))
    # ---------------- neighbours
    for i,(cx,n,c,w) in enumerate(((-6.2,'JUTA HOUSE','#C8372D',['#3A2A1E','#C9A24A','#16171C']),(6.2,'CHOORI CORNER','#D9367A',['#E8C547','#D9367A','#5AD0FF']),
                                   (-12.4,'AL-MADINA CLOTH','#2E6B4F',['#F4F1EA','#E8C547','#5A7FB0']),(12.4,'GENERAL STORE','#E8C547',['#C8372D','#2E8A6A','#F4F1EA']))): shopfront(cx,n,c,w,seed=i)
    for cx in (-12.4,-6.2,0,6.2,12.4,18.6,-18.6):
        c=['#E8D6C0','#D4E0C8','#E8C8B8','#C9DCE4','#D8C8A8','#C8C0D8','#E0D0B0'][int(cx/6.2)%7]
        B.box((cx,SHOP_Y0+2.2,SHOP_H+2.3),(3.05,2.3,1.4),M(c,.85,kind='wall'),0); B.box((cx,SHOP_Y0-.05,SHOP_H+2.6),(1.4,.05,.55),M('#2A3A5A' if not night else '#FFD98A',.2,emit=0 if not night else 1.4),0)
        B.box((cx,SHOP_Y0-.4,SHOP_H+1.15),(1.8,.4,.05),M('#9A9EA6',.5),.01)
        for k in range(5): B.box((cx-1.6+k*.8,SHOP_Y0-.78,SHOP_H+1.45),(.025,.025,.3),M('#5A5E66',.4,metal=.6),0)
        B.box((cx,SHOP_Y0-.78,SHOP_H+1.75),(1.8,.025,.025),M('#5A5E66',.4,metal=.6),0)
    for x in (-15,-3.1,3.1,15): B.box((x,SHOP_Y0-.05,(SHOP_H+3.7)/2),(.12,.12,(SHOP_H+3.7)/2),M('#CFC6B4',.85,kind='wall'),0)
    # opposite side wall + parked bikes + poles
    B.box((0,-7.5,2.4),(40,.3,2.4),M('#D8C8A8',.85,kind='wall'),0)
    for x in (-9,5,14): motorbike((x,-5.6,0),random.Random(int(x)).choice([10,-15,170]),random.Random(int(x)+1).choice(['#C8372D','#2A2C34','#2E5A9A']))
    for x in (-16,-4.5,9.5):
        B.cyl((x,-6.6,3.2),.09,6.4,M('#5A5E66',.4,metal=.6),seg=8)
        if night: B.box((x,-6.2,6.2),(.2,.12,.05),M('#FFE6B0',.2,emit=6),.01); point((x,-5.8,5.8),500,(1,.82,.55),r=.3)
    if night:
        for y,z,s in ((SHOP_Y0-.9,SHOP_H+1.0,3),(-2.0,6.0,5),(-5.0,5.6,7)): strlights(-20,20,y,z,seed=s)
        B.ico((-6,40,26),2.2,M('#FFF6D8',.2,emit=4),sub=2)
    for i in range(3): B.cyl((0,-6.4+i*.04,6.2-i*.15),.012,40,M('#16171C',.6),seg=6,rot=(0,R(90),0))
    for x in (-19,19): tree(x,-8.6,1.1)
    B.done('bazaar')
def shutter(z_bottom):
    """rolling shutter across the MASTER TAILORS opening; z_bottom = height of its lower edge"""
    e=empty((0,SHOP_Y0-.08,0)); h=SHOP_H-z_bottom
    obox((0,0,z_bottom+h/2),(SHOP_W+.05,.03,h/2),M('#8A9098',.45,metal=.6),.0,e)
    for k in range(int(h/.12)): obox((0,-.035,z_bottom+.06+k*.12),(SHOP_W+.05,.01,.008),M('#6E747C',.5,metal=.6),0,e)
    obox((0,-.04,z_bottom+.03),(SHOP_W+.05,.03,.04),M('#5A5E66',.4,metal=.6),.01,e); return e
def courtyard():
    X=60; B.box((X,0,-.05),(5,5,.05),M('#A8583E',.8,kind='tile',sc=2.2,h2='#8E4630'),0)
    for (x,y,w,d) in ((X,4.9,5,.15),(X-5,0,.15,5),(X+5,0,.15,5)): B.box((x,y,1.6),(w,d,1.6),M('#E0D4BC',.85,kind='wall'),0)
    B.box((X-3,4.8,1.15),(.7,.06,1.15),M('#5E3A22',.5,kind='wood'),.02)
    wd=M('#8A5E3A',.5,kind='wood'); B.box((X+2.2,3.2,.45),(1.0,.5,.05),wd,.02)
    for k in range(9): B.box((X+1.3+k*.22,3.2,.48),(.02,.48,.01),M('#E8D8B0',.8,kind='fabric'),0)
    for sx in (-1,1):
        for sy in (-1,1): B.cyl((X+2.2+sx*.95,3.2+sy*.45,.22),.05,.45,wd,seg=8)
    B.cyl((X-4.6,2.0,.7),.03,.5,M('#C9CED8',.3,metal=.8),seg=8); B.box((X-4.6,2.0,.2),(.3,.3,.2),M('#B8AE9C',.8,kind='concrete'),.02)
    for k,(x,y) in enumerate(((X-4.3,4.3),(X+4.3,4.3),(X-4.3,-2.0))):
        B.cyl((x,y,.25),.25,.5,M('#B05A3A',.7),seg=12,r2=.2); B.ico((x,y,.85),.42,M('#3F8A3A',.85,kind='leaves'),sub=1)
    B.box((X,4.78,2.7),(.6,.04,.04),M('#F4FAFF',.1,emit=8),.01); point((X,3.8,2.6),220,(.93,.97,1),r=.4)
    B.box((X+1.0,4.75,2.0),(.5,.02,.4),M('#2E6B4F',.6),.01); stext('786',(X+1.0,4.72,2.0),.18,'#E8C547')
    B.done('courtyard')
EID_X=150; EID_Y=0.0
def eidgah():
    X=EID_X; B.box((X,8,-.05),(30,22,.05),M('#C9B08A',.9,kind='concrete',sc=.4),0)
    for r_ in range(6):
        y=EID_Y-r_*1.25
        for k in range(14): B.box((X-8.4+k*1.3,y,.012),(.6,.5,.012),M('#2E6B4F' if (k+r_)%2 else '#E8E2D0',.9,kind='fabric'),0)
    mw=M('#F4F1EA',.8,kind='wall'); gr=M('#2E8A5A',.5)
    B.box((X,14,4.0),(9,1.2,4.0),mw,0); B.box((X,13.6,8.2),(9.2,1.4,.2),M('#E8E2D6',.8),0)
    for k in (-1,0,1):
        B.box((X+k*3.4,12.75,2.1),(1.05,.06,2.1),M('#3A2E28',.6),0); B.cyl((X+k*3.4,12.74,4.2),1.05,.12,M('#3A2E28',.6),seg=20,rot=(R(90),0,0))
    B.ico((X,14,9.6),2.6,mw,sub=2,sc=(1,1,1.1)); B.cyl((X,14,12.6),.06,1.2,M('#C9A24A',.3,metal=.8),seg=8); B.ico((X,14,13.3),.18,M('#C9A24A',.3,metal=.8),sub=1)
    for sx in (-1,1):
        mx=X+sx*10.2; B.cyl((mx,14,7.5),.75,15,mw,seg=12); B.cyl((mx,14,15.2),.95,.3,gr,seg=12); B.cyl((mx,14,16.4),.55,2.2,mw,seg=12); B.cyl((mx,14,18.0),.6,1.2,gr,seg=12,r2=.02)
    B.box((X,12.6,7.0),(6,.08,.35),gr,.01); stext('EID MUBARAK',(X,12.52,7.0),.5,'#F4F1EA')
    for k in range(12): B.box((X-14+k*2.5,22,1.2),(1.2,.2,1.2),M('#E0D4BC',.85,kind='wall'),0)
    for x,y in ((X-14,10),(X+14,10),(X-14,-2),(X+14,-2),(X-14,-12),(X+14,-12),(X-8,-14),(X+8,-14)): tree(x,y,1.25)
    for k in range(9): B.cyl((X-12+k*3,13.0,7.6),.01,3,M('#16171C',.6),seg=5,rot=(0,R(90),0)); B.box((X-12+k*3,13.0,7.45),(.12,.01,.18),M(['#2E8A5A','#F4F1EA'][k%2],.6),0)
    B.done('eidgah')
