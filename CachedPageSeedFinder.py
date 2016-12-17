"""
Cached Page Seed Finder

This command line tool/lib help you find some webpages you want still live in Cached Page Server.

Usage:
  CachedPageSeedFinder.py domain <domain> [--output=<ofname>] [--input=<dfname>] [--ignore=<list>]
  CachedPageSeedFinder.py (-h | --help)
  CachedPageSeedFinder.py --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  --ignore=<list> Ignore url with filter list. Split input use separator ',' ex. --ignore=key1,key2

"""

import inspect

from docopt import docopt
import requests
from bs4 import BeautifulSoup
import os.path

cachedPageURL = 'https://web.archive.org/'

def getCachedPpageLink(domain, test, ignore):

    if (test != None) and (os.path.exists(test) == True):
        testFile = open(test,"r")
        context = testFile.read()
        testFile.close()
        #print inspect.currentframe().f_lineno
    else:
        res = requests.get(cachedPageURL + 'web/*/' + domain + '*')
        context = res.text.encode("utf-8")
        #print inspect.currentframe().f_lineno

    soup = BeautifulSoup(context, "html.parser")

    linkCollector = []
    for item in soup.select('.url'):
        href = item.select('a')
        if len(href) > 0:
            add = True
            if ignore != None:
                for filter in ignore.split(','):
                    if href[0].text.find(filter) != -1:
                        add = False

            if add == True:
                linkCollector.append(cachedPageURL + 'web/2/' +
                                     href[0].text.encode("utf-8").replace(':80', ''))

    return linkCollector

if __name__ == '__main__':
    arguments = docopt(__doc__, version='CachedPageSeedFinder 0.1')
    #print arguments
    table = getCachedPpageLink(arguments['<domain>'], arguments['--input'], arguments['--ignore'])

    if (arguments['--output'] != None) and (len(arguments['--output']) > 0):
        thefile = open(arguments['--output'], "w")
        for link in table:
            print>>thefile, link
        thefile.close()
