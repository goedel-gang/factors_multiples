#!/usr/bin/env zsh
make XFLAGS="-D BOARD_SIZE=${2:-100}" -B $1
