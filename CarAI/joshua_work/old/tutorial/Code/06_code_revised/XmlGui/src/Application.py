from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from GuiBuilder import GuiHandler, GuiFromXml

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        handler = MyHandler()
        GuiFromXml("gui.xml", handler)

class MyHandler(GuiHandler):
    def __init__(self):
        GuiHandler.__init__(self)
        self.gender = [0] 

    def setName(self):
        title = ""
        if self.gender[0]:
            title = "Mister"
        else:
            title = "Miss"

        self.controls["nameLbl"]["text"] = "Hello " + title + " " + self.controls["nameEnt"].get() + "!"
