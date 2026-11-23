# ================================================================ PICNIC KARACHI — approval package (reference sheets, environment references, visual test)
_KD=[('REF_SHY',8),('REF_SAH',8),('REF_EMA',8),('REF_ILS',8),('E_road',8),('E_venue',8),('E_dj',8),('E_night',8),('T_arrive',7.0)]
SHOTS={}; SEQ=[]; _t=0.0
for k,d in _KD: SEQ.append((k,round(_t,3))); _t+=d
END=round(_t,3); WS=[0.0]; WE=[0.0]
def TK(key): return [t for k,t in SEQ if k==key][0]
def wl(i,key): return 0.0
def we(i,key): return 0.0
def talk(H,t,a,b,key,rest='smile',rate=8.0,shapes=('O','flat','o','grin','flat')):
    t0=wl(a,key); t1=we(b,key)
    if t0<=t<t1: face(H,mouth=shapes[int((t-t0)*rate+H['seed']*3)%len(shapes)])
    else: face(H,mouth=rest)
    return t0<=t<t1
def handsdown(H): H['arm'][1].rotation_euler=(0,0,0); H['arm'][-1].rotation_euler=(0,0,0)
def hips(H,k=1.0): H['arm'][1].rotation_euler=(R(-15*k),R(-35*k),R(70*k)); H['arm'][-1].rotation_euler=(R(-15*k),R(35*k),R(-70*k))
def L(a,b,q): return a+(b-a)*q
def cl(x): return max(0.0,min(1.0,x))
def headpos(H):
    bpy.context.view_layer.update(); return H['head'].matrix_world.translation.copy()
def cf(H,d=2.2,lat=.35,dz=0.0,lens=30,fs=3.5,tgt_dz=-.05):
    hp_=headpos(H); a=H['root'].rotation_euler[2]; fwd=Vector((math.sin(a),-math.cos(a),0)); rt=Vector((math.cos(a),math.sin(a),0))
    pos=hp_+fwd*d+rt*lat+Vector((0,0,dz)); tg=hp_+Vector((0,0,tgt_dz)); camset(tuple(pos),tuple(tg),lens,fs,focus=tuple(hp_))
def ots(A,Bh,back=1.1,side=.45,up=.1,lens=32,fs=3.0):
    """over A's shoulder looking at Bh's face"""
    side=math.copysign(max(abs(side),.8),side); back=max(back,1.3); lens=max(lens,36)
    a_=headpos(A); b_=headpos(Bh); d=(b_-a_); d.z=0; d.normalize(); rt=Vector((d.y,-d.x,0))
    pos=a_-d*back+rt*side+Vector((0,0,up)); camset(tuple(pos),tuple(b_+Vector((0,0,-.1))),lens,fs,focus=tuple(b_))
def put_at(H,t,x,y,rz,z=.0):
    H['root'].location=(x,y,z+.008); H['z0']=z; stand(H,t); H['root'].location[2]=z+.008; H['root'].rotation_euler[2]=R(rz); blink(H,t)
def seat(H,t,x,y,rz,sh=.47,z=0.0):
    blink(H,t); H['root'].location=(x,y,z+.008); H['root'].rotation_euler=(0,0,R(rz)); H['z0']=z; sit(H,1,sh+z,90)
def breathe(H,t): H['root'].scale=(1,1,1+.006*math.sin(t*2.2+H['seed']))
def phone_ear(H,s=1): H['arm'][s].rotation_euler=(R(-150),0,R(-28*s))
def phone_front(H,s=1,k=1.0): H['arm'][s].rotation_euler=(R(-85*k),0,R(-18*s*k))
def gesture(H,t,s=1,amp=1.0): H['arm'][s].rotation_euler=(R(-45*amp+10*math.sin(t*4)),0,R(-25*s*amp))


# ---------------------------------------------------------------- registry for collision QC
PEOPLE=[]
_person0=person
def person(loc,rz,C,mouth='smile',name=None):
    H=_person0(loc,rz,C,mouth,name); H['nm']=name or 'p%d'%len(PEOPLE); PEOPLE.append(H); return H

# ---------------------------------------------------------------- arm poses (arm[1] is at +x; outward = -Y roll for arm[1], +Y for arm[-1])
def ARMV(H,a=150,sw=0.0): H['arm'][1].rotation_euler=(0,R(-a-sw),0); H['arm'][-1].rotation_euler=(0,R(a-sw),0)
def GEST(H,s,up=50,out=15): H['arm'][s].rotation_euler=(R(-up),0,R(out*s))
def side(H,s,a=85): H['arm'][s].rotation_euler=(0,R(-a*s),0)

def reset(H):
    H['arm'][1].rotation_euler=(0,0,0); H['arm'][-1].rotation_euler=(0,0,0); H['head'].rotation_euler=(0,0,0); H['root'].rotation_euler[0]=0; H['root'].rotation_euler[1]=0; H['root'].scale=(1,1,1)
def gsit(H,t,x,y,rz,z=0.0):
    """sit on the ground / mat, legs forward"""
    reset(H); blink(H,t); H['root'].location=(x,y,z+.008); H['root'].rotation_euler=(0,0,R(rz)); H['z0']=z; sit(H,1,.07+z,88); H['root'].location[2]+=.004*math.sin(t*2+H['seed'])
def carsit(H,t,x,y,rz=90,z=.78):
    reset(H); blink(H,t); H['root'].location=(x,y,z+.008); H['root'].rotation_euler=(0,0,R(rz)); H['z0']=z; sit(H,1,1.25,90)
def stroll(H,t,x0,y0,hdg,v,arm=22,step=.56):
    reset(H); h=R(hdg); d=v*t; H['z0']=0; H['root'].location=(x0+math.sin(h)*d,y0-math.cos(h)*d,.008); H['root'].rotation_euler=(0,0,h); walk(H,d+H['seed'],step=step*H['C'].get('h',1.0) if False else step,arm=arm); blink(H,t)
CAST=dict(SHY=('Shaheriyar',SHY,178),SAH=('Sahil',SAH,174),EMA=('Eman',EMA,160),ILS=('Ilsa',ILS,163))
def heroes():
    return {k:person((0,0,0),0,C,'smile',name=k.lower()) for k,(nm,C,cm) in CAST.items()}
def mat_people(det,seed=40,skip=()):
    r=random.Random(seed); G=[]
    for mi,(x,y,rot,side,i,j) in enumerate(det):
        n=r.choice((2,2,3,3)); a0=r.uniform(0,6.28); kidmat=r.random()<.25
        for q in range(n):
            a=a0+q*2*pi/n+r.uniform(-.25,.25); px=x+math.cos(a)*1.45; py=y+math.sin(a)*1.05; rz=math.degrees(math.atan2(x-px,-(y-py)))
            H=person((px,py,0),rz,plocal(seed+mi*11+q*3,kid=(kidmat and q==n-1)),'smile',name='m%d_%d'%(mi,q)); G.append((H,px,py,rz,r.random(),(x,y)))
    def upd(t,look=None):
        for k,(H,px,py,rz,ph,c) in enumerate(G):
            gsit(H,t,px,py,rz); s=math.sin(t*1.3+ph*9)
            if look is not None: look_at(H,look,.9,maxpitch=40); face(H,mouth='o' if k%3==0 else 'smile',brow=.05)
            elif s>.3: face(H,mouth=('O','flat','o','grin')[int(t*7+k)%4]); GEST(H,1,38+10*math.sin(t*4+k),14)
            else: face(H,mouth='grin' if k%4==0 else 'smile'); H['head'].rotation_euler[2]=R(12*math.sin(t*.8+ph*6))
    return upd
def set_day(P=None,mood='morning_s',expo=0.0):
    setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=120,cascades=4); bpy.context.scene.view_settings.exposure=float(os.environ.get('EXPO',str(expo)))

def SH_REF(view):
    KEY=view; nm,C,cm=CAST[view[4:]]; studio(); setup_render('day',res=PCT,samples=SAMPLES,shadow_dist=30,mist=False); bpy.context.scene.view_settings.exposure=-.2
    area((0,-6,5),700,(8,5),(1,1,1),rot=(R(55),0,0),shadow=False)
    H=person((0,0,0),0,C,'smile',name=view)
    B.box((1.75,.0,.5),(.02,.02,.5),M('#2B2C33',.5),0)
    def upd(t):
        i=int(t+.01); reset(H); put_at(H,0.3,0,0,(0,90,180,35,0,35,35,0)[min(i,7)]); blink(H,0,force=0); face(H,mouth='smile',brow=0,brow_r=0,eyes=1.0)
        hh=headpos(H).z
        if i<=3: camset((0,-6.6,1.15),(0,0,1.05),40,8.0)
        elif i==4: face(H,mouth='grin'); camset((.25,-2.3,hh+.02),(0,0,hh-.02),40,8.0)
        elif i==5: H['root'].rotation_euler[2]=R(35); walk(H,.42,step=.56,arm=24); camset((0,-6.6,1.15),(0,0,1.05),40,8.0)
        elif i==6: gsit(H,0,0,0,35); face(H,mouth='O',brow=.06,eyes=1.25); ARMV(H,60); camset((0,-5.2,1.0),(0,-.2,.75),40,8.0)
        else: face(H,mouth='shout',brow=.05,brow_r=14,eyes=1.2); GEST(H,1,70,10); camset((.25,-2.6,hh+.02),(0,0,hh-.1),40,8.0)
    return dict(upd=upd)
for v in ('REF_SHY','REF_SAH','REF_EMA','REF_ILS'): SHOTS[v]=(lambda v=v: SH_REF(v))

def SH_ROAD(view):
    KEY=view; V=road(); setup_render('hotday',res=PCT,samples=SAMPLES,shadow_dist=110,cascades=4); bpy.context.scene.view_settings.exposure=-.25
    JX,JY=0.0,-2.5; jeep(JX,JY,90,'#C9A45A'); Hs=heroes(); phone(Hs['ILS'],1)
    seats=dict(SAH='fr',SHY='fl',EMA='br',ILS='bl')
    def upd(t):
        for o,x0,li,ph in V:
            c=((t+ph)%6.0); o.location[0]=x0+.9*ease(cl((c-4.6)/1.2))+ .9*int((t+ph)//6.0)*0
        for k,H in Hs.items():
            sx,sy=JEEP_SEATS[seats[k]]; carsit(H,t,JX+sx,JY+sy)
        S_,Y_,E_,I_=Hs['SAH'],Hs['SHY'],Hs['EMA'],Hs['ILS']
        GEST(S_,1,62,-14); GEST(S_,-1,62,14); face(S_,mouth='strain',brow=.04,brow_r=12)
        Y_['head'].rotation_euler[2]=R(-38); face(Y_,mouth='shout',brow=.05,brow_r=-14,eyes=1.15); GEST(Y_,-1,55+8*math.sin(t*9),8)
        face(E_,mouth='O',brow=.06); side(E_,1,70); side(E_,-1,70); GEST(I_,1,58,-10); look_at(I_,(JX-1.2,JY+.6,1.9),.8); face(I_,mouth='smile')
        i=int(t+.01)
        if i==0: camset((-34,-12,17),(8,-1,1.5),24,8.0)
        elif i==1: camset((6.6,-2.5,3.0),(0,-2.5,2.25),22,6.0)
        elif i==2: cf(Y_,d=2.0,lat=-.35,lens=30)
        elif i==3: camset((-9,3.5,3.2),(1,-2.5,2.0),26,6.0)
        else: cf(I_,d=1.9,lat=.35,lens=30)
    return dict(upd=upd)
SHOTS['E_road']=lambda: SH_ROAD('E_road')

def SH_VENUE(view):
    KEY=view; night=(view=='E_night'); P=venue(night=night)
    if night:
        setup_render('nightc',res=PCT,samples=SAMPLES,shadow_dist=60); bpy.context.scene.view_settings.exposure=.9
        LG=lantern_groups(1000); hx,hy=P['hero']
        for (lx,ly) in ((hx,hy),(0,30),(8,45),(-14,52),(0,70),(14,24),(-20,28)): point((lx,ly,4.5),900,(1,.74,.42),.8,shadow=False)
        area((0,80,40),90000,(160,160),(1,.72,.4),rot=(0,0,0),shadow=False)
    else:
        set_day(); LG=[]
    Hs=heroes(); mp=mat_people(P['det']); hx,hy=P['hero']; SY=P['SY']
    DJ=person((0,SY+1.6,1.4),0,DJP,'grin',name='dj'); DN=[person((0,0,0),180,plocal(900+k*7),'grin',name='dn%d'%k) for k in range(9)]
    WK=[person((0,0,0),0,plocal(700+k*5),'smile',name='wk%d'%k) for k in range(6)]; hl=lantern_obj(1.0) if night else None
    order=('ILS','SHY','SAH','EMA'); xs=(-2.7,-.9,.9,2.7)
    def crowd(t):
        reset(DJ); put_at(DJ,t,0,SY+1.6,0,z=1.4); b=abs(math.sin(t*6.0)); DJ['root'].location[2]+=.05*b; GEST(DJ,1,48,-12); DJ['arm'][-1].rotation_euler=(0,R(150+10*math.sin(t*6)),0); face(DJ,mouth='grin')
        for k,H in enumerate(DN):
            x=-7+ (k%5)*3.4+(1.7 if k>=5 else 0); y=SY-6.5-(k//5)*3.0; reset(H); put_at(H,t,x,y,180); bb=abs(math.sin(t*6.0+k)); H['root'].location[2]+=.09*bb
            if k%2: ARMV(H,150,12*math.sin(t*6+k))
            else: GEST(H,1,75+15*math.sin(t*6+k),14); GEST(H,-1,75-15*math.sin(t*6+k),14)
            face(H,mouth='grin')
        for k,H in enumerate(WK):
            if k<3: stroll(H,t+k*3.1,(-2.2,2.4,0)[k],150-(k*37)%60,0,1.0)      # walking toward the gate (-y)
            else: stroll(H,t+k*2.3,(68.5,69.5,67.6)[k-3],20+(k-3)*31,180,.9)   # along the vendor row (+y)
    def upd(t):
        i=int(t+.01); mp(t,look=(0,80,40) if night else None); crowd(t)
        for H in Hs.values(): reset(H)
        if view=='E_dj':
            for k,nm in enumerate(order): put_at(Hs[nm],t,xs[k],SY-16,180)
            if i<4: camset((5.5,SY-9.5,2.3),(0,SY+.5,3.0),24,6.0)
            else: camset((60,50,3.0),(75,74,2.2),22,8.0)
            return
        if night:
            for k,(nm,(dx,dy,rz)) in enumerate(zip(order,((-1.3,-.75,-25),(-.45,.85,-170),(1.25,.8,150),(1.35,-.7,35)))):
                H=Hs[nm]; gsit(H,t,hx+dx,hy+dy,rz); look_at(H,(hx,hy+30,45),1.0,maxpitch=42); face(H,mouth='o' if k%2 else 'smile',brow=.06,eyes=1.15)
            for e,ph,sp,sw in LG: e.location=(sw*math.sin(t*.3+ph),.5*sw*math.cos(t*.23+ph),(t+20)*sp*.9+6*math.sin(ph))
            hl.location=(hx+.2,hy+.1,1.6+1.1*t); 
            if i<4: camset((1.5,6,2.2),(0,74,34),18,8.0)
            else: camset((hx+4.6,hy-4.4,1.3),(hx,hy+.4,2.3),24,6.0)
            return
        if i<=1:
            for k,nm in enumerate(order): stroll(Hs[nm],t,xs[k],-10.0+ (0 if k in (1,2) else .5),180,1.2)
            if i==0: camset((3.5,-21,2.0),(0,-2,6.2),20,8.0)
            else: camset((0,7,10.5),(0,78,0),18,8.0)
        elif i<=3:
            for k,nm in enumerate(order): stroll(Hs[nm],t,xs[k],9.0+(0 if k in (1,2) else .5),180,1.2); face(Hs[nm],mouth='O' if k%2 else 'grin',brow=.06,eyes=1.15)
            yy=9.0+1.2*t; camset((1.6,yy+6.5,1.75),(0,yy,1.7),24,6.0)
        else:
            for k,(nm,(dx,dy,rz)) in enumerate(zip(order,((-1.3,-.75,-25),(-.45,.85,-170),(1.25,.8,150),(1.35,-.7,35)))):
                H=Hs[nm]; gsit(H,t,hx+dx,hy+dy,rz); face(H,mouth='grin' if k%2 else 'smile')
            camset((hx+4.8,hy-4.6,2.4),(hx,hy,.9),24,6.0)
    return dict(upd=upd)
for v in ('E_venue','E_dj','E_night'): SHOTS[v]=(lambda v=v: SH_VENUE(v))

def SH_TEST(view):
    KEY=view; P=venue(night=False); set_day(); Hs=heroes(); mp=mat_people(P['det']); SY=P['SY']
    WK=[person((0,0,0),0,plocal(700+k*5),'smile',name='wk%d'%k) for k in range(4)]
    order=('ILS','SHY','SAH','EMA'); xs=(-2.7,-.9,.9,2.7)
    def upd(t):
        mp(t)
        for k,H in enumerate(WK): stroll(H,t+k*4.0,(-2.4,2.6,-1.0,1.2)[k],95-(k*23),0,1.0)
        y=-9.0+1.25*t
        for k,nm in enumerate(order):
            H=Hs[nm]; stroll(H,t,xs[k],-9.0+(0 if k in (1,2) else .45),180,1.25,arm=22); kk=cl((t-3.6)/.6)
            if kk>0: face(H,mouth='O' if k%2==0 else 'grin',brow=.06*kk,eyes=1+.2*kk); H['head'].rotation_euler[0]=R(-6*kk)
        q=ease(cl((t-1.2)/4.6)); camset((L(1.2,0,q),L(y-6.5,y-3.0,q)+0,L(2.3,9.5,q)),(0,L(y+1,62,q),L(1.6,0,q)),L(24,18,q),8.0)
    return dict(upd=upd)
SHOTS['T_arrive']=lambda: SH_TEST('T_arrive')
