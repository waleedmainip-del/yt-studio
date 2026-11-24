# Jaskirat, pitch x1.30, pace x1.12, NO pause cutting (smooth, no gaps)
import json,subprocess,numpy as np,wave
SR=48000; F=1.30; TEMPO=1.12; LEAD=0.12
W=json.load(open('words_raw.json'))['words']
z=np.frombuffer(subprocess.run(['ffmpeg','-loglevel','error','-i','raw.mp3','-af',f'aresample={SR},asetrate={SR}*{F},aresample={SR},atempo={TEMPO/F:.5f}','-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout,np.float32).copy()
z=np.concatenate([np.zeros(int(LEAD*SR),np.float32),z,np.zeros(int(.6*SR),np.float32)]); z=z/max(abs(z).max(),1e-6)*.9
with wave.open('narr.wav','wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((z*32767).astype(np.int16).tobytes())
WW=[]
for x in W:
    t=x['text']
    if t.startswith('[') or t.endswith(']'): continue
    WW.append(dict(w=t,t0=round(LEAD+x['start']/TEMPO,3),t1=round(LEAD+x['end']/TEMPO,3)))
json.dump(WW,open('words.json','w')); print(len(WW),len(z)/SR)
print(' | '.join('%d %s %.1f'%(i,w['w'],w['t0']) for i,w in enumerate(WW)))
