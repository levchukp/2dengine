import json
import os
import shutil
import time
from g import *


pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)


class Game:
    def __init__(self):
        self.sprites = {}
        self.char = pygame.sprite.Group()
        self.tiles = {'000': 'wall.png', '10': 'grass.png',
                      None: 'none.png', '010': 'wall.png',
                      '50': 'sack.png', '600': 'sack.png',
                      '700': 'sack.png', '50': 'sack.png',
                      '90': 'sack.png', '3': 'sack.png',
                      '4': 'sack.png', '20': 'sack.png',
                      '020': 'wall.png', 'A0': 'wall.png'}
        self.curr_tiles = pygame.sprite.Group()
        self.current_world = [[Surface_Tile(j*80, i*80, self.curr_tiles) for j in range(10)] for i in range(10)]
        self.location = None
        self.x, self.y = 0, 0
        self.hero = None

    def add_sprite(self, elem, *args):
        self.sprites[elem.name] = elem
        if elem.kind == 'main_hero':
            self.hero = elem.name
            self.x, self.y = self.sprites[self.hero].x, self.sprites[self.hero].y
            self.location = 'lib/'+json.loads(self.sprites[self.hero].file)['char']['place'][2]+'.txt'

    def _square(self, loc, cx, cy):
        square = []
        cent_x, cent_y = len(loc) // 2 + 1, len(loc[0]) // 2 + 1
        for i in range(len(loc)):
            loc[i] = loc[i].split(';')[:-1]
        cx, cy = cent_x + cx, cent_y + cy
            
        if len(loc) < 10:
            square = loc.copy()
        else:
            start = cy-5 if cy-5 <= 0 else 0
            square += loc[start:cy+5]
             
        for i in range(len(square)):
            start = cx-5 if cx-5 <= 0 else 0
            square[i] = square[i][start:cx+5]
        for i in range(10 - len(square)):
            square.append([None for j in range(10)]) 
        for i in range(len(square)):
            if len(square[i]) < 10:
                for j in range(10 - len(square[i])):
                    square[i].append(None)
 
        return square
    
    def load(self):
        location = open(self.location, 'r').readlines()
        current_world = self._square(location, self.x, self.y)
        print(current_world)
        cent_x, cent_y = len(location) // 2 + 1, len(location[0]) // 2 + 1
        cx, cy = cent_x + self.x, cent_y + self.y
                
        for i in range(10):
            for j in range(10):
                self.current_world[i][j].reimage(current_world[i][j], self.tiles)
        
    
##    def update(self):
##        curr_x, curr_y = self.sprites[self.hero].x, self.sprites[self.hero].y
##
##        if curr_x != self.x:
##            if curr_x > self.x:
##                diff = curr_x - self.x
##                for i in range(10):
##                    self.current_world[i] = self.current_world[i][diff:]
##                    for j in range(diff):
##                        self.current_world[i].insert(-1, None)
##            else:
##                diff = self.x - curr_x
##                for i in range(10):
##                    self.current_world[i] = self.current_world[i][:10-diff]
##                    for j in range(diff):
##                        self.current_world[i].insert(0, None)
##            self.x = curr_x
##        if self.sprites[self.hero].y != self.y:
##            if curr_y > self.y:
##                diff = curr_y - self.y
##                for i in range(10):
##                    self.current_world = self.current_world[:10-diff]
##                    for j in range(diff):
##                        self.current_world.insert(-1, [None for j in range(10)])
##            else:
##                diff = self.y - curr_y
##                for i in range(10):
##                    self.current_world = self.current_world[diff:]
##                    for j in range(diff):
##                        self.current_world.insert(0, [None for j in range(10)])
##            self.y = curr_y
##        
##        self.load(current)


    def update(self):
        self.x, self.y = self.sprites[self.hero].x, self.sprites[self.hero].y
        self.load()


class Creature(pygame.sprite.Sprite): ##TODO
    def __init__(self, kind, name, hp, mp, sp, prot, damage, inventory, tex, x, y, group):
        super().__init__(group)
        self.kind, self.name = kind, name
        self.hp, self.mp, self.sp = hp, mp, sp
        self.prot, self.damage = prot, damage
        self.inventory = inventory
        self.x, self.y = x, y
        self.alive = True
        
        self.tex = tex
        self.image = pygame.image.load(os.path.join('tex', tex[0]))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        
class Hero(Creature): ##TODO
    def __init__(self, kind, name, hp, mp, sp, prot, damage, inventory, tex, x, y, group, file):
        super().__init__(kind, name, hp, mp, sp, prot, damage, inventory, tex, x, y, group)
        self.rect.x, self.rect.y = 320, 320
        self.file = '\n'.join(file.readlines())

    def move(self, event):
        if event.key == pygame.K_w:
            self.y += 1
        elif event.key == pygame.K_a:
            self.x -= 1
        elif event.key == pygame.K_s:
            self.y -= 1
        elif event.key == pygame.K_d:
            self.x += 1


class NPC(Creature):
    def __init__(self, kind, name, hp, mp, sp, prot, damage, inventory, tex, x, y, group):
        super().__init__(kind, name, hp, mp, sp, prot, damage, inventory, tex, x, y, group)

class Enemy(Creature):
    def __init__(self, kind, name, hp, mp, sp, prot, damage, inventory, tex, x, y, group):
        super().__init__(kind, name, hp, mp, sp, prot, damage, inventory, tex, x, y, group)


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

class Book(pygame.sprite.Sprite):
    pass
        

class Surface_Tile(pygame.sprite.Sprite): ##TODO
    def __init__(self, x, y, group):
        super().__init__(group)
        global playing
        self.image = pygame.image.load(os.path.join('tex', 'none.png'))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.through = True

    def reimage(self, kind, tiles):
        self.image = pygame.image.load(os.path.join('tex', tiles[kind]))
        self.through = False if kind[0] = '0' else False

class House(pygame.sprite.Sprite):
    pass

class Tree(pygame.sprite.Sprite):
    pass

class Bush(pygame.sprite.Sprite):
    pass

class Thing(pygame.sprite.Sprite):
    pass

class Container(Thing):
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


def pause(): ##TODO
    pass

def save_game(): ##TODO
    pass

def load_game(par): ##TODO
    pass

def exit_game(par):
    global game
    game = False
    pygame.quit()

def new_game(par): ##TODO
    global game
    global hero
    
    intro = 0
    
    gui.elements.clear()
    gui.blocked = False
    gui.active_element = None
    screen.fill(pygame.Color('black'))
    gui.add_element('GUI_Label_Countable', 'Hello', [(150, 100), (500, 200), (0, 0)], 'Enter Your name...', None, (255, 255, 255), 40, 'limit_size', 'font_adapt')
    gui.add_element('GUI_Text_Field', 'nickname', ((200, 300), (400, 100)), '', 'white', (0, 0, 0), 40, 'limit_size', 'font_adapt', 'grey')
    gui.add_element('GUI_Button', 'Continue', ((200, 540), (400, 100)), play, 'grey', 'red', 'white', ['rect', 'Continue', (255, 255, 255)])

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
        
    game = True
    playing.add_sprite(Hero('main_hero', nickname, 100, 100, 100, 1, 1, ['cloth', 'boots'], ['wall.png'], 0, 0, playing.char, open('saves/'+nickname+'/'+nickname+'.json', 'r+')))

           
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
                        return [gui.elements[i].func, gui.elements[i].name, event]  ## fix

        if event.type == pygame.KEYDOWN:
            if isinstance(gui.blocked, tuple):
                if hasattr(gui.elements[gui.blocked], 'texting'):
                    gui.elements[gui.blocked].texting(event)
            else:
                if game:
                     playing.sprites[playing.hero].move(event)
                
            

    gui.render(screen)
    if game:
        playing.update()
        playing.curr_tiles.draw(screen)
        playing.char.draw(screen)
        
    pygame.display.flip()
    clock.tick(fps)


def play():
    global game
    global hero
    
    gui.elements.clear()
    gui.blocked = False
    gui.active_element = None
    screen.fill(pygame.Color('black'))

    while game:
        process(screen)


game = False
clock = pygame.time.Clock()
playing = Game()
gui = GUI()      
fps = 60

pygame.mouse.set_cursor(*pygame.cursors.diamond)
start_screen()
if game:
    play()
pygame.quit()
