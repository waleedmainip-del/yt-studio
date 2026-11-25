from PIL import Image,ImageDraw,ImageFont
import os,math
os.chdir('/home/claude/aunty'); A='assets/'; os.makedirs(A,exist_ok=True)
F='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
def f(s): return ImageFont.truetype(F,s)
def fm(s): return ImageFont.truetype(FM,s)
def sign(fn,txt,bg,fg,w=1200,h=300,sub=None,border=None,fs=None):
    im=Image.new('RGB',(w,h),bg); d=ImageDraw.Draw(im)
    if border: d.rectangle((10,10,w-10,h-10),outline=border,width=14)
    s=fs or 130
    while d.textlength(txt,font=f(s))>w-120: s-=6
    d.text((w/2,h/2-(28 if sub else 0)),txt,font=f(s),fill=fg,anchor='mm')
    if sub: d.text((w/2,h-62),sub,font=fm(52),fill=fg,anchor='mm')
    im.save(A+fn+'.png')
# road shop boards (all must read fully)
sign('shop_a','JAHANGIR SWEETS','#C8102E','#FFE7A0',sub='Mithai · Samosa · Lassi',border='#FFE7A0')
sign('shop_b','BISMILLAH STORE','#1E5AA8','#FFFFFF',sub='General Items',border='#FFFFFF')
sign('shop_c','SAJJAD TAILORS','#2E6B4A','#F4EBDD',sub='Gents & Ladies',border='#F4EBDD')
sign('shop_d','NOOR PHARMACY','#F4F5FA','#0B7A3B',sub='24 Hours',border='#0B7A3B')
sign('shop_e','RISHTA CENTRE','#E8589A','#FFFFFF',sub='Shaadi · Mangni · Gossip',border='#FFFFFF')
sign('shop_f','CHAI KHANA','#5A3A22','#FFD58A',sub='Doodh Patti Rs 80',border='#FFD58A')
sign('lassi','LASSI','#F4F5FA','#1E5AA8',w=800,h=260,border='#1E5AA8')
sign('office','SAFE FUTURE (PVT) LTD','#13203A','#FFFFFF',w=1600,h=300,sub='Head Office',border='#C9A24A')
sign('rplate','LES 4417','#F4F5FA','#111111',w=600,h=200,border='#111111',fs=120)
sign('traffic','TRAFFIC POLICE','#F2C12E','#13203A',w=900,h=220,fs=110)
# GPS phone screens (portrait)
def phone(fn,draw):
    W,H=540,1080; im=Image.new('RGB',(W,H),'#0E1116'); d=ImageDraw.Draw(im); d.text((30,24),'9:41',font=f(28),fill='white'); draw(im,d,W,H); im.save(A+fn+'.png')
def gps1(im,d,W,H):
    d.rectangle((0,70,W,H),fill='#E8E4DA')
    for k in range(9): d.rectangle((k*70-20,70,k*70+10,H),fill='#F4F2EC')
    d.line([(W/2,H-120),(W/2,560),(W-60,560)],fill='#2F80ED',width=26); d.ellipse((W/2-26,H-146,W/2+26,H-94),fill='#2F80ED',outline='white',width=6)
    d.rounded_rectangle((20,90,W-20,300),24,fill='#1B7F4A'); d.text((60,150),'Left in 50 m',font=f(54),fill='white'); d.text((60,230),'Agle mor se left',font=fm(36),fill='#D8FFE8')
def gps2(im,d,W,H):
    gps1(im,d,W,H); d.rounded_rectangle((30,640,W-30,960),30,fill='#FFFFFF',outline='#E8589A',width=8)
    d.text((W/2,700),'Aur beta...',font=f(46),fill='#E8589A',anchor='mm'); d.text((W/2,790),'baal kab',font=f(58),fill='#13203A',anchor='mm'); d.text((W/2,870),'katwao ge?',font=f(58),fill='#13203A',anchor='mm')
phone('gps1',gps1); phone('gps2',gps2)
def fam(im,d,W,H):
    d.rectangle((0,60,W,170),fill='#075E54'); d.text((40,115),'Khandaan',font=f(40),fill='white',anchor='lm'); d.text((W-30,115),'412',font=f(34),fill='#7CFFB2',anchor='rm')
    msgs=[('Shabnam Phuppo','Mubarak ho beta!!'),('Rubina Khala','Mithai kab??'),('Nasreen Chachi','Salary kitni hai?'),('Tayi Ammi','Ab rishta pakka karo'),('Saima Aunty','Larki main dhoondti hoon'),('Phuppo 2','Mubarak!!!')]
    y=200
    for n,m in msgs:
        d.rounded_rectangle((30,y,W-60,y+120),22,fill='#FFFFFF'); d.text((54,y+30),n,font=f(28),fill='#E8589A',anchor='lm'); d.text((54,y+80),m,font=fm(32),fill='#13203A',anchor='lm'); y+=138
    d.rectangle((0,H-80,W,H),fill='#1F2C34'); d.text((W/2,H-40),'+406 more messages',font=fm(30),fill='#C9D6D2',anchor='mm')
phone('fam',fam)
def pm(im,d,W,H):
    d.rectangle((0,0,W,H),fill='#0B3D24'); d.text((W/2,230),'Incoming call',font=fm(36),fill='#BFE8D0',anchor='mm')
    d.ellipse((W/2-130,300,W/2+130,560),fill='#F4F5FA'); d.ellipse((W/2-110,320,W/2+110,540),fill='#0B7A3B'); d.text((W/2,430),'PM',font=f(96),fill='white',anchor='mm')
    d.text((W/2,640),'PRIME MINISTER',font=f(46),fill='white',anchor='mm'); d.text((W/2,700),'Islamabad',font=fm(32),fill='#BFE8D0',anchor='mm')
    for x,c in ((150,'#E8303A'),(390,'#22C55E')): d.ellipse((x-60,880,x+60,1000),fill=c)
phone('pm',pm)
# CV paper
im=Image.new('RGB',(600,840),'#FBFAF6'); d=ImageDraw.Draw(im); d.text((300,80),'CURRICULUM VITAE',font=f(44),fill='#13203A',anchor='mm'); d.text((300,150),'Waleed',font=f(56),fill='#1E5AA8',anchor='mm')
for k in range(14): d.rectangle((60,230+k*40,60+(460 if k%4 else 260),246+k*40),fill='#C9CDD6')
im.save(A+'cv.png')
# TV: breaking news (for Waleed's TV) — drawn studio, blocky anchor aunty
TW,TH=1280,720
im=Image.new('RGB',(TW,TH),'#0E2A55'); d=ImageDraw.Draw(im)
for k in range(12): d.rectangle((k*110,0,k*110+50,TH),fill='#123366')
x=640; d.rectangle((x-170,330,x+170,620),fill='#7A1E2E'); d.rectangle((x-110,120,x+110,330),fill='#C99468'); d.rectangle((x-140,90,x+140,160),fill='#6C3FA0'); d.rectangle((x-140,90,x-105,360),fill='#6C3FA0'); d.rectangle((x+105,90,x+140,360),fill='#6C3FA0')
for ex in (-45,45): d.ellipse((x+ex-16,210,x+ex+16,246),fill='#111111')
d.line([(x-36,292),(x+36,292)],fill='#7A1E2E',width=10)
d.rectangle((0,TH-200,TW,TH-110),fill='#C8102E'); d.text((30,TH-155),'BREAKING NEWS',font=f(56),fill='white',anchor='lm')
d.rectangle((0,TH-110,TW,TH),fill='#F4F5FA'); d.text((30,TH-55),'WALEED KO NAUKRI MIL GAYI · SHAADI KAB? WAZEH NAHI',font=f(40),fill='#13203A',anchor='lm')
d.rounded_rectangle((TW-230,30,TW-30,100),14,fill='#C8102E'); d.text((TW-130,65),'LIVE',font=f(44),fill='white',anchor='mm'); im.save(A+'tv_news.png')
im=Image.new('RGB',(TW,TH),'#0A0A0C'); im.save(A+'tv_off.png')
# lower third for the 3D news studio
im=Image.new('RGBA',(1600,300),(0,0,0,0)); d=ImageDraw.Draw(im); d.rectangle((0,0,1600,120),fill='#C8102E'); d.text((40,60),'BREAKING NEWS',font=f(78),fill='white',anchor='lm')
d.rectangle((0,120,1600,300),fill='#F4F5FA'); d.text((40,210),'Waleed ko naukri mil gayi!',font=f(70),fill='#13203A',anchor='lm'); im.save(A+'lower.png')
im=Image.new('RGB',(1600,500),'#0E2A55'); d=ImageDraw.Draw(im)
for k in range(16): d.rectangle((k*100,0,k*100+40,500),fill='#123366')
d.text((800,250),'NEWS 24',font=f(200),fill='#FFFFFF',anchor='mm'); im.save(A+'studio_wall.png')
# ticket
im=Image.new('RGB',(500,700),'#FFF8D8'); d=ImageDraw.Draw(im); d.rectangle((0,0,500,110),fill='#F2C12E'); d.text((250,55),'CHALLAN',font=f(60),fill='#13203A',anchor='mm')
d.text((250,220),'Jurm:',font=fm(40),fill='#13203A',anchor='mm'); d.text((250,290),'Bina topi',font=f(54),fill='#C8102E',anchor='mm'); d.text((250,400),'Jurmana:',font=fm(40),fill='#13203A',anchor='mm'); d.text((250,480),'1 glass LASSI',font=f(50),fill='#1E5AA8',anchor='mm'); d.text((250,600),'(saamne peeni hai)',font=fm(32),fill='#13203A',anchor='mm')
im.save(A+'ticket.png')
print('ok')
