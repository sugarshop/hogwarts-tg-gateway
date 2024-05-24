#!/bin/sh

CURDIR=$(cd $(dirname $0); pwd)

exec python "$CURDIR/main.py"