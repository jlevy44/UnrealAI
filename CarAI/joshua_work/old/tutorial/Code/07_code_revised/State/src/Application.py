from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from AppState import AppState

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        state = AppState("Application")
        state.request("Menu")
