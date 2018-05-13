
#from pandac.PandaModules import loadPrcFileData
#loadPrcFileData('', 'load-display tinydisplay')

import sys, numpy
import direct.directbase.DirectStart

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3, CollideMask
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32, GeoMipTerrain
from panda3d.core import CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletVehicle
from panda3d.bullet import ZUp
from functools import reduce

class NeuralNetGA:

    def __init__(self,shape, activation):
        self.shape = shape
        self.hidden_layers_size = self.shape[1:-1]
        self.input_size = self.shape[0]
        self.output_size = self.shape[-1]
        self.activation_functions = {'tanh': lambda x: numpy.tanh(x/4.)*10.}
        self.activation = self.activation_functions[activation]

        self.weights_dimensions = [(self.shape[i],self.shape[i+1]) for i in range(len(self.shape)-1)]
        #print(self.weights_dimensions)
        self.weights_indices = numpy.cumsum([dimensions[0]*dimensions[1] for dimensions in self.weights_dimensions])
        #print(self.weights_indices)
        # F2(W2*F(Wx))

    def predict(self,X):
        #print(X,self.weights)
        #print([X] + self.weights)
        self.y = reduce(lambda x,y: numpy.vectorize(self.activation)(numpy.dot(x,y)), [X] + self.weights)
        print(X,self.y)
        return self.y

    def assign_weights(self, weights_dict):
        #print(enumerate(numpy.split(numpy.array(weights_dict.values()),self.weights_indices[:-1]).tolist()))
        #print(numpy.array(list(weights_dict.values())))
        #print(numpy.split(numpy.array(list(weights_dict.values())),self.weights_indices))
        self.weights = [numpy.reshape(weights,self.weights_dimensions[i]) for i, weights in enumerate(numpy.split(numpy.array(list(weights_dict.values())),self.weights_indices[:-1])) if list(weights)]#.tolist()
        #print(self.weights)

    def evaluate_task(self, **kargs):
        self.assign_weights(kargs)
        self.model = lambda X: self.predict(X)
        self.task_output = self.task(self.model)
        return self.task_output

    def fit(self, task):
        self.task = task
        best_params, best_score, score_results, hist, log = maximize(evaluate_task,{'w%d'%i:numpy.linspace(-100,100,1000) for i in range(self.weights_indices[-1])},{})


class Game(DirectObject):

  def __init__(self, model):
    self.model = model
    base.setBackgroundColor(0.1, 0.1, 0.8, 1)
    base.setFrameRateMeter(True)

    base.cam.setPos(0, -20, 4)
    base.cam.lookAt(0, 0, 0)

    # Light
    alight = AmbientLight('ambientLight')
    alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
    alightNP = render.attachNewNode(alight)

    dlight = DirectionalLight('directionalLight')
    dlight.setDirection(Vec3(1, 1, -1))
    dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
    dlightNP = render.attachNewNode(dlight)

    render.clearLight()
    render.setLight(alightNP)
    render.setLight(dlightNP)

    # Input
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f1', self.toggleWireframe)
    self.accept('f2', self.toggleTexture)
    self.accept('f3', self.toggleDebug)
    self.accept('f5', self.doScreenshot)

    inputState.watchWithModifiers('forward', 'w')
    inputState.watchWithModifiers('left', 'a')
    inputState.watchWithModifiers('reverse', 's')
    inputState.watchWithModifiers('right', 'd')
    inputState.watchWithModifiers('turnLeft', 'q')
    inputState.watchWithModifiers('turnRight', 'e')

    # Task
    taskMgr.add(self.update, 'updateWorld')

    # Physics
    self.setup()

  # _____HANDLER_____

  def doExit(self):
    self.cleanup()
    sys.exit(1)

  def doReset(self):
    self.cleanup()
    self.setup()

  def toggleWireframe(self):
    base.toggleWireframe()

  def toggleTexture(self):
    base.toggleTexture()

  def toggleDebug(self):
    if self.debugNP.isHidden():
      self.debugNP.show()
    else:
      self.debugNP.hide()

  def doScreenshot(self):
    base.screenshot('Bullet')

  # ____TASK___

  def calculate_moves(self):
      self.y = self.model.predict(self.x)
      self.moves = self.y > 0 # 0.5

  def processInput(self, dt):
    engineForce = 0.0
    brakeForce = 0.0
    if self.moves[0]:#inputState.isSet('forward'):
      engineForce = 1000.0
      brakeForce = 0.0

    if not self.moves[0]:#inputState.isSet('reverse'):
      engineForce = 0.0
      brakeForce = 100.0

    if self.moves[1]:#inputState.isSet('turnLeft'):
      self.steering += dt * self.steeringIncrement
      self.steering = min(self.steering, self.steeringClamp)

    if not self.moves[1]:#inputState.isSet('turnRight'):
      self.steering -= dt * self.steeringIncrement
      self.steering = max(self.steering, -self.steeringClamp)
    """
    if inputState.isSet('forward'):
      engineForce = 1000.0
      brakeForce = 0.0

    if inputState.isSet('reverse'):
      engineForce = 0.0
      brakeForce = 100.0

    if inputState.isSet('turnLeft'):
      self.steering += dt * self.steeringIncrement
      self.steering = min(self.steering, self.steeringClamp)

    if inputState.isSet('turnRight'):
      self.steering -= dt * self.steeringIncrement
      self.steering = max(self.steering, -self.steeringClamp)
    """
    # Apply steering to front wheels
    self.vehicle.setSteeringValue(self.steering, 0);
    self.vehicle.setSteeringValue(self.steering, 1);

    # Apply engine and brake to rear wheels
    self.vehicle.applyEngineForce(engineForce, 2);
    self.vehicle.applyEngineForce(engineForce, 3);
    self.vehicle.setBrake(brakeForce, 2);
    self.vehicle.setBrake(brakeForce, 3);

  def raycast(self):
      """pFrom = render.getRelativePoint(self.yugoNP,Point3(0,0,0))#Point3(0,0,0)
      pFrom -= Point3(0,0,pFrom[2])
      pRel = render.getRelativePoint(base.cam,self.yugoNP.getPos())  # FIXME THIS IS IT!! get rid of z component
      pRel -= Point3(0,0,pRel[2])
      p45 = Point3(pRel[0] - pRel[1], pRel[1] + pRel[0],0)
      pn45 = Point3(pRel[0] + pRel[1], pRel[1] - pRel[0],0)
      #print(render.getRelativePoint(self.yugoNP,Point3(0,0,0)))
      #print(dir(self.yugoNP))
      pTo = [pFrom + pn45, pFrom + pRel, pFrom + p45]#[pFrom + Vec3(-10,10,0)*999,pFrom + Vec3(0,10,0)*999,pFrom + Vec3(10,10,0)*999]# FIXME should be relative to front of car, getting cloe! #self.yugoNP.getPosDelta()*99999]#[Point3(-10,10,0) * 99999,Point3(0,10,0) * 99999,Point3(10,10,0) * 99999]
      #self.ray = CollisionRay(0,0,0,100,0,0)
      result = [self.world.rayTestClosest(pFrom,pt) for pt in pTo]
      #print(dir(self.yugoNP))
      #print(result.getHitPos())
      return tuple([res.getHitPos().length() for res in result])
      """#queue = CollisionHandlerQueue()
      #traverser.addCollider(fromObject, queue)
      #traverser.traverse(render)
      #queue.sortEntries()
      #for entry in queue.getEntries():
      #print(entry)
      #print(result.getHitPos())
      #if result.getNode() != None:
      #print(self.yugoNP.getPos(result.getNode()))
      #print(self.cTrav)
      self.cTrav.traverse(render)
      entries = list(self.colHandler.getEntries())
      entries.sort(key=lambda y: y.getSurfacePoint(render).getY())
      #for entry in entries:      print(entry.getFromNodePath().getName())
      if entries:# and len(result) > 1:
          for r in entries:
              if r.getIntoNodePath().getName() == 'Box' and r.getFromNodePath().getName() in ['ray%d'%i for i in range(3)]:
                  self.ray_col_vec_dict[r.getFromNodePath().getName()].append(numpy.linalg.norm(list(r.getSurfacePoint(r.getFromNodePath()))[:-1]))
      self.ray_col_vec_dict = {k: (min(self.ray_col_vec_dict[k]) if len(self.ray_col_vec_dict[k]) >= 1 else 10000) for k in self.ray_col_vec_dict}
      self.x = numpy.array(list(self.ray_col_vec_dict.values()))
      #return entries

  def update(self, task):
    dt = globalClock.getDt()

    self.raycast()
    self.calculate_moves()
    self.ray_col_vec_dict = {k:[] for k in self.ray_col_vec_dict}
    self.processInput(dt)
    self.world.doPhysics(dt, 10, 0.008)




        #print(dir(result[1]))
        #print(numpy.linalg.norm(list(result[1].getSurfacePoint(result[1].getFromNodePath()))[:-1]))
    #base.camera.setPos(0,-40,10)
    #print self.vehicle.getWheel(0).getRaycastInfo().isInContact()
    #print self.vehicle.getWheel(0).getRaycastInfo().getContactPointWs()

    #print self.vehicle.getChassis().isKinematic()

    return task.cont

  def cleanup(self):
    self.world = None
    self.worldNP.removeNode()

  def setup(self):
    self.worldNP = render.attachNewNode('World')

    # World
    self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
    self.debugNP.show()

    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
    self.world.setDebugNode(self.debugNP.node())

    terrain = GeoMipTerrain("mySimpleTerrain")
    terrain.setHeightfield("./models/heightfield_2.png")
    terrain.getRoot().reparentTo(self.worldNP)#render)
    terrain.generate()

    # Plane
    shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
    np.node().addShape(shape)
    np.setPos(0, 0, -1)
    np.setCollideMask(BitMask32.allOn())

    self.world.attachRigidBody(np.node())

    # Chassis
    shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
    ts = TransformState.makePos(Point3(0, 0, 0.5))

    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Vehicle'))
    np.node().addShape(shape, ts)
    np.setPos(0, 0, 1)
    np.node().setMass(800.0)
    np.node().setDeactivationEnabled(False)

    self.world.attachRigidBody(np.node())

    #np.node().setCcdSweptSphereRadius(1.0)
    #np.node().setCcdMotionThreshold(1e-7)
    self.cTrav = CollisionTraverser()
    # Vehicle
    self.vehicle = BulletVehicle(self.world, np.node())
    self.vehicle.setCoordinateSystem(ZUp)
    self.yugoNP = loader.loadModel('models/yugo/yugo.egg')
    self.yugoNP.reparentTo(np)
    self.colHandler = CollisionHandlerQueue()
    self.ray_col_np = {}
    self.ray_col_vec_dict = {}
    for ray_dir in range(-1,2): # populate collision rays
        self.ray = CollisionRay()
        self.ray.setOrigin(ray_dir,0.5,0.5)
        self.ray.setDirection(ray_dir,1,0)
        self.ray_col = CollisionNode('ray%d'%(ray_dir+1))
        self.ray_col.addSolid(self.ray)
        self.ray_col.setFromCollideMask(BitMask32.allOn())#(0x0f))#CollideMask.bit(0)
        #self.ray_col.setIntoCollideMask(CollideMask.allOff())
        self.ray_col_np['ray%d'%(ray_dir+1)] = self.yugoNP.attachNewNode(self.ray_col)
        self.cTrav.addCollider(self.ray_col_np['ray%d'%(ray_dir+1)],self.colHandler)
        self.ray_col_np['ray%d'%(ray_dir+1)].show()
        self.ray_col_vec_dict['ray%d'%(ray_dir+1)] = []
    self.world.attachVehicle(self.vehicle)
    self.cTrav.showCollisions(render)



    # FIXME
    base.camera.reparentTo(self.yugoNP)

    # Right front wheel
    np = loader.loadModel('models/yugo/yugotireR.egg')
    np.reparentTo(self.worldNP)
    self.addWheel(Point3( 0.70,  1.05, 0.3), True, np)

    # Left front wheel
    np = loader.loadModel('models/yugo/yugotireL.egg')
    np.reparentTo(self.worldNP)
    self.addWheel(Point3(-0.70,  1.05, 0.3), True, np)

    # Right rear wheel
    np = loader.loadModel('models/yugo/yugotireR.egg')
    np.reparentTo(self.worldNP)
    self.addWheel(Point3( 0.70, -1.05, 0.3), False, np)

    # Left rear wheel
    np = loader.loadModel('models/yugo/yugotireL.egg')
    np.reparentTo(self.worldNP)
    self.addWheel(Point3(-0.70, -1.05, 0.3), False, np)

    # Steering info
    self.steering = 0.0            # degree
    self.steeringClamp = 45.0      # degree
    self.steeringIncrement = 120.0 # degree per second

    # Box
    for i,j in [(0,8),(-3,5),(6,-5),(8,3),(-4,-4)]:
        shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        # https://discourse.panda3d.org/t/wall-collision-help/23606
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Box'))
        np.node().setMass(1.0)
        np.node().addShape(shape)
        np.setPos(i, j, 2)
        np.setCollideMask(BitMask32.allOn())#(0x0f))

        self.world.attachRigidBody(np.node())
        self.boxNP = np
        #self.colHandler2 = CollisionHandlerQueue()


        visualNP = loader.loadModel('models/box.egg')
        visualNP.reparentTo(self.boxNP)
    #self.cTrav.addCollider(self.boxNP,self.colHandler)

    """
    aNode = CollisionNode("TheRay")

    self.ray = CollisionRay()
    self.ray.setOrigin( self.yugoNP.getPos() )
    self.ray.setDirection( Vec3(0, 10, 0) )
    #self.ray.show()


    aNodePath = self.yugoNP.attachNewNode( CollisionNode("TheRay") )
    aNodePath.node().addSolid(self.ray)
    aNodePath.show()
    """
    #aNode.addSolid(self.ray)
    #self.ray = CollisionRay(0,0,0,10,0,0)
    #self.ray.reparentTo(self.yugoNP)
    #self.rayColl = CollisionNode('PlayerRay')
    #self.rayColl.addSolid(self.ray)

    #self.playerRayNode = self.yugoNP.attachNewNode( self.rayColl )
    #self.playerRayNode.show()

    #base.myTraverser.addCollider (self.playerRayNode, base.floor)
    #base.floor.addCollider( self.playerRayNode, self.yugoNP)
    """
    MyEvent=CollisionHandlerFloor()
    MyEvent.setReach(100)
    MyEvent.setOffset(15.0)

    aNode = CollisionNode("TheRay")
    ray = CollisionRay()
    ray.setOrigin( self.boxNP.getPos() )
    ray.setDirection( Vec3(10, 0, 0) )

    aNode.addSolid(ray)
    aNodePath = MyModel.attachNewNode( aNode )

    Collision = ( aNode, "TheRay" )
    Collision[0].setFromCollideMask( BitMask32.bit( 1 ) )
    """
  def addWheel(self, pos, front, np):
    wheel = self.vehicle.createWheel()

    wheel.setNode(np.node())
    wheel.setChassisConnectionPointCs(pos)
    wheel.setFrontWheel(front)

    wheel.setWheelDirectionCs(Vec3(0, 0, -1))
    wheel.setWheelAxleCs(Vec3(1, 0, 0))
    wheel.setWheelRadius(0.25)
    wheel.setMaxSuspensionTravelCm(40.0)

    wheel.setSuspensionStiffness(40.0)
    wheel.setWheelsDampingRelaxation(2.3)
    wheel.setWheelsDampingCompression(4.4)
    wheel.setFrictionSlip(100.0);
    wheel.setRollInfluence(0.1)

model = NeuralNetGA([3,4,4,2],'tanh')
model.assign_weights({'w%d'%i:numpy.random.rand()-0.5 for i in range(36)})
game = Game(model)
base.run()
