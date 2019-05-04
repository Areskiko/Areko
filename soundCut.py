from youtube_dl import YoutubeDL
import pydub
import subprocess
import re
import os
from tkinter import filedialog
from tkinter import *
from functools import partial
import webbrowser
url = "https://www.youtube.com/"

tempTitle = "temporary"

mode ="Select Local File"

#youtube_dl can't find ffmpeg so converting manually
def convert(fileInput, fileOutput):
    cmds = ['ffmpeg', '-i', fileInput, fileOutput, "-loglevel", "quiet", "-y"]
    subprocess.call(cmds)

def downloadMp3(video):
    ydl_opts = {
        "format" : "mp4",
        'outtmpl': '{}.mp4'.format(tempTitle),
        "quiet": True
    }
    ydl = YoutubeDL(ydl_opts)
    ydl.download([video])

    info_dict = ydl.extract_info(video, download=False)
    video_title = info_dict.get('title', None)
    print(video_title)

    convert(tempTitle+".mp4", tempTitle+".mp3")
    os.remove(tempTitle+".mp4")

def openFileExplorer():
    return filedialog.askopenfilename( filetypes = ( ("MP3 Format", "*.mp3"), ("All Files", "*.*") ) )

def browse():
    if mode =="Youtube Link":
        webbrowser.open(url)

    else:
        path = openFileExplorer()
        pathSrtingVar.set(path)
        
def edit(*args):
    global mode
    mode = tkvar.get()
    if mode == "Youtube Link":
        pathSrtingVar.set("Click browse to open youtube and copy the link to the video here")

    else:
        pathSrtingVar.set("Enter path to file, or click browse to find")
        
def resize(*args):
    cont = pathSrtingVar.get()
    pathEntry.grid(row=3, column=1, ipadx=len(cont)*2)
    #pathEntry.update()

class Section():
    def __init__(self, audio):
        self.songContent = audio
        self.songLength = self.songContent.__len__()/1000
        self.smolFrame = Frame(mainFrame)
        self.smolFrame.pack()

        Label(self.smolFrame, text="Selection {}".format(len(selections))).pack(side=TOP)

        s = Scale(self.smolFrame, orient=HORIZONTAL, from_=0, to=self.songLength)
        s.pack()

        s2 = Scale(self.smolFrame, orient=HORIZONTAL, from_=0, to=self.songLength)
        s2.pack()


def start(*args):
    path = pathSrtingVar.get()
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            songContent = pydub.AudioSegment.from_mp3(path)
            sect = Section(songContent)
            global selections
            selections.append(sect)

            
            
    else:
        pass

#Start of App
root = Tk()
#root.geometry("500x500")

#Non work frame
topFrame = Frame(root)
topFrame.pack(side=TOP, fill=X)

#Title
title = Label(topFrame, text="Areko", font=("Arial", 16))
title.grid(row=0, column=1)

#Method Choice
tkvar = StringVar(topFrame)
choices = {"Select Local File":"SLF", "Youtube Link":"YL"}
tkvar.set("Select Mode")
tkvar.trace('w', edit)

optionsMenu = OptionMenu(topFrame, tkvar, *choices)
optionsMenu.grid(row=2, column=1)


#Path input and Browse button
pathSrtingVar = StringVar(topFrame)
pathSrtingVar.trace('w', resize)
pathEntry = Entry(topFrame, text=pathSrtingVar)
pathEntry.grid(row=3, column=1, ipadx=120)

selectButton = Button(topFrame, text="Browse", command=browse)
selectButton.grid(row=3, column=2)

startButton = Button(topFrame, text="Select", command=start)
startButton.grid(row=3, column=3)


#Working Frame
mainFrame = Frame(root)
mainFrame.pack(fill=X)

selections = []


root.mainloop()