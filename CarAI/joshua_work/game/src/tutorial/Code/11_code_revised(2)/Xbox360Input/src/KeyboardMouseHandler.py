from InputHandler import InputHandler
from panda3d.core import *

class KeyboardMouseHandler(InputHandler):
    def __init__(self):
        InputHandler.__init__(self)

        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True) 
        base.win.requestProperties(props)        
        
        self.accept("w", self.beginWalk)
        self.accept("w-up", self.endWalk)
        self.accept("s", self.beginReverse)
        self.accept("s-up", self.endReverse)
        self.accept("a", self.beginTurnLeft)
        self.accept("a-up", self.endTurnLeft)
        self.accept("d", self.beginTurnRight)
        self.accept("d-up", self.endTurnRight)

        taskMgr.add(self.updateInput, "update input")

    def resetMouse(self):
        cx = base.win.getProperties().getXSize() / 2
        cy = base.win.getProperties().getYSize() / 2
        base.win.movePointer(0, cx, cy)

    def updateInput(self, task):
        if base.mouseWatcherNode.hasMouse():
            messenger.send("turn", [-base.mouseWatcherNode.getMouseX() * 10])
        
        self.resetMouse()
        self.dispatchMessages()

        return task.cont
