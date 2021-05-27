import socket
import os
import sys
import hashlib


addr = '10.211.55.5'
port = 8000

def make_checksum(data):    
    checksum = 0x0
    data_arr = []
    tmp1 = 0
    tmp2 = 2
    
    for i in range(int(len(data) /2)):
        data_arr.append(data[tmp1:tmp2])
        tmp1 += 2
        tmp2 += 2

    for i in range(len(data_arr)):
        data_chunk = (hex(ord(data_arr[i][0]))) + (hex(ord(data_arr[i][1])))[2:]
        checksum += int(data_chunk, 0)
        checksum %= 0xFFFF
    checksum ^= 0xFFFF
    return (hex(checksum)[2:]).rjust(4, '0')

def make_header(Data, size):
    Src_addr = '0ad33705'
    Dst_addr = '0ad33705'
    Zeros = '00'
    Protocol = '17'
    leng = str(hex((size+8)))[2:]
    UDP_leng = leng.rjust(4, '0')
    Src_port = '1f40'
    Dst_port = '1f40'
    Length = UDP_leng
    checksum_init = '0000'

    data = Src_addr + Dst_addr + Zeros + Protocol + UDP_leng + Src_port + Dst_port + Length + checksum_init + Data
    checksum = make_checksum(data)
    print('final checksum: ', checksum)
    data = Src_addr + Dst_addr + Zeros + Protocol + UDP_leng + Src_port + Dst_port + Length + checksum + Data
    return data

def sender_send(file_name, addr):
        s.sendto("valid list command.".encode(), addr)
        if os.path.isfile(file_name):
            s.sendto("file exists!".encode(), addr)

            file_size = os.stat(file_name).st_size
            num = int(file_size/(1024 - 40)) + 1
            size_msg = "file_size : "  + str(num)
            s.sendto(size_msg.encode(), addr)
            s.sendto(str(num).encode(), addr)
            
            read_file = open(file_name, 'rb')
            check = num

            while check != 0:
                chunk_file = read_file.read(1024 - 40)
                data = make_header(chunk_file.decode('utf-8'), len(chunk_file))
                s.sendto(data.encode('utf-8'), addr)
                packet_msg = "packet number " + str(num - check + 1)
                print(packet_msg)
                check -= 1
            read_file.close()
            print("send complete")

        else: 
            print("file not found")


if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', 8000))
        print("waiting for client.")
    except socket.error:
        print("failed to create socket")
        sys.exit()

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
