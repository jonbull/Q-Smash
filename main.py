#Q-Smash is a hamfisted attempt at generating a "best guess" list for Merriam Webster's
#Quordle game.  It's like Wordle, but you have 9 guesses to guess 4 words thar share the
#same letter pool - https://www.merriam-webster.com/games/quordle/#/

class qsmash:
    def __init__(self, masterlist, debug):

        if debug > 0:
            self.debug = 0
        else:
            self.debug = debug
        self.solutionSet = set()
        self.refinedList = masterList.copy()
        self.wordValue = {}
        self.letterValues = {}

#build the Letter/Value table
    def calcLetterValue(self):
        for entry in self.refinedList:
            for letter in entry:
                if self.solutionSet.isdisjoint(letter):
                    if letter not in self.letterValues.keys():
                        self.letterValues[letter] = 0
                    else:
                        self.letterValues.update({letter:self.letterValues[letter]+1})

#remove dupes from our refinedList
    def removeDupes(self):
        for word in self.refinedList:
            mash = set()
            for letter in word:
                mash.add(letter)
            if len(word) != len(mash):
                self.refinedList.remove(word)

#build the Word/Value table, remove any 0 value words
    def calcWordValue(self):
        badWords = []
        self.wordValue.clear()
        for word in self.refinedList:
            mySum = 0
            for letter in word:
                if self.solutionSet.isdisjoint(letter):
                    mySum += self.letterValues[letter]
            if mySum > 0:
                self.wordValue[word] = mySum
            else:
                badWords.append(word)
        for thisWord in badWords:
            self.refinedList.remove(thisWord)


#update our solution set
    def updateSolutionSet(self,word):
        for letter in word:
            self.solutionSet.add(letter)

#display the current state of this mess
    def currentState(self):
        print ("Current Word Pool: "+str(len(self.wordValue.keys())))
        print ("Current Solution Set: "+str(self.solutionSet))
        print ("Unique characters in solution set: "+str(len(self.solutionSet)))
        valueOrder = []
        for val in self.wordValue.values():
            if val not in valueOrder:
                valueOrder.append(val)

        valueOrder.sort()
        botMin = 0
        botMax = 5
        topMin = len(valueOrder)-5
        topMax = len(valueOrder)
        print("Top 5, Bottom 5")
        for idx in range(botMin,botMax):
            print(str(valueOrder[idx])+": ",end="")
            for x, y in self.wordValue.items():
                if y == valueOrder[idx]: print(str(x)+" ",end="")
            print()
        print ("...")
        for idx in range(topMin,topMax):
            print(str(valueOrder[idx])+": ",end="")
            for x, y in self.wordValue.items():
                if y == valueOrder[idx]: print(str(x)+" ",end="")
            print()
        print()

debug = 1
if debug > 0:
    inputFile = 'TestData.txt'
else:
    inputFile = 'Data.txt'
masterList = open(inputFile).read().casefold().splitlines()

mine = qsmash(masterList,debug)
mine.removeDupes() #Remove words with duplicate letters
mine.calcLetterValue() #Calculate Letter/Value table
mine.calcWordValue() #Calculate Word/Value table

#solutionset = ["alert","sound","pitch","maybe"] #17/175
#myWordList = ["alert","sound","pitch","maybe"] #16/187
#solutionset = ["arise","count","badly","depth"] #16/209
#myWordList = ["arise","count","badly","depth"] #16/221
#solutionset = ["quick","metal","horse","dying"]  #18/180
#myWordList = ["quick","metal","horse","dying","power"] #20/118


for word in myWordList:
    mine.updateSolutionSet(word)
    mine.calcLetterValue()
    mine.calcWordValue()
mine.currentState()
