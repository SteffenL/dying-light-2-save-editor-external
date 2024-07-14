subprojects_add(
    NAME msgpack
    URL https://github.com/msgpack/msgpack-c/releases/download/cpp-6.1.1/msgpack-cxx-6.1.1.tar.gz
    HASH SHA256=5fd555742e37bbd58d166199e669f01f743c7b3c6177191dd7b31fb0c37fa191
    CMAKE_CACHE_ARGS
        -DCMAKE_POLICY_DEFAULT_CMP0077:STRING=NEW
        -DMSGPACK_CXX20:BOOL=ON
        -DMSGPACK_BUILD_DOCS:BOOL=OFF
        -DMSGPACK_USE_BOOST:BOOL=OFF
)
