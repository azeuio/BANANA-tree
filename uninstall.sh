#!/usr/bin/env bash

banana_tree_folder="$BANANATREE"

echo "Removing man page (sudo permission will be needed)"
sudo rm -f /usr/local/man/man1/BANANA-tree.1.gz

echo "Removing link at $HOME/bin/BANANA-tree"
rm -f $HOME/bin/BANANA-tree

echo "Unsetting environment variable"
unset BANANATREE
grep -ve "export BANANATREE=*" $HOME/.bashrc > /tmp/tmp_file58008707
cat /tmp/tmp_file58008707 > $HOME/.bashrc
source $HOME/.bashrc
rm /tmp/tmp_file58008707

echo "Removing folder at $banana_tree_folder"
rm -rfd $banana_tree_folder
