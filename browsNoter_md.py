#!/usr/bin/python

import os
import wx
import sys
#import shutil
import pyFileOps.file as fops

# developed by help of : https://wiki.wxpython.org/AnotherTutorial

class MyTextDropTarget(wx.TextDropTarget):

    def __init__(self, object):
        wx.TextDropTarget.__init__(self)
        self.object = object

    def onDropText(self, x, y, data):
        self.object.InsertStringItem(0, data)

class MyPopupMenu(wx.Menu):
    def __init__(self, app):
        wx.Menu.__init__(self)
        self.app = app
        item1 = wx.MenuItem(self, wx.NewId(), "Open File");   self.AppendItem(item1); self.Bind(wx.EVT_MENU, self.onOpenFile,   item1)
        item2 = wx.MenuItem(self, wx.NewId(), "Open Folder"); self.AppendItem(item2); self.Bind(wx.EVT_MENU, self.onOpenFolder, item2)
      
    def osOpen(self, full_path ):
        if sys.platform == 'linux2':
            os.system('xdg-open %s' %full_path) 
        else:
            os.system('start %s' %full_path)   

    def onOpenFile(self, event):
        print "Open File : ", self.app.i_select
        item = self.app.found_items[self.app.i_select][0];    # print "external open   : ", item
        abspath   = os.path.join(self.app.txtDir.GetValue(), item[1])
        full_path = os.path.join(abspath, item[0]);           # print full_path
        self.osOpen( full_path )
        
    def onOpenFolder(self, event):
        print "Open Folder : ", self.app.i_select
        item = self.app.found_items[self.app.i_select][0];    # print "external open   : ", item
        abspath   = os.path.join(self.app.txtDir.GetValue(), item[1])        
        self.osOpen( abspath )

class MyFrame(wx.Frame):
    #root_path   = ""
    #includes=['.c','.cpp','.h','.cl','.py']
    #excludes=['.png','.bmp','.jpg','.jpeg','.tif','.tiff','.gif']
    #search_str = 'virtual'
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(640, 480))
        splitter1 = wx.SplitterWindow(self     , -1, style=wx.SP_3D, size=(100,100))
        splitter2 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D, size=(100,100))
        splitter3 = wx.SplitterWindow(splitter1, -1, style=wx.SP_3D, size=(100,100))
        
        panel = wx.Panel(splitter3, -1, size=(100,100) )
        box = wx.BoxSizer(wx.VERTICAL)
        self.txtDir  = wx.TextCtrl(panel, -1); self.txtDir.SetValue( '/home/prokop/Dropbox/MyDevSW' )
        self.txtExt  = wx.TextCtrl(panel, -1); self.txtExt.SetValue('*.c;*.cpp;*.h;*.cl;*.py')
        self.txtStr  = wx.TextCtrl(panel, -1); self.txtStr.SetValue('virtual')
        box.Add(self.txtDir, 1, wx.EXPAND | wx.ALL, 3)
        box.Add(self.txtExt, 1, wx.EXPAND | wx.ALL, 3)
        box.Add(self.txtStr, 1, wx.EXPAND | wx.ALL, 3)
        panel.SetSizer(box)
        
        self.dir  = wx.GenericDirCtrl(splitter3, -1, dir=self.txtDir.GetValue(), size=(500,100), style=wx.DIRCTRL_DIR_ONLY)
        #self.lc1  = wx.ListCtrl(splitter2, -1, size=(100,100), style=wx.LC_LIST)
        self.lc1 = wx.ListCtrl(splitter2, -1, size=(200,100), style=wx.LC_REPORT)
        self.lc1.InsertColumn(0, 'file'); self.lc1.SetColumnWidth(0, 200)
        self.lc1.InsertColumn(1, 'path'); self.lc1.SetColumnWidth(1, 300)
        
        self.text = wx.TextCtrl(splitter2, 1000, '', size=(100, 100), style=wx.TE_MULTILINE | wx.TE_RICH | wx.TE_PROCESS_ENTER)
        #self.text.SetFocus()
        
        # http://stackoverflow.com/questions/3570254/in-wxpython-how-do-you-bind-a-evt-key-down-event-to-the-whole-window
        # http://stackoverflow.com/questions/8707160/wxpython-capture-keyboard-events-in-a-wx-frame
        # http://stackoverflow.com/questions/3570254/in-wxpython-how-do-you-bind-a-evt-key-down-event-to-the-whole-window
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)
        #self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        wx.EVT_LIST_ITEM_SELECTED(self, self.lc1.GetId(), self.onFileSelect )
        tree = self.dir.GetTreeCtrl()
        splitter2.SplitHorizontally(self.lc1, self.text)
        splitter3.SplitHorizontally(panel, self.dir)
        splitter1.SplitVertically  (splitter3, splitter2)
        wx.EVT_TREE_SEL_CHANGED(self, tree.GetId(), self.onFolderSelect )
        self.Centre()
        
        self.lc1.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
        self.popup = MyPopupMenu(self)
    
    def onKeyDown(self, event):
        keycode = event.GetKeyCode()
        print keycode
        if keycode == wx.WXK_RETURN:
            self.searchPath()
        event.Skip()
        
    def onRightDown(self,event):
        #pos = event.GetPosition()   # for some reason returns position relative to lc1
        pos = self.ScreenToClient( wx.GetMousePosition() ) # a bit hack
        self.PopupMenu(MyPopupMenu(self), pos )

    def onFileSelect(self, event ):
        #i = len(self.found_items) - event.GetIndex() -1 # why like that? - probably list filled last-on-top; numbered from 1
        i = event.GetIndex()
        self.i_select = i
        item = self.found_items[i]
        #print i," ",item
        abspath   = os.path.join( self.txtDir.GetValue(), item[0][1])
        full_path = os.path.join(abspath, item[0][0])
        print full_path
        self.text.LoadFile( full_path )
        self.text.SetInsertionPoint(0)
        nch = len(self.txtStr.GetValue())
        for ichar in item[1]:
            self.text.SetStyle(ichar, ichar+nch , wx.TextAttr("black", "yellow"))

    def onFolderSelect(self, event):
        self.txtDir.SetValue( self.dir.GetPath() )
        self.searchPath()
         
    def searchPath(self):
        path            = self.txtDir.GetValue()    
        self.includes   = self.txtExt.GetValue().split(";") #print  self.includes
        self.search_str = self.txtStr.GetValue()            #print  self.includes
        items    = fops.path2list_filter( path, include=self.includes, echoPerNFiles=100 ) 
        found_is, founds = fops.searchInFiles   ( items, path, self.search_str )
        #self.lc1.ClearAll()
        self.lc1.DeleteAllItems()
        #print "found %i items" %len(found_is)
        found_items = []
        for ii,i in enumerate(found_is):
            print items[i][0]
            #self.lc1.InsertStringItem(0, items[i][0] )
            num_items = self.lc1.GetItemCount()
            self.lc1.InsertStringItem(num_items,    items[i][0] )
            self.lc1.SetStringItem   (num_items, 1, items[i][1] )
            #self.lc1.InsertStringItem(num_items, "Hey" )
            #self.lc1.SetStringItem   (num_items, 1, "How" )
            found_items.append( (items[i],founds[ii]) ) 
        self.found_items = found_items
        
class MyApp(wx.App):

    def OnInit(self):
        frame = MyFrame(None, -1, "BrowseNoter")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
