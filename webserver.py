import socket
import threading
import signal

PORT = 8080
running = True

#Encerra servidor ao receber SIGTERM ou SIGINT
def stop(signum,frame):
    global running
    running = False

    #Conecta com localhost para fazer o 'accept' do servidor retornar
    s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1',PORT))
    s.close()

signal.signal(signal.SIGTERM,stop)
signal.signal(signal.SIGINT,stop)

def httpRequest(conn):
    data = conn.recv(8192)
    print(data)
    conn.send(b'HTTP/1.0 200 OK\r\n\r\n')
    conn.close()

def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    s.bind(('0.0.0.0',PORT))
    s.listen()

    while running:
        conn,addr = s.accept()
        print('Conectado com ',addr)
        th = threading.Thread(target=httpRequest,args=(conn,))
        th.start()

    s.close()

if __name__ == '__main__':
    main()
