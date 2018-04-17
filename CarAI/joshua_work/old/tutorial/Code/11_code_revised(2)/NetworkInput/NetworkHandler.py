from InputHandler import InputHandler
from panda3d.core import *

class NetworkHandler(InputHandler):
    def __init__(self):
        InputHandler.__init__(self)

        self.accept("net-walk-start", self.beginWalk)
        self.accept("net-walk-stop", self.endWalk)
        self.accept("net-left-start", self.beginTurnLeft)
        self.accept("net-left-stop", self.endTurnLeft)
        self.accept("net-right-start", self.beginTurnRight)
        self.accept("net-right-stop", self.endTurnRight)

        taskMgr.add(self.updateInput, "update network input")

    def updateInput(self, task):
        self.dispatchMessages()
        return task.cont
