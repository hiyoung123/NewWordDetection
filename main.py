#!usr/bin/env python
#-*- coding:utf-8 -*-

import argparse
from src.detection import NewWordDetection


def main(args):

    detection = NewWordDetection(
        alpha=args.alpha,
        beta=args.beta,
        hash_size=args.hash_size,
        block_num=args.block_num,
        max_word_len=args.max_word_len,
        dict_file=args.dict_file)
    detection.load_text(args.doc_path)
    for i in range(10):
        print(detection.word_info_dict[i])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--doc_path', default='data/corpus', type=str, help='Doc file path')
    parser.add_argument('--dict_file', default='data/dict.txt', type=str, help='Dict file')
    parser.add_argument('--stop_file', default='data/dict.txt', type=str, help='Stopwords file')
    parser.add_argument('--alpha', default=0.3, type=float, help='score=alpha*pmi + (1-alpha)*df')
    parser.add_argument('--beta', default=0.1, type=float, help='score=beta*freq + (1-beta)*score')
    parser.add_argument('--count', default='data/dict.txt', type=str, help='Dict file')
    parser.add_argument('--freq', default='data/dict.txt', type=str, help='Dict file')
    parser.add_argument('--pmi', default='data/dict.txt', type=str, help='Dict file')
    parser.add_argument('--df', default='data/dict.txt', type=str, help='Dict file')
    parser.add_argument('--score', default='data/dict.txt', type=str, help='Dict file')
    parser.add_argument('--max_word_len', default=5, type=int, help='max_word_len, default=5')
    parser.add_argument('--hash_size', default=64, type=int, help='hash_size, default=64')
    parser.add_argument('--block_num', default=4, type=int, help='block_num, default=4')
    args = parser.parse_args()
    main(args)