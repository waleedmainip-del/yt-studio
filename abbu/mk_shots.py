K=[('M_hook',0),('M_ac',7),('M_guard',20),('M_shirt',25),('M_cash',33),('M_atm',51),('M_atmscr',61),('M_food',70),('M_waiter',80),('M_snatch',89),('M_stranger',102),
('B_cut',110),('B_out',120),('B_fauji',131),('C_cinema',138),('C_advice',150),('N_cab',162),('N_tez',177),('N_switch',185),
('H_home',204),('H_abbu',218),('H_pizza',228),('H_stare',238),('H_switch',246),('H_bill',256),('H_end',260),('H_cta',272)]
h=open('_hdr.py').read().replace('KEYS_PLACEHOLDER',repr(K))
open('shots_by.py','w').write(h+'\n'+open('_body.py').read())
print(len(K))
