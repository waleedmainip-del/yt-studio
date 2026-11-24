K=[('M_hook',0),('M_plan',12),('M_six',23),('M_bilal',30),('M_kis',38),('M_toll',43),('M_donkey',52),('M_overtake',66),('M_hour',71),('M_chai',78),('M_family',89),('M_biryani',104),
('N_bhutta1',117),('N_bhutta2',129),('N_snow',136),('N_fridge',147),('N_stuck',153),('N_push',161),('N_chain',175),
('O_rates',187),('O_fog',205),('O_premium',212),
('L_selfie',218),('L_call',234),('L_proud',242),('R_ammi',249),('Q_photo',257),('R_snowman',268),('L_shock',281),('L_dhund',290),('Z_cta',300)]
h=open('_hdr.py').read().replace('KEYS_PLACEHOLDER',repr(K))
open('shots_by.py','w').write(h+'\n'+open('_body.py').read())
print(len(K))
