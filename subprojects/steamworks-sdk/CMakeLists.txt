set(URL gs://langnes-build-resources/libraries/steamworks-sdk/steamworks_sdk_159.zip)
#set(URL gs://${GCLOUD_BUCKET}/libraries/steamworks-sdk/steamworks_sdk_159.zip)

set(HASH 38589f5780029984f5bb618f34e216121af9ebd2847a44709d11f4728885007d)
set(LOCAL_FILE ${CMAKE_CURRENT_BINARY_DIR}/steamworks_sdk_159.zip)
set(EXTRACT_DIR ${CMAKE_CURRENT_BINARY_DIR})
set(SDK_DIR ${EXTRACT_DIR}/sdk)

subprojects_add(
    NAME steamworks_sdk
    DOWNLOAD_COMMAND ${CMAKE_COMMAND} -DURL=${URL} -DHASH=${HASH} -DLOCAL_FILE=${LOCAL_FILE} -DEXTRACT_DIR=${EXTRACT_DIR} -P ${CMAKE_CURRENT_SOURCE_DIR}/download.cmake
    NO_BUILD
    CMAKE_CACHE_ARGS
        -DBUILD_TESTS:BOOL=OFF
        -DBUILD_DOC:BOOL=OFF
        -DBUILD_SANDBOX:BOOL=OFF
        -DSKIP_PERFORMANCE_COMPARISON:BOOL=ON
)

#file(GENERATE OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/install.cmake CONTENT [[
install(FILES steamworks-config.cmake DESTINATION lib/cmake/steamworks)
install(DIRECTORY ${SDK_DIR}/public/steam DESTINATION include)

set(X86_64_ARCHS AMD64 x86_64)

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    install(FILES ${SDK_DIR}/redistributable_bin/osx/libsteam_api.dylib lib)
elseif(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    if(CMAKE_SYSTEM_PROCESSOR IN_LIST X86_64_ARCHS)
        install(FILES ${SDK_DIR}/redistributable_bin/linux64/libsteam_api.so DESTINATION lib)
    else()
        install(FILES ${SDK_DIR}/redistributable_bin/linux32/libsteam_api.so DESTINATION lib)
    endif()
elseif(CMAKE_SYSTEM_NAME STREQUAL "Windows")
    if(CMAKE_SYSTEM_PROCESSOR IN_LIST X86_64_ARCHS)
        install(FILES ${SDK_DIR}/redistributable_bin/win64/steam_api64.dll DESTINATION bin)
        install(FILES ${SDK_DIR}/redistributable_bin/win64/steam_api64.lib DESTINATION lib)
    else()
        install(FILES ${SDK_DIR}/redistributable_bin/steam_api.dll DESTINATION bin)
        install(FILES ${SDK_DIR}/redistributable_bin/steam_api.lib DESTINATION lib)
    endif()
endif()
#]])
