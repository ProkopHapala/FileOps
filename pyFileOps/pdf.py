
import os
import sys

def search_word( word, lines ):
	found = []
	for i,line in enumerate(lines):
		j = line.find(word)
		if( j > -1 ):
			found.append( (i,j) )
	return found

def search_pdf( fname, words ):
	found_dic = { }
	tmp_name = "/tmp/pdfsearch_tmp.txt"
	command = "pdftotext "+fname+" "+tmp_name 
	print command
	os.system( command )
	ftmp  = open( tmp_name,'r') 
	lines = ftmp.readlines()
	ftmp.close()
	for word in words:		
		found_dic[ word ] = search_word( word, lines )
	return found_dic

def some_found( found_dic ):
	for val in found_dic.values():
		if( len(val) > 0 ):
			return True
	return False

def search_pdf_path( path, words ):
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			full_path = os.path.join(dirpath, filename)
			found_dic = search_pdf( full_path, words )
			if some_found( found_dic ):
				print full_path
				print found_dic

if __name__ == "__main__":
	#found_dic = search_pdf( sys.argv[1], sys.argv[2:] )
	#print found_dic
	search_pdf_path( sys.argv[1], sys.argv[2:] )
