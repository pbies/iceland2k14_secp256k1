cmake_minimum_required(VERSION 3.14)
project(ice_secp256k1 VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Release build by default
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native -funroll-loops")

# Sources (implement these .cpp files to compile the library)
set(SOURCES
    Int.cpp
    IntGroup.cpp
    Point.cpp
    Secp256K1.cpp
    Bloom.cpp
    Timer.cpp
    Keccak.cpp
    sha256.cpp
    sha256sse.cpp
    sha512.cpp
    ripemd160.cpp
    ripemd160sse.cpp
    address_utils.cpp
    ice_secp256k1.cpp
    KeyHunt.cpp
)

add_library(ice_secp256k1 SHARED ${SOURCES})

target_compile_options(ice_secp256k1 PRIVATE
    -msse4.1 -msse4.2 -mavx2
    -Wall -Wno-deprecated-declarations
)

target_include_directories(ice_secp256k1 PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(ice_secp256k1 PRIVATE pthread m)

set_target_properties(ice_secp256k1 PROPERTIES
    OUTPUT_NAME "ice_secp256k1"
    VERSION     ${PROJECT_VERSION}
    SOVERSION   0
)

install(TARGETS ice_secp256k1 LIBRARY DESTINATION lib)
install(FILES
    ice_secp256k1.h
    Int.h
    Point.h
    Secp256K1.h
    Bloom.h
    Timer.h
    Keccak.h
    sha256.h
    sha512.h
    ripemd160.h
    sha256sse.h
    IntGroup.h
    KeyHunt.h
    address_utils.h
    DESTINATION include/ice_secp256k1
)
