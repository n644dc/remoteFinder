from tornado import websocket, web, ioloop
import tornado.httpserver
import datetime
import os
import sqlite3

# https://github.com/siysun/Tornado-wss/blob/master/main.py

clientList = set()

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
    
    def __init__(self):
        self.setupDatabase()

    def setupDatabase(self):
        self.dbRemotes = sqlite3.connect('remoteRegister.db')
        self.dbc = self.dbRemotes.cursor()

        try:
            self.dbc.execute('SELECT * FROM remotes')
        except Exception as ex:
            if 'no such table' in str(ex):
                self.dbc = self.dbRemotes.cursor()
                result = self.dbc.execute('''CREATE TABLE remotes (rid, rname, status, time)''')
                self.dbRemotes.commit()

        print("!!!! DB is Operational !!!!")

    def check_origin(self, origin):
        return True

    def open(self):
        print("client connected")
        if self not in clientList:
            clientList.add(self)
        self.sendMsg("Client Connected")

    def on_close(self):
        if self in clientList:
            clientList.remove(self)
        print("Client Disconnected")

    def on_message(self, message):
        print(message)
        self.sendMsg("hi")
        # Implement
        
    def sendMsg(self, message):
       data = {"type": "server", "value" : message}
       [con.write_message(data) for con in clientList]

    def processMessage(self, message):
        msgArray = [item.strip() for item in message.split(',')]
        
    def getRemote(self, rid):
        if self.remoteExists(rid):
            result = self.dbc.execute("SELECT * FROM remotes WHERE rid=?", (rid,))
            res = self.dbc.fetchone()
            returnRemote = {
                "rid" : res[0],
                "rname": res[1],
                "status": res[2],
                "time": res[3]
            }
            return returnRemote
        return None

    def getAllRemotes(self):
        allList = []

        result = self.dbc.execute("SELECT * FROM remotes")
        for res in result:
            returnRemote = {
                "rid" : res[0],
                "rname": res[1],
                "status": res[2],
                "time": res[3]
            }
            allList.append(returnRemote)
        return allList

    def addRemote(self, remote):
        if not self.remoteExists(remote['rid']):
            insertQry = "INSERT INTO remotes (rid, rname, status, time) VALUES ('{0}', '{1}', '{2}', '{3}')".format(remote['rid'], remote['rname'], remote['status'], remote["time"])
            result = self.dbc.execute(insertQry)
            self.dbRemotes.commit()
        else:
            self.updateRemote(remote)

    def updateRemote(self, remote):
        if self.remoteExists(remote['rid']):
            updateQry = "UPDATE remotes SET rname = '{0}', status = '{1}', time = '{2}' WHERE rid = '{3}'".format(remote['rname'], remote['status'], remote["time"], remote['rid'])
            result = self.dbc.execute(updateQry)
            self.dbRemotes.commit()
        else:
            self.addRemote(remote)
      
    def remoteExists(self, rid):
        result = self.dbc.execute("SELECT * FROM remotes WHERE rid=?", (rid,))
        if self.dbc.fetchone() is None:
            return False
        return True

##############


def testSocketServer():
    sh = SocketHandler()
    #This is for testing
    testremote = {
        "rid" : '1003',
        "rname": "room",
        "status": "tooting",
        "time": "128348238429342384293423"
    }

    if sh.remoteExists(testremote["rid"]):
        print("it already exists")
    else:
        sh.addRemote(testremote)

    print(sh.getRemote(testremote["rid"]))

    testremote["status"] = "quiet"

    sh.updateRemote(testremote)

    print(sh.getRemote(testremote["rid"]))

    rems = sh.getAllRemotes()
    for rem in rems:
        print(rem)
            
##############

# applications = tornado.web.Application([(r'/ws', SocketHandler), (r'/', IndexHandler)])

if __name__ == '__main__':

    testSocketServer()

    # http_server = tornado.httpserver.HTTPServer(applications)
    # http_server.listen(8188)

    # print("Starting server...")
    # ioloop.IOLoop.instance().start()
    
    
    
    