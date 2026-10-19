# -*- coding: utf-8 -*-
from pathlib import Path

from configbuilder.providers.symphonie.SymphonieConfig import SymphonieConfig
from configbuilder.providers.symphonie.nokoue.v1.notebook import *
import os


class S26Nokoue(SymphonieConfig):
    VERSION = "v1"
    BASE_DIR = Path(__file__).resolve().parent.parent

    def __init__(
            self,
            output_dir,
            notebook_grid,
            bathycote_in_file,
            lonlatfile,
            meteo_forcing_dir,
            obc_forcing_dir,
            tide_forcing_dir,
            river_so_forcing_file,
            river_oueme_forcing_file,
            river_djonou_forcing_file,
            river_portonovo_forcing_file,
            start_time,
            end_time,
            run_mode=0,
            config_name="NOK_MORA_v391",
            mpi_map_file_name=None,
            mpi_hole_plugging=None,
            model_source_dir=None,
    ):
        SymphonieConfig.__init__(self, model_source_dir, output_dir, config_name);

        self.set_meteo_forcing_dir(meteo_forcing_dir)
        self.set_obc_forcing_dir(obc_forcing_dir)

        # notebook_advection
        nb = NotebookAdvection(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_advection"] = nb

        # notebook_airseaflux
        nb = NotebookAirseaflux(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_airseaflux"] = nb

        # notebook_atlas
        nb = NotebookAtlas(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_atlas"] = nb

        # notebook_bathy
        nb = NotebookBathy(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            bathycote_in_file)
        self.notebooks["notebook_bathy"] = nb

        # notebook_bio
        nb = NotebookBio(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_bio"] = nb

        # notebook_bouees
        nb = NotebookBouees(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_bouees"] = nb

        # notebook_dateoutput
        nb = NotebookDateoutput(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_dateoutput"] = nb

        # notebook_drifter
        nb = NotebookDrifter(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_drifter"] = nb

        # notebook_eqstate
        nb = NotebookEqstate(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_eqstate"] = nb

        # notebook_graph
        nb = NotebookGraph(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_graph"] = nb

        # notebook_grid
        nb = NotebookGrid(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            base_file=notebook_grid,
            mpi_map_file_name=mpi_map_file_name,
            mpi_hole_plugging=mpi_hole_plugging,
            lonlatfile=lonlatfile
        )
        self.notebooks["notebook_grid"] = nb

        # notebook_list
        nb = NotebookList(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_list"] = nb

        # notebook_nesting
        nb = NotebookNesting(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_nesting"] = nb

        # notebook_nh
        nb = NotebookNH(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_nh"] = nb

        # notebook_oasis
        nb = NotebookOasis(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_oasis"] = nb

        # notebook_obcforcing
        nb = NotebookOBCForcing(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_obcforcing"] = nb

        # notebook_offline
        nb = NotebookOffline(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_offline"] = nb

        # notebook_optical
        nb = NotebookOptical(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_optical"] = nb

        # notebook_rivers
        nb = NotebookRivers(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            so_file=river_so_forcing_file,
            oueme_file=river_oueme_forcing_file,
            djonou_file=river_djonou_forcing_file,
            portonovo_file=river_portonovo_forcing_file,
        )
        self.notebooks["notebook_rivers"] = nb

        # notebook_spongelayer
        nb = NotebookSpongelayer(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks[" notebook_spongelayer"] = nb

        # notebook_tide
        nb = NotebookTide(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name,
            tide_forcing_dir=tide_forcing_dir)
        self.notebooks["notebook_tide"] = nb

        # notebook_time
        nb = NotebookTime(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            start_time,
            end_time,
            run_mode)
        self.notebooks["notebook_time"] = nb

        # notebook_tracer
        nb = NotebookTracer(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_tracer"] = nb

        # notebook_vertcoord
        nb = NotebookVertcoord(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_vertcoord"] = nb

        # notebook_visco
        nb = NotebookVisco(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"))
        self.notebooks["notebook_visco"] = nb

        # notebook_wave
        nb = NotebookWave(
            os.path.join(S26Nokoue.BASE_DIR, S26Nokoue.VERSION.lower(), "notebook"),
            self.config_name)
        self.notebooks["notebook_wave"] = nb

    def generate(self, only_config=False, overwrite=False):
        SymphonieConfig.generate(self,only_config=only_config,overwrite=overwrite)
        runDir = os.path.join(self.output_config_dir, self.config_name, "RUN")
        os.makedirs(runDir, exist_ok=True)
        os.makedirs(os.path.join(runDir, "tmp"), exist_ok=True)
        os.makedirs(os.path.join(runDir, "restart_input"), exist_ok=True)
        os.makedirs(os.path.join(runDir, "restart_output"), exist_ok=True)
        os.makedirs(os.path.join(runDir, "restart_outbis"), exist_ok=True)
