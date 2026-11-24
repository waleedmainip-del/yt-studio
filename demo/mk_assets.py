from PIL import Image,ImageDraw,ImageFont
import math,random,os,sys
os.chdir('/home/claude/demo')
F='/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'; FR='/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'; FM='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
def f(sz,b=True): return ImageFont.truetype(F if b else FR,sz)
def fm(sz): return ImageFont.truetype(FM,sz)
A='assets/'
# ------------------------------------------------ laptop screens 960x540 (trading platform, fictional "TradeX")
LW,LH=960,540
def candles(d,x0,y0,w,h,seq,start=0.5,cw=14,gap=8):
    """seq: list of deltas (+green, -red) in fraction of h"""
    v=start; x=x0
    for dv in seq:
        o=v; c=v+dv; hi=max(o,c)+abs(dv)*.25+.01; lo=min(o,c)-abs(dv)*.25-.01
        col='#22C55E' if dv>=0 else '#EF4444'
        Y=lambda q: y0+h-q*h
        d.line([(x+cw/2,Y(hi)),(x+cw/2,Y(lo))],fill=col,width=2)
        d.rectangle((x,Y(max(o,c)),x+cw,max(Y(min(o,c)),Y(max(o,c))+3)),fill=col)
        v=c; x+=cw+gap
    return v
def lap(name,title,badge,badge_c,bal_label,bal,bal_c,seq,extra=None,tint=None,start=.3):
    im=Image.new('RGB',(LW,LH),'#0E131B'); d=ImageDraw.Draw(im)
    d.rectangle((0,0,LW,52),fill='#151C27'); d.text((20,26),'TradeX',font=f(28),fill='#F2C12E',anchor='lm'); d.text((150,26),'XAUUSD · Gold',font=fm(22),fill='#C9D1DC',anchor='lm')
    d.rounded_rectangle((LW-230,10,LW-20,42),14,fill=badge_c); d.text((LW-125,26),badge,font=f(20),fill='#0E131B',anchor='mm')
    for k in range(6): d.line([(20,90+k*70),(640,90+k*70)],fill='#1D2633',width=1)
    candles(d,30,80,600,400,seq,start=start)
    d.rounded_rectangle((660,70,940,520),16,fill='#151C27')
    d.text((800,110),bal_label,font=fm(24),fill='#9AA6B5',anchor='mm'); d.text((800,170),bal,font=f(48 if len(bal)<10 else 40),fill=bal_c,anchor='mm')
    if extra: extra(d,im)
    if tint:
        ov=Image.new('RGB',(LW,LH),tint); im=Image.blend(im,ov,.22)
    im.save(A+name+'.png')
up=[.04,.03,-.01,.05,.04,-.02,.06,.05,.03,-.01,.06,.05,.04,.03,.05,.04,-.01,.05,.06,.05,.04,.06,.03,.04,.05,.06]
def demo_extra(d,im):
    d.text((800,240),'Profit (10 days)',font=fm(22),fill='#9AA6B5',anchor='mm'); d.text((800,280),'+ $999,000',font=f(34),fill='#22C55E',anchor='mm')
    d.rounded_rectangle((690,330,910,390),14,fill='#22C55E'); d.text((800,360),'TRADER OF THE YEAR',font=f(17),fill='#0E131B',anchor='mm')
    d.text((800,440),'(virtual money)',font=fm(20),fill='#5E6B7B',anchor='mm')
lap('lap_demo','','DEMO ACCOUNT','#F2C12E','Balance','$1,000,000','#22C55E',up,demo_extra,start=.05)
def real_extra(d,im):
    d.text((800,250),'Ready to trade',font=fm(24),fill='#9AA6B5',anchor='mm'); d.rounded_rectangle((690,300,910,370),14,fill='#2F6FE0'); d.text((800,335),'NEW TRADE',font=f(24),fill='white',anchor='mm')
lap('lap_real','','REAL ACCOUNT','#22C55E','Balance','Rs 20,000','#FFFFFF',[.02,-.03,.01,-.02,.03,-.01,.02,-.02,.01,.02,-.03,.02,-.01,.03,-.02,.01],real_extra,start=.45)
def green_extra(d,im):
    d.text((800,250),'Profit',font=fm(24),fill='#9AA6B5',anchor='mm'); d.text((800,300),'+ Rs 200',font=f(46),fill='#22C55E',anchor='mm')
    d.rounded_rectangle((300,60,560,120),16,fill='#22C55E'); d.text((430,90),'+ Rs 200',font=f(30),fill='#0E131B',anchor='mm')
lap('lap_green','','REAL ACCOUNT','#22C55E','Balance','Rs 20,200','#FFFFFF',[.01,-.02,.01,-.01,.02,-.01,.01,-.02,.01,.02,-.01,.01,.02,-.01,.01,.18],green_extra,start=.35)
def buy_extra(d,im):
    d.rectangle((660,70,940,520),fill='#151C27')
    d.text((800,100),'NEW ORDER',font=f(26),fill='white',anchor='mm')
    d.rounded_rectangle((680,130,920,180),12,fill='#22C55E'); d.text((800,155),'BUY  GOLD',font=f(26),fill='#0E131B',anchor='mm')
    d.text((690,215),'Amount',font=fm(20),fill='#9AA6B5',anchor='lm'); d.text((910,215),'ALL  Rs 20,200',font=f(20),fill='#F2C12E',anchor='rm')
    d.text((690,265),'Take profit',font=fm(20),fill='#9AA6B5',anchor='lm'); d.text((910,265),'to the moon',font=f(20),fill='white',anchor='rm')
    d.text((690,315),'Stop loss',font=fm(20),fill='#9AA6B5',anchor='lm'); d.rounded_rectangle((810,297,915,333),8,outline='#EF4444',width=3); d.text((862,315),'— —',font=f(20),fill='#EF4444',anchor='mm')
    d.text((800,365),'(empty)',font=fm(18),fill='#EF4444',anchor='mm')
    d.rounded_rectangle((680,420,920,490),14,fill='#2F6FE0'); d.text((800,455),'PLACE ORDER',font=f(26),fill='white',anchor='mm')
lap('lap_buy','','REAL ACCOUNT','#22C55E','','','#FFFFFF',[.02,-.01,.03,-.02,.02,.01,-.01,.03,.02,-.02,.01,.02,.03,-.01,.02,.01],buy_extra,start=.4)
base=[.02,-.01,.03,-.02,.02,.01,-.01,.03,.02,-.02,.01,.02,.03,-.01]
for k,(pl,bal) in enumerate((('- Rs 1,900','Rs 18,300'),('- Rs 6,400','Rs 13,800'),('- Rs 12,700','Rs 7,500'),('- Rs 17,900','Rs 2,300'))):
    seq=base+[-.05]*(k+1)+[-.07]*k
    def ex(d,im,pl=pl):
        d.text((800,250),'Open trade · Gold BUY',font=fm(21),fill='#9AA6B5',anchor='mm'); d.text((800,305),pl,font=f(44),fill='#EF4444',anchor='mm')
        d.text((800,370),'Stop loss: none',font=fm(21),fill='#EF4444',anchor='mm')
    lap('lap_red%d'%k,'','REAL ACCOUNT','#22C55E','Balance',bal,'#FFFFFF',seq,ex,tint='#5A0000' if k>=2 else None,start=.62)
im=Image.new('RGB',(LW,LH),'#0E131B'); d=ImageDraw.Draw(im); d.text((LW/2,200),'No internet connection',font=f(46),fill='white',anchor='mm'); d.text((LW/2,270),'Reconnecting...',font=fm(30),fill='#9AA6B5',anchor='mm')
d.rounded_rectangle((LW/2-260,330,LW/2+260,400),16,fill='#3A1418'); d.text((LW/2,365),'Your trade is still OPEN',font=f(28),fill='#EF4444',anchor='mm'); im.save(A+'lap_noint.png')
# ------------------------------------------------ phone screens 540x1080
W,H=540,1080
def ph(bg='#0E131B'): im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im); d.text((30,30),'11:48',font=f(26),fill='white'); return im,d
def bars(d,n,x=470,y=30):
    for k in range(4): d.rectangle((x+k*12,y+24-k*6,x+k*12+8,y+28),fill='white' if k<n else '#4A5563')
# Sir Zain profile (photo pasted later by mk_profile once the showroom still exists)
def profile(photo=None):
    im,d=ph('#FFFFFF'); d.text((30,30),'7:12',font=f(26),fill='#111'); bars(d,4)
    d.rectangle((0,80,W,90),fill='#F2F2F2')
    if photo:
        p=Image.open(photo).convert('RGB'); p=p.resize((W,int(p.height*W/p.width))); cy=(p.height-470)//2; p=p.crop((0,max(0,cy-40),W,max(0,cy-40)+470)); im.paste(p,(0,90))
    else: d.rectangle((0,90,W,560),fill='#888')
    d.ellipse((30,500,170,640),fill='white'); d.ellipse((36,506,164,634),fill='#F2C12E'); d.text((100,570),'SZ',font=f(52),fill='#111',anchor='mm')
    d.text((190,580),'Sir Zain',font=f(42),fill='#111',anchor='lm'); d.ellipse((380,562,412,594),fill='#2F80ED'); d.line([(388,579),(394,586),(405,570)],fill='white',width=4)
    d.text((190,630),'Forex Mentor · 48.2K followers',font=fm(22),fill='#666',anchor='lm')
    d.rounded_rectangle((30,670,510,830),18,fill='#F4F6F9')
    for i,t in enumerate(('100% signals','Lambo lifestyle','Mera student kabhi loss nahi karta')): d.text((50,705+i*45),('• ' if i else '')+t,font=f(26) if i==0 else fm(23),fill='#16A34A' if i==0 else '#222',anchor='lm')
    d.rounded_rectangle((30,860,510,950),45,fill='#16A34A'); d.text((270,905),'JOIN VIP  ·  Rs 5,000',font=f(30),fill='white',anchor='mm')
    im.save(A+'ph_profile.png')
if len(sys.argv)>1: profile(sys.argv[1]); print('profile ok'); sys.exit()
profile()
im,d=ph('#F4F6F9'); d.text((30,30),'7:20',font=f(26),fill='#111'); bars(d,4); d.ellipse((W/2-90,250,W/2+90,430),fill='#16A34A'); d.line([(W/2-45,342),(W/2-10,380),(W/2+50,300)],fill='white',width=18)
d.text((W/2,500),'Payment sent',font=f(44),fill='#111',anchor='mm'); d.text((W/2,570),'Rs 5,000',font=f(60),fill='#16A34A',anchor='mm'); d.text((W/2,650),'to  Sir Zain VIP',font=fm(30),fill='#444',anchor='mm'); im.save(A+'ph_paid.png')
def chat(name,msgs,fn,clock='11:48 PM'):
    im,d=ph('#0B141A'); bars(d,4); d.rectangle((0,70,W,170),fill='#1F2C34'); d.ellipse((24,90,94,160),fill='#F2C12E'); d.text((59,125),'SZ',font=f(26),fill='#111',anchor='mm')
    d.text((110,105),name,font=f(30),fill='white',anchor='lm'); d.text((110,142),'online',font=fm(20),fill='#8FA3AD',anchor='lm')
    y=220
    for who,txt in msgs:
        lines=[]; cur=''
        for wd in txt.split(' '):
            tr=(cur+' '+wd).strip()
            if d.textlength(tr,font=fm(30))>370: lines.append(cur); cur=wd
            else: cur=tr
        lines.append(cur); hh=24+len(lines)*44+28
        if who=='them': x0,x1,bg=24,24+420,'#1F2C34'
        else: x0,x1,bg=W-24-420,W-24,'#005C4B'
        d.rounded_rectangle((x0,y,x1,y+hh),18,fill=bg)
        for i,l in enumerate(lines): d.text((x0+22,y+18+i*44),l,font=fm(30),fill='white')
        d.text((x1-16,y+hh-12),clock,font=fm(16),fill='#8FA3AD',anchor='rb'); y+=hh+24
    im.save(A+fn+'.png')
chat('Sir Zain',[('them','Gold BUY. 100% sure. Jo hai sab laga do.')],'ph_signal')
chat('Sir Zain',[('them','Gold BUY. 100% sure. Jo hai sab laga do.'),('me','Sir, ab kya karun?'),('them','Market manipulation thi. Advanced course lo. 50% off.')],'ph_chat2',clock='2:13 AM')
chat('Sir Zain',[('them','Gold BUY. 100% sure. Jo hai sab laga do.'),('me','Sir, ab kya karun?')],'ph_chat1',clock='2:13 AM')
im,d=ph('#111827'); bars(d,0); d.text((W/2,380),'No signal',font=f(56),fill='white',anchor='mm'); d.text((W/2,460),'Searching...',font=fm(30),fill='#9CA3AF',anchor='mm')
for k in range(3): d.arc((W/2-60-k*40,560-k*40,W/2+60+k*40,680+k*40),220,320,fill='#4B5563',width=8)
im.save(A+'ph_nosignal.png')
im,d=ph('#111827'); bars(d,2); d.rounded_rectangle((40,330,500,640),24,fill='#1F2937'); d.text((W/2,400),'Mobile data',font=f(40),fill='white',anchor='mm'); d.text((W/2,470),'KHATAM',font=f(64),fill='#EF4444',anchor='mm'); d.text((W/2,560),'Remaining: 0 MB',font=fm(30),fill='#9CA3AF',anchor='mm'); im.save(A+'ph_nodata.png')
im,d=ph('#111827'); bars(d,3); d.ellipse((W/2-80,280,W/2+80,440),fill='#16A34A'); d.line([(W/2-40,362),(W/2-8,395),(W/2+45,322)],fill='white',width=16); d.text((W/2,510),'Rs 100 package',font=f(40),fill='white',anchor='mm'); d.text((W/2,570),'activated',font=fm(34),fill='#9CA3AF',anchor='mm'); im.save(A+'ph_pkg.png')
im,d=ph('#0E131B'); bars(d,3); d.text((W/2,120),'TradeX',font=f(34),fill='#F2C12E',anchor='mm'); d.text((W/2,330),'Balance',font=fm(36),fill='#9AA6B5',anchor='mm'); d.text((W/2,440),'Rs 0',font=f(120),fill='#EF4444',anchor='mm')
d.rounded_rectangle((40,560,500,680),20,fill='#3A1418'); d.text((W/2,600),'Margin call',font=f(34),fill='#EF4444',anchor='mm'); d.text((W/2,645),'Trade closed: - Rs 20,200',font=fm(24),fill='#F3B4B4',anchor='mm'); im.save(A+'ph_zero.png')
# map
im,d=ph('#E8E6DF'); d.text((30,30),'4:05',font=f(26),fill='#111'); bars(d,4)
for k in range(9): d.line([(0,150+k*110),(W,90+k*110)],fill='white',width=26)
for k in range(5): d.line([(60+k*120,90),(20+k*120,H)],fill='white',width=22)
d.rounded_rectangle((30,90,510,170),16,fill='white'); d.text((60,130),'Sir Zain Trading Office',font=fm(26),fill='#111',anchor='lm')
d.ellipse((W/2-40,470,W/2+40,550),fill='#EA4335'); d.polygon([(W/2-34,525),(W/2+34,525),(W/2,600)],fill='#EA4335'); d.ellipse((W/2-14,496,W/2+14,524),fill='white')
d.rounded_rectangle((40,830,500,1010),20,fill='white'); d.text((70,880),'Shop #4, Main Road',font=f(30),fill='#111',anchor='lm'); d.text((70,930),'Pizza Point',font=fm(28),fill='#EA4335',anchor='lm'); d.text((70,975),'Open now · Fast delivery',font=fm(22),fill='#666',anchor='lm')
im.save(A+'ph_map.png')
# demo on phone (end)
im,d=ph('#0E131B'); bars(d,4); d.text((W/2,120),'TradeX',font=f(34),fill='#F2C12E',anchor='mm'); d.rounded_rectangle((W/2-140,170,W/2+140,220),16,fill='#F2C12E'); d.text((W/2,195),'DEMO ACCOUNT',font=f(24),fill='#111',anchor='mm')
d.text((W/2,330),'Balance',font=fm(36),fill='#9AA6B5',anchor='mm'); d.text((W/2,430),'$1,000,000',font=f(76),fill='#22C55E',anchor='mm'); im.save(A+'ph_demo.png')
# ------------------------------------------------ signs / posters / receipts
def sign(fn,w,h,bg,lines,border=None):
    im=Image.new('RGB',(w,h),bg); d=ImageDraw.Draw(im)
    if border: d.rectangle((6,6,w-7,h-7),outline=border,width=10)
    for (txt,sz,col,y) in lines: d.text((w/2,y*h),txt,font=f(sz),fill=col,anchor='mm')
    im.save(A+fn+'.png')
sign('sign_pizza',1200,300,'#C8102E',[('PIZZA POINT',150,'#FFFFFF',.42),('FAST DELIVERY  ·  HOT & FRESH',46,'#FFD23F',.82)],border='#FFD23F')
sign('sign_mobile',1200,300,'#1D3E8A',[('MADNI MOBILE',130,'#FFFFFF',.40),('EASYLOAD  ·  PACKAGES  ·  REPAIR',46,'#7FE0FF',.82)],border='#7FE0FF')
sign('sign_showroom',1600,280,'#0B0B0E',[('PRESTIGE MOTORS',140,'#E8C25A',.46),('LUXURY CARS SHOWROOM',44,'#FFFFFF',.84)])
sign('sign_pkg',600,800,'#FFFFFF',[('DATA',110,'#1D3E8A',.18),('PACKAGES',80,'#1D3E8A',.32),('Rs 100',120,'#C8102E',.55),('1 GB  ·  1 DAY',56,'#111111',.72),('EASYLOAD HERE',48,'#16A34A',.9)],border='#1D3E8A')
sign('box_lid',600,600,'#E9D2A6',[('PIZZA POINT',80,'#C8102E',.3),('TOTAL',60,'#333333',.6),('Rs 3,000',96,'#111111',.78)])
sign('poster_trader',600,840,'#0E131B',[('TRADER',120,'#F2C12E',.22),('MINDSET',100,'#FFFFFF',.38),('$',260,'#22C55E',.66),('NO DAYS OFF',54,'#FFFFFF',.9)])
sign('poster_lambo',840,600,'#101014',[('DREAM BIG',96,'#FFFFFF',.15)])
# lambo poster drawing
im=Image.open(A+'poster_lambo.png'); d=ImageDraw.Draw(im)
d.polygon([(90,430),(200,330),(560,300),(760,380),(790,430),(790,470),(90,470)],fill='#F2C12E'); d.polygon([(250,340),(520,315),(640,380),(280,385)],fill='#1E2530')
for wx in (210,660): d.ellipse((wx-62,420,wx+62,544),fill='#000'); d.ellipse((wx-30,452,wx+30,512),fill='#888')
d.text((420,560),'LAMBO BY 25',font=f(40),fill='#F2C12E',anchor='mm'); im.save(A+'poster_lambo.png')
# Eidi envelope + bike jar labels
sign('lbl_bike',400,200,'#FFFFFF',[('BIKE FUND',62,'#C8102E',.5)])
sign('lbl_eidi',400,260,'#16A34A',[('EIDI',96,'#FFD23F',.5)])
# 100 rupee note (fictional design)
im=Image.new('RGB',(600,300),'#C25A4A'); d=ImageDraw.Draw(im); d.rectangle((14,14,586,286),outline='#7A2A20',width=8); d.text((470,150),'100',font=f(110),fill='#FFF0E0',anchor='mm'); d.ellipse((60,80,200,220),fill='#E09080'); d.text((130,150),'Rs',font=f(52),fill='#7A2A20',anchor='mm'); im.save(A+'note100.png')
im=Image.new('RGB',(600,300),'#2F7A4A'); d=ImageDraw.Draw(im); d.rectangle((14,14,586,286),outline='#174A2A',width=8); d.text((440,150),'5000',font=f(100),fill='#EFFFF0',anchor='mm'); d.ellipse((50,80,190,220),fill='#7FC09A'); im.save(A+'note5000.png')
print('ok')
