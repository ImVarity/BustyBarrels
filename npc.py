from render import *
from Square import Hitbox
from vector import Vector
from health import HealthBar
from chat import TextBubble



class NPC(Hitbox):
    def __init__(self, center, width, height, color, images, health=5):
        super().__init__(center, width, height, color)
        self.images = [img.convert_alpha() for img in player_images]
        self.spread = 1
        self.to_render = Render(self.images, self.center, self.angle, self.spread)
        self.health_bar = HealthBar(health, color)

        self.interacting = False

        self.text = TextBubble(Vector(200, 85), 300, 75)

        self.text.add_dialogue("What is up gamer")
        self.text.add_dialogue("Complete some tasks for me would ya")
        self.text.add_dialogue("Use the arrow keys ^`<> to navigate Press enter to confirm")
        self.text.add_dialogue("Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum")
        
        self.text.add_quests("Deliver 10 arrows:Plus 10 arrow multiplier", "1A10M10")
        self.text.add_quests("Break 5 barrels:Plus 10 range", "2B5R10")
        self.text.add_quests("Deliver 15 arrows:Plus 15 arrow multiplier", "1A10M15")
        self.text.add_quests("Break 10 barrels:Plus 20 range", "2B10R20")
        self.text.add_quests("Deliver 20 arrows:Plus 15 arrow multiplier", "1A20M15")
        self.text.add_quests("Break 20 barrels:Plus 25 range", "2B20R25")
        self.text.add_quests("Deliver 10 watermelons:Plus 20 arrow multiplier", "1W10M20")
        self.text.add_quests("Break 40 barrels:Plus 35 range", "2B40R35")
        self.text.add_quests("Deliver 20 watermelons:Plus 30 arrow multiplier", "1W20M30")
        self.text.add_quests("Break 50 barrels:Plus 30 range", "2B50R30")
        self.text.add_quests("Deliver 30 watermelons:Plus 10 arrow multiplier", "1W30M10")
        self.text.add_quests("Break 100 barrels:Plus 100 range", "2B100R100")
        # self.text.add_quests("Eat a banana:A slap", "1W0R1")
        # self.text.add_quests("Sell your soul:A kiss", "1A0R1")
        # self.text.add_quests("Eat a banana:A slap", "2B0R2")
        # self.text.add_quests("Sell your soul:A kiss", "1A0R2")
        # self.text.add_quests("Eat a banana:A slap", "1W0R3")
        # self.text.add_quests("Sell your soul:A kiss", "2B0R3")
        self.text.add_quests("Eat a banana:A slap", "1W0R0")
        self.text.add_quests("Sell your soul:A kiss", "1A0R0")


        self.quest_encryption = {
            "1" : "Deliver",
            "2" : "Break",
            "M" : "Arrow Multiplier",
            "R" : "Range",
            "A" : "Arrows",
            "B" : "Barrels",
            "W" : "Watermelons"
        }
        self.active_quest = ""

        self.quest_status = ""

        self.quest_goal = 0
        self.to_goal = 0
        self.reward_amount = ""
        self.reward_for_quest = 0


        self.not_enough = False
        self.not_enough_start = 0
        self.not_enough_end = 120
        self.not_enough_inc = 1


    def render(self, surface):
        self.to_render.render_stack(surface)

    def draw_healthbar(self, surface):
        self.health_bar.draw(surface, self.center, self.height)

    def delete_quest(self):
        self.text.trade(self.current_quest)

    def check_funds(self, surface):
        if self.not_enough:
            render_text((200 - len("not enough") * 7 / 2, 175), "Not enough", surface)
            self.not_enough_start += self.not_enough_inc
        if self.not_enough_start == self.not_enough_end:
            self.not_enough = False
            self.not_enough_start = 0




    def talk(self, surface, input, player, display):

        self.active_quest = self.text.display_text_bubble(surface, input)
        

        transaction = False

        if len(self.active_quest) > 0: # just pressed enter to confirm a quest
            if self.active_quest[0] == "1": # means there there is a delivery quest
                transaction = self.delivery(player)
                if not transaction:
                    self.not_enough = True
                    return False
            elif self.active_quest[0] == "2": # break barrels quest
                transaction = self.bust(player)
                if not transaction: # exits the talk to bust barrels
                    return False


        if transaction:
            self.exchange(self.active_quest)
            player.quest_completed = True
            self.active_quest = ""
        
        return True
            

    def delivery(self, player):
        end_idx = 0
        labor_amount = ""
        for i in range(2, len(self.active_quest)):
            if ord(self.active_quest[i]) > 57:
                labor_amount = self.active_quest[2:i]
                end_idx = i
                break

        if len(player.inventory[self.quest_encryption[self.active_quest[1]]]) >= int(labor_amount):
            # taking away how many items you collected
            player.inventory[self.quest_encryption[self.active_quest[1]]] = player.inventory[self.quest_encryption[self.active_quest[1]]][int(labor_amount)::]

            # rewarding the player

            reward = self.active_quest[end_idx]
            reward_amount = self.active_quest[end_idx + 1::]

            player.stats[reward] += int(reward_amount)
            
            return True
        else:
            return False
        
    def bust(self, player):
        end_idx = 0
        labor_amount = ""
        
        for i in range(2, len(self.active_quest)):
            if ord(self.active_quest[i]) > 57: # just checks if the unicode number is greater than the last unicode number for a number which is 9 because unicode numbers for letters are all after numbers
                labor_amount = self.active_quest[2:i]
                end_idx = i
                break
        self.quest_goal = int(labor_amount)
        self.reward_for_quest = self.active_quest[end_idx]
        self.reward_amount = self.active_quest[end_idx + 1::]
        

        player.active_quest_code = self.active_quest
        player.active_quest = self.quest_encryption["2"] + " " + str(player.quest_barrels_busted) + "/" + labor_amount + " Barrels"
        player.inQuest = True
        self.interacting = False
        return False
        


    def show_quest_status(self, display):


        M_surface = pygame.Surface((len(self.quest_status) * 7 + 4, 10), pygame.SRCALPHA).convert_alpha()
        M_surface.fill(npc_color)
        display.blit(M_surface, (mid_x - len(self.quest_status) * 7 / 2 - 2, 70 - 2))
        render_text((mid_x - len(self.quest_status) * 7 / 2, 70), self.quest_status, display, "white")

    def update_quests(self, player):
        if player.inQuest:
            space = player.active_quest.index(' ') + 1
            slash = player.active_quest.index('/')

            self.quest_status = str(player.active_quest[0:space]) + str(player.quest_barrels_busted) + str(player.active_quest[slash::])

            if player.quest_barrels_busted >= int(self.quest_goal):
                self.exchange(player.active_quest_code)

                player.stats[self.reward_for_quest] += int(self.reward_amount)
                player.quest_completed = True
                player.active_quest = ""
                player.active_quest_code = ""
                player.inQuest = False
                player.quest_barrels_busted = 0


        # if int(player.active_quest[slash + 1:player.active_quest.index("Ba")]) == player.quest_barrels_busted:


    
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



