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

from datetime import timedelta

from dateutil.relativedelta import relativedelta

from configbuilder.builder.file_template import FileTemplate


class NotebookTracer(FileTemplate):

    def __init__(self, base_dir, let_out_count=0, let_out_freq="BMM", start_time=None):

        FileTemplate.__init__(self, base_dir, "notebook_tracer.f");

        if let_out_count > 0 and start_time is not None:
            self.enable = 1
            self.let_out_count = let_out_count
            # Compute date and index of tracers let out from the start time
            dates = []
            for i in range(let_out_count):
                if let_out_freq == "BOM":
                    date = start_time.replace(day=1) + relativedelta(months=i)
                elif let_out_freq == "MOM":
                    date = start_time.replace(day=15) + relativedelta(months=i)
                elif let_out_freq == "BMM":
                    date = start_time + relativedelta(
                        months=i // 2,
                        days=14 * (i % 2)
                    )
                dates.append(date)

            self.tracers_map = {
                i + 1: {
                    "start": date - timedelta(minutes=1),
                    "end": date + timedelta(seconds=10),
                }
                for i, date in enumerate(dates)
            }
        else:
            self.enable = 0
            self.let_out_count = 0
            self.tracers_map = {}
