from youtube_dl import YoutubeDL
import pydub
import subprocess
import re
import os
from tkinter import filedialog
from tkinter import *
from functools import partial

tempTitle = "temporary"

#youtube_dl can't find ffmpeg so converting manually
def convert(fileInput, fileOutput):
    cmds = ['ffmpeg', '-i', fileInput, fileOutput, "-loglevel", "quiet", "-y"]
    subprocess.call(cmds)

def downloadMp3():
    video = str(input("Link: "))
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
    file = filedialog.askopenfilename( filetypes = ( ("MP3 Format", "*.mp3"), ("All Files", "*.*") ) )


root = Tk()



selectionFrame = Frame(root)
selectionFrame.pack(side=TOP)

mainFrame = Frame(root)
mainFrame.pack()

exportFrame = Frame(root)
exportFrame.pack(side=BOTTOM)

selectButton = Button(selectionFrame, text="Select File", command=openFileExplorer )
selectButton.pack()


label = Label(mainFrame, text="MainFrame")
label.pack()
exportLabel = Label(exportFrame, text="ExportFrame")
exportLabel.pack()



root.mainloop()