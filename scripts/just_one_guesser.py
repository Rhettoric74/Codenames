from word2vec_model import word2vec_model
import random
VOCAB_RESTRICT_SIZE = None
class JustOneGuesser:
    def __init__(self) -> None:
        pass
    def guess(self, clues_list):
        #TODO: come up with other ways the guesser can decide to pass
        candidates = word2vec_model.most_similar(positive=clues_list, topn = 20,  restrict_vocab=VOCAB_RESTRICT_SIZE)
        upper_case_clues = [clue.upper() for clue in clues_list]
        for candidate_word in candidates:
            candidate_word = candidate_word[0]
            #filter out potential multiple-word answers
            # prevent the guesser from guessing words given as clues
            if "_" not in candidate_word and candidate_word.upper() not in clues_list:
                return candidate_word
        return "<PASS>"
    def give_clue(self, word):
        # for now we just randomly choose one of the closest words to the word we're cluing towards
        potential_clues = word2vec_model.most_similar(positive=[word], topn = 50, restrict_vocab=VOCAB_RESTRICT_SIZE)
        legal_clues = []
        for clue in potential_clues:
            clue = clue[0]
            if "_" not in clue and word not in clue.upper():
                legal_clues.append(clue)
        # randomly choose to give one of the top ten best clues
        return random.choice(legal_clues[:15])
    
        