# Python code for an improved geometric inundation model considering hydrological connectivity and attenuation.
# Forked from https://github.com/geoye/attenuated_bathtub
# Adapted and Optimized with Numba

from queue import Queue

import numpy as np
from numba import njit
from osgeo import gdal
from scipy import ndimage
from scipy.ndimage import convolve
from spatialetl.utils.logger import logging


def read_img(filename, is_convert_nan=True, is_verbose=False, tofloat_16=False):
    dataset = gdal.Open(filename)
    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize
    im_proj = dataset.GetProjection()
    im_geotrans = dataset.GetGeoTransform()
    no_data = dataset.GetRasterBand(1).GetNoDataValue()
    im_data = dataset.GetRasterBand(1).ReadAsArray(0, 0, im_width, im_height)
    if tofloat_16:
        im_data = im_data.astype(np.float16)
    if is_convert_nan:
        im_data = im_data.astype(np.float32)
        im_data[im_data==no_data] = np.nan
    if is_verbose:
        return im_data, im_proj, im_geotrans
    else:
        return im_data


def write_img(file_path, im_proj, im_geotrans, im_data, dtype=None, nodata=None):
    if dtype is None:
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32
    else:
        datatype = dtype

    if len(im_data.shape) == 2:
        im_bands, (im_height, im_width) = 1, im_data.shape
    else:
        im_bands, im_height, im_width = im_data.shape 

    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(file_path, im_width, im_height, im_bands, datatype, options=['COMPRESS=LZW'])
    dataset.SetGeoTransform(im_geotrans)
    dataset.SetProjection(im_proj)

    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)
        if nodata:
            dataset.GetRasterBand(1).SetNoDataValue(nodata)
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i+1).WriteArray(im_data[i])
            if nodata:
                dataset.GetRasterBand(i+1).SetNoDataValue(nodata)
    del dataset


def inf2nan(x):
    x[np.isinf(x)] = np.nan
    return x

def nan2neginf(x):
    x[np.isnan(x)] = np.inf
    x[np.isinf(x)] = -np.inf
    return x

def remove_small_sea_areas(land_mask, min_pixels, offset=5):
    sea_mask = land_mask == 2

    labels, n = ndimage.label(sea_mask)

    sizes = np.bincount(labels.ravel())

    # Find amall areas in sea
    small_sea = np.zeros_like(sea_mask)

    for label in range(1, n + 1):
        if sizes[label] < min_pixels:
            small_sea[labels == label] = True

    # Transform sea to land
    land_mask[small_sea] = 1

    # Exclude an offset from the DEM borders
    if offset > 0:
        land_mask[:offset, :] = 1
        land_mask[-offset:, :] = 1
        land_mask[:, :offset] = 1
        land_mask[:, -offset:] = 1

    return land_mask

def extract_sea_level_at_coastline(slr_data,land_mask,offset=1):
    # 1 = land, 2 = sea
    land = land_mask == 1
    sea_mask = land_mask == 2

    # Find sea pixels directly adjacent to land pixels
    coast = np.zeros_like(land, dtype=bool)

    coast[:-1, :] |= land[:-1, :] & sea_mask[1:, :]
    coast[1:, :] |= land[1:, :] & sea_mask[:-1, :]
    coast[:, :-1] |= land[:, :-1] & sea_mask[:, 1:]
    coast[:, 1:] |= land[:, 1:] & sea_mask[:, :-1]

    # Exclude an offset from the DEM borders
    if offset > 0:
        coast[:offset, :] = False
        coast[-offset:, :] = False
        coast[:, :offset] = False
        coast[:, -offset:] = False

    sea_values_2d = np.full(land_mask.shape, np.nan)
    sea_values_2d[coast] = slr_data[coast]

    return sea_values_2d

def convolve_sealand_edge(mask):
    window = [[-1,-1,-1],
              [-1, 8,-1],
              [-1,-1,-1]]
    mask = mask - 1
    edges = np.where(convolve(mask, window, mode='constant') > 1)
    return np.column_stack(edges).tolist()


def get_land_mask(dem, slr, mask):
    return (mask == 1) & (dem <= np.nanmax(slr))


def initialize_queue(border):
    # ini_list = convolve_sealand_edge(all_mask)
    ini_list = np.column_stack(np.where(~np.isinf(border))).tolist()
    q = Queue()
    for idx in ini_list:
        q.put(idx)
    return q

def fast_atte_bathtub(dem, border_data, all_mask, atte_factor=0.02):
    land_mask = np.isfinite(dem)

    initial_queue = np.column_stack(
        np.where(~np.isinf(border_data))
    )

    n_initial = len(initial_queue)

    nrows, ncols = dem.shape

    queue = np.empty(
        dem.size,
        dtype=np.int64
    )

    in_queue = np.zeros(
        dem.shape,
        dtype=np.bool_
    )

    queue[:n_initial] = (
            initial_queue[:, 0] * ncols
            + initial_queue[:, 1]
    )

    in_queue[
        initial_queue[:, 0],
        initial_queue[:, 1]
    ] = True

    border_data, processed, updates, status = propagate_slr(
        dem,
        land_mask,
        border_data,
        queue,
        in_queue,
        atte_factor,
        n_initial
    )

    logging.debug("Processed:", processed)
    logging.debug("Updates:", updates)
    logging.debug("Status:", status)

    flood_depth = np.where(
        all_mask == 1,
        border_data,
        np.nan
    )

    flood_depth = inf2nan(flood_depth) - dem
    return flood_depth

@njit
def propagate_slr(
    dem,
    land_mask,
    border_data,
    queue,
    in_queue,
    atte_factor,
    n_initial
):
    nrows, ncols = dem.shape
    max_queue = queue.size

    dx = np.array(
        [-1, 1, 0, 0, -1, -1, 1, 1],
        dtype=np.int32
    )

    dy = np.array(
        [0, 0, -1, 1, -1, 1, -1, 1],
        dtype=np.int32
    )

    # Circular queue
    head = 0
    tail = n_initial
    queue_size = n_initial

    processed = 0
    updates = 0

    while queue_size > 0:

        # Get queue element
        idx = queue[head]

        head += 1
        if head >= max_queue:
            head = 0

        queue_size -= 1
        processed += 1

        x = idx // ncols
        y = idx % ncols

        in_queue[x, y] = False

        current_slr = border_data[x, y]
        new_slr = current_slr - atte_factor

        for k in range(8):

            nx = x + dx[k]
            ny = y + dy[k]

            # Boundary
            if nx < 0 or nx >= nrows:
                continue

            if ny < 0 or ny >= ncols:
                continue

            # Land only
            if not land_mask[nx, ny]:
                continue

            # Valid DEM
            if np.isnan(dem[nx, ny]):
                continue

            # Flood condition
            if dem[nx, ny] >= new_slr:
                continue

            # No improvement
            if new_slr <= border_data[nx, ny]:
                continue

            # Update
            border_data[nx, ny] = new_slr
            updates += 1

            # Add to queue
            if not in_queue[nx, ny]:

                # Check queue capacity
                if queue_size >= max_queue:
                    return border_data, processed, updates, -1

                queue[tail] = nx * ncols + ny

                tail += 1
                if tail >= max_queue:
                    tail = 0

                queue_size += 1

                in_queue[nx, ny] = True

    return border_data, processed, updates, 0
