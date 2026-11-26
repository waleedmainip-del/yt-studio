# usage: collect_kvl.py <tag> <rev:runid> [<rev:runid> ...]   (later revs override earlier ones, per shot)
# fetches render/kvl-<runid>-jN branches into gh/r<rev>/, merges the newest pieces per shot into gh/<tag>/
import sys, os, subprocess, glob, json, shutil, re
P = '/home/claude/kvl'; Y = '/home/claude/yt-studio'
src = open(P + '/shots_kvl.py').read()
SEQ = eval(re.search(r'^SEQ=(.*)$', src, re.M).group(1)); END = float(re.search(r'^END=(.*)$', src, re.M).group(1))
G = [int(round(t * 30)) for _, t in SEQ] + [int(round(END * 30))]
tag = sys.argv[1]; revs = [(int(a.split(':')[0]), a.split(':')[1]) for a in sys.argv[2:]]
have = {}
for rev, rid in sorted(revs):
    d = P + '/gh/r%d' % rev; os.makedirs(d, exist_ok=True)
    subprocess.run(['git', 'fetch', '-q', '-f', 'origin', 'refs/heads/render/kvl-%s-*:refs/remotes/origin/render/kvl-%s-*' % (rid, rid)], cwd=Y)
    brs = subprocess.check_output(['git', 'branch', '-r', '--list', 'origin/render/kvl-%s-*' % rid], cwd=Y, text=True).split()
    for b in brs:
        j = b.rsplit('-j', 1)[1]; dj = d + '/j' + j
        if not os.path.exists(dj + '/.done'):
            os.makedirs(dj, exist_ok=True)
            a = subprocess.Popen(['git', 'archive', b], cwd=Y, stdout=subprocess.PIPE); subprocess.run(['tar', '-x', '-C', dj], stdin=a.stdout); a.wait(); open(dj + '/.done', 'w').write('1')
    for f in glob.glob(d + '/j*/**/piece_*.mp4', recursive=True):
        nn, f0, f1 = os.path.basename(f)[:-4].split('_')[1:]; have.setdefault(int(nn), {}).setdefault(rev, []).append((int(f0), int(f1), f))
    print('rev', rev, 'branches', len(brs))
out = P + '/gh/' + tag; os.makedirs(out, exist_ok=True)
bad = [(f, s) for f in glob.glob(P + '/gh/r*/j*/**/status_*.json', recursive=True) for s in json.load(open(f)) if s.get('encoded') != s['need']]
print('BAD', bad)
missing = []; use = {}
for s in range(1, len(SEQ) + 1):
    g0, g1 = G[s - 1], G[s]; best = None
    for rev in sorted(have.get(s, {}), reverse=True):
        ps = sorted(have[s][rev]); ok = ps and ps[0][0] == g0 and ps[-1][1] == g1 and all(a[1] == b[0] for a, b in zip(ps, ps[1:]))
        if ok: best = (rev, ps); break
    if not best: missing.append(s); continue
    use[s] = best[0]
    for old in glob.glob(out + '/piece_%02d_*.mp4' % s): os.remove(old)
    for f0, f1, f in best[1]: shutil.copyfile(f, out + '/' + os.path.basename(f))
json.dump([dict(need=1, encoded=1)], open(out + '/status_00.json', 'w'))
print('used', ' '.join('%d:r%d' % (s, r) for s, r in sorted(use.items()))); print('MISSING', missing)
