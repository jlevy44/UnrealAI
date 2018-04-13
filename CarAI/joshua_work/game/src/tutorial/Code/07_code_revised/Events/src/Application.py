from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *

class Sender(DirectObject):
    def start(self):
        smiley = loader.loadModel("smiley")
        pause = Sequence(Wait(5), Func(messenger.send, "smiley-done", [smiley]))
        pause.start()

class Receiver(DirectObject):
    def __init__(self):
        self.accept("smiley-done", self.showSmiley)

    def showSmiley(self, smiley):
        smiley.reparentTo(render)

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cam.setPos(0, -10, 0)
        rec = Receiver()
        snd = Sender()
        snd.start()
