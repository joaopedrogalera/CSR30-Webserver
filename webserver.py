import socket
import threading
import signal
import os

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

def getContentType(fileName):
    ext = fileName.split('.')[-1]

    if ext == 'htm' or ext == 'html':
        return 'text/html'
    if ext == 'png':
        return 'image/png'
    if ext == 'jpg' or ext == 'jpeg':
        return 'image/jpeg'
    if ext == 'css':
        return 'text/css'
    return 'application/octet-stream'

def httpRequest(conn):
    data = conn.recv(8192)
    if data:
        #Converte o conteúdo do request para string e imprime (Python cuida das quebras de linha)
        datastr = data.decode('utf-8')
        print(datastr)

        headerLines = datastr.split('\r\n')
        request = headerLines[0].split(' ')
        if len(request) < 3:
            statusCode = "400 Bad Request"
            contentType = "text/html"
            content = '<html><head><title>Bad Request</title></head><body>Bad Request</body></html>'.encode('utf-8')
        else:
            fileName = '.' + (request[1] if not request[1] == '/' else '/index.html')


            if not os.path.isfile(fileName):
                statusCode = "404 Not Found"
                contentType = "text/html"
                content = '<html><head><title>Not Found</title></head><body>Not Found</body></html>'.encode('utf-8')
            else:
                statusCode = "200 OK"
                contentType = getContentType(fileName)
                f = open(fileName,'rb')
                content = f.read()
                f.close()

        conn.send(('HTTP/1.0 '+statusCode+'\r\n').encode('utf-8'))
        conn.send(('Content-Type: '+contentType+'\r\n').encode('utf-8'))
        conn.send(b'\r\n')
        conn.send(content)
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
