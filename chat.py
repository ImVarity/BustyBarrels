import pygame
from render import *

linen = (250, 240, 230)

mid_x, mid_y = 200, 200


class TextBubble:
    def __init__(self, position, width, height) -> None:

        self.location = position
        self.width = width
        self.height = height

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


    def reset(self):
        self.c_l = 0
        self.show_dialogue = ""

    def next(self):
        self.current_dialogue += 1
        self.reset()

    def key_input(self, input):
        if input["down"]:
            if self.hovering < 3:
                if self.hovering != len(self.quests) - 1:
                    self.hovering += 1
        elif input["up"]:
            if self.hovering != 0:
                self.hovering -= 1
        elif input["confirm"]:
            return self.current_quest

        return ""
        
    def display_text_bubble(self, surface, input):
        
        quest = self.key_input(input)

        if len(quest) > 0:
            return quest

        surface.blit(dialogue_box, (self.location.x - dialogue_box.get_width() / 2 - 14, self.location.y - dialogue_box.get_height() / 2 - 7))
        self.show_quests(surface)

        if self.current_dialogue >= self.dialogue_count:
            self.reset()
            self.current_dialogue = 0
            return ""
        
        # shows each letter and the continue text if reaching the last letter of the dialogue
        self.show_text(surface, self.show_dialogue, [self.location.x - self.width / 2 - 10, self.location.y - self.height / 2 + 20])
        if self.c_l == len(self.dialogue[self.current_dialogue]):
            self.show_continue_text(surface)
            return ""

        # puts every letter that we have been through in a shown dialogue variable
        self.show_dialogue += self.dialogue[self.current_dialogue][self.c_l]
        self.c_l += 1



        return ""

    def trade(self, quest):
        del self.quests[quest]
        pass

    def show_quests(self, surface):


        for i, (code, qr) in enumerate(self.quests.items()):
            quest = qr[0]
            reward = qr[1]
            selected_box = quest_box
            # box that is hovered on
            if i < 4: # only show the first 4 quests
                if self.hovering == i:
                    self.current_quest = code # change
                    # showing the quest
                    self.show_text(surface, quest, [self.location.x - (len(quest) * 7 / 2), self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40)])
                    selected_box = pygame.transform.scale(quest_box, (quest_box.get_width() + 30, quest_box.get_height()))
                    surface.blit(selected_box, (self.location.x - quest_box.get_width() / 2 - 15, self.location.y - quest_box.get_height() / 2 + 70 + (i * 40)))
                    # showing the reward
                    self.show_text(surface, reward, [self.location.x - (len(reward) * 8 / 2), self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) + 30])

                # boxes below what is hovered on
                elif i > self.hovering:
                    self.show_text(surface, quest, [self.location.x - 110, self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40) + 35])
                    surface.blit(selected_box, (self.location.x - quest_box.get_width() / 2 , self.location.y - quest_box.get_height() / 2 + 70 + (i * 40) + 35))

                # boxes above what is hovered on
                else:
                    self.show_text(surface, quest, [self.location.x - 110, self.location.y - quest_box.get_height() / 2 + 70 + 10 + (i * 40)])
                    surface.blit(selected_box, (self.location.x - quest_box.get_width() / 2 , self.location.y - quest_box.get_height() / 2 + 70 + (i * 40)))

                



    def show_text(self, surface, text, loc):

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
            surface.blit(abc[letter.capitalize()], (col + divider * 8, row))

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
            surface.blit(abc[letter.capitalize()], (col + divider * 8, row))


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
        # print(self.dialogue)
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

        print(self.quests)