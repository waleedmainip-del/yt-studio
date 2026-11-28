# Kit for the Islamabad vampire film: cape + fangs + collar, monkey, werewolf bits, hero mask, pirate hat, bats, lanyard.
def cape(H,out='#15161C',inn='#B8232E',w=1.12,n=3,collar=True,ln=3.3):
    """cape hung from the shoulders: n hinged panels (cape_flap makes it move). H['cape'] is its root (scale to 0 to remove it)"""
    u=H['u']; e=empty((0,.56*u,3.98*u),H['root']); P=[]; par=e; L_=ln*u/n; mo=M(out,.8,kind='fabric'); mi=M(inn,.75,kind='fabric')
    for i in range(n):
        p=empty((0,0,0) if i==0 else (0,0,-L_),par); ww=(w+.13*i)*u
        obox((0,.014,-L_/2),(ww,.014,L_/2+.012),mo,.006,p); obox((0,-.006,-L_/2),(ww-.03*u,.008,L_/2+.004),mi,.004,p)
        P.append(p); par=p
    for s in (-1,1): obox((s*.72*u,-.5*u,.06*u),(.3*u,.56*u,.05*u),mo,.03*u,e)                    # shoulder straps
    if collar:
        obox((0,.12*u,.5*u),(.6*u,.035*u,.56*u),mo,.03*u,e); obox((0,.08*u,.5*u),(.55*u,.012,.5*u),mi,.01,e)
        for s in (-1,1): obox((s*.84*u,-.16*u,.46*u),(.035*u,.34*u,.5*u),mo,.03*u,e,rot=(0,0,R(s*20))); obox((s*.8*u,-.16*u,.46*u),(.012,.3*u,.45*u),mi,.01,e,rot=(0,0,R(s*20)))
    H['cape']=e; H['capeP']=P; return e
def cape_flap(H,t,a=5,amp=6,w=3.0,k=1.0):
    for i,p in enumerate(H['capeP']): p.rotation_euler[0]=R(((a if i==0 else a*.5)+amp*(1+.4*i)*math.sin(t*w-i*.9))*k)
def cape_off(H): H['cape'].scale=(0,0,0)
def fangs(H):
    u=H['u']; fy=-.62*u-.004; H['fangs']=[obox((s*.11*u,fy,.2*u),(.036*u,.008,.075*u),M('#FFFFFF',.3,emit=.15),.004,H['head']) for s in (-1,1)]
def vamp(x,y,rz,name='drac',C=None,cap=True):
    H=mk(C or DRAC,x,y,rz,name); u=H['u']; fangs(H)
    obox((0,-.6*u,1.08*u),(.16*u,.05*u,.16*u),M('#0B0B10',.6),.02*u,H['head'],rot=(0,R(45),0))                    # widow's peak
    for s in (-1,1): obox((s*.66*u,-.1*u,.78*u),(.03*u,.1*u,.12*u),M((C or DRAC)['skin'],.55),.03*u,H['head'],rot=(R(-20),0,0))     # pointed ears
    if cap: cape(H)
    return H
def lanyard(H):
    u=H['u']; fr=-.5*u; bl=M('#1E6A3A',.7)
    for s in (-1,1): obox((s*.2*u,fr-.03,3.5*u),(.035*u,.008,.5*u),bl,.003,H['root'],rot=(0,R(s*22),0))
    obox((0,fr-.04,2.92*u),(.17*u,.01,.22*u),M('#F4F1EA',.5),.01,H['root']); obox((0,fr-.05,3.05*u),(.17*u,.006,.06*u),M('#1E6A3A',.5),.004,H['root']); obox((0,fr-.05,2.9*u),(.07*u,.006,.08*u),M('#C9D2E8',.5),.004,H['root'])
def mask(H,col='#16909E'):
    u=H['u']; fy=-.62*u; obox((0,fy+.001,.67*u),(.6*u,.004,.16*u),M(col,.6),.002,H['head'])
def pirate_hat(H):
    u=H['u']; fy=-.62*u; bk=M('#1B1B22',.7); hd=H['head']
    obox((0,0,1.27*u),(.9*u,.82*u,.06*u),bk,.03*u,hd); obox((0,0,1.5*u),(.56*u,.52*u,.2*u),bk,.08*u,hd); obox((0,-.74*u,1.5*u),(.62*u,.05*u,.26*u),bk,.04*u,hd)
    obox((0,-.8*u,1.5*u),(.12*u,.012,.1*u),M('#F4F1EA',.5),.03*u,hd); obox((0,-.8*u,1.36*u),(.2*u,.012,.03*u),M('#F4F1EA',.5),.004,hd)
    obox((-.25*u,fy-.008,.66*u),(.16*u,.006,.14*u),bk,.03*u,hd); obox((0,fy-.003,.84*u),(.63*u,.004,.022*u),bk,.002,hd,rot=(0,R(-10),0))
def wolfify(H):
    u=H['u']; fy=-.62*u; hd=H['head']; fur=M(H['C']['skin'],.9); dk=M('#2A1A10',.7)
    for s in (-1,1): obox((s*.42*u,.05*u,1.32*u),(.15*u,.08*u,.24*u),fur,.06*u,hd,rot=(0,R(s*14),0)); obox((s*.42*u,-.03*u,1.3*u),(.075*u,.02,.14*u),M('#D9A08A',.7),.02*u,hd,rot=(0,R(s*14),0))
    obox((0,fy-.2*u,.34*u),(.27*u,.24*u,.19*u),fur,.07*u,hd); obox((0,fy-.44*u,.44*u),(.1*u,.04*u,.07*u),dk,.03*u,hd)
    for s in (-1,1): obox((s*.15*u,fy-.38*u,.13*u),(.03*u,.025*u,.07*u),M('#FFFFFF',.3),.004,hd)
    for s in (-1,1): obox((s*.66*u,0,.35*u),(.07*u,.3*u,.3*u),fur,.06*u,hd)
def bat(loc=(0,0,-50),s=1.0):
    e=empty(loc); e.scale=(s,)*3; dm=M('#14141C',.6); oico((0,0,0),.11,dm,e,sc=(1,1.2,.9),sub=1); W=[]
    for sx in (1,-1):
        w=empty((sx*.08,0,0),e); obox((sx*.3,0,0),(.3,.13,.012),dm,.004,w); obox((sx*.52,-.06,0),(.1,.08,.012),dm,.004,w); W.append((w,sx))
    for sx in (-1,1): obox((sx*.05,-.08,.1),(.02,.02,.045),dm,.01,e)
    return dict(root=e,w=W)
def bat_fly(Bt,t,p,rz=0,ph=0.0):
    Bt['root'].location=p; Bt['root'].rotation_euler=(0,0,R(rz))
    for w,sx in Bt['w']: w.rotation_euler[1]=-sx*R(38*math.sin(t*22+ph))
# ---------------------------------------------------------------- monkey
def monkey(loc=(0,0,0),rz=0,s=1.0,caped=False):
    root=empty(loc,rot=(0,0,R(rz))); root.scale=(s,)*3; br=M('#8A6238',.88); bd=M('#6E4C2A',.88); fc_=M('#E8C9A0',.7); bk=M('#141418',.4)
    body=empty((0,0,.5),root); obox((0,0,.12),(.25,.2,.3),br,.1,body); obox((0,-.19,.1),(.16,.03,.2),fc_,.03,body)
    hd=empty((0,-.04,.5),body); obox((0,0,.2),(.24,.22,.21),br,.09,hd); obox((0,-.21,.16),(.17,.03,.15),fc_,.05,hd); obox((0,-.25,.08),(.1,.04,.07),fc_,.03,hd)
    for sx in (-1,1): oico((sx*.08,-.245,.22),.036,bk,hd,sub=1); oico((sx*.086,-.272,.236),.012,M('#FFFFFF',.3,emit=.6),hd,sub=1); obox((sx*.27,0,.22),(.05,.03,.08),fc_,.03,hd)
    obox((0,-.296,.06),(.05,.008,.012),bk,.002,hd); ARM={}; LEG={}
    for sx in (1,-1):
        a=empty((sx*.31,0,.36),body); obox((0,0,-.22),(.07,.07,.24),br,.04,a); obox((0,0,-.48),(.08,.08,.06),bd,.03,a); ARM[sx]=a
        l=empty((sx*.14,0,-.16),body); obox((0,0,-.14),(.085,.085,.16),br,.04,l); obox((0,-.06,-.31),(.09,.14,.04),bd,.03,l); LEG[sx]=l
    T=[]; par=body; p0=(0,.2,-.1)
    for i in range(4): e=empty(p0,par); obox((0,.11,0),(.04,.12,.04),br,.02,e); T.append(e); par=e; p0=(0,.22,0)
    cp=empty((0,.215,.42),body); obox((0,.02,-.3),(.3,.012,.32),M('#15161C',.8,kind='fabric'),.006,cp); obox((0,.0,-.3),(.28,.008,.3),M('#B8232E',.75,kind='fabric'),.004,cp)
    obox((0,-.21,.0),(.27,.23,.03),M('#15161C',.8,kind='fabric'),.02,cp); obox((0,.03,.18),(.26,.02,.2),M('#15161C',.8,kind='fabric'),.02,cp); obox((0,.01,.18),(.23,.01,.17),M('#B8232E',.75),.01,cp)
    Mk=dict(root=root,body=body,head=hd,arm=ARM,leg=LEG,tail=T,cape=cp,s=s)
    if not caped: cp.scale=(0,0,0)
    monkey_pose(Mk,0); return Mk
def monkey_pose(Mk,t,mode='sit',arm=None,look=(0,0),ph=0.0):
    """sit | stand | run. arm = {side: degrees forward-up}. look = (yaw, pitch) of the head"""
    b=Mk['body']; A=Mk['arm']; Lg=Mk['leg']
    if mode=='sit':
        b.location[2]=.2+.008*math.sin(t*3+ph); b.rotation_euler[0]=R(-6)
        for sx in (1,-1): Lg[sx].rotation_euler=(R(-84),0,R(sx*14)); A[sx].rotation_euler=(R(-28),0,R(-sx*6))
    elif mode=='stand':
        b.location[2]=.5+.008*math.sin(t*3+ph); b.rotation_euler[0]=0
        for sx in (1,-1): Lg[sx].rotation_euler=(0,0,0); A[sx].rotation_euler=(R(-8),0,R(-sx*10))
    else:
        w=t*15+ph; b.location[2]=.44+.07*abs(math.sin(w)); b.rotation_euler[0]=R(38)
        for sx in (1,-1): Lg[sx].rotation_euler=(R(-38+42*math.sin(w+(0 if sx>0 else pi))),0,0); A[sx].rotation_euler=(R(-70+40*math.sin(w+(pi if sx>0 else 0))),0,0)
    for sx,v in (arm or {}).items(): A[sx].rotation_euler=(R(-v),0,R(-sx*8))
    Mk['head'].rotation_euler=(R(-look[1])-(b.rotation_euler[0] if mode=='run' else 0),0,R(look[0]))
    for i,e in enumerate(Mk['tail']): e.rotation_euler=(R(-36-8*math.sin(t*2.2+i+ph)),0,R(6*math.sin(t*1.7+i)))
