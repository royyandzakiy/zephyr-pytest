# tests/firmware_update/CMakeLists.txt

cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(mcumgr_hello_test)

# Same switch as the app. The pytest side rebuilds this with UPDATED.
# zephyr_get, not set(CACHE): under sysbuild the value arrives in the image's
# sysbuild cache as <image>_FIRMWARE_VERSION, and only zephyr_get looks there.
# A plain -DFIRMWARE_VERSION=... on a non-sysbuild build still works too.
zephyr_get(FIRMWARE_VERSION)
if(NOT FIRMWARE_VERSION)
  set(FIRMWARE_VERSION "OLD")
endif()
message(STATUS "FIRMWARE_VERSION: ${FIRMWARE_VERSION}")

target_sources(app PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../../src/main.cpp)
target_compile_definitions(app PRIVATE
    FIRMWARE_VERSION="${FIRMWARE_VERSION}"
)
