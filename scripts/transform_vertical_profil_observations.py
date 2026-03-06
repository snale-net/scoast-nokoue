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
import os
import time

from spatialetl.point import LevelMultiPoint, TimeLevelMultiPoint
from spatialetl.providers.common.netcdf.point.default_writer import DefaultWriter
from spatialetl.utils.logger import logging

from nokoue.point.matlab.ctd_profil_reader import CTDProfilReader

if __name__ == "__main__":
    start_time = time.time()
    logging.setLevel(logging.RUN)

    LevelMultiPoint.DEPTH_DELTA = 0.05

    outputDir = "/data/observations/"

    reader = CTDProfilReader("/data/observations/NOK_CTD_PROF_201806.mat")
    profil = TimeLevelMultiPoint(reader);
    instru = "CTD"
    profil.name_station = "Vertical myGeoPoints"
    profil.data_source = instru

    writer = DefaultWriter(profil, os.path.join(outputDir, str(instru) + "_" + str(
             profil.read_variable_time()[0].strftime("%m-%Y")) + '_to_' + str(
             profil.read_variable_time()[profil.get_t_size() - 1].strftime("%m-%Y")) + '.nc'))

    writer.write_variable_sea_water_temperature()
    writer.write_variable_sea_water_salinity()
    writer.close()

    stop_time = time.time()
    print("----- Time ", (time.time() - start_time), " seconds -----")
    print('End of program')
    
    
       
        
    
    
    
    
    
