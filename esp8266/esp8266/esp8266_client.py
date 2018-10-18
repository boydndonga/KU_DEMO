from socket import socket, AF_INET, SOCK_STREAM
def send_data(addr,port,data):
    s=socket(AF_INET,SOCK_STREAM)
    try:
        s.connect((addr,port))
        s.sendall(data.encode("utf-8"))
        s.close()
        return True
    except Exception as err:
        print(err)
        return False


