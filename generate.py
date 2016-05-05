'''
Created on May 3, 2016

@author: xiao
'''
import argparse
import numpy as np
from bs4 import BeautifulSoup

_words = '''
    Lorem ipsum dolor sit amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna
    aliquam erat volutpat Ut wisi enim ad minim veniam quis nostrud exerci tation ullamcorper suscipit lobortis
    nisl ut aliquip ex ea commodo consequat Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse
    molestie consequat vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim
    qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi Nam liber tempor cum
    soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum
'''.split()

_headers = 'Parameter Value Description Unit'.split()
_subheaders = 'Min Max Typ Range'.split()

_template = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
       "http://www.w3.org/TR/html4/strict.dtd">
    <html lang="en">
    <head>
        <style type="text/css">
        body {
            margin: 2% 5%;
            font-family: Arial, sans-serif;
            background-color: white;
        }
        table,
        th,
        td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        td {
            padding: 5px;
        }
        .content {
            column-count: 1;
        }
        </style>
    </head>
    <body>
        <div class="content"></div>
    </body>
    </html>
'''
def sample_discrete_normal(low, high):
    '''
    Sampling a discrete number in the given range from
    a Gaussian distribution
    '''
    loc = (high + low) / 2
    scale = (high - low) / 2
    return int(np.random.normal(loc, scale))

def sample_discrete_uniform(low, high):
    '''
    Sampling a discrete number in the given range from
    a uniform distribution
    '''
    return int(np.random.uniform(low, high))
    
def create_paragraph(soup,
                     word_range=[20, 100],
                     numerical=False):
    p = soup.new_tag('p')
    target_length = np.random.randint(*word_range)
    if numerical:
        p.string = ''.join(str(np.random.randint(0, 10)) for i in xrange(target_length))
    else:
        rand_words = np.random.choice(_words, target_length)
        p.string = (' '.join(rand_words)).capitalize()
    return p

def create_header(soup,
                  level=1,
                  word_range=[2, 6],
                  all_cap_prob=0.5):
    level = max(1, level)
    level = min(5, level)
    h = soup.new_tag('h' + str(level)) 
    target_length = np.random.randint(*word_range)
    rand_words = np.random.choice(_words, target_length)
    content = (' '.join(rand_words))
    h.string = content.upper() if np.random.rand() < all_cap_prob else content.title()
    return h

def create_table(soup,
                 col_range=[2, 5],
                 row_range=[2, 8],
                 header_word_range=[1, 5],
                 header_col_max=1,
                 header_row_max=1,
                 value_len_range=[1, 4],
                 cell_word_range=[1, 10],
                 cell_sub_row_range=[1, 4],
                 ):
    table = soup.new_tag('table')
    tbody = soup.new_tag('tbody')
    table.append(tbody)
    rows = sample_discrete_normal(*row_range)
    columns = sample_discrete_normal(*col_range)
    for r in xrange(rows):
        tr = soup.new_tag('tr')
        for c in xrange(columns):
            td = soup.new_tag('td')
            if c < header_col_max or r < header_row_max:
                p = create_paragraph(soup, header_word_range)
            else:
                p = create_paragraph(soup, value_len_range, numerical=True)
            td.append(p)
            tr.append(td)
        tbody.append(tr)
    return table

# HTML generation pipeline
def create(head_prob=0.8):
    soup = BeautifulSoup(_template, 'html.parser')
    if np.random.rand() < head_prob:
        soup.body.insert(0, create_header(soup, level=1))
    content = soup.body.div
    content.append(create_paragraph(soup))
    content.append(create_table(soup))
    return soup

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", type=int, default=1337, nargs='?',
                        help="seed to make the generation deterministic")
    parser.add_argument("-output", "-o", default=None,
                        help="output directory, defaults to None and print to stdout")
    args = parser.parse_args()
    np.random.seed(args.seed)
    
    generated_html = create()
    if args.output is None:
        print generated_html.prettify()
    else:
        with open(args.output, 'w') as outf:
            outf.write(str(generated_html))
    
        
    
