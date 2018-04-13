from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from pandac.PandaModules import loadPrcFileData

loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.teapot = loader.loadModel("teapot")
        self.teapot.reparentTo(render)
        self.teapot.setPos(-5, 0, 0)

        self.pandaActor = Actor("panda", {"walk": "panda-walk"})
        self.pandaActor.reparentTo(render)
        self.pandaActor.setPos(Vec3(5, 0, 0))
        self.pandaActor.loop("walk")
        
        self.cam.setPos(0, -30, 6)