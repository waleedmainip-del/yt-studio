import re
s=open('shots_by.py').read()
K="""A_open 0, A_two 11, A_today 21, A_clock 30, A_ammi 40, A_five 47, A_ramzan 51, A_pull 60,
B_wake 67, B_insta 82, B_later 86, B_kamre 89, B_imp 95, B_kya 103, B_research 104, B_cat 105,
C_enter 116, C_bottles 127, C_charger 131, C_godaam 138, C_please 145, C_shirt 160, C_teen 165, C_decor 173,
D_lie 180, D_dream 191, D_calls 204, D_bro 209, D_unavail 220, D_kal 226, D_ups 235,
E_arrive 242, E_fix 247, E_beta 263, E_career 270, E_mash 288, E_sus 292, E_blanket 300,
F_night 311, F_promise 331, F_alarm 345,
G_morning 353, G_eye 361, G_monday 375, G_life 378, G_legend 391, G_five 395"""
L=[(a.split()[0],int(a.split()[1])) for a in K.replace('\n',' ').split(',')]
s=re.sub(r"_K=\[.*?\]\n",'_K='+repr(L)+'\n',s,count=1,flags=re.S)
s=s.replace('/home/claude/boy/audio/words.json','/home/claude/boy/audio_ur/words.json')
RANGES={(27,33):(40,46),(34,37):(47,50),(38,46):(51,59),(64,67):(82,85),(71,76):(89,94),(77,81):(95,102),(82,82):(103,103),(83,83):(104,104),
(115,121):(138,144),(122,131):(145,159),(137,144):(165,172),(145,149):(173,179),(159,170):(191,203),(173,183):(209,219),(184,187):(220,225),
(188,196):(226,234),(197,203):(235,241),(219,225):(263,269),(226,238):(270,287),(239,242):(288,291),(248,258):(300,310),(271,282):(331,344),(311,313):(375,377)}
for (a,b),(c,d) in RANGES.items():
    p="t,%d,%d,KEY"%(a,b); assert p in s,p; s=s.replace(p,"t,%d,%d,KEY"%(c,d))
for o,nw in ((65,83),(255,307),(258,310),(281,343),(298,361),(302,366),(306,370)):
    for f in ('wl','we'): s=s.replace("%s(%d,KEY)"%(f,o),"%s(%d,KEY)"%(f,nw))
open('shots_by_ur.py','w').write(s); print('ok')
