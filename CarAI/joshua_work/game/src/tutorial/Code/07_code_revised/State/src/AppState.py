from direct.fsm.FSM import FSM
from direct.gui.DirectGui import *
from panda3d.core import *

class AppState(FSM):
    def enterMenu(self):
        self.pandaBtn = DirectButton(text = "Panda", 
                                     scale = 0.12, 
                                     pos = Vec3(0, 0, 0.1),
                                     command = self.request,
                                     extraArgs = ["Panda"])
        self.smileyBtn = DirectButton(text = "Smiley", 
                                      scale = 0.1, 
                                      pos = Vec3(0, 0, -0.1),
                                      command = self.request,
                                      extraArgs = ["Smiley"])

    def exitMenu(self):
        self.pandaBtn.destroy()
        self.smileyBtn.destroy()

    def enterPanda(self):
        self.menuBtn = DirectButton(text = "Menu", 
                                    scale = 0.1, 
                                    pos = Vec3(0, 0, -0.8),
                                    command = self.request,
                                    extraArgs = ["Menu"])
        self.panda = loader.loadModel("panda")
        self.panda.reparentTo(render)
        base.cam.setPos(0, -40, 5)

    def exitPanda(self):
        self.menuBtn.destroy()
        self.panda.removeNode()

    def enterSmiley(self):
        self.menuBtn = DirectButton(text = "Menu", 
                                    scale = 0.1, 
                                    pos = Vec3(0, 0, -0.8),
                                    command = self.request,
                                    extraArgs = ["Menu"])
        self.smiley = loader.loadModel("smiley")
        self.smiley.reparentTo(render)
        base.cam.setPos(0, -20, 0)

    def exitSmiley(self):
        self.menuBtn.destroy()
        self.smiley.removeNode()
