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

from configbuilder.builder.file_template import FileTemplate
from configbuilder.exception import FileError


class NotebookRivers(FileTemplate):

    def __init__(self,base_dir,so_file,oueme_file,djonou_file,portonovo_file):

        FileTemplate.__init__(self, base_dir, "notebook_rivers");

        self.check_file_path_length(so_file)
        self.so_file = so_file

        self.check_file_path_length(oueme_file)
        self.oueme_file = oueme_file

        self.check_file_path_length(djonou_file)
        self.djonou_file = djonou_file

        self.check_file_path_length(portonovo_file)
        self.portonovo_file = portonovo_file

    def check_file_path_length(self, value):
        # Check if file exist
        if os.path.isfile(value):
            if len(value) > 200:
                raise FileError("NotebookRiver",
                                "River discharge file location '" + value + "' is too long. Max 200 characters", 1005)
        else:
            raise FileError("NotebookBathy",
                            "River discharge file location '" + value + "' doesn't exist", 1005)








