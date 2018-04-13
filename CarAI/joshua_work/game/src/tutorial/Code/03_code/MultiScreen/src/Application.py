from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from pandac.PandaModules import loadPrcFileData

loadPrcFileData("", "win-origin 0 0")
loadPrcFileData("", "win-size 2880 900")
loadPrcFileData("", "undecorated 1")

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.pandas = []

        for i in range(8):
            panda = Actor("panda", {"walk": "panda-walk"})
            panda.reparentTo(render)
            panda.loop("walk")
            panda.setX(-28 + i * 8)
            self.pandas.append(panda)

        self.cam.setPos(0, -40, 6)