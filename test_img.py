import sys
import pyFileOps.image as im
        
app = im.ImageViewer()
app.getFileList( sys.argv[1] )     
app.MainLoop()        

