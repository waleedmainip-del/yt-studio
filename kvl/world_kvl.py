# World for "Karachi vs Lahore": THE LINE - a closed motorway in the middle of the country.
# Lahore half = x<0 (fans face +x), Karachi half = x>0 (fans face -x). The arena is open toward -y, where the camera works. Scoreboard + banners on +y.
MOODS['kv_day']=dict(sun=(52,-150),e=3.1,col=(1,.94,.82),top='#2E86E0',bot='#CDE9FF',sky=.95,mist='#DCEAF4',cloud='#FFFFFF',cov=.5,cstr=.9)
MOODS['kv_gold']=dict(sun=(70,-128),e=2.6,col=(1,.78,.5),top='#4A78C8',bot='#FFC890',sky=.9,mist='#F0C8A0',cloud='#FFD8B8',cov=.5,cstr=.85)
MOODS['kv_dusk']=dict(sun=(80,-120),e=1.7,col=(1,.6,.44),top='#34388A',bot='#FF8A5A',sky=.9,mist='#B88278',cloud='#F0889A',cov=.45,cstr=.85)
MOODS['kv_night']=dict(sun=(55,-160),e=.5,col=(.62,.72,1.0),top='#060A20',bot='#1E2A52',sky=.6,mist='#18203C',cloud='#28325A',cov=.4,cstr=.6)
MOODS['kv_morn']=dict(sun=(64,150),e=2.7,col=(1,.9,.76),top='#4C92E0',bot='#FFE3C8',sky=.88,mist='#E8E0D6',cloud='#FFFFFF',cov=.55,cstr=.85)
RWK=13.0; BACKY=14.4; BOARD=[True]
def ground_text(body,x,y,size,col,rz=0.0,e=0.0,z=.014):
    cu=bpy.data.curves.new('gt','FONT'); cu.body=body; cu.align_x='CENTER'; cu.align_y='CENTER'; cu.size=size; cu.extrude=.003
    o=bpy.data.objects.new('gt',cu); o.location=(x,y,z); o.rotation_euler=(0,0,R(rz)); _col.objects.link(o); cu.materials.append(M(col,.6,emit=e) if e else M(col,.6)); return o
def minar(x,y,s=1.0,col='#F2EEE6',parent=None):
    """Minar-e-Pakistan style tower (3D)"""
    e=empty((x,y,0),parent); m=M(col,.6); d=M(shade(col,.8),.6)
    ocyl((0,0,.25*s),2.6*s,.5*s,d,e,rot=(0,0,0),seg=10); ocyl((0,0,.75*s),1.9*s,.5*s,m,e,rot=(0,0,0),seg=10); ocyl((0,0,1.4*s),1.2*s,.8*s,d,e,rot=(0,0,0),seg=10)
    ocyl((0,0,5.2*s),.7*s,6.8*s,m,e,rot=(0,0,0),seg=10,r2=.42*s)
    for k in range(4): ocyl((0,0,(2.9+k*1.7)*s),(.76-.07*k)*s,.14*s,d,e,rot=(0,0,0),seg=10)
    ocyl((0,0,8.75*s),.5*s,.3*s,d,e,rot=(0,0,0),seg=10); oico((0,0,9.15*s),.42*s,m,e,sc=(1,1,1.15),sub=2); ocyl((0,0,9.85*s),.04*s,.7*s,M('#D9B24A',.3,metal=.9),e,rot=(0,0,0),seg=6)
    return e
def flat_minar(par,x,z,s,col='#F6F0DA'):
    m=M(col,.6)
    obox((x,-.03,z-.95*s),(.52*s,.02,.1*s),m,0,par); obox((x,-.03,z-.75*s),(.36*s,.02,.1*s),m,0,par); obox((x,-.03,z+.05*s),(.13*s,.02,.72*s),m,0,par)
    obox((x,-.03,z+.84*s),(.17*s,.02,.07*s),m,0,par); obox((x,-.03,z+1.0*s),(.09*s,.02,.1*s),m,0,par); obox((x,-.03,z+1.2*s),(.015*s,.02,.12*s),m,0,par)
def flat_mazar(par,x,z,s,col='#F6F8FC'):
    m=M(col,.6)
    obox((x,-.03,z-.5*s),(.62*s,.02,.42*s),m,0,par); ocyl((x,-.03,z+.02*s),.5*s,.04,m,par,seg=24); obox((x,-.04,z-.55*s),(.18*s,.02,.3*s),M('#2466C9',.6),0,par); ocyl((x,-.04,z-.25*s),.18*s,.04,M('#2466C9',.6),par,seg=16)
    obox((x,-.03,z-.98*s),(.8*s,.02,.07*s),m,0,par)
def bunting(p,q,n,cols,sag=.7):
    wm=M('#3A3D44',.6); P=[]
    for k in range(n+1):
        f=k/n; z=L(p[2],q[2],f)-sag*4*f*(1-f); P.append((L(p[0],q[0],f),L(p[1],q[1],f),z))
    for k in range(n): bseg(P[k],P[k+1],.012,wm,seg=4)
    dx=q[0]-p[0]; dy=q[1]-p[1]; a=math.atan2(dy,dx)
    for k in range(n):
        c=((P[k][0]+P[k+1][0])/2,(P[k][1]+P[k+1][1])/2,(P[k][2]+P[k+1][2])/2-.2)
        B.box(c,(.16,.008,.2),M(cols[k%len(cols)],.7,kind='fabric'),0,rot=(0,R(45) if False else 0,a))
def flood_tower(x,y,h=13.0,face=(0,0)):
    pm=M('#6E7378',.5,metal=.5); B.cyl((x,y,h/2),.22,h,pm,seg=8,r2=.14); a=math.atan2(face[1]-y,face[0]-x)
    B.box((x,y,h+.5),(.14,1.5,.75),M('#3A3D44',.5),.03,rot=(0,0,a))
    for i in range(3):
        for j in range(2): B.box((x+math.cos(a)*.16-math.sin(a)*(i-1)*.9,y+math.sin(a)*.16+math.cos(a)*(i-1)*.9,h+.15+j*.7),(.03,.36,.28),lit('#FFF4D6',9.0),0,rot=(0,0,a))
def poplar(x,y,s=1.0,seed=0):
    r=random.Random(seed); B.cyl((x,y,1.5*s),.16*s,3.0*s,M('#6B4A2E',.85),seg=6)
    for k in range(4): B.ico((x+r.uniform(-.2,.2),y+r.uniform(-.2,.2),(3.2+k*1.5)*s),(1.25-.2*k)*s,M(r.choice(['#3F7A3A','#4F8A3A','#356E34','#5A9440']),.85,kind='leaves'),sc=(1,1,1.5),sub=1)
def nashta_table(x,y,rz=0):
    """Lahori breakfast table: puri stack, halwa, paaye pot, chanay, three tall lassi glasses"""
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#8A5A36',.6,kind='wood',sc=.6); st=M('#C9CED8',.25,metal=.9)
    obox((0,0,.98),(1.25,.62,.04),wd,.02,e); obox((0,0,1.03),(1.27,.64,.012),M('#F2E9D0',.7,kind='fabric'),.005,e); obox((0,-.63,.8),(1.27,.012,.22),M('#1F7A44',.7,kind='fabric'),.004,e)
    for sx in (-1,1):
        for sy in (-1,1): obox((sx*1.1,sy*.48,.47),(.05,.05,.47),wd,.01,e)
    for k in range(7): ocyl((-.8,.05,1.07+k*.035),.27-.004*k,.03,M(['#E8B85A','#DDA646','#F0C46A'][k%3],.6),e,rot=(0,0,R(k*20)),seg=14)   # puris
    ocyl((-.2,.12,1.1),.24,.12,st,e,rot=(0,0,0),seg=16,r2=.18); ocyl((-.2,.12,1.15),.2,.03,M('#E8862A',.5),e,rot=(0,0,0),seg=14)                  # halwa
    ocyl((.42,.1,1.2),.3,.32,st,e,rot=(0,0,0),seg=18); ocyl((.42,.1,1.35),.27,.03,M('#8A3A1E',.5),e,rot=(0,0,0),seg=16)                        # paaye pot
    for s_ in (-1,1): obox((.42+s_*.33,.1,1.3),(.05,.03,.02),st,.01,e)
    ocyl((-.25,-.32,1.07),.2,.05,M('#F4F1EA',.4),e,rot=(0,0,0),seg=14); ocyl((-.25,-.32,1.1),.16,.02,M('#C99A4A',.6),e,rot=(0,0,0),seg=12)       # chanay
    for k in range(3):
        ocyl((.72+k*.2,-.3,1.22),.075,.36,st,e,rot=(0,0,0),seg=12,r2=.06); ocyl((.72+k*.2,-.3,1.41),.078,.03,M('#FFFDF4',.5),e,rot=(0,0,0),seg=12)
    return e
def degh(x,y,rz=0,s=.72):
    """Karachi biryani degh on a stand; returns dict(root,lid)"""
    e=empty((x,y,0),rot=(0,0,R(rz))); e.scale=(s,s,s); st=M('#B8BCC4',.3,metal=.9); cu=M('#B8763A',.3,metal=.85); blk=M('#2A2C34',.6)
    for a in range(4): obox((.55*math.cos(a*pi/2+.78),.55*math.sin(a*pi/2+.78),.3),(.05,.05,.3),blk,.01,e)
    ocyl((0,0,.62),.72,.06,blk,e,rot=(0,0,0),seg=20); ocyl((0,0,1.0),.78,.7,cu,e,rot=(0,0,0),seg=24,r2=.62); ocyl((0,0,1.36),.82,.06,st,e,rot=(0,0,0),seg=24)
    ocyl((0,0,1.36),.72,.05,M('#E8B85A',.7),e,rot=(0,0,0),seg=20)
    r=random.Random(5)
    for k in range(26): a=r.uniform(0,6.28); d=r.uniform(0,.62); obox((d*math.cos(a),d*math.sin(a),1.4),(.035,.012,.012),M(r.choice(['#FFF6D8','#F28A1A','#F4F1EA','#E8C547']),.6),0,e,rot=(0,0,a))
    for k in range(5): a=k*1.26+.4; oico((.4*math.cos(a),.4*math.sin(a),1.44),.11,M('#E0B45A',.6),e,sc=(1.2,1,.8),sub=1)                                # aloo
    for k in range(3): a=k*2.1+1.2; obox((.2*math.cos(a),.2*math.sin(a),1.44),(.1,.07,.05),M('#8A4A26',.6),.03,e,rot=(0,0,a))                             # boti
    lid=empty((0,0,1.42),e); ocyl((0,0,.05),.84,.1,st,lid,rot=(0,0,0),seg=24,r2=.7); ocyl((0,0,.16),.1,.1,blk,lid,rot=(0,0,0),seg=10)
    sign('KARACHI BIRYANI',(0,-.8,.92),.13,'#FFFFFF','#2466C9',n=(0,-1,0),pad=.07,th=.02,parent=e)
    return dict(root=e,lid=lid)
def cutout(x,y,kind,rz=0):
    """city pride cut-out on a pole stand: 'badshahi' (domes + minarets) or 'sea' (waves + boat). Board faces local -y. returns empty (scale to pop)"""
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#6B4A2E',.7)
    for sx in (-1.5,1.5): obox((sx,.06,1.7),(.05,.04,1.7),wd,.01,e); obox((sx,.06,.05),(.3,.3,.05),wd,.01,e)
    if kind=='badshahi':
        red=M('#B8553A',.7); wh=M('#F6F2E8',.5)
        obox((0,0,3.2),(2.3,.04,.55),red,.0,e); obox((0,-.02,3.05),(.4,.04,.4),M('#3A2A22',.7),0,e); ocyl((0,-.02,3.45),.4,.08,M('#3A2A22',.7),e,seg=16)
        for dx,rr in ((-1.15,.5),(0,.72),(1.15,.5)): ocyl((dx,0,3.78),rr,.08,wh,e,seg=24); obox((dx,0,3.78+rr+.12),(.03,.04,.14),M('#D9B24A',.3,metal=.9),0,e)
        for sx in (-2.15,2.15): obox((sx,0,3.7),(.16,.04,1.05),red,0,e); ocyl((sx,0,4.78),.22,.08,wh,e,seg=16)
        sign('BADSHAHI MASJID',(0,-.04,2.35),.22,'#FFF6D8','#1F7A44',n=(0,-1,0),pad=.1,th=.03,parent=e)
    else:
        sea=M('#2E86D0',.4); fo=M('#F4F8FC',.5)
        obox((0,0,3.1),(2.3,.04,.6),sea,0,e)
        for k in range(8): ocyl((-2.0+k*.57,-.01,3.7),.3,.08,sea,e,seg=16); ocyl((-2.0+k*.57,-.02,3.78),.12,.06,fo,e,seg=10)
        obox((.5,-.03,4.05),(.55,.04,.12),M('#C8372D',.6),.02,e); obox((.5,-.03,4.5),(.03,.04,.36),wd,0,e); obox((.72,-.03,4.5),(.2,.03,.26),fo,0,e)
        ocyl((-1.3,-.03,4.9),.3,.06,M('#FFD86A',.4,emit=1.5),e,seg=20)
        sign('SEA VIEW',(0,-.04,2.3),.24,'#FFFFFF','#2466C9',n=(0,-1,0),pad=.1,th=.03,parent=e)
    return e
SCORE={}
BOARDOBJ=[]
BOARDKEEP=set()
def scoreboard(draws=74,year=75):
    y=BACKY-.4; dk=M('#16181E',.5); fr=M('#3A3D44',.5,metal=.4)
    for sx in (-2.6,2.6): B.box((sx,y+.3,2.0),(.18,.18,2.0),fr,.02)
    B.box((0,y+.2,6.6),(3.3,.16,2.75),dk,.03); B.box((0,y+.26,6.6),(3.42,.12,2.87),fr,.02)
    sign('THE BIG FIGHT',(0,y+.06,8.75),.36,'#FFE08A','#16181E',n=(0,-1,0),e=3.0,pad=.1,th=.05,always=True)
    sign('YEAR %d'%year,(0,y+.06,8.02),.26,'#FFFFFF','#16181E',n=(0,-1,0),e=2.0,pad=.08,th=.05,always=True)
    for x,lab,col in ((-2.15,'LAHORE','#3FC77A'),(0,'DRAWS','#FFE08A'),(2.15,'KARACHI','#6FC3EA')):
        sign(lab,(x,y+.06,7.25),.26 if lab!='KARACHI' else .24,col,'#16181E',n=(0,-1,0),e=2.5,pad=.06,th=.05,always=True)
        B.box((x,y+.1,5.55),(.95,.06,1.05),M('#0C0D12',.4),.02)
    em=lambda c: M(c,.4,emit=3.2)
    SCORE['L']=text('0',(-2.15,y,5.55),(0,-1,0),1.25,em('#3FC77A'),ex=.02); SCORE['K']=text('0',(2.15,y,5.55),(0,-1,0),1.25,em('#6FC3EA'),ex=.02)
    SCORE['D0']=text(str(draws),(0,y,5.55),(0,-1,0),1.05,em('#FFE08A'),ex=.02); SCORE['D1']=text(str(draws+1),(0,y,5.55),(0,-1,0),1.05,em('#FFE08A'),ex=.02); SCORE['D1'].scale=(0,0,0)
def score_draw(k):
    """k=0 old number, 1 new number (with a pop)"""
    a=SCORE['D0']; b=SCORE['D1']; a.scale=(1,1,1) if k<=0 else (0,0,0); s=0 if k<=0 else min(1.25,k*1.25) if k<1 else 1; b.scale=(s,s,s)
def tok_team(r,x,y,rz,team,z=0.0,arms=None):
    if team=='L': t=r.choice(['#C8372D','#E6B53A','#D9367A','#F2E9D0','#35975A','#F28A3A','#8A1F3A','#1F7A44','#E8C547','#F4F1EA']); p=r.choice([t,'#F2E9D0','#F4F1EA'])
    else: t=r.choice(['#F4F6FA','#6FC3EA','#27365A','#9AA8BC','#16909E','#2466C9','#C9D6E8','#3A8A9A','#7448C2','#2A2C34']); p=r.choice(['#23252E','#3A4A6A','#27365A','#4A4E5A'])
    token(x,y,rz,t,p,r.choice(TOKS),r.choice(['#15110E','#2A1E16','#3A2A1E']),h=r.uniform(.86,1.05),z=z,arms=arms)
def arena(mood='kv_day',night=0.0,seed=3,shadow=80,tokens=True,draws=74,vehicles=True,far=True,focus=(0,-4.0),xmin=8.2,stand=True,gtext=False,tanker_=True,south=True):
    """THE LINE arena. returns dict(sun=S)"""
    NIGHT[0]=night; r=random.Random(seed)
    B.box((0,40,-.08),(300,220,.05),M('#7FA850',.95,kind='grass',sc=.5),0)                                  # fields
    B.box((0,0,-.03),(300,RWK+1.6,.03),M('#A89E88',.9,kind='concrete',sc=.4),0)                             # shoulders
    B.box((0,0,-.01),(300,RWK,.02),M('#3A3C42',.82,kind='asphalt'),0)                                        # motorway
    wl=M('#EEECE2',.5); yl=M('#E8B83A',.5)
    for s in (-1,1):
        B.box((0,s*(RWK-.5),.012),(300,.09,.004),yl,0)
        for ly in (4.33,8.66):
            for k in range(-40,41):
                x=k*7.0
                if abs(x)<26: continue
                B.box((x,s*ly,.012),(1.6,.08,.004),wl,0)
    B.box((0,0,.014),(.32,RWK,.006),M('#F6F6F0',.85),0)                                                      # THE LINE
    B.done('road')
    if gtext: ground_text('LAHORE',-6.2,-5.6,2.3,'#F2EEE0'); ground_text('KARACHI',6.6,-5.6,2.3,'#F2EEE0')
    for s,cx in (((-1,-6.2),(1,6.6)) if gtext else ()):
        B.box((cx,-8.1,.014),(2.4,.14,.004),wl,0); B.box((cx+s*2.4,-8.1,.014),(.5,.14,.004),wl,0,rot=(0,0,R(-s*38))) ; B.box((cx+s*2.4,-8.1,.014),(.5,.14,.004),wl,0,rot=(0,0,R(s*38)))
    # back wall: bleachers + team banners + scoreboard
    cm=M('#B8B2A4',.85,kind='concrete',sc=.5)
    if stand:
        for k in range(3): B.box((0,11.3+k*1.25,.22+k*.42),(27,.65,.22+k*.42),cm,.02)
        for s,bg,col,nm in ((-1,'#1F7A44','#F2D36A','LAHORE'),(1,'#2466C9','#FFFFFF','KARACHI')):
            cx=s*14.0; B.box((cx,BACKY+.35,7.0),(9.8,.14,2.6),M(bg,.6,kind='fabric',sc=1.5),0); B.box((cx,BACKY+.42,7.0),(10.0,.1,2.8),M('#E6B53A' if s<0 else '#F4F6FA',.5),0)
            for px in (-9.0,0,9.0): B.box((cx+px,BACKY+.7,2.4),(.16,.16,2.4),M('#5A5E66',.5,metal=.4),.02)
            ic=empty((cx,BACKY+.19,0))
            if s<0: flat_minar(ic,0,6.9,1.75,'#F6E7A8')
            else: flat_mazar(ic,0,7.2,2.0,'#F6F8FC')
            for dx in (-6.0,6.0):
                for k_ in range(2): obox((dx,-.03,7.0),(.32,.02,.32),M(col,.5),0,ic,rot=(0,R(45*k_),0))
        if BOARD[0]:
            B.done('wall'); _b0={o.name for o in bpy.data.objects}; scoreboard(draws); B.done('board'); BOARDOBJ[:]=[o for o in bpy.data.objects if o.name not in _b0]
    B.done('wall')
    # crowd tokens: bleachers + road blocks behind the real fans
    if tokens:
        if stand:
            for k in range(3):
                for i in range(24):
                    for s,tm in ((-1,'L'),(1,'K')):
                        x=s*(3.9+i*.96); 
                        if i%2==k%2 or r.random()<.12: continue
                        y_=11.3+k*1.25; tok_team(r,x,y_,face_dir(focus[0]-x,focus[1]-y_),tm,z=.44+k*.84,arms='up' if r.random()<.28 else None)
        for s,tm in ((-1,'L'),(1,'K')):
            for ix in range(8):
                for iy in range(6):
                    x=s*(xmin+ix*1.9); y_=-.4+iy*1.95+(.5 if ix%2 else 0)
                    if r.random()<.14 or y_>9.9: continue
                    tok_team(r,x,y_,face_dir(focus[0]-x,focus[1]-y_),tm,arms='up' if r.random()<.22 else None)
        B.done('tokens')
    # bunting, floodlights, flags
    for s,cols in ((-1,['#1F7A44','#E6B53A','#F4F1EA']),(1,['#2466C9','#F4F6FA','#6FC3EA'])):
        for yy,zz in ((3.5,8.6),(8.5,9.0)):
            bunting((s*23.5,yy,zz+1.2),(0,yy,zz),30,cols,sag=1.0)
        flood_tower(s*24.5,12.6,13.0,face=(s*8,0)); flood_tower(s*24.5,-2.0,13.0,face=(s*6,3))
        for k in range(3): flag_pk(s*(27.5+k*.01),2+k*4.5,h=6.0,rz=0)
    B.done('deco')
    if not BOARD[0]:
        for sx in (-2.6,2.6): B.box((sx,BACKY-.1,2.0),(.18,.18,.01),M('#5A5E66',.5),0)
    if night>0:
        for s in (-1,1):
            point((s*9,-3,9.5),2600*night,(1,.95,.86),r=1.2,shadow=False); point((s*4,7,9.0),1500*night,(1,.92,.8),r=1.0,shadow=False)
    # vehicles the teams came in
    V=[]
    if vehicles:
        V.append(w11((-27.0,7.2,0),0,seed=4,col='#1F7A44',accent='#E6B53A')); V.append(krick((-24.5,-6.0,0),8,col='#2E8A3A',seed=2))
        V.append(w11((27.0,7.2,0),180,seed=9,col='#2466C9',accent='#F4F6FA'))
    if tanker_: V.append(tanker((15.5,-5.4,0),180))
    # far scenery: poplars, fields, pylons, hills
    if far:
        for i in range(34):
            x=-130+i*8+r.uniform(-2,2); poplar(x,20+r.uniform(0,5),r.uniform(1.2,1.9),seed=i)
            if i%3==0: poplar(x+3,34+r.uniform(0,9),r.uniform(1.4,2.2),seed=100+i)
        for i in range(9):
            x=-120+i*30; B.box((x,60,-.02),(11,14,.03),M(['#C9B458','#8FB85A','#D8C870','#6E9A48'][i%4],.95),0)
        for i in range(7):
            x=-110+i*37; pm=M('#8A8E96',.5,metal=.4); B.cyl((x,46,8),.3,16,pm,seg=6,r2=.12); B.box((x,46,13.0),(.1,3.2,.1),pm,0); B.box((x,46,15.2),(.1,2.2,.1),pm,0)
        for i in range(14):
            x=-170+i*26+r.uniform(-6,6); B.ico((x,150+r.uniform(0,30),-4),r.uniform(22,36),M(['#6A8A6E','#7A987A','#5E7E68'][i%3],.95),sc=(1.5,1,.55),sub=2)
        if south:
            for i in range(26):
                x=-110+i*9+r.uniform(-2,2); poplar(x,-24-r.uniform(0,6),r.uniform(1.2,1.8),seed=300+i)
            for i in range(12):
                x=-150+i*28+r.uniform(-5,5); B.ico((x,-120-r.uniform(0,25),-6),r.uniform(26,40),M(['#4E7A52','#5E8A5C','#3E6A48'][i%3],.95),sc=(1.6,1,.62),sub=2)
        B.done('far')
    S=setup_world(mood,shadow); return dict(sun=S,V=V)
# ---------------------------------------------------------------- small interior sets
def room(w=5.2,d=4.4,h=3.4,wall='#CFE6DC',floor='#C9A27A',base='#F4F1EA',kind='wood'):
    """three-wall room open toward -y; floor at z=0"""
    B.box((0,0,-.05),(w+1,d+3,.05),M(floor,.6,kind=kind,sc=.7),0); B.box((0,d,h/2),(w,.1,h/2),M(wall,.85,kind='wall',sc=.5),0)
    for s in (-1,1): B.box((s*w,0,h/2),(.1,d+.1,h/2),M(shade(wall,.93),.85,kind='wall',sc=.5),0)
    B.box((0,d-.11,.09),(w,.02,.09),M(base,.6),0); B.box((0,0,h+.05),(w+.2,d+.2,.05),M('#F4F1EA',.9),0)
def frame(x,y,z,w,h,col,pic,n=(0,-1,0)):
    B.box((x,y,z),(w+.05,.03,h+.05),M(col,.5),.01); B.box((x,y-.02,z),(w,.02,h),M(pic,.6),0)
def nursery():
    room(wall='#FCE8C8',floor='#C9A27A',kind='tile'); B.done('room')
    B.cyl((0,.2,.012),1.75,.024,M('#B9A6E0',.85,kind='fabric'),seg=28); B.cyl((0,.2,.016),1.3,.026,M('#F4C9D2',.85,kind='fabric'),seg=24)
    frame(-2.9,4.28,2.25,.5,.38,'#F4F1EA','#8FD0F0'); frame(2.9,4.28,2.25,.5,.38,'#F4F1EA','#F2B8C8')
    B.box((0,4.25,2.3),(1.0,.05,.75),M('#BFE6FF',.2,emit=1.2),.0); B.box((0,4.22,2.3),(1.08,.03,.04),M('#F4F1EA',.5),0); B.box((0,4.22,2.3),(.04,.03,.78),M('#F4F1EA',.5),0)
    for s in (-1,1): B.box((s*1.2,4.2,2.3),(.22,.04,.85),M('#F2C14E',.8,kind='fabric'),.02)
    B.box((-4.3,3.2,.55),(.7,.5,.55),M('#F4F1EA',.6),.03)
    for k,c in enumerate(('#E8554D','#4D8FE8','#F2C14E')): B.box((-4.5+k*.3,3.1,1.24),(.12,.12,.12),M(c,.6),.02)
    B.box((4.2,3.3,.4),(.55,.7,.4),M('#C9A27A',.6,kind='wood'),.03); B.ico((4.2,3.3,1.05),.3,M('#B8763A',.8),sub=2); B.ico((4.02,3.2,1.32),.11,M('#B8763A',.8),sub=1); B.ico((4.38,3.2,1.32),.11,M('#B8763A',.8),sub=1)
    B.done('nursery')
    P={}
    for s,nm,bg,col in ((-1,'LAHORE','#1F7A44','#F2D36A'),(1,'KARACHI','#2466C9','#FFFFFF')):
        e=empty((s*.7,.25,0)); obox((0,0,.03),(.13,.13,.03),M('#C9A27A',.6),.01,e); ocyl((0,0,.65),.022,1.25,M('#D9B24A',.3,metal=.9),e,rot=(0,0,0),seg=8)
        sign(nm,(0,-.03,1.2),.13,col,bg,n=(0,-1,0),pad=.06,th=.016,parent=e); P[nm]=e
    S,A,w_,bg_=setup_interior('day',room=(0,-.5,3.3),res=PCT,samples=SAMPLES,shadow_dist=18); A.data.energy=125; A.data.size=10; point((0,-4.5,2.6),420,(1,.96,.9),r=2.0,shadow=False)
    return P
def office():
    w=5.4; d=4.2; h=3.4; wall='#C9D3DE'
    B.box((0,0,-.05),(w+1,d+3,.05),M('#8A8E96',.6,kind='tile',sc=.7),0); B.box((0,d,h/2),(w,.1,h/2),M(wall,.85,kind='wall',sc=.5),0)
    B.box((-w,0,h/2),(.1,d+.1,h/2),M(shade(wall,.93),.85,kind='wall',sc=.5),0)
    wm=M(shade(wall,.93),.85,kind='wall',sc=.5); y0,y1=-1.75,.35
    B.box((w,(y1+d+.1)/2,h/2),(.1,(d+.1-y1)/2,h/2),wm,0); B.box((w,(-d-.1+y0)/2,h/2),(.1,(y0+d+.1)/2,h/2),wm,0); B.box((w,(y0+y1)/2,2.95),(.1,(y1-y0)/2,.45),wm,0)
    fr=M('#F4F1EA',.5); B.box((w-.12,y0,1.25),(.04,.06,1.25),fr,0); B.box((w-.12,y1,1.25),(.04,.06,1.25),fr,0); B.box((w-.12,(y0+y1)/2,2.52),(.04,(y1-y0)/2+.06,.04),fr,0)
    B.box((w+2.0,(y0+y1)/2,1.4),(1.9,(y1-y0)/2+.3,.02),M('#3A3D44',.8),0); B.box((w+3.9,(y0+y1)/2,1.4),(.05,1.4,1.4),M('#2A2C34',.8),0)
    B.box((w+2.0,(y0+y1)/2,-.03),(2.0,1.4,.03),M('#5A5E66',.7),0); B.box((w+2.0,(y0+y1)/2,2.85),(2.0,1.4,.03),M('#E8E8E8',.8),0)
    for s_ in (-1,1): B.box((w+2.0,(y0+y1)/2+s_*1.38,1.4),(2.0,.04,1.4),M('#B8C0CC',.85),0)
    B.box((w+2.0,(y0+y1)/2,2.8),(.6,.3,.03),M('#FFF8E8',.3,emit=2.5),0)
    B.box((0,d-.11,.09),(w,.02,.09),M('#F4F1EA',.6),0); B.box((0,0,h+.05),(w+.2,d+.2,.05),M('#F4F1EA',.9),0)
    B.done('room')
    wd=M('#6B4A2E',.5,kind='wood',sc=.6)
    B.box((0,1.3,.84),(1.5,.6,.04),wd,.02); B.box((0,.73,.42),(1.4,.03,.38),wd,.01)
    for s in (-1,1): B.box((s*1.4,1.3,.42),(.05,.55,.42),wd,.01)
    B.box((.95,1.25,.92),(.3,.2,.02),M('#2A2C34',.4),.01); B.box((.95,1.45,1.12),(.3,.02,.2),M('#2A2C34',.4),.01); B.box((.95,1.43,1.12),(.27,.01,.17),M('#9FD0F0',.3,emit=1.0),0)
    B.cyl((-1.25,1.55,.95),.05,.14,M('#C8372D',.5),seg=10)
    B.box((0,4.08,2.4),(1.4,.04,.8),M('#BFE6FF',.2,emit=1.3),0)
    for k in range(9): B.box((0,4.04,1.68+k*.18),(1.42,.02,.03),M('#F4F1EA',.6),0)
    frame(-3.3,4.08,2.0,.42,.55,'#D9B24A','#F2E9D0'); B.box((3.4,3.7,.9),(.5,.3,.9),M('#8A8E96',.5,metal=.4),.02)
    B.cyl((-4.4,3.4,.3),.3,.6,M('#B8553A',.7),seg=12,r2=.24); B.ico((-4.4,3.4,1.3),.6,M('#3F7A3A',.85,kind='leaves'),sc=(1,1,1.3),sub=1)
    B.done('office')
    sign('HR DEPARTMENT',(-3.3,4.07,3.0),.16,'#FFFFFF','#27365A',n=(0,-1,0),pad=.08,th=.02)
    sign('EXIT',(w-.12,(y0+y1)/2,2.8),.17,'#FFFFFF','#C8372D',n=(-1,0,0),e=2.5,pad=.08,th=.02,always=True)
    # executive chair (seat top .36) behind the desk
    e=empty((0,2.38,0)); bk=M('#16171C',.4)
    obox((0,0,.3),(.42,.4,.06),bk,.04,e); obox((0,.42,.95),(.42,.07,.62),bk,.05,e); ocyl((0,0,.13),.05,.26,M('#9AA0AA',.3,metal=.8),e,rot=(0,0,0),seg=8)
    for a in range(5): obox((.26*math.cos(a*1.257),.26*math.sin(a*1.257),.04),(.14,.025,.025),M('#9AA0AA',.3,metal=.8),.01,e,rot=(0,0,a*1.257))
    for s in (-1,1): obox((s*.46,.05,.5),(.04,.3,.03),bk,.02,e)
    paper=empty((-.55,1.15,.885)); obox((0,0,0),(.21,.29,.003),M('#F8F8F4',.7),0,paper); text('CV',(0,-.05,.004),(0,0,1),.12,M('#16171C',.5),ex=.001,parent=paper).rotation_euler=(0,0,0)
    S,A,w_,bg_=setup_interior('day',room=(0,-.5,3.3),res=PCT,samples=SAMPLES,shadow_dist=18); A.data.energy=185; A.data.size=10; point((0,-3.6,2.6),620,(1,.97,.94),r=2.0,shadow=False)
    return dict(paper=paper,door=((y0+y1)/2,w))
def roll_chair(x,y,rz,col='#3A4A6A'):
    """office chair on wheels, seat top .58, back toward local +y. returns empty"""
    e=empty((x,y,0),rot=(0,0,R(rz))); cm=M(col,.5); mt=M('#9AA0AA',.3,metal=.8)
    obox((0,0,.53),(.3,.3,.05),cm,.03,e); obox((0,.33,.92),(.29,.05,.34),cm,.04,e); ocyl((0,0,.3),.04,.44,mt,e,rot=(0,0,0),seg=8)
    for a in range(5): ang=a*1.257+.3; obox((.22*math.cos(ang),.22*math.sin(ang),.07),(.12,.022,.022),mt,.01,e,rot=(0,0,ang)); oico((.32*math.cos(ang),.32*math.sin(ang),.04),.04,M('#16171C',.5),e,sub=1)
    return e
def biryani_plate(par,loc,aloo=True):
    e=empty(loc,par); ocyl((0,0,.012),.2,.024,M('#F4F1EA',.4),e,rot=(0,0,0),seg=16); ocyl((0,0,.04),.16,.04,M('#E8B85A',.7),e,rot=(0,0,0),seg=14)
    r=random.Random(3)
    for k in range(10): a=r.uniform(0,6.28); d=r.uniform(0,.12); obox((d*math.cos(a),d*math.sin(a),.065),(.022,.008,.008),M(r.choice(['#FFF6D8','#F28A1A','#F4F1EA']),.6),0,e,rot=(0,0,a))
    if aloo: oico((.02,-.02,.1),.07,M('#E0B45A',.6),e,sc=(1.2,1,.85),sub=1)
    return e
def smog_view():
    """looking toward Lahore through the smog: only the tip of the minar and a welcome sign survive"""
    B.box((0,40,-.05),(200,120,.05),M('#8A8A80',.95),0); B.done('g')
    minar(0,60,2.6,col='#B8B4AA'); sign('WELCOME TO LAHORE',(-9,34,3.0),.9,'#D8D8D0','#6E7A70',n=(0,-1,0),pad=.3,th=.12)
    for sx in (-12.5,-5.5): B.box((sx,34.1,1.2),(.12,.12,1.2),M('#6E7378',.6),0)
    for i in range(7): B.box((-40+i*13,48+(i%3)*6,3+(i%4)),(3.2+(i%3),3,3+(i%4)),M('#8E8E88',.9),0)
    B.done('city')
    for k in range(7):
        m=M('#B4B4A8',.9,alpha=.34); B.box((0,10+k*6.5,9),(120,.02,14),m,0)
    B.done('smog')
    S,w,rp,bg=setup_render('ash',res=PCT,samples=SAMPLES,shadow_dist=60); return S
