import base64
import paramiko

from pwn import *

host = 'bandit.labs.overthewire.org'
port = 2220
context.log_level = 'warn'
p = log.progress('Solving level: ', level=30)
passwords = {0: 'bandit0'}


def connectToLevel(level):
    return ssh('bandit{}'.format(level), host=host, password=passwords[level], port=port)


def execute_command(shell, command):
    return shell[command].decode('utf-8')


def solve_one_command(level, command):
    shell = connectToLevel(level)
    passwords[level+1] = execute_command(shell, command)
    shell.close()


def solve_bandit(level):
    if level == 0:
        # Level 0
        p.status('0')
        solve_one_command(0, 'cat readme')
    elif level == 1:
        # Level 1
        p.status('1')
        solve_one_command(1, 'cat ./-')
    elif level == 2:
        # Level 2
        p.status('2')
        solve_one_command(2, 'cat spaces\ in\ this\ filename')
    elif level == 3:
        # Level 3
        p.status('3')
        solve_one_command(3, 'cat `find inhere -name ".*"`')
    elif level == 4:
        # Level 4
        p.status('4')
        solve_one_command(
            4, 'cat `find inhere -not -executable -exec sh -c \'file -b {} | grep "text$" 1>/dev/null\' \; -print`')
    elif level == 5:
        # Level 5
        p.status('5')
        solve_one_command(5, 'cat `find inhere/ -size 1033c -not -executable`')
    elif level == 6:
        # Level 6
        p.status('6')
        solve_one_command(
            6, 'cat `find / -user bandit7 -group bandit6 2>/dev/null`')
    elif level == 7:
        # Level 7
        p.status('7')
        passwords[8] = execute_command(connectToLevel(
            7), 'grep millionth data.txt').split()[1]
    elif level == 8:
        # Level 8
        p.status('8')
        solve_one_command(8, 'sort data.txt | uniq -u')
    elif level == 9:
        # Level 9
        p.status('9')
        passwords[10] = execute_command(connectToLevel(
            9), 'strings data.txt | grep "========== " | grep -v -E the\|pass\|is').split('==========')[1].strip()
    elif level == 10:
        # Level 10
        p.status('10')
        passwords[11] = execute_command(connectToLevel(
            10), 'cat data.txt | base64 -d').split('The password is ')[1].strip()
    elif level == 11:
        # Level 11
        p.status('11')
        passwords[12] = execute_command(connectToLevel(
            11), 'cat data.txt | tr a-zA-Z n-za-mN-ZA-M').split('The password is ')[1].strip()
    elif level == 12:
        # Level 12
        p.status('12')
        passwords[13] = execute_command(connectToLevel(12), 'cd `mktemp -d` && cp ~/data.txt . && xxd -r data.txt > data.gz \
                                                                && gunzip data.gz && bzip2 -d data && mv data.out data.gz \
                                                                && gunzip data && tar -xvf data && tar -xvf data5.bin \
                                                                && bzip2 -d data6.bin && tar -xvf data6.bin.out \
                                                                && mv data8.bin data8.gz && gunzip data8.gz && cat data8').split('The password is ')[1].strip()
    elif level == 13:
        # Level 13
        p.status('13')
        connectToLevel(13).download_file('sshkey.private')
        passwords[14] = ssh('bandit14', 'bandit.labs.overthewire.org', keyfile='sshkey.private', port=2220)[
            'cat /etc/bandit_pass/bandit14'].decode('utf-8')
    elif level == 14:
        # Level 14
        p.status('14')
        passwords[15] = execute_command(connectToLevel(14), 'echo "{}" | nc localhost 30000'.format(
            passwords[14])).split('Correct!\n')[1].strip()
    elif level == 15:
        # Level 15
        p.status('15')
        passwords[16] = execute_command(connectToLevel(15), 'echo "{}" | openssl s_client -connect localhost:30001 -ign_eof'.format(
            passwords[15])).split('Correct!\n')[1].split('closed')[0].strip()
    elif level == 16:
        # Level 16
        p.status('16')
        sshkey = execute_command(connectToLevel(16), 'echo "{}" | openssl s_client -connect localhost:31790 -ign_eof'.format(
            passwords[16])).split('Correct!\n')[1].split('closed')[0].strip()
        f = open('sshkey_bandit17', 'w').write(sshkey)
        passwords[17] = ssh('bandit17', 'bandit.labs.overthewire.org', keyfile='sshkey_bandit17', port=2220)[
            'cat /etc/bandit_pass/bandit17'].decode('utf-8')
    elif level == 17:
        # Level 17
        p.status('17')
        passwords[18] = execute_command(connectToLevel(
            17), 'diff passwords.new passwords.old | grep "<"').split('< ')[1].strip()
    elif level == 18:
        # Level 18
        p.status('18')
        solve_one_command(18, 'cat readme')
    elif level == 19:
        # Level 19
        p.status('19')
        solve_one_command(19, './bandit20-do cat /etc/bandit_pass/bandit20')
    elif level == 20:
        # Level 20
        p.status('20')
        passwords[21] = execute_command(connectToLevel(20), '(echo "{}" | nc -lvnp 6456 &) && sleep 2 && ./suconnect 6456'.format(
            passwords[20])).split('Password matches, sending next password\n')[1].strip()
    elif level == 21:
        # Level 21
        p.status('21')
        solve_one_command(21, 'cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv')
    elif level == 22:
        # Level 22
        p.status('22')
        solve_one_command(22, 'cat /tmp/8ca319486bfbbc3663ea0fbe81326349')
    elif level == 23:
        # Level 23
        p.status('23')
        solve_one_command(23, 'echo "cat /etc/bandit_pass/bandit24 > /tmp/m4rz3r0 && chmod 777 /tmp/m4rz3r0" > /var/spool/bandit24/foo/m4rz3r0.sh && chmod +x /var/spool/bandit24/foo/m4rz3r0.sh && sleep 30 && cat /tmp/m4rz3r0')
    elif level == 24:
        # Level 24
        p.status('24')
        script = base64.b64encode("""
                #!/bin/bash

                password={}

                for (( i=0; i<10000; i++ ))
                do
                    echo "$password $i"
                done | nc localhost 30002 | grep -v -E pincode\|Wrong\|Correct\|Exiting
                """.format(passwords[24]).encode('utf-8')).decode('utf-8')

        passwords[25] = execute_command(connectToLevel(
            24), "cd $(mktemp -d) && echo {} | base64 -d > script.sh && chmod +x script.sh && ./script.sh".format(script)).split("The password of user bandit25 is ")[1].strip()



def show_passwords():
    for level, password in passwords.items():
        print('bandit{}:{}'.format(str(level), password))

def write_passwords():
    passwords_file = open('bandit_pass', 'w')
    for level, password in passwords.items():
        passwords_file.write('bandit{}:{}\n'.format(str(level), password))

i = 0
while i < 34:
    try:
        solve_bandit(i)
    except (ConnectionError, paramiko.ssh_exception.SSHException):
        print("Connection Error. Retrying...")
    else:
        i += 1

p.success('All levels solved')
show_passwords()
save = input("Do you want to save the passwords to a file? (y/n): ")

if 'y' in save:
    write_passwords()