from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
from chat import TextBubble
import math

class NPC(Hitbox):
    def __init__(self, center, width, height, color, images, health=5):
        super().__init__(center, width, height, color)
        self.images = player_images
        self.spread = 1
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)

        self.interacting = False

        self.text = TextBubble(Vector((200, 85)), 300, 75)

        self.text.add_dialogue("Give me 100 watermelons you hippo")
        self.text.add_dialogue("Now give me 1000 arrows you monkey")
        self.text.add_dialogue("Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum")
    
    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)


    def talk(self, surface):
        self.text.display(surface)
    
    def reset_talk(self):
        self.text.reset()

    def next(self):
        self.text.next()

    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle



