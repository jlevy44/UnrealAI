from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from random import choice

class NetCommon:
    def __init__(self, protocol):
        self.manager = ConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        self.protocol = protocol

        taskMgr.add(self.updateReader, "updateReader")

    def updateReader(self, task):
        if self.reader.dataAvailable():
            data = NetDatagram()
            self.reader.getData(data)
            reply = self.protocol.process(data)

            if reply != None:
                self.writer.send(reply, data.getConnection())

        return task.cont

class Server(NetCommon):
    def __init__(self, protocol, port):
        NetCommon.__init__(self, protocol)
        self.listener = QueuedConnectionListener(self.manager, 0)
        socket = self.manager.openTCPServerRendezvous(port, 100)
        self.listener.addConnection(socket)
        self.connections = []

        taskMgr.add(self.updateListener, "updateListener")

    def updateListener(self, task):
        if self.listener.newConnectionAvailable():
            connection = PointerToConnection()
            if self.listener.getNewConnection(connection):
                connection = connection.p()
                self.connections.append(connection)
                self.reader.addConnection(connection)
                print "Server: New connection established."

        return task.cont

class Client(NetCommon):
    def __init__(self, protocol):
        NetCommon.__init__(self, protocol)      

    def connect(self, host, port, timeout):
        self.connection = self.manager.openTCPClientConnection(host, port, timeout)
        if self.connection:
            self.reader.addConnection(self.connection)
            print "Client: Connected to server."

    def send(self, datagram):
        if self.connection:
            self.writer.send(datagram, self.connection)

    def start(self):
        data = PyDatagram()
        data.addUint8(0)
        data.addString("hi")
        self.send(data)

class Protocol:
    def printMessage(self, title, msg):
        print "%s %s" % (title, msg)

    def buildReply(self, msgid, data):
        reply = PyDatagram()
        reply.addUint8(msgid)
        reply.addString(data)
        return reply

    def process(self, data):
        return None

class ServerProtocol(Protocol):
    def process(self, data):
        it = PyDatagramIterator(data)
        msgid = it.getUint8()

        if msgid == 0:
            pass
        elif msgid == 1:
            command = it.getString()
            self.printMessage("new command:", command)
            messenger.send(command)

        return self.buildReply(0, "ok")

class ClientProtocol(Protocol):
    def __init__(self):
        self.lastCommand = globalClock.getFrameTime()
        self.commands = ["net-walk-start", 
                         "net-walk-stop", 
                         "net-left-start", 
                         "net-left-stop",
                         "net-right-start",
                         "net-right-stop"]

    def process(self, data):
        time = globalClock.getFrameTime()
        if time - self.lastCommand > 0.5:
            self.lastCommand = time
            return self.buildReply(1, choice(self.commands))
        else:
            return self.buildReply(0, "nop")
