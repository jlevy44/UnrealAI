
#from pandac.PandaModules import loadPrcFileData
#loadPrcFileData('', 'load-display tinydisplay')

import sys, numpy, os
import pickle
import direct.directbase.DirectStart

from direct.showbase.DirectObject import DirectObject
from direct.showbase.InputStateGlobal import inputState
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3, CollideMask
from panda3d.core import Vec4
from panda3d.core import Point3
from panda3d.core import TransformState
from panda3d.core import BitMask32, GeoMipTerrain
from panda3d.core import CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue, CollisionBox

from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletVehicle
from panda3d.bullet import ZUp
from functools import reduce

class NeuralNetGA:

    def __init__(self, shape, activation):
        self.shape = shape
        self.hidden_layers_size = self.shape[1:-1]
        self.input_size = self.shape[0]
        self.output_size = self.shape[-1]
        self.activation_functions = {'tanh': lambda x: numpy.tanh(x/4.)*10.}
        self.activation = self.activation_functions[activation]

        self.weights_dimensions = [(self.shape[i],self.shape[i+1]) for i in range(len(self.shape)-1)]
        #print(self.weights_dimensions)
        self.weights_indices = numpy.cumsum([dimensions[0]*dimensions[1] for dimensions in self.weights_dimensions])
        self.bias_indices = numpy.cumsum(self.shape[1:])
        #print(self.weights_indices)
        # F2(W2*F(Wx))

    def predict(self,X):
        #print(X,self.weights)
        #print([X] + self.weights)
        #self.y = reduce(lambda x,y: numpy.vectorize(self.activation)(numpy.dot(x,y)), [X] + self.weights)
        current_layer = X
        #print(len(self.weights),len(self.bias))
        for i in range(len(self.weights)):
            #print(i)
            current_layer = self.activation(numpy.dot(current_layer,self.weights[i]) + self.bias[i])
        self.y = current_layer
        #print(X,self.y)
        return self.y

    def assign_weights(self, weights_dict, bias_dict):
        #print(enumerate(numpy.split(numpy.array(weights_dict.values()),self.weights_indices[:-1]).tolist()))
        #print(numpy.array(list(weights_dict.values())))
        #print(numpy.split(numpy.array(list(weights_dict.values())),self.weights_indices))
        #print(weights_dict,bias_dict)
        self.weights = [numpy.reshape(weights,self.weights_dimensions[i]) for i, weights in enumerate(numpy.split(numpy.array(list(weights_dict.values())),self.weights_indices[:-1])) if list(weights)]#.tolist()
        self.bias = numpy.split(numpy.array(list(bias_dict.values())),self.bias_indices[:-1])
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

  def endLoop(self):
      self.penalized_distance = self.distance*(numpy.exp(-self.time_max_steering/self.total_time))
      pickle.dump(self.penalized_distance,open('distance.p','wb'))
      sys.exit()
      #quit()
      #print("Distance was: ",self.distance)
      #os.execv(sys.executable,['python']+[__file__])
      #taskMgr.running = False

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
      #print(self.y)
      self.moves = self.y > 0 # 0.5

  def processInput(self, dt):
    engineForce = 0.0
    brakeForce = 0.0
    if self.moves[0]:#inputState.isSet('forward'):
      engineForce = 2000.0 # 1000.
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

  def check_collisions(self):
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
      #print(entries)
      entries.sort(key=lambda y: y.getSurfacePoint(render).getY())
      #for entry in entries:      print(entry.getFromNodePath().getName())
      if entries:# and len(result) > 1:
          #print(entries)
          for r in entries:

              #print(r.getIntoNodePath().getName())
              if r.getIntoNodePath().getName() == 'Plane' and r.getFromNodePath().getName() == 'yugo_box':
                  self.endLoop()
              if r.getIntoNodePath().getName() == 'Plane' and r.getFromNodePath().getName() in ['ray%d'%i for i in range(self.n_rays)]: #Box
                  self.ray_col_vec_dict[r.getFromNodePath().getName()].append(numpy.linalg.norm(list(r.getSurfacePoint(r.getFromNodePath()))[:-1]))
      self.ray_col_vec_dict = {k: (min(self.ray_col_vec_dict[k]) if len(self.ray_col_vec_dict[k]) >= 1 else 10000) for k in self.ray_col_vec_dict}
      self.x = numpy.array(list(self.ray_col_vec_dict.values()))
      #print(self.x)
      result = self.world.contactTest(self.yugoNP.node())
      #print(result.getNumContacts())
      #print(dir(self.yugoNP))
      #return entries

  def check_prevPos(self):
      if len(self.prevPos) > 80:
          #print(self.prevPos)
          #print(numpy.linalg.norm(self.prevPos[-1] - self.prevPos[0]))
          if numpy.linalg.norm(self.prevPos[-1] - self.prevPos[0]) < 4.5:
              #print("ERROR")
              self.endLoop()

          del self.prevPos[0:len(self.prevPos) - 80]

  def update(self, task):

    self.prevPos.append(self.yugoNP.getPos(render))
    dx = numpy.linalg.norm(self.prevPos[-1] - self.prevPos[-2])
    self.distance += dx
    self.distance_text.setText('Distance=%f'%(self.distance))
    #print(len(self.prevPos))

    dt = globalClock.getDt()
    self.total_time += dt
    if abs(self.steering) == abs(self.steeringClamp):
        self.time_max_steering += dt
    self.time_text.setText('TotalTime=%f'%(self.total_time))
    self.time_maxsteer_text.setText('TotalTimeMaxSteer=%f'%(self.time_max_steering))
    #self.penalized_distance = self.distance*(1.-numpy.exp(-self.time_max_steering/self.total_time))
    if self.distance > 10000:
        self.endLoop()
    self.check_prevPos()
    self.speed = dx/dt
    self.speed_text.setText('Speed=%f'%(self.speed))

    self.check_collisions()
    self.calculate_moves()
    self.ray_col_vec_dict = {k:[] for k in self.ray_col_vec_dict}
    self.processInput(dt)
    self.world.doPhysics(dt, 10, 0.008)
    # FIXME KEEP TRACK OF TOTAL DEGREES TURNED AND PENALIZE
    #self.doReset()




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
    self.distance_text = OnscreenText(text='Distance=0', pos = (0.85,0.85), scale = 0.05, mayChange=1)#Directxxxxxx(distance='Distance=%d'%(0))
    self.speed_text = OnscreenText(text='Speed=0', pos = (0.85,0.80), scale = 0.05, mayChange=1)#Directxxxxxx(distance='Distance=%d'%(0))
    self.time_text = OnscreenText(text='TotalTime=0', pos = (0.85,0.75), scale = 0.05, mayChange=1)#Directxxxxxx(distance='Distance=%d'%(0))
    self.time_maxsteer_text = OnscreenText(text='TotalTimeMaxSteer=0', pos = (0.85,0.70), scale = 0.05, mayChange=1)#Directxxxxxx(distance='Distance=%d'%(0))

    self.total_time = 0.
    self.time_max_steering = 0.
    # World
    self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
    self.debugNP.show()

    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
    self.world.setDebugNode(self.debugNP.node())

    #terrain = GeoMipTerrain("mySimpleTerrain")
    #terrain.setHeightfield("./models/heightfield_2.png")
    #terrain.getRoot().reparentTo(self.worldNP)#render)
    #terrain.generate()

    # Plane
    shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
    np.node().addShape(shape)
    np.setPos(0, 0, -1)
    np.setCollideMask(BitMask32.allOn())

    self.world.attachRigidBody(np.node())

    #np = self.worldNP.attachNewNode(BulletRigidBodyNode('Track'))
    #np.node().setMass(5000.0)
    #np.setPos(3, 0, 10)
    #np.setCollideMask(BitMask32.allOn())#(0x0f))
    #self.track = BulletVehicle(self.world, np.node())
    #self.track.setCoordinateSystem(ZUp)
    self.track_np = loader.loadModel('models/race_track_2.egg') # https://discourse.panda3d.org/t/panda3d-and-bullet-physics/15724/10
    self.track_np.setPos(-72, -7, -3.5)
    self.track_np.setScale(10)
    self.track_np.reparentTo(render)

    self.track_np.setCollideMask(BitMask32.allOn())#(0))#.allOn())
    self.world.attachRigidBody(np.node())
    self.track_np = np
    #self.track_np.show()

    # Chassis
    shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
    ts = TransformState.makePos(Point3(0, 0, 0.5))

    np = self.worldNP.attachNewNode(BulletRigidBodyNode('Vehicle'))
    np.node().addShape(shape, ts)
    np.setPos(0, 0, 0.05)
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
    self.yugoNP.setCollideMask(BitMask32(0))#.allOn())
    self.yugoNP.reparentTo(np)
    self.colHandler = CollisionHandlerQueue()


    # travel distance
    self.distance = 0.

    """self.sphere = CollisionSphere(0,0,0,2)
    self.sphere_col = CollisionNode('yugo')
    self.sphere_col.addSolid(self.sphere)
    self.sphere_col.setFromCollideMask(BitMask32.allOn())
    self.sphere_col_np = self.yugoNP.attachNewNode(self.sphere_col)
    self.cTrav.addCollider(self.sphere_col_np,self.colHandler)
    self.sphere_col_np.show()"""

    self.yugo_col = CollisionNode('yugo_box')
    self.yugo_col.addSolid(CollisionBox(Point3(0,0,0.7),0.9, 1.6, 0.05))
    self.yugo_col.setFromCollideMask(BitMask32(1))
    self.box_col_np = self.yugoNP.attachNewNode(self.yugo_col)
    self.cTrav.addCollider(self.box_col_np,self.colHandler)
    self.box_col_np.show()




    self.ray_col_np = {}
    self.ray_col_vec_dict = {}
    self.n_rays = self.model.shape[0]
    for i,ray_dir in enumerate(numpy.linspace(-numpy.pi/4,numpy.pi/4,self.n_rays)): # populate collision rays
        #print(ray_dir)
        self.ray = CollisionRay()
        y_dir, x_dir = numpy.cos(ray_dir), numpy.sin(ray_dir)
        self.ray.setOrigin(1.3*x_dir,1.3*y_dir,0.5)
        self.ray.setDirection(x_dir,y_dir,0)
        self.ray_col = CollisionNode('ray%d'%(i))
        self.ray_col.addSolid(self.ray)
        self.ray_col.setFromCollideMask(BitMask32.allOn())#(0x0f))#CollideMask.bit(0)
        #self.ray_col.setIntoCollideMask(CollideMask.allOff())
        self.ray_col_np['ray%d'%(i)] = self.yugoNP.attachNewNode(self.ray_col)
        self.cTrav.addCollider(self.ray_col_np['ray%d'%(i)],self.colHandler)
        self.ray_col_np['ray%d'%(i)].show()
        self.ray_col_vec_dict['ray%d'%(i)] = []
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
    self.steeringClamp = 38.0#45.0      # degree
    self.steeringIncrement = 105.0#120.0 # degree per second

    # add previous positions
    self.prevPos = []
    self.prevPos.append(self.yugoNP.getPos(render))

    # Box
    """
    for i,j in [(0,8),(-3,5),(6,-5),(8,3),(-4,-4),(0,0)]:
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

#while True:
# GA model
try:
    weights, bias, architecture, activation = pickle.load(open('weights.p','rb'))
    print("MODEL LOADED", weights)
except:
    weights, bias, architecture, activation =  ({'w%d'%i:numpy.random.rand()-0.5 for i in range(36)},{'b%d'%i:numpy.random.rand()-0.5 for i in range(10)},[3,4,4,2],'tanh')

model = NeuralNetGA(architecture,activation)
model.assign_weights(weights, bias)
game = Game(model)
base.run()
