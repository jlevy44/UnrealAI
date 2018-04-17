from direct.showbase.ShowBase import ShowBase
from panda3d.core import GeoMipTerrain

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.terrain = GeoMipTerrain("terrain")
        #doesn't use search path
        self.terrain.setHeightfield("../textures/height.png")
        self.terrain.setColorMap("../textures/grass.png")
        self.terrain.getRoot().setSz(35)
        #self.terrain.setBlockSize(16)
        #self.terrain.setNear(35)
        #self.terrain.setFar(75)
        self.terrain.getRoot().reparentTo(render)
        self.terrain.generate()

        z = self.terrain.getElevation(256, 256) * 40
        self.cam.setPos(256, 256, z)

        self.terrain.setFocalPoint(self.cam)
        self.taskMgr.add(self.updateTerrain, "update terrain")

    def updateTerrain(self, task):
        self.terrain.update()
        return task.cont