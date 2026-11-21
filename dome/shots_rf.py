SHOTS={}
WS=[w_['t0'] for w_ in json.load(open('/home/claude/dome/audio/words.json'))]
SEQ=[('C_hook', 0.0), ('E_fence', 4.17), ('E_clean', 6.94), ('E_saw', 9.8), ('E_crack', 11.66), ('E_long', 13.23), ('C_report', 15.87), ('C_smile', 17.01), ('E_paint', 20.16), ('C_mop', 22.94), ('W_pops', 25.16), ('W_pale', 27.44), ('W_wet', 29.64), ('W_nova', 32.66), ('E_crawl', 33.87), ('E_wider', 36.66), ('E_hand', 38.26), ('E_breeze', 40.91), ('E_scrape', 43.23), ('E_peek', 45.89), ('D_reveal', 47.56), ('D_dome', 50.23), ('C_leaders', 52.73), ('C_fear', 56.3), ('E_alarm', 59.8), ('E_guards', 61.01), ('E_once', 62.37), ('E_twice', 65.01), ('E_burst', 65.82), ('C_sun', 67.51), ('C_walk', 70.58), ('D_step', 73.01), ('D_grass', 74.49), ('D_end', 76.51)]
END=78.82
def DURof(key):
    i=[k for k,_ in SEQ].index(key); return (SEQ[i+1][1] if i+1<len(SEQ) else END)-SEQ[i][1]
def walker(H,start,hdg,speed,t,t0=0.0,arm=24):
    d=max(0,(t-t0))*speed; h=R(hdg); p=Vector(start)+Vector((math.sin(h),-math.cos(h),0))*d
    H['root'].location[0]=p.x; H['root'].location[1]=p.y; H['root'].rotation_euler[2]=h; walk(H,d+H['seed'],step=.55,arm=arm)
def people(specs):
    out=[]
    for i,(x,y,rz,kid) in enumerate(specs): out.append(av((x,y,0),rz,citizen(i*3+7,kid),{'mouth':'smile'},name='c%d'%i))
    return out

# =================================================================== CITY
def CT_(view):
    sunmode=view in ('sun','walk')
    LAMPS=city(hole=(270,9,9,8) if sunmode else None)
    if sunmode:
        w,bg=setup_dark('#FFD9A8',.55,res=PCT,samples=SAMPLES,bloom=.12)
        S=sun((R(76),0,R(0)),6.0,(1,.86,.66),2.0)
        sun((R(-30),0,R(30)),.6,(.55,.75,1.0),5.0).data.use_shadow=False
        for p in LAMPS: point(p,40,(1,.82,.55),.2,shadow=False)
    else:
        w,bg=setup_dark('#0B2238',1.4,res=PCT,samples=SAMPLES,bloom=.08)
        sun((R(18),0,R(35)),2.4,(.6,.8,1.0),8.0); sun((R(160),0,R(0)),.35,(.4,.65,1.0),8.0).data.use_shadow=False
        for p in LAMPS: point(p,90,(1,.8,.5),.2,shadow=False)
    ex={}
    if view=='hook':
        crowd=people([(-3,-2,90,False),(2.5,-3.5,-60,False),(-5.5,1.5,180,True),(5,1,120,False),(0,-6,0,False),(-2,4,200,False),(3.8,-6.5,30,True),(-7,-4,70,False),(6.5,-3,-100,False),(1,3.2,160,False)])
        def upd(t):
            for i,Hc in enumerate(crowd): blink(Hc,t); walker(Hc,(Hc['x'],Hc['y'],0),Hc['rz'],.75,t)
            q=ease(t/DUR); camset((0,-20+5*q,1.6+5.5*q),(0,4,4.5+9*q),17,9.0)
    elif view=='report':
        N=av((0,7.9,.0),180,NOVA,{'mouth':'o'},name='nova'); nova_extras(N)
        Bd=av((0,10.3,1.2),0,BRANDT,{'mouth':'smile'},name='brandt'); Bd['z0']=1.2
        g1=av((-1.6,10.6,1.2),0,guard(1),{'mouth':'flat'},name='g1'); g1['z0']=1.2; g2=av((1.6,10.6,1.2),0,guard(2),{'mouth':'flat'},name='g2'); g2['z0']=1.2
        def upd(t):
            for Hc in (N,Bd,g1,g2): blink(Hc,t); stand(Hc,t)
            N['root'].rotation_euler[2]=R(0); arm_to(N,1,(0,-30,2.0),ease(t/.3)); look_at(N,(0,10.3,3.3)); mouth_talk(N,t,0,DUR,rate=8)
            face(N,brow=.07,brow_r=-10); look_at(Bd,(0,7.9,1.6)); face(Bd,mouth='smile',brow=.02)
            q=ease(t/DUR); camset((3.0-.2*q,6.5,1.9),(0,9.1,2.3),26,5.6,focus=(0,8.4,1.9))
    elif view=='smile':
        N=av((.6,8.0,0),200,NOVA,{'mouth':'flat'},name='nova'); nova_extras(N)
        Bd=av((0,10.3,1.2),0,BRANDT,{'mouth':'smile'},name='brandt'); Bd['z0']=1.2
        def upd(t):
            for Hc in (N,Bd): blink(Hc,t); stand(Hc,t)
            look_at(Bd,(.6,8.0,1.5)); k=ease((t-.25)/.6)
            face(Bd,mouth='grin' if k>.5 else 'smile',brow=.02*k,brow_r=-6*k); Bd['head'].rotation_euler[1]=R(6)*k
            if t>1.5: arms(Bd,-30,0,8,-30,0,-8)
            look_at(N,(0,10.3,3.4)); face(N,mouth='flat',brow=.06,brow_r=-8)
            q=ease(t/DUR); camset((.9-.15*q,7.3,3.2),(0,10.3,3.4),52+8*q,3.2,focus=(0,10.2,3.4))
    elif view=='mop':
        N=av((2.6,-3.2,0),47,NOVA,{'mouth':'frown'},name='nova'); nova_extras(N); mop(N)
        crowd=people([(-4,-5,80,False),(5.5,-6,-90,False),(-1,-8.5,10,False),(3,-.5,190,True)]); point((3.6,-4.2,2.6),60,(1,.85,.65),.3,shadow=False)
        def upd(t):
            blink(N,t); stand(N,t); s_=math.sin(t*3.2)
            N['arm'][1].rotation_euler=(R(-28+10*s_),R(4),R(18*s_)); N['arm'][-1].rotation_euler=(R(-34+10*s_),0,R(-10))
            N['head'].rotation_euler=(R(18),0,R(-6)); face(N,mouth='frown',brow=-.02,brow_r=12); N['root'].rotation_euler[2]=R(47+6*s_)
            for Hc in crowd: blink(Hc,t); walker(Hc,(Hc['x'],Hc['y'],0),Hc['rz'],.8,t)
            q=ease(t/DUR); camset((4.4-.3*q,-4.9+.2*q,1.55),(2.5,-3.0,1.05),32,4.0,focus=(2.6,-3.2,1.1))
    elif view=='leaders':
        point((0,5.5,6.5),500,(.85,.9,1.0),.5,shadow=False)
        Bd=av((0,9.6,5.02),0,BRANDT,{'mouth':'smile'},name='brandt'); Bd['z0']=5.02
        crowd=people([(x,y,180,(i%5==0)) for i,(x,y) in enumerate([(-4,2),(-2.5,1.2),(-1,2.4),(.8,1.4),(2.4,2.2),(4,1.5),(-3.2,-.2),(-1.6,.2),(.2,.4),(1.8,-.3),(3.3,.3),(-.6,-1.6),(1.2,-1.4),(-2.4,-1.8),(2.8,-1.9)])])
        def upd(t):
            blink(Bd,t); stand(Bd,t); k=ease((t-.3)/.8); arms(Bd,-20-70*k,0,30+40*k,-20-70*k,0,-30-40*k); face(Bd,mouth='grin' if t>.6 else 'smile',brow=.02)
            look_at(Bd,(0,0,1.5))
            for Hc in crowd: blink(Hc,t); stand(Hc,t); look_at(Hc,(0,9.4,6.5)); face(Hc,mouth='flat')
            q=ease(t/DUR); camset((1.4,-3.2+.8*q,2.6),(0,9.6,6.6+.8*q),24,8.0)
    elif view=='fear':
        point((0,-4.5,2.4),220,(1,.9,.8),.5,shadow=False)
        crowd=people([(x,y,rz,kid) for (x,y,rz,kid) in [(-1.2,-1,10,False),(.2,-1.5,-6,True),(1.3,-.8,-20,False),(-.4,.4,4,False),(2.4,.2,-30,False),(-2.4,.3,24,False),(.9,1.2,0,True),(-1.6,1.8,12,False)]])
        def upd(t):
            for i,Hc in enumerate(crowd):
                blink(Hc,t); stand(Hc,t); k=ease((t-.2-i*.12)/.6)
                Hc['head'].rotation_euler=(R(-32*k),0,R(6*math.sin(i))); face(Hc,mouth='o' if i%2 else 'frown',brow=.06*k,brow_r=-12*k)
                if i==1: arm_to(Hc,1,(-1.2,-1,1.4),1); arm_to(Hc,-1,(-1.2,-1,1.2),1)
            q=ease(t/DUR); camset((.3,-5.8+.6*q,1.0),(0,0,3.2+1.0*q),24,4.0,focus=(0,-1.2,1.6))
    elif view=='sun':
        crowd=people([(-2,-4,0,False),(1.5,-5,20,False),(-4.5,-2,-20,True),(3.5,-2.5,10,False),(0,-2,-10,False),(-1,-7,0,False),(2.8,-7.5,-5,True),(5,-5,20,False)])
        def upd(t):
            for i,Hc in enumerate(crowd):
                blink(Hc,t); stand(Hc,t); k=ease((t-.1-i*.08)/.5); Hc['head'].rotation_euler=(R(-14*k),0,0)
                if i%3==0: Hc['arm'][1].rotation_euler=(R(-150*k),R(10),R(-30*k))
                face(Hc,mouth='O' if k>.5 and i%2 else 'o',brow=.08*k)
            q=ease(t/DUR); camset((.5,9.5-1.5*q,2.2+.8*q),(0,-30,3.5),20,8.0)
    elif view=='walk':
        sp=[(x,y,0,kid) for (x,y,kid) in [(-2,-2,False),(0,-1.5,False),(2,-2.2,True),(-1,-4,False),(1.2,-4.4,False),(-3,-5,True),(3,-5.6,False),(0,-6.5,False),(-2,-8,False),(1.8,-8.6,False),(-.8,-10,True),(2.6,-11,False)]]
        crowd=people(sp)
        def upd(t):
            for Hc in crowd: blink(Hc,t); walker(Hc,(Hc['x'],Hc['y'],0),0,1.0,t)
            q=ease(t/DUR); camset((1.5,3.5-1.5*q,1.7),(0,-20,2.4),24,8.0)
    return dict(upd=upd)
for _v in ('hook','report','smile','mop','leaders','fear','sun','walk'): SHOTS['C_'+_v]=(lambda v=_v: CT_(v))

# =================================================================== EDGE (pipe tunnel by the glass)
def EG_(view):
    mode={'crawl':'night','wider':'night','hand':'night','breeze':'night','scrape':'dawn','peek':'dawn','alarm':'alarm','guards':'alarm','once':'alarm','twice':'alarm','burst':'alarm'}.get(view,'day')
    painted=view in ('paint','crawl','wider','hand','breeze','scrape','peek','alarm','guards','once','twice','burst')
    G=edge(mode,scrape=view in ('wider','hand','breeze'),burst=(view=='burst'),painted=painted)
    w,bg=setup_dark('#05080E',.4 if mode=='day' else .15,res=PCT,samples=SAMPLES,bloom=.1)
    crack=G['crack']; ex={}
    if view=='paint':
        for o in G['fresh']: o['sx']=o.scale[0]; hide(o)
    if painted and view not in ('paint',):
        crack.scale=(0,0,0) if view=='crawl' else (1,1,1)
    if view in ('fence','clean'): crack.scale=(0,0,0)
    SC=Vector((ED['sc'][0],0,ED['sc'][1]))
    def scraped(r_):
        for o in G['tiles']:
            d=math.hypot(o.location[0]-SC.x,o.location[2]-SC.z)
            o.scale=(0,0,0) if d<r_ else (1,1,1)
    if view in ('peek','scrape','alarm','guards','once','twice','burst'): pass
    if view=='peek' or view in ('alarm','guards','once','twice'): scraped(.55)
    lightin=None
    if mode in ('dawn','alarm'):
        lightin=spot((ED['sc'][0]-.4,3.5,2.2),(ED['sc'][0]-.4,-3.0,.6),1500 if view!='scrape' else 0,(1,.78,.52),40,.4,.05)
    if mode=='alarm':
        beacons=[point((x,-1.2,ED['h']-.3),0,(1,.12,.08),.1,shadow=False) for x in (-4.5,0,4.5)]
        for x in (-4.5,0,4.5): B.cyl((x,-1.2,ED['h']-.15),.12,.15,M('#FF2A1A',.3,emit=4.0),seg=12)
        B.done('beac')
        def alarm_upd(t):
            v=.5+.5*math.sin(t*9)
            for b_ in beacons: b_.data.energy=260*v
        ex['alarm']=alarm_upd
    upd=None
    if view=='fence':
        g1=av((2.2,-1.9,0),-90,guard(4),{'mouth':'flat'},name='g1')
        def upd(t):
            blink(g1,t); walker(g1,(2.2,-1.9,0),-90,.6,t); look_at(g1,(0,0,1.6),.5)
            q=ease(t/DUR); camset((-4.6+.3*q,-3.05,1.75),(1.2,-.8,1.3),20,8.0)
    elif view=='clean':
        N=av((-.4,-1.15,0),180,NOVA,{'mouth':'smile'},name='nova'); nova_extras(N); headlamp(N,on=False); cloth(N,1)
        def upd(t):
            blink(N,t); stand(N,t); s_=math.sin(t*5.0)
            arm_to(N,1,(-.4+.35*s_,-.42,1.22+.05*math.cos(t*5.0)),1); N['arm'][-1].rotation_euler=(R(-20),0,R(-6))
            N['head'].rotation_euler=(R(12),0,R(4*s_)); face(N,mouth='smile',brow=.02)
            q=ease(t/DUR); camset((1.55-.15*q,-1.05,1.6),(-.6,-.85,1.45),28,4.5,focus=(-.4,-1.05,1.5))
    elif view=='saw':
        N=av((-.4,-1.15,0),180,NOVA,{'mouth':'smile'},name='nova'); nova_extras(N); headlamp(N,on=False); cloth(N,1)
        def upd(t):
            blink(N,t); stand(N,t); k=ease((t-.25)/.5)
            arm_to(N,1,(-.4,-.42,1.22),1-k);
            if k>0: N['arm'][1].rotation_euler=(R(L(-60,-20,k)),0,R(4))
            look_at(N,(.4,0,1.7),k); face(N,mouth='o' if k>.5 else 'smile',brow=.09*k,eyes=1+.2*k)
            q=ease(t/DUR); camset((-1.7+.15*q,-2.0,1.8),(.1,-.5,1.7),24,4.0,focus=(-.4,-1.1,1.7))
    elif view=='crack':
        def upd(t):
            q=ease(t/DUR); camset((-.2+.2*q,-.85+.15*q,1.66),(.15,0,1.62),42,2.8,focus=(.1,-.04,1.62))
            crack.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=7.0+1.5*math.sin(t*6)
    elif view=='long':
        N=av((-5.3,-1.0,0),90,NOVA,{'mouth':'o'},name='nova'); nova_extras(N); headlamp(N,on=False)
        def upd(t):
            blink(N,t); stand(N,t); look_at(N,(0,0,1.62)); face(N,mouth='o',brow=.08)
            q=ease(t/DUR); x=L(-3.8,3.8,q); camset((x-.6,-2.3,1.75),(x+1.2,0,1.6),24,6.0)
    elif view=='paint':
        P1=av((-2.2,-.95,0),0,painter(1),{'mouth':'flat'},name='p1'); r1=roller(P1); P2=av((1.4,-.95,0),0,painter(2),{'mouth':'flat'},name='p2'); r2=roller(P2)
        g1=av((2.9,-2.3,0),40,guard(5),{'mouth':'flat'},name='g1')
        fr=G['fresh']
        def upd(t):
            for Hc in (P1,P2,g1): blink(Hc,t); stand(Hc,t)
            for Hc,x0 in ((P1,-2.2),(P2,1.4)):
                s_=math.sin(t*4.5+x0); arm_to(Hc,1,(x0+.55*s_,-.06,1.65+.08*s_),1); Hc['root'].location[0]=x0+.15*math.sin(t*1.2+x0)
            look_at(g1,(0,0,1.6))
            for i,o in enumerate(fr):
                px=o.location[0]; d1=min(abs(px-(-2.2)),abs(px-1.4)); k=max(0,min(1,(t*2.2-d1*.8)))
                o.scale=(k,1,1) if k>0 else (0,0,0)
            q=ease(t/DUR); camset((.2,-3.05,1.7),(-.4,0,1.55),17,8.0)
    elif view in ('crawl','wider','hand','breeze'):
        N=av((0,-.9,0),180,NOVA,{'mouth':'flat'},name='nova'); nova_extras(N); hl=headlamp(N,on=True,e=(160 if view=='crawl' else 50)); wr=wrench(N,-1)
        point((1.1,-.4,1.95),18,(1,.86,.68),.3,shadow=False); point((-.5,-1.8,1.5),35,(.55,.7,1.0),.5,shadow=False)
        motes=dust_motes((ED['sc'][0]+.2,-.07,ED['sc'][1]),30,0,DURof('E_'+view),seed=5,mat=M('#FFF1D0',.3,emit=2.0,alpha=.7)) if view=='breeze' else None
        def upd(t):
            blink(N,t)
            if view=='crawl':
                x=L(4.6,1.0,t/DUR); crawl(N,(x,-.55,.6),-90,t,rate=5.0); hide(wr)
                q=ease(t/DUR); camset((x+1.6,-2.5,.95),(x-.1,-.55,.55),24,4.0,focus=(x,-.55,.6))
            elif view=='wider':
                stand(N,t); N['root'].location=(1.0,-1.15,.008); look_at(N,(.6,0,1.6)); face(N,mouth='o',brow=.08,eyes=1.15)
                crack.scale=(1,1,1+1.2*ease(t/DUR))
                q=ease(t/DUR); camset((-.7,-2.1+.2*q,1.75),(.5,-.2,1.6),26,4.0,focus=(.6,-.6,1.6))
            elif view=='hand':
                stand(N,t); N['root'].location=(.5,-.75,.008); k=ease((t-.2)/.7); arm_to(N,1,(.35,-.03,1.62),k); look_at(N,(.35,0,1.62)); face(N,mouth='flat' if t<1.2 else 'o',brow=.05)
                N['head'].rotation_euler[0]+=R(4*math.sin(t*2)); q=ease(t/DUR); camset((-.35,-1.0,1.72),(.38,-.15,1.62),34,2.6,focus=(.36,-.12,1.62))
            elif view=='breeze':
                stand(N,t); N['root'].location=(.45,-.62,.008); arm_to(N,1,(.35,-.03,1.62),1); look_at(N,(.2,0,1.6),.6); face(N,mouth='O' if t>.4 else 'o',brow=.1,eyes=1.25)
                N['head'].rotation_euler[2]+=R(10)*ease(t/1.0); motes(t)
                q=ease(t/DUR); camset((1.05,-.14,1.74),(.45,-.62,1.72),30+4*q,2.4,focus=(.45,-.62,1.74))
    elif view in ('scrape','peek'):
        N=av((.45,-.72,0),180,NOVA,{'mouth':'strain'},name='nova'); nova_extras(N); hl=headlamp(N,on=True,e=120); wr=wrench(N,1)
        fl=[]; r=random.Random(3)
        if view=='scrape':
            for i in range(40):
                o=obox((0,0,-5),(r.uniform(.015,.04),.004,r.uniform(.015,.04)),PAINT,0); fl.append([o,None])
        def upd(t):
            blink(N,t); stand(N,t)
            if view=='scrape':
                rr=.55*ease(t/(DUR*.92)); scraped(rr); s_=math.sin(t*14)
                arm_to(N,1,(SC.x+rr*.8*math.cos(t*5),-.08,SC.z+rr*.8*math.sin(t*5)),1); face(N,mouth='strain',brow=.04,brow_r=10)
                lightin.data.energy=900*ease(rr/.55); look_at(N,(SC.x,0,SC.z))
                for i,f in enumerate(fl):
                    t0=i*DUR/len(fl)
                    if t>=t0:
                        if f[1] is None: f[1]=(SC.x+rr*math.cos(i*2.4),SC.z+rr*.9*math.sin(i*2.4))
                        dt=t-t0; f[0].location=(f[1][0]+.05*math.sin(i),-.07-.25*dt,f[1][1]-4.9*dt*dt*.6); f[0].rotation_euler=(dt*6,dt*4,i)
                q=ease(t/DUR); camset((-.95,-1.0+.1*q,1.75),(.4,-.12,1.6),28,3.5,focus=(.35,-.3,1.62))
            else:
                look_at(N,(SC.x,0,SC.z)); face(N,mouth='O',brow=.12,eyes=1.3); N['arm'][1].rotation_euler=(R(-15),0,R(4)); hide(wr)
                q=ease(t/DUR); camset((1.0-.45*q,-1.65+1.15*q,1.88-.1*q),(SC.x-.1,3,SC.z),26+12*q,8.0)
    elif view=='alarm':
        N=av((.45,-.8,0),180,NOVA,{'mouth':'O'},name='nova'); nova_extras(N); headlamp(N,on=True,e=90); wr=wrench(N,1)
        def upd(t):
            blink(N,t); stand(N,t); ex['alarm'](t); k=ease((t-.15)/.4); N['root'].rotation_euler[2]=R(180-180*k); face(N,mouth='O',brow=.12,eyes=1.25)
            q=ease(t/DUR); camset((.6,-2.85,1.6),(.45,-.8,1.55),30,4.0)
    elif view=='guards':
        gs=[av((6.5+i*.9,-1.4-.5*(i%2),0),90,guard(10+i),{'mouth':'shout'},name='g%d'%i) for i in range(3)]
        def upd(t):
            ex['alarm'](t)
            for i,g in enumerate(gs): blink(g,t); g['root'].location[0]=6.5+i*.9-4.2*t; g['root'].rotation_euler[2]=R(90); run(g,4.2*t+i*.4); arm_to(g,1,(-3,-1.4,1.6),.6)
            q=ease(t/DUR); camset((-1.0,-2.0,1.4),(5.0,-1.5,1.4),26,5.0)
    elif view in ('once','twice'):
        N=av((.0,-1.25,0),180,NOVA,{'mouth':'strain'},name='nova'); nova_extras(N); headlamp(N,on=True,e=90); wr=wrench(N,1)
        gs=[av((4.0+i*.8,-1.5,0),90,guard(10+i),{'mouth':'shout'},name='g%d'%i) for i in range(2)]
        CRM=M('#F2FBFF',.3,emit=6.0); r=random.Random(11 if view=='once' else 12); segs=[]
        hit=Vector((0.0,-.05,1.35))
        def crackweb(p,ang,ln,dep,t0):
            if dep>3 or ln<.06: return
            a=ang+r.uniform(-.4,.4); q2=(p[0]+ln*math.cos(a),p[1]+ln*math.sin(a))
            mid=((p[0]+q2[0])/2,-.05,(p[1]+q2[1])/2); o=obox(mid,(ln/2,.003,.006),CRM,0); o.rotation_euler=(0,-a,0); segs.append((o,t0))
            crackweb(q2,a,ln*r.uniform(.7,.9),dep+1,t0+.05)
            if r.random()<.6: crackweb(q2,a+r.choice((-1,1))*r.uniform(.5,1.1),ln*.65,dep+1,t0+.07)
        tstrike=.55 if view=='once' else .3
        for k in range(9 if view=='once' else 14): crackweb((hit.x,hit.z),2*pi*k/(9 if view=='once' else 14),.25 if view=='once' else .45,0,tstrike)
        def upd(t):
            blink(N,t); stand(N,t); ex['alarm'](t)
            if view=='once': k=ease(t/.4) if t<.4 else 1-ease((t-.4)/.15)
            else: k=ease(t/.18) if t<.18 else 1-ease((t-.18)/.12)
            k=1-k if view=='once' else 1-k
            kk=ease((t-(.4 if view=='once' else .18))/.15)
            swing(N,kk if t>=(.4 if view=='once' else .18) else 0)
            if view=='once' and t<.4: swing(N,0); N['arm'][1].rotation_euler[0]=R(L(-60,-175,ease(t/.4))); N['arm'][-1].rotation_euler[0]=R(L(-54,-169,ease(t/.4)))
            face(N,mouth='strain',brow=.02,brow_r=14)
            for o,t0 in segs: o.scale=(0,0,0) if t<t0 else (min(1,(t-t0)/.06),1,1)
            SHAKE[0]=.02*max(0,1-(t-tstrike)/.25) if t>tstrike else 0
            for i,g in enumerate(gs): blink(g,t); g['root'].location[0]=4.0+i*.8-2.0*t; run(g,2.0*t+i*.3)
            if view=='once': q=ease(t/DUR); camset((-1.8+.3*q,-2.6,1.4),(.2,-.3,1.5),24,5.0)
            else: camset((1.7,-1.7,1.65),(-.1,-.1,1.4),22,4.0)
    elif view=='burst':
        N=av((.0,-1.25,0),180,NOVA,{'mouth':'O'},name='nova'); nova_extras(N); headlamp(N,on=True,e=60); wr=wrench(N,1)
        for o in G['tiles']: o.data.materials[0]=PAINT
        sh=[]; r=random.Random(5); GL=M('#DFF4FF',.05,spec=1.0,alpha=.35)
        for o in G['tiles']:
            if math.hypot(o.location[0]-SC.x,o.location[2]-SC.z)<.55: o.data.materials[0]=GL
            p=o.location.copy(); v=(r.uniform(-1.5,1.5),r.uniform(5,10),r.uniform(0,3.5)); sh.append((o,tuple(p),v,(r.uniform(-9,9),r.uniform(-9,9),r.uniform(-9,9))))
        ballistic(sh,.12,floor=-.35); flood=area((ED['sc'][0],1.2,1.35),0,(3.2,2.6),(1,.85,.62),rot=(R(-90),0,0),shadow=False)
        def upd(t):
            blink(N,t); stand(N,t); k=ease((t-.15)/.4)
            N['arm'][-1].rotation_euler=(R(-130*k),R(0),R(-35*k)); N['arm'][1].rotation_euler=(R(-20),0,R(10)); N['root'].rotation_euler[0]=R(-6*k); face(N,mouth='O',brow=.12,eyes=1.2)
            lightin.data.energy=1500+6000*ease((t-.1)/.6); ex['alarm'](t); flood.data.energy=3500*ease((t-.08)/.5)
            SHAKE[0]=.03*max(0,1-t/.4)
            q=ease(t/DUR); camset((-2.3-.2*q,-1.5,1.45),(.25,-.25,1.45),20,8.0)
    if upd is None:
        def upd(t): camset((0,-3,1.6),(0,0,1.6),24)
    return dict(upd=upd)
for _v in ('fence','clean','saw','crack','long','paint','crawl','wider','hand','breeze','scrape','peek','alarm','guards','once','twice','burst'): SHOTS['E_'+_v]=(lambda v=_v: EG_(v))

# =================================================================== WORKSHOP
def WS_(view):
    G=workshop(); w,bg=setup_dark('#1A1410',.25,res=PCT,samples=SAMPLES,bloom=.06)
    P=av((-.6,1.35,0),180,POPS,{'mouth':'smile'},name='pops'); N=av((.7,-.2,0),220,NOVA,{'mouth':'flat'},name='nova'); nova_extras(N)
    skin=P['skinm']; pb=skin.node_tree.nodes['Principled BSDF']
    def pale(k): pb.inputs['Base Color'].default_value=tuple(L(a,b,k) for a,b in zip(hexc(POPS['skin']),hexc('#E9DCD2')))
    def upd(t):
        blink(P,t); blink(N,t); stand(P,t); stand(N,t)
        if view=='pops':
            P['root'].rotation_euler[2]=R(180); P['arm'][1].rotation_euler=(R(-55+8*math.sin(t*4)),0,R(10)); P['arm'][-1].rotation_euler=(R(-45),0,R(-8))
            P['head'].rotation_euler=(R(18),0,0); face(P,mouth='smile'); pale(0)
            N['root'].rotation_euler[2]=R(248); walk(N,t*.6); N['root'].location[0]=2.7-.5*t; N['root'].location[1]=-.5+.2*t
            q=ease(t/DUR); camset((1.8-.3*q,-2.4,1.9),(-1.0,1.3,1.45),22,8.0)
        else:
            P['root'].rotation_euler[2]=R(40); N['root'].location=(.7,-.2,.008); N['root'].rotation_euler[2]=R(220)
            look_at(P,(.7,-.2,1.6)); look_at(N,(-.6,1.35,1.8))
            if view=='pale':
                k=ease((t-.4)/1.0); pale(k); face(P,mouth='o' if k>.4 else 'smile',brow=.08*k,eyes=1+.2*k); P['arm'][1].rotation_euler=(R(-20*k),0,0)
                q=ease(t/DUR); camset((.2,-.4,1.85),(-.6,1.35,1.9),40+10*q,2.8,focus=(-.6,1.35,1.9))
            elif view=='wet':
                pale(1); k=ease((t-.1)/.5); P['root'].rotation_euler[0]=R(10*k); P['head'].rotation_euler[0]+=R(10*k)
                mouth_talk(P,t,.15,DUR-.3,shapes=('o','flat','o','flat'),rate=6); face(P,brow=.1,brow_r=-8,eyes=1.15)
                face(N,mouth='flat',brow=.05)
                q=ease(t/DUR); camset((-.2,-.9,1.8),(-.55,1.3,1.9),30+6*q,3.2,focus=(-.6,1.35,1.9))
            elif view=='nova':
                pale(1); k=ease((t-.1)/.4); face(N,mouth='o' if k>.4 else 'flat',brow=.1*k,eyes=1+.3*k); N['head'].rotation_euler[2]+=R(-15*k)
                q=ease(t/DUR); camset((.02,.68,1.7),(.7,-.2,1.62),32+5*q,2.4,focus=(.7,-.2,1.62))
    return dict(upd=upd)
for _v in ('pops','pale','wet','nova'): SHOTS['W_'+_v]=(lambda v=_v: WS_(v))

# =================================================================== OUTSIDE: dried seabed
def DS_(view):
    grass=view in ('grass','end')
    if view in ('step','grass'): city(hole=(270,9,9,8)); seabed(grass=grass,hole=True,dome=False)
    else: seabed(grass=grass,hole=view not in ('reveal',))
    S,w,rp,bg=setup_render('morning_s' if grass else 'dawn',res=PCT,samples=SAMPLES)
    if not grass: S.rotation_euler=(R(78),0,0); S.data.energy=3.2; S.data.color=(1,.78,.55)
    sunb=None
    if not grass:
        B.cyl((-20,-260,10),9,.5,M('#FFF0C0',.2,emit=12.0),rot=(R(90),0,0),seg=40); B.done('sun')
    upd=None
    if view=='reveal':
        def upd(t):
            q=ease(t/DUR); camset((0,-37.5-2*q,1.8+.4*q),(-6,-120,4+2*q),24-4*q,8.0)
    elif view=='dome':
        def upd(t):
            q=ease(t/DUR); camset((-38+6*q,-78+4*q,6+4*q),(0,0,10),18,8.0)
    elif view=='step':
        N=av((0,-36.2,0),0,NOVA,{'mouth':'grin'},name='nova'); nova_extras(N); wr=wrench(N,1)
        P=av((-1.2,-35.4,0),0,POPS,{'mouth':'smile'},name='pops')
        crowd=[av((x,-34.8+dy,0),0,citizen(i*5+2,i%4==1),{'mouth':'smile'},name='s%d'%i) for i,(x,dy) in enumerate([(1.3,.2),(-2.6,.6),(2.6,.9),(0,1.2),(-1.5,1.6),(1.6,2.0)])]
        def upd(t):
            for i,Hc in enumerate([N,P]+crowd):
                blink(Hc,t); walker(Hc,(Hc['x'],Hc['y'],0),0,1.0,t)
                face(Hc,mouth='grin' if i%2==0 else 'smile',brow=.06)
            q=ease(t/DUR); camset((2.3,-42.5+.5*q,.6),(0,-36,1.6),26,5.0,focus=(0,-37.2,1.2))
    elif view=='grass':
        kids=[av((x,y,0),rz,citizen(i*9+40,True),{'mouth':'grin'},name='k%d'%i) for i,(x,y,rz) in enumerate([(-3,-44,90),(-1.5,-46,90),(2,-47,-90),(4,-43,-90)])]
        sitters=[av((x,y,0),rz,citizen(i*11+60,False),{'mouth':'smile'},name='a%d'%i) for i,(x,y,rz) in enumerate([(-6,-41,20),(-5,-40.5,-30),(5.5,-41.5,10),(7,-45,-40)])]
        def upd(t):
            for i,Hc in enumerate(kids): blink(Hc,t); Hc['root'].location[0]=Hc['x']+(2.4*t if i<2 else -2.4*t); run(Hc,2.4*t+i)
            for Hc in sitters: blink(Hc,t); sit(Hc,1,.02,90); Hc['head'].rotation_euler[0]=R(-10)
            q=ease(t/DUR); camset((0,-60+4*q,2.0+1.5*q),(0,-20,7),20,8.0)
    elif view=='end':
        N=av((0,-44,0),0,NOVA,{'mouth':'smile'},name='nova'); nova_extras(N); wr=wrench(N,1)
        P=av((-1.6,-41.5,0),20,POPS,{'mouth':'smile'},name='pops')
        def upd(t):
            blink(N,t); blink(P,t); stand(N,t); stand(P,t)
            N['arm'][1].rotation_euler=(R(-22),0,R(8)); k=ease((t-.4)/.5)
            face(N,mouth='grin' if k>.5 else 'smile',brow=.05*k,brow_r=-6); N['head'].rotation_euler=(R(-4),R(6*k),0)
            q=ease(t/DUR); camset((.15,-46.6+.4*q,1.62),(0,-44,1.6),40+6*q,2.8,focus=(0,-44.2,1.6))
    return dict(upd=upd)
for _v in ('reveal','dome','step','grass','end'): SHOTS['D_'+_v]=(lambda v=_v: DS_(v))
