from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
from chat import TextBubble

class NPC(Hitbox):
    def __init__(self, center, width, height, color, images, health=5):
        super().__init__(center, width, height, color)
        self.images = player_images
        self.spread = 1
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)

        self.interacting = False

        self.text = TextBubble(Vector((200, 85)), 300, 75)

        self.text.add_dialogue("What is up gamer")
        self.text.add_dialogue("Complete some tasks for me would ya")
        # self.text.add_dialogue("Enter shop")
        self.text.add_dialogue("Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum")
        
        self.text.add_quests("Deliver 10 arrows:Plus 10 arrow multiplier", "1A10M10")
        self.text.add_quests("Break 5 barrels:Plus 10 range", "2B5R10")
        self.text.add_quests("Deliver 30 arrows:Plus 30 arrow multiplier", "1A30M30")
        self.text.add_quests("Break 10 barrels:Plus 20 range", "2B10R20")
        self.text.add_quests("Deliver 10 watermelons:Plus 30 arrow multiplier", "1W10M30")
        self.text.add_quests("Break 50 barrels:Plus 70 range", "2B50R70")
        self.text.add_quests("Deliver 30 watermelons:Plus 30 arrow multiplier", "1W30M30")
        self.text.add_quests("Break 100 barrels:Plus 100 range", "2B100R100")





        self.text.add_quests("Eat a banana:A slap", "1W20R0")
        self.text.add_quests("Sell your soul:A kiss", "1A20R0")


        self.active_quest = ""


    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)


    def talk(self, surface, input):
        self.active_quest = self.text.display_text_bubble(surface, input)
        # if len(active_quest) > 0:
        #     self.active_quest = active_quest

    
    def reset_talk(self):
        self.text.reset()

    def exchange(self, quest):
        self.text.trade(quest)

    def next(self):
        self.text.next()

    def update(self, rotation_input, direction):
        self.handle_rotation(rotation_input)
        self.move(direction * -1)
        self.to_render.loc = [self.center.x, self.center.y]
        self.to_render.angle = self.angle



