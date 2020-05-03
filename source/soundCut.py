# pylint: disable=unused-wildcard-import
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
import math
import time
import threading
import ntpath
import datetime
import logging
logging.basicConfig(filename='areko.log', filemode='a', format='%(levelname)s - %(message)s')

tempTitle = "video_from_youtube"

mode ="Select Local File"

#youtube_dl can't find ffmpeg so converting manually
def convert(fileInput, fileOutput):
    cmds = ['ffmpeg', '-i', fileInput, fileOutput, "-loglevel", "quiet", "-y"]
    subprocess.Popen(cmds)

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

    convert(tempTitle+".mp4", tempTitle+".mp3")
    while not os.path.isfile(tempTitle+".mp3"):
        pass
    while True:
        try:
            os.rename(tempTitle+".mp4", tempTitle+".mp4")
            break
        except WindowsError:
            pass
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
        pathSrtingVar.set("Youtube link")

    else:
        pathSrtingVar.set("Path to file")

class Section():
    def __init__(self, audio, path):
        self.ID = len(selections)
        self.songContent = audio
        self.songLength = self.songContent.__len__()/1000
        self.smolFrame = Frame(mainFrame, pady=5)
        self.smolFrame.pack()

        Label(self.smolFrame, text=(ntpath.split(path)[1])[:40], width=38, font="Arial 10 bold" ).grid(row=0, column=0, columnspan=3, sticky="W")

        self.deleteButton = Button(self.smolFrame, text="Remove", command=lambda: delete(self.smolFrame, self.ID))
        self.deleteButton.grid(row=1, column=2, sticky="E")

        self.inverted = BooleanVar()
        self.inverted.set(False)
        self.reverseBox = Checkbutton(self.smolFrame, text="Invert Selection", variable=self.inverted, onvalue=True, offvalue=False)
        self.reverseBox.grid(row=2, column=2, sticky="E")

        self.lab1 = Label(self.smolFrame, text="From 0:0")
        self.lab1.grid(row=1, column=1, sticky="W")

        self.s = Scale(self.smolFrame, orient=HORIZONTAL, from_=0, to=self.songLength, command=self.updt1, showvalue=0, length=100)
        self.s.bind("<Button-1>", self.take_focus_1)
        self.s.grid(row=1, column=0, sticky="W")

        self.lab2 = Label(self.smolFrame, text="To 0:0")
        self.lab2.grid(row=2, column=1, sticky="W")

        self.s2 = Scale(self.smolFrame, orient=HORIZONTAL, from_=0, to=self.songLength, command=self.updt2, showvalue=0, length=100)
        self.s2.bind("<Button-1>", self.take_focus_2)
        self.s2.grid(row=2, column=0, sticky="W")
    
    def take_focus_1(self, event):
        self.s.focus_set()
    def take_focus_2(self, event):
        self.s2.focus_set()

    def updt1(self, val):
        val= int(val)
        try:
            hms = str(datetime.timedelta(seconds=val)).split(":")
            minutes = (hms[1])
            seconds = int(hms[2])
            fromTime = "From {}:{}".format(minutes, seconds)
        except NameError:
            fromTime = "From 0:0"
        self.lab1.config(text=fromTime)
        if self.s2.get() < val:
            self.s2.set(val+1)

    def updt2(self, val):
        val= int(val)
        try:
            hms = str(datetime.timedelta(seconds=val)).split(":")
            minutes = (hms[1])
            seconds = int(hms[2])
            fromTime = "To {}:{}".format(minutes, seconds)
        except NameError:
            fromTime = "To 0:0"
        self.lab2.config(text=fromTime)
        if val < self.s.get():
            self.s2.set(self.s.get()+1)

def delete(frame, ID):
    try:
        frame.destroy()
        del selections[ID]
    except Exception as e:
        logging.error(e)
        loadingLable['text'] = "Unexpected Error, see error log"



def start(*args):
    loadingLable['text'] = "Loading"
    try:
        if mode == "Select Local File":
            path = pathSrtingVar.get()
            if os.path.isfile(path):
                threading.Thread(target=load, args=(pathSrtingVar.get(),)).start()
            else:
                loadingLable.config(text="")
        else:
            YtLoadThread(pathSrtingVar.get())
    except Exception as e:
        logging.error(e)
        loadingLable['text'] = "Unexpected Error, see error log"


def YtLoadThread(path):
    try:
        threading.Thread(target=LoadYt, args=(path,)).start()
    except Exception as e:
        logging.error(e)
        loadingLable['text'] = "Unexpected Error, see error log"

def LoadYt(path):
    try:
        downloadMp3(path)
        load(tempTitle+".mp3")
    except Exception as e:
        logging.error(e)
        loadingLable['text'] = "Unexpected Error, see error log"
    
def load(path):
    try:
        songContent = pydub.AudioSegment.from_mp3(path)
        sect = Section(songContent, path)
        global selections
        selections.append(sect)
        loadingLable.config(text="")
    except Exception as e:
        logging.error(e)
        loadingLable['text'] = "Unexpected Error, see error log"

def exportBrowse():
    exportPathVar.set(filedialog.askdirectory())

def export():
    try:
        if (os.path.exists(exportPathVar.get())) and (not os.path.isfile(exportPathVar.get())):
            if exportNameVar.get == "":
                exportNameVar.set("example")
            whole = pydub.AudioSegment.empty()
            for sect in selections:
                segmentStart = sect.s.get()*1000
                segmentEnd = sect.s2.get()*1000
                if sect.inverted.get():
                    firstSegment = sect.songContent[:segmentStart]
                    secondSegment = sect.songContent[segmentEnd:]
                    whole+=firstSegment
                    whole+=secondSegment
                else:
                    segment = sect.songContent[segmentStart:segmentEnd]
                    whole+=segment
            name = exportNameVar.get().replace(".mp3", "")
            whole.export(exportPathVar.get()+"/"+name+".mp3", format="mp3")
            exportLabel['text'] = "Complete"
            time.sleep(5)
            exportLabel['text'] = ""
        else:
            exportBrowse()
    except Exception as e:
        logging.error(e)
        loadingLable['text'] = "Unexpected Error, see error log"

def exportThread():
    try:
        exportLabel['text'] = "Exporting"
        threading.Thread(target=export).start()
    except Exception as e:
        logging.error(e)
        loadingLable['text'] = "Unexpected Error, see error log"
#Start of App
root = Tk()
#root.geometry("500x500")

#Non work frame
topFrame = Frame(root)
topFrame.pack(fill=X)

#Title
menuFrame = Frame(topFrame)
menuFrame.pack(expand=1)
title = Label(menuFrame, text="Areko", font=("Arial", 16))
title.pack(side=TOP)

#Method Choice
tkvar = StringVar(menuFrame)
choices = {"Select Local File":"SLF", "Youtube Link":"YL"}
tkvar.set("Select Mode")
tkvar.trace('w', edit)

optionsMenu = OptionMenu(menuFrame, tkvar, *choices)
optionsMenu.pack(side=TOP)


#Path input and Browse button
pathSrtingVar = StringVar(menuFrame)
#pathSrtingVar.trace('w', resize)
pathEntry = Entry(menuFrame, text=pathSrtingVar)
pathEntry.pack(side=LEFT)

selectButton = Button(menuFrame, text="Browse", command=browse)
selectButton.pack(side=LEFT)

startButton = Button(menuFrame, text="Add", command=start)
startButton.pack(side=LEFT)

#Loading Warning
loadingFrame = Frame(root)
loadingFrame.pack(fill=X)
loadingLable = Label(loadingFrame)
loadingLable.pack(side=TOP)


#Working Frame
mainFrame = Frame(root)
mainFrame.pack(fill=X)

selections = []



#Export Frame
exportFrame = Frame(root)
exportFrame.pack(side=BOTTOM)

exportPathVar = StringVar(exportFrame)
exportNameVar = StringVar(exportFrame)

topExportFrame = Frame(exportFrame)
topExportFrame.pack(side=TOP)

Label(topExportFrame, text="Folder").pack(side=LEFT)
pathEntry = Entry(topExportFrame, text=exportPathVar)
pathEntry.pack(side=LEFT)
selectButton = Button(topExportFrame, text="Browse", command=exportBrowse)
selectButton.pack(side=LEFT)

bottomExportFrame = Frame(exportFrame)
bottomExportFrame.pack(side=BOTTOM)

Label(bottomExportFrame, text="Name").pack(side=LEFT)
nameEntry = Entry(bottomExportFrame, text=exportNameVar)
nameEntry.pack(side=LEFT)
exportButton = Button(bottomExportFrame, text="Export", command=exportThread)
exportButton.pack(side=LEFT)

exportLabel = Label(bottomExportFrame, text="")
exportLabel.pack(side=BOTTOM)

root.mainloop()
if os.path.isfile(tempTitle+".mp3"):
    os.remove(tempTitle+".mp3")
if os.path.isfile(tempTitle+".mp4"):
    os.remove(tempTitle+".mp4")