from pyFileOps import md
import os

fin = open('/home/prokop/Dropbox/MyDevSW/Markdown/test.md', 'r')

headers = []
links   = []
images  = []

md.getLabels( fin, headers, links, images )

print "headers", headers 
print
print "links",   links
print
print "images",  images


