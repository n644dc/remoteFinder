from tornado import websocket, web, ioloop
import tornado.httpserver
import datetime
import os
import sqlite3

# https://github.com/siysun/Tornado-wss/blob/master/main.py

clientList = set()

dbRemotes = sqlite3.connect('remoteRegister.db')
dbc = None

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
    
    def __init__(self):
        allRemotes = dbc.execute('SELECT * FROM remotes')
        
        for remote in allRemotes:
            print(remote)

    def check_origin(self, origin):
        return True

    def open(self):
        print("client connected")
        if self not in clientList:
            clientList.append(self)
        self.sendMsg("Client Connected")

    def on_close(self):
        if self in clientList:
            clientList.remove(self)

    def on_message(self, message):
        print(message)
        self.sendMsg("hi")
        # Implement
        
    def sendMsg(self, message):
       data = {"type": "server", "value" : message}
       [con.write_message(data) for con in clientList]

    def addRemote(self, remote):
        if not self.remoteExists(remote['rid']):
            dbc.execute('INSERT INTO remotes VALUES ({0}, {1}, {2})'.format(remote['rid'], remote['name'], remote['state']))
            dbc.commit()
        
    def getRemoteStatus(self, remote):
        print(remote)
        # Implement
      
    def setRemoteStatus(self, remote):
        dbc.execute('UPDATE remotes VALUES ({0}, {1}, {2})'.format(remote['rid'], remote['name'], remote['state']))
        dbc.commit()
      
    def remoteExists(self, rid):
        remote = dbc.execute("SELECT * FROM remotes WHERE rid=?", (rid,))
        if dbc.fetchone() is None:
            return False
        return True

##############

def setupDatabase():
    dbc = dbRemotes.cursor()
    try:
        allRemotes = dbc.execute('SELECT * FROM remotes')
    except Exception as ex:
        if 'no such table' in str(ex):
            dbc.execute('''CREATE TABLE remotes (rid, rname, status)''')
            dbc.commit()
            
##############

applications = tornado.web.Application([(r'/ws', SocketHandler), (r'/', IndexHandler)])

if __name__ == '__main__':

    setupDatabase()

    http_server = tornado.httpserver.HTTPServer(applications)
    http_server.listen(8188)

    print("Starting server...")
    ioloop.IOLoop.instance().start()
    
    
    
    