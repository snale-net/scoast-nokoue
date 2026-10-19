## Scripts

### 1. Generate the land sea binary mask from SYMPHONIE model

`symphonie_land_sea_mask.py`

Transform the land sea binary mask of the reference 2018 modelling to netCDF format.
The land sea mask is useful to clip model outputs on wet areas.

### 2. Transform SYMPHONIE modelling to geotiff format

`symphonie_to_geotiff.py`

Transform outputs of SYMPHONIE modelling to geotiff format.

### 3. Extract SYMPHONIE modelling to in-situ data

`symphonie_to_timeseries.py`

Extract data from the SYMPHONIE modelling at in-situ data observations and store them in netCDF format.

### 4. Transform in-situ data to maps

`observations_to_coverage.py`

Transform in-situ data from Matlab to tiff format with an objective interpolation.

### 5. Compute residence time from Eulerian tracers

`symphonie_eulerian_residence_time.py`

Compute the residence time of water from Eulerian tracers.

### 6. Compute residence time from Lagrangian tracers

`symphonie_lagrangian_residence_time.py`

Compute the residence time of water from Lagangrian tracers.

## How to use

```bash
docker run -v /XXXX/:/config -v ${PWD}:/script -w /script -it "scoast-nokoue:1.0" python scripts/symphonie_to_geotiff.py  
```