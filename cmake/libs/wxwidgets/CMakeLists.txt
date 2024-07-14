find_package(Git REQUIRED)

set(wxBUILD_SHARED OFF)

FetchContent_Declare(
    wxwidgets
    URL https://github.com/wxWidgets/wxWidgets/releases/download/v3.2.5/wxWidgets-3.2.5.tar.bz2
    URL_HASH SHA256=0ad86a3ad3e2e519b6a705248fc9226e3a09bbf069c6c692a02acf7c2d1c6b51
    PATCH_COMMAND ${GIT_EXECUTABLE} apply --directory=build/_deps/wxwidgets-src ${CMAKE_CURRENT_SOURCE_DIR}/wxwidgets.patch
)

FetchContent_MakeAvailable(wxwidgets)
