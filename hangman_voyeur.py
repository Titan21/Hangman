import hangman
import hangman_solver

game = hangman.hangman('wordlist.txt')
solver = hangman_solver.hangman_solver('wordlist.txt')
wordlength = len(game.word)
solver.wordLength = wordlength



while True:

    solver.updateCandidates(game.wrongguesses,game.rightguesses)
    bestguess = solver.findBestGuess()

    guessdone = game.guess(bestguess[0])

    if guessdone:
        print(f"Guessed correctly!\t{game.word}\nGuesses: {game.numguesses}\n\tWrong:{game.wrongguesses}")
        input("")
        game = hangman.hangman('wordlist.txt')
        solver = hangman_solver.hangman_solver('wordlist.txt')
        solver.wordLength = len(game.word)


hangman.demo()

print(f'yeah')