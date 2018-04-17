#pragma once

#include <pandaFramework.h>
#include <pandaSystem.h>
#include <asyncTask.h>
#include <randomizer.h>
#include <btBulletDynamicsCommon.h>

class SmileyTask
{
public:
	SmileyTask(NodePath& rndr, NodePath& sm, btDynamicsWorld* world);
	static AsyncTask::DoneStatus addSmiley(GenericAsyncTask* task, void* data);

	NodePath render;
	NodePath smiley;
	btDynamicsWorld* btWorld;
	int smileyCount;
};