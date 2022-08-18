"""
The Main File
"""

from subprocess import Popen, PIPE
import os
import json
import sys
import argparse
from pynput.keyboard import Key, Listener, Controller
import pyperclip

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--manual", action="store_true")
args = vars(parser.parse_args())


START, END = 0, -1
EXTRA = ""

def get_start():
    "Asks for the index to start at"
    global START
    print("\nType what number you want start at:")
    START = input()
    START = int(START)
    try:
        url_list[START]
    except IndexError:
        print("Index doesn't exist. Try again.")
        get_start()


def get_end():
    "Asks for the index to end at"
    global END
    print("\nType what number you want to end at:")
    END = input()
    END = int(END)
    try:
        url_list[END]
    except IndexError:
        print("Index doesn't exist. Try again.")
        get_end()
    END = int(END) + 1


print("Enter prefix: (blank to skip)")
prefix = input()

if args["manual"]:
    if not os.path.exists("manual.txt"):
        print(
            "There is no manual.txt file. Creating one now.\n"
            "Place your urls in here separeted by newlines"
        )
        with open("manual.txt", "w", encoding="utf-8") as f:
            f.write("")
        sys.exit()

    with open("manual.txt", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print("manual.txt is empty. put stuff in it")
        sys.exit()
    else:
        selected_list = [f"{prefix}{x.strip()}" for x in lines]
else:
    print("Enter your YT playlist:")
    url = input()
    print("\nPlease wait...\n")
    with Popen(
        ["youtube-dl", "--dump-json", "--flat-playlist", url],
        stdout=PIPE,
        stderr=PIPE,
        stdin=PIPE,
    ) as process:
        stdout, stderr = process.communicate()
    STR_OUTPUT = stdout.decode("utf-8")
    STR_OUTPUT = STR_OUTPUT.splitlines()
    STR_OUTPUT = ",".join(STR_OUTPUT)
    STR_OUTPUT = f"[{STR_OUTPUT}]"
    json_output = json.loads(STR_OUTPUT)

    title_list = []
    url_list = []
    for i in json_output:
        if "youtube" in url:
            x = i["title"]
            title_list.append(x)
            x = i["id"]
            x = prefix + "https://youtu.be/" + x
            url_list.append(x)
        elif "soundcloud" in url:
            x = i["title"]
            title_list.append(x)
            x = prefix + i["url"]
            url_list.append(x)
    title_list.reverse()
    url_list.reverse()

    for idx, i in enumerate(title_list):
        print(f"{idx} - {i}")

    get_start()
    get_end()
    selected_list = url_list[START:END]
    with open("URLs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(selected_list))
    EXTRA = "It is also inside URLs.txt in case you want to use those URLs for something else."

print(
    "\nNow press the right arrow key and it will paste the URLs in order on every press."
    f"\n{EXTRA}"
)

# with open('URLs.txt') as f:
# lines = f.readlines()

INDEX = 0


def on_release(key):
    "Check for a released key, and if it is the Right key, paste text"
    global INDEX
    if key == Key.right:
        keyboard = Controller()
        try:
            pyperclip.copy(selected_list[INDEX])
            keyboard.press(Key.ctrl)
            keyboard.press("v")
            keyboard.release(Key.ctrl)
            keyboard.release("v")
            INDEX += 1
        except IndexError:
            pass


with Listener(on_release=on_release) as listener:
    listener.join()
