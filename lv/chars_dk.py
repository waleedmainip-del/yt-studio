# Cast costume additions for "The Guy Who Couldn't Be Killed": Death (hood, robe, skull, scythe), band-aids, curlers, overalls.
def avatar_dk(loc,rotz,C,pose=None,name=None):
    C=dict(C)
    H=avatar_lh(loc,rotz,C,pose,name=name); u=H['u']; root=H['root']; Hd=H['head']; ARM=H['arm']; LEG=H['leg']; fy=-.62*u-.004
    def Hh(c,s_,m,rot=(0,0,0),bv=.06): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,Hd,rot=rot)
    def Rb(c,s_,m,rot=(0,0,0),bv=.02,par=None): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,par or root,rot=rot)
    H['props']={}
    if C.get('bandaid'):
        bm=M('#E8B98E',.7); bp=M('#D9A27A',.8)
        Hh((-.4,-.63,.45),(.17,.008,.06),bm,rot=(0,R(28),0),bv=.02); Hh((-.4,-.637,.45),(.05,.004,.045),bp,rot=(0,R(28),0),bv=.01)
        Hh((.28,-.63,1.12),(.14,.008,.05),bm,rot=(0,R(-12),0),bv=.02); Hh((.28,-.637,1.12),(.04,.004,.04),bp,rot=(0,R(-12),0),bv=.01)
        Rb((-.5,-.56,-.9),(.14,.01,.06),bm,par=ARM[-1],bv=.01)
    if C.get('scruffy'):   # messy spikes on top of the hair
        hm=M(C['hair'],.6,spec=.3); rr=random.Random(5)
        for i in range(9): Hh((rr.uniform(-.5,.5),rr.uniform(-.45,.4),1.38+rr.uniform(0,.12)),(.13,.13,.16),hm,rot=(R(rr.uniform(-35,35)),R(rr.uniform(-35,35)),rr.uniform(-.8,.8)),bv=.05)
        Hh((-.35,-.62,1.1),(.22,.07,.12),hm,rot=(0,R(25),0)); Hh((.1,-.63,1.08),(.18,.07,.14),hm,rot=(0,R(-15),0))
    if C.get('curlers'):
        cm=[M(c,.5) for c in ('#F28BB0','#7FC8F0','#F7D26A')]
        for i,(x,y,z) in enumerate([(-.42,-.3,1.42),(0,-.35,1.47),(.42,-.3,1.42),(-.3,.15,1.5),(.3,.15,1.5),(0,.4,1.4)]):
            ocyl((x*u,y*u,z*u),.11*u,.34*u,cm[i%3],Hd,rot=(0,R(90),0),seg=12)
    if C.get('robe'):   # bathrobe collar + belt
        rm=M(shade(C['top'],.85),.9,kind='fabric')
        for s in (-1,1): Rb((s*.32,-.53,3.55),(.2,.03,.5),rm,rot=(0,R(s*-22),0),bv=.02)
        Rb((0,-.54,2.6),(1.02,.03,.07),rm,bv=.01); Rb((.35,-.57,2.4),(.05,.02,.22),rm,bv=.01)
        for s in (-1,1): Rb((0,0,-.55),(.53,.54,.5),M(C['top'],.9,kind='fabric'),par=LEG[s],bv=.05)
    if C.get('overalls'):
        om=M(C['overalls'],.85,kind='fabric'); gm=M('#D9B24A',.3,metal=.8)
        Rb((0,-.53,2.75),(.62,.03,.6),om,bv=.02)
        for s in (-1,1): Rb((s*.45,-.535,3.65),(.1,.02,.42),om,bv=.01); Rb((s*.45,-.56,3.35),(.06,.01,.06),gm,bv=.01); Rb((s*.45,.53,3.4),(.1,.02,.62),om,bv=.01)
    if C.get('death'):
        hood=M(C['top'],.9,kind='fabric',spec=.1); hin=M('#07060A',.95,spec=0); bone=M(C['skin'],.5,spec=.3); bone2=M(shade(C['skin'],.7),.6)
        # hood shell around the head (open at the face)
        Hh((0,.12,1.5),(.82,.82,.14),hood,bv=.12); Hh((0,.72,.62),(.82,.14,.9),hood,bv=.1)
        for s in (-1,1): Hh((s*.76,.08,.62),(.1,.72,.92),hood,bv=.08); Hh((s*.64,-.6,.72),(.14,.08,.86),hood,rot=(0,0,R(s*-8)),bv=.05)
        Hh((0,-.58,1.36),(.7,.12,.1),hood,bv=.06); Hh((0,.15,1.68),(.3,.5,.1),hood,rot=(R(-12),0,0),bv=.08)
        edge=M(C.get('edge','#3B2F4E'),.8,kind='fabric')
        for s in (-1,1): Hh((s*.67,-.52,.72),(.03,.04,.8),hin,bv=.01); Hh((s*.78,-.69,.72),(.05,.02,.86),edge,bv=.01)
        Hh((0,-.69,1.44),(.82,.02,.05),edge,bv=.01)
        # skull details: deep sockets, red ember eyes, nose hole, teeth, cheek cracks
        for i_,o_ in enumerate(H['eyes']):
            if i_%2==1: o_.scale=(0,0,0)
        H['xeyes']=[]
        for s in (-1,1):
            e=ocyl((s*.25*u,fy-.004,.68*u),.15*u,.01,M('#0A0608',.9,spec=0),Hd,(1,1.2,1))
            g=ocyl((s*.25*u,fy-.012,.68*u),.06*u,.012,glow(C.get('glowc','#FF3B2F'),6.0),Hd)
            H['xeyes']+= [g]; Hh((s*.42,-.63,.4),(.02,.006,.09),bone2,rot=(0,R(s*20),0),bv=.003)
        Hh((0,-.632,.5),(.06,.006,.07),M('#0A0608',.9),rot=(0,R(45),0),bv=.004)
        for k_ in range(6): Hh((-.2+k_*.08,-.632,.16),(.03,.006,.05),M('#F7F3E8',.4),bv=.006)
        Hh((0,-.629,.16),(.27,.004,.075),M('#1A1214',.8),bv=.004)
        Hh((.18,-.632,1.0),(.012,.004,.12),bone2,rot=(0,R(25),0),bv=.002)
        # long robe to the floor with ragged hem, rope belt, wide sleeves
        for s in (-1,1):
            Rb((0,0,-1.05),(.56,.56,1.0),hood,par=LEG[s],bv=.06)
            for j in range(4): Rb((-.36+j*.24,-.57,-2.02-.06*(j%2)),(.1,.02,.06),hood,par=LEG[s],rot=(0,R(10*(j%2)),0),bv=.01)
            Rb((s*.5,0,-.75),(.66,.66,.7),hood,par=ARM[s],bv=.08); Rb((s*.5,0,-1.42),(.67,.67,.04),edge,par=ARM[s],bv=.02)
        Rb((0,0,2.15),(1.05,.56,.08),M('#5A4630',.9,kind='fabric'),bv=.03); Rb((.4,-.6,1.85),(.04,.03,.3),M('#5A4630',.9),bv=.01)
        Rb((0,.55,3.1),(.95,.06,1.0),hood,bv=.04)
        for s in (-1,1): Rb((s*.62,-.52,3.1),(.38,.04,.98),hood,bv=.03); Rb((s*.25,-.565,3.1),(.03,.01,.98),edge,bv=.005)
        # scythe in the left hand
        sw=M('#3A2A20',.7,kind='wood',sc=.5); bl=M('#C9CED8',.2,metal=1.0,spec=.9); a=ARM[-1]
        sc_=empty((-.5*u,-.05*u,-1.9*u),a); H['props']['scythe']=sc_
        ocyl((0,0,1.2*u),.055*u,6.4*u,sw,sc_,rot=(0,0,0),seg=10)
        for i in range(10):
            f=i/9; x=-1.9*u*f; z=4.45*u-.75*u*f*f; sl=math.atan2(1.5*f,1.9)
            obox((x,0,z),(.13*u,.025*u,(.17-.12*f)*u),bl,.01,sc_,rot=(0,sl,0))
        obox((-.05*u,0,4.35*u),(.12*u,.08*u,.12*u),M('#2A2C34',.4,metal=.8),.02,sc_)
    return H

def sandwich(parent=None,loc=(0,0,0),s=1.0):
    e=empty(loc,parent)
    for z,col,h,w in ((0,'#E2B36A',.035,.16),(.04,'#6FC38A',.012,.17),(.055,'#E8554D',.012,.15),(.07,'#F2D46A',.01,.16),(.085,'#C9704E',.016,.15),(.11,'#E2B36A',.035,.16)):
        obox((0,0,z*s),(w*s,.08*s,h*s),M(col,.7),.01*s,e)
    return e
def phone_obj(parent=None,loc=(0,0,0),s=1.0,lit=True):
    e=empty(loc,parent); obox((0,0,0),(.05*s,.008*s,.1*s),M('#16171C',.2,spec=.9),.01*s,e)
    scr=obox((0,-.009*s,0),(.044*s,.002,.092*s),M('#8FD0FF',.3,emit=2.0) if lit else M('#0B0B10',.2),.003,e); e['scr']=scr.name; return e
def piano(loc,rotz=0,broken=False):
    root=empty(loc,rot=(0,0,R(rotz))); bk=M('#141218',.18,spec=.9); wd=M('#2A1C18',.3,spec=.7); wh=M('#F4F1EA',.3); gold=M('#D9B24A',.3,metal=.9)
    P={}
    if not broken:
        obox((0,0,.75),(.78,.32,.75),bk,.03,root); obox((0,-.42,.82),(.75,.14,.04),wh,.01,root); obox((0,-.32,.9),(.75,.04,.08),bk,.01,root)
        for i in range(30): obox((-.72+i*.05,-.5,.86),(.015,.07,.015),bk,0,root)
        obox((0,0,1.52),(.82,.36,.04),bk,.02,root); obox((0,-.32,.2),(.7,.04,.18),wd,.01,root)
        for s in (-1,1): obox((s*.66,-.46,.42),(.06,.06,.42),bk,.02,root); ocyl((s*.3,-.34,1.2),.04,.02,gold,root)
        obox((0,-.33,1.18),(.3,.01,.12),M('#2A2C34',.4),.01,root)
    else:
        r=random.Random(9)
        obox((0,0,.25),(.8,.34,.25),bk,.03,root,rot=(R(8),R(-6),R(12))); obox((.3,.1,.6),(.5,.06,.4),bk,.02,root,rot=(R(-40),R(20),R(-30)))
        obox((-.9,-.4,.08),(.75,.14,.04),wh,.01,root,rot=(0,0,R(-25)))
        for i in range(26):
            x=r.uniform(-2.2,2.2); y=r.uniform(-1.8,1.6)
            obox((x,y,.02),(.015 if i%3 else .05,.07,.015),bk if i%3 else wh,0,root,rot=(0,0,r.uniform(0,6.3)))
        for i in range(7): obox((r.uniform(-1.5,1.5),r.uniform(-1.2,1.2),.05),(r.uniform(.1,.35),.03,r.uniform(.05,.12)),wd if i%2 else bk,.01,root,rot=(r.uniform(-.4,.4),r.uniform(-.4,.4),r.uniform(0,6.3)))
        for i in range(5): ocyl((r.uniform(-1,1),r.uniform(-1,1),.01),.008,r.uniform(.6,1.4),gold,root,rot=(R(90),0,r.uniform(0,6.3)),seg=6)
    return dict(root=root)
