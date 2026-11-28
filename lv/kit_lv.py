# Kit for the Lahore vampire-prince film: prince (silver circlet, blue cape, gold lining), queen (crown, plum cape), generic vampires, mithai box, poster, coffin.
def _ears(H,C):
    u=H['u']
    for s in (-1,1): obox((s*.66*u,-.1*u,.78*u),(.03*u,.1*u,.12*u),M(C['skin'],.55),.03*u,H['head'],rot=(R(-20),0,0))
def prince(x,y,rz,name='prince',cap=True,z=0.0):
    H=mk(PRINCE,x,y,rz,name,z=z); u=H['u']; fangs(H); _ears(H,PRINCE); sv=M('#D9B24A',.3,metal=.9); hd=H['head']
    for a in range(8):                                                        # silver circlet with one red stone
        an=a*math.pi/4; obox((.62*u*math.sin(an),-.6*u*math.cos(an),1.08*u),(.2*u,.03*u,.05*u),sv,.01*u,hd,rot=(0,0,an))
    obox((0,-.64*u,1.2*u),(.07*u,.03*u,.12*u),sv,.02*u,hd); oico((0,-.67*u,1.2*u),.045*u,M('#D8202A',.2,emit=1.2),hd,sub=1)
    if cap: cape(H,out='#18205A',inn='#C9A24A')
    return H
def queen(x,y,rz,name='queen',z=0.0):
    H=mk(QUEEN,x,y,rz,name,z=z); u=H['u']; fangs(H); _ears(H,QUEEN); gd=M('#C9A24A',.25,metal=.9); hd=H['head']
    for a in range(8):                                                        # tall spiked crown
        an=a*math.pi/4; obox((.5*u*math.sin(an),.1*u-.5*u*math.cos(an),1.62*u),(.16*u,.03*u,.08*u),gd,.01*u,hd,rot=(0,0,an)); obox((.5*u*math.sin(an),.1*u-.5*u*math.cos(an),1.84*u),(.05*u,.03*u,.18*u),gd,.02*u,hd,rot=(0,0,an))
    oico((0,-.43*u,1.66*u),.05*u,M('#8A2BE2',.2,emit=1.2),hd,sub=1)
    cape(H,out='#0E0E16',inn='#6A1B9A',w=1.2); return H
def vampx(C,x,y,rz,name,cap=True,out='#15161C',inn='#7A1420'):
    H=mk(C,x,y,rz,name); fangs(H); _ears(H,C)
    if cap: cape(H,out=out,inn=inn)
    return H
def mithai(H,s=1,col='#D83A8A'):
    """box of sweets hanging from a ribbon in hand s"""
    gd=M('#F2C14E',.4,metal=.5)
    return in_hand(H,s,lambda e:(obox((0,0,-.3),(.22,.22,.07),M(col,.6),.02,e),obox((0,0,-.3),(.225,.03,.075),gd,0,e),obox((0,0,-.3),(.03,.225,.075),gd,0,e),obox((0,0,-.13),(.012,.012,.12),gd,0,e)))
def photo(H,s=1,col='#F28AA0'):
    """phone held out at arm's length, screen towards whoever the arm points at, showing a portrait (arm-local: -z is along the arm, -y is up when the arm is level)"""
    def b(e):
        obox((0,-.02,-.16),(.12,.21,.012),M('#16171C',.4),.01,e); obox((0,-.02,-.174),(.105,.19,.003),M('#F4F1EA',.3,emit=2.4),0,e)
        oico((0,-.07,-.18),.055,M('#D8A277',.5,emit=.9),e,sc=(1,1,.1),sub=1); obox((0,-.13,-.18),(.07,.03,.003),M('#2A1B14',.5,emit=.2),0,e); obox((0,.07,-.18),(.085,.06,.003),M(col,.5,emit=.9),0,e)
    return in_hand(H,s,b)
def pbat(s=1.7):
    """the prince as a bat: bigger, with his silver circlet"""
    b=bat(s=s); sv=M('#D8DCE6',.25,metal=.9)
    for a in range(6): an=a*math.pi/3; obox((.09*math.sin(an),-.02-.09*math.cos(an),.12),(.05,.012,.02),sv,.004,b['root'],rot=(0,0,an))
    return b
def coffin(loc,rz=0,tilt=0,lid=True,parent=None):
    """coffin lying along y at loc (base centre). returns (root, lid)"""
    e=empty(loc,parent,rot=(R(tilt),0,R(rz))); cm=M('#3A2618',.6,kind='wood',sc=.5); gd=M('#C9A24A',.3,metal=.8)
    obox((0,0,.28),(.55,1.3,.28),cm,.05,e); obox((0,0,.3),(.47,1.2,.27),M('#7A1420',.8,kind='fabric'),.03,e)
    l=empty((-.55,0,.58),e); obox((.55,0,.05),(.57,1.32,.05),cm,.04,l); obox((.55,-.4,.105),(.05,.4,.008),gd,0,l); obox((.55,-.55,.105),(.2,.05,.008),gd,0,l)
    if not lid: l.scale=(0,0,0)
    return e,l
def poster(x,y,z,n=(0,-1,0),s=1.0,seed=0,txt=True):
    """rishta poster on a wall: pale face with silver hair + three lines of text. wall normal n (+-y or +-x)"""
    ny=n[1]; nx=n[0]; o=lambda d:(x+nx*d,y+ny*d,z); W=.62*s; Hh=.92*s
    t=(1,0) if nx==0 else (0,1); sg=-ny if nx==0 else nx
    def bx(du,dz,hw,hh,mat,d): B.box((x+nx*d+t[0]*du*sg,y+ny*d+t[1]*du*sg,z+dz),(hw if nx==0 else .006,.006 if nx==0 else hw,hh),mat,0)
    bx(0,0,W,Hh,M(['#F6E7B0','#FFD9E0','#DFF2E0','#F4F1EA'][seed%4],.85),.012)
    bx(0,.36*s,.2*s,.2*s,M('#C2CAE2',.6),.02); bx(0,.55*s,.23*s,.07*s,M('#7F88A4',.6),.026); bx(0,.61*s,.16*s,.03*s,M('#D9B24A',.4),.03)
    for k_ in (-1,1): bx(k_*.09*s,.45*s,.055*s,.013*s,M('#2A2E40',.5),.026); bx(k_*.045*s,.245*s,.014*s,.024*s,M('#F4F1EA',.4),.026)
    for k in (-1,1): bx(k*.09*s,.38*s,.035*s,.03*s,M('#D8202A',.3,emit=.6),.026)
    bx(0,.27*s,.07*s,.012*s,M('#3A2A2A',.5),.026)
    tz=lambda dz:(x+nx*.03,y+ny*.03,z+dz)
    if txt: text('RISHTA',tz(.02*s),n,.2*s,M('#B8232E',.5),ex=.004); text('350 SAAL',tz(-.26*s),n,.15*s,M('#16171C',.5),ex=.004); text('APNA QILA',tz(-.52*s),n,.15*s,M('#16171C',.5),ex=.004)
    else:
        bx(0,.02*s,.42*s,.09*s,M('#B8232E',.5),.02)
        for q in (-.26,-.52): bx(0,q*s,.36*s,.05*s,M('#3A3A40',.5),.02)
