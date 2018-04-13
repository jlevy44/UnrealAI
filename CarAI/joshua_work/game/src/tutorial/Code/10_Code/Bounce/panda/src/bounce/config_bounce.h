// Filename: config_bounce.h
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

#ifndef CONFIG_BOUNCE_H
#define CONFIG_BOUNCE_H

#include "pandabase.h"
#include "notifyCategoryProxy.h"
#include "configVariableDouble.h"

NotifyCategoryDecl(bounce, EXPCL_PANDABOUNCE, EXPTP_PANDABOUNCE);

extern ConfigVariableDouble bounce_floor_level;

extern EXPCL_PANDABOUNCE void init_libbounce();

#endif


