#version 330 compatibility
#extension GL_ARB_shader_texture_lod : enable
/* MakeUp - gbuffers_terrain.fsh
Render: Almost everything

Javier Garduño - GNU Lesser General Public License v3.0
*/

#define THE_END
#define GBUFFER_TERRAIN
#define FOLIAGE_V

#include "/common/solid_blocks_fragment.glsl"