subprojects_add(
    NAME wxwidgets
    DEPENDS zlib
    URL https://github.com/wxWidgets/wxWidgets/releases/download/v3.2.5/wxWidgets-3.2.5.tar.bz2
    HASH SHA256=0ad86a3ad3e2e519b6a705248fc9226e3a09bbf069c6c692a02acf7c2d1c6b51
    PATCH_FILE ${CMAKE_CURRENT_SOURCE_DIR}/wxwidgets.patch
    CMAKE_CACHE_ARGS
        -DwxBUILD_SHARED:BOOL=OFF
)
