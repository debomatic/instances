#!/bin/bash

if [ "$1" == "add" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver pgp.mit.edu --recv-key $2
elif [ "$1" == "import" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver pgp.mit.edu --import $2
elif [ "$1" == "delete" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver pgp.mit.edu --delete-key $2
elif [ "$1" == "list" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver pgp.mit.edu --list-keys
elif [ "$1" == "refresh" ]; then
	gpg --no-default-keyring --keyring $PWD/../keyring/debomatic.gpg --keyserver pgp.mit.edu --refresh-keys
else
	echo "Unknown command $1"
fi
