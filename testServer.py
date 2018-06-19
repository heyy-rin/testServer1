import socket
import cv2
import numpy
import time

count = 0
#socket 수신 버퍼를 읽어서 반환하는 함수
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

#수신에 사용될 내 ip와 내 port번호
TCP_IP = '192.168.0.66'
TCP_PORT = 5001
BUFSIZE = 1024
connect_list = []

if __name__ == '__main__':
    #TCP소켓 열고 수신 대기
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TCP_IP, TCP_PORT))
    server.listen(True)

    while True:


        print("wating connection ")
        client, addr = server.accept()  # socket과 client주소
        connect_list.append(client)
        print("connected : ")
        print(connect_list)

        if  connect_list :
            print("success connect !")

            length = recvall(client, 16)
            # 길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를
            # 먼저 받아서 이미지를 받을 때 편리하려고 하는 것이다.
            stringData = recvall(client, int(length))
            print("string length", length.decode())  # 받은 이미지 크기를 출력
            data = numpy.fromstring(stringData, dtype='uint8')

            connect_list.remove(client)

            print("connected : ")
            print(connect_list)

            client.close()

            decimg = cv2.imdecode(data, 1)
            #print("data : ", decimg)

            cv2.imshow('RECV', decimg)
            cv2.waitKey(1) # 0 으로 무한대기 상태면 멈출 수 있음




