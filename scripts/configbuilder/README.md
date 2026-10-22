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
#SBATCH --time=2-00:00:00
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
cd scripts/configbuilder

docker run -v /XXXX/grid/:/XXXX/grid  -v /XXXX/forcings/:/XXXX/forcings/  -v /XXXX/config/:/XXXX/config/ -v ${PWD}:/script -w /script -it "scoast-nokoue:1.1" python generate_ref2018.py

singularity exec --bind /work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/grid --bind /work/SCO/SCOAST/NOKOUE/RAW/forcings --bind /work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/configurations --bind ${PWD}:/script --pwd /script /work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/containers/scoast-nokoue-v1.1.sif python generate_ref2018.py 
```