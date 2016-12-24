# CachedPageSeedFinder
This command line tool/lib help you find some webpages you want still alive in Cached Page.


**Warning: add --history parameter. Be careful it's need to spend a lot of time if the request domain include so many pages.**


### Usage:
* CachedPageSeedFinder.py domain \<domain\> [--output=\<ofname\>] [--input=\<dfname\>] [--ignore=\<list\>]
* CachedPageSeedFinder.py (-h | --help)
* CachedPageSeedFinder.py --version

### Options:
* -h --help            Show this screen.
* --version            Show version.
* --output=<ofname>    Output all links to a file
* --ignore=<list>      Ignore url with filter list.
                       Split input use separator ',' ex. --ignore=key1,key2
* --history            Get whole domain link with all history
* --debugfile=<dfname> Debug only. Test parse link function use an input file.