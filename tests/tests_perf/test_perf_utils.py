#!/usr/bin/env python
# -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2016-2020, Intel Corporation
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
# *****************************************************************************

import time

import pandas


def get_exec_times(f, *args, repeat=5, number=1000000):
    """
    Get execution times.

    Parameters
    ----------
    f : func
        function to execute
    args : tuple
        parameters of the fucntion
    repeat : int
        number of measurements
    number : int
        number of the function calls within a single measurement

    Returns
    -------
    list
        list of execution times
    """
    exec_times = []

    # Warming up
    f(*args)

    for _ in range(repeat):
        start = time.time()
        for _ in range(number):
            f(*args)
        finish = time.time()

        exec_times.append((finish - start) / number)

    return exec_times


def is_true(input_string):
    """Check input is true"""
    if isinstance(input_string, str):
        input_string = input_string.lower()
    return input_string in ["yes", "y", "true", "t", "1", True]


class TestResults:
    results_data = pandas.DataFrame()

    def add(self, name, lib, dtype, size, **result):
        """Add performance testing results into global storage."""
        index_data = {
            "name": [name],
            "lib": [lib.__name__],
            "dtype": [dtype.__name__],
            "size": [size],
        }
        index = pandas.MultiIndex.from_frame(pandas.DataFrame(index_data))
        local_results_data = pandas.DataFrame(result, index=index)

        self.results_data = self.results_data.append(local_results_data)

    def print(self):
        """Print performance testing results from global data storage."""
        print("\nPerformance testing results:")
        print(self.results_data.sort_index().to_string())

    def dump(self):
        """Dump performance testing results from global data storage to csv."""
        self.results_data.sort_index().to_csv("perf_results.csv", float_format="%g")