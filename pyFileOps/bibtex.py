
import os
import sys

from bibtex_journals import journals

# ============ CONSTANST

aspects_main = [
'author',
'title',
'journal',
'year',
'volume',
'number',
'issue',
'pages',
'editor'
]
aspects_aux = [
'numpages',
'month',
'publisher',
'keywords',
'url',
]
aspects_DOIs = [
'doi',
'issn',
'isbn',
'pmid',
'arxivid',
]
aspects_local = [
'mendeley-groups',
'mendeley-tags',
'file',
'eprint',
'abstract',
]


bibtex_aspects = aspects_main + aspects_aux + aspects_DOIs + aspects_local

default_comment_aspects = aspects_aux + aspects_DOIs

bibtex_aspects_dict = {}


# ============ common functions

def init( ):
	global bibtex_aspects_dict
	bibtex_aspects_dict = { k:i for i,k in enumerate( bibtex_aspects ) }

def toDict( items ):
	keys = []
	dct  = {}
	for item in items:
		keys.append(item[0])
		dct[ item[0] ] = item[1]
	return dct,keys 

def dictOfVals( bibitems, aspect='journal', warn_no_key=True ):
	dct = {}
	for i,item in enumerate( bibitems ):
		if aspect in item[1]:
			val = item[1][aspect].strip().strip('{},"')
			if val in dct:
				dct[val].append(i)
			else:
				dct[val] = [i]
		elif warn_no_key: print "no key %s in %i %s" %(aspect,i,item[0]) 
	return dct



# ============ I/O Functions

def loadBibtex( fname, warn_unknown=True, strip__=True ):
	fin = open( fname, 'r' )
	articles = []
	item = None
	for line in fin:
		line_ = line.strip( )
		if item is not None:
			#print line
			if "=" in line:
				ls  = line.split("=",1)
				key = ls[0].strip().lower()
				if strip__: key = key.strip('_')
				if key in bibtex_aspects_dict:
					item[1][key] = ls[1].strip()
				elif warn_unknown:
					print "unknown key '%s' in '%s'" %(key,item[0])
			elif "}" in line:
				articles.append(item)
				item = None
				continue
		elif "@article" in line:
			label = line.split("{",1)[1].strip().strip(',')
			item = (label,{})
	fin.close()
	return articles

def toFile( fout, bibitems, use_aspects=aspects_main, comment_aspects=default_comment_aspects ):
	for item in bibitems:
		fout.write( "@article{%s,\n" %item[0] ) 
		for key in use_aspects:
			if key in item[1]:
				fout.write( "%s = %s\n" %(key,item[1][key]) )
		for key in comment_aspects:
			if key in item[1]:
				fout.write( "__%s = %s\n" %(key,item[1][key]) )
		fout.write( "}\n\n" ) 

def list2file( fname, lst ):
	fout = open( fname, 'w' )
	for item in lst:
		fout.write( item+"\n" )
	fout.close()

# ============ checking and analysis 

def find_duplicates( bibitems, by_aspects=['title'], warn_no_key=True ):
	dct        = {}
	collisions = []
	for i,item in enumerate( bibitems ):
		hstr = ""
		for aspect in by_aspects:
			if aspect in item[1]:
				hstr = hstr + item[1][aspect].strip().strip('{},')
			elif warn_no_key: print "no key %s in %i %s" %(aspect,i,item[0]) 
		if hstr in dct:
			j = dct[hstr]
			print " %i %s colide with %i %s" %(j,bibitems[j][0],i,bibitems[i][0]) 
			collisions.append( (j,i) )
		else:
			dct[hstr] = i
	return collisions

def check_journals( bibitems, journals=journals, normalize=-1 ):
	dct = {}
	full_dict    = { j[0].lower():j for j in journals };		dct.update(full_dict)
	abbrev_dict  = { j[1].lower():j for j in journals };		dct.update(abbrev_dict)
	#alias_dict   = { j[2].lower():j for j in journals };			dct.update(abbrev_dict)
	mangled_dict = { k.lower():j for j in journals for k in j[3] };	dct.update(mangled_dict)
	for i,item in enumerate(bibitems):
		if 'journal' not in item[1]:
			print "no 'journal' in %i '%s'" %(i,item[0])
			continue 
		journal = item[1]['journal'].strip().strip('{},"').lower()
		if journal in dct:
			if	normalize >= 0:
				item[1]['journal'] = "{%s}," %dct[journal][normalize]
		else:
			print "unknown journal '%s' in %i '%s'" %(journal,i,item[0])
			continue



