# cast for "Huss Huss" - new designs
HUSS=dict(skin='#B97A4E',hair='#141210',hairstyle='quiff',mustache='#1A1512',brow_c='#141210',top='#EDEAE4',jacket='#1C1D22',trim='#2C2D33',sleeve='#1C1D22',
          pants='#25262C',boots='#141418',belt='#141418',buckle='#8E95A3',h=1.1,gloves=None)
VILL=dict(skin='#D9A074',hair='#1E1A18',hairstyle='bald',beard='#3B2314',brow_c='#2A1B14',top='#3A1212',trim='#7A1414',vest='#8E1E1E',pants='#2A2A30',
          boots='#1B1B1F',gloves='#2A2A30',h=1.38,military=True)
COP=dict(skin='#E8B48C',hair='#3B2314',hairstyle='cap',cap='#1B2A4A',capstar=True,top='#8FB8E0',trim='#6E98C2',pants='#1B2A4A',shoes='#15161A',
         emblem='#D9B24A',tie='#1B2A4A',h=1.0,brow_c='#3B2314',belt='#15161A',buckle='#C9CDD6',radio=True)
TOUGH=dict(skin='#C98F62',hair='#2A1B14',hairstyle='cap',cap='#C9452E',top='#E8E4D8',pants='#3E4A5C',shoes='#22242B',short=True,h=1.12,brow_c='#2A1B14',beard='#2A1B14',chain=True)
def cop(seed):
    r=random.Random(seed*13+5); c=dict(COP); c['skin']=r.choice(SK); c['hair']=r.choice(HR[:3]); c['h']=r.choice([.96,1.0,1.04]); c['mustache']=c['hair'] if r.random()<.3 else None
    if not c['mustache']: del c['mustache']
    return c
def minion(seed):
    r=random.Random(seed*7+3)
    return dict(skin=r.choice(SK),hair='#141418',hairstyle='helmet',helmet='#2A2B30',top='#4A4C55',trim='#3A3C44',pants='#33353C',boots='#15161A',vest='#5A5C66',
                gloves='#15161A',h=r.choice([.98,1.02,1.06]),brow_c='#141418',emblem='#C9302C',military=True)
CIT_TOP=['#3B8E8C','#C65D4A','#6C5FB0','#4C7FC2','#8BB85A','#D98AA8','#F2EBDD','#5A6170','#B8683A','#2E7D5A']
CIT_PN=['#2E3A4E','#5C4A3A','#D8D0C2','#3E5E5A','#22242B','#6B4E6E']
def citizen(seed,kid=False):
    r=random.Random(seed*29+11)
    c=dict(skin=r.choice(SK),hair=r.choice(HR),hairstyle=r.choice(['quiff','fringe','bob','long','bun','short','ponytail','curly','old']),top=r.choice(CIT_TOP),pants=r.choice(CIT_PN),
           shoes=r.choice(['#F4F5FA','#22242B','#C9A27A','#3A2A1E','#8E3B32']),accent=r.choice(['#D2473A','#FFFFFF','#22242B']),
           h=(r.choice([.74,.78,.82]) if kid else r.choice([.94,.97,1.0,1.03,1.06])),short=r.random()<.3)
    if r.random()<.45: c['jacket']=r.choice(CIT_TOP); c['top']=r.choice(['#F4F1EA','#E9EAF0','#2B2C33'])
    if r.random()<.2: c['scarf']=r.choice(CIT_TOP)
    if kid and r.random()<.6: c['pack']=r.choice(CIT_TOP)
    if not kid and r.random()<.2: c['bag']=r.choice(['#7A4A22','#22242B','#A8362C'])
    if not kid and r.random()<.18: c['glasses']=True
    return c
