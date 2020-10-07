#!/bin/bash

if [ "$1" == "add" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver keys.gnupg.net --recv-key $2
elif [ "$1" == "import" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver keys.gnupg.net --import $2
elif [ "$1" == "delete" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver keys.gnupg.net --delete-key $2
elif [ "$1" == "list" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver keys.gnupg.net --list-keys
elif [ "$1" == "refresh" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver keys.gnupg.net --refresh-keys
else
	echo "Unknown command $1"
fi
