# Cast for "Karachi vs Lahore". Team Lahore = green + gold, Team Karachi = blue + white. Waleed keeps his fixed look (from cast_kz).
LG='#1F7A44'; LGOLD='#E6B53A'; KB='#2466C9'; KW='#F4F6FA'; KSKY='#6FC3EA'
SHEEDA=dict(skin='#B98A62',hair='#15110E',hairstyle='neat',neat=True,oily=True,stache='#15110E',stache_style='handlebar',top='#F2E9D0',trim='#D9C9A0',kurta=True,shalwar=True,
        pants='#F2E9D0',waistcoat=LG,scarf=LGOLD,chain=True,sandals='#5A3A22',watch=True,eye='#2A1A12',brow_t=1.5,h=1.08,wide=1.2)
GUDDU=dict(skin='#A9744C',hair='#15110E',hairstyle='curly',jacket=KB,top=KW,trim='#F4F6FA',pants='#23252E',cuff=True,shoes='#F4F5FA',sole='#F0F1F5',accent=KSKY,
        chain=True,headband=KSKY,eye='#2A1A12',brow_t=1.3,h=1.03,wide=.98)
REF=dict(skin='#C9925F',hair='#B8B8BC',hairstyle='cap',cap='#16171C',mustache='#C8C8CC',glasses=True,top='#F4F1EA',trim='#16171C',tie='#16171C',vest='#2A2C34',
        pants='#16171C',shoes='#16171C',sole='#2A2C34',accent='#16171C',eye='#2A1A12',brow_t=1.3,brow_c='#8A8A90',h=.96,wide=1.08)
ISB=dict(skin='#D9A273',hair='#2A1E16',hairstyle='neat',neat=True,shades='#16171C',top='#F4F1EA',trim='#DAD6CC',vest='#2F5D50',pants='#C9B48A',shoes='#8A5A36',sole='#F0F1F5',
        accent='#8A5A36',watch=True,eye='#2A1A12',brow_t=1.05,h=1.03,wide=.96)
BOSS=dict(skin='#C58C5E',hair='#3A3A42',hairstyle='short',receding=True,mustache='#3A3A42',glasses=True,jacket='#3D4254',top='#F4F1EA',trim='#2A2E3C',tie='#B8323A',
        pants='#3D4254',shoes='#16171C',sole='#2A2C34',accent='#16171C',watch=True,eye='#2A1A12',brow_t=1.5,h=1.0,wide=1.14)
CAND=dict(skin='#C9925F',hair='#15110E',hairstyle='fringe',top='#BFD6EC',trim='#9FBAD6',tie='#27365A',pants='#3A3D47',shoes='#3A2A1E',sole='#2A2C34',accent='#3A2A1E',
        eye='#2A1A12',brow_t=1.1,h=.97,wide=.96)
GUARD=dict(skin='#9E6A44',hair='#15110E',hairstyle='cap',cap='#27365A',capstar='#E6B53A',stache='#15110E',top='#27365A',trim='#1A2440',pants='#1A2440',boots='#16171C',
        belt='#16171C',eye='#2A1A12',brow_t=1.6,h=1.06,wide=1.1)
GUARD2=dict(GUARD,skin='#B07A50',stache=None,beard='#15110E',h=1.02,wide=1.16)
BABY=dict(skin='#D9A273',hair='#2A1E16',hairstyle='short',top='#FFF2C4',trim='#F2C14E',pants='#FFF2C4',shoes='#FFF2C4',sole='#F2C14E',accent='#F2C14E',eye='#2A1A12',
        brow_t=.8,h=.46,wide=1.12)
MOM=dict(skin='#D9A273',hair='#2A1E16',hairstyle='long',top=KSKY,trim=KB,kurta=True,pants=KW,dupatta=KW,dupatta_trim=KB,lashes=True,earrings=True,bangles=True,
        shoes='#C9A27A',sole='#3A2A1E',accent=KB,eye='#2A1A12',brow_t=1.0,h=.93,wide=1.0)
DAD=dict(skin='#C58C5E',hair='#15110E',hairstyle='short',beard='#15110E',top='#F2E9D0',trim=LGOLD,kurta=True,shalwar=True,pants='#F2E9D0',scarf=LG,sandals='#5A3A22',
        eye='#2A1A12',brow_t=1.3,h=1.04,wide=1.08)
def _fans(seed,tops,scarves,team):
    r=random.Random(seed); out=[]
    sk=['#C58C5E','#B07A50','#D9A273','#9E6A44','#C9925F','#A9744C']
    for i,tc in enumerate(tops):
        f=i%4==2; kid=i==5; old=i==3
        c=dict(skin=r.choice(sk),hair=r.choice(['#15110E','#2A1E16','#3A2A1E']),eye='#2A1A12',brow_t=r.uniform(1.0,1.45),h=r.uniform(.9,1.06),wide=r.uniform(.94,1.14),top=tc,trim=shade(tc,.72))
        if team=='L': c.update(kurta=True,shalwar=not f,pants='#F4F1EA' if f else (tc if i%2 else '#F2E9D0'),sandals=r.choice(['#3A2A1E','#5A3A22']))
        else:
            c.update(pants=r.choice(['#23252E','#3A4A6A','#27365A','#4A4E5A']),shoes=r.choice(['#F4F5FA','#16171C','#3A2A1E']),sole='#F0F1F5')
            if i%3==0: c.update(hoodie=True,strings='#F4F1EA')
            elif i%3==1: c['short']=True
            else: c['jacket']=shade(tc,.6)
        if f: c.update(hairstyle=['bun','ponytail','long','bob'][i%4],dupatta=scarves[i%len(scarves)],earrings=True,lashes=True,kurta=True,shalwar=False,pants='#F4F1EA'); c.pop('hoodie',None); c.pop('jacket',None); c.pop('short',None); c.pop('strings',None)
        else:
            c['hairstyle']=['short','curly','fringe','old','quiff','fringe','short','curly','neat'][i%9]; x=i%4
            if x==0: c['mustache']=c['hair']
            elif x==1: c['beard']=c['hair']
            elif x==3: c['glasses']=True
            if i%2==0: c['scarf']=scarves[i%len(scarves)]
            if team=='L' and i in (1,6): c['turban']=[LGOLD,'#C8372D'][i%2]
            if team=='K' and i in (1,7): c['hairstyle']='cap'; c['cap']=[KB,'#16171C'][i%2]
        if old: c.update(hair='#D0D0D4',hairstyle='old',beard='#E0E0E4',h=.9,topi='#F4F1EA'); c.pop('turban',None)
        if kid: c.update(h=.66,wide=1.0,hairstyle='fringe',hair='#15110E'); [c.pop(k,None) for k in ('mustache','beard','topi','glasses','turban')]
        out.append(c)
    return out
LFANS=_fans(41,['#C8372D','#E6B53A','#D9367A','#F2E9D0','#35975A','#F28A3A','#8A1F3A','#B8D86A','#E8C547','#9A6FD0','#F4F1EA','#2E6B4F'],[LG,LGOLD,'#F4F1EA'],'L')
KFANS=_fans(57,['#F4F6FA','#6FC3EA','#27365A','#9AA8BC','#16909E','#F2C14E','#C9D6E8','#3A8A9A','#7448C2','#E8554D','#2A2C34','#5AB0A0'],[KB,KW,KSKY],'K')
CAST_KVL=dict(WALEED=WALEED,SHEEDA=SHEEDA,GUDDU=GUDDU,REF=REF,ISB=ISB,BOSS=BOSS,CAND=CAND,GUARD=GUARD,BABY=BABY,MOM=MOM,DAD=DAD)
