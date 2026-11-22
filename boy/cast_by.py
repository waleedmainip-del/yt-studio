# cast for "Every Pakistani boy lives the same life": outfits unique to this film. h: 1.0 = 175 cm
WALEED=dict(skin='#C48A60',hair='#16100C',hairstyle='fringe',brow_c='#16100C',top='#3E5C76',trim='#2F475C',sleeve='#3E5C76',pants='#2B2C33',cuff=True,shoes='#3A6E8C',sole='#22242B',accent='#F2C12E',h=175/175)
AMMI=dict(skin='#C99468',hair='#1E1612',hairstyle='dupatta',dupatta='#F4F1EA',brow_c='#1E1612',top='#4E9C7E',trim='#3C7E64',kameez='#4E9C7E',kameez_border='#F4F1EA',pants='#F4F1EA',shoes='#8A5A3A',sole='#5A3A22',accent='#F4F1EA',bangles='#C9A24A',glasses=True,h=158/175)
BILAL=dict(skin='#AE7650',hair='#1A140E',hairstyle='cap',cap='#C6453A',brow_c='#1A140E',mustache='#1A140E',top='#2F8C99',trim='#257482',sleeve='#2F8C99',pants='#4A4F5A',shoes='#F4F5FA',sole='#DADDE2',accent='#FFFFFF',chain=True,h=173/175)
UNCLE=dict(skin='#B98057',hair='#7A7570',hairstyle='old',brow_c='#5A5550',mustache='#5A5550',glasses=True,top='#F4F1EA',trim='#6E6658',sleeve='#8A8070',jacket='#8A8070',pants='#8A8070',shoes='#2B2018',sole='#1A140E',accent='#C9A24A',belly=True,watch=True,h=170/175)
AUNTY2=dict(skin='#D0A07A',hair='#2A1E18',hairstyle='dupatta',dupatta='#7E1A2C',brow_c='#2A1E18',top='#C9A24A',trim='#A8862E',kameez='#C9A24A',kameez_border='#7E1A2C',pants='#7E1A2C',shoes='#7E1A2C',sole='#4A0E18',accent='#7E1A2C',bangles='#E8C25A',purse='#7E1A2C',h=160/175)
KUR=['#3B8E8C','#C65D4A','#6C5FB0','#4C7FC2','#8BB85A','#D98AA8','#F2EBDD','#5A6170','#B8683A','#2E7D5A','#E8DCC0','#9E3B4E']
def local(seed,kid=False,female=None):
    r=random.Random(seed*29+11); fem=(r.random()<.35) if female is None else female; col=r.choice(KUR)
    c=dict(skin=r.choice(SK[1:6]),hair=r.choice(HR[:3]+HR[5:7]),top=col,trim=shade(col,.85),pants=col if r.random()<.7 else r.choice(['#F2EFE8','#3B4F78','#2B2C33']),
           shoes=r.choice(['#8A5A2A','#22242B','#C9A24A','#F4F5FA','#5A3A22']),accent=r.choice(['#C9A24A','#FFFFFF','#22242B']),
           h=(r.choice([.74,.78,.82]) if kid else r.choice([.94,.97,1.0,1.03,1.06])),kameez=col)
    if fem:
        c['hairstyle']='dupatta'; c['dupatta']=r.choice(KUR); c['h']=c['h']-.04; c['kameez_border']=r.choice(['#E8C25A','#FFFFFF','#2B2C33'])
    else:
        c['hairstyle']=r.choice(['short','fringe','curly','old','cap','quiff'])
        if c['hairstyle']=='cap': c['cap']=r.choice(['#F4F1EA','#2B2C33','#9E3B4E'])
        if r.random()<.35: c['beard']=c['hair']
        elif r.random()<.3: c['mustache']=c['hair']
        if r.random()<.3: c['waistcoat']=r.choice(['#2B2C33','#5A3A22','#1F3A5A','#7A1E2E']); c['wc_trim']=shade(c['waistcoat'],.7)
        if c['hairstyle']=='old' and r.random()<.5: c['hair']='#C9C6C0'
    if kid: c.pop('kameez',None); c['short']=True
    return c

def extras(H):
    C=H['C']; u=H['u']; root=H['root']; fr=-.5*u; Hd=H['head']
    if C.get('kameez'):
        km=M(C['kameez'],.8,kind='fabric',spec=.2); bd=M(C.get('kameez_border',shade(C['kameez'],.85)),.7)
        for yy,dy in ((fr-.012,.012),(.5*u+.012,.012)): obox((0,yy,1.42*u),(1.02*u,dy,.6*u),km,.01,root)
        for s in (-1,1): obox((s*1.01*u,0,1.42*u),(.014,.53*u,.6*u),km,.01,root)
        obox((0,fr-.026,.84*u),(1.03*u,.01,.04*u),bd,.004,root)
        obox((0,fr-.026,3.55*u),(.05*u,.01,.42*u),bd,.003,root)
        for z in (3.75,3.5,3.25): ocyl((0,fr-.032,z*u),.035*u,.01,M('#F4F1EA',.3),root)
    if C.get('waistcoat'):
        wc=M(C['waistcoat'],.7,kind='fabric',spec=.25); wt=M(C.get('wc_trim','#C9A24A'),.4,metal=.4)
        for s in (-1,1):
            obox((s*.6*u,fr-.03,3.0*u),(.42*u,.02,.98*u),wc,.01,root); obox((s*1.03*u,0,3.0*u),(.02,.52*u,.98*u),wc,.01,root)
            obox((s*.19*u,fr-.05,3.0*u),(.02*u,.01,.98*u),wt,.002,root)
        obox((0,.52*u,3.0*u),(1.03*u,.02,.98*u),wc,.01,root)
        for z in (3.6,3.2,2.8,2.4): ocyl((.27*u,fr-.055,z*u),.04*u,.01,wt,root)
        obox((0,0,4.06*u),(.45*u,.45*u,.07*u),wc,.03*u,root)
    if C.get('kurta_short'):
        km=M(C['top'],.8,kind='fabric'); obox((0,fr-.012,1.85*u),(1.02*u,.012,.25*u),km,.01,root); obox((0,.5*u+.012,1.85*u),(1.02*u,.012,.25*u),km,.01,root)
    if C.get('flowers'):
        fl=[M('#FFFFFF',.6),M('#F2C12E',.6),M('#E2562E',.6)]
        for i,(x,z) in enumerate([(-.6,3.6),(.5,3.3),(-.2,2.8),(.7,2.5),(-.7,2.3),(.15,3.75),(.35,2.95)]): ocyl((x*u,fr-.016,z*u),.1*u,.008,fl[i%3],root)
        for i,(x,z) in enumerate([(-.5,3.4),(.6,2.9),(0,2.4)]): ocyl((x*u,.5*u+.016,z*u),.1*u,.008,fl[i%3],root)
    if C.get('camera'):
        cm=M('#22242B',.35); obox((0,fr-.09,3.05*u),(.32*u,.09,.2*u),cm,.02,root); ocyl((0,fr-.2,3.05*u),.12*u,.09,M('#11131A',.2,spec=.9),root)
        for s in (-1,1): obox((s*.35*u,fr-.03,3.6*u),(.03*u,.01,.5*u),cm,.003,root,rot=(0,R(s*30),0))
    if C.get('bangles') and 'arm' in H:
        for s in (-1,1):
            for k_ in range(2): obox((s*.5*u,0,(-1.5-.08*k_)*u),(.54*u,.54*u,.025*u),M(C['bangles'],.3,metal=.8),.01,H['arm'][s])
    if C.get('scarf_c'):
        obox((0,fr-.05,3.9*u),(.45*u,.03,.12*u),M(C['scarf_c'],.8,kind='fabric'),.02,root); obox((.3*u,fr-.05,3.3*u),(.12*u,.02,.5*u),M(C['scarf_c'],.8,kind='fabric'),.02,root)
    if C.get('hairstyle')=='dupatta':
        dm=M(C.get('dupatta','#2E8B6E'),.85,kind='fabric')
        obox((0,fr-.04,3.75*u),(1.0*u,.03,.16*u),dm,.03,root,rot=(0,R(-14),0)); obox((0,.5*u+.04,3.5*u),(1.0*u,.03,.45*u),dm,.03,root)
        for s in (-1,1): obox((s*1.04*u,0,3.6*u),(.04,.52*u,.35*u),dm,.02,root)
    if C.get('topi'):
        tp=M(C['topi'],.85,kind='fabric'); ocyl((0,0,1.27*u),.6*u,.2*u,tp,Hd,rot=(0,0,0),seg=16); ocyl((0,0,1.38*u),.58*u,.02*u,M(shade(C['topi'],.85),.8),Hd,rot=(0,0,0),seg=16)
    if C.get('chain'): 
        for k in range(9): a=-1.2+k*.3; obox((math.sin(a)*.42*u,fr-.03,2.95*u-math.cos(a)*.0-abs(a)*.0-(1-abs(a)/1.3)*.28*u),(.035*u,.02,.035*u),M('#E8C25A',.2,metal=.9),.01,root)
    if C.get('towel'): obox((-.62*u,fr-.03,2.82*u),(.3*u,.05,.5*u),M(C['towel'],.9,kind='fabric'),.03*u,root,rot=(0,0,0)); obox((-.62*u,-fr+.03,2.6*u),(.3*u,.05,.7*u),M(C['towel'],.9,kind='fabric'),.03*u,root)
    if C.get('pagri'):
        pg=M(C['pagri'],.6,kind='fabric',spec=.35); gd=M('#E8C25A',.3,metal=.7)
        ocyl((0,0,1.36*u),.72*u,.44*u,pg,Hd,seg=20,rot=(0,0,0)); ocyl((0,0,1.6*u),.66*u,.06*u,M(shade(C['pagri'],.8),.6),Hd,seg=20,rot=(0,0,0))
        for k in range(5): ocyl((0,0,1.18*u+k*.085*u),.735*u,.018*u,gd,Hd,seg=20,rot=(0,0,0))
        obox((.22*u,.1*u,2.0*u),(.14*u,.04*u,.3*u),gd,.02*u,Hd,rot=(0,R(-15),0)); oico((0,-.72*u,1.42*u),.08*u,M('#E8F4FF',.1,emit=.6),Hd)
    if C.get('haar'):
        fl=[M('#C21E3A',.6),M('#F4F1EA',.6),M('#E8C25A',.4,metal=.5)]
        for k in range(17):
            a=-1.35+k*(2.7/16); x=math.sin(a)*.62*u; z=3.92*u-(1-abs(a)/1.35)*1.55*u-abs(a)*.05*u; oico((x,fr-.07,z),.1*u,fl[k%3],root)
    if C.get('belly'):
        bm=M(C.get('kameez',C.get('jacket',C['top'])),.8,kind='fabric',spec=.2); obox((0,fr-.1,2.45*u),(.85*u,.12,.72*u),bm,.25*u,root)
    if C.get('purse'):
        pm=M(C['purse'],.35,metal=.5); obox((1.18*u,-.05*u,2.0*u),(.08*u,.32*u,.26*u),pm,.05*u,root); obox((1.12*u,-.05*u,2.65*u),(.01,.02,.55*u),pm,.003,root)
    if C.get('shades'): H['shades']=sunglasses(H)
    if C.get('shades_up'):
        e=sunglasses(H); e.location=(0,-.3*u,1.32*u); e.rotation_euler=(R(-60),0,0)
    return H
def hide(o): o.scale=(0,0,0)
def hideH(H): H['root'].scale=(0,0,0)
def sunglasses(H):
    u=H['u']; e=empty((0,-.64*u,.7*u),H['head']); SG=M('#0B0C10',.08,metal=.3,spec=1.0); FR=M('#C9A24A',.3,metal=.8)
    for s in (-1,1): obox((s*.25*u,0,0),(.2*u,.02*u,.14*u),SG,.03*u,e)
    obox((0,0,.07*u),(.6*u,.02*u,.02*u),FR,.01,e)
    for s in (-1,1): obox((s*.62*u,.3*u,.04*u),(.015*u,.3*u,.018*u),FR,.004,e)
    e['base']=tuple(e.location); return e
def person(loc,rz,C,mouth='smile',name=None):
    H=av(loc,rz,C,{'mouth':mouth},name=name); extras(H); return H
def crowd(specs,seed0=0,mouth='smile'):
    out=[]
    for i,(x,y,rz) in enumerate(specs):
        kid=(i%7==5); out.append(person((x,y,0),rz,local(seed0+i*3+1,kid),mouth,name='c%d_%d'%(seed0,i)))
    return out
def phone(H,s=1,screen='#7FD3FF'):
    u=H['u']; e=empty((s*.5*u,-.12*u,-2.0*u),H['arm'][s]); obox((0,0,0),(.09,.012,.16),M('#15161A',.3),.01,e); obox((0,-.014,0),(.08,.002,.145),M(screen,.3,emit=1.6),0,e); return e
def keys(H,s=-1):
    u=H['u']; e=empty((s*.5*u,-.1*u,-2.05*u),H['arm'][s]); ocyl((0,0,0),.035,.008,M('#C9CDD6',.3,metal=.9),e,rot=(R(90),0,0)); obox((0,0,-.06),(.012,.004,.04),M('#C9CDD6',.3,metal=.9),.002,e); obox((.02,0,-.06),(.012,.004,.035),M('#C9A24A',.3,metal=.9),.002,e); return e
def ladle(H,s=1):
    u=H['u']; e=empty((s*.5*u,-.05*u,-2.0*u),H['arm'][s]); obox((0,0,.15),(.012,.012,.25),M('#C9CDD6',.3,metal=.9),.004,e); oico((0,0,.42),.06,M('#C9CDD6',.3,metal=.9),e,sc=(1,1,.5)); return e
def walker(H,start,hdg,speed,t,t0=0.0,arm=24):
    d=max(0,(t-t0))*speed; h=R(hdg); p=Vector(start)+Vector((math.sin(h),-math.cos(h),0))*d
    H['root'].location[0]=p.x; H['root'].location[1]=p.y; H['root'].rotation_euler[2]=h; walk(H,d+H['seed'],step=.55,arm=arm)
