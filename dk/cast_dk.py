# Cast for "The Guy Who Couldn't Be Killed"
DEREK=dict(skin='#F2C6A2',hair='#C8652E',hairstyle='short',scruffy=True,freckles=True,bandaid=True,hoodie=True,top='#E3A82B',trim='#B9821A',strings='#FFFFFF',
           pants='#3B5B8C',shoes='#D9473A',accent='#F4F1EA',sole='#F4F1EA',eye='#2A1A12',brow_c='#A84E22',brow_t=1.25,brow_w=1.1,h=.98)
DEATH=dict(skin='#E9E4D6',hair='#16141C',hairstyle='bald',death=True,top='#17151D',trim='#0E0D12',pants='#17151D',shoes='#0E0D12',sole='#0E0D12',accent='#0E0D12',
           eye='#0A0608',brow_c='#7A7468',brow_t=1.6,brow_w=1.1,glowc='#FF3B2F',h=1.3,wide=1.06,face_w=.4)
MOM=dict(skin='#EFC09C',hair='#6A4A3A',hairstyle='bun',curlers=True,robe=True,top='#E79AB8',trim='#C97A9A',pants='#E79AB8',shoes='#F4F1EA',accent='#F28BB0',sole='#F4F1EA',
         glasses=True,earrings=True,lashes=True,eye='#2A1A12',brow_c='#5A3A2A',brow_t=1.35,h=.92,wide=1.12,face_w=.6)
MOVER=dict(skin='#C98F62',hair='#2A2420',hairstyle='cap',cap='#2F5E9E',top='#F4F1EA',pants='#2F5E9E',overalls='#2F5E9E',shoes='#5E3A1E',accent='#3A2A1E',sole='#2A1E14',mustache='#2A2420',h=1.0,wide=1.12)
CAST=dict(DEREK=DEREK,DEATH=DEATH,MOM=MOM,MOVER=MOVER)
BG=dict(DEREK='#F4E2B8',DEATH='#3A3446',MOM='#F6D8E4',MOVER='#D8E4F2')
EXPR=dict(
 DEREK=[('clueless','smile',.03,-4,1.0,0,4,0),('hungry','o',.05,8,1.15,4,0,0),('deadpan','flat',-.01,-2,.75,0,0,0),('happy','grin',.05,-4,1.05,-4,-4,5),('surprised','O',.06,0,1.25,-4,0,0)],
 DEATH=[('menacing','flat',-.04,-26,1.0,8,0,0),('furious','shout',-.04,-30,1.1,4,0,0),('confused','flat',.05,14,1.0,0,10,-5),('smug','smirk',.02,-10,.9,-6,3,6),('exhausted','frown',.04,18,.8,10,6,0)],
 MOM=[('angry','shout',-.03,-24,1.1,0,0,0),('worried','frown',.05,16,1.1,4,0,0),('sweet','smile',.04,-2,1.0,0,-5,4)],
 MOVER=[('working','strain',.0,-8,1.0,0,0,0),('shocked','O',.06,4,1.25,-4,0,0)])
