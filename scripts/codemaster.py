from game_board import GameBoard
from word2vec_model import word2vec_model
import numpy as np
import itertools
from guesser import PotentialGuess, Guesser
    
class CluegivingStrategy:
    def make_clue(board, team):
        return "", 0

class ClosestMean(CluegivingStrategy):
    def make_clue(board, team):
        own_words = board.get_team_words(team)
        print(own_words)
        print(team)
        best_clue = None
        best_score = -float("inf")
        for i in range(min(2, len(own_words)), 0, -1):
            for combination in itertools.combinations(own_words, i):
                # get the word most similar to the average of the grouped words
                cur_clues_list = word2vec_model.most_similar(positive=list(combination), topn=5)
                clue_idx = 0
                cur_clue_word = cur_clues_list[clue_idx][0]
                while not board.is_valid_clue(cur_clue_word):
                    clue_idx += 1
                    cur_clue_word = cur_clues_list[clue_idx][0]
                # compute the score 
                word_similarities, unguessed_indices = board.similarities_to_clue(cur_clue_word)
                sorted_guesses = sorted([PotentialGuess(unguessed_indices[i], word_similarities[i]) for i in range(len(word_similarities))])
                # pick the i most similar words, where i is the number of words supposedly connected by the clue.
                top_guesses = sorted_guesses[:i]
                predicted_score = 0
                for j, guess in enumerate(top_guesses):
                    # check if the potential guess is on the codemaster's team
                    if (board.grid[guess.index[0]][guess.index[1]] in own_words):
                        predicted_score += 2*2**(i - j - 1)
                    elif guess.index in board.bystander_indices:
                        predicted_score -= 1*2**(i - j - 1)
                    elif guess.index in board.assasin_indices:
                        predicted_score -= 5*2**(i - j - 1)
                    else:
                        predicted_score -= 2*2**(i - j - 1)
                print(predicted_score)
                if predicted_score >= best_score:
                    best_clue = (cur_clue_word, i)
                    best_score = predicted_score
        return best_clue
            
                    

class Codemaster:
    def __init__(self, team = None, strategy = ClosestMean):
        self.team = team
        self.strategy = strategy
    def give_clue(self, board):
        if self.team == None:
            self.team = board.get_current_team()
        return self.strategy.make_clue(board, self.team)

if __name__ == "__main__":
    gb = GameBoard()
    red_codemaster = Codemaster("Red")
    blue_codemaster = Codemaster("Blue")
    guesser = Guesser()
    while gb.winner == None:
        print(gb.codemaster_view())
        clue = None
        if gb.get_current_team() == "Red":
            clue = red_codemaster.give_clue(gb)
        else:
            clue = blue_codemaster.give_clue(gb)
        print(clue)
        guesser.word2vec_guess(clue, gb)

