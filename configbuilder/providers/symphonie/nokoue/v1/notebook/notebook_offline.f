&notebook_offline
!---------------------------------------------------------------------------------
!set the "offline procedure" parameters:
ioffline=1   ! 0=not used    | 1=create files | 2=read files               
removetide=0 ! 0=total field | 1=remove tides from the total field      
!---------------------------------------------------------------------------------
!Files directory & name of the file containing the list of the offline file:
directory_offline='../../../{{ candidate.config_name }}/OFFLINE/'
   offlinefile(1)='../../../{{ candidate.config_name }}/OFFLINE/liste_offline.txt'
   offlinefile(2)='none'
   offlinefile(3)='none'
   offlinefile(4)='none'
   offlinefile(5)='none'
   offlinefile(6)='none'
!---------------------------------------------------------------------------------
! Relevant if ioffline=1:
! Additional variables: (yes=1, no=0)
  ofl_rotation=0      ! rotated currents (eastward & northward) 
  ofl_rhp=0           ! potential density
  ofl_tke=0           ! time-averaged turbulent kinetic energy
  ofl_surflux=0       ! time-averaged surface fluxes
  ofl_type='short'    ! ofl_type='real' ! 3D velocities T & S format
  ofl_sshtype='real'  ! ofl_sshtype='short' ! ssh format
  flag_maxbotstress=0 ! 1=time-averaged maximum bottom stress (Aurelien Gangloff Thesis Eq28)
!---------------------------------------------------------------------------------
/
Note: 1- no outputs if periodicity <=0 
      2- When the lastest date is passed, we continue with the latest periodicity
DO NOT MODIFY THE NEXT LINE AS IT IS THE SIGNAL EXPECTED BY S TO START THE TIME LIST!!!!
Periodicity (hours) ! until yyyy / mm / dd / hh / mm / ss ! Don't touch this line 
1.                       2016   10   01   12   00   00
1.                       2017   10   01   00   00   00    
