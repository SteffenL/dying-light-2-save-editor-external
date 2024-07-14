find_package(Git REQUIRED)

set(RAPIDCSV_BUILD_TESTS OFF)

FetchContent_Declare(
    rapidcsv
    URL https://github.com/d99kris/rapidcsv/archive/refs/tags/v8.83.tar.gz
    URL_HASH SHA256=9342eeb0ce37e30b778c4c030129d03e99f44a66d4710ac19627187bee774097
    PATCH_COMMAND ${GIT_EXECUTABLE} apply --directory=build/_deps/rapidcsv-src ${CMAKE_CURRENT_SOURCE_DIR}/rapidcsv.patch
)

FetchContent_MakeAvailable(rapidcsv)
