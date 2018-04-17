#define OTHER_LIBS interrogatedb:c dconfig:c dtoolconfig:m \
                   dtoolutil:c dtoolbase:c dtool:m prc:c

#define USE_PACKAGES 
#define BUILDING_DLL BUILDING_PANDABOUNCE

#begin lib_target
  #define TARGET bounce
  #define LOCAL_LIBS \
    putil
    
  #define COMBINED_SOURCES $[TARGET]_composite1.cxx 

  #define SOURCES \
    config_bounce.h \
    bounce.I bounce.h
    
  #define INCLUDED_SOURCES \
    config_bounce.cxx \
    bounce.cxx

  #define INSTALL_HEADERS \
    bounce.I bounce.h

  #define IGATESCAN all

#end lib_target
