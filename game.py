import os
from g import *

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('grey'))

class Creature(pygame.sprite.Sprite):
    def __init__(self, kind, name, hp, mp, sp, inventory, tex, x, y, group):
        super().__init__(group)
        self.kind, self.name = kind, name
        self.hp, self.mp, self.sp = hp, mp, sp
        self.inventory = inventory

        self.image = pygame.image.load(os.path.join('', tex[0]))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load(os.path.join('', tex[0]))
        
        self.rect = self.sprite.image.get_rect()

        self.tex= tex
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y

class Armor:
    pass

class Weapon:
    pass

class Arch:
    pass

class Magic:
    pass

class Potion:
    pass

class Enemy(Creature):
    pass

class NPC(Creature):
    pass

class House:
    pass

class Thing:
    pass

class Container(Thing):
    pass

class Book():
    pass



game = True
clock = pygame.time.Clock()
gui = GUI()
               
fps = 60
a = []
ss = pygame.sprite.Group()
sack = Creature(1, 2, 3, 4, 5, [], ['sack.png'], 0, 0, ss)
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEMOTION:
            for i in gui.elements.keys():
                if gui.active_element is not None and not (gui.active_element[0][0] <= event.pos[0] <= gui.active_element[0][0]+gui.active_element[1][0] and gui.active_element[0][1] <= event.pos[1] <= gui.active_element[0][1]+gui.active_element[1][1]):
                    if hasattr(gui.elements[gui.active_element], 'state'):
                        gui.elements[gui.active_element].state = 'normal'
                    gui.active_element = None if not gui.blocked else gui.active_element
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
                    gui.blocked = False
                if i[0][0] <= event.pos[0] <= i[0][0]+i[1][0] and i[0][1] <= event.pos[1] <= i[0][1]+i[1][1]:
                    if hasattr(gui.elements[i], 'state'):
                        gui.blocked = True
                        gui.active_element = i
                        gui.elements[i].state = 'clicked'
                        gui.elements[i].func(event)

        if event.type == pygame.KEYDOWN:
            if gui.blocked:
                if hasattr(gui.elements[gui.active_element],'texting'):
                     gui.elements[gui.active_element].texting(event)
            
    screen.fill(pygame.Color('black'))
    gui.render()
    ss.draw(screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
