import json,sys
exec(open('/home/claude/picnic/sfx/seq.py').read())
FPS=30; only=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 and sys.argv[2] else None
P=[]
for i,(k,t) in enumerate(SEQ):
    if k=='END' or (only and (i+1) not in only): continue
    t1=SEQ[i+1][1] if i+1<len(SEQ) else END; g0=int(round(t*FPS)); g1=int(round(t1*FPS)); n=max(1,round((g1-g0)/45)); 
    for j in range(n): P.append([str(i+1),g0+(g1-g0)*j//n,g0+(g1-g0)*(j+1)//n])
jobs=[[] for _ in range(18)]
for i,p in enumerate(P): jobs[i%18].append(p)
json.dump({'fps':30,'v':int(sys.argv[1]),'jobs':jobs},open('/home/claude/yt-studio/picnic/jobs.json','w')); print(len(P),'pieces',sum(p[2]-p[1] for p in P),'frames')
