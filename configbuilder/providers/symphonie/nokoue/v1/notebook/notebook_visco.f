&notebook_visco

!....................................
! Turbulence closure:
      iturbulence=1     ! Turbulence closure scheme: 
                        ! 0: Gaspar1990 
                        ! 1: K-Eps (Michaud et al, OS 2012)
                        ! 2: Kh=constant_Kh, Km=constant_Km
                        ! 3: Kh=Km=karman*L*sqrt( (du/dz)**2+(dv/dz)**2 ) Prandlt
      constant_km=1.e-6 ! Relevant if iturbulence=2
      constant_kh=1.e-7 ! Relevant if iturbulence=2

      emin=1.d-8  !1.d-7        ! Minimum value of the Turbulent Kinetic Energy (TKE)     
      epsmin=1.d-12     ! Minimum value for EPSIPLON       
      tke_surf=1        ! TKE surf cond: 0=PROduction DIssipation Equilibrium, 1=Craig & Banner

! Stability functions (relevant if k-eps selected):
!     flag_tke_stab_func='kc94' ! kantha Clayson 1994
      flag_tke_stab_func='ca01' ! Canuto A 2001
!     flag_tke_stab_func='gp88' ! Galperin 1988

! relevant if Gaspar selected:
      ctke1=0.1 !
      ctke2=0.7 ! 
! Gaspar equivalent to Craig et Banner 1994 scheme (SM,B)=(0.39,16.6) (provided Lespilon=Lkm)
!     ctke1=0.55  ! Km=l.q.SM=l.sqrt(2.tken).SM=l.sqrt(tken).sqrt(2).SM ==>ctke1=sqrt(2).SM=0.55
!     ctke2=0.17  ! epsilon=2.sqrt(2.tken).tken/(B.l)=(tken**3/2)*(1/l)*2.sqrt(2)/B ==> ctke2=2.sqrt(2)/B

!....................................
! At molecular scale: 
! Apel J. R., 1987, Principle of Ocean Physics, Table in Appendix Three:
      kmol_m=0.  !  1.049e-6   ! molecular viscosity
      kmol_h=0.  !  1.49e-7    ! molecular diffusivity for heat
      kmol_s=0.  !  1.5e-9     ! molecular diffusivity for salt


!....................................
! SURFACE LAYER:
      z0s=0.01                ! Default surface roughness (meters)
      momentum_input_depth=0.2  !1. ! Default momentum input depth (meters)

!....................................
! BOTTOM LAYER:
!  Bottom roughness 
      z0b=0.0005     ! Sea bottom roughness (meters)
! z0b from a netcdf file if available:
!texte250='../../../Nokoue/BATHYMASK/symphonie-symtools-comodo.nc' ! lon-lat-dependent from file
      z0b_land=0.1   ! Bottom roughness on land. Useful for bed rivers, flooding of land, ...
      zlevel_land=0. ! z levels (in meters) of sea land transition

!  Bottom Drag Coefficient:
      flag_linearfric=0      ! Linear bottom friction if flag_linearfric=1
      coef_linearfric=0.0001 ! (relevant if flag_linearfric=1) coef of the linear friction
      cdseuil=2.5d-3         ! Minimum value of the bottom drag coefficient    
      cdb_2dh=2.d-3          ! Drag coefficient for 2DH (kmax=1) simulations


! external/internal modes coupling (vel_u(:,:,:,2)  vel_v(:,:,:,2) only):
  inv_ekman_depth=2. ! 0.1 ! inverse of the Ekman bottom layer thickness in m**-1 

!....................................
! Convection:
      convect_yn=0    ! 1 or 2 or 3 = Quick convection methods, 0 otherwise                    

!....................................
! Time stepping:
      assel0=0.1 ! 0.05     ! Time filter coefficient for the Laplacian scheme (Marsaleix et al OM 2012)

/
