from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

vertices = [Vec3(1, 0, 1), Vec3(-1, 0, 1), Vec3(-1, 0, -1), Vec3(1, 0, -1)]
texcoords = [Vec2(1, 1), Vec2(0, 1), Vec2(0, 0), Vec2(1, 0)]

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        format = GeomVertexFormat.getV3t2()
        geomData = GeomVertexData("box", format, Geom.UHStatic)
        vertexWriter = GeomVertexWriter(geomData, "vertex")
        uvWriter = GeomVertexWriter(geomData, "texcoord")

        for pos, tex in zip(vertices, texcoords):
            vertexWriter.addData3f(pos)
            uvWriter.addData2f(tex)

        triangles = GeomTriangles(Geom.UHStatic)
        triangles.addVertices(0, 1, 2)
        triangles.closePrimitive()
        triangles.addVertices(2, 3, 0)
        triangles.closePrimitive()

        geom = Geom(geomData)
        geom.addPrimitive(triangles)
        node = GeomNode("box")
        node.addGeom(geom)
        box = render.attachNewNode(node)
        texture = loader.loadTexture("crate.png")
        box.setTexture(texture)

        self.cam.setPos(0, -5, 0)
