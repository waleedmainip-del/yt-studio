# Cast for "Lahore Lahore Ayy!" (all new looks)
HAMZA=dict(skin='#C69062',hair='#120F0D',hairstyle='quiff',textured=True,highlights='#7A4A22',top='#16171C',trim='#F4F1EA',button='#F4F1EA',pants='#5A7AA8',kurta=True,shoes='#7A3A1E',accent='#7A3A1E',sole='#3A1E10',
           shades='up',shade_c='#C8372D',chain=True,watch=True,eye='#2A1A12',brow_t=1.3,h=1.0,wide=1.0)
AMMI=dict(skin='#C98F62',hair='#2A1B14',hairstyle='bun',lashes=True,earrings=True,bangles=True,top='#E8A01A',trim='#C8372D',pants='#E8A01A',kurta=True,dupatta='#C8372D',dupatta_trim='#F2C14E',sandals='#3A2414',eye='#2A1A12',h=.92,wide=1.15,button='#C8372D')
CARGUY=dict(skin='#B57A4E',hair='#120F0D',hairstyle='cap',cap='#16171C',top='#C8372D',trim='#9A2A22',pants='#16171C',shoes='#F4F5FA',accent='#C8372D',sole='#F0F1F5',chain=True,shades='eyes',shade_c='#16171C',eye='#2A1A12',h=1.02,wide=1.1,short=True)
TRAVELER=dict(skin='#C98F62',hair='#2A1B14',hairstyle='fringe',jacket='#4F7A3A',top='#E8D8B0',trim='#3A5A2A',pants='#C9B48A',shoes='#6B4A2E',accent='#6B4A2E',sole='#3A2414',pack='#E8641E',eye='#2A1A12',h=.96,wide=1.0)
LOREGUY=dict(skin='#A86F47',hair='#1B1512',hairstyle='curly',stache='#1B1512',top='#7448C2',trim='#F2C14E',pants='#F4F1EA',kurta=True,shalwar=True,sandals='#3A2414',eye='#2A1A12',h=.92,wide=1.25,glasses=True,button='#F2C14E')
TOURIST=dict(skin='#F4D2B8',hair='#E8C878',hairstyle='short',neat=True,top='#9FC8E8',trim='#7FA8C8',stripe='#F4F1EA',pants='#C9B48A',shoes='#6B4A2E',accent='#6B4A2E',sole='#3A2414',pack='#2B5AA8',eye='#3A6A9A',brow_c='#C8A858',h=1.15,wide=1.0,short=True)
TOURIST_L=dict(TOURIST,top='#F4F1EA',trim='#E0DACC',pants='#F4F1EA',kurta=True,shalwar=True,waistcoat='#16171C',shades='eyes',shade_c='#16171C',pack=None,sandals='#7A3A1E',chain=True,button='#D9B24A',stripe=None,short=False)
TOURIST_L={k:v for k,v in TOURIST_L.items() if v is not None}
import random as _r
def crowd_cast(n,seed=1):
    r=_r.Random(seed); out=[]
    for i in range(n):
        kurta=r.random()<.6; c=r.choice(['#F4F1EA','#BFD6E8','#E8D8B0','#2B5AA8','#5A3A22','#C8372D','#7448C2','#2B8A5A','#E8709A','#F2C14E'])
        d=dict(skin=r.choice(['#C69062','#B57A4E','#A86F47','#D9A57A','#9A5E38']),hair=r.choice(['#120F0D','#2A1B14','#4A3020']),hairstyle=r.choice(['short','fringe','curly','quiff','cap','old']),
               top=c,trim=c,pants=c if kurta else r.choice(['#3A3D44','#2A3350','#6B6050']),kurta=kurta,shalwar=kurta,eye='#2A1A12',h=r.uniform(.9,1.08),wide=r.uniform(.95,1.25),
               cap=r.choice(['#C8372D','#2B5AA8','#16171C']),stache=r.choice(['#120F0D',None,None]),sandals='#3A2416' if kurta else None,shoes='#16171C',accent='#16171C',sole='#F0F1F5')
        out.append({k:v for k,v in d.items() if v is not None})
    return out
