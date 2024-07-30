import pygame
import sys
from vector import Vector
import random
from particles import Particle
from render import *
from array import array
import moderngl
import math
from timer import Timer

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 800
display_width, display_height = 400, 400
screen = pygame.display.set_mode((screen_width, screen_height))
display = pygame.Surface((display_width, display_height))

clock = pygame.time.Clock()



def render_stack(surf, images, pos, rotation, spread):
    for i, img in enumerate(images):
        rotated_img = pygame.transform.rotate(img, rotation)
        surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2 , pos[1] - rotated_img.get_height() // 2 - i * spread))




    
# Define colors
background_color = (0, 0, 255)  # Black

#     position      direction     size
particles = []

clock = pygame.time.Clock()

shrink_rate = 1
gravity = .5

# Main loop
def square_surf(width, height, color):
    # Create a surface with an alpha channel (transparency)
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    # Draw the rectangle on the surface
    pygame.draw.rect(surf, color, pygame.Rect(0, 0, width, height))
    return surf



tracker = 0

rotation = 0

t = 1

multiplier = 1
running = True

size = 0

end = 400
reached = False

angle = 0
# print(math.sqrt(2) / 2)

hue = 0
sat = 0
light = 0



get = [7, 7, 7]
roller = [1, 1, 1]
slot_1_timer = Timer(20)
slot_2_timer = Timer(20)
slot_3_timer = Timer(20)
roller_timers = [slot_1_timer, slot_2_timer, slot_3_timer]
pointer = 0
 
filler = 1
filler_timer = Timer(1)




while running:
    display.fill((0, 0, 0))
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pos = (mouse_x * display_width // screen_width, mouse_y * display_height // screen_height)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                roller_timers[pointer].active = False
                pointer += 1
            if event.key == pygame.K_RETURN:
                sat -= .1
            if event.key == pygame.K_i:
                size += 1


    # display.blit(a_o_d_img.convert_alpha(), [200, 200])


    slot_1_timer.start_timer(1)
    slot_2_timer.start_timer(1)
    slot_3_timer.start_timer(1)
    filler_timer.start_timer(1)

    if filler_timer.alarm:
        filler += 1

    
    if slot_1_timer.alarm:
        roller[0] += 1
        slot_1_timer.reset_timer()
    if slot_2_timer.alarm:
        roller[1] += 1
        slot_2_timer.reset_timer()
    if slot_3_timer.alarm:
        roller[2] += 1
        slot_3_timer.reset_timer()

    for i in range(len(roller)):
        if roller[i] > 9:
            roller[i] = 1
    if filler > 9:
        filler = 1
    print(roller)


    if slot_1_timer.start > 12 and slot_1_timer.active:
        render_text_centered([200, 200], f'{filler}', display, "white")
    else:
        render_text_centered([200, 200], f'{roller[0]}', display, "white")
    
    if slot_2_timer.start > 12 and slot_2_timer.active:
        render_text_centered([210, 200], f'{filler}', display, "white")
    else:
        render_text_centered([210, 200], f'{roller[1]}', display, "white")

    
    if slot_3_timer.start > 12 and slot_3_timer.active:
        render_text_centered([220, 200], f'{filler}', display, "white")
    else:
        render_text_centered([220, 200], f'{roller[2]}', display, "white")


    render_text_centered([50, 50], f'{filler}', display, "white")

    tracker += 1
    if tracker % 120 == 0:
        direction_x = -1
        direction_y = 0


        for i in range(20):
            # print(pos[0], pos[1])
            p = Particle([pos[0], pos[1]], [random.randint(-324, 324) / 1000 / 2, random.randint(-324, 0) / 1000], random.randint(10, 20), "explosion", lighting=True)
            p.shrink_rate = .01
            p.gravity = 0.00
            particles.append(p)


    for i in range(len(particles) -1, -1, -1):
        particle = particles[i]
        particle.angle = angle
        particle.all(display)

        if particle.dead():
            particles.remove(particle)

    

    rotation += 1



    # Update the display
    screen.blit(pygame.transform.scale(display, screen.get_size()), [0, 0])

    pygame.display.flip()

    
    clock.tick(60)

# Quit Pygamex



pygame.quit()
sys.exit()






# import sys
# from array import array
# from render import *
# import time
# import pygame
# import moderngl

# pygame.init()
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
# screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
# display = pygame.Surface((800, 600))
# ctx = moderngl.create_context()

# clock = pygame.time.Clock()

# img = pygame.image.load('img.png')

# quad_buffer = ctx.buffer(data=array('f', [
#     # position (x, y), uv coords (x, y)
#     -1.0, 1.0, 0.0, 0.0,  # topleft
#     1.0, 1.0, 1.0, 0.0,   # topright
#     -1.0, -1.0, 0.0, 1.0, # bottomleft
#     1.0, -1.0, 1.0, 1.0,  # bottomright
# ]))

# vert_shader = '''
# #version 330 core

# in vec2 vert;
# in vec2 texcoord;
# out vec2 uvs;

# void main() {
#     uvs = texcoord;
#     gl_Position = vec4(vert, 0.0, 1.0);
# }
# '''

# frag_shader = '''
# #version 330 core

# uniform float time;
# uniform vec2 resolution;
# uniform sampler2D tex;
# uniform vec2 mouse_pos;
# uniform float amp;

# in vec2 uvs;
# out vec4 f_color;

# void main() {
#     vec2 uv = uvs;

#     // Center of the ripple effect
#     vec2 ripple_center = mouse_pos / resolution;

#     // Calculate distance from ripple center
#     float dist = distance(uv, ripple_center);

#     // Calculate ripple effect
#     float amplitude = amp; // Increase amplitude for a larger ripple effect
#     float frequency = 25.0; // Adjust frequency for the ripple effect
#     float ripple = amplitude * cos(frequency * dist - time * 5.0) / (dist * 40.0 + 1.0);

#     // Apply ripple effect
#     uv += ripple * normalize(uv - ripple_center);


#     vec3 col = texture(tex, uv).xyz;
#     f_color = vec4(col, 1.0);
# }

# '''
# # cool
# #     vec2 sample_pos = vec2(uvs.x + sin(uvs.y * time) * 0.1, uvs.y);

# program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
# render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

# def surf_to_texture(surf):
#     tex = ctx.texture(surf.get_size(), 4)
#     tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
#     tex.swizzle = 'BGRA'
#     tex.write(surf.get_view('1'))
#     return tex

# t = 0
# amp = 0
# create = 1
# up = False
# down = False
# end = False


# appear = False
# increasing = False

# pre_time = time.perf_counter()
# last_time = time.time()
# frames = 0
# timer = 0
# while True:

#     fps = clock.get_fps()
#     keys = pygame.key.get_pressed()

#     display.fill((0, 0, 0))
#     display.blit(img, (100, 100))

#     now_time = time.perf_counter()
#     dt = now_time - pre_time
#     # print(dt)
#     timer += dt
#     frames += 1

#     if timer >= 1:
#         print("frames",frames)
#     pre_time = time.perf_counter()



#     if up:
#         amp += 0.01
#     elif down:
#         amp -= 0.01
#     elif end:
#         amp = 0
    
#     up = keys[pygame.K_u]
#     down = keys[pygame.K_y]
#     end = keys[pygame.K_e]
    
#     t += .02
#     # print(amp)

#     mouse_x, mouse_y = 400, 300
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RETURN:
#                 appear = not appear
#                 increasing = not increasing
#             if event.key == pygame.K_SPACE:
#                 create = 0

#     if appear:
#         render_stack(display, alpha_images, [400, 300], 0, 1)

#         if increasing:
#             amp += .005
#         else:
#             amp -= .004
#             if amp <= .05:
#                 amp += .002
#             if amp <= 0:
#                 amp = 0
        

#         if amp >= 0.1:
#             increasing = False


#     frame_tex = surf_to_texture(display)
#     frame_tex.use(0)
#     program['tex'] = 0
#     program['resolution'] = (800, 600)
#     program['time'] = t
#     program['mouse_pos'] = (mouse_x, mouse_y)
#     program['amp'] = amp
#     # render_object.render(mode=moderngl.TRIANGLE_STRIP)

#     # display.blit(unaffected_surface, (0, 0))

    
#     pygame.display.flip()
    
#     frame_tex.release()
    
#     clock.tick(60)
    


#     # not bad could be better


# import sys
# from array import array
# from render import *

# import pygame
# import moderngl

# pygame.init()
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
# screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
# display = pygame.Surface((800, 600))
# ctx = moderngl.create_context()

# clock = pygame.time.Clock()

# img = pygame.image.load('img.png')

# quad_buffer = ctx.buffer(data=array('f', [
#     # position (x, y), uv coords (x, y)
#     -1.0, 1.0, 0.0, 0.0,  # topleft
#     1.0, 1.0, 1.0, 0.0,   # topright
#     -1.0, -1.0, 0.0, 1.0, # bottomleft
#     1.0, -1.0, 1.0, 1.0,  # bottomright
# ]))

# vert_shader = '''
# #version 330 core

# in vec2 vert;
# in vec2 texcoord;
# out vec2 uvs;

# void main() {
#     uvs = texcoord;
#     gl_Position = vec4(vert, 0.0, 1.0);
# }
# '''

# frag_shader = '''
# #version 330 core

# uniform float time;
# uniform vec2 resolution;
# uniform sampler2D tex;
# uniform vec2 mouse_pos;
# uniform float amp;

# in vec2 uvs;
# out vec4 f_color;

# void main() {
#     vec2 uv = uvs;

#     // Center of the ripple effect
#     vec2 ripple_center = mouse_pos / resolution;

#     // Calculate distance from ripple center
#     float dist = distance(uv, ripple_center);

#     // Calculate ripple effect
#     float amplitude = amp; // Increase amplitude for a larger ripple effect
#     float frequency = 50.0; // Adjust frequency for the ripple effect
#     float ripple = amplitude * cos(frequency * dist - time * 5.0) / (dist * 40.0 + 1.0);

#     // Apply ripple effect
#     uv += ripple * normalize(uv - ripple_center);

#     vec3 col = texture(tex, uv).xyz;
#     f_color = vec4(col, 1.0);
# }

# '''
# # cool
# #     vec2 sample_pos = vec2(uvs.x + sin(uvs.y * time) * 0.1, uvs.y);

# program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
# render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

# def surf_to_texture(surf):
#     tex = ctx.texture(surf.get_size(), 4)
#     tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
#     tex.swizzle = 'BGRA'
#     tex.write(surf.get_view('1'))
#     return tex

# t = 0
# amp = 0

# up = False
# down = False
# end = False


# appear = False
# increasing = False
# while True:

#     keys = pygame.key.get_pressed()

#     display.fill((0, 0, 0))
#     display.blit(img, (100, 100))



#     if up:
#         amp += 0.01
#     elif down:
#         amp -= 0.01
#     elif end:
#         amp = 0
    
#     up = keys[pygame.K_u]
#     down = keys[pygame.K_y]
#     end = keys[pygame.K_e]
    
#     t += .02
#     print(amp)

#     mouse_x, mouse_y = 400, 300
    
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RETURN:
#                 appear = not appear
#                 increasing = not increasing

#     if appear:
#         render_stack(display, alpha_images, [400, 300], 0, 1)

#         if increasing:
#             amp += .005
#         else:
#             amp -= .004
#             if amp <= .05:
#                 amp += .002
#             if amp <= 0:
#                 amp = 0
        

#         if amp >= 0.1:
#             increasing = False


#     frame_tex = surf_to_texture(display)
#     frame_tex.use(0)
#     program['tex'] = 0
#     program['resolution'] = (800, 600)
#     program['time'] = t
#     program['mouse_pos'] = (mouse_x, mouse_y)
#     program['amp'] = amp
#     render_object.render(mode=moderngl.TRIANGLE_STRIP)

#     # display.blit(unaffected_surface, (0, 0))

    
#     pygame.display.flip()
    
#     frame_tex.release()
    
#     clock.tick(60)
    


