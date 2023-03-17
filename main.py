#Q-Smash is a hamfisted attempt at generating a "best guess" list for Dictionary.com's
#Quordle game.  It's like Wordle, but you have 9 guesses to guess 4 words share the
# letter pool - https://www.merriam-webster.com/games/quordle/#/


import datetime
timestart = datetime.datetime.now()

class qsmash:
    def __init__(self):

        #debug values
        #0 = No debug
        #1 = High level messaging
        #1.5 = Something I'm interested in
        #2 = Max Verbocity
        self.debug = 2
        self.refinedList = []
        if self.debug > 0:
            inputFile = 'TestData.txt'
        else:
            inputFile = 'Data.txt'

        self.masterList = open(inputFile).read().casefold().splitlines()
        self.refinedList = self.masterList.copy()
        self.wordValue = {}
        if self.debug >= 1: print("masterList count = "+str(len(self.masterList)))


#Get us the number of times a letter appears
    def numbers(self):
        theNumbers = ({"a":0})
        for entry in self.masterList:
            for letter in entry:
                if letter not in theNumbers.keys():
                    theNumbers[letter] = 0
                else:
                    theNumbers.update({letter:theNumbers[letter]+1})

        if self.debug >= 2: print(theNumbers)

        self.nOrder = []
        self.lOrder = []

        for l, n in theNumbers.items():
            self.nOrder.append(n)

        self.nOrder.sort()

        for currN in self.nOrder:
            for l, n in theNumbers.items():
                if n == currN:
                    key = l
            self.lOrder.append(key)
            theNumbers.pop(key)

        if self.debug >= 2:
            for n in range(0,len(self.lOrder)):
                print(self.lOrder[n]+" = "+str(self.nOrder[n]))

#Remove Dupes:
#Assuming a duplicate letter is reasonably common (O, N, E, L) and from a strategy standpoint
#represents a missed opportunity to remove another letter from the solution pool remove words containing
#duplicate letters
    def removeDupes(self):
        if self.debug >= 1: print("Pre Process: refinedList count = " + str(len(self.refinedList)))
        for word in self.masterList:
            mash = set()
            for letter in word:
                mash.add(letter)
            if len(word) != len(mash):
                self.refinedList.remove(word)
        if self.debug >= 1: print("Post Process: refinedList count = " + str(len(self.refinedList)))

# Calculate Word Values"
# Word value will be the sum of letters, with the value of each letter being based on the number of times the letter
# appears in the dataset in .numbers()
    def wordList(self):
        theNumbers = ({})
        for n in range(0,len(self.lOrder)):
            theNumbers[self.lOrder[n]] = self.nOrder[n]

        for word in self.refinedList:
            mySum = 0
            for letter in word:
                mySum += theNumbers[letter]
            self.wordValue[word] = mySum

        if self.debug == 2: print(self.wordValue)

        self.wOrder = []
        self.vOrder = []

        for v in self.wordValue.values():
            self.vOrder.append(v)

        self.vOrder.sort()

        for currV in self.vOrder:
            for w,v in self.wordValue.items():
                #if self.debug: print("currV = "+str(currV)+" value = "+str(v))
                if v == currV:
                    key = w
            self.wOrder.append(key)
            self.wordValue.pop(key)

        if self.debug >= 1:
            for n in range(0,len(self.wOrder)):
                print(self.wOrder[n]+" = "+str(self.vOrder[n]))

#Reduce Our list
#Take the highest value word, remove all lesser valued words that contain ANY of the letters present in the target word
    def startSmash(self,word):
        if self.debug >= 1:
            print("Pre Process: refinedList count = " + str(len(self.refinedList)))
            print("Word = "+word)
        for letter in word:
            idx = 0
            while idx != len(self.wOrder):
                if letter in self.wOrder[idx]:
                    self.refinedList.remove(self.wOrder[idx])
                    self.wOrder.pop(idx)
                    self.vOrder.pop(idx)
                else:
                    idx += 1
        if self.debug >= 1: print("Post Process: refinedList count = " + str(len(self.refinedList)))
        for n in range(0,len(self.wOrder)):
            print(self.wOrder[n]+" = "+str(self.vOrder[n]))

mine = qsmash()
mine.numbers()
mine.removeDupes()
mine.wordList()
mine.startSmash('lucky')
mine.startSmash('fight')
mine.startSmash('brown')

print(f'#Time to complete: {datetime.datetime.now() - timestart}')