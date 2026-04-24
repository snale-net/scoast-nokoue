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

import time
from datetime import timedelta

from spatialetl.coverage import Coverage, TimeCoverage
from spatialetl.providers.common.gdal.coverage.tiff.default_writer import DefaultWriter
from spatialetl.providers.symphonie.coverage.netcdf.symphonie_eulerian_drifters_reader import SYMPHONIEEulerianDriftersReader as CoverageReader
from spatialetl.utils.logger import logging

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.RUN)

    Coverage.HORIZONTAL_INTERPOLATOR = "cgal"

    # Setting to compute residence time up to 160 days
    TimeCoverage.TIME_DELTA = timedelta(days=160)

    # Read SYMPHONIE data
    reader = CoverageReader('/data/grid/grid_zoom.nc',
                            '/data/modelling/symphonie/outputs/REF2018/EULERIAN/3/')

    coverage = TimeCoverage(
        reader,
        bbox=[2.3477, 2.57, 6.3644, 6.5100],
        resolution_x=0.0002,
        resolution_y=0.0002,
        freq="12SMS", # Select the first time of the period
        nb_thread=12);

    writer = DefaultWriter(coverage, '/data/outputs')

    writer.write_variable_sea_surface_residence_time()
    writer.write_variable_residence_time_at_ground_level()

    writer.close()

    print("----- Time ", (time.time() - start_time), " seconds -----")
    print('End of program')
