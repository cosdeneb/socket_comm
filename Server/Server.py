from pickle import FALSE, TRUE
from socket import *
import sys, os
import time
import threading
from _thread import *
from select import select
import numpy as np

from matplotlib.pyplot import connect
# from requests import get

class Server():

    def __init__(self):

        super(Server, self).__init__()
        self.soc1 = socket(AF_INET, SOCK_STREAM) # IPv4, TCP 사용하여 서버소켓 오픈
        self.soc2 = socket(AF_INET, SOCK_STREAM)
        # soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # 소켓 옵션 설정 ==> 포트 여러번 바인드하면 발생하는 에러 방지

        HOST = gethostbyname(gethostname())
        # host = get("https://api.ipify.org").text
        # HOST = gethostbyname(getfqdn())

        PORT1 = 9999
        PORT2 = 8888
        self.size = 1024
        self.counter = 0
        self.time_threshold = 0.5

        print('Server ip : {} / Port1 : {} & Port2 : {}'.format(str(HOST), str(PORT1), str(PORT2)))

        self.soc1.bind((HOST, PORT1))
        self.soc2.bind((HOST, PORT2))

        self.soc1.listen()
        self.soc2.listen()

        self.read_socket_list = [self.soc1, self.soc2]

        # t = threading.Thread(target=binder, args=(c, addr)) # Thread를 이용해서 Client 접속 대기를 만들고 다시 accept로 넘어가서 다른 Client 대기
        # t.start()


    def receive(self, direct, filename):

        with open(direct + "\\" + filename, 'wb') as f:

            try:
                data = np.zeros(self.size)
                while len(data) >= self.size:

                    read_socket, write_socket, error_socket = select(self.read_socket_list, [], [])

                    for conn_read_socket in read_socket:
                        if conn_read_socket == self.soc1:
                            
                            c1, addr1 = self.soc1.accept() # (소켓, 주소정보) tuple 반환 ==> addr[0] = ip, addr[1] = port
                            print(str(addr1), '에서 접속하였습니다.')
                            
                            data = c1.recv(self.size)
                            f.write(data)
                            self.counter += len(data)
                            print('Network Type : Cellular')
                            # print(data)
                            c1.close()

                        elif conn_read_socket == self.soc2:
                            c2, addr2 = self.soc2.accept()
                            print(str(addr2), '에서 접속하였습니다.')
                            
                            data = c2.recv(self.size)
                            f.write(data)
                            self.counter += len(data)
                            print("Network Type : WiFi")
                            # print(data)
                            c2.close()


            except ConnectionResetError:
                print('({}, {})와 연결이 끊어졌습니다.'.format(addr1[0], addr1[1]))
                print('({}, {})와 연결이 끊어졌습니다.'.format(addr2[0], addr2[1]))

            except KeyboardInterrupt:
                raise KeyboardInterrupt
                
        print('파일 저장 완료, 파일 크기 : {} byte'.format(self.counter))


############################################## main 함수 작동 부분 ################################################

if __name__ == '__main__':

    os.chdir(os.path.dirname(__file__)) # 실행 경로를 현재 .py 파일이 위치한 곳(서버의 위치)으로 변경
    direct = os.getcwd()
    filename = 'image.jpg'
    # filename = 'paraKQC_v1.txt'

    # t = threading.Thread(target=binder, args=(c, addr)) # Thread를 이용해서 Client 접속 대기를 만들고 다시 accept로 넘어가서 다른 Client 대기
    # t.start()
    # start_new_thread(binder, (c, addr))

    print('클라이언트 접속 대기 중')

    s = Server()
    s.receive(direct, filename)