from HangmanML import Hangman
from HangmanML import Hangman_Learner
from HangmanML import MongoDB_Access as mongo

##GLOBALS##

IS_GAME_RUNNING = True
ROUNDS = 1
RUNS = 0
WORD_LIST = mongo.get_dictionary_words()
games_played = 0

while RUNS < 10000:
    IS_GAME_RUNNING = True
    ROUNDS = 1
    hangman = Hangman.Hangman(WORD_LIST)
    learner = Hangman_Learner.Hangman_Learner()

    while IS_GAME_RUNNING:
        print("---------------")
        print("HANGMAN OUTPUT")
        print("ROUND " + str(ROUNDS))
        print("*for testing purposes... WORD: " + hangman.word)
        print("REMAINING GUESSES: " + str(hangman.guesses))
        print("PREVIOUS GUESSES: " + str(hangman.previous_guesses))
        print("ENCRYPTED WORD: " + hangman.encrypted_word)

        print("~~~~~")
        learner.think()
        guess = learner.guess()
        print("GUESSED LETTER: " + guess)
        hangman.manipulate_encrypted_word(guess)
        is_correct = hangman.is_guess_correct(guess)
        learner.calculate_frequencies(guess, is_correct)
        print("LEARNER'S PREVIOUS GUESSES: " + str(learner.previous_guesses))
        print("~~~~~")

        ROUNDS = ROUNDS + 1
        IS_GAME_RUNNING = hangman.is_game_running()
        # next_round = input("NEXT ROUND? ")
        # if next_round == "y":
        #     IS_GAME_RUNNING = True
        # else:
        #     IS_GAME_RUNNING = False

    learner.learn(hangman.win)
    games_played = games_played + 1
    ratio = str(games_played) + "," + str(learner.get_number_of_wins()) + "\n"
    file = open("games_played_ratio.csv" ,"a")
    file.write(ratio)
    file.close()
    RUNS = RUNS + 1



