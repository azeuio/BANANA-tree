#!/usr/bin/env bash

printf "\e[1mSetting environment variable\e[m\n"
unset BANANATREE
grep -ve "export BANANATREE=*" $HOME/.bashrc > /tmp/tmp_file58008707
cat /tmp/tmp_file58008707 > $HOME/.bashrc
echo "export BANANATREE='`realpath $(dirname "$0")`'" >> $HOME/.bashrc
source $HOME/.bashrc
rm /tmp/tmp_file58008707

printf "\e[1mLinking $HOME/bin/BANANA-tree to BANANA tree executable\e[m\n"
mkdir -p $HOME/bin/
ln -sf $BANANATREE/BANANA_tree/main.py $HOME/bin/BANANA-tree
chmod 755 $BANANATREE/update.sh
chmod 755 $BANANATREE/uninstall.sh
chmod 755 $BANANATREE/BANANA_tree/main.py

printf "\e[1mCreating man page (sudo permission will be needed)\e[m\n"
sudo ln -sf $BANANATREE/man_page.gz /usr/local/man/man1/BANANA-tree.1.gz

printf "\e[32;1mInstallation finished.\e[m\n"
echo "Start a new terminal to be able to use the command 'BANANA-tree'"