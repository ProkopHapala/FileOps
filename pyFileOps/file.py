
import sys
import os
import hashlib
import shutil

# ==== General utils

DEFALUT_CHUNK_SIZE = 8*1024

def chunk_reader(fobj, chunk_size=DEFALUT_CHUNK_SIZE, maxChunks=1000000000 ):
	"""Generator that reads a file in chunks of bytes"""
	#while ( i < maxChunks ):
	for i in xrange( maxChunks ):
		chunk = fobj.read(chunk_size)
		if not chunk:
			return
		yield chunk

def fileBitCompare( fname1, fname2, chunk_size=DEFALUT_CHUNK_SIZE, maxChunks=1000000000 ):
	fp1 = open( fname1, 'rb')
	fp2 = open( fname2, 'rb')
	#while True:
	for i in xrange( maxChunks ):
		chunk1 = fp1.read(chunk_size)
		chunk2 = fp2.read(chunk_size)
		if chunk1 != chunk2:
			fp1.close()
			fp2.close()
			return False
		if not chunk1:
			break
	fp1.close()
	fp2.close()
	return True

def hashFile( full_path, chunk_size=1024, maxChunks=1000000000, hashFunc=hashlib.sha1, seed="some seed" ):
	fin = open(full_path, 'rb')
	hashobj = hashFunc()
 	for chunk in chunk_reader( fin, chunk_size=chunk_size, maxChunks=maxChunks ):
		hashobj.update(chunk)
	hashobj.update( seed )
	fin.close()
	return hashobj.digest()

def dictByComponent( items, icomp ):
	dic = {}
	for item in items:
		key = item[icomp]
		if key in dic:
			dic[ key ].append(item)
		else:
			dic[ key ]=[item]
	return dic

def writeMatchList( matchList, fout=sys.stdout ):
	for match in matchList:
		file_i  = match[0]
		matches = match[1]
		fout.write( os.path.join(file_i[1], file_i[0])+ "\n" )
		for file_j in matches:
			fout.write( " -> " + os.path.join(file_j[1], file_j[0]) + "\n" )

def writeFileList( items, fout=sys.stdout ):
	for file_i in items:
		fout.write( os.path.join(file_i[1], file_i[0])  + "\n" )

# ==== Main algorithm	

def path2list( path, maxChunks=0, hashFunc=hashlib.sha1, echoPerNFiles = -1 ):
	nbytes = 0
	items = []
	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			full_path = os.path.join(dirpath, filename)
			rel_path  = os.path.relpath( dirpath, path)
			size      = os.path.getsize(full_path)
			hashval   = None
			if ( maxChunks > 0 ):
				hashval = hashFile( full_path, maxChunks=maxChunks, seed=str(size) )
			item = [ filename, rel_path, size, hashval ]
			items.append( item )
			if( echoPerNFiles > 0 ):
				nbytes+=size
				nfiles  = len(items)
				if( nfiles%echoPerNFiles == 0 ):
					print "files %i bytes %i   %s" %( nfiles, nbytes, full_path )
	return items


'''
def findDuplicates( path, maxChunks=1, hash=hashlib.sha1 ):
	hashes     = {}
	duplicates = []
	for path in paths:
		for dirpath, dirnames, filenames in os.walk(path):
			for filename in filenames:
				full_path = os.path.join(dirpath, filename)
				hashval = hashFile( full_path, maxChunks=maxChunks )
				file_id = ( hashval, os.path.getsize(full_path))
				duplicate = hashes.get(file_id, None)
				if duplicate:
					print "Duplicate found: %s and %s" % (full_path, duplicate)
				else:
					hashes[file_id] = full_path
'''

def extractBitEqual( ref, items, path, maxChunks=0 ):
	eq  = []
	neq = []
	ref_path = os.path.join( path, os.path.join( ref[1], ref[0] ) )
	for item in items:
		same     = False 
		if( ref[2] == item[2] ):
			item_path = os.path.join( path, os.path.join( ref[1], ref[0] ) )
			same      = fileBitCompare( ref_path, item_path, maxChunks=maxChunks )				
		if same:
			eq.append ( item )
		else:
			neq.append( item )
	return eq, neq

def findDuplicates( items, path, maxChunks=0 ):
	duplicates = []
	dic        = dictByComponent( items, 3 )   # hash-table based on hash
	for key,val in dic.iteritems():
		nhits = len(val)
		if nhits > 1:
			ref   = val[0 ]
			items = val[1:]
			while True:
				eq, neq = extractBitEqual( ref, items, path, maxChunks=0 )
				if len(eq) > 0:
					duplicates.append( [ref, eq] )
				if len(neq) < 2:
					break
				else:
					ref   = neq[0 ]
					items = neq[1:]
	return duplicates

def findCopies( items1, items2, path1, path2, maxChunks=0 ):
	#same      = []
	moved      = []
	notFound   = []
	size_dic   = dictByComponent( items2, 2 )
	#print size_dic
	for file_i in items1:
		#found = False
		size_i     = file_i  [2     ]		
		if size_i in size_dic: # search by file size 
			copies = []
			candidates  = size_dic[size_i]
			rel_name_i  = os.path.join(file_i[1], file_i[0])	
			full_path_i = os.path.join( path1, rel_name_i	)
			for file_j in candidates:
				if( file_j[3] == file_i[3] ):  # check hash
					full_path_j  = os.path.join( path2, os.path.join( file_j[1], file_j[0] )	)
					#print 
					#print "comparing files"
					#print full_path_i
					#print full_path_j
					check_passed = fileBitCompare( full_path_i, full_path_j, maxChunks=maxChunks )
					if( check_passed ):
						# TODO : check if are really the same ( not just hash )
						rel_name_j = os.path.join(file_j[0], file_j[1])
						if rel_name_i != rel_name_j:	# check file name					
							copies.append( file_j )
						#else:
							found = True
			if copies:
				moved.append( [ file_i, copies ] )
			#if found :
			#	same.append( file_i )
		else:
			notFound.append( file_i )
	return moved, notFound #, same	

def copyItems( items, src_path, dst_path ):
	for item in items:
		abs_path = os.path.join( dst_path, item[1] )
		if not os.path.isdir( abs_path ):
			os.makedirs( abs_path )
		src = os.path.join( os.path.join( src_path, item[1] ), item[0] )
		dst = os.path.join( abs_path, item[0] )
		print "copy: "
		print src
		print dst
		print 
		shutil.copyfile(src, dst)

def copyItemsSafe( items, src_path, dst_path, checkNChunk=0, DO_IT=True ):
	conflicts = []
	for item in items:
		abs_path = os.path.join( dst_path, item[1] )
		src = os.path.join( os.path.join( src_path, item[1] ), item[0] )
		dst = os.path.join( abs_path, item[0] )
		#print 
		#print src
		#print dst
		if not os.path.isdir( abs_path ):
			if( DO_IT ):
				os.makedirs( abs_path )
		elif os.path.isfile( dst ):
			src_size  = os.path.getsize(src)
			dst_size  = os.path.getsize(dst)
			same_files = False
			if ( src_size == dst_size ):
				same_files = fileBitCompare( src, dst, maxChunks=checkNChunk )
			if not same_files:
				conflicts.append( item )
				#print " conflict ! " 
			#else:
			#	print " same => ignore " 
			continue
		#print " copying " 
		if( DO_IT ):
			shutil.copyfile(src, dst)
	return conflicts
		
'''
def sync_list( path1, path2, hashLeve=0 ):
	items1 = path2list( path1, hashLeve=hashLeve )
	items2 = path2list( path2, hashLeve=hashLeve )
	#print " ====== items1 ======= "
	#writeFileList( items1 )
	#print " ====== items2 ======= "
	#writeFileList( items2 ) 
	moved, notFound, same = findCopies( items1, items2, path1, path2 )
	print
	print " ====== MOVED FILES ======= "
	print 
	writeMatchList( moved )
	print
	print " ====== NOT FOUND FILES ======= "
	print 
	writeFileList( notFound )
	print
	#print " ====== SAME FILES ======= "
	#print 
	#writeFileList( same )
	copyItems( notFound, path1, path2 )
'''



