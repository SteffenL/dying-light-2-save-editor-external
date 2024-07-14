set(steamworks_ROOT ${CMAKE_CURRENT_LIST_DIR}/../../../)
find_path(steamworks_INCLUDE_DIR NAMES steam_api.h HINTS ${steamworks_ROOT}/include/steam)

if(NOT steamworks_INCLUDE_DIR)
    message(FATAL_ERROR "Include directory not found")
endif()

add_library(steamworks SHARED IMPORTED)
target_include_directories(steamworks INTERFACE ${steamworks_ROOT}/include)
if(WIN32)
    if(CMAKE_SIZEOF_VOID_P GREATER 4)
        set_target_properties(steamworks PROPERTIES
            IMPORTED_LOCATION ${steamworks_ROOT}/bin/steam_api64.dll
            IMPORTED_IMPLIB ${steamworks_ROOT}/lib/steam_api64.lib
        )
    else()
        set_target_properties(steamworks PROPERTIES
            IMPORTED_LOCATION ${steamworks_ROOT}/bin/steam_api.dll
            IMPORTED_IMPLIB ${steamworks_ROOT}/lib/steam_api.lib
        )
    endif()
elseif(APPLE)
    set_target_properties(steamworks PROPERTIES
        IMPORTED_LOCATION ${steamworks_ROOT}/lib/libsteam_api.dylib
    )
elseif(CMAKE_SYSTEM_NAME MATCHES "Linux")
    if(CMAKE_SIZEOF_VOID_P GREATER 4)
        set_target_properties(steamworks PROPERTIES
            IMPORTED_LOCATION ${steamworks_ROOT}/lib/libsteam_api.so
        )
    else()
        set_target_properties(steamworks PROPERTIES
            IMPORTED_LOCATION ${steamworks_ROOT}/lib/libsteam_api.so
        )
    endif()
endif()
