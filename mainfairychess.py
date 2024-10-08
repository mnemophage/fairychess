import random
import copy
from PIL import Image
import requests
from io import BytesIO

url = 'https://github.com/mnemophage/fairychess/blob/7da4c5f3d625df9e8a1c265153151528f5508727/chessboard.png'
# i need copy so i can copy the piece rules from the piece index and use it to change the rule a bit and then copy it into
# into the board place where it is supposed to go.

# an object of class Npiece has six non self perameters. firDir and secDir tell you where it 
# moves in one move- 1,1 is diagonal, 0,1 is orthagonal.Royal is if its royal (when it dies u lose)
# choice is if you can choose between directions- a 1,1 with choice can choose diagonal/orthagonal
# leaps is if it leaps over other pieces, and rider is if it makes the same move multiple times
# in one direction per turn.
# isWhite is True by default and the code uses it to decide if it is an enemy piece
class Npiece:
    def __init__(self, firDir, secDir, Rider, isWhite, name):
        self.o = firDir
        self.d = secDir
        self.ri = Rider
        self.w = isWhite
        self.n = name
# these ints and bools are explained down above the pieces
# npiece stands for normal piece.

class Cpiece:
    def __init__(self, pieceOne, pieceTwo, Royal, isWhite, name):
        self.o = pieceOne
        self.t = pieceTwo
        self.r = Royal
        self.w = isWhite
        self.n = name
# Cpiece is combined piece

class Wpiece: 
    def __init__(self, name, isWhite, Leaps):
        self.n = name
        self.w = isWhite

# make a new class of real pieces on the board. make their square x and y 2 of the attributes.
        

# riderChance probably wont work yet cuz i havent tested lol
def riderChance(piece):
    i = random(1,3)
    if piece == "Ferz" and i == 3:
        piece.ri = True
        piece = "Bishop"
    elif piece == "Wazir" and i == 3:
        piece.ri = True
        piece == "Rook"
    elif piece == "Mann" and i == 3:
        piece.ri = True
        piece = "Queen"
    elif i == 3:
        piece.ri = True
        piece = piece + "rider"

# board goes column 0-7
bh, bw = 8, 8
board = [["Empty" for x in range(bh)] for y in range(bw)]
# call example: board[5][7]

Wazir = Npiece(0,1,False,True,"Wazir")
Ferz = Npiece(1,1,False,True,"Ferz")
Dababba = Npiece(2,0,False,True,"Dababba")
Knight = Npiece(2,1,False,True,"Knight")
Zebra = Npiece(2,3,False,True,"Zebra")
#Mann = Npiece(1,1,False,True,False,False,True,"Mann")
#King = Npiece(1,1,True,True,False,False,True,"King")
Camel = Npiece(3,1,False,True,"Camel")
Threeleaper = Npiece(3,0,False,True,"Threeleaper")
Fourleaper = Npiece(4,0,False,True,"Fourleaper")
Giraffe = Npiece(4,1,False,True,"Giraffe")
Stag = Npiece(4,2,False,True,"Stag")
Commuter = Npiece(4,4,False,True,"Commuter")
Antelope = Npiece(4,3,False,True,"Antelope")
Alfil = Npiece(2,2,False,True,"Alfil")
Tripper = Npiece(3,3,False,True,"Tripper")
# these are the simple (normal) pieces. they move in one move, once per turn.

# named riders
Rook = Npiece(0,1,True,True,"Rook")
Bishop = Npiece(1,1,True,True,"Bishop")
Nightrider = Npiece(2,1,True,True,"Nightrider")
# and the combined pieces
Dragonking = Cpiece(Rook, Ferz, True,True,"Dragonking")
Alibaba = Cpiece(Dababba, Alfil, False,True, "Alibaba")
Mann = Cpiece(Ferz,Wazir,False,True,"Mann")
King = Cpiece(Ferz,Wazir,True,True,"King")
Queen = Cpiece(Rook, Bishop, False,True,"Queen")
Cardinal = Cpiece(Bishop, Knight, False,True,"Cardinal")
Jack = Cpiece(Alibaba, Knight, False,True,"Jack")
Chancellor = Cpiece(Rook, Knight, False,True,"Chancellor")
Gnu = Cpiece(Knight,Camel,False,True,"Gnu")
Fortress = Cpiece(Ferz,Dababba, False, True, "Fortress")
Canvasser = Cpiece(Camel,Rook,False,True,"Canvasser")
Champion = Cpiece(Mann,Dababba,False,True,"Champion")
Camelzebra = Cpiece(Camel, Zebra, False, True, "Camelzebra")
Threetripper = Cpiece(Tripper, Threeleaper, False, True, "Threetripper")
Titan = Cpiece(Threetripper, Camelzebra, False, True, "Titan")
Meatball = Cpiece(Mann, Jack, False, True, "Meatball")
Marquis = Cpiece (Knight, Wazir, False, True, "Marquis")
Dragonhorse = Cpiece(Bishop,Wazir,False,True,"Dragon Horse")
Amazon = Cpiece(Queen,Knight,False,True,"Amazon")
Buffalo = Cpiece(Camelzebra, Knight,False,True,"Buffalo")
Elephant = Cpiece(Mann, Alfil, False, True, "Elephant")
Maharajah = Cpiece(Queen,Knight,True,True,"Maharajah")
Mounted_King = Cpiece(Knight,Mann,True,True,"Mounted King")
Centaur = Cpiece(Knight,Mann,False,True,"Centaur")
Sabertooth = Cpiece(Titan,Jack,False,True,"Sabertooth" )
# normal piece index- mostly jumpers and a few named riders
NpieceIndex = [Wazir, Ferz, Dababba, Threeleaper, Stag, Giraffe,
Fourleaper, Alfil, Antelope, Commuter, Tripper, Mann, Camel, Knight, Rook, Bishop,] 
CpieceIndex = [Jack, Alibaba, Cardinal, Chancellor, Gnu, Titan, Fortress, 
Canvasser, Champion,Titan,Marquis,Dragonhorse, Elephant,Centaur, Sabertooth ] #Grasshopper, Pawn, Manticore, Zebra, 
#Immobilizer, Jester, Gryphon, Checker-Man, Checker-King]
PowerIndex = [Meatball, Queen, Amazon,Buffalo,Sabertooth,]


RoyalIndex = [Dragonking, King, Maharajah,Mounted_King]

nIndexLength = len(NpieceIndex)
cIndexLength = len(CpieceIndex)
rIndexLength = len(RoyalIndex)
totalLength = cIndexLength + nIndexLength
# starts the game. 
rand = 0
# defines rand

def startup():
    for i in range(0,2):
        for g in range (0,8): # 16 cells- each a random piece
            rand = random.randrange(0,totalLength,1)
            if rand > nIndexLength:
                rand = rand - nIndexLength -1    # so it is in range 
                comPiece = copy.deepcopy(CpieceIndex[rand])
                comPiece.w = True
                board[i][g] = copy.deepcopy(comPiece)
            else:
                rand = rand - 1       # so it is in range
                normPiece = copy.deepcopy(NpieceIndex[rand])
                normPiece.w = True
                board[i][g] = copy.deepcopy(normPiece)
    for i in range(6,8):
        for g in range (0,8):
            rand = random.randrange(0,totalLength,1)
            if rand > nIndexLength-1:
                rand = rand - nIndexLength     # so it is in range 
                comPiece = copy.deepcopy(CpieceIndex[rand])
                comPiece.w = False # these are the black pieces
                board[i][g] = copy.deepcopy(comPiece) # needed to copy it twice so i could change the attributes
            else:
                rand = rand        # so it is in range
                normPiece = copy.deepcopy(NpieceIndex[rand])
                normPiece.w = False
                board[i][g] = copy.deepcopy(normPiece)
                



startup()
# this bit makes the kings and puts them in their places. 
rand = random.randrange(0,rIndexLength,1)
bk = copy.deepcopy(RoyalIndex[rand])
bk.w = False
board[0][4] = copy.deepcopy(bk)
wk = copy.deepcopy(bk)
wk.w = True
board[7][4] = copy.deepcopy(wk)

# prints the board
for i in range (0,2):
    for g in range(0,8):
        print ("("+str(i)+","+str(g)+")")
        print(board[i][g].n)
for i in range (6,8):
    for g in range(0,8):
        print ("("+str(i)+","+str(g)+")")
        print(board[i][g].n)


response = requests.get(url)
img = Image.open(BytesIO(response.content))


img.show()
