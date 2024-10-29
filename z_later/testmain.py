import pygame
import moderngl
import sys
import math
from array import array

# Initialize Pygame and set up OpenGL context
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
ctx = moderngl.create_context()

# Shader code
vert_shader = '''
#version 330 core


in vec2 vert;
in vec2 texcoord;

out vec2 uvs;

void main() {
    uvs = texcoord;
    uvs.y = 1.0 - uvs.y;  // Invert y-coordinate

    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core
precision mediump float;

in vec2 uvs;
out vec4 colour;

uniform sampler2D tex;
uniform vec2 resolution;
uniform float time;
uniform vec2 mouse_pos;

const float maxRadius = 0.5;

// Distance function for the effect
float getOffsetStrength(float t, vec2 dir) {
    float d = length(dir) - t * maxRadius;
    d *= 1. - smoothstep(0., 0.05, abs(d));
    d *= smoothstep(0., 0.05, t);
    d *= 1. - smoothstep(0.5, 1., t);
    return d;
}

void main() {
    vec2 centre = mouse_pos / resolution;
    vec2 dir = centre - uvs;
    float rD = getOffsetStrength(time, dir);

    // Apply chromatic aberration
    dir = normalize(dir);
    vec3 color;
    color.r = texture(tex, uvs + dir * rD).r;
    color.g = texture(tex, uvs + dir * rD * 0.9).g;
    color.b = texture(tex, uvs + dir * rD * 0.8).b;
    
    colour = vec4(color, 1.0);
}
'''

# Compile the shaders
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)

# Create a quad buffer for drawing a full-screen rectangle
quad_buffer = ctx.buffer(data=array('f', [
    -1.0,  1.0, 0.0, 1.0,  # Top-left
     1.0,  1.0, 1.0, 1.0,  # Top-right
    -1.0, -1.0, 0.0, 0.0,  # Bottom-left
     1.0, -1.0, 1.0, 0.0   # Bottom-right
]))
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

# Helper function to convert a Pygame surface to a texture
def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    return tex

# Load image and create initial texture
image = pygame.image.load('babygnu.png')
display = pygame.Surface((800, 600))
display.blit(image, (0, 0))

# Main loop
clock = pygame.time.Clock()
t = 0.0
mouse_x, mouse_y = pygame.mouse.get_pos()
while True:
    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            center_x = mouse_x / display.get_width()
            center_y = 1.0 - (mouse_y / display.get_height())  # Invert y for OpenGL coordinates
            t = 0  # Reset the time to trigger the shockwave

    # Update time variable
    t += 0.02

    # Get mouse position for shockwave center
    

    # Create texture from Pygame surface
    frame_tex = surf_to_texture(display)
    frame_tex.use()

    # Set uniforms for the shader
    program['tex'] = 0
    program['resolution'] = (800, 600)
    program['time'] = t
    program['mouse_pos'] = (mouse_x, mouse_y)

    # Render
    ctx.clear(0.1, 0.1, 0.1)
    render_object.render(moderngl.TRIANGLE_STRIP)
    
    pygame.display.flip()
    frame_tex.release()
    clock.tick(60)