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
from configbuilder.exception.FileError import FileError

class NotebookBathy(FileTemplate):

    def __init__(self,base_dir,texte250,mangrove_file_name):

        FileTemplate.__init__(self, base_dir, "notebook_bathy.f");
        self.texte250 = None
        self.set_texte250(texte250)

        self.mangrove_file_name = None
        self.set_mangrove_file_name(mangrove_file_name)

    def set_texte250(self, value):
        # Check if file exist
        if os.path.isfile(value):
            if len(value) > 100:
                raise FileError("NotebookBathy",
                                "Bathymetry path location '" + value + "' is too long. Max 100 characters", 1005)
            self.texte250 = value
        else:
            raise FileError("NotebookBathy",
                            "Bathymetry file '" + value + "' doesn't exist", 1005)

    def set_mangrove_file_name(self, value):
        # Check if file exist
        if os.path.isfile(value):
            if len(value) > 100:
                raise FileError("NotebookBathy",
                                "Mangrove path location '" + value + "' is too long. Max 100 characters", 1005)
            self.mangrove_file_name = value
        else:
            raise FileError("NotebookBathy",
                            "Mangrove file '" + value + "' doesn't exist", 1005)









