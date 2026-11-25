from PIL import Image,ImageDraw,ImageFont
import os,math
os.chdir('/home/claude/abbu'); A='assets/'; os.makedirs(A,exist_ok=True)
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
sign('s_style','STYLE HUB','#13203A','#F2C12E',sub='Men · Kids · Shoes',border='#F2C12E')
sign('s_food','BURGER STATION','#C8102E','#FFFFFF',sub='Food Court',border='#FFFFFF')
sign('s_barber','FAUJI SALON','#F4F5FA','#13203A',sub='Hair Cutting Since 1985',border='#C8102E')
sign('s_cinema','CINE STAR','#16171C','#F2C12E',sub='Screen 1',border='#F2C12E')
sign('s_mall','CITY MALL','#0B5A6E','#FFFFFF',w=1600,sub='Mega Sale 50%',border='#FFFFFF')
sign('s_shoes','SHOE PALACE','#6C3FA0','#FFFFFF',border='#FFFFFF')
sign('s_phone','MOBILE ZONE','#2E6B4A','#FFFFFF',border='#FFFFFF')
sign('s_sweet','KHAN SWEETS','#E8A33A','#5A2A0A',border='#5A2A0A')
sign('s_karyana','HAFEEZ KARYANA','#1E5AA8','#FFFFFF',border='#FFFFFF')
sign('s_hotel','DHABA 24/7','#7A1E2E','#FFE7A0',border='#FFE7A0')
sign('ac_off','AC BAND HAI','#F4F5FA','#C8102E',w=1000,h=360,sub='Bijli muft nahi aundi',border='#C8102E')
sign('tag','Rs 3,000','#F4F5FA','#C8102E',w=500,h=240,border='#C8102E',fs=110)
sign('taxi','TAXI','#F2C12E','#16171C',w=600,h=220,fs=140)
im=Image.new('RGB',(900,1200),'#F4EBDD'); d=ImageDraw.Draw(im); d.rectangle((0,0,900,1200),outline='#C8102E',width=24)
d.text((450,140),'SPECIAL',font=f(90),fill='#C8102E',anchor='mm'); d.text((450,280),'FAUJI CUT',font=f(130),fill='#13203A',anchor='mm')
x=450; d.rectangle((x-170,420,x+170,760),fill='#C49066'); d.rectangle((x-175,400,x+175,450),fill='#1A1410')
for ex in (-70,70): d.ellipse((x+ex-22,540,x+ex+22,590),fill='#111111')
d.rectangle((x-90,650,x+90,680),fill='#1A1410'); d.rectangle((x-220,780,x+220,1000),fill='#4A5536')
d.text((450,1090),'Style of 1985',font=f(70),fill='#13203A',anchor='mm'); im.save(A+'poster.png')
def atm(fn,lines,col='#0B5A6E'):
    im=Image.new('RGB',(800,600),col); d=ImageDraw.Draw(im); d.rectangle((0,0,800,90),fill='#062F3A'); d.text((400,45),'CITY BANK ATM',font=f(46),fill='white',anchor='mm')
    y=170
    for t,s,c in lines:
        while d.textlength(t,font=f(s))>700: s-=4
        d.text((400,y),t,font=f(s),fill=c,anchor='mm'); y+=int(s*1.45)
    for k,lab in enumerate(('Kiraya','Fees','Doodh','Shauq')): d.rounded_rectangle((40+k*185,500,200+k*185,570),12,fill='#F4F5FA'); d.text((120+k*185,535),lab,font=f(32),fill='#13203A',anchor='mm')
    im.save(A+fn+'.png')
atm('atm1',[('Enter amount',60,'#FFFFFF'),('Rs 5,000',96,'#F2C12E')])
atm('atm2',[('Paise kis kam layi?',62,'#FFFFFF'),('Pichle mahine wale',52,'#F2C12E'),('kithe gaye?',52,'#F2C12E')],'#7A1E2E')
# cinema screen: action hero paused + advice overlay
TW,TH=1600,700
im=Image.new('RGB',(TW,TH),'#2A3A5A'); d=ImageDraw.Draw(im)
d.rectangle((0,420,TW,TH),fill='#4A3A2A');
for k in range(8): d.rectangle((80+k*200,140,180+k*200,420),fill=['#3A4A6A','#2E3E5E'][k%2])
x=800; d.rectangle((x-120,260,x+120,560),fill='#16171C'); d.rectangle((x-80,110,x+80,260),fill='#C49066'); d.rectangle((x-90,90,x+90,140),fill='#1A1410')
for ex in (-35,35): d.rectangle((x+ex-25,170,x+ex+25,195),fill='#111111')
d.rectangle((x-200,300,x-120,330),fill='#16171C'); d.rectangle((x+120,300,x+260,330),fill='#16171C')
d.rounded_rectangle((TW/2-120,TH/2-90,TW/2-40,TH/2+90),12,fill=(255,255,255)); d.rounded_rectangle((TW/2+40,TH/2-90,TW/2+120,TH/2+90),12,fill=(255,255,255))
d.rectangle((0,TH-110,TW,TH),fill='#C8102E'); d.text((TW/2,TH-55),'NASEEHAT BREAK — Padhai poori karo!',font=f(56),fill='white',anchor='mm')
im.save(A+'screen.png')
def phone(fn,draw):
    W,H=540,1080; im=Image.new('RGB',(W,H),'#0E1116'); d=ImageDraw.Draw(im); d.text((30,24),'7:12',font=f(28),fill='white'); draw(im,d,W,H); im.save(A+fn+'.png')
def pizza(im,d,W,H):
    d.rectangle((0,60,W,180),fill='#C8102E'); d.text((W/2,120),'PIZZA POINT',font=f(48),fill='white',anchor='mm')
    d.ellipse((W/2-170,230,W/2+170,570),fill='#E8A33A'); d.ellipse((W/2-145,255,W/2+145,545),fill='#F2C14E')
    for a in range(8): d.ellipse((W/2+90*math.cos(a)-24,400+90*math.sin(a)-24,W/2+90*math.cos(a)+24,400+90*math.sin(a)+24),fill='#C8102E')
    d.text((W/2,640),'Large Tikka x2',font=f(40),fill='white',anchor='mm'); d.text((W/2,710),'+ Extra Cheese',font=fm(34),fill='#C9D6D2',anchor='mm'); d.text((W/2,800),'Rs 4,200',font=f(60),fill='#F2C12E',anchor='mm')
    d.rounded_rectangle((60,900,W-60,1000),30,fill='#22C55E'); d.text((W/2,950),'ORDER NOW',font=f(44),fill='white',anchor='mm')
phone('ph_pizza',pizza)
def chat(im,d,W,H):
    d.rectangle((0,60,W,170),fill='#075E54'); d.text((40,115),'Dosto ka group',font=f(36),fill='white',anchor='lm')
    y=220
    for t in ('Mall aaja yaar','AC on hai na?','haha','Burger party!'): d.rounded_rectangle((30,y,W-80,y+100),22,fill='#FFFFFF'); d.text((54,y+50),t,font=fm(34),fill='#13203A',anchor='lm'); y+=125
phone('ph_chat',chat)
print('ok')
