'''
Created on May 5, 2016

@author: xiao
'''
from argparse import ArgumentParser
from generate import *


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("seed", type = int, default = 103, nargs = '?',
                        help = "seed to make the generation deterministic")
    parser.add_argument("-output", "-o", default = None,
                        help = "output directory, defaults to None and print to stdout")
    parser.add_argument("-batch", type = int, default = None,
                    help = "Generates all htmls with seed from 0 to this number")
    args = parser.parse_args()
    seeds = [args.seed] if args.batch is None else xrange(args.batch)
    if args.batch is not None: args.output = None
    for seed in seeds:
        generated_html = create(seed)
        out_file = args.output if args.output else str(seed) + '.html'
    #         print generated_html.prettify()
        with open(out_file, 'w') as outf:
            outf.write(str(generated_html))
