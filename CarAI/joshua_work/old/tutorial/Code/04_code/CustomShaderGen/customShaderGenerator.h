#ifndef CUSTOMSHADERGENERATOR_H
#define CUSTOMSHADERGENERATOR_H

#include "shaderGenerator.h"

class EXPCL_PANDA_PGRAPHNODES CustomShaderGenerator : public ShaderGenerator {
PUBLISHED:
  CustomShaderGenerator(PT(GraphicsStateGuardianBase) gsg, PT(GraphicsOutputBase) host);
  virtual ~CustomShaderGenerator();
  virtual CPT(RenderAttrib) synthesize_shader(const RenderState *rs);

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    ShaderGenerator::init_type();
    register_type(_type_handle, "CustomShaderGenerator",
                  ShaderGenerator::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

 private:
  static TypeHandle _type_handle;
};

#endif