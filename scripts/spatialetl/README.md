## Scripts

### 1. Generate the land sea binary mask from SYMPHONIE model

`symphonie_land_sea_mask.py`

Transform the land sea binary mask of the reference 2018 modelling to netCDF format.
The land sea mask is useful to clip model outputs on wet areas.

### 2. Transform SYMPHONIE modelling to COG format

`symphonie_to_cog.py`

Transform outputs of SYMPHONIE modelling to Cloud Optimized Geotiff format.

`python symphonie_to_cog.py  \
    -g /XXX/grid.nc \
    -d /XXX/REF2018 \
    -o /XXX/outputs \
    --x_res 0.002 \
    --y_res 0.002 \
    --freq "daily average" \
    --start-time "2018-11-02 17:16:00" \
    --end-time "2018-11-02 17:16:00" \    
    --sea_surface_height`

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
docker run -v /XXXX/:/config -it "scoast-nokoue:1.2" python /app/spatialetl/symphonie_to_cog.py  \
    -g /XXX/grid.nc \
    -d /XXX/REF2018 \
    -o /XXX/outputs \
    --x_res 0.002 \
    --y_res 0.002 \
    --freq "daily average" \
    --start-time "2018-11-02 17:16:00" \
    --end-time "2018-11-02 17:16:00" \    
    --sea_surface_height 
```