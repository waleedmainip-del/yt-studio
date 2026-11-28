# World part 2 for "India vs Pakistan": mohalla street (dusk / night, Lahore or Delhi flavour), shaadi tent, cricket ground.
MOODS['ip_dusk']=dict(sun=(72,-135),e=2.4,col=(1,.74,.5),top='#3E6AC0',bot='#FFC08A',sky=.9,mist='#E8C0A0',cloud='#FFD0B0',cov=.45,cstr=.85)
MOODS['ip_night']=dict(sun=(58,-150),e=.6,col=(.6,.7,1.0),top='#060A1E',bot='#1C2850',sky=.6,mist='#161E3A',cloud='#232C52',cov=.4,cstr=.6)
MOODS['ip_dark']=dict(sun=(58,-150),e=.8,col=(.55,.66,1.0),top='#04061A',bot='#141C40',sky=.5,mist='#10162E',cloud='#1A2244',cov=.4,cstr=.5)
SY=5.4      # building line (half street width); road half width 3.4
MSIGN=dict(P=[('BUTT KARAHI','#B8323A'),('AL-MADINA CLOTH','#1E6A3A'),('LAHORI CHAI','#8A4A1E'),('KHAN MOBILE','#1E4A7A'),('SHAHI NAAN','#7A1F2E'),('CHAUDHRY STORE','#2F6B4F'),('PAAN SHOP','#5A2A7A'),('GOGA TAILORS','#27365A')],
           I=[('SHARMA SWEETS','#B8323A'),('GUPTA ELECTRONICS','#1E4A7A'),('DELHI CHAAT','#C8662C'),('RAJU PAAN','#5A2A7A'),('VERMA TAILORS','#27365A'),('CHAI POINT','#8A4A1E'),('MEHRA MEDICAL','#1E6A3A'),('NEW BOOK DEPOT','#7A1F2E')])
MCOL=dict(P=['#E8D2A0','#D9B08A','#CFE0C8','#E6C9B0','#C8D4D8','#E2C48A'],I=['#E8C8B0','#C9D8E8','#F0D890','#D8B8C8','#D0E0C0','#E0C0A0'])
def bldg(cx,w,fl,col,s,seed,sg,night,pw=True,note=None,balcony=False,nosign=False):
    """shop-house: shuttered shop + sign, upper floors with windows, roof clutter. front at y=s*SY. returns dict(roof=z, balc=(x,y,z))"""
    r=random.Random(seed); y0=s*SY; G=3.7; fh=3.1; H=G+fl*fh; dep=9.0; yc=y0+s*dep/2; wall=M(col,.85,kind='wall'); tr=M('#F2EBDA',.8); on_=night and pw
    B.box((cx,yc,H/2),(w/2-.04,dep/2,H/2),wall,0)
    shc=r.choice(['#8A8E96','#5A7FB0','#6A8A5A','#8A5A4A','#7A6A9A','#B8A070']); B.box((cx,y0-s*.05,1.5),(w/2-.55,.05,1.5),M(shc,.5,metal=.4),0)
    for j in range(8): B.box((cx,y0-s*.11,.28+j*.38),(w/2-.55,.02,.025),M(shade(shc,.6),.5),0)
    B.box((cx,y0-s*.13,.13),(.1,.04,.08),M('#C9A24A',.3,metal=.8),.01)
    for q in (-1,1): B.box((cx+q*(w/2-.3),y0-s*.1,1.65),(.22,.12,1.65),tr,.02)
    B.box((cx,y0-s*.1,3.15),(w/2-.08,.14,.1),tr,.02)
    if sg and not nosign: sign(sg[0],(cx,y0-s*.3,3.62),.3 if len(sg[0])<12 else .24,'#FFF6D8',sg[1],n=(0,-s,0),e=2.4 if on_ else 0,pad=.13,th=.1,frame='#E6B53A')
    if note:
        B.box((cx,y0-s*.135,1.75),(.8,.006,.32),M('#FBF8EE',.7),0); text(note[0],(cx,y0-s*.15,1.87),(0,-s,0),.14,M('#16171C',.5),ex=.004); text(note[1],(cx,y0-s*.15,1.62),(0,-s,0),.14,M('#B8232E',.5),ex=.004)
    ac=r.choice(['#C8372D','#2B58C9','#1E6A3A','#D9811A','#7448C2']); n_=max(4,int(w//1.2))
    for j in range(n_): B.box((cx-w/2+.3+(j+.5)*(w-.6)/n_,y0-s*.75,4.15),((w-.6)/n_/2,.6,.02),M(ac if j%2 else '#F4F1EA',.85,kind='fabric'),.004,rot=(R(-14*s),0,0))
    out=dict(roof=H,x=cx,y=y0+s*1.3)
    for f in range(fl):
        z=G+f*fh+1.75; n=max(2,int(w//2.4))
        for k in range(n):
            x=cx-w/2+(k+.5)*w/n; lit_=on_ and r.random()<.62
            B.box((x,y0-s*.03,z),(.52,.05,.72),lit(r.choice(['#FFD890','#FFE8B8','#BFE0FF']),4.5,always=True) if lit_ else M('#1E2844' if night else '#6A86A8',.3,spec=.8),0)
            B.box((x,y0-s*.08,z-.78),(.62,.09,.05),tr,.01); B.box((x,y0-s*.08,z+.78),(.62,.07,.05),tr,.01); B.box((x,y0-s*.07,z),(.03,.03,.72),tr,0)
            if r.random()<.35: B.box((x+.3,y0-s*.3,z-1.1),(.3,.22,.2),M('#C9CED8',.5,metal=.3),.03)
        if f==0 and balcony:
            bz=G+.08; B.box((cx,y0-s*.75,bz-.08),(1.9,.75,.08),M(shade(col,.85),.8),.02)
            for k in range(9): B.box((cx-1.8+k*.45,y0-s*1.44,bz+.5),(.03,.03,.5),M('#22242B',.4,metal=.6),0)
            B.box((cx,y0-s*1.44,bz+1.02),(1.9,.05,.04),M('#22242B',.4,metal=.6),0)
            B.box((cx,y0-s*.02,bz+1.25),(.75,.07,1.25),lit('#FFD890',3.5,always=True) if on_ else M('#10162A',.5),0)
            out['balc']=(cx,y0-s*.72,bz)
    B.box((cx,y0+s*.12,H+.28),(w/2,.12,.28),wall,0); B.box((cx,y0+s*.12,H+.58),(w/2+.05,.16,.04),tr,0)
    k=r.random()
    if k<.5: B.cyl((cx+r.uniform(-1,1),y0+s*3.2,H+1.0),.62,1.5,M(r.choice(['#2B58C9','#16171C','#3A6A9A']),.5),seg=12); B.box((cx,y0+s*3.2,H+.2),(.8,.8,.2),M('#8A8E96',.6),0)
    else: B.cyl((cx+r.uniform(-1,1),y0+s*2.6,H+.55),.5,.06,M('#C9CED8',.4,metal=.6),rot=(R(55*s),0,0),seg=14); B.cyl((cx,y0+s*2.6,H+.3),.04,.6,M('#6E7378',.5),seg=6)
    return out
def mohalla(side='P',night=False,pw=True,seed=3,note_at=None,hero=None,veh=True,lamps=True,balcs=False,nopole=None):
    """street along x, camera looks down +x. hero = index of the +y building that gets the balcony. returns dict(blds=[(s,info)],...)"""
    NIGHT[0]=1.0 if night else 0.0; r=random.Random(seed); S=setup_world(('ip_night' if pw else 'ip_dark') if night else 'ip_dusk',shadow=60)
    B.box((20,0,-.3),(140,140,.2),M('#55524C',.9,kind='concrete',sc=.4),0); B.box((20,0,-.03),(70,3.4,.03),M('#3A3B40',.85,kind='concrete',sc=.5),0)
    for s in (-1,1): B.box((20,s*4.4,.06),(70,1.0,.07),M('#A8A294',.8,kind='tile',sc=1.2),.0); B.box((20,s*3.42,.05),(70,.06,.06),M('#D8D2C0',.7),0)
    for k in range(34): B.box((-46+k*4.0,0,.004),(.9,.06,.004),M('#E8E2C8',.5),0)
    out=dict(blds=[],side=side); sg=MSIGN[side]; cols=MCOL[side]; si=0
    for s in (1,-1):
        x=-34.0; i=0
        while x<70:
            w=r.uniform(6.2,8.6); fl=r.randint(2,4); hero_=(s==1 and hero is not None and i==hero)
            info=bldg(x+w/2,w,3 if hero_ else fl,cols[(si+i)%len(cols)],s,seed*50+si,sg[si%len(sg)],night,pw,note=(note_at[1] if (note_at and note_at[0]==(s,i)) else None),balcony=hero_ or balcs,nosign=hero_ or balcs)
            out['blds'].append((s,i,info)); x+=w; i+=1; si+=1
    # poles, wires, bunting across the street, lamps
    bc=PAL[side]['bunt']
    for k,x in enumerate(range(-22,60,9)):
        bunting((x,-SY+.3,7.4+.5*(k%2)),(x,SY-.3,7.2+.5*((k+1)%2)),13,bc,sag=1.1)
        if lamps and k%2==0: street_lamp(x+4,(-1 if k%4==0 else 1)*4.9,h=7.5,arms=((1,) if k%4==0 else (-1,)))
    for s in (-1,1):
        for x in range(-30,66,16):
            if nopole and s==1 and nopole[0]<x+3*s<nopole[1]: continue
            pole(x+3*s,s*4.75,h=8.2)
        wires(-34,66,s*4.75,s*4.75,7.6,3,seed+s)
    if night and pw:
        for x in range(-18,60,9): bulb_string((x+4.5,-SY+.3,6.6),(x+4.5,SY-.3,6.6),14,1.0,['#FFD890','#FF8A6A','#8AD0FF','#9AE89A'],4.0,r_=.07)
    # far skyline
    for s in (1,-1):
        x=-60
        while x<110:
            w=r.uniform(9,16); h=r.uniform(16,34); B.box((x+w/2,s*(SY+16+r.uniform(0,10)),h/2),(w/2,5,h/2),M(r.choice(['#2A3048','#343A54','#3E4460']) if night else r.choice(['#C9B8A8','#D9C4A8','#B8C4CC']),.8),0); x+=w+r.uniform(0,3)
    B.box((75,0,12),(1,30,12),M('#2A3048' if night else '#C9B8A8',.8),0)
    B.done('mohalla')
    if veh:
        out['rick']=rickshaw((6.5,-2.2,0),196,'#2E8A3A' if side=='P' else '#E8B23A'); motorbike((-2.5,2.75,0),90,'#C8372D'); motorbike((14,2.8,0),84,'#2B58C9'); car((24,-2.3,0),180,'#C9CED8',seed=4)
        motorbike((30,2.8,0),95,'#16171C')
    return out
# ---------------------------------------------------------------- shaadi tent
MOODS['ip_shaadi']=dict(sun=(60,-160),e=.5,col=(.62,.7,1.0),top='#080A22',bot='#222A56',sky=.55,mist='#1A1E3C',cloud='#262E56',cov=.4,cstr=.6)
STG=.5      # stage height
def shaadi():
    """wedding tent open toward -y. stage at y 3.2..6.4 (top STG). backstage behind the flower wall (y>7)."""
    NIGHT[0]=1.0; S=setup_world('ip_shaadi',shadow=50); r=random.Random(11)
    B.box((0,0,-.3),(80,80,.2),M('#3A4A3A',.9,kind='concrete',sc=.4),0); B.box((0,1,-.02),(7.6,12.5,.03),M('#8A1F2E',.9,kind='fabric',sc=.8),0)
    B.box((0,-2.5,.005),(.9,6.0,.012),M('#E6B53A',.85,kind='fabric'),0)
    B.box((0,4.8,STG/2),(5.2,1.6,STG/2),M('#F4E9C8',.7),.03); B.box((0,3.1,STG/4),(1.6,.25,STG/4),M('#E6D9BC',.7),.02)
    # flower wall
    B.box((0,6.55,2.4),(5.2,.12,2.4),M('#F6EEDC',.85,kind='fabric'),0)
    fc=['#E8554D','#F2A0B8','#FFD23F','#F4F1EA','#F28A3A','#D96C8A']
    for i in range(27):
        for j in range(11):
            if (i*7+j*3)%5==0: continue
            B.ico((-5.0+i*.385,6.4,.75+j*.42),.17+.04*((i+j)%3),M(fc[(i*3+j*5+(i//4))%len(fc)],.8),sub=1)
    for s in (-1,1):
        B.box((s*5.35,6.5,2.6),(.14,.14,2.6),M('#E6B53A',.4,metal=.6),.02)
        for k in range(6): B.box((s*(4.2-k*.12),6.3,4.6-k*.55),(.9,.03,.3),M('#B8232E' if k%2 else '#E6B53A',.85,kind='fabric'),.01)
    # thrones on the stage (seat top STG+.58)
    for x in (-1.15,1.15):
        B.box((x,5.1,STG+.3),(.8,.5,.28),M('#7A1F2E',.8,kind='fabric'),.05); B.box((x,5.1,STG+.52),(.76,.46,.06),M('#B8232E',.8,kind='fabric'),.04)
        B.box((x,5.62,STG+1.15),(.8,.1,.85),M('#7A1F2E',.8,kind='fabric'),.06); B.box((x,5.56,STG+2.05),(.5,.08,.16),M('#E6B53A',.35,metal=.8),.04)
        for q in (-1,1): B.box((x+q*.86,5.1,STG+.55),(.09,.5,.42),M('#E6B53A',.35,metal=.8),.03)
    # tent: poles, striped canopy, light strings
    for sx in (-1,1):
        for y in (-10,-4.5,1,6.6): B.cyl((sx*7.4,y,3.4),.09,6.8,M('#D8D2C4',.5),seg=8)
    for k in range(16): B.box((-7.0+k*.933+.2,-1.7,6.85+.25*math.sin(k*.42)),(.47,8.9,.02),M('#E8B23A' if k%2 else '#B8232E',.85,kind='fabric'),0)
    for y in (-8,-5,-2,1): bulb_string((-7.3,y,6.3),(7.3,y,6.3),22,1.3,['#FFE0A0','#FFD070'],5.0,r_=.075)
    for sx in (-1,1):
        bulb_string((sx*7.3,-10,5.2),(sx*7.3,6.5,5.2),24,.5,['#FFE0A0'],5.0,r_=.075)
        for k in range(12): B.box((sx*7.5,-9+k*1.95,2.6),(.04,.92,2.6),M('#F2E3C4' if k%2 else '#E8B23A',.85,kind='fabric'),0)
    B.box((0,13.6,3.2),(7.6,.06,3.2),M('#F2E3C4',.85,kind='fabric'),0)
    for k in range(16): B.box((-7.0+k*.933+.2,10.2,6.6),(.47,3.4,.02),M('#E8B23A' if k%2 else '#B8232E',.85,kind='fabric'),0)
    # backstage clutter
    for x,y in ((-5.6,7.9),(-5.4,10.0)): deg(x,y,s=.8,lid=True,fire=False)
    for k in range(3): B.box((5.6,8.0,.3+k*.6),(.6,.45,.29),M(['#8A5A36','#7A4E2A','#9A6A40'][k],.7,kind='wood'),.02)
    bulb_string((-7.3,7.2,5.0),(7.3,7.2,5.0),22,.9,['#FFE0A0','#FFD070'],5.0,r_=.075)
    for x in (-4,-1.3,1.3,4): B.box((x,6.72,2.4),(.06,.06,2.4),M('#6B4A2E',.7,kind='wood'),0)
    B.box((0,6.72,3.6),(5.2,.05,.06),M('#6B4A2E',.7,kind='wood'),0); B.box((0,6.72,1.4),(5.2,.05,.06),M('#6B4A2E',.7,kind='wood'),0)
    B.done('shaadi')
    point((0,3.5,5.6),900,(1,.9,.72),r=1.5,shadow=True); point((0,-4,5.8),520,(1,.88,.7),r=2.0,shadow=False); point((0,10.6,3.6),420,(1,.86,.66),r=1.0,shadow=False)
    return dict()
SEATS_G=[(-4.2,-1.2),(-2.1,-1.2),(2.1,-1.2),(4.2,-1.2),(-4.2,-3.6),(-2.1,-3.6),(2.1,-3.6),(4.2,-3.6)]
# ---------------------------------------------------------------- cricket ground (what the TV shows)
MOODS['ip_ground']=dict(sun=(50,-170),e=.9,col=(.75,.82,1.0),top='#060A22',bot='#2A3A78',sky=.6,mist='#141C3A',cloud='#1E2850',cov=.4,cstr=.6)
def ground():
    """pitch along y: batting crease at y=-10, bowler's crease at y=+10. floodlit night."""
    NIGHT[0]=1.0; S=setup_world('ip_ground',shadow=70); r=random.Random(5)
    B.box((0,0,-.3),(160,160,.2),M('#143A1E',.9),0)
    for k in range(18): B.box((0,-76+k*9,-.02+.001*(k%2)),(80,4.5,.02),M('#2E8A3E' if k%2 else '#34963F',.85),0)
    B.box((0,0,.006),(1.7,12.2,.008),M('#A8905C',.9,kind='concrete',sc=.6),0)
    for y in (-10,10):
        B.box((0,y,.016),(1.9,.03,.004),M('#F8F8F4',.6),0); B.box((0,y+(1.3 if y<0 else -1.3),.016),(1.9,.03,.004),M('#F8F8F4',.6),0)
        for sx in (-1,1): B.box((sx*1.45,y+(.65 if y<0 else -.65),.016),(.03,.68,.004),M('#F8F8F4',.6),0)
    # 30-yard dots, boundary rope + boards, stands with crowd confetti, floodlights
    for k in range(40): a=k*2*pi/40; B.cyl((30*math.cos(a),30*math.sin(a),.02),.12,.02,M('#F8F8F4',.6),seg=6)
    for k in range(120):
        a=k*2*pi/120; x=62*math.cos(a); y=62*math.sin(a); B.box((x,y,.12),(1.7,.12,.12),M('#F4F1EA',.7),.02,rot=(0,0,a+pi/2))
        B.box((66*math.cos(a),66*math.sin(a),.6),(1.8,.08,.6),lit(['#1E4A7A','#B8323A','#E6B53A','#1E6A3A','#7448C2','#F28A3A'][k%6],1.4,always=True),0,rot=(0,0,a+pi/2))
    cc=['#E8554D','#4D8FE8','#F2C14E','#6FC38A','#F4F1DE','#9B6FD0','#FF8A3A','#2A2C34','#D8A0B8']
    for k in range(60):
        a=k*2*pi/60; ca=math.cos(a); sa=math.sin(a)
        for j in range(7):
            rr=70+j*2.6; z=1.6+j*1.75; B.box((rr*ca,rr*sa,z-.6),(3.9,1.3,.9),M('#3A3F52',.8),0,rot=(0,0,a+pi/2))
            for q in range(7): B.box(((rr-.2)*ca-sa*(q-3)*1.05,(rr-.2)*sa+ca*(q-3)*1.05,z+.75),(.42,.3,.42),M(cc[(k*5+j*3+q*7)%len(cc)],.8),.04,rot=(0,0,a+pi/2))
        B.box((90*ca,90*sa,9),(4.8,1.0,9),M('#2A2E40',.8),0,rot=(0,0,a+pi/2))
    for a in (38,142,218,322):
        x=96*math.cos(R(a)); y=96*math.sin(R(a)); B.cyl((x,y,19),.7,38,M('#6E7378',.5,metal=.5),seg=8); B.box((x*.985,y*.985,39),(5.5,.5,3.2),lit('#FFF6DC',11,always=True),0,rot=(0,0,R(a)+pi/2))
    B.done('ground')
    for a in (38,142,218,322): point((60*math.cos(R(a)),60*math.sin(R(a)),30),90000,(1,.97,.9),r=4,shadow=False)
    point((0,0,26),14000,(1,.97,.92),r=6,shadow=True)
    return dict()
