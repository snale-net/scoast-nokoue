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
import logging

from bathtub.atte_bathtub import read_img, write_img, rasterize_land_sea_mask

if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

    dem_file = "/dem/MNS_PHR_20241202_4326.tif"
    mask_shapefile = "/dem/merged.shp"
    out_maskfile = "/dem/flood_nokoue_mask.tif"

    dem, proj, geotrans = read_img(dem_file, is_verbose=True)

    # Generate the land sea mask
    land_mask = rasterize_land_sea_mask(
        mask_shapefile,
        dem,
        proj,
        geotrans
    )

    write_img(out_maskfile, proj, geotrans, land_mask)
    logging.info(f"Finish: {out_maskfile}")
    del dem, proj, geotrans