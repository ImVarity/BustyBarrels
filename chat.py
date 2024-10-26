import pygame
from render import *

pygame.init()

menu_click = pygame.mixer.Sound('sfx/menuclick.wav')


linen = (250, 240, 230)

mid_x, mid_y = 200, 200


class TextBubble:
    def __init__(self, position, width, height) -> None:

        self.location = position
        self.width = width
        self.height = height

        self.sounds = None

        self.rect = pygame.Rect(position.x - width / 2, position.y - height / 2, width, height)

        self.dialogue = []

        self.dialogue_count = 0
        self.current_dialogue = 0
        self.continue_text = "press c to continue"
        self.c_l = 0
        self.show_dialogue = ""


        self.quests = {}

        self.quests_count = 0


        self.hovering = 0
        

        self.current_quest = ""


        self.inputs = {'up': False, 'down': False, 'confirm': False}


    def reset(self):
        self.c_l = 0
        self.show_dialogue = ""

    def next(self):
        self.current_dialogue += 1
        self.reset()

    def key_input(self, input):
        # print(input)
        if self.current_dialogue >= 2 and len(self.quests) > 0:
            if input["down"]:
                if self.hovering < 3:
                    if self.hovering != len(self.quests) - 1:
                        menu_click.play()
                        self.hovering += 1
            elif input["up"]:
                if self.hovering != 0:
                    menu_click.play()
                    self.hovering -= 1
            elif input["confirm"]:
                menu_click.play()
                return self.current_quest

        return ""
        
    def display_text_bubble(self, surface, input, person="Mikhail"):
        quest = self.key_input(input)
        if len(quest) > 0:
            return quest
        
        if person == "Mikhail":
            surface.blit(dialogue_box.convert_alpha(), (self.location.x - dialogue_box.get_width() / 2 - 14, self.location.y - dialogue_box.get_height() / 2 - 7))
        elif person == "Jack":
            surface.blit(dialogue_box.convert_alpha(), (self.location.x - dialogue_box.get_width() / 2 - 14, self.location.y - dialogue_box.get_height() / 2 - 7))
        

        if self.current_dialogue >= self.dialogue_count:
            self.reset()
            self.current_dialogue = 0
            return ""
        # shows each letter and the continue text if reaching the last letter of the dialogue
        self.show_text(surface, self.show_dialogue, [self.location.x - self.width / 2 - 10, self.location.y - self.height / 2 + 20], "black")
        if self.c_l == len(self.dialogue[self.current_dialogue]):
            self.show_continue_text(surface)
            if self.current_dialogue > 1:
                self.show_quests(surface)
            return ""

        # puts every letter that we have been through in a shown dialogue variable
        self.show_dialogue += self.dialogue[self.current_dialogue][self.c_l]
        self.c_l += 1


        return ""

    def trade(self, quest):
        try:
            # if we are hovering over the last item and there are no more quests after, we hovering over the top after deleting
            x = list(self.quests).index(quest)
            del self.quests[quest]
            if len(self.quests) == x:
                self.hovering -= 1
            # print(x)
        except:
            pass

    def show_quests(self, surface):
        # dont show hovering if its -1
        if self.hovering == -1:
            pass

        for i, (code, qr) in enumerate(self.quests.items()):
            quest = qr[0]
            reward = qr[1]
            selected_box = quest_box

            npc_color = (47,79,79, 100)
            quest_surface = pygame.Surface((len(quest) * 8 + 4, 10), pygame.SRCALPHA).convert_alpha()
            reward_surface = pygame.Surface((len(reward) * 8 + 4, 10), pygame.SRCALPHA).convert_alpha()
            quest_surface.fill(npc_color)
            reward_surface.fill(npc_color)

            # box that is hovered on
            if i < 4: # only show the first 4 quests
                if self.hovering == i:
                    self.current_quest = code # change
                    # showing the quest
                    selected_box = pygame.transform.scale(quest_box, (quest_box.get_width() + 30, quest_box.get_height()))
                    surface.blit(selected_box.convert_alpha(), (self.location.x - quest_box.get_width() / 2 - 15, self.location.y - quest_box.get_height() / 2 + 70 + (i * 40)))
                    surface.blit(quest_surface, (self.location.x - (len(quest) * 8 / 2), self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) - 2))
                    self.show_text(surface, quest, [self.location.x - (len(quest) * 8 / 2), self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40)], "white")
                    # showing the reward
                    surface.blit(reward_surface, [self.location.x - (len(reward) * 8 / 2), self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) + 25 - 2])
                    self.show_text(surface, reward, [self.location.x - (len(reward) * 8 / 2), self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) + 25], "white")
                    self.show_text(surface, "Enter to confirm", [self.location.x - (len("Enter to confirm") * 8 / 2), self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) + 45], "black")
                    if code[1] == 'A':
                        surface.blit(arrow_images[3].convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 80 + (i * 40) - 5])
                    elif code[1] == 'W':
                        surface.blit(watermelon_img.convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 80 + (i * 40) - 2])
                    elif code[1] == 'B':
                        surface.blit(barrel_img.convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 80 + (i * 40) - 6])

                # boxes below what is hovered on
                elif i > self.hovering:
                    surface.blit(selected_box.convert_alpha(), (self.location.x - quest_box.get_width() / 2 , self.location.y - quest_box.get_height() / 2 + 70 + (i * 40) + 35))
                    self.show_text(surface, quest, [self.location.x - 110, self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) + 35], "black")
                    if code[1] == 'A':
                        surface.blit(arrow_images[3].convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 80 + (i * 40) + 30])
                    elif code[1] == 'W':
                        surface.blit(watermelon_img.convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 80 + (i * 40) + 33])
                    elif code[1] == 'B':
                        surface.blit(barrel_img.convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 80 + (i * 40) + 29])


                # boxes above what is hovered on
                else:
                    surface.blit(selected_box.convert_alpha(), (self.location.x - quest_box.get_width() / 2 , self.location.y - quest_box.get_height() / 2 + 70 + (i * 40)))
                    self.show_text(surface, quest, [self.location.x - 105, self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40)], "black")
                    if code[1] == 'A':
                        surface.blit(arrow_images[3].convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) - 5])
                    elif code[1] == 'W':
                        surface.blit(watermelon_img.convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) - 2])
                    elif code[1] == 'B':
                        surface.blit(barrel_img.convert_alpha(), [self.location.x + 105, self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) - 6])
                


            
    def show_text(self, surface, text, loc, color):

        col = loc[0]
        row = loc[1]

        divider = 0

        for letter in text:
            divider += 1
            if letter == " ":
                continue
            if letter == "+":
                row += 8
                divider = 0
                continue
            surface.blit(abc[letter.capitalize()][color].convert_alpha(), (col + divider * 8, row))

    def show_continue_text(self, surface):
        col = self.location.x - self.width / 2 + 120 + 15
        row = self.location.y - self.height / 2 + 10 + 8 * 6 + 24

        divider = 0

        for letter in self.continue_text:
            divider += 1
            if letter == " ":
                continue
            if letter == "+":
                row += 8
                divider = 0
                continue
            surface.blit(abc[letter.capitalize()]["black"].convert_alpha(), (col + divider * 8, row))


    def add_dialogue(self, text):
        enter = ""

        tokened = text.split(" ")
        counter = 0

        for word in tokened:
            if len(word) + 1 + counter < 40:
                enter += word + " "
                counter += len(word) + 1
            else:
                enter += "+"
                counter = len(word) + 1
                enter += word + " "

        self.dialogue.append(enter)
        self.dialogue_count += 1


    def add_quests(self, qr, code):

        first_tokened = qr.split(":")
        quest = first_tokened[0]
        reward = first_tokened[1]
        
        both = [quest, reward]

        self.quests[code] = []

        for text in both:
            enter = ""
            tokened = text.split(" ")
            counter = 0

            for word in tokened:
                if len(word) + 1 + counter < 40:
                    enter += word + " "
                    counter += len(word) + 1
                else:
                    enter += "+"
                    counter = len(word) + 1
                    enter += word + " "

            self.quests[code].append(enter)
        self.quests_count += 1



    def give_inputs(self, inputs):
        self.inputs = inputs
