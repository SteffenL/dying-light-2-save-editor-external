set(BUILD_TESTS OFF)
set(BUILD_DOC OFF)
set(BUILD_SANDBOX OFF)
set(SKIP_PERFORMANCE_COMPARISON ON)

set(PRIVATE_LIBS_URL gs://langnes-build-resources/libraries)

FetchContent_Declare(
    steamworks-sdk
    URL ${PRIVATE_LIBS_URL}/steamworks-sdk/steamworks_sdk_159.zip
    URL_HASH SHA256=38589f5780029984f5bb618f34e216121af9ebd2847a44709d11f4728885007d
    DOWNLOAD_COMMAND
)

FetchContent_MakeAvailable(steamworks-sdk)
