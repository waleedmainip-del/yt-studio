# "Sialkot - Everyone Is an Exporter": shots. Rig note: brow_r POSITIVE = angry slant, NEGATIVE = worried slant.
SEQ=[('HOOK', 0.0), ('CHAIW', 2.533), ('CHAI', 3.867), ('MOQ', 4.567), ('THISIS', 7.233), ('CAME', 8.8), ('SMALL', 11.067), ('YAHAN', 12.733), ('SMILED', 13.867), ('BAS', 15.933), ('WORKSHOP', 17.933), ('UNCLE', 19.733), ('ONEFB', 20.567), ('KAHAN', 21.567), ('WORLDCUP', 23.3), ('HAANHAAN', 24.233), ('TRUE', 26.567), ('LAST4', 27.633), ('KICK', 29.567), ('NEVER', 31.433), ('EVERY', 33.6), ('TRIED', 36.567), ('CRICKET', 37.933), ('BAT', 39.567), ('SK1', 41.0), ('HOCKEY', 41.933), ('GLOVES', 43.8), ('SOUND', 45.567), ('KYABAJ', 47.567), ('BAAJA', 48.867), ('MEIN', 50.233), ('YES', 52.867), ('SHIPPED', 56.567), ('SOMEWHERE', 58.133), ('NOIDEA', 61.067), ('MET', 62.733), ('OLDBIKE', 64.933), ('SIMPLE', 65.933), ('NORMAL', 67.0), ('FORTY', 68.733), ('EKFB', 70.933), ('MOQ2', 73.133), ('SIRF', 75.0), ('SAMPLE', 76.8), ('HOPE', 78.867), ('THEEK', 80.867), ('AIRPORT', 82.933), ('NOBODY', 84.5), ('NEEDED', 86.0), ('NOBUILT', 87.933), ('BUILT', 89.133), ('AIRLINE', 92.133), ('OHVI', 93.133), ('WENTHOME', 94.5), ('ABBUQ', 96.133), ('KYALAYE', 98.0), ('ONEFB2', 99.633), ('ONEBAT', 100.633), ('ONEBILL', 101.433), ('BILLBHI', 102.733), ('DOLLAR', 104.3), ('SMALLCITY', 105.633), ('NOSEA', 106.8), ('WHOLE', 108.933), ('CTA', 112.0)]
END=114.9333
WI={'HOOK': 0, 'CHAIW': 7, 'CHAI': 11, 'MOQ': 12, 'THISIS': 17, 'CAME': 20, 'SMALL': 27, 'YAHAN': 34, 'SMILED': 37, 'BAS': 42, 'WORKSHOP': 46, 'UNCLE': 50, 'ONEFB': 52, 'KAHAN': 54, 'WORLDCUP': 59, 'HAANHAAN': 61, 'TRUE': 67, 'LAST4': 71, 'KICK': 78, 'NEVER': 85, 'EVERY': 92, 'TRIED': 100, 'CRICKET': 103, 'BAT': 108, 'SK1': 113, 'HOCKEY': 114, 'GLOVES': 117, 'SOUND': 119, 'KYABAJ': 125, 'BAAJA': 130, 'MEIN': 133, 'YES': 138, 'SHIPPED': 147, 'SOMEWHERE': 151, 'NOIDEA': 158, 'MET': 162, 'OLDBIKE': 167, 'SIMPLE': 169, 'NORMAL': 171, 'FORTY': 177, 'EKFB': 182, 'MOQ2': 188, 'SIRF': 193, 'SAMPLE': 197, 'HOPE': 203, 'THEEK': 208, 'AIRPORT': 214, 'NOBODY': 219, 'NEEDED': 222, 'NOBUILT': 226, 'BUILT': 229, 'AIRLINE': 238, 'OHVI': 240, 'WENTHOME': 244, 'ABBUQ': 249, 'KYALAYE': 253, 'ONEFB2': 258, 'ONEBAT': 260, 'ONEBILL': 262, 'BILLBHI': 265, 'DOLLAR': 270, 'SMALLCITY': 273, 'NOSEA': 276, 'WHOLE': 280, 'CTA': 290}
SHOTS={}
# portrait frame: 36 mm is the VERTICAL sensor size, so half-width/distance = 10.125/lens
def cam2(t,p0,p1,tg,lens,tg1=None):
    q=ease(t/DUR); camset(LV(p0,p1,q),tg if tg1 is None else LV(tg,tg1,q),lens,8)
def headw(H): return H['root'].matrix_world@Vector((0,0,4.75*H['u']))
def c1(t,H,yaw=12,dist=2.8,lens=36,dz=0.0,tz=-.22,push=.08,ref=None,q=None,sx=0.0):
    """single: camera in front of H (yaw degrees round from its facing), slow push-in"""
    h=headw(H); a=(H['root'].rotation_euler[2] if ref is None else R(ref))+R(yaw); f=Vector((math.sin(a),-math.cos(a),0)); d=dist*(1-push*(ease(t/DUR) if q is None else q)); h=h+Vector((-f.y,f.x,0))*sx
    camset(tuple(h+f*d+Vector((0,0,dz))),(h.x,h.y,h.z+tz),lens,8)
def c2(t,Ha,Hb,frm=(0,-1),lens=30,fit=1.0,dz=.1,tz=-.6,push=.07,sh=0.0,pad=1.5):
    """two-shot square on to the pair, from the side that frm points to; distance set so both fit"""
    a=headw(Ha); b=headw(Hb); m=(a+b)/2; d=b-a; d.z=0; n=Vector((-d.y,d.x,0)).normalized()
    if n.x*frm[0]+n.y*frm[1]<0: n=-n
    dist=(d.length+pad)/(2*10.125/lens)*fit*(1-push*ease(t/DUR))
    camset(tuple(m+n*dist+d.normalized()*sh+Vector((0,0,dz))),(m.x,m.y,m.z+tz),lens,8)
def fc(H,m):
    F=dict(calm=dict(mouth='smile',brow=0,brow_r=0,eyes=1.0),flat=dict(mouth='flat',brow=.01,brow_r=0,eyes=.9),bored=dict(mouth='flat',brow=.02,brow_r=-3,eyes=.78),happy=dict(mouth='grin',brow=.04,brow_r=0,eyes=1.05),
           shock=dict(mouth='O',brow=.07,brow_r=-6,eyes=1.3),worry=dict(mouth='o',brow=.05,brow_r=-12,eyes=1.15),sad=dict(mouth='frown',brow=.03,brow_r=-12,eyes=1.0),firm=dict(mouth='flat',brow=-.02,brow_r=8,eyes=.95),
           smug=dict(mouth='smile',brow=.03,brow_r=6,eyes=.82),dead=dict(mouth='flat',brow=.01,brow_r=0,eyes=.8),wow=dict(mouth='o',brow=.06,brow_r=0,eyes=1.25),laugh=dict(mouth='grin',brow=.05,brow_r=-4,eyes=.6))
    face(H,**F[m])
def carry(H,label='EXPORT',col='#C9A26A',s=1.0):
    u=H['u']; e=empty((0,-(.52+.28*s)*u,3.0*u),H['root']); obox((0,0,0),(.36*s,.26*s,.24*s),M(col,.85),.015,e); obox((0,0,.238*s),(.06*s,.26*s,.006),M('#B88A52',.8),0,e)
    if label: text(label,(0,-.266*s,0),(0,-1,0),.13*s,M('#3A2A1E',.6),ex=.003,parent=e)
    return e
def carry_pose(H):
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-58),R(-s*9),0)
def notes(n=5):
    N=[]
    for k in range(n):
        e=empty((0,0,-5)); m=M('#16171C',.5); oico((0,0,0),.12,m,e,sc=(1.2,.5,.9),sub=1); obox((.11,0,.24),(.016,.016,.24),m,0,e); obox((.19,0,.45),(.09,.016,.045),m,0,e); N.append(e)
    return N
def notes_upd(N,t,src,d=(0,-1,0),reach=5.0,rz=0.0):
    for k,e in enumerate(N):
        q=((t*.5+k/len(N))%1.0); s_=math.sin(pi*q)
        e.location=(src[0]+d[0]*reach*q+.5*math.sin(t*3+k*2.1),src[1]+d[1]*reach*q,src[2]+1.5*q+.25*math.sin(t*4+k)); e.scale=(s_,s_,s_); e.rotation_euler=(0,R(15*math.sin(t*5+k)),R(rz))
def piper(H,tag=False,tc='#B8232E'):
    """bagpipe tucked under the +x arm, both hands on the chanter"""
    u=H['u']; bp=bagpipe_o(H['root'],1.0,tc,tag); bp.location=(.74*u,-.5*u,3.0*u); return bp
def pipe_pose(H,t):
    H['arm'][1].rotation_euler=(R(-34+2*math.sin(t*9)),R(-14),0); H['arm'][-1].rotation_euler=(R(-44+2*math.sin(t*9+1.5)),R(30),0)
def scot_kit(H):
    u=H['u']; rt=H['root']; tc=M('#B8232E',.8,kind='fabric'); gc=M('#1E4A2E',.8)
    obox((0,0,1.6*u),(.9*u,.52*u,.68*u),tc,.03,rt)
    for q in (-.5,0,.5): obox((q*u,0,1.6*u),(.05*u,.53*u,.69*u),gc,0,rt)
    for z in (1.25,1.9): obox((0,0,z*u),(.91*u,.53*u,.05*u),gc,0,rt)
    obox((0,-.56*u,1.7*u),(.2*u,.05*u,.22*u),M('#F2E9D0',.8,kind='fabric'),.04,rt)
# ================================================================ set A: bazaar
def wcast(i): return WORK[i] if i>=0 else person(40-i*13)
def baz(who='',wk=(),mood='sk_day',lights=True,pp=(14.8,7.4)):
    """who: c chai wala, f football shop, b bat shop, h hockey shop, p bagpipe maker. wk: walkers (cast idx, lane y, dir, x at shot start, carton label)"""
    bazaar(mood,lights); A=dict(W=[],pp=pp); FILLE[0]=0
    if 'c' in who: A['chai']=mk(CHAIW,-10.3,6.95,0,'chaiw')
    if 'f' in who: A['ballm']=mk(WORK[1],-4.3,6.9,0,'ballm')
    if 'b' in who: A['bat']=mk(SHOPK,-.5,7.35,0,'shopk')
    if 'h' in who: A['hock']=mk(WORK[3],6.6,7.25,0,'hockm')
    if 'p' in who: A['pipe']=mk(PIPEM,pp[0],pp[1],0,'pipem'); A['bp']=piper(A['pipe'])
    for k,(ci,y,d,x0,lab) in enumerate(wk):
        H=mk(wcast(ci),x0,y,90*d,'w%d'%k); A['W'].append(dict(H=H,y=y,d=d,x0=x0,box=carry(H,lab,s=1.2)))
    return A
def baz_idle(A,t):
    for k in ('chai','ballm','bat','hock'):
        if k in A: H=A[k]; standp(H,t,H['root'].location[0],H['root'].location[1],0); fc(H,'calm')
    if 'pipe' in A: H=A['pipe']; standp(H,t,A['pp'][0],A['pp'][1],0); pipe_pose(H,t); face(H,mouth='o',brow=.03,eyes=1.0); blink(H,t,force=1); H['root'].rotation_euler[1]=R(3*math.sin(t*3))
    for p in A['W']:
        H=p['H']; H['root'].location[0]=p['x0']+p['d']*1.25*t; H['root'].location[1]=p['y']; H['root'].rotation_euler[2]=R(90*p['d']); walk(H,1.25*(t+3),step=.5); carry_pose(H); blink(H,t); fc(H,'calm')
def boys(A): A['wa']=mk(WALEED,0,0,0,'waleed'); A['za']=mk(ZAIN,0,0,0,'zain'); return A['wa'],A['za']
def HOOK():
    A=baz('c',[(0,.3,-1,-12.6,'EXPORT'),(2,-1.6,-1,-8.0,'EXPORT'),(-1,2.0,-1,-5.5,'EXPORT'),(-2,-.5,-1,-1.5,'EXPORT'),(-3,1.3,-1,3.5,'EXPORT'),(-4,-2.6,1,6.0,None),(-5,2.9,1,-2.0,None)])
    def upd(t): baz_idle(A,t); cam2(t,(-20.6,.15,1.9),(-20.0,.15,2.0),(0,.15,3.3),24)
    return dict(upd=upd)
SHOTS['HOOK']=HOOK
def CHAIW_():
    A=baz('c'); ch=A['chai']; kt=empty((0,0,-5)); ocyl((0,0,.13),.15,.27,M('#C9CED8',.25,metal=.9),kt,rot=(0,0,0),seg=12,r2=.1); ocyl((.18,0,.18),.02,.22,M('#C9CED8',.25,metal=.9),kt,rot=(0,R(60),0),seg=6)
    def upd(t):
        baz_idle(A,t); fc(ch,'flat'); k=tl(t,.1,.5); ch['arm'][1].rotation_euler=(R(-74-12*k),R(-10),0); ch['arm'][-1].rotation_euler=(R(-56),R(8),0)
        kt.location=Vector(handw(ch,1))+Vector((0,0,.02)); kt.rotation_euler=(R(32*k),0,R(-90)); look_at(ch,(-10.3,5.9,1.4),1.0,maxpitch=20)
        c1(t,ch,yaw=10,dist=3.0,lens=36)
    return dict(upd=upd)
SHOTS['CHAIW']=CHAIW_
WP=(-11.7,4.4); ZP=(-9.6,4.5)
def CHAI():
    A=baz('c',[(2,-1.6,1,-15.0,None)],lights=False); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); standp(wa,t,WP[0],WP[1],172); standp(za,t,ZP[0],ZP[1],190); fc(za,'calm'); fc(wa,'calm'); speak(wa,t,11,11,gesture=False)
        wa['arm'][1].rotation_euler=(R(-112),R(-14),0); look_at(wa,hp(A['chai']),.7,maxyaw=35); look_at(za,hp(A['chai']),1.0,maxyaw=35)
        c1(t,wa,yaw=4,dist=2.5,lens=36)
    return dict(upd=upd)
SHOTS['CHAI']=CHAI
def MOQ():
    A=baz('c'); ch=A['chai']
    def upd(t):
        baz_idle(A,t); fc(ch,'dead'); speak(ch,t,12,16,gesture=False); look_at(ch,(-11.7,4.4,2.0),.7)
        k=tl(t,ws(14)-.1,ws(14)+.2); ch['arm'][1].rotation_euler=(R(-60-70*k),R(8*k),0); ch['arm'][-1].rotation_euler=(R(-40),R(6),0)
        c1(t,ch,yaw=-6,dist=2.8,lens=38)
    return dict(upd=upd)
SHOTS['MOQ']=MOQ
def THISIS():
    A=baz('',[(0,-1.2,1,33.0,'EXPORT'),(-1,1.4,-1,37.0,None)])
    def upd(t): baz_idle(A,t); cam2(t,(24.8,-2.8,1.7),(25.8,-2.4,2.2),(40,0,9.4),20,(40,0,10.4))
    return dict(upd=upd)
SHOTS['THISIS']=THISIS
def CAME():
    A=baz('f',[(0,-4.5,-1,1.0,None),(-1,4.8,-1,5.0,None)]); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); walk_path(wa,[(-10.6,1.05),(-5.0,1.05)],t,-.5,DUR+.6,step=.5,arm=22); walk_path(za,[(-10.4,2.8),(-4.8,2.8)],t,-.5,DUR+.6,step=.5,arm=22)
        fc(wa,'bored'); fc(za,'calm'); x=wa['root'].location[0]; look_at(wa,(x+4,1.05-5*math.sin(t*2.0),2.7),.8,maxyaw=45)
        camset((x+5.8,1.9,1.9),(x,1.92,1.5),28,8)
    return dict(upd=upd)
SHOTS['CAME']=CAME
def b1(A,t): standp(A['wa'],t,-6.1,2.0,14); standp(A['za'],t,-4.3,2.2,-14)
def SMALL():
    A=baz('f',[(2,4.7,1,-11.0,None)]); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b1(A,t); fc(wa,'bored'); fc(za,'calm'); crossed(wa,tl(t,.2,.6)); look_at(wa,(-6+7*math.sin(t*2.4),-6,2.9),1.0,maxyaw=50); look_at(za,hp(wa),1.0,maxyaw=40)
        c1(t,wa,yaw=-12,dist=2.8)
    return dict(upd=upd)
SHOTS['SMALL']=SMALL
def YAHAN():
    A=baz('f',[(2,4.7,1,-8.5,None)]); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b1(A,t); fc(wa,'bored'); fc(za,'calm'); look_at(wa,hp(za),1.0,maxyaw=38); look_at(za,hp(wa),1.0,maxyaw=38); speak(wa,t,34,36,gesture=False); what_pose(wa,tl(t,.05,.3),t,.5)
        c2(t,wa,za,frm=(0,-1),lens=30)
    return dict(upd=upd)
SHOTS['YAHAN']=YAHAN
def SMILED():
    A=baz('f'); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b1(A,t); fc(wa,'bored'); k=tl(t,.15,.6); face(za,mouth='smile' if k>.4 else 'flat',brow=.03*k,brow_r=6*k,eyes=1.0-.18*k); look_at(za,hp(wa),.5,maxyaw=30); za['head'].rotation_euler[1]=R(5*k)
        c1(t,za,yaw=12,dist=3.0,push=.14,q=.5*t/DUR)
    return dict(upd=upd)
SHOTS['SMILED']=SMILED
def BAS():
    A=baz('f'); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b1(A,t); fc(wa,'bored'); fc(za,'smug'); look_at(za,hp(wa),.5,maxyaw=30); za['head'].rotation_euler[1]=R(5); speak(za,t,42,45,gesture=False)
        k=tl(t,ws(43)-.15,ws(43)+.2); za['arm'][-1].rotation_euler=(R(-22*k),R(34*k),0); za['arm'][1].rotation_euler=(R(-22*k),R(-34*k),0)
        c1(t,za,yaw=12,dist=3.0,push=.14,q=.5+.5*t/DUR)
    return dict(upd=upd)
SHOTS['BAS']=BAS
# ================================================================ set B: football workshop
UNP=(1.7,1.1); WW=(-.5,-1.1); ZW=(-2.1,-.4)
def fbw(boys_=True):
    A=fb_workshop(); FILLE[0]=18; un=mk(STITCH,UNP[0],UNP[1],0,'stitch'); un['home']=(UNP[0],UNP[1],0); A['un']=un; A['ball']=ball_o(r=.25)
    if boys_: A['wa']=mk(WALEED,WW[0],WW[1],131,'waleed'); A['za']=mk(ZAIN,ZW[0],ZW[1],111,'zain')
    return A
def stitch(A,t,work=1.0,up=0.0,look=None):
    """the old stitcher on his stool. work = needle hand moving, up = lifts the ball in his right hand, look = world point to look at (else he watches the ball)"""
    un=A['un']; sitp(un,t,seat=.61,lean=8*(1-up)*(0 if look else 1)); w=work*(1-up)
    un['arm'][-1].rotation_euler=(R(-50),R(12),0); un['arm'][1].rotation_euler=(R(-50+12*w*math.sin(t*5.5)-88*up),R(-12+7*w*math.sin(t*5.5)-30*up),0)
    hl=Vector(handw(un,-1)); hr=Vector(handw(un,1)); lapp=(hl+hr)/2+Vector((0,-.1,.06)); A['ball'].location=lapp.lerp(hr+Vector((0,0,.3)),up); A['ball'].rotation_euler=(t*.4*(1-up),0,t*.3*(1-up))
    if look: look_at(un,look,1.0,maxyaw=55,maxpitch=25)
    else: look_at(un,tuple(A['ball'].location),1.0,maxpitch=20+25*up)
def fb_boys(A,t,m='calm',mz='calm',at=None):
    wa,za=A['wa'],A['za']; standp(wa,t,WW[0],WW[1],131); standp(za,t,ZW[0],ZW[1],111); fc(wa,m); fc(za,mz); g=at or hp(A['un']); look_at(wa,g,1.0,maxyaw=30); look_at(za,g,1.0,maxyaw=30)
def WORKSHOP():
    A=fbw(False)
    def upd(t): stitch(A,t); fc(A['un'],'flat'); cam2(t,(.2,-2.9,1.5),(.55,-2.1,1.45),(1.4,1.2,1.3),24)
    return dict(upd=upd)
SHOTS['WORKSHOP']=WORKSHOP
def UNCLE():
    A=fbw(False)
    def upd(t): stitch(A,t); fc(A['un'],'flat'); c1(t,A['un'],yaw=-16,dist=2.9,lens=36,dz=-.15,tz=-.38)
    return dict(upd=upd)
SHOTS['UNCLE']=UNCLE
def ONEFB():
    A=fbw(False)
    def upd(t): stitch(A,t); fc(A['un'],'flat'); b=Vector(A['ball'].location); q=ease(t/DUR); camset(tuple(b+Vector((-.55,-1.5+.15*q,.45))),tuple(b+Vector((0,0,.06))),44,8)
    return dict(upd=upd)
SHOTS['ONEFB']=ONEFB
def KAHAN():
    A=fbw()
    def upd(t):
        stitch(A,t); fb_boys(A,t,'calm',at=tuple(A['ball'].location)); fc(A['un'],'flat'); wa=A['wa']; speak(wa,t,54,58,gesture=False); pointw(wa,-1,tuple(A['ball'].location),tl(t,.05,.35))
        c2(t,wa,A['za'],frm=(.4,.9),lens=30,fit=.95)
    return dict(upd=upd)
SHOTS['KAHAN']=KAHAN
def WORLDCUP():
    A=fbw()
    def upd(t):
        fb_boys(A,t); un=A['un']; stitch(A,t,work=.2,look=hp(A['wa'])); fc(un,'dead'); speak(un,t,59,60,gesture=False); c1(t,un,yaw=-24,dist=2.5,lens=40,dz=-.1)
    return dict(upd=upd)
SHOTS['WORLDCUP']=WORLDCUP
def HAANHAAN():
    A=fbw()
    def upd(t):
        stitch(A,t,work=.2,look=hp(A['wa'])); fb_boys(A,t,'calm','dead'); wa,za=A['wa'],A['za']; fc(wa,'laugh'); speak(wa,t,61,66,gesture=False); wa['root'].rotation_euler[0]=R(-6+4*math.sin(t*11)); wa['head'].rotation_euler[0]=R(-8+5*math.sin(t*11))
        wa['arm'][-1].rotation_euler=(R(-70+12*math.sin(t*10)),R(20),0); k=tl(t,ws(63),ws(63)+.25); wa['arm'][1].rotation_euler=(R(-46*k),R(30*k),0); look_at(za,hp(wa),1.0,maxyaw=45)
        c2(t,wa,za,frm=(.4,.9),lens=32,fit=.92,sh=.1)
    return dict(upd=upd)
SHOTS['HAANHAAN']=HAANHAAN
def TRUE_():
    A=fbw()
    def upd(t):
        fb_boys(A,t); un=A['un']; stitch(A,t,work=0,look=hp(A['wa'])); fc(un,'dead'); un['head'].rotation_euler[0]+=R(7); face(un,brow=.05*tl(t,.2,.5)); c1(t,un,yaw=-20,dist=2.2,lens=44,dz=-.25,tz=-.12,push=.12)
    return dict(upd=upd)
SHOTS['TRUE']=TRUE_
def NEVER():
    A=fbw()
    def upd(t):
        k=tl(t,.1,.7); stitch(A,t,1-k,k); fb_boys(A,t,'shock'); un=A['un']; face(un,mouth='smile',brow=.03,brow_r=-6,eyes=1.0); c1(t,un,yaw=-12,dist=3.4,lens=34,dz=-.55,tz=.3)
    return dict(upd=upd)
SHOTS['NEVER']=NEVER
def WHOLE():
    A=fbw(False); un=A['un']; SL=(0,3.62,2.78)
    def upd(t):
        k=tl(t,.5,1.0); tr=tl(t,1.5,2.2); standp(un,t,-.15,2.75,L(180,25,tr)); un['arm'][1].rotation_euler=(R(L(-60,-128,k)*(1-tr)-10*tr),R(-6),0)
        hw=Vector(handw(un,1)); A['ball'].location=tuple(LV(hw+Vector((0,.1,.25)),Vector(SL),tl(t,.85,1.05))); A['ball'].rotation_euler=(0,0,0); fc(un,'calm' if tr>.5 else 'flat')
        cam2(t,(.6,-1.4,2.1),(.35,-.2,2.1),(-.1,3.2,2.15),28)
    return dict(upd=upd)
SHOTS['WHOLE']=WHOLE
# ================================================================ set C: stadium
PSPOT=(0,19.5)
def stad():
    A=stadium(); FILLE[0]=0; A['ball']=ball_o(r=.24); A['st']=mk(PLAY[0],-.8,16.3,180,'striker'); A['gk']=mk(PLAY[2],0,25.7,0,'keeper'); return A
def LAST4():
    A=stad()
    def upd(t):
        st,gk=A['st'],A['gk']; standp(st,t,-.8,16.3,180); fc(st,'firm'); standp(gk,t,.5*math.sin(t*5),25.7,0); arms_up(gk,.55,t,60,jig=6); fc(gk,'firm')
        A['ball'].location=(PSPOT[0],PSPOT[1],.24); cam2(t,(.6,17.6,.42),(.3,18.15,.5),(0,21.5,1.3),24)
    return dict(upd=upd)
SHOTS['LAST4']=LAST4
def KICK():
    A=stad(); tk=.7
    def upd(t):
        st,gk=A['st'],A['gk']
        if t<tk: walk_path(st,[(-.8,16.3),(-.3,19.0)],t,0,tk,step=.75,arm=40,run_=True,ease_in=.3,ease_out_=.05)
        else: standp(st,t,-.3,19.0,180); st['arm'][1].rotation_euler=(R(-40),R(-50),0); st['arm'][-1].rotation_euler=(R(30),R(40),0)
        kk=tl(t,tk-.1,tk+.08)*(1-tl(t,tk+.12,tk+.55)); st['leg'][1].rotation_euler[0]=R(-75*kk); st['root'].rotation_euler[0]=R(-8*kk); fc(st,'firm')
        q=max(0,min(1,(t-tk)/.5)); A['ball'].location=(L(0,3.05,q),L(19.5,27.3,q),.24+2.25*q+2.2*q*(1-q)); A['ball'].rotation_euler=(t*18,0,t*7)
        d=tl(t,tk+.05,tk+.42); standp(gk,t,-2.9*d,25.7,0); gk['root'].rotation_euler[1]=R(74*d); gk['root'].location[2]=.75*math.sin(pi*d)*(1 if d<1 else 0)+.32*d; arms_up(gk,.5+.5*d,t,30); fc(gk,'shock' if d>.3 else 'firm')
        cam2(t,(.3,11.6,4.9),(.4,12.6,4.7),(.3,22.5,1.3),30,(.8,23.5,1.5))
    return dict(upd=upd)
SHOTS['KICK']=KICK
def EVERY():
    A=stad()
    def upd(t):
        st,gk=A['st'],A['gk']; standp(gk,t,-2.9,25.7,0); gk['root'].rotation_euler[1]=R(84); gk['root'].location[2]=.34; arms_up(gk,1.0,t,30); fc(gk,'sad')
        walk_path(st,[(-1.0,20.0),(-6.0,22.0)],t,-.6,DUR+1.5,step=.8,arm=0,run_=True); arms_up(st,1.0,t,26,jig=10); fc(st,'happy')
        A['ball'].location=(3.05,27.45,.24+.5*abs(math.cos(t*7))*max(0,1-t/.9)); A['ball'].rotation_euler=(t*2.5*max(0,1-t/2.5),0,0)
        cam2(t,(4.9,30.1,.75),(4.3,29.6,.85),(2.2,26.0,.8),26)
    return dict(upd=upd)
SHOTS['EVERY']=EVERY
# ================================================================ bazaar again: bats, hockey, gloves
def b2(A,t): standp(A['wa'],t,.1,2.3,14); standp(A['za'],t,1.9,2.45,-14)
def TRIED():
    A=baz('b',[(2,-4.5,-1,5.0,None)]); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); walk_path(wa,[(-3.9,2.2),(-.2,2.2)],t,-.2,DUR+.3,step=.6,arm=30); walk_path(za,[(-6.2,3.3),(-2.6,3.3)],t,-.2,DUR+.3,step=.5,arm=20); fc(wa,'firm'); fc(za,'calm'); x=wa['root'].location[0]
        camset((x+4.2,2.0,1.95),(x+.1,2.3,1.7),32,8)
    return dict(upd=upd)
SHOTS['TRIED']=TRIED
def CRICKET():
    A=baz('b',[(2,4.7,-1,5.0,None)]); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b2(A,t); fc(wa,'smug'); fc(za,'calm'); look_at(wa,hp(za),.5,maxyaw=30); look_at(za,hp(wa),1.0,maxyaw=38); speak(wa,t,103,107,gesture=False)
        k=tl(t,.05,.3); wa['arm'][-1].rotation_euler=(R(-146*k),R(8*k),0); wa['arm'][1].rotation_euler=(R(-18*k),R(-40*k),0)
        c1(t,wa,yaw=-12,dist=2.9)
    return dict(upd=upd)
SHOTS['CRICKET']=CRICKET
def BAT():
    A=baz('b'); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b2(A,t); fc(wa,'smug'); fc(za,'smug'); look_at(wa,hp(za),1.0,maxyaw=38); look_at(za,hp(wa),.8,maxyaw=35); speak(za,t,108,112,gesture=False)
        k=tl(t,.05,.3); za['arm'][1].rotation_euler=(R(-150*k),R(-10*k),0)
        cam2(t,(1.0,-3.4,2.3),(1.0,-3.0,2.25),(1.0,2.5,2.25),26)
    return dict(upd=upd)
SHOTS['BAT']=BAT
def SK1():
    A=baz('b'); sk=A['bat']; bt=bat_o()
    def upd(t):
        baz_idle(A,t); fc(sk,'happy'); k=ease_out(tl(t,-.1,.25)); sk['arm'][1].rotation_euler=(R(-150*k),R(-10),0); bt.location=handw(sk,1); bt.rotation_euler=(R(180),0,R(14*math.sin(t*6)))
        c1(t,sk,yaw=8,dist=3.4,lens=34,tz=.1)
    return dict(upd=upd)
SHOTS['SK1']=SK1
def HOCKEY():
    A=baz('h'); hk=A['hock']; sk=empty((0,0,-5)); ocyl((0,0,-.3),.035,1.5,M('#C8372D',.5),sk,rot=(0,0,0),seg=8); obox((.11,0,-1.08),(.14,.035,.05),M('#F2EBDA',.6),.02,sk)
    def upd(t):
        baz_idle(A,t); fc(hk,'happy'); k=ease_out(tl(t,-.1,.25)); hk['arm'][-1].rotation_euler=(R(-120*k),R(10),0); sk.location=handw(hk,-1); sk.rotation_euler=(0,0,R(8*math.sin(t*5)))
        c1(t,hk,yaw=-8,dist=3.4,lens=34,tz=.05)
    return dict(upd=upd)
SHOTS['HOCKEY']=HOCKEY
def GLOVES():
    A=baz('h')
    def upd(t): baz_idle(A,t); cam2(t,(8.6,5.2,2.35),(8.3,5.8,2.3),(8.3,8.4,2.2),34)
    return dict(upd=upd)
SHOTS['GLOVES']=GLOVES
# ================================================================ the bagpipe shop: the boys look in from the pavement, the camera works from inside
WB=(12.25,3.9); ZB=(13.95,4.0)
def b3(A,t): standp(A['wa'],t,WB[0],WB[1],166); standp(A['za'],t,ZB[0],ZB[1],194)
PSRC=(15.1,6.6,2.7)
def SOUND():
    A=baz('p',[(2,-1.5,-1,20.0,'EXPORT'),(0,1.2,1,6.0,None)]); wa,za=boys(A); N=notes(4)
    def upd(t):
        baz_idle(A,t); walk_path(wa,[(10.1,3.9),WB],t,-.3,1.05,step=.5,arm=22); walk_path(za,[(11.8,4.0),ZB],t,-.3,1.1,step=.5,arm=20)
        k=tl(t,1.05,1.5); fc(za,'calm'); fc(wa,'worry' if k>.3 else 'flat')
        if t>1.05: standp(wa,t,WB[0],WB[1],L(90,166,k)); standp(za,t,ZB[0],ZB[1],L(90,194,tl(t,1.2,1.7))); look_at(wa,PSRC,1.0,maxyaw=50)
        else: look_at(wa,PSRC,tl(t,.6,1.0),maxyaw=70)
        notes_upd(N,t,PSRC,d=(-.25,-1,0),reach=3.0,rz=0); c2(t,wa,za,frm=(0,1),lens=24,push=0)
    return dict(upd=upd)
SHOTS['SOUND']=SOUND
def KYABAJ():
    A=baz('p',[(2,-1.5,-1,16.5,'EXPORT'),(0,1.2,1,9.0,None)]); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b3(A,t); fc(wa,'worry'); fc(za,'calm'); look_at(wa,hp(za),tl(t,.2,.5),maxyaw=38); look_at(za,hp(wa),1.0,maxyaw=38); speak(wa,t,125,129,gesture=False)
        c1(t,wa,yaw=16,dist=2.8)
    return dict(upd=upd)
SHOTS['KYABAJ']=KYABAJ
def BAAJA():
    A=baz('p',[(2,-1.5,-1,13.0,'EXPORT')]); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b3(A,t); fc(wa,'worry'); fc(za,'dead'); look_at(za,hp(wa),.5,maxyaw=30); speak(za,t,130,132,gesture=False); c1(t,za,yaw=-16,dist=2.8)
    return dict(upd=upd)
SHOTS['BAAJA']=BAAJA
def MEIN():
    A=baz('p'); wa,za=boys(A)
    def upd(t):
        baz_idle(A,t); b3(A,t); fc(wa,'shock'); fc(za,'smug'); speak(wa,t,133,137,gesture=False)
        hands_head(wa,tl(t,ws(136),ws(136)+.2)); look_at(wa,hp(za),1.0-tl(t,ws(135)-.2,ws(135)),maxyaw=40); c1(t,wa,yaw=16,dist=2.8,lens=36)
    return dict(upd=upd)
SHOTS['MEIN']=MEIN
def YES():
    A=baz('p'); wa,za=boys(A); N=notes(5)
    def upd(t):
        baz_idle(A,t); b3(A,t); notes_upd(N,t,(15.3,7.0,2.9),d=(-.4,-.6,0),reach=2.2); c1(t,A['pipe'],yaw=4,dist=2.9,lens=36,push=.2,tz=-.3)
    return dict(upd=upd)
SHOTS['YES']=YES
def SHIPPED():
    A=baz('h',[(0,4.7,-1,12.0,None)]); wk=mk(WORK[2],0,0,90,'porter'); ct=handcart(0,0,180); bx=empty((0,0,.67),ct); obox((0,0,.36),(.62,.44,.36),M('#C9A26A',.85),.015,bx); obox((0,0,.722),(.1,.44,.006),M('#B88A52',.8),0,bx)
    text('TO: SCOTLAND',(0,.448,.4),(0,1,0),.15,M('#3A2A1E',.6),ex=.003,parent=bx)
    def upd(t):
        baz_idle(A,t); x=4.6+1.5*t; ct.location=(x,1.4,0); wk['root'].location[0]=x-2.3; wk['root'].location[1]=1.4; walk(wk,1.5*t+2,step=.5); wk['root'].rotation_euler[2]=R(90)
        for s in (1,-1): wk['arm'][s].rotation_euler=(R(-50),R(-s*4),0)
        fc(wk,'calm'); blink(wk,t); camset((x-.7,-3.2,1.75),(x-1.0,1.4,1.2),22,8)
    return dict(upd=upd)
SHOTS['SHIPPED']=SHIPPED
# ================================================================ set D: Scotland
def scot():
    scotland(); FILLE[0]=0; A={}; H=mk(SCOT,0,0,0,'scot',z=1.0); scot_kit(H); A['sc']=H; A['bp']=piper(H,True); A['N']=notes(4); return A
def scot_idle(A,t):
    H=A['sc']; standp(H,t,0,0,0); pipe_pose(H,t); face(H,mouth='o',brow=.04,brow_r=0,eyes=1.0); blink(H,t,force=1); H['root'].rotation_euler[1]=R(3*math.sin(t*3.2)); H['leg'][1].rotation_euler[0]=R(-9*max(0,math.sin(t*6.4)))
    notes_upd(A['N'],t,(.7,-.3,3.3),d=(.6,-.2,0),reach=2.4)
def SOMEWHERE():
    A=scot()
    def upd(t): scot_idle(A,t); c1(t,A['sc'],yaw=20,dist=5.4,lens=28,dz=-.7,tz=-.55,push=.14)
    return dict(upd=upd)
SHOTS['SOMEWHERE']=SOMEWHERE
def NOIDEA():
    A=scot()
    def upd(t):
        scot_idle(A,t); H=A['sc']; H['root'].rotation_euler[1]=0; g=A['bp'].matrix_world.translation; h=headw(H); q=ease(t/DUR)
        camset(tuple(LV((.45,-2.3,2.75),(.42,-1.45,2.45),q)),tuple(LV(((g.x+h.x)/2,-.2,(g.z+h.z)/2+.05),(g.x-.02,g.y-.2,g.z+.1),q)),36,8)
    return dict(upd=upd)
SHOTS['NOIDEA']=NOIDEA
# ================================================================ set E: the factory yard
CP=(-8.15,5.0); WP2=(-10.0,4.9); ZP2=(-11.75,5.1); BKP=(-5.2,3.0)
def fac(rider=False):
    factory(); FILLE[0]=0; A={}; A['wa']=mk(WALEED,WP2[0],WP2[1],18,'waleed'); A['za']=mk(ZAIN,ZP2[0],ZP2[1],22,'zain')
    if rider: A['bk']=kbike((0,0,0),180,'#8A3A2A',rider=RAFIQ,name='rafiq')
    else: A['bk']=kbike((0,0,0),180,'#8A3A2A'); A['ch']=mk(RAFIQ,CP[0],CP[1],-18,'rafiq'); A['cup']=cup_of(A['ch'],1)
    return A
def fac_idle(A,t,m='calm',mz='calm',sip=0.0):
    wa,za=A['wa'],A['za']; standp(wa,t,WP2[0],WP2[1],18); standp(za,t,ZP2[0],ZP2[1],22); fc(wa,m); fc(za,mz)
    if 'ch' in A:
        ch=A['ch']; standp(ch,t,CP[0],CP[1],-18); fc(ch,'calm'); roll(A['bk'],BKP[0],BKP[1],180,0); look_at(wa,hp(ch),1.0,maxyaw=30); look_at(za,hp(ch),1.0,maxyaw=30); look_at(ch,hp(wa),1.0,maxyaw=30); hold_chai(ch,A['cup'],1,sip=sip)
def MET():
    A=fac(True)
    def upd(t):
        fac_idle(A,t); q=ease_out(max(0,min(1,(t+.3)/(DUR+.7)))); x=L(9.0,-1.5,q); roll(A['bk'],x,3.0,180,9.0-x); fc(A['bk']['rider'],'calm'); A['bk']['root'].location[2]=.012*math.sin(t*38)
        camset((x-4.7,2.2,1.5),(x,3.0,1.45),36,8)
    return dict(upd=upd)
SHOTS['MET']=MET
def OLDBIKE():
    A=fac(True); P=[oico((0,0,-5),.14,M('#8A8E92',.9),None,sub=1) for k in range(4)]
    def upd(t):
        fac_idle(A,t); roll(A['bk'],BKP[0],BKP[1],180,0); A['bk']['root'].location[2]=.014*math.sin(t*40); A['bk']['root'].rotation_euler[1]=R(.8*math.sin(t*33)); fc(A['bk']['rider'],'calm')
        for k,o in enumerate(P): q=(t*1.4+k/4)%1.0; o.location=(BKP[0]+1.45+.9*q,BKP[1]-.15,.5+.6*q); o.scale=tuple(3*[.4+1.3*q])
        cam2(t,(BKP[0]+.5,-2.5,1.3),(BKP[0]+.3,-2.0,1.3),(BKP[0],3.0,1.2),30)
    return dict(upd=upd)
SHOTS['OLDBIKE']=OLDBIKE
def SIMPLE():
    A=fac()
    def upd(t):
        fac_idle(A,t); ch=A['ch']; ch['arm'][-1].rotation_euler=(R(-58+14*math.sin(t*11)),R(-26),0); look_at(ch,(CP[0],2.4,1.3),.6,maxpitch=25); c1(t,ch,yaw=8,dist=3.6,lens=34,tz=-.8,sx=.28)
    return dict(upd=upd)
SHOTS['SIMPLE']=SIMPLE
def NORMAL():
    A=fac()
    def upd(t):
        fac_idle(A,t,sip=.7*tl(t,.5,.95)*(1-tl(t,1.3,1.65))); ch=A['ch']; look_at(ch,(CP[0]+.2,-4,2.1),1.0); c1(t,ch,yaw=-8,dist=2.7,lens=38)
    return dict(upd=upd)
SHOTS['NORMAL']=NORMAL
def FORTY():
    A=fac()
    def upd(t):
        fac_idle(A,t); wa,za,ch=A['wa'],A['za'],A['ch']; k=tl(t,.15,.7); standp(wa,t,WP2[0],WP2[1],L(18,165,k)); standp(za,t,ZP2[0],ZP2[1],L(22,175,tl(t,.3,.9))); fc(wa,'wow'); fc(za,'smug')
        look_at(wa,(-9.9,6.8,5.5),1.0,maxyaw=40,maxpitch=40); look_at(ch,(-8.5,-6,2.4),1.0); fc(ch,'smug')
        cam2(t,(-9.9,-2.2,2.5),(-9.9,-1.5,2.7),(-9.9,6.2,3.7),24)
    return dict(upd=upd)
SHOTS['FORTY']=FORTY
def EKFB():
    A=fac()
    def upd(t):
        fac_idle(A,t); wa=A['wa']; fc(wa,'calm'); speak(wa,t,182,187,gesture=False); k=tl(t,.1,.4)
        for s in (1,-1): wa['arm'][s].rotation_euler=(R(-62*k+3*math.sin(t*8)),R(s*20*k),0)
        c1(t,wa,yaw=-16,dist=2.8)
    return dict(upd=upd)
SHOTS['EKFB']=EKFB
def MOQ2():
    A=fac()
    def upd(t): fac_idle(A,t); ch=A['ch']; fc(ch,'dead'); speak(ch,t,188,192,gesture=False); c1(t,ch,yaw=10,dist=2.7,lens=38)
    return dict(upd=upd)
SHOTS['MOQ2']=MOQ2
def SIRF():
    A=fac()
    def upd(t):
        fac_idle(A,t,'worry'); wa=A['wa']; speak(wa,t,193,196,gesture=False); k=tl(t,ws(195)-.2,ws(195)+.05); wa['arm'][-1].rotation_euler=(R(-140*k),R(8*k),0); wa['root'].rotation_euler[0]=R(4*k)
        c1(t,wa,yaw=-16,dist=2.7,lens=38)
    return dict(upd=upd)
SHOTS['SIRF']=SIRF
def SAMPLE():
    A=fac()
    def upd(t):
        fac_idle(A,t,'worry'); ch=A['ch']; fc(ch,'smug'); speak(ch,t,197,202,gesture=False); k=tl(t,.1,.4); ch['arm'][-1].rotation_euler=(R(-78*k+5*math.sin(t*13)*k),R(14*k),0)
        c1(t,ch,yaw=14,dist=2.5,lens=40)
    return dict(upd=upd)
SHOTS['SAMPLE']=SAMPLE
def HOPE():
    A=fac()
    def upd(t):
        k=tl(t,1.0,1.4); fac_idle(A,t,'smug' if k>.5 else 'firm'); wa=A['wa']; look_at(wa,(WP2[0]+3*math.sin(t*2.2),-6,3.6),1-k,maxyaw=50)
        c1(t,wa,yaw=-28,dist=2.6,lens=38)
    return dict(upd=upd)
SHOTS['HOPE']=HOPE
def THEEK():
    A=fac()
    def upd(t):
        fac_idle(A,t,'firm'); wa,za=A['wa'],A['za']; speak(wa,t,208,213,gesture=False); k=tl(t,ws(210)-.2,ws(210)+.15)
        for s in (1,-1): wa['arm'][s].rotation_euler=(R(-28*k),R(-s*(66+6*math.sin(t*9))*k),0)
        look_at(za,hp(wa),1.0,maxyaw=50); c2(t,za,wa,frm=(0,-1),lens=30,pad=2.4)
    return dict(upd=upd)
SHOTS['THEEK']=THEEK
def AIRPORT():
    A=fac()
    def upd(t):
        fac_idle(A,t,'smug'); wa=A['wa']; speak(wa,t,214,218,gesture=False); k=tl(t,.05,.35); wa['arm'][-1].rotation_euler=(R(-152*k),R(10*k),0); wa['arm'][1].rotation_euler=(R(-10*k),R(-36*k),0)
        c2(t,wa,A['ch'],frm=(0,-1),lens=28,fit=.93)
    return dict(upd=upd)
SHOTS['AIRPORT']=AIRPORT
def NOBODY():
    A=fac()
    def upd(t):
        fac_idle(A,t,'smug'); ch=A['ch']; fc(ch,'dead'); blink(ch,t,force=1 if (.3<t<.45 or .95<t<1.1) else 0); look_at(ch,(CP[0]-.3,-4,2.1),1.0); c1(t,ch,yaw=-6,dist=2.5,lens=40,push=.04)
    return dict(upd=upd)
SHOTS['NOBODY']=NOBODY
# ================================================================ set F: the field and the airport
MEN=[RAFIQ,SHOPK,BIZM[0],BIZM[1]]; MX=(-3.0,-1.0,1.0,3.0)
def NEEDED():
    airfield(False); FILLE[0]=0; P=[(-1.9+1.27*i,.35*i) for i in range(4)]; Hs=[mk(c,P[i][0],P[i][1],-20,'m%d'%i) for i,c in enumerate(MEN)]
    def upd(t):
        for i,H in enumerate(Hs):
            standp(H,t,P[i][0],P[i][1],-20); fc(H,'sad'); look_at(H,(-14+5*t,-16,13),1.0,maxyaw=50,maxpitch=30)
            if i==2: H['arm'][1].rotation_euler=(R(-150*tl(t,.3,.7)),R(-12),0)
            else: crossed(H,1.0)
        cam2(t,(-4.15,-3.55,1.45),(-3.95,-3.35,1.5),(-.6,.4,1.9),26)
    return dict(upd=upd)
SHOTS['NEEDED']=NEEDED
def NOBUILT():
    airfield(False); FILLE[0]=0; Hs=[mk(c,MX[i],-3.5,180,'m%d'%i) for i,c in enumerate(MEN)]
    def upd(t):
        for i,H in enumerate(Hs): standp(H,t,MX[i],-3.5,180); crossed(H,1.0 if i%2 else 0)
        cam2(t,(0,-14,3.2),(0,-13.4,3.2),(0,40,4.6),24)
    return dict(upd=upd)
SHOTS['NOBUILT']=NOBUILT
def BUILT():
    airfield(True); FILLE[0]=0; Hs=[mk(c,MX[i],-3.5,180,'m%d'%i) for i,c in enumerate(MEN)]; p1=plane(); p1.location=(-9,33.5,0); p2=plane()
    def upd(t):
        for i,H in enumerate(Hs): standp(H,t,MX[i],-3.5,180); arms_up(H,tl(t,.9+i*.12,1.25+i*.12),t,24,jig=8)
        q=max(0,min(1,(t+.4)/(DUR+.6))); x=L(-62,46,q*q*.6+q*.4); up=tl(q,.5,1.0); p2.location=(x,22,17*up*up); p2.rotation_euler=(0,R(-13*tl(q,.45,.75)),0)
        cam2(t,(0,-13.4,3.2),(0,-11.6,3.3),(0,40,4.6),24,(0,40,6.0))
    return dict(upd=upd)
SHOTS['BUILT']=BUILT
WP3=(-.9,-4.0); CP3=(1.0,-3.8)
def air2():
    airfield(True); FILLE[0]=0; A={}; A['wa']=mk(WALEED,WP3[0],WP3[1],10,'waleed'); A['ch']=mk(RAFIQ,CP3[0],CP3[1],-10,'rafiq'); A['cup']=cup_of(A['ch'],1); p1=plane(); p1.location=(-9,33.5,0); return A
def air_idle(A,t):
    wa,ch=A['wa'],A['ch']; standp(wa,t,WP3[0],WP3[1],10); standp(ch,t,CP3[0],CP3[1],-10); fc(wa,'shock'); fc(ch,'dead'); hold_chai(ch,A['cup'],1,sip=0)
def AIRLINE():
    A=air2()
    def upd(t):
        air_idle(A,t); wa=A['wa']; speak(wa,t,238,239,gesture=False); look_at(wa,hp(A['ch']),.45*tl(t,.05,.3),maxyaw=40); wa['arm'][-1].rotation_euler=(R(-50*tl(t,.05,.3)),R(-24),0)
        c1(t,wa,yaw=-10,dist=2.8)
    return dict(upd=upd)
SHOTS['AIRLINE']=AIRLINE
def OHVI():
    A=air2(); p2=plane()
    def upd(t):
        air_idle(A,t); ch=A['ch']; speak(ch,t,240,243,gesture=False); q=max(0,min(1,(t+.1)/(DUR+.2))); p2.location=(L(-42,36,q),30,L(13,21,q)); p2.rotation_euler=(0,R(-9),0)
        c1(t,ch,yaw=8,dist=2.5,lens=30,dz=-1.0,tz=.15)
    return dict(upd=upd)
SHOTS['OHVI']=OHVI
# ================================================================ set G: the house gate at night
WG=(-.9,1.3); AG=(1.0,3.5); BAGP=(-2.1,1.0)
def bag_b():
    e=empty((0,0,0)); obox((0,0,.3),(.5,.26,.26),M('#2A3550',.8,kind='fabric'),.12,e); obox((0,0,.6),(.3,.03,.05),M('#16171C',.7),.02,e); obox((0,-.27,.3),(.3,.01,.06),M('#E6B53A',.5),0,e); return e
def gate(abbu=True):
    A=homegate(); FILLE[0]=42; A['wa']=mk(WALEED,WG[0],WG[1],139,'waleed'); A['ab']=mk(ABBU,AG[0],AG[1] if abbu else 40,-41,'abbu'); A['bag']=bag_b(); A['bag'].location=(BAGP[0],BAGP[1],0); A['bag'].rotation_euler=(0,0,R(25)); return A
def gate_idle(A,t,wm='calm',am='firm'):
    wa,ab=A['wa'],A['ab']; standp(wa,t,WG[0],WG[1],139); standp(ab,t,AG[0],ab['root'].location[1],-41); fc(wa,wm); fc(ab,am); look_at(wa,(AG[0],AG[1],2.05),1.0,maxyaw=30); look_at(ab,hp(wa),1.0,maxyaw=30); crossed(ab,1.0)
def WENTHOME():
    A=gate(); wa=A['wa']
    def upd(t):
        gate_idle(A,t); walk_path(wa,[(-6.4,1.2),(-1.6,1.2),(WG[0],WG[1])],t,-.6,DUR+.2,step=.5,arm=14); fc(wa,'calm'); wa['arm'][-1].rotation_euler=(R(6),0,0)
        hw=Vector(handw(wa,-1)); A['bag'].location=(hw.x,hw.y,max(0,hw.z-.62)); A['bag'].rotation_euler=(0,0,wa['root'].rotation_euler[2]+R(90)); look_at(A['ab'],hp(wa),1.0,maxyaw=60)
        cam2(t,(-1.5,-5.0,2.05),(-1.1,-4.3,2.0),(-.5,2.6,1.8),24)
    return dict(upd=upd)
SHOTS['WENTHOME']=WENTHOME
def ABBUQ():
    A=gate(False)
    def upd(t): gate_idle(A,t,'happy'); wave_hi(A['wa'],t,.1,1,1.0); c1(t,A['wa'],yaw=4,dist=3.0,tz=-.05)
    return dict(upd=upd)
SHOTS['ABBUQ']=ABBUQ
def KYALAYE():
    A=gate()
    def upd(t):
        gate_idle(A,t); ab=A['ab']; face(ab,brow=.04,brow_r=6); speak(ab,t,253,257,gesture=False); k=tl(t,ws(255)-.2,ws(255)+.1); ab['arm'][-1].rotation_euler=(R(-50-8*k),R(-34+70*k),0)
        c1(t,ab,yaw=30,dist=2.8,lens=38)
    return dict(upd=upd)
SHOTS['KYALAYE']=KYALAYE
def show(A,t,k1,k2):
    """Waleed lifts the football (k1) then the bat (k2)"""
    wa=A['wa']; wa['arm'][1].rotation_euler=(R(-142*k1),R(-8*k1),0); A['fb'].location=Vector(handw(wa,1))+Vector((0,0,.3)) if k1>.02 else Vector((0,0,-5)); A['fb'].rotation_euler=(0,0,t*1.5)
    if k2>.02: wa['arm'][-1].rotation_euler=(R(-142*k2),R(8*k2),0); A['bt'].location=handw(wa,-1); A['bt'].rotation_euler=(R(180),0,R(139))
    else: A['bt'].location=(0,0,-5)
def ONEFB2():
    A=gate(False); A['fb']=ball_o(r=.26); A['bt']=bat_o()
    def upd(t): gate_idle(A,t,'happy'); show(A,t,ease_out(tl(t,0,.3)),0); c1(t,A['wa'],yaw=4,dist=3.3,lens=34,tz=.25,push=.1,q=.5*t/DUR)
    return dict(upd=upd)
SHOTS['ONEFB2']=ONEFB2
def ONEBAT():
    A=gate(False); A['fb']=ball_o(r=.26); A['bt']=bat_o()
    def upd(t): gate_idle(A,t,'happy'); show(A,t,1,ease_out(tl(t,0,.28))); c1(t,A['wa'],yaw=4,dist=3.3,lens=34,tz=.25,push=.1,q=.5+.5*t/DUR)
    return dict(upd=upd)
SHOTS['ONEBAT']=ONEBAT
def bill_o():
    e=empty((0,0,-5)); obox((0,0,-.62),(.17,.004,.62),M('#FBF8EE',.7),0,e); T=[text('BILL',(0,.008,-.14),(0,1,0),.1,M('#16171C',.5),ex=.002,parent=e),text('$ 86',(0,.008,-1.08),(0,1,0),.11,M('#B8232E',.5),ex=.002,parent=e)]
    for k in range(6): T.append(obox((0,.006,-.34-k*.11),(.12,.002,.012),M('#5A5A62',.6),0,e))
    return e,T
def bill_upd(B_,H,s,k,rz=-19):
    e,T=B_; e.location=handw(H,s); e.scale=(1,1,max(.03,k)); e.rotation_euler=(0,0,R(rz))
    for o in T: o.scale=(1,1,1) if k>.97 else (0,0,0)
def rest(A):
    """football on the ground by his feet, bat leaning in his left hand"""
    wa=A['wa']; A['fb'].location=(-1.75,1.75,.26); A['fb'].rotation_euler=(0,0,0); wa['arm'][-1].rotation_euler=(R(-8),R(10),0); A['bt'].location=handw(wa,-1); A['bt'].rotation_euler=(0,R(8),R(139))
def ONEBILL():
    A=gate(False); bi=bill_o(); A['fb']=ball_o(r=.26); A['bt']=bat_o()
    def upd(t):
        gate_idle(A,t); wa=A['wa']; face(wa,mouth='grin',brow=.05,brow_r=-10,eyes=1.1); rest(A); wa['arm'][1].rotation_euler=(R(-88),R(14),0); bill_upd(bi,wa,1,ease_out(tl(t,.1,.7)),rz=-41)
        c1(t,wa,yaw=4,dist=3.4,lens=34,tz=-.6,sx=.3,push=.04)
    return dict(upd=upd)
SHOTS['ONEBILL']=ONEBILL
def BILLBHI():
    A=gate()
    def upd(t):
        gate_idle(A,t); ab=A['ab']; fc(ab,'shock'); speak(ab,t,265,269,gesture=False); hands_head(ab,tl(t,.1,.35)); ab['root'].location[2]+=.12*math.sin(pi*max(0,min(1,(t-.05)/.25)))
        c1(t,ab,yaw=30,dist=2.8,lens=36)
    return dict(upd=upd)
SHOTS['BILLBHI']=BILLBHI
def DOLLAR():
    A=gate(False); bi=bill_o(); A['fb']=ball_o(r=.26); A['bt']=bat_o()
    def upd(t):
        gate_idle(A,t); wa=A['wa']; face(wa,mouth='grin',brow=.05,brow_r=-12,eyes=1.0); speak(wa,t,270,272,gesture=False); rest(A); wa['arm'][1].rotation_euler=(R(-88),R(14),0); bill_upd(bi,wa,1,1.0,rz=-41)
        c1(t,wa,yaw=5,dist=3.2,lens=34,tz=-.55,sx=.32,push=0)
    return dict(upd=upd)
SHOTS['DOLLAR']=DOLLAR
def CTA():
    A=gate(); bi=bill_o(); A['fb']=ball_o(r=.26); A['bt']=bat_o()
    def upd(t):
        gate_idle(A,t); wa,ab=A['wa'],A['ab']; k=tl(t,.0,.45); standp(wa,t,WG[0],WG[1],L(139,6,k)); fc(wa,'calm'); A['fb'].location=(-1.75,1.75,.26); A['bt'].location=(0,0,-5); speak(wa,t,290,296,gesture=False)
        what_pose(wa,tl(t,ws(294)-.1,ws(294)+.2),t,.6); fc(ab,'shock'); ab['arm'][-1].rotation_euler=(R(-10),0,0); ab['arm'][1].rotation_euler=(R(-104),R(-14),0); bill_upd(bi,ab,1,1.0,rz=139)
        look_at(ab,Vector(handw(ab,1))+Vector((0,-.2,-.5)),1.0,maxpitch=35)
        cam2(t,(-.25,-3.0,2.0),(-.15,-2.4,1.95),(0,2.4,1.6),28)
    return dict(upd=upd)
SHOTS['CTA']=CTA
# ================================================================ the city, golden hour
GW=[(0,.3,-1,-10.5,None),(2,-1.7,1,-17.0,None),(-1,2.0,-1,-2.5,None),(-2,-.5,1,3.5,None),(-3,1.3,-1,12.0,None),(-4,-2.6,1,-7.5,None),(-5,2.9,1,20.0,None)]
def SMALLCITY():
    A=baz('',GW,mood='sk_gold')
    def upd(t): baz_idle(A,t); cam2(t,(-37,0,13.5),(-34.5,0,12.8),(40,0,6.5),24)
    return dict(upd=upd)
SHOTS['SMALLCITY']=SMALLCITY
def NOSEA():
    A=baz('',GW,mood='sk_gold')
    def upd(t): baz_idle(A,t); cam2(t,(0,0,11.5),(7,0,15.5),(40,0,10.5),24,(40,0,9.0))
    return dict(upd=upd)
SHOTS['NOSEA']=NOSEA
