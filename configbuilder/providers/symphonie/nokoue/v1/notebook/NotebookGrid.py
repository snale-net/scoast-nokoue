from configbuilder.builder.file_template import FileTemplate
from configbuilder.exception.FileError import FileError
import f90nml
import os

class NotebookGrid(FileTemplate):

    def __init__(self,base_dir,base_file,mpi_map_file_name=None,mpi_hole_plugging=None,lonlatfile=None):

        FileTemplate.__init__(self, base_dir, "notebook_grid.f");

        nml = f90nml.read(base_file)

        self.iglb = nml["notebook_grid"]["iglb"]
        self.jglb = nml["notebook_grid"]["jglb"]
        self.kmax = nml["notebook_grid"]["kmax"]
        self.dxb = nml["notebook_grid"]["dxb"]
        self.dyb = nml["notebook_grid"]["dyb"]
        self.phi0 = nml["notebook_grid"]["phi0"]
        self.longi0 = nml["notebook_grid"]["longi0"]
        self.latit0 = nml["notebook_grid"]["latit0"]
        self.grid_i0 = nml["notebook_grid"]["grid_i0"]
        self.grid_j0 = nml["notebook_grid"]["grid_j0"]
        self.rayonterre = nml["notebook_grid"]["rayonterre"]
        self.northpole_lon = nml["notebook_grid"]["northpole_lon"]
        self.northpole_lat = nml["notebook_grid"]["northpole_lat"]
        self.southpole_lon = nml["notebook_grid"]["southpole_lon"]
        self.southpole_lat = nml["notebook_grid"]["southpole_lat"]
        self.nbdom_imax = nml["notebook_grid"]["nbdom_imax"]
        self.nbdom_jmax = nml["notebook_grid"]["nbdom_jmax"]
        self.iperiodicboundary = nml["notebook_grid"]["iperiodicboundary"]
        self.jperiodicboundary = nml["notebook_grid"]["jperiodicboundary"]

        self.mpi_map_file_name = None
        self.set_mpi_map_file_name(mpi_map_file_name)

        self.mpi_hole_plugging = None
        self.set_mpi_hole_plugging(mpi_hole_plugging)

        self.lonlatfile = None
        self.set_lonlatfile(lonlatfile)

    def set_mpi_map_file_name(self,value):

        if value != None:
            if os.path.isfile(value):
                if len(value) > 100:
                    raise FileError("NotebookGrid",
                                    "MPI map path location '" + value + "' is too long. Max 100 characters", 1005)
                self.mpi_map_file_name = value
            else:
                raise FileError("NotebookGrid",
                                "MPI map file '" + value + "' doesn't exist", 1005)

    def set_mpi_hole_plugging(self,value):
        if value != None:
            if os.path.isfile(value):
                if len(value) > 100:
                    raise FileError("NotebookGrid",
                                    "MPI hole pluggin path location '" + value + "' is too long. Max 100 characters", 1005)
                self.mpi_hole_plugging = value
            else:
                raise FileError("NotebookGrid",
                                "MPI hole pluggin file '" + value + "' doesn't exist", 1005)

    def set_lonlatfile(self,value):
        if os.path.isfile(value):
            if len(value) > 100:
                raise FileError("NotebookGrid",
                                "LonLat path location '" + value + "' is too long. Max 100 characters", 1005)

            self.lonlatfile = value
        else:
            raise FileError("NotebookGrid",
                            "LonLat file '" + value + "' doesn't exist", 1005)






