# India vs Pakistan - shots part 3: the world stops (street, shops, wedding), the cricket on TV, the streets at night
def STOPS():
    W=mohalla('P'); FILLE[0]=0
    bag=empty((0,0,-5)); obox((0,0,0),(.16,.12,.2),M('#F4F4F0',.6,alpha=.85),.05,bag)
    def upd(t):
        q=ease(t/DUR); bag.location=(2+3.5*t,-1.2+.5*math.sin(t*2),1.2+.5*math.sin(t*3.1)); bag.rotation_euler=(t*2,t*1.3,t*3)
        camset(LV((-21,0,11.0),(-14,0,4.4),q),LV((16,0,3.0),(22,0,3.4),q),22,8)
    return dict(upd=upd)
SHOTS['STOPS']=STOPS
def ROADS():
    W=mohalla('I',seed=7); FILLE[0]=0; ball=oico((0,0,.22),.22,M('#F4F1EA',.5),None,sub=2); pap=empty((0,0,-5)); obox((0,0,0),(.3,.22,.004),M('#EDE8DC',.7),0,pap)
    def upd(t):
        q=ease(t/DUR); ball.location=(1.5+2.2*t,1.4-.9*t,.22); ball.rotation_euler=(t*6,t*8,0)
        pap.location=(4-2.5*t,-.6+.4*t,.25+.2*abs(math.sin(t*5))); pap.rotation_euler=(t*4,t*2.2,t*3)
        camset(LV((-7.5,-.5,.5),(-6.6,-.5,.55),q),(14,.3,3.2),21,8)
    return dict(upd=upd)
SHOTS['ROADS']=ROADS
def SHOPS():
    W=mohalla('P',seed=3,note_at=((1,5),('MATCH KE BAAD','AANA')),nopole=(-4,16)); FILLE[0]=10
    cx=[i for s,k,i in W['blds'] if s==1 and k==5][0]['x']
    def upd(t):
        q=ease(t/DUR); camset(LV((cx-3.4,-.9,2.3),(cx-2.7,-.1,2.3),q),(cx-.1,SY,2.55),27,8)
    return dict(upd=upd)
SHOTS['SHOPS']=SHOPS
# ---------------------------------------------------------------- the wedding
def turban(H,col='#8A1F2E'):
    u=H['u']; Hd=H['head']; m=M(col,.8,kind='fabric')
    obox((0,0,.98*u),(.72*u,.72*u,.24*u),m,.08*u,Hd); obox((0,0,1.22*u),(.56*u,.56*u,.16*u),m,.08*u,Hd); obox((0,-.72*u,1.02*u),(.12*u,.04*u,.2*u),M('#E6B53A',.3,metal=.8),.02*u,Hd)
    obox((.3*u,-.3*u,1.5*u),(.05*u,.05*u,.22*u),M('#F4F1EA',.6),.02*u,Hd,rot=(0,R(18),0))
def wed_set(back=False):
    shaadi(); FILLE[0]=22; G=[]
    if not back:
        for i,(x,y) in enumerate(SEATS_G):
            pchair(x,y,180,['#F4F1EA','#E8D2A0'][i%2]); H=mk(GUESTS[i],x,y,180,'g%d'%i); H['home']=(x,y,180); H['ph']=phone_of(H,1); G.append(H)
    br=mk(BRIDE,1.15,5.05,0,'bride',z=STG); br['home']=(1.15,5.05,0); sa=mk(SASUR,-.6,1.6,8,'sasur'); return G,br,sa
def wed_idle(G,br,sa,t):
    for H in G:
        sitp(H,t,seat=.56,lean=8); phone_up(H,1,1.0,h=3.0,fw=1.2,sx=.55); look_at(H,handw(H,1),1.0,maxpitch=30); face(H,mouth='o',brow=.04,eyes=1.1)
    sitp(br,t,lean=0); crossed(br); face(br,mouth='frown',brow=-.03,brow_r=-12,eyes=.95); br['head'].rotation_euler[2]=R(8*math.sin(t*1.2))
def WEDDING():
    G,br,sa=wed_set()
    def upd(t):
        wed_idle(G,br,sa,t); standp(sa,t,-.6,1.6,8); look_at(sa,(6*math.sin(t*2.4),-6,2),1.0,maxyaw=70); face(sa,mouth='frown',brow=.03,brow_r=8,eyes=1.05); what_pose(sa,.5,t,amp=.3)
        q=ease(t/DUR); camset(LV((0,-9.3,3.0),(0,-8.5,2.85),q),(0,4.4,2.2),20,8)
    return dict(upd=upd)
SHOTS['WEDDING']=WEDDING
def DULHA():
    G,br,sa=wed_set()
    def upd(t):
        wed_idle(G,br,sa,t); standp(sa,t,-.6,1.6,8); look_at(sa,(4*math.sin(t*5.5),-6,2.1),1.0,maxyaw=60); face(sa,mouth='O',brow=.04,brow_r=10,eyes=1.15)
        what_pose(sa,1,t,amp=.8); speak(sa,t,29,31,gesture=False)
        q=ease(t/DUR); camset(LV((-.95,-2.9,2.05),(-.9,-2.55,2.05),q),(-.45,1.6,2.0),29,8)
    return dict(upd=upd)
SHOTS['DULHA']=DULHA
def LASTOVER():
    shaadi(); FILLE[0]=30; gr=mk(GROOM,0,8.5,180,'groom'); y1=mk(YAAR1,-1.8,7.75,170,'yaar1'); y2=mk(YAAR2,1.8,7.75,190,'yaar2'); bh=mk(BEHRA,3.9,7.9,205,'behra'); turban(gr); ph=phone_of(gr,1)
    gl=point((0,0,0),14,(.6,.8,1.0),r=.2,shadow=False)
    def upd(t):
        for H,x,y,rz in ((gr,0,8.5,180),(y1,-1.8,7.75,170),(y2,1.8,7.75,190),(bh,3.9,7.9,205)): standp(H,t,x,y,rz)
        phone_up(gr,1,1.0,h=3.5,fw=1.3,sx=.35); bpy.context.view_layer.update(); pw=Vector(handw(gr,1)); gl.location=pw+Vector((0,.35,.15))
        look_at(gr,pw,1.0,maxpitch=28); face(gr,mouth='flat',brow=.05,eyes=1.2); speak(gr,t,32,37,gesture=False)
        k=ease(tl(t,ws(35)-.2,ws(35)+.1)); gr['arm'][-1].rotation_euler=(R(-100*k+5*math.sin(t*10)*k),R(-26*k),0)
        for H in (y1,y2,bh): look_at(H,pw,1.0,maxyaw=70,maxpitch=30); face(H,mouth='o',brow=.06,eyes=1.2); H['root'].rotation_euler[0]=R(9)
        for s in (1,-1): y1['arm'][s].rotation_euler=(R(-58),R(s*10),0)
        crossed(y2); bh['arm'][1].rotation_euler=(R(-64),0,0)
        q=ease(t/DUR); camset(LV((.5,13.0,2.1),(.4,12.6,2.08),q),(.35,8.3,1.95),19,8)
    return dict(upd=upd)
SHOTS['LASTOVER']=LASTOVER
# ---------------------------------------------------------------- the cricket (what the TV shows)
def ball_of(H,s=1):
    return in_hand(H,s,lambda e: oico((0,-.08,-.02),.085,M('#B8232E',.4),e,sub=2))
def run_bowler(bw,t,y0,y1,x=1.0):
    walk_path(bw,[(x,y0),(x,y1)],t,-.2,DUR+.25,step=.7,run_=True,ease_in=.02,ease_out_=.02,arm=40); bw['root'].rotation_euler[0]=R(9); face(bw,mouth='strain',brow=-.03,brow_r=-14,eyes=1.0); blink(bw,t,force=0)
def BOWL():
    ground(); FILLE[0]=60; bw=mk(BOWLER,1.0,17,0,'bowler'); um=mk(UMPIRE,-1.5,11.8,0,'umpire'); stumps(0,10,90); ball_of(bw,1)
    def upd(t):
        run_bowler(bw,t,17.5,10.4); bw['arm'][1].rotation_euler=(R(-60+30*math.sin(t*13)),0,0)
        standp(um,t,-1.5,11.8,0); look_at(um,(0,-10,1.5),1.0); face(um,mouth='flat',brow=0,eyes=1.0); um['arm'][1].rotation_euler=(R(-20),0,0)
        q=t/DUR; camset((1.25,-3.0+.6*q,1.0),(1.0,L(17.5,10.4,q),1.75),85,8)
    return dict(upd=upd)
SHOTS['BOWLER']=BOWL
def BOWLER2():
    ground(); FILLE[0]=0; bw=mk(BOWLER,1.0,19,0,'bowler'); um=mk(UMPIRE,-1.5,11.8,0,'umpire'); bt=mk(BATTER,-.35,-9.3,180,'batter'); stumps(0,10,90); stumps(0,-10,90); ball_of(bw,1); bb=bat(bt,1)
    def upd(t):
        run_bowler(bw,t,19.5,11.0); bw['arm'][1].rotation_euler=(R(-60+30*math.sin(t*13)),0,0)
        standp(um,t,-1.5,11.8,0); standp(bt,t,-.35,-9.3,180); bt['root'].rotation_euler[0]=R(12); bt['arm'][1].rotation_euler=(R(-28+4*math.sin(t*10)),R(-14),0); bt['arm'][-1].rotation_euler=(R(-34),R(14),0)
        look_at(bt,hp(bw),1.0); q=ease(t/DUR); camset(LV((0,36,13.5),(0,33,12.6),q),(0,-2,1.2),72,8)
    return dict(upd=upd)
SHOTS['BOWLER2']=BOWLER2
# ---------------------------------------------------------------- the streets at night
NTOPS=dict(P=['#0B6B3C','#F4F1EA','#2F6B4F','#E8D2A0','#1E8A4A','#C9D6E8','#0B6B3C','#F2E9D0','#3F7A3A','#D9B08A'],I=['#1E73E8','#FF8A1E','#F4F1EA','#2B58C9','#E8B23A','#6FC3EA','#1E73E8','#FF9933','#C9D6E8','#27365A'])
def STREET(side):
    def f():
        pw=side=='I'; W=mohalla(side,night=True,pw=pw,seed=5 if side=='P' else 9,balcs=True,veh=False); FILLE[0]=0
        C=_fans(71 if side=='P' else 83,NTOPS[side],['#F4E9C8','#F2C14E','#E8A0B8'],'L' if side=='P' else 'K'); N=[]
        bl=sorted([(i['balc'],s) for s,k,i in W['blds'] if 'balc' in i and -4<i['x']<34],key=lambda v:v[0][0])[:8]; x0=min(v[0][0] for v in bl if v[1]==1)
        for j,((x,y,z),s) in enumerate(bl):
            H=mk(C[j%len(C)],x,y,0 if s==1 else 180,'n%d'%j,z=z); H['home']=(x,y,0 if s==1 else 180); H['ph']=j*1.3
            if not pw: H['tor']=phone_of(H,1); point((x,y-1.0*s,z+2.6),70,(.7,.82,1.0),r=.3,shadow=False)
            else: point((x,y-1.6*s,z+2.8),60,(1,.86,.62),r=.4,shadow=False)
            N.append(H)
        if not pw:
            for x in (2,14,26): point((x,0,6.5),520,(.6,.72,1.0),r=2,shadow=False)
        fw=[firework2((16,0,19),.12,'#FFE08A' if pw else '#9AE8A8',seed=3,rad=6),firework2((30,2,23),.5,'#FF9A6A' if pw else '#F4F6FA',seed=5,rad=6)]
        def upd(t):
            for H in N:
                x,y,rz=H['home']; standp(H,t,x,y,rz); arms_up(H,1,t,spread=20,jig=12); face(H,mouth='shout',brow=.06,eyes=1.15); H['root'].location[2]=H['z0']+.008+.32*abs(math.sin(t*8.5+H['ph']))
                look_at(H,(x+6,0,H['z0']+3),.6)
            for u_ in fw: u_(t)
            q=ease(t/DUR); camset(LV((x0-6.2,-2.2,4.2),(x0-5.6,-1.9,4.35),q),(x0+1.2,SY-1.0,5.75),26,8)
        return dict(upd=upd)
    return f
SHOTS['STREETP']=STREET('P'); SHOTS['STREETI']=STREET('I')
def KYA(side,a,b):
    def f():
        pw=side=='I'; W=mohalla(side,night=True,pw=pw,seed=5 if side=='P' else 9,hero=5,veh=False); FILLE[0]=34 if not pw else 14
        bx,by,bz=[i for s,k,i in W['blds'] if s==1 and k==5][0]['balc']; dad=mk(FAMC[side]['d'],bx,by,0,'kdad',z=bz)
        point((bx-1.5,by-4.5,bz+2.8),420 if not pw else 520,(.62,.74,1.0) if not pw else (1,.88,.68),r=1.5,shadow=False)
        def upd(t):
            standp(dad,t,bx,by-.15,0); dad['root'].rotation_euler[0]=R(11); what_pose(dad,1,t,amp=1.0); look_at(dad,(bx+5*math.sin(t*7),by-9,bz+1),1.0,maxyaw=50)
            face(dad,mouth='shout',brow=.06,eyes=1.25); speak(dad,t,a,b,gesture=False)
            q=ease(t/DUR); camset(LV((bx-1.9,by-7.4,3.2),(bx-1.7,by-7.0,3.3),q),(bx,by,bz+1.75),31,8)
        return dict(upd=upd)
    return f
SHOTS['KYAP']=KYA('P',242,243); SHOTS['KYAI']=KYA('I',244,245)
