from datetime import datetime
from configbuilder.builder.file_template import FileTemplate
from configbuilder.exception.DateValueError import DateValueError
from configbuilder.exception import RunModeValueError

class NotebookTime(FileTemplate):

    def __init__(self,base_dir,start_time,end_time,run_mode):

        FileTemplate.__init__(self, base_dir, "notebook_time.f");

        self.start_time = None
        self.set_start_time(start_time)

        self.end_time = None
        self.set_end_time(end_time)

        self.check_time()

        self.run_mode = None
        self.set_run_mode(run_mode)

    def set_start_time(self,value):
        if type(value) == datetime:
            self.start_time = value
        else:
            datetimeFormat = '%Y-%m-%d %H:%M:%S'
            try:
                self.start_time = datetime.strptime(value, datetimeFormat)
            except ValueError:
                raise DateValueError("NotebookTime",
                                "Start time '"+str(value)+"' does not match format '"+str(datetimeFormat)+"'",
                                1005)

    def set_end_time(self,value):
        if type(value) == datetime:
            self.end_time = value
        else:
            datetimeFormat = '%Y-%m-%d %H:%M:%S'
            try:
                self.end_time = datetime.strptime(value, datetimeFormat)
            except ValueError:
                raise DateValueError("NotebookTime",
                                "End time '"+str(value)+"' does not match format '"+str(datetimeFormat)+"'",
                                1005)

    def check_time(self):

        if self.end_time < self.start_time:
            raise DateValueError("NotebookTime",
                                "End time is before start time. Start time : '"+str(self.start_time)+"' / End time '"+str(self.end_time)+"'",
                                1005)

    def set_run_mode(self,value):

        if type(value) == int:
            if value == -1 or value == 0:
                self.run_mode = value
            else:
                raise RunModeValueError("NotebookTime",
                                     "Run mode have to be -1 or 0. Current value : '" + str(value) + "'",
                                     1005)
        else:
            raise RunModeValueError("NotebookTime",
                                    "Run mode have to be an integer. Current type : '" + str(type(value)) + "'",
                                    1005)










