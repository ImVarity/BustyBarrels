from render import *
from Square import Hitbox
from health import HealthBar

class Barrel(Hitbox):
    def __init__(self, center, width, height, color, health=5):
        super().__init__(center, width, height, color)

        self.images = [img.convert_alpha() for img in barrel_images]
        # self.images = []
        # for i in range(len(butterfly_images_stack)):
        #     self.images.append([img.convert_alpha() for img in butterfly_images_stack[i]])


        self.spread = 1
        self.to_render = Render(self.images, center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)
    
    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)



    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

