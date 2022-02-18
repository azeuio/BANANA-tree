#!/usr/bin/env bash

ask_for_confirmation()
{
    while [ "$input" != "y" ] && [ "$input" != "n" ];
    do
        read  -n 1 -p "$1 (y/n) " input
        echo
    done
    if [ "$input" == "y" ];
    then
        return 0
    fi
    return 1
}

printf "Setting environment variable\n"
unset BANANATREE
echo -n .
cp $HOME/.bashrc $HOME/.bashrc.backup
grep -ve "export BANANATREE=*" $HOME/.bashrc > /tmp/tmp_file58008707
echo -n .
cat /tmp/tmp_file58008707 > $HOME/.bashrc
echo -n .
echo "export BANANATREE='`realpath $(dirname "$0")`'" >> $HOME/.bashrc
echo -n .
source $HOME/.bashrc
rm -f /tmp/tmp_file58008707
echo " OK"

printf "Linking $HOME/bin/BANANA-tree to BANANA tree executable\n"
mkdir -p $HOME/bin/
echo -n .
ln -sf $BANANATREE/BANANA_tree/main.py $HOME/bin/BANANA-tree
echo -n .
chmod 755 $BANANATREE/update.sh
echo -n .
chmod 755 $BANANATREE/uninstall.sh
echo -n .
chmod 755 $BANANATREE/BANANA_tree/main.py
echo " OK"

printf "\e[1mFor the following steps, sudo permission is required\e[m\n"
sudo echo -n ""
if (ask_for_confirmation "Create man page ?");
then
    echo -n .
    sudo mkdir -p /usr/local/man/man1/
    echo -n .
    sudo ln -sf $BANANATREE/man_page.gz /usr/local/man/man1/BANANA-tree.1.gz
    echo . ok
fi
if (ask_for_confirmation "Add auto-completion for this command ?");
then
    echo -n .
    sudo mkdir -p /usr/share/bash-completion/completions/
    sudo rm -f /usr/share/bash-completion/completions/BANANA-tree
    echo -n .
    sudo cp auto_completion /usr/share/bash-completion/completions/BANANA-tree
    echo . ok
fi
printf "\e[32;1mInstallation finished.\e[m\n"
echo "Start a new terminal to be able to use the command 'BANANA-tree'"