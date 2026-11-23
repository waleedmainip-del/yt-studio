# Shots for "Lahore - Everyone Is Secretly Rich". Cuts sit on narration words (audio/words.json); SEQ is written by gen_seq.py.
SHOTS={}
END=76.7333
SEQ=[('OPEN', 0.0), ('WANT', 3.433), ('MEET', 6.267), ('W1', 9.567), ('B1', 12.667), ('S1', 15.3), ('BSTARE', 18.233), ('B2', 18.733), ('ARRIVE', 20.133), ('W2', 22.833), ('B3', 25.0), ('S2', 26.767), ('ORDER', 28.967), ('B4', 32.367), ('S3', 34.667), ('B5', 36.033), ('EAT', 37.833), ('BILL', 38.367), ('SILENT', 40.2), ('W3', 42.2), ('B6', 44.733), ('S4', 47.567), ('W4', 49.933), ('B7', 51.5), ('FREEZE', 53.367), ('APPS', 53.767), ('S5', 56.2), ('W5', 59.5), ('B8', 61.333), ('LOOKB', 62.733), ('WAITERIN', 63.067), ('WHO', 64.6), ('POINT', 65.933), ('MORAL', 68.567), ('DISHES', 71.367), ('WALK', 73.0)]
W_=json.load(open(LH+'/audio/words.json'))
def wt(a,b): return (W_[a]['s'],W_[b]['e'])
def ws(i): return W_[i]['s']-T0
def we(i): return W_[i]['e']-T0
def rest(H,a=6): H['arm'][1].rotation_euler=(R(-5),0,R(a)); H['arm'][-1].rotation_euler=(R(-5),0,R(-a))
def cwalk(H,x0,y,d,v,t,step=.55,arm=24):
    H['root'].location[0]=x0+d*v*t; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(90*d); walk(H,v*t+H['seed'],step=step,arm=arm)
def nod(H,t,a=5,f=6): H['head'].rotation_euler[0]+=R(a*math.sin(t*f))
def menu_card(e,s=1.0):
    obox((0,-.1,.16*s),(.17*s,.012,.25*s),M('#7A1F2E',.5),.01,e); obox((0,-.114,.16*s),(.14*s,.004,.21*s),M('#D9B24A',.3,metal=.8),.004,e); obox((0,-.119,.16*s),(.125*s,.004,.195*s),M('#7A1F2E',.5),.004,e)
    text('MENU',(0,-.125,.16*s),(0,-1,0),.075*s,M('#FFE7A0',.4,emit=.8),ex=.004,parent=e)
# ================================================================ CANAL (dusk): the plan
CP={'wa':(0,2.0,0),'bi':(-1.25,3.1,14),'sh':(1.25,3.1,-14)}
def cset(night=False,fx_=0.0,place=True):
    S=canal(night,fx_); P={}
    for k,C in (('wa',WALEED),('bi',BILAL),('sh',SHERRY)):
        x,y,rz=CP[k]; P[k]=mk(C,x,y,rz,k)
    S['P']=P; S['W']=walkers(5,3,-45,45,(20.2,),z=.07); return S
def cidle(S,t,skip=()):
    traffic(S,T0+t); upd_walkers(S['W'],T0+t)
    for k,H in S['P'].items():
        if k in skip: continue
        x,y,rz=CP[k]; H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(rz); stand(H,t); blink(H,t); rest(H); H['head'].rotation_euler=(0,0,0)
def OPEN_():
    S=cset(); wa,bi,sh=S['P']['wa'],S['P']['bi'],S['P']['sh']; sparkles((3.5,.9,2.2),1.6,.2,3.4,n=34,size=.05,seed=5,rise=.3)
    def upd(t):
        cidle(S,t,skip=('wa','bi','sh')); v=1.15
        cwalk(wa,6.4,.9,-1,v,t); cwalk(bi,7.5,-.25,-1,v,t); cwalk(sh,7.5,2.0,-1,v,t); shk(bi,1)
        for H in (wa,bi,sh): blink(H,t)
        face(wa,mouth='smirk',brow=.04); face(bi,mouth='smirk',brow=.02); face(sh,mouth='smile')
        x=wa['root'].location[0]; q=ease(t/DUR); camset((x-L(4.6,3.6,q),.9+.5*(1-q),L(.95,1.25,q)),(x,.95,1.95),24,8)
    return dict(upd=upd)
SHOTS['OPEN']=OPEN_
def WANT_():
    S=cset(); wa,bi,sh=S['P']['wa'],S['P']['bi'],S['P']['sh']; bubble('#RICHLIFE',(0,2.3,3.2),W_[15]['s']-dict(SEQ)['WANT'],size=.16,col='#FFFFFF',bg='#E8306A')
    fl=point((.3,-.6,2.5),0,(1,1,1),r=.3,shadow=False)
    def upd(t):
        cidle(S,t); bi['root'].location=(-1.35,3.2,0); sh['root'].location=(1.35,3.2,0); arm_to(wa,1,(1.0,.3,1.5),1); wa['arm'][-1].rotation_euler=(R(-6),0,R(-14))
        bi['root'].rotation_euler[1]=R(-6); sh['root'].rotation_euler[1]=R(6); shk(bi,1)
        bi['arm'][-1].rotation_euler=(R(-155),0,R(-12)); sh['arm'][1].rotation_euler=(R(-155),0,R(12))
        face(wa,mouth='grin',brow=.05); face(bi,mouth='smirk',brow=.03); face(sh,mouth='grin',brow=.04)
        for H in (wa,bi,sh): look_at(H,(.3,-.9,2.3),.6)
        tf=ws(18)+.25; fl.data.energy=2500*max(0,1-abs(t-tf)/.09)
        q=ease(t/DUR); camset(LV((.3,-1.7,2.4),(.25,-1.4,2.36),q),(0,2.6,1.85),21,8)
    return dict(upd=upd)
SHOTS['WANT']=WANT_
def MEET_():
    S=cset(); P=S['P']
    for k,nm,wi,c in (('wa','WALEED',19,'#0E5C56'),('bi','BILAL',20,'#7A1F2E'),('sh','SHERRY',22,'#2B5A8A')): x,y,_=CP[k]; label(nm,(x*1.08,y,3.05),W_[wi]['s']-dict(SEQ)['MEET'],size=.21,col='#FFFFFF',bg=c)
    def upd(t):
        cidle(S,t); shk(P['bi'],0); face(P['wa'],mouth='grin',brow=.04); face(P['bi'],mouth='smirk'); face(P['sh'],mouth='smile')
        gest(P['wa'],t,1,.5,5,-58); look_at(P['bi'],hp(P['wa']),.6); look_at(P['sh'],hp(P['wa']),.6)
        q=ease(t/DUR); camset(LV((.4,-2.3,2.0),(.2,-1.9,2.05),q),(0,2.4,2.0),23,8)
    return dict(upd=upd)
SHOTS['MEET']=MEET_
def ctalk(key,a,b,cam,lens=36,extra=None,rest_='flat',tz=-.28,shades=0):
    def S_():
        S=cset(); P=S['P']
        def upd(t):
            cidle(S,t); shk(P['bi'],shades); H=P[key]; talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k!=key: look_at(o,hp(H),.7,maxyaw=55)
            if extra: extra(S,t)
            q=ease(t/DUR); h=hp(H,tz); c1=(cam[0]+(h[0]-cam[0])*.07,cam[1]+(h[1]-cam[1])*.07,cam[2]); camset(LV(cam,c1,q),h,lens,2.8)
        return dict(upd=upd)
    return S_
def _w1(S,t): H=S['P']['wa']; gest(H,t,1,.9,7,-70); H['arm'][-1].rotation_euler=(R(-40),0,R(-30)); H['head'].rotation_euler[2]=R(8*math.sin(t*2.2))
def _b1(S,t):
    H=S['P']['bi']; k=tl(t,ws(35),ws(35)+.3); shk(H,k); H['arm'][1].rotation_euler=(R(-18),0,R(26)); H['arm'][-1].rotation_euler=(R(-18),0,R(-26)); H['head'].rotation_euler[0]=R(-7*k)
def _s1(S,t):
    H=S['P']['sh']; k=tl(t,ws(42),ws(42)+.3); arm_to(H,-1,(-3.2,1.8,1.5),k); face(H,brow=-.02,brow_r=-8,eyes=.8); B_=S['P']['bi']; face(B_,mouth='flat' if t<ws(46) else 'o',brow=.06 if t>ws(46) else 0)
def _b2(S,t):
    H=S['P']['bi']; shk(H,1); k=tl(t,0,.3); arm_to(H,1,H['root'].matrix_world@Vector((.25,-.5,1.75)),k); face(H,brow=.05); H['head'].rotation_euler[0]=R(-8)
SHOTS['W1']=ctalk('wa',28,33,(.45,-1.2,2.0),extra=_w1,rest_='grin')
SHOTS['B1']=ctalk('bi',34,40,(-1.55,-.3,2.0),extra=_b1,rest_='smirk')
SHOTS['S1']=ctalk('sh',41,48,(1.55,-.3,2.0),extra=_s1)
def BSTARE_():
    S=cset(); P=S['P']; bubble('PETROL: EMPTY',(-4.3,1.4,2.75),.12,size=.17,col='#FFFFFF',bg='#D8301A')
    def upd(t):
        cidle(S,t); shk(P['bi'],1); bi=P['bi']; bi['root'].location[0]=-2.1; bi['root'].location[1]=2.0; face(bi,mouth='flat',brow=.06,eyes=1.15); look_at(bi,(-4.3,1.6,1.2),min(1,t/.3)*.9,maxyaw=70)
        for k in ('wa','sh'): look_at(P[k],hp(bi),.8,maxyaw=60); face(P[k],mouth='smirk')
        q=ease(t/DUR); camset(LV((-3.5,-2.3,1.7),(-3.45,-2.0,1.7),q),(-3.2,1.8,1.45),24,8)
    return dict(upd=upd)
SHOTS['BSTARE']=BSTARE_
SHOTS['B2']=ctalk('bi',49,52,(-1.55,-.3,2.0),extra=_b2,rest_='smirk',shades=1)
# ================================================================ ROOFTOP RESTAURANT
DSEATS=[(-4.9,4.8,0),(-6.25,3.3,84),(4.7,5.1,0),(6.05,3.6,-84),(-5.6,-1.2,0),(-6.95,-2.7,84)]
def tarms(H,dz=0.0):
    m=root_mat(H)
    for s in (1,-1): arm_to(H,s,m@Vector((s*.34,-.62,1.2+dz)),1)
def tset(stage,waiter=None,stand_=False):
    rooftop(stage); P={}
    for k,C in (('wa',WALEED),('bi',BILAL),('sh',SHERRY)):
        x,y,rz=SEATS[k]; P[k]=mk(C,x,y,rz,k)
    D=[]
    for i,(x,y,rz) in enumerate(DSEATS): chair(x,y,rz,cu='#2B6A8A'); D.append(mk(person(41+i*3),x,y,rz,'d%d'%i))
    chef=mk(dict(person(8),apron='#F4F1EA',hairstyle='cap',cap='#F4F1EA',top='#F4F1EA',pants='#2A2C34'),-6.6,6.25,0,'chef')
    wtr=mk(WAITER,waiter[0],waiter[1],waiter[2],'waiter') if waiter else None
    steam((-6.6,5.3,1.4),0,99,n=12,seed=6,size=.09)
    return dict(P=P,D=D,chef=chef,wt=wtr,wpos=waiter)
def tidle(S,t,free=(),look=None):
    for k,H in S['P'].items():
        seat(H,t+dseed(k),.6); H['root'].location[0]=SEATS[k][0]; H['root'].location[1]=SEATS[k][1]; H['root'].rotation_euler[2]=R(SEATS[k][2]); H['head'].rotation_euler=(0,0,0); shk(H,0) if k=='bi' else None
        if k not in free: tarms(H)
    for i,H in enumerate(S['D']):
        seat(H,t+i*1.7,.6); H['root'].rotation_euler[2]=R(DSEATS[i][2]); tarms(H,.04*math.sin(t*2.4+i)); H['head'].rotation_euler=(R(5+5*math.sin(t*1.6+i*2)),0,R(10*math.sin(t*.7+i)))
        face(H,mouth='smile' if int(t*1.5+i)%3 else 'o')
        if look is not None: look_at(H,look,.8,maxyaw=80)
    c=S['chef']; stand(c,t); blink(c,t); c['arm'][1].rotation_euler=(R(-55+14*math.sin(t*5)),0,R(8)); c['arm'][-1].rotation_euler=(R(-40),0,R(-10))
    w=S['wt']
    if w: stand(w,t); blink(w,t); w['root'].location[0]=S['wpos'][0]; w['root'].location[1]=S['wpos'][1]; w['root'].rotation_euler[2]=R(S['wpos'][2]); w['arm'][1].rotation_euler=(R(-5),0,R(5)); w['arm'][-1].rotation_euler=(R(-42),R(-20),0); w['head'].rotation_euler=(0,0,0)
TC={'wa':(.4,-1.75,1.98),'bi':(.62,-1.35,1.98),'sh':(-.62,-1.35,1.98)}     # close-up camera per seat
def ttalk(stage,key,a,b,cam=None,lens=38,extra=None,init=None,rest_='flat',tz=-.3,waiter=None,fs=2.8):
    def S_():
        S=tset(stage,waiter); P=S['P']; c0=cam or TC[key]
        if init: init(S)
        def upd(t):
            tidle(S,t); H=P[key]; talk(H,t,*wt(a,b),rest=rest_); face(H,brow=.04)
            for k,o in P.items():
                if k!=key: look_at(o,hp(H),.6,maxyaw=60)
            if extra: extra(S,t)
            q=ease(t/DUR); h=hp(H,tz); c1=(c0[0]+(h[0]-c0[0])*.07,c0[1]+(h[1]-c0[1])*.07,c0[2]); camset(LV(c0,c1,q),h,lens,fs)
        return dict(upd=upd)
    return S_
WIDE=((0,-4.9,2.1),(0,.6,1.62),21)
def ARRIVE_():
    S=tset('menu',(3.1,-2.4,face_dir(-3.1,-2.6))); P=S['P']; AP={'wa':(0,-4.3),'bi':(-1.95,-4.0),'sh':(1.9,-4.0)}
    def upd(t):
        tidle(S,t,free=('wa','bi','sh'))
        for k,H in P.items():
            x,y=AP[k]; H['root'].location[0]=x; H['root'].location[1]=y; H['root'].rotation_euler[2]=R(180); stand(H,t+dseed(k)); blink(H,t); rest(H); H['head'].rotation_euler=(R(-14*tl(t,.3,1.2)),0,R((10 if k=='bi' else -10 if k=='sh' else 0)*math.sin(t*1.3)))
        shk(P['bi'],0); w=S['wt']; b=tl(t,.6,1.3)-tl(t,2.2,2.9); w['root'].rotation_euler[0]=R(16*b); face(w,mouth='smile')
        q=ease(t/DUR); camset(LV((0,-7.55,2.5),(0,-7.4,3.5),q),LV((0,4,2.3),(0,10,3.4),q),19,8)
    return dict(upd=upd)
SHOTS['ARRIVE']=ARRIVE_
WFL=(-1.55,-2.15,face_dir(1.55,2.15))            # waiter, front-left of the table (seen from behind in wides)
WBR=(1.95,2.65,face_dir(-1.95,-2.65))            # waiter, behind-right (faces camera)
def W2_():
    S=tset('menu',WBR); P=S['P']
    def upd(t):
        tidle(S,t,free=('wa',)); wa=P['wa']; talk(wa,t,*wt(59,64),rest='grin'); face(wa,brow=.05); k=tl(t,0,.25); sn=math.sin(t*14)*4*(1 if t<ws(60) else 0)
        wa['arm'][1].rotation_euler=(R(-150*k+sn),R(-10),0); arm_to(wa,-1,root_mat(wa)@Vector((-.34,-.62,1.2)),1); look_at(wa,hp(S['wt']),.6)
        for k_ in ('bi','sh'): look_at(P[k_],hp(wa),.5); face(P[k_],mouth='smirk' if k_=='bi' else 'smile')
        w=S['wt']; w['root'].rotation_euler[0]=R(8*tl(t,ws(60),ws(60)+.4))
        q=ease(t/DUR); camset(LV((.2,-5.1,2.15),(.15,-4.7,2.12),q),(0,.5,1.55),26,5.6)
    return dict(upd=upd)
SHOTS['W2']=W2_
def _b3(S,t):
    H=S['P']['bi']; k=tl(t,.1,.5)
    gest(H,t,1,.9,6,-75); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); H['root'].rotation_euler[0]=R(-6*k); face(H,brow=.05)
def _s2i(S):
    S['menu']=in_hand(S['P']['sh'],1,lambda e: menu_card(e,1.25)); S['bub']=bubble('KARAHI  Rs 8,500',(1.25,-.25,2.75),W_[73]['s']-dict(SEQ)['S2'],size=.14,col='#FFFFFF',bg='#D8301A')
def _s2(S,t):
    H=S['P']['sh']; H['arm'][1].rotation_euler=(R(-78),R(14),0); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); look_at(H,hp(S['P']['wa']),tl(t,ws(71)-.1,ws(71)+.2)*.25,maxyaw=70)
    face(H,brow=.06,eyes=1.15)
def _ordi(S): S['menu']=in_hand(S['P']['wa'],-1,lambda e: menu_card(e,1.25)); S['pad']=in_hand(S['wt'],-1,lambda e: obox((0,-.08,.1),(.09,.012,.13),M('#F4F1EA',.6),.01,e))
def ORDER_():
    S=tset('menu',WBR); P=S['P']; _ordi(S)
    def upd(t):
        tidle(S,t,free=('wa',)); wa=P['wa']; talk(wa,t,*wt(80,83),rest='grin'); face(wa,brow=.06)
        wa['arm'][-1].rotation_euler=(R(-74),R(-16),0); sw=tl(t,ws(80),ws(83)); m=root_mat(wa); arm_to(wa,1,m@Vector((.05,-.72,L(1.95,1.45,sw))),tl(t,ws(77)+.3,ws(80)))
        look_at(wa,hp(S['wt']),.75*tl(t,ws(80)-.2,ws(80)+.2),maxyaw=75)
        w=S['wt']; w['arm'][1].rotation_euler=(R(-72+6*math.sin(t*22)*(1 if t>ws(81) else 0)),R(20),0); w['arm'][-1].rotation_euler=(R(-70),R(-18),0); face(w,mouth='flat' if t<ws(82) else 'o',brow=.06*tl(t,ws(82),ws(82)+.3)); look_at(w,hp(wa,-.4),.8)
        for k_ in ('bi','sh'): look_at(P[k_],hp(wa),.7); face(P[k_],mouth='grin' if k_=='bi' else 'flat',brow=.05 if k_=='sh' else 0)
        q=ease(t/DUR); camset(LV((-.9,-2.6,2.0),(-.75,-2.3,2.0),q),(.75,1.9,1.82),30,4)
    return dict(upd=upd)
SHOTS['ORDER']=ORDER_
def _b4(S,t): H=S['P']['bi']; gest(H,t,1,1.0,8,-95); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); face(H,brow=.05)
def _s3(S,t): H=S['P']['sh']; face(H,brow=-.02,brow_r=-10,eyes=.75); H['head'].rotation_euler[2]+=R(-6)
def _b5i(S): S['gl']=in_hand(S['P']['bi'],1,lambda e: (ocyl((0,-.06,.1),.055,.2,M('#DCEAF2',.05,spec=1.0,alpha=.4),e,rot=(0,0,0),seg=10),ocyl((0,-.06,.08),.046,.13,M('#F28A3A',.4,alpha=.9),e,rot=(0,0,0),seg=10))); sparkles((-1.0,-.3,2.75),.5,ws_abs(92),ws_abs(92)+1.4,n=18,size=.04,seed=7,rise=.3)
def ws_abs(i): return W_[i]['s']-dict(SEQ)['B5']
def _b5(S,t): H=S['P']['bi']; k=tl(t,0,.35); H['arm'][1].rotation_euler=(R(-128*k),R(-8),0); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); face(H,brow=.06); H['head'].rotation_euler[0]=R(-6*k)
SHOTS['B3']=ttalk('menu','bi',65,70,extra=_b3,rest_='smirk',waiter=WBR)
SHOTS['S2']=ttalk('menu','sh',71,76,extra=_s2,init=_s2i,waiter=WBR)
SHOTS['B4']=ttalk('feast','bi',84,88,extra=_b4,rest_='grin')
SHOTS['S3']=ttalk('feast','sh',89,90,extra=_s3)
SHOTS['B5']=ttalk('feast','bi',91,93,extra=_b5,init=_b5i,rest_='grin')
def EAT_():
    S=tset('feast'); P=S['P']; D_={k:in_hand(P[k],1,lambda e: drumstick(e,1.5)) for k in P}
    def upd(t):
        tidle(S,t)
        for i,(k,H) in enumerate(P.items()):
            c=math.sin(t*9+i*2); H['arm'][1].rotation_euler=(R(-118+8*c),R(-22),0); H['head'].rotation_euler[0]=R(6+5*c); face(H,mouth='o' if c>0 else 'flat',brow=.04)
        q=ease(t/DUR); camset(LV((.3,-4.6,2.3),(.2,-4.2,2.25),q),(0,.5,1.5),26,5.6)
    return dict(upd=upd)
SHOTS['EAT']=EAT_
def BILL_():
    S=tset('bill',WBR); P=S['P']; fo,setk=receipt()
    def upd(t):
        tidle(S,t); k=tl(t,.15,.5); fo.location[2]=L(1.6,1.06,ease_out(k)); fo.scale=(k,k,k); setk(max(0,(t-.55)/1.5))
        w=S['wt']; face(w,mouth='smile')
        for i,(k_,H) in enumerate(P.items()): look_at(H,(0,-.9,1.0),tl(t,.3,.7),maxyaw=80,maxpitch=45); face(H,mouth='smile' if t<.9 else 'o',brow=.06*tl(t,.9,1.2),eyes=1+.15*tl(t,.9,1.2))
        q=ease(t/DUR); camset(LV((.25,-3.3,2.7),(.2,-3.5,2.45),q),LV((0,-.3,1.05),(0,-.9,.7),q),30,5.6)
    return dict(upd=upd)
SHOTS['BILL']=BILL_
def bill_done():
    fo,setk=receipt(); setk(1.0); return fo
def SILENT_():
    S=tset('bill',WBR); P=S['P']; bill_done()
    def upd(t):
        tidle(S,t,look=(0,0,1.2) if t>1.4 else None)
        for k_,H in P.items(): look_at(H,(0,-.7,1.0),1,maxyaw=80,maxpitch=45); face(H,mouth='o',brow=.06,eyes=1.18); H['root'].rotation_euler[1]=0
        w=S['wt']; face(w,mouth='smile')
        q=ease(t/DUR); camset(LV((0,-4.8,2.15),(0,-4.0,2.05),q),(0,.6,1.5),25,5.6)
    return dict(upd=upd)
SHOTS['SILENT']=SILENT_
def _bi(S): bill_done()
def _w3(S,t): H=S['P']['wa']; look_at(H,hp(S['P']['bi']),.35,maxyaw=70); face(H,brow=.06,brow_r=8); arm_to(H,1,(-.2,-.4,1.3),tl(t,ws(101),ws(101)+.3)); face(S['P']['bi'],mouth='flat',brow=.05)
def _b6(S,t):
    H=S['P']['bi']; k=tl(t,0,.25); w=math.sin(t*9)*5
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-95*k+w),R(-s*22),0)
    face(H,brow=.06); H['head'].rotation_euler[2]+=R(8*math.sin(t*5))
def _s4i(S): bill_done(); S['strip']=in_hand(S['P']['sh'],-1,lambda e: (obox((0,-.08,.3),(.1,.004,.4),M('#FFFFFF',.8,emit=.25),0,e),[obox((0,-.086,.05+j*.08),(.07,.002,.012),M('#3A3D47',.7),0,e) for j in range(8)]))
def _s4(S,t):
    H=S['P']['sh']; arm_to(H,1,hp(S['P']['wa'],-.5),tl(t,ws(116)-.1,ws(116)+.2)); H['arm'][-1].rotation_euler=(R(-85),R(18),0); look_at(H,hp(S['P']['wa']),.25,maxyaw=70); face(H,brow=.06,brow_r=-6,eyes=1.1)
    face(S['P']['wa'],mouth='o',brow=.06)
def _w4(S,t):
    H=S['P']['wa']; k=tl(t,0,.25)
    for s in (1,-1): H['arm'][s].rotation_euler=(R(-166*k),R(-s*8*k),0)
    face(H,brow=.06,brow_r=10,eyes=1.15); H['head'].rotation_euler[2]+=R(10*math.sin(t*6))
def _b7(S,t):
    H=S['P']['bi']; arm_to(H,-1,hp(S['P']['wa'],-.5),tl(t,ws(129)-.1,ws(129)+.15)); arm_to(H,1,root_mat(H)@Vector((.34,-.62,1.2)),1); H['root'].rotation_euler[0]=R(8*tl(t,ws(131),ws(131)+.2)); look_at(H,hp(S['P']['wa']),.3,maxyaw=70); face(H,brow=.06,brow_r=-8,eyes=1.1)
SHOTS['W3']=ttalk('bill','wa',100,106,extra=_w3,init=_bi)
SHOTS['B6']=ttalk('bill','bi',107,115,extra=_b6,init=_bi)
SHOTS['S4']=ttalk('bill','sh',116,121,extra=_s4,init=_s4i)
SHOTS['W4']=ttalk('bill','wa',122,127,extra=_w4,init=_bi,rest_='o')
SHOTS['B7']=ttalk('bill','bi',128,133,extra=_b7,init=_bi,rest_='o')
def FREEZE_():
    S=tset('bill'); P=S['P']; bill_done()
    def upd(t):
        tidle(S,t); k=tl(t,.15,.55)
        for k_,H in P.items(): H['root'].rotation_euler[0]=R(-9*k); face(H,mouth='flat',brow=-.02*k,eyes=1-.25*k); H['head'].rotation_euler[0]=R(14*k)
        
        q=ease(t/DUR); camset(LV((0,-4.7,3.4),(0,-4.5,3.2),q),(0,.5,1.4),26,5.6)
    return dict(upd=upd)
SHOTS['FREEZE']=FREEZE_
def phones_up(S,t,k):
    for k_,H in S['P'].items(): hold_phone(H,1,k); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); look_at(H,H['arm'][1].matrix_world@Vector(hand_loc(H,1)),.9*k,maxyaw=40,maxpitch=22)
def APPS_():
    S=tset('bill'); P=S['P']; bill_done(); PH={k:phone(H,1) for k,H in P.items()}; GL={k:point((0,0,0),0,(.55,.8,1.0),r=.2,shadow=False) for k in P}
    def upd(t):
        tidle(S,t,free=('wa','bi','sh'))
        for i,(k_,H) in enumerate(P.items()):
            k=tl(t,.25+i*.22,.6+i*.22); PH[k_].scale=(k,k,k); hold_phone(H,1,k); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); hl=H['arm'][1].matrix_world@Vector(hand_loc(H,1))
            look_at(H,hl,.9*k,maxyaw=40,maxpitch=22); GL[k_].location=hl+Vector((0,0,.2)); GL[k_].data.energy=7*k; face(H,mouth='flat',brow=.03)
        q=ease(t/DUR); camset(LV((0,-4.9,2.1),(0,-4.5,2.08),q),(0,.6,1.5),26,5.6)
    return dict(upd=upd)
SHOTS['APPS']=APPS_
def bal(key,a,b,txt,bg,wi,bx,rest_='flat',fx_=None):
    def init(S):
        bill_done(); S['ph']={k:phone(H,1) for k,H in S['P'].items()}; H=S['P'][key]; S['gl']=point((0,0,0),0,(.55,.8,1.0),r=.2,shadow=False)
        bubble(txt,(H['root'].location[0]+bx[0],H['root'].location[1]+bx[1],2.78),W_[wi]['s']-dict(SEQ)[SHOTKEY[key]],size=.2,col='#FFFFFF',bg=bg)
    def extra(S,t):
        phones_up(S,t,1); H=S['P'][key]; S['gl'].location=(H['arm'][1].matrix_world@Vector(hand_loc(H,1)))+Vector((0,0,.2)); S['gl'].data.energy=7
        for k_,o in S['P'].items():
            if k_!=key: o['head'].rotation_euler=(R(14),0,0)
        if fx_: fx_(S,t)
    return ttalk('bill',key,a,b,extra=extra,init=init,rest_=rest_,tz=-.42)
SHOTKEY={'sh':'S5','wa':'W5','bi':'B8'}
def _s5(S,t): face(S['P']['sh'],brow=.05,brow_r=8)
def _w5(S,t): face(S['P']['wa'],brow=.06,brow_r=10)
def _b8(S,t): H=S['P']['bi']; k=tl(t,ws(151),ws(152)); H['root'].rotation_euler[0]=R(10*k); face(H,brow=.06,brow_r=12,eyes=.85)
SHOTS['S5']=bal('sh',141,146,'BALANCE: Rs 340','#2B5A8A',144,(-.55,-.55),fx_=_s5)
SHOTS['W5']=bal('wa',147,149,'BALANCE: Rs 120','#0E5C56',148,(0,-.6),fx_=_w5)
SHOTS['B8']=bal('bi',150,152,'BALANCE: - Rs 45','#D8301A',151,(.55,-.55),fx_=_b8)
def LOOKB_():
    S=tset('bill'); P=S['P']; bill_done(); PH={k:phone(H,1) for k,H in P.items()}
    def upd(t):
        tidle(S,t,free=('wa','bi','sh')); phones_up(S,t,1); bi=P['bi']; k=tl(t,.1,.6)
        for k_ in ('wa','sh'): H=P[k_]; look_at(H,hp(bi),k,maxyaw=85); face(H,mouth='flat',brow=-.02,brow_r=-10,eyes=.8)
        bi['root'].rotation_euler[0]=R(12*k); bi['head'].rotation_euler[0]=R(22*k); face(bi,mouth='flat',brow=.06,brow_r=12)
        q=ease(t/DUR); camset(LV((0,-4.6,2.1),(-.3,-3.9,2.05),q),LV((0,.6,1.5),(-.5,.5,1.5),q),27,5.6)
    return dict(upd=upd)
SHOTS['LOOKB']=LOOKB_
WAP=(-.5,-2.5,180)
def WAITERIN_():
    S=tset('bill',(-.5,-6.4,180)); w=S['wt']; bill_done(); PH_={k:phone(H,1) for k,H in S['P'].items()}
    def upd(t):
        tidle(S,t); k=walk_path(w,[(-.5,-6.6),(-.5,-2.5)],t,-.2,DUR-.25,step=.5,arm=10); face(w,mouth='flat',brow=-.01); blink(w,t)
        if t>DUR-.25: stand(w,t); w['root'].rotation_euler[2]=R(180)
        w['arm'][1].rotation_euler[0]*=.4; w['arm'][-1].rotation_euler=(R(-42),R(-20),0); phones_up(S,t,1)
        for H in S['P'].values(): face(H,mouth='flat',brow=.05)
        wy=w['root'].location[1]; q=ease(t/DUR); camset((.75,wy-2.7,2.45),(-.1,.4,1.7),24,5.6)
    return dict(upd=upd)
SHOTS['WAITERIN']=WAITERIN_
def WHO_():
    S=tset('bill',WAP); w=S['wt']; bill_done(); point((.6,-1.0,2.5),90,(1,.88,.72),r=.6,shadow=False); cm=in_hand(w,1,lambda e: (obox((0,-.08,.1),(.085,.03,.15),M('#22242B',.4),.02,e),obox((0,-.112,.15),(.065,.004,.05),M('#8FD0FF',.3,emit=2.0),.004,e)))
    def upd(t):
        tidle(S,t); talk(w,t,*wt(156,158),rest='smile'); w['arm'][1].rotation_euler=(R(-48*tl(t,.1,.4)),R(-12),0); w['arm'][-1].rotation_euler=(R(-42),R(-20),0)
        face(w,brow=.06*tl(t,ws(157),ws(157)+.2),brow_r=-6); w['head'].rotation_euler[2]=R(6*tl(t,we(158),we(158)+.3))
        q=ease(t/DUR); camset(LV((.2,-.35,1.85),(.16,-.5,1.88),q),hp(w,-.3),34,2.8)
    return dict(upd=upd)
SHOTS['WHO']=WHO_
PT={'wa':'bi','bi':'sh','sh':'wa'}
def pointing(S,t,k):
    P=S['P']
    for a,b in PT.items():
        H=P[a]; arm_to(H,1,hp(P[b],-.35),k); arm_to(H,-1,root_mat(H)@Vector((-.34,-.62,1.2)),1); look_at(H,hp(P[b]),k,maxyaw=85); face(H,mouth='shout' if k>.5 else 'flat',brow=.05,brow_r=-8)
def POINT_():
    S=tset('bill',WAP); bill_done(); w=S['wt']
    def upd(t):
        tidle(S,t,free=('wa','bi','sh'),look=(0,0,1.6) if t>.7 else None); k=ease_out(tl(t,.45,.62)); pointing(S,t,k); face(w,mouth='flat',brow=-.03)
        w['arm'][-1].rotation_euler=(R(-42),R(-20),0)
        q=ease(t/DUR); camset(LV((1.7,-4.2,2.3),(1.6,-3.9,2.25),q),(0,.5,1.5),23,5.6)
    return dict(upd=upd)
SHOTS['POINT']=POINT_
def MORAL_():
    S=tset('bill',WAP); bill_done(); w=S['wt']
    def upd(t):
        tidle(S,t,free=('wa','bi','sh'),look=(0,0,1.6)); pointing(S,t,1); face(w,mouth='flat',brow=-.03); w['arm'][-1].rotation_euler=(R(-42),R(-20),0); w['head'].rotation_euler[2]=R(14*math.sin(t*2.2))
        q=ease(t/DUR); camset(LV((1.6,-3.9,2.25),(4.2,-9.4,6.2),q),LV((0,.5,1.5),(0,6,3.4),q),L(23,19,q),8)
    return dict(upd=upd)
SHOTS['MORAL']=MORAL_
# ================================================================ KITCHEN: until the bill arrives
def DISHES_():
    kitchen(); P={}
    for (k,C),x in zip((('bi',BILAL_K),('wa',WALEED_K),('sh',SHERRY_K)),KX): P[k]=mk(C,x,1.5,0,k)
    w=mk(WAITER,2.9,1.5,-90,'waiter'); PL={}; SP={}
    for k,H in P.items():
        PL[k]=in_hand(H,-1,lambda e: ocyl((0,-.1,.05),.23,.03,M('#F8F6F0',.3,spec=.8),e,rot=(R(90),0,0),seg=18)); SP[k]=in_hand(H,1,lambda e: obox((0,-.08,.02),(.09,.05,.06),M('#F2C14E',.9),.02,e))
    for i,x in enumerate(KX): sparkles((x,.3,1.5),.5,0,6,n=14,size=.05,seed=20+i,rise=.9,mat=M('#FFFFFF',.2,emit=.8))
    def upd(t):
        for i,(k,H) in enumerate(P.items()):
            stand(H,t+i); blink(H,t); x=KX[i]; a=t*9+i*2
            arm_to(H,-1,(x-.22,.62,1.5),1); arm_to(H,1,(x+.16+.09*math.cos(a),.6,1.52+.07*math.sin(a)),1); H['head'].rotation_euler=(R(16),0,0)
        face(P['wa'],mouth='grin',brow=.05); P['wa']['head'].rotation_euler=(R(4),0,R(10*math.sin(t*1.5)))
        face(P['bi'],mouth='flat',brow=.05,brow_r=12); look_at(P['sh'],hp(P['wa']),tl(t,.6,1.0)*.9,maxyaw=80); face(P['sh'],mouth='flat',brow=-.03,brow_r=-12,eyes=.75)
        stand(w,t); blink(w,t); arm_to(w,1,root_mat(w)@Vector((-.3,-.45,1.45)),1); arm_to(w,-1,root_mat(w)@Vector((.3,-.45,1.38)),1); w['leg'][1].rotation_euler[0]=R(-9*max(0,math.sin(t*10))); face(w,mouth='flat',brow=-.03,brow_r=-8)
        look_at(w,hp(P['sh']),.8)
        q=ease(t/DUR); camset(LV((-5.3,-1.9,2.15),(-5.0,-1.7,2.12),q),(-.6,1.25,1.8),27,8)
    return dict(upd=upd)
SHOTS['DISHES']=DISHES_
# ================================================================ CANAL (night): the walk home
def WALK_():
    X0=41.0; S=canal(True,36.0); wa=mk(WALEED,X0,1.5,-90,'wa'); bi=mk(BILAL,X0+1.05,.05,-90,'bi'); sh=mk(SHERRY,X0+1.05,2.5,-90,'sh'); bk=S['bike']; W=walkers(4,5,-10,80,(20.2,),z=.07)
    def upd(t):
        traffic(S,T0+t); upd_walkers(W,T0+t); v=.95; tt=t+.5
        cwalk(wa,X0,1.5,-1,v,tt,step=.5,arm=20); cwalk(bi,X0+1.05,.05,-1,v,tt,step=.5,arm=10); cwalk(sh,X0+1.05,2.5,-1,v,tt,step=.5,arm=12)
        for H in (wa,bi,sh): blink(H,t)
        bx=bi['root'].location[0]+.2; bk['root'].location=(bx,-1.0,0); bk['root'].rotation_euler[2]=R(180)
        for wl in bk['wheels']: wl.rotation_euler[1]=-(v*tt)/(.32*1.4)
        arm_to(bi,1,(bx-.85,-.56,1.62),1); shk(bi,0); bi['root'].rotation_euler[0]=R(10); face(bi,mouth='flat',brow=.05,brow_r=12); bi['head'].rotation_euler[0]=R(14)
        talk(wa,t,*wt(177,184),rest='grin'); face(wa,brow=.05); g=tl(t,ws(177),ws(177)+.3)*(1-tl(t,we(184),we(184)+.4)); wa['arm'][1].rotation_euler[0]=L(wa['arm'][1].rotation_euler[0],R(-72+7*math.sin(t*7)),g); wa['arm'][1].rotation_euler[1]=R(-10*g)
        look_at(wa,hp(sh),.5*tl(t,ws(181),ws(181)+.3),maxyaw=70)
        face(sh,mouth='flat',brow=-.03,brow_r=-12,eyes=.75); look_at(sh,hp(wa),.6,maxyaw=70); fp=tl(t,we(184)+.1,we(184)+.5)
        if fp>0: arm_to(sh,1,sh['head'].matrix_world@Vector((.1,-.5,.25)),fp,base=tuple(sh['arm'][1].rotation_euler)); sh['head'].rotation_euler[0]=R(14*fp)
        x=wa['root'].location[0]; q=ease(t/DUR); camset((x-L(4.9,4.1,q),.2,L(1.75,1.9,q)),(x+.5,.3,1.75),20,5.6)
    return dict(upd=upd)
SHOTS['WALK']=WALK_
