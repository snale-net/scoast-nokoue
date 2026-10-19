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
import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.spatial import cKDTree
from spatialetl.utils.timing import timing

""""
This optimal interpolator is inspired from 

Wong, A.P.S., Johnson, G.C., Owens, W.B., 2003. Delayed-mode calibration of
autonomous CTD profiling float salinity data by χ-S climatology. J. Atmos. Ocean.
Technol. 20, 308–318. https://doi.org/10.1175/1520-0426(2003)020<0308:
DMCOAC>2.0.CO;2.

Bretherton, F.P., Davis, R.E., Fandry, C.B., 1976. A technique for objective analysis and
design of oceanographic experiments applied to MODE-73. Deep. Res. Oceanogr.
Abstr. 23, 559–582. https://doi.org/10.1016/0011-7471(76)90001-2.

McIntosh, P.C., 1990. Oceanographic data interpolation: objective analysis and splines.
J. Geophys. Res. 95, 13529. https://doi.org/10.1029/jc095ic08p13529.
"""


def objective_analysis(
        x_points,
        y_points,
        values_points,
        x_grid,
        y_grid,
        large_scale,
        small_scale
):
    # Source points
    if x_points.shape != y_points.shape:
        raise ValueError(f"Source points X / Y axis haven't the same size : {x_points.shape} / {y_points.shape}")

    src_x_points = x_points.flatten()
    src_y_points = y_points.flatten()
    src_values_points = values_points.flatten()
    src_xy_points = np.column_stack((src_y_points, src_x_points))

    # Destination grid
    if x_grid.ndim != 2 and y_grid.ndim != 2:
        x_grid, y_grid = np.meshgrid(x_grid, y_grid)
    elif x_grid.shape != y_grid.shape:
        raise ValueError(f"dst_grid isn't a regular grid")
    dst_xy_grid = np.column_stack((y_grid.flatten(), x_grid.flatten()))

    noise_var = noise_est(src_values_points.reshape(1, -1), src_y_points, src_x_points)
    signal_var = signal_est(src_values_points.reshape(1, -1))

    # Grande échelle
    z1, e1, zdata1 = map_grid(
        src_values_points,
        src_points=src_xy_points,
        dst_grid=dst_xy_grid,
        scale=large_scale,
        signal_var=signal_var,
        noise_var=noise_var
    );

    # Petite échelle sur résidu
    residual = src_values_points - zdata1
    signal_res = signal_est(residual.reshape(1, -1))

    z2, e2, _ = map_grid(
        residual,
        src_points=src_xy_points,
        dst_grid=dst_xy_grid,
        scale=small_scale,
        signal_var=signal_res,
        noise_var=noise_var
    );

    z = z1 + z2
    e = e1 + e2

    mapped_data = z.reshape(x_grid.shape)
    mapped_error = e.reshape(x_grid.shape)

    return mapped_data, mapped_error


def map_grid(
        src_values,
        src_points,
        dst_grid,
        scale,
        signal_var,
        noise_var
):
    nData = src_points.shape[0]

    # --- Covariance matrix ---
    covar_points = signal_var * covarxy(src_points, src_points, scale)
    Cdd = covar_points + noise_var * np.eye(nData)

    c, lower = cho_factor(Cdd)

    def solve(B):
        return cho_solve((c, lower), B)

    # --- Precompute solves ---
    ones = np.ones(nData)

    Cinv_1 = solve(ones)
    Cinv_z = solve(src_values)

    sumC = Cinv_1.sum()
    moy = Cinv_z.sum() / sumC

    # weights
    w = solve(src_values - moy)

    # --- Data interpolation ---
    vdata = covar_points @ w + moy

    # --- Grid interpolation ---
    Cmd = signal_var * covarxy(dst_grid, src_points, scale)
    vgrid = Cmd @ w + moy

    # --- Error computation (optimized) ---
    # Solve once for all grid points
    X = solve(Cmd.T)  # shape: (nData, nGrid)

    # diag(Cmd @ Cinv @ Cmd.T) without full matrix product
    diag_term = np.einsum("ij,ij->j", Cmd.T, X)

    # sum(Cmd @ Cinv, axis=1)
    sum_term = X.sum(axis=0)

    vgriderror = np.sqrt(
        signal_var
        - diag_term
        + ((1 - sum_term) ** 2) / sumC
    )

    return vgrid, vgriderror, vdata


def covarxy(
        dst_points,
        src_points,
        scale
):
    # Split coordinates
    src_lat = src_points[:, 0]
    src_lon = src_points[:, 1]

    dst_lat = dst_points[:, 0]
    dst_lon = dst_points[:, 1]

    # Broadcasted pairwise distances
    d = ac_distance(
        src_lat[None, :],  # shape (1, n2)
        src_lon[None, :],
        dst_lat[:, None],  # shape (n1, 1)
        dst_lon[:, None]
    )

    # Covariance matrix
    C = np.exp(-(d / scale) ** 2)

    return C


def noise_est(
        a,
        xlat,
        xlong
):
    coords = np.column_stack((xlat, xlong))
    tree = cKDTree(coords)

    # k=2 → first neighbor is self, second is nearest other point
    dist, idx = tree.query(coords, k=2)

    nn_idx = idx[:, 1]

    diffv = a - a[:, nn_idx]

    return np.nanvar(diffv, axis=1) / 2


def signal_est(
        a
):
    return np.nanvar(a, axis=1);


def ac_distance(
        y_points,
        x_points,
        y_point: float,
        x_point: float
):
    lat1 = np.radians(y_points)
    lat2 = np.radians(y_point)
    lon1 = np.radians(x_points)
    lon2 = np.radians(x_point)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    sin_dlat = np.sin(dlat * 0.5)
    sin_dlon = np.sin(dlon * 0.5)

    a = sin_dlat * sin_dlat + np.cos(lat1) * np.cos(lat2) * sin_dlon * sin_dlon

    rng = 2 * 6371 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))

    return rng
