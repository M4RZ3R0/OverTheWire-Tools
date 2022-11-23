import base64
import paramiko

from pwn import *

host = 'krypton.labs.overthewire.org'
port = 2231
context.log_level = 'warn'
p = log.progress('Solving level: ', level=30)
passwords = {1: 'KRYPTONISGREAT'}


def connectToLevel(level):
    return ssh('krypton{}'.format(level), host=host, password=passwords[level], port=port)


def execute_command(shell, command):
    return shell[command].decode('utf-8')


def solve_one_command(level, command):
    shell = connectToLevel(level)
    passwords[level+1] = execute_command(shell, command)
    shell.close()


def decrypt_vigenere(ciphertext, key):
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    ciphertext_int = [ord(i) for i in ciphertext]
    plaintext = ''
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
        plaintext += chr(value + 65)
    return plaintext


def decrypt_stream(ciphertext, crypt):
    key = ''
    for i in range(len(ciphertext)):
        k = ord(ciphertext[i]) - ord(crypt[i])
        if k < 0:
            k += 26
        k += ord('A')
        key += chr(k)
    return key


def solve_krypton(level):
    match level:
        case 1:
            # Level 1
            p.status('1')
            passwords[2] = execute_command(connectToLevel(
                1), 'cat /krypton/krypton1/krypton2 | tr A-Z N-ZA-M').split('PASSWORD')[1].strip()
        case 2:
            # Level 2
            p.status('2')
            solve_one_command(
                2, 'cat /krypton/krypton2/krypton3 | tr A-Z O-ZA-N')
        case 3:
            # Level 3
            p.status('3')
            passwords[4] = execute_command(connectToLevel(
                3), 'cat /krypton/krypton3/krypton4 | tr A-Z "BOIHGKNQVTWYURXZAJEMSLDFPC"').split()[-1].strip()
        case 4:
            # Level 4
            p.status('4')
            passwords[5] = decrypt_vigenere(execute_command(connectToLevel(
                4), "cat /krypton/krypton4/krypton5").replace(' ', ''), "FREKEY")
        case 5:
            # Level 5
            p.status('5')
            passwords[6] = decrypt_vigenere(execute_command(connectToLevel(
                5), "cat /krypton/krypton5/krypton6").replace(' ', ''), "KEYLENGTH")
        case 6:
            # Level 6
            p.status('6')
            passwords[6] = decrypt_stream(execute_command(connectToLevel(
                6), "cat /krypton/krypton6/krypton7").replace(' ', ''), execute_command(connectToLevel(6), "cd $(mktemp -d) && chmod 777 . && ln -s /krypton/krypton6/keyfile.dat && python3 -c 'print(\"A\" * 30)' > plain.txt && /krypton/krypton6/encrypt6 plain.txt cipher.txt && cat cipher.txt"))


def show_passwords():
    for level, password in passwords.items():
        print('krypton{}:{}'.format(str(level), password))


def write_passwords():
    passwords_file = open('krypton_pass', 'w')
    for level, password in passwords.items():
        passwords_file.write('krypton{}:{}\n'.format(str(level), password))


i = 0
while i < 34:
    try:
        solve_krypton(i)
    except (ConnectionError, paramiko.ssh_exception.SSHException):
        print("Connection Error. Retrying...")
    else:
        i += 1

p.success('All levels solved')
show_passwords()
save = input("Do you want to save the passwords to a file? (y/n): ")

if 'y' in save:
    write_passwords()
