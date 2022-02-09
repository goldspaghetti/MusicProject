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
    def __init__(self, filename, musicSelector):
        #filename is pathlib obj #not anymore 8^(
        #self.extension = filename.suffix
        self.musicSelector = musicSelector
        self.jsonDic = musicSelector.jsonData

        self.musicName = os.path.basename(filename)
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
        self.hop_length = 0
        self.sampleDurationSec = 0
        self.audioVisArray = []
        self.chromaData = []
        #self.initAudioVisData(filename)
        self.loadAudioData()

        self.mainFrame = None


        print("sampleDurationSec: " + str(self.sampleDurationSec))
        print("sample length: " + str(len(self.audioData)))
        print("chroma length: " + str(self.chromaData.shape))
        #print("sample num: " + )

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
        """
        n_fft= 2048
        hop_length = n_fft//4
        self.hop_length = hop_length
        y, sr = librosa.load(filename, sr=44100)
        #hop_length = n_fft//4
        #hop_length = 100
        #self.hop_length = hop_length
        
        M = librosa.feature.melspectrogram(y=y, sr=sr)
        M_db = librosa.power_to_db(M, ref=np.max)
        reshapedMdb = M_db.reshape(32, 4, M_db.shape[1])
        self.audioVisArray = np.mean(reshapedMdb, axis=1)
        
        self.songDur = librosa.get_duration(y, sr=sr, n_fft=n_fft)

        self.sampleDurationSec = (self.songDur/M_db.shape[1])
        """
        #hop Length test along with only chroma
        n_fft= 2048
        hop_length = n_fft//4
        self.hop_length = hop_length
        y, sr = librosa.load(filename, sr=44100)
        

        #M = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length)
        #M_db = librosa.power_to_db(M, ref=np.max)
        #reshapedMdb = M_db.reshape(32, 4, M_db.shape[1])
        #self.audioVisArray = np.mean(reshapedMdb, axis=1)
        self.chromaData = librosa.feature.chroma_stft(y, sr=sr, hop_length=hop_length)
        #reduce accuracy, why not
        newChromaData = np.empty(self.chromaData.shape, dtype=np.int8)
        for i in range(self.chromaData.shape[0]):
            for j in range(self.chromaData.shape[1]):
                newChromaData[i][j] = round(self.chromaData[i][j]* 100, 0)

        self.chromaData = newChromaData

        self.songDur = librosa.get_duration(y, sr=sr, n_fft=n_fft, hop_length=hop_length)
        
        
        self.sampleDurationSec = (self.songDur/self.chromaData.shape[1])




        print("song dur: " + str(self.songDur))
        #getting chroma data
        #yHarmonic, yPercussive = librosa.effects.hpss(y)
        #difference between cqt and stft chroma?
        #self.chromaData = librosa.feature.chroma_cqt(y, sr=sr)
        #self.chromaData = librosa.feature.chroma_stft(y, sr=sr)

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
        #currMusicDic["audioVisArray"] = self.audioVisArray.tolist()
        currMusicDic["chromaData"] = self.chromaData.tolist()
        self.musicSelector.addToJson(self.filename, currMusicDic)

    def loadAudioData(self):
        dir = "MusicAudioData.json"
        if (self.filename in self.jsonDic.keys()):
            #INIT HERE
            currMusicDic = self.jsonDic[self.filename]
            self.songDur = currMusicDic["songDur"]
            self.sampleDurationSec = currMusicDic["sampleDurationSec"]
            #self.audioVisArray = np.asarray(currMusicDic["audioVisArray"])
            self.chromaData = np.asarray(currMusicDic["chromaData"], dtype=np.int8)
            print("chroma type: " + str(type(self.chromaData)))
            #print(audioVis)
        else:
            self.initAudioVisData(self.filename)
            self.saveAudioData()

    def initUI(self, parent, column, row):
        self.mainFrame = ttk.Frame(parent)
