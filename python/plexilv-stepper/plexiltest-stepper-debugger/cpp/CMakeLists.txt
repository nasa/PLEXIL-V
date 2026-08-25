cmake_minimum_required(VERSION 3.15)
project(PlexilDebuggerProject LANGUAGES CXX C)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT DEFINED ENV{PLEXIL_HOME})
    message(FATAL_ERROR "Please set the PLEXIL_HOME environment variable before running CMake.")
endif()

set(PLEXIL_INCLUDE_DIR "$ENV{PLEXIL_HOME}/include")
set(PLEXIL_SRC_DIR "$ENV{PLEXIL_HOME}/src")
set(PLEXIL_LIB_DIR "$ENV{PLEXIL_HOME}/lib")

find_library(PLEXIL_EXEC_LIB NAMES PlexilExec PATHS ${PLEXIL_LIB_DIR} REQUIRED)
find_library(PLEXIL_XML_LIB NAMES PlexilXmlParser PATHS ${PLEXIL_LIB_DIR} REQUIRED)
find_library(PLEXIL_PUGI_LIB NAMES pugixml PATHS ${PLEXIL_LIB_DIR} REQUIRED)
find_library(PLEXIL_INTFC_LIB NAMES PlexilIntfc PATHS ${PLEXIL_LIB_DIR} REQUIRED)
find_library(PLEXIL_EXPR_LIB NAMES PlexilExpr PATHS ${PLEXIL_LIB_DIR} REQUIRED)
find_library(PLEXIL_VALUE_LIB NAMES PlexilValue PATHS ${PLEXIL_LIB_DIR} REQUIRED)
find_library(PLEXIL_UTILS_LIB NAMES PlexilUtils PATHS ${PLEXIL_LIB_DIR} REQUIRED)
find_library(PLEXIL_APP_LIB NAMES PlexilAppFramework PATHS ${PLEXIL_LIB_DIR} REQUIRED)

set(PLEXIL_LIBRARIES
  ${PLEXIL_EXEC_LIB} ${PLEXIL_INTFC_LIB} ${PLEXIL_EXPR_LIB}
  ${PLEXIL_VALUE_LIB} ${PLEXIL_APP_LIB} ${PLEXIL_XML_LIB}
  ${PLEXIL_PUGI_LIB} ${PLEXIL_UTILS_LIB}
)

set(PLEXIL_INCLUDE_DIRS
  ${PLEXIL_SRC_DIR}/exec
  ${PLEXIL_SRC_DIR}/expr
  ${PLEXIL_SRC_DIR}/intfc
  ${PLEXIL_SRC_DIR}/utils
  ${PLEXIL_INCLUDE_DIR}
)

# Tell MacOS and Linux to look for dependencies in the same folder as loaded dylib
if(APPLE)
    set(CMAKE_INSTALL_RPATH "@loader_path")
elseif(UNIX)
    set(CMAKE_INSTALL_RPATH "$ORIGIN")
endif()


# Build libraries
add_library(StateInfoListener SHARED StateInfoListener.cc)
target_include_directories(StateInfoListener PUBLIC ${PLEXIL_INCLUDE_DIRS})
target_link_libraries(StateInfoListener PUBLIC ${PLEXIL_LIBRARIES})

add_library(PlexilStepper SHARED Stepper.cc StepperPlexilInterface.cc StepperPythonInterface.cc)
target_link_libraries(PlexilStepper PUBLIC StateInfoListener)

install(TARGETS StateInfoListener PlexilStepper DESTINATION plexiltest/cext)
