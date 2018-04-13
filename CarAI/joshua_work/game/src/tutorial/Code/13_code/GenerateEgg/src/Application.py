from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.egg import *

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.generateEgg()
        model = loader.loadModel("generated")
        model.reparentTo(render)

        dirLight = DirectionalLight("directional")
        dirNode = render.attachNewNode(dirLight)
        dirNode.setHpr(20, 20, 20)
        render.setLight(dirNode)
        self.cam.setPos(5, -5, -5)
        self.cam.lookAt(model)

    def generateEgg(self):
        eggRoot = EggData()
        meshGroup = EggGroup("Mesh")
        vertexPool = EggVertexPool("Vertices")
        eggRoot.addChild(vertexPool)
        eggRoot.addChild(meshGroup)

        # this does NOT use Panda3D's coordinate system!
        vertices = (Point3D(-1, 1, 1),
                    Point3D(-1, -1, 1),
                    Point3D(1, -1, 1),
                    Point3D(1, 1, 1),
                    Point3D(1, 1, -1),
                    Point3D(1, -1, -1),
                    Point3D(-1, -1, -1),
                    Point3D(-1, 1, -1))

        texcoords = (Point2D(0, 1),
                     Point2D(0, 0),
                     Point2D(1, 0),
                     Point2D(1, 1))

        faces = ((0, 1, 2, 3),
                 (4, 5, 6, 7),
                 (7, 6, 1, 0),
                 (3, 2, 5, 4),
                 (7, 0, 3, 4),
                 (1, 6, 5, 2))

        texture = EggTexture("color", Filename("../textures/texture.png"))

        for face in faces:
            polygon = EggPolygon()
            meshGroup.addChild(polygon)
            for index, uv in zip(face, texcoords):
                vertex = vertexPool.makeNewVertex(vertices[index])
                vertex.setUv(uv)
                polygon.addVertex(vertex)
            polygon.addTexture(texture)
            polygon.recomputePolygonNormal()
            polygon.triangulateInPlace(True)

        eggRoot.writeEgg(Filename("../models/generated.egg"))
