from nltk.test.gensim_fixt import setup_module
setup_module()
from nltk.data import find
import gensim
word2vec_sample = 'models/GoogleNews-vectors-negative300.bin'
global word2vec_model
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=True)