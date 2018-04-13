from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cam.setPos(0, -30, 6)
        taskMgr.doMethodLater(3, self.load, "load", extraArgs = ["teapot", Vec3(-5, 0, 0), self.modelLoaded])
        taskMgr.doMethodLater(5, self.load, "load", extraArgs = ["panda", Vec3(5, 0, 0), self.actorLoaded])

    def load(self, name, pos, cb):
        loader.loadModel(name, callback = cb, extraArgs = [pos])

    def modelLoaded(self, model, pos):
        model.reparentTo(render)
        model.setPos(pos)

    def actorLoaded(self, model, pos):
        self.panda = Actor(model, {"walk": "panda-walk"})
        self.panda.reparentTo(render)
        self.panda.setPos(pos)
        self.panda.loop("walk")
