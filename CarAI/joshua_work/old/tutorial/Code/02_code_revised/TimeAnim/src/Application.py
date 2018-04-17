from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.sun = loader.loadModel("smiley")
        self.sun.reparentTo(render)
        self.sun.setScale(5)

        self.phantom = loader.loadModel("teapot")
        self.phantom.reparentTo(self.sun)
        self.phantom.setScale(0.1)
        self.phantom.setPos(0, -5, 0)
        self.phantom.hide()

        self.earth = loader.loadModel("frowney")
        self.earthCenter = render.attachNewNode("earthCenter")
        self.earth.reparentTo(self.earthCenter)
        self.earth.setPos(20, 0, 0)

        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(self.earth)
        self.panda.setScale(0.1)
        self.panda.setPos(Vec3(0.7, 0, 0.7))
        self.panda.setHpr(0, 0, 40)
        self.panda.loop("walk")

        self.moon = loader.loadModel("box")
        self.moonCenter = self.earthCenter.attachNewNode("moonCenter")
        self.moon.reparentTo(self.moonCenter)
        self.moonCenter.setPos(self.earth.getPos())
        self.moon.setPos(0, 0, 6)

        self.cam.setPos(0, -100, 0)
        self.taskMgr.add(self.update, "update")

    def update(self, task):
        self.sun.setP(task.time * 10)
        self.earth.setH(task.time * -100)
        self.earthCenter.setH(task.time * 50)
        self.moonCenter.setR(task.time * 150)
        return task.cont
