subprojects_add(
    NAME cereal
    URL https://github.com/USCiLab/cereal/archive/refs/tags/v1.3.2.tar.gz
    HASH SHA256=16a7ad9b31ba5880dac55d62b5d6f243c3ebc8d46a3514149e56b5e7ea81f85f
    CMAKE_CACHE_ARGS
        -DBUILD_TESTS:BOOL=OFF
        -DBUILD_DOC:BOOL=OFF
        -DBUILD_SANDBOX:BOOL=OFF
        -DSKIP_PERFORMANCE_COMPARISON:BOOL=ON
)
