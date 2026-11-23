# ================================================================ PICNIC KARACHI — final film
_SJ=json.load(open('/home/claude/picnic/audio/seq.json')); SEQ=[(k,t) for k,t in _SJ['seq']]; END=_SJ['end']; SHOTS={}
WJ=json.load(open('/home/claude/picnic/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
LN={l_['key']:l_ for l_ in _SJ['lines']}
def TK(key): return [t for k,t in SEQ if k==key][0]
def wl(i,key): return WS[i]-TK(key)
def we(i,key): return WE[i]-TK(key)
def speaking(line,g):
    l_=LN[line]
    if l_['sp'] is None or g<l_['t0']-.05 or g>l_['t1']: return False
    for i in range(l_['i0'],l_['i1']+1):
        if WS[i]-.04<=g<=WE[i]+.06: return True
    return False
def say(H,t,KEY,line=None,rest='smile',shapes=('O','flat','o','grin','flat'),rate=9.0):
    g=t+TK(KEY); sp=speaking(line or KEY,g)
    face(H,mouth=shapes[int(g*rate+H['seed']*3)%len(shapes)] if sp else rest); return sp
def lt(line,off=0,KEY=None): return WS[LN[line]['i0']+off]-TK(KEY or line)      # start of a word of a line, relative to shot KEY
def lend(line,KEY=None): return LN[line]['t1']-TK(KEY or line)
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


SHOUT=('shout','O','shout','grin','O')
# ---------------------------------------------------------------- ROAD (scenes 1-2)
JY=-2.5
def SH_ROAD(view):
    KEY=view; V=road(); setup_render('hotday',res=PCT,samples=SAMPLES,shadow_dist=110,cascades=4); bpy.context.scene.view_settings.exposure=-.25
    JP=jeep(0,JY,90,'#C9A45A'); Hs=heroes(); S_,Y_,E_,I_=Hs['SAH'],Hs['SHY'],Hs['EMA'],Hs['ILS']
    ph=phone(I_,1); scr=img_plane(LOGO,(0,-.02,0),.14,.076,(0,-1,0),emit=1.4,parent=ph); bigph=empty((0,0,0)); obox((0,0,0),(.42,.03,.8),M('#15161A',.3),.05,bigph); obox((0,-.032,0),(.385,.004,.74),M('#69C0E3',.4,emit=1.0),.01,bigph); img_plane(LOGO,(0,-.04,.06),.7,.38,(0,-1,0),emit=1.3,parent=bigph); bigph.scale=(0,0,0)
    seats=dict(SAH='fr',SHY='fl',EMA='br',ILS='bl')
    JXv=[0.0]
    def cam4(q=0.0): camset((JXv[0]+L(5.0,4.5,q),JY+.15,L(3.75,3.55,q)),(JXv[0]-.55,JY,2.15),26,6.0)
    def jcf(H,sg=1,d=1.65,lens=34): cf(H,d=d,lat=.35*sg,dz=.12,lens=lens)
    def creep(g,li): c=(g+li*1.3)%5.0; return .7*(int((g+li*1.3)//5.0)+ease(cl((c-3.6)/1.2)))
    def upd(t):
        g=t+TK(KEY); q=ease(cl(t/DUR)); v=view; drive=(v=='V_drive'); gd=TK('V_drive') if drive else g
        for o,x0,li,ph_ in V:
            o.location[0]=x0+creep(min(g,gd),li)
            if drive and li==1 and x0>0: o.location[0]+=9.0*t*t
            elif drive: o.location[0]+=1.6*ease(cl((t-.3-.1*li)/2.2))
        jx=creep(min(g,gd),1)+(5.2*max(0,t-.35)**2 if drive else 0)
        JXv[0]=jx; JP.location[0]=jx
        for k,H in Hs.items():
            sx,sy=JEEP_SEATS[seats[k]]; carsit(H,g,jx+sx,JY+sy); face(H,mouth='smile',brow=0,brow_r=0,eyes=1.0)
        # idle driving poses
        GEST(S_,1,58,-14); GEST(S_,-1,58,14); GEST(I_,1,62,-12); look_at(I_,tuple(hand_pos(I_,1)) if False else (jx-1.3,JY+.75,1.95),.9,maxpitch=40); bigph.scale=(0,0,0)
        shake=.02*math.sin(g*23)
        for H in Hs.values(): H['root'].location[2]+=.006*math.sin(g*17+H['seed'])
        if v=='N_world':
            face(S_,mouth='strain',brow=.04,brow_r=12); face(Y_,mouth='frown',brow=.03,brow_r=-12); Y_['head'].rotation_euler[2]=R(20*math.sin(g*1.3)); face(E_,mouth='flat'); side(E_,1,60)
            qq=ease(cl(t/DUR)); camset((L(-46,-17,qq),L(-15,-9.5,qq),L(22,7.5,qq)),(L(6,1.5,qq)+jx,JY,L(1.5,2.2,qq)),L(22,26,qq),8.0)
        elif v=='C_horn':
            say(Y_,t,KEY,rest='frown',shapes=SHOUT); Y_['head'].rotation_euler[2]=R(-52); face(Y_,brow=.05,brow_r=-14,eyes=1.15); GEST(Y_,-1,60+8*math.sin(g*14),10); face(S_,mouth='strain',brow=.05,brow_r=14); face(E_,mouth='O'); side(E_,1,72); side(E_,-1,72)
            cam4(q)
        elif v=='C_main':
            say(S_,t,KEY,rest='strain',shapes=SHOUT); ARMV(S_,118,8*math.sin(g*16)); S_['head'].rotation_euler[2]=R(42); face(S_,brow=.06,brow_r=14,eyes=1.2); jcf(S_,-1)
        elif v=='C_kaun':
            say(Y_,t,KEY,rest='O',shapes=SHOUT); Y_['head'].rotation_euler[2]=R(-35+70*ease(cl(t/.9))); side(Y_,1,70); side(Y_,-1,70); face(Y_,brow=.06,brow_r=10); jcf(Y_,1)
        elif v=='C_poora':
            e1=lend(KEY)+.05; sp=say(E_,t,KEY,rest='grin',shapes=SHOUT); ARMV(E_,105,10*math.sin(g*13)); face(E_,brow=.06,eyes=1.2)
            for H in (S_,Y_): face(H,mouth='strain',brow=.05,brow_r=12)
            if t<e1: jcf(E_,1)
            else: kk=ease(cl((t-e1)/.7)); camset((jx+L(5,7,kk),-11.4,L(8.5,10.5,kk)),(jx,JY+1,1.6),24,8.0)
        elif v=='C_holiday':
            say(Y_,t,KEY,rest='frown',shapes=('O','flat','o','frown','flat'),rate=8); Y_['head'].rotation_euler[0]=R(-16*ease(cl(t/.8))); side(Y_,1,36+8*math.sin(g*2.4)); side(Y_,-1,36-8*math.sin(g*2.4)); face(Y_,brow=.05,brow_r=16)
            k3=cl((t-lt(KEY,8))/.2)
            if t<lt(KEY,5)-.1: cam4(q)
            else: jcf(Y_,1,d=L(1.9,1.55,ease(cl((t-lt(KEY,5))/2.0))))
        elif v=='C_real':
            e1=lend(KEY)+.1; say(S_,t,KEY,rest='flat',rate=7); face(S_,brow=-.02,brow_r=-8); S_['head'].rotation_euler[2]=R(38)
            if t<e1: jcf(S_,-1)
            else: kk=ease(cl((t-e1)/.4)); Y_['head'].rotation_euler[0]=R(24*kk); face(Y_,mouth='frown',brow=.05,brow_r=18); jcf(Y_,1)
        elif v=='D_look':
            e1=lt(KEY,4)-.12; say(I_,t,KEY,rest='grin',rate=8); face(I_,brow=.06,eyes=1.2)
            if t<e1: GEST(I_,1,62,-12); jcf(I_,-1)
            else:
                kk=ease(cl((t-e1)/.3)); GEST(I_,1,L(62,96,kk),-8); bpy.context.view_layer.update(); hp_=hand_pos(I_,1); bigph.scale=(1,1,1); bigph.location=(jx+.1,JY+.2,2.75); bigph.rotation_euler=(R(-6),0,R(90+8*math.sin(g*2)))
                camset((jx+2.6,JY+.2,2.8),(jx+.1,JY+.2,2.75),34,5.0)
        elif v=='D_park':
            say(Y_,t,KEY,rest='frown',rate=8); Y_['head'].rotation_euler[2]=R(48); face(Y_,brow=-.02,brow_r=-10); GEST(Y_,1,40,12); jcf(Y_,1)
        elif v=='D_normal':
            say(I_,t,KEY,rest='smirk',rate=8); face(I_,brow=.03,brow_r=8); GEST(I_,-1,48+6*math.sin(g*5),12); jcf(I_,-1)
        elif v=='D_food':
            say(S_,t,KEY,rest='o',rate=8); S_['head'].rotation_euler[2]=R(55); face(S_,brow=.06,eyes=1.3); jcf(S_,-1)
        elif v=='D_exp':
            say(I_,t,KEY,rest='grin',rate=8); face(I_,brow=.05,eyes=1.15); GEST(I_,-1,55,14); jcf(I_,-1)
        elif v=='D_expb':
            say(I_,t,KEY,line='D_exp',rest='grin',rate=8); GEST(I_,-1,55+10*math.sin(g*4),14); face(I_,brow=.05)
            S_['head'].rotation_euler[2]=R(58); Y_['head'].rotation_euler[2]=R(-58); face(S_,mouth='o',brow=.05); face(Y_,mouth='flat',brow=.03); look_at(E_,headpos(I_),.9); face(E_,mouth='smile',brow=.04)
            cam4(q)
        elif v=='D_lant':
            say(E_,t,KEY,rest='o',rate=8); look_at(E_,headpos(I_),.7); face(E_,brow=.06,eyes=1.3); side(E_,1,50); jcf(E_,1)
        elif v=='D_int':
            e1=lend(KEY)+.05; say(S_,t,KEY,rest='grin',rate=8); S_['head'].rotation_euler[2]=R(50*(1-ease(cl((t-e1)/.3)))); face(S_,brow=.04,brow_r=10)
            if t<e1: jcf(S_,-1)
            else: cam4(1.0)
        else:  # V_drive
            for H in Hs.values(): face(H,mouth='grin',brow=.05)
            ARMV(E_,120,8*math.sin(g*9)); camset((creep(gd,1)+L(-13,-10,q),JY-5.5,L(5.5,4.2,q)),(jx+2,JY,1.8),24,8.0)
    return dict(upd=upd)
for v in ('N_world','C_horn','C_main','C_kaun','C_poora','C_holiday','C_real','D_look','D_park','D_normal','D_food','D_exp','D_expb','D_lant','D_int','V_drive'): SHOTS[v]=(lambda v=v: SH_ROAD(v))

# ---------------------------------------------------------------- VENUE (scenes 3-6)
NIGHT=('V_lanterns','L_peace','L_yes','L_stay','L_needed','F_n1d','F_n2','F_n2b','F_req','F_what','F_kal','F_ghar','F_vouch','F_last')
ORDER=('ILS','SHY','SAH','EMA'); XS=(-2.7,-.9,.9,2.7)
MATPOS=dict(ILS=(-1.45,-.8,-28),SHY=(-.55,.95,-165),SAH=(1.4,.85,152),EMA=(1.5,-.75,38))
def SH_VENUE(view):
    KEY=view; night=view in NIGHT; dusk=(view=='V_dusk'); P=venue(night=night,dusk=dusk); hx,hy=P['hero']; SY=P['SY']; LG=[]
    if night:
        setup_render('nightc',res=PCT,samples=SAMPLES,shadow_dist=60); bpy.context.scene.view_settings.exposure=1.0; LG=lantern_groups(1000)
        for (lx,ly) in ((hx,hy),(0,30),(9,42),(-15,50),(0,66),(14,24),(-20,30)): point((lx,ly,4.6),1100,(1,.74,.42),.8,shadow=False)
        area((0,80,45),120000,(170,170),(1,.72,.4),shadow=False)
    elif dusk:
        setup_render('dusk',res=PCT,samples=SAMPLES,shadow_dist=110,cascades=4); bpy.context.scene.view_settings.exposure=.55
        for (lx,ly) in ((hx,hy),(0,30),(9,42),(-15,50)): point((lx,ly,4.6),500,(1,.78,.5),.8,shadow=False)
    elif view=='V_sunset': setup_render('golden',res=PCT,samples=SAMPLES,shadow_dist=120,cascades=4); bpy.context.scene.view_settings.exposure=.1
    else: set_day()
    jeep(-24,-9,180,'#C9A45A'); Hs=heroes(); S_,Y_,E_,I_=Hs['SAH'],Hs['SHY'],Hs['EMA'],Hs['ILS']; mp=mat_people(P['det'])
    DJ=person((0,SY+1.6,1.4),0,DJP,'grin',name='dj'); DN=[person((0,0,0),180,plocal(900+k*7),'grin',name='dn%d'%k) for k in range(9)]
    WK=[person((0,0,0),0,plocal(700+k*5),'smile',name='wk%d'%k) for k in range(6)]; TN=[person((0,0,0),90,plocal(800+k*9),'smile',name='tn%d'%k) for k in range(6)]
    hl=[lantern_obj(1.0) for _ in range(3)] if (night or dusk) else []
    def crowd(g):
        reset(DJ); put_at(DJ,g,0,SY+1.6,0,z=1.4); b=abs(math.sin(g*6.0)); DJ['root'].location[2]+=.05*b; GEST(DJ,1,48,-12); DJ['arm'][-1].rotation_euler=(0,R(150+10*math.sin(g*6)),0); face(DJ,mouth='grin')
        for k,H in enumerate(DN):
            x=-7+(k%5)*3.4+(1.7 if k>=5 else 0); y=SY-6.5-(k//5)*3.0; reset(H); put_at(H,g,x,y,180); bb=abs(math.sin(g*6.0+k)); H['root'].location[2]+=.09*bb
            if k%2: ARMV(H,150,12*math.sin(g*6+k))
            else: GEST(H,1,75+15*math.sin(g*6+k),14); GEST(H,-1,75-15*math.sin(g*6+k),14)
            face(H,mouth='grin')
        for k,H in enumerate(WK):
            if k<3: stroll(H,(g+k*23)%68,(-2.3,2.4,.1)[k],148-(k*2),0,1.0)
            else: stroll(H,(g+k*23)%60,(64.2,65.4,63.2)[k-3],18+(k-3)*9,180,.9)
        for k,H in enumerate(TN):
            reset(H); put_at(H,g,71.2,22+13.0*(k*2 if k<5 else 9)+(.9 if k%2 else -.9),90); gaze_idle(H,g)
            if k%2==0: GEST(H,1,50+8*math.sin(g*3+k),10); face(H,mouth=('O','smile','o','grin')[int(g*5+k)%4])
    def onmat(g,up=None):
        for nm,(dx,dy,rz) in MATPOS.items():
            H=Hs[nm]; gsit(H,g,hx+dx,hy+dy,rz); face(H,mouth='smile',brow=.02,brow_r=0,eyes=1.0)
            if up is not None: look_at(H,up,1.0,maxpitch=20); face(H,brow=.05,eyes=1.12)
    def abreast(g,y,v=1.2,face_=None):
        for k,nm in enumerate(ORDER): stroll(Hs[nm],g,XS[k],y+(0 if k in (1,2) else .45),180,v); face(Hs[nm],mouth='smile',brow=.02,brow_r=0,eyes=1.0)
    SKY=(hx+2,hy+38,44)
    def mcf(H,sg=1,d=2.0,lens=32): cf(H,d=d,lat=1.05*sg,dz=.5,lens=lens,tgt_dz=-.12)
    def upd(t):
        g=t+TK(KEY); q=ease(cl(t/DUR)); v=view; mp(g,look=(0,80,42) if night else None); crowd(g)
        for H in Hs.values(): reset(H)
        for e,ph,sp,sw in LG: e.location=(sw*math.sin(g*.3+ph),.5*sw*math.cos(g*.23+ph),((g*sp*.9+ph*9)%34)-6+3*math.sin(ph))
        for k,o in enumerate(hl): o.scale=(0,0,0)
        if v=='V_gate':
            abreast(t,-17.5,1.25); camset((L(5.5,4.5,q),L(-27.5,-25.5,q),L(1.5,1.8,q)),(0,-2,L(5.6,6.0,q)),20,8.0)
        elif v=='V_reveal':
            abreast(t,-7.0,1.25); y=-7.0+1.25*t
            for k,nm in enumerate(ORDER):
                kk=cl((t-2.4)/.6); face(Hs[nm],mouth='O' if k%2==0 else 'grin',brow=.06*kk,eyes=1+.2*kk)
            qq=ease(cl((t-.5)/3.6)); camset((L(1.2,0,qq),L(y-6.5,y-2.5,qq),L(2.3,10.0,qq)),(0,L(y+1,66,qq),L(1.6,0,qq)),L(24,18,qq),8.0)
        elif v=='A_space':
            abreast(0,6.0,0)
            for nm in ORDER: reset(Hs[nm]); put_at(Hs[nm],g,XS[ORDER.index(nm)],6.0+(0 if nm in ('SHY','SAH') else .45),180); look_at(Hs[nm],(XS[ORDER.index(nm)]*4,60,2),.8); face(Hs[nm],mouth='grin',brow=.05,eyes=1.1)
            say(Y_,t,KEY,rest='O',shapes=SHOUT); side(Y_,1,78); side(Y_,-1,78); face(Y_,brow=.06); cf(Y_,d=L(3.0,2.5,q),lat=.55,dz=-.35,lens=28)
        elif v=='A_music':
            abreast(t,7.0,1.1); say(S_,t,KEY,rest='grin',rate=8); GEST(S_,1,62+8*math.sin(g*5),16); face(S_,brow=.05); look_at(Y_,headpos(S_),.6); y=7.0+1.1*t
            camset((5.2,y+5.8,1.85),(.2,y,1.72),26,6.0)
        elif v=='V_through':
            for k,nm in enumerate(ORDER): stroll(Hs[nm],t,XS[k],13.0+(0 if k in (1,2) else .45),180,1.0)
            yy=L(15.5,31,q); camset((-4.9,yy,L(1.9,1.6,q)),(-12.5,yy+7.5,.75),24,5.6)
        elif v=='V_dj':
            onmat(g); camset((L(2.9,2.3,q),SY-L(5.2,4.2,q),L(1.7,2.0,q)),(0,SY+.9,3.1),22,6.0)
        elif v=='P_nothing':
            onmat(g); say(I_,t,KEY,rest='grin',rate=8); side(I_,1,40); side(I_,-1,40); I_['root'].rotation_euler[0]=R(-8); mcf(I_,1)
        elif v=='P_qual':
            onmat(g); say(S_,t,KEY,rest='smirk',rate=8); S_['root'].rotation_euler[0]=R(-16); ARMV(S_,160); face(S_,brow=.03,brow_r=10,eyes=.8); mcf(S_,-1)
        elif v=='P_things':
            onmat(g); x_,y_,rz_=MATPOS['EMA']; reset(E_); put_at(E_,g,hx+3.6,hy-.6,90); say(E_,t,KEY,rest='grin',rate=8); GEST(E_,1,82,18); face(E_,brow=.06,eyes=1.2)
            for nm in ('ILS','SHY','SAH'): look_at(Hs[nm],headpos(E_),.8)
            cf(E_,d=L(2.9,2.5,q),lat=.6,lens=28)
        elif v=='V_explore':
            for k,nm in enumerate(('EMA','ILS')): stroll(Hs[nm],t,(69.0,67.1)[k],30.0+k*.3,180,1.15); look_at(Hs[nm],(75,34+1.15*t+6,2.2),.9); face(Hs[nm],mouth='grin',brow=.05)
            for k,nm in enumerate(('SAH','SHY')): stroll(Hs[nm],t,(69.2,67.3)[k],27.2+k*.3,180,1.15); look_at(Hs[nm],(75,31+1.15*t+6,2.2),.9); face(Hs[nm],mouth='o' if k else 'grin',brow=.05)
            GEST(E_,-1,70,16); y=30+1.15*t; camset((65.8,y+7.2,1.9),(70.2,y-.5,1.75),24,6.0)
        elif v=='F_n1':
            onmat(g); camset((L(-30,-18,q),L(34,50,q),L(17,15,q)),(L(-4,6,q),L(70,84,q),0),20,8.0)
        elif v=='F_n1b':
            onmat(g); camset((L(-5.5,-4.2,q),SY+1.2,3.2),(.4,SY+.6,2.9),26,6.0)
        elif v=='F_n1c':
            onmat(g); camset((64,L(34,44,q),3.4),(75,L(52,62,q),2.2),22,8.0)
        elif v=='V_sunset':
            onmat(g); camset((L(10,7,q),L(4,7,q),L(5.5,8.5,q)),(L(-12,-14,q),70,L(4,6,q)),20,8.0)
        elif v=='V_dusk':
            onmat(g); kk=ease(cl((t-.8)/1.2)); hl[0].scale=(1,1,1); hl[0].location=(hx+.25,hy+.05,.45+.9*kk)
            for nm in ORDER: look_at(Hs[nm],(hx+.25,hy+.05,.6+.9*kk),1.0); face(Hs[nm],mouth='o' if nm in ('EMA','SAH') else 'smile',brow=.05)
            GEST(Y_,1,58,-18); GEST(I_,-1,58,18); camset((hx+L(4.2,3.6,q),hy-L(4.0,3.4,q),L(1.5,1.9,q)),(hx+.2,hy+.1,1.25),26,4.0)
        elif v=='V_lanterns':
            onmat(g,up=SKY)
            for k,o in enumerate(hl): o.scale=(1,1,1); o.location=(hx+(2.6,-6.5,5.8)[k],hy+(3.2,5.0,-4.6)[k],1.4+1.5*t+.3*k)
            kk=ease(cl((t-.3)/3.2)); camset((hx+L(5.5,3.5,kk),hy-L(7.5,6.0,kk),L(1.5,1.2,kk)),(hx-1+0*kk,hy+L(3,34,kk),L(1.6,40,kk)),L(24,17,kk),8.0)
        elif v in ('L_peace','L_yes','L_stay','L_needed'):
            onmat(g,up=SKY); H={'L_peace':Y_,'L_yes':I_,'L_stay':S_,'L_needed':E_}[v]; e1=lend(KEY)+.1
            say(H,t,KEY,rest='smile',shapes=('o','flat','O','smile','flat'),rate=7.5); face(H,brow=.05,eyes=1.12)
            if v=='L_stay': S_['root'].rotation_euler[0]=R(-14); ARMV(S_,160)
            if v=='L_needed' and t>e1: kk=ease(cl((t-e1)/.8)); camset((hx+L(0,.4,kk),hy-L(6.5,8.5,kk),L(1.0,.9,kk)),(hx,hy+10,L(9,14,kk)),18,8.0)
            else: mcf(H,1 if v in ('L_peace','L_needed') else -1,d=L(2.2,1.9,q))
        elif v=='F_n1d':
            onmat(g,up=SKY); camset((L(-3,0,q),L(12,16,q),2.2),(0,L(70,80,q),L(30,36,q)),18,8.0)
        elif v=='F_n2':
            onmat(g,up=SKY); camset((hx+L(1.0,.5,q),hy-L(5.6,6.8,q),L(3.0,3.5,q)),(hx,hy+10,L(6,9,q)),20,8.0)
        elif v=='F_n2b':
            onmat(g,up=SKY); camset((hx+L(6,9,q),hy-L(7,12,q),L(4,10,q)),(hx-4,hy+30,L(6,12,q)),20,8.0)
        elif v in ('F_req','F_what','F_kal','F_ghar'):
            onmat(g); H={'F_req':Y_,'F_what':S_,'F_kal':Y_,'F_ghar':I_}[v]; e1=lend(KEY)+.1
            for nm in ORDER:
                if Hs[nm] is not H: look_at(Hs[nm],headpos(Y_ if v!='F_ghar' else I_),.85)
            say(H,t,KEY,rest='smile' if v!='F_ghar' else 'grin',shapes=SHOUT if v=='F_ghar' else ('O','flat','o','grin','flat'),rate=8)
            if v=='F_req': GEST(Y_,1,56,10)
            if v=='F_kal': face(Y_,mouth=None,brow=.05); side(Y_,1,40); side(Y_,-1,40)
            if v=='F_ghar':
                ARMV(I_,118,8*math.sin(g*14)); face(I_,brow=.06,eyes=1.2)
                if t>e1:
                    for nm in ORDER: face(Hs[nm],mouth='grin',brow=.05); Hs[nm]['root'].location[2]+=.012*abs(math.sin(g*11+ORDER.index(nm)))
                    camset((hx+4.6,hy-4.6,2.3),(hx,hy+.2,1.1),24,5.0); 
                else: mcf(I_,1)
            else: mcf(H,1 if H is Y_ else -1)
        elif v=='F_vouch':
            onmat(g,up=SKY); camset((L(4,2,q),L(8,11,q),L(3.0,4.5,q)),(0,L(60,70,q),L(22,30,q)),18,8.0)
        else:  # F_last
            onmat(g,up=SKY); camset((hx-3.1,hy-L(8,6.5,q),L(2.7,2.1,q)),(hx-1,hy+L(14,30,q),L(10,44,q)),L(22,18,q),8.0)
    return dict(upd=upd)
for v in ('V_gate','V_reveal','A_space','A_music','V_through','V_dj','P_nothing','P_qual','P_things','V_explore','F_n1','F_n1b','F_n1c','V_sunset','V_dusk')+NIGHT: SHOTS[v]=(lambda v=v: SH_VENUE(v))
SHOTS['END']=lambda: SH_VENUE('F_last')
