#include <cardMaker.h>
#include "Application.h"
#include "SmileyTask.h"

Application::Application(int argc, char* argv[])
{
	framework.open_framework(argc, argv);
	win = framework.open_window();
	cam = win->get_camera_group();
	render = win->get_render();
}

Application::~Application()
{
}

void Application::run()
{
	init();
	framework.main_loop();
	framework.close_framework();
}

void Application::init()
{
	setupBullet();
	PT(AsyncTaskManager) taskMgr = AsyncTaskManager::get_global_ptr();

	smiley = win->load_model(framework.get_models(), "smiley");
	SmileyTask* add = new SmileyTask(render, smiley, btWorld);
	PT(GenericAsyncTask) addSmiley = new GenericAsyncTask("AddSmiley", &SmileyTask::addSmiley, add);
	addSmiley->set_delay(0.01);
	taskMgr->add(addSmiley);

	PT(GenericAsyncTask) bt = new GenericAsyncTask("UpdateBullet", &BulletTask::updateBullet, btWorld);
	taskMgr->add(bt);

	addGround();
	cam.set_pos(0, -100, 10);
}

void Application::setupBullet()
{
	collisionConfiguration = new btDefaultCollisionConfiguration();
	dispatcher = new btCollisionDispatcher(collisionConfiguration);
	broadphase = new btDbvtBroadphase();

	btSequentialImpulseConstraintSolver* sol = new btSequentialImpulseConstraintSolver;
	solver = sol;

	btWorld = new btDiscreteDynamicsWorld(dispatcher, broadphase, solver, collisionConfiguration);
	btWorld->setGravity(btVector3(0, -9.81f, 0));
}

void Application::addGround()
{
	CardMaker cm("ground");
	cm.set_frame(-500, 500, -500, 500);
	NodePath ground = render.attach_new_node(cm.generate());
	ground.look_at(0, 0, -1);
	ground.set_color(0.2f, 0.4f, 0.8f);

	btCollisionShape* shape = new btBoxShape(btVector3(btScalar(500), btScalar(0.5f), btScalar(500)));

	btTransform trans;
	trans.setIdentity();
	trans.setOrigin(btVector3(0, -0.5f, 0));

	btDefaultMotionState* ms = new btDefaultMotionState(trans);
	btScalar mass(0);
	btVector3 inertia(0, 0, 0);
	btRigidBody::btRigidBodyConstructionInfo info(mass, ms, shape, inertia);
	info.m_restitution = btScalar(0.5f);
	info.m_friction = btScalar(0.7f);
	btRigidBody* body = new btRigidBody(info);

	btWorld->addRigidBody(body);
}

AsyncTask::DoneStatus BulletTask::updateBullet(GenericAsyncTask* task, void* data)
{
	btScalar dt(ClockObject::get_global_clock()->get_dt());
	btDynamicsWorld* btWorld = reinterpret_cast<btDynamicsWorld*>(data);
	btWorld->stepSimulation(dt);
	return AsyncTask::DS_cont;
}