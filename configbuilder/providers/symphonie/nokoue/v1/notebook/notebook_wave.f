&notebook_wave1
iwve=0 ! 0: off / 1: on
/

&notebook_wave2

txt_wavemodeltype='ww3_on_sgrid'  ! ww3 input field at "w" location of the grid (no interpolation)
wave_obc_type=1                     ! wave obc type
ww3_flagcumul=0                     ! wave model variables are 0=instantaneous 1=time-averaged

texte80(1)='../../../NOK_MORA_v391/LIST/list_dir'
texte80(2)='../../../NOK_MORA_v391/LIST/list_foc'
texte80(3)='../../../NOK_MORA_v391/LIST/list_hs'
texte80(4)='../../../NOK_MORA_v391/LIST/list_t'
texte80(5)='../../../NOK_MORA_v391/LIST/list_taw'
texte80(6)='../../../NOK_MORA_v391/LIST/list_two'
texte80(7)='../../../NOK_MORA_v391/LIST/list_uss'
texte80(8)='../../../NOK_MORA_v391/LIST/list_hsw'
!texte80(9)='../../../Nokoue/LIST/list_bhd' ! Bernouilli Head
/

wave obc type:

WAVE_OBC_TYPE=1:
The forcing fields did not take the wave effect into account

WAVE_OBC_TYPE=2:
The forcing fields took the wave effect into account and provide Lagrangian currents

WAVE_OBC_TYPE=3:
The forcing fields took the wave effect into account and provide eulerian currents

Exemple de script pour faire les listes:
#!/bin/bash
DIR=$1
ls $DIR/*nc > ../../../Nokoue/LIST/list_dir
ls $DIR/*nc > ../../../Nokoue/LIST/list_foc
ls $DIR/*nc > ../../../Nokoue/LIST/list_hs
ls $DIR/*nc > ../../../Nokoue/LIST/list_t
ls $DIR/*nc > ../../../Nokoue/LIST/list_taw
ls $DIR/*nc > ../../../Nokoue/LIST/list_two
ls $DIR/*nc > ../../../Nokoue/LIST/list_uss
ls $DIR/*nc > ../../../Nokoue/LIST/list_hsw
