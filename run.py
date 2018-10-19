# from lstm import LSTM
# from keras.models import Model
import os
import pickle
import numpy as np
import embeddings

def normalization(vec):
    vmin, vmax = vec.min(), vec.max()
    vec = (vec-vmin)/(vmax-vmin)
    return vec.tolist()

def main():
    if not os.path.isfile("./data/tags.vector.pkl"):
        embeddings.run()
    with open("./data/tags.vector.pkl", 'rb') as f:
        tag_vecs = pickle.load(f)
        max_length = pickle.load(f)
    res = []
    for i in range(len(tag_vecs)):
        vec = np.array((64,), dtype=np.float64)
        for tag_vec in tag_vecs[i]:
            vec += np.array(tag_vec)
        vec = normalization(vec)
        res.append(vec)
    with open("./data/tags.vec.txt", 'w', encoding='utf-8') as f:
        for vec in res:
            f.write(str(vec) + '\n')

if __name__ == "__main__":
    main()
    # model = LSTM()
    # model.build_model()
    #
    # intermediate_layer_model = Model(inputs=model.input,
    #                                  outputs=model.get_layer('cell_2').output)
    # output = intermediate_layer_model.predict()