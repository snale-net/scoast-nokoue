&notebook_spongelayer

! Define the parameters of the lateral nudging (or sponge) layer

! Sponge layer depending on distance ( 'dist') or on horizontal resolution ( 'dxdy' )
 flag_sponge_txt='dist'
!flag_sponge_txt='dxdy'
! details of the 'dxdy' option in:
! https://docs.google.com/document/d/10A6XnRxEiuXqTIloBfFt_G-bFn-UHUw95E49TuttA0w/edit

! sponge_l is the size of the nudging/sponge layer (relevant if flag_sponge_txt=='dist')
sponge_l=30     ! Width (in grid nodes) of the nudging/sponge layer              

! sponge_dx_critic is the resolution below which the restoring force is applied (relevant if flag_sponge_txt=='dxdy')
 sponge_dx_critic=2500.  !meters (relevant if flag_sponge_txt=='dxdy')

! sponge_dx_width is the decay scale of the hyperbolic tangent function (relevant if flag_sponge_txt=='dxdy')
 sponge_dx_width=1000. !meters (relevant if flag_sponge_txt=='dxdy')

! Barotropic velocity:
relax_ext=0.1   ! Nudging time scale (days) for barotropic velocity. 
                ! UNUSED IF relax_ext<0.

! Baroclinic velocity:
relax_int=1.    ! Nudging time scale (days) for baroclinic velocity. 
                ! UNUSED IF relax_int<0.

! Temperature and Salinity:
! Scheme:
relaxtype_ts=1  ! 2= full grid + low frequency filter
                ! 1= sponge layer only, restoring force is current dependent
                ! 5= sponge layer only, restoring force is based on relax_ts 

relax_ts=60.    ! Case relaxtype_ts=2: relax_ts is a nudging time scale (days)
                ! Case relaxtype_ts=1: the nudging time scale depends on velocity.
                ! UNUSED IF relax_ts<0.

! T,S advection in spongelayer
! https://docs.google.com/document/d/1djA4xtqN5U-kf0c0ezLFCydew2Ln4VrcIBjUh8G-dAs/edit
flag_upwind_obc=0 ! upwind advection for T,S at the open borders if flag_upwind_obc=1

! Obsolete settings
relax_es=-999.   ! Time scale (days) for a domain-averaged conserved ssh         
OBCFREEORFIX=0   ! Flather OBC scheme in external mode.  0=Forced by OGCM, 1=Forced by LF  OBCFREEORFIX
RELAX_BPC=-9999. ! UNUSED - Nudging time scale (days) for bottom pressure                  RELAX_BPC
OBCTYPE_TS=0     ! Scheme for T,S OBC                                                      OBCTYPE_TS
OBCTYPE_P=0      ! UNUSED - Scheme for P OBC - UNSUSED                                     OBCTYPE_P

/
