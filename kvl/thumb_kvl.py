# Thumbnail scene (not part of SEQ): Lahore captain | Waleed on THE LINE with lassi + bun kabab | Karachi captain
def THUMB():
    BOARD[0]=False; arena('kv_gold'); LF=mkfans('L',skip=(0,)); KF=mkfans('K',skip=(0,)); FILLE[0]=60
    sh=mk(SHEEDA,-1.62,-.1,26,'sheeda'); gu=mk(GUDDU,1.62,-.1,-26,'guddu'); wa=mk(WALEED,0,-.75,0,'wa')
    l2=in_hand(wa,-1,lassi_big); b2=in_hand(wa,1,bun_kabab); mu=stache(wa)
    def upd(t):
        place(wa,0,-.75,0); hstand(wa,t); blink(wa,t,force=0)
        for s,e in ((-1,l2),(1,b2)): wa['arm'][s].rotation_euler=(R(-96),0,R(s*36)); upright(e,wa,s)
        wa['head'].rotation_euler=(R(-4),R(-7),0); face(wa,mouth='grin',brow=.06,brow_r=4,eyes=1.12)
        for H,x,rz,s in ((sh,-1.62,26,1),(gu,1.62,-26,-1)):
            place(H,x,-.1,rz); hstand(H,t); blink(H,t,force=0); H['root'].rotation_euler[0]=R(7)
            bpy.context.view_layer.update(); arm_to(H,s,hp(wa,-.1),1.0,base=(0,0,0)); H['arm'][-s].rotation_euler=(R(-150),R(-s*20),0)
            look_at(H,hp(wa),1.0); face(H,mouth='shout',brow=-.04,brow_r=-18,eyes=1.05)
        fans(LF,t,'fist',look=hp(wa),talky=False); fans(KF,t,'fist',look=hp(wa),talky=False)
        camset((0,-4.6,1.42),(0,-.3,2.32),19,8)
    return dict(upd=upd)
SHOTS['THUMB']=THUMB
