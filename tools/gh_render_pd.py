# GitHub runner: render this job's (shot, F0, F1) pieces of the Lahore episode 1 and encode each piece at 30 fps.
import json, os, subprocess, sys, time
J = int(sys.argv[1]); pieces = json.load(open('pd/jobs.json'))['jobs'][J]
LH = os.path.join(os.environ['GITHUB_WORKSPACE'], 'pd'); out = os.path.join(os.environ['GITHUB_WORKSPACE'], 'gh_out'); os.makedirs(out, exist_ok=True)
SAMPLES = os.environ.get('SAMPLES', '8'); status = []
for shot, f0, f1 in pieces:
    nn = '%02d' % int(shot); t0 = time.time(); lp = out + '/log_%s_%05d.txt' % (nn, f0)
    with open(lp, 'w') as log:
        r = subprocess.run(['xvfb-run', '-a', 'blender', '-b', '-P', LH + '/film_pd.py', '--', shot, '100', SAMPLES, 'anim', str(f0), str(f1)],
                           stdout=log, stderr=subprocess.STDOUT, env=dict(os.environ, LH=LH, OUTR=LH + '/render'))
    lines = open(lp, errors='ignore').read().splitlines(); open(lp, 'w').write('\n'.join(lines[-60:]) + '\n')
    fd = LH + '/render/frames/S' + nn
    have = [fd + '/f%05d.png' % k for k in range(f0, f1) if os.path.exists(fd + '/f%05d.png' % k)]
    st = dict(shot=nn, f0=f0, f1=f1, need=f1 - f0, have=len(have), rc=r.returncode, sec=round(time.time() - t0))
    if len(have) == f1 - f0:
        mp4 = out + '/piece_%s_%05d_%05d.mp4' % (nn, f0, f1)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-start_number', str(f0), '-i', fd + '/f%05d.png',
                        '-frames:v', str(f1 - f0), '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', mp4], check=True)
        st['encoded'] = int(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0', '-show_entries',
                                                     'stream=nb_read_frames', '-of', 'csv=p=0', mp4]).strip())
        for f in have: os.remove(f)
    status.append(st); json.dump(status, open(out + '/status_%02d.json' % J, 'w'), indent=1); print(st, flush=True)
sys.exit(1 if [s for s in status if s.get('encoded') != s['need']] else 0)
