import json,subprocess,os,numpy as np
from scipy.io import wavfile
A='/home/claude/picnic/audio/'
LINES={ # speaker lines in recording order
 'SHY':["SAHIL! HORN BAND KAR!","TOH PHIR KAUN BAJA RAHA HAI?!","Guys, I need a holiday. I need peace. I need silence.","Picnic? Bhai, hum park mein jaa ke kya karenge?","WAIT... ITNA SARA SPACE?!","Bro... Karachi mein itna peaceful scene bhi hota hai?","Guys, one request.","Kal bhi yahin aana hai."],
 'SAH':["MAIN NAHI BAJA RAHA!","Bro, you're living in Karachi. Be realistic.","Is there food?","Okay, now I'm interested.","Bro, finally koi jagah hai jahan horn ki jagah music sunai deta hai!","Perfect. I'm professionally qualified for that.","Guys, can we stay here permanently?","What?"],
 'EMA':["BHAI, POORA KARACHI BAJA RAHA HAI!","Lanterns? In Karachi?","Wait, there are so many things happening here!","Honestly... this is exactly what Karachi needed."],
 'ILS':["Wait! Look at this. Picnic Karachi.","Bro, it's not just a normal picnic.","There's a whole experience. Picnic mats, music, activities... even lanterns at night.","Guys, today we're doing absolutely nothing.","Apparently, yes.","BRO, PEHLE GHAR TOH CHAL!"],
 'NAR':["In this world... living in Karachi is an extreme sport.","More than five hundred picnic mats, a daytime DJ session, ten activity vendors and one thousand lanterns lighting up the sky.","A place to relax, enjoy activities, spend time with your favourite people and escape the usual chaos of Karachi.","And there's more: Picnic Karachi is giving ten free vouchers to our audience.","This isn't another chaotic day in Karachi. It's Picnic Karachi."]}
EN={('SHY',0):"SAHIL! STOP HONKING!",('SAH',0):"I'M NOT HONKING!",('SHY',1):"THEN WHO IS?!",('EMA',0):"BRO, ALL OF KARACHI IS HONKING!",('SHY',3):"Picnic? Bro, what would we even do in a park?",('SHY',4):"WAIT... THIS MUCH SPACE?!",
    ('SAH',4):"Bro, finally a place where you hear music instead of horns!",('SHY',5):"Bro... Karachi can be this peaceful?",('SHY',7):"We're coming back here tomorrow too.",('ILS',5):"BRO, LET'S GO HOME FIRST!"}
# timeline: (key, speaker, line index) or (key, None, seconds of picture-only beat); gap = pause AFTER the item
TL=[('N_world','NAR',0,.25),('C_horn','SHY',0,.12),('C_main','SAH',0,.1),('C_kaun','SHY',1,.15),('C_poora','EMA',0,.7),('C_holiday','SHY',2,.3),('C_real','SAH',1,.75),
    ('D_look','ILS',0,.25),('D_park','SHY',3,.25),('D_normal','ILS',1,.2),('D_food','SAH',2,.3),('D_exp','ILS',2,.3),('D_lant','EMA',1,.3),('D_int','SAH',3,.35),
    ('V_drive',None,2.6,0),('V_gate',None,3.6,0),('V_reveal',None,4.6,0),('A_space','SHY',4,.35),('A_music','SAH',4,.3),('V_through',None,4.4,0),
    ('V_dj',None,3.8,0),('P_nothing','ILS',3,.25),('P_qual','SAH',5,.4),('P_things','EMA',2,.3),('V_explore',None,3.8,0),
    ('V_sunset',None,3.2,0),('V_dusk',None,2.8,0),('V_lanterns',None,5.6,0),('L_peace','SHY',5,.35),('L_yes','ILS',4,.35),('L_stay','SAH',6,.35),('L_needed','EMA',3,.8),
    ('F_n1','NAR',1,.3),('F_n2','NAR',2,.45),('F_req','SHY',6,.2),('F_what','SAH',7,.2),('F_kal','SHY',7,.3),('F_ghar','ILS',5,.7),('F_vouch','NAR',3,.3),('F_last','NAR',4,.5),('END',None,4.2,0)]
SUB={'F_n1':[('F_n1',0),('F_n1b',6),('F_n1c',10),('F_n1d',13)],'F_n2':[('F_n2',0),('F_n2b',9)],'D_exp':[('D_exp',0),('D_expb',4)],'C_holiday':[('C_holiday',0)]}
def toks(s): return s.split()
def load(sp):
    d=json.load(open(A+sp.lower()+'.json')); ws=[w for w in (d['words'] if isinstance(d,dict) else d) if w.get('type','word')=='word' and not w['text'].startswith('[') and not w['text'].endswith(']')]
    out=[]; i=0
    for ln in LINES[sp]:
        n=len(toks(ln)); seg=ws[i:i+n]; assert len(seg)==n,(sp,ln); out.append(seg); i+=n
    assert i==len(ws),(sp,i,len(ws),[w['text'] for w in ws]); return out
SR=48000; PITCH=1.30; PACE=1.12
def clip(sp,seg):
    """cut one line; narrator gets the channel pitch/pace, characters a mild speed-up. returns (samples, [(w,t0,t1)])"""
    sr,x=wavfile.read(A+sp.lower()+'_n.wav'); a=max(0,seg[0]['start']-.05); b=min(len(x)/sr,seg[-1]['end']+.14); raw=x[int(a*sr):int(b*sr)]
    wavfile.write('/tmp/c.wav',sr,raw)
    if sp=='NAR': af="asetrate=48000*%.2f,aresample=48000,atempo=%.6f"%(PITCH,PACE/PITCH); k=PACE
    else: af="atempo=1.07"; k=1.07
    subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/c.wav','-af',af+',afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse','-ar','48000','/tmp/c2.wav'],check=True)
    sr2,y=wavfile.read('/tmp/c2.wav'); return y.astype(np.float32)/32768,[(w['text'],(w['start']-a)/k,(w['end']-a)/k) for w in seg]
W={sp:load(sp) for sp in LINES}; t=0.25; bus=[]; words=[]; seq=[]; lines=[]; en=[]
for key,sp,arg,gap in TL:
    if sp is None: seq.append((key,round(t,3))); lines.append(dict(key=key,sp=None,t0=round(t,3),t1=round(t+arg,3))); t+=arg; continue
    y,ww=clip(sp,W[sp][arg]); t0=t; bus.append((t0,y)); i0=len(words)
    for (w,a,b) in ww: words.append(dict(w=w,t0=round(t0+a,3),t1=round(t0+b,3),sp=sp,key=key))
    for sk,off in SUB.get(key,[(key,0)]): seq.append((sk,round(max(0,words[i0+off]['t0']-.1),3) if off or seq else round(max(0,t0-.1),3)))
    t1=t0+len(y)/SR; lines.append(dict(key=key,sp=sp,t0=round(t0,3),t1=round(t1,3),i0=i0,i1=len(words)-1,text=LINES[sp][arg]))
    if (sp,arg) in EN: en.append(dict(t0=round(t0,3),t1=round(t1,3),en=EN[(sp,arg)]))
    t=t1+gap
END=round(t,3); seq[0]=(seq[0][0],0.0); out=np.zeros(int((END+.5)*SR),dtype=np.float32)
for t0,y in bus: i=int(t0*SR); out[i:i+len(y)]+=y
wavfile.write(A+'narr.wav',SR,(np.clip(out,-1,1)*32767).astype(np.int16))
json.dump(words,open(A+'words.json','w'),indent=0); json.dump(dict(seq=seq,end=END,lines=lines),open(A+'seq.json','w'),indent=0); json.dump(en,open(A+'english_lines.json','w'),indent=0)
print('END',END,len(words),'words'); print([(k,round((seq[i+1][1] if i+1<len(seq) else END)-s,2)) for i,(k,s) in enumerate(seq)])
