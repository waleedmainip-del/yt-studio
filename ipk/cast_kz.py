# Cast for "Everyone Is From Karachi". Every named character has its own silhouette, palette and accessory.
# avatar_kz() adds: zombie anatomy (glowing eyes, eye rings, stitches, torn clothes), crown/cape, chef hat, hard hat, turban,
# astronaut helmet, stethoscope, camera, mohawk, headband, garland, money wad, order pad.
def avatar_kz(loc,rz,C,name=None):
    C=dict(C)
    if C.get('zombie'): C.setdefault('eye','#E9E36A'); C.setdefault('scruffy',True)
    H=avatar_bg(loc,rz,C,name=name); u=H['u']; root=H['root']; Hd=H['head']; ARM=H['arm']; LEG=H['leg']; fy=-.62*u-.004; fr=-.5*u
    def Hh(c,s_,m,rot=(0,0,0),bv=.03,par=None): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,par or Hd,rot=rot)
    def Rb(c,s_,m,rot=(0,0,0),bv=.02,par=None): return obox(tuple(v*u for v in c),tuple(v*u for v in s_),m,bv*u,par or root,rot=rot)
    gold=M('#E6B93A',.25,metal=.9); dk=M('#1B1B22',.4); H['zglow']=[]; H['zeyes']=[]; H['kz']={}
    if C.get('zombie'):
        ring=M(shade(C['skin'],.5),.7); zg=M(C.get('zeye','#F4F06A'),.3,emit=1.8); pm=M('#1A1A12',.5); st=M(shade(C['skin'],.4),.7); hole=M(shade(C['skin'],.86),.6)
        for s in (-1,1):
            ocyl((s*.25*u,fy+.001,.64*u),.17*u,.006,ring,Hd,(1,1.3,1))
            a=ocyl((s*.25*u,fy-.004,.66*u),.1*u,.006,zg,Hd,(1,1.3,1)); b=ocyl((s*.25*u,fy-.008,.66*u),.034*u,.004,pm,Hd); H['zeyes']+=[a,b]
            g=ocyl((s*.25*u,fy-.0095,.66*u),.13*u,.003,M('#FFFBB0',.3,emit=10.0),Hd,(1,1.3,1)); g.scale=(0,0,0); H['zglow'].append(g)
        # stitched scar on the left cheek, small one on the brow
        Hh((.42,-.632,.33),(.16,.006,.013),st,rot=(0,R(-28),0),bv=.002)
        for k in range(3): Hh((.31+k*.1,-.633,.39-k*.053),(.012,.006,.05),st,rot=(0,R(-28),0),bv=.002)
        Hh((-.42,-.632,1.0),(.1,.006,.012),st,rot=(0,R(20),0),bv=.002)
        for k in range(2): Hh((-.46+k*.09,-.633,.985+k*.033),(.011,.006,.04),st,rot=(0,R(20),0),bv=.002)
        # torn clothes: holes showing skin, ragged hem, ripped sleeve, knee hole
        if not C.get('no_torn'):
            Rb((.52,-.512,2.6),(.2,.008,.13),hole,rot=(0,R(18),0),bv=.004); Rb((-.6,-.512,3.52),(.13,.008,.09),hole,rot=(0,R(-30),0),bv=.004)
            dc=M(shade(C.get('jacket') or C['top'],.55),.85)
            for x_,w_ in ((-.72,.11),(-.2,.08),(.3,.13),(.78,.09)): Rb((x_,-.516,2.17),(w_,.008,w_),dc,rot=(0,R(45),0),bv=.002)
            if not C.get('short'): Rb((.5,0,-.98),(.515,.515,.1),hole,par=ARM[1],bv=.01)
            Rb((0,-.508,-1.02),(.28,.008,.15),hole,par=LEG[-1],bv=.004)
    if C.get('crown'):
        e=empty((0,.02*u,C.get('crown_z',1.36)*u),Hd,rot=(R(-5),R(10),0)); jw=M('#C8324A',.3,emit=.8); H['kz']['crown']=e
        for sy in (-1,1): obox((0,sy*.6*u,.1*u),(.64*u,.045*u,.13*u),gold,.01,e)
        for sx in (-1,1): obox((sx*.6*u,0,.1*u),(.045*u,.64*u,.13*u),gold,.01,e)
        sp=[(-.5,-.6),(-.17,-.6),(.17,-.6),(.5,-.6),(-.6,-.2),(-.6,.25),(.6,-.2),(.6,.25),(-.4,.6),(0,.6),(.4,.6)]
        for i,(x,y) in enumerate(sp):
            if C['crown']=='broken' and i==2: obox((x*u,y*u,.26*u),(.07*u,.04*u,.06*u),gold,.004,e,rot=(0,R(25),0)); continue
            obox((x*u,y*u,.36*u),(.075*u,.045*u,.16*u),gold,.006,e); oico((x*u,y*u,.56*u),.065*u,gold,e,sub=1)
        for x in (-.34,0,.34): oico((x*u,-.655*u,.1*u),.06*u,jw,e,sub=1)
    if C.get('cape'):
        cm=M(C['cape'],.85,kind='fabric'); cl=M(shade(C['cape'],.62),.85,kind='fabric')
        Rb((0,.64,2.5),(.96,.05,1.55),cm,rot=(R(-3),0,0),bv=.03); Rb((0,.3,4.13),(.98,.42,.1),cm,bv=.05)
        for k in range(6): Rb((-.8+k*.32,.66,.98),(.15,.045,.15),cl,rot=(0,R(45),0),bv=.01)
        for s in (-1,1): Rb((s*.62,-.36,4.12),(.34,.26,.09),cm,bv=.04); oico((s*.4*u,-.56*u,4.02*u),.09*u,gold,root,sub=1)
        Rb((0,-.56,4.0),(.4,.02,.035),gold,bv=.01)
    if C.get('chefhat'):
        wm=M('#F6F4EE',.8,kind='fabric'); Hh((0,.02,1.42),(.56,.56,.22),wm,bv=.05); Hh((0,.02,1.82),(.68,.68,.26),wm,bv=.2); Hh((0,.02,1.25),(.6,.6,.06),M('#E2DED4',.8),bv=.02)
    if C.get('hardhat'):
        hm=M(C['hardhat'],.35,spec=.7); Hh((0,.04,1.36),(.7,.72,.24),hm,bv=.2); Hh((0,-.5,1.18),(.62,.42,.04),hm,bv=.03); Hh((0,.04,1.56),(.1,.6,.08),hm,bv=.04)
    if C.get('turban'):
        tm=M(C['turban'],.85,kind='fabric'); t2=M(shade(C['turban'],.78),.85,kind='fabric')
        Hh((0,.03,1.4),(.74,.74,.3),tm,bv=.24); Hh((.08,-.28,1.56),(.56,.42,.13),t2,rot=(0,R(20),0),bv=.1); Hh((-.1,.1,1.7),(.44,.44,.12),tm,bv=.1)
        Hh((.56,.62,.7),(.13,.05,.55),tm,bv=.03)
        if C.get('kalgi'): oico((0,-.76*u,1.5*u),.09*u,M('#C8324A',.3,emit=.8),Hd,sub=1); Hh((0,-.74,1.86),(.05,.03,.3),M('#F4F1EA',.6),bv=.02); oico((0,-.74*u,1.5*u),.12*u,gold,Hd,sc=(1,.4,1),sub=1)
    if C.get('mohawk'):
        mm=M(C['mohawk'],.5,spec=.5)
        for k in range(6): Hh((0,-.5+k*.2,1.5+.12*math.sin(k*1.1+.4)),(.08,.12,.28),mm,rot=(R(-12+k*5),0,0),bv=.04)
    if C.get('headband'): Hh((0,0,1.0),(.645,.645,.07),M(C['headband'],.8,kind='fabric'),bv=.02)
    if C.get('astro'):
        gl=M('#BFE6FF',.04,spec=1.0,alpha=.16); wm=M('#EEF0F4',.45,spec=.6); og=M('#E2702A',.5)
        Hh((0,.04,1.42),(.82,.84,.12),wm,bv=.1); Hh((0,.8,.62),(.82,.1,.86),wm,bv=.08); Hh((0,.04,-.16),(.82,.84,.1),wm,bv=.06)
        for s in (-1,1): Hh((s*.78,.04,.62),(.08,.84,.86),wm,bv=.06); Hh((s*.78,-.3,.62),(.1,.16,.2),og,bv=.04)
        Hh((0,-.78,1.36),(.76,.04,.08),og,bv=.02); Hh((0,-.78,-.1),(.76,.04,.06),og,bv=.02)
        o=Hh((0,-.79,.63),(.7,.008,.66),gl,bv=0); o.name='glass_visor'
        Hh((.5,.3,1.62),(.02,.02,.3),M('#C9CED8',.3,metal=.8),bv=.005); oico((.5*u,.3*u,1.92*u),.05*u,M('#E8554D',.3,emit=1.5),Hd,sub=1)
        Rb((-.5,-.53,3.5),(.3,.03,.22),M('#3A4A6A',.5),bv=.02)
        for k,c in enumerate(('#E8554D','#F2C14E','#6FC38A')): Rb((-.7+k*.2,-.57,3.5),(.06,.012,.06),M(c,.4,emit=.8),bv=.01)
        Rb((.5,-.53,3.5),(.24,.012,.16),M('#1E6A3A',.5),bv=.004); Rb((.32,-.535,3.5),(.06,.012,.16),M('#F4F1EA',.5),bv=.004)
        for s in (-1,1): Rb((s*.5,0,-.6),(.535,.535,.06),og,par=ARM[s],bv=.01); Rb((0,0,-.9),(.52,.53,.06),og,par=LEG[s],bv=.01)
    if C.get('steth'):
        sm=M('#2A2C34',.4)
        for s in (-1,1): Rb((s*.3,-.53,3.7),(.03,.02,.34),sm,rot=(0,R(s*-14),0),bv=.01)
        Rb((0,-.53,3.3),(.03,.02,.16),sm,bv=.01); ocyl((0,fr-.03*u-.01,3.1*u),.1*u,.03,M('#C9CED8',.3,metal=.8),root)
    if C.get('camera'):
        Rb((0,-.6,3.1),(.3,.12,.2),dk,bv=.03); ocyl((0,fr-.2*u,3.1*u),.14*u,.14*u,M('#3A3D44',.3,metal=.6),root); ocyl((0,fr-.275*u,3.1*u),.09*u,.01,M('#6FB7E8',.1,spec=1),root)
        for s in (-1,1): Rb((s*.3,-.53,3.65),(.035,.012,.4),M('#C8372D',.7),rot=(0,R(s*-22),0),bv=.004)
    if C.get('garland'):
        cs=[M('#E8554D',.7),M('#F6F4EE',.7),M('#F2A11A',.7)]
        for k in range(13):
            a=R(-78+k*13); oico((.62*math.sin(a)*u,fr-.07*u,(4.0-.95*math.cos(a))*u),.085*u,cs[k%3],root,sub=1)
    if C.get('notes'):   # fanned wad of cash between the fingers of the right hand
        e=empty((.5*u,-.5*u,-1.95*u),ARM[1]); H['kz']['notes']=e
        for k,c in enumerate(('#6FA86A','#C86A6A','#6A8AC8','#6FA86A')): obox((0,-.14*u,(.02+k*.004)),(.13*u,.3*u,.004),M(c,.7),.002,e,rot=(0,0,R(-24+k*16)))
    if C.get('pad'):     # order pad in the left hand, pencil behind the right ear
        e=empty((-.5*u,-.5*u,-1.95*u),ARM[-1]); H['kz']['pad']=e
        obox((0,-.1*u,.02),(.2*u,.28*u,.03*u),M('#F6F4EE',.7),.004,e); obox((0,-.1*u,.02+.035*u),(.2*u,.05*u,.012*u),M('#C8372D',.6),.002,e,rot=(0,0,0))
        Hh((.68,-.1,.82),(.022,.3,.022),M('#F2C14E',.5),rot=(R(18),0,0),bv=.005)
    return H
def zeyes(H,k):
    """scale a zombie's glowing eyes (k=1 normal, >1 wide, 0 shut)"""
    for i,o in enumerate(H.get('zeyes',[])): o.scale=(k,1.3*k,1) if i%2==0 else (k,k,1)
def zglow(H,k):
    for o in H.get('zglow',[]): o.scale=(k,1.3*k,1) if k>0 else (0,0,0)

WALEED=dict(skin='#C58C5E',hair='#15110E',hairstyle='quiff',textured=True,highlights='#5A3A20',jacket='#0E7C74',top='#F4F1EA',trim='#F4E9C8',pants='#22283A',cuff=True,
        shoes='#F4F5FA',accent='#0E7C74',sole='#F0F1F5',watch=True,eye='#2A1A12',brow_t=1.25,h=1.0,wide=1.0,belt='#3A2A1E')
WAITER=dict(skin='#B07A50',hair='#15110E',hairstyle='neat',neat=True,stache='#15110E',top='#F4F1EA',trim='#DAD6CC',waistcoat='#7A1F2E',pants='#1C1D24',rolled=True,
        towel='#E8B23A',shoes='#16171C',sole='#2A2C34',accent='#16171C',pad=True,eye='#2A1A12',brow_t=1.2,h=.98,wide=.95)
COOK=dict(skin='#9E6A44',hair='#D8D8DC',hairstyle='bald',beard='#D8D8DC',stache='#C8C8CC',topi='#F4F1EA',top='#F4F1EA',trim='#DAD6CC',short=True,apron='#2E6B4F',
        towel='#C8372D',pants='#4A4A54',sandals='#2A2C34',ladle=True,eye='#2A1A12',brow_t=1.5,brow_c='#8A8A90',h=1.02,wide=1.32)
CHAIWALA=dict(skin='#8A5A3A',hair='#15110E',hairstyle='short',stache='#15110E',stache_style='handlebar',topi='#7A1F2E',top='#D8CFB4',trim='#B8AE90',kurta=True,shalwar=True,
        pants='#D8CFB4',waistcoat='#5A3A22',sandals='#3A2A1E',eye='#2A1A12',brow_t=1.35,h=.94,wide=1.1)
CONDUCTOR=dict(skin='#A9744C',hair='#15110E',hairstyle='fringe',oily=True,mustache='#15110E',top='#8FB8D8',trim='#6E9ABF',kurta=True,shalwar=True,pants='#8FB8D8',
        scarf='#C8372D',bag='#3A2A1E',sandals='#2A2C34',notes=True,eye='#2A1A12',brow_t=1.3,h=.9,wide=.92)
PM=dict(skin='#C9925F',hair='#9A9AA2',hairstyle='neat',neat=True,mustache='#B8B8BC',glasses=True,top='#F6F4EE',trim='#E2DED4',kurta=True,shalwar=True,pants='#F6F4EE',
        waistcoat='#16171C',shoes='#16171C',sole='#2A2C34',accent='#16171C',watch=True,eye='#2A1A12',brow_t=1.3,brow_c='#6A6A70',h=1.05,wide=1.1)
ASTRO=dict(skin='#B07A50',hair='#15110E',hairstyle='short',stache='#15110E',top='#F1F3F6',trim='#D8DCE2',pants='#F1F3F6',gloves='#C9CED8',boots='#C9CED8',pack='#D8DCE2',
        astro=True,eye='#2A1A12',brow_t=1.3,h=1.0,wide=1.14)
BEDMAN=dict(skin='#C9925F',hair='#E8E8EA',hairstyle='old',beard='#F4F1EA',glasses=True,jacket='#8A6A4A',top='#E8E2D0',trim='#6E5236',pants='#5A5A66',sandals='#3A2A1E',
        eye='#2A1A12',brow_t=1.2,brow_c='#B8B8BC',h=.93,wide=1.04)
UNCLE=dict(skin='#B98A62',hair='#D8D8DC',hairstyle='old',beard='#E8E8EA',stache='#D8D8DC',glasses=True,topi='#F4F1EA',top='#E8D9B8',trim='#C9B48A',kurta=True,shalwar=True,
        pants='#E8D9B8',sandals='#5A3A22',eye='#2A1A12',brow_t=1.3,brow_c='#9A9AA2',h=.95,wide=1.14)
GROOM=dict(skin='#C58C5E',hair='#15110E',hairstyle='short',mustache='#15110E',turban='#8A1F3A',kalgi=True,garland=True,top='#F2E2B0',trim='#D9B24A',kurta=True,shalwar=True,
        pants='#F6F4EE',waistcoat='#D9B24A',shoes='#D9B24A',sole='#8A6A2A',accent='#8A1F3A',eye='#2A1A12',brow_t=1.25,h=1.03,wide=1.04)
DHOLI=dict(skin='#9E6A44',hair='#15110E',hairstyle='short',stache='#15110E',stache_style='handlebar',turban='#F2A11A',top='#D9367A',trim='#F2C14E',kurta=True,shalwar=True,
        pants='#F6F4EE',waistcoat='#2B58C9',sandals='#3A2A1E',eye='#2A1A12',brow_t=1.4,h=1.0,wide=1.16)
DHOLI2=dict(DHOLI,skin='#B07A50',turban='#35975A',top='#F2C14E',trim='#D9367A',waistcoat='#7448C2',stache_style='strong',h=.96,wide=1.06)
AUNTY=dict(skin='#D9A273',hair='#2A1E16',hairstyle='bun',glasses=True,top='#7448C2',trim='#5A3496',kurta=True,pants='#F4F1EA',dupatta='#F2C14E',dupatta_trim='#D9367A',
        lashes=True,earrings=True,bangles=True,handbag='#C8372D',shoes='#C9A27A',sole='#3A2A1E',accent='#E6B53A',eye='#2A1A12',brow_t=1.0,h=.9,wide=1.12)
FRIENDS=[dict(skin='#C9925F',hair='#15110E',hairstyle='fringe',hoodie=True,top='#E2702A',trim='#F4E9C8',strings='#F4F1EA',pants='#2A2C34',shoes='#F4F5FA',eye='#2A1A12',brow_t=1.2,h=.98,wide=1.0),
         dict(skin='#A9744C',hair='#15110E',hairstyle='curly',glasses=True,top='#27365A',trim='#E8C547',kurta=True,shalwar=True,pants='#27365A',sandals='#3A2A1E',eye='#2A1A12',brow_t=1.3,h=1.04,wide=.96),
         dict(skin='#D9A273',hair='#3A2A1E',hairstyle='cap',cap='#C8372D',top='#F2C14E',trim='#C8372D',short=True,pants='#3A4A6A',shoes='#16171C',sole='#F0F1F5',chain=True,eye='#2A1A12',brow_t=1.15,h=.92,wide=1.18),
         dict(skin='#B07A50',hair='#15110E',hairstyle='short',beard='#15110E',jacket='#3A5A8A',top='#F4F1EA',trim='#27365A',pants='#8A7A5A',shoes='#5A3A22',sole='#F0F1F5',watch=True,eye='#2A1A12',brow_t=1.4,h=1.06,wide=1.08)]
KIT=dict(top='#1E8A4A',trim='#F2C14E',pants='#F6F4EE',stripe='#1E8A4A',shoes='#F4F5FA',sole='#C8372D',accent='#1E8A4A',short=True)
CRICK=[dict(KIT,skin=s,hair=h,hairstyle=hs,eye='#2A1A12',brow_t=1.25,h=hh,wide=w,**x) for s,h,hs,hh,w,x in (
        ('#B07A50','#15110E','cap',1.02,1.0,dict(cap='#1E8A4A',capstar='#F2C14E')),('#C9925F','#2A1E16','curly',.94,1.1,dict(headband='#F2C14E')),
        ('#9E6A44','#15110E','short',1.06,.96,dict(beard='#15110E')),('#D9A273','#3A2A1E','quiff',.98,1.04,dict(shades='#16171C')))]
# ---------------------------------------------------------------- zombies
ZS=['#8FB37A','#7FA868','#9CBF8A','#86A870','#A3B88A','#7A9E7A','#93AD84']
def Z(**k):
    d=dict(zombie=True,hair='#22301E',hairstyle='fringe',brow_t=1.5,h=1.0,wide=1.0,shoes='#3A3D44',sole='#2A2C34',accent='#2A2C34',pants='#3A3D47'); d.update(k); return d
ZED=Z(skin=ZS[0],top='#C9D6E8',trim='#A9B8CC',tie='#B8323A',glasses=True,pants='#3A4258',shoes='#3A2A1E',h=1.0,wide=1.02,bandaid=True)
ZKING=Z(skin='#6E9A62',hair='#2A2A34',hairstyle='old',stache='#22281E',stache_style='handlebar',zeye='#FF9A3A',crown='broken',cape='#5A2A7A',jacket='#3A2A4A',top='#2A2030',trim='#E6B93A',
        pants='#2A2030',boots='#2A2030',gloves='#3A2A4A',chain=True,brow_t=1.8,h=1.24,wide=1.24,no_torn=False)
ZVAR=[Z(skin=ZS[1],hairstyle='neat',neat=True,top='#F1F3F6',trim='#D8DCE2',kurta=True,pants='#4A7A8A',steth=True,h=1.02,wide=.98),                       # doctor
      Z(skin=ZS[2],hairstyle='short',stache='#22301E',chefhat=True,top='#F6F4EE',trim='#E2DED4',apron='#E8E2D0',scarf='#C8372D',pants='#3A3A42',h=1.0,wide=1.26), # chef
      Z(skin=ZS[3],hairstyle='short',hardhat='#F2C14E',top='#5A7FB0',trim='#4A6A96',vest='#E2702A',pants='#6A5A40',boots='#4A3A26',h=1.06,wide=1.12),            # builder
      Z(skin=ZS[4],hair='#C8C8CC',hairstyle='bun',glasses=True,top='#D8A0B8',trim='#B8809A',kurta=True,pants='#F4F1EA',dupatta='#9A6FD0',h=.86,wide=1.1,scruffy=False), # granny
      Z(skin=ZS[0],hairstyle='cap',cap='#F4F1EA',top='#E8554D',trim='#F2C14E',short=True,camera=True,shades='#16171C',pants='#C9B48A',shoes='#F4F5FA',h=1.03,wide=1.06,scruffy=False), # tourist
      Z(skin=ZS[5],hairstyle='curly',top='#1E8A4A',trim='#F2C14E',short=True,headband='#F2C14E',stripe='#F2C14E',pants='#F6F4EE',shoes='#F4F5FA',h=.97,wide=1.0,scruffy=False),          # cricket fan
      Z(skin=ZS[6],hairstyle='short',receding=True,mustache='#22301E',jacket='#2A2C34',top='#F4F1EA',trim='#16171C',tie='#2B58C9',pants='#2A2C34',handbag='#5A3A22',h=1.04,wide=1.08,scruffy=False), # businessman
      Z(skin=ZS[3],hairstyle='bald',mohawk='#D9367A',top='#16171C',trim='#2A2C34',short=True,chain=True,pants='#3A2A4A',boots='#16171C',h=1.0,wide=.98,scruffy=False),                    # punk
      Z(skin=ZS[1],hairstyle='short',headband='#C8372D',top='#C8372D',trim='#16171C',short=True,pants='#16171C',shoes='#F4F5FA',h=1.1,wide=1.34),               # gym bro
      Z(skin=ZS[2],hairstyle='cap',cap='#2B58C9',top='#8FB8D8',trim='#6E9ABF',bag='#8A5A36',pants='#27365A',h=.96,wide=1.0,scruffy=False),                    # postman
      Z(skin=ZS[4],hair='#2A2030',hairstyle='long',lashes=True,earrings=True,top='#16909E',trim='#0E6A76',kurta=True,pants='#F4F1EA',dupatta='#F2C14E',h=.92,wide=1.02,scruffy=False), # aunty
      Z(skin=ZS[0],hairstyle='fringe',hoodie=True,top='#7448C2',trim='#5A3496',strings='#F4F1EA',phones='#F2C14E',pack='#E2702A',pants='#2A2C34',h=.94,wide=1.0), # student
      Z(skin=ZS[6],hair='#D8D8DC',hairstyle='old',beard='#D8D8DC',topi='#F4F1EA',top='#B8B0A0',trim='#9A9280',kurta=True,shalwar=True,pants='#B8B0A0',sandals='#3A2A1E',h=.9,wide=1.06,scruffy=False)] # elder
ZRICK=Z(skin=ZS[5],hairstyle='cap',cap='#2E8A6A',beard='#22301E',top='#8A6A4A',trim='#6E5236',kurta=True,shalwar=True,pants='#8A6A4A',scarf='#E8E2D0',sandals='#2A2C34',h=.98,wide=1.08,scruffy=False)
ZCHAI=Z(skin=ZS[2],hairstyle='short',stache='#22301E',stache_style='handlebar',topi='#7A1F2E',top='#D8CFB4',trim='#B8AE90',kurta=True,shalwar=True,pants='#D8CFB4',apron='#C8372D',
        sandals='#3A2A1E',h=.96,wide=1.1,scruffy=False)
ZCRIC=Z(**dict(KIT,skin=ZS[0],hairstyle='cap',cap='#1E8A4A',capstar='#F2C14E',h=1.0,wide=1.02,scruffy=False,no_torn=True))
CAST=dict(WALEED=WALEED,WAITER=WAITER,COOK=COOK,CHAIWALA=CHAIWALA,CONDUCTOR=CONDUCTOR,PM=PM,ASTRO=ASTRO,BEDMAN=BEDMAN,UNCLE=UNCLE,GROOM=GROOM,DHOLI=DHOLI,AUNTY=AUNTY)
ZCAST=dict(ZKING=ZKING,ZED=ZED,DOCTOR=ZVAR[0],CHEF=ZVAR[1],BUILDER=ZVAR[2],GRANNY=ZVAR[3],TOURIST=ZVAR[4],FAN=ZVAR[5],BOSS=ZVAR[6],PUNK=ZVAR[7],GYM=ZVAR[8],POSTMAN=ZVAR[9])
# ---------------------------------------------------------------- human crowd: 24 unique looks (no two share top colour + hairstyle), all ages
_TOPS=['#C8372D','#2E6B4F','#E8C547','#5A7FB0','#D9367A','#F4F1EA','#7A4A8A','#E28A3A','#1E3FA0','#3A8A9A','#9A3A5A','#6A8A3A','#B05A3A','#2A2C34','#C9A0E0','#5AB0A0','#8A5A36','#E8956A','#4A5A6A','#D8CFB4',
       '#F28AA0','#35975A','#B8D86A','#27365A']
_r=random.Random(91); CROWD=[]
for i,tc in enumerate(_TOPS):
    f=i%3==2; kid=i in (5,13,20)
    c=dict(skin=_r.choice(['#C58C5E','#B07A50','#D9A273','#9E6A44','#C9925F','#A9744C']),hair=_r.choice(['#15110E','#2A1E16','#3A2A1E']),eye='#2A1A12',
        brow_t=_r.uniform(1.0,1.45),h=_r.uniform(.88,1.06),wide=_r.uniform(.94,1.2),top=tc,trim=shade(tc,.75),kurta=i%2==0,shalwar=i%2==0,sandals=_r.choice(['#3A2A1E','#5A3A22','#2A2C34']))
    c['pants']=tc if c['kurta'] else _r.choice(['#2A2C34','#3A4A6A','#8A7A5A','#27365A'])
    if f: c.update(hairstyle=['bun','ponytail','long','bob'][i%4],dupatta=_r.choice(['#E8C547','#F4F1EA','#D9367A','#5AB0A0','#7448C2']),earrings=True,bangles=i%2==0,lashes=True,kurta=True,shalwar=False,pants='#F4F1EA')
    else:
        c.update(hairstyle=['short','curly','quiff','old','fringe'][i%5]); x=i%4
        if x==0: c['mustache']=c['hair']
        elif x==1: c['beard']=c['hair']; c['topi']=_r.choice(['#F4F1EA','#D8CFB4','#3A3A42'])
        elif x==2: c['hairstyle']='cap'; c['cap']=_r.choice(['#C8372D','#2E5A9A','#16171C','#E8C547'])
        else: c['glasses']=True
        if c['hairstyle']=='old': c['hair']='#C8C8CC'; c['h']=.9
    if kid: c.update(h=.68,wide=1.0,hairstyle='fringe' if not f else 'ponytail',hair='#15110E'); c.pop('mustache',None); c.pop('beard',None); c.pop('topi',None); c.pop('glasses',None)
    CROWD.append(c)
ZKING_CHEF=dict(ZKING,cape=None,apron='#F4F1EA',chefhat=True,crown='whole',crown_z=2.12,towel='#C8372D',gloves=None,chain=None)
AUNTY_R=dict(AUNTY,handbag=None)
