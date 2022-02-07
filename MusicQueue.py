from tkinter import ttk
from tkinter import *
import math

class MusicQueue:
    def __init__(self):
        #self.playlistPosition
        #eh just use musicController playlistPosition
        self.mainFrame = None
        #self.initUI()

        self.singleMusicEntries = []
    
    def addMusicsToQueue(self, singleMusics, musicController):
        for singleMusic in singleMusics:
            currSingleMusicEntry = SingleMusicEntry(playlistNum=len(self.singleMusicEntries), name=singleMusic.filename, artist="resign", duration=singleMusic.songDur, musicController=musicController)
            currSingleMusicEntry.initUI(self.mainFrame, column=0, row=len(self.singleMusicEntries))
            self.singleMusicEntries.append(currSingleMusicEntry)

    def initUI(self, parent):
       self.mainFrame = parent

    def updateCurrPlaylistQueue(self, playlistNum):
        pass

    #def initUI(self, parent, row, column):
    #    self.mainFrame = ttk.Frame(parent)
    #    pass


class SingleMusicEntry:
    def __init__(self, playlistNum, name, artist, duration, musicController):
        self.playlistNum = playlistNum
        self.name = name
        self.artist = artist
        self.duration = str(math.ceil(duration))
        self.mainFrame = None
        self.musicController = musicController

    def initUI(self, parent, column, row):
        self.mainFrame = ttk.Frame(parent, style="MusicSelectionFrame.TFrame")
        self.skipToPlaylistButton = ttk.Button(self.mainFrame, command=lambda:self.musicController.skipToPlaylistPos(newPos=self.playlistNum), text="skip to")
        self.nameLabel = ttk.Label(self.mainFrame, text=self.name)
        self.artistLabel = ttk.Label(self.mainFrame, text=self.artist)
        self.durationLabel = ttk.Label(self.mainFrame, text=self.duration)

        self.skipToPlaylistButton.grid(column=0, row=0, rowspan=2, sticky=(N, W, E, S))
        self.nameLabel.grid(column=1, row=0, columnspan=2, sticky=(N, W, E, S))
        self.artistLabel.grid(column=1, row=1, sticky=(N, W, E, S))
        self.durationLabel.grid(column=2, row=1, sticky=(N, W, E, S))

        self.mainFrame.grid(column=column, row=row, sticky=(N, W, E, S))

    def destory(self):
        #Do I need this? supposedly unliking it would put it into trash collector whatever
        pass