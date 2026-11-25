K=[('M_hook',0),('M_ac',7),('M_guard',17),('M_shirt',22),('M_cash',31),('M_atm',58),('M_atmscr',65),('M_food',75),('M_waiter',87),('M_snatch',99),('M_stranger',112),
('B_cut',123),('B_out',130),('B_fauji',135),('C_cinema',145),('C_advice',154),('N_cab',165),('N_tez',175),('N_switch',184),
('H_home',202),('H_abbu',214),('H_pizza',224),('H_stare',234),('H_switch',251),('H_bill',261),('H_end',265),('H_cta',279)]
h=open('_hdr.py').read().replace('KEYS_PLACEHOLDER',repr(K))
open('shots_by.py','w').write(h+'\n'+open('_body.py').read())
print(len(K))
