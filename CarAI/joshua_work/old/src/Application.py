from direct.showbase.ShowBase import ShowBase
from Scene import Scene
from panda3d.core import loadPrcFileData

loadPrcFileData("", "win-size 1200 600")
loadPrcFileData("", "audio-libary-name p3openal-audio")

class Application(ShowBase):
	def __init__(self):
		ShowBase.__init__(self,Scene)

		self.Scene = Scene


Application(Scene())
