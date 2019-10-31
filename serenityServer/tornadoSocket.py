from tornado import websocket, web, ioloop
import tornado.httpserver
import os
import json

cl = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
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
        messageObject = json.loads(message)
        print("Got Here - Message Received")
        print(messageObject)
        
    def sendMsg(self, message):
         data = {"type": "server", "value" : message}
         self.write_message(data)
         
# app = web.Application([
#     (r'/', IndexHandler),
#     (r'/ws', SocketHandler)
# ], auto_reload=True)

if __name__ == '__main__':

    config_dict = {"certfile": os.path.join(os.path.abspath('.'), "private", "cert.pem"),
                   "keyfile": os.path.join(os.path.abspath('.'), "private", "privkey.pem"),
                   "port": "88",
                   "address": "0.0.0.0",
                   "hmac_key": False,
                   "tokens": False}
    urls = [
        (r'/ws', SocketHandler)]
    application = tornado.web.Application(urls, auto_reload=True)
    ssl_options = dict(certfile=config_dict["certfile"], keyfile=config_dict["keyfile"])
    http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_options)
    http_server.listen(int(config_dict["port"]), address=config_dict["address"])
    SocketHandler.tokens = config_dict["hmac_key"]



    print("Starting server...")
    # app.listen(8888)
    ioloop.IOLoop.instance().start()
    
    
    
    