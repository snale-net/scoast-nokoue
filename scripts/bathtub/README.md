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
docker  docker run -v /XXXX/:/dem -v /XXXX/:/config -it "scoast-nokoue:1.3" python /app/bathtub/compute_flood_extent_on_dem.py \
  --dem_path /dem/mns_pleiades_test_4326.tif  \
  --mask_path /dem/flood_nokoue_mask.tif \
  --output_folder /config/TODTF \
  --msl_folder /config/TODTF \
  --date 20181102_171652 \
  --step 0.2
```