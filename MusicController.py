import time
import AudioVisualizer
import simpleaudio as sa
from tkinter import *
from tkinter import ttk
from SingleMusic import SingleMusic
from AudioVisualizer import AudioVisualizer
from MusicQueue import MusicQueue
import math

class MusicController:
    def __init__(self, audioVis, root, musicQueue):
        self.root = root
        self.currPlaylist = []
        self.musicQueue = musicQueue
        self.playlistPosition = 0
        self.musicPosition = 0
        self.audioVis = audioVis

        #mostly temp stuff
        self.currSong = None
        self.audioPlayObj = None
        self.opStart = 0
        self.musicLength = 0
        self.musicPaused = True
        self.reset = False
        self.updateMusicPositionExists = False
        self.volume = -12

        self.musicVolumeBar = MusicVolumeBar(self)
        self.musicBar = MusicProgressBar(self)

    def startPlaying(self):
        print("curr playlistpos: " + str(self.playlistPosition))
        print("trying to play")
        if (not self.musicPaused):
            return -1

        if (self.playlistPosition < 0):
            self.playlistPosition = 0

        if (self.playlistPosition >= len(self.currPlaylist)):
            print("playlist position is too high!")
            print(len(self.currPlaylist))
            return -1

        currAudio = self.currPlaylist[self.playlistPosition]
        #UPDATE VOLUME (PROBABLY ONLY DO THIS WHEN NEW SONG, OTHERWISE IT WILL DO IT EVERY TIME IT pAUSES)
        currAudio.updateVolume(self.volume)

        self.musicLength = currAudio.songDur
        print("music length: " + str(self.musicLength))

        #if (self.musicPosition >= self.musicLength):
        #    print("music is over")
        #    self.musicEnd()
        #    return -1
        self.currSong = currAudio
        self.musicPaused = False
        currSample, self.musicPosition = currAudio.getSegmentFromLocation(self.musicPosition)
        self.audioPlayObj = sa.play_buffer(currSample, num_channels=currAudio.numChannels, bytes_per_sample=currAudio.bytesPerSample, sample_rate=currAudio.sampleRate)
        self.playStart = time.time()
        self.opStart = time.time()
        print(self.updateMusicPositionExists)
        if (not self.updateMusicPositionExists):
            print("starting new updateMusicPosition")
            print("curr Music Pos: " + str(self.musicPosition))
            self.root.after(0, lambda:self.updateMusicPosition(self.root))
            self.updateMusicPositionExists = True

    def updateMusicPosition(self, root):
        now = time.time()
        deltaTime = now - self.opStart
        self.opStart = now
        self.musicPosition += deltaTime
        if (self.musicPaused):
            print("music paused")
            self.updateMusicPositionExists = False
            return -1
        #if (self.reset):
        #    deltaTime = 0
        #    self.reset = False
        if (self.musicPosition >= self.musicLength):
            print("music ended UPDATE")
            print(self.musicPosition)
            print(self.musicLength)
            self.updateMusicPositionExists = False
            self.musicEnd()
            return 1
        else:
            #audio vis stuff
            self.audioVis.drawVisDataOnce(self.currSong, self.musicPosition)
            self.musicBar.updateProgress(self.musicPosition, self.musicLength)
            root.after(50, lambda:self.updateMusicPosition(root))

    def musicEnd(self):
        self.musicPosition = 0
        print("old playlistPos: " + str(self.playlistPosition))
        self.playlistPosition += 1
        self.musicPaused = True
        self.stopPlaying()
        if (self.audioPlayObj == None):
            print("audioobj is none")
        #self.reset = True
        if (self.playlistPosition >= len(self.currPlaylist)):
            print("playlist out of bounds, " + str(len(self.currPlaylist)))
            print("currPlaylistPos: " + str(self.playlistPosition))
            self.playlistPosition -= 1
        else:
            self.startPlaying()

    def stopPlaying(self):
        print("pausing")
        self.reset = True
        if (self.audioPlayObj != None):

            self.audioPlayObj.stop()
            self.musicPaused = True
            self.reset = True
        else:
            print("audio play obj is none")

    def skipToPos(self, newPos=None, increment=None, percent=None):
        self.stopPlaying()
        if (increment != None):
            self.musicPosition = increment
        elif (newPos != None):
            self.musicPosition = newPos
        elif (percent != None):
            pass
        self.startPlaying()
    
    def skipToPlaylistPos(self, newPos=None, increment=None):
        self.stopPlaying()
        self.musicPosition = 0
        if (increment != None):
            self.playlistPosition += increment
            pass
        elif (newPos != None):
            self.playlistPosition = newPos
            pass

        self.startPlaying()
    
    def setNewPlaylist(self):
        pass

    def addToPlaylist(self, singleMusics):
        print(len(singleMusics))
        for singleMusic in singleMusics:
            self.currPlaylist.append(singleMusic)
        self.musicQueue.addMusicsToQueue(singleMusics, self)
    
    def adjustVolume(self, volume):
        self.volume = volume
        #MAYBE PAUSE
        if (self.currSong != None):
            self.stopPlaying()
            self.currSong.updateVolume(volume)
            self.startPlaying()

    def initUI(self, parent, column, row):
        mainFrameLabel = ttk.Label(text="Music Controller")
        mainFrame = ttk.LabelFrame(parent, style="BackgroundLabelframe.TLabelframe", labelwidget=mainFrameLabel)
        #mainFrame.winfo_reqheight=15
        playButton = ttk.Button(mainFrame, text="play", command=self.startPlaying, style="TButton")
        pauseButton = ttk.Button(mainFrame, text="pause", command=self.stopPlaying, style="TButton")
        skipSongButton = ttk.Button(mainFrame, text="skip song", command=lambda:self.skipToPlaylistPos(increment=1), style="TButton")
        rewindButton = ttk.Button(mainFrame, text="rewind", command=lambda:self.skipToPos(newPos=0), style="TButton")
        goBackButton = ttk.Button(mainFrame, text="go back", command=lambda:self.skipToPlaylistPos(increment=-1), style="TButton")
        
        self.musicBar.initUI(mainFrame, 0, 0, 1)
        self.musicVolumeBar.initUI(mainFrame, column=1, row=1, columnspan=1, rowspan=5)

        playButton.grid(column=0, row=1, sticky=(N, W, E, S))
        pauseButton.grid(column=0, row=2, sticky=(N, W, E, S))
        skipSongButton.grid(column=0, row=3, sticky=(N, W, E, S))
        rewindButton.grid(column=0, row=4, sticky=(N, W, E, S))
        goBackButton.grid(column=0, row=5, sticky=(N, W, E, S))

        mainFrame.columnconfigure(0, weight=1)
        for i in range(5):
            mainFrame.rowconfigure(i+1, weight=1)
        mainFrame.grid(column=column, row=row, sticky=(N, W, E, S))

class MusicProgressBar:
    def __init__(self, musicController):
        self.progressCanvas = None
        self.progressRectangle = None
        self.canvasHeight = 0
        self.canvasWidth = 0
        self.currSongLength = 0
        self.currSongPosition = 0
        self.musicController = musicController

    def updateProgress(self, currTime, songTime):
        self.currSongLength = songTime
        self.currSongPosition = currTime
        #print("----")
        #print((currTime//songTime)*self.canvasWidth)
        #print(self.canvasWidth)
        if (songTime == 0):
            return -1
        self.progressCanvas.coords(self.progressRectangle, 0, 0, math.floor((currTime/songTime)*self.canvasWidth), self.canvasHeight)

    def initUI(self, parent, row, column, columnspan):
        self.mainFrame = ttk.Frame(parent, style="BackgroundFrame.TFrame")
        #self.mainFrame.winfo_reqheight=15
        self.progressCanvas = Canvas(self.mainFrame, bg= "#002635", highlightthickness=0, height=50)
        self.canvasHeight = self.progressCanvas.winfo_height()
        self.canvasWidth = self.progressCanvas.winfo_width()
        self.progressRectangle = self.progressCanvas.create_rectangle(0, 0, 0, self.canvasHeight, fill="#00ffff")
        
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.rowconfigure(0, weight=1)
        self.progressCanvas.bind("<Configure>", lambda event: self.onResize(event))
        self.progressCanvas.bind("<Button-1>", lambda event: self.skipToMusicPos(event))

        self.progressCanvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainFrame.grid(row=row, column=column, columnspan=columnspan, sticky=(N, W, E, S))

    def skipToMusicPos(self, event):
        mousePosX = event.x
        musicPercent = mousePosX / self.canvasWidth
        musicTime = self.currSongLength * musicPercent
        self.musicController.skipToPos(newPos=musicTime)
        #get percentage of canvas, skip to song

    def onResize(self, event):
        self.canvasHeight = self.progressCanvas.winfo_height()
        self.canvasWidth = self.progressCanvas.winfo_width()
        self.updateProgress(self.currSongPosition, self.currSongLength)

class MusicVolumeBar:
    def __init__(self, musicController):
        self.volumeCanvas = None
        self.volumeRectangle = None
        self.lowestDb = -36
        self.currDb = -12
        self.musicController = musicController

    def initUI(self, parent, column, row, columnspan, rowspan):
        self.mainFrame = ttk.Frame(parent, style="BackgroundFrame.TFrame")
        self.volumeCanvas = Canvas(self.mainFrame, bg= "#002635", highlightthickness=0, width=25)
        self.volumeRectangle = self.volumeCanvas.create_rectangle(0, 0, self.volumeCanvas.winfo_width(), self.volumeCanvas.winfo_height(), fill="#00ffff")
        self.volumeCanvas.bind("<Configure>", lambda event:self.adjustCanvas())
        self.volumeCanvas.bind("<Button-1>", lambda event:self.adjustVolume(event))
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)
        self.volumeCanvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainFrame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=(N, W, E, S))

    def adjustVolume(self, event):
        #get percentage down
        newVolume = math.floor(self.lowestDb * (event.y /self.volumeCanvas.winfo_height()))
        self.currDb = newVolume
        print("new volume: " + str(newVolume))
        self.adjustCanvas()
        self.musicController.adjustVolume(newVolume)

    def adjustCanvas(self):
        #self.volumeCanvas.coords(self.volumeRectangle, 0, 0, self.volumeCanvas.winfo_width(), self.volumeCanvas.winfo_height())
        #print("new volume bar height: " + str(math.floor(1 - (self.currDb / self.lowestDb))))
        self.volumeCanvas.coords(self.volumeRectangle, 0, math.floor(((self.currDb / self.lowestDb)) * self.volumeCanvas.winfo_height()), self.volumeCanvas.winfo_width(), self.volumeCanvas.winfo_height())

class MusicThread:
    def __init__(self, audioQueue):
        self.audioQueue = audioQueue

        pass

    def mainLoop(self):
        while (True):
            #if (self.audioQueue)
            pass
            
        pass

    def handleQueueEvents(self):
        pass
def main():
    root = Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    audioVis = AudioVisualizer()
    audioVis.initUI(root, column=0, row=0)
    musicController = MusicController(audioVis, root)
    playButton = ttk.Button(root, text="play", command=musicController.startPlaying)
    pauseButton = ttk.Button(root, text="pause", command=musicController.stopPlaying)
    skipSongButton = ttk.Button(root, text="skip song", command=lambda:musicController.skipToPlaylistPos(increment=1))
    rewindButton = ttk.Button(root, text="rewind", command=lambda:musicController.skipToPos(newPos=0))
    goBackButton = ttk.Button(root, text="go back", command=lambda:musicController.skipToPlaylistPos(increment=-1))

    playButton.grid(column=0, row=1, sticky=(N, W, E, S))
    pauseButton.grid(column=0, row=2, sticky=(N, W, E, S))
    skipSongButton.grid(column=0, row=3, sticky=(N, W, E, S))
    rewindButton.grid(column=0, row=4, sticky=(N, W, E, S))
    goBackButton.grid(column=0, row=5, sticky=(N, W, E, S))

    filename = "/Users/gold_spaghetti/Documents/music/oddling/divide/Single - divide.mp3"
    filename2 = "/Users/gold_spaghetti/Documents/music/oddling/one/01 - ascend.mp3"
    currSong = SingleMusic(filename)
    currSong2 = SingleMusic(filename2)
    musicController.currPlaylist.append(currSong)
    musicController.currPlaylist.append(currSong2)

    root.mainloop()
    pass

if (__name__ == "__main__"):
    main()