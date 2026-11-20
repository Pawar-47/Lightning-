#version 330 compatibility
#extension GL_ARB_shader_texture_lod : enable
/* MakeUp - composite.fsh
Render: Bloom and volumetric light

Javier Garduño - GNU Lesser General Public License v3.0
*/

#define COMPOSITE_SHADER

#include "/common/composite_fragment.glsl"