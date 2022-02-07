import librosa, math
import numpy as np
from tkinter import *
from tkinter import ttk
import time
from pydub import AudioSegment
from pydub.playback import play
from pathlib import Path

from SingleMusic import SingleMusic


class AudioVisualizer():
    def __init__(self):
        self.mainFrame = None
        self.canvasWidth = 0
        self.canvasHeight = 0
        self.widthIntervals = 0
        self.heightIntervals = 0
        self.canvas = None

        #FOR CHROMA TEST:
        self.rectNum = 12

        #REGULAR VIS
        #self.rectNum = 32
        
        self.rectangles = []

        self.drawingVis = False
        self.visStartTime = 0

    def resizeCanvas(self, event):
        self.canvasWidth= self.canvas.winfo_width()-1
        self.canvasHeight = self.canvas.winfo_height()-1
        self.widthIntervals = math.floor(self.canvasWidth/self.rectNum)
        self.heightIntervals = math.floor(self.canvasHeight/80)
        for i in range(self.rectNum):
            self.canvas.coords(self.rectangles[i], self.widthIntervals*i+2, self.canvasHeight, self.widthIntervals*(i+1)+2, self.canvasHeight)

    def getVisDataThread(self, visQueue, currSong):
        startTime = time.time()
        currTime = 0
        while (currTime < currSong.songDur):
            currSample = math.ceil(currTime / currSong.sampleDurationSec)
            sampleValues = []
            for i in range(currSong.audioVisArray.shape[0]):
                sampleValues.append(currSong.audioVisArray[i, currSample] + 80)
            visQueue.put(sampleValues)
    
    def startDrawVisData(self, root, currSong):
        self.drawingVis = True
        self.visStartTime = time.time()
        root.after(0, lambda:self.drawVisData(root, currSong))

    def drawVisData(self, root, currSong):
        currTime = time.time() - self.visStartTime
        if (not self.drawingVis or currTime >= currSong.songDur):
            return 0
        else:
            currSample = math.ceil(currTime / currSong.sampleDurationSec)
            sampleValues = []
            for i in range(currSong.audioVisArray.shape[0]):
                sampleValues.append(currSong.audioVisArray[i, currSample] + 80)
            
            for i in range(self.rectNum):
                currRectangle = self.rectangles[i]
                currRectangleCoors = self.canvas.coords(currRectangle)
                self.canvas.coords(currRectangle, currRectangleCoors[0], self.canvasHeight - (sampleValues[i] * self.heightIntervals), currRectangleCoors[2], currRectangleCoors[3])
            root.after(40, lambda:self.drawVisData(root, currSong))

    def drawVisDataOnce(self, currSong, currTime):
        if (currTime >= currSong.songDur):
            return 0
        else:
            currSample = math.ceil(currTime / currSong.sampleDurationSec)
            sampleValues = []
            #print(currSample)
            if (currSample >= currSong.audioVisArray.shape[1]):
                print("OVER TIME")
                return -1

            #FOR REGULAR VIS
            #for i in range(currSong.audioVisArray.shape[0]):
            #    sampleValues.append(currSong.audioVisArray[i, currSample] + 80)
            
            #CHROMA VIS
            for i in range(currSong.chromaData.shape[0]):
                sampleValues.append(currSong.chromaData[i, currSample] * 80)
            
            for i in range(self.rectNum):
                currRectangle = self.rectangles[i]
                currRectangleCoors = self.canvas.coords(currRectangle)
                self.canvas.coords(currRectangle, currRectangleCoors[0], self.canvasHeight - (sampleValues[i] * self.heightIntervals), currRectangleCoors[2], currRectangleCoors[3])

    def drawVisDataChroma(self, currSong, currTime):
        if (currTime >= currSong.songDur):
            return 0
        else:
            currSample = math.ceil(currTime / currSong.sampleDurationSec)
            sampleValues = []
            if (currSample >= currSong.audioVisArray.shape[1]):
                print("OVER TIME")
                return -1

            for i in range(currSong.audioVisArray.shape[0]):
                sampleValues.append(currSong.audioVisArray[i, currSample] * 80)
            for i in range(self.rectNum):
                currRectangle = self.rectangles[i]
                currRectangleCoors = self.canvas.coords(currRectangle)
                self.canvas.coords(currRectangle, currRectangleCoors[0], self.canvasHeight - (sampleValues[i] * self.heightIntervals), currRectangleCoors[2], currRectangleCoors[3])

    def addNoteLabel(self, parent):
        noteFrames = ttk.Frame(parent)
        noteLabels = [ttk.Label(noteFrames, text="C"), ttk.Label(noteFrames, text="C#"), ttk.Label(noteFrames, text="D"), ttk.Label(noteFrames, text="D#")
        , ttk.Label(noteFrames, text="E"), ttk.Label(noteFrames, text="F"), ttk.Label(noteFrames, text="F#"), ttk.Label(noteFrames, text="G"), ttk.Label(noteFrames, text="G#"), ttk.Label(noteFrames, text="A"), ttk.Label(noteFrames, text="A#"), ttk.Label(noteFrames, text="B")]
        for i in range(len(noteLabels)):
            noteLabels[i].grid(column=i, row=1, sticky=(N, W, E, S))
            noteFrames.columnconfigure(i, weight=1)
        noteFrames.grid(column=0, row=1, sticky=(N, W, E, S))

    def addRectangles(self, rectangleNum):
        self.canvasWidth = self.canvas.winfo_width()-1
        self.canvasHeight = self.canvas.winfo_height()-1
        self.widthIntervals = math.floor(self.canvasWidth/rectangleNum)
        self.heightIntervals = math.floor(self.canvasHeight/80)
        self.rectangles = []
        for i in range(rectangleNum):
            self.rectangles.append(self.canvas.create_rectangle(self.widthIntervals*i*2, self.canvasHeight, self.widthIntervals*(i+1)+2, self.canvasHeight, fill="#00ffff"))
        return self.rectangles

    def initUI(self, parent, column, row):
        self.mainFrame = ttk.Frame(parent, style="BackgroundFrame.TFrame")
        
        self.canvas = Canvas(self.mainFrame, bg= "#002635", highlightthickness=0)
        
        #FOR CHROMA:
        self.addRectangles(self.rectNum)
        self.addNoteLabel(self.mainFrame)

        #FOR REGULAR VIS:
        """
        self.canvasWidth = self.canvas.winfo_width()-1
        self.canvasHeight = self.canvas.winfo_height()-1
        self.widthIntervals = math.floor(self.canvasWidth/32)
        self.heightIntervals = math.floor(self.canvasHeight/80)
        self.rectangles = []
        for i in range(32):
            self.rectangles.append(self.canvas.create_rectangle(self.widthIntervals*i+2, self.canvasHeight, self.widthIntervals*(i+1)+2, self.canvasHeight, fill="#00ffff"))
        """
        #END REGULAR VIS
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.columnconfigure(0, weight=1)
        
        self.canvas.bind("<Configure>", lambda event: self.resizeCanvas(event))
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S), padx=1, pady=1)
        self.mainFrame.grid(column=column, row=row, sticky=(N, W, E, S))

def main():
    root = Tk()
    filename = "/Users/gold_spaghetti/Documents/music/oddling/divide/Single - divide.mp3"
    filename2 = "/Users/gold_spaghetti/Downloads/Hybrid Statement.ogg"
    filename3 = "shit.mp3"
    currFile = Path(filename)
    currSong = SingleMusic(filename)
    audioVis = AudioVisualizer()
    startButton = ttk.Button(root, command=lambda:audioVis.startDrawVisData(root, currSong))

    audioVis.initUI(root, 0, 0)
    startButton.grid(column=0, row=1)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.mainloop()

if (__name__ == "__main__"):
    main()