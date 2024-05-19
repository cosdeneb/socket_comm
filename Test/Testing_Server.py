import socket
import select

IP = ''
PORT1 = 5050
PORT2 = 5060
SIZE = 1024
ADDR1 = (IP, PORT1)
ADDR2 = (IP, PORT2)

server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket1.bind(ADDR1)  # 주소 바인딩
server_socket1.listen()  # 클라이언트의 요청을 받을 준비

server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket2.bind(ADDR2)  # 주소 바인딩
server_socket2.listen()  # 클라이언트의 요청을 받을 준비

read_socket_list = [server_socket1, server_socket2]

while True:
    # select 선언
    conn_read_socket_list, conn_write_socket_list, conn_except_socket_list = select.select(read_socket_list, [], [])
    for conn_read_socket in conn_read_socket_list:
        if conn_read_socket == server_socket1:
            print('hello socket1')
            client_socket, client_addr = server_socket1.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
            msg = client_socket.recv(SIZE)  # 클라이언트가 보낸 메시지 반환
            print("[{}] message : {}".format(client_addr,msg))  # 클라이언트가 보낸 메시지 출력
            
            client_socket.sendall("welcome 5050!".encode())  # 클라이언트에게 응답
            
            client_socket.close()  # 클라이언트 소켓 종료
        
        elif server_socket2 == server_socket2:
            print('hello socket2')
            client_socket, client_addr = server_socket2.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
            msg = client_socket.recv(SIZE)  # 클라이언트가 보낸 메시지 반환
            print("[{}] message : {}".format(client_addr,msg))  # 클라이언트가 보낸 메시지 출력
            
            client_socket.sendall("welcome 5060!".encode())  # 클라이언트에게 응답
            
            client_socket.close()  # 클라이언트 소켓 종료









