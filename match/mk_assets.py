from PIL import Image,ImageDraw,ImageFont
import os,math
os.chdir('/home/claude/match'); A='assets/'
F='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
def f(s): return ImageFont.truetype(F,s)
def fm(s): return ImageFont.truetype(FM,s)
TW,TH=1280,720
def field(d):
    d.rectangle((0,0,TW,TH),fill='#2E7D3A')
    for k in range(10): d.rectangle((0,k*72,TW,k*72+36),fill='#2A7536')
    d.rectangle((560,120,720,600),fill='#C9B48A'); d.rectangle((600,140,680,160),fill='#F4F5FA'); d.rectangle((600,560,680,580),fill='#F4F5FA')
def scorebar(d,txt,need='NEED 12 OFF 6'):
    d.rectangle((0,TH-110,TW,TH),fill='#0B1F3A'); d.rectangle((0,TH-110,300,TH),fill='#0B7A3B')
    d.text((150,TH-55),'PAK',font=f(64),fill='white',anchor='mm'); d.text((330,TH-55),txt,font=f(56),fill='white',anchor='lm')
    d.rounded_rectangle((820,TH-95,TW-20,TH-15),18,fill='#F2C12E'); d.text((1050,TH-55),need,font=f(44),fill='#0B1F3A',anchor='mm')
    d.rounded_rectangle((20,20,300,80),14,fill='#C8102E'); d.text((160,50),'FINAL · LIVE',font=f(34),fill='white',anchor='mm')
def tv(fn,txt,need,big=None,bigc='#F2C12E',sub=None):
    im=Image.new('RGB',(TW,TH)); d=ImageDraw.Draw(im); field(d)
    # batsman + bowler silhouettes (blocky)
    for (x,y,c) in ((640,470,'#0B7A3B'),(640,200,'#1D3E8A')): d.rectangle((x-30,y-90,x+30,y+20),fill=c); d.rectangle((x-22,y-140,x+22,y-92),fill='#B98A62')
    scorebar(d,txt,need)
    if big:
        d.rounded_rectangle((TW/2-360,TH/2-150,TW/2+360,TH/2+60),40,fill='#0B1F3A'); d.text((TW/2,TH/2-45),big,font=f(150),fill=bigc,anchor='mm')
        if sub: d.text((TW/2,TH/2+110),sub,font=f(46),fill='white',anchor='mm',stroke_width=4,stroke_fill='#0B1F3A')
    im.save(A+fn+'.png')
tv('tv_score','168/6  (19 ov)','NEED 12 OFF 6')
tv('tv_lastover','168/6  (19 ov)','NEED 12 OFF 6',big='LAST OVER',bigc='#FFFFFF')
tv('tv_four','172/6  (19.1)','NEED 8 OFF 5',big='FOUR!')
tv('tv_dot','172/6  (19.2)','NEED 8 OFF 4',big='DOT BALL',bigc='#FFFFFF')
tv('tv_caught','172/7  (19.3)','REPLAY',big='CAUGHT!',bigc='#FF5A5A',sub='Not a six. Caught at the boundary.')
im=Image.new('RGB',(TW,TH),'#3A1E3A'); d=ImageDraw.Draw(im)
d.rectangle((0,0,TW,TH),fill='#4A2A4A'); d.rectangle((0,420,TW,TH),fill='#2A1A2A')
for (x,skin,hair,shawl,ang) in ((420,'#C99468','#1E1612','#C8102E',1),(860,'#B98A62','#4A3A30','#E8DCC4',-1)):
        d.rectangle((x-150,330,x+150,620),fill=shawl); d.rectangle((x-110,110,x+110,330),fill=skin); d.rectangle((x-130,80,x+130,150),fill=hair); d.rectangle((x-130,80,x-100,330),fill=hair); d.rectangle((x+100,80,x+130,330),fill=hair)
        for ex in (-45,45): d.ellipse((x+ex-18,200,x+ex+18,240),fill='#111111'); d.line([(x+ex-28,180+ang*ex*.2),(x+ex+28,180-ang*ex*.2)],fill='#111111',width=10)
        d.line([(x-40,290),(x+40,280)],fill='#7A1E2E',width=10)
d.rectangle((0,TH-120,TW,TH),fill='#1A0E1A'); d.text((40,TH-60),'MERI SAAS KA PYAAR  ·  Episode 214',font=f(48),fill='#FFD6E8',anchor='lm'); d.text((TW-40,TH-60),'9:00 PM',font=f(48),fill='#FFFFFF',anchor='rm')
d.text((TW/2,560),'"Tum ne meri chai mein cheeni kyun dali?!"',font=f(46),fill='white',anchor='mm',stroke_width=4,stroke_fill='#1A0E1A')
im.save(A+'tv_drama.png')
for nm,col,txt,bars in (('ups_dead','#E8303A','BATTERY 0%',0),('ups_full','#22C55E','BATTERY 100%',5)):
    im=Image.new('RGB',(300,400),'#1A1B22'); d=ImageDraw.Draw(im); d.text((150,50),'UPS',font=f(56),fill='#C9CDD6',anchor='mm')
    d.rectangle((70,110,230,330),outline='#C9CDD6',width=8); d.rectangle((120,92,180,110),fill='#C9CDD6')
    for k in range(5): d.rectangle((86,300-k*42,214,330-k*42),fill=col if k<bars else '#2B2C33')
    if bars==0: d.rectangle((86,300,214,330),fill=col)
    d.text((150,370),txt,font=f(34),fill=col,anchor='mm'); im.save(A+nm+'.png')
W,H=540,1080
im=Image.new('RGB',(W,H),'#000000'); d=ImageDraw.Draw(im); d.text((30,30),'9:47',font=f(26),fill='white')
for k in range(4): d.rectangle((460+k*12,54-k*6,468+k*12,58),fill='white' if k<1 else '#4A5563')
p=Image.open(A+'tv_score.png').resize((W,int(W*TH/TW))); p=p.point(lambda v:v*.45); im.paste(p,(0,330))
cx,cy=W/2,330+p.height/2
for k in range(8):
    a=k*math.pi/4; d.ellipse((cx+46*math.cos(a)-10,cy+46*math.sin(a)-10,cx+46*math.cos(a)+10,cy+46*math.sin(a)+10),fill=(255,255,255) if k<5 else (120,120,120))
d.text((W/2,cy+110),'Buffering...',font=f(40),fill='white',anchor='mm'); d.text((W/2,880),'LIVE · 0.2 Mbps',font=fm(28),fill='#E8303A',anchor='mm'); im.save(A+'ph_buffer.png')
print('ok')
