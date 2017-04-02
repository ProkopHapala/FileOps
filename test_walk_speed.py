#!/usr/bin/python

import pyFileOps.file as fops
import scandir 
import os     
import time

def countFiles( path, dir_walk ):
	nfiles = 0
	ndirs  = 0
	for dirpath, dirnames, filenames in dir_walk(path):
		nfiles += len(filenames)
		ndirs  += len(dirnames)
	return nfiles, ndirs

path = "/home/prokop/Dropbox/MyDevSW"
path = "/home/prokop/Dropbox"

path = "/home/prokop/git_SW"


t1=time.clock()
nfiles, ndirs = countFiles( path, dir_walk=os.walk )
t2=time.clock()
print "======== os.walk      : nfiles %i ndirs %i time %f [s]"  %(nfiles, ndirs,t2-t1)

t1=time.clock()
nfiles, ndirs = countFiles( path, dir_walk=scandir.walk )
t2=time.clock()
print "======== scandir.walk : nfiles %i ndirs %i time %f [s]" %(nfiles, ndirs,t2-t1)


'''
t1=time.clock()
fops.path2list( path, maxChunks=0, echoPerNFiles = 1000, dir_walk=os.walk )
t2=time.clock()
print "======== os.walk     : %s [s]"  %(t2-t1)

t1=time.clock()
fops.path2list( path, maxChunks=0, echoPerNFiles = 1000, dir_walk=scandir.walk )
t2=time.clock()
print "======== scandir.walk: %s [s]" %(t2-t1)
'''
