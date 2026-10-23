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
from datetime import timedelta, datetime

import time

from spatialetl.coverage import Coverage, TimeCoverage
from spatialetl.providers.common.gdal.coverage.tiff.cog_writer import COGWriter
from spatialetl.providers.symphonie.coverage.netcdf.symphonie_reader import SYMPHONIEReader as CoverageReader
from spatialetl.utils.logger import logging


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-g", "--grid_path",
        type=str,
        help="Path to the grid file",
        required=True,
        default="/config/OFFLINE/grid.nc"
    )

    parser.add_argument(
        "-d", "--graphique_folder",
        type=str,
        help="Path to the graphique folder",
        required=True,
        default="/config/GRAPHIQUES"
    )

    parser.add_argument(
        "--x_res",
        type=float,
        default=0.0002,
        help="Target longitude resolution (default : 0.0002)",
    )
    parser.add_argument(
        "--y_res",
        type=float,
        default=0.0002,
        help="Target latitude resolution (défault : 0.0002)",
    )
    parser.add_argument(
        "--freq",
        type=str,
        choices=["daily average","1d"],
        default="daily average",
        help="Target temporal frequency (défault : daily average)",
    )

    parser.add_argument(
        "--start-time",
        type=datetime.fromisoformat,
        default=datetime.fromisoformat("2018-01-01 00:00:00"),
        help="Start datetime (format : YYYY-MM-DD HH:MM:SS)",
    )
    parser.add_argument(
        "--end-time",
        type=datetime.fromisoformat,
        default=datetime.fromisoformat("2019-01-01 00:00:00"),
        help="End datetime (format : YYYY-MM-DD HH:MM:SS)",
    )

    parser.add_argument(
        "-o", "--output_folder",
        type=str,
        help="Path to the folder where the results are stored (default: ./outputs)",
        default="./outputs"
    )

    parser.add_argument("--sea_surface_height", "-ssh", required=False, action="store_true", help="Compute sea surface height above mean sea level")

    parser.add_argument("--sea_surface_salinity", required=False, action="store_true", help="Compute sea surface salinity")

    parser.add_argument("--sea_ground_salinity", required=False, action="store_true", help="Compute sea water salinity at ground level")

    return parser.parse_args()

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.RUN)

    args = parse_args()

    Coverage.HORIZONTAL_INTERPOLATOR = "cgal"

    if args.freq == "daily average":
        # Setting to compute a daily average
        TimeCoverage.TIME_INTERPOLATION_METHOD = "mean"
        TimeCoverage.TIME_DELTA = timedelta(days=1)
        freq="1d"
    else:
        TimeCoverage.TIME_DELTA = timedelta(hours=5)
        freq=args.freq

    # Read SYMPHONIE data
    reader = CoverageReader(args.grid_path, args.graphique_folder)

    coverage = TimeCoverage(
        reader,
        resolution_x=args.x_res,
        resolution_y=args.y_res,
        freq=freq,
        start_time=args.start_time,
        end_time=args.end_time,
        nb_thread=12);

    os.makedirs(args.output_folder, exist_ok=True)
    writer = COGWriter(coverage, args.output_folder)

    if args.sea_surface_height:
        writer.write_variable_sea_surface_height_above_mean_sea_level()
    if args.sea_surface_salinity:
        writer.write_variable_sea_surface_salinity()
    if args.sea_ground_salinity:
        writer.write_variable_sea_water_salinity_at_ground_level()

    writer.close()

    stop_time = time.time()
    logging.info(f"----- Time {time.time() - start_time} seconds -----")
    logging.info('End of program')
