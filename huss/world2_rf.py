# props + fx helpers for "Huss Huss"
def hide(o): o.scale=(0,0,0)
def hideH(H): H['root'].scale=(0,0,0)
def sunglasses(H):
    u=H['u']; e=empty((0,-.64*u,.7*u),H['head']); SG=M('#0B0C10',.08,metal=.3,spec=1.0)
    for s in (-1,1): obox((s*.25*u,0,0),(.2*u,.02*u,.13*u),SG,.03*u,e)
    obox((0,0,.06*u),(.58*u,.02*u,.025*u),SG,.01,e)
    for s in (-1,1): obox((s*.6*u,.3*u,.03*u),(.015*u,.3*u,.02*u),SG,.004,e)
    e['base']=tuple(e.location); return e
def glasses_off(e,k):
    """k 0..1: lower glasses forward and away, then vanish"""
    b=Vector(e['base']); e.location=tuple(b+Vector((0,-.25*k,-.35*k))); e.rotation_euler=(R(-40*k),0,0); e.scale=(1,1,1) if k<.98 else (0,0,0)
def inhaler(parent=None,loc=(0,0,0)):
    e=empty(loc,parent); m=M('#2E7DD8',.4); obox((0,0,0),(.03,.022,.06),m,.01,e); obox((0,-.035,-.045),(.025,.03,.018),m,.008,e); obox((0,0,.065),(.022,.015,.012),M('#E8ECF2',.4),.005,e); return e
def coat(H):
    """long trench coat tails"""
    u=H['u']; c=M(H['C']['jacket'],.75,kind='fabric'); root=H['root']
    for s in (-1,1): obox((s*.52*u,0,1.45*u),(.5*u,.54*u,.6*u),c,.05*u,root)
    obox((0,.53*u,1.45*u),(1.02*u,.02,.6*u),c,.02,root)
    obox((0,-.3*u,4.15*u),(.75*u,.3*u,.12*u),c,.05*u,root)
def breath(H,times,size=.07,n=4):
    u=H['u']
    for i,t0 in enumerate(times): puff((0,-.75*u,.3*u),t0,size=size,n=n,rise=-.05,life=.55,drift=(0,-.35,0),seed=i+3,parent=H['head'])
def shockwave(center,t0,r1=4.0,dur=.6,col='#FFFFFF'):
    n=48; vs=[]; fs=[]
    for i in range(n):
        a_=2*pi*i/n; vs+= [(math.cos(a_)*.9,math.sin(a_)*.9,0),(math.cos(a_),math.sin(a_),0)]
    for i in range(n): j=(i+1)%n; fs.append((2*i,2*j,2*j+1,2*i+1))
    o=omesh(vs,fs,M(col,.3,emit=2.0,alpha=.35),loc=center); o.scale=(0,0,0); o.visible_shadow=False
    def fn(o,t):
        q=(t-t0)/dur
        if q<=0 or q>=1: o.scale=(0,0,0); return
        r_=.2+r1*ease_out(q); o.scale=(r_,r_,1+2*(1-q))
        o.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value=.4*(1-q)
    fx.add(o,fn); return o
def jitter(H,t,amp=3.0,rate=37):
    H['root'].rotation_euler[1]=R(amp*math.sin(t*rate)); H['head'].rotation_euler[1]=R(amp*1.3*math.sin(t*rate*1.3+1))
def flee(H,t,hdg,speed=4.5,t0=0):
    d=max(0,t-t0)*speed; h=R(hdg); p=Vector((H['x'],H['y'],0))+Vector((math.sin(h),-math.cos(h),0))*d
    H['root'].location[0]=p.x; H['root'].location[1]=p.y; H['root'].rotation_euler[2]=h
    if t>t0: run(H,d+H['seed'],arm=70); H['arm'][1].rotation_euler=(R(-150+30*math.sin(t*15)),0,R(20)); H['arm'][-1].rotation_euler=(R(-150-30*math.sin(t*15)),0,R(-20))
def walker(H,start,hdg,speed,t,t0=0.0,arm=24):
    d=max(0,(t-t0))*speed; h=R(hdg); p=Vector(start)+Vector((math.sin(h),-math.cos(h),0))*d
    H['root'].location[0]=p.x; H['root'].location[1]=p.y; H['root'].rotation_euler[2]=h; walk(H,d+H['seed'],step=.55,arm=arm)
def people(specs,fn):
    return [av((x,y,0),rz,fn(i*3+7+(5 if kid else 0)) if not kid else fn(i*3+7,True),{'mouth':'smile'},name='p%d_%d'%(i,int(x*10))) for i,(x,y,rz,kid) in enumerate(specs)]
