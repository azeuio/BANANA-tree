#!/usr/bin/env bash

cd $HOME
if git clone https://github.com/azeuio/BANANA-tree.git $HOME/BANANA-tree
then
    echo "linking BANANA tree executable to $HOME/bin/BANANA-tree"
    mkdir -p $HOME/bin/
    ln -sf $HOME/BANANA-tree/main.py $HOME/bin/BANANA-tree
    echo "creating man page (sudo permission will be asked)"
    sudo ln -sf $HOME/delivery/BANANA-tree/man_page.gz /usr/local/man/man1/BANANA-tree.1.gz
else
    echo "Error: could not clone repository"
fi
cd -
rm ./install.sh
