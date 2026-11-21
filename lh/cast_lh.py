# Cast for "In This World, Everyone Is Lahori" - approved design directions from the production brief.
HAMZA=dict(skin='#B97A4E',hair='#2E1C12',hairstyle='quiff',textured=True,top='#0E6F6C',trim='#0A5053',pants='#EFE6D2',cuff=True,kurta=True,shalwar=True,
           sandals='#7A4A22',watch=True,eye='#2A1A12',brow_c='#2E1C12',brow_t=1.25,brow_w=1.05,h=1.0,button='#E8D9B0')
CHACHA=dict(skin='#C08A5C',hair='#2A2420',hairstyle='bald',receding=True,grey='#A2A2AA',top='#EFE6D2',trim='#D6C9AE',pants='#EFE6D2',cuff=True,kurta=True,shalwar=True,
            sandals='#5E3A1E',waistcoat='#6B4A2E',stache='#2A2420',stache_style='handlebar',eye='#2A1A12',brow_c='#2A2420',brow_t=1.5,brow_w=1.12,h=.86,wide=1.16,face_w=.9,button='#8A6A3C')
ZARA=dict(skin='#C9905F',hair='#1A1210',hairstyle='bob',braid=True,top='#D9A21B',trim='#7A1F2E',pants='#7A1F2E',kurta=True,shalwar=True,dupatta='#7A1F2E',dupatta_trim='#E6B53A',
          shoes='#F4F5FA',accent='#D9A21B',sole='#F0F1F5',lashes=True,earrings=True,bangles=True,eye='#2A1A12',brow_c='#1A1210',h=.95,button='#E6B53A',tie_c='#D9A21B')
BILAL=dict(skin='#C98F62',hair='#15120F',hairstyle='short',neat=True,cheeks=True,top='#8FD9B6',trim='#5FB892',pants='#F7F5EF',cuff=True,kurta=True,shalwar=True,
           shoes='#F4F5FA',accent='#35975A',sole='#F0F1F5',eye='#2A1A12',brow_t=1.3,h=.97,wide=1.13,face_w=.95,button='#F7F5EF')
ZORAK=dict(skin='#7E6F9A',hair='#4A3F63',hairstyle='bald',alien=True,top='#23252E',trim='#15161C',pants='#1E2028',boots='#2B2F3A',gloves='#2B2F3A',belt='#2B2F3A',buckle='#35C8FF',
           eye='#0B0B12',brow_c='#5A4A7A',brow_t=1.45,brow_w=1.15,h=1.24,wide=1.1,face_w=.3)
JAMEEL=dict(skin='#B5794E',hair='#1B1512',hairstyle='short',top='#F7F5EF',trim='#D9D4C6',pants='#F7F5EF',cuff=True,kurta=True,shalwar=True,sandals='#3E2A1A',apron='#1F4D3A',
            short=True,rolled=True,stache='#1B1512',stache_style='strong',towel='#C8372D',ladle=True,topi='#F7F5EF',eye='#2A1A12',brow_t=1.35,brow_w=1.08,h=1.02,wide=1.1,face_w=.6,button='#D9D4C6')
CAST=dict(HAMZA=HAMZA,CHACHA=CHACHA,ZARA=ZARA,BILAL=BILAL,ZORAK=ZORAK,JAMEEL=JAMEEL)
BG=dict(HAMZA='#CFE8E4',CHACHA='#F0E2C8',ZARA='#F2D9C4',BILAL='#D6F0E0',ZORAK='#D4D0EA',JAMEEL='#E4EAD8')
# expression sets: (label, mouth, brow lift, brow tilt, eye scale, head pitch, head roll, head yaw)
EXPR=dict(
 HAMZA=[('confident','smirk',.0,-10,1.0,0,3,-8),('surprised','O',.06,-2,1.2,-4,0,0),('amused','grin',.02,-6,.92,2,-4,6),('worried','strain',.03,14,1.05,4,3,0),('shocked','shout',.06,4,1.3,-8,0,0)],
 CHACHA=[('annoyed','frown',-.02,-22,.85,4,0,-6),('proud','smirk',.03,-6,.95,-8,2,6),('confused','flat',.05,12,1.05,0,10,-4),('suspicious','flat',-.03,-16,.7,2,-6,10),('delighted','grin',.05,-2,1.0,-4,-3,0)],
 ZARA=[('sarcastic','smirk',.04,-12,.8,0,6,-10),('confident','smile',.01,-8,1.0,-4,0,6),('frightened','O',.06,14,1.3,-4,0,0),('amused','grin',.03,-4,.95,2,-5,4),('determined','flat',-.02,-18,.95,3,0,0)],
 BILAL=[('hungry','o',.05,6,1.2,6,0,0),('excited','grin',.06,-2,1.2,-6,0,0),('shocked','shout',.06,6,1.3,-6,0,0),('disappointed','frown',.02,16,.9,10,4,0),('happy','smile',.03,-4,1.0,0,-4,5)],
 ZORAK=[('intimidating','flat',-.04,-24,.85,6,0,0),('confused','flat',.05,12,1.05,0,10,-6),('amazed','O',.06,0,1.25,-6,0,0),('too spicy','strain',.04,16,1.15,-4,5,0),('delighted','grin',.05,-4,1.05,-4,-4,5)],
 JAMEEL=[('calm','flat',.0,-5,.9,0,0,0),('proud','smirk',.03,-8,.95,-8,0,6),('serious','flat',-.03,-18,.9,3,0,0),('amused','smile',.03,-4,.95,0,-4,-5),('satisfied','smile',.02,-2,.75,-3,3,0)])
