# Cast for "Khana Khul Gaya". WALEED keeps his face/hair; wedding look = cream kurta + maroon waistcoat.
WALEED=dict(skin='#C58C5E',hair='#15110E',hairstyle='quiff',textured=True,highlights='#5A3A20',top='#F2E8D0',trim='#D8C8A0',kurta=True,shalwar=True,pants='#F2E8D0',
        waistcoat='#7A1E2E',sandals='#3A2A1E',eye='#2A1A12',brow_t=1.25,h=1.0,wide=1.04,watch=True)
AMMI=dict(skin='#C9925F',hair='#1A1412',hairstyle='bun',top='#1E7A5A',trim='#E8C547',kurta=True,shalwar=True,pants='#F4F1EA',dupatta='#E8C547',dupatta_trim='#1E7A5A',
          earrings=True,bangles=True,lashes=True,sandals='#C9A24A',eye='#2A1A12',brow_t=1.3,h=.92,wide=1.12)
PLATE_AUNTY=dict(skin='#B98A62',hair='#2A1E16',hairstyle='bob',top='#7A3A9A',trim='#E8C547',kurta=True,shalwar=True,pants='#2A1E3A',dupatta='#C9A0E0',dupatta_trim='#7A3A9A',
          earrings=True,bangles=True,lashes=True,glasses=True,sandals='#5A3A22',eye='#2A1A12',brow_t=1.4,h=.9,wide=1.22)
SHOP_AUNTY=dict(skin='#C9925F',hair='#3A2A1E',hairstyle='bun',top='#E2702A',trim='#B0451A',kurta=True,shalwar=True,pants='#F2D6B0',dupatta='#F4D35E',dupatta_trim='#E2702A',
          earrings=True,bangles=True,lashes=True,sandals='#3A2A1E',eye='#2A1A12',brow_t=1.35,h=.88,wide=1.2)
BILAL=dict(skin='#A9744C',hair='#15110E',hairstyle='curly',beard='#15110E',top='#16171C',trim='#3A3A42',kurta=True,shalwar=True,pants='#16171C',sandals='#5A3A22',
          eye='#2A1A12',brow_t=1.3,h=1.02,wide=1.08)
UNCLE=dict(skin='#B07A50',hair='#2A2A2E',hairstyle='old',grey='#6A6A70',receding=True,mustache='#2A2A2E',top='#F4F1EA',trim='#DAD6CC',kurta=True,shalwar=True,pants='#F4F1EA',
          waistcoat='#4A5A6A',sandals='#2A2C34',eye='#2A1A12',brow_t=1.45,h=.98,wide=1.3,watch=True)
WAITER=dict(skin='#9E6A44',hair='#15110E',hairstyle='short',top='#F4F1EA',trim='#C8372D',waistcoat='#C8372D',pants='#16171C',shoes='#16171C',bowtie='#16171C',
          eye='#2A1A12',brow_t=1.2,h=1.0,wide=1.0)
CAST=dict(WALEED=WALEED,AMMI=AMMI,PLATE_AUNTY=PLATE_AUNTY,SHOP_AUNTY=SHOP_AUNTY,BILAL=BILAL,UNCLE=UNCLE,WAITER=WAITER)
_r=random.Random(91); GUESTS=[]
for i in range(18):
    f=i%2==1; c=dict(skin=_r.choice(['#C58C5E','#B07A50','#D9A273','#9E6A44','#C9925F']),hair=_r.choice(['#15110E','#2A1E16','#3A2A1E','#8A8A90']),eye='#2A1A12',brow_t=_r.uniform(1,1.35),
        h=_r.uniform(.84,1.04),wide=_r.uniform(1.0,1.2),top=_r.choice(['#C8372D','#2E6B4F','#E8C547','#5A7FB0','#D9367A','#F4F1EA','#7A4A8A','#E28A3A','#1E3FA0','#16171C']),kurta=True,shalwar=True,
        sandals=_r.choice(['#3A2A1E','#C9A24A','#2A2C34']))
    c['trim']=shade(c['top'],.75); c['pants']=_r.choice([c['top'],'#F4F1EA','#2A2C34'])
    if f: c.update(hairstyle=_r.choice(['bun','ponytail','bob']),dupatta=_r.choice(['#E8C547','#F4F1EA','#D9367A','#5AB0A0','#C9A0E0']),earrings=True,bangles=True,lashes=True)
    else: c.update(hairstyle=_r.choice(['short','curly','quiff','old']),**({'waistcoat':_r.choice(['#3A3A42','#7A5A2E','#2E4A6A'])} if _r.random()<.5 else {}),**({'mustache':c['hair']} if _r.random()<.4 else {}))
    GUESTS.append(c)
