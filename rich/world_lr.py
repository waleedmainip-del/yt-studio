
# ================================================================ KARACHI OLD BAZAAR + CLOTH SHOP
def sign(body,loc,n,w,h,fg='#FFE9A8',bg=None,emit=0.0,ex=.012,border=None):
    """readable sign: backing plate, text fitted to (w,h) and pushed in front of the surface along n (axis-aligned n)"""
    nv=Vector(n).normalized(); L_=Vector(loc); ya=abs(nv.y)>.5
    if border: B.box(tuple(L_-nv*.012),(w/2+.05 if ya else .012, .012 if ya else w/2+.05, h/2+.05),M(border,.3,metal=.6),.005)
    if bg: B.box(tuple(L_),(w/2 if ya else .015, .015 if ya else w/2, h/2),M(bg,.6),.005)
    t=text(body,tuple(L_+nv*(.03+ex)),n,1.0,M(fg,.35,emit=emit),ex=ex); bpy.context.view_layer.update()
    dw,dh=t.dimensions.x,t.dimensions.y
    s=min(w*.88/max(dw,1e-3),h*.78/max(dh,1e-3)); t.scale=(s,s,1); return t
CLOTH=['#C9302C','#2E6E9E','#F2C14E','#2E8B57','#8E2A6A','#E8742A','#F4F1EA','#1F8A8A','#D63384','#5A3A8A','#3E5A7A','#A8513A']
def cloth_stack(x,y,z,n,r,w=.26,d=.2,axis='y'):
    for k in range(n):
        c=r.choice(CLOTH); B.box((x,y,z+.035+k*.07),(w if axis=='y' else d, d if axis=='y' else w,.032),M(c,.85,kind='fabric'),.012)
def shirt_hang(x,y,z,col,face=(0,-1),s=1.0):
    """a shirt on a hanger, front facing `face` (axis aligned)"""
    m=M(col,.8,kind='fabric'); ya=abs(face[1])>.5
    def bx(dx,dz,hw,hz,mat=m,th=.025):
        if ya: B.box((x+dx*s,y,z+dz*s),(hw*s,th,hz*s),mat,.012)
        else: B.box((x,y+dx*s,z+dz*s),(th,hw*s,hz*s),mat,.012)
    bx(0,-.38,.2,.3); bx(-.27,-.2,.07,.13); bx(.27,-.2,.07,.13); bx(0,-.06,.07,.035,M(shade(col,.8),.8,kind='fabric'),.03)
    bx(0,.02,.012,.05,M('#8A8F99',.3,metal=.8),.008)
def mannequin(x,y,z,col,rz=0):
    e=empty((x,y,z),rot=(0,0,R(rz))); W_=M('#E8E0D4',.5)
    obox((0,0,1.12),(.2,.11,.3),M(col,.8,kind='fabric'),.03,e); obox((0,0,.52),(.17,.1,.3),M('#2B2C33',.8,kind='fabric'),.02,e)
    for s in (-1,1): obox((s*.27,0,1.12),(.06,.07,.28),M(col,.8,kind='fabric'),.02,e)
    ocyl((0,0,1.52),.05,.1,W_,e); obox((0,0,1.68),(.1,.1,.12),W_,.04,e); ocyl((0,0,.11),.03,.22,M('#8A8F99',.3,metal=.8),e); ocyl((0,0,.01),.2,.02,M('#8A8F99',.3,metal=.8),e)
    return e
def minibus(x,y,rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz)))
    obox((0,0,1.45),(3.2,1.15,.95),M('#C9302C',.35,metal=.2),.12,e); obox((0,0,2.0),(3.0,1.17,.3),M('#22303E',.08,spec=1.0),.04,e)
    obox((0,0,2.5),(3.25,1.2,.12),M('#F2C14E',.4),.05,e); obox((0,0,2.72),(2.6,.9,.1),M('#8A8F99',.4,metal=.6),.02,e)
    for k,c in enumerate(('#F2C14E','#2E8B57','#2E6E9E','#F4F1EA','#D63384','#F2C14E','#2E8B57','#2E6E9E')):
        for s in (-1,1): obox((-2.8+k*.8,s*1.16,1.0),(.32,.012,.3),M(c,.4),.01,e)
    for s in (-1,1): obox((3.21,s*.75,1.0),(.03,.22,.12),M('#FFF2C8',.3,emit=3),.01,e)
    for sx in (-2.0,2.0):
        for sy in (-1,1): ocyl((sx,sy*1.05,.5),.5,.3,M('#111216',.8),e,rot=(R(90),0,0),seg=18)
    return e
def facade(x0,x1,yf,nrm,r,name,col,stone='#D8C09A',floors=2,open_front=False,z0=0.0):
    """shop + colonial upper floors. facade plane at y=yf, facing nrm (+1 => faces +y, -1 => faces -y); building body lies behind it."""
    w=x1-x0; cx=(x0+x1)/2; back=yf-nrm*3.0; ST=M(stone,.85,kind='concrete',sc=.6); ST2=M(shade(stone,.86),.85,kind='concrete',sc=.6)
    H0=3.5
    if not open_front:
        B.box((cx,back,H0/2),(w/2,3.0,H0/2),M(shade(stone,.7),.9,kind='wall'),.02)
        # shutter / goods display
        if r.random()<.35:
            B.box((cx,yf+nrm*.03,1.5),(w/2-.3,.04,1.45),M('#7A8088',.45,metal=.6),.01)
            for k in range(12): B.box((cx,yf+nrm*.08,.2+k*.24),(w/2-.3,.02,.02),M('#5A5F66',.45,metal=.6),0)
        else:
            B.box((cx,yf+nrm*.02,1.5),(w/2-.3,.03,1.45),M('#2A2420',.9),0)
            for k in range(int((w-.8)/.55)):
                xx=x0+.6+k*.55; shirt_hang(xx,yf+nrm*.12,2.75,r.choice(CLOTH),(0,nrm))
            for k in range(int((w-.8)/.7)): cloth_stack(x0+.65+k*.7,yf+nrm*.3,.5,r.randint(3,7),r)
            B.box((cx,yf+nrm*.3,.25),(w/2-.3,.3,.25),M('#6B4A2A',.6,kind='wood'),.02)
    # signboard
    sign(name,(cx,yf+nrm*.25,H0+.45),(0,nrm,0),w-.5,.7,fg='#FFFFFF',bg=col,emit=.5,border='#C9A24A')
    # awning
    B.box((cx,yf+nrm*.75,H0-.12),(w/2-.1,.75,.04),M(r.choice(('#B03A2E','#1F5A7A','#2E6E4A','#C98A2A')),.85,kind='fabric'),.02,rot=(R(-10*nrm),0,0))
    # upper colonial floors
    for f in range(floors):
        zb=H0+1.0+f*3.2
        B.box((cx,back,zb+1.6),(w/2,3.0,1.6),ST,.03); B.box((cx,yf+nrm*.12,zb+.05),(w/2+.05,.2,.1),ST2,.02)
        nwin=max(1,int(w/1.9))
        for k in range(nwin):
            wx=x0+w*(k+.5)/nwin
            B.box((wx,yf+nrm*.03,zb+1.45),(.5,.04,.85),M('#3E5A4E',.6,kind='wood'),.01); B.cyl((wx,yf+nrm*.03,zb+2.3),.5,.08,M('#3E5A4E',.6,kind='wood'),rot=(R(90),0,0),seg=18)
            B.box((wx,yf+nrm*.06,zb+1.45),(.02,.02,.85),M('#E8E0D0',.6),0); B.box((wx,yf+nrm*.1,zb+.55),(.62,.1,.06),ST2,.01)
            if r.random()<.4: B.box((wx,yf+nrm*.45,zb+.3),(.7,.4,.05),ST2,.01); [B.box((wx-.6+j*.2,yf+nrm*.82,zb+.62),(.02,.02,.3),M('#2B2C33',.4,metal=.6),0) for j in range(7)]; B.box((wx,yf+nrm*.82,zb+.94),(.7,.03,.03),M('#2B2C33',.4,metal=.6),0)
            if r.random()<.3: B.box((wx+.75,yf+nrm*.25,zb+1.0),(.25,.18,.15),M('#D8DEE6',.4),.03)
    zt=H0+1.0+floors*3.2
    B.box((cx,yf+nrm*.1,zt+.2),(w/2+.08,.25,.2),ST2,.03)
    for k in range(int(w/.6)): B.box((x0+.3+k*.6,yf+nrm*.1,zt+.55),(.12,.12,.15),ST2,.02)

def bazaar(seed=21):
    """Lane along x, floor z=0, y in [-4,0]. Hero cloth shop: x -3..3, y 0..5.2, floor z=.15, open front. Returns dict(fan, shirts)."""
    r=random.Random(seed)
    # ground
    B.box((0,-3.5,-.05),(70,3.5,.05),M('#8A8274',.9,kind='concrete',sc=.5),0)
    for k in range(-34,35): B.box((k*2.0+.0,-3.5,.004),(.02,3.5,.004),M('#6E675C',.9),0)
    B.box((0,-3.5,.006),(70,.08,.004),M('#5A544A',.9),0)
    names_n=['AL-KARAM FABRICS','SADDAR WATCH CO','PAK SWEETS','BOLTON TAILORS','CITY BAGS','NOOR JEWELLERS','LYARI SPORTS','QUETTA CHAI']
    names_s=['KARACHI CLOTH HOUSE','MADINA SHOES','ROYAL PERFUMES','MEMON CROCKERY','ZAM ZAM ELECTRONICS','BURNS ROAD BIRYANI','CLIFTON OPTICS','SEA VIEW TOYS','GULSHAN BOOKS']
    cols=['#1F5A7A','#8E2A3A','#2E6E4A','#5A3A8A','#B05A1E','#22303E','#7A1E4A','#1F6E6E']
    # north side (y>=0) shops left and right of the hero shop
    x=-34.0; i=0
    while x<34:
        w=r.uniform(4.2,6.0)
        if x<3.0 and x+w>-3.0:
            if x<-3.0-2.5: w=-3.0-x
            else: x=3.0; continue
        facade(x,x+w,0.0,-1,r,names_n[i%len(names_n)],cols[i%len(cols)],stone=r.choice(('#D8C09A','#CDB58C','#E0CBA8')),floors=r.choice((2,2,3))); x+=w; i+=1
    x=-34.0; i=0
    while x<34:
        w=r.uniform(4.2,6.0); facade(x,x+w,-7.0,1,r,names_s[i%len(names_s)],cols[(i+3)%len(cols)],stone=r.choice(('#D8C09A','#CDB58C','#E0CBA8')),floors=r.choice((2,3,3))); x+=w; i+=1
    # overhead: cloth canopies, wires, bulbs
    for k in range(18):
        xx=-32+k*3.8; B.box((xx,-3.5,5.9+.2*math.sin(k)),(.9,3.6,.02),M(r.choice(('#E8742A','#F2C14E','#2E8B57','#C9302C','#F4F1EA','#2E6E9E')),.9,kind='fabric',alpha=1.0),.0,rot=(0,R(8*math.sin(k*2)),0))
    wires(-34,34,-6.9,-.1,5.2,5,seed)
    for k in range(-30,31,6): B.cyl((k,-6.8,2.6),.06,5.2,M('#5A5F66',.5,metal=.4),seg=8); B.box((k,-6.5,5.0),(.08,.3,.05),M('#5A5F66',.5),0); B.box((k,-6.2,4.95),(.12,.1,.05),M('#FFF2D8',.3,emit=1.5),.02)
    # street life: carts, crates, parked bikes
    for (cx,cy) in ((-26,-6.2),(27,-1.0),(-17,-1.0),(14,-1.0),(22,-6.2)):
        B.box((cx,cy,.55),(.8,.45,.05),M('#6B4A2A',.6,kind='wood'),.02)
        for sx in (-1,1): B.cyl((cx+sx*.6,cy,.3),.3,.06,M('#2B2C33',.6),rot=(R(90),0,0),seg=14)
        for k in range(10): B.ico((cx-.6+(k%5)*.3,cy-.2+(k//5)*.35,.7),.11,M(r.choice(('#E8742A','#F2C14E','#C9302C','#6FA84A')),.6),sub=1)
        B.box((cx,cy,1.9),(.9,.55,.03),M(r.choice(('#C9302C','#2E6E9E','#F2C14E')),.85,kind='fabric'),.01)
        for sx in (-1,1): B.cyl((cx+sx*.75,cy+.4,1.2),.02,1.4,M('#8A8F99',.4,metal=.6),seg=6)
    # far end: road with minibus and clock tower (Empress-market style)
    B.box((40,-3.5,-.04),(6,30,.05),M('#4A4C52',.9,kind='asphalt'),0)
    ST=M('#D2B48A',.85,kind='concrete',sc=.5)
    B.box((52,-3.5,5),(5,9,5),ST,.05); B.box((52,-3.5,15),(2.2,2.2,7),ST,.05); B.box((52,-3.5,23),(1.6,1.6,1.5),ST,.05)
    for s in (-1,1): B.cyl((49.75,-3.5+s*0,17.5),1.3,.1,M('#F4F1EA',.5),rot=(0,R(90),0),seg=24)
    B.box((49.68,-3.5,17.9),(.02,.05,.5),M('#1E1A18',.5),0); B.box((49.68,-3.2,17.5),(.02,.35,.05),M('#1E1A18',.5),0)
    for k in range(4): B.box((52+(1.9 if k%2 else -1.9),-3.5+(1.9 if k<2 else -1.9),23),(.3,.3,2.0),ST,.03)
    for k in range(6): B.cyl((47,-10.5+k*2.8,3),1.0,.1,M('#3E5A4E',.6),rot=(0,R(90),0),seg=18)
    minibus(40,-9,90); rickshaw(39.5,2.5,90)
    B.box((0,-2,-.2),(120,60,.1),M('#8A8274',.95),0)
    for k in range(14):
        xx=r.uniform(-60,60); yy=r.choice((-1,1))*r.uniform(14,30)-3.5; h=r.uniform(9,18); B.box((xx,yy,h/2),(r.uniform(3,6),r.uniform(3,6),h/2),M(r.choice(('#D8C09A','#C8B8A0','#E0D0B8','#B8A890')),.95,kind='wall'),0)
    # ---------------- hero shop
    WAL=M('#EDE3CF',.85,kind='wall'); WOOD=M('#6B4226',.5,kind='wood',sc=2); FL=M('#C9B99A',.4,kind='tile',sc=1.2)
    B.box((0,2.6,.075),(3.0,2.6,.075),FL,.01); B.box((0,-.12,.05),(3.0,.14,.05),M('#B8AC98',.8,kind='concrete'),.01)
    B.box((0,5.25,2.0),(3.05,.06,2.0),WAL,0)
    for s in (-1,1): B.box((s*3.02,2.6,2.0),(.06,2.6,2.0),WAL,0); B.box((s*2.92,.0,2.0),(.14,.14,2.0),M('#D2B48A',.85,kind='concrete'),.02)
    B.box((0,2.6,3.95),(3.05,2.65,.06),M('#F4F1EA',.9),0)
    # upper floors above hero shop
    for f in range(2):
        zb=4.6+f*3.2; ST_=M('#D8C09A',.85,kind='concrete',sc=.6); B.box((0,3.0,zb+1.6),(3.0,3.0,1.6),ST_,.03); B.box((0,-.12,zb+.05),(3.05,.2,.1),M('#B8A07A',.85),.02)
        for k in range(3):
            wx=-2+k*2; B.box((wx,-.03,zb+1.45),(.5,.04,.85),M('#3E5A4E',.6,kind='wood'),.01); B.cyl((wx,-.03,zb+2.3),.5,.08,M('#3E5A4E',.6,kind='wood'),rot=(R(90),0,0),seg=18); B.box((wx,-.1,zb+.55),(.62,.1,.06),M('#B8A07A',.85),.01)
    sign('BISMILLAH GARMENTS',(0,-.3,4.28),(0,-1,0),5.6,.62,fg='#FFE9A8',bg='#7A1E2E',emit=.9,border='#C9A24A')
    # shelves on back + side walls with cloth stacks
    for z in (.55,1.2,1.85,2.5,3.15):
        B.box((0,5.0,z),(2.9,.22,.025),WOOD,.005)
        for k in range(14): cloth_stack(-2.7+k*.415,5.0,z+.02,r.randint(3,6) if z<3 else r.randint(2,4),r,w=.18,d=.18)
    for s in (-1,1):
        for z in (.55,1.2,1.85,2.5):
            B.box((s*2.78,3.6,z),(.2,1.3,.025),WOOD,.005)
            for k in range(6): cloth_stack(s*2.78,2.5+k*.44,z+.02,r.randint(3,6),r,w=.18,d=.17)
    # hanging shirt rail on side walls near front + mannequins
    for s in (-1,1):
        B.cyl((s*2.6,1.2,2.75),.02,1.9,M('#8A8F99',.3,metal=.8),rot=(R(90),0,0),seg=8)
        for k in range(6): shirt_hang(s*2.6,.45+k*.3,2.7,CLOTH[(k*2+(0 if s>0 else 3))%len(CLOTH)],(-s,0))
    mannequin(-2.3,.55,.15,'#C9302C',10); mannequin(2.3,.55,.15,'#F2C14E',-10)
    # counter (glass front) with displays
    B.box((0,2.6,.62),(2.1,.27,.47),WOOD,.02); B.box((0,2.32,.62),(2.0,.012,.38),M('#BFD8E8',.05,spec=1.0,alpha=.35),0); B.box((0,2.6,1.1),(2.15,.3,.02),M('#D8C8A8',.3,kind='wood'),.01)
    for k in range(7): cloth_stack(-1.75+k*.58,2.5,.22,3,r,w=.2,d=.13)
    # counter props: till, tape, FIXED PRICE sign
    B.box((1.7,2.65,1.2),(.2,.16,.09),M('#2B2C33',.4,metal=.3),.02); B.box((1.7,2.6,1.32),(.16,.06,.04),M('#9FD8FF',.3,emit=.6),.01)
    B.cyl((-1.75,2.65,1.14),.07,.04,M('#F2C14E',.5),seg=14)
    sign('FIXED PRICE',(0,4.74,2.98),(0,-1,0),1.3,.3,fg='#C9302C',bg='#FFFFFF',border='#2B2C33')
    sign('NO BARGAINING',(0,4.74,2.66),(0,-1,0),1.3,.2,fg='#2B2C33',bg='#FFFFFF')
    # ceiling tube lights
    for xx in (-1.5,1.5): B.box((xx,2.6,3.86),(.7,.04,.03),M('#F4F8FF',.2,emit=7.0),0)
    B.box((0,.9,3.86),(1.2,.04,.03),M('#F4F8FF',.2,emit=7.0),0)
    B.done('bazaar')
    # ceiling fan (animated)
    fan=empty((0,2.0,3.55)); ocyl((0,0,.18),.03,.4,M('#8A8F99',.3,metal=.8),fan); ocyl((0,0,0),.12,.08,M('#E8E0D0',.4),fan)
    for k in range(3): obox((.45*math.cos(k*2.094),.45*math.sin(k*2.094),0),(.4,.07,.008),M('#E8E0D0',.4),.004,fan,rot=(0,0,k*2.094))
    # the blue shirts (folded) on counter, a calculator, shopkeeper's stool
    def folded(col):
        e=empty((0,0,0)); obox((0,0,.035),(.2,.26,.035),M(col,.8,kind='fabric'),.015,e); obox((0,-.17,.075),(.1,.06,.012),M(shade(col,.8),.8,kind='fabric'),.008,e)
        for j in range(3): ocyl((0,-.05+j*.09,.073),.012,.006,M('#F4F1EA',.4),e,seg=8)
        return e
    s1=folded('#2E6EC9'); s2=folded('#2E6EC9')
    calc=empty((0,0,0)); obox((0,0,.012),(.07,.11,.012),M('#2B2C33',.4),.006,calc); obox((0,.06,.026),(.055,.03,.003),M('#B8D8B0',.3,emit=.4),0,calc)
    for a in range(3):
        for b_ in range(3): obox((-.04+a*.04,-.07+b_*.04,.026),(.013,.013,.003),M('#D8DEE6',.5),0,calc)
    stool=empty((2.2,3.6,.15)); ocyl((0,0,.45),.2,.05,M('#C9302C',.6),stool); [ocyl((.13*math.cos(a),.13*math.sin(a),.22),.02,.44,M('#8A8F99',.3,metal=.8),stool) for a in (0,1.57,3.14,4.71)]
    bag=empty((0,0,0)); obox((0,0,-.2),(.17,.06,.2),M('#F4F1EA',.6),.01,bag); obox((0,-.062,-.2),(.1,.002,.05),M('#7A1E2E',.6),0,bag); obox((0,0,.02),(.07,.008,.02),M('#F4F1EA',.6),.004,bag)
    return dict(fan=fan,s1=s1,s2=s2,calc=calc,stool=stool,bag=bag)
