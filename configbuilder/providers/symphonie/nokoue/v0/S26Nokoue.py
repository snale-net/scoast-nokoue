# -*- coding: utf-8 -*-
from configbuilder.providers.symphonie.SymphonieConfig import SymphonieConfig
from configbuilder.providers.symphonie.nokoue.build import Makefile, MakefileInc
from configbuilder.providers.symphonie.nokoue.notebook import *
import os


class S26Nokoue(SymphonieConfig):
    VERSION = "NOKOUE"

    def __init__(
            self,
            model_source_dir,
            output_dir,
            config_name,
            notebook_grid,
            bathycote_in_file,
            lonlatfile,
            meteo_forcing_dir,
            obc_forcing_dir,
            tide_forcing_dir,
            start_time,
            end_time,
            comp="IFORT",
            compiler="mpiexec.hydra",
            run_mode=0,
            debug_mode=False,
            mpi_map_file_name=None,
            mpi_hole_plugging=None,
    ):
        SymphonieConfig.__init__(self, model_source_dir, output_dir, config_name);

        self.set_meteo_forcing_dir(meteo_forcing_dir)
        self.set_obc_forcing_dir(obc_forcing_dir)

        # Makefile
        self.makefiles.append(Makefile(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "build")))
        self.makefiles.append(MakefileInc(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "build"),
            self.config_name,
            SymphonieConfig.NETCDF_INC,
            SymphonieConfig.NETCDF_LIB,
            comp=comp,
            compiler=compiler,
            debug_mode=debug_mode))

        # notebook_advection
        nb = NotebookAdvection(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_advection"] = nb

        # notebook_airseaflux
        nb = NotebookAirseaflux(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_airseaflux"] = nb

        # notebook_atlas
        nb = NotebookAtlas(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_atlas"] = nb

        # notebook_bathy
        nb = NotebookBathy(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            bathycote_in_file)
        self.notebooks["notebook_bathy"] = nb

        # notebook_bio
        nb = NotebookBio(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_bio"] = nb

        # notebook_bouees
        nb = NotebookBouees(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_bouees"] = nb

        # notebook_dateoutput
        nb = NotebookDateoutput(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_dateoutput"] = nb

        # notebook_drifter
        nb = NotebookDrifter(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_drifter"] = nb

        # notebook_eqstate
        nb = NotebookEqstate(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_eqstate"] = nb

        # notebook_graph
        nb = NotebookGraph(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_graph"] = nb

        # notebook_grid
        nb = NotebookGrid(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            base_file=notebook_grid,
            mpi_map_file_name=mpi_map_file_name,
            mpi_hole_plugging=mpi_hole_plugging,
            lonlatfile=lonlatfile
        )
        self.notebooks["notebook_grid"] = nb

        # notebook_list
        nb = NotebookList(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_list"] = nb

        # notebook_nesting
        nb = NotebookNesting(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_nesting"] = nb

        # notebook_nh
        nb = NotebookNH(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_nh"] = nb

        # notebook_oasis
        nb = NotebookOasis(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_oasis"] = nb

        # notebook_obcforcing
        nb = NotebookOBCForcing(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_obcforcing"] = nb

        # notebook_offline
        nb = NotebookOffline(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_offline"] = nb

        # notebook_optical
        nb = NotebookOptical(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_optical"] = nb

        # notebook_rivers
        nb = NotebookRivers(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_rivers"] = nb

        # notebook_spongelayer
        nb = NotebookSpongelayer(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks[" notebook_spongelayer"] = nb

        # notebook_tide
        nb = NotebookTide(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name,
            tide_forcing_dir=tide_forcing_dir)
        self.notebooks["notebook_tide"] = nb

        # notebook_time
        nb = NotebookTime(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            start_time,
            end_time,
            run_mode)
        self.notebooks["notebook_time"] = nb

        # notebook_tracer
        nb = NotebookTracer(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_tracer"] = nb

        # notebook_vertcoord
        nb = NotebookVertcoord(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_vertcoord"] = nb

        # notebook_visco
        nb = NotebookVisco(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_visco"] = nb

        # notebook_wave
        nb = NotebookWave(
            os.path.join(SymphonieConfig.BASE_DIR, SymphonieConfig.MODEL.lower(), S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_wave"] = nb

    def add_river_forcing(self, name,
                          i_index,
                          j_index,
                          length,
                          flux_direction,
                          distance_wind,
                          default_discharge,
                          water_depth,
                          salinity,
                          min_annual_temperature,
                          month_min_temperature,
                          max_annual_temperature,
                          periodicity_discharge,
                          start_time,
                          file=None):
        river = {}
        river["name"] = name
        river["i_index"] = i_index
        river["j_index"] = j_index
        river["length"] = length
        river["flux_direction"] = flux_direction
        river["distance_wind"] = distance_wind
        river["default_discharge"] = default_discharge
        river["water_depth"] = water_depth
        river["salinity"] = salinity
        river["min_annual_temperature"] = min_annual_temperature
        river["month_min_temperature"] = month_min_temperature
        river["max_annual_temperature"] = max_annual_temperature
        river["periodicity_discharge"] = periodicity_discharge
        river["file"] = file
        river["start_time"] = start_time

        self.notebooks["notebook_rivers"].rivers_forcing.append(river)
