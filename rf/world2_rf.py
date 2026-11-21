# extra sets: city bus (moving prop) and the night neighbourhood
def bus():
    """city bus, near side in the plane y=0 (local), body extends to +y... built around origin; returns root empty"""
    BODY=M('#E8ECEF',.3,metal=.2); TEAL=M('#1E8F8A',.3,metal=.2); DK=M('#0B0D12',.5); GL=M('#0A1420',.03,spec=1.0,alpha=.38); RUB=M('#111216',.8)
    Lb=5.2; W=2.5
    B.box((0,-.02,.72),(Lb,.03,.38),BODY,.02); B.box((0,-.03,.62),(Lb,.012,.07),TEAL,.004); B.box((0,-.02,2.72),(Lb,.03,.3),BODY,.02); B.box((0,-W/2,3.03),(Lb,W/2,.06),BODY,.04)
    B.box((0,-W/2,.36),(Lb,W/2,.04),DK,0); B.box((0,-W+.02,1.7),(Lb,.03,1.35),DK,0)
    for sx in (-1,1): B.box((sx*Lb,-W/2,1.7),(.04,W/2,1.35),BODY,.03)
    for k in range(8): B.box((-Lb+.1+k*(2*Lb-.2)/7,-.02,1.75),(.05,.035,.7),DK,.005)
    for k in range(4): B.box((-3.6+k*2.4,-W/2,2.95),(.7,.06,.02),M('#DDF2FF',.3,emit=1.2),0)
    for sx_ in (-3.4,3.2):
        for yy in (-.12,-W+.12): B.cyl((sx_,yy,.45),.45,.26,RUB,rot=(R(90),0,0),seg=20); B.cyl((sx_,yy+(.12 if yy>-1 else -.12),.45),.2,.03,M('#8A8E96',.4,metal=.6),rot=(R(90),0,0),seg=14)
    B.box((-Lb-.03,-.5,.8),(.02,.22,.1),M('#FFF2C8',.3,emit=9.0),.01); B.box((-Lb-.03,-W+.5,.8),(.02,.22,.1),M('#FFF2C8',.3,emit=9.0),.01); B.box((Lb+.03,-W/2,.8),(.02,1.0,.06),M('#FF3A2A',.3,emit=5.0),.01)
    B.box((-Lb-.02,-W/2,2.75),(.02,.9,.16),M('#FFB02E',.3,emit=4.0),0)
    objs=B.done('bus'); g=obox((0,-.005,1.75),(Lb-.05,.004,.68),GL,0); g.name='glass_bus'
    root=empty((0,0,0))
    for o in objs+[g]: o.parent=root
    return root

def neighbourhood():
    """row of five houses on a wet night street; returns list of (warm_windows_obj, cold_windows_obj, x)"""
    GR=M('#1F3A2A',.9,kind='grass'); ASPH=M('#14161B',.2,spec=.8); WALK=M('#3C3F48',.5,kind='concrete',sc=1.0)
    B.box((0,8,-.05),(40,14,.05),GR,0); B.box((0,-4.5,-.04),(40,3.2,.05),ASPH,0); B.box((0,-.6,0),(40,.75,.06),WALK,0); B.box((0,-9.5,-.05),(40,2,.06),GR,0)
    for k in range(-8,9): B.box((k*3.2,-4.5,.012),(.8,.06,.004),M('#C9C4A8',.4),0)
    cols=[('#B9C7D6','#3A4660'),('#E6D7B8','#6B3A2E'),('#C9D9C4','#2F4A3A'),('#E2C0B8','#4A3040'),('#D8D2C8','#33373F')]; out=[]; r=random.Random(11)
    for i in range(5):
        x=-13+i*6.5; wc,rc=cols[i]; w=2.3; d=2.6; h=3.0+.5*(i%2)
        WM=M(wc,.8,kind='siding'); RM=M(rc,.7,kind='shingle'); TR=M('#F4F1EA',.5)
        B.box((x,3.6,h/2),(w,d,h/2),WM,0)
        # gable roof (two slabs) + gable triangle
        for sg in (-1,1): B.box((x+sg*(w/2+.05),3.6,h+.78),(w*.62,d+.25,.07),RM,.01,rot=(0,R(-sg*33),0))
        B.poly([(x-w,1.0-.001,h),(x+w,1.0-.001,h),(x,1.0-.001,h+1.5)],WM); B.box((x+w*.5,4.2,h+1.1),(.22,.22,.6),M('#6B4A3E',.8,kind='concrete',sc=.3),.01)
        # door, porch, steps, path
        B.box((x-.9,.98,1.05),(.42,.04,1.05),M(rc,.5),.01); B.box((x-.9,.94,2.2),(.55,.05,.06),TR,.01); B.box((x-.62,.93,1.05),(.03,.02,.05),M('#C9A24A',.3,metal=.9),.005)
        B.box((x-.9,.55,.12),(.8,.45,.12),M('#8A8E96',.7,kind='concrete'),.01); B.box((x-.9,-.05,.02),(.45,.3,.02),WALK,0)
        B.box((x-.9,.75,2.5),(.9,.4,.04),RM,.01,rot=(R(12),0,0))
        for sg in (-1,1): B.cyl((x-.9+sg*.8,.2,1.25),.05,2.4,TR,seg=8)
        # window frames
        wins=[(x+.95,1.35),(x+.95,h-.55+.0)] + ([(x-.9,h-.5)] if i%2 else [])
        for (wx,wz) in wins:
            B.box((wx,.97,wz),(.62,.03,.52),TR,.01); B.box((wx,.93,wz-.56),(.7,.08,.04),TR,.01)
        B.poly([(x-.5,.99,h+.75),(x+.5,.99,h+.75),(x+.5,.99,h+.2),(x-.5,.99,h+.2)],WM) if False else None
        # hedge, mailbox, tree
        for k in range(5): B.ico((x+.2+k*.42,.35,.32),.34,M(['#2F6A3A','#36783F','#2A5E34'][k%3],.8),sc=(1,1,.9),sub=1)
        B.cyl((x-2.3,-.9,.5),.04,1.0,M('#22252C',.5),seg=8); B.box((x-2.3,-.9,1.08),(.14,.22,.1),M(['#C9452E','#2B58C9','#D8D2C8'][i%3],.4),.03)
        tx_=x+2.9; B.cyl((tx_,1.6,1.1),.16,2.2,M('#4A3424',.8,kind='wood'),seg=10)
        for k in range(7): a=k*.9; B.ico((tx_+.6*math.cos(a),1.6+.5*math.sin(a),2.6+.35*(k%3)),.75,M(['#24523A','#2B5E40','#1F4A34'][k%3],.85),sub=1)
        wm=M('#FFC66B',.4,emit=4.5); cm=M('#8FD2FF',.3,emit=5.5)
        ws=[]; cs=[]
        for (wx,wz) in wins:
            for mat,lst in ((wm,ws),(cm,cs)):
                o=obox((wx,.955,wz),(.56,.01,.46),mat,0); lst.append(o)
                for dx,dz,sx,sz in ((0,0,.02,.46),(0,0,.56,.02)): obox((0,-.012,0),(sx,.004,sz),TR,0,o)
        gl=point((x+.95,-.4,1.4),0,(1,.75,.4),.3,shadow=False)
        out.append(dict(x=x,warm=ws,cold=cs,light=gl))
    for lx in (-9.8,3.2):
        B.cyl((lx,-1.2,2.4),.06,4.8,M('#22252C',.4,metal=.6),seg=10); B.box((lx,-1.7,4.8),(.05,.55,.05),M('#22252C',.4),.01); B.box((lx,-2.15,4.72),(.15,.22,.06),M('#FFE2A8',.3,emit=8.0),.02)
        spot((lx,-2.1,4.6),(lx,-1.8,0),1800,(1,.82,.55),120,.7,.15)
    # far hills / skyline + moon + stars
    r=random.Random(5)
    for k in range(18): B.ico((-34+k*4,16+r.uniform(-2,2),r.uniform(-1,1)),r.uniform(4,7),M('#0E1A22',.9),sub=1)
    B.ico((-9,40,17),2.2,M('#F4F1DC',.5,emit=3.0),sub=3)
    for k in range(70): B.ico((r.uniform(-40,40),45,r.uniform(6,30)),r.uniform(.04,.1),M('#FFFFFF',.5,emit=4.0),sub=1)
    B.done('batch_nb')
    return out
