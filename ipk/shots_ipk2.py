# India vs Pakistan - shots part 2: the secret call, the last over, blackout + buffering, the tie, the loop ending
def ph_set(side,who='dbm'):
    Hm,F=room_set(side,who); b=F['b']; ph=phone_of(b,-1 if side=='I' else 1); cp=cup_of(b,1) if side=='I' else None; return Hm,F,b,ph,cp
def boy_call(F,b,cp,t,k=1.0,h=3.35,fw=1.05,sx=1.15):
    """phone held up beside the face for a video call (Rohan keeps the cup in his other hand)"""
    sitp(b,t,lean=0); s=-1 if F['side']=='I' else 1
    if cp is not None: cup_hold(b,cp,t)
    phone_up(b,s,k,h=h,fw=fw,sx=sx)
def SECRET():
    Hm,F,wa,ph,cp=ph_set('P'); dad=F['d']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); sitp(wa,t,lean=0); k=ease(tl(t,.5,1.2)); g=tl(t,.05,.3)*(1-tl(t,.7,1.0))
        phone_up(wa,1,k,h=2.9,fw=1.2,sx=.9); look_at(wa,hp(dad) if g>.5 else handw(wa,1),1.0,maxyaw=70,maxpitch=28); face(wa,mouth='smirk' if k>.6 else 'flat',brow=.03,eyes=1.0)
        cam_one(wa,ease(t/DUR),side=.55,dist=3.9,lens=31,tz=-.4)
    return dict(upd=upd)
SHOTS['SECRET']=SECRET
def FRIENDS():
    P,I,FP,FI=dh_set(); php=phone_of(FP['b'],1); phi=phone_of(FI['b'],-1); cp=cup_of(FI['b'],1); dm=M('#8FE0FF',.3,emit=4.0)
    dots=[oico((0,0,-9),.06,dm,None,sub=1) for k in range(11)]; t1=ws(154)-.15
    def upd(t):
        for Hm,F,c in ((P,FP,None),(I,FI,cp)):
            home_lights(Hm,t); fam_idle(F,t,'tense'); b=F['b']; boy_call(F,b,c,t,1.0,h=3.6,fw=1.25,sx=.75)
            look_at(b,handw(b,-1 if F['side']=='I' else 1),1.0,maxyaw=60,maxpitch=25); face(b,mouth='grin',brow=.03,eyes=1.05)
        bpy.context.view_layer.update(); a=Vector(handw(FP['b'],1)); b_=Vector(handw(FI['b'],-1))
        for k,o in enumerate(dots):
            f=(k+1)/12; p=a.lerp(b_,f); p.x+=1.0*math.sin(pi*f)*(1 if k%2 else .9); p.y-=.5
            on=t>t1+k*.03; pulse=.6+.4*math.sin(t*14-k*.9); o.location=p if on else (0,0,-9); o.scale=tuple(3*[pulse])
        dh_cam(.2+.3*ease(t/DUR))
    return dict(upd=upd)
SHOTS['FRIENDS']=FRIENDS
def CALL(side,a,b_,m='smirk',dark=False,shout=False):
    def f():
        Hm,F,b,ph,cp=ph_set(side); glow=point((0,0,0),0,(.6,.8,1.0),r=.2,shadow=False)
        if dark: FILLE[0]=3
        def upd(t):
            frz=side=='I' and 200<a<250
            home_lights(Hm,t,power=0.0 if dark else 1.0,tv=0.0 if dark else (.5 if frz else 1.0),flick=0 if frz else 1)
            fam_idle(F,t,'shock' if dark else 'tense'); boy_call(F,b,cp,t)
            s=-1 if side=='I' else 1; bpy.context.view_layer.update(); hw=Vector(handw(b,s)); look_at(b,hw,1.0,maxyaw=50,maxpitch=20)
            face(b,mouth=m,brow=.05 if shout else .02,eyes=1.2 if shout else 1.0); speak(b,t,a,b_,gesture=False)
            if shout: b['head'].rotation_euler[0]=R(-10*tl(t,0,.2)); b['root'].location[2]+=.02*math.sin(t*30)
            glow.location=hw+Vector((-s*.25,-.35,.1)); glow.data.energy=26 if dark else 5
            cam_one(b,ease(t/DUR),side=-.3*s,dist=3.1,lens=33,tz=-.12)
        return dict(upd=upd)
    return f
SHOTS['GAYE']=CALL('P',155,159,'smirk'); SHOTS['SAPNE']=CALL('I',160,162,'smirk')
SHOTS['TERE']=CALL('P',220,224,'o',dark=True); SHOTS['NAHI']=CALL('I',225,227,'o'); SHOTS['NAHI2']=CALL('P',228,228,'shout',dark=True,shout=True)
SHOTS['PHIRSE']=CALL('P',270,272,'frown'); SHOTS['PHIRSE2']=CALL('I',273,274,'flat')
def KISSE():
    Hm,F,wa,ph,cp=ph_set('P'); dad=F['d']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); boy_call(F,wa,cp,t); face(wa,mouth='o',brow=.06,eyes=1.25); look_at(wa,hp(dad),tl(t,.25,.45),maxyaw=38)
        a=ease(tl(t,0,.2)); look_at(dad,hp(wa),a,maxyaw=52); mood(dad,'glare'); dad['root'].rotation_euler[1]=R(-7*a); speak(dad,t,163,168,gesture=False)
        q=ease(t/DUR); camset(LV((.4,-3.75,2.1),(.34,-3.45,2.06),q),(0,1.42,1.72),26,8)
    return dict(upd=upd)
SHOTS['KISSE']=KISSE
def KOINAHI():
    Hm,F,wa,ph,cp=ph_set('P'); dad=F['d']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); sitp(wa,t,lean=0); look_at(dad,hp(wa),1.0,maxyaw=80); mood(dad,'glare')
        k=ease(tl(t,0,.18)); wa['arm'][1].rotation_euler=(R(L(-100,38,k)),R(8*k),0); wa['arm'][-1].rotation_euler=(R(-40),R(4),0)
        look_at(wa,hp(dad),.55,maxyaw=70); face(wa,mouth='grin',brow=.06,brow_r=10,eyes=1.1); speak(wa,t,169,171,gesture=False)
        cam_one(wa,ease(t/DUR),side=-.5,dist=3.4,lens=32,tz=-.2)
    return dict(upd=upd)
SHOTS['KOINAHI']=KOINAHI
# ---------------------------------------------------------------- the TV (reverse shots)
def tv_cam(k=0.0,close=False):
    if close: camset(LV((.25,2.3,1.95),(.1,1.95,1.93),k),(0,-3.36,1.8),31,8)
    else: camset(LV((-.5,2.55,2.05),(-.3,2.2,2.0),k),(0,-3.36,1.72),30,8)
def TVSHOT(side,pages,who='',pop=None,close=False,spin=None,flick=1):
    """pages: list of (t_from, [groups]) ; spin=(t0,t1) shows the buffering wheel over a dimmed picture"""
    def f():
        Hm=home(side,0.0,tvwall=True); home_world(); F=family(side,0.0,who) if who else None; FILLE[0]=10; TV=Hm['tv']; pg=[(tf() if callable(tf) else tf,g) for tf,g in pages]
        pp=(pop[0],pop[1]()) if pop else None
        def upd(t):
            sp=spin is not None and spin[0]<=t<spin[1]
            home_lights(Hm,t,tv=.5 if sp else 1.0,flick=0 if sp else flick)
            if F: fam_idle(F,t,'tense')
            g=[x for tf,x in pg if t>=tf][-1]
            tv_show(TV,(['field','dark','spin'] if sp else g),t,pop=pp)
            tv_cam(ease(t/DUR),close)
        return dict(upd=upd)
    return f
SHOTS['LASTOV']=TVSHOT('P',[(-9,['field','dark','lastover'])],pop=('lastover',lambda: .1))
SHOTS['ONEBALL']=TVSHOT('I',[(-9,['field','dark','oneball']),(lambda: ws(179)-.06,['field','dark','oneball','tworuns'])],pop=('tworuns',lambda: ws(179)-.06))
SHOTS['BUFFERTV']=TVSHOT('I',[(-9,['field'])],spin=(.18,99))
SHOTS['STREAM']=TVSHOT('I',[(-9,['field'])],spin=(-1,.5))
SHOTS['TIED']=TVSHOT('P',[(-9,['field','dark','tied']),(lambda: ws(260)-.08,['field','dark','super'])],who='',pop=('super',lambda: ws(260)-.08),close=True,flick=.3)
def BREATH():
    P,I,FP,FI=dh_set()
    def upd(t):
        for Hm,F in ((P,FP),(I,FI)):
            home_lights(Hm,t); fam_idle(F,t,'tense'); k=ease(tl(t,0,.6))
            for q in 'db':
                H=F[q]; sitp(H,t,lean=13*k,up=.12*k if q=='d' else 0); look_at(H,TVP(F['z0']),1.0); face(H,mouth='flat',brow=.06,brow_r=6,eyes=1.25)
                for s in (1,-1): H['arm'][s].rotation_euler=(R(-62),R(s*8),0)
                H['root'].location[0]+=.006*math.sin(t*31+H['seed'])
        dh_cam(.3+.5*ease(t/DUR))
    return dict(upd=upd)
SHOTS['BREATH']=BREATH
# ---------------------------------------------------------------- LIGHT CHALI GAYI / buffering
def LIGHT():
    Hm,F=room_set('P'); dad=F['d']; t1=ws(195)-.07
    def upd(t):
        on=t<t1; FILLE[0]=16 if on else 3
        home_lights(Hm,t,power=1.0 if on else 0.0,tv=1.0 if on else 0.0); fam_idle(F,t,'tense' if on else 'shock')
        if not on:
            k=ease(tl(t,t1+.05,t1+.3)); sitp(dad,t,up=k); arms_up(dad,k,t,spread=22,jig=8); face(dad,mouth='shout',brow=.06,eyes=1.25); speak(dad,t,195,197,gesture=False)
            dad['head'].rotation_euler[0]=R(-14*k)
            for q in 'bmg': look_at(F[q],(0,0,3.3),.6)
        cam_wide(ease(t/DUR))
    return dict(upd=upd)
SHOTS['LIGHT']=LIGHT
def BUFFER():
    Hm,F,ro,cp=cup_set(); dad=F['d']
    def upd(t):
        home_lights(Hm,t,tv=.5,flick=0); fam_idle(F,t,'shock'); sitp(ro,t,lean=0); cup_hold(ro,cp,t); k=ease(tl(t,.05,.35))
        look_at(ro,hp(dad),k,maxyaw=70); face(ro,mouth='flat',brow=.05,brow_r=10,eyes=1.15); speak(ro,t,201,205,gesture=False)
        bpy.context.view_layer.update(); arm_to(ro,-1,(BOYP[0]-.3,-3.3,1.7),k,base=(R(-40),R(4),0))
        tw=math.sin(t*38)*(t>ws(202)); face(dad,mouth='O',brow=.06,brow_r=0,eyes=1.3); dad['head'].rotation_euler[2]=R(2.5*tw)
        cam_two(ease(t/DUR),dx=.2,tx=0)
    return dict(upd=upd)
SHOTS['BUFFER']=BUFFER
def panic(dad,t,ph=0.0):
    """dad on his feet in front of the sofa: hands on head, then pacing, then arms to the sky"""
    a=tl(t,.1,.45); pc=tl(t,1.3,1.6)*(1-tl(t,3.0,3.3)); sky=ease(tl(t,3.2,3.6))
    x=DADP[0]-.42*math.sin((t-1.3)*3.4)*pc; sitp(dad,t,up=ease(a)); dad['root'].location[0]=x
    if pc>0: walk(dad,abs(.42*math.cos((t-1.3)*3.4))*8,step=.3,arm=0); dad['root'].location[2]=dad['z0']+.008
    what_pose(dad,a*(1-sky),t,amp=.6);
    if sky>0: arms_up(dad,sky,t,spread=24,jig=6); dad['head'].rotation_euler[0]=R(-22*sky)
    face(dad,mouth='shout' if sky>.5 else 'O',brow=.06,eyes=1.25)
def PROBLEM():
    P,I,FP,FI=dh_set(); php=phone_of(FP['b'],1); glow=point((0,0,0),22,(.6,.8,1.0),r=.2,shadow=False)
    def upd(t):
        home_lights(P,t,power=0.0,tv=0.0); home_lights(I,t,tv=.5,flick=0)
        for F in (FP,FI):
            fam_idle(F,t,'shock'); panic(F['d'],t); b=F['b']; look_at(b,hp(F['d']),1.0,maxyaw=80)
        phone_up(FP['b'],1,1.0,h=3.3,fw=1.25,sx=.8); bpy.context.view_layer.update(); glow.location=Vector(handw(FP['b'],1))+Vector((-.2,-.4,.2))
        dh_cam(.1+.5*ease(t/DUR))
    return dict(upd=upd)
SHOTS['PROBLEM']=PROBLEM
def HEARD():
    P,I,FP,FI=dh_set(); fl=[point((6.5,2.5,z+2.3),0,(1,.85,.6),r=1.0,shadow=False) for z in (0,UPZ)]
    def upd(t):
        home_lights(P,t,power=0.0,tv=0.0); home_lights(I,t,tv=.5,flick=0); k=ease(tl(t,.35,.6))
        for F,L_ in ((FP,fl[0]),(FI,fl[1])):
            fam_idle(F,t,'shock'); sitp(F['d'],t,up=1.0); what_pose(F['d'],1-k,t,amp=.3)
            for q in 'db': look_at(F[q],(7.0,2.0,F['z0']+2.4),k,maxyaw=85); face(F[q],mouth='o',brow=.06,eyes=1.2)
            L_.data.energy=260*k*(.6+.4*math.sin(t*23))
        dh_cam(.5)
    return dict(upd=upd)
SHOTS['HEARD']=HEARD
def SOMETHING():
    P,I,FP,FI=dh_set(); t1=ws(239)-.1
    def upd(t):
        home_lights(P,t,power=0.0,tv=0.0); home_lights(I,t,tv=.5,flick=0)
        for F in (FP,FI):
            fam_idle(F,t,'shock'); dad,b=F['d'],F['b']; sitp(dad,t,up=1.0); g=math.sin(t*5.5)
            if t<t1: look_at(dad,hp(b) if g>0 else (7,2,F['z0']+2.4),1.0,maxyaw=80); look_at(b,hp(dad) if g<0 else (7,2,F['z0']+2.4),1.0,maxyaw=80); what_pose(dad,.8,t,amp=.4)
            else:
                d=min(3.9,(t-t1)*4.6); pts=[(DADP[0],DADP[1]-.85),(DADP[0]+.5,.05),(2.0,.02),(3.0,-.5)]
                walk_path(dad,pts,t,t1,t1+.9,z=F['z0'],step=.5,run_=True); look_at(b,hp(dad),1.0,maxyaw=85)
            face(dad,mouth='O',brow=.06,eyes=1.2); face(b,mouth='o',brow=.06,eyes=1.15)
        dh_cam(.5+.2*ease(t/DUR))
    return dict(upd=upd)
SHOTS['SOMETHING']=SOMETHING
def BACKS():
    Hm,F=room_set('P','bmg'); t1=.28
    def upd(t):
        on=t>=t1 and not (t1+.1<t<t1+.17); FILLE[0]=16 if on else 3
        home_lights(Hm,t,power=1.0 if on else 0.0,tv=1.0 if t>t1+.5 else 0.0); fam_idle(F,t,'shock' if t<t1+.4 else 'tense')
        if t1<t<t1+.6:
            for q in 'bmg': look_at(F[q],(0,-.3,3.3),1.0,maxpitch=40)
        cam_wide(ease(t/DUR))
    return dict(upd=upd)
SHOTS['BACK']=BACKS
def SCREEN():
    P,I,FP,FI=dh_set()
    def upd(t):
        for Hm,F in ((P,FP),(I,FI)):
            home_lights(Hm,t,flick=.4); fam_idle(F,t,'tense'); dad=F['d']; sitp(dad,t,up=1.0); dad['root'].rotation_euler[0]=R(9*ease(tl(t,0,.5))); look_at(dad,TVP(F['z0']),1.0)
            face(dad,mouth='flat',brow=.06,eyes=1.2); sitp(F['b'],t,lean=13); look_at(F['b'],TVP(F['z0']),1.0); face(F['b'],mouth='flat',brow=.06,eyes=1.2)
        dh_cam(.3+.5*ease(t/DUR))
    return dict(upd=upd)
SHOTS['SCREEN']=SCREEN
# ---------------------------------------------------------------- the faint
FNT=(1.9,-2.05)
def FAINT(side):
    def f():
        Hm,F=room_set(side); dad=F['d']; t0=.22
        def upd(t):
            home_lights(Hm,t,tv=.38,flick=.4); fam_idle(F,t,'shock')
            if t<t0: standp(dad,t,FNT[0],FNT[1],90); look_at(dad,TVP(),1.0,maxyaw=70); what_pose(dad,1,t,amp=.3); face(dad,mouth='O',brow=.06,eyes=1.3)
            else: faintp(dad,t,t0,FNT[0],FNT[1],90)
            for q in 'bmg': look_at(F[q],hp(dad),1.0 if t>t0+.2 else .4,maxyaw=85,maxpitch=40)
            q=ease(t/DUR); camset(LV((.2,-6.5,3.2),(.25,-6.2,3.15),q),(.6,-.9,.75),22,8)
        return dict(upd=upd)
    return f
SHOTS['FAINTP']=FAINT('P'); SHOTS['FAINTI']=FAINT('I')
def SAMETIME():
    P,I,FP,FI=dh_set()
    def upd(t):
        for Hm,F in ((P,FP),(I,FI)):
            home_lights(Hm,t,tv=.35,flick=.4); fam_idle(F,t,'shock'); dad,b=F['d'],F['b']; faintp(dad,t,-2.0,FNT[0],FNT[1],90)
            sitp(b,t,lean=14,up=.15); look_at(b,(.8,FNT[1],F['z0']+.3),1.0,maxyaw=80,maxpitch=40); face(b,mouth='o',brow=.06,eyes=1.2)
            for s in (1,-1): b['arm'][s].rotation_euler=(R(-62),R(s*8),0)
        k=ease(t/DUR); camset((0,-16+1.0*k,3.2),(0,1.55,3.2),72,8)
    return dict(upd=upd)
SHOTS['SAMETIME']=SAMETIME
def SATBACK():
    P,I,FP,FI=dh_set(); cp=cup_of(FI['b'],1); t1=ws(277)-.1
    def upd(t):
        for Hm,F in ((P,FP),(I,FI)):
            home_lights(Hm,t); fam_idle(F,t,'tense'); dad=F['d']; k=1-ease(tl(t,t1,t1+.45)); sitp(dad,t,up=k); look_at(dad,TVP(F['z0']),1.0)
            if k<=0: crossed(dad)
        cup_hold(FI['b'],cp,t); dh_cam(.4+.3*ease(t/DUR))
    return dict(upd=upd)
SHOTS['SATBACK']=SATBACK
def SEATS():
    Hm,F,ro,cp=cup_set('dbm'); dad=F['d']
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); sitp(ro,t,lean=0); cup_hold(ro,cp,t); look_at(ro,TVP(),1.0); face(ro,mouth='flat',brow=.05,eyes=1.15); crossed(dad)
        q=ease(t/DUR); camset(LV((.2,-4.9,2.1),(.6,-3.6,1.95),q),LV((0,1.42,1.75),(BOYP[0]-.2,1.3,1.7),q),27,8)
    return dict(upd=upd)
SHOTS['SEATS']=SEATS
def NOBODY():
    Hm,F=room_set('P')
    def upd(t):
        home_lights(Hm,t); fam_idle(F,t,'tense'); crossed(F['d']); g=1 if (t*2.2)%1.0<.5 else -1
        for q in 'dbmg':
            H=F[q]; sitp(H,0.0,lean=11); look_at(H,TVP(),1.0); blink(H,0.0,force=0); face(H,mouth='flat',brow=.06,eyes=1.2); H['head'].rotation_euler[2]+=R(5*g*(1 if q in 'bm' else -1))
        crossed(F['d']); cam_wide(ease(t/DUR))
    return dict(upd=upd)
SHOTS['NOBODY']=NOBODY
# ---------------------------------------------------------------- the loop: LIGHT! + CTA
def hand_flag(H,s,side):
    def b(e):
        ocyl((0,-.06,-.5),.02,1.25,M('#D8D2C4',.5),e,rot=(0,0,0),seg=6)
        if side=='P':
            obox((.36,-.06,-.92),(.27,.008,.2),M('#01411C',.7,kind='fabric'),0,e); obox((.05,-.06,-.92),(.07,.008,.2),M('#F8F8F4',.7),0,e)
            ocyl((.36,-.07,-.92),.1,.006,M('#F8F8F4',.7),e,rot=(R(90),0,0),seg=18); ocyl((.39,-.075,-.95),.085,.006,M('#01411C',.7),e,rot=(R(90),0,0),seg=18)
            ocyl((.36,-.05,-.92),.1,.006,M('#F8F8F4',.7),e,rot=(R(90),0,0),seg=18); ocyl((.39,-.045,-.95),.085,.006,M('#01411C',.7),e,rot=(R(90),0,0),seg=18)
        else:
            for k,c in enumerate(('#138808','#F8F8F4','#FF9933')): obox((.3,-.06,-1.05+k*.133),(.32,.008,.0667),M(c,.7,kind='fabric'),0,e)
            for dy in (-.07,-.05): ocyl((.3,dy,-.917),.05,.006,M('#000080',.6),e,rot=(R(90),0,0),seg=14)
    return in_hand(H,s,b)
def LIGHT2():
    P,I,FP,FI=dh_set(); t1=.14
    def upd(t):
        on=t<t1; home_lights(P,t,power=1.0 if on else 0.0,tv=1.0 if on else 0.0); home_lights(I,t)
        fam_idle(FP,t,'tense' if on else 'shock'); fam_idle(FI,t,'tense'); crossed(FI['d'])
        if not on:
            k=ease(tl(t,t1+.05,t1+.25)); dad=FP['d']; sitp(dad,t,up=k); arms_up(dad,k,t,spread=22,jig=8); face(dad,mouth='shout',brow=.06,eyes=1.25)
            g=ease(tl(t,t1+.2,t1+.45))
            for q in 'db': look_at(FI[q],(FI[q]['root'].location[0],.6,UPZ-2.0),g,maxpitch=40); face(FI[q],mouth='o',brow=.06,eyes=1.2)
        dh_cam(.7)
    return dict(upd=upd)
SHOTS['LIGHT2']=LIGHT2
def CTA():
    P,I,FP,FI=dh_set(); torch=point((0,0,0),0,(.75,.86,1.0),r=.25,shadow=False); php=phone_of(FP['b'],1)
    ti=ws(299)-.1; tp=ws(301)-.25
    def upd(t):
        home_lights(P,t,power=0.0,tv=0.0); home_lights(I,t,tv=.5,flick=0); P['moon'].data.energy=120
        fam_idle(FP,t,'shock'); fam_idle(FI,t,'shock'); sitp(FP['d'],t,up=1.0); what_pose(FP['d'],1,t,amp=.4); FP['d']['head'].rotation_euler[0]=R(-18); face(FP['d'],mouth='shout',brow=.06,eyes=1.2)
        hands=tl(t,.3,.6); what_pose(FI['d'],hands,t,amp=.3); face(FI['d'],mouth='O',brow=.06,eyes=1.25)
        up=ease(tl(t,.5,1.1))
        for F,tt in ((FP,tp),(FI,ti)):
            b=F['b']; sitp(b,t,up=up); look_at(b,(b['root'].location[0],-16,F['z0']+2.0),1.0); k=ease(tl(t,tt,tt+.3))
            face(b,mouth='grin' if k>.5 else 'smirk',brow=.04,eyes=1.05); b['arm'][1].rotation_euler=(R(-30*up),R(-34*up),0)
            b['arm'][-1].rotation_euler=(R(-162*k+6*math.sin(t*9)*k),R(-18*k),0)
        phone_up(FP['b'],1,up,h=3.4,fw=1.2,sx=.9); bpy.context.view_layer.update(); torch.location=Vector(handw(FP['b'],1))+Vector((-.35,-.5,.4)); torch.data.energy=60
        dh_cam(.2+.6*ease(min(1,t/4.5)))
    return dict(upd=upd)
SHOTS['CTA']=CTA
