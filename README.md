Package ``scoast-nokoue``


## Directory Structure


```bash
.
├── nokoue # Custom readers / writers of spatialETL for Nokoue modelling
│   ├── coverage # 2D vars
│   │   └── matlab # Matlab data format
│   │   └── shape # Shapefiles data format
│   │   └── symphonie # SYMPHONIE model format
│   ├── operator # Spatial operators : interpolators
│   └── point # Timeseries
│       ├── matlab # Matlab format
│       └── symphonie # SYMPHONIE model format
└── scripts # Main scripts
```
## Installation

Pull the spatialetl docker image

```bash
docker image pull fretif/spatialetl:beta1.2
```

## Scripts

### 1. Generate the land sea binary mask from SYMPHONIE model

`generate_land_sea_mask.py`

Transform the land sea binary mask of the reference 2018 modelling to netCDF format.
The land sea mask is useful to clip model outputs on wet areas.

### 2. Transform climat modelling to geotiff format

`symphonie_climato_to_geotiff.py`

Transform outputs of climat modelling to geotiff format.

### 3. Extract flood extent from reference 2018 modelling to shapefile format

`symphonie_ref2018_to_flood_extent.py`

Extract flood extent and flood severity classification (1=low, 2=moderate, 3=high, 4=very high) of the reference 2018 modelling to shapefile format.
Documentation on the classification can be found in the PPRL guide (https://www.ecologie.gouv.fr/sites/default/files/documents/Guide_m%C3%A9thodo_PPRL_%202014.pdf
                # Page 109) 

### 4. Transform reference 2018 modelling to geotiff format

`symphonie_ref2018_to_geotiff.py`

Transform outputs of the reference 2018 modelling to geotiff format.

### 5. Extract Reference 2018 modelling to in-situ data

`symphonie_ref2018_to_timeseries.py`

Extract data from the reference 2018 modelling at in-situ data observations and store them in netCDF format.

### 6. Transform in-situ data to netCDF format

`transform_vertical_profil_observations.py`

Transform in-situ data from Matlab to netCDF format.

### 7. Transform in-situ data to maps

`transform_vertical_profil_observations_to_coverage.py`

Transform in-situ data from Matlab to tiff format with an objective interpolation.


## How to use

```bash
docker run -v /XXXX/:/data -w /data  -v ${PWD}:/script -w /script -it "fretif/spatialetl:beta1.2" python scripts/symphonie_ref2018_to_geotiff.py  
```