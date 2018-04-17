// Filename: bounce.h
// Created by: clang (10Oct10)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

#ifndef BOUNCE_H
#define BOUNCE_H

#include "pandabase.h"
#include "typedObject.h"
#include "randomizer.h"

////////////////////////////////////////////////////////////////////
//       Class : Bounce
// Description : Bouncing simulator for jumping smiley demo.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDABOUNCE Bounce : public TypedObject {
PUBLISHED:
  INLINE Bounce();
  INLINE ~Bounce();

  INLINE float get_z();
  INLINE void set_z(float z);
  void update();

private:
  float _velocity;
  float _z;
  Randomizer _rand;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedObject::init_type();
    register_type(_type_handle, "Bounce",
                  TypedObject::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:

  static TypeHandle _type_handle;

};

#include "bounce.I"

#endif

