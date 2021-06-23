#!usr/bin/env python
#-*- coding:utf-8 -*-

import argparse
from src.detection import NewWordDetection


def main(args):

    detection = NewWordDetection(alpha=0.3, beta=0.1)
    detection.load_text(args.doc_path)
    for i in range(10):
        print(detection.word_info_dict[i])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--doc_path', default='data/corpus', type=str, help='Doc file path')
    parser.add_argument('--dict_file', default='data/dict.txt', type=str, help='Dict file')
    args = parser.parse_args()
    main(args)