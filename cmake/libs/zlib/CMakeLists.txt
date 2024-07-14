find_package(Git REQUIRED)

set(ZLIB_BUILD_EXAMPLES OFF)

FetchContent_Declare(
    zlib
    URL https://www.zlib.net/zlib-1.3.1.tar.xz
    URL_HASH SHA256=38ef96b8dfe510d42707d9c781877914792541133e1870841463bfa73f883e32
    PATCH_COMMAND ${GIT_EXECUTABLE} apply --directory=build/_deps/zlib-src ${CMAKE_CURRENT_SOURCE_DIR}/zlib.patch
)

FetchContent_MakeAvailable(zlib)
