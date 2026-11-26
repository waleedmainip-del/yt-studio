# usage: qc_cuts.py <ghdir> <out_prefix> <width> [shots...]  -> first + last frame of every shot, labelled
import sys, os, glob, subprocess, re
from PIL import Image, ImageDraw
G, outp, W = sys.argv[1], sys.argv[2], int(sys.argv[3]); only = [int(x) for x in sys.argv[4:]]
src = open('/home/claude/kz/shots_kz.py').read(); SEQ = eval(re.search(r'^SEQ=(.*)$', src, re.M).group(1))
tmp = '/tmp/qcc_%d' % os.getpid(); os.makedirs(tmp, exist_ok=True); ims = []
for s in range(1, len(SEQ) + 1):
    if only and s not in only: continue
    ps = sorted(glob.glob(G + '/piece_%02d_*.mp4' % s), key=lambda f: int(os.path.basename(f).split('_')[2]))
    if not ps: continue
    for tag, f, n in (('first', ps[0], 0), ('last', ps[-1], None)):
        f0, f1 = [int(x) for x in os.path.basename(f)[:-4].split('_')[2:]]; k = 0 if n == 0 else f1 - f0 - 1
        o = '%s/%02d_%s.png' % (tmp, s, tag)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vf', 'select=eq(n\\,%d),scale=%d:-1' % (k, W), '-frames:v', '1', o])
        if os.path.exists(o): ims.append((s, tag, f0 + k, o))
cols = 8; per = 40
for si in range(0, len(ims), per):
    part = ims[si:si + per]; im0 = Image.open(part[0][3]); w, h = im0.size; rows = (len(part) + cols - 1) // cols
    sh = Image.new('RGB', (cols * w, rows * h), '#101010'); d = ImageDraw.Draw(sh)
    for i, (s, tag, k, o) in enumerate(part):
        x, y = (i % cols) * w, (i // cols) * h; sh.paste(Image.open(o).convert('RGB'), (x, y))
        d.rectangle((x, y, x + 110, y + 13), fill='#000000'); d.text((x + 2, y + 1), '%d %s %s f%d' % (s, SEQ[s - 1][0][:6], tag[0].upper(), k), fill='#FFFF00')
    sh.save('%s_%d.jpg' % (outp, si // per), quality=86); print(si // per, sh.size)
