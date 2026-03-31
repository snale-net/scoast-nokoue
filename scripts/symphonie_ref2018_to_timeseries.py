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

import numpy as np
from spatialetl.point import TimeMultiPoint, LevelMultiPoint, TimeLevelMultiPoint
from spatialetl.providers.common.netcdf.point.default_time_level_multi_point_reader import \
    DefaultTimeLevelMultiPointReader
from spatialetl.providers.common.netcdf.point.default_writer import DefaultWriter as DefaultWriter
from nokoue.point.symphonie.ref2018_reader import SYMPHONIEReader
from spatialetl.utils.logger import logging

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.RUN)

    # In-situ data in netCDF format
    obsFile = "/data/observations/CTD_06-2018_to_06-2018.nc"

    # SYMPHONIE model data
    modelGrid = '/data/grid_zoom.nc'
    modelData = '/data/modelling/symphonie/outputs/REF2018/'

    # Output dir
    outputDir = "/data/outputs/"
    outputFilename = "symphonie_profils_"

    # We don't interpolate in time so we set the timedelta to the SYMPHONIE output frequency
    TimeMultiPoint.TIME_DELTA = timedelta(minutes=20)

    LevelMultiPoint.DEPTH_DELTA = 0.2
    LevelMultiPoint.VERTICAL_INTERPOLATION_METHOD = "linear"

    # Read the in-situ data
    profilReader = DefaultTimeLevelMultiPointReader(obsFile)
    profil = TimeLevelMultiPoint(profilReader)

    x = profil.read_axis_x()
    y = profil.read_axis_y()
    nbPoints = profil.get_nb_points()

    stationCoords = np.zeros([nbPoints, 2])
    for i in range(0, nbPoints):
        stationCoords[i] = [x[i], y[i]]

    # Read the SYMPHONIE output
    reader = SYMPHONIEReader(
        modelGrid,
        modelData,
        stationCoords  # Give the exact same location as the observations
    )
    myPoints = TimeLevelMultiPoint(
        reader,
        zbox=[0.0, 2.0],  # Only export data from the surface to 2m depth
        resolution_z=0.2,  # Interpolate every 20 cm
        # time_range=profil.read_axis_t() # Give the exact same datetime as the observations
        start_time="2018-11-02 17:16:00",  # or use the start_time / end_time
        end_time="2018-11-02 17:16:00"
    )

    writer = DefaultWriter(myPoints, outputDir + outputFilename + str(
        myPoints.read_axis_t()[0].strftime("%m-%Y")) + '_to_' + str(
        myPoints.read_axis_t()[myPoints.get_t_size() - 1].strftime("%m-%Y")) + '.nc')

    writer.write_variable_sea_water_temperature()
    writer.write_variable_sea_water_salinity()
    writer.close()

    stop_time = time.time()
    print("----- Time ", (time.time() - start_time), " seconds -----")
    print('End of program')
