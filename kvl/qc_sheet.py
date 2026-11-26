# usage: qc_sheet.py <ghdir> <out.jpg> <step_frames> <cols> <width> <shot> [<shot> ...]
# contact sheet of rendered pieces: one thumbnail every <step> frames, labelled shot/frame
import sys, os, glob, subprocess, re
from PIL import Image, ImageDraw
G, out, step, cols, W = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]); shots = [int(x) for x in sys.argv[6:]]
src = open('/home/claude/kvl/shots_kvl.py').read(); SEQ = eval(re.search(r'^SEQ=(.*)$', src, re.M).group(1))
tmp = '/tmp/qc_%d' % os.getpid(); os.makedirs(tmp, exist_ok=True); ims = []
for s in shots:
    for f in sorted(glob.glob(G + '/piece_%02d_*.mp4' % s)):
        f0, f1 = [int(x) for x in os.path.basename(f)[:-4].split('_')[2:]]
        sel = [k for k in range(f0, f1) if (k - f0) % step == step // 2 or k == f1 - 1 and (f1 - f0) < step]
        for k in sel:
            o = '%s/%02d_%05d.png' % (tmp, s, k)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vf', 'select=eq(n\\,%d),scale=%d:-1' % (k - f0, W), '-frames:v', '1', o])
            if os.path.exists(o): ims.append((s, k, o))
if not ims: sys.exit('no frames')
im0 = Image.open(ims[0][2]); w, h = im0.size; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * h), '#101010'); d = ImageDraw.Draw(sheet)
for i, (s, k, o) in enumerate(ims):
    x, y = (i % cols) * w, (i // cols) * h; sheet.paste(Image.open(o).convert('RGB'), (x, y))
    d.rectangle((x, y, x + 92, y + 13), fill='#000000'); d.text((x + 2, y + 1), '%d %s f%d' % (s, SEQ[s - 1][0][:6], k), fill='#FFFF00')
sheet.save(out, quality=88); print(len(ims), sheet.size)
