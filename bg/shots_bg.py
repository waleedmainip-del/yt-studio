# Shots for "Baddie Ghar Par". SEQ/END are filled by gen_seq.py from the narration words; storyboard uses provisional times.
SHOTS={}
END=103.0667
SEQ=[('CAFE_HOOK', 0.0), ('HOOK_SINK', 2.933), ('ZOYA_INTRO', 5.5), ('VLOG', 11.233), ('RIDE', 14.667), ('GATE_REVEAL', 17.233), ('AMMI_IN', 20.167), ('STARE', 23.433), ('BRIBE1', 25.133), ('LIVE', 28.067), ('LIVE2', 32.0), ('UI_LIVE_END', 33.5), ('BRIBE2', 34.367), ('CAFE_FRIENDS', 35.367), ('PHONE_UNDER', 40.033), ('UI_RATING', 42.7), ('WALEED_TYPE', 45.3), ('UI_COMMENT', 49.033), ('UI_PROFILE', 53.067), ('ZOYA_SMILE', 55.1), ('CONFRONT', 56.367), ('DEAL', 62.267), ('DEFEAT', 68.433), ('AMMI_GATE', 72.833), ('UI_RISHTA', 77.367), ('INVITE', 81.7), ('DINNER', 84.567), ('ORDER', 88.267), ('SINK_TALK', 91.733), ('MORAL', 94.3), ('CTA', 99.9)]
BALLS=[]
import os as _os
W_=json.load(open(LH+'/audio/words.json')) if _os.path.exists(LH+'/audio/words.json') else []
def wt(a,b): return (W_[a]['s'],W_[b]['e']) if W_ else (T0+.2,T0+1.5)
def ws(i): return W_[i]['s']-T0 if W_ else .3
def we(i): return W_[i]['e']-T0 if W_ else 1.5
def mk(C,x,y,rz,name,z=0.0): return avatar_bg((x,y,z),rz,C,name=name)
def fwd(rz): return (math.sin(R(rz)),-math.cos(R(rz)))
def drift(c0,tg,t,a=.06): q=ease(t/DUR); return LV(c0,(L(c0[0],tg[0],a),L(c0[1],tg[1],a),c0[2]),q)
def closecam(H,rz,side=.3,dist=3.0,dz=.05,tz=-.3,lens=36,bias=0.0):
    h=hp(H); f=fwd(rz); f=(f[0],f[1]-bias); n_=math.hypot(*f); f=(f[0]/n_,f[1]/n_); rt=(-f[1],f[0])
    return (h[0]+f[0]*dist+rt[0]*side,h[1]+f[1]*dist+rt[1]*side,h[2]+dz),(h[0],h[1],h[2]+tz),lens
def bike_obj(x,y,rz):
    mb=motorbike((x,y,0),rz,'#C8372D'); mb['root'].scale=(1.4,)*3
    bx=obox((-.95,0,1.35),(.34,.32,.3),M('#E2482A',.5),.04,mb['root']); obox((-.95,-.325,1.38),(.26,.005,.2),M('#F4F1EA',.6),0,mb['root'])
    stext('TEZ',(-.95,-.335,1.44),.11,'#E2482A',parent=mb['root']); stext('DELIVERY',(-.95,-.335,1.3),.05,'#16171C',parent=mb['root'])
    return mb
def food_bag(H,s=-1):
    u=H['u']; e=empty((s*.5*u,-.1*u,-2.3*u),H['arm'][s])
    obox((0,0,-.3*u),(.32*u,.22*u,.34*u),M('#C9A06A',.8,kind='fabric'),.03*u,e); obox((0,-.225*u,-.28*u),(.2*u,.005,.12*u),M('#E2482A',.5),.01*u,e)
    for k in (-1,1): obox((k*.18*u,0,.08*u),(.02*u,.02*u,.12*u),M('#8A6A3A',.6),.005,e)
    return e
def money(H,s=1,amt='100'):
    u=H['u']; e=empty((s*.5*u,-.35*u,-2.1*u),H['arm'][s]); col='#C9A0D8' if amt=='100' else '#E8956A'
    obox((0,0,0),(.32*u,.008,.15*u),M(col,.6),.005*u,e); stext(amt,(0,-.012*u,0),.09*u,'#3A2A4A',parent=e); return e
def selfie(H,s=1,k=1.0):
    u=H['u']; arm_to(H,s,root_mat(H)@Vector((s*.45*u,-1.35*u,3.75*u)),k,base=(0,0,0))
# ================================================================ CAFE
def cafe_set():
    cafe_z(); _S,_A,_w,_bg=setup_interior('day',room=(0,0,4.2),res=PCT,samples=SAMPLES,shadow_dist=22); _A.data.energy*=.45
    S={}; table_round(*TABLE,r_=.72); B.done('t')
    SEATS=dict(z=(0,.98,0),f1=(-1.02,.05,90),f2=(1.02,.05,-90))
    S['ch']=[chair_cafe(TABLE[0]+x,TABLE[1]+y,rz) for x,y,rz in SEATS.values()]
    S['z']=mk(ZOYA_OUT,TABLE[0],TABLE[1]+.98,0,'zoya')
    S['f1']=mk(FRIEND1,TABLE[0]-1.02,TABLE[1]+.05,90,'f1'); S['f2']=mk(FRIEND2,TABLE[0]+1.02,TABLE[1]+.05,-90,'f2')
    S['cup']=coffee_cup(S['z'],-1); S['ph']=phone_in_hand(S['z'],1,'#E8A0C8')
    for k,H in (('f1',S['f1']),('f2',S['f2'])): S[k+'cup']=None
    B.cyl((TABLE[0]+.35,TABLE[1]+.2,1.13),.12,.2,M('#F4F1EA',.4),seg=14); B.cyl((TABLE[0]-.3,TABLE[1]+.35,1.1),.1,.16,M('#E8C547',.4),seg=14); B.done('cups')
    return S
def sitp(H,t,h=.62): seat(H,t,h);
def CAFE_HOOK():
    S=cafe_set(); z=S['z']
    for H in (S['f1'],S['f2']): H['root'].location[2]=-30
    def upd(t):
        sitp(z,t); selfie(z,1); face(z,mouth='smirk',brow=.03); z['arm'][-1].rotation_euler=(R(-60),0,R(-10)); look_at(z,S['ph'].matrix_world.translation,.6)
        q=ease(t/DUR); camset(LV((-1.9,-2.3,2.25),(-1.5,-1.8,2.15),q),(0,1.1,1.65),24,4)
    return dict(upd=upd)
SHOTS['CAFE_HOOK']=CAFE_HOOK
def ZOYA_INTRO():
    S=cafe_set(); z=S['z']
    for H in (S['f1'],S['f2']): H['root'].location[2]=-30
    T=dict(SEQ).get('ZOYA_INTRO',0)
    bubble('ZOYA  •  200K FOLLOWERS',(TABLE[0],TABLE[1]+.98,3.05),.3,size=.11,col='#FFFFFF',bg='#D9367A')
    def upd(t):
        sitp(z,t); face(z,mouth='smile',brow=.02); z['arm'][-1].rotation_euler=(R(-70),0,R(-8)); z['arm'][1].rotation_euler=(R(-20),0,R(8))
        c0,tg,ln=closecam(z,0,.25,3.4,dz=.25,lens=30,tz=-.6); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['ZOYA_INTRO']=ZOYA_INTRO
def VLOG():
    S=cafe_set(); z=S['z']
    for H in (S['f1'],S['f2']): H['root'].location[2]=-30
    def upd(t):
        sitp(z,t); selfie(z,1); talk(z,t,*wt(29,38),rest='smile'); face(z,brow=.04); z['arm'][-1].rotation_euler=(R(-40),R(10),R(-30)); look_at(z,S['ph'].matrix_world.translation,.7)
        h=hp(z); camset((h[0]-1.3,h[1]-2.2,h[2]-.1),(h[0]+.25,h[1],h[2]-.45),26,2.8)
    return dict(upd=upd)
SHOTS['VLOG']=VLOG
def CAFE_FRIENDS():
    S=cafe_set(); z=S['z']; wa=mk(WALEED,2.6,-1.8,-40,'wa'); bag=food_bag(wa,-1)
    def upd(t):
        for H in (z,S['f1'],S['f2']): sitp(H,t)
        face(z,mouth='flat',brow=.06,eyes=1.2); face(S['f1'],mouth='smile'); face(S['f2'],mouth='grin')
        wa['root'].location=(2.1,-1.0,0); wa['root'].rotation_euler=(0,0,R(-40)); stand(wa,t); blink(wa,t)
        k=math.sin(t*5); wa['arm'][1].rotation_euler=(R(-80),0,R(20+15*k)); wa['arm'][-1].rotation_euler=(R(-75),0,R(-25-15*k)); face(wa,mouth='smirk',brow=.04)
        q=ease(t/DUR); camset(LV((-.4,-3.6,2.3),(-.2,-3.2,2.2),q),(.5,.4,1.5),22,4)
    return dict(upd=upd)
SHOTS['CAFE_FRIENDS']=CAFE_FRIENDS
# ================================================================ STREET / GATE
def street_set(night=True,zoya=None,ammi=False,wa_c=WALEED,bike=True):
    leaves=house_z(night); setup_world('night' if night else 'day',shadow=40)
    S={'leaves':leaves}
    if bike: S['bike']=bike_obj(2.6,GY_-2.6,180)
    S['wa']=mk(wa_c,.4,GY_-1.2,0,'wa')
    if zoya: S['z']=mk(zoya,0,GY_+.55,0,'zoya')
    if ammi: S['am']=mk(AMMI,-.9,GY_+1.6,0,'ammi')
    return S
def gate_open(S,k):
    for h,s in zip(S['leaves'],(-1,1)): h.rotation_euler[2]=R(s*100*k)
def RIDE():
    S=street_set(True,bike=True); wa=S['wa']; mb=S['bike']; wa['root'].location[2]=-30
    rid=mk(WALEED_RIDE,0,0,0,'rider'); rid['root'].parent=mb['root']; rid['root'].location=(-.05,0,.35); rid['root'].rotation_euler=(0,0,R(90)); rid['root'].scale=(1/1.4,)*3
    def upd(t):
        x=L(-9,2.6,ease_out(tl(t,0,DUR*.85))); mb['root'].location=(x,GY_-2.6,0); mb['root'].rotation_euler=(0,0,R(180))
        for w_ in mb['wheels']: w_.rotation_euler[1]=-x*2.2
        sit(rid,1,.85,legs=80)
        for s in (1,-1): rid['arm'][s].rotation_euler=(R(-75),0,R(s*8))
        blink(rid,t)
        camset((x-3.5,GY_-6.2,1.6),(x+.5,GY_-2.4,1.3),26,4)
    return dict(upd=upd)
SHOTS['RIDE']=RIDE
def GATE_REVEAL():
    S=street_set(True,zoya=ZOYA_HOME); wa=S['wa']; z=S['z']; bag=food_bag(wa,-1)
    def upd(t):
        k=ease(tl(t,.2,1.2)); gate_open(S,k)
        z['root'].location=(0,GY_+.5-.5*k,0); stand(z,t); blink(z,t); face(z,mouth='flat',brow=0)
        wa['root'].location=(.9,GY_-1.3,0); wa['root'].rotation_euler=(0,0,R(200)); stand(wa,t); blink(wa,t)
        q=ease(t/DUR); camset(LV((-2.4,GY_-4.4,1.7),(-2.1,GY_-3.9,1.65),q),(.3,GY_-.3,1.4),24,4)
    return dict(upd=upd)
SHOTS['GATE_REVEAL']=GATE_REVEAL
def AMMI_IN():
    S=street_set(True,zoya=ZOYA_HOME,ammi=True); gate_open(S,1); z=S['z']; am=S['am']
    def upd(t):
        z['root'].location=(0,GY_,0); stand(z,t); blink(z,t); face(z,mouth='O',eyes=1.2,brow=.06)
        am['root'].location=(-.6,GY_+2.3,0); am['root'].rotation_euler=(0,0,R(-15)); stand(am,t); blink(am,t); talk(am,t,*wt(54,59),rest='flat'); face(am,brow=-.04,brow_r=-12)
        am['arm'][1].rotation_euler=(R(-100+12*math.sin(t*6)),0,R(15))
        S['wa']['root'].location=(1.3,GY_-1.4,0); camset((-1.7,GY_-3.0,2.3),(-.6,GY_+2.2,1.9),30,4)
    return dict(upd=upd)
SHOTS['AMMI_IN']=AMMI_IN
def STARE():
    S=street_set(True,zoya=ZOYA_HOME); gate_open(S,1); z=S['z']; wa=S['wa']; bag=food_bag(wa,-1)
    def upd(t):
        z['root'].location=(0,GY_,0); stand(z,t); face(z,mouth='flat',eyes=1.25,brow=.05)
        wa['root'].location=(.8,GY_-1.35,0); wa['root'].rotation_euler=(0,0,R(212)); stand(wa,t); face(wa,mouth='flat',eyes=1.25,brow=.05)
        camset((-2.8,GY_-3.2,1.95),(.4,GY_-.6,1.65),24,4)
    return dict(upd=upd)
SHOTS['STARE']=STARE
def BRIBE1():
    S=street_set(True,zoya=ZOYA_HOME); gate_open(S,1); z=S['z']; wa=S['wa']; bag=food_bag(wa,-1); m=money(z,1,'100')
    def upd(t):
        z['root'].location=(0,GY_,0); stand(z,t); blink(z,t); talk(z,t,*wt(67,73),rest='flat'); face(z,brow=-.04,brow_r=-10)
        k=ease(tl(t,ws(71)-.3,ws(71)+.2)); arm_to(z,1,Vector((.45,GY_-.8,1.55)),k)
        wa['root'].location=(.8,GY_-1.35,0); wa['root'].rotation_euler=(0,0,R(212)); stand(wa,t); blink(wa,t); face(wa,mouth='smirk')
        camset((-2.4,GY_-3.4,2.0),(.15,GY_-.5,1.6),26,2.8)
    return dict(upd=upd)
SHOTS['BRIBE1']=BRIBE1
def LIVE():
    S=street_set(False,zoya=ZOYA_OUT,bike=True); gate_open(S,0); z=S['z']; wa=S['wa']; mb=S['bike']; wa['root'].location[2]=-30
    rid=mk(WALEED_RIDE,0,0,0,'rider'); rid['root'].parent=mb['root']; rid['root'].location=(-.05,0,.35); rid['root'].rotation_euler=(0,0,R(90)); rid['root'].scale=(1/1.4,)*3
    S['ph']=phone_in_hand(z,1,'#FF4F7A')
    def upd(t):
        z['root'].location=(-.3,GY_-.9,0); z['root'].rotation_euler=(0,0,R(10)); stand(z,t); blink(z,t); selfie(z,1); face(z,mouth='grin',brow=.03)
        mb['root'].location=(30,GY_-2.7,0)
        h=hp(z); camset((h[0]-1.5,h[1]-2.4,h[2]-.2),(h[0]+.3,h[1],h[2]-.5),26,2.8)
    return dict(upd=upd)
SHOTS['LIVE']=LIVE
def BRIBE2():
    S=street_set(False,zoya=ZOYA_OUT,bike=True); z=S['z']; wa=S['wa']; m=money(z,1,'500')
    def upd(t):
        z['root'].location=(-.3,GY_-.9,0); z['root'].rotation_euler=(0,0,R(28)); stand(z,t); blink(z,t); talk(z,t,*wt(90,92),rest='flat'); face(z,brow=-.05,brow_r=-14)
        k=ease(tl(t,ws(90)-.2,ws(90)+.3)); arm_to(z,1,Vector((.3,GY_-1.85,1.6)),k)
        wa['root'].location=(.5,GY_-2.4,0); wa['root'].rotation_euler=(0,0,R(30)); stand(wa,t); blink(wa,t); face(wa,mouth='grin')
        camset((-1.3,GY_-4.9,1.85),(.2,GY_-1.5,1.6),26,4)
    return dict(upd=upd)
SHOTS['BRIBE2']=BRIBE2
def CONFRONT():
    S=street_set(False,zoya=ZOYA_HOME,bike=True); gate_open(S,1); z=S['z']; wa=S['wa']; z['root'].location=(0,GY_-.3,0)
    def upd(t):
        z['root'].location=(.2,GY_-.4,0); z['root'].rotation_euler=(0,0,R(-20)); stand(z,t); blink(z,t); talk(z,t,*wt(151,161),rest='smirk'); face(z,brow=.03)
        kp=tl(t,ws(158)-.2,ws(158)+.2)*(1-tl(t,we(161)+.3,we(161)+.6)); z['arm'][1].rotation_euler=(R(-80*kp),0,R(40*kp))
        wa['root'].location=(1.5,GY_-1.9,0); wa['root'].rotation_euler=(0,0,R(150)); stand(wa,t); blink(wa,t); face(wa,mouth='flat',brow=.06,eyes=1.15)
        camset((-1.5,GY_-3.9,1.8),(.85,GY_-1.1,1.6),24,4)
    return dict(upd=upd)
SHOTS['CONFRONT']=CONFRONT
def AMMI_GATE():
    S=street_set(False,zoya=ZOYA_HOME,ammi=True,bike=True); gate_open(S,1); z=S['z']; wa=S['wa']; am=S['am']
    def upd(t):
        z['root'].location=(.4,GY_-.4,0); z['root'].rotation_euler=(0,0,R(-30)); stand(z,t); face(z,mouth='O',eyes=1.2)
        am['root'].location=(-.85,GY_-.1,0); am['root'].rotation_euler=(0,0,R(-25)); stand(am,t); blink(am,t); talk(am,t,*wt(190,203),rest='grin'); face(am,brow=.06,eyes=1.15)
        k_=tl(t,ws(193)-.2,ws(193)+.2); am['arm'][1].rotation_euler=(R(-95*k_),0,R(20*k_)); am['root'].location[1]=GY_-.1-.3*ease(tl(t,0,.8))
        wa['root'].location=(1.5,GY_-1.9,0); wa['root'].rotation_euler=(0,0,R(150)); stand(wa,t); face(wa,mouth='O',eyes=1.2,brow=.06)
        camset((-1.9,GY_-4.7,1.85),(.5,GY_-.95,1.6),22,4)
    return dict(upd=upd)
SHOTS['AMMI_GATE']=AMMI_GATE
# ================================================================ KITCHEN / DINING
def kit_set(night=True):
    kitchen_z(night); _S,_A,_w,_bg=setup_interior('night' if night else 'day',room=(0,0,3.6),res=PCT,samples=SAMPLES,shadow_dist=16); _A.data.energy*=.5; return {}
def HOOK_SINK():
    kit_set(); z=mk(ZOYA_HOME,SINK[0],SINK[1],180,'zoya'); d=empty((0,0,0));
    def upd(t):
        z['root'].location=(SINK[0],SINK[1],0); z['root'].rotation_euler=(0,0,R(180)); stand(z,t); blink(z,t); face(z,mouth='flat',brow=-.02)
        k=math.sin(t*6)
        for s in (1,-1): arm_to(z,s,Vector((SINK[0]+s*.25+.05*k*s,1.7,1.25+.03*k)),1)
        q=ease(t/DUR); camset(LV((1.7,-1.6,2.7),(1.5,-1.3,2.6),q),(-1.0,1.5,1.4),20,4)
    return dict(upd=upd)
SHOTS['HOOK_SINK']=HOOK_SINK
def DINNER():
    kit_set(); z=mk(ZOYA_HOME,3.55,-.5,180,'zoya'); wa=mk(WALEED,4.85,-.5,180,'wa'); am=mk(AMMI,4.2,1.75,0,'am')
    point((4.2,-1.4,2.6),160,(1,.93,.84),r=.9); point((4.6,2.0,2.9),70,(1,.9,.8),r=.6)
    def upd(t):
        for H in (z,wa,am): seat(H,t,.62)
        e1=math.sin(t*7.5); e2=math.sin(t*6+1.3)
        arm_to(wa,1,Vector((4.75,.15+.08*e1,1.1+.28*max(0,e1))),1); arm_to(wa,-1,Vector((4.95,.1,1.05)),1)
        face(wa,mouth='grin' if e1>0 else 'O',brow=.04); look_at(wa,(4.7,.2,1.0),.4)
        arm_to(am,1,Vector((4.35,1.2+.05*e2,1.08+.15*max(0,e2))),1); face(am,mouth='smile',brow=.03); look_at(am,hp(wa),.6)
        face(z,mouth='flat',brow=-.05,brow_r=-12); look_at(z,hp(wa),.7); arm_to(z,-1,Vector((3.65,.15,1.04)),1)
        q=ease(t/DUR); camset(LV((4.4,2.26,3.0),(4.35,2.2,2.75),q),LV((4.2,-.45,1.35),(4.2,-.45,1.45),q),L(22,26,q),4)
    return dict(upd=upd)
SHOTS['DINNER']=DINNER
def SINK_BOTH():
    kit_set(); z=mk(ZOYA_HOME,SINK[0]-.62,SINK[1],180,'zoya'); wa=mk(WALEED,SINK[0]+.62,SINK[1],180,'wa')
    def upd(t):
        for H,dx in ((z,-.62),(wa,.62)):
            H['root'].location=(SINK[0]+dx,SINK[1],0); H['root'].rotation_euler=(0,0,R(180)); stand(H,t); blink(H,t)
            k=math.sin(t*6+dx)
            for s in (1,-1): arm_to(H,s,Vector((SINK[0]+dx*.4+s*.18,1.72,1.25+.03*k)),1)
        look_at(z,hp(wa),.5); look_at(wa,hp(z),.5); face(z,mouth='flat',brow=-.03); face(wa,mouth='flat',brow=-.03)
        q=ease(t/DUR); camset(LV((1.9,-1.4,2.7),(1.7,-1.1,2.6),q),(-.9,1.4,1.5),20,4)
    return dict(upd=upd)
SHOTS['SINK_BOTH']=SINK_BOTH

# ================================================================ added shots
def street_day(zoya=ZOYA_HOME,ammi=False):
    S=street_set(False,zoya=zoya,ammi=ammi,bike=True); gate_open(S,1); return S
def LIVE2():
    S=street_set(False,zoya=ZOYA_OUT,bike=True); z=S['z']; wa=S['wa']; mb=S['bike']; wa['root'].location[2]=-30; S['ph']=phone_in_hand(z,1,'#FF4F7A')
    rid=mk(WALEED_RIDE,0,0,0,'rider'); rid['root'].parent=mb['root']; rid['root'].location=(-.05,0,.35); rid['root'].rotation_euler=(0,0,R(90)); rid['root'].scale=(1/1.4,)*3
    def upd(t):
        z['root'].location=(-.3,GY_-.9,0); z['root'].rotation_euler=(0,0,R(10)); stand(z,t); blink(z,t); selfie(z,1)
        k=tl(t,we(89),we(89)+.3); face(z,mouth='O' if k>.5 else 'grin',eyes=1+.25*k,brow=.03+.04*k)
        if k>0: z['root'].rotation_euler[2]=R(10+40*k)
        x=L(4.5,1.4,ease_out(tl(t,0,1.0))); mb['root'].location=(x,GY_-2.7,0); sit(rid,1,.85,legs=80)
        for s_ in (1,-1): rid['arm'][s_].rotation_euler=(R(-75),0,R(s_*8))
        talk(rid,t,*wt(85,89),rest='smirk'); rid['props']['helmet'].scale=(0,0,0)
        for o in rid.get('hair_objs',[]): o.scale=(1,1,1)
        look_at(rid,hp(z),.7)
        camset((-2.2,GY_-4.6,1.95),(.6,GY_-1.6,1.7),24,4)
    return dict(upd=upd)
SHOTS['LIVE2']=LIVE2
def PHONE_UNDER():
    S=cafe_set(); z=S['z']; wa=mk(WALEED,2.1,-1.0,-40,'wa'); bag=food_bag(wa,-1)
    def upd(t):
        for H in (z,S['f1'],S['f2']): sitp(H,t)
        k=ease(tl(t,.2,.9)); arm_to(z,1,Vector((TABLE[0]+.25,TABLE[1]+.55,L(1.3,.85,k))),1)
        face(z,mouth='flat',brow=-.04,brow_r=-10); look_at(z,S['ph'].matrix_world.translation,.8*k,maxpitch=45)
        face(S['f1'],mouth='smile'); face(S['f2'],mouth='smile'); look_at(S['f1'],hp(S['f2']),.6); look_at(S['f2'],hp(S['f1']),.6)
        wa['root'].location=(2.1,-1.0,0); wa['root'].rotation_euler=(0,0,R(-40)); stand(wa,t); blink(wa,t); face(wa,mouth='smirk'); look_at(wa,hp(z),.7)
        c0,tg,ln=closecam(z,0,-.35,3.5,dz=.15,lens=28,tz=-.85); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['PHONE_UNDER']=PHONE_UNDER
def WALEED_TYPE():
    S=street_set(False,bike=True); wa=S['wa']; ph=phone_in_hand(wa,1,'#E8F0FF')
    def upd(t):
        wa['root'].location=(2.0,GY_-2.2,0); wa['root'].rotation_euler=(0,0,R(15)); stand(wa,t); blink(wa,t)
        arm_to(wa,1,root_mat(wa)@Vector((.25*wa['u'],-1.25*wa['u'],3.6*wa['u'])),1); arm_to(wa,-1,root_mat(wa)@Vector((-.05*wa['u'],-1.3*wa['u'],3.5*wa['u'])),1)
        look_at(wa,ph.matrix_world.translation,.8,maxpitch=45); face(wa,mouth='grin' if t>DUR*.5 else 'smirk',brow=.05)
        c0,tg,ln=closecam(wa,15,.6,3.0,lens=30,tz=-.6); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['WALEED_TYPE']=WALEED_TYPE
def ZOYA_SMILE():
    S=street_day(); z=S['z']; wa=S['wa']; ph=phone_in_hand(z,1,'#FFF3B0'); wa['root'].location[2]=-30
    def upd(t):
        z['root'].location=(.2,GY_-.4,0); z['root'].rotation_euler=(0,0,R(0)); stand(z,t); blink(z,t)
        arm_to(z,1,root_mat(z)@Vector((.25*z['u'],-1.25*z['u'],3.6*z['u'])),1); look_at(z,ph.matrix_world.translation,.7*(1-tl(t,DUR*.55,DUR*.8)),maxpitch=40)
        face(z,mouth='smirk' if t>DUR*.45 else 'flat',brow=.03 if t>DUR*.45 else -.02)
        c0,tg,ln=closecam(z,0,.3,2.8,lens=32,tz=-.5); camset(drift(c0,tg,t,.1),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['ZOYA_SMILE']=ZOYA_SMILE
def DEAL():
    S=street_day(); z=S['z']; wa=S['wa']; ph=phone_in_hand(z,1,'#9FD3C7')
    def upd(t):
        z['root'].location=(.2,GY_-.4,0); z['root'].rotation_euler=(0,0,R(-20)); stand(z,t); blink(z,t); talk(z,t,*wt(168,176),rest='smirk'); face(z,brow=.04)
        k=tl(t,ws(172)-.2,ws(172)+.2); arm_to(z,1,root_mat(z)@Vector((.4*z['u'],-1.5*z['u'],L(3.4,4.9,k)*z['u'])),1)
        wa['root'].location=(1.5,GY_-1.9,0); wa['root'].rotation_euler=(0,0,R(150)); stand(wa,t); blink(wa,t); face(wa,mouth='O' if k>.5 else 'flat',brow=.06,eyes=1.1+.15*k)
        camset((-1.8,GY_-3.7,1.8),(.6,GY_-1.0,1.7),26,4)
    return dict(upd=upd)
SHOTS['DEAL']=DEAL
def DEFEAT():
    S=street_day(ammi=True); z=S['z']; wa=S['wa']; am=S['am']
    def upd(t):
        z['root'].location=(.2,GY_-.4,0); z['root'].rotation_euler=(0,0,R(-20)); stand(z,t); blink(z,t); face(z,mouth='smirk',brow=.03)
        wa['root'].location=(1.5,GY_-1.9,0); wa['root'].rotation_euler=(0,0,R(150)); stand(wa,t); blink(wa,t)
        k=ease(tl(t,.2,1.0)); wa['head'].rotation_euler[0]=R(14*k); wa['root'].rotation_euler[0]=R(5*k); face(wa,mouth='flat',brow=-.05,brow_r=-14,eyes=.8)
        for s_ in (1,-1): wa['arm'][s_].rotation_euler=(R(4),0,R(s_*3))
        ka=ease(tl(t,ws(182),ws(189))); am['root'].location=(-.6,L(GY_+2.4,GY_+.5,ka),0); am['root'].rotation_euler=(0,0,R(-10))
        if 0<ka<1: walk(am,ka*1.9+am['seed'],step=.5,arm=18)
        else: stand(am,t)
        blink(am,t); face(am,mouth='flat',brow=.02)
        camset((-1.8,GY_-4.6,1.9),(.75,GY_-.9,1.6),22,4)
    return dict(upd=upd)
SHOTS['DEFEAT']=DEFEAT
def INVITE():
    S=street_day(ammi=True); z=S['z']; wa=S['wa']; am=S['am']
    def upd(t):
        z['root'].location=(.6,GY_-.2,0); z['root'].rotation_euler=(0,0,R(-30)); stand(z,t); blink(z,t); face(z,mouth='flat',brow=-.04,brow_r=-10)
        am['root'].location=(-.4,GY_-.45,0); am['root'].rotation_euler=(0,0,R(-35)); stand(am,t); blink(am,t); talk(am,t,*wt(216,223),rest='grin'); face(am,brow=.05)
        k=tl(t,ws(218)-.2,ws(218)+.3); am['arm'][1].rotation_euler=(R(-70*k),0,R(-40*k))
        wa['root'].location=(1.5,GY_-1.9,0); wa['root'].rotation_euler=(0,0,R(150)); stand(wa,t); blink(wa,t); face(wa,mouth='smile',brow=.03)
        c0,tg,ln=closecam(am,-35,-.4,3.0,lens=30,tz=-.5); camset(drift(c0,tg,t),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['INVITE']=INVITE
def ORDER():
    kit_set(); z=mk(ZOYA_HOME,3.55,-.5,180,'zoya'); wa=mk(WALEED,4.85,-.5,180,'wa'); am=mk(AMMI,4.2,1.75,0,'am')
    point((4.2,-.9,2.3),140,(1,.93,.84),r=.9)
    def upd(t):
        for H in (z,wa,am): seat(H,t,.62)
        talk(am,t,*wt(233,241),rest='flat'); face(am,brow=-.02)
        k=tl(t,ws(235),ws(235)+.3); look_at(am,hp(z) if k<.5 else hp(wa),.85)
        if k<.5: arm_to(am,1,Vector((3.7,.9,1.5)),ease(tl(t,ws(233)-.2,ws(233)+.2)))
        else: arm_to(am,-1,Vector((4.75,.9,1.5)),k)
        face(z,mouth='flat',brow=-.05,brow_r=-12,eyes=.9); face(wa,mouth='O' if k>.5 else 'smile',eyes=1+.25*k,brow=.05*k); look_at(z,hp(am),.6); look_at(wa,hp(am),.6)
        q=ease(t/DUR); camset(LV((4.2,-2.7,3.05),(4.2,-2.3,2.95),q),(4.2,1.75,1.75),L(30,34,q),4)
    return dict(upd=upd)
SHOTS['ORDER']=ORDER
def SINK_TALK():
    kit_set(); z=mk(ZOYA_HOME,SINK[0]-.62,SINK[1],180,'zoya'); wa=mk(WALEED,SINK[0]+.62,SINK[1],180,'wa')
    point((-1.0,-1.0,2.4),120,(1,.94,.86),r=.8)
    def upd(t):
        kz=ease(tl(t,ws(242)-.45,ws(242)-.05)); kw=ease(tl(t,ws(246)-.45,ws(246)-.05))
        for H,dx,kk,tr in ((z,-.62,kz,40),(wa,.62,kw,-40)):
            H['root'].location=(SINK[0]+dx,SINK[1]-.12*kk,0); H['root'].rotation_euler=(0,0,R(L(180,tr,kk))); stand(H,t); blink(H,t)
            w_=math.sin(t*6+dx)
            if kk<.6:
                for s_ in (1,-1): arm_to(H,s_,Vector((SINK[0]+dx*.4+s_*.18,1.72,1.25+.03*w_)),1-kk/.6)
            else:
                for s_ in (1,-1): H['arm'][s_].rotation_euler=(R(-15),0,R(s_*6))
        talk(z,t,*wt(242,245),rest='flat'); talk(wa,t,*wt(246,247),rest='flat')
        face(z,brow=-.05,brow_r=-12); face(wa,brow=-.05,brow_r=-12,eyes=.95)
        look_at(z,hp(wa),.8*kz); look_at(wa,hp(z),.8*kw)
        q=ease(t/DUR); camset(LV((-1.0,-2.7,2.5),(-1.0,-2.3,2.4),q),(-1.0,1.0,1.75),26,2.8)
    return dict(upd=upd)
SHOTS['SINK_TALK']=SINK_TALK
def MORAL():
    kit_set(); z=mk(ZOYA_HOME,SINK[0]-.62,SINK[1],180,'zoya'); wa=mk(WALEED,SINK[0]+.62,SINK[1],180,'wa'); am=mk(AMMI,3.4,-.6,-60,'am')
    def upd(t):
        for H,dx in ((z,-.62),(wa,.62)):
            H['root'].location=(SINK[0]+dx,SINK[1],0); H['root'].rotation_euler=(0,0,R(180)); stand(H,t); blink(H,t)
            k=math.sin(t*6+dx)
            for s_ in (1,-1): arm_to(H,s_,Vector((SINK[0]+dx*.4+s_*.18,1.72,1.25+.03*k)),1)
        stand(am,t); blink(am,t); face(am,mouth='smile'); look_at(am,hp(z),.6)
        q=ease(t/DUR); camset(LV((1.2,-1.0,2.5),(3.0,-3.4,3.0),q),LV((-.9,1.3,1.5),(.2,.8,1.4),q),L(22,20,q),5.6)
    return dict(upd=upd)
SHOTS['MORAL']=MORAL
def CTA():
    kit_set(); z=mk(ZOYA_HOME,SINK[0]-.62,SINK[1],180,'zoya'); wa=mk(WALEED,SINK[0]+.62,SINK[1],180,'wa')
    def upd(t):
        for H,dx in ((z,-.62),(wa,.62)):
            H['root'].location=(SINK[0]+dx,SINK[1],0); stand(H,t); blink(H,t)
        k=ease(tl(t,.1,.7)); z['root'].rotation_euler=(0,0,R(L(180,30,k))); wa['root'].rotation_euler=(0,0,R(L(180,-30,ease(tl(t,.4,1.0)))))
        for H in (z,wa):
            for s_ in (1,-1): H['arm'][s_].rotation_euler=(R(-10),0,R(s_*6))
        face(z,mouth='smirk',brow=.04); face(wa,mouth='grin',brow=.04)
        camset((-.7,-1.7,1.9),(-.75,1.0,1.75),24,2.8)
    return dict(upd=upd)
SHOTS['CTA']=CTA
def STREET_EST():
    S=street_set(False,bike=False); wa=S['wa']; wa['root'].location[2]=-30
    def upd(t):
        q=ease(t/DUR); camset(LV((-6,GY_-8,4.5),(-4.5,GY_-7,3.2),q),(0,GY_+1,2.0),22,8)
    return dict(upd=upd)
SHOTS['STREET_EST']=STREET_EST
UI_SHOTS={'UI_LIVE_END','UI_RATING','UI_COMMENT','UI_PROFILE','UI_RISHTA'}
for _k in UI_SHOTS: SHOTS[_k]=None
SEQ=[('CAFE_HOOK', 0.0), ('HOOK_SINK', 2.933), ('ZOYA_INTRO', 5.5), ('VLOG', 11.233), ('RIDE', 14.667), ('GATE_REVEAL', 17.233), ('AMMI_IN', 20.167), ('STARE', 23.433), ('BRIBE1', 25.133), ('LIVE', 28.067), ('LIVE2', 32.0), ('UI_LIVE_END', 33.5), ('BRIBE2', 34.367), ('CAFE_FRIENDS', 35.367), ('PHONE_UNDER', 40.033), ('UI_RATING', 42.7), ('WALEED_TYPE', 45.3), ('UI_COMMENT', 49.033), ('UI_PROFILE', 53.067), ('ZOYA_SMILE', 55.1), ('CONFRONT', 56.367), ('DEAL', 62.267), ('DEFEAT', 68.433), ('AMMI_GATE', 72.833), ('UI_RISHTA', 77.367), ('INVITE', 81.7), ('DINNER', 84.567), ('ORDER', 88.267), ('SINK_TALK', 91.733), ('MORAL', 94.3), ('CTA', 99.9)]
END=103.0667
