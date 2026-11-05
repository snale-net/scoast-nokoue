&notebook_tracer1

 imodeltrc={{ candidate.enable }}   ! Passive tracers model: 1=on  0=off
 vbmax={{ candidate.let_out_count }}       ! Number of independent 3D tracers
 ksomax={{ candidate.let_out_count }}     ! Ponctual sources number
/

&notebook_tracer2

! Settling velocity for each tracer in m/s (sign convention:  <0):
wsed(1,1)=-0.

! Is the tracer a radionucleide or not (default =0)
radionucleide(1)=0

! Half-life radioactive decay for each tracer if they are radioactive in days (default is 1000000.):
TauR(1)=1000000.
{% for index, item in candidate.tracers_map.items() %}
! Let out n°{{ index }}
! Horizontal coordinates:
 socard( 0,{{ index }})=0     ! if a=0 then b=i c=j / if a=1 then b=lat(°) c=lon(°)
 socard( 1,{{ index }})=200   ! b
 socard( 2,{{ index }})=200   ! c
! Depth:
 socard(-1,{{ index }})=0     ! (a,b,c) if a=0 then b=kmin c=kmax / if a=1 then b=zmin c=zmax
 socard( 3,{{ index }})=1     ! b
 socard( 4,{{ index }})=10    ! c
! tracers concerned (min & max number)
 socard( 5,{{ index }})=1     ! tracers min number
 socard( 6,{{ index }})=1     ! tracers max number
 socard( 7,{{ index }})=0.001 ! Production term (per second)
! Dates:
 sodate(1:6,1,{{ index }})={{ item.start.strftime('%Y , %m , %d , %H , %M , %S') }} ! Start time (yyyy mm dd hh mm ss)
 sodate(1:6,2,{{ index }})={{ item.end.strftime('%Y , %m , %d , %H , %M , %S') }}  ! End   time (yyyy mm dd hh mm ss)
{% endfor %}
/