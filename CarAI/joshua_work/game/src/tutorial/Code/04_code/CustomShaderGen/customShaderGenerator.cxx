#include "customShaderGenerator.h"

TypeHandle CustomShaderGenerator::_type_handle;

CustomShaderGenerator::CustomShaderGenerator(PT(GraphicsStateGuardianBase) gsg, PT(GraphicsOutputBase) host) :
  ShaderGenerator(gsg, host) {
}

CustomShaderGenerator::~CustomShaderGenerator() {
}

CPT(RenderAttrib) CustomShaderGenerator::
synthesize_shader(const RenderState *rs) {
  analyze_renderstate(rs);
  reset_register_allocator();

  pgraph_cat.info() << "Generating shader for render state " << rs << "\n";

  // These variables will hold the results of register allocation.

  char *normal_vreg = 0;
  char *ntangent_vreg = 0;
  char *ntangent_freg = 0;
  char *nbinormal_vreg = 0;
  char *nbinormal_freg = 0;
  char *htangent_vreg = 0;
  char *hbinormal_vreg = 0;
  pvector<char *> texcoord_vreg;
  pvector<char *> texcoord_freg;
  pvector<char *> tslightvec_freg;
  char *world_position_freg = 0;
  char *world_normal_freg = 0;
  char *eye_position_freg = 0;
  char *eye_normal_freg = 0;

  if (_vertex_colors) {
    _vcregs_used = 1;
    _fcregs_used = 1;
  }

  // Generate the shader's text.

  ostringstream text;

  text << "//Cg\n";

  text << "void vshader(\n";
  const TextureAttrib *texture = DCAST(TextureAttrib, rs->get_attrib_def(TextureAttrib::get_class_slot()));
  const TexGenAttrib *tex_gen = DCAST(TexGenAttrib, rs->get_attrib_def(TexGenAttrib::get_class_slot()));
  for (int i=0; i<_num_textures; i++) {
    texcoord_vreg.push_back(alloc_vreg());
    texcoord_freg.push_back(alloc_freg());
    text << "\t in float4 vtx_texcoord" << i << " : " << texcoord_vreg[i] << ",\n";
    text << "\t out float4 l_texcoord" << i << " : " << texcoord_freg[i] << ",\n";
  }
  if (_vertex_colors) {
    text << "\t in float4 vtx_color : COLOR,\n";
    text << "\t out float4 l_color : COLOR,\n";
  }
  if (_need_world_position || _need_world_normal) {
    text << "\t uniform float4x4 trans_model_to_world,\n";
  }
  if (_need_world_position) {
    world_position_freg = alloc_freg();
    text << "\t out float4 l_world_position : " << world_position_freg << ",\n";
  }
  if (_need_world_normal) {
    world_normal_freg = alloc_freg();
    text << "\t out float4 l_world_normal : " << world_normal_freg << ",\n";
  }
  if (_need_eye_position) {
    text << "\t uniform float4x4 trans_model_to_view,\n";
    eye_position_freg = alloc_freg();
    text << "\t out float4 l_eye_position : " << eye_position_freg << ",\n";
  }
  if (_need_eye_normal) {
    eye_normal_freg = alloc_freg();
    text << "\t uniform float4x4 tpose_view_to_model,\n";
    text << "\t out float4 l_eye_normal : " << eye_normal_freg << ",\n";
  }
  if (_map_index_height >= 0 || _need_world_normal || _need_eye_normal) {
    normal_vreg = alloc_vreg();
    text << "\t in float4 vtx_normal : " << normal_vreg << ",\n";
  }
  if (_map_index_height >= 0) {
    htangent_vreg = alloc_vreg();
    hbinormal_vreg = alloc_vreg();
    if (_map_index_normal == _map_index_height) {
      ntangent_vreg = htangent_vreg;
      nbinormal_vreg = hbinormal_vreg;
    }
    text << "\t in float4 vtx_tangent" << _map_index_height << " : " << htangent_vreg << ",\n";
    text << "\t in float4 vtx_binormal" << _map_index_height << " : " << hbinormal_vreg << ",\n";
    text << "\t uniform float4 mspos_view,\n";
    text << "\t out float3 l_eyevec,\n";
  }
  if (_lighting) {
    if (_map_index_normal >= 0) {
      // If we had a height map and it used the same stage, that means we already have those inputs.
      if (_map_index_normal != _map_index_height) {
        ntangent_vreg = alloc_vreg();
        nbinormal_vreg = alloc_vreg();
        text << "\t in float4 vtx_tangent" << _map_index_normal << " : " << ntangent_vreg << ",\n";
        text << "\t in float4 vtx_binormal" << _map_index_normal << " : " << nbinormal_vreg << ",\n";
      }
      ntangent_freg = alloc_freg();
      nbinormal_freg = alloc_freg();
      text << "\t out float4 l_tangent : " << ntangent_freg << ",\n";
      text << "\t out float4 l_binormal : " << nbinormal_freg << ",\n";
    }
    if (_shadows) {
      for (int i=0; i<(int)_dlights.size(); i++) {
        if (_dlights[i]->_shadow_caster) {
          text << "\t uniform float4x4 trans_model_to_clip_of_dlight" << i << ",\n";
          text << "\t out float4 l_dlightcoord" << i << ",\n";
        }
      }
      for (int i=0; i<(int)_slights.size(); i++) {
        if (_slights[i]->_shadow_caster) {
          text << "\t uniform float4x4 trans_model_to_clip_of_slight" << i << ",\n";
          text << "\t out float4 l_slightcoord" << i << ",\n";
        }
      }
    }
  }
  text << "\t float4 vtx_position : POSITION,\n";
  text << "\t out float4 l_position : POSITION,\n";
  text << "\t uniform float4x4 mat_modelproj\n";
  text << ") {\n";

  text << "\t l_position = mul(mat_modelproj, vtx_position);\n";
  if (_need_world_position) {
    text << "\t l_world_position = mul(trans_model_to_world, vtx_position);\n";
  }
  if (_need_world_normal) {
    text << "\t l_world_normal = mul(trans_model_to_world, vtx_normal);\n";
  }
  if (_need_eye_position) {
    text << "\t l_eye_position = mul(trans_model_to_view, vtx_position);\n";
  }
  if (_need_eye_normal) {
    text << "\t l_eye_normal.xyz = mul((float3x3)tpose_view_to_model, vtx_normal.xyz);\n";
    text << "\t l_eye_normal.w = 0;\n";
  }
  for (int i=0; i<_num_textures; i++) {
    if (!tex_gen->has_stage(texture->get_on_stage(i))) {
      text << "\t l_texcoord" << i << " = vtx_texcoord" << i << ";\n";
    }
  }
  if (_vertex_colors) {
    text << "\t l_color = vtx_color;\n";
  }
  if (_lighting && (_map_index_normal >= 0)) {
    text << "\t l_tangent.xyz = mul((float3x3)tpose_view_to_model, vtx_tangent" << _map_index_normal << ".xyz);\n";
    text << "\t l_tangent.w = 0;\n";
    text << "\t l_binormal.xyz = mul((float3x3)tpose_view_to_model, -vtx_binormal" << _map_index_normal << ".xyz);\n";
    text << "\t l_binormal.w = 0;\n";
  }
  if (_shadows) {
    text << "\t float4x4 biasmat = {0.5f, 0.0f, 0.0f, 0.5f, 0.0f, 0.5f, 0.0f, 0.5f, 0.0f, 0.0f, 0.5f, 0.5f, 0.0f, 0.0f, 0.0f, 1.0f};\n";
    for (int i=0; i<(int)_dlights.size(); i++) {
      if (_dlights[i]->_shadow_caster) {
        text << "\t l_dlightcoord" << i << " = mul(biasmat, mul(trans_model_to_clip_of_dlight" << i << ", vtx_position));\n";
      }
    }
    for (int i=0; i<(int)_slights.size(); i++) {
      if (_slights[i]->_shadow_caster) {
        text << "\t l_slightcoord" << i << " = mul(biasmat, mul(trans_model_to_clip_of_slight" << i << ", vtx_position));\n";
      }
    }
  }
  if (_map_index_height >= 0) {
    text << "\t float3 eyedir = mspos_view.xyz - vtx_position.xyz;\n";
    text << "\t l_eyevec.x = dot(vtx_tangent" << _map_index_height << ".xyz, eyedir);\n";
    text << "\t l_eyevec.y = dot(vtx_binormal" << _map_index_height << ".xyz, eyedir);\n";
    text << "\t l_eyevec.z = dot(vtx_normal.xyz, eyedir);\n";
    text << "\t l_eyevec = normalize(l_eyevec);\n";
  }
  text << "}\n\n";

  text << "void fshader(\n";
  if (_need_world_position) {
    text << "\t in float4 l_world_position : " << world_position_freg << ",\n";
  }
  if (_need_world_normal) {
    text << "\t in float4 l_world_normal : " << world_normal_freg << ",\n";
  }
  if (_need_eye_position) { 
    text << "\t in float4 l_eye_position : " << eye_position_freg << ",\n";
  }
  if (_need_eye_normal) {
    text << "\t in float4 l_eye_normal : " << eye_normal_freg << ",\n";
  }
  const TexMatrixAttrib *tex_matrix = DCAST(TexMatrixAttrib, rs->get_attrib_def(TexMatrixAttrib::get_class_slot()));
  for (int i=0; i<_num_textures; i++) {
    TextureStage *stage = texture->get_on_stage(i);
    Texture *tex = texture->get_on_texture(stage);
    nassertr(tex != NULL, NULL);
    text << "\t uniform sampler" << texture_type_as_string(tex->get_texture_type()) << " tex_" << i << ",\n";
    if (!tex_gen->has_stage(stage)) {
      text << "\t in float4 l_texcoord" << i << " : " << texcoord_freg[i] << ",\n";
    }
    if (tex_matrix->has_stage(stage)) {
      text << "\t uniform float4x4 texmat_" << i << ",\n";
    }
  }
  if (_lighting && (_map_index_normal >= 0)) {
    text << "\t in float3 l_tangent : " << ntangent_freg << ",\n";
    text << "\t in float3 l_binormal : " << nbinormal_freg << ",\n";
  }
  if (_lighting) {
    for (int i=0; i<(int)_alights.size(); i++) {
      text << "\t uniform float4 alight_alight" << i << ",\n";
    }
    for (int i=0; i<(int)_dlights.size(); i++) {
      text << "\t uniform float4x4 dlight_dlight" << i << "_rel_view,\n";
      if (_shadows && _dlights[i]->_shadow_caster) {
        if (_use_shadow_filter) {
          text << "\t uniform sampler2DShadow k_dlighttex" << i << ",\n";
        } else {
          text << "\t uniform sampler2D k_dlighttex" << i << ",\n";
        }
        text << "\t float4 l_dlightcoord" << i << ",\n";
      }
    }
    for (int i=0; i<(int)_plights.size(); i++) {
      text << "\t uniform float4x4 plight_plight" << i << "_rel_view,\n";
    }
    for (int i=0; i<(int)_slights.size(); i++) {
      text << "\t uniform float4x4 slight_slight" << i << "_rel_view,\n";
      text << "\t uniform float4   satten_slight" << i << ",\n";
      if (_shadows && _slights[i]->_shadow_caster) {
        if (_use_shadow_filter) {
          text << "\t uniform sampler2DShadow k_slighttex" << i << ",\n";
        } else {
          text << "\t uniform sampler2D k_slighttex" << i << ",\n";
        }
        text << "\t float4 l_slightcoord" << i << ",\n";
      }
    }
    if (_need_material_props) {
      text << "\t uniform float4x4 attr_material,\n";
    }
    if (_have_specular) {
      if (_material->get_local()) {
        text << "\t uniform float4 mspos_view,\n";
      } else {
        text << "\t uniform float4 row1_view_to_model,\n";
      }
    }
  }
  if (_map_index_height >= 0) {
    text << "\t float3 l_eyevec,\n";
  }
  if (_out_aux_any) {
    text << "\t out float4 o_aux : COLOR1,\n";
  }
  text << "\t out float4 o_color : COLOR0,\n";
  if (_vertex_colors) {
    text << "\t in float4 l_color : COLOR,\n";
  } else {
    text << "\t uniform float4 attr_color,\n";
  }
  for (int i=0; i<_num_clip_planes; ++i) {
    text << "\t uniform float4 clipplane_" << i << ",\n";
  }
  text << "\t uniform float4 attr_colorscale\n";
  text << ") {\n";
  // Clipping first!
  for (int i=0; i<_num_clip_planes; ++i) {
    text << "\t if (l_world_position.x * clipplane_" << i << ".x + l_world_position.y ";
    text << "* clipplane_" << i << ".y + l_world_position.z * clipplane_" << i << ".z + clipplane_" << i << ".w <= 0) {\n";
    text << "\t discard;\n";
    text << "\t }\n";
  }
  text << "\t float4 result;\n";
  if (_out_aux_any) {
    text << "\t o_aux = float4(0,0,0,0);\n";
  }
  // Now generate any texture coordinates according to TexGenAttrib. If it has a TexMatrixAttrib, also transform them.
  for (int i=0; i<_num_textures; i++) {
    TextureStage *stage = texture->get_on_stage(i);
    if (tex_gen != NULL && tex_gen->has_stage(stage)) {
      switch (tex_gen->get_mode(stage)) {
        case TexGenAttrib::M_world_position:
          text << "\t float4 l_texcoord" << i << " = l_world_position;\n";
          break;
        case TexGenAttrib::M_world_normal:
          text << "\t float4 l_texcoord" << i << " = l_world_normal;\n";
          break;
        case TexGenAttrib::M_eye_position:
          text << "\t float4 l_texcoord" << i << " = l_eye_position;\n";
          break;
        case TexGenAttrib::M_eye_normal:
          text << "\t float4 l_texcoord" << i << " = l_eye_normal;\n";
          text << "\t l_texcoord" << i << ".w = 1.0f;\n";
          break;
        default:
          pgraph_cat.error() << "Unsupported TexGenAttrib mode\n";
          text << "\t float4 l_texcoord" << i << " = float4(0, 0, 0, 0);\n";
      }
    }
    if (tex_matrix != NULL && tex_matrix->has_stage(stage)) {
      text << "\t l_texcoord" << i << " = mul(texmat_" << i << ", l_texcoord" << i << ");\n";
      text << "\t l_texcoord" << i << ".xyz /= l_texcoord" << i << ".w;\n";
    }
  }
  text << "\t // Fetch all textures.\n";
  if (_map_index_height >= 0 && parallax_mapping_samples > 0) {
    Texture *tex = texture->get_on_texture(texture->get_on_stage(_map_index_height));
    nassertr(tex != NULL, NULL);
    text << "\t float4 tex" << _map_index_height << " = tex" << texture_type_as_string(tex->get_texture_type());
    text << "(tex_" << _map_index_height << ", l_texcoord" << _map_index_height << ".";
    switch(tex->get_texture_type()) {
      case Texture::TT_cube_map:
      case Texture::TT_3d_texture: text << "xyz"; break;
      case Texture::TT_2d_texture: text << "xy";  break;
      case Texture::TT_1d_texture: text << "x";   break;
    }
    text << ");\n\t float3 parallax_offset = l_eyevec.xyz * (tex" << _map_index_height;
    if (_map_height_in_alpha) {
      text << ".aaa";
    } else {
      text << ".rgb";
    }
    text << " * 2.0 - 1.0) * " << parallax_mapping_scale << ";\n";
    // Additional samples
    for (int i=0; i<parallax_mapping_samples-1; i++) {
      text << "\t parallax_offset = l_eyevec.xyz * (parallax_offset + (tex" << _map_index_height;
      if (_map_height_in_alpha) {
        text << ".aaa";
      } else {
        text << ".rgb";
      }
      text << " * 2.0 - 1.0)) * " << 0.5 * parallax_mapping_scale << ";\n";
    }
  }
  for (int i=0; i<_num_textures; i++) {
    if (i != _map_index_height) {
      Texture *tex = texture->get_on_texture(texture->get_on_stage(i));
      nassertr(tex != NULL, NULL);
      // Parallax mapping pushes the texture coordinates of the other textures away from the camera.
      if (_map_index_height >= 0 && parallax_mapping_samples > 0) {
        text << "\t l_texcoord" << i << ".xyz -= parallax_offset;\n";
      }
      text << "\t float4 tex" << i << " = tex" << texture_type_as_string(tex->get_texture_type());
      text << "(tex_" << i << ", l_texcoord" << i << ".";
      switch(tex->get_texture_type()) {
        case Texture::TT_cube_map:
        case Texture::TT_3d_texture: text << "xyz"; break;
        case Texture::TT_2d_texture: text << "xy";  break;
        case Texture::TT_1d_texture: text << "x";   break;
      }
      text << ");\n";
    }
  }
  if (_lighting) {
    if (_map_index_normal >= 0) {
      text << "\t // Translate tangent-space normal in map to view-space.\n";
      text << "\t float3 tsnormal = ((float3)tex" << _map_index_normal << " * 2) - 1;\n";
      text << "\t l_eye_normal.xyz *= tsnormal.z;\n";
      text << "\t l_eye_normal.xyz += l_tangent * tsnormal.x;\n";
      text << "\t l_eye_normal.xyz += l_binormal * tsnormal.y;\n";
      text << "\t l_eye_normal.xyz  = normalize(l_eye_normal.xyz);\n";
    } else {
      text << "\t // Correct the surface normal for interpolation effects\n";
      text << "\t l_eye_normal.xyz = normalize(l_eye_normal.xyz);\n";
    }
  }
  if (_out_aux_normal) {
    text << "\t // Output the camera-space surface normal\n";
    text << "\t o_aux.rgb = (l_eye_normal.xyz*0.5) + float3(0.5,0.5,0.5);\n";
  }
  if (_lighting) {
    text << "\t // Begin view-space light calculations\n";
    text << "\t float ldist,lattenv,langle;\n";
    text << "\t float4 lcolor,lspec,lvec,lpoint,latten,ldir,leye,lhalf;";
    if (_shadows) {
      text << "\t float lshad;\n";
    }
    if (_separate_ambient_diffuse) {
      if (_have_ambient) {
        text << "\t float4 tot_ambient = float4(0,0,0,0);\n";
      }
      if (_have_diffuse) {
        text << "\t float4 tot_diffuse = float4(0,0,0,0);\n";
      }
    } else {
      if (_have_ambient || _have_diffuse) {
        text << "\t float4 tot_diffuse = float4(0,0,0,0);\n";
      }
    }
    if (_have_specular) {
      text << "\t float4 tot_specular = float4(0,0,0,0);\n";
      if (_material->has_specular()) {
        text << "\t float shininess = attr_material[3].w;\n";
      } else {
        text << "\t float shininess = 50; // no shininess specified, using default\n";
      }
    }
    for (int i=0; i<(int)_alights.size(); i++) {
      text << "\t // Ambient Light " << i << "\n";
      text << "\t lcolor = alight_alight" << i << ";\n";
      if (_separate_ambient_diffuse && _have_ambient) {
        text << "\t tot_ambient += lcolor;\n";
      } else if(_have_diffuse) {
        text << "\t tot_diffuse += lcolor;\n";
      }
    }
    for (int i=0; i<(int)_dlights.size(); i++) {
      text << "\t // Directional Light " << i << "\n";
      text << "\t lcolor = dlight_dlight" << i << "_rel_view[0];\n";
      text << "\t lspec  = dlight_dlight" << i << "_rel_view[1];\n";
      text << "\t lvec   = dlight_dlight" << i << "_rel_view[2];\n";
      text << "\t lcolor *= saturate(0.5 * dot(l_eye_normal.xyz, lvec.xyz) + 0.5);\n";
      if (_shadows && _dlights[i]->_shadow_caster) {
        if (_use_shadow_filter) {
          text << "\t lshad = shadow2DProj(k_dlighttex" << i << ", l_dlightcoord" << i << ").r;\n";
        } else {
          text << "\t lshad = tex2Dproj(k_dlighttex" << i << ", l_dlightcoord" << i << ").r > l_dlightcoord" << i << ".z / l_dlightcoord" << i << ".w;\n";
        }
        text << "\t lcolor *= lshad;\n";
        text << "\t lspec *= lshad;\n";
      }
      if (_have_diffuse) {
        text << "\t tot_diffuse += lcolor;\n";
      }
      if (_have_specular) {
        if (_material->get_local()) {
          text << "\t lhalf  = normalize(lvec - normalize(l_eye_position));\n";
        } else {
          text << "\t lhalf = dlight_dlight" << i << "_rel_view[3];\n";
        }
        text << "\t lspec *= pow(saturate(dot(l_eye_normal.xyz, lhalf.xyz)), shininess);\n";
        text << "\t tot_specular += lspec;\n";
      }
    }
    for (int i=0; i<(int)_plights.size(); i++) {
      text << "\t // Point Light " << i << "\n";
      text << "\t lcolor = plight_plight" << i << "_rel_view[0];\n";
      text << "\t lspec  = plight_plight" << i << "_rel_view[1];\n";
      text << "\t lpoint = plight_plight" << i << "_rel_view[2];\n";
      text << "\t latten = plight_plight" << i << "_rel_view[3];\n";
      text << "\t lvec   = lpoint - l_eye_position;\n";
      text << "\t ldist = length(float3(lvec));\n";
      text << "\t lvec /= ldist;\n";
      text << "\t lattenv = 1/(latten.x + latten.y*ldist + latten.z*ldist*ldist);\n";
      text << "\t lcolor *= lattenv * saturate(0.5 * dot(l_eye_normal.xyz, lvec.xyz) + 0.5);\n";
      if (_have_diffuse) {
        text << "\t tot_diffuse += lcolor;\n";
      }
      if (_have_specular) {
        if (_material->get_local()) {
          text << "\t lhalf  = normalize(lvec - normalize(l_eye_position));\n";
        } else {
          text << "\t lhalf = normalize(lvec - float4(0,1,0,0));\n";
        }
        text << "\t lspec *= lattenv;\n";
        text << "\t lspec *= pow(saturate(dot(l_eye_normal.xyz, lhalf.xyz)), shininess);\n";
        text << "\t tot_specular += lspec;\n";
      }
    }
    for (int i=0; i<(int)_slights.size(); i++) {
      text << "\t // Spot Light " << i << "\n";
      text << "\t lcolor = slight_slight" << i << "_rel_view[0];\n";
      text << "\t lspec  = slight_slight" << i << "_rel_view[1];\n";
      text << "\t lpoint = slight_slight" << i << "_rel_view[2];\n";
      text << "\t ldir   = slight_slight" << i << "_rel_view[3];\n";
      text << "\t latten = satten_slight" << i << ";\n";
      text << "\t lvec   = lpoint - l_eye_position;\n";
      text << "\t ldist  = length(float3(lvec));\n";
      text << "\t lvec /= ldist;\n";
      text << "\t langle = saturate(dot(ldir.xyz, lvec.xyz));\n";
      text << "\t lattenv = 1/(latten.x + latten.y*ldist + latten.z*ldist*ldist);\n";
      text << "\t lattenv *= pow(langle, latten.w);\n";
      text << "\t if (langle < ldir.w) lattenv = 0;\n";
      text << "\t lcolor *= lattenv * saturate(0.5 * dot(l_eye_normal.xyz, lvec.xyz) + 0.5);\n";
      if (_shadows && _slights[i]->_shadow_caster) {
        if (_use_shadow_filter) {
          text << "\t lshad = shadow2DProj(k_slighttex" << i << ", l_slightcoord" << i << ").r;\n";
        } else {
          text << "\t lshad = tex2Dproj(k_slighttex" << i << ", l_slightcoord" << i << ").r > l_slightcoord" << i << ".z / l_slightcoord" << i << ".w;\n";
        }
        text << "\t lcolor *= lshad;\n";
        text << "\t lspec *= lshad;\n";
      }

      if (_have_diffuse) {
        text << "\t tot_diffuse += lcolor;\n";
      }
      if (_have_specular) {
        if (_material->get_local()) {
          text << "\t lhalf  = normalize(lvec - normalize(l_eye_position));\n";
        } else {
          text << "\t lhalf = normalize(lvec - float4(0,1,0,0));\n";
        }
        text << "\t lspec *= lattenv;\n";
        text << "\t lspec *= pow(saturate(dot(l_eye_normal.xyz, lhalf.xyz)), shininess);\n";
        text << "\t tot_specular += lspec;\n";
      }
    }

    const LightRampAttrib *light_ramp = DCAST(LightRampAttrib, rs->get_attrib_def(LightRampAttrib::get_class_slot()));
    switch (light_ramp->get_mode()) {
    case LightRampAttrib::LRT_single_threshold:
      {
        float t = light_ramp->get_threshold(0);
        float l0 = light_ramp->get_level(0);
        text << "\t // Single-threshold light ramp\n";
        text << "\t float lr_in = dot(tot_diffuse.rgb, float3(0.33,0.34,0.33));\n";
        text << "\t float lr_scale = (lr_in < " << t << ") ? 0.0 : (" << l0 << "/lr_in);\n";
        text << "\t tot_diffuse = tot_diffuse * lr_scale;\n";
        break;
      }
    case LightRampAttrib::LRT_double_threshold:
      {
        float t0 = light_ramp->get_threshold(0);
        float t1 = light_ramp->get_threshold(1);
        float l0 = light_ramp->get_level(0);
        float l1 = light_ramp->get_level(1);
        float l2 = light_ramp->get_level(2);
        text << "\t // Double-threshold light ramp\n";
        text << "\t float lr_in = dot(tot_diffuse.rgb, float3(0.33,0.34,0.33));\n";
        text << "\t float lr_out = " << l0 << "\n";
        text << "\t if (lr_in > " << t0 << ") lr_out=" << l1 << ";\n";
        text << "\t if (lr_in > " << t1 << ") lr_out=" << l2 << ";\n";
        text << "\t tot_diffuse = tot_diffuse * (lr_out / lr_in);\n";
        break;
      }
    }
    text << "\t // Begin view-space light summation\n";
    if (_have_emission) {
      if (_map_index_glow >= 0) {
        text << "\t result = attr_material[2] * saturate(2 * (tex" << _map_index_glow << ".a - 0.5));\n";
      } else {
        text << "\t result = attr_material[2];\n";
      }
    } else {
      if (_map_index_glow >= 0) {
        text << "\t result = saturate(2 * (tex" << _map_index_glow << ".a - 0.5));\n";
      } else {
        text << "\t result = float4(0,0,0,0);\n";
      }
    }
    if ((_have_ambient)&&(_separate_ambient_diffuse)) {
      if (_material->has_ambient()) {
        text << "\t result += tot_ambient * attr_material[0];\n";
      } else if (_vertex_colors) {
        text << "\t result += tot_ambient * l_color;\n";
      } else if (_flat_colors) {
        text << "\t result += tot_ambient * attr_color;\n";
      } else {
        text << "\t result += tot_ambient;\n";
      }
    }
    if (_have_diffuse) {
      if (_material->has_diffuse()) {
        text << "\t result += tot_diffuse * attr_material[1];\n";
      } else if (_vertex_colors) {
        text << "\t result += tot_diffuse * l_color;\n";
      } else if (_flat_colors) {
        text << "\t result += tot_diffuse * attr_color;\n";
      } else {
        text << "\t result += tot_diffuse;\n";
      }
    }
    if (light_ramp->get_mode() == LightRampAttrib::LRT_default) {
      text << "\t result = saturate(result);\n";
    }
    text << "\t // End view-space light calculations\n";

    // Combine in alpha, which bypasses lighting calculations.
    // Use of lerp here is a workaround for a radeon driver bug.
    if (_calc_primary_alpha) {
      if (_vertex_colors) {
        text << "\t result.a = l_color.a;\n";
      } else if (_flat_colors) {
        text << "\t result.a = attr_color.a;\n";
      } else {
        text << "\t result.a = 1;\n";
      }
    }
  } else {
    if (_vertex_colors) {
      text << "\t result = l_color;\n";
    } else if (_flat_colors) {
      text << "\t result = attr_color;\n";
    } else {
      text << "\t result = float4(1,1,1,1);\n";
    }
  }

  // Loop first to see if something is using primary_color or last_saved_result.
  bool have_saved_result = false;
  bool have_primary_color = false;
  for (int i=0; i<_num_textures; i++) {
    TextureStage *stage = texture->get_on_stage(i);
    if (stage->get_mode() != TextureStage::M_combine) continue;
    if (stage->uses_primary_color() && !have_primary_color) {
      text << "\t float4 primary_color = result;\n";
      have_primary_color = true;
    }
    if (stage->uses_last_saved_result() && !have_saved_result) {
      text << "\t float4 last_saved_result = result;\n";
      have_saved_result = true;
    }
  }

  // Now loop through the textures to compose our magic blending formulas.
  for (int i=0; i<_num_textures; i++) {
    TextureStage *stage = texture->get_on_stage(i);
    switch (stage->get_mode()) {
    case TextureStage::M_modulate:
    case TextureStage::M_modulate_glow:
    case TextureStage::M_modulate_gloss:
      text << "\t result *= tex" << i << ";\n";
      break;
    case TextureStage::M_decal:
      text << "\t result.rgb = lerp(result, tex" << i << ", tex" << i << ".a).rgb;\n";
      break;
    case TextureStage::M_blend: {
      LVecBase4f c = stage->get_color();
      text << "\t result.rgb = lerp(result, tex" << i << " * float4("
           << c[0] << ", " << c[1] << ", " << c[2] << ", " << c[3] << "), tex" << i << ".r).rgb;\n";
      break; }
    case TextureStage::M_replace:
      text << "\t result = tex" << i << ";\n";
      break;
    case TextureStage::M_add:
      text << "\t result.rgb += tex" << i << ".rgb;\n";
      if (_calc_primary_alpha) {
        text << "\t result.a   *= tex" << i << ".a;\n";
      }
      break;
    case TextureStage::M_combine:
      text << "\t result.rgb = ";
      if (stage->get_combine_rgb_mode() != TextureStage::CM_undefined) {
        text << combine_mode_as_string(stage, stage->get_combine_rgb_mode(), false, i);
      } else {
        text << "tex" << i << ".rgb";
      }
      if (stage->get_rgb_scale() != 1) {
        text << " * " << stage->get_rgb_scale();
      }
      text << ";\n\t result.a = ";
      if (stage->get_combine_alpha_mode() != TextureStage::CM_undefined) {
        text << combine_mode_as_string(stage, stage->get_combine_alpha_mode(), true, i);
      } else {
        text << "tex" << i << ".a";
      }
      if (stage->get_alpha_scale() != 1) {
        text << " * " << stage->get_alpha_scale();
      }
      text << ";\n";
      break;
    case TextureStage::M_blend_color_scale:
      text << "\t result.rgb = lerp(result, tex" << i << " * attr_colorscale, tex" << i << ".r).rgb;\n";
      break;
    default:
      break;
    }
    if (stage->get_saved_result() && have_saved_result) {
      text << "\t last_saved_result = result;\n";
    }
  }
  // Apply the color scale.
  text << "\t result *= attr_colorscale;\n";

  if (_subsume_alpha_test) {
    const AlphaTestAttrib *alpha_test = DCAST(AlphaTestAttrib, rs->get_attrib_def(AlphaTestAttrib::get_class_slot()));
    text << "\t // Shader includes alpha test:\n";
    double ref = alpha_test->get_reference_alpha();
    switch (alpha_test->get_mode()) {
    case RenderAttrib::M_never:          text<<"\t discard;\n";
    case RenderAttrib::M_less:           text<<"\t if (result.a >= "<<ref<<") discard;\n";
    case RenderAttrib::M_equal:          text<<"\t if (result.a != "<<ref<<") discard;\n";
    case RenderAttrib::M_less_equal:     text<<"\t if (result.a >  "<<ref<<") discard;\n";
    case RenderAttrib::M_greater:        text<<"\t if (result.a <= "<<ref<<") discard;\n";
    case RenderAttrib::M_not_equal:      text<<"\t if (result.a == "<<ref<<") discard;\n";
    case RenderAttrib::M_greater_equal:  text<<"\t if (result.a <  "<<ref<<") discard;\n";
    }
  }

  if (_out_primary_glow) {
    if (_map_index_glow >= 0) {
      text << "\t result.a = tex" << _map_index_glow << ".a;\n";
    } else {
      text << "\t result.a = 0.5;\n";
    }
  }
  if (_out_aux_glow) {
    if (_map_index_glow >= 0) {
      text << "\t o_aux.a = tex" << _map_index_glow << ".a;\n";
    } else {
      text << "\t o_aux.a = 0.5;\n";
    }
  }

  if (_lighting) {
    if (_have_specular) {
      if (_material->has_specular()) {
        text << "\t tot_specular *= attr_material[3];\n";
      }
      if (_map_index_gloss >= 0) {
        text << "\t tot_specular *= tex" << _map_index_gloss << ".a;\n";
      }
      text << "\t result.rgb = result.rgb + tot_specular.rgb;\n";
    }
  }

  const LightRampAttrib *light_ramp = DCAST(LightRampAttrib, rs->get_attrib_def(LightRampAttrib::get_class_slot()));
  switch (light_ramp->get_mode()) {
  case LightRampAttrib::LRT_hdr0:
    text << "\t result.rgb = (result*result*result + result*result + result) / (result*result*result + result*result + result + 1);\n";
    break;
  case LightRampAttrib::LRT_hdr1:
    text << "\t result.rgb = (result*result + result) / (result*result + result + 1);\n";
    break;
  case LightRampAttrib::LRT_hdr2:
    text << "\t result.rgb = result / (result + 1);\n";
    break;
  default: break;
  }

  // The multiply is a workaround for a radeon driver bug.
  // It's annoying as heck, since it produces an extra instruction.
  text << "\t o_color = result * 1.000001;\n";
  if (_subsume_alpha_test) {
    text << "\t // Shader subsumes normal alpha test.\n";
  }
  if (_disable_alpha_write) {
    text << "\t // Shader disables alpha write.\n";
  }
  text << "}\n";

  // Insert the shader into the shader attrib.
  CPT(RenderAttrib) shattr = create_shader_attrib(text.str());
  if (_subsume_alpha_test) {
    shattr=DCAST(ShaderAttrib, shattr)->set_flag(ShaderAttrib::F_subsume_alpha_test, true);
  }
  if (_disable_alpha_write) {
    shattr=DCAST(ShaderAttrib, shattr)->set_flag(ShaderAttrib::F_disable_alpha_write, true);
  }
  clear_analysis();
  reset_register_allocator();
  return shattr;
}
