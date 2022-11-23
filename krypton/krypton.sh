#!/bin/bash

MAXLEVEL=7

function change_password {
    sed -i "$(expr $level + 1) c\\krypton$level\:$password" krypton_pass
}

if [ $# -eq 0 -o $# -eq 1 ]
then
    echo "Error - Invalid usage"
    echo "Syntax : $0 connect/store level_number"
    exit 1
fi

if [ ! -f krypton_pass ]
then
    echo "Error - Password file 'krypton_pass' doesn't exist"
    echo -n "Create password file? (y/n) "
    read choice
    
    if [ $choice == 'y' ]
    then
        echo "krypton1:KRYPTONISGREAT" >krypton_pass
        for (( i = 2; i <= $MAXLEVEL; i++ ))
        do
            echo "krypton$i:" >>krypton_pass
        done
    else
        exit 1
    fi
fi

if [ $1 == "connect" ]
then
    level=$2
    user_pass=($(grep "krypton$level:" krypton_pass | tr ":" "\n"))
    password=${user_pass[1]}

    if [ -z $password ]
    then
        echo "Error - Password not stored"
        echo "Achieve the previous level first"
        exit 1
    fi
    while [ $level -le $MAXLEVEL ]
    do
        sshpass -p "$password" ssh krypton$level@krypton.labs.overthewire.org -p2231
        
        level=$(expr $level + 1)
        echo -n "Do you have the password in the clipboard? (y/n) "
        read have_password
        
        if [ $have_password == "y" ]
        then
            password=$(xclip)
            change_password
        else
            break
        fi
    done
elif [ $1 == "store" ]
then
    level=$2
    echo -n "Enter the password: "
    read password
    change_password
else
    echo "Error - Invalid usage"
    echo "Syntax : $0 connect/store level_number"
    exit 1
fi
