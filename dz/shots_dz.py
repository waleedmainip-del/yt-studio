# Shots for "Darzi Ka Kal". SEQ/END are filled by gen_seq.py.
SHOTS={}
END=79.4
SEQ=[('HOOK', 0.0), ('KAL0', 2.6), ('GIVE', 3.867), ('M1', 9.567), ('KAL2', 11.567), ('KAL3', 15.2), ('WAQFA', 19.033), ('CURTAIN', 23.133), ('JOOTE', 29.933), ('BEHIND', 32.6), ('CHAAND', 35.233), ('CROWD', 41.067), ('SEW', 43.567), ('DARK', 47.167), ('TORCH', 49.433), ('PACKET', 52.933), ('OPEN', 56.8), ('EID', 60.233), ('REVEAL', 66.667), ('MR1', 69.133), ('MR2', 72.433), ('CTA', 75.767)]
import os as _os
FILLE=[40.0]; _FL=[]
_camset0=camset
def camset(loc,tg,lens,*a,**k):
    _camset0(loc,tg,lens,*a,**k)
    if not _FL: _FL.append(point((0,0,0),FILLE[0],(1,.93,.85),r=.4,shadow=False))
    v=Vector(tg)-Vector(loc); _FL[0].location=Vector(loc)+v.normalized()*min(1.0,v.length*.3)+Vector((0,0,.35)); _FL[0].data.energy=FILLE[0]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0
def we(i): return W_[i]['e']-T0
def mk(C,x,y,rz,name,z=0.0): return avatar_bg((x,y,z),rz,C,name=name)
def fwd(rz): return (math.sin(R(rz)),-math.cos(R(rz)))
def drift(c0,tg,t,a=.06): q=ease(t/DUR); return LV(c0,(L(c0[0],tg[0],a),L(c0[1],tg[1],a),c0[2]),q)
def closecam(H,rz,side=.3,dist=3.0,dz=.05,tz=-.3,lens=36):
    h=hp(H); f=fwd(rz); rt=(-f[1],f[0])
    return (h[0]+f[0]*dist+rt[0]*side,h[1]+f[1]*dist+rt[1]*side,h[2]+dz),(h[0],h[1],h[2]+tz),lens
def cal(txt):
    e=empty((0,COUNTER_Y-.33,.62)); obox((0,0,0),(.62,.02,.22),M('#F4F1EA',.5),.01,e); obox((0,-.01,.17),(.62,.015,.05),M('#C8372D',.5),0,e)
    stext(txt,(0,COUNTER_Y-.37,.57),.17,'#16171C'); return e
def shop_day(c='EID: 21 DIN'): bazaar(False); setup_world('day',shadow=40); cal(c)
def shop_night(c='CHAAND RAAT'): bazaar(True); setup_world('night',shadow=40); cal(c)
MS=(0,COUNTER_Y+.55)   # Master behind the counter
def master_at_counter(C=None): return mk(C or MASTER,MS[0],MS[1],0,'master')
def tape_on(m):
    u=m['u']; e=empty((0,0,0),m['root']);
    for s in (1,-1): obox((s*.42*u,-.55*u,3.1*u),(.06*u,.02*u,.75*u),M('#E8C547',.5),0,e)
    return e
def bundle(parent,col='#1E3FA0',sz=1.0):
    e=empty((0,0,0),parent); obox((0,0,0),(.24*sz,.17*sz,.07*sz),M(col,.85,kind='fabric'),.03,e); obox((0,0,.072*sz),(.25*sz,.02,.002),M('#E8C547',.4),0,e); return e
# ---------------------------------------------------------------- crowd helpers
def crowd(n,x0,x1,y0,y1,rz=0,seed=1,dresses=None,skip=None):
    r=random.Random(seed); P=[]; cols=n if abs(y1-y0)<.01 else max(1,int(round(n/2)))
    for i in range(n):
        x=L(x0,x1,(i%cols+.5)/cols)+r.uniform(-.1,.1); y=L(y0,y1,(i//cols)/max(1,(n-1)//cols))+r.uniform(-.1,.1)
        if skip and skip(x,y): continue
        H=mk((dresses or CROWD)[(i+seed)%len(dresses or CROWD)],x,y,rz+r.uniform(-12,12),'c%d_%d'%(seed,i)); H['ph']=r.uniform(0,6); P.append(H)
    return P
def chant(P,t,on=True,k=1.0):
    for H in P:
        stand(H,t); blink(H,t); ph=H['ph']; b=math.sin(t*5.2+ph)
        if on: H['arm'][1].rotation_euler=(R(-150-25*b*k),0,R(10)); H['arm'][-1].rotation_euler=(R(-20),0,R(-6)); face(H,mouth='O' if b>0 else 'flat',brow=-.05)
        else: face(H,mouth='flat')
# ================================================================ HOOK: bazaar day, Eid rush
def HOOK():
    shop_day(); m=master_at_counter(); tape_on(m)
    P=[]
    for i,(y,d) in enumerate(((-1.2,1),(-2.6,-1),(-4.0,1))):
        for k in range(4):
            H=mk(CROWD[(i*4+k)%len(CROWD)],0,y,90*d,'w%d%d'%(i,k)); P.append(dict(H=H,x0=-16+k*8+i*2.5,y=y,d=d))
    def upd(t):
        stand(m,t); blink(m,t); face(m,mouth='smile',brow=.03); look_at(m,(0,-4,1.5),.5)
        for p in P:
            x=-16+((p['x0']+16)+p['d']*1.1*t)%32; p['H']['root'].location=(x,p['y'],0); p['H']['root'].rotation_euler=(0,0,R(90*p['d'])); walk(p['H'],1.1*t+p['x0'],step=.55); blink(p['H'],t)
        k=tl(t,ws(9)-.6,ws(9)); q=ease(t/DUR)
        camset(LV((-3.5,-7.2,2.6),(-1.6,-4.6,2.0),q),LV((0,2.6,2.4),(0,2.8,1.9),q),L(20,26,q),5)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
def KAL0():
    shop_day(); m=master_at_counter(); tape_on(m)
    def upd(t):
        stand(m,t); blink(m,t); u=m['u']
        face(m,mouth='smile',brow=.05); m['head'].rotation_euler[1]=R(8*tl(t,.1,.4))
        if .3<t<.75: face(m,eyes=.1)
        pass
        c0,tg,ln=closecam(m,0,.15,2.6,dz=-.05,lens=34,tz=-.35); camset(drift(c0,tg,t,.08),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['KAL0']=KAL0
WC=(0.15,COUNTER_Y-.95)     # Waleed at the counter
def GIVE():
    shop_day(); m=master_at_counter(); tape_on(m); wa=mk(WALEED,-4,-1.5,0,'wa'); b=bundle(wa['arm'][1]); b.location=(.5*wa['u'],-.35*wa['u'],-2.15*wa['u'])
    pts=[(-4,-1.5),(-1.2,.5),WC]
    def upd(t):
        stand(m,t); blink(m,t); face(m,mouth='smile',brow=.03)
        q=walk_path(wa,pts,t,0,ws(20)); blink(wa,t)
        if q>=1: stand(wa,t); wa['root'].rotation_euler[2]=R(0)
        kg=tl(t,ws(23)-.4,ws(24)); u=wa['u']
        arm_to(wa,1,root_mat(wa)@Vector((.3*u,-1.4*u,L(2.6,3.3,kg)*u)),.4+.6*kg if q>=1 else 0)
        km=tl(t,ws(25),ws(27)); arm_to(m,1,Vector((.2,COUNTER_Y-.05,1.15)),km)
        if km>.5: b.parent=None; b.location=(.25,COUNTER_Y-.05,1.12); b.rotation_euler=(0,0,0)
        face(wa,mouth='grin' if t>ws(20) else 'smile',brow=.04); look_at(wa,hp(m),.6*tl(t,ws(19),ws(20)))
        look_at(m,hp(wa),.5)
        if t<ws(20)-.3: q2=ease(t/DUR); camset((-3.4,-4.6,1.9),(-1.6,.6,1.45),26,4)
        else: camset((2.5,2.8,1.75),(.05,2.8,1.45),22,4)
    return dict(upd=upd)
SHOTS['GIVE']=GIVE
def counter_talk(a,b,react_m=None,react_w=None,cam='m',calt='EID: 21 DIN',prop=None,Wd=WALEED):
    def S_():
        shop_day(calt); m=master_at_counter(); tape_on(m); wa=mk(Wd,WC[0],WC[1],0,'wa')
        pr=prop(m,wa) if prop else None
        def upd(t):
            stand(m,t); blink(m,t); stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(0); m['root'].rotation_euler[2]=R(0)
            talk(m,t,*wt(a,b),rest='smile'); face(m,brow=.04); look_at(m,hp(wa),.6); look_at(wa,hp(m),.6)
            if react_m: react_m(m,t,pr)
            if react_w: react_w(wa,t)
            hm=hp(m); hw=hp(wa); q=ease(t/DUR)
            if cam=='m': camset(LV((2.2,1.3,1.85),(2.05,1.5,1.82),q),(hm[0],hm[1],hm[2]-.3),30,2.8)
            else: camset(LV((1.35,3.5,1.8),(1.25,3.35,1.78),q),(hw[0],hw[1],hw[2]-.3),30,2.8)
        return dict(upd=upd)
    return S_
def _pat(m,t,pr):
    u=m['u']; k=math.sin(t*6)*.5+.5; arm_to(m,1,Vector((.25,COUNTER_Y-.05,1.12+.05*k)),tl(t,.2,.5)); arm_to(m,-1,root_mat(m)@Vector((-.6*u,-1.3*u,4.0*u)),tl(t,ws(31),ws(31)+.3))
def _bun(m,wa): b=bundle(None); b.location=(.25,COUNTER_Y-.05,1.12); return b
SHOTS['M1']=counter_talk(28,33,_pat,lambda w,t: face(w,mouth='grin',brow=.04),calt='EID: 21 DIN',prop=_bun)
def KAL2():
    shop_day('EID: 20 DIN'); m=mk(MASTER,.2,4.65,0,'master'); tape_on(m); wa=mk(WALEED,-3.5,-1.4,0,'wa')
    sc=empty((0,0,0),m['arm'][1]); sc.location=(.5*m['u'],-.35*m['u'],-2.1*m['u'])
    for s in (1,-1): obox((s*.03,0,-.12),(.015,.01,.14),M('#C9CED8',.25,metal=.9),0,sc,rot=(0,R(s*12),0))
    obox((0,0,.06),(.05,.012,.04),M('#C8372D',.4),.01,sc)
    def upd(t):
        stand(m,t); blink(m,t); m['root'].rotation_euler=(R(14),0,0); u=m['u']
        cut=math.sin(t*16)*.5+.5; arm_to(m,1,Vector((.3,4.25,.98+.03*cut)),1 if t<ws(37)-.2 else 1-tl(t,ws(37)-.2,ws(37)+.2)); arm_to(m,-1,Vector((-.1,4.25,.93)),1 if t<ws(37) else 0)
        if t>ws(37): m['root'].rotation_euler=(R(14*(1-tl(t,ws(37),ws(37)+.3))),0,0); look_at(m,hp(wa),.6)
        talk(m,t,*wt(37,42),rest='smile'); face(m,brow=.03)
        q=walk_path(wa,[(-3.5,-1.4),(-1.0,.6),WC],t,0,ws(37)-.2); blink(wa,t)
        if q>=1: stand(wa,t); wa['root'].rotation_euler[2]=R(0)
        face(wa,mouth='smile' if t<ws(39) else 'flat',brow=.04 if t<ws(39) else -.03); look_at(wa,hp(m),.5)
        if t<ws(37)-.3: camset((-3.2,-4.4,2.0),(-.6,1.8,1.4),24,4)
        else: camset((2.2,1.4,1.85),(.2,4.3,1.3),26,4)
    return dict(upd=upd)
SHOTS['KAL2']=KAL2
def _btn(m,wa):
    e=empty((0,0,0),m['arm'][-1]); e.location=(-.5*m['u'],-.4*m['u'],-2.1*m['u']); obox((0,0,0),(.12,.09,.035),M('#C9A24A',.3,metal=.6),.01,e)
    for k in range(6): B.cyl((0,0,0),.02,.01,M(['#F4F1EA','#16171C','#C8372D'][k%3],.3),seg=10) if False else ocyl(((k%3-1)*.06,(k//3-.5)*.06,.04),.022,.012,M(['#F4F1EA','#16171C','#C8372D'][k%3],.3),e,rot=(0,0,0))
    return e
def _btn_m(m,t,pr): arm_to(m,-1,root_mat(m)@Vector((-.2*m['u'],-1.5*m['u'],3.4*m['u'])),tl(t,.1,.4)); m['head'].rotation_euler[1]=R(-6*tl(t,ws(52)-.1,ws(52)+.2))
SHOTS['KAL3']=counter_talk(47,52,_btn_m,lambda w,t: face(w,mouth='flat',brow=-.06,brow_r=-10,eyes=.85),calt='ROZA 20',prop=_btn)
def WAQFA():
    shop_day('ROZA 25'); sh=shutter(1.25); wa=mk(WALEED,-1.7,1.55,0,'wa')
    sg=empty((.0,SHOP_Y0-.14,1.65)); obox((0,0,0),(.75,.02,.24),M('#F4F1EA',.5),.01,sg); stext('NAMAZ KA WAQFA',(0,SHOP_Y0-.17,1.7),.13,'#C8372D'); stext('5 MINUTE',(0,SHOP_Y0-.17,1.53),.1,'#16171C')
    for s in (1,-1): obox((s*.6,0,.4),(.005,.005,.25),M('#16171C',.5),0,sg)
    sun=bpy.data.objects.get('Sun') or [o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='SUN'][0]; r0=sun.rotation_euler.copy()
    def upd(t):
        k=tl(t,ws(55)-.2,DUR-.3); u=wa['u']
        stand(wa,t); wa['root'].location=(-1.7,1.3,.16); wa['root'].rotation_euler=(0,0,R(10)); blink(wa,t)
        for s in (1,-1): arm_to(wa,s,root_mat(wa)@Vector((-s*.3*u,-1.0*u,3.1*u)),1)
        if k<.5: face(wa,mouth='flat',brow=-.04,brow_r=-8); wa['head'].rotation_euler[0]=R(-6)
        else: face(wa,mouth='O',eyes=.05); wa['head'].rotation_euler=(R(14),R(16),0)
        sun.rotation_euler=(r0[0]+R(30)*k,r0[1],r0[2]+R(60)*k); sun.data.energy=3.0*(1-.6*k)
        q=ease(t/DUR); camset(LV((-2.2,-3.8,1.8),(-1.8,-3.2,1.7),q),(-.7,1.6,1.4),24,4)
    return dict(upd=upd)
SHOTS['WAQFA']=WAQFA
# --------------------------------------------------------------- curtain feet
def curtain_set(c='ROZA 29'):
    shop_day(c); m=mk(MASTER,CURT[0],CURT[1]+.32,0,'master'); return m
def master_hide(m,t,wig=0):
    stand(m,t); m['root'].location=(CURT[0]+.03*math.sin(t*9)*wig,CURT[1]+.32,0); m['root'].rotation_euler=(0,0,0)
    for s in (1,-1): m['arm'][s].rotation_euler=(R(-10),0,R(s*6))
def CURTAIN():
    m=curtain_set(); wa=mk(WALEED,-3.2,-1.6,0,'wa')
    def upd(t):
        master_hide(m,t); q=walk_path(wa,[(-3.2,-1.6),(-.2,1.2),(1.9,2.4),(2.12,3.55)],t,.1,ws(66)-.1); blink(wa,t)
        if q>=1: stand(wa,t); wa['root'].rotation_euler[2]=R(face_dir(CURT[0]-2.12,CURT[1]-3.55))
        look_at(wa,(CURT[0],CURT[1],.3),.7*tl(t,ws(73)-.2,ws(73)+.3),maxpitch=40); face(wa,mouth='flat',brow=-.04,eyes=1.05)
        if t<ws(66)-.4: camset((-2.4,-4.0,1.8),(.0,2.6,1.4),24,4)
        elif t<ws(73)-.1: camset((-.4,2.5,1.85),(1.75,5.0,1.1),24,4)
        else: q2=tl(t,ws(73)-.1,DUR); camset(LV((1.5,3.4,.48),(1.5,3.5,.42),q2),(CURT[0],CURT[1]+.3,.22),30,2.8)
    return dict(upd=upd)
SHOTS['CURTAIN']=CURTAIN
def JOOTE():
    m=curtain_set(); wa=mk(WALEED,2.12,3.55,0,'wa')
    def upd(t):
        master_hide(m,t); stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(face_dir(CURT[0]-2.12,CURT[1]-3.55))
        talk(wa,t,*wt(78,86),rest='flat'); face(wa,brow=-.03,brow_r=-8); arm_to(wa,1,Vector((CURT[0]-.2,CURT[1]-.1,.6)),tl(t,ws(83)-.2,ws(83)+.2)*(1-tl(t,DUR-.5,DUR)))
        c0,tg,ln=closecam(wa,face_dir(CURT[0]-2.12,CURT[1]-3.55),-.25,1.05,dz=-.05,lens=20,tz=-.35); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['JOOTE']=JOOTE
def BEHIND():
    m=curtain_set(); wa=mk(WALEED,2.12,3.55,0,'wa')
    def upd(t):
        master_hide(m,t,wig=1); talk(m,t,*wt(87,94),rest='flat'); stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(face_dir(CURT[0]-2.12,CURT[1]-3.55))
        for s in (1,-1): m['leg'][s].rotation_euler[0]=R(10*math.sin(t*7+s))
        face(wa,mouth='flat',brow=-.07,brow_r=-14,eyes=.8)
        if t<ws(91): camset((1.5,3.35,.45),(CURT[0],CURT[1]+.3,.25),30,2.8)
        else: c0,tg,ln=closecam(wa,face_dir(CURT[0]-2.12,CURT[1]-3.55),.25,1.05,dz=-.05,lens=20,tz=-.35); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['BEHIND']=BEHIND
# --------------------------------------------------------------- chaand raat
def outside_crowd(n=12):
    return crowd(n,-3.6,3.6,-.3,-3.0,rz=180,seed=3,skip=lambda x,y: abs(x-.6)<.5 and abs(y+1.0)<.5)
def CHAAND():
    shop_night(); m=master_at_counter(); P=outside_crowd(); wa=mk(WALEED,.6,-1.0,180,'wa')
    def upd(t):
        stand(m,t); blink(m,t); face(m,mouth='O',eyes=1.2,brow=.06); look_at(m,(0,-2,1.5),.5)
        chant(P,t,on=False); stand(wa,t); blink(wa,t); face(wa,mouth='flat',brow=-.05)
        q=ease(t/DUR)
        if t<ws(100)-.1: camset(LV((-4,-9.5,4.5),(-3,-8.6,3.8),q),(-4,8,6),20,5)
        else: camset(LV((-2.8,-7.4,2.3),(-2.2,-6.4,2.1),q),(0,0,1.6),22,5)
    return dict(upd=upd)
SHOTS['CHAAND']=CHAAND
def CROWD_():
    shop_night(); m=master_at_counter(); P=outside_crowd(); wa=mk(WALEED,.6,-1.0,180,'wa'); P.append(wa); wa['ph']=1.3
    def upd(t):
        stand(m,t); blink(m,t); face(m,mouth='O',eyes=1.25,brow=.08)
        chant(P,t,on=True,k=1.0)
        camset((1.8,4.6,1.7),(0,-1.6,1.5),22,4)
    return dict(upd=upd)
SHOTS['CROWD']=CROWD_
def SEW(mode='on'):
    def S_():
        shop_night(); m=mk(MASTER,MACHINE[0],MACHINE[1]+.62,0,'master'); P=outside_crowd(10)
        for k in range(8): B.box((.2,4.2,.95+k*.07),(.45,.32,.03),M(['#C8372D','#2E6B4F','#E8C547','#5A7FB0','#F4F1EA','#9A3A5A'][k%6],.85,kind='fabric'),.01)
        B.done('stack')
        tube=[o for o in bpy.data.objects if o.type=='LIGHT' and o.data.type=='POINT' and abs(o.location.z-3.0)<.05 and abs(o.location.y-4.0)<.05]
        tubeE=[o.data.energy for o in tube]; torches=[]
        if mode!='on':
            for i,H in enumerate(P):
                ph=phone_in_hand(H,1,'#FFFFFF',em=0); torches.append((H,ph,point((0,0,0),0,(1,.97,.9),r=.05,shadow=False)))
        def upd(t):
            seat(m,t,.55); m['root'].location=(MACHINE[0],MACHINE[1]+.62,0); blink(m,t); u=m['u']; sp=math.sin(t*38)
            arm_to(m,1,Vector((MACHINE[0]+.1,MACHINE[1]-.05,.82+.01*sp)),1); arm_to(m,-1,Vector((MACHINE[0]-.25,MACHINE[1]-.05,.82-.01*sp)),1)
            face(m,mouth='flat',brow=-.06,brow_r=-12,eyes=1.15); m['head'].rotation_euler[0]=R(12)
            chant(P,t,on=(mode=='on'),k=.6)
            off=0
            if mode=='dark': off=tl(t,ws(130)-.05,ws(130)+.05)
            if mode=='torch': off=1
            for o,e in zip(tube,tubeE): o.data.energy=e*(1-off)
            for H,ph,l in torches:
                kk=tl(t,ws(132)+H['ph']*.12,ws(132)+H['ph']*.12+.15) if mode=='torch' else 0; u_=H['u']
                arm_to(H,1,root_mat(H)@Vector((.3*u_,-1.6*u_,(3.8+.6*kk)*u_)),kk); l.location=ph.matrix_world.translation+Vector((0,.15,0)); l.data.energy=22*kk
                for o in ph.children: pass
            FILLE[0]=40*(1-off)+6*off
            if mode=='on': camset((-.2,2.2,1.6),(MACHINE[0],MACHINE[1],1.05),26,2.8)
            elif mode=='dark': camset((.4,1.4,1.75),(MACHINE[0],MACHINE[1],1.1),24,4)
            else: q=ease(t/DUR); camset(LV((2.2,4.9,1.9),(2.1,4.6,1.85),q),(-.6,1.0,1.1),20,5)
        return dict(upd=upd)
    return S_
SHOTS['SEW']=SEW('on'); SHOTS['DARK']=SEW('dark'); SHOTS['TORCH']=SEW('torch')
def PACKET():
    shop_night('CHAAND RAAT'); m=master_at_counter(); wa=mk(WALEED,WC[0],WC[1],0,'wa')
    pk=empty((0,0,0)); obox((0,0,0),(.22,.15,.08),M('#C9A06A',.8,kind='fabric'),.02,pk); obox((0,0,.081),(.23,.02,.002),M('#C8372D',.5),0,pk)
    def upd(t):
        stand(m,t); blink(m,t); face(m,mouth='smile',eyes=.6,brow=-.02); u=m['u']
        k=tl(t,.2,.8); hm=Vector((.15,COUNTER_Y-.1,1.25))
        arm_to(m,1,hm,k*(1-tl(t,1.3,1.6)))
        kt=tl(t,1.0,1.3); blink(wa,t)
        if t<ws(149):
            stand(wa,t); wa['root'].location=(WC[0],WC[1],0); wa['root'].rotation_euler[2]=R(0); arm_to(wa,1,hm+Vector((0,-.1,0)),tl(t,.6,1.0)); face(wa,mouth='O' if t<1.3 else 'grin',eyes=.7 if t<1.0 else 1.2,brow=.05)
            pk.location=hm if t<1.3 else wa['arm'][1].matrix_world@Vector(hand_loc(wa,1))
        else:
            walk_path(wa,[WC,(-.5,0),(-2.5,-3.5),(-8,-4.5)],t,ws(149),DUR+.6,run_=True,ease_in=.1); pk.location=wa['arm'][1].matrix_world@Vector(hand_loc(wa,1)); face(wa,mouth='grin',brow=.06)
        if t<ws(149)-.1: camset((1.9,-.6,1.9),(.1,COUNTER_Y-.4,1.45),26,4)
        else: camset((-1.0,-6.0,1.7),(-1.5,-1.5,1.3),24,5)
    return dict(upd=upd)
SHOTS['PACKET']=PACKET
def OPEN():
    courtyard(); setup_world('night',shadow=20); wa=mk(WALEED,60.4,1.2,0,'wa')
    k_=empty((0,0,0)); kb=M('#D8CFB4',.85,kind='fabric')
    obox((0,0,0),(.13,.015,.17),kb,.02,k_); [obox((s*.15,0,.1),(.06,.012,.05),kb,.01,k_) for s in (1,-1)]; obox((0,-.016,.12),(.02,.002,.05),M('#E8C547',.4),0,k_)
    pk=empty((0,0,0)); obox((0,0,0),(.22,.15,.08),M('#C9A06A',.8,kind='fabric'),.02,pk)
    def upd(t):
        stand(wa,t); blink(wa,t); u=wa['u']; k=tl(t,.15,.7)
        pk.location=root_mat(wa)@Vector((0,-1.4*u,2.4*u)); pk.rotation_euler=(0,0,0)
        if t>.7: pk.location=(60.9,1.0,.0+.08)
        for s in (1,-1): arm_to(wa,s,root_mat(wa)@Vector((s*.3*u,-1.7*u,L(2.6,3.3,k)*u)),1)
        k_.location=root_mat(wa)@Vector((0,-1.8*u,L(2.4,3.1,k)*u)) if t>.5 else Vector((0,0,-30)); k_.rotation_euler=(0,0,0)
        face(wa,mouth='smile' if t<ws(154)-.2 else 'O',eyes=1.0+.4*tl(t,ws(154)-.2,ws(154)+.1),brow=.02+.06*tl(t,ws(154)-.2,ws(154)+.1)); look_at(wa,k_.location if t>.5 else pk.location,.6,maxpitch=40)
        talk(wa,t,*wt(154,157),rest='O')
        q=ease(t/DUR); camset(LV((60.4,-1.6,1.75),(60.4,-1.0,1.7),q),(60.4,1.2,1.55),30,2.8)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN
# --------------------------------------------------------------- Eid prayer
def eid_set():
    eidgah(); setup_world('day',shadow=60); FILLE[0]=15
    front=crowd(8,EID_X-5.2,EID_X+5.2,EID_Y,EID_Y,rz=180,seed=11,skip=lambda x,y: abs(x-EID_X)<1.0)
    back=crowd(8,EID_X-5.2,EID_X+5.2,EID_Y-2.5,EID_Y-2.5,rz=180,seed=13,skip=lambda x,y: abs(x-(EID_X+1.3))<.9)
    for H in front+back:
        H['root'].rotation_euler[2]=R(180)
    ma=mk(MASTER_EID,EID_X,EID_Y,180,'master'); wa=mk(WALEED_EID,EID_X+1.3,EID_Y-2.5,180,'wa')
    return front,back,ma,wa
def pray(P,t):
    for H in P:
        stand(H,t); blink(H,t); H['root'].rotation_euler[2]=R(180)
        for s in (1,-1): H['arm'][s].rotation_euler=(R(-62),0,R(-s*28))
def EID():
    front,back,ma,wa=eid_set()
    def upd(t):
        pray(front+back+[ma],t); stand(wa,t); blink(wa,t); wa['root'].rotation_euler[2]=R(180)
        for s in (1,-1): wa['arm'][s].rotation_euler=(R(-62),0,R(-s*28))
        face(wa,mouth='smile',brow=.02); kk=tl(t,ws(170),ws(172)); look_at(wa,hp(ma),.4*kk)
        if t<ws(166)-.1: q=ease(t/DUR); camset(LV((EID_X-7,EID_Y-12,6),(EID_X-5,EID_Y-10,5),q),(EID_X,EID_Y+4,4),20,6)
        elif t<ws(170)-.1: c0,tg,ln=closecam(wa,180,.3,1.5,lens=24,tz=-.35); camset(c0,tg,ln,2.8)
        else: c0,tg,ln=closecam(ma,180,0,L(2.4,1.7,tl(t,ws(170),DUR)),lens=24,tz=-.4); camset(c0,tg,ln,2.8)
    return dict(upd=upd)
SHOTS['EID']=EID
def EIDTALK(a,b,who,react=None,cam='ma'):
    def S_():
        front,back,ma,wa=eid_set()
        def upd(t):
            pray(front+back,t); stand(ma,t); blink(ma,t); stand(wa,t); blink(wa,t)
            ma['root'].rotation_euler[2]=R(face_dir(1.3,-2.5)*tl(t,-1,0)) ; wa['root'].rotation_euler[2]=R(face_dir(-1.3,2.5))
            sp,ls=(ma,wa) if who=='ma' else (wa,ma)
            talk(sp,t,*wt(a,b),rest='smile' if who=='ma' else 'O'); look_at(sp,hp(ls),.6); look_at(ls,hp(sp),.6)
            if who=='ma': face(ma,brow=.04); face(wa,mouth='flat',brow=-.08,brow_r=-16,eyes=.85)
            else: face(wa,brow=.08,eyes=1.3); face(ma,mouth='smile',eyes=.6)
            if react: react(ma,wa,t)
            if cam=='ma': c0,tg,ln=closecam(ma,face_dir(1.3,-2.5),-.4,2.8,lens=30,tz=-.35); camset(drift(c0,tg,t),tg,ln,2.8)
            else: c0,tg,ln=closecam(wa,face_dir(-1.3,2.5),.35,2.0,lens=24,tz=-.4); camset(drift(c0,tg,t),tg,ln,2.8)
        return dict(upd=upd)
    return S_
def _point(ma,wa,t): u=wa['u']; arm_to(wa,1,Vector(hp(ma))+Vector((0,0,-.6)),tl(t,ws(176)-.2,ws(176)+.2))
def _rev_turn(ma,wa,t): ma['root'].rotation_euler[2]=R(180+(face_dir(1.3,-2.5)-180)*tl(t,.2,.8)); face(ma,mouth='smile',eyes=.7)
SHOTS['REVEAL']=EIDTALK(174,179,'wa',react=lambda ma,wa,t:(_rev_turn(ma,wa,t),_point(ma,wa,t)),cam='wa')
SHOTS['MR1']=EIDTALK(180,188,'ma',react=lambda ma,wa,t: arm_to(ma,1,root_mat(ma)@Vector((.4*ma['u'],-1.2*ma['u'],3.0*ma['u'])),tl(t,ws(183),ws(184))))
SHOTS['MR2']=EIDTALK(189,199,'ma',react=lambda ma,wa,t: arm_to(ma,1,Vector(hp(wa))+Vector((0,0,-1.0)),tl(t,ws(194),ws(195))))
def CTA():
    front,back,ma,wa=eid_set()
    def upd(t):
        pray(front+back,t); stand(ma,t); stand(wa,t); blink(ma,t); blink(wa,t)
        ma['root'].rotation_euler[2]=R(face_dir(1.3,-2.5)); wa['root'].rotation_euler[2]=R(face_dir(-1.3,2.5))
        face(ma,mouth='smile',eyes=.6); face(wa,mouth='flat',brow=-.1,brow_r=-18,eyes=.75); look_at(wa,hp(ma),.6)
        u=wa['u']; arm_to(wa,-1,root_mat(wa)@Vector((-.15*u,-.9*u,5.4*u)),tl(t,.3,.7))
        c0,tg,ln=closecam(wa,face_dir(-1.3,2.5),.0,2.0,lens=26,tz=-.4); camset(drift(c0,tg,t,.18),tg,ln,2.8)
    return dict(upd=upd)
SHOTS['CTA']=CTA
SEQ=[('HOOK', 0.0), ('KAL0', 2.6), ('GIVE', 3.867), ('M1', 9.567), ('KAL2', 11.567), ('KAL3', 15.2), ('WAQFA', 19.033), ('CURTAIN', 23.133), ('JOOTE', 29.933), ('BEHIND', 32.6), ('CHAAND', 35.233), ('CROWD', 41.067), ('SEW', 43.567), ('DARK', 47.167), ('TORCH', 49.433), ('PACKET', 52.933), ('OPEN', 56.8), ('EID', 60.233), ('REVEAL', 66.667), ('MR1', 69.133), ('MR2', 72.433), ('CTA', 75.767)]
END=79.4
