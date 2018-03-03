import os
from g import *
import json

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)

class Creature(pygame.sprite.Sprite):
    def __init__(self, kind, name, hp, mp, sp, inventory, tex, x, y, group):
        super().__init__(group)
        self.kind, self.name = kind, name
        self.hp, self.mp, self.sp = hp, mp, sp
        self.inventory = inventory

        self.image = pygame.image.load(os.path.join('tex', tex[0]))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load(os.path.join('tex', tex[0]))
        
        self.rect = self.sprite.image.get_rect()

        self.tex= tex
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y

class Armor(pygame.sprite.Sprite):
    pass

class Weapon(pygame.sprite.Sprite):
    pass

class Arch(pygame.sprite.Sprite):
    pass

class Magic(pygame.sprite.Sprite):
    pass

class Potion(pygame.sprite.Sprite):
    pass

class Enemy(Creature):
    pass

class NPC(Creature):
    pass

class Thing(pygame.sprite.Sprite):
    pass

class Container(Thing):
    pass

class Book(pygame.sprite.Sprite):
    pass

class Hero(Creature):
    pass

class Surface_Tile(pygame.sprite.Sprite):
    pass

class House(pygame.sprite.Sprite):
    pass

class Tree(pygame.sprite.Sprite):
    pass

class Bush(pygame.sprite.Sprite):
    pass


def map(place):
    pass

def quest_list():
    pass

def state():
    pass

def attack():
    pass

def start_screen():
    global screen
    global game
    global intro
    
    screen.fill(pygame.Color('brown'))
    gui.add_element('GUI_Label_Countable', 'name', [(200, 100), (400, 200), (0, 0)], 'GAME', None, (255, 255, 255), 40, 'limit_size', 'font_adapt')
    gui.add_element('GUI_Button', 'new_game', ((200, 300), (400, 100)), new_game, 'black', 'grey', 'white', ['rect', 'New game', (255, 255, 255)])    
    gui.add_element('GUI_Button', 'load_game', ((200, 420), (400, 100)), load_game, 'black', 'grey', 'white', ['rect', 'Load game', (255, 255, 255)])
    gui.add_element('GUI_Button', 'exit_game', ((200, 540), (400, 100)), exit_game, 'black', 'grey', 'white', ['rect', 'Exit game', (255, 255, 255)])
    
    while game or intro:
        process(screen)


def pause():
    pass

def save_game():
    pass

def load_game(par):
    global game
    game = False

def exit_game(par):
    global game
    global intro
    
    game = False
    intro = False

def new_game(par):
    global game
    intro = False

def process(screen):
    global game
    global fps
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEMOTION:
            for i in gui.elements.keys():
                if gui.active_element is not None and not (gui.active_element[0][0] <= event.pos[0] <= gui.active_element[0][0]+gui.active_element[1][0] and gui.active_element[0][1] <= event.pos[1] <= gui.active_element[0][1]+gui.active_element[1][1]):
                    if hasattr(gui.elements[gui.active_element], 'state'):
                        gui.elements[gui.active_element].state = 'normal'
                    gui.active_element = None
                if i[0][0] <= event.pos[0] <= i[0][0]+i[1][0] and i[0][1] <= event.pos[1] <= i[0][1]+i[1][1]:
                    gui.active_element = i
                    if hasattr(gui.elements[i], 'state'):
                        gui.elements[i].state = 'selected'

        if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            for i in gui.elements.keys():
                if gui.active_element is not None and not (gui.active_element[0][0] <= event.pos[0] <= gui.active_element[0][0]+gui.active_element[1][0] and gui.active_element[0][1] <= event.pos[1] <= gui.active_element[0][1]+gui.active_element[1][1]):
                    if hasattr(gui.elements[gui.active_element], 'state'):
                        gui.elements[gui.active_element].state = 'normal'
                    gui.active_element = None
                if i[0][0] <= event.pos[0] <= i[0][0]+i[1][0] and i[0][1] <= event.pos[1] <= i[0][1]+i[1][1]:
                    if hasattr(gui.elements[i], 'state'):
                        gui.active_element = i
                        gui.elements[i].state = 'clicked'
                        gui.elements[i].func(event)

        if event.type == pygame.KEYDOWN:
            if gui.blocked:
                if hasattr(gui.elements[gui.active_element],'texting'):
                        gui.elements[gui.active_element].texting(event)

    gui.render(screen)
    pygame.display.flip()
    clock.tick(fps)


game = False
clock = pygame.time.Clock()
gui = GUI()      
fps = 60

intro = True
start_screen()
pygame.quit()
