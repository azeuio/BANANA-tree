#!/usr/bin/env bash

cd $HOME
if git clone https://github.com/azeuio/BANANA-tree.git $HOME/BANANA-tree
then
    echo "linking $HOME/bin/BANANA-tree to BANANA tree executable"
    mkdir -p $HOME/bin/
    ln -sf $HOME/BANANA-tree/BANANA-tree/main.py $HOME/bin/BANANA-tree
    chmod 755 $HOME/BANANA-tree/update.sh
    chmod 755 $HOME/BANANA-tree/uninstall.sh
    chmod 755 $HOME/BANANA-tree/BANANA-tree/main.py
    rm -f $HOME/BANANA-tree/install.sh
    echo "creating man page (sudo permission will be asked)"
    sudo ln -sf $HOME/delivery/BANANA-tree/man_page.gz /usr/local/man/man1/BANANA-tree.1.gz
else
    echo "Error: could not clone repository"
fi
cd -
rm -f ./install.sh
