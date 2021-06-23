#!usr/bin/env python
#-*- coding:utf-8 -*-

import os
import argparse
from src.deduplicate import DuplicateRemove
from src.detection import NewWordDetection

dr = DuplicateRemove(64, 4)

def main(args):
    bash_path = args.dco_path
    for file in os.listdir(bash_path):
        text = load_file(os.path.join(bash_path, file))



def load_file(file):
    if not os.path.exists(file):
        return
    text = open(file, 'r', encoding='utf-8').read()
    return text




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--doc_path', type=str, help='Doc file path')
    parser.add_argument('--dict_file', type=str, help='Dict file')
    #parser.add_argument('--')
    args = parser.parse_args()
    main(args)