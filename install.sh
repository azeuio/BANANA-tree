#!/usr/bin/env bash

cd $HOME
if git clone https://github.com/azeuio/BANANA-tree.git $HOME/BANANA-tree
then
    echo "coping BANANA tree to $HOME/bin/BANANA-tree"
    mkdir -p $HOME/bin/
    ls -sf $HOME/BANANA-tree/main.py BANANA-tree
    echo "adding manpage"
    # sudo cp $HOME/norminette/manpage.1.gz /usr/share/man/man1/norminette.1.gz
    # sudo cp $HOME/norminette/manpage.1f.gz /usr/share/man/man1/norminette.1f.gz
else
    echo "Error: could not clone repository"
fi
