from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from FollowCam import FollowCam
from NetworkHandler import NetworkHandler
from NetClasses import Server, Client, ServerProtocol, ClientProtocol

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setupScene()
        self.setupInput()
        self.setupNetwork()

    def setupScene(self):
        self.world = loader.loadModel("environment")
        self.world.reparentTo(render)
        self.world.setScale(0.5)
        self.world.setPos(-8, 80, 0)

        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(render)
        self.followCam = FollowCam(self.cam, self.panda)

    def setupInput(self):
        self.netInput = NetworkHandler()
        self.accept("walk-start", self.beginWalk)
        self.accept("walk-stop", self.endWalk)
        self.accept("reverse-start", self.beginReverse)
        self.accept("reverse-stop", self.endReverse)
        self.accept("walk", self.walk)
        self.accept("reverse", self.reverse)        
        self.accept("turn", self.turn)

    def setupNetwork(self):
        server = Server(ServerProtocol(), 9999)
        client = Client(ClientProtocol())
        client.connect("localhost", 9999, 3000)
        client.start()

    def beginWalk(self):
        self.panda.setPlayRate(1.0, "walk")
        self.panda.loop("walk")

    def endWalk(self):
        self.panda.stop()

    def beginReverse(self):
        self.panda.setPlayRate(-1.0, "walk")
        self.panda.loop("walk")

    def endReverse(self):
        self.panda.stop()

    def walk(self, rate):
        self.panda.setY(self.panda, rate)

    def reverse(self, rate):
        self.panda.setY(self.panda, rate)

    def turn(self, rate):
        self.panda.setH(self.panda, rate)
