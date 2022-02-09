from tkinter import *
from tkinter import ttk

from MusicController import MusicController
from SingleMusic import SingleMusic
from AudioVisualizer import AudioVisualizer
from MusicQueue import MusicQueue
import os, json

class Albumn:
    #music albumn
    def __init__(self, baseDir, musicFiles, musicController, musicSelector):
        self.musicController = musicController
        self.mainFrame = None
        self.baseDir = baseDir
        self.singleMusics = []
        for singleMusic in musicFiles:
            self.singleMusics.append(SingleMusic(os.path.join(baseDir, singleMusic), musicSelector))

    def initUI(self, parent, column, row):
        self.mainFrame = ttk.Frame(parent, style="TFrame")
        titleLabel = ttk.Label(self.mainFrame, text=self.baseDir)
        songNumLabel = ttk.Label(self.mainFrame, text="songNum")
        artistLabel = ttk.Label(self.mainFrame, text="artist")
        addToPlaylistButton = ttk.Button(self.mainFrame, text="addToPlaylist", command=lambda:self.musicController.addToPlaylist(self.singleMusics))
        #placeholder for img
        albumnImg = ttk.Label(self.mainFrame, text="img")

        addToPlaylistButton.grid(column=0, row=0, rowspan=2, sticky= (N, W, E, S))
        albumnImg.grid(column=1, row=0, rowspan=2, sticky=(N, W, E, S))
        titleLabel.grid(column=2, row=0, columnspan=2, sticky=(N, W, E, S))
        songNumLabel.grid(column=3, row=1, sticky=(N, W, E, S))
        artistLabel.grid(column=2, row=1, sticky=(N, W, E, S))

        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.grid(column=column, row=row, sticky=(N, W, E, S))
    

class App():
    def __init__(self):
        self.mainFrame = None

    def initUI(self, root):
        self.mainFrame = ttk.Frame(root)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))

class MusicSelector():
    def __init__(self, musicController):
        self.musicController = musicController
        self.frameContainer = None
        self.currPlaylistFrame = None
        self.songSelectFrame = None
        self.currPlaylistCanvas = None
        self.songSelectCanvas = None
        self.jsonData = None
        self.albumns = []
        #for now, dummy albums
        #for i in range(90):
        #    currAlbumn = Albumn()
        #    self.albumns.append(currAlbumn)
        self.initAlbumns()
    
    def onConfigure(self, canvas):
        #print("wot")
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resizeInsideCanvas(self, event, canvas):
        print("wot")
        print(event.width)
        #print(self.songSelectFrame.config())
        canvas.itemconfigure("insideFrame", width=event.width)
        self.songSelectFrame.configure(width=event.width)
        #self.onConfigure(canvas)
        #for albumn in self.albumns:
        #    albumn.mainFrame.configure(width=event.width)
        #self.songSelectCanvas.itemconfigure("insideFrame", width=event.width)

    def initAlbumns(self):
        baseDir = "/Users/gold_spaghetti/Documents/music/boss-battle-records/hacknet"
        #baseDir = "/Users/gold_spaghetti/Documents/music/oddling/divide"
        #baseDir = "/Users/gold_spaghetti/Documents/music/system96"
        #baseDir = "/Users/gold_spaghetti/Documents/UnityShite/PEPSIMAN/Assets/Sound/"
        #baseDir = "/Users/gold_spaghetti/Documents/UnityShite/RhythmShite/Assets/audio"
        self.getCurrJson()
        for root, subfolders, filenames in os.walk(baseDir):
            musicFiles = []
            for subfolder in subfolders:
                print("SUBFOLDER OF: " + root + " : " + subfolder)
            for filename in filenames:
                if (os.path.splitext(filename)[1] == (".mp3" or ".ogg" or ".wav" or".m4a")):
                    musicFiles.append(filename)
                print("file inside: " + root + " : " + filename)
            if len(musicFiles) > 0:
                currAlbumn = Albumn(root, musicFiles, self.musicController, self)
                self.albumns.append(currAlbumn)
        self.saveAudioFile()
        self.jsonData = None
        

    #SHOULD THIS BE UNDER HERE?
    def getCurrJson(self):
        currFile = open("./MusicAudioData.json")
        self.jsonData = json.load(currFile)
        currFile.close()

    def saveAudioFile(self):
        #DO THIS AT END OR JUST ADD A BUTTON I GUESS
        currFile = open("./MusicAudioData.json", "w")
        json.dump(self.jsonData, currFile)
        currFile.close()
        pass

    def addToJson(self, filename, newDic):
        self.jsonData[filename] = newDic


    def updateAllJson(self):

        pass

    def initUI(self, parentFrame):
        #self.frameContainer=ttk.Frame(parentFrame, style="BackgroundFrame.TFrame")
        self.mainFrame = ttk.Frame(parentFrame, padding="5 0 5 0")
        self.currPlaylistLabel = ttk.Label(text="Current Playlist", style="TLabel")
        self.songSelectLabel = ttk.Label(text="Song Selection", style="TLabel")
        self.currPlaylistBackgroundFrame = ttk.LabelFrame(self.mainFrame, style="BackgroundLabelframe.TLabelframe", labelwidget=self.currPlaylistLabel)
        self.songSelectBackgroundFrame = ttk.Labelframe(self.mainFrame, style="BackgroundLabelframe.TLabelframe", labelwidget=self.songSelectLabel)
        self.currPlaylistCanvas = Canvas(self.currPlaylistBackgroundFrame, bg="#002635", borderwidth=0, highlightcolor="#c694ff", highlightthickness=0)
        self.songSelectCanvas = Canvas(self.songSelectBackgroundFrame, bg="#002635", borderwidth=0, highlightcolor="#c694ff", highlightthickness=0)

        #self.currPlaylistFrame = ttk.LabelFrame(self.currPlaylistCanvas, borderwidth=5, relief="sunken", text="Current Playlist", style="TLabelframe")
        #self.songSelectFrame = ttk.LabelFrame(self.songSelectCanvas, borderwidth=5, relief="sunken", text="Albumns", style="TLabelframe")
        self.currPlaylistFrame = ttk.Frame(self.currPlaylistCanvas, style="TFrame")
        self.songSelectFrame = ttk.Frame(self.songSelectCanvas, style="TFrame")

        #self.songSelectFrame.columnconfigure(0, weight=1)

        playlistScrollbar = ttk.Scrollbar(self.currPlaylistBackgroundFrame, orient=VERTICAL, command=self.currPlaylistCanvas.yview, style="Vertical.TScrollbar")
        songSelectScrollbar = ttk.Scrollbar(self.songSelectBackgroundFrame, orient=VERTICAL, command=self.songSelectCanvas.yview, style="Vertical.TScrollbar")

        self.songSelectCanvas.configure(yscrollcommand=songSelectScrollbar.set, scrollregion=self.songSelectCanvas.bbox("all"))
        self.currPlaylistCanvas.configure(yscrollcommand=playlistScrollbar.set, scrollregion=self.currPlaylistCanvas.bbox("all"))

        self.currPlaylistCanvas.create_window((0, 0), window=self.currPlaylistFrame, anchor=NW,tags=("insideFrame",))
        self.songSelectCanvas.create_window((0, 0), window=self.songSelectFrame, anchor=NW, tags=("insideFrame"))

        self.songSelectFrame.bind("<Configure>", lambda event: self.onConfigure(self.songSelectCanvas))
        self.currPlaylistFrame.bind("<Configure>", lambda event: self.onConfigure(self.currPlaylistCanvas))
        self.currPlaylistCanvas.bind("<Configure>", lambda event: self.resizeInsideCanvas(event, self.currPlaylistCanvas))
        self.songSelectCanvas.bind("<Configure>", lambda event: self.resizeInsideCanvas(event, self.songSelectCanvas))

        print(len(self.albumns))
        for i in range(len(self.albumns)):
            currAlbumn = self.albumns[i]
            currAlbumn.initUI(self.songSelectFrame, row=i, column=0)

        self.currPlaylistCanvas.grid(column=0, row=0, sticky=(N, W, E, S))
        self.songSelectCanvas.grid(column=0, row=0, sticky=(N, W, E, S))

        playlistScrollbar.grid(column=1, row=0, sticky=(N, W, E, S))
        songSelectScrollbar.grid(column=1, row=0, sticky=(N, W, E, S))

        self.currPlaylistBackgroundFrame.rowconfigure(0, weight=1)
        self.currPlaylistBackgroundFrame.columnconfigure(0, weight=1)
        self.songSelectBackgroundFrame.rowconfigure(0, weight=1)
        self.songSelectBackgroundFrame.columnconfigure(0, weight=1)

        self.currPlaylistBackgroundFrame.grid(column=0, row=1, sticky=(N, W, E, S))
        self.songSelectBackgroundFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainFrame.columnconfigure(0, weight=1)
        #self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.grid(column=0, row=0, rowspan=2, sticky=(N, W, E, S))
        """
        self.frameContainer.rowconfigure(0, weight=1)
        self.frameContainer.rowconfigure(1, weight=1)
        self.frameContainer.columnconfigure(0, weight=1)
        self.frameContainer.grid(column=0, rowspan=2, sticky=(N, W, E, S))
        """

def main():
    root = Tk()
    
    #style stuff

    #s.configure("defaultFrame.TFrame", bg="#212121", highlightcolor="#34b0d2")
    #s.configure("TLabelFrame", bg="#212121", highlightcolor="#002635", highlightbackground="#212121", highlightthickness=5,foreground="#34b0d2")
    #s.configure('TButton', foreground='#34b0d2')

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = App()
    app.initUI(root)
    audioVisualizer = AudioVisualizer()
    musicQueue = MusicQueue()
    musicController = MusicController(audioVisualizer, root, musicQueue)
    musicSelector = MusicSelector(musicController)

    musicSelector.initUI(app.mainFrame)
    musicQueue.initUI(musicSelector.currPlaylistFrame)
    audioVisualizer.initUI(app.mainFrame, column=1, row=0)
    musicController.initUI(app.mainFrame, column=1, row=1)
    #app.initUI(root)

    s=ttk.Style()
    
    s.theme_create("styleTest", parent="clam",
        settings={
            "TLabelframe":{
                "configure":{
                    "background":"#212121",
                    #"foreground":"#e6e6dc"
                    #"releif":"solid",
                    #"bordercolor":"#e6e6dc"
                }
            },
            "TLabelframe.Label":{
                "configure":{
                    "background":"#e6e6dc"
                }
            },
            "TButton":{
                "configure":{
                    "background":"#212121",
                    "foreground":"#00cccc"
                }
            },
            "TFrame":{
                "configure":{
                    "background":"#002635",
                    "borderwidth":0,
                    "highlightthickness":0
                    #"releif":None

                }
            },
            "MusicSelectionFrame.TFrame":{
                "configure":{
                    "background":"#002635",
                    "relief":"solid",
                    "bordercolor":"#00cccc",
                    "borderwidth":2
                }
            },
            "BackgroundFrame.TFrame":{
                "configure":{
                    "background":"#002635"
                }
            },
            "BackgroundLabelframe.TLabelframe":{
                "configure":{
                    "background":"#002635",
                    "relief":"solid",
                    "bordercolor":"#00cccc",
                    "borderwidth":5,
                    "padding":"2 2 2 2"
                }
            },
            "TLabel":{
                "configure":{
                    "background":"#002635",
                    "foreground":"#00cccc"
                }
            },
            "Vertical.TScrollbar":{
                "configure":{
                    "bordercolor":"#7eb2dd",
                    "background":"#002635",
                }
            }
        }
    )

    
    
    s.theme_use("styleTest")
    s.configure("BackgroundLabelframe.TLabelframe", bordercolor="#00cccc")
    """
    #s.configure("TLabelframe", background="#212121",releif="solid",bordercolor="#e6e6dc", borderwidth=2, foreground="#e6e6dc")
    s.configure("TLabelframe", background="#212121", highlightcolor="#00cccc", highlightthickness=2)
    s.configure("Tframe", background="#212121")
    #s.configure("TLabelframe.Label", background="#212121",foreground="#00cccc")
    s.configure("TButton",background="#212121",foreground="#e6e6dc",)
    #s.configure("TFrame", background="#212121",foreground="#e6e6dc")

    """
    print(s.theme_use())

    root.mainloop()
    pass

if (__name__ == "__main__"):
    main()