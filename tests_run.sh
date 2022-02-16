#!/usr/bin/env bash

if [ "$0" == "$(realpath $0)" ];
then
    path="BANANA-tree --test"
else
    path="$0"
fi

if [ $# -gt 2 ];
then
    echo "$path: Invalid number of arguments"
    echo "Try '$path --help' for more information"
    exit 1
fi
if [ "$(echo $* | grep -w -- --help)" != "" ];
then
    echo "Usage: $path [branch] [--help]"
    echo ""
    printf "branch\tcoverage report will use branch coverage.\n"
    printf "\0--help\tDisplays this help and exit.\n"
    exit 0
fi
a="$(pip list | grep coverage)"
if [ "$a" == "" ];
then
    printf "\e[31;1mPackage coverage was not found.\e[m\n" 1>&2
    echo "Tests will be run but no coverage report will be generated."
    printf "Run this command '\e[33mpip install coverage\e[m' to have a coverage report generated\n"
    $BANANATREE/BANANA_tree/tests_run.py
elif [ $# -eq 0 ] || [ "$1" == "line" ];
then
    coverage run --omit=*tests/*,*tests_run* $BANANATREE/BANANA_tree/tests_run.py
    coverage report
elif [ $# -gt 1 ] || [ "$1" == "branch" ];
then
    coverage run --omit=*tests/*,*tests_run* --branch\
    $BANANATREE/BANANA_tree/tests_run.py
    coverage report
else
    echo "Invalid parameter"
    echo "Try '$path --help' for more information"
fi