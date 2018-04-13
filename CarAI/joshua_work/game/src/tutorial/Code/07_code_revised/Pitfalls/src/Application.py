from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
from GameObject import GameObject
from GameObject import handle_event
from panda3d.core import *

class Sender(GameObject):
    def start(self):
        smiley = loader.loadModel("smiley")
        pause = Sequence(Wait(5), Func(messenger.send, "smiley-done", [smiley]))
        pause.start()

class Receiver(GameObject):
    @handle_event("smiley-done")
    def showSmiley(self, smiley):
        smiley.reparentTo(render)
        messenger.send("smiley-shown")

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("smiley-shown", self.clean)
        self.cam.setPos(0, -10, 0)
        self.rec = Receiver()
        snd = Sender()
        snd.start()

    def clean(self):
        self.ignore("smiley-shown")
        self.rec.destroy()
