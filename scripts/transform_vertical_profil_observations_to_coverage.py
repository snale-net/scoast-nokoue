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

from spatialetl.coverage import Coverage, TimeCoverage
from spatialetl.providers.common.gdal.coverage.tiff.default_writer import DefaultWriter
from nokoue.coverage.matlab.ctd_profil_reader import CTDProfilReader as CoverageReader
from spatialetl.utils.logger import logging

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.INFO)

    # Read data from CTD Coverage reader
    reader = CoverageReader(
        [
            "/data/matlab/NOK_CTD_PROF_201712.mat",
            "/data/matlab/NOK_CTD_PROF_201801.mat",
            "/data/matlab/NOK_CTD_PROF_201802.mat",
            "/data/matlab/NOK_CTD_PROF_201803.mat",
            "/data/matlab/NOK_CTD_PROF_201804.mat",
            "/data/matlab/NOK_CTD_PROF_201805.mat",
            "/data/matlab/NOK_CTD_PROF_201806.mat",
            "/data/matlab/NOK_CTD_PROF_201807.mat",
            "/data/matlab/NOK_CTD_PROF_201808.mat",
            "/data/matlab/NOK_CTD_PROF_201809.mat",
            "/data/matlab/NOK_CTD_PROF_201810.mat",
            "/data/matlab/NOK_CTD_PROF_201811.mat",
            "/data/matlab/NOK_CTD_PROF_201812.mat"
        ],
        "/data/mask/NOK_sea_binary_mask.nc"
    )
    coverage = TimeCoverage(reader);

    writer = DefaultWriter(coverage, '/data/outputs/')
    writer.write_variable_sea_surface_salinity()
    writer.write_variable_sea_water_salinity_at_ground_level()
    writer.close()

    stop_time = time.time()
    print("----- Time ", (time.time() - start_time), " seconds -----")
    print('End of program')
