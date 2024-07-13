set(BUILD_TESTS OFF)
set(BUILD_DOC OFF)
set(BUILD_SANDBOX OFF)
set(SKIP_PERFORMANCE_COMPARISON ON)

FetchContent_Declare(
    cereal
    URL https://github.com/USCiLab/cereal/archive/refs/tags/v1.3.2.tar.gz
    URL_HASH SHA256=16a7ad9b31ba5880dac55d62b5d6f243c3ebc8d46a3514149e56b5e7ea81f85f
)

FetchContent_MakeAvailable(cereal)
