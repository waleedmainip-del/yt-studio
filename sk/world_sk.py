# Worlds for "Sialkot - Everyone Is an Exporter". All sets are new for this film:
#   bazaar()  sports bazaar with the clock tower      fb_workshop()  football stitching room      stadium()  night football stadium
#   scotland() highland knoll                         factory()      exporter's yard              airfield() field -> airport      homegate() Lahore house gate at night
MOODS['sk_day']=dict(sun=(56,-38),e=3.0,col=(1,.93,.8),top='#3A8CE4',bot='#D6ECFF',sky=.95,mist='#DCE8F2',cloud='#FFFFFF',cov=.5,cstr=.9)
MOODS['sk_gold']=dict(sun=(74,-52),e=2.3,col=(1,.74,.48),top='#4470C4',bot='#FFC488',sky=.9,mist='#EEC4A0',cloud='#FFD4B0',cov=.5,cstr=.85)
MOODS['sk_in']=dict(sun=(60,-160),e=.4,col=(1,.9,.8),top='#101018',bot='#1A1A24',sky=.3,mist='#1A1A24',cloud='#20202A',cov=.3,cstr=.5)
MOODS['sk_stad']=dict(sun=(50,-170),e=.8,col=(.75,.82,1.0),top='#050818',bot='#22326A',sky=.6,mist='#121A38',cloud='#1C2650',cov=.4,cstr=.6)
MOODS['sk_scot']=dict(sun=(62,140),e=2.1,col=(.92,.96,1.0),top='#6E90B4',bot='#DCE6EE',sky=.9,mist='#C8D4DC',cloud='#F4F6F8',cov=.78,cstr=.9)
MOODS['sk_night']=dict(sun=(58,-150),e=.6,col=(.6,.7,1.0),top='#060A1E',bot='#1C2850',sky=.6,mist='#161E3A',cloud='#232C52',cov=.4,cstr=.6)
SKY=5.4; BALLW='#F6F4EE'; BALLD='#1B1D24'; WILLOW='#E8D2A0'
PD=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(.58,.58,.58),(-.58,.58,.58),(.58,-.58,.58),(-.58,-.58,.58),(.58,.58,-.58),(-.58,-.58,-.58)]
def spotd(loc,e,col,size=80,blend=.6,shadow=True,r=.5):
    bpy.ops.object.light_add(type='SPOT',location=loc); p=bpy.context.object; p.data.energy=e; p.data.color=col; p.data.spot_size=R(size); p.data.spot_blend=blend
    p.data.shadow_soft_size=r; p.data.use_shadow=shadow; return p
# ---------------------------------------------------------------- goods
def ball_b(x,y,z,r=.26,c2=BALLD,n=6):
    B.ico((x,y,z),r,M(BALLW,.45),sub=2)
    for d in PD[:n]: B.ico((x+d[0]*r*.8,y+d[1]*r*.8,z+d[2]*r*.8),r*.3,M(c2,.5),sub=1)
def ball_o(loc=(0,0,-5),r=.26,parent=None,c2=BALLD):
    e=empty(loc,parent); oico((0,0,0),r,M(BALLW,.45),e,sub=2)
    for d in PD: oico((d[0]*r*.8,d[1]*r*.8,d[2]*r*.8),r*.3,M(c2,.5),e,sub=1)
    return e
def bat_b(x,y,z,grip='#C8372D',rz=0):
    B.box((x,y,z),(.13,.035,.5),M(WILLOW,.6,kind='wood'),.02,rot=(0,0,R(rz))); B.cyl((x,y,z+.72),.04,.46,M(grip,.7),seg=8)
def bat_o(parent=None,grip='#C8372D'):
    """bat held by the handle: origin at the grip, blade hanging down (-z)"""
    e=empty((0,0,-5),parent); obox((0,0,-.74),(.13,.035,.5),M(WILLOW,.6,kind='wood'),.02,e); ocyl((0,0,-.02),.04,.46,M(grip,.7),e,rot=(0,0,0),seg=8); return e
def stick_b(x,y,z,col='#2B58C9',rz=0):
    B.cyl((x,y,z),.035,1.5,M(col,.5),seg=8); B.box((x+.11*math.cos(R(rz)),y+.11*math.sin(R(rz)),z-.78),(.14,.035,.05),M('#F2EBDA',.6),.02,rot=(0,0,R(rz)))
def bagpipe_b(x,y,z,s=1.0,tc='#B8232E'):
    B.ico((x,y,z),.3*s,M(tc,.8,kind='fabric'),sc=(1.25,.75,.85),sub=2); B.box((x,y-.02*s,z),(.37*s,.21*s,.03*s),M('#1E4A2E',.8),0); B.box((x,y-.02*s,z),(.03*s,.21*s,.25*s),M('#1E4A2E',.8),0)
    for k,dx in enumerate((-.18,0,.18)):
        h=(.95 if k==0 else .7)*s; B.cyl((x+dx*s,y,z+.2*s+h/2),.03*s,h,M('#2A1A12',.4),seg=8); B.cyl((x+dx*s,y,z+.2*s+h),.05*s,.07*s,M('#F2E9D0',.4),seg=8)
    B.cyl((x+.32*s,y,z-.32*s),.028*s,.5*s,M('#2A1A12',.4),seg=8,rot=(0,R(25),0))
def bagpipe_o(parent=None,s=1.0,tc='#B8232E',tag=False):
    """bagpipe as one object: origin at the bag. drones go up (+z), chanter down. tag = cream label 'MADE IN SIALKOT' on the front (-y) of the bag"""
    e=empty((0,0,-5),parent); oico((0,0,0),.3*s,M(tc,.8,kind='fabric'),e,sc=(1.25,.75,.85),sub=2); obox((0,-.02*s,0),(.37*s,.21*s,.03*s),M('#1E4A2E',.8),0,e); obox((0,-.02*s,0),(.03*s,.21*s,.25*s),M('#1E4A2E',.8),0,e)
    for k,dx in enumerate((-.18,0,.18)):
        h=(.95 if k==0 else .7)*s; ocyl((dx*s,0,.2*s+h/2),.03*s,h,M('#2A1A12',.4),e,rot=(0,0,0),seg=8); ocyl((dx*s,0,.2*s+h),.05*s,.07*s,M('#F2E9D0',.4),e,rot=(0,0,0),seg=8)
    ocyl((.3*s,-.12*s,-.38*s),.028*s,.55*s,M('#2A1A12',.4),e,rot=(R(-12),R(20),0),seg=8); ocyl((.02*s,-.2*s,.34*s),.022*s,.34*s,M('#2A1A12',.4),e,rot=(R(-35),0,0),seg=8)
    if tag:
        obox((-.02*s,-.245*s,-.02*s),(.2*s,.006,.085*s),M('#F6F0DC',.7),0,e); text('MADE IN SIALKOT',(-.02*s,-.256*s,-.02*s),(0,-1,0),.045*s,M('#16171C',.5),ex=.002,parent=e)
    return e
def carton_b(x,y,z,w=.5,d=.4,h=.36,label=None,n=(0,-1,0),col='#C9A26A',size=None):
    B.box((x,y,z+h),(w,d,h),M(col,.85),.015); B.box((x,y,z+2*h-.004),(w*.16,d,.006),M('#B88A52',.8),0)
    if label:
        nv=Vector(n); p=Vector((x,y,z+h))+Vector((nv.x*(w+.006),nv.y*(d+.006),0)); text(label,tuple(p),n,size or min(.2,1.5*(w if abs(nv.y)>.5 else d)/max(4,len(label))),M('#3A2A1E',.6),ex=.003)
def handcart(x,y,rz=0):
    e=empty((x,y,0),rot=(0,0,R(rz))); wd=M('#8A6A46',.8,kind='wood'); obox((0,0,.62),(1.0,.6,.05),wd,.02,e)
    for sy in (-.66,.66): wheel((0,sy,.34),.34,.07,e)
    obox((1.25,0,.72),(.3,.03,.03),wd,.01,e); obox((1.25,.5,.72),(.3,.03,.03),wd,.01,e); obox((1.25,-.5,.72),(.3,.03,.03),wd,.01,e); obox((1.53,0,.72),(.03,.53,.03),wd,.01,e)
    obox((-.7,.4,.3),(.04,.04,.3),wd,.01,e); obox((-.7,-.4,.3),(.04,.04,.3),wd,.01,e)
    return e
# ---------------------------------------------------------------- set A: the bazaar
def goods(cx,y0,s,kind,r):
    wd=M('#7A5A3A',.8,kind='wood'); yb=y0+s*3.05; n=(0,-s,0)
    if kind=='balls':
        for row in range(4):
            B.box((cx,yb-s*.2,1.0+row*.72),(2.4,.26,.03),wd,0)
            for k in range(8): ball_b(cx-2.1+k*.6,yb-s*.2,1.3+row*.72,.25,[BALLD,'#B8232E','#2B58C9','#1E6A3A'][(k+row)%4])
        for k in range(5): B.cyl((cx-2.0+k*1.0,y0+s*.25,3.1),.012,.9,M('#2A2C34',.6),seg=4); ball_b(cx-2.0+k*1.0,y0+s*.25,2.42,.27,[BALLD,'#B8232E','#2B58C9'][k%3])
        B.box((cx-1.6,y0+s*.75,.5),(.8,.45,.5),wd,.03)
        for k,(dx,dz) in enumerate(((-.5,0),(0,0),(.5,0),(-.25,.44),(.25,.44),(0,.88))): ball_b(cx-1.6+dx,y0+s*.75,1.26+dz,.26,[BALLD,'#B8232E','#2B58C9'][k%3])
    elif kind=='bats':
        for row in range(2):
            B.box((cx,yb-s*.08,1.9+row*1.45),(2.45,.05,.04),wd,0)
            for k in range(10): bat_b(cx-2.15+k*.478,yb-s*.14,1.25+row*1.45,['#C8372D','#2B58C9','#1E6A3A','#E6B53A','#16171C'][(k+row)%5])
        B.cyl((cx+1.9,y0+s*.7,.45),.38,.9,M('#5A7FB0',.6),seg=12)
        for k in range(5): bat_b(cx+1.9+.22*math.cos(k*1.3),y0+s*.7+.22*math.sin(k*1.3),1.05,['#C8372D','#E6B53A','#2B58C9'][k%3],rz=k*40)
        B.box((cx-1.5,y0+s*.8,.55),(.9,.4,.55),wd,.03); B.box((cx-1.5,y0+s*.8,1.12),(1.0,.46,.03),M('#F2EBDA',.6),.01)
        for k in range(3): B.box((cx-2.1+k*.6,y0+s*.8,1.2),(.2,.13,.06),M(['#F4F1EA','#C8372D','#2B58C9'][k],.6),.03)
    elif kind=='hockey':
        B.box((cx-1.4,yb-s*.1,1.5),(1.0,.05,.04),wd,0); B.box((cx-1.4,yb-s*.1,.25),(1.0,.2,.25),wd,.02)
        for k in range(9): stick_b(cx-2.25+k*.21,yb-s*.2,1.25,['#2B58C9','#C8372D','#16171C','#E6B53A','#1E6A3A'][k%5],rz=-90*s)
        B.box((cx+1.25,yb-s*.06,2.0),(1.15,.04,1.2),M('#F2EBDA',.7),0)
        for i in range(4):
            for j in range(3):
                gc=['#C8372D','#2B58C9','#F2C14E','#16171C','#1E6A3A','#F28A3A'][(i+j*2)%6]
                for q in (-.13,.13): B.box((cx+.4+i*.57+q,yb-s*.13,1.25+j*.75),(.1,.05,.2),M(gc,.7,kind='fabric'),.04); B.box((cx+.4+i*.57+q,yb-s*.13,1.02+j*.75),(.11,.055,.06),M('#F4F1EA',.7),.02)
        for k in range(3): B.ico((cx-.2+k*.5,y0+s*.7,1.3),.2,M(['#2B58C9','#C8372D','#16171C'][k],.35),sc=(1,1.15,.9),sub=2)
        B.box((cx+.3,y0+s*.7,.55),(1.0,.4,.55),wd,.03)
    elif kind=='pipes':
        for k in range(5): bagpipe_b(cx-2.0+k*1.0,yb-s*.3,2.05,.95,['#B8232E','#1E4A7A','#1E6A3A','#B8232E','#5A2A7A'][k]); B.box((cx-2.0+k*1.0,yb-s*.1,2.9),(.05,.08,.05),wd,0)
        B.box((cx-1.3,y0+s*.9,.5),(1.1,.45,.5),wd,.03)
        for k in range(4): B.cyl((cx-2.0+k*.45,y0+s*.9,1.06),.035,.9,M('#2A1A12',.4),seg=8,rot=(0,R(90),0))
        for k in range(3): B.cyl((cx+1.6,y0+s*(.6+k*.3),.3+k*.02),.18,1.4,M(['#B8232E','#1E4A7A','#1E6A3A'][k],.8,kind='fabric'),seg=10,rot=(0,R(90),0))
    elif kind=='chai':
        B.box((cx,y0+s*.55,.62),(2.3,.4,.62),M('#3E7A6A',.6),.03); B.box((cx,y0+s*.55,1.27),(2.4,.48,.035),M('#D8D2C4',.4,metal=.3),.01)
        B.box((cx-1.3,y0+s*.6,1.42),(.4,.3,.12),M('#3A3D44',.5,metal=.5),.02); B.cyl((cx-1.3,y0+s*.6,1.78),.3,.5,M('#C9CED8',.25,metal=.9),seg=14,r2=.2); B.cyl((cx-1.3,y0+s*.6,2.08),.06,.1,M('#16171C',.5),seg=8)
        B.cyl((cx-.95,y0+s*.5,1.86),.03,.34,M('#C9CED8',.25,metal=.9),seg=6,rot=(0,R(60),0))
        for k in range(6): B.cyl((cx+.2+(k%3)*.26,y0+s*(.45+(k//3)*.24),1.36),.09,.14,M('#F4F1EA',.4),seg=10,r2=.075)
        for k in range(3): B.cyl((cx+1.5+k*.3,y0+s*.6,1.48),.13,.36,M(['#E8B45A','#C8662C','#F2E3C4'][k],.3,alpha=1.0),seg=10); B.cyl((cx+1.5+k*.3,y0+s*.6,1.69),.14,.06,M('#C8372D',.5),seg=10)
        for row in range(2):
            B.box((cx,yb-s*.2,1.6+row*.8),(2.3,.24,.03),wd,0)
            for k in range(9): B.box((cx-2.0+k*.5,yb-s*.2,1.82+row*.8),(.16,.14,.19),M(['#C8372D','#F2C14E','#2E8A3E','#2B58C9','#F28A3A'][(k+row)%5],.6),.02)
    else:
        for row in range(3):
            B.box((cx,yb-s*.2,.9+row*.85),(2.4,.26,.03),wd,0)
            for k in range(7): B.box((cx-2.1+k*.7,yb-s*.2,1.16+row*.85),(.26,.2,.22),M(r.choice(['#8A5A3A','#2A3550','#6B1F2E','#3A6A5A','#C9A26A','#16171C','#B8A070']),.7,kind='fabric'),.03)
        B.box((cx,y0+s*.8,.5),(1.6,.42,.5),wd,.03)
def shop(cx,s,kind,sg,col,fl=2,seed=0,w=6.0,light=True):
    r=random.Random(seed); y0=s*SKY; G=3.9; H=G+fl*3.0; dep=8.0; yc=y0+s*dep/2; wall=M(col,.85,kind='wall'); tr=M('#F2EBDA',.8); n=(0,-s,0)
    B.box((cx,yc,(G+H)/2),(w/2-.03,dep/2,(H-G)/2),wall,0)
    for q in (-1,1): B.box((cx+q*(w/2-.22),yc,G/2),(.2,dep/2,G/2),wall,0)
    B.box((cx,y0+s*3.25,G/2),(w/2-.4,.1,G/2),M(shade(col,.72),.9),0); B.box((cx,y0+s*1.6,.06),(w/2-.4,1.65,.06),M('#8A8078',.8,kind='tile',sc=.8),0)
    B.box((cx,y0-s*.1,G-.22),(w/2-.05,.14,.22),tr,.02)
    sz=.34 if len(sg[0])<13 else (.27 if len(sg[0])<19 else .215)
    sign(sg[0],(cx,y0-s*.32,G+.6),sz,sg[2] if len(sg)>2 else '#FFF6D8',sg[1],n=n,pad=.14,th=.1,frame='#E6B53A')
    ac=r.choice(['#C8372D','#2B58C9','#1E6A3A','#D9811A','#7448C2','#0E7C74']); n_=5
    for j in range(n_): B.box((cx-w/2+.3+(j+.5)*(w-.6)/n_,y0-s*.9,G-.48),((w-.6)/n_/2,.8,.02),M(ac if j%2 else '#F4F1EA',.85,kind='fabric'),.004,rot=(R(-12*s),0,0))
    for f in range(fl):
        for q in (-1.7,0,1.7):
            B.box((cx+q,y0-s*.02,G+1.75+f*3.0),(.5,.05,.7),M('#27344A',.3,spec=.8),0); B.box((cx+q,y0-s*.06,G+.98+f*3.0),(.62,.09,.05),tr,0)
            for qq in (-1,1): B.box((cx+q+qq*.56,y0-s*.05,G+1.75+f*3.0),(.05,.04,.72),M(r.choice(['#2E6A5A','#5A3A22','#3A5A8A']),.7),0)
    B.box((cx,yc,H+.12),(w/2+.05,dep/2+.05,.12),tr,0)
    if r.random()<.6: B.cyl((cx+r.uniform(-1.5,1.5),yc,H+.9),.55,1.1,M(r.choice(['#16171C','#2B58C9','#F4F1EA']),.5),seg=12)
    goods(cx,y0,s,kind,r)
    if light: point((cx,y0+s*1.5,3.3),260,(1,.9,.72),r=.6,shadow=False)
    return H
NSHOP=[(-17,'gen',('LEATHER JACKETS','#3A2A1E')),(-11,'chai',('SIALKOTI CHAI','#B8232E')),(-5,'balls',('CHAMPION FOOTBALL CO.','#1E4A7A')),(1,'bats',('SIALKOT BAT HOUSE','#1E6A3A')),
       (7,'hockey',('IQBAL SPORTS','#7448C2')),(13,'pipes',('HIGHLAND BAGPIPE WORKS','#5A1626')),(19,'gen',('SURGICAL INSTRUMENTS','#0E5A74')),(25,'gen',('EXPORT QUALITY GLOVES','#8A4A1E'))]
SSHOP=[(-17,'gen',('KASHMIR CLOTH HOUSE','#7A1F2E')),(-11,'gen',('PUNJAB CARGO','#2A3550')),(-5,'gen',('STAR TAILORS','#0E7C74')),(1,'gen',('CITY SPORTS','#B8232E')),
       (7,'gen',('ALLAMA BOOK DEPOT','#1E6A3A')),(13,'gen',('RIAZ CYCLE WORKS','#D9811A')),(19,'gen',('DOABA SWEETS','#7448C2')),(25,'gen',('FAUJI TRUNK HOUSE','#3A5A2A'))]
WALLC=['#C9825A','#E0C8A0','#B86A4A','#D8B48C','#C9A27A','#A8563A','#E6D6BE','#BF7A52']
def clock_tower(x,y):
    br=M('#B8573A',.85,kind='wall'); cr=M('#F2E9D0',.7); B.box((x,y,.5),(3.2,3.2,.5),M('#8A8078',.8),.05); B.box((x,y,6.5),(2.0,2.0,5.5),br,.03)
    for z in (4.2,8.2,11.9): B.box((x,y,z),(2.14,2.14,.14),cr,.03)
    for a in range(4):
        dx,dy=[(0,-1),(1,0),(0,1),(-1,0)][a]; B.box((x+dx*2.02,y+dy*2.02,2.4),(.55 if dy else .04,.55 if dx else .04,1.0),M('#3A2418',.6,kind='wood'),.02)
        B.box((x+dx*2.02,y+dy*2.02,6.2),(.5 if dy else .04,.5 if dx else .04,.9),M('#27344A',.3),.02)
    B.box((x,y,14.0),(2.25,2.25,2.0),cr,.04)
    for a in range(4):
        dx,dy=[(0,-1),(1,0),(0,1),(-1,0)][a]; rt=(R(90),0,0) if dy else (0,R(90),0)
        B.cyl((x+dx*2.29,y+dy*2.29,14.0),1.42,.06,M('#FBF8EE',.5),rot=rt,seg=28); B.cyl((x+dx*2.26,y+dy*2.26,14.0),1.58,.05,M('#2A2C34',.5),rot=rt,seg=28)
        B.box((x+dx*2.33,y+dy*2.33,14.42),((.035 if dy else .02),(.035 if dx else .02),.5),M('#16171C',.5),0)
        B.box((x+dx*2.33+(.3 if dy else 0),y+dy*2.33+(.3 if dx else 0),14.0),((.33 if dy else .02),(.33 if dx else .02),.035),M('#16171C',.5),0)
    B.box((x,y,16.2),(2.45,2.45,.2),cr,.04); B.box((x,y,17.1),(1.3,1.3,.8),br,.03); B.ico((x,y,18.3),1.25,M('#2E6A5A',.5,metal=.3),sc=(1,1,.85),sub=2); B.cyl((x,y,19.8),.05,1.4,M('#E6B53A',.3,metal=.8),seg=6)
    B.cyl((x,y,.2),7.0,.4,M('#9A9088',.8),seg=28)
    for k in range(16): a=k*pi/8; B.ico((x+5.6*math.cos(a),y+5.6*math.sin(a),.75),.42,M(['#E8554D','#F2C14E','#F2A0B8','#4F8A3A'][k%4],.8,kind='leaves'),sub=1)
def bazaar(mood='sk_day',lights=True):
    NIGHT[0]=0.0; S=setup_world(mood,shadow=70); r=random.Random(11)
    B.box((0,0,-.1),(90,40,.1),M('#4A4744',.9,kind='concrete',sc=1.6),0)
    for s in (1,-1): B.box((0,s*4.4,.09),(60,1.0,.09),M('#B88A6A',.85,kind='tile',sc=.7),0); B.box((0,s*3.42,.11),(60,.06,.11),M('#8A8078',.8),0)
    for i,(cx,kind,sg) in enumerate(NSHOP): shop(cx,1,kind,sg,WALLC[i%8],fl=2+(i%3==1),seed=20+i,light=lights)
    for i,(cx,kind,sg) in enumerate(SSHOP): shop(cx,-1,kind,sg,WALLC[(i+3)%8],fl=2+(i%2),seed=40+i,light=False)
    for s in (1,-1):
        for cx in (-23,-29,31): shop(cx,s,'gen',('SIALKOT TRADERS' if cx<0 else 'CHOWK MEDICAL','#3A3A44'),WALLC[(cx+s)%8],fl=3,seed=cx+60+s,light=False)
    clock_tower(40,0)
    for k in range(70):
        x=r.uniform(-44,58); y=r.choice((-1,1))*r.uniform(15,52); w=r.uniform(2.5,5); d=r.uniform(2.5,5); h=r.uniform(4,11); c=r.choice(WALLC)
        if abs(x-40)<9 and abs(y)<20: continue
        B.box((x,y,h/2),(w,d,h/2),M(c,.9,kind='wall'),0); B.box((x,y,h+.1),(w+.1,d+.1,.1),M('#F2EBDA',.8),0)
        if k%3==0: B.cyl((x+w*.4,y,h+.8),.5,1.0,M(r.choice(['#16171C','#2B58C9','#F4F1EA']),.5),seg=10)
        if k%7==0: B.cyl((x,y,h+2.6),.5,5.0,M('#F2E9D0',.7),seg=8); B.ico((x,y,h+5.4),.7,M('#2E6A5A',.5),sc=(1,1,1.2),sub=2)
    for k,x in enumerate((-15,-6,3,12)):                                          # cloth shades strung high across the lane
        c=['#E8554D','#F2C14E','#2E8AD8','#6FC38A'][k]
        B.box((x,0,8.9-.25*(k%2)),(1.25,5.3,.02),M(c,.85,kind='fabric'),0,rot=(0,R(5 if k%2 else -5),0))
    for x in (-21,-3,15):
        for s in (1,-1): B.cyl((x,s*3.7,4.0),.1,8.0,M('#6E7378',.5,metal=.4),seg=8); B.box((x,s*3.7,7.6),(.9,.05,.05),M('#4A4E56',.5),0)
    for sy in (-3.7,3.7): B.cyl((0,sy,7.72),.014,54,M('#16171C',.6),seg=4,rot=(0,R(90),0))
    for (x,y) in ((-14.5,3.9),(4.2,3.9),(22,3.9),(-8,-3.9),(10,-3.9),(16.2,-3.9)):
        B.cyl((x,y,.35),.32,.5,M('#B8573A',.8),seg=10,r2=.26); B.ico((x,y,.95),.5,M(r.choice(['#4F8A3A','#3F7A3A','#5F9A4A']),.85,kind='leaves'),sub=1)
    for i,(x,y,lab) in enumerate(((-7.6,3.95,'EXPORT'),(-7.6,3.95,None),(9.9,3.9,'EXPORT'))):
        if lab or i!=1: carton_b(x,y,.18+(.72 if i==1 else 0),.42,.34,.3,lab,n=(0,-1,0))
    carton_b(-8.5,3.95,.18,.42,.34,.3,'FRAGILE'); carton_b(-8.05,3.95,.78,.42,.34,.3,'EXPORT')
    B.done('bazaar'); return S
# ---------------------------------------------------------------- set B: football stitching workshop
def fb_workshop():
    """room x -5.2..5.2, y -4..4.2 (open towards -y for the camera). stitcher's stool at (1.7,1.1). returns dict(lights)"""
    NIGHT[0]=1.0; S=setup_world('sk_in',shadow=30); br=M('#B8765A',.85,kind='wall'); wd=M('#7A5A3A',.8,kind='wood'); r=random.Random(5)
    B.box((0,0,-.1),(7,6,.1),M('#8A8078',.85,kind='concrete',sc=.8),0); B.box((0,4.3,2.2),(5.3,.1,2.2),br,0)
    for sx in (-1,1): B.box((sx*5.3,0,2.2),(.1,4.3,2.2),br,0)
    B.box((0,0,4.5),(5.4,4.4,.1),M('#8A8274',.9),0); B.box((0,4.18,.55),(5.2,.04,.55),M('#2E6A6A',.7),0)
    for q in (-2.6,2.6): B.box((q,0,4.3),(.12,4.3,.12),wd,0)
    B.box((-1.6,-.6,.012),(2.2,1.5,.012),M('#8A3A3A',.9,kind='fabric',sc=.5),0); B.box((-1.6,-.6,.02),(1.9,1.2,.012),M('#C9A26A',.9,kind='fabric',sc=.5),0)
    for i,(x,y,z) in enumerate(((-4.3,-1.2,0),(-4.3,-1.2,.72),(-4.35,-2.3,0))): carton_b(x,y,z+.02,.5,.48,.36,'EXPORT' if i==1 else None,n=(1,0,0))
    B.box((-5.16,2.9,2.6),(.03,.5,.7),M('#F4F1EA',.7),0); B.box((-5.14,2.9,2.95),(.02,.42,.22),M('#1E6A3A',.7),0)
    B.cyl((-2.6,0,4.15),.05,.5,M('#3A3D44',.5),seg=6)
    for a in range(3): B.box((-2.6+.75*math.cos(a*2.094),.75*math.sin(a*2.094),3.9),(.75,.13,.02),M('#D8D2C4',.5),0,rot=(0,0,a*2.094))
    for sx in (-1,1): B.box((sx*5.18,0,.55),(.04,4.2,.55),M('#2E6A6A',.7),0)
    for row in range(4):                                                         # the wall of finished footballs
        B.box((-.6,3.9,1.0+row*.74),(3.9,.3,.035),wd,0)
        for k in range(13):
            if (row,k)!=(2,7): ball_b(-4.2+k*.6,3.9,1.3+row*.74,.25,[BALLD,'#B8232E','#2B58C9','#1E6A3A','#F28A3A'][(k*2+row)%5])
    for q in (-4.5,-.6,3.3): B.box((q,3.9,1.9),(.05,.3,1.9),wd,0)
    B.box((4.2,4.14,2.5),(.75,.04,.9),M('#BFE0F4',.2,emit=1.6),0)                 # window
    for q in (-1,0,1): B.box((4.2+q*.75,4.1,2.5),(.04,.05,.94),wd,0)
    B.box((4.2,4.1,2.5),(.79,.05,.04),wd,0)
    for i,(x,y,z,lab) in enumerate(((4.4,2.0,0,'MADE IN PAKISTAN'),(4.4,2.0,.72,'MADE IN PAKISTAN'),(4.4,.95,0,'EXPORT'),(4.4,.95,.72,None),(4.4,2.0,1.44,None))):
        carton_b(x,y,z+.02,.5,.48,.36,lab,n=(-1,0,0),size=.085 if lab and len(lab)>8 else .16)
    B.box((1.7,.25,.36),(.75,.38,.04),wd,.02)                                    # low work bench in front of the stool
    for q in ((-.65,-.3),(.65,-.3),(-.65,.3),(.65,.3)): B.box((1.7+q[0],.25+q[1],.17),(.04,.04,.17),wd,.01)
    B.cyl((1.7,1.1,.28),.3,.56,wd,seg=12); B.cyl((1.7,1.1,.57),.33,.05,M('#B8232E',.8,kind='fabric'),seg=12)
    for k in range(5): B.box((1.15+k*.14,.2,.42),(.06,.07,.012),M([BALLW,BALLD,'#B8232E'][k%3],.6),0,rot=(0,0,R(k*17)))
    B.cyl((2.25,.3,.47),.08,.14,M('#C9A26A',.6),seg=10); B.cyl((2.25,.3,.6),.012,.16,M('#C9CED8',.3,metal=.8),seg=4)
    B.cyl((-3.6,2.6,.3),.5,.6,M('#8A6A46',.8),seg=12)
    for k in range(5): ball_b(-3.6+.26*math.cos(k*1.3),2.6+.26*math.sin(k*1.3),.72+.06*(k%2),.24,[BALLD,'#B8232E','#2B58C9'][k%3])
    B.cyl((.4,1.6,4.0),.012,.9,M('#16171C',.6),seg=4); B.ico((.4,1.6,3.5),.13,M('#FFE2A8',.3,emit=7.0),sub=2); B.cyl((.4,1.6,3.62),.22,.14,M('#2E6A5A',.5,metal=.3),seg=12,r2=.08)
    B.box((-5.16,.4,1.7),(.04,.9,1.7),M('#5A3A22',.7,kind='wood'),.02); B.box((-5.14,.4,1.7),(.03,.75,1.55),M('#FFE9C0',.3,emit=1.2),0)   # doorway, daylight outside
    B.box((0,-4.4,2.2),(5.3,.1,2.2),br,0); B.box((0,-4.28,.55),(5.2,.04,.55),M('#2E6A6A',.7),0)        # front wall (cameras stay inside the room)
    for row in range(2):
        B.box((-2.9,-4.1,1.5+row*.8),(1.9,.22,.035),wd,0)
        for k in range(9): B.cyl((-4.5+k*.4,-4.1,1.72+row*.8),.11,.36,M(['#F4F1EA','#B8232E','#2B58C9','#16171C','#F2C14E'][(k+row)%5],.6),seg=10,r2=.05)
    B.box((2.4,-4.26,2.5),(.75,.04,.9),M('#BFE0F4',.2,emit=1.6),0)
    for q in (-1,0,1): B.box((2.4+q*.75,-4.22,2.5),(.04,.05,.94),wd,0)
    B.box((2.4,-4.22,2.5),(.79,.05,.04),wd,0)
    for i,(x,y,z) in enumerate(((4.3,-3.5,0),(4.3,-3.5,.72),(4.35,-2.4,0))): carton_b(x,y,z+.02,.5,.48,.36,None)
    B.cyl((-.6,-4.24,3.2),.34,.05,M('#F4F1EA',.5),seg=20,rot=(R(90),0,0)); B.box((-.6,-4.2,3.3),(.012,.01,.1),M('#16171C',.5),0); B.box((-.52,-4.2,3.2),(.08,.01,.012),M('#16171C',.5),0)
    B.done('fbw')
    L=[point((.4,1.6,2.9),380,(1,.86,.62),r=.5,shadow=True),point((-2.5,-1.5,2.6),380,(1,.9,.76),r=1.5,shadow=False),point((3.4,3.2,2.6),260,(.8,.9,1.0),r=.8,shadow=False),
       point((1.6,-2.6,2.2),200,(1,.9,.8),r=1.5,shadow=False)]
    return dict(L=L)
# ---------------------------------------------------------------- set C: the stadium
def stadium():
    """pitch along y, goal at y=+26 (goal line), centre spot at the origin"""
    NIGHT[0]=1.0; S=setup_world('sk_stad',shadow=80); wl=M('#F8F8F4',.6)
    B.box((0,0,-.3),(140,140,.2),M('#0E2A16',.9),0)
    for k in range(13): B.box((0,-30+k*5,-.02+.001*(k%2)),(24,2.5,.02),M('#2E8A3E' if k%2 else '#37993F',.85),0)
    B.box((0,0,.012),(22,.07,.006),wl,0)
    for k in range(40): a=k*2*pi/40; B.box((5*math.cos(a),5*math.sin(a),.012),(.4,.07,.006),wl,0,rot=(0,0,a+pi/2))
    B.cyl((0,0,.014),.16,.01,wl,seg=10)
    for sx in (-1,1): B.box((sx*22,0,.012),(.07,26,.006),wl,0); B.box((sx*10,21,.012),(.07,5,.006),wl,0); B.box((sx*4.5,24.2,.012),(.07,1.8,.006),wl,0)
    B.box((0,26,.012),(22,.07,.006),wl,0); B.box((0,16,.012),(10,.07,.006),wl,0); B.box((0,22.4,.012),(4.5,.07,.006),wl,0); B.cyl((0,19.5,.014),.14,.01,wl,seg=8)
    gp=M('#FAFAFA',.4)                                                             # goal: posts, bar, net
    for sx in (-1,1): B.cyl((sx*4.0,26,1.6),.09,3.2,gp,seg=8); B.cyl((sx*4.0,28.2,.9),.05,1.8,gp,seg=6)
    B.cyl((0,26,3.2),.09,8.1,gp,seg=8,rot=(0,R(90),0)); nm=M('#E8ECF0',.7)
    for k in range(17): B.box((-4+k*.5,27.1,2.45),(.012,1.25,.012),nm,0,rot=(R(-33),0,0)); B.box((-4+k*.5,28.2,.9),(.012,.012,.9),nm,0)
    for k in range(7): B.box((0,28.2,.15+k*.27),(4.0,.012,.012),nm,0)
    for k in range(5): B.box((0,26.3+k*.42,3.05-k*.28),(4.0,.012,.012),nm,0)
    for sx in (-1,1):
        for k in range(6): B.box((sx*4.0,26.3+k*.38,1.5-k*.1),(.012,.012,1.5-k*.1),nm,0)
    cc=['#E8554D','#4D8FE8','#F2C14E','#6FC38A','#F4F1DE','#9B6FD0','#FF8A3A','#2A2C34','#D8A0B8']; r=random.Random(3)
    def stand(cx,cy,ax,L_):                                                        # ax: 0 = runs along x, 1 = along y ; stepped tiers with crowd confetti
        for t_ in range(9):
            off=3.2+t_*1.5; z=1.2+t_*1.25
            if ax==0: B.box((cx,cy+off*(1 if cy>0 else -1),z/2),(L_,.78,z/2),M('#20283C',.8),0)
            else: B.box((cx+off*(1 if cx>0 else -1),cy,z/2),(.78,L_,z/2),M('#20283C',.8),0)
            for k in range(int(L_*2/.62)):
                if r.random()<.86:
                    u_=-L_+.3+k*.62; c=M(r.choice(cc),.8);
                    if ax==0: B.box((cx+u_,cy+off*(1 if cy>0 else -1),z+.33),(.2,.18,.33),c,.04)
                    else: B.box((cx+off*(1 if cx>0 else -1),cy+u_,z+.33),(.18,.2,.33),c,.04)
        if ax==0: B.box((cx,cy+1.7*(1 if cy>0 else -1),.5),(L_,.08,.5),lit('#1E4A7A',1.2,always=True),0)
        else: B.box((cx+1.7*(1 if cx>0 else -1),cy,.5),(.08,L_,.5),lit('#B8323A',1.2,always=True),0)
    stand(0,29,0,26); stand(24,0,1,30); stand(-24,0,1,30); stand(0,-33,0,26)
    for (x,y) in ((-30,40),(30,40),(-30,-40),(30,-40)):
        B.cyl((x,y,13),.5,26,M('#8A8E96',.5,metal=.5),seg=8); B.box((x,y,27),(3.4,.4,2.0),M('#3A3D44',.5),.05,rot=(0,0,math.atan2(-x,y)+pi/2))
        for i in range(5):
            for j in range(3): B.ico((x+(i-2)*1.3*abs(math.cos(math.atan2(-x,y)+pi/2))-(.5*(1 if y>0 else -1)),y-(1 if y>0 else -1)*.5,25.6+j*1.3),.42,M('#FFFFFF',.3,emit=9.0),sub=1)
    B.done('stad')
    L=[point((0,8,22),26000,(1,.98,.94),r=3.0,shadow=True),point((-16,24,16),9000,(.95,.97,1.0),r=3.0,shadow=False),point((16,24,16),9000,(.95,.97,1.0),r=3.0,shadow=False),
       point((0,-14,18),12000,(1,.98,.94),r=3.0,shadow=False),point((0,34,9),3500,(1,.95,.9),r=2.0,shadow=False)]
    return dict(L=L)
