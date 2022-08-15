# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT krakensdr_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT krakensdr_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND krakensdr_python_files
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(krakensdr
   ../../..
   gr::krakensdr
   "${krakensdr_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET krakensdr_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:krakensdr_python>
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/krakensdr/
)

install(TARGETS krakensdr_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/krakensdr COMPONENT pythonapi)
