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

mode ="Youtube Link"

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
    if mode =="Select Local File":
        path = openFileExplorer()
        pathEntry.delete(0, END)
        pathEntry.insert(0, path)

    else:
        webbrowser.open(url)
        
def edit(*args):
    global mode
    mode = tkvar.get()
    if mode == "Select Local File":
        pathEntry.delete(0, END)
        pathEntry.insert(0, "Enter path to file, or click browse to find")
    else:
        pathEntry.delete(0, END)
        pathEntry.insert(0, "Click browse to open youtube and copy the link to the video here")

root = Tk()
root.geometry("500x500")



selectionFrame = Frame(root)
selectionFrame.pack(side=TOP, fill=X)

mainFrame = Frame(root)
mainFrame.pack()

exportFrame = Frame(root)
exportFrame.pack(side=BOTTOM)


tkvar = StringVar(root)
choices = {"Select Local File":"SLF", "Youtube Link":"YL"}
tkvar.set("Select Method")
tkvar.trace('w', edit)

optionsMenu = OptionMenu(selectionFrame, tkvar, *choices)
optionsMenu.pack(fill=X)


pathEntry = Entry(selectionFrame)
#pathEntry.grid(row=0)
pathEntry.pack(side=LEFT, fill=X, expand=1)

selectButton = Button(selectionFrame, text="Browse")
#selectButton.grid(row=0, column=1)
selectButton.pack(side=RIGHT)


label = Label(mainFrame, text="MainFrame")
label.pack()
exportLabel = Label(exportFrame, text="ExportFrame")
exportLabel.pack()



root.mainloop()