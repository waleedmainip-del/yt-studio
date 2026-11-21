# cast for "The City Under the Dome" - all new designs, nobody in a yellow hoodie
NOVA=dict(skin='#D6A27A',hair='#2FA3E8',hairstyle='bob',brow_c='#1C5E8C',top='#E8743B',trim='#2E6E78',sleeve='#E8743B',pants='#2E6E78',
          shoes='#3A2E28',accent='#F2C14E',sole='#22242B',boots='#3A2E28',gloves='#3A3D47',cuff=True,cargo=True,h=.86,
          emblem='#F2C14E',belt='#4A3526',buckle='#C9CDD6')
POPS=dict(skin='#E3B48E',hair='#C9CBD0',hairstyle='old',beard='#D8D9DD',mustache='#D8D9DD',glasses=True,brow_c='#BFC2C8',top='#4F6E7E',trim='#3E5866',
          pants='#4F6E7E',shoes='#2B241E',apron='#7A5A3A',accent='#B8873A',h=.96,cuff=True)
BRANDT=dict(skin='#F0C9A6',hair='#4A4C55',hairstyle='quiff',mustache='#2B2C33',brow_c='#2B2C33',top='#D5D9E1',jacket='#C3C8D2',trim='#7F8796',sleeve='#C3C8D2',
            pants='#8E95A3',shoes='#22242B',accent='#1E5FA8',h=1.08,medals=['#D9B24A','#C9452E','#2B58C9'],emblem='#1E5FA8',tie='#1E5FA8',belt='#2B2C33',buckle='#D9B24A')
def guard(seed):
    r=random.Random(seed*17+9)
    return dict(skin=r.choice(SK),hair='#1E1A18',hairstyle='helmet',helmet='#1F2E4A',top='#2A3B5C',trim='#1B2740',pants='#24324E',boots='#15181F',
                vest='#33476B',gloves='#15181F',h=r.choice([1.0,1.03,1.06]),brow_c='#1E1A18',radio=True,emblem='#E3A33A',military=True)
def painter(seed):
    r=random.Random(seed*7+1); c=dict(skin=r.choice(SK),hair=r.choice(HR),hairstyle='cap',cap='#E8E4D8',top='#E8E4D8',trim='#C9C3B4',pants='#E8E4D8',
          shoes='#7A6A5A',h=r.choice([.97,1.0,1.03]),gloves='#3B6FB6',brow_c='#2A1B14'); return c
CIT_TOP=['#3B8E8C','#C65D4A','#E0B25A','#6C5FB0','#4C7FC2','#8BB85A','#D98AA8','#F2EBDD','#5A6170','#B8683A']
CIT_PN=['#2E3A4E','#5C4A3A','#D8D0C2','#3E5E5A','#22242B','#6B4E6E']
def citizen(seed,kid=False):
    r=random.Random(seed*29+11)
    c=dict(skin=r.choice(SK),hair=r.choice(HR),hairstyle=r.choice(['quiff','fringe','bob','long','bun','short','ponytail','curly','old']),top=r.choice(CIT_TOP),pants=r.choice(CIT_PN),
           shoes=r.choice(['#F4F5FA','#22242B','#C9A27A','#3A2A1E','#8E3B32']),accent=r.choice(['#D2473A','#FFFFFF','#22242B','#E0B25A']),
           h=(r.choice([.74,.78,.82]) if kid else r.choice([.94,.97,1.0,1.03,1.06])),short=r.random()<.3)
    if r.random()<.45: c['jacket']=r.choice(CIT_TOP); c['top']=r.choice(['#F4F1EA','#E9EAF0','#2B2C33'])
    if r.random()<.2: c['scarf']=r.choice(CIT_TOP)
    if kid and r.random()<.6: c['pack']=r.choice(CIT_TOP)
    if not kid and r.random()<.18: c['glasses']=True
    if c['top']=='#E0B25A' and not c.get('jacket'): c['top']='#C65D4A'
    return c
