from pyFileOps import bibtex

bibtex.init()

bibfiles = ['introduction.bib','Fireball.bib','transport.bib','HRI.bib','SiNC.bib']
texfiles = ['introduction.tex','transport.tex','HRI.tex','HRSTM.tex','SiNC.tex']

'''
for bibfile in bibfiles:
	print 
	print "=========== FILE : ", bibfile
	print
	bibitems = bibtex.loadBibtex( bibfile )
	print ">>> checking journals..."
	bibtex.check_journals( bibitems, normalize=0 )
'''

replace_dict = {
'Binnig1986':'Binnig1986_ert7987',
'Pavlicek_PRL12': 'Pavlicek_PRL12_SDFSDF', 
'Zhang2013': 'Zhang2013_ASDASDAS', 
'Weiss2010': 'Weiss2010_sdfg778', 
'PavlicekNatChem2015': 'PavlicekNatChem2015_797879', 
'Holscher1996': 'Holscher1996_978797', 
'Sweetman2014': 'Sweetman2014_58797', 
'Richmond1984': 'Richmond1984_48787', 
'Bengtsson2000': 'Bengtsson2000_SDFSDFSDF', 
'Hamalainen2014': 'Hamalainen2014_79DFSD', 
'Hapala_Book_2015': 'Hapala_Book_2015_66664', 
'Hapala_electro_distortion': 'Hapala_578787',
}

for fname in texfiles:
	print 
	print "=========== FILE : ", fname
	print
	#cite_dict = bibtex.findCitations( fname )
	#print cite_dict
	bibtex.replaceCitations( fname, "_"+fname, replace_dict )





