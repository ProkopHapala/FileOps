import sys
import pyFileOps.file as fops

path = sys.argv[1]

items                = fops.path2list( path, maxChunks =10, echoPerNFiles=100 )                      # hash items using first 100 kb

#duplicates, notFound = fops.findCopies    ( items, items, path, path, maxChunks=1000000000 ) # find copies with exact check ( full file content )
duplicates = fops.findDuplicates( items, path, maxChunks=1000000000 ) # find copies with exact check ( full file content )

fops.writeMatchList( duplicates, fout = open( "duplicates.log", 'w'    ) ) 

print 
print " ==== DUPLICATES FOUND : "
fops.writeMatchList( duplicates ) 

