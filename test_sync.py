import sys
import pyFileOps.file as fops

path1 = sys.argv[1]
path2 = sys.argv[2]

#fops.sync_list( path1, path2, hashLeve=0 )

hashLeve=0
items1 = fops.path2list( path1, hashLeve=hashLeve )
items2 = fops.path2list( path2, hashLeve=hashLeve )
moved, notFound = fops.findCopies( items1, items2, path1, path2 )

fops.writeMatchList( moved    , fout = open( "moved.log", 'w'    ) ) # these files from "path1" have some equivalent in "path2"; with different name; maybe more
fops.writeFileList ( notFound , fout = open( "notFound.log", 'w' ) ) # these files from "path1" does not have equivalent in "path2"; 

conflicts = fops.copyItemsSafe( notFound, path1, path2, checkNChunk=0, DO_IT=False )
fops.writeFileList ( conflicts, fout = open( "conflicts.log", 'w' )  )
print " ==== COPY CONFLICTS : "
fops.writeFileList ( conflicts )

