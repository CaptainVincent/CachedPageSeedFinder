"""
< Cached Page Seed Finder >
This command line tool/lib help you find some webpages you want still live in Cached Page Server.

Usage:
  CachedPageSeedFinder.py domain <domain> [--output=<ofname>] [--debugfile=<dfname>] [--ignore=<list>] [--history]
  CachedPageSeedFinder.py (-h | --help)
  CachedPageSeedFinder.py --version

Options:
  -h --help            Show this screen.
  --version            Show version.
  --output=<ofname>    Output all links to a file
  --ignore=<list>      Ignore url with filter list.
                       Split input use separator ',' ex. --ignore=key1,key2
  --history            Get whole domain link with all history
  --debugfile=<dfname> Debug only. Test parse link function use an input file.

"""

import inspect

from docopt import docopt
import requests
from bs4 import BeautifulSoup
import os.path

cachedPageURL = 'https://web.archive.org/'

def getCachedPageLink(domain, debugfile, ignore, history):

    if (debugfile != None) and (os.path.exists(debugfile) == True):
        testFile = open(debugfile,"r")
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
            if (ignore != None) and (len(ignore) > 0) :
                for filter in ignore.split(','):
                    if href[0].text.find(filter) != -1:
                        add = False
            if add == True:
                linkCollector.append(href[0].text.encode("utf-8").replace(':80', ''))

    ConvertLinkCollector = []
    if history == True:
        for item in linkCollector:
            res = requests.get(cachedPageURL + 'web/*/' + item)
            soup = BeautifulSoup(res.text.encode("utf-8"), "html.parser")
            for link in soup.select('.captures'):
               ConvertLinkCollector.append(cachedPageURL + link.find('a').get('href'))
    else:
        for item in linkCollector:
            ConvertLinkCollector.append(cachedPageURL + 'web/2/' + item)

    return ConvertLinkCollector


if __name__ == '__main__':
    arguments = docopt(__doc__, version='CachedPageSeedFinder 0.2')
    print arguments
    table = getCachedPageLink(arguments['<domain>'], arguments['--debugfile'], arguments['--ignore'], arguments['--history'])

    if (arguments['--output'] != None) and (len(arguments['--output']) > 0):
        thefile = open(arguments['--output'], "w")
        for link in table:
            print>>thefile, link
        thefile.close()
