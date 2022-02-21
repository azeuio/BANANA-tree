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
    echo "Usage: $path [OPTION]..."
    echo ""
    printf "--branch\tcoverage report will use branch coverage.\n"
    echo "OPTION:"
    printf "\t--coverage\n"
    printf "\t\tDisplays coverage report after executing the tests.\n"
    printf "\t--help\n"
    printf "\t\tDisplays this help and exit.\n"
    printf "\t--only-coverage\n"
    printf "\t\tOnly displey the coverage without rerunning the tests.\n"
    exit 0
fi

if [ "$(echo $* | grep -w -- --only-coverage)" != "" ];
then
    cd $BANANATREE
    coverage report -m
    cd - > /dev/null
    exit 0
fi

coverage_installed="$(pip list | grep coverage)"
if [ "$coverage_installed" == "" ];
then
    printf "\e[31;1mPackage coverage was not found.\e[m\n" 1>&2
    echo "Tests will be run but no coverage report will be generated."
    printf "Run this command '\e[33mpip install coverage\e[m' to have a coverage report generated\n"
    $BANANATREE/BANANA_tree/tests_run.py
    exit 1
fi

if [ "$(echo $* | grep -w -- --branch)" != "" ];
then
    coverage run --omit=*tests/*,*tests_run* --branch\
    $BANANATREE/BANANA_tree/tests_run.py
else
    coverage run --omit=*tests/*,*tests_run* $BANANATREE/BANANA_tree/tests_run.py
fi

if [ "$(echo $* | grep -w -- --coverage)" != "" ];
then
    cd $BANANATREE
    coverage report -m
    cd - > /dev/null
fi
