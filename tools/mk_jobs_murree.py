# build murree/jobs.json: split every shot into pieces and spread them over N jobs (optionally only some shots)
import json,re,sys
FPS=30; N=20; PIECE=60
src=open('murree/shots_by.py').read(); K=eval(re.search(r"_K=(\[.*?\])\nSEQ",src,re.S).group(1)); W=json.load(open('murree/audio/words.json'))
WS=[w['t0'] for w in W]; WE=[w['t1'] for w in W]; st=[0.0 if i==0 else round(WS[i]-.1,3) for k,i in K]; st.append(round(WE[-1]+2.0,3))
only=[int(x) for x in sys.argv[1:]]
pieces=[]
for n in range(1,len(K)+1):
    if only and n not in only: continue
    g0=int(round(st[n-1]*FPS)); g1=int(round(st[n]*FPS)); k=max(1,round((g1-g0)/PIECE)); 
    for j in range(k): pieces.append((str(n),g0+(g1-g0)*j//k,g0+(g1-g0)*(j+1)//k))
pieces.sort(key=lambda p:-(p[2]-p[1])); jobs=[[] for _ in range(N)]; load=[0]*N
for p in pieces:
    i=load.index(min(load)); jobs[i].append(list(p)); load[i]+=p[2]-p[1]+6
json.dump(dict(fps=FPS,jobs=jobs),open('murree/jobs.json','w'),indent=1); print('pieces',len(pieces),'frames',sum(p[2]-p[1] for p in pieces),'load',load)
