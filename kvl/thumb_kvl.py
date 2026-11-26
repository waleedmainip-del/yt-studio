# Thumbnail scene (not part of SEQ): Waleed on THE LINE with lassi + bun kabab, both captains shouting behind him
def THUMB():
    BOARD[0]=False; arena('kv_gold'); LF=mkfans('L',skip=(0,)); KF=mkfans('K',skip=(0,)); FILLE[0]=60
    sh=mk(SHEEDA,-1.4,.5,22,'sheeda'); gu=mk(GUDDU,1.4,.5,-22,'guddu'); wa=mk(WALEED,0,-.8,0,'wa')
    l2=in_hand(wa,-1,lassi_big); b2=in_hand(wa,1,bun_kabab); mu=stache(wa)
    for c in l2.children_recursive:
        if c.type=='MESH' and c.data.materials and c.data.materials[0].name.startswith('#E8554D'): c.hide_render=True
    def upd(t):
        place(wa,0,-.8,0); hstand(wa,t); blink(wa,t,force=0)
        for s,e in ((-1,l2),(1,b2)): wa['arm'][s].rotation_euler=(R(-48),0,R(s*32)); upright(e,wa,s,yaw=(180 if s<0 else 0))
        wa['head'].rotation_euler=(R(-3),R(-6),0); face(wa,mouth='grin',brow=.06,brow_r=4,eyes=1.12)
        for H,x,rz,s in ((sh,-1.4,22,1),(gu,1.4,-22,-1)):
            place(H,x,.5,rz); hstand(H,t); blink(H,t,force=0); H['root'].rotation_euler[0]=R(6)
            arms_up(H,1.0,t,spread=20,only=-s); H['arm'][s].rotation_euler=(R(-22),R(-s*4),0)
            look_at(H,hp(wa),.45); face(H,mouth='shout',brow=-.04,brow_r=-18,eyes=1.05)
        fans(LF,t,'fist',look=hp(wa)); fans(KF,t,'fist',look=hp(wa))
        camset((0,-4.7,1.3),(0,-.2,2.45),21,8)
    return dict(upd=upd)
SHOTS['THUMB']=THUMB
