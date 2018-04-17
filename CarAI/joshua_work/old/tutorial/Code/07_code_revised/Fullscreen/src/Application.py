from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.status = OnscreenText("Window Mode")
        toggle = Sequence(Wait(3),
                          Func(self.status.setText, "Switching to Fullscreen Mode"),
                          Wait(2),
                          Func(self.toggleFullscreen, 1280, 800, 0, 0, 1), 
                          Wait(3),
                          Func(self.status.setText, "Switching to Window Mode"),
                          Wait(2),
                          Func(self.toggleFullscreen, 800, 600, 50, 50, 0))
        toggle.start()

    def toggleFullscreen(self, width, height, posX, posY, full):
        winProps = WindowProperties()
        winProps.setOrigin(posX, posY)
        winProps.setSize(width, height)
        winProps.setFullscreen(full)
        self.win.requestProperties(winProps)

        if full:
            self.status.setText("Fullscreen Mode")
        else:
            self.status.setText("Window Mode");
