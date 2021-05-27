import socket
import os
import sys
import hashlib

addr = '34.64.105.127'
port = 8000

try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', 8000))
        print("waiting for client.")
except socket.error:
	print("failed to create socket")
	sys.exit()

def check_md5(path):
	f = open(path, 'rb')
	data = f.read()
	md5_hash = hashlib.md5(data).hexdigest()
	return md5_hash

def sender_send(file_name, addr):
        s.sendto("valid list command.".encode(), addr)
        if os.path.isfile(file_name):
            s.sendto("file exists!".encode(), addr)

            file_size = os.stat(file_name).st_size
            num = int(file_size/2048) + 1
            size_msg = "file_size : "  + str(num)
            s.sendto(size_msg.encode(), addr)
            s.sendto(str(num).encode(), addr)
            
            read_file = open(file_name, 'rb')
            check = num

            while check != 0:
                chunk_file = read_file.read(2048)
                s.sendto(chunk_file, addr)
                packet_msg = "packet number " + str(num - check + 1)
                print(packet_msg)
                check -= 1
            read_file.close()
            print("send complete")

        else: 
            print("file not found")


if __name__ == "__main__":
    while True:    
        try:
            data, client_addr = s.recvfrom(2000)
        except ConnectionResetError:
                print("error. port number not matching.")
                sys.exit()

        text = data.decode('utf8')
        handler = text.split()

        if handler[0] == 'receive':
            sender_send(handler[1], client_addr)
        else:
            print("Command is wrong")
            s.close()
            sys.exit()
