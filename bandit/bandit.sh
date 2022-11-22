#!/bin/bash

function change_password {
  sed -i "$(expr $level + 1) c\\bandit$level\:$password" bandit_pass
}

if [ $# -eq 0 -o $# -eq 1 ]; then
  echo "Error - Invalid usage"
  echo "Syntax : $0 connect/store level_number"
  exit 1
fi

if [ ! -f bandit_pass ]; then
  echo "Error - Password file 'bandit_pass' doesn't exist"
  echo -n "Create password file? (y/n) "
  read choice

  if [ $choice == 'y' ]; then
    echo "bandit0:bandit0" >bandit_pass
    for ((i = 0; i < 34; i++)); do
      echo "bandit$i:" >>bandit_pass
    done
  else
    exit 1
  fi
fi

if [ $1 == "connect" ]; then
  level=$2

  if [ -z $(grep "bandit$level" bandit_pass) ]; then
    echo "Error - Password not stored"
    echo "Achieve the previous level first"
    exit 1
  fi
  while [ $level -le 33 ]; do
    user_pass=($(grep "bandit$level" bandit_pass | tr ":" "\n"))
    pass=${user_pass[1]}
    sshpass -p "$pass" ssh bandit$level@bandit.labs.overthewire.org -p2220

    level=$(expr $level + 1)
    echo -n "Do you have the password in the clipboard? (y/n) "
    read have_password

    if [ $have_password == "y" ]; then
      password=$(xclip)
      change_password
    else
      break
    fi
  done
elif [ $1 == "store" ]; then
  level=$2
  echo -n "Enter the password: "
  read password
  change_password
else
  echo "Error - Invalid usage"
  echo "Syntax : $0 connect/store level_number"
  exit 1
fi
