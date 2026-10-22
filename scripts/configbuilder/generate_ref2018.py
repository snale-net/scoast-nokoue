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
import logging
import os

from configbuilder.providers.symphonie.SymphonieConfig import SymphonieConfig
from configbuilder.providers.symphonie.nokoue.v1.S26Nokoue import S26Nokoue

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

    # All these directories have to be binded during the Singularity exec command
    grid_base_dir = "/work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/grid"
    forcings_base_dir = "/work/SCO/SCOAST/NOKOUE/RAW/forcings"
    config_base_dir = "/work/DTF/common/UC/SCOAST/NK/SYMPHONIE-v1.0/configurations"

    config_name = "REF2018"

    logging.info("Create config : " + config_name + "...")

    if not os.path.isdir(config_base_dir):
        # Create the configuration directory
        os.mkdir(config_base_dir)

    myConfig = S26Nokoue(
        config_name=config_name,
        output_dir=config_base_dir,
        start_time='2017-11-01 00:00:00',
        end_time='2019-01-01 00:00:00',
        notebook_grid=f"{grid_base_dir}/notebook_grid.f",
        mpi_map_file_name=f"{grid_base_dir}/description_domaine_180.next",
        mpi_hole_plugging=f"{grid_base_dir}/description_trous_180.txt",
        lonlatfile=f"{grid_base_dir}/lonlat_Cotonou_20190211.nc",
        bathycote_in_file=f"{grid_base_dir}/bathycote_in_CNES_V1.0.ijh",
        mangrove_file_name=f"{grid_base_dir}/mask_mangrove_cnes.dat",
        meteo_forcing_dir=f"{forcings_base_dir}/DATA/ECMWF",
        obc_forcing_dir=f"{forcings_base_dir}/DATA/COPERNICUS",
        tide_forcing_dir=f"{forcings_base_dir}/FES2014",
        river_so_forcing_file=f"{forcings_base_dir}/FLEUVES/Yves_R1012_6m3s/SO_academic_new.dat",
        river_oueme_forcing_file=f"{forcings_base_dir}/FLEUVES/Yves_R1012_6m3s/OUEME_academic_new.dat",
        river_djonou_forcing_file=f"{forcings_base_dir}/FLEUVES/Yves_R1012_6m3s/DJONOU_academic_new.dat",
        river_portonovo_forcing_file=f"{forcings_base_dir}/FLEUVES/Yves_R1012_6m3s/DJONOU_academic_new.dat"
    )

    myConfig.generate(only_config=True,overwrite=True)

    logging.info("Config generated with success")
