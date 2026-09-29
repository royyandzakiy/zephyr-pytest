cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(hello_world)

# Pick firmware variant: -DFIRMWARE_VERSION=OLD or -DFIRMWARE_VERSION=UPDATED
set(FIRMWARE_VERSION "OLD" CACHE STRING "Firmware variant (OLD or UPDATED)")

target_sources(app PRIVATE src/main.cpp)
target_compile_definitions(app PRIVATE
    FIRMWARE_VERSION="${FIRMWARE_VERSION}"
)
