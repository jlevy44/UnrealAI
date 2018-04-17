from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.nameEnt = DirectEntry(scale = 0.08, pos = Vec3(-0.4, 0, 0.15), width = 10)
        self.nameLbl = DirectLabel(text = "Hi, what's your name?", 
                                   pos = Vec3(0, 0, 0.4), 
                                   scale = 0.1,
                                   textMayChange = 1,
                                   frameColor = Vec4(0, 0, 0, 0))
        helloBtn = DirectButton(text = "Say Hello!", 
                                scale = 0.1, 
                                command = self.setName,
                                pos = Vec3(0, 0, -0.1))

        self.gender = [0]
        genderRdos = [DirectRadioButton(text = "Female", 
                                        variable = self.gender, 
                                        value = [0], 
                                        scale = 0.05,
                                        pos = Vec3(-0.08, 0, 0.05)),
                      DirectRadioButton(text = "Male", 
                                        variable = self.gender, 
                                        value = [1], 
                                        scale = 0.05,
                                        pos = Vec3(0.16, 0, 0.05))]
        for btn in genderRdos:
            btn.setOthers(genderRdos)

    def setName(self):
        self.acceptDlg = YesNoDialog(text = "Are you sure?", 
                                     command = self.acceptName)

    def acceptName(self, clickedYes):
        self.acceptDlg.cleanup()
        if clickedYes:
            self.loadName()

    def loadName(self):
        self.waitBar = DirectWaitBar(text = "Loading", 
                                     range = 100, 
                                     value = 0, 
                                     pos = Vec3(0, 0, -0.3))
        inc = Func(self.loadStep)
        show = Func(self.setNameLabel)
        load = Sequence(Wait(1), inc, Wait(2), inc, Wait(1), inc, Wait(3), inc, show)
        load.start()

    def loadStep(self):
        self.waitBar["value"] += 25

    def setNameLabel(self):
        title = ""
        if self.gender[0]:
            title = "Mister"
        else:
            title = "Miss"

        self.nameLbl["text"] = "Hello " + title + " " + self.nameEnt.get() + "!"
