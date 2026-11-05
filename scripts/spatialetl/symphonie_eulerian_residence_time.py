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
from datetime import datetime
from datetime import timedelta

import numpy as np
import time
from dateutil.relativedelta import relativedelta

from spatialetl.coverage import Coverage, TimeCoverage
from spatialetl.providers.common.gdal.coverage.tiff.cog_writer import COGWriter
from spatialetl.providers.symphonie.coverage.netcdf.symphonie_eulerian_tracers_reader import \
    SYMPHONIEEulerianTracersReader as CoverageReader
from spatialetl.utils.logger import logging


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-g", "--grid_path",
        type=str,
        help="Path to the grid file (default: /config/OFFLINE/grid.nc)",
        required=True,
        default="/config/OFFLINE/grid.nc"
    )

    parser.add_argument(
        "-d", "--graphique_folder",
        type=str,
        help="Path to the graphique folder (default: /config/GRAPHIQUES)",
        required=True,
        default="/config/GRAPHIQUES"
    )

    parser.add_argument(
        "--let_out_count",
        type=int,
        default=24,
        help="Number of tracers let out (défault : 24)",
    )

    parser.add_argument(
        "--let_out_freq",
        type=str,
        choices=["BOM","MOM", "BMM"],
        default="BMM",
        help=(
            "Tracers let ou frequency: "
            "BOM (Beginning Of Month), "
            "MOM (Middle Of Month), "
            "BMM (Beginning and Middle of Month)."
            "(default : BMM)"
        )
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
        "--max_duration",
        type=int,
        default=160,
        help="Maximum duration of residence time in days (défault : 160)",
    )

    parser.add_argument(
        "-o", "--output_folder",
        type=str,
        help="Path to the folder where the results are stored (default: /config/TODTF)",
        default="/config/TODTF"
    )

    parser.add_argument("--sea_surface_residence_time", required=False, action="store_true", help="Compute sea surface residence time")

    parser.add_argument("--sea_ground_residence_time", required=False, action="store_true", help="Compute sea residence time at ground level")

    return parser.parse_args()

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.RUN)

    args = parse_args()

    Coverage.HORIZONTAL_INTERPOLATOR = "cgal"

    # Setting to compute residence time up to {args.max_duration} days
    TimeCoverage.TIME_DELTA = timedelta(days=args.max_duration)

    # Create output dir
    os.makedirs(args.output_folder, exist_ok=True)

    # Read SYMPHONIE data
    reader = CoverageReader(args.grid_path,
                            os.path.join(args.graphique_folder, "*ECO3M-S*"))

    # Get the start time of the simulation
    cf_start_time = np.min(reader.times)
    start_time = datetime(
        cf_start_time.year,
        cf_start_time.month,
        cf_start_time.day,
        cf_start_time.hour,
        cf_start_time.minute,
        cf_start_time.second,
        cf_start_time.microsecond
    )

    # Compute date and index of tracers let out from the start time
    dates = []
    for i in range(args.let_out_count):
        if args.let_out_freq == "BOM":
            date = start_time.replace(day=1) + relativedelta(months=i)
        elif args.let_out_freq == "MOM":
            date = start_time.replace(day=15) + relativedelta(months=i)
        elif args.let_out_freq == "BMM":
            date = start_time + relativedelta(
                months=i // 2,
                days=14 * (i % 2)
            )
        dates.append(date)

    date_tracers_map = {date: i + 1 for i, date in enumerate(dates)}

    # For each let out, compute the residence time
    for date, tracer_index in date_tracers_map.items():

        reader.set_tracer_index(tracer_index)

        coverage = TimeCoverage(
            reader,
            bbox=[2.3477, 2.57, 6.3644, 6.5100],
            resolution_x=args.x_res,
            resolution_y=args.y_res,
            start_time=date,
            end_time=date,
            nb_thread=12)

        writer = COGWriter(coverage, args.output_folder)

        if args.sea_surface_residence_time:
            writer.write_variable_sea_surface_residence_time()
        if args.sea_ground_residence_time:
            writer.write_variable_residence_time_at_ground_level()

        writer.close()

    logging.info(f"----- Time {time.time() - start_time} seconds -----")
    logging.info('End of program')
