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
import os
import time

from spatialetl.coverage import TimeCoverage
from spatialetl.providers.common.gdal.coverage.tiff.cog_writer import COGWriter
from spatialetl.providers.nokoue.coverage.matlab.ctd_profil_reader import CTDProfilReader as CoverageReader
from spatialetl.utils.logger import logging

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input_path",
        type=str,
        action="append",
        help="Path to the observations MATLAB file",
        required=True
    )

    parser.add_argument(
        "-m", "--mask_path",
        type=str,
        help="Path to the mask file (NetCDF format)",
        required=True,
    )

    parser.add_argument(
        "-o", "--output_folder",
        type=str,
        help="Path to the folder where the results are stored (default: ./outputs)",
        default="./outputs"
    )

    parser.add_argument("--sea_surface_salinity", required=False, action="store_true", help="Compute sea surface salinity")

    parser.add_argument("--sea_ground_salinity", required=False, action="store_true", help="Compute sea water salinity at ground level")

    return parser.parse_args()

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.RUN)

    args = parse_args()

    # Read data from CTD Coverage reader
    reader = CoverageReader(
        args.input_path,
        args.mask_path
    )
    coverage = TimeCoverage(reader);

    os.makedirs(args.output_folder, exist_ok=True)
    writer = COGWriter(coverage, args.output_folder)

    if args.sea_surface_salinity:
        writer.write_variable_sea_surface_salinity()
    if args.sea_ground_salinity:
        writer.write_variable_sea_water_salinity_at_ground_level()
    writer.close()

    stop_time = time.time()
    logging.info(f"----- Time {time.time() - start_time} seconds -----")
    logging.info('End of program')
