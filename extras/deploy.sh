#!/bin/sh

set -e


PROJECT_DIR="E:/Jenkins/pjproject"
echo "${PROJECT_DIR}"

PATH=/usr/bin:$PATH

export PATH="${PATH}"
MINGW_HOME="C:/msys32/mingw32"
PACKAGE_DIR="${PROJECT_DIR}\dist"
function build(){
    cd ${PROJECT_DIR}

    ./configure --disable-speex-aec --disable-l16-codec --disable-speex-codec --disable-opencore-amr  --disable-v4l2 ${PACKAGE_DIR}
    make dep
    make
    make install
}

build