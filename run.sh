#!/bin/bash

docker run -it \
    -v $PWD:/mnt \
    --privileged \
    angr/angr
