# kit for "India vs Pakistan": generic pose helpers (lifted from the kvl shot files) + family staging for the two houses
def place(H,x,y,rz):
    H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(rz)
def crossed(H,k=1.0):
    H['arm'][1].rotation_euler=(R(-58*k),R(34*k),0); H['arm'][-1].rotation_euler=(R(-50*k),R(-34*k),0)
def handw(H,s): return H['arm'][s].matrix_world@Vector(hand_loc(H,s))
def speak(H,t,a,b,s=1,amp=1.0,base=-55,rate=7.0,gesture=True):
    g0,g1=wt(a,b); talk(H,t,g0,g1,rate=rate)
    if gesture and g0-T0-.1<=t<=g1-T0+.25: gest(H,t,s,amp,6.5,base)
def single(H,yaw=30,dist=3.0,dz=.12,tz=-.2,lens=32):
    h=Vector(hp(H)); a=H['root'].rotation_euler[2]+R(yaw); f=Vector((math.sin(a),-math.cos(a),0)); c=h+f*dist+Vector((0,0,dz))
    return (c.x,c.y,c.z),(h.x,h.y,h.z+tz),lens
def hands_head(H,k=1.0,dx=.95,dz=5.55,dy=-.05,only=None):
    m=root_mat(H); u=H['u']
    for s in ((1,-1) if only is None else (only,)): arm_to(H,s,m@Vector((s*dx*u,dy*u,dz*u)),k,base=(0,0,0))
def what_pose(H,k=1.0,t=0.0,amp=1.0):
    b=math.sin(t*9)*amp
    for s in (1,-1): H['arm'][s].rotation_euler=(R((-30+4*b)*k),R(-s*(60+5*b)*k),0)
def arms_up(H,k=1.0,t=0.0,spread=18,jig=0.0,only=None):
    for s in ((1,-1) if only is None else (only,)): H['arm'][s].rotation_euler=(R((-165+jig*math.sin(t*12+s))*k),R(s*spread*k),0)
def pointw(H,s,p,k=1.0): arm_to(H,s,p,k,base=tuple(H['arm'][s].rotation_euler))
def lap(H,k=1.0):
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-40*k),R(-s*4*k),0)
# ---------------------------------------------------------------- families
FAMC=dict(P=dict(d=ABBU,b=WALEED,m=AMMI,g=DADA),I=dict(d=PAPA,b=ROHAN,m=MUMMY,g=DADI))
FPOS=dict(d=(DADP,0.0),b=(BOYP,0.0),m=(MOMP,MOMRZ),g=(GRANP,GRANRZ))
SEAT=.58
def TVP(z0=0.0): return (0.0,-3.3,z0+1.6)
def family(side,z0=0.0,who='dbmg'):
    F=dict(side=side,z0=z0,who=who)
    for k in who:
        (x,y),rz=FPOS[k]; H=mk(FAMC[side][k],x,y,rz,side+k,z=z0); H['home']=(x,y,rz); H['k']=k; F[k]=H
    F['all']=[F[k] for k in who]; return F
def sitp(H,t,x=None,y=None,rz=None,seat=SEAT,lean=0.0,up=0.0):
    """seated at home position (or x,y,rz). up 0..1 = standing up from the seat"""
    hx,hy,hr=H['home']; hx=hx if x is None else x; hy=hy if y is None else y; hr=hr if rz is None else rz; f=fwd(H['home'][2])
    place(H,hx+f[0]*.85*up,hy+f[1]*.85*up,hr)
    sit(H,1-up,H['z0']+seat,legs=76); blink(H,t); H['root'].rotation_euler[0]=R(lean*(1-up)); H['root'].rotation_euler[1]=R(.8)*math.sin(t*.8+H['seed'])*(1-up)
    lap(H,1-up); H['head'].rotation_euler=(0,0,0)
def standp(H,t,x,y,rz):
    place(H,x,y,rz); H['root'].rotation_euler[0]=0; hstand(H,t); H['head'].rotation_euler=(0,0,0)
MOODF=dict(watch=dict(mouth='flat',brow=.01,brow_r=0,eyes=1.0),tense=dict(mouth='o',brow=.05,brow_r=0,eyes=1.15),calm=dict(mouth='smile',brow=0,brow_r=0,eyes=1.0),
           shock=dict(mouth='O',brow=.06,brow_r=0,eyes=1.25),glare=dict(mouth='frown',brow=-.03,brow_r=-14,eyes=.95),happy=dict(mouth='grin',brow=.04,brow_r=0,eyes=1.05),
           sad=dict(mouth='frown',brow=.03,brow_r=12,eyes=1.0),shout=dict(mouth='shout',brow=.05,brow_r=-8,eyes=1.15))
MOODL=dict(watch=3,tense=11,calm=0,shock=-3,glare=5,happy=2,sad=6,shout=6)
def mood(H,m): face(H,**MOODF[m])
def fam_idle(F,t,m='watch',look=None,skip=''):
    tv=TVP(F['z0']) if look is None else look
    for k in F['who']:
        if k in skip: continue
        H=F[k]; sitp(H,t,lean=MOODL.get(m,3)); look_at(H,tv,1.0,maxyaw=80,maxpitch=30); mood(H,m)
        if m=='tense': H['root'].location[2]+=.012*math.sin(t*17+H['seed'])        # knee-bounce nerves
def jump(H,t,t0,h=.45,dur=.5,n=1):
    """hop n times starting at t0 (adds to root z)"""
    q=(t-t0)/dur
    if 0<=q<n: H['root'].location[2]+=h*math.sin(pi*(q%1.0))
def cheer(H,t,t0,ph=0.0):
    """leap off the sofa with both arms up"""
    k=tl(t,t0,t0+.18)
    if k<=0: return
    sitp(H,t,up=k); arms_up(H,k,t,spread=20,jig=10); face(H,mouth='shout',brow=.06,eyes=1.15); H['root'].location[2]+=.3*abs(math.sin((t-t0)*9+ph))*k
def faintp(H,t,t0,x,y,rz=0.0,spr=28):
    """plank fall backward onto the floor (standing start), then lie"""
    k=min(1,max(0,(t-t0)/.34)); a=-90*(k*k); bo=math.sin(min(1,max(0,(t-t0-.34)/.25))*pi)*4*(k>=1)
    place(H,x,y,rz); legs0(H); H['root'].rotation_euler[0]=R(a+bo); H['root'].location[2]=H['z0']+.008+.55*H['u']*math.sin(R(-a))
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-10*k),R(-s*spr*k),0)
    blink(H,t,force=1 if k>.6 else 0); face(H,mouth='O',brow=.06,eyes=1.2); H['head'].rotation_euler=(0,0,0)
def cup_of(H,s=1): return chai(H,s,1.5)
def phone_of(H,s=1): return phone(H,s,1.5)
def phone_up(H,s=1,k=1.0,h=3.6,fw=1.25,sx=.3):
    """hold the phone up in front of the chest/face"""
    m=root_mat(H); u=H['u']; arm_to(H,s,m@Vector((s*sx*u,-fw*u,h*u)),k,base=tuple(H['arm'][s].rotation_euler))
def dh_cam(k=0.0,dz=0.0,lens=80):
    """dollhouse camera: both rooms stacked. k = small push-in 0..1"""
    camset((0,-16+1.6*k,UPZ/2+1.75+dz),(0,1.55,UPZ/2+1.75+dz),lens+0*k,8)
def lab(H): return H
