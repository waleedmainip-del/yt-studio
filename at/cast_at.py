# Cast for "Ashraf Tawa Takes Over" — Ashraf Tawa is an invented local legend (not a real person)
PAWA=dict(skin='#C69062',hair='#1A1411',hairstyle='quiff',textured=True,highlights='#6A4A30',jacket='#C8372D',top='#F4F1EA',trim='#16171C',stripe='#F4F1EA',pants='#16171C',shoes='#F4F5FA',accent='#C8372D',sole='#F0F1F5',
          chain=True,shades='up',shade_c='#16171C',eye='#2A1A12',brow_t=1.2,h=1.05,wide=.9)
JOJO=dict(skin='#B57A4E',hair='#15120F',hairstyle='cap',cap='#2B8A8A',top='#F2C14E',trim='#D9A21C',pants='#3A4A6A',shoes='#16171C',accent='#2B8A8A',sole='#F0F1F5',eye='#2A1A12',h=.9,wide=1.2,cheeks=True,short=True)
ASHRAF=dict(skin='#A8693E',hair='#120F0D',hairstyle='old',receding=True,stache='#120F0D',top='#F4F1EA',trim='#E0DACC',pants='#F4F1EA',kurta=True,shalwar=True,waistcoat='#16171C',chain=True,
            shades='eyes',shade_c='#D9B24A',sandals='#5A3420',eye='#1E1612',brow_t=1.8,brow_w=1.25,h=1.16,wide=1.42,button='#D9B24A',watch=True)
DADI=dict(skin='#B98A62',hair='#D8D8DC',hairstyle='bun',glasses=True,top='#E8E4DA',trim='#C9C2B0',pants='#E8E4DA',kurta=True,dupatta='#F4F1EA',sandals='#3A2416',eye='#2A1A12',brow_c='#A8A8AC',h=.82,wide=1.05)
GYMBRO=dict(skin='#9A5E38',hair='#0E0C0B',hairstyle='short',beard='#0E0C0B',vest='#16171C',top='#16171C',trim='#16171C',pants='#3A3D44',shoes='#C8372D',accent='#F4F1EA',sole='#F0F1F5',eye='#1E1612',h=1.1,wide=1.45,short=True)
BARBER=dict(skin='#B57A4E',hair='#8A8480',hairstyle='old',stache='#8A8480',top='#F4F1EA',trim='#E0DACC',pants='#5A5E66',apron='#2B8A8A',shoes='#16171C',accent='#16171C',sole='#16171C',eye='#2A1A12',h=.96,wide=1.05)
CUST=dict(skin='#C98F62',hair='#1E1612',hairstyle='fringe',top='#7448C2',trim='#5A38A0',pants='#3A3D44',shoes='#F4F5FA',accent='#7448C2',sole='#F0F1F5',eye='#2A1A12',h=.95,towel=True)
DHOLI=dict(skin='#A86F47',hair='#1B1512',hairstyle='short',stache='#1B1512',topi='#F2C14E',top='#2B8A5A',trim='#1F6A44',pants='#F4F1EA',kurta=True,shalwar=True,sandals='#3A2416',eye='#2A1A12',h=1.0,wide=1.1)
import random as _r
def crowd_cast(n,seed=1):
    r=_r.Random(seed); out=[]
    for i in range(n):
        kurta=r.random()<.6; c=r.choice(['#C8372D','#2B5AA8','#2B8A5A','#F2C14E','#7448C2','#F28A3A','#F4F1EA','#5A3A22','#3A6A8A','#CF3F78'])
        d=dict(skin=r.choice(['#C69062','#B57A4E','#A86F47','#D9A57A','#9A5E38']),hair=r.choice(['#120F0D','#2A1B14','#4A3020']),hairstyle=r.choice(['short','fringe','curly','quiff','cap','old']),
               top=c,trim=c,pants=c if kurta else r.choice(['#3A3D44','#2A3350','#6B6050']),kurta=kurta,shalwar=kurta,eye='#2A1A12',h=r.uniform(.88,1.08),wide=r.uniform(.95,1.25),
               cap=r.choice(['#C8372D','#2B5AA8','#16171C']),stache=r.choice(['#120F0D',None,None]),beard=r.choice(['#120F0D',None,None,None]),sandals='#3A2416' if kurta else None,
               shoes='#16171C',accent='#16171C',sole='#F0F1F5')
        out.append({k:v for k,v in d.items() if v is not None})
    return out
