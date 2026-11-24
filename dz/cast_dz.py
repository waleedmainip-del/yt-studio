# Cast for "Darzi Ka Kal". WALEED keeps his fixed series look (Eid morning: Abbu's old oversized kurta).
WALEED=dict(skin='#C58C5E',hair='#15110E',hairstyle='quiff',textured=True,highlights='#5A3A20',jacket='#0E7C74',top='#F4F1EA',trim='#F4E9C8',pants='#22283A',cuff=True,
        shoes='#F4F5FA',accent='#0E7C74',sole='#F0F1F5',watch=True,eye='#2A1A12',brow_t=1.25,h=1.0,wide=1.0,belt='#3A2A1E')
WALEED_EID=dict(WALEED); [WALEED_EID.pop(k) for k in ('jacket','cuff','belt','accent')]; WALEED_EID.update(top='#D8CFB4',trim='#BFB394',kurta=True,shalwar=True,pants='#D8CFB4',wide=1.12,topi='#F4F1EA',sandals='#5A3A22',shoes=None)
MASTER=dict(skin='#B07A50',hair='#B8B8BE',hairstyle='old',grey='#D8D8DC',beard='#E8E8EA',glasses=True,topi='#F4F1EA',top='#8A9A8C',trim='#6E7E70',kurta=True,shalwar=True,
            pants='#8A9A8C',waistcoat='#3A3A42',sandals='#3A2A1E',eye='#2A1A12',brow_t=1.3,h=.94,wide=1.1)
MASTER_EID=dict(MASTER); MASTER_EID.update(top='#1E3FA0',trim='#E8C547',pants='#F4F1EA',waistcoat='#E8C547',sandals='#C9A24A')
CAST=dict(WALEED=WALEED,WALEED_EID=WALEED_EID,MASTER=MASTER,MASTER_EID=MASTER_EID)
_r=random.Random(77); CROWD=[]
for i in range(16):
    f=i%3==1; c=dict(skin=_r.choice(['#C58C5E','#B07A50','#D9A273','#9E6A44','#C9925F']),hair=_r.choice(['#15110E','#2A1E16','#3A2A1E','#B8B8BE']),eye='#2A1A12',brow_t=_r.uniform(1,1.35),
        h=_r.uniform(.82,1.05),wide=_r.uniform(.98,1.18),top=_r.choice(['#C8372D','#2E6B4F','#E8C547','#5A7FB0','#9A3A5A','#F4F1EA','#7A4A8A','#E28A3A','#3A8A9A']),kurta=_r.random()<.7,shalwar=True,
        sandals=_r.choice(['#3A2A1E','#5A3A22','#2A2C34']))
    c['trim']=shade(c['top'],.8); c['pants']=_r.choice([c['top'],'#F4F1EA','#2A2C34'])
    if f: c.update(hairstyle=_r.choice(['bun','ponytail','braid' if False else 'bob']),dupatta=_r.choice(['#E8C547','#F4F1EA','#D9367A','#5AB0A0']),earrings=True,bangles=True,lashes=True)
    else: c.update(hairstyle=_r.choice(['short','curly','quiff','old']),**({'beard':c['hair']} if _r.random()<.35 else {}),**({'topi':'#F4F1EA'} if _r.random()<.3 else {}))
    CROWD.append(c)
