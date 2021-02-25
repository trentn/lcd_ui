import time
import random
import threading
import subprocess

from . import UI_Element, InvalidDirection
from .content import Content, DynamicContent, ScrollingContent

class DialInput(UI_Element):
    def __init__(self, label, init_value):
        self.label = label
        self.value = init_value
        self.set = False

    def scroll(self,dir):
        self.set = False
        if dir == 'up':
            self.value = self.value + 1
        elif dir == 'down':
            self.value = self.value - 1
        else:
            pass

    def cycle(self):
        pass

    def select(self):
        pass

    def get_display(self):
        return [self.label, str(self.value)]


class SelectTemp(DialInput):
    def select(self):
        with open('/tmp/target_temp','w') as f:
            str_val = str(self.value)
            f.write(str_val+'0'*max(0,5-len(str_val)))
        self.set = True




class ListInput(UI_Element):
    def __init__(self, options, num_lines=2):
        self._options = options
        self._num_lines = num_lines
        self._select_line = 0
        self._display_start = 0
        self._display_threads = []
        self.is_displayed = False

    def scroll_display(self,dir):
        if dir == 'up':
            if self._display_start > 0:
                self._display_start = (self._display_start - 1)
        elif dir == 'down':
            if self._display_start < len(self._options)-self._num_lines:
                self._display_start = (self._display_start + 1)
        else:
            raise InvalidDirection

    def scroll(self,dir):
        if dir == 'up':
            if self._select_line > 0:
                self._select_line = (self._select_line - 1)
            else:
                self.scroll_display('up')
        elif dir == 'down':
            if self._select_line < self._num_lines-1:
                self._select_line = (self._select_line + 1)
            else:
                self.scroll_display('down')
        else:
            raise InvalidDirection

    def cycle(self):
        pass

    def select(self):
        pass

    def get_display(self):
        lines = self._options[self._display_start:self._display_start+self._num_lines]
        lines = [">" + str(line[0]) if i==self._select_line else " " + str(line[0]) for i,line in enumerate(lines)]
        return lines

    def start(self,event_queue):
        self.is_displayed = True
        for entry in self._options:
            if isinstance(entry[0],DynamicContent):
                t = threading.Thread(target=entry[0].run,args=(event_queue,),daemon=True)
                t.start()
                self._display_threads.append(t)
    
    def stop(self):
        self.is_displayed = False


class SSIDList(ListInput):
    def __init__(self,num_lines=2):
        super().__init__(None,num_lines)

    def start(self,event_queue):
        self._options = []
        result = subprocess.check_output('iwlist wlan0 scan | grep ESSID', shell=True, text=True)
        for r in result.strip().split('\n'):
            option = ScrollingContent('', dynamic_content=r.split('"')[1])
            option.set_parent(self)
            self._options.append((option,None)) 
        super().start(event_queue)
