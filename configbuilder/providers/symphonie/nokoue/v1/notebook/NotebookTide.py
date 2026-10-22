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
from configbuilder.exception import DirectoryError


class NotebookTide(FileTemplate):

    def __init__(self,base_dir,name,tide_forcing_dir):

        FileTemplate.__init__(self, base_dir, "notebook_tide");
        self.config_name = name
        self.tide_forcing_dir = None
        self.set_tide_forcing_dir(tide_forcing_dir)

    def set_tide_forcing_dir(self,value):

        if (os.path.isdir(value)):

            if os.listdir(value):
                self.tide_forcing_dir = value
            else:
                raise DirectoryError("NotebookTide",
                                     "[Tide forcing directory] '" + value + "' is empty", 1005)
        else:
            raise DirectoryError("NotebookTide",
                                 "[Tide forcing directory] No such directory: '" + value + "'", 1005)

