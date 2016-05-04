'''
Created on May 4, 2016

@author: xiao
'''
import random
import argparse
from bs4 import BeautifulSoup

_template = open('skeleton.html').read()

# Generation pipeline
def create(max_list_length = 10,
           table_width_range = [2,10],
           table_height_range = [2,20],
           table_cell_char_range = [1, 10],
           paragraph_char_range = [100, 500], 
           ):
    soup = BeautifulSoup(_template,'lxml')
    return soup.body

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", type=int, default=1337, nargs='?',
                        help="seed to make the generation deterministic")
    parser.add_argument("-output","-o", default=None, 
                        help="output directory, defaults to None and print to stdout")
    args = parser.parse_args()
    random.seed(args.seed)
    if args.output is None:
        print create()
    