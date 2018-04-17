#pragma once

#include <pandaFramework.h>
#include <pandaSystem.h>
#include <asyncTask.h>
#include <btBulletDynamicsCommon.h>

class Application
{
public:
	Application(int argc, char* argv[]);
	~Application();
	void run();

private:
	void init();
	void setupBullet();
	void addGround();
	void updateBullet();

private:
	NodePath render;
	NodePath cam;
	NodePath smiley;
	WindowFramework* win;
	PandaFramework framework;
	
	btBroadphaseInterface*	broadphase;
	btCollisionDispatcher*	dispatcher;
	btConstraintSolver*	solver;
	btDefaultCollisionConfiguration* collisionConfiguration;
	btDynamicsWorld* btWorld;
};

class BulletTask
{
public:
	static AsyncTask::DoneStatus updateBullet(GenericAsyncTask* task, void* data);
};