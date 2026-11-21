SHOTS={}
WJ=json.load(open('/home/claude/ouii/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('H_aerial',0),('H_exit',14),('E_walk',20),('E_one',29),('E_bro',39),
    ('I_doors',45),('I_sign',51),('I_wow',56),('I_relax',64),('I_staff',70),('I_welcome',75),('I_order',83),('I_just',88),('I_budget',94),
    ('T_arrive',98),('T_ice',103),('T_glow',108),('T_sip',114),('T_silence',118),('T_wait',122),('T_bsip',127),('T_yaar',133),
    ('W_out',141),('W_orbit',143),('W_boys',149),('W_what',156),('W_hungry',158),
    ('C_table',162),('C_pic',170),('C_eat',174),('C_film',177),('C_more',186),('C_sixth',193),('C_cons',197),('C_last',201),('C_owner',207),
    ('F_reach',216),('F_napkins',221),('F_chair',223),('F_dive',226),('F_staff',231),('F_guys',236),('F_freeze',241),('F_not',243),
    ('B_ask',245),('B_open',252),('B_smile',255),('B_boys',258),('B_listen',267),('B_stand',272),('B_wash',276),('B_walk',281),('B_shout',287),
    ('Z_forgot',291),('Z_tea',300),('Z_wings',301),('Z_brand',303),('Z_same',307),('Z_obv',310),('Z_logo',311)]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.1,3)) for k,i in _K]
END=round(WE[-1]+1.5,3)
def TK(key): return [t for k,t in SEQ if k==key][0]
def wl(i,key): return WS[i]-TK(key)
def we(i,key): return WE[i]-TK(key)
def talk(H,t,a,b,key,rest='smile',rate=8.0,shapes=('O','flat','o','grin','flat')):
    t0=wl(a,key); t1=we(b,key)
    if t0<=t<t1: face(H,mouth=shapes[int((t-t0)*rate+H['seed']*3)%len(shapes)])
    else: face(H,mouth=rest)
    return t0<=t<t1
def hand_w(H,s=1):
    u=H['u']; P=H['arm'][s]; return root_mat(H)@(Vector(P.location)+Euler(P.rotation_euler).to_matrix()@Vector((s*.5*u,0,-1.95*u)))
def carry(o,H,s=1,off=(0,0,0)):
    p=hand_w(H,s); o.location=(p.x+off[0],p.y+off[1],p.z+off[2])
def seat(H,x,y,rz,sh=.52,k=1.0):
    H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler=(0,0,R(rz)); H['z0']=0; sit(H,k,sh,90); H['head'].rotation_euler=(0,0,0)
def rest(H,t=0,a=-14):
    s=H['seed']; b=1.5*math.sin(t*1.3+s); arms(H,a+b,0,5,a-b,0,-5)
def breathe(H,t):
    H['root'].location[2]+=.006*math.sin(t*2.1+H['seed']); H['root'].rotation_euler[1]=R(1.0)*math.sin(t*.8+H['seed'])
def nod(H,t,amp=5,rate=5): H['head'].rotation_euler[0]+=R(amp)*math.sin(t*rate)
def flash(loc,t0,e=2500):
    p=point(loc,0,(1,1,1),.2,shadow=False)
    def fn(o,t): o.data.energy=e*max(0,1-abs(t-t0)/.07)
    fx.add(p,fn); return p
POS=dict(hm=(0,1.25,0),bi=(-1.75,0,90),sh=(1.75,0,-90))
HEAD=dict(hm=(0,1.25,1.9),bi=(-1.75,0,1.96),sh=(1.75,0,1.86))
GSEAT=[(GT[0][0]-1.35,GT[0][1],90,.52),(GT[0][0]+1.35,GT[0][1],-90,.52),(GT[1][0]-1.35,GT[1][1],90,.52),(GT[1][0]+1.35,GT[1][1],-90,.52),
       (GT[2][0]-1.35,GT[2][1],90,.52),(GT[2][0]+1.35,GT[2][1],-90,.52),(6.3,2.6,-90,.76),(4.05,2.6,90,.52),(-5.4,4.85,0,.76),(-3.2,4.85,0,.76)]
def guests():
    G=[]
    for i,(x,y,rz,sh) in enumerate(GSEAT):
        C=design(200+i*7) if i%3 else local(300+i*5,female=(i%2==0)); C['h']=min(C.get('h',1),1.0)
        H=person((x,y,0),rz,C,'smile',name='g%d'%i); H['gs']=(x,y,rz,sh); H['gi']=i; G.append(H)
    for (tx,ty) in GT:
        tea((tx-.3,ty+.1,TH),drops=False,seed=int(tx*7)%9+2); burger((tx+.3,ty-.1,TH));
    fries((5.1,2.7,TH),30); tea((5.0,2.3,TH),drops=False,seed=8); tea((-5.3,3.9,TH),drops=False,seed=6); plate_pasta((-3.2,3.85,TH))
    return G
def g_upd(G,t):
    for H in G:
        x,y,rz,sh=H['gs']; i=H['gi']; seat(H,x,y,rz,sh); blink(H,t); breathe(H,t); ph=H['seed']
        sp=math.sin(t*.9+ph*3)>0.2
        if i%2==0 and sp: face(H,mouth=('o','flat','O','smile')[int(t*7+ph)%4]); arms(H,-35-18*math.sin(t*4+ph),0,10,-20,0,-8)
        elif i%4==1: face(H,mouth='grin'); arms(H,-55,0,18,-55,0,-18); nod(H,t,4,3)
        else: face(H,mouth='smile'); arms(H,-22,0,6,-40-10*math.sin(t*2+ph),0,-10)
        H['head'].rotation_euler[2]=R(12)*math.sin(t*.6+ph)
def resto(food=0,with_guests=True,door=0.0,staff=False,wings_n=9):
    S={}; S['DR']=restaurant(door_open=door)
    S['hm']=person((0,1.25,0),0,HAMZA,'smile',name='hamza'); S['bi']=person((-1.75,0,0),90,BILAL,'smile',name='bilal'); S['sh']=person((1.75,0,0),-90,SHERRY,'smile',name='sherry')
    S['ch']={k:chair_obj(*POS[k]) for k in POS}
    S['G']=guests() if with_guests else []
    S['st2']=person((2.6,5.4,0),0,STAFF2,'smile',name='staff2')
    if staff: S['st']=person((4.6,3.4,0),0,STAFF,'smile',name='staff')
    S['nb']=napkin_box((.05,-.45,TH))
    if food==0:
        for (x,y,rz) in ((0,.35,0),(-.7,0,90),(.7,0,-90)): menu_card((x,y,TH),rz)
    if food>=1: S['tea']=tea((0,.36,TH))
    if food>=2: S['wb']=wings_bowl((0,-.02,TH),n=wings_n)
    if food>=3:
        S['fr']=fries((.62,.32,TH),20); S['bg']=burger((-.72,.3,TH)); S['na']=nachos((.72,-.3,TH)); S['pa']=plate_pasta((-.7,-.32,TH)); S['fr2']=fries((-.3,.45,TH),-30,seed=7)
        S['tea2']=tea((-.95,-.02,TH),fill=.6,drops=False,seed=4); S['tea3']=tea((.98,.02,TH),fill=.75,drops=False,seed=5)
    return S
def three(S,t,looks=None):
    for k in ('hm','bi','sh'):
        H=S[k]; seat(H,*POS[k]); blink(H,t); rest(H,t); breathe(H,t)
    if S['G']: g_upd(S['G'],t)
    s2=S['st2']; blink(s2,t); stand(s2,t); s2['root'].location[0]=2.6+.5*math.sin(t*.5); arms(s2,-50,0,10,-50,0,-10)
def lookat(S,k,target,amt=1.0): look_at(S[k],target,amt)
def cam_on(k,t,q,lens=50,dx=0,dz=0,fs=2.8,push=.25):
    h=HEAD[k]
    if k=='hm': c=(.45+dx,-2.5+push*q,2.08+dz)
    elif k=='bi': c=(1.0+dx-push*q*.5,.62,2.1+dz)
    else: c=(-1.0+dx+push*q*.5,.62,2.03+dz)
    camset(c,(h[0],h[1],h[2]+.0),lens*.82,fs,focus=h)
def cam3(q,z=2.5,y=-5.75,lens=24,fs=5.6,tz=1.62): camset((.0,y+.35*q,z),(0,.3,tz),lens,fs,focus=(0,.6,1.7))

# ============================================================ EXTERIOR
def street(night=False,aerial=False,mood='golden'):
    DR=boulevard(night=night,aerial=aerial); B.done('street'); S_,w,rp,bg=setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=170 if aerial else 70)
    if aerial: w.mist_settings.start=90; w.mist_settings.depth=330
    cars=[car(-30,-.4,'#C9302C',0),car(28,-5.2,'#F4F1EA',180),car(-55,-.4,'#2B58C9',0),car(60,-5.2,'#2B2C33',180)]
    def cu(t,sp=7.0):
        for i,c in enumerate(cars):
            d=1 if i%2==0 else -1; x0=(-30,28,-55,60)[i]; c.location[0]=x0+d*sp*t
    return DR,cu
def SH_aerial():
    DR,cu=street(aerial=True)
    crowd_=[person((x,y,0),rz,design(500+i*3),'smile',name='p%d'%i) for i,(x,y,rz) in enumerate(((-5,3.2,90),(6,4.6,-90),(-9,4.4,90),(11,3.4,-90)))]
    def upd(t):
        cu(t)
        for i,c in enumerate(crowd_): blink(c,t); walker(c,(c['x'],c['y'],0),c['rz'],1.0,t,arm=20)
        q=t/DUR; e=ease_out(q)**1.15
        p=(L(-26,0,ease(q)),L(-150,-13.5,e),L(96,4.6,e)); tg=(0,L(-60,6,ease_out(q)),L(0,4.9,ease(q)))
        camset(p,tg,L(22,26,q),8.0)
    return dict(upd=upd)
SHOTS['H_aerial']=SH_aerial
def SH_exit():
    DR,cu=street()
    A=person((0,6.6,0),0,design(611),'grin',name='exA'); Bq=person((.2,7.9,0),0,local(77,female=True),'grin',name='exB'); Cq=person((-4.5,3.4,0),90,design(640),'smile',name='exC')
    bags=[obox((0,0,0),(.2,.13,.16),M(c,.7),.02) for c in (ORANGE,'#F4E6CC',ORANGE,'#F4E6CC',ORANGE)]
    for b in bags[::2]: obox((0,-.135,.02),(.1,.004,.05),M('#FFF3E0',.5,emit=1),0,b)
    wg=empty((0,0,0)); wing(wg,(0,0,0),(0,R(90),0),1.3)
    def upd(t):
        cu(t,5); k=ease((t-.15)/.6);
        for s,e in DR: e.rotation_euler[2]=R(s*k*-80)
        for c in (A,Bq,Cq): blink(c,t)
        walk_path(A,[(0,6.9),(.2,4.6),(1.6,2.9)],t,.35,DUR+.5,step=.5,arm=0); A['root'].rotation_euler[1]=R(5)*math.sin(t*5)
        arms(A,-80,0,-14,-80,0,14); face(A,mouth='grin',brow=.05); A['head'].rotation_euler=(R(-8),R(6)*math.sin(t*4),0)
        pA=(hand_w(A,1)+hand_w(A,-1))/2
        for i,b in enumerate(bags): b.location=(pA.x+.03*math.sin(t*5+i)*i,pA.y-.02,pA.z+.2+i*.33); b.rotation_euler=(0,0,.25*i+.05*math.sin(t*5+i))
        walk_path(Bq,[(.3,8.6),(-.2,6.2),(-1.5,4.0)],t,.9,DUR+1.2,step=.5,arm=0); arms(Bq,-10,0,5,-128-8*math.sin(t*9),0,-22)
        wg.location=hand_w(Bq,-1)+Vector((0,-.05,.08)); face(Bq,mouth=('O','grin')[int(t*5)%2],brow=.05,eyes=1.15)
        stand(Cq,t); look_at(Cq,(0,5,2.2)); face(Cq,mouth='O',brow=.06); arms(Cq,-20,0,5,-20,0,-5)
        q=ease(t/DUR); camset((L(3.4,2.9,q),-2.2+.5*q,1.5),(0,5.2,L(2.6,2.3,q)),24,6.0,focus=(0,5.5,2.0))
    return dict(upd=upd)
SHOTS['H_exit']=SH_exit
def friends_out(xs=(-1.0,.15,1.2)):
    return (person((xs[0],3.3,0),180,HAMZA,'smile',name='hamza'),person((xs[1],2.9,0),180,BILAL,'smile',name='bilal'),person((xs[2],3.4,0),180,SHERRY,'smile',name='sherry'))
def SH_ewalk():
    DR,cu=street(); Hm,Bi,Sh=friends_out(); ped=[person((9,4.9,0),-90,design(700),'smile',name='pd1'),person((-16,2.9,0),90,local(41,female=True),'smile',name='pd2')]
    P={'hm':[(-10,3.9),(-3,3.9),(-1.6,3.7)],'bi':[(-11.9,5.0),(-5,5.0),(-3.5,4.9)],'sh':[(-12.1,2.9),(-5.2,2.9),(-3.7,2.9)]}
    def upd(t):
        cu(t,6)
        for k,H in (('hm',Hm),('bi',Bi),('sh',Sh)):
            blink(H,t); walk_path(H,P[k],t,-3.2,DUR+.4,step=.56,arm=24,ease_in=.05,ease_out_=.3)
        face(Hm,mouth='grin',brow=.03); Hm['head'].rotation_euler[2]=R(-25)*ease((t-.8)/.5); talk(Bi,t,20,23,'E_walk',rest='smile'); face(Sh,mouth='smile')
        look_at(Sh,(0,6,5.5),ease((t-1.2)/.6))
        for i,c in enumerate(ped): blink(c,t); walker(c,(c['x'],c['y'],0),c['rz'],1.0,t,arm=20)
        x=Hm['root'].location[0]; q=ease(t/DUR); camset((x+L(6.2,5.4,q),L(-.6,.1,q),1.5),(x-.9,3.9,1.75),26,5.6,focus=(x,3.9,1.8))
    return dict(upd=upd)
SHOTS['E_walk']=SH_ewalk
def SH_etalk(view):
    KEY='E_'+view; DR,cu=street(); Hm=person((-1.6,3.7,0),90,HAMZA,'smile',name='hamza'); Bi=person((1.0,4.75,0),-90,BILAL,'smile',name='bilal'); Sh=person((1.1,2.85,0),-90,SHERRY,'smile',name='sherry')
    Sh['root'].rotation_euler[2]=R(-150)
    def upd(t):
        cu(t,6)
        for c in (Hm,Bi,Sh): blink(c,t); stand(c,t)
        Hm['root'].rotation_euler[2]=R(90); Bi['root'].rotation_euler[2]=R(-105); Sh['root'].rotation_euler[2]=R(-75)
        look_at(Bi,(-1.6,3.7,2.0)); look_at(Sh,(-1.6,3.7,2.0),.8)
        if view=='one':
            talk(Hm,t,29,38,KEY,rest='smirk'); a=wl(33,KEY); b=wl(35,KEY); c=wl(37,KEY)
            if t<a-.15: k=ease(t/.3); arms(Hm,-35*k,0,10,-35*k,0,-10)
            elif t<b: k=ease((t-a+.15)/.18); arms(Hm,-10,0,5,L(-35,-165,k),0,-8); Hm['root'].location[2]+=.03*math.sin(min(1,(t-a+.15)/.3)*pi)
            elif t<c: k=ease((t-b)/.2); arms(Hm,L(-10,-75,k),0,L(5,-40,k),L(-165,-60,k),0,L(-8,30,k)); Hm['head'].rotation_euler[0]=R(8*k)
            else: k=ease((t-c)/.18); arms(Hm,L(-75,-45,k),0,L(-40,45*k,k),L(-60,-45,k),0,L(30,-45,k))
            look_at(Hm,(1.0,3.8,2.0),.7); face(Hm,brow=.04,brow_r=-8)
            arms(Bi,-8,0,4,-8,0,-4); face(Bi,mouth='flat',brow=-.01); arms(Sh,-8,0,4,-8,0,-4); face(Sh,mouth='smile'); nod(Sh,t,3,3)
            q=ease(t/DUR); camset((L(2.3,1.9,q),3.75,2.0),(-1.6,3.7,1.8),34,3.5,focus=(-1.6,3.7,1.95))
        else:
            talk(Bi,t,39,44,KEY,rest='flat',shapes=('o','flat','O','flat')); k=ease(t/.3)
            arms(Bi,-16*k,0,-26*k,-16*k,0,26*k); face(Bi,brow=-.02,brow_r=4,eyes=.8); Bi['head'].rotation_euler[2]+=R(-8)*math.sin(t*2.2); Bi['head'].rotation_euler[0]=R(4)
            arms(Hm,-8,0,4,-8,0,-4); face(Hm,mouth='smirk'); look_at(Hm,(1.0,4.75,2.0)); face(Sh,mouth='grin'); nod(Sh,t,7,7); arms(Sh,-8,0,4,-8,0,-4)
            q=ease(t/DUR); camset((L(-2.4,-2.1,q),L(2.6,2.8,q),2.05),(1.0,4.4,1.85),32,3.5,focus=(1.0,4.75,2.0))
    return dict(upd=upd)
for v in ('one','bro'): SHOTS['E_'+v]=(lambda v=v: SH_etalk(v))
def SH_logo():
    DR,cu=street(night=True,mood='sunset'); Hm,Bi,Sh=friends_out((-1.4,0,1.4))
    for s_ in (-1,1): point((s_*3.5,4.4,3.0),260,(1,.7,.4),.5,shadow=False)
    point((0,3.6,5.2),420,(1,.72,.4),.6,shadow=False)
    sparkles((0,5.2,5.6),3.2,0,3,n=26,size=.07,seed=4,rise=.5)
    def upd(t):
        cu(t,5)
        for i,c in enumerate((Hm,Bi,Sh)):
            blink(c,t); stand(c,t); c['root'].rotation_euler[2]=R(180); c['root'].location[1]=(3.2,2.8,3.3)[i]
            k=ease((t-.15-i*.08)/.3); arms(c,-165*k,0,14,-165*k,0,-14); c['root'].location[2]=c['z0']+.008+.16*k*abs(math.sin((t-.2)*5+i*.5)); look_at(c,(0,6,6),1)
        q=ease(t/DUR); camset((0,L(-5.2,-6.6,q),L(1.5,1.9,q)),(0,6,L(4.3,4.6,q)),L(24,22,q),8.0)
    return dict(upd=upd)
SHOTS['Z_logo']=SH_logo

# ============================================================ INTERIOR: arrival
def SH_in(view):
    KEY='I_'+view
    if view in ('doors','wow','relax'):
        S=resto(food=0); Hm,Bi,Sh=S['hm'],S['bi'],S['sh']
        if view=='doors':
            P={'hm':[(-9.2,-2.4),(-6.6,-2.4),(-4.6,-2.2)],'bi':[(-11.0,-2.0),(-8.4,-2.1),(-6.3,-1.9)],'sh':[(-12.6,-2.8),(-10.0,-2.7),(-7.9,-2.75)]}
            def upd(t):
                g_upd(S['G'],t); k=ease((t+.05)/.55); set_doors(S['DR'],k)
                for kk,H in (('hm',Hm),('bi',Bi),('sh',Sh)):
                    blink(H,t); p=walk_path(H,P[kk],t,.25,DUR+.1,step=.52,arm=20,ease_in=.1,ease_out_=.35)
                e=ease((t-1.2)/.5); face(Hm,mouth='smile' if t<1.2 else 'o',brow=.05*e,eyes=1+.2*e); face(Bi,mouth='smile' if t<1.4 else 'O',brow=.05*e); face(Sh,mouth='smile' if t<1.0 else 'O',brow=.06*e,eyes=1+.25*e)
                for H in (Hm,Bi,Sh): H['head'].rotation_euler[0]=R(-9*e)
                Sh['head'].rotation_euler[2]=R(-28*e*math.sin(t*1.6)); Bi['head'].rotation_euler[2]=R(24*e)
                q=ease(t/DUR); camset((L(-1.6,-1.0,q),L(-2.9,-3.2,q),1.85),(-6.2,-2.4,L(1.75,1.85,q)),26,4.5,focus=(-5.6,-2.4,1.8))
            return dict(upd=upd)
        SP={'hm':(-5.2,-2.0),'bi':(-6.3,-2.9),'sh':(-3.6,-2.9)}
        def base(t):
            g_upd(S['G'],t); set_doors(S['DR'],max(0,1-t/1.2) if view=='wow' else 0)
            for kk,H in (('hm',Hm),('bi',Bi),('sh',Sh)):
                H['root'].location[0],H['root'].location[1]=SP[kk]; blink(H,t); stand(H,t); arms(H,-6,0,4,-6,0,-4)
            Hm['root'].rotation_euler[2]=R(60); Bi['root'].rotation_euler[2]=R(75); Sh['root'].rotation_euler[2]=R(35)
        if view=='wow':
            def upd(t):
                base(t); talk(Sh,t,56,63,KEY,rest='O',shapes=('O','o','grin','O','flat'))
                Sh['head'].rotation_euler=(R(-10),0,R(38)*math.sin(t*1.9+.4)); k=ease(t/.4); arms(Sh,-14*k,0,-34*k,-14*k,0,34*k); face(Sh,brow=.06,eyes=1.25)
                Bi['head'].rotation_euler=(R(-12),0,R(-30)*math.sin(t*1.3)); face(Bi,mouth='O',brow=.05); face(Hm,mouth='smirk'); Hm['head'].rotation_euler=(R(-4),0,R(18)*math.sin(t*1.1))
                q=ease(t/DUR); camset((L(-.9,-1.3,q),L(-3.5,-3.3,q),L(2.0,2.1,q)),(-3.9,-2.75,1.85),L(26,30,q),3.5,focus=(-3.6,-2.9,1.9))
            return dict(upd=upd)
        def upd(t):
            base(t); Sh['root'].location[0],Sh['root'].location[1]=(-3.4,-3.55); Hm['root'].rotation_euler[2]=R(100); talk(Hm,t,64,69,KEY,rest='smirk'); k=ease(t/.3); b=math.sin(t*6)
            arms(Hm,-58*k,0,L(0,-18,k)+4*b,-58*k,0,L(0,18,k)-4*b); face(Hm,brow=-.01,brow_r=-6,eyes=.75); Hm['head'].rotation_euler=(R(3),0,R(-12))
            face(Sh,mouth='O',brow=.05); Sh['head'].rotation_euler=(R(-10),0,R(30)*math.sin(t*1.5)); face(Bi,mouth='smile'); look_at(Bi,(-5.2,-2.0,2.0))
            q=ease(t/DUR); camset((L(-2.9,-3.1,q),L(-1.7,-1.75,q),2.05),(-5.2,-2.0,1.82),28,3.0,focus=(-5.2,-2.0,1.95))
        return dict(upd=upd)
    if view=='sign':
        S=resto(food=0); sparkles((-4.3,5.6,2.9),1.6,0,2.5,n=24,size=.05,seed=9,rise=.3)
        def upd(t):
            three(S,t); q=ease_out(t/DUR); camset((L(-3.7,-4.1,q),L(.6,2.0,q),L(2.55,2.8,q)),(-4.3,5.9,L(2.6,2.9,q)),L(22,27,q),5.6,focus=(-4.3,5.9,2.8))
        return dict(upd=upd)
    S=resto(food=0,staff=True); Hm,Bi,Sh,St=S['hm'],S['bi'],S['sh'],S['st']; SPOS=(1.75,-1.75); pad=obox((0,0,0),(.1,.012,.14),M('#F4F1EA',.6),.01)
    def staff_at(t,talking=None):
        St['root'].location[0],St['root'].location[1]=SPOS; blink(St,t); stand(St,t); St['root'].rotation_euler[2]=R(heading_to(St,(0,.4)))
        arms(St,-18,0,-12,-16,0,10); pad.location=hand_w(St,1)+Vector((-.05,-.02,.1)); pad.rotation_euler=(R(-35),0,St['root'].rotation_euler[2])
    def upd(t):
        three(S,t)
        if view=='staff':
            walk_path(St,[(4.4,3.3),(3.3,.4),(1.95,-1.5),(1.75,-1.75)],t,-.9,DUR+.25,step=.54,arm=14,ease_in=.05,ease_out_=.3); blink(St,t); face(St,mouth='smile')
            arms_l=St['arm'][1].rotation_euler[0]; St['arm'][1].rotation_euler=(R(-62),0,R(-18)); pad.location=hand_w(St,1)+Vector((0,0,.1)); pad.rotation_euler=(R(-35),0,St['root'].rotation_euler[2])
            for k in ('hm','bi','sh'): look_at(S[k],(St['root'].location[0],St['root'].location[1],2.0),ease((t-.3)/.5))
            face(Hm,mouth='smirk'); face(Bi,mouth='smile'); face(Sh,mouth='grin')
            q=ease(t/DUR); camset((L(-1.0,-.6,q),-5.7,2.5),(.5,.2,1.6),24,5.6,focus=(0,.5,1.7))
        elif view=='welcome':
            staff_at(t); talk(St,t,75,82,KEY,rest='grin',shapes=('grin','O','o','grin','flat')); k=ease(t/.3); b=math.sin(t*5)
            St['arm'][-1].rotation_euler=(R(-16-12*k),0,R(10+48*k+5*b)); nod(St,t,4,5); face(St,brow=.04)
            for k_ in ('hm','bi','sh'): look_at(S[k_],(SPOS[0],SPOS[1],2.0))
            q=ease(t/DUR); camset((L(-.7,-.5,q),L(1.0,.8,q),2.15),(SPOS[0],SPOS[1],1.8),32,3.2,focus=(SPOS[0],SPOS[1],1.95))
        elif view=='order':
            staff_at(t); talk(Hm,t,83,87,KEY,rest='smirk'); k=ease(t/.25); arms(Hm,-14,0,5,L(-14,-150,k),0,-12); look_at(Hm,(SPOS[0],SPOS[1],2.0),.9); face(Hm,brow=.03,brow_r=-6)
            look_at(Bi,HEAD['hm']); look_at(Sh,HEAD['hm']); q=ease(t/DUR); cam_on('hm',t,q,48)
        elif view=='just':
            staff_at(t); talk(Bi,t,88,93,KEY,rest='O',shapes=('O','o','shout','flat','O')); look_at(Bi,HEAD['hm']); a=wl(90,KEY)
            if t<a: k=ease(t/.2); arms(Bi,-18*k,0,-40*k,-18*k,0,40*k)
            else: k=ease((t-a)/.2); arms(Bi,-18,0,L(-40,-78,k)+6*math.sin(t*12),-18,0,L(40,78,k)-6*math.sin(t*12))
            face(Bi,brow=.06,brow_r=6,eyes=1.2); Bi['root'].rotation_euler[0]=R(6); look_at(Hm,HEAD['bi'],.8); face(Hm,mouth='smirk'); look_at(Sh,HEAD['hm']); face(Sh,mouth='grin')
            q=ease(t/DUR); cam_on('bi',t,q,44)
        else:
            staff_at(t); talk(Hm,t,94,97,KEY,rest='smirk'); k=ease(t/.25); arms(Hm,-14,0,5,-118*k-6*math.sin(t*9),0,-30*k); face(Hm,brow=-.01,brow_r=-8,eyes=.55); Hm['head'].rotation_euler=(R(-6),0,R(8)); nod(Hm,t,3,6)
            look_at(Bi,HEAD['hm']); face(Bi,mouth='flat',brow=-.02); look_at(Sh,HEAD['hm']); q=ease(t/DUR); cam_on('hm',t,q,52)
    return dict(upd=upd)
for v in ('doors','sign','wow','relax','staff','welcome','order','just','budget'): SHOTS['I_'+v]=(lambda v=v: SH_in(v))

# ============================================================ THE TEA
TEA0=(0,.36,TH)
def SH_tea(view):
    KEY='T_'+view; S=resto(food=1,staff=(view=='arrive')); Hm,Bi,Sh=S['hm'],S['bi'],S['sh']; TE=S['tea']; tr=TE['root']
    for o in list(bpy.data.objects):
        pass
    if view=='arrive':
        St=S['st']; ty=tray()
        def upd(t):
            three(S,t); St['root'].location[0],St['root'].location[1]=(1.4,1.65); blink(St,t); stand(St,t); St['root'].rotation_euler[2]=R(-78); face(St,mouth='grin')
            k=ease((t-.1)/.75); tgt=(L(.9,.12,k),L(.75,.42,k),L(TH+.75,TH+.34,k)); arm_reach(St,-1,tgt); St['arm'][1].rotation_euler=(R(-75),0,R(-10)); carry(ty,St,1,(0,0,.06))
            St['root'].rotation_euler[0]=R(10*k); tr.location=(L(.9,0,k),L(.75,.36,k),L(TH+.42,TH,ease_in(k) if k<1 else 1)); tr.location[2]=L(TH+.42,TH,k)
            for kk in ('hm','bi','sh'): look_at(S[kk],(tr.location[0],tr.location[1],TH+.3));
            face(Hm,mouth='smirk'); face(Bi,mouth='flat'); face(Sh,mouth='o',brow=.04)
            q=ease(t/DUR); camset((L(-.95,-.8,q),L(-1.5,-1.35,q),TH+.5),(0,.36,TH+.3),34,2.4,focus=(tr.location[0],tr.location[1],TH+.25))
        return dict(upd=upd)
    if view in ('ice','glow'):
        drops=[]
        if view=='ice':
            for i,o in enumerate(TE['ice']): o['z1']=o.location[2]; o['x1']=o.location[0]; o['y1']=o.location[1]
            sp=[oico((0,0,0),.012,M('#FFD9B0',.05,spec=1.0,alpha=.8),sub=1) for i in range(14)]; rr=random.Random(3)
            ballistic([(o,(0+rr.uniform(-.05,.05),.36+rr.uniform(-.05,.05),TH+.46),(rr.uniform(-.7,.7),rr.uniform(-.7,.7),rr.uniform(1.2,2.4)),(3,2,1)) for o in sp[:7]],.42,floor=TH+.01,e=.2)
            ballistic([(o,(0+rr.uniform(-.05,.05),.36+rr.uniform(-.05,.05),TH+.46),(rr.uniform(-.7,.7),rr.uniform(-.7,.7),rr.uniform(1.2,2.4)),(3,2,1)) for o in sp[7:]],.78,floor=TH+.01,e=.2)
            for o in sp: o.scale=(0,0,0)
            S['sp']=sp
        else: sparkles((0,.36,TH+.45),.32,.1,DUR,n=22,size=.02,seed=5,rise=.25)
        def upd(t):
            three(S,t); look_at(Hm,(0,.36,TH+.3)); face(Hm,mouth='smirk'); look_at(Bi,(0,.36,TH+.3)); look_at(Sh,(0,.36,TH+.3)); face(Sh,mouth='o',brow=.04)
            if view=='ice':
                for i,o in enumerate(TE['ice']):
                    tt=t-.12-i*.13; o.location[2]=fall(tt,o['z1']+.85,o['z1'],g=7,e=.25) if tt>0 else o['z1']+.85; o.rotation_euler[0]=tt*5 if tt<.5 else o.rotation_euler[0]
                    o.scale=(1,1,1) if tt>-.05 else (0,0,0)
                for j,o in enumerate(S['sp']): o.scale=(1,1,1) if (t>.44 if j<7 else t>.8) and t<1.5 else (0,0,0)
                TE['liq2'].location[2]=.05+.34+.008*math.sin(t*30)*max(0,1-abs(t-.6))
                q=ease(t/DUR); camset((L(.8,.72,q),L(-.75,-.66,q),TH+L(.62,.5,q)),(0,.36,TH+.3),50,2.2,focus=(0,.36,TH+.27))
            else:
                a=R(L(-62,28,ease(t/DUR))); rr=1.3; q=ease(t/DUR)
                camset((rr*math.sin(a),.36-rr*math.cos(a),TH+L(.24,.42,q)),(0,.36,TH+.3),48,1.8,focus=(0,.36,TH+.27))
        if view=='glow': point((0,.1,TH+.9),45,(1,.62,.32),.2,shadow=False)
        return dict(upd=upd)
    MOUTH_H=(0,.86,1.78); MOUTH_B=(-1.33,0,1.84)
    def hold(H,s,tloc): arm_reach(H,s,(tloc[0]+(.0),tloc[1],tloc[2]+.2))
    def upd(t):
        three(S,t)
        if view=='sip':
            k=ease((t-.1)/.6); p=LV(TEA0,(MOUTH_H[0]+.0,MOUTH_H[1]-.12,MOUTH_H[2]-.42),k); tr.location=p; tr.rotation_euler=(R(-14*k),0,0); arm_reach(Hm,-1,(p[0]-.2,p[1]+.02,p[2]+.2)); Hm['arm'][1].rotation_euler=(R(-14),0,R(5))
            Hm['head'].rotation_euler=(R(10*k),0,0); face(Hm,mouth='o' if k>.8 else 'smirk',eyes=1-.5*ease((t-.7)/.3),brow=.0)
            look_at(Bi,HEAD['hm']); look_at(Sh,HEAD['hm']); face(Bi,mouth='flat'); face(Sh,mouth='smile')
            q=ease(t/DUR); cam_on('hm',t,q,50,dz=-.06)
        elif view=='silence':
            p=(MOUTH_H[0],MOUTH_H[1]-.12,MOUTH_H[2]-.42); k=ease((t-.25)/.5); p2=LV(p,(0,.5,TH+.02),k); tr.location=p2; tr.rotation_euler=(R(-14*(1-k)),0,0); arm_reach(Hm,-1,(p2[0]-.2,p2[1]+.02,p2[2]+.2)); Hm['arm'][1].rotation_euler=(R(-14),0,R(5))
            a=wl(119,KEY); e=ease((t-a+.1)/.45); face(Hm,mouth='flat' if t<a else 'o',eyes=L(.55,1.5,e),brow=.07*e,brow_r=-5); Hm['head'].rotation_euler=(R(L(8,-3,e)),0,0); Hm['blink_force']=0
            for o in Hm['lids']: o.scale=(0,0,0)
            look_at(Bi,HEAD['hm']); look_at(Sh,HEAD['hm'])
            q=ease(t/DUR); h=HEAD['hm']; camset((L(.3,.15,q),L(-2.0,-1.1,q),L(2.02,1.98,q)),(h[0],h[1],h[2]+.02),L(44,60,q),2.8,focus=h)
        elif view=='wait':
            a=wl(123,KEY); b=wl(124,KEY); c=wl(125,KEY); talk(Hm,t,122,122,KEY,rest='o');
            if t>=b: talk(Hm,t,124,126,KEY,rest='grin')
            talk(Sh,t,123,123,KEY,rest='smile'); face(Hm,eyes=1.35,brow=.06); Hm['blink_force']=0
            k=ease((t-c+.25)/.6); p=LV((0,.5,TH),(-.72,.08,TH),k); tr.location=p; tr.rotation_euler=(0,0,0)
            if t>c-.3: arm_reach(Hm,1,(p[0],p[1]+.02,p[2]+.3)); look_at(Hm,HEAD['bi'],ease((t-c+.2)/.3))
            else: arms(Hm,-40,0,10,-40,0,-10)
            look_at(Sh,HEAD['hm'],ease((t-a+.2)/.25)); face(Sh,brow=.03 if t>a else 0); look_at(Bi,(p[0],p[1],TH+.3) if t>c else HEAD['hm']); face(Bi,mouth='flat',brow=.02)
            q=ease(t/DUR); cam3(q)
        elif view=='bsip':
            k=ease((t-.05)/.6); p=LV((-.72,.08,TH),(MOUTH_B[0]+.14,MOUTH_B[1],MOUTH_B[2]-.42),k); tr.location=p; tr.rotation_euler=(0,R(14*k),0); arm_reach(Bi,-1,(p[0]+.02,p[1]-.2,p[2]+.2)); Bi['arm'][1].rotation_euler=(R(-14),0,R(5))
            a=wl(131,KEY); e=ease((t-a)/.3); Bi['head'].rotation_euler=(R(10*k*(1-e)),0,0); face(Bi,mouth='o' if k>.8 and t<a else ('flat' if t>=a else 'flat'),eyes=L(1-.5*ease((t-.6)/.3),1.45,e),brow=.07*e)
            if t>a: Bi['blink_force']=0
            look_at(Hm,HEAD['bi']); face(Hm,mouth='grin',brow=.04); look_at(Sh,HEAD['bi']); face(Sh,mouth='smile')
            q=ease(t/DUR); cam_on('bi',t,q,46,dz=-.05)
        else:
            p=(MOUTH_B[0]+.14,MOUTH_B[1],MOUTH_B[2]-.42); k=ease(t/.8); p2=LV(p,(-.8,.1,TH),k); tr.location=p2; tr.rotation_euler=(0,R(14*(1-k)),0); arm_reach(Bi,-1,(p2[0]+.02,p2[1]-.2,p2[2]+.2)); Bi['arm'][1].rotation_euler=(R(-14),0,R(5))
            talk(Bi,t,133,140,KEY,rest='flat',rate=6,shapes=('o','flat','o','flat')); face(Bi,eyes=1.4,brow=.06,brow_r=10); Bi['head'].rotation_euler=(R(-4),0,R(-30));
            for o in Bi['lids']: o.scale=(0,0,0)
            look_at(Hm,HEAD['bi']); face(Hm,mouth='grin'); look_at(Sh,HEAD['bi']); face(Sh,mouth='O',brow=.04)
            q=ease(t/DUR); h=HEAD['bi']; camset((L(-.1,-.45,q),L(-2.0,-1.6,q),2.04),h,L(40,50,q),2.6,focus=h)
        if view in ('silence','bsip','yaar'):
            for H in (Hm,Bi):
                if H.get('blink_force')==0:
                    for o in H['lids']: o.scale=(0,0,0)
    return dict(upd=upd)
for v in ('arrive','ice','glow','sip','silence','wait','bsip','yaar'): SHOTS['T_'+v]=(lambda v=v: SH_tea(v))

# ============================================================ THE WINGS
def SH_wings(view):
    KEY='W_'+view; S=resto(food=2,staff=(view=='out')); Hm,Bi,Sh=S['hm'],S['bi'],S['sh']; S['tea']['root'].location=(-.8,.1,TH); wb=S['wb']['root']
    if view=='out':
        St=S['st']; ty=tray(); steam((0,0,0),0,0,n=1)
        def upd(t):
            three(S,t); walk_path(St,[(4.6,3.6),(3.6,1.4),(2.3,-.9)],t,-.2,DUR+.5,step=.6,arm=0,ease_in=.05,ease_out_=.2); blink(St,t); face(St,mouth='grin',brow=.04)
            arms(St,-150,0,-12,-12,0,-4); p=hand_w(St,1); ty.location=(p.x,p.y,p.z+.03); wb.location=(p.x,p.y,p.z+.05)
            for kk in ('hm','bi','sh'): look_at(S[kk],(p.x,p.y,p.z),ease(t/.4)); face(S[kk],mouth='O',brow=.06,eyes=1.2)
            q=ease(t/DUR); camset((L(1.5,1.1,q),L(-2.6,-2.9,q),1.25),(p.x-.2,p.y,p.z-.1),28,4.0,focus=(p.x,p.y,p.z))
        return dict(upd=upd)
    if view=='orbit':
        steam((0,-.02,TH+.42),-1,DUR+1,n=16,size=.03); sparkles((0,-.02,TH+.45),.42,0,DUR,n=26,size=.022,seed=8,rise=.2); point((0,-.5,TH+.9),70,(1,.7,.4),.2,shadow=False)
        def upd(t):
            three(S,t)
            for kk in ('hm','bi','sh'): look_at(S[kk],(0,0,TH+.25)); face(S[kk],mouth='O',brow=.06,eyes=1.25); arms(S[kk],-40,0,10,-40,0,-10)
            q=t/DUR; a=R(-200+360*ease(q)*.92); rr=L(1.45,1.25,math.sin(pi*q))
            camset((rr*math.sin(a),-.02-rr*math.cos(a),TH+L(.62,.52,q)),(0,-.02,TH+.24),40,2.4,focus=(0,-.02,TH+.24))
        return dict(upd=upd)
    steam((0,-.02,TH+.42),-1,DUR+1,n=10,size=.028)
    def upd(t):
        three(S,t)
        if view=='boys':
            talk(Sh,t,149,155,KEY,rest='o',rate=7,shapes=('o','flat','O','flat')); look_at(Sh,(0,0,TH+.25)); face(Sh,eyes=1.3,brow=.05,brow_r=8); k=ease((t-wl(150,KEY))/.4); arms(Sh,-30-25*k,0,8,-30-25*k,0,-8)
            look_at(Hm,(0,0,TH+.25)); look_at(Bi,(0,0,TH+.25)); face(Hm,mouth='O'); face(Bi,mouth='o')
            q=ease(t/DUR); cam_on('sh',t,q,48)
        elif view=='what':
            talk(Hm,t,156,157,KEY,rest='flat'); look_at(Hm,HEAD['sh'],ease(t/.2)); face(Hm,brow=.05,brow_r=8); arms(Hm,-45,0,-12,-45,0,12); look_at(Sh,(0,0,TH+.25)); look_at(Bi,HEAD['sh'])
            q=ease(t/DUR); cam_on('hm',t,q,50)
        else:
            talk(Sh,t,158,161,KEY,rest='grin',shapes=('O','grin','shout','o','grin')); a=wl(161,KEY); k=ease((t-a+.1)/.2); look_at(Sh,HEAD['hm'],1-k*.4); face(Sh,eyes=1.25,brow=.06)
            arms(Sh,-40-110*k-6*math.sin(t*14)*k,0,10+12*k,-40-110*k+6*math.sin(t*14)*k,0,-10-12*k); Sh['root'].location[2]+=.05*k*abs(math.sin(t*9))
            look_at(Hm,HEAD['sh']); look_at(Bi,HEAD['sh']); face(Hm,mouth='grin'); face(Bi,mouth='grin')
            q=ease(t/DUR); cam_on('sh',t,q,L(44,50,q),dz=.03)
    return dict(upd=upd)
for v in ('out','orbit','boys','what','hungry'): SHOTS['W_'+v]=(lambda v=v: SH_wings(v))

# ============================================================ CHAOS (feast)
BOWL=(0,-.02,TH+.26)
def SH_chaos(view):
    KEY='C_'+view; last=view in ('last','owner'); S=resto(food=3,wings_n=1 if last else 9); Hm,Bi,Sh=S['hm'],S['bi'],S['sh']; S['tea']['root'].location=(.25,.5,TH); WB=S['wb']
    steam((0,-.02,TH+.42),-1,DUR+1,n=8,size=.026)
    ph_s=phone(Sh,1,'#FFD9A0') if view in ('table','pic') else None; ph_h=phone(Hm,1,'#9FD8FF') if view in ('table','film') else None
    hw=None
    if view in ('table','eat','more','cons'): hw=empty((0,0,0)); wing(hw,(0,0,0),(0,0,R(90)),1.15,2)
    if view=='pic': flash((1.0,-.2,TH+.9),.55); flash((1.0,-.2,TH+.9),1.0)
    if view=='owner': sparkles((1.5,-.1,2.9),.5,.2,DUR,n=26,size=.035,seed=6,rise=.3,mat=GOLDL); point((1.6,-.6,3.0),120,(1,.82,.4),.2,shadow=False)
    lw=WB['wings'][0] if last else None
    if lw: lw.parent=None; lw.rotation_euler=(0,0,0)
    def pic(t):
        arms(Sh,-98+4*math.sin(t*2),0,-18,-98+4*math.sin(t*2),0,26); look_at(Sh,(.3,0,TH+.4),.8); face(Sh,mouth='grin',brow=.03)
        if ph_s: ph_s.rotation_euler=(R(-75),0,0)
    def eat(t,H=None):
        H=H or Bi; c=(t*1.6+H['seed'])%1.0; k=math.sin(pi*min(1,c/.75))**.6; m=(-1.3,0,1.74); p=LV((-.9,-.05,TH+.35),m,k)
        arm_reach(H,-1,(p[0],p[1]-.16,p[2]+.02)); H['arm'][1].rotation_euler=(R(-30),0,R(8))
        if hw: hw.location=p; hw.rotation_euler=(0,0,R(90))
        face(H,mouth='O' if k>.85 else ('grin' if c>.75 else 'o'),brow=.03); H['head'].rotation_euler[0]=R(6*k)
    def film(t):
        a=R(-34+22*math.sin(t*.8)); arms(Hm,-88,0,math.degrees(a)*.6,-25,0,-8); look_at(Hm,(0,0,TH+.3),.7); face(Hm,mouth='o',brow=.03,eyes=.85)
        if ph_h: ph_h.rotation_euler=(R(-80),R(90),0)
    def upd(t):
        three(S,t)
        if view=='table':
            pic(t); eat(t); film(t); q=ease(t/DUR); camset((L(.9,-.5,q),L(-2.3,-2.6,q),L(3.25,2.9,q)),(0,.25,TH+.1),L(24,27,q),5.0,focus=(0,0,TH+.2))
        elif view=='pic':
            pic(t); look_at(Hm,HEAD['sh'],.5); face(Hm,mouth='grin'); arms(Bi,-40,0,8,-40,0,-8); q=ease(t/DUR); cam_on('sh',t,q,40,dz=.05)
        elif view=='eat':
            eat(t); q=ease(t/DUR); cam_on('bi',t,q,48)
        elif view=='film':
            film(t); eat(t,Bi) if False else arms(Bi,-45,0,8,-45,0,-8); face(Bi,mouth='grin'); face(Sh,mouth='grin')
            q=t/DUR; a=R(-35+50*ease(q)); rr=2.3; camset((rr*math.sin(a),1.0-rr*math.cos(a),L(1.75,2.05,q)),(0,.75,1.7),34,2.8,focus=(0,1.0,1.8))
        elif view=='more':
            talk(Bi,t,186,192,KEY,rest='grin'); k=ease((t-.25)/.55); p=LV((-.95,.0,TH+.5),(-.18,-.02,TH+.36),k); arm_reach(Bi,1,p); Bi['arm'][-1].rotation_euler=(R(-30),0,R(-8)); Bi['root'].rotation_euler[0]=R(10*k)
            hw.location=(p[0],p[1],p[2]-.04) if False else (0,0,-5); look_at(Bi,(0,0,TH+.3),.8); face(Bi,brow=.03); look_at(Hm,HEAD['bi'],ease((t-.6)/.3)); face(Hm,mouth='flat',brow=-.02,brow_r=10)
            look_at(Sh,HEAD['bi'],.6); face(Sh,mouth='smile'); q=ease(t/DUR); camset((L(1.3,1.1,q),L(-3.3,-3.0,q),2.35),(-.7,.1,1.6),30,3.5,focus=(-1.0,0,1.7))
        elif view=='sixth':
            talk(Hm,t,193,196,KEY,rest='shout',shapes=('shout','O','shout','o')); arm_to(Hm,-1,(-1.6,.1,1.75)); Hm['arm'][1].rotation_euler=(R(-30),0,R(6)); look_at(Hm,HEAD['bi']); face(Hm,brow=-.03,brow_r=16,eyes=1.15)
            Hm['root'].rotation_euler[0]=R(8); Hm['root'].location[2]+=.03*abs(math.sin(t*10)); look_at(Sh,HEAD['bi']); face(Sh,mouth='grin'); q=ease(t/DUR); cam_on('hm',t,q,L(44,50,q),dx=-.5)
        elif view=='cons':
            talk(Bi,t,197,200,KEY,rest='smirk'); p=(-1.0,-.5,2.08+.03*math.sin(t*3)); arm_reach(Bi,-1,(p[0],p[1]-.02,p[2]-.14)); hw.location=p; hw.rotation_euler=(0,t*1.4,R(90)); Bi['arm'][1].rotation_euler=(R(-40),0,R(-30))
            look_at(Bi,p,.9); face(Bi,brow=.04,brow_r=-10,eyes=.8); look_at(Hm,HEAD['bi']); face(Hm,mouth='flat',brow=-.03,brow_r=12); look_at(Sh,HEAD['bi']); face(Sh,mouth='grin')
            q=ease(t/DUR); cam_on('bi',t,q,50,dz=.03)
        elif view=='last':
            a=wl(203,KEY); k=ease((t-a+.1)/.5); k2=ease((t-a-.35)/.45); p0=(0.02,-.04,TH+.24); p=LV(p0,(1.15,-.05,TH+.75),k2)
            arm_reach(Sh,-1,(L(1.0,p[0],k if k2<=0 else 1),p[1]+.14 if False else p[1],L(TH+.5,p[2]+.02,k if k2<=0 else 1)) if k2<=0 else (p[0],p[1],p[2]+.02)); lw.location=p; lw.rotation_euler=(0,R(-25*k2),0)
            Sh['root'].rotation_euler[0]=R(10*k*(1-k2)); look_at(Sh,p); face(Sh,mouth='smirk' if k2<.8 else 'grin',brow=.04,brow_r=-10)
            look_at(Hm,p,ease((t-a)/.3)); look_at(Bi,p,ease((t-a-.1)/.3)); face(Hm,mouth='o',brow=.05); face(Bi,mouth='O',brow=.05)
            q=ease(t/DUR); camset((L(-.55,-.75,q),L(-1.2,-1.5,q),TH+L(.5,.75,q)),(L(0,.6,k2),0,TH+L(.25,.55,k2)),L(46,38,q),3.0,focus=p)
        else:
            talk(Sh,t,207,215,KEY,rest='grin'); p=(1.42,-.12,2.78+.02*math.sin(t*4)); arm_reach(Sh,-1,p); lw.location=(p[0],p[1],p[2]+.1); lw.rotation_euler=(0,R(-70),t*1.2); Sh['arm'][1].rotation_euler=(R(-25),0,R(-30))
            Sh['head'].rotation_euler=(R(-8),0,R(-28+8*math.sin(t*2))); face(Sh,brow=.05,brow_r=-12,eyes=.9)
            look_at(Hm,(1.42,-.12,2.8)); look_at(Bi,(1.42,-.12,2.8)); face(Hm,mouth='o',brow=-.02,brow_r=14); face(Bi,mouth='flat',brow=-.03,brow_r=16); arms(Hm,-50,0,8,-50,0,-8); arms(Bi,-50,0,8,-50,0,-8)
            q=ease(t/DUR); camset((L(-1.0,-.8,q),L(1.0,.9,q),L(2.3,2.35,q)),(1.65,-.05,L(2.3,2.38,q)),L(28,31,q),3.5,focus=(1.75,0,2.0))
    return dict(upd=upd)
for v in ('table','pic','eat','film','more','sixth','cons','last','owner'): SHOTS['C_'+v]=(lambda v=v: SH_chaos(v))

# ============================================================ THE FIGHT
WP=(.55,-.1,TH+1.25)     # where the wing is held during the fight
def fight_pose(S,t,k=1.0,slow=1.0,lw=None,dive=0.0,freeze=False):
    Hm,Bi,Sh=S['hm'],S['bi'],S['sh']; tt=t*slow; j=0 if freeze else 1
    # Sherry: leaning back, wing held high away from the others
    seat(Sh,1.75,0,-90); Sh['root'].rotation_euler[0]=R(-14*k); p=(1.9+.04*j*math.sin(tt*7),-.15,2.75+.04*j*math.sin(tt*9)); arm_reach(Sh,-1,p); Sh['arm'][1].rotation_euler=(R(-70*k),0,R(-40*k))
    if lw: lw.location=(p[0],p[1],p[2]+.1); lw.rotation_euler=(0,R(-70),0)
    face(Sh,mouth='shout',brow=.05,brow_r=10,eyes=1.2); look_at(Sh,HEAD['hm'] if not freeze else (1.75,-1.75,2.0),.9)
    # Bilal: standing, lunging over the table
    Bi['root'].location[0]=-1.45+.25*k; Bi['root'].location[1]=0; Bi['root'].rotation_euler=(R(26*k),0,R(90)); Bi['z0']=0; legs0(Bi); Bi['root'].location[2]=.008+.05*j*abs(math.sin(tt*8))
    Bi['leg'][1].rotation_euler[0]=R(-20*k); Bi['leg'][-1].rotation_euler[0]=R(24*k)
    arm_to(Bi,1,p); arm_to(Bi,-1,(p[0],p[1]+.3,p[2]-.2)); face(Bi,mouth='shout',brow=-.03,brow_r=16,eyes=1.2); look_at(Bi,p if not freeze else (1.75,-1.75,2.0),.9)
    # Hamza: half standing reaching, or diving across the table
    if dive<=0:
        Hm['root'].location[0]=0; Hm['root'].location[1]=1.25-.2*k; Hm['root'].rotation_euler=(R(30*k),0,R(-35*k)); Hm['z0']=0; legs0(Hm); Hm['root'].location[2]=.008+.05*j*abs(math.sin(tt*8+1))
        arm_to(Hm,1,p); arm_to(Hm,-1,(p[0],p[1],p[2]-.3))
    else:
        d=ease(dive); arc=math.sin(pi*min(1,dive))*.45
        Hm['root'].location=(L(0,-.5,d),L(1.9,1.7,d),L(.3,TH+.3,min(1,d*1.6))+arc*(1 if dive<1 else 0)); Hm['root'].rotation_euler=(R(L(30,84,min(1,d*1.5))),0,R(L(8,30,d))); Hm['z0']=Hm['root'].location[2]; legs0(Hm)
        Hm['leg'][1].rotation_euler[0]=R(8*math.sin(tt*10)*j); Hm['leg'][-1].rotation_euler[0]=R(-8*math.sin(tt*10)*j)
        arms(Hm,-172,0,10,-165,0,-14)
    face(Hm,mouth='shout',brow=-.03,brow_r=18,eyes=1.2)
    if dive<=0: look_at(Hm,p if not freeze else (1.75,-1.75,2.0),.9)
    else: Hm['head'].rotation_euler=(R(-55),0,R(-40) if freeze else 0)
    for H in (Hm,Bi,Sh): blink(H,t)
def SH_fight(view):
    KEY='F_'+view; S=resto(food=3,wings_n=1,staff=True); Hm,Bi,Sh,St=S['hm'],S['bi'],S['sh'],S['st']; S['tea']['root'].location=(.25,.5,TH); lw=S['wb']['wings'][0]; lw.parent=None
    ty=tray(); rr=random.Random(12); NAP=[obox((0,0,0),(.1,.1,.002),M('#FFFFFF',.8),0) for i in range(18)]
    T_N={'reach':9,'napkins':.05,'chair':-.85,'dive':-1.95,'staff':-3.6,'guys':-5.4,'freeze':-7.3,'not':-8.6}[view]
    for i,o in enumerate(NAP):
        a=rr.uniform(0,6.28); v=(1.5*math.cos(a),1.5*math.sin(a),rr.uniform(3.2,5.2)); ph=rr.uniform(0,6); p0=(.05,-.45,TH+.2)
        def fn(o,t,v=v,ph=ph,i=i,p0=p0):
            tt=t-T_N-i*.012
            if tt<=0: o.scale=(0,0,0); return
            o.scale=(1,1,1); up=v[2]*tt-.5*9.8*tt*tt; tp=v[2]/9.8
            if tt>tp: z=p0[2]+v[2]*tp-.5*9.8*tp*tp-(tt-tp)*.55-.0*tt
            else: z=p0[2]+up
            z=max(.012 if (abs(p0[0]+v[0]*min(tt,1.2)*.8)>1.15) else TH+.012,z); d=min(tt,1.4)
            o.location=(p0[0]+v[0]*d*.8+.25*math.sin(tt*2.5+ph),p0[1]+v[1]*d*.8+.2*math.cos(tt*2.1+ph),z); fl=0 if z<=TH+.02 else 1
            o.rotation_euler=(fl*math.sin(tt*5+ph)*1.2,fl*math.cos(tt*4+ph)*1.2,ph+tt)
        fx.add(o,fn)
    chB=S['ch']['bi']; chH=S['ch']['hm']
    def clear(dv):
        S['wb']['root'].location=(-.6,-.34,TH); S['tea']['root'].location=(-.15,-.48,TH); S['tea3']['root'].location=(.98,-.5,TH); S['nb'].location=(.45,-.52,TH)
        if dv>.7:
            for k_ in ('fr','na'): S[k_].scale=(0,0,0)
            S['tea3']['root'].scale=(0,0,0)
    def chairs(t,gt):
        # gt = time since the fight started ("reach"); Bilal's chair gets kicked back and spins
        k=max(0,gt-1.2); kk=1-math.exp(-k*2.2); chB.location=(-1.75-1.9*kk,0+.9*kk,0); chB.rotation_euler=(0,0,R(90)+R(760)*kk*(1 if k>0 else 0))
        k2=max(0,gt-3.2); k3=min(1,k2/.45); chH.location=(0,1.25+.7*ease_out(k3),.0); chH.rotation_euler=(R(-88)*ease(k3),0,0)
    def staff(t,talk_=None):
        St['root'].location[0],St['root'].location[1]=(1.75,-1.85); blink(St,t); stand(St,t); St['root'].rotation_euler[2]=R(-141); arms(St,-78,0,-10,-8,0,-4); carry(ty,St,1,(0,0,.04)); face(St,mouth='flat',brow=-.01,eyes=.75)
        St['head'].rotation_euler=(0,0,R(-6))
    GT0={'reach':0,'napkins':1.24,'chair':2.13,'dive':3.24,'staff':4.92,'guys':6.68,'freeze':8.56,'not':9.9}[view]
    def upd(t):
        three(S,t); gt=GT0+t; staff(t); chairs(t,gt); clear(1.25 if view in ('staff','guys','freeze','not') else (0 if view!='dive' else max(0,(t-wl(227,KEY)+.35)/.9)))
        if view=='reach':
            sl=.55; k=ease(t/.55); fight_pose(S,t,k,slow=sl,lw=lw); p=lw.location
            q=ease(t/DUR); camset((L(-.5,-.3,q),L(-3.9,-3.6,q),L(1.35,1.45,q)),(.45,.2,L(2.05,2.2,q)),L(22,24,q),4.5,focus=(.5,0,2.2))
        elif view=='napkins':
            fight_pose(S,t,1,lw=lw); q=ease(t/DUR); SHAKE[0]=.012; camset((L(-1.0,-.8,q),-4.1,L(2.0,2.2,q)),(0,.2,1.95),26,5.0,focus=(0,0,2.0))
        elif view=='chair':
            fight_pose(S,t,1,lw=lw); q=ease(t/DUR); cx=chB.location[0]; camset((L(-1.3,-1.6,q),L(-3.2,-3.0,q),.6),(cx+.2,chB.location[1],.85),24,4.0,focus=(cx,chB.location[1],.9))
        elif view=='dive':
            a=wl(227,KEY); dv=max(0,(t-a+.35)/.9); fight_pose(S,t,1,lw=lw,dive=dv); SHAKE[0]=.01 if dv>.9 else 0
            if dv>.75:
                e=ease((dv-.75)/.4); S['fr2'].location=(-.3-.5*e,.45+.6*e,TH+.5*math.sin(pi*min(1,e))); S['fr2'].rotation_euler=(3*e,2*e,0); S['bg'].location=(-.72-.8*e,.3+.3*e,TH+.4*math.sin(pi*min(1,e)))
            q=ease(t/DUR); camset((L(.3,.15,q),L(-3.7,-3.4,q),L(2.9,2.75,q)),(0,.55,1.55),24,5.0,focus=(0,.8,1.8))
        elif view in ('staff','guys'):
            fight_pose(S,t,1,lw=lw,dive=1.25,freeze=False)
            if view=='guys':
                talk(St,t,236,240,KEY,rest='flat',rate=6,shapes=('o','flat','o','flat')); k=ease((t-wl(237,KEY))/.3); St['arm'][-1].rotation_euler=(R(-8-50*k),0,R(-4-34*k)); St['head'].rotation_euler=(R(4),0,R(-6+10*math.sin(t*2.5)))
            else: St['head'].rotation_euler=(0,0,R(-6));
            if view=='staff' and t>.9: face(St,eyes=.75 if (t-.9)%1.1>.12 else .05)
            q=ease(t/DUR); camset((L(-1.0,-.8,q),L(-1.15,-1.25,q),2.15),(1.75,-1.85,1.85),L(32,36,q),2.6,focus=(1.75,-1.85,1.95))
        elif view=='freeze':
            fight_pose(S,0,1,lw=lw,dive=1.25,freeze=True)
            for H in (Hm,Bi,Sh): face(H,mouth='o',eyes=1.35,brow=.06,brow_r=0)
            q=ease(t/DUR); camset((L(.2,.1,q),L(-5.4,-5.2,q),L(2.6,2.55,q)),(.2,.2,1.75),24,6.5,focus=(0,.3,1.8))
        else:
            fight_pose(S,t,1,lw=lw,dive=1.25,freeze=False); talk(Hm,t,243,244,KEY,rest='shout',shapes=('shout','O','shout')); Hm['head'].rotation_euler=(R(-60),0,R(-20)); face(Hm,brow=-.04,brow_r=20,eyes=1.3)
            hp=Hm['head'].matrix_world.translation; q=ease_out(t/.35); SHAKE[0]=.012*(1 if t>wl(243,KEY) else 0)
            hx,hy,hz=(.5,-.02,TH+.42); camset((L(1.9,1.35,q),L(-2.3,-1.5,q),L(1.95,1.8,q)),(hx,hy,hz),L(30,40,q),3.0,focus=(hx,hy,hz))
    return dict(upd=upd)
for v in ('reach','napkins','chair','dive','staff','guys','freeze','not'): SHOTS['F_'+v]=(lambda v=v: SH_fight(v))

# ============================================================ THE BILL
def SH_bill(view):
    KEY='B_'+view; S=resto(food=3,wings_n=0,staff=(view=='ask')); Hm,Bi,Sh=S['hm'],S['bi'],S['sh']; S['tea']['root'].location=(-.75,-.4,TH); S['wb']['root'].location=(.78,-.28,TH); S['tea3']['root'].location=(.95,.35,TH)
    for k_ in ('fr','fr2','bg','na','pa'): S[k_].scale=(0,0,0)
    S['tea']['liq'].scale=(1,1,.12); S['tea']['liq'].location[2]=.07; S['tea']['liq2'].location[2]=.09
    for (x,y) in ((-.7,.3),(-.25,-.38),(.3,.42)): ocyl((x,y,TH+.015),.24,.03,M('#F4F1EA',.35),None,rot=(0,0,0),seg=22); obox((x+.05,y,TH+.035),(.09,.07,.004),M('#B8521E',.4),.003,rot=(0,0,x*3))
    rr=random.Random(5)
    for i in range(7): obox((rr.uniform(-.9,.9),rr.uniform(-.5,.5),TH+.012),(.09,.09,.01),M('#FFFFFF',.8),.004,rot=(rr.uniform(-.2,.2),rr.uniform(-.2,.2),rr.uniform(0,3)))
    BF=bill_folder((0,0,0)); br=BF['root']; rec=obox((0,0,0),(.1,.002,.5),M('#FFFFFF',.6,emit=.3),0); rec.scale=(0,0,0)
    for j in range(22): obox((-.02 if j%2 else .01,-.004,.44-j*.042),(.07,.001,.006),M('#3A3D47',.6),0,rec)
    obox((.0,-.004,-.46),(.08,.001,.016),M('#C9302C',.5,emit=.4),0,rec)
    HB=(0,.86,1.52)   # folder held in front of Hamza's chest
    def held(t,open_=1.0,roll=0.0,show=0.0):
        br.location=(HB[0],HB[1],HB[2]+.0); br.rotation_euler=(R(L(-32,8,show)),0,R(180*show)); BF['hinge'].rotation_euler=(0,0,R(-150*open_))
        arm_reach(Hm,-1,(HB[0]+.2,HB[1]+.02,HB[2])); arm_reach(Hm,1,(HB[0]-.2,HB[1]+.02,HB[2]))
        if roll>0:
            ln=L(.05,1.0,roll); rec.scale=(1,1,ln); rec.location=(HB[0],HB[1]-.03,HB[2]-.17-.5*ln); rec.rotation_euler=(R(-6),0,0)
        else: rec.scale=(0,0,0)
    def bstand(t,k):
        # Bilal rises from his chair and steps back
        seat(Bi,-1.75-.0*k,0,90,k=1-k);
    def upd(t):
        three(S,t)
        if view=='ask':
            St=S['st']; a=wl(248,KEY); talk(Hm,t,0,0,KEY,rest='smirk'); k=ease((t-.2)/.3); kd=ease((t-a-.15)/.4)
            walk_path(St,[(4.4,3.3),(3.3,.6),(1.6,1.0)],t,.5,a+.45,step=.56,arm=10,ease_in=.1,ease_out_=.3); blink(St,t); face(St,mouth='smile')
            if t<a+.2: arms(Hm,-14,0,5,L(-14,-160,k)+5*math.sin(t*9)*k,0,-10); br.location=hand_w(St,-1)+Vector((0,0,.12)); br.rotation_euler=(0,0,St['root'].rotation_euler[2]); BF['hinge'].rotation_euler=(0,0,0); St['arm'][-1].rotation_euler=(R(-70),0,0)
            else:
                e=ease((t-a-.2)/.45); p0=hand_w(St,-1)+Vector((0,0,.12)); arm_reach(St,-1,(L(1.1,.5,e),L(1.0,.95,e),1.6)); p=LV(tuple(hand_w(St,-1)+Vector((0,0,.1))),HB,e); br.location=p; br.rotation_euler=(R(-32*e),0,R(L(math.degrees(St['root'].rotation_euler[2]),0,e))); BF['hinge'].rotation_euler=(0,0,0)
                arm_reach(Hm,-1,(p[0]+.2,p[1]+.02,p[2])); arm_reach(Hm,1,(p[0]-.2,p[1]+.02,p[2]))
            face(Hm,brow=.03,brow_r=-10,eyes=.8); Hm['head'].rotation_euler=(R(-5),0,R(-14)*(1-kd)); look_at(Bi,HEAD['hm'],.6); look_at(Sh,HEAD['hm'],.6); face(Bi,mouth='grin'); face(Sh,mouth='grin')
            arms(Bi,-50,0,-30,-50,0,30); arms(Sh,-30,0,8,-30,0,-8)
            q=ease(t/DUR); camset((L(-1.0,-.7,q),L(-2.9,-2.6,q),2.2),(.4,1.1,1.8),36,3.5,focus=(0,1.25,1.85))
        elif view=='open':
            k=ease((t-.1)/.45); held(t,open_=k); Hm['head'].rotation_euler=(R(22*k),0,0); face(Hm,mouth='smirk',brow=.03,eyes=.85)
            look_at(Bi,HEAD['hm'],.6); look_at(Sh,HEAD['hm'],.6); q=ease(t/DUR); camset((L(.4,.3,q),L(-1.5,-1.2,q),L(1.95,2.0,q)),(0,1.05,1.72),36,3.0,focus=(0,.95,1.7))
        elif view=='smile':
            e=ease((t-.25)/.5); held(t,open_=1,roll=ease((t-.5)/.8)); Hm['head'].rotation_euler=(R(22-6*e),0,0)
            face(Hm,mouth='smirk' if t<.3 else ('flat' if t<.75 else 'frown'),eyes=L(.85,1.5,e),brow=.07*e,brow_r=L(-5,12,e)); Hm['blink_force']=0
            for o in Hm['lids']: o.scale=(0,0,0)
            look_at(Bi,HEAD['hm'],.6); look_at(Sh,HEAD['hm'],.6)
            q=ease(t/DUR); camset((L(.3,.15,q),L(-1.9,-1.2,q),L(1.95,1.95,q)),(0,1.15,L(1.75,1.85,q)),L(38,52,q),2.6,focus=HEAD['hm'])
        elif view=='boys':
            held(t,open_=1,roll=1); talk(Hm,t,258,258,KEY,rest='frown',shapes=('o','flat','o'));
            if t>wl(260,KEY)-.05: talk(Hm,t,260,265,KEY,rest='frown',shapes=('o','flat','O','flat'))
            talk(Bi,t,259,259,KEY,rest='smile'); talk(Sh,t,266,266,KEY,rest='smile'); e=ease((t-wl(260,KEY))/.3)
            Hm['head'].rotation_euler=(R(L(16,2,ease(t/.5))),0,R(-22*e*math.sin((t-wl(260,KEY))*1.6)) if t>wl(260,KEY) else 0); face(Hm,eyes=1.3,brow=.05,brow_r=12)
            look_at(Bi,HEAD['hm']); look_at(Sh,HEAD['hm']); arms(Bi,-40,0,8,-40,0,-8); arms(Sh,-40,0,8,-40,0,-8); face(Bi,brow=.03 if t>wl(259,KEY) else 0); face(Sh,brow=.03 if t>wl(266,KEY) else 0)
            q=ease(t/DUR); cam3(q)
        elif view=='listen':
            k=ease(t/.4); held(t,open_=1,roll=1,show=k); talk(Hm,t,267,271,KEY,rest='frown',rate=6,shapes=('o','flat','o','frown')); face(Hm,eyes=1.2,brow=.05,brow_r=16); Hm['head'].rotation_euler=(R(4),0,0); nod(Hm,t,-3,2)
            look_at(Bi,(0,.86,1.5)); look_at(Sh,(0,.86,1.5)); face(Bi,mouth='O',brow=.06,eyes=1.3); face(Sh,mouth='O',brow=.06,eyes=1.3)
            q=ease(t/DUR); cam_on('hm',t,q,L(40,46,q),dz=-.12,push=.4)
        elif view in ('stand','wash'):
            held(t,open_=1,roll=1,show=1); face(Hm,mouth='frown',eyes=1.2,brow=.04,brow_r=14); look_at(Sh,(0,.86,1.5)); face(Sh,mouth='O',brow=.06)
            if view=='stand':
                k=ease((t-.25)/1.0); seat(Bi,-1.75-.35*k,0,90,k=1-k); arms(Bi,-10,0,4,-10,0,-4); face(Bi,mouth='flat',brow=.05,brow_r=12,eyes=1.15); Bi['head'].rotation_euler=(0,0,R(20*math.sin(t*3)*(1-k)))
                look_at(Hm,(-2.0,0,2.1),ease((t-.9)/.3)*.9); S['ch']['bi'].location=(-1.75-.75*k,0,0)
                q=ease(t/DUR); camset((L(.2,.4,q),L(-2.3,-2.5,q),L(1.9,2.05,q)),(-1.85,0,L(1.8,1.95,q)),34,3.2,focus=(-1.9,0,1.9))
            else:
                seat(Bi,-2.1,0,90,k=0); S['ch']['bi'].location=(-2.5,0,0); stand(Bi,t); Bi['root'].rotation_euler[2]=R(90); talk(Bi,t,276,280,KEY,rest='grin',shapes=('grin','o','flat','grin'))
                arms(Bi,-10,0,4,-120,0,-50+8*math.sin(t*5)); face(Bi,brow=.06,brow_r=14,eyes=1.1); Bi['head'].rotation_euler=(0,0,R(-12+10*math.sin(t*4))); look_at(Hm,(-2.1,0,2.1),.9)
                q=ease(t/DUR); camset((L(-.35,-.5,q),L(-1.7,-1.5,q),2.05),(-2.1,0,2.0),44,2.8,focus=(-2.1,0,2.0))
        elif view=='walk':
            held(t,open_=1,roll=1,show=1); S['ch']['bi'].location=(-2.5,0,0); S['ch']['bi'].rotation_euler=(0,0,R(60))
            walk_path(Bi,[(-2.1,-.0),(-2.6,-1.5),(-4.2,-2.3),(-6.0,-2.4)],t,-.1,DUR+.6,step=.38,arm=8,ease_in=.1,ease_out_=.2); Bi['root'].rotation_euler[0]=R(9); arms(Bi,-28,0,-12,-28,0,12); Bi['root'].location[2]+=.03
            face(Bi,mouth='strain',brow=.05,brow_r=14); Bi['head'].rotation_euler[2]=R(40*math.sin(t*3.2)); look_at(Hm,(Bi['root'].location[0],Bi['root'].location[1],2.0)); look_at(Sh,(Bi['root'].location[0],Bi['root'].location[1],2.0)); face(Sh,mouth='O'); face(Hm,mouth='O',brow=.05)
            bx=Bi['root'].location[0]; by=Bi['root'].location[1]; q=ease(t/DUR); camset((L(-.2,-.5,q),L(-3.1,-2.9,q),L(2.3,2.2,q)),(L(-4.0,-5.6,q),-2.2,L(1.9,2.05,q)),26,5.6,focus=(bx,by,1.9))
        else:
            S['ch']['bi'].location=(-2.5,0,0); S['ch']['bi'].rotation_euler=(0,0,R(60)); Bi['root'].location[0],Bi['root'].location[1]=(-6.0,-2.4); stand(Bi,t); Bi['root'].rotation_euler[2]=R(-90); arms(Bi,-60,0,-20,-60,0,20); face(Bi,mouth='strain',brow=.06,eyes=1.3); Bi['head'].rotation_euler=(0,0,R(-80)*ease(t/.25))
            k=ease(t/.25); Hm['root'].location[0]=0; Hm['root'].location[1]=1.25; Hm['root'].rotation_euler=(R(8),0,R(-62*k)); Hm['z0']=0; sit(Hm,1-k,.52,90); S['ch']['hm'].location=(0,1.25+.5*k,0)
            talk(Hm,t,287,290,KEY,rest='shout',shapes=('shout','O','shout','o')); Hm['blink_force']=0; arm_to(Hm,-1,(-6,-2.4,2.6)); Hm['arm'][1].rotation_euler=(R(-20),0,R(20)); face(Hm,brow=-.03,brow_r=18,eyes=1.25); Hm['head'].rotation_euler=(R(-4),0,0)
            Hm['root'].location[2]+=.04*abs(math.sin(t*9)); rec.scale=(0,0,0); br.location=(.3,.5,TH+.02); br.rotation_euler=(R(90),0,R(20)); BF['hinge'].rotation_euler=(0,0,R(-170))
            look_at(Sh,(-6,-2.4,2.0)); k2=ease((t-.5)/.3); arms(Sh,-30,0,8,L(-30,-150,k2),0,L(-8,-38,k2)); face(Sh,mouth='grin',eyes=1-.9*k2)
            for o in Hm['lids']: o.scale=(0,0,0)
            q=ease(t/DUR); camset((L(-2.5,-2.2,q),L(-1.3,-1.2,q),L(1.9,2.0,q)),(.15,1.2,2.0),L(30,34,q),3.2,focus=(0,1.25,2.05))
    return dict(upd=upd)
for v in ('ask','open','smile','boys','listen','stand','wash','walk','shout'): SHOTS['B_'+v]=(lambda v=v: SH_bill(v))

# ============================================================ ENDING
def SH_end(view):
    KEY='Z_'+view
    if view=='brand':
        S=resto(food=3); sparkles((-4.3,5.6,2.6),1.8,0,2.5,n=30,size=.05,seed=9,rise=.3)
        def upd(t):
            three(S,t); q=ease(t/DUR); camset((L(-3.0,-3.4,q),L(1.3,1.9,q),L(2.3,2.45,q)),(-4.3,5.9,L(2.45,2.5,q)),L(26,29,q),5.6,focus=(-4.3,5.9,2.6))
        return dict(upd=upd)
    S=resto(food=3,wings_n=9); Hm,Bi,Sh=S['hm'],S['bi'],S['sh']; S['tea']['root'].location=(.25,.5,TH)
    if view=='tea': S['tea']['root'].location=(0,-.25,TH); sparkles((0,-.25,TH+.45),.3,0,1,n=16,size=.02,seed=5,rise=.2); point((0,-.6,TH+.8),45,(1,.62,.32),.2,shadow=False)
    if view=='wings': steam((0,-.02,TH+.42),-1,2,n=10,size=.03); sparkles((0,-.02,TH+.45),.4,0,1,n=16,size=.02,seed=8,rise=.2)
    ph=phone(Sh,-1,'#FFD9A0') if view=='forgot' else None
    if view=='forgot': flash((.6,-.9,2.2),1.5,1800)
    def upd(t):
        three(S,t)
        if view=='forgot':
            arm_reach(Sh,-1,(1.55,-.85,2.35)); ph.rotation_euler=(R(-100),0,R(180)); Sh['root'].rotation_euler[0]=R(0); Sh['head'].rotation_euler=(R(-6),0,R(-42)); face(Sh,mouth='grin',brow=.04)
            Hm['root'].rotation_euler[1]=R(-8); Hm['root'].location[0]=.25; arms(Hm,-150-6*math.sin(t*6),0,-14,-20,0,-6); face(Hm,mouth='grin',brow=.04); look_at(Hm,(1.5,-.9,2.3),.8)
            Bi['root'].rotation_euler[0]=R(12); c=(t*1.4)%1; arms(Bi,-110-10*math.sin(t*5),0,-20,-110+10*math.sin(t*5),0,20); face(Bi,mouth='grin',brow=.04); look_at(Bi,(1.5,-.9,2.3),.9)
            q=ease(t/DUR); camset((L(1.9,1.55,q),L(-2.9,-2.5,q),L(2.45,2.4,q)),(.1,.55,1.75),L(26,28,q),4.5,focus=(0,.7,1.85))
        elif view=='tea':
            q=t/DUR; a=R(-25+25*q); rr=1.25; camset((rr*math.sin(a),-.25-rr*math.cos(a),TH+.36),(0,-.25,TH+.3),46,1.8,focus=(0,-.25,TH+.27))
        elif view=='wings':
            q=t/DUR; a=R(-40+35*q); rr=1.3; camset((rr*math.sin(a),-.02-rr*math.cos(a),TH+.62),(0,-.02,TH+.26),42,2.2,focus=(0,-.02,TH+.24))
        elif view=='same':
            talk(Hm,t,307,309,KEY,rest='grin'); k=ease(t/.3); arms(Hm,-60*k,0,-25*k,-60*k,0,25*k); face(Hm,brow=.05,brow_r=-8); Hm['head'].rotation_euler=(0,0,R(22)*math.sin(t*4.5)); look_at(Bi,HEAD['hm']); look_at(Sh,HEAD['hm']); face(Bi,mouth='grin'); face(Sh,mouth='grin')
            q=ease(t/DUR); cam_on('hm',t,q,46)
        else:
            for i,H in enumerate((Hm,Bi,Sh)):
                k=ease((t-.02*i)/.2); arms(H,-165*k-8*math.sin(t*14+i),0,16,-165*k+8*math.sin(t*14+i),0,-16); face(H,mouth='shout',brow=.06,eyes=1.15); H['root'].location[2]+=.09*k*abs(math.sin(t*8+i*.4)); H['head'].rotation_euler[0]=R(-10*k)
            q=ease_out(t/DUR); SHAKE[0]=.008; cam3(q,tz=1.75)
    return dict(upd=upd)
for v in ('forgot','tea','wings','brand','same','obv'): SHOTS['Z_'+v]=(lambda v=v: SH_end(v))
