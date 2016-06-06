from pyFileOps import bibtex

bibtex.init()
#print bibtex.bibtex_keys_dict

bibitems = bibtex.loadBibtex( 'my_citations.bib' )

#collisions = bibtex.find_duplicates( bibitems )
#collisions = bibtex.find_duplicates( bibitems, by_aspects=['doi'] )
#print collisions

dct_of_journals = bibtex.dictOfVals( bibitems, aspect='journal' )

print sorted(dct_of_journals) 

#print bibitems

fout = open( 'test.bib', 'w' )
bibtex.toFile( fout, bibitems )
fout.close()
