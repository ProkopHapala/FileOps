#!/usr/bin/python

import sys;     
sys.path.append("/home/prokop/git/FileOps")
from pyFileOps import bibtex; 
bibtex.init()

# ============= Hapala.tex

bibitems   = bibtex.loadBibtex( 'Hapala.bib' )
print [ item[0] for item in bibitems ]
bibtex.check_journals( bibitems, normalize=1 )
fout       = open( '_Hapala.bib', 'w' )
bibtex.toFile( fout, bibitems )
fout.close()


# ============= Main.tex

bibfiles = ['Hapala.bib','introduction.bib','Fireball.bib','transport.bib','HRI.bib','SiNC.bib']
texfiles = [ 'introduction.tex','transport.tex','HRI.tex','HRSTM.tex','SiNC.tex']

all_items = []
item_dct = {}
for fname in bibfiles:
	print 
	print "=========== FILE : ", fname
	print
	bibitems    = bibtex.loadBibtex( fname )
	colls       = bibtex.find_duplicates_label_files( bibitems, fname, item_dct )
	colls       = bibtex.find_duplicates( all_items, by_aspects=['title'] )
	bibtex.check_journals( bibitems, normalize=1 ) # convert journals to short version
	#print item_dct.keys()
	all_items  += bibitems 
	#colls = bibtex.find_duplicates_label( bibitems )
	#bibtex.find_duplicates( )
	#bibtex.check_journals( bibitems, normalize=0 )

print "=======================  Duplicates :  Title "
colls       = bibtex.find_duplicates( all_items, by_aspects=['title'] )
print "=======================  Duplicates :  doi "
colls       = bibtex.find_duplicates( all_items, by_aspects=['doi'], warn_no_key=False )
#print "=======================  Duplicates :  Title ", ['journal','year','volume']
#colls       = bibtex.find_duplicates( all_items, by_aspects=['journal','year','volume'] )

known_labes = {}
fmerged = open( 'used.bib', 'w' )
for fname in texfiles:
	print 
	print "=========== FILE : ", fname
	print
	new_labels,known_labes = bibtex.findCitations( fname, known_labes )
	new_items  = bibtex.selectByLabel( new_labels, all_items )
	print new_labels
	fmerged.write( "\n%%============= Occured in file %s \n\n" %fname  )
	bibtex.toFile( fmerged, new_items )
fmerged.close()
	



