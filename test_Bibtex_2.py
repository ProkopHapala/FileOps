from pyFileOps import bibtex

bibtex.init()

#bibfiles = ['Fireball.bib','HRI.bib','HRI.tex','HRSTM.tex','introduction.bib','SiNC.bib','transport.bib']
#texfiles = ['Greens_function.tex','HRI.tex','HRSTM.tex','introduction.tex','main.tex','MFF.tex','SiNC.tex','transport.tex']
bibfiles = ['introduction.bib','Fireball.bib','transport.bib','HRI.bib','SiNC.bib']
texfiles = ['introduction.tex','transport.tex','HRI.tex','HRSTM.tex','SiNC.tex']

#bibitems = []
#for bibfile in bibfiles:
#	bibitems += bibtex.loadBibtex( bibfile )
#dct_of_journals = bibtex.dictOfVals( bibitems, aspect='journal' )
#bibtex.list2file( 'journals.txt', sorted(dct_of_journals) )

for bibfile in bibfiles:
	print 
	print "=========== FILE : ", bibfile
	print
	bibitems = bibtex.loadBibtex( bibfile )
	print ">>> checking journals..."
	bibtex.check_journals( bibitems, normalize=0 )
	fout = open( "_"+bibfile, 'w' )
	bibtex.toFile( fout, bibitems )
	fout.close()




