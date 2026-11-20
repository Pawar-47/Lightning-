#version 330 compatibility
#extension GL_ARB_shader_texture_lod : enable
/* MakeUp - gbuffers_damagedblock.vsh
Render: Damaged block effect

Javier Garduño - GNU Lesser General Public License v3.0
*/

#define NETHER
#define NO_SHADOWS
#define GBUFFER_DAMAGE

#include "/common/damage_vertex.glsl"