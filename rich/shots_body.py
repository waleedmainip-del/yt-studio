
# ---------------------------------------------------------------- registry for collision QC
PEOPLE=[]
_person0=person
def person(loc,rz,C,mouth='smile',name=None):
    H=_person0(loc,rz,C,mouth,name); H['nm']=name or 'p%d'%len(PEOPLE); PEOPLE.append(H); return H

# ---------------------------------------------------------------- arm poses (arm[1] is at +x; outward = -Y roll for arm[1], +Y for arm[-1])
def ARMV(H,a=150,sw=0.0): H['arm'][1].rotation_euler=(0,R(-a-sw),0); H['arm'][-1].rotation_euler=(0,R(a-sw),0)
def GEST(H,s,up=50,out=15): H['arm'][s].rotation_euler=(R(-up),0,R(out*s))
def side(H,s,a=85): H['arm'][s].rotation_euler=(0,R(-a*s),0)
FZ=.15
def stepz(y): return FZ*cl((y+.3)/.3)
def reset(H):
    H['arm'][1].rotation_euler=(0,0,0); H['arm'][-1].rotation_euler=(0,0,0); H['head'].rotation_euler=(0,0,0); H['root'].rotation_euler[0]=0; H['root'].rotation_euler[1]=0; H['root'].scale=(1,1,1)
def at(H,t,x,y,rz):
    reset(H); put_at(H,t,x,y,rz,z=stepz(y))
def wp(H,t,pts,t0,t1,arm=24):
    reset(H); blink(H,t); q=walk_path(H,pts,t,t0,t1,arm=arm); y=H['root'].location[1]; z=stepz(y); dz=H['root'].location[2]-H['z0']
    if not (0<q<1): legs0(H); dz=.008
    H['z0']=z; H['root'].location[2]=z+dz; return q
def lean(H,deg): H['root'].rotation_euler[0]=R(deg)
def pray(H,k=0.0): H['arm'][1].rotation_euler=(R(-64+k),0,R(-21)); H['arm'][-1].rotation_euler=(R(-64+k),0,R(21))
def palms(H,a=38,w=0.0): GEST(H,1,a+w,14); GEST(H,-1,a-w,14)

def lane_people(KEY,seed=300):
    A=[];Bn=[]
    for i in range(7):
        A.append((person((0,0,0),-90,local(seed+i*7,female=(i%2==1)),'smile',name='la%d'%i),-20+i*5.7+(i%2)*.9))
        Bn.append((person((0,0,0),90,local(seed+100+i*9,female=(i%3==0)),'smile',name='lb%d'%i),-18+i*5.7+(i%3)*.7))
    SP=((-6.6,-1.0,180),(5.6,-1.0,180),(7.6,-1.0,180),(-9.6,-1.0,180),(-20.5,-1.0,180),(18.5,-1.0,180))
    ST=[person((x,y,0),rz,local(seed+200+i*3,female=(i%2==0)),'smile',name='st%d'%i) for i,(x,y,rz) in enumerate(SP)]
    V=person((12.3,-1.0,0),0,local(seed+301,female=False),'smile',name='vendor'); Cu=person((12.3,-2.55,0),180,local(seed+317,female=True),'smile',name='cust')
    TG=TK(KEY)
    def upd(t,a=True,b=True,st0=True,neg=False):
        g=t+TG
        for lst,on,y,dr in ((A,a,-5.3,-1),(Bn,b,-2.8,1)):
            for H,x0 in lst:
                if not on: hideH(H); continue
                H['root'].scale=(1,1,1); x=((x0+dr*1.1*g+20)%40)-20; H['z0']=0; H['root'].location=(x,y,.008); H['root'].rotation_euler=(0,0,R(90*dr))
                walk(H,1.1*g+H['seed'],step=.55,arm=22); blink(H,g); H['head'].rotation_euler[2]=0
        for i,H in enumerate(ST):
            x,y,rz=SP[i]; reset(H); put_at(H,g,x,y,rz); gaze_idle(H,g)
            if i==0 and not st0: hideH(H)
        reset(V); put_at(V,g,12.3,-1.0,0); gaze_idle(V,g)
        if neg:
            reset(Cu); put_at(Cu,g,12.3,-2.55,180); k=math.sin(t*7); GEST(Cu,1,55+18*k,16); GEST(Cu,-1,55-18*k,16); face(Cu,mouth=('O','flat','o','grin')[int(t*8)%4],brow=.05,brow_r=10)
            hips(V); V['head'].rotation_euler[2]=R(22*math.sin(t*6)); face(V,mouth='frown',brow=-.02,brow_r=-10)
            if t>1.55: ARMV(V,125,8*math.sin(t*14)); face(V,mouth='shout',brow=.06)
        else: hideH(Cu)
    return upd

WC=(-.4,1.55); SC=(.45,3.3); BP=(1.6,-1.45); WL=(-.4,-1.45); WT=(-.4,.5)
def SH(view):
    KEY=view; P=bazaar(); setup_render('afternoon',res=PCT,samples=SAMPLES,shadow_dist=55)
    bpy.context.scene.view_settings.exposure=float(os.environ.get('EXPO','0.05'))
    for x in (-1.6,1.6): point((x,2.2,3.0),45,(1,.95,.86),.5,shadow=False)
    point((0,1.0,3.0),40,(1,.95,.86),.5); point((0,4.2,2.9),25,(1,.93,.82),.4,shadow=False)
    for x in (-20,-10,0,10,20): area((x,-3.5,5.4),380,(9,6),(1,.9,.76),shadow=False)
    W=person((0,0,0),0,WAL,'smile',name='waleed'); SK=person((0,0,0),0,SKP,'smile',name='shopkeeper'); BL=person((0,0,0),0,BLL,'smile',name='bilal')
    def _cup(e): ocyl((0,0,.02),.05,.17,M('#F4F1EA',.5),e); ocyl((0,0,.115),.053,.02,M('#E8742A',.5),e); ocyl((.02,0,.19),.008,.14,M('#C9302C',.5),e)
    prop_hand(BL,-1,_cup)
    u=SK['u']; DM=M('#8FD8FF',.08,spec=1.0,emit=.25)
    drops=[oico((sx*u,-.66*u,1.1*u),.028,DM,SK['head'],sc=(1,1,1.6)) for sx in (-.45,.38,-.12,.5)]
    lane=lane_people(KEY); s1,s2,calc,stool,bag,fan=P['s1'],P['s2'],P['calc'],P['stool'],P['bag'],P['fan']
    if view=='E_shirt': sparkles((-.4,2.5,1.28),.3,.15,3.0,n=16,size=.022,seed=5,rise=.25)
    if view=='B_exp': sparkles((-.1,-1.45,2.1),.45,.2,2.4,n=14,size=.022,seed=7,rise=.3)
    inshop=view[0] in 'DCF' or view in ('E_shirt','X_1500','X_turn','X_1000','X_leave')
    def sweat(t,on):
        for i,o in enumerate(drops):
            if not on: o.scale=(0,0,0); continue
            q=((t*.55+i*.27)%1.0); o.scale=(1,1,1.6); o.location[2]=(1.15-.8*q)*u
    def held(o,H,s,off=(0,-.06,.2),rot=(R(-90),0,R(180))):
        bpy.context.view_layer.update(); p=hand_pos(H,s); o.location=(p.x+off[0],p.y+off[1],p.z+off[2]); o.rotation_euler=rot; o.scale=(1,1,1)
    def upd(t):
        SHAKE[0]=0.0; q=ease(cl(t/DUR)); fan.rotation_euler[2]=(t+TK(KEY))*9.0
        for H in (W,SK,BL): reset(H)
        # defaults
        at(W,t,WC[0],WC[1],180); at(SK,t,SC[0],SC[1],0); at(BL,t,BP[0],BP[1],180); look_at(BL,headpos(W),.8); GEST(BL,-1,62,-8); face(BL,mouth='smile')
        look_at(SK,headpos(W),.8); look_at(W,headpos(SK),.8); face(W,mouth='smile',brow=0,brow_r=0,eyes=1.0); face(SK,mouth='smile',brow=0,brow_r=0,eyes=1.0)
        s1.location=(-.4,2.52,1.125); s1.rotation_euler=(0,0,0); s1.scale=(1,1,1); s2.scale=(0,0,0); calc.location=(1.05,2.6,1.122); calc.rotation_euler=(0,0,R(15)); calc.scale=(1,1,1)
        bag.scale=(0,0,0); stool.location=(2.2,3.6,.15); sweat(t,False); la=dict(a=True,b=True)
        v=view
        if v=='H_lane':
            hideH(W); hideH(BL); camset((L(-14,-10.5,q),-4.05,L(5.4,3.0,q)),(8,-3.6,L(3.0,2.2,q)),22,8.0)
        elif v=='H_neg':
            hideH(W); hideH(BL); la=dict(a=True,b=False,neg=True); camset((L(8.75,8.95,q),-1.78,1.7),(12.3,-1.78,1.55),20,5.0)
        elif v=='H_wal':
            hideH(BL); la=dict(a=True,b=False); x=-12+1.25*t; reset(W); W['z0']=0; W['root'].location=(x,-2.2,.008); W['root'].rotation_euler=(0,0,R(90)); walk(W,1.25*t+W['seed'],step=.58,arm=26); blink(W,t)
            k=cl((t-wl(21,KEY))/.5); face(W,mouth='smirk' if k<.5 else 'grin',brow=-.02,brow_r=10); cf(W,d=L(3.3,1.9,ease(k)),lat=.5,dz=-.45,lens=L(30,36,ease(k)))
        elif v=='E_enter':
            la=dict(a=False,b=False); wp(W,t,[(-3.6,-1.45),(-.4,-1.45),(-.4,1.55)],0,DUR-.25,arm=24); face(W,mouth='smile'); look_at(SK,headpos(W),.9)
            GEST(SK,1,25+20*cl((t-2.6)/.5),10); face(SK,mouth='grin' if t>2.6 else 'smile'); hideH(BL)
            camset((L(.5,.25,q),-6.2,L(1.75,1.6,q)),(0,0,2.55),18,8.0)
        elif v=='E_shirt':
            GEST(W,1,58*cl(t/.5),4); face(W,mouth='o',brow=.05,eyes=1.2); look_at(W,(-.4,2.5,1.1),1.0); camset((L(1.0,.85,q),L(1.75,1.85,q),1.8),(-.45,2.5,1.2),L(30,36,q),3.2,focus=(-.4,2.5,1.15))
        elif v=='D_how':
            talk(W,t,45,50,KEY,rest='smile'); GEST(W,1,56+5*math.sin(t*5),6); cf(W,d=1.75,lat=.55,lens=30)
        elif v=='D_4000':
            talk(SK,t,51,53,KEY,rest='smirk'); hips(SK); face(SK,brow=.03,brow_r=-8); cf(SK,d=L(1.85,1.65,q),lat=.6,lens=30)
        elif v=='D_stare':
            face(W,mouth='flat',brow=-.01,eyes=1.0); blink(W,t,force=0); W['head'].rotation_euler=(0,0,0); cf(W,d=L(1.75,1.5,q),lat=.42,lens=32,fs=2.8)
        elif v=='D_800':
            e1=we(61,KEY)+.2
            if t<e1: talk(W,t,60,61,KEY,rest='flat',rate=6); face(W,brow=-.01); blink(W,t,force=0); cf(W,d=1.5,lat=.5,lens=34)
            else:
                k=cl((t-e1)/.25); face(SK,mouth='O',brow=.06,eyes=1.0+.35*k); SK['head'].rotation_euler[0]=R(-4*k); cf(SK,d=L(1.7,1.35,ease(k)),lat=.55,lens=36)
        elif v=='D_shirt':
            talk(SK,t,62,65,KEY,rest='O',shapes=('shout','O','shout','grin','O')); face(SK,brow=.06,brow_r=10,eyes=1.25); kk=3*math.sin(t*16); SK['arm'][1].rotation_euler=(R(-86+kk),0,R(-20)); SK['arm'][-1].rotation_euler=(R(-86+kk),0,R(20))
            bpy.context.view_layer.update(); pa=hand_pos(SK,1); pb=hand_pos(SK,-1); s1.location=((pa.x+pb.x)/2,(pa.y+pb.y)/2-.05,(pa.z+pb.z)/2+.12); s1.rotation_euler=(R(-90),0,R(180)); cf(SK,d=2.05,lat=.5,dz=.1,lens=28)
        elif v=='D_cust':
            talk(W,t,66,73,KEY,rest='smile',rate=7); palms(W,36,4*math.sin(t*3)); face(W,brow=.03); W['head'].rotation_euler[1]=R(4*math.sin(t*2)); cf(W,d=L(1.9,1.7,q),lat=.6,lens=30)
        elif v=='C_calc':
            k=cl((t-.3)/.5); GEST(SK,1,72*k,-10); GEST(SK,-1,(50+10*math.sin(t*18))*cl((t-.9)/.3),-24); face(SK,mouth='flat',brow=-.03,brow_r=-10); look_at(SK,(.6,2.6,1.6),.8)
            if k>.5: held(calc,SK,1,off=(0,-.04,.06),rot=(R(-55),0,0))
            face(W,mouth='flat'); camset((L(2.0,1.9,q),.35,2.45),(-.1,2.8,1.5),20,6.0)
        elif v in ('C_3500','C_3000'):
            a_,b_=(79,82) if v=='C_3500' else (85,86); talk(SK,t,a_,b_,KEY,rest='flat',shapes=('O','flat','shout','grin','flat') if v=='C_3000' else ('O','flat','o','grin','flat'))
            side(SK,1,16); side(SK,-1,16 if v=='C_3500' else 55+6*math.sin(t*15)); calc.scale=(0,0,0); face(SK,brow=-.02 if v=='C_3500' else .05,brow_r=-10 if v=='C_3500' else 8,eyes=1.0 if v=='C_3500' else 1.2)
            cf(SK,d=1.95 if v=='C_3500' else 1.75,lat=.58,dz=.05,lens=30 if v=='C_3500' else 33)
        elif v=='C_900':
            talk(W,t,83,84,KEY,rest='flat',rate=6); face(W,brow=-.01); cf(W,d=1.5,lat=.5,dz=.05,lens=36)
        elif v=='C_950':
            talk(W,t,87,88,KEY,rest='smirk',rate=6); face(W,brow=.0,brow_r=8); cf(W,d=1.55,lat=.45,lens=32)
        elif v=='C_sweat':
            sweat(t,True); face(SK,mouth='strain',brow=.04,brow_r=12,eyes=1.15); SK['head'].rotation_euler[2]=R(7*math.sin(t*5)); calc.scale=(0,0,0)
            if t>we(93,KEY)+.25: side(SK,-1,14); side(SK,1,14)
            cf(SK,d=L(1.75,1.5,q),lat=.42,lens=32,fs=2.8)
        elif v=='C_please':
            sweat(t,True); talk(SK,t,94,95,KEY,rest='frown',shapes=('shout','O','shout','O')); pray(SK,5*math.sin(t*12)); face(SK,brow=.06,brow_r=16,eyes=1.2); lean(SK,3); cf(SK,d=2.15,lat=.58,dz=.25,lens=28)
        elif v=='X_leave':
            tt=.55; k=ease(cl(t/tt)); sweat(t,True)
            if t<tt: at(W,t,WC[0],WC[1],L(180,360,k))
            else: wp(W,t,[WC,WT],tt,DUR-.05,arm=22)
            face(W,mouth='flat',brow=-.01); kk=cl((t-.5)/.4); ARMV(SK,L(0,128,ease(kk)),6*math.sin(t*15)); face(SK,mouth='O',brow=.06,eyes=1.3); lean(SK,8*kk)
            camset((-1.9,-1.9,1.45),(-.15,1.6,1.72),26,5.0,focus=tuple(headpos(W)))
        elif v=='X_1500':
            at(W,t,WT[0],WT[1],0); sweat(t,True); talk(SK,t,102,104,KEY,rest='O',shapes=('shout','O','shout','grin')); lean(SK,12); GEST(SK,1,84+4*math.sin(t*13),-8); side(SK,-1,40); face(SK,brow=.06,brow_r=14,eyes=1.25)
            camset((-1.55,1.2,1.5),tuple(headpos(SK)+Vector((0,0,-.12))),28,4.5)
        elif v=='X_turn':
            t1_=wl(107,KEY); t2_=we(110,KEY); sweat(t,True); pray(SK); face(SK,mouth='frown',brow=.05,brow_r=14)
            if t<.6: wp(W,t,[(-.4,.95),WT],-.5,.6,arm=18)
            else: k=ease(cl((t-t1_)/(t2_-t1_))); at(W,t,WT[0],WT[1],L(0,180,k))
            face(W,mouth='smirk' if t>t1_ else 'flat',brow=-.01,brow_r=8)
            camset((L(-1.15,-1.0,q),L(2.15,2.0,q),1.8),tuple(headpos(W)+Vector((0,0,-.08))),L(26,30,q),4.0)
        elif v=='X_1000':
            at(W,t,WT[0],WT[1],180); sweat(t,True); talk(W,t,112,115,KEY,rest='flat',rate=6.5); GEST(W,1,70,4); face(W,brow=-.01); cf(W,d=L(1.75,1.55,q),lat=.5,lens=32)
        elif v=='F_sky':
            t1_=wl(122,KEY); sweat(t,True)
            if t<t1_: look_at(SK,(.45,2.4,4.6),1.0); face(SK,mouth='frown',brow=.06,brow_r=16); k=cl(t/.5); side(SK,1,28*k); side(SK,-1,28*k)
            else: k=ease(cl((t-t1_)/.5)); look_at(SK,(.45,2.6,.9),k); face(SK,mouth='frown',brow=-.01,brow_r=14,eyes=.75); lean(SK,5*k)
            cf(SK,d=L(1.9,1.7,q),lat=.5,dz=-.28,lens=28)
        elif v=='F_fine':
            talk(SK,t,126,131,KEY,rest='frown',shapes=('O','flat','frown','o')); face(SK,brow=-.01,brow_r=14,eyes=.85); k=ease(cl((t-wl(127,KEY))/.5)); GEST(SK,-1,66*k,-12); lean(SK,4*k)
            s1.location=(-.4,L(2.56,2.44,k),1.125); face(W,mouth='smile'); camset((L(2.0,1.9,q),.35,2.45),(-.1,2.8,1.5),20,6.0)
        elif v=='F_smile':
            k=cl(t/.35); face(W,mouth='grin' if k>.6 else 'smile',brow=.03,eyes=.92); cf(W,d=L(1.7,1.5,q),lat=.42,lens=32,fs=2.8)
        elif v=='F_two':
            talk(W,t,134,138,KEY,rest='grin',rate=7); k=ease(cl((t-wl(135,KEY))/.3)); GEST(W,1,100*k,6); face(W,brow=.04); cf(W,d=1.8,lat=.58,lens=30)
        elif v=='F_TWO':
            k=ease(cl(t/.3)); SHAKE[0]=.018*(1-cl(t/.5)); face(SK,mouth='shout',brow=.06,eyes=1.45); ARMV(SK,118*k,5*math.sin(t*20)); SK['root'].location[2]+=.06*math.sin(pi*cl(t/.3)); cf(SK,d=L(2.3,1.75,k),lat=.55,lens=L(26,32,k))
        elif v=='F_family':
            talk(W,t,140,144,KEY,rest='smile',rate=7); palms(W,34,3*math.sin(t*3)); face(W,brow=.06,brow_r=-12,eyes=1.12); W['head'].rotation_euler[1]=R(7); cf(W,d=1.65,lat=.55,lens=32)
        elif v=='B_watch':
            la=dict(a=True,b=False); t1_=wl(149,KEY); bag.scale=(1,1,1); bag.location=(-.4,2.52,1.125+.42); bag.rotation_euler=(0,0,0); s1.scale=(0,0,0)
            face(SK,mouth='frown',brow=-.01,brow_r=14,eyes=.8); GEST(SK,-1,50,-12); face(W,mouth='grin'); GEST(W,1,50,4)
            sip=cl(math.sin(t*2.2)*3); GEST(BL,-1,62+52*sip,-10); face(BL,mouth='o',brow=.06,eyes=1.25)
            if t<t1_: cf(BL,d=L(2.3,2.05,q),lat=.75,lens=30)
            else: GEST(BL,-1,30,-6); camset((.55,-3.1,1.9),(-.05,2.4,1.5),30,5.0,focus=(0,2.5,1.6))
        elif v=='B_how':
            la=dict(a=False,b=False); bag.scale=(1,1,1); tw=1.7
            if t<tw: wp(W,t,[WC,WL],-.6,tw,arm=14)
            else: k=ease(cl((t-tw)/.4)); at(W,t,WL[0],WL[1],L(0,90,k))
            k2=ease(cl((t-.9)/.6)); at(BL,t,BP[0],BP[1],L(180,270,k2)); talk(BL,t,153,160,KEY,rest='o'); GEST(BL,-1,60,-8); GEST(BL,1,22+6*math.sin(t*5),14); face(BL,brow=.06,eyes=1.2); look_at(BL,headpos(W),.9)
            face(W,mouth='smirk',brow_r=8); look_at(W,headpos(BL),.8*cl((t-1.0)/.5)); W['arm'][-1].rotation_euler=(0,0,0); held(bag,W,-1,off=(0,0,-.02),rot=(0,0,W['root'].rotation_euler[2]))
            s1.scale=(0,0,0); face(SK,mouth='frown',eyes=.8); camset((.6,-6.2,3.2),(.6,-1.45,1.0),22,8.0)
        elif v=='B_exp':
            la=dict(a=True,b=False); at(W,t,WL[0],WL[1],90); at(BL,t,BP[0],BP[1],270); GEST(BL,-1,60,-8); bag.scale=(1,1,1); held(bag,W,-1,off=(0,0,-.02),rot=(0,0,R(90))); s1.scale=(0,0,0)
            talk(W,t,161,161,KEY,rest='smirk',rate=6); face(W,brow=.02,brow_r=10,eyes=.85); W['head'].rotation_euler[1]=R(-5); cf(W,d=L(1.8,1.55,q),lat=.38,lens=32,fs=2.8)
        elif v=='B_ruined':
            la=dict(a=True,b=False); hideH(W); hideH(BL); s1.scale=(0,0,0); at(SK,t,0,.55,0); talk(SK,t,162,167,KEY,rest='shout',shapes=('shout','O','shout','grin','shout')); face(SK,brow=.06,brow_r=14,eyes=1.3)
            ARMV(SK,128,10*math.sin(t*13)); SK['root'].location[2]+=.05*abs(math.sin(t*6.5)); sweat(t,True)
            camset((L(.85,.7,q),L(-2.15,-1.9,q),1.35),tuple(headpos(SK)+Vector((0,0,-.1))),30,5.0)
        elif v in ('O_walk','O_end'):
            la=dict(a=True,b=False,st0=False); t0_=0 if v=='O_walk' else TK('O_end')-TK('O_walk'); g=t+t0_; x=-2.6-1.2*g; s1.scale=(0,0,0)
            for H,y in ((W,-1.45),(BL,-3.35)):
                reset(H); H['z0']=0; H['root'].location=(x-(0 if H is W else .5),y,.008); H['root'].rotation_euler=(0,0,R(-90)); walk(H,1.2*g+H['seed'],step=.58,arm=20 if H is W else 24); blink(H,g)
            GEST(BL,-1,62,-8); look_at(BL,headpos(W),.7); face(BL,mouth='o' if v=='O_walk' else 'smile',brow=.05); bag.scale=(1,1,1); held(bag,W,-1,off=(0,0,-.02),rot=(0,0,R(-90)))
            at(SK,t,0,.55,0); face(SK,mouth='frown'); side(SK,1,20); side(SK,-1,20)
            if v=='O_walk': face(W,mouth='smirk',brow_r=8); camset((x-5.0,-2.4,1.5),(x,-2.4,1.62),28,6.0)
            else: face(W,mouth='grin',brow=.03,eyes=.9); cf(W,d=L(2.1,1.8,q),lat=.45,dz=-.2,lens=32)
        elif v=='O_shop':
            hideH(W); hideH(BL); s1.scale=(0,0,0); stool.location=(.45,4.0,.15); reset(SK); seat(SK,t,.45,4.0,0,sh=.475,z=.15); k=ease(cl(t/1.2)); SK['head'].rotation_euler[0]=R(L(8,30,k)); face(SK,mouth='frown',brow=-.01,brow_r=14,eyes=.6)
            SK['root'].rotation_euler[0]=0; calc.location=(.45,2.6,1.122); sweat(t,True); camset((L(.3,.36,q),L(.2,.9,q),1.72),(.45,4.0,L(2.1,1.95,q)),L(22,26,q),8.0)
        if not inshop and v not in ('B_watch','O_shop','E_enter'): pass
        lane(t,**la)
    return dict(upd=upd)
for v,_ in _K: SHOTS[v]=(lambda v=v: SH(v))
