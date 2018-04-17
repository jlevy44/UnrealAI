from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import audioop

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.addSmiley()
        self.addGround()
        self.setupMicrophone()
        self.cam.setPos(0, -50, 10)

    def setupMicrophone(self):
        for i in range(MicrophoneAudio.getNumOptions()):
            print i, MicrophoneAudio.getOption(i)

        if MicrophoneAudio.getNumOptions() > 0:
            index = raw_input("choose device: ")
            opt = MicrophoneAudio.getOption(0)
            self.cursor = opt.open()
            taskMgr.add(self.update, "update audio")

    def addSmiley(self):
        self.smiley = loader.loadModel("smiley")
        self.smiley.reparentTo(render)
        self.smiley.setZ(10)

    def addGround(self):
        cm = CardMaker("ground")
        cm.setFrame(-500, 500, -500, 500)
        ground = render.attachNewNode(cm.generate())
        ground.setColor(0.2, 0.4, 0.2)
        ground.lookAt(0, 0, -1)

    def update(self, task):
        if self.cursor.ready() >= 16:
            data = self.cursor.readSamples(self.cursor.ready())
            rms = audioop.rms(data, 2)
            minmax = audioop.minmax(data, 2)
            intensity = float(rms) / 32767.0
            self.win.setClearColor(Vec4(intensity, intensity, intensity, 1))
            print rms, minmax

            currentZ = self.smiley.getZ()
            self.smiley.setZ(currentZ - 0.3 + intensity)

            if self.smiley.getZ() <= 1:
                self.smiley.setZ(1)
        
        return task.cont
