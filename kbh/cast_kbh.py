# Cast for "Everyone Is a Bhaiya from Karachi" — every character has a distinct silhouette, palette and accessory.
WALEED=dict(skin='#C58C5E',hair='#15110E',hairstyle='quiff',textured=True,highlights='#5A3A20',jacket='#2B3F7A',top='#F2E8D0',trim='#E8B23A',pants='#8A7A5A',cargo=True,
        shoes='#F4F5FA',accent='#E8B23A',sole='#F0F1F5',watch=True,pack='#C8372D',eye='#2A1A12',brow_t=1.25,h=1.0,wide=1.0)
DOODH=dict(skin='#9E6A44',hair='#2A1E16',hairstyle='short',mustache='#1A1412',stache_style='thick',top='#F4F1EA',trim='#DAD6CC',kurta=True,shalwar=True,pants='#2E5A9A',
        topi='#E2702A',sandals='#5A3A22',scarf='#C8372D',eye='#2A1A12',brow_t=1.4,h=.92,wide=1.02)
POLICE=dict(skin='#B07A50',hair='#15110E',hairstyle='cap',mustache='#15110E',top='#16171C',trim='#2A2C34',pants='#B8A27A',belt='#3A2A1E',cap='#16171C',capstar='#E8C547',
        shades='#16171C',radio=True,shoes='#16171C',military=True,eye='#2A1A12',brow_t=1.5,h=1.04,wide=1.18)
MAN1=dict(skin='#C9925F',hair='#8A8A90',hairstyle='old',beard='#D8D8DC',glasses=True,topi='#F4F1EA',top='#2E6B4F',trim='#1E4A36',kurta=True,shalwar=True,pants='#2E6B4F',
        waistcoat='#7A5A2E',sandals='#3A2A1E',eye='#2A1A12',brow_t=1.3,h=1.08,wide=.94)
MAN2=dict(skin='#D9A273',hair='#15110E',hairstyle='curly',top='#E2702A',trim='#F4D35E',pants='#2A2C34',chain='#E8C547',shades='#16171C',shoes='#C8372D',sole='#F0F1F5',
        eye='#2A1A12',brow_t=1.2,h=.86,wide=1.2)
BIRYANI=dict(skin='#A9744C',hair='#15110E',hairstyle='short',receding=True,mustache='#15110E',stache_style='thick',vest='#F4F1EA',top='#F4F1EA',trim='#F4F1EA',pants='#3A3A42',apron='#E8A040',
        towel='#C8372D',ladle=True,sandals='#2A2C34',eye='#2A1A12',brow_t=1.55,h=1.0,wide=1.34)
UNCLE=dict(skin='#B98A62',hair='#D8D8DC',hairstyle='old',grey='#E8E8EA',beard='#F4F1EA',glasses=True,jacket='#C9B48A',top='#C9B48A',trim='#A8956A',pants='#C9B48A',
        topi='#3A3A42',sandals='#5A3A22',eye='#2A1A12',brow_t=1.3,h=.95,wide=1.12)
SHOPKEEP=dict(skin='#C58C5E',hair='#2A1E16',hairstyle='fringe',top='#7A1E2E',trim='#E8C547',kurta=True,shalwar=True,pants='#7A1E2E',scarf='#F4D35E',watch=True,
        sandals='#3A2A1E',eye='#2A1A12',brow_t=1.3,h=.97,wide=1.05)
RICKSHAW=dict(skin='#9E6A44',hair='#15110E',hairstyle='cap',beard='#15110E',cap='#2E8A6A',top='#8A6A4A',trim='#6E5236',kurta=True,shalwar=True,pants='#8A6A4A',
        scarf='#E8E2D0',sandals='#2A2C34',eye='#2A1A12',brow_t=1.35,h=.98,wide=1.08)
COUNTER=dict(skin='#C9925F',hair='#15110E',hairstyle='neat',neat=True,top='#F4F5FA',trim='#DAD6CC',vest='#1E2E5A',tie='#C8372D',pants='#1E2E5A',shoes='#16171C',glasses=True,
        eye='#2A1A12',brow_t=1.2,h=1.0,wide=.98)
PILOT=dict(skin='#B07A50',hair='#2A2A2E',hairstyle='cap',mustache='#2A2A2E',top='#F4F5FA',trim='#E8C547',jacket='#16213A',tie='#16171C',pants='#16213A',cap='#16213A',capstar='#E8C547',
        shades='#2A3A5A',medals=['#E8C547','#E8C547','#C8372D'],shoes='#16171C',watch=True,eye='#2A1A12',brow_t=1.3,h=1.06,wide=1.06)
CAST=dict(WALEED=WALEED,DOODH=DOODH,POLICE=POLICE,MAN1=MAN1,MAN2=MAN2,BIRYANI=BIRYANI,UNCLE=UNCLE,SHOPKEEP=SHOPKEEP,RICKSHAW=RICKSHAW,COUNTER=COUNTER,PILOT=PILOT)
# crowd: 20 unique combos, no two share a top colour + hairstyle
_TOPS=['#C8372D','#2E6B4F','#E8C547','#5A7FB0','#D9367A','#F4F1EA','#7A4A8A','#E28A3A','#1E3FA0','#3A8A9A','#9A3A5A','#6A8A3A','#B05A3A','#2A2C34','#C9A0E0','#5AB0A0','#8A5A36','#E8956A','#4A5A6A','#D8CFB4']
_r=random.Random(55); CROWD=[]
for i,tc in enumerate(_TOPS):
    f=i%3==2; c=dict(skin=_r.choice(['#C58C5E','#B07A50','#D9A273','#9E6A44','#C9925F','#A9744C']),hair=_r.choice(['#15110E','#2A1E16','#3A2A1E','#8A8A90']),eye='#2A1A12',
        brow_t=_r.uniform(1.0,1.45),h=_r.uniform(.84,1.06),wide=_r.uniform(.96,1.24),top=tc,trim=shade(tc,.75),kurta=i%2==0,shalwar=i%2==0,sandals=_r.choice(['#3A2A1E','#5A3A22','#2A2C34']))
    c['pants']=tc if c['kurta'] else _r.choice(['#2A2C34','#3A4A6A','#8A7A5A'])
    if f: c.update(hairstyle=['bun','ponytail','bob'][i%3],dupatta=_r.choice(['#E8C547','#F4F1EA','#D9367A','#5AB0A0']),earrings=True,bangles=True,lashes=True)
    else:
        c.update(hairstyle=['short','curly','quiff','old','fringe'][i%5])
        x=i%4
        if x==0: c['mustache']=c['hair']
        elif x==1: c['beard']=c['hair']; c['topi']='#F4F1EA'
        elif x==2: c['cap']=_r.choice(['#C8372D','#2E5A9A','#16171C'])
        else: c['glasses']=True
    CROWD.append(c)
