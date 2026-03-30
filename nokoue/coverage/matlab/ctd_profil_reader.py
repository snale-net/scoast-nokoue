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
from __future__ import division, print_function, absolute_import

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytz
from netCDF4 import num2date, Dataset
from scipy.interpolate import NearestNDInterpolator
from scipy.io import loadmat
from spatialetl.coverage.io.coverage_reader import CoverageReader
from spatialetl.coverage.time_coverage import TimeCoverage
from spatialetl.utils.logger import logging

from nokoue.operator.interpolator import objective_analysis


class CTDProfilReader(CoverageReader):
    PRIMARY_KEY = "CleanedData";

    def __init__(self, myFile, myMask, bbox=None, resolution_x=None, resolution_y=None):
        CoverageReader.__init__(self, myMask);

        self.files = []
        self.times = []

        for file in myFile:
            if not os.path.exists(file):
                logging.warning(f"{file} doesn't exists. We skip it")
            else:

                # The measurements duration is usually few days with one time per measurement.
                # In this reader, we decided to merge all these measurements to a unique map so we calculate the mean of the measurement duration.
                self.mat = loadmat(file)
                data = self.mat[CTDProfilReader.PRIMARY_KEY]['TIME'][0][0][0][0][0][0]
                temp = num2date(data, units="days since 01-01-01 00:00:00", calendar="julian")

                dates = []
                localTimeZone = pytz.timezone("Africa/Porto-Novo")
                for dd in temp:
                    try:
                        ddl = datetime.strptime(str(dd), '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        ddl = datetime.strptime(str(dd), '%Y-%m-%d %H:%M:%S')
                    finally:
                        final = localTimeZone.localize(
                            ddl - timedelta(days=365)).astimezone(
                            pytz.timezone("UTC")).replace(tzinfo=None)
                        dates.append(final)

                # We compute the mean of the measurement times.
                x = np.array([np.datetime64(t) for t in dates])
                try:
                    current_time = datetime.strptime(str(np.mean(x.astype(int)).astype(x.dtype)),
                                                     '%Y-%m-%dT%H:%M:%S.%f')
                except ValueError:
                    current_time = datetime.strptime(str(np.mean(x.astype(int)).astype(x.dtype)),
                                                     '%Y-%m-%dT%H:%M:%S')

                self.times.append(current_time)
                self.files.append(file)

        if len(self.times) == 0:
            raise ValueError("No time records found")

        self.t_size = len(self.files)

        # We open the first file
        self.last_opened_t_index = 0
        self.open_file(self.last_opened_t_index)

        # We load land sea mask
        nc_mask = Dataset(self.filename, 'r')
        self.Xx = nc_mask.variables['longitude'][:]
        self.Yy = nc_mask.variables['latitude'][:]
        self.mask = nc_mask.variables['sea_mask'][:]
        is_mask_to_resample = False

        if bbox is not None and resolution_x is not None and resolution_y is not None:
            is_mask_to_resample = True
            ymin = bbox[2]
            ymax = bbox[3]
            xmin = bbox[0]
            xmax = bbox[1]
            self.Xx = np.arange(xmin, xmax, resolution_x)
            self.Yy = np.arange(ymin, ymax, resolution_y)
        elif bbox is not None and resolution_x is None and resolution_y is None:
            is_mask_to_resample = True
            ymin = bbox[2]
            ymax = bbox[3]
            xmin = bbox[0]
            xmax = bbox[1]
            self.Xx = np.linspace(xmin, xmax)
            self.Yy = np.linspace(ymin, ymax)
        elif bbox is None and resolution_x is not None and resolution_y is not None:
            is_mask_to_resample = True
            x = self.mat[CTDProfilReader.PRIMARY_KEY]['LON'][0][0][0][0][0][0]
            y = self.mat[CTDProfilReader.PRIMARY_KEY]['LAT'][0][0][0][0][0][0]
            self.Xx = np.arange(min(x), max(x), resolution_x)
            self.Yy = np.arange(min(y), max(y), resolution_y)

        if is_mask_to_resample:
            # If needed, we interpole the land sea mask on the destination grid
            logging.info("[CTProfilReader] Interpolate sea binary mask")
            src_grid_x, src_grid_y = np.meshgrid(nc_mask.variables['longitude'][:], nc_mask.variables['latitude'][:])
            points = np.array([src_grid_x.flatten(), src_grid_y.flatten()]).T
            interp = NearestNDInterpolator(points, nc_mask.variables['sea_mask'][:].flatten())
            dst_local_grid_x, dst_local_grid_y = np.meshgrid(self.Xx, self.Yy)
            self.mask = interp((dst_local_grid_x, dst_local_grid_y))

    def open_file(self, index_t):

        if len(self.files) == 1 and index_t > 0:
            return

        if index_t != self.last_opened_t_index:
            self.mat = loadmat(self.files[index_t])

    def close(self):
        return

    def is_regular_grid(self):
        return True

    def get_x_size(self):
        return np.shape(self.Xx)[0];

    def get_y_size(self):
        return np.shape(self.Yy)[0];

    def get_z_size(self):
        return np.shape(self.mat[CTDProfilReader.PRIMARY_KEY]['PRES'][0][0][0][0][0][0])[0]

    def get_t_size(self):
        return self.t_size

    def read_axis_x(self, xmin, xmax, ymin, ymax):
        return self.Xx[xmin:xmax]

    def read_axis_y(self, xmin, xmax, ymin, ymax):
        return self.Yy[ymin:ymax]

    def read_axis_z(self, zmin, zmax):
        return self.mat[CTDProfilReader.PRIMARY_KEY]['PRES'][0][0][0][0][0][0][zmin:zmax]

    def read_axis_t(self, tmin, tmax, timestamp):

        if timestamp == 1:
            return [(t - TimeCoverage.TIME_DATUM).total_seconds() \
                    for t in self.times[tmin:tmax]];
        else:
            return self.times[tmin:tmax]

    # Variables
    def read_variable_longitude(self, xmin, xmax, ymin, ymax):
        return self.read_axis_x(xmin, xmax, ymin, ymax)

    def read_variable_latitude(self, xmin, xmax, ymin, ymax):
        return self.read_axis_y(xmin, xmax, ymin, ymax)

    def read_variable_time(self, tmin, tmax):
        return self.read_axis_t(tmin, tmax, timestamp=0)

    def read_variable_sea_surface_salinity_at_time(self, index_t, xmin, xmax, ymin, ymax):

        self.open_file(index_t)

        x = self.mat[CTDProfilReader.PRIMARY_KEY]['LON'][0][0][0][0][0][0]
        y = self.mat[CTDProfilReader.PRIMARY_KEY]['LAT'][0][0][0][0][0][0]

        # Select the first valid value on each vertical profils
        idx = pd.DataFrame(self.mat[CTDProfilReader.PRIMARY_KEY]['PSAL'][0][0][0][0][0]).apply(
            pd.Series.first_valid_index)
        arr = self.mat[CTDProfilReader.PRIMARY_KEY]['PSAL'][0][0][0][0][0]
        data = arr[idx, np.arange(len(idx))]

        large_scale = 2;
        small_scale = 0.1;
        z, _ = objective_analysis(x, y, data, self.Xx, self.Yy, large_scale, small_scale)

        # Apply land sea mask
        z[self.mask != 1] = np.nan

        return z[ymin:ymax, xmin:xmax]

    def read_variable_sea_water_salinity_at_ground_level_at_time(self, index_t, xmin, xmax, ymin, ymax):

        self.open_file(index_t)

        x = self.mat[CTDProfilReader.PRIMARY_KEY]['LON'][0][0][0][0][0][0]
        y = self.mat[CTDProfilReader.PRIMARY_KEY]['LAT'][0][0][0][0][0][0]

        # Select the last valid value on each vertical profils
        idx = pd.DataFrame(self.mat[CTDProfilReader.PRIMARY_KEY]['PSAL'][0][0][0][0][0]).apply(
            pd.Series.last_valid_index)
        arr = self.mat[CTDProfilReader.PRIMARY_KEY]['PSAL'][0][0][0][0][0]
        data = arr[idx, np.arange(len(idx))]

        large_scale = 2;
        small_scale = 0.1;
        z, _ = objective_analysis(x, y, data, self.Xx, self.Yy, large_scale, small_scale)

        # Apply land sea mask
        z[self.mask != 1] = np.nan

        return z[ymin:ymax, xmin:xmax]
