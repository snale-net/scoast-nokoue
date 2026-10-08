# MIT License
# Copyright (c) 2024 [SNALE - French SAS Company - RCS 951 724 616]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys

sys.path.insert(1, ".")

import os
import numpy as np
from nokoue.processing.atte_bathtub import nan2neginf, read_img, write_img, extract_sea_level_at_coastline, \
    fast_atte_bathtub, rasterize_land_sea_mask
from spatialetl.utils.logger import logging

if __name__ == '__main__':
    logging.setLevel(logging.RUN)

    out_dir = "/data/outputs"
    dem_file = "/data/observations/topography/DR_V3/mns_pleiades_chenal_4326.tif"
    mask_shapefile = "/data/raw-data/IGN_Masques/merged.shp"
    msl_file = "/data/modelling/bathtub/20181102_171652_ssh_msl.tiff"

    dem, proj, geotrans = read_img(dem_file, is_verbose=True)

    # Generate the land sea mask
    land_mask = rasterize_land_sea_mask(
        mask_shapefile,
        dem,
        proj,
        geotrans
    )

    write_img(f"{out_dir}/flood_nokoue_mask.tif", proj, geotrans, land_mask)

    slr_data,slr_proj,slr_geotrans = read_img(msl_file, is_verbose=True)
    slr_data = slr_data +0.5
    slr_data = np.flip(slr_data, axis=0)
    slr_data = extract_sea_level_at_coastline(slr_data,slr_geotrans,land_mask,geotrans)
    write_img(f"{out_dir}/flood_nokoue_slr.tif", proj, geotrans, slr_data)
    slr_data_b = nan2neginf(slr_data)

    #atte_factor = 0.005
    atte_factor = 0

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    out_path = f"{out_dir}/flood_nokoue_{str(atte_factor).replace('.', 'p')}.tif"

    fd = fast_atte_bathtub(dem, slr_data, land_mask, atte_factor=atte_factor)
    write_img(out_path, proj, geotrans, fd)
    logging.info(f"Finish: {out_path}")
    del fd, dem, proj, geotrans