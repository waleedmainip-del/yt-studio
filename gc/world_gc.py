# Set for "Gali Cricket Ke Qanoon": a narrow residential gali at asr time, brick wicket, overhead wires, and Razia Khala's green gate.
# Gali runs along x. House fronts at y=+-GY. Wicket at (0,0); bowler runs in from +x. Razia Khala's gate at (RX, GY).
GY=3.3
RX=17.5
WIRE_X=4.2; WIRE_Z=5.3
HOUSE_COLS=['#E8D8B8','#D8C4A0','#C9D6D8','#E6C8B0','#D0C8E0','#B8D0C0','#E0D0C0','#F0E0C8']
def house(cx,w,floors,col,side,seed,door=True):
    r=random.Random(seed); s=side; yf=s*GY; d=5.0; H=floors*3.0+.4; yc=yf+s*d/2
    wm=M(col,.85,kind='wall',sc=.7); trim=M(shade(col,.82),.8); grill=M('#2A2C34',.4,metal=.6)
    B.box((cx,yc,H/2),(w/2,d/2,H/2),wm,0)
    B.box((cx,yf+s*.02,.35),(w/2,.04,.35),M(shade(col,.7),.9,kind='concrete'),0)                  # damp plinth
    for f in range(floors):
        zb=f*3.0
        if f==0 and door:
            dx=cx+r.uniform(-w/4,w/4); B.box((dx,yf-s*.03,1.2),(.62,.05,1.2),M(r.choice(['#6E4A2E','#2F5A3A','#3D5A80','#7A1F2E']),.6,kind='wood'),.02)
            B.box((dx,yf-s*.06,2.5),(.8,.06,.08),trim,.02); B.box((dx,yf-s*.1,.08),(.75,.25,.08),M('#B8A890',.85),.01)
            B.box((dx+.5,yf-s*.07,1.25),(.05,.03,.05),M('#D9B24A',.3,metal=.8),0)
            wx=cx+(w/4 if dx<cx else -w/4)
        else: wx=cx
        for q in ((wx,) if f==0 else (cx-w/4,cx+w/4)):
            B.box((q,yf-s*.03,zb+1.75),(.7,.04,.6),M('#5E7A8A',.1,spec=.9),0)
            for k in range(6): B.box((q-.6+k*.24,yf-s*.08,zb+1.75),(.018,.02,.62),grill,0)
            B.box((q,yf-s*.08,zb+1.75),(.72,.02,.018),grill,0); B.box((q,yf-s*.06,zb+2.45),(.85,.12,.06),trim,.02)
            if r.random()<.5: B.box((q+.95,yf-s*.25,zb+2.3),(.3,.22,.2),M('#E8E8E2',.5),.03)          # AC unit
        if f>0 and r.random()<.6:                                                                       # balcony with plants / washing
            B.box((cx,yf-s*.55,zb+.12),(w/2-.4,.55,.08),trim,.02)
            for k in range(int(w/.5)): B.box((cx-w/2+.6+k*.45,yf-s*1.05,zb+.6),(.02,.02,.45),grill,0)
            B.box((cx,yf-s*1.05,zb+1.05),(w/2-.4,.03,.03),grill,0)
            if r.random()<.6:
                for k in range(3): B.ico((cx-w/3+k*1.1,yf-s*.75,zb+.45),.28,M('#3F7A3A',.85,kind='leaves'),sub=1); B.cyl((cx-w/3+k*1.1,yf-s*.75,zb+.27),.16,.3,M('#B8562A',.7),seg=8)
            else:
                B.box((cx,yf-s*.9,zb+2.1),(w/2-.5,.008,.008),M('#16171C',.5),0)
                for k in range(5): B.box((cx-w/3+k*.9,yf-s*.9,zb+1.75),(.28,.01,.34),M(r.choice(['#C8372D','#2B58C9','#F2C14E','#F4F1EA','#7A1F2E']),.8,kind='fabric'),0)
    B.box((cx,yc,H+.25),(w/2+.05,d/2+.05,.25),trim,0)                                              # parapet
    if r.random()<.7: B.cyl((cx+r.uniform(-w/3,w/3),yc,H+1.0),.55,1.1,M(r.choice(['#2A2C34','#C8372D','#F2F2EE']),.5),seg=14)   # water tank
    B.box((cx+w/2-.35,yf-s*.08,1.7),(.18,.06,.25),M('#C9CED8',.4),.02); B.box((cx+w/2-.35,yf-s*.12,1.72),(.08,.01,.06),M('#16171C',.5),0)   # meter box
def razia_house():
    """compound wall + green double gate (animated leaves) + two-storey house behind a courtyard"""
    wallc=M('#C9DCC4',.85,kind='wall',sc=.7); s=1; x0,x1=RX-4.0,RX+4.0
    for a,b in ((x0,RX-1.25),(RX+1.25,x1)): B.box(((a+b)/2,GY+.12,1.45),((b-a)/2,.14,1.45),wallc,0); B.box(((a+b)/2,GY+.12,2.95),((b-a)/2+.05,.2,.08),M('#A8BCA4',.8),.01)
    for x in (RX-1.32,RX+1.32): B.box((x,GY+.12,1.6),(.12,.2,1.6),M('#A8BCA4',.8),.02)
    B.box((RX,GY+.12,3.25),(1.45,.12,.1),M('#1E5A3A',.4,metal=.5),.02)
    stext('RAZIA MANZIL',(RX,GY-.03,3.55),.2,'#1E5A3A',n=(0,-1,0))
    B.box((RX,GY+3.0,.02),(4.0,2.8,.02),M('#B8B0A0',.85,kind='tile'),0)                          # courtyard
    B.box((RX,GY+8.0,3.4),(4.6,2.0,3.4),M('#E6D8C0',.85,kind='wall'),0)
    for x in (RX-2.2,RX+2.2):
        for z in (1.8,4.8): B.box((x,GY+5.97,z),(.7,.04,.6),M('#2A3238',.2),0)
    B.box((RX,GY+5.97,1.3),(.6,.04,1.3),M('#5A3A22',.6,kind='wood'),.02)
    B.ico((RX+3.2,GY+3.5,.9),.9,M('#3F7A3A',.85,kind='leaves'),sub=1); B.cyl((RX+3.2,GY+3.5,.3),.35,.6,M('#B8562A',.7),seg=10)
    B.box((RX-3.0,GY+4.2,.55),(.6,.4,.55),M('#7A5A3A',.7,kind='wood'),.02)                          # charpai stand-in: old crate
    r=random.Random(77); cols=['#D7E84A','#F2F2EE','#C8372D','#D7E84A','#E8A23A','#3A8FD8','#E4F25A']
    for k in range(340):                                                                   # the pile: every ball that never came back
        a=r.uniform(0,2*pi); rr=1.35*math.sqrt(r.uniform(0,1)); x=RX-2.0+math.cos(a)*rr*1.15; y=GY+4.5+math.sin(a)*rr*.8
        z=.09+(1-rr/1.35)**1.3*1.15+r.uniform(-.04,.04)
        oico((x,y,z),r.uniform(.085,.1),M(r.choice(cols),.65,kind='fabric'),None,sub=1)
    for k in range(9): oico((RX+r.uniform(-3.4,3.4),GY+r.uniform(1.2,5.4),.09),.09,M(r.choice(cols),.65,kind='fabric'),None,sub=1)
    leaves=[]
    gm=M('#1E6A3A',.45,metal=.5)
    for s_ in (-1,1):
        hinge=empty((RX+s_*1.2,GY+.12,0)); leaves.append(hinge)
        obox((-s_*.6,0,1.25),(.58,.04,1.2),gm,.02,hinge)
        for k in range(5): obox((-s_*(.12+k*.24),-.05,2.5),(.02,.02,.14),gm,0,hinge)
        obox((-s_*.6,-.05,1.25),(.5,.015,.02),M('#164E2C',.5,metal=.5),0,hinge)
        obox((-s_*1.1,-.06,1.2),(.03,.03,.08),M('#D9B24A',.3,metal=.8),0,hinge)
    return leaves
def brick_mat(): return M('#A8502E',.85,kind='wall',sc=.3)
def wicket():
    """stack of bricks used as stumps; returns list of (obj, rest_loc, rest_rot)"""
    bm=brick_mat(); W=[]
    for (loc,half) in (((0,-.17,.06),(.07,.15,.06)),((0,.17,.06),(.07,.15,.06)),((0,0,.18),(.07,.32,.06)),((0,-.09,.47),(.06,.07,.23)),((0,.09,.47),(.06,.07,.23)),((0,0,.78),(.07,.15,.06))):
        o=obox(loc,half,bm,.012); W.append((o,Vector(loc),half))
    return W
def bricks_fall(W,t,t_hit,power=1.0,seed=1):
    """bricks hit at t_hit fly backwards (-x) and settle flat on the ground; before t_hit they stand stacked"""
    r=random.Random(seed)
    for i,(o,rl,half) in enumerate(W):
        if t<t_hit or i<2 and power<1.5: o.location=rl; o.rotation_euler=(0,0,0); continue
        dt=t-t_hit; vx=-(1.2+r.uniform(0,1.3))*power; vy=r.uniform(-.9,.9)*power; vz=(1.6+r.uniform(0,1.4))*power*(rl.z+.3)
        T=max(.15,(vz+math.sqrt(vz*vz+2*9.8*rl.z))/9.8); tt=min(dt,T)
        x=rl.x+vx*tt*(1+.6*min(1,max(0,dt-T))); y=rl.y+vy*tt; z=rl.z+vz*tt-4.9*tt*tt
        if dt>=T: z=half[2]; x=rl.x+vx*T+vx*.25*min(.4,dt-T)
        spin=min(dt,T)*r.uniform(6,11)
        o.location=(x,y,max(half[2] if dt>=T else 0,z)); o.rotation_euler=(spin if dt<T else round(spin/(pi/2))*(pi/2),r.uniform(-1,1)*spin*.3 if dt<T else 0,spin*.4)
BALLS=[]
def ball_obj(r_=.095):
    e=empty((0,0,0)); oico((0,0,0),r_,M('#E4F25A',.55,emit=.35,kind='fabric'),e,sub=2)
    for k in range(2): ocyl((0,0,0),r_*1.02,.045,M('#D6332A',.5,emit=.2),e,rot=(R(90*k),0,0),seg=16)        # red tape bands
    BALLS.append(e); return e
def bat_obj(parent=None):
    """tape-ball bat; local origin at the top of the handle, blade hanging along -z"""
    e=empty((0,0,0),parent); wd=M('#C8955A',.55,kind='wood',sc=.35); face_=M('#D9AE74',.5,kind='wood',sc=.35); grip=M('#1C1D22',.8)
    ocyl((0,0,-.19),.032,.38,grip,e,rot=(0,0,0),seg=10)                                   # rubber grip
    for k in range(5): ocyl((0,0,-.04-k*.075),.036,.018,M('#C8372D' if k%2 else '#F2F2EE',.6),e,rot=(0,0,0),seg=10)   # grip tape rings
    obox((0,0,-.42),(.028,.05,.06),wd,.01,e)                                              # splice
    for s_ in (1,-1): obox((0,s_*.055,-.5),(.03,.04,.035),wd,.01,e,rot=(R(-s_*28),0,0))     # sloped shoulders
    obox((0,0,-.92),(.024,.085,.44),face_,.012,e)                                          # flat face
    obox((.03,0,-.95),(.022,.035,.4),wd,.015,e)                                            # back spine
    obox((0,0,-1.37),(.024,.078,.02),wd,.015,e)                                            # toe
    for k in range(2): obox((0,0,-.62-k*.42),(.027,.088,.022),M('#C8372D',.5),0,e)          # red tape bands
    return e
def bucket_obj(parent=None):
    e=empty((0,0,0),parent); r=random.Random(40)
    ocyl((0,0,.22),.3,.46,M('#2B78C9',.5),e,rot=(0,0,0),seg=18); ocyl((0,0,.45),.31,.03,M('#1E5A9A',.5),e,rot=(0,0,0),seg=18)
    obox((0,0,.62),(.3,.012,.012),M('#C9CED8',.3,metal=.8),0,e)
    for k in range(40):
        a=r.uniform(0,2*pi); rr=r.uniform(0,.22) if k<28 else r.uniform(0,.12); z=.36+(.1 if k>=28 else 0)+r.uniform(0,.08)
        oico((math.cos(a)*rr,math.sin(a)*rr,z),.065,M('#E4F25A',.6,kind='fabric'),e,sub=1); ocyl((math.cos(a)*rr,math.sin(a)*rr,z),.067,.03,M('#D6332A',.5),e,rot=(R(r.uniform(0,180)),R(r.uniform(0,180)),0),seg=12)
    return e
def gali_k():
    r=random.Random(9)
    B.box((0,0,-.05),(80,30,.05),M('#9A938A',.9,kind='concrete',sc=.5),0)
    B.box((0,0,.004),(80,GY-.35,.004),M('#8E887E',.9,kind='concrete',h2='#A39C92',sc=1.2),0)
    for s in (1,-1): B.box((0,s*(GY-.22),.03),(80,.16,.03),M('#5E5A52',.8),0); B.box((0,s*(GY-.22),.005),(80,.11,.005),M('#3A3830',.4,spec=.6),0)  # nali
    B.box((.0,0,.006),(.9,.04,.003),M('#F4F1EA',.7),0); B.box((8.9,0,.006),(.05,.6,.003),M('#F4F1EA',.7),0)                        # chalk crease lines
    for s in (1,-1):
        x=-34
        while x<46:
            if s==1 and RX-4.05<=x<RX+4.05: x=RX+4.05; continue
            w=r.uniform(5.5,8.0)
            if s==1 and x<RX-4.0<x+w: w=RX-4.0-x
            house(x+w/2,w,r.randint(2,3),r.choice(HOUSE_COLS),s,int(x*7+s*3)); x+=w+.05
    leaves=razia_house()
    # wires: the famous taar across the gali + bundles along the houses
    for x in (WIRE_X,-9,12,27):
        z=WIRE_Z if x==WIRE_X else r.uniform(5,6.2)
        for k in range(3 if x==WIRE_X else 2): B.box((x+k*.18,0,z-k*.12),(.012,GY+.3,.012),M('#16171C',.5),0)
    for s in (1,-1): B.box((0,s*(GY-.25),5.9),(70,.015,.015),M('#16171C',.5),0); B.box((0,s*(GY-.3),5.75),(70,.015,.015),M('#16171C',.5),0)
    for x in (-14,10,30): B.cyl((x,-GY+.35,3.6),.12,7.2,M('#8A8A84',.7,kind='concrete'),seg=8); B.box((x,-GY+.35,7.0),(.08,.5,.06),M('#5A5E66',.4),.01)
    # neem tree, parked bikes, a cot, cricket kit
    for k in range(9): B.ico((-11+math.cos(k)*1.2,-GY+.7+math.sin(k)*.6,6.2+math.sin(k*2)*.7),1.2,M('#3F7A3A',.85,kind='leaves'),sub=1)
    B.cyl((-11,-GY+.6,2.8),.28,5.6,M('#6E5038',.85,kind='wood'),seg=8)
    B.done('gali')
    for x,rz in ((-6.5,8),(24,-8)): mb=motorbike((x,-GY+1.0,0),rz,r.choice(['#C8372D','#16171C'])); mb['root'].scale=(1.4,)*3
    setup_world('golden',60)
    point((6,-1.0,7.0),600,(1,.85,.62),r=2.5,shadow=False); point((RX,1.0,4.0),300,(1,.85,.65),r=1.5,shadow=False); point((0,-1,3.5),200,(1,.9,.75),r=1.2,shadow=False)
    return {'leaves':leaves}
