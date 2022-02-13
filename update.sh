#!/usr/bin/env bash


if [ "$BANANATREE" == "" ];
then
    echo "hi"
    command="$(realpath $(dirname $0))/install.sh"
    echo $command
    $command
    source $HOME/.bashrc
    exit $?
fi

original_pwd=$PWD
if ! cd $BANANATREE;
then
    echo "Folder '$BANANATREE' doesn't exists."
    echo -n "Please install the program following the README instructions "
    echo "at https://github.com/azeuio/BANANA-tree"
    exit 1
fi
git_pull_output=$(git pull origin main)
if [ "$git_pull_output" != "Already up to date." ]
then
    $(realpath $(dirname $0))/install.sh
fi
cd $original_pwd