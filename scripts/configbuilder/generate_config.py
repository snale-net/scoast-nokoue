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
import argparse
import logging
import os
from datetime import datetime

from configbuilder.providers.symphonie.nokoue.v1.S26Nokoue import S26Nokoue


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-n", "--config_name",
        type=str,
        help="Name of the configuration",
        required=True,
    )

    parser.add_argument(
        "--grid_notebook_path",
        type=str,
        help="Absolute path to the grid notebook file",
        required=True,
    )

    parser.add_argument(
        "--grid_coordinates_path",
        type=str,
        help="Absolute path to the grid coordinates file (lonlat)",
        required=True,
    )

    parser.add_argument(
        "--grid_bathycote_path",
        type=str,
        help="Absolute path to the grid bathymetry file (bathycote_in)",
        required=True,
    )

    parser.add_argument(
        "--mpi_domain_path",
        type=str,
        help="Absolute path to the MPI domain decomposition file (description_domain.next)",
        required=True,
    )

    parser.add_argument(
        "--mpi_hole_path",
        type=str,
        help="Absolute path to the MPI domain decomposition holes file (description_trou.txt)",
        required=True,
    )

    parser.add_argument(
        "--acadjas_mask_path",
        type=str,
        default=None,
        help="Absolute path to the Acadjas mask (default: None)"
    )

    parser.add_argument(
        "--meteo_forcing_path",
        type=str,
        help="Absolute path to the meteo forcing directory containing meteo field",
        required=True,
    )

    parser.add_argument(
        "--ocean_forcing_path",
        type=str,
        help="Absolute path to the ocean forcing directory containing ocean field",
        required=True,
    )

    parser.add_argument(
        "--tide_forcing_path",
        type=str,
        help="Absolute path to the tide forcing directory containing FES2014 field",
        required=True,
    )

    parser.add_argument(
        "--river_so_discharge_path",
        type=str,
        help="Absolute path to the river So discharge file",
        required=True,
    )

    parser.add_argument(
        "--river_oueme_discharge_path",
        type=str,
        help="Absolute path to the river Oueme discharge file",
        required=True,
    )

    parser.add_argument(
        "--river_djonou_discharge_path",
        type=str,
        help="Absolute path to the river Djonou discharge file",
        required=True,
    )

    parser.add_argument(
        "--start-time",
        type=datetime.fromisoformat,
        default=datetime.fromisoformat("2017-10-01 00:00:00"),
        help="Start datetime (format : YYYY-MM-DD HH:MM:SS)",
    )
    parser.add_argument(
        "--end-time",
        type=datetime.fromisoformat,
        default=datetime.fromisoformat("2019-01-01 00:00:00"),
        help="End datetime (format : YYYY-MM-DD HH:MM:SS)",
    )

    parser.add_argument(
        "--tracers_let_out_count",
        type=int,
        default=0,
        help="Number of tracers let out (default : 0)",
    )

    parser.add_argument(
        "--tracers_let_out_freq",
        type=str,
        choices=["BOM", "MOM", "BMM"],
        default="BMM",
        help=(
            "Tracers let ou frequency: "
            "BOM (Beginning Of Month), "
            "MOM (Middle Of Month), "
            "BMM (Beginning and Middle of Month)."
            "(default : BMM)"
        )
    )

    parser.add_argument(
        "-o", "--output_folder",
        type=str,
        help="Path to the folder where the configuration will be stored (default: ./outputs)",
        default="./outputs"
    )

    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

    args = parse_args()

    config_base_dir = args.output_folder
    config_name = args.config_name

    logging.info("Create config : " + config_name + "...")

    if not os.path.isdir(config_base_dir):
        # Create the configuration directory
        os.mkdir(config_base_dir)

    myConfig = S26Nokoue(
        config_name=config_name,
        output_dir=config_base_dir,
        start_time=args.start_time,
        end_time=args.end_time,
        notebook_grid=args.grid_notebook_path,
        lonlatfile=args.grid_coordinates_path,
        bathycote_in_file=args.grid_bathycote_path,
        mpi_map_file_name=args.mpi_domain_path,
        mpi_hole_plugging=args.mpi_hole_path,
        mangrove_file_name=args.acadjas_mask_path,
        meteo_forcing_dir=args.meteo_forcing_path,
        obc_forcing_dir=args.ocean_forcing_path,
        tide_forcing_dir=args.tide_forcing_path,
        river_so_forcing_file=args.river_so_discharge_path,
        river_oueme_forcing_file=args.river_oueme_discharge_path,
        river_djonou_forcing_file=args.river_djonou_discharge_path,
        river_portonovo_forcing_file=args.river_djonou_discharge_path,
        tracers_let_out_count=args.tracers_let_out_count,
        tracers_let_out_freq=args.tracers_let_out_freq,
    )

    myConfig.generate(only_config=True,overwrite=True)

    logging.info("Config generated with success")
