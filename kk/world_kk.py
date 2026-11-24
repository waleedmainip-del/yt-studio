# Wedding hall for "Khana Khul Gaya": seating tables, stage, buffet behind a curtain, VIP table.
BALLS=[]
HALL_X=(-12,12); HALL_Y=(-10,10); HH=5.2
BUF_Y=6.4          # buffet table line (curtain at y=5.2)
CURT_Y=5.2
PLATES=(-6.5,BUF_Y-.1); DAIG=(-1.5,BUF_Y); QORMA=(3.2,BUF_Y); KHEER=(8.0,BUF_Y); RAITA=(-4.2,BUF_Y)
VIP=(-8.5,-6.5); STAGE=(0,-8.6)
TABLES=[(-6,-1.5),(0,-1.5),(6,-1.5),(-3,-4.5),(3,-4.5),(-6,1.8),(6,1.8),(8.5,-5.0)]
def chair(x,y,rz,col='#C9A24A',seat='#7A1E2E'):
    e=empty((x,y,0),rot=(0,0,R(rz))); g=M(col,.3,metal=.6); s=M(seat,.85,kind='fabric')
    obox((0,0,.47),(.22,.22,.04),s,.02,e); obox((0,.2,.85),(.22,.03,.36),s,.02,e)
    for sx in (-1,1):
        for sy in (-1,1): obox((sx*.19,sy*.19,.22),(.02,.02,.22),g,0,e)
    obox((0,.22,1.24),(.24,.03,.04),g,.01,e); return e
def round_table(x,y,n=6,food=False,seed=0):
    B.cyl((x,y,.74),.95,.04,M('#F7F5EF',.8,kind='fabric'),seg=28); B.cyl((x,y,.38),1.0,.72,M('#F4F1EA',.85,kind='fabric'),seg=28,r2=.97)
    B.cyl((x,y,.8),.12,.1,M('#C9A24A',.3,metal=.7),seg=12); B.ico((x,y,1.0),.17,M('#E8559A',.85,kind='leaves'),sub=1)
    if food:
        for k in range(3): B.cyl((x+.5*math.cos(k*2.1),y+.5*math.sin(k*2.1),.77),.13,.02,M('#F4F1EA',.2),seg=16)
    return [(x+1.45*math.sin(R(a)),y-1.45*math.cos(R(a)),a) for a in range(0,360,360//n)]
def hall():
    fl=M('#7A1E2E',.9,kind='fabric',sc=2); B.box((0,0,-.04),(12,10,.04),fl,0)
    B.box((0,0,HH+.05),(12,10,.05),M('#F4EEDC',.8),0)
    wall=M('#F2E6C8',.85,kind='wall')
    B.box((0,10,HH/2),(12,.1,HH/2),wall,0); B.box((0,-10,HH/2),(12,.1,HH/2),wall,0)
    for x in (-12,12): B.box((x,0,HH/2),(.1,10,HH/2),wall,0)
    for x in range(-11,12,2):
        for y in (-9.9,9.9): B.box((x,y,HH/2),(.12,.08,HH/2),M('#C9A24A',.3,metal=.6),0)
    # chandeliers + fairy curtains
    for (x,y) in ((-6,-3),(0,-3),(6,-3),(-6,2.5),(0,2.5),(6,2.5)):
        B.cyl((x,y,HH-.4),.02,.8,M('#C9A24A',.3,metal=.8),seg=6); B.cyl((x,y,HH-1.0),.55,.12,M('#C9A24A',.3,metal=.8),seg=18,r2=.35)
        for k in range(10): B.ico((x+.5*math.cos(k*.63),y+.5*math.sin(k*.63),HH-1.2),.06,M('#FFF6D8',.1,emit=6),sub=1)
        point((x,y,HH-1.4),150,(1,.9,.72),r=.4)
    for k in range(40): B.cyl((-11.8+k*.6,-9.85,HH-1.3),.006,2.6,M('#FFE6A8',.1,emit=3),seg=4)
    # stage + couple sofa + flower backdrop
    B.box((STAGE[0],STAGE[1],.25),(4.2,1.3,.25),M('#C9A24A',.4,metal=.4),.02)
    B.box((STAGE[0],STAGE[1]-.35,.85),(1.4,.4,.35),M('#F4F1EA',.6,kind='fabric'),.08); B.box((STAGE[0],STAGE[1]-.7,1.35),(1.4,.12,.55),M('#C9A24A',.4,metal=.5),.08)
    for k in range(26):
        a=k/25; B.ico((STAGE[0]-4+8*a,STAGE[1]-1.1,1.0+3.0*math.sin(a*math.pi)),.32,M(['#D9367A','#F4F1EA','#E8559A','#C8372D'][k%4],.85,kind='leaves'),sub=1)
    B.box((STAGE[0],STAGE[1]-1.2,2.4),(4.2,.05,2.4),M('#F7E8F0',.8,kind='fabric'),0)
    point((STAGE[0],STAGE[1]+1.5,3.5),400,(1,.85,.75),r=.6)
    # buffet line (behind curtain)
    tb=M('#F7F5EF',.8,kind='fabric'); B.box((0,BUF_Y,.4),(10.5,.5,.4),tb,.02); B.box((0,BUF_Y-.48,.42),(10.5,.02,.38),M('#C9A24A',.4,kind='fabric'),0)
    for x,lab in ((PLATES[0],'PLATES'),(RAITA[0],'RAITA'),(DAIG[0],'BIRYANI'),(QORMA[0],'QORMA'),(5.6,'NAAN'),(KHEER[0],'KHEER')):
        B.box((x,BUF_Y-.52,.62),(.45,.02,.12),M('#16171C',.4),.01); stext(lab,(x,BUF_Y-.55,.62),.12,'#E8C547')
    # biryani daig
    B.cyl((DAIG[0],DAIG[1],1.12),.48,.6,M('#B8BCC4',.25,metal=.8),seg=24,r2=.42); B.cyl((DAIG[0],DAIG[1],1.43),.43,.03,M('#E8A040',.8),seg=24)
    for k in range(9): B.box((DAIG[0]+random.Random(k).uniform(-.3,.3),DAIG[1]+random.Random(k+9).uniform(-.3,.3),1.46),(.03,.03,.02),M(['#F4F1EA','#C8372D','#E8C547'][k%3],.7),.01)
    # qorma chafing dish
    B.box((QORMA[0],QORMA[1],.95),(.42,.28,.12),M('#C9CED8',.2,metal=.9),.03); B.box((QORMA[0],QORMA[1],1.06),(.38,.24,.02),M('#8A3A1A',.5),.01)
    # kheer, raita, naan
    B.box((KHEER[0],KHEER[1],.95),(.42,.28,.12),M('#C9CED8',.2,metal=.9),.03); B.box((KHEER[0],KHEER[1],1.06),(.38,.24,.02),M('#F4EAD0',.6),.01)
    B.cyl((RAITA[0],RAITA[1],.92),.25,.12,M('#F4F1EA',.3),seg=18); B.cyl((RAITA[0],RAITA[1],.98),.22,.01,M('#E8F2E0',.5),seg=18)
    B.cyl((5.6,BUF_Y,.88),.3,.06,M('#C9A06A',.5),seg=18)
    for k in range(4): B.box((5.6,BUF_Y,.95+k*.03),(.22,.15,.012),M('#E0B070',.7),.01)
    B.box((PLATES[0],PLATES[1],.82),(.3,.3,.02),M('#C9CED8',.2,metal=.8),.01)
    # VIP table
    B.box((VIP[0],VIP[1],.75),(1.3,.6,.04),M('#F7F5EF',.8,kind='fabric'),.02); B.box((VIP[0],VIP[1],.38),(1.32,.62,.36),M('#C9A24A',.5,kind='fabric'),.02)
    B.box((VIP[0],VIP[1]-.62,1.15),(.35,.03,.15),M('#16171C',.4),.01); stext('VIP',(VIP[0],VIP[1]-.66,1.15),.2,'#E8C547')
    for sx in (-1,1): B.ico((VIP[0]+sx*1.0,VIP[1],.95),.2,M('#E8559A',.85,kind='leaves'),sub=1)
    B.done('hall')
def curtain_obj(open_k=0.0):
    """buffet curtain (y=CURT_Y); open_k slides the two halves apart"""
    L_=empty((0,0,0)); R_=empty((0,0,0)); fab=M('#C8A050',.7,kind='fabric'); fab2=M('#B08A3A',.7,kind='fabric')
    for k in range(18):
        obox((-.32-k*.6,CURT_Y+(k%2)*.06,HH/2),(.3,.04,HH/2),fab if k%2 else fab2,.02,L_); obox((.32+k*.6,CURT_Y+(k%2)*.06,HH/2),(.3,.04,HH/2),fab if k%2 else fab2,.02,R_)
    B.cyl((0,CURT_Y,HH-.1),.04,24,M('#C9A24A',.3,metal=.8),seg=8,rot=(0,R(90),0))
    def set_(k): L_.location=(-11*k,0,0); R_.location=(11*k,0,0)
    set_(open_k); return set_
