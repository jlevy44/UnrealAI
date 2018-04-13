#pragma once

#include <pandaFramework.h>
#include <pandaSystem.h>
#include <btBulletDynamicsCommon.h>

class SmileyMotionState : public btMotionState
{
public:
	SmileyMotionState(const btTransform& start, const NodePath& sm);
	virtual ~SmileyMotionState() {}
	virtual void getWorldTransform(btTransform& trans) const;
	virtual void setWorldTransform(const btTransform& trans);

protected:
	btTransform transform;
	NodePath smiley;
};