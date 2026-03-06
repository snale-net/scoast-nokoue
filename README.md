Package ``scoast-nokoue``


## Directory Structure


```bash
.
├── nokoue # Custom readers / writers of spatialETL for Nokoue modelling
│   ├── coverage # 2D vars
│   │   └── symphonie # SYMPHONIE model format
│   └── point # Timeseries
│       ├── matlab # Matlab format
│       └── symphonie # SYMPHONIE model format
└── scripts # Main scripts
```
## Installation

Pull the spatialetl docker image

```bash
docker image pull fretif/spatialetl:beta1
```

## Scripts

### 1. Transform reference 2018 modelling to geotiff format

`symphonie_ref2018_to_geotiff.py`

Transform output of the reference 2018 modelling to geotiff format.

### 2. Extract Reference 2018 modelling to in-situ data

`symphonie_ref2018_to_timeseries.py`

Extract data from the reference 2018 modelling at in-situ data observations and store them in netCDF format.

### 3. Transform in-situ data to netCDF format

`transform_vertical_profil_observations.py`

Transform in-situ data from Matlab to netCDF format


## How to use

```bash
docker run -v /XXXX/:/data -w /data  -v ${PWD}:/script -w /script -it "fretif/spatialetl:beta1" python scripts/symphonie_ref2018_to_geotiff.py  
```