import just_one_guesser
from word2vec_model import word2vec_model
import game_board
import numpy as np
import random
import copy
class JustOneGame:
    def __init__(self, words_list = None, num_players = 7):
        if words_list == None:
            words_list = random.sample(game_board.GameBoard().words_list, 13)
        self.words_list = words_list
        self.num_players = num_players
        self.players = []
        for i in range(num_players):
            self.players.append(just_one_guesser.JustOneGuesser())
        self.game_score = 0
    def remove_unallowed_clues(self, clues_list, word):
        #TODO: add more robust ways of removing illegal clues:
        allowed_list = []
        for clue in clues_list:
            if clues_list.count(clue) == 1 and word not in clue:
                allowed_list.append(clue)
        return allowed_list
                
    def play_game(self):
        turn_index = 0
        while len(self.words_list) > 0:
            active_guesser = self.players[turn_index % self.num_players]
            current_word = self.words_list.pop(0)
            if current_word not in word2vec_model:
                current_word = current_word.lower()
            clues_list = [player.give_clue(current_word) for player in self.players if player != active_guesser]
            print("Clues:", clues_list)
            allowed_list = self.remove_unallowed_clues(clues_list, current_word)
            print(allowed_list)
            guess = active_guesser.guess(allowed_list)
            print("Word:", current_word, "Guess:", guess)
            if guess.upper() == current_word.upper():
                self.game_score += 1
                print("Correct guess!")
            elif guess != "<PASS>":
                # remove an additional word randomly from the list
                # if the guesser guessed incorrectly
                if len(self.words_list) > 0:
                    self.words_list.remove(random.choice(self.words_list))
                else:
                    self.game_score -= 1
            turn_index += 1
        print("Final score:", self.game_score)
if __name__ == "__main__":
    game = JustOneGame()
    game.play_game()
            
