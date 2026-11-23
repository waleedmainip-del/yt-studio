# Lahori cast costume system. Builds on avatar() v3 (chars_base.py, unchanged) and adds kurta, shalwar, sandals,
# waistcoat, dupatta, braid, topi, moustaches, alien anatomy + armour, apron/chef props.
def avatar_lh(loc,rotz,C,pose=None,name=None):
    C=dict(C)
    if C.get('kurta'): C.setdefault('belt',C['top']); C.setdefault('buckle',C['top'])
    if C.get('sandals'): C['shoes']=C['skin']; C['accent']=C['sandals']; C['sole']=shade(C['sandals'],.55)
    H=av(loc,rotz,C,pose,name=name); u=H['u']; root=H['root']; Hd=H['head']; ARM=H['arm']; LEG=H['leg']; fr=-.5*u; fy=-.62*u-.004
    tee=M(C['top'],.8,kind='fabric',spec=.2); trim=M(C.get('trim',shade(C['top'],.75)),.8,kind='fabric',spec=.2); skin=M(C['skin'],.55,spec=.3)
    pants=M(C['pants'],.85,kind='fabric',spec=.2); hair=M(C['hair'],.6,spec=.3); gold=M('#D9B24A',.3,metal=.9); dk=M('#1B1B22',.3)
    def Hh(c,s_,m=hair,rot=(0,0,0),bv=.06): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,Hd,rot=rot)
    def Rb(c,s_,m,rot=(0,0,0),bv=.02,par=None): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,par or root,rot=rot)
    H['xeyes']=[]
    if C.get('kurta'):
        st=M(shade(C['top'],.8),.8)
        for s in (-1,1):
            Rb((0,0,-.3),(.515,.53,.33),tee,bv=.04,par=LEG[s]); Rb((0,0,-.62),(.52,.535,.028),trim,bv=.008,par=LEG[s])
            Rb((s*.5,-.535,-.4),(.012,.004,.2),st,bv=.001,par=LEG[s])
            Rb((s*.965,-.512,3.0),(.012,.01,.96),st,bv=.001)
        Rb((0,0,4.04),(.37,.37,.075),trim,bv=.03); Rb((0,-.525,3.5),(.085,.02,.48),trim,bv=.004)
        for i in range(3): ocyl((0,fr-.022*u-.012,(3.85-i*.28)*u),.035*u,.012,M(C.get('button','#F4F1EA'),.4),root)
        Rb((.52,-.515,3.45),(.2,.012,.17),st,bv=.004); Rb((.52,-.525,3.6),(.21,.014,.025),trim,bv=.003)
    if C.get('shalwar'):
        for s in (-1,1): Rb((0,0,-1.12),(.535,.545,.42),pants,bv=.12,par=LEG[s])
    if C.get('sandals'):
        sm=M(C['sandals'],.6)
        for s in (-1,1):
            Rb((0,-.36,-1.8),(.53,.1,.165),sm,par=LEG[s]); Rb((0,.48,-1.78),(.53,.05,.14),sm,par=LEG[s]); Rb((0,-.2,-1.665),(.07,.3,.03),sm,bv=.01,par=LEG[s])
            ocyl((0,-.36*u,-1.63*u),.05*u,.02,gold,LEG[s],rot=(0,0,0))
    if C.get('watch'):
        Rb((.5,-.545,-1.42),(.13,.012,.1),M('#C9CED8',.25,metal=.9),bv=.01,par=ARM[1]); Rb((.5,-.556,-1.42),(.09,.006,.07),M('#0E1A2B',.2),bv=.005,par=ARM[1])
    if C.get('waistcoat'):
        wc=M(C['waistcoat'],.8,kind='fabric',spec=.2); wd=M(shade(C['waistcoat'],.75),.8)
        for s in (-1,1):
            Rb((s*.57,-.535,3.02),(.43,.035,.96),wc,bv=.02); Rb((s*1.012,0,2.95),(.02,.52,.88),wc,bv=.01)
            Rb((s*.6,-.575,2.55),(.26,.012,.03),wd,bv=.004); Rb((s*.5,-.05,4.045),(.34,.5,.03),wc,bv=.02)
        Rb((0,.53,3.02),(1.0,.035,.96),wc,bv=.02)
        for i in range(3): ocyl((.2*u,fr-.045*u-.012,(3.3-i*.32)*u),.04*u,.012,gold,root)
        Rb((-.58,-.578,3.5),(.2,.01,.025),M('#F4F1EA',.6),bv=.003)
    if C.get('topi'):
        tm=M(C['topi'],.85,kind='fabric'); Hh((0,.02,1.36),(.6,.6,.2),tm,bv=.1); Hh((0,.02,1.2),(.63,.63,.045),M(shade(C['topi'],.86),.85),bv=.02)
    if C.get('receding'):
        g=M(C.get('grey','#9A9AA2'),.6)
        Hh((0,.53,.75),(.67,.18,.48)); Hh((0,.3,1.22),(.62,.4,.1))
        for s in (-1,1): Hh((s*.62,.28,.88),(.08,.36,.3)); Hh((s*.625,-.02,.8),(.075,.12,.2),g); Hh((s*.5,.02,1.2),(.16,.2,.09),g)
    if C.get('textured'):
        rr=random.Random(11)
        for i in range(14):
            Hh((rr.uniform(-.5,.5),rr.uniform(-.5,.35),1.42+rr.uniform(0,.14)),(.17,.17,.12),rot=(R(rr.uniform(-20,10)),R(rr.uniform(-18,18)),rr.uniform(-.6,.6)),bv=.07)
        for s in (-1,1): Hh((s*.64,.12,.72),(.035,.45,.2),M(shade(C['hair'],1.5),.6),bv=.02)
    if C.get('neat'):
        Hh((.06,-.1,1.38),(.62,.58,.1),bv=.08); Hh((.2,-.56,1.26),(.42,.1,.11),rot=(0,R(-10),0)); Hh((-.42,-.56,1.2),(.2,.1,.09),rot=(0,R(14),0)); Hh((-.3,-.2,1.47),(.02,.42,.02),M(shade(C['skin'],.9),.6),bv=.005)
    if C.get('cheeks'):
        for s in (-1,1): Hh((s*.53,-.38,.3),(.14,.26,.2),skin,bv=.12); ocyl((s*.42*u,fy-.002,.36*u),.1*u,.006,M('#E88A76',.8),Hd)
    if C.get('stache'):
        sm=M(C['stache'],.7); st=C.get('stache_style','strong')
        for o_ in H['mouths'].values():
            pass
        if st=='handlebar':
            Hh((0,-.635,.47),(.2,.03,.075),sm,bv=.03)
            for s in (-1,1): Hh((s*.3,-.635,.44),(.14,.028,.065),sm,rot=(0,R(s*14),0),bv=.03); Hh((s*.47,-.635,.5),(.055,.026,.085),sm,rot=(0,R(-s*28),0),bv=.025)
        else:
            Hh((0,-.635,.47),(.3,.03,.08),sm,bv=.03)
            for s in (-1,1): Hh((s*.33,-.635,.4),(.07,.028,.1),sm,rot=(0,R(s*12),0),bv=.03)
    if C.get('lashes'):
        for s in (-1,1):
            Hh((s*.37,-.628,.79),(.07,.004,.018),dk,rot=(0,R(-s*32),0),bv=.002); Hh((s*.25,-.628,.82),(.12,.004,.014),dk,bv=.002)
        ocyl((0,fy-.003,.3*u),.001,.001,dk,Hd)
    if C.get('earrings'):
        for s in (-1,1): Hh((s*.645,-.2,.3),(.03,.03,.03),gold,bv=.02); Hh((s*.645,-.2,.2),(.05,.05,.06),gold,bv=.03)
    if C.get('bangles'):
        for s in (-1,1): Rb((s*.5,0,-1.4),(.545,.545,.03),gold,bv=.01,par=ARM[s]); Rb((s*.5,0,-1.3),(.545,.545,.02),M('#7A1F2E',.4),bv=.008,par=ARM[s])
    if C.get('braid'):
        pts=[(.28,.66,4.72),(.5,.6,4.4),(.72,.3,4.14),(.78,-.2,4.1),(.7,-.56,3.86),(.64,-.63,3.5),(.62,-.64,3.14),(.62,-.64,2.8),(.62,-.64,2.48)]
        for i,p in enumerate(pts): Rb(p,(.14,.13,.21),hair,rot=(0,0,(.45 if i%2 else -.45)),bv=.09)
        Rb((.62,-.64,2.28),(.1,.1,.06),M(C.get('tie_c','#7A1F2E'),.5),bv=.03); Rb((.62,-.64,2.12),(.11,.1,.12),hair,bv=.07)
        Hh((0,-.6,1.16),(.62,.08,.09)); Hh((-.3,-.62,1.02),(.3,.07,.16),rot=(0,R(18),0)); Hh((.34,-.62,1.02),(.28,.07,.16),rot=(0,R(-18),0))
    if C.get('dupatta'):
        dp=M(C['dupatta'],.85,kind='fabric',spec=.2); dt=M(C.get('dupatta_trim','#E6B53A'),.5,metal=.4)
        Rb((-.1,-.56,3.62),(.95,.035,.2),dp,rot=(0,R(14),0),bv=.03); Rb((-.1,-.585,3.47),(.93,.012,.022),dt,rot=(0,R(14),0),bv=.004)
        Rb((-.72,-.02,4.05),(.3,.54,.05),dp,bv=.03); Rb((.78,0,4.06),(.24,.54,.05),dp,bv=.03)
        Rb((-.72,.555,3.05),(.27,.035,1.05),dp,bv=.03); Rb((-.72,.575,2.05),(.27,.014,.03),dt,bv=.004)
        Rb((.2,.555,3.5),(.7,.035,.5),dp,rot=(0,R(-20),0),bv=.03)
    if C.get('alien'):
        sk2=M(shade(C['skin'],.72),.5,spec=.3); met=M(C.get('armour','#2B2F3A'),.32,metal=.9); met2=M(shade(C.get('armour','#2B2F3A'),1.3),.3,metal=.9); bl=glow(C.get('glowc','#35C8FF'),4.0)
        Hh((0,.12,1.42),(.52,.5,.3),skin,bv=.24); Hh((0,.2,1.8),(.3,.4,.2),skin,bv=.18); Hh((0,-.02,1.52),(.06,.56,.26),sk2,bv=.05)
        for s in (-1,1):
            Hh((s*.5,.32,1.62),(.09,.3,.42),sk2,rot=(R(-28),R(s*16),0),bv=.07); Hh((s*.66,.1,.75),(.06,.3,.2),sk2,rot=(R(-12),0,R(s*10)),bv=.05)
            e1=ocyl((s*.3*u,fy-.004,.7*u),.2*u,.012,M('#0B0B12',.15,spec=.8),Hd,(1,1,1.3)); e1.rotation_euler=(R(90),R(-s*16),0)
            e2=ocyl((s*.3*u,fy-.012,.7*u),.1*u,.012,glow('#39E6D2',2.5),Hd,(1,1,1.25)); e3=ocyl((s*.3*u+.05*u,fy-.02,.79*u),.04*u,.01,M('#FFFFFF',.2,emit=.6),Hd)
            H['xeyes']+= [e1,e2]
            Hh((s*.43,-.63,.4),(.085,.01,.05),skin,bv=.004)
        Hh((0,-.63,.52),(.03,.012,.07),sk2,bv=.01)
        # armour
    if C.get('alien') and not C.get('no_armour'):
        Rb((0,-.56,3.3),(.86,.07,.6),met,bv=.06); Rb((0,-.6,3.42),(.5,.05,.32),met2,bv=.05); ocyl((0,fr-.14*u-.012,3.42*u),.17*u,.02,bl,root); ocyl((0,fr-.13*u-.012,3.42*u),.22*u,.02,met,root)
        for s in (-1,1):
            Rb((s*.62,-.625,3.42),(.14,.012,.02),bl,bv=.004); Rb((s*.5,-.58,2.5),(.34,.05,.2),met2,bv=.04); Rb((s*.5,-.625,2.5),(.2,.012,.018),bl,bv=.004)
            Rb((s*.5,0,.16),(.74,.72,.24),met,bv=.12,par=ARM[s]); Rb((s*.62,0,.42),(.5,.56,.12),met2,bv=.08,par=ARM[s]); Rb((s*.5,-.73,.12),(.4,.012,.022),bl,bv=.004,par=ARM[s])
            Rb((s*.5,0,-1.22),(.57,.57,.32),met,bv=.06,par=ARM[s]); Rb((s*.5,-.575,-1.22),(.3,.012,.02),bl,bv=.004,par=ARM[s])
            Rb((0,-.52,-.75),(.4,.04,.22),met2,bv=.05,par=LEG[s]); Rb((0,-.6,-1.5),(.3,.012,.02),bl,bv=.004,par=LEG[s]); Rb((0,-.52,-.2),(.42,.03,.14),met,bv=.04,par=LEG[s])
        Rb((0,.4,4.12),(.7,.28,.2),met,bv=.1); Rb((0,.56,3.2),(.8,.06,.7),met,bv=.06); Rb((0,.625,3.3),(.04,.012,.5),bl,bv=.004)
    if C.get('rolled'):
        for s in (-1,1): Rb((s*.5,0,-.82),(.535,.535,.085),trim,bv=.04,par=ARM[s])
    if C.get('apron'):
        am=M(C['apron'],.8,kind='fabric')
        for s in (-1,1): Rb((0,-.545,-.36),(.5,.022,.42),am,bv=.01,par=LEG[s])
        Rb((0,0,4.07),(.4,.4,.04),am,bv=.02); Rb((0,-.575,2.72),(.32,.01,.02),M(shade(C['apron'],.7),.8),bv=.003)
    if C.get('towel'):
        tw=M(C['towel'],.9,kind='fabric'); tw2=M('#F4F1EA',.9)
        Rb((.72,-.05,4.07),(.24,.56,.045),tw,bv=.03); Rb((.72,-.585,3.62),(.22,.035,.42),tw,bv=.03); Rb((.72,.56,3.7),(.22,.035,.36),tw,bv=.03)
        for z in (3.36,3.5): Rb((.72,-.625,z),(.22,.008,.025),tw2,bv=.003)
    if C.get('ladle'):
        lm=M('#C9CED8',.3,metal=.9); a=ARM[-1]
        Rb((-.5,-.2,-1.9),(.035,.035,.62),lm,bv=.02,par=a,rot=(R(-78),0,0)); o=ocyl((-.5*u,-.9*u,-1.76*u),.2*u,.12*u,lm,a,rot=(0,0,0),r2=.12*u)
        Rb((-.5,.38,-2.02),(.05,.05,.09),M('#5E3A1E',.6),bv=.03,par=a,rot=(R(-78),0,0))
    for s_,o_,z0 in H['brows']: o_.scale=(C.get('brow_w',1.0),1,C.get('brow_t',1.0))
    w=C.get('wide',1.0)
    if w!=1.0:
        root.scale=(w,1+(w-1)*.45,1); fw=C.get('face_w',.5); Hd.scale=((1+(w-1)*fw)/w,1/(1+(w-1)*.45),1)
    return H
