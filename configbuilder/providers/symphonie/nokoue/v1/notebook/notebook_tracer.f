&notebook_tracer1

imodeltrc=0   ! Passive tracers model: 1=on  0=off
 vbmax=3       ! Number of independent 3D tracers
 ksomax=0      ! Ponctual sources number

/

&notebook_tracer2

! Settling velocity for each tracer in m/s (sign convention:  <0):
wsed(1,1)=-0.

! Is the tracer a radionucleide or not (default =0)
radionucleide(1)=0

! Half-life radioactive decay for each tracer if they are radioactive in days (default is 1000000.):
TauR(1)=1000000.
!TauR(2)=8.0 ! for exemple Iode_131

! Concentrations at river mouth
! Must be specified for all rivers (same order as in notebook_river) and for all tracers:
! river_bio(tracer counter,river counter,1)=100.
! river_bio(1,1,1)=100. ! variable n°1 river n°1
! river_bio(2,1,1)=100. ! variable n°2 river n°1

! river_bio(1,2,1)=100. ! variable n°1 river n°2
! river_bio(2,2,1)=100. ! variable n°2 river n°2

! river_bio(1,3,1)=100. ! variable n°1 river n°3
! river_bio(2,3,1)=100. ! variable n°2 river n°3

! river_bio(1,4,1)=100. ! variable n°1 river n°4
! river_bio(2,4,1)=100. ! variable n°2 river n°4

!! Additional source points:
!! Source n°1 - 1Oct
!! Horizontal coordinates:
! socard( 0,1)=0     ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,1)=200   ! b
! socard( 2,1)=200   ! c
!! Depth:
! socard(-1,1)=0     ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,1)=1     ! b
! socard( 4,1)=10    ! c
!! tracers concerned (min & max number)
! socard( 5,1)=1     ! tracers min number
! socard( 6,1)=1     ! tracers max number
! socard( 7,1)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,1)= 2017 , 09 , 30 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,1)= 2017 , 10 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°2 - 15Oct
!! Horizontal coordinates:
! socard( 0,2)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,2)=200  ! b
! socard( 2,2)=200  ! c
!! Depth:
! socard(-1,2)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,2)=1    ! b
! socard( 4,2)=10   ! c
!! tracers concerned (min & max number)
! socard( 5,2)=2     ! tracers min number
! socard( 6,2)=2     ! tracers max number
! socard( 7,2)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,2)= 2017 , 10 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,2)= 2017 , 10 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°3 - 1Nov
!! Horizontal coordinates:
! socard( 0,3)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,3)=200  ! b
! socard( 2,3)=200  ! c
!! Depth:
! socard(-1,3)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,3)=1    ! b
! socard( 4,3)=10   ! c
!! tracers concerned (min & max number)
! socard( 5,3)=3     ! tracers min number
! socard( 6,3)=3     ! tracers max number
! socard( 7,3)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,3)= 2017 , 10 , 31 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,3)= 2017 , 11 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°4 - 15Nov
!! Horizontal coordinates:
! socard( 0,4)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,4)=200  ! b
! socard( 2,4)=200  ! c
!! Depth:
! socard(-1,4)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,4)=1    ! b
! socard( 4,4)=10   ! c
!! tracers concerned (min & max number)
! socard( 5,4)=4     ! tracers min number
! socard( 6,4)=4     ! tracers max number
! socard( 7,4)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,4)= 2017 , 11 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,4)= 2017 , 11 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°5 - 1Dec
!! Horizontal coordinates:
! socard( 0,5)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,5)=200  ! b
! socard( 2,5)=200  ! c
!! Depth:
! socard(-1,5)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,5)=1    ! b
! socard( 4,5)=10   ! c
!! tracers concerned (min & max number)
! socard( 5,5)=5     ! tracers min number
! socard( 6,5)=5     ! tracers max number
! socard( 7,5)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,5)= 2017 , 11 , 30 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,5)= 2017 , 12 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°6 - 15Dec
!! Horizontal coordinates:
! socard( 0,6)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,6)=200  ! b
! socard( 2,6)=200  ! c
!! Depth:
! socard(-1,6)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,6)=1    ! b
! socard( 4,6)=10   ! c
!! tracers c6ncerned (min & max number)
! socard( 5,6)=6     ! tracers min number
! socard( 6,6)=6     ! tracers max number
! socard( 7,6)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,6)= 2017 , 12 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,6)= 2017 , 12 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°7 - 1Jan
!! Horizontal coordinates:
! socard( 0,7)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,7)=200  ! b
! socard( 2,7)=200  ! c
!! Depth:
! socard(-1,7)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,7)=1    ! b
! socard( 4,7)=10   ! c
!! tracers c7ncerned (min & max number)
! socard( 5,7)=7     ! tracers min number
! socard( 6,7)=7     ! tracers max number
! socard( 7,7)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,7)= 2017 , 12 , 31 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,7)= 2018 , 01 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°8 - 15Jan
!! Horizontal coordinates:
! socard( 0,8)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,8)=200  ! b
! socard( 2,8)=200  ! c
!! Depth:
! socard(-1,8)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,8)=1    ! b
! socard( 4,8)=10   ! c
!! tracers c8ncerned (min & max number)
! socard( 5,8)=8     ! tracers min number
! socard( 6,8)=8     ! tracers max number
! socard( 7,8)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,8)= 2018 , 01 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,8)= 2018 , 01 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°9 - 1Fev
!! Horizontal coordinates:
! socard( 0,9)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,9)=200  ! b
! socard( 2,9)=200  ! c
!! Depth:
! socard(-1,9)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,9)=1    ! b
! socard( 4,9)=10   ! c
!! tracers c9ncerned (min & max number)
! socard( 5,9)=9     ! tracers min number
! socard( 6,9)=9     ! tracers max number
! socard( 7,9)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,9)= 2018 , 01 , 31 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,9)= 2018 , 02 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°10 - 15Fev
!! Horizontal coordinates:
! socard( 0,10)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,10)=200  ! b
! socard( 2,10)=200  ! c
!! Depth:
! socard(-1,10)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,10)=1    ! b
! socard( 4,10)=10   ! c
!! tracers c10ncerned (min & max number)
! socard( 5,10)=10    ! tracers min number
! socard( 6,10)=10    ! tracers max number
! socard( 7,10)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,10)= 2018 , 02 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,10)= 2018 , 02 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°11 - 1Mar
!! Horizontal coordinates:
! socard( 0,11)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,11)=200  ! b
! socard( 2,11)=200  ! c
!! Depth:
! socard(-1,11)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,11)=1    ! b
! socard( 4,11)=10   ! c
!! tracers c11ncerned (min & max number)
! socard( 5,11)=11    ! tracers min number
! socard( 6,11)=11    ! tracers max number
! socard( 7,11)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,11)= 2018 , 02 , 28 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,11)= 2018 , 03 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°12 - 15Mar
!! Horizontal coordinates:
! socard( 0,12)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,12)=200  ! b
! socard( 2,12)=200  ! c
!! Depth:
! socard(-1,12)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,12)=1    ! b
! socard( 4,12)=10   ! c
!! tracers c12ncerned (min & max number)
! socard( 5,12)=12    ! tracers min number
! socard( 6,12)=12    ! tracers max number
! socard( 7,12)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,12)= 2018 , 03 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,12)= 2018 , 03 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°13 - 1Avr
!! Horizontal coordinates:
! socard( 0,13)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,13)=200  ! b
! socard( 2,13)=200  ! c
!! Depth:
! socard(-1,13)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,13)=1    ! b
! socard( 4,13)=10   ! c
!! tracers c13ncerned (min & max number)
! socard( 5,13)=13    ! tracers min number
! socard( 6,13)=13    ! tracers max number
! socard( 7,13)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,13)= 2018 , 03 , 31 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,13)= 2018 , 04 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°14 - 15Avr
!! Horizontal coordinates:
! socard( 0,14)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,14)=200  ! b
! socard( 2,14)=200  ! c
!! Depth:
! socard(-1,14)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,14)=1    ! b
! socard( 4,14)=10   ! c
!! tracers c14ncerned (min & max number)
! socard( 5,14)=14    ! tracers min number
! socard( 6,14)=14    ! tracers max number
! socard( 7,14)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,14)= 2018 , 04 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,14)= 2018 , 04 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°15 - 1May
!! Horizontal coordinates:
! socard( 0,15)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,15)=200  ! b
! socard( 2,15)=200  ! c
!! Depth:
! socard(-1,15)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,15)=1    ! b
! socard( 4,15)=10   ! c
!! tracers c15ncerned (min & max number)
! socard( 5,15)=15    ! tracers min number
! socard( 6,15)=15    ! tracers max number
! socard( 7,15)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,15)= 2018 , 04 , 30 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,15)= 2018 , 05 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°16 - 15May
!! Horizontal coordinates:
! socard( 0,16)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,16)=200  ! b
! socard( 2,16)=200  ! c
!! Depth:
! socard(-1,16)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,16)=1    ! b
! socard( 4,16)=10   ! c
!! tracers c16ncerned (min & max number)
! socard( 5,16)=16    ! tracers min number
! socard( 6,16)=16    ! tracers max number
! socard( 7,16)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,16)= 2018 , 05 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,16)= 2018 , 05 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°17 - 1Jun
!! Horizontal coordinates:
! socard( 0,17)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,17)=200  ! b
! socard( 2,17)=200  ! c
!! Depth:
! socard(-1,17)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,17)=1    ! b
! socard( 4,17)=10   ! c
!! tracers c17ncerned (min & max number)
! socard( 5,17)=17    ! tracers min number
! socard( 6,17)=17    ! tracers max number
! socard( 7,17)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,17)= 2018 , 05 , 31 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,17)= 2018 , 06 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°18 - 15Jun
!! Horizontal coordinates:
! socard( 0,18)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,18)=200  ! b
! socard( 2,18)=200  ! c
!! Depth:
! socard(-1,18)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,18)=1    ! b
! socard( 4,18)=10   ! c
!! tracers c18ncerned (min & max number)
! socard( 5,18)=18    ! tracers min number
! socard( 6,18)=18    ! tracers max number
! socard( 7,18)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,18)= 2018 , 06 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,18)= 2018 , 06 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°19 - 1Jul
!! Horizontal coordinates:
! socard( 0,19)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,19)=200  ! b
! socard( 2,19)=200  ! c
!! Depth:
! socard(-1,19)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,19)=1    ! b
! socard( 4,19)=10   ! c
!! tracers c19ncerned (min & max number)
! socard( 5,19)=19    ! tracers min number
! socard( 6,19)=19    ! tracers max number
! socard( 7,19)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,19)= 2018 , 06 , 30 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,19)= 2018 , 07 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°20 - 15Jul
!! Horizontal coordinates:
! socard( 0,20)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,20)=200  ! b
! socard( 2,20)=200  ! c
!! Depth:
! socard(-1,20)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,20)=1    ! b
! socard( 4,20)=10   ! c
!! tracers c20ncerned (min & max number)
! socard( 5,20)=20    ! tracers min number
! socard( 6,20)=20    ! tracers max number
! socard( 7,20)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,20)= 2018 , 07 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,20)= 2018 , 07 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°21 - 1Aug
!! Horizontal coordinates:
! socard( 0,21)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,21)=200  ! b
! socard( 2,21)=200  ! c
!! Depth:
! socard(-1,21)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,21)=1    ! b
! socard( 4,21)=10   ! c
!! tracers c21ncerned (min & max number)
! socard( 5,21)=21    ! tracers min number
! socard( 6,21)=21    ! tracers max number
! socard( 7,21)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,21)= 2018 , 07 , 31 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,21)= 2018 , 08 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°22 - 15Aug
!! Horizontal coordinates:
! socard( 0,22)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,22)=200  ! b
! socard( 2,22)=200  ! c
!! Depth:
! socard(-1,22)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,22)=1    ! b
! socard( 4,22)=10   ! c
!! tracers c22ncerned (min & max number)
! socard( 5,22)=22    ! tracers min number
! socard( 6,22)=22    ! tracers max number
! socard( 7,22)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,22)= 2018 , 08 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,22)= 2018 , 08 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°23 - 1Sep
!! Horizontal coordinates:
! socard( 0,23)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,23)=200  ! b
! socard( 2,23)=200  ! c
!! Depth:
! socard(-1,23)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,23)=1    ! b
! socard( 4,23)=10   ! c
!! tracers c23ncerned (min & max number)
! socard( 5,23)=23    ! tracers min number
! socard( 6,23)=23    ! tracers max number
! socard( 7,23)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,23)= 2018 , 08 , 31 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,23)= 2018 , 09 , 01 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)
!
!! Source n°24 - 15Sep
!! Horizontal coordinates:
! socard( 0,24)=0.   ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
! socard( 1,24)=200  ! b
! socard( 2,24)=200  ! c
!! Depth:
! socard(-1,24)=0    ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
! socard( 3,24)=1    ! b
! socard( 4,24)=10   ! c
!! tracers c24ncerned (min & max number)
! socard( 5,24)=24    ! tracers min number
! socard( 6,24)=24    ! tracers max number
! socard( 7,24)=0.001 ! Production term (per second)
!! Dates:
! sodate(1:6,1,24)= 2018 , 09 , 14 , 23  , 59  , 00  ! Start time (yyyy mm dd hh mm ss)
! sodate(1:6,2,24)= 2018 , 09 , 15 , 00  , 00  , 10  ! End   time (yyyy mm dd hh mm ss)

/
