#version 330 compatibility
#extension GL_ARB_shader_texture_lod : enable
/* MakeUp - deferred.vsh
Render: Ambient occlusion, volumetric clouds

Javier Garduño - GNU Lesser General Public License v3.0
*/

#define DEFERRED_SHADER

#include "/common/deferred_vertex.glsl"
