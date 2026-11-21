SHOTS={}
WS=[w_['t0'] for w_ in json.load(open('/home/claude/rf/audio/words.json'))]
END=103.19
SEQ=[('L_copy', 0.0), ('L_stop', 3.28), ('L_wash', 5.96), ('L_smile', 9.02), ('L_face', 10.9), ('L_back', 12.6), ('L_write', 15.54), ('L_laugh', 21.22), ('ST_leave', 24.08), ('ST_win', 25.5), ('ST_pud', 28.56), ('ST_bus', 29.46), ('ST_no', 30.92), ('H_door', 34.08), ('H_clk1', 35.72), ('H_clk2', 37.3), ('H_mom', 39.22), ('H_sis', 41.32), ('H_mir', 44.04), ('H_bdoor', 47.3), ('B_wide', 48.46), ('B_mir', 51.28), ('B_hit', 54.2), ('B_face', 57.36), ('H_empty', 58.88), ('H_copies', 61.04), ('NB', 63.22), ('B_creak', 67.3), ('B_down', 69.4), ('B_hood', 71.44), ('B_cface', 72.3), ('B_smile', 73.4), ('B_turn', 74.2), ('B_look', 76.42), ('B_point', 77.8), ('B_shadow', 81.14), ('B_window', 82.08), ('B_rip', 83.94), ('B_crack', 86.18), ('B_water', 89.38), ('B_hug', 91.38), ('H_tick', 94.34), ('H_thanks', 97.14), ('H_late', 99.7)]
def mirror_pose(Hr,Hs):
    """make reflection avatar Hs copy real avatar Hr across the plane y=0 (arms/legs swapped)"""
    r=Hr['root']; q=Hs['root']; q.location=(r.location[0],-r.location[1],r.location[2])
    q.rotation_euler=(r.rotation_euler[0],-r.rotation_euler[1],pi-r.rotation_euler[2])
    for s in (1,-1):
        a=Hr['arm'][s].rotation_euler; Hs['arm'][-s].rotation_euler=(a[0],-a[1],-a[2])
        l=Hr['leg'][s]; Hs['leg'][-s].rotation_euler=(l.rotation_euler[0],-l.rotation_euler[1],-l.rotation_euler[2]); Hs['leg'][-s].location[2]=l.location[2]
    h=Hr['head'].rotation_euler; Hs['head'].rotation_euler=(h[0],-h[1],-h[2])
def hide(o): o.scale=(0,0,0)
def hideH(H): H['root'].scale=(0,0,0)

# =================================================================== LOCKER ROOM
def LK_(view):
    G=locker_room(); FL=point((.6,.5,2.3),0,(.9,.97,1.0),.3,shadow=False); setup_dark('#0A1420',.3,res=PCT,samples=SAMPLES,bloom=.05)
    H=av((0,-1.05,0),180,MARCUS,{'mouth':'flat'},name='marcus'); Rf=av((0,1.05,0),0,MARCUS,{'mouth':'flat'},name='marcusR')
    WR=M('#F4FBFF',.6,emit=.25,alpha=.8); txt=[]
    if view=='write':
        for i,(wd,z) in enumerate((("DON'T",2.52),("GO",2.14),("HOME",1.76))): txt.append(text(wd,(.5,-.012,z),(0,-1,0),.3,WR,ex=.002))
        fog=ocyl((.5,-.008,2.14),.72,.002,M('#EAF6FA',.9,emit=.12,alpha=.42),sc=(1.05,1,1),seg=40); fog.name='glass_fog'
    if view=='wash':
        tap=ocyl((0,-.27,1.16),.012,.2,M('#CFEFFF',.1,emit=.6,alpha=.55),rot=(0,0,0),seg=8); tap.name='glass_tap'
        drops=[oico((0,0,0),.022,M('#CFEFFF',.1,emit=.5,alpha=.7),sub=1) for i in range(10)]
    def wave(Hx,t):
        stand(Hx,t); k=ease((t-.15)/.3); Hx['arm'][1].rotation_euler=(R(-150*k),0,R(16*k+14*k*math.sin(t*11))); Hx['arm'][-1].rotation_euler=(R(-6),0,R(-4))
        q=ease((t-1.45)/.3); sw=math.sin((t-1.45)*5.2)*q; Hx['root'].rotation_euler[1]=R(9)*sw; Hx['head'].rotation_euler=(0,R(8)*sw,0)
        face(Hx,mouth='grin' if t>.25 else 'smile',brow=.05)
    def upd(t):
        blink(H,t); blink(Rf,t)
        if view=='copy':
            wave(H,t); mirror_pose(H,Rf); face(Rf,mouth='grin' if t>.25 else 'smile',brow=.05)
            q=ease(t/DUR); H['root'].location[1]=-.9; mirror_pose(H,Rf); camset((3.45,-.6,1.62),(0,-.05,1.52),22+1.0*q,8.0)
        elif view=='stop':
            wave(H,2.75); mirror_pose(H,Rf); face(Rf,mouth='flat',brow=-.02); Rf['head'].rotation_euler=(R(3),0,0); Rf['root'].rotation_euler[1]=0; blink(Rf,0,0)
            k=ease((t-.75)/.35); wave(H,2.75+t)
            if k>0:
                H['arm'][1].rotation_euler=(R(-150*(1-k)-20*k),0,R(16*(1-k)+8*k)); H['root'].rotation_euler[1]=0; H['head'].rotation_euler=(0,0,0); face(H,mouth='flat' if k<1 else 'o',brow=.1*k,eyes=1+.15*k)
                H['root'].rotation_euler[0]=R(5)*ease((t-1.3)/.4)
            q=ease(t/DUR); camset((1.1,-2.75+.25*q,2.2),(-.1,.8,1.86),44+3*q,4.0,focus=(0,1.05,1.9))
        elif view=='wash':
            up=ease((t-1.75)/.4)
            H['root'].location=(0,-1.2,.008); legs0(H); H['root'].rotation_euler=(R(10)*(1-up),0,R(180)); H['head'].rotation_euler=(R(12+6*math.sin(t*9))*(1-up),0,0)
            sc_=math.sin(t*9)*(1-up)
            for s in (1,-1): H['arm'][s].rotation_euler=(R(-78-16*sc_)*(1-up)+R(-12)*up,0,R(-s*(34+8*sc_))*(1-up))
            face(H,mouth='flat',brow=0); blink(H,t,1 if t<2.1 else None)
            mirror_pose(H,Rf); blink(Rf,t,1 if t<2.1 else None)
            for i,o in enumerate(drops):
                ph=(t*1.9+i*.37)%1.0; a=i*2.4
                if up>.2: hide(o)
                else: o.scale=(1,1,1.5); o.location=(.2*math.cos(a)*(.3+ph),-.7+.1*math.sin(a),1.72-.62*ph*ph)
            FL.data.energy=60; hideH(Rf); hide(G); camset((.55,.8,1.8),(0,-1.0,1.6),34,8.0)
        elif view=='smile':
            stand(H,t); arms(H,-8,0,-4,-8,0,4); face(H,mouth='flat',brow=.02); look_at(H,(0,1.05,1.9),.9)
            mirror_pose(H,Rf); sm=ease((t-.3)/.25)
            if sm>0: face(Rf,mouth='grin' if sm>.5 else 'smile',brow=.05); Rf['head'].rotation_euler[0]=R(-4*sm)
            else: face(Rf,mouth='flat',brow=.02)
            q=ease(t/DUR); camset((1.5,-3.4+.3*q,2.05),(-.2,.6,1.74),40+4*q,4.0,focus=(0,1.05,1.9))
        elif view=='face':
            stand(H,t); arms(H,-8,0,-4,-8,0,4); k=ease((t-.35)/.3); face(H,mouth='flat',brow=.02+.04*k,eyes=1+.15*k); look_at(H,(0,1.05,1.9),.9)
            FL.data.energy=60; hideH(Rf); hide(G); q=ease(t/DUR); camset((.45-.1*q,.75,1.9),(0,-1.2,1.86),45+5*q,8.0,focus=(0,-1.1,1.9))
        elif view=='back':
            stand(H,t); k=ease((t-.2)/.55); H['root'].location[1]=-1.05-.7*k; H['root'].location[2]+=.03*math.sin(pi*k); face(H,mouth='o',brow=.1,eyes=1.15); arms(H,-24*k,0,-12*k,-24*k,0,12*k); look_at(H,(0,1.05,1.9),.9)
            Rf['root'].location=(0,1.05,.008); Rf['root'].rotation_euler=(0,0,0); legs0(Rf); arms(Rf,-6,0,-3,-6,0,3); face(Rf,mouth='grin',brow=.05); Rf['head'].rotation_euler=(R(-3),0,R(6)*ease((t-1.2)/.4))
            camset((1.9,-4.3,2.1),(-.25,.6,1.7),34,5.6,focus=(0,1.05,1.9))
        elif view=='write':
            H['root'].location=(0,-1.75,.008); legs0(H); arms(H,-24,0,-12,-24,0,12); face(H,mouth='o',brow=.1,eyes=1.15); look_at(H,(.5,0,2.1),.9)
            Rf['root'].location=(0,1.05,.008); Rf['root'].rotation_euler=(R(-8)*ease(t/.4)*(1-ease((t-1.3)/.4)),0,0); legs0(Rf)
            br=ease(t/.35)*(1-ease((t-1.25)/.3)); face(Rf,mouth='O' if br>.5 else 'flat',brow=0); Rf['head'].rotation_euler=(R(-10)*br,0,R(-14))
            f=ease((t-.35)/.9); fog.scale=(1.05*f,1,f) if f>0 else (0,0,0)
            ws=tuple(WS[i_]-T0 for i_ in (48,49,50)); wr=ease((t-1.5)/.4); tz=2.52; tx=.5
            for i,w0 in enumerate(ws):
                kk=ease((t-(w0-.45))/.35)
                if i>0: tz=L(tz,2.52-.38*i,kk)
            tx=.5+.25*math.sin(t*13)*(1 if any(w0-.3<t<w0+.25 for w0 in ws) else .15)
            arm_to(Rf,-1,(tx,.02,tz),wr) if wr>0 else arms(Rf,-6,0,-3,-6,0,3)
            for i,o in enumerate(txt):
                kk=ease((t-ws[i]+.12)/.3); o.scale=(kk,kk,kk) if kk>0 else (0,0,0)
            q=ease(t/DUR); camset((-1.75+.2*q,-2.9+.3*q,2.02),(.38,.3,2.1),38+3*q,8.0,focus=(0,0,2.1))
        elif view=='laugh':
            stand(H,t); b=abs(math.sin(t*11)); k=1-ease((t-1.75)/.3)
            H['root'].location[2]+=.025*b*k; H['head'].rotation_euler=(R(-10*k-4*b*k),0,0); face(H,mouth='grin',brow=.06,eyes=.75 if k>.5 else 1)
            w=ease((t-.9)/.25)*k; H['arm'][1].rotation_euler=(R(-95*w),0,R(20*w+18*w*math.sin(t*12))); H['arm'][-1].rotation_euler=(R(-8),0,R(-4))
            tr=ease((t-1.75)/.6); H['root'].rotation_euler[2]=R(180-125*tr)
            FL.data.energy=60; hideH(Rf); hide(G); camset((.55,.75,1.9),(0,-1.2,1.8),40,8.0,focus=(0,-1.1,1.9))
    return dict(upd=upd)
for _v in ('copy','stop','wash','smile','face','back','write','laugh'): SHOTS['L_'+_v]=(lambda v=_v: LK_(v))

# =================================================================== RAINY STREET
def ST_(view):
    pud=(1.6,-1.4,1.5,.7) if view=='pud' else None
    G=street(puddle=pud); setup_dark('#070B18',.6,res=PCT,samples=SAMPLES,ssr=True,bloom=.09,mist=('#141C34',8,45,.55)); rain(0,-3,box=(9,6,9))
    H=av((-2.4,-1.25,.07),90,MARCUS,{'mouth':'flat'},name='marcus'); Rf=av((0,1.25,.07),90,MARCUS,{'mouth':'flat'},name='marcusR')
    pk=obox((0,.62*H['u'],3.0*H['u']),(.7*H['u'],.3*H['u'],.8*H['u']),M('#16909E',.7,kind='fabric'),.06,H['root'])
    pk2=obox((0,.62*H['u'],3.0*H['u']),(.7*H['u'],.3*H['u'],.8*H['u']),M('#16909E',.7,kind='fabric'),.06,Rf['root'])
    if view=='bus': BU=bus(); BL=point((0,-4.9,2.3),0,(.75,.9,1.0),.3,shadow=False)
    if view=='pud': point((pud[0]+1.2,pud[1]-.6,-1.6),45,(.8,.9,1.0),.3,shadow=False)
    def shake(Hx,t,amp=26,rate=9): Hx['head'].rotation_euler=(R(4),0,R(amp*math.sin(t*rate)))
    def upd(t):
        blink(H,t)
        if view=='leave':
            walk_path(H,[(-7.5,-1.3),(-2.0,-1.3)],t,-1.2,2.4,z=.07,step=.5,ease_in=.05,ease_out_=.05,mood=1); face(H,mouth='smirk',brow=.03)
            hideH(Rf); q=t/DUR; camset((2.6-.5*q,-8.8,.9),(-3.4,-.6,2.9),28,8.0)
        elif view=='win':
            walk_path(H,[(-2.9,-1.25),(2.4,-1.25)],t,0,3.3,z=.07,step=.5,ease_in=.1,ease_out_=.3,mood=2)
            k=ease((t-1.2)/.35); look_at(H,(H['root'].location[0]+.6,0,1.9),k); face(H,mouth='flat' if k<.5 else 'o',brow=.08*k,eyes=1+.1*k)
            mirror_pose(H,Rf); Rf['root'].location[2]=H['root'].location[2]
            Rf['root'].rotation_euler[2]=L(Rf['root'].rotation_euler[2],R(0),k)
            if k>.5: legs0(Rf); arms(Rf,-6,0,-4,-6,0,4); shake(Rf,t-1.4); face(Rf,mouth='flat',brow=-.02,brow_r=-10)
            x=H['root'].location[0]; camset((x+2.6,-6.2,1.5),(x+.3,.2,2.0),28,5.6,focus=(x,-1.25,1.6))
        elif view=='pud':
            px,py=pud[0],pud[1]
            H['root'].location=(px-1.3,py,.078); H['root'].rotation_euler=(0,0,R(90)); stand(H,t); arms(H,-10,0,-6,-10,0,6); look_at(H,(px,py,-1.0),1.0,maxpitch=60); face(H,mouth='o',brow=.1,eyes=1.15)
            Rf['root'].location=(px-1.3,py,.046); Rf['root'].rotation_euler=(0,0,R(90)); Rf['root'].scale=(1,1,-1)
            legs0(Rf); arms(Rf,-10,0,-6,-10,0,6); Rf['head'].rotation_euler=(R(-10),0,R(26*math.sin(t*11))); face(Rf,mouth='flat',brow_r=-10)
            hide(G); camset((px+3.7,py-.12,2.0),(px-.7,py,.55),30,8.0)
        elif view=='bus':
            H['root'].location=(.25,-2.25,.078); H['root'].rotation_euler=(0,0,0); stand(H,t); arms(H,-14,0,-8,-14,0,8); face(H,mouth='o',brow=.1,eyes=1.15)
            bx=L(13.5,-12.5,t/DUR); BU.location=(bx,-4.0,0)
            on=abs(bx)<4.9; Rf['root'].location=(.25,-5.75,.078); Rf['root'].rotation_euler=(0,0,R(180)); Rf['root'].scale=(1,1,1) if on else (0,0,0)
            legs0(Rf); arms(Rf,-6,0,-4,-6,0,4); shake(Rf,t,28,11); face(Rf,mouth='flat',brow_r=-10); BL.data.energy=260 if on else 0
            hide(G); camset((2.9,-.9,1.9),(-.5,-4.3,1.55),22,8.0)
        else:   # 'no'
            H['root'].location=(-.75,-1.5,.078); H['root'].rotation_euler=(0,0,R(170)); stand(H,t); arms(H,-14,0,-8,-14,0,8); look_at(H,(0,1.25,1.9),1)
            Rf['root'].location=(.25,1.2,.078); Rf['root'].rotation_euler=(0,0,R(-8)); legs0(Rf); arms(Rf,-6,0,-4,-6,0,4)
            tn=WS[83]-T0-.08; big=ease((t-tn)/.25)
            if t<tn-.05: shake(Rf,t,24,9); face(Rf,mouth='flat',brow=-.02,brow_r=-12)
            else: Rf['head'].rotation_euler=(R(6),0,R(34*math.sin((t-tn)*7)*math.exp(-(t-tn)*1.2))); face(Rf,mouth='o',brow=-.03,brow_r=-14); Rf['arm'][1].rotation_euler=(R(-95*big),0,R(-10*big))
            q=ease(t/DUR); camset((.95-.15*q,-3.3+.5*q,1.85),(.1,.9,1.82),40+6*q,4.0,focus=(.25,1.2,1.85))
    return dict(upd=upd)
for _v in ('leave','win','pud','bus','no'): SHOTS['ST_'+_v]=(lambda v=_v: ST_(v))

# =================================================================== HOUSE
FROZ=[]
def frozen_family():
    Mo=av((-.3,-3.8,0),-50,MOMR,{'mouth':'smile'},name='mom'); Si=av((.5,-2.5,0),200,SIS,{'mouth':'grin'},name='sis')
    walk(Mo,.42,step=.55); Mo['arm'][1].rotation_euler=(R(-55),0,R(-8)); Mo['arm'][-1].rotation_euler=(R(20),0,0); Mo['head'].rotation_euler=(R(4),0,R(-25))
    mug=ocyl((.05,-4.3,1.05),.07,.13,M('#F4F1EA',.4),rot=(R(55),R(20),0),seg=14)
    for k in range(6): oico((.1+.05*k,-4.35-.03*k,.98-.07*k-.01*k*k),.03-.003*k,M('#6B3A1E',.2,spec=.8),sub=2)
    Si['root'].location[2]=.32; Si['arm'][1].rotation_euler=(R(-150),0,R(18)); Si['arm'][-1].rotation_euler=(R(-150),0,R(-18)); Si['leg'][1].rotation_euler=(R(-25),0,0); Si['leg'][-1].rotation_euler=(R(30),0,0); Si['head'].rotation_euler=(R(-14),0,0); face(Si,mouth='grin',brow=.08)
    pl=omesh([(0,-.22,0),(-.13,.16,.03),(0,.12,0),(.13,.16,.03)],[(0,1,2),(0,2,3)],M('#F7F7F2',.6),loc=(1.1,-2.1,1.95),thick=.004); pl.rotation_euler=(R(12),0,R(40))
    FROZ.append(pl); FROZ.append(mug)
    return Mo,Si
def HS_(view):
    warm=view in ('tick','thanks','late')
    G=house('warm' if warm else 'frozen'); setup_dark('#060A14',.5 if warm else .35,res=PCT,samples=SAMPLES,bloom=.05)
    H=av((2.3,-5.2,0),20,MARCUS,{'mouth':'flat'},name='marcus'); Rf=av((0,1.0,0),0,MARCUS,{'mouth':'flat'},name='marcusR')
    if not warm: Mo,Si=frozen_family()
    if view=='bdoor': point((-3.7,-5.2,.6),30,(.45,.7,1.0),.2,shadow=False)
    if view=='door': point((2.6,-7.2,2.0),260,(.5,.65,1.0),.3,shadow=False)
    def upd(t):
        blink(H,t); clock_set(0,frozen=True)
        if view=='door':
            walk_path(H,[(2.72,-7.3),(2.72,-6.3),(2.65,-5.6)],t,-.2,1.25,z=0,step=.42,ease_in=.1,ease_out_=.4,mood=0); face(H,mouth='o' if t>.6 else 'flat',brow=.08,eyes=1.1); hideH(Rf)
            q=ease(t/DUR); camset((3.35,-2.9+.2*q,1.62),(2.4,-6.4,1.45),30,5.6,focus=(2.7,-6.0,1.6))
        elif view in ('clk1','clk2'):
            hideH(H); hideH(Rf); q=ease(t/DUR)
            if view=='clk1': camset((2.45,-2.6+.5*q,1.75),(3.2,-.4,1.72),50,8.0)
            else: camset((-1.3,-2.6+.5*q,2.1),(-1.9,-.1,2.72),75,8.0)
        elif view=='mom':
            H['root'].location=(1.05,-4.95,.008); H['root'].rotation_euler=(0,0,R(heading_to(H,(-.3,-3.8)))); stand(H,t); look_at(H,(-.3,-3.8,1.95),1); face(H,mouth='o',brow=.1,eyes=1.15)
            w=ease(t/.3); H['arm'][1].rotation_euler=(R(-100*w),0,R(18*w*math.sin(t*10))); H['arm'][-1].rotation_euler=(R(-8),0,R(-4)); hideH(Rf)
            q=ease(t/DUR); camset((-1.85+.15*q,-6.4,1.5),(.5,-4.15,1.15),21,5.6,focus=(-.3,-3.8,1.6))
        elif view=='sis':
            hideH(H); hideH(Rf); q=ease(t/DUR); camset((-.75+.15*q,-.55,1.15),(.5,-2.5,1.4),32,5.6,focus=(.5,-2.5,1.3))
        elif view=='mir':
            H['root'].location=(-.3,-1.55,.008); H['root'].rotation_euler=(0,0,R(180)); stand(H,t); arms(H,-8,0,-4,-8,0,4); face(H,mouth='o',brow=.06)
            mirror_pose(H,Rf); legs0(Rf); face(Rf,mouth='flat',brow_r=-8); arms(Rf,-6,0,-4,-6,0,4); Rf['root'].rotation_euler=(0,0,0)
            k=ease((t-(WS[114]-T0-.25))/.4); arm_to(Rf,1,(-.55,.35,.05),k) if k>0 else None; Rf['head'].rotation_euler=(R(18*k),0,0); blink(Rf,t)
            look_at(H,(-.3,1.55,1.85-.9*ease((t-(WS[114]-T0+.2))/.4)),1,maxpitch=45)
            q=ease(t/DUR); hideH(Mo); hideH(Si); [hide(o) for o in FROZ]; camset((1.2,-3.45+.25*q,1.78),(-.15,.6,1.4),30+3*q,5.6,focus=(-.3,1.5,1.6))
        elif view=='bdoor':
            walk_path(H,[(-1.5,-3.6),(-2.25,-4.5)],t,-.3,.9,z=0,step=.42,ease_in=.1,ease_out_=.4); face(H,mouth='flat',brow=.06); hideH(Rf)
            if t>.6: arm_to(H,1,(-3.2,-5.2,1.3),ease((t-.6)/.3))
            q=ease(t/DUR); camset((-.35+.1*q,-6.35,1.62),(-2.55,-4.75,1.25),23,5.6,focus=(-2.3,-4.6,1.5))
        elif view=='empty':
            hideH(H); hideH(Rf); q=t/DUR; camset((3.2-.5*q,-1.0-.3*q,2.3),(.1,-3.3,1.25),27,8.0)
        elif view=='copies':
            hideH(H); hideH(Rf); cam=(-1.25,-4.75,1.72); k=ease((t-(WS[153]-T0-.05))/.16)
            Mo['head'].rotation_euler=(R(4)*(1-k),0,R(-25)*(1-k)+R(8)*k); face(Mo,mouth='grin' if k>.5 else 'smile',brow=-.03*k,brow_r=-12*k)
            q=ease(t/DUR); camset((cam[0]+.25*q,cam[1]+.22*q,cam[2]),(-.42,-3.95,1.78),30,8.0)
        elif view=='tick':
            hideH(H); hideH(Rf); clock_set(t*1.0+.5); q=ease(t/DUR); camset((2.45,-2.9+.6*q,1.75),(3.2,-.4,1.6),42,8.0)
        else:
            clock_set(40+t)
            H['root'].location=(-.4,-1.8,.008); H['root'].rotation_euler=(0,0,R(190)); stand(H,t); look_at(H,(0,1.0,1.8),1); face(H,mouth='smile',brow=.04)
            Rf['root'].location=(.0,1.15,.008); Rf['root'].rotation_euler=(0,0,0); legs0(Rf); arms(Rf,-6,0,-4,-6,0,4); blink(Rf,t)
            if view=='thanks':
                wv=ease((t-.25)/.3); H['arm'][1].rotation_euler=(R(-150*wv),0,R(14*wv+10*wv*math.sin(t*9))); H['arm'][-1].rotation_euler=(R(-8),0,R(4)); face(Rf,mouth='flat',brow=0)
                q=ease(t/DUR); camset((.95,-3.3,2.0),(-.1,.4,1.6),32+2*q,5.6,focus=(0,1.1,1.8))
            else:
                walk_path(H,[(-.4,-1.8),(-1.2,-2.6),(-1.6,-4.6)],t,.15,2.6,z=0,step=.45,ease_in=.15,ease_out_=.1); face(H,mouth='smile')
                late=ease((t-.25)/.2); face(Rf,mouth='grin' if late>.5 else 'flat',brow=.05*late)
                wv=ease((t-.5)/.3); Rf['arm'][-1].rotation_euler=(R(-150*wv),0,R(-14*wv-10*wv*math.sin(t*9)))
                lk=ease((t-1.9)/.3); Rf['head'].rotation_euler=(0,0,R(-9)*lk)
                if t>2.45: blink(Rf,t,1 if t<2.62 else 0)
                q=ease(t/DUR); camset((.95-.45*q,-3.3+1.0*q,2.0-.1*q),(-.1+.1*q,.4,1.6+.22*q),34+16*q,5.6,focus=(0,1.1,1.8))
    return dict(upd=upd)
for _v in ('door','clk1','clk2','mom','sis','mir','bdoor','empty','copies','tick','thanks','late'): SHOTS['H_'+_v]=(lambda v=_v: HS_(v))

def NB_():
    HS=neighbourhood(); setup_dark('#0A1230',1.0,res=PCT,samples=SAMPLES,ssr=True,bloom=.12,mist=('#18244A',14,60,.5))
    bpy.ops.object.light_add(type='SUN'); S=bpy.context.object; S.rotation_euler=(R(55),0,R(160)); S.data.energy=1.4; S.data.color=(.55,.68,1.0)
    fl=[point((h['x']+.9,.2,1.6),0,(.6,.85,1.0),.3,shadow=False) for h in HS]
    def upd(t):
        for i,h in enumerate(HS):
            ts=.45+i*.62; on=t>=ts
            for o in h['warm']: o.scale=(0,0,0) if on else (1,1,1)
            for o in h['cold']: o.scale=(1,1,1) if on else (0,0,0)
            fl[i].data.energy=(900*math.exp(-(t-ts)*7)+60) if on else 0; h['light'].data.energy=0 if on else 90
        q=t/DUR; camset((-13.5+1.2*q,-5.6,3.4-.2*q),(-3.0+1.2*q,3.0,1.7),28,8.0)
    return dict(upd=upd)
SHOTS['NB']=NB_

# =================================================================== BASEMENT
def no_shadow(Hc):
    seen=set()
    def rec(o):
        for sl in getattr(o,'material_slots',[]):
            if sl.material and sl.material.name not in seen: seen.add(sl.material.name); sl.material.shadow_method='NONE'
        for c in o.children: rec(c)
    rec(Hc['root'])
def stair_pos(k): return (-3.15,-5.9+.4*k,2.94-.3*k)
def BS_(view):
    G,cloth=basement(); setup_dark('#04060C',.25,res=PCT,samples=SAMPLES,bloom=.09)
    M0=(-.2,-2.3); C1=(-2.6,-1.6)
    H=av((M0[0],M0[1],0),180,MARCUS,{'mouth':'o'},name='marcus'); Rf=av((.9,1.6,0),0,MARCUS,{'mouth':'flat'},name='marcusR')
    Mo=av((-.45,.42,0),0,MOMR,{'mouth':'O'},name='mom'); Si=av((.5,.4,0),0,SIS,{'mouth':'O'},name='sis')
    C=av((C1[0],C1[1],0),100,COPY,{'mouth':'grin'},name='copy'); no_shadow(C)
    bulb=point((.3,-3.2,2.5),70,(1,.8,.55),.1); mg=area((0,-.5,1.7),45,(2.2,2.6),(.55,.82,1.0),rot=(R(90),0,0),shadow=True); bk=point((0,2.2,2.2),70,(.6,.85,1.0),.5,shadow=False); ck=point((-2.0,-2.3,2.3),140,(.6,.8,1.0),.2,shadow=False); fill=point((0,-3.6,2.2),70,(1,.85,.7),.4,shadow=False)
    if view=='face': point((.4,-.9,2.0),45,(.6,.85,1.0),.3,shadow=False)
    if view in ('creak','look','turn','hug'): point((.45,-1.25,1.95),40,(.75,.88,1.0),.3,shadow=False)
    beam=spot((6.5,-2.2,3.6),(C1[0],C1[1],1.4),0,(1,.85,.55),30,.3,.2)
    LK=M('#FFE2A8',.3,emit=8.0); leaks=[obox((3.69,-2.2,2.5+sz*.51),(.01,.87,.03),LK,0) for sz in (-1,1)]+[obox((3.69,-2.2+sy*.86,2.5),(.01,.03,.52),LK,0) for sy in (-1,1)]
    pane=obox((3.685,-2.2,2.55),(.01,.74,.39),M('#FFE9B8',.3,emit=7.0),0); pane.scale=(0,0,0)
    if view in ('window','rip'): point((3.3,-2.2,2.5),30,(1,.85,.55),.3,shadow=False)
    d=Vector((M0[0]-C1[0],M0[1]-C1[1],0)).normalized(); hd=math.degrees(math.atan2(d.x,-d.y))
    ex={}
    if view=='shadow': ex['key']=spot((2.6,-2.1,1.25),(-2.0,-2.0,.2),2000,(1,.85,.6),60,.3,.02)
    if view=='crack':
        cam=Vector((-.4,-3.9,1.6)); cc=Vector((C1[0],C1[1],1.05)); n=(cam-cc); n.z=0; n.normalize(); rt=Vector((-n.y,n.x,0)); P0=cc+n*.42
        CRM=M('#F2FBFF',.3,emit=6.0); r=random.Random(7); segs=[]
        def crack(p,ang,ln,depth,t0):
            if depth>3 or ln<.05: return
            a=ang+r.uniform(-.5,.5); q=(p[0]+ln*math.cos(a),p[1]+ln*math.sin(a))
            if abs(q[0])>.72 or abs(q[1])>1.0: return
            mid=P0+rt*((p[0]+q[0])/2)+Vector((0,0,(p[1]+q[1])/2)); o=obox(tuple(mid),(ln/2,.004,.007),CRM,0); o.rotation_euler=(0,-a,math.atan2(rt.y,rt.x)); segs.append((o,t0))
            crack(q,a,ln*r.uniform(.7,.95),depth+1,t0+.13)
            if r.random()<.75: crack(q,a+r.choice((-1,1))*r.uniform(.6,1.2),ln*.7,depth+1,t0+.16)
        for k in range(7): crack((r.uniform(-.1,.1),r.uniform(-.1,.5)),k*.9+.3,.3,0,.35+.06*k)
        ex['segs']=segs
        cols=[('#15120E',.85,1.0),('#8A5A3D',.62,.85),('#F2B81E',.1,.62),('#F2B81E',-.2,.1),('#232A3E',-.95,-.2),('#F4F5FB',-1.05,-.95)]; sh=[]
        for i in range(70):
            c,z0,z1=cols[r.choice([0,1,2,2,2,3,3,4,4,4,5])]; x=r.uniform(-.7 if z0>-.2 and z1<.7 else -.36,.7 if z0>-.2 and z1<.7 else .36); z=r.uniform(z0,z1); s_=r.uniform(.06,.16)
            o=omesh([(-s_,0,-s_*.6),(s_,0,-s_*.3),(r.uniform(-s_,s_),0,s_)],[(0,1,2)],M(c,.15,spec=1.0),thick=.02); p=P0-n*.42+rt*x+Vector((0,0,z)); o.rotation_euler=(0,r.uniform(0,6),math.atan2(rt.y,rt.x))
            v=(rt*x*2.2+n*r.uniform(-.6,1.2)+Vector((0,0,r.uniform(.5,3.0)))-Vector((1.6,0,0))); sh.append((o,tuple(p),tuple(v),(r.uniform(-9,9),r.uniform(-9,9),r.uniform(-9,9))))
        ballistic(sh,1.78,floor=.03); ex['sh']=[x_[0] for x_ in sh]
        shaft=omesh([(3.7,-1.5,2.9),(3.7,-2.9,2.9),(3.7,-2.9,2.15),(3.7,-1.5,2.15),(C1[0],C1[1]+.8,2.3),(C1[0],C1[1]-.8,2.3),(C1[0],C1[1]-.8,.1),(C1[0],C1[1]+.8,.1)],[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],M('#FFE2A8',.5,emit=1.0,alpha=.05)); shaft.name='glass_shaft'
    if view in ('water','hug'):
        N=26; vs=[(BSm['x0']+(BSm['x1']-BSm['x0'])*i/N,0,BSm['z0']+(BSm['z1']-BSm['z0'])*j/N) for j in range(N+1) for i in range(N+1)]
        fs=[(j*(N+1)+i,j*(N+1)+i+1,(j+1)*(N+1)+i+1,(j+1)*(N+1)+i) for j in range(N) for i in range(N)]
        wat=omesh(vs,fs,M('#9FDCFF',.08,spec=1.0,emit=.35,alpha=.5)); wat.name='glass_water'
        for p in wat.data.polygons: p.use_smooth=True
        ex['wat']=wat; ex['vs']=vs
    def family(t,amp=1.0):
        for X_,ph in ((Mo,0),(Si,1.3)):
            legs0(X_); b=math.sin(t*9+ph)
            for s in (1,-1): arm_to(X_,s,(X_['root'].location[0]+s*.28,.02+.14*max(0,s*b),1.45 if X_ is Mo else 1.05),1)
            face(X_,mouth='O' if b>0 else 'o',brow=.1,brow_r=12); X_['root'].location[2]=.008+.012*abs(b)*amp; X_['head'].rotation_euler=(R(-6),0,0)
    def ripple(t,amp):
        me=ex['wat'].data
        for i,v in enumerate(ex['vs']):
            me.vertices[i].co.y=amp*(.05*math.sin(v[0]*5+t*7)+.05*math.sin(v[2]*4-t*6)+.035*math.sin((v[0]+v[2])*9+t*11))
        me.update()
    def upd(t):
        blink(H,t); blink(C,t); blink(Rf,t)
        family(t); Rf['root'].location=(1.0,1.5,.008); legs0(Rf); face(Rf,mouth='flat'); arms(Rf,-6,0,-4,-6,0,4); Rf['head'].rotation_euler=(0,0,0)
        C['root'].location=(C1[0],C1[1],.008); C['root'].rotation_euler=(0,0,R(hd)); legs0(C); arms(C,-6,0,-3,-6,0,3); C['head'].rotation_euler=(R(8),0,0); face(C,mouth='grin',brow=-.03,brow_r=-14,eyes=.9)
        H['root'].location=(M0[0],M0[1],.008); H['root'].rotation_euler=(0,0,R(180)); stand(H,t); arms(H,-20,0,-10,-20,0,10); face(H,mouth='O',brow=.12,eyes=1.2); look_at(H,(0,.4,1.6),1)
        if view=='wide':
            k=L(5.2,8.6,ease(t/DUR)); p=stair_pos(k); H['root'].location=p; H['z0']=p[2]; H['root'].rotation_euler=(0,0,R(180)); walk(H,(k-5.2)*.5,step=.4,arm=12); H['root'].location=(p[0],p[1],p[2]+.008); look_at(H,(0,0,1.6),1); face(H,mouth='o',brow=.1,eyes=1.15)
            hideH(C); q=ease(t/DUR); camset((2.3-.25*q,-5.75,2.0),(-1.15,-1.5,1.45),18,8.0)
        elif view=='mir':
            k=ease(t/1.2); H['root'].location[1]=-2.9+.6*k; hideH(C); q=ease(t/DUR); camset((1.6,-4.7+.4*q,1.8),(0,.3,1.5),30+3*q,5.6,focus=(0,0,1.6))
        elif view=='hit':
            hideH(H); hideH(C); hideH(Rf); q=ease(t/DUR); camset((.3-.1*q,-1.75+.25*q,1.4),(0,.4,1.28),30,8.0)
        elif view=='face':
            k=ease((t-.4)/.25); face(H,mouth='o' if k<.5 else 'flat',brow=.12*(1-k)-.02*k,brow_r=-10*k,eyes=1.2-.2*k); arms(H,-8,0,-4,-8,0,4)
            hideH(C); q=ease(t/DUR); camset((.2,-.55-.1*q,1.85),(-.2,-2.3,1.87),52+6*q,8.0)
        elif view=='creak':
            k=ease((t-.55)/.25); H['head'].rotation_euler=(0,0,R(-70)*k); face(H,mouth='o',brow=.12,eyes=1.2); arms(H,-8,0,-4,-8,0,4)
            ks=L(1.2,3.0,t/DUR); p=stair_pos(ks); C['z0']=p[2]; C['root'].location=p; C['root'].rotation_euler=(0,0,R(180)); walk(C,(ks)*.5,step=.4,arm=10); C['root'].location=(p[0],p[1],p[2]+.008)
            camset((.75,-.75,1.75),(-1.9,-4.0,1.75),28,5.6,focus=(-.2,-2.3,1.8))
        elif view=='down':
            ks=L(3.0,7.2,t/DUR); p=stair_pos(ks); C['z0']=p[2]; C['root'].location=p; C['root'].rotation_euler=(0,0,R(180)); walk(C,ks*.5,step=.4,arm=10); C['root'].location=(p[0],p[1],p[2]+.008); C['head'].rotation_euler=(R(10),0,R(-35)); face(C,mouth='smile',brow=-.02,brow_r=-10)
            hideH(H); q=ease(t/DUR); camset((-1.5,-2.3-.2*q,.8),(-3.1,-4.2+.5*q,2.3),26,8.0)
        elif view in ('hood','cface','smile'):
            hideH(H); base=Vector((C1[0],C1[1],0)); q=ease(t/DUR)
            if view=='hood': cp=base+d*(1.7-.1*q)+Vector((.15,0,1.45)); camset(tuple(cp),(C1[0],C1[1],1.5),36,8.0)
            elif view=='cface': face(C,mouth='flat',brow=0,brow_r=0,eyes=1.0); C['head'].rotation_euler=(0,0,0); cp=base+d*(1.6-.1*q)+Vector((0,0,1.8)); camset(tuple(cp),(C1[0],C1[1],1.8),55,8.0)
            else:
                g=ease((t-.25)/.2); face(C,mouth='grin' if g>.5 else 'flat',brow=-.05*g,brow_r=-18*g,eyes=1-.15*g); C['head'].rotation_euler=(R(10)*g,0,R(7)*g); cp=base+d*(1.25-.12*q)+Vector((0,0,1.74)); camset(tuple(cp),(C1[0],C1[1],1.76),52,8.0)
        elif view=='turn':
            H['root'].rotation_euler=(0,0,R(hd+180)); arms(H,-25,0,-12,-25,0,12); look_at(H,(C1[0],C1[1],1.8),1)
            k=ease(t/.3); arm_to(C,1,(M0[0],M0[1],1.5),k); mouth_talk(C,t,.1,.85,shapes=('O','grin','o','grin'),rate=8,rest='grin'); C['head'].rotation_euler=(R(6),0,R(6))
            cp=Vector((M0[0],M0[1],0))+d*1.55+Vector((d.y*.85,-d.x*.85,1.95)); camset(tuple(cp),(C1[0],C1[1],1.5),34,5.6,focus=(C1[0],C1[1],1.7))
        elif view=='look':
            k=ease((t-.25)/.35); H['root'].rotation_euler=(0,0,R(hd+180+ (180-(hd+180))*k)); arms(H,-22,0,-10,-22,0,10); look_at(H,(1.0,1.5,1.85),k); face(H,mouth='o',brow=.1,eyes=1.15)
            hideH(C); Mo['root'].location[0]=-.9; Si['root'].location[0]=-.15; Rf['root'].location=(.75,.6,.008); q=ease(t/DUR); camset((2.0-.1*q,-3.9,1.72),(-.3,.4,1.6),27,5.6,focus=(.75,.6,1.7))
        elif view=='point':
            hideH(H); hideH(C); Mo['root'].location[0]=-.9; Si['root'].location[0]=-.15; Rf['root'].location=(.75,.6,.008); k=ease((t-.5)/.4); arm_to(Rf,1,(C1[0]+.6,C1[1],.0),k); Rf['head'].rotation_euler=(R(14)*k,0,R(-16)*k); face(Rf,mouth='o' if k>.5 else 'flat',brow=.06,brow_r=-8)
            for X_ in (Mo,Si): X_['head'].rotation_euler=(R(4),0,R(-30)*ease((t-1.0)/.4))
            q=ease(t/DUR); camset((-.3+.2*q,-2.7+.4*q,1.7),(.45,.5,1.4),33+4*q,8.0)
        elif view=='shadow':
            H['root'].rotation_euler=(0,0,R(hd+180)); arms(H,-22,0,-10,-22,0,10); look_at(H,(C1[0],C1[1],.0),1,maxpitch=50); bulb.data.energy=15
            q=ease(t/DUR); camset((1.5,-4.7+.2*q,2.9),(-1.45,-1.85,.45),24+1.5*q,8.0)
        elif view=='window':
            H['root'].rotation_euler=(0,0,R(90)); arms(H,-10,0,-5,-10,0,5); look_at(H,(3.7,-2.2,2.5),ease((t-.2)/.3),maxpitch=40); face(H,mouth='flat',brow=.02,brow_r=-10,eyes=1.0)
            hideH(C); q=ease(t/DUR); camset((-1.7+.3*q,-3.1,2.05),(3.7,-2.2,2.3),36+6*q,5.6,focus=(3.7,-2.2,2.5))
        elif view in ('rip',):
            tr=.72; walk_path(H,[M0,(1.6,-2.25),(3.0,-2.2)],t,0,tr,z=0,step=.8,ease_in=.15,ease_out_=.15,run_=True); face(H,mouth='shout',brow_r=-12)
            j=max(0,t-tr); 
            if j>0:
                legs0(H); H['root'].rotation_euler=(0,0,R(90)); z=max(0,3.2*j-9.8*j*j/2*1.6); H['root'].location=(3.0,-2.2,.008+z); 
                for s in (1,-1): H['arm'][s].rotation_euler=(R(-170 if j<.35 else -60),0,R(-s*8))
            f=ease((t-(tr+.3))/.3); cloth.location=(3.62-.15*f,-2.2-1.05*f,2.5-2.42*f*f); cloth.rotation_euler=(R(55*f),R(-80*f),0); beam.data.energy=9000*ease((t-(tr+.3))/.2)
            pane.scale=(1,1,1) if f>.1 else (0,0,0)
            for o in leaks: o.scale=(0,0,0) if f>.1 else (1,1,1)
            hideH(C); q=ease(t/DUR); camset((.7,-5.2+.3*q,1.5),(3.1,-2.2,2.0),25,8.0)
        elif view=='crack':
            hide(cloth); [hide(o) for o in leaks]; pane.scale=(1,1,1); beam.data.energy=9000; hideH(H); gone=t>=1.78
            sk=min(1,t/.2); shock(C,sk); face(C,mouth='O',brow=.06,brow_r=14,eyes=1.25); C['root'].rotation_euler=(R(-6)*sk,0,R(hd-60*sk)); C['root'].location[0]=C1[0]+.02*math.sin(t*60)*(t>.3)
            if gone: hideH(C)
            for o,t0 in ex['segs']: o.scale=(0,0,0) if (t<t0 or gone) else (min(1,(t-t0)/.1),1,1)
            for o in ex['sh']: o.scale=(1,1,1) if gone else (0,0,0)
            q=ease(t/DUR); camset((-.4,-3.9+.2*q,1.6),(C1[0],C1[1],1.15),30,8.0)
        elif view=='water':
            hide(cloth); [hide(o) for o in leaks]; pane.scale=(1,1,1); beam.data.energy=4000; hide(G); hideH(C); ripple(t,ease(t/.4))
            H['root'].location[1]=-2.0; arms(H,-40,0,-10,-40,0,10); face(H,mouth='o',brow=.12)
            k=ease((t-.5)/1.0)
            for X_,x0 in ((Mo,-.45),(Si,.5)): X_['root'].location=(x0,.42-.5*k,.008); face(X_,mouth='o',brow=.1); [arm_to(X_,s,(x0+s*.25,-1.2,1.3),1) for s in (1,-1)]
            q=ease(t/DUR); camset((1.5-.2*q,-4.2+.4*q,1.75),(0,.1,1.5),30,8.0)
        else:   # hug
            hide(cloth); [hide(o) for o in leaks]; pane.scale=(1,1,1); beam.data.energy=4000; hideH(C); ripple(t,max(0,1-t/1.2)); hide(G) if t<1.2 else None
            ex['wat'].scale=(1,1,1) if t<1.2 else (0,0,0)
            k=ease(t/.7); kn=ease((t-.5)/.5)
            H['root'].location=(0,-1.75,.008); H['root'].rotation_euler=(0,0,R(180)); legs0(H); kneel(H,.55*kn,bow=.3); 
            for s in (1,-1): H['arm'][s].rotation_euler=(R(-85),0,R(-s*(40-30*kn)))
            face(H,mouth='grin' if t>.8 else 'o',brow=.08); H['head'].rotation_euler=(R(-6),0,0)
            for X_,x0,x1,y1 in ((Mo,-.45,-.33,-1.28),(Si,.5,.36,-1.33)):
                X_['root'].location=(L(x0,x1,k),L(-.08,y1,k),.008+.12*math.sin(pi*k)); X_['root'].rotation_euler=(R(14)*k,0,0); legs0(X_)
                for s in (1,-1): X_['arm'][s].rotation_euler=(R(-80),0,R(-s*(30-22*k)))
                face(X_,mouth='grin' if t>.9 else 'o',brow=.08); X_['head'].rotation_euler=(R(-4),0,0)
            Rf['root'].location=(.9,1.7,.008); face(Rf,mouth='smile'); Rf['root'].scale=(1,1,1) if t>1.2 else (0,0,0)
            q=ease(t/DUR); camset((2.05-.15*q,-3.35+.1*q,2.25),(-.1,-1.45,.95),24+3*q,5.6,focus=(0,-1.5,1.1))
    return dict(upd=upd)
for _v in ('wide','mir','hit','face','creak','down','hood','cface','smile','turn','look','point','shadow','window','rip','crack','water','hug'): SHOTS['B_'+_v]=(lambda v=_v: BS_(v))
