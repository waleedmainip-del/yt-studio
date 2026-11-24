from PIL import Image,ImageDraw,ImageFont
import os,sys
os.chdir('/home/claude/murree'); A='assets/'
F='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
def f(s): return ImageFont.truetype(F,s)
def fm(s): return ImageFont.truetype(FM,s)
def sign(fn,w,h,bg,lines,border=None):
    im=Image.new('RGB',(w,h),bg); d=ImageDraw.Draw(im)
    if border: d.rectangle((6,6,w-7,h-7),outline=border,width=10)
    for (txt,sz,col,y) in lines: d.text((w/2,y*h),txt,font=f(sz),fill=col,anchor='mm')
    im.save(A+fn+'.png')
sign('plate',600,150,'#F4F5FA',[('LEB 2471',96,'#111111',.55)],border='#111111')
sign('sign_toll',1800,260,'#1D4E9E',[('MURREE EXPRESSWAY  ·  TOLL PLAZA',96,'#FFFFFF',.42),('Rs 150  ·  ALL LANES',52,'#FFD23F',.82)])
sign('bill_murree',1200,600,'#E8F2FA',[('MURREE',150,'#1D4E9E',.3),('Barf · Chai · Sukoon',70,'#333333',.58),('Sirf 2 ghante!',78,'#C8102E',.82)],border='#1D4E9E')
sign('sign_chai',1200,320,'#C8102E',[('CHACHA DHABA',120,'#FFFFFF',.42),('Doodh Patti  ·  Pakoray  ·  Parathay',48,'#FFD23F',.82)],border='#FFD23F')
for p in (50,100,300): sign('price_%d'%p,600,440,'#FFFFFF',[('BHUTTA',96,'#2E6B4A',.27),('Rs %d'%p,150 if p<300 else 160,'#C8102E',.66)],border='#2E6B4A')
sign('sign_mall',1200,350,'#2E6B4A',[('MALL ROAD',130,'#FFFFFF',.45),('2 km  →',70,'#FFD23F',.8)],border='#FFFFFF')
for i,(n,c,s2) in enumerate((('SHALIMAR SHAWLS','#7A2E3A','Woollen · Shawls'),('CAFE KASHMIR','#2E4E7A','Kashmiri Chai'),('MURREE CRAFTS','#5A3A7A','Gifts · Souvenirs'),('HOT CORN CORNER','#2E6B4A','Bhutta · Soup'),('CHAPLI HOUSE','#8C5A2A','Since 1985'),('SNOW PHOTO STUDIO','#3A5A6A','Rs 500 per photo'))):
    sign('shop%d'%i,1300,180,c,[(n,84,'#FFFFFF',.42),(s2,38,'#FFE7B0',.82)])
im=Image.new('RGB',(1000,700),'#14301F'); d=ImageDraw.Draw(im); d.rectangle((10,10,989,689),outline='#C9A24A',width=12)
d.text((500,80),'ROOM RATES',font=f(80),fill='#F2C12E',anchor='mm')
for k,(a,b) in enumerate((('Room','Rs 25,000'),('Snow View','+ Rs 5,000'),('Heater','+ Rs 3,000'),('Hot Water','Kal subah se'))):
    d.text((90,210+k*115),a,font=f(58),fill='#FFFFFF',anchor='lm'); d.text((910,210+k*115),b,font=f(58),fill='#F2C12E' if k<3 else '#FF8A80',anchor='rm')
im.save(A+'rate_board.png')
sign('sign_hotel',1000,300,'#14301F',[('SNOW VIEW HOTEL',96,'#F2C12E',.45),('★★★★★ (by owner)',44,'#FFFFFF',.8)])
# phone: Ammi calling
W,H=540,1080
im=Image.new('RGB',(W,H),'#1B2A3A'); d=ImageDraw.Draw(im); d.text((30,30),'8:42',font=f(26),fill='white')
d.ellipse((W/2-110,250,W/2+110,470),fill='#E8A3B8'); d.text((W/2,360),'A',font=f(130),fill='white',anchor='mm')
d.text((W/2,550),'Ammi',font=f(64),fill='white',anchor='mm'); d.text((W/2,630),'calling...',font=fm(34),fill='#9FB3C8',anchor='mm')
for x,c in ((W/2-130,'#E8303A'),(W/2+130,'#22C55E')): d.ellipse((x-60,850,x+60,970),fill=c)
d.line([(W/2+105,905),(W/2+150,915)],fill='white',width=14); d.line([(W/2-155,915),(W/2-105,905)],fill='white',width=14)
im.save(A+'ph_ammi.png')
def photo(src):
    im=Image.new('RGB',(W,H),'#000000'); d=ImageDraw.Draw(im); p=Image.open(src).convert('RGB'); p=p.resize((W,int(p.height*W/p.width)))
    im.paste(p,(0,(H-p.height)//2)); d.rectangle((0,0,W,90),fill='#075E54'); d.text((30,45),'Ammi',font=f(34),fill='white',anchor='lm'); d.text((W-30,45),'photo',font=fm(26),fill='#CFE8E2',anchor='rm')
    im.save(A+'ph_roof.png')
if len(sys.argv)>1: photo(sys.argv[1])
print('ok')
