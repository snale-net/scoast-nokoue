&notebook_vertcoord

! Vertical distribution of the s levels
! https://docs.google.com/document/d/1lCiiOzhpXSxY0fMnc9iKGCnMSZWYbfQBy1ypdYAXQG0/edit

igesig=1       ! 0=sigma coordinate  1=generalized coordinate

!..............................................
! Relevant if igesig=1 (generalized coordinate)
hgesig=30.     ! H0. Regular sigma coordinate if h<H0. "Attracted" gen. coord. if h>H0
!..............................................


!..............................................
! Relevant if igesig=0 (sigma coordinate)
dz_vertical_incr_fact=1.08  ! Depth Resolution Increasing Factor
!..............................................

!.........  VQS or (s-z hybrid) grid section  .......................
flag_merged_levels=0 ! merged levels if flag_merged_levels=1
vqs_cst1=300.        ! (m) Bathymetry envelope when true bathymetry=0
vqs_cst2=50.         ! (m) Hsig separates sigma area (h<Hsig) and vqs area (h>=Hsig)
vqs_cst3=1.          ! Curvature factor of the envelope bathymetry (avoid levels and bathymetry having opposite sign slopes)

! Relevant if flag_merged_levels=1:
nbvstepmin=5         ! Minimum number of levels

! Building the hybrid grid (VQS) from a file of "envelope bathymetry" characteristics:
! https://docs.google.com/document/d/1lCiiOzhpXSxY0fMnc9iKGCnMSZWYbfQBy1ypdYAXQG0/edit
 vqs_file='none'
!vqs_file='../../../NOK_MORA_v391/BATHYMASK/vqs_file'
!.........  VQS or (s-z hybrid) grid section  .......................

dzsurfmin=1.5 ! if>0 dzsurfmin(m) preserves surface resolution: surface delta z = MIN (surface delta z, dzsurfmin )

flag_z2dv_outputs=0 ! If=1 produce ascii files (named z2dv_OE_rank, z2dv_SN_rank) to visualize the position of grid levels in vertical planes


! Other parameters
isigfile=0     ! sigma coodinate is: 0=computed or 1=read from "sigma.in" input file

/
