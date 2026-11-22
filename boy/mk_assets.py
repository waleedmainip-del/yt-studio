from PIL import Image,ImageDraw,ImageFont
import math
F='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FR='/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'
def f(sz,b=True): return ImageFont.truetype(F if b else FR,sz)
W,H=540,1080
def base(bg='#101218'):
    im=Image.new('RGBA',(W,H),bg); d=ImageDraw.Draw(im); return im,d
# lock screen
im,d=base('#1B2A4A')
for y in range(H): d.line([(0,y),(W,y)],fill=(27+int(40*y/H),42+int(20*y/H),74+int(60*y/H)))
d.text((W/2,300),'11:47',font=f(150),fill='white',anchor='mm'); d.text((W/2,420),'Saturday, 14 June',font=f(34,False),fill='#DDE6F5',anchor='mm')
for i,(t,c) in enumerate((('Ammi  ·  12 missed calls','#E8505B'),('Bilal: bro uth gaya?','#2F8C99'))):
    d.rounded_rectangle((40,560+i*130,W-40,670+i*130),28,fill='#3D4F7A'); d.text((70,615+i*130),t,font=f(30),fill='white',anchor='lm')
im.save('assets/scr_lock.png')
# reels feed
def feed(k):
    im,d=base('#000000'); cols=['#E8505B','#2F8C99','#F2C12E','#7A4EC2','#3E9C5A']
    d.rectangle((0,0,W,H),fill=cols[k%5]); d.ellipse((W/2-120,H/2-160,W/2+120,H/2+80),fill=cols[(k+2)%5])
    d.text((30,40),'Reels',font=f(44),fill='white'); 
    for j,ic in enumerate(('♥','💬','➤')): d.ellipse((W-90,560+j*120,W-30,620+j*120),fill=(255,255,255,90))
    d.text((W-60,590),'♥',font=f(34),fill='white',anchor='mm')
    d.text((30,H-150),'@daily.funny.clips',font=f(28),fill='white'); d.text((30,H-105),'wait for it... 😂'.replace('😂',''),font=f(28,False),fill='white')
    im.save('assets/scr_feed%d.png'%k)
for k in range(4): feed(k)
# cat falling video (6 frames)
def cat(k):
    im,d=base('#F4E9D8'); d.rectangle((0,700,W,H),fill='#C9B48F')
    # sofa
    d.rounded_rectangle((60,520,460,720),30,fill='#8E3B46'); d.rounded_rectangle((60,430,460,560),30,fill='#A3485A'); d.rounded_rectangle((30,500,110,720),25,fill='#7A2E3A'); d.rounded_rectangle((410,500,490,720),25,fill='#7A2E3A')
    path=[(260,470,0),(360,460,10),(440,470,35),(470,560,80),(470,700,150),(430,780,180)]
    x,y,a=path[k]
    cs=Image.new('RGBA',(200,200),(0,0,0,0)); c=ImageDraw.Draw(cs)
    c.ellipse((40,80,170,160),fill='#E8923A'); c.ellipse((10,40,90,120),fill='#E8923A'); c.polygon([(18,55),(28,15),(48,48)],fill='#E8923A'); c.polygon([(55,45),(78,12),(85,52)],fill='#E8923A')
    c.ellipse((30,65,44,79),fill='black'); c.ellipse((58,65,72,79),fill='black'); c.line([(165,120),(195,70)],fill='#E8923A',width=14)
    if k>=3: c.ellipse((40,88,62,104),fill='#6E2E1E')
    cs=cs.rotate(-a,expand=True); im.alpha_composite(cs,(int(x-cs.width/2),int(y-cs.height/2)))
    d=ImageDraw.Draw(im); d.text((30,40),'Reels',font=f(44),fill='#222'); d.text((30,H-150),'@cats.being.cats',font=f(28),fill='#222'); d.text((30,H-105),'he did NOT see that coming',font=f(26,False),fill='#222')
    im.save('assets/scr_cat%d.png'%k)
for k in range(6): cat(k)
# dream car video
def car(k):
    im,d=base('#0E0F14')
    for y in range(H//2,H): d.line([(0,y),(W,y)],fill=(30,30,38))
    ox=-60+k*60
    d.polygon([(40+ox,640),(120+ox,560),(300+ox,530),(430+ox,600),(500+ox,640),(500+ox,690),(40+ox,690)],fill='#F2C12E')
    d.polygon([(150+ox,568),(290+ox,540),(380+ox,590),(170+ox,600)],fill='#1E2530')
    for wx in (130,410): d.ellipse((wx-48+ox,650,wx+48+ox,746),fill='#111'); d.ellipse((wx-24+ox,674,wx+24+ox,722),fill='#888')
    d.text((W/2,200),'DREAM CAR',font=f(64),fill='white',anchor='mm'); d.text((W/2,280),'0-100 in 2.9s',font=f(34,False),fill='#F2C12E',anchor='mm')
    d.text((30,H-120),'@supercar.life',font=f(28),fill='white')
    im.save('assets/scr_car%d.png'%k)
for k in range(4): car(k)
# incoming call
im,d=base('#123A3F'); d.ellipse((W/2-110,240,W/2+110,460),fill='#2F8C99'); d.text((W/2,350),'B',font=f(120),fill='white',anchor='mm')
d.text((W/2,540),'Bilal',font=f(60),fill='white',anchor='mm'); d.text((W/2,610),'video call...',font=f(32,False),fill='#BFE3E6',anchor='mm')
d.ellipse((90,860,210,980),fill='#E8505B'); d.ellipse((330,860,450,980),fill='#3E9C5A'); im.save('assets/scr_call.png')
# alarm
im,d=base('#0B0C12'); d.text((W/2,330),'7:00',font=f(150),fill='white',anchor='mm'); d.text((W/2,440),'ALARM  ·  GYM!!!',font=f(36),fill='#F2C12E',anchor='mm')
d.rounded_rectangle((60,800,250,900),40,fill='#2A2C36'); d.text((155,850),'Snooze',font=f(34),fill='white',anchor='mm')
d.rounded_rectangle((290,800,480,900),40,fill='#E8505B'); d.text((385,850),'Stop',font=f(34),fill='white',anchor='mm'); im.save('assets/scr_alarm.png')
# monitor game (16:9)
im=Image.new('RGBA',(960,540),'#1A1030'); d=ImageDraw.Draw(im)
for y in range(270,540): d.line([(0,y),(960,y)],fill=(40,30+int((y-270)/4),60))
d.polygon([(380,540),(470,270),(490,270),(580,540)],fill='#3A3A44')
for k in range(6): d.rectangle((474,300+k*40,486,320+k*40),fill='#F2C12E')
d.polygon([(420,480),(450,430),(510,430),(540,480)],fill='#E8505B'); d.text((40,30),'SCORE 48,250',font=f(40),fill='white'); d.text((700,30),'LAP 3/3',font=f(40),fill='#F2C12E')
im.save('assets/mon_game.png')
# posters
im=Image.new('RGBA',(600,840),'#111318'); d=ImageDraw.Draw(im); d.polygon([(40,520),(140,420),(380,390),(520,470),(570,520),(570,580),(40,580)],fill='#F2C12E'); d.polygon([(170,430),(370,400),(470,470),(190,470)],fill='#1E2530')
for wx in (150,480): d.ellipse((wx-55,540,wx+55,650),fill='#000'); d.ellipse((wx-28,567,wx+28,623),fill='#888')
d.text((300,150),'DREAM',font=f(110),fill='white',anchor='mm'); d.text((300,270),'BIG',font=f(110),fill='#F2C12E',anchor='mm'); d.text((300,750),'NO DAYS OFF',font=f(52),fill='white',anchor='mm')
im.save('assets/poster_car.png')
im=Image.new('RGBA',(600,840),'#2F4E8C'); d=ImageDraw.Draw(im); d.text((300,200),'GYM',font=f(140),fill='white',anchor='mm'); d.text((300,360),'MODE',font=f(140),fill='#F2C12E',anchor='mm'); d.text((300,560),'5 AM CLUB',font=f(64),fill='white',anchor='mm'); d.text((300,700),'(starting Monday)',font=f(40,False),fill='#BFD0F0',anchor='mm')
im.save('assets/poster_gym.png')
print('ok')
