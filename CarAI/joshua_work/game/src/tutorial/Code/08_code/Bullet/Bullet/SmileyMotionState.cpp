#include "SmileyMotionState.h"

SmileyMotionState::SmileyMotionState(const btTransform& start, const NodePath& sm)
{
	transform = start;
	smiley = sm;
}

void SmileyMotionState::getWorldTransform(btTransform& trans) const
{
	trans = transform;
}

void SmileyMotionState::setWorldTransform(const btTransform& trans)
{
	transform = trans;
	btQuaternion rot = trans.getRotation();
	LQuaternionf prot(rot.w(), -rot.x(), -rot.z(), -rot.y());
	smiley.set_hpr(prot.get_hpr());
	btVector3 pos = trans.getOrigin();
	smiley.set_pos(pos.x(), pos.z(), pos.y());
}