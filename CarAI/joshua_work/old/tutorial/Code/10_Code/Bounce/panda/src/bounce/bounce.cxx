// Filename: bounce.cxx
// Created by:  clang (10Oct10)
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

#include "bounce.h"

TypeHandle Bounce::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: Bounce::update
//       Access: Public
//  Description: Performs a simulation step. 
//               Updates velocity and position.
////////////////////////////////////////////////////////////////////
void Bounce::
update() {
  if (_z <= bounce_floor_level)
    _velocity = _rand.random_real(0.7f) + 0.1f;
  
  _z = _z + _velocity;
  _velocity -= 0.01f;
}
