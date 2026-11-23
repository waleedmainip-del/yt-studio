import json, subprocess, os, numpy as np
from scipy.io import wavfile
from scipy.signal import resample_poly
R='/home/claude/rich'
exec(open(R+'/sfx/seq.py').read())
W=json.load(open(R+'/audio/words.json')); CARD=0.0; TOT=END+CARD
def ts(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
ass=["[Script Info]","PlayResX: 1080","PlayResY: 1920","","[V4+ Styles]",
"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: C,Inter,104,&H0000D7FF,&H0000D7FF,&H00101010,&H80000000,1,0,0,0,100,100,0,0,1,8,3,2,70,70,470,1",
"Style: E,Inter,46,&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,1,0,0,0,100,100,0,0,1,4,2,2,90,90,330,1","","[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for i,w in enumerate(W):
    a_,b_=w['t0'],w['t1']; nxt=W[i+1]['t0'] if i+1<len(W) else b_+.3
    end=min(nxt,max(b_+.08,a_+.12)) if nxt-b_<.45 else b_+.15
    txt=w['w'].upper().strip('.,!?').replace('"','')
    if txt.endswith('...'): txt=txt[:-3]
    txt=txt.rstrip('.')
    if i+1<len(W): end=min(end,W[i+1]['t0']-.05)
    end=max(end,a_+.05)
    ass.append(f"Dialogue: 0,{ts(max(0,a_-.02))},{ts(min(END,end))},C,,0,0,0,,{txt}")
EL=json.load(open(R+'/audio/english_lines.json'))
for k_,L_ in enumerate(EL):
    e_=min(L_['t1']+.25, EL[k_+1]['t0']-.06) if k_+1<len(EL) else L_['t1']+.6
    ass.append(f"Dialogue: 0,{ts(max(0,L_['t0']-.05))},{ts(e_)},E,,0,0,0,,{L_['en'].replace(chr(34),'')}")
# ---- price scoreboard (top of frame)
ass.insert(ass.index("[Events]")-1,"Style: P,Inter,62,&H00FFFFFF,&H00FFFFFF,&H00101010,&HB0000000,1,0,0,0,100,100,0,0,3,10,0,2,60,60,650,1")
WSs=[w_['t0'] for w_ in W]
PR=[(51,"4,000",None),(60,"4,000","800"),(81,"3,500","800"),(83,"3,500","900"),(85,"3,000","900"),(87,"3,000","950"),(103,"1,500","950"),(112,"1,500","1,000"),(126,"1,000","1,000")]
PEND=WSs[134]-.1
for k_,(wi,sp,wp_) in enumerate(PR):
    a_=WSs[wi]+.05; b_=PR[k_+1][0] if k_+1<len(PR) else None; b_=(WSs[b_]+.05) if b_ is not None else PEND
    txt="{\\c&H5A5AFF&}SHOP   Rs "+sp+"\\N{\\c&H7CF07C&}WALEED   Rs "+(wp_ or "?")
    if k_==len(PR)-1: txt="{\\c&H00D7FF&}DEAL   Rs 1,000"
    ass.append(f"Dialogue: 1,{ts(a_)},{ts(b_)},P,,0,0,0,,{txt}")
ass.append(f"Dialogue: 1,{ts(WSs[139])},{ts(WSs[145]-.15)},P,,0,0,0,,{{\\c&H00D7FF&}}Rs 1,000  x 2")
open(R+'/subs.ass','w').write('\n'.join(ass))
sr,n=wavfile.read(R+'/audio/narr.wav'); n=n.astype(np.float32)/32768
if n.ndim>1: n=n.mean(1)
sr2,s=wavfile.read(R+'/sfx/sfx.wav'); s=s.astype(np.float32)/32768
if sr!=sr2: s=resample_poly(s,sr//300,sr2//300) if sr%300==0 and sr2%300==0 else resample_poly(s,sr,sr2)
L=int(TOT*sr); nn=np.zeros(L); nn[:min(L,len(n))]=n[:L]; ss=np.zeros(L); ss[:min(L,len(s))]=s[:L]
win=int(.05*sr); env=np.sqrt(np.convolve(nn**2,np.ones(win)/win,'same')); env=np.convolve(env,np.ones(int(.25*sr))/int(.25*sr),'same')
duck=1-.45*np.clip(env/(env.max()*.35),0,1)
mix=nn+ss*duck*1.6; t=np.arange(L)/sr; mix*=np.clip((TOT-t)/0.6,0,1)
pk=np.abs(mix).max(); mix=mix/max(1,pk/.89)
wavfile.write(R+'/mix.wav',sr,(mix*32767).astype(np.int16))
segs=[f'{R}/segs/seg_{k:02d}.mp4' for k in range(1,len(SEQ)+1)]; have=[p for p in segs if os.path.exists(p)]; print('segments',len(have),'/',len(segs))
if len(have)==len(segs) and os.environ.get('ENCODE'):
    open(R+'/segs/list.txt','w').write(''.join(f"file '{p}'\n" for p in segs))
    raw=R+'/raw.mkv'; out=os.environ.get('OUT',R+'/Karachi_Bargainer_v1.mp4')
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',R+'/segs/list.txt','-i',R+'/mix.wav','-vf',f"fade=t=in:st=0:d=0.5,ass={R}/subs.ass:fontsdir=/usr/share/fonts/opentype/inter",'-r','30','-c:v','libx264','-crf','19','-preset','medium','-pix_fmt','yuv420p','-c:a','pcm_s16le','-shortest',raw],check=True)
    m=subprocess.run(['ffmpeg','-hide_banner','-i',raw,'-af','loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    j=json.loads(m[m.rindex('{'):m.rindex('}')+1])
    subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-c:v','copy','-af',f"loudnorm=I=-15:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",'-ar','48000','-c:a','aac','-b:a','192k','-movflags','+faststart',out],check=True)
    os.remove(raw); print('encoded',out,os.path.getsize(out)/1e6,'MB')
