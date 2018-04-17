#include "SmileyTask.h"
#include "SmileyMotionState.h"

SmileyTask::SmileyTask(NodePath& rndr, NodePath& sm, btDynamicsWorld* world)
{
	smileyCount = 0;
	smiley = sm;
	render = rndr;
	btWorld = world;
}

AsyncTask::DoneStatus SmileyTask::addSmiley(GenericAsyncTask* task, void* data)
{
	SmileyTask* add = reinterpret_cast<SmileyTask*>(data);
	NodePath render = add->render;
	NodePath smiley = add->smiley;
	btDynamicsWorld* btWorld = add->btWorld;

	NodePath sm = render.attach_new_node("smiley-instance");
	Randomizer rnd;
	smiley.instance_to(sm);

	btCollisionShape* shape = new btSphereShape(btScalar(1));

	btTransform trans;
	trans.setIdentity();
	trans.setOrigin(btVector3(rnd.random_real(40) - 20, rnd.random_real(20) + 10, rnd.random_real(60) - 30));

	btScalar mass(10);
	btVector3 inertia(0, 0, 0);
	shape->calculateLocalInertia(mass, inertia);

	SmileyMotionState* ms = new SmileyMotionState(trans, sm);
	btRigidBody::btRigidBodyConstructionInfo info(mass, ms, shape, inertia);
	info.m_restitution = btScalar(0.5f);
	info.m_friction = btScalar(0.7f);
	btRigidBody* body = new btRigidBody(info);

	btWorld->addRigidBody(body);

	add->smileyCount++;
	if (add->smileyCount == 100)
		return AsyncTask::DS_done;

	return AsyncTask::DS_again;
}