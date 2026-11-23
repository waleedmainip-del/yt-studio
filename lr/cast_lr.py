# Cast for "Lahore - Everyone Is Secretly Rich" (Pakistan city series, episode 1)
# WALEED is the ONE fixed series character: this exact dict is reused unchanged in every episode.
WALEED=dict(skin='#C58C5E',hair='#15110E',hairstyle='quiff',textured=True,highlights='#5A3A20',jacket='#0E7C74',top='#F4F1EA',trim='#F4E9C8',pants='#22283A',cuff=True,
            shoes='#F4F5FA',accent='#0E7C74',sole='#F0F1F5',watch=True,eye='#2A1A12',brow_t=1.25,h=1.0,wide=1.0,belt='#3A2A1E')
# episode cast (new looks each episode)
BILAL=dict(skin='#B57A4E',hair='#120F0D',hairstyle='short',neat=True,beard='#120F0D',jacket='#7A1F2E',top='#16171C',trim='#5A1420',pants='#2A2C34',shoes='#3A2414',accent='#3A2414',sole='#1E120A',
           shades='up',shade_c='#D9B24A',chain=True,eye='#2A1A12',brow_t=1.35,h=.985,wide=1.12)
SHERRY=dict(skin='#D2A074',hair='#2A1B14',hairstyle='fringe',glasses=True,top='#8FB8D8',trim='#6A94B8',button='#F4F1EA',rolled=True,pants='#C9B48A',shoes='#F4F5FA',accent='#6A94B8',sole='#F0F1F5',
            eye='#2A1A12',h=.966,wide=.95,belt='#5A3A22')
WAITER=dict(skin='#A86F47',hair='#16110E',hairstyle='short',neat=True,stache='#16110E',top='#F8F6F0',trim='#E6E2D8',waistcoat='#16171C',bowtie='#7A1F2E',pants='#16171C',shoes='#101014',accent='#101014',sole='#101014',
            towel='#F4F1EA',eye='#2A1A12',h=.99,wide=1.0)
# washing-up versions (same people, aprons on, jackets off)
def _apr(C,col='#F4F1EA'):
    d=dict(C); d['apron']=col; d.pop('jacket',None); d['rolled']=True; return d
WALEED_K=_apr(dict(WALEED,top='#F4F1EA',trim='#DAD6CC')); BILAL_K=_apr(dict(BILAL,shades=None,trim='#2A2C34')); SHERRY_K=_apr(SHERRY)
BILAL_K={k:v for k,v in BILAL_K.items() if v is not None}
