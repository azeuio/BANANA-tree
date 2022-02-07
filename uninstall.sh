#!/usr/bin/env bash

echo "removing man page (sudo permission will be asked)"
sudo rm -f /usr/local/man/man1/BANANA-tree.1.gz
echo "removing link at $HOME/bin/BANANA-tree"
rm -f $HOME/bin/BANANA-tree
echo "removing folder at $HOME/BANANA-tree"
rm -rfd $HOME/BANANA-tree
