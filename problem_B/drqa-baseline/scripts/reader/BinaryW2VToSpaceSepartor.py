#%%
from gensim.models.keyedvectors import KeyedVectors
from tqdm import tqdm
#%%
w2v = KeyedVectors.load_word2vec_format("182/model.bin", binary=True)
#%%
word_vecs = {}
for word in tqdm(w2v.vocab):
    vec = w2v[word]
    word = word.replace("::", "_")
    word = word.split("_")[0]
    word_vecs[word] = vec
#%%
with open("ruwiki_300.txt", "wt") as outfile:
    for word, vec in tqdm(word_vecs.items()):
        vec = " ".join([str(i) for i in vec])
        wordvec = " ".join([word, vec])
        outfile.write(wordvec + "\n")