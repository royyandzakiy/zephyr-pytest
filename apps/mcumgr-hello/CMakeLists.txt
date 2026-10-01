cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(mcumgr_hello)

# Firmware variant, OLD (default) or UPDATED: -DFIRMWARE_VERSION=UPDATED
# zephyr_get() so the value also reaches the app under sysbuild.
zephyr_get(FIRMWARE_VERSION)
if(NOT FIRMWARE_VERSION)
  set(FIRMWARE_VERSION "OLD")
endif()
message(STATUS "FIRMWARE_VERSION: ${FIRMWARE_VERSION}")

target_sources(app PRIVATE src/main.cpp)
target_compile_definitions(app PRIVATE
    FIRMWARE_VERSION="${FIRMWARE_VERSION}"
)
