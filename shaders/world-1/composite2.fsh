#version 330 compatibility
#extension GL_ARB_shader_texture_lod : enable
/* MakeUp - composite1.fsh
Render: Antialiasing and motion blur

Javier Garduño - GNU Lesser General Public License v3.0
*/

#define NETHER
#define COMPOSITE2_SHADER
#define NO_SHADOWS

#include "/common/composite2_fragment.glsl"
