from HangmanML import MongoDB_Access as mongo
import random

class Hangman:
    def __init__(self, word_list):
        self.previous_guesses = []
        self.guesses = 10
        self.word_list = None
        self.word = None
        self.encrypted_word = None
        #self.get_word_list()
        self.get_random_word(word_list)
        self.encrypt_word()
        self.win = None

    def get_word_list(self):
        word_list = mongo.get_dictionary_words()
        self.word_list = word_list

    def get_random_word(self, word_list):
        getting_word = True
        is_alphabetical = False
        while getting_word:
            random_num = random.randint(0, len(word_list) - 1)
            random_word = word_list[random_num]
            for letter in random_word:
                ascii_value = ord(letter)
                if 65 <= ascii_value <= 90 or 97 <= ascii_value <= 122:
                    is_alphabetical = True
            if is_alphabetical:
                self.word = random_word
                getting_word = False

    def encrypt_word(self):
        encrypted_word = ""
        for letter in self.word:
            encrypted_word = encrypted_word + "*"
        self.encrypted_word = encrypted_word

    def get_guess(self):
        guess = input("ENTER A GUESS: ").lower()
        return guess

    def guessed_before(self, guess):
        if self.previous_guesses.count(guess) > 0:
            return True
        return False

    def is_guess_correct(self, guess):
        if len(guess) > 1 or not guess.isalpha():
            print("INVALID GUESS")
            return False
        if self.guessed_before(guess):
            print("YOU HAVE ALREADY GUESSED THAT LETTER")
            return False
        for letter in self.word:
            if guess == letter.lower() or letter == letter.upper():
                print("CORRECT GUESS!")
                self.previous_guesses.append(guess)
                return True
        print("INCORRECT GUESS")
        self.previous_guesses.append(guess)
        global GUESSES
        self.guesses = self.guesses - 1
        return False

    def manipulate_encrypted_word(self, guess):
        encrypted_list = list(self.encrypted_word)
        i = 0
        for letter in self.word:
            if guess == letter.lower() or guess == letter.upper():
                encrypted_list[i] = letter
            i = i + 1
        self.encrypted_word = "".join(encrypted_list)

    def is_game_running(self):
        is_game_running = True
        if self.word == self.encrypted_word:
            print("YOU WON!")
            print("WORD: " + self.word)
            self.win = True
            is_game_running = False
            return is_game_running
        if self.guesses == 0:
            print("YOU LOST!")
            print("CORRECT WORD: " + self.word)
            is_game_running = False
            self.win = False
            return is_game_running
        return is_game_running
