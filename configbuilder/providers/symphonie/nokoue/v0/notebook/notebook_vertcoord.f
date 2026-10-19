&notebook_vertcoord

! Vertical distribution of the s levels

igesig=1       ! 0=sigma coordinate  1=generalized coordinate      
isigfile=0     ! sigma coodinate is: 0=computed or 1=read from "sigma.in" input file
hgesig=30.     ! 100.    ! H0. Regular sigma coordinate if h<H0. "Attracted" gen. coord. if h>H0

! Sigma / Step grid:
ihybsig=0      ! 0 unused. 1=compute the Hybrid s-step grid. 2=read it in a file  
nbvstepmin=5   ! Case IHYBSIG=1. Minimum number of levels (in the shallow areas)
sigstepgridfile="../../../{{ candidate.config_name }}/BATHYMASK/sigstepgridfile.nc"

!Obsolete parameters
!nhybsig=0    ! Case IHYBSIG=1. Number of loops of the iterative process              
!hstepmin=3.    ! Case IHYBSIG=1. Define "the shallow area" with a H criteria  
!hstepmax=150.  ! Case IHYBSIG=1. H1. Use the kmax "declared" levels when h>H1   
!verticalgridfile="../../../Nokoue/z_level.txt"
!ale_selected=0 ! "Arbitray Lagrangian Eulerian" grid (1=yes, 0=no)  

vststep=0
flag_merged_levels=0
dzsurfmin=1.5 ! if>0 dzsurfmin(m) preserves surface resolution: surface delta z = MIN (surface delta z, dzsurfmin )

/
