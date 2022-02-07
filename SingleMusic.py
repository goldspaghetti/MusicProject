import librosa
from tkinter import *
from tkinter import ttk
import numpy as np
import pathlib
from pathlib import Path
from pydub import AudioSegment
import os
import math
import json

class SingleMusic:
    def __init__(self, filename):
        #filename is pathlib obj #not anymore 8^(
        #self.extension = filename.suffix


        self.filename = filename
        self.extension = os.path.splitext(filename)[1]
        self.originalAudioSegment = AudioSegment.from_file(filename, extension=self.extension[1:])
        #adjusted for volume
        self.audioSegment = self.originalAudioSegment - 0
        
        #convert audioSegment into an array of [2][sampleNum]
        self.audioData = self.audioSegment.get_array_of_samples()
        self.numChannels = 2
        self.bytesPerSample = 2
        self.sampleRate = 44100

        #inits from initAudioVisData
        self.songDur = 0
        self.sampleDurationSec = 0
        self.audioVisData = []
        self.chromaData = []
        self.initAudioVisData(filename)
        
        self.mainFrame = None

        print("sampleDurationSec: " + str(self.sampleDurationSec))
        print("sample length: " + str(len(self.audioData)))

    def getSegmentFromLocation(self, startTime):
        #assuming frequency of 44100
        print("startTime: " + str(startTime))
        currSample = math.floor(startTime*self.sampleRate*2)
        if (currSample %2 != 0):
            currSample += 1
        print("currSample: " + str(currSample))
        print("curr duration: " + str(currSample*self.sampleDurationSec))
        return self.audioData[currSample:], (currSample/self.sampleRate/2)

    def updateVolume(self, volume):
        self.audioSegment = self.originalAudioSegment + volume
        #update raw data
        self.audioData = self.audioSegment.get_array_of_samples()

    def initAudioVisData(self, filename):
        n_fft= 2048
        y, sr = librosa.load(filename, sr=44100)
        hop_length = n_fft//4
        M = librosa.feature.melspectrogram(y=y, sr=sr)
        M_db = librosa.power_to_db(M, ref=np.max)
        reshapedMdb = M_db.reshape(32, 4, M_db.shape[1])
        self.audioVisArray = np.mean(reshapedMdb, axis=1)
        self.songDur = librosa.get_duration(y, sr=sr, n_fft=n_fft, hop_length = hop_length)
        self.sampleDurationSec = (self.songDur/M_db.shape[1])

        #getting chroma data
        #yHarmonic, yPercussive = librosa.effects.hpss(y)
        #difference between cqt and stft chroma?
        #self.chromaData = librosa.feature.chroma_cqt(y, sr=sr)
        self.chromaData = librosa.feature.chroma_stft(y, sr=sr)

        #testing if length is the same
        """
        print("----")
        print(self.chromaData.shape)
        print(self.audioVisArray.shape)

        print(self.chromaData.shape[1])
        print(self.audioVisArray.shape[1])
        print("---")
        """
        #maybe add params for other effects down the line
    
    def saveAudioData(self):
        dir = "./MusicAudioData.json"
        currMusicDic = {}
        currMusicDic["songDur"] = self.songDur
        currMusicDic["sampleDurationSec"] = self.sampleDurationSec
        currMusicDic["audioVisData"] = self.audioVisData
        currMusicDic["chromaData"] = self.chromaData
        return self.filename, currMusicDic

    def loadAudioData(self, jsonDic):
        dir = "MusicAudioData.json"
        if (self.filename in jsonDic.keys()):
            #INIT HERE
            currMusicDic = jsonDic[self.filename]
            self.songDur = currMusicDic["songDur"]
            self.sampleDurationSec = currMusicDic["sampleDurationSec"]
            self.audioVisData = currMusicDic["audioVisData"]
            self.chromaData = currMusicDic["chromaData"]
        else:
            self.initAudioVisData(self.filename)
            self.saveAudioData

    def initUI(self, parent, column, row):
        self.mainFrame = ttk.Frame(parent)
