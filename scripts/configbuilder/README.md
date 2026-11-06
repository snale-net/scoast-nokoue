## Singularity definition file

```
export SINGULARITY_TMPDIR=/singularity
module load singularity/4.1.5
singularity build --fakeroot --bind /work/softs/rh8/spack_install/linux-rhel8-x86_64/gcc-8.5.0/intel-oneapi-compilers-2021.3.0-po2unejzdcprr7unoes754heiqovvwbw/ --bind /work/softs/rh8/spack_install_20/linux-rhel8-x86_64/gcc-8.5.0/intel-oneapi-mpi-2021.10.0-a4vpkrrwo5bemjm5tfa2d57c4u6pbky7/ --bind /etc/pki/ca-trust/extracted/pem/ --bind /usr/share/Modules /work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/containers/symphonie-prebuilt.sif /work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/containers/symphonie-prebuilt.def
singularity build --fakeroot --bind /work/softs/rh8/spack_install/linux-rhel8-x86_64/gcc-8.5.0/intel-oneapi-compilers-2021.3.0-po2unejzdcprr7unoes754heiqovvwbw/ --bind /work/softs/rh8/spack_install_20/linux-rhel8-x86_64/gcc-8.5.0/intel-oneapi-mpi-2021.10.0-a4vpkrrwo5bemjm5tfa2d57c4u6pbky7/ /work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/containers/symphonie-v1.0.sif /work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/containers/symphonie-v1.0.def
```

### Submission file

```
#SBATCH --job-name=symphonie_run
#SBATCH --output=log-%j.out
#SBATCH --error=log-%j.err
#SBATCH -N 2
#SBATCH -n 180
#SBATCH --time=3-00:00:00
#SBATCH --account=XXXXX
#SBATCH --exclusive

module load singularity/4.1.5
module load intel-oneapi-mpi/2021.10.0
module use --append /work/DTF/common/UC/SCOAST/NK/sharedmodules
module load ucx/1.16.0

cd config-dir
rm RUN/tmp/*

mpirun -np 180 singularity exec --pwd /model/SYMPHONIE_v391/RDIR/NOK_MORA_v391 \
	--bind ${PWD}:/model/NOK_MORA_v391 \
    --bind /work/softs/rh8/spack_install/linux-rhel8-x86_64/gcc-8.5.0/intel-oneapi-compilers-2021.3.0-po2unejzdcprr7unoes754heiqovvwbw/ \
    --bind /work/softs/rh8/spack_install_20/linux-rhel8-x86_64/gcc-8.5.0/intel-oneapi-mpi-2021.10.0-a4vpkrrwo5bemjm5tfa2d57c4u6pbky7/ \
	/work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/containers/symphonie-v1.0.sif \
    ./symphonie.exe
```

## Scripts

### 1. Generate the REF2018 configuration

`generate_ref2018.py`


## How to use

```bash
docker run \
  -v /XXXX/grid/:/XXXX/grid \
  -v /XXXX/forcings/:/XXXX/forcings/ \
  -v /XXXX/config/:/XXXX/config/  \
  -it "scoast-nokoue:1.3" python /app/configbuilder/generate_ref2018.py \
  -n REF2018-TRACERS \
  -o /XXXX/config/ \
  --start-time "2017-11-01 00:00:00" \
  --end-time "2019-01-01 00:00:00" \    
  --grid_notebook_path  /XXXX/grid/notebook_grid.f \ 
  --grid_coordinates_path /XXXX/grid/lonlat_Cotonou_20190211.nc \ 
  --grid_bathycote_path  /XXXX/grid/bathycote_in_CNES_V1.0.ijh  \ 
  --mpi_domain_path  /XXXX/grid/description_domaine_180.next \ 
  --mpi_hole_path  /XXXX/grid/description_trous_180.txt \ 
  --acadjas_mask_path  /XXXX/grid/mask_mangrove_cnes.dat \ 
  --tracers_let_out_count 0 \
  --tracers_let_out_freq BMM  \
  --meteo_forcing_path /XXXX/forcings/ecmwf/2016-2019 \
  --ocean_forcing_path /XXXX/forcings/mercator \
  --tide_forcing_path /XXXX/forcings/fes2014  \  
  --river_so_discharge_path /XXXX/forcings/rivers/Yves_R1012_6m3s/SO_academic_new.dat  \ 
  --river_oueme_discharge_path /XXXX/forcings/rivers/Yves_R1012_6m3s/OUEME_academic_new.dat \ 
  --river_djonou_discharge_path /XXXX/forcings/rivers/Yves_R1012_6m3s/DJONOU_academic_new.dat

singularity exec  \
  --bind /XXXX/grid \
  --bind /XXXX/forcings  \
  --bind /XXX/config  \
  scoast-nokoue-v1.3.sif  \
  python /app/configbuilder/generate_ref2018.py 
  -n REF2018-TRACERS \
  -o /XXXX/config/ \
  --start-time "2017-11-01 00:00:00" \
  --end-time "2019-01-01 00:00:00" \    
  --grid_notebook_path  /XXXX/grid/notebook_grid.f \ 
  --grid_coordinates_path /XXXX/grid/lonlat_Cotonou_20190211.nc \ 
  --grid_bathycote_path  /XXXX/grid/bathycote_in_CNES_V1.0.ijh  \ 
  --mpi_domain_path  /XXXX/grid/description_domaine_180.next \ 
  --mpi_hole_path  /XXXX/grid/description_trous_180.txt \ 
  --acadjas_mask_path  /XXXX/grid/mask_mangrove_cnes.dat \ 
  --tracers_let_out_count 24 \
  --tracers_let_out_freq BMM  \
  --meteo_forcing_path /XXXX/forcings/ecmwf/2016-2019 \
  --ocean_forcing_path /XXXX/forcings/forcings/mercator \
  --tide_forcing_path /XXXX/forcings/forcings/fes2014  \  
  --river_so_discharge_path /XXXX/forcings/forcings/rivers/Yves_R1012_6m3s/SO_academic_new.dat  \ 
  --river_oueme_discharge_path /XXXX/forcings/forcings/rivers/Yves_R1012_6m3s/OUEME_academic_new.dat \ 
  --river_djonou_discharge_path /XXXX/forcings/forcings/rivers/Yves_R1012_6m3s/DJONOU_academic_new.dat
```