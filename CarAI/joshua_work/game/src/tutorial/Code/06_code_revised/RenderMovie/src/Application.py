from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

loadPrcFileData("", "audio-library-name p3openal_audio")

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        cm = CardMaker("plane")
        cm.setFrame(-1, 1, -1, 1)
        
        plane = render2d.attachNewNode(cm.generate())
        movie = loader.loadTexture("movie.avi")
        sound = loader.loadSfx("movie.avi")
       
        plane.setTexture(movie)
        plane.setTexScale(TextureStage.getDefault(), movie.getTexScale())        
        
        movie.setLoop(0)
        movie.synchronizeTo(sound)
        sound.play()
