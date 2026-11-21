SHOTS={}
WS=[w_['t0'] for w_ in json.load(open('/home/claude/huss/audio/words.json'))]
SEQ=[('S_hook', 0.0), ('S_city', 1.4), ('S_name', 5.44), ('S_why', 7.44), ('A_clock', 9.12), ('A_brush', 13.34), ('A_break', 14.77), ('A_mirror', 16.23), ('S_lambo', 19.92), ('P_400', 22.91), ('P_never', 26.8), ('P_approach', 29.27), ('P_huss', 32.75), ('P_run', 33.96), ('S_arrive', 36.02), ('S_destroy', 39.27), ('S_sees', 43.77), ('S_you', 46.61), ('S_glasses', 48.98), ('S_charge', 51.77), ('S_step1', 53.23), ('S_step2', 56.12), ('S_faster', 57.98), ('S_shake', 61.77), ('S_army', 64.55), ('S_nobody', 66.2), ('S_ask', 68.41), ('S_look', 71.98), ('S_whisper', 74.62), ('S_inhaler', 76.7), ('S_end', 79.05)]
END=81.2
def TK(key): return [t for k,t in SEQ if k==key][0]
def wl(i,key): return WS[i]-TK(key)          # word i time, local to shot
def mkhuss(loc,rz,glasses=True,mouth='flat'):
    H=av(loc,rz,HUSS,{'mouth':mouth},name='huss'); coat(H); g=sunglasses(H) if glasses else None; return H,g
def day():
    S,w,rp,bg=setup_render('afternoon',res=PCT,samples=SAMPLES); return S

# =================================================================== STREET
def ST_(view):
    street(); day(); KEY='S_'+view; ex={}
    upd=None
    if view=='hook':
        H,g=mkhuss((0,-1,0),0); breath(H,[wl(i,KEY) for i in (0,1,2)],size=.09,n=5)
        def upd(t):
            blink(H,t,0); stand(H,t); face(H,mouth='O' if any(0<=t-wl(i,KEY)<.25 for i in (0,1,2)) else 'flat',brow=-.02,brow_r=14)
            k=max([max(0,1-abs(t-wl(i,KEY)-.08)/.18) for i in (0,1,2)]); H['root'].scale=(1+.03*k,1+.03*k,1-.01*k); H['head'].rotation_euler[0]=R(-6*k)
            q=ease(t/DUR); camset((0,-3.3+.3*q,1.55),(0,-1,2.2),40,4.0,focus=(0,-1.3,2.2))
    elif view=='city':
        H,g=mkhuss((-7,5.4,0),-90)
        cs=people([(-1,5.0,90,False),(0,6.0,80,False),(1.6,5.2,100,True),(1.0,6.4,90,False),(-3.5,6.4,95,False)],citizen)
        def upd(t):
            blink(H,t); walker(H,(-7,5.4,0),-90+180,1.2,t,arm=12); face(H,mouth='flat',brow=-.02,brow_r=12)
            for i,c in enumerate(cs):
                blink(c,t); stand(c,t); hx=H['root'].location[0]; d=c['x']-hx
                k=ease((2.6-d)/1.2); c['root'].location[1]=c['y']+(1.3 if c['y']>5.5 else -1.0)*k; c['root'].rotation_euler[2]=R(c['rz']+(-90 if c['y']>5.5 else 90)*k*.5)
                look_at(c,(hx,5.4,1.9)); face(c,mouth='o' if k>.2 else 'smile',brow=.08*k)
                if k>.3 and i%2==0: shock(c,min(1,k)*.6)
            q=ease(t/DUR); camset((5.4,2.4,1.45),(-2.0,5.6,2.0),22,8.0)
    elif view=='name':
        H,g=mkhuss((0,0,0),0)
        def upd(t):
            blink(H,t,0); stand(H,t); face(H,mouth='smirk' if t>1.0 else 'flat',brow=-.02,brow_r=14); H['arm'][1].rotation_euler=(R(-8),0,R(6)); H['arm'][-1].rotation_euler=(R(-8),0,R(-6))
            q=ease(t/DUR); camset((.9-.5*q,-2.7,.35),(0,0,2.4+.5*q),18,8.0)
    elif view=='why':
        a,b=people([(-.4,6.0,-20,False),(.5,6.1,20,False)],citizen)
        def upd(t):
            for i,c in enumerate((a,b)):
                blink(c,t); stand(c,t); k=ease((t-.3-i*.2)/.4)
                c['arm'][1].rotation_euler=(R(-40*k),0,R(55*k)); c['arm'][-1].rotation_euler=(R(-40*k),0,R(-55*k)); c['head'].rotation_euler=(0,R(12*k*(1 if i else -1)),0)
                face(c,mouth='frown' if i else 'flat',brow=.1*k,brow_r=-14*k)
            q=ease(t/DUR); camset((1.1,3.35,1.75),(0,6.0,1.75),30,5.0,focus=(0,6.0,1.8))
    elif view=='lambo':
        cr=car(0,1.8,'#F07A1A',rz=0,sport=True); H,g=mkhuss((0,-1.4,0),-90)
        def upd(t):
            x=-12+14*t; cr.location[0]=x; H['root'].location[0]=x+1.5*ease(t/DUR)+.6; H['root'].rotation_euler[2]=R(-90+180)
            run(H,x*1.0,arm=80); H['root'].rotation_euler[0]=R(22); face(H,mouth='flat',brow=-.03,brow_r=14)
            SHAKE[0]=.01; camset((x+4.5,-5.5,1.1),(x+1.5,.2,1.1),26,8.0)
    elif view in ('arrive','destroy','sees','you','charge','shake','army'):
        V=av((7.0,0,0),-90,VILL,{'mouth':'grin'},name='vill'); H,g=mkhuss((-3,0,0),90)
        mins=[av((10.5+(i%3)*1.4,-1.8+(i//3)*1.8,0),-90,minion(i),{'mouth':'flat'},name='m%d'%i) for i in range(6)]
        if view=='arrive':
            hideH(H); puff((7,0,.2),.15,size=.9,n=10,rise=.6,life=1.6,col=M('#C9C1B0',.9),seed=2); shockwave((7,0,.05),.12,6.0,.8,'#E8DCC8')
            def upd(t):
                k=ease_in(min(1,t/.2)); V['root'].location[2]=12*(1-k)+.008; V['z0']=0; legs0(V)
                if t>.2: kneel(V,max(0,1-(t-.2)/.6)*.8,bow=.3)
                face(V,mouth='grin',brow=-.04,brow_r=18); blink(V,t)
                for m in mins: blink(m,t); stand(m,t)
                SHAKE[0]=.06*max(0,1-abs(t-.22)/.5)
                q=ease(t/DUR); camset((1.0,-3.0,.5),(7,0,2.6),20,8.0)
        elif view=='destroy':
            hideH(H); P=car(4,-2.6,'#F4F5FA',rz=10,police=True)
            cops=[av((2.5,-1.0,0),-80+180,cop(i),{'mouth':'O'},name='cop%d'%i) for i in range(2)]
            chunks=[]; r=random.Random(3); CH=M('#C9B79C',.75,kind='wall')
            for i in range(14): o=obox((12+r.uniform(-2,2),7.2,14+r.uniform(-2,3)),(r.uniform(.4,1.0),r.uniform(.3,.6),r.uniform(.4,1.0)),CH,.04); chunks.append((o,tuple(o.location),(r.uniform(-2,0),-r.uniform(1,3),r.uniform(0,2)),(r.uniform(-4,4),r.uniform(-4,4),r.uniform(-4,4))))
            ballistic(chunks,.2,floor=.3)
            def upd(t):
                blink(V,t); stand(V,t); face(V,mouth='shout',brow=-.04,brow_r=18)
                V['arm'][1].rotation_euler=(R(-150*ease(t/.4)),0,R(20));
                k=ease((t-1.6)/.5); P.location=(4-1.5*k,-2.6-1.0*k,2.2*math.sin(pi*k)); P.rotation_euler=(R(180*k),0,R(10))
                for i,c in enumerate(cops):
                    blink(c,t); kk=ease((t-2.4-i*.15)/.3); c['root'].rotation_euler=(R(-80*kk),0,R(100)); c['root'].location[0]=2.5-1.2*kk; c['root'].location[2]=.3*math.sin(pi*kk); face(c,mouth='O')
                SHAKE[0]=.03 if .2<t<1.2 else 0
                q=ease(t/DUR); camset((-2.5,-6.5,2.0),(6,1,5.5-3*q),20,8.0)
        elif view=='sees':
            def upd(t):
                blink(V,t); blink(H,t,0); stand(V,t); stand(H,t); k=ease(t/.5); V['root'].rotation_euler[2]=R(-90)
                lk=ease((t-.9)/.4); V['root'].rotation_euler[0]=R(-8*lk); V['head'].rotation_euler=(R(-25*lk+6*math.sin(t*20)*lk),0,0)
                face(V,mouth='grin' if lk>.2 else 'flat',brow=.06*lk,eyes=1+.1*lk); V['arm'][1].rotation_euler=(R(-20*lk),0,R(30*lk)); V['arm'][-1].rotation_euler=(R(-20*lk),0,R(-30*lk))
                for m in mins: blink(m,t); stand(m,t)
                face(H,mouth='flat',brow=-.02,brow_r=14)
                q=ease(t/DUR); camset((-4.5,-1.4,2.6),(7,0,2.7),40+5*q,8.0)
        elif view=='you':
            def upd(t):
                blink(V,t); stand(V,t); arm_to(V,1,(-3,0,1.6),ease(t/.3)); face(V,mouth='shout' if (t%0.5)<.35 else 'grin',brow=-.04,brow_r=18)
                V['root'].rotation_euler[0]=R(8); q=ease(t/DUR); camset((2.6,-1.3,2.6),(7,0,3.3),34+6*q,4.0,focus=(7,0,3.2))
        elif view=='charge':
            def upd(t):
                blink(V,t); V['root'].location[0]=7-5.5*ease_in(min(1,t/DUR)*.8+.2*min(1,t/DUR)); run(V,V['root'].location[0]*-1,arm=60); V['root'].rotation_euler[0]=R(18); face(V,mouth='shout',brow=-.05,brow_r=20)
                for i,m in enumerate(mins): blink(m,t); m['root'].location[0]=10.5+(i%3)*1.4-3*t; run(m,3*t+i)
                SHAKE[0]=.02; camset((-1.4,-.5,1.0),(5,0,2.4),22,8.0)
        elif view=='shake':
            V['root'].location[0]=.8
            def upd(t):
                blink(V,t); stand(V,t); jitter(V,t,3.0+4*ease(t/2)); face(V,mouth='strain' if t<2.0 else 'O',brow=.1,eyes=1.2)
                k=ease((t-2.0)/.5); kneel(V,k,bow=.5) if k>0 else None
                if k>0: jitter(V,t,2)
                q=ease(t/DUR); camset((-1.7,-3.8,1.6),(.8,0,2.0-.6*k),26,6.0)
        elif view=='army':
            hideH(H); V['root'].location=(.8,0,.008); kneel(V,1,bow=.5)
            for i,m in enumerate(mins): m['x']=m['root'].location[0]-6; m['y']=m['root'].location[1]; m['root'].location[0]-=6
            def upd(t):
                for i,m in enumerate(mins): blink(m,t); flee(m,t,90,5.0,t0=.1*(i%3)); face(m,mouth='O',brow=.12)
                camset((-1.0,-4.5,1.4),(6,0,1.6),22,8.0)
    elif view in ('step1','step2','faster','glasses','nobody','ask','look','whisper','end'):
        H,g=mkhuss((-3,0,0),90)
        V=av((.8,0,0),-90,VILL,{'mouth':'O'},name='vill') if view in ('step1','step2','faster','nobody') else None
        cops=[av((x,y,0),rz,cop(i),{'mouth':'o'},name='c%d'%i) for i,(x,y,rz) in enumerate([(-4.6,-2.2,-30),(-1.5,-2.4,30),(-3.0,-2.9,0)])] if view in ('nobody','ask','look','whisper','inhaler','end') else []
        if view in ('step1','step2'):
            hw=wl(143 if view=='step1' else 146,KEY); breath(H,[hw],size=.12,n=7); shockwave((-2.5,0,.06),hw,5.0,.7)
            def upd(t):
                blink(H,t,0); stand(H,t); k=ease((t-(hw-.5))/.45); H['root'].location[0]=-3+(.6 if view=='step2' else 0)+.6*k
                H['leg'][1].rotation_euler[0]=R(-28*math.sin(pi*k)); face(H,mouth='O' if 0<t-hw<.3 else 'flat',brow=-.02,brow_r=14)
                if V: V['root'].location[0]=5-2.0*min(1,t/DUR)*(1 if view=='step1' else .3); run(V,t*3,arm=50); V['root'].rotation_euler[2]=R(-90); face(V,mouth='shout')
                SHAKE[0]=.03*max(0,1-abs(t-hw-.05)/.25)
                if view=='step1': camset((-2.6,-4.6,1.1),(-2.4,0,1.1),28,8.0)
                else: q=ease(t/DUR); camset((-5.5,-2.2,1.2),(1,0,1.6),24,8.0)
        elif view=='faster':
            hs=[wl(i,KEY) for i in range(152,157)]; breath(H,hs,size=.1,n=5)
            for i,h in enumerate(hs): shockwave((-1.8,0,1.9),h,3.0+i*.4,.5)
            def upd(t):
                blink(H,t,0); stand(H,t); H['root'].location[0]=-1.8; face(H,mouth='O' if any(0<=t-h<.12 for h in hs) else 'strain',brow=-.03,brow_r=16)
                k=max([max(0,1-abs(t-h-.05)/.12) for h in hs]+[0]); H['root'].scale=(1+.04*k,1+.04*k,1); SHAKE[0]=.02+.03*k if t>hs[0]-.2 else 0
                q=ease(t/DUR); camset((-.6,-1.5,2.25),(-1.8,0,2.35),36+10*q,3.2,focus=(-1.8,-.2,2.3))
        elif view=='glasses':
            def upd(t):
                blink(H,t,0); stand(H,t); k=ease((t-.5)/1.6); arm_to(H,1,tuple(g.matrix_world.translation),min(1,k*3) if k<.95 else 1-ease((t-2.3)/.4))
                glasses_off(g,k); face(H,mouth='flat',brow=-.04,brow_r=16,eyes=1.0)
                q=ease(t/DUR); camset((-1.5,-1.1,2.25),(-3,0,2.35),44+8*q,3.0,focus=(-3,0,2.3))
        elif view in ('nobody','ask','look','whisper','end'):
            if V: V['root'].location[0]=.8; kneel(V,1,bow=.5)
            if view=='whisper': hw=wl(192,KEY)
            if view=='end': hs=[wl(i,KEY) for i in (201,202,203)]; breath(H,hs,size=.1,n=5); inh=inhaler(H['arm'][1],(.5*H['u'],-.1,-1.95*H['u']))
            def upd(t):
                blink(H,t,0); stand(H,t)
                for i,c in enumerate(cops):
                    blink(c,t); stand(c,t); look_at(c,(-3,0,2.3))
                    if view=='nobody': c['head'].rotation_euler[1]=R(14*math.sin(t*2+i)); face(c,mouth='flat',brow=.1,brow_r=-12)
                    if view=='ask' and i==1: arm_to(c,1,(-3,0,2.0),.8); mouth_talk(c,t,wl(179,KEY)-.05,wl(182,KEY)+.7,shapes=('O','o','O'),rate=7); c['root'].rotation_euler[0]=R(6)
                    if view=='whisper': k=ease((t-.6)/.4); c['root'].rotation_euler[0]=R(14*k); face(c,mouth='o',brow=.08)
                    if view=='end': flee(c,t,c['rz']+180,5.0,t0=.25+.1*i); face(c,mouth='O',brow=.12)
                if view=='nobody':
                    face(H,mouth='flat',brow=-.02,brow_r=12); q=ease(t/DUR); camset((-2.2,-6.3,1.7),(-2.2,-1,1.7),24,8.0)
                elif view=='ask':
                    H['root'].rotation_euler[2]=R(20); face(H,mouth='flat',brow=-.02,brow_r=12); q=ease(t/DUR); camset((-2.6,-5.2,1.9),(-2.3,-1.8,1.9),26+6*q,5.0)
                elif view=='look':
                    H['root'].rotation_euler[2]=R(20); k=ease((t-.9)/1.3); arm_to(H,1,tuple(g.matrix_world.translation),min(1,k*3) if k<.95 else 0); glasses_off(g,k); face(H,mouth='flat',brow=-.03,brow_r=14)
                    q=ease(t/DUR); camset((-3.4,-2.0,2.3),(-3,0,2.35),40+6*q,3.0,focus=(-3,0,2.3))
                elif view=='whisper':
                    hide(g); H['root'].rotation_euler[2]=R(20); face(H,mouth='o' if hw<t<hw+.5 else 'flat',brow=.02,brow_r=-6,eyes=.9); H['head'].rotation_euler[0]=R(6)
                    q=ease(t/DUR); camset((-3.0,-1.55,2.38),(-3,0,2.3),38+8*q,2.4,focus=(-3,-.2,2.3))
                elif view=='end':
                    hide(g); H['root'].rotation_euler[2]=R(20); k=ease(t/.25); arm_to(H,1,tuple(H['head'].matrix_world@Vector((0,-.9*H['u'],.3*H['u']))),k)
                    face(H,mouth='O' if any(0<=t-h<.25 for h in hs) else 'flat',brow=.05,brow_r=-8,eyes=1.1)
                    q=ease(t/DUR); camset((-3.4,-4.2+.6*q,1.8),(-3,0,2.0),26,6.0)
    elif view=='inhaler':
        H,g=mkhuss((-3,0,0),20); hide(g)
        inh=inhaler(None,(-2.85,-.3,1.6)); r_=random.Random(2)
        def upd(t):
            blink(H,t,0); stand(H,t); face(H,mouth='flat',brow=.06,brow_r=-6)
            q=min(1,t/.7); z=max(.04,1.6-1.6*q*q)+(.12*abs(math.sin((t-.7)*9))*math.exp(-(t-.7)*3) if t>.7 else 0)
            inh.location=(-2.85+.2*min(1,t),-.3-.2*min(1,t),z); inh.rotation_euler=(t*6 if t<.7 else R(90),t*3 if t<.7 else 0,0)
            camset((-2.0,-1.9,.25),(-2.7,-.45,.25+.6*(1-min(1,t/.7))),40,2.8,focus=(-2.65,-.5,.2))
    if upd is None:
        def upd(t): camset((0,-6,1.8),(0,0,1.8),24)
    return dict(upd=upd)
for _v in ('hook','city','name','why','lambo','arrive','destroy','sees','you','glasses','charge','step1','step2','faster','shake','army','nobody','ask','look','whisper','inhaler','end'): SHOTS['S_'+_v]=(lambda v=_v: ST_(v))

# =================================================================== APARTMENT (3:47 AM)
def AP_(view):
    mir=apartment(); w,bg=setup_dark('#0A1020',.35,res=PCT,samples=SAMPLES,bloom=.08); KEY='A_'+view
    moon=area((-4.2,1.8,2.2),300,(1.5,1.2),(.55,.7,1.0),rot=(R(-90),0,0)); fill=point((1.5,-1.0,2.6),40,(.6,.7,1.0),.5,shadow=False)
    if view=='clock': point((-1.15,1.6,.9),3,(1,.25,.2),.1,shadow=False); point((-2.6,-.2,2.5),70,(.55,.65,1.0),.4,shadow=False)
    if view in ('brush','mirror'): point((1.5,1.6,2.6),45,(1,.95,.85),.2)
    if view=='mirror': point((2.4,.9,2.4),70,(1,.92,.8),.3,shadow=False); point((1.5,2.3,2.0),25,(.8,.9,1.0),.2,shadow=False)
    if view=='break': point((5.0,1.5,2.6),45,(1,.9,.75),.2)
    H,g=mkhuss((-2.6,1.4,0),0)
    if view=='clock':
        u=H['u']
        def upd(t):
            blink(H,t,0); k=1 if t>=1.6 else 0
            if not k:
                H['root'].location=(-2.6,2.15-4.75*u,.82); H['root'].rotation_euler=(R(-90),0,R(180)); legs0(H)
                H['root'].rotation_euler=(R(-90),0,0); H['root'].location=(-2.6,2.15-4.75*u,.82)
                face(H,mouth='flat',brow=0,eyes=1.0)
            else:
                H['root'].rotation_euler=(0,0,0); H['root'].location=(-2.6,1.0,0); H['z0']=0; sit(H,1,.72,90); face(H,mouth='flat',brow=-.03,brow_r=14)
            if t<1.6: camset((-1.0,1.3,.8),(-1.15,1.9,.74),45,2.4,focus=(-1.15,1.85,.74))
            else: q=ease((t-1.6)/(DUR-1.6)); camset((-2.6,-1.6,1.9),(-2.6,1.0,1.7),30+6*q,5.0)
    elif view in ('brush','break'):
        cx=1.8 if view=='brush' else 4.4
        def upd(t):
            blink(H,t); walker(H,(cx-2.4,1.25,0),-90+180,1.8,t,arm=12); face(H,mouth='flat',brow=-.02,brow_r=12)
            camset((cx-.35,1.3,1.25),(cx,2.15,1.0),40,2.2,focus=(cx,2.15,1.0))
    elif view=='mirror':
        H['root'].location=(1.5,1.55,.008); H['root'].rotation_euler[2]=R(180)
        hs=[wl(i,KEY) for i in (50,51,52)]; breath(H,hs,size=.08,n=4)
        mm=mir.data.materials[0]; mb=mm.node_tree.nodes['Principled BSDF']
        def upd(t):
            blink(H,t,0); stand(H,t); H['root'].location=(1.5,1.55,.008)
            face(H,mouth='O' if any(0<=t-h<.25 for h in hs) else 'flat',brow=-.03,brow_r=16)
            k=max([max(0,1-abs(t-h-.08)/.18) for h in hs]+[0]); H['root'].scale=(1+.03*k,1+.03*k,1)
            fog=min(1,sum(max(0,t-h) for h in hs)*.5); mb.inputs['Roughness'].default_value=.03+.6*fog; mb.inputs['Base Color'].default_value=tuple(L(a,b,fog) for a,b in zip(hexc('#BFD0E0'),hexc('#EEF2F5')))
            q=ease(t/DUR); camset((2.6,.85,2.4),(1.45,2.2,2.2),26+6*q,4.0,focus=(1.5,1.7,2.3))
    return dict(upd=upd)
for _v in ('clock','brush','break','mirror'): SHOTS['A_'+_v]=(lambda v=_v: AP_(v))

# =================================================================== PARK (south side of the avenue)
def PK_(view):
    CLEARP[0]=(view=='400'); street(); day(); KEY='P_'+view
    H,g=mkhuss((24,-8.65,0),180)
    if view=='400':
        H['root'].location=(28,-14,.12); H['z0']=.12; H['root'].rotation_euler[2]=R(0)
        thugs=[]; r=random.Random(4)
        for ring_,n in ((2.2,8),(3.4,12),(4.6,14)):
            for i in range(n):
                a=2*pi*i/n+r.uniform(-.1,.1); x=28+ring_*math.cos(a); y=-14+ring_*math.sin(a)
                th=av((x,y,.12),math.degrees(math.atan2(28-x,-( -14-y))),minion(i+int(ring_*10)),{'mouth':'shout'},name='t%d_%d'%(i,int(ring_*10))); th['ring']=ring_; th['a']=a; thugs.append(th)
        hs=[.6,1.6,2.6]; breath(H,hs,size=.1,n=5)
        for h in hs: shockwave((28,-14,.15),h,6.0,.8)
        def upd(t):
            blink(H,t,0); stand(H,t); face(H,mouth='O' if any(0<=t-h<.25 for h in hs) else 'flat',brow=-.03,brow_r=14)
            for th in thugs:
                ring_=th['ring']; hit=hs[0]+(ring_-2.2)*.18; k=ease((t-hit)/.3)
                th['root'].rotation_euler[0]=R(-85*k); th['root'].location[2]=.12+.25*math.sin(pi*min(1,k)); face(th,mouth='O' if k>0 else 'shout')
            q=ease(t/DUR); camset((28+6.5*math.cos(-1.3+.4*q),-14+6.5*math.sin(-1.3+.4*q),9.0),(28,-14,.5),22,8.0)
    elif view in ('never','approach','huss','run'):
        cup=obox((0,0,0),(.05,.05,.07),M('#F4F1EA',.4),.01,H['arm'][1]); cup.location=(.5*H['u'],-.12,-1.95*H['u'])
        T=av((19.5,-8.5,.12),-90+180,TOUGH,{'mouth':'smirk'},name='tough')
        hs=[wl(i,KEY) for i in (87,88,89)] if view=='huss' else []
        if hs: breath(H,hs,size=.11,n=6)
        peek=[av((x,y,.12),rz,citizen(i+40),{'mouth':'o'},name='pk%d'%i) for i,(x,y,rz) in enumerate([(26.5,-11.5,200),(21.8,-11,160)])] if view=='never' else []
        def upd(t):
            blink(H,t,0); sit(H,1,.5,90); H['root'].location=(24,-8.65,H['root'].location[2])
            H['arm'][1].rotation_euler=(R(-60 if view!='never' else -70-25*ease(max(0,math.sin(t*1.6)))),0,R(10)); face(H,mouth='flat',brow=-.02,brow_r=12)
            for i,p in enumerate(peek): blink(p,t); stand(p,t); look_at(p,(24,-8.6,1.6)); p['root'].location[0]=p['x']+.25*math.sin(t*2+i)
            blink(T,t)
            if view=='never': hideH(T); q=ease(t/DUR); camset((25.4,-6.4,1.5),(24,-8.8,1.3),28,6.0)
            elif view=='approach':
                d=walk_path(T,[(19.5,-7.2),(22.9,-7.2)],t,0,DUR*.85); face(T,mouth='smirk',brow=-.04,brow_r=16); T['arm'][1].rotation_euler[0]+=R(-30)
                q=ease(t/DUR); camset((21.3,-5.0,1.7),(23.9,-8.6,1.2),24,8.0)
            elif view=='huss':
                T['root'].location=(22.9,-7.2,.12); T['root'].rotation_euler[2]=R(120)
                face(H,mouth='O' if any(0<=t-h<.2 for h in hs) else 'strain',brow=-.04,brow_r=16); H['arm'][1].rotation_euler=(R(-30),0,R(10))
                camset((23.8,-6.5,1.75),(24,-8.65,1.6),32,3.2,focus=(24,-8.6,1.6))
            elif view=='run':
                T['x']=22.9; T['y']=-7.2; flee(T,t,-135,6.0,t0=.15); face(T,mouth='O',brow=.14,eyes=1.3); T['root'].location[2]=.12
                camset((26.8,-8.6,3.6),(21.0,-6.2,.8),22,8.0)
    return dict(upd=upd)
for _v in ('400','never','approach','huss','run'): SHOTS['P_'+_v]=(lambda v=_v: PK_(v))
