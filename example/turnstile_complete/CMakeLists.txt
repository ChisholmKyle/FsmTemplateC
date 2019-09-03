cmake_minimum_required (VERSION 3.9)
project (turnstile)

file (
    GLOB
    EXAMPLE_SOURCE_FILES
    "${PROJECT_SOURCE_DIR}/*.h"
    "${PROJECT_SOURCE_DIR}/*.c")

add_executable (turnstile ${EXAMPLE_SOURCE_FILES})

target_compile_options(
    turnstile
    PRIVATE
    -Wall)
target_include_directories(
    turnstile
    PRIVATE
    ${PROJECT_SOURCE_DIR}/)
