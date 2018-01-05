#!/usr/bin/python

# special characters:
'`'
'<'
'#'
'!['
'['
'$'

# https://stackoverflow.com/questions/10085568/slices-to-immutable-strings-by-reference-and-not-copy

'''
TODO:
    * multi-line code blocks
    * optimize speed
'''

def skipChars(s,i=0,c=' '):
    while(s[i]==c): i+=1
    return i

def skipWhite(s,i=0):
    while( (s[i]==' ') or (s[i]=='\t') ): i+=1
    return i

'''
class MdParser:
    def __init__():
        self.verb = False

    def linksInLine( ):
'''

def tryGetHeaderCaption(line):
    for i,c in enumerate( line ):
        if c==' ' or c=='\t': continue
        if c=='#':
            #print line
            j=i+1
            j=skipChars(line,i=i,c='#')
            #print line[j:].strip(),j-i
            return line[j:].strip(),j-i
        else:
            return None,i

def getLinksInLine( line, links, figs ):
    i = 0
    n = len(line)
    inverb=False
    while True:
        if i>=n: break
        c = line[i]
        if c=='`':
            #if (i+2<n): 
            #    if( line[i+1]=='`' and line[i+1]=='`' ):
            #        state.verb = not state.verb
            #        i+=2
            inverb= not inverb
        elif (c=='[') and not inverb:
            to = links
            if line[i-1]=='!':
                to = figs
            
            iend =line.index( ']', i )
            name = line[i+1:iend].strip()
            #i=skipWhite()
            i=skipChars(line,i=iend+1,c=' ')
            print line[iend:iend+10], "   ",  line[i:i+10]
            path=''
            if(line[i]=='('):
                iend=line.index( ')', i )
                path=line[i+1:iend]
            to.append( (name,path) )
        i+=1


def getLabels( f, headers=[], links=[], figs=[] ):
    #state={inverb:False}
    for line in f:
        header,i = tryGetHeaderCaption(line)
        #print header,i
        if header is not None:
            headers.append( (header,i) )
            #print headers
            continue
        else:
            getLinksInLine( line, links, figs )
    return headers, links, figs

