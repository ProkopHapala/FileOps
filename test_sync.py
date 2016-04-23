import sys
import pyFileOps.file as fops

path1 = sys.argv[1]
path2 = sys.argv[2]

fops.sync_list( path1, path2, hashLeve=0 )
