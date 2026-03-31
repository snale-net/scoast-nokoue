#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
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
from spatialetl.coverage import Coverage, TimeCoverage, TimeLevelCoverage
from spatialetl.providers.common.netcdf.coverage.default_writer import DefaultWriter
from spatialetl.utils.logger import logging

from nokoue.coverage.symphonie.ref2018_reader import SYMPHONIEReader as CoverageReader

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.RUN)

    Coverage.HORIZONTAL_INTERPOLATOR = "cgal"

    reader = CoverageReader('/data/Nokoue-2019/grid/grid_zoom.nc',
                            '/data/Nokoue-2019/modelling/symphonie/outputs/REF2018/')

    coverage = Coverage(
        reader,
        bbox=[2.3477, 2.5509, 6.3644, 6.5100],
        resolution_x=0.0002,
        resolution_y=0.0002,
        nb_thread=12);

    writer = DefaultWriter(coverage,
                           '/data/outputs/NOK_sea_binary_mask.nc')
    writer.write_variable_2D_sea_binary_mask()
    writer.close()

    stop_time = time.time()
    print("----- Time ", (time.time() - start_time), " seconds -----")
    print('End of program')
