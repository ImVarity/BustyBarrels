from render import *
from Square import Hitbox
from health import HealthBar
from chat import TextBubble
from vector import Vector

class Gambler(Hitbox):
    def __init__(self, center, width, height, color, images, health=5):
        super().__init__(center, width, height, color)

        self.images = [img.convert_alpha() for img in player_images]
        self.spread = 1
        self.to_render = Render(self.images, center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)

        self.interacting = False

        self.trades = {}

        self.chat = TextBubble(Vector(200, 85), 300, 75)
        self.chat.add_dialogue("Oh boy OH BOY")
        self.chat.add_dialogue("Triple money HERE")
        self.chat.add_dialogue("Use the arrow keys ^`<> to navigate Press enter to confirm")


    


    def draw_difficulty(self, display):
        pass

    
    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)


    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle

    def next(self): # next dialogue
        self.chat.next()

    def reset_talk(self): # resets the current dialogue so letters appear again
        self.chat.reset()

    def talk(self, player, inputs, display):
        self.chat.give_inputs(inputs)
        self.chat.display_text_bubble(display, inputs)
        # self.chat.display_difficulty(display)
        # self.active_quest = self.chat.display_text_bubble(display, inputs)

        # transaction = False

        # if transaction:
        #     self.exchange(self.active_quest)
        #     self.active_quest = ""
        
        return True

    def exchange(self, quest):
        self.chat.trade(quest)

    def draw_hud(self, display):
        pass



