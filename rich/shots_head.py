# ================================================================ KARACHI BARGAINER — shot table
_K=[('H_lane', 0), ('H_neg', 10), ('H_wal', 16), ('E_enter', 26), ('E_shirt', 42), ('D_how', 48), ('D_4000', 54), ('D_stare', 57), ('D_800', 61), ('D_shirt', 63), ('D_cust', 67), ('C_calc', 75), ('C_3500', 81), ('C_900', 85), ('C_3000', 87), ('C_950', 89), ('C_sweat', 91), ('C_please', 96), ('X_leave', 98), ('X_1500', 105), ('X_turn', 108), ('X_1000', 114), ('F_sky', 118), ('F_fine', 128), ('F_smile', 134), ('F_two', 136), ('F_TWO', 141), ('F_family', 142), ('B_watch', 147), ('B_how', 155), ('B_exp', 163), ('B_ruined', 164), ('O_walk', 170), ('O_end', 176), ('O_shop', 182)]
NW=186
IX=dict(_K)
_KS=[k for k,_ in _K]
def NX(key): j=_KS.index(key); return _K[j+1][1] if j+1<len(_K) else NW
def say(H,t,key,a=0,b=None,**kw): return talk(H,t,IX[key]+a,(NX(key)-1 if b is None else IX[key]+b),key,**kw)
SHOTS={}
WJ=json.load(open('/home/claude/rich/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
SEQ=[(k,0.0 if i==0 else round(WS[i]-.12,3)) for k,i in _K]
END=round(WE[-1]+1.2,3)
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
def L(a,b,q): return a+(b-a)*q
def cl(x): return max(0.0,min(1.0,x))
def headpos(H):
    bpy.context.view_layer.update(); return H['head'].matrix_world.translation.copy()
def cf(H,d=2.2,lat=.35,dz=0.0,lens=30,fs=3.5,tgt_dz=-.05):
    hp_=headpos(H); a=H['root'].rotation_euler[2]; fwd=Vector((math.sin(a),-math.cos(a),0)); rt=Vector((math.cos(a),math.sin(a),0))
    pos=hp_+fwd*d+rt*lat+Vector((0,0,dz)); tg=hp_+Vector((0,0,tgt_dz)); camset(tuple(pos),tuple(tg),lens,fs,focus=tuple(hp_))
def ots(A,Bh,back=1.1,side=.45,up=.1,lens=32,fs=3.0):
    """over A's shoulder looking at Bh's face"""
    side=math.copysign(max(abs(side),.8),side); back=max(back,1.3); lens=max(lens,36)
    a_=headpos(A); b_=headpos(Bh); d=(b_-a_); d.z=0; d.normalize(); rt=Vector((d.y,-d.x,0))
    pos=a_-d*back+rt*side+Vector((0,0,up)); camset(tuple(pos),tuple(b_+Vector((0,0,-.1))),lens,fs,focus=tuple(b_))
def put_at(H,t,x,y,rz,z=.0):
    H['root'].location=(x,y,z+.008); H['z0']=z; stand(H,t); H['root'].location[2]=z+.008; H['root'].rotation_euler[2]=R(rz); blink(H,t)
def seat(H,t,x,y,rz,sh=.47,z=0.0):
    blink(H,t); H['root'].location=(x,y,z+.008); H['root'].rotation_euler=(0,0,R(rz)); H['z0']=z; sit(H,1,sh+z,90)
def breathe(H,t): H['root'].scale=(1,1,1+.006*math.sin(t*2.2+H['seed']))
def phone_ear(H,s=1): H['arm'][s].rotation_euler=(R(-150),0,R(-28*s))
def phone_front(H,s=1,k=1.0): H['arm'][s].rotation_euler=(R(-85*k),0,R(-18*s*k))
def gesture(H,t,s=1,amp=1.0): H['arm'][s].rotation_euler=(R(-45*amp+10*math.sin(t*4)),0,R(-25*s*amp))

