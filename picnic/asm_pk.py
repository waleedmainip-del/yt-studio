import json, subprocess, os, numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
from PIL import Image, ImageDraw, ImageFont
R='/home/claude/picnic'
exec(open(R+'/sfx/seq.py').read())
W=WJ; TOT=END; T=dict(SEQ)
def ts(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
ass=["[Script Info]","PlayResX: 1080","PlayResY: 1920","","[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: C,Inter,100,&H0000D7FF,&H0000D7FF,&H00101010,&H80000000,1,0,0,0,100,100,0,0,1,8,3,2,70,70,470,1",
"Style: E,Inter,46,&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,1,0,0,0,100,100,0,0,1,4,2,2,90,90,330,1",
"Style: T,Inter,64,&H00FFFFFF,&H00FFFFFF,&H00E3C169,&H00E3C169,1,0,0,0,100,100,2,0,3,16,0,8,60,60,210,1",
"Style: V,Inter,84,&H00FFFFFF,&H00FFFFFF,&H00E3C169,&H00E3C169,1,0,0,0,100,100,1,0,3,22,0,8,60,60,330,1","","[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ENDT=T['END']
for i,w in enumerate(W):
    a_,b_=w['t0'],w['t1']; nxt=W[i+1]['t0'] if i+1<len(W) else b_+.3
    end=min(nxt,max(b_+.08,a_+.12)) if nxt-b_<.45 else b_+.15
    txt=w['w'].upper().replace('...','').strip('.,!?:').replace('"','')
    if i+1<len(W): end=min(end,W[i+1]['t0']-.03)
    end=max(end,a_+.05)
    ass.append(f"Dialogue: 0,{ts(max(0,a_-.02))},{ts(min(ENDT,end))},C,,0,0,0,,{txt}")
EL=json.load(open(R+'/audio/english_lines.json'))
for k_,L_ in enumerate(EL): ass.append(f"Dialogue: 0,{ts(max(0,L_['t0']-.05))},{ts(L_['t1']+.2)},E,,0,0,0,,{L_['en']}")
# on-screen event facts (exact confirmed figures only)
for k,txt in (('F_n1','500+ PICNIC MATS'),('F_n1b','DAYTIME DJ SESSION'),('F_n1c','10 ACTIVITY VENDORS'),('F_n1d','1,000 LANTERNS')):
    i=[kk for kk,_ in SEQ].index(k); ass.append(f"Dialogue: 1,{ts(SEQ[i][1]+.08)},{ts(SEQ[i+1][1]-.04)},T,,0,0,0,,{txt}")
ass.append(f"Dialogue: 1,{ts(T['F_vouch']+1.3)},{ts(T['F_last']-.1)},V,,0,0,0,,{{\\fad(200,150)}}10 FREE VOUCHERS\\NFOR OUR AUDIENCE")
ass.append(f"Dialogue: 1,{ts(T['V_gate']+.5)},{ts(T['V_gate']+3.3)},T,,0,0,0,,{{\\fad(200,200)}}KARACHI UNITED STADIUM, CLIFTON")
open(R+'/subs.ass','w').write('\n'.join(ass))
# ---- end card
def endcard(path,dur):
    BG=(105,192,227); im=Image.new('RGB',(1080,1920),BG); lg=Image.open(R+'/logo_crop.jpg').convert('RGB'); lw=900; lh=int(lg.size[1]*lw/lg.size[0]); lg=lg.resize((lw,lh),Image.LANCZOS); BG=lg.getpixel((4,4)); im=Image.new('RGB',(1080,1920),BG)
    im.paste(lg,(90,190)); d=ImageDraw.Draw(im)
    F=lambda s,wt='Bold': ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-%s.otf'%wt,s)
    def ctr(y,txt,f,fill=(255,255,255),sp=0):
        w=sum(d.textlength(c,font=f) for c in txt)+sp*(len(txt)-1); x=(1080-w)/2
        for c in txt: d.text((x,y),c,font=f,fill=fill); x+=d.textlength(c,font=f)+sp
    ctr(820,'MAKE ROOM FOR',F(56,'SemiBold'),sp=10); ctr(900,'BETTER MEMORIES.',F(56,'SemiBold'),sp=10)
    d.rounded_rectangle((150,1060,930,1350),28,fill=(255,255,255)); ctr(1098,'SUNDAY 29 NOVEMBER',F(58,'ExtraBold'),fill=(40,110,150),sp=2); ctr(1186,'3 PM – 11 PM',F(54,'Bold'),fill=(40,110,150),sp=2); ctr(1274,'KARACHI UNITED STADIUM, CLIFTON',F(32,'SemiBold'),fill=(60,130,170),sp=2)
    d.rounded_rectangle((110,1410,970,1680),28,fill=(255,215,0)); ctr(1436,'10 FREE VOUCHERS',F(66,'ExtraBold'),fill=(20,40,60),sp=2); ctr(1526,'ONLY FOR MY AUDIENCE',F(46,'Bold'),fill=(20,40,60),sp=2); ctr(1596,'GO GET THEM!',F(52,'ExtraBold'),fill=(20,40,60),sp=4)
    im.save(R+'/endcard.png')
    subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i',R+'/endcard.png','-t',f'{dur:.3f}','-r','30','-vf','fade=t=in:st=0:d=0.45','-c:v','libx264','-crf','14','-preset','veryfast','-pix_fmt','yuv420p',path],check=True)
SD=os.environ.get('SEGS','segs'); n=len(SEQ); endseg=f'{R}/{SD}/seg_{n:02d}.mp4'; g0=int(round(T['END']*30)); g1=int(round(END*30)); endcard(endseg,(g1-g0)/30)
sr,nv=wavfile.read(R+'/audio/narr.wav'); nv=nv.astype(np.float32)/32768
sr2,s=wavfile.read(R+'/sfx/sfx.wav'); s=s.astype(np.float32)/32768
if sr!=sr2: s=resample_poly(s,sr//300,sr2//300)
L=int(TOT*sr); nn=np.zeros(L); nn[:min(L,len(nv))]=nv[:L]; ss=np.zeros(L); ss[:min(L,len(s))]=s[:L]
win=int(.05*sr); env=np.sqrt(np.convolve(nn**2,np.ones(win)/win,'same')); env=np.convolve(env,np.ones(int(.25*sr))/int(.25*sr),'same')
duck=1-.55*np.clip(env/(env.max()*.3),0,1)
mix=nn+ss*duck*1.5; t=np.arange(L)/sr; mix*=np.clip((TOT-t)/0.8,0,1)
pk=np.abs(mix).max(); mix=mix/max(1,pk/.89); wavfile.write(R+'/mix.wav',sr,(mix*32767).astype(np.int16))
segs=[f'{R}/{SD}/seg_{k:02d}.mp4' for k in range(1,n+1)]; have=[p for p in segs if os.path.exists(p)]; print('segments',len(have),'/',len(segs))
if len(have)==len(segs) and os.environ.get('ENCODE'):
    open(f'{R}/{SD}/list.txt','w').write(''.join(f"file '{p}'\n" for p in segs))
    raw=R+'/raw.mkv'; out=os.environ.get('OUT',R+'/Picnic_Karachi_v1.mp4')
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{R}/{SD}/list.txt','-i',R+'/mix.wav','-vf',f"fade=t=in:st=0:d=0.4,ass={R}/subs.ass:fontsdir=/usr/share/fonts/opentype/inter",'-r','30','-c:v','libx264','-crf','25','-preset','medium','-pix_fmt','yuv420p','-c:a','pcm_s16le','-shortest',raw],check=True)
    m=subprocess.run(['ffmpeg','-hide_banner','-i',raw,'-af','loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    j=json.loads(m[m.rindex('{'):m.rindex('}')+1])
    subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-c:v','copy','-af',f"loudnorm=I=-15:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",'-ar','48000','-c:a','aac','-b:a','192k','-movflags','+faststart',out],check=True)
    os.remove(raw); print('encoded',out,os.path.getsize(out)/1e6,'MB')
