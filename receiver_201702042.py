import socket
import os
import sys
import hashlib

def check_md5_hash(path):
    f = open(path, 'rb')
    data = f.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash


host = ""
port = 8000

if __name__=='__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(0)
        s.settimeout(15)
        print("receiver created")
   
    except socket.error:
        print("1failed to create socket")
        sys.exit()
    
    while True:
        command = input("enter a command: \n1. receive [file_name]\n2. exit\n")
        command_spl = command.split()

        if command_spl[0] == 'exit':
            socket.close()
            sys.exit()

        if command_spl[0] == 'receive':
            s.sendto(command.encode(), (host, int(port)))

            is_valid, addr = s.recvfrom(2000)
            print(is_valid.decode())
            is_exist, addr = s.recvfrom(2000)
            print(is_exist.decode())
            file_size, addr = s.recvfrom(2000)
            print(file_size.decode())
            num, addr = s.recvfrom(2000)

            num = int(num.decode()) + 1
            check = num

            write_file = open(command_spl[1], "wb")

            while check != 1:
                chunk_file, addr = s.recvfrom(2048)
                write_file.write(chunk_file)
                packet_msg = "packet number " + str(num - check + 1)
                print(packet_msg)
                check -= 1
    
            write_file.close()
        else:
            print("Command is wrong")
            socket.close()
            sys.exit()

