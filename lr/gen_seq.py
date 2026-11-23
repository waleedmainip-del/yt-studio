# writes the SEQ line of shots_lr.py from the narration word times
import json,re
exec(open('remap.py').read()); W=remap_words(json.load(open('audio/words.json'))); s=lambda i:W[i]['s']; e=lambda i:W[i]['e']
spec=[('OPEN',0.0),('WANT',s(9)-.15),('MEET',s(19)-.25),('W1',s(28)-.12),('B1',s(34)-.12),('S1',s(41)-.12),('B2',s(49)-.1),('ARRIVE',s(53)-.5),('W2',s(59)-.15),('B3',s(65)-.1),('S2',s(71)-.1),
      ('ORDER',s(77)-.15),('B4',s(84)-.12),('S3',s(89)-.1),('B5',s(91)-.1),('EAT',e(93)+.3),('BILL',s(94)-.25),('SILENT',s(97)-.2),('W3',s(100)-.12),('B6',s(107)-.1),('S4',s(116)-.1),('W4',s(122)-.1),('B7',s(128)-.1),
      ('FREEZE',e(133)+.08),('APPS',s(134)-.15),('S5',s(141)-.12),('W5',s(147)-.12),('B8',s(150)-.12),('LOOKB',e(152)+.2),('WAITERIN',s(153)-.15),('WHO',s(156)-.12),('POINT',s(159)-.55),('MORAL',s(165)-.15),('DISHES',s(173)-.3),('WALK',s(177)-.65)]
seq=[(n,round(round(t*30)/30,3)) for n,t in spec]
assert all(seq[i][1]<seq[i+1][1] for i in range(len(seq)-1))
p='shots_lr.py'; t=open(p).read(); t=re.sub(r'^SEQ=\[.*\]$','SEQ='+repr(seq),t,flags=re.M); open(p,'w').write(t)
for i,(n,x) in enumerate(seq): print(i+1,n,x,round((seq[i+1][1] if i+1<len(seq) else 89.4333)-x,2))
