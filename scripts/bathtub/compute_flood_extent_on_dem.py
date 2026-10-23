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
import argparse
from datetime import datetime
import logging
import os

import numpy as np

from bathtub.atte_bathtub import read_img, extract_sea_level_at_coastline, \
    fast_atte_bathtub, write_flood_extent_to_parquet, write_cog, nan2neginf


def get_parser():
    """
    Argument parser for rasterization of Symphonie outputs.

    Returns:
    the parser.
    """

    parser = argparse.ArgumentParser(description=("Compute flooding from Symphonie modeling"))

    parser.add_argument(
        "-d", "--dem_path",
        type=str,
        help="Path to the dem file (tif)",
        required=True,
    )

    parser.add_argument(
        "-m", "--mask_path",
        type=str,
        help="Path to the mask file (tif)",
        required=True,
    )

    parser.add_argument(
        "--output_folder",
        type=str,
        help="Path to the folder where the results are stored (default: ./outputs)",
        default="./outputs"
    )

    parser.add_argument(
        "--date",
        type=datetime.fromisoformat,
        default=datetime.fromisoformat("2018-01-01 12:00:05"),
        help="Date time for the computation of the flooding in YYYYMMDD_hhmmss format (default: 20180101_120005)",
        required=True,
    )

    parser.add_argument(
        "--msl_folder",
        type=str,
        help="Path to the folder where the sea surface height above mean sea level results are stored (default: ./outputs)",
        default="./outputs"
    )

    parser.add_argument(
        "--export_cog",
        action="store_true",
        help="Enable exporting COG raster of flooded areas (default: False)",
    )

    parser.add_argument(
        "--step",
        type=float,
        help="Compute range of SLR elevation from the original SSH value to ssh upper bound arguments",
        default=None
    )

    parser.add_argument(
        "--slr_max",
        type=float,
        help="SLR elevation maximal value",
        default=2.0
    )

    return parser


if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

    # PARAMETERS
    parser = get_parser()
    args = parser.parse_args()

    dem_file = args.dem_path
    mask_file = args.mask_path

    time = args.date
    msl_file = os.path.join(args.msl_folder, f"{time.strftime('%Y%m%d_%H%M%S')}_ssh_msl.tiff")

    out_dir = args.output_folder
    export_cog = args.export_cog

    # BEGIN
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if not os.path.exists(dem_file):
        logging.error(f"Unable to find the DEM file {dem_file}")
        raise ValueError(f"Unable to find the DEM file {dem_file}")
    dem, proj, geotrans = read_img(dem_file, is_verbose=True)

    if not os.path.exists(mask_file):
        logging.error(f"Unable to find the land sea mask file {mask_file}")
        raise ValueError(f"Unable to find the land sea mask file {mask_file}")
    land_mask = read_img(mask_file)

    if not os.path.exists(msl_file):
        logging.error(f"Unable to find the SSH file {msl_file}")
        raise ValueError(f"Unable to find the SSH file {msl_file}")

    slr_data, slr_proj, slr_geotrans = read_img(msl_file, is_verbose=True)
    slr_data = np.flip(slr_data, axis=0)
    slr_data = extract_sea_level_at_coastline(slr_data, slr_geotrans, land_mask, geotrans)
    slr_data = nan2neginf(slr_data)
    mask = np.isfinite(slr_data)
    ref_level = np.mean(slr_data[np.isfinite(slr_data)])

    atte_factor = 0

    if  args.step == None:
        levels = [0]
    else:
        levels = np.arange(0,args.slr_max-ref_level,args.step)

    for level in levels:
        slr_data[mask] += level

        logging.info(f"Computing flood extend for {ref_level+level:.2f}m of SLR")
        fd = fast_atte_bathtub(dem, slr_data, land_mask, atte_factor=atte_factor)

        out_path = f"{out_dir}/{time.strftime('%Y%m%d_%H%M%S')}_flood_extent_{ref_level+level:.2f}m.parquet"
        write_flood_extent_to_parquet(out_path, proj, geotrans, fd)

        if export_cog:
            out_path = f"{out_dir}/{time.strftime('%Y%m%d_%H%M%S')}_flood_extent_{ref_level+level:.2f}m.tiff"
            write_cog(out_path, proj, geotrans, fd)

    logging.info(f"Finish")
    del fd, dem, proj, geotrans
