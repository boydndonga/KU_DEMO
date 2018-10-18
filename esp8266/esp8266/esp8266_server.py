import socket
from machine import Pin
import network
import espConfig

class Server:
    def __init__(self,af_inet,port):
        self.af_inet=af_inet
        self.port=port
        self.output_pins={i:Pin(i,Pin.OUT) for i in (2,4,5,12,13,15)}
        self.states=[1,0]
        self.sta_if = network.WLAN(network.STA_IF)
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as msg:
            print("Socket creation error: " + str(msg))   

    def wifi_connect(self,ssid,password):
        '''
        connect device to a wifi network if not connected
        '''
        if not self.sta_if.isconnected():
            self.sta_if.active(True)
            self.sta_if.connect(ssid,password)
            while not self.sta_if.isconnected():
                pass
            print("connected to {}".format(ssid))
        return True

    def set_pin(self,user_in):
        try: pin_concatState=int(user_in)
        except: return "error converting input to int" 
        if len(str(pin_concatState))==2:
            if int(str(pin_concatState)[0]) in self.output_pins and int(str(pin_concatState)[1]) in (0,1):
                self.output_pins[int(str(pin_concatState)[0])].value(int(str(pin_concatState)[1]))
                print(self.output_pins[int(str(pin_concatState)[0])])
                return "success"
        elif len(str(pin_concatState))==3:
            if int(str(pin_concatState)[:2]) in self.output_pins and int(str(pin_concatState)[2]) in (0,1):
                self.output_pins[int(str(pin_concatState)[:2])].value(int(str(pin_concatState)[2]))
                print(self.output_pins[int(str(pin_concatState)[:2])])
                return "success"
        else:
            return "Wrong Input"
 
    def terminate_socket(self):
        try:
            self.s.close()
        except Exception as err:
            print("ERROR:"+err)

    def socket_bind(self):
        try:
            print("Binding socket to port: " + str(self.port))
            self.s.bind((self.af_inet,self.port))
            self.s.listen(5)
        except socket.error as msg:
            print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
            try: self. terminate_socket()
            except Exception as err: print("ERROR:"+str(err))
            self.socket_bind()

    def receive_commands(self):
        try:
            while True:
                conn, address = self.s.accept()
                print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
                data=conn.recv(1024)
                if data: 
                    try: 
                        server_command=data.decode("utf-8")                  
                        response=self.set_pin(server_command)
                        try: conn.send(response.encode("utf-8"))
                        except Exception as err: pass
                        conn.close()
                    except Exception as err:
                        print("ERROR:%s"%err)
                        conn.close()
                        pass
                else:
                    conn.close()
                    pass  
        except Exception as e:
            print("ERROR:%s"%e)


def main(af_inet,port):
    server=Server(af_inet,port)
    server.socket_bind()
    if server.wifi_connect(espConfig.SSID,espConfig.PASSWORD):
        while True:
            server.receive_commands()
        server.terminate_socket()

while True:
    main("0.0.0.0",9999)