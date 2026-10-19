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
from datetime import datetime, timedelta

import numpy as np
import pytz
from netCDF4 import num2date
from scipy.io import loadmat
from spatialetl.point import TimeMultiPoint
from spatialetl.point.io.multi_point_reader import MultiPointReader


class CTDProfilReader(MultiPointReader):

    PRIMARY_KEY = "CleanedData";

    def __init__(self,myFile):
        MultiPointReader.__init__(self, myFile);
        self.mat = loadmat(self.filename)
        self.profilmax = np.shape(self.mat[CTDProfilReader.PRIMARY_KEY]['LON'][0][0][0][0][0][0])[0]
        self.zmax = np.shape(self.mat[CTDProfilReader.PRIMARY_KEY]['PRES'][0][0][0][0][0][0])[0]
        self.tmax = np.shape(self.mat[CTDProfilReader.PRIMARY_KEY]['TIME'][0][0][0][0][0][0])[0]

    # Axis
    def get_z_size(self):
        return self.zmax

    def get_t_size(self):
        return self.tmax

    def read_axis_x(self):
        return self.mat[CTDProfilReader.PRIMARY_KEY]['LON'][0][0][0][0][0][0]

    def read_axis_y(self):
        return self.mat[CTDProfilReader.PRIMARY_KEY]['LAT'][0][0][0][0][0][0]

    def read_axis_z(self):
        return self.mat[CTDProfilReader.PRIMARY_KEY]['PRES'][0][0][0][0][0][0]

    def read_axis_t(self,tmin,tmax, timestamp=0):

        data = self.mat[CTDProfilReader.PRIMARY_KEY]['TIME'][0][0][0][0][0][0][tmin:tmax]

        temp = num2date(data, units="days since 01-01-01 00:00:00", calendar="julian")

        localTimeZone = pytz.timezone("Africa/Porto-Novo")
        result = [
            localTimeZone.localize(datetime.strptime(str(t), '%Y-%m-%d %H:%M:%S.%f') - timedelta(days=365)).astimezone(
                pytz.timezone("UTC")).replace(tzinfo=None) \
            for t in temp];

        if timestamp == 1:
            return [(t - TimeMultiPoint.TIME_DATUM).total_seconds() \
                    for t in result];
        else:
            return result

    def is_coverage_based(self):
        return False

    # Scalar
    def read_variable_time(self,tmin,tmax,timestamp=0):
        return self.read_axis_t(tmin,tmax,timestamp)

    def read_variable_sea_water_temperature_at_time_and_depth(self,index_t, index_z):

        data = np.empty([self.profilmax])
        data[:] = np.nan
        data[index_t] = self.mat[CTDProfilReader.PRIMARY_KEY]['TEMP'][0][0][0][0][0][index_z][index_t]

        return data

    def read_variable_sea_water_salinity_at_time_and_depth(self,index_t, index_z):

        data = np.empty([self.profilmax])
        data[:] = np.nan
        data[index_t] = self.mat[CTDProfilReader.PRIMARY_KEY]['PSAL'][0][0][0][0][0][index_z][index_t]

        return data

    def read_variable_sea_water_density_at_time_and_depth(self,index_t, index_z):

        data = np.empty([self.profilmax])
        data[:] = np.nan
        data[index_t] = self.mat[CTDProfilReader.PRIMARY_KEY]['DENS'][0][0][0][0][0][index_z][index_t]

        return data

    def read_variable_sea_water_turbidity_at_time_and_depth(self,index_t, index_z):

        data = np.empty([self.profilmax])
        data[:] = np.nan
        data[index_t] = self.mat[CTDProfilReader.PRIMARY_KEY]['TURB'][0][0][0][0][0][index_z][index_t]

        return data

    def read_variable_sea_water_electrical_conductivity_at_time_and_depth(self,index_t, index_z):

        data = np.empty([self.profilmax])
        data[:] = np.nan
        data[index_t] = self.mat[CTDProfilReader.PRIMARY_KEY]['COND'][0][0][0][0][0][index_z][index_t]*0.1 # millisiemens/centimeter to siemens/meter

        return data


