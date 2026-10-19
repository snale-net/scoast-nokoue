&notebook_time

! Enter the time for the start and the end of the simulation:
datesim(1:6,1)={{ candidate.start_time.strftime('%Y , %m , %d , %H , %M , %S') }} ! Start time (yyyy mm dd hh mm ss)
datesim(1:6,2)={{ candidate.end_time.strftime('%Y , %m , %d , %H , %M , %S') }}  ! End   time (yyyy mm dd hh mm ss)

! Define datesim(1:6,2) from a maximum number of iterations of the internal mode:
iteration3d_max=-999 ! active if > 0 . Number of iterations from datesim(1:6,1) 

!-----------------------------------------------------------------------------------
! Initial state:
initial=0               ! 0> Standard procedure  >1 Start from the end the previous simulation
restartfileperiod=30.   ! Production periodicity (see restartfileunits) of the restart files (no file if <=0.)
restartfileunits='d'    ! units of restartfileperiod. 'd'=days, 'm'=minutes, 's'=seconds
flag_0status_option=0   ! 0=stop if field not found, 1=ignore and go on if field not found
flag_binary=0           ! 0= new netcdf restart files. 1= old chanel9 restart files

!-----------------------------------------------------------------------------------
! Time step: 
! External mode: set the CFL input parameters of the barotropic momentum equation
   cfl_sshmax=3.           ! A priori maximum value for the sea surface height (m)  
   cfl_umax=3.             ! A priori maximum value for the current (m/s)             
   cfl_reduce=1.8          ! A priori attenuation factor for the CFL first guess

! Internal mode:
! Option 1: give the ratio dt_internal/dt_external
   iteration2d_max_now=16  ! ratio dt_internal/dt_external   
! Option 2: give the internal step (iteration2d_max_now will be adjusted)
!  dti_fw=180.             ! internal time step in seconds

!-------------------------------------------------------------------------------------
! Simulation mode:
run_option={{ candidate.run_mode }} ! 0=Standard procedure  -1=Stop the simulation at the end of the initialization

/

Note about RESTARTFILEPERIOD:
If RESTARTFILEPERIOD=0 or RESTARTFILEPERIOD<0 no restart file
Otherwise RESTARTFILEPERIOD indicates the periodicity (in days) of the restart file production.
If RESTARTFILEPERIOD>=0 a restart file is created at the end of the simulation.
