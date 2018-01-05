import sys
import os
import wx
import pyFileOps.file as fops
import random
import pickle

class ImageViewer(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')
        self.panel = wx.Panel(self.frame)
        self.maxW = 1920
        self.maxH = 1000
        self.createWidgets()
        self.frame.Show()
        self.ilist     = 0
        self.scoreDict = {}

    def getFileList(self,path):
        items = fops.path2list( path )
        self.path = path
        self.files = []
        for item in items:
            if ".jpg" in item[0]:
                #print( item )
                self.files.append([item[0],item[1],None])
            try:
                self.loadScore()
            except:
                print( "cannot load scoreDict" )
        
    def createWidgets(self):
        instructions = 'Browse for an image'
        img = wx.EmptyImage(240,240)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
        browseBtn = wx.Button(self.panel, label='Browse')
        browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY), 0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(browseBtn, 0, wx.ALL, 5)        
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        self.panel.SetFocus()

    def onKeyPress(self, event):
        keycode = event.GetKeyCode()
        #print( keycode )
        if keycode == wx.WXK_RIGHT:
            self.viewImageIndex(self.ilist+1)	
        elif keycode == wx.WXK_LEFT:
            self.viewImageIndex(self.ilist-1)
        elif  keycode == wx.WXK_DOWN:
            self.changeScore( self.files[self.ilist], -1 )
        elif  keycode == wx.WXK_UP:
            self.changeScore( self.files[self.ilist], +1 )
        else:
            try:
                ch = chr(keycode)
                print( "ch: ", ch )
                if ch == 'R':
                    print( "shuffling" )
                    random.shuffle(self.files)
                elif ch == 'S':
                    print "saving"
                    self.saveScore()
                elif ch == 'L':
                    print "loading"
                    self.loadScore()
                elif ch == '0':
                    self.changeScore_abs( self.files[self.ilist], 0 )
            except:
                pass
        event.Skip()
        #print( self.files[self.ilist] )

	def changeScore( self, item, dscore ):
		path = os.path.join( item[1], item[0] )
		if path in self.scoreDict:
			self.scoreDict[path] += dscore;
		else:
			self.scoreDict[path] = dscore;
		print( path, "score set to : ", self.scoreDict[path] )
		self.frame.SetTitle('Score: '+str(self.scoreDict[path])+ ' path:' + path )
		
	def changeScore_abs( self, item, score ):
		path = os.path.join( item[1], item[0] )
		self.scoreDict[path] = score;
		print( path, "score set to : ", self.scoreDict[path] )
		self.frame.SetTitle('Score: '+str(self.scoreDict[path])+ ' path:' + path )	

	def saveScore(self):
		fpath = os.path.join( self.path, 'image_scores.pkl' )
		fops.saveDict( fpath, self.scoreDict )
		#with open( fpath, 'wb') as f:
		#	print( "saving scores to :  ", fpath )
		#	pickle.dump( self.scoreDict, f, 0 )
		#	#pickle.dump( self.scoreDict, f, pickle.HIGHEST_PROTOCOL)

	def loadScore(self):
		fpath = os.path.join( self.path, 'image_scores.pkl' )
		dct = fops.loadDict( fpath, self.scoreDict )
		self.scoreDict = dct
		#print( self.scoreDict )

	def viewImageIndex(self, i ):
		#print( "view image ", i )
		n = len(self.files)
		if i < 0:
			i=n+i
		elif i >= n:
			i=i-n
		#print( "view image ", i )
		self.ilist = i
		item  = self.files[i]
		relpath = os.path.join( item[1], item[0] )
		filepath = item_path = os.path.join( self.path, relpath )
		self.viewImage( filepath )
		if relpath in self.scoreDict:
			self.frame.SetTitle('Score: '+str(self.scoreDict[relpath])+ ' path:' + relpath )
		else:
			self.frame.SetTitle('Score: None path:' + relpath )

	def viewImage(self, filepath, auto_zoom=True ):
		#print( filepath )
		try:
			img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
			# scale the image, preserving the aspect ratio
			W = img.GetWidth(); H = img.GetHeight();
			rescale_X   = float(W)/self.maxW
			rescale_Y   = float(H)/self.maxH
			rescale_max = max( rescale_X, rescale_Y  ); 
			#rescale_min = min( rescale_X, rescale_Y  ); 
			if    ( rescale_max > 1.0 ) or ( ( rescale_max < 1.0 ) and auto_zoom ):
				img = img.Scale( W/rescale_max, H/rescale_max )
			self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
			self.panel.Refresh()
			self.mainSizer.Fit(self.frame)
		except:
			print( "problem loading ", filepath )

	def onBrowse(self, event):
		wildcard = "JPEG files (*.jpg)|*.jpg"
		dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard, style=wx.OPEN)
		#if dialog.ShowModal() == wx.ID_OK:
		#	self.photoTxt.SetValue(dialog.GetPath())
		dialog.Destroy() 
		self.onView()

if __name__ == '__main__':
	app = im.ImageViewer() 
	app.getFileList("/home/prokop/Desktop/img")    
	app.MainLoop()   
