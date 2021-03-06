#!usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import math
import time
from src.deduplicate import DuplicateRemove


class WordInfo:
    def __init__(self, text):
        self.text = text
        self.count = 0
        self.freq = 0
        self.pmi = 0
        self.df = 0
        self.score = 0
        self.left = {}
        self.right = {}
        self.left_entropy = 0
        self.right_entropy = 0

    def __eq__(self, other):
        return self.text == other.text

    def __str__(self):
        return '(Word: %s, Count: %s, Freq: %s, PMI: %s, DF: %s, Score: %s, Left: %s, Right: %s)' \
               % (self.text, self.count, self.freq, self.pmi, self.df, self.score, self.left, self.right)


class NewWordDetection:
    def __init__(self, count=0, freq=0.0, pmi=0.0, df=0.0, score=0.0, alpha=0.0, beta=0.0, max_word_len=5,
                 hash_size=64, block_num=4, dict_file='data/dict.txt', stopwords=[]):
        """
        :param count: 词数阈值
        :param freq: 词频阈值
        :param pmi: pmi阈值
        :param df: df阈值
        :param score: 得分阈值
        :param alpha: 调节参数 - alpha越大，pmi占比越大，df占比越小
        :param beta: 调节参数 - beta越大，freq 占比越大
        :param max_word_len: 最大词长度
        :param hash_size: simhash 维度
        :param block_num: 倒排索引数量
        :param dict_file: 原有词典，主要用于文本去重中频率计算，其次比较新词
        :param stopwords: 停用词，用于文本去重
        """
        self.count = count
        self.freq = freq
        self.pmi = pmi
        self.df = df
        self.score = score
        self.alpha = alpha
        self.beta = beta
        self.max_word_len = max_word_len
        self.word_info_dict = {}
        self.remove = DuplicateRemove(hash_size, block_num, dict_file, stopwords)

    @staticmethod
    def extract_cand_words(text, max_word_len):
        indexes = []
        doc_len = len(text)
        for i in range(doc_len):
            for j in range(i + 1, min(i + 1 + max_word_len, doc_len + 1)):
                indexes.append((i, j))
        return sorted(indexes, key=lambda x: text[x[0]:x[1]])

    @staticmethod
    def calc_pmi(word_info, word_info_dict):
        grams = [(word_info.text[0:_i], word_info.text[_i:]) for _i in range(1, len(word_info.text))]
        if len(grams) == 0:
            return 0
        return min(
            map(
                lambda x: math.log(word_info.freq/(word_info_dict[x[0]].freq * word_info_dict[x[1]].freq)),
                grams
            )
        )

    @staticmethod
    def calc_df(word_info):
        return min(word_info.right_entropy, word_info.left_entropy)

    @staticmethod
    def calc_score(word_info, alpha, beta):
        score = alpha * word_info.pmi + (1-alpha) * word_info.df
        score = beta * word_info.freq + (1-beta) * score
        return score

    @staticmethod
    def calc_entropy(words: dict):
        if len(words) == 0:
            return 0
        total_len = sum(words.values())
        return sum(map(lambda x: -x/total_len*math.log(x/total_len), words.values()))

    def counter(self, text):
        text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#”“￥：%……&*（）]+", '', text)
        word_index_list = self.extract_cand_words(text, self.max_word_len)
        total_word_len = len(word_index_list)

        for start, end in word_index_list:
            # 获取词信息，没有则创建
            word = text[start:end]
            if word not in self.word_info_dict:
                self.word_info_dict[word] = WordInfo(word)
            word_info = self.word_info_dict[word]

            # 统计频数
            word_info.count += 1
            # 统计词频
            word_info.freq = word_info.count / total_word_len
            # 统计左词
            left = text[start-1:start]
            word_info.left[left] = word_info.left.get(left, 0) + 1
            # 统计右词
            right = text[end:end+1]
            word_info.right[right] = word_info.right.get(right, 0) + 1

    def compute(self):

        for word in self.word_info_dict:
            word_info = self.word_info_dict[word]

            # 计算左词熵
            word_info.left_entropy = self.calc_entropy(word_info.left)
            # 计算右词熵
            word_info.right_entropy = self.calc_entropy(word_info.right)
            # 计算PMI值
            word_info.pmi = self.calc_pmi(word_info, self.word_info_dict)
            # 计算DF值
            word_info.df = self.calc_df(word_info)
            # 计算SCORE值
            word_info.score = self.calc_score(word_info, self.alpha, self.beta)

        self.word_info_dict = sorted(self.word_info_dict.values(), key=lambda v: v.score, reverse=True)

    def load_text(self, file_path):
        if not os.path.exists(file_path):
            return

        for file in os.listdir(file_path):
            file = os.path.join(file_path, file)
            text = open(file, 'r', encoding='utf-8').read()
            if self.remove.contains(text):
                print('重复内容文章：%s' % file)
                continue
            print('新处理文章：%s' % file)
            self.remove.insert(text, file)
            self.counter(text)

        self.compute()


if __name__ == '__main__':
    start_time = time.process_time()
    doc = open('../data/document2', 'r', encoding='utf-8').read()
    nwd = NewWordDetection(alpha=0.3, beta=0.1)
    for i in range(20):
        print(nwd.word_info_dict[i])
    print('Total time : %s' % (time.process_time() - start_time))
    word_dict = [x.split()[0] for x in open('../data/dict.txt', 'r', encoding='utf-8')]
    for word in nwd.word_info_dict:
        if word.text not in word_dict:
            print(word)
