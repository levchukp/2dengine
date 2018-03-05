import json
import os
import shutil
import time
from g import *


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
    intro = 0
    
    screen.fill(pygame.Color('brown'))
    gui.add_element('GUI_Label_Countable', 'name', [(200, 100), (400, 200), (0, 0)], 'GAME', None, (255, 255, 255), 40, 'limit_size', 'font_adapt')
    gui.add_element('GUI_Button', 'new_game', ((200, 300), (400, 100)), new_game, 'black', 'grey', 'white', ['rect', 'New game', (255, 255, 255)])    
    gui.add_element('GUI_Button', 'load_game', ((200, 420), (400, 100)), load_game, 'black', 'grey', 'white', ['rect', 'Load game', (255, 255, 255)])
    gui.add_element('GUI_Button', 'exit_game', ((200, 540), (400, 100)), exit_game, 'black', 'grey', 'white', ['rect', 'Exit game', (255, 255, 255)])

    do = 0
    while intro != 'new_game':
        do = process(screen)
        if do:
            if isinstance(do, tuple):
                 self.blocked = do
            else:
                intro = do[1]
                time.sleep(0.1)
                break
    do[0](do[2])

def pause():
    pass

def save_game():
    pass

def load_game(par):
    global game
    game = False

def exit_game(par):
    global game
    game = False
    pygame.quit()

def new_game(par):
    global game
    intro = 0
    
    gui.elements.clear()
    gui.blocked = False
    gui.active_element = None
    screen.fill(pygame.Color('black'))
    gui.add_element('GUI_Label_Countable', 'Hello', [(150, 100), (500, 200), (0, 0)], 'Enter Your name...', None, (255, 255, 255), 40, 'limit_size', 'font_adapt')
    gui.add_element('GUI_Text_Field', 'nickname', ((200, 300), (400, 100)), '', 'white', (0, 0, 0), 40, 'limit_size', 'font_adapt', 'grey')
    gui.add_element('GUI_Button', 'Continue', ((200, 540), (400, 100)), play, 'grey', 'red', 'white', ['rect', 'Continue', (255, 255, 255)])

    game = True
    
    while intro != 'Continue':
        do = process(screen)
        if do:
            intro = do[1]
            if intro != 'Continue':
                res = do[0](do[2])
                if isinstance(res, tuple):
                    gui.blocked = res
            else:
                break

    
    nickname = ''.join(gui.elements[((200, 300), (400, 100))].field.text)
    os.mkdir('saves/'+nickname)
    shutil.copy('lib/save.json', 'saves/'+nickname)
    os.rename('saves/'+nickname+'/save.json', 'saves/'+nickname+'/'+nickname+'.json')
    with open('saves/'+nickname+'/'+nickname+'.json', 'r+') as f:
        change = f.read()[3:]
        change = json.loads(change)
        change['char']['name'] = nickname
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(change, f, indent=2))

           
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in gui.elements.keys():
                gui.blocked = None
                if gui.active_element is not None and not (gui.active_element[0][0] <= event.pos[0] <= gui.active_element[0][0]+gui.active_element[1][0] and gui.active_element[0][1] <= event.pos[1] <= gui.active_element[0][1]+gui.active_element[1][1]):
                    if hasattr(gui.elements[gui.active_element], 'state'):
                        gui.elements[gui.active_element].state = 'normal'
                    gui.active_element = None
                if i[0][0] <= event.pos[0] <= i[0][0]+i[1][0] and i[0][1] <= event.pos[1] <= i[0][1]+i[1][1]:
                    if hasattr(gui.elements[i], 'state'):
                        gui.active_element = i
                        gui.elements[i].state = 'clicked'
                        gui.render(screen)
                        pygame.display.flip()
                        clock.tick(fps)
                        return [gui.elements[i].func, gui.elements[i].name, event]

        if event.type == pygame.KEYDOWN:
            if gui.blocked:
                if hasattr(gui.elements[gui.blocked], 'texting'):
                    gui.elements[gui.blocked].texting(event)

    gui.render(screen)
    pygame.display.flip()
    clock.tick(fps)

def play():
    global game
    gui.elements.clear()
    gui.blocked = False
    gui.active_element = None
    screen.fill(pygame.Color('black'))

    while game:
        process(screen)

game = False
clock = pygame.time.Clock()
gui = GUI()      
fps = 60

start_screen()
play()
pygame.quit()
