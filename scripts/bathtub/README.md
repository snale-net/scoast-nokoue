## Input files

All example data can be found on TREX : 
`/work/SCO/SCOAST/NOKOUE/PROCESSING/BATHTUB`

The DEM have to use the CRS:4326 and the TIF format.
The MNS_PHR converted to CRS:4326 can be found here : `/work/SCO/SCOAST/NOKOUE/PROCESSING/BATHTUB/MNS_PHR_20241202_4326.tif`

## Scripts

### 1. Rasterize the land sea mask polygon on the DEM raster

`rasterize_land_sea_mask.py`

The land sea mask polygon can be found here `/work/SCO/SCOAST/NOKOUE/PROCESSING/BATHTUB/merged.shp`

### 2. Compute flood extent on the DEM raster from SYMPHONIE Mean Sea Level output

`compute_flood_extent_on_dem.py`

The land see mask polygon rasterized on the DEM can be found here : `/work/SCO/SCOAST/NOKOUE/PROCESSING/BATHTUB/flood_nokoue_mask.tif`

## How to use

```bash
cd scripts/bathtub
docker  docker run -v /XXXX/:/dem -v /XXXX/:/config -v ${PWD}:/script -w /script -it "scoast-nokoue:1.0" python compute_flood_extent_on_dem.py
```