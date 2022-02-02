from math import inf
import os
import sys
import random
import logging
import string
from typing import NoReturn,List

#logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class hangman_solver:



    wordlist : List[str] = []
    candidates : List[str] = []

    wrongguesses : List[str] = []
    rightguesses : List[str] = []
    remainingGuesses : List[str] = []

    wordLength : int

    letterFrequency : List[str] = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','z','q']


    def __init__(self, wordlist_filename:str) -> NoReturn:
        self.loadWordList(wordlist_filename)
        self.wordLength = 0
        assert len(self.wordlist) > 0
        self.initializeRemainingGuesses()
        assert len(self.remainingGuesses) > 0


    def loadWordList(self, filename:str) -> NoReturn:
        """Loads the given wordlist"""
        with open(os.path.join(sys.path[0], filename)) as file:
        
            templist = file.readlines()
            for word in templist:
                self.wordlist.append(word.lower().strip())
            self.wordlist.sort(key=lambda x: len(x))

    def initializeRemainingGuesses(self) -> NoReturn:
        for char in string.ascii_lowercase:
            self.remainingGuesses.append(char)
    
    def initializeCandidates(self, wordLength:int) -> NoReturn:
        self.wordLength = wordLength

    def updateCandidates(self,lettersNotIncluded : List[str], lettersIncluded : List[str]) -> NoReturn:
        if(len(self.candidates) == 0):
                self.calculateCandidates()
        self.updateGuesses(lettersNotIncluded,lettersIncluded)
        self.calculateCandidates()

    def calculateCandidates(self) -> NoReturn:

        containsLettersNotIncluded : bool = False
        containsLettersNotMatching : bool = True

        newcandidates : List[str] = []

        if len(self.candidates) == 0 :
            for word in self.wordlist:
                if len(word) == self.wordLength :
                    newcandidates.append(word)
        else:
            for word in self.candidates:
                containsLettersNotIncluded = False
                containsLettersNotMatching = False
                for i,char in enumerate(word):
                    if(char in self.wrongguesses):
                        containsLettersNotIncluded = True
                        break
                    if(self.rightguesses[i].isalpha() and self.rightguesses[i] != char):
                        containsLettersNotMatching = True
                        break
                if(not containsLettersNotMatching and not containsLettersNotIncluded):
                    newcandidates.append(word)
                    logging.debug(f'added {word} to newcandidates')
        self.candidates = newcandidates.copy()


    def calculatedRemainingCandidates(self, letter:str) -> int:

        candidateCount : int = len(self.candidates)

        for word in self.candidates:
            if letter in word:
                candidateCount -= 1
        return candidateCount



    def findBestGuess(self) -> str:
        assert len(self.candidates) > 0

        bestletter = []
        score = len(self.candidates)

        for letter in self.remainingGuesses:
            remainingCandidatesCount = self.calculatedRemainingCandidates(letter)
            if remainingCandidatesCount <= score :
                if remainingCandidatesCount < score:
                    bestletter = []
                bestletter.append(letter)
                score = remainingCandidatesCount
            logging.debug(f'Remaining Candidates with letter {letter} : {remainingCandidatesCount}')
        return (bestletter[0],score)

    def updateGuesses(self, lettersNotIncluded : List[str], lettersIncluded : List[str]) -> NoReturn:
        # assert self.wordLength == len(lettersIncluded)

        self.wrongguesses = lettersNotIncluded.copy()
        self.rightguesses = lettersIncluded.copy()

        for letter in self.remainingGuesses.copy():
            if(letter in self.wrongguesses or letter in self.rightguesses):
                self.remainingGuesses.remove(letter)


    def interactiveSolve(self):

        while True:
            if self.wordLength == 0:
                wordInput = input("Enter Word Length\n")
                if wordInput.isnumeric:
                    self.wordLength = int(wordInput)
                else:
                    print(f'Please enter the length of the word')
                continue

            rightLetterInput = input("Enter the known word, using _ for unknown letters\n")
            self.rightguesses = []
            for letter in rightLetterInput:
                self.rightguesses += letter

            wrongLetterInput = input("Enter a wrong letter\n")
            self.wrongguesses += wrongLetterInput

            
            self.updateCandidates(self.wrongguesses,self.rightguesses)
            bestGuess,score = self.findBestGuess()
            if score == 1:
                print(f"I've found the Answer: {self.candidates}")
            print(f'Hmm, My next guess would be {bestGuess}.\nWith that letter, there will be {score} words left')        
        pass

if (__name__ == '__main__'):
    guesser = hangman_solver("wordlist.txt")

    guesser.interactiveSolve()

    guesser.wordLength = 6

    guesser.updateCandidates([],['','','','','',''])


    best = guesser.findBestGuess()
    print(f'{best}')
