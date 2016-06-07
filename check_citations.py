#!/usr/bin/python

import sys;     
sys.path.append("/home/prokop/git/FileOps")
from pyFileOps import bibtex; 
bibtex.init()

bibfiles = ['introduction.bib','Fireball.bib','transport.bib','HRI.bib','SiNC.bib']
texfiles = ['introduction.tex','transport.tex','HRI.tex','HRSTM.tex','SiNC.tex']


all_items = []
item_dct = {}
for fname in bibfiles:
	print 
	print "=========== FILE : ", fname
	print
	bibitems    = bibtex.loadBibtex( fname )
	all_items  += bibitems 
	#colls      = bibtex.find_duplicates_label_files( bibitems, fname, item_dct )
	#colls = bibtex.find_duplicates_label( bibitems )
	#bibtex.find_duplicates( )
	#bibtex.check_journals( bibitems, normalize=0 )

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
	



