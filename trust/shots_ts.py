SHOTS={}
WJ=json.load(open('/home/claude/trust/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('I_city',0),('I_honest',10),('I_among',28),('I_lying',40),('I_welcome',49),
    ('Q_bro',52),('Q_traffic',61),('Q_sach',66),
    ('S_bhai',78),('S_kaisa',93),('S_sirf',95),('S_double',106),('S_guar',107),('S_sherry',108),('S_opp',120),('S_jeb',129),('S_dubai',137),('S_dubai2',145),('S_phone',148),
    ('P_bump',155),('P_wallet',157),('P_look',165),('P_tez',170),('P_sad',179),
    ('F_call',184),('F_kaun',194),('F_send',203),('F_days',207),('F_insta',218),('F_angry',229),('F_shop',236),('F_seekh',242),
    ('U_ruko',260),('U_rehne',267),('U_return',270),('U_sherry',276),('U_izzat',285),('U_achay',297),('U_shor',302),
    ('B_bike',314),('B_push',326),('B_paise',333),('B_allah',344),('B_narr',348),
    ('T_chai',365),('T_sherry',388),('T_lekin',400),('T_toh',414),('T_bilkul',428),
    ('M_people',441),('M_jeb',455),('M_help',463),('M_scam',481),('M_vendor',491),('M_share',504),('M_mother',520),('M_shop',531),('M_city',540),
    ('Z_dan',559)]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.1,3)) for k,i in _K]
END=round(WE[-1]+.5,3)
def TK(key): return [t for k,t in SEQ if k==key][0]
def wl(i,key): return WS[i]-TK(key)
def we(i,key): return WE[i]-TK(key)
def talk(H,t,a,b,key,rest='smile',rate=8.0,shapes=('O','flat','o','grin','flat')):
    t0=wl(a,key); t1=we(b,key)
    if t0<=t<t1: face(H,mouth=shapes[int((t-t0)*rate+H['seed']*3)%len(shapes)])
    else: face(H,mouth=rest)
    return t0<=t<t1
def handsdown(H): H['arm'][1].rotation_euler=(0,0,0); H['arm'][-1].rotation_euler=(0,0,0)
def hips(H,k=1.0): H['arm'][1].rotation_euler=(R(-15*k),R(-35*k),R(70*k)); H['arm'][-1].rotation_euler=(R(-15*k),R(35*k),R(-70*k))


END=round(WE[-1]+1.0,3)
def headpos(H):
    bpy.context.view_layer.update(); return H['head'].matrix_world.translation.copy()
def cf(H,d=2.2,lat=.35,dz=0.0,lens=30,fs=3.5,tgt_dz=-.05,extra=None):
    """camera in front of H's face (H facing direction), slight lateral offset"""
    hp_=headpos(H); a=H['root'].rotation_euler[2]; fwd=Vector((math.sin(a),-math.cos(a),0)); rt=Vector((math.cos(a),math.sin(a),0))
    pos=hp_+fwd*d+rt*lat+Vector((0,0,dz)); tg=hp_+Vector((0,0,tgt_dz))
    if extra is not None: tg=(tg+extra)/2
    camset(tuple(pos),tuple(tg),lens,fs,focus=tuple(hp_))
def two(A,Bh,d=3.0,dz=0.0,lens=26,fs=4.0,bias=.5):
    """two-shot from the front of a pair standing roughly side by side facing -y"""
    a_=headpos(A); b_=headpos(Bh); mid=a_*(1-bias)+b_*bias; a=round(math.degrees(A['root'].rotation_euler[2])/180)*math.pi
    fwd=Vector((math.sin(a),-math.cos(a),0)); p=mid+fwd*d+Vector((0,0,dz))
    camset(tuple(p),(mid.x,mid.y,mid.z-.15),lens,fs,focus=tuple(mid))
def put_at(H,t,x,y,rz,z=.0):
    H['root'].location=(x,y,z+.008); H['z0']=z; stand(H,t); H['root'].location[2]=z+.008; H['root'].rotation_euler[2]=R(rz); blink(H,t)
def mk_market(mood='morning_s',seed=41):
    market(seed); B.done('market'); setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=60)
def bgcrowd(seed,n=10,band=(-1.2,3.0),xr=(-24,24)):
    r=random.Random(seed); sp=[]
    for i in range(n): sp.append((r.uniform(*xr),r.uniform(*band),r.choice((90,-90))))
    cs=crowd(sp,seed)
    def f(t):
        for i,c in enumerate(cs):
            blink(c,t)
            if i%4!=3: walker(c,(c['x'],c['y'],0),c['rz'],.85+.1*(i%3),t,arm=16)
            else: stand(c,t); gaze_idle(c,t)
    return cs,f

# ============================================================ INTRO
def SH_I(view):
    KEY=view
    if view in ('I_city','I_welcome'):
        city(9,False,R_=170,ss=-1); B.done('city'); setup_render('morning',res=PCT,samples=SAMPLES,shadow_dist=200)
        def upd(t):
            q=ease(t/DUR)
            if view=='I_city': camset((L(-50,-20,q),L(-200,-160,q),L(75,60,q)),(0,L(-90,-60,q),0),24,8.0)
            else: camset((L(20,0,q),L(-70,-100,q),L(55,85,q)),(0,-20,0),22,8.0)
        return dict(upd=upd)
    mk_market('dawn' if view=='I_honest' else 'dusk',seed=43)
    if view=='I_honest':
        V=person((0,0,0),180,local(201),'smile',name='v'); L1=person((0,0,0),90,dict(local(202),top='#D8C8A0',pants='#7A6A5A'),'flat',name='l1')
        bucket_=empty((0,0,0)); obox((0,0,.12),(.22,.11,.12),M('#A8513A',.85,kind='concrete',sc=.5),.005,bucket_)
        def upd(t):
            put_at(V,t,-1.0,2.6,180); V['arm'][1].rotation_euler=(R(-80+20*math.sin(t*3)),0,R(10)); V['arm'][-1].rotation_euler=(R(-80+20*math.sin(t*3+1)),0,R(-10)); face(V,mouth='smile')
            x=-4+1.0*t; L1['root'].location=(x,-.8,.008); L1['rotation']=0; L1['root'].rotation_euler[2]=R(90); walk(L1,x,step=.45,arm=0); blink(L1,t); arms(L1,-170,0,10,-170,0,-10)
            bucket_.location=headpos(L1)+Vector((0,0,.32)); face(L1,mouth='flat',brow=-.03)
            q=ease(t/DUR); camset((L(1.5,2.2,q),-4.2,1.6),(-1.2,.8,1.5),24,6.0)
        return dict(upd=upd)
    S_=person((0,0,0),0,SCAM,'smirk',name='scam'); T_=person((0,0,0),0,THIEF,'smirk',name='thief')
    cash=empty((0,0,0))
    for k in range(5): obox((0,0,.006*k),(.08,.04,.003),M('#5FA84A',.6),0,cash)
    cs,bg=bgcrowd(301,12)
    def upd(t):
        bg(t)
        if view=='I_among':
            put_at(S_,t,0,-1.4,0); hideH(T_); S_['arm'][1].rotation_euler=(R(-40),0,R(-35)); S_['arm'][-1].rotation_euler=(R(-15),0,R(10)); cash.location=hand_pos(S_,1)+Vector((0,-.05,.05))
            cash.rotation_euler=(0,0,R(20*math.sin(t*6))); face(S_,mouth='smirk',brow=-.03,brow_r=-14); S_['head'].rotation_euler[0]=R(15)
            q=ease(t/DUR); cf(S_,d=L(2.6,1.7,q),lat=.3,dz=-.1,lens=30)
        else:
            cash.scale=(0,0,0); put_at(S_,t,-1.2,-1.2,15); put_at(T_,t,1.0,-1.6,-15)
            face(S_,mouth='grin' if t%1.4<.7 else 'smirk',brow=-.02); face(T_,mouth='smirk',brow=-.04,brow_r=12); T_['head'].rotation_euler[2]=R(25*math.sin(t*2))
            S_['arm'][1].rotation_euler=(R(-140),0,R(-20)) if t<1.4 else (R(-30),0,0)
            q=ease(t/DUR); camset((L(-.6,.4,q),-5.0,1.5),(0,-1.4,1.8),24,5.0)
    return dict(upd=upd)
for v in ('I_city','I_honest','I_among','I_lying','I_welcome'): SHOTS[v]=(lambda v=v: SH_I(v))

# ============================================================ MARKET: question, scammer, pickpocket
def SH_S(view):
    KEY=view; mk_market('morning_s',seed=41)
    D=person((0,0,0),0,DAN,'smile',name='dan'); S=person((0,0,0),0,SHER,'smile',name='sher'); SC=person((0,0,0),0,SCAM,'grin',name='scam'); TH=person((0,0,0),0,THIEF,'flat',name='thief')
    ph=phone(SC,-1,'#7FD3FF'); ph.scale=(0,0,0); wal=empty((0,0,0)); obox((0,0,0),(.06,.012,.05),M('#5A3A22',.6),.008,wal); wal.scale=(0,0,0)
    cs,bg=bgcrowd(311,14)
    def upd(t):
        bg(t); hideH(TH)
        if view in ('Q_bro','Q_traffic','Q_sach'):
            hideH(SC); x=-3+.9*t if view=='Q_bro' else -1.0
            for H,dx,rz in ((D,0,-15),(S,1.0,15)):
                H['root'].location=(x+dx,-1.6,.008); H['root'].rotation_euler[2]=R(rz); blink(H,t)
                if view=='Q_bro': walk(H,x+dx,step=.55,arm=16)
                else: stand(H,t)
            if view=='Q_bro':
                D['root'].rotation_euler[2]=R(70); S['root'].rotation_euler[2]=R(70); talk(D,t,52,60,KEY,rest='smile'); look_at(D,headpos(S),.6); look_at(S,headpos(D),.5)
                camset((x+3.2,-3.8,1.6),(x+.6,-1.6,1.85),26,5.0)
            elif view=='Q_traffic':
                talk(S,t,61,61,KEY,rest='o'); talk(D,t,62,62,KEY,rest='flat') if t>wl(62,KEY)-.05 else None; talk(S,t,63,63,KEY,rest='o') if t>wl(63,KEY)-.05 else None
                talk(D,t,64,64,KEY,rest='flat') if t>wl(64,KEY)-.05 else None; talk(S,t,65,65,KEY,rest='o') if t>wl(65,KEY)-.05 else None
                S['arm'][1].rotation_euler=(R(-60),0,R(-20)); look_at(S,headpos(D),.5); look_at(D,headpos(S),.3); two(D,S,d=2.8,lens=26)
            else:
                talk(D,t,66,77,KEY,rest='flat'); face(D,brow=.02,brow_r=10); D['arm'][1].rotation_euler=(R(-30),0,R(-45+10*math.sin(t*3)))
                cf(D,d=1.9,lat=-.25,lens=30)
            return
        if view in ('P_bump','P_wallet','P_look','P_tez','P_sad'):
            hideH(SC)
            if view=='P_bump':
                put_at(D,t,0,-1.6,-10); put_at(S,t,1.1,-1.4,10); face(S,mouth='smile')
                tx=L(-1.6,1.6,min(1,t/DUR)); TH['root'].scale=(1,1,1); TH['root'].location=(tx,-2.05,.008); TH['root'].rotation_euler[2]=R(90); walk(TH,tx,step=.6,arm=18); blink(TH,t)
                hit=math.exp(-((tx-0)/.4)**2); D['root'].rotation_euler[1]=R(8*hit); D['root'].location[1]=-1.6+.12*hit
                talk(TH,t,155,156,KEY,rest='flat'); TH['arm'][-1].rotation_euler=(R(-40*hit),0,R(20*hit)); wal.scale=(1,1,1) if tx>0 else (0,0,0); wal.location=hand_pos(TH,-1)
                face(D,mouth='o' if hit>.3 else 'smile'); camset((-.2,-5.0,1.4),(.2,-1.8,1.5),24,4.0)
            else:
                put_at(D,t,0,-1.6,-10); put_at(S,t,1.1,-1.4,10)
                if view=='P_wallet':
                    k=ease(t/.3); D['arm'][1].rotation_euler=(R(-15),R(0),R(30*k)); talk(D,t,157,159,KEY,rest='O',shapes=('shout','O')); talk(S,t,160,161,KEY,rest='o') if t>wl(160,KEY)-.05 else None
                    talk(D,t,162,164,KEY,rest='O',shapes=('shout','O')) if t>wl(162,KEY)-.05 else None; face(D,brow=.12,eyes=1.2); shock(D,.4) if t>wl(162,KEY) else None
                    look_at(S,headpos(D),.6); two(D,S,d=2.8,lens=26)
                elif view=='P_look':
                    for H,ph_ in ((D,0),(S,1.3)): H['root'].rotation_euler[2]=R(-60*math.sin(t*2.2+ph_)); face(H,mouth='O',brow=.08)
                    talk(D,t,165,169,KEY,rest='frown'); q=ease(t/DUR); camset((L(.5,.5,q),-3.8,L(3.2,2.4,q)),(.5,-1.5,1.4),22,5.0)
                elif view=='P_tez':
                    talk(S,t,170,178,KEY,rest='smirk'); look_at(S,headpos(D),.4); S['arm'][1].rotation_euler=(R(-75),0,R(-30)); face(S,brow=.02,brow_r=-10); cf(S,d=1.9,lat=-.3,lens=30)
                else:
                    talk(D,t,179,183,KEY,rest='frown',rate=5); D['head'].rotation_euler[0]=R(14); face(D,brow=.06,brow_r=-16,eyes=.8); D['root'].rotation_euler[2]=R(-5); cf(D,d=1.7,lat=.25,dz=-.15,lens=32)
            return
        # scammer scene: D at (0,-1.6) facing slightly right, SC at (1.1,-1.5) facing slightly left; S joins from right
        put_at(D,t,0,-1.6,-20); put_at(SC,t,1.05,-1.5,25); S_in=view not in ('S_bhai','S_kaisa','S_sirf','S_double','S_guar')
        if S_in: put_at(S,t,-1.05,-1.5,-30)
        else: hideH(S)
        if view=='S_bhai':
            k=ease(t/1.0); SC['root'].location=(L(4,1.05,k),-1.5,.008); SC['root'].rotation_euler[2]=R(L(-90,25,k)); walk(SC,SC['root'].location.x,step=.55,arm=16) if t<1.0 else None
            talk(SC,t,78,92,KEY,rest='grin'); SC['arm'][1].rotation_euler=(R(-110),0,R(-20+15*math.sin(t*5))); look_at(D,headpos(SC),.6); face(SC,brow=.06)
            two(D,SC,d=3.0,lens=26)
        elif view=='S_kaisa': talk(D,t,93,94,KEY,rest='o'); look_at(D,headpos(SC),.6); cf(D,d=1.9,lat=.3,lens=30)
        elif view=='S_sirf':
            talk(SC,t,95,105,KEY,rest='grin'); SC['arm'][1].rotation_euler=(R(-30),0,R(-55)); SC['arm'][-1].rotation_euler=(R(-30+15*math.sin(t*4)),0,R(55)); look_at(SC,headpos(D),.5); face(SC,brow=.08)
            cf(SC,d=2.0,lat=-.3,lens=30)
        elif view=='S_double': talk(D,t,106,106,KEY,rest='O'); face(D,eyes=1.3,brow=.13); look_at(D,headpos(SC),.6); cf(D,d=1.4,lat=.15,lens=34)
        elif view=='S_guar':
            talk(SC,t,107,107,KEY,rest='grin'); SC['arm'][1].rotation_euler=(R(-35),0,R(-70)); face(SC,brow=.1); cf(SC,d=1.6,lat=-.2,lens=32)
        elif view=='S_sherry':
            k=ease(t/.9); S['root'].location=(L(-3.5,-1.05,k),-1.5,.008); S['root'].rotation_euler[2]=R(L(90,-30,k)); walk(S,S['root'].location.x,step=.55) if t<.9 else None
            talk(S,t,108,119,KEY,rest='smirk'); S['arm'][1].rotation_euler=(R(-70),0,R(30)) if t>1.0 else (0,0,0); look_at(S,headpos(SC),.6); look_at(D,headpos(S),.5)
            camset((0,-4.6,1.75),(0,-1.5,1.85),24,4.5)
        elif view=='S_opp': talk(SC,t,120,128,KEY,rest='grin',rate=6); SC['arm'][-1].rotation_euler=(R(-70),R(35),R(-70)); face(SC,brow=.04,brow_r=-8); look_at(SC,headpos(S),.5); cf(SC,d=2.0,lat=-.3,lens=30)
        elif view=='S_jeb': talk(S,t,129,136,KEY,rest='smirk'); hips(S); face(S,brow=-.02,brow_r=12); look_at(S,headpos(SC),.6); cf(S,d=2.0,lat=.3,lens=30)
        elif view=='S_dubai':
            ph.scale=(1,1,1); k=ease((t-1.0)/1.0)
            SC['arm'][-1].rotation_euler=(R(-130),0,R(30)); ph.location=headpos(SC)+Vector((-.25,-.05,-.05)); talk(SC,t,137,144,KEY,rest='grin',rate=8)
            SC['root'].location=(1.05+5*k,-1.5,.008); SC['root'].rotation_euler[2]=R(L(25,-90,min(1,k*3))); walk(SC,SC['root'].location.x,step=.6,arm=10) if k>0 else None
            for H in (D,S): look_at(H,headpos(SC),.7); face(H,mouth='o')
            q=ease(t/DUR); camset((L(0,1.0,q),-4.6,1.7),(L(.5,2.5,q),-1.5,1.85),24,4.5)
        elif view=='S_dubai2': hideH(SC); talk(D,t,145,147,KEY,rest='o'); D['root'].rotation_euler[2]=R(30); face(D,brow=.08); D['head'].rotation_euler[1]=R(10); cf(D,d=1.8,lat=.3,lens=30)
        else: hideH(SC); talk(S,t,148,154,KEY,rest='smirk'); S['root'].rotation_euler[2]=R(-10); face(S,brow=-.02,brow_r=-10); cf(S,d=1.8,lat=-.3,lens=30)
    return dict(upd=upd)
for v in ('Q_bro','Q_traffic','Q_sach','S_bhai','S_kaisa','S_sirf','S_double','S_guar','S_sherry','S_opp','S_jeb','S_dubai','S_dubai2','S_phone','P_bump','P_wallet','P_look','P_tez','P_sad'): SHOTS[v]=(lambda v=v: SH_S(v))

# ============================================================ FAKE FRIEND (evening footpath)
def SH_F(view):
    KEY=view; street(-24,24,77,shops=.6); B.done('st'); setup_render('dusk',res=PCT,samples=SAMPLES,shadow_dist=50); area((.5,-2.5,2.6),220,(3,2),(1,.9,.8),rot=(R(-70),0,0),shadow=False)
    D=person((0,0,0),0,DAN,'flat',name='dan'); S=person((0,0,0),0,SHER,'flat',name='sher'); ph=phone(D,1,'#7FD3FF')
    cs,bg=bgcrowd(321,6,band=(-.5,3.0))
    def upd(t):
        bg(t); put_at(D,t,1.0,-5.2,195,.18); put_at(S,t,0,-5.1,165,.18)
        D['arm'][1].rotation_euler=(R(-125),0,R(30)); ph.location=hand_pos(D,1)
        if view in ('F_call',):
            talk(D,t,184,193,KEY,rest='o',rate=3,shapes=('o','flat')); face(D,brow=.06,brow_r=-10); D['head'].rotation_euler[2]=R(-15); look_at(S,headpos(D),.6)
            two(D,S,d=2.6,lens=26,bias=.35)
        elif view=='F_kaun':
            D['arm'][1].rotation_euler=(R(-20),0,R(10)); talk(S,t,194,195,KEY,rest='o'); talk(D,t,196,198,KEY,rest='flat') if t>wl(196,KEY)-.05 else None
            talk(S,t,199,200,KEY,rest='o') if t>wl(199,KEY)-.05 else None; talk(D,t,201,202,KEY,rest='flat') if t>wl(201,KEY)-.05 else None; look_at(S,headpos(D),.6); look_at(D,headpos(S),.4)
            two(D,S,d=2.6,lens=26)
        elif view in ('F_send','F_days','F_insta'):
            D['arm'][1].rotation_euler=(R(-75),0,R(-25)); D['head'].rotation_euler[0]=R(18); face(D,mouth='flat' if view!='F_insta' else 'O',brow=.05 if view!='F_insta' else .12,eyes=1.0 if view!='F_insta' else 1.2)
            hideH(S) if view!='F_send' else None; cf(D,d=1.6,lat=.35,dz=-.05,lens=30)
        elif view=='F_angry':
            D['arm'][1].rotation_euler=(R(-60),0,R(-20)); talk(D,t,229,235,KEY,rest='frown',shapes=('shout','O','shout','frown')); face(D,brow=-.06,brow_r=22); cf(D,d=1.9,lat=.3,lens=30)
        elif view=='F_shop':
            D['arm'][1].rotation_euler=(R(-20),0,0); talk(S,t,236,241,KEY,rest='smirk'); look_at(S,headpos(D),.5); face(S,brow=-.02,brow_r=-8); cf(S,d=1.9,lat=-.3,lens=30)
        else:
            ph.scale=(0,0,0); x=-2+.7*t; D['root'].location=(x,-5.3,.19); D['root'].rotation_euler[2]=R(90); walk(D,x,step=.5,arm=10); hideH(S)
            talk(D,t,242,259,KEY,rest='flat',rate=5); face(D,brow=.03,eyes=.85); D['head'].rotation_euler[0]=R(8)
            camset((x+3.0,-3.2,1.5),(x+.2,-5.3,1.9),26,5.0)
    return dict(upd=upd)
for v in ('F_call','F_kaun','F_send','F_days','F_insta','F_angry','F_shop','F_seekh'): SHOTS[v]=(lambda v=v: SH_F(v))

# ============================================================ UNCLE RASHID (shop)
def SH_U(view):
    KEY=view; tube=shopset(); setup_interior('day',room=(0,0,3.0),res=PCT,samples=SAMPLES); bpy.context.scene.view_settings.exposure=-0.8; point((0,1.6,2.8),30,(.92,.97,1.0),.6); point((-1,-1.5,2.6),22,(1,.9,.75),.6)
    U=person((.4,1.35,0),0,RASH,'smile',name='rashid'); D=person((0,0,0),0,DAN,'smile',name='dan'); S=person((0,0,0),0,SHER,'smile',name='sher')
    cash=empty((0,0,0))
    for k in range(3): obox((0,0,.006*k),(.08,.04,.003),M('#5FA84A',.6),0,cash)
    def upd(t):
        put_at(U,t,.4,1.35,0); D['root'].location=(-.7,-.7,.008)
        if view=='U_ruko':
            k=ease(t/1.0); D['root'].location=(L(-.7,-1.5,k),L(-.7,-2.0,k),.008); D['root'].rotation_euler[2]=R(L(180,135,k)); stand(D,t); blink(D,t)
            put_at(S,t,-.4,-2.2,170); talk(U,t,260,266,KEY,rest='smile',rate=6); U['arm'][1].rotation_euler=(R(-40),0,R(-70+15*math.sin(t*6))); face(U,brow=.06)
            cf(U,d=1.35,lat=-.25,lens=28)
        else:
            put_at(D,t,-.7,-.55,200); put_at(S,t,-1.5,-.3,215)
            if view=='U_rehne': talk(D,t,267,269,KEY,rest='smile'); D['arm'][1].rotation_euler=(R(-30),0,R(40)); cf(D,d=1.25,lat=.3,lens=28)
            elif view=='U_return':
                cash.scale=(1,1,1); k=ease(t/.8); U['arm'][1].rotation_euler=(R(-85*k),0,R(-35*k)); cash.location=hand_pos(U,1)+Vector((0,-.05,.04)); talk(U,t,270,275,KEY,rest='smile',rate=6)
                cf(U,d=1.5,lat=-.95,dz=-.05,tgt_dz=-.2,lens=26)
            elif view=='U_sherry': talk(S,t,276,284,KEY,rest='o'); S['arm'][1].rotation_euler=(R(-30),0,R(40)); cf(S,d=1.25,lat=.3,lens=28)
            elif view=='U_izzat':
                talk(U,t,285,296,KEY,rest='smile',rate=5); U['arm'][-1].rotation_euler=(R(-80),0,R(10)); face(U,brow=.03,eyes=.9)
                U['arm'][-1].rotation_euler=(R(-30),0,R(20)); q=ease(t/DUR); cf(U,d=L(1.4,1.1,q),lat=.2,lens=28)
            elif view=='U_achay': talk(D,t,297,301,KEY,rest='grin'); face(D,eyes=.85,brow=.04); cf(D,d=1.25,lat=.3,lens=28)
            else:
                talk(U,t,302,313,KEY,rest='smile',rate=5); U['head'].rotation_euler=(R(4),0,R(10*math.sin(t*.8))); face(U,eyes=.85)
                q=ease(t/DUR); cf(U,d=L(1.45,1.2,q),lat=-.3,lens=26)
    return dict(upd=upd)
for v in ('U_ruko','U_rehne','U_return','U_sherry','U_izzat','U_achay','U_shor'): SHOTS[v]=(lambda v=v: SH_U(v))

# ============================================================ BILAL (night road)
def SH_B(view):
    KEY=view; street(-24,24,88,shops=.4); mechanic_shop(4,6.8); B.done('night'); setup_render('nightc',res=PCT,samples=SAMPLES,shadow_dist=40)
    for x in (-12,-4,4,12): point((x,-4.9,7.0),520,(1,.82,.55),.8)
    area((0,-9,2.5),1100,(6,3),(.8,.85,1.0),rot=(R(-90),0,0),shadow=False)
    Bi=person((0,0,0),0,BIL,'frown',name='bilal'); St=person((0,0,0),0,STRG,'smile',name='str'); Me=person((0,0,0),0,MECH,'flat',name='mech'); bk=bike(0,0,0,'#C0392B'); point((4,5.4,2.6),260,(1,.85,.6),.6); point((1,1.0,2.6),120,(1,.85,.6),.6)
    def upd(t):
        if view=='B_bike':
            bk.location=(.9,-1.3,0); bk.rotation_euler=(0,0,R(10)); put_at(Bi,t,-.3,-1.6,-10)
            Bi['arm'][1].rotation_euler=(R(-60),0,R(-10)); Bi['arm'][-1].rotation_euler=(R(-70+12*math.sin(t*12)),0,R(10))
            k=ease((t-.6)/1.2); St['root'].location=(L(-5,-1.4,k),L(-2.6,-1.9,k),.008); St['root'].rotation_euler[2]=R(90 if k<1 else 40); walk(St,St['root'].location.x,step=.55) if k<1 else stand(St,t); blink(St,t)
            talk(St,t,314,316,KEY,rest='smile',rate=6); talk(Bi,t,317,325,KEY,rest='frown',rate=6) if t>wl(317,KEY)-.05 else None; face(Bi,brow=.04,brow_r=-14); hideH(Me)
            camset((0.2,-5.2,1.5),(-.6,-1.6,1.6),24,5.0)
        elif view in ('B_push','B_paise','B_allah'):
            k=ease(t/DUR) if view=='B_push' else 1.0; bx=L(-1,2.4,k); bk.location=(bx,-.6,0); bk.rotation_euler=(0,0,0)
            if view=='B_push': put_at(Bi,t,bx-1.0,-.75,90); put_at(St,t,bx-.25,.1,90)
            else: put_at(Bi,t,bx-.6,-1.3,40); put_at(St,t,bx+.5,-1.3,-40)
            hideH(Me)
            if view=='B_push':
                for H in (Bi,St): walk(H,bx*1.5,step=.45,arm=0); arms(H,-80,0,0,-80,0,0); H['root'].rotation_euler[2]=R(90)
                Bi['root'].rotation_euler[2]=R(90); talk(Bi,t,326,332,KEY,rest='smile',rate=6) if t>wl(326,KEY)-.05 else None
                camset((bx+.8,-4.4,1.5),(bx-.8,-.6,1.2),24,5.0)
            elif view=='B_paise':
                talk(St,t,333,343,KEY,rest='smile',rate=6); St['arm'][1].rotation_euler=(R(-70),0,R(25)); look_at(St,headpos(Bi),.5)
                face(St,brow=.03); cf(St,d=2.0,lat=-.35,lens=30)
            else:
                talk(Bi,t,344,347,KEY,rest='grin',rate=6); Bi['arm'][1].rotation_euler=(R(-80),0,R(30)); Bi['arm'][-1].rotation_euler=(R(-80),0,R(-30))
                face(Bi,eyes=.85,brow=.04); look_at(Bi,headpos(St),.5); cf(Bi,d=2.0,lat=.35,lens=30)
        else:
            bk.location=(3.0,4.6,.18); bk.rotation_euler=(0,0,0); put_at(Me,t,3.6,4.0,-150,.18); Me['arm'][1].rotation_euler=(R(-60+20*math.sin(t*7)),0,R(10)); Me['root'].rotation_euler[0]=R(15)
            put_at(Bi,t,1.6,2.0,-20); put_at(St,t,.6,2.0,20); St['arm'][1].rotation_euler=(R(-150),0,R(20+25*math.sin(t*7))); face(St,mouth='grin'); face(Bi,mouth='grin')
            q=ease(t/DUR); camset((L(1.0,2.0,q),-3.6,L(1.6,2.4,q)),(2.0,2.4,1.4),22,6.0)
    return dict(upd=upd)
for v in ('B_bike','B_push','B_paise','B_allah','B_narr'): SHOTS[v]=(lambda v=v: SH_B(v))

# ============================================================ TEA STALL (evening)
def SH_T(view):
    KEY=view; street(-24,24,99,shops=.5); teastall(); B.done('tea'); setup_render('dusk',res=PCT,samples=SAMPLES,shadow_dist=40)
    point((0,3.0,2.7),160,(1,.8,.55),.8); area((0,-6,2.4),300,(4,2),(1,.85,.7),rot=(R(-90),0,0),shadow=False)
    D=person((0,0,0),0,DAN,'flat',name='dan'); S=person((0,0,0),0,SHER,'flat',name='sher'); CW=person((0,0,0),180,local(331),'smile',name='chaiwala')
    cup=[empty((0,0,0)) for _ in range(2)]
    for c in cup: ocyl((0,0,0),.04,.08,M('#F4F1EA',.3),c,rot=(0,0,0),seg=10)
    def upd(t):
        for H,x,rz in ((D,-.45,-20),(S,.45,20)):
            blink(H,t); H['root'].location=(x,.68,.008); H['root'].rotation_euler=(0,0,R(rz)); H['z0']=0; sit(H,1,.44,90)
        put_at(CW,t,-.8,4.1,180); CW['arm'][1].rotation_euler=(R(-60+10*math.sin(t*3)),0,0)
        cup[0].location=hand_pos(D,1); cup[1].location=hand_pos(S,-1); D['arm'][1].rotation_euler=(R(-70),0,R(-10)); S['arm'][-1].rotation_euler=(R(-70),0,R(10))
        if view=='T_chai': talk(D,t,365,387,KEY,rest='flat',rate=7); face(D,brow=.03,brow_r=-10); look_at(D,headpos(S),.4); q=ease(t/DUR); camset((L(-.2,.0,q),L(-2.6,-2.2,q),1.25),(0,.7,1.35),24,4.0)
        elif view=='T_sherry': talk(S,t,388,399,KEY,rest='flat'); face(S,brow=-.02,brow_r=10); look_at(S,headpos(D),.6); cf(S,d=1.8,lat=-.3,dz=-.1,lens=30)
        elif view=='T_lekin': talk(D,t,400,413,KEY,rest='smile',rate=6); look_at(D,headpos(S),.5); cf(D,d=1.8,lat=.3,dz=-.1,lens=30)
        elif view=='T_toh':
            talk(S,t,414,414,KEY,rest='o'); talk(D,t,415,427,KEY,rest='smile',rate=6) if t>wl(415,KEY)-.05 else None; look_at(S,headpos(D),.6); look_at(D,headpos(S),.3)
            q=ease(t/DUR); camset((L(-.3,-.1,q),-2.4,1.3),(-.1,.7,1.35),26,4.0)
        else:
            talk(S,t,428,440,KEY,rest='smile',rate=6); look_at(S,headpos(D),.5); face(D,mouth='smile'); q=ease(t/DUR); camset((L(0,0,q),L(-2.4,-3.8,q),L(1.3,2.2,q)),(0,.7,1.35),L(26,22,q),5.0)
    return dict(upd=upd)
for v in ('T_chai','T_sherry','T_lekin','T_toh','T_bilkul'): SHOTS[v]=(lambda v=v: SH_T(v))

# ============================================================ MONTAGE + FINAL
def SH_M(view):
    KEY=view
    if view=='M_city':
        city(9,False,R_=170,ss=-1); B.done('city'); setup_render('golden',res=PCT,samples=SAMPLES,shadow_dist=200)
        def upd(t): q=ease(t/DUR); camset((L(-30,0,q),L(-120,-150,q),L(40,70,q)),(0,-20,0),24,8.0)
        return dict(upd=upd)
    mood={'M_people':'morning_s','M_jeb':'afternoon','M_help':'afternoon','M_scam':'nightc','M_vendor':'golden','M_share':'afternoon','M_mother':'dusk','M_shop':'dawn','Z_dan':'golden'}[view]
    street(-24,24,{'M_people':51,'M_jeb':52,'M_help':53,'M_scam':54,'M_vendor':55,'M_share':56,'M_mother':57,'M_shop':58,'Z_dan':59}[view],shops=.8)
    if view=='M_mother': doorway(0,6.7)
    if view in ('M_people','M_vendor','Z_dan'):
        r=random.Random(5)
        for i in range(8): cart(-14+i*4,3.6,500+i)
    B.done('m'); setup_render(mood,res=PCT,samples=SAMPLES,shadow_dist=50)
    if mood=='nightc':
        for x in (-12,-4,4,12): point((x,-4.9,7.0),220,(1,.82,.55),.8)
    if view=='M_people':
        cs,bg=bgcrowd(401,36,band=(-3.4,3.2),xr=(-10,10))
        def upd(t): bg(t); q=ease(t/DUR); camset((L(-4,4,q),-5.4,3.2),(L(-4,4,q),0,1.2),22,8.0)
        return dict(upd=upd)
    if view=='M_jeb':
        TH=person((0,0,0),90,THIEF,'smirk',name='thief'); V=person((0,0,0),90,local(402),'smile',name='vic'); cs,bg=bgcrowd(403,8)
        def upd(t):
            bg(t); x=-2+.8*t
            for H,dy in ((V,0),(TH,-.5)): H['root'].location=(x-(.45 if H is TH else 0),-1.4+dy,.008); H['root'].rotation_euler[2]=R(90); walk(H,x,step=.5,arm=12); blink(H,t)
            TH['arm'][1].rotation_euler=(R(-40-20*math.sin(t*3)),0,R(40)); face(TH,mouth='smirk',brow=-.04,brow_r=14); TH['head'].rotation_euler[2]=R(20*math.sin(t*2))
            camset((x+2.2,-4.9,1.5),(x-.3,-1.6,1.3),26,4.0)
        return dict(upd=upd)
    if view=='M_help':
        E=person((0,0,0),0,ELD,'smile',name='eld'); H_=person((0,0,0),0,local(404),'smile',name='helper'); traffic_=[]
        def upd(t):
            y=-4.0+1.1*t
            for H,dx in ((E,0),(H_,.55)): H['root'].location=(dx,y,.008); H['root'].rotation_euler[2]=R(180); walk(H,y,step=.35,arm=6); blink(H,t)
            arm_to(H_,-1,headpos(E)+Vector((0,0,-.4)),1.0); face(E,mouth='smile',eyes=.85); face(H_,mouth='smile')
            camset((-1.6,y+3.2,1.5),(.3,y,1.5),28,5.0)
        return dict(upd=upd)
    if view=='M_scam':
        A_=person((0,0,0),0,SCAM,'grin',name='s1'); B_=person((0,0,0),0,THIEF,'smirk',name='s2'); C_=person((0,0,0),0,local(405),'grin',name='s3')
        def upd(t):
            for H,x,rz in ((A_,-1.1,15),(B_,0,0),(C_,1.1,-15)): put_at(H,t,x,-1.5,rz); face(H,mouth='smirk' if H is not A_ else 'grin',brow=-.04,brow_r=14)
            A_['arm'][-1].rotation_euler=(R(-130),0,R(30)); C_['arm'][1].rotation_euler=(R(-80),0,R(-30))
            q=ease(t/DUR); camset((0,L(-5.0,-4.0,q),1.4),(0,-1.5,1.8),24,5.0)
        return dict(upd=upd)
    if view=='M_vendor':
        V=person((0,0,0),0,local(406),'smile',name='v'); Cu=person((0,0,0),0,local(407,female=True),'smile',name='c'); coin=empty((0,0,0)); obox((0,0,0),(.07,.035,.003),M('#5FA84A',.6),0,coin)
        def upd(t):
            put_at(V,t,-.5,3.0,180); put_at(Cu,t,-.3,1.7,-10); k=ease((t-.5)/.8)
            V['arm'][1].rotation_euler=(R(-90*k),0,0); coin.location=hand_pos(V,1); face(V,mouth='smile'); face(Cu,mouth='grin' if t>DUR*.6 else 'o')
            q=ease(t/DUR); camset((1.6,.0,1.7),(-.4,2.4,1.5),28,4.0)
        return dict(upd=upd)
    if view=='M_share':
        W1=person((0,0,0),0,dict(local(408),top='#D8C8A0',pants='#7A6A5A'),'smile',name='w1'); W2=person((0,0,0),0,local(409),'flat',name='w2')
        roti=empty((0,0,0)); ocyl((0,0,0),.12,.015,M('#D8A050',.7),roti,rot=(0,0,0),seg=14)
        def upd(t):
            for H,x,rz in ((W1,.5,140),(W2,-.4,220)): blink(H,t); H['root'].location=(x,-5.3,.19); H['root'].rotation_euler=(0,0,R(rz)); H['z0']=.19; sit(H,1,.45+.19,90)
            k=ease((t-.6)/.8); W1['arm'][1].rotation_euler=(R(-50*k),0,R(-15*k)); roti.location=hand_pos(W1,1); face(W2,mouth='grin' if k>.8 else 'flat',eyes=.9); face(W1,mouth='smile')
            camset((-.4,-3.0,1.9),(.05,-5.3,1.0),26,4.0)
        return dict(upd=upd)
    if view=='M_mother':
        Mo=person((0,0,0),0,MOM,'flat',name='mom'); Son=person((0,0,0),90,local(410),'smile',name='son')
        def upd(t):
            put_at(Mo,t,0,6.1,0,.18); Mo['root'].location[2]=.18; k=ease((t-1.2)/1.0); face(Mo,mouth='grin' if k>.5 else 'flat',brow=.03)
            x=L(-6,-.9,ease(min(1,t/2.0))); Son['root'].location=(x,5.4,.19); Son['root'].rotation_euler[2]=R(90); walk(Son,x,step=.55,arm=16) if t<2.0 else stand(Son,t); blink(Son,t)
            Mo['arm'][1].rotation_euler=(R(-120*k),0,R(-30)); Mo['arm'][-1].rotation_euler=(R(-120*k),0,R(30))
            camset((.6,1.6,1.6),(-.4,5.8,1.6),26,5.0)
        return dict(upd=upd)
    if view=='M_shop':
        K=person((0,0,0),180,local(411),'smile',name='k'); sh=obox((0,6.75,1.3),(2.2,.04,1.2),M('#8A9098',.4,metal=.6),0)
        def upd(t):
            put_at(K,t,0,5.9,180,.18); K['root'].location[2]=.19; k=ease(t/(DUR*.8)); sh.location=(0,6.72,1.3+2.2*k); arms(K,-170+40*(1-k),0,15,-170+40*(1-k),0,-15)
            if k>.95: K['root'].rotation_euler[2]=R(L(180,360,ease((t-DUR*.8)/.5))); face(K,mouth='grin')
            camset((1.4,2.6,1.6),(0,6.2,1.6),24,5.0)
        return dict(upd=upd)
    # Z_dan final: Daniyal to camera on golden market street
    D=person((0,0,0),0,DAN,'smile',name='dan'); cs,bg=bgcrowd(412,12,band=(-.4,3.2))
    def upd(t):
        bg(t); put_at(D,t,0,-1.6,0); talk(D,t,559,575,KEY,rest='smile',rate=6); face(D,brow=.03,brow_r=-6)
        D['arm'][1].rotation_euler=(R(-60),0,R(-20)) if wl(564,KEY)<t<wl(570,KEY) else (R(-10),0,0)
        q=ease(t/DUR); cf(D,d=L(2.6,1.8,q),lat=0.0,dz=-.05,lens=30)
    return dict(upd=upd)
for v in ('M_people','M_jeb','M_help','M_scam','M_vendor','M_share','M_mother','M_shop','M_city','Z_dan'): SHOTS[v]=(lambda v=v: SH_M(v))
