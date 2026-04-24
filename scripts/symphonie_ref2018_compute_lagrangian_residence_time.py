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

from netCDF4 import Dataset
from spatialetl.coverage import Coverage, TimeCoverage
from spatialetl.coverage.io.multi_point_reader import MultiPointReader as MultiPointCovReader
from spatialetl.point import TimeMultiPoint
from spatialetl.providers.common.gdal.coverage.tiff.default_writer import DefaultWriter
from spatialetl.providers.symphonie.point.netcdf.symphonie_lagrangian_drifters_reader import \
    SYMPHONIELagrangianDriftersReader as MultiPointReader
from spatialetl.utils.logger import logging

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.RUN)

    # Setting to compute residence time up to 160 days
    TimeMultiPoint.TIME_DELTA = timedelta(days=160)

    # Read SYMPHONIE drifters data
    reader = MultiPointReader('/data/modelling/symphonie/outputs/REF2018/DRIFTER_OUPUT/Drifter_1erOct',)

    drifters = TimeMultiPoint(
        reader,
        freq="12SMS",  # Select the first time of the period
    )

    # We load land sea mask
    nc_mask = Dataset("/data/grid/NOK_sea_binary_mask.nc", 'r')

    # Make a CoverageReader from MultiPoint (=> 2d interpolation)
    cov_reader = MultiPointCovReader(
        points=drifters,
        resolution_x=0.0002,
        resolution_y=0.0002,
        mask_axis_x=nc_mask.variables['longitude'][:],
        mask_axis_y=nc_mask.variables['latitude'][:],
        mask_values=nc_mask.variables['sea_mask'][:]
    )

    coverage = TimeCoverage(cov_reader)
    writer = DefaultWriter(coverage,'/data/outputs')

    writer.write_variable_ocean_tracer_residence_time()
    writer.close()

    print("----- Time ", (time.time() - start_time), " seconds -----")
    print('End of program')
