import random

class Hangman_Learner:
    def __init__(self):
        #self.guesses = guesses
        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z"]
        self.vowels = ["a", "e", "i", "o", "u"]
        self.consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t",
                "v", "w", "x", "y", "z"]
        self.previous_guesses = []
        self.choose_vowel = None
        self.choose_randomly = None
        self.letter_frequencies = self.get_letter_frequencies()

    def get_letter_frequencies(self):
        letter_frequencies = self.read_file("letter_frequencies.txt")
        if letter_frequencies is None or letter_frequencies == "":
            letter_frequencies = self.reset_letter_frequencies()
        return letter_frequencies

    def consonant_or_vowel(self):
        if len(self.previous_guesses) == 0:
            self.choose_vowel = True
            #print("Choosing vowel: first guess ")
            return
        if len(list(set(self.previous_guesses).intersection(self.vowels))) ==  len(self.vowels):
            self.choose_vowel = False
            #print("Choosing consonant: out of vowels")
            return
        if len(list(set(self.previous_guesses).intersection(self.consonants))) ==  len(self.consonants):
            self.choose_vowel = True
            #print("Choosing vowel: out of consonants")
            return
        if len(self.consonants) == 0 and len(self.vowels) == 0:
            self.choose_vowel = None
            #print("Out of vowels and consonants")
            return
        if self.vowels.count(self.previous_guesses[len(self.previous_guesses)-1]) > 0:
            self.choose_vowel = False
            #print("Choosing consonant: last guess was vowel")
            return
        if self.consonants.count(self.previous_guesses[len(self.previous_guesses)-1]) > 0:
            self.choose_vowel = True
            #print("Choosing vowel: last guess was consonant")
            return

    def update_previous_guesses(self, guess):
        self.previous_guesses.append(guess)

    def manipulate_vowels(self, letter):
        self.vowels.remove(letter)

    def manipulate_consonants(self, letter):
        self.consonants.remove(letter)

    def random_guess(self):
        is_guessing = True
        while is_guessing:
            n = random.randint(0, len(self.alphabet) - 1)
            letter = self.alphabet[n]
            if self.previous_guesses.count(letter) == 0:
                self.update_previous_guesses(letter)
                self.alphabet.remove(letter)
                return letter

    def calculate_frequencies(self, guess, is_correct):
        if self.letter_frequencies is None:
            self.reset_letter_frequencies()
        if is_correct:
            frequency = self.letter_frequencies.get(guess)
            frequency[0] = frequency[0] + 1
            frequency[1] = frequency[1] + 1
            self.letter_frequencies[guess] = frequency
        else:
            frequency = self.letter_frequencies.get(guess)
            frequency[1] = frequency[1] + 1
            self.letter_frequencies[guess] = frequency

    def write_file(self, data, file_name):
        file = open(file_name , "w")
        file.write(str(data))
        file.close()

    def append_file(self, data, file_name):
        file = open(file_name, "a")
        file.write(str(data))
        file.close()

    def read_file(self, file_name):
        file = open(file_name , "r")
        data = file.read()
        try:
            letter_frequencies = eval(data)
        except SyntaxError:
            letter_frequencies = None
        file.close()
        return letter_frequencies

    def sequential_guess(self, i):
        if i < len(self.alphabet):
            letter = self.alphabet[i]
            return letter
        return "z"

    def calculate_percentages(self): #returns dictionary of letters with their percentages calculated
        if self.letter_frequencies is None:
            self.reset_letter_frequencies()
        frequencies = list(self.letter_frequencies.values())
        letters = list(self.letter_frequencies.keys())
        percentages = {}
        for i in range(len(frequencies)):
            element = frequencies[i]
            times_correct = element[0]
            times_guessed = element[1]
            try:
                percentage = times_correct / times_guessed
                letter = letters[i]
                percentages.update({letter: percentage})
            except ZeroDivisionError:
                percentage = 0
                letter = letters[i]
                percentages.update({letter: percentage})
        return percentages

    def is_all_weighted(self, calculated_percentages):
        percentages = list(calculated_percentages.values())
        if percentages.count(0) > 0:
            return False
        return True

    def get_vowel_percentages(self, letter_percentages):
        vowel_percentages = {}
        for i in range(len(self.vowels)):
            vowel = self.vowels[i]
            percentage = letter_percentages.get(vowel)
            vowel_percentages[vowel] = percentage
        return vowel_percentages

    def get_consonant_percentages(self, letter_percentages):
        consonant_percentages = {}
        for i in range(len(self.consonants)):
            consonant = self.consonants[i]
            percentage = letter_percentages.get(consonant)
            consonant_percentages[consonant] = percentage
        return consonant_percentages

    def get_highest_percentage_letter(self, letter_percentages):
        try:
            i = 0
            letters = list(letter_percentages.keys())
            percentages = list(letter_percentages.values())
            #print(letters)
            highest_percentage_letter = letters[i]
            highest_percentage = percentages[i]
            i = i + 1
            while i < len(letters):
                next_letter = letters[i]
                next_percentage = percentages[i]
                if next_percentage > highest_percentage:
                    highest_percentage = next_percentage
                    highest_percentage_letter = next_letter
                i = i + 1
            return highest_percentage_letter
        except Exception:
            return "Skip"


    def guess_vowel(self, vowel_percentages):
        is_guessed_before = False
        vowel = self.get_highest_percentage_letter(vowel_percentages)
        if self.previous_guesses.count(vowel) > 0:
            is_guessed_before = True
            vowel_percentages.pop(vowel)
        while is_guessed_before:
            vowel = self.get_highest_percentage_letter(vowel_percentages)
            if self.previous_guesses.count(vowel) > 0:
                is_guessed_before = True
                vowel_percentages.pop(vowel)
            else:
                is_guessed_before = False
        #self.manipulate_vowels(vowel)
        self.update_previous_guesses(vowel)
        return vowel

    def guess_consonant(self, consonant_percentages):
        is_guessed_before = False
        consonant = self.get_highest_percentage_letter(consonant_percentages)
        if self.previous_guesses.count(consonant) > 0:
            is_guessed_before = True
            consonant_percentages.pop(consonant)
        while is_guessed_before:
            consonant = self.get_highest_percentage_letter(consonant_percentages)
            if self.previous_guesses.count(consonant) > 0:
                is_guessed_before = True
                consonant_percentages.pop(consonant)
            else:
                is_guessed_before = False
        #self.manipulate_consonants(consonant)
        self.update_previous_guesses(consonant)
        return consonant

    def get_number_of_wins(self):
        data = self.read_file("game_results.txt")
        if data is None:
            number_of_wins = 0
        else:
            number_of_wins = data.get("number_of_wins")
        return number_of_wins

    def get_number_of_games_played(self):
        data = self.read_file("game_results.txt")
        if data is None:
            number_of_games_played = 0
        else:
            number_of_games_played = data.get("number_of_games_played")
        return number_of_games_played

    def reset_letter_frequencies(self):
        letter_frequencies = {"a": [0, 0], "b": [0, 0], "c": [0, 0], "d": [0, 0], "e": [0, 0], "f": [0, 0], "g": [0, 0],
                              "h": [0, 0], "i": [0, 0], "j": [0, 0], "k": [0, 0], "l": [0, 0], "m": [0, 0], "n": [0, 0],
                              "o": [0, 0], "p": [0, 0], "q": [0, 0], "r": [0, 0],
                              "s": [0, 0], "t": [0, 0], "u": [0, 0], "v": [0, 0], "w": [0, 0], "x": [0, 0], "y": [0, 0],
                              "z": [0, 0]}
        return letter_frequencies

    ##METHODS TO BE CALLED PUBLICLY##
    def think(self):
        #print(self.letter_frequencies)
        letter_percentages = self.calculate_percentages()
        #print(letter_percentages)
        self.choose_randomly = not self.is_all_weighted(letter_percentages) #sets a boolean data member that determines whether to guess randomly or not
        #print("Choosing randomly: " + str(self.choose_randomly))
        #self.choose_randomly = False
        if not self.choose_randomly:
            self.consonant_or_vowel() #sets a boolean data member that determines whether to guess a vowel or a consonant

    def guess(self):
        #print("Choosing vowel: " + str(self.choose_vowel))
        if self.choose_randomly:
            guess = self.random_guess()
            return guess
        letter_percentages = self.calculate_percentages()
        if self.choose_vowel:
            vowel_percentages = self.get_vowel_percentages(letter_percentages)
            guess = self.guess_vowel(vowel_percentages)
            return guess
        consonant_percentages = self.get_consonant_percentages(letter_percentages)
        guess = self.guess_consonant(consonant_percentages)
        return guess

    def learn(self, is_won):
        keys = ("letter_percentages", "vowel_percentages", "consonant_percentages", "number_of_wins", "number_of_games_played")
        data_package = dict.fromkeys(keys)
        data_list = []
        i = 0

        letter_percentages = self.calculate_percentages()
        vowel_percentages = self.get_vowel_percentages(letter_percentages)
        consonant_percentages = self.get_consonant_percentages(letter_percentages)
        number_of_wins = self.get_number_of_wins()
        number_of_games_played = self.get_number_of_games_played()

        if is_won:
            number_of_wins = number_of_wins + 1
        number_of_games_played = number_of_games_played + 1

        ratio = str(number_of_games_played) + "," + str(number_of_wins) + "\n"
        data_list.append(letter_percentages)
        data_list.append(vowel_percentages)
        data_list.append(consonant_percentages)
        data_list.append(number_of_wins)
        data_list.append(number_of_games_played)

        for key in data_package:
            data_package[key] = data_list[i]
            i = i + 1
        self.append_file(ratio, "games_played_ratio.csv")
        self.write_file(data_package, "game_results.txt")
        self.write_file(self.letter_frequencies, "letter_frequencies.txt")
