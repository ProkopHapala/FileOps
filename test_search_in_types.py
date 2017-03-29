#!/usr/bin/python

import sys
import pyFileOps.file as fops
import os


ext_code = ['.c','.cpp','.h','.cl','.py']
ext_text = ['.md','.txt']

ext_doc    = ['.pdf','.ps','.dvi']
ext_vector = ['.svg', '.cdr'] 
ext_img    = ['.png','.bmp','.jpg','.jpeg','.tif','.tiff','.gif']
ext_movie  = ['.mov','.avi','.mpg']

path = sys.argv[1]
items = fops.path2list_filter( path, include=(ext_text+ext_code), echoPerNFiles=100 ) 
fops.writeFileList( items, fout=sys.stdout )
found_is = fops.searchInFiles( items, path, 'go back' )
print "==========="
fops.writeFileList( [ items[i] for i in found_is ], fout=sys.stdout ) 

#print items

'''
def walkTest(path):
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        print dirpath, dirnames, filenames
        items = []
        for filename in filenames:
            print "filename ", filename
            full_path = os.path.join(dirpath, filename)
            rel_path  = os.path.relpath( dirpath, path)
            size      = os.path.getsize(full_path)
            hashval   = None
    return items
       
walkTest(sys.argv[1])
'''

