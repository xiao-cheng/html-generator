'''
Created on May 3, 2016

@author: xiao
'''
from numpy.random import RandomState
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
    <!DOCTYPE html>
    <html>
    <head>
        <style type="text/css">
        body {
            margin: 2% 5%;
            font-family: Arial, sans-serif;
            background-color: white;
            font-size: 80%;
        }
        .fullgrid,
        .fullgrid tr,
        .fullgrid td{
            border: 1px solid black;
            border-collapse: collapse;
        }
        .outteronly{
            border: 1px solid black;
        }
        table{
            -webkit-column-break-inside:avoid;
            column-break-inside:avoid;
        }
        td {
            padding: 5px;
        }
        .col2 {
            column-count: 2;
            -webkit-column-count: 2;
        }
        .bold{
            font-weight: bold;
        }
        </style>
    </head>
    <body>
        <div></div>
    </body>
    </html>
'''
def sample_discrete_normal(rand, low, high):
    '''
    Sampling a discrete number in the given range from
    a Gaussian distribution, truncated to the given range
    '''
    loc = (high + low) / 2
    scale = (high - low) / 2
    sample = int(rand.normal(loc, scale))
    return min(high, max(low,sample))

def sample_discrete_uniform(rand, low, high):
    '''
    Sampling a discrete number in the given range from
    a uniform distribution
    '''
    return int(rand.uniform(low, high))
    
def create_paragraph(rand,
                     soup,
                     word_range=[20, 100],
                     numerical=False,
                     bold=False):
    p = soup.new_tag('p')
    if bold:
        p['class'] = 'bold'
    target_length = rand.randint(*word_range)
    if numerical:
        p.string = ''.join(str(rand.randint(0, 10)) for i in xrange(target_length))
    else:
        rand_words = rand.choice(_words, target_length)
        p.string = (' '.join(rand_words)).capitalize()
    return p

def create_header(rand,
                  soup,
                  level=1,
                  word_range=[2, 6],
                  all_cap_prob=0.5):
    level = max(1, level)
    level = min(5, level)
    h = soup.new_tag('h' + str(level)) 
    target_length = rand.randint(*word_range)
    rand_words = rand.choice(_words, target_length)
    content = (' '.join(rand_words))
    h.string = content.upper() if rand.rand() < all_cap_prob else content.title()
    return h

def create_list(rand,
                soup,
                ul_prob = 0.95,
                items_range = [1,10]):
    list_elem = soup.new_tag('ul'if rand.rand()<ul_prob else 'ol')
    for i in xrange(sample_discrete_normal(rand, *items_range)):
        li = soup.new_tag('li')
        li.append(create_paragraph(rand, soup, [3,12]))
        list_elem.append(li)
    return list_elem 

_table_styles = ['fullgrid','outteronly',[]]
def create_table(rand,
                 soup,
                 row_range=[2, 8],
                 col_range=[2, 5],
                 header_word_range=[1, 5],
                 header_col_max=1,
                 header_row_max=1,
                 header_bold_prob = 0.5,
                 value_len_range=[1, 4],
                 cell_word_range=[1, 10],
                 cell_sub_row_range=[1, 4],
                 ):
    table = soup.new_tag('table')
    table['class'] = rand.choice(_table_styles)
    tbody = soup.new_tag('tbody')
    table.append(tbody)
    rows = sample_discrete_normal(rand, *row_range)
    columns = sample_discrete_normal(rand, *col_range)
    bold = rand.rand() < header_bold_prob
    for r in xrange(rows):
        tr = soup.new_tag('tr')
        for c in xrange(columns):
            td = soup.new_tag('td')
            if c < header_col_max or r < header_row_max:
                
                p = create_paragraph(rand, soup, header_word_range, bold = bold and r < header_row_max)
            else:
                p = create_paragraph(rand, soup, value_len_range, numerical=True)
            td.append(p)
            tr.append(td)
        tbody.append(tr)
    return table

# HTML generation pipeline
def create(seed,
           head_prob = 0.8,
           two_col_prob = 0.3,
           section_range = [5,9]):
    '''
    Creates the same html for a given seed
    '''
    rand = RandomState(seed)
    soup = BeautifulSoup(_template, 'html.parser')
    if rand.rand() < head_prob:
        soup.body.insert(0, create_header(rand, soup, level=1))
    content = soup.body.div
    if rand.rand() < two_col_prob:
        content['class'] = 'col2'
    def append_section(new_elem, header_level = 0):
        div = soup.new_tag('div')
        if header_level > 0:
            div.append(create_header(rand, soup, level = header_level))
        div.append(new_elem)
        content.append(div)
    actions = [lambda:append_section(create_paragraph(rand, soup)),
               lambda:append_section(create_table(rand, soup), header_level = 3),
               lambda:append_section(create_list(rand, soup), header_level = 3)]
    section_count = sample_discrete_normal(rand, *section_range)
    for _sec_i in xrange(section_count):
        action = rand.choice(actions)
        action()
        
    return soup
