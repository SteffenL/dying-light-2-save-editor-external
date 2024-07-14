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
    set(SINGLE_ARGS NAME URL HASH PATCH_FILE)
    set(MULTI_ARGS DEPENDS CMAKE_CACHE_ARGS)
    cmake_parse_arguments(SP "" "${SINGLE_ARGS}" "${MULTI_ARGS}" ${ARGN})

    list(APPEND EP_ARGS
        ${SP_NAME}
    )

    if(SP_DEPENDS)
        list(APPEND EP_ARGS DEPENDS ${SP_DEPENDS})
    endif()

    list(APPEND EP_ARGS
        URL ${SP_URL}
        URL_HASH ${SP_HASH}
        DOWNLOAD_EXTRACT_TIMESTAMP TRUE
    )

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

    list(APPEND EP_ARGS CMAKE_CACHE_ARGS ${SP_SHARED_CMAKE_CACHE_ARGS})
    list(APPEND EP_ARGS CMAKE_CACHE_ARGS ${SP_CMAKE_CACHE_ARGS})

    get_directory_property(SP_COMPILE_DEFINITIONS_LIST COMPILE_DEFINITIONS)
    foreach(ITEM IN LISTS SP_COMPILE_DEFINITIONS_LIST)
        set(ITEM "-D${ITEM}")
        string(REPLACE "\\" "\\\\" ITEM "${ITEM}")
        string(REPLACE "\"" "\\\"" ITEM "${ITEM}")
        if(ITEM MATCHES " ")
            set(ITEM "\"${ITEM}\"")
        endif()
        set(SP_CXX_FLAGS "${SP_CXX_FLAGS} ${ITEM}")
    endforeach()
    if(SP_CXX_FLAGS)
        list(APPEND EP_ARGS "-DCMAKE_CXX_FLAGS:STRING=${SP_CXX_FLAGS}")
    endif()

    message("EP_ARGS = ${EP_ARGS}")
    ExternalProject_Add(${EP_ARGS})
endfunction()
