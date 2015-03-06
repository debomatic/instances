#!/bin/bash

for chroot in `schroot -l | perl -ne '/chroot:(\S+-debomatic)/ && print "$1\n"'`
do
        [[ $chroot =~ [^-]+-([^-]+)-debomatic ]]
        arch=${BASH_REMATCH[1]}
        sbuild-update -udcar --arch=$arch $chroot
done
