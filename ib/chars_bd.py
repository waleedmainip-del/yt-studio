# Costume additions for the Lahori Baddie cast: sunglasses, chain, handbag, bow tie.
def avatar_bd(loc,rotz,C,pose=None,name=None):
    H=avatar_lh(loc,rotz,dict(C),pose,name=name); u=H['u']; root=H['root']; Hd=H['head']; ARM=H['arm']; fy=-.62*u-.004
    def Hh(c,s_,m,rot=(0,0,0),bv=.03): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,Hd,rot=rot)
    def Rb(c,s_,m,rot=(0,0,0),bv=.02,par=None): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,par or root,rot=rot)
    H['props']={}
    if C.get('shades'):
        e=empty((0,0,0),Hd); lm=M('#0E0F14',.08,spec=1.0); fm=M(C.get('shade_c','#D9B24A'),.3,metal=.9)
        for s in (-1,1): obox((s*.27*u,fy-.03,.68*u),(.21*u,.012,.15*u),lm,.04*u,e); obox((s*.63*u,-.3*u,.72*u),(.012,.32*u,.02*u),fm,0,e)
        obox((0,fy-.03,.74*u),(.08*u,.012,.02*u),fm,0,e); H['props']['shades']=e
        if C['shades']=='up': e.location=(0,.12*u,.62*u); e.rotation_euler=(R(-28),0,0)
    if C.get('chain'):
        gm=M('#E6C25A',.25,metal=1.0)
        for k in range(9):
            a=R(-60+k*15); Rb((.34*math.sin(a),-.525,3.78-.36*math.cos(a)),(.035,.012,.035),gm,bv=.012)
    if C.get('bag'): pass
    if C.get('handbag'):
        bm=M(C['handbag'],.4,spec=.6); a=ARM[-1]
        Rb((-.5,-.1,-2.75),(.38,.14,.3),bm,par=a,bv=.05); Rb((-.5,-.1,-2.3),(.22,.02,.16),M(shade(C['handbag'],.7),.4),par=a,bv=.02); Rb((-.5,-.25,-2.7),(.06,.01,.06),M('#E6C25A',.3,metal=.9),par=a,bv=.01)
    if C.get('bowtie'):
        bm=M(C['bowtie'],.6)
        for s in (-1,1): Rb((s*.14,-.535,3.9),(.11,.02,.08),bm,bv=.02)
        Rb((0,-.545,3.9),(.04,.02,.05),bm,bv=.01)
    if C.get('highlights'):
        hm=M(C['highlights'],.5,spec=.4)
        for s in (-1,1): Hh((s*.63,-.15,.55),(.03,.12,.5),hm)
    return H
