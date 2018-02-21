import pygame

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))


class GUI:
    def __init__(self):
        self.elements = {}
        self.element_types = {'GUI_Label_Uncountable': GUI_Label_Uncountable, 'GUI_Label_Countable': GUI_Label_Countable}

    def add_element(self, element_type, *args):
        element = self.element_types[element_type](*args)
        self.elements[element.position] = element
        del element

    def render(self):
        for element in self.elements.values():
            element.render()


class GUI_Object:
    def __init__(self, name, position):
        self.name = name
        self.position = position  ## ((x, y), (w, h), [(x_shift, y_shift)])

    def render(self):
        pass


class GUI_Label_Countable(GUI_Object):  ##TODO
    def __init__(self, name, position, text, bg, tx_color, font_size, count_type, count_factor):
        super().__init__(name, position)
        self.text = text
        self.bg = bg
        self.tx_color = tx_color
        self.font_size = font_size
        self.count_type = count_type
        self.count_factor = count_factor
        edit = None
        self.edit = None
        if self.count_type == 'limit_width':
            text, height = self.text_adapt_lw(self.text, self.position[1][0], self.font_size)
            self.position = (self.position[0], (self.position[1][0], height), self.position[2])
        if self.count_type == 'limit_height':  ## not now
            text, width = self.text_adapt_lh(self.text, self.position[1][1], self.font_size)
            self.position[1][0] = width
        if self.count_type == 'limit_size':
            text, font_size = self.text_adapt_ls(self.text, self.position[1], self.count_factor, self.font_size)
            self.font_size = font_size
            del self.edit

        self.text = text

        if self.bg is not None:
            self.rect = pygame.Rect(self.position[0], self.position[1])

    def text_adapt_lw(self, text, width, font_size):
        t = []
        font = pygame.font.Font(None, font_size)
        j = 0
        while j < len(text):
            for i in range(len(text)):
                t_e = font.render(text[j:j+i+1], 1, self.tx_color)
                if t_e.get_width() > width:
                    t += [text[0:i]]
                    j = i
                    break
                else:
                    j += 1
                    break
        
        height = len(t) * t_e.get_height()
        return t, height
    
    def text_adapt_lh(self, text, height, font_size):  ## not now
        pass
    
    def text_adapt_ls(self, text, size, size_factor, font_size):
        if size_factor == 'font_adapt':
            font = pygame.font.Font(None, font_size)
            t = font.render(text, 1, self.tx_color)
            if t.get_width() > size[1] and self.edit != 'largen':
                self.edit = 'smallen'
                font_size -= 3
                text, font_size = self.text_adapt_ls(text, size, size_factor, font_size)
            if t.get_width() < size[1] and self.edit != 'smallen':
                self.edit = 'largen'
                font_size += 3
                text, font_size = self.text_adapt_ls(text, size, size_factor, font_size)
        else:
            x_parameter = (size[0] * size[1]) // len(text)
            font = pygame.font.Font(None, font_size)
            t_e = font.render(text, 1, self.tx_color)
            
            if t_e.get_width() * t_e.get_height() < x_parameter and self.edit != 'smallen':
                self.edit = 'largen'
                text, font_size = text_adapt_ls(text, size, size_factor, font_size+3)
                self.edit = 'ohgod' if self.edit is not None else self.edit
            if t_e.get_width() * t_e.get_height() > x_parameter and self.edit != 'largen':
                self.edit = 'smallen'
                text, font_size = text_adapt_ls(text, size, size_factor, font_size-3)
                self.edit = 'ohgod' if self.edit is not None else self.edit
            if self.edit != 'smallen' and self.edit != 'largen':
                a, b = t_e.get_height(), t_e.get_width()
                text = [[text[j] for j in range(a*b, a*b + a)] for i in range(b)]
                self.edit = None
                
        return text, font_size
        

    def render(self):
        global screen

        if self.bg is not None:
            pygame.draw.rect(screen, pygame.Color(self.bg), self.rect, 0)
        font = pygame.font.Font(None, self.font_size)
        for num, line in enumerate(self.text):
            l = font.render(line, 1, self.tx_color)
            screen.blit(l, (self.position[0][0] + self.position[2][0], self.position[0][1] + self.position[2][1] + l.get_height()*num+5))


class GUI_Label_Uncountable(GUI_Object):
    def __init__(self, name, position, text, bg, tx_color, font_size):
        super().__init__(name, position)
        self.text = text
        self.bg = bg
        self.tx_color = tx_color
        self.font_size = font_size
        if bg is not None:
            self.rect = pygame.Rect(position[0], position[1])

    def text_adapt(self, text_value, width, font, edit=False):
        if text_value:
            text = font.render(bytes(text_value, encoding='utf-8'), 1, self.tx_color)
            if text.get_width() > width:
                edit = True
                text_value = text_value[:-1]
                text_value = self.text_adapt(text_value, width, font, edit)
            else:
                return text_value
        return text_value

    def render(self):
        global screen
        if self.bg is not None:
            pygame.draw.rect(screen, pygame.Color(self.bg), self.rect, 0)
        font = pygame.font.Font(None, self.font_size)
        text = self.text_adapt(self.text, self.position[1][0]-self.position[2][0], font)
        text = text[:-2] + '...' if text != self.text else text
        text = font.render(text, 1, self.tx_color)
        screen.blit(text, (self.position[0][0] + self.position[2][0], self.position[0][1] + self.position[2][1]))


class GUI_Button(GUI_Object):  ##TODO
    pass

class GUI_Slider(GUI_Object):  ##TODO
    pass

class GUI_Changeable_Label(GUI_Object):  ##TODO
    pass

class GUI_Text_Field(GUI_Object):  ##TODO
    pass

game = True
clock = pygame.time.Clock()
gui = GUI()

gui.add_element('GUI_Label_Countable', '1', [(10, 10), (100, None), (10, 10)], 'abcdefghigklmnop', 'white', (255, 0, 0), 30, 'limit_width', None) ##limit_height, limit_size
fps = 60

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    screen.fill(pygame.Color('black'))
    gui.render()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
