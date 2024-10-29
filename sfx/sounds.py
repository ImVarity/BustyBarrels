import pygame

class SFX:

    def __init__(self) -> None:
        self.dash_sound = pygame.mixer.Sound('sfx/grabitem.wav')
        self.collect_sound_2 = pygame.mixer.Sound('sfx/collectitem2.wav')
        self.explosion_sound = pygame.mixer.Sound('sfx/explosion.wav')
        self.menu_click = pygame.mixer.Sound('sfx/menuclick.wav')
        self.arrow_shot = pygame.mixer.Sound('sfx/arrow_shot.wav')
        self.arrow_shot.set_volume(3)

        self.arrow_shot2 = pygame.mixer.Sound('sfx/arrow_sound2.wav')
        # self.swing = pygame.mixer.Sound('sfx/swing_sound.wav')
        self.damage = pygame.mixer.Sound('sfx/damage.mp3')
        self.throw = pygame.mixer.Sound('sfx/throw.wav')
        self.stick = pygame.mixer.Sound('sfx/stick.wav')

        self.heal = pygame.mixer.Sound('sfx/heal.wav')
        self.heal.set_volume(.4)

        self.player_take_damage = pygame.mixer.Sound('sfx/player_damage.wav')
        self.player_take_damage.set_volume(.45)

        self.explosion_sound.set_volume(.2)
        

