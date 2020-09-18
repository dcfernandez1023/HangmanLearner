import Hangman
import Hangman_Learner
import MongoDB_Access as mongo
from tqdm import tqdm

##GLOBALS##

#RUNS = 0
WORD_LIST = mongo.get_dictionary_words()

for i in tqdm(range(10000)):
    IS_GAME_RUNNING = True
    # ROUNDS = 1
    hangman = Hangman.Hangman(WORD_LIST)
    learner = Hangman_Learner.Hangman_Learner()

    while IS_GAME_RUNNING:
        # print("---------------")
        # print("HANGMAN OUTPUT")
        # print("ROUND " + str(ROUNDS))
        # print("*for testing purposes... WORD: " + hangman.word)
        # print("REMAINING GUESSES: " + str(hangman.guesses))
        # print("PREVIOUS GUESSES: " + str(hangman.previous_guesses))
        # print("ENCRYPTED WORD: " + hangman.encrypted_word)

        # print("~~~~~")
        learner.think()
        guess = learner.guess()
        if guess == "Skip":
            break
        # print("GUESSED LETTER: " + guess)
        hangman.manipulate_encrypted_word(guess)
        is_correct = hangman.is_guess_correct(guess)
        learner.calculate_frequencies(guess, is_correct)
        # print("LEARNER'S PREVIOUS GUESSES: " + str(learner.previous_guesses))
        # print("~~~~~")

        # ROUNDS = ROUNDS + 1
        IS_GAME_RUNNING = hangman.is_game_running()

    learner.learn(hangman.win)



