add_compile_definitions(
    # Boost 1.84 targets Windows 10 API by default
    BOOST_USE_WINAPI_VERSION=0x601
    # Target Windows 7
    WINVER=0x601
    _WIN32_WINNT=0x601
)

subprojects_add_shared_cache_args(
    -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
    -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_BINARY_DIR}/install
    -DZLIB_USE_STATIC_LIBS:BOOL=ON
    -DBoost_USE_STATIC_LIBS:BOOL=ON
)

# Add libraries to project
#add_subdirectory(zlib)
#add_subdirectory(boost)
#add_subdirectory(cereal)
#add_subdirectory(msgpack)
#add_subdirectory(wxwidgets)
#add_subdirectory(rapidcsv)
add_subdirectory(steamworks-sdk)
