
from settings import BACKEND_config
import socketio
sio=socketio.Client()

class SocketIoHandler():
    is_connected=False


    def __init__(self):

        self.socket= sio
        self.connect()
        self.ListenerCallBack=None
    def setCallBackListener(self,call_backs):
        self.ListenerCallBack=call_backs

    def set_con(self):
        print (" BACKEND UP")
        self.is_connected=True        

    def set_discon(self):
        print (" !!!  BACKEND DOWN !!!")

        self.is_connected=False   


    def connect(self):
     
     self.socket.on('connect', self.set_con)
     self.socket.on('disconnect', self.set_discon)
  
     self.socket.connect(BACKEND_config["socket_url"]+"?isServer=true")


    def isConnected(self):
       return self.is_connected

    def call_backs(self):
            @self.socket.event
            def run_command(data):
                print(data)
                self.ListenerCallBack(data)


            