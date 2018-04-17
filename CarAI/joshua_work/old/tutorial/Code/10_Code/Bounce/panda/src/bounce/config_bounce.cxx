// Filename: config_bounce.cxx
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

#include "config_bounce.h"
#include "bounce.h"
#include "dconfig.h"

Configure(config_bounce);
NotifyCategoryDef(bounce, "");

ConfigureFn(config_bounce) {
  init_libbounce();
}

ConfigVariableDouble bounce_floor_level
("bounce-floor-level", 0);

////////////////////////////////////////////////////////////////////
//     Function: init_libbounce
//  Description: Initializes the library.  This must be called at
//               least once before any of the functions or classes in
//               this library can be used.  Normally it will be
//               called by the static initializers and need not be
//               called explicitly, but special cases exist.
////////////////////////////////////////////////////////////////////
void
init_libbounce() {
  static bool initialized = false;
  if (initialized) {
    return;
  }
  initialized = true;

  Bounce::init_type();
}

