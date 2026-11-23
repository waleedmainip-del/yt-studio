import sys,os
from PIL import Image, ImageDraw, ImageFont
D=sys.argv[1]; F=lambda s,w='Bold': ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-%s.otf'%w,s)
CH=[('S01','SHAHERIYAR','Boy · 178 cm · quiff, trimmed beard and moustache · white shirt, dark trousers, brown shoes, watch'),
    ('S02','SAHIL','Boy · 174 cm · wavy fringe, moustache · beige tee, black trousers, white sneakers, wrist band'),
    ('S03','EMAN','Girl · 160 cm · hair tied back · brown shirt-dress, cream shoes'),
    ('S04','ILSA','Girl · 163 cm · long open hair, glasses · green kurta, cream trousers, green scarf')]
LAB=['FRONT','SIDE','BACK','3/4','FACE','WALKING','SITTING','EXPRESSION']; out=[]
for sid,nm,desc in CH:
    ims=[]
    for v in range(8):
        p='%s/%s_%02d.00.png'%(D,sid,v); ims.append(Image.open(p).convert('RGB') if os.path.exists(p) else None)
    if not any(ims): continue
    idx=[v for v in range(8) if ims[v]]; rows=(len(idx)+3)//4
    w,h=[i for i in ims if i][0].size; cw=380; ch=int(h*cw/w); sheet=Image.new('RGB',(cw*4,ch*rows+150),(245,243,238)); d=ImageDraw.Draw(sheet)
    d.text((28,22),nm,font=F(58,'ExtraBold'),fill=(30,34,44)); d.text((30,96),desc,font=F(25,'Medium'),fill=(90,96,110))
    for n_,v in enumerate(idx):
        im=ims[v]; x=(n_%4)*cw; y=150+(n_//4)*ch
        if im: sheet.paste(im.resize((cw,ch),Image.LANCZOS),(x,y))
        d.rectangle((x+10,y+10,x+18+d.textlength(LAB[v],font=F(22)),y+44),fill=(30,34,44)); d.text((x+14,y+14),LAB[v],font=F(22),fill=(255,255,255))
    fn='/home/claude/picnic/Picnic_Characters_%s.png'%nm.title(); sheet.save(fn); out.append(fn); print(fn,sheet.size)
