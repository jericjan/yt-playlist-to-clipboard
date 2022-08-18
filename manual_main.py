import pyperclip
from pynput.keyboard import Key, Listener, Controller
from subprocess import Popen, PIPE
import json
import os
import sys



if not os.path.exists('manual.txt'):
    print("There is no manual.txt file. Creating one now. Place your urls in here separeted by newlines")
    with open('manual.txt', 'w') as f:
        f.write('')
    sys.exit()

print("Enter prefix: (blank to skip)")
prefix = input()
    
with open('manual.txt') as f:
    lines = f.readlines()
    
if not lines:
    print("manual.txt is empty. put stuff in it")
    sys.exit()
else:
    lines = [f"{prefix}{x.strip()}" for x in lines]


print("\nNow press the right arrow key and it will paste the URLs in order on every press.\nIt is also inside URLs.txt in case you want to use those URLs for something else.")

index = 0

def on_release(key):
    global index
    if key == Key.right:        
        keyboard = Controller()
        try:
            pyperclip.copy(lines[index])
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release(Key.ctrl)
            keyboard.release('v')        
            index += 1
        except IndexError:
            pass

with Listener(on_release=on_release) as listener:
    listener.join()
    