"""
a simplistic tool for fetching and parsing ADN sequences at ebi.ac.uk
"""

import requests


def ebi_url(key:str) -> tuple[str, dict]:
    """
    returns a URL and associated params
    """
    return (f"http://www.ebi.ac.uk/ena/browser/api/embl/{key}",
            { 'download': 'true'})


def download(url, params, verbose=False):
    """
    the actual download - discards obvious failures
    """

    response = requests.get(url, params=params)
    text = response.text
    if 'not supported' in text:
        print("WARNING: url=", url)
        print("  a retourné", text)
    if verbose:
        print("url=", url)
        print("text=", text)
    print(f"download {url} returns {len(text)} chars")
    return text


def valid_contents(line):
    """
    keeps only the contents that has nucleotides
    """
    return "".join( [ x.upper() for x in line if x.lower() in ('c', 'a', 'g', 't')])


def parse(text):
    """
    rough parsing of the .txt format
    """
    in_sequence = False
    result = ""
    for line in text.split("\n"):
        # print(f"line {line}")
        start = line[:2]
        if start == 'SQ':
            in_sequence = True
        elif start == '  ' and in_sequence:
            result += valid_contents(line)
        elif start == '//':
            in_sequence = False
    return result


def fetch(key):
    """
    one-stop shopping
    """
    url, params = ebi_url(key)
    try:
        return parse(download(url, params))
    except Exception as e:
        print(f"Impossible d'aller chercher la clé {key}")
        return str(e)


# how to display our own source code
import inspect
def list_module(module):
    lines, lineno = inspect.getsourcelines(module)
    for line in lines:
        print(line, end="")
