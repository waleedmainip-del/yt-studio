# Shots 18-34
WP=(0.0,-.2); SDP=(-1.45,-.2); GDP=(1.45,-.2)
def chips(e,s=1.0):
    obox((0,-.1,.14*s),(.12*s,.05*s,.16*s),M('#F2C14E',.35,spec=.7),.03,e); obox((0,-.152*s-.002,.14*s),(.1*s,.004,.06*s),M('#C8372D',.5),0,e)
    obox((0,-.1,.31*s),(.11*s,.04*s,.02*s),M('#F2C14E',.35,spec=.7),.01,e)
def wal_idle(wa,t,x=WP[0],y=WP[1],rz=0,mouth='smile'):
    place(wa,x,y,rz); wa['root'].rotation_euler[0]=0; hstand(wa,t); wa['head'].rotation_euler=(0,0,0); face(wa,mouth=mouth,brow=0,brow_r=0,eyes=1)
def munch(wa,cp,t,ph=0.0,rate=2.2):
    c=.5+.5*math.cos(t*rate*2*pi/2.2+ph); hold_chai(wa,cp,s=1,a=-55,sip=c*.9); face(wa,mouth='o' if c>.8 and int(t*8)%2 else 'flat')
def NOBODY():
    LF,KF,sh,gu,nt,dg=food_set(); rf=ref_mk(0,-.9,0); whistle(rf); FILLE[0]=0
    def upd(t):
        cap_idle(sh,t,-1.35,1.25,90,hp(gu)); cap_idle(gu,t,1.35,1.25,-90,hp(sh))
        for H in (sh,gu):
            H['arm'][1].rotation_euler=(R(-95+14*math.sin(t*11+H['seed'])),R(-6),0); face(H,mouth='shout' if int(t*6+H['seed'])%2 else 'O',brow=-.03,brow_r=-14); H['root'].rotation_euler[0]=R(6)
        place(rf,0,-.9,0); hstand(rf,t); hands_head(rf,1,dx=1.05,dz=4.95); face(rf,mouth='frown',brow=-.02); blink(rf,t,force=1)
        fans(LF,t,'shout',look=(3,1,2),talky=True); fans(KF,t,'shout',look=(-3,1,2),talky=True)
        q=ease(t/DUR); camset(LV((0,-13.5,8.4),(0,-12.2,7.6),q),(0,.6,1.3),20,8)
    return dict(upd=upd)
SHOTS['NOBODY']=NOBODY
def DIFFERENT():
    arena('kv_dusk',gtext=False); LF=mkfans('L'); KF=mkfans('K'); sh,gu=captains(); FILLE[0]=30
    def upd(t):
        k=tl(t,.2,1.0)
        cap_idle(sh,t,-SX,CY,SRZ); cap_idle(gu,t,SX,CY,-SRZ)
        for H in (sh,gu): look_at(H,LV(hp(gu if H is sh else sh),(0,-9,1.8),k),1.0,maxyaw=80); face(H,mouth='o' if k>.5 else 'frown',brow=.04*k)
        fans(LF,t,'freeze',look=(0,-9,1.8),k=k); fans(KF,t,'freeze',look=(0,-9,1.8),k=k)
        q=ease(t/DUR); camset(LV((0,-7.0,2.3),(0,-6.0,2.2),q),(0,1.4,2.05),24,8)
    return dict(upd=upd)
SHOTS['DIFFERENT']=DIFFERENT
def ONEBOY():
    arena('kv_dusk',gtext=False); LF=mkfans('L'); KF=mkfans('K'); sh,gu=captains(); wa=mk(WALEED,0,6.0,0,'wa'); cp=in_hand(wa,1,chips); FILLE[0]=40
    Y0=6.0
    def upd(t):
        d=min(Y0-WP[1],1.95*t); y=Y0-d
        place(wa,0,y,0); walk(wa,d,step=.5,arm=16); blink(wa,t); hold_chai(wa,cp,s=1,a=-55,sip=0); face(wa,mouth='smile'); wa['head'].rotation_euler[2]=R(14*math.sin(t*2.2))
        for H,x in ((sh,-SX),(gu,SX)): cap_idle(H,t,x,CY,SRZ if x<0 else -SRZ,hp(wa)); face(H,mouth='o',brow=.04)
        fans(LF,t,'freeze',look=hp(wa)); fans(KF,t,'freeze',look=hp(wa))
        camset((0,y-5.4,2.45),(0,y+1.0,1.85),26,8)
    return dict(upd=upd)
SHOTS['ONEBOY']=ONEBOY
def WALEEDS():
    BOARD[0]=False
    arena('kv_dusk',gtext=False); LF=mkfans('L',only=(0,5,2)); KF=mkfans('K',only=(0,5,2)); sh,gu=captains(); wa=mk(WALEED,WP[0],WP[1],0,'wa'); cp=in_hand(wa,1,chips); FILLE[0]=60
    def upd(t):
        wal_idle(wa,t); hold_chai(wa,cp,s=1,a=-55,sip=0); face(wa,mouth='smile'); look_at(wa,(0,-5,2.1),1.0)
        for H,x in ((sh,-SX),(gu,SX)): cap_idle(H,t,x,CY,SRZ if x<0 else -SRZ,hp(wa)); face(H,mouth='o',brow=.04)
        fans(LF,t,'freeze',look=hp(wa)); fans(KF,t,'freeze',look=hp(wa))
        q=ease(t/DUR); camset(LV((.35,-2.9,2.35),(.3,-2.55,2.3),q),(0,WP[1],2.05),40,8)
    return dict(upd=upd)
SHOTS['WALEED']=WALEEDS
def WON():
    arena('kv_dusk',gtext=False); LF=mkfans('L'); KF=mkfans('K'); sh,gu=captains(); wa=mk(WALEED,WP[0],WP[1],0,'wa'); cp=in_hand(wa,1,chips); FILLE[0]=40
    def upd(t):
        wal_idle(wa,t); munch(wa,cp,t); look_at(wa,(0,-6,2),1.0)
        a=tl(t,0,.6); b=tl(t,ws(129)-.1,ws(129)+.3)
        for H,x,s in ((sh,-SX,-1),(gu,SX,1)):
            cap_idle(H,t,x,CY,L(SRZ if x<0 else -SRZ,face_dir(-x,WP[1]-CY),a)); look_at(H,LV(hp(gu if H is sh else sh),hp(wa),b),1.0)
            r_=math.sin(t*9+H['seed'])*.5+.5
            for q in (1,-1): H['arm'][q].rotation_euler=(R(-62),R(q*(26+10*r_)),0)
            H['root'].rotation_euler[0]=R(9*b); face(H,mouth='smirk',brow=-.02,brow_r=-10)
        fans(LF,t,'idle',look=hp(wa)); fans(KF,t,'idle',look=hp(wa))
        q=ease(t/DUR); camset(LV((0,-5.4,2.25),(0,-4.8,2.2),q),(0,.4,1.95),26,8)
    return dict(upd=upd)
SHOTS['WON']=WON
def BHOOK():
    BOARD[0]=False
    arena('kv_dusk',gtext=False); LF=mkfans('L',only=(0,5)); KF=mkfans('K',only=(0,5)); sh,gu=captains(); wa=mk(WALEED,WP[0],WP[1],0,'wa'); cp=in_hand(wa,1,chips); FILLE[0]=60
    def upd(t):
        wal_idle(wa,t); look_at(wa,(.6,-5,2.1),1.0)
        hold_chai(wa,cp,s=1,a=-40,sip=0); r_=math.sin(t*7)*.5+.5
        arm_to(wa,-1,root_mat(wa)@Vector((-.15,-.62,2.55*wa['u']+.1*r_)),1.0,base=(0,0,0))
        sh_=tl(t,ws(135)-.1,ws(135)+.2)*(1-tl(t,ws(137),ws(138)))
        wa['root'].location[2]=wa['z0']+.008+.04*sh_; wa['head'].rotation_euler[1]=R(8*sh_)
        face(wa,mouth='smile',brow=.03*sh_); speak(wa,t,133,138,gesture=False)
        for H,x in ((sh,-SX),(gu,SX)): cap_idle(H,t,x,CY,SRZ if x<0 else -SRZ,hp(wa)); face(H,mouth='flat',brow=-.02)
        fans(LF,t,'idle',look=hp(wa)); fans(KF,t,'idle',look=hp(wa))
        c,tg,ln=single(wa,yaw=24,dist=3.0,lens=33); q=ease(t/DUR); camset(LV(c,(c[0]-.1,c[1]+.2,c[2]),q),tg,ln,8)
    return dict(upd=upd)
SHOTS['BHOOK']=BHOOK
def ROUND2():
    arena('kv_dusk',gtext=False); LF=mkfans('L',focus=(0,-2.4)); KF=mkfans('K',focus=(0,-2.4)); rf=ref_mk(0,-2.5,0); whistle(rf); bd=placard(rf,'ROUND 2','ROAST','#2466C9')
    sh,gu=captains(); wa=mk(WALEED,WP[0],WP[1],0,'wa'); cp=in_hand(wa,1,chips); FILLE[0]=40
    def upd(t):
        fans(LF,t,'fist' if t>.5 else 'idle',look=hp(rf)); fans(KF,t,'fist' if t>.5 else 'idle',look=hp(rf))
        place(rf,0,-2.5,0); hstand(rf,t); k=tl(t,0,.3); s_=.6+.4*k; bd.scale=(s_,s_,s_); bd.location=(0,-.3*rf['u'],L(5.6,7.05,k)*rf['u'])
        bpy.context.view_layer.update(); hold_board(rf,bd,1.0); face(rf,mouth='O' if t<.5 else 'flat',brow=.03)
        for H,x in ((sh,-SX),(gu,SX)): cap_idle(H,t,x,CY,SRZ if x<0 else -SRZ,hp(gu if H is sh else sh)); crossed(H); face(H,mouth='smirk',brow=-.02,brow_r=-8)
        wal_idle(wa,t); munch(wa,cp,t); look_at(wa,hp(rf),1.0)
        q=ease(t/DUR); camset(LV((-1.9,-7.4,1.6),(-1.6,-6.7,1.75),q),(0,-2.0,2.45),24,8)
    return dict(upd=upd)
SHOTS['ROUND2']=ROUND2
# ---------------------------------------------------------------- roast
def roast_set(skipL=(),skipK=(),cut=None,mood='kv_dusk'):
    arena(mood,gtext=False); LF=mkfans('L',skip=skipL); KF=mkfans('K',skip=skipK); sh,gu=captains(); wa=mk(WALEED,WP[0],WP[1],0,'wa'); cp=in_hand(wa,1,chips)
    co=None
    if cut=='L': co=cutout(-3.0,3.4,'badshahi',-28)
    if cut=='K': co=cutout(3.0,3.4,'sea',28)
    return LF,KF,sh,gu,wa,cp,co
def roast_idle(sh,gu,wa,cp,t,watch):
    cap_idle(sh,t,-SX,CY,SRZ,hp(gu)); cap_idle(gu,t,SX,CY,-SRZ,hp(sh)); wal_idle(wa,t); munch(wa,cp,t); look_at(wa,hp(watch),1.0)
def pop_cut(co,t,t0):
    k=tl(t,t0,t0+.35); b=1.0+.08*math.sin(min(1,max(0,(t-t0-.35)/.4))*pi)*(k>=1); co.location[2]=L(-5.2,0,k); co.scale=(b,b,b)
def BADSHAHI():
    LF,KF,sh,gu,wa,cp,co=roast_set(skipL=(0,5),cut='L'); FILLE[0]=45
    def upd(t):
        roast_idle(sh,gu,wa,cp,t,sh); crossed(gu); face(gu,mouth='flat',brow=-.02)
        pop_cut(co,t,ws(144)); g=tl(t,ws(145)-.2,ws(145)+.1)
        arm_to(sh,-1,(-3.0,3.6,3.8),g,base=(0,0,0)); sh['arm'][1].rotation_euler=(R(-30),R(-10),0); sh['root'].rotation_euler[0]=R(-5*g)
        look_at(sh,(-1,-5,2.2),1.0); face(sh,mouth='grin',brow=.03); speak(sh,t,143,147,gesture=False)
        fans(LF,t,'cheer' if t>ws(145) else 'idle',look=(-3.0,3.4,3.8)); fans(KF,t,'glare',look=hp(sh))
        q=ease(t/DUR); camset(LV((-.2,-5.5,2.0),(-.45,-5.0,2.1),q),(-2.4,1.6,2.75),24,8)
    return dict(upd=upd)
SHOTS['BADSHAHI']=BADSHAHI
def SAMANDAR():
    LF,KF,sh,gu,wa,cp,co=roast_set(skipK=(0,5),cut='K'); FILLE[0]=45
    def upd(t):
        roast_idle(sh,gu,wa,cp,t,gu); crossed(sh); face(sh,mouth='flat',brow=-.02)
        pop_cut(co,t,ws(148)-.05); g=tl(t,ws(150)-.2,ws(150)+.1)
        arm_to(gu,1,(3.0,3.6,3.8),g,base=(0,0,0)); gu['arm'][-1].rotation_euler=(R(-30),R(10),0)
        look_at(gu,(1,-5,2.2),1.0); face(gu,mouth='smirk',brow=.03); speak(gu,t,148,151,gesture=False)
        fans(KF,t,'cheer' if t>ws(150) else 'idle',look=(3.0,3.4,3.8)); fans(LF,t,'glare',look=hp(gu))
        q=ease(t/DUR); camset(LV((.2,-5.5,2.0),(.45,-5.0,2.1),q),(2.4,1.6,2.75),24,8)
    return dict(upd=upd)
SHOTS['SAMANDAR']=SAMANDAR
def TANKER():
    LF,KF,sh,gu,wa,cp,co=roast_set(cut='K'); co.location[2]=0; FILLE[0]=30; TK=(13.5,-5.4,2.6)
    def upd(t):
        roast_idle(sh,gu,wa,cp,t,sh)
        p=tl(t,ws(154)-.2,ws(154)+.15); arm_to(sh,1,TK,p,base=(0,0,0)); look_at(sh,LV(hp(gu),TK,p),1.0)
        face(sh,mouth='grin',brow=.03); speak(sh,t,152,159,gesture=False)
        lg=tl(t,ws(157),ws(158))
        fans(LF,t,'laugh' if lg>0 else 'idle',look=TK if p>.5 else hp(sh)); fans(KF,t,'gasp' if lg>0 else 'idle',look=TK if p>.5 else hp(sh))
        face(gu,mouth='O' if lg>0 else 'flat',brow=.05*lg); look_at(gu,LV(hp(sh),TK,lg),1.0)
        q=ease(t/DUR); camset(LV((-4.4,-4.6,2.3),(-4.0,-4.2,2.4),q),LV((4.0,-1.2,2.0),(6.0,-2.2,2.1),q),22,8)
    return dict(upd=upd)
SHOTS['TANKER']=TANKER
def CELEB():
    LF,KF,sh,gu,wa,cp,co=roast_set(); FILLE[0]=40
    def upd(t):
        roast_idle(sh,gu,wa,cp,t,sh); crossed(gu); face(gu,mouth='flat',brow=-.03,brow_r=-8)
        b=math.sin(t*7.5); place(sh,-SX,CY,SRZ+20*math.sin(t*3.7)); sh['root'].location[2]=sh['z0']+.008+.12*abs(b)
        for s in (1,-1): sh['arm'][s].rotation_euler=(R(-150+25*b*s),R(s*24),0)
        sh['leg'][1].rotation_euler[0]=R(-30*max(0,b)); sh['leg'][-1].rotation_euler[0]=R(-30*max(0,-b)); face(sh,mouth='grin',brow=.05); sh['head'].rotation_euler[1]=R(8*b)
        fans(LF,t,'dance'); fans(KF,t,'glare',look=hp(sh))
        if t>ws(162): look_at(wa,hp(gu),1.0)
        q=ease(t/DUR); camset(LV((-1.0,-6.2,2.3),(-1.4,-5.6,2.4),q),(-3.4,2.4,1.9),22,8)
    return dict(upd=upd)
SHOTS['CELEB']=CELEB
def SMOG1():
    BOARD[0]=False
    LF,KF,sh,gu,wa,cp,co=roast_set(); FILLE[0]=55
    def upd(t):
        roast_idle(sh,gu,wa,cp,t,gu); crossed(sh); face(sh,mouth='flat',brow=.02)
        k=tl(t,0,.35); place(gu,SX,CY,L(-SRZ,-14,k)); bpy.context.view_layer.update()
        m=root_mat(gu); arm_to(gu,-1,m@Vector((.22,-.5,3.15*gu['u'])),k,base=(0,0,0)); gu['arm'][1].rotation_euler=(R((-150+8*math.sin(t*4))*k),R(26*k),0)
        gu['head'].rotation_euler=(R(-8*k),0,0); blink(gu,t,force=1 if .3<t<ws(171)-.05 else None)
        face(gu,mouth='smile',brow=.06); speak(gu,t,165,172,gesture=False)
        fans(KF,t,'laugh',look=hp(gu)); fans(LF,t,'glare',look=hp(gu))
        camset(LV((SX+.35,CY-3.35,2.28),(SX+.3,CY-3.05,2.26),ease(t/DUR)),(SX,CY,hp(gu)[2]-.22),32,8)
    return dict(upd=upd)
SHOTS['SMOG1']=SMOG1
def SMOG2():
    smog_view(); FILLE[0]=0
    def upd(t):
        q=ease(t/DUR); camset(LV((-3.0,-4.0,3.0),(-2.4,4.0,3.4),q),LV((-6.0,34,3.2),(-5.5,34,3.4),q),30,8)
    return dict(upd=upd)
SHOTS['SMOG2']=SMOG2
FALLERS=(0,5,2)
def faint(H,t,t0,x,y):
    k=min(1,max(0,(t-t0)/.34)); a=-90*(k*k); bo=math.sin(min(1,max(0,(t-t0-.34)/.25))*pi)*4*(k>=1)
    place(H,x,y,90); H['root'].rotation_euler[0]=R(a+bo); H['root'].location[2]=H['z0']+.55*H['u']*math.sin(R(-a))
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-10*k),R(-s*55*k),0)
    blink(H,t,force=1 if k>.6 else 0); face(H,mouth='O',brow=.06,eyes=1.2)
def FAINT():
    arena('kv_dusk',gtext=False); LF=mkfans('L',skip=(1,4,6,7)); sh,gu=captains(); FILLE[0]=35
    T3=[.15,.4,.62]
    def upd(t):
        cap_idle(sh,t,-SX,CY,SRZ,(-4.5,3.8,1.0)); face(sh,mouth='O',brow=.06); what_pose(sh,tl(t,.1,.4),t,amp=.5)
        for H in LF:
            if H['i'] in FALLERS:
                x,y,_=H['home']; stand(H,t); faint(H,t,T3[FALLERS.index(H['i'])],x,y)
            else: fan(H,t,'gasp',look=(-4.5,3.8,.5))
        q=ease(t/DUR); camset(LV((-.6,-4.0,2.5),(-.8,-3.6,2.6),q),(-5.2,3.4,1.0),23,8)
    return dict(upd=upd)
SHOTS['FAINT']=FAINT
def TIED():
    arena('kv_dusk',gtext=False); LF=mkfans('L',focus=(0,BACKY)); KF=mkfans('K',focus=(0,BACKY)); FILLE[0]=0
    def upd(t):
        fans(LF,t,'idle',look=(0,BACKY,6)); fans(KF,t,'idle',look=(0,BACKY,6))
        k=tl(t,.75,.95); score_draw(0 if t<.75 else min(1.0,.5+k*.8) if k<1 else 1)
        q=ease(t/DUR); camset(LV((0,BACKY-11.4,6.2),(0,BACKY-10.0,6.35),q),(0,BACKY,6.4),25,8)
    return dict(upd=upd)
SHOTS['TIED']=TIED
# ---------------------------------------------------------------- the decision
def decide_set(mood='kv_dusk',skipL=(),skipK=(),cps=True):
    arena(mood,gtext=False); LF=mkfans('L',skip=skipL,focus=WP); KF=mkfans('K',skip=skipK,focus=WP); sh,gu=captains(); wa=mk(WALEED,WP[0],WP[1],0,'wa')
    return LF,KF,sh,gu,wa
def DOWN():
    LF,KF,sh,gu,wa=decide_set(); cp=in_hand(wa,1,chips); FILLE[0]=40
    def upd(t):
        wal_idle(wa,t); hold_chai(wa,cp,s=1,a=-40,sip=0); look_at(wa,(0,-6,2),1.0); face(wa,mouth='smile')
        k=ease(min(1,max(0,(t-.2)/1.4)))
        for H,p0,p1,r0,r1 in ((sh,(-SX,CY),SDP,SRZ,90),(gu,(SX,CY),GDP,-SRZ,-90)):
            x=L(p0[0],p1[0],k); y=L(p0[1],p1[1],k); cap_idle(H,t,x,y,L(r0,r1,k),hp(wa)); walk(H,1.1*k,step=.45,arm=14) if 0<k<1 else None
            face(H,mouth='smile',brow=.02)
        fans(LF,t,'idle',look=hp(wa)); fans(KF,t,'idle',look=hp(wa))
        q=ease(t/DUR); camset(LV((0,-7.2,2.6),(0,-5.6,2.3),q),(0,.0,1.95),24,8)
    return dict(upd=upd)
SHOTS['DOWN']=DOWN
def lassi_big(e,s=1.0):
    gl=M('#DCEFF6',.06,spec=1.0,alpha=.45); ls=M('#FFFDF4',.5)
    ocyl((0,-.12,.3*s),.2*s,.6*s,gl,e,rot=(0,0,0),seg=18,r2=.17*s); ocyl((0,-.12,.27*s),.18*s,.5*s,ls,e,rot=(0,0,0),seg=18,r2=.155*s)
    ocyl((0,-.12,.53*s),.183*s,.04*s,M('#F6EED8',.6),e,rot=(0,0,0),seg=18); obox((.22*s,-.12,.32*s),(.05*s,.025*s,.15*s),gl,.02,e)
    obox((-.05*s,-.12,.72*s),(.012,.012,.25*s),M('#E8554D',.5),0,e,rot=(0,R(14),0))
LASP=(-.78,-.62,1.32)
def LASSI():
    LF,KF,sh,gu,wa=decide_set(); FILLE[0]=45
    l1=in_hand(sh,1,lassi_big); l2=in_hand(wa,1,lassi_big); l2.scale=(0,0,0)
    def upd(t):
        wal_idle(wa,t,rz=-22); cap_idle(sh,t,SDP[0],SDP[1],48,hp(wa)); cap_idle(gu,t,GDP[0],GDP[1],-48,hp(wa)); crossed(gu); face(gu,mouth='frown',brow=-.02)
        tg=ws(199)+.1; a=tl(t,.15,.7); b=tl(t,tg-.25,tg); c=tl(t,tg,tg+.45)
        if t<tg:
            arm_to(sh,1,LASP,a,base=(R(-20),0,0)); upright(l1,sh,1); l1.scale=(1,1,1); l2.scale=(0,0,0)
            arm_to(wa,1,(LASP[0]+.22,LASP[1],LASP[2]-.05),b,base=(0,0,0)); face(sh,mouth='grin',brow=.03); look_at(wa,LASP,b)
        else:
            l1.scale=(0,0,0); l2.scale=(1,1,1); sh['arm'][1].rotation_euler=(R(-20*(1-c)),0,0)
            arm_to(wa,1,LV((LASP[0]+.22,LASP[1],LASP[2]-.05),(-.2,-.75,1.25),c),1.0,base=(0,0,0)); upright(l2,wa,1)
            look_at(wa,LASP,1-c); face(wa,mouth='O' if c<.6 else 'grin',brow=.05,eyes=1.12); face(sh,mouth='grin',brow=.03)
        fans(LF,t,'cheer' if t>tg else 'idle',look=hp(wa)); fans(KF,t,'glare',look=hp(sh))
        q=ease(t/DUR); camset(LV((-.45,-4.55,2.1),(-.5,-4.15,2.05),q),(-.45,-.2,1.7),25,8)
    return dict(upd=upd)
SHOTS['LASSI']=LASSI
