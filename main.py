import pyperclip
from pynput.keyboard import Key, Listener, Controller
from subprocess import Popen, PIPE
import json

print('Enter your YT playlist:')
url = input()
print("Enter prefix: (blank to skip)")
prefix = input()
print("\nPlease wait...\n")
process = Popen(['youtube-dl', '--dump-json', '--flat-playlist',url], stdout=PIPE, stderr=PIPE, stdin=PIPE)
stdout, stderr = process.communicate()
str_output = stdout.decode("utf-8")
str_output = str_output.splitlines()
str_output = ','.join(str_output)
str_output = f"[{str_output}]"
json_output = json.loads(str_output)


title_list = []    
url_list = []
for i in json_output:
    if "youtube" in url:
        x = i['title']
        title_list.append(x)
        x = i['id']
        x = prefix + "https://youtu.be/"+x
        url_list.append(x)
    elif "soundcloud" in url:
        x = i['title']
        title_list.append(x)
        x = prefix + i['url']
        url_list.append(x)        
title_list.reverse()
url_list.reverse()    

for idx, i in enumerate(title_list):
    print(f"{idx} - {i}")

def get_start():    
    global start
    print("\nType what number you want start at:")
    start = input()
    start = int(start)
    try:
        url_list[start]
    except:
        print("Index doesn't exist. Try again.")
        get_start()
   
def get_end():
    global end
    print("\nType what number you want to end at:")
    end = input()   
    end = int(end)
    try:
        url_list[end]
    except:
        print("Index doesn't exist. Try again.")
        get_end()        
    end = int(end) + 1

    
get_start()
get_end()    
selected_list = url_list[start:end]

# for i in selected_list:
    # print(i)
    
with open('URLs.txt', 'w') as f:
    f.write('\n'.join(selected_list))    

print("\nNow press the right arrow key and it will paste the URLs in order on every press.\nIt is also inside URLs.txt in case you want to use those URLs for something else.")
    
# with open('URLs.txt') as f:
    # lines = f.readlines()

index = 0

def on_release(key):
    global index
    if key == Key.right:        
        keyboard = Controller()
        try:
            pyperclip.copy(selected_list[index])
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release(Key.ctrl)
            keyboard.release('v')        
            index += 1
        except IndexError:
            pass

with Listener(on_release=on_release) as listener:
    listener.join()
    