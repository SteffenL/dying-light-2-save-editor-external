include(FetchContent)

# zlib shared options
set(ZLIB_USE_STATIC_LIBS ON)

# boost shared options
set(Boost_USE_STATIC_LIBS ON)
# Boost 1.84 targets Windows 10 API by default
add_compile_definitions(BOOST_USE_WINAPI_VERSION=0x601)
# Target Windows 7
add_compile_definitions(WINVER=0x601 _WIN32_WINNT=0x601)

# Add libraries to project
add_subdirectory(zlib)
add_subdirectory(boost)
add_subdirectory(cereal)
add_subdirectory(msgpack)
add_subdirectory(wxwidgets)
add_subdirectory(rapidcsv)
add_subdirectory(steamworks-sdk)
