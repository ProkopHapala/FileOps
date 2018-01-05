
import re

# https://stackoverflow.com/questions/13361766/regex-issue-in-making-a-markdown-parser
# string = re.sub('^#{1}([^#].*)$', '<h1>\\1</h1>', string, flags=re.MULTILINE)

# https://stackoverflow.com/questions/6695439/how-to-link-to-a-named-anchor-in-multimarkdown

# https://stackoverflow.com/questions/250271/python-regex-how-to-get-positions-of-matches

# https://stackoverflow.com/questions/2403122/regular-expression-to-extract-text-between-square-brackets
"\[(.*?)\]"

#[line for line in open('file.txt') if re.match(r'f\(\s*([^,]+)\s*,\s*([^,]+)\s*\)',line)]

re_links   = None
re_labels  = None 

def findLabels(lines ):
    global re_links
    if re_links is None:
        #re_links = re.compile( "^#([^#].*)$", re.MULTILINE)
        re_links = re.compile( "^#(.*)$", re.MULTILINE)
    #for m in p.finditer('a1b2c3d4'):
    #    print m.start(), m.group()
    #return [ i for i,line in enumerate(lines) if re_links.match(line) ]
    #return [ re_links.match() for line in lines if line) ]
    results = []
    for i,line in enumerate(lines):
        match = re_links.match(line)
        if ( match ):
            results.append( (i,match.start(),match.end()) )
    return results


def findLinks(lines):
    if re_links is None:
        re_links = re.compile( "\[(.*?)\]", re.MULTILINE)


if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f: 
        print findLabels(f.readlines())
