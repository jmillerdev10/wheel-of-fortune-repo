from re import I
from pyrsistent import b
from regex import F
from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalstatusloc
from config import winnerstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random
import csv

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""
solved = False

guessedletters = []
guessedvowels = []


# Reads dictionary.txt and stores all words in a list
def readDictionaryFile():
    global dictionary
    with open(dictionaryloc, "r") as file:
        dictionaryRaw = file.read()
        dictionary = list(map(str, dictionaryRaw.split()))
        # getWord() # This needs to be called from within wofRoundSetup(). Delete this line once that is in place
        # print(dictionary)
        
def readTurnTxtFile(playerNum):
    global turntext
    with open(turntextloc, "r") as file:
        turntext = file.read()
    # print(turntext % (players[playerNum]["name"]))
    turnaction = input("\n" + turntext % (players[playerNum]["name"]))
    return turnaction   
    #read in turn intial turn status "message" from file

        
# def readFinalRoundTxtFile():
#     global finalroundtext   
#     #read in turn intial turn status "message" from file

def readRoundStatusTxtFile():
    global roundstatus
    with open(roundstatusloc, "r") as file:
        roundstatus = file.read()
        print(roundstatus % (players[0]["name"], players[0]["roundtotal"], players[1]["name"], players[1]["roundtotal"], players[2]["name"], players[2]["roundtotal"]))

def readFinalStatusTxtFile():
    global finalstatus
    with open(finalstatusloc, "r") as file:
        finalstatus = file.read()
        print(finalstatus % (players[0]["name"], players[0]["gametotal"], players[1]["name"], players[1]["gametotal"], players[2]["name"], players[2]["gametotal"]))

def readWinnerStatusTxtFile(playerNum):
    global winnerstatus
    with open(winnerstatusloc, "r") as file:
        winnerstatus = file.read()
        print(winnerstatus % (players[playerNum]["name"], players[playerNum]["roundtotal"]))

# Open the wheeldata file and read it into the application
def readWheelTxtFile():
    global wheellist
    with open(wheeltextloc, "r") as file:
        wheelRaw = file.read()
        wheellist = list(map(str, wheelRaw.split()))
        # print(wheellist)

# Prompt user for player names, store those names in the players dict
# in the nested dictionaries with the "name" key    
def getPlayerInfo():
    global players
    players[0]["name"] = input("Enter player 1's name: ")
    players[1]["name"] = input("Enter player 2's name: ")
    players[2]["name"] = input("Enter player 3's name: ")
    # print(players)

def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
#     readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
#     readFinalRoundTxtFile() 
    
# Sets the puzzle word for the round, make a blank board to fill in
# as correct guesses are made
def getWord():
    global dictionary
    roundWord = random.choice(dictionary)
    roundUnderscoreWord = []
    # print(roundWord)
    for letter in list(roundWord):
        roundUnderscoreWord.append('_')
    return roundWord, roundUnderscoreWord
    
# Sets the stage for each round
def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    global guessedletters
    global guessedvowels
    guessedletters = []
    guessedvowels = []
    word_and_board = getWord()
    roundWord = word_and_board[0]
    blankWord = word_and_board[1]
    print(roundWord) # Remember to remove this before deploying the game!
    print("\nLet's take a look at the puzzle...")
    print(blankWord)
    playerNumberList = list(players.keys())
    initPlayer = random.choice(playerNumberList)
    # print("initPlayer is: " + str(initPlayer)) # uncomment this to make sure initPlayer was properly assigned
    players[0]["roundtotal"] = 0
    players[1]["roundtotal"] = 0
    players[2]["roundtotal"] = 0

    return initPlayer

def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    global roundstatus
    letter_value = random.choice(wheellist)
    if letter_value == "BANKRUPT":
        print("Sorry! You landed on 'BANKRUPT'")
        players[playerNum]["roundtotal"] = 0
        count = [None, 0]
        stillinTurn = False
    elif letter_value == "LoseTurn":
        print("Sorry! You landed on 'Lose a Turn'")
        count = [None, 0]
        stillinTurn = False
    else:
        letter = input("\nYou landed on $%s. Pick a letter: " % letter_value)
    
        if letter not in guessedletters:
            guessedletters.append(letter)
            count = guessletter(letter, playerNum)
            if count[0]:
                stillinTurn = True
            else: 
                stillinTurn = False
        else:
            print("Oops! That letter has already been guessed.")
            stillinTurn = False  

    if count[1] > 0:
        reward = count[1] * int(letter_value)
        # print(reward)
        players[playerNum]["roundtotal"] = players[playerNum]["roundtotal"] + reward
        # print(players[playerNum])
        print("Reward for this turn was $%s" % (reward))
        readRoundStatusTxtFile()
        # print(roundstatus % (players[0]["name"], players[0]["roundtotal"], players[1]["name"], players[1]["roundtotal"], players[2]["name"], players[2]["roundtotal"]))
    return stillinTurn
    # Get random value for wheellist
    # Check for bankrupcy, and take action.
    # Check for loose turn
    # Get amount from wheel if not loose turn or bankruptcy
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
    # Change player round total if they guess right.     
    


def guessletter(letter, playerNum): 
    global players
    global blankWord

    i = 0
    count = 0
    if letter in roundWord:
        for character in roundWord:
            if letter == character:
                index = i
                blankWord[index] = letter
                count += 1
            i = i + 1
        goodGuess = True
        if count > 1:
            print("\nThere are %i %s's" % (count, letter))

        else: 
            print("\nThere is %i %s" % (count, letter))
    else:
        print("\nSorry. %c is not in the puzzle" % (letter))
        goodGuess = False
    print(blankWord)

    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore 
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    # ensure letter is a consonate.
    
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    vowelguess = input("Enter the vowel: ")
    print(guessedvowels)
    
    if vowelguess in vowels:
        if vowelguess not in guessedvowels:
            guessedvowels.append(vowelguess)
            goodGuess = guessletter(vowelguess, playerNum)
        else:
            print("Oops! That vowel has already been guessed.")
            goodGuess = False
    else:
        print("Oops! %c is not a vowel. Try again" % (vowelguess))
        buyVowel(playerNum)
        
    readRoundStatusTxtFile()
        
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    
    return goodGuess      
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord

    wordguess = input("\nType your word guess and press 'Enter': ")  
    if wordguess == roundWord:
        blankWord = list(wordguess)
    else:
        print("\nSorry. That guess was incorrect.")  

    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish)  
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players
    global solved

    readRoundStatusTxtFile()
    # print(roundstatusloc % (players[0], players[0]["roundtotal"], players[1], players[1]["roundtotal"], players[2], players[2]["roundtotal"]))

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    
    solved = False
    while not solved:
        stillinTurn = True
        while stillinTurn:
            choice = readTurnTxtFile(playerNum)
                        
            if(choice.strip().upper() == "S"):
                stillinTurn = spinWheel(playerNum)
            elif(choice.strip().upper() == "B"):
                if players[playerNum]["roundtotal"] < vowelcost:
                    print("Sorry, you do not have enough money to buy a vowel. You must spin or solve the puzzle")
                    wofTurn(playerNum)
                    # choice = readTurnTxtFile(playerNum)
                else:
                    players[playerNum]["roundtotal"] = players[playerNum]["roundtotal"] - vowelcost
                    stillinTurn = buyVowel(playerNum)
            elif(choice.upper() == "G"):
                stillinTurn = guessWord(playerNum)
            else:
                print("Not a correct option")
        
        if blankWord == list(roundWord):
            print("We have a winner. The word was %s" % (roundWord))
            solved = True
            players[playerNum]["gametotal"] = players[playerNum]["gametotal"] + players[playerNum]["roundtotal"]
            # players[1]["gametotal"] = players[1]["gametotal"] + players[1]["roundtotal"]
            # players[2]["gametotal"] = players[2]["gametotal"] + players[2]["roundtotal"]

            # print(players)


            readFinalStatusTxtFile()
            
        else:
            if playerNum == 0 or playerNum == 1:
                playerNum = playerNum + 1
                wofTurn(playerNum)
            else:
                playerNum = 0
                wofTurn(playerNum)
        

    
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()

    wofTurn(initPlayer)
    
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.

# def wofFinalRound():
#     global roundWord
#     global blankWord
#     global finalroundtext
#     winplayer = 0
#     amount = 0
    
#     # Find highest gametotal player.  They are playing.
#     # Print out instructions for that player and who the player is.
#     # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
#     # Use the guessletter function to check for {'R','S','T','L','N','E'}
#     # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
#     # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
#     # Print out the current blankWord again
#     # Remember guessletter should fill in the letters with the positions in blankWord
#     # Get user to guess word
#     # If they do, add finalprize and gametotal and print out that the player won 


def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            print("Time to play Round %s!" % (i+1))
            wofRound()
        else:
            readFinalStatusTxtFile()
            finalscores = []
            templeader = ['', 0]
            for player in players:
                finalscores.append([players[player]["name"], players[player]["gametotal"]])
            for score in finalscores:
                if score[1] > templeader[1]:
                    templeader = score
            print("\n" + templeader[0] + " will be moving on to the Final Round!")
            print("\nFinal Round Under Construction!")
    #         wofFinalRound()

if __name__ == "__main__":
    main()
    
    
