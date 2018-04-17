from direct.showbase.DirectObject import DirectObject
from panda3d.core import *

class InputHandler(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)

        # don't use -repeat because of slight delay after keydown
        self.walk = False
        self.reverse = False
        self.left = False
        self.right = False

        taskMgr.add(self.updateInput, "update input")

    def beginWalk(self):
        messenger.send("walk-start")
        self.walk = True

    def endWalk(self):
        messenger.send("walk-stop")
        self.walk = False

    def beginReverse(self):
        messenger.send("reverse-start")
        self.reverse = True

    def endReverse(self):
        messenger.send("reverse-stop")
        self.reverse = False

    def beginTurnLeft(self):
        self.left = True

    def endTurnLeft(self):
        self.left = False

    def beginTurnRight(self):
        self.right = True

    def endTurnRight(self):
        self.right = False

    def dispatchMessages(self):
        if self.walk:
            messenger.send("walk", [-0.1])
        elif self.reverse:
            messenger.send("reverse", [0.1])
        
        if self.left:
            messenger.send("turn", [0.8])
        elif self.right:
            messenger.send("turn", [-0.8])

    def updateInput(self, task):
        return task.cont
