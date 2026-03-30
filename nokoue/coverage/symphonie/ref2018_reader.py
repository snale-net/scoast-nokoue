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

import numpy as np
from spatialetl.exception.variable_name_error import VariableNameError
from spatialetl.providers.symphonie.coverage.netcdf.symphonie_reader import SYMPHONIEReader as GenericReader
from spatialetl.utils.logger import logging
from spatialetl.utils.variable_definition import VariableDefinition


class SYMPHONIEReader(GenericReader):
    """
    The reference 2018 was compressed by NCO tool by storing values as short.
    The fillvalue wans't proprely handled so we can't use the fillvalue stored in the netCDF file.
    We use the wetmask variable to fill missing values
    """

    def __init__(self, myGrid, myFile):
        GenericReader.__init__(self, myGrid, myFile);

    def read_variable_2D_wet_binary_mask_at_time(self, index_t, xmin, xmax, ymin, ymax):
        try:
            self.open_file(index_t)
            if "wetmask_t" in self.ncfile.variables:
                self.ncfile.variables["wetmask_t"].set_auto_mask(False)
                data = np.ma.filled(self.ncfile.variables["wetmask_t"][0, ymin:ymax, xmin:xmax].astype(int),
                                    fill_value=-9999)
                data[self.ncfile.variables["wetmask_t"][0, ymin:ymax, xmin:xmax] != 1] = -9999
            else:
                logging.debug(
                    "No variables found for '" + str(VariableDefinition.LONG_NAME['wet_binary_mask']) + "'")
                raise (VariableNameError("SymphonieReader",
                                         "No variables found for '" + str(
                                             VariableDefinition.LONG_NAME['wet_binary_mask']) + "'",
                                         1000))

            return data

        except Exception as ex:
            logging.debug("Error '" + str(ex) + "'")
            raise (VariableNameError("SymphonieReader", "An error occured : '" + str(ex) + "'", 1000))

    def read_variable_sea_surface_height_above_mean_sea_level_at_time(self, index_t, xmin, xmax, ymin, ymax):
        try:
            self.open_file(index_t)

            if "ssh_w" in self.ncfile.variables:
                self.ncfile.variables["ssh_w"].set_auto_mask(False)
                data = np.ma.filled(self.ncfile.variables["ssh_w"][0, ymin:ymax, xmin:xmax], fill_value=np.nan)
            else:
                logging.debug("No variables found for '" + str(
                    VariableDefinition.LONG_NAME['sea_surface_height_above_mean_sea_level']) + "'")
                raise (VariableNameError("SymphonieReader",
                                         "No variables found for '" + str(
                                             VariableDefinition.LONG_NAME[
                                                 'sea_surface_height_above_mean_sea_level']) + "'",
                                         1000))

            if "wetmask_t" in self.ncfile.variables:  # We apply the wetmask
                data[self.ncfile.variables["wetmask_t"][0, ymin:ymax, xmin:xmax] != 1] = np.nan

            return data

        except Exception as ex:
            logging.debug("Error '" + str(ex) + "'")
            raise (VariableNameError("SymphonieReader", "An error occured : '" + str(ex) + "'", 1000))

    def read_variable_sea_water_column_thickness_at_time(self, index_t, xmin, xmax, ymin, ymax):
        try:
            self.open_file(index_t)
            bathy = self.grid.variables["hm_w"][ymin:ymax, xmin:xmax]
            if "hssh" in self.ncfile.variables:
                self.ncfile.variables["hssh"].set_auto_mask(False)
                data = np.ma.filled(self.ncfile.variables["hssh"][0, ymin:ymax, xmin:xmax], fill_value=np.nan)
            elif "ssh_w" in self.ncfile.variables:
                self.ncfile.variables["ssh_w"].set_auto_mask(False)
                data = np.ma.filled(self.ncfile.variables["ssh_w"][0, ymin:ymax, xmin:xmax] + bathy, fill_value=np.nan)
            elif "ssh" in self.ncfile.variables:
                self.ncfile.variables["ssh"].set_auto_mask(False)
                data = np.ma.filled(self.ncfile.variables["ssh"][0, ymin:ymax, xmin:xmax] + bathy, fill_value=np.nan)
            elif "ssh_inst" in self.ncfile.variables:
                self.ncfile.variables["ssh_inst"].set_auto_mask(False)
                data = np.ma.filled(self.ncfile.variables["ssh_inst"][0, ymin:ymax, xmin:xmax] + bathy,
                                    fill_value=np.nan)
            else:
                logging.debug("No variables found for '" + str(
                    VariableDefinition.LONG_NAME['sea_water_column_thickness']) + "'")
                raise (VariableNameError("SymphonieReader",
                                         "No variables found for '" + str(
                                             VariableDefinition.LONG_NAME['sea_water_column_thickness']) + "'",
                                         1000))

            if "wetmask_t" in self.ncfile.variables:  # We apply the wetmask
                data[self.ncfile.variables["wetmask_t"][0, ymin:ymax, xmin:xmax] == 0] = np.nan

            data[data < 0.1] = 0  # Remove values on topo
            return data

        except Exception as ex:
            logging.debug("Error '" + str(ex) + "'")
            raise (VariableNameError("SymphonieReader", "An error occured : '" + str(ex) + "'", 1000))

    def read_variable_barotropic_sea_water_velocity_at_time(self, index_t, xmin, xmax, ymin, ymax):
        try:
            self.open_file(index_t)
            index_z = self.get_z_size() - 1
            xmin_overlap, xmax_overlap, ymin_overlap, ymax_overlap, new_xmin, new_xmax, new_ymin, new_ymax = self.compute_overlap_indexes(
                xmin, xmax, ymin, ymax)

            mask_t = self.grid.variables["mask_t"][index_z, ymin_overlap:ymax_overlap, xmin_overlap:xmax_overlap];
            mask_u = self.grid.variables["mask_u"][index_z, ymin_overlap:ymax_overlap, xmin_overlap:xmax_overlap];
            mask_v = self.grid.variables["mask_v"][index_z, ymin_overlap:ymax_overlap, xmin_overlap:xmax_overlap];

            if self.gridrotcos_t is None and self.gridrotsin_t is None:
                self.compute_rot()

            rotcos = self.gridrotcos_t[ymin_overlap:ymax_overlap, xmin_overlap:xmax_overlap];
            rotsin = self.gridrotsin_t[ymin_overlap:ymax_overlap, xmin_overlap:xmax_overlap];

            if "velbar_u" in self.ncfile.variables and "velbar_v" in self.ncfile.variables:
                self.ncfile.variables["velbar_u"].set_auto_mask(False)
                data_u = np.ma.filled(
                    self.ncfile.variables["velbar_u"][0, ymin_overlap:ymax_overlap, xmin_overlap:xmax_overlap],
                    fill_value=np.nan)
                self.ncfile.variables["velbar_v"].set_auto_mask(False)
                data_v = np.ma.filled(
                    self.ncfile.variables["velbar_v"][0, ymin_overlap:ymax_overlap, xmin_overlap:xmax_overlap],
                    fill_value=np.nan)
            else:
                logging.debug("No variables found for 'Barotropic Sea Water Velocity'")
                raise (VariableNameError("SymphonieReader",
                                         "No variables found for 'Barotropic Sea Water Velocity'",
                                         1000))

            u_rot, v_rot = self.compute_vector_rotation(data_u, data_v, rotcos, rotsin, mask_t, mask_u, mask_v)

            if "wetmask_t" in self.ncfile.variables:  # We apply the wetmask
                u_rot[self.ncfile.variables["wetmask_t"][0, ymin_overlap:ymax_overlap,
                xmin_overlap:xmax_overlap] == 0] = np.nan
                v_rot[self.ncfile.variables["wetmask_t"][0, ymin_overlap:ymax_overlap,
                xmin_overlap:xmax_overlap] == 0] = np.nan

            return [u_rot[new_ymin:new_ymax, new_xmin:new_xmax], v_rot[new_ymin:new_ymax, new_xmin:new_xmax]]

        except Exception as ex:
            logging.debug("Error '" + str(ex) + "'")
            raise (VariableNameError("SymphonieReader", "An error occured : '" + str(ex) + "'", 1000))

    def read_variable_sea_surface_salinity_at_time(self, index_t, xmin, xmax, ymin, ymax):
        try:
            self.open_file(index_t)
            index_z = self.get_z_size() - 1
            if "sal" in self.ncfile.variables:
                self.ncfile.variables["sal"].set_auto_mask(False)
                data = np.ma.filled(self.ncfile.variables["sal"][0, index_z, ymin:ymax, xmin:xmax],
                                    fill_value=np.nan)
            else:
                logging.debug("No variables found for '" + str(
                    VariableDefinition.LONG_NAME['sea_surface_salinity']) + "'")
                raise (VariableNameError("SymphonieReader",
                                         "No variables found for '" + str(
                                             VariableDefinition.LONG_NAME['sea_surface_salinity']) + "'",
                                         1000))

            if "wetmask_t" in self.ncfile.variables:  # We apply the wetmask
                data[self.ncfile.variables["wetmask_t"][0, ymin:ymax, xmin:xmax] != 1] = np.nan

            return data

        except Exception as ex:
            logging.debug("Error '" + str(ex) + "'")
            raise (VariableNameError("SymphonieReader", "An error occured : '" + str(ex) + "'", 1000))

    def read_variable_sea_water_salinity_at_ground_level_at_time(self, index_t, xmin, xmax, ymin, ymax):
        try:
            self.open_file(index_t)
            index_z = 0
            if "sal" in self.ncfile.variables:
                self.ncfile.variables["sal"].set_auto_mask(False)
                data = np.ma.filled(self.ncfile.variables["sal"][0, index_z, ymin:ymax, xmin:xmax],
                                    fill_value=np.nan)
            else:
                logging.debug("No variables found for '" + str(
                    VariableDefinition.LONG_NAME['sea_water_salinity_at_ground_level']) + "'")
                raise (VariableNameError("SymphonieReader",
                                         "No variables found for '" + str(
                                             VariableDefinition.LONG_NAME['sea_water_salinity_at_ground_level']) + "'",
                                         1000))

            if "wetmask_t" in self.ncfile.variables:  # We apply the wetmask
                data[self.ncfile.variables["wetmask_t"][0, ymin:ymax, xmin:xmax] != 1] = np.nan

            return data

        except Exception as ex:
            logging.debug("Error '" + str(ex) + "'")
            raise (VariableNameError("SymphonieReader", "An error occured : '" + str(ex) + "'", 1000))
