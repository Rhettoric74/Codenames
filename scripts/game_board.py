import random
import os
import sys
import copy
from word2vec_model import word2vec_model
sys.path.append(os.pardir)
class GameBoard:
    def __init__(self, words_file = "words\words_eng_400.txt", rows = 5, columns = 5, card_distribution = (9, 8, 7, 1)) -> None:
        self.teams = ["Red", "Blue"]
        random.shuffle(self.teams)
        self.rows = rows
        self.columns = columns
        words = []
        with open(words_file) as f:
            for line in f:
                words.append(line.strip())
        selected_words = random.sample(words, rows * columns)
        self.words_list = selected_words
        self.grid = []
        for i in range(rows):
            self.grid.append(selected_words[i*columns : (i + 1) * columns])
        grid_indicies = set()
        for i in range(rows):
            for j in range(columns):
                grid_indicies.add((i, j))
        self.starting_team_indices = set(random.sample(list(grid_indicies), card_distribution[0]))
        for index in list(self.starting_team_indices):
            grid_indicies.remove(index)
        self.second_team_indices = set(random.sample(list(grid_indicies), card_distribution[1]))
        for index in list(self.second_team_indices):
            grid_indicies.remove(index)
        self.bystander_indices = set(random.sample(list(grid_indicies), card_distribution[2]))
        for index in list(self.bystander_indices):
            grid_indicies.remove(index)
        self.assasin_indices = set(random.sample(list(grid_indicies), card_distribution[3]))
        self.starting_teams_turn = True
        self.winner = None
    def similarities_to_clue(self, clue):
        unguessed_words = []
        unguessed_indices = []
        guessed_list = self.teams + ["Bystander", "Assasin"]
        for row in range(self.rows):
            for column in range(self.columns):
                word = self.grid[row][column]
                if word not in guessed_list and word.lower() in word2vec_model:
                    unguessed_words.append(word.lower())
                    unguessed_indices.append((row, column))
                elif word not in guessed_list and word.lower() not in word2vec_model:
                    unguessed_words.append(word[0].upper() + word[1:].lower())
                    unguessed_indices.append((row, column))
                elif word not in guessed_list:
                    print(word)
        return ([word2vec_model.similarity(clue, word) for word in unguessed_words], unguessed_indices)
    def __repr__(self):
        board = ""
        if self.winner != None:
            board += self.winner + " has won!\n"
        elif self.starting_teams_turn:
            board += self.teams[0] + "'s turn\n"
        else:
            board += self.teams[1] + "'s turn\n"
        for i in range(self.rows):
            for j in range(self.columns):
                board += self.grid[i][j] + " " * (16 - len(self.grid[i][j]))
            board += "\n"
        return board
    def codemaster_view(self):
        board = ""
        if self.winner != None:
            board += self.winner + " has won!\n"
        elif self.starting_teams_turn:
            board += self.teams[0] + "'s turn\n"
        else:
            board += self.teams[1] + "'s turn\n"
        for i in range(self.rows):
            for j in range(self.columns):
                team_signifier = ""

                if (i, j) in self.starting_team_indices:
                    team_signifier = self.teams[0][0]
                elif (i, j) in self.second_team_indices:
                    team_signifier = self.teams[1][0]
                elif (i, j) in self.bystander_indices:
                    team_signifier = "I"
                elif (i, j) in self.assasin_indices:
                    team_signifier = "A"
                
                board += team_signifier + "-" + self.grid[i][j] + " " * (16 - len(self.grid[i][j]))
            board += "\n"
        return board
    def get_current_team(self):
        if self.starting_teams_turn:
            return self.teams[0]
        return self.teams[1]
    def get_team_words(self, team):
        if team == self.teams[0]:
            return [self.grid[i][j] for (i, j) in self.starting_team_indices if self.grid[i][j] != self.teams[0]]
        elif team == self.teams[1]:
            return [self.grid[i][j] for (i, j) in self.second_team_indices if self.grid[i][j] != self.teams[1]]
        elif team == "Bystander":
            return [self.grid[i][j] for (i, j) in self.bystander_indices if self.grid[i][j] != "Bystander"]
        elif team == "Assassin":
            return [self.grid[i][j] for (i, j) in self.assasin_indices if self.grid[i][j] != "Assassin"]
    def check_for_winner(self):
        """Purpose: check if a team has already won. This function should be called whenever 
        tiles are revealed on the board, to ensure the winner is updated properly."""
        if len(self.get_team_words("Assassin")) > 0:
            if len(self.get_team_words(self.teams[0])) == 0:
                self.winner = self.teams[0]
            elif len(self.get_team_words(self.teams[1])) == 0:
                self.winner = self.teams[1]
    def is_valid_clue(self, clue_word):
        if clue_word in self.words_list:
            return False
        return True
    def reveal(self, indices, team):
        selected_tile_type = None
        if indices in self.starting_team_indices:
            self.grid[indices[0]][indices[1]] = self.teams[0]
            selected_tile_type = self.teams[0]
            self.starting_team_indices.remove(indices)
        elif indices in self.second_team_indices:
            self.grid[indices[0]][indices[1]] = self.teams[1]
            selected_tile_type = self.teams[1]
            self.second_team_indices.remove(indices)
        elif indices in self.bystander_indices:
            self.grid[indices[0]][indices[1]] = "Bystander"
            selected_tile_type = "Bystander"
            self.bystander_indices.remove(indices)
        else:
            self.grid[indices[0]][indices[1]] = "Assasin"
            selected_tile_type = "Assasin"
            self.assasin_indices.remove(indices)
            remaining_team = copy.copy(self.teams)
            remaining_team.remove(team)
            self.winner = remaining_team[0]
        if selected_tile_type != team:
            self.starting_teams_turn = not self.starting_teams_turn
        self.check_for_winner()


        
if __name__ == "__main__":
    board = GameBoard()
    print(board.codemaster_view())
    while board.winner == None:
        indices_chosen = input("Choose the indices of the tile you want to tap:\n")
        indices_chosen = (int(indices_chosen[1]), int(indices_chosen[4]))
        print(indices_chosen)
        board.reveal(indices_chosen, board.get_current_team())
        print(board.codemaster_view())


