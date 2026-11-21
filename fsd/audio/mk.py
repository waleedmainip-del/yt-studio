import json,subprocess,numpy as np,wave
SR=48000; F=1.30; TEMPO=1.16; KEEP=0.26
W=json.load(open("words_raw.json"))["words"]
x=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i','raw.mp3','-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout,np.float32).copy()
fr=480; n=len(x)//fr; e=np.sqrt((x[:n*fr].reshape(n,fr)**2).mean(1)); v=e>0.01
cuts=[];i=0
while i<n:
    if not v[i]:
        j=i
        while j<n and not v[j]: j+=1
        d=(j-i)*.01
        if d>KEEP+.04 and i>0 and j<n:
            mid=(i+j)/2*.01; cuts.append((mid-(d-KEEP)/2,mid+(d-KEEP)/2))
        i=j
    else: i+=1
segs=[];p=0.0
for a,b in cuts: segs.append((p,a)); p=b
segs.append((p,len(x)/SR))
out=[];f=int(.008*SR)
for a,b in segs:
    s=x[int(a*SR):int(b*SR)].copy(); s[:f]*=np.linspace(0,1,f); s[-f:]*=np.linspace(1,0,f); out.append(s)
y=np.concatenate(out)
def mapt(t):
    acc=0
    for a,b in segs:
        if t<=b: return acc+max(0,t-a)
        acc+=b-a
    return acc
z=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-af',f'asetrate={SR}*{F},aresample={SR},atempo={TEMPO/F:.5f}','-f','f32le','-ac','1','-ar',str(SR),'-'],input=y.tobytes(),capture_output=True).stdout,np.float32).copy()
LEAD=0.12
z=np.concatenate([np.zeros(int(LEAD*SR),np.float32),z,np.zeros(int(.6*SR),np.float32)])
z=z/max(abs(z).max(),1e-6)*.9
with wave.open('narr.wav','wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((z*32767).astype(np.int16).tobytes())
WW=[]
for w_ in W:
    t=w_['text']
    if t.startswith('[') or t.endswith(']'): continue
    WW.append(dict(w=t.replace('Wee','OUII'),t0=round(LEAD+mapt(w_['start'])/TEMPO,3),t1=round(LEAD+mapt(w_['end'])/TEMPO,3)))
json.dump(WW,open('words.json','w'))
print(len(WW),'dur',len(z)/SR)
print(' | '.join('%d %s %.2f'%(i,w_['w'],w_['t0']) for i,w_ in enumerate(WW)))
