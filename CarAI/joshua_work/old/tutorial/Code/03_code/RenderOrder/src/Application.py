from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.panda = Actor("panda", {"walk": "panda-walk"})
        self.panda.reparentTo(render)
        self.panda.loop("walk")
        self.panda.setBin("fixed", 40, 0) 

        self.teapot = loader.loadModel("teapot")
        self.teapot.reparentTo(render)
        self.teapot.setBin("fixed", 40, 1)
        self.teapot.setDepthTest(False)
        self.teapot.setDepthWrite(False)

        self.smiley = loader.loadModel("smiley")
        self.smiley.reparentTo(render)
        self.smiley.setPos(0, 50, 6)
        self.smiley.setScale(30)
        self.smiley.setBin("background", 10)
        self.smiley.setDepthTest(False)
        self.smiley.setDepthWrite(False)        

        self.cam.setPos(0, -30, 6)
