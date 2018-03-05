import pygame


class GUI:
    def __init__(self):
        self.elements = {}
        self.element_types = {'GUI_Label_Uncountable': GUI_Label_Uncountable, 'GUI_Label_Countable': GUI_Label_Countable, 'GUI_Button': GUI_Button, 'GUI_Changeable_Label': GUI_Changeable_Label, 'GUI_Text_Field': GUI_Text_Field}
        self.blocked = False
        self.active_element = None

    def add_element(self, element_type, *args):
        element = self.element_types[element_type](*args)
        self.elements[element.position] = element
        del element

    def render(self, screen):
        for element in self.elements.values():
            element.render(screen)


class GUI_Object:
    def __init__(self, name, position):
        self.name = name
        self.position = position  ## ((x, y), (w, h), [(x_shift, y_shift)])

    def render(self):
        pass


class GUI_Label_Countable(GUI_Object): ## []
    def __init__(self, name, position, text, bg, tx_color, font_size, count_type, count_factor):
        super().__init__(name, position)
        self.text = text
        self.bg = bg
        self.tx_color = tx_color
        self.font_size = font_size
        self.count_type = count_type
        self.count_factor = count_factor
        self.edit = ''

        if self.count_type == 'limit_width':
            text, height = self.text_adapt_lw(self.text, self.position[1][0]-self.position[2][0], self.font_size)
            self.position = (self.position[0], (self.position[1][0], height+self.position[2][1]), self.position[2])
        if self.count_type == 'limit_height':  ## not now
            text, width = self.text_adapt_lh(self.text, self.position[1][1], self.font_size)
            self.position[1][0] = width
        if self.count_type == 'limit_size':
            self.position = (self.position[0], (self.position[1][0], self.position[1][1]), self.position[2])
            text, font_size = self.text_adapt_ls(self.text, [self.position[1][0], self.position[1][1]], self.count_factor, self.font_size)
            text, p = self.text_adapt_lw(''.join(text), self.position[1][0]-self.position[2][0], (font_size * len(text)) // (len(text) + 1))
            self.font_size = (font_size * len(text)) // (len(text) + 1)
            #del self.edit

        self.text = text
        if self.bg is not None:
            self.rect = pygame.Rect(self.position[0], self.position[1])


    def text_adapt_lw(self, text, width, font_size):
        t = []
        font = pygame.font.Font(None, font_size)
        j = 0
        
        if font.render(text, 1, self.tx_color).get_width() <= width:
            t.append(text)
            return text, font.render(text, 1, self.tx_color).get_height()
        
        while j < len(text):
            for i in range(len(text)):
                t_e = font.render(text[j:j+i+1], 1, self.tx_color)
                if t_e.get_width() > width or j+i > len(text):
                    t.append(text[j:j+i])
                    j = j+i
                    break
                
        height = len(t) * t_e.get_height()
        return t, height
    
    def text_adapt_lh(self, text, height, font_size):  ## not now+
        pass
    
    def text_adapt_ls(self, text, size, size_factor, font_size):
        if size_factor == 'font_adapt':
            font = pygame.font.Font(None, font_size)
            t = font.render(text, 1, self.tx_color)
            if t.get_width() > size[0] and self.edit != 'largen':
                self.edit = 'smallen'
                font_size -= 2
                text, font_size = self.text_adapt_ls(text, size, size_factor, font_size)
            if t.get_width() < size[0] and self.edit != 'smallen':
                self.edit = 'largen'
                font_size += 2
                text, font_size = self.text_adapt_ls(text, size, size_factor, font_size)
        else:
            x_parameter = (size[0] * size[1]) // len(text)
            font = pygame.font.Font(None, font_size)
            t_e = font.render('a', 1, self.tx_color)
            b, a = t_e.get_height(), t_e.get_width()
            if b * a < x_parameter and self.edit != 'smallen':
                self.edit = 'largen'
                text, font_size = self.text_adapt_ls(text, size, size_factor, font_size+1)
                self.edit = 'ohgod' if self.edit != '' else self.edit
            if b * a > x_parameter and self.edit != 'largen':
                self.edit = 'smallen'
                text, font_size = self.text_adapt_ls(text, size, size_factor, font_size-1)
                self.edit = 'ohgod' if self.edit != '' else self.edit
            if self.edit not in ['smallen', 'largen' , '']:
                bad_code = text
                text = [''.join([text[j] for j in range((size[0] // a) * i, (size[0] // a) * (i+1))]) for i in range(size[1] // b)]
                if ''.join(text) != bad_code:
                    text.append(bad_code[(size[0] // a) * (size[1] // b):])
                self.edit = ''
                
        return text, font_size
        

    def render(self, screen):
        if not isinstance(self.text, list):
            if self.count_type == 'limit_width':
                text, height = self.text_adapt_lw(self.text, self.position[1][0]-self.position[2][0], self.font_size)
                self.position = (self.position[0], (self.position[1][0], height+self.position[2][1]), self.position[2])
            if self.count_type == 'limit_height':  ## not now
                text, width = self.text_adapt_lh(self.text, self.position[1][1], self.font_size)
                self.position[1][0] = width
            if self.count_type == 'limit_size':
                self.position = (self.position[0], (self.position[1][0], self.position[1][1]), self.position[2])
                text, font_size = self.text_adapt_ls(self.text, [self.position[1][0], self.position[1][1]], self.count_factor, self.font_size)
                text, p = self.text_adapt_lw(''.join(text), self.position[1][0]-self.position[2][0], (font_size * len(text)) // (len(text) + 1))
                self.font_size = (font_size * len(text)) // (len(text) + 1)
                del self.edit

            self.text = text
        if self.bg is not None:
            pygame.draw.rect(screen, pygame.Color(self.bg), self.rect, 0)
            self.rect = pygame.Rect(self.position[0], self.position[1])
            
        font = pygame.font.Font(None, self.font_size)
        self.text = self.text if isinstance(self.text, list) else [self.text]
        for num, line in enumerate(self.text):
            l = font.render(line, 1, self.tx_color)
            screen.blit(l, (self.position[0][0] + self.position[2][0], self.position[0][1] + self.position[2][1] + l.get_height()*num))


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


class GUI_Button(GUI_Object):
    def __init__(self, name, position, func, normal, selected, clicked, button_pars):
        super().__init__(name, position)
        self.func = func
        self.normal, self.selected, self.clicked = normal, selected, clicked
        self.button_pars = button_pars
        if button_pars[0] == 'rect':
            self.rect = pygame.Rect(position[0], position[1])  
        self.state = 'normal'
        self.text = GUI_Label_Countable(self.button_pars[1], [self.position[0], self.position[1], (5, 5)], self.button_pars[1], None, self.button_pars[2], 40, 'limit_size', 'font_adapt')

    def click(self, event):
        self.func(1)
    
    def render(self, screen):
        if self.state == 'normal':
            color = self.normal
        elif self.state == 'selected':
            color = self.selected
        elif self.state == 'clicked':
            color = self.clicked

        if self.button_pars[0] == 'rect':
            pygame.draw.rect(screen, pygame.Color(color), self.rect, 0)
        if len(self.button_pars) > 1:
            self.text.render(screen)
            
class GUI_Slider(GUI_Object):  ##not_now
    pass


class GUI_Changeable_Label(GUI_Object):  ##bad_code: args
    def __init__(self, name, position, dependency, bg, value_color, text):
        super().__init__(name, position)
        self.dependency = dependency
        self.bg, self.value_color, self.text = bg, value_color, text
        if bg is not None:
            self.rect = pygame.Rect(position[0], position[1])

    def make_rect(self, par, value):
        if value[2] == 'tall':
            return pygame.Rect((self.position[0][0], self.position[0][1]+par), (self.position[1][0], self.position[1][1]-par))
        elif value[2] == 'wide':
            return pygame.Rect((self.position[0][0]+par, self.position[0][1]), (self.position[1][0]-par, self.position[1][1]))

    def render(self):
        global screen
        value = self.dependency(1)
        
        if self.bg is not None:
            pygame.draw.rect(screen, pygame.Color(self.bg), self.rect, 0)
            if self.value_color[1] is not None:
                r = self.make_rect(int(self.position[1][1]*(1-value[1])), self.text)
                pygame.draw.rect(screen, pygame.Color(self.value_color), r, 0)

        if self.text[1] == 'False':
            font = pygame.font.Font(None, self.text['size'])
            text = font.render(value[0], 1, self.text['color'])
            screen.blit(text, (self.position[0][0] + self.position[2][0], self.position[0][1] + self.position[2][1]))


class GUI_Text_Field(GUI_Object):
    def __init__(self, name, position, text, bg, tx_color, font_size, count_type, count_factor, clicked):
        super().__init__(name, position)
        self.field = GUI_Label_Countable('0', [position[0], (position[1][0], None), (5, 5)], text, bg, tx_color, font_size, 'limit_width', None)
        #self.position = self.field.position
        self.bg = bg
        self.clicked = clicked
        self.state = 'normal'

    def func(self, thing):
        if thing.type == pygame.MOUSEBUTTONDOWN:
            return self.position

    def texting(self, event):
        if event.key != pygame.K_BACKSPACE:        
            self.field.text = ''.join(self.field.text) + event.unicode
        else:
            self.field.text = ''.join(self.field.text)[:-1]
        

    def render(self, screen):
        if self.state != 'normal':
            self.field.bg = self.clicked
        elif self.state == 'normal':
            self.field.bg = self.bg
        self.field.render(screen)
        #self.position = self.field.position

if __name__ == '__main__':
    print('Start GUI')
