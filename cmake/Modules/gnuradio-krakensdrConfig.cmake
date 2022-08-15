find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_KRAKENSDR gnuradio-krakensdr)

FIND_PATH(
    GR_KRAKENSDR_INCLUDE_DIRS
    NAMES gnuradio/krakensdr/api.h
    HINTS $ENV{KRAKENSDR_DIR}/include
        ${PC_KRAKENSDR_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_KRAKENSDR_LIBRARIES
    NAMES gnuradio-krakensdr
    HINTS $ENV{KRAKENSDR_DIR}/lib
        ${PC_KRAKENSDR_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-krakensdrTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_KRAKENSDR DEFAULT_MSG GR_KRAKENSDR_LIBRARIES GR_KRAKENSDR_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_KRAKENSDR_LIBRARIES GR_KRAKENSDR_INCLUDE_DIRS)
