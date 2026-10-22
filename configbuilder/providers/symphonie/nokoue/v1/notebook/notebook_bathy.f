&notebook_bathy

!...............
! Land-Sea mask and (TEMPORARY) H file:
! NOTE: the bathymetry contained in the following file will be smoothed by the model so 
! don't consider it as the true bathymetry
  texte250='{{ candidate.texte250 }}'  ! land sea "mapped" mask and bathymetry old format

! Remove secondary bassins
flag_remove_secondary_bassins=1 ! activated if =1. Note: High cost if large grid

!...............
! Bounds and Smoothing if option=1
ioption=0             ! 1=apply smoothing and threshold options, 0 otherwise
 h_inf=0.4             ! h>h_inf(meters) (if ioption==1)
 h_inf_obc=10.         ! as h_inf but within a 10 points OBC layer
 rmax_=0.15            ! smoothing parameter "rmax". Default value 1/kmax if rmax<0
 hrmax=20.             ! (m) prevents division by 0 in r=abs(delta_H)/max(2H,hrmax) < rmax
 nsmooth=10            ! loop number in the smoothing "regular" routine
 flag1_smooth_h_mask=1 ! flag related to the "regular" smoothing routine (see explanation below)
 flag3_smooth_h_mask=1 ! flag related to the "rmax"    smoothing routine

!flag_smooth_h_mask=0: all points are smoothed in the same way regardless of the value of the sea/land mask.
!flag_smooth_h_mask=1: Only the sea points are smoothed. Nil gradient condition perpendicular to the coast.
!flag_smooth_h_mask=2: Only the sea points are smoothed. Dirichlet condition at the coast.

!...............
! Wetdry parameters:
wetdry_cst1=0.5             ! h for cancellation of baroclinic velocities
wetdry_cst2=0.1             ! h for cancellation of barotropic velocities
wetdry_cst3=0.01            ! h for cancellation of traceur tendencies
!...............

!..............
! Mangrove setting:
mangrove_file_name='{{ candidate.mangrove_file_name }}'     ! magrove sea mask file
coef_diss_mangrove=0.01     ! Coef of the linear mangrove friction
linear_coef_mangrove=0      ! 0 for quadratic law or 1 for linear coef in mangrove
mangrove_scheme     =1      ! 1 = Eq7 method, Eq9 method otherwise

! CD3D in wave non-hydrostatic model ONLY !
 flag_cd3d=1 ! CD3D Drag linear & quadratic terms
!flag_cd3d=2 ! CD3D Drag linear & quadratic terms + intertiel resistance term

! https://docs.google.com/document/d/1V9cnPdDir-x3Ic3DjFHDpJ8osOkKobqs4pt5z4iHTPU/edit
!..............


!...............
! Merge the bathymetry with the external ogcm bathy within a boundary sponge layer
  mergebathy_filename='nomerge' ! if no merge...
! Size of the boundary layer where the merge is applied:
  mergebathy_sponge=0  ! no merge
!...............

!..................
flag_bathy_update=0 ! =1: bathymetry variable with time

/


&notebook_bathy2
! post smoothed bathymetry corrector file
  texte250='none' 
! texte250='../../../Nokoue/BATHYMASK/post_smoothed_bathy_corrector.ijDeltaH' ! i (glb), j(glb) , delta H(m), distance (indexes)
/
