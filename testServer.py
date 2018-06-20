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

# 송신을 위한 socket을 만들고 sock에 connect
def createSocket() :
    # 연결할 서버(수신단)의 ip주소와 port번호
    #TCP_IP = '172.30.1.4'
    #TCP_IP =  '210.115.49.252'
    try :
        global client2

        TCP_IP = '192.168.0.66' # 보낼 PC의 IP
        TCP_PORT = 5002
        #송신을 위한 socket 준비
        client2 = socket.socket()
        client2.connect((TCP_IP, TCP_PORT))

    except socket.error as msg :
        print("socket create error ! "+ str(msg))


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
        client1, addr = server.accept()  # socket과 client주소
        connect_list.append(client1)
        print("connected : ")
        print(connect_list)

        if  connect_list :

            print("client 1 -> success connection ! ")

            length = recvall(client1, 16)
            # 길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를
            # 먼저 받아서 이미지를 받을 때 편리하려고 하는 것이다.
            stringData = recvall(client1, int(length))
            print("string length", length.decode())  # 받은 이미지 크기를 출력
            data = numpy.fromstring(stringData, dtype='uint8')

            connect_list.remove(client1)
            print("connected : ")
            print(connect_list)
            client1.close()

            decimg = cv2.imdecode(data, 1)
            cv2.imshow('SERVER@recv', decimg)
            cv2.waitKey(1) # 0으로 무한대기 상태면 멈출 수 있음

            createSocket() # client2로 연결되는 socket 생성
            # client2 으로 다시 전송. 이미지를 String 형태로 변환(인코딩)
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, imgencode = cv2.imencode('.jpg', decimg, encode_param)
            data = numpy.array(imgencode)
            stringData = data.tostring()

            client2.send(str(len(stringData)).ljust(16).encode())  # 이미지 크기 먼저 저송
            client2.send(stringData)  # 이미지 배열 전송
            client2.close() # client2 socket 닫기






