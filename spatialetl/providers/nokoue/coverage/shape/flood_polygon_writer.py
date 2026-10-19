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

import geopandas as gpd
import numpy as np
from rasterio.features import shapes
from rasterio.transform import Affine
from scipy.interpolate import splprep, splev
from shapely import Polygon, MultiPolygon
from shapely.geometry import shape
from shapely.ops import unary_union
from spatialetl.coverage.io.coverage_writer import CoverageWriter
from spatialetl.coverage.time_coverage import TimeCoverage
from spatialetl.coverage.time_level_coverage import TimeLevelCoverage
from spatialetl.exception.coverage_error import CoverageError
from spatialetl.utils.logger import logging
from spatialetl.utils.variable_definition import VariableDefinition


def smooth_polygon_spline(poly, smoothing=2.0, num_points=1000):
    coords = np.array(poly.exterior.coords)

    if len(coords) < 4:
        return poly

    x, y = coords[:, 0], coords[:, 1]

    tck, _ = splprep([x, y], s=smoothing, per=True)
    u_new = np.linspace(0, 1, num_points)
    x_new, y_new = splev(u_new, tck)

    return Polygon(np.column_stack([x_new, y_new]))


def smooth_geometry(geom, smoothing=1.0, num_points=1000):
    if geom.geom_type == "Polygon":
        return smooth_polygon_spline(geom, smoothing, num_points)

    elif geom.geom_type == "MultiPolygon":
        return MultiPolygon([
            smooth_polygon_spline(p, smoothing, num_points)
            for p in geom.geoms
        ])

    return geom


class FloodingPolygonWriter(CoverageWriter):

    def __init__(self, cov, myFile, classification=[1, 2, 3, 4], mask=None):
        CoverageWriter.__init__(self, cov, myFile);

        if self.coverage.is_regular_grid() == False:
            raise ValueError("This writer supports only Coverage with a regular horizontal axis.")

        if os.path.isdir(self.filename) is False:
            raise ValueError("Filename has to be a directory.")

        self.rows = self.coverage.get_x_size(type="target_global")
        self.cols = self.coverage.get_y_size(type="target_global")

        xmin = np.min(self.coverage.read_axis_x(type="target_global"))
        xmax = np.max(self.coverage.read_axis_x(type="target_global"))
        ymin = np.min(self.coverage.read_axis_y(type="target_global"))
        ymax = np.max(self.coverage.read_axis_y(type="target_global"))
        self.x_pixel_size = round((xmax - xmin) / self.coverage.get_x_size(type="target_global"), 6)
        self.y_pixel_size = round((ymax - ymin) / self.coverage.get_y_size(type="target_global"), 6)

        self.transform = Affine.from_gdal(xmin, self.x_pixel_size, 0.0, ymin, 0.0, self.y_pixel_size)

        self.classification = classification

        if mask and os.path.isfile(mask):
            self.mask = gpd.read_file(mask)
        else:
            self.mask = None

    def close(self):
        return

    # Variables
    def write_variable_flood_extent(self):

        if (isinstance(self.coverage, TimeCoverage) or isinstance(self.coverage, TimeLevelCoverage)):

            for time_index in range(0, self.coverage.get_t_size()):
                time = self.coverage.read_axis_t(type="target_global")[time_index]

                logging.info(f"[FloodPolygonWriter] Writing flood extent at time '{time}'")

                global_data = np.empty([self.coverage.get_y_size(), self.coverage.get_x_size()])

                local_data = self.coverage.read_variable_sea_water_column_thickness_at_time(time_index)
                self._gathering_var(local_data, global_data)

                global_data[global_data == 9.96921e+36] = np.nan  # Remove NaN
                global_data[global_data <= 0.1] = np.nan

                # smoothed = gaussian_filter(global_data, sigma=0.2)

                # Raster to polygon
                mask = ~np.isnan(global_data)
                geoms = (
                    shape(geom)
                    for geom, value in shapes(mask.astype("uint8"), transform=self.transform)
                    if value == 1
                )
                total_union = unary_union(list(geoms))

                # smoothed = smooth_geometry(total_union, smoothing=min(self.x_pixel_size, self.y_pixel_size) / 2)
                # simplified = smoothed.simplify(min(self.x_pixel_size, self.y_pixel_size), preserve_topology=True)

                union_vector_gdf = gpd.GeoDataFrame(geometry=[total_union], crs="EPSG:4326")
                union_vector_gdf['Type'] = 'flooded'
                union_vector_gdf['Datetime'] = time.strftime("%Y-%m-%d %H:%M:%S")

                # Saving GeoDataFrame to shapefile
                union_vector_gdf.to_file(
                    os.path.join(self.filename, f"{time.strftime("%Y%m%d_%H%M%S")}_flood_extent.shp"))
        else:
            raise CoverageError("FloodingPolygonWriter",
                                "The given coverage is not an instance of 'TimeCoverage' or 'TimeLevelCoverage'")

    def write_variable_flood_severity(self):

        if (isinstance(self.coverage, TimeCoverage) or isinstance(self.coverage, TimeLevelCoverage)):

            for time_index in range(0, self.coverage.get_t_size()):
                time = self.coverage.read_axis_t(type="target_global")[time_index]

                height = np.empty([self.coverage.get_y_size(), self.coverage.get_x_size()])

                local_data = self.coverage.read_variable_sea_water_column_thickness_at_time(time_index)
                self._gathering_var(local_data, height)

                height[height == 9.96921e+36] = np.nan  # Remove NaN
                height[height <= 0.1] = np.nan

                speed = np.empty([self.coverage.get_y_size(), self.coverage.get_x_size()])
                local_data = self.coverage.read_variable_barotropic_sea_water_speed_at_time(time_index)
                self._gathering_var(local_data, speed)

                global_data = np.stack((height, speed))

                # Apply classification with height and speed
                # https://www.ecologie.gouv.fr/sites/default/files/documents/Guide_m%C3%A9thodo_PPRL_%202014.pdf
                # Page 109
                # severity 1 = low
                # severity 2 = moderate
                # severity 3 = high
                # severity 4 = very high
                global_data[0][(global_data[0] > 1.0) & (global_data[1] >= 0.5)] = 4
                global_data[0][(global_data[0] > 1.0) & (global_data[1] < 0.5)] = 3
                global_data[0][(global_data[0] >= 0.5) & (global_data[0] <= 1.0) & (global_data[1] >= 0.5)] = 3
                global_data[0][(global_data[0] >= 0.5) & (global_data[0] <= 1.0) & (global_data[1] < 0.5)] = 2
                global_data[0][(global_data[0] < 0.5) & (global_data[1] >= 0.5)] = 2
                global_data[0][(global_data[0] > 0.1) & (global_data[1] < 0.5)] = 1

                for dem_threshold in self.classification:
                    mask = np.ma.masked_equal(global_data[0][:], dem_threshold).mask

                    if np.all(mask == False):
                        logging.warning(
                            f"[FloodPolygonWriter] No flood severity {dem_threshold} was found at time '{time}'")
                        continue

                    geoms = (
                        shape(geom)
                        for geom, value in shapes(mask.astype("uint8"), transform=self.transform)
                        if value == 1
                    )
                    total_union = unary_union(list(geoms))

                    if total_union.is_empty:
                        logging.warning(
                            f"[FloodPolygonWriter] No flood severity {dem_threshold} was found at time '{time}'")
                        continue

                    logging.info(
                        f"[FloodPolygonWriter] Writing flood severity {dem_threshold} at time '{time}'")

                    # smoothed = smooth_geometry(total_union, smoothing=min(self.x_pixel_size, self.y_pixel_size) / 2)

                    union_vector_gdf = gpd.GeoDataFrame(geometry=[total_union], crs="EPSG:4326")

                    if self.mask is not None:
                        union_vector_gdf = union_vector_gdf.overlay(self.mask, how='difference')

                    union_vector_gdf['Type'] = 'classification'
                    union_vector_gdf['Severity'] = dem_threshold
                    union_vector_gdf['Datetime'] = time.strftime("%Y-%m-%d %H:%M:%S")

                    # Saving GeoDataFrame to shapefile
                    union_vector_gdf.to_file(
                        os.path.join(self.filename, f"{time.strftime("%Y%m%d_%H%M%S")}_flood_severity.shp"), mode="a")

        else:
            raise CoverageError("FloodingPolygonWriter",
                                "The given coverage is not an instance of 'TimeCoverage' or 'TimeLevelCoverage'")
