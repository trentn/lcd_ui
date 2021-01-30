import queue
from .lcd_proxy import LCDProxy
from .ui_elements import Menu, Content, DisplayFileLine

class UI(object):
    def __init__(self, root_elem):
        self.display = LCDProxy()
        self.prev_menus = []
        self.current_elem = root_elem
        self.update_display()
        self.event_queue = queue.Queue()

    def run(self):
        def print_display():
            print() 
            print(self.display)

        print_display()
        
        i = None
        while i != 'quit':
            e = self.event_queue.get()
            if e['type'] == 'input':
                i = e['val']
                if e['val'] == 'quit':
                    continue
                self.handle_input(i)
                self.update_display()
            if e['type'] == 'display_update':
                self.update_display()

            print_display()
    
    def handle_input(self,input):
        if input == 'up':
            self.current_elem.scroll('up')
        
        elif input == 'down':
            self.current_elem.scroll('down')
        
        elif input == 'select':
            if isinstance(self.current_elem,Menu):
                self.goto_next_menu()
            else:
                pass

        elif input == 'cycle':
            self.current_elem.cycle()
        
        elif input == 'back':
            self.go_back_menu()

    def update_display(self):
        self.display.clear()
        lines = self.current_elem.get_display()
        for i,line in enumerate(lines):
            self.display.cursor_pos(i,0)
            self.display.write_word(line)

    def goto_next_menu(self):
        next_menu = self.current_elem.select()
        if next_menu:
            self.prev_menus.append(self.current_elem)
            self.current_elem = next_menu
            self.current_elem.start(self.event_queue)

    def go_back_menu(self):
        if self.prev_menus:
                self.current_elem.stop()
                self.current_elem = self.prev_menus.pop()