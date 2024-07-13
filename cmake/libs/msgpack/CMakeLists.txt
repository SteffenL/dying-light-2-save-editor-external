set(CMAKE_POLICY_DEFAULT_CMP0077 NEW)
set(MSGPACK_CXX20 ON)
set(MSGPACK_BUILD_DOCS OFF)
set(MSGPACK_USE_BOOST OFF)

FetchContent_Declare(
    msgpack
    URL https://github.com/msgpack/msgpack-c/releases/download/cpp-6.1.1/msgpack-cxx-6.1.1.tar.gz
    URL_HASH SHA256=5fd555742e37bbd58d166199e669f01f743c7b3c6177191dd7b31fb0c37fa191
)

FetchContent_MakeAvailable(msgpack)
