#!/usr/bin/env bash

cd $HOME/BANANA-tree
git_pull_output=$(git pull)
if [ "$git_pull_output" != "Already up to date." ]
then
    echo "linking BANANA tree executable to $HOME/bin/BANANA-tree"
    mkdir -p $HOME/bin/
    ln -sf $HOME/BANANA-tree/main.py $HOME/bin/BANANA-tree
    echo "creating man page (sudo permission will be asked)"
	sudo rm -f /usr/local/man/man1/BANANA-tree.1.gz
    sudo ln -sf $HOME/delivery/BANANA-tree/man_page.gz /usr/local/man/man1/BANANA-tree.1.gz
fi
cd -