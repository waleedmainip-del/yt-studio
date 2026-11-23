# avatar system v3 (Roblox R6 proportions, u=.42). Adds hoodie, curly hair, helmet, vest, mustache, medals, ponytail.
def avatar(loc,rotz,C,pose=None,u=.42):
    pose=pose or {}; k=C.get('h',1.0); u=u*k
    root=empty((loc[0],loc[1],loc[2]+.008),rot=(0,0,R(rotz)))
    skin=M(C['skin'],.55,spec=.3); tee=M(C['top'],.8,kind='fabric',spec=.2); hair=M(C['hair'],.6,spec=.3)
    jk=C.get('jacket'); body=M(jk,.75,kind='fabric',spec=.2) if jk else tee; trim=M(C.get('trim',shade(jk or C['top'],.75)),.8,kind='fabric',spec=.2)
    slv=M(C.get('sleeve',jk or C['top']),.75,kind='fabric',spec=.2); pants=M(C['pants'],.85,kind='fabric',spec=.2)
    shoe=M(C.get('shoes','#22242B'),.45); acc=M(C.get('accent','#E0483A'),.5); sole=M(C.get('sole','#F0F1F5'),.6); dk=M('#1B1B22',.3)
    fr=-.5*u; X={}
    obox((0,0,3.0*u),(1.0*u,.5*u,1.0*u),body,.07*u,root)
    obox((0,0,4.06*u),(.3*u,.3*u,.1*u),skin,.03*u,root)
    if C.get('hoodie'):
        X['pocket']=(0,fr-.03,2.52*u)
        obox((0,fr-.012,2.5*u),(.62*u,.02,.3*u),trim,.012,root)
        for s in (-1,1): obox((s*.58*u,fr-.03,2.62*u),(.05*u,.012,.2*u),M(shade(C.get('trim',C['top']),.7),.8),.003,root,rot=(0,R(s*-28),0))
        obox((0,.42*u,3.95*u),(.66*u,.22*u,.16*u),trim,.08*u,root)
        obox((0,.52*u,3.75*u),(.5*u,.06*u,.3*u),trim,.06*u,root)
        for s in (-1,1):
            obox((s*.5*u,-.12*u,4.02*u),(.18*u,.42*u,.12*u),trim,.06*u,root)
            obox((s*.16*u,fr-.03,3.62*u),(.035*u,.014,.32*u),M(C.get('strings','#FFFFFF'),.6),.004,root)
            obox((s*.16*u,fr-.034,3.28*u),(.05*u,.016,.04*u),M(C.get('strings','#FFFFFF'),.4),.004,root)
        obox((0,0,2.08*u),(1.03*u,.53*u,.1*u),trim,.03*u,root)
    if jk:
        obox((0,fr-.012,3.0*u),(.2*u,.012,.97*u),tee,.004,root)
        for s in (-1,1):
            obox((s*.215*u,fr-.02,3.0*u),(.025*u,.012,.98*u),M('#C9CED8',.4,metal=.6),.003,root)
            obox((s*.62*u,fr-.016,2.5*u),(.2*u,.01,.022*u),M(shade(jk,.65),.8),.003,root,rot=(0,R(s*12),0))
            obox((s*.5*u,-.05*u,4.07*u),(.34*u,.5*u,.09*u),trim,.05*u,root)
        obox((0,.36*u,4.09*u),(.6*u,.2*u,.11*u),trim,.06*u,root)
        obox((0,0,2.1*u),(1.03*u,.53*u,.1*u),trim,.03*u,root)
    elif not C.get('hoodie'):
        obox((0,-.3*u,4.02*u),(.42*u,.24*u,.04*u),trim,.02*u,root)
    if C.get('military'):
        mp=M(shade(C['top'],.82),.85,kind='fabric')
        for s in (-1,1):
            obox((s*.48*u,fr-.02,3.45*u),(.3*u,.02,.26*u),mp,.01,root); obox((s*.48*u,fr-.03,3.66*u),(.32*u,.022,.07*u),M(shade(C['top'],.7),.8),.006,root)
            obox((s*.48*u,fr-.04,3.6*u),(.03*u,.008,.03*u),M('#B9A46A',.4,metal=.6),.002,root)
        obox((0,fr-.02,3.0*u),(.03*u,.012,.95*u),M(shade(C['top'],.72),.8),.002,root)
        for s in (-1,1): obox((s*1.02*u,0,3.97*u),(.2*u,.5*u,.05*u),M(shade(C['top'],.8),.8),.01,root)
    if C.get('vest'):
        vm=M(C['vest'],.85,kind='fabric')
        obox((0,0,3.05*u),(1.04*u,.56*u,.8*u),vm,.05*u,root)
        for x in (-.62,-.21,.21,.62): obox((x*u,fr-.09,2.75*u),(.17*u,.06,.18*u),M(shade(C['vest'],.82),.85),.02*u,root); obox((x*u,fr-.1,2.95*u),(.18*u,.065,.04*u),M(shade(C['vest'],.7),.85),.01,root)
        obox((.55*u,fr-.09,3.55*u),(.12*u,.05,.22*u),dk,.02*u,root); obox((.55*u,fr-.09,3.85*u),(.02*u,.02,.12*u),dk,.004,root)
    if C.get('medals'):
        for i,c in enumerate(C['medals']): obox(((-.65+i*.15)*u,fr-.03,3.62*u),(.06*u,.012,.05*u),M(c,.5),.003,root)
    if C.get('emblem'): obox((0,fr-.028,3.35*u),(.11*u,.006,.11*u),M(C['emblem'],.4,emit=.2),.008,root,rot=(0,R(45),0))
    if C.get('tie'): obox((0,fr-.03,3.3*u),(.07*u,.008,.55*u),M(C['tie'],.6),.004,root); obox((0,fr-.034,3.88*u),(.1*u,.01,.08*u),M(C['tie'],.6),.004,root)
    if C.get('apron'):
        obox((0,fr-.03,2.75*u),(.8*u,.012,.85*u),M(C['apron'],.8,kind='fabric'),.01,root); obox((0,fr-.045,2.6*u),(.4*u,.008,.2*u),M(shade(C['apron'],.8),.8),.006,root)
        for s in (-1,1): obox((s*.5*u,fr-.03,3.8*u),(.05*u,.012,.25*u),M(C['apron'],.8),.004,root)
    if C.get('scarf'): obox((0,0,4.08*u),(.5*u,.5*u,.14*u),M(C['scarf'],.9,kind='fabric'),.08*u,root); obox((.25*u,fr-.03,3.6*u),(.14*u,.03,.42*u),M(C['scarf'],.9,kind='fabric'),.02,root)
    if not C.get('hoodie'):
        obox((0,0,2.02*u),(1.01*u,.51*u,.06*u),M(C.get('belt','#3A2A1E'),.6),.01,root); obox((0,fr-.02,2.02*u),(.09*u,.01,.07*u),M(C.get('buckle','#D9B24A'),.3,metal=.9),.004,root)
    if C.get('bag'):
        bg=M(C['bag'],.7,kind='fabric')
        for yy in (fr-.035,.5*u+.035): obox((0,yy,3.05*u),(.07*u,.012,1.3*u),bg,.004,root,rot=(0,R(40 if yy<0 else -40),0))
        obox((-.55*u,.68*u,2.2*u),(.45*u,.17*u,.36*u),bg,.04*u,root); obox((-.55*u,.86*u,2.36*u),(.46*u,.02,.2*u),M(shade(C['bag'],.8),.7),.01,root)
    if C.get('pack'):
        pk=M(C['pack'],.7,kind='fabric'); X['pack']=obox((0,.78*u,3.05*u),(.7*u,.28*u,.8*u),pk,.1*u,root); obox((0,1.07*u,2.75*u),(.45*u,.04,.3*u),M(shade(C['pack'],.8),.7),.02,root)
        for s in (-1,1): obox((s*.6*u,fr-.02,3.3*u),(.09*u,.012,.7*u),pk,.004,root)
    if C.get('radio'):
        obox((0,.62*u,3.1*u),(.45*u,.14*u,.55*u),M('#3E4A2C',.8),.03*u,root); obox((.3*u,.62*u,3.85*u),(.02*u,.02*u,.35*u),dk,.004,root)
    ARM={};LEG={}
    for s in (-1,1):
        P=empty((s*1.02*u,0,3.9*u),root,rot=(R(pose.get('arm_x%+d'%s,0)),R(pose.get('arm_y%+d'%s,0)),0)); ARM[s]=P
        sl=C.get('short',False)
        obox((s*.5*u,0,(-.35 if sl else -.7)*u),(.5*u,.5*u,(.45 if sl else .8)*u),slv,.06*u,P)
        if sl: obox((s*.5*u,0,-1.2*u),(.46*u,.46*u,.4*u),skin,.05*u,P)
        else: obox((s*.5*u,0,-1.55*u),(.52*u,.52*u,.09*u),trim,.04*u,P)
        if C.get('gloves'): obox((s*.5*u,0,-1.8*u),(.48*u,.48*u,.21*u),M(C['gloves'],.7),.07*u,P)
        else: obox((s*.5*u,0,-1.8*u),(.46*u,.46*u,.2*u),skin,.07*u,P)
        if C.get('watch') and s==1: obox((s*.5*u,0,-1.42*u),(.535*u,.535*u,.05*u),dk,.01,P)
        Lg=empty((s*.5*u,0,2.0*u),root,rot=(R(pose.get('leg_x%+d'%s,0)),0,0)); LEG[s]=Lg
        obox((0,0,-.85*u),(.49*u,.5*u,.85*u),pants,.05*u,Lg)
        if C.get('cuff'): obox((0,0,-1.6*u),(.51*u,.52*u,.09*u),M(shade(C['pants'],1.35),.85,kind='fabric'),.02*u,Lg)
        if C.get('stripe'): obox((s*.495*u,0,-.85*u),(.01,.08*u,.8*u),M(C['stripe'],.6),.002,Lg)
        if C.get('cargo'): obox((s*.5*u,-.05*u,-.95*u),(.02,.3*u,.22*u),M(shade(C['pants'],.8),.85),.005,Lg)
        if C.get('boots'):
            obox((0,-.06*u,-1.6*u),(.52*u,.58*u,.36*u),M(C['boots'],.6),.06*u,Lg); obox((0,-.06*u,-1.965*u),(.53*u,.6*u,.04*u),M('#1B1B22',.7),.02*u,Lg)
        else:
            obox((0,-.08*u,-1.82*u),(.5*u,.6*u,.14*u),shoe,.06*u,Lg); obox((0,-.08*u,-1.965*u),(.52*u,.62*u,.04*u),sole,.02*u,Lg)
            obox((0,-.1*u,-1.82*u),(.51*u,.2*u,.05*u),acc,.01,Lg); obox((0,-.6*u,-1.86*u),(.42*u,.09*u,.1*u),sole,.03*u,Lg)
    Hd=empty((0,0,4.15*u),root,rot=(R(pose.get('head_x',0)),R(pose.get('head_y',0)),R(pose.get('head_z',0))))
    obox((0,0,.6*u),(.62*u,.62*u,.6*u),skin,.13*u,Hd); hb=.06*u; hs=C.get('hairstyle','fringe')
    def H(c,s_,rot=(0,0,0),m=hair,bv=None): obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,hb if bv is None else bv*u,Hd,rot=rot)
    if hs not in ('bald','helmet'): H((0,.03,1.2),(.67,.67,.15)); H((0,.53,.75),(.67,.18,.48))
    if hs=='quiff':
        for s in (-1,1): H((s*.62,.15,.95),(.07,.5,.26))
        H((0,-.42,1.36),(.56,.3,.17),(R(-14),0,0)); H((-.08,-.56,1.5),(.42,.22,.13),(R(-24),0,R(6))); H((.1,-.2,1.42),(.46,.3,.1),(R(-6),0,R(-5))); H((0,-.63,1.14),(.6,.07,.09))
    elif hs=='fringe':
        for s in (-1,1): H((s*.61,.2,.86),(.1,.44,.36))
        for x,dp,ry in zip([-.52,-.27,-.02,.24,.5],[.2,.27,.18,.24,.13],[10,6,-4,-8,-14]): H((x,-.6,1.14-dp/2),(.15,.11,dp/2+.1),(0,R(ry),0))
    elif hs=='curly':
        rr=random.Random(7)
        for s in (-1,1):
            for j in range(3): H((s*.64,-.25+j*.3,.92+rr.uniform(-.04,.04)),(.1,.15,.2),bv=.07)
        for ix in range(4):
            for iy in range(4):
                H((-.48+ix*.32+rr.uniform(-.03,.03),-.45+iy*.3+rr.uniform(-.03,.03),1.38+rr.uniform(0,.08)),(.19,.19,.16),rot=(0,0,rr.uniform(-.4,.4)),bv=.09)
        for ix in range(5): H((-.5+ix*.25,-.62,1.18+rr.uniform(-.03,.03)),(.14,.1,.13),bv=.06)
        for ix in range(4): H((-.4+ix*.27,.6,1.0+rr.uniform(-.05,.05)),(.17,.12,.22),bv=.08)
    elif hs in('bob','long'):
        Ln=.75 if hs=='bob' else 1.15
        for s in (-1,1): H((s*.62,.1,1.2-Ln/2-.1),(.1,.55,Ln/2+.1))
        H((0,.56,1.2-Ln/2-.15),(.67,.14,Ln/2+.15)); H((-.2,-.6,1.08),(.46,.09,.14),(0,R(8),0)); H((.42,-.6,1.0),(.2,.09,.2),(0,R(-10),0))
    elif hs=='ponytail':
        for s in (-1,1): H((s*.61,.2,.92),(.08,.44,.28))
        H((0,-.6,1.14),(.62,.08,.1)); H((0,.75,1.1),(.18,.16,.18)); H((0,.86,.72),(.16,.14,.36),rot=(R(12),0,0)); H((0,.66,1.2),(.12,.06,.08),m=M(C.get('tie_c','#C9452E'),.5))
    elif hs=='bun':
        for s in (-1,1): H((s*.61,.2,.9),(.09,.44,.3))
        H((0,.5,1.5),(.28,.28,.26)); H((0,-.6,1.12),(.6,.08,.1))
    elif hs=='short':
        for s in (-1,1): H((s*.61,.2,1.0),(.08,.44,.2))
        H((0,-.58,1.16),(.62,.08,.08))
    elif hs=='old':
        for s in (-1,1): H((s*.61,.2,.9),(.09,.44,.28))
    elif hs=='cap':
        cm=M(C.get('cap','#D2473A'),.7,kind='fabric')
        for s in (-1,1): H((s*.61,.25,.85),(.08,.38,.2))
        H((0,0,1.3),(.69,.69,.2),m=cm); H((0,-.95,1.16),(.55,.38,.04),m=cm)
        if C.get('capstar'): H((0,-.7,1.32),(.1,.02,.1),m=M('#E6B53A',.3,metal=.8),rot=(0,R(45),0))
        else: H((0,-.7,1.3),(.12,.02,.1),m=M('#FFFFFF',.6))
    elif hs=='dupatta':
        dm=M(C.get('dupatta','#2E8B6E'),.85,kind='fabric')
        H((0,.06,1.24),(.74,.72,.17),m=dm,bv=.12); H((0,.62,.72),(.74,.16,.62),m=dm,bv=.08)
        for s in (-1,1): H((s*.72,.08,.72),(.06,.66,.58),m=dm,bv=.05)
        H((0,-.64,1.16),(.56,.06,.08))
    elif hs=='buckethat':
        hm=M(C.get('hat','#C9B48A'),.85,kind='fabric')
        for s in (-1,1): H((s*.61,.2,.9),(.08,.44,.25))
        H((0,0,1.33),(.67,.67,.26),m=hm,bv=.12); H((0,0,1.1),(.95,.95,.035),m=hm,bv=.03); H((0,0,1.2),(.68,.68,.04),m=M(shade(C.get('hat','#C9B48A'),.7),.8),bv=.02)
    elif hs=='helmet':
        hm=M(C.get('helmet','#5B6B45'),.75,kind='fabric')
        H((0,.02,1.22),(.74,.76,.42),m=hm,bv=.34); H((0,.02,.86),(.79,.81,.07),m=M(shade(C.get('helmet','#5B6B45'),.85),.8),bv=.05); H((0,.1,1.5),(.5,.5,.12),m=hm,bv=.1)
        for s in (-1,1): H((s*.64,-.1,.55),(.03,.04,.42),m=M('#2A2A22',.7),bv=.01)
    if C.get('phones'):
        pm=M(C['phones'],.4)
        for s in (-1,1): H((s*.7,0,.62),(.1,.24,.26),m=pm)
        H((0,0,1.42),(.72,.08,.05),m=pm)
    fy=-.62*u-.004; white=M('#FFFFFF',.2,emit=.3); ey=M(C.get('eye','#1B1B22'),.7,spec=.05); BR=[]; EY=[]
    for s in (-1,1):
        EY.append(ocyl((s*.25*u,fy,.66*u),.11*u,.01,ey,Hd,(1,1.3,1))); EY.append(ocyl((s*.25*u+.035*u,fy-.006,.73*u),.036*u,.01,white,Hd))
        _b=obox((s*.25*u,fy,(.93+pose.get('brow',0))*u),(.15*u,.006,.038*u),M(shade(C.get('brow_c',C['hair']),.55),.7),.003,Hd,rot=(0,R(-s*pose.get('brow_r',-5)),0)); BR.append((s,_b,.93*u))
        obox((s*.43*u,fy,.4*u),(.08*u,.004,.045*u),M(shade(C['skin'],.9),.7),.004,Hd)
        if C.get('glasses'):
            g=M('#22242B',.4)
            for dx,dz,hx,hz in [(0,.17,.17,.02),(0,-.17,.17,.02),(.17,0,.02,.17),(-.17,0,.02,.17)]: obox(((s*.25+dx)*u,fy-.012,(.66+dz)*u),(hx*u,.006,hz*u),g,.002,Hd)
        if C.get('freckles'):
            for dx,dz in [(.3,.48),(.38,.52),(.46,.47)]: ocyl((s*dx*u,fy-.001,dz*u),.013*u,.004,M(shade(C['skin'],.75),.7),Hd)
    if C.get('glasses'): obox((0,fy-.012,.68*u),(.08*u,.006,.018*u),M('#22242B',.4),.002,Hd)
    if C.get('beard'):
        obox((0,fy+.004,.07*u),(.5*u,.02,.075*u),M(C['beard'],.7),.01,Hd)
        for s_ in (-1,1): obox((s_*.43*u,fy+.004,.3*u),(.075*u,.02,.21*u),M(C['beard'],.7),.01,Hd)
    if C.get('mustache'): obox((0,fy-.006,.47*u),(.2*u,.012,.042*u),M(C['mustache'],.7),.008,Hd)
    mo=pose.get('mouth','smile'); mm=M('#7A2A20',.5); MO={}
    zm=.38 if C.get('mustache') else .42
    MO['smile']=[obox((.15*u*math.cos(a_),fy,(zm)*u+.15*u*math.sin(a_)),(.03*u,.006,.02*u),mm,.002,Hd,rot=(0,-(a_+R(90)),0)) for a_ in [R(215+i*110/6) for i in range(7)]]
    MO['frown']=[obox((.13*u*math.cos(a_),fy,.2*u+.13*u*math.sin(a_)),(.028*u,.006,.02*u),mm,.002,Hd,rot=(0,-(a_+R(90)),0)) for a_ in [R(40+i*100/6) for i in range(7)]]
    MO['flat']=[obox((0,fy,.3*u),(.13*u,.006,.02*u),mm,.002,Hd)]
    MO['grin']=[obox((0,fy,.3*u),(.19*u,.006,.09*u),M('#4A1512',.5),.02*u,Hd),obox((0,fy-.004,.35*u),(.17*u,.004,.03*u),white,.002,Hd)]
    MO['o']=[ocyl((0,fy,.3*u),.08*u,.01,M('#4A1512',.5),Hd,(1,1.2,1))]
    MO['O']=[ocyl((0,fy,.28*u),.11*u,.01,M('#4A1512',.5),Hd,(1,1.35,1))]
    MO['smirk']=[obox((-.03*u,fy,.3*u),(.11*u,.006,.02*u),mm,.002,Hd,rot=(0,R(-8),0)),obox((.13*u,fy,.34*u),(.04*u,.006,.02*u),mm,.002,Hd,rot=(0,R(-35),0))]
    MO['strain']=[obox((0,fy,.3*u),(.15*u,.006,.035*u),M('#4A1512',.5),.004,Hd),obox((0,fy-.003,.3*u),(.13*u,.004,.012*u),white,.002,Hd)]
    MO['shout']=[ocyl((0,fy,.26*u),.12*u,.01,M('#4A1512',.5),Hd,(1.25,1.0,1)),obox((0,fy-.003,.33*u),(.12*u,.004,.02*u),white,.002,Hd)]
    for k_,objs in MO.items():
        for o_ in objs:
            o_['sc']=tuple(o_.scale)
            if k_!=mo: o_.scale=(0,0,0)
    return dict(root=root,arm=ARM,leg=LEG,head=Hd,u=u,z0=loc[2],brows=BR,mouths=MO,eyes=EY,mouth=mo,X=X,C=C)

def face(H,mouth=None,brow=None,brow_r=None,eyes=None):
    if mouth is not None and H.get('mouths') and mouth!=H.get('mouth'):
        for k_,objs in H['mouths'].items():
            for o_ in objs: o_.scale=tuple(o_['sc']) if k_==mouth else (0,0,0)
        H['mouth']=mouth
    for s_,o_,z0 in H.get('brows',[]):
        if brow is not None: o_.location[2]=z0+min(brow,.06)*H['u']
        if brow_r is not None: o_.rotation_euler[1]=R(-s_*brow_r)
    if eyes is not None:
        for i_,o_ in enumerate(H.get('eyes',[])):
            if i_%2==0: o_.scale=(eyes,1.3*eyes,1)
def lids(H):
    u=H['u']; H['lids']=[obox((s*.25*u,-.62*u-.012,.66*u),(.135*u,.005,.16*u),H['skinm'],.002,H['head']) for s in (-1,1)]
    for o in H['lids']: o.scale=(0,0,0)
def av(loc,rz,C,pose=None,name=None):
    H=avatar(loc,rz,C,pose); H['skinm']=M(C['skin'],.55,spec=.3); H['rz']=rz; H['x']=loc[0]; H['y']=loc[1]
    H['seed']=dseed(name or (C['hair']+C['top']+C['skin']+str(loc))); lids(H); H['blink_force']=None; return H
def blink(H,t,force=None):
    if force is not None: v=force
    else:
        q=(t+H['seed']*1.3)%(2.6+H['seed']%1.1); v=1 if q<.11 else 0
    for o in H['lids']: o.scale=(v,v,v)
def walk(H,dist,step=.6,lift=.07,arm=26,lean=3,t=0,mood=0):
    u=H['u']; Lg=2*u; p=(dist/(2*step))%1.0; zs=[]
    for s in (1,-1):
        q=(p+(0 if s==1 else .5))%1.0
        if q<.5: xf=step/2-step*(q/.5); lf=0
        else: e=ease((q-.5)/.5); xf=-step/2+step*e; lf=lift*math.sin(pi*(q-.5)/.5)
        th=math.asin(max(-.95,min(.95,xf/Lg))); H['leg'][s].rotation_euler[0]=-th
        H['leg'][s].location[2]=2.0*u+lf
        if q<.5: zs.append(Lg*math.cos(th)-Lg)
    H['root'].location[2]=H['z0']+.008+(zs[0] if zs else 0)
    sw=math.sin(2*pi*(p-.04))
    H['arm'][1].rotation_euler[0]=R(arm)*sw; H['arm'][-1].rotation_euler[0]=-R(arm)*sw
    H['arm'][1].rotation_euler[1]=R(-3); H['arm'][-1].rotation_euler[1]=R(3)
    H['root'].rotation_euler[0]=R(lean); H['root'].rotation_euler[1]=R(1.6)*math.sin(2*pi*p)
    H['head'].rotation_euler[1]=-R(1.6)*math.sin(2*pi*p); H['head'].rotation_euler[0]=R(lean+mood)+R(1.2)*math.sin(4*pi*p)
def run(H,dist,t=0,arm=55): walk(H,dist,step=1.0,lift=.24,arm=arm,lean=12,t=t)
def idle(H,t,keep_arms=True):
    s=H['seed']; H['root'].location[2]=H['z0']+.008+.006*math.sin(t*2.1+s)
    H['root'].rotation_euler[1]=R(1.3)*math.sin(t*.7+s); H['root'].rotation_euler[0]=0
    for q in (1,-1): H['leg'][q].rotation_euler[0]=0; H['leg'][q].location[2]=2.0*H['u']
def look(H,target,t,amt=1.0,maxdeg=55):
    rz=H['root'].rotation_euler[2]; dx=target[0]-H['root'].location[0]; dy=target[1]-H['root'].location[1]
    a=math.atan2(dx,-dy)-rz; a=(a+pi)%(2*pi)-pi; a=max(-R(maxdeg),min(R(maxdeg),a)); H['head'].rotation_euler[2]=a*amt
def gaze_idle(H,t):
    s=H['seed']; H['head'].rotation_euler[2]=R(14)*math.sin(t*.6+s)*ease(math.sin(t*.23+s*2)*.5+.5); H['head'].rotation_euler[0]=R(3)*math.sin(t*.4+s)
def kneel(H,k,bow=1.0):
    u=H['u']; Lg=2*u; th=math.acos(max(.05,1-.45*k));
    H['leg'][1].rotation_euler[0]=-th; H['leg'][-1].rotation_euler[0]=th
    drop=Lg-Lg*math.cos(th); H['root'].location[2]=H['z0']+.008-drop
    H['root'].rotation_euler[0]=R(10)*k*bow; H['head'].rotation_euler[0]=R(30)*k*bow
    H['arm'][1].rotation_euler=(-R(38)*k,0,0); H['arm'][-1].rotation_euler=(R(10)*k,0,0)
def shock(H,k):
    H['arm'][1].rotation_euler=(-R(110)*k,0,R(25)*k); H['arm'][-1].rotation_euler=(-R(110)*k,0,-R(25)*k)
def hand_pos(H,s=1):
    u=H['u']; return H['arm'][s].matrix_world@Vector((s*.5*u,0,-1.95*u))
def accel(d,v,tau=.25): return 0 if d<=0 else v*(d-tau*(1-math.exp(-d/tau)))

SK=['#F2C6A0','#E8B48C','#C98F62','#B97A4E','#8A5A3C','#F7D2B0','#D9A074','#6E4630']; HR=['#1E1A18','#3B2314','#5A3415','#C9772B','#E3C36A','#2A1B14','#6B6B74','#B5522A']
TPC=['#D2473A','#2B58C9','#35975A','#E6A31C','#7448C2','#16909E','#F4F1EA','#CF3F78','#3A3D47','#8E5BA8']; PN=['#27365A','#3A3D47','#4A3D32','#D8D2C8','#22242B','#3B6FB6','#5A5F4A']
def design(seed,kid=False):
    r=random.Random(seed*31+5); c=dict(skin=r.choice(SK),hair=r.choice(HR),hairstyle=r.choice(['quiff','fringe','bob','long','bun','short','cap','ponytail','curly']),top=r.choice(TPC),pants=r.choice(PN),
        shoes=r.choice(['#F4F5FA','#22242B','#C9A27A','#D2473A','#3A2A1E']),accent=r.choice(['#D2473A','#FFFFFF','#22242B','#F2C12E']),h=(r.choice([.78,.8,.83]) if kid else r.choice([.94,.97,1.0,1.03,1.06])),short=r.random()<.35)
    if r.random()<.5: c['jacket']=r.choice(TPC); c['top']=r.choice(['#F4F1EA','#E9EAF0','#22242B'])
    if c['hairstyle']=='cap': c['cap']=r.choice(TPC)
    if kid: c['pack']=r.choice(TPC)
    elif r.random()<.25: c['bag']=r.choice(['#7A4A22','#22242B','#A8362C'])
    if not kid and r.random()<.2: c['glasses']=True
    return c
def soldier(seed):
    r=random.Random(seed*13+3)
    return dict(skin=r.choice(SK),hair=r.choice(['#1E1A18','#3B2314','#2A1B14']),hairstyle='helmet',helmet=r.choice(['#5B6B45','#55643F','#606F48']),top='#5E6B47',trim='#4C5739',
                pants='#56623F',cargo=True,boots=r.choice(['#2B241E','#3A2E22']),vest=r.choice(['#4A5536','#454F33']),military=True,h=r.choice([.98,1.0,1.03,1.05]),gloves='#2A2A22',brow_c='#2A1B14',radio=(r.random()<.3))
