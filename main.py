import os

from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd

root = Tk()
root.title("SVG GERBILFUCKER")
frm = ttk.Frame(root, padding=10)
frm.grid()

# 0 = Leave, don't change
# 1 = Offset X,
# 2 = Offset Y
pathCommandArgCounts = {
    "M": [1,2],
    "m": [0,0],

    "L": [1,2],
    "l": [0,0],
    "H": [1],
    "h": [0],
    "V": [2],
    "v": [0],

    "C": [1,2,1,2,1,2],
    "c": [0,0,0,0,0,0],
    "S": [1,2,1,2],
    "s": [0,0,0,0],

    "Q": [1,2,1,2],
    "q": [0,0,0,0],
    "T": [1,2],
    "t": [0,0],

    "A": [0,0,0,0,0,1,2],
    "a": [0,0,0,0,0,0,0],

    "Z": [],
    "z": []
}

transformX = 0
transformY = 0

class CoordInst:
    startI = 0
    oldPath = []
    newPath = []
    def __init__(self, startI, endI, pathStr):
        self.startI = startI
        self.endI = endI
        pathI = 0
        self.pathIStr = ""
        self.pathCommand = ""
        for c in pathStr:
            if c in pathCommandArgCounts.keys():
                if len(self.pathIStr) > 0:
                    self.addPathIStrToPath(pathI)
                self.pathCommand = c
                self.oldPath.append(c)
                self.newPath.append(c)
                pathI = 0
            else:
                if c == ',':
                    self.addPathIStrToPath(pathI)
                    pathI += 1
                else:
                    self.pathIStr += c

        print(self.oldPath)
        print(self.newPath)

    def addPathIStrToPath(self, pathI):
        self.oldPath.append(self.pathIStr)
        fVal = float(self.pathIStr)
        if pathCommandArgCounts[self.pathCommand][pathI] == 1:
            fVal += transformX
        elif pathCommandArgCounts[self.pathCommand][pathI] == 2:
            fVal += transformY
        self.newPath.append(str(fVal))
        self.pathIStr = ""



def getCoordinates(content):
    global transformX
    global transformY
    translateI = content.find("translate(") + 10
    commaI = content.find(",", translateI)
    transformX = float(content[translateI:commaI])
    endBracketI = content.find(")", commaI)
    transformY = float(content[commaI + 1:endBracketI])

    start = 0
    #while start != -1:
    start = content.find('d="') + 3
    end = content.find('"', start)
    path = content[start:end]
    tCoordInst = CoordInst(start, end, path)

def replaceNoneFills(content):
    content.replace("fill=\"none\"", "fill=\"#000000\" fill-opacity=\"0\" ")

def chooseFiles():
    print("choosefiles")
    files = fd.askopenfiles(mode="r")
    for file in files:
        print(file.name)
        opened = open(file.name, "r")
        content = opened.read()
        print(content)
        getCoordinates(content)


def chooseOutputFolder():
    folder = fd.askdirectory()
    print(folder)

ttk.Label(frm, text="SVG GERBILFUCKER").grid(column=0, row=0)
ttk.Label(frm, text="SVG Manipulator for Pixi.js Use").grid(column=0, row=1)

ttk.Button(frm, text="Choose Files", command=chooseFiles).grid(column=0, row=3)
ttk.Button(frm, text="Set Output Folder", command=chooseOutputFolder).grid(column=1, row=3)

root.mainloop()
