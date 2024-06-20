import pygame
import time
from render import *

linen = (250, 240, 230)



class TextBubble:
    def __init__(self, position, width, height) -> None:

        self.location = position
        self.width = width
        self.height = height

        self.rect = pygame.Rect(position.x - width / 2, position.y - height / 2, width, height)

        self.dialogue = []

        self.dialogue_count = 0

        self.current_dialogue = 0

        self.speed = 150


        self.show_dialogue = ""




        self.c_l = 0

        self.continue_text = "press c to continue"


    def reset(self):
        self.c_l = 0
        self.show_dialogue = ""

    def next(self):
        self.current_dialogue += 1
        self.reset()

        
    def display(self, surface):

        # pygame.draw.rect(surface, linen, self.rect)
        surface.blit(dialogue_box, (self.location.x - dialogue_box.get_width() / 2 - 14, self.location.y - dialogue_box.get_height() / 2 - 7))
        self.show_quests(surface)
        if self.current_dialogue >= self.dialogue_count:
            self.reset()
            self.current_dialogue = 0
            return
            

        print(self.dialogue[self.current_dialogue])

        self.show(surface, self.show_dialogue)
        if self.c_l == len(self.dialogue[self.current_dialogue]):
            self.show_continue_text(surface)
            return

        self.show_dialogue += self.dialogue[self.current_dialogue][self.c_l]
        self.c_l += 1

    def show_quests(self, surface):
        surface.blit(quest_box, (0, 0))


    def show(self, surface, text):
        col = self.location.x - self.width / 2
        row = self.location.y - self.height / 2 + 10

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
            if len(word) + 1 + counter < 36:
                enter += word + " "
                counter += len(word) + 1
            else:
                enter += "+"
                counter = len(word) + 1
                enter += word + " "

        self.dialogue.append(enter)
        print(self.dialogue)
        self.dialogue_count += 1


