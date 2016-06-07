
import os
import sys

from bibtex_journals import journals

# ============ CONSTANST

bib_classes = [ "@article{", "@book{", "@inbook{" ]

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

def toDict2( items, warn_duplicates=True ):
	keys = []
	dct  = {}
	for i,item in enumerate( items ):
		label = item[0]
		if label in dct:
			if warn_duplicates:
				print "duplicate label '%s' at %i " %(label,i)
			continue
		dct[label] = item
		keys.append(label)
	return dct,keys 

def selectByLabel( labels, items, dct=None, warn_duplicates=True, warn_missing=True ):
	if dct is None:
		dct,junk = toDict2( items, warn_duplicates=warn_duplicates )
	selected = []
	for label in labels:
		if label in dct:
			selected.append( dct[label] )
		else:
			if warn_missing:
				print "missing label '%s'" %label
	return selected
	
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
					val = ls[1].strip()
					if val[-1] != ',':
						val=val+','
					item[1][key] = val
				elif warn_unknown:
					print "unknown key '%s' in '%s'" %(key,item[0])
			elif "}" in line:
				articles.append(item)
				item = None
				continue
		elif "@article" in line:
			label = line.split("{",1)[1].strip().strip(',')
			item = (label,{},fname)
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

def find_duplicates_label( bibitems, verbose=True ):
	dct        = {}
	collisions = []
	for i,item in enumerate( bibitems ):
		if item[0] in dct:
			dct[item[0]].append(i)
			collisions.append( ( dct[item[0]][0], i ) )
			if verbose:
				print "duplicate label '%s' (%i,%i) " %( item[0], dct[item[0]][0], i )
		else:
			dct[item[0]]=[i]
	return collisions

def find_duplicates_label_files( bibitems, fname, dct, verbose=True ):
	collisions = []
	for i,item in enumerate( bibitems ):
		label = item[0]
		if label in dct:
			coll = ( dct[label], fname )
			collisions.append( coll )
			if verbose:
				print "label '%s' from '%s' previously declared in '%s'" %( label, coll[1], coll[0] )
		else:
			dct[label]=fname
	return collisions


def find_duplicates( bibitems, by_aspects=['title'], warn_no_key=True ):
	dct        = {}
	collisions = []
	for i,item in enumerate( bibitems ):
		hstr = ""
		for aspect in by_aspects:
			if aspect in item[1]:
				hstr = hstr + item[1][aspect].strip().strip('{},')
			elif warn_no_key: print "no key %s in %i %s" %(aspect,i,item[0])
		if ( len(hstr)>0 ) and (hstr in dct):
			j = dct[hstr]
			print " %i %s in %s colide with %i %s in %s " %(j,bibitems[j][0],bibitems[j][2],i,bibitems[i][0],bibitems[i][2]) 
			print "'%s'" %hstr
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

# ============ Citations in Latex

def findCitations( fname, dct = {} ):
	lst = []
	fin = open( fname, 'r' )
	i = 0
	for line in fin:
		if "\cite{" in line:
			toks = line.split( "\cite{" )[1:]
			for tok in toks:
				cites = tok.split("}")[0]
				for cit in cites.split(","):
					cit = cit.strip()
					if cit in dct:
						dct[cit].append( i ) 
					else:
						dct[cit] = [i] 
						lst.append( cit )
					#print i,cit
				i+=1
	fin.close()
	return lst,dct

def replaceCitations( fin, fout, replace_dict ):
	fin  = open( fin, 'r' )
	fout = open( fout, 'w' )
	nrep = 0
	for line in fin:
		if "\cite{" in line:
			toks = line.split( "\cite{" )
			line_list = [ toks[0] ]
			for tok in toks[1:]:
				line_list.append( "\cite{" )
				cites = tok.split("}",1)
				citlst = cites[0].split(",")
				for j,cit in enumerate(citlst):
					cit = cit.strip()
					if cit in replace_dict:
						print "replacing '%s' --> '%s' " %(cit,replace_dict[cit])
						cit = replace_dict[cit]						
						nrep += 1
					line_list.append( cit )
					if j < len(citlst)-1:
						line_list.append( ',' )
				line_list.append( "}"+cites[1] )
			line = "".join( line_list )
		fout.write(line)
	fout.close()
	fin.close()
	return nrep






