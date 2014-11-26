#!/bin/bash

base='amd64'
declare -a architectures=('i386' 'arm64' 'armel' 'armhf' 'powerpc' 's390x')
declare -a ubuntuarchive=('amd64' 'i386')

for arch in "${architectures[@]}"
do
	rm -fr $arch
	mkdir $arch
	cp $base/* $arch/
	find $arch -type f | xargs sed -i "s/$base/$arch/g"
	if [[ ! ${ubuntuarchive[*]} =~ $arch ]]
	then
		find $arch -type f | xargs sed -ri "s;(archive|security).ubuntu.com/ubuntu;ports.ubuntu.com/ubuntu-ports;g"
	fi
done
