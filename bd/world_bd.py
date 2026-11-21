# Sets for "Everyone Wants a Lahori Baddie": city park, rooftop at golden hour, glass-front boulevard, cafe terrace, house gate, phone UI screens.
def stext(body,loc,size,col,n=(0,-1,0),e=0.0,parent=None,ex=.02):
    return text(body,loc,n,size,M(col,.4,emit=e) if e else M(col,.5),ex=ex,parent=parent)
def palm(x,y,h=6.0,s=1.0):
    tr=M('#8A6A4A',.85,kind='wood',sc=.5); lf=M('#3F8A4A',.8,kind='leaves')
    for k in range(6): B.cyl((x+.05*math.sin(k),y,h*(k+.5)/6),.2*s-.012*k,h/6+.02,tr,seg=8)
    for k in range(9):
        a=k*2*pi/9; B.box((x+math.cos(a)*1.1*s,y+math.sin(a)*1.1*s,h+.15),(1.2*s,.22*s,.03),lf,.01,rot=(0,R(22),a))
        B.box((x+math.cos(a)*2.1*s,y+math.sin(a)*2.1*s,h-.45),(.7*s,.16*s,.03),lf,.01,rot=(0,R(48),a))
    B.ico((x,y,h),.3*s,M('#6A4A2E',.8),sub=1)
def bush(x,y,s=1.0,col='#4F8A3A'):
    for dx,dy,r_ in ((0,0,.6),(.5,.15,.45),(-.45,-.1,.5)): B.ico((x+dx*s,y+dy*s,.35*s),r_*s,M(col,.85,kind='leaves'),sc=(1,1,.8),sub=1)
def flowerbed(x0,x1,y,seed=1):
    r=random.Random(seed); B.box(((x0+x1)/2,y,.08),((x1-x0)/2,.35,.08),M('#5A4030',.9),.02)
    for k in range(int((x1-x0)*3)): B.ico((r.uniform(x0,x1),y+r.uniform(-.25,.25),.24),.09,M(r.choice(['#E8554D','#F2C14E','#F28BB0','#F4F1EA','#B06AD0']),.7),sub=1)
def park_bench(x,y,rz=0):
    wd=M('#8A5A3A',.7,kind='wood'); mt=M('#2A3A30',.4,metal=.5); e=empty((x,y,0),rot=(0,0,R(rz)))
    for k in range(4): obox((0,-.3+k*.16,.55),(1.1,.07,.025),wd,.01,e)
    for k in range(3): obox((0,.33,.75+k*.17),(1.1,.02,.07),wd,.01,e)
    for dx in (-1.0,1.0): obox((dx,0,.27),(.04,.3,.27),mt,.01,e); obox((dx,.33,.75),(.04,.03,.5),mt,.01,e); obox((dx,-.05,.78),(.04,.3,.025),mt,.01,e)
    return e
def park():
    B.box((0,0,-.05),(120,120,.05),M('#6FA04C',.9,kind='grass',sc=.5),0)
    B.box((0,0,.01),(60,1.6,.012),M('#D8C9A8',.85,kind='concrete',sc=.6),0)
    for s in (-1,1): B.box((0,s*1.68,.04),(60,.08,.04),M('#B8A888',.8,kind='concrete'),.01)
    # fountain
    st=M('#D9D2C4',.6,kind='concrete'); wt=M('#7FC8F0',.15,spec=.9,alpha=.8)
    B.cyl((0,9,.3),3.0,.6,st,seg=28); B.cyl((0,9,.55),2.75,.14,wt,seg=28); B.cyl((0,9,1.1),.35,1.6,st,seg=12); B.cyl((0,9,1.9),1.1,.12,st,seg=20); B.cyl((0,9,2.6),.12,1.4,wt,seg=8)
    r=random.Random(3)
    for k in range(26):
        x=r.uniform(-45,45); y=r.choice([r.uniform(6,30),r.uniform(-30,-5)])
        if abs(x)<4.5 and 5<y<13: continue
        tree(x,y,r.uniform(1.0,1.7),r.choice(['#4F8A3A','#5E9A44','#467E36','#6AA84F']),'#5A3E28')
    for x in range(-40,41,8): flowerbed(x-2.2,x+2.2,3.6,x); bush(x+4,4.2,1.0)
    for x in range(-36,37,12): B.cyl((x,-2.3,2.0),.07,4.0,M('#2A3A30',.4,metal=.5),seg=8); B.ico((x,-2.3,4.1),.22,M('#FFF2C8',.3,emit=.6),sub=2)
    for k in range(14):
        x=-90+k*14+r.uniform(-3,3); h=r.uniform(12,26); B.box((x,55+r.uniform(0,12),h/2),(4.5,4.5,h/2),M(r.choice(['#D9C8B0','#C9B8A0','#B8C0C8','#E0D4C0']),.8,kind='concrete'),0)
        for z in range(3,int(h)-1,3): B.box((x,50.4,z),(3.8,.05,.5),M('#3A4658',.2,spec=.8),0)
    for x in (-30,-18,-6,6,18,30): B.box((x,-9,.5),(5,.25,.5),M('#3F7A3A',.9,kind='leaves'),.1)
def rooftop():
    fl=M('#C9A88A',.85,kind='tile',h2='#B89878',sc=1.2); wl=M('#E8D8BE',.85,kind='wall'); wl2=M('#C8773A',.85,kind='wall')
    B.box((0,0,-.1),(7,6,.1),fl,0)
    for (x,y,sx,sy) in ((0,6,7,.15),(0,-6,7,.15),(-7,0,.15,6),(7,0,.15,6)): B.box((x,y,.5),(sx,sy,.5),wl,.02); B.box((x,y,1.03),(sx+.05,sy+.05,.05),M('#F4EBDA',.7),.01)
    B.box((4.5,4.2,1.5),(2.0,1.5,1.5),wl2,.02); B.box((4.5,2.68,1.1),(.5,.04,1.05),M('#3A6A8A',.5,kind='wood'),.01); B.box((4.5,4.2,3.05),(2.2,1.7,.06),M('#F4EBDA',.7),.02)
    B.cyl((5.2,4.6,3.9),.75,1.5,M('#2A2C34',.5),seg=18); B.cyl((5.2,4.6,4.7),.5,.15,M('#2A2C34',.5),seg=18)
    for dx in (-.5,.5):
        for dy in (-.5,.5): B.box((5.2+dx,4.6+dy,3.2),(.04,.04,.15),M('#5A5E66',.5,metal=.5),0)
    # charpai
    wd=M('#7A5236',.7,kind='wood'); wv=M('#E8D2A8',.9,kind='fabric',h2='#C8372D',sc=3)
    B.box((-1.2,.6,.52),(1.0,.5,.03),wv,.01)
    for dx in (-.98,.98):
        for dy in (-.48,.48): B.cyl((-1.2+dx,.6+dy,.27),.045,.6,wd,seg=8)
    B.box((-1.2,.6-.5,.52),(1.02,.03,.04),wd,.01); B.box((-1.2,.6+.5,.52),(1.02,.03,.04),wd,.01)
    # clothesline + clothes
    B.cyl((-6.2,3.5,1.4),.04,2.8,M('#5A5E66',.5,metal=.5),seg=6); B.cyl((1.5,5.4,1.4),.04,2.8,M('#5A5E66',.5,metal=.5),seg=6)
    r=random.Random(4)
    for k in range(7):
        f=(k+.5)/7; B.box((-6.2+7.7*f,3.5+1.9*f,2.2),(.34,.02,.42),M(r.choice(['#E8554D','#F4F1EA','#4D8FE8','#F2C14E','#6FC38A','#CF3F78']),.9,kind='fabric'),.0,rot=(0,0,math.atan2(1.9,7.7)))
    for (x,y) in ((-6,-5),(-4.8,-5.2),(6,-4.8),(2.4,-5.3),(-6.2,1.5)):
        B.cyl((x,y,.25),.28,.5,M('#B5603F',.8),seg=12,r2=.22); B.ico((x,y,.8),.42,M(r.choice(['#4F8A3A','#5E9A44','#3F8A4A']),.85,kind='leaves'),sub=1)
    B.box((1.8,-1.2,.3),(.3,.3,.3),M('#3A6A8A',.6),.03); B.cyl((1.8,-1.2,.68),.12,.14,M('#F4F1EA',.5),seg=10)
    # neighbouring rooftops + skyline
    for k in range(60):
        x=r.uniform(-90,90); y=r.uniform(-70,90)
        if abs(x)<11 and abs(y)<10: continue
        w=r.uniform(3,6); h=r.uniform(-6,3) if abs(x)<25 and abs(y)<25 else r.uniform(-4,10)
        c=r.choice(['#E8D8BE','#D9B48A','#C8773A','#E6C9A0','#B8C8D0','#F2D9B8','#C9A27A'])
        B.box((x,y,h/2-6),(w,w,h/2+6),M(c,.85,kind='wall'),0); B.box((x,y,h+.4),(w,w,.4),M(shade(c,.9),.85),0) if r.random()<.5 else None
        if r.random()<.4: B.cyl((x+r.uniform(-1,1),y,h+1.3),.6,1.2,M('#2A2C34',.5),seg=10)
    B.cyl((-30,60,10),1.2,26,M('#E8E0D0',.7),seg=10); B.ico((-30,60,23.5),1.6,M('#3F8A6A',.5),sc=(1,1,1.3),sub=2)
    B.cyl((-18,64,7),7,5,M('#E8E0D0',.7),seg=8); B.ico((-18,64,10),6,M('#F4EEE0',.6),sc=(1,1,.8),sub=2)
def shopfront(cx,w,name,col,Y=7.0,h=7.5,sign='#F4F1EA',door=True):
    fr=M(col,.5); gl=M('#BFD6E8',.05,spec=1.0,alpha=.3); inn=M('#FFE8C4',.5,emit=.3)
    B.box((cx,Y+3,h/2),(w/2,3,h/2),M(shade(col,1.1),.7,kind='concrete'),0); B.box((cx,Y-.03,1.9),(w/2-.3,.03,1.8),inn,0); B.box((cx,Y-.08,1.9),(w/2-.3,.02,1.8),gl,0)
    for k in range(int(w/1.6)+1): B.box((cx-w/2+.3+k*(w-.6)/max(1,int(w/1.6)),Y-.1,1.9),(.05,.05,1.8),fr,0)
    B.box((cx,Y-.25,4.3),(w/2,.3,.55),fr,.03); stext(name,(cx,Y-.58,4.25),.5,sign,e=1.5)
    B.box((cx,Y-.12,3.7),(w/2-.3,.06,.06),fr,0)
    for f in range(1):
        for k in range(int(w/2.2)): B.box((cx-w/2+1.1+k*2.2,Y-.02,6.0),(.7,.04,.6),M('#1E2A3C',.1,spec=.9),0)
    if door: B.box((cx+w/2-1.3,Y-.12,1.2),(.55,.04,1.2),M('#2A2C34',.3,metal=.5),.01); B.box((cx+w/2-1.3,Y-.14,1.2),(.48,.03,1.12),gl,0)
def strip():
    B.box((0,0,-.05),(120,5,.05),M('#3A3C42',.85,kind='asphalt'),0)
    for s in (-1,1):
        B.box((0,s*6.2,.08),(120,1.3,.08),M('#C8BFB0',.8,kind='tile',h2='#B8AF9F',sc=2.0),0); B.box((0,s*4.95,.09),(120,.07,.09),M('#9A958C',.7),.01)
    for k in range(-30,31): B.box((k*4.0,0,.003),(1.0,.07,.003),M('#EDEBE4',.6),0)
    names=[('SHADES & CO','#1F2A44'),('BEAN THEORY','#3A2A20'),('LUXE MALL','#5A1F3A'),('ROYAL WATCHES','#2A3A30'),('GLOW STUDIO','#6A3A7A'),('URBAN FITS','#22242B'),('SWEET TOOTH','#A84A3A'),('TECH HUB','#1F3F5A')]
    x=-52; i=0
    while x<52:
        w=[9,8,11,8,9,10][i%6]; nm,c=names[i%8]; shopfront(x+w/2,w,nm,c,h=7.5+(i%3)*2.0); x+=w; i+=1
    x=-52; i=3
    while x<52:
        w=[10,9,8,11][i%4]; nm,c=names[(i+4)%8]; B.box((x+w/2,-10.5,5),(w/2,3.5,5),M(shade(c,1.4),.7,kind='concrete'),0); B.box((x+w/2,-6.98,2),(w/2-.4,.03,1.8),M('#FFE8C4',.5,emit=.3),0); B.box((x+w/2,-6.8,4.4),(w/2,.25,.5),M(c,.5),.03); x+=w; i+=1
    for x in range(-48,49,8): palm(x+2,5.3,5.2,.8); palm(x-2,-5.3,5.2,.8)
    for x in range(-44,45,11):
        B.cyl((x,5.25,.3),.5,.6,M('#D9D2C4',.6,kind='concrete'),seg=10); bush(x,5.25,.7)
    r=random.Random(8)
    for k in range(12):
        s=r.choice([-1,1]); B.box((r.uniform(-50,50),s*20+r.uniform(-4,4),r.uniform(10,18)),(r.uniform(4,7),4,r.uniform(10,18)),M(r.choice(['#B8C0C8','#C9B8A0','#A8B0BA']),.7,kind='concrete'),0)
def cafe_table(x,y):
    mt=M('#22252B',.4,metal=.6); tp=M('#EDE6D8',.3,spec=.6)
    B.cyl((x,y,.98),.52,.05,tp,seg=24); B.cyl((x,y,.5),.05,.95,mt,seg=8); B.cyl((x,y,.03),.3,.05,mt,seg=16)
    B.cyl((x,y,1.06),.04,.12,M('#F4F1EA',.2,spec=.8,alpha=.6),seg=10); B.ico((x,y,1.18),.05,M('#E8554D',.6),sub=1)
def cafe_chair(x,y,rz):
    e=empty((x,y,0),rot=(0,0,R(rz))); rt=M('#C9A27A',.7,kind='wood'); mt=M('#22252B',.4,metal=.6)
    obox((0,0,.55),(.3,.3,.03),rt,.02,e); obox((0,.3,.95),(.3,.025,.36),rt,.03,e)
    for dx in (-.26,.26):
        for dy in (-.26,.26): obox((dx,dy,.27),(.02,.02,.27),mt,0,e)
    return e
def cafe():
    # terrace deck y in [-4,4], x in [-9,9]; glass cafe at y=4..10; street at y<-6 with valet parking
    B.box((0,-30,-.2),(120,24,.05),M('#3A3C42',.85,kind='asphalt'),0); B.box((0,10,-.2),(120,20,.05),M('#B8B2A8',.85,kind='concrete',sc=.5),0)
    B.box((0,0,-.08),(9.5,4.3,.1),M('#8A6A4A',.6,kind='wood',sc=.4),.02)
    for k in range(38): B.box((-9.2+k*.5,0,.022),(.008,4.3,.003),M('#5A4030',.8),0)
    fr=M('#1E2228',.4,metal=.5); gl=M('#BFD6E8',.05,spec=1.0,alpha=.25)
    B.box((0,7.5,4.0),(9.5,3.2,4.0),M('#2A2E36',.6,kind='concrete'),0); B.box((0,4.28,2.0),(9.0,.03,1.9),M('#FFDDAA',.5,emit=.35),0); B.box((0,4.22,2.0),(9.0,.02,1.9),gl,0)
    for k in range(10): B.box((-9+k*2.0,4.2,2.0),(.05,.06,1.9),fr,0)
    B.box((0,4.0,4.6),(9.5,.4,.6),fr,.03); stext('CAFÉ LUMIÈRE',(0,3.56,4.55),.62,'#FFE7B8',e=2.5)
    B.box((0,3.2,3.9),(9.5,.9,.04),M('#7A1F2E',.85,kind='fabric'),.01,rot=(R(-10),0,0))
    r=random.Random(6)
    for k in range(6): B.box((-7.5+k*3,6.2,1.0),(.9,.5,.04),M('#EDE6D8',.4),.01); B.cyl((-7.5+k*3,6.2,.5),.05,1.0,fr,seg=6)
    # planters + rail
    for x in range(-9,10,3):
        B.box((x,-4.1,.5),(.5,.25,.3),M('#3A3A40',.6,kind='concrete'),.03); bush(x,-4.1,.6); B.ico((x,-4.1,.95),.3,M('#3F8A4A',.85,kind='leaves'),sub=1)
    for s in (-1,1): B.box((s*9.4,0,.6),(.06,4.2,.4),gl,0); B.box((s*9.4,0,1.02),(.07,4.2,.03),fr,0)
    for x in (-10.8,10.8): palm(x,-2,6.5,1.0); palm(x,3.4,6.0,.9)
    # string lights
    for row,(y0,z0) in enumerate(((-3.6,3.6),(-1.2,3.9),(1.2,3.9),(3.2,3.7))):
        for k in range(19):
            x=-9+k; z=z0-.35*math.sin(pi*(k%6)/6); B.ico((x,y0,z),.07,M('#FFE2A0',.3,emit=6.0),sub=1)
        B.box((0,y0,z0-.1),(9.3,.008,.008),M('#1E2228',.5),0)
    for x in (-9.3,9.3):
        for y in (-3.8,3.4): B.cyl((x,y,2.0),.05,3.9,fr,seg=8)
    tabs=[(-6,-1.5),(-6,1.8),(-2.4,2.2),(3.6,2.0),(6.6,-1.6),(6.8,1.9),(3.2,-2.2)]
    for (x,y) in tabs: cafe_table(x,y); cafe_chair(x-.95,y,90); cafe_chair(x+.95,y,-90)
    cafe_table(0,-.6)
    # street side: kerb, lamps, far buildings
    B.box((0,-5.2,-.1),(60,.9,.06),M('#C8BFB0',.8,kind='tile',h2='#B8AF9F',sc=2.0),0)
    for x in range(-40,41,10): B.cyl((x,-5.6,2.4),.07,4.8,fr,seg=8); B.ico((x,-5.6,4.9),.2,M('#FFE7B8',.3,emit=4.0),sub=2)
    for k in range(12):
        x=-66+k*12; h=r.uniform(8,16); c=r.choice(['#3A4050','#4A4450','#2E3A48','#504A44'])
        B.box((x,-22,h/2),(5.5,4,h/2),M(c,.7,kind='concrete'),0)
        for z in range(2,int(h)-1,3):
            for j in range(4):
                if r.random()<.6: B.box((x-3.6+j*2.4,-17.95,z),(.7,.04,.8),M('#FFD9A0',.4,emit=1.8),0)
    for x in range(-36,37,9): palm(x+4,-14.5,6.0,.9)
    return tabs
def cafe_lights():
    for (x,y) in ((-6,0),(0,0),(6,0),(-3,2.5),(3,-2.5)): point((x,y,3.6),170,(1,.85,.62),r=.8,shadow=False)
    point((0,3.2,2.2),260,(1,.82,.6),r=1.5,shadow=False)
def gate_street():
    B.box((0,0,-.05),(60,3.2,.05),M('#4A4C52',.85,kind='asphalt'),0); B.box((0,4.2,.06),(60,1.0,.06),M('#C8BFB0',.8,kind='concrete'),0); B.box((0,-4.2,.06),(60,1.0,.06),M('#C8BFB0',.8,kind='concrete'),0)
    r=random.Random(12); x=-40; i=0
    while x<40:
        w=r.choice([9,10,12]); c=r.choice(['#F2E6D0','#E8D2B0','#D9E2E8','#F0D8C8','#E2E8D8']); cx=x+w/2
        B.box((cx,12,3.5),(w/2-.6,3.5,3.5),M(c,.85,kind='wall'),.02); B.box((cx,12,7.1),(w/2-.4,3.7,.12),M('#F4EBDA',.7),.02)
        for dx in (-w/4,w/4): B.box((cx+dx,8.46,4.8),(.7,.05,.8),M('#1E2A3C',.1,spec=.9),0); B.box((cx+dx,8.42,4.8),(.8,.04,.9),M('#F4EBDA',.7),.02)
        B.box((cx,5.2,1.0),(w/2,.12,1.0),M(shade(c,.9),.85,kind='wall'),.02); B.box((cx,5.2,2.05),(w/2+.05,.16,.06),M('#B5603F',.8),.01)
        gm=M(r.choice(['#2A2C34','#5A2A2A','#1F3F5A','#3A4A3A']),.4,metal=.6); B.box((cx,5.1,1.15),(1.5,.06,1.15),gm,.02)
        for j in range(9): B.box((cx-1.4+j*.35,5.02,1.15),(.03,.03,1.05),M('#D9B24A',.3,metal=.9),0)
        for dx in (-1.7,1.7): B.box((cx+dx,5.2,1.3),(.22,.22,1.3),M(shade(c,.8),.85,kind='wall'),.02); B.ico((cx+dx,5.2,2.75),.18,M('#FFF2C8',.3,emit=.8),sub=2)
        tree(cx+w/2-.8,7.2,1.1,r.choice(['#4F8A3A','#5E9A44']),'#5A3E28'); bush(cx-w/2+1.2,6.2,.9)
        B.box((cx,-9,3),(w/2-.6,3,3),M(r.choice(['#F2E6D0','#E8D2B0','#D9E2E8']),.85,kind='wall'),.02); B.box((cx,-5.3,1.0),(w/2,.12,1.0),M('#E0D4C0',.85,kind='wall'),.02)
        x+=w; i+=1
    for x in range(-30,37,12): B.cyl((x,3.9,3.5),.08,7,M('#7A7E86',.6,kind='concrete'),seg=8); B.box((x,3.9,6.6),(.8,.05,.05),M('#3A3D44',.5),0)

# ---------------------------------------------------------------- phone UI (flat, self-lit, far below the world)
UIZ=-200.0
def ui_mat(c,e=1.0): return M(c,.6,emit=e,spec=0)
def ui_panel(w=2.2,h=4.4,bg='#FFFFFF'):
    root=empty((0,0,UIZ)); obox((0,.08,0),(w/2+.12,.06,h/2+.12),ui_mat('#16171C',.05),.1,root); obox((0,0,0),(w/2,.01,h/2),ui_mat(bg),.0,root); return root
def ui_text(root,body,x,z,size,col='#16171C',al='CENTER'):
    o=text(body,(x,-.03,z),(0,-1,0),size,ui_mat(col),ex=.0,parent=root); o.data.align_x=al; return o
def ui_box(root,x,z,w,h,col,r=.04): return obox((x,-.02,z),(w/2,.005,h/2),ui_mat(col),r,root)
def ui_cam(z=0,d=7.4,lens=50): camset((0,-d,UIZ+z),(0,0,UIZ+z),lens,16)
