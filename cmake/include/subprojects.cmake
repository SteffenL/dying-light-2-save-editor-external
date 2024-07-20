include(ExternalProject)
find_package(Git REQUIRED)

macro(subprojects_init)
    set(SP_ROOT_DIR ${CMAKE_BINARY_DIR}/subprojects)
    set_directory_properties(PROPERTIES EP_BASE ${SP_ROOT_DIR})
endmacro()

macro(subprojects_add_shared_cache_args)
    list(APPEND SP_SHARED_CMAKE_CACHE_ARGS ${ARGV})
endmacro()

function(subprojects_add)
    set(OPTIONS NO_CONFIGURE NO_BUILD)
    set(SINGLE_ARGS NAME URL HASH PATCH_FILE)
    set(MULTI_ARGS DEPENDS DOWNLOAD_COMMAND CMAKE_CACHE_ARGS)
    cmake_parse_arguments(SP "${OPTIONS}" "${SINGLE_ARGS}" "${MULTI_ARGS}" ${ARGN})

    list(APPEND EP_ARGS ${SP_NAME})

    if(SP_DEPENDS)
        list(APPEND EP_ARGS DEPENDS ${SP_DEPENDS})
    endif()

    if(SP_URL)
        list(APPEND EP_ARGS URL ${SP_URL})
    endif()

    if(SP_URL)
        list(APPEND EP_ARGS URL_HASH ${SP_HASH})
    endif()

    list(APPEND EP_ARGS DOWNLOAD_EXTRACT_TIMESTAMP TRUE)

    if(SP_PATCH_FILE)
        cmake_path(RELATIVE_PATH SP_ROOT_DIR BASE_DIRECTORY ${CMAKE_SOURCE_DIR} OUTPUT_VARIABLE SP_RELATIVE_ROOT_DIR)
        list(APPEND EP_ARGS
            PATCH_COMMAND
                ${GIT_EXECUTABLE}
                apply
                --directory=${SP_RELATIVE_ROOT_DIR}/Source/${SP_NAME}
                ${SP_PATCH_FILE}
        )
    endif()

    if(SP_DOWNLOAD_COMMAND)
        list(APPEND EP_ARGS DOWNLOAD_COMMAND ${SP_DOWNLOAD_COMMAND})
    endif()

    if(SP_NO_CONFIGURE)
        list(APPEND EP_ARGS CONFIGURE_COMMAND "")
    endif()

    if(SP_NO_BUILD)
        list(APPEND EP_ARGS BUILD_COMMAND "")
    endif()

    if(SP_NO_INSTALL)
        list(APPEND EP_ARGS INSTALL_COMMAND "")
    endif()

    list(APPEND EP_ARGS CMAKE_CACHE_ARGS
        ${SP_SHARED_CMAKE_CACHE_ARGS}
        ${SP_CMAKE_CACHE_ARGS}
    )

    get_directory_property(SP_COMPILE_DEFINITIONS_LIST COMPILE_DEFINITIONS)
    foreach(FLAG IN LISTS SP_COMPILE_DEFINITIONS_LIST)
        string(APPEND SP_CXX_FLAGS " [===[-D${FLAG}]===]")
    endforeach()
    if(SP_CXX_FLAGS)
        list(APPEND EP_ARGS "-DCMAKE_CXX_FLAGS:STRING=${SP_CXX_FLAGS}")
    endif()

    foreach(ARG IN LISTS EP_ARGS)
        string(APPEND EP_ARGS_ESCAPED " [====[${ARG}]====]")
    endforeach()

    cmake_language(EVAL CODE "ExternalProject_Add(${EP_ARGS_ESCAPED})")
endfunction()
