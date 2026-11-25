K=[('A_hook',0),('A_job',8),('A_stop',24),('A_mirror',28),('A_drv1',37),('A_wal',45),('A_drv2',49),('A_gps',56),('A_cop',71),('A_scold',81),('A_ticket',91),('A_lassi',97),
('B_gate',108),('B_guard',122),('B_wait',130),('B_anda',144),('B_cv',153),('B_shazia',168),('B_pakki',173),('B_roti',183),
('C_walk',192),('C_win',201),('C_mub',211),('D_phone',218),('D_tv',228),('E_news',233),('D_sit',249),('D_pm',255),('F_pm',260),('D_cta',265)]
h=open('_hdr.py').read().replace('KEYS_PLACEHOLDER',repr(K))
open('shots_by.py','w').write(h+'\n'+open('_body.py').read())
print(len(K))
