K=[('X_hook',0),('X_final',13),('X_chacha',32),('X_abbu',41),('X_bilal',52),('X_abbu92',61),('X_dada',73),('X_pak',88),('X_lastover',104),('X_yorker',112),('X_four',129),('X_hug',132),('X_dot',147),('X_cut',163),('X_ups',182),('X_stream',186),('X_buffer',190),('X_window',199),('X_radio',209),('X_six',223),('G_party',228),('X_replay',239),('G_back',250),('G_stubborn',259),('X_upscheck',269),('X_ammi',281),('X_cta',299)]
h=open('_hdr.py').read().replace('KEYS_PLACEHOLDER',repr(K))
open('shots_by.py','w').write(h+'\n'+open('_body.py').read())
print(len(K))
