# "Baddie Ghar Par" costume additions: oily (glossy) hair, full-face rider helmet, rider jacket stripes, delivery box, phone, iced coffee.
def avatar_bg(loc,rotz,C,pose=None,name=None):
    H=avatar_bd(loc,rotz,C,pose,name=name); u=H['u']; root=H['root']; Hd=H['head']; ARM=H['arm']; fy=-.62*u-.004
    def Hh(c,s_,m,rot=(0,0,0),bv=.03,par=None): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,par or Hd,rot=rot)
    def Rb(c,s_,m,rot=(0,0,0),bv=.02,par=None): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,par or root,rot=rot)
    if C.get('longhair'):
        hm=M(C['hair'],.6,spec=.3); hl=M(C.get('highlights',C['hair']),.5,spec=.4)
        Hh((0,.64,.25),(.64,.1,.85),hm,bv=.08); Hh((0,.6,-.55),(.56,.1,.3),hm,bv=.1)
        for s_ in (-1,1):
            Hh((s_*.64,-.05,.15),(.1,.5,.75),hm,bv=.06); Hh((s_*.5,-.45,-.45),(.16,.12,.35),hm,bv=.08)
            Hh((s_*.67,-.2,.3),(.03,.1,.5),hl,bv=.02)
    if C.get('oily'):
        gl=M(C['hair'],.3,spec=.85)
        for o in Hd.children_recursive:
            if o.type=='MESH' and o.active_material and o.active_material.name.startswith(C['hair']) and 'fabric' not in o.active_material.name: o.active_material=gl
    if C.get('rider'):
        ref=M('#E9EEF2',.25,spec=.9,emit=.25); dk=M('#1C1D22',.6)
        Rb((0,-.522,3.15),(1.0,.012,.06),ref,bv=.005); Rb((0,.522,3.15),(1.0,.012,.06),ref,bv=.005)
        for s in (-1,1): Rb((s*.5,0,-.9),(.53,.53,.05),ref,bv=.01,par=ARM[s]); Rb((s*.5,0,-.5),(.53,.53,.04),dk,bv=.01,par=ARM[s])
        Rb((0,.53,3.7),(.62,.01,.24),M('#F4F1EA',.5),bv=.01)
        stext('TEZ',(0,.545*u,3.74*u),.16*u,C['jacket'],n=(0,1,0),parent=root); stext('DELIVERY',(0,.545*u,3.55*u),.075*u,'#16171C',n=(0,1,0),parent=root)
        Rb((-.55,-.53,3.75),(.2,.012,.1),M('#F4F1EA',.5),bv=.01); stext('TEZ',(-.55*u,-.545*u,3.74*u),.07*u,C['jacket'],parent=root)
    if C.get('dbox'):
        bm=M(C['dbox'],.5); e=empty((0,.62*u,3.0*u),root)
        obox((0,.42*u,0),(.9*u,.42*u,.8*u),bm,.06*u,e); obox((0,.85*u,0),(.6*u,.012,.32*u),M('#F4F1EA',.5),.01,e)
        stext('TEZ',(0,.87*u,.05*u),.2*u,C['dbox'],n=(0,1,0),parent=e); stext('DELIVERY',(0,.87*u,-.14*u),.08*u,'#16171C',n=(0,1,0),parent=e)
        for s in (-1,1): obox((s*.45*u,-.05*u,.35*u),(.07*u,.08*u,.5*u),M('#1C1D22',.6),.02*u,e)
        H['props']['dbox']=e
    if C.get('moto'):
        hm=C['hair']; H['hair_objs']=[o for o in Hd.children if o.type=='MESH' and o.active_material and o.active_material.name.startswith(hm)]
        for o in H['hair_objs']: o.scale=(0,0,0)
        e=empty((0,0,0),Hd); sh=M(C['moto'],.25,spec=.9); vz=M('#101218',.05,spec=1.0)
        obox((0,.02*u,.62*u),(.74*u,.74*u,.72*u),sh,.3*u,e); obox((0,-.7*u,.7*u),(.6*u,.06*u,.28*u),vz,.1*u,e)
        obox((0,.05*u,1.33*u),(.14*u,.62*u,.04*u),M('#F4F1EA',.4),.03*u,e); obox((0,-.7*u,.22*u),(.5*u,.06*u,.12*u),M('#1C1D22',.5),.05*u,e)
        H['props']['helmet']=e
    if C.get('hand_helmet'):
        a=ARM[1]; e=empty((.5*u,-.2*u,-2.15*u),a); sh=M(C['hand_helmet'],.25,spec=.9)
        obox((0,0,0),(.62*u,.62*u,.6*u),sh,.26*u,e); obox((0,-.6*u,.05*u),(.5*u,.05*u,.22*u),M('#101218',.05,spec=1.0),.08*u,e); H['props']['hhelmet']=e
    return H
def phone_in_hand(H,s=1,screen='#2A3A5A',em=1.2):
    u=H['u']; a=H['arm'][s]; e=empty((s*.5*u,-.42*u,-2.05*u),a)
    obox((0,0,0),(.2*u,.02*u,.4*u),M('#16171C',.3,spec=.8),.03*u,e); obox((0,-.022*u,0),(.18*u,.004,.37*u),M(screen,.3,emit=em),.01*u,e)
    return e
def coffee_cup(H,s=-1):
    u=H['u']; a=H['arm'][s]; e=empty((s*.5*u,-.3*u,-2.1*u),a)
    ocyl((0,0,0),.15*u,.42*u,M('#EAF2F4',.1,alpha=.55),e,rot=(0,0,0),r2=.12*u); ocyl((0,0,-.02*u),.135*u,.34*u,M('#8A5A36',.4),e,rot=(0,0,0),r2=.11*u)
    ocyl((0,0,.23*u),.16*u,.04*u,M('#F4F1EA',.3),e,rot=(0,0,0)); obox((.05*u,0,.42*u),(.015*u,.015*u,.2*u),M('#2E8A6A',.4),.005*u,e,rot=(0,R(12),0))
    return e
