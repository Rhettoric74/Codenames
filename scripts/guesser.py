from word2vec_model import word2vec_model
from game_board import GameBoard
class PotentialGuess:
        def __init__(self, index, similarity):
            self.index = index
            self.similarity = similarity
        def __lt__(self, other):
            return self.similarity < other.similarity
class Guesser:
    def word2vec_guess(this, clue, board):
        """
        Purpose: use word2vec embeddings to guess the closest words to the given clue
        Parameters: clue, a tuple containing a string (the word for the clue), and a the number of words
                the clue is meant to go to.
            board, a GameBoard object representing the state of the game.
        Returns: none, guesses words on the board"""
        clue_word = clue[0]
        starting_team = board.get_current_team()
        target_number = clue[1]
        guesses = 0
        guesses_list = []
        word_similarities, unguessed_indices = board.similarities_to_clue(clue_word)
        sorted_guess_indices = sorted([PotentialGuess(unguessed_indices[i], word_similarities[i]) for i in range(len(unguessed_indices))])
        while board.get_current_team() == starting_team and guesses < target_number:
            guesses += 1
            best_guess = sorted_guess_indices.pop(-1)
            closest_word_index = best_guess.index
            print(best_guess.similarity)
            guesses_list.append(board.grid[closest_word_index[0]][closest_word_index[1]])
            board.reveal(closest_word_index, starting_team)
            print(board.codemaster_view())
        if board.get_current_team() == starting_team:
            # switch turns if there weren't any errors that already caused turns to swap.
            board.starting_teams_turn = not board.starting_teams_turn
        print(guesses_list)
if __name__ == "__main__":
    board = GameBoard()
    guesser = Guesser()
    print(board.codemaster_view())
    while board.winner == None:
        
        clue = input("Enter your clue for the " + board.get_current_team() + " team:\n")
        clue = clue.split(",")
        formatted_clue = (clue[0], int(clue[1]))
        guesser.word2vec_guess(formatted_clue, board)
        print(board.codemaster_view())
