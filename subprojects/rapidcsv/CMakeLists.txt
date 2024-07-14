subprojects_add(
    NAME rapidcsv
    URL https://github.com/d99kris/rapidcsv/archive/refs/tags/v8.83.tar.gz
    HASH SHA256=9342eeb0ce37e30b778c4c030129d03e99f44a66d4710ac19627187bee774097
    PATCH_FILE ${CMAKE_CURRENT_SOURCE_DIR}/rapidcsv.patch
    CMAKE_CACHE_ARGS
        -DRAPIDCSV_BUILD_TESTS:BOOL=OFF
)
