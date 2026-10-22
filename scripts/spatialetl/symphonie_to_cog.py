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
from datetime import timedelta, datetime

import time

from spatialetl.coverage import Coverage, TimeCoverage
from spatialetl.providers.common.gdal.coverage.tiff.cog_writer import COGWriter
from spatialetl.providers.symphonie.coverage.netcdf.symphonie_reader import SYMPHONIEReader as CoverageReader
from spatialetl.utils.logger import logging


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--resolution-x",
        type=float,
        default=0.0002,
        help="Target longitude resolution (default : 0.0002)",
    )
    parser.add_argument(
        "--resolution-y",
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
        help="Date de début (format : YYYY-MM-DD HH:MM:SS)",
    )
    parser.add_argument(
        "--end-time",
        type=datetime.fromisoformat,
        default=datetime.fromisoformat("2019-01-01 00:00:00"),
        help="Date de fin (format : YYYY-MM-DD HH:MM:SS)",
    )

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
    reader = CoverageReader('/config/OFFLINE/grid.nc',
                            '/config/GRAPHIQUES')

    coverage = TimeCoverage(
        reader,
        resolution_x=args.resolution_x,
        resolution_y=args.resolution_y,
        freq=freq,
        start_time=args.start_time,
        end_time=args.end_time,
        nb_thread=12);

    writer = COGWriter(coverage, '/config/TODTF/')

    writer.write_variable_sea_surface_height_above_mean_sea_level()
    writer.write_variable_sea_surface_salinity()
    writer.write_variable_sea_water_salinity_at_ground_level()
    writer.close()

    stop_time = time.time()
    logging.info(f"----- Time {time.time() - start_time} seconds -----")
    logging.info('End of program')
