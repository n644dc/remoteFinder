from tornado import websocket, web, ioloop
import tornado.httpserver
import datetime
import os
import json
# https://github.com/siysun/Tornado-wss/blob/master/main.py

cl = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
    
    self.REGISTER_FILE = 'registerList.json'
    
    self.registerList = None

    def check_origin(self, origin):
        return True

    def open(self):
      if self not in cl:
        cl.append(self)
      self.sendMsg("Client Connected")

    def on_close(self):
      if self in cl:
        cl.remove(self)

    def on_message(self, message):
      print(message)
      # messageObject = json.loads(message)
      # print(messageObject)
      # Implement
        
    def sendMsg(self, message):
       data = {"type": "server", "value" : message}
       self.write_message(data)
         
    def readRegister(self, path):
      registerList = None
      
      if not os.path.isfile(self.REGISTER_FILE):
        with open(self.REGISTER_FILE, 'w'): pass
        print('New Register List Created.')
        
      with open(path) as f:
        registerList = f.readlines()
        print('registerList loaded.')
    
    def writeRegister(self, path):
      print("Not Implemented")
      # Implement
      # write self.REGISTER_FILE with registerList
    
    def addRemote(self, remoteString):
      print(remoteString)
      # Implement
        
    def remoteRemote(self, remoteString):
      print(remoteString)
      # Implement
      
    def checkRemoteAlive(self, remoteString):
      print(remoteString)
      # Implement
      
    def getRemoteStatus(self, remoteString):
      print(remoteString)
      # Implement
      
    def setRemoteStatus(self, remoteString):
      print(remoteString)
      # Implement
      
    def remoteExists(self, remoteString):
      print(remoteString)
      # Implement

if __name__ == '__main__':
  config_dict = {"certfile": os.path.join(os.path.abspath('.'), "private", "cert.pem"),
                 "keyfile": os.path.join(os.path.abspath('.'), "private", "privkey.pem"),
                 "port": "88",
                 "address": "0.0.0.0",
                 "hmac_key": False,
                 "tokens": False}
  urls = [(r'/ws', SocketHandler)]
  application = tornado.web.Application(urls, auto_reload=True)
  ssl_options = dict(certfile=config_dict["certfile"], keyfile=config_dict["keyfile"])
  http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_options)
  http_server.listen(int(config_dict["port"]), address=config_dict["address"])
  SocketHandler.tokens = config_dict["hmac_key"]

  print("Starting server...")
  ioloop.IOLoop.instance().start()
    
    
    
    