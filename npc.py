from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
from chat import TextBubble
import math

class NPC(Hitbox):
    def __init__(self, center, width, height, color, images, health=5):
        super().__init__(center, width, height, color)
        self.images = images
        self.spread = 1.2
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)

        self.interacting = False

        self.text = TextBubble(Vector((200, 60)), 300, 75)

        self.text.add_dialogue("Give me a hundred watermelons you hippo")
        self.text.add_dialogue("Now give me one thousand arrows you monkey")
    
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

