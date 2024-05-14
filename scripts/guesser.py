from word2vec_model import word2vec_model
from game_board import GameBoard

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
        guessed_list = board.teams + ["Bystander", "Assasin"]
        guesses = 0
        while board.get_current_team() == starting_team and guesses < target_number:
            guesses += 1
            unguessed_words = []
            unguessed_indices = []
            for row in range(board.rows):
                for column in range(board.columns):
                    word = board.grid[row][column]
                    if word not in guessed_list and word.lower() in word2vec_model:
                        unguessed_words.append(word.lower())
                        unguessed_indices.append((row, column))
                    elif word not in guessed_list and word.lower() not in word2vec_model:
                        unguessed_words.append(word[0].upper() + word[1:].lower())
                        unguessed_indices.append((row, column))
                    elif word not in guessed_list:
                        print(word)
            word_distances = [word2vec_model.similarity(clue_word, word) for word in unguessed_words]
            min_distance = max(word_distances)
            closest_word_index = unguessed_indices[word_distances.index(min_distance)]
            board.reveal(closest_word_index, starting_team)
            print(board.codemaster_view())
        if board.get_current_team() == starting_team:
            # switch turns if there weren't any errors that already caused turns to swap.
            board.starting_teams_turn = not board.starting_teams_turn
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
