# -*- coding:utf-8 -*-qq邮箱登陆登录
# import gensim
import numpy as np
import logging
import os
import re
from itertools import islice

# model = gensim.models.KeyedVectors.load_word2vec_format("./data/wiki.en.vector", binary=False)
#
# print(model.most_similar("queen"))

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def getWords(file):
    words = []
    logger.info("Getting words list.")
    with open(file, 'r', encoding='utf-8') as f:
        for line in islice(f, 1, None):
            # print(line)
            line = line.strip('\n').split(' ')
            words.append(line[0])
    return words

def getVec(words, file):
    word2vec = {}
    with open(file, 'r', encoding='utf-8') as f:
        for line in islice(f, 1, None):
            line = line.strip('\n').split(' ')
            if line[0] in words:
                word2vec[line[0]] = line[1:]
    return word2vec

def getIndex(str):
    start = "tags"
    end = ".txt"
    pattern = re.compile(start + '(.*?)' + end, re.S)
    index = pattern.findall(str, pos=45)
    return int(index[0])

def getTags(path):
    tags = {}
    logger.info("Getting the tags of pictures.")
    list = os.listdir(path)
    for file in list:
        file = os.path.join(path, file)
        # print(file)
        if os.path.isfile(file):
            indx = getIndex(file)
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip('\n').lower().split(' ')
                    if indx in tags:
                        tags[indx].append(line)
                    else:
                        tmp = []
                        tmp.append(line)
                        tags[indx] = tmp
    return tags

def getTagVec(tags, word2vec):
    for k, v in tags.items():
        tag_vec = []
        for tag in v:
            vec = np.zeros((64))
            if len(tag) > 1:
                for i in range(len(tag)):
                    if tag[i] in word2vec:
                        vec += np.array(word2vec[tag[i]])
            else:
                if tag[0] in word2vec:
                    vec += np.array(word2vec[tag[0]])
            if not (vec == np.zeros((64))).all():
                tag_vec.append(vec.tolist())
        tags[k] = tag_vec
    return tags

def getMaxLength(tags):
    max_length = 0
    for k, v in tags.items():
        max_length = max(max_length, len(v))
    return max_length

if __name__ == "__main__":
    tag = "mirflickr25k\mirflickr25k\mirflickr\meta\\tags_raw"
    vec = "data\wiki.en.vector"
    words = getWords(vec)
    tags = getTags(tag)
    ywords = []
    nwords = []
    for k in tags:
        # print(k)
        for v in tags[k]:
            for word in v:
                if word in words:
                    ywords.append(word)
                else:
                    nwords.append(word)
    word2vec = getVec(ywords, vec)
    # print(len(ywords))
    # print(len(nwords))
    del words, nwords, ywords
    tag_vec = getTagVec(tags, word2vec)
    max_length = getMaxLength(tags)
    del tags, word2vec

    with open("./data/tags.vector", 'w', encoding='utf-8') as f:
        for k, v in tag_vec:
            f.write(k + ' ' + v)

