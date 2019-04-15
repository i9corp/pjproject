#!/bin/sh

set -e


PROJECT_DIR="E:/Jenkins/pjproject"
echo "${PROJECT_DIR}"

PATH=/usr/bin:$PATH

export PATH="${PATH}"
MINGW_HOME="C:/msys32/mingw32"
MINGW_BIN="${MINGW_HOME}/bin"
COMMAND_MAKE="${MINGW_BIN}/mingw32-make.exe"
PACKAGE_DIR="${PROJECT_DIR}\dist"
function build(){
    cd ${PROJECT_DIR}

    ./configure --disable-speex-aec --disable-l16-codec --disable-speex-codec --disable-opencore-amr  --disable-v4l2 --prefix=${PACKAGE_DIR}
    ${COMMAND_MAKE} dep
    ${COMMAND_MAKE}
    ${COMMAND_MAKE} install
}

build