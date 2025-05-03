from word2vec_model import word2vec_model
from game_board import GameBoard
import numpy as np
import random
import time

MIN_COUNTS = 100
class FrenchToastGame:
    def __init__(self, word = None):
        print("I have a french toast!")
        self.word = word
        self.current_guess = "toast"
        self.guessed = False
    def generate_word(self):
        # TODO: restrict this to just nouns
        self.word = GameBoard().grid[0][0]
    def answer_guess(self, new_guess):
        if self.word.upper() == new_guess.upper():
            print("It is " + self.word + "!")
            self.current_guess = new_guess
            self.guessed = True
            return True
        new_guess_similarity = word2vec_model.similarity(self.word, new_guess)
        current_guess_similarity = word2vec_model.similarity(self.current_guess, self.word)
        print(max(new_guess_similarity, current_guess_similarity))
        if new_guess_similarity > current_guess_similarity:
            print("Closer to", new_guess)
            self.current_guess = new_guess
            return True
        else:
            print("Closer to", self.current_guess)
            return False
    def get_guesses_from_terminal(self):
        while not self.guessed:
            print("We're on " + self.current_guess)
            current_guess = input("Is it closer to " + self.current_guess + " or closer to ")
            while current_guess not in word2vec_model:
                print(current_guess + " has no vector representation")
                current_guess = input("Is it closer to " + self.current_guess + " or closer to ")
            self.answer_guess(current_guess)
class FrenchToastGuesser:
    def __init__(self):
        self.positive_guesses = []
        self.negative_guesses = []
        self.num_guesses = 0
        self.num_repeat_guesses = 0
    def generate_guess(self, game, wait_time = 0):
        self.num_guesses += 1
        self.positive_guesses.append(game.current_guess)
        # reduce randomness the more previous guesses there have been
        top_n = max(10, 1000 - self.num_guesses * 10)
        similar_words = word2vec_model.most_similar(positive=self.positive_guesses[-5:], negative=self.negative_guesses[-5:], topn=top_n)
        filtered_similar_words = [word for word, vector in similar_words if (word2vec_model.get_vecattr(word, 'count') >= MIN_COUNTS) and word.isalpha() and word not in (self.positive_guesses + self.negative_guesses)]
        if len(filtered_similar_words) == 0:
            print("No guesses passed the filter!")
            guess = random.choice(similar_words)[0]
        else:
            guess = random.choice(filtered_similar_words)
        print("Closer to " + game.current_guess + " or closer to " + guess + "?")
        if guess in self.negative_guesses or guess in self.positive_guesses:
            self.num_repeat_guesses += 1
        if not game.answer_guess(guess):
            self.negative_guesses.append(guess)
        if wait_time > 0:
            time.sleep(wait_time)
    def play_game(self, game, wait_time = 0, guess_limit = float("inf")):
        while not game.guessed and self.num_guesses < guess_limit:
            self.generate_guess(game, wait_time)
if __name__ == '__main__':
    game = FrenchToastGame("Kitchen")
    #game.generate_word()
    print(game.word)
    guesser = FrenchToastGuesser()
    time.sleep(2)
    guesser.play_game(game, 0, 100)
    print(guesser.num_guesses, guesser.num_repeat_guesses)
    