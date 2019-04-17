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

    ./configure --disable-video --disable-speex-aec --disable-l16-codec --disable-speex-codec --disable-sdl --disable-openh264 --disable-v4l2 --disable-opus --disable-opencore-amr --disable-ssl  --disable-libyuv --disable-libwebrtc --disable-bcg729 --disable-sound --disable-resample --disable-shared --prefix=${PACKAGE_DIR}
    ${COMMAND_MAKE} dep
    ${COMMAND_MAKE}
    ${COMMAND_MAKE} install
}

build
