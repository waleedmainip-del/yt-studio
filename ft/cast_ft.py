# Cast for "Faisalabad: The Textile Kingdom" (all new looks)
JUNAID=dict(skin='#C08A5C',hair='#15120F',hairstyle='quiff',textured=True,highlights='#5A3A22',jacket='#2A2C34',top='#F4F1EA',trim='#16171C',stripe='#D9B24A',pants='#16171C',shoes='#7A3A1E',accent='#7A3A1E',sole='#3A1E10',
            shades='up',shade_c='#C9A24A',watch=True,eye='#2A1A12',brow_t=1.2,h=1.0,wide=.95)
RASHID=dict(skin='#A86F47',hair='#B8B8BC',hairstyle='old',receding=True,stache='#C8C8CC',top='#F4F1EA',trim='#E0DACC',pants='#F4F1EA',kurta=True,shalwar=True,waistcoat='#5A5E66',scarf='#F2C14E',
            sandals='#3A2416',eye='#1E1612',brow_c='#C8C8CC',brow_t=1.6,h=1.0,wide=1.2,button='#D9B24A',glasses=True)
BILAL=dict(skin='#C69062',hair='#1A1411',hairstyle='curly',top='#F28A3A',trim='#C8372D',stripe='#2B8A5A',pants='#2A3350',shoes='#F4F5FA',accent='#F28A3A',sole='#F0F1F5',eye='#2A1A12',h=1.08,wide=.85,short=True,cheeks=True)
DANISH=dict(skin='#B57A4E',hair='#120F0D',hairstyle='cap',cap='#16909E',top='#2B8A5A',trim='#1F6A44',stripe='#F4F1EA',hoodie=True,pants='#3A3D44',shoes='#16171C',accent='#2B8A5A',sole='#F0F1F5',eye='#2A1A12',h=.94,wide=1.1)
SALEEM=dict(skin='#9A5E38',hair='#120F0D',hairstyle='short',stache='#120F0D',stache_style='strong',top='#7A1F2E',trim='#5A1520',pants='#7A1F2E',kurta=True,shalwar=True,waistcoat='#C9A24A',chain=True,
            sandals='#3A2416',eye='#1E1612',brow_t=1.7,h=1.02,wide=1.45,button='#D9B24A',watch=True)
BUYER=dict(skin='#F0C8A8',hair='#D8B060',hairstyle='fringe',neat=True,jacket='#1E2A44',top='#F4F5FA',trim='#16171C',tie='#C8372D',pants='#1E2A44',shoes='#16171C',accent='#16171C',sole='#16171C',
           eye='#3A6A9A',brow_c='#B8904A',h=1.12,wide=1.0,glasses=False,watch=True)
MUKHTAR=dict(skin='#8E5634',hair='#0E0C0B',hairstyle='short',stache='#0E0C0B',stache_style='strong',top='#16171C',trim='#16171C',pants='#16171C',kurta=True,shalwar=True,topi='#F4F1EA',sandals='#16171C',eye='#1E1612',brow_t=1.8,brow_w=1.3,h=1.1,wide=1.5,chain=True)
AMMI=dict(skin='#C98F62',hair='#2A1B14',hairstyle='bun',lashes=True,earrings=True,top='#7448C2',trim='#F2C14E',pants='#F1E8D4',kurta=True,dupatta='#F2C14E',sandals='#D9B24A',eye='#2A1A12',h=.92,wide=1.1)
import random as _r
def crowd_cast(n,seed=1):
    r=_r.Random(seed); out=[]
    for i in range(n):
        kurta=r.random()<.65; c=r.choice(['#F4F1EA','#BFD6E8','#E8D8B0','#2B5AA8','#5A3A22','#3A6A8A','#C8372D','#7448C2','#2B8A5A','#E8709A'])
        d=dict(skin=r.choice(['#C69062','#B57A4E','#A86F47','#D9A57A','#9A5E38']),hair=r.choice(['#120F0D','#2A1B14','#4A3020','#8A8480']),hairstyle=r.choice(['short','fringe','curly','quiff','cap','old']),
               top=c,trim=c,pants=c if kurta else r.choice(['#3A3D44','#2A3350','#6B6050']),kurta=kurta,shalwar=kurta,eye='#2A1A12',h=r.uniform(.9,1.08),wide=r.uniform(.95,1.25),
               cap=r.choice(['#C8372D','#2B5AA8','#16171C']),stache=r.choice(['#120F0D',None,None]),sandals='#3A2416' if kurta else None,shoes='#16171C',accent='#16171C',sole='#F0F1F5')
        out.append({k:v for k,v in d.items() if v is not None})
    return out
