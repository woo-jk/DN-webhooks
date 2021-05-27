import socket
import os
import sys
import hashlib

host = "10.211.55.5"
port = 8000

def make_checksum(data):
    tmp1 = 0
    tmp2 = 2
    data_arr = []
    checksum = 0x0

    for i in range(int(len(data)/2)):
        data_arr.append(data[tmp1:tmp2])
        tmp1 += 2
        tmp2 += 2

    for i in range(len(data_arr)):
        data_chunk = (hex(ord(data_arr[i][0]))) + (hex(ord(data_arr[i][1])))[2:]
        checksum += int(data_chunk, 0)
        checksum %= 0xFFFF
    checksum ^= 0xFFFF
    return (hex(checksum)[2:]).rjust(4, '0')

def header_slice(data):
    header = data[:36]
    checksum = data[36:40]
    result = data[40:]
    return header, result, checksum

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
                chunk_file, addr = s.recvfrom(1024)
                header, result, send_checksum = header_slice(chunk_file.decode())
                receive_data = header + '0000' + result
                receive_checksum = make_checksum(receive_data)

                print('sender checksum:', send_checksum)
                print('receiver checksum:', receive_checksum)

                if receive_checksum != send_checksum:
                    socket.close()
                    print('checksum is not equal')
                    sys.exit()

                write_file.write(chunk_file[40:])
                packet_msg = "packet number " + str(num - check + 1)
                print(packet_msg)
                check -= 1
    
            write_file.close()
        else:
            print("Command is wrong")
            socket.close()
            sys.exit()

