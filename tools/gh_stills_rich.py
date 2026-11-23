# GitHub runner: QC stills + collision report for a list of (shot, "t1,t2,..")
import json, os, subprocess, sys
J=int(sys.argv[1]); items=json.load(open('rich/stills.json'))['jobs'][J]
RF='/home/claude/rich'; out=os.path.join(os.environ['GITHUB_WORKSPACE'],'gh_out'); os.makedirs(out,exist_ok=True); os.makedirs(RF+'/stills',exist_ok=True)
pct=os.environ.get('QPCT','34')
for shot,ts in items:
    for mode in ('still','collide'):
        lp=out+'/log_%s_%s.txt'%(shot,mode)
        with open(lp,'w') as log:
            subprocess.run(['xvfb-run','-a','blender','-b','-P',RF+'/film_lr.py','--',str(shot),pct,'2',mode,ts],stdout=log,stderr=subprocess.STDOUT,env=dict(os.environ,FPS='30'))
        L=open(lp,errors='ignore').read().splitlines(); open(lp,'w').write('\n'.join([l for l in L if 'Error' in l or 'error' in l or 'Traceback' in l or 'line ' in l or 'COLLIDE' in l or 'STILL' in l][-40:])+'\n')
for f in os.listdir(RF+'/stills'):
    os.replace(RF+'/stills/'+f, out+'/'+f)
