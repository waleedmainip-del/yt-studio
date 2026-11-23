# ================================================================ KARACHI BARGAINER — shot table
_K=[('H_lane',0),('H_neg',10),('H_wal',16),('E_enter',23),('E_shirt',38),
    ('D_how',45),('D_4000',51),('D_stare',54),('D_800',60),('D_shirt',62),('D_cust',66),
    ('C_calc',74),('C_3500',79),('C_900',83),('C_3000',85),('C_950',87),('C_sweat',89),('C_please',94),
    ('X_leave',96),('X_1500',102),('X_turn',105),('X_1000',112),
    ('F_sky',116),('F_fine',126),('F_smile',132),('F_two',134),('F_TWO',139),('F_family',140),
    ('B_watch',145),('B_how',153),('B_exp',161),('B_ruined',162),('O_walk',168),('O_end',176),('O_shop',181)]
SHOTS={}
WJ=json.load(open('/home/claude/rich/audio/words.json')); WS=[w_['t0'] for w_ in WJ]; WE=[w_['t1'] for w_ in WJ]
_K=[('I_venue',0),('I_aunty',18),('I_uncle',25),('I_mehndi',34),('I_mistake',39),
    ('P_yaaro',57),('P_bhai',71),('P_bilkul',77),('P_tut',84),('P_haters',91),('P_move',96),('P_chair',109),
    ('S_dj',116),('S_ladies',121),('S_walk',130),('S_forget',137),('S_change',146),('S_which',149),('S_save',151),('S_rush',157),('S_fight',166),('S_street',178),
    ('A_watch',186),('A_ye',195),('A_pata',203),('A_kaisi',208),('A_beta',212),
    ('U_jump',219),('U_side',227),('U_dance',234),('U_who',247),('U_knees',252),('D_dadi',260),
    ('W_dj',271),('W_dadi',278),('W_crowd',279),('W_seven',283),('W_seventy',289),
    ('N_narr',297),('N_morning',310),('N_ammi',313),('N_tabiyat',322),('N_dadi',327),('N_bahar',337)]
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

