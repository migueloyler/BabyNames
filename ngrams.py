""" Miguel Oyler-Castrillo, Project 5, ngrams.py
"""

import requests
import re
from ast import literal_eval


def google_ngram_request(tokens, start_year, end_year):
    """
    Return the text of the google ngram results for a list of 'tokens'
    starting with 'start_year' and ending with 'end_year'
    Args:
        tokens (list of str):
        start_year (int):
        end_year (int):
    """
    string_request = ['%2C'+ i for i in tokens[1:]]
    request_string = 'http://books.google.com/ngrams/graph?content=' + tokens[0] + ''.join(string_request) + '&year_start=' + str(start_year) + '&year_end=' + str(end_year)
    req = requests.get(request_string)
    return req.text


def parse(text):
    """
    extract the data from a google ngram request.  Return a dictionary
    where keys are search terms and values are lists of percentages
    Args:
        text (str):
    """
    res = re.findall('var data = (.*?);\\n', text)
    if res:
        data = {qry['ngram']: qry['timeseries']
                for qry in literal_eval(res[0])}
        return data
    else:
        return None

if __name__ == '__main__':
    google_ngram_request(['allen', 'eric', 'sarah'], 1880, 2000)
