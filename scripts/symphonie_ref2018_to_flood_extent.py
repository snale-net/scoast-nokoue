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

import time
from datetime import timedelta

from spatialetl.coverage import Coverage, TimeCoverage
from nokoue.coverage.shape.flood_polygon_writer import FloodingPolygonWriter as DefaultWriter
from nokoue.coverage.symphonie.ref2018_reader import SYMPHONIEReader as CoverageReader
from spatialetl.utils.logger import logging

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.INFO)

    Coverage.HORIZONTAL_INTERPOLATOR = "cgal"

    # Setting to compute a daily average
    TimeCoverage.TIME_INTERPOLATION_METHOD = "mean"
    TimeCoverage.TIME_DELTA = timedelta(hours=1.5)

    # Read SYMPHONIE data
    reader = CoverageReader('/data/grid/grid_zoom.nc',
                            '/data/modelling/symphonie/outputs/REF2018/')

    coverage = TimeCoverage(
        reader,
        resolution_x=0.0002,
        resolution_y=0.0002,
        freq="1h",
        start_time="2018-11-02 17:16:00",
        end_time="2018-11-02 17:16:00",
        nb_thread=12);

    writer = DefaultWriter(coverage, '/data/outputs')
    writer.write_variable_flood_extent()
    writer.write_variable_flood_severity()
    writer.close()

    stop_time = time.time()
    print("----- Time ", (time.time() - start_time), " seconds -----")
    print('End of program')
