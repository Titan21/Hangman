from typing import NoReturn,List
import random
import sys
import os

#random.seed(0)


class hangman: 

    wordlist_filename :str 
    numguesses : int
    allowedWrongGuesses : int
    wrongguesses : List[str]
    rightguesses : List[str]
    word : str
    guessdone : bool



    def __init__(self, wordlist_filename :str):
        self.wordlist_filename = wordlist_filename
        self.numguesses = 0
        self.allowedWrongGuesses = 10
        self.wrongguesses  = []
        self.word = ''
        self.word = self.selectword()
        self.rightguesses = [''] * len(self.word)
        self.guessdone = False

    def selectword(self) -> str:
        """Select a single random word from the given wordlist"""
        with open(os.path.join(sys.path[0], self.wordlist_filename)) as file:
        
            wordlist = file.readlines()
            while(len(self.word) < 5):
                return random.choices(wordlist)[0].lower().strip()



    def guess(self, guessed_character : str) -> bool:
        """Evaluates a player's guess

        Args:
            character (str): [Character supplied by player to evaluate]

        Returns:
            bool: [Checks if game is finished]
        """
        self.numguesses += 1

        if guessed_character in self.word:
            for i,character in enumerate(self.word):
                if character == guessed_character:
                    self.rightguesses[i] = guessed_character
        else:
            self.wrongguesses.append(guessed_character)
        return self.checkguessdone()

    def drawword(self):
        """Draws the word visually on screen"""
        for mychar in self.word:
            if(mychar in self.rightguesses):
                print(mychar,end='')
            else:
                print("_",end='')
        print("\n")

    def checkguessdone(self) -> bool:
        """Checks if the correct word has been guessed completely
        """
        for char in self.word:
            if(char not in self.rightguesses):
                return False
        return True

    def resetgame(self) -> NoReturn:
        """Resets the game back to the initial state
        """

        self.numguesses = 0
        self.wrongguesses = []
        self.rightguesses = []
        self.word = ''
        self.word = self.selectword()
        self.guessdone = False

    def display_end_game_score(self) -> NoReturn:
        """Print Game End Results
        """
        if(self.guessdone):
            print(f'Congratulations, You\'ve won!\tYou took {len(self.wrongguesses)} wrong guesses')
        else:
            print("Sorry, you didn't guess it")
            print("The correct word would have been:")
        print(self.word)

    def checkreplay(self) -> bool:
        """Checks if the player wants to play again
        """
        print("Want to play again? Y / N")
        input_value = input("Enter single letter\n")
        if(input_value.lower() == 'y'):
            self.resetgame()
            return True
        else:
            return False

    def is_finished(self) -> bool:
        """Checks if the game is finished

        Returns:
            bool: is the game finished?
        """
        return not (len(self.wrongguesses) <= self.allowedWrongGuesses and not self.guessdone)


if __name__ == "__main__":


        while True:
            game = hangman("wordlist.txt")

            while( not game.is_finished() ):
                os.system('cls||clear')
                game.drawword()
                print(f'Wrong Guesses: {len(game.wrongguesses)} / {game.allowedWrongGuesses}\tWrong: {game.wrongguesses}\t')

                input_value = input("Enter single letter\n")
                if(not input_value.isalpha()):
                    print(f"please enter a single character. You've entered {input_value}")
                    input()
                    continue
                input_value = input_value[0].lower()
                if(input_value in game.rightguesses or input_value in game.wrongguesses):
                    print(f"You've already guessed {input_value}")
                    input()
                    continue
                game.guessdone = game.guess(input_value)
                
            game.display_end_game_score()
            game.is_finished()
            if not game.checkreplay():
                break




